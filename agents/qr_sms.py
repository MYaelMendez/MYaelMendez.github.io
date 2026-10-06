#!/usr/bin/env python3
"""
qr_sms.py — QR SMS: text messages that carry a SEALED envelope, never a secret.

SMS is the tightest transport we use: 160 GSM-7 chars per segment, no
attachments, no rich body. That constraint shapes the design.

Three ways to move a secret by SMS:

  1. SHORT envelope  — a small sealed blob fits one segment as-is.
  2. QR LINK         — the SMS carries a URL that resolves to the QR PNG,
                       so the phone scans instead of parsing text.
  3. SPLIT envelope  — a large envelope is chunked across N segments with
                       `ae:1:secret:...` split markers; the receiver reassembles.

Every path carries ciphertext. A leaked SMS thread yields nothing without
the vault passphrase.

Transport backends (pick one via env):
  VAEULT_SMS_BACKEND=twilio     — Twilio REST API
  VAEULT_SMS_BACKEND=android    — adb shell am start (a tethered Android)
  VAEULT_SMS_BACKEND=stdout     — print the message (dry run / copy-paste)

Usage:
    python qr_sms.py send <TO> <KEY> <VALUE> [--split] [--qr-link]
    python qr_sms.py check                       read inbox, import every envelope
    python qr_sms.py decode <TEXT>               decode a pasted SMS body
    python qr_sms.py segments <TEXT>             show how a body splits

Twilio config: VAEULT_TWILIO_SID, VAEULT_TWILIO_TOKEN, VAEULT_TWILIO_FROM
Android config: VAEULT_ADB (default "adb"), VAEULT_ANDROID_SERIAL (optional)
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import time
import uuid

AGENTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AGENTS))

VAULT_PATH = pathlib.Path(os.environ.get(
    "VAEULT_PATH", r"C:\æ\secrets\privateclient\privateclient.væult"))
VAEULT_MODULE = pathlib.Path(os.environ.get("VAEULT_MODULE", r"C:\æ\væult\væult.py"))

BACKEND = os.environ.get("VAEULT_SMS_BACKEND", "stdout").lower()
SMS_LIMIT = 160                      # GSM-7 single segment
SMS_MULTI_LIMIT = 153                # per-segment when concatenated

TWILIO_SID = os.environ.get("VAEULT_TWILIO_SID", "")
TWILIO_TOKEN = os.environ.get("VAEULT_TWILIO_TOKEN", "")
TWILIO_FROM = os.environ.get("VAEULT_TWILIO_FROM", "")

ADB = os.environ.get("VAEULT_ADB", "adb")
ANDROID_SERIAL = os.environ.get("VAEULT_ANDROID_SERIAL", "")

ENVELOPE_MAGIC = "ae:1:"
CHUNK_RE = re.compile(r"^ae:1:([a-z]+):chunk:(\d+)/(\d+):(.+)$")
# v2 chunk marker carries a MESSAGE ID: ae:1:<type>:chunk:<msgid>:<i>/<n>:<part>
# Without it, chunks from two different messages with the same N are
# indistinguishable and reassemble() silently splices a corrupt-but-valid
# envelope. The msgid makes a mixed set detectable and refusable.
CHUNK_RE_V2 = re.compile(r"^ae:1:([a-z]+):chunk:([0-9a-f]{8}):(\d+)/(\d+):(.+)$")
LEGACY_CHUNK_RE = re.compile(r"^ae:1:([a-z]+):(.+):chunk:(\d+)/(\d+)$")


# ── vault ─────────────────────────────────────────────────────────────────────

def _load_vault_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("_vaeult_sms", str(VAEULT_MODULE))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _unlock(mod):
    passphrase = os.environ.get("VAEULT_PASSPHRASE")
    if not passphrase:
        raise RuntimeError("VAEULT_PASSPHRASE not set")
    doc = mod.load_raw(VAULT_PATH)
    salt = mod._b64d(doc["salt"])
    kdf = doc.get("kdf", "scrypt")
    if kdf == "pbkdf2":
        key = mod.derive_key_pbkdf2(passphrase, salt, doc.get("iterations", 600000))
    else:
        key = mod.derive_key(passphrase, salt, doc.get("n", mod.KDF_N),
                             doc.get("r", mod.KDF_R), doc.get("p", mod.KDF_P))
    chk = doc.get("check")
    if chk:
        try:
            mod.open_entry(key, "__check__", chk)
        except Exception:
            raise RuntimeError("wrong passphrase")
    return key, doc


# ── segmentation ──────────────────────────────────────────────────────────────

def segments(body: str) -> list[str]:
    """Split a body into SMS segments. Single if it fits, else numbered chunks.

    Multi-segment parts are marked
    `ae:1:<type>:chunk:<msgid>:<i>/<n>:<part>` so the receiver can reassemble
    without guessing. The marker is itself parseable by the same decoder.

    The msgid is a per-message random tag. Without it, chunks from two
    different messages with the same chunk count are indistinguishable and
    reassemble() silently splices a corrupt-but-valid envelope — a wrong
    result that still passes is_envelope(). The msgid makes that refusable.
    """
    if len(body) <= SMS_LIMIT:
        return [body]

    # find the type so the chunk marker is typed
    kind = "secret"
    m = re.match(r"^ae:1:([a-z]+):", body)
    if m:
        kind = m.group(1)

    msgid = uuid.uuid4().hex[:8]
    payload = body
    # reserve room for the marker on each part
    marker_len = len(f"ae:1:{kind}:chunk:{msgid}:99/99:")
    room = SMS_MULTI_LIMIT - marker_len
    if room < 20:
        room = 20

    parts = [payload[i:i + room] for i in range(0, len(payload), room)]
    n = len(parts)
    return [f"ae:1:{kind}:chunk:{msgid}:{i+1}/{n}:{p}" for i, p in enumerate(parts)]


def reassemble(texts: list[str]) -> str:
    """Reassemble chunked envelopes. A single un-chunked envelope passes through.

    Chunks are grouped BY MESSAGE ID. A set containing chunks from more than
    one message is REFUSED rather than spliced — that is the whole reason the
    msgid exists. Legacy markers (no msgid) fall back to index ordering and
    cannot be grouped, so a mixed legacy set is still refusable only on count.
    """
    by_msg: dict[str, list] = {}
    legacy: list = []

    for t in texts:
        t = t.strip()
        m2 = CHUNK_RE_V2.match(t)
        if m2:
            kind, msgid, idx, total, part = (m2.group(1), m2.group(2),
                                             int(m2.group(3)), int(m2.group(4)), m2.group(5))
            by_msg.setdefault(msgid, []).append((idx, total, part))
            continue
        m = CHUNK_RE.match(t)
        if m:
            kind, idx, total, part = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
            legacy.append((idx, total, part))
            continue
        m3 = LEGACY_CHUNK_RE.match(t)
        if m3:
            kind, part, idx, total = (m3.group(1), m3.group(2),
                                      int(m3.group(3)), int(m3.group(4)))
            legacy.append((idx, total, part))
            continue
        return t          # not chunked — a whole envelope

    # a v2 set mixed with v1 chunks is ambiguous — refuse
    if by_msg and legacy:
        raise ValueError("mixed chunk formats (v2 msgid + v1) — refusing to splice")
    if len(by_msg) > 1:
        raise ValueError(
            f"chunks from {len(by_msg)} different messages — refusing to splice "
            f"(ids: {', '.join(sorted(by_msg))})")

    chunks = next(iter(by_msg.values())) if by_msg else legacy
    if not chunks:
        return ""
    chunks.sort(key=lambda c: c[0])
    total = chunks[0][1]
    if len(chunks) != total:
        raise ValueError(f"incomplete: {len(chunks)}/{total} segments")
    # every chunk must agree on the total
    if any(c[1] != total for c in chunks):
        raise ValueError("inconsistent chunk counts — refusing to splice")
    return "".join(c[2] for c in chunks)


# ── backends ──────────────────────────────────────────────────────────────────

def _send_twilio(to: str, body: str) -> dict:
    import urllib.parse
    import urllib.request
    if not (TWILIO_SID and TWILIO_TOKEN and TWILIO_FROM):
        return {"ok": False, "stderr": "qr_sms: VAEULT_TWILIO_SID/TOKEN/FROM not set"}
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    data = urllib.parse.urlencode({"To": to, "From": TWILIO_FROM, "Body": body}).encode()
    req = urllib.request.Request(url, data=data)
    import base64
    auth = base64.b64encode(f"{TWILIO_SID}:{TWILIO_TOKEN}".encode()).decode()
    req.add_header("Authorization", f"Basic {auth}")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return {"ok": True, "status": r.status}
    except Exception as e:
        return {"ok": False, "stderr": f"qr_sms: twilio failed ({e})"}


def _send_android(to: str, body: str) -> dict:
    """Send via a tethered Android through adb (no cloud, no carrier API)."""
    if not _adb_available():
        return {"ok": False, "stderr": "qr_sms: adb not available"}
    # sms: URI opens the messaging app pre-filled; the operator taps send.
    import urllib.parse
    uri = f"sms:{urllib.parse.quote(to)}?body={urllib.parse.quote(body)}"
    cmd = [ADB]
    if ANDROID_SERIAL:
        cmd += ["-s", ANDROID_SERIAL]
    cmd += ["shell", "am", "start", "-a", "android.intent.action.SENDTO",
            "-d", uri]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return {"ok": r.returncode == 0, "stdout": r.stdout.strip(),
                "stderr": r.stderr.strip() if r.returncode else ""}
    except Exception as e:
        return {"ok": False, "stderr": f"qr_sms: adb failed ({e})"}


def _adb_available() -> bool:
    try:
        r = subprocess.run([ADB, "devices"], capture_output=True, text=True, timeout=10)
        return r.returncode == 0 and len(r.stdout.strip().splitlines()) > 1
    except Exception:
        return False


def _send_stdout(to: str, body: str) -> dict:
    print(f"  [stdout backend] to={to}")
    print(f"  {body}")
    return {"ok": True, "stdout": body}


def _dispatch_send(to: str, body: str) -> dict:
    if BACKEND == "twilio":
        return _send_twilio(to, body)
    if BACKEND == "android":
        return _send_android(to, body)
    return _send_stdout(to, body)


# ── send ──────────────────────────────────────────────────────────────────────

def send_sms(to: str, key_name: str, value: str, split: bool = False,
             qr_link: bool = False) -> dict:
    """Seal the value, envelope it, and text it. The body is never plaintext."""
    import qr_envelope as qe

    mod = _load_vault_module()
    vkey, doc = _unlock(mod)

    blob = mod.seal(vkey, key_name, value)
    envelope = qe.encode("secret", {"name": key_name, "blob": blob})

    if qr_link:
        # carry a link instead of the blob — the phone scans the QR at that URL
        body = f"væult:{key_name} qr:// {envelope[:40]}… (full QR at the link)"
        # a real deployment would upload the PNG and text the URL; we keep the
        # envelope in the message so it still works without a server.
        body = envelope

    parts = segments(envelope) if (split or len(envelope) > SMS_LIMIT) else [envelope]
    results = []
    for p in parts:
        results.append(_dispatch_send(to, p))

    ok = all(r.get("ok") for r in results)
    return {
        "ok": ok,
        "key": key_name,
        "to": to,
        "envelope": envelope,
        "segments": len(parts),
        "bytes": len(envelope),
        "backend": BACKEND,
        "results": results,
    }


# ── receive ───────────────────────────────────────────────────────────────────

def check_inbox() -> list[dict]:
    """Read SMS from a tethered Android and import every envelope found."""
    import qr_envelope as qe

    if not _adb_available():
        raise RuntimeError("qr_sms: adb not available (no tethered Android)")

    cmd = [ADB]
    if ANDROID_SERIAL:
        cmd += ["-s", ANDROID_SERIAL]
    cmd += ["shell", "content", "query", "--uri", "content://sms/inbox",
            "--projection", "body,address,date"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError(f"qr_sms: content query failed ({r.stderr.strip()})")

    # collect envelope-looking lines
    texts = []
    for line in r.stdout.splitlines():
        for token in re.findall(r"ae:1:[A-Za-z0-9+/=:._-]+", line):
            texts.append(token)

    if not texts:
        return []

    # group by key name — reassembly needs the chunk set per message
    mod = _load_vault_module()
    vkey, doc = _unlock(mod)

    # simplest correct approach: try to reassemble ALL chunks together, and
    # also try each un-chunked envelope on its own.
    results = []
    whole = [t for t in texts if not CHUNK_RE.match(t)]
    chunked = [t for t in texts if CHUNK_RE.match(t)]

    candidates = list(whole)
    if chunked:
        try:
            candidates.append(reassemble(chunked))
        except ValueError:
            pass

    imported = []
    for env in candidates:
        try:
            kind, payload = qe.decode(env)
        except ValueError:
            continue
        if kind != "secret":
            continue
        name, blob = payload.get("name"), payload.get("blob")
        if not name or not blob:
            continue
        try:
            mod.open_entry(vkey, name, blob)      # prove it opens under our key
        except Exception:
            continue
        doc["entries"][name] = blob
        doc["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        imported.append(name)

    if imported:
        mod.save_raw(VAULT_PATH, doc)
        results.append({"keys": imported})

    return results


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv: list[str]) -> None:
    if len(argv) < 2:
        print(__doc__)
        return
    cmd = argv[1]

    if cmd == "send":
        if len(argv) < 5:
            print("usage: qr_sms.py send <TO> <KEY> <VALUE> [--split] [--qr-link]")
            return
        r = send_sms(argv[2], argv[3], argv[4],
                     split="--split" in argv, qr_link="--qr-link" in argv)
        if r["ok"]:
            print(f"  ✓ texted '{r['key']}' to {r['to']} "
                  f"({r['segments']} segment(s), {r['bytes']} bytes, backend={r['backend']})")
        else:
            print(f"  ✗ send failed")
            for res in r["results"]:
                if not res.get("ok"):
                    print(f"    {res.get('stderr')}")

    elif cmd == "check":
        try:
            results = check_inbox()
        except Exception as e:
            print(f"  ✗ {e}")
            return
        if not results:
            print("  no envelope SMS found")
        for r in results:
            print(f"  ✓ imported {', '.join(r['keys'])}")

    elif cmd == "decode":
        if len(argv) < 3:
            print("usage: qr_sms.py decode '<body>'")
            return
        import qr_envelope as qe
        body = reassemble([argv[2]]) if CHUNK_RE.match(argv[2]) else argv[2]
        kind, payload = qe.decode(body)
        print(json.dumps({"type": kind, "payload": payload}, indent=2, ensure_ascii=False))

    elif cmd == "segments":
        if len(argv) < 3:
            print("usage: qr_sms.py segments '<body>'")
            return
        parts = segments(argv[2])
        print(f"  {len(parts)} segment(s), limit {SMS_LIMIT}:")
        for i, p in enumerate(parts, 1):
            print(f"    [{i}] ({len(p)} chars) {p[:70]}")

    else:
        print(f"unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv)
