# Results

Every number measured on the machine below. Nothing projected.

## Machine

```
Host    Victus · Windows 11 · git-bash
CPU     Intel i5-13420H · 8 cores (4P+4E) · 12 threads
RAM     32 GB
GPU     RTX 3050 6GB — NOT USED by the walk
Python  3.12.13 · MuJoCo 4.0.1 · ONNX Runtime 1.32.0 · NumPy 2.2.6
```

**The walk runs entirely on CPU.** `doctor` reports `gpu_required: false`.

## Policy

```
Menlo/asimov1-locomotion-0818
831,809 bytes
sha256 47f70691ecd5afda2933b2e6430d2375004c943552284172a2d7b28b84188a0c
input  obs      [1, 78] float32
output actions  [1, 23] float32
```

## Reference reproduction

The published proof, reproduced exactly:

| metric | reference | tinyPython |
|---|---|---|
| duration | 12.0 s | 12.0 s |
| policy ticks | 600 | 600 |
| physics steps | 2400 | 2400 |
| base travel | 4.1868 m | **4.1868 m** |
| COM travel | 4.1743 m | **4.1743 m** |
| min base height | 0.6125 m | **0.6125 m** |
| fall | none | **none** |

`tests/test_tinypython.py::test_walk_reproduces_the_reference` asserts this
within 0.01 m.

## Speed

| run | simulated | wall | realtime factor |
|---|---|---|---|
| 12 s @ vx 0.4 | 12.0 s | 0.96 s | **12.53×** |
| 20 s @ vx 0.45 | 20.0 s | 1.57 s | **12.75×** |
| 8 s @ various | 8.0 s | 0.65–0.66 s | ~12× |

Twenty seconds of humanoid locomotion in under two seconds, on a laptop CPU.

## Command space

All seven verified; `upright` and `obeyed_command` both true unless noted.

| command | x (m) | y (m) | min_z | ok |
|---|---|---|---|---|
| stand (0,0,0) | −0.007 | −0.003 | 0.6121 | ✓ |
| walk vx 0.4 | +2.763 | −0.346 | 0.6125 | ✓ |
| fast vx 0.6 | +4.336 | −0.284 | 0.6116 | ✓ |
| turn wz 0.5 | +0.523 | +2.066 | 0.6121 | ✓ |
| back vx −0.2 | −0.578 | +0.363 | 0.6113 | ✓ |
| strafe vy 0.3 | +0.208 | +1.790 | 0.6118 | ✓ |
| strafe vy −0.3 | −0.404 | −1.894 | 0.6122 | ✓ |

(8 s runs except where noted.)

## Determinism

Same command → identical trace bytes. `test_walk_is_deterministic` runs the
same 4 s walk twice and asserts equal SHA-256.

## The gait, measured

```
foot separation    min 0.217 · max 0.331 · mean 0.301 m
left knee          6.6° → 52.5°    (45.9° swing)
right knee       −51.4° → −9.7°    (41.7° swing)
foot z at peak     −0.565 / −0.580  → 1.5 cm difference
```

**This is a shuffle, not a stride.** The knees flex substantially but the feet
stay near the ground and slide forward. No foot-clearance term appears in the
reward, so the policy never learned to lift its feet.

`test_gait_is_a_shuffle_not_a_stride` pins the knee swing between 30° and 90° so
a future policy change is noticed rather than silently altering the claim.

## Tests

```
14 passed in 6.37s
```

Covering: contract shapes, slot partition, quaternion orthonormality and
degenerate input, absence of any hardware/network path, structured refusal on
missing assets, reference reproduction, determinism, standing/backward/lateral
success, verify recomputing against a lying flag, and the gait observation.

Tests skip cleanly when the policy or MuJoCo is absent.

## The film it produced

`asimov-walk-916.mp4` — the trace rendered by tinyGPU:

```
720 frames · 1,007,041 triangles/frame · RTX 3050 CUDA
raster 70.5 ms/frame · 256.4 s render
audio: voice ✓ world ✓ 22 events · torch false · 0.0% near-silent
gate PASS · lum 23.1 · contrast 46.31 · motion 1.493 · black 0
receipt 6e796c4ffa65308063d873eaaa5cc6583087be2b01d2bd8813f4c8e5e110d3cc
locomotion.source "policy" · policy sha recorded in the film metadata
```

**Defect found and fixed:** that first render's video ended at 30 s while its
audio ran to 71.34 s — the last 41 seconds were a frozen frame. The frame count
had been hand-picked. The harness now derives it from the voice track. See
[WALK-LOOP.md](../docs/WALK-LOOP.md).

## Limits

- Simulation only; no hardware attached.
- The policy is Menlo's; we run it, we did not train it.
- Training randomizations (noise, delays, gain jitter) are not reproduced. The
  viewer's inference contract is matched; the robustness envelope is not.
- One machine; no second-box reproduction.
- Requires the pinned physics MJCF (`nq=30`, `nv=29`).
