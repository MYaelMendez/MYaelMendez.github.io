"""Asimov robot stick-lesson builder for tiny-voca-voice.

Stdlib-only orchestrator: copies the unmodified upstream stick-scene runtime,
writes Asimov lesson pages, synthesizes tiny-voca narration, and records one
LESSON://BUILD receipt in the shared hash-chained ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import shutil
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import tiny_voca_paths as paths  # noqa: E402

ASSETS = ROOT / "assets" / "stick-scene"
IDENTITY = ROOT / "identity.json"
SPEAK = ROOT / "scripts" / "tiny_voca_voice.py"
PY = os.environ.get("HERMES_TINY_VOCA_PYTHON") or shutil.which("python3") or sys.executable
DEFAULT_SPEED = 1.25

LESSONS = {
    "asimov-authority": {
        "title": "Authority command",
        "chain": "commandprompt.ai × privateclient.ai",
        "scene": "asimov-authority",
        "label": "A human types a command, approves it privately, and Asimov acts.",
        "lines": [
            {"voice": "M2", "text": "Lesson one. The human types the command. Private client holds the signature. Only then does Asimov move."},
            {"voice": "F2", "text": "Authority is not transferable."},
        ],
    },
    "asimov-verbs": {
        "title": "Governed verbs",
        "chain": "æ Robot Verbs",
        "scene": "asimov-verbs",
        "label": "A human pulls the governed verbs lever and Asimov balances and steps.",
        "lines": [
            {"voice": "M2", "text": "Lesson two. Stand, damp, balance, set velocity, set joints. Every verb crosses the policy gate."},
        ],
    },
    "asimov-twin": {
        "title": "USD twin",
        "chain": "asimov-avatar.usda",
        "scene": "asimov-twin",
        "label": "A human feeds qpos into the Asimov USD twin and the robot walks.",
        "lines": [
            {"voice": "F2", "text": "Lesson three. The USD twin makes the robot visible."},
            {"voice": "M2", "text": "Human root to æ to receipt. The twin is proof, not authority."},
        ],
    },
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _out(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _fail(message, **extra):
    obj = {"success": False, "error": message, "authority": "HUMAN://ROOT"}
    obj.update(extra)
    _out(obj)
    return 1


def _duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def _parse_json(stdout):
    raw = (stdout or "").strip()
    if not raw:
        return {"success": False, "error": "empty output from tiny-voca script"}
    for candidate in (raw, raw.splitlines()[-1]):
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    return {"success": False, "error": "tiny-voca script did not emit JSON", "stdout": raw[-500:]}


def _synthesize(text: str, voice: str, output: Path, speed: float):
    output.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [PY, str(SPEAK), "--text", text, "--voice", voice,
         "--output", str(output), "--speed", str(speed)],
        capture_output=True, text=True, timeout=600,
    )
    result = _parse_json(proc.stdout)
    if proc.returncode != 0 and result.get("success"):
        result["success"] = False
        result["error"] = (proc.stderr or "synthesis failed")[-500:]
    if not result.get("success"):
        raise RuntimeError(result.get("error") or "synthesis failed")
    return {
        "voice": paths.canonical_voice(voice),
        "text": text,
        "wav": str(output.relative_to(output.parents[1])),
        "duration_s": round(_duration(output), 3),
        "sha256": _sha(output),
        "receipt": result.get("receipt"),
    }


def _html(lesson_ids, cards):
    parts = []
    for lid in lesson_ids:
        spec = LESSONS[lid]
        parts.append(f"""
    <figure>
      <div class="tag">{html.escape(spec['chain'])}</div>
      <stick-scene scene="{html.escape(spec['scene'])}" play="view" no-font
        label="{html.escape(spec['label'])}" style="height:230px"></stick-scene>
      <figcaption><b>{html.escape(spec['title'])}</b>
        <span>{html.escape(spec['label'])}</span>""")
        for number, line in enumerate(cards[lid]):
            parts.append(
                f'<audio controls preload="none" src="audio/{number}.wav"></audio>'
                f'<span>{html.escape(line["voice"].upper())} · {html.escape(line["text"])}</span>'
            )
        parts.append("</figcaption></figure>")
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>&gt;_æ: ASIMOV STICK LESSONS</title>
<style>
:root{--bg:#050a08;--paper:#fbfbf9;--green:#00ff9f;--cyan:#00ccff;--gold:#d4af37;--muted:#8892b0;--line:rgba(0,255,159,.2);--mono:"JetBrains Mono",Consolas,monospace}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:#d7f5e8;font-family:var(--mono);line-height:1.5}
.wrap{max-width:960px;margin:0 auto;padding:24px 20px 56px}header{padding:36px 0 22px;border-bottom:1px solid var(--line)}
h1{margin:0;color:#eafff5;font-size:clamp(1.8rem,5vw,3rem)}.lede{color:#9fd8c0;max-width:70ch}
.chain{display:inline-block;margin-top:12px;padding:7px 12px;border:1px solid rgba(212,175,55,.5);color:var(--gold);font-size:13px}
.voicemap{margin-top:10px;color:var(--muted);font-size:12px}
figure{margin:18px 0;background:var(--paper);border:1px solid #d8ddd8;border-radius:12px;padding:16px 18px;color:#141414}
.tag{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6f817c;margin-bottom:8px}
stick-scene{display:block;width:100%;height:230px;background:white;border-radius:8px;cursor:pointer;background-image:radial-gradient(#e6e6e6 1px,transparent 1.2px);background-size:14px 14px}
figcaption b{font-size:15px}figcaption span{display:block;color:#5d6d66;font-size:13px;margin-top:4px}
audio{width:100%;height:32px;margin-top:10px}footer{margin-top:36px;border-top:1px solid var(--line);padding-top:16px;color:var(--muted);font-size:12px}
a{color:var(--cyan)}
</style></head><body><div class="wrap">
<header><h1>&gt;_æ: ASIMOV STICK LESSONS</h1>
<p class="lede">Local, self-hosted narration over the upstream stick-scene runtime. Three lessons: command, governed verbs, and the USD twin.</p>
<div class="chain">HUMAN://ROOT → æ → RECEIPT</div>
<div class="voicemap">F2 · nous girl → human intent &nbsp;|&nbsp; M2 · hermes-agent → agent runtime &nbsp;|&nbsp; ROBOT · asimov-robot → robot body</div></header>
<main>""" + "".join(parts) + """</main>
<footer>Built on <a href="https://github.com/nilbuild/stick-scene">nilbuild/stick-scene</a>, MIT © Kamran Ahmed. Runtime copied unchanged. Narration by tiny-voca with hash-chained receipts. Independent build; no institutional endorsement claimed.</footer>
</div>
<script src="stick.js" defer></script>""" + "".join(
        f'<script src="scenes/{html.escape(LESSONS[lid]["scene"])}.js" defer></script>' for lid in lesson_ids
    ) + "</body></html>\n"


def build(lesson: str, out: Path, speed: float):
    if not ASSETS.exists():
        return _fail("stick-scene assets missing", expected=str(ASSETS))
    lesson_ids = list(LESSONS) if lesson in ("all", "", None) else [lesson]
    unknown = [lid for lid in lesson_ids if lid not in LESSONS]
    if unknown:
        return _fail("unknown lesson", unknown=unknown, available=list(LESSONS))
    out.mkdir(parents=True, exist_ok=True)
    audio_dir = out / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    scene_dir = out / "scenes"
    scene_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(ASSETS / "stick.js", out / "stick.js")
    shutil.copy2(ASSETS / "LICENSE", out / "LICENSE")
    for lid in lesson_ids:
        scene = LESSONS[lid]["scene"]
        shutil.copy2(ASSETS / "scenes" / f"{scene}.js", scene_dir / f"{scene}.js")

    cards = {}
    numbered = []
    for lid in lesson_ids:
        lines = []
        for index, line in enumerate(LESSONS[lid]["lines"]):
            name = f"{lid}-{index:02d}.wav"
            info = _synthesize(line["text"], line["voice"], audio_dir / name, speed)
            info["file"] = f"audio/{name}"
            lines.append(info)
            numbered.append(info)
        cards[lid] = lines

    index = out / "index.html"
    index.write_text(_html(lesson_ids, cards), encoding="utf-8")
    manifest = {
        "authority": "HUMAN://ROOT",
        "product": "tiny-voca-voice",
        "capability": "asimov-robot-stick-lessons",
        "identity": json.loads(IDENTITY.read_text(encoding="utf-8")) if IDENTITY.exists() else None,
        "lesson": lesson or "all",
        "lessons": lesson_ids,
        "speed": speed,
        "runtime": "nilbuild/stick-scene",
        "runtime_sha256": _sha(out / "stick.js"),
        "narration": numbered,
        "files": {"index": str(index.name), "sha256": _sha(index)},
    }
    (out / "lesson.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        receipt = paths.append_custom_receipt({
            "action": paths.ACTION_LESSON_BUILD,
            "lesson": lesson or "all",
            "lessons": lesson_ids,
            "output": str(out),
            "sha256": _sha(index),
            "narration_count": len(numbered),
            "runtime_sha256": manifest["runtime_sha256"],
        })
    except Exception as exc:
        receipt = None
    _out({"success": True, "action": paths.ACTION_LESSON_BUILD, "authority": "HUMAN://ROOT",
          "lesson": lesson or "all", "lessons": lesson_ids, "output": str(out),
          "index": str(index), "narration": numbered, "receipt": receipt})


def main():
    p = argparse.ArgumentParser(description="Build narrated Asimov stick lessons.")
    p.add_argument("--op", choices=("list", "build"), required=True)
    p.add_argument("--lesson", default="all")
    p.add_argument("--out", default=None)
    p.add_argument("--speed", type=float, default=DEFAULT_SPEED)
    args = p.parse_args()
    if args.op == "list":
        _out({"success": True, "authority": "HUMAN://ROOT",
              "lessons": [{"id": k, "title": v["title"], "scene": v["scene"],
                           "lines": len(v["lines"])} for k, v in LESSONS.items()]})
        return 0
    if not args.out:
        return _fail("--out is required for build")
    try:
        return build(args.lesson, Path(args.out).expanduser(), args.speed)
    except Exception as exc:
        return _fail(f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    raise SystemExit(main())
