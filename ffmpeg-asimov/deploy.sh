#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ARTIFACT_DIR="${ARTIFACT_DIR:-$HERE/assets}"
PAGES_DIR="${PAGES_DIR:?set PAGES_DIR to the .github.io checkout}"
VERSION="$(python3 -c "import json;print(json.load(open('$HERE/manifest.json'))['version'])")"
TARGET="$PAGES_DIR/ffmpeg-asimov"
mkdir -p "$TARGET"
cp "$ARTIFACT_DIR"/* "$TARGET/"
cd "$PAGES_DIR"
git add ffmpeg-asimov
git commit -m "Deploy menlo-asimov-ffmpeg ${VERSION}" || true
git push origin "${BRANCH:-gh-pages}"
echo "https://myaelmendez.github.io/ffmpeg-asimov/menlo-asimov-ffmpeg-916.mp4"
