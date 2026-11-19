"""rtx_asimov — the real Asimov CAD, forward-kinematics from URDF, raster on CUDA.

Correction of an earlier mistake: the actuated MJCF carries BOTH visual meshes
and collision primitives (group=3 capsules/spheres, rgba .2 .6 .2 .3). Rendering
those primitives draws the physics proxy, not the robot. The authoritative
geometry is urdf.json: 26 links, each mapped to its STL, 25 joints with
rpy/axis/xyz. This walks that tree exactly as render_free_walk.py does, then
hands every triangle to the RTX.

    python rtx_asimov.py --out film.mp4 [--frames N] [--pose stand|walk]

No OpenGL. MuJoCo is not needed for the visual path at all — the URDF supplies
the kinematics, CuPy supplies the pixels.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rtx_raster import RtxRenderer, load_stl, persp, look_at  # noqa: E402

# Portable by default: everything resolves relative to THIS file, or to a
# --model-dir the user passes. No HERMES_HOME, no operator path, no OS assumption.
HERE = Path(__file__).resolve().parent
MODEL = Path(os.environ.get('ASIMOV_MODEL', HERE / 'model'))
BUNDLE = Path(os.environ.get('ASIMOV_URDF_DIR', MODEL))
MESHES = Path(os.environ.get('ASIMOV_MESHES', MODEL / 'meshes'))


def _ffmpeg():
    """ffmpeg from PATH, or an explicit override. Never a vendored private path."""
    import shutil
    override = os.environ.get('ASIMOV_FFMPEG')
    if override:
        return Path(override)
    found = shutil.which('ffmpeg')
    if found:
        return Path(found).parent
    raise SystemExit('ffmpeg not found on PATH. Install it, or set ASIMOV_FFMPEG=<dir>.')


def _font(sz, bold=False):
    """First available monospace across Windows / macOS / Linux, else PIL default."""
    from PIL import ImageFont
    cands = [
        f"C:/Windows/Fonts/{'consolab' if bold else 'consola'}.ttf",
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf' if bold
        else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        '/usr/share/fonts/TTF/DejaVuSansMono.ttf',
        '/System/Library/Fonts/Menlo.ttc',
        '/Library/Fonts/Courier New.ttf',
    ]
    for c in cands:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, sz)
            except Exception:
                pass
    return ImageFont.load_default()

W, HH = 720, 1280
HDR, VH = 92, 720
HUD = HDR + VH


def rot_euler(rpy):
    x, y, z = rpy
    Rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
    Ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    Rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def axis_rot(axis, ang):
    v = np.asarray(axis, float)
    n = np.linalg.norm(v)
    if n < 1e-9:
        return np.eye(3)
    v = v / n
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) * math.cos(ang) + (1 - math.cos(ang)) * np.outer(v, v) + math.sin(ang) * K


def transforms(urdf, angles):
    """URDF forward kinematics: walk parent -> child until every link is placed."""
    xf = {'pelvis_link': np.eye(4)}
    for _ in range(8):
        for j in urdf['joints']:
            p, c = j['parent'], j['child']
            if p in xf and c not in xf:
                ang = angles.get(j['name'], 0.0)
                m = np.eye(4)
                m[:3, :3] = rot_euler(j['rpy']) @ axis_rot(j.get('axis', [0, 0, 1]), ang)
                m[:3, 3] = j['xyz']
                xf[c] = xf[p] @ m
    return xf


def load_links(urdf):
    """Every link's FULL triangle set. No point sampling, no collision proxies."""
    out = {}
    for name, info in urdf['links'].items():
        fn = info.get('mesh')
        if not fn:
            continue
        p = MESHES / fn
        if not p.exists():
            cand = [q for q in MESHES.iterdir() if q.stem.lower() == Path(fn).stem.lower()]
            if not cand:
                print(f'  MISSING mesh for {name}: {fn}')
                continue
            p = cand[0]
        v, n = load_stl(p)
        out[name] = (v, n)
    return out


def world_tris(links, xf, root):
    Vs, Ns, Ls = [], [], []
    for i, (name, (v, n)) in enumerate(links.items()):
        if name not in xf:
            continue
        M = root @ xf[name]
        R = M[:3, :3].astype(np.float32)
        t = M[:3, 3].astype(np.float32)
        Vs.append(v @ R.T + t)
        Ns.append(n @ R.T)
        Ls.append(np.full(len(v), i, np.int32))
    return (np.concatenate(Vs).astype(np.float32),
            np.concatenate(Ns).astype(np.float32),
            np.concatenate(Ls))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--frames', type=int, default=0)
    ap.add_argument('--fps', type=int, default=24)
    ap.add_argument('--seconds', type=float, default=8.0)
    ap.add_argument('--workdir')
    ap.add_argument('--model-dir', help='directory holding urdf.json and meshes/ (default: ./model)')
    ap.add_argument('--title', default='rtx:// asimov')
    ap.add_argument('--tagline', default='REAL MENLO CAD · URDF FK · CUDA RASTER')
    a = ap.parse_args()

    import cupy as cp
    from PIL import Image, ImageDraw, ImageFont

    global BUNDLE, MESHES
    if a.model_dir:
        BUNDLE = Path(a.model_dir)
        MESHES = BUNDLE / 'meshes'
    urdf_path = BUNDLE / 'urdf.json'
    if not urdf_path.exists():
        raise SystemExit(f'urdf.json not found at {urdf_path}. '
                         'Pass --model-dir, or run fetch_model.py first.')
    urdf = json.loads(urdf_path.read_text(encoding='utf-8'))
    links = load_links(urdf)
    print(f'  device: {cp.cuda.runtime.getDeviceProperties(0)["name"].decode()}')
    print(f'  URDF links {len(urdf["links"])}  joints {len(urdf["joints"])}  meshes loaded {len(links)}')

    out = Path(a.out)
    wd = Path(a.workdir) if a.workdir else out.parent / (out.stem + '-rtx')
    fd = wd / 'frames'
    fd.mkdir(parents=True, exist_ok=True)

    nf = a.frames or int(round(a.seconds * a.fps))
    ident = np.array([0.0, 0.67, 1.0], np.float32)      # hermes blue head
    chassis = np.array([0.86, 0.87, 0.90], np.float32)
    names = list(links)
    cols = np.array([ident if n == 'neck_pitch_link' else chassis for n in names], np.float32)

    # stand pose: a small idle sway, no collision geometry anywhere
    xf0 = transforms(urdf, {})
    root0 = np.eye(4); root0[2, 3] = 0.0
    V0, N0, L0 = world_tris(links, xf0, root0)
    zmin = float(V0[:, 2].min()); zmax = float(V0[:, 2].max())
    print(f'  triangles {len(V0)}   model z {zmin:.3f} .. {zmax:.3f}')

    r = RtxRenderer(W, VH)
    P = persp(45, 0.05, 60.0, aspect=W / VH)
    ctr = np.array([0.0, 0.0, (zmin + zmax) / 2], np.float32)
    span = zmax - zmin
    dist = span * 1.55

    F_B, F_S, F_X = _font(30, True), _font(19), _font(17)

    r.render(V0, N0, cols[L0], P @ look_at(ctr + [dist, 0, 0.15], ctr))  # warmup

    t0 = time.time(); rms = 0.0
    for i in range(nf):
        tt = i / a.fps
        ang = {}
        for j in urdf['joints']:
            nm = j['name']
            if 'knee' in nm:
                ang[nm] = 0.06 * math.sin(tt * 1.1)
            elif 'ankle_pitch' in nm:
                ang[nm] = -0.03 * math.sin(tt * 1.1)
            elif 'shoulder_pitch' in nm:
                ang[nm] = 0.05 * math.sin(tt * 0.9 + 1.0)
            elif 'neck_yaw' in nm:
                ang[nm] = 0.10 * math.sin(tt * 0.7)
        xf = transforms(urdf, ang)
        root = np.eye(4)
        root[:3, :3] = rot_euler([0, 0, 0.02 * math.sin(tt * 0.5)])
        V, N, L = world_tris(links, xf, root)
        az = 0.10 * math.sin(tt * 0.35)
        eye = ctr + np.array([dist * math.cos(az), dist * math.sin(az), 0.15], np.float32)
        tr = time.time()
        img = r.render(V, N, cols[L], P @ look_at(eye, ctr))
        rms += (time.time() - tr) * 1000

        canvas = Image.new('RGB', (W, HH), (11, 10, 6))
        canvas.paste(Image.fromarray(img), (0, HDR))
        dr = ImageDraw.Draw(canvas, 'RGBA')
        dr.rectangle([0, 0, W, HDR], fill=(212, 175, 55, 255))
        dr.text((26, 14), a.title, font=F_B, fill=(11, 10, 6, 255))
        dr.text((26, 54), a.tagline, font=F_S, fill=(58, 48, 16, 255))
        dr.rectangle([0, HUD, W, HH], fill=(14, 13, 8, 255))
        dr.rectangle([0, HUD, W, HUD + 5], fill=(0, 170, 255, 255))
        y = HUD + 20
        for ln in [f'{len(links)} CAD links · {len(urdf["joints"])} joints',
                   f'{len(V):,} triangles per frame',
                   'URDF forward kinematics · no collision proxies',
                   'rasterised on RTX 3050 · CuPy RawKernel · zero OpenGL']:
            dr.text((26, y), ln, font=F_S, fill=(255, 246, 218, 255)); y += 30
        dr.text((26, HH - 40), 'RTX:// CUDA · HUMAN://ROOT · Menlo Research CAD',
                font=F_X, fill=(138, 122, 63, 255))
        canvas.save(fd / f'f{i:05d}.png')
        if i % 48 == 0:
            print(f'  {i}/{nf}')

    el = time.time() - t0
    print(f'  {nf} frames in {el:.1f}s  ({el/nf*1000:.0f} ms/frame total, {rms/nf:.1f} ms raster)')
    silent = wd / 'silent.mp4'
    subprocess.run([str(_ffmpeg() / 'ffmpeg'), '-v', 'error', '-y', '-framerate', str(a.fps),
                    '-i', str(fd / 'f%05d.png'), '-c:v', 'h264_nvenc', '-preset', 'p5',
                    '-b:v', '6M', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                    str(silent)], capture_output=True, timeout=1800)
    silent.replace(out)
    meta = dict(frames=nf, fps=a.fps, links=len(links), joints=len(urdf['joints']),
                triangles=len(V0), seconds=round(el, 1),
                ms_per_frame=round(el / nf * 1000, 1), raster_ms=round(rms / nf, 1),
                device='RTX 3050 CUDA', source='urdf.json', bytes=out.stat().st_size)
    (wd / 'rtx.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    print('  ' + json.dumps(meta))


if __name__ == '__main__':
    main()
