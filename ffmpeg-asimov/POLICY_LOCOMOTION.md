# Policy-driven Asimov locomotion

The gap is filled. Asimov no longer needs a mocap-guided weld to walk: the
official Menlo locomotion policy runs as a governed harness inside our MuJoCo
stack.

```text
HUMAN://ROOT → ae → ONNX policy → 23 joint targets → MuJoCo → receipt
```

## What changed

| Before | After |
|---|---|
| `physics_free_trace.json`, mocap weld constraints | `physics_policy_trace.json`, ONNX policy at 50 Hz |
| Base trajectory prescribed by reference | Base trajectory emerges from PD control + ground contact |
| “mocap-guided, not autonomous” caveat | Policy-driven locomotion, still simulation-only |

## Verified contract

- Policy: `Menlo/asimov1-locomotion-0818`, SHA-256 `47f70691…88a0c`.
- Input: 78 floats — angular velocity ×0.25, projected gravity, `[vx, vy, wz]`,
  joint position slots, joint velocity slots ×0.1, previous raw action.
- Output: 23 joint-position actions, clipped to ±10, then
  `target = default + 0.25 × action`.
- Control: 0.02 s policy period, 4 MuJoCo substeps of 0.005 s.
- PD: per-joint `kp`, `kd`, and torque limits from `env.yaml`.
- Action lag: 2 substeps; one-pole target filter α ≈ 0.992105.

## Verified run

| Metric | Result |
|---|---|
| Duration | 12.000 s |
| Policy ticks | 600 |
| MuJoCo steps | 2400 |
| Base travel | +4.1868 m |
| COM travel | +4.1743 m |
| Minimum base height | 0.6125 m |
| Fall | none |
| Video | `asimov-policy-walk-916.mp4`, 720×1280, 24 fps, H.264+AAC |

## Ops

```json
{"op": "policy_locomotion", "duration": 12, "vx": 0.4}
{"op": "policy_walk", "publish": true}
```

## Limits

- This is simulation, not hardware deployment.
- The policy viewer's training randomizations (noise, delays, gain jitter) are
  not reproduced; the exact viewer inference contract is.
- Visual rendering uses the official Asimov STLs through the URDF transform
  tree; the physics loop uses a mesh-stripped MJCF to stay within memory.
- No institutional endorsement from Nous Research or Menlo Research is claimed.

## Sources

- https://docs.menlo.ai/asimov/1/overview
- https://github.com/menloresearch/asimov-1
- https://github.com/menloresearch/humanoid-policy-viewer
- https://huggingface.co/Menlo/asimov1-locomotion-0818
- https://github.com/menloresearch/asimov-mjlab
