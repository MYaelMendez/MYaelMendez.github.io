"""Policy-driven Asimov locomotion harness.

Runs Menlo/asimov1-locomotion-0818 (ONNX, 78 obs -> 23 actions) inside MuJoCo
using the menloresearch/humanoid-policy-viewer inference contract. Produces a
24 Hz qpos trace compatible with render_free_walk.py and a HUMAN://ROOT receipt.
"""
import hashlib, importlib.util, json, os, re, shutil, subprocess, sys
from pathlib import Path
import numpy as np
import mujoco
from ae_paths import ANIM, MESHES, REPO_ROOT, SCRIPTS, ensure_runtime

ensure_runtime()
POLICY_DIR = Path(os.environ.get('HERMES_AE_POLICY_DIR', Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes')) / 'asimov-policy'))
RUNTIME = ANIM / 'policy_model'
MESH_RUNTIME = ANIM / 'policy_meshes'
TRACE_OUT = ANIM / 'physics_policy_trace.json'

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


def build_runtime_model():
    """Materialize the physics-only pinned MJCF with policy actuators."""
    if RUNTIME.exists(): shutil.rmtree(RUNTIME)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    src = (REPO_ROOT / 'model' / 'xml' / 'asimov_1_policy_physics.xml').read_text()
    path = RUNTIME / 'asimov_1_policy_physics.xml'
    path.write_text(src)
    return path


def quat_to_mat(q):
    w, x, y, z = q
    n = np.sqrt(w*w + x*x + y*y + z*z) or 1.0; w,x,y,z = w/n,x/n,y/n,z/n
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])


def run(args):
    policy_p = POLICY_DIR / 'policy.onnx'
    if not policy_p.exists(): raise SystemExit(f'policy missing: {policy_p}')
    import onnxruntime as ort
    sess = ort.InferenceSession(str(policy_p), providers=['CPUExecutionProvider'])
    in_name = sess.get_inputs()[0].name
    model_p = build_runtime_model()
    model = mujoco.MjModel.from_xml_path(str(model_p))
    data = mujoco.MjData(model)
    if model.nq != 30 or model.nv != 29:
        raise SystemExit(f'unexpected model size nq={model.nq} nv={model.nv}')
    qadr = np.array([mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, j) for j in JOINTS])
    qpos_adr = np.array([model.jnt_qposadr[i] for i in qadr])
    qvel_adr = np.array([model.jnt_dofadr[i] for i in qadr])
    act_adr = np.array([mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, j[:-7]) for j in JOINTS])
    if np.any(act_adr < 0): raise SystemExit('policy actuators missing')
    if model.actuator_ctrlrange.ndim == 2:
        for i, aid in enumerate(act_adr):
            model.actuator_ctrlrange[aid, 0] = -float(TAU_LIMIT[i])
            model.actuator_ctrlrange[aid, 1] = float(TAU_LIMIT[i])
    else:
        for i, aid in enumerate(act_adr):
            model.actuator_ctrlrange[2*aid] = -float(TAU_LIMIT[i])
            model.actuator_ctrlrange[2*aid+1] = float(TAU_LIMIT[i])

    mujoco.mj_resetData(model, data)
    data.qpos[:3] = [0, 0, 0.639]
    data.qpos[3:7] = [1, 0, 0, 0]
    data.qpos[qpos_adr] = DEFAULT_POS
    mujoco.mj_forward(model, data)

    cmd = np.array([float(args.get('vx', 0.4)), float(args.get('vy', 0.0)), float(args.get('wz', 0.0))], np.float32)
    duration = float(args.get('duration', 12.0))
    ticks = int(round(duration / POLICY_DT))
    prev_action = np.zeros(23, np.float32)
    filtered = DEFAULT_POS.copy()
    target_hist = [DEFAULT_POS.copy() for _ in range(ACTION_LAG + 1)]
    qpos_hist, qvel_hist, base_hist, com_hist, act_hist = [], [], [], [], []
    min_z, fell_at = 99.0, None

    for t in range(ticks):
        wxyz = data.qpos[3:7]
        gravity = quat_to_mat(wxyz).T @ np.array([0.0, 0.0, -1.0])
        obs = np.concatenate([
            0.25 * data.qvel[3:6],
            gravity.astype(np.float32),
            cmd,
            *[(data.qpos[qpos_adr[s]] - DEFAULT_POS[s]).astype(np.float32) for s in SLOTS],
            *[(0.1 * data.qvel[qvel_adr[s]]).astype(np.float32) for s in SLOTS],
            prev_action,
        ]).astype(np.float32)
        if obs.shape != (78,): raise SystemExit(f'obs shape {obs.shape}')
        raw = np.asarray(sess.run(None, {in_name: obs[None, :]})[0])[0]
        if raw.shape != (23,) or not np.all(np.isfinite(raw)):
            raise SystemExit(f'bad policy output {raw.shape}')
        action = np.clip(raw, -ACTION_CLIP, ACTION_CLIP).astype(np.float32)
        prev_action = action
        target = DEFAULT_POS + ACTION_SCALE * action
        filtered = LPF_ALPHA * target + (1 - LPF_ALPHA) * filtered
        target_hist.append(filtered.copy())
        delayed = target_hist[max(0, len(target_hist) - 1 - ACTION_LAG)]
        for _ in range(SUBSTEPS):
            for i, aid in enumerate(act_adr):
                tau = KP[i] * (delayed[i] - data.qpos[qpos_adr[i]]) - KD[i] * data.qvel[qvel_adr[i]]
                data.ctrl[aid] = float(np.clip(tau, -TAU_LIMIT[i], TAU_LIMIT[i]))
            mujoco.mj_step(model, data)
        z = float(data.qpos[2])
        min_z = min(min_z, z)
        if z < 0.35 and fell_at is None: fell_at = round(t * POLICY_DT, 3)
        qpos_hist.append(data.qpos.copy()); qvel_hist.append(data.qvel.copy())
        base_hist.append(data.qpos[:7].copy())
        mujoco.mj_comPos(model, data)
        com_hist.append(np.asarray(data.subtree_com[0]).copy())
        act_hist.append(action.copy())

    # resample 50 Hz policy trace to 24 fps for the deterministic renderer
    fps, out_n = 24, int(round(duration * 24))
    qpos = np.array([qpos_hist[min(len(qpos_hist)-1, int(f / fps / POLICY_DT))] for f in range(out_n)])
    qvel = np.array([qvel_hist[min(len(qvel_hist)-1, int(f / fps / POLICY_DT))] for f in range(out_n)])
    base = np.array([base_hist[min(len(base_hist)-1, int(f / fps / POLICY_DT))] for f in range(out_n)])
    com = np.array([com_hist[min(len(com_hist)-1, int(f / fps / POLICY_DT))] for f in range(out_n)])
    actions = np.array([act_hist[min(len(act_hist)-1, int(f / fps / POLICY_DT))] for f in range(out_n)])
    trace = {
        'authority': 'HUMAN://ROOT', 'policy': 'Menlo/asimov1-locomotion-0818',
        'policy_sha256': hashlib.sha256(policy_p.read_bytes()).hexdigest(),
        'joint_names': JOINTS, 'joint_refs': DEFAULT_POS.tolist(),
        'qpos': qpos.tolist(), 'qvel': qvel.tolist(), 'base': base.tolist(),
        'com': com.tolist(), 'actions': actions.tolist(),
        'command': cmd.tolist(), 'nq': int(model.nq), 'nv': int(model.nv), 'nu': 23,
        'policy_ticks': ticks, 'physics_steps': ticks * SUBSTEPS,
        'duration_s': duration, 'base_x': float(base[-1, 0] - base[0, 0]),
        'com_x': float(com[-1, 0] - com[0, 0]), 'min_z': min_z, 'fell_at': fell_at,
        'success': bool(fell_at is None and (base[-1, 0] - base[0, 0]) > 0.1),
    }
    TRACE_OUT.write_text(json.dumps(trace, separators=(',', ':')))

    sys.path.insert(0, str(REPO_ROOT))
    spec = importlib.util.spec_from_file_location('ae', REPO_ROOT / '__init__.py')
    ae = importlib.util.module_from_spec(spec); spec.loader.exec_module(ae)
    rec = ae._receipt('POLICY://LOCOMOTION', {
        'authority': 'HUMAN://ROOT', 'policy': trace['policy'],
        'policy_sha256': trace['policy_sha256'], 'command': cmd.tolist(),
        'base_x': trace['base_x'], 'com_x': trace['com_x'], 'min_z': min_z,
        'fell_at': fell_at, 'success': trace['success'], 'trace': str(TRACE_OUT),
    })
    print(json.dumps({'success': trace['success'], 'trace': str(TRACE_OUT),
                      'base_x': round(trace['base_x'], 4), 'com_x': round(trace['com_x'], 4),
                      'min_z': round(min_z, 4), 'fell_at': fell_at,
                      'ticks': ticks, 'steps': ticks * SUBSTEPS, 'receipt': rec['hash']}))


if __name__ == '__main__':
    run(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {})
