"""DAO Brain for the native Asimov head viewport.

The DAO brain deliberates proposals as a governance layer, never as an
authority root. It evaluates every proposal through æ Policy, maps the decision
to a head-viewport state, optionally replies with tiny-voca, and writes a
hash-chained DAO://DECISION receipt.
"""
import hashlib, importlib.util, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
FACE_STATE = Path(os.environ.get('HERMES_AE_FACE_STATE', HERMES_HOME / 'ae' / 'asimov-face.json'))
LEDGER = Path(os.environ.get('HERMES_AE_LEDGER', HERMES_HOME / 'ae-receipts.jsonl'))
TTS = Path(os.environ.get('HERMES_AE_TTS', HERMES_HOME / 'plugins' / 'tiny-voca-voice' / 'scripts' / 'tiny_voca_voice.py'))
AUDIO = HERMES_HOME / 'ae' / 'dao-head-reply.wav'
PY = os.environ.get('HERMES_AE_PYTHON', '/usr/local/bin/python3')

STATE_COLORS = {
    'IDLE': (0, 204, 255), 'LISTENING': (0, 204, 255), 'THINKING': (133, 233, 252),
    'SPEAKING': (212, 175, 55), 'AWAITING_APPROVAL': (212, 175, 55),
    'APPROVED': (0, 255, 159), 'REFUSED': (255, 0, 255), 'ERROR': (255, 59, 71),
}


def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f'cannot load {path}')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def policy_engine():
    return _module('ae_policy_engine', ROOT / 'scripts' / 'ae_policy.py')


def face_module():
    return _module('head_viewport_engine', ROOT / 'scripts' / 'head_viewport.py')


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


def _sha_obj(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def state_for(decision, intent, speak):
    if decision == 'deny':
        return 'REFUSED'
    if decision == 'require_approval':
        return 'AWAITING_APPROVAL'
    if decision != 'allow':
        return 'ERROR'
    if intent in ('publish', 'actuate', 'teleop', 'commerce', 'checkout', 'payment', 'external_write'):
        return 'APPROVED'
    if speak:
        return 'SPEAKING'
    if intent in ('read', 'observe', 'probe', 'inspect', 'verify', 'speak', 'voice'):
        return 'LISTENING'
    return 'IDLE'


def reply_for(decision, intent):
    if decision == 'require_approval':
        return 'Proposal received. Private-client approval required.'
    if decision == 'deny':
        return 'Refused by æ policy. Authority stays with HUMAN ROOT.'
    if decision != 'allow':
        return 'DAO brain error. Receipt written.'
    if intent in ('publish', 'actuate', 'teleop', 'commerce', 'checkout', 'payment', 'external_write'):
        return 'Approved under HUMAN ROOT. Executing through a governed harness.'
    return 'Observation complete. Receipt written.'


def _speak(text, voice):
    if not TTS.exists():
        return {'success': False, 'error': f'tiny-voca CLI missing: {TTS}'}
    AUDIO.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    home = os.environ.get('HERMES_AE_TINY_VOCA_HOME')
    if home:
        env['TINY_VOCA_HOME'] = home
    p = subprocess.run([PY, str(TTS), '--text', text, '--voice', voice, '--output', str(AUDIO)],
                       capture_output=True, text=True, timeout=300, env=env)
    if p.returncode != 0:
        return {'success': False, 'error': (p.stderr or p.stdout)[-600:]}
    return {'success': True, 'audio': str(AUDIO), 'voice': voice,
            'bytes': AUDIO.stat().st_size if AUDIO.exists() else 0}


def status():
    face = face_module()._load()
    p = policy_engine()
    pv = p.run({'action': 'verify'})
    return {'success': True, 'authority': 'HUMAN://ROOT',
            'dao_brain': face.get('dao_brain'), 'face_mode': face.get('mode'),
            'viewport_enabled': face.get('viewport_enabled'),
            'policy_sha256': p.sha(p.POLICY), 'policy_verify': pv['success'],
            'ledger_head': _last_hash()}


def propose(args):
    embedded = args.get('request') if isinstance(args.get('request'), dict) else {}
    intent = str(args.get('intent') or embedded.get('action') or args.get('action_request') or 'unknown').lower()
    proposal = {
        'actor': args.get('actor') or embedded.get('actor') or 'vision-model',
        'action': intent,
        'source': args.get('source') or embedded.get('source') or 'vision-model',
        'approval': args.get('approval') or embedded.get('approval'),
        'controls': args.get('controls') or embedded.get('controls'),
        'authority_claim': args.get('authority_claim') or embedded.get('authority_claim'),
    }
    proposal = {k: v for k, v in proposal.items() if v is not None}
    p = policy_engine()
    policy_result = p.run({'action': 'evaluate', 'request': proposal})
    decision = policy_result['decision']
    speak = bool(args.get('speak'))
    state = state_for(decision, intent, speak)
    reply = reply_for(decision, intent)
    proposal_sha = _sha_obj(proposal)
    dao = {
        'face_state': state,
        'color': list(STATE_COLORS[state]),
        'last_decision': decision,
        'last_intent': intent,
        'last_source': proposal['source'],
        'last_proposal_sha256': proposal_sha,
        'last_reply': reply,
        'policy_sha256': p.sha(p.POLICY),
        'updated_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
    }
    fm = face_module()
    face = fm._load()
    face['dao_brain'] = dao
    fm._save(face)
    rec = receipt('DAO://DECISION', {'decision': decision, 'face_state': state,
                                     'intent': intent, 'actor': proposal['actor'],
                                     'source': proposal['source'], 'proposal_sha256': proposal_sha,
                                     'policy_sha256': dao['policy_sha256'],
                                     'policy_rules': policy_result['rules']})
    out = {'success': True, 'authority': 'HUMAN://ROOT', 'decision': decision,
           'allow': policy_result['allow'], 'face_state': state, 'color': dao['color'],
           'reply': reply, 'proposal_sha256': proposal_sha,
           'policy': {'decision': decision, 'rules': policy_result['rules'],
                      'reasons': policy_result['reasons']},
           'receipt': rec}
    if speak:
        out['voice'] = _speak(reply, args.get('voice', 'M2'))
    return out


def set_state(args):
    state = str(args.get('state', 'IDLE')).upper()
    if state not in STATE_COLORS:
        return {'success': False, 'error': 'unknown state', 'available': sorted(STATE_COLORS)}
    fm = face_module()
    face = fm._load()
    dao = face.get('dao_brain') or {}
    dao['face_state'] = state
    dao['color'] = list(STATE_COLORS[state])
    dao['updated_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    face['dao_brain'] = dao
    fm._save(face)
    rec = receipt('DAO://STATE', {'face_state': state})
    return {'success': True, 'face_state': state, 'receipt': rec}


def verify():
    p = policy_engine()
    pv = p.run({'action': 'verify'})
    face = face_module()._load()
    dao = face.get('dao_brain') or {}
    checks = {
        'policy_verify': bool(pv.get('success')),
        'authority': face.get('authority') == 'HUMAN://ROOT',
        'face_state': dao.get('face_state') in STATE_COLORS,
        'ledger_chain': p.verify_chain()['success'],
    }
    return {'success': all(checks.values()), 'checks': checks, 'dao_brain': dao}


def run(args):
    action = args.get('action', 'status')
    if action == 'propose':
        return propose(args)
    if action == 'state':
        return set_state(args)
    if action == 'verify':
        return verify()
    return status()


if __name__ == '__main__':
    try:
        print(json.dumps(run(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}), ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'success': False, 'error': f'{type(exc).__name__}: {exc}'}))
