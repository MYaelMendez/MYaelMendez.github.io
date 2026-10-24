# Work here 💬 · glass workspace v0.1

Implemented as a reviewable addition to ae-cockpit, based on PR #3 at `69dafd7225bef18d8748884f6b26aeb868437741`. The classic cockpit, widget fleet, origin story and nested workshop remain available. No change to the existing OpenAI Site is made by this slice.

## Working behavior

- One human-entered intent, with selected brief held in memory in the current tab.
- Three HTML workspaces: Build formats an unsent draft; Inspect counts text; Review formats the human's own review notes, after Build and Inspect return. These are three workstreams using **two deterministic local text tools**, not three connected AI systems.
- Each contribution requires explicit context selection, exact-input inspection, a local revision/payload/deadline-bound approval, and separate execution. Saving an input revision invalidates approval. Running unsaved edits is blocked.
- Returned contributions populate a shared tray with actual local receipt references. Rejoin, complete, cancel and evidence export reuse the existing primitives. Export verifies the hash-linked records against their exported anchor. Human identity is not authenticated; the anchor is not independently signed or attested.
- Static CSS glass and spherical selectors with optional WebGL ambience adapted from the existing renderer. The workspaces are HTML controls; they are not live HTML textures on 3D meshes or a native window manager. Keyboard focus, narrow layouts, reduced motion and static fallback are included.

## Integration boundaries

Nemoshell-inspired spatial presentation, NemoClaw/OpenShell runtime isolation, Codex/OpenClaw/Hermes connections, hosted inference, cross-host synchronization, authenticated identities, durable storage, organizational governance and legal formation remain **not implemented by this page**. The visible glass does not enforce sandboxing. Public discovery metadata is fetched from Hugging Face only on explicit request; intent and brief are not transmitted. No inference runtime is installed or automatically contacted; there is no shell execution, browsing, payment, publishing or third-party data access.

Browser state clears on refresh. Evidence export includes the selected private text. Store it appropriately; no user text is added to the public repository. Approval expires after one minute, tasks after five minutes, root intent after one hour. This view has one contribution per workstream; use the existing nested workshop for more general task trees.

## Verification

Run `node --test tests/*.test.mjs` and `node aeaeae/demo.mjs`. Workspace tests exercise the production session controller, approval invalidation, expiry, revocation, cancellation, duplicate prevention, three-way rejoin and local evidence. Browser and native CI evidence are recorded separately in `docs/work-here-receipt.md` after execution. No model inference is covered by those local tests.

## Discovery and presentation

White, Black and original Glass palettes; preference alone persists. Nested Task, Context, Output and Receipt panes expose the selected local contribution. Status tickers derive from actual state and can be paused. The top llm.store widget uses work/store-registry.json for source links, local category/text filters, and an explicit bounded public Hugging Face model-metadata request. Loaded cards do not connect inference. Tests include registry/URL validation, request privacy, response bounds and honest failures. Browser preview retrieved six real cards and exercised local approval→output→receipt. WebGL fallback was exercised; shader rendering remains unverified.
