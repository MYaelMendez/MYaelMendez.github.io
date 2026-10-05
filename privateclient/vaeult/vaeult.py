#!/usr/bin/env python3
"""væult — a password-secured local vault for sovereign secrets.

Custody model (per the æ standing rule):
  * the vault file is ENCRYPTED AT REST with a key derived from a passphrase
    the operator types (never stored, never echoed, never logged);
  * it lives under C:\\æ\\secrets\\ — the gitignored custody root;
  * the plaintext never touches disk, the transcript, or a remote URL.

Crypto: scrypt (N=2^15, r=8, p=1) -> 32-byte key -> AES-256-GCM (AEAD).
Every entry is encrypted with a fresh 96-bit nonce; the GCM tag authenticates
both the ciphertext and the entry name, so a tampered or swapped entry fails
closed rather than decrypting to garbage.

Format (JSON envelope, base64 fields):
  {"v": 1, "kdf": "scrypt", "n": 32768, "r": 8, "p": 1,
   "salt": "...", "created": "...", "entries": {"NAME": {"n":"...","ct":"..."}}}

Usage:
  python væult.py init                 # create the vault (asks for a passphrase twice)
  python væult.py set NAME             # add/update a secret (value read hidden)
  python væult.py get NAME             # print a secret to stdout
  python væult.py list                 # list entry names (never values)
  python væult.py rm NAME              # delete an entry
  python væult.py export NAME          # print shell-safe export line
  python væult.py verify               # self-test: round-trip + tamper detection

QR air-gap handoff (transport, never plaintext):
  python væult.py qr NAME [--out P]    # encode ONE sealed entry as a QR PNG
  python væult.py qr-open IMAGE        # decode a QR PNG and import the entry
  python væult.py qr-show NAME         # print the QR payload as text (terminal/ASCII)

The QR carries the entry's SEALED blob (name + nonce + ciphertext), not the
plaintext — so a photographed or shoulder-surfed QR is useless without the
vault passphrase. This is the same AEAD envelope the vault stores; QR is just a
second transport for it. A large secret may exceed QR version 40 capacity; the
command says so instead of truncating.


Passphrase source (first match wins):
  VAEULT_PASSPHRASE env var  ->  interactive getpass prompt
The env var exists so a scripted consumer can unlock non-interactively; it is
NEVER persisted and NEVER printed.
"""
from __future__ import annotations

import base64
import getpass
import hashlib
import json
import os
import pathlib
import secrets as _secrets
import sys
import time

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def _default_vault() -> pathlib.Path:
    """Neutral default: a `secrets/privateclient/` convention under the user's
    home, so the tool is portable (OSW). The operator's own root is set with
    VAEULT_PATH, never baked in."""
    return pathlib.Path.home() / "secrets" / "privateclient" / "privateclient.væult"


DEFAULT_VAULT = _default_vault()

KDF_N, KDF_R, KDF_P = 32768, 8, 1          # scrypt cost (2^15 = ~32MB, ~50ms)
KEY_LEN, NONCE_LEN, TAG_LEN = 32, 12, 16


# ── crypto ────────────────────────────────────────────────────────────────────

def _b64e(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def _b64d(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


def derive_key(passphrase: str, salt: bytes, n: int = KDF_N,
               r: int = KDF_R, p: int = KDF_P) -> bytes:
    return hashlib.scrypt(passphrase.encode("utf-8"), salt=salt,
                          n=n, r=r, p=p, dklen=KEY_LEN, maxmem=128 * 1024 * 1024)


def derive_key_pbkdf2(passphrase: str, salt: bytes, iterations: int = 600000) -> bytes:
    """PBKDF2-HMAC-SHA256 — matches the web vault (v2) format."""
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"),
                               salt, iterations, dklen=KEY_LEN)


def _aad(name: str) -> bytes:
    """Bind the entry name into the AEAD so a renamed entry fails to open."""
    return b"vault-entry:" + name.encode("utf-8")


def seal(key: bytes, name: str, value: str) -> dict:
    nonce = _secrets.token_bytes(NONCE_LEN)
    ct = AESGCM(key).encrypt(nonce, value.encode("utf-8"), _aad(name))
    return {"n": _b64e(nonce), "ct": _b64e(ct)}


def open_entry(key: bytes, name: str, blob: dict) -> str:
    nonce, ct = _b64d(blob["n"]), _b64d(blob["ct"])
    return AESGCM(key).decrypt(nonce, ct, _aad(name)).decode("utf-8")


# ── vault file ────────────────────────────────────────────────────────────────

def load_raw(path: pathlib.Path) -> dict:
    if not path.exists():
        sys.exit(f"væult: no vault at {path}\n  run: python {pathlib.Path(__file__).name} init")
    return json.loads(path.read_text(encoding="utf-8"))


def save_raw(path: pathlib.Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, path)                 # atomic
    try:                                   # best-effort 0600 on POSIX
        os.chmod(path, 0o600)
    except OSError:
        pass


def unlock(doc: dict, passphrase: str | None = None) -> bytes:
    salt = _b64d(doc["salt"])
    if passphrase is None:
        passphrase = os.environ.get("VAEULT_PASSPHRASE") or getpass.getpass("væult passphrase: ")
    kdf = doc.get("kdf", "scrypt")
    if kdf == "pbkdf2":
        key = derive_key_pbkdf2(passphrase, salt, doc.get("iterations", 600000))
    else:
        n, r, p = doc.get("n", KDF_N), doc.get("r", KDF_R), doc.get("p", KDF_P)
        key = derive_key(passphrase, salt, n, r, p)
    # cheap sentinel check so a wrong passphrase says so, not "decrypt failed"
    chk = doc.get("check")
    if chk:
        try:
            open_entry(key, "__check__", chk)
        except Exception:
            sys.exit("væult: wrong passphrase (or corrupt vault)")
    return key


# ── commands ──────────────────────────────────────────────────────────────────

def cmd_init(path: pathlib.Path, args: list[str]) -> None:
    if path.exists() and "--force" not in args:
        sys.exit(f"væult: vault already exists at {path} (use --force to overwrite)")
    p1 = os.environ.get("VAEULT_PASSPHRASE") or getpass.getpass("new vault passphrase: ")
    if not os.environ.get("VAEULT_PASSPHRASE"):
        p2 = getpass.getpass("confirm passphrase: ")
        if p1 != p2:
            sys.exit("væult: passphrases did not match")
    if len(p1) < 8:
        sys.exit("væult: passphrase must be at least 8 characters")
    salt = _secrets.token_bytes(32)
    doc = {"v": 1, "kdf": "scrypt", "n": KDF_N, "r": KDF_R, "p": KDF_P,
           "salt": _b64e(salt), "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "entries": {}}
    key = derive_key(p1, salt)
    doc["check"] = seal(key, "__check__", "ok")     # wrong-passphrase sentinel
    save_raw(path, doc)
    print(f"væult: created {path}")
    print(f"  kdf=scrypt n={KDF_N} r={KDF_R} p={KDF_P} · cipher=AES-256-GCM")


def cmd_set(path: pathlib.Path, args: list[str]) -> None:
    if not args:
        sys.exit("usage: væult set NAME")
    name = args[0]
    doc = load_raw(path)
    key = unlock(doc)
    value = os.environ.get("VAEULT_VALUE") or getpass.getpass(f"value for {name} (hidden): ")
    if not value:
        sys.exit("væult: empty value refused")
    doc["entries"][name] = seal(key, name, value)
    doc["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    save_raw(path, doc)
    print(f"væult: stored '{name}' ({len(value)} chars, encrypted)")


def cmd_get(path: pathlib.Path, args: list[str]) -> None:
    if not args:
        sys.exit("usage: væult get NAME")
    name = args[0]
    doc = load_raw(path)
    if name not in doc["entries"]:
        sys.exit(f"væult: no entry '{name}'")
    key = unlock(doc)
    sys.stdout.write(open_entry(key, name, doc["entries"][name]))
    sys.stdout.write("\n")


def cmd_list(path: pathlib.Path, args: list[str]) -> None:
    doc = load_raw(path)
    entries = doc.get("entries", {})
    print(f"væult: {path}")
    print(f"  created {doc.get('created','?')} · updated {doc.get('updated','?')} · "
          f"{len(entries)} entr{'y' if len(entries)==1 else 'ies'}")
    for name in sorted(entries):
        blob = entries[name]
        print(f"  • {name}  ({len(_b64d(blob['ct'])) - TAG_LEN} bytes ct)")


def cmd_rm(path: pathlib.Path, args: list[str]) -> None:
    if not args:
        sys.exit("usage: væult rm NAME")
    name = args[0]
    doc = load_raw(path)
    if name not in doc["entries"]:
        sys.exit(f"væult: no entry '{name}'")
    unlock(doc)                       # require the passphrase to delete
    del doc["entries"][name]
    save_raw(path, doc)
    print(f"væult: removed '{name}'")


def cmd_export(path: pathlib.Path, args: list[str]) -> None:
    if not args:
        sys.exit("usage: væult export NAME")
    name = args[0]
    doc = load_raw(path)
    if name not in doc["entries"]:
        sys.exit(f"væult: no entry '{name}'")
    key = unlock(doc)
    val = open_entry(key, name, doc["entries"][name])
    # shell-safe: single-quote, escape embedded quotes
    print(f"export {name}='{val.replace(chr(39), chr(39)+chr(92)+chr(39)+chr(39))}'")


def cmd_verify(path: pathlib.Path, args: list[str]) -> None:
    """Self-test: round-trip, wrong-passphrase, tamper detection."""
    doc = load_raw(path)
    key = unlock(doc)
    name = "__selftest__"
    secret = "væult-selftest-" + _secrets.token_hex(8)
    blob = seal(key, name, secret)
    assert open_entry(key, name, blob) == secret, "round-trip failed"
    # tamper: flip a ciphertext byte -> must raise
    raw = bytearray(_b64d(blob["ct"]))
    raw[0] ^= 0x01
    tampered = {"n": blob["n"], "ct": _b64e(bytes(raw))}
    try:
        open_entry(key, name, tampered)
        sys.exit("væult: TAMPER NOT DETECTED — do not trust this vault")
    except Exception:
        pass
    # rename: AAD mismatch -> must raise
    try:
        open_entry(key, "__renamed__", blob)
        sys.exit("væult: AAD binding FAILED — entry rename not detected")
    except Exception:
        pass
    print("væult: verify OK")
    print("  ✓ round-trip · ✓ tamper detected · ✓ name-binding enforced · ✓ AEAD AES-256-GCM")


# ── QR air-gap transport ──────────────────────────────────────────────────────
# The QR carries the SEALED envelope, never plaintext. QR is a transport for
# bytes that are already useless without the vault passphrase.

_QR_PREFIX = "VAEULT1:"          # lets qr-open recognise our payloads


def _qr_payload(name: str, blob: dict) -> str:
    return _QR_PREFIX + json.dumps({"name": name, "blob": blob},
                                   ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def cmd_qr(path: pathlib.Path, args: list[str]) -> None:
    """Encode ONE sealed entry as a QR PNG (no passphrase needed — it's sealed)."""
    if not args:
        sys.exit("usage: væult qr NAME [--out PATH]")
    name = args[0]
    out = None
    if "--out" in args:
        out = args[args.index("--out") + 1]
    doc = load_raw(path)
    if name not in doc["entries"]:
        sys.exit(f"væult: no entry '{name}'")
    payload = _qr_payload(name, doc["entries"][name])
    try:
        import qrcode
    except ImportError:
        sys.exit("væult: qrcode not installed (pip install qrcode pillow)")
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2)
    qr.add_data(payload)
    try:
        qr.make(fit=True)
    except Exception as e:  # noqa: BLE001
        sys.exit(f"væult: secret too large for a QR (v40 cap ~2.9KB): {e}")
    if qr.version > 40:
        sys.exit(f"væult: needs QR v{qr.version} > v40 cap — secret too large")
    img = qr.make_image(fill_color="black", back_color="white")
    dest = pathlib.Path(out) if out else path.with_suffix(".qr." + name + ".png")
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest)
    print(f"væult: sealed QR for '{name}' -> {dest}")
    print(f"  version v{qr.version} · {len(payload)} bytes · SEALED (no plaintext)")


def cmd_qr_show(path: pathlib.Path, args: list[str]) -> None:
    """Print the sealed QR payload as text (for terminal ASCII or manual transport)."""
    if not args:
        sys.exit("usage: væult qr-show NAME")
    name = args[0]
    doc = load_raw(path)
    if name not in doc["entries"]:
        sys.exit(f"væult: no entry '{name}'")
    print(_qr_payload(name, doc["entries"][name]))


def cmd_qr_open(path: pathlib.Path, args: list[str]) -> None:
    """Decode a QR PNG and import its sealed entry into this vault."""
    if not args:
        sys.exit("usage: væult qr-open IMAGE")
    img_path = pathlib.Path(args[0])
    if not img_path.exists():
        sys.exit(f"væult: no image at {img_path}")
    try:
        from pyzbar.pyzbar import decode as _zbar
        from PIL import Image
    except ImportError:
        sys.exit("væult: need pyzbar + pillow (pip install pyzbar pillow)")
    found = _zbar(Image.open(img_path))
    if not found:
        sys.exit("væult: no QR detected (pyzbar cannot read cv2/PIL mode=1 images — use this decoder)")
    data = found[0].data.decode("utf-8", errors="replace")
    if not data.startswith(_QR_PREFIX):
        sys.exit("væult: not a væult QR payload")
    payload = json.loads(data[len(_QR_PREFIX):])
    name, blob = payload["name"], payload["blob"]
    doc = load_raw(path)
    key = unlock(doc)
    # PROVE the sealed blob opens under this vault's key before storing it
    try:
        value = open_entry(key, name, blob)
    except Exception:
        sys.exit(f"væult: QR '{name}' does NOT open under this vault's passphrase "
                 f"(different vault, or tampered) — refused")
    doc["entries"][name] = blob
    doc["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    save_raw(path, doc)
    print(f"væult: imported '{name}' from QR ({len(value)} chars, verified under this key)")


CMDS = {"init": cmd_init, "set": cmd_set, "get": cmd_get, "list": cmd_list,
        "rm": cmd_rm, "export": cmd_export, "verify": cmd_verify,
        "qr": cmd_qr, "qr-show": cmd_qr_show, "qr-open": cmd_qr_open}


def main(argv: list[str]) -> None:
    if len(argv) < 2 or argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd, rest = argv[1], argv[2:]
    path = pathlib.Path(os.environ.get("VAEULT_PATH", str(DEFAULT_VAULT)))
    if cmd == "init":
        cmd_init(path, rest)
    else:
        CMDS[cmd](path, rest) if cmd in CMDS else sys.exit(f"væult: unknown command '{cmd}'")


if __name__ == "__main__":
    main(sys.argv)
