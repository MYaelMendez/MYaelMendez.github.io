"""Portable path, voice-alias and receipt helpers for tiny-voca.

Standard library only: this module must import cleanly without numpy,
onnxruntime or dizione.  Every location is derived from environment
variables so the CLI never carries a machine-local root.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

GENESIS = "0" * 64
AUTHORITY = "HUMAN://ROOT"
ACTION_TTS_SPEAK = "TTS://SPEAK"
ACTION_LESSON_BUILD = "LESSON://BUILD"
ACTION_PROMPT_BUILD = "PROMPT://BUILD"
ACTION_VOICE_BIND = "VOICE://BIND"
ACTION_VOICE_SPEAK = "VOICE://SPEAK"
SAMPLE_RATE = 24000

_F2_ALIASES = ("F2", "nous-girl", "nous_girl", "nous girl")
_M2_ALIASES = ("M2", "hermes-agent", "hermes_agent", "hermes agent")

VOICE_ALIASES = {
    "F2": {"id": "F2", "name": "nous-girl", "aliases": list(_F2_ALIASES)},
    "M2": {"id": "M2", "name": "hermes-agent", "aliases": list(_M2_ALIASES)},
}


def _normalize(value) -> str:
    text = str(value).strip().lower().replace("_", " ").replace("-", " ")
    return " ".join(text.split())


_ALIAS_TO_ID = {
    _normalize(alias): voice_id
    for voice_id, info in VOICE_ALIASES.items()
    for alias in info["aliases"]
}


def canonical_voice(value) -> str:
    """Map any accepted alias to its canonical id (F2 or M2)."""
    key = _normalize(value)
    if key in _ALIAS_TO_ID:
        return _ALIAS_TO_ID[key]
    raise ValueError(
        "unknown voice %r; accepted: F2/nous-girl and M2/hermes-agent" % (value,)
    )


# ---- runtime locations -------------------------------------------------

def hermes_home() -> Path:
    return Path(os.environ.get("HERMES_HOME") or (Path.home() / ".hermes")).expanduser()


def runtime_root() -> Path:
    """TINY_VOCA_HOME wins; otherwise HERMES_HOME/tiny-voca."""
    override = os.environ.get("TINY_VOCA_HOME")
    if override:
        return Path(override).expanduser()
    return hermes_home() / "tiny-voca"


def model_path(root=None) -> Path:
    base = Path(root).expanduser() if root is not None else runtime_root()
    return base / "onnx" / "model.onnx"


def config_path(root=None) -> Path:
    base = Path(root).expanduser() if root is not None else runtime_root()
    return base / "config.json"


def phonemizer_dir(root=None) -> Path:
    base = Path(root).expanduser() if root is not None else runtime_root()
    return base / "phonemizer"


def apply_env(root=None) -> str:
    """Point dizione at the runtime root's phonemizer data (override stale env)."""
    value = str(phonemizer_dir(root))
    os.environ["DIZIONE_DATA"] = value
    return value


def ledger_path() -> Path:
    override = os.environ.get("HERMES_TINY_VOCA_LEDGER")
    if override:
        return Path(override).expanduser()
    return hermes_home() / "tiny-voca-receipts.jsonl"


def default_output() -> Path:
    return Path.home() / ".hermes" / "tiny-voca-out.wav"


# ---- hash-chained receipts ---------------------------------------------

def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_hash(prev: str, body: dict) -> str:
    """H(prev || canonical_json(body without 'hash')), hex sha256."""
    payload = {key: value for key, value in body.items() if key != "hash"}
    return hashlib.sha256(
        str(prev).encode("utf-8") + canonical_json(payload).encode("utf-8")
    ).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def last_hash(path=None) -> str:
    ledger = Path(path) if path is not None else ledger_path()
    if not ledger.exists():
        return GENESIS
    lines = [line for line in ledger.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return GENESIS
    try:
        return json.loads(lines[-1]).get("hash") or GENESIS
    except (ValueError, AttributeError):
        return GENESIS


def build_receipt(result: dict, voice: str, alias: str, path=None, ts=None) -> dict:
    """Build one TTS://SPEAK receipt linked to the current ledger head."""
    body = {
        "ts": ts or _now(),
        "action": ACTION_TTS_SPEAK,
        "authority": AUTHORITY,
        "voice": voice,
        "alias": alias,
        "success": bool(result.get("success")),
        "sha256": result.get("sha256"),
        "duration_s": result.get("duration_s"),
        "output": result.get("output"),
        "prev": last_hash(path),
    }
    body["hash"] = compute_hash(body["prev"], body)
    return body


def append_receipt(result: dict, voice: str, alias: str, path=None) -> dict:
    """Append the receipt to the JSONL ledger and return it."""
    ledger = Path(path) if path is not None else ledger_path()
    receipt = build_receipt(result, voice, alias, ledger)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False) + "\n")
    return receipt


def append_custom_receipt(body: dict, path=None) -> dict:
    """Append an arbitrary receipt body to the same hash-chained ledger.

    The caller supplies action-specific fields; this helper adds the authority,
    timestamp, prev link, and hash. Verification treats every entry alike.
    """
    ledger = Path(path) if path is not None else ledger_path()
    record = dict(body)
    record.setdefault("ts", _now())
    record.setdefault("authority", AUTHORITY)
    record["prev"] = last_hash(ledger)
    record["hash"] = compute_hash(record["prev"], record)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def verify_chain(path=None) -> dict:
    """Validate both links (prev) and content hashes (hash) of a ledger."""
    ledger = Path(path) if path is not None else ledger_path()
    if not ledger.exists():
        return {"success": True, "ok": True, "count": 0, "head": GENESIS,
                "broken_at": None, "ledger": str(ledger), "authority": AUTHORITY}
    prev = GENESIS
    count = 0
    for number, line in enumerate(
        [line for line in ledger.read_text(encoding="utf-8").splitlines() if line.strip()], 1
    ):
        try:
            record = json.loads(line)
        except ValueError:
            return {"success": False, "ok": False, "count": count, "head": prev,
                    "broken_at": number, "reason": "invalid JSON",
                    "ledger": str(ledger), "authority": AUTHORITY}
        if record.get("prev") != prev:
            return {"success": False, "ok": False, "count": count, "head": prev,
                    "broken_at": number, "reason": "prev mismatch",
                    "ledger": str(ledger), "authority": AUTHORITY}
        if compute_hash(prev, record) != record.get("hash"):
            return {"success": False, "ok": False, "count": count, "head": prev,
                    "broken_at": number, "reason": "hash mismatch (tampered)",
                    "ledger": str(ledger), "authority": AUTHORITY}
        prev = record["hash"]
        count += 1
    return {"success": True, "ok": True, "count": count, "head": prev,
            "broken_at": None, "ledger": str(ledger), "authority": AUTHORITY}
