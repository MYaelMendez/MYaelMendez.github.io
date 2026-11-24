# Native TTS with tiny-voca

This document explains how `tiny-voca-voice` plugs into Hermes Agent's native
text-to-speech layer, how to provision and verify the weights, and what to check
when speech fails. For the CLI and tool reference, see the
[README](../README.md).

## How the provider works

Hermes treats TTS providers as command wrappers. For a `type: command`
provider, Hermes writes the utterance to a temporary UTF-8 file, substitutes
`{input_path}` and `{output_path}` into the configured `command`, runs it, and
reads the resulting audio file. The `tiny_voca_voice.py` CLI implements exactly
this contract:

1. Read text from `--text-file {input_path}`.
2. Canonicalize the voice alias, phonemize with `dizione`, synthesize via ONNX
   Runtime on CPU.
3. Write a 16-bit mono 24 kHz WAV to `--output {output_path}`.
4. Print exactly one JSON object on the **last** line of stdout, including the
   receipt hash.

The CLI also accepts `--text` for interactive use, but the native provider
always uses `--text-file`. Runtime dependencies (`numpy`, `onnxruntime`,
`dizione`) are imported lazily inside the synthesis path.

## Configuration

Merge this block into `config.yaml`:

```yaml
tts:
  provider: tiny-voca
  providers:
    tiny-voca:
      type: command
      command: "python3 $HERMES_HOME/plugins/tiny-voca-voice/scripts/tiny_voca_voice.py --text-file {input_path} --output {output_path} --voice M2"
      output_format: wav
      timeout: 180
      voice_compatible: true
```

| Key | Value | Why |
|---|---|---|
| `type` | `command` | Hermes launches the CLI as a subprocess |
| `command` | see above | `{input_path}` / `{output_path}` are injected by Hermes |
| `output_format` | `wav` | Matches the CLI's PCM WAV output |
| `timeout` | `180` | First call loads the ONNX model lazily |
| `voice_compatible` | `true` | Allows callers to pass a voice override |

If your Hermes build does not expand environment variables inside config,
replace `$HERMES_HOME` with its expanded absolute path. Ensure `python3` on
`PATH` can import `numpy`, `onnxruntime`, and `dizione`.

Enable the provider:

```sh
hermes config set tts.provider tiny-voca
```

After enabling, the built-in `text_to_speech` tool and the `/voice on` and
`/voice tts` toggles route through this provider.

## Weights and runtime root

The runtime root is resolved in this order:

1. `$TINY_VOCA_HOME` if set.
2. Otherwise `$HERMES_HOME/tiny-voca`.
3. Otherwise `$HOME/.hermes/tiny-voca` when `HERMES_HOME` is also unset.

Expected layout:

```
$TINY_VOCA_HOME/
├── onnx/
│   └── model.onnx
├── config.json
└── phonemizer/          # exported as DIZIONE_DATA on every synthesis call
```

Provision and verify:

```sh
ROOT="${TINY_VOCA_HOME:-${HERMES_HOME:-$HOME/.hermes}/tiny-voca}"
mkdir -p "$ROOT/onnx"
curl -L --fail -o "$ROOT/onnx/model.onnx" \
  https://huggingface.co/n4ze3m/tiny-voca/resolve/main/onnx/model.onnx
printf '%s  %s\n' \
  fe6d918791a15b82e37465981d7f27a070e46b46635e5a3482fc8dff87a1ae46 \
  "$ROOT/onnx/model.onnx" | sha256sum -c -
```

Do not proceed if the checksum check fails: a truncated or replaced model can
produce garbage audio or crash the inference session.

## Voices and aliases

| Canonical | Accepted aliases | Character |
|---|---|---|
| `F2` | `F2`, `f2`, `nous-girl`, `nous_girl`, `nous girl` | female, en-US |
| `M2` | `M2`, `m2`, `hermes-agent`, `hermes_agent`, `hermes agent` | male, en-US |

Alias matching is case-insensitive and treats `-` and `_` as spaces. `F2` is the
root/question voice; `M2` is the build/narration voice and the default for the
native provider. To use `F2` natively, change `--voice M2` to `--voice F2` in the
command string, or call `tts_speak` with a voice argument. `tts_voices({})`
reports the live voice list and the expected model checksum.

## Receipts

Each successful synthesis appends a `TTS://SPEAK` receipt to the JSONL ledger
at `$HERMES_HOME/tiny-voca-receipts.jsonl`, or at
`$HERMES_TINY_VOCA_LEDGER` when that variable is set. The entry records:

- `ts`, `action: TTS://SPEAK`, `authority: HUMAN://ROOT`
- canonical `voice`, supplied `alias`, `success`
- WAV `sha256`, `duration_s`, and `output` path
- `prev` — the previous head hash, or 64 zeroes for the first entry
- `hash` — `sha256(prev || canonical_json(entry_without_hash))`

The CLI echoes the new `hash` in the `receipt` field of its JSON result. A
receipt-write failure never breaks synthesis: `receipt` becomes `null` and a
`receipt_error` field explains why.

`tts_verify({})`, or `python3 scripts/tiny_voca_verify.py`, recomputes every
hash and confirms each `prev` links to the preceding entry. It reports
`success`, `ok`, `count`, `head`, and `broken_at`. This verifies structure and
linkage only, not authenticity.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `missing dependency` on synthesis | `numpy`, `onnxruntime`, or `dizione` not importable | Install them into the interpreter that runs the CLI |
| `nothing in the text could be read` | Non-English or empty input | Provide readable English text |
| `unknown voice` error | Unrecognized voice string | Use a canonical voice or a documented alias |
| Failure at first synthesis | `onnx/model.onnx` missing or corrupt | Re-download and re-verify the SHA-256 |
| `receipt: null` | Ledger path is not writable | Set `HERMES_TINY_VOCA_LEDGER` to a writable file |
| Provider falls back | `tts.provider` not set to `tiny-voca` | Re-run the `hermes config set` command |
| Call times out | Cold ONNX load or very long text | Raise `timeout` and split the text into shorter files |

## Limits

- English only; no multilingual phonemization.
- CPU inference, no streaming, no real-time playback.
- 24 kHz mono 16-bit WAV output; sentences are split at 300 characters and
  joined with 180 ms gaps; one utterance is capped at 512 tokens.
- The native provider command is fixed to one voice per configuration; both
  voices are available through the CLI and `tts_speak`.
