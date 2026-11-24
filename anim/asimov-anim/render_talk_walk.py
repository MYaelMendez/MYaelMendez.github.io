"""Asimov: front-facing walking-forward talker, built from official CAD + URDF.

- Yaw 90° = true front view (verified against the STL geometry)
- Walk-forward conveyed by gait + progressive zoom + moving ground lines
- Mouth/jaw and status panel driven by the tiny-voca narration envelope
"""
import json, math, struct, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

MESH = Path('/opt/data/hermes-asimov/model/meshes')
URDF = json.load(open('/opt/data/asimov-simulator/urdf.json'))
AUDIO = Path('/opt/data/asimov-anim/talk-walk.wav')
AUDIO9 = Path('/opt/data/asimov-anim/talk-walk-9s.wav')
OUT = Path('/opt/data/asimov-anim/talk_walk_frames')
W, H, FPS, SECS = 720, 1280, 24, 9
YAW = math.radians(90)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

# --- audio envelope, padded to exact 9 s ------------------------------------
with wave.open(str(AUDIO), 'rb') as w:
    sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
    raw = w.readframes(w.getnframes())
a = np.frombuffer(raw, dtype='<i2').astype(np.float64) / 32767.0
if ch == 2:
    a = a.reshape(-1, 2).mean(axis=1)
target = sr * SECS
a9 = np.zeros(target, dtype=np.float64)
a9[:min(len(a), target)] = a[:min(len(a), target)]
with wave.open(str(AUDIO9), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(a9, -1, 1) * 32767).astype('<i2').tobytes())
win = max(1, int(sr * 0.05))
env = np.sqrt(np.convolve(a9 ** 2, np.ones(win) / win, mode='same'))
peak = np.percentile(env[env > 0.005], 95) if np.any(env > 0.005) else 1.0
env = np.clip(env / max(peak, 1e-6), 0, 1)
print('audio', sr, 'Hz', round(len(a9)/sr,3), 's; env peak', round(float(env.max()),3))

# --- URDF helpers -----------------------------------------------------------
def rot_euler(rpy):
    x, y, z = rpy
    Rx = np.array([[1,0,0],[0,math.cos(x),-math.sin(x)],[0,math.sin(x),math.cos(x)]])
    Ry = np.array([[math.cos(y),0,math.sin(y)],[0,1,0],[-math.sin(y),0,math.cos(y)]])
    Rz = np.array([[math.cos(z),-math.sin(z),0],[math.sin(z),math.cos(z),0],[0,0,1]])
    return Rz @ Ry @ Rx

def axis_rot(axis, ang):
    v = np.asarray(axis, float); n = np.linalg.norm(v)
    if n < 1e-9: return np.eye(3)
    v = v / n
    K = np.array([[0,-v[2],v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]])
    return np.eye(3)*math.cos(ang) + (1-math.cos(ang))*np.outer(v,v) + math.sin(ang)*K

def local_matrix(j, ang):
    m = np.eye(4)
    m[:3,:3] = rot_euler(j['rpy']) @ axis_rot(j.get('axis',[0,0,1]), ang)
    m[:3,3] = j['xyz']
    return m

def transforms(angles):
    xf = {'pelvis_link': np.eye(4)}
    for _ in range(6):
        for j in URDF['joints']:
            p, c = j['parent'], j['child']
            if p in xf and c not in xf:
                xf[c] = xf[p] @ local_matrix(j, angles.get(j['name'], 0.0))
    return xf

RX = np.array([[1,0,0],[0,0,1],[0,-1,0.]])
RY = np.array([[math.cos(YAW),0,math.sin(YAW)],[0,1,0],[-math.sin(YAW),0,math.cos(YAW)]])
VIEW = RY @ RX  # row-vector

def gait(t):
    phase = t * 2 * math.pi / 2.0
    ramp = min(1.0, t / 1.2, (SECS - t) / 1.2)
    a = {}
    a['left_hip_pitch_joint'] = 0.30 * math.sin(phase) * ramp
    a['left_knee_joint'] = 0.38 * max(0.0, -math.sin(phase - 0.4)) * ramp
    a['left_ankle_pitch_joint'] = 0.12 * math.sin(phase - 1.0) * ramp
    a['right_hip_pitch_joint'] = -0.30 * math.sin(phase) * ramp
    a['right_knee_joint'] = 0.38 * max(0.0, math.sin(phase - 0.4)) * ramp
    a['right_ankle_pitch_joint'] = -0.12 * math.sin(phase - 1.0) * ramp
    a['left_shoulder_pitch_joint'] = -0.24 * math.sin(phase) * ramp
    a['right_shoulder_pitch_joint'] = 0.24 * math.sin(phase) * ramp
    a['left_elbow_joint'] = 0.10 * ramp
    a['right_elbow_joint'] = 0.10 * ramp
    a['waist_yaw_joint'] = 0.05 * math.sin(phase * 0.5) * ramp
    # head bob / talking emphasis
    e = env[min(len(env)-1, int(t * sr))]
    a['neck_pitch_joint'] = -0.04 * e + 0.02 * math.sin(t * 3)
    a['neck_yaw_joint'] = 0.07 * math.sin(t * 0.8)
    return a

# --- load and sample STLs ---------------------------------------------------
def stl_vertices(path):
    raw = path.read_bytes()
    n = struct.unpack('<I', raw[80:84])[0]
    if 84 + 50*n != len(raw): return np.empty((0,3))
    tri = np.frombuffer(raw, dtype=np.uint8, offset=84, count=50*n).reshape(n,50)
    v = np.frombuffer(tri[:,12:48].tobytes(), dtype='<f4').reshape(n,3,3)
    return v[:,1:,:].reshape(-1,3).astype(float)

samples = {}
for name, info in URDF['links'].items():
    v = stl_vertices(MESH / info['mesh'])
    if len(v):
        samples[name] = v[::max(1, len(v)//1400)]
print('sampled links', len(samples), 'points', sum(len(v) for v in samples.values()))

def link_world(name, v, xf):
    vh = np.c_[v, np.ones(len(v))]
    w = (vh @ xf[name].T)[:, :3]
    return w @ VIEW.T

def frame_points(t):
    xf = transforms(gait(t))
    out = {}
    for name, v in samples.items():
        p = link_world(name, v, xf)
        # jaw drop on the head mesh when speaking
        if name == 'neck_pitch_link':
            e = env[min(len(env)-1, int(t*sr))]
            hc = (p[:,1].min()+p[:,1].max())/2
            lower = p[:,1] < hc
            p[lower, 1] -= 0.012 * e
        out[name] = p
    return np.vstack(list(out.values())), out['neck_pitch_link']

base, head0 = frame_points(0.0)
xmin, xmax = base[:,0].min(), base[:,0].max()
ymin, ymax = base[:,1].min(), base[:,1].max()
zmin, zmax = base[:,2].min(), base[:,2].max()
cx = (xmin+xmax)/2; cy = (ymin+ymax)/2
# leave headroom for the forward zoom
ZOOM_MAX = 1.18
scale = min((W-70)/(max(xmax-xmin,1e-6)*ZOOM_MAX),
            (H-150)/(max(ymax-ymin,1e-6)*ZOOM_MAX))
print('scale', round(scale,1))

font_big = ImageFont.truetype(FONT, 21)
font_small = ImageFont.truetype(FONT, 13)
font_tiny = ImageFont.truetype(FONT, 11)

if OUT.exists():
    import shutil; shutil.rmtree(OUT)
OUT.mkdir(parents=True, exist_ok=True)

for frame in range(FPS*SECS):
    t = frame/FPS
    pts, head = frame_points(t)
    progress = t/SECS
    zoom = 1 + (ZOOM_MAX-1)*progress
    px = np.clip(((pts[:,0]-cx)*scale*zoom + W/2).astype(int), 0, W-1)
    py = np.clip((H/2 - (pts[:,1]-cy)*scale*zoom).astype(int), 0, H-1)
    depth = np.clip((pts[:,2]-zmin)/max(zmax-zmin,1e-6), 0, 1)
    buf = np.empty((H,W,3), dtype=np.uint8); buf[:] = (3,10,7)
    order = np.argsort(depth)
    g = (115+140*depth[order]).astype(np.uint8)
    b = (70+90*depth[order]).astype(np.uint8)
    buf[py[order], px[order]] = np.stack([np.zeros_like(g), g, b], axis=1)

    # ground lines sweeping toward viewer as he advances
    floor = H/2 - (ymin-cy)*scale*zoom
    for k in range(7):
        off = ((k + progress*3.0) % 7) / 7.0
        yy = int(floor + off*120)
        if 0 <= yy < H:
            alpha = int(20 + 60*(1-off))
            buf[yy, :] = (0, alpha, int(alpha*0.6))

    img = Image.fromarray(buf)
    dr = ImageDraw.Draw(img)
    dr.text((16,14), '>_æ: ASIMOV-1 · FRONT / WALK / TALK', font=font_big, fill=(0,255,159))
    dr.text((16,42), 'tiny-voca M2 · official 25-DOF CAD · walking forward', font=font_small, fill=(0,190,150))

    # mouth driven by speech envelope
    e = float(env[min(len(env)-1, int(t*sr))])
    hx = ((head[:,0]-cx)*scale*zoom + W/2)
    hy = (H/2 - (head[:,1]-cy)*scale*zoom)
    mx = int(np.clip(hx.mean(), 0, W-1))
    my = int(np.clip(np.percentile(hy, 72), 0, H-1))
    mw = int(8 + 62*e)
    mh = max(2, int(3 + 9*e))
    if e > 0.03:
        for glow, col in [(12,(0,55,40)), (6,(0,140,95)), (0,(0,255,190))]:
            dr.rectangle((mx-mw-glow, my-mh-glow, mx+mw+glow, my+mh+glow), outline=col, width=2)
        dr.text((mx+70, my-8), 'SPEAKING', font=font_tiny, fill=(0,255,159))
    else:
        dr.line((mx-10,my,mx+10,my), fill=(0,120,85), width=2)

    # level meter
    lvl = int(120*e)
    dr.rectangle((W-150, 18, W-20, 30), outline=(0,90,60))
    if lvl: dr.rectangle((W-150, 18, W-150+lvl, 30), fill=(0,255,159))
    dr.text((W-150, 34), f'TTS {int(e*100):3d}%', font=font_tiny, fill=(0,200,150))

    dr.text((16, H-34), f'HUMAN://ROOT · t={t:04.1f}s · forward', font=font_small, fill=(0,220,160))
    pw = int((W-36)*min(1.0, t/SECS))
    dr.rectangle((18,H-14,W-18,H-10), outline=(0,80,55))
    if pw: dr.rectangle((18,H-14,18+pw,H-10), fill=(0,255,159))
    img.save(OUT/f'{frame:05d}.png')
    if frame % 48 == 0: print('frame',frame,'/',FPS*SECS,'env',round(e,2))
print('frames',len(list(OUT.glob('*.png'))))
