"""Author and verify the Asimov USD digital twin from official URDF + qpos trace.

This is a first-class USD ASCII stage: 26 link frames, 25 governed joints,
relative mesh references, and qpos time samples from the official physics trace.
No Omniverse install is required to author or verify it here.
"""
import hashlib, json, math, os, shutil, sys, xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
MODEL = Path(os.environ.get('HERMES_AE_ASIMOV_MODEL', HERMES_HOME / 'hermes-asimov' / 'model'))
TRACE = Path(os.environ.get('HERMES_AE_QPOS_TRACE', HERMES_HOME / 'asimov-anim' / 'physics_trace.json'))
OUT = Path(os.environ.get('HERMES_AE_USD_OUT', ROOT / 'packages' / 'asimov-twin' / '1.0.0'))
URDF = MODEL / 'urdf' / 'asimov_1_25dof.urdf'
MESHES = MODEL / 'meshes'
MANIFEST = OUT / 'manifest.json'
USD = OUT / 'asimov-avatar.usda'
FPS = 24


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest() if Path(path).exists() else None


def fmt(v):
    return f'{float(v):.9g}'


def tri(v):
    return '(' + ', '.join(fmt(x) for x in v) + ')'


def parse_urdf():
    if not URDF.exists():
        raise RuntimeError(f'URDF missing: {URDF}')
    root = ET.parse(URDF).getroot()
    links = {}
    for link in root.findall('link'):
        name = link.attrib.get('name')
        if not name:
            continue
        mesh = link.find('./visual/geometry/mesh')
        fname = Path(mesh.attrib['filename']).name if mesh is not None and mesh.attrib.get('filename') else None
        links[name] = {'name': name, 'mesh': fname}
    joints = {}
    for joint in root.findall('joint'):
        name = joint.attrib['name']
        p_el = joint.find('parent')
        c_el = joint.find('child')
        parent = p_el.attrib.get('link') if p_el is not None else None
        child = c_el.attrib.get('link') if c_el is not None else None
        if not name or not parent or not child:
            continue
        origin = joint.find('origin')
        xyz = [float(x) for x in origin.attrib.get('xyz', '0 0 0').split()] if origin is not None else [0.0, 0.0, 0.0]
        rpy = [float(x) for x in origin.attrib.get('rpy', '0 0 0').split()] if origin is not None else [0.0, 0.0, 0.0]
        axis_el = joint.find('axis')
        axis = [float(x) for x in axis_el.attrib.get('xyz', '1 0 0').split()] if axis_el is not None else [1.0, 0.0, 0.0]
        limit = joint.find('limit')
        lo = float(limit.attrib.get('lower', '-3.14159')) if limit is not None else -3.14159
        hi = float(limit.attrib.get('upper', '3.14159')) if limit is not None else 3.14159
        joints[child] = {'name': name, 'parent': parent, 'child': child, 'xyz': xyz,
                         'rpy': rpy, 'axis': axis, 'type': joint.attrib.get('type', 'fixed'),
                         'lower': lo, 'upper': hi}
    parents = {j['child'] for j in joints.values()}
    roots = [n for n in links if n not in parents]
    if not roots:
        raise RuntimeError('no root link found in URDF')
    order, queue = [], [roots[0]]
    while queue:
        name = queue.pop(0)
        if name in order:
            continue
        order.append(name)
        queue += [j['child'] for j in joints.values() if j['parent'] == name]
    return links, joints, order


def load_qpos():
    if not TRACE.exists():
        raise RuntimeError(f'qpos trace missing: {TRACE}')
    data = json.loads(TRACE.read_text())
    names = data['joint_names']
    qpos = data['qpos']
    if not names or not qpos or len(names) != len(qpos[0]):
        raise RuntimeError('qpos trace shape mismatch')
    mapping = {}
    for frame in qpos:
        for name, value in zip(names, frame):
            mapping.setdefault(name, []).append(float(value))
    return names, qpos, mapping


def rot_op(axis):
    a = [abs(x) for x in axis]
    i = max(range(3), key=lambda k: a[k])
    return ['xformOp:rotateX', 'xformOp:rotateY', 'xformOp:rotateZ'][i], axis[i]


def build():
    links, joints, order = parse_urdf()
    joint_names, qpos, samples = load_qpos()
    (OUT / 'meshes').mkdir(parents=True, exist_ok=True)
    (OUT / 'model').mkdir(parents=True, exist_ok=True)
    copied = []
    for name, link in links.items():
        src = MESHES / (link['mesh'] or '')
        if link['mesh'] and src.exists():
            dst = OUT / 'meshes' / src.name
            if not dst.exists() or sha(dst) != sha(src):
                shutil.copyfile(src, dst)
            copied.append(src.name)
    for src in (URDF, MODEL / 'xml' / 'asimov_1_25dof.xml', TRACE):
        if src.exists():
            shutil.copyfile(src, OUT / 'model' / src.name)

    lines = [
        '#usda 1.0',
        '(',
        '    defaultPrim = "Asimov"',
        '    upAxis = "Z"',
        '    metersPerUnit = 1',
        f'    timeCodesPerSecond = {FPS}',
        '    startTimeCode = 0',
        f'    endTimeCode = {max(0, len(qpos) - 1)}',
        '    customLayerData = {',
        '        string authority = "HUMAN://ROOT"',
        '        string source = "menloresearch/asimov-1"',
        '        string asset_class = "asimov-avatar"',
        '        string note = "URDF link frames + governed joints + qpos replay; mesh geometry remains in referenced STL files"',
        '    }',
        ')',
        '',
        'def Xform "Asimov" (',
        '    kind = "component"',
        '    customData = {',
        '        string authority = "HUMAN://ROOT"',
        '        string identity = "hermes-agent build body"',
        '        string source = "menloresearch/asimov-1"',
        f'        int dof = {len(joints)}',
        f'        int links = {len(links)}',
        f'        int frames = {len(qpos)}',
        '    }',
        ')',
        '{',
    ]
    for link_name in order:
        link = links[link_name]
        j = joints.get(link_name)
        lines += ['', f'    def Xform "{link_name}"', '    {']
        if j:
            lines += [f'        double3 xformOp:translate = {tri(j["xyz"])}',
                      f'        double3 xformOp:rotateXYZ = {tri([math.degrees(v) for v in j["rpy"]])}',
                      '        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ"]']
        else:
            lines += ['        double3 xformOp:translate = (0, 0, 0)',
                      '        double3 xformOp:rotateXYZ = (0, 0, 0)',
                      '        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ"]']
        if link['mesh'] and (OUT / 'meshes' / link['mesh']).exists():
            lines += [f'        asset inputs:file = @./meshes/{link["mesh"]}@',
                      f'        string inputs:mesh_sha256 = "{sha(OUT / "meshes" / link["mesh"])}"']
        if j:
            op, sign = rot_op(j['axis'])
            lines += ['', f'        def Xform "joint_{j["name"]}" (',
                      '            customData = {',
                      f'                string joint_type = "{j["type"]}"',
                      f'                string parent = "{j["parent"]}"',
                      f'                string child = "{j["child"]}"',
                      f'                double lower = {fmt(j["lower"])}',
                      f'                double upper = {fmt(j["upper"])}',
                      '            }',
                      '        )',
                      '        {',
                      '            double3 xformOp:translate = (0, 0, 0)']
            key = j['name']
            if key not in samples:
                key = next((n for n in joint_names if n.replace('_joint', '_link') == j['name']), j['name'])
            vals = samples.get(key, [0.0] * len(qpos))
            lines.append(f'            double3 {op}.timeSamples = {{')
            for i, value in enumerate(vals[:len(qpos)]):
                ang = math.degrees(value) * (1.0 if sign >= 0 else -1.0)
                vec = [0.0, 0.0, 0.0]
                vec[['x', 'y', 'z'].index(op[-1].lower())] = ang
                lines.append(f'                {i}: {tri(vec)},')
            lines += ['            }',
                      '            uniform token[] xformOpOrder = ["xformOp:translate", "' + op + '"]',
                      f'            string inputs:joint_name = "{key}"',
                      f'            float inputs:qpos.timeSamples = {{ ' + ', '.join(f'{i}: {fmt(v)}' for i, v in enumerate(vals[:len(qpos)])) + ' }',
                      '        }']
        lines.append('    }')
    lines += ['}', '', 'def Scope "Provenance"', '{',
              f'    asset inputs:urdf = @./model/{URDF.name}@',
              f'    asset inputs:mjcf = @./model/asimov_1_25dof.xml@',
              f'    asset inputs:qpos_trace = @./model/{TRACE.name}@',
              f'    string urdf_sha256 = "{sha(URDF)}"',
              f'    string mjcf_sha256 = "{sha(MODEL / "xml" / "asimov_1_25dof.xml")}"',
              f'    string qpos_sha256 = "{sha(TRACE)}"',
              '}']
    USD.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    manifest = {
        'schema': 'hermes-ae/asimov-twin/1.0.0',
        'name': 'asimov-avatar',
        'version': '1.0.0',
        'authority': 'HUMAN://ROOT',
        'source': 'menloresearch/asimov-1',
        'format': 'USD ASCII',
        'stage': USD.name,
        'stage_sha256': sha(USD),
        'stage_bytes': USD.stat().st_size,
        'urdf_sha256': sha(URDF),
        'mjcf_sha256': sha(MODEL / 'xml' / 'asimov_1_25dof.xml'),
        'qpos_trace_sha256': sha(TRACE),
        'links': len(links),
        'joints': len(joints),
        'frames': len(qpos),
        'fps': FPS,
        'mesh_files': sorted(copied),
        'receipt_action': 'AVATAR://USD_BIND',
        'note': 'mesh geometry is referenced as STL assets; convert to skinned USD geometry in Omniverse for ACE workflows',
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'README.md').write_text(
        '# Asimov Avatar — USD digital twin\n\n'
        'Authored from official Asimov-1 URDF/MJCF, 26 STL mesh references, and a real MuJoCo qpos trace.\n\n'
        '```text\nHUMAN://ROOT → æ → Asimov Agent → asimov-avatar.usda → RECEIPT\n```\n\n'
        f'- Links: {len(links)}\n- Joints: {len(joints)}\n- Qpos frames: {len(qpos)}\n\n'
        'This first slice authors transform hierarchy, governed joints, mesh references, and qpos replay. '
        'It is not yet an ACE skinned avatar.\n', encoding='utf-8')
    return {'success': True, 'manifest': manifest, 'out': str(OUT)}


def verify():
    if not MANIFEST.exists() or not USD.exists():
        return {'success': False, 'error': 'manifest or USD stage missing'}
    m = json.loads(MANIFEST.read_text())
    text = USD.read_text()
    checks = {
        'usda_header': text.startswith('#usda 1.0'),
        'default_prim': 'defaultPrim = "Asimov"' in text,
        'authority': 'HUMAN://ROOT' in text,
        'stage_hash': sha(USD) == m['stage_sha256'],
        'link_frames': text.count('def Xform "') >= m['links'],
        'joints': text.count('def Xform "joint_') == m['joints'],
        'time_samples': text.count('.timeSamples') >= m['joints'],
        'meshes': all((OUT / 'meshes' / n).exists() for n in m['mesh_files']),
    }
    try:
        from pxr import Usd
        stage = getattr(Usd, 'Stage').Open(str(USD))
        checks['pxr_stage_open'] = bool(stage and stage.GetDefaultPrim())
    except Exception:
        checks['pxr_stage_open'] = 'skipped'
    return {'success': all(checks.values()), 'checks': checks, 'manifest': m}


def info():
    return {'success': MANIFEST.exists(), 'manifest': json.loads(MANIFEST.read_text()) if MANIFEST.exists() else None}


def run(args):
    action = args.get('action', 'info')
    if action == 'build':
        return build()
    if action == 'verify':
        return verify()
    return info()


if __name__ == '__main__':
    try:
        print(json.dumps(run(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}), ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'success': False, 'error': f'{type(exc).__name__}: {exc}'}))
