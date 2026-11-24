"""Sovereign projection harness — deterministic rebuild and verification.

First principles:
  1. HUMAN://ROOT is the only authority.
  2. A projection is a composition of existing harnesses, never a new plugin.
  3. Live capture is pinned as hashed inputs; production replay is deterministic.
  4. Every build and publish writes a receipt to the one ledger.
  5. QC fails closed; aesthetics stay with the human.

Usage: sovereign_projection.py '{"action":"verify"}' or
       sovereign_projection.py '{"action":"render","publish":false}'
"""
import hashlib, importlib.util, json, os, re, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = Path(__file__).resolve().parent
REPO_ROOT = next((p for p in [HERE, *HERE.parents] if (p / '__init__.py').exists() and (p / 'harnesses.json').exists()), None)
if REPO_ROOT is None:
    raise SystemExit('cannot locate hermes-ae repo root')
assert REPO_ROOT is not None
PKG = REPO_ROOT / 'packages' / 'sovereign-projection' / '1.0.0'
ASSETS = PKG / 'assets'
OUT = Path(os.environ.get('SOVEREIGN_PROJECTION_OUT', REPO_ROOT / 'out' / 'sovereign-projection'))
FRAMES = OUT / 'frames'
W, H, FPS, SECS = 720, 1280, 24, 12
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
GOLD, ICE, CYAN, GREEN, MAGENTA, WHITE, MUTED = (212,175,55),(133,233,252),(0,204,255),(0,255,159),(255,0,255),(235,240,245),(136,146,176)
VOID = (5,5,5)
f_h = ImageFont.truetype(FONT, 34)
f_s = ImageFont.truetype(FONT, 17)
f_m = ImageFont.truetype(FONT, 20)
f_t = ImageFont.truetype(FONT, 13)


def run(cmd, timeout=900):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout)[-1200:])
    return p.stdout


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ae_mod():
    spec = importlib.util.spec_from_file_location('ae', REPO_ROOT / '__init__.py')
    if spec is None or spec.loader is None:
        raise SystemExit('cannot load ae plugin')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def receipt(action, detail):
    return ae_mod()._receipt(action, dict(detail, authority='HUMAN://ROOT'))


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_type,width,height,codec_name,r_frame_rate,nb_frames',
        '-show_entries', 'format=duration,size', '-of', 'json', str(path)]))


def verify():
    html = ASSETS / 'sovereignty-resources.html'
    if not html.exists():
        return {'success': False, 'error': 'source HTML missing'}
    text = html.read_text()
    principles = {
        'authority': 'HUMAN://ROOT' in text,
        'no_script_tags': '<script' not in text.lower(),
        'no_runtime_fetch': 'fetch(' not in text.lower(),
        'theme_vars': '--foreground' in text and '--accent' in text,
        'face_links': all(x in text for x in ('asimov-face-video.mp4', 'asimov-face-video-sm.gif', 'sovereign-resources-demo-916.mp4')),
    }
    media = {}
    for name in ('asimov-face-video.mp4','asimov-face-video-sm.gif','asimov-face-9x16.gif','sovereign-resources-demo-916.mp4','sovereign-resources-demo-480.gif'):
        p = ASSETS / name
        media[name] = {'exists': p.exists(), 'bytes': p.stat().st_size if p.exists() else 0, 'sha256': sha(p) if p.exists() else None}
    screenshots = {}
    for name in ('top','mid','deep'):
        p = ASSETS / f'sovereign-demo-{name}.png'
        im = Image.open(p).convert('RGB')
        screenshots[name] = {'width': im.width, 'height': im.height, 'sha256': sha(p)}
    demo = probe(ASSETS / 'sovereign-resources-demo-916.mp4')
    v = next(s for s in demo['streams'] if s['codec_type'] == 'video')
    demo_ok = (v['width'] == 720 and v['height'] == 1280 and v['codec_name'] == 'h264'
               and int(v.get('nb_frames', 0)) == 288 and abs(float(demo['format']['duration']) - 12.0) < 0.05)
    chain = ae_mod()._verify_chain()
    ok = all(principles.values()) and all(m['exists'] and m['bytes'] > 0 for m in media.values()) and demo_ok and chain.get('success', False)
    return {'success': ok, 'principles': principles, 'media': media,
            'screenshots': screenshots, 'demo': demo_ok,
            'ledger': {'success': chain.get('success'), 'count': chain.get('count'), 'head': chain.get('head')}}


def glow(img, xy, text, font, color, blur=10):
    layer = Image.new('RGBA', (W,H), (0,0,0,0))
    ImageDraw.Draw(layer).text(xy, text, font=font, fill=color+(255,))
    return ImageChops.screen(img, layer.filter(ImageFilter.GaussianBlur(blur)).convert('RGB'))


def fit(im, maxw, maxh):
    r = min(maxw/im.width, maxh/im.height)
    return im.resize((int(im.width*r), int(im.height*r)), Image.Resampling.LANCZOS)


def card(img, d, im, y, label):
    im = fit(im, 660, 390)
    x = (W-im.width)//2
    d.rounded_rectangle((x-10,y-10,x+im.width+10,y+im.height+10), radius=8, fill=(10,10,16), outline=CYAN, width=2)
    img.paste(im,(x,y))
    d.text((x,y+im.height+16), label, font=f_m, fill=ICE)


def render(args):
    if FRAMES.exists(): shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)
    shots = [Image.open(ASSETS / f'sovereign-demo-{n}.png').convert('RGB') for n in ('top','mid','deep')]
    face_dir = OUT / 'face-frames'; face_dir.mkdir(parents=True, exist_ok=True)
    for i, t in enumerate((0.5,1.5,2.5), 1):
        run(['ffmpeg','-y','-ss',str(t),'-i',str(ASSETS/'asimov-face-video.mp4'),
             '-frames:v','1',str(face_dir/f'{i}.png')])
    faces = [Image.open(face_dir/f'{i}.png').convert('RGB') for i in (1,2,3)]
    for frame in range(FPS*SECS):
        t = frame/FPS
        img = Image.new('RGB',(W,H),VOID); d=ImageDraw.Draw(img)
        for y in range(0,H,3): d.line((0,y,W,y),fill=(9,9,12),width=1)
        d.text((28,24),'>_æ: SOVEREIGN RESOURCES',font=f_s,fill=GOLD)
        d.text((28,52),'PUBLISHED BUNDLE · HUMAN://ROOT',font=f_t,fill=MUTED)
        if t < 1.5:
            img = glow(img,(60,430),'SOVEREIGN',f_h,GOLD,18); d=ImageDraw.Draw(img)
            d.text((60,485),'RESOURCES',font=f_h,fill=ICE)
            d.text((60,560),'41 capabilities · 8 meshes · 1 principal',font=f_m,fill=WHITE)
            d.text((60,600),'gate · ledger · receipt · fleet',font=f_s,fill=MUTED)
        elif t < 4.2:
            card(img,d,shots[0],175,'DOMAINS · PORTFOLIO · GITHUB · R&D KERNEL')
            d.text((40,1130),'01 / digital sovereignty',font=f_s,fill=GOLD)
        elif t < 6.7:
            card(img,d,shots[1],175,'MESH MODULES · KERNEL INVARIANTS')
            d.text((40,1130),'02 / policy gives rights · kernel gives keys',font=f_s,fill=GOLD)
        elif t < 9.1:
            card(img,d,shots[2],175,'ÆSIMOV · FLEET C2 · GOLDEN RULE')
            d.text((40,1130),'03 / body · eyes · brain · face spec',font=f_s,fill=GOLD)
        elif t < 11.2:
            idx = min(2,int((t-9.1)/0.7)); face=fit(faces[idx],520,900)
            x=(W-face.width)//2; y=205
            d.rounded_rectangle((x-10,y-10,x+face.width+10,y+face.height+10),radius=8,fill=(10,10,16),outline=MAGENTA,width=2)
            img.paste(face,(x,y)); d=ImageDraw.Draw(img)
            d.text((40,1140),'04 / 8 face states · damped springs · readout',font=f_s,fill=GOLD)
        else:
            img = glow(img,(60,470),'>_æ:',f_h,GOLD,18); d=ImageDraw.Draw(img)
            d.text((60,545),'authority not transferable',font=f_m,fill=ICE)
            d.text((60,590),'raw.githubusercontent.com / MYaelMendez',font=f_t,fill=MUTED)
            d.text((60,620),'receipt · #osw #ioa',font=f_t,fill=GREEN)
        d.line((28,H-40,W-28,H-40),fill=(40,40,50),width=2)
        pw=int((W-56)*min(1,t/SECS))
        if pw: d.line((28,H-40,28+pw,H-40),fill=GOLD,width=3)
        img.save(FRAMES/f'{frame:05d}.png')
    mp4 = OUT/'sovereign-resources-demo-916.mp4'
    gif = OUT/'sovereign-resources-demo-480.gif'
    run(['ffmpeg','-y','-framerate',str(FPS),'-i',str(FRAMES/'%05d.png'),
         '-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)])
    run(['ffmpeg','-y','-i',str(mp4),'-vf',
         'fps=10,scale=480:853:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3',
         '-loop','0',str(gif)])
    q = verify()
    pub = {'skipped': True, 'reason': 'not_requested'}
    if args.get('publish') and q['success']:
        gallery = Path(os.environ.get('HERMES_AE_GALLERY', ''))
        if gallery.exists():
            for src in (mp4,gif):
                shutil.copy(src,gallery/src.name)
            gen=gallery/'generate_gallery.py'
            if gen.exists(): run([sys.executable,str(gen)],timeout=180)
            for cmd in (['git','-C',str(gallery),'add',mp4.name,gif.name,'videos.html'],
                        ['git','-C',str(gallery),'commit','-m','Publish sovereign projection demo'],
                        ['git','-C',str(gallery),'push','origin','gh-pages']):
                try: run(cmd,timeout=300)
                except RuntimeError as e:
                    if 'nothing to commit' in str(e): continue
                    raise
            pub={'skipped':False,'gallery':str(gallery)}
    rec=receipt('PROJECTION://RENDER',{'mp4_sha256':sha(mp4),'gif_sha256':sha(gif),
        'duration_s':SECS,'resolution':'720x1280','fps':FPS,'qc':q['success'],'publish':pub})
    shutil.rmtree(FRAMES,ignore_errors=True)
    return {'success':q['success'],'mp4':str(mp4),'mp4_sha256':sha(mp4),
            'gif':str(gif),'gif_sha256':sha(gif),'publish':pub,'receipt':rec['hash']}


def main():
    args=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
    action=args.get('action','verify')
    out = verify() if action=='verify' else render(args)
    out = dict(out, authority='HUMAN://ROOT', action=action)
    if action=='verify':
        out['receipt'] = receipt('PROJECTION://VERIFY',{'success':out['success'],
            'ledger_head':out.get('ledger',{}).get('head')})['hash']
    print(json.dumps(out,ensure_ascii=False))


if __name__=='__main__': main()
