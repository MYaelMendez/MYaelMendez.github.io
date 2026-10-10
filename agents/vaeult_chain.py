#!/usr/bin/env python3
"""
væult_chain.py — the whole tool chain, under one name.

væult is not one script. It is the chain: custody → format → gate → authority →
contract → dispatch → publish → transport. Each link was built to answer a
failure the previous link could not.

    væult://            the chain itself
    væult:// chain      every link, its role, its verbs
    væult:// verify     does every link still compile and answer?
    væult:// manifest   machine-readable chain (for agents)
    væult:// <link> <action> [...]      call any link through one entry

WHY ONE NAME
------------
Eight tools with eight CLIs is eight things to remember and eight places to be
inconsistent. Naming the chain makes the contract explicit: a link that cannot
answer is a broken chain, and `væult:// verify` says so.

The links, in order:

    1  vault        custody          the sealed store
    2  envelope     format           ae:1:<type>:<b64url> — one wire format
    3  supervision  gate             produce-and-verify, refuses broken artifacts
    4  signing      authority        Ed25519 capability cards
    5  pledge       contract         the commitment every agent signs
    6  kanban       dispatch         physical cards → board state
    7  push         publish          fleet-safe, kanban-serialized
    8  transport    delivery         sealed envelopes over mail / SMS

USAGE
    python væult_chain.py chain
    python væult_chain.py verify
    python væult_chain.py manifest --out væult-chain.json
    python væult_chain.py call supervision status
    python væult_chain.py call envelope encode secret '{"name":"K"}'
"""
from __future__ import annotations

import argparse
import importlib
import json
import pathlib
import subprocess
import sys
import time

AGENTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AGENTS))

# ── the chain ─────────────────────────────────────────────────────────────────
# Ordered by data flow: a secret is sealed, formatted, gated, authorised,
# committed to, dispatched, published, delivered.

CHAIN = [
    {
        "n": 1, "id": "vault", "module": "væult", "path": "C:/æ/væult/væult.py",
        "role": "custody", "answers": "where the secret lives",
        "verbs": ["init", "set", "get", "list", "rm", "export", "verify", "qr", "qr-open"],
        "shape": "cli",
    },
    {
        "n": 2, "id": "envelope", "module": "qr_envelope", "path": "C:/æ/agents/qr_envelope.py",
        "role": "format", "answers": "how anything crosses a boundary",
        "verbs": ["TYPES", "encode", "decode", "inspect", "is_envelope"],
        "shape": "python",
    },
    {
        "n": 3, "id": "supervision", "module": "qr_supervision", "path": "C:/æ/agents/qr_supervision.py",
        "role": "gate", "answers": "is the artifact real, or a picture of one",
        "verbs": ["produce", "supervise", "selftest", "chain_prev", "chain_append"],
        "shape": "python",
    },
    {
        "n": 4, "id": "signing", "module": "card_signing", "path": "C:/æ/agents/card_signing.py",
        "role": "authority", "answers": "who may act, and until when",
        "verbs": ["keygen", "sign_card", "verify_card"],
        "shape": "python",
    },
    {
        "n": 5, "id": "pledge", "module": "agent_pledge", "path": "C:/æ/agents/agent_pledge.py",
        "role": "contract", "answers": "what an agent has promised",
        "verbs": ["pledge_text", "pledge_hash", "commit", "verify", "roster", "render_html"],
        "shape": "python",
    },
    {
        "n": 6, "id": "kanban", "module": "qr_kanban", "path": "C:/æ/agents/qr_kanban.py",
        "role": "dispatch", "answers": "how a physical card moves the board",
        "verbs": ["mint_card", "read_card", "dispatch", "require_pledge", "VERBS"],
        "shape": "python",
    },
    {
        "n": 7, "id": "push", "module": "kanban_push", "path": "C:/æ/agents/kanban_push.py",
        "role": "publish", "answers": "how a fleet pushes without colliding",
        "verbs": ["cmd_push", "cmd_status", "cmd_rescue", "KanbanLock", "ensure_task"],
        "shape": "python",
    },
    {
        "n": 8, "id": "transport", "module": "qr_mail", "path": "C:/æ/agents/qr_mail.py",
        "role": "delivery", "answers": "how a sealed envelope reaches a person",
        "verbs": ["send_mail", "check_inbox", "decode_file", "render_qr_png", "seal_for_mail"],
        "shape": "python",
        "also": [{"id": "sms", "module": "qr_sms", "path": "C:/æ/agents/qr_sms.py",
                  "verbs": ["send_sms", "check_inbox", "segments", "reassemble"]}],
    },
]

BY_ID = {l["id"]: l for l in CHAIN}


# ── introspection ─────────────────────────────────────────────────────────────

def _import(module: str):
    try:
        return importlib.import_module(module), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def link_status(link: dict) -> dict:
    """Does this link exist, import, and expose the verbs it claims?"""
    path = pathlib.Path(link["path"])
    out = {"id": link["id"], "path": str(path), "exists": path.exists(),
           "role": link["role"], "answers": link["answers"],
           "verbs_declared": link["verbs"], "verbs_found": [], "missing": [],
           "ok": False, "detail": ""}

    if not path.exists():
        out["detail"] = "file not found"
        return out

    if link["shape"] == "cli":
        # a CLI link: prove it answers --help or a known verb
        try:
            r = subprocess.run([sys.executable, str(path), "verify"],
                               capture_output=True, text=True, timeout=30)
            out["ok"] = r.returncode in (0, 1, 2)  # answers = alive
            out["detail"] = "cli answers" if out["ok"] else f"rc={r.returncode}"
        except Exception as e:
            out["detail"] = f"{type(e).__name__}"
        return out

    mod, err = _import(link["module"])
    if mod is None:
        out["detail"] = f"import failed — {err}"
        return out
    found = [v for v in link["verbs"] if hasattr(mod, v)]
    out["verbs_found"] = found
    out["missing"] = [v for v in link["verbs"] if not hasattr(mod, v)]
    out["ok"] = not out["missing"]
    out["detail"] = "all verbs present" if out["ok"] else f"missing: {', '.join(out['missing'])}"
    return out


def verify_chain() -> dict:
    """Every link, checked. A chain is only as strong as its weakest link."""
    links = [link_status(l) for l in CHAIN]
    # the transport link has a second module
    for l in CHAIN:
        for extra in l.get("also", []):
            p = pathlib.Path(extra["path"])
            mod, err = _import(extra["module"])
            found = [v for v in extra["verbs"] if mod and hasattr(mod, v)]
            missing = [v for v in extra["verbs"] if v not in found]
            links.append({
                "id": extra["id"], "path": str(p), "exists": p.exists(),
                "role": "delivery", "answers": "sealed envelope over SMS",
                "verbs_declared": extra["verbs"], "verbs_found": found,
                "missing": missing,
                "ok": (mod is not None) and not missing,
                "detail": ("all verbs present" if mod is not None and not missing
                           else (f"import failed — {err}" if mod is None
                                 else f"missing: {', '.join(missing)}")),
            })
    broken = [l for l in links if not l["ok"]]
    return {"chain": links, "total": len(links), "ok": len(links) - len(broken),
            "broken": [l["id"] for l in broken], "healthy": not broken}


# ── calling a link ────────────────────────────────────────────────────────────

def call(link_id: str, action: str, *args) -> dict:
    """Call one link through the chain entry. Never raises."""
    link = BY_ID.get(link_id)
    if link is None:
        # the sms sibling
        for l in CHAIN:
            for extra in l.get("also", []):
                if extra["id"] == link_id:
                    link = {**extra, "shape": "python"}
        if link is None:
            return {"ok": False, "error": f"no link '{link_id}' "
                                          f"(have: {', '.join(BY_ID)})"}

    if link["shape"] == "cli":
        try:
            r = subprocess.run([sys.executable, link["path"], action, *[str(a) for a in args]],
                               capture_output=True, text=True, timeout=180)
            return {"ok": r.returncode == 0, "link": link_id, "action": action,
                    "stdout": r.stdout.strip()[:4000], "stderr": r.stderr.strip()[:800],
                    "rc": r.returncode}
        except Exception as e:
            return {"ok": False, "link": link_id, "action": action,
                    "error": f"{type(e).__name__}: {e}"}

    mod, err = _import(link["module"])
    if mod is None:
        return {"ok": False, "link": link_id, "error": f"import failed — {err}"}
    fn = getattr(mod, action, None)
    if fn is None:
        return {"ok": False, "link": link_id, "action": action,
                "error": f"'{link_id}' has no '{action}' "
                         f"(have: {', '.join(link['verbs'])})"}

    # A constant (TYPES, VERBS) is a value, not a call — return it as-is.
    if not callable(fn):
        return {"ok": True, "link": link_id, "action": action, "result": fn}

    # Split passthrough args into kwargs (--flag value / --flag) and positionals,
    # so `call pledge verify --agent zeus` reaches verify(agent_id="zeus")
    # instead of verify("--agent", "zeus").
    kwargs, positional = {}, []
    i = 0
    while i < len(args):
        a = args[i]
        if isinstance(a, str) and a.startswith("--"):
            key = a[2:].replace("-", "_")
            if i + 1 < len(args) and not (isinstance(args[i + 1], str)
                                          and args[i + 1].startswith("--")):
                kwargs[key] = args[i + 1]
                i += 2
            else:
                kwargs[key] = True
                i += 1
        else:
            positional.append(a)
            i += 1

    try:
        result = fn(*positional, **kwargs)
        return {"ok": True, "link": link_id, "action": action, "result": result}
    except TypeError:
        # the link may not take kwargs — retry positionally before failing
        try:
            result = fn(*(positional + list(kwargs.values())))
            return {"ok": True, "link": link_id, "action": action, "result": result}
        except Exception as e:
            return {"ok": False, "link": link_id, "action": action,
                    "error": f"{type(e).__name__}: {e}"}
    except Exception as e:
        return {"ok": False, "link": link_id, "action": action,
                "error": f"{type(e).__name__}: {e}"}


# ── the manifest ──────────────────────────────────────────────────────────────

def manifest() -> dict:
    """Machine-readable chain — an agent can fetch this and know the whole system."""
    v = verify_chain()
    by_id = {l["id"]: l for l in v["chain"]}
    return {
        "system": "æ://",
        "name": "væult",
        "meaning": "the whole tool chain, under one name",
        "flow": "custody → format → gate → authority → contract → dispatch → publish → delivery",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "healthy": v["healthy"],
        "links_total": v["total"],
        "links_ok": v["ok"],
        "links": [
            {"n": l["n"], "id": l["id"], "role": l["role"], "answers": l["answers"],
             "path": l["path"], "verbs": l["verbs"],
             "status": "ok" if by_id.get(l["id"], {}).get("ok") else "broken"}
            for l in CHAIN
        ],
        "entry": "væult:// <link> <action> [args]",
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv):
    ap = argparse.ArgumentParser(description="væult — the whole tool chain")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("chain")
    sub.add_parser("verify")
    m = sub.add_parser("manifest"); m.add_argument("--out", default=None)
    c = sub.add_parser("call")
    c.add_argument("link")
    c.add_argument("action", nargs="?", default=None)
    c.add_argument("args", nargs=argparse.REMAINDER,
                   help="everything after <action>, passed through verbatim")

    # Everything after `call <link> <action>` belongs to the LINK, not to us.
    # Without this, a flag like `--agent zeus` is parsed by our own argparse and
    # rejected before the link ever sees it.
    argv = list(argv)
    if "call" in argv:
        i = argv.index("call")
        # argv[0] is the script name — argparse must not see it
        head = argv[1:i + 1]          # up to and including "call"
        tail = argv[i + 1:]           # link, action, then passthrough
        a = ap.parse_args(head + tail[:2])
        a.args = tail[2:]
    else:
        a = ap.parse_args(argv[1:])

    if a.cmd == "chain":
        v = verify_chain()
        print(f"væult — the whole tool chain   ({v['ok']}/{v['total']} links healthy)\n")
        print("  #  LINK          ROLE        ANSWERS")
        for l in CHAIN:
            st = next((x for x in v["chain"] if x["id"] == l["id"]), {})
            mark = "✓" if st.get("ok") else "✗"
            print(f"  {mark} {l['n']}  {l['id']:12s}  {l['role']:10s}  {l['answers']}")
            print(f"        {'':12s}  {'':10s}  {l['path']}")
        for l in CHAIN:
            for extra in l.get("also", []):
                st = next((x for x in v["chain"] if x["id"] == extra["id"]), {})
                mark = "✓" if st.get("ok") else "✗"
                print(f"  {mark} {'':2s}  {extra['id']:12s}  {'delivery':10s}  {extra['path']}")
        if v["broken"]:
            print(f"\n  BROKEN: {', '.join(v['broken'])}")
        return 0 if v["healthy"] else 1

    if a.cmd == "verify":
        v = verify_chain()
        for l in v["chain"]:
            mark = "✓" if l["ok"] else "✗"
            print(f"  {mark} {l['id']:12s} {l['detail']}")
        print(f"\n  {v['ok']}/{v['total']} healthy")
        return 0 if v["healthy"] else 1

    if a.cmd == "manifest":
        d = manifest()
        text = json.dumps(d, indent=2, ensure_ascii=False)
        if a.out:
            pathlib.Path(a.out).write_text(text, encoding="utf-8")
            print(f"  wrote {a.out}")
        else:
            print(text)
        return 0

    if a.cmd == "call":
        if not a.action:
            r = {"ok": True, "link": a.link,
                 "verbs": BY_ID.get(a.link, {}).get("verbs", [])}
            print(json.dumps(r, indent=2, default=str))
            return 0
        res = call(a.link, a.action, *a.args)
        out = res.get("stdout") or res.get("error")
        if out is None and "result" in res:
            out = res["result"]
        print(out if isinstance(out, str) else json.dumps(out, indent=2, default=str))
        return 0 if res.get("ok") else 1

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
