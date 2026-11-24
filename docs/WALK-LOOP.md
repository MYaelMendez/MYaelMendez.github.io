# THE WALK LOOP — how a policy-driven robot film is made

This is the **method**, not the artifact. Anyone with the three packages can
reproduce the film byte for byte. Every number below was measured.

```
tinyPython  →  tinyGPU  →  gate  →  receipt  →  publish
  physics       pixels     verdict    proof       surface
```

The difference from every other robot film: **the motion is not keyframed.**
A neural policy produces joint targets, MuJoCo resolves contact, and the base
trajectory *emerges*. Nobody authored where the body goes.

---

## The three packages

| | role | weight | runs on |
|---|---|---|---|
| **tiny-voca** | voice | 4.5M params · 57 MB | CPU |
| **tinyGPU** | pixels | 527 lines · 22.6 KB | NVIDIA CUDA |
| **tinyPython** | motion | ~330 lines | CPU |

None requires a compiler, an engine, a cloud account, or a credential.

---

## Step 1 — produce the motion

```bash
tinypython doctor                                   # policy + physics present?
tinypython walk walk.json --vx 0.45 --duration 20   # simulate
tinypython verify walk.json                         # recompute, don't trust the flag
```

Measured:

```
1000 policy ticks · 4000 physics steps
7.8696 m travel · min_z 0.6106 m · no fall
1.57 s wall → 12.75× realtime, CPU only
policy  Menlo/asimov1-locomotion-0818
sha256  47f70691ecd5afda2933b2e6430d2375004c943552284172a2d7b28b84188a0c
```

The trace carries `qpos` (30 floats: 7 free-joint + 23 joints), `base`, `com`,
the command, and the policy hash. **It is a plan, not a command.** `grants:false`,
`executed:false`, `hardware:false`.

## Step 2 — write the spec

The spec commands the film. **Never edit the renderer to change a video.**

```json
{"title": "asimov://walk",
 "tagline": "POLICY-DRIVEN LOCOMOTION · NOT KEYFRAMED",
 "texture": "room_cold",
 "scenes": [{"kicker": "01 · ...", "speak": "...",
             "speaker": "hermes", "voice": "M2", "state": "SPEAKING"}]}
```

## Step 3 — render

```bash
python rtx_asimov.py --out film.mp4 \
  --trace walk.json --scenes spec.json --texture room_cold \
  --model-dir ./model --frames 720 --fps 24
```

`--trace` replaces the synthetic gesture with the policy's poses. Voice and
world are a **stage**, not an afterthought: the harness synthesises each scene,
derives the frame count from the audio, and mixes a sound world under it.

## Step 4 — gate

```bash
python vidæo.py verify film.mp4
```

Thresholds are never lowered to pass. Fix the scene.

## Step 5 — publish

```bash
python kanban_push.py push --task <name> --branch gh-pages
```

Never bare `git push` — concurrent agents collide.

---

## Four defects found by measuring, not by looking

Each was caught by a check aimed at the **thing**, not a proxy for it.

**1. The camera looked down the walking axis.** The robot walks along +X and
the camera sat on +X, so the stride went into the lens and read as standing
still. The joints were correct the whole time. Fix: side-on camera for trace
mode. *A correct pose can be an invisible pose.*

**2. The gait is a shuffle, not a stride.** Measured across the cycle:

```
foot separation   0.217 – 0.331 m
left knee         6.6° → 52.5°   (46° swing)
right knee      -51.4° → -9.7°
foot z difference 1.5 cm         ← feet barely leave the ground
```

Nobody rewarded the policy for foot clearance, so it never learned to lift its
feet. **The reward wrote the gait.** The film says this out loud rather than
claiming a human-like walk.

**3. Video ended 41 s before the audio.** 720 frames at 24 fps is 30 s; the ten
scenes' narration totals 71.34 s. The last 41 seconds were a frozen frame under
continuing voice. Root cause: the frame count was hand-picked. Fix: the harness
now **derives frames from the voice track** and extends the picture to match.
*Attention does not survive a pivot; stages do.*

**4. An invented overlay function.** The fix for #3 called `_overlay(...)`,
which does not exist. Fifth invented API of the session. Grep the definition
before calling it.

---

## Verification checklist

Before calling a film done:

- [ ] `ffprobe` video duration **equals** audio duration
- [ ] decoded frame count equals intended frame count
- [ ] gate PASS with the thresholds unchanged
- [ ] near-silent windows ≈ 0% (a speaking robot in a silent room is still mute)
- [ ] a frame inspected **at delivery scale**, cropped to the subject
- [ ] `locomotion.source == "policy"` and the policy sha recorded
- [ ] receipt written; push recorded through `kanban_push.py`

---

## What this loop does not do

- **No hardware.** No serial port, no motor, no socket. A trace is a plan.
- **No training.** The policy is Menlo's; we run it, we did not train it.
- **No face tablet** in the RTX path — the head is a plain block.
- **One machine.** No second-box reproduction yet.

> The refusal has to belong to the person who owns the robot.
