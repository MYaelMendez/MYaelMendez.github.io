# ASIMOV PET — evolution plan

Body: menloresearch/asimov-1 · atlas `picoasimov-atlas.webp` 1536×1872 · 9 states × 6 frames ·
cell 192×208 · **91% alpha** · renderer three.js r186 (**RTX 3050 @ 1.21 ms/frame** measured).

Invariant for every phase: **the receipt changes shape, never disappears.** A pet that cannot be
hashed is decoration, and decoration presented as capability is the one thing this estate forbids.

---

## P0 · Substrate (done)

Atlas path fixed to the site root; mount loads and reports state. Verified by image `naturalWidth`,
not by attributes.

## P1 · Authority on the body — *small, high meaning*

The pet answers `asimov://` verbs instead of clicks alone.

- `aePetWidget.signal('plan'|'approve'|'refuse'|'receipt')` maps to states:
  `plan → running`, `approve → waving`, `refuse → failed`, `receipt → review`.
- Every mapping is logged as `[| "PET", <signal>, <state>, "QR://pet/<state>" |]`.
- Gate: refuse never animates happily — `failed` wins over any prior state until cleared.

## P2 · Telemetry-driven states — *the pet becomes an indicator*

States reflect measured estate signals, not only interaction.

| signal | state | source |
|---|---|---|
| job running / dispatch live | `running` | fleet/ticker |
| awaiting human approval | `waiting` | æ policy |
| gate refused | `failed` | any supervisor |
| receipt landed | `review` | hash chain |
| idle > 30 s | `idle` | timer |

API: `aePetWidget.signal(name)`, plus `auto(true|false)`.

## P3 · Live articulation — *the unlock*

Replace pre-baked frames with the jointed geometry (`ffmpeg-asimov/urdf.json`, 26 links / 25
joints) rendered in-page.

- Pose = function of `(state, t)`, so any expression becomes possible.
- **Receipt**: per-frame FNV digest over `readPixels` of a fixed 64 px crop + pose hash — the same
  technique `rtx://render` proved. Two runs, same digest.
- Falls back to the sprite atlas when WebGL or the mesh is unavailable, and declares which.

## P4 · DOM-aware locomotion — *the visible payoff*

Position, velocity, and an obstacle set read from **live element rects**.

- Walks the viewport, turns at edges, avoids the hero card and the dock.
- Never overlaps text: obstacles recomputed on resize (throttled).
- Debug overlay showing the obstacle set, off by default.

## P5 · Higher-resolution raster — *independent, cheap*

Re-rasterise cells at 384×416 (and 4K for large displays). Renderer exists; the sprite path stays
as the fallback.

## P6 · Voice on events

tiny-voca wired to `waving`/`failed`/`review` once synthesis is unblocked. Blocked today on the
numpy ABI mismatch in the local TTS runtime.

---

## Sequencing

```
P1 → P2 → P3 → P4
                 ↘ P5 (parallel)      P6 (blocked)
```

P3 is the critical path: it removes limitations 1, 3 and 5 together. P4 depends on it.
P5 and P6 are independent.

## Acceptance per phase

One measured check each, recorded in `AE-CONTINUITY.md`. No phase ships on reasoning.
