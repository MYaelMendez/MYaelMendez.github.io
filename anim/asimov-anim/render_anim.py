"""Render an animated standing Asimov from the official CAD + URDF joint tree.

Frame painter: samples STL vertices, applies URDF transforms with a gentle
walk/idle gait, maps Z-up to Y-up, projects to a fixed 9:16 orthographic
viewport, and writes PNG frames for ffmpeg assembly.
"""
import json, math, struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

MESH = Path('/opt/data/hermes-asimov/model/meshes')
URDF = json.load(open('/opt/data/asimov-simulator/urdf.json'))
OUT = Path('/opt/data/asimov-anim/frames')
W, H, FPS, SECS = 720, 1280, 24, 9
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

# --- URDF helpers -----------------------------------------------------------
def rot_euler(rpy):
    x, y, z = rpy
    Rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
    Ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    Rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

def axis_rot(axis, angle):
    a = np.asarray(axis, dtype=float)
    n = np.linalg.norm(a)
    if n < 1e-9:
        return np.eye(3)
    a = a / n
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) * math.cos(angle) + (1 - math.cos(angle)) * np.outer(a, a) + math.sin(angle) * K

def local_matrix(joint, angle):
    m = np.eye(4)
    m[:3, :3] = rot_euler(joint['rpy']) @ axis_rot(joint.get('axis', [0, 0, 1]), angle)
    m[:3, 3] = joint['xyz']
    return m

def transforms(angles):
    xf = {'pelvis_link': np.eye(4)}
    for _ in range(6):
        for j in URDF['joints']:
            p, c = j['parent'], j['child']
            if p in xf and c not in xf:
                xf[c] = xf[p] @ local_matrix(j, angles.get(j['name'], 0.0))
    return xf

# Z-up -> Y-up, then a fixed 3/4 yaw
RX = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0.]])
YAW = math.radians(22)
RY = np.array([[math.cos(YAW), 0, math.sin(YAW)], [0, 1, 0], [-math.sin(YAW), 0, math.cos(YAW)]])
VIEW = RY @ RX  # row-vector: p @ VIEW.T

def gait(t):
    phase = t * 2 * math.pi / 2.2
    amp = min(1.0, t / 1.5, (SECS - t) / 1.5)
    a = {}
    a['left_hip_pitch_joint'] = 0.26 * math.sin(phase) * amp
    a['left_knee_joint'] = 0.32 * max(0.0, -math.sin(phase - 0.5)) * amp
    a['left_ankle_pitch_joint'] = 0.10 * math.sin(phase - 1.0) * amp
    a['right_hip_pitch_joint'] = -0.26 * math.sin(phase) * amp
    a['right_knee_joint'] = 0.32 * max(0.0, math.sin(phase - 0.5)) * amp
    a['right_ankle_pitch_joint'] = -0.10 * math.sin(phase - 1.0) * amp
    a['waist_yaw_joint'] = 0.06 * math.sin(phase * 0.5) * amp
    a['left_shoulder_pitch_joint'] = -0.18 * math.sin(phase) * amp
    a['right_shoulder_pitch_joint'] = 0.18 * math.sin(phase) * amp
    a['left_elbow_joint'] = 0.12 * amp
    a['right_elbow_joint'] = 0.12 * amp
    a['neck_yaw_joint'] = 0.10 * math.sin(t * 0.7)
    a['neck_pitch_joint'] = 0.04 * math.sin(t * 0.9)
    return a

# --- load and sample STL vertices ------------------------------------------
def stl_vertices(path):
    raw = path.read_bytes()
    n = struct.unpack('<I', raw[80:84])[0]
    if 84 + 50 * n != len(raw):
        return np.empty((0, 3))
    tri = np.frombuffer(raw, dtype=np.uint8, offset=84, count=50 * n).reshape(n, 50)
    v = np.frombuffer(tri[:, 12:48].tobytes(), dtype='<f4').reshape(n, 3, 3)
    return v[:, 1:, :].reshape(-1, 3).astype(np.float64)

samples = {}
for name, info in URDF['links'].items():
    v = stl_vertices(MESH / info['mesh'])
    if len(v):
        step = max(1, len(v) // 1800)
        samples[name] = v[::step]
print('sampled links:', len(samples), 'points:', sum(len(v) for v in samples.values()))

def world_points(t):
    xf = transforms(gait(t))
    chunks = []
    for name, v in samples.items():
        vh = np.c_[v, np.ones(len(v))]
        w = (vh @ xf[name].T)[:, :3]
        chunks.append(w @ VIEW.T)
    return np.vstack(chunks)

# fixed projection from the t=0 standing pose
base = world_points(0.0)
xmin, xmax = base[:, 0].min(), base[:, 0].max()
ymin, ymax = base[:, 1].min(), base[:, 1].max()
zmin, zmax = base[:, 2].min(), base[:, 2].max()
scale = min((W - 70) / max(xmax - xmin, 1e-6), (H - 110) / max(ymax - ymin, 1e-6))
cx = (xmin + xmax) / 2
cy = (ymin + ymax) / 2
floor_y = H / 2 - (ymin - cy) * scale
print('projection scale:', round(scale, 1), 'floor_y:', round(floor_y, 1))

font_big = ImageFont.truetype(FONT, 22)
font_small = ImageFont.truetype(FONT, 14)

if OUT.exists():
    import shutil
    shutil.rmtree(OUT)
OUT.mkdir(parents=True, exist_ok=True)

for frame in range(FPS * SECS):
    t = frame / FPS
    pts = world_points(t)
    ix = np.clip(((pts[:, 0] - cx) * scale + W / 2).astype(int), 0, W - 1)
    iy = np.clip((H / 2 - (pts[:, 1] - cy) * scale).astype(int), 0, H - 1)
    depth = np.clip((pts[:, 2] - zmin) / max(zmax - zmin, 1e-6), 0, 1)
    buf = np.empty((H, W, 3), dtype=np.uint8)
    buf[:] = (3, 10, 7)
    order = np.argsort(depth)  # far first, near overwrites
    g = (115 + 140 * depth[order]).astype(np.uint8)
    b = (70 + 90 * depth[order]).astype(np.uint8)
    buf[iy[order], ix[order]] = np.stack([np.zeros_like(g), g, b], axis=1)
    # ground line
    fy = int(floor_y)
    if 0 <= fy < H:
        buf[fy, :] = (0, 70, 45)
    img = Image.fromarray(buf)
    dr = ImageDraw.Draw(img)
    dr.text((18, 16), '>_æ: ASIMOV-1 · URDF DRIVEN', font=font_big, fill=(0, 255, 159))
    dr.text((18, 46), 'official 25-DOF CAD · Z-up → Y-up', font=font_small, fill=(0, 190, 150))
    dr.text((18, H - 34), f'HUMAN://ROOT · t={t:04.1f}s', font=font_small, fill=(0, 220, 160))
    # progress bar
    pw = int((W - 36) * min(1.0, t / SECS))
    dr.rectangle((18, H - 14, W - 18, H - 10), outline=(0, 80, 55))
    if pw > 0:
        dr.rectangle((18, H - 14, 18 + pw, H - 10), fill=(0, 255, 159))
    img.save(OUT / f'{frame:05d}.png')
    if frame % 48 == 0:
        print('frame', frame, '/', FPS * SECS)
print('frames written:', len(list(OUT.glob('*.png'))))
