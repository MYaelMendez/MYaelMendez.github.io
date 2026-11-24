# æLOCOMOTION

Policy-driven Asimov-1 gait harness. One package, one authority chain.

```text
HUMAN://ROOT → ae → ONNX policy → MuJoCo → receipt
```

## What is in the box

- `policy/` — ONNX checkpoint, `env.yaml`, `agent.yaml`, source README, provision manifest
- `model/` — pinned MJCF base, visual, and physics-only variants with 23 policy actuators
- `scripts/` — policy loop, video renderer, and publish pipeline
- `docs/POLICY_LOCOMOTION.md` — contract and verification record
- `proof.json` — the verified 12-second run

## Install

```bash
HERMES_AE_POLICY_DIR="$HOME/.hermes/asimov-policy" ./install.sh
./verify.sh
```

## Run

```bash
ae({"op":"policy_locomotion","duration":12,"vx":0.4})
ae({"op":"policy_walk","publish":true})
```

## Verified

12 s · 600 policy ticks · 2400 MuJoCo steps · +4.1868 m base travel · no fall.

## Limit

Simulation only. The exact policy-viewer inference contract is reproduced;
training-time noise and gain randomizations are not.
