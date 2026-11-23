# Chatport · Personal DAO MVP

**Status:** review branch; not merged or deployed.

## Product
Chatᵖᵒʳᵗ ^ OPENSOURCEWARE ^ æ ^ STUDIO — The chat within the chat. A conversational workspace for your personal organization. You can get work done here.

**Syntax:** `#` goal, `@` agent, `/` action. Example: `@ORCHESTRATOR #gtd /plan`.

## Implemented in this review
- Standalone, responsive portrait-friendly `/chatport/` interface.
- Local browser-based agent profile toggles and goal/task board.
- Deterministic parsing for `/plan`, `/review`, `/status`, `/do`, `/publish`.
- Explicit refusal to pretend `/do` and `/publish` perform external effects.
- Local JSON export and reset; HTML escaping of all displayed user content.
- Link to existing æ Studio Site as a peer destination.

## Not implemented
- No remote agent calls, MCP server, external action, real authentication, GitHub persistence, cross-session sync, automatic chat handoff, legal formation, payment or publishing.
- No registered global `cli://` or `dao://` protocol.
- Local storage is device/browser-scoped and not suitable for secrets.
- No claim that a proposed plan is an executed action.

## Next gates
1. Review UX and test in mobile browser.
2. Add deterministic parser tests and accessible keyboard interactions.
3. Define agent registry and human-approval contract.
4. Bind verified capabilities with scoped permissions, explicit confirmations and Witness receipts.
5. Integrate with existing æ Studio without replacing it or transferring authority.

**Invariant:** Many agents. One principal. Context may propagate; authority does not.
