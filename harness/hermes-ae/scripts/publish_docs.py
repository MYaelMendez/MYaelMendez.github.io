"""Generate docs/VIDEOS.md and docs/RECEIPT_CHAIN.md from repo data.

Uses videos.json plus a sanitized ledger snapshot. Never writes paths or secrets.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def load(path, default):
    return json.loads(Path(path).read_text()) if Path(path).exists() else default


def main():
    videos = load(ROOT / "videos.json", {"gallery": "", "videos": []})
    snapshot = load(ROOT / "receipts_snapshot.json", [])
    lines = ["# Videos", "",
             "Published artifacts from the `hermes-ae` studio.", ""]
    for v in videos["videos"]:
        lines += [f"## {v['title']}", "",
                  f"- File: `{v['name']}`",
                  f"- Specs: {v['resolution']}, {v['fps']} fps, {v['duration_s']} s, {v['codec']}",
                  f"- Physics: {v['physics']}",
                  f"- Receipt: `{v['receipt']}`",
                  f"- [Download]({v['url']})", ""]
    lines += ["## Gallery", "", f"- [Full video gallery]({videos['gallery']})", ""]
    (DOCS / "VIDEOS.md").write_text("\n".join(lines))

    chain = ["# Receipt Chain", "",
             f"Sanitized snapshot: {len(snapshot)} entries. Full ledger is `HUMAN://ROOT` hash-chained.", "",
             "| Time | Action | Authority | Hash |", "|---|---|---|---|"]
    for e in snapshot[-40:]:
        chain.append(f"| {e.get('ts','')} | `{e.get('action','')}` | {e.get('authority','')} | `{e.get('hash','')[:16]}…` |")
    chain.append("")
    (DOCS / "RECEIPT_CHAIN.md").write_text("\n".join(chain))
    print(json.dumps({"success": True, "videos": len(videos["videos"]),
                      "receipts": len(snapshot)}))


if __name__ == "__main__":
    main()
