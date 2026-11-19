# rtx-asimov

**The real Menlo Asimov CAD, rasterised on your RTX. No OpenGL, no compiler, no engine.**

```
26 CAD links · 25 joints · 1,007,041 triangles per frame
~31 ms/frame on an RTX 3050 6GB laptop
```

## Why this exists

On many Optimus laptops the NVIDIA OpenGL driver is never registered — OpenGL
silently falls back to the integrated GPU, and the discrete card sits idle. This
renderer does not use OpenGL at all. MuJoCo is not needed either: the URDF
supplies forward kinematics, CuPy supplies the pixels.

That means it runs where a normal GPU renderer cannot, and it reproduces on any
machine with CUDA rather than depending on a driver preference a user would
never know to set.

## Install

```bash
pip install cupy-cuda13x pillow numpy
# ffmpeg must be on PATH (or set ASIMOV_FFMPEG=<dir containing ffmpeg>)
```

Use the CuPy wheel matching your CUDA version (`cupy-cuda12x`, `cupy-cuda13x`, …).

## Run

```bash
python fetch_model.py            # 26 meshes + urdf.json -> ./model/
python rtx_asimov.py --out film.mp4 --seconds 8
```

Three files. That is the whole renderer:

| file | role |
|---|---|
| `rtx_raster.py` | the CUDA rasteriser — depth + shade kernels |
| `rtx_asimov.py` | URDF forward kinematics, scene assembly, encode |
| `fetch_model.py` | fetch the authoritative geometry, hash-verified |

## What you get

- **Real CAD.** Every triangle comes from Menlo Research's own STL files,
  fetched from `menloresearch/asimov-1`. Not collision proxies, not point
  samples, not a simplified stand-in.
- **Deterministic.** Same model and pose produce byte-identical frames. Verified
  across two independent directories: `27628f6615e6cc6f0a0cff5e`.
- **Hash-verified assets.** `model/manifest.json` records a SHA-256 for every
  file, so a corrupted download is caught rather than rendered.

## Honest performance

**~31 fps for a million triangles is slow for this GPU.** A hardware rasteriser
would do 500–2000 fps. This kernel is one thread per triangle with a serial
bounding-box loop, no backface culling, no tile binning, no hierarchical Z. It is
a software rasteriser, and it performs like one.

The point is not speed. The point is that it **runs at all** where OpenGL is
blocked, with **zero build dependency**, and produces **identical pixels** for
anyone who runs it.

Measured on: i5-13420H, 32 GB, RTX 3050 6 GB (cc 8.6), CUDA 13.3, Windows 11.
Raster 31 ms/frame; total ~330 ms/frame including URDF kinematics, NumPy
transforms of 1M triangles, and PNG writes. The GPU is not the bottleneck.

## Not verified

- Tested on one machine. A second physical box has not run it.
- Linux and macOS font/ffmpeg paths are written but unexercised.
- No shadows, no floor plane, no face screen. It is a clean clay render.

## Provenance

Geometry: **Menlo Research**, `menloresearch/asimov-1`,
`sim-model/asimov_1_25dof/meshes/`. No institutional endorsement is claimed.
URDF link/joint map: `ffmpeg-asimov/urdf.json` from the æ OpenSourceWare harness.

The tool is open. The authority is not: nothing here grants a robot permission
to move. `HUMAN://ROOT` holds the signature.

## License

MIT for this renderer. The Menlo CAD carries its own upstream license — see
`menloresearch/asimov-1`.
