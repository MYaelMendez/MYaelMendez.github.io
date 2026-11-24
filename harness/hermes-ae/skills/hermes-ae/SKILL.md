---
name: hermes-ae
description: Receipted Asimov studio ops for physics and video.
version: "3.18.0"
author: "Yael Méndez (@yaelmendez), Hermes Agent"
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [asimov, robot, video, physics, receipts, mujoco, ffmpeg]
    related_skills: []
---

# hermes-ae Skill

`hermes-ae` exposes a single receipted tool, `ae`, for the Asimov robot studio. It
dispatches bundled physics/render pipelines and local legacy plugin tools, then
records a HUMAN://ROOT hash-chained receipt for every operation on a JSONL ledger.
It runs prebuilt scripts and reports their QC results; it does not train voices,
design robots, or edit meshes. MuJoCo and ffmpeg make it Linux-only.

## When to Use

- Generate an Asimov studio talk/walk video with physics and visemes.
- Generate the mocap-guided free-base walk video.
- Probe or render media, list voices, or reach a local legacy plugin tool.
- Inspect, list, or verify the receipt ledger.
- Don't use for: designing new robot models, training TTS voices, or editing
  meshes; those are inputs, not operations this tool performs.

## Prerequisites

- Linux host with `mujoco`, `numpy`, and `Pillow` importable by the interpreter
  named in `HERMES_AE_PYTHON`.
- `ffmpeg` and `ffprobe` on `PATH`.
- `git` configured with push access only if publishing to the gallery repo.
- Environment variables (all optional; defaults are relative to the user home
  `.hermes` directory):
  - `HERMES_HOME` — Hermes home; scopes the default ledger and plugin paths.
  - `HERMES_AE_PYTHON` — interpreter used to launch the bundled scripts.
  - `HERMES_AE_PLUGINS` — directory of local legacy plugins for `call`/shortcuts.
  - `HERMES_AE_LEDGER` — JSONL receipt ledger path.
  - `HERMES_AE_HOME`, `HERMES_AE_ANIM`, `HERMES_AE_MODEL`, `HERMES_AE_MESHES`,
    `HERMES_AE_GALLERY` — runtime asset and gallery paths.
- Repo-relative model manifests ship under `model/`. Binary meshes and videos are
  not bundled and must be provisioned at the runtime paths above.

## How to Run

Call the registered `ae` tool with a JSON object. `op` selects the action; every
other key is forwarded as an argument. Each call returns a JSON string with
`success`, `op`, `result`, and a `receipt`.

- Core ops need no external tooling: `status`, `receipts`, `verify`, `ops`, `call`.
- TTS primitive: `speak`/`tts_speak`, `voices`/`tts_voices`, `tts_receipts`.
- Bundled pipelines: `studio_video`, `free_walk` (heavy; use a long timeout).
- Shortcuts (`speak`, `voices`, `render`, `probe`, `gallery`, `vlc`, `nodes`,
  `robot_say`, `studio`, `physics`, `face_states`, `chimera_speak`, and others)
  reach local legacy plugins only when installed under `HERMES_AE_PLUGINS`.

Use `read_file` to inspect this repo's sources, `patch` or `write_file` to edit
them, and `terminal` to run local checks. Do not invoke bundled pipelines from
`terminal` directly; go through the `ae` tool so a receipt is always written.

## Quick Reference

- `ae {"op":"status"}` — version, plugin count, shortcuts, chain head.
- `ae {"op":"ops"}` — list shortcuts and bundled ops.
- `ae {"op":"receipts","limit":10}` — last N receipts.
- `ae {"op":"verify"}` — validate the hash chain.
- `ae {"op":"call","plugin":"...","tool":"...","arg":"..."}` — invoke a local plugin tool.
- `ae {"op":"studio_video","publish":false}` — studio pipeline, no publish.
- `ae {"op":"free_walk","publish":false,"authorization":"user"}` — free-walk pipeline.
- `ae {"op":"speak","text":"...","voice":"hermes-agent"}` — TTS shortcut; `nous-girl` selects F2.
- `ae {"op":"render","script":"...","output":"..."}` — ffmpeg render shortcut.

## Procedure

1. Confirm prerequisites: with `terminal`, check `ffmpeg -version` and that the
   `HERMES_AE_PYTHON` interpreter imports `mujoco`, `numpy`, and `PIL`.
   Completion: all checks exit 0.
2. Point `HERMES_AE_LEDGER` at a sandbox file so dry-run receipts stay separate
   from production. Completion: the variable is exported before any `ae` call.
3. Check state: call `ae {"op":"status"}`. Completion: `success` is true and
   `result.receipts.success` is true.
4. Run a pipeline with `publish:false` first, e.g.
   `ae {"op":"studio_video","publish":false}` with a timeout of at least 1500s.
   Completion: a JSON line with `success` true, an `output` path, and a `qc`
   report whose video, audio, sound, and frame checks are all true.
5. Verify the chain: call `ae {"op":"verify"}`. Completion: `result.success` is
   true and `result.count` equals the number of receipts written so far.
6. Publish only on intent: rerun with `publish:true` (requires `git` push
   access). Completion: the `publish` block shows non-zero `raw_status` and
   `api_status`.

## Pitfalls

- Heavy pipelines import MuJoCo in a subprocess and take minutes; always use a
  long timeout (1500s) with `terminal` or the call will be cut off.
- `call` and shortcuts return an error with an `available` list when the target
  plugin is absent from `HERMES_AE_PLUGINS`; check `status.plugins_on_disk` first.
- Publishing pushes to a GitHub Pages `gh-pages` branch over the network and is
  on by default, so set `publish:false` for dry runs.
- Every operation appends a receipt, including failed and unknown ops, so
  `receipts.count` grows even on error.
- The chain is a local HUMAN://ROOT hash chain, not a secret-key signature;
  `verify` checks structure and linkage only, not authenticity.
- Binary assets are not in the repo; missing meshes or videos fail late inside
  the render subprocess and surface as an `error` string in the result.

## Verification

- Unit tests: from the repo root run
  `terminal(command="python3 -m unittest discover -s tests -v")`.
  Completion: all tests pass with no network access or heavy scripts invoked.
- Chain check: `ae {"op":"verify"}` returns `result.success:true` and a `head`
  equal to the last receipt hash returned by `ae {"op":"receipts"}`.
- Smoke check: `ae {"op":"status"}` returns `result.version:"3.1.1"` and
  `result.actor:"hermes-ae"`.

## Lessons from the v3.1 build

- The product is the authority chain, not the model: `HUMAN://ROOT → æ → RECEIPT`.
  Every new capability must strengthen that chain or it is decoration.
- A harness is a governed capability envelope; a plugin is only packaging.
  Consolidate surfaces before adding features. One `ae` tool beat eighteen plugins.
- Every published artifact needs one canonical source of truth: gallery from live
  MP4s, one hash-chained ledger, one identity file, one repo, one tag.
- Deterministic PIL-frame painting plus ffmpeg is the reliable production video
  path. WebGL is a preview/control surface; browser capture is not reliable.
- QC must fail closed on duration, frame count, codec, audio levels, bright
  pixels, sha256, and chain validity. Adjust thresholds to the aesthetic, not
  to make a failing artifact pass.
- Real artifacts beat claims: official Asimov CAD, official MJCF, tiny-voca
  voices, qpos telemetry, and honest caveats about mocap-guided locomotion.
- Identity binding: `nous girl` (F2) holds the root frame; `hermes-agent` (M2)
  builds; Asimov-1 is the build body. Human authority is never transferred.
- Verify through the wrapper, not just the handler: FakeCtx signatures, nested
  `result` objects, and local-func registries caused three patch releases.
- Patch releases are cheaper than force-moving tags. Keep the masterpiece
  artifact stable and fix code in a new tag.
- User operating mode: execute with tools, report receipts, do not hand back
  instructions-only help.

