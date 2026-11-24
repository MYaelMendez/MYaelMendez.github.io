"""Removable Asimov face / low-bandwidth fallback controller.

The face is an OPTIONAL 1:1 tablet presence module. Removing it does not remove
the agent: Asimov falls back to tiny-voca voice replies, and optionally to a
Pi500 keyboard teleop client. Every mode change and teleop command is receipted
on the unified HUMAN://ROOT ledger.
"""
import hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
STATE = Path(os.environ.get('HERMES_AE_FACE_STATE', HERMES_HOME / 'ae' / 'asimov-face.json'))
LEDGER = Path(os.environ.get('HERMES_AE_LEDGER', HERMES_HOME / 'ae-receipts.jsonl'))
TTS = Path(os.environ.get('HERMES_AE_TTS', HERMES_HOME / 'plugins' / 'tiny-voca-voice' / 'scripts' / 'tiny_voca_voice.py'))
PY = os.environ.get('HERMES_AE_PYTHON', '/usr/local/bin/python3')
AUDIO = HERMES_HOME / 'ae' / 'asimov-face-reply.wav'

KEYMAP = {
    'w': ('motion', 'locomotion', 'forward'),
    's': ('motion', 'locomotion', 'backward'),
    'a': ('motion', 'locomotion', 'turn_left'),
    'd': ('motion', 'locomotion', 'turn_right'),
    'q': ('motion', 'left_arm', 'raise'),
    'e': ('motion', 'right_arm', 'raise'),
    'r': ('motion', 'head', 'look_up'),
    'f': ('motion', 'head', 'look_down'),
    ' ': ('safety', 'all', 'all_stop'),
    'v': ('voice', 'voice', 'listen'),
    't': ('face', 'tablet', 'toggle'),
    'x': ('safety', 'all', 'safe_stop'),
}

DEFAULT_STATE = {
    'authority': 'HUMAN://ROOT',
    'tablet_present': True,
    'mode': 'tablet',
    'voice': 'M2',
    'wake_source': 'android-mcp',
    'teleop': {'enabled': False, 'deadman': False, 'last_key': None},
    'note': 'face is a presence module, not the authority root',
}


def _load():
    if not STATE.exists():
        return dict(DEFAULT_STATE)
    try:
        data = json.loads(STATE.read_text(encoding='utf-8'))
        out = dict(DEFAULT_STATE)
        out.update(data)
        out['teleop'] = dict(DEFAULT_STATE['teleop'], **(data.get('teleop') or {}))
        return out
    except Exception:
        return dict(DEFAULT_STATE)


def _save(state):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def _last_hash():
    if not LEDGER.exists():
        return 'GENESIS'
    lines = [x for x in LEDGER.read_text(encoding='utf-8').splitlines() if x.strip()]
    try:
        return json.loads(lines[-1])['hash'] if lines else 'GENESIS'
    except Exception:
        return 'GENESIS'


def _receipt(action, detail):
    e = {'ts': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
         'action': action, 'authority': 'HUMAN://ROOT', 'prev': _last_hash(),
         'detail': detail}
    payload = json.dumps(e, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    e['hash'] = hashlib.sha256(payload.encode()).hexdigest()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open('a', encoding='utf-8') as f:
        f.write(json.dumps(e, ensure_ascii=False) + '\n')
    return e


def _status():
    state = _load()
    return {'success': True, 'authority': 'HUMAN://ROOT', 'state': state,
            'dao_brain': state.get('dao_brain'),
            'voices': ['F2', 'M2'], 'keys': {k: list(v) for k, v in KEYMAP.items()},
            'tts_available': TTS.exists(), 'audio_path': str(AUDIO),
            'ledger': str(LEDGER), 'head': _last_hash()}


def _set_tablet(present, mode=None):
    state = _load()
    state['tablet_present'] = bool(present)
    state['mode'] = mode or ('tablet' if present else 'voice')
    if state['mode'] != 'teleop':
        state['teleop']['enabled'] = False
    _save(state)
    action = 'FACE://ATTACH' if present else 'FACE://DETACH'
    rec = _receipt(action, {'mode': state['mode'], 'tablet_present': state['tablet_present']})
    return {'success': True, 'state': state, 'receipt': rec}


def _voice(text, voice):
    if not text:
        return {'success': False, 'error': 'text is required (ASR/wake source is external)'}
    if not TTS.exists():
        return {'success': False, 'error': f'tiny-voca CLI missing: {TTS}'}
    AUDIO.parent.mkdir(parents=True, exist_ok=True)
    cmd = [PY, str(TTS), '--text', str(text), '--voice', voice, '--output', str(AUDIO)]
    env = dict(os.environ)
    tts_home = os.environ.get('HERMES_AE_TINY_VOCA_HOME')
    if tts_home:
        env['TINY_VOCA_HOME'] = tts_home
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env)
    if p.returncode != 0:
        return {'success': False, 'error': (p.stderr or p.stdout)[-800:]}
    state = _load()
    rec = _receipt('FACE://VOICE_REPLY', {'text': str(text)[:240], 'voice': voice,
                                         'audio': str(AUDIO), 'bytes': AUDIO.stat().st_size if AUDIO.exists() else 0})
    return {'success': True, 'audio': str(AUDIO), 'voice': voice, 'mode': state['mode'], 'receipt': rec,
            'note': 'wake word and speech-to-text are supplied by Android MCP / phone; this op replies with tiny-voca'}


def _teleop(key, arm, deadman):
    key = ' ' if key == 'space' else str(key).lower()
    if key not in KEYMAP:
        return {'success': False, 'error': 'unknown key', 'available': sorted(KEYMAP)}
    kind, group, command = KEYMAP[key]
    allowed = kind in ('safety', 'voice', 'face')
    if kind == 'motion' and not (arm and deadman):
        rec = _receipt('FACE://TELEOP_DENIED', {'key': key, 'group': group,
                                               'command': command, 'reason': 'deadman/arm not engaged'})
        return {'success': False, 'error': 'arm and deadman required for motion',
                'receipt': rec, 'key': key}
    state = _load()
    state['teleop']['last_key'] = key
    state['teleop']['enabled'] = kind == 'motion' or state['mode'] == 'teleop'
    state['teleop']['deadman'] = bool(deadman)
    if kind == 'face' and command == 'toggle':
        state = _load()
        return _set_tablet(not state['tablet_present'], 'voice')
    _save(state)
    detail = {'key': key, 'kind': kind, 'group': group, 'command': command,
              'arm': bool(arm), 'deadman': bool(deadman), 'mode': state['mode']}
    rec = _receipt('FACE://TELEOP', detail)
    return {'success': True, 'mode': state['mode'], 'command': detail, 'receipt': rec}


def run(args):
    action = args.get('action', 'status')
    if action == 'status':
        return _status()
    if action == 'attach':
        return _set_tablet(True, args.get('mode', 'tablet'))
    if action == 'detach':
        return _set_tablet(False, args.get('mode', 'voice'))
    if action == 'voice':
        return _voice(args.get('text'), args.get('voice', _load().get('voice', 'M2')))
    if action == 'teleop':
        return _teleop(args.get('key'), bool(args.get('arm')), bool(args.get('deadman')))
    if action == 'keys':
        return {'success': True, 'keys': {k: list(v) for k, v in KEYMAP.items()},
                'note': 'motion requires --arm and deadman engaged'}
    return {'success': False, 'error': f'unknown action {action!r}',
            'available': ['status', 'attach', 'detach', 'voice', 'teleop', 'keys']}


if __name__ == '__main__':
    try:
        payload = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
        print(json.dumps(run(payload), ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'success': False, 'error': f'{type(exc).__name__}: {exc}'}))
