"""æRTX asimov studio — the Asimov CAD body as the standard model for our videos.

Spec-driven. The spec commands; never edit this file to change a video.
Renders the real menloresearch/asimov-1 geometry with native MuJoCo, poses and
colours it per scene, optionally speaks each scene with tinyVOCA, encodes with
NVENC, and gates with SupervisorVideo.

    python asimov_studio.py --spec spec.json --out film.mp4

Spec shape:
{
  "title": "asimov://", "tagline": "...", "fps": 24,
  "scenes": [
    {"kicker":"THE GATE", "state":"REFUSED", "dur":4.0,
     "lines":["asimov://plan stand","decision  require_approval"],
     "banner":"THE ROBOT DOES NOT MOVE",
     "speak":"Policy says approval required.", "voice":"M2"}
  ]
}

States drive the head: colour + yaw + pitch. Layout is separated — the robot
owns the viewport, the HUD owns a solid panel below. Overlap is impossible.
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

H = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
PL = Path(os.environ.get('HERMES_AE_HOME', H / 'plugins' / 'hermes-ae'))
PY = os.environ.get('HERMES_AE_PYTHON', sys.executable)
FF = H / 'tools' / 'ffmpeg-7.1-nvenc' / 'bin'
TTS = H / 'plugins' / 'tiny-voca-voice' / 'scripts' / 'tiny_voca_voice.py'
VIDAEO = Path('C:/æ/vidæo/vidæo.py')

W, HH = 720, 1280
HDR, VIEW_H = 92, 800
HUD_Y = HDR + VIEW_H

# state -> (rgb, neck yaw, neck pitch)
STATES = {
    'IDLE':              ((150, 150, 155),  0.00,  0.00),
    'LISTENING':         ((0, 204, 255),    0.00,  0.00),
    'SPEAKING':          ((0, 255, 159),    0.00, -0.08),
    'THINKING':          ((133, 233, 252),  0.18, -0.04),
    'AWAITING_APPROVAL': ((212, 175, 55),   0.38,  0.06),
    'APPROVED':          ((0, 255, 159),    0.00, -0.10),
    'REFUSED':           ((255, 0, 255),   -0.62,  0.20),
    'ERROR':             ((255, 59, 71),   -0.30,  0.24),
}


def build_model():
    import mujoco
    src = (PL / 'model/xml/asimov_1_25dof_actuated.xml').read_text(encoding='utf-8')
    src = re.sub(r'meshdir="[^"]*"', f'meshdir="{(PL/"model/meshes").as_posix()}"', src)
    vis = f'<visual><global offwidth="{W}" offheight="{VIEW_H}"/><quality shadowsize="4096"/></visual>'
    src = re.sub(r'<visual>.*?</visual>', vis, src, count=1, flags=re.S) if '<visual>' in src \
        else src.replace('</mujoco>', vis + '</mujoco>')
    m = mujoco.MjModel.from_xml_string(src)
    d = mujoco.MjData(m)
    d.ctrl[:] = np.clip(0.0, m.actuator_ctrlrange[:, 0], m.actuator_ctrlrange[:, 1])
    for _ in range(1200):
        mujoco.mj_step(m, d)
    return mujoco, m, d


def speak(text, voice, out):
    if not TTS.exists():
        return None
    env = dict(os.environ)
    env['HERMES_HOME'] = str(H)
    env.setdefault('TINY_VOCA_HOME', str(H / 'tiny-voca'))
    for k in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV'):
        env.pop(k, None)
    p = subprocess.run([PY, str(TTS), '--text', text, '--voice', voice, '--output', str(out)],
                       capture_output=True, text=True, encoding='utf-8', timeout=300, env=env)
    try:
        r = json.loads(p.stdout)
        return out if r.get('success') else None
    except Exception:
        return None


def render(spec, out_path, workdir):
    import mujoco
    from PIL import Image, ImageDraw, ImageFont
    mujoco, m, d = build_model()
    base_q = d.qpos.copy()

    def adr(n):
        j = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_JOINT, n)
        return int(m.jnt_qposadr[j]) if j >= 0 else None
    AY, AP = adr('neck_yaw_joint'), adr('neck_pitch_joint')
    hb = m.body('neck_pitch_link').id
    head_geoms = [g for g in range(m.ngeom) if m.geom_bodyid[g] == hb]

    fps = int(spec.get('fps', 24))
    scenes = spec['scenes']
    workdir.mkdir(parents=True, exist_ok=True)
    frames_dir = workdir / 'frames'
    frames_dir.mkdir(exist_ok=True)

    # voice first: measured durations override the spec's estimate
    t = 0.0
    for i, s in enumerate(scenes):
        wav = None
        if s.get('speak'):
            wav = speak(s['speak'], s.get('voice', 'M2'), workdir / f's{i}.wav')
        if wav and wav.exists():
            dur = wav.stat().st_size / 48000.0
        else:
            dur = float(s.get('dur', 3.0))
        s['_t0'], s['_t1'], s['_wav'] = t, t + dur, wav
        t += dur
    total = t
    nf = int(round(total * fps))
    print(f"scenes={len(scenes)} total={total:.3f}s frames={nf}@{fps}fps")

    def font(sz, bold=False):
        p = f"C:/Windows/Fonts/{'consolab' if bold else 'consola'}.ttf"
        return ImageFont.truetype(p, sz) if Path(p).exists() else ImageFont.load_default()
    F_BIG, F_MED, F_SM, F_XS = font(27, True), font(19, True), font(15), font(13)

    r = mujoco.Renderer(m, height=VIEW_H, width=W)
    cam = mujoco.MjvCamera()
    cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    cam.lookat = np.array([0.0, 0.0, float(spec.get('lookat_z', 0.62))])
    cam.distance = float(spec.get('distance', 2.35))
    cam.elevation = float(spec.get('elevation', -4))

    def smooth(k): return k * k * (3 - 2 * k)

    for i in range(nf):
        tt = i / fps
        s, idx = scenes[0], 0
        for k, sc in enumerate(scenes):
            if sc['_t0'] <= tt < sc['_t1']:
                s, idx = sc, k
                break
        if tt >= scenes[-1]['_t1']:
            s, idx = scenes[-1], len(scenes) - 1
        prev = scenes[max(0, idx - 1)]
        rgb, yaw, pitch = STATES.get(s.get('state', 'IDLE'), STATES['IDLE'])
        prgb, pyaw, ppitch = STATES.get(prev.get('state', 'IDLE'), STATES['IDLE'])
        k = smooth(min(1.0, max(0.0, (tt - s['_t0']) / 0.55)))
        cr = tuple(int(prgb[c] + (rgb[c] - prgb[c]) * k) for c in range(3))
        cy = pyaw + (yaw - pyaw) * k + 0.012 * math.sin(tt * 1.7)
        cp = ppitch + (pitch - ppitch) * k + 0.008 * math.sin(tt * 2.3)

        d.qpos[:] = base_q
        if AY is not None: d.qpos[AY] = cy
        if AP is not None: d.qpos[AP] = cp
        mujoco.mj_forward(m, d)
        for g in head_geoms:
            m.geom_rgba[g] = [cr[0] / 255, cr[1] / 255, cr[2] / 255, 1.0]
        cam.azimuth = float(spec.get('azimuth', 104)) + 8 * math.sin(tt * 0.42)
        r.update_scene(d, camera=cam)
        view = Image.fromarray(r.render())

        canvas = Image.new('RGB', (W, HH), (11, 10, 6))
        canvas.paste(view, (0, HDR))
        dr = ImageDraw.Draw(canvas, 'RGBA')
        dr.rectangle([0, 0, W, HDR], fill=(212, 175, 55, 255))
        dr.text((26, 16), spec.get('title', 'asimov://'), font=F_BIG, fill=(11, 10, 6, 255))
        dr.text((26, 56), spec.get('tagline', 'ASIMOV 1 · MENLO CAD · LOCAL'),
                font=F_SM, fill=(58, 48, 16, 255))

        dr.rectangle([0, HUD_Y, W, HH], fill=(14, 13, 8, 255))
        dr.rectangle([0, HUD_Y, W, HUD_Y + 4], fill=cr + (255,))
        y = HUD_Y + 16
        if s.get('kicker'):
            dr.text((26, y), s['kicker'], font=F_XS, fill=(201, 179, 106, 255)); y += 24
        if s.get('banner'):
            dr.rectangle([22, y, W - 22, y + 52], fill=cr + (255,))
            dr.text((36, y + 11), s['banner'], font=F_BIG, fill=(11, 10, 6, 255)); y += 64
        for ln in s.get('lines', [])[:7]:
            dr.text((26, y), ln, font=F_SM, fill=(255, 246, 218, 255)); y += 24
        if s.get('state'):
            dr.text((26, HH - 74), f"FACE  {s['state']}", font=F_XS, fill=cr + (255,))
        dr.text((26, HH - 52), spec.get('footer',
                'HUMAN://ROOT → æ POLICY → asimov:// → RECEIPT'),
                font=F_XS, fill=(228, 214, 166, 255))
        dr.rectangle([26, HH - 26, W - 26, HH - 18], fill=(212, 175, 55, 70))
        dr.rectangle([26, HH - 26, 26 + int((W - 52) * tt / total), HH - 18],
                     fill=(255, 233, 168, 255))
        canvas.save(frames_dir / f'f{i:05d}.png')
        if i % 100 == 0:
            print(f"  {i}/{nf} t={tt:.2f} {s.get('state','IDLE')}")

    # audio: concat the spoken scenes, pad to the film length
    wavs = [s['_wav'] for s in scenes if s.get('_wav')]
    silent = workdir / 'silent.mp4'
    subprocess.run([str(FF / 'ffmpeg.exe'), '-v', 'error', '-y', '-framerate', str(fps),
                    '-i', str(frames_dir / 'f%05d.png'), '-c:v', 'h264_nvenc',
                    '-preset', 'p5', '-b:v', '6M', '-pix_fmt', 'yuv420p', str(silent)],
                   capture_output=True, timeout=1800)
    if wavs:
        lst = workdir / 'audio.txt'
        lst.write_text(''.join(f"file '{w.as_posix()}'\n" for w in wavs), encoding='utf-8')
        track = workdir / 'track.wav'
        subprocess.run([str(FF / 'ffmpeg.exe'), '-v', 'error', '-y', '-f', 'concat',
                        '-safe', '0', '-i', str(lst), '-ar', '24000', '-ac', '1', str(track)],
                       capture_output=True, timeout=600)
        subprocess.run([str(FF / 'ffmpeg.exe'), '-v', 'error', '-y', '-i', str(silent),
                        '-i', str(track), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
                        '-shortest', str(out_path)], capture_output=True, timeout=900)
    else:
        silent.replace(out_path)

    meta = {'total_s': round(total, 3), 'frames': nf, 'fps': fps,
            'model': 'asimov_1_25dof_actuated.xml', 'source': 'menloresearch/asimov-1',
            'renderer': 'mujoco-native', 'bytes': out_path.stat().st_size,
            'scenes': [{k: v for k, v in s.items() if not k.startswith('_')} | 
                       {'t0': round(s['_t0'], 3), 't1': round(s['_t1'], 3),
                        'spoken': bool(s.get('_wav'))} for s in scenes]}
    (workdir / 'studio.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\n{out_path}  {out_path.stat().st_size} bytes")
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--workdir')
    ap.add_argument('--verify', action='store_true')
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding='utf-8'))
    out = Path(a.out)
    wd = Path(a.workdir) if a.workdir else out.parent / (out.stem + '-studio')
    meta = render(spec, out, wd)
    if a.verify and VIDAEO.exists():
        p = subprocess.run([PY, str(VIDAEO), 'verify', str(out)],
                           capture_output=True, text=True, encoding='utf-8', timeout=900)
        print(p.stdout[-1200:])


if __name__ == '__main__':
    main()
