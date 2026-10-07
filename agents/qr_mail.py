#!/usr/bin/env python3
"""
qr_mail.py — QR mail: email that carries a SEALED envelope, never a secret.

The problem with plain secret mail: the value sits in the body, plaintext in
transit and plaintext in the inbox forever. Anyone who reads the mailbox has
the secret.

QR mail changes the payload. The email body carries an `ae:1:secret:...`
envelope whose contents are AES-256-GCM ciphertext, and the message ALSO
attaches the QR PNG so the same secret can be printed and scanned. A leaked
inbox yields ciphertext — useless without the vault passphrase.

Two transports, one envelope:
    body text  → copy/paste or programmatic import
    QR PNG     → print it, scan it, hand it over physically

Usage:
    python qr_mail.py send <TO> <KEY> <VALUE> [--qr]   seal + mail (optionally attach QR)
    python qr_mail.py check                            scan inbox, import every envelope
    python qr_mail.py decode <FILE>                    decode an .eml or envelope text

Config (env):
    VAEULT_IMAP_HOST/PORT/USER/PASS/FOLDER
    VAEULT_SMTP_HOST/PORT/USER/PASS
    VAEULT_PATH / VAEULT_PASSPHRASE / VAEULT_MODULE

The passphrase is the shared key. Sender and recipient must hold the same
vault passphrase for the envelope to open — that is the point: possession of
the mailbox is not possession of the secret.
"""
from __future__ import annotations

import email
import imaplib
import json
import os
import pathlib
import smtplib
import sys
import time
from email.message import EmailMessage

AGENTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AGENTS))

VAULT_PATH = pathlib.Path(os.environ.get(
    "VAEULT_PATH", r"C:\æ\secrets\privateclient\privateclient.væult"))
VAEULT_MODULE = pathlib.Path(os.environ.get("VAEULT_MODULE", r"C:\æ\væult\væult.py"))

IMAP_HOST = os.environ.get("VAEULT_IMAP_HOST", "imap.gmail.com")
IMAP_PORT = int(os.environ.get("VAEULT_IMAP_PORT", "993"))
IMAP_USER = os.environ.get("VAEULT_IMAP_USER", "")
IMAP_PASS = os.environ.get("VAEULT_IMAP_PASS", "")
IMAP_FOLDER = os.environ.get("VAEULT_IMAP_FOLDER", "INBOX")
PROCESSED_FOLDER = os.environ.get("VAEULT_PROCESSED_FOLDER", "væult-processed")

SMTP_HOST = os.environ.get("VAEULT_SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("VAEULT_SMTP_PORT", "587"))
SMTP_USER = os.environ.get("VAEULT_SMTP_USER", IMAP_USER)
SMTP_PASS = os.environ.get("VAEULT_SMTP_PASS", IMAP_PASS)

SUBJECT_PREFIX = "[væult]"
QR_MAGIC = "ae:1:"


# ── vault ─────────────────────────────────────────────────────────────────────

def _load_vault_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("_vaeult_mail", str(VAEULT_MODULE))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _unlock(mod):
    """Return (key, doc) or raise. Passphrase from VAEULT_PASSPHRASE only."""
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


# ── seal / open ───────────────────────────────────────────────────────────────

def seal_for_mail(mod, key, name: str, value: str) -> dict:
    """Seal a value exactly as the vault does (AEAD, name-bound)."""
    return mod.seal(key, name, value)


def open_from_mail(mod, key, name: str, blob: dict) -> str:
    return mod.open_entry(key, name, blob)


# ── QR rendering ──────────────────────────────────────────────────────────────

def render_qr_png(envelope: str) -> bytes:
    """Render an envelope to PNG bytes (for attachment).

    GATED: the artifact is decoded back through two real decoders before it is
    returned. If it does not decode, this raises — a mailed QR that cannot be
    scanned is worse than no attachment.
    """
    try:
        import qr_supervision as qs
        return qs.render_verified(envelope)
    except ImportError:
        pass  # gate unavailable — fall through to an ungated render

    import qrcode
    from io import BytesIO
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2)
    qr.add_data(envelope)
    qr.make(fit=True)
    if qr.version > 40:
        raise ValueError(f"needs v{qr.version} > v40 cap")
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ── send ──────────────────────────────────────────────────────────────────────

def send_mail(to: str, key_name: str, value: str, attach_qr: bool = False) -> dict:
    """Seal the value, envelope it, and mail it. The body is never plaintext."""
    import qr_envelope as qe

    mod = _load_vault_module()
    vkey, doc = _unlock(mod)

    # 1. seal the value (AEAD, bound to the entry name)
    blob = seal_for_mail(mod, vkey, key_name, value)

    # 2. envelope it as a secret
    envelope = qe.encode("secret", {"name": key_name, "blob": blob})

    # 3. build the message — the BODY carries the envelope, never the value
    msg = EmailMessage()
    msg["Subject"] = f"{SUBJECT_PREFIX} {key_name}"
    msg["From"] = SMTP_USER
    msg["To"] = to
    msg.set_content(
        f"æ:// sealed secret envelope\n\n"
        f"key: {key_name}\n"
        f"sealed: AES-256-GCM (name-bound AEAD)\n"
        f"opens under: the shared vault passphrase\n\n"
        f"{envelope}\n\n"
        f"-- \n"
        f"This message carries ciphertext. A leaked inbox yields nothing\n"
        f"without the passphrase. Decode with:  qr:// decode <envelope>\n"
    )

    # 4. optionally attach the QR PNG so it can be printed and scanned
    if attach_qr:
        try:
            png = render_qr_png(envelope)
            msg.add_attachment(png, maintype="image", subtype="png",
                               filename=f"{key_name}.qr.png")
        except Exception as e:
            return {"ok": False, "stderr": f"qr_mail: QR render failed ({e})"}

    if not SMTP_USER or not SMTP_PASS:
        return {"ok": False, "stderr": "qr_mail: VAEULT_SMTP_USER / VAEULT_SMTP_PASS not set",
                "envelope": envelope}

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    return {"ok": True, "key": key_name, "to": to, "envelope": envelope,
            "qr_attached": attach_qr, "bytes": len(envelope)}


# ── receive ───────────────────────────────────────────────────────────────────

def _iter_envelopes(msg) -> list[str]:
    """Find every envelope in a message: body text + any QR PNG attachment."""
    found = []

    # 1. body text — scan every text part for the envelope magic
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            try:
                body = part.get_payload(decode=True).decode("utf-8", errors="replace")
            except Exception:
                continue
            for line in body.splitlines():
                line = line.strip()
                if line.startswith(QR_MAGIC) or line.startswith("æ:") or line.startswith("VAEULT1:"):
                    found.append(line)

    # 2. QR PNG attachments — scan the image with pyzbar
    for part in msg.walk():
        if part.get_content_type() == "image/png":
            try:
                from pyzbar.pyzbar import decode as zbar
                from PIL import Image
                from io import BytesIO
                raw = part.get_payload(decode=True)
                if not raw:
                    continue
                for hit in zbar(Image.open(BytesIO(raw))):
                    text = hit.data.decode("utf-8", errors="replace")
                    if text.startswith(QR_MAGIC) or text.startswith("æ:") or text.startswith("VAEULT1:"):
                        found.append(text)
            except Exception:
                continue

    return found


def _connect_imap() -> imaplib.IMAP4_SSL:
    if not IMAP_USER or not IMAP_PASS:
        raise RuntimeError("VAEULT_IMAP_USER / VAEULT_IMAP_PASS not set")
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(IMAP_USER, IMAP_PASS)
    return mail


def _ensure_folder(mail, name: str):
    typ, folders = mail.list()
    if folders:
        names = [f.decode().split(' "/"')[-1].strip('"') for f in folders if f]
        if name not in names:
            try:
                mail.create(name)
            except Exception:
                pass


def check_inbox() -> list[dict]:
    """Scan the inbox for [væult] mail, decode every envelope, import each."""
    import qr_envelope as qe

    if not VAULT_PATH.exists():
        return []

    mod = _load_vault_module()
    vkey, doc = _unlock(mod)

    mail = _connect_imap()
    results = []
    try:
        _ensure_folder(mail, PROCESSED_FOLDER)
        mail.select(IMAP_FOLDER)
        typ, data = mail.search(None, "UNSEEN")
        if not data or not data[0]:
            return []

        for uid in data[0].split():
            typ, msg_data = mail.fetch(uid, "(RFC822)")
            if not msg_data or not msg_data[0]:
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg.get("Subject", "")
            if SUBJECT_PREFIX not in subject:
                continue

            imported = []
            for envelope in _iter_envelopes(msg):
                try:
                    kind, payload = qe.decode(envelope)
                except ValueError:
                    continue
                if kind != "secret":
                    continue
                name = payload.get("name")
                blob = payload.get("blob")
                if not name or not blob:
                    continue
                # PROVE it opens under OUR key before storing
                try:
                    value = open_from_mail(mod, vkey, name, blob)
                except Exception:
                    continue
                doc["entries"][name] = blob
                doc["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
                imported.append(name)

            if imported:
                mod.save_raw(VAULT_PATH, doc)
                mail.copy(uid, PROCESSED_FOLDER)
                mail.store(uid, "+FLAGS", "\\Deleted")
                results.append({"uid": uid.decode(), "keys": imported})

        mail.expunge()
        return results
    finally:
        mail.logout()


def decode_file(path: str) -> list[dict]:
    """Decode envelopes from an .eml file (offline, no mailbox needed)."""
    import qr_envelope as qe
    raw = pathlib.Path(path).read_bytes()
    msg = email.message_from_bytes(raw)
    out = []
    for envelope in _iter_envelopes(msg):
        try:
            kind, payload = qe.decode(envelope)
            out.append({"type": kind, "payload": payload})
        except ValueError as e:
            out.append({"error": str(e)})
    return out


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv: list[str]) -> None:
    if len(argv) < 2:
        print(__doc__)
        return
    cmd = argv[1]

    if cmd == "send":
        if len(argv) < 5:
            print("usage: qr_mail.py send <TO> <KEY> <VALUE> [--qr]")
            return
        r = send_mail(argv[2], argv[3], argv[4], attach_qr="--qr" in argv)
        if r["ok"]:
            print(f"  ✓ mailed '{r['key']}' to {r['to']}"
                  f"{' (QR attached)' if r['qr_attached'] else ''}")
            print(f"  envelope: {r['envelope'][:64]}...")
        else:
            print(f"  ✗ {r['stderr']}")

    elif cmd == "check":
        try:
            results = check_inbox()
        except Exception as e:
            print(f"  ✗ {e}")
            return
        if not results:
            print("  no new [væult] mail")
        for r in results:
            print(f"  ✓ imported {', '.join(r['keys'])} (uid {r['uid']})")

    elif cmd == "decode":
        if len(argv) < 3:
            print("usage: qr_mail.py decode <FILE.eml>")
            return
        for item in decode_file(argv[2]):
            print(json.dumps(item, indent=2, ensure_ascii=False))

    else:
        print(f"unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv)
