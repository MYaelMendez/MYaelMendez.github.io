# Mapping OpenSourceWare to the official Menlo Asimov SDK

## Official source

The official SDK repository is `menloresearch/menlo-sdk` — “Python SDK for Menlo robots. Supports Asimov 1,” Apache-2.0, Python 3.12+.[7][8] The import is `menlo`; the Asimov wire lives in `menlo.asimov`, and one `Robot` works across every transport.[10]

The SDK is a **client of Asimov Edge**: it drives the robot through the edge's arbiter and safety layer, never as a bypass.[10] The Drive Robot page and a paired gamepad outrank it.[8] Our æ policy layer belongs **above** this boundary, not inside it.

## Layer map

| Menlo official layer | OpenSourceWare layer | Relationship |
|---|---|---|
| `asimov-1` mechanical CAD, MJCF, URDF[3] | `packages/asimov-twin/1.0.0/asimov-avatar.usda` | Hash-bound projection of official source, not a replacement body |
| `menlo-sdk` / `menlo.asimov.Robot`[7][10] | `hermes-ae` `robot` harness | We wrap calls in authority checks + receipts; SDK remains the device client |
| SDK verbs: `damp`, `stand`, `balance`, `set_velocity`, `trajectory`, `set_joints`[10] | future `ae({op:"sdk", ...})` verbs | One governed `ae` call per SDK verb, with `POLICY://EVALUATE` first |
| SDK facts: `get_state()`, `Sent`, `Outcome`, faults, alerts, battery[10] | `ae` receipt detail | State is the truth about effect; hash before/after state into the receipt |
| `udp` / `hybrid` / `livekit` transports[13] | deployment profiles | `livekit` for Internet-of-Agents remote control; `hybrid` for lab LAN + media; `udp` only on a trusted network |
| Camera, microphone, speaker via LiveKit tracks[8][13] | `viewport`, `tiny-voca`, `face` harnesses | Media is projected into the 9:16 viewport or played through the robot speaker |
| Digital Asimov browser twin[12] | Asimov Viewport + USD qpos replay | Menlo's official sandbox; our public projection layer adds DOM awareness and receipts |

## Existing local bridge

We already follow the official speaker contract. `plugins/hermes-asimov/sdk_play.py` mirrors `examples/play_audio.py`:

```text
tiny-voca WAV (16-bit PCM)
→ menlo.asimov.Robot().connect(require_state=False)
→ robot.has("speaker")
→ robot.speaker.play_pcm(pcm, sample_rate_hz, channels) in 1 s chunks
```

The official docs describe the same 16-bit PCM `play_pcm` contract and 1-second chunk pattern.[8] In local mode we render the WAV only; SDK mode is explicit and never contacts a robot unless a robot is configured.

## Authority flow

```text
HUMAN://ROOT
→ æ Policy evaluates proposal
→ DAO Brain sets face state
→ privateclient.ai approval
→ ae router selects harness
→ menlo-sdk Robot verb
→ Asimov Edge safety layer
→ robot state / Outcome
→ SDK://VERB receipt
```

Important: the SDK already reports facts and leaves safety in firmware/Edge and guards in user code.[10] OpenSourceWare is that **user-side guard and receipt layer**. We do not replace Edge safety; we govern what is allowed to ask it.

## Deployment mapping

| Environment | SDK mode | Our surface |
|---|---|---|
| Trusted robot LAN, control only | `udp` | local C2, no camera/audio; one state client |
| Lab LAN with media | `hybrid` | face script, qpos viewport, tiny-voca speaker |
| Remote / Internet of Agents | `livekit` | phone teleprompter, Asimov Viewport, agentic ecommerce drafts |

`udp` has no sign-in, so trust the network before enabling it; `hybrid` keeps commands on UDP and media on LiveKit; `livekit` carries everything through the room.[13]

## Honest boundary

- We map to the SDK as a **governance and orchestration layer**, not as a forked SDK.
- We currently bridge **speaker/media**, not the full motion verb surface.
- Motion verbs should only be added behind `POLICY://EVALUATE`, human approval or deadman, and a receipt that records `get_state()` / `Outcome`.
- The official SDK reports facts; it is not an emergency stop.[8] Physical E-Stop and Edge safety remain authoritative for motion.

## Next build

Implemented as `ae({op:"verbs"})`: `status`, `state`, `stand`, `balance`,
`walk` via `set_velocity`, `damp`, `play_pcm`, and the other official verbs,
all behind æ Policy and `SDK://VERB` receipts.

## Sources

[3] https://github.com/menloresearch/asimov-1 — Asimov 1 open-source humanoid repository
[7] https://github.com/menloresearch/menlo-sdk — menlo-sdk repository
[8] https://docs.menlo.ai/asimov/1/program/sdk — Python SDK documentation
[10] https://github.com/menloresearch/menlo-sdk/blob/main/AGENTS.md — menlo-sdk AGENTS.md
[12] https://docs.menlo.ai/asimov/digital-asimov — Digital Asimov overview
[13] https://docs.menlo.ai/sdk/connection-modes — SDK connection modes
