# æ Robot Verbs

`æ Robot Verbs` are governed wrappers over the official Menlo SDK surface. They do **not** invent wire synonyms: the motion names are Menlo's own verbs, and media calls use the official `Robot.camera`, `Robot.microphone`, and `Robot.speaker` objects.[10]

```text
HUMAN://ROOT → æ Policy → ae({op:"verbs"}) → menlo.asimov.Robot → receipt
```

## Canonical set

| æ verb | Official call | Class | Gate |
|---|---|---|---|
| `status` | SDK version / saved-robot presence | read | allow |
| `state` / `get_state` | `Robot.get_state()` | read | allow |
| `check` | state facts only, sends nothing | read | allow |
| `stand` | `Robot.stand()` | motion | approval or deadman |
| `damp` | `Robot.damp()` | motion | approval or deadman |
| `balance` | `Robot.balance()` | motion | approval or deadman |
| `set_velocity` | `Robot.set_velocity()` | motion | approval or deadman |
| `trajectory` | `Robot.trajectory()` | motion | approval or deadman |
| `set_joints` | `Robot.set_joints()` | motion | approval or deadman |
| `photo` | `Robot.camera.photo()` | media | allow + receipt |
| `capture_clip` | `Robot.camera.capture_clip()` | media | allow + receipt |
| `record_audio` | `Robot.microphone.chunks()` | media | allow + receipt |
| `play_pcm` | `Robot.speaker.play_pcm()` | media | allow + receipt |

`stand`, `damp`, `set_velocity`, and `trajectory` are wire verbs; `balance` and `set_joints` are official SDK additions.[10] The SDK reports facts rather than applying state-based refusals; guards belong in user code.[10] æ Policy is that guard.

## Ops

```json
ae({"op":"verbs","action":"list"})
ae({"op":"verbs","action":"plan","verb":"stand"})
ae({"op":"verbs","action":"plan","verb":"stand","approval":{"human":true,"expires_at":"2030-01-01T00:00:00Z"}})
ae({"op":"verbs","action":"execute","verb":"status"})
```

`plan` is the default safe path: it evaluates policy, hashes arguments, and returns the exact SDK call without connecting. `execute` stays dry-run unless `HERMES_AE_SDK_LIVE=1`; even then, motion verbs require a bound human approval or an armed deadman.

## Receipts

| Decision | Action |
|---|---|
| allowed plan | `SDK://VERB_PLAN` |
| denied | `SDK://VERB_DENIED` |
| live success | `SDK://VERB` |
| live error | `SDK://VERB_ERROR` |

Each receipt records `verb`, `official` call, `args_sha256`, `policy_sha256`, `sdk_version`, and actor. Motion receipts include post-state where available.

## Transport mapping

| Deployment | SDK mode | Use |
|---|---|---|
| trusted robot LAN, control only | `udp` | no media, one state client |
| lab LAN with camera/audio | `hybrid` | UDP commands, LiveKit media |
| remote / Internet of Agents | `livekit` | everything through the robot room |

`udp` carries no sign-in; trust the network before enabling it. `hybrid` keeps commands local while media crosses LiveKit; `livekit` carries commands and state through the room.[13]

## Authority rule

The SDK is a client of Asimov Edge and its safety layer, never a bypass.[10] The official docs also say nothing in the SDK is an emergency stop.[8] æ Robot Verbs therefore add governance, not physical safety: the E-Stop, Edge arbiter, and firmware remain authoritative for motion.

## Sources

[8] https://docs.menlo.ai/asimov/1/program/sdk — Python SDK documentation
[10] https://github.com/menloresearch/menlo-sdk/blob/main/AGENTS.md — menlo-sdk AGENTS.md
[13] https://docs.menlo.ai/sdk/connection-modes — SDK connection modes
