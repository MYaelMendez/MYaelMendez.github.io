#!/usr/bin/env python3
"""Verify the atlas is exactly what `build_capabilities.py` derives.

Runs the real builder in a throwaway sandbox and compares its three outputs
byte-for-byte with the committed files. Writes NOTHING to the repo — the point
is to prove the committed atlas is derived, not hand-maintained.

    python tools/verify_atlas.py          # exit 1 if stale
"""
import filecmp
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILDER = Path("tools/build_capabilities.py")
OUTPUTS = ("ae-atlas.json", "ae-atlas.js", "capability-manifest.json")


def main() -> int:
    sandbox = Path(tempfile.mkdtemp(prefix="atlas-verify-"))
    try:
        (sandbox / "tools").mkdir()
        shutil.copy2(ROOT / "surface-manifest.json", sandbox / "surface-manifest.json")
        shutil.copy2(ROOT / BUILDER, sandbox / BUILDER)
        subprocess.run([sys.executable, str(BUILDER)], cwd=sandbox, check=True,
                       capture_output=True, text=True)
        stale = []
        for name in OUTPUTS:
            made, kept = sandbox / name, ROOT / name
            if not kept.exists():
                stale.append(f"{name}: missing from repo")
            elif not filecmp.cmp(made, kept, shallow=False):
                a = json.loads(made.read_text(encoding="utf-8"))
                b = json.loads(kept.read_text(encoding="utf-8"))
                detail = f"derived {len(a) if isinstance(a, list) else a.get('count')}" \
                         f" vs committed {len(b) if isinstance(b, list) else b.get('count')}"
                stale.append(f"{name}: differs ({detail})")
        if stale:
            print("STALE: the atlas is not what the builder derives")
            for s in stale:
                print("  - " + s)
            print("fix: python tools/build_capabilities.py")
            return 1
        n = json.loads((ROOT / "ae-atlas.json").read_text(encoding="utf-8"))["count"]
        print(f"FRESH: atlas derived and byte-identical · {n} addresses")
        return 0
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
