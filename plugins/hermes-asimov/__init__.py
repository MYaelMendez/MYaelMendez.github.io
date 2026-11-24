"""Hermes-Asimov — robot actor / spokesrobot.

Official model: menloresearch/asimov-1 sim-model/asimov_1_25dof.
Voice: tiny-voca local TTS -> 16-bit PCM -> menlo-sdk speaker.play_pcm().
Every action is HUMAN://ROOT receipted. No robot is contacted in local mode;
SDK mode requires a configured robot (hybrid/livekit) and is explicit.
"""
import json, subprocess, os
from pathlib import Path
from datetime import datetime, timezone

PY = '/usr/local/bin/python3'
TTS = '/opt/data/tiny_voca_voice.py'
SDK_PLAY = str(Path(__file__).parent / 'sdk_play.py')
VIDEO = str(Path(__file__).parent / 'actor_video.py')
STUDIO = str(Path(__file__).parent / 'studio_video.py')
MODEL = Path('/opt/data/hermes-asimov/model')
RECEIPTS = Path(os.environ.get('HERMES_HOME', '/opt/data/.hermes')) / 'hermes-asimov-receipts.jsonl'


def _out(d):
    return json.dumps(d, ensure_ascii=False)


def _receipt(action, extra=None):
    e = {'ts': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
         'action': action, 'authority': 'HUMAN://ROOT'}
    if extra:
        e.update(extra)
    try:
        RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
        with RECEIPTS.open('a', encoding='utf-8') as f:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    except Exception:
        pass
    return e


def _run(cmd, timeout=300):
    p = subprocess.run([PY] + cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        return {'success': False, 'error': (p.stderr or p.stdout or 'subprocess failed')[-800:]}
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        return {'success': False, 'error': 'non-JSON output', 'raw': p.stdout[-400:]}


def register(ctx):
    def asimov_status(args: dict) -> str:
        urdf = MODEL / 'urdf' / 'asimov_1_25dof.urdf'
        mjcf = MODEL / 'xml' / 'asimov_1_25dof.xml'
        meshes = sorted((MODEL / 'meshes').glob('*.STL')) if (MODEL / 'meshes').exists() else []
        ok = urdf.exists() and mjcf.exists() and len(meshes) >= 26
        _receipt('ASIMOV://STATUS', {'ok': ok})
        return _out({'success': ok, 'actor': 'hermes-asimov',
                     'model': 'asimov_1_25dof', 'source': 'menloresearch/asimov-1',
                     'urdf': str(urdf), 'mjcf': str(mjcf), 'meshes': len(meshes),
                     'links': 26, 'joints': 25,
                     'speaker_contract': 'menlo.asimov.Robot.speaker.play_pcm',
                     'voice': 'tiny-voca (F2/M2, 24 kHz, local ONNX)',
                     'authority': 'HUMAN://ROOT'})

    def asimov_say(args: dict) -> str:
        text = args.get('text', '')
        if not text:
            return _out({'success': False, 'error': 'text is required'})
        voice = args.get('voice', 'M2')
        out = args.get('output', '/opt/data/hermes-asimov-speech.wav')
        mode = args.get('mode', 'local')  # local | sdk
        r = _run([TTS, '--text', text, '--voice', voice, '--output', out])
        if not r.get('success'):
            _receipt('ASIMOV://SAY', {'success': False, 'error': r.get('error')})
            return _out(r)
        played = {'mode': 'local', 'note': 'WAV rendered; no robot contacted'}
        if mode == 'sdk':
            played = _run([SDK_PLAY, out], timeout=180)
        result = {'success': True, 'actor': 'hermes-asimov', 'text': text,
                  'voice': voice, 'wav': out, 'sha256': r.get('sha256'),
                  'duration_s': r.get('duration_s'), 'speaker': played}
        _receipt('ASIMOV://SAY', {'success': True, 'sha256': r.get('sha256'),
                                  'voice': voice, 'mode': mode,
                                  'speaker': played.get('mode', mode)})
        return _out(result)

    def asimov_voice_video(args: dict) -> str:
        text = args.get('text', 'I am Hermes Asimov. Human root, receipts on every action.')
        out = args.get('output', '/opt/data/attachments/hermes-asimov-spokesrobot.mp4')
        r = _run([VIDEO, '--text', text, '--output', out], timeout=400)
        _receipt('ASIMOV://VIDEO', {'success': bool(r.get('success')),
                                    'output': out, 'sha256': r.get('sha256')})
        return _out(r)

    def asimov_studio_video(args: dict) -> str:
        clean = {k: v for k, v in args.items() if k in
                 ('script','seconds','voice','captions','physics','publish')}
        r = _run([STUDIO, json.dumps(clean)], timeout=1500)
        _receipt('ASIMOV://STUDIO_VIDEO', {'success': bool(r.get('success')),
                                           'sha256': r.get('sha256'),
                                           'physics': r.get('physics'),
                                           'publish': r.get('publish')})
        return _out(r)

    def asimov_receipts(args: dict) -> str:
        n = int(args.get('limit') or 10)
        lines = RECEIPTS.read_text(encoding='utf-8').splitlines() if RECEIPTS.exists() else []
        return _out({'success': True, 'authority': 'HUMAN://ROOT', 'count': len(lines),
                     'receipts': [json.loads(x) for x in lines[-n:]]})

    for name, fn, props in [
        ('asimov_status', asimov_status, {}),
        ('asimov_say', asimov_say, {
            'text': {'type': 'string'}, 'voice': {'type': 'string', 'enum': ['F2', 'M2']},
            'output': {'type': 'string'}, 'mode': {'type': 'string', 'enum': ['local', 'sdk']}}),
        ('asimov_voice_video', asimov_voice_video, {
            'text': {'type': 'string'}, 'output': {'type': 'string'}}),
        ('asimov_studio_video', asimov_studio_video, {
            'script': {'type': 'string'}, 'seconds': {'type': 'integer'},
            'voice': {'type': 'string', 'enum': ['F2','M2']},
            'captions': {'type': 'boolean'}, 'physics': {'type': 'boolean'},
            'publish': {'type': 'boolean'}}),
        ('asimov_receipts', asimov_receipts, {'limit': {'type': 'integer'}}),
    ]:
        ctx.register_tool(name=name, toolset='hermes-asimov', handler=fn,
                          schema={'type': 'object', 'properties': props,
                                  'required': ['text'] if name == 'asimov_say' else []})
