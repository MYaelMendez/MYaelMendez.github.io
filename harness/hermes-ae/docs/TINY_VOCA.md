# tiny-voca as a Hermes primitive

`tiny-voca` is now a first-class Hermes TTS provider, not just a video voice
script. It runs locally through ONNX Runtime with no API key and no cloud call.

## Native provider

`config.yaml`:

```yaml
tts:
  provider: tiny-voca
  providers:
    tiny-voca:
      type: command
      command: "/usr/local/bin/python3 /opt/data/plugins/hermes-ae/scripts/tiny_voca_voice.py --text-file {input_path} --output {output_path} --voice M2"
      output_format: wav
      timeout: 180
      voice_compatible: true
```

Hermes writes text to `{input_path}`; the CLI writes WAV to `{output_path}`.
Native TTS is available through the built-in `text_to_speech` tool and voice
toggles (`/voice on`, `/voice tts`). The provider uses M2 (`hermes-agent`) by default.

## Voices

| Voice | Identity | Use |
|---|---|---|
| `F2` / `nous girl` | female, en-US, 24 kHz | root voice, questions, challenges |
| `M2` / `hermes-agent` | male, en-US, 24 kHz | build voice, explanations, narration |

Both voices are exposed through the `ae` tool:

```json
{"op": "voices"}
{"op": "tts_voices"}
{"op": "speak", "text": "Human root.", "voice": "nous-girl"}
{"op": "tts_speak", "text": "Receipts on every action.", "voice": "hermes-agent"}
{"op": "tts_receipts", "limit": 10}
```

## CLI contract

```bash
python scripts/tiny_voca_voice.py \
  --text "..." \
  --voice hermes-agent \
  --output /path/to/out.wav
```

Also accepts `--text-file` for native Hermes TTS. Weights default to
`/opt/data/tiny-voca-weights`; override with `HERMES_AE_TTS_ROOT`. The
phonemizer data path is derived from the same root via `DIZIONE_DATA`.

## Receipts

Every `ae` speech operation writes a `HUMAN://ROOT` hash-chained receipt to the
unified ledger. The CLI also emits a voice receipt containing timestamp, voice,
sha256, duration, and output. Use `ae({op:"verify"})` to validate the chain.

## Limits

- English only.
- Local CPU inference; no streaming.
- Voice aliases: `nous-girl`/`nous girl` → F2, `hermes-agent` → M2.
- The native provider is fixed to `hermes-agent` (M2); both voices are selectable through `ae`.
