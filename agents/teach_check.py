#!/usr/bin/env python3
"""
teach_check.py — is every agent actually taught to use the chain?

TEACHING IS NOT A SKILL FILE
----------------------------
A skill only loads when its trigger matches. That is not teaching — it is
documentation that hopes to be found. A fleet learns through surfaces it is
FORCED to read:

    1. AGENTS.md              auto-loaded into every agent in C:\\æ
    2. kænbæn system-map      "every agent reads this before acting"
    3. capability-contracts   "what each agent can do — read before dispatching"

If the chain is not in those three, an agent can work a whole session without
knowing it exists. This script checks that it IS, and reports exactly which
surface has drifted.

It also checks the inverse: that the surfaces do not point at things that no
longer exist. A stale instruction is worse than a missing one — it sends an
agent confidently to a dead end.

USAGE
    python teach_check.py            check every surface, exit 1 if any is stale
    python teach_check.py --json     machine-readable
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

BASE = pathlib.Path(os.environ.get("AE_BASE", r"C:\æ"))
AGENTS_MD = BASE / "AGENTS.md"
K_BASE = pathlib.Path(os.environ.get("KAENBAEN_BASE", str(BASE / "kænbæn")))
SYS_MAP = K_BASE / "system-map.json"
CONTRACTS = K_BASE / "capability-contracts.json"

# What a taught agent must be able to find, and where it must be findable.
REQUIRED_TERMS = {
    "AGENTS.md": ["væult", "væult://chain", "kanban_push.py", "agent_pledge.py"],
    "system-map": ["vaeult-chain"],
    "capability-contracts": ["vaeult_chain"],
}


def _read_text(p: pathlib.Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def _read_json(p: pathlib.Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def check() -> dict:
    results = []

    # 1. AGENTS.md — the highest-reach surface
    md = _read_text(AGENTS_MD)
    missing = [t for t in REQUIRED_TERMS["AGENTS.md"] if t not in md]
    results.append({
        "surface": "AGENTS.md", "path": str(AGENTS_MD),
        "exists": AGENTS_MD.exists(), "reach": "every agent in C:\\æ (auto-loaded)",
        "required": REQUIRED_TERMS["AGENTS.md"], "missing": missing,
        "ok": AGENTS_MD.exists() and not missing,
    })

    # 2. system-map — "every agent reads this before acting"
    smap = _read_json(SYS_MAP)
    surfaces = smap.get("surfaces", {})
    missing = [t for t in REQUIRED_TERMS["system-map"] if t not in surfaces]
    results.append({
        "surface": "kænbæn system-map", "path": str(SYS_MAP),
        "exists": SYS_MAP.exists(), "reach": "every agent reads this before acting",
        "required": REQUIRED_TERMS["system-map"], "missing": missing,
        "ok": SYS_MAP.exists() and not missing,
    })

    # 3. capability-contracts — what each agent can do
    con = _read_json(CONTRACTS)
    agents = con.get("agents", {})
    missing = [t for t in REQUIRED_TERMS["capability-contracts"] if t not in agents]
    results.append({
        "surface": "capability-contracts", "path": str(CONTRACTS),
        "exists": CONTRACTS.exists(), "reach": "read before dispatching",
        "required": REQUIRED_TERMS["capability-contracts"], "missing": missing,
        "ok": CONTRACTS.exists() and not missing,
    })

    # 4. INVERSE CHECK — do the surfaces point at files that exist?
    # A stale instruction is worse than a missing one.
    dead = []
    chain = BASE / "agents" / "væult_chain.py"
    if "væult_chain.py" in md and not chain.exists():
        dead.append({"referenced": str(chain), "in": "AGENTS.md"})
    for name, rel in (("kanban_push.py", "agents/kanban_push.py"),
                      ("agent_pledge.py", "agents/agent_pledge.py")):
        if name in md and not (BASE / rel).exists():
            dead.append({"referenced": str(BASE / rel), "in": "AGENTS.md"})
    if "vaeult-chain" in surfaces:
        m = surfaces["vaeult-chain"].get("cli", "")
        p = m.split("python", 1)[-1].strip() if "python" in m else ""
        if p and not pathlib.Path(p).exists():
            dead.append({"referenced": p, "in": "system-map"})
    results.append({
        "surface": "pointers resolve", "path": "-",
        "exists": True, "reach": "a stale instruction sends an agent to a dead end",
        "required": ["every referenced path exists"], "missing": [d["referenced"] for d in dead],
        "ok": not dead, "dead": dead,
    })

    ok = all(r["ok"] for r in results)
    return {"ok": ok, "surfaces": results,
            "taught": sum(1 for r in results if r["ok"]), "total": len(results)}


def main(argv):
    ap = argparse.ArgumentParser(description="is every agent taught to use the chain?")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv[1:])

    r = check()
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0 if r["ok"] else 1

    print(f"TEACHING CHECK — {r['taught']}/{r['total']} surfaces carry the chain\n")
    for s in r["surfaces"]:
        mark = "✓" if s["ok"] else "✗"
        print(f"  {mark} {s['surface']}")
        print(f"      reach: {s['reach']}")
        if s["missing"]:
            print(f"      MISSING: {', '.join(s['missing'])}")
        if s.get("dead"):
            for d in s["dead"]:
                print(f"      DEAD POINTER: {d['referenced']} (referenced in {d['in']})")
    if not r["ok"]:
        print("\n  An agent can work a whole session without knowing the chain exists.")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
