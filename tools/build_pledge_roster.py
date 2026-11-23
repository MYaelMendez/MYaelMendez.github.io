#!/usr/bin/env python3
"""Derive the published pledge roster from LOCAL custody.

Custody — the signed commitments — lives at ``C:\\æ\\kænbæn\\agent-pledge.json`` and is
local-only, never published. This tool publishes the **roster** (who committed, and
whether that commitment is current against the pledge as it stands now) without ever
publishing keys or signatures.

    python tools/build_pledge_roster.py            # write agent-pledge.json
    python tools/build_pledge_roster.py --check    # exit 1 if the roster is stale

This gate runs where custody lives (the operator's machine), not in CI: the source
file is deliberately outside the repo.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "agent-pledge.json"
DEFAULT_CUSTODY = Path(r"C:\æ\kænbæn\agent-pledge.json")
DEFAULT_MODULE_DIR = r"C:\æ\agents"


def build(custody_path: Path, module_dir: str) -> dict:
    sys.path.insert(0, module_dir)
    import agent_pledge as pledge  # noqa: E402 — local-only module, path is explicit

    custody = json.loads(custody_path.read_text(encoding="utf-8"))
    commitments = custody.get("commitments") or {}
    agents = []
    for agent in sorted(commitments):
        r = pledge.verify(agent)
        agents.append({
            "agent": agent,
            "status": r["status"],
            "ok": bool(r.get("ok")),
            "signed_at": r.get("signed_at", ""),
            "fingerprint": r.get("fingerprint", ""),
            "reason": r.get("reason", ""),
        })
    # The signing key is the operator's card key by design ("one identity per
    # operator"), so agent ids are ROLES on one identity — not separate agents.
    # Publish the count so nothing reads this roster as 8 cryptographic identities.
    distinct_keys = len({(v.get("pubkey") or "") for v in commitments.values()})
    return {
        "system": "æ://",
        "pledge_hash": pledge.pledge_hash(),
        "committed": sum(1 for a in agents if a["ok"]),
        "total": len(agents),
        "distinct_keys": distinct_keys,
        "identity_note": "one operator key (card.key) — agent ids are roles on that identity, not separate cryptographic agents",
        "agents": agents,
        "text_url": "https://myaelmendez.github.io/pledge.html",
        "commit_command": "python agent_pledge.py commit --agent <id>",
        "gate": "python agent_pledge.py require --agent <id>",
        "source": "derived from local custody; keys and signatures never published",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--custody", default=str(DEFAULT_CUSTODY))
    ap.add_argument("--module-dir", default=DEFAULT_MODULE_DIR)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    custody = Path(a.custody)
    if not custody.exists():
        print(f"STALE: custody not found at {custody} — this gate runs where custody lives")
        return 1
    try:
        doc = build(custody, a.module_dir)
    except ImportError as e:
        print(f"STALE: cannot import agent_pledge from {a.module_dir}: {e}")
        return 1

    if a.check:
        if not OUT.exists():
            print(f"STALE: {OUT} missing")
            return 1
        if json.loads(OUT.read_text(encoding="utf-8")) != doc:
            print("STALE: agent-pledge.json differs from custody")
            return 1
        print(f"FRESH: roster derived from custody · {doc['committed']}/{doc['total']} current")
        return 0

    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} · {doc['committed']}/{doc['total']} current · hash {doc['pledge_hash'][:12]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
