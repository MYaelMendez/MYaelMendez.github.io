"""Asimov = hermes-agent build identity clip.

12-second 9:16 proof: official Asimov-1 CAD walks on the mocap-guided MuJoCo
qpos trace while the hermes-agent (M2) voice explains the binding.
"""
import hashlib, json, math, re, shutil, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from ae_paths import ANIM, MESHES, REPO_ROOT, SCRIPTS, GALLERY_REPO, LEDGER, PY, BUNDLED_MODEL, ensure_runtime

ensure_runtime()
BASE = ANIM / 'asimov-agent'
FRAMES = BASE / 'frames'
OUT = ANIM / 'asimov-agent-build-916.mp4'
W, H, FPS, SECS = 720, 1280, 24, 12
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
GREEN, CYAN, MAGENTA, WHITE, BG = (0,255,159), (0,204,255), (255,0,255), (225,255,242), (3,9,12)
DIM = (24,70,58)
TEXT = ('I am hermes-agent, the build voice of OpenSourceWare. '
        'This body is Asimov-1, twenty five degrees of freedom. '
        'Human root stays. I ask, I execute, I return a receipt. '
        'Authority is never transferred. Execution is visible.')
TITLE = '>_æ: HERMES-AGENT // BUILD'
SUBTITLE = 'BODY: ASIMOV-1 · 25 DOF · OFFICIAL MENLO CAD'
ACTION = 'VIDEO://ASIMOV_HERMES_AGENT_BUILD'
STAGE_LINE = ''

f_title=ImageFont.truetype(FONT,28); f_sub=ImageFont.truetype(FONT,16)
f_voice=ImageFont.truetype(FONT,19); f_cap=ImageFont.truetype(FONT,24); f_tiny=ImageFont.truetype(FONT,11)


def run(cmd, timeout=900):
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
    if p.returncode!=0: raise RuntimeError((p.stderr or p.stdout)[-1000:])
    return p.stdout


def glow_text(img,xy,text,font,color,radius=12):
    layer=Image.new('RGBA',img.size,(0,0,0,0)); ImageDraw.Draw(layer).text(xy,text,font=font,fill=color+(255,))
    img.paste(ImageChops.screen(img,layer.filter(ImageFilter.GaussianBlur(radius)).convert('RGB')))
    ImageDraw.Draw(img).text(xy,text,font=font,fill=color)


def wav_info(path):
    with wave.open(str(path),'rb') as w:
        sr,ch=w.getframerate(),w.getnchannels(); a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32767.0
    if ch==2: a=a.reshape(-1,2).mean(axis=1)
    return sr,a


def wrap(text,font,maxw):
    tmp=ImageDraw.Draw(Image.new('RGB',(1,1))); lines=[]; cur=''
    for word in text.split():
        trial=(cur+' '+word).strip()
        if tmp.textbbox((0,0),trial,font=font)[2]<=maxw: cur=trial
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines


def build_audio():
    BASE.mkdir(parents=True,exist_ok=True)
    wav=BASE/'narration.wav'
    if not wav.exists():
        run([PY,str(SCRIPTS/'tiny_voca_voice.py'),'--text',TEXT,'--voice','hermes-agent',
             '--speed','1.3','--output',str(wav)])
    sr,a=wav_info(wav)
    out=np.zeros(sr*SECS); out[:min(len(a),len(out))]=a[:min(len(a),len(out))]
    wav9=BASE/'narration-9s.wav'
    with wave.open(str(wav9),'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
    # caption timeline from measured words, proportional to audio length
    speech=min(len(a)/sr,SECS-0.3)
    parts=[s for s in re.split(r'(?<=[.!?])\s+',TEXT) if s.strip()]
    weights=[len(s.split()) for s in parts]; tw=sum(weights)
    timeline=[]; t=0.0
    for s,wgt in zip(parts,weights):
        d=(wgt/tw)*speech; timeline.append({'start':round(t,3),'end':round(t+d,3),'text':s}); t+=d
    win=max(1,int(sr*0.04))
    env=np.sqrt(np.convolve(out**2,np.ones(win)/win,mode='same'))
    env=np.clip(env/max(float(np.percentile(env,95)),1e-6),0,1)
    return wav9,timeline,env,sr


def stl_points(path,limit=120):
    raw=path.read_bytes(); n=int(np.frombuffer(raw[80:84],dtype='<u4')[0])
    tri=np.frombuffer(raw,dtype=np.uint8,offset=84,count=50*n).reshape(n,50)
    v=np.frombuffer(tri[:,12:48].tobytes(),dtype='<f4').reshape(n,3,3)[:,1:,:].reshape(-1,3)
    return v[::max(1,len(v)//limit)].astype(float)


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
    w,x,y,z=q; n=math.sqrt(w*w+x*x+y*y+z*z) or 1.0; w,x,y,z=w/n,x/n,y/n,z/n
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])


def load_robot():
    urdf=json.loads((BUNDLED_MODEL/'urdf.json').read_text())
    trace_p=ANIM/'physics_free_trace.json'
    if not trace_p.exists() or not MESHES.exists(): return None
    trace=json.loads(trace_p.read_text())
    pts={}
    for name,info in urdf['links'].items():
        p=MESHES/info['mesh']
        if p.exists(): pts[name]=stl_points(p)
    if not pts: return None
    names,refs,qpos=trace['joint_names'],np.asarray(trace['joint_refs']),np.asarray(trace['qpos'])
    YAW=math.radians(78)
    RX=np.array([[1,0,0],[0,0,1],[0,-1,0.]])
    RY=np.array([[math.cos(YAW),0,math.sin(YAW)],[0,1,0],[-math.sin(YAW),0,math.cos(YAW)]])
    VIEW=RY@RX
    def frame_points(idx):
        b=qpos[idx,:7]; root=np.eye(4); root[:3,:3]=quat_mat(b[3:7]); root[:3,3]=b[:3]
        ang={n:float(qpos[idx,7+i]-refs[i]) for i,n in enumerate(names)}
        xf={'pelvis_link':np.eye(4)}
        for _ in range(6):
            for j in urdf['joints']:
                p,c=j['parent'],j['child']
                if p in xf and c not in xf:
                    m=np.eye(4); m[:3,:3]=rot_euler(j['rpy'])@axis_rot(j.get('axis',[0,0,1]),ang.get(j['name'],0)); m[:3,3]=j['xyz']
                    xf[c]=xf[p]@m
        out={}
        for name,v in pts.items():
            vh=np.c_[v,np.ones(len(v))]
            out[name]=((vh@(root@xf[name]).T)[:,:3])@VIEW.T
        return np.vstack(list(out.values())),b,np.asarray(trace['com'][idx])
    sample=np.vstack([frame_points(i)[0] for i in (0,108,215)])
    xmin,xmax=sample[:,0].min(),sample[:,0].max(); ymin,ymax=sample[:,1].min(),sample[:,1].max()
    zmin,zmax=sample[:,2].min(),sample[:,2].max(); cx,cy=(xmin+xmax)/2,(ymin+ymax)/2
    scale=min((W-100)/max(xmax-xmin,1e-6),470/max(ymax-ymin,1e-6))
    return frame_points,(cx,cy,scale,zmin,zmax),trace


def render(timeline,env,sr,robot):
    if FRAMES.exists(): shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True,exist_ok=True)
    fp,(cx,cy,scale,zmin,zmax),trace=robot
    for frame in range(FPS*SECS):
        t=frame/FPS
        img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img)
        for y in range(0,H,4): d.line((0,y,W,y),fill=(4,18,15),width=1)
        glow_text(img,(26,22),TITLE,f_title,CYAN,14)
        d.text((28,60),SUBTITLE,font=f_sub,fill=GREEN)
        if STAGE_LINE:
            d.rounded_rectangle((26,92,W-26,124),radius=8,fill=(5,20,16),outline=CYAN)
            d.text((40,100),STAGE_LINE,font=f_sub,fill=GREEN)
        # real CAD
        idx=min(len(trace['qpos'])-1,int((t/SECS)*(len(trace['qpos'])-1)))
        pts,base,com=fp(idx)
        px=np.clip(((pts[:,0]-cx)*scale+W/2).astype(int),0,W-1)
        py=np.clip((600-(pts[:,1]-cy)*scale).astype(int),160,1010)
        depth=np.clip((pts[:,2]-zmin)/max(zmax-zmin,1e-6),0,1)
        buf=np.array(img); order=np.argsort(depth)
        for i in order[::2]:
            if 0<=px[i]<W and 0<=py[i]<H:
                buf[py[i],px[i]]=(0,int(150+105*depth[i]),int(80+100*depth[i]))
        img=Image.fromarray(buf); d=ImageDraw.Draw(img)
        # viseme mouth
        e=float(env[min(len(env)-1,int(t*sr))])
        mx,my=360,int(315+8*math.sin(t*2))
        mw=int(14+58*e); mh=max(2,int(3+12*e))
        if e>0.03:
            for glow,col in [(10,(0,60,45)),(5,(0,150,110)),(0,(0,255,190))]:
                d.rounded_rectangle((mx-mw-glow,my-mh-glow,mx+mw+glow,my+mh+glow),radius=8,outline=col,width=2)
            d.text((mx+70,my-8),f'SPEAKING {int(e*100):3d}%',font=f_tiny,fill=CYAN)
        # telemetry
        d.rounded_rectangle((40,150,360,205),radius=10,fill=(5,20,16),outline=CYAN)
        d.text((56,160),f'VOICE  M2 / hermes-agent',font=f_voice,fill=CYAN)
        d.text((56,185),f'nu={trace["nu"]}  nq={trace["nq"]}  base X {base[0]:+.3f} m',font=f_tiny,fill=GREEN)
        d.text((40,230),f'COM X {com[0]:+.3f} m · receipts on every action',font=f_sub,fill=(120,230,190))
        # caption
        cur=next((s for s in timeline if s['start']<=t<s['end']),None)
        if cur:
            lines=wrap(cur['text'],f_cap,W-120); y=1060-(len(lines)-1)*18
            dr=d.textbbox((0,0),cur['text'],font=f_cap); tw=dr[2]-dr[0]
            d.rounded_rectangle(((W-tw)//2-20,y-12,(W+tw)//2+20,y+len(lines)*34+12),radius=10,fill=(3,18,13),outline=DIM)
            glow_text(img,((W-tw)//2,y),'\n'.join(lines),f_cap,WHITE,8)
        d.text((30,H-36),'HUMAN://ROOT · authority stays human · execution visible',font=f_sub,fill=GREEN)
        pw=int((W-60)*min(1.0,t/SECS)); d.rectangle((30,H-16,W-30,H-10),outline=DIM)
        if pw: d.rectangle((30,H-16,30+pw,H-10),fill=CYAN)
        img.save(FRAMES/f'{frame:05d}.png')


def qc(path):
    probe=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,codec_name,r_frame_rate,nb_frames','-show_entries','format=duration,size','-of','json',str(path)]))
    v=next(s for s in probe['streams'] if s['codec_type']=='video'); au=next((s for s in probe['streams'] if s['codec_type']=='audio'),None)
    p=subprocess.run(['ffmpeg','-i',str(path),'-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True)
    vol=p.stdout+p.stderr
    mean=float(re.search(r'mean_volume: ([-\d.]+) dB',vol).group(1)); peak=float(re.search(r'max_volume: ([-\d.]+) dB',vol).group(1))
    frames=sorted(FRAMES.glob('*.png')); a=np.asarray(Image.open(frames[len(frames)//2]).convert('RGB'))
    bright=int((a.max(axis=2)>140).sum())
    ok=(v['width']==720 and v['height']==1280 and v['codec_name']=='h264' and au and au['codec_name']=='aac'
        and int(v.get('nb_frames',0))==288 and abs(float(probe['format']['duration'])-12.0)<0.05 and mean>-25 and peak<-0.5 and bright>8000)
    return {'success':ok,'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'frames':int(v.get('nb_frames',0)),
            'duration_s':float(probe['format']['duration']),'size_bytes':int(probe['format']['size']),'mean_db':mean,'peak_db':peak,'bright_pixels':bright}


def publish(path):
    if not GALLERY_REPO.exists(): return {'skipped':True}
    dst=GALLERY_REPO/path.name; dst.write_bytes(path.read_bytes())
    gen=GALLERY_REPO/'generate_gallery.py'
    if gen.exists(): run([PY,str(gen)],timeout=180)
    for cmd in [['git','-C',str(GALLERY_REPO),'add',path.name,'videos.html'],
                ['git','-C',str(GALLERY_REPO),'commit','-m','Add Asimov hermes-agent build identity clip\n\nSigned: HUMAN://ROOT / >_æ:'],
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
    args=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
    wav,timeline,env,sr=build_audio()
    robot=load_robot()
    if not robot: raise SystemExit('robot runtime missing: meshes or trace unavailable')
    render(timeline,env,sr,robot)
    out=Path(args.get('output') or OUT)
    run(['ffmpeg','-y','-framerate',str(FPS),'-i',str(FRAMES/'%05d.png'),'-i',str(wav),
         '-af','volume=0.9','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',
         '-crf','20','-c:a','aac','-b:a','128k','-t',str(SECS),str(out)])
    q=qc(out)
    pub=publish(out) if (args.get('publish',True) and q['success']) else {'skipped':True}
    sys.path.insert(0,str(REPO_ROOT)); import importlib.util
    spec=importlib.util.spec_from_file_location('ae',REPO_ROOT/'__init__.py'); ae=importlib.util.module_from_spec(spec); spec.loader.exec_module(ae)
    rec=ae._receipt(ACTION,{'authority':'HUMAN://ROOT','output':str(out),
        'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'duration_s':SECS,'voice':'hermes-agent (M2)',
        'body':'asimov-1','qc':q,'publish':pub})
    shutil.rmtree(FRAMES,ignore_errors=True)
    print(json.dumps({'success':q['success'],'output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
                      'qc':q,'publish':pub,'receipt':rec['hash'],'authority':'HUMAN://ROOT'}))

if __name__=='__main__': main()
