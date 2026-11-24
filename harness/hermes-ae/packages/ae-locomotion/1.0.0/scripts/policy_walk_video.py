"""Publish the policy-driven Asimov walk as a 12-second 9:16 clip.

Consumes physics_policy_trace.json from policy_locomotion.py, renders with the
parameterized Asimov renderer, adds tiny-voca M2 narration, QC gates, publishes
to the Pages gallery, and writes a HUMAN://ROOT receipt.
"""
import hashlib, importlib.util, json, os, re, shutil, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image
from ae_paths import ANIM, REPO_ROOT, SCRIPTS, GALLERY_REPO, PY, ensure_runtime

ensure_runtime()
TRACE = ANIM / 'physics_policy_trace.json'
FRAMES = ANIM / 'policy_walk_frames'
AUDIO = ANIM / 'policy-walk.wav'
OUT = ANIM / 'asimov-policy-walk-916.mp4'
TEXT = ('Policy-driven locomotion. This is Asimov one, running the Menlo '
        'locomotion ONNX policy inside MuJoCo. Seventy-eight observations in, '
        'twenty-three joint targets out. Human root. Receipts on every step.')


def run(cmd, env=None, timeout=900):
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=timeout)
    if p.returncode != 0: raise RuntimeError((p.stderr or p.stdout)[-1500:])
    return p.stdout


def wav_duration(path):
    with wave.open(str(path), 'rb') as w: return w.getnframes() / w.getframerate()


def build_audio():
    for speed in (1.4, 1.6, 1.8):
        run([PY, str(SCRIPTS / 'tiny_voca_voice.py'), '--text', TEXT, '--voice', 'hermes-agent',
             '--speed', str(speed), '--output', str(AUDIO)])
        if wav_duration(AUDIO) <= 11.7: return speed
    raise SystemExit('narration too long even at speed 1.8')


def qc(path):
    probe = json.loads(run(['ffprobe','-v','error','-show_entries',
        'stream=codec_type,width,height,codec_name,r_frame_rate,nb_frames',
        '-show_entries','format=duration,size','-of','json',str(path)]))
    v = next(s for s in probe['streams'] if s['codec_type']=='video')
    au = next((s for s in probe['streams'] if s['codec_type']=='audio'), None)
    p = subprocess.run(['ffmpeg','-i',str(path),'-vn','-af','volumedetect','-f','null','-'],
                       capture_output=True, text=True)
    vol = p.stdout + p.stderr
    mg = re.search(r'mean_volume: ([-\d.]+) dB', vol)
    pg = re.search(r'max_volume: ([-\d.]+) dB', vol)
    mean = float(mg.group(1)) if mg else -99.0
    peak = float(pg.group(1)) if pg else 0.0
    frames = sorted(FRAMES.glob('*.png'))
    bright = int((np.asarray(Image.open(frames[len(frames)//2]).convert('RGB')).max(axis=2) > 140).sum())
    ok = (v['width']==720 and v['height']==1280 and v['codec_name']=='h264' and au and au['codec_name']=='aac'
          and int(v.get('nb_frames',0))==288 and abs(float(probe['format']['duration'])-12.0)<0.05
          and mean > -25 and peak < -0.5 and bright > 8000)
    return {'success': ok, 'width': v['width'], 'height': v['height'], 'fps': v['r_frame_rate'],
            'frames': int(v.get('nb_frames',0)), 'duration_s': float(probe['format']['duration']),
            'size_bytes': int(probe['format']['size']), 'mean_db': mean, 'peak_db': peak,
            'bright_pixels': bright}


def publish(path):
    if not GALLERY_REPO.exists(): return {'skipped': True}
    (GALLERY_REPO / path.name).write_bytes(path.read_bytes())
    gen = GALLERY_REPO / 'generate_gallery.py'
    if gen.exists(): run([PY, str(gen)], timeout=180)
    for cmd in [['git','-C',str(GALLERY_REPO),'add',path.name,'videos.html'],
                ['git','-C',str(GALLERY_REPO),'commit','-m','Publish policy-driven Asimov walk\n\nSigned: HUMAN://ROOT / >_æ:'],
                ['git','-C',str(GALLERY_REPO),'push','origin','gh-pages']]:
        try: run(cmd, timeout=300)
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
    args = json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
    if not TRACE.exists(): raise SystemExit('run policy_locomotion.py first')
    trace = json.loads(TRACE.read_text())
    if not trace.get('success'): raise SystemExit('policy trace did not pass its own gate')
    speed = build_audio()
    env = os.environ.copy(); env['HERMES_AE_TRACE'] = str(TRACE); env['HERMES_AE_FRAMES'] = str(FRAMES); env['HERMES_AE_CAMERA_FOLLOW'] = '1'
    run([PY, str(SCRIPTS / 'render_free_walk.py')], env=env, timeout=600)
    sh = hashlib.sha256(TRACE.read_bytes()).hexdigest()
    run(['ffmpeg','-y','-framerate','24','-i',str(FRAMES/'%05d.png'),'-i',str(AUDIO),
         '-af','volume=0.9','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',
         '-crf','20','-c:a','aac','-b:a','128k','-t','12',str(OUT)])
    q = qc(OUT)
    pub = publish(OUT) if (args.get('publish', True) and q['success']) else {'skipped': True}
    sys.path.insert(0,str(REPO_ROOT))
    spec=importlib.util.spec_from_file_location('ae',REPO_ROOT/'__init__.py')
    if spec is None or spec.loader is None: raise SystemExit('cannot load ae plugin')
    ae=importlib.util.module_from_spec(spec); spec.loader.exec_module(ae)
    rec=ae._receipt('VIDEO://POLICY_LOCOMOTION',{'authority':'HUMAN://ROOT','output':str(OUT),
        'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'duration_s':12.0,
        'policy':trace['policy'],'policy_sha256':trace['policy_sha256'],
        'trace_sha256':sh,'base_x':trace['base_x'],'com_x':trace['com_x'],
        'voice':'hermes-agent (M2)','speed':speed,'qc':q,'publish':pub})
    shutil.rmtree(FRAMES, ignore_errors=True)
    print(json.dumps({'success':q['success'],'output':str(OUT),
        'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'qc':q,'publish':pub,
        'base_x':round(trace['base_x'],4),'com_x':round(trace['com_x'],4),
        'receipt':rec['hash'],'authority':'HUMAN://ROOT'}))


if __name__=='__main__': main()
