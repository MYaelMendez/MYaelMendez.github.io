#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
POLICY_DIR="${HERMES_AE_POLICY_DIR:-$HOME/.hermes/asimov-policy}"
PLUGIN_SCRIPTS="${HERMES_AE_SCRIPTS_DIR:-$HOME/.hermes/plugins/hermes-ae/scripts}"
mkdir -p "$POLICY_DIR" "$PLUGIN_SCRIPTS"
cp "$HERE"/policy/policy.onnx "$HERE"/policy/env.yaml "$HERE"/policy/agent.yaml "$POLICY_DIR/"
cp "$HERE"/scripts/*.py "$PLUGIN_SCRIPTS/"
echo "installed ae-locomotion into $POLICY_DIR and $PLUGIN_SCRIPTS"
