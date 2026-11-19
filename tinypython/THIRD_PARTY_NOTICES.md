# Third-party notices

tinyPython is a small route to other people's large work. **No institutional
endorsement is claimed from Menlo Research, Nous Research, or DeepMind.**

---

## Menlo Research — the policy and the robot

The locomotion policy is **`Menlo/asimov1-locomotion-0818`**, trained and
published by Menlo Research. tinyPython does not train anything; it runs their
831,809-byte ONNX file.

- https://huggingface.co/Menlo/asimov1-locomotion-0818
- sha256 `47f70691ecd5afda2933b2e6430d2375004c943552284172a2d7b28b84188a0c`
- https://github.com/menloresearch/asimov-1 — the humanoid CAD
- https://github.com/menloresearch/humanoid-policy-viewer — the inference
  contract this file implements (observation layout, action scaling, PD gains,
  action lag, target filter)
- https://docs.menlo.ai/asimov/1/overview

The pinned physics MJCF (`asimov_1_policy_physics.xml`, `nq=30`, `nv=29`) derives
from Menlo's published model. Consult upstream for the licence governing these
assets. They are **not redistributed here** — point `TINYPYTHON_ASSETS` at your
own copy.

Menlo's `AGENTS.md` states that the guard belongs in user code. tinyPython
simulates; it does not act.

---

## MuJoCo — the physics engine

Apache-2.0, Copyright DeepMind Technologies Limited.
https://github.com/google-deepmind/mujoco

Used unmodified via its Python bindings. No MuJoCo source is vendored.

---

## ONNX Runtime

MIT License, Copyright Microsoft Corporation.
https://github.com/microsoft/onnxruntime

Used unmodified, CPU execution provider only.

---

## NumPy

BSD-3-Clause. https://github.com/numpy/numpy

---

## Nous Research — the runtime

**Hermes Agent** (Nous Research) orchestrates the film pipeline this package
plugs into. tinyPython does **not** depend on it — it is a standalone CLI.
`HERMES_HOME` is read only to locate an existing asset copy.

- https://github.com/NousResearch/hermes-agent

---

## The æ stack

The policy gate, the receipt chain, and the film harnesses are part of the
æ / #opensourceware stack by Yæl Méndez, Apache-2.0.

- https://myaelmendez.github.io/refusal.html

---

## What is original here

| Component | Origin |
|---|---|
| `tinypython.py` — CLI, doctor/walk/verify, asset resolution | **original** |
| Success criterion: *upright AND obeyed the commanded axis* | **original** |
| `verify` recomputing from geometry rather than trusting a flag | **original** |
| The gait measurement and its regression test | **original** |
| Inference contract (obs layout, gains, lag, filter) | Menlo Research |
| The policy weights | Menlo Research |
| Physics, inference, arrays | MuJoCo, ONNX Runtime, NumPy |
