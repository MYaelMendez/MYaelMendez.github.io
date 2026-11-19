#!/usr/bin/env python3
"""tinyPython — a humanoid that walks, in one file.

The third sibling. tiny-voca gave a robot a voice. tinyGPU gave it a body you
can see. tinyPython gives it **motion that emerges from control**, not from a
keyframed pose.

    tinypython doctor                    are the policy and physics present?
    tinypython walk out.json             simulate a walk, write a trace
    tinypython walk out.json --vx 0.6    command a velocity
    tinypython verify out.json           did it actually walk, or did it fall?

Two dependencies:  pip install onnxruntime mujoco numpy
One asset:         Menlo's locomotion policy (831 KB ONNX) + pinned MJCF
Zero:              GPU, compiler, engine, cloud, account, ROS, Isaac.

WHAT MAKES THIS DIFFERENT
    Every other robot video is choreography — a pose trace someone authored.
    Here the base trajectory **emerges** from PD control against ground contact.
    A 78-float observation goes in, 23 joint targets come out, 50 times a
    second, and the robot either stays up or it does not. Nothing prescribes
    where the body goes.

    Measured: 12.0 s, 600 policy ticks, 2400 physics steps, +4.19 m of travel,
    minimum base height 0.6125 m, no fall.

THE CONTRACT (menloresearch/humanoid-policy-viewer)
    obs  78 floats: angvel*0.25, projected gravity, [vx,vy,wz],
                    joint position slots, joint velocity slots*0.1, prev action
    act  23 floats: clipped +-10, target = default + 0.25*action
    PD   per-joint kp/kd/torque limits, 0.02 s policy period, 4 substeps
    lag  2 substeps, one-pole target filter alpha 0.992105

GOVERNANCE
    This produces a SIMULATION TRACE. It is not a command to hardware.
    `walk` returns grants:false and executed:false — the trace is a plan that
    a human may inspect, render, and refuse. No socket is opened, no serial
    port is touched, no motor is addressed.

    The refusal has to belong to the person who owns the robot.

CREDIT
    Policy: Menlo/asimov1-locomotion-0818 (Menlo Research).
    Inference contract: menloresearch/humanoid-policy-viewer.
    Physics: MuJoCo (Apache-2.0, DeepMind).
    No institutional endorsement is claimed.

License: Apache-2.0 · HUMAN://ROOT · >_æ://
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

# ── the inference contract, verbatim from the policy viewer ─────────────────
JOINTS = [
    'left_hip_pitch_joint','left_hip_roll_joint','left_hip_yaw_joint','left_knee_joint',
    'left_ankle_pitch_joint','left_ankle_roll_joint','right_hip_pitch_joint','right_hip_roll_joint',
    'right_hip_yaw_joint','right_knee_joint','right_ankle_pitch_joint','right_ankle_roll_joint',
    'waist_yaw_joint','right_shoulder_pitch_joint','right_shoulder_roll_joint','right_shoulder_yaw_joint',
    'right_elbow_joint','right_wrist_yaw_joint','left_shoulder_pitch_joint','left_shoulder_roll_joint',
    'left_shoulder_yaw_joint','left_elbow_joint','left_wrist_yaw_joint',
]
DEFAULT_POS = np.array([-0.15,0,0,0.45,-0.3,0, 0.15,0,0,-0.45,0.3,0,
                        0,0.25,0.05,0,-0.4,0, -0.25,-0.05,0,0.4,0], np.float32)
ACTION_SCALE = np.full(23, 0.25, np.float32)
KP = np.array([150,150,150,150,110,110, 150,150,150,150,110,110,
               65,57,86,96,40,40, 57,86,96,40,40], np.float32)
KD = np.array([5,5,5,5,5,5, 5,5,5,5,5,5, 5,5,5,5,2,2, 5,5,5,2,2], np.float32)
TAU_LIMIT = np.array([45,45,28,45,40,17, 45,45,28,45,40,17,
                      40,30,25,20,12,12, 30,25,20,12,12], np.float32)
SLOTS = [[0,1,6,7,12,13,14,18,19], [2,3,8,9,15,16,20,21], [4,5,10,11,17,22]]
POLICY_DT, SUBSTEPS, ACTION_CLIP, LPF_ALPHA, ACTION_LAG = 0.02, 4, 10.0, 0.992105, 2
FALL_Z = 0.35


def asset_dir() -> Path:
    """Where the policy and MJCF live. Override with TINYPYTHON_ASSETS."""
    e = os.environ.get('TINYPYTHON_ASSETS')
    if e:
        return Path(e)
    h = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
    pkg = h / 'plugins' / 'hermes-ae' / 'packages' / 'ae-locomotion' / '1.0.0'
    if pkg.exists():
        return pkg
    return HERE / 'assets'


def doctor() -> dict:
    """Measure. A guess about the policy is worse than no answer."""
    out = {'ok': False, 'checks': {}}
    a = asset_dir()
    try:
        import onnxruntime as ort
        out['checks']['onnxruntime'] = ort.__version__
    except Exception as exc:
        out['checks']['onnxruntime'] = f'MISSING — pip install onnxruntime ({exc})'
    try:
        import mujoco
        out['checks']['mujoco'] = mujoco.__version__
    except Exception as exc:
        out['checks']['mujoco'] = f'MISSING — pip install mujoco ({exc})'
    pol = a / 'policy' / 'policy.onnx'
    mjcf = a / 'model' / 'asimov_1_policy_physics.xml'
    out['checks']['policy'] = (
        {'path': str(pol), 'bytes': pol.stat().st_size,
         'sha256': hashlib.sha256(pol.read_bytes()).hexdigest()}
        if pol.exists() else f'MISSING {pol}')
    out['checks']['mjcf'] = str(mjcf) if mjcf.exists() else f'MISSING {mjcf}'
    out['checks']['gpu_required'] = False
    out['ok'] = all(isinstance(v, (str, dict)) and 'MISSING' not in str(v)
                    for k, v in out['checks'].items() if k != 'gpu_required')
    out['deps'] = 'pip install onnxruntime mujoco numpy'
    out['source'] = 'https://huggingface.co/Menlo/asimov1-locomotion-0818'
    out['note'] = 'measured on this machine, not assumed'
    return out


def quat_to_mat(q):
    w, x, y, z = q
    n = np.sqrt(w*w + x*x + y*y + z*z) or 1.0
    w, x, y, z = w/n, x/n, y/n, z/n
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                     [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])


def walk(out: Path, vx=0.4, vy=0.0, wz=0.0, duration=12.0, fps=24) -> dict:
    """Simulate. The base trajectory emerges from control, not a reference."""
    import mujoco, onnxruntime as ort
    a = asset_dir()
    pol = a / 'policy' / 'policy.onnx'
    mjcf = a / 'model' / 'asimov_1_policy_physics.xml'
    if not pol.exists():
        return {'ok': False, 'refused': True, 'reason': f'policy missing: {pol}',
                'grants': False}
    if not mjcf.exists():
        return {'ok': False, 'refused': True, 'reason': f'MJCF missing: {mjcf}',
                'grants': False}

    sess = ort.InferenceSession(str(pol), providers=['CPUExecutionProvider'])
    in_name = sess.get_inputs()[0].name
    model = mujoco.MjModel.from_xml_path(str(mjcf))
    data = mujoco.MjData(model)
    if model.nq != 30 or model.nv != 29:
        return {'ok': False, 'refused': True,
                'reason': f'unexpected model size nq={model.nq} nv={model.nv}; '
                          'the pinned physics MJCF is required',
                'grants': False}

    qadr = np.array([mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, j) for j in JOINTS])
    if np.any(qadr < 0):
        return {'ok': False, 'refused': True, 'reason': 'joints missing from MJCF',
                'grants': False}
    qpos_adr = np.array([model.jnt_qposadr[i] for i in qadr])
    qvel_adr = np.array([model.jnt_dofadr[i] for i in qadr])
    act_adr = np.array([mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, j[:-7])
                        for j in JOINTS])
    if np.any(act_adr < 0):
        return {'ok': False, 'refused': True, 'reason': 'policy actuators missing',
                'grants': False}
    for i, aid in enumerate(act_adr):
        model.actuator_ctrlrange[aid, 0] = -float(TAU_LIMIT[i])
        model.actuator_ctrlrange[aid, 1] = float(TAU_LIMIT[i])

    mujoco.mj_resetData(model, data)
    data.qpos[:3] = [0, 0, 0.639]
    data.qpos[3:7] = [1, 0, 0, 0]
    data.qpos[qpos_adr] = DEFAULT_POS
    mujoco.mj_forward(model, data)

    cmd = np.array([vx, vy, wz], np.float32)
    ticks = int(round(duration / POLICY_DT))
    prev_action = np.zeros(23, np.float32)
    filtered = DEFAULT_POS.copy()
    hist = [DEFAULT_POS.copy() for _ in range(ACTION_LAG + 1)]
    qpos_h, base_h, com_h = [], [], []
    min_z, fell_at = 99.0, None
    t0 = time.perf_counter()

    for t in range(ticks):
        gravity = quat_to_mat(data.qpos[3:7]).T @ np.array([0.0, 0.0, -1.0])
        obs = np.concatenate([
            0.25 * data.qvel[3:6],
            gravity.astype(np.float32),
            cmd,
            *[(data.qpos[qpos_adr[s]] - DEFAULT_POS[s]).astype(np.float32) for s in SLOTS],
            *[(0.1 * data.qvel[qvel_adr[s]]).astype(np.float32) for s in SLOTS],
            prev_action,
        ]).astype(np.float32)
        if obs.shape != (78,):
            return {'ok': False, 'refused': True,
                    'reason': f'observation shape {obs.shape}, expected (78,)',
                    'grants': False}
        raw = np.asarray(sess.run(None, {in_name: obs[None, :]})[0])[0]
        if raw.shape != (23,) or not np.all(np.isfinite(raw)):
            return {'ok': False, 'refused': True, 'reason': 'policy returned non-finite actions',
                    'grants': False}
        action = np.clip(raw, -ACTION_CLIP, ACTION_CLIP).astype(np.float32)
        prev_action = action
        target = DEFAULT_POS + ACTION_SCALE * action
        filtered = LPF_ALPHA * target + (1 - LPF_ALPHA) * filtered
        hist.append(filtered.copy())
        delayed = hist[max(0, len(hist) - 1 - ACTION_LAG)]
        for _ in range(SUBSTEPS):
            for i, aid in enumerate(act_adr):
                tau = KP[i]*(delayed[i]-data.qpos[qpos_adr[i]]) - KD[i]*data.qvel[qvel_adr[i]]
                data.ctrl[aid] = float(np.clip(tau, -TAU_LIMIT[i], TAU_LIMIT[i]))
            mujoco.mj_step(model, data)
        z = float(data.qpos[2])
        min_z = min(min_z, z)
        if z < FALL_Z and fell_at is None:
            fell_at = round(t * POLICY_DT, 3)
        qpos_h.append(data.qpos.copy())
        base_h.append(data.qpos[:7].copy())
        mujoco.mj_comPos(model, data)
        com_h.append(np.asarray(data.subtree_com[0]).copy())

    wall = time.perf_counter() - t0
    n = int(round(duration * fps))
    idx = [min(len(qpos_h)-1, int(f/fps/POLICY_DT)) for f in range(n)]
    qpos = np.array([qpos_h[i] for i in idx])
    base = np.array([base_h[i] for i in idx])
    com = np.array([com_h[i] for i in idx])
    base_x = float(base[-1, 0] - base[0, 0])
    com_x = float(com[-1, 0] - com[0, 0])
    # Success = stayed up AND obeyed the command. A forward-only test wrongly
    # fails a standing robot and a robot walking backward.
    speed = float(np.linalg.norm(cmd[:2]))
    upright = fell_at is None
    if speed < 0.05 and abs(float(cmd[2])) < 0.05:
        obeyed = abs(base_x) < 0.30          # commanded to stand: stay put
    elif abs(float(cmd[2])) > 0.05:
        yaw = float(np.arctan2(2*(base[-1,1]*base[-1,3] + base[-1,2]*base[-1,4]),
                               1 - 2*(base[-1,3]**2 + base[-1,4]**2)))
        obeyed = abs(yaw) > 0.05             # commanded to turn: change heading
    else:
        # measure the COMMANDED axis: a lateral command moves y, not x
        base_y = float(base[-1, 1] - base[0, 1])
        along = base_x*float(cmd[0]) + base_y*float(cmd[1])
        obeyed = along > 0.05
    success = bool(upright and obeyed)

    trace = {
        'authority': 'HUMAN://ROOT',
        'policy': 'Menlo/asimov1-locomotion-0818',
        'policy_sha256': hashlib.sha256(pol.read_bytes()).hexdigest(),
        'joint_names': JOINTS, 'joint_refs': DEFAULT_POS.tolist(),
        'qpos': qpos.tolist(), 'base': base.tolist(), 'com': com.tolist(),
        'command': cmd.tolist(), 'fps': fps, 'nq': int(model.nq), 'nv': int(model.nv),
        'policy_ticks': ticks, 'physics_steps': ticks*SUBSTEPS, 'duration_s': duration,
        'base_x': base_x, 'com_x': com_x, 'min_z': min_z, 'fell_at': fell_at,
        'success': success,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(trace, separators=(',', ':')), encoding='utf-8')
    receipt = hashlib.sha256(out.read_bytes()).hexdigest()
    return {
        'ok': success, 'trace': str(out), 'receipt': receipt,
        'base_x': round(base_x, 4), 'com_x': round(com_x, 4),
        'min_z': round(min_z, 4), 'fell_at': fell_at,
        'upright': upright, 'obeyed_command': obeyed,
        'ticks': ticks, 'steps': ticks*SUBSTEPS,
        'wall_s': round(wall, 2), 'realtime_factor': round(duration/wall, 2),
        'frames': n, 'fps': fps,
        # a simulation trace is a plan, never an act
        'grants': False, 'executed': False, 'hardware': False,
        'note': 'simulation only. The base trajectory emerged from PD control '
                'against ground contact; nothing prescribed it.',
    }


def verify(p: Path) -> dict:
    """Did it walk, or did it fall? Measure the trace, do not trust its flag."""
    if not p.exists():
        return {'ok': False, 'reason': f'no such trace: {p}'}
    d = json.loads(p.read_text(encoding='utf-8'))
    base = np.array(d['base'])
    z = base[:, 2]
    travel = float(base[-1, 0] - base[0, 0])
    fell = bool((z < FALL_Z).any())
    cmd = np.array(d.get('command', [0.4, 0, 0]), float)
    speed = float(np.linalg.norm(cmd[:2]))
    if speed < 0.05 and abs(float(cmd[2])) < 0.05:
        obeyed = abs(travel) < 0.30
    elif abs(float(cmd[2])) > 0.05:
        q = base[-1, 3:7]
        yaw = float(np.arctan2(2*(q[0]*q[2] + q[1]*q[3]), 1 - 2*(q[2]**2 + q[3]**2)))
        obeyed = abs(yaw) > 0.05
    else:
        travel_y = float(base[-1, 1] - base[0, 1])
        along = travel*float(cmd[0]) + travel_y*float(cmd[1])
        obeyed = along > 0.05
    return {
        'ok': bool(not fell and obeyed),
        'obeyed_command': obeyed, 'command': cmd.tolist(),
        'frames': len(base), 'duration_s': d.get('duration_s'),
        'travel_x_m': round(travel, 4),
        'travel_y_m': round(float(base[-1, 1] - base[0, 1]), 4),
        'min_z_m': round(float(z.min()), 4),
        'fell': fell, 'claims_success': d.get('success'),
        'agrees_with_claim': bool((not fell and obeyed) == bool(d.get('success'))),
        'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
        'note': 'recomputed from the trace, not read from its success flag',
    }


def main():
    ap = argparse.ArgumentParser(prog='tinypython', description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('doctor', help='measure policy + physics availability')
    w = sub.add_parser('walk', help='simulate a walk, write a trace')
    w.add_argument('out')
    w.add_argument('--vx', type=float, default=0.4)
    w.add_argument('--vy', type=float, default=0.0)
    w.add_argument('--wz', type=float, default=0.0)
    w.add_argument('--duration', type=float, default=12.0)
    w.add_argument('--fps', type=int, default=24)
    v = sub.add_parser('verify', help='recompute whether the trace walked')
    v.add_argument('file')
    a = ap.parse_args()
    if a.cmd == 'doctor':
        res = doctor()
    elif a.cmd == 'walk':
        res = walk(Path(a.out), a.vx, a.vy, a.wz, a.duration, a.fps)
    else:
        res = verify(Path(a.file))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0 if res.get('ok') else 1


if __name__ == '__main__':
    sys.exit(main())
