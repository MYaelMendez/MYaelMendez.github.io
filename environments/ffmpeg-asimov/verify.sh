#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
BASE_URL="${BASE_URL:-https://raw.githubusercontent.com/MYaelMendez/MYaelMendez.github.io/gh-pages/ffmpeg-asimov}"
python3 - "$HERE" "$BASE_URL" <<'PYVERIFY'
import hashlib, json, sys, time, urllib.request
from pathlib import Path
here, base = Path(sys.argv[1]), sys.argv[2].rstrip('/')
m = json.loads((here/'manifest.json').read_text())
ok = True
for f in m['files']:
    want = f['sha256']; got = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(f'{base}/{f["path"]}', timeout=30) as r:
                got = hashlib.sha256(r.read()).hexdigest()
            break
        except Exception:
            time.sleep(2 * (attempt + 1))
    status = 'OK' if got == want else 'FAIL'
    print(f'{status} {f["path"]}')
    ok = ok and got == want
print('VERIFY', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
PYVERIFY
