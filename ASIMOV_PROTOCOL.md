# asimov:// — the OpenSourceWare command-and-control protocol

`asimov://` is a governed address layer over the official Menlo SDK. It invents
no wire synonyms: every motion name is Menlo's own verb. It adds the two things
the SDK deliberately leaves to user code — **an authority gate and a receipt** —
and one transport the SDK does not ship: **`sim`**.

```text
HUMAN://ROOT → æ POLICY → asimov:// → menlo.asimov.Robot → RECEIPT
```

- Engine: `agents/asimov_protocol.py`
- Wraps: `ae_verbs.py` (verbs), `ae_policy.py` (rules), `daobrain.py` (deliberation)
- Protocol: `asimov-protocol/1`
- Authority: `HUMAN://ROOT`
- Ledger: `$HERMES_HOME/asimov-protocol.jsonl`

## Routes

| Address | Class | Gate | Effect |
|---|---|---|---|
| `asimov://` | read | allow | protocol status, transports, verb count |
| `asimov://status` | read | allow | SDK version, robot presence, live flag |
| `asimov://verbs` | read | allow | the canonical verb set (14) |
| `asimov://state` | read | allow | `Robot.get_state()` |
| `asimov://plan <verb>` | any | policy | exact SDK call, **never connects** |
| `asimov://exec <verb>` | any | policy | dry-run unless `HERMES_AE_SDK_LIVE=1` |
| `asimov://sim <verb>` | any | policy | plan against the simulation transport |
| `asimov://grant <verb>` | meta | — | reports the approval shape; **grants nothing** |

Unknown route or unknown verb → `{"success": false, "refused": true, ...}`.
Fail closed. No silent fall-through.

## Transports

The SDK ships three. All require hardware. The fourth is ours.

| Mode | Official | Requires | Media |
|---|---|---|---|
| `udp` | yes | robot on a trusted LAN | no |
| `hybrid` | yes | robot + LiveKit | yes |
| `livekit` | yes | robot + room | yes |
| **`sim`** | **no — OSW** | **a laptop (MuJoCo)** | yes |

`sim` exists so the *same* C2 code path — same verbs, same gates, same receipts —
runs where no robot exists. `Robot(source: ConnectionConfig | Transport)` accepts
a custom transport; `SimTransport` implements the official interface
(`open · close · send · play_audio · subscribe_state · subscribe_frames ·
subscribe_outcome · subscribe_audio · subscribe_controller_change`) against
MuJoCo instead of a socket. We implement their protocol; we do not fork their SDK.

**Status: `sim` is specified and routed, not yet implemented.** `asimov://sim`
returns a policy-evaluated plan and says so plainly.

## Verb classes

| Class | Verbs | Gate |
|---|---|---|
| read | `status` `state` `get_state` `check` | allow + receipt |
| media | `photo` `capture_clip` `record_audio` `play_pcm` | allow + receipt |
| motion | `stand` `damp` `balance` `set_velocity` `trajectory` `set_joints` | **approval or armed deadman** |

Motion names are Menlo's wire verbs. `balance` and `set_joints` are official SDK
additions. Nothing here renames them.

## Measured behaviour

Run on Victus (i5-13420H, RTX 3050), `menlo-sdk 0.1.0`, no robot configured:

```text
asimov://                 success  verb_count=14
asimov://plan stand       require_approval  ACT-001  allowed=false  executed=false
                          official=Robot.stand()
asimov://plan state       allow  allowed=true  official=Robot.get_state()
asimov://sim stand        require_approval  ACT-001  transport=sim
asimov://plan launch      REFUSED  unknown verb
asimov://bogus            REFUSED  unknown route
asimov://grant stand      grants=false
```

Receipts: `ASIMOV://PLAN`, `ASIMOV://EXEC`. Hash-chained, genesis `0×64`,
chain verified.

## Authority boundary

```text
address ≠ permission
policy allow ≠ human approval
plan ≠ execution
sim ≠ hardware
```

`asimov://grant` reports the required approval shape and **never grants**.
Only `HUMAN://ROOT` signs, bound to an action hash and an expiry. Motion
additionally accepts an armed deadman.

The SDK is a client of Asimov Edge and its safety layer, never a bypass.
Nothing in the SDK is an emergency stop. This protocol adds governance, not
physical safety: the E-Stop, Edge arbiter, and firmware remain authoritative
for motion.

## What is not done

- `SimTransport` is specified, not implemented.
- No physical Asimov has been driven. Every result above is a plan or a refusal.
- `æ://` symbol binding is not wired: `🤖 -> stand` does not yet resolve to
  `asimov://plan stand`. That wire is the next link.

## Sources

- https://github.com/menloresearch/menlo-sdk — official SDK (Apache-2.0)
- https://docs.menlo.ai/asimov/1/program/sdk — SDK documentation
- https://docs.menlo.ai/sdk/connection-modes — connection modes
- `AE_ROBOT_VERBS.md`, `AE_POLICY.md`, `MENLO_SDK_MAPPING.md`, `DAO_BRAIN.md`
