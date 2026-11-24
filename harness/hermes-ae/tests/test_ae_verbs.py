"""Unit tests for æ Robot Verbs."""
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class VerbTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env = dict(os.environ, HERMES_HOME=self.tmp.name,
                   HERMES_AE_LEDGER=str(Path(self.tmp.name) / 'ledger.jsonl'))
        self.old = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        spec = importlib.util.spec_from_file_location('ae_verbs_test', str(ROOT / 'scripts' / 'ae_verbs.py'))
        assert spec is not None and spec.loader is not None
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def tearDown(self):
        for k, v in self.old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_list(self):
        r = self.mod.run({'action': 'list'})
        self.assertTrue(r['success'])
        self.assertEqual(r['count'], 14)
        self.assertIn('stand', r['verbs'])
        self.assertIn('play_pcm', r['verbs'])

    def test_read_plan_allowed(self):
        r = self.mod.run({'action': 'plan', 'verb': 'status'})
        self.assertTrue(r['allowed'])
        self.assertEqual(r['mode'], 'dry_run')
        self.assertIn('receipt', r)

    def test_motion_requires_approval(self):
        r = self.mod.run({'action': 'plan', 'verb': 'stand'})
        self.assertFalse(r['allowed'])
        self.assertEqual(r['decision'], 'require_approval')

    def test_approval_enables_motion_plan(self):
        r = self.mod.run({'action': 'plan', 'verb': 'stand',
                          'approval': {'human': True, 'expires_at': '2030-01-01T00:00:00Z'}})
        self.assertTrue(r['allowed'])
        self.assertEqual(r['plan']['object'], 'Robot')

    def test_unknown_verb(self):
        r = self.mod.run({'action': 'plan', 'verb': 'fly'})
        self.assertFalse(r['success'])
        self.assertIn('available', r)


if __name__ == '__main__':
    unittest.main()
