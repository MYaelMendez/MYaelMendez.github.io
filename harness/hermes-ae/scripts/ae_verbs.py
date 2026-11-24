"""æ Robot Verbs — governed wrappers over official Menlo SDK verbs.

No invented wire verbs: stand/damp/set_velocity/trajectory are Menlo wire verbs;
balance/set_joints are official SDK verbs; media calls use the official camera,
microphone and speaker objects. Every call passes æ Policy first and writes a
receipt. Live execution is opt-in with HERMES_AE_SDK_LIVE=1.
"""
import hashlib, importlib.util, json, os, sys, time, wave
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
LEDGER = Path(os.environ.get('HERMES_AE_LEDGER', HERMES_HOME / 'ae-receipts.jsonl'))

VERBS = {
    'status':       {'official': 'importlib.metadata.version("menlo-sdk")', 'class': 'read', 'note': 'SDK version and saved-robot presence only; sends nothing.'},
    'state':        {'official': 'Robot.get_state()', 'class': 'read', 'alias': 'get_state'},
    'get_state':    {'official': 'Robot.get_state()', 'class': 'read'},
    'check':        {'official': 'Robot.get_state() facts', 'class': 'read', 'note': 'Report mode, arming, faults, alerts, battery; sends nothing.'},
    'stand':        {'official': 'Robot.stand()', 'class': 'motion'},
    'damp':         {'official': 'Robot.damp()', 'class': 'motion'},
    'balance':      {'official': 'Robot.balance()', 'class': 'motion'},
    'set_velocity': {'official': 'Robot.set_velocity()', 'class': 'motion'},
    'trajectory':   {'official': 'Robot.trajectory()', 'class': 'motion'},
    'set_joints':   {'official': 'Robot.set_joints()', 'class': 'motion'},
    'photo':        {'official': 'Robot.camera.photo()', 'class': 'media'},
    'capture_clip': {'official': 'Robot.camera.capture_clip()', 'class': 'media'},
    'record_audio': {'official': 'Robot.microphone.chunks()', 'class': 'media'},
    'play_pcm':     {'official': 'Robot.speaker.play_pcm()', 'class': 'media'},
}


def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f'cannot load {path}')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def policy_engine():
    return _module('ae_policy_for_verbs', ROOT / 'scripts' / 'ae_policy.py')


def _sha_obj(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def _last_hash():
    if not LEDGER.exists():
        return 'GENESIS'
    lines = [x for x in LEDGER.read_text(encoding='utf-8').splitlines() if x.strip()]
    try:
        return json.loads(lines[-1])['hash'] if lines else 'GENESIS'
    except Exception:
        return 'GENESIS'


def receipt(action, detail):
    e = {'ts': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
         'action': action, 'authority': 'HUMAN://ROOT', 'prev': _last_hash(),
         'detail': detail}
    payload = json.dumps(e, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    e['hash'] = hashlib.sha256(payload.encode()).hexdigest()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open('a', encoding='utf-8') as f:
        f.write(json.dumps(e, ensure_ascii=False) + '\n')
    return e


def _sdk_version():
    try:
        import importlib.metadata as md
        return md.version('menlo-sdk')
    except Exception as exc:
        return f'unavailable: {type(exc).__name__}'


def list_verbs():
    return {'success': True, 'authority': 'HUMAN://ROOT', 'count': len(VERBS),
            'sdk_version': _sdk_version(), 'verbs': VERBS,
            'note': 'No invented wire verbs; media methods are official SDK objects on Robot.camera / microphone / speaker.'}


def _safe(value):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _state_dict(state):
    out = {}
    for key in ('mode', 'armed', 'battery', 'fault', 'alert'):
        value = getattr(state, key, None)
        if value is not None:
            out[key] = _safe(value)
    return out


def _live(verb, args):
    from menlo.asimov import Robot
    if verb == 'status':
        return {'sdk_version': _sdk_version(), 'saved_robot': Path(HERMES_HOME, '.menlo', 'robots.toml').exists()}
    if verb in ('state', 'get_state', 'check'):
        with Robot().connect() as robot:
            return {'state': _state_dict(robot.get_state())}
    if verb in ('stand', 'damp', 'balance', 'set_velocity', 'trajectory', 'set_joints'):
        with Robot().connect() as robot:
            result = getattr(robot, verb)(**args)
            return {'sent': _safe(result), 'state_after': _state_dict(robot.get_state())}
    with Robot().connect(require_state=False) as robot:
        if verb == 'photo':
            frame = robot.camera.photo(**args)
            return {'photo': {'width': getattr(frame, 'width', None), 'height': getattr(frame, 'height', None)}}
        if verb == 'capture_clip':
            clip = robot.camera.capture_clip(**args)
            return {'clip': _safe(clip)}
        if verb == 'record_audio':
            seconds = float(args.get('seconds', 1.0))
            timeout = float(args.get('timeout', 5.0))
            deadline = time.monotonic() + seconds
            chunks = 0
            for chunk in robot.microphone.chunks(timeout=timeout):
                chunks += 1
                if time.monotonic() >= deadline:
                    break
            return {'audio_chunks': chunks, 'seconds': seconds}
        if verb == 'play_pcm':
            path = Path(args.get('wav') or args.get('path') or '')
            if not path.exists():
                return {'error': 'wav/path is required for play_pcm'}
            with wave.open(str(path), 'rb') as w:
                if w.getsampwidth() != 2:
                    return {'error': 'wav must be 16-bit PCM'}
                rate, channels = w.getframerate(), w.getnchannels()
                pcm = w.readframes(w.getnframes())
            step = int(rate) * 2 * channels
            chunks = 0
            for start in range(0, len(pcm), step):
                robot.speaker.play_pcm(pcm[start:start+step], sample_rate_hz=rate, channels=channels)
                chunks += 1
            return {'played_s': round(len(pcm) / (2 * channels * rate), 3), 'chunks': chunks}
    return {'error': 'unsupported verb'}


def call(args):
    verb = str(args.get('verb') or args.get('action') or '').lower()
    if verb not in VERBS:
        return {'success': False, 'error': 'unknown verb', 'available': sorted(VERBS)}
    live = bool(args.get('live'))
    payload = {k: v for k, v in args.items() if k not in ('verb', 'action', 'live', 'approval', 'controls', 'actor', 'source')}
    request = {
        'actor': args.get('actor') or 'hermes-ae',
        'action': verb,
        'source': args.get('source') or 'local',
        'approval': args.get('approval'),
        'controls': args.get('controls'),
        'authority_claim': args.get('authority_claim'),
    }
    request = {k: v for k, v in request.items() if v is not None}
    p = policy_engine()
    decision = p.run({'action': 'evaluate', 'request': request})
    args_sha = _sha_obj(payload)
    detail = {'verb': verb, 'official': VERBS[verb]['official'], 'decision': decision['decision'],
              'args_sha256': args_sha, 'policy_sha256': p.sha(p.POLICY),
              'sdk_version': _sdk_version(), 'actor': request['actor']}
    result = {'success': True, 'authority': 'HUMAN://ROOT', 'verb': verb,
              'official': VERBS[verb]['official'], 'decision': decision['decision'],
              'allowed': decision['allow'], 'rules': decision['rules'],
              'reasons': decision['reasons'], 'args_sha256': args_sha}

    if decision['decision'] == 'deny':
        detail['executed'] = False
        result['executed'] = False
        result['receipt'] = receipt('SDK://VERB_DENIED', detail)
        return result
    if not live:
        detail['executed'] = False
        result['executed'] = False
        result['mode'] = 'dry_run'
        result['plan'] = {'import': 'menlo.asimov', 'object': 'Robot', 'call': VERBS[verb]['official'], 'args': payload}
        result['receipt'] = receipt('SDK://VERB_PLAN', detail)
        return result
    if os.environ.get('HERMES_AE_SDK_LIVE') != '1':
        return {'success': False, 'error': 'live execution requires HERMES_AE_SDK_LIVE=1',
                'decision': decision['decision'], 'allowed': decision['allow']}
    try:
        out = _live(verb, payload)
        detail['executed'] = True
        result['executed'] = True
        result['mode'] = 'live'
        result['result'] = out
        result['receipt'] = receipt('SDK://VERB', detail)
    except Exception as exc:
        detail['executed'] = False
        detail['error'] = str(exc)[:600]
        result['success'] = False
        result['executed'] = False
        result['error'] = str(exc)[:600]
        result['receipt'] = receipt('SDK://VERB_ERROR', detail)
    return result


def run(args):
    action = args.get('action', 'list')
    if action == 'list':
        return list_verbs()
    if action in ('call', 'execute', 'plan'):
        return call(args)
    return {'success': False, 'error': f'unknown action {action!r}', 'available': ['list', 'call', 'plan', 'execute']}


if __name__ == '__main__':
    try:
        print(json.dumps(run(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}), ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'success': False, 'error': f'{type(exc).__name__}: {exc}'}))
