#!/usr/bin/env python3
"""
qr_envelope.py — the unified æ:// QR envelope.

ONE format for everything we QR-encode. A scanner reads the prefix, dispatches
on the type, and knows exactly what it holds without guessing.

Wire format (text, QR-safe, base64url, no padding):

    ae:1:<type>:<b64url(json)>

  · "ae:"    — the magic. ASCII, charset-proof (see decode() note).
  · "1"      — envelope version.
  · <type>   — one of the TYPES below.
  · <b64url> — the payload, base64url-encoded JSON (no padding).

Why base64url: QR alphanumeric mode is denser, and base64url avoids the
"+", "/", "=" characters that force byte mode. A 2.9KB payload fits a v40 QR.

TYPES
  key        — an Ed25519/RSA keypair (public + private, paper backup)
  secret     — a SEALED vault entry (væult: nonce + ciphertext)
  contract   — a smart contract (escrow, multisig, timelock, ...)
  capability — an authorization grant (what an agent may do, until when)
  route      — a scheme command to execute (e.g. "væult:// status")
  handoff    — an agent-to-agent transfer (identity + payload)
  identity   — a node's public identity (no secrets)
  manifest   — a surface index fragment (for offline distribution)

Backward compatibility: `væult.py` still emits `VAEULT1:` payloads; decode()
recognizes that legacy prefix and maps it to type "secret".

Usage:
    from qr_envelope import encode, decode, TYPES
    text = encode("secret", {"name": "API_KEY", "blob": {...}})
    kind, payload = decode(text)          # -> ("secret", {...})
    text = encode("route", {"cmd": "væult:// status"})

CLI:
    python qr_envelope.py encode <type> '<json>'
    python qr_envelope.py decode '<envelope text>'
    python qr_envelope.py inspect '<envelope text>'
    python qr_envelope.py types
"""
from __future__ import annotations

import base64
import json
import sys

MAGIC = "ae:"
VERSION = "1"
LEGACY_PREFIX = "VAEULT1:"          # væult.py's original format

TYPES = (
    "key",          # Ed25519/RSA keypair
    "secret",       # sealed vault entry
    "contract",     # smart contract
    "capability",   # authorization grant
    "route",        # a scheme command
    "handoff",      # agent-to-agent transfer
    "identity",     # node public identity
    "manifest",     # surface index fragment
)


# ── codec ─────────────────────────────────────────────────────────────────────

def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64url_decode(text: str) -> bytes:
    pad = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + pad)


def encode(kind: str, payload: dict) -> str:
    """Encode a typed payload into an æ:// QR envelope string."""
    if kind not in TYPES:
        raise ValueError(f"unknown type '{kind}' (valid: {', '.join(TYPES)})")
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dict")
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return f"{MAGIC}{VERSION}:{kind}:{_b64url_encode(raw)}"


def decode(text: str) -> tuple[str, dict]:
    """Decode an envelope. Returns (kind, payload).

    Accepts the unified ae: format and the legacy VAEULT1: format.
    Raises ValueError on anything unrecognized.

    NOTE ON THE MAGIC: it is ASCII ("ae:"), not the rune "æ:". pyzbar
    re-interprets the UTF-8 bytes of "æ" as halfwidth katakana ("ﾃｦ"),
    so a rune magic survives generation but fails on scan. An ASCII magic
    is charset-proof across every decoder — the æ identity lives in the
    payload and the surface, not in the transport bytes.
    """
    text = (text or "").strip()

    # legacy væult payloads → normalized to the "secret" type
    if text.startswith(LEGACY_PREFIX):
        body = text[len(LEGACY_PREFIX):]
        return "secret", json.loads(body)

    # tolerate a scanner that returned the rune form (older payloads)
    if text.startswith("æ:"):
        text = "ae:" + text[2:]

    if not text.startswith(MAGIC):
        raise ValueError("not an æ:// envelope (missing 'ae:' magic)")

    parts = text.split(":", 3)
    if len(parts) != 4:
        raise ValueError("malformed envelope (expected ae:1:<type>:<data>)")

    _, version, kind, data = parts
    if version != VERSION:
        raise ValueError(f"unsupported envelope version '{version}'")
    if kind not in TYPES:
        raise ValueError(f"unknown envelope type '{kind}'")

    try:
        payload = json.loads(_b64url_decode(data).decode("utf-8"))
    except Exception as exc:
        raise ValueError(f"corrupt payload ({exc})") from exc

    return kind, payload


def is_envelope(text: str) -> bool:
    """Cheap check: does this text look like an envelope we can decode?"""
    t = (text or "").strip()
    return t.startswith(MAGIC) or t.startswith(LEGACY_PREFIX)


def inspect(text: str) -> dict:
    """Decode and describe without exposing the full payload (safe for logs)."""
    kind, payload = decode(text)
    keys = sorted(payload.keys())
    # a per-type hint of what the payload carries — never the values
    hints = {
        "key":        [k for k in keys if k in ("algorithm", "fingerprint", "public_key")],
        "secret":     [k for k in keys if k in ("name", "blob")],
        "contract":   [k for k in keys if k in ("type", "parties", "hash")],
        "capability": [k for k in keys if k in ("grant", "expires", "subject")],
        "route":      ["cmd"] if "cmd" in keys else [],
        "handoff":    [k for k in keys if k in ("from", "to", "kind")],
        "identity":   [k for k in keys if k in ("node", "public_key", "host")],
        "manifest":   [k for k in keys if k in ("surfaces", "base_url")],
    }
    return {
        "type": kind,
        "version": VERSION,
        "fields": keys,
        "carries": hints.get(kind, []),
        "bytes": len(text),
        "sealed": kind in ("secret", "capability"),   # payload is ciphertext/opaque
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv: list[str]) -> None:
    if len(argv) < 2 or argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return

    cmd = argv[1]

    if cmd == "types":
        for t in TYPES:
            print(f"  {t}")
        return

    if cmd == "encode":
        if len(argv) < 4:
            print("usage: qr_envelope.py encode <type> '<json>'")
            return
        kind = argv[2]
        payload = json.loads(argv[3])
        print(encode(kind, payload))
        return

    if cmd == "decode":
        if len(argv) < 3:
            print("usage: qr_envelope.py decode '<envelope>'")
            return
        kind, payload = decode(argv[2])
        print(f"type: {kind}")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if cmd == "inspect":
        if len(argv) < 3:
            print("usage: qr_envelope.py inspect '<envelope>'")
            return
        print(json.dumps(inspect(argv[2]), indent=2, ensure_ascii=False))
        return

    print(f"unknown command '{cmd}'")


if __name__ == "__main__":
    main(sys.argv)
