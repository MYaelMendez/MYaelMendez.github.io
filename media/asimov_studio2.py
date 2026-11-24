"""æ:// ASIMOV STUDIO v2 — one or two Asimov bodies, camera presets, dialogue.

The spec commands. Never edit this file to change a film.

    python asimov_studio2.py --spec spec.json --out film.mp4 [--verify]

Spec:
{
  "title": "...", "tagline": "...", "fps": 24,
  "cast": "pair",                 // "solo" | "pair"
  "camera": "front",              // front|three_quarter|side|back|low|high|orbit
  "scenes": [
    {"kicker":"...", "speaker":"nous", "state":"SPEAKING",
     "lines":["..."], "banner":"...",
     "speak":"...", "voice":"F2"}
  ]
}

Cast: nous girl = F2 = magenta head. hermes-agent = M2 = cyan head.
In a pair scene the speaker turns toward the other; the listener dims.
Geometry: menloresearch/asimov-1, hash-verified. Renderer: native MuJoCo.
"""
import argparse, json, math, os, re, subprocess, sys, warnings
from pathlib import Path
import numpy as np
warnings.filterwarnings('ignore')

H = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
PL = Path(os.environ.get('HERMES_AE_HOME', H / 'plugins' / 'hermes-ae'))
PY = os.environ.get('HERMES_AE_PYTHON', sys.executable)
FF = H / 'tools' / 'ffmpeg-7.1-nvenc' / 'bin'
TTS = H / 'plugins' / 'tiny-voca-voice' / 'scripts' / 'tiny_voca_voice.py'
VIDAEO = Path('C:/æ/vidæo/vidæo.py')

W, HH, HDR, VIEW_H = 720, 1280, 92, 800
HUD_Y = HDR + VIEW_H

# camera presets. The robot faces +X; azimuth 180 with Y-separation is FRONT.
CAMERAS = {
    'front':         dict(az=180, el=-3,  dist=3.0, look=0.70),
    'three_quarter': dict(az=155, el=-4,  dist=3.0, look=0.70),
    'side':          dict(az=90,  el=-3,  dist=3.0, look=0.70),
    'back':          dict(az=0,   el=-3,  dist=3.0, look=0.70),
    'low':           dict(az=180, el=-14, dist=2.8, look=0.55),
    'high':          dict(az=180, el=16,  dist=3.2, look=0.80),
    'close':         dict(az=180, el=-2,  dist=1.9, look=1.02),
    'orbit':         dict(az=180, el=-3,  dist=3.0, look=0.70, orbit=22),
}
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
CAST = {
    'nous':   dict(prefix='',   rgb=(255, 64, 220), voice='F2', label='nous girl'),
    'hermes': dict(prefix='b_', rgb=(0, 170, 255),  voice='M2', label='hermes-agent'),
}


def build(cast='pair', sep=0.42):
    import mujoco
    src = (PL / 'model/xml/asimov_1_25dof_actuated.xml').read_text(encoding='utf-8')
    src = re.sub(r'meshdir="[^"]*"', f'meshdir="{(PL/"model/meshes").as_posix()}"', src)
    vis = f'<visual><global offwidth="{W}" offheight="{VIEW_H}"/><quality shadowsize="4096"/></visual>'
    src = re.sub(r'<visual>.*?</visual>', vis, src, count=1, flags=re.S) if '<visual>' in src \
        else src.replace('</mujoco>', vis + '</mujoco>')
    parent = mujoco.MjSpec.from_string(src)
    if cast == 'pair':
        child = mujoco.MjSpec.from_string(src)
        first = parent.worldbody.first_body()
        first.pos = [0, -sep, float(first.pos[2])]      # keep the 0.630 stand height
        parent.worldbody.add_frame(pos=[0, sep, 0]).attach_body(
            child.worldbody.first_body(), 'b_', '')
    m = parent.compile()
    d = mujoco.MjData(m)
    d.ctrl[:] = np.clip(0.0, m.actuator_ctrlrange[:, 0], m.actuator_ctrlrange[:, 1])
    for _ in range(1500):
        mujoco.mj_step(m, d)
    mujoco.mj_forward(m, d)
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
        return out if json.loads(p.stdout).get('success') else None
    except Exception:
        return None


def render(spec, out_path, wd):
    from PIL import Image, ImageDraw, ImageFont
    cast = spec.get('cast', 'solo')
    mujoco, m, d = build(cast, float(spec.get('separation', 0.42)))
    base_q = d.qpos.copy()

    def jadr(name):
        j = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_JOINT, name)
        return int(m.jnt_qposadr[j]) if j >= 0 else None

    actors = {}
    keys = ['nous', 'hermes'] if cast == 'pair' else ['nous']
    for k in keys:
        c = CAST[k]
        p = c['prefix']
        hb = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, p + 'neck_pitch_link')
        geoms = [g for g in range(m.ngeom) if m.geom_bodyid[g] == hb]
        actors[k] = dict(geoms=geoms, yaw=jadr(p + 'neck_yaw_joint'),
                         pitch=jadr(p + 'neck_pitch_joint'), **c)
    print(f"cast={cast} actors={list(actors)} nq={m.nq} geoms={m.ngeom}")

    fps = int(spec.get('fps', 24))
    scenes = spec['scenes']
    wd.mkdir(parents=True, exist_ok=True)
    fd = wd / 'frames'; fd.mkdir(exist_ok=True)

    t = 0.0
    for i, s in enumerate(scenes):
        wav = None
        if s.get('speak'):
            who = s.get('speaker', 'hermes' if cast == 'pair' else 'nous')
            voice = s.get('voice') or CAST.get(who, CAST['nous'])['voice']
            s['_voice'] = voice
            wav = speak(s['speak'], voice, wd / f's{i}.wav')
        dur = (wav.stat().st_size / 48000.0) if (wav and wav.exists()) else float(s.get('dur', 3.0))
        s['_t0'], s['_t1'], s['_wav'] = t, t + dur, wav
        t += dur
    total, nf = t, int(round(t * fps))
    print(f"scenes={len(scenes)} total={total:.3f}s frames={nf}@{fps}")

    def font(sz, bold=False):
        p = f"C:/Windows/Fonts/{'consolab' if bold else 'consola'}.ttf"
        return ImageFont.truetype(p, sz) if Path(p).exists() else ImageFont.load_default()
    F_BIG, F_SM, F_XS = font(27, True), font(15), font(13)

    r = mujoco.Renderer(m, height=VIEW_H, width=W)
    cam = mujoco.MjvCamera(); cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    smooth = lambda k: k * k * (3 - 2 * k)

    for i in range(nf):
        tt = i / fps
        s, idx = scenes[0], 0
        for k, sc in enumerate(scenes):
            if sc['_t0'] <= tt < sc['_t1']:
                s, idx = sc, k; break
        if tt >= scenes[-1]['_t1']:
            s, idx = scenes[-1], len(scenes) - 1
        prev = scenes[max(0, idx - 1)]
        who = s.get('speaker', 'nous')
        rgb, yaw, pitch = STATES.get(s.get('state', 'IDLE'), STATES['IDLE'])
        prgb, pyaw, ppitch = STATES.get(prev.get('state', 'IDLE'), STATES['IDLE'])
        k = smooth(min(1.0, max(0.0, (tt - s['_t0']) / 0.5)))
        cr = tuple(int(prgb[c] + (rgb[c] - prgb[c]) * k) for c in range(3))

        d.qpos[:] = base_q
        for name, A in actors.items():
            if cast == 'pair':
                active = (name == who)
                base_rgb = A['rgb']
                # speaker wears the state colour; listener keeps its identity, dimmed
                col = cr if active else tuple(int(v * 0.55) for v in base_rgb)
                turn = (-0.34 if name == 'nous' else 0.34) if active else \
                       (0.16 if name == 'nous' else -0.16)
                yy = turn + 0.012 * math.sin(tt * 1.7 + (0 if name == 'nous' else 1.6))
                pp = (pitch if active else 0.0) + 0.008 * math.sin(tt * 2.1)
            else:
                col, yy, pp = cr, yaw + 0.012 * math.sin(tt * 1.7), pitch + 0.008 * math.sin(tt * 2.3)
            if A['yaw'] is not None: d.qpos[A['yaw']] = yy
            if A['pitch'] is not None: d.qpos[A['pitch']] = pp
            for g in A['geoms']:
                m.geom_rgba[g] = [col[0] / 255, col[1] / 255, col[2] / 255, 1.0]
        mujoco.mj_forward(m, d)

        cp = CAMERAS.get(s.get('camera', spec.get('camera', 'front')), CAMERAS['front'])
        cam.lookat = np.array([0.0, 0.0, cp['look']])
        cam.distance = cp['dist']; cam.elevation = cp['el']
        cam.azimuth = cp['az'] + cp.get('orbit', 0) * math.sin(tt * 0.35)
        r.update_scene(d, camera=cam)
        view = Image.fromarray(r.render())

        canvas = Image.new('RGB', (W, HH), (11, 10, 6))
        canvas.paste(view, (0, HDR))
        dr = ImageDraw.Draw(canvas, 'RGBA')
        dr.rectangle([0, 0, W, HDR], fill=(212, 175, 55, 255))
        dr.text((26, 16), spec.get('title', 'æ:// ASIMOV STUDIO'), font=F_BIG, fill=(11, 10, 6, 255))
        dr.text((26, 56), spec.get('tagline', 'MENLO CAD · NATIVE MUJOCO · LOCAL'),
                font=F_SM, fill=(58, 48, 16, 255))

        dr.rectangle([0, HUD_Y, W, HH], fill=(14, 13, 8, 255))
        dr.rectangle([0, HUD_Y, W, HUD_Y + 4], fill=cr + (255,))
        y = HUD_Y + 16
        if cast == 'pair':
            x = 26
            for name, A in actors.items():
                on = (name == who)
                col = A['rgb'] if on else (90, 84, 60)
                lbl = A['label'] + (' ●' if on else '')
                tw = dr.textlength(lbl, font=F_XS) + 18
                dr.rectangle([x, y, x + tw, y + 24], fill=col + (255,))
                dr.text((x + 9, y + 5), lbl, font=F_XS, fill=(11, 10, 6, 255))
                x += tw + 8
            y += 34
        if s.get('kicker'):
            dr.text((26, y), s['kicker'], font=F_XS, fill=(201, 179, 106, 255)); y += 22
        if s.get('banner'):
            dr.rectangle([22, y, W - 22, y + 50], fill=cr + (255,))
            dr.text((36, y + 10), s['banner'], font=F_BIG, fill=(11, 10, 6, 255)); y += 62
        for ln in s.get('lines', [])[:6]:
            dr.text((26, y), ln, font=F_SM, fill=(255, 246, 218, 255)); y += 23
        dr.text((26, HH - 52), spec.get('footer', 'HUMAN://ROOT → æ POLICY → asimov:// → RECEIPT'),
                font=F_XS, fill=(228, 214, 166, 255))
        dr.rectangle([26, HH - 26, W - 26, HH - 18], fill=(212, 175, 55, 70))
        dr.rectangle([26, HH - 26, 26 + int((W - 52) * tt / total), HH - 18], fill=(255, 233, 168, 255))
        canvas.save(fd / f'f{i:05d}.png')
        if i % 100 == 0:
            print(f"  {i}/{nf} t={tt:.2f} {who} {s.get('state','IDLE')}")

    silent = wd / 'silent.mp4'
    subprocess.run([str(FF / 'ffmpeg.exe'), '-v', 'error', '-y', '-framerate', str(fps),
                    '-i', str(fd / 'f%05d.png'), '-c:v', 'h264_nvenc', '-preset', 'p5',
                    '-b:v', '6M', '-pix_fmt', 'yuv420p', str(silent)],
                   capture_output=True, timeout=1800)
    wavs = [s['_wav'] for s in scenes if s.get('_wav')]
    if wavs:
        lst = wd / 'audio.txt'
        lst.write_text(''.join(f"file '{w.as_posix()}'\n" for w in wavs), encoding='utf-8')
        track = wd / 'track.wav'
        subprocess.run([str(FF / 'ffmpeg.exe'), '-v', 'error', '-y', '-f', 'concat', '-safe', '0',
                        '-i', str(lst), '-ar', '24000', '-ac', '1', str(track)],
                       capture_output=True, timeout=600)
        subprocess.run([str(FF / 'ffmpeg.exe'), '-v', 'error', '-y', '-i', str(silent),
                        '-i', str(track), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
                        '-shortest', str(out_path)], capture_output=True, timeout=900)
    else:
        silent.replace(out_path)

    meta = dict(total_s=round(total, 3), frames=nf, fps=fps, cast=cast,
                camera=spec.get('camera', 'front'), bytes=out_path.stat().st_size,
                model='asimov_1_25dof_actuated.xml', source='menloresearch/asimov-1',
                scenes=[{k: v for k, v in s.items() if not k.startswith('_')} |
                        {'t0': round(s['_t0'], 3), 't1': round(s['_t1'], 3),
                         'voice': s.get('_voice'), 'spoken': bool(s.get('_wav'))} for s in scenes])
    (wd / 'studio.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')
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
    render(spec, out, wd)
    if a.verify and VIDAEO.exists():
        p = subprocess.run([PY, str(VIDAEO), 'verify', str(out)],
                           capture_output=True, text=True, encoding='utf-8', timeout=900)
        print(p.stdout[-1000:])


if __name__ == '__main__':
    main()
