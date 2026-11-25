# THE FUNNEL — from stranger to sovereign

**Thesis.** A visitor should leave with **their own** setup: their compute funded, their identity,
their repository, their home surface — wearing *their* mark, running *our* ware. The operator then
focuses on content; the user runs capability.

White-labelling is not a feature here. It is the **default posture**: nothing on the surface may
presume æ, or presume the operator's identity.

---

## Stages

| # | stage | what the user does | automatable? |
|---|---|---|---|
| 1 | **compute** | takes the Nous referral → Portal subscription | link only — no code |
| 2 | **identity** | makes a GitHub account if they have none | instructions; no automation |
| 3 | **wire** | enters their GitHub handle | **yes** — reads *public* data |
| 4 | **home** | bookmarks / sets as home | partial — browser refuses programmatic home-setting |
| 5 | **wear** | sets glyph + name + accent | **yes** — already built (`ae-label.js`) |
| 6 | **fork** | creates their repo from the template | **yes** — "Use this template", no auth needed |
| 7 | **publish** | ships it to `*.github.io` | **yes** — steps + checklist |
| 8 | **share** | publishes their first receipted artifact | **yes** — the tiny family |
| 9 | **form** | ready → DAOLLC through the Doola referral | link only — **URL not supplied** |
| 10 | **support** | buys the operator a coffee | link only — **URL not supplied** |

### Stages 9–10 — declared, deliberately not invented

Two closing CTAs belong here: forming the business through the operator's **Doola** referral,
and a **coffee** if the ware was worth something. Neither link exists anywhere on the surface
today — a search of the whole tree found only a `doola` *keyword* in
`.well-known/skills/index.json`, and no coffee URL at all.

They are recorded as **NOT SET — operator-supplied** rather than filled with a plausible-looking
referral slug. A fabricated affiliate link is worse than a missing one: it silently misdirects
money. When the operator supplies both, they become two lines and a stage-9/10 state flips from
`needs-you` to `live`.

---

## Stage 3 — the contribution graph (the honest part)

A contribution graph needs GitHub's **GraphQL API, which requires a token**. Two options, and the
choice matters:

- **No token:** read public events (`/users/{handle}/events/public`) and render *activity*, not the
  private contribution grid. Works immediately, zero secrets.
- **With a PAT:** full graph. The token is a **secret** — it belongs in the local vault
  (`C:\æ\secrets\`), **never** in a chat, a URL, or a public surface.

**Rule:** the surface asks for a *handle*, never a password or a token. Anything the user pastes
beyond a handle is refused and redirected to the vault.

## Stage 4 — "make it your home"

Browsers do **not** allow a page to set itself as the home page. What we can do honestly:
- a visible **⋆ add to home / set as start page** control with per-browser instructions;
- an **installable PWA manifest** (name, icons, `display: standalone`, start_url) so the surface can
  be added to a dock or home screen **without** lying about it.

Declared, not implied.

## Stage 6–7 — their repo, published like ours

The transferable part is the **method**, and every item below is something we already run:

| practice | how we do it | what they get |
|---|---|---|
| one truth surface | everything serves the Pages branch | the same rule, stated |
| derived, never hand-written | `aeqr_index.py` rebuilds the index from `git ls-files` | the generator |
| claim → gate → hash | receipts beside every artifact | the tiny family |
| push through a lock | `kanban_push.py` — claim before you act | the script + why |
| continuity as memory | `AE-CONTINUITY.md`, dated sections, no stale claims | a template |
| licences stated per artifact | MIT / CC-BY-4.0 named where they apply | the table |

Forking the estate is the shortcut: the console, the store, the pet, the instruments and both brand
modules ship as the starting point, wearing a demo face until the visitor names themselves.

---

## Non-negotiables

1. **Nothing defaults to æ.** Empty label = the surface's own demo face.
2. **An address is not a permission.** Coordinates resolve; they grant nothing.
3. **A refusal is a result** with a record — the funnel says NO honestly when a step needs a human.
4. **Secrets never cross a boundary.** Handle yes; token no — vault only.
5. **Every step reports its own state.** Measured, declared, or absent.

## Build order

1. **Funnel page** — the eight stages, each reporting its own state (done / needs you / not possible).
2. **PWA manifest** — the honest version of "make it your home".
3. **Handle → activity** (no token) on the white-labelled surface.
4. **Starter kit** — template repo + publish checklist + continuity template.
5. **BYO inputs** for the tiny family, so the instruments work on *their* artifacts.
