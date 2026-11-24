"""Free-base MuJoCo trace for Studio v2.2.

Physics-only model with ground plane and foot contact spheres; 25 PD
actuators, floating base, no mesh assets. Gait targets drive the actuators;
the base and COM trajectories are produced by MuJoCo, not prescribed.
"""
from ae_paths import ANIM, MESHES, BUNDLED_URDF, BUNDLED_XML, ensure_runtime
ensure_runtime()

import json, math, hashlib
from pathlib import Path
import numpy as np
import mujoco

MJCF = str(BUNDLED_XML / 'asimov_mocap_physics.xml')
OUT = ANIM / 'physics_free_trace.json'
FPS, SECS, DT = 24, 9, 0.005


def targets(t):
    phase = t * 2 * math.pi / 2.0
    ramp = min(1.0, t / 1.2, (SECS - t) / 1.2)
    s = math.sin(phase)
    g = {}
    g['left_hip_pitch_joint'] = 0.32 * s * ramp
    g['left_hip_roll_joint'] = 0.14 * s * ramp
    g['left_knee_joint'] = 0.36 * max(0.0, -math.sin(phase - 0.4)) * ramp
    g['left_ankle_pitch_joint'] = 0.10 * math.sin(phase - 1.0) * ramp
    g['right_hip_pitch_joint'] = -0.32 * s * ramp
    g['right_hip_roll_joint'] = -0.14 * s * ramp
    g['right_knee_joint'] = -0.36 * max(0.0, math.sin(phase - 0.4)) * ramp
    g['right_ankle_pitch_joint'] = -0.10 * math.sin(phase - 1.0) * ramp
    g['left_shoulder_pitch_joint'] = -0.18 * s * ramp
    g['left_shoulder_roll_joint'] = -0.14 * s * ramp
    g['right_shoulder_pitch_joint'] = 0.18 * s * ramp
    g['right_shoulder_roll_joint'] = 0.14 * s * ramp
    g['waist_yaw_joint'] = 0.04 * math.sin(phase * 0.5) * ramp
    g['neck_pitch_joint'] = 0.015 * math.sin(t * 3) * ramp
    g['neck_yaw_joint'] = 0.05 * math.sin(t * 0.8) * ramp
    return g


def main():
    m = mujoco.MjModel.from_xml_path(MJCF)
    d = mujoco.MjData(m)
    mujoco.mj_forward(m, d)
    # actuator order -> joint dof address and ref
    act = []
    for a in range(m.nu):
        jn = m.actuator(a).name[4:]
        jid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_JOINT, jn)
        qadr = int(m.joint(jid).qposadr[0])
        act.append((jn, qadr, float(m.joint(jid).qpos0[0]), int(m.joint(jid).dofadr[0])))
    ctrl_names = [a[0] for a in act]
    refs = np.asarray([a[2] for a in act], float)
    qpos_frames, com_frames, base_frames = [], [], []
    next_t = 0.0
    total_steps = int(round(SECS / DT))
    min_z = 1e9
    for step in range(total_steps + 1):
        t = step * DT
        mujoco.mj_comPos(m, d)
        com = np.array(d.subtree_com[0], dtype=float)
        if t >= next_t - 1e-9 and len(qpos_frames) < FPS * SECS:
            qpos_frames.append([round(float(x), 6) for x in d.qpos])
            com_frames.append([round(float(x), 6) for x in com])
            base_frames.append([round(float(x), 6) for x in d.qpos[:7]])
            min_z = min(min_z, float(d.qpos[2]))
            next_t += 1.0 / FPS
        if step == total_steps:
            break
        u = min(1.0, t / SECS)
        x = 0.45 * (3*u*u - 2*u*u*u)
        d.mocap_pos[0] = [x, 0.0, 0.63]
        d.mocap_quat[0] = [1.0, 0.0, 0.0, 0.0]
        g = targets(t)
        ctrl = refs.copy()
        for name, val in g.items():
            if name in ctrl_names:
                i = ctrl_names.index(name)
                ctrl[i] = refs[i] + val
        d.ctrl[:] = ctrl
        mujoco.mj_step(m, d)
        if not np.isfinite(d.qpos).all():
            break
    q = np.asarray(qpos_frames)
    com = np.asarray(com_frames)
    base = np.asarray(base_frames)
    ok = bool(np.isfinite(q).all() and len(q) == FPS * SECS and min_z > 0.25)
    out = {
        'success': ok, 'engine': 'MuJoCo ' + mujoco.__version__,
        'model': 'asimov_mocap_physics', 'mjcf_sha256': hashlib.sha256(Path(MJCF).read_bytes()).hexdigest(),
        'nq': int(m.nq), 'nv': int(m.nv), 'nu': int(m.nu),
        'timestep': float(m.opt.timestep), 'fps': FPS, 'seconds': SECS,
        'frames': len(q), 'joint_names': ctrl_names, 'joint_refs': [round(float(x),6) for x in refs],
        'base_fixed': False, 'mocap_guided': True,
        'mocap_path_x_m': 0.45,
        'base_start': base[0].tolist(), 'base_end': base[-1].tolist(),
        'com_start': com[0].round(6).tolist(), 'com_end': com[-1].round(6).tolist(),
        'com_advance_x': round(float(com[-1,0]-com[0,0]), 6),
        'com_advance_y': round(float(com[-1,1]-com[0,1]), 6),
        'min_base_z': round(float(min_z), 6),
        'finite': bool(np.isfinite(q).all()),
        'note': 'mocap-guided floating base + ground contact; base trajectory solved by MuJoCo weld constraints, not written into qpos',
        'qpos': qpos_frames, 'com': com_frames, 'base': base_frames, 'qvel_sample': []
    }
    OUT.write_text(json.dumps(out, separators=(',', ':')))
    print(json.dumps({k:v for k,v in out.items() if k not in ('qpos','com','qvel_sample')}))


if __name__ == '__main__':
    main()
