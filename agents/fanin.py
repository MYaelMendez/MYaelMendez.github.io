#!/usr/bin/env python3
"""fanin — N receipts → ONE truth, with a human authority boundary.

Link 11 of væult: the missing fan-in. Every other link produces evidence;
this one consumes it and emits a single, hash-chained verdict. It is READ-ONLY
over every source: no DB is written, no task is claimed, nothing is published.

    hermes      kanban-unified.json   (recomputed content hash)
    tiny        tiny.html RESULTS     (flaky/refused are findings, not passes)
    chain       væult_chain.verify    (a broken link blocks the truth)
    push        task_events kind=pushed (a push must be on record)

    PASS   only if every source is coherent AND no doctor is flaky/refused
    BLOCKED otherwise, with each reason named

    python fanin.py            -> write github-pages/truth.json
    python fanin.py --check    -> compare stored receipt with live state
    python fanin.py --selftest -> gate logic, no real sources touched
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
OUT = ROOT / "github-pages" / "truth.json"
HERMES_DB = Path(os.environ.get(
    "HERMES_KANBAN_DB",
    str(Path(os.environ.get("LOCALAPPDATA", Path.home())) / "hermes" / "kanban.db")))
SCHEMA = "ae/truth/1"
AUTHORITY = "HUMAN://ROOT"


def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return digest(p.read_bytes()) if p.exists() else ""


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def source(sid, path, sha256, ok, findings, meta=None) -> dict:
    return {"id": sid, "path": str(path), "sha256": sha256, "ok": bool(ok),
            "findings": list(findings), "meta": meta or {}}


# ── collectors ────────────────────────────────────────────────────────────────

def collect_unified() -> dict:
    p = ROOT / "github-pages" / "kanban-unified.json"
    if not p.exists():
        return source("unified", p, "", False, ["missing: kanban-unified.json"])
    d = json.loads(p.read_text(encoding="utf-8"))
    findings = []
    if d.get("schema") != "ae/kanban-unified/1":
        findings.append("schema mismatch")
    try:
        import kanban_unified
        recomputed = kanban_unified.content_hash(d["cards"], d["sources"])
        if recomputed != d.get("content_sha256"):
            findings.append(f"content hash drift {d.get('content_sha256', '')[:12]}")
    except Exception as e:
        findings.append(f"cannot recompute hash: {type(e).__name__}")
    return source("unified", p, sha_file(p), not findings, findings,
                  {"cards": len(d.get("cards", [])), "counts": d.get("counts", {})})


def collect_tiny() -> dict:
    p = ROOT / "github-pages" / "tiny.html"
    if not p.exists():
        return source("tiny", p, "", False, ["missing: tiny.html"])
    raw = p.read_text(encoding="utf-8")
    m = re.search(r"const RESULTS = (\[.*?\]);\s*\nconst FAMILY", raw, re.S)
    if not m:
        return source("tiny", p, sha_file(p), False, ["no measured RESULTS array"])
    results = json.loads(m.group(1))
    ok = sum(1 for r in results if r.get("ok") and not r.get("flaky"))
    flaky = sum(1 for r in results if r.get("flaky"))
    refused = sum(1 for r in results if not r.get("ok"))
    findings = []
    if flaky:
        findings.append(f"{flaky} doctor(s) flaky — interpreters disagree")
    if refused:
        findings.append(f"{refused} doctor(s) refused")
    return source("tiny", p, sha_file(p), not findings, findings,
                  {"total": len(results), "ok": ok, "flaky": flaky, "refused": refused})


def collect_chain() -> dict:
    try:
        mod = importlib.import_module("væult_chain")
        v = mod.verify_chain()
    except Exception as e:
        return source("chain", "væult_chain.py", "", False,
                      [f"chain verify failed: {type(e).__name__}: {e}"])
    findings = [] if v.get("healthy") else [f"broken links: {', '.join(v.get('broken', []))}"]
    return source("chain", "væult_chain.py", "", not findings, findings,
                  {"total": v.get("total"), "ok": v.get("ok")})


def collect_push() -> dict:
    if not HERMES_DB.exists():
        return source("push", HERMES_DB, "", False, ["missing: kanban.db"])
    con = sqlite3.connect(f"file:{HERMES_DB}?mode=ro", uri=True)
    try:
        n = con.execute("SELECT COUNT(*) FROM task_events WHERE kind='pushed'").fetchone()[0]
        row = con.execute(
            "SELECT payload, created_at FROM task_events WHERE kind='pushed' "
            "ORDER BY id DESC LIMIT 1").fetchone()
    finally:
        con.close()
    findings = [] if n else ["no push recorded on the board"]
    meta = {"pushes": n}
    if row:
        try:
            meta["latest_sha"] = json.loads(row[0]).get("sha", "")[:12]
        except Exception:
            meta["latest_sha"] = "?"
        meta["latest_at"] = row[1]
    return source("push", HERMES_DB, sha_file(HERMES_DB), not findings, findings, meta)


def collect() -> dict[str, dict]:
    return {"sources": [collect_unified(), collect_tiny(), collect_chain(), collect_push()]}


# ── the gate ──────────────────────────────────────────────────────────────────

def gate(collection: dict) -> dict:
    """Pure: same collection → same verdict. No clock, no I/O, no exceptions."""
    reasons = []
    required = {"unified", "tiny", "chain", "push"}
    present = {s.get("id") for s in collection.get("sources", [])}
    for rid in sorted(required - present):
        reasons.append(f"{rid}: missing source")
    for s in collection.get("sources", []):
        for f in s.get("findings", []):
            reasons.append(f"{s.get('id', '?')}: {f}")
        if not s.get("ok") and not s.get("findings"):
            reasons.append(f"{s.get('id', '?')}: source not ok")
    return {"verdict": "PASS" if not reasons else "BLOCKED", "reasons": reasons}


def receipt(collection: dict, verdict: dict) -> str:
    body = {
        "schema": SCHEMA,
        "verdict": verdict["verdict"],
        "reasons": verdict["reasons"],
        "sources": [{k: s.get(k) for k in ("id", "sha256", "ok", "findings", "meta")}
                    for s in collection.get("sources", [])],
    }
    return digest(canonical(body))


def build() -> dict:
    collection = collect()
    verdict = gate(collection)
    return {"schema": SCHEMA,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "verdict": verdict["verdict"], "reasons": verdict["reasons"],
            "sources": collection["sources"],
            "receipt_sha256": receipt(collection, verdict),
            "authority": AUTHORITY, "grants": False, "executed": False,
            "note": "A verified claim, not an authorization. Publication still "
                    "requires a human-approved kanban_push."}


def emit() -> dict:
    d = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(f"truth -> {OUT}  verdict={d['verdict']}  receipt={d['receipt_sha256'][:16]}")
    for r in d["reasons"]:
        print(f"  BLOCK {r}")
    if not d["reasons"]:
        print("  PASS all sources coherent")
    return d


def check() -> dict:
    if not OUT.exists():
        print("DRIFT: no truth.json — run fanin.py first")
        return {"ok": False, "reason": "missing"}
    old = json.loads(OUT.read_text(encoding="utf-8"))
    live = build()
    same = (old.get("receipt_sha256") == live["receipt_sha256"]
            and old.get("verdict") == live["verdict"])
    out = {"ok": same, "stored": old.get("receipt_sha256", "")[:16],
           "live": live["receipt_sha256"][:16], "verdict": live["verdict"],
           "reasons": live["reasons"]}
    print(f"{'OK' if same else 'DRIFT'} · stored {out['stored']} · live {out['live']} "
          f"· {live['verdict']}")
    for r in live["reasons"]:
        print(f"  {r}")
    return out


def selftest() -> dict:
    def s(sid, ok=True, findings=(), sha="a" * 64):
        return source(sid, f"/test/{sid}", sha, ok, findings)

    checks = []
    clean = {"sources": [s("unified"), s("tiny"), s("chain"), s("push")]}
    v = gate(clean)
    assert v["verdict"] == "PASS" and not v["reasons"], v
    checks.append("clean-PASS")
    r1 = receipt(clean, v)
    assert r1 == receipt(clean, gate(clean)), "receipt not deterministic"
    checks.append("receipt-deterministic")

    flaky = {"sources": [s("unified"), s("tiny", False, ["1 doctor(s) flaky"]),
                         s("chain"), s("push")]}
    v = gate(flaky)
    assert v["verdict"] == "BLOCKED" and any("flaky" in x for x in v["reasons"]), v
    checks.append("flaky-BLOCKED-named")

    stale = {"sources": [s("unified", False, ["content hash drift abc"]),
                         s("tiny"), s("chain"), s("push")]}
    v = gate(stale)
    assert v["verdict"] == "BLOCKED" and any("hash drift" in x for x in v["reasons"]), v
    checks.append("stale-BLOCKED-named")

    broken = {"sources": [s("unified"), s("tiny"), s("chain", False, ["broken links: x"]),
                          s("push")]}
    assert gate(broken)["verdict"] == "BLOCKED"
    checks.append("broken-chain-BLOCKED")

    nopush = {"sources": [s("unified"), s("tiny"), s("chain"),
                          s("push", False, ["no push recorded on the board"])]}
    assert gate(nopush)["verdict"] == "BLOCKED"
    checks.append("no-push-BLOCKED")

    missing = {"sources": [s("unified"), s("tiny")]}
    assert gate(missing)["verdict"] == "BLOCKED"
    checks.append("missing-source-BLOCKED")

    assert r1 != receipt(flaky, gate(flaky)), "receipt must change with verdict"
    checks.append("receipt-changes-on-BLOCKED")
    out = {"ok": True, "checks": checks}
    print(json.dumps(out, indent=1))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="fanin — N receipts → ONE truth")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    if a.check:
        return 0 if check()["ok"] else 2
    d = emit()
    return 0 if d["verdict"] == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
