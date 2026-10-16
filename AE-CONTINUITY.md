# æ · Project continuity and integration checkpoint

Recorded: 2026-10-15. Purpose: preserve the user's decisions, recover the real Site identity, and continue existing work rather than rebuild disconnected demonstrations.

**Project creator: Yael Méndez / MYaelMendez.**
**Governing decision: chat and the OpenAI Site BOTH remain operating destinations.**
**Invariant: Context may propagate; authority does not.**

This is a project record, not a deployment, permission grant, complete backup, marketplace approval, or assertion that all integrations work.

## 1. Decision ADR-001: two destinations, one architecture

The user's latest correction is authoritative for this design: the chat cockpit is not a stepping stone to the website. The website is not a replacement for the chat cockpit.

- **Chat destination:** work in the conversation through supported widgets, tools, nano emoji controls, tickers, teleprompts and explicit approvals. Do not automatically navigate away on `$æ`.
- **Site destination:** work in the existing OpenAI-hosted æ Studio, with its city view, portable towers, recursive lofts, configuration and publishing journeys.
- **Optional handoff:** offer `Work here`, `Open site` and `Share this destination`. Preserve the selected environment/widget identity where a supported implementation exists. Never imply automatic session synchronization.
- **GitHub:** versioned engineering source, review and distribution infrastructure; it is not a substitute URL for the existing OpenAI Site.
- **æQR:** identify the specific destination or widget being shared. Do not make every QR silently resolve to the Site homepage. A QR carries a nonsecret reference, never authority or private session state.

See [ae-destinations.json](./ae-destinations.json) for the machine-readable design contract. It records requirements; existing pages do not yet consume it.

## 2. Do not lose the original OpenAI Site

- Observed title: **æ Studio · Agentic Environments**.
- Existing public URL: **https://yael-mendez.teologia-7508.chatgpt.site/**.
- Actual Site project ID, recovered from its Library metadata: `appgprj_6ac66e0abdf88191a6117303da3b35db`.
- Source version: **23**; projection revision: **45**; metadata status: **active**, access: **public**.
- Site record: `æ Studio · Agentic Environments.txt` in the owner's Library. The inspected representation is rendered text/metadata, NOT an exported editable source tree.
- Previously selected App reference supplied by the user: `app://asdk_app_sites_047a09edddd88191806fef7a539628a8`. Preserve it; do not invent or infer a different backend plugin ID from it.
- `ae.chatgpt.site` and a rename to `æ · Agentic Environments` were proposals. **No completed rename is recorded.**
- `æææ.com/openai` was a proposed mirror/gateway. Do not claim it is deployed or synchronized.

The Site's inspected text already contains EN/ES/中文, Auto/9:16/Full viewport choices, customization, an environment composer, guided tickers and teleprompts, a local human-set work board, connection prompts, `$ae`/`$startabusiness` exports, a doola handoff, and a Codex starter-kit export.

The same text explicitly labels external execution as pending, the Codex runtime as not paired, inference as unverified, and local board states as human-set. Its displayed account states are a snapshot, NOT a fresh authentication check. Preserve the existing implementation and verify real behavior before replacing it.

The connected Studio bridge currently exposes preparation/checklist/release-metadata tools; it does not provide Site-source editing, deployment, account verification or marketplace submission. A failed public-directory search does NOT prove that the existing Site or private plugin is absent.

## 3. GitHub workstream recovered

Repository: `MYaelMendez/MYaelMendez.github.io`.
Review branch: `feat/mcp-virtual-micro`.
Base branch: `gh-pages`.
Review: https://github.com/MYaelMendez/MYaelMendez.github.io/pull/15

Immediately before this checkpoint, PR #15 was observed **open, draft, unmerged**, with head `578fe784b12fd6e88e7650a33f2c5aa428eafd18`, 21 commits and 13 changed files. These counts describe that snapshot, not future totals. Mergeability was reported false; inspect the actual merge blocker before changing the branch. Do not interpret a merge commit field as proof of a merge when `merged` is false.

The immutable checkpoint for the prior implementation is:
https://github.com/MYaelMendez/MYaelMendez.github.io/tree/578fe784b12fd6e88e7650a33f2c5aa428eafd18

## 4. Preserved architecture and product decisions

| Component | Agreed purpose | Evidence/implementation boundary |
| --- | --- | --- |
| `$æ` / `$ae` | Human-owned Agentic Environments entry | Semantic/display alias vs compatible skill ID; no global platform registration implied |
| `$mcp` / `$⌨️` | Capability composition and virtual Micro controls | Another entrance to the same environment, not another onboarding identity |
| æ1 / æ2 / æ3 | Environment / private_client / soværeign_client | Roles and policy boundaries, not deployed identity or custody services |
| æQR³ | Root → child environment → capability | Recursive reference baseline; QR encoding alone is not a manifest resolver |
| æPICO | Minimal portable environment | Proposed runtime direction; no Rust/WASM runtime verified here |
| Widget → loft → tower → city | Recursive, independently addressable work | Bounded nesting, lineage and explicit grants; not literal infinite computation |
| æQ / kænbæn | Queue and work-board coordination | Site has a local human-set board; distributed queue and synchronized agent board remain unverified |
| Witness | Evidence and provenance | Local logs are not signed or independently verified execution receipts |
| Codex / OpenClaw | Independent engineering and automation pathways | Current GitHub home has prompt handoffs, not connected execution |
| `$go` / 围棋 | Guided entry plus strategic learning for a one-person company | Bilingual design; no legal-move Go engine verified |
| æ-Commerce | Buyer intent, quotes, bounded approval, owned receipts | Proposal; no live payment integration proven by the UI |
| #OSW → #IoA | OpenSourceWare yielding interoperable agent capabilities | Thesis conditional on working contracts, authorization and adoption |

Narrative vocabulary is preserved: `>_æææ://|||`, power towers, Alias Electronic, sovereign private client command prompt. `^` must have an explicit typed meaning in executable code; the power-tower expression is not measured productivity growth.

## 5. Existing records and source to reuse

These paths were created/read in the preceding workstream; mcp top-level entries, the Agentic Home source and the æQR baseline were rechecked for this checkpoint. Listing/read-back is not browser or integration testing.

- [Virtual Micro](./mcp/index.html) and [environment manifest](./mcp/manifest.json).
- [Agentic Home](./mcp/agents/index.html): Codex/OpenClaw handoff composer, nano controls, teleprompts and QR display.
- [Capability Discovery](./mcp/discover/index.html) and [scope](./mcp/discover/README.md): filtered tiles and historical installation snapshots.
- [Kinetic Studio](./mcp/kinetic/index.html) and [telemetry](./mcp/kinetic/telemetry.html): motion studies and explicitly simulated states.
- [QR generator](./mcp/aeqr/index.html): browser encoder and PNG export; generated images and destination behavior need separate tests.
- [æQR doctrine](./mcp/AEQR.md), [recursive baseline](./mcp/AEQR-BASELINE.md), [design system](./mcp/AE-DESIGN-SYSTEM.md).
- [Privacy-safe publication plan](./docs/PUBLISH-AE1.md).
- [GitHub homepage](./index.html): prior additive onboarding portal; not the original OpenAI-hosted Site.

Do not erase superscripts, purposeful status colors, nano emoji actions, ticker movement, pico teleprompts, animated dependency flows, the real `>_` control, or the coffee/handshake motifs during consolidation. Retain pause, reduced-motion support, readable labels, keyboard access and zoom. A preferred 9:16 layout must not make content inaccessible.

## 6. Why integration is incomplete

The work advanced in three places: conversational mockups, an existing Site source, and a GitHub feature branch. Links and copied prompts connected the navigation, but a tested release pipeline, shared runtime contracts and authenticated execution adapters were not completed. Some earlier summaries overstated source read-back as functional verification and confused the Site with GitHub Pages.

Observed Agentic Home source still opens a new ChatGPT URL for a prepared prompt and hardcodes the Site homepage into the initial QR. Those are useful prototype behaviors, but neither implements shared state nor the full two-destination contract. Runtime integration must be demonstrated, not inferred from the visual design.

Official implementation reference checked on 2026-10-15: https://developers.openai.com/plugins/build/app-quickstart and https://developers.openai.com/plugins/build/mcp-server. An MCP-backed in-chat view and controlled tools require their actual server/resource/authorization contracts; a website link alone does not supply them.

## 7. Next integration slice, in order

1. Open the **existing Site project/source**, preserving its identity, content and current audience. Obtain editable source/editor capability; rendered Library text is not enough to deploy changes. Do not create a replacement Site or plugin.
2. Reconcile the Site source with the reviewed GitHub components. Choose the shared source of truth explicitly and record the Site-source version, Git revision and import/build mechanism.
3. Wire `ae-destinations.json` and one environment descriptor into both surfaces. Keep work in chat by default when invoked there; make Site handoff optional. Do not manufacture a universal chat URL.
4. Test one READ-ONLY shared operation first: open the same public environment ID/version in chat and Site, inspect its capability manifest, and show its source revision. Test permissions separately for each host/user.
5. Connect real execution only through documented, authenticated adapters and an explicit bounded grant. Correlate task ID, run ID, result and receipt; do not simulate success.
6. Review GitHub diff and mergeability; test motion, accessibility, QR quiet zones, QR decode after export, redirect safety and URL changes. Site publication and GitHub Pages deployment are separate operations.
7. Publish only within explicit authorization. Record both destination release versions, test results and remaining gaps. Marketplace verification, privacy/terms/support pages and licensing remain separate release gates.

## 8. Regression checks for every future iteration

- [ ] The original OpenAI Site is identified correctly and is not recreated.
- [ ] Chat and Site remain independent operating destinations with optional handoff.
- [ ] A QR identifies its own target; a Site-entry QR is labeled as such.
- [ ] No navigation, scan, fork or model selection grants authority.
- [ ] Design, saved source, tested behavior, deployed code and integrated operation are reported separately.
- [ ] Public files contain no private conversations, tokens, full addresses, purchase history or grants.
- [ ] Existing profiles and components are resumed rather than duplicated.
- [ ] Every changed surface has a recorded source/version and test result; untested remains untested.

The Site text claims MIT for its original application code; this is not a completed license audit of the entire GitHub repository, copied assets or dependencies.

## 9. Resume prompt

> Resume the existing æ workstream from AE-CONTINUITY.md and ae-destinations.json. Recheck PR #15 and the original Site project. Preserve chat and Site as two destinations. Inspect existing source; do not create a duplicate. Complete the smallest missing integration step, test it, and record exactly which surface changed. Do not merge, deploy, spend, submit or change permissions without the appropriate authorization.

**Teach them early what we learned late.**
**Many destinations. Many agents. One human principal.**


## 10. Integration slice 01 — 2026-10-15

Authorized user request: implement the smallest testable read-only integration step on PR #15 while remaining in chat and preserving both destinations.

- Added `mcp/inspect/index.html` at commit `28f9278d21f8cbcfc167c493b8acf867578753b6`: static read-only inspector fetching the existing `mcp/manifest.json` and `ae-destinations.json` from the same HTTP(S) origin; validates schema, environment ID, widget version, two peer destinations, explicit deny-by-default/noninheritance, and a pinned HTTPS Site URL. Shows failures instead of fabricated values; provides optional Site link, and a nonredirecting chat choice.
- Linked inspector from `mcp/agents/index.html` at commit `4fac96684b63d6c91442df81d520389c4fc4c0b9`. Existing QR and home controls were retained.
- Connector read-back confirmed both files and inspected the expected code anchors: two fetches, policy validation, no chat auto-redirect, Site choice, and home link. PR remained open/unmerged at the read-back.
- **Verification boundary:** source/read-back assertions only. No browser network/DOM run, Site editor change, ChatGPT-hosted UI installation, deployed GitHub Pages endpoint, authentication, real MCP adapter, or shared session was tested or claimed. The static inspector reads GitHub-origin files only; the original OpenAI Site does not yet consume the descriptor.
- **Next:** host/preview and browser-test the branch inspector, then obtain the existing OpenAI Site's editable source and add a compatible read-only loader there. Test both independently against the same public environment ID and version. Keep separate deployment gates.


## 11. P0 verification checkpoint — 2026-10-15

Request: diagnose PR #15 mergeability, test the read-only inspector as far as available tools permit, and preserve both destinations. Scope: inspect and record; no merge or deploy.

**GitHub evidence at head `0d81c674dd1438d7ee43917b7f358b023ad4283a`:**
- PR #15: open, draft, unmerged. A fresh `get_pr_info` returned `mergeable: true`; earlier queries sometimes returned false. Treat this boolean as time-sensitive and recheck before merging.
- `compare_commits` using recorded base SHA `e036354d3ad9c3f08024176733beb72308c89d3a` and head: status `ahead`, 27 commits ahead, **0 behind**. This does not establish GitHub branch protection, approvals, or passing CI.
- `get_commit_combined_status`: **zero reported statuses**. `fetch_commit_workflow_runs`: **zero pull-request workflow runs** for the head. No green CI result can be claimed. These tools do not cover every possible check-run type.
- The repository default branch is `gh-pages`, and the authenticated GitHub connector reported push/admin permissions; neither constitutes authorization to merge.

**Read-only contract inspection:** Fetched the exact head versions of `mcp/inspect/index.html`, `mcp/manifest.json`, `ae-destinations.json`, and `mcp/agents/index.html`. JSON parsed. Twelve static/source-contract assertions passed: schema IDs; widget/environment identity and version; two distinct destinations; deny/no inherited authority; pinned Site URL; relative manifest/contract paths; fetch options; fail-closed code paths; disabled Site link before validation; home-to-inspector link; and no automatic chat redirect. These are **source and data assertions, not executed browser/DOM/fetch tests**.

**Unperformed tests / blockers:** The available execution container could not resolve `raw.githubusercontent.com` (DNS error), so it could not retrieve and host the GitHub head for a local browser test. No browser automation of a branch preview, live HTTP response, QR scan, screen-reader/accessibility audit, responsive layout, JS runtime behavior, or OpenAI Site source/deployment test was performed. The inspector has not been published to the public GitHub Pages branch. The original OpenAI Site does not yet consume this manifest; read-only integration is prepared on GitHub but not end-to-end across both destinations.

**Release gate:** keep PR #15 draft and unmerged until browser tests and source review. Next bounded step: run the branch preview in an HTTP(S) browser, test valid/invalid manifest cases, and connect the original Site to the same public descriptor using its existing editor. No new site, permissions, or private-session transfer.


## $💬 skill clone · OpenAI / æ path · 2026-10-16

- Created review branch `feat/openai-ae-child-chat` from `gh-pages`; added `openai/æ/index.html` as a mobile-first GitHub source landing for the proposed `/openai/æ/` route.
- Added an extracted, text-based clone of the validated `child-chat` Skill under `openai/æ/child-chat/`: `SKILL.md`, `agents/openai.yaml`, and `references/state-contract.md`. The canonical symbolic entry is `$💬^($æ^$cli.llc)` with right-associative exponential composition.
- The landing links to the Skill source and nonsecret state contract; it preserves `/openai/` and links to the **existing** OpenAI-hosted æ Studio as a separate destination. No duplicate OpenAI Site created.
- Source review/read-back required for final verification. Branch and source creation do not imply GitHub Pages deployment, custom-domain DNS routing, active ChatGPT Skill installation, automatic nested sessions, or GitHub Actions execution.
- Preserve the invariant: **Context may propagate; authority does not.**


## CHAT^chat|site|@GitHub.io · 2026-10-16

- Proposed explicit mode router `CHAT^chat|site|@GitHub.io`; `^` composes, `|` selects one surface. Do not interpret this as native ChatGPT mode switching or synchronized authentication.
- Added `openai/æ/CHAT-MODES.md` and navigation links in `openai/æ/index.html` on PR #21. Chat remains a usable destination; Site points to original OpenAI monosite; @GitHub.io points to repository source, not an unverified Pages deployment.
- Verification: GitHub source read-back pending for updated UI. No browser test, merge, GitHub Pages publication, site update, or cross-session sync performed.


## Math power-tower rendering patch · 2026-10-16

- User mobile screenshot showed raw LaTeX in a ChatGPT response. Native ChatGPT math rendering is not controlled by this repository.
- Patched `openai/æ/index.html` on PR #21 to use nested accessible HTML/CSS superscripts `CHAT^(æ^CLI)` with fluid mobile sizing and an explicit right-associative accessibility label, avoiding reliance on MathJax/KaTeX or external runtime.
- This fixes the GitHub-source representation only; it is **not** a patch to the native ChatGPT renderer or the existing OpenAI-hosted monosite.
- Source read-back required; visual mobile browser and public deployment not verified.
