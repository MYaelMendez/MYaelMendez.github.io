#!/bin/sh
# Install the tiny-voca-voice plugin into a Hermes Agent plugins directory.
# No credentials, tokens, or network access are required.
set -eu

# Resolve the directory containing this script so install works from anywhere.
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

# Where to install: HERMES_HOME if set, otherwise $HOME/.hermes.
HERMES_HOME=${HERMES_HOME:-$HOME/.hermes}
TARGET="$HERMES_HOME/plugins/tiny-voca-voice"

# Start from a clean target directory.
rm -rf "$TARGET"
mkdir -p "$TARGET"

# Copy the plugin payload. The existence guard keeps the installer usable in a
# docs-only checkout; when the full plugin is present, every item is copied.
for item in plugin.yaml identity.json __init__.py scripts skills docs assets \
            desktop dashboard site package.json CITATION.cff \
            README.md CHANGELOG.md NOTICE.md LICENSE; do
    if [ -e "$SCRIPT_DIR/$item" ]; then
        cp -R "$SCRIPT_DIR/$item" "$TARGET/"
    fi
done

if [ ! -f "$TARGET/scripts/tiny_voca_voice.py" ]; then
    echo "warning: scripts/tiny_voca_voice.py is not present in $TARGET" >&2
fi

cat <<EOF

tiny-voca-voice 1.2.0 installed to: $TARGET

Enable native TTS (run this command):
    hermes config set tts.provider tiny-voca

Next: provision and verify onnx/model.onnx under
    \${TINY_VOCA_HOME:-\$HERMES_HOME/tiny-voca}
See docs/NATIVE_TTS.md for the exact commands.
EOF
