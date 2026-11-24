# Voice → Compute Identity Map

`tiny-voca-voice` 1.2.0 ships a machine-readable identity map at `identity.json`.
It is exposed by `tts_voices({})` under `identity` and `compute_layers`, and it
is embedded in every generated Asimov lesson bundle's `lesson.json`.

The human remains root. Voices are instruments, not principals. Authority is
never transferred by a voice alias, a robot body, or a compute binding.

| Voice | Name | Role | Principal | Compute layer | Runtime |
|---|---|---|---|---|---|
| `F2` | nous girl | root voice | `HUMAN://ROOT` | `human-intent` | tiny-voca ONNX / CPU, 24 kHz |
| `M2` | hermes-agent | build voice | `agent` | `agent-runtime` | tiny-voca ONNX / CPU, 24 kHz |
| `ROBOT` | asimov-robot | robot body voice | `robot` | `robot-body` | F2 source → robotVOICE → `menlo.asimov.Robot.speaker.play_pcm`, 44.1 kHz |

## Meaning

- **F2 / nous girl** carries human intent and root questions. It is the source
  timbre for the robot voice, but it does not sign or grant authority.
- **M2 / hermes-agent** carries agent narration and build reporting. It executes
  under approval; it is not the authority root.
- **ROBOT / asimov-robot** is the body output identity. It derives from F2,
  resamples 24 kHz → 44.1 kHz for the Asimov speaker path, and remains an
  executor. The Menlo Edge safety layer still owns physical safety.

## Query from Hermes

```text
tts_voices({})
```

The response includes:

```json
{
  "identity": { "bindings": { "F2": {}, "M2": {}, "ROBOT": {}, "SOVÆREIGN": {} } },
  "compute_layers": {
    "human-intent": "F2 / nous girl — HUMAN://ROOT intent, local tiny-voca CPU",
    "agent-runtime": "M2 / hermes-agent — agent execution, local tiny-voca CPU",
    "robot-body": "ROBOT / asimov-robot — F2 source resampled for Menlo Asimov speaker",
    "human-twin": "SOVÆREIGN / soværeign voice — human-approved VoxMel clone, English and Chinese"
  }
}
```

Authority chain:

```text
HUMAN://ROOT → æ → RECEIPT
```
