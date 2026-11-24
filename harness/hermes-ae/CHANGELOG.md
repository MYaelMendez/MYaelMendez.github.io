## 3.18.0

- Made the native Asimov head viewport DOM aware. `ae({op:"head", action:"dom"})`
  and `ae({op:"head_dom"})` perform bounded, read-only CDP DOM projection with
  `VIEWPORT://DOM_AWARENESS` receipts.
- Added a self-DOM digest panel to the self-contained head viewport HTML.

## 3.17.0

- Removed the tablet-face concept. The head mask and three exterior covers are
  now one native viewport system with four programmable shell zones
  (`03C`, `04C`, `06C`, `07C`).
- Added `ae({op:"head"})`; `ae({op:"face"})` remains a compatibility alias.
- Renamed the runtime contract to `scripts/head_viewport.py` and rewrote the
  DAO Brain surface around the native head viewport.

## 3.16.0

- Added **æ TV**: `ae({op:"tv_episode"})` compiles a script into a receipted
  MP4 using deterministic frames, tinyVOICE narration, and ffmpeg.
- Added `docs/AE_TV.md`: channel ontology, harness mapping, and governance.
- QC gates video codec, dimensions, audio codec, duration, and bright pixels.

## 3.15.0

- Added **æ Robot Verbs**: `ae({op:"verbs"})` lists, plans, and optionally
  executes governed wrappers over official Menlo SDK verbs.
- Motion verbs require human approval or an armed deadman; live execution is
  opt-in with `HERMES_AE_SDK_LIVE=1`; every decision is receipted.
- Extended `ae-policy.json` to v1.1.0 with the official verb names.

## 3.14.0

- Added the **DAO Brain** to power the 1:1 Asimov face tablet.
- `ae({op:"daobrain"})` evaluates proposals through æ Policy, maps decisions
  to face states, optionally speaks replies through tiny-voca, and writes
  `DAO://DECISION` receipts.
- Bound the DAO Brain into `identity.json`; added `docs/DAO_BRAIN.md`.

## 3.13.0

- Added **æ Policy**: a machine-readable OpenSourceWare authority policy for
  robots and agents in the Internet of Agents.
- Added `ae({op:"policy"})` with `show`, `verify`, and `evaluate`; every
  decision writes a `POLICY://EVALUATE` receipt and fails closed.
- Bound the policy into `identity.json` and added `docs/AE_POLICY.md`.

## 3.12.0

- Added the first **Asimov USD digital twin**: `ae({op:"twin"})` builds and
  verifies `packages/asimov-twin/1.0.0/asimov-avatar.usda` from official
  URDF/MJCF, 26 mesh references, and 216 qpos frames.
- Bound the twin into `identity.json` with `AVATAR://USD_BIND`.
- Added `scripts/asimov_twin.py` and `docs/ASIMOV_TWIN.md`. This is a robot twin,
  not an ACE skinned human avatar.

## 3.11.0

- Made the 1:1 Asimov face a **removable presence tablet**: `ae({op:"face"})`
  attaches/detaches it, falls back to tiny-voca voice replies, and accepts Pi500
  keyboard teleop with arm + deadman safety.
- Added `scripts/removable_face.py`, `scripts/pi500_teleop.py`, and
  `docs/REMOVABLE_FACE.md`. Every mode change and command is receipted.
- Bound the new capabilities into `identity.json`; no new harness was added.

## 3.10.0

- Bound the published Asimov Viewport into Asimov Agent identity: qpos CAD
  viewer, DOM readout, source-to-screen film, capability showreel, and receipts
  on one surface.

## 3.9.1

- Force-added the sovereign projection binary assets that the repo `.gitignore`
  had excluded from v3.9.0.

## 3.9.0

- Refactored the sovereign bundle into a governed `sovereign projection`
  package: authority first, deterministic replay, hashed pinned inputs,
  fail-closed QC, one receipt chain, and no extra harness.
- Added `ae({op:"projection"})` and `ae({op:"projection_render"})`.

## 3.8.0

- Bound `mobility.foundation/mobility/` as the canonical public homepage for
  Asimov Agent and the æLOCOMOTION package, with the GitHub Pages path retained
  as fallback.

## 3.7.0

- Unified the robot identity as **Asimov Agent**: one `ae({"op":"agent"})` call
  reports voice, body, harnesses, ONNX policy, DOM awareness, model hashes, and
  ledger state under `HUMAN://ROOT`.

## 3.6.0

- Added `ae({op:"viewport_dom"})`: read-only DOM awareness for the Asimov
  viewport harness via Chrome DevTools Protocol, with a projected snapshot and
  a `VIEWPORT://DOM_AWARENESS` receipt.
- No page mutation, no screenshot, no full-DOM dump.

## 3.5.0

- Packaged the policy-driven gait harness as `æLOCOMOTION` / `ae-locomotion`
  v1.0.0 with manifest, checksums, install/verify scripts, bundled ONNX policy,
  MJCF variants, renderer pipeline, and proof record.

## 3.4.1

- Fixed `ffmpeg_demo`, `policy_locomotion`, and `policy_walk` routing: these are
  bundled scripts and must not be registered as local funcs.
- No policy or film changes; v3.4.0 artifacts remain current.

## 3.4.0

- Replaced the mocap-guided gait with a real ONNX locomotion policy: Menlo
  `asimov1-locomotion-0818`, 78 observations to 23 joint targets at 50 Hz.
- Added `policy_locomotion` and `policy_walk` ops, a physics-only policy MJCF,
  a following-camera renderer, and the published `asimov-policy-walk-916.mp4`.
- Verified 12 s, 600 policy ticks, 2400 MuJoCo steps, +4.1868 m base travel,
  no fall, and a receipted chain.

## 3.3.0

- Added `ae({op:"ffmpeg_demo"})`: a 12-second 9:16 demo where Asimov, driven by
  the hermes-agent build voice, explains the ffmpeg harness chain.
- Parameterized the Asimov renderer for reusable harness identity clips.

## 3.2.0

- Promoted ffmpeg to the canonical media harness, with `media` retained as an alias.
- Added `ae({op:"ffmpeg"})` plus runtime/encoder probing in `harness` and `run_harness`.
- ffmpeg is now a governed envelope: inputs, outputs, receipt action, fallback, and QC policy.

## 3.1.1

- Fixed the `agent_body` unit-test assertion to read the wrapped `result` object.
- No identity or film changes; v3.1.0 artifacts remain current.

## 3.1.0

- Bound Asimov-1 as the visible body of the `hermes-agent` build voice.
- Added `identity.json`, `docs/ASIMOV_AGENT.md`, and the `ae({op:"agent_body"})` op.
- Published the `asimov-agent-build-916.mp4` identity proof clip.

## 3.0.1

- Fixed `run_harness` so it validates `chain` instead of requiring a single `name`.
- No film or docs changes; v3.0.0 masterpiece artifacts remain current.

## 3.0.0

- Introduced the Mixture of Harnesses (MoH) registry and `harnesses`, `harness`, `run_harness`, and `masterpiece` ops on the single `ae` tool.
- Added the v3.0.0 masterpiece pipeline: 30-second two-voice hero film, harness ontology course, hero page, and release proof.

## 2.5.0

- Named the two tiny-voca voices: F2 is `nous girl`, M2 is `hermes-agent`.
- Added CLI voice aliases (`nous-girl`, `nous girl`, `hermes-agent`, etc.) and exposed the names through `ae voices`.
- Updated the open-course template and tiny-voca docs to use the new identities.

## 2.4.0

- Promoted tiny-voca to a Hermes TTS primitive: native `tts.provider: tiny-voca` now points at the installed plugin CLI.
- Added `tts_speak`, `tts_voices`, and `tts_receipts` aliases to the single `ae` tool.
- Added `docs/TINY_VOCA.md` documenting the native provider, voice roles, CLI contract, and receipts.

## 2.3.1

- Refreshed sanitized receipt snapshot to the full 45-entry ledger at release time.
- Added a 1.1 MB looping GIF preview of the free-base walk.
- Added a self-contained WebGL qpos viewer with frame scrubbing, play/pause, camera presets, and live base/COM telemetry.
- Added scripts/export_webgl.py to regenerate the viewer from the URDF and runtime trace.

## 2.3.0

- Made core ops self-contained: `speak`, `voices`, `probe`, `witness`, `gallery`, `physics`, and `studio_sync` no longer require legacy plugins.
- Kept `op=call` as an optional bridge to locally installed legacy plugins.
- Added fresh-clone acceptance harness, CI workflow, video index, and sanitized receipt-chain snapshot.

# Changelog

All notable changes to `hermes-ae` are documented here. Version numbers follow
the plugin version in `plugin.yaml`.

## 2.2.0

- Added the bundled `free_walk` local op (Studio v2.2): mocap-guided, free-base
  walk with a ground plane and foot contact spheres. Forward motion and COM
  trajectory are produced by MuJoCo weld constraints, not prescribed.
- New render pipeline `render_free_walk.py` consuming `physics_free_trace.json`
  (`nq=32` including the floating base) and `free_visemes.json`.
- New free-walk physics trace (`asimov_mocap_physics.xml`) and viseme timeline.
- Output video: `asimov-free-walk-916.mp4` (720x1280, 24 fps, 9 s, 216 frames,
  h264/aac) with QC checks and a `VIDEO://ASIMOV_FREE_WALK_916` receipt.
- New env vars: `HERMES_AE_MESHES`, `HERMES_AE_GALLERY` (see `scripts/ae_paths.py`).

## 2.1.0

- Added the bundled `studio_video` local op (Studio v2.1): fixed-base MuJoCo
  physics trace with 25 PD position actuators plus phoneme-driven visemes.
- New physics-only actuated model (`asimov_1_25dof_physics.xml`, `nu=25`, base
  fixed for capture) and renderer `render_studio_v2.py`.
- Output video: `asimov-studio-v2-916.mp4` with a
  `VIDEO://ASIMOV_STUDIO_V2` receipt recording physics, phoneme hashes, and QC.
- Added `studio_v2_frames` generation and cleanup, gallery regeneration, and
  `gh-pages` publish flow.

## 2.0.0

- Consolidated the separate helper plugins behind a single `ae` tool with an
  `op` enum, replacing direct per-plugin tool calls.
- Added shortcut routing (`SHORTCUTS`) to optional legacy local plugins via a
  lightweight `FakeCtx` loader; no heavy imports at registration time.
- Added `op=call` escape hatch for arbitrary installed plugin/tool pairs.
- Introduced the `HUMAN://ROOT` hash-chained receipt ledger with `status`,
  `receipts`, and `verify` ops.

## 1.x

- Early, per-plugin tools for tiny-voca TTS, ffmpeg rendering/VLC control,
  Asimov speech/video, MuJoCo studio, and robot voice — later superseded by the
  unified `ae` tool in 2.0.0.
