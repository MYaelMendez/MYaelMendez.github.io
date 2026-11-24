"""Asimov Studio v2.2 orchestrator: mocap-guided free-base walk video.

Runs physics trace -> visemes -> render -> ffmpeg -> QC -> receipt -> publish.
Prints one JSON line on stdout.
"""
import json, sys, subprocess, hashlib, wave, re, shutil
from pathlib import Path
import numpy as np
from ae_paths import ANIM, GALLERY_REPO, REPO_ROOT, SCRIPTS, PY, ensure_runtime

ensure_runtime()
TEXT = ('I am Asimov. This walk is simulated. Human root. '
        'Receipts on every action. Greater than underscore ae.')
OUT = ANIM / 'asimov-free-walk-916.mp4'
WAV = ANIM / 'free-walk.wav'
WAV9 = ANIM / 'free-walk-9s.wav'
RAW = 'https://raw.githubusercontent.com/MYaelMendez/MYaelMendez.github.io/gh-pages/asimov-free-walk-916.mp4'


def run(cmd, timeout=900):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout or 'command failed')[-1200:])
    return p.stdout


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ensure_audio():
    if not WAV.exists():
        run([PY, str(SCRIPTS / 'tiny_voca_voice.py'), '--text', TEXT,
             '--voice', 'M2', '--speed', '1.25', '--output', str(WAV)], timeout=300)
    with wave.open(str(WAV), 'rb') as w:
        sr, ch, _ = w.getframerate(), w.getnchannels(), w.getsampwidth()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float) / 32767.0
    if ch == 2:
        a = a.reshape(-1, 2).mean(axis=1)
    b = np.zeros(sr * 9)
    b[:min(len(a), len(b))] = a[:min(len(a), len(b))]
    with wave.open(str(WAV9), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(b, -1, 1) * 32767).astype('<i2').tobytes())


def qc_video(path):
    from PIL import Image
    probe = json.loads(run(['ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_type,width,height,codec_name,r_frame_rate,nb_frames',
        '-show_entries', 'format=duration,size', '-of', 'json', str(path)]))
    v = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    au = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
    ok_video = (v['width'] == 720 and v['height'] == 1280 and v['codec_name'] == 'h264'
                and int(v.get('nb_frames', 0)) == 216
                and abs(float(probe['format']['duration']) - 9.0) < 0.05)
    ok_audio = au is not None and au['codec_name'] == 'aac'
    vp = subprocess.run(['ffmpeg', '-i', str(path), '-vn', '-af', 'volumedetect', '-f', 'null', '-'],
                        capture_output=True, text=True)
    vol = vp.stdout + vp.stderr
    mean = float(re.search(r'mean_volume: ([-\d.]+) dB', vol).group(1))
    peak = float(re.search(r'max_volume: ([-\d.]+) dB', vol).group(1))
    ok_sound = mean > -25 and peak < -0.5
    frames = sorted((ANIM / 'free_walk_frames').glob('*.png'))
    bright = 0
    if frames:
        for f in (frames[0], frames[len(frames)//2]):
            a = np.asarray(Image.open(f).convert('RGB'))
            bright = max(bright, int((a.max(axis=2) > 140).sum()))
    ok_frame = bright > 15000
    return {'success': all([ok_video, ok_audio, ok_sound, ok_frame]),
            'video': ok_video, 'audio': ok_audio, 'sound': ok_sound, 'frame': ok_frame,
            'width': v['width'], 'height': v['height'], 'fps': v['r_frame_rate'],
            'frames': int(v.get('nb_frames', 0)), 'duration_s': float(probe['format']['duration']),
            'size_bytes': int(probe['format']['size']), 'mean_db': mean, 'peak_db': peak,
            'bright_pixels': bright}


def publish(path):
    dst = GALLERY_REPO / path.name
    dst.write_bytes(path.read_bytes())
    gen = GALLERY_REPO / 'generate_gallery.py'
    if not gen.exists():
        gen = SCRIPTS / 'generate_gallery.py'
    run([PY, str(gen)], timeout=120)
    for cmd in [['git', '-C', str(GALLERY_REPO), 'add', path.name, 'videos.html'],
                ['git', '-C', str(GALLERY_REPO), 'commit', '-m',
                 'Add Asimov free-base walk video (Studio v2.2)\n\nSigned: HUMAN://ROOT / >_æ:'],
                ['git', '-C', str(GALLERY_REPO), 'push', 'origin', 'gh-pages']]:
        try:
            run(cmd, timeout=300)
        except RuntimeError as e:
            if 'nothing to commit' in str(e):
                continue
            raise
    import urllib.request
    def code(url):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return r.status
        except Exception:
            return 0
    return {'raw_status': code(RAW),
            'api_status': code('https://api.github.com/repos/MYaelMendez/MYaelMendez.github.io/contents/' + path.name + '?ref=gh-pages')}


def main():
    args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    ensure_audio()
    trace = json.loads(run([PY, str(SCRIPTS / 'physics_free_trace.py')], timeout=600).splitlines()[-1])
    vis = json.loads(run([PY, str(SCRIPTS / 'visemes_free.py')], timeout=180).splitlines()[-1])
    vis_data = json.loads((ANIM / 'free_visemes.json').read_text())
    run([PY, str(SCRIPTS / 'render_free_walk.py')], timeout=900)
    run(['ffmpeg', '-y', '-framerate', '24', '-i', str(ANIM / 'free_walk_frames/%05d.png'),
         '-i', str(WAV9), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
         '-crf', '20', '-c:a', 'aac', '-b:a', '128k', '-t', '9', str(OUT)], timeout=900)
    q = qc_video(OUT)
    pub = publish(OUT) if args.get('publish', True) else {'skipped': True}
    sys.path.insert(0, str(REPO_ROOT))
    import importlib.util
    spec = importlib.util.spec_from_file_location('ae', str(REPO_ROOT / '__init__.py'))
    ae = importlib.util.module_from_spec(spec); spec.loader.exec_module(ae)
    r = ae._receipt('VIDEO://ASIMOV_FREE_WALK_916', {
        'authority': 'HUMAN://ROOT', 'output': str(OUT), 'sha256': sha(OUT),
        'bytes': OUT.stat().st_size, 'duration_s': 9.0, 'fps': 24,
        'resolution': '720x1280', 'codec': 'h264/aac',
        'physics': {'model': trace['model'], 'mjcf_sha256': trace['mjcf_sha256'],
                    'nq': trace['nq'], 'nu': trace['nu'], 'frames': trace['frames'],
                    'com_advance_x_m': trace['com_advance_x'],
                    'min_base_z': trace['min_base_z'], 'mocap_guided': trace['mocap_guided']},
        'visemes': {'source': vis['source'], 'sha256': vis_data['phoneme_sha256'],
                    'events': len(vis_data['events'])},
        'voice': 'tiny-voca M2', 'qc': q, 'publish': pub,
        'authorization': args.get('authorization', 'user')})
    shutil.rmtree(ANIM / 'free_walk_frames', ignore_errors=True)
    print(json.dumps({'success': q['success'], 'output': str(OUT), 'sha256': sha(OUT),
                      'physics': {'model': trace['model'], 'nq': trace['nq'], 'nu': trace['nu'],
                                  'frames': trace['frames'], 'com_advance_x_m': trace['com_advance_x']},
                      'qc': q, 'publish': pub, 'receipt': r['hash'],
                      'authority': 'HUMAN://ROOT'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
