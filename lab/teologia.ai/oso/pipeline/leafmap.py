#!/usr/bin/env python3
"""
leafmap.py - Biblia del Oso (1569): character offset in src/djvu.txt -> facsimile leaf.

How the mapping works (stdlib only):
  archive.org publishes, for item 'la-biblia-del-oso',
    * _hocr_searchtext.txt.gz  : the OCR text, page after page
    * _hocr_pageindex.json.gz  : per leaf [start, end) char offsets into that searchtext
    * _page_numbers.json       : per leaf the printed page number, when detected
  djvu.txt and the searchtext contain the SAME OCR characters, differing only in whitespace
  (checked: 4,631,264 non-whitespace chars, identical). So a djvu offset is converted to
  "count of non-whitespace chars before it", which is then located in the searchtext and
  looked up in the page index.

  The result is cached in pipeline/leafmap.json (djvu char offset where each leaf starts),
  so normal use needs only that file.

Offsets are Python str (Unicode code point) offsets into djvu.txt read as UTF-8,
NOT byte offsets. Leaf numbers are archive.org's 0-based leafNum, which is what the
viewer's /page/n<leaf> URL uses.

Usage:
  from pipeline.leafmap import offset_to_leaf, leaf_url, offset_to_url
  python3 pipeline/leafmap.py 123456          # prints leaf, printed page, URL
  python3 pipeline/leafmap.py --build         # rebuild leafmap.json from src/
"""
import bisect, gzip, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
DJVU = os.path.join(SRC, "djvu.txt")
SEARCHTEXT = os.path.join(SRC, "La_Biblia_del_Oso_hocr_searchtext.txt.gz")
PAGEINDEX = os.path.join(SRC, "La_Biblia_del_Oso_hocr_pageindex.json.gz")
PAGENUMS = os.path.join(SRC, "La_Biblia_del_Oso_page_numbers.json")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leafmap.json")
ITEM = "la-biblia-del-oso"
VIEW = "https://archive.org/details/%s/page/n%d"

_ws = re.compile(r"\s")


def _nonws_prefix(text):
    """nonws[i] = number of non-whitespace chars in text[:i] (len(text)+1 entries)."""
    out = [0] * (len(text) + 1)
    n = 0
    for i, ch in enumerate(text):
        out[i] = n
        if not ch.isspace():
            n += 1
    out[len(text)] = n
    return out


def build():
    djvu = open(DJVU, encoding="utf-8").read()
    st = gzip.open(SEARCHTEXT).read().decode("utf-8")
    pi = json.load(gzip.open(PAGEINDEX))
    pn = json.load(open(PAGENUMS, encoding="utf-8"))["pages"]
    a, b = _ws.sub("", djvu), _ws.sub("", st)
    if a != b:
        raise SystemExit("djvu.txt and hocr searchtext differ beyond whitespace; mapping invalid")
    st_nw = _nonws_prefix(st)
    # non-ws count at which each leaf starts
    leaf_nw = [st_nw[s] for (s, e, _hs, _he) in pi]
    # invert: djvu offset where that non-ws count is reached
    dj_nw = _nonws_prefix(djvu)
    leaf_off = [bisect.bisect_left(dj_nw, k) for k in leaf_nw]
    printed = {p["leafNum"]: (p.get("pageNumber") or None) for p in pn}
    data = {
        "item": ITEM,
        "djvu_chars": len(djvu),
        "leaf_count": len(pi),
        "note": "leaf_start_offset[i] = first djvu.txt char offset (code points) on leaf i; "
                "empty leaves share the offset of the next leaf with text.",
        "leaf_start_offset": leaf_off,
        "printed_page": [printed.get(i) for i in range(len(pi))],
    }
    json.dump(data, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    return data


_DATA = None


def _data():
    global _DATA
    if _DATA is None:
        _DATA = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else build()
    return _DATA


def offset_to_leaf(offset):
    """djvu.txt char offset -> 0-based archive.org leaf number."""
    d = _data()
    if not 0 <= offset <= d["djvu_chars"]:
        raise ValueError("offset out of range")
    offs = d["leaf_start_offset"]
    # last leaf whose start <= offset (empty leaves collapse onto the next text leaf)
    return max(0, bisect.bisect_right(offs, offset) - 1)


def leaf_url(leaf):
    return VIEW % (ITEM, leaf)


def offset_to_url(offset):
    return leaf_url(offset_to_leaf(offset))


def printed_page(leaf):
    """Printed page/folio number archive.org detected for the leaf, or None."""
    return _data()["printed_page"][leaf]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        d = build()
        print("built", CACHE, d["leaf_count"], "leaves")
    else:
        for arg in sys.argv[1:]:
            o = int(arg)
            lf = offset_to_leaf(o)
            print(o, lf, printed_page(lf), leaf_url(lf))
