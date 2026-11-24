#!/usr/bin/env python3
"""Asimov build manifest + kaizen receipt loop.

Usage:
  python3 scripts/asimov_kaizen.py build
  echo '{"result":"PASS", ...}' | python3 scripts/asimov_kaizen.py review
  python3 scripts/asimov_kaizen.py status
"""
import hashlib, json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "asimov-build.json"
LOG = ROOT / "asimov-kaizen.jsonl"
PAGE = "asimov-head-lab.html"
CANONICAL = "https://myaelmendez.github.io/" + PAGE
ASSETS = [
    PAGE,
    "assets/gltf/asimov-web.glb",
    "assets/vendor/three.module.js",
    "assets/vendor/GLTFLoader.js",
    "ffmpeg-asimov/asimov_1_25dof.urdf",
    "ffmpeg-asimov/asimov_1_25dof.xml",
]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def build():
    missing = [p for p in ASSETS if not (ROOT / p).exists()]
    if missing:
        raise SystemExit("missing assets: " + ", ".join(missing))
    payload = {
        "schema": "asimov-build/1.0",
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "authority": "HUMAN://ROOT → æ → ae → RECEIPT",
        "page": CANONICAL,
        "head": {"mesh": "neck_pitch_link", "source": "menloresearch/asimov-1"},
        "shell": {"color": "#ff6a00", "emissive": "#ff3d00"},
        "mask": {"matrix": "32x28", "kind": "LED canvas texture", "tablet": False},
        "assets": {p: sha256_file(ROOT / p) for p in ASSETS},
    }
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["hash"] = hashlib.sha256(body).hexdigest()
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["hash"])
    return payload

def last_hash():
    if not LOG.exists():
        return None
    for line in reversed(LOG.read_text().splitlines()):
        try:
            return json.loads(line).get("hash")
        except Exception:
            pass
    return None

def review():
    rec = json.loads(sys.stdin.read())
    rec["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rec["prev"] = last_hash()
    body = json.dumps(rec, sort_keys=True, separators=(",", ":")).encode()
    rec["hash"] = hashlib.sha256(body).hexdigest()
    with LOG.open("a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    print(rec["hash"])

def status():
    if not LOG.exists():
        print("no reviews")
        return
    lines = LOG.read_text().splitlines()
    last = json.loads(lines[-1])
    print(json.dumps({k: last.get(k) for k in ("ts", "result", "page", "shell", "hash")}, indent=2))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    {"build": build, "review": review, "status": status}[cmd]()
