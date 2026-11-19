"""Prepare the Asimov CAD for WebGL: STL -> compact binary, plus a scene manifest.

three.js needs positions+normals as typed arrays. One .bin per link keeps the
fetches parallel and the manifest small. URDF joints are emitted verbatim so the
browser can run the SAME forward kinematics the Python harness does.

    python webgl_prep.py --model ./model --out ./scene
"""
from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path

import numpy as np


def stl_to_bin(p: Path, dest: Path):
    b = p.read_bytes()
    n = struct.unpack('<I', b[80:84])[0]
    raw = np.frombuffer(b, dtype=np.uint8, count=n * 50, offset=84).reshape(n, 50)
    rec = raw[:, :48].copy().view('<f4').reshape(n, 12)
    tri = rec.reshape(n, 4, 3)
    nrm = tri[:, 0, :].astype(np.float32)
    pos = tri[:, 1:, :].reshape(-1, 3).astype(np.float32)
    ln = np.linalg.norm(nrm, axis=1, keepdims=True)
    nrm = np.divide(nrm, ln, out=np.zeros_like(nrm), where=ln > 1e-9)
    nrm = np.repeat(nrm, 3, axis=0)              # flat per-vertex normals
    tris = len(pos) // 3
    # NO decimation. Keeping every k-th triangle punches holes in a closed
    # surface — the result reads as shattered geometry, not a lighter model.
    # Full resolution: the GPU has 6 GB and these are static buffers.
    inter = np.empty((len(pos), 6), np.float32)
    inter[:, :3] = pos
    inter[:, 3:] = nrm
    dest.write_bytes(inter.tobytes())
    return len(pos), tris, 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='./model')
    ap.add_argument('--out', default='./scene')
    a = ap.parse_args()
    model, out = Path(a.model).resolve(), Path(a.out).resolve()
    (out / 'mesh').mkdir(parents=True, exist_ok=True)
    urdf = json.loads((model / 'urdf.json').read_text(encoding='utf-8'))

    links = {}
    total_v = 0
    for name, info in urdf['links'].items():
        fn = info.get('mesh')
        if not fn:
            continue
        src = model / 'meshes' / fn
        if not src.exists():
            cand = [q for q in (model / 'meshes').iterdir()
                    if q.stem.lower() == Path(fn).stem.lower()]
            if not cand:
                print(f'  MISSING {name}: {fn}')
                continue
            src = cand[0]
        nv, tris, k = stl_to_bin(src, out / 'mesh' / f'{name}.bin')
        links[name] = {'bin': f'mesh/{name}.bin', 'vertices': nv,
                       'source_triangles': tris, 'decimation': k}
        total_v += nv
        print(f'  {name:32s} {nv:>7,} verts  (1/{k} of {tris:,} tris)')

    manifest = {
        'robot': urdf.get('robot', 'asimov_1_25dof'),
        'links': links,
        'joints': urdf['joints'],
        'total_vertices': total_v,
        'source': 'menloresearch/asimov-1 sim-model/asimov_1_25dof',
    }
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(f'\n  {len(links)} links, {total_v:,} vertices -> {out}')


if __name__ == '__main__':
    main()
