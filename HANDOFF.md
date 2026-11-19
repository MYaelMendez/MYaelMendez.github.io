# æ · SESSION HANDOFF — 2026-11-19

Read this first after a reload. Everything below is measured, not asserted.

## Restore the companion stack

```
C:\æ\agents\asimov_up.cmd
```

Starts four local services. No credentials, no cloud.

| port | service | why |
|---|---|---|
| 8162 | `asimov_env.py` | perception — GPU, RAM, receipts, renders |
| 8161 | scene server | the WebGL companion page + 70 MB of CAD |
| 9333 | Chrome CDP | **`--force_high_performance_gpu`** — the whole unlock |
| 8081 | VLC | the human truth pane |

Verify: `curl http://127.0.0.1:8162/env` then
`node %SC%\webgl-asimov\companion.mjs status`.

## What was accomplished

**Three GPU paths where there was one.**
```
Intel OpenGL   570 ms/frame   the accidental default (NVIDIA ICD unregistered)
CuPy CUDA       31 ms/frame   software raster, zero deps, bit-deterministic
WebGL/ANGLE    ~1–3 ms        hardware, shadows, PBR, MSAA — one Chrome flag
```

**The unlock:** this Optimus laptop has no registered NVIDIA OpenGL ICD
(`nvoglv64.dll` exists only in the driver store). Four levers to force OpenGL
onto the discrete GPU all failed. **Chrome reaches it via ANGLE→D3D11 with
`--force_high_performance_gpu`.** Verified: `ANGLE (NVIDIA, RTX 3050, D3D11)`.

**The Asimov browser companion.** Not a frame factory — a live robot surface
Hermes drives over CDP. `status / pose / setState / say / move / ledger`.
It perceives the machine every 4 s and its expression follows GPU load and
temperature. `move()` is refused: `require_approval · ACT-001, AUTH-002`.
**It shows anything and grants nothing.**

**mp4:// 11/11 links**, `hermes-asimov` **18 tools**, 391 receipts,
105 films published.

## Pending — in priority order

1. **Verify the desktop pane renders.** `Companion` iframe was added to
   `desktop-plugins/hermes-asimov/plugin.js` (418→477 lines, pane 340→420px).
   It parses; it has **never been seen in the running app**. That is the first
   thing to check after the reload.
2. **Bundle the scene into the plugin.** The pane loads `127.0.0.1:8161`, which
   needs a local server a stranger would not have. Serve it from the plugin's
   own static route instead.
3. **Render a full WebGL film.** Only 6 test frames exist. The renderer is the
   best of the three and has produced no film yet.
4. **Re-render `rtx-hermes-collision-proxy-916.mp4`** with the URDF path so the
   spoken version has correct geometry.
5. **Second-machine reproduction.** Still one laptop. Highest-information test.
6. **Tests 24 → 60.** homeassistant ships 60; we ship 24.
7. **The grant binding.** Operator decision. Unbuilt by design.

## Known defects, carried forward

- `rtx-hermes-collision-proxy-916.mp4` renders **collision capsules as the body**.
  Published under that name deliberately, as evidence.
- Older films predate the warmup guard (frame 0 artifact) and the `-shortest`
  fix (dropped frames). Not re-rendered.
- WebGL capture is ~150 ms/frame, **98% CDP screenshot cost**, not render cost.
  `Page.startScreencast` or raw buffer capture would fix it.
- The companion's `_react()` can override an agent-set state on the next
  perception tick. Needs a hold so SPEAKING is not clobbered.

## Lessons worth keeping (kaizen)

**Measure the thing, not a proxy.** A glob's length is not a mesh count
(Windows is case-insensitive: 52 was 26). A patch testing clean is not a render
advancing. A passing gate is not a right film. Three instances in one session.

**Read the repos before building.** The correct model — `urdf.json`, 26 links —
was in `ffmpeg-asimov/` in the repo I was publishing to all session. I rebuilt
from the actuated MJCF and rendered its collision proxies.

**A third path usually exists.** OpenGL blocked → wrote a CUDA rasteriser →
the browser was there all along, and better. Exhausting two options is not
exhausting the space.

**Assessment scale changes verdicts.** A face called crude at full-frame
downscale was refined when cropped. Same class as the board-resolution bug.

**Fix the scene, never the threshold.** Motion 0.386 = WARN → strengthened the
gesture to 3.479, not lowered the gate.

**String replaces hit the first occurrence.** `requestAnimationFrame(tick)`
appeared twice; the boot calls landed inside the loop and spawned a timer
every frame. Anchor on surrounding context, not a bare line.
