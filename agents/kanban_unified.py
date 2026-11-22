#!/usr/bin/env python3
"""KÆNBÆN UNIFIED — four boards, one coherent view.

Reads every board on this host WITHOUT writing to any of them:

  hermes  C:/Users/yaelm/AppData/Local/hermes/kanban.db   (tasks — authority)
  waves   C:/æ/agents/kanban.db                            (fleet wave rail)
  tiny    C:/æ/github-pages/tiny.html                      (measured doctors)
  irl     C:/æ/github-pages/kanban-irl/board.json          (signed physical cards)

Every native state is mapped into ONE lane vocabulary:

  READY   actionable now
  WORK    in progress
  VERIFY  waiting on a gate / disagreement
  DONE    verified or completed
  BLOCKED refused, failed or held

A card keeps its native status verbatim beside the unified lane, so the mapping
is auditable and nothing is silently re-labelled. One source hash per input and
one content hash over cards+source hashes make drift detectable.

    python kanban_unified.py              # write JSON + HTML
    python kanban_unified.py --check      # compare content hash, write nothing
"""
from __future__ import annotations

import argparse
import hashlib
import html as htmllib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENTS = Path(__file__).resolve().parent
ROOT = AGENTS.parent
sys.path.insert(0, str(AGENTS))
sys.path.insert(0, str(ROOT / "tiny"))

HERMES_DB = Path(r"C:\Users\yaelm\AppData\Local\hermes\kanban.db")
WAVES_DB = AGENTS / "kanban.db"
TINY_HTML = ROOT / "github-pages" / "tiny.html"
IRL_JSON = ROOT / "github-pages" / "kanban-irl" / "board.json"
OUT_DIR = ROOT / "github-pages"
OUT_JSON = OUT_DIR / "kanban-unified.json"
OUT_HTML = OUT_DIR / "kanban-unified.html"
SCHEMA = "ae/kanban-unified/1"
LANES = ("READY", "WORK", "VERIFY", "DONE", "BLOCKED")


def esc(s) -> str:
    return htmllib.escape(str(s), quote=True)


def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return digest(p.read_bytes())


def card(uid, source, lane, native, title, detail, evidence) -> dict:
    return {"uid": uid, "source": source, "lane": lane, "native": native,
            "title": title, "detail": detail, "evidence": evidence}


def hermes_cards() -> list[dict]:
    if not HERMES_DB.exists():
        return []
    con = sqlite3.connect(f"file:{HERMES_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    rows = con.execute("SELECT id,title,status,assignee FROM tasks "
                       "WHERE status != 'archived'").fetchall()
    con.close()
    m = {"done": "DONE", "running": "WORK", "review": "VERIFY",
         "blocked": "BLOCKED", "scheduled": "BLOCKED", "ready": "READY",
         "triage": "READY", "todo": "READY"}
    return [card(f"hermes:{r['id']}", "hermes", m.get(r["status"], "READY"),
                 r["status"], r["title"], f"assignee: {r['assignee'] or '-'}",
                 r["id"]) for r in rows]


def wave_cards() -> list[dict]:
    if not WAVES_DB.exists():
        return []
    con = sqlite3.connect(f"file:{WAVES_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT w.name AS wave, w.status AS wstatus, t.task_name, t.status, "
        "t.agent, t.commit_sha FROM wave_tasks t JOIN waves w ON w.id=t.wave_id "
        "ORDER BY w.name, t.task_name").fetchall()
    con.close()
    m = {"complete": "DONE", "completed": "DONE", "pending": "READY",
         "claimed": "WORK", "running": "WORK", "failed": "BLOCKED"}
    return [card(f"wave:{r['wave']}:{r['task_name']}", "waves",
                 m.get(r["status"], "READY"), r["status"],
                 f"{r['wave']} · {r['task_name']}",
                 f"agent: {r['agent'] or '-'} · wave: {r['wstatus']}",
                 r["commit_sha"] or "-") for r in rows]


def tiny_cards() -> list[dict]:
    import tiny_family
    raw = TINY_HTML.read_text(encoding="utf-8")
    m = re.search(r"const RESULTS = (\[.*?\]);\s*\nconst FAMILY", raw, re.S)
    if not m:
        return []
    results = json.loads(m.group(1))
    out = []
    for i, (name, dom, role) in enumerate(tiny_family.FAMILY):
        r = results[i] if i < len(results) else {}
        if r.get("flaky"):
            lane, native = "VERIFY", "flaky"
        elif r.get("ok"):
            lane, native = "DONE", "ok"
        else:
            lane, native = "BLOCKED", "refused"
        reason = r.get("refusal") or r.get("check") or "doctor ok"
        out.append(card(f"tiny:{name}", "tiny", lane, native, name,
                        f"{dom} · {role}", reason[:110]))
    return out


def irl_cards() -> list[dict]:
    b = json.loads(IRL_JSON.read_text(encoding="utf-8"))
    m = {"claim": "READY", "build": "WORK", "dispatch": "WORK",
         "verify": "VERIFY", "audit": "VERIFY", "receipt": "DONE",
         "push": "DONE", "sync": "DONE"}
    return [card(f"irl:{c.get('verb')}:{c.get('id')}", "irl",
                 m.get(c.get("verb"), "READY"), c.get("verb", "-"),
                 c.get("name") or c.get("id") or "?",
                 f"addr: {c.get('addr', '-')}", c.get("sha", "-"))
            for c in b.get("cards", [])]


def collect() -> tuple[list[dict], dict]:
    groups = {"hermes": hermes_cards, "waves": wave_cards,
              "tiny": tiny_cards, "irl": irl_cards}
    cards, sources = [], {}
    paths = {"hermes": HERMES_DB, "waves": WAVES_DB,
             "tiny": TINY_HTML, "irl": IRL_JSON}
    for name, fn in groups.items():
        cs = fn()
        cards.extend(cs)
        p = paths[name]
        sources[name] = {"path": str(p), "sha256": sha_file(p) if p.exists() else None,
                         "cards": len(cs)}
    cards.sort(key=lambda c: (LANES.index(c["lane"]), c["source"], c["uid"]))
    return cards, sources


def content_hash(cards: list[dict], sources: dict) -> str:
    body = json.dumps({"cards": cards, "sources": sources}, sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return digest(body)


CSS = """
:root{--void:#050505;--gold:#D4AF37;--text:#e8e8e8;--mut:#a89e80;--line:rgba(212,175,55,.24);
--ready:#70dcff;--work:#ffd166;--verify:#bf5af2;--done:#39ff14;--blocked:#ff6b6b}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--void);color:var(--text);font-family:'JetBrains Mono',ui-monospace,monospace;min-height:100vh}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.5;
 background:repeating-linear-gradient(0deg,rgba(212,175,55,.03) 0 1px,transparent 1px 4px)}
.wrap{position:relative;z-index:1;max-width:1700px;margin:0 auto;padding:clamp(14px,2vw,28px)}
header{display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;align-items:flex-end;
 padding-bottom:15px;border-bottom:1px solid var(--line)}
.eyebrow{font-size:.62rem;letter-spacing:.4em;text-transform:uppercase;color:var(--gold)}
h1{font-family:Orbitron,sans-serif;font-weight:900;font-size:clamp(1.8rem,4vw,3rem);color:var(--gold);margin-top:8px}
.sub{font-size:.72rem;color:var(--mut);margin-top:9px;max-width:760px;line-height:1.6}
.filters{display:flex;gap:7px;flex-wrap:wrap;margin:16px 0}
button{font:inherit;font-size:.62rem;letter-spacing:.1em;color:var(--gold);background:rgba(0,0,0,.5);
 border:1px solid var(--line);border-radius:999px;padding:6px 12px;cursor:pointer}
button:hover,button.on{background:rgba(212,175,55,.16);color:#fff}
.board{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;align-items:start}
@media(max-width:1300px){.board{grid-template-columns:repeat(2,1fr)}}
@media(max-width:700px){.board{grid-template-columns:1fr}}
.lane{border:1px solid var(--line);border-radius:12px;background:rgba(9,8,4,.72);padding:11px;min-height:160px}
.lane header{display:flex;justify-content:space-between;align-items:center;border:0;border-bottom:1px dashed var(--line);
 padding:0 0 9px;margin-bottom:10px}
.lane h2{font-family:Orbitron,sans-serif;font-size:.68rem;letter-spacing:.16em;color:var(--c)}
.lane .cnt{font-family:Orbitron,sans-serif;font-size:1.15rem;font-weight:900;color:var(--c)}
.stack{display:flex;flex-direction:column;gap:7px;max-height:72vh;overflow:auto}
.card{border:1px solid var(--line);border-left:2px solid var(--sc);border-radius:7px;
 padding:8px 9px;background:rgba(0,0,0,.42)}
.card h3{font-size:.68rem;font-weight:400;color:var(--text);margin:3px 0;line-height:1.35;word-break:break-word}
.meta{display:flex;justify-content:space-between;font-size:.55rem;color:var(--mut);gap:6px}
.src{color:var(--sc);letter-spacing:.08em}
.det{font-size:.56rem;color:var(--mut);margin-top:4px;word-break:break-word;line-height:1.4}
footer{margin-top:20px;border-top:1px solid var(--line);padding-top:13px;font-size:.6rem;color:var(--mut);
 display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
code{color:#ffd966}
"""


def render(cards: list[dict], sources: dict, chash: str) -> str:
    counts = {l: sum(1 for c in cards if c["lane"] == l) for l in LANES}
    colours = {"READY": "var(--ready)", "WORK": "var(--work)", "VERIFY": "var(--verify)",
               "DONE": "var(--done)", "BLOCKED": "var(--blocked)"}
    srccol = {"hermes": "#D4AF37", "waves": "#e7ba59", "tiny": "#70dcff", "irl": "#ff8fab"}
    cols = []
    for lane in LANES:
        items = []
        for c in [x for x in cards if x["lane"] == lane]:
            items.append(
                f'<article class="card" data-source="{esc(c["source"])}" '
                f'style="--sc:{srccol.get(c["source"], "#D4AF37")}">'
                f'<div class="meta"><span class="src">{esc(c["source"].upper())}</span>'
                f'<span>{esc(c["native"])}</span></div>'
                f'<h3>{esc(c["title"])}</h3>'
                f'<div class="det">{esc(c["detail"])}</div>'
                f'<div class="meta"><span>{esc(c["uid"])}</span>'
                f'<span>{esc(c["evidence"])[:32]}</span></div></article>')
        cols.append(
            f'<section class="lane" style="--c:{colours[lane]}">'
            f'<header><h2>{lane}</h2><span class="cnt">{counts[lane]}</span></header>'
            f'<div class="stack">{"".join(items) or "<div class=det>sin tarjetas</div>"}</div></section>')
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    srcs = " · ".join(f"{n}:{d['cards']} <code>{d['sha256'][:10] if d['sha256'] else 'missing'}</code>"
                      for n, d in sources.items())
    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KÆNBÆN · unificado</title>
<meta name="description" content="{len(cards)} tarjetas de 4 tableros en una sola vista coherente: hermes, waves, tiny*, kanban IRL.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=JetBrains+Mono:wght@300;400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<header><div><div class="eyebrow">æ:// kænbæn · unificado</div><h1>un tablero</h1>
<p class="sub">Cuatro fuentes, un vocabulario de carriles. Hermes manda; waves, tiny* y el tablero IRL se proyectan en él. Estado nativo intacto en cada tarjeta.</p></div>
<div class="score" style="text-align:right"><span style="font-family:Orbitron;font-size:2.2rem;font-weight:900;color:var(--gold)">{len(cards)}</span><span style="display:block;font-size:.6rem;color:var(--mut);letter-spacing:.14em">TARJETAS · {len(sources)} FUENTES</span></div></header>
<div class="filters"><button class="on" data-f="all">TODAS</button>{''.join(f'<button data-f="{n}">{n.upper()}</button>' for n in sources)}</div>
<div class="board">{''.join(cols)}</div>
<footer><span>{srcs}</span><span>content <code>{chash[:16]}</code> · {esc(now)} · <a href="truth.json" style="color:var(--gold);text-decoration:none">truth.json →</a></span></footer>
</div><script>
document.querySelectorAll('button[data-f]').forEach(b=>b.onclick=()=>{{
  document.querySelectorAll('button[data-f]').forEach(x=>x.classList.toggle('on',x===b));
  document.querySelectorAll('.card').forEach(c=>c.style.display=(b.dataset.f==='all'||c.dataset.source===b.dataset.f)?'':'none');
}});
</script></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="KÆNBÆN UNIFIED — coherent view of all boards")
    ap.add_argument("--check", action="store_true", help="verify content hash, write nothing")
    a = ap.parse_args()
    cards, sources = collect()
    chash = content_hash(cards, sources)
    counts = {l: sum(1 for c in cards if c["lane"] == l) for l in LANES}
    if a.check:
        if not OUT_JSON.exists():
            print(f"DRIFT: no manifest at {OUT_JSON}")
            return 1
        old = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        same = old.get("content_sha256") == chash
        print(f"{'OK' if same else 'DRIFT'} · content {chash[:16]} · "
              f"manifest {old.get('content_sha256', '?')[:16]}")
        print("lanes: " + " ".join(f"{k}={counts[k]}" for k in LANES))
        return 0 if same else 2
    manifest = {"schema": SCHEMA, "generated_at": datetime.now(timezone.utc).isoformat(
        timespec="seconds"), "content_sha256": chash, "lanes": list(LANES),
        "counts": counts, "sources": sources, "cards": cards}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(manifest, ensure_ascii=False, indent=1,
                                   sort_keys=True) + "\n", encoding="utf-8")
    OUT_HTML.write_text(render(cards, sources, chash), encoding="utf-8")
    print(f"unified -> {OUT_JSON} · {OUT_HTML}")
    print(f"cards={len(cards)}  " + " ".join(f"{k}={counts[k]}" for k in LANES))
    print(f"content_sha256={chash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
