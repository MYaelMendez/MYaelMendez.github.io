# Architecture

## Overview

`hermes-ae` is a single-tool plugin. `plugin.yaml` declares exactly one tool,
`ae`, registered by `__init__.py`. The handler is a dispatcher: it reads an `op`
from the argument dict, routes it, writes one `HUMAN://ROOT` receipt, and
returns a JSON string of the form:

```json
{"success": true, "op": "...", "result": {...}, "receipt": {...}}
```

Registration is cheap: legacy plugins are loaded lazily on first use, and heavy
dependencies (MuJoCo, ONNX, Pillow) are imported only inside the bundled scripts.

## Dispatch map

`op` values fall into four groups:

1. **Built-ins** — `status`, `receipts`, `verify`, `ops`. These inspect plugin
   state and the receipt ledger.
2. **`call`** — direct invocation of `plugin`/`tool` (`op=call`, with `plugin`
   and `tool` arguments), the general escape hatch.
3. **Shortcuts** (`SHORTCUTS`) — named aliases such as `speak`, `render`, `vlc`,
   `robot_say`, `studio`, `physics`, `chimera_speak`, mapped to a plugin/tool pair
   in an optional legacy plugin directory. A missing plugin yields a structured
   error listing what is available.
4. **Bundled local ops** (`LOCAL_OPS`) — `studio_video` and `free_walk`. These
   run a Python script in `scripts/` as a subprocess with a JSON argument blob
   and a generous timeout (1500 s), parsing the single JSON line it prints.

Legacy plugin loading uses a `FakeCtx` that implements `register_tool`,
`register_command`, `register_skill`, and `register_hook`; modules are loaded by
file path from `HERMES_AE_PLUGINS/<plugin>/__init__.py` and cached after first use.

## Video pipelines

Both bundled ops share the same staged flow and print one JSON summary line:

```text
TTS (tiny-voca) → physics trace (MuJoCo) → visemes (dizione) → render (Pillow)
→ ffmpeg encode → QC (ffprobe + volumedetect + frame brightness) → receipt → publish
```

### studio_video (Studio v2.1)

- Script: `scripts/studio_video.py`.
- Physics: `scripts/physics_trace.py` using `model/xml/asimov_1_25dof_physics.xml`
  — a physics-only MJCF with 25 PD position actuators, **base fixed** for
  capture, sampled at 24 Hz over 9 s (216 frames).
- Mouth: `scripts/visemes.py` → `visemes.json`.
- Renderer: `scripts/render_studio_v2.py` — deterministic STL point-cloud painter
  with prescribed forward approach and ground sweep.
- Output: `asimov-studio-v2-916.mp4`.
- Receipt action: `VIDEO://ASIMOV_STUDIO_V2`.

### free_walk (Studio v2.2)

- Script: `scripts/free_walk_video.py`.
- Physics: `scripts/physics_free_trace.py` using
  `model/xml/asimov_mocap_physics.xml` — floating base, ground plane, and foot
  contact spheres. Gait targets drive 25 actuators; base and COM trajectories
  are solved by MuJoCo (`nq=32` including the base). No prescribed zoom.
- Mouth: `scripts/visemes_free.py` → `free_visemes.json`.
- Renderer: `scripts/render_free_walk.py` — fixed camera; the robot genuinely
  translates across the frame.
- Output: `asimov-free-walk-916.mp4`.
- Receipt action: `VIDEO://ASIMOV_FREE_WALK_916`.

Both outputs are 720x1280, 24 fps, 9 s, 216 frames, h264 video + aac audio.
QC verifies codecs, dimensions, frame count, duration, audio levels, and frame
brightness. Frame caches are removed after a successful run.

## Model manifests

`model/` ships only text manifests:

- `model/urdf.json` — the 25-DOF link/joint map (`asimov_1_25dof`).
- `model/urdf/asimov_1_25dof.urdf` and `asimov_1_25dof_ae.urdf`.
- `model/xml/asimov_1_25dof.xml`, `asimov_1_25dof_actuated.xml`,
  `asimov_1_25dof_physics.xml`, `asimov_free_physics.xml`,
  `asimov_mocap_physics.xml`.

Binary STL meshes and finished videos are intentionally not in the repository;
they live under the configured runtime paths (see INSTALL.md).

## Path configuration

`scripts/ae_paths.py` centralizes all paths. Every location has an environment
override with a default under `$HERMES_HOME`, so the plugin stays portable:

| Variable | Purpose | Default |
| --- | --- | --- |
| `HERMES_HOME` | Hermes install root | `~/.hermes` |
| `HERMES_AE_HOME` | Runtime root | `$HERMES_HOME/ae` |
| `HERMES_AE_ANIM` | Animation/frame artifacts | `$HERMES_AE_HOME/asimov-anim` |
| `HERMES_AE_MODEL` | Runtime model dir | `$HERMES_AE_HOME/model` |
| `HERMES_AE_MESHES` | STL mesh dir | `$HERMES_AE_MODEL/meshes` |
| `HERMES_AE_GALLERY` | Gallery repo checkout | `$HERMES_AE_HOME/gallery` |
| `HERMES_AE_LEDGER` | Receipt ledger file | `$HERMES_HOME/ae-receipts.jsonl` |
| `HERMES_AE_PLUGINS` | Legacy plugin dir (dispatcher) | `$HERMES_HOME/plugins` |
| `HERMES_AE_PYTHON` | Python used for subprocesses | `/usr/local/bin/python3` |

`ensure_runtime()` creates the runtime directories on demand. Bundled manifests
are resolved relative to the repository (`model/`), independent of these paths.

## Publishing

With `publish: true` (the default), a finished MP4 is copied into the gallery
repo, `generate_gallery.py` rebuilds `videos.html`, and the result is committed
and pushed to the `gh-pages` branch. The published raw URL form is documented in
the README. Passing `publish: false` skips publishing while still producing,
checking, and receipting the local video.
