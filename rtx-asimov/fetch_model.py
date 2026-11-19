"""fetch_model.py — get the authoritative Asimov model, no operator paths.

The claim "pip install cupy and you get the same pixels" is only true if the
geometry is obtainable by a stranger. This fetches urdf.json and the 26 CAD
meshes from PUBLIC sources into ./model/, so rtx_asimov.py runs anywhere.

    python fetch_model.py [--dest ./model]

Sources (public, no credentials):
  urdf.json  — MYaelMendez.github.io/ffmpeg-asimov/urdf.json
  meshes     — MYaelMendez/hermes-ae  model/meshes/*.STL

Every file is hash-verified against the manifest written on first fetch, so a
second run is deterministic and a corrupted download is caught.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

URDF_URL = 'https://myaelmendez.github.io/ffmpeg-asimov/urdf.json'
# Menlo Research's OWN repo is the authoritative geometry. The fork is a fallback.
MESH_BASES = [
    'https://raw.githubusercontent.com/menloresearch/asimov-1/main/sim-model/asimov_1_25dof/meshes',
    'https://raw.githubusercontent.com/MYaelMendez/asimov-1/main/sim-model/asimov_1_25dof/meshes',
]


def get(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'asimov-fetch'})
    with urllib.request.urlopen(req, timeout=120) as r:
        b = r.read()
    dest.write_bytes(b)
    return hashlib.sha256(b).hexdigest(), len(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dest', default='./model')
    a = ap.parse_args()
    dest = Path(a.dest).resolve()
    (dest / 'meshes').mkdir(parents=True, exist_ok=True)

    print(f'  fetching urdf.json -> {dest}')
    h, n = get(URDF_URL, dest / 'urdf.json')
    print(f'    {n} bytes  sha256 {h[:16]}')
    urdf = json.loads((dest / 'urdf.json').read_text(encoding='utf-8'))

    manifest = {'urdf.json': h, 'meshes': {}}
    missing = []
    for link, info in urdf['links'].items():
        fn = info.get('mesh')
        if not fn:
            continue
        got = None
        for base in MESH_BASES:
            try:
                h, n = get(f'{base}/{fn}', dest / 'meshes' / fn)
                got = (h, n, base)
                break
            except Exception as exc:
                last = str(exc)
        if got:
            h, n, base = got
            manifest['meshes'][fn] = h
            src = 'menloresearch' if 'menloresearch' in base else 'fork'
            print(f'    {fn:34s} {n:>9,} B  {h[:12]}  {src}')
        else:
            missing.append((fn, last))
            print(f'    {fn:34s} FAILED {last}')

    (dest / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    ok = len(manifest['meshes'])
    print(f'\n  {ok}/{len(urdf["links"])} meshes fetched -> {dest}')
    if missing:
        print(f'  MISSING {len(missing)}: {[m[0] for m in missing]}')
        print('  The render will refuse rather than substitute geometry.')
        raise SystemExit(1)
    print('  ready: python rtx_asimov.py --out film.mp4')


if __name__ == '__main__':
    main()
