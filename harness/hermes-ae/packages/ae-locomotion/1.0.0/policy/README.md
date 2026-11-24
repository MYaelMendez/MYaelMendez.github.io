---
library_name: asimov
pipeline_tag: robotics
license: bsd-3-clause
---

# Asimov 1 locomotion policy checkpoint

- Basic velocity-commanded locomotion policy for Asimov 1, trained in Isaac Lab with PPO and adversarial motion priors (AMP).
- `policy.onnx` is the exported policy for inference, producing joint-position actions.
- `agent.yaml` records the actor-critic and AMP training settings, including the motion data configuration.
- `env.yaml` records the simulation and locomotion task settings, including observations, actions, commands, and rewards.
- Training and evaluation code: [menloresearch/isaac_asimov](https://github.com/menloresearch/isaac_asimov).

## How to run

Run the policy in a browser simulation of Asimov 1 with
[humanoid-policy-viewer](https://github.com/menloresearch/humanoid-policy-viewer).
It needs Node, git and bash, and no GPU:

```bash
git clone https://github.com/menloresearch/humanoid-policy-viewer
cd humanoid-policy-viewer
npm run hf Menlo/asimov1-locomotion-0818
```

This downloads the policy, starts the viewer and opens it in your browser.
Drive the robot with the velocity sliders, push it, or run the benchmark suite.

## Inputs and outputs

- **Input:** 78 values at 50 Hz: base angular velocity, projected gravity,
  velocity command (`vx, vy, wz`), joint positions and velocities, and the
  previous action. All of these are available on the real robot.
- **Output:** 23 joint position actions (legs, waist and arms; the neck is not
  driven). Each target is `default_joint_pos + action_scale * action`, with
  both values in `env.yaml`.
- Trained in Isaac Lab (PhysX); the viewer simulates it in MuJoCo.

The full observation order and joint list are in the viewer's
[supported policies](https://github.com/menloresearch/humanoid-policy-viewer/blob/main/docs/huggingface.md#supported-policies)
doc.
