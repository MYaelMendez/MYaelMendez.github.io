# Asimov Robotics Build Plan · v1.0

Authority: `HUMAN://ROOT → æ → ae → RECEIPT`

Problem this fixes: ad hoc edits, stale browser panes, and fresh-tab checks were treated as proof. They are not. One loop is now canonical.

## Principles

1. One manifest: `asimov-build.json` is the source of truth for page, assets, shell, mask, and authority.
2. One canonical URL: the page named in the manifest is the only page to review. Cache-busted filenames are preferred over query strings.
3. One review: browser state is proof only when it comes from the canonical URL and includes WebGL2, mesh load, material color, control counts, and canvas pixel evidence.
4. One receipt: every loop appends to `asimov-kaizen.jsonl` with a hash-chained record.
5. One kaizen: every defect becomes a countermeasure in the skill before the next loop.

## Loop

1. **Build** — run `python3 scripts/asimov_kaizen.py build`. Verify assets exist and hash them.
2. **Publish** — commit the manifest, plan, and any page changes to `gh-pages`; wait for the canonical URL to serve the expected build hash.
3. **Review** — open the canonical URL in `browser_exec`; assert:
   - title includes `NEON ORANGE`
   - WebGL2 context exists
   - `window.__ae` exists
   - head reports `neck_pitch_link · 32x28 mask`
   - shell color `ff6a00`, emissive `ff3d00`
   - 6 programs, 8 states, 5 cameras
   - canvas has orange pixels and green LED pixels
4. **Record** — pipe the review JSON into `python3 scripts/asimov_kaizen.py review`.
5. **Kaizen** — for each defect: write root cause + countermeasure into `skills/robotics-kaizen-loop/SKILL.md`.
6. **Repeat** — next loop starts from step 1. No exceptions.

## Loop 2 — controllable head environment

- Target: `https://myaelmendez.github.io/asimov-head-lab.html`
- Source: `assets/gltf/asimov-web.glb` → `neck_pitch_link` (the real Asimov-1 head)
- Environment: Three.js scene with floor, light rig, particles, and camera presets
- Control: full head transform (yaw/pitch/roll/position/scale), mask programs/states, LED surface, environment presets, lighting, and motion modes
- Review: same browser evidence standard as Loop 1, plus transform/environment assertions

## Current canonical build

- Page: `https://myaelmendez.github.io/asimov-head-lab.html`
- Head: `assets/gltf/asimov-web.glb` → `neck_pitch_link`
- Shell: `#ff6a00`, emissive `#ff3d00`
- Mask: 32×28 LED texture, no tablet
- Rig: `ffmpeg-asimov/asimov_1_25dof.urdf`, `ffmpeg-asimov/asimov_1_25dof.xml`
