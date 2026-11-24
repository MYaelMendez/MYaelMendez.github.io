"""tinyTELEPROMPTER — narrated 9:16 prompt cards powered by tinyVOCA.

Stdlib orchestrator. Builds a self-contained page with TTS-synced lines,
keyboard controls, receipts, and a deterministic script manifest.
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

CLI = ROOT / "scripts" / "tiny_voca_voice.py"
PY = os.environ.get("HERMES_TINY_VOCA_PYTHON") or shutil.which("python3") or sys.executable
DEFAULT_SPEED = 1.25

SCRIPTS = {
    "sovereignty": {
        "title": "Sovereign namespace",
        "subtitle": "One authority across eight domains",
        "lines": [
            {"voice": "F2", "text": "One authority. Many domains."},
            {"voice": "M2", "text": "A E L dot net defines the language."},
            {"voice": "F2", "text": "Command prompt dot A I gives the command."},
            {"voice": "M2", "text": "Private client dot A I holds the signature."},
            {"voice": "F2", "text": "Mobility dot foundation hosts the body."},
            {"voice": "M2", "text": "My A El Mendez dot github dot I O renders the proof."},
            {"voice": "F2", "text": "A store distributes the artifacts."},
            {"voice": "M2", "text": "A A A dot com is the signal. Sovereign dot com is the law."},
        ],
    },
    "asimov-voice-map": {
        "title": "Asimov voice map",
        "subtitle": "Voice is an instrument, not authority",
        "lines": [
            {"voice": "F2", "text": "F two, nous girl, carries human intent. The human remains root."},
            {"voice": "M2", "text": "M two, hermes agent, builds and narrates under approval."},
            {"voice": "F2", "text": "The robot voice uses F two as its source."},
            {"voice": "M2", "text": "It speaks through the body layer. It is an executor, never authority."},
            {"voice": "F2", "text": "Human root to A E to receipt."},
        ],
    },
}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _out(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _fail(message, **extra):
    obj = {"success": False, "error": message, "authority": "HUMAN://ROOT"}
    obj.update(extra)
    _out(obj)
    return 1


def _parse_json(stdout: str) -> dict:
    raw = (stdout or "").strip()
    if not raw:
        return {"success": False, "error": "empty output from tiny-voca CLI"}
    for candidate in (raw, raw.splitlines()[-1]):
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    return {"success": False, "error": "tiny-voca CLI did not emit JSON", "stdout": raw[-400:]}


def _duration(p: Path) -> float:
    with wave.open(str(p), "rb") as w:
        return w.getnframes() / w.getframerate()


def _synthesize(text: str, voice: str, output: Path, speed: float) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [PY, str(CLI), "--text", text, "--voice", voice,
         "--output", str(output), "--speed", str(speed)],
        capture_output=True, text=True, timeout=300,
    )
    result = _parse_json(proc.stdout)
    if proc.returncode != 0 and result.get("success"):
        result["success"] = False
        result["error"] = (proc.stderr or "synthesis failed")[-400:]
    if not result.get("success"):
        raise RuntimeError(result.get("error") or "synthesis failed")
    receipt = result.get("receipt")
    if isinstance(receipt, dict):
        receipt = receipt.get("hash")
    return {
        "voice": paths.canonical_voice(voice),
        "text": text,
        "audio": f"audio/{output.name}",
        "duration_s": round(_duration(output), 3),
        "sha256": _sha(output),
        "receipt": receipt,
    }


def _load_script(name: str) -> dict:
    p = Path(name).expanduser()
    if p.exists():
        data = json.loads(p.read_text(encoding="utf-8"))
        if not data.get("lines"):
            raise ValueError("script JSON must contain a non-empty 'lines' array")
        return {"title": data.get("title", "tinyTELEPROMPTER"),
                "subtitle": data.get("subtitle", "tinyVOCA powered"),
                "lines": data["lines"]}
    if name not in SCRIPTS:
        raise KeyError(f"unknown script {name!r}; available: {list(SCRIPTS)}")
    return SCRIPTS[name]


PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#050505">
<title>__TITLE__ · tinyTELEPROMPTER</title>
<style>
:root{color-scheme:dark;--void:#050505;--card:#0a100e;--line:rgba(0,255,159,.20);--gold:#d4af37;--cyan:#00ccff;--mag:#ff4fd8;--green:#00ff9f;--ice:#85e9fc;--text:#e8f5ee;--muted:#8892b0;--mono:"JetBrains Mono",Consolas,Menlo,monospace}
*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:#000;color:var(--text);font-family:var(--mono)}
body{display:grid;place-items:center;padding:0}
.app{width:min(100vw,56.25dvh);height:min(100dvh,177.78vw);min-height:0;background:var(--void);border:1px solid #173a32;display:flex;flex-direction:column;overflow:hidden}
.top{padding:12px 14px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:flex-start;gap:8px}
.brand{font-size:15px;font-weight:700;color:var(--gold);letter-spacing:.04em}.sub{font-size:10px;color:var(--muted);margin-top:3px}.tag{font-size:10px;color:var(--cyan);text-align:right}
.meter{height:4px;background:#10241f}.meter div{height:100%;width:0;background:var(--green);transition:width .12s linear}
.viewport{position:relative;flex:1;min-height:0;overflow:hidden;background:var(--card)}
.viewport:before{content:"READ LINE";position:absolute;top:42%;left:0;right:0;border-top:1px solid var(--gold);z-index:3;pointer-events:none;font-size:9px;color:var(--gold);letter-spacing:.16em;padding-left:10px;transform:translateY(-14px)}
.viewport:after{content:"";position:absolute;inset:0;background:linear-gradient(var(--void),transparent 20%,transparent 72%,var(--void));pointer-events:none;z-index:2}
.scroll{position:absolute;inset:0;overflow:hidden;padding:8vh 18px 12vh;will-change:transform}
.line{font-size:var(--fs,24px);line-height:1.42;margin:0 0 34px;opacity:.28;color:var(--text);transition:opacity .18s,color .18s;text-wrap:balance}
.line.active{opacity:1;color:var(--ice);text-shadow:0 0 18px rgba(133,233,252,.28)}
.line .voice{display:block;font-size:10px;letter-spacing:.14em;color:var(--muted);margin-bottom:4px}
.line.active .voice{color:var(--mag)}
.controls{padding:10px 12px 12px;border-top:1px solid var(--line);display:grid;gap:8px}
.row{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
button,select{background:#0d1a16;color:var(--text);border:1px solid #245045;border-radius:8px;min-height:42px;padding:8px 10px;font:inherit;font-size:12px;cursor:pointer}
button.primary{background:#0b3b2e;border-color:var(--green);color:var(--green);font-weight:700;flex:1}
button.on{border-color:var(--gold);color:var(--gold)}
select{flex:1;min-width:0}.status{display:flex;justify-content:space-between;gap:8px;font-size:10px;color:var(--muted)}
.foot{font-size:9px;color:var(--muted);text-align:center;letter-spacing:.05em}
.chain{color:var(--green)}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
@media(max-width:480px){.app{height:100dvh;width:min(100vw,56.25dvh);min-height:0}.line{font-size:var(--fs,20px)}}
</style></head><body><main class="app">
<header class="top"><div><div class="brand">&gt;_æ: tinyTELEPROMPTER</div><div class="sub">__SUBTITLE__ · tinyVOCA powered</div></div><div class="tag">9:16 · __LINECOUNT__ lines<br>receipts on</div></header>
<div class="meter"><div id="fill"></div></div>
<section class="viewport" id="viewport"><div class="scroll" id="scroll"></div></section>
<footer class="controls">
  <select id="picker" aria-label="Choose line"></select>
  <div class="row">
    <button id="prev" aria-label="Previous line">◀</button>
    <button id="play" class="primary" aria-label="Play or pause">▶ PLAY</button>
    <button id="next" aria-label="Next line">▶|</button>
    <button id="slower" aria-label="Slower">−</button>
    <button id="faster" aria-label="Faster">+</button>
    <button id="speak" class="on" aria-label="Toggle tinyVOCA voice">VOICE</button>
    <button id="font" aria-label="Cycle font size">Aa</button>
    <button id="reset" aria-label="Reset">↺</button>
  </div>
  <div class="status"><span id="speed">1.00×</span><span id="pos">1 / __LINECOUNT__</span><span id="eta">0s left</span><span id="receipt">HUMAN://ROOT</span></div>
  <div class="foot chain">HUMAN://ROOT → æ → RECEIPT · authority not transferable</div>
</footer></main>
<script>
(function(){'use strict';
var LINES=__LINES__;
var idx=0,rate=1,playing=false,elapsed=0,last=null,voiceOn=true,fsIndex=1,fs=[20,24,28,32];
var viewport=document.getElementById('viewport'),scroll=document.getElementById('scroll'),picker=document.getElementById('picker');
var play=document.getElementById('play'),fill=document.getElementById('fill'),speedEl=document.getElementById('speed');
var posEl=document.getElementById('pos'),etaEl=document.getElementById('eta'),rcptEl=document.getElementById('receipt');
var audio=null;
function fmt(s){s=Math.max(0,Math.round(s));return s<60?s+'s':Math.floor(s/60)+'m'+(s%60)+'s'}
function total(){return LINES.reduce(function(a,l){return a+l.duration_s/rate},0)}
function render(){
  scroll.innerHTML='';
  LINES.forEach(function(l,i){
    var d=document.createElement('div');d.className='line'+(i===idx?' active':'');d.style.setProperty('--fs',fs[fsIndex]+'px');
    var v=document.createElement('span');v.className='voice';v.textContent=l.voice.toUpperCase()+' · '+(i+1);
    d.appendChild(v);d.appendChild(document.createTextNode(l.text));scroll.appendChild(d);
  });
  var active=scroll.children[idx];
  if(active)scroll.style.transform='translateY('+Math.max(0,viewport.clientHeight*.42-active.offsetTop-active.offsetHeight/2)+'px)';
  picker.value=String(idx);posEl.textContent=(idx+1)+' / '+LINES.length;
  rcptEl.textContent=LINES[idx].receipt?String(LINES[idx].receipt).slice(0,12):'HUMAN://ROOT';
  var done=0;for(var i=0;i<idx;i++)done+=LINES[i].duration_s/rate;
  var p=Math.max(0,Math.min(1,(done+Math.min(elapsed,LINES[idx].duration_s/rate))/Math.max(.001,total())));
  fill.style.width=(p*100)+'%';etaEl.textContent=fmt(Math.max(0,total()-done-elapsed))+' left';
}
function stopAudio(){if(audio){audio.pause();audio.currentTime=0;audio=null}}
function speak(){stopAudio();if(!voiceOn)return;audio=new Audio(LINES[idx].audio);audio.playbackRate=rate;audio.play().catch(function(){})}
function go(i){idx=Math.max(0,Math.min(LINES.length-1,i));elapsed=0;render();if(playing)speak()}
function pause(){playing=false;play.textContent='▶ PLAY';stopAudio()}
function tick(ts){
  if(last===null)last=ts;var dt=Math.min(.08,(ts-last)/1000);last=ts;
  if(playing){elapsed+=dt*rate;var limit=LINES[idx].duration_s;if(elapsed>=limit){if(idx<LINES.length-1)go(idx+1);else{pause();elapsed=limit}}render()}
  requestAnimationFrame(tick);
}
LINES.forEach(function(l,i){var o=document.createElement('option');o.value=String(i);o.textContent=(i+1)+' · '+l.voice+' · '+l.text.slice(0,26);picker.appendChild(o)});
play.addEventListener('click',function(){playing=!playing;play.textContent=playing?'Ⅱ PAUSE':'▶ PLAY';if(playing){last=null;speak()}else stopAudio()});
document.getElementById('next').addEventListener('click',function(){go(idx+1)});
document.getElementById('prev').addEventListener('click',function(){go(idx-1)});
document.getElementById('slower').addEventListener('click',function(){rate=Math.max(.5,rate-.25);speedEl.textContent=rate.toFixed(2)+'×';if(audio)audio.playbackRate=rate;render()});
document.getElementById('faster').addEventListener('click',function(){rate=Math.min(2,rate+.25);speedEl.textContent=rate.toFixed(2)+'×';if(audio)audio.playbackRate=rate;render()});
document.getElementById('speak').addEventListener('click',function(e){voiceOn=!voiceOn;e.currentTarget.classList.toggle('on',voiceOn);if(!voiceOn)stopAudio()});
document.getElementById('font').addEventListener('click',function(){fsIndex=(fsIndex+1)%fs.length;render()});
document.getElementById('reset').addEventListener('click',function(){pause();go(0)});
picker.addEventListener('change',function(){go(Number(picker.value))});
document.addEventListener('keydown',function(e){
 if(e.code==='Space'){e.preventDefault();play.click()}
 if(e.code==='ArrowRight')go(idx+1);if(e.code==='ArrowLeft')go(idx-1);
 if(e.key==='+'||e.key==='=')document.getElementById('faster').click();if(e.key==='-')document.getElementById('slower').click();
 if(e.key==='r'||e.key==='R')document.getElementById('reset').click();
});
window.addEventListener('resize',render);document.addEventListener('visibilitychange',function(){if(document.hidden)pause()});
render();requestAnimationFrame(tick);
})();
</script></body></html>
'''


def _page(meta: dict, items: list) -> str:
    payload = json.dumps([{
        "voice": i["voice"], "text": i["text"], "audio": i["audio"],
        "duration_s": i["duration_s"], "receipt": i.get("receipt"),
    } for i in items], ensure_ascii=False)
    return (PAGE.replace("__TITLE__", html.escape(meta["title"]))
                .replace("__SUBTITLE__", html.escape(meta["subtitle"]))
                .replace("__LINECOUNT__", str(len(items)))
                .replace("__LINES__", payload))


def build(name: str, out: Path, speed: float):
    meta = _load_script(name)
    out.mkdir(parents=True, exist_ok=True)
    audio_dir = out / "audio"
    audio_dir.mkdir(exist_ok=True)
    items = []
    for n, line in enumerate(meta["lines"]):
        items.append(_synthesize(line["text"], line["voice"], audio_dir / f"{n:02d}.wav", speed))
    index = out / "index.html"
    index.write_text(_page(meta, items), encoding="utf-8")
    manifest = {
        "authority": "HUMAN://ROOT",
        "product": "tiny-voca-voice",
        "capability": "tiny-teleprompter",
        "script": name,
        "title": meta["title"],
        "speed": speed,
        "lines": items,
        "index_sha256": _sha(index),
    }
    (out / "script.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        receipt = paths.append_custom_receipt({
            "action": paths.ACTION_PROMPT_BUILD,
            "script": name,
            "lines": len(items),
            "total_duration_s": round(sum(i["duration_s"] for i in items), 3),
            "index_sha256": _sha(index),
            "output": str(out),
        })
    except Exception as exc:
        receipt = None
    _out({"success": True, "action": paths.ACTION_PROMPT_BUILD,
          "authority": "HUMAN://ROOT", "script": name, "output": str(out),
          "index": str(index), "lines": len(items), "receipt": receipt})


def main():
    p = argparse.ArgumentParser(description="Build a tinyVOCA-powered teleprompter.")
    p.add_argument("--op", choices=("list", "build"), required=True)
    p.add_argument("--script", default="sovereignty")
    p.add_argument("--out", default=None)
    p.add_argument("--speed", type=float, default=DEFAULT_SPEED)
    args = p.parse_args()
    if args.op == "list":
        _out({"success": True, "authority": "HUMAN://ROOT",
              "scripts": [{"id": k, "title": v["title"], "lines": len(v["lines"])}
                          for k, v in SCRIPTS.items()]})
        return 0
    if not args.out:
        return _fail("--out is required for build")
    try:
        return build(args.script, Path(args.out).expanduser(), args.speed)
    except Exception as exc:
        return _fail(f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    raise SystemExit(main())
