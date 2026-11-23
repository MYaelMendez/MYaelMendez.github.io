# ae Open Widgets v0.1 / MoW Garden

**Open Sovereign / ae Studio / Agentic Environments**

A standalone, dependency-free review implementation of four full 9:16 scenes, stateful drawers and recursively composable local widgets. Existing `index.html`, the OpenAI Site, and partner integrations are not replaced or changed.

## Run locally

Requires Node.js 22 or newer. No npm packages or API credentials are needed for local composition.

```sh
cd open-widgets/v0.1
npm run check
npm start
```

Open `http://127.0.0.1:4173`. The server binds only to loopback and serves an explicit allowlist of frontend assets. The API adapter is disabled. Loading the page does not call OpenAI.

## What works

- Four independent full scenes: MoW Garden, Agent Fleet, Widget Factory, Public Worlds.
- Horizontal scroll/swipe, Previous/Next, direct scene controls and keyboard navigation.
- Drawers retain state while closed or while navigating between scenes.
- Notes, counters, checklists and mixtures can contain heterogeneous child widgets.
- Focus a nested widget in a larger world without losing its state.
- Fork, retire and regrow structures with new identities and without private values.
- Review and download an allowlisted JSON layout. No note values, intention, model output, credentials or permission grants are exported.
- API client and server adapter contract with authenticated-session and one-request approval gates.
- Local witness events explicitly distinguished from provider receipts and deployment.

The executable pilot limits nesting to six edges and 80 active nodes. These are rendering budgets, not a conceptual limit on the architecture. State is in memory only; reloading clears it. A layout export preserves structure, not private work.

## What is not connected

No multi-agent runner, GitHub mutation, email, payments, formation, public deployment, in-chat MCP UI installation, or synchronization with the existing OpenAI Site. MoM and MoA remain binding contracts; only local widget code operates by default. Local seeds are not AI responses.

## OpenAI backend

See [the adapter contract](docs/API-CONTRACT.md). The server-side Responses adapter is implemented, but no real request has been made for this review. Actual project/model access, credentials, authentication and quota policy must be supplied and verified separately.

The provided launcher refuses live mode without a reviewed server authentication module. It does not collect your API key in the browser or offer a fake connected account.

1. Keep `AE_OPENAI_ENABLED=false` for review.
2. For an authorized future pilot, place credentials in protected server environment variables, never in source or chat.
3. Select a model your project is authorized to use with `OPENAI_MODEL`.
4. Implement the `authenticate(req)` contract, including trusted sessions, expiry, scopes and CSRF tokens.
5. Only then enable the adapter explicitly. The included server is a loopback development harness, not a production hosting recommendation.

## Testing

```sh
npm run check
# Optional: Python playwright package and an installed Chromium are required.
python tests/browser.py
# DOM-only fallback for runners whose browser cannot navigate to local URLs:
AE_BROWSER_OFFLINE=1 python tests/browser.py
```

The fallback uses local HTML/CSS and flattened module code in about:blank. It does not validate HTTP navigation, CSP enforcement or ESM loading. See [validation evidence](docs/VALIDATION.md) for actual results and limits.

## Continuity

This implements the interaction slice from the full-9:16 / recursive-MoW design saved in PR #25; it does not merge that PR. The reviewed base is `151c6b3a4dd85fadace959cb85bd3028e28c765e`.

Read [the local continuity checkpoint](docs/CONTINUITY.md), the repository's `AGENTS.md`, `AE-CONTINUITY.md`, and `ae-destinations.json` before extending this work. Chat and the existing OpenAI Site remain peer operating destinations. This module does not redirect either one.

No new license is imposed on the existing repository, brands or dependencies by this review.

**Many widgets. Many agents. One human principal. Return value to the human.**
