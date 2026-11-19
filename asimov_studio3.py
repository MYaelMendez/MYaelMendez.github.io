"""æ:// ASIMOV STUDIO v3 — mixture of robots.

Five bodies. wætz is the human's digital twin: the remote pilot the others
support while he learns to write the policy. Per-actor derived voices, a face
camera that tracks the speaker, and a face tablet rendered on the CAD head.

    python asimov_studio3.py --spec spec.json --out film.mp4 [--verify]

Spec:
{ "title","tagline","fps","cast":"five|pair|solo","camera":"front",
  "scenes":[{"speaker":"waetz","state":"SPEAKING","camera":"face",
             "kicker","banner","lines":[...],"speak":"..."}] }

Geometry: menloresearch/asimov-1, hash-verified. Renderer: native MuJoCo.
The spec commands; never edit this file to change a film.
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
FOVY = 45.0

# actor -> prefix, head colour, voice derivation (measured distinct by centroid)
CAST = {
    'nous':   dict(pfx='',   rgb=(255, 64, 220), voice='F2', speed=1.00, shift=0.0,  rng=1.00,
                   label='nous girl',      role='root voice'),
    'hermes': dict(pfx='b_', rgb=(0, 170, 255),  voice='M2', speed=1.00, shift=0.0,  rng=1.00,
                   label='hermes-agent',   role='build voice'),
    'waetz':  dict(pfx='c_', rgb=(245, 245, 250), voice='M2', speed=1.02, shift=2.0,  rng=1.30,
                   label='wætz',           role='human digital twin · test pilot'),
    'menlo':  dict(pfx='d_', rgb=(255, 150, 0),  voice='M2', speed=0.94, shift=-3.5, rng=0.65,
                   label='menlo-research', role='upstream source'),
    'asimov': dict(pfx='e_', rgb=(0, 255, 120),  voice='F2', speed=1.06, shift=-1.5, rng=0.35,
                   label='asimov-agent',   role='robot body'),
}
ORDER = ['nous', 'hermes', 'waetz', 'menlo', 'asimov']   # wætz at centre

CAMERAS = {
    'front':         dict(az=180, el=-3,  look=0.70),
    'three_quarter': dict(az=155, el=-4,  look=0.70),
    'side':          dict(az=90,  el=-3,  look=0.70),
    'back':          dict(az=0,   el=-3,  look=0.70),
    'low':           dict(az=180, el=-14, look=0.55),
    'high':          dict(az=180, el=16,  look=0.80),
    'orbit':         dict(az=180, el=-3,  look=0.70, orbit=20),
    'face':          dict(az=180, el=-2,  look=0.03, dist=0.62, track=True),
    'pilot':         dict(az=180, el=-2,  look=0.30, dist=1.55, track='waetz'),
}
DIST_BY_CAST = {'solo': 2.35, 'pair': 3.0, 'five': 4.8}
STATES = {
    'IDLE': ((150,150,155), 0.0, 0.0), 'LISTENING': ((0,204,255), 0.0, 0.0),
    'SPEAKING': ((0,255,159), 0.0, -0.08), 'THINKING': ((133,233,252), 0.18, -0.04),
    'AWAITING_APPROVAL': ((212,175,55), 0.38, 0.06), 'APPROVED': ((0,255,159), 0.0, -0.10),
    'REFUSED': ((255,0,255), -0.62, 0.20), 'ERROR': ((255,59,71), -0.30, 0.24),
}


def build(cast='five', sep=0.42):
    import mujoco
    src = (PL / 'model/xml/asimov_1_25dof_actuated.xml').read_text(encoding='utf-8')
    src = re.sub(r'meshdir="[^"]*"', f'meshdir="{(PL/"model/meshes").as_posix()}"', src)
    vis = f'<visual><global offwidth="{W}" offheight="{VIEW_H}"/><quality shadowsize="4096"/></visual>'
    src = re.sub(r'<visual>.*?</visual>', vis, src, count=1, flags=re.S) if '<visual>' in src \
        else src.replace('</mujoco>', vis + '</mujoco>')
    names = ORDER if cast == 'five' else (['nous', 'hermes'] if cast == 'pair' else ['nous'])
    # keep wætz centred in every cast size
    if cast == 'pair':
        names = ['waetz', 'hermes']
    n = len(names)
    ys = {nm: (i - (n - 1) / 2) * sep for i, nm in enumerate(names)}
    parent = mujoco.MjSpec.from_string(src)
    first = parent.worldbody.first_body()
    a0 = CAST[names[0]]
    first.pos = [0, ys[names[0]], float(first.pos[2])]
    for nm in names[1:]:
        child = mujoco.MjSpec.from_string(src)
        parent.worldbody.add_frame(pos=[0, ys[nm], 0]).attach_body(
            child.worldbody.first_body(), CAST[nm]['pfx'], '')
    m = parent.compile(); d = mujoco.MjData(m)
    d.ctrl[:] = np.clip(0.0, m.actuator_ctrlrange[:, 0], m.actuator_ctrlrange[:, 1])
    for _ in range(1500): mujoco.mj_step(m, d)
    mujoco.mj_forward(m, d)
    return mujoco, m, d, names, a0


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
    dirv = np.array([math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), math.sin(e)])
    eye = np.asarray(lookat) + dist*dirv
    fwd = np.asarray(lookat)-eye; fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, np.array([0.,0.,1.])); right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    rel = np.asarray(pt)-eye
    z = float(np.dot(rel, fwd))
    if z <= 1e-6: return None
    f = (h/2.0)/math.tan(math.radians(FOVY)/2.0)
    return (w/2.0 + f*float(np.dot(rel,right))/z, h/2.0 - f*float(np.dot(rel,up))/z, z, f)


def tablet(img, cx, cy, scale, rgb, mouth=0.12, blink=1.0):
    from PIL import ImageDraw
    dr = ImageDraw.Draw(img, 'RGBA')
    tw, th = 150*scale, 96*scale
    x0, y0 = cx-tw/2, cy-th/2
    dr.rectangle([x0,y0,x0+tw,y0+th], fill=(8,8,10,235), outline=rgb+(255,),
                 width=max(1,int(2*scale)))
    ew, eh = 30*scale, 12*scale*blink
    ey = cy-12*scale
    for ex in (cx-26*scale, cx+26*scale):
        dr.rectangle([ex-ew/2,ey-eh/2,ex+ew/2,ey+eh/2], fill=rgb+(255,))
    mw, mh = 46*scale, max(2*scale, 16*scale*mouth)
    my = cy+24*scale
    dr.rectangle([cx-mw/2,my-mh/2,cx+mw/2,my+mh/2], fill=rgb+(255,))


def render(spec, out_path, wd):
    from PIL import Image, ImageDraw, ImageFont
    cast = spec.get('cast', 'five')
    mujoco, m, d, names, a0 = build(cast, float(spec.get('separation', 0.42)))
    base_q = d.qpos.copy()

    def jadr(n):
        j = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_JOINT, n)
        return int(m.jnt_qposadr[j]) if j >= 0 else None
    actors = {}
    for nm in names:
        c = CAST[nm]; p = c['pfx']
        hb = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, p+'neck_pitch_link')
        actors[nm] = dict(geoms=[g for g in range(m.ngeom) if m.geom_bodyid[g]==hb],
                          yaw=jadr(p+'neck_yaw_joint'), pitch=jadr(p+'neck_pitch_joint'),
                          body=hb, **c)
    print(f"cast={cast} actors={names} nq={m.nq} geoms={m.ngeom}")

    fps = int(spec.get('fps', 24)); scenes = spec['scenes']
    wd.mkdir(parents=True, exist_ok=True); fd = wd/'frames'; fd.mkdir(exist_ok=True)
    t = 0.0
    for i, s in enumerate(scenes):
        who = s.get('speaker', 'waetz')
        if who not in actors: who = names[0]
        s['_who'] = who
        wav = speak(s['speak'], who, wd/f's{i}.wav') if s.get('speak') else None
        dur = (wav.stat().st_size/48000.0) if (wav and wav.exists()) else float(s.get('dur',3.0))
        s['_t0'], s['_t1'], s['_wav'] = t, t+dur, wav
        t += dur
    total, nf = t, int(round(t*fps))
    print(f"scenes={len(scenes)} total={total:.3f}s frames={nf}@{fps}")

    def font(sz, bold=False):
        p = f"C:/Windows/Fonts/{'consolab' if bold else 'consola'}.ttf"
        return ImageFont.truetype(p, sz) if Path(p).exists() else ImageFont.load_default()
    F_BIG, F_SM, F_XS = font(26,True), font(15), font(12)

    r = mujoco.Renderer(m, height=VIEW_H, width=W)
    cam = mujoco.MjvCamera(); cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    smooth = lambda k: k*k*(3-2*k)
    default_dist = DIST_BY_CAST.get(cast, 3.0)

    for i in range(nf):
        tt = i/fps
        s, idx = scenes[0], 0
        for k, sc in enumerate(scenes):
            if sc['_t0'] <= tt < sc['_t1']: s, idx = sc, k; break
        if tt >= scenes[-1]['_t1']: s, idx = scenes[-1], len(scenes)-1
        prev = scenes[max(0, idx-1)]
        who = s['_who']
        rgb, yaw, pitch = STATES.get(s.get('state','IDLE'), STATES['IDLE'])
        prgb, pyaw, ppitch = STATES.get(prev.get('state','IDLE'), STATES['IDLE'])
        k = smooth(min(1.0, max(0.0,(tt-s['_t0'])/0.5)))
        cr = tuple(int(prgb[c]+(rgb[c]-prgb[c])*k) for c in range(3))

        d.qpos[:] = base_q
        for nm, A in actors.items():
            active = (nm == who)
            if len(actors) > 1:
                col = cr if active else tuple(int(v*0.55) for v in A['rgb'])
                # everyone turns slightly toward the pilot; the speaker turns more
                toward = -0.22 if A.get('_y',0) > 0 else 0.22
                yy = (toward*1.5 if active else toward*0.6) + 0.012*math.sin(tt*1.7+hash(nm)%7)
                pp = (pitch if active else 0.0) + 0.008*math.sin(tt*2.1)
            else:
                col, yy, pp = cr, yaw+0.012*math.sin(tt*1.7), pitch+0.008*math.sin(tt*2.3)
            if A['yaw'] is not None: d.qpos[A['yaw']] = yy
            if A['pitch'] is not None: d.qpos[A['pitch']] = pp
            for g in A['geoms']:
                m.geom_rgba[g] = [col[0]/255, col[1]/255, col[2]/255, 1.0]
        mujoco.mj_forward(m, d)

        cp = CAMERAS.get(s.get('camera', spec.get('camera','front')), CAMERAS['front'])
        track = cp.get('track')
        target = who if track is True else (track if isinstance(track,str) else None)
        if target and target in actors:
            hp = d.xpos[actors[target]['body']].copy()
            lookat = hp + np.array([0.0, 0.0, cp['look']])
            dist = cp.get('dist', 1.5)
        else:
            lookat = np.array([0.0, 0.0, cp['look']]); dist = cp.get('dist', default_dist)
        az = cp['az'] + cp.get('orbit',0)*math.sin(tt*0.35)
        cam.lookat = lookat; cam.distance = dist; cam.elevation = cp['el']; cam.azimuth = az
        r.update_scene(d, camera=cam)
        img = Image.fromarray(r.render())

        # face tablet on the tracked speaker
        if target and target in actors:
            A = actors[target]
            hp = d.xpos[A['body']].copy()
            pr = project(hp+np.array([0.075,0.0,0.045]), lookat, az, cp['el'], dist, W, VIEW_H)
            if pr:
                px, py, z, f = pr
                sc = (f*0.11)/z/100.0
                mo = 0.35+0.35*abs(math.sin(tt*9.0)) if s.get('state')=='SPEAKING' else 0.12
                bl = 0.15 if math.sin(tt*3.1) > 0.96 else 1.0
                tablet(img, px, py, sc, cr if len(actors)>1 else cr, mo, bl)

        canvas = Image.new('RGB',(W,HH),(11,10,6)); canvas.paste(img,(0,HDR))
        dr = ImageDraw.Draw(canvas,'RGBA')
        dr.rectangle([0,0,W,HDR], fill=(212,175,55,255))
        dr.text((26,16), spec.get('title','æ:// MIXTURE OF ROBOTS'), font=F_BIG, fill=(11,10,6,255))
        dr.text((26,56), spec.get('tagline','MENLO CAD · NATIVE MUJOCO · LOCAL'), font=F_SM, fill=(58,48,16,255))
        dr.rectangle([0,HUD_Y,W,HH], fill=(14,13,8,255))
        dr.rectangle([0,HUD_Y,W,HUD_Y+4], fill=cr+(255,))
        y = HUD_Y+14
        if len(actors) > 1:
            x = 24
            for nm in names:
                A = actors[nm]; on = (nm == who)
                col = A['rgb'] if on else (78,72,52)
                lbl = A['label'] + (' ●' if on else '')
                tw = dr.textlength(lbl, font=F_XS)+14
                if x+tw > W-20: x = 24; y += 26
                dr.rectangle([x,y,x+tw,y+22], fill=col+(255,))
                dr.text((x+7,y+4), lbl, font=F_XS, fill=(11,10,6,255)); x += tw+6
            y += 30
        if s.get('kicker'):
            dr.text((26,y), s['kicker'], font=F_XS, fill=(201,179,106,255)); y += 21
        if s.get('banner'):
            dr.rectangle([22,y,W-22,y+48], fill=cr+(255,))
            dr.text((34,y+10), s['banner'], font=F_BIG, fill=(11,10,6,255)); y += 58
        for ln in s.get('lines',[])[:5]:
            dr.text((26,y), ln, font=F_SM, fill=(255,246,218,255)); y += 22
        dr.text((26,HH-50), spec.get('footer','HUMAN://ROOT → wætz → æ POLICY → RECEIPT'),
                font=F_XS, fill=(228,214,166,255))
        dr.rectangle([26,HH-24,W-26,HH-17], fill=(212,175,55,70))
        dr.rectangle([26,HH-24,26+int((W-52)*tt/total),HH-17], fill=(255,233,168,255))
        canvas.save(fd/f'f{i:05d}.png')
        if i % 100 == 0: print(f"  {i}/{nf} t={tt:.2f} {who} {s.get('state')} cam={s.get('camera','front')}")

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
                        '-c:v','copy','-c:a','aac','-b:a','128k','-shortest',str(out_path)],
                       capture_output=True, timeout=900)
    else:
        silent.replace(out_path)
    meta = dict(total_s=round(total,3), frames=nf, fps=fps, cast=cast, actors=names,
                bytes=out_path.stat().st_size, source='menloresearch/asimov-1',
                renderer='mujoco-native',
                scenes=[{k:v for k,v in s.items() if not k.startswith('_')} |
                        {'t0':round(s['_t0'],3),'t1':round(s['_t1'],3),
                         'speaker':s['_who'],'spoken':bool(s.get('_wav'))} for s in scenes])
    (wd/'studio.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False), encoding='utf-8')
    print(f"\n{out_path}  {out_path.stat().st_size} bytes")
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--workdir'); ap.add_argument('--verify', action='store_true')
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding='utf-8'))
    out = Path(a.out)
    wd = Path(a.workdir) if a.workdir else out.parent/(out.stem+'-studio')
    render(spec, out, wd)
    if a.verify and VIDAEO.exists():
        p = subprocess.run([PY,str(VIDAEO),'verify',str(out)], capture_output=True,
                           text=True, encoding='utf-8', timeout=900)
        print(p.stdout[-900:])


if __name__ == '__main__':
    main()
