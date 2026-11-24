# AE-LEARNINGS — what each imported codebase taught the OS

**The standing rule.** Every time a codebase is brought into the program, the OS learns
something it could not have invented alone. That learning is wasted if it stays in the commit
message. So each import records three things:

| field | question |
|---|---|
| **pattern** | what mechanism did this codebase carry that the OS did not have? |
| **landed** | where does it live now — file, window, receipt? |
| **unlearned** | what did we *not* take, and why not? |

An entry without an artifact is a note, not a lesson. An entry with a receipt is a lesson.

---

## Register

### L01 · `mech-os.html` — the window manager
- **pattern:** layout computed by a manager (`layoutWindows`), never hand-placed; a window
  standard (title drives the menu, `[▣]` docks, `[◈]` mirrors).
- **landed:** `github-pages/mech-os.html`; continuity §86–§90.
- **unlearned:** persistence. Open windows are forgotten on reload.

### L02 · the `@media (max-width:768px)` trap
- **pattern:** CSS with `!important` outranks inline geometry. A manager that does not own its
  cascade silently loses to a phone rule at 764 px.
- **landed:** the re-scoped selector `body:not(.tiled):not(.portrait) .window`.
- **unlearned:** a width sweep. Geometry was verified at 1440×900 and 390×844, not across the
  range; the handoff is asserted, not swept.

### L03 · `ae-label.js` — the white-label standard
- **pattern:** one shared module instead of per-page copies; a surface opts into accent-following
  by *declaring* a variable rather than being edited.
- **landed:** `assets/brand/ae-label.js`; adopted by `mech-os.html`.
- **unlearned:** `index.html` still carries its own implementation. Two implementations exist —
  the drift the standard exists to prevent.

### L04 · `ae/control/index-live.html` — the æ://OPS intent chain
- **pattern:** the full verb spine as a *named sequence* —
  `INTENT → DISCOVER → COMPILE → AUTHORIZE → EXECUTE → WITNESS → RETURN` — plus a
  **MEDIDO / DECLARADO** provenance split and explicit refusals ("markets refuse prices
  without provider + source + timestamp").
- **landed:** worn as the `æ://OPS · CONTROL` window in `mech-os.html`.
- **unlearned:** the OS has the same verb chain as *plans*, not as *acts*. The control surface
  runs locally with a real SHA-256 receipt and no external execution — the console should adopt
  the same honesty about its own frontier.

### L05 · `picoasimov` pet atlas
- **pattern:** an asset as a *receipt* — 9 states × 6 frames from a real CAD, sha256'd.
- **landed:** `pet/pet.json`, `waetz.html`, hero + section mounts via `aeMountPet`.
- **unlearned:** DOM-aware locomotion is proposed, not implemented.

---

## How a new entry is made

1. Import the codebase.
2. Read enough to name the mechanism — not the whole corpus.
3. Write one row here: pattern, landed, unlearned.
4. If the lesson is worth teaching onward, it becomes a spec surface under
   `>_æ://…/*.md` and a window in the console.

**Rule:** the OS grows by import plus record. An import without a record is a dependency;
with a record it is a capability.
