"""æ TV episode compiler — script + tinyVOICE + ffmpeg → receipted MP4.

Invoked by ae({op:"tv_episode", ...}) with one JSON argument.
Deterministic frame painter; WebGL is never used in the release path.
"""
from __future__ import annotations

import glob
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = os.environ.get('HERMES_AE_PYTHON', sys.executable)
HERMES_HOME = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
GALLERY = Path(os.environ.get('HERMES_AE_GALLERY', HERMES_HOME / 'ae' / 'gallery'))
SR = 24000
GAP_S = 0.18
VOICE_ALIASES = {
    'f2': 'F2', 'nous girl': 'F2', 'nous-girl': 'F2', 'nous_girl': 'F2',
    'm2': 'M2', 'hermes': 'M2', 'hermes-agent': 'M2', 'hermes agent': 'M2',
}
SIZES = {'916': (720, 1280), '9:16': (720, 1280), '1x1': (1080, 1080), '1:1': (1080, 1080)}


def _fail(message, **extra):
    out = {'success': False, 'error': message, 'authority': 'HUMAN://ROOT'}
    out.update(extra)
    print(json.dumps(out, ensure_ascii=False))
    return 1


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _font(size, bold=False):
    candidates = []
    if bold:
        candidates += glob.glob('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf')
    candidates += glob.glob('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
    candidates += glob.glob('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    try:
        from PIL import ImageFont
        for c in candidates:
            if Path(c).exists():
                return ImageFont.truetype(c, size)
        return ImageFont.load_default()
    except Exception:
        return None


def _canonical_voice(value):
    return VOICE_ALIASES.get(str(value or '').strip().lower())


def _load_lines(args):
    raw = args.get('lines')
    path = args.get('script')
    if path:
        p = Path(path).expanduser()
        if not p.exists():
            raise FileNotFoundError(f'script not found: {p}')
        text = p.read_text(encoding='utf-8')
        if p.suffix.lower() == '.json':
            data = json.loads(text)
            raw = data.get('lines', []) if isinstance(data, dict) else data
        else:
            raw = [x.strip() for x in text.splitlines() if x.strip() and not x.lstrip().startswith('#')]
    if not raw:
        text = args.get('text')
        if text:
            raw = [x.strip() for x in str(text).splitlines() if x.strip()]
    if not raw:
        raise ValueError('script, lines, or text is required')
    out = []
    default_voice = _canonical_voice(args.get('voice')) or 'M2'
    for item in raw:
        if isinstance(item, str):
            out.append({'text': item, 'voice': default_voice, 'language': 'en'})
            continue
        voice = _canonical_voice(item.get('voice')) or default_voice
        lang = str(item.get('language') or 'en')
        text = str(item.get('text') or '').strip()
        if not text:
            continue
        if voice not in ('F2', 'M2'):
            raise ValueError(
                f"voice {item.get('voice')!r} is not provisioned locally; "
                'SOVÆREIGN requires a provisioned VoxMel provider and VOICE://BIND')
        if lang.lower().startswith('zh'):
            raise ValueError('Chinese narration requires the provisioned VoxMel provider')
        out.append({'text': text, 'voice': voice, 'language': lang})
    if not out:
        raise ValueError('no narration lines')
    return out


def _concat_wavs(parts, output):
    params = None
    chunks = []
    gap = b'\x00\x00' * int(SR * GAP_S)
    for i, part in enumerate(parts):
        with wave.open(str(part), 'rb') as w:
            if params is None:
                params = w.getparams()
            if params.nchannels != 1 or params.sampwidth != 2 or params.framerate != SR:
                raise ValueError('all narration WAVs must be mono 16-bit 24 kHz')
            chunks.append(w.readframes(w.getnframes()))
            if i < len(parts) - 1:
                chunks.append(gap)
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b''.join(chunks))
    return sum(len(c) // 2 for c in chunks) / SR


def _wrap(text, font, draw, max_width):
    words = str(text).split()
    if not words:
        return []
    lines, cur = [], ''
    for word in words:
        trial = f'{cur} {word}'.strip()
        box = draw.textbbox((0, 0), trial, font=font)
        if box[2] - box[0] <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _render_frames(lines, spans, width, height, fps, channel, fmt, frames_dir, duration):
    from PIL import Image, ImageDraw
    total = max(2, int(math.ceil(duration * fps)))
    f_title = _font(max(22, width // 22), True)
    f_chan = _font(max(13, width // 46), True)
    f_body = _font(max(20, width // 34), False)
    f_small = _font(max(12, width // 58), False)
    bright = []
    story = {}
    samples = {int(total * p): p for p in (0.12, 0.5, 0.88)}
    for i in range(total):
        t = i / fps
        img = Image.new('RGB', (width, height), (4, 9, 6))
        d = ImageDraw.Draw(img)
        for y in range(0, height, 6):
            g = int(8 + 20 * y / height)
            d.rectangle((0, y, width, y + 2), fill=(4, min(g, 40), 10))
        pad = max(22, width // 28)
        d.text((pad, pad), 'æ TV', font=f_title, fill=(0, 255, 159))
        d.text((pad, pad + max(34, width // 18)), channel, font=f_chan, fill=(0, 204, 255))
        d.text((width - pad - d.textlength(fmt, font=f_chan), pad), fmt,
               font=f_chan, fill=(125, 156, 140))
        idx = next((k for k, s in enumerate(spans) if s['start'] <= t <= s['end']), len(spans) - 1)
        span = spans[idx]
        d.text((pad, int(height * 0.24)), f"CHANNEL://PLAY · {idx + 1:02d}/{len(spans):02d} · {span['voice']}",
               font=f_small, fill=(0, 255, 159))
        wrapped = _wrap(span['text'], f_body, d, width - pad * 2)
        y = int(height * 0.31)
        for line in wrapped[:8]:
            d.text((pad, y), line, font=f_body, fill=(214, 255, 233))
            y += max(30, width // 26)
        wave_y = int(height * 0.76)
        seed = int(hashlib.sha256(span['text'].encode()).hexdigest()[:8], 16)
        bars = 54
        for b in range(bars):
            h = 6 + ((seed >> (b % 24)) & 15) * 3 + int(10 * abs(math.sin(t * 3 + b * 0.4)))
            x = pad + b * (width - pad * 2) // bars
            d.rectangle((x, wave_y - h, x + max(3, width // 160), wave_y + h), fill=(0, 160, 110))
        prog = min(1.0, t / duration)
        d.rectangle((pad, height - pad - 44, width - pad, height - pad - 40), fill=(20, 60, 45))
        d.rectangle((pad, height - pad - 44, pad + int((width - pad * 2) * prog), height - pad - 40),
                    fill=(0, 255, 159))
        d.text((pad, height - pad - 30), 'HUMAN://ROOT → æ → ae → CHANNEL://PLAY → RECEIPT',
               font=f_small, fill=(0, 204, 255))
        p = frames_dir / f'{i:05d}.png'
        img.save(p)
        if i in samples:
            key = f'{samples[i]:.2f}'
            story[key] = p
            data = img.tobytes()[::48]  # every 16th RGB pixel
            bright.append(sum(1 for i in range(1, len(data), 3) if data[i] > 120))
    return total, bright, story


def _probe(path, width, height, expected_duration):
    p = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames',
        '-show_entries', 'format=duration,size', '-of', 'json', str(path)
    ], capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or 'ffprobe failed')[-500:])
    data = json.loads(p.stdout)
    streams = data.get('streams', [])
    video = next((s for s in streams if s.get('codec_type') == 'video'), {})
    audio = next((s for s in streams if s.get('codec_type') == 'audio'), {})
    duration = float(data.get('format', {}).get('duration') or 0)
    if video.get('codec_name') != 'h264':
        raise RuntimeError(f"expected h264 video, got {video.get('codec_name')!r}")
    if video.get('width') != width or video.get('height') != height:
        raise RuntimeError(f"wrong dimensions {video.get('width')}x{video.get('height')}")
    if audio.get('codec_name') != 'aac':
        raise RuntimeError(f"expected aac audio, got {audio.get('codec_name')!r}")
    if abs(duration - expected_duration) > 1.5:
        raise RuntimeError(f'duration {duration:.2f}s differs from expected {expected_duration:.2f}s')
    return {'duration_s': round(duration, 3), 'video_codec': video['codec_name'],
            'audio_codec': audio['codec_name'], 'width': width, 'height': height,
            'size': int(data.get('format', {}).get('size') or 0)}


def main():
    try:
        args = json.loads(sys.argv[1])
    except Exception as e:
        return _fail(f'bad JSON args: {e}')
    try:
        channel = str(args.get('channel') or 'æ://tiny-voice')
        fmt_key = str(args.get('format') or '916')
        if fmt_key not in SIZES:
            raise ValueError(f"format must be one of {sorted(SIZES)}")
        width, height = SIZES[fmt_key]
        fps = int(args.get('fps') or 24)
        speed = float(args.get('speed') or 1.15)
        lines = _load_lines(args)
        out = Path(args.get('out') or args.get('output') or
                   (HERMES_HOME / 'ae' / 'tv' / 'episode.mp4')).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        work = Path(tempfile.mkdtemp(prefix='ae-tv-', dir='/opt/data/cache/scratch'))
        frames = work / 'frames'
        frames.mkdir()
        wavs = []
        spans = []
        cursor = 0.0
        for i, line in enumerate(lines):
            wav = work / f'line-{i:03d}.wav'
            p = subprocess.run([
                PY, str(ROOT / 'scripts' / 'tiny_voca_voice.py'),
                '--text', line['text'], '--voice', line['voice'],
                '--output', str(wav), '--speed', str(speed)
            ], capture_output=True, text=True, timeout=300)
            if p.returncode != 0:
                raise RuntimeError((p.stderr or p.stdout or 'tts failed')[-800:])
            info = json.loads(p.stdout.strip().splitlines()[-1])
            if not info.get('success'):
                raise RuntimeError(str(info.get('error') or 'tts failed'))
            dur = float(info.get('duration_s') or 0)
            spans.append({'start': round(cursor, 3), 'end': round(cursor + dur, 3),
                          'text': line['text'], 'voice': line['voice'],
                          'language': line['language'], 'sha256': info.get('sha256'),
                          'receipt': info.get('receipt')})
            cursor += dur + GAP_S
            wavs.append(wav)
        narration = work / 'narration.wav'
        duration = _concat_wavs(wavs, narration) + 0.6
        total, bright, story = _render_frames(
            lines, spans, width, height, fps, channel, fmt_key.replace(':', ''), frames, duration)
        mp4 = work / 'episode.mp4'
        cmd = [
            'ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-start_number', '0',
            '-i', str(frames / '%05d.png'), '-i', str(narration), '-vf', 'format=yuv420p',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p',
            '-r', str(fps), '-c:a', 'aac', '-b:a', '128k', '-ar', '48000',
            '-af', 'loudnorm=I=-18:TP=-1.5:LRA=11', '-movflags', '+faststart', '-shortest', str(mp4)
        ]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
        if p.returncode != 0:
            raise RuntimeError((p.stderr or p.stdout or 'ffmpeg failed')[-1200:])
        qc = _probe(mp4, width, height, duration)
        if not bright or min(bright) < 1:
            raise RuntimeError('QC failed: sampled frames contain no bright pixels')
        shutil.copy2(mp4, out)
        for key, src in story.items():
            shutil.copy2(src, out.parent / f'{out.stem}-frame-{key.replace(".", "_")}.png')
        published = None
        if args.get('publish') and GALLERY.exists():
            published = GALLERY / out.name
            shutil.copy2(out, published)
        result = {
            'success': True, 'authority': 'HUMAN://ROOT', 'action': 'VIDEO://RENDER',
            'channel': channel, 'format': fmt_key, 'voice_engine': 'tiny-voca ONNX CPU',
            'output': str(out), 'sha256': _sha(out), 'bytes': out.stat().st_size,
            'duration_s': qc['duration_s'], 'frames': total, 'fps': fps,
            'lines': len(lines), 'voices': sorted({x['voice'] for x in lines}),
            'spans': spans, 'qc': qc, 'bright_pixels': bright,
            'storyboards': [str(out.parent / f'{out.stem}-frame-{k.replace(".", "_")}.png') for k in story],
            'published': str(published) if published else None,
            'receipt_actions': ['TTS://SPEAK', 'FFMPEG://RENDER', 'FFMPEG://PROBE', 'VIDEO://QC'],
        }
        shutil.rmtree(work, ignore_errors=True)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as e:
        return _fail(f'{type(e).__name__}: {e}')


if __name__ == '__main__':
    raise SystemExit(main())
