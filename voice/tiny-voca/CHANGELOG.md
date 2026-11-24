## [1.3.1] - 2026-11-18

### Changed

- `SOVÆREIGN` default timbre set to the **broadcast** signal-derived variant
  from the bound human reference; low and bright remain alternates.
- VoxMel router now uses the bound voice card for default prompt audio and
  transcript when `VOXMEL_PROMPT_AUDIO` / `VOXMEL_PROMPT_TEXT` are unset.

## [1.3.0] - 2026-11-18

### Added

- Voice Lab: `tts_lab` tool with `card`, `bind`, `provision`, and `ad` ops.
- Consent-gated `SOVÆREIGN` binding with `VOICE://BIND` receipts.
- Chinese one-person-company ad script and VoxMel render plan.
- `docs/VOICE_LAB.md` with the full clone/ad governance workflow.

# Changelog

All notable changes to `tiny-voca-voice` are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `GO://TINY` starter: `tts_voice({op:"go"})` produces a receipted two-voice
  tinyVOCA demo and reports VoxMel readiness.
- `examples/tiny-voice/` consent, exact-transcript, and Chinese script templates.
- tinyVOICE router with `tts_voice`: lists local providers, binds a consented
  human digital-twin voice with `VOICE://BIND`, and routes synthesis to
  tiny-voca or VoxMel with `VOICE://SPEAK`.
- `SOVÆREIGN` identity binding: `human-twin`, English and Chinese, human root,
  explicit consent required.
- `docs/TINY_VOICE.md` with provider matrix and one-person-company thesis.
- `tts_teleprompt` tool and `scripts/tiny_teleprompter.py`: builds a 9:16
  tinyTELEPROMPTER page with TTS-synced lines, horizontal read band, active-line
  highlight, progress/ETA, keyboard controls, voice toggle, and `PROMPT://BUILD`
  receipts.
- `docs/TINY_TELEPROMPTER.md` with script schema and controls.
- Built-in scripts: `sovereignty` and `asimov-voice-map`.
- Beautiful self-contained project page at `site/index.html`, with availability
  table, 1:1 film, install link, and upstream attribution.
- Brand assets: SVG master and 1080×1080 logo under `assets/brand/`.
- `docs/ATTRIBUTION.md` with explicit thanks to original tiny-voca, dizione,
  and stick-scene authors. #opensourceware #internetofagents
- `CITATION.cff` with upstream preferred citation.
- CI now runs desktop plugin checks alongside Python tests.
- Unified Hermes Desktop half: `desktop/plugin.js` docks a tinyVOCA pane beside
  the conversation with a statusbar chip and palette command.
- Scoped backend `dashboard/plugin_api.py` with `/status`, `/identity`, and
  `/speak` routes under `/api/plugins/tiny-voca-voice/`.
- Node check/test scripts and packaging tests for the desktop half.
- One-click install link in README.
- Upgraded the three Asimov stick lessons and repo film with identity-specific
  figures: nous girl hoodie/skirt/hair, Hermes winged helmet/visor/caduceus,
  and a CAD-derived Asimov with visor, side panels, antenna, chest plate, and
  joints. Motion and frame QA clean.

## [1.2.0] - 2026-11-18

### Added

- Machine-readable `identity.json` binding voices to principals and compute
  layers: `F2/nous girl → human-intent`, `M2/hermes-agent → agent-runtime`,
  `ROBOT/asimov-robot → robot-body`.
- `tts_voices({})` now returns `identity` and `compute_layers`, so Hermes-agent
  users can query the mapping from inside a session.
- `docs/VOICE_COMPUTE_MAP.md` explaining the three compute layers and the
  F2-derived robot voice path through robotVOICE to the Menlo Asimov speaker.
- Generated Asimov lesson bundles now embed the identity map in `lesson.json`
  and display the voice→layer map on the lesson page.

### Changed

- Version bumped to 1.2.0 across manifest, metadata, plugin, skill, installer,
  acceptance, README, and changelog.
- `install.sh` copies `identity.json`.

## [1.1.0] - 2026-11-18

### Added

- `tts_stick_lesson` — a fifth registered Hermes tool that lists or builds
  narrated Asimov robot stick lessons.
- `scripts/asimov_stick_lesson.py` — stdlib orchestrator that copies the
  unchanged upstream stick-scene runtime, writes a self-contained lesson page,
  synthesizes tiny-voca narration, and records one `LESSON://BUILD` receipt.
- `assets/stick-scene/` — upstream MIT runtime, license, and three Asimov
  scenes: authority command, governed verbs, and USD twin.
- `docs/ASIMOV_STICK_LESSONS.md` — lesson contract, output layout, receipt
  model, and authority statement.
- `append_custom_receipt()` in `scripts/tiny_voca_paths.py` so `LESSON://BUILD`
  joins the same hash chain as `TTS://SPEAK` without double receipting.
- Packaging, plugin, and acceptance tests for the fifth tool and assets.

### Changed

- Version bumped to 1.1.0 across manifest, package metadata, plugin version,
  skill frontmatter, installer, acceptance, and changelog.
- README and skill updated to present the plugin as a first-class Hermes
  capability with TTS and Asimov education surfaces.

## [1.0.0] - 2026-11-17

### Added

- First-class Hermes packaging for the tiny-voca voice layer.
- `scripts/tiny_voca_voice.py` provider contract: `--text-file` in, WAV out,
  one JSON object on the last stdout line, with canonical `voice`, supplied
  `alias`, `sha256`, `duration_s`, and `receipt` fields.
- Native TTS provider `tiny-voca` with `type: command`, `output_format: wav`,
  and `voice_compatible: true`; enable with
  `hermes config set tts.provider tiny-voca`.
- Four registered tools — `tts_speak`, `tts_voices`, `tts_receipts`, and
  `tts_verify` — plus the `speak` / `voices` shortcuts in the parent `ae` tool.
- Voice aliases: `nous-girl` and variants resolve to `F2`; `hermes-agent` and
  variants resolve to `M2`. Alias normalization is case-insensitive.
- `HUMAN://ROOT` hash-chained `TTS://SPEAK` receipts on a JSONL ledger, with a
  64-zero genesis `prev` and `sha256(prev || canonical_json(body))` linkage.
- Runtime root override `TINY_VOCA_HOME`, falling back to
  `$HERMES_HOME/tiny-voca`; SHA-256 verification for `onnx/model.onnx`.
- `skills/tiny-voca-voice/SKILL.md` and `docs/NATIVE_TTS.md`.
- `install.sh`, Apache-2.0 `LICENSE`, `NOTICE.md`, `.gitignore`, and a CI
  workflow limited to `py_compile` and `unittest`.

### Notes

- Weights are not vendored; download and verify them before first use.
- Upstream: `n4ze3m/tiny-voca` and `n4ze3m/dizione` (both Apache-2.0).

[1.2.0]: https://github.com/MYaelMendez/tiny-voca/releases/tag/v1.2.0
[1.1.0]: https://github.com/MYaelMendez/tiny-voca/releases/tag/v1.1.0
[1.0.0]: https://github.com/n4ze3m/tiny-voca/releases/tag/v1.0.0
[1.3.0]: https://github.com/MYaelMendez/tiny-voca/releases/tag/v1.3.0
[1.3.1]: https://github.com/MYaelMendez/tiny-voca/releases/tag/v1.3.1
