# æ Design System · v0.1

Status: independent third-party design specification. Not an OpenAI endorsement, partnership, or official OpenAI product.

## Sources
- https://openai.com/brand/
- https://developers.openai.com/plugins/concepts/ui-guidelines

## Principle: borrow discipline, not identity

Use readable platform-native typography, restrained hierarchy, generous whitespace, system controls, predictable spacing, accessibility and accurate capability labels. OpenAI trademarks and logos belong to OpenAI. Do not redraw, recolor, merge, animate, or incorporate them into the æ mark. Do not imply official affiliation or use OpenAI names as the name of this product.

## æ identity
- Primary brand: **æ · Agentic Environments**. ASCII identifier: **ae**.
- Human authority glyph: **🫵**.
- Structural motif: **æQR³** root -> environment -> capability.
- Visual DNA: minimal neutral canvas; sovereign green as a sparing accent, not a replacement for host UI colors; optional dark and light modes.
- Native system font stack. Never distribute or imitate proprietary font assets.
- 9:16 is a preferred mobile presentation, not a fixed viewport or accessibility constraint.

## Recursive scale

| Level | Surface | Role |
| --- | --- | --- |
| Nano | Emoji + short label | Discover an intent or capability |
| Pico | Single actionable card | Inspect state, scope, provider |
| Widget | Focused interactive tool | Compose and review an operation |
| Loft | Related widgets | A coherent workflow |
| Tower | Floors and queues | Human-owned environment |
| City | Forkable network | Interoperable environments |

Each scale uses the same semantic states: Proposed, Available, Connected, Authorized, Running, Verified, Failed. Never represent a proposal or prior snapshot as live status.

## ChatGPT-native presentation

Inside ChatGPT, inherit system colors, typography, spacing, and accessibility conventions. Use æ accents only in appropriate branded content and supported accent surfaces. Avoid decorative gradients, busy backgrounds, fake ChatGPT chrome, and embedding an app logo in the body when the host already provides app identification.

Outside ChatGPT, independent æ pages may use a distinct dark-green visual identity with accessible contrast and responsive layouts. Avoid co-branded lockups unless approved by the relevant owners.

## æQ + kænbæn

æQ owns intent intake, authorization requests, dispatch readiness, idempotency and event receipts.
kænbæn shows Backlog, Prepared, Authorized, Running, Review, Verified, Blocked.
Cards link to actual repository refs, workflow run IDs and Witness evidence when available. Multiplayer context sharing does not grant shared credentials or tool permissions.

## Nano ticker and teleprompt rules

Ticker entries must show source, observation time and state. No fabricated live telemetry.
Nano emojis need accessible text labels, keyboard navigation, focus indicators and usable touch targets.
Teleprompts are short, sequential, user-controlled, with pause/back/next and no automatic execution.

## Product architecture

OpenAI services: separately connected tools and services, each with its own terms and authorization.
GitHub: versioned files, issues, pull requests and Actions.
Codex and OpenClaw: distinct integration pathways; listing either does not imply connection.
æ: orchestration and interface design, not inherited authority.

**Invariant: Context may propagate; authority does not.**
