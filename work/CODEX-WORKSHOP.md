# Codex workshop — implementation checkpoint

Recorded October 27, 2026. This is a verified status record, not an execution grant.

## One workshop, multiple surfaces

- GitHub Pages: [homepage capability card](https://myaelmendez.github.io/#codex-capability), also exposed at [/work/](https://myaelmendez.github.io/work/#codex-capability).
- Existing authenticated Studio: [Codex workshop](https://yael-mendez.teologia-7508.chatgpt.site/codex-workspace).
- The local Build / Inspect / Review viewports remain browser text tools. The Codex card is an optional destination, not an embedded sandbox or a second agent implementation.
- The card uses native nested disclosures for purpose, selected context, permissions/budget and evidence. White, Black and Glass palettes are retained; expanded content grows naturally.

## Current capability boundary

| Capability | Evidence and limit |
| --- | --- |
| Identity and task preparation | Signed-in owner configuration and preparation were verified in the existing Studio. Tasks persist server-side. Sign-in alone does not grant paid execution. |
| Review and launch guards | Payload/hash-bound review, expiry, owner checks, idempotency and a required spending field are implemented and covered by local gateway tests. |
| Real Codex execution | BLOCKED. The last live launch returned HTTP 400, unknown_parameter for spend_control. The required $0.25 session ceiling was rejected. No successful sandbox turn, command output or test run is claimed. |
| Status, stop and evidence | Status inspection, cancellation requests, reconciliation and JSON evidence export are implemented. Their successful provider execution path remains unverified. |
| GitHub operations | Repository clone, commit, push and deployment are not connected to the workshop. |
| Shared contribution tray | Homepage contributions remain local. Workshop results are not automatically imported into that tray. |
| Spending authorization | No monthly project ceiling has been selected or configured as part of this work. No uncapped launch retry was made. |

The card's state is explicitly dated; it does not perform a live provider health check. Its external link includes no query, fragment, local intent, selected source, profile, credentials or authority. Opening the link does not start paid work.

## Revisions and verification receipts

- [PR #40](https://github.com/MYaelMendez/MYaelMendez.github.io/pull/40): optional workshop link.
- [PR #41](https://github.com/MYaelMendez/MYaelMendez.github.io/pull/41): one commit, four changed files, nested capability card. Merged as `1a506e4c88d956633f9324341c61d25441e779c8`.
- Contrast correction: `7c702982c8ee9e17765adb8388dbd56a4ce9708f`. Stylesheet version correction: `39dfe07c29e0ff156a6f704e310a4c5632834259`.
- [Native CI](https://github.com/MYaelMendez/MYaelMendez.github.io/actions/runs/40535761822): completed successfully for the card PR.
- [Final Pages deployment](https://github.com/MYaelMendez/MYaelMendez.github.io/actions/runs/40537357126): completed successfully for the stylesheet version correction.
- Local suites: 22 homepage/workspace tests and 11 Studio gateway tests passed. These are 33 test cases across two source surfaces, not 33 working integrations.
- Browser: root and /work/ card observed; permissions disclosure expanded and collapsed; signed-in Studio configuration observed. Corrected launch colors verified in White (white on dark) and Black (dark on light). Physical mobile, screen readers and successful sandbox execution remain unverified.

**Numbering:** #41 is GitHub's pull request identifier in a shared issue/PR sequence. It is not a count of 41 implementations, deployments, versions or connected agents.

## Next completion gate

Verify a supported spending boundary with an explicitly authorized amount before another paid launch. Then perform one small reviewed task and retain its provider session/turn IDs, command results and evidence. Only a verified successful turn can establish operational Codex execution. Do not substitute additional visual polish for this gate.

Follow the bounded verification rules in [AGENTS.md](../AGENTS.md). Reuse existing tasks and reconcile uncertain launches before retrying.

This focused checkpoint supersedes earlier Codex status claims where they conflict. Historical continuity text is preserved rather than republished. This documentation revision changes no credential, provider policy, runtime, budget or permission.
