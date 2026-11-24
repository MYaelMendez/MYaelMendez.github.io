"""Generate a 9:16 two-voice open-course video from a lesson JSON.

F2 and M2 are tiny-voca voices. The lesson JSON supplies the title, id,
principle, and dialogue segments. Frames are deterministic PIL paintings;
ffmpeg assembles them with the generated narration. No cloud publish by default.
"""
import argparse, hashlib, json, math, shutil, subprocess, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from ae_paths import ANIM, REPO_ROOT, SCRIPTS, PY, ensure_runtime

ensure_runtime()
W, H, FPS = 720, 1280, 24
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
GREEN = (0, 255, 159)
CYAN = (0, 204, 255)
MAGENTA = (255, 0, 255)
WHITE = (225, 255, 242)
BG = (3, 9, 12)
DIM = (24, 70, 58)
GAP = 0.25
SPEED = 1.2

f_title = ImageFont.truetype(FONT, 28)
f_sub = ImageFont.truetype(FONT, 16)
f_voice = ImageFont.truetype(FONT, 18)
f_caption = ImageFont.truetype(FONT, 25)
f_dim = ImageFont.truetype(FONT, 16)
f_foot = ImageFont.truetype(FONT, 14)


def run(cmd, timeout=600):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout or 'command failed')[-1200:])
    return p.stdout


def wav_info(path):
    with wave.open(str(path), 'rb') as w:
        sr, ch = w.getframerate(), w.getnchannels()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64) / 32767.0
    if ch == 2:
        a = a.reshape(-1, 2).mean(axis=1)
    return sr, a


def glow_text(img, xy, text, font, color, radius=12):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(xy, text, font=font, fill=color + (255,))
    blur = layer.filter(ImageFilter.GaussianBlur(radius)).convert('RGB')
    img.paste(ImageChops.screen(img, blur))
    ImageDraw.Draw(img).text(xy, text, font=font, fill=color)


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


def build_audio(lesson, work):
    work.mkdir(parents=True, exist_ok=True)
    seg_files, timeline = [], []
    t = 0.0
    for i, seg in enumerate(lesson['segments'], 1):
        voice = seg['voice']
        if voice not in ('F2', 'M2'):
            raise SystemExit(f'segment {i}: voice must be F2 or M2')
        out = work / f'{i:02d}-{voice}.wav'
        run([PY, str(SCRIPTS / 'tiny_voca_voice.py'), '--text', seg['text'],
             '--voice', voice, '--speed', str(lesson.get('speed', SPEED)),
             '--output', str(out)])
        sr, a = wav_info(out)
        dur = len(a) / sr
        timeline.append({'start': round(t, 4), 'end': round(t + dur, 4),
                         'voice': voice, 'text': seg['text']})
        seg_files.append(a)
        seg_files.append(np.zeros(int(GAP * sr)))
        t += dur + GAP
    speech = np.concatenate(seg_files)
    secs = int(lesson.get('duration') or math.ceil(t + 0.8))
    sr = lesson.get('sample_rate', 24000)
    joined = np.zeros(sr * secs)
    joined[:min(len(speech), len(joined))] = speech[:min(len(speech), len(joined))]
    wav = work / 'narration.wav'
    with wave.open(str(wav), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(joined, -1, 1) * 32767).astype('<i2').tobytes())
    return wav, timeline, secs, sr


def envelope(wav, sr):
    _, a = wav_info(wav)
    win = max(1, int(sr * 0.04))
    e = np.sqrt(np.convolve(a ** 2, np.ones(win) / win, mode='same'))
    return np.clip(e / max(float(np.percentile(e, 95)), 1e-6), 0, 1)


def seg_at(timeline, t):
    for i, seg in enumerate(timeline):
        if seg['start'] <= t < seg['end']:
            return i, seg
    return None, None


def render_frames(lesson, timeline, env, sr, secs, out_dir):
    if out_dir.exists(): shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    title = str(lesson['title']).upper()
    lesson_id = str(lesson['id'])
    principle = lesson.get('principle', 'source visible · authority human · receipts public · self hosted')
    roles = lesson.get('roles', {'F2': 'NOUS GIRL', 'M2': 'HERMES-AGENT'})
    for frame in range(FPS * secs):
        t = frame / FPS
        idx, seg = seg_at(timeline, t)
        img = Image.new('RGB', (W, H), BG)
        d = ImageDraw.Draw(img)
        for y in range(0, H, 4):
            d.line((0, y, W, y), fill=(4, 18, 15), width=1)
        glow_text(img, (28, 26), f'>_æ: {title}', f_title, GREEN, 14)
        d.text((30, 66), f'OPEN COURSE · {lesson_id} · TWO VOICES', font=f_sub, fill=CYAN)
        vcolor = GREEN
        if seg:
            vcolor = MAGENTA if seg['voice'] == 'F2' else CYAN
            vlabel = f"{seg['voice']} // {roles[seg['voice']]}"
            d.rounded_rectangle((40, 118, 380, 160), radius=12, fill=(8, 22, 20), outline=vcolor, width=2)
            d.text((58, 130), vlabel, font=f_voice, fill=vcolor)
            d.text((W - 190, 132), f'VOICE {seg["voice"]}', font=f_sub, fill=vcolor)
        segments = timeline
        prev = segments[idx-1] if idx and idx > 0 else None
        nxt = segments[idx+1] if idx is not None and idx+1 < len(segments) else None
        if prev:
            d.text((70, 300), prev['text'], font=f_dim, fill=(45, 105, 88))
        if seg:
            lines = wrap(seg['text'], f_caption, W - 140)
            y = 470 - (len(lines) - 1) * 18
            glow_text(img, (70, y), '\n'.join(lines), f_caption, WHITE, 10)
            if int(t * 2) % 2 == 0:
                cw = d.textbbox((0, 0), lines[-1], font=f_caption)[2]
                yy = y + (len(lines)-1)*34
                d.line((70+cw+6, yy+4, 70+cw+6, yy+30), fill=vcolor, width=3)
        if nxt:
            d.text((70, 760), nxt['text'], font=f_dim, fill=(45, 105, 88))
        for j, ln in enumerate(wrap(principle, f_sub, W - 100)):
            d.text((70, 892 + j * 22), ln, font=f_sub, fill=GREEN)
        d.text((70, 946), 'not just open code — open authority, open operation, open proof',
               font=f_dim, fill=(110, 220, 180))
        e = float(env[min(len(env)-1, int(t*sr))])
        fy = 1060
        d.line((60, fy, W-60, fy), fill=DIM, width=2)
        for i in range(48):
            x = 70 + i * ((W-140)/48)
            a = e * (0.35 + 0.65 * abs(math.sin(i*0.7 + t*4)))
            h = int(6 + 46*a)
            col = MAGENTA if i < 24 else CYAN
            if seg and ((seg['voice']=='F2' and i>=24) or (seg['voice']=='M2' and i<24)):
                col = tuple(int(c*0.35) for c in col)
            d.line((x, fy-h, x, fy+h), fill=col, width=2)
        d.text((70, fy+62), f"F2 {roles['F2']}", font=f_dim, fill=MAGENTA)
        d.text((W-200, fy+62), f"M2 {roles['M2']}", font=f_dim, fill=CYAN)
        d.text((30, H-36), f'HUMAN://ROOT · t={t:04.1f}s · open course', font=f_foot, fill=GREEN)
        pw = int((W-60)*min(1.0, t/secs))
        d.rectangle((30, H-16, W-30, H-10), outline=DIM)
        if pw:
            d.rectangle((30, H-16, 30+pw, H-10), fill=GREEN)
        img.save(out_dir / f'{frame:05d}.png')
    return out_dir


def qc(video, frames_dir):
    from PIL import Image
    probe = json.loads(run(['ffprobe','-v','error','-show_entries',
        'stream=codec_type,width,height,codec_name,r_frame_rate,nb_frames',
        '-show_entries','format=duration,size','-of','json',str(video)]))
    v = next(s for s in probe['streams'] if s['codec_type']=='video')
    au = next((s for s in probe['streams'] if s['codec_type']=='audio'), None)
    vp = subprocess.run(['ffmpeg','-i',str(video),'-vn','-af','volumedetect','-f','null','-'],
                        capture_output=True,text=True)
    vol = vp.stdout+vp.stderr
    import re
    mean = float(re.search(r'mean_volume: ([-\d.]+) dB',vol).group(1))
    peak = float(re.search(r'max_volume: ([-\d.]+) dB',vol).group(1))
    sample = sorted(frames_dir.glob('*.png'))
    bright = 0
    if sample:
        f = sample[len(sample)//2]
        a = np.asarray(Image.open(f).convert('RGB'))
        bright = int((a.max(axis=2)>140).sum())
    ok = (v['width']==720 and v['height']==1280 and v['codec_name']=='h264'
          and au is not None and au['codec_name']=='aac' and mean>-25 and peak<-0.5 and bright>10000)
    return {'success':ok,'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],
            'frames':int(v.get('nb_frames',0)),'duration_s':float(probe['format']['duration']),
            'size_bytes':int(probe['format']['size']),'mean_db':mean,'peak_db':peak,
            'bright_pixels':bright}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lesson', required=True)
    ap.add_argument('--output')
    ap.add_argument('--no-cleanup', action='store_true')
    args = ap.parse_args()
    lesson = json.loads(Path(args.lesson).read_text())
    work = ANIM / 'courses' / lesson['id']
    wav, timeline, secs, sr = build_audio(lesson, work)
    env = envelope(wav, sr)
    frames = render_frames(lesson, timeline, env, sr, secs, work / 'frames')
    out = Path(args.output) if args.output else work / f"{lesson['id']}-916.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    run(['ffmpeg','-y','-framerate',str(FPS),'-i',str(frames/'%05d.png'),
         '-i',str(wav),'-af','volume=0.9','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',
         '-crf','20','-c:a','aac','-b:a','128k','-t',str(secs),str(out)], timeout=900)
    q = qc(out, frames)
    sys_path = str(REPO_ROOT)
    import sys
    sys.path.insert(0, sys_path)
    import importlib.util
    spec = importlib.util.spec_from_file_location('ae', REPO_ROOT / '__init__.py')
    ae = importlib.util.module_from_spec(spec); spec.loader.exec_module(ae)
    rec = ae._receipt(f"COURSE://{lesson['id'].upper()}", {
        'authority':'HUMAN://ROOT','lesson':lesson['id'],'title':lesson['title'],
        'output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
        'duration_s':secs,'voices':['F2','M2'],'qc':q})
    if not args.no_cleanup:
        shutil.rmtree(frames, ignore_errors=True)
    print(json.dumps({'success':q['success'],'lesson':lesson['id'],'output':str(out),
                      'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
                      'duration_s':secs,'qc':q,'receipt':rec['hash'],'authority':'HUMAN://ROOT'}))


if __name__ == '__main__':
    main()
