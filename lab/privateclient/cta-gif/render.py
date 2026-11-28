#!/usr/bin/env python3
"""#startabusiness CTA GIFs · privateclient/default@1.0.0 card look, animated studio flow.
write → check → hold → ✓ approved → yellow "#startabusiness /" CTA with domain æsymov + æQR.
Author = LinkedIn page "#startabusiness LLM.STORE". LAB only. (Hark, 2026-10-19)
usage: python3 render.py <door> <W> <H> <outdir>"""
import sys, os, io, math, segno, cairosvg
from PIL import Image, ImageDraw, ImageFont

FPS = 15
N = 120  # 8.0 s
F = "/usr/share/fonts/truetype/dejavu/"
EMO = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
def font(kind, size):
    p = {"sans": "DejaVuSans.ttf", "sansb": "DejaVuSans-Bold.ttf", "mono": "DejaVuSansMono.ttf",
         "monob": "DejaVuSansMono-Bold.ttf"}[kind]
    return ImageFont.truetype(F + p, max(8, int(size)))
_emo = ImageFont.truetype(EMO, 109)
_ecache = {}
def emoji_img(ch, size):
    k = (ch, size)
    if k not in _ecache:
        im = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((0, 0), ch, font=_emo, embedded_color=True)
        im = im.crop(im.getbbox())
        r = size / max(im.size)
        _ecache[k] = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    return _ecache[k]
def is_emo(ch):
    o = ord(ch)
    return o >= 0x1F000 or ch in "✅✋✍⌨"
def runs(t):
    out = []
    for ch in t:
        if ch == "\ufe0f": continue
        e = is_emo(ch)
        if out and not e and not out[-1][0]: out[-1][1] += ch
        else: out.append([e, ch])
    return out
def text_w(t, f):
    w = 0
    for e, s in runs(t):
        w += f.size * 1.15 if e else f.getlength(s)
    return w
def draw_text(img, d, xy, t, f, fill, anchor="l"):
    """single-line text with color-emoji fallback; xy = (x, baseline-ish middle y)"""
    x, y = xy
    w = text_w(t, f)
    if anchor == "m": x -= w / 2
    elif anchor == "r": x -= w
    for e, s in runs(t):
        if e:
            em = emoji_img(s, int(f.size * 1.0))
            img.alpha_composite(em, (int(x + f.size * 0.07), int(y - em.height / 2)))
            x += f.size * 1.15
        else:
            d.text((x, y), s, font=f, fill=fill, anchor="lm")
            x += f.getlength(s)
    return w

# ---------- æsymov face (ae.face/0.2, lab/face/lang/pc-face.js) ----------
MOOD = {
 "ready":   ("M88 120H106M134 120H152", "M100 196Q120 206 140 196", None),
 "checking":("scan", "M104 198H136", None),
 "ok":      ("M88 126L97 114L106 126M134 126L143 114L152 126", "M96 192Q120 214 144 192", "#3ee08f"),
}
DOMAINS = {"cli.llc": ("#f97316", "$"), "daollc.ai": ("#c084fc", "◆"), "privateclient.ai": ("#00f3ff", None)}
PCCROWN = '<path d="M111 40L115.5 45L120 40M125 31V45" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
_fcache = {}
def face(domain, mood, size, scan=0.0):
    k = (domain, mood, size, round(scan, 2))
    if k in _fcache: return _fcache[k]
    c, g = DOMAINS[domain]
    eyes, mouth, tint = MOOD[mood]
    tint = tint or c
    if g:
        fs = 24 if len(g) > 2 else 28 if len(g) > 1 else 32
        crown = f'<text x="120" y="52" text-anchor="middle" font-family="DejaVu Sans Mono" font-weight="bold" font-size="{fs}" stroke="none">{g}</text>'
    else:
        crown = PCCROWN
    if eyes == "scan":
        ex = f'<rect x="{72 + 88 * scan:.1f}" y="98" width="8" height="44" rx="3" stroke="none"/><path d="M88 120H106M134 120H152" stroke-width="4" stroke-linecap="round" opacity=".35"/>'
    else:
        ex = f'<path d="{eyes}" fill="none" stroke-width="{5 if mood == "ready" else 4}" stroke-linecap="round" stroke-linejoin="round"/>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -10 280 280" width="{size}" height="{size}">
<defs><filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<path d="M52 78Q52 18 120 18Q188 18 188 78V176Q188 246 120 250Q52 246 52 176Z" fill="#141416" stroke="#3a3a3e" stroke-width="3"/>
<g fill="{c}" stroke="{c}">{crown}</g>
<rect x="66" y="92" width="108" height="56" rx="26" fill="#030a0b" stroke="{tint}" stroke-width="3"/>
<g fill="{tint}" stroke="{tint}" filter="url(#gl)">{ex}</g>
<path d="{mouth}" fill="none" stroke="{tint}" stroke-width="4" stroke-linecap="round"/>
<path d="M52 176Q60 232 120 240Q180 232 188 176" fill="none" stroke="#b87333" stroke-opacity=".6" stroke-width="2.5"/>
</svg>'''
    im = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")
    _fcache[k] = im
    return im

# ---------- page mark: yellow/blue/green æ stack ----------
def page_mark(size):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    s = size * 0.56; o = (size - s) / 2
    for i, col in enumerate(["#2bb673", "#2f6fe0", "#f5c400"]):
        dx = o + (1 - i) * size * 0.15
        d.rounded_rectangle([dx, dx, dx + s, dx + s], radius=size * 0.06, fill=col, outline="#111", width=max(2, size // 36))
    top = o - size * 0.15
    d.text((top + s / 2, top + s / 2 + size * 0.01), "æ", font=font("sansb", s * 0.72), fill="#111", anchor="mm")
    return im

def qr_img(url, px):
    q = segno.make(url, error="m")
    m = [list(r) for r in q.matrix]
    n = len(m); quiet = 2
    cell = px / (n + 2 * quiet)
    im = Image.new("RGB", (int(px), int(px)), "white"); d = ImageDraw.Draw(im)
    for i, r in enumerate(m):
        for j, v in enumerate(r):
            if v:
                x0 = (j + quiet) * cell; y0 = (i + quiet) * cell
                d.rectangle([round(x0), round(y0), round(x0 + cell) - 1, round(y0 + cell) - 1], fill="black")
    return im, q.version

THEMES = {
 "night": dict(bg="#000000", c="#00f3ff", ink="#e9f6f7", dim="#7d9a9e", grid=(0, 243, 255, 20), card="#06191b", bd="#1d4a4e", ok="#3ddc84", head="#ffffff"),
 "day":   dict(bg="#f4efe3", c="#00747c", ink="#161616", dim="#48443d", grid=(22, 22, 22, 22), card="#fffaf0", bd="#c9c0ad", ok="#1a7f45", head="#161616"),
}
DOORS = {
 "clillc": dict(domain="cli.llc", label="CLI.LLC", theme="night", rid="CLI-0001",
                head="Cli in, llc out.", sub="🌍 founders anywhere · LLC with doola",
                cta_sub="🌍 LLC with doola"),
 "daollc": dict(domain="daollc.ai", label="DAOLLC.AI", theme="day", rid="DAO-0001", dc_day="#7c3aed",
                head="DAO LLC ◆", sub="🤖 robot-assisted smart contracts",
                cta_sub="🤖 DAO LLC · smart contracts"),
}
URL = "https://privateclient.ai/startabusiness?door={}"
AUTHOR = "#startabusiness LLM.STORE"
YEL = "#f5c400"

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3

def build(door, W, H, outdir):
    D = DOORS[door]; T = THEMES[D["theme"]]; dom = D["domain"]; dc = DOMAINS[dom][0]
    url = URL.format(door)
    s = W / 1080
    tall = H / W > 1.1
    os.makedirs(outdir, exist_ok=True)
    # static background
    base = Image.new("RGBA", (W, H), T["bg"]); bd = ImageDraw.Draw(base)
    step = int(54 * s)
    for x in range(0, W + 1, step): bd.line([(x, 0), (x, H)], fill=T["grid"], width=1)
    for y in range(0, H + 1, step): bd.line([(0, y), (W, y)], fill=T["grid"], width=1)
    g = Image.new("RGBA", (W, H)); gd = ImageDraw.Draw(g)
    base = Image.alpha_composite(Image.new("RGBA", (W, H), T["bg"]), base)
    bd = ImageDraw.Draw(base)
    bd.rectangle([int(24 * s), int(24 * s), W - int(24 * s), H - int(24 * s)], outline=T["c"], width=max(3, int(3 * s)))
    # author row (LinkedIn page as author)
    av = int(84 * s); mx = int(64 * s)
    base.alpha_composite(page_mark(av), (mx, int(52 * s)))
    nf = font("sansb", 36 * s); tf = font("sans", 25 * s)
    draw_text(base, bd, (mx + av + int(20 * s), int(52 * s) + av * 0.33), AUTHOR, nf, T["ink"])
    draw_text(base, bd, (mx + av + int(20 * s), int(52 * s) + av * 0.78), "Now · 🌐 · ✓ human-reviewed", tf, T["dim"])
    qsm = int(132 * s)
    qsmall, qv = qr_img(url, qsm)
    qbig_px = int((300 if not tall else 290) * s)
    qbig, _ = qr_img(url, qbig_px)

    # geometry
    if tall:
        Y = dict(steps=205, face=245, fsz=390, head=735, sub=830, act=1020, foot=H / s - 62)
        C = dict(face=130, fsz=400, dom=590, sub=668, btn=715, btnh=116, qr=880, qlabel=1205)
    else:
        Y = dict(steps=190, face=215, fsz=300, head=585, sub=670, act=815, foot=H / s - 62)
        C = dict(face=125, fsz=340, dom=520, sub=596, row=660, btnh=116)
    Y = {k: v * s for k, v in Y.items()}; C = {k: v * s for k, v in C.items()}
    steps = [("✍️", "write"), ("✅", "check"), ("✋", "hold"), ("✓", "ok")]

    hf = font("sansb", 92 * s); sf = font("sans", 36 * s); mf = font("monob", 26 * s); sm = font("mono", 24 * s)
    frames = []
    for f in range(N):
        im = base.copy(); d = ImageDraw.Draw(im)
        cta = f >= 84
        # phase
        if f < 36: ph = 0
        elif f < 54: ph = 1
        elif f < 72: ph = 2
        else: ph = 3
        if not cta:
            # small æQR top-right (template position)
            qx = W - mx - qsm; qy = int(46 * s)
            d.rectangle([qx - 8 * s, qy - 8 * s, qx + qsm + 8 * s, qy + qsm + 8 * s], fill="white")
            im.paste(qsmall, (qx, qy))
            d.text((qx + qsm / 2, qy + qsm + 26 * s), "æQR", font=font("monob", 18 * s), fill=T["c"], anchor="mm")
            # steps indicator
            sw = 170 * s; sx0 = W / 2 - sw * 2
            for i, (ic, lb) in enumerate(steps):
                cx = sx0 + sw * i + sw / 2 - 8 * s; on = i == ph; done = i < ph
                col = T["c"] if on else (T["ok"] if done else T["dim"])
                if on:
                    d.rounded_rectangle([cx - 58 * s, Y["steps"] - 26 * s, cx + 74 * s, Y["steps"] + 26 * s], radius=26 * s, outline=T["c"], width=max(2, int(3 * s)))
                if ic == "✓":
                    d.text((cx - 22 * s, Y["steps"]), "✓", font=font("sansb", 30 * s), fill=col, anchor="mm")
                else:
                    draw_text(im, d, (cx - 22 * s, Y["steps"]), ic, font("sans", 26 * s), col, "m")
                d.text((cx + 6 * s, Y["steps"]), lb, font=font("mono", 20 * s), fill=col, anchor="lm")
                if i < 3: d.text((sx0 + sw * (i + 1), Y["steps"]), "›", font=font("monob", 26 * s), fill=T["dim"], anchor="mm")
            # face
            mood = "checking" if ph == 1 else ("ok" if ph == 3 else "ready")
            scan = 0.5 - 0.5 * math.cos((f - 36) / 9 * math.pi) if ph == 1 else 0
            fi = face(dom, mood, int(Y["fsz"]), scan)
            im.alpha_composite(fi, (int(W / 2 - fi.width / 2), int(Y["face"])))
            # headline typing
            full = D["head"]
            n = len(full) if f >= 28 else max(0, int((f - 4) / 24 * len(full) + 0.999)) if f >= 4 else 0
            shown = full[:n]
            fs = hf
            while text_w(full, fs) > W - 2 * mx - 40 * s: fs = font("sansb", fs.size - 4)
            wfull = text_w(full, fs); xl = W / 2 - wfull / 2
            draw_text(im, d, (xl, Y["head"]), shown, fs, T["head"])
            if ph == 0 and (f // 4) % 2 == 0:
                cx = xl + text_w(shown, fs) + 6 * s
                d.rectangle([cx, Y["head"] - fs.size * 0.45, cx + 6 * s, Y["head"] + fs.size * 0.45], fill=T["c"])
            # sub fades in
            if f >= 28:
                a = ease((f - 28) / 6)
                col = tuple(int(int(T["bg"][i:i + 2], 16) * (1 - a) + int(T["ink"][i:i + 2], 16) * a) for i in (1, 3, 5))
                draw_text(im, d, (W / 2, Y["sub"]), D["sub"], sf, col, "m")
            # action zone
            ay = Y["act"]
            if ph == 1:
                chips = ["✓ spelling", "✓ tone", "✓ rules"]
                cw = 230 * s; x0 = W / 2 - cw * 1.5
                for i, ch in enumerate(chips):
                    on = f >= 39 + i * 5
                    col = T["ok"] if on else T["dim"]
                    d.rounded_rectangle([x0 + cw * i + 10 * s, ay - 34 * s, x0 + cw * (i + 1) - 10 * s, ay + 34 * s], radius=34 * s, outline=col, width=max(2, int(3 * s)))
                    d.text((x0 + cw * i + cw / 2, ay), ch if on else "· " + ch[2:], font=mf, fill=col, anchor="mm")
            elif ph == 2:
                bw = 700 * s; bh = 96 * s; x0 = W / 2 - bw / 2
                p = ease((f - 54) / 14)
                d.rounded_rectangle([x0, ay - bh / 2, x0 + bw, ay + bh / 2], radius=bh / 2, outline=T["c"], width=max(3, int(3 * s)), fill=T["card"])
                if p > 0.02:
                    d.rounded_rectangle([x0, ay - bh / 2, x0 + bw * p, ay + bh / 2], radius=bh / 2, fill=T["ok"])
                draw_text(im, d, (W / 2, ay), "✋ Hold · I approve this message", font("sansb", 32 * s), T["ink"], "m")
                if p > 0.02:
                    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
                    draw_text(lay, ld, (W / 2, ay), "✋ Hold · I approve this message", font("sansb", 32 * s), "#ffffff", "m")
                    msk = Image.new("L", (W, H), 0); ImageDraw.Draw(msk).rectangle([0, 0, x0 + bw * p, H], fill=255)
                    lay.putalpha(Image.composite(lay.getchannel("A"), Image.new("L", (W, H), 0), msk))
                    im.alpha_composite(lay)
            elif ph == 3:
                k = ease((f - 72) / 4); sc = 1.35 - 0.35 * k
                st = Image.new("RGBA", (int(760 * s), int(150 * s)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
                sd.rounded_rectangle([20 * s, 20 * s, 740 * s, 130 * s], radius=18 * s, outline="#0a66c2", width=max(4, int(6 * s)))
                sfnt = font("sansb", 40 * s)
                tw = sfnt.getlength("I APPROVE THIS MESSAGE"); mw = 52 * s; x0 = 380 * s - (mw + 20 * s + tw) / 2
                pts = lambda P: [(x0 + px * 3.0 * s, 47 * s + py * 3.0 * s) for px, py in P]
                sd.line(pts([(3, 12), (7.5, 17), (12, 12)]), fill=T["c"], width=max(3, int(6 * s)), joint="curve")
                sd.line(pts([(17, 3), (17, 17)]), fill=T["c"], width=max(3, int(6 * s)))
                sd.text((x0 + mw + 20 * s, 75 * s), "I APPROVE THIS MESSAGE", font=sfnt, fill="#4c9be8" if D["theme"] == "night" else "#0a66c2", anchor="lm")
                st = st.rotate(2.9, resample=Image.BICUBIC, expand=True)
                st = st.resize((int(st.width * sc), int(st.height * sc)), Image.LANCZOS)
                if k < 1:
                    st.putalpha(st.getchannel("A").point(lambda v: int(v * k)))
                im.alpha_composite(st, (int(W / 2 - st.width / 2), int(ay - st.height / 2)))
            # receipt footer
            d.text((W / 2, Y["foot"]), f"🧾 {D['rid']} · privateclient.ai/startabusiness".replace("🧾 ", ""), font=sm, fill=T["dim"], anchor="mm")
        else:
            # CTA scene
            k = ease((f - 84) / 5)
            fi = face(dom, "ok", int(C["fsz"]))
            fy = C["face"] + (1 - k) * 30 * s
            im.alpha_composite(fi, (int(W / 2 - fi.width / 2), int(fy)))
            df = font("monob", 104 * s)
            d.text((W / 2, C["dom"]), D["label"], font=df, fill=(D.get("dc_day", dc) if D["theme"] == "day" else dc), anchor="mm")
            draw_text(im, d, (W / 2, C["sub"]), D["cta_sub"], font("sans", 38 * s), T["ink"], "m")
            bf = font("sansb", 50 * s)
            if tall:
                bw = 640 * s; bx = W / 2 - bw / 2; by = C["btn"]
                qx = int(W / 2 - qbig_px / 2); qy = int(C["qr"])
                lab_y = C["qlabel"]
            else:
                bw = 590 * s; bx = mx + 10 * s; by = C["row"] + (qbig_px - C["btnh"]) / 2
                qx = int(W - mx - 12 * s - qbig_px); qy = int(C["row"])
                lab_y = qy + qbig_px + 32 * s
            pulse = 1 + 0.025 * math.sin((f - 84) / 30 * 2 * math.pi * 2)
            bh = C["btnh"]; cxb = bx + bw / 2; cyb = by + bh / 2
            w2 = bw * pulse / 2; h2 = bh * pulse / 2
            d.rounded_rectangle([cxb - w2 + 6 * s, cyb - h2 + 8 * s, cxb + w2 + 6 * s, cyb + h2 + 8 * s], radius=18 * s, fill="#000000" if D["theme"] == "day" else "#3a3a3e")
            d.rounded_rectangle([cxb - w2, cyb - h2, cxb + w2, cyb + h2], radius=18 * s, fill=YEL, outline="#000", width=max(3, int(4 * s)))
            d.text((cxb, cyb), "#startabusiness /", font=bf, fill="#000", anchor="mm")
            if not tall:
                d.text((cxb, by + bh + 50 * s), "privateclient.ai/startabusiness", font=font("monob", 24 * s), fill=T["c"], anchor="mm")
                d.text((cxb, by + bh + 88 * s), "æQR →", font=font("mono", 24 * s), fill=T["dim"], anchor="mm")
            pad = int(12 * s)
            d.rectangle([qx - pad, qy - pad, qx + qbig_px + pad, qy + qbig_px + pad], fill="white", outline=T["c"], width=max(2, int(3 * s)))
            im.paste(qbig, (qx, qy))
            if tall: d.text((W / 2, lab_y), "privateclient.ai/startabusiness", font=font("monob", 24 * s), fill=T["c"], anchor="mm")
            d.text((W / 2, H - 62 * s), "✓ human-reviewed · " + D["rid"], font=sm, fill=T["dim"], anchor="mm")
            if k < 1:  # quick fade-in from the approved card
                prev = frames[83]
                im = Image.blend(prev, im, k)
            if f >= 114:  # crossfade back to frame 0 for a clean loop
                a = ease((f - 114) / 5)
                im = Image.blend(im, frames[0], a)
        frames.append(im)
    for i, im in enumerate(frames):
        im.convert("RGB").save(f"{outdir}/f{i:04d}.png")
    return url, qv

if __name__ == "__main__":
    door, W, H, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    print(build(door, W, H, out))
