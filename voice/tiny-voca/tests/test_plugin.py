"""Public tests for tiny-voca-voice plugin registration and tool contracts."""
import importlib.util, json, sys, tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FakeCtx:
    def __init__(self):
        self.tools = {}
        self.skills = {}
        self.hooks = {}

    def register_tool(self, name, toolset, handler, schema):
        self.tools[name] = (handler, schema)

    def register_skill(self, name, path):
        self.skills[name] = Path(path)

    def register_hook(self, name, handler):
        self.hooks[name] = handler


def load_plugin(herMES_home=None):
    if herMES_home:
        import os
        os.environ["HERMES_HOME"] = str(herMES_home)
    spec = importlib.util.spec_from_file_location("tiny_voca_plugin", ROOT / "__init__.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TinyVocaPluginTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="tiny-voca-test-")
        self.ctx = FakeCtx()
        self.mod = load_plugin(Path(self.tmp.name))
        self.mod.register(self.ctx)

    def tearDown(self):
        self.tmp.cleanup()

    def test_registers_seven_tools_and_skill(self):
        self.assertEqual(set(self.ctx.tools), {"tts_speak", "tts_voices", "tts_receipts",
                                               "tts_verify", "tts_stick_lesson", "tts_teleprompt", "tts_voice", "tts_lab"})
        self.assertIn("tiny-voca-voice", self.ctx.skills)
        self.assertTrue(self.ctx.skills["tiny-voca-voice"].exists())

    def test_voices_exposes_named_aliases(self):
        out = json.loads(self.ctx.tools["tts_voices"][0]({}))
        self.assertTrue(out["success"])
        ids = [v["id"] for v in out["voices"]]
        self.assertEqual(ids, ["F2", "M2"])
        names = [v["name"] for v in out["voices"]]
        self.assertEqual(names, ["nous-girl", "hermes-agent"])
        self.assertIn("nous-girl", out["voices"][0]["aliases"])
        self.assertIn("hermes-agent", out["voices"][1]["aliases"])

    def test_voices_exposes_identity_and_compute_layers(self):
        out = json.loads(self.ctx.tools["tts_voices"][0]({}))
        layers = out["identity"]["bindings"]
        self.assertEqual(out["version"], "1.3.1")
        self.assertEqual(layers["F2"]["compute_layer"], "human-intent")
        self.assertEqual(layers["M2"]["compute_layer"], "agent-runtime")
        self.assertEqual(layers["ROBOT"]["compute_layer"], "robot-body")
        self.assertEqual(layers["ROBOT"]["source_voice"], "F2")

    def test_receipts_empty_ledger(self):
        out = json.loads(self.ctx.tools["tts_receipts"][0]({"limit": 5}))
        self.assertTrue(out["success"])
        self.assertEqual(out["count"], 0)
        self.assertEqual(out["receipts"], [])

    def test_stick_lesson_list(self):
        out = json.loads(self.ctx.tools["tts_stick_lesson"][0]({"op": "list"}))
        self.assertTrue(out["success"])
        ids = [x["id"] for x in out["lessons"]]
        self.assertEqual(ids, ["asimov-authority", "asimov-verbs", "asimov-twin"])
        self.assertTrue(all(x["lines"] > 0 for x in out["lessons"]))

    def test_teleprompt_list(self):
        out = json.loads(self.ctx.tools["tts_teleprompt"][0]({"op": "list"}))
        self.assertTrue(out["success"])
        self.assertEqual([s["id"] for s in out["scripts"]],
                         ["sovereignty", "asimov-voice-map"])

    def test_voice_lab_card(self):
        out = json.loads(self.ctx.tools["tts_lab"][0]({"op": "card"}))
        self.assertTrue(out["success"])
        self.assertEqual(out["voice"], "SOVÆREIGN")
        self.assertIn("VOICE://BIND", out["governance"])
        self.assertIn("chinese-one-person-company.json", out["ad_script"] or "")

    def test_voice_list(self):
        out = json.loads(self.ctx.tools["tts_voice"][0]({"op": "list"}))
        self.assertTrue(out["success"])
        self.assertEqual([p["id"] for p in out["providers"]], ["tiny-voca", "voxmel"])
        self.assertIn("SOVÆREIGN", out["identity"]["bindings"])

    def test_speak_requires_text_or_file(self):
        out = json.loads(self.ctx.tools["tts_speak"][0]({}))
        self.assertFalse(out["success"])
        self.assertIn("text", out["error"])

    def test_no_machine_local_paths_in_committed_code(self):
        bad_root = "/opt" + "/data"
        files = [ROOT / "__init__.py", ROOT / "plugin.yaml", ROOT / "pyproject.toml"]
        for p in files:
            self.assertNotIn(bad_root, p.read_text(encoding="utf-8"), p.name)


if __name__ == "__main__":
    unittest.main()
