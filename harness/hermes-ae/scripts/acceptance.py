"""Fresh-clone acceptance for hermes-ae.

No heavy dependencies: verifies registration, core ops, receipt chain, and the
stdlib unittest suite. Safe to run in CI on a clean checkout.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class FakeCtx:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name, toolset, handler, schema):
        self.tools[name] = (handler, toolset)

    def register_command(self, *args, **kwargs):
        pass

    def register_skill(self, *args, **kwargs):
        pass

    def register_hook(self, *args, **kwargs):
        pass


def main():
    with tempfile.TemporaryDirectory(prefix="hermes-ae-acceptance-") as tmp:
        env = dict(os.environ, HERMES_HOME=tmp,
                   HERMES_AE_LEDGER=str(Path(tmp) / "ae-receipts.jsonl"))
        os.environ.update({k: v for k, v in env.items() if k.startswith("HERMES_AE")})
        os.environ["HERMES_HOME"] = tmp
        spec = importlib.util.spec_from_file_location("ae_acceptance", str(ROOT / "__init__.py"))
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ctx = FakeCtx()
        mod.register(ctx)
        assert sorted(ctx.tools) == ["ae"], ctx.tools
        ae = ctx.tools["ae"][0]
        status = json.loads(ae({"op": "status"}))
        assert status["success"] and status["result"]["version"] == "3.18.0"
        ops = json.loads(ae({"op": "ops"}))
        expected = {"speak", "tts_speak", "voices", "tts_voices", "tts_receipts", "probe", "witness", "gallery", "physics",
                    "studio_sync", "head", "head_dom", "face", "twin", "policy", "daobrain", "verbs", "studio_video", "free_walk", "masterpiece", "harnesses", "agent_body", "ffmpeg_demo", "policy_locomotion", "viewport_dom", "agent", "projection_render", "tv_episode"}
        assert expected.issubset(set(ops["result"]["local_funcs"]) | set(ops["result"]["local_ops"]))
        assert json.loads(ae({"op": "verify"}))["success"]
        tests = subprocess.run([sys.executable, "-m", "unittest", "discover",
                                "-s", str(ROOT / "tests"), "-v"],
                               capture_output=True, text=True)
        if tests.returncode != 0:
            print(tests.stdout + tests.stderr)
            raise SystemExit(tests.returncode)
        print(json.dumps({"success": True, "version": status["result"]["version"],
                          "tools": sorted(ctx.tools), "core_ops": sorted(expected),
                          "unittest": "OK"}, indent=2))


if __name__ == "__main__":
    main()
