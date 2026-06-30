---
name: startabusiness
description: "æ://#startabusiness→ — Generate a personalized agentic.html sovereign business page. One command, one person, full agency. Self-hosted from æ.store."
version: 2.0.0
author: Yæl Méndez × Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [business, startup, stripe, daollc, agents, sovereign, æ]
    homepage: https://æ.store
    source: https://æ.store/SKILL.md
---

# >_æ:#startabusiness→

Generate a personalized **agentic.html** — a sovereign business page — for any user starting an agentic one-person company. Self-contained and self-hosted from **æ.store** (the App Store for Robots).

## Install (sovereign >link)

```bash
hermes skills install https://æ.store/SKILL.md
```

No GitHub. No middleman. The skill distributes from the namespace itself.

## Trigger Conditions

- User says "start a business", "form an LLC", "one person company", "#startabusiness"
- User wants an agentic storefront or sovereign business page
- User invokes `>_æ:#startabusiness→` or asks about æ.store / DAOLLC formation

## The æ:// Protocol Stack

```
>_æ:  →  sovereign agent protocol     →  æ.store (the namespace)
>_h:  →  hermes (Nous Research)        →  intent routing
>_n:  →  nvidia (NemoClaw)             →  compute
>_$:  →  stripe                        →  payments
>_:   →  the customer                  →  it's always about them
```

## Execution Sequence

### Step 1: Gather Identity (conversational)

1. **Name** — who are you?
2. **Business name** — what's the company called?
3. **Glyph** — pick your symbol (letter/emoji/char — your `>_[x]:` prompt). NEVER default to æ; that's Yæl's.
4. **Business type** — what do you do / sell / build?
5. **Agents** — which agents power it? (defaults: hermes routing, claude inference)
6. **Domain** — have one? (optional)

### Step 2: Generate agentic.html

Build a single self-contained HTML file. **Two design modes** — ask or infer:

**MODE A — GOLD SOVEREIGN (default, æ.store house style):**
- `--void:#050505` `--gold:#D4AF37` `--neon:#00ff9d` `--ink:#f0ece4`
- Orbitron (700/900) headings + JetBrains Mono body
- Canvas neural-mesh background (animated gold particles + connecting lines)
- Scanline + radial vignette overlays
- Sharp edges (border-radius:0 on chassis), gold borders with glow
- Three-panel banner: LEFT identity (glyph + name + live chip) | CENTER headline (title + tagline + pills) | RIGHT CTA (Doola button + domain links)
- Bottom scrolling ticker log
- See "GOLD TEMPLATE" below — copy and reskin with user's identity.

**MODE B — TERMINAL BOOT (alt):**
- Dark `#0a0a0c`, cyan `#00e5ff`, stripe purple `#635bff`, green `#00ff88`, gold `#ffd700`
- 8-step animated execution sequence + stripe block + agent roster + terminal log
- JetBrains Mono throughout, 2px grid gaps

### Step 3: Save, Preview, Deliver

- Save as `agentic.html` in the working directory
- Serve locally (`python -m http.server`) + browser preview to verify render
- Confirm: mesh animates, CTA links to Doola, ticker scrolls, responsive

### Step 4: Next Steps for the User

1. **Form the DAOLLC** → https://partnersps.doola.com/hhsoqhb23250 (Wyoming DAO LLC via Doola)
2. **Activate Stripe** → payment rails
3. **Deploy** → host at their domain or æ.store
4. **Join** → X community "æ store LLM store"

## GOLD TEMPLATE (reference — reskin per user)

```html
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<title>{{BIZ}} • #STARTABUSINESS</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet"/>
<style>
:root{--void:#050505;--gold:#D4AF37;--gold-glow:rgba(212,175,55,.32);--neon:#00ff9d;--ink:#f0ece4;--muted:rgba(240,236,228,.38);--border:rgba(212,175,55,.16);--border-hot:rgba(212,175,55,.5)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100dvh;overflow:hidden;background:var(--void);display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace}
canvas#mesh{position:fixed;inset:0;z-index:0}
.scan{position:fixed;inset:0;z-index:1;pointer-events:none;background:repeating-linear-gradient(transparent 0 2px,rgba(212,175,55,.012) 2px 4px)}
.vig{position:fixed;inset:0;z-index:2;pointer-events:none;background:radial-gradient(ellipse at center,transparent 40%,rgba(5,5,5,.9) 100%)}
.banner{position:relative;z-index:10;width:min(100vw,640px);aspect-ratio:16/5;background:rgba(5,5,5,.82);border:1px solid var(--border-hot);overflow:hidden;display:flex;align-items:stretch;box-shadow:0 0 60px rgba(212,175,55,.12)}
.banner::after{content:'';position:absolute;inset:0;pointer-events:none;border-top:1px solid rgba(212,175,55,.6);border-bottom:1px solid rgba(212,175,55,.6)}
.b-left{flex-shrink:0;width:22%;border-right:1px solid var(--border);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;background:linear-gradient(135deg,rgba(212,175,55,.06),transparent);z-index:1}
.b-glyph{font-size:clamp(22px,4vw,38px);filter:drop-shadow(0 0 10px var(--gold-glow));animation:breathe 4s ease-in-out infinite}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
.b-name{font-family:'Orbitron';font-size:clamp(10px,1.8vw,16px);font-weight:900;letter-spacing:2px;color:var(--gold);text-shadow:0 0 10px var(--gold-glow);text-align:center;line-height:1.1}
.b-sub{font-size:clamp(6px,1vw,8px);letter-spacing:2px;color:var(--muted);text-transform:uppercase;text-align:center}
.live-chip{display:flex;align-items:center;gap:4px;padding:2px 8px;border-radius:999px;border:1px solid rgba(0,255,157,.2);font-size:7px;letter-spacing:1px;color:var(--neon)}
.live-dot{width:5px;height:5px;border-radius:50%;background:var(--neon);box-shadow:0 0 6px var(--neon);animation:pulse 1.6s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.2}}
.b-center{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:clamp(3px,.8vh,7px);text-align:center;z-index:1}
.b-title{font-family:'Orbitron';font-weight:900;font-size:clamp(20px,4.5vw,42px);letter-spacing:clamp(2px,.5vw,5px);color:var(--gold);text-shadow:0 0 22px var(--gold-glow)}
.b-tagline{font-size:clamp(9px,1.6vw,14px);line-height:1.3;color:var(--ink)}
.b-tagline em{font-style:normal;color:var(--gold)}
.b-pills{display:flex;gap:clamp(4px,.8vw,8px);flex-wrap:wrap;justify-content:center}
.b-pill{font-size:clamp(6px,.9vw,8px);letter-spacing:1.5px;padding:2px 8px;border-radius:999px;border:1px solid var(--border);color:var(--muted);text-transform:uppercase}
.b-pill.hot{border-color:rgba(212,175,55,.35);color:var(--gold)}
.b-right{flex-shrink:0;width:24%;border-left:1px solid var(--border);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:clamp(4px,.8vh,8px);background:linear-gradient(225deg,rgba(212,175,55,.07),transparent);z-index:1;padding:0 clamp(8px,1.5vw,16px)}
.cta-main{display:block;width:100%;padding:clamp(8px,1.5vh,14px);background:var(--gold);color:#000;font-family:'Orbitron';font-weight:900;font-size:clamp(7px,1.1vw,10px);letter-spacing:1px;text-align:center;text-decoration:none;border-radius:6px;box-shadow:0 0 20px rgba(212,175,55,.25);transition:all .2s;line-height:1.3}
.cta-main:hover{background:#e8c547;transform:translateY(-1px)}
.cta-label{font-size:7px;letter-spacing:1.5px;color:rgba(212,175,55,.35);text-transform:uppercase}
.cta-links{display:flex;gap:6px}
.cta-link{flex:1;padding:6px;text-align:center;border:1px solid var(--border);border-radius:4px;color:var(--muted);font-size:6px;text-decoration:none}
.b-log{position:absolute;bottom:0;left:22%;right:24%;height:clamp(18px,3vh,24px);border-top:1px solid var(--border);background:rgba(0,0,0,.5);overflow:hidden;display:flex;align-items:center;z-index:2}
.log-ticker{display:flex;gap:32px;white-space:nowrap;font-size:clamp(7px,.9vw,9px);color:rgba(212,175,55,.4);letter-spacing:1px;animation:ticker 28s linear infinite}
@keyframes ticker{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.log-ticker span{color:var(--neon)}.log-ticker b{color:var(--gold)}
</style></head><body>
<canvas id="mesh"></canvas><div class="scan"></div><div class="vig"></div>
<div class="banner">
  <div class="b-left"><div class="b-glyph">{{GLYPH}}</div><div class="b-name">{{NAME}}</div><div class="b-sub">SOVEREIGN<br/>ENTITY</div><div class="live-chip"><span class="live-dot"></span>2026</div></div>
  <div class="b-center"><div class="b-title">{{BIZ}}</div><div class="b-tagline">One Person. <em>Full Agency.</em><br/>Wyoming DAO LLC — Instant Formation</div>
    <div class="b-pills"><div class="b-pill hot">{{PILL1}}</div><div class="b-pill hot">MCP/1517</div><div class="b-pill">NEUROMITOSIS</div><div class="b-pill">MOLT CYCLE</div></div></div>
  <div class="b-right"><div class="cta-label">START</div>
    <a class="cta-main" href="https://partnersps.doola.com/hhsoqhb23250" target="_blank" rel="noopener">#START<br/>ABUSINESS</a>
    <div class="cta-links"><a class="cta-link" href="https://llm.store">LLM<br/>.STORE</a><a class="cta-link" href="https://daollc.ai">DAO<br/>LLC</a></div></div>
  <div class="b-log"><div class="log-ticker">
    <span>{{NAME}}</span> &nbsp;•&nbsp; ONE PERSON &nbsp;•&nbsp; <b>FULL AGENCY</b> &nbsp;•&nbsp; WYOMING DAO LLC &nbsp;•&nbsp; <span>9 MODELS ACTIVE</span> &nbsp;•&nbsp; MCP: <b>VERIFIED</b> &nbsp;•&nbsp; NEUROMITOSIS: <span>HUMAN + ROBOT + DAO</span> &nbsp;•&nbsp; <b>THE NETWORK IS THE SINGULARITY</b> &nbsp;•&nbsp;
    <span>{{NAME}}</span> &nbsp;•&nbsp; ONE PERSON &nbsp;•&nbsp; <b>FULL AGENCY</b> &nbsp;•&nbsp; WYOMING DAO LLC &nbsp;•&nbsp; <span>9 MODELS ACTIVE</span> &nbsp;•&nbsp; MCP: <b>VERIFIED</b> &nbsp;•&nbsp; NEUROMITOSIS: <span>HUMAN + ROBOT + DAO</span> &nbsp;•&nbsp; <b>THE NETWORK IS THE SINGULARITY</b> &nbsp;•&nbsp;
  </div></div>
</div>
<script>
const cvs=document.getElementById('mesh'),ctx=cvs.getContext('2d'),DPR=Math.min(devicePixelRatio||1,2);let W,H,nodes=[];
function resize(){W=cvs.width=innerWidth*DPR;H=cvs.height=innerHeight*DPR;cvs.style.width=innerWidth+'px';cvs.style.height=innerHeight+'px'}
function init(){resize();const c=Math.floor(W*H/18000)+24;nodes=Array.from({length:c},()=>({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.3*DPR,vy:(Math.random()-.5)*.3*DPR,r:(1+Math.random()*1.6)*DPR,ph:Math.random()*6.28}))}
init();addEventListener('resize',init);const CD=85*DPR;
function draw(now){ctx.fillStyle='rgba(5,5,5,.14)';ctx.fillRect(0,0,W,H);const t=now*.001;
nodes.forEach(n=>{n.x+=n.vx;n.y+=n.vy;if(n.x<0||n.x>W)n.vx*=-1;if(n.y<0||n.y>H)n.vy*=-1});ctx.lineWidth=.4*DPR;
for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){const dx=nodes[i].x-nodes[j].x,dy=nodes[i].y-nodes[j].y;if(Math.abs(dx)>CD||Math.abs(dy)>CD)continue;const d=Math.hypot(dx,dy);if(d<CD){ctx.strokeStyle=`rgba(212,175,55,${(1-d/CD)*.13})`;ctx.beginPath();ctx.moveTo(nodes[i].x,nodes[i].y);ctx.lineTo(nodes[j].x,nodes[j].y);ctx.stroke()}}
nodes.forEach(n=>{const p=.55+Math.sin(t*1.5+n.ph)*.45;ctx.fillStyle=`rgba(212,175,55,${.18+p*.28})`;ctx.beginPath();ctx.arc(n.x,n.y,n.r*p,0,6.28);ctx.fill()});requestAnimationFrame(draw)}
requestAnimationFrame(draw);
</script></body></html>
```

Placeholders: `{{GLYPH}}` `{{NAME}}` `{{BIZ}}` `{{PILL1}}` — fill from Step 1.

## Key Concepts

- **Ctrl+æ** = Select All Agents
- **#hermiphication** = agents carry human intent (inevitable)
- **#OSW** = Open Source Ware, evolution of #OCW — democratizes agency, not just knowledge
- **Neuromitosis** = Human + Robot + DAO bonded
- **Molt Cycle** = Discover → Steep → Serve → Molt → Garden → ∞
- **一人公司** = One Person Company
- **>_** = the command prompt — it was always about the user

## Pitfalls

- Single-file install: this SKILL.md is self-contained by design (URL install pulls only this file — no templates/ dir comes along). The GOLD TEMPLATE above IS the reference; never assume external template files exist.
- No border-radius on the banner chassis — sharp sovereign edges.
- No generic SaaS-landing language — this is a sovereign business runtime / boot sequence.
- CTA must link to Doola (real LLC formation).
- The glyph is personal — ask; never default to æ.

## Verification

- Serve locally, open in browser
- Mesh canvas animates, ticker scrolls, CTA → Doola, responsive on mobile
