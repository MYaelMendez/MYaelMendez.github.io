#!/usr/bin/env python3
"""Build `.well-known/agent-card.json` — the machine surface an agent fetches first.

Derived, never hand-maintained: every list comes from a real index in the repo, so a
regenerate is a gate, not a claim. Run after any change to the indexes.

    python tools/build_agent_card.py            # write .well-known/agent-card.json
    python tools/build_agent_card.py --check    # exit 1 if the card is stale
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".well-known" / "agent-card.json"
HOME = "https://myaelmendez.github.io"
CONSOLE = f"{HOME}/ae/control/index-live.html"


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def build():
    caps = load("capability-manifest.json").get("capabilities", [])
    tools = load("code-mode-tools.json").get("capabilities", [])
    mesh = load("skill-guide/capability-mesh.json")
    atlas = load("ae-atlas.json")
    sm = load("surface-manifest.json")

    skills = [
        {"id": s.get("name", ""), "category": s.get("cat", ""), "tier": s.get("tier", ""),
         "desc": s.get("desc", "")}
        for s in mesh.get("skills", [])
    ]
    schemes = [
        {"id": s.get("scheme", ""), "node": s.get("node", ""), "tier": s.get("tier", ""),
         "desc": s.get("desc", "")}
        for s in mesh.get("schemes", [])
    ]
    nodes = [
        {"id": n.get("id", ""), "name": n.get("name", ""), "role": n.get("role", ""),
         "gpu": n.get("gpu", "")}
        for n in mesh.get("nodes", [])
    ]
    addresses = [
        {"id": s.get("id", ""), "name": s.get("name", ""), "address": f"x{s['x']}:y{s['y']}:z{s['z']}:æ{s['a']}",
         "url": s.get("url", ""), "cat": s.get("cat", "")}
        for s in atlas.get("addresses", [])
    ]

    return {
        "$schema": f"{HOME}/schemas/agent-card-v1.json",
        "schema": "ae.agent-card/1",
        "name": "æ:// HOMEBASE",
        "description": "Sovereign agentic-engineering estate — find any resource, invoke the local compiler, receive a SHA-256 receipt.",
        "url": CONSOLE,
        "version": "1.0.0",
        "protocol": ">_æ:",
        "operator": {
            "name": "Yæl Méndez",
            "x": "@yaelmendez",
            "github": "MYaelMendez",
            "email": "yael@llm.store",
        },
        "endpoints": {
            "console": CONSOLE,
            "agent_card": f"{HOME}/.well-known/agent-card.json",
            "atlas": f"{HOME}/ae-atlas.json",
            "discover": f"{HOME}/ae/control/index-live.html#discover",
            "manifest": f"{HOME}/capability-manifest.json",
            "webmcp": f"{HOME}/.well-known/webmcp.json",
            "did": f"{HOME}/.well-known/did.json",
            "skills": f"{HOME}/.well-known/skills/index.json",
        },
        "discovery": {
            "kind": "client-side index search",
            "note": "The console queries six estate indexes in the browser; there is no server.",
            "indexes": ["ae-atlas.json", "codebase.json", "qr_inventory.json",
                        "code-mode-tools.json", "capability-mesh.json",
                        "capability-manifest.json", "surface-manifest.json"],
        },
        "invocation": {
            "kind": "url",
            "example": f"{CONSOLE}?intent=find%20asimov",
            "verbs": ["find <query>", "atlas", "ls", "goto <coord>", "æ://<name>",
                      "origin", "help"],
            "note": "Resolving an address navigates; it never executes. Every verb is read-only.",
        },
        "capabilities": [
            {"id": c.get("id", ""), "name": c.get("name", ""), "address": c.get("address", ""),
             "url": c.get("url", ""), "category": c.get("category", ""),
             "capabilities": c.get("capabilities", [])}
            for c in caps
        ],
        "tools": [{"id": t.get("name", ""), "mesh": t.get("mesh", ""), "doc": t.get("doc", "")}
                  for t in tools],
        "skills": skills,
        "schemes": schemes,
        "nodes": nodes,
        "addresses": addresses,
        "categories": sm.get("categories", []),
        "authority": {
            "human_governed": True,
            "note": "An address is not a permission. Resolving never executes.",
            "gates": ["agent_pledge.py require --agent <id>", "asimov:// requires a bound human approval"],
        },
        "receipt": {
            "schema": "ae.local.compile.receipt.v1",
            "algorithm": "sha256",
            "note": "Real hash over local results; no external execution, no market data.",
        },
        "counts": {
            "capabilities": len(caps),
            "tools": len(tools),
            "skills": len(skills),
            "schemes": len(schemes),
            "nodes": len(nodes),
            "addresses": len(addresses),
            "surfaces": len(addresses),
        },
        "generated_from": sorted([
            "capability-manifest.json", "code-mode-tools.json", "skill-guide/capability-mesh.json",
            "ae-atlas.json", "surface-manifest.json",
        ]),
    }


def main():
    card = build()
    if "--check" in sys.argv:
        if not OUT.exists():
            print(f"STALE: {OUT} missing")
            return 1
        current = json.loads(OUT.read_text(encoding="utf-8"))
        if current != card:
            print("STALE: card differs from sources")
            for k in sorted(set(current) | set(card)):
                if current.get(k) != card.get(k):
                    print(f"  - {k}")
            return 1
        print(f"FRESH: {OUT} matches sources · {card['counts']}")
        return 0
    OUT.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} · {card['counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
