"""Generate a real MuJoCo qpos trace for Asimov Studio v2.1.

The actuated MJCF has 25 position actuators and a fixed base for capture.
A walking target is applied through d.ctrl; the qpos trace is sampled at 24 Hz
for a 9-second clip (216 frames). Joint dynamics are genuine MuJoCo PD.
"""
from ae_paths import ANIM, MESHES, BUNDLED_URDF, BUNDLED_XML, ensure_runtime
ensure_runtime()

import json, math, hashlib
from pathlib import Path
import numpy as np
import mujoco

MJCF = str(BUNDLED_XML / 'asimov_1_25dof_physics.xml')
OUT = ANIM / 'physics_trace.json'
FPS, SECS, DT = 24, 9, 0.005


def targets(t):
    phase = t * 2 * math.pi / 2.0
    ramp = min(1.0, t / 1.2, (SECS - t) / 1.2)
    s = math.sin(phase)
    g = {}
    g['left_hip_pitch_joint'] = 0.48 * s * ramp
    g['left_hip_roll_joint'] = 0.35 * s * ramp
    g['left_knee_joint'] = 0.60 * max(0.0, -math.sin(phase - 0.4)) * ramp
    g['left_ankle_pitch_joint'] = 0.12 * math.sin(phase - 1.0) * ramp
    g['right_hip_pitch_joint'] = -0.48 * s * ramp
    g['right_hip_roll_joint'] = -0.35 * s * ramp
    g['right_knee_joint'] = -0.60 * max(0.0, math.sin(phase - 0.4)) * ramp
    g['right_ankle_pitch_joint'] = -0.12 * math.sin(phase - 1.0) * ramp
    g['left_shoulder_pitch_joint'] = -0.24 * s * ramp
    g['left_shoulder_roll_joint'] = -0.35 * s * ramp
    g['right_shoulder_pitch_joint'] = 0.24 * s * ramp
    g['right_shoulder_roll_joint'] = 0.35 * s * ramp
    g['left_elbow_joint'] = 0.10 * ramp
    g['right_elbow_joint'] = 0.10 * ramp
    g['waist_yaw_joint'] = 0.05 * math.sin(phase * 0.5) * ramp
    g['neck_pitch_joint'] = 0.02 * math.sin(t * 3) * ramp
    g['neck_yaw_joint'] = 0.07 * math.sin(t * 0.8) * ramp
    return g


def main():
    m = mujoco.MjModel.from_xml_path(MJCF)
    d = mujoco.MjData(m)
    mujoco.mj_forward(m, d)
    names = [m.joint(i).name for i in range(m.njnt)]
    refs = [float(m.joint(i).qpos0[0]) for i in range(m.njnt)]
    idx = {n: i for i, n in enumerate(names)}
    q0 = np.array(d.qpos, dtype=float)
    qpos_frames, qvel_frames = [], []
    next_t = 0.0
    total_steps = int(round(SECS / DT))
    for step in range(total_steps + 1):
        t = step * DT
        if t >= next_t - 1e-9 and len(qpos_frames) < FPS * SECS:
            qpos_frames.append([round(float(x), 6) for x in d.qpos])
            qvel_frames.append([round(float(x), 6) for x in d.qvel[:min(len(d.qvel), 12)]])
            next_t += 1.0 / FPS
        if step == total_steps:
            break
        g = targets(t)
        ctrl = np.zeros(m.nu, dtype=float)
        for name, val in g.items():
            if name in idx and idx[name] < m.nu:
                ctrl[idx[name]] = refs[idx[name]] + val
        d.ctrl[:] = ctrl
        mujoco.mj_step(m, d)
    qarr = np.asarray(qpos_frames)
    qend = np.array(d.qpos, dtype=float)
    finite = bool(np.isfinite(qarr).all())
    maxabs = float(np.abs(qarr).max()) if finite else 0.0
    out = {
        'success': finite and len(qpos_frames) == FPS * SECS and maxabs < 3.2,
        'engine': 'MuJoCo ' + mujoco.__version__,
        'model': 'asimov_1_25dof_actuated',
        'mjcf_sha256': hashlib.sha256(Path(MJCF).read_bytes()).hexdigest(),
        'nq': int(m.nq), 'nv': int(m.nv), 'nu': int(m.nu),
        'timestep': float(m.opt.timestep), 'fps': FPS, 'seconds': SECS,
        'frames': len(qpos_frames), 'joint_names': names,
        'joint_refs': [round(float(x), 6) for x in refs],
        'qpos_start': [round(float(x), 6) for x in q0],
        'qpos_end': [round(float(x), 6) for x in qend],
        'max_abs_qpos': round(maxabs, 6),
        'finite': finite,
        'base_fixed_for_capture': True,
        'note': '25 position actuators; base fixed; forward root path prescribed by renderer',
        'qpos': qpos_frames,
        'qvel_sample': qvel_frames,
    }
    OUT.write_text(json.dumps(out, separators=(',', ':')))
    print(json.dumps({k: v for k, v in out.items() if k not in ('qpos','qvel_sample')}))


if __name__ == '__main__':
    main()
