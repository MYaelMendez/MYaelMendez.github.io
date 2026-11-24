# MECH-OS BUILD SPECIFICATION v0.2

**Base frame:** 9:16 · **any viewport is allowed** · **mobile is the primary target**
Surface: [mech-os.html](https://myaelmendez.github.io/mech-os.html) · Charter: [AE-PROTOCOL.md](./AE-PROTOCOL.md)

---

## S1 · Viewport discipline

**Rule V1 — the base frame is 9:16.** The composition is authored against a portrait phone.
Landscape is an accommodation, never the reference.

**Rule V2 — fit, never overflow.** At every width the desktop must have **zero horizontal
overflow**. Vertical overflow is permitted *only* by explicit scrolling of `#desktop`; windows
are never clipped silently.

**Rule V3 — one manager owns geometry.** All window boxes are computed by `layoutWindows()`.
Hand-placed `style="top:…"` values in markup are **initial hints only** and are overwritten on
the first layout pass. No media query may carry `!important` over inline geometry.

**Rule V4 — sweep, don't sample.** Layout claims are verified across a sweep
(320 / 390 / 768 / 1024 / 1440 px) and both orientations, not at two chosen widths.

### Current state → required
| claim | state |
|---|---|
| portrait stacks 9:16 full-width | measured 390×844 |
| landscape tiles four 9:16 + 1:1 flow | measured 1440×900 |
| width sweep | **not done** |

---

## S2 · Theme system

**Rule T1 — several palettes, one contract.** Every surface exposes these variables; nothing
else may encode colour:

```
--ae-bg   --ae-ink   --ae-accent   --ae-line   --ae-dim
```

Surfaces that already own an accent (`--gold`, `--secondary-color`, `--primary-color`) keep
working: the theme writes those **if and only if the surface declares them**.

**Rule T2 — day or night, chosen or automatic.** Default follows `prefers-color-scheme`; a
manual choice overrides it and persists in `localStorage['ae-theme-v1']`. A visitor who picks
nothing gets the correct one for their clock, untagged.

### Palettes

| id | name | feel | bg | accent | use |
|---|---|---|---|---|---|
| `void` | æ void *(default)* | gold on nothing | `#050505` | `#D4AF37` | night |
| `ember` | ember | warm dark | `#120B08` | `#FF6B35` | late day |
| `glacier` | glacier | cold dark | `#04080C` | `#6EE7F9` | night |
| `verdant` | verdant | deep green | `#041007` | `#7CE38B` | long sessions |
| `orchid` | orchid | violet dark | `#0C0514` | `#C084FC` | dusk |
| `paper` | paper | **light** | `#F5F1E6` | `#8A6A00` | bright day |

Each palette carries `dim`/`line`/`ink` companions — a palette is a complete surface, not one
hex value.

**Rule T3 — the theme is data.** One module (`assets/brand/ae-theme.js`), one control in the
console top bar. Copy-pasting per page is prohibited.

---

## S3 · Native readiness

Not integration. **Readiness** = the surface already speaks the right verbs, refuses honestly,
and carries the receipt.

### S3.1 · androidmcp
- **verbs:** `android.*` — device reach, input, screen, app lifecycle.
- **gate:** no act without a bound human approval (same shape as `asimov://` ACT-001).
- **receipt:** `plan → approve → act → sha256`.
- **refusal we publish:** `NO DEVICE PAIRED`.

### S3.2 · webmcs
- **verbs:** `web.*` — navigate, read DOM, submit.
- **gate:** a page is **evidence**, not authority; a read-back is not a browser test.
- **receipt:** per action, with the source it came from.
- **refusal we publish:** `SANDBOX · NO LIVE SESSION`.

### S3.3 · agentic commerce
- **verbs:** `store.*`, `order.*`, `pay.*`.
- **gate:** **no order, charge or transfer without an explicit signed intent.**
- **receipt:** amount, currency, destination, intent hash — before and after.
- **refusal we publish:** `PRICES REFUSED · provider + source + timestamp required`
  (already implemented on the markets rail).

**Common rule:** each domain ships **three artefacts together** — a verb file, a receipt, and a
window that wears it. A domain with only a verb file is declared **spec-stage**, never live.

---

## S4 · Window contract (unchanged, restated)

| mechanic | behaviour |
|---|---|
| title | drives the æ menu automatically |
| `[▣]` | dock → 1:1 square in the flow |
| `[◈]` | mirror any estate `.html` surface |
| `[x]` | close; layout recomputes |
| standard set | `SYSTEM_STATUS` · `COMM_LOGS` · `MODEL_COMBINATOR` · `ROOT_ENDPOINT` — start docked |
| master | claims the first portrait slot |

### S4.1 · Widget standard (new)

A capability that more than one window needs is **a widget, not a copy**. One module over one
data source, mounted per window, each instance reporting its own count.

```
assets/<domain>/ae-<domain>-widget.js   +   <div data-<domain> [data-<domain>-cat] [data-<domain>-limit] [data-<domain>-compact]>
```

Rules:
- **one renderer.** No window carries its own markup for shared content.
- **declare, don't import.** A window opts in with attributes; it never copies a list.
- **counted.** Every instance exposes `data-<domain>-count` / `-shown`, so a window cannot claim
  more than it displays.
- **lensed.** The same widget renders per host scope (category, limit) — one component, many
  views.

First instance of the standard: **`assets/atlas/ae-atlas-widget.js`** over `window.AE_ATLAS`,
mounted natively by the `ORIGIN` window. `origin/index.html` keeps its own fuller rendering;
both read the same data.

---

## S5 · Non-goals

- No cloud execution. Custody stays on Victus.
- No external API binding without a stated source and timestamp.
- No decoration presented as measurement. Random visuals stay clearly decorative.

---

## S6 · Delivery order

1. theme module + palettes + control *(this pass)*
2. `origin/` window *(next, per operator)*
3. width sweep rig
4. declared/measured counter
