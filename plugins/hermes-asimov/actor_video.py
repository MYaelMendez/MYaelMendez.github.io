"""Hermes-Asimov spokesrobot video — official CAD render + tiny-voca voice."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np, sys, wave, os, shutil, argparse

sys.path.insert(0, '/opt/data')
import tiny_voca_voice as voice

W, H, FPS, SECS = 720, 1280, 24, 9
N = FPS * SECS
CAD = '/opt/data/attachments/asimov-fresh-green.png'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
f1 = ImageFont.truetype(FONT, 40)
f2 = ImageFont.truetype(MONO, 19)
f3 = ImageFont.truetype(MONO, 14)
GREEN, CYAN, MAG = (0,255,159), (0,204,255), (255,0,255)

ap = argparse.ArgumentParser()
ap.add_argument('--text', default='I am Hermes Asimov. Human root, receipts on every action.')
ap.add_argument('--output', default='/opt/data/attachments/hermes-asimov-spokesrobot.mp4')
a = ap.parse_args()

wav = '/tmp/hermes-asimov-line.wav'
voice.speak_text(a.text, wav, voice='M2', speed=1.05)
with wave.open(wav, 'rb') as f:
    aud = np.frombuffer(f.readframes(f.getnframes()), dtype='<i2').astype(np.float32)/32767
frame_audio = np.zeros(int(voice.SR*SECS), np.float32)
frame_audio[:min(len(aud), len(frame_audio))] = aud[:len(frame_audio)]
with wave.open(wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(voice.SR)
    w.writeframes((np.clip(frame_audio, -1, 1)*32767).astype('<i2').tobytes())

base = Image.open(CAD).convert('RGB') if os.path.exists(CAD) else Image.new('RGB',(1280,577),(7,9,10))
# Use the CAD viewport as a band; portrait canvas keeps it legible without distortion.
cad = base.resize((W, int(W*base.height/base.width)), Image.LANCZOS)

frames = '/opt/data/hermes_asimov_frames'
if os.path.exists(frames): shutil.rmtree(frames)
os.makedirs(frames, exist_ok=True)
rng = np.random.default_rng(20261116)
px, py = rng.uniform(0,W,180), rng.uniform(0,H,180)

def glow(img, xy, text, font, color):
    layer = Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
    d.text(xy, text, font=font, fill=(*color,255), anchor='mm')
    b=d.textbbox(xy,text,font=font,anchor='mm'); pad=30
    box=(max(0,b[0]-pad),max(0,b[1]-pad),min(W,b[2]+pad),min(H,b[3]+pad))
    sub=layer.crop(box); reg=img.crop(box).convert('RGBA')
    reg=ImageChops.screen(reg,sub.filter(ImageFilter.GaussianBlur(18)))
    reg=ImageChops.screen(reg,sub.filter(ImageFilter.GaussianBlur(6)))
    reg=Image.alpha_composite(reg,sub); img.paste(reg.convert('RGB'),(box[0],box[1]))

for n in range(N):
    t=n/FPS
    im=Image.new('RGB',(W,H),(7,9,10)); d=ImageDraw.Draw(im)
    for y in range(0,H,4): d.line([(0,y),(W,y)],fill=(9,12,16))
    y0=430
    im.paste(cad,(0,y0))
    d.rectangle([0,y0,W,y0+cad.height],outline=CYAN,width=2)
    d.text((W//2,90),'HERMES-ASIMOV',font=f1,fill=GREEN,anchor='mm')
    d.text((W//2,150),'official 25-DOF CAD · tiny-voca voice',font=f2,fill=(170,210,220),anchor='mm')
    for i in range(len(px)):
        xx=int((px[i]+t*12)%W); yy=int((py[i]+t*7)%H)
        c=[GREEN,CYAN,MAG][i%3]
        d.ellipse([xx-1,yy-1,xx+1,yy+1],fill=c)
    cy=y0+cad.height+55
    for i in range(26):
        xx=70+i*23; amp=int(6+40*abs(np.sin(t*8+i*0.5)))
        d.rounded_rectangle([xx,cy-amp,xx+8,cy+amp],radius=4,fill=GREEN)
    d.text((W//2,H-110),'HUMAN://ROOT · receipts on every action',font=f2,fill=GREEN,anchor='mm')
    d.text((W//2,H-72),'menlo-sdk speaker path · robot actor',font=f3,fill=(95,130,150),anchor='mm')
    im.save(f'{frames}/{n:05d}.png')

import subprocess
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{frames}/%05d.png',
                '-i',wav,'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',
                '-crf','20','-r',str(FPS),'-c:a','aac','-b:a','128k','-shortest','-t',str(SECS),a.output],check=True)
shutil.rmtree(frames,ignore_errors=True)
import hashlib
print(__import__('json').dumps({'success':True,'output':a.output,'duration_s':SECS,
                                'sha256':hashlib.sha256(open(a.output,'rb').read()).hexdigest()}))
