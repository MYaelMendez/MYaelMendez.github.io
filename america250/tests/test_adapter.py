"""Contract tests against a mock server; no model inference is performed."""
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import gpt_oss_adapter as adapter

TASK = {"schema":"ae.america250.task.v1", "role":"build", "intent":"Offer", "selected_context":"Selected data"}
GOOD = {"model":"mock-gpt-oss", "choices":[{"finish_reason":"stop","message":{"content":json.dumps({"summary":"Draft", "artifact":"Offer draft", "evidence":[]})}}]}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.server.received = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(GOOD).encode())

    def log_message(self, *args):
        pass


class AdapterTests(unittest.TestCase):
    def test_mock_transport_and_pending_receipt(self):
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            r = adapter.run(TASK, f'http://127.0.0.1:{server.server_port}/v1')
            self.assertEqual(r['status'], 'pending_human_review')
            self.assertEqual(r['grants'], [])
            self.assertFalse(r['model']['weight_identity_verified'])
            self.assertEqual(r['task_hash'], adapter.digest(TASK))
            self.assertNotIn('tools', server.received)
            self.assertEqual(server.received['model'], 'gpt-oss:20b')
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_remote_and_redirect_rejected(self):
        for url in ['https://example.com/v1','http://localhost/v1','http://127.0.0.1.evil.test/v1','http://127.0.0.1/v1?x=1','http://user@127.0.0.1/v1']:
            with self.assertRaises(ValueError): adapter.endpoint(url)
        with self.assertRaises(ValueError): adapter.NoRedirect().redirect_request(None,None,302,'',{},'http://example.com')

    def test_imported_authority_rejected(self):
        with self.assertRaises(ValueError): adapter.validate_task({**TASK, 'grants':['execute']})

    def test_incomplete_or_tool_output_rejected(self):
        for choice in [{'finish_reason':'length','message':{'content':'{}'}},{'finish_reason':'stop','message':{'tool_calls':[{}],'content':'{}'}}]:
            with self.assertRaises(ValueError): adapter.parse_response({'choices':[choice]})

    def test_evidence_remains_unverified(self):
        c = {'summary':'Draft','artifact':'Text','evidence':[{'url':'https://example.com','note':'Reported reference'}]}
        r = adapter.parse_response({'choices':[{'finish_reason':'stop','message':{'content':json.dumps(c)}}]})
        self.assertEqual(r['evidence'][0]['verification'],'reported_unverified')

    def test_unsupported_schema_and_oversize_rejected(self):
        with self.assertRaises(ValueError): adapter.validate_task({**TASK,'intent':'x'*4001})
        with self.assertRaises(ValueError): adapter.request_body(TASK,'other-model')


if __name__ == '__main__': unittest.main()
