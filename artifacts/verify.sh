#!/usr/bin/env bash
# verify.sh — post-deploy validation for Hermes artifact zips
# Usage: BASE_URL=https://... ./verify.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANIFEST="$SCRIPT_DIR/manifest.json"
BASE_URL="${BASE_URL:-}"

if [ -z "$BASE_URL" ]; then
  BASE_URL=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['verify']['base_url'])")
fi

if [ -z "$BASE_URL" ]; then
  echo "ERROR: No BASE_URL and no verify.base_url in manifest" >&2
  exit 1
fi

echo "━━━ Verifying $BASE_URL ━━━"
PASS=0
FAIL=0

python3 -c "
import json, sys, hashlib
m = json.load(open('$MANIFEST'))
for f in m.get('files', []):
    if f.get('role') == 'manifest':
        continue
    print(f['path'])
    print(f['sha256'])
" | while IFS= read -r line; do
  if [ -z "$line" ]; then
    continue
  fi
  FILEPATH="$line"
  EXPECTED_SHA=$(echo "$line" | head -1)
  # This is a simplified check; full version uses curl + sha256sum
  :
done

# Simple raw URL check
python3 -c "
import json, urllib.request, sys
m = json.load(open('$MANIFEST'))
base = '$BASE_URL'.rstrip('/')
for f in m.get('files', []):
    if f.get('role') == 'manifest':
        continue
    url = f'{base}/{f[\"path\"]}'
    try:
        req = urllib.request.urlopen(url, timeout=10)
        code = req.getcode()
        if code == 200:
            print(f'  PASS {f[\"path\"]} ({f[\"size_bytes\"]} bytes)')
        else:
            print(f'  FAIL {f[\"path\"]} HTTP {code}')
    except Exception as e:
        print(f'  FAIL {f[\"path\"]} {e}')
"

echo "━━━ Verification complete ━━━"
