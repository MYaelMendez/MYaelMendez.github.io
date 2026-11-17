"""Asimov renderer: policy-driven or mocap-guided free-base physics trace.

Consumes physics_free_trace.json (nq=32 including base) and visemes.json.
No prescribed zoom: forward motion is the simulated base translation solved by
MuJoCo weld constraints. Camera is fixed; the robot actually moves across it.
"""
from ae_paths import ANIM, MESHES, BUNDLED_MODEL, BUNDLED_XML, ensure_runtime
ensure_runtime()

import json, math, os, struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

MESH = MESHES
URDF = json.load(open(BUNDLED_MODEL / 'urdf.json'))
TRACE = json.load(open(os.environ.get('HERMES_AE_TRACE', ANIM / 'physics_free_trace.json')))
VISEMES = json.load(open(ANIM / 'free_visemes.json'))
OUT = Path(os.environ.get('HERMES_AE_FRAMES', ANIM / 'free_walk_frames'))
W, H, FPS = 720, 1280, 24
SECS = int(round(float(TRACE.get('duration_s', 9))))
YAW = math.radians(78)
FOLLOW = os.environ.get('HERMES_AE_CAMERA_FOLLOW', '') == '1'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

names = TRACE['joint_names']
refs = np.asarray(TRACE['joint_refs'], float)
qpos = np.asarray(TRACE['qpos'], float)
com = np.asarray(TRACE['com'], float)
base = np.asarray(TRACE['base'], float)

# --- math -------------------------------------------------------------------
def rot_euler(rpy):
    x,y,z=rpy
    Rx=np.array([[1,0,0],[0,math.cos(x),-math.sin(x)],[0,math.sin(x),math.cos(x)]])
    Ry=np.array([[math.cos(y),0,math.sin(y)],[0,1,0],[-math.sin(y),0,math.cos(y)]])
    Rz=np.array([[math.cos(z),-math.sin(z),0],[math.sin(z),math.cos(z),0],[0,0,1]])
    return Rz@Ry@Rx

def axis_rot(axis,ang):
    v=np.asarray(axis,float); n=np.linalg.norm(v)
    if n<1e-9: return np.eye(3)
    v=v/n; K=np.array([[0,-v[2],v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]])
    return np.eye(3)*math.cos(ang)+(1-math.cos(ang))*np.outer(v,v)+math.sin(ang)*K

def quat_mat(q):
    w,x,y,z=q
    n=math.sqrt(w*w+x*x+y*y+z*z) or 1.0; w,x,y,z=w/n,x/n,y/n,z/n
    return np.array([
      [1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
      [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
      [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])

def transforms(angles):
    xf={'pelvis_link':np.eye(4)}
    for _ in range(6):
        for j in URDF['joints']:
            p,c=j['parent'],j['child']
            if p in xf and c not in xf:
                ang=angles.get(j['name'],0.0)
                m=np.eye(4)
                m[:3,:3]=rot_euler(j['rpy'])@axis_rot(j.get('axis',[0,0,1]),ang)
                m[:3,3]=j['xyz']
                xf[c]=xf[p]@m
    return xf

RX=np.array([[1,0,0],[0,0,1],[0,-1,0.]])
RY=np.array([[math.cos(YAW),0,math.sin(YAW)],[0,1,0],[-math.sin(YAW),0,math.cos(YAW)]])
VIEW=RY@RX

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
print('sampled',len(samples),'links',sum(len(v) for v in samples.values()),'points')

def world_points(idx, viseme):
    b=qpos[idx,:7]
    root=np.eye(4); root[:3,:3]=quat_mat(b[3:7]); root[:3,3]=b[:3]
    ang={n:float(qpos[idx,7+i]-refs[i]) for i,n in enumerate(names)}
    xf=transforms(ang)
    out={}
    for name,v in samples.items():
        m=root@xf[name]
        vh=np.c_[v,np.ones(len(v))]
        w=(vh@m.T)[:,:3]@VIEW.T
        if name=='neck_pitch_link':
            hc=(w[:,1].min()+w[:,1].max())/2
            w[w[:,1]<hc,1]-=0.018*viseme['open']
        out[name]=w
    return np.vstack(list(out.values())), out['neck_pitch_link']

def viseme_at(t):
    for e in VISEMES['events']:
        if e['start']<=t<e['end']: return e
    return {'viseme':'rest','open':0.0,'width':0.15,'symbol':''}

def caption_at(t):
    for c in VISEMES['captions']:
        if c['start']<=t<c['end']: return c['text']
    return ''

# fixed projection from a few sampled frames
samples_idx=[0,54,108,162,215]
allp=[]
for i in samples_idx:
    p,_=world_points(i,{'open':0.0})
    if FOLLOW:
        p=p.copy(); p[:,0] -= base[min(i,len(base)-1),0]
    allp.append(p)
A=np.vstack(allp)
xmin,xmax=A[:,0].min(),A[:,0].max(); ymin,ymax=A[:,1].min(),A[:,1].max()
zmin,zmax=A[:,2].min(),A[:,2].max()
cx=(xmin+xmax)/2; cy=(ymin+ymax)/2
scale=min((W-70)/max(xmax-xmin,1e-6),(H-150)/max(ymax-ymin,1e-6))
floor=H/2-(ymin-cy)*scale
print('fixed scale',round(scale,1),'bounds x',round(xmin,3),round(xmax,3),'y',round(ymin,3),round(ymax,3))

font_big=ImageFont.truetype(FONT,21); font_small=ImageFont.truetype(FONT,13); font_tiny=ImageFont.truetype(FONT,11)
if OUT.exists():
    import shutil; shutil.rmtree(OUT)
OUT.mkdir(parents=True,exist_ok=True)

for frame in range(FPS*SECS):
    t=frame/FPS; v=viseme_at(t)
    pts,head=world_points(min(frame,len(qpos)-1),v)
    bx=base[min(frame,len(base)-1),0]
    proj=pts.copy(); proj_head=head.copy()
    if FOLLOW:
        proj[:,0]-=bx; proj_head[:,0]-=bx
    px=np.clip(((proj[:,0]-cx)*scale+W/2).astype(int),0,W-1)
    py=np.clip((H/2-(pts[:,1]-cy)*scale).astype(int),0,H-1)
    depth=np.clip((pts[:,2]-zmin)/max(zmax-zmin,1e-6),0,1)
    buf=np.empty((H,W,3),dtype=np.uint8); buf[:]=(3,10,7)
    order=np.argsort(depth)
    g=(115+140*depth[order]).astype(np.uint8); b=(70+90*depth[order]).astype(np.uint8)
    buf[py[order],px[order]]=np.stack([np.zeros_like(g),g,b],axis=1)
    fy=int(floor)
    if 0<=fy<H: buf[fy,:]=(0,80,50)
    img=Image.fromarray(buf); dr=ImageDraw.Draw(img)
    dr.text((16,14),'>_æ: ASIMOV-1 · POLICY-DRIVEN · ONNX',font=font_big,fill=(0,255,159))
    dr.text((16,42),'Menlo ONNX locomotion · 78 obs / 23 actions · MuJoCo 4.0.1',font=font_small,fill=(0,190,150))
    # viseme mouth
    hx=((proj_head[:,0]-cx)*scale+W/2); hy=(H/2-(proj_head[:,1]-cy)*scale)
    mx=int(np.clip(hx.mean(),0,W-1)); my=int(np.clip(np.percentile(hy,72),0,H-1))
    mw=int(8+62*v['width']*v['open']); mh=max(2,int(3+10*v['open']))
    if v['open']>0.03:
        for glow,col in [(12,(0,55,40)),(6,(0,140,95)),(0,(0,255,190))]:
            dr.rectangle((mx-mw-glow,my-mh-glow,mx+mw+glow,my+mh+glow),outline=col,width=2)
        dr.text((mx+70,my-8),f"SPEAKING {v['viseme'].upper()}",font=font_tiny,fill=(0,255,159))
    else: dr.line((mx-10,my,mx+10,my),fill=(0,120,85),width=2)
    cap=caption_at(t)
    if cap:
        dr.rectangle((40,H-92,W-40,H-50),fill=(3,16,11),outline=(0,110,75))
        dr.text((52,H-82),cap,font=font_small,fill=(0,255,175))
    # physics telemetry from simulated trajectory
    bx=base[min(frame,len(base)-1),0]; cm=com[min(frame,len(com)-1),0]
    if FOLLOW:
        ry=H-126
        dr.line((30,ry,W-30,ry),fill=(0,90,60),width=2)
        for k in range(-4,5):
            tx=int(W/2 + (k*0.5 - (bx%1.0))*200)
            if 30<tx<W-30:
                dr.line((tx,ry-8,tx,ry+8),fill=(0,200,140),width=2)
        dr.text((30,ry-26),f'TRAVEL {bx:+.3f} m · ONNX POLICY 50 Hz',font=font_tiny,fill=(0,255,180))
    aq=qpos[min(frame,len(qpos)-1),7:]-refs
    active=int(np.sum(np.abs(aq)>0.01))
    dr.text((W-200,18),f'nq={TRACE["nq"]} nu={TRACE["nu"]}',font=font_tiny,fill=(0,200,150))
    dr.text((W-200,32),f'BASE X {bx:+.3f} m',font=font_tiny,fill=(0,200,150))
    dr.text((W-200,46),f'COM X {cm:+.3f} m',font=font_tiny,fill=(0,200,150))
    dr.text((W-200,60),f'ACTIVE {active}/{len(refs)}',font=font_tiny,fill=(0,200,150))
    dr.text((16,H-34),f'HUMAN://ROOT · t={t:04.1f}s · policy-driven ONNX locomotion',font=font_small,fill=(0,220,160))
    pw=int((W-36)*min(1.0,t/SECS)); dr.rectangle((18,H-14,W-18,H-10),outline=(0,80,55))
    if pw: dr.rectangle((18,H-14,18+pw,H-10),fill=(0,255,159))
    img.save(OUT/f'{frame:05d}.png')
    if frame%48==0: print('frame',frame,'base',round(float(bx),3),'viseme',v['viseme'])
print('frames',len(list(OUT.glob('*.png'))))
