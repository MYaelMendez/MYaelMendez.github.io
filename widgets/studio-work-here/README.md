# Work here · æ Studio

The exact nested widget shown in chat, preserved as versioned source alongside the existing homepage. The human directs three local viewports: Build → Inspect → Review. Work, llm.store discovery links, and connection boundaries remain nested inside one portrait environment. Glass, White, and Black appearances are selectable.

## Reproduce

No dependencies or API keys are required. From this folder:

```sh
node build.mjs
node --test widget.test.mjs
python3 -m http.server 8000
```

Open `http://localhost:8000/`. `index.html` is the generated standalone page. `widget.html` is the original in-chat fragment, byte for byte; its SHA-256 is recorded in `manifest.json`. Run the build again after intentional edits and update the manifest hash after review. A hash proves consistency with the recorded bytes, not identity or independent attestation.

## What this demonstrates

- A conversation can contain a reusable, inspectable interface with nested local state, useful controls, and explicit boundaries.
- Local formatting returns the exact intent in a draft template. Inspection measures the draft. Human review records entered notes.
- Controls preserve intent across navigation. Edits clear affected contributions and approvals. Events record actual local interactions.
- The same fragment can be rendered by a compatible chat host or wrapped as a standalone page without rewriting its interaction code.

## Evidence and limits

Six Node tests exercise source integrity, standalone inclusion, approval/dependency gates, actual returned output/events, invalidation, navigation, text rendering, and absence of API transports. The control fixture is deliberately small; these tests do not establish browser rendering, screen-reader accessibility, mobile behavior, or provider integration. The recorded original chat run used equivalent fixture checks. No browser test or CI result is claimed by these files.

State exists only in the current rendered instance. Reloading loses it. The fragment does **not** synchronize with the homepage or the OpenAI-hosted Studio, call an AI model, authenticate a human, run Codex/OpenClaw/Hermes, isolate processes, or issue an execution grant. Event records are not signed witness receipts. External discovery links are optional navigation, not connections. The historical OpenAI connection note in the exact fragment is dated October 25, 2026; it is not a live status probe.

This is a captured chat companion, not a replacement for the richer existing `/work/` implementation. Chat and the OpenAI-hosted Studio remain peer destinations. No homepage route, existing implementation, credentials, account access, or deployment configuration is changed by saving this source.

**Context may propagate; authority does not.**
