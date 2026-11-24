#!/bin/sh
# Install the hermes-ae plugin into a Hermes Agent plugin directory.
set -eu

# Resolve the directory containing this script so the install works from anywhere.
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

# Where to install: HERMES_HOME if set, otherwise $HOME/.hermes.
HERMES_HOME=${HERMES_HOME:-$HOME/.hermes}
TARGET="$HERMES_HOME/plugins/hermes-ae"

# Start from a clean target directory.
rm -rf "$TARGET"
mkdir -p "$TARGET"

# Copy only the plugin payload.
for item in plugin.yaml __init__.py scripts skills model docs courses webgl assets harnesses.json identity.json ae-policy.json packages videos.json receipts_snapshot.json; do
    cp -R "$SCRIPT_DIR/$item" "$TARGET/"
done

cat <<EOF

hermes-ae installed to: $TARGET

Enable the plugin:
    hermes config set plugins.enabled '[hermes-ae]'

Verify the installation:
    hermes plugins doctor hermes-ae
EOF
