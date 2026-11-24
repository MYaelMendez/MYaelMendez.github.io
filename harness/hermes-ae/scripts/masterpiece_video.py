"""v3.0.0 masterpiece film: Mixture of Harnesses in five scenes.

Deterministic PIL frames + tiny-voca two-voice narration + ffmpeg assembly.
Optional publish copies the film into the Pages gallery repo and regenerates
videos.html. Prints one JSON line.
"""
import argparse, hashlib, json, math, shutil, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from ae_paths import ANIM, MESHES, REPO_ROOT, SCRIPTS, GALLERY_REPO, LEDGER, PY, BUNDLED_MODEL, ensure_runtime

ensure_runtime()
BASE = ANIM / 'masterpiece'
FRAMES = BASE / 'frames'
OUT = ANIM / 'moh-masterpiece-916.mp4'
W, H, FPS, SECS = 720, 1280, 24, 30
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
GREEN, CYAN, MAGENTA = (0, 255, 159), (0, 204, 255), (255, 0, 255)
WHITE, BG, DIM = (225, 255, 242), (3, 9, 12), (24, 70, 58)

f_title = ImageFont.truetype(FONT, 30)
f_sub = ImageFont.truetype(FONT, 16)
f_big = ImageFont.truetype(FONT, 25)
f_mid = ImageFont.truetype(FONT, 19)
f_small = ImageFont.truetype(FONT, 14)
f_tiny = ImageFont.truetype(FONT, 11)


def run(cmd, timeout=900):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout or 'command failed')[-1200:])
    return p.stdout


def glow_text(img, xy, text, font, color, radius=12):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(xy, text, font=font, fill=color + (255,))
    blur = layer.filter(ImageFilter.GaussianBlur(radius)).convert('RGB')
    img.paste(ImageChops.screen(img, blur))
    ImageDraw.Draw(img).text(xy, text, font=font, fill=color)


def glow_line(img, pts, color, width=2, glow=8):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).line(pts, fill=color + (170,), width=width + glow)
    blur = layer.filter(ImageFilter.GaussianBlur(max(1, glow // 2))).convert('RGB')
    img.paste(ImageChops.screen(img, blur))
    ImageDraw.Draw(img).line(pts, fill=color, width=width)


def wrap(text, font, maxw):
    tmp = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    lines, cur = [], ''
    for word in text.split():
        trial = (cur + ' ' + word).strip()
        if tmp.textbbox((0, 0), trial, font=font)[2] <= maxw:
            cur = trial
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines


def wav_info(path):
    with wave.open(str(path), 'rb') as w:
        sr, ch = w.getframerate(), w.getnchannels()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64) / 32767.0
    if ch == 2:
        a = a.reshape(-1, 2).mean(axis=1)
    return sr, a


# ---------- audio from course ----------
def build_audio(course):
    BASE.mkdir(parents=True, exist_ok=True)
    segs, timeline, t = [], [], 0.0
    gap = 0.12
    for i, seg in enumerate(course['segments'], 1):
        voice = seg['voice']
        out = BASE / f'{i:02d}-{voice}.wav'
        run([PY, str(SCRIPTS / 'tiny_voca_voice.py'), '--text', seg['text'],
             '--voice', voice, '--speed', str(course.get('speed', 1.25)), '--output', str(out)])
        sr, a = wav_info(out)
        dur = len(a) / sr
        timeline.append({'start': round(t, 4), 'end': round(t + dur, 4),
                         'voice': voice, 'text': seg['text']})
        segs += [a, np.zeros(int(sr * gap))]
        t += dur + gap
    joined = np.concatenate(segs)
    out = np.zeros(sr * SECS)
    out[:min(len(joined), len(out))] = joined[:min(len(joined), len(out))]
    wav = BASE / 'narration.wav'
    with wave.open(str(wav), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
    win = max(1, int(sr * 0.04))
    env = np.sqrt(np.convolve(out ** 2, np.ones(win) / win, mode='same'))
    env = np.clip(env / max(float(np.percentile(env, 95)), 1e-6), 0, 1)
    return wav, timeline, env, sr, t


# ---------- real Asimov point cloud ----------
def stl_points(path, limit=120):
    raw = path.read_bytes()
    n = int(np.frombuffer(raw[80:84], dtype='<u4')[0])
    tri = np.frombuffer(raw, dtype=np.uint8, offset=84, count=50 * n).reshape(n, 50)
    v = np.frombuffer(tri[:, 12:48].tobytes(), dtype='<f4').reshape(n, 3, 3)[:, 1:, :].reshape(-1, 3)
    return v[::max(1, len(v) // limit)].astype(float)


def rot_euler(rpy):
    x, y, z = rpy
    Rx = np.array([[1,0,0],[0,math.cos(x),-math.sin(x)],[0,math.sin(x),math.cos(x)]])
    Ry = np.array([[math.cos(y),0,math.sin(y)],[0,1,0],[-math.sin(y),0,math.cos(y)]])
    Rz = np.array([[math.cos(z),-math.sin(z),0],[math.sin(z),math.cos(z),0],[0,0,1]])
    return Rz @ Ry @ Rx


def axis_rot(axis, ang):
    v = np.asarray(axis, float); n = np.linalg.norm(v)
    if n < 1e-9: return np.eye(3)
    v = v / n; K = np.array([[0,-v[2],v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]])
    return np.eye(3)*math.cos(ang) + (1-math.cos(ang))*np.outer(v,v) + math.sin(ang)*K


def quat_mat(q):
    w, x, y, z = q
    n = math.sqrt(w*w + x*x + y*y + z*z) or 1.0; w,x,y,z = w/n,x/n,y/n,z/n
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])


def load_robot():
    urdf = json.loads((BUNDLED_MODEL/'urdf.json').read_text())
    trace_p = ANIM / 'physics_free_trace.json'
    if not trace_p.exists() or not MESHES.exists():
        return None
    trace = json.loads(trace_p.read_text())
    pts = {}
    for name, info in urdf['links'].items():
        p = MESHES / info['mesh']
        if p.exists(): pts[name] = stl_points(p)
    if not pts: return None
    names, refs, qpos = trace['joint_names'], np.asarray(trace['joint_refs']), np.asarray(trace['qpos'])
    YAW = math.radians(78)
    RX = np.array([[1,0,0],[0,0,1],[0,-1,0.]])
    RY = np.array([[math.cos(YAW),0,math.sin(YAW)],[0,1,0],[-math.sin(YAW),0,math.cos(YAW)]])
    VIEW = RY @ RX
    def frame_points(idx):
        b = qpos[idx,:7]
        root = np.eye(4); root[:3,:3] = quat_mat(b[3:7]); root[:3,3] = b[:3]
        ang = {n: float(qpos[idx,7+i] - refs[i]) for i, n in enumerate(names)}
        xf = {'pelvis_link': np.eye(4)}
        for _ in range(6):
            for j in urdf['joints']:
                p, c = j['parent'], j['child']
                if p in xf and c not in xf:
                    m = np.eye(4)
                    m[:3,:3] = rot_euler(j['rpy']) @ axis_rot(j.get('axis',[0,0,1]), ang.get(j['name'],0))
                    m[:3,3] = j['xyz']
                    xf[c] = xf[p] @ m
        out = {}
        for name, v in pts.items():
            vh = np.c_[v, np.ones(len(v))]
            out[name] = ((vh @ (root @ xf[name]).T)[:,:3]) @ VIEW.T
        return np.vstack(list(out.values())), b, np.asarray(trace['com'][idx])
    sample = np.vstack([frame_points(i)[0] for i in (0,108,215)])
    xmin, xmax = sample[:,0].min(), sample[:,0].max()
    ymin, ymax = sample[:,1].min(), sample[:,1].max()
    zmin, zmax = sample[:,2].min(), sample[:,2].max()
    cx, cy = (xmin+xmax)/2, (ymin+ymax)/2
    scale = min((W-100)/max(xmax-xmin,1e-6), (430)/max(ymax-ymin,1e-6))
    return frame_points, (cx, cy, scale, zmin, zmax), trace


# ---------- render ----------
def render(registry, course, timeline, env, sr, robot):
    if FRAMES.exists(): shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True, exist_ok=True)
    harnesses = registry['harnesses'] if isinstance(registry, dict) else registry
    principle = course.get('principle', 'mechanism + authority + receipt = opensourceware')
    for frame in range(FPS * SECS):
        t = frame / FPS
        img = Image.new('RGB', (W, H), BG)
        d = ImageDraw.Draw(img)
        for y in range(0, H, 4): d.line((0, y, W, y), fill=(4,18,15), width=1)
        glow_text(img, (26, 22), '>_æ: OPENSOURCEWARE', f_title, GREEN, 14)
        d.text((28, 60), 'MOH // MASTERPIECE · ONE TOOL · ONE LEDGER', font=f_sub, fill=CYAN)

        if t < 4:
            a = min(1.0, t / 1.2)
            glow_text(img, (60, 300), 'HUMAN://ROOT', f_big, tuple(int(c*a) for c in GREEN), 16)
            glow_line(img, [(360, 370), (360, 600)], GREEN, 2, 10)
            glow_text(img, (270, 630), 'æ', ImageFont.truetype(FONT, 64), tuple(int(c*a) for c in GREEN), 26)
            glow_line(img, [(360, 740), (360, 900)], CYAN, 2, 10)
            glow_text(img, (90, 930), 'RECEIPT', f_big, tuple(int(c*a) for c in CYAN), 16)
            d.text((60, 1030), 'authority flows down · receipts flow up', font=f_mid, fill=(120,230,190))
        elif t < 10:
            cx, cy = 360, 620
            rx, ry = 270, 330
            for i, h in enumerate(harnesses):
                ang = i * 2 * math.pi / len(harnesses) + t*0.15
                x = cx + rx*math.cos(ang); y = cy + ry*math.sin(ang)
                glow_line(img, [(cx,cy),(int(x),int(y))], MAGENTA if i%3==0 else CYAN, 1, 6)
                d.rounded_rectangle((x-62,y-16,x+62,y+16), radius=8, fill=(5,22,16), outline=CYAN if i%3 else MAGENTA)
                d.text((x-54,y-8), h['name'], font=f_tiny, fill=WHITE)
                p = (t*0.6 + i/len(harnesses)) % 1
                px, py = cx + (x-cx)*p, cy + (y-cy)*p
                d.ellipse((px-4,py-4,px+4,py+4), fill=GREEN)
            glow_text(img, (320, 590), 'ae', ImageFont.truetype(FONT, 54), GREEN, 24)
        elif t < 16 and robot:
            fp, (cx, cy, scale, zmin, zmax), trace = robot
            idx = min(len(trace['qpos'])-1, int((t-10)*24))
            pts, base, com = fp(idx)
            px = np.clip(((pts[:,0]-cx)*scale + W/2).astype(int), 0, W-1)
            py = np.clip((520 - (pts[:,1]-cy)*scale).astype(int), 180, 1000)
            depth = np.clip((pts[:,2]-zmin)/max(zmax-zmin,1e-6), 0, 1)
            buf = np.array(img)
            order = np.argsort(depth)
            for i in order[::2]:
                if 0 <= px[i] < W and 0 <= py[i] < H:
                    buf[py[i], px[i]] = (0, int(150+105*depth[i]), int(80+100*depth[i]))
            img = Image.fromarray(buf); d = ImageDraw.Draw(img)
            d.text((40, 180), f'ASIMOV-1 · nu={trace["nu"]} · nq={trace["nq"]}', font=f_mid, fill=GREEN)
            d.text((40, 210), f'BASE X {base[0]:+.3f} m · COM X {com[0]:+.3f} m', font=f_small, fill=CYAN)
        elif t < 22:
            cur = next((s for s in timeline if s['start'] <= t < s['end']), None)
            if cur:
                col = MAGENTA if cur['voice']=='F2' else CYAN
                name = 'nous girl' if cur['voice']=='F2' else 'hermes-agent'
                d.rounded_rectangle((50,300,430,346), radius=10, fill=(6,22,17), outline=col, width=2)
                d.text((70,312), f'{cur["voice"]} // {name}', font=f_mid, fill=col)
                lines = wrap(cur['text'], f_big, W-120)
                y = 480-(len(lines)-1)*18
                glow_text(img, (60,y), '\n'.join(lines), f_big, WHITE, 10)
            e = float(env[min(len(env)-1,int(t*sr))])
            for i in range(40):
                x=60+i*15; h=int(4+40*e*abs(math.sin(i*.6+t*3)))
                d.line((x,1000-h,x,1000+h), fill=MAGENTA if i<20 else CYAN, width=2)
            d.text((60,1020),'F2 NOUS GIRL',font=f_tiny,fill=MAGENTA)
            d.text((520,1020),'M2 HERMES-AGENT',font=f_tiny,fill=CYAN)
        elif t < 27:
            lines = [json.loads(x) for x in LEDGER.read_text().splitlines() if x.strip()] if LEDGER.exists() else []
            for i in range(7):
                y = 280+i*100
                h = min(len(lines), max(0, int((t-22)*3)-6+i))
                d.rounded_rectangle((110,y,610,y+62), radius=8, fill=(4,20,14), outline=GREEN if h else DIM, width=2)
                txt = f'{lines[-h]["action"]}  {lines[-h]["hash"][:12]}' if h else 'AWAITING RECEIPT'
                d.text((130,y+20), txt, font=f_small, fill=WHITE if h else (40,90,70))
        else:
            glow_text(img, (140,360), '>_æ:', ImageFont.truetype(FONT, 76), GREEN, 26)
            d.text((150,470), 'HUMAN://ROOT · authority not transferable', font=f_mid, fill=CYAN)
            d.text((150,510), 'github.com/MYaelMendez/hermes-ae', font=f_small, fill=(120,230,190))
            d.text((150,550), 'myaelmendez.github.io', font=f_small, fill=(120,230,190))

        # constant caption + principle strip + footer
        cur = next((s for s in timeline if s['start'] <= t < s['end']), None)
        if cur and not (16 <= t < 22):
            d.rounded_rectangle((40,1090,W-40,1138), radius=9, fill=(3,18,13), outline=DIM)
            d.text((56,1104), cur['text'][:86], font=f_small, fill=(190,255,225))
        d.text((40,1160), principle, font=f_small, fill=GREEN)
        d.text((40,1190), f'HUMAN://ROOT · t={t:04.1f}s · mixture of harnesses', font=f_tiny, fill=CYAN)
        pw = int((W-80)*min(1.0,t/SECS))
        d.rectangle((40,H-22,W-40,H-16), outline=DIM)
        if pw: d.rectangle((40,H-22,40+pw,H-16), fill=GREEN)
        img.save(FRAMES/f'{frame:05d}.png')


def qc(path):
    probe = json.loads(run(['ffprobe','-v','error','-show_entries',
        'stream=codec_type,width,height,codec_name,r_frame_rate,nb_frames',
        '-show_entries','format=duration,size','-of','json',str(path)]))
    v = next(s for s in probe['streams'] if s['codec_type']=='video')
    au = next((s for s in probe['streams'] if s['codec_type']=='audio'), None)
    p = subprocess.run(['ffmpeg','-i',str(path),'-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True)
    import re
    mean = float(re.search(r'mean_volume: ([-\d.]+) dB',p.stdout+p.stderr).group(1))
    peak = float(re.search(r'max_volume: ([-\d.]+) dB',p.stdout+p.stderr).group(1))
    f = sorted(FRAMES.glob('*.png'))[len(list(FRAMES.glob('*.png')))//2]
    a = np.asarray(Image.open(f).convert('RGB'))
    bright = int((a.max(axis=2)>140).sum())
    ok = (v['width']==720 and v['height']==1280 and v['codec_name']=='h264'
          and au and au['codec_name']=='aac' and int(v.get('nb_frames',0))==720
          and abs(float(probe['format']['duration'])-30.0)<0.05 and mean>-25 and peak<-0.5 and bright>8000)
    return {'success':ok,'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],
            'frames':int(v.get('nb_frames',0)),'duration_s':float(probe['format']['duration']),
            'size_bytes':int(probe['format']['size']),'mean_db':mean,'peak_db':peak,'bright_pixels':bright}


def publish(path):
    if not GALLERY_REPO.exists(): return {'skipped':True,'reason':'gallery repo missing'}
    dst = GALLERY_REPO/path.name; dst.write_bytes(path.read_bytes())
    gen = GALLERY_REPO/'generate_gallery.py'
    if gen.exists(): run([PY,str(gen)],timeout=180)
    for cmd in [['git','-C',str(GALLERY_REPO),'add',path.name,'videos.html','index.html'],
                ['git','-C',str(GALLERY_REPO),'commit','-m','Publish MoH masterpiece\n\nSigned: HUMAN://ROOT / >_æ:'],
                ['git','-C',str(GALLERY_REPO),'push','origin','gh-pages']]:
        try: run(cmd,timeout=300)
        except RuntimeError as e:
            if 'nothing to commit' in str(e): continue
            raise
    import urllib.request
    def code(u):
        try:
            with urllib.request.urlopen(u,timeout=30) as r: return r.status
        except Exception: return 0
    return {'raw_status':code('https://raw.githubusercontent.com/MYaelMendez/MYaelMendez.github.io/gh-pages/'+path.name),
            'api_status':code('https://api.github.com/repos/MYaelMendez/MYaelMendez.github.io/contents/'+path.name+'?ref=gh-pages')}


def main():
    args = json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
    registry = json.loads((REPO_ROOT/'harnesses.json').read_text())
    course = json.loads((REPO_ROOT/'courses'/'osw-103.json').read_text())
    wav, timeline, env, sr, speech_end = build_audio(course)
    robot = load_robot()
    render(registry, course, timeline, env, sr, robot)
    out = Path(args.get('output') or OUT)
    run(['ffmpeg','-y','-framerate',str(FPS),'-i',str(FRAMES/'%05d.png'),
         '-i',str(wav),'-af','volume=0.9','-c:v','libx264','-pix_fmt','yuv420p',
         '-movflags','+faststart','-crf','20','-c:a','aac','-b:a','128k','-t',str(SECS),str(out)])
    q = qc(out)
    pub = publish(out) if (args.get('publish', True) and q['success']) else {'skipped':True, 'reason':'qc_failed' if not q['success'] else 'not_requested'}
    sys.path.insert(0,str(REPO_ROOT))
    import importlib.util
    spec=importlib.util.spec_from_file_location('ae',REPO_ROOT/'__init__.py')
    ae=importlib.util.module_from_spec(spec); spec.loader.exec_module(ae)
    rec=ae._receipt('VIDEO://MOH_MASTERPIECE',{'authority':'HUMAN://ROOT','output':str(out),
        'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'duration_s':SECS,
        'resolution':'720x1280','voices':['nous-girl','hermes-agent'],'qc':q,'publish':pub,
        'harnesses':len(registry['harnesses']) if isinstance(registry,dict) else len(registry)})
    shutil.rmtree(FRAMES,ignore_errors=True)
    print(json.dumps({'success':q['success'],'output':str(out),
        'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'speech_end_s':round(speech_end,3),
        'qc':q,'publish':pub,'receipt':rec['hash'],'authority':'HUMAN://ROOT'}))


if __name__=='__main__':
    main()
