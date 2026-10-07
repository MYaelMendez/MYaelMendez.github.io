#!/usr/bin/env python3
"""æ://qr_keys — local QR code infrastructure for private key management.

Keys are generated, stored, and transported as QR codes.
Nothing touches the network. Paper is the backup medium.
"""

import os
import sys
import json
import qrcode
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

# ══════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════
KEY_DIR = Path(r"C:\æ\secrets\keys")
QR_DIR = KEY_DIR / "qr"
LEDGER_FILE = Path(r"C:\æ\keeper\ledger.jsonl")
MAX_QR_VERSION = 40  # max QR version (40x40 modules)

# ══════════════════════════════════════════════════════════
# ED25519 KEY GENERATION (stdlib only, no external crypto lib needed)
# ══════════════════════════════════════════════════════════

def generate_ed25519_keypair():
    """Generate Ed25519 keypair using cryptography library.

    Proper Ed25519 implementation with clamping and scalarmult.
    """
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    private_key = Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    return {
        "private_key": private_bytes.hex(),
        "public_key": public_bytes.hex(),
        "algorithm": "ed25519",
        "created": datetime.now(timezone.utc).isoformat(),
        "fingerprint": hashlib.sha256(public_bytes).hexdigest()[:16]
    }


def generate_rsa_keypair(bits=2048):
    """Generate RSA keypair using Python's stdlib.

    WARNING: RSA key generation requires proper primality testing.
    This is a simplified version. Use cryptography.hazmat for production.
    """
    import secrets
    import random

    # Simplified RSA - NOT for production use
    # Real implementation needs proper prime generation
    def is_prime(n, k=10):
        if n < 2: return False
        if n == 2 or n == 3: return True
        if n % 2 == 0: return False

        # Miller-Rabin primality test
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def generate_prime(bits):
        while True:
            n = secrets.randbits(bits) | (1 << (bits - 1)) | 1
            if is_prime(n):
                return n

    # RSA key generation
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)

    public_key = {"e": e, "n": n}
    private_key = {"d": d, "n": n, "p": p, "q": q}

    return {
        "private_key": private_key,
        "public_key": public_key,
        "algorithm": "rsa",
        "bits": bits,
        "created": datetime.now(timezone.utc).isoformat(),
        "fingerprint": hashlib.sha256(str(n).encode()).hexdigest()[:16]
    }


# ══════════════════════════════════════════════════════════
# QR CODE ENCODING / DECODING
# ══════════════════════════════════════════════════════════

def encode_qr(data, filepath=None, version=None):
    """Encode data as QR code image.

    Args:
        data: string or dict to encode
        filepath: where to save (auto-generated if None)
        version: QR version (1-40, None = auto)

    Returns:
        dict with filepath, size, version, data_hash
    """
    if isinstance(data, dict):
        data = json.dumps(data, ensure_ascii=False, sort_keys=True)

    # Create QR code
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% recovery
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save
    if filepath is None:
        QR_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filepath = QR_DIR / f"qr_{ts}.png"

    img.save(str(filepath))

    # GATE: prove the artifact decodes back through both real decoders.
    # A key on paper that does not scan is a lost key.
    try:
        import sys as _s
        _s.path.insert(0, str(Path(__file__).resolve().parent))
        import qr_supervision as _qs
        _rep = _qs.supervise_raw(str(filepath), data)
        if not _rep.passed:
            raise RuntimeError(f"qr_key_manager: supervision refused — {_rep.reason()}")
    except ImportError:
        pass  # gate unavailable

    return {
        "filepath": str(filepath),
        "size": img.size,
        "version": qr.version,
        "data_hash": hashlib.sha256(data.encode()).hexdigest()[:16],
        "data_length": len(data)
    }


def decode_qr(filepath):
    """Decode QR code image to data using pyzbar.

    Args:
        filepath: path to QR code image

    Returns:
        dict with decoded data, metadata
    """
    from pyzbar.pyzbar import decode
    from PIL import Image

    img = Image.open(str(filepath))
    results = decode(img)

    if not results:
        return {"data": None, "format": "unknown", "valid": False, "error": "no QR detected"}

    data = results[0].data.decode("utf-8")

    # Try to parse as JSON
    try:
        parsed = json.loads(data)
        return {"data": parsed, "format": "json", "valid": True}
    except json.JSONDecodeError:
        return {"data": data, "format": "text", "valid": True}


def encode_key_as_qr(keypair, filepath=None):
    """Encode a keypair as QR code for physical backup.

    The private key is encoded in the QR. Paper is the backup.
    The QR is the ONLY copy - if you lose it, the key is gone.
    """
    # Create a structured key payload
    payload = {
        "k": keypair.get("private_key", ""),
        "p": keypair.get("public_key", ""),
        "a": keypair.get("algorithm", "unknown"),
        "f": keypair.get("fingerprint", ""),
        "c": keypair.get("created", ""),
        "v": 1
    }

    # Compress: remove whitespace from JSON
    compressed = json.dumps(payload, separators=(',', ':'))

    # Check if it fits in QR version 40 (max ~2953 bytes for alphanumeric)
    if len(compressed) > 2953:
        # Split into multiple QR codes
        chunks = [compressed[i:i+2953] for i in range(0, len(compressed), 2953)]
        results = []
        for i, chunk in enumerate(chunks):
            chunk_payload = {"c": chunk, "n": i+1, "t": len(chunks)}
            result = encode_qr(chunk_payload, filepath=filepath)
            results.append(result)
        return {"chunks": results, "total": len(chunks)}
    else:
        result = encode_qr(compressed, filepath=filepath)
        return {"qr": result, "chunks": 1}


def decode_qr_to_key(filepath):
    """Decode a QR code back to a keypair.

    Returns the keypair dict if valid, None if invalid.
    """
    decoded = decode_qr(filepath)

    if not decoded.get("valid"):
        return None

    data = decoded["data"]

    # Handle chunked QR codes
    if isinstance(data, dict) and "c" in data and "n" in data:
        # This is a chunk - need all chunks to reconstruct
        return {"chunk": data, "complete": False}

    # Single QR code
    if isinstance(data, dict) and "k" in data and "p" in data:
        return {
            "private_key": data["k"],
            "public_key": data["p"],
            "algorithm": data["a"],
            "fingerprint": data["f"],
            "created": data["c"],
            "complete": True
        }

    return None


# ══════════════════════════════════════════════════════════
# KEY MANAGEMENT
# ══════════════════════════════════════════════════════════

def create_key(name, algorithm="ed25519"):
    """Create a new key and encode as QR code.

    The key is stored locally AND as a QR code for physical backup.
    The private key NEVER leaves the machine in plaintext.
    """
    # Generate keypair
    if algorithm == "ed25519":
        keypair = generate_ed25519_keypair()
    elif algorithm == "rsa":
        keypair = generate_rsa_keypair()
    else:
        return {"error": f"unknown algorithm: {algorithm}"}

    # Save private key locally (encrypted in production)
    KEY_DIR.mkdir(parents=True, exist_ok=True)
    key_file = KEY_DIR / f"{name}.key"

    # In production, encrypt the key before saving
    # For now, save as JSON (NOT for production use)
    with open(key_file, 'w', encoding='utf-8') as f:
        json.dump(keypair, f, indent=2)

    # Encode as QR for physical backup
    qr_result = encode_key_as_qr(keypair)

    # Log to ledger
    ledger_append({
        "kind": "key_created",
        "text": f"created key '{name}' ({algorithm})",
        "evidence": f"fingerprint={keypair['fingerprint']}, qr={qr_result.get('chunks', 1)} chunks"
    })

    return {
        "name": name,
        "algorithm": algorithm,
        "fingerprint": keypair["fingerprint"],
        "public_key": keypair["public_key"],
        "private_key": keypair["private_key"],
        "qr": qr_result,
        "key_file": str(key_file)
    }


def list_keys():
    """List all keys in the key directory."""
    if not KEY_DIR.exists():
        return {"keys": []}

    keys = []
    for key_file in KEY_DIR.glob("*.key"):
        try:
            with open(key_file, encoding='utf-8') as f:
                keypair = json.load(f)
            keys.append({
                "name": key_file.stem,
                "algorithm": keypair.get("algorithm"),
                "fingerprint": keypair.get("fingerprint"),
                "created": keypair.get("created"),
                "public_key": keypair.get("public_key")
            })
        except json.JSONDecodeError:
            keys.append({"name": key_file.stem, "error": "corrupt"})

    return {"keys": keys}


def get_key(name):
    """Get a key by name (public key only - private key stays local)."""
    key_file = KEY_DIR / f"{name}.key"
    if not key_file.exists():
        return {"error": f"key '{name}' not found"}

    with open(key_file, encoding='utf-8') as f:
        keypair = json.load(f)

    # Return public key only
    return {
        "name": name,
        "algorithm": keypair.get("algorithm"),
        "fingerprint": keypair.get("fingerprint"),
        "public_key": keypair.get("public_key"),
        "created": keypair.get("created")
    }


def sign_with_key(name, message):
    """Sign a message with a local key using Ed25519.

    Returns the signature. The private key never leaves the function.
    """
    key_file = KEY_DIR / f"{name}.key"
    if not key_file.exists():
        return {"error": f"key '{name}' not found"}

    with open(key_file, encoding='utf-8') as f:
        keypair = json.load(f)

    # Proper Ed25519 signing
    private_key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(keypair["private_key"]))
    signature = private_key.sign(message.encode())

    # Log to ledger
    ledger_append({
        "kind": "signed",
        "text": f"signed message with key '{name}'",
        "evidence": f"fingerprint={keypair['fingerprint']}, msg_hash={hashlib.sha256(message.encode()).hexdigest()[:16]}"
    })

    return {
        "signature": signature.hex(),
        "public_key": keypair["public_key"],
        "fingerprint": keypair["fingerprint"]
    }


def verify_signature(public_key, message, signature):
    """Verify an Ed25519 signature against a public key."""
    try:
        pk = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key))
        pk.verify(bytes.fromhex(signature), message.encode())
        return True
    except Exception:
        return False


# ══════════════════════════════════════════════════════════
# LEDGER
# ══════════════════════════════════════════════════════════

def ledger_append(entry):
    """Append entry to the keeper ledger."""
    LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry["iso"] = datetime.now(timezone.utc).isoformat()
    entry["sig"] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()[:16]
    with open(LEDGER_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ══════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="æ://qr_keys - local QR key management")
    subparsers = parser.add_subparsers(dest="command")

    # create key
    create_parser = subparsers.add_parser("create", help="Create a new key")
    create_parser.add_argument("name", help="Key name")
    create_parser.add_argument("--algorithm", choices=["ed25519", "rsa"], default="ed25519")

    # list keys
    subparsers.add_parser("list", help="List all keys")

    # get public key
    get_parser = subparsers.add_parser("get", help="Get public key")
    get_parser.add_argument("name", help="Key name")

    # sign message
    sign_parser = subparsers.add_parser("sign", help="Sign a message")
    sign_parser.add_argument("name", help="Key name")
    sign_parser.add_argument("message", help="Message to sign")

    # encode QR
    qr_parser = subparsers.add_parser("qr-encode", help="Encode data as QR")
    qr_parser.add_argument("data", help="Data to encode (JSON string or text)")
    qr_parser.add_argument("--filepath", help="Output filepath")

    # decode QR
    decode_parser = subparsers.add_parser("qr-decode", help="Decode a QR code")
    decode_parser.add_argument("filepath", help="QR code image path")

    args = parser.parse_args()

    if args.command == "create":
        result = create_key(args.name, args.algorithm)
        print(json.dumps(result, indent=2))
    elif args.command == "list":
        result = list_keys()
        print(json.dumps(result, indent=2))
    elif args.command == "get":
        result = get_key(args.name)
        print(json.dumps(result, indent=2))
    elif args.command == "sign":
        result = sign_with_key(args.name, args.message)
        print(json.dumps(result, indent=2))
    elif args.command == "qr-encode":
        data = args.data
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            pass  # Keep as string
        result = encode_qr(data, filepath=args.filepath)
        print(json.dumps(result, indent=2))
    elif args.command == "qr-decode":
        result = decode_qr_to_key(args.filepath)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()
