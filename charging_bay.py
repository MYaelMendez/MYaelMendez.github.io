"""æ:// CHARGING BAY — five robots docked, sharing prompts and responses.

The scene has a reason to be static: they are CHARGING. Downtime is when the
cast talks. Each body sits on a dock with a live charge level; the face tablet
carries expression, viseme and charge; the HUD shows the prompt/response pair
being exchanged.

    python charging_bay.py --spec spec.json --out film.mp4 [--verify]
"""
import argparse, json, math, os, re, subprocess, sys, warnings
from pathlib import Path
import numpy as np
warnings.filterwarnings('ignore')
sys.path.insert(0, str(Path(__file__).resolve().parent))

H = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
PL = Path(os.environ.get('HERMES_AE_HOME', H / 'plugins' / 'hermes-ae'))
PY = os.environ.get('HERMES_AE_PYTHON', sys.executable)
FF = H / 'tools' / 'ffmpeg-7.1-nvenc' / 'bin'
TTS = H / 'plugins' / 'tiny-voca-voice' / 'scripts' / 'tiny_voca_voice.py'
VIDAEO = Path('C:/æ/vidæo/vidæo.py')

W, HH, HDR, VH = 720, 1280, 92, 720
HUD = HDR + VH
FOVY = 45.0

CAST = {
    'nous':   dict(pfx='',   rgb=(255, 64, 220), voice='F2', speed=1.00, shift=0.0,  rng=1.00, label='nous girl'),
    'hermes': dict(pfx='b_', rgb=(0, 170, 255),  voice='M2', speed=1.00, shift=0.0,  rng=1.00, label='hermes-agent'),
    'waetz':  dict(pfx='c_', rgb=(245, 245, 250), voice='M2', speed=1.02, shift=2.0,  rng=1.30, label='wætz'),
    'menlo':  dict(pfx='d_', rgb=(255, 150, 0),  voice='M2', speed=0.94, shift=-3.5, rng=0.65, label='menlo-research'),
    'asimov': dict(pfx='e_', rgb=(0, 255, 120),  voice='F2', speed=1.06, shift=-1.5, rng=0.35, label='asimov-agent'),
}
ORDER = ['nous', 'hermes', 'waetz', 'menlo', 'asimov']
STATE_RGB = {'IDLE': (150,150,155), 'LISTENING': (0,204,255), 'SPEAKING': (0,255,159),
             'THINKING': (133,233,252), 'AWAITING_APPROVAL': (212,175,55),
             'APPROVED': (0,255,159), 'REFUSED': (255,0,255), 'ERROR': (255,59,71)}


def build(sep=0.46):
    import mujoco
    src = (PL / 'model/xml/asimov_1_25dof_actuated.xml').read_text(encoding='utf-8')
    src = re.sub(r'meshdir="[^"]*"', f'meshdir="{(PL/"model/meshes").as_posix()}"', src)
    vis = f'<visual><global offwidth="{W}" offheight="{VH}"/><quality shadowsize="4096"/></visual>'
    src = re.sub(r'<visual>.*?</visual>', vis, src, count=1, flags=re.S) if '<visual>' in src \
        else src.replace('</mujoco>', vis + '</mujoco>')
    parent = mujoco.MjSpec.from_string(src)
    ys = {n: (i - 2) * sep for i, n in enumerate(ORDER)}
    first = parent.worldbody.first_body()
    first.pos = [0, ys['nous'], float(first.pos[2])]
    for n in ORDER[1:]:
        child = mujoco.MjSpec.from_string(src)
        parent.worldbody.add_frame(pos=[0, ys[n], 0]).attach_body(
            child.worldbody.first_body(), CAST[n]['pfx'], '')
    # charging docks: a pad + a status light under each body
    for n in ORDER:
        pad = parent.worldbody.add_body(name=f'dock_{n}', pos=[0, ys[n], 0.012])
        pad.add_geom(type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.20, 0.17, 0.012],
                     rgba=[0.10, 0.10, 0.12, 1], contype=0, conaffinity=0)
        strip = parent.worldbody.add_body(name=f'strip_{n}', pos=[0.19, ys[n], 0.026])
        strip.add_geom(type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.008, 0.15, 0.004],
                       rgba=[c / 255 for c in CAST[n]['rgb']] + [1],
                       contype=0, conaffinity=0)
    m = parent.compile(); d = mujoco.MjData(m)
    d.ctrl[:] = np.clip(0.0, m.actuator_ctrlrange[:, 0], m.actuator_ctrlrange[:, 1])
    for _ in range(1500): mujoco.mj_step(m, d)
    mujoco.mj_forward(m, d)
    return mujoco, m, d, ys


def speak(text, actor, out):
    c = CAST[actor]
    if not TTS.exists(): return None
    env = dict(os.environ); env['HERMES_HOME'] = str(H)
    env.setdefault('TINY_VOCA_HOME', str(H / 'tiny-voca'))
    for k in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV'): env.pop(k, None)
    p = subprocess.run([PY, str(TTS), '--text', text, '--voice', c['voice'],
                        '--speed', str(c['speed']), '--pitch-shift', str(c['shift']),
                        '--pitch-range', str(c['rng']), '--output', str(out)],
                       capture_output=True, text=True, encoding='utf-8', timeout=300, env=env)
    try:
        return out if json.loads(p.stdout).get('success') else None
    except Exception:
        return None


def project(pt, lookat, az, el, dist, w, h):
    a, e = math.radians(az), math.radians(el)
    dv = np.array([math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), math.sin(e)])
    eye = np.asarray(lookat) + dist*dv
    fwd = np.asarray(lookat)-eye; fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, np.array([0.,0.,1.])); right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    rel = np.asarray(pt)-eye
    z = float(np.dot(rel, fwd))
    if z <= 1e-6: return None
    f = (h/2.0)/math.tan(math.radians(FOVY)/2.0)
    return (w/2.0 + f*float(np.dot(rel,right))/z, h/2.0 - f*float(np.dot(rel,up))/z, z, f)


def render(spec, out_path, wd):
    import mujoco
    from PIL import Image, ImageDraw, ImageFont
    from robot_face2 import face as make_face
    mujoco, m, d, ys = build(float(spec.get('separation', 0.46)))
    base_q = d.qpos.copy()

    def jadr(n):
        j = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_JOINT, n)
        return int(m.jnt_qposadr[j]) if j >= 0 else None
    A = {}
    for n in ORDER:
        p = CAST[n]['pfx']
        hb = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, p+'neck_pitch_link')
        A[n] = dict(body=hb, geoms=[g for g in range(m.ngeom) if m.geom_bodyid[g]==hb],
                    yaw=jadr(p+'neck_yaw_joint'), pitch=jadr(p+'neck_pitch_joint'),
                    y=ys[n], **CAST[n])
    fps = int(spec.get('fps', 24)); scenes = spec['scenes']
    wd.mkdir(parents=True, exist_ok=True); fd = wd/'frames'; fd.mkdir(exist_ok=True)

    t = 0.0
    for i, s in enumerate(scenes):
        who = s.get('speaker', 'waetz')
        s['_who'] = who
        wav = speak(s['speak'], who, wd/f's{i}.wav') if s.get('speak') else None
        dur = (wav.stat().st_size/48000.0) if (wav and wav.exists()) else float(s.get('dur', 3.0))
        s['_t0'], s['_t1'], s['_wav'] = t, t+dur, wav
        t += dur
    total, nf = t, int(round(t*fps))
    print(f"scenes={len(scenes)} total={total:.2f}s frames={nf}@{fps}")

    def font(sz, bold=False):
        p = f"C:/Windows/Fonts/{'consolab' if bold else 'consola'}.ttf"
        return ImageFont.truetype(p, sz) if Path(p).exists() else ImageFont.load_default()
    F_T, F_B, F_M, F_S, F_X = font(26,True), font(19,True), font(15,True), font(14), font(12)

    r = mujoco.Renderer(m, height=VH, width=W)
    cam = mujoco.MjvCamera(); cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    smooth = lambda k: k*k*(3-2*k)
    charge0 = spec.get('charge_start', {})

    for i in range(nf):
        tt = i/fps
        s, idx = scenes[0], 0
        for k, sc in enumerate(scenes):
            if sc['_t0'] <= tt < sc['_t1']: s, idx = sc, k; break
        if tt >= scenes[-1]['_t1']: s, idx = scenes[-1], len(scenes)-1
        who = s['_who']; st = s.get('state', 'SPEAKING')
        rgb = STATE_RGB.get(st, (212,175,55))
        prev = scenes[max(0, idx-1)]
        prgb = STATE_RGB.get(prev.get('state','IDLE'), rgb)
        k = smooth(min(1.0, max(0.0, (tt-s['_t0'])/0.5)))
        cr = tuple(int(prgb[c]+(rgb[c]-prgb[c])*k) for c in range(3))

        # charge climbs over the film
        chg = {n: min(1.0, charge0.get(n, 0.30) + 0.55*(tt/total)) for n in ORDER}
        close = s.get('camera') == 'face'

        d.qpos[:] = base_q
        for n, a in A.items():
            active = (n == who)
            col = cr if active else tuple(int(v*0.6) for v in a['rgb'])
            toward = -0.26 if a['y'] > 0 else 0.26
            # in a face close-up the speaker faces camera, not the others
            if close and active:
                yy = 0.0 + 0.008*math.sin(tt*1.5)
            else:
                yy = (toward*1.4 if active else toward*0.5) + 0.010*math.sin(tt*1.5+hash(n)%7)
            if a['yaw'] is not None: d.qpos[a['yaw']] = yy
            if a['pitch'] is not None: d.qpos[a['pitch']] = 0.02*math.sin(tt*1.9)
            for g in a['geoms']:
                m.geom_rgba[g] = [col[0]/255, col[1]/255, col[2]/255, 1.0]
        mujoco.mj_forward(m, d)

        if close:
            hp = d.xpos[A[who]['body']].copy()
            lookat = hp + np.array([0.0, 0.0, 0.03]); dist = 0.66; az, el = 180, -2
        else:
            lookat = np.array([0.0, 0.0, 0.66]); dist = float(spec.get('distance', 4.7))
            az = 180 + 5*math.sin(tt*0.3); el = -3
        cam.lookat = lookat; cam.distance = dist; cam.azimuth = az; cam.elevation = el
        r.update_scene(d, camera=cam)
        img = Image.fromarray(r.render())

        # faces on every head (wide) or just the speaker (close)
        for n, a in A.items():
            if close and n != who: continue
            hp = d.xpos[a['body']].copy()
            pr = project(hp + np.array([0.078, 0.0, 0.040]), lookat, az, el, dist, W, VH)
            if not pr: continue
            px, py, z, f = pr
            fw = (f*0.115)/z
            fh = fw*0.66
            if fw < 14: continue
            active = (n == who)
            vis = 0
            if active and st == 'SPEAKING':
                vis = [2,3,5,4,2,6,3,7][int(tt*7) % 8]
            bl = 1.0 if math.sin(tt*2.3 + hash(n)%5) > 0.975 else 0.0
            gz = (0.35 if a['y']>0 else -0.35, 0.0) if not active else (0.0, 0.0)
            fimg = make_face((int(fw), int(fh)), cr if active else a['rgb'],
                             viseme=vis, blink=bl, gaze=gz, charge=chg[n],
                             state=st if active else 'LISTENING',
                             glow=1.2 if active else 0.6)
            img.paste(fimg, (int(px-fw/2), int(py-fh/2)), fimg)

        canvas = Image.new('RGB', (W, HH), (11,10,6)); canvas.paste(img, (0, HDR))
        dr = ImageDraw.Draw(canvas, 'RGBA')
        dr.rectangle([0,0,W,HDR], fill=(212,175,55,255))
        dr.text((26,15), spec.get('title','æ:// CHARGING BAY'), font=F_T, fill=(11,10,6,255))
        dr.text((26,54), spec.get('tagline','DOCKED · SHARING PROMPTS AND RESPONSES'), font=F_S, fill=(58,48,16,255))

        dr.rectangle([0,HUD,W,HH], fill=(14,13,8,255))
        dr.rectangle([0,HUD,W,HUD+4], fill=cr+(255,))
        y = HUD+14
        # charge row
        x = 22
        for n in ORDER:
            a = A[n]; on = (n == who); col = a['rgb'] if on else (78,72,52)
            lbl = f"{a['label']} {int(chg[n]*100)}%"
            tw = dr.textlength(lbl, font=F_X)+14
            if x+tw > W-18: x = 22; y += 26
            dr.rectangle([x,y,x+tw,y+22], fill=col+(255,))
            dr.text((x+7,y+4), lbl, font=F_X, fill=(11,10,6,255)); x += tw+5
        y += 32
        if s.get('kicker'):
            dr.text((26,y), s['kicker'], font=F_X, fill=(201,179,106,255)); y += 21
        if s.get('prompt'):
            dr.rectangle([22,y,W-22,y+30], fill=(212,175,55,42))
            dr.text((30,y+7), '▸ '+s['prompt'], font=F_S, fill=(255,233,168,255)); y += 38
        if s.get('banner'):
            dr.rectangle([22,y,W-22,y+46], fill=cr+(255,))
            dr.text((32,y+10), s['banner'], font=F_B, fill=(11,10,6,255)); y += 56
        for ln in s.get('lines', [])[:4]:
            dr.text((26,y), ln, font=F_S, fill=(255,246,218,255)); y += 22
        dr.text((26,HH-48), spec.get('footer','HUMAN://ROOT → wætz → æ POLICY → RECEIPT'),
                font=F_X, fill=(228,214,166,255))
        dr.rectangle([26,HH-24,W-26,HH-17], fill=(212,175,55,70))
        dr.rectangle([26,HH-24,26+int((W-52)*tt/total),HH-17], fill=(255,233,168,255))
        canvas.save(fd/f'f{i:05d}.png')
        if i % 100 == 0: print(f"  {i}/{nf} t={tt:.2f} {who} {st} cam={'face' if close else 'wide'}")

    silent = wd/'silent.mp4'
    subprocess.run([str(FF/'ffmpeg.exe'),'-v','error','-y','-framerate',str(fps),
                    '-i',str(fd/'f%05d.png'),'-c:v','h264_nvenc','-preset','p5',
                    '-b:v','6M','-pix_fmt','yuv420p',str(silent)], capture_output=True, timeout=2400)
    wavs = [s['_wav'] for s in scenes if s.get('_wav')]
    if wavs:
        lst = wd/'audio.txt'
        lst.write_text(''.join(f"file '{w.as_posix()}'\n" for w in wavs), encoding='utf-8')
        track = wd/'track.wav'
        subprocess.run([str(FF/'ffmpeg.exe'),'-v','error','-y','-f','concat','-safe','0',
                        '-i',str(lst),'-ar','24000','-ac','1',str(track)], capture_output=True, timeout=600)
        subprocess.run([str(FF/'ffmpeg.exe'),'-v','error','-y','-i',str(silent),'-i',str(track),
                        '-c:v','copy','-filter:a',f'apad=whole_dur={total:.6f}','-c:a','aac','-b:a','128k','-movflags','+faststart',
                        '-t',f'{total:.6f}',str(out_path)], capture_output=True, timeout=900)
    else:
        silent.replace(out_path)
    meta = dict(total_s=round(total,3), frames=nf, fps=fps, bytes=out_path.stat().st_size,
                scene='charging-bay', faststart=True,
                scenes=[{k:v for k,v in s.items() if not k.startswith('_')} |
                        {'t0':round(s['_t0'],3),'t1':round(s['_t1'],3),'speaker':s['_who']}
                        for s in scenes])
    (wd/'studio.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False), encoding='utf-8')
    print(f"\n{out_path}  {out_path.stat().st_size} bytes")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--workdir'); ap.add_argument('--verify', action='store_true')
    ap.add_argument('--smoke', type=int, default=0)
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding='utf-8'))
    if a.smoke: spec['scenes'] = spec['scenes'][:a.smoke]
    out = Path(a.out)
    wd = Path(a.workdir) if a.workdir else out.parent/(out.stem+'-studio')
    render(spec, out, wd)
    if a.verify and VIDAEO.exists():
        p = subprocess.run([PY,str(VIDAEO),'verify',str(out)], capture_output=True,
                           text=True, encoding='utf-8', timeout=900)
        print(p.stdout[-800:])


if __name__ == '__main__':
    main()
