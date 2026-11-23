# ESTATE SPEC — measured, not declared

> **For Hermes:** execute with the subagent-driven-development skill, task by task.
> Do not batch tasks; each one lands as its own commit through `kanban_push.py`.

**Goal:** every figure on a surface names the instrument that produced it, and every
instrument can be re-run.

**Architecture:** three layers, cheapest first. **(a) Existence** — does the page
resolve and does what it cites exist. **(b) Binding** — does the artifact the page
shows match the receipt it cites, byte for byte. **(c) Claims** — is each figure
produced by a named instrument, and is there a stated falsifier. Nothing at layer
(c) is trustworthy until (a) and (b) are green.

**Tech stack:** Python 3 stdlib generators next to the surfaces they measure;
`kanban_push.py` for every push; JSON as the only machine format; markdown as the
only human format. No new dependencies.

---

## 0. Current state — measured, 2026-11-23

| instrument | result |
|---|---|
| `agents/estate_index.py` | **419 surfaces** · 228 at root · 30 addressed · 389 unaddressed · 11.6 MB |
| `agents/estate_health.py` | **420 surfaces** · 418 reachable · **2 unreachable** · **28 with missing assets** · 391 healthy |
| `væult_chain.py manifest` | 12 links · 11 healthy · `supervision` broken under uv-3.12 |
| `robots/index.json` | 6 robots · 6 present · 4 unregistered dialects |
| `purpose.html` | 5 charter clauses + 6 earned rules, all falsifiable |

The 2 unreachable pages are **not broken**: `privateclient/bridge.html` and
`continuity-wasm/dist/probe.html` exist on disk and are untracked — unpublished
work, not defects.

---

## 1. Known defects

Every one was found by measurement, not by reading. Each carries its measured value
so the correction is scheduled rather than remembered.

| # | defect | measured |
|---|---|---|
| D1 | `supervision` reported **broken**, cause is an interpreter | 12/12 under hermes-venv and gpu; **11/12** under uv-3.12 (no qrcode/pillow) |
| D2 | manifest counts 12 links, lists **11** | `links_total: 12`, `len(links): 11` — `sms` counted, never listed |
| D3 | a receipt was displayed but never compared to the served bytes | `robot-env-demo.html` prints sha256 but never hashes the film |
| D4 | the gate read as a whole-film verdict while sampling 5 frames | `frames_analizados: 5` of 96 = **5.2 %** |
| D5 | the pet rig computed a box nobody sees | coord 192×208 vs **screen 67.56×73.19** at 1080×1920 |
| D6 | `tinyfanin.html` held a second copy of its own truth | hand-wrote head + 4 rows that `tinyfanin-truth.json` carries |
| D7 | `waetz.html` held a typed atlas contract the receipt already carried | 4 constants duplicated; fixed 2026-11-23 |
| D8 | the triangle count had no instrument | fell through to `min_opaque_px` = **4,328** where the page said 1,007,041 |
| D9 | the host and the fleet surface disagreed on the scheme | `robots.html` = wætz://; `waetz.html` said nothing; fixed 2026-11-23 |
| D10 | the estate's own health instrument was wrong twice | non-ASCII paths called dead (6 live pages); JS concatenation counted as paths (**89** phantom failures) |

D5, D6, D7, D9, D10 are corrected and shipped. D1–D4 and D8 remain.

---

## 2. Specifications

Each requirement is falsifiable: it states the instrument and the value that breaks it.

### S1 · A figure names its instrument
Every number, count or address rendered on a surface carries the source that produced
it — a file path, a command, or a receipt field. A figure with no named source is
rendered as `unverified`.
**Falsifier:** a surface contains a numeric literal that is not a dimension, a threshold
or an index.

### S2 · One truth per fact
No surface holds a copy of a number that a machine artifact already carries.
**Falsifier:** a value appears in both a `.json` and an `.html` without the HTML
reading it. *Instances closed:* D6, D7, D8.

### S3 · A receipt binds to its artifact
Wherever a receipt is shown, the page verifies the artifact against it —
fetch → `crypto.subtle.digest('SHA-256')` → compare. Until it does, it renders the
receipt as `unbound`.
**Falsifier:** a page displays a sha256 and cannot say whether the bytes match.

### S4 · A gate states its sample
Any aggregate quality figure states `sampled / total`. A five-frame verdict on a
96-frame film must read `5 / 96`, not `PASS`.
**Falsifier:** a gate verdict with no denominator.

### S5 · A rendering claim names its coordinate space
Crispness, fit and box size state whether they are device coordinates or screen
coordinates, and give the factor between them.
**Falsifier:** a crispness claim without a `k`. *Instance closed:* D5.

### S6 · A missing verb is a named refusal
Never a crash, never a blank. The refusal names the verb and the robot.
**Falsifier:** an empty cell or an uncaught exception where a verb belongs.

### S7 · A status names its environment
Any healthy/broken verdict states the interpreter and working directory that produced
it, or says the check is missing.
**Falsifier:** a bare `ok`/`broken`. *Instance open:* D1.

---

## 3. Work items

Ordered by dependency. Each is one commit through `kanban_push.py`.

### Wave 0 — close the three sync gaps (packaging, 3 commits)

**T0.1** · `robots.html` meta description still says `robot:// — one governed address
space` while the title says `wætz://`.
Modify `github-pages/robots.html:7`. Expected after: description names wætz:// as the
policy over robot://.

**T0.2** · the hub links the page as `robot:// — the fleet index`.
Modify `github-pages/index.html` (the registry link row). Expected after: the label
reads `wætz:// — the policy over robot://`.

**T0.3** · `purpose.html` names no scheme.
Add to clause 3 or the closing block: `wætz://` is the proprietary policy,
`robot://` the dialect it governs. Expected after: the charter's authority order
matches `robots.html`'s rule.

### Wave 1 — clear the 28 dangling refs (measurement-driven)

Instrument: `python agents/estate_health.py`. **Acceptance: `dangling` → 0.**

**T1.1** `_studio/` cluster — `contributions-studio.html`, `homebase-studio.html`:
`favicon.svg`, `filmmemory-status.json`, `homebase.html`, `capability-mesh.html`,
`origin-spectrum.html`, `kaenbaen`.
**T1.2** `asimov-viewport*` cluster — `videos.html`, `menlo-asimov-ffmpeg-latest.zip`.
**T1.3** root cluster — `menlo-asimov-ffmpeg-916.mp4`, `gpu-preview.html`,
`qpos_viewer.html`, `sim.html`, `video-vision.mp4`, `sovereign-capacity-916.mp4`.
**T1.4** `aipodcast_me/` cluster — `holomesh.mp4`, `cuda-mcp2.mp4`.
**T1.5** remainder — `gospel-bookstore/qr.png`, `api/...` routes referenced by
`qr_keys.html` and `ael-tv-net-station-creator.html`.

Rule per item: if the asset exists elsewhere, correct the path; if it is genuinely
gone, remove the reference or mark it `unbuilt`. **Do not create placeholder files.**

### Wave 2 — the claims contract (the layer that matters)

**T2.1** Write `agents/claims_check.py`: scan the ten surfaces below for numeric
literals outside code, and report which are sourced. **Acceptance:** it runs and
prints a table; it does not need to be clean yet.
Surfaces: `index.html`, `robots.html`, `purpose.html`, `waetz.html`, `tinyfanin.html`,
`pet/test-916.html`, `aipodcast_me/robot-env-demo.html`, `tinyae.html`, `tinyhq.html`,
`origin/index.html`.

**T2.2** · D3 — `aipodcast_me/robot-env-demo.html` must verify the film.
Add: fetch `robot-env.mp4`, digest, compare to `d.sha256`; render `BOUND` or `UNBOUND`.
Expected after: the panel says `BOUND`.

**T2.3** · D4 — the gate's sample.
Render `frames_negros 0 / 5` as `0 / 5 of 96 frames (5.2 %)`. Expected after: the
denominator is visible.

**T2.4** · D1 — `væult_chain.py` `link_status` must classify an import failure as
`missing-dependency`, not `broken`, and record the interpreter that ran.
Expected after: `manifest` reports `supervision` as `dep-gap (uv-3.12)` rather than
`broken`.

**T2.5** · D2 — `manifest.links` must include every counted link.
Expected after: `links_total == len(links)`. Add a self-check assertion.

### Wave 3 — binding and drift

**T3.1** Extend `agents/estate_health.py` with `--bind`: for every surface whose
receipt is cited, hash the artifact and compare. **Acceptance:** a `bound` column
appears in `estate-health.json`.
**T3.2** Put `estate-health.json`'s failures on the hub — the failures, not a
dashboard. **Acceptance:** the hub shows `28 dangling` and the list.

---

## 4. BLOCKED — operator decisions

These are not stubs. Until decided, the code returns an explicit refusal naming the
reason.

**B1 · Which surfaces matter.** No traffic data exists. The plan assumes the ten
surfaces in T2.1. *Options:* install a ping counter, or accept the ten as the estate's
representatives. Interim: `claims_check.py` reports on the ten and says the selection
is assumed.

**B2 · `fits` semantics for the pet.** Containment, or allowed overflow?
Interim: report `contains` and `overflows` separately; do not collapse them.

**B3 · Prune or complete.** 419 surfaces, 389 unaddressed. *Options:* prune to a
deliberate dozen, or address them. Interim: nothing is deleted; the count is published.

---

## 5. Acceptance

The spec is done when, and only when:

1. `python agents/estate_health.py` reports **0 dangling refs** and **0 unreachable**
   (excluding untracked files, which it must say are untracked).
2. `python agents/claims_check.py` reports **0 unsourced figures** across the ten
   surfaces.
3. `python agents/væult_chain.py manifest` reports **12/12 with a named environment**
   per link, and no link reads `broken` without a classified cause.
4. Every surface that shows a moving artifact carries a verifiable receipt.
5. The hub publishes the current failure count, not a verdict.

Each is a command with an expected number. None requires judgement.
