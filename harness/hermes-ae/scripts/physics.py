"""MuJoCo physics step for the synced Asimov-1 studio model.

Default: physics-only MJCF with 25 PD position actuators (nu=25), base fixed
for capture — the same model used by hermes-asimov Studio v2.1.
Pass `--legacy` to step the original unactuated MJCF (nu=0) for comparison.
"""
import sys, json, hashlib
import numpy as np
import mujoco

PHYSICS = '/opt/data/hermes-asimov/model/xml/asimov_1_25dof_physics.xml'
LEGACY = '/opt/data/hermes-asimov/model/xml/asimov_1_25dof.xml'


def main():
    legacy = '--legacy' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    steps = int(args[0]) if args else 500
    path = LEGACY if legacy else PHYSICS
    m = mujoco.MjModel.from_xml_path(path)
    d = mujoco.MjData(m)
    mujoco.mj_forward(m, d)
    q0 = np.array(d.qpos, dtype=float).copy()
    e0 = float(d.energy[0] + d.energy[1])
    for _ in range(steps):
        mujoco.mj_step(m, d)
    q1 = np.array(d.qpos, dtype=float).copy()
    e1 = float(d.energy[0] + d.energy[1])
    mujoco.mj_comPos(m, d)
    com = np.array(d.subtree_com[0], dtype=float)
    out = {
        'success': True,
        'engine': 'MuJoCo ' + mujoco.__version__,
        'model': 'asimov_1_25dof_legacy' if legacy else 'asimov_1_25dof_physics',
        'mjcf': path,
        'mjcf_sha256': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
        'nq': int(m.nq), 'nv': int(m.nv), 'nu': int(m.nu),
        'nbody': int(m.nbody), 'njnt': int(m.njnt),
        'ngeom': int(m.ngeom), 'nmesh': int(m.nmesh),
        'timestep': float(m.opt.timestep), 'steps': steps,
        'time_s': round(float(d.time), 4),
        'qpos_start': [round(float(x), 6) for x in q0[:7]],
        'qpos_end': [round(float(x), 6) for x in q1[:7]],
        'energy_start_j': round(e0, 4), 'energy_end_j': round(e1, 4),
        'com': [round(float(x), 6) for x in com],
        'base_fixed_for_capture': not legacy,
        'synced_with': 'hermes-asimov Studio v2.1',
        'note': ('original MJCF: no actuators (nu=0); base falls under gravity'
                 if legacy else
                 '25 PD position actuators, base fixed; synced Studio v2.1 capture model'),
    }
    print(json.dumps(out))


if __name__ == '__main__':
    main()
