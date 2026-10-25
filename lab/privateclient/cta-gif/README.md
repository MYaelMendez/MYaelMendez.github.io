# cta-gif · #startabusiness / (LAB)

Two animated CTAs built from the Private Client post card (`privateclient/default@1.0.0`, Terminal night/day themes), for the LinkedIn page **#startabusiness LLM.STORE** (linkedin.com/company/daollc). LAB only: nothing is posted, nothing is deployed to privateclient.ai.

Idea: Yæl, 2026-10-19 — "we can use our linkedin post template as a gif call to action too!"

| door | theme | headline | æQR target |
|---|---|---|---|
| CLI.LLC (`$` crown, #f97316) | 🌙 night | Cli in, llc out. · 🌍 founders anywhere · LLC with doola | https://privateclient.ai/startabusiness?door=clillc |
| DAOLLC.AI (`◆` crown, #c084fc) | ☀️ day | DAO LLC ◆ · 🤖 robot-assisted smart contracts | https://privateclient.ai/startabusiness?door=daollc |

Flow (8 s, 15 fps, loops): ✍️ write (typing) → ✅ check (face `checking`, ✓ spelling / tone / rules) → ✋ hold (fill) → ✓ I APPROVE THIS MESSAGE (face `ok`) → CTA: domain æsymov (ae.face/0.2, `lab/face/lang/pc-face.js` domain crowns), yellow **#startabusiness /** button (#f5c400, black), big æQR (segno, ECC M). Last 0.4 s crossfades to frame 0.

Files: `startabusiness_{clillc,daollc}_{1200x1200,1080x1350}.{gif,mp4}` · `render.py` (PIL + cairosvg renderer; `python3 render.py clillc 1200 1200 out/` then ffmpeg palettegen/paletteuse).

QR check: every GIF and MP4 decoded with zxing-cpp on a card frame (small æQR) and a CTA frame (big æQR) → the door URL above.

## Captions (drafts, not posted)

**CLI.LLC**
```
⌨️ Cli in, llc out.
🌍 → 🏢 LLC with doola
✍️ ✅ ✋ ✓

#startabusiness /
https://privateclient.ai/startabusiness
```

**DAOLLC.AI**
```
🤖 DAO LLC ◆
smart contracts · robot-assisted
✋ a human holds the key ✓

#startabusiness /
https://privateclient.ai/startabusiness
```
