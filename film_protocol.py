"""film:// — the cinematic pipeline, addressable from >_æ://

The film industry de-risks before it spends: screenplay is cheap, principal
photography is expensive. A worldwide user computing at robot level should
start at the STORYBOARD, not at a 35-minute render.

    film://                    the stages and their gates
    film://board <spec>        PRE-PROD: one frame per scene, ~20s, human-judgeable
    film://render <spec>       PRODUCTION: background job, returns a handle
    film://status <job>        the job's frames, gate verdict, receipt
    film://jobs                recent renders

Stage discipline (cinematic-development-model): a stage advances when its GATE
passes, never on a timer. The board is the human gate; SupervisorVideo is the
machine gate. Both are required — the machine measures pixels, the human judges
whether it is right.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SCHEME = 'film://'
AUTHORITY = 'HUMAN://ROOT'
H = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
AGENTS = Path(os.environ.get('AE_AGENTS', r'C:\æ\agents'))
PY = os.environ.get('HERMES_AE_PYTHON', sys.executable)
RUN = H / 'cache' / 'scratch' / 'ae-render-run'
PREVIEW = H / 'cache' / 'scratch' / 'preview'

STAGES = [
    {'stage': 'DEVELOPMENT', 'artifact': 'narrative structure',
     'gate': 'is it a coherent story?', 'cost': 'seconds'},
    {'stage': 'GREENLIGHT', 'artifact': 'scene spec (JSON)',
     'gate': 'bounded and renderable', 'cost': 'seconds'},
    {'stage': 'PRE-PROD', 'artifact': 'storyboard sheet', 'tool': 'film://board',
     'gate': 'THE HUMAN LOOKS AND APPROVES', 'cost': '~20s'},
    {'stage': 'PRODUCTION', 'artifact': 'frames', 'tool': 'film://render',
     'gate': 'deterministic, 0 black frames', 'cost': '~35min for five bodies'},
    {'stage': 'POST', 'artifact': 'master + audio', 'tool': 'auto on encode',
     'gate': 'SupervisorVideo PASS + receipt', 'cost': '~1min'},
    {'stage': 'DISTRIBUTION', 'artifact': 'published URL',
     'gate': 'live HTTP 200, verified', 'cost': '~2min'},
]


def _env():
    e = dict(os.environ)
    e['HERMES_HOME'] = str(H)
    e.setdefault('HERMES_AE_PYTHON', PY)
    e.setdefault('TINY_VOCA_HOME', str(H / 'tiny-voca'))
    for k in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV'):
        e.pop(k, None)
    return e


def _stage_files():
    RUN.mkdir(parents=True, exist_ok=True)
    for f in ('proof_sheet.py', 'charging_bay.py', 'asimov_studio3.py',
              'asimov_studio.py', 'robot_face2.py', 'robot_face.py'):
        s = AGENTS / f
        if s.exists():
            (RUN / f).write_bytes(s.read_bytes())


def _refuse(reason, **extra):
    return {'success': False, 'refused': True, 'scheme': SCHEME,
            'authority': AUTHORITY, 'reason': reason, **extra}


def stages():
    return {'success': True, 'scheme': SCHEME, 'authority': AUTHORITY,
            'model': 'cinematic-development-model', 'stages': STAGES,
            'rule': 'A stage advances when its gate passes, never on a timer.',
            'note': 'The board is the HUMAN gate. SupervisorVideo is the machine gate. '
                    'Both are required: pixels are measurable, rightness is not.'}


def board(spec_path, scene='charging_bay', out=None):
    sp = Path(spec_path)
    if not sp.exists():
        return _refuse(f'spec not found: {sp}')
    _stage_files()
    runner = RUN / 'proof_sheet.py'
    if not runner.exists():
        return _refuse(f'proof_sheet missing: {runner}')
    PREVIEW.mkdir(parents=True, exist_ok=True)
    dest = Path(out) if out else PREVIEW / f'{sp.stem}-proof.png'
    try:
        p = subprocess.run([PY, str(runner), '--spec', str(sp), '--out', str(dest),
                            '--scene', scene], capture_output=True, text=True,
                           encoding='utf-8', timeout=600, env=_env(), cwd=str(RUN))
    except Exception as exc:
        return _refuse(f'{type(exc).__name__}: {exc}')
    if not dest.exists():
        return _refuse('board produced no image', log=(p.stderr or p.stdout or '')[-400:])
    spec = json.loads(sp.read_text(encoding='utf-8'))
    return {'success': True, 'scheme': SCHEME, 'authority': AUTHORITY,
            'stage': 'PRE-PROD', 'artifact': str(dest), 'bytes': dest.stat().st_size,
            'scenes': len(spec.get('scenes', [])),
            'gate': 'HUMAN — look at the sheet and approve before rendering',
            'approved': False,
            'next': f'film://render {sp}',
            'note': 'Cheap representation of the same decision. Judge it, then spend.'}


def render(spec_path, scene='charging_bay', name=None, smoke=0):
    import importlib.util as u
    rj = H / 'plugins' / 'hermes-asimov' / 'render_jobs.py'
    if not rj.exists():
        return _refuse(f'render_jobs missing: {rj}')
    s = u.spec_from_file_location('rj_film', rj)
    m = u.module_from_spec(s)
    s.loader.exec_module(m)
    r = m.launch(scene=scene, spec=spec_path, name=name, smoke=smoke)
    r.update(scheme=SCHEME, stage='PRODUCTION',
             human_gate='run film://board first — the sheet is the cheap decision')
    return r


def status(job_id):
    import importlib.util as u
    rj = H / 'plugins' / 'hermes-asimov' / 'render_jobs.py'
    if not rj.exists():
        return _refuse(f'render_jobs missing: {rj}')
    s = u.spec_from_file_location('rj_film2', rj)
    m = u.module_from_spec(s)
    s.loader.exec_module(m)
    r = m.status(job_id)
    r.update(scheme=SCHEME)
    return r


def jobs(limit=8):
    import importlib.util as u
    rj = H / 'plugins' / 'hermes-asimov' / 'render_jobs.py'
    if not rj.exists():
        return _refuse(f'render_jobs missing: {rj}')
    s = u.spec_from_file_location('rj_film3', rj)
    m = u.module_from_spec(s)
    s.loader.exec_module(m)
    return m.listing(limit)


def dispatch(raw):
    s = raw.strip()
    if s.startswith(SCHEME):
        s = s[len(SCHEME):]
    parts = s.split(None, 1)
    route = parts[0].lower() if parts else ''
    rest = parts[1].strip() if len(parts) > 1 else ''
    if route in ('', 'stages', 'status'):
        return stages()
    if route in ('board', 'storyboard', 'previz', 'proof'):
        if not rest:
            return _refuse('spec path required', usage='film://board <spec.json>')
        return board(rest)
    if route == 'render':
        if not rest:
            return _refuse('spec path required', usage='film://render <spec.json>')
        return render(rest)
    if route == 'job':
        return status(rest) if rest else _refuse('job_id required')
    if route == 'jobs':
        return jobs()
    return _refuse(f'unknown route {route!r}',
                   routes=['', 'stages', 'board', 'render', 'job', 'jobs'])


if __name__ == '__main__':
    print(json.dumps(dispatch(' '.join(sys.argv[1:]) or SCHEME), ensure_ascii=False))
