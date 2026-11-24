#!/usr/bin/env python3
"""Render the legible 9:16 OpenSourceWare retrospective (v2)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

W, H = 1080, 1920
OUT = Path('/opt/data/MYaelMendez-work/artifacts/history-retrospective-916-v2.png')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'

VOID = (5, 6, 7)
INK = (232, 244, 236)
MUTED = (150, 168, 158)
GREEN = (0, 255, 159)
CYAN = (0, 204, 255)
GOLD = (212, 175, 55)
MAGENTA = (255, 0, 255)
RED = (255, 59, 92)

im = Image.new('RGB', (W, H), VOID)
d = ImageDraw.Draw(im)

def f(size):
    return ImageFont.truetype(FONT, size)

def glow_text(x, y, text, font, fill, glow=None, anchor='la'):
    glow = glow or fill
    for dx in (-2, -1, 0, 1, 2):
        for dy in (-2, -1, 0, 1, 2):
            if dx or dy:
                d.text((x + dx * 2, y + dy * 2), text, font=font, fill=glow, alpha=45, anchor=anchor)
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)

def line(x1, y1, x2, y2, color, width=1, alpha=255):
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.line((x1, y1, x2, y2), fill=color + (alpha,), width=width)
    im.paste(Image.alpha_composite(im.convert('RGBA'), overlay).convert('RGB'), (0, 0))
    # redraw object after composite
    return ImageDraw.Draw(im)

def wrap(text, font, max_width):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if d.textlength(test, font=font) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(x, y, text, font, fill, max_width, lh, bullet=None):
    lines = wrap(text, font, max_width)
    for ln in lines:
        if bullet:
            d.ellipse((x, y + 12, x + 7, y + 19), fill=GREEN)
            d.text((x + 20, y), ln, font=font, fill=fill)
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

# background grid + scanlines + border
for yy in range(44, H - 44, 44):
    line(34, yy, W - 34, yy, GREEN, 1, 12)
for xx in range(34, W - 34, 44):
    line(xx, 44, xx, H - 44, CYAN, 1, 8)
for yy in range(0, H, 3):
    d.line((0, yy, W, yy), fill=(0, 0, 0), width=1)
line(28, 38, W - 28, 38, GREEN, 2, 90)
line(28, H - 38, W - 28, H - 38, GREEN, 2, 90)
line(28, 38, 28, H - 38, GREEN, 2, 90)
line(W - 28, 38, W - 28, H - 38, GREEN, 2, 90)

# header
glow_text(540, 78, 'OPENSOURCEWARE / INTERNET OF AGENTS', f(30), CYAN, anchor='ma')
glow_text(540, 124, 'OUR ENTIRE HISTORY', f(78), GOLD, anchor='ma')
glow_text(540, 224, 'three movements · one authority chain', f(34), MUTED, anchor='ma')
line(120, 272, W - 120, 272, GOLD, 2, 110)

acts = [
    ('01', 'ORIGIN / AUTHORITY', CYAN, [
        'The stack began with identity and authority: HUMAN://ROOT → æ → RECEIPT.',
        'OpenSourceWare is named; æ is executable authority, not decoration.',
        'Essence: authorized agency made visible.',
        'Ambient engineering: human intent → æ authority → ambient execution → public receipt → durable artifact.',
        'Domains: æl.net language · æ.store artifacts · æææ.com signal',
        'soværeign.com law · commandprompt.ai command · privateclient.ai approval',
        'mobility.foundation body · myaelmendez.github.io proof',
    ]),
    ('02', 'MACHINES / HARNESSES', GREEN, [
        '18 plugins collapsed into hermes-ae: one ae tool, one hash-chained ledger.',
        'Mixture of Harnesses: voice · ffmpeg · control · physics · viewport · robot · publish · course · ledger',
        'Asimov Agent: URDF/MJCF/USD twin · DAO Brain · æ Policy · verbs · face states · viewport',
        'ffmpeg = deterministic production camera; WebGL = preview/control only.',
        'Pattern: capability → authority gate → execution → receipt → artifact → address',
    ]),
    ('03', 'VOICE / NOW', MAGENTA, [
        'tinyVOCA became tinyVOICE: F2 · M2 · ROBOT · SOVÆREIGN from the 35.4s reference.',
        'Broadcast timbre is default · tinyTELEPROMPTER · stick lessons · desktop dock · æ TV.',
        'VoxMel-0.3B + Vocos provisioned; bf16 pushed; Chinese synthesis blocked by 2.2 GiB RAM.',
        'Storage: 325 artifacts offloaded to GitHub · caches pruned · 3.4 GiB free.',
    ]),
]

y = 308
for num, title, color, bullets in acts:
    glow_text(70, y, num, f(42), color)
    glow_text(142, y + 8, title, f(38), INK)
    y += 76
    line(70, y, W - 70, y, color, 1, 90)
    y += 18
    for b in bullets:
        y = para(92, y, b, f(27), INK, 900, 42, bullet=True)
        y += 6
    y += 18

# doctrine
line(90, y, W - 90, y, GOLD, 2, 130)
y += 34
glow_text(540, y, 'THE DOCTRINE', f(44), GOLD, anchor='ma')
y += 74
glow_text(540, y, 'authorized agency made visible', f(42), INK, anchor='ma')
y += 78
glow_text(540, y, 'human = root · agents ask · you hold · receipts public', f(31), GREEN, anchor='ma')

# footer
line(70, H - 170, W - 70, H - 170, CYAN, 2, 110)
glow_text(540, H - 142, 'HUMAN://ROOT → æ → ae → RECEIPT', f(38), CYAN, anchor='ma')
glow_text(540, H - 82, '#opensourceware #internetofagents', f(28), MUTED, anchor='ma')
glow_text(540, H - 42, 'signed: HUMAN://ROOT / >_æ:', f(28), GREEN, anchor='ma')

# subtle vignette
vig = Image.new('L', (W, H), 0)
vd = ImageDraw.Draw(vig)
for i in range(90, 0, -1):
    a = int(10 * (1 - i / 90))
    vd.ellipse((-W//2 + i*4, -H//2 + i*7, W + W//2 - i*4, H + H//2 - i*7), fill=a)
vig = vig.filter(ImageFilter.GaussianBlur(24))
black = Image.new('RGB', (W, H), (0, 0, 0))
im = Image.composite(black, im, vig)
im.save(OUT)
print(OUT, im.size, OUT.stat().st_size)
