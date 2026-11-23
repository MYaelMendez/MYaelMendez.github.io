# PET-MANEUVER — iterative design

**Question.** How does the Asimov pet become fully capable of maneuvering about the
viewport, and DOM-aware?

**Answer in one line.** It is not a sprite problem, it is a *locomotion* problem: the
viewport is 2D, the atlas is a fixed-camera film strip, so maneuvering = a 2D pose
(`x, y, facing, state`) driven by a state machine that reads the DOM. Each stage below
adds one capability and one **measured** gate.

---

## The measured constraint (do not design around it)

From `pet/pet.json` — the receipt:

| fact | value |
|---|---|
| atlas | 1536 × 1872 RGBA (`picoasimov-atlas.webp`, sha256 `1963ee54…`) |
| grid | 8 columns × 9 rows, frame 192 × 208 |
| **frames per state** | **6** — columns 6–7 are unused (measured: 0 opaque samples) |
| states (row order) | `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, `review` |
| policy | `Menlo/asimov1-locomotion-0818` (sha256 `47f70691…`) |
| verb sources | `verbs/out/walk.json` = `[0.4, 0, 0]` · `verbs/out/turn.json` = `[0, 0, 0.8]` |
| determinism | same model + same traces → same bytes; the hash is the receipt |

**What this means.** There is **horizontal** locomotion (`running-right`, `running-left`)
and a forward gait (`running`). There is **no vertical** locomotion, **no turn-in-place**
row, and **no climb**. The pet's *pose* is 2D but its *art* is a fixed camera. Any stage
that needs vertical or turning is a **render job on the RTX**, not CSS.

**Defect found and fixed while writing this.** The home driver cycled 8 columns and
labelled rows 5–8 `sleeping/sitting/standing/backflip`. Both were wrong: the receipt says
6 frames and `failed/waiting/running/review`. Fixed in `ba9631e` — the pet was blanking
two ticks in every eight.

---

## Stage 0 — the honest baseline (shipped)

The pet is a DOM element at a fixed point, 9 states × 6 frames, DOM-driven.

- **asset cost:** none (atlas exists, hash-sealed).
- **gate:** `pet.json` receipt verified; 9 rows × 6 columns measured opaque; state
  switching changes `background-position` to the right row.
- **verified:** atlas loads (natural 1536); `aePet.set('waving')` → row 3 (`-624px`); the
  label follows.
- **declared, not verified:** the frame loop (headless rAF is throttled; 12 fps in a real
  browser).

## Stage 1 — a real pose, anchored to the DOM (no new assets)

Give the pet a pose object `{x, y, facing, state}` and anchor it to a **slot element**
instead of a hard-coded pixel offset. The slot is placed by the layout, so the pet survives
reflow.

- **asset cost:** none.
- **gate (measured):** on resize the pet re-anchors inside its slot, and its
  `getBoundingClientRect()` never intersects the section's text box. A rect-overlap test
  runs on every anchor and reports `overlap: false`.
- **declares:** "the pet is placed by the layout, not by a magic number."

## Stage 2 — horizontal maneuvering (the atlas already has it)

A state machine: `idle → walk-right → arrive → idle`. Position advances `px/frame`, the
row switches to `running-right`/`running-left`, and `facing` flips.

- **asset cost:** none.
- **gate (measured):** given a DOM target, the pet arrives within N frames **and** its
  footprint stays inside the viewport (`0 ≤ x ≤ vw − w`) at every step. Logged as a
  `walk-receipt` per trip: `{from, to, frames, out_of_bounds: 0}`.
- **declares:** "it walks, it does not teleport."

## Stage 3 — DOM awareness (reading the page)

The pet reads the DOM and reacts:

1. **nav-follow** — click a nav link, the pet walks to that section's anchor.
2. **cursor-facing** — it turns to face the pointer (`running-left` vs `running-right`
   semantics reused as facing).
3. **scroll-attention** — it idles beside the section currently in view.
4. **state-report** — its label reads the estate's own numbers (`estate.json`): receipts,
   drift, surfaces.

- **asset cost:** none.
- **gate (measured):** for every nav link, the pet's final `x` is within the target
  section's rect; and an a11y test asserts the pet **never covers a link or button**
  (rect intersection over all `a, button`). Fail-closed: if it would overlap, it stops at
  the boundary and says so.
- **declares:** "it reads the page, and it yields to the page."

## Stage 4 — vertical + turning (a render job, not CSS)

Add rows for `walk-up`, `walk-down`, `turn`, `climb`. Extend `verbs/out/` with the turn and
vertical traces, re-render the CAD on the sovereign RTX 3050, re-seal the atlas.

- **asset cost:** one render pass; deterministic, so the new atlas has a new sha256.
- **gate (measured):** ≥ 12 states; the same `min_opaque_px` floor (4,328); the receipt
  hash changes and the old hash is recorded as superseded (not deleted).
- **declares:** the estate's rule — *the spec commands, the scene is never edited*.

## Stage 5 — real control (the actual robot)

Drive the pet from the Menlo locomotion policy (MuJoCo, 25 joints) instead of a sprite row.
The pet becomes a live render of the real sim, and the sprite and the policy must agree.

- **asset cost:** the sim + a render bridge; the existing `walk.json` / `turn.json` verbs
  are the contract.
- **gate (measured):** the same `[0.4,0,0]` walk and `[0,0,0.8]` turn that the hardware
  verbs accept produce the same displacement and heading in the render. Disagreement is a
  defect, not a calibration.
- **declares:** "this is the robot, not a picture of the robot" — the estate's own rule.

---

## The rule that governs every stage

> **A thing that has not been checked back is not a thing.**

So each stage ships with a **receipt**, not a claim: the pose, the target, the frames, the
overlap test, and the hash of whatever asset it used. Where a gate does not exist, the
page says the check is missing — it never reports a pass.

**Ranked:** 1 → 2 → 3 are pure DOM and can ship in one pass. 4 is the first real cost
(RTX render). 5 is the sovereign goal and the honest end state.
