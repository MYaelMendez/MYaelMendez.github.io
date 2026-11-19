# tinyGPU

**A complete GPU robot renderer in one file.** The sibling of
[tiny-voca](https://github.com/MYaelMendez/tiny-voca).

tiny-voca proved a 4.5M-parameter model can do what "requires" a cloud TTS.
tinyGPU proves a laptop GPU can render what "requires" a workstation: real CAD,
a million triangles a frame, deterministic pixels, no cloud. **527 lines,
22.6 KB, two files.**

```
pip install cupy-cuda13x pillow numpy      # two deps (numpy comes with cupy)
# ffmpeg on PATH

python tinygpu.py doctor                   # does my GPU work? measured
python tinygpu.py fetch                    # Menlo's Asimov CAD, hash-verified
python tinygpu.py render out.mp4           # a film, on your card
python tinygpu.py verify out.mp4           # did it come out right?
```

## Measured on an RTX 3050 6GB Laptop

```
device        NVIDIA GeForce RTX 3050 6GB Laptop GPU
compute       8.6 · 20 SMs · 1.18 GHz · 6.0 TFLOPS FP32 · 6.44 GB
matmul        21.51 ms · 798.7 GFLOPS
geometry      26 CAD links · 25 joints · 1,007,041 triangles/frame
raster        76 ms/frame
96 frames     39.9 s total
OpenGL        none
```

That card is roughly **0.6% of an H100's compute and 8% of its memory**. It
renders a million triangles a frame anyway.

## Why this exists

On an Optimus laptop the NVIDIA OpenGL ICD is often **not registered**, so
MuJoCo's GL silently falls back to the Intel iGPU. Four levers to force OpenGL
onto the discrete card all failed. CUDA reaches it directly.

The capability was always there. Only the **route** was missing.

That is the whole #opensourceware claim: **open capability composes downward.**
One person with a laptop assembles what used to require an institution — and
the piece they add is the one the institution structurally cannot supply.

## What is tiny about it

| | tiny-voca | tinyGPU |
|---|---|---|
| weight | 4.5M params · 57 MB | **527 lines · 22.6 KB** |
| runs on | CPU | your NVIDIA card |
| deps | onnxruntime | cupy, pillow, numpy |
| cloud | none | none |
| account | none | none |
| compiler | none | none |

tinyGPU vendors **no CAD**. `fetch` pulls Menlo Research's meshes from their
public repo and writes a SHA-256 manifest. Duplicating 100 MB of someone else's
work would drift from it.

## Determinism

Same model + same poses → **byte-identical frames**. The depth test packs depth
and triangle id into a single `uint64` `atomicMin`, so there is no
read-modify-write race between the depth and colour passes.

## Honesty

- **Simulation only.** No physical robot is attached.
- A pose trace is **not a signed command**. Nothing here grants authority.
- `doctor` measures your machine; it does not assume. If CUDA is missing it
  says so and names the fix.
- `verify` reports decode and geometry. It does **not** judge visual quality.
- CAD authored by **Menlo Research**. No institutional endorsement is claimed.

## Four bugs worth knowing

Each was the same class — inventing an API instead of reading it:

1. The renderer class is `RtxRenderer`, not `Raster`.
2. `urdf.json` uses `links[name]['mesh']`, and `joints` is a **list**, not a dict.
3. A loop variable named `n` shadowed the normals array. Twice.
4. The shade kernel wants colours in **0–1**. Passing 0–255 saturates every
   pixel to white — producing a *valid MP4 with correct geometry* that looks
   like a flat silhouette.

**A passing pipeline is not a right picture.** Look at the frame.

## License

Apache-2.0 · `HUMAN://ROOT` · `>_æ://`
