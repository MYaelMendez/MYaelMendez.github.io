#!/usr/bin/env python3
"""
segment.py - Biblia del Oso (1569) OCR -> verse JSON (status 'ocr').

Locates a book/chapter in the archive.org djvu.txt OCR and splits it into
verses. The modernized SSE grid is used ONLY as a guide (verse counts,
boundaries, which OCR lines are body text vs. margin noise). No guide text is
ever written to the output: every character in `orig` comes from djvu.txt.

Usage:
  python3 pipeline/segment.py GEN 1 2        # chapters 1 and 2 of Genesis
  python3 pipeline/segment.py GEN 1 --debug  # print per-line decisions
"""
import argparse, json, os, re, sys, unicodedata
from difflib import SequenceMatcher
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DJVU = os.path.join(ROOT, "src", "djvu.txt")
GRID = os.path.join(ROOT, "src", "sse_grid", "spanish_sagradas_escrituras_1569_utf8.txt")
OCR_SRC = "archive.org/details/la-biblia-del-oso"

# Book config: OSIS code -> (grid book index, regex anchoring the book's title page in djvu.txt,
# regex anchoring the next book's start, used only to bound the search window)
BOOKS = {
    "GEN": ("01O", r"Primero Libro de Moy", r"Segundo Libro de Moy|EXODO|ÉXODO"),
}

HEADING_RE = re.compile(r"C\s?A\s?P\s?I\s?T")

# ---------------------------------------------------------------- normalize
def _fold(ch):
    """Map one char to a spelling-neutral skeleton (or '' to drop)."""
    d = unicodedata.normalize("NFD", ch)
    c = d[0].lower() if d else ""
    if not c.isalpha():
        return ""
    return {"ſ": "s", "f": "s", "v": "u", "y": "i", "z": "c", "ç": "c", "j": "x",
            "g": "x", "h": "", "b": "u", "w": "u", "q": "c", "k": "c", "ñ": "n"}.get(c, c)

def skeleton(s):
    """Return (normalized string, index map back into s). Doubled letters collapse."""
    out, idx = [], []
    for i, ch in enumerate(s):
        c = _fold(ch)
        if not c:
            continue
        if out and out[-1] == c:
            continue
        out.append(c); idx.append(i)
    return "".join(out), idx

# ---------------------------------------------------------------- inputs
def load_grid(book_idx):
    g = defaultdict(dict)
    with open(GRID, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 6 or p[0] != book_idx:
                continue
            txt = re.sub(r"<[^>]+>", "", p[5])
            g[int(p[1])][int(p[2])] = txt
    return g

def load_djvu():
    with open(DJVU, encoding="utf-8", errors="replace") as f:
        return f.read().split("\n")

# ---------------------------------------------------------------- alignment
K = 5  # n-gram size for anchoring

def build_index(s):
    ix = defaultdict(list)
    for i in range(len(s) - K + 1):
        ix[s[i:i + K]].append(i)
    return ix

def align_line(lnorm, gnorm, gix, prior):
    """Find where a normalized OCR line sits in the guide chapter.
    Returns (guide_start, guide_end, line_start, line_end, coverage) or None."""
    if len(lnorm) < K:
        return None
    votes = Counter()
    for i in range(len(lnorm) - K + 1):
        for gp in gix.get(lnorm[i:i + K], ()):
            votes[(gp - i) // 4] += 1
    if not votes:
        return None
    # Formulaic phrases ("y fue la tarde y la mañana") recur in many verses, so
    # among offsets with a strong vote pick the one nearest the reading position.
    top = max(votes.values())
    cands = [o * 4 for o, v in votes.items() if v >= max(2, 0.6 * top)] or [max(votes, key=votes.get) * 4]
    def cost(off):
        d = off - prior
        return d if d >= -40 else 10000 + abs(d)
    best = min(cands, key=cost)
    lo = max(0, best - 30); hi = min(len(gnorm), best + len(lnorm) + 30)
    sm = SequenceMatcher(None, gnorm[lo:hi], lnorm, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 3]
    if not blocks:
        return None
    matched = sum(b.size for b in blocks)
    ls, le = blocks[0].b, blocks[-1].b + blocks[-1].size
    gs, ge = lo + blocks[0].a, lo + blocks[-1].a + blocks[-1].size
    span = max(1, le - ls)
    return gs, ge, ls, le, matched / len(lnorm), matched / span, blocks, lo

# ---------------------------------------------------------------- cleaning
REF_TOKEN = re.compile(r"^[\*\(\[]?[A-Za-zÁÉÍÓÚáéíóúñ\.]{1,8}[\.,]?\s?\d+[\.,:;]\d+[\.,;+]*$")
PILCROW = re.compile(r"^(?:€\]?|4\]|G\||q\]|¶|\(\]|y\])\s+")
VERSE_NUM = re.compile(r"^[\W_]{0,3}(\d{1,2})[\.\s]+")

def trim_to_word_bounds(line, a, b):
    """Expand [a,b) in original line to whole words."""
    while a > 0 and not line[a - 1].isspace():
        a -= 1
    while b < len(line) and not line[b].isspace():
        b += 1
    return line[a:b].strip()

def clean_fragment(t):
    t = re.sub(r"\s+", " ", t).strip()
    # drop trailing marginal reference tokens like '*P/136 7.' or 'Ter.2)%'
    toks = t.split(" ")
    while toks and (REF_TOKEN.match(toks[-1]) or re.fullmatch(r"[\W\d_]+", toks[-1]) and toks[-1] not in (".", ":", ",", ";", "?")):
        toks.pop()
    while toks and (REF_TOKEN.match(toks[0]) or re.fullmatch(r"[\W_]+", toks[0]) and toks[0] not in ("¶",)):
        toks.pop(0)
    return " ".join(toks)

def join_lines(frags):
    out = ""
    for f in frags:
        if not out:
            out = f
        elif re.search(r"[-=—]$", out):
            out = re.sub(r"[-=—]$", "", out) + f
        else:
            out += " " + f
    return out

# ---------------------------------------------------------------- chapter location
def chapter_windows(lines, book, grid, want):
    _, start_re, end_re = BOOKS[book]
    b0 = next(i for i, l in enumerate(lines) if re.search(start_re, l))
    b1 = next((i for i, l in enumerate(lines[b0 + 50:], b0 + 50) if re.search(end_re, l)), len(lines))
    heads = [i for i in range(b0, b1) if HEADING_RE.search(lines[i])]
    def score(h, ch):
        if ch not in grid:
            return 0
        g = skeleton(" ".join(grid[ch][v] for v in sorted(grid[ch])[:4]))[0]
        gix = build_index(g)
        hits = 0
        for l in lines[h:h + 60]:
            n = skeleton(l)[0]
            hits += sum(1 for i in range(len(n) - K + 1) if n[i:i + K] in gix)
        return hits
    wins = {}
    for ch in want:
        h = max(heads, key=lambda h: score(h, ch))
        nxt = [x for x in heads if x > h]
        # end = the heading that best matches the next chapter, else +600 lines
        if ch + 1 in grid and nxt:
            e = max(nxt[:6], key=lambda x: score(x, ch + 1))
        else:
            e = min(h + 600, b1)
        wins[ch] = (h, e)
    return wins

# ---------------------------------------------------------------- segmentation
def local_align(raw, gv):
    """Align one OCR line against ONE guide verse skeleton.
    Returns dict(cov, matched, gs, ge, a, b) where [a,b) is the kept span of raw."""
    lnorm, imap = skeleton(raw)
    if len(lnorm) < 3 or not gv:
        return None
    sm = SequenceMatcher(None, gv, lnorm, autojunk=False)
    blocks = [x for x in sm.get_matching_blocks() if x.size >= 3]
    if not blocks:
        return None
    # keep the densest run of blocks (drop stray blocks far from the main run)
    runs, cur = [], [blocks[0]]
    for x in blocks[1:]:
        if x.b - (cur[-1].b + cur[-1].size) <= 8:
            cur.append(x)
        else:
            runs.append(cur); cur = [x]
    runs.append(cur)
    run = max(runs, key=lambda r: sum(x.size for x in r))
    matched = sum(x.size for x in run)
    ls, le = run[0].b, run[-1].b + run[-1].size
    return {"cov": matched / len(lnorm), "matched": matched,
            "gs": run[0].a, "ge": run[-1].a + run[-1].size,
            "a": imap[ls], "b": imap[le - 1] + 1, "len": len(lnorm)}

def num_tokens(raw):
    """Integers among the first 4 tokens of a line (verse numbers may follow a margin ref)."""
    out = []
    for i, tok in enumerate(raw.split()[:4]):
        m = re.fullmatch(r"[^\d\s]{0,2}(\d{1,2})[\.,]?", tok)
        if m:
            out.append((int(m.group(1)), i))
    return out

def start_similarity(raw, gv, after_tok=0):
    toks = raw.split()
    text = " ".join(toks[after_tok + 1:]) if after_tok is not None else raw
    n = skeleton(text)[0][:25]
    if len(n) < 6:
        return 0.0
    return SequenceMatcher(None, gv[:len(n) + 5], n, autojunk=False).ratio()

def segment_chapter(lines, h, e, gverses, book, ch, debug=False):
    vnums = sorted(gverses)
    gv = {v: skeleton(gverses[v])[0] for v in vnums}
    body = [i for i in range(h + 1, e) if lines[i].strip()]
    notes = defaultdict(list)

    # Phase 1: find the line that opens each verse (printed number + matching incipit)
    start = {}
    cursor = 0
    for v in vnums:
        best = None
        for j in range(cursor, min(len(body), cursor + 45)):
            raw = lines[body[j]]
            if v == 1:
                sim = start_similarity(raw, gv[v], None)
                al = local_align(raw, gv[v])
                if al and al["cov"] >= 0.6 and al["gs"] < 15 and al["matched"] >= 8:
                    best = (j, None, 1.0, 1.0); break
                continue
            for n, ti in num_tokens(raw):
                exact = n == v
                conf = (not exact) and n % 10 == v % 10 and abs(n - v) == 10
                if exact or conf:
                    sim = start_similarity(raw, gv[v], ti)
                    sc = sim + (0.3 if exact else 0)
                    if sim >= 0.45 and (best is None or sc > best[3]):
                        best = (j, (n, ti), sim, sc)
            if best and best[1][0] == v and best[2] >= 0.5:
                break
        if best:
            start[v] = best
            cursor = best[0] + 1
            if best[1] and best[1][0] != v:
                notes[v].append(f"printed verse number OCR'd as '{best[1][0]}'")
    # fallback A: incipit match (whole line or mid-line), between neighbours' starts
    cut = {}
    for v in vnums:
        if v in start:
            continue
        lo = max([start[u][0] + 1 for u in start if u < v] or [0])
        hi = min([start[u][0] for u in start if u > v] or [len(body)])
        cand = None
        for j in range(lo, hi):
            raw = lines[body[j]]
            sim = start_similarity(raw, gv[v], None)
            if sim >= 0.7 and (cand is None or sim > cand[2]):
                cand = (j, None, sim, sim); ccut = 0
            al = local_align(raw, gv[v][:30])
            if al and al["gs"] <= 3 and al["matched"] >= 12 and al["a"] > 0 and (cand is None or 0.69 > cand[2]):
                a = al["a"]
                # back up over a printed number / pilcrow / callout just before the incipit
                mm = re.search(r"(?:\S{0,3}\s+)?(?:[€¶+*»]\s*)+$|\d{1,2}\s*$", raw[:a])
                if mm: a = mm.start()
                while a > 0 and not raw[a - 1].isspace(): a -= 1
                cand = (j, None, 0.69, 0.69); ccut = a
        if cand:
            start[v] = cand
            if ccut:
                cut[v] = ccut
                notes[v].append(f"verse begins mid-line (djvu line {body[cand[0]]+1}); split by alignment, printed number not recognized")
            else:
                notes[v].append("printed verse number not recognized in OCR; start found by incipit match")
    # fallback B: opener printed out of reading order (column interleave)
    displaced = {}
    used = {start[v][0] for v in start}
    for v in vnums:
        if v in start or v == 1:
            continue
        for j, ln in enumerate(body):
            if j in used:
                continue
            raw = lines[ln]
            for n, ti in num_tokens(raw):
                if n == v and ti == 0 and start_similarity(raw, gv[v], ti) >= 0.6:
                    displaced[v] = j
                    break
            if v in displaced:
                notes[v].append(f"opening line (djvu line {ln+1}) found out of reading order (column interleave); reattached")
                break
    # Phase 2: assign lines in each span, filter margin noise by local alignment
    frags = defaultdict(list)
    order = sorted(start, key=lambda v: (start[v][0], cut.get(v, 0)))
    # lines whose tail opens the next verse: give the head to the span that owns the line
    for v, c in cut.items():
        j = start[v][0]
        head = lines[body[j]][:c]
        prev = [u for u in order if start[u][0] <= j and u < v]
        if prev and head.strip():
            pv = prev[-1]
            span_vs = [u for u in vnums if pv <= u < v]
            u, al = max(((u, local_align(head, gv[u])) for u in span_vs), key=lambda x: x[1]["matched"] if x[1] else 0)
            if al and al["matched"] >= 4:
                txt = clean_fragment(trim_to_word_bounds(head, al["a"], al["b"]))
                if txt:
                    frags[u].append((al["gs"], body[j], txt, False))
    def sandwiched(j, j0, j1, raw, v):
        """A body-looking line between two lines that align to the same verse."""
        if not (j0 < j < j1 - 1) or len(raw.strip()) < 25:
            return False
        letters = sum(c.isalpha() for c in raw); 
        if letters / max(1, len(raw.strip())) < 0.7 or REF_TOKEN.match(raw.split()[0]):
            return False
        def ok(k):
            a = local_align(lines[body[k]], gv[v]); return keep(a)
        return ok(j - 1) and ok(j + 1)
    def keep(al):
        return al and al["matched"] >= 5 and (al["cov"] >= 0.5 or al["matched"] >= 15)
    for k, v in enumerate(order):
        j0 = start[v][0]
        j1 = start[order[k + 1]][0] if k + 1 < len(order) else len(body)
        # missing verses between v and next start share this span
        span_vs = [u for u in vnums if v <= u < (order[k + 1] if k + 1 < len(order) else 10**6)]
        for j in range(j0, j1):
            if j in displaced.values():
                continue
            ln = body[j]; raw = lines[ln]
            nxt = order[k + 1] if k + 1 < len(order) else None
            if j == j0 and v in cut:
                raw = raw[cut[v]:]
            if nxt in cut and j == j1 - 1 + 0 and False:
                pass
            if j == j0 and start[v][1]:
                ti = start[v][1][1]
                raw_use = " ".join(raw.split()[ti + 1:])
            else:
                raw_use = raw
            scored = [(u, local_align(raw_use, gv[u])) for u in span_vs]
            u, al = max(scored, key=lambda x: (x[1]["matched"] if x[1] else 0))
            if j == j0:
                al = local_align(raw_use, gv[v]); u = v
                if al: al["a"] = 0 if start[v][1] else al["a"]
                if start[v][1] and al and al["matched"] >= 4:
                    al["keep"] = True   # opener validated by printed number + incipit
            if al and al.get("keep"):
                pass
            elif not keep(al) and sandwiched(j, j0, j1, raw_use, v):
                al = {"gs": 10**5 + j, "a": 0, "b": len(raw_use), "matched": 0, "cov": 0}
                u = v
                notes[v].append(f"djvu line {ln+1} kept by context (between body lines of this verse) though the guide did not match it; check for margin text")
            elif not keep(al):
                # displaced line? (column interleave) test against every verse
                best = None
                cands = []
                for w in vnums:
                    a2 = local_align(raw_use, gv[w])
                    if a2:
                        cands.append((a2["matched"], w, a2))
                cands.sort(key=lambda x: -x[0])
                if cands and cands[0][0] >= 18 and cands[0][2]["cov"] >= 0.7 and \
                        (len(cands) == 1 or cands[0][0] - cands[1][0] >= 6):
                    best = (cands[0][1], cands[0][2])
                if best:
                    u, al = best
                    notes[u].append(f"djvu line {ln+1} found out of reading order (column interleave) and reattached by alignment")
                else:
                    if debug: print(f"  DROP {ln+1} [{v}]: {raw!r}")
                    continue
            txt = clean_fragment(trim_to_word_bounds(raw_use, al["a"], al["b"]))
            if not txt:
                continue
            frags[u].append((al["gs"], ln, txt, j == j0 and u == v))
            if debug: print(f"  KEEP {ln+1} -> v{u} cov={al['cov']:.2f}: {txt!r}")

    for v, j in displaced.items():
        raw = lines[body[j]]
        al = local_align(raw, gv[v])
        if al:
            txt = clean_fragment(trim_to_word_bounds(raw, 0, al["b"]))
            frags[v].append((-1, body[j], txt, True))
    out = []
    for v in vnums:
        fl = frags.get(v, [])
        nts = list(dict.fromkeys(notes.get(v, [])))
        orig = None
        lines_used = []
        if fl:
            # opener first, then OCR order; a reattached displaced line goes by alignment position
            opener = [f for f in fl if f[3]]
            rest = sorted([f for f in fl if not f[3]], key=lambda f: (f[0] if any("reattached" in n and str(f[1]+1) in n for n in nts) else -1, f[1]))
            rest = sorted(rest, key=lambda f: f[0]) if any("reattached" in n for n in nts) else sorted(rest, key=lambda f: f[1])
            seq = opener + rest
            texts = [f[2] for f in seq]
            lines_used = sorted(set(f[1] for f in fl))
            t0 = texts[0]
            m = VERSE_NUM.match(t0)
            if m and int(m.group(1)) in (v, v % 10 + 30, v % 10 + 10, v % 10 + 20):
                t0 = t0[m.end():]
            if PILCROW.match(t0):
                t0 = "¶ " + PILCROW.sub("", t0)
            t0 = re.sub(r"^\*\s*", "", t0)
            texts[0] = t0
            orig = re.sub(r"\s+", " ", join_lines(texts)).strip()
            gl = len(gv[v]); ol = len(skeleton(orig)[0])
            if gl and ol / gl < 0.8:
                nts.append(f"possibly incomplete: OCR text is {ol/gl:.0%} of expected length")
            elif gl and ol / gl > 1.25:
                nts.append(f"possibly contains margin noise: OCR text is {ol/gl:.0%} of expected length")
            if v == 1:
                nts.append("verse 1 opens with a woodcut initial; the initial letter is lost/garbled in OCR")
            if v not in start and v not in displaced:
                nts.append("opening line not identified (printed number not recognized); text assigned to this verse by alignment")
        else:
            nts.append("verse not found in OCR")
        if lines_used:
            nts.append(f"djvu.txt lines {lines_used[0]+1}-{lines_used[-1]+1}")
        out.append({
            "id": f"oso1569:{book}.{ch}.{v}",
            "book": book, "chapter": ch, "verse": v,
            "orig": orig, "norm": None,
            "page": {"scan": OCR_SRC, "leaf": None, "bbox": None},
            "status": "ocr",
            "evidence": {"ocr_src": OCR_SRC, "corrected_by": None, "verified_by": None, "sha256": None},
            "notes": nts,
        })
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book"); ap.add_argument("chapters", nargs="+", type=int)
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "v"))
    a = ap.parse_args()
    book = a.book.upper()
    grid = load_grid(BOOKS[book][0])
    lines = load_djvu()
    wins = chapter_windows(lines, book, grid, a.chapters)
    for ch in a.chapters:
        h, e = wins[ch]
        print(f"{book} {ch}: djvu lines {h+1}-{e} (heading: {lines[h].strip()!r})", file=sys.stderr)
        vs = segment_chapter(lines, h, e, grid[ch], book, ch, a.debug)
        os.makedirs(os.path.join(a.out, book), exist_ok=True)
        p = os.path.join(a.out, book, f"{ch}.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(vs, f, ensure_ascii=False, indent=2)
        found = sum(1 for v in vs if v["orig"])
        print(f"  wrote {p}: {found}/{len(vs)} verses with text", file=sys.stderr)

if __name__ == "__main__":
    main()
