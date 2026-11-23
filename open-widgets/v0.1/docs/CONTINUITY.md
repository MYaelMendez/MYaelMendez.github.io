# ae Open Widgets / review checkpoint / 2026-10-20

Repository: MYaelMendez/MYaelMendez.github.io.
Branch: feature/ae-open-widgets-v01.
Inspected base: 151c6b3a4dd85fadace959cb85bd3028e28c765e.
Scope: new standalone module at open-widgets/v0.1; no merge or deployment.

## Preserved decisions

- Full 9:16 carousel scenes are independent environments, not miniature dashboard tiles. The viewport is a native composition rather than a limit on other screens.
- Drawers provide depth; carousels provide breadth; heterogeneous mixtures provide composition.
- Widgets nest recursively and preserve local state. Runtime depth and node limits prevent unusable rendering; focus offers a larger working view.
- Compostable MoW: reuse, fork, retire and regenerate useful structures, without passing private values or authority.
- Origin x0:y0:z0:ae:ae and public x0:y0:z:0:ae:ae:ae are represented with the user's ae ligature in code. They are navigation/design labels, never grants.
- Human intention is the pivot, not a health-service integration. No partner-specific services or external communication were added.
- Chat and the existing OpenAI Site remain peer destinations; this standalone module does not install an in-chat widget, edit the Site, or assert shared sessions.

## Actual implementation

Four scenes; local note/counter/checklist/mixture nodes; stateful drawers; subtree focus; identity-preserving editing; fresh-ID template fork/regrow; privacy-filtered public layout review/export; disabled OpenAI client; trusted-host backend adapter contract; fixed Responses API transport; local HTTP server with a frontend asset allowlist; tests and documentation.

The local model of MoM/MoA is a binding architecture, not a connected multi-model fleet. No external agents, email, GitHub writes, payments or public publishing occur from the UI.

## Next gates

Review the diff. Reproduce the tests on target devices and a real HTTP(S) browser. Select and implement a server authentication provider, verify model entitlements and budget limits, review credentials outside chat/public source, and separately authorize a bounded live API test. Any merge, deployment or Site integration needs its own approval.

See VALIDATION.md for performed versus unperformed checks. Do not convert a DOM test into a live-integration claim.
