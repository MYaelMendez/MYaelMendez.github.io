# Removable Asimov Face

The 1:1 face is an **optional presence tablet**, not the agent's brain and not the authority root.

```text
HUMAN://ROOT → æ → Asimov Agent → [tablet | voice | teleop] → RECEIPT
```

Removing the tablet only removes high-pixel presence. The agent, voice, body model, receipts, and authority chain remain intact.

## Modes

| Mode | Trigger | Behavior |
|---|---|---|
| `tablet` | face attached | full 1:1 face, visemes, viewport projection |
| `voice` | face detached | tiny-voca replies; wake/STT supplied by Android MCP phone |
| `teleop` | Pi500 keyboard | key commands move joints / stop / toggle face |

Priority: `tablet` is presentational; `voice` is the default fallback; `teleop` is an explicit operator override.

## State

State lives at `$HERMES_HOME/ae/asimov-face.json` (override with `HERMES_AE_FACE_STATE`).

```json
{
  "authority": "HUMAN://ROOT",
  "tablet_present": false,
  "mode": "voice",
  "voice": "M2",
  "wake_source": "android-mcp",
  "teleop": {"enabled": false, "deadman": false, "last_key": null}
}
```

## Ops

```json
ae({"op":"face","action":"status"})
ae({"op":"face","action":"detach","mode":"voice"})
ae({"op":"face","action":"voice","text":"Asimov online. Awaiting authorization.","voice":"M2"})
ae({"op":"face","action":"teleop","key":"w","arm":true,"deadman":true})
ae({"op":"face","action":"attach"})
```

Receipt actions: `FACE://ATTACH`, `FACE://DETACH`, `FACE://VOICE_REPLY`, `FACE://TELEOP`, `FACE://TELEOP_DENIED`.

## Pi500 keyboard

Copy `scripts/pi500_teleop.py` and `scripts/removable_face.py` to the Pi 500 and run:

```bash
python3 pi500_teleop.py --help
PI500_ARM=1 python3 pi500_teleop.py
python3 pi500_teleop.py --key w --arm --deadman
python3 pi500_teleop.py --demo
```

| Key | Command |
|---|---|
| `w` / `s` | locomotion forward / backward |
| `a` / `d` | turn left / right |
| `q` / `e` | raise left / right arm |
| `r` / `f` | look up / down |
| `space` | all stop |
| `v` | voice listen (transcribed text supplied externally) |
| `t` | toggle tablet face |
| `x` | safe stop / exit |

Safety: motion keys require **arm** (`PI500_ARM=1` or `--arm`) **and** a per-command deadman prefix `!` in interactive mode (or `--deadman` in one-shot mode). A denied command still writes a `FACE://TELEOP_DENIED` receipt.

## Limits (stated plainly)

- This is the control contract and reference client, not a physical tablet fabrication package.
- `tiny-voca` handles **speech output**. Wake-word and speech-to-text come from the phone / Android MCP layer; this module never pretends STT happened locally.
- No motion command drives hardware without arm + deadman, and every command is receipted.
- The tablet can fail or disappear at any time; the agent does not depend on it for authority, identity, or receipts.
