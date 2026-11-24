"""Stdlib-only packaging checks; no network, weights, or heavy imports."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class PackagingTest(unittest.TestCase):
    def test_cli_contract_strings(self):
        src = (ROOT / "scripts" / "tiny_voca_voice.py").read_text(encoding="utf-8")
        for token in ("--text-file", "--output", "print(json.dumps(", "sha256"):
            self.assertIn(token, src, f"CLI source missing {token!r}")

    def test_skill_frontmatter(self):
        content = (ROOT / "skills" / "tiny-voca-voice" / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "SKILL.md must start with ---")
        parts = content.split("---\n", 2)
        self.assertGreaterEqual(len(parts), 3, "frontmatter must close with ---")
        fm = parts[1]
        for key in ("name:", "description:", "version:", "author:",
                    "license:", "platforms:", "metadata:"):
            self.assertIn(key, fm, f"frontmatter missing {key}")
        m = re.search(r"^description:\s*(.+)$", fm, re.M)
        self.assertIsNotNone(m)
        desc = m.group(1).strip().strip('"')
        self.assertLessEqual(len(desc), 60, "description exceeds 60 chars")
        self.assertTrue(desc.endswith("."), "description must end with a period")
        for section in ("When to Use", "Prerequisites", "How to Run",
                        "Quick Reference", "Procedure", "Pitfalls", "Verification"):
            self.assertIn(f"## {section}", content, f"missing section {section}")

    def test_identity_map_is_shipped(self):
        identity = json.loads((ROOT / "identity.json").read_text(encoding="utf-8"))
        self.assertEqual(identity["authority"], "HUMAN://ROOT")
        self.assertEqual(set(identity["compute_layers"]),
                         {"human-intent", "agent-runtime", "robot-body", "human-twin"})
        install = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("identity.json", install)

    def test_teleprompter_capability_is_shipped(self):
        src = (ROOT / "scripts" / "tiny_teleprompter.py").read_text(encoding="utf-8")
        for token in ("ACTION_PROMPT_BUILD", "READ LINE", "HUMAN://ROOT → æ → RECEIPT",
                      "prefers-reduced-motion", "tinyVOCA powered"):
            self.assertIn(token, src, f"teleprompter source missing {token!r}")
        self.assertIn("tts_teleprompt", (ROOT / "plugin.yaml").read_text(encoding="utf-8"))
        self.assertIn("docs/TINY_TELEPROMPTER.md", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_default_timbre_is_bound(self):
        ident = json.loads((ROOT / "identity.json").read_text(encoding="utf-8"))
        b = ident["bindings"]["SOVÆREIGN"]
        self.assertEqual(b["default_timbre"], "broadcast")
        self.assertEqual([v["id"] for v in b["timbre_variants"]], ["low", "bright", "broadcast"])
        self.assertTrue(b["bind_receipt"])

    def test_voice_lab_is_shipped(self):
        for rel in ("scripts/tiny_voice_lab.py", "docs/VOICE_LAB.md",
                    "examples/tiny-voice/chinese-one-person-company.json"):
            self.assertTrue((ROOT / rel).exists(), f"missing {rel}")
        src = (ROOT / "scripts" / "tiny_voice_lab.py").read_text(encoding="utf-8")
        for token in ("VOICE://BIND", "SOVÆREIGN", "VOXMEL_REPO", "ad"):
            self.assertIn(token, src)
        self.assertIn("tts_lab", (ROOT / "plugin.yaml").read_text(encoding="utf-8"))

    def test_go_tiny_starter_is_shipped(self):
        for rel in ("examples/tiny-voice/consent.template.txt",
                    "examples/tiny-voice/prompt_text.template.txt",
                    "examples/tiny-voice/sovereignty.zh.json"):
            self.assertTrue((ROOT / rel).exists(), f"missing starter asset {rel}")
        src = (ROOT / "scripts" / "tiny_voice.py").read_text(encoding="utf-8")
        self.assertIn("GO://TINY", src)
        self.assertIn("VOXMEL_CONSENT", src)

    def test_tiny_voice_router_is_shipped(self):
        src = (ROOT / "scripts" / "tiny_voice.py").read_text(encoding="utf-8")
        for token in ("ACTION_VOICE_BIND", "ACTION_VOICE_SPEAK", "VOXMEL_REPO",
                      "SOVÆREIGN", "human-twin"):
            self.assertIn(token, src, f"tinyVOICE source missing {token!r}")
        self.assertIn("tts_voice", (ROOT / "plugin.yaml").read_text(encoding="utf-8"))

    def test_first_class_repo_beauty_and_attribution(self):
        for rel in ("site/index.html", "assets/brand/hermes-agent-tinyvoca-logo.svg",
                    "assets/brand/hermes-agent-tinyvoca-logo-1080.png",
                    "docs/ATTRIBUTION.md", "CITATION.cff"):
            self.assertTrue((ROOT / rel).exists(), f"missing repo asset {rel}")
        notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("Thank you to the original", notice)
        self.assertIn("#opensourceware #internetofagents", notice)
        site = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        self.assertIn("HUMAN://ROOT → æ → RECEIPT", site)
        self.assertIn("#opensourceware #internetofagents", site)
        install = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("site package.json CITATION.cff", install)

    def test_desktop_dock_is_shipped(self):
        for rel in ("desktop/plugin.js", "dashboard/manifest.json",
                    "dashboard/plugin_api.py", "package.json"):
            self.assertTrue((ROOT / rel).exists(), f"missing desktop asset {rel}")
        install = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("desktop dashboard site package.json CITATION.cff", install)
        self.assertIn("requires_hermes", (ROOT / "plugin.yaml").read_text(encoding="utf-8"))

    def test_stick_lesson_assets_and_skill(self):
        assets = ROOT / "assets" / "stick-scene"
        for rel in ("stick.js", "LICENSE", "scenes/asimov-authority.js",
                    "scenes/asimov-verbs.js", "scenes/asimov-twin.js"):
            self.assertTrue((assets / rel).exists(), f"missing asset {rel}")
        skill = (ROOT / "skills" / "tiny-voca-voice" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("tts_stick_lesson", skill)
        self.assertIn("Asimov stick lessons", skill)

    def test_install_prints_provider_command(self):
        install = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("hermes config set tts.provider tiny-voca", install)
        self.assertIn("plugins/tiny-voca-voice", install)

    def test_ci_is_compile_and_unittest_only(self):
        ci = (ROOT / ".github" / "workflows" / "test.yml").read_text(encoding="utf-8")
        self.assertIn("py_compile", ci)
        self.assertIn("unittest", ci)
        self.assertNotIn("acceptance.py", ci)


if __name__ == "__main__":
    unittest.main()
