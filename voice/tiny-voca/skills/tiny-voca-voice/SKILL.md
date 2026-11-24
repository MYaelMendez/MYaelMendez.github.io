---
name: tiny-voca-voice
description: Speak English locally and build narrated Asimov lessons.
version: "1.3.1"
author: Yæl Méndez (@yaelmendez), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tts, voice, onnx, local, receipts, english, stick-lessons, asimov]
    related_skills: []
---

# tiny-voca-voice Skill

`tiny-voca-voice` is a first-class Hermes plugin with seven registered tools.
It speaks English locally through the tiny-voca ONNX model, writes 24 kHz mono
WAV files, appends `HUMAN://ROOT` hash-chained receipts, and builds narrated
Asimov stick lessons on the unmodified upstream stick-scene runtime.
It does not train voices, clone voices, stream audio, or read non-English text.

## When to Use

- The user asks for speech or an audio file from text and no cloud TTS is set.
- A native Hermes TTS provider is needed (`tts.provider: tiny-voca`).
- You need to list voices, inspect receipts, or verify the receipt chain.
- The user asks for an Asimov stick-figure lesson, an educational robot scene,
  or a narrated OpenSourceWare explanation.
- Don't use for: non-English text, singing, voice cloning, real-time streaming,
  or drawing figures from scratch; use a canvas scene skill for custom scenes.

## Prerequisites

- Python 3.11+ with `numpy`, `onnxruntime`, and `dizione` importable. They load
  lazily, so packaging checks need only the standard library.
- Weights under `$TINY_VOCA_HOME`, falling back to `$HERMES_HOME/tiny-voca`.
  The file `onnx/model.onnx` must match SHA-256
  `fe6d918791a15b82e37465981d7f27a070e46b46635e5a3482fc8dff87a1ae46`.
- The plugin installed at `$HERMES_HOME/plugins/tiny-voca-voice`:
  `terminal(command="sh install.sh")` from the repo root. The unified package
  also ships `desktop/plugin.js` and `dashboard/plugin_api.py` for Hermes Desktop.
- Hermes tools: `terminal` for scripts, `write_file` and `read_file` for text,
  `search_files` for plugin assets, `browser_exec` for page QA when available.

## How to Run

Prefer the registered tools: `tts_speak`, `tts_voices`, `tts_receipts`,
`tts_verify`, `tts_stick_lesson`, `tts_teleprompt`, `tts_voice`, and `tts_lab`. All paths below are
repo-relative or environment-based; never hardcode a machine-local directory.

- `terminal(command="python3 scripts/tiny_voca_voice.py --text-file in.txt --output out.wav --voice M2")`
- `terminal(command="python3 scripts/asimov_stick_lesson.py --op list")`
- `terminal(command="python3 scripts/asimov_stick_lesson.py --op build --lesson all --out out/")`
- `terminal(command="python3 scripts/tiny_teleprompter.py --op build --script sovereignty --out teleprompter/")`
- `terminal(command="python3 scripts/tiny_voca_verify.py")`
- `terminal(command="hermes config set tts.provider tiny-voca")`
- `read_file(path="docs/VOICE_COMPUTE_MAP.md")` — voice identity map.
- `read_file(path="site/index.html")` — beautiful project page.
- `read_file(path="docs/ASIMOV_STICK_LESSONS.md")` — lesson contract.
- `read_file(path="docs/TINY_TELEPROMPTER.md")` — teleprompter contract.
- `read_file(path="docs/TINY_VOICE.md")` — tinyVOICE provider and twin governance.
- `read_file(path="docs/VOICE_LAB.md")` — SOVÆREIGN binding and Chinese ad workflow.
- Voices: `F2` (`nous-girl`) and `M2` (`hermes-agent`); aliases are normalized.
- Identity: `F2 → human-intent`, `M2 → agent-runtime`, `ROBOT → robot-body`, `SOVÆREIGN → human-twin`.
- Receipts: `TTS://SPEAK`, `LESSON://BUILD`, `PROMPT://BUILD`; authority `HUMAN://ROOT`.

## Quick Reference

- `tts_speak({text, voice, output, speed})` — synthesize one utterance.
- `tts_voices({})` — list voices, aliases, identity bindings, and runtime status.
- `tts_receipts({limit})` — read the recent hash-chained ledger entries.
- `tts_verify({})` — validate every receipt link and content hash.
- `tts_stick_lesson({op:"list"})` — list the three Asimov lessons.
- `tts_stick_lesson({op:"build", lesson:"all", out:"..."})` — build the page,
  copy the unchanged upstream runtime, synthesize narration, and receipt it.
- `tts_teleprompt({op:"list"})` — list teleprompter scripts.
- `tts_teleprompt({op:"build", script:"sovereignty", out:"..."})` — build a
  narrated 9:16 command glass with `PROMPT://BUILD`.
- `tts_voice({op:"list"})` — list tinyVOICE providers and identity bindings.
- `tts_lab({op:"card"})` — inspect the consent-gated SOVÆREIGN voice lab.
- Desktop dock: `desktop/plugin.js` + `dashboard/plugin_api.py`; enable
  **tinyVOCA Voice Dock** in Capabilities → Plugins, then use the right pane.
- Lesson IDs: `asimov-authority`, `asimov-verbs`, `asimov-twin`, `all`.
- Default narration speed: `1.25`.

## Procedure

1. Provision weights. With `terminal`, download `onnx/model.onnx` from the
   upstream URL and check its SHA-256.
   Completion: the checksum equals the value in Prerequisites.
2. Install the plugin: `terminal(command="sh install.sh")`.
   Completion: `scripts/tiny_voca_voice.py` and `assets/stick-scene/` exist
   under `$HERMES_HOME/plugins/tiny-voca-voice`.
3. Synthesize speech with `tts_speak`, or enable native TTS with
   `terminal(command="hermes config set tts.provider tiny-voca")`.
   Completion: the CLI returns JSON with `success:true`, canonical `voice`,
   `duration_s`, and a 64-hex `sha256`.
4. List lessons with `tts_stick_lesson({op:"list"})`.
   Completion: all three IDs appear with at least one narration line each.
5. Build a bundle with `tts_stick_lesson({op:"build", lesson:"all", out:"..."})`.
   Completion: `index.html`, `stick.js`, `scenes/`, `audio/`, `lesson.json`,
   and the upstream `LICENSE` exist in the output directory.
6. Check the WAVs with `read_file` on `lesson.json` and `terminal` checksums.
   Completion: each narration entry's `sha256` matches its WAV on disk.
7. Check receipts with `tts_receipts({limit:20})`: the last `TTS://SPEAK` and
   `LESSON://BUILD` entries must each chain from the previous `hash`.
   Completion: `tts_verify({})` returns `ok:true` and `broken_at:null`.
8. Open `index.html` with `browser_exec` when a browser is available.
   Completion: `window.SCENES` contains all lesson scene IDs and each
   `<stick-scene>` has one canvas with no horizontal overflow.

## Pitfalls

- English only: `dizione` cannot phonemize other languages; the CLI returns
  `{"success": false, "error": "..."}` instead of a WAV.
- Long text is split into sentences of at most 300 characters and joined with
  180 ms of silence; a single utterance is capped at 512 tokens.
- The native provider is fixed to `M2`. Select `F2` with `--voice F2`, an alias,
  or the `tts_speak` tool's `voice` argument.
- The first call is slow while the lazy ONNX session loads; keep a generous
  `terminal` timeout.
- Weight and phonemizer paths follow `$TINY_VOCA_HOME` / `$HERMES_HOME/tiny-voca`.
  A missing `onnx/model.onnx` fails at session creation, not argument parse.
- `LESSON://BUILD` is appended to the same ledger as `TTS://SPEAK`; do not
  write a second wrapper receipt for the same bundle.
- `install.sh` copies `assets/`; skip it and the lesson builder fails with
  `stick-scene assets missing` even though TTS tools still work.
- Receipt verification checks hash linkage and content hashes, not authenticity.

## Verification

- `terminal(command="python3 -m unittest discover -s tests -v")` — all tests
  pass with no network access and no weights required.
- `terminal(command="python3 scripts/acceptance.py")` — fresh-clone packaging,
  five-tool registration, portability, and syntax all pass.
- `terminal(command="python3 scripts/asimov_stick_lesson.py --op build --lesson asimov-authority --out out/")`
  — page, runtime, scene, WAV, manifest, and receipt all appear under `out/`.
- Native path: after enabling the provider, `text_to_speech` produces a WAV
  and `tts_verify({})` reports `ok:true`.
