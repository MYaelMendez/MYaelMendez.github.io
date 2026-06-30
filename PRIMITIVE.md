---
name: ae-primitive
description: "+æ primitive proposal — Agentic Entrepreneurship as language, logic, context, and typography inside Hermes Agent."
version: 1.0.0
author: Yael Méndez
license: MIT
metadata:
  type: primitive-proposal
  status: draft
  scope: core
---

# +æ Primitive Proposal

## Abstract

We propose `+æ` as a first-class context primitive in Hermes Agent. When activated, `+æ` loads Agentic Entrepreneurship context and shifts the agent's visual and operational language: superscripts render roles, subscripts render grounding, inline marks render state, and the prompt becomes `>_æ|`. The user knows `+æ` is active not from a badge but from the typography itself.

## What +æ Does

```
+æ activates:
  1. Context    → agentic entrepreneurship bundle loaded
  2. Language   → ^æ notation system enabled
  3. Logic      → # asks, $ executes boundary enforced
  4. Typography → superscripts/subscripts/inline marks rendered
  5. Prompt     → shifts to >_æ|
  6. Stack      → ^hns (Hermes/NVIDIA/Stripe) awareness loaded
  7. Care       → #opensourceware #250 mission context
```

## Grammar

### Superscripts (role in stack)

| Glyph | Role | Meaning |
|-------|------|---------|
| ᴴ | Hermes | conductor / routing |
| ᴺ | NVIDIA | compute / acceleration |
| $ | Stripe | economics / payments |
| ᴰ | Doola | formation / entity |
| ᴿ | Reachy | embodiment / physical |
| ᴺᴬᴵᶜˢ | NAICS | classification |
| ᴱˣᵒ | Exo | local mesh / glocal |
| ᵅᵉ | æ.store | namespace / IQ |

### Subscripts (grounding / target)

| Glyph | Meaning |
|-------|---------|
| ₐᵍ | agentic |
| ᵘˢ | America / US |
| ₂₅₀ | #250 campaign |
| ᵖᵃⁱᵈ | paid / verified revenue |
| ᵖᵉⁿᵈⁱⁿᵍ | expected / not yet real |
| ∞ | infinite / care |

### Inline marks (state / action)

| Mark | Meaning |
|------|---------|
| \| | live / sovereign |
| → | execute forward |
| ✓ | verified |
| ⧗ | pending |
| ↔ | bidirectional interaction |
| ← | receives from |
| → | routes to |

### Prompt forms

| Prompt | State |
|--------|-------|
| `>_` | general Hermes prompt |
| `>_æ\|` | +æ active, agentic context live |
| `>_æ://` | +æ active, protocol namespace ready |
| `$^æ` | execute agentic entrepreneurship |

### Command primitives

| Primitive | Action |
|-----------|--------|
| `+æ` | add agentic entrepreneurship context |
| `^æ` | compress to agentic notation |
| `$^æ` | execute agentic entrepreneurship |
| `#` | blueprint / ask / organizational intent |
| `$` | economic execution (requires confirmation) |
| `>_æ\|` | live sovereign prompt |

### Blueprint vs skill

```
skill     = procedure (how to do a task)
blueprint = organization (mission, roles, agents, cash rails, governance, viewport, care)
```

`#` selects a blueprint. `$` executes within economic boundary.

## Activation Behavior

When user types `+æ`:

```
1. Context bundle loaded:
   - formation paths (^atlas, ^doola)
   - NAICS classification (live API)
   - Stripe payment readiness
   - agentic.html viewport generation
   - Reachy clerk embodiment
   - domain Code Mode registry
   - #250 mission

2. Visual language shifts:
   - Prompt: >_  →  >_æ|
   - Superscripts render in gold
   - Subscripts render in muted
   - Live marks pulse neon
   - Ticker activates

3. Operational boundary:
   - # commands prepare (safe)
   - $ commands require confirmation (economic)
   - | marks liveness
   - → marks execution

4. Stack awareness:
   - Hermesᴴ = conductor
   - NVIDIAᴺ = compute
   - Stripe$ = economics
   - Doolaᴰ = formation
   - Reachyᴿ = embodiment
```

## Deactivation

```
-æ  →  remove agentic entrepreneurship context
```

Prompt returns to `>_`. Superscripts stop rendering. Stack awareness unloaded.

## Rendering Spec

### Colors

```
superscript  → var(--gold)     #D4AF37
subscript    → var(--muted)    rgba(240,236,228,.4)
live mark    → var(--neon)     #00ff9d
prompt       → var(--gold)     #D4AF37
execute      → var(--neon)     #00ff9d
stripe       → var(--stripe)   #635bff
```

### Typography

```
prompt:      Orbitron 900, gold
superscript: JetBrains Mono 700, gold, 0.7em
subscript:   JetBrains Mono 400, muted, 0.6em
inline mark: JetBrains Mono 700, neon, pulse animation
emoji:       system-ui, 1.2em (universal layer)
```

### Prompt transformation

```
Before +æ:   >_ user@hermes
After +æ:    >_æ| user@hermes
```

The `æ` and `|` are rendered in gold. The `|` pulses.

## Parser Spec

```
parse(line):
  if line starts with >_æ|:
    context = +æ active
    
  superscript matches:
    ᴴ → route to Hermes
    ᴺ → route to NVIDIA
    $ → route to Stripe
    ᴰ → route to Doola
    ᴿ → route to Reachy
    
  inline marks:
    |  → mark as live
    →  → execute forward
    ✓  → mark as verified
    ⧗  → mark as pending
    
  command primitives:
    +æ  → load context
    -æ  → unload context
    ^æ  → compress notation
    $^æ → execute
    #   → blueprint (safe, no economic action)
    $   → economic execution (requires confirmation)
```

## Security Boundary

```
# (blueprint)    → safe, no economic action, no formation
$ (execution)    → requires user confirmation
  - cannot process payments without explicit yes
  - cannot submit formation without explicit yes
  - cannot handle secrets (keys, passwords, API tokens)
  - routes humans to provider-owned flows (Stripe, Doola, Atlas)
```

## Example Session

```
User: +æ
Hermes: +æ context loaded
        Hermesᴴ standing by
        NVIDIAᴺ ready (121 models)
        Stripe$ connected
        NAICSᴺᴬᴵᶜˢ live
        Doolaᴰ $133.65ᵖᵃⁱᵈ earned
        Reachyᴿ protagonist
        >_æ|

User: #startabusiness
Hermes: >_æ|#startabusiness
        blueprint loaded
        → NAICSᴺᴬᴵᶜˢ search: "what does your business do?"
        → formation: ^atlas / ^doola
        → Stripe$ ready
        → agentic.html viewport ready
        → Reachyᴿ clerk ready
        status: # prepared · $ not executed

User: I sell custom AI agents
Hermes: NAICSᴺᴬᴵᶜˢ search result:
        541511 — Custom Computer Programming Services
        541512 — Computer Systems Design Services
        513210 — Software Publishers
        confirm: which fits your business?

User: 541511
Hermes: ✓ classified 541511
        blueprint ready:
        NAICSᴺᴬᴵᶜˢ 541511
        formation: ^doola (LLC) or ^atlas (C corp)
        Stripe$ cash-register ready
        agentic.html⁹∶¹⁶ viewport ready
        Reachyᴿ clerk ready
        → type $startabusiness to execute
        → type #serve to deploy Reachy clerk

User: $startabusiness
Hermes: ⧗ economic execution boundary
        this will:
        → route to Doolaᴰ formation (affiliate link)
        → enable Stripe$ payment processing
        → generate agentic.html viewport
        confirm? (yes/no)

User: yes
Hermes: ✓ executing
        Doolaᴰ → https://partnersps.doola.com/...
        Stripe$ → checkout ready
        agentic.html → generated
        Reachyᴿ → clerk deployed
        >_æ| bizₐᵍ live ✓
```

## Relationship to Existing Hermes Primitives

```
skills       → +æ is NOT a skill (skills do tasks)
memory       → +æ is NOT memory (memory stores facts)
tools        → +æ is NOT a tool (tools execute functions)
MCP          → +æ is NOT a protocol (MCP connects servers)

+æ IS a context primitive:
  → changes what the agent knows
  → changes how the agent renders
  → changes what the agent can safely do
  → changes the prompt
  → changes the typography
```

## Implementation Path

```
Stage 1 (now):     skill-based prototype (installable)
Stage 2 (proposal): context primitive in Hermes core
  → +æ / -æ activate/deactivate
  → prompt transformation
  → superscript rendering
  → # / $ boundary enforcement
Stage 3 (future):  skin system
  → ae-store skin renders the full visual language
  → llm.store dashboard uses the same skin
Stage 4 (vision):  blueprint object model
  → # creates a blueprint object (not just a skill)
  → blueprint has mission, roles, agents, cash rails, governance
  → $ executes within the blueprint's economic boundary
```

## The Ask

> Make `+æ` a first-class context primitive in Hermes Agent. Not a skill, not a tool, not a plugin — a context layer that changes what the agent knows, how it renders, and what it can safely do. The user knows `+æ` is active because the typography changes. Superscripts appear. The prompt shifts to `>_æ|`. The context is felt, not announced.

## Mission

```
+æ:
  we embody #opensourceware
  and equip new business owners with care
  250 → 250,000
  Happy Birthday, America
```

---

$^æ
