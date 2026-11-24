"""æ Policy decision engine.

Standalone stdlib module for any machine: Hermes runtime, Asimov body, Pi500
keyboard, Android MCP bridge, viewport, or commerce surface. Every evaluation
writes a receipt to the unified HUMAN://ROOT ledger.
"""
import hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
POLICY = Path(os.environ.get('HERMES_AE_POLICY', ROOT / 'ae-policy.json'))
LEDGER = Path(os.environ.get('HERMES_AE_LEDGER', HERMES_HOME / 'ae-receipts.jsonl'))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).exists() else None


def load():
    if not POLICY.exists():
        raise RuntimeError(f'policy missing: {POLICY}')
    return json.loads(POLICY.read_text(encoding='utf-8'))


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


def verify_chain():
    if not LEDGER.exists():
        return {'success': True, 'count': 0, 'head': 'GENESIS'}
    lines = [x for x in LEDGER.read_text(encoding='utf-8').splitlines() if x.strip()]
    prev, ok, broken = 'GENESIS', True, None
    for i, line in enumerate(lines):
        e = json.loads(line)
        h = e.pop('hash', None)
        if e.get('prev') != prev:
            ok, broken = False, i
            break
        calc = hashlib.sha256(json.dumps(e, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        if calc != h:
            ok, broken = False, i
            break
        prev = h
    return {'success': ok, 'count': len(lines), 'head': prev, 'broken_at': broken}


def expired(approval):
    exp = (approval or {}).get('expires_at')
    if not exp:
        return False
    try:
        dt = datetime.fromisoformat(str(exp).replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt < datetime.now(timezone.utc)
    except Exception:
        return True


def evaluate(request):
    policy = load()
    req = dict(request)
    actor = req.get('actor')
    action = str(req.get('action', 'unknown')).lower()
    source = str(req.get('source', 'local')).lower()
    controls = req.get('controls') or {}
    approval = req.get('approval') or {}
    reasons, rules = [], []

    def hit(rule_id, reason):
        rules.append(rule_id)
        reasons.append(reason)

    if not actor:
        hit('FAIL-001', 'missing actor')
    claim = req.get('authority_claim')
    if claim and str(claim) != 'HUMAN://ROOT':
        hit('AUTH-001', 'authority claim is not HUMAN://ROOT')
    if actor in (policy.get('revoked_actors') or []):
        hit('REV-001', 'actor is revoked')

    privileged = action in policy['privileged_actions']
    read_only = action in policy['read_only_actions']
    draft_source = source in ('agent_message', 'external_intent', 'marketplace',
                              'llm_agent', 'qr', 'url_discovery', 'nfc', 'discovery_link')
    deadman = bool(controls.get('arm')) and bool(controls.get('deadman'))
    signed = bool(approval.get('human')) and not expired(approval)

    if action not in policy['decision_matrix']:
        hit('FAIL-001', f'unknown action {action!r}')
    if draft_source and source in ('qr', 'url_discovery', 'nfc', 'discovery_link'):
        hit('AUTH-003', 'discovery source is not permission')
    elif draft_source:
        hit('AUTH-002', 'agent/external source is a draft until approved')

    if privileged:
        if signed:
            hit('APP-001', 'human-root approval is bound and unexpired')
        elif deadman:
            hit('ACT-001', 'armed deadman present for actuation')
        else:
            hit('ACT-001', 'privileged action requires approval or armed deadman')
    if read_only and not actor:
        hit('FAIL-001', 'read-only action still requires actor identity')

    deny = any(r in ('FAIL-001', 'AUTH-001', 'AUTH-003', 'REV-001') for r in rules)
    needs = (not deny and privileged and not (signed or deadman)) or \
            (not deny and draft_source and not signed and not read_only)
    decision = 'deny' if deny else ('require_approval' if needs else 'allow')

    rec = receipt('POLICY://EVALUATE', {
        'decision': decision, 'action': action, 'actor': actor, 'source': source,
        'policy_sha256': sha(POLICY), 'rules': rules, 'reasons': reasons,
    })
    return {'success': True, 'policy': policy['name'], 'policy_sha256': sha(POLICY),
            'decision': decision, 'allow': decision == 'allow', 'rules': rules,
            'reasons': reasons, 'authority': policy['authority'], 'receipt': rec}


def show():
    p = load()
    return {'success': True, 'policy': p, 'policy_sha256': sha(POLICY)}


def verify():
    p = load()
    required = ['authority', 'glyph', 'chain', 'rules', 'decision_matrix', 'fail_closed']
    checks = {
        'authority': p.get('authority') == 'HUMAN://ROOT',
        'glyph': p.get('glyph') == 'æ',
        'chain': p.get('chain') == ['HUMAN://ROOT', 'æ', 'ae', 'harness', 'RECEIPT'],
        'fail_closed': bool(p.get('fail_closed')),
        'rules': len(p.get('rules', [])) >= 8,
        'bindings': len(p.get('bindings', {})) >= 6,
        'ledger_chain': verify_chain()['success'],
    }
    return {'success': all(checks.values()), 'checks': checks,
            'policy_sha256': sha(POLICY)}


def run(args):
    action = args.get('action', 'show')
    if action == 'verify':
        return verify()
    if action == 'evaluate':
        return evaluate(args.get('request', args))
    return show()


if __name__ == '__main__':
    try:
        print(json.dumps(run(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}), ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'success': False, 'error': f'{type(exc).__name__}: {exc}'}))
