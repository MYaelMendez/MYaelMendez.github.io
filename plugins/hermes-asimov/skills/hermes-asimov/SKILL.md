---
name: hermes-asimov
description: Hermes-Asimov robot actor and spokesrobot — official Asimov-1 25-DOF model assembled, tiny-voca voice wired to the menlo-sdk speaker path.
---

# hermes-asimov

The robot actor / spokesrobot. Assembled from `menloresearch/asimov-1` `sim-model/asimov_1_25dof` (URDF + MJCF + 26 STL meshes, 26 links / 25 revolute joints; SHA256 URDF `0cd39d5f…f7a6`, MJCF `5d11a900…81c`). License CERN-OHL-S-2.0.

## Tools

- `asimov_status` — assembled model, meshes, speaker contract, voice
- `asimov_say({text, voice?, output?, mode?})` — tiny-voca WAV; `mode=local` (default) renders locally, `mode=sdk` plays via `menlo-sdk` `Robot.speaker.play_pcm` on a configured robot (hybrid/livekit)
- `asimov_voice_video({text?, output?})` — 9:16 spokesrobot clip with CAD viewport + tiny-voca narration
- `asimov_receipts({limit?})` — HUMAN://ROOT receipt log

## Voice path

`tiny_voca_voice.speak_text` → 16-bit PCM WAV → `menlo.asimov.Robot().connect(require_state=False)` → `robot.speaker.play_pcm(pcm, sample_rate_hz, channels)` in 1 s chunks. SDK example: `/opt/data/hermes-asimov/sdk/examples/play_audio.py`. No robot is contacted unless `mode=sdk` and a robot is configured via `menlo setup`.

## Files

Model: `/opt/data/hermes-asimov/model` · SDK examples: `/opt/data/hermes-asimov/sdk/examples` · Plugin: `/opt/data/plugins/hermes-asimov`.

Receipts: `$HERMES_HOME/hermes-asimov-receipts.jsonl`.

## Limits

Local mode renders audio only — it does not play on hardware. SDK mode requires a paired Asimov over hybrid/livekit; UDP carries no audio. The MuJoCo harness in this install is a receipted kinematic harness (real MuJoCo dynamics not installed); the CAD viewport is Three.js.
