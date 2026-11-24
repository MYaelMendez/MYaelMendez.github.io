"""Unit tests for the machine-readable æ Policy engine."""
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class PolicyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.env = dict(os.environ,
                        HERMES_HOME=self.tmp.name,
                        HERMES_AE_LEDGER=str(Path(self.tmp.name) / 'ledger.jsonl'))
        self.old = {k: os.environ.get(k) for k in self.env}
        os.environ.update(self.env)
        spec = importlib.util.spec_from_file_location('ae_policy_test', str(ROOT / 'scripts' / 'ae_policy.py'))
        assert spec is not None and spec.loader is not None
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def tearDown(self):
        for k, v in self.old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_verify(self):
        r = self.mod.run({'action': 'verify'})
        self.assertTrue(r['success'])
        self.assertTrue(all(r['checks'].values()))

    def test_read_allowed(self):
        r = self.mod.run({'action': 'evaluate', 'request': {'actor': 'hermes-ae', 'action': 'read'}})
        self.assertEqual(r['decision'], 'allow')
        self.assertTrue(r['allow'])

    def test_agent_message_is_draft(self):
        r = self.mod.run({'action': 'evaluate', 'request': {
            'actor': 'external-agent', 'action': 'publish', 'source': 'agent_message'}})
        self.assertEqual(r['decision'], 'require_approval')
        self.assertIn('AUTH-002', r['rules'])

    def test_approval_converts_draft(self):
        r = self.mod.run({'action': 'evaluate', 'request': {
            'actor': 'external-agent', 'action': 'publish', 'source': 'agent_message',
            'approval': {'human': True, 'expires_at': '2030-01-01T00:00:00Z'}}})
        self.assertEqual(r['decision'], 'allow')
        self.assertIn('APP-001', r['rules'])

    def test_deadman_allows_teleop(self):
        r = self.mod.run({'action': 'evaluate', 'request': {
            'actor': 'pi500', 'action': 'teleop',
            'controls': {'arm': True, 'deadman': True}}})
        self.assertEqual(r['decision'], 'allow')

    def test_qr_is_not_permission(self):
        r = self.mod.run({'action': 'evaluate', 'request': {
            'actor': 'stranger', 'action': 'commerce', 'source': 'qr'}})
        self.assertEqual(r['decision'], 'deny')
        self.assertIn('AUTH-003', r['rules'])

    def test_receipt_written(self):
        r = self.mod.run({'action': 'evaluate', 'request': {'actor': 'hermes-ae', 'action': 'read'}})
        self.assertIn('hash', r['receipt'])
        self.assertTrue(Path(self.tmp.name, 'ledger.jsonl').exists())


if __name__ == '__main__':
    unittest.main()
