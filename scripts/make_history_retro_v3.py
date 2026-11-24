#!/usr/bin/env python3
"""Render the legible 9:16 OpenSourceWare retrospective (v3, collision-safe)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1080, 1920
OUT = Path('/opt/data/MYaelMendez-work/artifacts/history-retrospective-916-v3.png')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
VOID = (5, 6, 7); INK = (232, 244, 236); MUTED = (145, 163, 153)
GREEN = (0, 255, 159); CYAN = (0, 204, 255); GOLD = (212, 175, 55); MAGENTA = (255, 0, 255)

im = Image.new('RGB', (W, H), VOID)
d = ImageDraw.Draw(im)

def f(size): return ImageFont.truetype(FONT, size)

def shadow_text(x, y, text, font, fill, anchor='la'):
    d.text((x + 2, y + 2), text, font=font, fill=(fill[0]//4, fill[1]//4, fill[2]//4), anchor=anchor)
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)

def wrap(text, font, max_width):
    out, cur = [], ''
    for word in text.split():
        trial = (cur + ' ' + word).strip()
        if d.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur: out.append(cur)
            cur = word
    if cur: out.append(cur)
    return out

# faint terminal grid + scanlines
for yy in range(48, H - 48, 44):
    d.line((38, yy, W - 38, yy), fill=(12, 22, 18), width=1)
for xx in range(38, W - 38, 44):
    d.line((xx, 48, xx, H - 48), fill=(10, 18, 16), width=1)
for yy in range(0, H, 3):
    d.line((0, yy, W, yy), fill=(0, 0, 0), width=1)

# border
d.rectangle((24, 24, W - 24, H - 24), outline=GREEN, width=2)
d.rectangle((34, 34, W - 34, H - 34), outline=GOLD, width=1)

# header
shadow_text(W//2, 72, 'OPENSOURCEWARE / INTERNET OF AGENTS', f(30), CYAN, 'ma')
shadow_text(W//2, 122, 'OUR ENTIRE HISTORY', f(76), GOLD, 'ma')
shadow_text(W//2, 218, 'three movements · one authority chain', f(34), MUTED, 'ma')
d.line((120, 268, W - 120, 268), fill=GOLD, width=2)

acts = [
    ('01', 'ORIGIN / AUTHORITY', CYAN, [
        'HUMAN://ROOT → æ → RECEIPT',
        'authorized agency made visible',
        'OpenSourceWare: intent → authority → execution → receipt → artifact',
        'æl.net · æ.store · æææ.com · soværeign.com',
        'commandprompt.ai · privateclient.ai · mobility.foundation · myaelmendez.github.io',
    ]),
    ('02', 'MACHINES / HARNESSES', GREEN, [
        '18 plugins → hermes-ae: one ae tool, one ledger',
        'harnesses: voice · ffmpeg · control · physics · viewport · robot · publish · course · ledger',
        'Asimov Agent: URDF/MJCF/USD twin · DAO Brain · æ Policy · face states',
        'ffmpeg deterministic camera; WebGL preview/control',
        'capability → gate → execution → receipt → artifact → address',
    ]),
    ('03', 'VOICE / NOW', MAGENTA, [
        'tinyVOCA → tinyVOICE: F2 · M2 · ROBOT · SOVÆREIGN (35.4s)',
        'broadcast timbre · tinyTELEPROMPTER · stick lessons · desktop dock · æ TV',
        'VoxMel-0.3B + Vocos ready; bf16 pushed; Chinese blocked by 2.2 GiB RAM',
        'storage: 325 artifacts offloaded · 3.4 GiB free',
    ]),
]

card_y = 280
for idx, (num, title, color, bullets) in enumerate(acts):
    card_h = 410 if idx == 0 else (430 if idx == 1 else 380)
    d.rounded_rectangle((42, card_y, W - 42, card_y + card_h), radius=16, fill=(8, 12, 10), outline=color, width=2)
    d.line((42, card_y + 8, W - 42, card_y + 8), fill=color, width=3)
    shadow_text(72, card_y + 20, num, f(40), color)
    shadow_text(142, card_y + 30, title, f(36), INK)
    d.line((72, card_y + 82, W - 72, card_y + 82), fill=color, width=1)
    y = card_y + 94
    for b in bullets:
        lines = wrap(b, f(24), W - 158)
        assert y + len(lines) * 34 <= card_y + card_h - 14, f'overflow {idx} {b}'
        for j, ln in enumerate(lines):
            x = 84 if j == 0 else 104
            d.ellipse((x - 18, y + 10, x - 11, y + 17), fill=GREEN)
            d.text((x, y), ln, font=f(24), fill=INK)
            y += 34
        y += 4
    card_y += card_h + 14

# doctrine
d.rounded_rectangle((42, 1530, W - 42, 1702), radius=16, fill=(10, 10, 9), outline=GOLD, width=2)
shadow_text(W//2, 1550, 'THE DOCTRINE', f(42), GOLD, 'ma')
shadow_text(W//2, 1614, 'authorized agency made visible', f(40), INK, 'ma')
shadow_text(W//2, 1670, 'human = root · agents ask · you hold · receipts public', f(29), GREEN, 'ma')

# footer
d.line((80, 1744, W - 80, 1744), fill=CYAN, width=2)
shadow_text(W//2, 1768, 'HUMAN://ROOT → æ → ae → RECEIPT', f(36), CYAN, 'ma')
shadow_text(W//2, 1834, '#opensourceware #internetofagents', f(27), MUTED, 'ma')
shadow_text(W//2, 1876, 'signed: HUMAN://ROOT / >_æ:', f(27), GREEN, 'ma')

im.save(OUT)
print(OUT, im.size, OUT.stat().st_size)
