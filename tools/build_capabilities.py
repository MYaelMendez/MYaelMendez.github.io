#!/usr/bin/env python3
"""æ:// capability derivation — ONE manifest → atlas + capability index.
Derived, never hand-written. Edit surface-manifest.json, run this.
    python tools/build_capabilities.py
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
LAYER = ["public", "published", "operator", "custody"]

sm = json.loads((ROOT / "surface-manifest.json").read_text(encoding="utf-8"))
cats = [c["id"] for c in sm["categories"]]

def x_of(cat): return (cats.index(cat) + 1) if cat in cats else len(cats) + 1
def authority(s):
    cat = s.get("category", "")
    if cat == "secrets" or s.get("auth") == "passphrase": return 3
    if cat == "privateclient" or s.get("agent_access") == "write": return 2
    if s.get("external"): return 1
    return 0

counts, atlas, caps = {}, [], []
def next_y(cat, z):
    """y = item ordinal within (category, depth). Every (x,y,z,æ) is unique."""
    key = (cat, z); y = counts.get(key, 0); counts[key] = y + 1; return y

def emit(id, name, url, cat, x, y, z, a, desc, access, tags):
    atlas.append({"id": id, "name": name, "url": url, "cat": cat, "x": x, "y": y, "z": z, "a": a, "desc": desc, "access": access})
    caps.append({"id": id, "name": name, "address": f"x{x}:y{y}:z{z}:æ{a}", "url": url, "category": cat,
                 "capabilities": tags, "access": access, "layer": a, "layer_name": LAYER[a]})

for s in sm["surfaces"]:
    cat = s.get("category", "misc"); x = x_of(cat); a = authority(s); tags = s.get("capabilities", [])
    emit(s["id"], s["name"], s["url"], cat, x, next_y(cat, 0), 0, a, s.get("description", ""), s.get("agent_access", "read"), tags)
    for sub in s.get("subpages", []):
        # subpages live at depth z=1, each with its own y ordinal — never collide,
        # and they are REAL resources so they belong in the capability manifest too
        emit(s["id"] + "-" + sub["name"].lower(), sub["name"], sub["url"], cat, x, next_y(cat, 1), 1, a,
             s["name"] + " · " + sub["name"], s.get("agent_access", "read"), tags)

(ROOT / "ae-atlas.json").write_text(json.dumps({
    "$schema": "https://myaelmendez.github.io/schemas/ae-atlas-v1.json", "name": "æ:// coordinate atlas", "version": "1.0.0",
    "description": "Every surface addressed in 4-space. x=category ordinal, y=item ordinal, z=depth, æ=authority gradient. Origin = x0:y0:z0:æ0.",
    "origin": {"x": 0, "y": 0, "z": 0, "a": 0}, "authority_axis": {"0": "public", "1": "published", "2": "operator", "3": "custody"},
    "categories": cats, "count": len(atlas), "addresses": atlas}, ensure_ascii=False, indent=2), encoding="utf-8")

(ROOT / "ae-atlas.js").write_text("window.AE_ATLAS=" + json.dumps(atlas, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")

(ROOT / "capability-manifest.json").write_text(json.dumps({
    "$schema": "https://myaelmendez.github.io/schemas/capability-manifest-v1.json", "name": "æ:// capability manifest", "version": "1.0.0",
    "homebase": "https://myaelmendez.github.io", "operator": "Yæl Méndez",
    "description": "One manifest. Every capability surface addressed in 4-space and reachable by code-mode. Derived from surface-manifest.json — never hand-written.",
    "authority_axis": {"0": "public", "1": "published", "2": "operator", "3": "custody"},
    "discovery": {"manifest": "/capability-manifest.json", "atlas": "/ae-atlas.json", "surfaces": "/surface-manifest.json", "code_mode": "/code.html"},
    "count": len(caps), "capabilities": caps}, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"derived: {len(atlas)} addresses, {len(caps)} capabilities")
