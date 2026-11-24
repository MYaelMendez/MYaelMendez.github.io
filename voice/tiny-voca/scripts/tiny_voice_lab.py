"""tinyVOICE Voice Lab — consent-gated SOVÆREIGN binding and Chinese ad prep."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import tiny_voca_paths as paths  # noqa: E402

LAB_HOME = paths.hermes_home() / 'tiny-voice-lab'
BIND_CARD = LAB_HOME / 'voice-card.json'
AD_SCRIPT = ROOT / 'examples' / 'tiny-voice' / 'chinese-one-person-company.json'
VOICE = 'SOVÆREIGN'
ENV_KEYS = ('VOXMEL_REPO', 'VOXMEL_MODEL_DIR', 'VOXMEL_VOCOS_DIR',
            'VOXMEL_TOKENIZER_PATH', 'VOXMEL_PROMPT_AUDIO',
            'VOXMEL_PROMPT_TEXT', 'VOXMEL_CONSENT', 'VOXMEL_PYTHON')


def _out(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _fail(msg, **extra):
    obj = {'success': False, 'error': msg, 'authority': 'HUMAN://ROOT'}
    obj.update(extra)
    _out(obj)
    return 1


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _wav_info(p: Path) -> dict:
    with wave.open(str(p), 'rb') as w:
        return {'channels': w.getnchannels(), 'sampwidth': w.getsampwidth(),
                'rate': w.getframerate(), 'duration_s': round(w.getnframes() / w.getframerate(), 3)}


def _card():
    if not BIND_CARD.exists():
        return {'bound': False, 'voice': VOICE}
    return json.loads(BIND_CARD.read_text(encoding='utf-8'))


def op_card():
    card = _card()
    script = AD_SCRIPT if AD_SCRIPT.exists() else None
    ad = json.loads(script.read_text(encoding='utf-8')) if script else None
    _out({'success': True, 'authority': 'HUMAN://ROOT', 'lab': 'tinyVOICE Voice Lab',
          'voice': VOICE, 'compute_layer': 'human-twin', 'bound': card.get('bound', False),
          'voice_card': str(BIND_CARD), 'ad_script': str(script) if script else None,
          'ad_lines': len(ad.get('lines', [])) if ad else 0,
          'governance': 'HUMAN://ROOT → consent → VOICE://BIND → VOICE://SPEAK → RECEIPT',
          'requirements': ENV_KEYS})


def op_bind(args):
    reference = Path(args.reference).expanduser() if args.reference else None
    transcript = Path(args.transcript).expanduser() if args.transcript else None
    consent = Path(args.consent).expanduser() if args.consent else None
    if not reference or not reference.exists():
        raise FileNotFoundError('reference WAV is required')
    if reference.suffix.lower() != '.wav':
        raise ValueError('reference must be a WAV file')
    info = _wav_info(reference)
    if info['duration_s'] < 3:
        raise ValueError('reference WAV must be at least 3 seconds')
    if info['rate'] < 16000:
        raise ValueError('reference WAV must be at least 16 kHz')
    if not transcript or not transcript.exists():
        raise FileNotFoundError('exact reference transcript is required')
    if not consent or not consent.exists():
        raise FileNotFoundError('explicit consent file is required')
    consent_text = consent.read_text(encoding='utf-8')
    if 'HUMAN://ROOT' not in consent_text or 'consent' not in consent_text.lower():
        raise ValueError('consent file must contain HUMAN://ROOT and explicit consent')
    LAB_HOME.mkdir(parents=True, exist_ok=True)
    receipt = paths.append_custom_receipt({
        'action': paths.ACTION_VOICE_BIND, 'authority': 'HUMAN://ROOT',
        'voice': VOICE, 'provider': 'voxmel', 'compute_layer': 'human-twin',
        'reference_sha256': _sha(reference), 'transcript_sha256': _sha(transcript),
        'consent_sha256': _sha(consent), 'reference': info})
    card = {'bound': True, 'voice': VOICE, 'compute_layer': 'human-twin',
            'authority': 'HUMAN://ROOT', 'provider': 'voxmel',
            'reference': str(reference), 'reference_sha256': _sha(reference),
            'transcript': str(transcript), 'transcript_sha256': _sha(transcript),
            'consent': str(consent), 'consent_sha256': _sha(consent),
            'receipt_hash': receipt.get('hash'), 'wav': info}
    BIND_CARD.write_text(json.dumps(card, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    _out({'success': True, 'action': paths.ACTION_VOICE_BIND, 'voice': VOICE,
          'voice_card': str(BIND_CARD), 'receipt': receipt.get('hash'),
          'reference': info, 'authority': 'HUMAN://ROOT'})


def op_provision():
    env = {k: os.environ.get(k) for k in ENV_KEYS}
    missing = [k for k, v in env.items() if not v]
    bad_paths = []
    for k in ('VOXMEL_REPO', 'VOXMEL_MODEL_DIR', 'VOXMEL_VOCOS_DIR',
              'VOXMEL_TOKENIZER_PATH', 'VOXMEL_PROMPT_AUDIO',
              'VOXMEL_PROMPT_TEXT', 'VOXMEL_CONSENT'):
        v = env.get(k)
        if v and not Path(v).expanduser().exists():
            bad_paths.append(k)
    card = _card()
    ready = not missing and not bad_paths and bool(card.get('bound'))
    _out({'success': True, 'ready': ready, 'voice': VOICE,
          'bound': bool(card.get('bound')), 'missing_env': missing,
          'bad_paths': bad_paths, 'requirements': ENV_KEYS,
          'authority': 'HUMAN://ROOT'})


def _concat_wavs(parts, output):
    params = None
    chunks = []
    gap = b'\x00\x00' * int(0.18 * 24000)
    for i, p in enumerate(parts):
        with wave.open(str(p), 'rb') as w:
            if params is None:
                params = w.getparams()
            chunks.append(w.readframes(w.getnframes()))
            if i < len(parts) - 1:
                chunks.append(gap)
    if params is None:
        raise RuntimeError('no narration WAVs to concatenate')
    with wave.open(str(output), 'wb') as w:
        w.setnchannels(params.nchannels); w.setsampwidth(params.sampwidth)
        w.setframerate(params.framerate); w.writeframes(b''.join(chunks))
    return round(sum(len(c) / params.sampwidth / params.nchannels for c in chunks) / params.framerate, 3)


def op_ad(args):
    if not AD_SCRIPT.exists():
        raise FileNotFoundError(f'ad script missing: {AD_SCRIPT}')
    card = _card()
    if not card.get('bound'):
        raise RuntimeError('SOVÆREIGN is not bound; run voice lab bind first')
    if not os.environ.get('VOXMEL_REPO'):
        raise RuntimeError('VoxMel is not provisioned; run voice lab provision first')
    ad = json.loads(AD_SCRIPT.read_text(encoding='utf-8'))
    out = Path(args.out).expanduser() if args.out else LAB_HOME / 'chinese-ad'
    out.mkdir(parents=True, exist_ok=True)
    plan = {'success': True, 'authority': 'HUMAN://ROOT', 'voice': VOICE,
            'title': ad.get('title'), 'subtitle': ad.get('subtitle'),
            'lines': ad.get('lines', []), 'output_dir': str(out),
            'provider': 'voxmel', 'language': 'zh',
            'governance': 'HUMAN://ROOT → consent → VOICE://BIND → VOICE://SPEAK → RECEIPT'}
    if args.build_audio:
        wavs = []
        for i, line in enumerate(ad.get('lines', [])):
            wav = out / f'{i:02d}.wav'
            p = subprocess.run([
                sys.executable, str(SCRIPTS / 'tiny_voice.py'), '--op', 'speak',
                '--provider', 'voxmel', '--voice', VOICE, '--language', 'zh',
                '--text', str(line.get('text') or ''), '--output', str(wav)
            ], capture_output=True, text=True, timeout=900)
            if p.returncode != 0:
                raise RuntimeError((p.stderr or p.stdout or 'voxmel speak failed')[-1000:])
            res = json.loads(p.stdout.strip().splitlines()[-1])
            if not res.get('success'):
                raise RuntimeError(str(res.get('error') or 'voxmel speak failed'))
            wavs.append(wav)
        narration = out / 'narration.wav'
        duration = _concat_wavs(wavs, narration)
        plan['narration'] = str(narration)
        plan['narration_sha256'] = _sha(narration)
        plan['duration_s'] = duration
    (out / 'render-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    plan['render_plan'] = str(out / 'render-plan.json')
    _out(plan)


def main():
    p = argparse.ArgumentParser(description='tinyVOICE Voice Lab.')
    p.add_argument('--op', choices=('card', 'bind', 'provision', 'ad'), required=True)
    p.add_argument('--reference'); p.add_argument('--transcript'); p.add_argument('--consent')
    p.add_argument('--out'); p.add_argument('--build-audio', action='store_true')
    a = p.parse_args()
    try:
        if a.op == 'card':
            op_card(); return 0
        if a.op == 'bind':
            return op_bind(a)
        if a.op == 'provision':
            op_provision(); return 0
        return op_ad(a)
    except Exception as e:
        return _fail(f'{type(e).__name__}: {e}')


if __name__ == '__main__':
    raise SystemExit(main())
