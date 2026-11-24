"""tiny-voca-voice 1.3.1 — self-hosted English TTS plus Asimov stick lessons.

The plugin registers seven light tools and delegates synthesis, verification,
lesson, teleprompter, and provider routing to portable scripts. All paths resolve
from $HERMES_HOME; no machine-local roots. The CLI writes the canonical receipts.
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
CLI = SCRIPTS / "tiny_voca_voice.py"
VERIFY = SCRIPTS / "tiny_voca_verify.py"
STICK = SCRIPTS / "asimov_stick_lesson.py"
TELEPROMPTER = SCRIPTS / "tiny_teleprompter.py"
VOICE = SCRIPTS / "tiny_voice.py"
LAB = SCRIPTS / "tiny_voice_lab.py"
IDENTITY = ROOT / "identity.json"
PY = os.environ.get("HERMES_TINY_VOCA_PYTHON") or shutil.which("python3") or sys.executable
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
LEDGER = Path(os.environ.get("HERMES_TINY_VOCA_LEDGER", HERMES_HOME / "tiny-voca-receipts.jsonl"))
MODEL_SHA256 = "fe6d918791a15b82e37465981d7f27a070e46b46635e5a3482fc8dff87a1ae46"

VOICES = [
    {"id": "F2", "name": "nous-girl", "aliases": ["F2", "f2", "nous-girl", "nous_girl", "nous girl"],
     "language": "en-US", "sample_rate": 24000},
    {"id": "M2", "name": "hermes-agent", "aliases": ["M2", "m2", "hermes-agent", "hermes_agent", "hermes agent"],
     "language": "en-US", "sample_rate": 24000},
]


def _out(obj):
    return json.dumps(obj, ensure_ascii=False)


def _parse_json(stdout):
    raw = (stdout or "").strip()
    if not raw:
        return {"success": False, "error": "empty output from tiny-voca script"}
    for candidate in (raw, raw.splitlines()[-1]):
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    return {"success": False, "error": "tiny-voca script did not emit JSON", "stdout": raw[-500:]}


def _run(script, args):
    if not script.exists():
        return {"success": False, "error": f"script missing: {script}"}
    try:
        p = subprocess.run([PY, str(script)] + list(args), capture_output=True,
                           text=True, timeout=300)
        result = _parse_json(p.stdout)
        if p.returncode != 0 and result.get("success", False):
            result["success"] = False
        if p.returncode != 0 and not result.get("error"):
            result["error"] = (p.stderr or "tiny-voca script failed")[-500:]
        return result
    except Exception as exc:
        return {"success": False, "error": f"{type(exc).__name__}: {exc}"}


def _identity():
    if not IDENTITY.exists():
        return {"success": False, "error": "identity.json missing"}
    try:
        return json.loads(IDENTITY.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"success": False, "error": f"identity.json invalid: {exc}"}


def register(ctx):
    def tts_speak(args: dict) -> str:
        text = args.get("text", "")
        if not text and args.get("text_file"):
            text = str(Path(args["text_file"]).read_text(encoding="utf-8"))
        if not text:
            return _out({"success": False, "error": "text or text_file is required"})
        output = args.get("output") or str(HERMES_HOME / "tiny-voca-out.wav")
        cmd = ["--text", text, "--voice", str(args.get("voice", "M2")),
               "--output", str(output), "--speed", str(args.get("speed", 1.0)),
               "--pitch-shift", str(args.get("pitch_shift", 0.0)),
               "--pitch-range", str(args.get("pitch_range", 1.0))]
        return _out(_run(CLI, cmd))

    def tts_voices(args: dict) -> str:
        runtime = HERMES_HOME / "tiny-voca"
        model = runtime / "onnx" / "model.onnx"
        identity = _identity()
        return _out({"success": True, "authority": "HUMAN://ROOT", "version": "1.3.1",
                     "voices": VOICES, "identity": identity,
                     "compute_layers": identity.get("compute_layers", {}),
                     "model": "tiny-voca",
                     "parameters": 4537291, "sample_rate": 24000,
                     "backend": "ONNX Runtime CPU",
                     "runtime": str(runtime), "model_present": model.exists(),
                     "model_sha256_expected": MODEL_SHA256})

    def tts_receipts(args: dict) -> str:
        limit = int(args.get("limit") or 10)
        lines = LEDGER.read_text(encoding="utf-8").splitlines() if LEDGER.exists() else []
        receipts = []
        for line in lines[-limit:]:
            try:
                receipts.append(json.loads(line))
            except Exception:
                continue
        return _out({"success": True, "authority": "HUMAN://ROOT",
                     "count": len(lines), "receipts": receipts})

    def tts_verify(args: dict) -> str:
        return _out(_run(VERIFY, []))

    def tts_stick_lesson(args: dict) -> str:
        op = args.get("op", "list")
        cmd = ["--op", str(op)]
        if args.get("lesson"):
            cmd += ["--lesson", str(args["lesson"])]
        if args.get("out"):
            cmd += ["--out", str(args["out"])]
        if args.get("speed") is not None:
            cmd += ["--speed", str(args["speed"])]
        return _out(_run(STICK, cmd))

    def tts_teleprompt(args: dict) -> str:
        cmd = ["--op", str(args.get("op", "list"))]
        if args.get("script"):
            cmd += ["--script", str(args["script"])]
        if args.get("out"):
            cmd += ["--out", str(args["out"])]
        if args.get("speed") is not None:
            cmd += ["--speed", str(args["speed"])]
        return _out(_run(TELEPROMPTER, cmd))

    def tts_lab(args: dict) -> str:
        cmd = ["--op", str(args.get("op", "card"))]
        for key, flag in (("reference", "--reference"), ("transcript", "--transcript"),
                          ("consent", "--consent"), ("out", "--out")):
            if args.get(key) is not None:
                cmd += [flag, str(args[key])]
        if args.get("build_audio"):
            cmd.append("--build-audio")
        return _out(_run(LAB, cmd))

    def tts_voice(args: dict) -> str:
        cmd = ["--op", str(args.get("op", "list"))]
        for key, flag in (("provider", "--provider"), ("voice", "--voice"),
                          ("text", "--text"), ("output", "--output"),
                          ("language", "--language"), ("speed", "--speed"),
                          ("prompt_audio", "--prompt-audio"),
                          ("prompt_text", "--prompt-text"), ("consent", "--consent")):
            if args.get(key) is not None:
                cmd += [flag, str(args[key])]
        return _out(_run(VOICE, cmd))

    ctx.register_tool(
        name="tts_speak", toolset="tiny-voca-voice", handler=tts_speak,
        schema={"type": "object", "properties": {
            "text": {"type": "string", "description": "English text to synthesize."},
            "text_file": {"type": "string", "description": "UTF-8 file containing text."},
            "voice": {"type": "string", "description": "F2/nous-girl or M2/hermes-agent; aliases accepted."},
            "output": {"type": "string", "description": "Output .wav path."},
            "speed": {"type": "number"}, "pitch_shift": {"type": "number"},
            "pitch_range": {"type": "number"},
        }, "required": []},
    )
    ctx.register_tool(
        name="tts_voices", toolset="tiny-voca-voice", handler=tts_voices,
        schema={"type": "object", "properties": {}},
    )
    ctx.register_tool(
        name="tts_receipts", toolset="tiny-voca-voice", handler=tts_receipts,
        schema={"type": "object", "properties": {
            "limit": {"type": "integer", "description": "Recent receipts to return. Default 10."}}},
    )
    ctx.register_tool(
        name="tts_verify", toolset="tiny-voca-voice", handler=tts_verify,
        schema={"type": "object", "properties": {}},
    )
    ctx.register_tool(
        name="tts_stick_lesson", toolset="tiny-voca-voice", handler=tts_stick_lesson,
        schema={"type": "object", "properties": {
            "op": {"type": "string", "enum": ["list", "build"],
                   "description": "List lessons or build a narrated lesson bundle."},
            "lesson": {"type": "string",
                       "description": "asimov-authority, asimov-verbs, asimov-twin, or all."},
            "out": {"type": "string", "description": "Output directory for build."},
            "speed": {"type": "number", "description": "Narration speed. Default 1.25."},
        }, "required": ["op"]},
    )
    ctx.register_tool(
        name="tts_teleprompt", toolset="tiny-voca-voice", handler=tts_teleprompt,
        schema={"type": "object", "properties": {
            "op": {"type": "string", "enum": ["list", "build"],
                   "description": "List teleprompter scripts or build a 9:16 narrated page."},
            "script": {"type": "string",
                       "description": "sovereignty, asimov-voice-map, or a path to script JSON."},
            "out": {"type": "string", "description": "Output directory for build."},
            "speed": {"type": "number", "description": "Narration speed. Default 1.25."},
        }, "required": ["op"]},
    )
    ctx.register_tool(
        name="tts_voice", toolset="tiny-voca-voice", handler=tts_voice,
        schema={"type": "object", "properties": {
            "op": {"type": "string", "enum": ["list", "bind", "speak", "go"],
                   "description": "List providers, bind a digital twin, synthesize, or run the GO://TINY starter."},
            "provider": {"type": "string", "enum": ["tiny-voca", "voxmel"]},
            "voice": {"type": "string", "description": "F2, M2, ROBOT, or SOVÆREIGN."},
            "text": {"type": "string"}, "output": {"type": "string"},
            "language": {"type": "string", "description": "en or zh."},
            "speed": {"type": "number"},
            "prompt_audio": {"type": "string", "description": "Reference WAV for VOICE://BIND."},
            "prompt_text": {"type": "string", "description": "Exact transcript for VOICE://BIND."},
            "consent": {"type": "string", "description": "Explicit consent file for VOICE://BIND."},
        }, "required": ["op"]},
    )

    ctx.register_tool(
        name="tts_lab", toolset="tiny-voca-voice", handler=tts_lab,
        schema={"type": "object", "properties": {
            "op": {"type": "string", "enum": ["card", "bind", "provision", "ad"],
                   "description": "Inspect, bind, provision, or build the Chinese ad."},
            "reference": {"type": "string", "description": "Clean voice reference WAV."},
            "transcript": {"type": "string", "description": "Exact transcript of the reference WAV."},
            "consent": {"type": "string", "description": "Explicit HUMAN://ROOT consent file."},
            "out": {"type": "string", "description": "Ad output directory."},
            "build_audio": {"type": "boolean", "description": "Synthesize narration with VoxMel."},
        }, "required": ["op"]},
    )
    skill = ROOT / "skills" / "tiny-voca-voice" / "SKILL.md"
    if skill.exists():
        ctx.register_skill("tiny-voca-voice", skill)
