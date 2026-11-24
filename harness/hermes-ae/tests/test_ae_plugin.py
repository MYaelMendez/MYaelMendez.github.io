"""Offline unit tests for the hermes-ae plugin.

Loads the repo-root ``__init__.py`` with importlib against a temporary
``HERMES_HOME``/ledger, then drives the registered ``ae`` tool. Only stdlib is
used: no network calls and no heavy bundled scripts are ever executed.
"""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INIT_FILE = REPO_ROOT / "__init__.py"

_ENV_KEYS = (
    "HERMES_HOME",
    "HERMES_AE_LEDGER",
    "HERMES_AE_PLUGINS",
    "HERMES_AE_PYTHON",
)


class FakeCtx:
    """Minimal registration context that records registered tools."""

    def __init__(self):
        self.tools = {}
        self.commands = {}
        self.hooks = {}

    def register_tool(self, name, toolset, handler, schema):
        self.tools[name] = (toolset, handler, schema)

    def register_command(self, name, handler, description, args_hint):
        self.commands[name] = (handler, description, args_hint)

    def register_hook(self, name, handler):
        self.hooks[name] = handler


class AePluginTests(unittest.TestCase):
    def setUp(self):
        self._saved_env = {key: os.environ.get(key) for key in _ENV_KEYS}
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)

        home = Path(self._tmp.name)
        os.environ["HERMES_HOME"] = str(home)
        os.environ["HERMES_AE_LEDGER"] = str(home / "ae-receipts.jsonl")
        os.environ["HERMES_AE_PLUGINS"] = str(home / "plugins")
        # Guard against any accidental subprocess using a stale interpreter.
        os.environ["HERMES_AE_PYTHON"] = sys.executable
        self.ledger = Path(os.environ["HERMES_AE_LEDGER"])

        self.module = self._load_module()
        self.ctx = FakeCtx()
        self.module.register(self.ctx)
        self.handler = self.ctx.tools["ae"][1]

    def tearDown(self):
        for key, value in self._saved_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def _load_module(self):
        name = "hermes_ae_test_%d" % id(self)
        spec = importlib.util.spec_from_file_location(name, INIT_FILE)
        assert spec is not None and spec.loader is not None
        loader = spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        self.addCleanup(sys.modules.pop, name, None)
        loader.exec_module(module)
        return module

    def _call(self, **args):
        return json.loads(self.handler(args))

    def test_registers_exactly_one_tool_named_ae(self):
        self.assertEqual(list(self.ctx.tools), ["ae"])
        toolset, handler, schema = self.ctx.tools["ae"]
        self.assertEqual(toolset, "hermes-ae")
        self.assertTrue(callable(handler))
        self.assertIsInstance(schema, dict)
        self.assertIn("op", schema.get("properties", {}))

    def test_status_works_with_temp_ledger(self):
        out = self._call(op="status")
        self.assertTrue(out["success"])
        self.assertEqual(out["op"], "status")
        result = out["result"]
        self.assertEqual(result["actor"], "hermes-ae")
        self.assertEqual(result["authority"], "HUMAN://ROOT")
        self.assertEqual(result["version"], "3.18.0")
        self.assertTrue(result["receipts"]["success"])
        self.assertTrue(self.ledger.exists())
        self.assertIn("hash", out["receipt"])

    def test_ops_works_with_temp_ledger(self):
        out = self._call(op="ops")
        self.assertTrue(out["success"])
        self.assertEqual(out["op"], "ops")
        self.assertIn("shortcuts", out["result"])
        self.assertIn("local_ops", out["result"])
        self.assertIn("studio_video", out["result"]["local_ops"])
        self.assertIn("tv_episode", out["result"]["local_ops"])
        self.assertTrue(self.ledger.exists())

    def test_tts_aliases_advertised(self):
        out = self._call(op="ops")
        for name in ("speak", "tts_speak", "voices", "tts_voices", "tts_receipts"):
            self.assertIn(name, out["result"]["local_funcs"])

    def test_voices_lists_f2_m2(self):
        out = self._call(op="voices")
        self.assertTrue(out["success"])
        self.assertEqual([v["id"] for v in out["result"]["voices"]], ["F2", "M2"])

    def test_harness_registry(self):
        out = self._call(op="harnesses")
        self.assertTrue(out["success"])
        self.assertEqual(out["result"]["count"], 9)
        self.assertIn("physics", out["result"]["harnesses"][3]["name"] if isinstance(out["result"]["harnesses"][3], dict) else "physics")

    def test_agent_body_binding(self):
        out = self._call(op="agent_body")
        self.assertTrue(out["success"])
        self.assertEqual(out["result"]["bindings"]["M2"]["body"], "asimov-1")
        self.assertEqual(out["result"]["bindings"]["M2"]["name"], "hermes-agent")

    def test_ffmpeg_harness(self):
        out = self._call(op="harness", name="ffmpeg")
        self.assertTrue(out["success"])
        self.assertEqual(out["result"]["harness"]["name"], "ffmpeg")
        self.assertIn("media", out["result"]["harness"]["aliases"])
        self.assertTrue(out["result"]["harness"]["probe"]["success"])

    def test_script_ops_route_to_scripts(self):
        out = self._call(op="ops")
        self.assertIn("policy_locomotion", out["result"]["local_ops"])
        self.assertNotIn("policy_locomotion", out["result"]["local_funcs"])
        self.assertNotIn("ffmpeg_demo", out["result"]["local_funcs"])

    def test_packaged_locomotion_manifest(self):
        import json as _json
        from pathlib import Path as _Path
        manifest = _json.loads((_Path(__file__).resolve().parents[1] / 'packages' / 'ae-locomotion' / '1.0.0' / 'manifest.json').read_text())
        self.assertEqual(manifest['name'], 'æLOCOMOTION')
        self.assertEqual(manifest['authority'], 'HUMAN://ROOT')
        self.assertTrue(manifest['verified']['success'])

    def test_agent_unified_runtime(self):
        out = self._call(op="agent")
        self.assertTrue(out["success"])
        self.assertEqual(out["result"]["agent"]["name"], "Asimov Agent")
        self.assertTrue(out["result"]["capabilities"]["viewport_dom"])
        self.assertTrue(out["result"]["capabilities"]["onnx_locomotion"])

    def test_mobility_homepage_binding(self):
        out = self._call(op="agent")
        self.assertTrue(out["result"]["agent"]["homepage"].startswith("https://mobility.foundation/"))

    def test_projection_package(self):
        out = self._call(op="projection")
        self.assertTrue(out["success"])
        self.assertEqual(out["result"]["manifest"]["authority"], "HUMAN://ROOT")
        self.assertIn("ffmpeg", out["result"]["manifest"]["composition"])

    def test_agent_viewport_binding(self):
        out = self._call(op="agent")
        self.assertTrue(out["result"]["agent"]["viewport"].endswith("/asimov-viewport/"))

    def test_verify_on_empty_ledger(self):
        out = self._call(op="verify")
        self.assertTrue(out["success"])
        self.assertTrue(out["result"]["success"])
        self.assertEqual(out["result"]["count"], 0)
        self.assertEqual(out["result"]["head"], "GENESIS")

    def test_unknown_op_fails_gracefully(self):
        out = self._call(op="definitely_not_an_op")
        self.assertFalse(out["success"])
        self.assertEqual(out["op"], "definitely_not_an_op")
        self.assertFalse(out["result"]["success"])
        self.assertIn("unknown op", out["result"]["error"])
        self.assertIn("available", out["result"])
        self.assertIn("hash", out["receipt"])

    def test_receipt_chain_verifies_after_operations(self):
        for op in ("status", "ops"):
            out = self._call(op=op)
            self.assertTrue(out["success"], "%s: %s" % (op, out))
            self.assertIn("hash", out["receipt"])

        out = self._call(op="verify")
        self.assertTrue(out["success"])
        self.assertTrue(out["result"]["success"])
        self.assertEqual(out["result"]["count"], 2)

        lines = [x for x in self.ledger.read_text(encoding="utf-8").splitlines() if x.strip()]
        self.assertEqual(len(lines), 3)
        self.assertEqual(json.loads(lines[-1])["prev"], json.loads(lines[-2])["hash"])

    def test_verify_detects_tampering(self):
        self._call(op="status")
        self._call(op="ops")
        lines = self.ledger.read_text(encoding="utf-8").splitlines()
        entry = json.loads(lines[0])
        entry["detail"] = {"ok": False}
        lines[0] = json.dumps(entry)
        self.ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")

        out = self._call(op="verify")
        self.assertFalse(out["result"]["success"])
        self.assertEqual(out["result"]["broken_at"], 0)


if __name__ == "__main__":
    unittest.main()
