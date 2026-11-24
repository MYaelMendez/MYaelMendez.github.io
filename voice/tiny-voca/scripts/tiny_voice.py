"""tinyVOICE router — tiny-voca today, VoxMel zero-shot cloning when provisioned.

Fail-closed. Never clones a voice without an explicit VOICE://BIND receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import tiny_voca_paths as paths  # noqa: E402

IDENTITY = ROOT / "identity.json"
VOCA_CLI = ROOT / "scripts" / "tiny_voca_voice.py"
PY = os.environ.get("HERMES_TINY_VOCA_PYTHON") or shutil.which("python3") or sys.executable


def _out(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _fail(message, **extra):
    obj = {"success": False, "error": message, "authority": "HUMAN://ROOT"}
    obj.update(extra)
    _out(obj)
    return 1


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _identity() -> dict:
    return json.loads(IDENTITY.read_text(encoding="utf-8"))

def _voice_card() -> dict:
    p = paths.hermes_home() / "tiny-voice-lab" / "voice-card.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def _voice_id(value: str, identity: dict) -> str:
    raw = str(value or "").strip().lower().replace("_", " ").replace("-", " ")
    for voice_id, binding in identity.get("bindings", {}).items():
        aliases = [str(a).strip().lower().replace("_", " ").replace("-", " ")
                   for a in binding.get("aliases", [])]
        if raw in aliases:
            return voice_id
    raise KeyError(f"unknown voice {value!r}")


def _duration(p: Path) -> float:
    with wave.open(str(p), "rb") as w:
        return w.getnframes() / w.getframerate()


def _parse_json(stdout: str) -> dict:
    raw = (stdout or "").strip()
    if not raw:
        return {"success": False, "error": "empty output"}
    for candidate in (raw, raw.splitlines()[-1]):
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    return {"success": False, "error": "no JSON object in output", "stdout": raw[-400:]}


def _providers(identity: dict):
    return [
        {
            "id": "tiny-voca",
            "name": "tinyVOCA",
            "runtime": "tiny-voca ONNX / CPU",
            "languages": ["en"],
            "voices": ["F2", "M2"],
            "cloning": False,
            "status": "shipped" if VOCA_CLI.exists() else "missing",
        },
        {
            "id": "voxmel",
            "name": "VoxMel",
            "runtime": "wavelet-factorized autoregressive mel + Vocos",
            "languages": ["en", "zh"],
            "voices": ["SOVÆREIGN"],
            "cloning": True,
            "status": "requires local model, Vocos weights, reference audio, and consent",
        },
    ]


def op_list():
    identity = _identity()
    _out({"success": True, "authority": "HUMAN://ROOT",
          "product": "tinyVOICE",
          "providers": _providers(identity),
          "identity": identity})


def op_bind(args):
    identity = _identity()
    voice_id = _voice_id(args.voice or "SOVÆREIGN", identity)
    binding = identity["bindings"][voice_id]
    if binding.get("compute_layer") != "human-twin":
        raise ValueError("VOICE://BIND is only for the human-twin voice")
    prompt_audio = Path(args.prompt_audio).expanduser() if args.prompt_audio else None
    prompt_text = Path(args.prompt_text).expanduser() if args.prompt_text else None
    consent = Path(args.consent).expanduser() if args.consent else None
    if not prompt_audio or not prompt_audio.exists():
        raise FileNotFoundError("prompt audio is required for VOICE://BIND")
    if not prompt_text or not prompt_text.exists():
        raise FileNotFoundError("exact prompt transcript is required for VOICE://BIND")
    if not consent or not consent.exists():
        raise FileNotFoundError("explicit consent file is required for VOICE://BIND")
    consent_text = consent.read_text(encoding="utf-8")
    if "HUMAN://ROOT" not in consent_text or "consent" not in consent_text.lower():
        raise ValueError("consent file must contain HUMAN://ROOT and explicit consent")
    receipt = paths.append_custom_receipt({
        "action": paths.ACTION_VOICE_BIND,
        "voice": voice_id,
        "provider": "voxmel",
        "authority": "HUMAN://ROOT",
        "prompt_audio_sha256": _sha(prompt_audio),
        "prompt_text_sha256": _sha(prompt_text),
        "consent_sha256": _sha(consent),
        "sample_rate_hz": 24000,
    })
    _out({"success": True, "action": paths.ACTION_VOICE_BIND,
          "voice": voice_id, "provider": "voxmel",
          "receipt": receipt.get("hash"), "authority": "HUMAN://ROOT"})


def _voxmel_cmd(args, output: Path):
    repo = os.environ.get("VOXMEL_REPO")
    if not repo or not Path(repo).exists():
        raise RuntimeError("VOXMEL_REPO must point to a local Vox checkout")
    model = os.environ.get("VOXMEL_MODEL_DIR")
    vocos = os.environ.get("VOXMEL_VOCOS_DIR")
    tokenizer = os.environ.get("VOXMEL_TOKENIZER_PATH")
    if not model or not Path(model).exists():
        raise RuntimeError("VOXMEL_MODEL_DIR missing or not found")
    if not vocos or not Path(vocos).exists():
        raise RuntimeError("VOXMEL_VOCOS_DIR missing or not found")
    if not tokenizer or not Path(tokenizer).exists():
        raise RuntimeError("VOXMEL_TOKENIZER_PATH missing or not found")
    card = _voice_card()
    prompt_audio = os.environ.get("VOXMEL_PROMPT_AUDIO") or card.get("default_prompt_audio")
    prompt_text = os.environ.get("VOXMEL_PROMPT_TEXT") or card.get("transcript")
    if not prompt_audio or not prompt_text:
        raise RuntimeError("VOXMEL_PROMPT_AUDIO and VOXMEL_PROMPT_TEXT required for cloning")
    if not Path(prompt_audio).exists():
        raise RuntimeError(f"prompt audio not found: {prompt_audio}")
    if not Path(prompt_text).exists():
        raise RuntimeError(f"prompt transcript not found: {prompt_text}")
    py = os.environ.get("VOXMEL_PYTHON") or PY
    cmd = [py, "-m", "voxcore.cli", "--model", model,
           "--tokenizer-path", tokenizer, "--vocos-path", vocos,
           "--device", os.environ.get("VOXMEL_DEVICE", "auto"),
           "--prompt-audio", prompt_audio, "--prompt-text", prompt_text,
           "--text", args.text, "--output", str(output)]
    if os.environ.get("VOXMEL_FP16"):
        cmd.append("--fp16")
    if os.environ.get("VOXMEL_BF16"):
        cmd.append("--bf16")
    for env_name, flag in (("VOXMEL_CHECKPOINT", "--checkpoint"),
                           ("VOXMEL_SEED", "--seed"),
                           ("VOXMEL_CFG_TEXT", "--cfg-text-strength"),
                           ("VOXMEL_CFG_SPK", "--cfg-spk-strength"),
                           ("VOXMEL_UP_STEPS", "--up-steps")):
        value = os.environ.get(env_name)
        if value:
            cmd += [flag, value]
    return cmd, Path(repo)


def op_speak(args):
    identity = _identity()
    provider = args.provider or "tiny-voca"
    text = str(args.text or "").strip()
    if not text:
        raise ValueError("text is required")
    output = Path(args.output).expanduser() if args.output else None
    if not output:
        raise ValueError("output is required")

    if provider == "tiny-voca":
        proc = subprocess.run(
            [PY, str(VOCA_CLI), "--text", text, "--voice", args.voice or "M2",
             "--output", str(output), "--speed", str(args.speed or 1.0)],
            capture_output=True, text=True, timeout=300)
        result = _parse_json(proc.stdout)
        if proc.returncode != 0 and result.get("success"):
            result["success"] = False
        if proc.returncode != 0 and not result.get("error"):
            result["error"] = (proc.stderr or "tiny-voca failed")[-500:]
        result["provider"] = "tiny-voca"
        _out(result)
        return 0 if result.get("success") else 1

    if provider != "voxmel":
        raise ValueError("provider must be tiny-voca or voxmel")
    voice_id = _voice_id(args.voice or "SOVÆREIGN", identity)
    if identity["bindings"][voice_id].get("compute_layer") != "human-twin":
        raise ValueError("VoxMel provider is bound to the human-twin voice")
    cmd, cwd = _voxmel_cmd(args, output)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=str(cwd))
    if proc.returncode != 0 or not output.exists():
        raise RuntimeError((proc.stderr or proc.stdout or "voxmel failed")[-1000:])
    receipt = paths.append_custom_receipt({
        "action": paths.ACTION_VOICE_SPEAK,
        "authority": "HUMAN://ROOT",
        "provider": "voxmel",
        "voice": voice_id,
        "language": args.language or "en",
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "sha256": _sha(output),
        "duration_s": round(_duration(output), 3),
        "output": str(output),
    })
    _out({"success": True, "provider": "voxmel", "voice": voice_id,
          "output": str(output), "sha256": _sha(output),
          "duration_s": round(_duration(output), 3),
          "receipt": receipt.get("hash"), "authority": "HUMAN://ROOT"})
    return 0


def _join_wavs(parts, output: Path, gap_s=0.18):
    params = None
    frames = []
    gap_frames = int(gap_s * paths.SAMPLE_RATE)
    for i, p in enumerate(parts):
        with wave.open(str(p), "rb") as w:
            if params is None:
                params = w.getparams()
            frames.append(w.readframes(w.getnframes()))
            if i < len(parts) - 1:
                frames.append(b"\x00\x00" * gap_frames)
    output.parent.mkdir(parents=True, exist_ok=True)
    if params is None:
        raise RuntimeError("no WAV parts to join")
    with wave.open(str(output), "wb") as w:
        w.setnchannels(params.nchannels)
        w.setsampwidth(params.sampwidth)
        w.setframerate(params.framerate)
        w.writeframes(b"".join(frames))


def op_go(args):
    out = Path(args.output).expanduser() if args.output else paths.hermes_home() / "tiny-voice-go"
    out.mkdir(parents=True, exist_ok=True)
    script = [
        ("F2", "Human root to A E to receipt."),
        ("M2", "Go tiny. Local voice, public receipts."),
    ]
    made = []
    for n, (voice, text) in enumerate(script):
        wav = out / f"go-{n:02d}-{voice}.wav"
        proc = subprocess.run(
            [PY, str(VOCA_CLI), "--text", text, "--voice", voice,
             "--output", str(wav), "--speed", str(args.speed or 1.25)],
            capture_output=True, text=True, timeout=300)
        result = _parse_json(proc.stdout)
        if proc.returncode != 0 or not result.get("success"):
            raise RuntimeError(result.get("error") or (proc.stderr or "tiny-voca failed")[-500:])
        rec = result.get("receipt")
        if isinstance(rec, dict):
            rec = rec.get("hash")
        made.append({"voice": voice, "text": text, "audio": str(wav),
                     "duration_s": result.get("duration_s"),
                     "sha256": result.get("sha256"), "receipt": rec})
    joined = out / "go.wav"
    _join_wavs([Path(item["audio"]) for item in made], joined)
    env_keys = ("VOXMEL_REPO", "VOXMEL_MODEL_DIR", "VOXMEL_VOCOS_DIR",
                "VOXMEL_TOKENIZER_PATH", "VOXMEL_PROMPT_AUDIO",
                "VOXMEL_PROMPT_TEXT", "VOXMEL_CONSENT")
    voxmel_ready = {k: bool(os.environ.get(k)) for k in env_keys}
    bundle = {
        "authority": "HUMAN://ROOT",
        "product": "tinyVOICE",
        "action": "GO://TINY",
        "output": str(out),
        "joined_wav": str(joined),
        "joined_sha256": _sha(joined),
        "lines": made,
        "voxmel_ready": voxmel_ready,
        "voxmel_can_bind": all(voxmel_ready.values()),
        "authority_chain": "HUMAN://ROOT → æ → RECEIPT",
    }
    (out / "go.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _out({"success": True, "action": "GO://TINY", "authority": "HUMAN://ROOT",
          "output": str(out), "wav": str(joined), "sha256": _sha(joined),
          "lines": len(made), "voxmel_ready": all(voxmel_ready.values())})


def main():
    p = argparse.ArgumentParser(description="tinyVOICE local voice router.")
    p.add_argument("--op", choices=("list", "bind", "speak", "go"), required=True)
    p.add_argument("--provider", choices=("tiny-voca", "voxmel"), default="tiny-voca")
    p.add_argument("--voice", default=None)
    p.add_argument("--text", default=None)
    p.add_argument("--output", default=None)
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--language", default="en")
    p.add_argument("--prompt-audio", default=None)
    p.add_argument("--prompt-text", default=None)
    p.add_argument("--consent", default=None)
    args = p.parse_args()
    try:
        if args.op == "list":
            op_list()
            return 0
        if args.op == "bind":
            return op_bind(args)
        if args.op == "go":
            return op_go(args)
        return op_speak(args)
    except Exception as exc:
        return _fail(f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    raise SystemExit(main())
