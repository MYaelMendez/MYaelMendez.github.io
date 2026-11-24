# tinyVOICE

`tinyVOICE` is the umbrella local voice layer for OpenSourceWare. It keeps
`tiny-voca-voice` as the stable package id while adding a second optional
provider: VoxMel.

The thesis:

> One-person company, many voices, one human root.

## Providers

| Provider | Runtime | Voices | Languages | Cloning | Status |
|---|---|---|---|---|---|
| `tiny-voca` | tiny-voca ONNX / CPU | `F2`, `M2` | English | no | shipped |
| `voxmel` | VoxMel + Vocos | `SOVÆREIGN` | English, Chinese | yes | requires local model, Vocos weights, reference audio, and consent |

VoxMel is the native Chinese voice path for the one-person company movement.
The human digital-twin voice is `SOVÆREIGN`: a consent-gated clone of the human
principal's voice, never an authority source.

## Identity

| Voice | Compute layer | Principal | Meaning |
|---|---|---|---|
| `F2` · nous girl | `human-intent` | `HUMAN://ROOT` | root intent; source timbre for robot voice |
| `M2` · hermes-agent | `agent-runtime` | `agent` | build and narration voice |
| `ROBOT` · asimov-robot | `robot-body` | `robot` | F2 source through the Menlo Asimov speaker |
| `SOVÆREIGN` · soværeign voice | `human-twin` | `HUMAN://ROOT` | human-approved VoxMel clone, English and Chinese |

## Governance

Voice cloning is a side effect on identity. It requires:

```text
HUMAN://ROOT → explicit consent → VOICE://BIND → VOICE://SPEAK → RECEIPT
```

A `VOICE://BIND` receipt records the SHA-256 of the reference audio, exact
transcript, and consent file. The agent may not bind a voice without that
receipt. `SOVÆREIGN` speaks with authority derived only from the human; it is
the digital twin, not the root.

## CLI

```sh
python3 scripts/tiny_voice.py --op list
python3 scripts/tiny_voice.py --op go
python3 scripts/tiny_voice.py --op bind \
  --voice SOVÆREIGN \
  --prompt-audio reference.wav \
  --prompt-text transcript.txt \
  --consent consent.txt
python3 scripts/tiny_voice.py --op speak \
  --provider tiny-voca --voice M2 --text "Receipts on every action." --output out.wav
python3 scripts/tiny_voice.py --op speak \
  --provider voxmel --voice SOVÆREIGN --language zh \
  --text "一人公司，权威不转移。" --output out.wav
```

## VoxMel environment

The VoxMel adapter is fail-closed. Set these before using the `voxmel` provider:

- `VOXMEL_REPO` — path to a local Vox checkout.
- `VOXMEL_MODEL_DIR` — directory with `config.yaml` and checkpoint.
- `VOXMEL_VOCOS_DIR` — Vocos model directory.
- `VOXMEL_TOKENIZER_PATH` — Qwen tokenizer path.
- `VOXMEL_PROMPT_AUDIO`, `VOXMEL_PROMPT_TEXT` — reference pair.
- `VOXMEL_CONSENT` — explicit consent file containing `HUMAN://ROOT` and consent.
- Optional: `VOXMEL_CHECKPOINT`, `VOXMEL_DEVICE`, `VOXMEL_SEED`,
  `VOXMEL_CFG_TEXT`, `VOXMEL_CFG_SPK`, `VOXMEL_UP_STEPS`.

No weights are vendored. The adapter refuses to run if any required path is
missing. `examples/tiny-voice/` contains consent, transcript, and Chinese script
templates.

## Default timbre

The bound `SOVÆREIGN` reference has three signal-derived timbre variants. The
default for the human digital twin is **broadcast** — warm, compressed, and
clear for public narration. `low` and `bright` remain alternates. This is a
timbre selection over the bound reference, not a VoxMel-generated clone.

## Voice Lab

Use the consent-gated Voice Lab to bind a human-approved clone to `SOVÆREIGN`
and prepare the Chinese one-person-company ad. See `docs/VOICE_LAB.md`.

## Upstream

VoxMel: https://github.com/MYaelMendez/Vox — Apache-2.0. Thank you to VoxDance
Lab and contributors for the open model and technical report.

`HUMAN://ROOT → æ → RECEIPT`

#opensourceware #internetofagents
