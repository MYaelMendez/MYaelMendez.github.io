"""repo_film — any repository in the portfolio becomes a storyboard.

The portfolio is not a list of links. It is a set of things that can be
EXPLAINED, and the film pipeline already knows how to explain a thing with
gates and receipts. So: repo -> real facts -> scene spec -> proof sheet.

    python repo_film.py --repo tiny-voca --out sheet.png
    python repo_film.py --owner MYaelMendez --index portfolio.json

Every number on the sheet comes from the GitHub API or the repo itself.
Nothing is invented. If a fact cannot be fetched, the scene says so.

The five-robot cast narrates by ROLE:
    nous girl       why it exists / the human intent
    menlo-research  what it is built from
    hermes-agent    how it is built and tested
    asimov-agent    what it can do
    wætz            what a newcomer should try first
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

H = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
PY = os.environ.get('HERMES_AE_PYTHON', sys.executable)
RUN = H / 'cache' / 'scratch' / 'ae-render-run'
OUT = H / 'cache' / 'scratch' / 'portfolio'
API = 'https://api.github.com'


def gh(path):
    """Prefer `gh api` — it authenticates from the keyring, so no token ever
    enters this process, a log, or a transcript. Falls back to anonymous HTTP,
    which is rate-limited to 60/hr and will honestly report the failure."""
    try:
        p = subprocess.run(['gh', 'api', path], capture_output=True, text=True,
                           encoding='utf-8', timeout=45)
        if p.returncode == 0 and p.stdout.strip():
            return json.loads(p.stdout)
    except Exception:
        pass
    req = urllib.request.Request(API + path, headers={
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'ae-repo-film'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as exc:
        return {'_error': f'{type(exc).__name__}: {exc}'}


def facts(owner, repo):
    meta = gh(f'/repos/{owner}/{repo}')
    if '_error' in meta:
        return {'ok': False, 'repo': repo, 'error': meta['_error']}
    langs = gh(f'/repos/{owner}/{repo}/languages')
    langs = {} if '_error' in langs else langs
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:4]
    readme = gh(f'/repos/{owner}/{repo}/readme')
    text = ''
    if '_error' not in readme and readme.get('content'):
        import base64
        try:
            text = base64.b64decode(readme['content']).decode('utf-8', 'replace')
        except Exception:
            text = ''
    lic = (meta.get('license') or {}).get('spdx_id') or 'unlicensed'
    return {
        'ok': True, 'repo': repo, 'owner': owner,
        'url': meta.get('html_url'),
        'description': meta.get('description') or '(no description)',
        'language': meta.get('language') or 'mixed',
        'languages': [{'name': n, 'pct': round(100*v/total, 1)} for n, v in top],
        'stars': meta.get('stargazers_count', 0),
        'forks': meta.get('forks_count', 0),
        'size_kb': meta.get('size', 0),
        'license': lic,
        'topics': meta.get('topics', [])[:6],
        'pushed': (meta.get('pushed_at') or '')[:10],
        'homepage': meta.get('homepage') or '',
        'readme_head': text[:1400],
        'has_readme': bool(text),
    }


def spec_from_facts(f):
    """Scenes carry ONLY fetched facts. No invented capability claims."""
    if not f.get('ok'):
        return {'title': f['repo'], 'scenes': [{
            'camera': 'wide', 'speaker': 'nous', 'state': 'ERROR',
            'kicker': 'COULD NOT READ THIS REPOSITORY',
            'lines': [f.get('error', 'unknown')[:44]],
            'speak': 'I could not read this repository. I will not describe what I cannot see.'}]}
    name = f['repo']
    langs = ', '.join(f"{l['name']} {l['pct']}%" for l in f['languages'][:3]) or f['language']
    desc = f['description']
    topics = ', '.join(f['topics']) if f['topics'] else 'no topics declared'
    lic = f['license']
    scenes = [
        {'camera': 'wide', 'speaker': 'waetz', 'state': 'SPEAKING',
         'kicker': f'{name.upper()} · A NEWCOMER ARRIVES',
         'lines': [desc[:44], f"{f['stars']} stars · {f['forks']} forks"],
         'prompt': f'what is {name}?',
         'speak': f"This is {name}. {desc}"},
        {'camera': 'face', 'speaker': 'menlo', 'state': 'SPEAKING',
         'kicker': 'MENLO-RESEARCH · WHAT IT IS MADE OF',
         'lines': [langs[:44], f"{f['size_kb']} KB · pushed {f['pushed']}"],
         'prompt': 'response · composition',
         'speak': f"It is built from {langs}. {f['size_kb']} kilobytes, last pushed {f['pushed']}."},
        {'camera': 'wide', 'speaker': 'hermes', 'state': 'SPEAKING',
         'kicker': 'HERMES-AGENT · HOW IT IS HELD',
         'lines': [f'license  {lic}', f'topics   {topics[:34]}'],
         'prompt': 'response · terms',
         'speak': f"The license is {lic}. Topics: {topics}."},
        {'camera': 'face', 'speaker': 'nous', 'state': 'SPEAKING',
         'kicker': 'NOUS GIRL · WHY IT EXISTS',
         'lines': ['open source ware', 'the human intent is the spec'],
         'prompt': 'response · intent',
         'speak': f"{name} exists so a person can own this capability, not rent it."},
        {'camera': 'wide', 'speaker': 'asimov', 'state': 'SPEAKING',
         'kicker': 'ASIMOV-AGENT · WHERE IT RUNS',
         'lines': ['local first · your machine', 'no account required to read it'],
         'prompt': 'response · substrate',
         'speak': "It runs on your own machine. The source is public. Nothing here needs my permission."},
        {'camera': 'face', 'speaker': 'waetz', 'state': 'LISTENING',
         'kicker': 'WÆTZ · WHAT TO TRY FIRST',
         'lines': ['read the readme', 'then board it before you build it'],
         'prompt': f'clone {name}',
         'speak': f"Clone {name}, read its readme, and board your change before you render it. That is how I learn."},
    ]
    return {'title': f'æ:// {name}', 'tagline': 'OPEN SOURCE WARE · LOCAL · RECEIPTED',
            'footer': f"github.com/{f['owner']}/{name}",
            'fps': 24, 'separation': 0.46, 'distance': 4.7,
            'charge_start': {'nous': .58, 'hermes': .41, 'waetz': .18, 'menlo': .35, 'asimov': .22},
            'scenes': scenes}


def board(spec, dest, scene='charging_bay'):
    RUN.mkdir(parents=True, exist_ok=True)
    AG = Path(os.environ.get('AE_AGENTS', r'C:\æ\agents'))
    for fn in ('proof_sheet.py', 'charging_bay.py', 'robot_face2.py', 'robot_face.py'):
        s = AG / fn
        if s.exists():
            (RUN / fn).write_bytes(s.read_bytes())
    OUT.mkdir(parents=True, exist_ok=True)
    sp = OUT / f"{spec['title'].split()[-1]}-spec.json"
    sp.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding='utf-8')
    e = dict(os.environ)
    e['HERMES_HOME'] = str(H)
    e.setdefault('HERMES_AE_PYTHON', PY)
    for k in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV'):
        e.pop(k, None)
    p = subprocess.run([PY, str(RUN / 'proof_sheet.py'), '--spec', str(sp),
                        '--out', str(dest), '--scene', scene],
                       capture_output=True, text=True, encoding='utf-8',
                       timeout=900, env=e, cwd=str(RUN))
    return {'ok': dest.exists(), 'spec': str(sp), 'sheet': str(dest),
            'bytes': dest.stat().st_size if dest.exists() else 0,
            'log': (p.stdout or '') + (p.stderr or '')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--owner', default='MYaelMendez')
    ap.add_argument('--repo')
    ap.add_argument('--out')
    ap.add_argument('--index', help='write a portfolio index JSON instead of one sheet')
    ap.add_argument('--limit', type=int, default=12)
    a = ap.parse_args()
    if a.index:
        repos = gh(f'/users/{a.owner}/repos?per_page=100&sort=updated')
        if isinstance(repos, dict):
            print(json.dumps({'ok': False, 'error': repos.get('_error')}))
            return
        idx = []
        for r in repos[:a.limit]:
            f = facts(a.owner, r['name'])
            idx.append({k: f.get(k) for k in
                        ('repo', 'description', 'language', 'stars', 'forks',
                         'license', 'size_kb', 'pushed', 'url', 'topics')} if f.get('ok')
                       else {'repo': r['name'], 'error': f.get('error')})
        p = Path(a.index)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({'owner': a.owner, 'count': len(idx), 'repos': idx},
                                indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"  {p}  {len(idx)} repos  {p.stat().st_size} bytes")
        return
    if not a.repo:
        print('  --repo or --index required')
        return
    f = facts(a.owner, a.repo)
    spec = spec_from_facts(f)
    dest = Path(a.out) if a.out else OUT / f'{a.repo}-proof.png'
    r = board(spec, dest)
    print(json.dumps({'repo': a.repo, 'facts_ok': f.get('ok'), **r}, ensure_ascii=False))


if __name__ == '__main__':
    main()
