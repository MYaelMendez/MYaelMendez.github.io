"""Unit tests for the DAO Brain native head-viewport engine."""
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class DaoBrainTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env = dict(os.environ,
                   HERMES_HOME=self.tmp.name,
                   HERMES_AE_LEDGER=str(Path(self.tmp.name) / 'ledger.jsonl'),
                   HERMES_AE_FACE_STATE=str(Path(self.tmp.name) / 'face.json'))
        self.old = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        spec = importlib.util.spec_from_file_location('daobrain_test', str(ROOT / 'scripts' / 'daobrain.py'))
        assert spec is not None and spec.loader is not None
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def tearDown(self):
        for k, v in self.old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def face_state(self):
        return json.loads(Path(self.tmp.name, 'face.json').read_text())['dao_brain']['face_state']

    def test_proposal_awaits_approval(self):
        r = self.mod.run({'action': 'propose', 'actor': 'vision-model',
                          'source': 'vision-model', 'intent': 'publish'})
        self.assertEqual(r['decision'], 'require_approval')
        self.assertEqual(r['face_state'], 'AWAITING_APPROVAL')
        self.assertEqual(self.face_state(), 'AWAITING_APPROVAL')

    def test_approval_produces_approved_state(self):
        r = self.mod.run({'action': 'propose', 'actor': 'vision-model',
                          'source': 'vision-model', 'intent': 'publish',
                          'approval': {'human': True, 'expires_at': '2030-01-01T00:00:00Z'}})
        self.assertEqual(r['decision'], 'allow')
        self.assertEqual(r['face_state'], 'APPROVED')

    def test_deadman_teleop(self):
        r = self.mod.run({'action': 'propose', 'actor': 'pi500', 'intent': 'teleop',
                          'controls': {'arm': True, 'deadman': True}})
        self.assertEqual(r['face_state'], 'APPROVED')

    def test_qr_refused(self):
        r = self.mod.run({'action': 'propose', 'actor': 'stranger',
                          'source': 'qr', 'intent': 'commerce'})
        self.assertEqual(r['decision'], 'deny')
        self.assertEqual(r['face_state'], 'REFUSED')

    def test_read_only_listening(self):
        r = self.mod.run({'action': 'propose', 'actor': 'viewport', 'intent': 'read'})
        self.assertEqual(r['face_state'], 'LISTENING')

    def test_state_and_receipt(self):
        r = self.mod.run({'action': 'state', 'state': 'THINKING'})
        self.assertEqual(r['face_state'], 'THINKING')
        self.assertIn('hash', r['receipt'])
        self.assertTrue(Path(self.tmp.name, 'ledger.jsonl').exists())


if __name__ == '__main__':
    unittest.main()
