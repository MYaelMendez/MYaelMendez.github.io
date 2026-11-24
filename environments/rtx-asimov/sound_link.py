"""sound_link — the film's world stops being silent.

A robot that speaks in a silent room is still in a mute world. Voice is not
sound design. This derives an audio Spec from the FILM's own scene timings, so
every impact lands on a cut by construction, never by hand-nudging.

    film spec (scenes with t0/t1, state, speaker)
        → audio Spec (bed + events at exact times)
        → orb DSP render (numpy only, deterministic, 48 kHz stereo)
        → mix under the voices
        → receipt

Upstream: stdevMac/orb-audio (Apache-2.0 code + planner weights).
The optional 9.1M 'detail' model is NON-COMMERCIAL and is never loaded here.

Determinism is the contract: same film spec → identical audio bytes.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

H = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
SOUND = Path(os.environ.get('AE_SOUND', H / 'cache' / 'scratch' / 'sound'))
PY = os.environ.get('HERMES_AE_PYTHON', sys.executable)
FF = H / 'tools' / 'ffmpeg-7.1-nvenc' / 'bin'
LEDGER = H / 'sound-receipts.jsonl'
SR = 48000

# state → what the world does. The refusal has weight; approval resolves.
STATE_SOUND = {
    'SPEAKING':          [('swell', 0.00, 0.45, -26.0)],
    'THINKING':          [('ui_pop', 0.00, 0.20, -24.0)],
    'LISTENING':         [('click', 0.00, 0.12, -27.0)],
    'AWAITING_APPROVAL': [('sub_drop', 0.00, 1.40, -16.0), ('bell', 0.05, 1.80, -22.0)],
    'APPROVED':          [('bell', 0.00, 1.60, -18.0), ('swell', 0.00, 0.80, -24.0)],
    'REFUSED':           [('glitch', 0.00, 0.55, -18.0), ('sub_drop', 0.02, 1.20, -18.0)],
    'ERROR':             [('glitch', 0.00, 0.70, -16.0)],
    'IDLE':              [],
}


def _canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def _head():
    if LEDGER.exists():
        ls = [l for l in LEDGER.read_text(encoding='utf-8').splitlines() if l.strip()]
        if ls:
            try:
                return json.loads(ls[-1])['hash']
            except Exception:
                pass
    return '0' * 64


def receipt(action, detail):
    b = {'ts': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
         'action': action, 'authority': 'HUMAN://ROOT', 'detail': detail, 'prev': _head()}
    b['hash'] = hashlib.sha256(_canon(b).encode('utf-8')).hexdigest()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open('a', encoding='utf-8') as fh:
        fh.write(_canon(b) + '\n')
    return b


def spec_from_film(film: dict, *, texture='sci_fi', bed_db=-30.0,
                   dock_clicks=True, seed_base=100) -> dict:
    """Derive the audio Spec from the film's scene boundaries.

    Timings come from the film. Nothing is placed by ear.
    """
    scenes = film.get('scenes', [])
    total = float(film.get('_total') or sum(s.get('_dur', 0.0) for s in scenes))
    if not total:
        raise ValueError('film spec has no timings — render it first, or pass _total')
    events = []
    seed = seed_base
    t = 0.0
    for i, s in enumerate(scenes):
        t0 = float(s.get('_t0', t))
        dur = float(s.get('_dur', s.get('_t1', t0) - t0))
        t = t0 + dur
        st = s.get('state', 'SPEAKING')
        # the dock engages on every cut — this is the cut, audibly
        if dock_clicks and i > 0:
            events.append(dict(role='click', t=round(t0, 3), dur=0.10,
                               gain_db=-22.0, pan=0.0, seed=seed))
            seed += 1
        for role, off, d, g in STATE_SOUND.get(st, []):
            tt = t0 + off
            if tt + d <= total + 0.5:
                events.append(dict(role=role, t=round(tt, 3), dur=d,
                                   gain_db=g, pan=0.0, seed=seed))
                seed += 1
        # a banner is a beat — give it air
        if s.get('banner'):
            events.append(dict(role='riser', t=round(max(0.0, t0 - 0.6), 3), dur=0.65,
                               gain_db=-25.0, pan=0.0, seed=seed))
            seed += 1
    # the last scene resolves
    if scenes:
        events.append(dict(role='bell', t=round(max(0.0, total - 2.2), 3), dur=2.0,
                           gain_db=-21.0, pan=0.0, seed=seed))
    return dict(duration=round(total, 3), texture=texture, mood='calm',
                bed_gain_db=bed_db, events=events)


def render(audio_spec: dict, out_wav: Path) -> dict:
    """orb DSP path: numpy only, no torch, no checkpoint, no detail model.

    The grammar bounds a Spec at MAX_EVENTS=8. A film longer than a few scenes
    needs more, so we LAYER: one bed render (texture, zero events) plus N event
    renders (texture='none', <=8 events each), all at full duration with events
    at their absolute times, then sum. Summing is exact and deterministic, and
    the bed is counted once rather than N times.
    """
    src = SOUND / 'src'
    if not src.exists():
        return {'ok': False, 'refused': True, 'reason': f'Sound repo not found: {SOUND}'}
    out_wav.parent.mkdir(parents=True, exist_ok=True)

    events = audio_spec.get('events', [])
    dur = audio_spec['duration']
    layers = [dict(duration=dur, texture=audio_spec.get('texture', 'sci_fi'),
                   mood=audio_spec.get('mood', 'calm'),
                   bed_gain_db=audio_spec.get('bed_gain_db', -30.0), events=[])]
    for i in range(0, len(events), 8):
        layers.append(dict(duration=dur, texture='none', mood='calm',
                           events=events[i:i + 8]))

    code = (
        "import sys,json,hashlib,pathlib,numpy as np,wave;"
        f"sys.path.insert(0,{str(src)!r});"
        "from orb.api import render_spec;"
        "layers=json.loads(sys.stdin.read());"
        "acc=None;"
        "\nfor L in layers:"
        "\n    a=render_spec(L)"
        "\n    acc=a if acc is None else acc+a"
        "\npeak=float(np.abs(acc).max()) or 1.0"
        "\nif peak>0.95: acc=acc*(0.95/peak)"
        "\npcm=(np.clip(acc,-1,1)*32767).astype('<i2')"
        f"\nwith wave.open({str(out_wav)!r},'wb') as w:"
        "\n    w.setnchannels(2 if acc.ndim>1 else 1); w.setsampwidth(2); w.setframerate(48000)"
        "\n    w.writeframes(pcm.tobytes())"
        f"\nprint(json.dumps({{'sha256':hashlib.sha256(pathlib.Path({str(out_wav)!r}).read_bytes()).hexdigest(),"
        f"'bytes':pathlib.Path({str(out_wav)!r}).stat().st_size,'torch':'torch' in sys.modules,"
        "'peak':peak,'layers':len(layers)}))"
    )
    e = dict(os.environ)
    for k in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV'):
        e.pop(k, None)
    p = subprocess.run([PY, '-c', code], input=json.dumps(layers),
                       capture_output=True, text=True, encoding='utf-8',
                       timeout=900, env=e, cwd=str(SOUND))
    try:
        r = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        return {'ok': False, 'refused': True,
                'reason': (p.stderr or p.stdout or 'no output')[-500:]}
    r.update(ok=True, wav=str(out_wav), events=len(events),
             duration=dur, texture=audio_spec.get('texture'))
    r['receipt'] = receipt('SOUND://RENDER', {k: r[k] for k in ('sha256', 'bytes', 'events')})
    return r


def mix(film_mp4: Path, bed_wav: Path, out_mp4: Path, *, voice_gain=1.0, bed_gain=0.55) -> dict:
    """Mix the world UNDER the voices. Speech stays intelligible; the bed sits below."""
    if not film_mp4.exists():
        return {'ok': False, 'refused': True, 'reason': f'film missing: {film_mp4}'}
    if not bed_wav.exists():
        return {'ok': False, 'refused': True, 'reason': f'bed missing: {bed_wav}'}
    # [1] = film's own voice track, [2] = the world. amix with weights, then limit.
    fc = (f'[1:a]volume={voice_gain}[v];'
          f'[2:a]volume={bed_gain}[b];'
          '[v][b]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[m];'
          '[m]alimiter=limit=0.95[a]')
    cmd = [str(FF / 'ffmpeg.exe'), '-v', 'error', '-y',
           '-i', str(film_mp4), '-i', str(film_mp4), '-i', str(bed_wav),
           '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
           '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
           '-movflags', '+faststart', str(out_mp4)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=900)
    if not out_mp4.exists():
        return {'ok': False, 'refused': True, 'reason': (p.stderr or 'mux failed')[-400:]}
    r = {'ok': True, 'out': str(out_mp4), 'bytes': out_mp4.stat().st_size,
         'voice_gain': voice_gain, 'bed_gain': bed_gain}
    r['receipt'] = receipt('SOUND://MIX', {'bytes': r['bytes'], 'bed_gain': bed_gain})
    return r


def world(film_meta: Path, film_mp4: Path, out_mp4: Path, **kw) -> dict:
    """film meta (with timings) → world spec → DSP → mix. One call, receipted."""
    meta = json.loads(Path(film_meta).read_text(encoding='utf-8'))
    spec = meta.get('spec', meta)
    if '_total' not in spec and 'total_s' in meta:
        spec['_total'] = meta['total_s']
    for s, m in zip(spec.get('scenes', []), meta.get('scenes', [])):
        for k in ('_t0', '_t1', 't0', 't1'):
            if k in m:
                s[k] = m[k]
        if 't0' in m and 't1' in m:
            s['_t0'], s['_dur'] = m['t0'], m['t1'] - m['t0']
    a = spec_from_film(spec, **{k: v for k, v in kw.items()
                                if k in ('texture', 'bed_db', 'dock_clicks', 'seed_base')})
    wav = Path(out_mp4).with_suffix('.world.wav')
    r = render(a, wav)
    if not r.get('ok'):
        return r
    m = mix(Path(film_mp4), wav, Path(out_mp4),
            **{k: v for k, v in kw.items() if k in ('voice_gain', 'bed_gain')})
    m['world_spec'] = a
    m['render'] = {k: r[k] for k in ('sha256', 'bytes', 'events', 'torch')}
    return m
