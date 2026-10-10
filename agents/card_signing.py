#!/usr/bin/env python3
"""
card_signing.py — sign a kanban card so possession is not authority.

THE GAP
-------
`qr_kanban.py` renders a card carrying `{"cmd": "kanban://complete t_abc123"}`.
Nothing authenticates it. A photograph, a printout, or a screenshot of someone
else's card dispatches the same board mutation. Verified: `qr_kanban.py` contains
no signature check at all.

The pieces to fix this already existed and were unwired:
  · `contract_qr.py` ships Ed25519 `sign_contract` / `verify_contract`
  · the `capability` envelope type exists for `{grant, subject, expires}`

THE MODEL
---------
A card is a **capability**, not a route. The route says what to do; the
capability says who may do it and until when.

    unsigned  route       anyone holding the bytes can dispatch
    signed    capability  only a holder of the signing key can mint a valid card

Signing binds the card to:
  · the exact command  (so a signature cannot be replayed on another verb)
  · a subject          (the operator or agent the grant is for)
  · an expiry          (so a photographed card stops working)

WHAT THIS DOES AND DOES NOT BUY
-------------------------------
It DOES stop: forged cards, a card for `list` replayed as `archive`, and a card
photographed last month still working.

It does NOT stop: a genuine card photographed TODAY within its expiry. A bearer
token is a bearer token. For that, the verifier needs a nonce the board consumes
on first use — see `--single-use` below, which records spent nonces.

USAGE
-----
    # mint a signing key (once)
    python card_signing.py keygen --out C:\\æ\\secrets\\keys\\card.key

    # sign a card
    python card_signing.py sign --verb complete --task t_abc123 --ttl 3600

    # verify a card payload before dispatching it
    python card_signing.py verify '<payload json>'
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import pathlib
import secrets
import sys
import time

AGENTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AGENTS))

KEY_DIR = pathlib.Path(os.environ.get("CARD_KEY_DIR", r"C:\æ\secrets\keys"))
DEFAULT_KEY = KEY_DIR / "card.key"
SPENT_FILE = KEY_DIR / "card-spent.json"


# ── keys ──────────────────────────────────────────────────────────────────────

def _ed25519():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey)
    from cryptography.hazmat.primitives import serialization
    return Ed25519PrivateKey, Ed25519PublicKey, serialization


def keygen(out: pathlib.Path | None = None) -> dict:
    """Generate a card signing keypair. Returns paths + the public fingerprint."""
    Ed25519PrivateKey, _, serialization = _ed25519()
    out = pathlib.Path(out or DEFAULT_KEY)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        return {"ok": False, "error": f"refusing to overwrite existing key {out}"}

    priv = Ed25519PrivateKey.generate()
    priv_hex = priv.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()).hex()
    pub_hex = priv.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw).hex()

    out.write_text(priv_hex, encoding="ascii")
    try:
        os.chmod(out, 0o600)
    except OSError:
        pass
    pub = out.with_suffix(".pub")
    pub.write_text(pub_hex, encoding="ascii")

    return {"ok": True, "private": str(out), "public": str(pub),
            "fingerprint": hashlib.sha256(bytes.fromhex(pub_hex)).hexdigest()[:16]}


def load_private(path: pathlib.Path | None = None) -> bytes:
    p = pathlib.Path(path or DEFAULT_KEY)
    if not p.exists():
        raise FileNotFoundError(
            f"no card signing key at {p} — run: card_signing.py keygen")
    return bytes.fromhex(p.read_text(encoding="ascii").strip())


def load_public(path: pathlib.Path | None = None) -> bytes:
    p = pathlib.Path(path or DEFAULT_KEY).with_suffix(".pub")
    if not p.exists():
        raise FileNotFoundError(f"no card public key at {p}")
    return bytes.fromhex(p.read_text(encoding="ascii").strip())


# ── the signed card ───────────────────────────────────────────────────────────

def _canonical(verb: str, task_id: str | None, subject: str,
               expires_at: int, nonce: str) -> bytes:
    """The exact bytes a signature commits to.

    Canonicalised so signer and verifier cannot disagree about whitespace or key
    order — the classic way a signature scheme silently fails to verify.
    """
    return json.dumps({
        "verb": verb, "task_id": task_id or "", "subject": subject,
        "expires_at": expires_at, "nonce": nonce,
    }, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign_card(verb: str, task_id: str | None = None, *, ttl: int = 3600,
              subject: str | None = None, key_path: pathlib.Path | None = None,
              single_use: bool = False) -> dict:
    """Mint a signed capability card. Returns the payload to put in the envelope."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    subject = subject or os.environ.get("AGENT_ID") or os.environ.get("USERNAME") or "operator"
    expires_at = int(time.time()) + int(ttl)
    nonce = secrets.token_hex(8)

    priv = Ed25519PrivateKey.from_private_bytes(load_private(key_path))
    sig = priv.sign(_canonical(verb, task_id, subject, expires_at, nonce))
    pub_hex = priv.public_key().public_bytes(
        encoding=__import__("cryptography.hazmat.primitives.serialization",
                            fromlist=["serialization"]).Encoding.Raw,
        format=__import__("cryptography.hazmat.primitives.serialization",
                          fromlist=["serialization"]).PublicFormat.Raw).hex()

    return {
        "verb": verb,
        "task_id": task_id,
        "subject": subject,
        "expires_at": expires_at,
        "nonce": nonce,
        "single_use": bool(single_use),
        "sig": base64.urlsafe_b64encode(sig).decode("ascii").rstrip("="),
        "by": hashlib.sha256(bytes.fromhex(pub_hex)).hexdigest()[:16],
        "cmd": f"kanban://{verb}" + (f" {task_id}" if task_id else ""),
    }


# ── verification ──────────────────────────────────────────────────────────────

def _spent() -> set:
    if not SPENT_FILE.exists():
        return set()
    try:
        return set(json.loads(SPENT_FILE.read_text(encoding="utf-8")).get("nonces", []))
    except Exception:
        return set()


def _mark_spent(nonce: str):
    SPENT_FILE.parent.mkdir(parents=True, exist_ok=True)
    s = _spent()
    s.add(nonce)
    SPENT_FILE.write_text(json.dumps({"nonces": sorted(s)[-2000:]}, indent=1), encoding="utf-8")


def verify_card(payload: dict, *, public_key: bytes | None = None,
                consume: bool = False) -> dict:
    """Verify a signed card. Returns {ok, reason, ...}. Never raises.

    Checks, in order — each is a distinct refusal reason so a failure is
    diagnosable rather than a generic 'invalid':
      1. the payload carries a signature
      2. the signature verifies against the public key
      3. the card has not expired
      4. the nonce has not been spent (when single_use)
    """
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature

    if not isinstance(payload, dict):
        return {"ok": False, "reason": "payload is not an object"}
    sig_b64 = payload.get("sig")
    if not sig_b64:
        return {"ok": False, "reason": "unsigned card"}

    try:
        sig = base64.urlsafe_b64decode(sig_b64 + "=" * (-len(sig_b64) % 4))
    except Exception:
        return {"ok": False, "reason": "malformed signature encoding"}

    try:
        pub = public_key if public_key is not None else load_public()
    except FileNotFoundError as e:
        return {"ok": False, "reason": str(e)}

    msg = _canonical(payload.get("verb", ""), payload.get("task_id"),
                     payload.get("subject", ""), int(payload.get("expires_at", 0)),
                     payload.get("nonce", ""))
    try:
        Ed25519PublicKey.from_public_bytes(pub).verify(sig, msg)
    except InvalidSignature:
        return {"ok": False, "reason": "signature does not verify"}
    except Exception as e:
        return {"ok": False, "reason": f"verification error: {type(e).__name__}"}

    exp = int(payload.get("expires_at", 0))
    if exp and time.time() > exp:
        return {"ok": False, "reason": f"card expired {int(time.time() - exp)}s ago",
                "verb": payload.get("verb")}

    if payload.get("single_use"):
        if payload.get("nonce") in _spent():
            return {"ok": False, "reason": "card already used (nonce spent)",
                    "verb": payload.get("verb")}
        if consume:
            _mark_spent(payload["nonce"])

    return {"ok": True, "reason": "valid", "verb": payload.get("verb"),
            "task_id": payload.get("task_id"), "subject": payload.get("subject"),
            "expires_in": max(0, exp - int(time.time())) if exp else None}


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv):
    ap = argparse.ArgumentParser(description="sign kanban cards so possession is not authority")
    sub = ap.add_subparsers(dest="cmd")

    k = sub.add_parser("keygen")
    k.add_argument("--out", default=None)

    s = sub.add_parser("sign")
    s.add_argument("--verb", required=True)
    s.add_argument("--task", default=None)
    s.add_argument("--ttl", type=int, default=3600)
    s.add_argument("--subject", default=None)
    s.add_argument("--single-use", action="store_true")

    v = sub.add_parser("verify")
    v.add_argument("payload", help="the card payload as JSON")
    v.add_argument("--consume", action="store_true")

    a = ap.parse_args(argv[1:])

    if a.cmd == "keygen":
        r = keygen(pathlib.Path(a.out) if a.out else None)
        print(json.dumps(r, indent=2))
        return 0 if r.get("ok") else 1

    if a.cmd == "sign":
        card = sign_card(a.verb, a.task, ttl=a.ttl, subject=a.subject,
                         single_use=a.single_use)
        print(json.dumps(card, indent=2, ensure_ascii=False))
        return 0

    if a.cmd == "verify":
        try:
            payload = json.loads(a.payload)
        except json.JSONDecodeError as e:
            print(json.dumps({"ok": False, "reason": f"bad JSON: {e}"}))
            return 1
        r = verify_card(payload, consume=a.consume)
        print(json.dumps(r, indent=2))
        return 0 if r["ok"] else 1

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
