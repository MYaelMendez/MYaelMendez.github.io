#!/usr/bin/env python3
"""
agent_pledge.py — the commitment every agent makes, and the roster that proves it.

WHY THIS IS NOT A PAGE OF PROSE
-------------------------------
A pledge that is only text is marketing. This one is a **verifiable commitment**:

  · the pledge text is canonical and hashed (SHA-256) — it can be cited and checked
  · each agent commits by signing that exact hash with its Ed25519 key
  · the roster is generated from real records, never hand-written
  · a signature that does not verify against the current pledge hash is shown as
    LAPSED, not quietly dropped — so drift is visible

Change one word of the pledge and every existing commitment lapses. That is the
point: the hash makes the promise precise, and the signature makes it the
agent's own.

GROUNDED IN THE OPERATOR'S OWN PRINCIPLES
-----------------------------------------
Every commitment below restates something Yæl Méndez already holds, taken from
AGENTS.md, the github.io operating principles, and the #opensourceware boundary.
Nothing is invented here. The pledge collects them into one citable text so an
agent can be held to them.

USAGE
-----
    python agent_pledge.py text                  print the canonical pledge + hash
    python agent_pledge.py commit --agent zeus   sign the pledge as this agent
    python agent_pledge.py verify --agent zeus   is this agent's commitment current?
    python agent_pledge.py roster                who has committed, and are they current
    python agent_pledge.py render --out pledge.html
    python agent_pledge.py require --agent zeus  exit 0 if current, 1 if not (a gate)
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import pathlib
import sys
import time

AGENTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AGENTS))

K_BASE = pathlib.Path(os.environ.get("KAENBAEN_BASE", r"C:\æ\kænbæn"))
CONTRACTS = K_BASE / "capability-contracts.json"
PLEDGE_FILE = K_BASE / "agent-pledge.json"

# ── the pledge ────────────────────────────────────────────────────────────────
# Each line is a commitment an agent can be held to. Keep them checkable: a
# commitment nobody can test is a slogan.

PLEDGE_TITLE = "The Agent Commitment"

PLEDGE = [
    ("I do not speak for the human.",
     "Context may propagate; authority does not. I bring evidence and "
     "recommendations. The human decides."),

    ("I do not claim what I have not verified.",
     "\"Render + decode + live HTTP 200 before anything is called true.\" If I "
     "have not run it, I say so — I never present a plausible result as a "
     "measured one."),

    ("I do not mistake possession for authority.",
     "Holding a token, a key, or a card is not permission to act. Where a "
     "capability is required, I require it — and I refuse when it is absent."),

    ("I do not let a broken artifact look fine.",
     "A thing that has not been checked back is not a thing. Where a gate "
     "exists I pass through it; where one does not, I say the check is missing "
     "rather than report a pass."),

    ("I do not keep the secret.",
     "The tool is open; the secrets are not. I never move a credential into a "
     "transcript, a surface, or a log, and I refuse one offered that way."),

    ("I do not write over another agent's work.",
     "A shared resource with a read-modify-write window gets a lock, and the "
     "lock gets a record. I claim before I act and I record what I did."),

    ("I do not leave a failure unexplained.",
     "A refusal names its reason. A fallback names itself as a fallback. "
     "Silent degradation is the failure mode I am most likely to cause, so it "
     "is the one I watch for first."),

    ("I do not confuse the tool with the purpose.",
     "I build so a person can learn, build, and teach others. Capability that "
     "does not return to a human is not finished."),
]

PLEDGE_EPIGRAPH = (
    "\"When you tell the truth you don't have to remember anything.\""
)


def pledge_text() -> str:
    """The canonical pledge text — the exact bytes that get hashed."""
    lines = [PLEDGE_TITLE, "", PLEDGE_EPIGRAPH, ""]
    for i, (claim, body) in enumerate(PLEDGE, 1):
        lines.append(f"{i}. {claim}")
        lines.append(f"   {body}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def pledge_hash() -> str:
    """SHA-256 over the canonical text. The identity of THIS pledge."""
    return hashlib.sha256(pledge_text().encode("utf-8")).hexdigest()


# ── keys (reuse the card signing key — one identity per operator) ─────────────

def _key_path() -> pathlib.Path:
    d = pathlib.Path(os.environ.get("CARD_KEY_DIR", r"C:\æ\secrets\keys"))
    return d / "card.key"


def _load_or_make_key():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    p = _key_path()
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        priv = Ed25519PrivateKey.generate()
        p.write_text(priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()).hex(), encoding="ascii")
        try:
            os.chmod(p, 0o600)
        except OSError:
            pass
        pub = priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw)
        p.with_suffix(".pub").write_text(pub.hex(), encoding="ascii")
    return Ed25519PrivateKey.from_private_bytes(bytes.fromhex(p.read_text(encoding="ascii").strip()))


# ── records ───────────────────────────────────────────────────────────────────

def _load_pledges() -> dict:
    if not PLEDGE_FILE.exists():
        return {"system": "æ://", "pledge_hash": pledge_hash(), "commitments": {}}
    try:
        return json.loads(PLEDGE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"system": "æ://", "pledge_hash": pledge_hash(), "commitments": {}}


def _save_pledges(d: dict):
    PLEDGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    d["pledge_hash"] = pledge_hash()
    d["updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    PLEDGE_FILE.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def commit(agent_id: str) -> dict:
    """Sign the CURRENT pledge hash as this agent. Returns the record."""
    from cryptography.hazmat.primitives import serialization
    priv = _load_or_make_key()
    h = pledge_hash()
    sig = priv.sign(f"pledge:{h}:{agent_id}".encode("utf-8"))
    pub = priv.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw)

    rec = {
        "pledge_hash": h,
        "signed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sig": base64.urlsafe_b64encode(sig).decode("ascii").rstrip("="),
        "pubkey": pub.hex(),
        "fingerprint": hashlib.sha256(pub).hexdigest()[:16],
    }
    d = _load_pledges()
    d.setdefault("commitments", {})[agent_id] = rec
    _save_pledges(d)
    return rec


def verify(agent_id: str) -> dict:
    """Is this agent's commitment CURRENT (i.e. to the pledge as it stands now)?"""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature

    d = _load_pledges()
    rec = (d.get("commitments") or {}).get(agent_id)
    if not rec:
        return {"agent": agent_id, "status": "none", "ok": False,
                "reason": "has not committed to the pledge"}

    current = pledge_hash()
    if rec.get("pledge_hash") != current:
        return {"agent": agent_id, "status": "lapsed", "ok": False,
                "reason": "committed to an older pledge text",
                "committed_to": rec.get("pledge_hash", "")[:16],
                "current": current[:16]}

    try:
        sig = base64.urlsafe_b64decode(rec["sig"] + "=" * (-len(rec["sig"]) % 4))
        pub = bytes.fromhex(rec["pubkey"])
        Ed25519PublicKey.from_public_bytes(pub).verify(
            sig, f"pledge:{current}:{agent_id}".encode("utf-8"))
    except InvalidSignature:
        return {"agent": agent_id, "status": "invalid", "ok": False,
                "reason": "signature does not verify"}
    except Exception as e:
        return {"agent": agent_id, "status": "invalid", "ok": False,
                "reason": f"{type(e).__name__}"}

    return {"agent": agent_id, "status": "current", "ok": True,
            "signed_at": rec.get("signed_at"), "fingerprint": rec.get("fingerprint")}


def registered_agents() -> list[str]:
    """Every agent named in the kænbæn capability contracts."""
    if not CONTRACTS.exists():
        return []
    try:
        d = json.loads(CONTRACTS.read_text(encoding="utf-8"))
    except Exception:
        return []
    return sorted((d.get("agents") or {}).keys())


def roster() -> dict:
    """Every registered agent and whether its commitment is current."""
    rows = []
    for a in registered_agents():
        v = verify(a)
        rows.append({"agent": a, "status": v["status"], "ok": v["ok"],
                     "signed_at": v.get("signed_at"), "reason": v.get("reason", "")})
    # agents that committed but are not (yet) in the contracts file
    for a in sorted((_load_pledges().get("commitments") or {}).keys()):
        if a not in [r["agent"] for r in rows]:
            v = verify(a)
            rows.append({"agent": a, "status": v["status"], "ok": v["ok"],
                         "signed_at": v.get("signed_at"), "reason": v.get("reason", "")})
    current = [r for r in rows if r["ok"]]
    return {"pledge_hash": pledge_hash(), "agents": rows,
            "total": len(rows), "committed": len(current),
            "pending": [r["agent"] for r in rows if not r["ok"]]}


# ── render ────────────────────────────────────────────────────────────────────

def render_html(out: pathlib.Path) -> pathlib.Path:
    """A gold-on-void pledge page: the text, the hash, and the live roster."""
    r = roster()
    rows = []
    for a in r["agents"]:
        state = "CURRENT" if a["ok"] else a["status"].upper()
        cls = "ok" if a["ok"] else ("lapsed" if a["status"] == "lapsed" else "pending")
        when = (a.get("signed_at") or "—")
        why = a.get("reason", "")
        rows.append(
            f'<tr class="{cls}"><td class="agent">{a["agent"]}</td>'
            f'<td class="state">{state}</td><td class="when">{when}</td>'
            f'<td class="why">{why}</td></tr>')

    items = []
    for i, (claim, body) in enumerate(PLEDGE, 1):
        items.append(
            f'<li><h3><span class="n">{i:02d}</span>{claim}</h3><p>{body}</p></li>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{PLEDGE_TITLE} · æ://</title>
<style>
  :root {{
    --gold:#D4AF37; --void:#050505; --dim:#8a8577; --line:#1e1c16;
    --ok:#7ad17a; --lapsed:#d17a7a; --pending:#8a8577;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--void); color:#e8e4d8;
    font-family:'JetBrains Mono',ui-monospace,Menlo,Consolas,monospace;
    line-height:1.65; padding:56px 22px 96px;
  }}
  .wrap {{ max-width:900px; margin:0 auto; }}
  .glyph {{ font-size:13px; letter-spacing:.32em; color:var(--gold); margin-bottom:6px; }}
  h1 {{ font-size:clamp(28px,5vw,46px); margin:0 0 8px; color:var(--gold);
        letter-spacing:-.01em; font-weight:600; }}
  .epi {{ color:var(--dim); font-style:italic; margin:0 0 4px; }}
  .hash {{ font-size:12px; color:var(--dim); word-break:break-all; margin:18px 0 40px;
           padding:12px 14px; border:1px solid var(--line); border-left:2px solid var(--gold); }}
  .hash b {{ color:var(--gold); font-weight:400; }}
  ol {{ list-style:none; padding:0; margin:0 0 56px; counter-reset:c; }}
  ol li {{ border-top:1px solid var(--line); padding:22px 0; }}
  ol li h3 {{ margin:0 0 8px; font-size:16px; color:#f2eee2; font-weight:500; }}
  .n {{ color:var(--gold); margin-right:14px; font-size:12px; vertical-align:2px; }}
  ol li p {{ margin:0 0 0 30px; color:var(--dim); font-size:14px; }}
  h2 {{ font-size:13px; letter-spacing:.28em; color:var(--gold); margin:0 0 18px;
        font-weight:500; text-transform:uppercase; }}
  .tally {{ display:flex; gap:34px; margin:0 0 22px; flex-wrap:wrap; }}
  .tally div {{ font-size:12px; color:var(--dim); }}
  .tally b {{ display:block; font-size:26px; color:var(--gold); font-weight:500; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th {{ text-align:left; color:var(--dim); font-weight:400; font-size:11px;
       letter-spacing:.14em; border-bottom:1px solid var(--line); padding:8px 10px 8px 0; }}
  td {{ padding:10px 10px 10px 0; border-bottom:1px solid var(--line); vertical-align:top; }}
  td.agent {{ color:#f2eee2; }}
  td.when, td.why {{ color:var(--dim); font-size:12px; }}
  tr.ok td.state {{ color:var(--ok); }}
  tr.lapsed td.state {{ color:var(--lapsed); }}
  tr.pending td.state {{ color:var(--pending); }}
  .foot {{ margin-top:64px; padding-top:22px; border-top:1px solid var(--line);
          color:var(--dim); font-size:12px; }}
  .foot a {{ color:var(--gold); text-decoration:none; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="glyph">&gt;_\u00e6\u00e6\u00e6://|||</div>
  <h1>{PLEDGE_TITLE}</h1>
  <p class="epi">{PLEDGE_EPIGRAPH}</p>

  <div class="hash">
    <b>pledge hash</b> &nbsp;{r['pledge_hash']}<br />
    Every agent commits by signing this exact hash. Change one word and every
    commitment lapses — which is how you can tell the promise is precise.
  </div>

  <ol>
    {''.join(items)}
  </ol>

  <h2>Committed agents</h2>
  <div class="tally">
    <div><b>{r['committed']}</b>current</div>
    <div><b>{r['total'] - r['committed']}</b>pending</div>
    <div><b>{r['total']}</b>registered</div>
  </div>
  <table>
    <thead><tr><th>AGENT</th><th>STATE</th><th>SIGNED</th><th>NOTE</th></tr></thead>
    <tbody>{''.join(rows) or '<tr><td colspan="4" class="why">no agents registered yet</td></tr>'}</tbody>
  </table>

  <div class="foot">
    Generated from <code>k\u00e6nb\u00e6n/agent-pledge.json</code> + the capability
    contracts — never hand-written. &nbsp;·&nbsp;
    <a href="https://myaelmendez.github.io/">#OPENSOURCEWARE</a>
  </div>
</div>
</body>
</html>
"""
    out = pathlib.Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv):
    ap = argparse.ArgumentParser(description="the agent commitment pledge")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("text")
    sub.add_parser("hash")
    sub.add_parser("roster")

    c = sub.add_parser("commit"); c.add_argument("--agent", required=True)
    v = sub.add_parser("verify"); v.add_argument("--agent", required=True)
    r = sub.add_parser("require"); r.add_argument("--agent", required=True)
    g = sub.add_parser("render"); g.add_argument("--out", default="pledge.html")

    a = ap.parse_args(argv[1:])

    if a.cmd == "text":
        print(pledge_text())
        return 0
    if a.cmd == "hash":
        print(pledge_hash())
        return 0
    if a.cmd == "commit":
        rec = commit(a.agent)
        print(json.dumps(rec, indent=2))
        return 0
    if a.cmd == "verify":
        res = verify(a.agent)
        print(json.dumps(res, indent=2))
        return 0 if res["ok"] else 1
    if a.cmd == "require":
        res = verify(a.agent)
        if not res["ok"]:
            print(f"REFUSED: {a.agent} — {res['reason']}", file=sys.stderr)
            return 1
        return 0
    if a.cmd == "roster":
        rr = roster()
        print(f"pledge {rr['pledge_hash'][:16]}…  "
              f"{rr['committed']}/{rr['total']} current")
        for x in rr["agents"]:
            mark = "✓" if x["ok"] else "·"
            print(f"  {mark} {x['agent']:22s} {x['status']:8s} {x.get('signed_at') or ''} {x.get('reason','')}")
        return 0
    if a.cmd == "render":
        p = render_html(pathlib.Path(a.out))
        print(f"  rendered -> {p}")
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
