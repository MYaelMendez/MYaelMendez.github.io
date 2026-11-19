"""robot_face v2 — proportional, expressive, viseme-driven.

v1 used fixed pixel offsets, so on a 220px panel the eyes were 7% of the screen
and read as dots. Everything here is a FRACTION of the panel, so the face scales.

Adds: large capsule eyes with iris/pupil/catchlight, eased lids, brows with
state-driven tilt, and a mouth with CURVATURE (smile/frown) plus 8 visemes that
stay distinct at render size. Charge arc, scanlines, status dot.
"""
from PIL import Image, ImageDraw, ImageFilter

SS = 3

# viseme: (width_frac_of_mouth_box, height_frac, roundness, openness)
VISEMES = [
    (0.62, 0.05, 0.5, 0.0),   # 0 rest
    (0.55, 0.03, 0.5, 0.0),   # 1 M/B/P closed
    (0.52, 0.62, 0.8, 1.0),   # 2 A open tall
    (0.86, 0.26, 0.3, 0.5),   # 3 E wide
    (0.74, 0.12, 0.2, 0.2),   # 4 I narrow
    (0.34, 0.52, 1.0, 0.9),   # 5 O round
    (0.24, 0.34, 1.0, 0.7),   # 6 U small
    (0.66, 0.14, 0.3, 0.3),   # 7 F/V
]

# state -> (brow tilt, mouth curve, eye openness)
# curve: +1 smile, -1 frown, 0 flat
STATE_EXPR = {
    'IDLE':              (0.0,   0.0,  0.85),
    'LISTENING':         (0.35,  0.25, 1.0),
    'SPEAKING':          (0.05,  0.30, 1.0),
    'THINKING':          (0.55, -0.10, 0.75),
    'AWAITING_APPROVAL': (0.30,  0.0,  0.95),
    'APPROVED':          (0.45,  0.75, 1.0),
    'REFUSED':           (-0.85, -0.65, 0.70),
    'ERROR':             (-0.60, -0.80, 0.55),
}


def _rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=max(0, r), fill=fill, outline=outline, width=width)


def _mouth(d, cx, cy, mw, mh, curve, rgb, rnd, openness):
    """A mouth with curvature. curve +1 smile .. -1 frown."""
    if abs(curve) < 0.12 or openness > 0.45:
        box = [cx - mw / 2, cy - mh / 2, cx + mw / 2, cy + mh / 2]
        _rr(d, box, int(mh / 2 * rnd), fill=rgb + (235,))
        if openness > 0.45 and mh > 6:
            ib = [box[0] + mw * 0.10, box[1] + mh * 0.16,
                  box[2] - mw * 0.10, box[3] - mh * 0.16]
            if ib[2] > ib[0] and ib[3] > ib[1]:
                _rr(d, ib, int(mh / 3 * rnd), fill=(5, 7, 9, 205))
        return
    # curved mouth: a thick arc drawn as a polyline
    n = 26
    pts = []
    for i in range(n + 1):
        t = i / n
        x = cx - mw / 2 + mw * t
        # parabola: smile dips at the centre when curve>0 (screen y grows down)
        y = cy + curve * mh * 0.9 * (1 - (2 * t - 1) ** 2)
        pts.append((x, y))
    d.line(pts, fill=rgb + (235,), width=max(2, int(mh * 0.55)), joint='curve')


def face(size, rgb, *, viseme=0, blink=0.0, gaze=(0.0, 0.0), charge=None,
         state='IDLE', glow=1.0, scan=True, curve=None, brow=None):
    W1, H1 = int(size[0]), int(size[1])
    w, h = W1 * SS, H1 * SS
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    pad = 0.02 * w
    bez = [pad, pad, w - pad, h - pad]
    _rr(d, bez, 0.09 * h, fill=(15, 16, 19, 244), outline=rgb + (255,),
        width=max(1, int(0.014 * h)))
    ins = 0.035 * w
    scr = [bez[0] + ins, bez[1] + ins, bez[2] - ins, bez[3] - ins]
    _rr(d, scr, 0.07 * h, fill=(5, 7, 9, 255))

    gl = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    _rr(ImageDraw.Draw(gl), scr, 0.07 * h, fill=rgb + (int(30 * glow),))
    img = Image.alpha_composite(img, gl.filter(ImageFilter.GaussianBlur(0.035 * h)))
    d = ImageDraw.Draw(img)

    if scan:
        step = max(2, int(0.018 * h))
        for yy in range(int(scr[1]), int(scr[3]), step):
            d.line([(scr[0], yy), (scr[2], yy)], fill=rgb + (12,), width=1)

    bt, mc, eo = STATE_EXPR.get(state, STATE_EXPR['IDLE'])
    if curve is None: curve = mc
    if brow is None: brow = bt

    cx, cy = w / 2, h / 2
    sw, sh = scr[2] - scr[0], scr[3] - scr[1]

    # EYES — large: each ~24% of screen width
    ew, eh = 0.24 * sw, 0.26 * sh
    eye_y = cy - 0.13 * sh
    eye_dx = 0.20 * sw
    openh = max(0.02 * sh, eh * eo * (1 - 0.93 * blink))
    for sx in (-1, 1):
        ex = cx + sx * eye_dx
        box = [ex - ew / 2, eye_y - openh / 2, ex + ew / 2, eye_y + openh / 2]
        _rr(d, box, openh / 2, fill=rgb + (240,))
        if blink < 0.5 and openh > 0.06 * sh:
            gx = ex + gaze[0] * ew * 0.20
            gy = eye_y + gaze[1] * openh * 0.18
            pr = min(ew, openh) * 0.30
            d.ellipse([gx - pr, gy - pr, gx + pr, gy + pr], fill=(6, 8, 10, 235))
            hr = pr * 0.34
            hx, hy = gx - pr * 0.34, gy - pr * 0.36
            d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(255, 255, 255, 210))

    # BROWS
    for sx in (-1, 1):
        bx = cx + sx * eye_dx
        by = eye_y - eh * 0.85 - brow * 0.02 * sh
        tilt = brow * 0.05 * sh * sx * (-1 if state == 'REFUSED' else 1)
        d.line([(bx - ew * 0.46, by + tilt), (bx + ew * 0.46, by - tilt)],
               fill=rgb + (175,), width=max(2, int(0.022 * sh)))

    # MOUTH — large: ~46% of screen width
    wf, hf, rnd, op = VISEMES[max(0, min(7, int(viseme)))]
    mw = 0.46 * sw * wf
    mh = max(0.022 * sh, 0.30 * sh * hf)
    _mouth(d, cx, cy + 0.22 * sh, mw, mh, curve, rgb, rnd, op)

    # CHARGE arc
    if charge is not None:
        c = max(0.0, min(1.0, charge))
        x0, x1 = scr[0] + 0.07 * sw, scr[2] - 0.07 * sw
        by = scr[3] - 0.055 * sh
        lw = max(2, int(0.022 * sh))
        d.line([(x0, by), (x1, by)], fill=rgb + (55,), width=lw)
        d.line([(x0, by), (x0 + (x1 - x0) * c, by)], fill=rgb + (225,), width=lw)

    r = 0.016 * sh
    dx, dy = scr[2] - 0.05 * sw, scr[1] + 0.05 * sh
    d.ellipse([dx - r, dy - r, dx + r, dy + r], fill=rgb + (210,))

    return img.resize((W1, H1), Image.LANCZOS)


def paste_face(base, centre, size, rgb, **kw):
    f = face(size, rgb, **kw)
    base.paste(f, (int(centre[0] - size[0] / 2), int(centre[1] - size[1] / 2)), f)
    return base
