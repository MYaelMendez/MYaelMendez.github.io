"""Backend routes for the tinyVOCA Hermes Desktop dock.

Exports `router = APIRouter()` mounted at `/api/plugins/tiny-voca-voice/`.
Heavy imports stay inside subprocesses: this module is stdlib + FastAPI only.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from fastapi import APIRouter, HTTPException

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = ROOT / "identity.json"
CLI = ROOT / "scripts" / "tiny_voca_voice.py"
VERSION = "1.3.1"
router = APIRouter()


def _home() -> Path:
    return Path(os.environ.get("HERMES_HOME") or (Path.home() / ".hermes")).expanduser()


def _runtime() -> Path:
    override = os.environ.get("TINY_VOCA_HOME")
    return Path(override).expanduser() if override else _home() / "tiny-voca"


def _identity() -> dict:
    if not IDENTITY.exists():
        raise HTTPException(503, "identity.json missing from tiny-voca plugin")
    try:
        return json.loads(IDENTITY.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HTTPException(503, f"identity.json invalid: {exc}")


def _canonical_voice(value: str, identity: dict) -> str:
    raw = str(value or "M2").strip().lower().replace("_", " ").replace("-", " ")
    for voice_id, binding in identity.get("bindings", {}).items():
        aliases = [str(a).strip().lower().replace("_", " ").replace("-", " ") for a in binding.get("aliases", [])]
        if raw in aliases:
            return "F2" if binding.get("source_voice") else voice_id
    raise HTTPException(400, "voice must be F2, M2, or ROBOT")


def _parse_json(stdout: str) -> dict:
    raw = (stdout or "").strip()
    if not raw:
        return {"success": False, "error": "empty output from tiny-voca CLI"}
    for candidate in (raw, raw.splitlines()[-1]):
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    return {"success": False, "error": "tiny-voca CLI did not emit JSON"}


@router.get("/status")
async def status() -> dict:
    identity = _identity()
    runtime = _runtime()
    return {
        "success": True,
        "authority": "HUMAN://ROOT",
        "version": VERSION,
        "runtime": str(runtime),
        "model_present": (runtime / "onnx" / "model.onnx").exists(),
        "voices": list(identity.get("bindings", {})),
        "compute_layers": identity.get("compute_layers", {}),
    }


@router.get("/identity")
async def identity_route() -> dict:
    identity = _identity()
    return {"success": True, "authority": "HUMAN://ROOT", "identity": identity}


@router.post("/speak")
async def speak(body: dict) -> dict:
    identity = _identity()
    text = str((body or {}).get("text", "")).strip()
    if not text:
        raise HTTPException(400, "text is required")
    if len(text) > 1000:
        raise HTTPException(400, "text must be 1000 characters or fewer")
    requested = str((body or {}).get("voice", "M2"))
    voice = _canonical_voice(requested, identity)
    try:
        speed = float((body or {}).get("speed", 1.25))
    except (TypeError, ValueError):
        raise HTTPException(400, "speed must be a number")
    speed = max(0.5, min(2.0, speed))

    if not CLI.exists():
        raise HTTPException(503, "tiny-voca CLI missing from plugin package")
    out_dir = _home() / "tiny-voca-desktop"
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / f"speak-{int(time.time() * 1000)}.wav"
    py = os.environ.get("HERMES_TINY_VOCA_PYTHON") or shutil.which("python3") or sys.executable
    cmd = [py, str(CLI), "--text", text, "--voice", voice,
           "--output", str(output), "--speed", str(speed)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except Exception as exc:
        raise HTTPException(500, f"synthesis failed: {type(exc).__name__}: {exc}")
    result = _parse_json(proc.stdout)
    if proc.returncode != 0 or not result.get("success"):
        raise HTTPException(500, result.get("error") or (proc.stderr or "synthesis failed")[-500:])
    return {
        "success": True,
        "authority": "HUMAN://ROOT",
        "voice": voice,
        "alias": requested,
        "speed": speed,
        "output": str(output),
        "sha256": result.get("sha256"),
        "duration_s": result.get("duration_s"),
        "receipt": result.get("receipt"),
    }
