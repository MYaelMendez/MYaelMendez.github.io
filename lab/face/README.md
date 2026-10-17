# æ æ æ · Asimov 1 face kiosk · LAB

> Make something agents want. · Human stays root. · Evidence ≠ Authority.

A fullscreen face for a phone or tablet mounted on the Asimov 1 robot. It reads `ae.face/0.1` state and draws one of seven moods. **Read-only, authority æ1: the face never sends anything to the robot.** LAB page, `noindex`.

Live (LAB): https://lutheraninstitute.github.io/aeee-lab/lab/face/

## Inputs, in order

1. **`?src=<url>`** polls a `face.json` every 500 ms (one request at a time, 900 ms timeout). It shows `:lost` when the fetch fails, the JSON is invalid, the state is older than 0.5 s (`ts`, `at`, `age_ms` or `stale`), or nothing good arrived for 1.5 s. The URL must allow CORS from this page (or be same-origin). Example: `?src=face.sample.json`.
2. **🪞 Mirror** (button or `M`): paste an `ae.face/0.1` JSON and the face draws it. The schema is checked (`schema`, `authority` = æ1, `mood`, `mode`, `battery`, `armed`); fields like `command`, `arm` or `move` are ignored with a notice. A pasted JSON's `ts` age is not checked (it is pasted, not live). Polling pauses while the mirror is shown; **↺ back to live** resumes it.
3. **Demo** (default without `?src`): cycles the seven moods. Mood buttons or keys `1`–`7` pin one.

Other parameters: `?maxage=0.5` (seconds), `?demo=4` (seconds per mood), `?mood=think` (pin), `?theme=u|y|b|g|r`, `?hud=0` (hide controls) / `?hud=1` (never auto-hide). Keys: `M` mirror, `D` demo, `F` fullscreen, `T` theme. Controls fade after 5 s; tap to bring them back. The page asks for a screen wake lock where the browser allows it.

## Moods (priority order, safety wins)

The face derives a mood from the fields and also reads the reported `mood`; it shows whichever ranks higher. A JSON that says `ready` while `mode` is `DAMP` shows `:sleep`.

| mood | rule | idle motion (motion = state) |
|---|---|---|
| `hold` | fault / `FAULT_DAMP` | glitch: cyan/magenta split line, slice flicker, jitter; crown turns hot |
| `lost` | state older than 0.5 s | radar sweep, pupils scan left–right, sway, scattered letters, `? ? ?` |
| `tired` | battery < 20 | half-lidded eyes, slow heavy blink, sag, drooping letters, blinking battery cell |
| `sleep` | `DAMP` | eyes closed, slow 7 s breath, `z z Z` drift, dim crown |
| `think` | `STAND`, not armed | one brow raised, pupils drift up, head tilt, thought dots, typing letters |
| `ready` | `STAND`, armed | open eyes, blink, breath, halo pulse, crown wave, "ARMED · MOVE ALLOWED" |
| `work` | `MOVE` | narrowed eyes, furrowed brow, bob, scan bar, tracking pupils, marching letters |

## Style

🛸 holomesh: void `#05060a`, gold `#D4AF37`, cyan `#39e6ff`, faint blueprint grid, Orbitron + JetBrains Mono, `>_` prompts. The face is **one continuous Picasso line** (a single SVG path: head, cheek, eyes, brow, nose, mouth, chin) drawn on with stroke-dash. Every mood uses the same path structure, so moods **morph** into each other and blinks are real morphs of the line. Theme swatches 🟨🟦🟩 (yellow/blue/green on cream `#f4efe3`, black ink), 🛸, and ♻️ rotate. `prefers-reduced-motion` turns off every animation, morph and blink.

## Files

- `index.html`: the kiosk, one self-contained file (no external JS; Google Fonts only).
- `moods/<mood>.svg`: the seven faces as static SVGs.
- `face.sample.json`: a sample state for `?src=face.sample.json`.
- `src/`: `core.js` (geometry, validate, derive), `index.tpl.html`, `build.js` (inlines core → `index.html`), `build-svgs.js` (→ `moods/`). Build: `node src/build.js && node src/build-svgs.js`.

Producer of `face.json`: `ae/face.py` / `ae/serve.py` in [LutheranInstitute/Robot](https://github.com/LutheranInstitute/Robot/tree/ae-face/ae) (branch `ae-face`).

LAB · simulation-grade UI, not a safety system. The robot's own controls and the human principal decide. #osw #ioa #æææ
