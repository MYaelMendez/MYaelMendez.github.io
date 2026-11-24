# Third-Party Notices

This file records the components used by `hermes-ae` that are not covered by
the plugin's MIT license.

## Asimov-1 robot model

- **Source:** [menloresearch/asimov-1](https://github.com/menloresearch/asimov-1)
- **License:** CERN Open Hardware Licence Version 2 — Strongly Reciprocal
  (**CERN-OHL-S-2.0**).
- This repository includes XML/URDF kinematic and dynamics manifests derived
  from the Asimov-1 model (`model/xml/`, `model/urdf/`, `model/urdf.json`) for
  the 25-DOF `asimov_1_25dof` variant. Binary STL mesh assets are **not**
  included and must be supplied separately in `HERMES_AE_MESHES`.
- The model remains subject to its original CERN-OHL-S-2.0 terms. The MIT
  license in `LICENSE` applies only to the `hermes-ae` plugin code.

## Runtime dependencies

The following are used at runtime but are not vendored in this repository and
remain under their own licenses:

- **MuJoCo** — physics engine (capture uses MuJoCo 4.0.1).
- **NumPy** — numerical arrays.
- **Pillow** — frame/mesh rasterization and image QC.
- **ONNX Runtime** — inference backend for tiny-voca TTS.
- **dizione** — phonemizer used for viseme timelines.
- **tiny-voca** — self-hosted English TTS weights (voices `F2` / `M2`, 24 kHz).
- **FFmpeg / FFprobe** — encoding, muxing, and QC.
- **Git** — gallery publishing to the `gh-pages` branch.

Refer to each project's own distribution for its license text. No assertion is
made here about the licenses of these external components beyond what their
respective authors publish.
