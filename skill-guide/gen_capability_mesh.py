#!/usr/bin/env python3
"""
gen_capability_mesh.py — regenerate capability-mesh.json from the live skill
library + a live GPU probe.

Scans every SKILL.md in the Hermes skills tree, classifies each skill by the
compute tier it needs (gpu / local / cpu), probes the local GPU, and writes
the payload the capability-mesh.html surface reads.

Usage:
    python gen_capability_mesh.py                     # default paths
    python gen_capability_mesh.py --out PATH          # custom output
    python gen_capability_mesh.py --no-probe          # skip nvidia-smi
    python gen_capability_mesh.py --print             # also print a summary

The skill root is discovered the same way Hermes does:
    $HERMES_HOME/skills  →  ~/AppData/Local/hermes/skills (Windows)
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import time
from collections import Counter

# ── skill discovery ───────────────────────────────────────────────────────────

def skills_root() -> pathlib.Path:
    """Resolve the live Hermes skills directory."""
    home = os.environ.get("HERMES_HOME")
    if home:
        p = pathlib.Path(home) / "skills"
        if p.is_dir():
            return p
    # Windows default
    cand = pathlib.Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / "skills"
    if cand.is_dir():
        return cand
    # POSIX default
    cand = pathlib.Path.home() / ".hermes" / "skills"
    if cand.is_dir():
        return cand
    raise SystemExit("gen_capability_mesh: cannot find the Hermes skills root "
                     "(set HERMES_HOME or pass --skills)")


FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def parse_frontmatter(text: str) -> dict:
    m = FM_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def scan_skills(root: pathlib.Path) -> list[dict]:
    out = []
    for skill_md in root.rglob("SKILL.md"):
        rel = skill_md.parent.relative_to(root)
        parts = rel.parts
        if not parts or any(p.startswith(".") for p in parts):
            continue
        name = parts[-1]
        category = parts[0] if len(parts) > 1 else "single"
        try:
            text = skill_md.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        fm = parse_frontmatter(text)
        body = FM_RE.sub("", text, count=1)
        out.append({
            "name": fm.get("name", name),
            "category": category,
            "dir": str(rel).replace("\\", "/"),
            "description": fm.get("description", ""),
            "chars": len(text),
            "lines": text.count("\n") + 1,
            "refs": len(list((skill_md.parent / "references").glob("*"))) if (skill_md.parent / "references").is_dir() else 0,
            "scripts": len(list((skill_md.parent / "scripts").glob("*"))) if (skill_md.parent / "scripts").is_dir() else 0,
            "templates": len(list((skill_md.parent / "templates").glob("*"))) if (skill_md.parent / "templates").is_dir() else 0,
        })
    return out


# ── compute classification ────────────────────────────────────────────────────
# The tier is a ROUTING decision: where must this skill run?
#   gpu   → needs the RTX leaf (victus)
#   local → must run on this machine (custody, no cloud)
#   cpu   → runs anywhere (cheapest)

CATEGORY_TIER = {
    # GPU-bound: training, inference, quantization, generation
    "mlops": "gpu",
    "cuda": "gpu",
    "data-science": "gpu",
    # media + creative are MIXED — decided per-skill by keyword (default cpu)
    "media": "cpu",
    "creative": "cpu",
    # local-only: custody, the sovereign stack, agent internals
    "sovereign": "local",
    "agentic": "local",
    "hermes": "local",
    "security": "local",
    "local-secret-source": "local",
    "mcp": "local",
    "autonomous-ai-agents": "local",
    "desktop": "local",
    "hermes-native": "local",
    "hermes-operator-grammar": "local",
    # cpu: everything else
    "software-development": "cpu",
    "research": "cpu",
    "productivity": "cpu",
    "business": "cpu",
    "github": "cpu",
    "web": "cpu",
    "email": "cpu",
    "note-taking": "cpu",
    "devops": "cpu",
    "gaming": "cpu",
    "smart-home": "cpu",
    "social-media": "cpu",
    "leisure": "cpu",
    "dogfood": "cpu",
    "single": "cpu",
}

# Keyword overrides. A skill's NAME + description promotes it to gpu ONLY when
# the tool genuinely needs the GPU — not merely because it mentions a model.
# Bare "torch"/"transformers" is too broad (a doc skill can name them).
GPU_KEYWORDS = (
    "cuda", "gpu", "rtx", "nvidia", "nvenc", "cublas", "cupy", "tensorrt",
    "llama.cpp", "llama-cpp", "gguf", "quantization", "vllm", "triton",
    "flash-attention", "fsdp", "deepseek", "diffusion", "stable-diffusion",
    "comfyui", "musicgen", "audiocraft", "whisper", "segment-anything",
    "sam", "lora", "peft", "qlora", "finetun", "grpo", "dpo", "rlhf",
    "axolotl", "unsloth", "torchtitan", "nemo-curator", "sparse-autoencoder",
    "obliteratus", "tensorrt", "matmul", "shader", "webgpu", "manim",
)
LOCAL_KEYWORDS = (
    "vault", "væult", "secret", "custody", "sovereign", "glocal", "chassis",
    "conductor", "private", "local-secret", "mesh", "victus", "leaf",
)


def classify(skill: dict) -> str:
    name = skill["name"].lower()
    desc = (skill.get("description") or "").lower()
    hay = name + " " + desc
    cat = skill["category"]

    # explicit local wins (custody cannot leave the machine)
    if any(k in name for k in LOCAL_KEYWORDS):
        return "local"
    if cat in ("sovereign", "security", "local-secret-source", "agentic", "hermes"):
        return "local"
    # gpu keywords promote — match on the skill NAME first (strong signal),
    # then the description (weak signal, only for gpu-native categories)
    if any(k in name for k in GPU_KEYWORDS):
        return "gpu"
    if cat in ("mlops", "cuda", "media", "data-science", "creative") and any(k in hay for k in GPU_KEYWORDS):
        return "gpu"
    return CATEGORY_TIER.get(cat, "cpu")


TIER_INFO = {
    "gpu":   {"label": "GPU",   "color": "#00ff9d", "node": "victus", "desc": "Needs the RTX leaf"},
    "local": {"label": "LOCAL", "color": "#D4AF37", "node": "victus", "desc": "Runs on this machine"},
    "cpu":   {"label": "CPU",   "color": "#00ccff", "node": "any",    "desc": "Runs anywhere"},
}


# ── GPU probe ─────────────────────────────────────────────────────────────────

def probe_gpu() -> dict:
    """Live nvidia-smi probe. Falls back to the last known values."""
    fallback = {"name": "NVIDIA GeForce RTX 3050 6GB Laptop GPU", "vram_total": 6144,
                "vram_used": 0, "util": 0, "cc": "8.6", "temp": None, "power": None}
    try:
        r = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=name,memory.total,memory.used,utilization.gpu,compute_cap,temperature.gpu,power.draw",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode != 0 or not r.stdout.strip():
            return fallback
        parts = [p.strip() for p in r.stdout.strip().splitlines()[0].split(",")]
        return {
            "name": parts[0],
            "vram_total": int(float(parts[1])),
            "vram_used": int(float(parts[2])),
            "util": int(float(parts[3])),
            "cc": parts[4],
            "temp": int(float(parts[5])) if parts[5] not in ("", "[N/A]") else None,
            "power": float(parts[6]) if parts[6] not in ("", "[N/A]") else None,
        }
    except Exception:
        return fallback


# ── build ─────────────────────────────────────────────────────────────────────

def build(skills: list[dict], gpu: dict, probe: bool) -> dict:
    payload_skills = []
    for s in skills:
        tier = classify(s)
        payload_skills.append({
            "name": s["name"],
            "cat": s["category"],
            "tier": tier,
            "desc": (s.get("description") or "")[:140],
            "scripts": s.get("scripts", 0),
            "refs": s.get("refs", 0),
            "lines": s.get("lines", 0),
            "chars": s.get("chars", 0),
        })

    nodes = [
        {
            "id": "victus", "name": "Victus · teknium", "role": "RTX leaf",
            "gpu": gpu["name"].split(" Laptop")[0] if gpu.get("name") else "RTX 3050 6GB",
            "vram_total": gpu.get("vram_total", 6144), "vram_used": gpu.get("vram_used", 0),
            "cc": gpu.get("cc", "8.6"), "util": gpu.get("util", 0),
            "temp": gpu.get("temp"), "power": gpu.get("power"),
            "status": "local", "location": "this machine",
        },
        {"id": "droplet", "name": "Droplet", "role": "backbone broker", "gpu": None,
         "vram_total": 0, "vram_used": 0, "status": "remote", "location": "sjc"},
        {"id": "cloud", "name": "Nous Cloud", "role": "gateway agents", "gpu": None,
         "vram_total": 0, "vram_used": 0, "status": "cloud", "location": "portal.nousresearch.com"},
    ]

    schemes = [
        {"scheme": "pc://inference", "node": "victus", "desc": "RTX 3050 GGUF inference · -ngl 99", "tier": "gpu"},
        {"scheme": "pc://matmul", "node": "victus", "desc": "GPU matrix multiply", "tier": "gpu"},
        {"scheme": "pc://probe", "node": "victus", "desc": "GPU probe · live telemetry", "tier": "gpu"},
        {"scheme": "+æ://victus", "node": "victus", "desc": "This sovereign compute node", "tier": "local"},
        {"scheme": "+æ://vps", "node": "droplet", "desc": "Backbone node status", "tier": "cpu"},
        {"scheme": "+æ://secrets", "node": "victus", "desc": "Secret broker · local custody", "tier": "local"},
        {"scheme": "væult://", "node": "victus", "desc": "Sovereign vault", "tier": "local"},
        {"scheme": "NVIDIA://c2", "node": "victus", "desc": "GeForce C2 surface", "tier": "gpu"},
    ]

    counts = Counter(s["tier"] for s in payload_skills)

    return {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "probe": probe,
        "skills": payload_skills,
        "tiers": TIER_INFO,
        "nodes": nodes,
        "schemes": schemes,
        "summary": {
            "total_skills": len(payload_skills),
            "gpu": counts.get("gpu", 0),
            "local": counts.get("local", 0),
            "cpu": counts.get("cpu", 0),
            "executable": sum(1 for s in payload_skills if s["scripts"] > 0),
            "nodes": len(nodes),
            "categories": len({s["cat"] for s in payload_skills}),
        },
    }


def main():
    ap = argparse.ArgumentParser(description="Regenerate capability-mesh.json")
    ap.add_argument("--out", default=str(pathlib.Path(r"C:\æ\skill-guide\capability-mesh.json")))
    ap.add_argument("--skills", default=None, help="override the skills root")
    ap.add_argument("--no-probe", action="store_true", help="skip nvidia-smi")
    ap.add_argument("--print", dest="do_print", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(args.skills) if args.skills else skills_root()
    skills = scan_skills(root)
    if not skills:
        raise SystemExit(f"gen_capability_mesh: no SKILL.md found under {root}")

    gpu = {"name": "NVIDIA GeForce RTX 3050 6GB Laptop GPU", "vram_total": 6144, "vram_used": 0, "cc": "8.6"}
    if not args.no_probe:
        gpu = probe_gpu()

    payload = build(skills, gpu, probe=not args.no_probe)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    s = payload["summary"]
    print(f"gen_capability_mesh: wrote {out}")
    print(f"  skills   : {s['total_skills']}  (gpu {s['gpu']} · local {s['local']} · cpu {s['cpu']})")
    print(f"  executable: {s['executable']}")
    print(f"  nodes    : {s['nodes']}  ·  categories: {s['categories']}")
    if payload["probe"]:
        n = payload["nodes"][0]
        print(f"  gpu      : {n['gpu']} · cc {n['cc']} · {n['vram_used']}/{n['vram_total']} MiB · {n['util']}% util")
    if args.do_print:
        print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
