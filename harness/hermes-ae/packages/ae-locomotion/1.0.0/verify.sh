#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
sha256sum -c checksums.sha256
python3 - <<'PY'
import json
m=json.load(open('manifest.json'))
assert m['name']=='æLOCOMOTION'
assert m['authority']=='HUMAN://ROOT'
assert m['verified']['success'] is True
print('manifest OK:',m['slug'],m['version'],m['verified']['base_x_m'],'m')
PY
