#!/usr/bin/env bash
# deploy_droplet.sh — bake live droplet-system status into droplet.html, push to github.io.
# Part of the github-pages point-of-truth loop (deploy -> ingest -> cortex).
set -uo pipefail

DROPLET_IP="129.212.180.252"
PAGE="droplet.html"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

probe() { curl -s --max-time 25 "$1" 2>/dev/null; }

# 1) droplet own node (:3000)
DROPLET_JSON="$(probe "http://${DROPLET_IP}:3000/xrpc/ae.vps.rtx?op=status")"
# 2) droplet -> victus via tunnel (:3050)
TUNNEL_JSON="$(ssh -o BatchMode=yes -o ConnectTimeout=8 root@${DROPLET_IP} \
  "curl -s --max-time 20 'http://127.0.0.1:3050/xrpc/ae.vps.rtx?op=probe'" 2>/dev/null)"
# 3) victus local (:3050)
VICTUS_JSON="$(probe "http://127.0.0.1:3050/xrpc/ae.vps.rtx?op=probe")"

if [ -n "$TUNNEL_JSON" ]; then
  BADGE='<span class="badge up">LIVE &mdash; droplet reaches Victus RTX</span>'
  TUNNEL_LINE='reverse tunnel UP &middot; droplet:3050 &rarr; victus:3050'
  GPU_NAME="$(printf '%s' "$TUNNEL_JSON" | python -c 'import sys,json;print(json.load(sys.stdin)["probe"]["name"])' 2>/dev/null || echo 'RTX 3050')"
  GPU_MEM="$(printf '%s' "$TUNNEL_JSON" | python -c 'import sys,json;print(json.load(sys.stdin)["probe"]["memory_total_mib"])' 2>/dev/null || echo '6144')"
  GPU_LINE="$GPU_NAME &middot; ${GPU_MEM} MiB"
else
  BADGE='<span class="badge down">DOWN &mdash; tunnel not forwarding (run: bash rtx-bridge.sh up)</span>'
  TUNNEL_LINE='reverse tunnel DOWN &mdash; see "bring it live" below'
  GPU_LINE='unreachable via tunnel'
fi

[ -n "$DROPLET_JSON" ] && DROPLET_LINE='vps_node UP &middot; PDS + broker serving' || DROPLET_LINE='vps_node not responding'
[ -n "$VICTUS_JSON" ] && VICTUS_LINE='vps_node UP &middot; GPU-backed' || VICTUS_LINE='vps_node not running (bash rtx-bridge.sh up)'

# inject via env vars (avoids shell-quoting the JSON)
BADGE="$BADGE" TS="$TS" DROPLET_LINE="$DROPLET_LINE" VICTUS_LINE="$VICTUS_LINE" \
TUNNEL_LINE="$TUNNEL_LINE" GPU_LINE="$GPU_LINE" PAGE="$PAGE" python - <<'PY'
import os
p = os.environ["PAGE"]
s = open(p, encoding="utf-8").read()
s = s.replace("__STATUS_BADGE__", os.environ["BADGE"])
s = s.replace("__STATUS_TS__", os.environ["TS"])
s = s.replace("__DROPLET_LINE__", os.environ["DROPLET_LINE"])
s = s.replace("__VICTUS_LINE__", os.environ["VICTUS_LINE"])
s = s.replace("__TUNNEL_LINE__", os.environ["TUNNEL_LINE"])
s = s.replace("__GPU_LINE__", os.environ["GPU_LINE"])
open(p, "w", encoding="utf-8").write(s)
print("baked:", "LIVE" if "LIVE" in os.environ["BADGE"] else "DOWN")
PY

cd "$(dirname "$0")"
git add "$PAGE"
git commit -m "droplet.html: re-bake live status @ $TS"
git push origin gh-pages
echo "pushed -> https://MYaelMendez.github.io/droplet.html"
