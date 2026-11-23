# >_æ://neuromitosis/mech-hermes/llm_store — build specification

**Route:** `>_æ://neuromitosis/mech-hermes/llm_store`
**Status:** specification. Nothing here is built beyond what §1 lists as existing.
**Rule:** every number in this document is either read from a cited artifact or marked
`PROPOSED`. A `PROPOSED` number is a design target, never a measurement.

---

## 0. Thesis

The model store is not a page you visit. It is a **module the conductor serves**.

Today `llm-store.html` is a storefront with an omnibox whose commands are
`ls models` / `executeCommand(...)` — a CLI wearing a storefront's clothes, with no backend
(its `/api/llm-store/inference` fetch cannot resolve on a static host). `mech-os.html` is the
opposite: a rich console (draggable windows, command input, a robot canvas, a spatial frame,
an evolving typography system) with **fabricated telemetry** until §78 made it measured, and
no execution behind it.

This specification joins them: the console becomes the **operator surface**, the agent
runtime becomes the **conductor**, the local RTX (or the CUDA_MCP² broker) becomes the
**leaf**, and the store catalogue becomes the conductor's capability list. The human states
intent; the conductor returns a receipt.

This is the estate's own law restated: **one human → many agents needs "us" in between = the
conductor (the product).**

---

## 1. What already exists (measured)

| asset | fact | source |
|---|---|---|
| mech-os console | panels `robot-window`, `robot-pos`, `robot-bat`, `robot-canvas`, `spatial-window`, `spatial-frame`; measured ticker | `mech-os.html` DOM |
| store family | 13 surfaces; `llm-store.html` 309 KB, 54 model mentions, 51 price figures | `estate.json` + `tinyorigin gems` |
| live price feed | OpenRouter public API, 477 models; watch-list 104 | `openrouter.ai/api/v1/models` |
| estate index | 420 surfaces · 11.0 MB · 30 addressed · 390 unaddressed | `estate.json` |
| address atlas | 52 addresses · 49 live · 3 dead | `tinyorigin verify` |
| pet atlas | 1536×1872 · 9 states × 6 frames · 1,007,041 tris | `pet/pet.json` |
| locomotion | baseline 12 s @ vx 0.4 → **+4.1868 m** · knee swing 38.8°/37.7° · ~5 cm clearance · verdict *a shuffle, not a stride* | `policies/0818/MEASURED.md` |
| proof corpus | 152 films · 115 live · 37 unpublished · 5 defective (2 still live) | `film-corpus.json` |
| loopback broker | `127.0.0.1:7890`, loopback-bound, never echoes values, audit log | `secret_bridge.py` |

These are the parts. The build wires them; it does not replace them.

---

## 2. Target architecture

```
SURFACE   mech-os console (white-labelled)         human looks here
  │       intent in, receipt out — never a key
  ▼
BRIDGE    loopback relay 127.0.0.1:<port>         the only crossing
  │       op → plan → approval → act → receipt
  ▼
CONDUCTOR Hermes (>_h:)                            intent, custody, memory, dispatch
  │       catalogue · policy · fleet waves
  ▼
LEAF      Victus RTX (llama.cpp) · CUDA_MCP² broker → droplet
```

**The bridge is the only boundary.** Everything public is static; everything that acts is
local. No credential crosses the bridge; only ops and crypto proofs.

---

## 3. Modules

### 3.1 Console (`mech-os`)
- `MODEL_COMBINATOR` → live catalogue: model, context, $/1M in/out, state, `QR://` handle.
  Prices from the same feed the markets ticker reads.
- `VISUAL_ROBOT_MCP` → the **real CAD pet** (`aeMountPet`), states and receipts, not theatre.
- `SPATIAL_GATEWAY :: 4D_CORE` → the **measured** locomotion block (+4.1868 m, gait, verdict).
- New: `LLM_STORE` window → intent box + plan view + receipt view.

### 3.2 Conductor (Hermes)
- Intent parser → plan object.
- Catalogue resolver (which leaf, which model, which cost).
- Custody (keys held locally, referenced by id).
- Dispatch + fan-in (one truth from N receipts).
- Memory (operator preferences, white-label profile).

### 3.3 Bridge
Ops: `store.catalogue`, `store.quote`, `store.plan`, `store.run`, `store.receipt`,
`pet.state`, `locomotion.trace`. Every op returns `{ok, plan|result, receipt}`. Refusals are
results, not errors.

---

## 4. Contracts

Receipt (hash-chained, same shape as `tinyorigin`):
```
H(prev ∥ ts ∥ op ∥ plan ∥ result ∥ evidence)
```

Catalogue entry:
```
id · provider · context · in_per_M · out_per_M · local_capable · license · receipt_of_source
```

Plan (never executed silently):
```
intent · model · leaf · estimated_cost · approver · deadline · receipt
```

---

## 5. The conductor loop

1. Human types intent in the console.
2. Console → bridge `store.plan`.
3. Conductor resolves catalogue + leaf, writes a plan, **stops**.
4. Human approves (explicit). No approval, no act.
5. Leaf runs; receipt returns through the same bridge.
6. Console shows plan + receipt side by side. Fan-in: N leaves → one truth.

---

## 6. Built for LongCat 2.5 Ultra Max

The build is designed so a long-context, tool-using agent can execute it **without holding a
wizard's opinion** — every stage is specified as a gate the agent can run and prove:

- **Long-horizon:** the spec is the contract; the agent carries it across sessions and hands
  off by writing skills, not by re-explaining.
- **Tool orchestration:** each stage names the exact tool (`terminal`, `read_file`, `patch`,
  `browser_exec`, `delegate_task`) and the exact artifact it produces.
- **Parallel fan-out:** independent modules (catalogue, pet panel, spatial panel, bridge) are
  separable and merge behind a PASS gate.
- **Self-verification:** every stage ends with a command that proves it, and a receipt.
- **Procedural memory:** each completed stage lands as a skill entry so the next session starts
  from the mechanism, not the recollection.

Capability is used where it pays: generation, delegation, verification — **not** as a
substitute for a gate.

---

## 7. Governance

- Plan → approval → act. Address is not permission.
- Motion/spend requires a bound human.
- Custody never moves. Keys stay on Victus; the page never sees one.
- Refusal is a result and is logged.
- One surface, one responsibility: console renders, bridge brokers, conductor decides, leaf runs.

---

## 8. Build stages

| # | stage | gate (measured) |
|---|---|---|
| 0 | catalogue into `MODEL_COMBINATOR` | live prices render; source named |
| 1 | loopback bridge `store.*` | op returns a receipt; refusal paths return `ok:false` |
| 2 | intent → plan (no execution) | plan shown, nothing ran, `executed:false` |
| 3 | approval gate + run | receipt hash verifies; without approval, no run |
| 4 | pet panel wired | real atlas draws; state changes measured |
| 5 | spatial panel wired | measured locomotion numbers shown, verdict text present |
| 6 | white-label the console | visitor's mark applies; nothing defaults to æ |
| 7 | estate-wide rollout | atlas pages carry it; drift zero |

Each stage: artifact + receipt + continuity entry.

---

## 9. White-label

The console is the product. The white-label layer already proven on the home (glyph, name,
accent, persisted locally) extends to the console: the operator wears it, the store keeps its
data. Nothing defaults to æ.

---

## 10. Verification

One command per stage, plus: the console renders offline; the bridge refuses an unapproved
`run`; a receipt recomputes; the drift sweep stays clean.

---

## 11. Blockers, honestly

- **Static host:** no direct agent call from github.io — the bridge is mandatory, not optional.
- **Local inference:** local model capability bounds what the leaf can serve; the CUDA_MCP²
  route is the fallback and is not yet measured end-to-end.
- **Catalogue truth:** prices are a third-party feed; they must be quoted with their source and
  timestamp, never as our own rates.
- **Governance:** until stage 3 lands, the console is a viewer. Do not describe it as operable.
