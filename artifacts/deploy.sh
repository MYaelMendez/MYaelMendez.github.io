#!/usr/bin/env bash
# deploy.sh — one-command deploy for Hermes artifact zips
# Usage: ARTIFACT_DIR=. ./deploy.sh
set -euo pipefail

ARTIFACT_DIR="${ARTIFACT_DIR:-.}"
MANIFEST="$ARTIFACT_DIR/manifest.json"

if [ ! -f "$MANIFEST" ]; then
  echo "ERROR: manifest.json not found in $ARTIFACT_DIR" >&2
  exit 1
fi

REPO=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['repo'])")
BRANCH=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['branch'])")
PAGES_PATH=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['pages_path'])")
ARTIFACT=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['artifact'])")
VERSION=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['version'])")
PAGES_DIR=$(dirname "$PAGES_PATH")

echo "━━━ Deploying $ARTIFACT $VERSION to $REPO:$BRANCH ━━━"

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

git clone --depth 1 --branch "$BRANCH" "https://github.com/$REPO.git" "$TMPDIR/repo" 2>/dev/null || {
  echo "Branch $BRANCH not found, cloning default..." >&2
  git clone --depth 1 "https://github.com/$REPO.git" "$TMPDIR/repo"
}

cd "$TMPDIR/repo"
mkdir -p "$PAGES_DIR"

# Copy files from manifest
python3 -c "
import json, shutil, sys
m = json.load(open('$MANIFEST'))
for f in m.get('files', []):
    src = '$ARTIFACT_DIR/' + f['path']
    dst = f['path']
    if f.get('role') == 'manifest':
        continue
    shutil.copy2(src, dst)
    print(f'  copied {f[\"path\"]}')
"

git add -A
git commit -m "Deploy $ARTIFACT $VERSION" || echo "Nothing to commit"
git push origin "$BRANCH"

echo "━━━ Deployed ━━━"
echo "Live: https://$(echo $REPO | cut -d/ -f1).github.io/$(echo $REPO | cut -d/ -f2)/${PAGES_DIR%/}/"
