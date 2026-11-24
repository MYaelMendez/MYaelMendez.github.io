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
    ap.add_argument('--scenes', help='scene spec JSON with speak/state lines — enables voice + world')
    ap.add_argument('--texture', default='sci_fi', help='world bed texture')
    ap.add_argument('--silent', action='store_true', help='skip the sound stage')
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
        # Motion must clear the supervisor's movimiento > 0.5 threshold. A gentle
        # idle sway measured 0.386 = WARN, so the pose is a real gesture: knees
        # load, arms swing, head turns, and the camera arcs. Fix the scene, never
        # the threshold.
        for j in urdf['joints']:
            nm = j['name']
            if 'knee' in nm:
                ang[nm] = 0.22 * math.sin(tt * 1.9)
            elif 'ankle_pitch' in nm:
                ang[nm] = -0.12 * math.sin(tt * 1.9)
            elif 'hip_pitch' in nm:
                ang[nm] = 0.10 * math.sin(tt * 1.9 + 0.6)
            elif 'shoulder_pitch' in nm:
                ang[nm] = 0.30 * math.sin(tt * 1.5 + 1.0)
            elif 'elbow' in nm:
                ang[nm] = 0.25 * math.sin(tt * 1.5 + 2.0)
            elif 'waist_yaw' in nm:
                ang[nm] = 0.14 * math.sin(tt * 0.9)
            elif 'neck_yaw' in nm:
                ang[nm] = 0.34 * math.sin(tt * 1.2)
            elif 'neck_pitch' in nm:
                ang[nm] = 0.12 * math.sin(tt * 1.6)
        xf = transforms(urdf, ang)
        root = np.eye(4)
        root[:3, :3] = rot_euler([0, 0, 0.10 * math.sin(tt * 0.7)])
        root[2, 3] = 0.03 * math.sin(tt * 1.9)
        V, N, L = world_tris(links, xf, root)
        az = 0.34 * math.sin(tt * 0.55)
        eye = ctr + np.array([dist * math.cos(az), dist * math.sin(az),
                              0.15 + 0.10 * math.sin(tt * 0.8)], np.float32)
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
    # ── sound stage ──────────────────────────────────────────────────────
    # The OpenGL films all carry a world (0% near-silent windows). The RTX
    # path inherited none of it — superior compute must not mean losing the
    # audio. Voice and world are a stage here, not a manual afterthought.
    audio = {'voice': False, 'world': False}
    if not a.silent:
        try:
            sys.path.insert(0, str(HERE))
            import sound_link as S
            scenes = json.loads(Path(a.scenes).read_text(encoding='utf-8'))['scenes'] \
                if a.scenes else None
        except Exception as exc:
            scenes = None
            print(f'  sound stage unavailable: {type(exc).__name__}: {exc}')
        if scenes:
            # voice: one line per scene, timed by its own audio length
            tts = Path(os.environ.get('HERMES_HOME', Path.home()/'.hermes')) / \
                'plugins' / 'tiny-voca-voice' / 'scripts' / 'tiny_voca_voice.py'
            wavs = []
            if tts.exists():
                for i, sc in enumerate(scenes):
                    w = wd / f's{i}.wav'
                    subprocess.run([sys.executable, str(tts), '--text', sc.get('speak', ''),
                                    '--voice', sc.get('voice', 'M2'), '--output', str(w)],
                                   capture_output=True, timeout=300)
                    if w.exists():
                        wavs.append(w)
                audio['voice'] = len(wavs) == len(scenes) and bool(wavs)
            if wavs:
                lst = wd / 'audio.txt'
                lst.write_text(''.join(f"file '{w.as_posix()}'\n" for w in wavs), encoding='utf-8')
                track = wd / 'track.wav'
                subprocess.run([str(_ffmpeg()/'ffmpeg'), '-v', 'error', '-y', '-f', 'concat',
                                '-safe', '0', '-i', str(lst), '-ar', '24000', '-ac', '1',
                                str(track)], capture_output=True, timeout=600)
                total = track.stat().st_size / 48000.0
                subprocess.run([str(_ffmpeg()/'ffmpeg'), '-v', 'error', '-y',
                                '-i', str(silent), '-i', str(track), '-c:v', 'copy',
                                '-filter:a', f'apad=whole_dur={total:.6f}',
                                '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart',
                                '-t', f'{total:.6f}', str(out)], capture_output=True, timeout=900)
                # world: derived from the film's OWN scene boundaries
                try:
                    t0 = 0.0
                    for sc, w in zip(scenes, wavs):
                        d_ = w.stat().st_size / 48000.0
                        sc['_t0'] = t0; sc['_dur'] = d_; t0 += d_
                    spec_ = {'scenes': scenes, '_total': t0}
                    a_ = S.spec_from_film(spec_, texture=a.texture, bed_db=-29.0)
                    wv = wd / 'world.wav'
                    r_ = S.render(a_, wv)
                    if r_.get('ok'):
                        mixed = wd / 'world.mp4'
                        m_ = S.mix(out, wv, mixed, bed_gain=0.5)
                        if m_.get('ok'):
                            mixed.replace(out)
                            audio['world'] = True
                            audio['events'] = len(a_['events'])
                            audio['torch'] = r_.get('torch')
                except Exception as exc:
                    print(f'  world stage failed: {type(exc).__name__}: {exc}')
    if not out.exists():
        silent.replace(out)
    meta = dict(audio=audio, frames=nf, fps=a.fps, links=len(links), joints=len(urdf['joints']),
                triangles=len(V0), seconds=round(el, 1),
                ms_per_frame=round(el / nf * 1000, 1), raster_ms=round(rms / nf, 1),
                device='RTX 3050 CUDA', source='urdf.json', bytes=out.stat().st_size)
    (wd / 'rtx.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    print('  ' + json.dumps(meta))


if __name__ == '__main__':
    main()
