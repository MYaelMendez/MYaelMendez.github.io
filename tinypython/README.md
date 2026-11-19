# tinyPython

**A humanoid that walks, in one file.** Motion that emerges from control,
not from a keyframed pose.

```bash
pip install onnxruntime mujoco numpy

tinypython doctor                      # policy + physics present? measured
tinypython walk out.json --vx 0.45     # simulate a walk
tinypython verify out.json             # recompute: did it walk, or fall?
```

No GPU. No compiler. No engine. No ROS. No Isaac. No cloud. No account.

---

## Three efforts, one route

| | |
|---|---|
| **Menlo Research** | trained the locomotion policy and published it openly |
| **Nous Research** | authored Hermes Agent, the runtime that carries intent |
| **#opensourceware** | the claim that open capability composes *downward* |

tinyPython is the third made concrete: **831 KB of someone else's policy plus
~330 lines of ours**, and a humanoid walks on a laptop CPU.

**No institutional endorsement is claimed.** See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

---

## The siblings

| | role | weight | runs on |
|---|---|---|---|
| [tiny-voca](https://github.com/MYaelMendez/tiny-voca) | voice | 4.5M params · 57 MB | CPU |
| [tinyGPU](https://github.com/MYaelMendez/tinyGPU) | pixels | 527 lines · 22.6 KB | NVIDIA CUDA |
| **tinyPython** | **motion** | **~330 lines** | **CPU** |

A robot that speaks, that you can see, that moves under its own control.
Three small routes to three large capabilities.

---

## What makes this different

Every robot video is choreography — someone keyed the poses. Here:

```
78-float observation → ONNX policy → 23 joint targets → PD → MuJoCo contact
                        50 times a second
```

**The base trajectory emerges.** Nothing prescribes where the body goes. It
stays up or it does not.

---

## Measured

RTX 3050 laptop machine, but **the walk uses no GPU** — i5-13420H, 12 threads.

```
12 s at vx 0.4    600 ticks · 2400 steps · +4.1868 m · min_z 0.6125 · no fall
20 s at vx 0.45  1000 ticks · 4000 steps · +7.8696 m · min_z 0.6106 · no fall
wall time         1.57 s for 20 s of walking → 12.75× realtime
```

Command space, all verified:

| command | result | x | y |
|---|---|---|---|
| stand | ok | −0.007 | −0.003 |
| walk vx 0.4 | ok | +2.763 | −0.346 |
| fast vx 0.6 | ok | +4.336 | −0.284 |
| turn wz 0.5 | ok | +0.523 | +2.066 |
| back vx −0.2 | ok | −0.578 | +0.363 |
| strafe vy 0.3 | ok | +0.208 | +1.790 |
| strafe vy −0.3 | ok | −0.404 | −1.894 |

### The gait is a shuffle, not a stride

Measured across the cycle:

```
foot separation    0.217 – 0.331 m
left knee          6.6° → 52.5°   (46° swing)
right knee       −51.4° → −9.7°
foot z difference  1.5 cm         ← the feet barely leave the ground
```

**Nobody rewarded the policy for foot clearance, so it never learned to lift
its feet.** The reward wrote the gait. This is stated rather than hidden
behind a "our robot walks" headline — and there is a test pinning the
observation so a future policy change is noticed.

---

## The contract

From `menloresearch/humanoid-policy-viewer`:

```
obs   78 floats: angvel×0.25, projected gravity, [vx,vy,wz],
                 joint position slots, joint velocity slots×0.1, prev action
act   23 floats: clipped ±10, target = default + 0.25×action
PD    per-joint kp/kd/torque limits, 0.02 s period, 4 substeps of 0.005 s
lag   2 substeps, one-pole target filter α = 0.992105
```

`doctor` reports the policy's SHA-256 so you can confirm you are running the
same weights: `47f70691ecd5afda2933b2e6430d2375004c943552284172a2d7b28b84188a0c`.

---

## Governed by design

**This produces a simulation trace. It is not a command to hardware.**

Every response carries `grants:false`, `executed:false`, `hardware:false`.
No socket is opened, no serial port is touched, no motor is addressed. A test
asserts the source contains no hardware or network path.

The trace is a **plan** a human may inspect, render, and refuse. The policy
layer lives in the æ stack: **https://myaelmendez.github.io/refusal.html**

> The refusal has to belong to the person who owns the robot.

---

## Three bugs found by testing the command space

**1. Success was forward-only.** Standing still and walking backward were
scored failures — inherited from a `base_x > 0.1` test. Standing is a correct
behaviour. Now: *upright AND obeyed the command*.

**2. Obeyed measured only x.** A lateral command moved the robot **+1.79 m in
y** and was scored a failure. Now measures the commanded axis.

**3. `verify` trusted the trace's flag.** Now it recomputes from the geometry.
A test writes `success:false` into a good trace and asserts verify still
reports `ok:true`.

All three were **my measurement, not the policy**. The robot was right every
time.

---

## Limits, stated

- **Simulation only.** No physical robot is attached.
- **The policy is Menlo's.** We run it; we did not train it.
- **Training randomizations not reproduced** — noise, delays, gain jitter. The
  viewer's inference contract is matched exactly; the robustness envelope is not.
- **One machine.** No second-box reproduction.
- Requires the pinned physics MJCF (`nq=30`, `nv=29`). A different model is a
  structured refusal, not a silent mismatch.

---

## The full loop

```
tinyPython → tinyGPU → gate → receipt → publish
  physics     pixels    verdict   proof     surface
```

See [WALK-LOOP.md](../docs/WALK-LOOP.md) for the method, including the four
defects found by measuring rather than looking.

---

Apache-2.0 · `HUMAN://ROOT` · `>_æ://` · [@yaelmendez](https://x.com/yaelmendez)
