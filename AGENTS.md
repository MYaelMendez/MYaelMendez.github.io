# Repository continuity

Before changing the æ environment, read [AE-CONTINUITY.md](./AE-CONTINUITY.md) and [ae-destinations.json](./ae-destinations.json), then inspect the actual source and current branch. These files record project decisions; they do not grant execution authority.

## Preserve the user's architecture

- ChatGPT's chat cockpit and the existing OpenAI-hosted Site are BOTH operating destinations. Handoff is optional. Do not turn chat into a compulsory website launcher.
- The original Site is https://yael-mendez.teologia-7508.chatgpt.site/ with Site project ID `appgprj_6ac66e0abdf88191a6117303da3b35db`. Its current metadata/source must be rechecked before Site edits. Do not confuse it with GitHub Pages or create a duplicate Site/plugin.
- Resume the existing `feat/mcp-virtual-micro` / PR #15 workstream when it is still active. Recheck status; do not assume old revisions, branch state or permissions remain current.
- Reuse the existing onboarding, QR, kinetic, discovery and agent-home components. Do not rebuild them from conversational recollection.
- Preserve private context and grants outside public files. Scanning, nesting and forking do not transfer authority.
- Report source changes, tests, deployment and integration as separate states. Never label a read-back check as a browser test or a simulated event as verified execution.
- After substantive changes, update the continuity record with affected surfaces, source revisions, checks performed and remaining blockers. Keep unknowns explicit.

Read more specific directory instructions when present. Keep commits reviewable and within the user's authorized scope. A request to save or prepare work does not authorize a merge, deployment, purchase, public submission or permission change.

## Bounded verification and recovery

- Before starting, name the changed surface, completion condition and known blocker. Reuse the existing implementation; do not add another prototype to avoid an unresolved integration.
- For an unchanged asynchronous deployment, default to at most three status checks over two minutes. If still pending, preserve its exact run ID, report pending and continue independent work. Resume observation of that run later; do not create another deployment merely to check it.
- Stop observing terminal runs. Repeat a failed operation only after a relevant input, implementation or external state changed; explain that change. Never repeat a billable mutation whose outcome is uncertain without reconciliation.
- For a UI change, perform one focused browser verification after deployment. If it reveals a defect, batch the repair and stylesheet/cache version update into one revision before redeploying. Recheck the affected behavior; broaden testing only for a new concern.
- Provider rejection of a required budget or permission boundary is a blocker. Preserve the boundary, record the error and complete independent preparation; never retry with the protection removed.
- Record source, tests, deployment and verified provider execution separately. A PR number counts an issue/PR identifier, not implementations, releases or product versions. A documentation-only checkpoint does not require re-running or re-deploying the application just to repeat an existing receipt.

The current focused Codex checkpoint is [work/CODEX-WORKSHOP.md](./work/CODEX-WORKSHOP.md). Historical continuity entries remain dated records; use the focused checkpoint for the later Codex work.
