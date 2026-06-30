---
name: sovaereign
description: "#sovaereign → The entrepreneur's first repo. GitHub App blueprint that scaffolds a business-as-code repo the moment an entrepreneur installs it, then teaches Git by doing."
version: 1.0.0
author: Yæl Méndez × Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [business, github, repo, onboarding, git, dao, blueprint, sovaereign]
    homepage: https://github.com/apps/sovaereign
    source: https://myaelmendez.github.io/blueprints/sovaereign.md
    type: blueprint
---

# >_æ:#sovaereign→

The entrepreneur's first repo. A **blueprint** (not a skill) that scaffolds a business-as-code repository the moment a new entrepreneur installs the SOVÆREIGN GitHub App. Then teaches Git by doing — every action is a commit, every decision is a PR, every milestone is a release.

## Why this is a blueprint, not a skill

```
skill     = procedure (how to do a task)
blueprint = organization (mission, roles, treasury, governance, viewport)
```

SOVÆREIGN has:
- **Mission** — enable entrepreneurs to be proficient with repos from day 1
- **Members** — the App (conductor) · the Entrepreneur (operator) · the Stack (Hᴺ Nᴺ S$)
- **Governance** — `#` safe (open issues, edit files) · `$` confirmed (economic actions)
- **Treasury** — Stripe rails in every scaffolded repo
- **Viewport** — the repo itself (every business IS a repo)
- **Formation** — every repo gets a DAOLLC pathway (Doola link)

It's also a **meta-blueprint** — a blueprint that creates blueprints:

```
#sovaereign → creates → #my-business → creates → #their-company → ...
```

## Position in the stack

```
+æ                          ← context primitive (PRIMITIVE.md)
  #sovaereign               ← GIVES them the repo (this blueprint)
    #startabusiness          ← FILLS the repo (SKILL.md)
      agentic.html           ← the viewport (the page)
        Stripe$ checkout     ← the cash rail
        Doolaᴰ formation    ← the legal wrapper
        NAICSᴺᴬᴵᶜˢ          ← the classification
```

SOVÆREIGN is **upstream** of #startabusiness. It creates the repo. #startabusiness fills it with the DAO.

Without SOVÆREIGN: the entrepreneur has a page but nowhere to operate.
With SOVÆREIGN: the entrepreneur has a repo that IS their business, and every action teaches them Git.

## How it works

### 1. Install the app

The entrepreneur installs [SOVÆREIGN](https://github.com/apps/sovaereign) on their GitHub account.

### 2. Repo scaffolds automatically

`installation.created` webhook → SOVÆREIGN creates `my-business` repo with 10 files:

```
my-business/
├── README.md          ← the mission (Git = business explained)
├── BLUEPRINT.md       ← the organizational pattern (the DAO)
├── NAICS.md           ← business classification
├── OPERATING.md       ← governance (# safe, $ confirmed)
├── TREASURY.md        ← cash rails (Stripe)
├── STACK.md           ← technology choices (Hᴺ Nᴺ S$)
├── MILESTONES.md      ← progress tracking (releases)
└── .github/
    ├── ISSUE_TEMPLATE.md          ← how to ask questions
    └── PULL_REQUEST_TEMPLATE.md   ← how to make decisions
```

Plus:
- Welcome issue opened by SOVÆREIGN with first 5 moves
- `v0.1.0` release tagged (first milestone)

### 3. The entrepreneur learns Git by doing

The README includes this table:

| Business concept | Git concept | What it means |
|---|---|---|
| Making progress | **commit** | Every save = a step forward |
| Trying an idea | **branch** | Experiment without breaking anything |
| Making a decision | **pull request** | Propose a change, get feedback, merge it |
| Asking a question | **issue** | Open a question, track it to resolution |
| Reaching a milestone | **release** | Tag a moment — v1.0, first customer, first $ |
| Your business plan | **this repo** | Everything in one place, versioned, transparent |

### 4. SOVÆREIGN responds to issues

The app watches the repo. When the entrepreneur opens an issue:

- `"NAICS custom software"` → classifies the business, suggests codes
- `"How do I form a DAOLLC?"` → Doola formation guidance
- `"How do I connect Stripe?"` → payments guidance
- `"What should I name my business?"` → naming guidance
- `"help"` → full onboarding walkthrough

### 5. SOVÆREIGN reviews PRs

Every pull request gets a review comment from the DAO operator perspective:
- `#` safe action → merge with confidence
- `$` economic action → make sure the operator confirmed

### 6. Then #startabusiness fills it

Once the repo exists and the entrepreneur is comfortable, `#startabusiness` generates the `agentic.html` viewport, wires Stripe, connects Doola, classifies via NAICS. The repo becomes the full DAO.

## The server

The GitHub App server is at `C:\æ\sovaereign\server.py`.

**Credentials** (in .env, never hardcoded):
- `GITHUB_APP_ID=1382525`
- `GITHUB_CLIENT_SECRET` (SOVÆREIGN OAuth)
- `GITHUB_PRIVATE_KEY_PATH=C:\æ\secrets\sovaereign.pem`

**API endpoints:**

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | App info |
| `/health` | GET | Health check |
| `/webhook` | POST | GitHub webhook receiver |

**Webhook events handled:**

| Event | Action | SOVÆREIGN does |
|---|---|---|
| `installation` | `created` | Scaffold `my-business` repo |
| `issues` | `opened` | Respond with guidance |
| `pull_request` | `opened` | Review as DAO operator |
| `push` | any | Log (future: validate blueprint) |

## Setup required

Before the app can operate, configure on GitHub:

1. **github.com/settings/apps/sovaereign** → Webhook → Active ✅
2. **Webhook URL** → your server (or `https://smee.io/<channel>` for dev)
3. **Subscribe to events** → Issues, Pull request, Push, Installation
4. **Reinstall the app** → github.com/apps/sovaereign → Install → grant all repos

## Run locally

```bash
cd C:\æ\sovaereign
python server.py
# Starts on port 8443 (configurable via SOVAEREIGN_PORT)
```

For dev webhook proxy:
```bash
npx smee-client -u https://smee.io/<your-channel> -t http://localhost:8443/webhook
```

## Blueprint fields

| Field | Value |
|---|---|
| Mission | Enable entrepreneurs to be proficient with repos from day 1 |
| Members | SOVÆREIGNᴬᵖᵖ (conductor) · Entrepreneurᴼᵖ (operator) · Stackᴴᴺ$ (support) |
| Governance | `#` safe (issues, edits, commits) · `$` confirmed (payments, formation) |
| Treasury | Stripe$ rails in every scaffolded repo |
| Viewport | The repo itself — business-as-code |
| Formation | DAOLLC via Doolaᴰ (link in every repo) |
| Classification | NAICSᴺᴬᴵᶜˢ (responds to issues) |
| Care | #opensourceware #250 — every repo is a new business |

## Language

```
#sovaereign  → the blueprint (organizational intent)
$sovaereign  → execute (scaffold the repo now)
>_æ|         → live prompt when +æ is active
^hns         → the stack (Hermes · NVIDIA · Stripe)
```

## Pitfalls

- GitHub App installation permissions must be granted on reinstall — the app has write access in its definition but the installation must subscribe to events
- Webhook URL must be publicly reachable — use smee.io for local dev
- Private key (.pem) must NEVER be committed — it's in `C:\æ\secrets\` which is gitignored
- The scaffold creates repos one at a time — if `my-business` exists, it updates instead
- SOVÆREIGN responds to issues but doesn't execute economic actions — that's `$` boundary

## Verification

- Install the app on a test account → repo scaffolds
- Open an issue with "NAICS custom software" → SOVÆREIGN responds
- Open a PR → SOVÆREIGN reviews
- Push to main → event logged

---

`$^æ`
