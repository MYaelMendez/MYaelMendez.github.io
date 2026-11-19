#!/usr/bin/env python3
"""mp4:// — the whole media chain, under one name.

væult named the authority chain: custody → format → gate → authority → contract
→ dispatch → publish → delivery → adoption. Nine links, each answering a failure
the previous one could not.

mp4:// names the media chain, by the same rule:

    intent → spec → board → cast → render → supervision → receipt → publish → adoption

The failure each link answers:

    intent       "make a video" is not a plan            → stages with gates
    spec         a wish is not renderable                → bounded JSON
    board        35 minutes to learn the face is wrong   → 21 seconds, human eyes
    cast         a dome is not a character               → faces, timbres, roles
    render       a picture of a robot is not a robot     → real CAD, real physics
    supervision  a plausible frame is not a good frame   → measured thresholds
    receipt      "it worked" is not evidence             → SHA-256 chain
    publish      a push is not a page                    → live URL, verified
    adoption     my laptop is not your laptop            → harness + spec, public

THE RULE THIS CHAIN EXISTS TO ENFORCE
    The machine gate measures pixels. The human gate judges rightness.
    Both are required. Where a gate exists, pass through it. Where one does
    not, say the check is missing rather than report a pass.

Usage
    python mp4_chain.py chain
    python mp4_chain.py verify
    python mp4_chain.py call <link> <action> [args]
    python mp4_chain.py manifest --out mp4-chain.json
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

SCHEME = "mp4://"
NAME = "mp4"
MEANING = "the whole media chain, under one name"
FLOW = "intent → spec → board → cast → render → supervision → receipt → publish → adoption"
AUTHORITY = "HUMAN://ROOT"

AG = pathlib.Path(os.environ.get("AE_AGENTS", r"C:\æ\agents"))
VID = pathlib.Path(os.environ.get("AE_VIDAEO_DIR", r"C:\æ\vidæo"))
FAC = pathlib.Path(os.environ.get("AE_FACTORY", r"C:\æ\store\mp4-factory-app"))
SITE = pathlib.Path(os.environ.get("AE_SITE", r"C:\æ\github-pages"))
PY = os.environ.get("HERMES_AE_PYTHON", sys.executable)

CHAIN = [
    dict(n=1, id="film", role="intent", answers="which stage, and whose gate",
         path=AG / "film_protocol.py", module="film_protocol", shape="module",
         verbs=["stages", "board", "render", "status", "jobs", "dispatch"]),
    dict(n=2, id="spec", role="format", answers="what the film commands",
         path=AG / "repo_film.py", module="repo_film", shape="module",
         verbs=["facts", "spec_from_facts", "board"]),
    dict(n=3, id="board", role="human gate", answers="is it right, before the spend",
         path=AG / "proof_sheet.py", module="proof_sheet", shape="module",
         verbs=["build_cast", "sheet"], human=True),
    dict(n=4, id="cast", role="performers", answers="who speaks, with what face and timbre",
         path=AG / "robot_face2.py", module="robot_face2", shape="module",
         verbs=["face", "paste_face"]),
    dict(n=5, id="render", role="production", answers="deterministic frames from real CAD",
         path=AG / "charging_bay.py", module="charging_bay", shape="module",
         verbs=["build", "speak", "project", "render"],
         also=[dict(id="studio", path=AG / "asimov_studio3.py", module="asimov_studio3",
                    verbs=["build", "speak", "project", "tablet", "render"])]),
    dict(n=6, id="supervision", role="machine gate", answers="is it real, or a picture of one",
         path=VID / "vidæo.py", module="vidæo", shape="module",
         verbs=["gate_spec", "gate_render", "gate_verify", "cmd_verify"]),
    dict(n=7, id="receipt", role="evidence", answers="what actually happened, hash-chained",
         path=pathlib.Path(os.environ.get("HERMES_HOME", pathlib.Path.home() / ".hermes"))
              / "plugins" / "hermes-asimov" / "render_jobs.py",
         module="render_jobs", shape="module",
         verbs=["launch", "status", "listing", "receipt"]),
    dict(n=8, id="factory", role="throughput", answers="GPU-native scenes at scale",
         path=FAC / "mp4-factory-1080p.mjs", shape="node", verbs=[]),
    dict(n=9, id="publish", role="delivery", answers="a live URL, not a push",
         path=SITE, shape="dir", verbs=[]),
]
BY_ID = {l["id"]: l for l in CHAIN}
for _l in CHAIN:
    for _e in _l.get("also", []):
        BY_ID[_e["id"]] = dict(_e, role=_l["role"], answers=_l["answers"],
                               shape="module", n=_l["n"])


def _load(path: pathlib.Path, module: str):
    """Import by file path. 'æ' in a path is fine for importlib (not for argv)."""
    try:
        spec = importlib.util.spec_from_file_location(f"mp4_{module}", path)
        if spec is None or spec.loader is None:
            return None, "no loader"
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        return mod, None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def link_status(link: dict) -> dict:
    path = pathlib.Path(link["path"])
    out = dict(id=link["id"], role=link["role"], answers=link["answers"],
               path=str(path), exists=path.exists(), shape=link.get("shape", "module"),
               verbs_declared=link.get("verbs", []), verbs_found=[], missing=[],
               ok=False, detail="", human_gate=bool(link.get("human")))
    if not path.exists():
        out["detail"] = "not found"
        return out
    shape = out["shape"]
    if shape == "dir":
        n = len(list(path.glob("*.mp4")))
        out["ok"] = n > 0
        out["detail"] = f"{n} films on the truth surface"
        return out
    if shape == "node":
        out["ok"] = path.stat().st_size > 0
        out["detail"] = f"{path.stat().st_size} B of renderer"
        return out
    mod, err = _load(path, link.get("module", path.stem))
    if mod is None:
        out["detail"] = f"import failed — {err}"
        return out
    declared = link.get("verbs", [])
    out["verbs_found"] = [v for v in declared if hasattr(mod, v)]
    out["missing"] = [v for v in declared if not hasattr(mod, v)]
    out["ok"] = not out["missing"]
    out["detail"] = "all verbs present" if out["ok"] else f"missing: {', '.join(out['missing'])}"
    return out


def verify_chain() -> dict:
    links = [link_status(l) for l in CHAIN]
    for l in CHAIN:
        for extra in l.get("also", []):
            links.append(link_status(dict(extra, role=l["role"], answers=l["answers"],
                                          shape="module", n=l["n"])))
    broken = [l["id"] for l in links if not l["ok"]]
    return dict(scheme=SCHEME, authority=AUTHORITY, chain=links, total=len(links),
                ok=len(links) - len(broken), broken=broken, healthy=not broken,
                rule="The machine gate measures pixels; the human gate judges rightness. "
                     "Both are required.")


def call(link_id: str, action: str | None = None, *args) -> dict:
    """Call one link through the chain entry. Never raises, never grants."""
    link = BY_ID.get(link_id)
    if link is None:
        return dict(ok=False, refused=True, scheme=SCHEME,
                    reason=f"unknown link {link_id!r}", links=list(BY_ID))
    path = pathlib.Path(link["path"])
    if not path.exists():
        return dict(ok=False, refused=True, scheme=SCHEME, link=link_id,
                    reason=f"link missing: {path}")
    if link.get("shape") in ("node", "dir"):
        return dict(ok=False, refused=True, scheme=SCHEME, link=link_id,
                    reason=f"{link['shape']} link is invoked directly, not through call()",
                    path=str(path))
    mod, err = _load(path, link.get("module", path.stem))
    if mod is None:
        return dict(ok=False, refused=True, scheme=SCHEME, link=link_id,
                    reason=f"import failed — {err}")
    fn = getattr(mod, action or "", None)
    if fn is None or not callable(fn):
        return dict(ok=False, refused=True, scheme=SCHEME, link=link_id,
                    reason=f"no verb {action!r}",
                    verbs=[v for v in link.get("verbs", []) if hasattr(mod, v)])
    try:
        res = fn(*args)
    except Exception as e:
        return dict(ok=False, refused=True, scheme=SCHEME, link=link_id,
                    reason=f"{type(e).__name__}: {e}")
    if isinstance(res, dict):
        res.setdefault("scheme", SCHEME)
        res.setdefault("authority", AUTHORITY)
        return res
    return dict(ok=True, scheme=SCHEME, authority=AUTHORITY, link=link_id, result=res)


def manifest() -> dict:
    v = verify_chain()
    return dict(system="æ://", name=NAME, scheme=SCHEME, meaning=MEANING, flow=FLOW,
                authority=AUTHORITY,
                generated=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                healthy=v["healthy"], links_total=v["total"], links_ok=v["ok"],
                broken=v["broken"],
                human_gate="board — a sheet returns approved:false; only the operator flips it",
                rule=v["rule"],
                links=[dict(n=i + 1, **{k: l[k] for k in
                           ("id", "role", "answers", "path", "shape", "verbs_declared",
                            "verbs_found", "ok", "detail", "human_gate")})
                       for i, l in enumerate(v["chain"])],
                self="https://myaelmendez.github.io/mp4-chain.json")


def main(argv=None):
    ap = argparse.ArgumentParser(description="mp4:// — the whole media chain")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("chain")
    sub.add_parser("verify")
    m = sub.add_parser("manifest"); m.add_argument("--out", default=None)
    c = sub.add_parser("call")
    c.add_argument("link"); c.add_argument("action", nargs="?", default=None)
    c.add_argument("args", nargs=argparse.REMAINDER)
    a = ap.parse_args(argv)

    if a.cmd == "call":
        print(json.dumps(call(a.link, a.action, *a.args), ensure_ascii=False, default=str))
        return 0
    if a.cmd == "verify":
        v = verify_chain()
        print(f"  {SCHEME}  {v['ok']}/{v['total']} links answer")
        for l in v["chain"]:
            mark = "✓" if l["ok"] else "✗"
            star = " ★HUMAN" if l["human_gate"] else ""
            print(f"  {mark} {l['id']:12s} {l['role']:12s} {l['detail']}{star}")
        if v["broken"]:
            print(f"  BROKEN: {', '.join(v['broken'])}")
        print(f"  healthy: {v['healthy']}")
        return 0 if v["healthy"] else 1
    if a.cmd == "manifest":
        m = manifest()
        txt = json.dumps(m, indent=2, ensure_ascii=False)
        if a.out:
            p = pathlib.Path(a.out); p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(txt, encoding="utf-8")
            print(f"  {p}  {p.stat().st_size} bytes  {m['links_ok']}/{m['links_total']} links")
        else:
            print(txt)
        return 0
    # default: chain
    print(f"  {SCHEME} — {MEANING}")
    print(f"  {FLOW}\n")
    for l in CHAIN:
        star = " ★" if l.get("human") else "  "
        print(f"  {l['n']}{star} {l['id']:12s} {l['role']:12s} {l['answers']}")
    print("\n  ★ = the human gate. A board returns approved:false.")
    print("  The machine measures pixels; the human judges rightness. Both required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
