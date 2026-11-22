"""
export_wasm_state.py — derive the continuity sections JSON from continuity.xml.

The Rust core takes a state JSON; this produces that state from the REAL
committed record so the browser probe exercises actual data, not a fixture.
Writes continuity-wasm/dist/state.json.
"""
from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

XML = Path("C:/æ/github-pages/continuity.xml")
OUT = Path("C:/æ/github-pages/continuity-wasm/dist/state.json")
VERDICTS = ("proved", "broke", "change")


def main():
    root = ET.parse(XML).getroot()
    sections = []
    for s in root.find("sections"):
        num = s.get("num", "")
        sections.append({
            "key": s.get("ordinal"),
            "label": f"§{num}" if num else "§·",
            "title": s.findtext("title") or "",
            "date": s.get("date", ""),
            "parity": s.get("parity", "ok"),
            "has_proved": s.get("has_proved") == "1",
            "has_broke": s.get("has_broke") == "1",
            "has_change": s.get("has_change") == "1",
        })
    OUT.write_text(json.dumps(sections, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT} — {len(sections)} sections from {XML.name}")


if __name__ == "__main__":
    main()
