# Hermes-Agent://tinyVOCA

> Local voices. Named compute layers. Receipted authority.

**`tiny-voca-voice` — first-class Hermes Agent package · CPU only · 24 kHz · Apache-2.0 · Hermes ≥0.22.2**

[Beautiful project page](site/index.html) · [Install in Hermes](hermes://plugin/install?repo=MYaelMendez/tiny-voca&enable=1) · [1:1 film](assets/hermes-agent-tinyvoca-repo-1x1.mp4) · [Attribution](docs/ATTRIBUTION.md)

`tiny-voca-voice` packages the [tiny-voca](https://huggingface.co/n4ze3m/tiny-voca)
ONNX model as a first-class Hermes provider and Desktop dock. It runs entirely
on CPU: no API key, no cloud call, no PyTorch. Weights are downloaded once and
SHA-256 verified. Every spoken line is recorded as a `HUMAN://ROOT` hash-chained
`TTS://SPEAK` receipt.

> **Thank you to the original tiny-voca project and its authors.** This package
> stands on their source, along with [dizione](https://github.com/n4ze3m/dizione)
> and [nilbuild/stick-scene](https://github.com/nilbuild/stick-scene). We built
> the authority, receipts, identity map, and Hermes surfaces on top of their
> work. #opensourceware #internetofagents

Version 1.1.0 added `tts_stick_lesson`, which builds narrated Asimov robot stick
lessons on the unchanged upstream stick-scene runtime. Version 1.2.0 adds
`identity.json`, a machine-readable voice → principal → compute-layer map that
`tts_voices({})` exposes to Hermes-agent users. tinyTELEPROMPTER is the newest
surface: a narrated 9:16 command glass with `PROMPT://BUILD` receipts.

- **Version:** 1.2.0
- **Runtime root:** `$TINY_VOCA_HOME`, falling back to `$HERMES_HOME/tiny-voca`
- **Plugin destination:** `$HERMES_HOME/plugins/tiny-voca-voice`
- **Provider name:** `tiny-voca` (enable with `hermes config set tts.provider tiny-voca`)

## What ships

| Path | Purpose |
|---|---|
| `plugin.yaml` | Manifest: eight tools and this plugin version |
| `identity.json` | Voice → principal → compute-layer identity map |
| `scripts/tiny_voca_voice.py` | Provider CLI: `--text-file` in, WAV out, JSON on the last stdout line |
| `scripts/tiny_voca_paths.py` | Stdlib-only path, alias, and receipt-chain helpers |
| `scripts/tiny_voca_verify.py` | Validate the receipt hash chain; prints one JSON line |
| `scripts/asimov_stick_lesson.py` | Build narrated Asimov stick lessons with a `LESSON://BUILD` receipt |
| `scripts/tiny_teleprompter.py` | Build TTS-synced 9:16 teleprompter pages with `PROMPT://BUILD` receipts |
| `scripts/tiny_voice.py` | tinyVOICE router: tiny-voca today, VoxMel human-twin voice when provisioned |
| `assets/stick-scene/` | Unmodified upstream runtime, MIT license, and three Asimov scenes |
| `__init__.py` | Registers the seven `tts_*` tools and the skill |
| `skills/tiny-voca-voice/SKILL.md` | Hermes skill that teaches an agent to use the tools |
| `desktop/plugin.js` | Hermes Desktop half: docked pane, statusbar chip, palette command |
| `dashboard/manifest.json` + `dashboard/plugin_api.py` | Scoped `/api/plugins/tiny-voca-voice/` backend |
| `package.json` | Node check/test scripts for the desktop half |
| `site/index.html` | Beautiful self-contained project page |
| `assets/brand/` | SVG master and 1080×1080 logo |
| `docs/ATTRIBUTION.md` | Human-readable upstream thanks |
| `CITATION.cff` | Citation metadata with upstream preferred citation |
| `assets/hermes-agent-tinyvoca-repo-1x1.mp4` | 1:1 repo explainer film |
| `docs/REPO_VIDEO.md` | Repo film spec, timeline, and receipt |
| `docs/NATIVE_TTS.md` | Native provider config, weights provisioning, troubleshooting |
| `docs/VOICE_COMPUTE_MAP.md` | Voice identity, principal, and compute-layer mapping |
| `docs/ASIMOV_STICK_LESSONS.md` | Stick-lesson contract, output layout, and authority model |
| `docs/TINY_TELEPROMPTER.md` | Teleprompter contract, controls, and receipts |
| `docs/TINY_VOICE.md` | tinyVOICE providers, Chinese voice, and digital-twin governance |
| `docs/VOICE_LAB.md` | SOVÆREIGN binding and Chinese ad workflow |
| `install.sh` | Copies the plugin into `$HERMES_HOME/plugins/tiny-voca-voice` |
| `.github/workflows/test.yml` | CI: `py_compile` + `unittest` only |

## Requirements

- Python 3.11+ with `numpy`, `onnxruntime`, and `dizione` importable. These are
  imported lazily, so packaging checks and unit tests need only the stdlib.
- The tiny-voca ONNX weights (checksum below). No other model files are bundled.
- Hermes Agent with plugin loading and native TTS support.

No credentials, tokens, or network access are needed at speech time.

## Project page

A beautiful, self-contained landing page lives at [`site/index.html`](site/index.html).
Hosted preview: https://htmlpreview.github.io/?https://raw.githubusercontent.com/MYaelMendez/tiny-voca/main/site/index.html

It includes the 1:1 film, the voice→compute map, an availability table, the
install link, and the upstream attribution.

## Install

```sh
sh install.sh
```

The script copies the plugin payload into `$HERMES_HOME/plugins/tiny-voca-voice`
(`HERMES_HOME` defaults to `$HOME/.hermes`) and prints the command that enables
native TTS:

```sh
hermes config set tts.provider tiny-voca
```

It never prompts for secrets and writes nothing outside the Hermes home.

## Hermes Desktop dock

This is a unified Hermes plugin package: the Python tools and the Desktop half
install together. Install with:

```text
hermes://plugin/install?repo=MYaelMendez/tiny-voca&enable=1
```

Then **Capabilities → Plugins → Rescan** and enable **tinyVOCA Voice Dock**.
The pane docks to the right of the conversation; the statusbar chip shows
weight readiness. It reaches its own scoped backend at
`/api/plugins/tiny-voca-voice/` for `/status`, `/identity`, and `/speak`.
No cookies, tokens, core patches, webviews, or external services are used.

The desktop half is opt-in. The Python backend is mounted only when
`tiny-voca-voice` is in `plugins.enabled`, matching Hermes' security boundary.

### Provision the weights

```sh
ROOT="${TINY_VOCA_HOME:-$HERMES_HOME/tiny-voca}"
mkdir -p "$ROOT/onnx"
curl -L --fail -o "$ROOT/onnx/model.onnx" \
  https://huggingface.co/n4ze3m/tiny-voca/resolve/main/onnx/model.onnx
printf '%s  %s\n' \
  fe6d918791a15b82e37465981d7f27a070e46b46635e5a3482fc8dff87a1ae46 \
  "$ROOT/onnx/model.onnx" | sha256sum -c -
```

Stop if the checksum check fails. The CLI sets `DIZIONE_DATA` to `$ROOT/phonemizer`
on every synthesis call, overriding any stale value in the environment.

## Repo film

A 25-second 1:1 explainer is included at
`assets/hermes-agent-tinyvoca-repo-1x1.mp4`. It maps F2, M2, and ROBOT to their
compute layers and demonstrates `tts_stick_lesson`. See
[docs/REPO_VIDEO.md](docs/REPO_VIDEO.md).

## CLI

The CLI contract is deliberately small: a UTF-8 text file in, a 16-bit WAV out,
and exactly one JSON result on the **last** line of stdout.

```sh
python3 scripts/tiny_voca_voice.py \
  --text-file input.txt \
  --output out.wav \
  --voice M2
```

| Flag | Default | Notes |
|---|---|---|
| `--text-file` | — | Provider path; reads UTF-8 text |
| `--text` | — | Inline alternative; mutually exclusive with `--text-file` |
| `--output` | `$HOME/.hermes/tiny-voca-out.wav` | Parent directories are created automatically |
| `--voice` | `M2` | `F2`/`M2` or an alias; aliases are resolved before inference |
| `--speed` | `1.0` | Speech rate multiplier |
| `--pitch-shift` | `0.0` | Pitch offset |
| `--pitch-range` | `1.0` | Pitch variability |

Successful output (last line):

```json
{"success": true, "output": "...", "voice": "M2", "alias": "M2",
 "sentences": 1, "duration_s": 2.31, "sample_rate": 24000,
 "sha256": "<64 hex chars>", "receipt": "<chain hash>"}
```

`voice` is canonical (`F2` or `M2`); `alias` echoes what the caller supplied.
If receipt writing fails, synthesis still succeeds and `receipt` is `null` with
a `receipt_error` field. Failures print
`{"success": false, "error": "..."}` and exit non-zero.

## Native provider config

Hermes writes the utterance to `{input_path}` and the CLI writes the WAV to
`{output_path}`. Add or merge this block in `config.yaml`:

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

If your Hermes build does not expand environment variables in config, replace
`$HERMES_HOME` with its expanded path. The native provider is fixed to `M2`;
set `voice_compatible: true` so callers may still pass a voice override.

Enable it from a `terminal` call:

```sh
hermes config set tts.provider tiny-voca
```

Once enabled, the built-in `text_to_speech` tool and the `/voice on` and
`/voice tts` toggles route through this provider. See
[docs/NATIVE_TTS.md](docs/NATIVE_TTS.md) for a full walkthrough.

## Plugin tools and aliases

The plugin registers eight top-level tools:

| Tool | Action |
|---|---|
| `tts_speak` | Synthesize text to WAV and append a `TTS://SPEAK` receipt |
| `tts_voices` | List voices, aliases, and the expected model checksum |
| `tts_receipts` | Read recent ledger entries |
| `tts_verify` | Validate the receipt hash chain |
| `tts_stick_lesson` | List or build narrated Asimov stick lessons |
| `tts_teleprompt` | List or build TTS-synced tinyTELEPROMPTER pages |
| `tts_voice` | List tinyVOICE providers, bind a consented digital-twin voice, or synthesize |
| `tts_lab` | Consent-gated SOVÆREIGN voice lab and Chinese one-person-company ad prep |

Example calls:

```text
tts_voices({})
tts_speak({"text": "Receipts on every action.", "voice": "hermes-agent"})
tts_stick_lesson({"op": "list"})
tts_stick_lesson({"op": "build", "lesson": "all", "out": "/path/to/bundle"})
tts_teleprompt({"op": "list"})
tts_teleprompt({"op": "build", "script": "sovereignty", "out": "/path/to/teleprompter"})
tts_voice({"op": "list"})
tts_lab({"op": "card"})
tts_receipts({"limit": 10})
tts_verify({})
```

The parent Hermes repo's aggregate `ae` tool exposes the `speak` and `voices`
shortcuts, which dispatch to `tts_speak` and `tts_voices` respectively.

### tinyTELEPROMPTER

`tts_teleprompt` builds a 9:16 command glass from a deterministic script. Lines
are synthesized by tinyVOCA, highlighted inside a horizontal read band, and
receipted with `TTS://SPEAK` plus one `PROMPT://BUILD`. It has play/pause, line
jump, speed, font-size, voice toggle, keyboard controls, progress, and ETA.
See [docs/TINY_TELEPROMPTER.md](docs/TINY_TELEPROMPTER.md).

### Asimov stick lessons

`tts_stick_lesson` builds a self-contained page with three lessons:
authority command, governed robot verbs, and the USD twin. It copies the
upstream runtime byte-for-byte, synthesizes English narration for each lesson,
writes `lesson.json`, and appends one `LESSON://BUILD` receipt. See
[docs/ASIMOV_STICK_LESSONS.md](docs/ASIMOV_STICK_LESSONS.md).

### Voice aliases

| Canonical | Aliases | Character |
|---|---|---|
| `F2` | `F2`, `f2`, `nous-girl`, `nous_girl`, `nous girl` | female, en-US, 24 kHz |
| `M2` | `M2`, `m2`, `hermes-agent`, `hermes_agent`, `hermes agent` | male, en-US, 24 kHz |

Alias resolution is case-insensitive and normalizes `-` and `_` to spaces.
`F2` is the root/question voice; `M2` is the build/narration voice and the
default for the native provider.

### Voice identity and compute layers

Identity is not just an alias. `identity.json` binds each voice to a principal
and a compute layer; `tts_voices({})` returns the same map to Hermes users.

| Identity | Compute layer | Meaning |
|---|---|---|
| `F2` · nous girl | `human-intent` | Root voice, `HUMAN://ROOT`; also the source timbre for the robot voice |
| `M2` · hermes-agent | `agent-runtime` | Build/narration voice; agent executes, never signs |
| `ROBOT` · asimov-robot | `robot-body` | F2 source resampled for the Menlo Asimov speaker via robotVOICE |

See [docs/VOICE_COMPUTE_MAP.md](docs/VOICE_COMPUTE_MAP.md).

## Receipts

Every successful synthesis appends a `TTS://SPEAK` receipt to the JSONL ledger
at `$HERMES_HOME/tiny-voca-receipts.jsonl` (override with
`HERMES_TINY_VOCA_LEDGER`). Each entry records `ts`, `action`, `authority`,
canonical `voice`, supplied `alias`, `success`, WAV `sha256`, `duration_s`,
`output`, `prev`, and `hash`. A completed lesson bundle appends one
`LESSON://BUILD` entry to the same chain. The chain begins with `prev` equal to
64 zeroes; each hash is `sha256(prev || canonical_json(entry_without_hash))`.

The CLI echoes the new `hash` in its `receipt` field and `tts_verify` validates
every link and content hash. This is a local tamper-evident chain: verification
checks structure and linkage, not cryptographic authenticity.

## Limits

- **English only** — the phonemizer cannot read other languages; non-readable
  text returns `{"success": false, "error": "..."}`.
- **Local CPU inference**, no streaming, no real-time playback.
- **24 kHz, mono, 16-bit WAV** output; peaks normalized to 0.99.
- Sentences longer than 300 characters are split; chunks are joined with
  180 ms of silence. A single utterance is capped at 512 tokens.
- The first call is slow while the lazy ONNX session loads.
- Native provider defaults to fixed `M2`; both voices are selectable via the CLI
  or the `tts_speak` tool.
- Weights are not vendored; they must be provisioned and verified at install time.

## License and upstream

Plugin packaging and documentation are released under the terms in
[LICENSE](LICENSE) (Apache-2.0). Upstream components remain under their own
licenses — see [NOTICE.md](NOTICE.md):

- [n4ze3m/tiny-voca](https://github.com/n4ze3m/tiny-voca) — Apache-2.0 (model/weights).
- [n4ze3m/dizione](https://github.com/n4ze3m/dizione) — Apache-2.0 (phonemizer).
- [nilbuild/stick-scene](https://github.com/nilbuild/stick-scene) — MIT (canvas runtime; copied unchanged under `assets/stick-scene/`).

`HUMAN://ROOT` is an attribution marker for the receipt ledger, not a software
license.

## Thanks

Thank you again to the original [tiny-voca](https://github.com/n4ze3m/tiny-voca)
authors for the source that made this development possible. See
[docs/ATTRIBUTION.md](docs/ATTRIBUTION.md) for the full credit.

#opensourceware #internetofagents
