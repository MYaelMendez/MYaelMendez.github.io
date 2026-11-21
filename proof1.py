#!/usr/bin/env python3
"""proof1.py — render a PROOF/1 spec into a receipted film.

    python proof1.py <name>.proof.json            # -> <name>.mp4 + receipt + meta
    python proof1.py <name>.proof.json --dry      # resolve + report, render nothing

A proof/film/1 spec is the whole artefact: identity, emoji context, beats
(sources + provenance), voice, overlays, gates and the output receipt. The
renderer is deterministic — same spec + same sources -> same bytes.

Laws: the spec commands; a gate refusal is repaired in the spec, never by
lowering a threshold; every source is cited in-frame.
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FFMPEG = Path(os.environ.get(
    'FFMPEG', 'C:/Users/yaelm/AppData/Local/hermes/tools/ffmpeg-7.1-nvenc/bin/ffmpeg.exe'))
FFPROBE = FFMPEG.parent / 'ffprobe.exe'
TCV = Path('C:/æ/tinycudavideo/tinycudavideo.py')
VOICE = Path('C:/æ/osw-voice-lab/det_voice.py')

GOLD = (212, 175, 55)
INK = (235, 232, 225)
DIM = (140, 132, 110)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def font(size: int):
    for c in ('C:/Windows/Fonts/consola.ttf', 'C:/Windows/Fonts/cour.ttf',
              'C:/Windows/Fonts/lucon.ttf'):
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def duration(p: Path) -> float:
    r = subprocess.run([str(FFPROBE), '-v', 'error', '-show_entries',
                        'format=duration', '-of', 'csv=p=0', str(p)],
                       capture_output=True, text=True, timeout=120)
    return float(r.stdout.strip() or 0)


def resolve_sources(spec: dict) -> list[dict]:
    b = spec['beats']
    assets = sorted(Path(b['sources_dir']).glob(b['glob']), key=sha256_file)
    if len(assets) < b['count']:
        raise SystemExit(f"need {b['count']} sources, found {len(assets)}")
    out = []
    labels = b.get('labels', [])
    expected = b.get('expected', [])
    for i, p in enumerate(assets[:b['count']]):
        s = sha256_file(p)
        if i < len(expected) and expected[i].get('sha256') not in (None, s):
            raise SystemExit(
                f'source drift: {p.name} is {s[:16]}…, spec records '
                f'{expected[i]["sha256"][:16]}… — refuse, do not render')
        out.append({'beat': i + 1, 'source': p, 'name': p.name,
                    'label': labels[i] if i < len(labels) else None,
                    'sha256': s, 'bytes': p.stat().st_size,
                    'duration_s': round(duration(p), 3)})
    return out


def synth_voice(spec: dict, work: Path) -> Path | None:
    v = spec.get('voice')
    if not v or not v.get('text'):
        return None
    wav = work / 'voice.wav'
    r = subprocess.run([sys.executable, str(VOICE), 'synth', '--text', v['text'],
                        '--voice', v.get('voice', 'hermes'), '--seed', str(v.get('seed', 9)),
                        '--out', str(wav)], capture_output=True, text=True, timeout=900)
    if r.returncode != 0 or not wav.exists():
        print(r.stdout[-800:], r.stderr[-800:])
        raise SystemExit('voice synthesis failed')
    d = duration(wav)
    lim = v.get('max_seconds')
    if lim and d > lim:
        raise SystemExit(f'voice {d:.3f}s exceeds max_seconds {lim} — size the line')
    print(f'  voice {d:.3f}s (limit {lim})')
    return wav


def slice_beat(src: Path, out_dir: Path, fps: int) -> list[Path]:
    d = duration(src)
    t0 = max(0.0, (d - 1.0) / 2.0)
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(FFMPEG), '-y', '-v', 'error', '-ss', f'{t0:.3f}',
                    '-i', str(src), '-t', '1.0',
                    '-vf', f'fps={fps},scale={W}:{H}:flags=lanczos',
                    '-pix_fmt', 'rgb24', str(out_dir / 'f%03d.png')],
                   check=True, timeout=300)
    return sorted(out_dir.glob('f*.png'))


def overlay(img, spec, beat, total, src_name, src_sha, fi, n_per, label=None):
    o = spec['overlay']
    W, H = img.size
    d = ImageDraw.Draw(img)
    f_big, f_mid = font(190), font(44)
    f_small, f_tiny = font(30), font(24)
    f_lab = font(34)

    panel = tuple(o.get('lower_third', {}).get('fill', [22, 19, 13]))
    sb = o.get('source_block', {})
    if sb:
        x0, y0, x1, y1 = sb.get('rect', [0, 540, 620, 720])
        d.rectangle([x0, y0, x1, y1], fill=panel)
        d.rectangle([x0, y0, x1, y0 + 3], fill=GOLD)
        d.text((x0 + 4, y0 + 20), 'SOURCE', font=f_tiny, fill=DIM)
        d.text((x0 + 4, y0 + 56), src_name[:34], font=f_small, fill=INK)
        d.text((x0 + 4, y0 + 110), src_sha[:sb.get('sha256_chars', 32)],
               font=f_small, fill=GOLD)

    if o.get('beat_numeral', True):
        d.text((48, 168), f'{beat:02d}', font=f_big, fill=GOLD)
        d.text((52, 380), f'/ {total:02d}', font=f_mid, fill=DIM)
    if label:
        d.text((52, 470), label, font=f_lab, fill=INK)

    lt = o.get('lower_third', {})
    band_top = H - lt.get('height', 250)
    d.rectangle([0, band_top, W, H], fill=panel)
    d.rectangle([0, band_top, W, band_top + 3], fill=GOLD)

    if o.get('progress_cells') == 'per_frame':
        cw, ch, gap = 26, 10, 6
        x0, y0 = 52, band_top + 46
        for i in range(n_per):
            x = x0 + i * (cw + gap)
            d.rectangle([x, y0, x + cw, y0 + ch],
                        fill=GOLD if i <= fi else (38, 36, 30))

    d.text((52, band_top + 104), o.get('footer', 'GPL'), font=f_tiny, fill=DIM)
    d.text((52, band_top + 146),
           f'asset {beat:02d}/{total:02d} · checked back · sha256',
           font=f_tiny, fill=GOLD)
    return img


def main() -> int:
    global W, H
    ap = argparse.ArgumentParser()
    ap.add_argument('spec')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()

    spec = json.loads(Path(a.spec).read_text(encoding='utf-8'))
    assert spec.get('schema') == 'proof/film/1', 'not a proof/film/1 spec'
    W, H = spec.get('size', [720, 1280])
    fps = spec.get('fps', 24)
    name = spec['output']['name']
    outdir = Path(a.spec).resolve().parent / 'render'
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f'{name}.mp4'

    print(f"  spec   {spec['title']} — {spec['tagline']}")
    srcs = resolve_sources(spec)
    for s in srcs:
        print(f"    beat {s['beat']:02d} ← {s['name']}  {s['sha256'][:16]}")
    if a.dry:
        return 0

    work = outdir / (name + '-work')
    frames = work / 'frames'
    frames.mkdir(parents=True, exist_ok=True)
    wav = synth_voice(spec, work)

    n_per = int(round(spec['beats']['per_beat_seconds'] * fps))
    idx = 0
    for s in srcs:
        for j, f in enumerate(slice_beat(s['source'], work / f"b{s['beat']:02d}", fps)):
            im = Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS)
            overlay(im, spec, s['beat'], len(srcs), s['name'], s['sha256'], j, n_per,
                    s.get('label'))
            im.save(frames / f'f{idx:05d}.png')
            idx += 1
    total = idx
    print(f'  {total} frames · {total / fps:.3f} s')

    cmd = [sys.executable, str(TCV), 'produce', '--frames', str(frames),
           '--out', str(out), '--fps', str(fps), '--emoji',
           spec.get('emoji', {}).get('symbol', '🤖')]
    if wav:
        cmd += ['--audio', str(wav)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    sys.stdout.write(r.stdout[-1500:])
    if r.returncode != 0:
        print(r.stderr[-1200:])
        return r.returncode

    g = subprocess.run([sys.executable, str(TCV), 'gate', str(out)],
                       capture_output=True, text=True, timeout=600)
    gate = json.loads(g.stdout[g.stdout.find('{'):])
    rec = subprocess.run([sys.executable, str(TCV), 'receipt', str(out)],
                         capture_output=True, text=True, timeout=600)
    receipt = json.loads(rec.stdout[rec.stdout.find('{'):])

    meta = {'schema': 'proof/film/1', 'spec': str(a.spec), 'title': spec['title'],
            'tagline': spec['tagline'], 'seconds': round(total / fps, 3),
            'frames': total, 'fps': fps, 'size': [W, H],
            'emoji': spec.get('emoji'), 'voice': spec.get('voice'),
            'sources': [{k: v for k, v in s.items() if k != 'source'} for s in srcs],
            'gate': gate, 'receipt': receipt}
    (outdir / f'{name}.meta.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    (outdir / f'{name}.receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(f"  sha256 {receipt['sha256']}")
    print(f"  gate   {'PASS' if gate.get('ok') else 'FAIL'}  lum {gate['pixels']['luminance']}"
          f"  mov {gate['pixels']['motion']}  black {gate['pixels']['black_pct']}")
    return 0 if gate.get('ok') else 1


if __name__ == '__main__':
    raise SystemExit(main())
