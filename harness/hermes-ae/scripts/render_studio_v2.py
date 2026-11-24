"""Asimov Studio v2.1 renderer.

Consumes a real MuJoCo qpos trace (25 actuated joints, base fixed) and a
phoneme-derived viseme/caption timeline. Renders a front-facing 9:16 clip
with prescribed forward approach, ground sweep, viseme mouth, captions,
and qpos telemetry. Deterministic STL point-cloud painter.
"""
from ae_paths import ANIM, MESHES, BUNDLED_URDF, BUNDLED_XML, ensure_runtime
ensure_runtime()

import json, math, struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

MESH = MESHES
URDF = json.load(open(BUNDLED_URDF / 'urdf.json'))
TRACE = json.load(open(ANIM / 'physics_trace.json'))
VISEMES = json.load(open(ANIM / 'visemes.json'))
OUT = ANIM / 'studio_v2_frames'
W, H, FPS, SECS = 720, 1280, 24, 9
YAW = math.radians(78)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

joint_names = TRACE['joint_names']
refs = TRACE['joint_refs']
qpos = np.asarray(TRACE['qpos'], dtype=float)
angle_by_frame = qpos - np.asarray(refs)  # absolute qpos -> URDF angle

# --- URDF helpers -----------------------------------------------------------
def rot_euler(rpy):
    x,y,z=rpy
    Rx=np.array([[1,0,0],[0,math.cos(x),-math.sin(x)],[0,math.sin(x),math.cos(x)]])
    Ry=np.array([[math.cos(y),0,math.sin(y)],[0,1,0],[-math.sin(y),0,math.cos(y)]])
    Rz=np.array([[math.cos(z),-math.sin(z),0],[math.sin(z),math.cos(z),0],[0,0,1]])
    return Rz@Ry@Rx

def axis_rot(axis, ang):
    v=np.asarray(axis,float); n=np.linalg.norm(v)
    if n<1e-9: return np.eye(3)
    v=v/n; K=np.array([[0,-v[2],v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]])
    return np.eye(3)*math.cos(ang)+(1-math.cos(ang))*np.outer(v,v)+math.sin(ang)*K

def local_matrix(j, ang):
    m=np.eye(4); m[:3,:3]=rot_euler(j['rpy'])@axis_rot(j.get('axis',[0,0,1]),ang); m[:3,3]=j['xyz']; return m

def transforms(angles):
    xf={'pelvis_link':np.eye(4)}
    for _ in range(6):
        for j in URDF['joints']:
            p,c=j['parent'],j['child']
            if p in xf and c not in xf:
                xf[c]=xf[p]@local_matrix(j, angles.get(j['name'],0.0))
    return xf

RX=np.array([[1,0,0],[0,0,1],[0,-1,0.]])
RY=np.array([[math.cos(YAW),0,math.sin(YAW)],[0,1,0],[-math.sin(YAW),0,math.cos(YAW)]])
VIEW=RY@RX

# --- STL sampling -----------------------------------------------------------
def stl_vertices(path):
    raw=path.read_bytes(); n=struct.unpack('<I',raw[80:84])[0]
    if 84+50*n!=len(raw): return np.empty((0,3))
    tri=np.frombuffer(raw,dtype=np.uint8,offset=84,count=50*n).reshape(n,50)
    v=np.frombuffer(tri[:,12:48].tobytes(),dtype='<f4').reshape(n,3,3)
    return v[:,1:,:].reshape(-1,3).astype(float)

samples={}
for name,info in URDF['links'].items():
    v=stl_vertices(MESH/info['mesh'])
    if len(v): samples[name]=v[::max(1,len(v)//1400)]
print('sampled links',len(samples),'points',sum(len(v) for v in samples.values()))

def frame_points(frame_idx, viseme):
    ang={n:float(angle_by_frame[frame_idx,i]) for i,n in enumerate(joint_names)}
    xf=transforms(ang)
    out={}
    for name,v in samples.items():
        vh=np.c_[v,np.ones(len(v))]
        w=(vh@xf[name].T)[:,:3]@VIEW.T
        if name=='neck_pitch_link':
            hc=(w[:,1].min()+w[:,1].max())/2
            low=w[:,1]<hc
            w[low,1]-=0.018*viseme['open']
        out[name]=w
    return np.vstack(list(out.values())), out['neck_pitch_link']

base,head0=frame_points(0, {'open':0.0})
xmin,xmax=base[:,0].min(),base[:,0].max(); ymin,ymax=base[:,1].min(),base[:,1].max()
zmin,zmax=base[:,2].min(),base[:,2].max()
cx=(xmin+xmax)/2; cy=(ymin+ymax)/2
ZOOM_MAX=1.18
scale=min((W-70)/(max(xmax-xmin,1e-6)*ZOOM_MAX),(H-150)/(max(ymax-ymin,1e-6)*ZOOM_MAX))
print('scale',round(scale,1))

def viseme_at(t):
    ev=VISEMES['events']
    for e in ev:
        if e['start']<=t<e['end']: return e
    return {'viseme':'rest','open':0.0,'width':0.15,'symbol':''}

def caption_at(t):
    for c in VISEMES['captions']:
        if c['start']<=t<c['end']: return c['text']
    return ''

font_big=ImageFont.truetype(FONT,21); font_small=ImageFont.truetype(FONT,13); font_tiny=ImageFont.truetype(FONT,11)

if OUT.exists():
    import shutil; shutil.rmtree(OUT)
OUT.mkdir(parents=True,exist_ok=True)

for frame in range(FPS*SECS):
    t=frame/FPS; v=viseme_at(t)
    pts,head=frame_points(min(frame,len(qpos)-1), v)
    progress=t/SECS; zoom=1+(ZOOM_MAX-1)*progress
    px=np.clip(((pts[:,0]-cx)*scale*zoom+W/2).astype(int),0,W-1)
    py=np.clip((H/2-(pts[:,1]-cy)*scale*zoom).astype(int),0,H-1)
    depth=np.clip((pts[:,2]-zmin)/max(zmax-zmin,1e-6),0,1)
    buf=np.empty((H,W,3),dtype=np.uint8); buf[:]=(3,10,7)
    order=np.argsort(depth)
    g=(115+140*depth[order]).astype(np.uint8); b=(70+90*depth[order]).astype(np.uint8)
    buf[py[order],px[order]]=np.stack([np.zeros_like(g),g,b],axis=1)
    floor=H/2-(ymin-cy)*scale*zoom
    for k in range(7):
        off=((k+progress*3.0)%7)/7.0; yy=int(floor+off*120)
        if 0<=yy<H:
            al=int(20+60*(1-off)); buf[yy,:]=(0,al,int(al*0.6))
    img=Image.fromarray(buf); dr=ImageDraw.Draw(img)
    dr.text((16,14),'>_æ: ASIMOV-1 · STUDIO v2.1 · PHYSICS/VISEME',font=font_big,fill=(0,255,159))
    dr.text((16,42),'MUJoCo qpos trace · dizione phonemes · tiny-voca M2',font=font_small,fill=(0,190,150))
    hx=((head[:,0]-cx)*scale*zoom+W/2); hy=(H/2-(head[:,1]-cy)*scale*zoom)
    mx=int(np.clip(hx.mean(),0,W-1)); my=int(np.clip(np.percentile(hy,72),0,H-1))
    mw=int(8+62*v['width']*v['open']); mh=max(2,int(3+10*v['open']))
    if v['open']>0.03:
        for glow,col in [(12,(0,55,40)),(6,(0,140,95)),(0,(0,255,190))]:
            dr.rectangle((mx-mw-glow,my-mh-glow,mx+mw+glow,my+mh+glow),outline=col,width=2)
        dr.text((mx+70,my-8),f"SPEAKING {v['viseme'].upper()}",font=font_tiny,fill=(0,255,159))
    else:
        dr.line((mx-10,my,mx+10,my),fill=(0,120,85),width=2)
    cap=caption_at(t)
    if cap:
        dr.rectangle((40,H-92,W-40,H-50),fill=(3,16,11),outline=(0,110,75))
        dr.text((52,H-82),cap,font=font_small,fill=(0,255,175))
    # telemetry
    aq=angle_by_frame[min(frame,len(qpos)-1)]
    active=int(np.sum(np.abs(aq)>0.01))
    dr.text((W-190,18),f'nu={TRACE["nu"]} q={len(aq)}',font=font_tiny,fill=(0,200,150))
    dr.text((W-190,32),f'ACTIVE {active}/25',font=font_tiny,fill=(0,200,150))
    dr.text((16,H-34),f'HUMAN://ROOT · t={t:04.1f}s · forward',font=font_small,fill=(0,220,160))
    pw=int((W-36)*min(1.0,t/SECS)); dr.rectangle((18,H-14,W-18,H-10),outline=(0,80,55))
    if pw: dr.rectangle((18,H-14,18+pw,H-10),fill=(0,255,159))
    img.save(OUT/f'{frame:05d}.png')
    if frame%48==0: print('frame',frame,'/',FPS*SECS,'viseme',v['viseme'],'cap',bool(cap))
print('frames',len(list(OUT.glob('*.png'))))
