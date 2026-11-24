"""Native Asimov head viewport controller.

The head mask and three exterior covers are programmable viewport surfaces.
There is no tablet face. Low-bandwidth voice fallback and Pi500 teleop remain
available; every mode change and teleop command is receipted on the unified
HUMAN://ROOT ledger.
"""
import hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
STATE = Path(os.environ.get('HERMES_AE_HEAD_STATE') or os.environ.get('HERMES_AE_FACE_STATE') or (HERMES_HOME / 'ae' / 'asimov-head.json'))
LEDGER = Path(os.environ.get('HERMES_AE_LEDGER', HERMES_HOME / 'ae-receipts.jsonl'))
TTS = Path(os.environ.get('HERMES_AE_TTS', HERMES_HOME / 'plugins' / 'tiny-voca-voice' / 'scripts' / 'tiny_voca_voice.py'))
PY = os.environ.get('HERMES_AE_PYTHON', '/usr/local/bin/python3')
AUDIO = HERMES_HOME / 'ae' / 'asimov-head-reply.wav'
DOM_SCRIPT = ROOT / 'scripts' / 'viewport_dom.py'

EXTERIOR_ZONES = [
    {'id': 'front_mask', 'part': 'ASV1_700_03C', 'role': 'primary LED viewport'},
    {'id': 'top_cover', 'part': 'ASV1_700_04C', 'role': 'status strip'},
    {'id': 'left_cover', 'part': 'ASV1_700_06C', 'role': 'side status strip'},
    {'id': 'right_cover', 'part': 'ASV1_700_07C', 'role': 'side status strip'},
]

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
    't': ('viewport', 'head', 'toggle'),
    'x': ('safety', 'all', 'safe_stop'),
}

DEFAULT_STATE = {
    'authority': 'HUMAN://ROOT',
    'viewport_enabled': True,
    'mode': 'viewport',
    'voice': 'M2',
    'wake_source': 'android-mcp',
    'exterior_zones': EXTERIOR_ZONES,
    'teleop': {'enabled': False, 'deadman': False, 'last_key': None},
    'note': 'native head viewport; the head never signs',
}


def _load():
    if not STATE.exists():
        return dict(DEFAULT_STATE)
    try:
        data = json.loads(STATE.read_text(encoding='utf-8'))
        out = dict(DEFAULT_STATE)
        out.update(data)
        out['teleop'] = dict(DEFAULT_STATE['teleop'], **(data.get('teleop') or {}))
        # Migrate legacy state without carrying tablet semantics forward.
        if 'viewport_enabled' not in out:
            out['viewport_enabled'] = bool(data.get('tablet_present', True))
        if out.get('mode') == 'tablet':
            out['mode'] = 'viewport'
        out.pop('tablet_present', None)
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
            'exterior_zones': EXTERIOR_ZONES,
            'voices': ['F2', 'M2'], 'keys': {k: list(v) for k, v in KEYMAP.items()},
            'tts_available': TTS.exists(), 'audio_path': str(AUDIO),
            'ledger': str(LEDGER), 'head': _last_hash()}


def _set_viewport(enabled, mode=None):
    state = _load()
    state['viewport_enabled'] = bool(enabled)
    state['mode'] = mode or ('viewport' if enabled else 'voice')
    if state['mode'] != 'teleop':
        state['teleop']['enabled'] = False
    _save(state)
    action = 'VIEWPORT://ENABLE' if enabled else 'VIEWPORT://DISABLE'
    rec = _receipt(action, {'mode': state['mode'], 'viewport_enabled': state['viewport_enabled'],
                            'exterior_zones': [z['id'] for z in EXTERIOR_ZONES]})
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
    rec = _receipt('VIEWPORT://VOICE_REPLY', {'text': str(text)[:240], 'voice': voice,
                                             'audio': str(AUDIO), 'bytes': AUDIO.stat().st_size if AUDIO.exists() else 0})
    return {'success': True, 'audio': str(AUDIO), 'voice': voice, 'mode': state['mode'], 'receipt': rec,
            'note': 'wake word and speech-to-text are supplied by Android MCP / phone; this op replies with tiny-voca'}


def _dom(args):
    if not DOM_SCRIPT.exists():
        return {'success': False, 'error': f'DOM projection script missing: {DOM_SCRIPT}'}
    payload = {
        'endpoint': args.get('endpoint', 'http://127.0.0.1:9222'),
        'match': args.get('match', 'asimov'),
        'selector': args.get('selector', ''),
    }
    proc = subprocess.run([PY, str(DOM_SCRIPT), json.dumps(payload, ensure_ascii=False)],
                          capture_output=True, text=True, timeout=120)
    try:
        out = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception:
        out = {'success': False, 'error': (proc.stderr or proc.stdout or 'dom read failed')[-800:]}
    return {
        'success': bool(out.get('success')),
        'authority': 'HUMAN://ROOT',
        'head': 'native Asimov head viewport',
        'read_only': True,
        'digest': out.get('digest'),
        'target': out.get('target'),
        'dom': out.get('dom'),
        'receipt': out.get('receipt'),
        'error': out.get('error'),
    }


def _teleop(key, arm, deadman):
    key = ' ' if key == 'space' else str(key).lower()
    if key not in KEYMAP:
        return {'success': False, 'error': 'unknown key', 'available': sorted(KEYMAP)}
    kind, group, command = KEYMAP[key]
    allowed = kind in ('safety', 'voice', 'viewport')
    if kind == 'motion' and not (arm and deadman):
        rec = _receipt('VIEWPORT://TELEOP_DENIED', {'key': key, 'group': group,
                                                   'command': command, 'reason': 'deadman/arm not engaged'})
        return {'success': False, 'error': 'arm and deadman required for motion',
                'receipt': rec, 'key': key}
    state = _load()
    state['teleop']['last_key'] = key
    state['teleop']['enabled'] = kind == 'motion' or state['mode'] == 'teleop'
    state['teleop']['deadman'] = bool(deadman)
    if kind == 'viewport' and command == 'toggle':
        state = _load()
        return _set_viewport(not state['viewport_enabled'], 'voice')
    _save(state)
    detail = {'key': key, 'kind': kind, 'group': group, 'command': command,
              'arm': bool(arm), 'deadman': bool(deadman), 'mode': state['mode']}
    rec = _receipt('VIEWPORT://TELEOP', detail)
    return {'success': True, 'mode': state['mode'], 'command': detail, 'receipt': rec}


def run(args):
    action = args.get('action', 'status')
    if action == 'status':
        return _status()
    if action in ('enable', 'attach', 'on'):
        return _set_viewport(True, args.get('mode', 'viewport'))
    if action in ('disable', 'detach', 'off'):
        return _set_viewport(False, args.get('mode', 'voice'))
    if action == 'voice':
        return _voice(args.get('text'), args.get('voice', _load().get('voice', 'M2')))
    if action in ('dom', 'dom_read', 'project_dom'):
        return _dom(args)
    if action == 'teleop':
        return _teleop(args.get('key'), bool(args.get('arm')), bool(args.get('deadman')))
    if action == 'keys':
        return {'success': True, 'keys': {k: list(v) for k, v in KEYMAP.items()},
                'note': 'motion requires --arm and deadman engaged'}
    return {'success': False, 'error': f'unknown action {action!r}',
            'available': ['status', 'enable', 'disable', 'voice', 'dom', 'teleop', 'keys']}


if __name__ == '__main__':
    try:
        payload = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
        print(json.dumps(run(payload), ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'success': False, 'error': f'{type(exc).__name__}: {exc}'}))
