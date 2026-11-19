"""proof_sheet — the whole film in front of human eyes in seconds.

The video is the HUMAN gate. The supervisor measures pixels; only the operator
can judge whether a face reads as expressive or a scene makes sense. So the
binding constraint is TIME-TO-HUMAN-EYES, not time-to-final-film.

A five-body 967-frame film takes ~35 minutes. This renders ONE representative
frame per scene into a single contact sheet — ~9 frames, under a minute — so
the operator can reject a face, a layout or a narrative before committing.

    python proof_sheet.py --spec spec.json --out sheet.png [--scene charging_bay]

Each cell is labelled with scene number, speaker, state, camera and the spoken
line, so the sheet reads as a storyboard rather than a gallery.
"""
import argparse, json, math, os, re, sys, warnings
from pathlib import Path
import numpy as np
warnings.filterwarnings('ignore')
sys.path.insert(0, str(Path(__file__).resolve().parent))

H = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
PL = Path(os.environ.get('HERMES_AE_HOME', H / 'plugins' / 'hermes-ae'))
PY = os.environ.get('HERMES_AE_PYTHON', sys.executable)

CW, CH = 720, 1280         # cell size — MUST match the film, or the board lies.
                           # At 360px cells a face renders 11px wide and every
                           # iris/pupil/catchlight collapses to a square: the
                           # operator would judge a face the film never shows.
HDR, VH = 92, 720
HUD = HDR + VH


def build_cast(order, sep, docks=True):
    import mujoco
    src = (PL / 'model/xml/asimov_1_25dof_actuated.xml').read_text(encoding='utf-8')
    src = re.sub(r'meshdir="[^"]*"', f'meshdir="{(PL/"model/meshes").as_posix()}"', src)
    vis = f'<visual><global offwidth="{CW}" offheight="{VH}"/><quality shadowsize="2048"/></visual>'
    src = re.sub(r'<visual>.*?</visual>', vis, src, count=1, flags=re.S) if '<visual>' in src \
        else src.replace('</mujoco>', vis + '</mujoco>')
    parent = mujoco.MjSpec.from_string(src)
    ys = {n: (i - (len(order)-1)/2) * sep for i, n in enumerate(order)}
    first = parent.worldbody.first_body()
    first.pos = [0, ys[order[0]], float(first.pos[2])]
    return parent, ys, src


def sheet(spec, out_path, cast_mod):
    import mujoco
    from PIL import Image, ImageDraw, ImageFont
    from robot_face2 import face as make_face

    CAST, ORDER = cast_mod.CAST, cast_mod.ORDER
    STATE_RGB = getattr(cast_mod, 'STATE_RGB', None) or {
        'IDLE': (150,150,155), 'LISTENING': (0,204,255), 'SPEAKING': (0,255,159),
        'THINKING': (133,233,252), 'AWAITING_APPROVAL': (212,175,55),
        'APPROVED': (0,255,159), 'REFUSED': (255,0,255), 'ERROR': (255,59,71)}

    sep = float(spec.get('separation', 0.46))
    parent, ys, src = build_cast(ORDER, sep)
    for n in ORDER[1:]:
        child = mujoco.MjSpec.from_string(src)
        parent.worldbody.add_frame(pos=[0, ys[n], 0]).attach_body(
            child.worldbody.first_body(), CAST[n]['pfx'], '')
    for n in ORDER:
        pad = parent.worldbody.add_body(name=f'dock_{n}', pos=[0, ys[n], 0.012])
        pad.add_geom(type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.20, 0.17, 0.012],
                     rgba=[0.10,0.10,0.12,1], contype=0, conaffinity=0)
        st = parent.worldbody.add_body(name=f'strip_{n}', pos=[0.19, ys[n], 0.026])
        st.add_geom(type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.008,0.15,0.004],
                    rgba=[c/255 for c in CAST[n]['rgb']]+[1], contype=0, conaffinity=0)
    m = parent.compile(); d = mujoco.MjData(m)
    d.ctrl[:] = np.clip(0.0, m.actuator_ctrlrange[:,0], m.actuator_ctrlrange[:,1])
    for _ in range(1200): mujoco.mj_step(m, d)
    mujoco.mj_forward(m, d)
    base_q = d.qpos.copy()

    def jadr(n):
        j = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_JOINT, n)
        return int(m.jnt_qposadr[j]) if j >= 0 else None
    A = {}
    for n in ORDER:
        p = CAST[n]['pfx']
        hb = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, p+'neck_pitch_link')
        A[n] = dict(body=hb, geoms=[g for g in range(m.ngeom) if m.geom_bodyid[g]==hb],
                    yaw=jadr(p+'neck_yaw_joint'), y=ys[n], **CAST[n])

    def font(sz, bold=False):
        p = f"C:/Windows/Fonts/{'consolab' if bold else 'consola'}.ttf"
        return ImageFont.truetype(p, sz) if Path(p).exists() else ImageFont.load_default()
    F_T, F_M, F_S, F_X = font(30,True), font(22,True), font(20), font(18)

    r = mujoco.Renderer(m, height=VH, width=CW)
    cam = mujoco.MjvCamera(); cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    scenes = spec['scenes']
    cols = min(3, len(scenes))
    rows = math.ceil(len(scenes)/cols)
    sheet_img = Image.new('RGB', (CW*cols, CH*rows), (11,10,6))

    for i, s in enumerate(scenes):
        who = s.get('speaker', ORDER[0])
        stt = s.get('state', 'SPEAKING')
        rgb = STATE_RGB.get(stt, (212,175,55))
        close = s.get('camera') == 'face'
        chg = {n: min(1.0, spec.get('charge_start', {}).get(n, 0.30) + 0.55*(i/max(1,len(scenes)-1)))
               for n in ORDER}
        d.qpos[:] = base_q
        for n, a in A.items():
            active = (n == who)
            col = rgb if active else tuple(int(v*0.6) for v in a['rgb'])
            toward = -0.26 if a['y'] > 0 else 0.26
            yy = 0.0 if (close and active) else (toward*1.4 if active else toward*0.5)
            if a['yaw'] is not None: d.qpos[a['yaw']] = yy
            for g in a['geoms']:
                m.geom_rgba[g] = [col[0]/255, col[1]/255, col[2]/255, 1.0]
        mujoco.mj_forward(m, d)
        if close:
            hp = d.xpos[A[who]['body']].copy()
            lookat = hp + np.array([0,0,0.03]); dist, az, el = 0.66, 180, -2
        else:
            lookat = np.array([0,0,0.66]); dist = float(spec.get('distance',4.7))*0.92
            az, el = 180, -3
        cam.lookat = lookat; cam.distance = dist; cam.azimuth = az; cam.elevation = el
        r.update_scene(d, camera=cam)
        view = Image.fromarray(r.render())

        # faces
        FOVY = 45.0
        def proj(pt):
            a_, e_ = math.radians(az), math.radians(el)
            dv = np.array([math.cos(e_)*math.cos(a_), math.cos(e_)*math.sin(a_), math.sin(e_)])
            eye = lookat + dist*dv
            fwd = lookat-eye; fwd /= np.linalg.norm(fwd)
            rt = np.cross(fwd, np.array([0.,0.,1.])); rt /= np.linalg.norm(rt)
            up = np.cross(rt, fwd); rel = np.asarray(pt)-eye
            z = float(np.dot(rel, fwd))
            if z <= 1e-6: return None
            f = (VH/2.0)/math.tan(math.radians(FOVY)/2.0)
            return (CW/2.0+f*float(np.dot(rel,rt))/z, VH/2.0-f*float(np.dot(rel,up))/z, z, f)
        for n, a in A.items():
            if close and n != who: continue
            pr = proj(d.xpos[a['body']].copy() + np.array([0.078,0,0.040]))
            if not pr: continue
            px, py, z, f = pr
            fw = (f*0.115)/z; fh = fw*0.66
            if fw < 10: continue
            active = (n == who)
            vis = 2 if (active and stt == 'SPEAKING') else 0
            fi = make_face((int(fw), int(fh)), rgb if active else a['rgb'],
                           viseme=vis, charge=chg[n],
                           state=stt if active else 'LISTENING',
                           glow=1.2 if active else 0.6)
            view.paste(fi, (int(px-fw/2), int(py-fh/2)), fi)

        cell = Image.new('RGB', (CW, CH), (11,10,6))
        cell.paste(view, (0, HDR))
        dr = ImageDraw.Draw(cell, 'RGBA')
        dr.rectangle([0,0,CW,HDR], fill=(212,175,55,255))
        dr.text((20,12), f"{i+1:02d}  {s.get('camera','wide').upper()}", font=F_T, fill=(11,10,6,255))
        dr.text((20,52), f"{CAST[who]['label']} · {stt}", font=F_S, fill=(58,48,16,255))
        dr.rectangle([0,HUD,CW,CH], fill=(14,13,8,255))
        dr.rectangle([0,HUD,CW,HUD+6], fill=rgb+(255,))
        y = HUD+20
        if s.get('kicker'):
            dr.text((20,y), s['kicker'][:46], font=F_X, fill=(201,179,106,255)); y += 30
        if s.get('banner'):
            dr.rectangle([16,y,CW-16,y+48], fill=rgb+(255,))
            dr.text((28,y+12), s['banner'][:30], font=F_M, fill=(11,10,6,255)); y += 60
        if s.get('prompt'):
            dr.text((20,y), '> '+s['prompt'][:46], font=F_X, fill=(255,233,168,255)); y += 30
        for ln in s.get('lines', [])[:3]:
            dr.text((20,y), ln[:48], font=F_X, fill=(255,246,218,255)); y += 28
        # the spoken line, wrapped — this is what the human is judging
        sp = s.get('speak', '')
        if sp:
            y += 8
            line = ''
            for w in sp.split():
                if dr.textlength(line+w, font=F_X) > CW-44:
                    dr.text((20,y), line, font=F_X, fill=(180,168,130,255)); y += 26; line = w+' '
                else: line += w+' '
                if y > CH-32: break
            if y <= CH-32: dr.text((20,y), line, font=F_X, fill=(180,168,130,255))
        sheet_img.paste(cell, ((i%cols)*CW, (i//cols)*CH))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet_img.save(out_path)
    print(f"  {out_path}  {out_path.stat().st_size} bytes  {sheet_img.size}  {len(scenes)} scenes")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--scene', default='charging_bay')
    a = ap.parse_args()
    import importlib.util as u
    p = Path(__file__).resolve().parent / f'{a.scene}.py'
    if not p.exists():
        print(f"renderer not found: {p}"); return
    s = u.spec_from_file_location('castmod', p)
    mod = u.module_from_spec(s)
    s.loader.exec_module(mod)
    spec = json.loads(Path(a.spec).read_text(encoding='utf-8'))
    sheet(spec, Path(a.out), mod)


if __name__ == '__main__':
    main()
