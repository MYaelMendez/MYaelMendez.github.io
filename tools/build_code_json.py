#!/usr/bin/env python3
"""Build `code.json` — the machine-readable face of æ://code-mode.

Agents love code-mode because it is composable; they cannot use it while it only
exists as an HTML terminal. This derives one parseable document from the real
indexes plus the DSL verbs actually implemented in code.html:

    python tools/build_code_json.py            # write code.json
    python tools/build_code_json.py --check    # exit 1 if stale
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "code.json"
HOME = "https://myaelmendez.github.io"

VERBS_BLOCK = re.compile(r"out\('<span class=\"h\">\s*(æ[.\w]+)\(([^)]*)\)\s*(.*?)</span>'")


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def dsl_verbs():
    """Derive the DSL verb list from code.html's own help block — no drift."""
    html = (ROOT / "code.html").read_text(encoding="utf-8")
    verbs = []
    for name, args, desc in VERBS_BLOCK.findall(html):
        verbs.append({"name": name, "args": args.strip(), "desc": re.sub(r"<[^>]+>", "", desc).strip()})
    return verbs


def build():
    caps = load("capability-manifest.json").get("capabilities", [])
    cb = load("codebase.json")
    tools = load("code-mode-tools.json").get("capabilities", [])
    return {
        "$schema": f"{HOME}/schemas/code-mode-v1.json",
        "schema": "ae.code-mode/1",
        "name": "æ://code-mode",
        "description": "Terminal I/O over the mesh — ranked, composable discovery. One fetch, no scraping.",
        "surface": "/code.html",
        "data": "/code.json",
        "invocation": {
            "kind": "url",
            "example": f"{HOME}/code.html?cmd=%C3%A6.find('cuda')",
            "note": "?cmd=<expr> runs on load; pipes compose (find(q) | open).",
        },
        "dsl": dsl_verbs(),
        "capabilities": [
            {
                "id": c.get("id", ""), "name": c.get("name", ""),
                "address": c.get("address", ""), "url": c.get("url", ""),
                "category": c.get("category", ""), "layer": c.get("layer"),
                "access": c.get("access", "read"),
                "capabilities": c.get("capabilities", []),
            }
            for c in caps
        ],
        "modules": [
            {
                "id": m.get("id", ""), "kind": m.get("kind", ""), "path": m.get("path", ""),
                "exports": m.get("exports", []), "address": m.get("address"),
                "desc": m.get("desc", ""),
            }
            for m in cb.get("modules", [])
        ],
        "tools": [
            {"id": t.get("name", ""), "mesh": t.get("mesh", ""), "sig": t.get("sig", ""),
             "doc": t.get("doc", "")}
            for t in tools
        ],
        "runtime": cb.get("runtime", {}),
        "counts": {
            "dsl": len(dsl_verbs()),
            "capabilities": len(caps),
            "modules": len(cb.get("modules", [])),
            "tools": len(tools),
        },
    }


def main():
    doc = build()
    if "--check" in sys.argv:
        if not OUT.exists():
            print(f"STALE: {OUT} missing")
            return 1
        if json.loads(OUT.read_text(encoding="utf-8")) != doc:
            print("STALE: code.json differs from sources")
            return 1
        print(f"FRESH: {OUT} · {doc['counts']}")
        return 0
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} · {doc['counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
