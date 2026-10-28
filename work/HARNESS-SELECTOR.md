# License-first harness selector

Recorded October 28, 2026. The existing root and /work/ discovery widget share one selector implementation in harnesses.mjs.

Harness-code filters: Open source (default), MIT, Apache 2.0, Proprietary, All. Six initial records: Codex CLI (Apache 2.0), OpenClaw / Hermes Agent / DeepSeek Harness (MIT), Copilot CLI / Claude Code (proprietary). Each record links to the upstream license and separately describes model and service terms. These are dated discovery records, not a complete licensing audit of all dependencies or models.

Selecting creates only an inspectable proposed plan in the current tab, with no grants and no selected model or service. Changing the filter or harness clears that plan. No installation, credential request, connection, API call, purchase or execution follows selection. Reload clears the plan. The hosted Codex workshop is explicitly distinguished from the open-source Codex CLI; its existing budget blocker is unchanged.

Verification before commit: existing 22 local homepage tests plus three selector tests. Added the selector tests to the existing PR workflow. Browser/deployment evidence must be reported separately after actual publication. Physical mobile and screen-reader checks remain outstanding.

This focused record extends the repository continuity notes. No historic context, credential, budget, provider configuration or authority was republished or modified.
