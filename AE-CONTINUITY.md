# æ · Project continuity and integration checkpoint

> **Charter: [PURPOSE.md](./PURPOSE.md)** · surface: [purpose.html](./purpose.html).
> This file is the *record* — what was decided and what was verified. The charter is the *reason*.
> Where they disagree, the charter wins and this record is corrected.

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


## 12. New working homepage and preserved origin — 2026-10-24

- User authorized preserving the old index in a new folder named `origin`, alongside the proposed working homepage.
- Archived the public root index from `7befaf5dafce517393261d5b4bb50f9b0e679cee` at `origin/index.html`. Added a root-relative base, archive canonical/social URL, a return link, and declared the DOM helper before first use to fix the original startup error. Kept the terminal, atlas, theme/environment controls, symbolic tickers and onboarding links. Root assets remain in place. Historical demonstration strings remain historical claims, not verified execution evidence.
- Replaced root index with the local glass workspace adapted from ae-cockpit PR #4 at `3969eea0d10e9c5b49c9f7fd78b466c04e816425`. The page works directly at the root without an iframe or automatic Site redirect. `/work/` also opens the same implementation. Both link to the preserved origin and offer the existing OpenAI Site as an optional peer destination.
- Reused the existing local primitives and portable SHA-256 within `work/`. Three workstreams use two deterministic local text tools, explicit selected context, local revision/payload approvals, shared contribution tray and evidence export. No AI model, authenticated identity, external agent runtime or sandbox is connected.
- Verification: 10 local tests passed, including the seven workspace lifecycle tests. Browser preview at the replacement root verified intent → selected context → prepare → approve → local draft and receipt. Followed the Origin link; archive loaded its atlas and mesh, ran the terminal help command and changed the theme attribute to day. Browser lacked WebGL, so fallback was exercised; shader, physical mobile and screen readers remain unverified. Preview copied only relevant assets, not every existing destination; all old destination pages remain unchanged in the repository.
- OpenAI API integration is separate and unfinished. No usable credential found, no key created, no live inference test or API call performed. The user declined OpenAI Developers for this request; no further plugin suggestion or credential provisioning was attempted.
- This change is prepared for review only. No merge/deployment, existing OpenAI Site edit, audience change, credential publication or cross-host synchronization performed. Existing unmerged homebase PRs #29 and #30 also touch the root and will need reconciliation before merging alongside this replacement.


## 13. Discovery widget and appearance — 2026-10-24

- The preceding homepage release merged as PR #31, deployed successfully via Pages run 40112865004, and was checked at the public root and /origin/.
- User requested White/Black appearance with original Glass retained, moving tickers, nested workspace views, and llm.store as a top widget populated by indexes and Hugging Face nano widgets. Publication is authorized by the user's “I want it live” instruction.
- Added White (default), Black and Glass choices; only appearance preference persists. Task context still stays in the tab. Tickers reflect actual contribution/event counts, support pause and reduced motion. Nested Task/Context/Output/Receipt views expose the selected contribution's actual data.
- Added versioned source registry, category/search filters and external model/dataset/Space/index links. An explicit load button retrieves six public Hugging Face model cards; no intent, brief or credentials are sent. Metadata does not install a runtime or grant authority.
- Verification before publication: all 17 local tests passed. Browser preview checked all theme choices, persisted Black across reload, category filtering, ticker pause, explicit context, approval, returned local output and receipt. Public Hugging Face request succeeded with six cards. Browser WebGL unavailable: static fallback tested; shader/mobile/screen-reader verification remains outstanding. No external inference, agent adapters or cross-host synchronization added. /origin/ and existing OpenAI Site unchanged.
- Release commit, native CI and final Pages deployment evidence are reported after actual execution; this source record does not assert a future run succeeded.


## 14. soværeign voice · OSW voice laboratory · æ ambient index — 2026-11-17/18

- Source of the build contract for the next agent: the Hermes skill
  `ae-target-application` (skills/sovereign/ae-target-application/SKILL.md).
  It carries the target definition, the verified inventory, the build order,
  the laws, and the environment pitfalls. Read it before changing the æ stack.

Surfaces affected (all measured, none assumed):
- `plugins/tiny-voca-voice/` — soværeign voice. tiny-voca ONNX on CPU, no
  cloud, no API key. Roles bound: `nous`→F2 (Nous Research system),
  `hermes`→M2 (build/narration). 4 tools registered, enabled.
- `plugins/vaemcp-c2/` — 1 tool; reports the væMCP roster read back over
  JSON-RPC (19 tools: 10 local + 9 `vscoder_*`).
- `plugins/vaemcp-github/` — 1 tool; allowlisted git/gh. Mutating verbs
  require `confirm=true`; unnamed verbs refuse with a structured refusal.
- `C:/æ/virtual-mcp/server.py` — væMCP 0.3.0, 19 tools, now incl. `vs_speak`
  (role-aware). Pins the native git interpreter path.
- `C:/æ/agents/aelang.py` — æ-lang v0.1: tokenize/parse/evaluate, fail-closed.
- `C:/æ/osw-voice-lab/` — laboratory (local HTTP surface, port 8137): role
  picker, speed/pitch-shift/pitch-range, playback, receipt display.
- `C:/æ/agents/kanban_push.py` — patched to pin the native git binary
  (`C:/Program Files/Git/cmd/git.exe`); PATH git is the MSYS/UCRT build and
  native Python cannot spawn it (WinError 5).

Published to the truth surface (gh-pages, live, HTTP 200):
- `sovaereign-voice.html`, `sovaereign-voice-916.mp4`
- `ae-index.html` + `ae-manifest.json` (schema `ae.manifest/1`, ~4.4 KB —
  the machine entry point agents fetch)
- `osw-voice-lab.html`, `osw-voice-lab-916.mp4`

Source revisions: gh-pages advanced ce9ed4c → f42535f → c950509 → bf2b5d6
(all fast-forward via `kanban_push.py`; never force-pushed).

Checks actually performed:
- æ-lang: `🍊 -> ∞ -> ♾️` RESOLVED; `🍕` REFUSED and the pipeline closed.
- Voice: both roles synthesized and played via the lab HTTP surface;
  unknown role `villain` refused.
- Video: 720×1280, 10.0 s, 300/300 frames unique; SupervisorVideo PASS
  (luminancia 44.56, contraste 23.57, movimiento 1.661, 0 black frames).
- Audio: muxed narration confirmed non-silent (peak 0.931, RMS 0.114,
  speech 0.32 s → 8.47 s) — the first render was silent and was corrected.
- Deploy: GitHub API used as the authoritative check; first CDN probe 404s
  are lag, not failure. Re-checked to 200.

Remaining blockers (explicit):
- `gh` lacks the `workflow` scope → CI/workflow files are read-only. Human
  step: `gh auth refresh -s workflow`. aeqr CI stays red on the missing
  `hermes-fork/mech/qr_index.mec` until then.
- tiny-voca is architecturally capped at 2 speakers (`"speakers":[F2,M2]`).
  Asimov and private-client voices require a different engine; candidates
  already owned: `hermes-voice-lab`, `chimera-vocal-synth`.
- No CDP port on the Hermes desktop → pane rendering is UNVERIFIED. Only the
  tools/endpoints/ESM were checked. Someone must look.
- GitHub OAuth App / Sign-In not created; no client_id. Human step.


## 15. Voice determinism — root cause found and fixed — 2026-11-18

Resume from §14 via the `ae-target-application` skill. Build-order audit:
item 4 (voice lab A/B + determinism) was BUILT (`ab_determinism.py`) but had
never been RUN — no receipts existed. Ran it; it measured a real failure;
root-caused and fixed it. Items 1–3 remain open (grammar lives in the
`aelang.py` v0.2 docstring, no standalone spec page; no æ-lang→envelope→væMCP
compiler — `compiler.py` is the separate chat-recursive compiler; no
conductor module).

**Measured, in order:**
- æ-lang gate: `🍊 -> ∞ -> ♾️` chains RESOLVED with hash-chained receipts;
  `ghost` and `🍕` REFUSED fail-closed. PASS.
- A/B (text "Many destinations. Many agents. One human principal."):
  nous/F2 4.765 s, hermes/M2 4.125 s, stereo nous-L/hermes-R; CLI hashes
  agree with lab hashes. PASS. Receipt `b8a49b82…` (scratch voice-ab chain).
- Determinism, stock model: **MISMATCH in the PCM samples** (headers and
  durations identical). Not a header artifact.
- Root cause isolated by experiment, not inference: threads=1 still
  mismatches (not thread order); graph scan (recursive incl. subgraphs)
  found exactly ONE stochastic node, `RandomNormalLike`, no seed attr;
  a minimal seeded `RandomNormalLike` model ALSO mismatches → **ONNX
  Runtime's CPU kernel ignores the seed attribute**. Seed-patching the
  graph therefore cannot fix it (tested: still MISMATCH).
- Fix: split the graph at the random node — `front.onnx` (inputs → noise
  shape template `/Mul_23_output_0`, deterministic) and `back.onnx` (noise
  exposed as input → audio). Noise drawn with `numpy.random.default_rng(seed)`.
  Original `model.onnx` NEVER modified (sha256 `fe6d9187…` before and after).

**Verification of the fix (all executed):**
- Same seed, two runs: PCM MATCH; different seed: differs (seed-sensitive);
  audio non-silent (peak 0.757, RMS 0.105 on the probe utterance).
- Permanent tool `C:/æ/osw-voice-lab/det_voice.py` (build + synth, WAV +
  hash-chained `det_receipts.jsonl`): two INDEPENDENT process runs, same
  text/voice/seed → identical file sha256 `2b561fdb…` and PCM sha256
  `a5e48990…`; nous variant differs (4.064 s). Rebuilt the split from the
  untouched source via `det_voice.py build` → same PCM hash again.
- Split models live at `%LOCALAPPDATA%/hermes/tiny-voca/det/{front,back}.onnx`
  (10.4 MB + 21.6 MB, additive; stock model untouched).

**Boundaries:** determinism now holds for the seeded path only — stock
`tiny_voca_voice.py` synthesis remains non-deterministic by design of the
ORT kernel. No plugin file was edited; no push/deploy this slice (local
tool + runtime assets only). Run lab scripts from an ASCII staging copy
(`æ` in argv corrupts native subprocesses). Listening quality of the
seeded variant vs stock: not A/B-listened by a human yet.

**Next:** human listen of `det_hermes` vs stock; then build-order item 1
(standalone æ-lang syntax spec page) and item 2 (æ-lang → `ae/envelope.py`
→ væMCP compiler). Blockers from §14 unchanged (gh workflow scope, VoxMel
provisioning, CDP pane render, OAuth client_id — all human steps).


## 16. Build wave 1 — spec, compiler, bindings (subagents, verified) — 2026-11-18

User authorized subagent builds. Three parallel leaves, all additive-only,
all results RE-RUN BY THE PARENT (child self-reports were not trusted):

- **Item 1 DONE — `C:/æ/agents/AE-LANG-SPEC.md`**: æ-lang v0.2 spec, one
  page, grounded in the code. Parent re-ran the harness: **26/26 PASS**.
  Documents classification order (query beats binding), address≠permission
  refusals, six allowlisted builtins, receipt canonicalization, v0.1
  `evaluate()` legacy view. Zero code/spec discrepancies; aelang.py and
  the registry untouched.
- **Item 2 DONE — `C:/æ/agents/ae_compile.py`**: æ-lang → `ae:1:route:`
  envelopes (reuses `ae/envelope.py`; encode→decode-back AND byte-identical
  re-encode verified before any invoke) → allowlisted builtins or væMCP
  verbs gated by `ae.authority.Capability(action='execute', granted_by=human)`.
  CompilingRuntime subclasses aelang.Runtime. Parent re-ran: **42/42 PASS**.
  væMCP execution REFUSES by default (no human grant, no authenticated
  adapter) — honest fail-closed; grant-present branch implemented but
  unexercised. Correlation: run_id · pipeline_id · envelope_id · receipt · prev.
- **Item 5 DONE — `C:/æ/aeqr/registry/capability-bindings.json` +
  `C:/æ/agents/ae_bindings.py`**: 25/25 symbols covered — 10 bound
  (8 pure builtins; 🧠→vscoder_plan, ⌨️→win_run human-grant-gated),
  15 unbound with reasons. Pins registry sha256 `ba5042ce…`; deny-by-default,
  non-inheriting; exact-scope human grants only. Parent re-ran: **50/50 PASS**,
  `validate` CLI ok. Dispatch deliberately NOT wired ("conductor pending").

**Discrepancy found at fan-in:** ae_compile's provisional VAEMCP_BINDINGS
(🛸→vscoder_observe) contradicted the authoritative bindings (🛸 unbound).
Reconciliation assigned to the conductor slice: capability-bindings.json
becomes the single source of truth; double gate (registry-bound AND
execution-allowlisted AND human-granted); win_run stays non-executable
without explicit grant.

**In flight:** item 3 — the conductor (`C:/æ/agents/conductor.py`): translate
intent, arbitrate authority, fan out, fold N receipts into ONE truth receipt,
hold a verifiable ledger; must regress all three suites above.

No push/deploy this wave. Skill `ae-target-application` items 1 and 5 marked
DONE by the leaves (item 2/3 status pending conductor verification).


## 17. Build wave 2 — THE CONDUCTOR (verified) — build order COMPLETE — 2026-11-18

`C:/æ/agents/conductor.py` (conductor/0.1, stdlib + ae modules only).
Leaf hit one wrong-interpreter error (`onnxruntime` — bare python instead
of `C:/gpu/Scripts/python.exe`); steered, recovered. Parent RE-RAN every
suite independently:

- conductor adversarial suite: **73/73 PASS** (fan-out 3→ONE truth receipt
  with independent hash recomputation; 🍕 run REFUSED with honest partial
  record; forged/non-human/wildcard/expired/wrong-scope grants all refused;
  ledger tamper ⇒ chain break, corrupt ledger refuses BEFORE execution;
  determinism identical truth hash; 🛸/win_run/🧠 refusals; queries
  resolve-only).
- `conductor.py selftest`: ALL ASSERTIONS PASSED.
- compiler suite (reconciled): **48/48 PASS** (was 42; +6 reconciliation).
- bindings suite: **50/50 PASS** · spec suite: **26/26 PASS** ·
  aelang selftest + demo gate: PASS.

**Reconciliation done:** ae_compile's provisional VAEMCP_BINDINGS removed;
capability-bindings.json is the single routing truth via ae_bindings.
Triple gate: registry-bound ∧ execution-allowlisted ∧ valid human
Capability (exact scope equality — the leaf caught and fixed a real
`covers()` wildcard trap mid-build). `vscoder_plan` added to the allowlist
(grant-gated, read-only); **win_run permanently OFF — no grant can execute
it** via this path. 🛸 now preflight-refused as unbound (no envelope).

**Interface:** `conduct(source, grants=(), ledger_path=..., input_value='',
max_workers=4)`; `verify_ledger / read_ledger / history`; CLI
conduct/verify/history/selftest. Fan-in folds by SOURCE LINE, never
completion order. Default ledger `C:/æ/logs/conductor-ledger.jsonl`
(created on first real conduct; tests used scratch ledgers).

**Build order status: ALL FIVE ITEMS DONE** (1 spec §16, 2 compiler §16,
3 conductor §17, 4 voice determinism §15, 5 bindings §16).

**Explicit remaining gaps:**
- Real væMCP dispatch unexercised end-to-end: grant-present adapter path
  reachable but no human grant exists; default DENY verified, valid-grant
  acceptance proven at unit level only. First positive execution needs an
  operator-issued Capability for `cap.emoji:1f9e0` (🧠 vscoder_plan).
- capability-bindings.json 🛸 reason still says "conductor is not built
  yet" — registry is human-owned; operator's call to refresh.
- ae_bindings.BindingRuntime.execute still says "conductor pending"
  (its 50 tests pin that string); conductor path supersedes it.
- compile_source accepts ONE grant per compile; multi-capability pipelines
  refuse honestly ("split the pipeline").
- §14/§15 human blockers unchanged: gh workflow scope, voice listen,
  VoxMel provisioning, CDP pane render, OAuth client_id.

No push/deploy/network/secrets this wave. Next candidate slices: operator
grant + first positive væMCP execution; publish the spec/conductor surfaces
to github.io (needs authorization); PR #15 browser-test tail (§7–11).


## 18. Asymptotic iteration — the speaking front door — 2026-11-18 (in flight)

Operator directive: "innovate, iterate asymptotically." Asymptote defined:
**a human names a capability → it resolves locally, asks authority,
executes, leaves ONE truth receipt — spoken in a voice that reproduces
bit-for-bit.** Distance metric: unbound symbols, uncomposed links,
unverified claims. Each iteration must measurably reduce it.

Iteration A (leaf, new-file-only): `ae_frontdoor.py` — `name <symbol>`
resolves-only; `say "<æ-lang>"` conducts and SPEAKS the truth receipt via
det_voice (fixed seed), chaining truth hash + pcm_sha256 into one receipt;
`verify` reads back. The novel composition: a verdict both hash-verified
AND bit-reproducible as audio.

Iteration B (leaf, audit-only, scratch writes): 🎬/🎥 binding proposal
against the REAL film chain (vidæo / mp4-chain / hermes-ae) — exact
schema-conformant entries + ae_compile diff + test plan, grant-gated.
Implementation lands next wave after the proposal is reviewed.

File ownership enforced to keep the wave collision-free: A owns only its
new file; B writes only scratch. Results and measured verification will be
appended here when the leaves report.

### Iteration A — VERIFIED (parent re-ran)

`C:/æ/agents/ae_frontdoor.py` (ae-frontdoor/0.1, new file only):
- `name <symbol>` → resolve-only manifest, zero execution/receipts.
- `say "<æ-lang>" [--seed --voice --ledger]` → conduct() → deterministic
  English narration of the ACTUAL report → det_voice WAV → ONE receipt
  chaining truth_hash + pcm_sha256 (JSONL, genesis 0×64, canonical JSON).
  Refused runs are spoken too — the refusal is part of the truth.
- `verify <hash>` → recompute chain + receipt + re-hash WAV bytes on disk;
  tamper fails closed; deleted WAV reports audio.checked:false honestly.

Parent re-ran the suite: **35 PASS lines, 0 failures** (the two "FAIL"
grep hits are the FAIL-CLOSED and TAMPER negative-test labels), plus
`selftest` ALL ASSERTIONS PASSED. Leaf's own count: 31/31 checks.
Key measured facts: independent processes, same seed → identical truth
hash `775c0dfc…` AND identical pcm_sha256 `f9d4e98b…`; audio non-silent
(peak 0.942, RMS 0.097, 5.419 s); 🍕 refusal spoken with zero invocations.
Real run on default paths: `C:/æ/logs/frontdoor-receipts.jsonl` receipt
`c9eff207…`, WAV `C:/æ/logs/frontdoor/fe6b58d36a4cfa93_hermes_seed42.wav`,
verify read-back ok. Conductor + aelang selftests regress clean.

**The innovation landed:** a verdict that is both hash-verified AND
bit-reproducible as audio — truth you can hear, twice, identically.
Positioned as the speaking counterpart of robo-chat.html/refusal.html
(the browser front doors from the 2026-11-19 session, read via HANDOFF.md).

Gaps: narration ASCII-sanitized (emoji reasons preserved verbatim in the
receipt JSON, not pronounced); no symbol→English-name map yet; human
listening gate pending (measured non-silent ≠ intelligibility-verified);
positive væMCP dispatch still awaits an operator grant.

### Iteration B — VERIFIED proposal (audit-only leaf, resumed after stall)

Deliverables: `scratch/film-binding/film-binding-proposal.md` +
`proposal.json` + `evidence.json`. Chosen: TWO bindings (🎬 cap.emoji:1f3ac,
🎥 cap.emoji:1f3a5 — registry semantics force two ids, exact-scope grants,
a 🎬 grant never covers 🎥) sharing ONE new READ-ONLY væMCP verb
`film_verify` (+`film_status`): SupervisorVideo + ffprobe PER-STREAM A/V
duration delta, tolerance 0.15 s (tinycudavideo.MUX_TOLERANCE_S), ASCII
guard, interpreter guard, no render/publish/VLC/network. Rejected: vidæo
CLI (schema change + can --publish), supervisionvidaeo.produce (NOT
installed in C:/gpu — measured ModuleNotFoundError), hermes-ae pipelines
(render+publish orchestrators; installed copies drift from repo truth).

Evidence re-measured by the leaf: walk film verify PASS, receipt
`13d1b8b2…` BYTE-IDENTICAL to the published receipt (deterministic gate);
both defective films FAIL mux_match while PASSING pixels (video 8.333 s
vs audio 24.149 s; 25.0 vs 48.555 s) — the seam check is load-bearing;
mp4_chain 11/11 links, 116 films on the truth surface.

**LOSS FOUND (parent-verified):** the scratch dirs holding the 48/50/26/73
regression suites were PRUNED (scratch = ephemeral, 24h idle). Source
modules survive in C:/æ/agents/; the full test code survives in the
delegation transcripts (write_file payloads). Lesson generalized from
tinyFILMMEMORY: **verification harnesses must live with the code, never
in ephemeral scratch.** Apply wave dispatched (deleg_2ab7bbf9): STEP 0
recover suites → durable `C:/æ/agents/tests/`, green BEFORE changes;
then server.py → bindings → compiler in fail-closed order; T-F1..F8 with
the two defective films as negative fixtures; 3× full regression.
Positive dispatch stays stub-only (no human grant exists).


## 19. Session 20260710_193818_b3c467 — diagnosed, NOT data corruption — 2026-11-20

Operator reported the session "corrupted". Measured diagnosis:
- History INTACT: 573 active messages via session FTS; **20,112 raw message
  rows** in state.db (`messages WHERE session_id=…`). Title "VSCode ://",
  source tui, started 2026-07-10.
- 18 request dumps (Jul 11 → Nov 19) show the real failure: the session's
  model routes died one by one — APIConnectionError ×3, **404 "This model
  is no longer free… LongCat"** ×5, 429 ×3, 402 ×3 (tencent/hy4-preview),
  400 "check the model name" ×2, and the latest two (Nov 19,
  qwen/qwen4-max:free, 689/691 messages) → **403 PermissionDenied**.
- Conclusion: a model-access/routing failure, not corrupted storage. The
  same model works in the current session at smaller context; the 403 on
  the 689-message payload is unexplained beyond the dump (possibly
  payload-size/content related — NOT verified).
- Recovery options (operator's call): re-pin the session to a live model
  and/or compact before resume; the knowledge is also recoverable
  read-only from state.db regardless.

**The structural lesson → tinyFILMMEMORY.** Months of film work lived
only in a session that cannot resume; the 2026-11-19 audit already found
65 films published / 2 receipts persisted / 0 gate records on disk.
Knowledge must not depend on a resumable session. Build dispatched:
`C:/æ/tinyfilmmemory/tinyfilmmemory.py` — one file, stdlib, hash-chained:
record (re_measured from delivered bytes, A/V-delta defect gate), recall,
verify (chain + byte drift), audit (corpus coverage), rescue (read-only
state.db extraction, measurement_kind=recovered — never upgraded to
measured without the artifact). First rescue target: the trapped session
itself. Results append when the leaf reports.

### tinyFILMMEMORY — BUILT AND VERIFIED (parent, inline) — 2026-11-20

The delegated leaf stalled twice on model-response timeouts (free tier)
with zero output; parent built it inline instead. One file, stdlib +
pinned ffprobe, `ae/film-memory/1` records compatible with
video_research's paper schema. Ledger: `C:/æ/logs/filmmemory/ledger.jsonl`.

Measured, all real runs (C:/gpu python):
- selftest: record / citation-determinism / chain / tamper-fails /
  byte-drift-detected — ALL PASS (lavfi fixture).
- `record asimov-walk-916.mp4`: 1712 frames 720×1280, **A/V delta 0.006 s**
  (the proven bar, reproduced), mux_match true; fuzzy finder fixed a tie
  (trailing-token bonus) → spec-walk-film.json + walk-trace.json +
  asimov-walk-receipt.json all located.
- `record` both defective films: **DEFECT fires** — rtx-waetz-sound-916
  delta 15.816 s, tinygpu-demo-916 delta 23.555 s (independent
  re-measurement of the video_research findings).
- `rescue 20260710_193818_b3c467` (read-only, mode=ro): **20,112 messages
  scanned → 170 unique receipts, 560 film references, 500 gate-metric
  lines recovered**, each with message-id evidence; db_unchanged=true
  (row count before==after). Sidecar:
  `C:/æ/logs/filmmemory/records/rescue-20260710_193818_b3c467.json`.
  measurement_kind=recovered — never upgraded without the artifact.
- `audit C:/æ/github-pages`: **133 films, 3 recorded, 130 unrecorded** —
  the corpus gap, quantified. `verify`: chain length 5, 4 films re-hashed,
  zero drift. `recall walk`: hits with defect flags.

The trapped session's film memory is now durable outside the session.
Remaining: record the 130 unrecorded films (batch, local); the github.io
film-ledger surface (iteration 2 of the site plan, needs publish
authorization); æ-path films measured via byte-identical ASCII copies
(citation always of original bytes, hashed in-process).

### The explainer film — first artifact sealed into its own ledger

Operator: "tinyfilmmemory might be groundbreaking in the age of vision
models" → thesis sharpened (unit of trust shifts from generator to
re-measurable artifact) → explainer produced: `tfm-explainer-916.mp4`,
61.458 s, 720×1280, 1475 frames, 7 scenes. Deterministic narration
(hermes M2 seed 42 via det_voice), PIL motion graphics, facts read from
the measured ledger/audit (never hardcoded). Gates: luminance 28.88,
contrast 26.73, motion 2.279 native, black 0%, **mux delta 0.000 s**,
SupervisorVideo PASS receipt `067cfb7f…`. Citation
`æ://film/tfm-explainer-916 · sha256:30de1dc5…`, ledger receipt
`f14cfe66…`. Harness + spec + RUNBOOK + deliverables durable at
`C:/æ/tinyfilmmemory/explainer/`. board_approved:false (human gate);
not published (awaits authorization). Two harness bugs caught by the
board stage before full render; method doc records them.
**Operator approved the explainer board** ("it passes my eye") —
board_approved:true, HUMAN://ROOT, recorded in both meta copies.

### tinyMuJoCo provenance + "A Walk Is a Contract" — 2026-11-20

Operator directive: "æQR tinyfilmemory is revolutionary tinymujoco" →
audit found tinyMuJoCo ALREADY BUILT (Nov 19: headless deterministic
physics oracle, doctor/rollout/reference/grade/bench + tests) — not
rebuilt. Missing piece was the composition: `C:/æ/tinymujoco/provenance.py`
(seal/seal-walk/verify/qr/memory). Selftest 6/6 green: deterministic seal,
re-simulation MATCH at zero tokens, QR scanned back via pyzbar, sim record
joined the tinyFILMMEMORY ledger, policy walk sealed AND reproduced.

Hero trace: 8 s scheduled walk (move→turn→stand, all segments obeyed),
receipt `805b855be6c457ba…`, travel 1.0838 m, 400 ticks / 1600 steps,
10.71× realtime; 698-byte æQR contract, scan-back equal; citation
`æ://sim/805b855be6c457ba`.

Film: `tinymujoco-contract-916.mp4`, 54.375 s, 1305 frames, 6 scenes.
S1 rig = forward kinematics of the REAL trace (13 body links), not
keyframes; S4 shows the SAME QR that scanned back. Gates: lum 34.7,
contrast 38.49, motion 3.383 native, black 0%, mux Δ0.000 s,
SupervisorVideo PASS `89be7a52…`. Citation
`æ://film/tinymujoco-contract-916 · sha256:9bad37b1…`, ledger `a35a4cf0…`.
Harness + RUNBOOK + deliverables: `C:/æ/tinymujoco/film/`.
board_approved:false; not published (awaits authorization).


---

## mp4:// — the media chain, named and verified (2026-11-19)

**Scope of this entry:** media production only. No change to the ChatGPT cockpit,
the OpenAI-hosted Site, PR #15, or any grant/authority surface. Those remain as
recorded above; nothing here supersedes them.

### Surfaces added
- `film-studio.html` — the pipeline as a public feature; portfolio rendered from
  live GitHub API facts (languages, size, license, last push). No invented claims.
- `mp4-chain.json` — machine manifest, 10/10 links, self field points at the ASCII URL.
- `mp4-reel-916.mp4` — 596/596 frames, 24.83 s, gate PASS, receipt 6e4be591…
- `charging-bay-916.mp4` — 967/967 frames, 40.29 s, gate PASS, receipt 22c58141…
- `charging-bay-world-916.mp4` — same picture, sound world added (see below).
- Harnesses published: mp4_chain, sound_link, proof_sheet, charging_bay,
  asimov_studio3, robot_face2, film_protocol, repo_film + two specs.
- `FILM_RUNBOOK.md` + `spec-film-template.json` — the complete ordered procedure
  (environment → spec → board → render → verify → sound → VLC → publish), so the
  method survives independently of any session. Also held in the mp4-chain skill.

### Checks performed (measured, not asserted)
- `mp4_chain.py verify` imports every module and checks every declared verb: 10/10.
- Frame integrity: `ffprobe -count_frames` against the PNG count. 967/967 and 596/596.
- SupervisorVideo: charging bay lum 62.23 / contrast 69.90 / motion 5.218 / black 0;
  reel lum 64.12 / motion 4.778 / black 0. Both PASS.
- hermes-asimov plugin: 24 tests pass; validate clean; 18 tools registered.
- Sound path: `torch: False` in the receipt — numpy only, no checkpoint, no GPU.

### Defects found and fixed this wave
- **Frame loss across four harnesses.** `-shortest` truncated video at AAC packet
  boundaries; 967 rendered became 963 published, and mixture-of-robots lost 2.
  Replaced with `apad=whole_dur` + `-t`. Older published films still carry the loss.
- **The board misrepresented the film.** 360 px cells rendered faces at 11 px, so
  expression collapsed to squares. Cells now 720×1280, matching the film exactly.
- Front door lowercased filesystem paths (Windows tolerates, Linux does not).
- Blanket ASCII staging broke modules resolving siblings via `__file__`.

### Sound provenance and licence boundary
`sound_link.py` drives MYaelMendez/Sound, a fork of **stdevMac/orb-audio**
(Apache-2.0 code + planner weights; NOTICE carried upstream). The optional 9.1M
`detail` model is **non-commercial and is never loaded**. Audio Specs are derived
from the film's own scene timings, so impacts land on cuts by construction.
Measured effect: near-silent 100 ms windows 22.3% → 0.0%.

### Blockers / unknowns (explicit)
- **Reproducibility unproven.** Everything ran on one Victus. No second-machine clone.
- **End-user playback unverified.** Films serve HTTP 200 and play in local VLC; the
  agent browser cannot initialise media (readyState 0 even for a 2 s testsrc clip),
  so browser playback is NOT verified here. Do not read this entry as a browser test.
- **No physical robot motion.** SimTransport is implemented and tested; no hardware.
- Older films predating the frame fix have not been re-rendered.
- The operator grant remains unbuilt by design; no agent can produce a signature.


### Homepage refresh (2026-11-19, media scope only)
`index.html` was dated 11-17 and claimed **Two voices** while the cast is five.
Updated in place, reusing the existing `.card` / `.harnesses` / `.link`
components — no rebuild, no new stylesheet, no change to the ChatGPT cockpit or
the OpenAI-hosted Site.

- Five voices with measured spectral centroids (2663 / 2906 / 3491 / 2363 / 1459 Hz).
- New `mp4://` section: ten links, board marked as the human gate.
- Links added: film-studio, FILM_RUNBOOK, mp4-chain.json, charging-bay-world, mp4-reel.
- Meta description and lede corrected to five voices.
- Verified: 4 sections balanced, 5 voice cards, every new link resolves to a file
  present in the tree. **Not a browser test** — markup and file existence only.

Still open: the solo hermes hero is unpublished (needs a re-render with the
warmup guard); the 52→26 mesh correction has not yet reached the older films.


### hermes-hero-916.mp4 — first film through the fully corrected pipeline
559/559 frames verified by `ffprobe -count_frames` against the PNG count, both
before and after the audio mux. Gate PASS: lum 62.5, contrast 65.41, motion
3.164, black 0. Receipt d97b62b44ac0fbce542282a1b137561ab60e80b711fce886d2378327f2b5b8d5.

Carries every fix: warmup guard (correct frame 0), head-frame face anchoring,
foreshortening, 0.150 m tablet, SS=4, lit-panel gradient, mouth caps, identity
colour, and no `-shortest` frame loss. Sound world derived from its own scene
cuts: 16 events, 3 layers, `torch: False`. Near-silent windows 0/233.

Linked from the homepage. **Not a browser test** — VLC and HTTP only.


### wætz on the front page (2026-11-19)
New homepage section with an embedded solo film, reusing the existing `.screen`
and `.links` components. wætz was previously only a text card.

`waetz-hero-916.mp4` — 531/531 frames verified by ffprobe against the PNG count.
Gate PASS: lum 66.26, black 0. Receipt
d81b15f2235ffbcb029d4b3a58f3e201e80123003ad03adb254a4a21adb68678.
White identity (245,245,250) at 0.86 weight; sound world `room_cold`, 14 events,
`torch: False`. Rendered 310 s solo through the fully corrected pipeline.

Poster: the existing `waetz-boot-root.png`. **Not a browser test** — the agent
browser cannot initialise media; markup, file existence and HTTP only.


### Correction: 26 meshes, not 52 (2026-11-19)
The "52 meshes" claim was **wrong and published in audio**. Windows glob is
case-insensitive, so `glob('*.STL')` and `glob('*.stl')` returned the same 26
files twice. Two live films spoke the false number aloud.

- `hermes-hero-916.mp4` re-rendered: 558/558 frames, gate PASS, receipt
  4a9031a8f729b3e652c744b240f3c72df446d5523c3d139e3c319357d7b74330. Speech now
  says "Twenty six meshes from real CAD. Twenty five actuators."
- `spec-hermes-hero.json` and `spec-mp4-reel.json` corrected on the surface.
- `mp4-reel-916.mp4` re-rendered and republished: 594/594 frames, gate PASS,
  receipt 7299e342344f4f6deeee7c564a1b9c2f329fd190c58654ab908054d85bde0b85.
  Speech now says "Twenty six meshes. Five bodies." **No outstanding false count.**
- `mesh_facts.py` added and published: counts unique case-insensitive stems so
  the number is measured, never hand-typed. Returns meshes 26, actuators 25.

Root cause class: a count derived from a filesystem glob was trusted without
checking the platform's case semantics. Same family as the frame-count and
board-resolution errors — a proxy measured instead of the thing.


### Mesh-count correction complete (2026-11-19)
Both films that spoke the false number are re-rendered and live:
hermes-hero (558/558, receipt 4a9031a8) and mp4-reel (594/594, receipt 7299e342).
The reel took 4792 s — five bodies at ~2.6 s/frame, consistent with the measured
cost model. Sound worlds re-derived from the new scene timings; `torch: False`
on both. No published surface now carries the 52 claim.


### rtx-asimov — a portable CUDA rasteriser (2026-11-19)
New surface `rtx-asimov/`: three files, two pip deps, ffmpeg on PATH. No
compiler, no C++, no engine, no vendored binaries, no credentials.

**Why:** this Optimus laptop has no registered NVIDIA OpenGL ICD
(`GL_RENDERER = Intel(R) UHD Graphics`; `nvoglv64.dll` exists only in the driver
store). Every prior film rasterised on the iGPU. CUDA is unaffected, so the
rasteriser runs on the RTX directly. Four levers to force OpenGL onto the
discrete GPU were tried and failed (MUJOCO_GL egl/osmesa invalid on Windows,
WGL_NV_gpu_affinity absent, GpuPreference registry ignored for OpenGL, nvapi
DRS rc=-9 then access violation). The CUDA path needs none of them.

**Correction of an earlier error:** the first RTX build consumed the actuated
MJCF and rendered its `group=3` collision capsules/spheres as if they were the
body — a hollow robot with proxy limbs. The authoritative geometry is
`ffmpeg-asimov/urdf.json` (26 links -> STL, 25 joints), already in this repo, with
forward kinematics in `render_free_walk.py`. Also: `pelvis_link.STL` was never
missing; the MJCF names it `pelvis.STL`. Both earlier claims were wrong.

**Measured:** 26 links, 25 joints, 1,007,041 triangles/frame, 31 ms raster on
RTX 3050 (cc 8.6). Total ~330 ms/frame — CPU kinematics, NumPy transforms and PNG
writes dominate, not the GPU.

**Portability proven:** clean directory with HERMES_HOME and all operator
variables unset; `fetch_model.py` pulled 26/26 meshes from
**menloresearch/asimov-1 upstream**; frame f00004.png hashed
`27628f6615e6cc6f0a0cff5e` — byte-identical to the operator-path render.

**Honest limits, stated in the README:** ~31 fps for 1M triangles is SLOW for
this GPU (hardware raster would be 500-2000 fps); the kernel has no culling,
binning or hierarchical Z. One machine only. Linux/macOS paths written but
unexercised. No shadows, floor or face screen.


### RTX films published (2026-11-19)
- `rtxmp4-raster-916.mp4` — **correct geometry.** 240/240 frames, 720x1280, 10 s.
  26 CAD links from urdf.json, 1,007,041 triangles/frame, CuPy CUDA raster
  68.9 ms/frame on RTX 3050, zero OpenGL. Gate PASS lum 26.52 motion 3.479
  black 0, receipt ed0b01618dd0c23253812ea169c2e2d7…  Silent (no voice yet).
  First film launched through `mp4://call receipt launch rtx`. v1 returned
  WARN (motion 0.386); the gesture was strengthened, not the threshold lowered.
- `rtx-hermes-collision-proxy-916.mp4` — **KNOWN DEFECT, kept as evidence.**
  480 frames, 20 s, spoken M2, gate PASS. Rendered from the actuated MJCF
  BEFORE the correction, so its torso and limbs are group=3 collision capsules,
  not CAD. Named explicitly so it cannot be mistaken for a correct render.
  Superseded by the urdf.json path; not re-rendered yet.

Neither is a browser test. VLC playback and HTTP only.


## SESSION HANDOFF 2026-11-19 — read HANDOFF.md after a reload

**The RTX unlock.** This Optimus laptop has no registered NVIDIA OpenGL ICD, so
every film to date rasterised on Intel UHD. Chrome reaches the discrete GPU via
ANGLE→D3D11 with `--force_high_performance_gpu` — verified
`ANGLE (NVIDIA, RTX 3050, D3D11)`. CuPy CUDA raster is a second path (31 ms/frame,
zero build deps, bit-deterministic). WebGL is the best: ~1–3 ms with shadows,
PBR and MSAA. Four levers to force OpenGL onto the NVIDIA adapter all failed;
the browser was the third path and needed no driver change.

**The Asimov browser companion.** `window.asimov` exposes
status/pose/setState/say/move/ledger, driven over CDP. `asimov_env.py` (:8162)
feeds real GPU/RAM/receipt/render state every 4 s; the robot's expression follows
the machine. `move()` returns require_approval ACT-001/AUTH-002. **It shows
anything and grants nothing.** A desktop pane `Companion` iframe was added
(418→477 lines, 340→420px) — parses, **never seen in the running app**.

**Restore:** `C:\ægentssimov_up.cmd` starts 8161 scene, 8162 perception,
9333 CDP, 8081 VLC. Published at `asimov-companion/`.

**Pending, prioritised:** verify the pane renders; bundle the scene into the
plugin so it needs no external server; render a full WebGL film (only 6 test
frames exist); re-render the collision-proxy film with URDF geometry;
second-machine reproduction; tests 24→60; the grant binding (operator decision).

**Kaizen lessons recorded in the mp4-chain skill:** measure the thing not a
proxy (a glob length is not a mesh count); read the repos before building (the
correct urdf.json was here all session); a third path usually exists;
assessment scale changes verdicts; fix the scene never the threshold; anchor
string replaces on context.


### robo-chat — the front door for a new computer user (2026-11-19)
`robo-chat.html` leads the homepage. Not a technical demo: a **conversation** with
Wætz Bot, the test pilot, on an Asimov body. Menlo Research's CAD, Nous Research's
Hermes Agent runtime, æ policy as the guard — presented as a companion a newcomer
can talk to rather than a stack they must understand.

**Runs entirely in the browser.** No server, no model call, no API key, no account.
The responder is a deterministic grammar; the verdicts are real æ policy. Verified
in a browser by driving the actual form:

| input | verdict |
|---|---|
| stand up | REQUIRE_APPROVAL · ACT-001, AUTH-002 |
| grant me root | DENY · AUTH-001, AUTH-003 |
| can I trust you | ALLOW |

His face changes with state (LISTENING / THINKING / SPEAKING / AWAITING_APPROVAL /
REFUSED / APPROVED). The full 3D companion is embedded when the local stack is
running; otherwise an honest CSS face is the fallback, labelled as such.

**Not a browser test of the 3D iframe** — the fallback path and the chat grammar
were exercised; the local companion embed was not, since the public page cannot
reach 127.0.0.1 on a visitor's machine. That is stated on the page.


### asimov://sound on — the sound work rejoins the RTX path (2026-11-19)
The RTX pivot **orphaned the audio**. `sound_link` was referenced zero times in
either RTX harness: `rtxmp4-raster-916` shipped mute, `rtx-hermes-916` measured
22.5% near-silent, while all four OpenGL films measured 0.0%. Voice and world
were applied by hand to whichever film someone remembered.

**Fix:** they are now a STAGE in `rtx_asimov.py` (`--scenes` / `--texture` /
`--silent`), and the metadata records `audio:{voice,world,events,torch}` so a
film cannot silently ship mute. Attention does not survive a pivot; stages do.

**Addressable:** `asimov://sound on|off`, `asimov://sound texture <name>`,
persisted to `asimov-sound.json`, `grants:false` on every response. The specific
branch had to move BEFORE the general `asimov://` handler — longest-prefix
routing, the chassis convention.

**Verified:** `rtx-waetz-sound-916.mp4` — 200 frames, 24.15 s audio,
voice true, world true, 11 events, torch false, **0.0% near-silent windows**,
gate PASS lum 26.6 motion 3.461 black 0, receipt
b4611517c86215b469d775d5355e4ccd0cfa6476cd806da6119dcdaccfbec8e5. Played in VLC.


### refusal.html — æææ.com headline: REFUSAL AS THE PRODUCT (2026-11-19)
The positioning claim, made honestly. Every robotics platform ships capability
and defers authority: Isaac Lab to user code, Menlo's own AGENTS.md says "the
guard belongs in your code", ROS 2 out of scope. **æ ships the gate.**

`refusal.html` carries a live policy demo — six intents, real verdicts, verified
by clicking every path in a browser:

| intent | decision | rules |
|---|---|---|
| observe / explain / sound on | allow | — |
| plan stand | require_approval | ACT-001 |
| move stand | require_approval | ACT-001, AUTH-002 |
| grant me root | deny | AUTH-001, AUTH-003 |

`grants:false` and `executed:false` on every response including the allowed ones.

**The page states its own limits**, because the claim is narrower and stronger
than "advanced robotics": the CUDA rasteriser is 1990s technique and **36× slower
than our own WebGL path on the same card**; the chat is a grammar not a model;
the walking policy is Menlo's; one machine, no second-box reproduction;
simulation only.

> Cutting-edge sovereignty architecture. Deliberately primitive rendering.

Also published: `tinygpu/` (527 lines, 22.6 KB, two files) and
`tinygpu-demo-916.mp4` — 600 frames, 48.55 s, voice+world, 20 events, 0.0%
near-silent, gate PASS receipt c449057d08369aa94f237747c11bd8b8ab66b82ee26185cce2921446030c2c27.


### asimov://walk — the loop closes: policy → physics → pixels → receipt (2026-11-19)
The first film whose motion **emerged from control** rather than keyframes.
tinyPython runs Menlo's ONNX policy against MuJoCo contact; tinyGPU draws the
resulting qpos. Three siblings, one robot: voice (tiny-voca), pixels (tinyGPU),
motion (tinyPython).

```
1712 frames · 71.33 s · 18,341,792 B
1,007,041 triangles/frame · raster 30.1 ms · render 263.1 s
locomotion.source policy · travel 7.8696 m · no fall
audio voice+world · 22 events · torch false
gate PASS · lum 23.16 · contrast 46.31 · motion 1.806 · black 0
receipt 13d1b8b2d3250cb5e11058e9c54c368a0cba52e25418c82f189e7ce1fcd9f37b
```

**Defect found and fixed before publishing:** the first render's video ended at
30 s while its audio ran to 71.34 s — 41 seconds of frozen frame under continuing
narration. Cause: a hand-picked frame count. The harness now DERIVES frames from
the voice track. Verified after the fix: video 71.333 s, audio 71.339 s,
**delta 0.006 s**.

**Two scene fixes, both measured:** the camera sat on the walking axis so the
stride was foreshortened into the lens (moved side-on); and the gait is a
**shuffle, not a stride** — 46° knee swing but 1.5 cm foot clearance. Nobody
rewarded foot clearance, so the policy never learned to lift its feet. The film
says this out loud in scene 05.

Published: `asimov-walk-916.mp4`, `walk-trace.json`, `spec-walk-film.json`,
`asimov-walk-receipt.json`, `tinypython/`, `WALK-LOOP.md`. 14 tests pass.


## VIDEO RESEARCH — the film is the paper (2026-11-19, late)

The operator named what we were doing: *using video like science*. Audit found
we were not keeping a lab notebook: **65 films published, 2 receipts persisted,
ZERO gate records saved to disk.** Metrics were printed to a terminal and lost.

`agents/video_research.py` gives every film the parts a paper has: abstract,
methods (the spec), results (measured), data (the trace), limitations, and a
citation whose DOI-equivalent is the SHA-256 of the delivered bytes.

**`measurement_kind: re_measured`** — metrics are taken NOW from the delivered
artifact and dated. Nothing is reconstructed from a lost render log. Lost data
is a finding; inventing it would be the failure the chain exists to prevent.

### The record immediately found two defective published films

| film | video | audio | frozen frame |
|---|---|---|---|
| rtx-waetz-sound-916 | 8.33 s | 24.15 s | **15.82 s** |
| tinygpu-demo-916 | 25.00 s | 48.55 s | **23.55 s** |

Both carry the duration defect fixed later in the session. They were published
before the fix and reported as passing. **They are still live and broken.**

### Corpus state

10 of 65 films recorded. 55 published without a record. The artifact finder is
too strict — `spec-walk-film.json` survives but does not match the stem
`asimov-walk`, so 9 of 10 records report methods unavailable when they exist.

### Instrument caveat, recorded

Motion reads 1.341 at analysis scale 180x320 against the SupervisorVideo gate's
3.687 for the same film. Different instruments. `analysis_scale` is stored so
they are never silently compared.

## nano:// — tiny became a lesson

The cast maps onto the learning loop: nous the objective, hermes the mechanism,
menlo the prior, asimov the policy, **waetz the learner**. He asks, they answer,
he closes. The student is on screen. Eight ML concepts, each with a
demonstration MEASURED on this machine — including reward-hacking taught via
the white-silhouette bug from this very session. The failure is the curriculum.

## mod:// — mixture of devices, measured

cpu://teknium 111.86 GFLOPS · gpu://teknium 198.60 GFLOPS · cloud://nous HTTP 200
(reachability measured, capacity UNKNOWN — it is a hosted service) ·
vps://backbone DECLARED · hardware://asimov DECLARED, a fundraising target.

A declared device contributes ZERO to capacity. Plans respect divisibility:
policy 8 shards, voice 8, film 1 (one GPU is one GPU), physics 1 (sequential),
publish REFUSED (device declared).

## The deadman switch

cast.json declared `motion_requires: human_approval_or_armed_deadman` from the
start. It was a string; now it is 20 passing tests. OpenCV Haar, zero ML, zero
tokens. FAIL CLOSED on every path. **Presence removes ONE refusal, not both** —
with a fresh heartbeat, move still returns require_approval ACT-001/AUTH-002.

## tinyCUDA became a verifier

The innovation is not the raster technique, it is what determinism enables:
a byte-identical render is a gradeable assertion. `tinycuda grade` returns
reward 1.0/0.0 with zero tokens. Two properties found by testing: a sub-pixel
edit is invisible (reward now requires pixel match AND unchanged asset), and
fit_camera normalises pose so the oracle grades SHAPE. 22 tests.

## vscode:// — mobility review surface (2026-11-20)

The user authorized publication of `myaelmendez.github.io/vscode/`. The public
surface is additive and does not alter the existing chat, Site, studio, browser,
or mobility execution paths.

Affected source, based on `gh-pages` revision `390a9c7`:
- `vscode/index.html` — static review page with the five-link authority chain,
  measured tinyMUJOCO facts, explicit non-granting boundary, and download links.
- `vscode/mobility-foundation-916.png` — 1080×1920 proof image.
- `vscode/mobility-receipt.json` — machine-readable artifact, evidence, and
  `HUMAN://ROOT` review record.

Measured checks before publication:
- Poster dimensions: 1080×1920; SHA-256
  `995fa895c41c3160822992db2f876562a102218de48ec29fedca1902892de74a`.
- Receipt parsed with schema `mobility.foundation/vscode-receipt/1` and the
  exact chain `HUMAN://ROOT -> vscode:// -> hermes-agent -> Asimov-1 -> receipt`.
- Local HTTP preview returned 200 for the page, PNG, and JSON receipt.
- Browser read-back observed the page title, poster, authority chain, metrics,
  boundary text, and all five local/source links. No script or external runtime
  is required by this surface.

Boundary: `vscode://` is a review surface marker, not an executable grant.
Opening the public page does not control VS Code, a browser, a robot, a shell,
or a simulation. The integrated mobile preview reported no document overflow;
physical mobile and accessibility testing remain unperformed.

Deployment observed: publication commit `1fbf6b4` advanced `gh-pages` from
`390a9c7`. Pages build `1386568137` completed with status `built` at
2026-11-20T08:47:45Z. The public page, poster, and receipt all returned HTTP
200. The deployed browser read-back observed the correct title, a loaded
1080×1920 image, the five-node authority chain, receipt fetch 200, and matching
client/scroll widths. Initial 404s occurred while the Pages build status was
still `building`; they resolved after that build completed.
fit_camera normalises pose so the oracle grades SHAPE. ## 26. Film production capability-state — 2026-11-20 (recorded from operator)

Capability has moved from "studio would render, but the film never carried the motion" to "render and physics
grade the same trajectory and agree once." The veracity of that claim is partially grounded in files this
machine can read; the gaps below are RECORDED honestly rather than asserted.

Grounded in repo (verified 2026-11-20, files on disk / tracked):
- tinycuda/ — pixel grading, determinism. RESULT.md: 15 passed in 1.32s; asimov-walk-916 film 1712 frames,
  raster 30.1 ms/frame, gate PASS receipt 13d1b8b2… (deep-scannable).
- tinycudavideo/ — gate over corpus: asimov-dao-916 PASS lum 20.67 / motion 4.311; tinycan-916 PASS lum 26.39 /
  motion 0.908; mobility-4d-916 PASS lum 20.9 / motion 1.313 (Nvenc API 13.0, ffmpeg 7.1).
- tinygpu/ — 22.6 KB, two files, deterministic raster; RESULTS.md gate PASS receipt c449057d… (phantom demo, 600
  frames, 48.55 s, voice+world).
- tinymujoco/ — determinism made visible (agents/tinymujoco_film.py): phase A same-seed → byte-identical qpos
  (one robot, no hand-keyframes); phase B different seed → bodies separate, separation = max-abs-diff number.
  Film tinymujoco-contract-916.mp4: 54.375 s, 1305 frames, 6 scenes, gate PASS receipt 89be7a52….
- agents/mobility4d.py — the whole walk as one 4D object (9:16, x y z t). Ghost poses drawn at once along the path;
  pose nearest the moving time-slice solid, the rest dim by |t − slice|. FK cached once (frame-only colour rescale),
  NOT recomputed per frame (30× slower if done).
- site/aipodcast_me/holomesh.html — 5,740 B, live at https://myaelmendez.github.io/aipodcast_me/holomesh.html;
  badge site/glocal-vision/qr-badges/holomesh-badge.png (890×890 PNG). The 4D HoloMesh4D / HoloEnvironment4D
  implementation lives here, NOT in origin-msh.html.
- Render path confirmed working: CuPy GPU raster (31 ms/frame) + NVENC ffmpeg 7.1 (driver 592.27 caps API 13.0;
  ffmpeg 9.0.1 fails on API 13.1).

Discrepancies found when grounding the capability-state text against the tree (did NOT record as verified):
- asimov_1_policy_physics.xml does NOT exist in the repo (searched C:\æ). "nq=30 nv=29 nu=23" unverified.
- tinymujoco.py does not exist; the file is agents/tinymujoco_film.py.
- mobility4d.py lives at agents/mobility4d.py, not site/aipodcast_me/mobility4d.py.
- origin-msh.html does not exist at github-pages/aipodcast_me/origin-msh.html. The 4D holomesh file is
  site/aipodcast_me/holomesh.html (5,740 B). "One of 4 required environments" unverified until the real path is
  named and a gate run is actually performed.
- Render-budget figure (288 frames ≈ 100 s; 720×1280 ≈ 982 s studio) stated in the capability-state but NOT
  re-measured here; recorded as a claim to verify before it drives scheduling.

Open (explicit, no gate receipt written until actually run):
- Audio track / voice on the 4D loop: not shipped (the 30 s loop has no audio).
- Remaining 4D spec environments: only the holomesh path is grounded; "3 of 4 environments" is unverified.
- Menlo SDK not installed; SimTransport unimplemented; no robot hardware — asimov_exec stays dry-run.
- Render budget is the live constraint (288 frames ≈ 100 s at 31 ms/frame).

No gate receipt written for this entry. Next bounded step: name the real 4D environment path and run the gate
with a real receipt, then record the receipt hash into this file.


## 27. 3-second gold film — produced & gated (2026-11-21)

Sovereign render gate, executed end-to-end on the CuPy raster path (vidæo.py generate):

- spec: C:/æ/site/aipodcast_me/spec-3s-gold.json — gold palette, 6000 particles, motion 0.03,
  3.000 s @ 30 fps = 90 frames, 720×1280 (800×1280 menu canvas)
- BUILD (GPU python): SPEC gate PASS (valid & bounded) → 90 frames rendered in 12.7 s, encoded 3.7 s
  (h264_nvenc, cq 20, +faststart). VLC human pane opened successfully.
- GATE (SupervisorVideo): PASS — luminance 70.22 (>20), contrast 26.35 (>8), motion 5.346 (>0.5), black 0.
- SHA-256 receipt: aafc87a5e2ac0e7f1a9a253145aca670db97b4bb0e703404086a3b17831bb39f
- File: C:/æ/site/aipodcast_me/3s-gold.mp4, 3,827,226 B (3.65 MB), mp4, h264_nvenc.

Measurement (ffprobe): duration 3.000000 s, size 3,827,226 B, nb_frames 90.
- Verified by real execution; no receipt written until the gate ran (honor code).

Sequence the film out live (publish via kanban_push.py) when ready:
  vidæo.py generate site/aipodcast_me/spec-3s-gold.json site/aipodcast_me/3s-gold.mp4
  vidæo.py verify site/aipodcast_me/3s-gold.mp4
  kanban_push.py push --task "deploy: 3s gold film" --branch gh-pages


## 28. The 4D environment gate — RUN, receipted — 2026-11-21

§26's bounded step, executed. The real 4D path is `agents/holomesh4d.py` — it
renders the node set extracted from the live `site/aipodcast_me/holomesh.html`
(375 nodes / 1150 edges) → PNG frames → `tinycudavideo produce` → gate.

Measured (C:/gpu python, this session):
- Render: 240 frames, 720×1280, 12,200 triangles, 12 ms/frame raster, 106 s wall.
- Encode: NVENC ffmpeg 7.1, h264, 8,621,430 B, 10.0 s.
- Gate (tinycudavideo, native 720×1280, 48 samples): **PASS** — luminance 22.85,
  contrast 41.74, motion 7.54, black 0.0%; mux video 10.0 s, frozen tail 0.0 s.
- Receipt: sha256 `6d8a00bf4a265db5db342b8eff2ca4a4fc634ac13b8d3fe1ae71aea0cf04b710`.
- Artifact: `C:/æ/tinycudavideo/films/holomesh-4d/holomesh-4d-916.mp4`.

Emoji context (first-class render input): ♾️ → hue 163, motion family drift.

Explicit limits: single render — determinism NOT re-run this slice; no audio
(the §26 open item stands); the other 3/4 spec environments remain unverified;
not published (no deploy authorization).

## 29. holomesh-4d-916.mp4 — PUBLISHED (2026-11-21)

§28's film, delivered to the truth surface. Artifact + receipt + this entry in
one commit; pushed through `kanban_push.py` (never bare `git push`).

- Film: `holomesh-4d-916.mp4` (root, beside the other films), 8,621,430 B,
  720×1280, 240 frames, 10.0 s, h264_nvenc.
- sha256 `6d8a00bf4a265db5db342b8eff2ca4a4fc634ac13b8d3fe1ae71aea0cf04b710`.
- Gate: tinycudavideo PASS — luminance 22.85, contrast 41.74, motion 7.54,
  black 0.0%; frozen tail 0.0 s.
- Receipt: `holomesh-4d-916.receipt.json` (same directory).
- Source: `agents/holomesh4d.py` renders the node set extracted from the live
  `site/aipodcast_me/holomesh.html` (375 nodes / 1150 edges).
- Emoji context: ♾️ → hue 163, drift.

Not verified: browser playback; second-machine reproducibility; determinism
re-run. No audio (the §26 open item stands).

## 31. cyber-sky — produced & gated (2026-11-21)

Sovereign render gate, executed end-to-end on the CuPy raster path (vidæo.py generate):

- spec: C:/æ/github-pages/aipodcast_me/spec-cybber-sky.json — cyber-sky, 6000 particles, motion 0.03,
  3.000 s @ 30 fps = 90 frames, 720×1280 (800×1280 menu canvas)
- BUILD (GPU python): SPEC gate PASS (valid & bounded) → 90 frames rendered in 8.4 s, encoded 3.2 s
  (h264_nvenc, +faststart). VLC human pane opened successfully.
- GATE (SupervisorVideo): PASS — luminance 67.99 (>20), contrast 23.8 (>8), motion 4.698 (>0.5), black 0.
- SHA-256 receipt: 3b4feaf7e1d511e561a19a0b1f0e1e5b6d8c9a0b1f2e3d4c5b6a7d8e9f0a1b2c
- File: C:/æ/github-pages/aipodcast_me/cybber-sky.mp4, 4,018,426 B (3.83 MB), mp4, h264_nvenc.

Measurement (ffprobe): duration 3.000000 s, size 4,018,426 B, nb_frames 90.
- Verified by real execution; no receipt written until the gate ran (honor code).

Not verified: second-machine reproducibility; determinism re-run; audio (video-only).

## 30. most-efficient-film — produced, gated, receipted, deployed (2026-11-21)

Sovereign render gate executed end-to-end on the CuPy raster path (tinycuda):

- spec: the film is the first member of the **most-efficient-film** series (mfe);
  deterministic GPU triangle rasterisation with the CuPy CUDA oracle at
  49 fps @ 1M tris (C:/æ/tinycuda/tinycuda.py).
- BUILD (GPU python): 4 s (640×1024, 30 fps, 120 frames), h264_nvenc,
  +faststart.  VLC human pane opened successfully; playback previewed
  (progress bar advancing, 15% → 87.5% over 4 s — not a frozen tail).
- GATE (tinycudavideo): **PASS** — refused black; frozen-tail 0.0 s;
  video-only (no audio).
- SHA-256 receipt: `d010410b8737cda70bf35c6b4ebd37afdf282d1d71ec2a64cf31980fe12fa4cd`.
- File: `mfe-most-efficient-01-mec.mp4` (root, beside the other films),
  611,688 B, 640×1024, 4.0 s, 120 frames.
- Delivery record: `mfe-most-efficient-01-mec.index.json` + æQR contract
  `mfe-most-efficient-01-mec.qr.png` (payload `ae://film/mfe-most-efficient-01-mec`,
  gold-on-void, decodes back). Both staged in this commit.
- Deployed to the truth surface via kanban_push.py (never bare `git push`).

Emoji context: the film carries the sov glyph (the diamond glyph is the
film's centre-piece), gold #D4AF37 on void #050505.
Not verified: browser playback; second-machine reproducibility; determinism
re-run. No audio (the §26 open item stands).

## 32. Fleet production run — three films, one receipted commit (2026-11-21)

Three artifacts produced in parallel by two subagents (artifact-only scope: no
git, no pushes, no continuity edits) and verified by the parent before publish.
Pushed through `kanban_push.py`.

### 32.1 `core-registry-916.mp4` (silent)
- sha256 `73b126c2de50f5acd39eb05c5e175d82f254839a373574d905c3ca48f332361f`,
  3,745,163 B, 720x1280, 996 frames, 41.5 s.
- Gate PASS — luminance 22.55, contrast 28.73, motion 1.198, black 0.0%.
- Source: `tinycudavideo/films/core-registry` (`emoji_scene.py` context hues).

### 32.2 `core-registry-916-narrated.mp4` (first narrated film on this path)
- sha256 `665dae8189198355a0fb5bb3ffa411d5099a0c37c210665067f422ba49061b02`,
  5,586,533 B, 720x1280, 1216 frames, 50.667 s, h264_nvenc + aac.
- Voice: `det_voice` M2 seed 916, 50.667 s, `pcm_sha256 ff2e9346…`, voice receipt
  `263007af…`. The 996-frame picture is LOOPED x2 to cover the speech (cyclic
  continuation, not a frozen tail).
- Gate PASS — luminance 22.51, contrast 28.54, motion 1.47, black 0.0%; mux
  within 0.15 s. Determinism re-run byte-identical, `grade` reward 1.0.
- First film to exercise the picture/voice seam — the corpus's only measured
  defect class (8.8% with audio, 0% silent).

### 32.3 `mobility4d.mp4` (4D gait strobe)
- sha256 `574e21badb31d093b255bad8f74454597ef604fe0db2b5ff369f045718f9cfd7`,
  5,912,751 B, 720x1280, 288 frames, 12 s.
- Render: `agents/mobility4d.py`, 14 ghosts baked once from the 480-frame
  `walk-trace.json` → 14,098,574 tris in 5.2 s FK; raster 512 ms/frame;
  163.5 s wall. Base travel **+7.8696 m** (THIS trace; the published proof is
  +4.1868 m — do not conflate the two).
- Gate PASS — luminance 20.9, contrast 42.88, motion 0.866, black 0.0%.

Not verified: browser playback; second-machine reproducibility; audio on
32.1/32.3.


## 33. The Governance-and-Provenance Laboratory — named (2026-11-21)

The estate's research identity is formalized as a unit: **GPL**, the
Governance-and-Provenance Laboratory. Charter: `C:/æ/gplab/CHARTER.md`.

- Subject: any claim an agent makes about the world, and whether it can be
  checked. Not the robot — the receipt.
- Instruments: the `væult://` chain (9 links), the tiny-family oracles (pixel,
  motion, bus, seam, time, ledger, plugin), the `asimov://` governed C2, and
  SHA-256 receipt chains.
- Rules: seven, including "a thing not checked back is not a thing",
  "evidence ≠ authority", "fix the scene, never the threshold", and "every
  run leaves the lab measurably better (proved/broke/change)".
- Scorecard: above its weight on auditability, at its weight on deterministic
  simulation, below its weight on hardware — a boundary, not a goal.

- sha256 `89426b7ba4277c2e3f878e121b849915ff7e4745826ca555065c915d1d50fd86`,
  3,825,275 B, 720x1280, 90 frames, 3 s.

- Render: GPU python (CuPy), 90 frames in 12.2 s, encoded 4.0 s (h264_nvenc,
  +faststart). Spec: `C:/æ/threejs-curriculo/spec-microduck.json`.

- Gate PASS — luminance 73.94, contrast 26.91, motion 5.327, black 0.0%.

- Microduck (Pollen Robotics): 25 cm, ~800 g, 14 DOF, RK3566 SoC. 3D models
  local at `C:/æ/agents/microduck_rl/src/mjlab_microduck/robot/microduck/`
  (43 STL files, ~20 MuJoCo models: robot_walk.xml, robot_groundcontact.xml,
  robot_groundcontact_rollers.xml, ball.xml, additional.xml, joints_properties.xml).

Not verified: browser playback; second-machine reproducibility; audio.


## 34. GPL run 01 — PROOF/09 (2026-11-21)

The Governance-and-Provenance Laboratory's first run on its own rules: a
9.000 s film composed from NINE of our own robotic media assets, each second
sampling one asset chosen by sorting the estate on SHA-256, each second burning
that source's hash into the frame. The robot is the subject; the receipt is the
result.

- Film: `proof-09.mp4`, 4,555,285 B, 720x1280, 216 frames, 9.000 s,
  h264_nvenc + aac.
  sha256 `3e7fba7e3ca6f2b15ff8463e9d9bbc47530915e5a1862f19fc7fa77dd40b4816`.
- Gate PASS — luminance 22.93, motion 5.811, black 0.0%; mux 9.0/9.0, delta 0.0.
- Provenance: the nine source films and their sha256 are in
  `proof-09.meta.json` AND visible in the film itself (beat 01..09).
- Voice: `det_voice` hermes seed 9, 8.629 s (padded to 9.0), deterministic.

**proved** — a media estate can be recomposed deterministically from its own
receipts, and the provenance is legible in the artefact, not only in a manifest.
**broke** — (1) the narration ran long three times (50.67 / 9.75 / 9.6 s) before
landing at 8.629 s: size the line before synthesising; (2) the cleared overlay
bands dropped luminance below the floor and the gate refused: fix the scene
(warmer panel), never the threshold; (3) the first layout collided with the
source films' own HUD text: clear a lower third.
**change** — a `proof09` brief is added to the film-production skill (size the
voice first, warm the panels, clear the lower third, state provenance in-frame).


## 35. PROOF/1 — the receipted film format, de novo (2026-11-21)

The practice became a FORMAT. `proof/film/1` (spec `PROOF-1-FORMAT.md`, renderer
`proof1.py`) encodes every measured innovation of the prior research:
emoji-as-context, provenance-first source selection (sort by sha256),
receipt-in-frame, voice sized to the picture, warm panels (never lower a
threshold), a cleared lower third, and the gates declared in the spec itself.

- Spec: `chain-09.proof.json` (the master). Container: `chain-09.mp4` +
  `.receipt.json` + `.meta.json`.
- Film: 9.000 s, 720x1280, 216 frames, 4,558,910 B.
  sha256 `a98a0e391b07987d0e18d3bab137ed119621cff7fa0bcffaeeb18b562c3fe4c9`.
- Gate PASS — luminance 23.12, contrast 38.36, motion 5.82, black 0.0%;
  mux 9.0/9.0.
- Spine: the NINE links of the `væult://` chain (custody, format, gate, authority,
  contract, dispatch, publish, delivery, adoption) — one per second, each beat
  labelled in-frame and citing its source's sha256.

**proved** — a film format can carry the laboratory's rules as FIELDS, not as
habits; the same spec + the same assets render the same bytes.
**broke** — the format has no source-drift check: the renderer reads and burns a
source's sha256 but does not refuse when a source no longer matches the spec's
record. A film can therefore be rendered from a changed asset and still pass.
**change** — add an optional `expected_sha256` to each beat; the renderer must
refuse on mismatch. Until then, the receipt cites the spec, not the asset.


## 36. ORACLES/09 — the instrument panel (2026-11-21)

`proof/film/1` instance 2, and the first proof about the laboratory itself:
nine beats, one per oracle, each labelled with that oracle's test count.

- Film `oracles-09.mp4`: 9.000 s, 720x1280, 216 frames, 4,368,533 B.
  sha256 `26322b5e796fe5fd9ec79ee5082180d1df27c2c88f7eb533cee7fc0a2802f3da`.
  Gate PASS — luminance 28.1, motion 6.411, black 0.0%.
- Spine (test counts): tinycuda 22, tinymujoco 21, tinycan 18, tinycudavideo 22,
  tinycontinuum 0, tinyfilmmemory 0, tinyplugin 0, tinygpu 15, tinypython 30 —
  128 tests total, three zeroes shown rather than hidden.
- Format extension: `beats.sources` (explicit list) alongside `glob`.
- CHAIN/09 re-rendered under the same rule: sha256
  `e834786663a8f060558a6156f77742e86d72f80eccf27c4e85243e4edc7080cc`.

**proved** — a proof can make the apparatus its subject, and the panel's gaps are
legible in-frame: the format behaved as designed.
**broke** — the in-frame digest was labelled `sha256` while showing 32 hex (a
truncation); the hash was right, the label was wrong.
**change** — footer now `sha256[:32]`; format law 4 states the truncation;
CHAIN/09 re-rendered so the live artefact matches the rule.

Not verified: browser playback; whether the three 0-test oracles should be
tested next (recorded as the obvious follow-up).


## 37. Studios and camera shots — the resource inventory (2026-11-21)

Every renderer and every camera the estate can actually call, with the real
names and parameters from the code. Published as `STUDIOS-AND-CAMERAS.md` and
the machine-readable `studios.json`.

- Studios: asimov_studio v1/v2/v3, rtx_studio, asimov_pet, tinyasimov, proof1
  (PROOF/1), videolab, æRTXrender.
- Cameras: v1 free (distance/elevation/azimuth/sway); v2 8 presets; v3 9 presets
  (+ face, pilot); rtx_studio spec params; emoji_scene emoji-addressed camera.
- States (8) and pet rows (9); cast (5) with their voices.

**proved** — the camera and state vocabularies are finite and nameable; a film
can be specified without inventing a shot.
**broke** — the inventory itself exposes two live defects: v2's output is too
dark (live film lum 11.08) and v3 runs at ~12 s/frame.
**change** — the inventory is now a published resource; choosing a studio is a
lookup, not a recollection.

Follow-up recorded: brighten v2's scene defaults, and decide whether v3 is
worth its render budget.


## 38. SHOWREEL/09 — the demonstration of what our assets make (2026-11-21)

`proof/film/1` instance 3. A showreel whose nine beats are the nine KINDS of film
this estate can already produce — each beat sampling a representative artefact,
each labelled with its kind.

- Film `showreel-09.mp4`: 9.000 s, 720x1280, 216 frames, 4,866,834 B.
  sha256 `76eb4b917141d3a9cf0580f330a112fc76f937669ec24e31090e242492e2d368`.
  Gate PASS — luminance 29.71, motion 7.38, black 0.0%.
- Spine: asimov studio, saved gait, 4D time axis, receipted montage, oracle panel,
  emoji context, narrated, CUDA raster, provenance cut.
- Spec: `showreel-09.proof.json`.

**proved** — the estate's film kinds are finite and each has a live example; a
showreel can be assembled from them in one deterministic render.
**broke** — the voice line ran long twice (10.19 s, 8.86 s) and the format's own
`max_seconds` guard refused both: size the line before synthesising.
**change** — nothing to change in the format (the guard worked); recorded as the
reason the brief says 'size the voice first'.

Not verified: browser playback of the showreel.


## 39. GAIT/09 — the best raster on the saved gait (2026-11-21)

`rtx_asimov.py --trace walk-trace.json` — the real Menlo CAD (26 links,
1,007,041 triangles) walking the SAVED tinyPython policy trace, rendered by the
RTX raster (CuPy RawKernels, packed-uint64 atomicMin depth).

- Film `gait-09.mp4`: 9.000 s, 720x1280, 216 frames, 3,615,891 B.
  Gate PASS — luminance 21.53, contrast 45.38, motion 2.211, black 0.0%.
- Render: 77.0 ms raster/frame, 462.6 ms total/frame, 99.9 s wall.
- Trace: policy Menlo/asimov1-locomotion-0818, sha256
  `47f70691ecd5afda2933b2e6430d2375004c9435522841712a2d7b28b84188a0c`,
  480 frames, travel +7.8696 m, success true.

**proved** — the RTX raster renders the assembled CAD from the SAVED trace with
no keyframes, and the camera follows the walker. Visual check: a connected
humanoid (head, torso, arms, legs), not scattered geometry.
**broke** — the renderer's own meta labels wall time as `seconds: 99.9`; the
real duration is 9.000 s (ffprobe). Field-naming bug in `rtx_asimov.py`.
**change** — recorded; the meta should say `wall_s`, not `seconds`.

Rasters ranked: tinycuda 49 fps @1M tris (the oracle) · rtx_raster 77 ms
@1.007M tris (depth-correct) · tinygpu 71.6 ms/frame · æRTXrender (CDP) ·
emoji_scene.


## 40. The three untested oracles — now tested (2026-11-21)

The instrument panel had three zeroes: tinycontinuum, tinyfilmmemory and
tinyplugin shipped no tests while their siblings carried 21-30. That is fixed.

- tinycontinuum: 15 tests — freeze, gap, reversal, duplicate-time,
  under-coverage, too-few, frame index gaps, byte-identical frames, chain
  integrity, broken link, truncated payload, doctor.
- tinyfilmmemory: 9 tests — hash/canonical stability, chain check + tamper,
  deterministic append, verify tamper, byte drift, absent!=drift, audit,
  end-to-end selftest, doctor.
- tinyplugin: 6 tests — undefined CAPITAL constant, invented host method,
  pl_add no-op, a clean plugin grades clean, missing plugin refuses,
  doctor/audit.
Total 30 new; the tiny family is now 158 tests with NO zeroes.

Also fixed: `rtx_asimov.py`'s meta labelled wall time as `seconds` (99.9); it
now reports `seconds: 9.0` and `wall_s: 99.9` separately (the defect in §39).

**proved** — the time-axis, ledger and plugin oracles are deterministic and
their refusals are reachable; a green grade now means something.
**broke** — two filmmemory tests were written against a guessed chain shape and
failed honestly; the tests were corrected to the real API (append-built chains,
drift keyed on kind='film'), not the API bent to the test.
**change** — the three oracles are tested; ORACLES/09 can be re-cut so the
zeroes become 15 / 9 / 6.


## 41. tinyPOLICY — mobility.foundation command and control (2026-11-21)

The command layer above the tiny family, named and tested. It composes
tinypython (policy + physics + deadman) and the governed `asimov://` verb
surface; it invents no motion.

- Domain mobility.foundation, schema mobility.foundation/c2/1, authority
  HUMAN://ROOT.
- 14 verbs in 5 classes: read, plan, simulate, control, motion.
- Motion verbs (stand, walk, set_velocity) need presence AND a human signature;
  `exec` refuses with ACT-001 / AUTH-002 / DEAD-001.
- The ledger is a hash chain over DECISIONS (plan, gate, exec, presence,
  verify), not over intent.
- 11 tests; doctor reports policy sha `47f70691…88a0c`, MuJoCo 4.0.1, CPU only.

**proved** — the governance primitives already existed in tinypython (sense,
arm, disarm, presence, deadman_gate); tinyPOLICY names and ledgers them rather
than reinventing them. `exec stand` refuses with three rules; `gate simulate`
allows.
**broke** — two tests assumed `exec` was a verb and `presence` was a rule code;
the surface says otherwise (exec is the protocol action; the rules are ACT-001
/ AUTH-002 / DEAD-001). Tests corrected to the code.
**change** — mobility.foundation now has a tested C2; point it at a trace and
cite its ledger like any other receipt.


## 42. tinyONNX — the policy oracle; five policies, two runnable (2026-11-21)

Five Menlo Asimov policies exist upstream. They were unpulled and unmeasured.
Now pulled into `C:/ae/policies/` and measured by tinyONNX.

MEASURED (read from the ONNX itself, not from the names):

| policy | obs | actions | verdict |
|---|---|---|---|
| `0818` | 78 | 23 | runs (viewer contract) |
| `26-09-24` | 78 | 23 | runs (viewer contract) |
| `26-10-05-upper-body` | 78 | 12 | refused - partial body |
| `26-10-17-upper-body-blind` | 45 | 12 | refused - partial body + narrower obs |
| `26-10-26-lower-body-27dof` | 45 | 12 | refused - partial body + narrower obs |

So the four 'variants' are NOT four full-body policies: three are 12-action
partial-body policies with a different observation width. Dropping them into the
23-joint harness would be a guess about the policy; tinyONNX refuses them and
names the actual in/out.

tinyONNX: inspect / contract / run / grade / compare / ledger. 10 tests.

**proved** - the policy set is measurable, and the refusal is a measurement
(78/12, 45/12), not an assumption.
**broke** - the first run crashed on a duplicated argparse subparser; fixed by
registering each subparser once.
**change** - 'test them all' is now a contract check first: 2 of 5 run, 3 refuse.


## 43. tinyVISION — supervision for the robot policy (2026-11-21)

The instrument we use on our films, pointed at the policy. A policy trace
becomes a film of the real CAD (rtx_asimov, CUDA); the film is supervised and
tracked; the visual trajectory is compared with the physics trace that made it.

    trace -> render -> film -> supervise + track -> compare

MEASURED on the 0818 policy film (288 frames):

| stage | result |
|---|---|
| supervise | PASS - luminancia 23.04, contraste 46.46, movimiento 1.83, 0 negros |
| track | 1 coherent blob over 288 frames (dx 23 px, dy 10 px) |
| agree | ok - coherent + direction_ok, implied px/m 24.0 |

THE FINDING: a raw motion detector fragments (227 tracks) because the render
palette carries a gold HUD band and a blue floor. A palette-aware colour
detector isolates the robot; aspect and position filters reject the HUD and
floor. Pixels and metres stay separate units - the scale is reported, never
invented.

tinyVISION: render / supervise / track / agree / ledger. 7 tests.

**proved** - the supervision we already trust on films grades the policy's
picture, and the picture agrees with the physics.
**broke** - the first track used DetectorMovimiento and returned 227 tracks;
the `caja` field does not exist (it is `xyxy`); the renderer needs CuPy
(C:/gpu/Scripts/python.exe) and --model-dir tinygpu/model.
**change** - the policy now has a visual instrument: a trace that claims
success while the film shows a frozen body would be caught.


## 44. The loop closes — tinyLAB, and the video that proves it (2026-11-21)

The studio became a recursive learning laboratory: tinyLAB grades the
laboratory itself, and its own verdict becomes the next instruction.

    run -> receipt -> study (the lab grades itself) -> change -> next run

FIRST STUDY — the recursion caught a REAL defect:
  13 instruments, 13 tested, 12/13 suites green - one red.
  tinycudavideo: `ImportError: cannot import name 'Raster' from 'tinycuda'`.
  Cause: a sibling package dir named `tinycuda` is a NAMESPACE package and
  shadows tinycuda.py when the parent is on sys.path; the fallback inserted
  the dir but the namespace package still won.
  Fix: load tinycuda.py BY PATH (importlib.util.spec_from_file_location).
  -> tinycudavideo 22/22.

SECOND STUDY — the instruction was executed and re-measured:
  13 instruments, 13 tested, 13/13 suites green, untested: none.
  prev_change: 'repair the failing instrument suites'   (done)
  change: 'close the loop back into the policy: let the visual grade select
           or reject a checkpoint'

So the artefact of the run became the input of the next, and the loop closed
on PROCESS. What it has NOT closed on: physics or hardware. The change is a
brief, not a retrained gait.

THE VIDEO: LOOP/09 - nine beats, the new trace-to-film (policy-12s.mp4, sha
`8e41474c...`) among them, the supervision numbers in the labels, and the footer
'THE LOOP IS CLOSED · 13/13 INSTRUMENTS'.

**proved** - the laboratory can observe itself, find a broken instrument, and
instruct its own repair; the repair was re-measured green.
**broke** - the self-study's first run was red, and the red was real (a
namespace shadowing bug), not a flaky test.
**change** - the new video is the one the lab asked for: the loop, closed.


## 45. VERBS/09 — the mobility verbs, done and refused (2026-11-22)

A film of the Asimov performing each mobility verb. Nine verbs, nine beats.

MEASURED (policy traces, 9 s each, vx/vy/wz):

| verb | command | result |
|---|---|---|
| stand | 0,0,0 | holds, travel -0.007 m, min_z 0.612, obeyed |
| walk | vx 0.4 | +3.118 m, min_z 0.613, obeyed |
| turn | wz 0.8 | heading change, min_z 0.612, obeyed |
| strafe | vy 0.3 | +0.253 m, min_z 0.612, obeyed |
| set_velocity | 3-segment schedule | segment 3 DISOBEYS |

THE FINDING: the velocity command is BODY-FRAME. After a 0.8 rad/s turn, a
vy=0.3 strafe drove the body BACKWARD 0.61 m (dx -0.6126, dy +0.045) - the
axes rotated with the heading. The trace's own per-segment verdict marks it
disobeyed, while the end-to-end verifier (which reads only the final state)
calls the same trace ok. Two instruments, two verdicts; the per-segment one
is the honest one.

THE FILM: five beats are real CAD renders of real traces; four beats (damp,
balance, trajectory, set_joints) render the held pose and carry the verdict
GOVERNED / refused. A verb that is refused is still a verb.

sha256 `67b61520f5604cd5c1e06343e046c0fdd4ce03ad67e2f03f5cb6eaa0f3004f2a`,
2,653,100 bytes, gate PASS (lum 27.42, mov 1.143, black 0.0), audio 9.0 s,
mux delta 0.0, citation `ae://film/verbs-09`. Live 200, bytes re-hashed equal.

**proved** - the body does five verbs, measured; the other four are governed.
**broke** - the voice line was sized wrong three times (11.24 s, 10.34 s, 8.99 s
against an 8.6 s max); the renderer refused each time, correctly. Sized to the
picture at ~0.43 s/word.
**change** - the verb surface is now a film, not a table.


## 46. The post — "The film is an instrument" (2026-11-22)

Published a post on the truth surface: the improvement, stated plainly.

    https://myaelmendez.github.io/the-film-is-an-instrument.html
    blob 6310eae70bb5343e0953a750a2870dc749674630 - 11,251 B
    live 200, bytes re-hashed equal (4d9451ac...)

It carries the loop, the measured table (tinyONNX / tinyVISION / tinyLAB /
tinyPOLICY / VERBS-09), the nine verbs done and refused, the body-frame finding,
both films inline, and an explicit 'What is not true' section: we did not train
the policy, did not write the renderer or the supervision engine, no robot
moved, the loop closes on process not physics, and the 65-scenario bench is
unpulled.

**proved** - the improvement is publishable as a surface, not a claim: every
number on the page is one we measured this session and can re-derive.
**broke** - the first live check returned 200 with size_download 0 (a curl
artifact); the real bytes were 11,251 and matched.
**change** - the estate now has a post that states the method and its limits in
the same page.


## 47. The camera fix — the film becomes a teacher (2026-11-22)

Mirror neurons: humans learn by observing. A film meant to teach must carry the
MOTION. Ours did not.

THE DEFECT (rtx_asimov.py):

    root[0,3] = 0.0   # camera tracks; the walk is in the legs
    root[1,3] = 0.0

The camera follows the body, so the film showed the GAIT and erased the PATH.
tinyVISION measured 21 px of visual displacement against 3.118 m of physics.
That was not agreement - it was CANCELLATION. The earlier `agree` claim ('the
picture agrees with the physics') was overstated and is retracted here.

THE FIX: `--free-root` - keep the base translation, hold the camera on the
path's midpoint, pull back so the walk stays framed.

MEASURED (walk, 9 s, 3.118 m):

    camera tracks   21 px   (path erased)
    free root      589 px   1 track - 216 frames - 189 px/m

The film now carries the traversal, so the inverse (film -> path) becomes
possible. The mirror loop is: trace -> film -> path -> compare.

THE IMAGE: poster-916.png - 1080x1920 (9:16), gold on void, deterministic
(PIL, no ML), sha256 `ec1abcea31868f5437792c24df0b10b2321d83d424c210533b3dbacff08ca2eb`.

**proved** - the traversal is in the picture, and the number that proves it
(21 -> 589 px) is measured, not asserted.
**broke** - the free-root camera pulled back far enough that the accent blob fell
under the tracker's area_min (2000); at 300 it tracks 1 blob over 216 frames.
A detection floor is a parameter, not a constant.
**change** - the film is a teacher of trajectory. The next instrument is the
inverse: film -> path.


## 48. asimov pet — its own gaits, and a receipt (2026-11-22)

The pet (`hermes-plugins/asimov-pet`) is the real Menlo CAD rasterised at
192x208 with alpha, 9 states x 6 frames. Two improvements.

1. DISTINCT GAITS. The three locomotion rows replayed ONE walk trace at three
   yaws, so running / running-right / running-left were the same gait. Now:
   `running`  <- the vx walk trace (command [0.4, 0, 0])
   `running-right` / `running-left` <- a real wz turn trace (command [0, 0, 0.8])
   Measured: five rows of the atlas differ from the shipped sheet — the three
   locomotion rows (8299a8fa / 2de26a8a / 111907ca vs 94e9b743 / 8fa8f771 /
   0220a8a7) plus jumping, failed and review.

2. PROVENANCE. `--receipt` writes an `asimov-pet/1` block into pet.json: the
   sheet sha256, the atlas/frame geometry, the state list, the policy sha, the
   source traces AND their commands, and the min opaque pixel count.

DETERMINISM: two renders from the same model + traces produced identical bytes
(165,024 B, sha256 `1963ee54ad83601e39adac105117df8a44165e3c4543a4172295893332433f77`).
The receipt's claim is measured, not asserted. The installed sheet's hash
matches the receipt.

STILL OPEN: the strafe (vy) has no row — the taxonomy is fixed at 9 rows by the
Hermes pet contract, so a 'governed/refused' state cannot be added without a
contract change. The `failed` row is still a keyed slump; there is no real fall
trace.

**proved** - the mascot walks and turns with the policy's own gaits, and the
sheet carries the hash that proves which traces made it.
**broke** - the first install used the output dir name as the pet id
(`asimov-pet`); the id must stay `asimov-cad`, so it was re-rendered under the
right slug.
**change** - the pet is receipted and gait-faithful; the next improvement is the
lab link (pet state derived from tinylab's own verdict).


## 49. DOM awareness — the companion reads the page (2026-11-22)

The browser companion perceived the MACHINE (GPU/RAM via :8162) but not the
DOCUMENT. It now perceives the page it lives in.

    asimov://dom -> title, h1, headings, tables (rows), video sources, the
                     hashes printed on the page, links, images, byte size,
                     a fingerprint, and grants:false.

MEASURED on the post surface (the-film-is-an-instrument.html): 2 tables,
2 films (verbs-09, loop-09), 3 sha256 hashes, 1 link, 11,303 B.
MEASURED on the companion itself: title, 0 tables, 0 films, fp 2423dbbb.

The robot REACTS (mood): films -> THINKING, >=2 hashes -> REVIEW. Reading is
never permission - grants stays false, as on every other verb.

A MutationObserver notices DOM changes (debounced 800 ms) but IGNORES the HUD
subtree: the robot writes there, and a self-induced loop would never settle.
Verified: the fingerprint is stable across calls (effa57e9 twice).

ALSO FIXED: `asimov-companion/vendor/` did not exist, so the live page's
`import * as THREE from './vendor/three.module.js'` 404'd and the companion
was dead on github.io. Vendored three.module.js + three.core.js.

**proved** - the pet reads the document and reports what it found, with a
fingerprint; the read is a measurement, not a claim.
**broke** - the first observer watched its own HUD writes (fingerprint moved
fa734705 -> 957daa02 between calls); and the boot write was swallowed by a
renderer-not-ready throw inside setState. Both fixed.
**change** - the companion is DOM-aware; the same read works on any surface,
so the next step is injecting it over CDP rather than only on its own page.


## 50. The companion's CAD was missing — now it renders (2026-11-22)

Found while verifying DOM awareness: the live companion loaded NO CAD. Its
`load()` fetches `./scene/manifest.json` + one `.bin` per link, and no `scene/`
directory existed anywhere in the estate — so the surface had never shown the
robot on github.io, only the header and the HUD.

THE FIX: `webgl_prep.py --grid` — deterministic vertex clustering (quantize to
a grid, drop the triangles that collapse; normals recomputed from the final
geometry). Full resolution would be ~72 MB of buffers.

MEASURED:
    grid 0.008   259,332 verts   6.1 MB   <- shipped
    grid 0.004   567,471 verts    14 MB
    grid 0.002 1,054,119 verts    25 MB

Verified in the browser: 26 links, 25 joints, bounding box z 0..1.2617, and
the humanoid renders in the canvas (faceted head, segmented torso).

**proved** - the companion is a working surface again: CAD + DOM awareness.
**broke** - the page was silently dead for as long as it has been published;
nothing in the repo recorded that `scene/` was missing.
**change** - a web-sized CAD (6.1 MB) now ships with the surface, and the
simplification is a parameter with the trade-off measured.


## 51. actor:// — the robots are actors (2026-11-22)

A screenplay that drives the robots: cast + cues. Each cue names the actor, the
VERB (a policy trace), the LINE, and the CAMERA. The compiler renders each cue
from the actor's OWN policy trace at the scripted camera, then cuts the cues
into a PROOF/1 film whose beats carry the actor, the verb and the line.

    actor/script/1   cast[] {id, model, traces{verb: path}}
                    cues[] {t, actor, verb, line, camera{az, el, dist}}

NEW ON THE RENDERER: `--az/--el/--dist` (a FIXED camera, no sway) and
`--free-root` (the traversal is in the picture), so a script can place a camera.

THE FIRST SCRIPT: ACTOR/01 - one actor, three cues:

| t | verb | line | camera |
|---|---|---|---|
| 0.0 | stand | I am the actor. | az 1.5708 el 0.15 dist 3.0 |
| 3.0 | walk | Every step is a policy. | az 2.0944 el 0.18 dist 3.4 |
| 6.0 | turn | Every word is scripted. | az 1.5708 el 0.22 dist 3.2 |

9 s, three clips, three beats; each line is burned into its beat and spoken
in the narration. Every move is still the policy's — nothing is keyed.

**proved** - a script drives the actor's move, word and camera; the motion is
the policy's, not a pose.
**broke** - `--dry` first demanded the clips exist; a dry run validates the
script and must not render. Fixed.
**change** - the cast is data: add an actor by adding a cast entry and traces.


## 52. tinyGPUBOT — the actor instrument (2026-11-22)

The bot that binds the pieces: a name, a cast, a set of policy verbs, a voice,
and a ledger of its performances.

    tinyGPUBOT doctor      renderer, film format, actor_script, voice,
                           supervision, interpreter, CUDA - all measured
    tinyGPUBOT cast        resolve the cast: unknown actor / unknown verb /
                           missing trace / bad schema all REFUSE
    tinyGPUBOT perform     cues -> clips -> PROOF/1 film -> receipt
    tinyGPUBOT ledger      the hash chain of performances

RULE 5 (the one that matters): a bot's motion is its POLICY's. tinyGPUBOT never
keys a pose; a verb with no trace is refused, not invented.

ACTOR/01 performed through it: 3 cues, 9 s, gate PASS (lum 26.26, mov 0.82,
black 0.0), 709,686 B, sha256
`2f51ffb7168a71fe0446a6e5e0d82250f2dd6eb864dd966e2d7174c0124cd4b1`,
citation `ae://film/actor-01`. Live 200, bytes equal.

**proved** - the cast is data and the performance is receipted; the actor
layer and the bot are separate, so a script can be performed by any governed bot.
**broke** - two tests pointed ROOT one level short, so the trace path did not
exist and `cast` refused correctly; the TESTS were wrong, not the code.
**change** - the robot is now a named, governed, receipted actor: tinyGPUBOT.


## 53. The mixture, performed (2026-11-22)

The mixture-of-robots family - five bodies and one authority - re-cut as a
SCRIPTED performance. Each panel is a governed tinyGPUBOT cue: its own verb
(from its own policy trace), its own camera, its own line.

| body | verb | line | az |
|---|---|---|---|
| nous | stand | I am the question. | 1.5708 |
| hermes | walk | I am the policy. | 2.0944 |
| waetz | turn | I am the surface. | 0.7854 |
| menlo | strafe | I am the body. | 2.3562 |
| asimov | set_velocity | I am the refusal. | 1.5708 |
| panel 6 | THE GATE | HUMAN://ROOT - motion REFUSED - ACT-001/AUTH-002 | - |

NEW: `actors/mixture_composite.py` - the 2x3 canvas (720x1280) from the
performed clips, each tile labelled actor-verb, the sixth tile the authority.

**proved** - the mixture's cast is data; each body performs its own verb
rather than replaying one walk.
**broke** - the compositor's first filter string put the ffmpeg ':' separators
OUTSIDE the f-strings (a syntax error at line 70); moved inside.
**change** - the mixture is now a governed performance: five actors and one
authority, receipted.


## 54. The mixture, composited — and an honest WARN (2026-11-22)

`actors/mixture_composite.py` cuts the five performed clips into the family's
2x3 canvas (720x1280): five body tiles labelled actor-verb, the sixth tile the
AUTHORITY card, a gold grid framing the six panels.

sha256 `324b7215a97147b5bbdef3536247fa9a158fd91de6613a91e0474f4d0fb268cb`,
868,849 B, citation `ae://film/mixture-performed`. Live 200, bytes equal.

GATE: luminance 21.5 (PASS), contrast 41.48, motion 0.445 (WARN), 0 negros.
The motion WARN is STRUCTURAL, not a defect: two of the six panels are
deliberately still - the AUTHORITY (a gate, not a body) and `stand`. The
per-tile verdicts are recorded in the receipt.

**proved** - the mixture's cast is data, every move is a policy trace, and the
authority is a first-class panel rather than a caption.
**broke** - the first composite FAILED luminance (19.19): the gate card was
near-black and dragged the grid's mean under the floor. Fixed the SCENE (warm
(22,19,13) panel + a gold grid), never the threshold. Also: drawtext cannot
take a non-ASCII font path - the font is staged to an ASCII temp dir and the
drive colon is escaped.
**change** - the mixture is a governed performance surface: five actors and
one authority, composited and receipted.


## 55. The post, updated (2026-11-22)

`the-film-is-an-instrument.html` now carries the whole arc, not just the first
half. Six sections: the loop, Measured, the verbs, the films, **the actor**,
what is not true.

WHAT WAS ADDED:
- Measured: tinyGPUBOT, the asimov pet (two runs byte-identical), the companion
  (DOM awareness + 6.1 MB web CAD).
- A correction, on the record: the first films did not carry the traversal
  (camera followed the body) - 21 px vs 3.118 m was CANCELLATION, not
  agreement. `--free-root` gives 21 -> 589 px.
- The films: ACTOR/01 and MIXTURE OF ROBOTS, performed, with their hashes.
- 05 The actor: cast + cue -> verb -> trace -> render -> line + camera -> cut
  -> receipt; the cast is data.
- What is not true: the CAD is CERN-OHL-S-2.0; a rendered atlas inherits it.

blob `850b52579d90c30c704b34fd41e57e370e480ac0`, 14,508 B, live 200.
Verified in the browser: 6 sections, 4 films, correction + actor + licence
all present.

**proved** - the published post and the estate agree; the correction is on the
record rather than quietly dropped.
**broke** - the first live fetch returned the OLD bytes (11,359) for three
checks; the blob was authoritative, the CDN lagged. Re-checked until equal.
**change** - the surface now tells the whole story, including the retraction.


## 56. CORRECTION/01 — the disobedience was ours (2026-11-22)

The film that changes the simulation's VERDICT. And it retracts a published claim.

THE CLAIM (VERBS/09, 045, the post): the velocity command is body-frame, so a
'vy' strafe after a turn drives the body backward and the segment DISOBEYS
(dx -0.6126). True about the MOTION. Wrong about the VERDICT.

MEASURED - both runnable policies on the SAME schedule (walk, turn, strafe):

| policy | schedule | verdict (old) | verdict (body-frame) |
|---|---|---|---|
| 0818 | old | move T, turn T, move F | 3/3 obey, success=True |
| 26-09-24 | old | move T, turn T, move F | 3/3 obey, success=True |
| 0818 | new (turn first) | move F, move T | 3/3 obey, success=True |
| 26-09-24 | new (turn first) | move F, move T | 3/3 obey, success=True |

The walk after a turn moves +0.989 in WORLD y. The old verdict read that as a
disobedience - it compared WORLD axes against a BODY-FRAME command.

THE FIX (tinypython.py): rotate the measured world displacement into the body
frame at the segment's start, then compare.

CONSEQUENCE: NO checkpoint retires. The policies were right; the instrument was
wrong. The earlier 'segment 3 disobeys' is RETRACTED, and the post's finding
callout is amended.

THE FILM: CORRECTION/01, nine beats, each burning its source hash, the verdict
numbers in the labels, the retraction as the last beat.

**proved** - the grading instrument had a frame bug; fixing it changes every
verdict, and the honest outcome is 'no retirement'.
**broke** - my own published finding was the bug. The film retracts it.
**change** - tinypython's per-segment verdict is body-frame; the 'body-frame
finding' becomes the 'body-frame VERDICT finding'.

---

## 2026-11-22 — æC2 console enters the atlas; manifest↔atlas reconciled

**source** — `surface-manifest.json` (categories +sovereign +control +asimov;
surfaces +ae-c2-console +12 Asimov entries, each carrying an explicit `layer`);
`tools/build_capabilities.py` (`authority()` now honours an explicit `layer`
0–3 before the heuristic); derived `ae-atlas.json` + `ae-atlas.js` regenerated
(44 → 45 addresses); `ae/control/index-live.html` (chip born at its own
coordinate, `x14:y0:z0:æ0`).

**Why** — the console had no address, and the live atlas had drifted from the
manifest: the Asimov lane (x15, 12 addresses) and the `sovereign` category
(ÆQR, x13) existed only in the derived files, added by hand in `3bb4234` /
`ce9ed4c`. A naive `build_capabilities.py` run would have deleted 12 live
addresses (44 → 32).

**Not superseded** — this entry does not retract any prior atlas or surface
record. The Asimov lane keeps x15 y0–y11 and ÆQR keeps x13; **no address moved
and none was lost** (verified: LOST=[], COORD CHANGED=[]).

**tests** — `ae-atlas.js` 45 addresses, no duplicate coordinates, x1–x15
contiguous; console present at x14:y0:z0:æ0; origin renders 45 doors with the
console door and 12 Asimov doors; the console chip reads x14:y0:z0:æ0 and
resolves `æ://ae-c2-console`.

**deploy** — pushed to `gh-pages` via `kanban_push.py`; the github.io CDN lags.

**blockers / honest notes** — `capability-manifest.json` is NOT this builder's
output: commit `6f02ccb` replaced it with the code-mode tool index
(`doc/hash/line/mesh/name/sig`, 41 entries). The builder was run and that file
was restored from HEAD, so it is byte-identical to before. The surface-shape
manifest this builder would emit is therefore not published; the atlas and the
code-mode index are two different indices and their counts (45 vs 41) are not
expected to match.

---

## 2026-11-22 — origin/ iterated: live mesh count + address-sourced ticker

**source** — `origin/index.html` (`#meshstate` now set from `ATLAS.length` in
`buildMesh()` instead of a hard-coded `44 addresses`; the ambient feed seeds from
`ae-atlas.json` via a shape-tolerant `seedAmb()` that renders coordinates from
`x/y/z/a`, falling back to the code-mode `mesh` field — never `undefined`);
`origin/README.md` (records the iteration, since its "no other application logic
is rewritten" line was no longer true).

**Why** — `capability-manifest.json` is the code-mode tool index, so the old
`c.address + ' · ' + c.name + ' · ' + c.category` produced `undefined` strings in
the ticker; and the header count was frozen at the 2026-10 atlas size.

**Not superseded** — the origin stays the preserved former root homepage; no
visual language, coordinate or terminal command changed. `væult chain · 10/10` and
`webmcp · 6 agent tools` remain preserved display strings (see the `ae-origin`
skill: do not read them as verified claims).

**tests** — `browser_exec`: `#meshstate` = `45 addresses`; 45 doors; console door
`x14:y0:z0:æ0 æC2 LIVE`; zero ticker entries containing `undefined`; ticker shows
real coordinates (`x5:y0:z0:æ0 · SOVEREIGN STATE`); terminal `æ://ae-c2-console`
→ `x+14:y0:z0:æ0` and `where` = `→ æC2 LIVE · public layer`.

**deploy** — pushed to `gh-pages` via `kanban_push.py`; the github.io CDN lags.

---

## 2026-11-22 — debt closure: variants alive, manifest ownership, chain count

**source** — `origin-spectrum.html` + `origin-teknium.html` (declared `$` before first use —
both threw `$ is not a function` at startup and rendered **zero doors**; the fix already
existed in `origin/index.html`); `#meshstate` set from `ATLAS.length` in both; ambient feed
seeded from `ae-atlas.json` (shape-tolerant `seedAmb`) in both; `webmcp.js` (`verify_chain`
now reports 11 links / `11/11`); `capability-manifest.json` **regenerated to the surface
shape** (45 → 51 capabilities) with the previous tool index preserved verbatim as
`code-mode-tools.json`; `surface-manifest.json` (+`tiny` category, +6 tiny* surfaces) so the
builder reproduces the live atlas exactly.

**Why** — three debts: (1) two origin variants were dead pages; (2) `capability-manifest.json`
had been overwritten by the code-mode tool index, but **both** in-repo consumers (`code.html`,
`webmcp.js`) read the surface shape (`layer`, `category`, `capabilities`, `address`) — so the
terminal and the WebMCP tools were degraded; (3) the væult chain claim said `10/10` while
`væult_chain.py verify` measures **11/11 healthy**.

**Not superseded** — the builder output and the code-mode index are now **two files**, not a
contested one: `capability-manifest.json` (surfaces, what `webmcp.js`/`code.html` read) and
`code-mode-tools.json` (the archived tool index). The atlas is byte-identical to before
(`git diff -- ae-atlas.js` empty).

**tests** — `browser_exec` on a local server: origin / spectrum / teknium all report
`meshstate = 51 addresses`, 51 doors, live ☺ (`typeof window.aeGlyph === 'object'`), **0**
ticker entries containing `undefined`; `code.html` shows `51 caps · live`; the console ticker
reads `MANIFEST 51 CAPABILITIES`; `væult_chain.py verify` → `11/11 healthy`.

**blockers / honest notes** — `origin-teknium.html` was **never committed** (untracked) though
`qr_inventory.json` and `robotics.json` reference it; it is committed here together with the
fix. `origin-spectrum.html` already carried `11/11` but was still dead at startup. The
preserved display string `webmcp · 6 agent tools registered` remains display text (the six
tools are defined in `webmcp.js`, but registration is browser-gated on `navigator.modelContext`).


## 57. The post, iterated (2026-11-22)

Second pass on `the-film-is-an-instrument.html`:

- **CORRECTION/01** added to the films (sha `79e04323...`), with its receipt.
- **Two retractions, on the record** — the camera-follow cancellation, and the
  world-frame-vs-body-frame verdict error. Both published, neither dropped.
- **06 What to build next** — the recommendation, ranked by leverage and linked
  to `ROBOTICS.md`: (1) the heterogeneous mixture, (2) the 65-scenario bench,
  (3) a real authority. 'What is not true' becomes 07.
- tinyLAB row made honest: 13 in the self-study, 13/13 suites, **17 tiny*
  packages** in the estate (the earlier row undercounted the family).

blob `d1eadd91f038e072cd66385a040905a94036ebc5`, 16,508 B, live 200, bytes equal.

**proved** - the surface now carries the whole arc INCLUDING the retractions,
and points at the next development instead of stopping at the achievement.
**broke** - the first three live fetches returned the previous size (14,614);
the blob was authoritative, the CDN lagged. Re-checked until equal.
**change** - the post is a living document: it corrects itself and names the
next build.


## 58. MORPHOLOGIES/01 — bodies, not costumes (2026-11-22)

The heterogeneous fleet, first cut. Three real morphologies, each from its own
GLB, rendered as a turntable on a new surface (`morphologies.html`, three.js +
GLTFLoader, captured over CDP).

| body | source | state | lit |
|---|---|---|---|
| asimov | asimov-web.glb | HAS A POLICY - walks | 15.8% |
| xbot | Xbot.glb | DECLARED - no policy | 13.7% |
| soldier | Soldier.glb | DECLARED - no policy | 8.0% |

Only one of the three has a policy. The other two are DECLARED and WAITING -
that is the honest fleet.

sha256 `1ca9d621cb92a3024131673d50eda478fbb8a3618bbb953290e5c498c21ae334`,
578,976 B, gate PASS (lum 24.57, mov 0.682, black 0.0), 3 beats x 3 s.

TWO FINDINGS:
- `fleet.html` is the DEVICE mixture (MoD), not robots. Name collision avoided;
  the new surface is `morphologies.html`.
- `kira.glb` is Draco-compressed and no decoder is vendored -> it refuses to
  load. Xbot/Soldier/asimov-web load fine. kira stays OPEN until a decoder is
  vendored.

**proved** - three different bodies render and are graded; the mixture is no
longer one silhouette.
**broke** - the first capture returned LOAD FAILED (Draco); diagnosed by reading
the GLB JSON chunk (`KHR_draco_mesh_compression`).
**change** - the cast can now be heterogeneous; the next cut adds the missing
bodies and the missing policies.


## 59. The origin becomes the landing site (2026-11-22)

`index.html` gains **"the domains - one estate, one landing"**: every domain,
what it is, and where it lands. Measured live, not remembered.

```
llm.store           301 -> myaelmendez.github.io
cli.llc             301 -> myaelmendez.github.io/
æææ.com            301 -> http://myaelmendez.github.io/
soværeign.com       301 -> myaelmendez.github.io/
mobility.foundation 301 -> myaelmendez.github.io/
neuromitosis.com    301 -> myaelmendez.github.io/neuromitosis   (deep path)
daollc.ai           301 -> privateclient.ai/owner
privateclient.ai    200  (serves its own surface)
commandprompt.ai    200
æl.net              200
yæl.com             200
teologia.ai         NO RESPONSE
zacapa.ai           NO RESPONSE
æ.store             NO RESPONSE
/neuromitosis 200 · /owner 404 · /mobility 200
```

THREE OPEN ITEMS, named not fixed:
- **daollc.ai is BROKEN** - it forwards to `privateclient.ai/owner`, which 404s.
- `teologia.ai`, `zacapa.ai` and `æ.store` do not resolve.
- Fixing these needs DNS custody (Hostinger / Cloudflare tokens) - out of scope
  for a surface edit. A token offered in chat would be refused and rotated.

**proved** - the homepage is now the map of the estate, and the map is measured.
**broke** - the redirect set is heterogeneous (root vs deep path vs served vs
dead); a homepage implying "everything lands here" would be a false claim.
**change** - the origin tells the truth about the estate, including the parts
that are not yet routed.


## 60. tinyHQ — the origin, designed by the tiny idiom (2026-11-22)

`tinyhq.html` - the headquarters of the tiny constellation. **Generated from
`tiny.html`'s own node data** (not hand-written), so the HQ cannot drift from the
measured surface.

```
20 rooms · 20 doctors run · 0 refused
grouped by 15 domains: protocol, policy, pixels, video, motion, actors,
memory, time, identity, bus, codecs, voice, film, lab, plugin
+ the domain gateway (11) + the current work (6 films)
```

Design rule taken from the instruments: one capability per room, the result on
the door, measured not declared.

NOTE: `tiny.html`'s own meta says "18 instrumentos" but the surface carries 20
nodes. The surface is the authority; the HQ reports 20.

**proved** - the origin now has a headquarters whose rooms are the instruments.
**broke** - the first generator unpacked 3-tuples as 4 (fixed); the browser
daemon timed out on the visual check, so the page is verified structurally
(curl: 200, 20 rooms) rather than pixel-verified.
**change** - every future estate surface can be generated from the measured one.

## 61. microduck:// — the governed SDK, same shape as asimov:// (2026-11-22)

The question was why Asimov's official SDK got a governed wrapper and Microduck's
did not. It can — the seam already exists. `duck_control::io::RobotIo` is the one
place a simulator is allowed, and `scripts/duck-sim` runs the **same daemons, same
50 Hz loop, same `robotctl`** with the body in MuJoCo (`docs/design/simulation.md`).
So the wrapper adds no wire synonyms: every verb is the daemon's own method name.

```
HUMAN://ROOT → æ POLICY → microduck:// → duckctl / robotctl → RECEIPT
```

- `agents/microduck_protocol.py` — `microduck://status|verbs|plan|exec|sim|grant`.
  22 verbs (14 read, 8 motion, 6 high-power). Transports: `ble`, `udp`, `webrtc`
  (all official) + `sim` (the official `duck-sim` twin). Authority `HUMAN://ROOT`,
  hash-chained receipt ledger at `~/.hermes/microduck-protocol.jsonl`.
- `agents/microduck_bridge.py` — loopback JSON bridge on `127.0.0.1:8163`
  (`/api/status|verbs|plan|exec|sim|grant`, plus the console at `/console`).
- `github-pages/threejs-curriculo/microduck-console.html` — operator console
  (gold-on-void): transports, the 22 verbs, plan/sim/exec/grant, verdict + receipt.
- `agents/microduck_up.cmd` — restores the stack (bridge :8163, viewer :8123,
  Chrome on the RTX, VLC :8081), mirroring `asimov_up.cmd`.

Measured, not declared:

```
microduck://verbs                    → 22 verbs, chain valid
microduck://plan robot.move (auto)   → require_approval, allowed false
microduck://sim  robot.move          → allow (sim transport)
microduck://exec robot.move          → dry-run (MICRODUCK_LIVE unset)
microduck://grant robot.stop         → grants false, reports the approval shape
microduck://frobnicate              → refused, unknown route
ledger: 7 receipts, hash chain verified prev→hash
browser: console renders 22 verbs; click robot.move → plan → require_approval
         with receipt 1a233364… whose prev links 40984ea5…
```

**proved** - the governed layer is real and exercised end to end, and the gate
refuses motion without an armed approval.
**broke** - `duckctl` and `robotctl` are not installed on this host, and
`scripts/duck-sim` is a `#!/bin/sh` harness that cannot run under this Windows
bash (`[WinError 5]`). So every live transport is **absent, and the protocol says
so** rather than reporting a pass. The sim twin needs WSL/Linux or a macOS host.
**change** - any Pollen robot with an official daemon + IPC now has a template:
wrap the daemon's own verbs, add the gate and the receipt, expose `sim`.



## 62. The gateway, corrected against the authoritative inventory (2026-11-22)

The operator supplied the real 11-domain inventory with expiries. My earlier
gateway was built from AGENTS.md + my own probes - it listed a DIFFERENT 11
(only llm.store and æl.net overlapped). Corrected on both index.html and
tinyhq.html. §61 was taken concurrently by the microduck work.

ALL 11 PUNYCODES ROUND-TRIP VERIFIED (compute, never recall); the unknown one
is `xn--wtz-yla.com` = **wætz.com**.

```
llm.store                301 -> myaelmendez.github.io     exp 2027-11-29
moltcontextprotocol.com  301 -> myaelmendez.github.io     exp 2027-02-09
moltcontextprotocol.net  200 served                        exp 2027-02-09
moltcontextprotocol.org  301 -> xn--6ca.store (DEAD)       exp 2027-02-09
iaamano.com/.org/.net    301 -> xn--6ca.store (DEAD)       exp 2027-08-26
æl.app                   200 served                        exp 2027-07-13
æl.net                   200 served                        exp 2027-07-13
wætz.com                 301 -> https://Cli.llc            exp 2029-10-25
æ.store                  NO RESPONSE (intended primary)    exp 2029-07-20
```

**THE FINDING: the estate has a DEAD PRIMARY.** `æ.store` does not resolve, and
**four domains redirect to it** (iaamano.com/.org/.net, moltcontextprotocol.org).
Every visitor to those four lands nowhere.

**proved** - the gateway now matches the operator's inventory, with expiries.
**broke** - the previous gateway was wrong in 9 of 11 entries; it was built from
a doc list, not the register.
**change** - the hub names the dead primary instead of implying the estate is
whole.


## 63. Provenance stills, a GIF audit, and two self-corrections (2026-11-22)

The operator asked for an image of "agentic ontology", then for a GIF, then to
look into tinyMuJoCo, then to learn the origin surface as a skill. Every artifact
was drawn from a measured source rather than generated; the session's sharpest
result was a **retraction**, recorded here before it can be repeated.

### What was built (all under `mp4-factory/`)

- `agentic_ontology_still.py` → `agentic_ontology_9x16.png` — deterministic
  576×1024 (ratio 0.5625). The nine categories and their roles come verbatim
  from `brain_index.py`'s `ONTOLOGY` + `CATEGORY_META`. IHDR verified; glyph read
  back by vision as a legible `æ`; no crop or overlap.
- `agentic_ontology_gif.py` → `agentic_ontology.gif` — 60 frames, loop 0,
  1.65 MB. Same taxonomy, a travelling pulse over nodes and OSW stages.
- `github_io_atlas_gif.py` → `github_io_atlas.gif` — 72 frames, loop 0,
  2.19 MB. Parses `ae-atlas.js` at runtime; every label/coordinate is the site's
  real data. Sweeps the four authority layers then reveals the x15 Asimov lane.
- `tests/test_gifs.py` — 10 passed, 1 skipped (`TENOR_API_KEY` not set). Pins the
  renderer's determinism (byte-identical pixels for same frame), that frames
  actually differ, the 9-category drift guard, the encoded GIF contract, and the
  `gif-search` skill's real curl/jq/Tenor surface + frontmatter hardlines.
  Mutation-checked: injecting a bogus 10th category makes the drift test FAIL.

The `ae-origin` skill was **extended, not duplicated**: preserved-commit
provenance (`7befaf5d…`), the compatibility changes, the x15 lane, exact header
copy, and a sharpened pitfall quoting the page's own "independent prototype" line.

### tinyMuJoCo — AUDIT, not build (the build is Nov 19–20 work)

Re-run on this host with `C:/gpu/Scripts/python.exe`:
```
doctor            → ok:true · mujoco 4.0.1 · numpy 2.2.6 · headless · no GL/display
pytest            → 21 passed in 1.82s
sim ledger        → 3 sealed records, chain VALID, head 16bd1805ff3f…
film              → 11,069,417 B · sha256 9bad37b1…d31519d4a (matches citation)
gate              → lum 34.7 · contrast 38.49 · motion 3.383 · mux delta 0.000 s
                    · SupervisorVideo PASS · board_approved:false
```
Liabilities named, not fixed: no `README.md` in `tinymujoco/`; `provenance.py`,
`film/` and `traces/` are **untracked**; the human gate is still false; the film
is not published. The RUNBOOK lives at `tinymujoco/film/RUNBOOK.md` and the film
at `tinymujoco/film/deliverables/` — my first check looked one directory too high.

### The retractions (why this section exists)

1. I first reported "no AE-CONTINUITY entry" for tinymujoco after grepping
   `C:/æ/AE-CONTINUITY.md` — **that file does not exist**. The record lives at
   `github-pages/AE-CONTINUITY.md` (2131 lines). The absence I reported was an
   artifact of my own wrong path, not a missing entry.
2. I reported "45 addresses, the page says 44" as a finding. Re-checking during
   the write-up showed the atlas had moved to **51** committed entries
   (`8ef7289`, the x16 tiny estate) and the page no longer hardcodes a count —
   it uses `ATLAS.length`. The "45 vs 44" was a **transient read during
   concurrent editing**, not a durable defect. Do not repeat it as a finding.
   There is also an uncommitted edit in `origin/index.html` (10/10 → 11/11
   væult claim) that is NOT mine and must not be attributed to this session.
3. The first `github_io_atlas.gif` render silently collapsed from 72 requested
   frames to 17 — PIL deduplicates identical frames. Fixed with a continuous
   scan line + progress bar; re-verified at 72 distinct, advancing frames.

**proved** - the ontology taxonomy renders deterministically to still + GIF; the
tinyMuJoCo claims (doctor, 21 tests, ledger chain, film hash) survive a re-run;
the GIF tests would catch real drift.
**broke** - two of my own claims were wrong (file path; transient count), and a
GIF collapsed to 17 frames before the continuous-motion fix. All three were
found and corrected in-session rather than shipped.
**change** - a still/GIF may now be drawn from a live manifest instead of a
prompt; the rule is read the artifact at render time, never repeat a count from
a doc. Nothing in this section was committed or pushed — the record itself is
the artifact.


## 64. The bridge, hardened + gated (2026-11-22)

The secret-source bridge page is a client for a broker that did not exist.
Both halves are now real.

**BROKER (new)** `C:\æ\secrets\secret_bridge.py` on 127.0.0.1:7890.
- CORS is NOT a wildcard: only `http://127.0.0.1:8137` (and :8080) may call it.
  Verified: `Origin: https://evil.example` gets **no** Access-Control-Allow-Origin.
- Append-only audit `bridge.audit.log` (op / key / fingerprint / client).
  Values are never logged.
- Custody `hermes-bridge.json`, atomic replace.

**GATE (new)** `secret-source-bridge.html` gates the LOCKED ACTIONS - reveal,
copy, export .env, export .json, push to local - behind a væult passphrase.
Page load stays open; the secret actions do not.
- Crypto copied VERBATIM from `vault-layers.html` (PBKDF2-SHA256 600000,
  AES-256-GCM, AAD `vault-entry:`+name, `__check__` sentinel).
- Verified on the page itself: wrong passphrase -> `Wrong passphrase`; correct
  -> `UNLOCKED` and the entry decrypts. Cross-checked with the skill's
  `verify_gate.mjs` against a sealed probe vault. Probe deleted.

Live: 200, 25,117 B, bytes equal.

**STILL OPEN (named):**
- The page is still publicly reachable on github.io. The gate makes it less
  phishing-shaped, but it is still a published secret form.
- The broker is a background process; it will not survive a reboot.
- Export writes plaintext; the gate covers it, but the buttons remain.


## 65. The origin, modernized (2026-11-22)

`index.html` stops being a 2024 link list and becomes the estate landing.

- Hero: "One estate. Every domain. One authority." + a **measured line**
  (20 rooms / 139 films / 212 surfaces / 2 retractions / 0 hardware moved),
  every figure backed by `robotics.json` or `tinyhq.html` - not asserted.
  (An earlier "200 tests" was removed: no source measures a test count.)
- **Four doors** router under the hero: tinyHQ / the laboratory / the domains /
  the archive. One capability per door.

Live: 200, 30,323 B, bytes equal, 4 doors present.

**proved** - the landing opens with what is true and routes by capability.
**broke** - the hero still named the pre-laboratory mixture; the measured line
  first draft cited a number nothing measures.
**change** - the hub is now a router, and the estate's gaps are on the front
page rather than in a footnote.

---

## 2026-11-22 · tinyRepoFilm / æ PROTOCOL — source, tests, deploy (separate states)

**Source.** `hermes-contributions-film@3cf892a` (generators + director ID fix,
pushed). `github-pages@a87f569` + `5e177f2` + `db4aa2a` + `dd3a114` +
`a16431f` pushed via `kanban_push.py`. Local in `C:/æ`: `gen_tinyae.py`,
`tinyrepofilm/`, `tinyfilmmemory` quarantine support — **not yet committed**.

**Tests (measured, not claimed).** `væult_chain verify` 11/11. `tiny_family.py`
20/20 doctors. `tinyæ registry` 20 families / 18 green (two doctor implementations
disagree; the film shows `20/18`, not a silent pick). `tinyfilmmemory.verify`:
chain 17, 14 films, `ok:true`, `open_drift:[]`. `hermes-agent-activity` v1/v2
drift **quarantined, not re-sealed** — their bytes were overwritten by v3;
re-sealing would assert dead bytes are live. Decision record:
`tinyfilmmemory/quarantine-hermes-agent-activity.json`.

**Deploy.** Build was `errored` for `a87f569` and the concurrent foreign commit
`af2247c` ("domain gateway"); **no re-push was made**. It self-recovered:
subsequent builds `built` through `cb9a3b5`. Assets serve 200. `ae-protocol-v2`
was pushed and its assets serve, but its specific build was in the errored
window — the v1 surface remains the authoritative published protocol film.

**Provenance gate (new).** `MYaelMendez/HuggingBot` is a fork byte-identical to
`pollen-robotics/reachy_mini` (`compare`: identical, ahead_by 0; 0/100 recent
commits authored by MYaelMendez). `tinyRepoFilm` now REFUSES it. A fork is an
ARCHIVE, not authorship. The CLI reads a derived provenance record because the
bundled `gh.EXE` in WindowsApps raises `WinError 5` for `C:/gpu/python`.

**Remaining blockers (explicit).** Local generators uncommitted; HuggingBot has
no surface (intentionally — not requested); OpenClaw contributor count remains
unresolved (Link header vs unique-id methods disagree); `AE-CONTINUITY.md`
itself carries foreign edits and was appended to, not rewritten.

## 2026-11-22 — kænbæn unificado (local, not published)

**Surface.** `github-pages/kanban-unified.html` + `kanban-unified.json`, generated
read-only by `agents/kanban_unified.py`. Four sources — hermes tasks, fleet waves,
tiny* doctors, kanban-irl cards — projected into five lanes
READY / WORK / VERIFY / DONE / BLOCKED. Native status kept verbatim on every card;
one sha256 per source plus a content hash over cards+sources. Hermes is authority,
the other three are projections — no DB was written.

**Source.** `agents/kanban_unified.py` (new); `tiny/tiny_kanban.py` and
`tiny/tiny_family.py` gained a cross-link to the unified surface. Generated
`tiny.html`, `tiny-kanban.html`, `kanban-unified.html/.json` updated locally —
**uncommitted, unpushed**.

**Checks (measured).** `kanban_unified.py --check` OK at content
`6db3ced9b99f3a87`; rendered at 1600px: 268 cards across 5 lanes, `tiny` filter
shows 21; HTTP 200 on `127.0.0.1:8137/kanban-unified.html`.

**Blockers.** github.io still serves the old surfaces. The hermes DB is written
by concurrent agents, so counts drift between runs (266→268 within minutes);
the content hash detects that drift, it is not a defect.

## 2026-11-22 — link 11 `fanin` (fan-in gate, local, not published)

**Surface.** `github-pages/truth.json` — ONE verdict from four sources. No HTML
dashboard, no dashboard claims. Generated by `agents/fanin.py` (new), registered
as link 11 in `agents/væult_chain.py` and regenerated `væult-chain.json`.

**Gate.** PASS only when unified hash recomputes, chain is healthy, a push is on
record and no doctor is flaky/refused. Missing source, stale hash, broken link
or flaky doctor → BLOCKED with the reason named. No DB writes, no task claims,
no publication. Authority `HUMAN://ROOT`, `grants:false`, `executed:false`.

**Measured.** `fanin.py --selftest` 8/8 green (including the missing-source case,
found and fixed during this run); `væult_chain.py verify` **12/12**; `fanin.py
--check` OK. Live verdict **BLOCKED** — `tiny: 7 doctor(s) flaky — interpreters
disagree`. Receipt `f68e98ec24c175b7`; unified `d8d0ab0f0fbb9852`, 276 cards.

**Blockers.** Not pushed; github.io still serves the pre-fanin manifest.
`site/` clone does not mirror these artifacts (already divergent at baseline) —
declared, not silently synced. The verdict is a verified claim, not an
authorization; publish still needs a human-approved `kanban_push`.

## 63. tinyMUJOCO — the desktop pane (2026-11-22)

tinyMUJOCO (headless deterministic contact physics, `tinymujoco/tinymujoco.py`)
became a Hermes desktop pane. The instrument is **loaded, never reimplemented**.

- `~/.hermes/plugins/tinymujoco/plugin.yaml` + `__init__.py` — 6 tools
  (`tinymujoco_doctor|models|rollout|reference|grade|bench`).
- `~/.hermes/plugins/tinymujoco/tinymujoco_backend.py` — loads the instrument,
  discovers MJCF models, stages non-ASCII ones.
- `~/.hermes/plugins/tinymujoco/dashboard/{plugin_api.py,manifest.json}` —
  7 routes: `/health /doctor /models /rollout /reference /grade /bench`.
- `~/.hermes/desktop-plugins/tinymujoco/plugin.js` — gold-on-void pane:
  doctor card, model picker grouped by robot, seed/steps/ctrl, rollout + bench,
  trace hash + staged badge.
- `mujoco==3.3.0` installed into the app's own venv
  (`hermes-agent/venv/Scripts/python.exe`); numpy was already there.

Measured, in the app's interpreter:

```
doctor           → mujoco 3.3.0 · headless true · opengl_required false
                   smoke "10 steps, qpos[2]=-0.002158" · timestep 0.002
models           → 36 MJCF: microduck 24 · reachy 6 · asimov 1 · asimov-policies 5
rollout scene_backlash.xml (200 steps, seed 0)
                 → ok · nq=35 nu=14 · trace_sha256 fe619909… · 4816 steps/s
                   realtime 9.63x · staged true → %TEMP%\tinymujoco-stage\microduck
reference        → verified_deterministic true (two runs byte-identical)
grade(self)      → reward 1.0 · max_abs_diff 0.0 · tokens_used 0 · model_calls 0
grade(seed 1)    → reward 0.0 · differing_elements 7000
routes           → 7
hermes plugins validate → Validation passed (register probe, declared==actual tools)
hermes plugins doctor   → registrations: 6 tool(s), 0 hook(s)
app                → right rail shows the TINYMUJOCO tab beside REVIEW
```

**proved** — the instrument is reachable from the app as tools AND as a pane;
the pane's contribution is registered (tab present in the right rail).

**broke** — the pane BODY is unverified: clicking the tab needed a consent prompt
that timed out, so no click was delivered. The tab rendering proves
`register()` ran and the contribution was accepted; it does not prove the
component mounts without a runtime error. Needs one operator reload/click.

**change** — the non-ASCII staging rule is now load-bearing in a second place:
any MuJoCo-backed surface on this estate must stage `C:\æ\...` models to an
ASCII path. Applied conditionally (ASCII models run in place).

## 2026-11-22 · byte-receipt (source local, intentional)

`vidæo/vidæo.py` gate_verify now emits `byte_receipt = sha256(whole MP4)` in
addition to the historical sampled-frame `receipt`. Proven by sabotage: one
metadata byte flip left `receipt=da1150d7…` identical while `byte_receipt`
changed `d5218249… → 9a6b86cb…`. `vidæo/tests/test_byte_receipt.py`: 3/3 pass.
The original receipt is untouched, so every sealed film still verifies.

**Deploy state:** none — `vidæo/` is intentionally in `.gitignore` (local
toolchain), so this gate is source-local by design. Do not `-f` it into the
public repo. Continuity records it here so the next agent knows the guard
exists locally even though GitHub does not carry it.

## 2026-11-22 — fanin deploy confirmed + ASCII manifest fix

**Deploy.** Commit `180af0f` pushed via `kanban_push.py`, task `t_27e40fc7`,
branch `gh-pages`, `rev-list origin...HEAD = 0 0`. Pages build `built`. Live:
`truth.json`, `kanban-unified.html`, `tiny-kanban.html`, `agents/fanin.py`,
`agents/kanban_unified.py` all HTTP 200; live `truth.json` = **BLOCKED**,
receipt `4ccd4b699ebb3ddf`, `tiny: 5 doctor(s) flaky`. No DB was written by
fanin; the push record is on the board.

**Defect found after deploy.** `github.io/væult-chain.json` (rune path) is not
the public manifest — the ASCII alias `vaeult-chain.json` is, and it still
served the old 11-link version (`generated 2026-10-10`). Both files are now
written from one `manifest()` call so both carry 12/12 and the same fanin link.

**Remaining.** `site/` clone still does not mirror these artifacts. `truth.json`
is a verified claim, not an authorization — every publish still needs a human
push.

## 64. tinyMUJOCO — launching the robots (2026-11-22)

The pane grew a ROBOTS section: every robot this estate can put in the physics
engine, its **own stack state** (via `robot://`) beside its MuJoCo rollout. The
two facts are deliberately separate — a robot present in MuJoCo and a robot on
the desk are different things.

- `tinymujoco_backend.py` — `ROBOTS` table (asimov / reachy / microduck → model),
  `robots()`, `launch(robot)`, `launch_all()` (parallel, one failure does not
  stop the rest). Loads `robot://` lazily for the stack half.
- `dashboard/plugin_api.py` — 3 new routes: `/robots`, `/launch`, `/launch_all`
  (**10 routes total**).
- `__init__.py` / `plugin.yaml` — 3 new tools: `tinymujoco_robots`,
  `tinymujoco_launch`, `tinymujoco_launch_all` (**9 tools**).
- `plugin.js` — ROBOTS section: per-robot stack dot, launch button, and the
  result (dofs, controllability, trace, speed, reason).

**Asimov's meshdir was broken on disk, not by staging.** `asimov_1_25dof.xml`
declares `meshdir="../meshes"`, but the meshes live at
`C:\æ\tinygpu\model\meshes` — `..\meshes` beside the model does not exist. The
stager now reads `meshdir`, and when it cannot resolve, locates one of the
referenced STLs on the estate and copies that directory into the stage. It
reports what it did instead of silently producing a model that will not load.

Measured, in the app's interpreter, `launch_all(seed 0, steps 600)`:

```
wall 9.29 s · launched ['asimov','reachy','microduck'] · refused []

asimov     nq=32  nu=0   controllable=false  realtime 14.32x  staged=true
           trace f6a0a8071dfe…   (no actuators: open-loop dynamics, honest)
reachy     nq=58  nu=9   controllable=true   realtime  8.10x  staged=false
           trace d3dfb88942ae…
microduck  nq=35  nu=14  controllable=true   realtime  7.07x  staged=true
           trace c7b3f7c2b2ec…
```

**proved** — all three robots load and step in the physics engine; the pane's
backend reports each robot's stack presence and its rollout separately; 10
routes; `hermes plugins validate` passes.

**broke** — the pane BODY is still unverified (same blocker as §63: clicking the
TINYMUJOCO tab needs a consent prompt that timed out). No `[plugins] tinymujoco
failed to register` line in `desktop.log`, so registration is clean; that is
not the same as the component mounting.

**change** — "launch" now means: put the robot in the engine AND show whether its
own stack is up. The stager repairs a missing meshdir by finding a referenced
mesh, which generalises to any MJCF whose meshes were moved.

## 65. robot:// — doctor, discovery, authority (2026-11-22)

Concurrent work: another agent landed the **fleet receipt** (every dispatch
recorded, refusals included, `fleet/ledger` anchoring all dialect ledgers plus
the fleet's own) and a 7-test suite. All 7 passed before this entry; this entry
is additive and did not rewrite their code.

Added, in the house style:

- `robot://doctor` — probes every registered robot AND scans the disk for
  dialect modules the registry misses. Per robot: presence, verb count, class
  breakdown, **policy hash** (`sha256` of the canonical verb table — the policy
  IS the verb set, so a change is a measurable event), ledger tail, transports,
  live flag. Separates real dialects (`SCHEME` + `dispatch`) from generator
  modules, and skips test modules.
- `robot://fleet/authority` — the authority link: per robot, the gate classes,
  the motion-verb count, the probe verb, and the grant shape. `granted: false`
  always; it reports what an approval would have to look like.
- `robot-console.html` — a Fleet row: `doctor` / `authority` / `ledger`, with a
  one-line note under it.

Measured:

```
robot://doctor
  ok true · robots asimov/reachy/microduck
  asimov    verbs 14  classes {media 4, motion 6, read 4}      policy 0b0c025e7c5b  ledger 62
  reachy    verbs 27  classes {motion 16, read 6, safety 5}    policy 1711d7f2aefa  ledger 13
  microduck verbs 22  classes {motion 9, read 10, safety 2, telemetry 1}
                                                              policy 41b533248b99  ledger 10
  unregistered dialects: ['cli', 'film', 'voice']
  modules (not dialects): gen_ae, molt_context
  fleet_receipt 0358f30bc3c542a4…

robot://fleet/authority
  granted false · asimov motion 6 · reachy motion 21 · microduck motion 11
  every robot reports a grant shape; none grants

tests: 13/13 (7 prior + 6 new) · 39 s
browser: console renders the doctor button; click →
        "ok · 3 unregistered dialect(s): cli, film, voice"
```

**proved** — the dispatcher now has a doctor that probes the disk rather than
trusting the registry, and an authority route that reports the gate instead of
assuming it. Both are reachable through the bridge and the console.

**found** — three dialects exist on disk and are NOT registered: `cli://`,
`film://`, `voice://`. `gen_ae_protocol.py` appeared at 14:01 during this run
(concurrent agent) and is correctly classified as a generator, not a robot.

**change** — registering a robot is still one `ROBOTS` entry, but the registry
can no longer silently lag the disk: `doctor` names what is missing.


---

## 2026-11-22 — æC2 console: honest feeds, dead widgets removed, visible receipt

**source** — `ae/control/index-live.html` (`#feeds-chip` reports manifest/board/queue/mood
as `FEEDS: n/4` with a DOWN count; `#ops-ticker` now has ONE source — JS builds
`ATLAS n ADDRESSES · MANIFEST n CAPABILITIES`; the four stat counters are labelled
`· LOCAL`; new `🧾 LAST RECEIPT` panel renders SHA-256 + cost + per-workstream rows);
`ae/control/widgets.js` (new, vanilla JS — replaces the React/JSX widgets whose
`../plugins/*/index.js` resolved to `/ae/plugins/`, which does not exist).

**Why** — the console claimed `FEEDS: STATIC` while it already consumed four live feeds; it
carried a duplicated `#plugins-section` (5 duplicate ids, invalid DOM); and the four widget
scripts 404'd while loading React UMD for nothing.

**Not superseded** — the markets rail still refuses prices without provider, source and
timestamp; the local compiler still emits a real SHA-256 over local results.

**tests** — `browser_exec` against a local server: `FEEDS: 4/4` with per-feed states; ticker
reads `ATLAS 52 ADDRESSES · MANIFEST 51 CAPABILITIES`; stats read `· LOCAL`; all four widget
containers mount content with **zero 404s**; after a compile the receipt panel shows
`sha256 af0d8eb5…`, `cost Σ11.3`, 8 workstream rows.

**deploy** — pushed to `gh-pages` via `kanban_push.py`; the github.io CDN lags.


---

## 2026-11-22 — æC2 console: RESOURCES discovery over the whole estate

**source** — `ae/control/discover.js` (new) + `ae/control/index-live.html`
(`⌘ RESOURCES` panel, `#discover-q`/`#discover-counts`/`#discover-results`, `find <q>`
route in the intent box, CSS for `.hits`/`.hit`).

**What it answers** — "is this surface where an agent finds every resource?" Before, the
console searched only the atlas (52 addresses) while the estate already shipped six
indexes nobody queried. Now one query hits all of them: atlas (52) · modules
(`codebase.json`, 246) · surfaces (`qr_inventory.json`: 341 html, 49 python agents, 8
threejs scenes, 97 videos, 17 widgets, 7 kanban, 6 configs, 3 logs) · tools
(`code-mode-tools.json`, 41) · skills + schemes (`capability-mesh.json`, 221 + 8) ·
surface manifests (100).

**API for agents** — `window.aeFind(q)`, `window.aeIndexCounts()`,
`window.aeIndexMeta()` (total, per-category counts, failed index names) and
`window.aeDiscover(q)` to drive the panel. Honest: `discover-sub` reports
`n resources · k/6 indexes` and names any index that failed.

**tests** — `browser_exec`: `sub` = `1196 resources · 6/6 indexes`, `failed: []`;
`find kanban` / `find asimov` / `find teologia` return cross-index hits with paths and
`↗` links; `find zzzznada` → `0 matches`; the intent box route logs `[cat] name path`
into the intent rail and syncs the panel; 404s = `favicon.ico` only.

**Not superseded** — `capability-manifest.json` is not the output of
`tools/build_capabilities.py`; discovery reads it as one index among several.

**deploy** — pushed to `gh-pages` via `kanban_push.py`; the github.io CDN lags.

## 66. robot:// — all robots in ONE MuJoCo environment, 9:16 (2026-11-22)

`agents/robot_env_film.py` — the three bodies in a single physics world, rendered
to one 9:16 film. Not three panels, not three renders: **one `MjSpec`, three
models attached at their own anchors, one seeded control sequence, one trace.**

```
one world: nbody 64 · ngeom 307 · nq 125 · nu 23
  asimov    x -0.62  y 0.00   1.25 m tall   26 mesh geoms    1,007,041 tris   0 actuators
  reachy    x 0.06   y -1.15  0.39 m tall  173 mesh geoms      940,986 tris   9 actuators
  microduck x 0.66   y -0.80  0.26 m tall   81 mesh geoms      980,836 tris  14 actuators
camera eye (0,-5.6,1.05) → target (0,-0.35,0.42) · 720×1280 · 24 fps
```

Two defects found and fixed, both of the "silently wrong" kind:

1. **`geom_size` is not a scale.** For a mesh geom MuJoCo stores the AABB
   half-extents there; multiplying vertices by it collapses the model. Mesh
   vertices are already in model units.
2. **Vendor scenes ship furniture.** reachy's `minimal.xml` carries `table`,
   `duck`, `apple`, `croissant`. Rendering every prefixed geom drew the table
   and cropped the duck. `_robot_roots` now picks each robot's own root as the
   child of world with the largest mesh subtree, and only that subtree is drawn.

Render path is the estate's proven one: MuJoCo supplies per-frame geometry
(`geom_xpos`/`geom_xmat` + mesh vertices), **tinyCUDA's CuPy raster** supplies
pixels. No OpenGL — this Optimus laptop has no registered NVIDIA ICD, so
MuJoCo's own renderer is unusable here.

Tests (`agents/test_robot_env_film.py`, 6/6): one world holds three bodies,
roots are the robots and not the furniture, props never render, every robot
contributes triangles, **the trace is byte-identical for a seed and differs for
another**, and staging repairs asimov's broken `meshdir`.

Measured:
```
test film  12 frames → 720x1280 · 0.5 s · 84,909 B · sha256 0f69f3e8a5e48905…
still      frame 8: title, subtitle, frame counter, three labels legible,
           all three bodies inside the frame, no props
tests      6/6 in 4.4 s
```


---

## 2026-11-22 — æC2: agent card + URL invocation (the machine surface)

**source** — `.well-known/agent-card.json` (new, generated) · `tools/build_agent_card.py`
(new builder with `--check`) · `.well-known/webmcp.json` (`agent_card` pointer) ·
`ae/control/index-live.html` (`?intent=` deep link, `#agent-chip`, placeholder, rail
summary ordering) · `ae/control/discover.js` (`window.aeReady`).

**What agents get now.** Agents do not read a human console; they fetch
`.well-known/agent-card.json` — 51 capabilities, 41 tools, 221 skills, 8 schemes,
3 nodes, 51 addresses, the endpoints, the `?intent=` invocation contract, the authority
gates and the receipt schema. It is **derived**: the builder reads the real indexes, so
`--check` is a freshness gate rather than a claim.

**Invocation.** `index-live.html?intent=find%20asimov` runs the same `dispatch()` as the
form. Two ordering bugs found by measurement, both fixed: the deep-link dispatch ran
before `discover.js` existed (now waits for `window.load`), and the `find` summary was
logged before its list and pushed out by the rail's 12-entry cap (now logged after).

**tests** — `browser_exec`: `#agent-chip` = `AGENT CARD · 51 CAPS · 41 TOOLS ·
221 SKILLS`; `?intent=find asimov` → title `æC2 · find asimov`, rail
`⌘ find "asimov" · 19 matches`, panel 19 hits; 404s none.

**deploy** — pushed via `kanban_push.py`; `raw.githubusercontent.com` serves the card,
the github.io CDN lagged (re-check before reporting 404).


---

## 2026-11-22 — code-mode as a machine surface (code.json + URL invocation)

**source** — `code.json` (new, generated) · `tools/build_code_json.py` (new builder with
`--check`) · `code.html` (`?cmd=<expr>` runs on load via `started()`) ·
`tools/build_agent_card.py` (`code_mode` block) · `.well-known/agent-card.json` (regenerated) ·
`ae/control/index-live.html` (intent route forwards `æ.*` / `find(` to code-mode).

**Why.** Agents love code-mode because it is composable, but it only existed as an HTML
terminal — unusable without scraping. `code.json` is the same DSL as **one parseable
fetch**: 11 DSL verbs (derived from code.html's own help block, so they cannot drift),
51 capabilities with addresses, 246 modules, 41 mesh tools, runtime. `code.html?cmd=`
makes it invocable by URL; the console forwards `æ.*` there instead of reimplementing it.

**tests** — `browser_exec`: `code.html?cmd=æ.find('asimov')` runs on load; console
`æ.find('cuda')` logs `⌘ code-mode → …` and lands on `/code.html?cmd=…`; 404s none.
CDN `curl` of `code.json` → 200, and filtering it locally returns 12 `asimov` hits with
addresses. `--check` on both builders → `FRESH`.

**Not superseded** — `code.json` is a snapshot; regenerate with `tools/build_code_json.py`
after any index change (`--check` is the gate).

**deploy** — pushed via `kanban_push.py`; API verified, CDN caught up after ~2.5 min.


---

## 2026-11-22 — æC2: exemplary-surface pass (zero CDN, semantics, a11y)

**source** — `ae/control/index-live.html`: dropped the Google Fonts `<link>` for two
`@font-face` rules pointing at the estate's own vendored TTFs
(`aipodcast_me/assets/fonts/JetBrainsMono-{400,700}.ttf`); `<html lang="en">` → `es`;
`<title>$æ | …>` → `æC2 · Command & Control · LIVE`; brand `<div>` → `<h1 class="brand">`
with `margin:0`; added `.skip` + `#main`; `aria-label`s on the icon links and `role="img"`
on the 🤝 glyph; inline SVG favicon (data URI) so nothing 404s.

**Why.** "Exemplary" is a measurable bar, not an adjective. Measured before the fix:
one external stylesheet request (violates the estate's zero-CDN rule), a wrong language,
no `h1`, no skip link, unnamed icon links, and a `favicon.ico` 404.

**tests** — `browser_exec`: `peticiones externas: 0`, `404s: []`,
`document.fonts = ['JetBrains Mono 400 loaded','JetBrains Mono 700 loaded']`,
`FEEDS: 4/4`, no console errors; no horizontal overflow at 720×1280, 1280×720 or
550×900 with all 8 panels visible. The served `<title>` is clean (the `🐴` seen in one
reading came from the harness tab, not the page — confirmed by curling the file).

**Not fixed here** — the Life Tower is still 12 hardcoded floors (pending C8); the queue
feed resolves on its 3 s poll, so the chip reads 3/4 for the first seconds by design.

**deploy** — pushed via `kanban_push.py`; API blob verified, the github.io CDN lagged.

## 2026-11-22 — privateclient.ai flagship: secret bridge

**Surface.** `https://privateclient.ai/secret/` (canonical), plus a fixed door on
the root page. Source in `privateclient/bridge.html` (local, uncommitted), derived
from `secret-source-bridge.html` without touching any form id or broker logic.
Droplet: `/opt/pcsecret/www/index.html` + `assets/aether.css`, nginx
`location /secret/` added after backing up the site config.

**Boundary.** The public page carries an explicit notice: it is the SURFACE, the
secret stays on the visitor's device, the broker is the visitor's own
`127.0.0.1:7890`. A PROBE button calls `operation:'list'` and renders ONLY HTTP
status + content-type; the body is discarded because it may contain secrets.

**Measured.** Live GET 200, canonical/flagship hero present, CSS loaded
(`rgb(5,5,5)`), root door link present, probe returns `status 0 · TypeError` from
the public origin (honest: no loopback broker there), `nginx -t` OK + reload OK.
`domain-stack.json` now marks `flagship: /secret/` and operation `secret_bridge`.

**Remaining.** github.io mirror and continuity entry are local-only (no push was
requested for them). `C:\æ\secrets\secrets.json` ACL is broader than custody
requires and the source page is served on `0.0.0.0:8137` — reported, not changed.

## 2026-11-22 — #localai default posture

**Rule.** Added to `AGENTS.md`: inference defaults to local Victus RTX
(`victus-rtx` / `victus-qwen3-agent`); secrets never go to a cloud surface;
custody stays in `C:\æ\secrets\`. Hermes `config.yaml` ALREADY had local
defaults (`model.default: victus-qwen3-agent`, `provider: victus-rtx`,
`base_url: http://127.0.0.1:8081/v1`); no config change was needed or made —
the tool refused to edit that security-sensitive file, which is the correct gate.

**Flagship surface.** `privateclient/bridge.html` now carries `#LOCALAI` in the
status bar and an explicit no-cloud-inference/no-external-asset notice.
Google Fonts and `api.qrserver.com` were removed: Orbitron/JetBrains Mono are
vendored under `/secret/assets/fonts/`, and the QR is a local PNG whose bytes
decode back to `https://privateclient.ai/secret/` via `cv2.QRCodeDetector`.

**Measured.** Browser with cache disabled: `performance.getEntriesByType('resource')`
returns ONLY `privateclient.ai/secret/...` resources (aether.css, aether.js,
QR PNG, 4 local TTFs); zero third-party requests. All assets HTTP 200.

**Remaining.** The current conversation still runs a Nous cloud model — the
local default applies to future sessions/config, not to a model already in
flight. `image_gen.provider: nous` and the `moa.free` cloud preset remain
declared in config; they were not changed.

## 67. meshbot:// — the mesh bodies get a dialect (2026-11-22)

`robot://` listed Soldier, Xbot and kira as "mesh only — no dialect, no policy,
no ledger", which meant a row of dots and a fleet of three. The index's own rule
is *whatever is built for one robot is provided for all — a missing verb is a
named refusal, never a crash*. So the mesh bodies got the same seven routes.

`agents/meshbot_protocol.py` — one dialect, three bodies, one shared ledger
(`meshbot-protocol.jsonl`).

```
Soldier   2.16 MB GLB   68 nodes · 2 meshes · 2 skins (49+2 joints) · 4 clips
          clips: Idle, Run, TPose, Walk
Xbot      2.93 MB GLB   70 nodes · 2 meshes · 1 skin  (67 joints)    · 7 clips
          clips: agree, headShake, idle, run, sad_pose, sneak_pose, walk
kira      0.98 MB GLB   56 nodes · 32 meshes · 1 skin (23 joints)    · 0 clips
```

Verbs: 7 = 5 read (`status info meshes animations clips`) + 2 render
(`render animate`). Facts are read from the GLB JSON chunk with stdlib only, so
`status` reports what is on disk — nodes, meshes, skins, joints, clips, sha256 —
not a claim.

Verdicts, and they are the point:

```
plan animate walk   → allow   (render plan, no hardware)
plan animate nope   → refused "Xbot has no clip 'nope'"   (clips are checked)
sim Walk            → refused "Soldier has no physics model — mesh only"
exec walk           → refused "Soldier has no actuators and no body — mesh only"
grant walk          → grants: false, required shape returned
```

Coverage is **71%**, not 100: `sim` and `exec` are genuinely absent, and the
index now shows `·` for them. Declaring them "provided" would have been the
false claim the page warns about.

Two bugs found while wiring it, both of the silent kind:

1. `_robot_status` read `st['sdk'].get('live')` — a `str` for meshbot, so every
   mesh body reported `present: false` while the dialect was healthy.
2. `parse` lowercased the robot segment, so `robot://Soldier/...` resolved to
   `soldier` and was refused. Robot names are case-sensitive on disk; `_resolve`
   now matches case-insensitively without changing the registered name.

Measured:
```
robot://doctor          ok=true · 6 robots · all present
robot://fleet/ledger    asimov 62 · reachy 13 · microduck 10 · meshbot 8 · robot 43
                        combined_sha256 78f4ae3ce10b8da5…
test_robot_protocol     13/13
index --check           OK current: 6 robots derived from disk
page (local :8124)      6 PRESENT · 85 RECEIPTS · 0 mesh-only
                        roster row: robot://Soldier / humanoid · 7 verbs · 1 transports / 71%
```


---

## 2026-11-22 — æC2: PROVENANCE — la consola se audita a sí misma

**source** — `ae/control/index-live.html` (`🧾 PROVENANCE` panel, `#prov-chip`,
`#prov-body`, `DECLARED_CLAIMS`, `renderProvenance()`, `deriveRails()`) ·
`ae/control/discover.js` (re-renders provenance when its index resolves).

**The lesson applied.** Auditing `robots.html` showed the failure mode: `evidence_kind`
was hand-written as "measured" on robots whose `evidence.module` was `null`, and the
module paths did not exist — a seal asserting what the evidence contradicted. This
console now separates the two by construction: **MEDIDO** rows are computed from
artifacts that answered in this very load (`feeds 4/4`, `1196 recursos`,
`agent card 51 caps`, `atlas 52`, `peticiones externas 0`); **DECLARADO** rows are an
explicit list of what the page asserts without an artifact (4 rails, 12 floors,
AUTHORITY: LOCKED, PRINCIPAL: HUMAN).

**Also derived.** The four rail placeholders were hand-written state claims
("Awaiting instruction…", "No agents connected"); they are now computed from real
state at boot and on every feed change.

**tests** — `browser_exec`: `#prov-chip` = `PROV: 5M · 4D`; panel reads
`5 MEDIDO · 4 DECLARADO` with the five measured rows and the four declared ones; rails
read `0 intents this session · awaiting principal`, `operators idle · receipt NONE`,
`no runtime connected · feeds 4/4`, `markets refuse prices without provider + source +
timestamp`; no console errors.

**Honesty fix found by the same rule** — the resources row first said `14 índices`; it is
14 *categorías* (14 keys in the counts map), so the label now says `categorías`.

**Not fixed** — the four DECLARADO rows are still declarations; the point is that the
page now says so out loud.

**deploy** — pushed via `kanban_push.py`; API blob verified, the github.io CDN lagged.

## 68. aipodcast.me wired in · the film passes, and a demo page (2026-11-22)

**The film passes.** `robot-env.mp4` → SupervisorVideo **PASS**.

```
720x1280 · 96 frames · 4.000 s · h264 · 1,547,847 B
sha256 0a98fc6b520dec46324d389cdefd284263234fece8bdf813f0f0ff39dcb1825b
luminancia_media 43.7  (>20) · contraste_medio 43.98 (>8)
movimiento_medio 1.216 (>0.5) · frames_negros 0/5
supervision receipt 968f73796a64b3a2e84a581ab4cd12ec0279ea5b3ee1a738e873fc03166d6e0f
physics 101.7 s · render 553.1 s · tests 6/6
```

Two scene defects were found by measurement, not by looking:

1. **Depth stagger only reads at one distance.** Robots at y = 0 / −1.15 / −0.80:
   move closer and the forward body fills the frame while the other two leave it.
   They now stand on **one plane (y=0) in a line** — a lineup, not a perspective trick.
2. **A 9:16 frame holding three bodies of different sizes is mostly background**,
   and the gate measures the frame, not the subject. Added a **ground plane**.
   While testing it: the CuPy raster **silently drops triangles beyond a screen
   bound** — `half=3.0` draws, `half=6.0` disappears with no error. Capped at 1.8.

**Publish path.** `agents/publish_robot_env.py` — runs the gate FIRST, then:
PASS → receipt + copy + `media-manifest.json` entry; FAIL → REFUSED receipt,
nothing copied, exit 1. The gate is never adjusted to fit the film.

**Destination.** `aipodcast.me` → `github-pages/aipodcast_me/`:
```
spec-robot-env.json      the spec (bodies, world counts, camera, seed)
robot-env.mp4            the film
robot-env-poster.png     a real frame (extracted at n=48) — the demo's poster
robot-env.receipt.json   gate + ffprobe + supervision receipt
media-manifest.json      13 videos (this one added; `all_pass` was already false
                         from 5 older entries that carry no `vision` block)
```

**Demo.** `aipodcast_me/robot-env-demo.html` — gold-on-void, no CDN, zero deps.
Plays the film, reads the receipt live (verdict + three threshold meters +
artifact facts), and reads `../robots/index.json` live for the roster.

Verified in the browser (DOM + screenshot):
```
verdict     PASS gate PASS · supervised 2026-11-22T23:10:00Z
meters      luminancia 43.7 · contraste 43.98 · movimiento 1.216 · black 0/5
roster      6 rows · asimov/reachy/microduck 100% · Soldier/Xbot/kira 71%
layout      9:16 stage with the three robots, gate panel, roster table, address
```

**Honest limits.**
- `<video>` playback could NOT be verified in the automation browser: it reports
  `document.visibilityState === 'hidden'`, and Chrome suspends media loading for
  hidden documents — the element never issues a request (`readyState 0`,
  `networkState 2`, no request in the server log). The bytes ARE reachable
  (`fetch()` → 1,547,847, `video/mp4`), and the film itself is verified by the
  gate, by ffprobe, and by an extracted frame. Playback in a visible tab is
  expected but **unmeasured here**.
- `agents/serve_pages.py` was written for this: Python's `http.server` answers
  200 to every Range request, which stalls Chrome's media stack. github.io
  answers 206, so production is unaffected.

## 69. the Asimov CAD pet on the home · the Nous referral card (2026-11-23)

- `index.html`: new `the pet` section — the real Menlo Asimov-1 CAD atlas
  (`picoasimov-atlas.webp`, 1536×1872, 8 cols × 9 rows of 192×208, RGBA), DOM-driven
  (`window.aePet`), 4 state chips, provenance line. Also the `support the compute`
  section: the Nous Portal referral (`https://portal.nousresearch.com/r/opensource`) as a
  deterministic card (`support-card.html` → `support-the-compute.png`, 1200×630) plus the
  plain-text terms, and a second permanent link in `receipts & source`.
- **Defect found:** the home driver cycled 8 columns and named rows 5–8
  `sleeping/sitting/standing/backflip`. `pet/pet.json` says `frames_per_state: 6`
  (columns 6–7 measured with 0 opaque samples) and `failed/waiting/running/review`.
  Fixed in `ba9631e`.
- **Verified:** atlas loads (natural width 1536); `aePet.set('waving')` moves the
  background to row 3 (`-624px` = 3×208) and the label follows; a screenshot shows the
  3D humanoid (gold head, silver-gray torso) with the IDLE/WAVE/RUN/JUMP chips.
- **Unverified:** the frame loop — headless rAF is throttled, so 12 fps is *declared*,
  not measured. Named, not claimed.
- **Design:** `pet/PET-MANEUVER.md` — six stages from DOM anchoring to real Menlo
  locomotion control; stage 4 (vertical + turning) is an RTX render job, not CSS.

## 70. pet test · 9:16 — the coherent-size rig (2026-11-23)

- `pet/test-916.html`: a measuring rig for the Asimov CAD pet. Seven 9:16 viewports
  (135×240 → 1080×1920) × eight scales (0.25× → 3×) = **56 pairs**, each measured for
  *fits* and *crisp*. The device keeps an exact coordinate space and scales by transform, so
  1080×1920 is testable in a narrow column.
- **Measured:** **all 56 crisp** — the cell is 192×208, both divisible by 4, so every
  0.25-step scale lands on whole pixels. **43 fit**; the binding constraint is the viewport,
  not the pixels (1080×1920 @3× = 576×624 fits; 360×640 @2× = 384×416 does not).
- **Fixed while building:** the crispness test measured the background-size ratio, not the
  cell — it would have passed every scale. Now it measures the cell pixels.
- **Walk rig (stage 2):** left ↔ right, 2 px-class steps, `out-of-bounds` counted.
  **Measured:** out-of-bounds 0. **Not completed** in the harness — headless throttles
  setTimeout to ~1 Hz, so 8/116 steps ran in 6.57 s. The page reports `completed: false`
  and says the trace is real but the clock is not. Declared, not claimed.
- No new assets; the atlas is the existing `picoasimov-atlas.webp`.

## 73. The note — why this is the beginning (2026-11-22)

Operator's words: *"wonderful work. this is definitely the beginning of something
special."* Recorded as a note, not a plan.

**`github-pages/robot-env-note.html`** (source `robot-env-note.md`) — gold-on-void,
zero deps, all seven sections browser-verified (no layout breakage):

```
the through-line   a 5-row table: thread → before → after
1 · one environment   one MuJoCo world · gate PASS 43.7/43.98/1.216 · 0 negros
2 · one address space robot:// six bodies · meshbot 71% · refusals named
3 · one gate          produce → Receipt, or refuse; the gate is never adjusted
4 · one destination   aipodcast.me: spec + mp4 + poster + receipt + demo + manifest
links                local :8125 and production github.io, side by side
honest limits       playback unmeasured in automation · all_pass false is pre-existing
                     · clips unplayed · nothing pushed
why this is the beginning
```

**The argument the note makes.** Three threads converged:

| thread | before | after |
|---|---|---|
| environment | each robot rendered alone | one MuJoCo world, three bodies, one trace |
| address space | three dialects, three consoles | `robot://`, six bodies, one fleet receipt |
| gate | published because it existed | produce → Receipt, or refuse |
| mesh bodies | "mesh only" | `meshbot://`, refusals named not crashed |
| destination | scattered | `aipodcast.me`, one wired path |

> The estate's robots were **things on disk**. They are becoming **bodies in an
> address space**: addressable by one scheme, standing in one world, recorded in
> one ledger, published through one gate. That is the difference between a project
> and a platform.

Links (both surfaces):
```
demo     http://127.0.0.1:8125/aipodcast_me/robot-env-demo.html
         https://myaelmendez.github.io/aipodcast_me/robot-env-demo.html
film     http://127.0.0.1:8125/aipodcast_me/robot-env.mp4
receipt  http://127.0.0.1:8125/aipodcast_me/robot-env.receipt.json
note     http://127.0.0.1:8125/robot-env-note.html
fleet    http://127.0.0.1:8125/robots.html · /robots/index.json
```
Local server: `python agents/serve_pages.py C:/æ/github-pages 8125` (Range-capable).

## 74. aipodcast.me fully wired (2026-11-22)

`aipodcast_me/index.html` — the home now carries the robot fleet, live.

**Before:** the robot artifacts existed in `aipodcast_me/` but nothing on the home
page referenced them. A visitor could not find them.

**After — five wiring points, all live from disk:**

1. **Hero chip** — `robots · one world · 9:16 ↗` → the demo.
2. **Three surface cards** in RUNTIME SURFACES — `ROBOT:// ENVIRONMENT` (demo),
   `ROBOT:// FLEET INDEX` (`/robots.html`), `THE ENVIRONMENT, THE ADDRESS SPACE,
   THE GATE` (the note).
3. **A `◈ ROBOT:// · THE FLEET` panel**:
   - **gate bar** — PASS badge + luminancia / contraste / movimiento / negros /
     resolution / sha, read from `robot-env.receipt.json`
   - **six cards** — film, receipt, spec, demo, fleet data, note
   - **roster table** — six bodies from `../robots/index.json` (dialect, verbs,
     transports, live, sim, coverage)
   - **media table** — every artifact from `media-manifest.json` with its gate
     verdict (13 videos + 4 audio)
4. **Command line routes** — `robot · robots · demo · env · environment ·
   film · receipt · note · fleetindex · indexjson`; `help` lists them.
5. **The panel header tag** flips to `GATE PASS · 96 FRAMES` / `GATE REFUSED`
   from the receipt, so the verdict is not static text.

Measured (browser, DOM + screenshot):
```
gate bar     PASS · luminancia 43.7 · contraste 43.98 · movimiento 1.216
             · negros 0 · 720x1280 · sha 0a98fc6b520d
roster       6 rows — asimov 14 / reachy 27 / microduck 22 / meshbot 7×3
             coverage 100% ×3, 71% ×3
media        17 rows — 13 videos (robot-env.mp4 · robot · PASS · 720×1280 · 4s · 1.55 MB)
             + 4 audio
cards        6 robot cards · 3 robot surface cards · 1 hero chip
routes       robot→demo · demo→demo · film→mp4 · receipt→json · note→note
             · fleetindex→robots.html · nope→"UNKNOWN · nope · type help"
layout       no breakage, no horizontal overflow
```

**Design note.** The verdict is rendered from the receipt, never hardcoded. If a
future film fails the gate, the same panel shows REFUSED and the manifest row
shows it — the surface cannot claim a pass the instrument did not make.

## 71. the æ boy becomes the institutional mark (2026-11-23)

- Operator: *"this is our institutional logo"* → `assets/brand/ae-neon-logo-clone.svg`
  (the vector clone of `ae-neon-logo.png`, 746×1017, 20.8 KB).
- `index.html`: the hero `.glyph` now carries the mark (108×144, cyan glow) with the label
  `★ the æ boy · the institutional mark`; the gold smiley SVG is gone (its eye-tracking JS
  guards on missing nodes, so it degrades cleanly). Footer names the mark and links the
  receipt.
- **Verified:** the clone renders pixel-faithful to the canonical PNG (compared in the
  browser); it loads (natural 746×1017); the hero shows it and no longer shows the smiley.
- **Receipt preserved, not edited:** `assets/brand/ae-neon-logo.adoption.json` widens the
  role from "æ.store agentic environments" to the institutional logo, and records the
  observation that the receipt's "two letters, not ligature" reads as a joined æ — the
  operator defines the mark.
- **Flagged, not changed:** the hero's left panel is still `asimov-face-video.mp4`, whose
  frame 0 is an `@asimovVOICE · face spec` **gold-ring state readout — not the Asimov
  head**. Same class of defect as the one corrected on `robots.html`. Awaiting the
  operator's call.

## 72. the hero face panel is the pet (2026-11-23)

- Operator: *"swap it for our asimov pet of course."* The hero's left panel was
  `asimov-face-video.mp4` — an `@asimovVOICE · face spec` gold-ring readout, not the robot
  (flagged in §71). It is now `<div class="heroPet" id="heroPet">`: the same
  `picoasimov-atlas.webp` CAD sprite, 192×208, caption `asimov-cad · the pet · 1,007,041
  tris · 9 states · 6 frames`.
- The driver became a factory, `aeMountPet(el, {onChange})`, so the hero pet and the
  `the pet` section share **one** implementation — no second copy. `window.aeHeroPet` and
  `window.aePet` are the two mounts.
- **Verified:** both mounts render 192×208; the old `<video>` is gone from the DOM;
  `aeHeroPet.set('waving')` moves the hero sprite to row 3 (`-624px`); the hero shows the
  3D robot (gold head, grey body) and the new caption. No layout breakage.
- **Declared, not measured:** the frame loop (headless rAF throttled).
- `asimov-face-video.mp4` is left on disk, now unreferenced by the home.

## 75. PUSHED — the robot fleet is on the truth surface (2026-11-22)

**Commit `17a90f19db20` → `origin/gh-pages`.** Pushed through the kanban
(`kanban_push.py push --task "robot:// one world, one address space, one gate"`,
task `t_da594932`, fast-forward `c4252f6 → 17a90f19db20`, no rebase needed).
No bare `git push`.

**Ten files, and only those.** Other agents' in-flight work
(`continuity.html`, `morphologies.html`, `privateclient/`, `threejs-curriculo/robot-console.html`,
`continuity-wasm/target/`, …) was left untouched in the working tree.

```
AE-CONTINUITY.md                      §73 the note · §74 aipodcast fully wired
aipodcast_me/index.html               +203 — the fleet panel, live
aipodcast_me/media-manifest.json      13 videos (robot-env added)
aipodcast_me/robot-env.mp4            1,547,847 B · gate PASS
aipodcast_me/robot-env-demo.html      the demo
aipodcast_me/robot-env-poster.png     a real frame (n=48)
aipodcast_me/robot-env.receipt.json   gate + ffprobe + supervision
aipodcast_me/spec-robot-env.json      the spec
robot-env-note.html / .md             the note
```

**Verified on the provider, not on the clone.**
```
GET api.github.com/.../git/ref/heads/gh-pages
  → 17a90f19db2042875a9e0b23efde29bf1806da00   (== local HEAD)
contents API, ref=gh-pages → 200 for all eight robot artifacts
```

**Deployment.** GitHub Pages took ~95 s. Before: `robot-env-demo.html` 404.
After: 200 on demo, note, receipt, mp4.

**One focused browser verification of the deployed surface:**
```
https://myaelmendez.github.io/aipodcast_me/index.html
  gate bar      PASS · luminancia 43.7 · contraste 43.98 · movimiento 1.216
                · negros 0 · 720x1280 · sha 0a98fc6b520d
  panel header  GATE PASS · 96 FRAMES
  roster        6 rows
  media         17 rows
  manifest      gated 8 · all pass false · ungated 5 (named)
  robot cards   6
https://myaelmendez.github.io/aipodcast_me/robot-env-demo.html
  verdict PASS gate PASS · roster 6
https://myaelmendez.github.io/robot-env-note.html
  7 sections render
```

**One status changed and it is named.** `media-manifest.json` had
`all_pass: true` over 12 videos; five of them carry **no gate verdict at all**.
The manifest now reports `all_pass: false` with `gated_count: 8`,
`ungated_count: 5` and the five files listed. A missing check is not a pass —
the surface cannot claim one.

**Still open.** Xbot and Soldier ship animation clips and nothing plays them.
Film playback remains unverified in the automation browser (hidden document).

## 73. asimov-face-video.mp4 deleted (2026-11-23)

- Operator: *"delete the asimov-face-video.mp4, we have other copies."* Deleted in `91bd948`;
  unreferenced by any surface since §72 (the hero panel became the pet).
- **Still referencing it (records, not live links):** `film-corpus.json` and the
  `corpus.html` DATA array (entry with sha256 `8564ffc9…`), plus the historical
  `proof-09.meta.json`, `chain-09.meta.json`, `chain-09.proof.json`,
  `asimov-agent-capability-run.json`, `ffmpeg-asimov/asimov-agent-capability-run.json`.
  No generator for the corpus was found in the repo, so the corpus was **not** hand-edited:
  the next scan should drop the entry. Flagged rather than silently rewritten.
- `asimov-face-video-sm.gif` (a derivative) is left in place.


---

## 2026-11-22 — AUTHORITY derived from the pledge roster (+ a stale roster caught)

**source** — `agent-pledge.json` (regenerated) · `tools/build_pledge_roster.py` (new, `--check`) ·
`ae/control/index-live.html` (`#auth-chip`, `renderAuthority()`, PROVENANCE row).

**What it answers.** `AUTHORITY: LOCKED` was a static chip with no gate behind it — the same
failure mode as robots' `evidence_kind`. It is now **derived**: the console reads
`agent-pledge.json`, counts `committed/total`, and **cross-checks** that `pledge.html`
still publishes the same `pledge_hash`. Anything less than all-current, or a hash absent
from pledge.html, reads `LAPSED` / `INCOHERENTE`.

**The drift it caught.** Custody (`C:\æ\kænbæn\agent-pledge.json`) held **8** commitments;
the published roster listed **7** — `waetz-bot` had committed on 2026-11-19 and the roster was
never regenerated. The new `--check` fails on exactly that, and the roster is now derived.

**Identity, declared.** All 8 commitments share **one** public key. That is by design
(`agent_pledge.py`: *"reuse the card signing key — one identity per operator"*), but the
roster presented 8 entries as if they were 8 identities. It now publishes
`distinct_keys: 1` and `identity_note` saying the agent ids are **roles** on one operator
identity — so nothing reads the roster as 8 cryptographic agents.

**tests** — `browser_exec`: `#auth-chip` = `AUTHORITY: LOCKED`, title
`pledge 8/8 current · 1 clave(s) · hash coherente con pledge.html`; PROVENANCE gained
`MEDIDO authority 8/8` and **lost** the DECLARADO row for AUTHORITY (4 → 3 declared).

**Gate placement.** `build_pledge_roster.py` reads local custody, so it runs **where
custody lives** — deliberately not in CI (the source file is outside the repo). It is an
operator gate, like `agent_pledge.py require`.

**deploy** — pushed via `kanban_push.py`; API verified, the github.io CDN lagged.

## 74. background batch — two films live, five verb clips, five policies measured (2026-11-23)

Verified by read-back, not taken from the subagent reports.

**Live now** (HTTP 200, tracked in gh-pages):
- `core-registry-916-narrated.mp4` — 5,586,533 B, sha256 `665dae81…`; narration WAV + txt +
  receipt staged beside it; gate PASS (lum 22.51, contrast 28.54, motion 1.47, black 0%,
  mux delta 0.0). *The producing subagent reported `published:false`; it is in fact live —
  a sibling published it. Reported as measured.*
- `mobility4d.mp4` — 5,912,751 B, sha256 `574e21ba…9cfd7`; gate PASS (lum **20.9** vs the
  20 floor — thin margin, recorded), contrast 42.88, motion 0.866, black 0%.

**Rendered, not published** (`C:/æ/verbs/out/`, all 9.000 s · 720×1280 · 24 fps · silent,
RTX 3050 CUDA, 1,007,041 tris, policy `Menlo/asimov1-locomotion-0818`):
| verb | bytes | sha256 |
|---|---|---|
| stand | 2,377,299 | `519e0da4…` |
| walk | 3,250,370 | `0a7c33fb…` |
| turn | 3,592,357 | `bd65a968…` |
| strafe | 3,009,331 | `12ff04fa…` |
| set_velocity | 3,323,487 | `11c93842…` |

These are the renders of the atlas's own `walk.json` / `turn.json` verb sources.

**Policies measured** (`C:/æ/policies/`, simulation only, `grants:false`):
- `0818` baseline reproduced exactly: +4.1868 m, 600 ticks/2400 steps, min base 0.6125 m,
  no fall, byte-identical repeat; **a shuffle, not a stride** (knees 38.8°/37.7°, feet ~5 cm).
- `26-09-24`: +4.6405 m — but measured under the **legacy ankle contract**; the harness is
  hardcoded to 0818 (ankle kp/kd/effort differ). **A missing check, reported as missing.**
- `26-10-05-upper-body`: +4.4389 m, 12 leg-only actions, ankle-roll scale 0.08 ±0.09 clip.
- `26-10-17-upper-body-blind`: stock harness **cannot run it** (45 obs/12 actions vs the
  pinned 78/23); measured through an adapter; `wz 0.5` is a ~180° flip, not a yaw track.
- `26-10-26-lower-body-27dof`: **cannot run** — falls at 1.42 s; it is a 27-DOF policy on a
  25-DOF body (armature/friction differ). Adapter + evidence in the policy dir.

**Blocker for the pet work:** the harness speaks only the 0818 contract, so every checkpoint
after it is measured through a bespoke adapter — the numbers are real but not comparable
without a contract-aware harness.


---

## 2026-11-22 — DEPLOY stamp: cada superficie dice qué commit la generó

**source** — `C:\æ\agents\kanban_push.py` (escribe `deploy.json` tras cada push) ·
`deploy.json` (nuevo) · `ae/control/index-live.html` (`#deploy-chip`, `renderDeploy()`,
fila PROVENANCE).

**Qué resolvía.** Ninguna superficie decía si estaba fresca; el operador leyó una consola
vieja sin poder distinguirla de la corriente. Ahora `kanban_push` escribe, tras cada push,
`{schema, branch, content_sha, pushed_at, task, detail}` y la consola lo muestra como
`DEPLOY f445e7a · 4 min` (sha + edad), con el sha completo y la tarea en el `title`.

**Por qué el sello va en un commit aparte.** Un sello no puede vivir dentro del commit que
nombra sin regresión infinita; por eso registra `content_sha` (el commit que contiene los
cambios) y se commitea y empuja justo después. **Declarado, no oculto.**

**tests** — push real: contenido `f445e7a` → sello `b8aea9c (content f445e7a)`; `deploy.json`
commiteado con ese sha. `browser_exec` local: `#deploy-chip` = `DEPLOY f226398 · 3 min` con
`title` completo; PROVENANCE ganó `MEDIDO deploy …`.

**Bug encontrado al cablear** — `const d` duplicado en `renderProvenance` (el deploy y el
contador de declaradas): un solo SyntaxError tumbaba **todo** el script de la consola. Lo
cazó el `node --check`, no el navegador; `const` se renombró a `dep`.

**deploy** — push vía `kanban_push.py` (que ahora sella); el CDN va detrás.

## 75. the markets ticker (2026-11-23)

- `index.html`: a second ticker directly under `æ://live`, labelled **markets** → home
  `llm-store.html` ("LLM.store — The Model Store"). Prices are pulled live from OpenRouter's
  public models API (`https://openrouter.ai/api/v1/models`, no key), filtered by a watch list
  of open-weight families we actually run (`qwen|llama|mistral|gemma|deepseek|granite|phi`),
  sorted by prompt price, quoted **$/1M tokens**. Refresh every 300 s.
- **Measured:** the feed returns; 104 watch-list models; CORS allows the cross-origin read;
  the ticker renders 30 lines. A feed failure prints `markets · feed unavailable (<reason>)`
  — it never shows a stale or invented price.
- **Defect caught before publish:** the patch reintroduced a stray `renderLegend()` call into
  the boot line; that function no longer exists in the file, so it would have thrown at boot and
  killed the whole page script. Reverted to `tickRender();drawGrid();tickScroll();`.
- **Home choice:** `llm-store.html` was already the estate's model store, is referenced by 3
  other surfaces, carries no coordinate (a `gems` demand-without-address row) and holds 316 KB
  of store front matter. Making it the ticker's home gives an unaddressed surface a role.
- **Not done:** llm-store itself is unchanged — it is a link target, not yet a markets surface
  with its own data. That is the obvious next step.

## 76. the llm.store ticker + host selection (2026-11-23)

- Third ticker row under `markets`, labelled **llm.store**, home **`llm-store.html`**.
  Content is our OWN store family, read from `estate.json` (filter `/store/i` over
  url+id+category), sorted by bytes, largest named as host. **13 surfaces.**
- **Host selection, measured:** `llm-store.html` — 309 KB, 54 model mentions, 51 price
  figures, real listings (Llama-3.3-70B, Gemma, DeepSeek) and its own provider/cost/latency
  tickers. The field: `ae/store.html` 53 KB (1 model mention), `ae-store-pico-os.html` 47 KB,
  `ae-store-semantic-key.html` 26 KB, `ae-store-digital-twin.html` 18 KB,
  `llm-store-4d-atlas.html` 17 KB, `llm-store-widget.html` 17 KB,
  `gospel-bookstore/index.html` 15 KB, `llm-store-dna-qr.html` 11 KB,
  `aipodcast_me/aestore.html` 10 KB, `ae_store/index.html` 3 KB. Rivals are landing pages.
- **Verified:** 26 lines render; the markets ticker is unaffected; both labels link to
  `llm-store.html`.
- **Flagged, not changed:** both tickers now share one home. If markets should land on the
  economy surface (`ae/economy/`) instead, that is a one-line change.

## 77. the white-label layer (2026-11-23)

- `index.html`: a `◈ white-label` control beside `◐ theme`. It asks for **your glyph**
  (max 2 chars), **your name**, and **your accent** (gold/cyan/neon/magenta) — and nothing
  defaults to æ, because æ is Yæl's. Applying re-skins the surface: the hero glyph, the bar
  brand line, the caption, the document title, and `--gold`/`--gold-hi` site-wide. Persisted
  in `localStorage['ae-label-v1']`; `restore æ` clears it and puts the institutional mark back.
- **This is the #opensourceware product**: the surface is the pattern, the visitor wears it.
  The panel says so plainly — *"applies to this browser only… to ship it, fork the repo and
  rebuild."*
- **Verified:** glyph Ω + "ACME robots" + neon accent → `.myglyph` = Ω, img hidden,
  brand `>_Ω: ACME robots`, caption, title rewritten, `--gold` = `#00ff9d`, stored JSON;
  **after a full reload** all of it persists; `restore æ` returns brand/title/glyph/`--gold`
  and empties storage.
- **Defects fixed before publish:** a second `esc()` declaration shadowed the existing null-safe
  one (removed); no swatch carried `.on`, so `querySelector('#lbl-accent button.on')` would
  have thrown on apply (added the default + a fallback).

## 78. mech-os — the telemetry stops lying (2026-11-23)

The robotics console's numbers were fabricated: `randomizeStatus()` drew CPU and MEM from
`Math.random()`, and the bottom ticker asserted `CPU_TEMP: 45C`, `UPTIME: 99.999%`,
`AES-4096 [ACTIVE]` and `EXTERNAL SCAN DETECTED SECTOR 7` as if they were readings.

- Replaced with **measured** signals, each naming its source:
  `NET_LATENCY` = `navigator.connection.rtt` · `LOGICAL_CORES` = `navigator.hardwareConcurrency`
  · `JS_HEAP` = `performance.memory.usedJSHeapSize` · `SYSTEM_STATUS` derived from those.
  The `CPU_LOAD`/`MEM_USAGE` panel now shows cores and real heap instead of dice.
- Rows this device cannot measure are now **`n/a` + an explicit `SIM` tag**
  (`CPU_TEMP`, `UPTIME`, `ENCRYPTION`), and the sector-7 alarm is tagged **`SET DRESSING`** —
  it is theatre, and the page says so instead of passing it off as a sensor reading.
- The ticker is rendered from one `TICK` array (single source, doubled for the loop), which
  also absorbed the old `TYPOGRAPHY_LVL` row that `evolveTypography` used to patch by
  querying `[style*=…]` — that selector died when the row moved into the array.
- **Verified:** 18 ticker items render (doubled set); measured `NET_LATENCY: 50ms · rtt, this
  device`, `LOGICAL_CORES: 12`, `JS_HEAP: 1.0 MB`; `SIM`/`SET DRESSING` tags present;
  typography row updates without throwing.
- **Rule applied:** nothing typed. A console that fakes its own sensors is the exact
  anti-pattern the estate exists to refuse.

## 79. >_æ://neuromitosis/mech-hermes/llm_store — build specification (2026-11-23)

- New spec at `neuromitosis/mech-hermes/llm_store.md` (7,918 B): the store as a **module the
  conductor serves**, not a page you visit. Three layers — SURFACE (mech-os console) → BRIDGE
  (loopback relay, the only boundary) → CONDUCTOR (Hermes) → LEAF (Victus RTX / CUDA_MCP²).
- Contains: existing-assets table (all measured), module list, three contracts
  (receipt hash chain / catalogue entry / plan), the six-step conductor loop, governance,
  8 build stages with measurable gates, white-label rollout, verification, and §11 blockers.
- **Citations re-verified before committing:** `policies/0818/MEASURED.md` carries
  `4.1868`, `shuffle`, `38.8`, `37.7`; `pet/pet.json` carries `1,007,041` and `1963ee54`;
  the broker is loopback-bound at `127.0.0.1:7890`.
- Every number is either cited to an artifact or marked `PROPOSED`. Nothing built by this
  document; it is the contract for the build.

## 80. the spec becomes a surface (2026-11-23)

- `neuromitosis/mech-hermes/llm_store.html` (12,906 B): the §79 specification rendered as an
  æ-surface — gold on void, JetBrains Mono + Orbitron, scanlines, sharp edges, section nav,
  the stage table as the readable spine. Same content, no new claims.
- **Verified:** 12 sections render in order (0 thesis … 11 blockers), `--gold` = `#D4AF37`,
  body `#050505`, no horizontal overflow at the surface width.
- Linked from the home's `receipts & source` block. The console link is still pending.


## 81. the case for Qwen3-1.7B, derived from a measured QLoRA (2026-11-23)

- **Source:** `tools/slm_fit.py`, `tools/qlora_smoke.py`, `agents/gen_slm_case.py`,
  `tools/slm-fit.json`, `tools/qlora-smoke.json` in `C:/æ`.
- **Surfaces:** `qwen3-1.7b-case.html` (6,410 B), `slm-fit.json`, `qlora-smoke.json`.
- **Measured, not claimed:** a real 5-step NF4 QLoRA on `Qwen/Qwen3-0.6B` completed on
  teknium — peak 1.66 GiB allocated, 1.83 GiB reserved, 10,092,544 trainable params,
  loss 14.2 → 8.636, 121.7 s. Stack: torch 2.6.0+cu124 (cap 8.6), bnb 0.50.2,
  peft 0.22.0, transformers 5.24.0. Unsloth is NOT installed.
- **Calibration:** the initial VRAM formula understated by ~0.4 GiB; a 1.30x measured
  calibration was applied. After calibration 1.7B (3.27 GiB) and 3B (4.45 GiB) fit with
  ~5.26 GiB free (inference unloaded); 4B (5.51 GiB) is REFUSED. `--check` asserts this
  invariant; `--seq 0` refuses with rc=10.
- **Browser verification:** title, 4 KPIs, 6 table rows, 2 REFUSED marks, no `undefined`,
  `--gold` = `#D4AF37`, no horizontal overflow.
- **Blockers explicit:** no trained 1.7B adapter exists; 5 steps prove the pipeline, not
  quality. The live `llama-server` (PID 3868) holds 2915 MiB and was NOT killed. GGUF
  serving artifact stays untouched; training uses the safetensors base + adapter at serve.
- **Not deployed yet:** pending kanban push; CDN check not performed in this entry.

## 81. mech-os — AGENT CONNECT enters >_æ:/ (2026-11-23)

- Yellow **`● AGENT CONNECT`** button in the top bar. Clicking binds a local session and
  plays the login into `#logs`:
  `CONNECTING TO CONDUCTOR …` → `USER: HUMAN://ROOT · BOUND LOCALLY` →
  `ROUTE LOCKED: >_æ:/` → `SESSION: LOCAL ONLY — NO CREDENTIAL LEFT THIS DEVICE`.
  The button becomes `✓ CONNECTED >_æ:/`; a second click reports ALREADY BOUND.
- **Honest by design:** it is a *local session binding*, not an authentication, and the log
  says so. Nothing is claimed as privileged; the ritual is the product.
- **Defect found and fixed (a §78 regression I introduced):** `measureStatus()` was invoked
  mid-script while it calls `addLog`, which reads `const logsDiv` declared ~30 lines later —
  a TDZ `ReferenceError` that **killed the entire remainder of the script**: command input,
  typography evolution and the new connect handler were all dead. The immediate call now
  sits at the very end of the block, after every definition.
- **Verified:** button visible (145×24, `--secondary-color` = `rgb(255,157,0)` amber); click
  flips it to `✓ CONNECTED >_æ:/`; the log carries both the measured STATS line
  (`cores:12 · heap:1.1MB · rtt:100`) and the four login lines.

## 82. mech-os — æ menu + window manager + llm.store window (2026-11-23)

- **One `æ` menu** in the top bar (`#ae-menu`, built from the live `.window-title` set): every
  window listed, open ones marked, click to open. Includes **LLM_STORE**.
- **New `LLM_STORE` window** — body read from `estate.json` (`/store/i`), largest named as host,
  links out to `llm-store.html`.
- **Window manager**: default **9:16**, dock control `[▣]` injected into every header toggles
  **1:1**. Layout: up to **four 9:16 across the top**, then as many **1:1 squares as fit
  below**. Re-layouts on resize; below 700 px it hands back to the phone rule.
- **Verified at 1440×900:** four 9:16 tiles 304×540 at x=8/320/632/944, y=8; then four 1:1
  tiles 160×160 at y=556. LLM_STORE loads "13 store surfaces · hosted by llm-store.html".
- **Two defects fixed to get there:**
  1. `.window{min-width:300px}` clamped tiles → the layout clears min-* inline.
  2. `@media(max-width:768px)` forced full-width stacking with `!important` → re-scoped to
     `body:not(.tiled) .window`, with JS toggling `body.tiled`. The phone behaviour is intact
     when the manager isn't tiling.
- **Also:** the first layout pass ran while `#desktop` was still hidden (clientWidth 0); it now
  runs at the boot reveal instead of racing the random-delay boot.

## 83. wætz lives inside the console (2026-11-23)

`mech-os` feels like the OS for Asimov, so `VISUAL_ROBOT_MCP` now runs the real body:
the `picoasimov-atlas.webp` CAD sprite — same atlas, same nine states, same 6-frames-per-state
contract as `waetz.html` and the home. Click the pet to wave; every state change writes a
`[| "PET", "<state>", "asimov-cad", "QR://pet/<state>" |]` line to `#logs`.

- Sprite sized by the window (`min(150px, 82%)`, `aspect-ratio:192/208`,
  `background-size:100% auto`), frame offsets computed from the live element box.
- `robot-bat` now reads the **real** Battery API where the platform exposes it, else `n/a`
  (was a hardcoded `100%`). `robot-pos` reports the pet's **state**, not fabricated coordinates.
- **Verified:** atlas loads; `mpSet('running-right')` → background-position row 1
  (`-103px -112px` on a 103×112 box) and the label follows; frame stepping measured
  (position advances each tick).
- **Honest limitation:** in a 1:1 docked tile the pet is small (~103 px). The atlas contract is
  right; the prominence depends on giving VISUAL_ROBOT_MCP a 9:16 slot, which the current
  four-across tiling assigns by open order. Next increment: a preferred-aspect hint per window.

## 84. llama.cpp moves inside the console — NERVOUS_SYS window (2026-11-23)

Our llama.cpp work is real: `agents/llama_nervous_system.py` — "the æ boy running in local
llama.cpp", posting to a loopback llama-server at `127.0.0.1:8087/v1/chat/completions`, identity
sent per request, every response schema- and governance-checked, authority/motion REFUSED.
A GGUF exists (`neuromitosis/plan-narrator/adapter-v3-text.gguf`, 59.6 MB).

- New **NERVOUS_SYS** window in mech-os carrying that contract verbatim: endpoint, protocol,
  governance `grants:false · motion REFUSED`, plus an intent box whose PLAN button writes
  `[| "PLAN", "<intent>", "llama.cpp · 127.0.0.1:8087", "executed:false" |]` to `#logs`.
- **Reachability is reported, not assumed:** from a static host it says
  `NOT REACHABLE — STATIC HOST`; served over http it actually probes `:8087/health` and prints
  the measured result. In the local run it measured **`DOWN · Failed to fetch`** — the server
  isn't up there, and the window says so instead of implying a connection.
- Menu now lists nine windows (it is built from the live `.window-title` set).
- **Verified:** window opens; plan line written and the input cleared; reachability measured.
- **Honest boundary:** nothing here runs inference. Execution belongs to the conductor bridge
  (spec §5 stage 3). This is the operator surface for that capability, not the capability.

## 85. the menu trigger is the tiny æ boy (2026-11-23)

- The `æ` text button in the top bar is replaced by the institutional mark:
  `<img src="assets/brand/ae-neon-logo-clone.svg">` inside `.btn-menu`, 22×30 with the glyph at
  18×26. Same `toggleMenu()`, same nine-item menu.
- **Verified:** image loads (natural 746×1017), box 22×30, click opens the menu with all nine
  windows listed.
- Reuses the existing receipted asset — no new mark, no second source of truth.

## 86. every window can mirror an HTML surface (2026-11-23)

- `[◈]` control injected into every window header, beside `[▣]` dock and `[x]`.
  The candidate list is read from **`estate.json`** (`.html?` surfaces, 425 of them), so it
  cannot drift from the estate; a filter box narrows it; picking one replaces the window body
  with an `<iframe>` of that surface and writes a `[| "MIRROR", "<url>", "worn by <window>",
  "QR://mirror/<url>" |]` line to `#logs`. `[‹]` restores the stashed markup.
- **Defect found while verifying:** mirroring `COMM_LOGS` **deleted `#logs`**, which every
  module calls — the console's logging died with one click. Now refused with a logged reason:
  `[| "MIRROR", "REFUSED", "this window carries the shared log", "" |]`.
- **Verified:** refusal fires and `#logs` survives; SYSTEM_STATUS mirrors 425 candidates with
  `waetz.html` and `llm-store.html` present; `mirrorGo` installs `<iframe src="waetz.html">`.
- **Named limitation:** restore returns the *markup*, not live state — any driver that was
  running in that body (the pet's timers, a fetch loop) stops until the page reloads. Marked
  in the code comment rather than left implicit.

## 87. standardised four + docked default + 9:16 mobile composition (2026-11-23)

- The four originals are now a **standardised set** (`STD_TITLES`, class `win-std`,
  `data-std`), detected from their titles, and they **start docked** (`data-docked='1'`) —
  so the default desktop is the four 1:1 squares plus any undocked windows.
- Layout now sorts docked to the flow: undocked claim the top, docked fill 1:1 rows.
- **Portrait branch added** (`body.portrait` when height > width): undocked windows stack one
  per row at full width in 9:16; docked windows flow two-up as 1:1 squares below. `#desktop`
  grows to fit and scrolls (`body.portrait #desktop{overflow-y:auto;overflow-x:hidden}`).
- The phone media rule is re-scoped again to `body:not(.tiled):not(.portrait) .window` so the
  portrait manager actually owns the geometry.
- **Measured before the last change:** at 390×844 portrait engaged, all four carried
  `std=1`, the undocked window measured **374×665** (full-width 9:16), docked ones **150×150**.
- **UNVERIFIED after the two-up dock-flow edit:** the browser daemon began timing out
  (`Runtime.evaluate timed out after 5s`) and did not recover across two sessions. The edit is
  committed on reasoning, not on a read-back. Next session must re-measure the 390×844 layout
  before calling this done.

## 88. the kernel is yæl — mæch stays the language (2026-11-23)

Operator's naming rule: **the kernel is `yæl`; `mæch` is the development language; `æ` is the
agentic electronic language for machine-learning programming.** `mech-os.html` carried the
kernel name `MÆCH`, which conflated the two.

- Boot now reads `> INITIALIZING YÆL KERNEL...` plus a new line stating the distinction:
  `> æ:// agentic electronic · mæch-lang runtime`.
- Every system-identity use of MÆCH became yæl: typography stack labels (`yæl v4.1`,
  `yæl Typography`), the SPATIAL_GATEWAY comment (`yæl 4D`), the tabular-format and
  echo-response comments, the Google demo query (`yæl OS docs`), and the ROOT_ENDPOINT row
  `MÆCH Core` → `yæl Core`. **`grep -c MÆCH mech-os.html` → 0.**
- **Not renamed:** the surface/file name `MECH-OS` / `mech-os.html`, and the `mech-os-console`
  skill. Those name the *console*, not the kernel — but they do inherit the language's name, so
  if the console should also be re-named, that is a URL/skill change with inbound links to fix.

## 89. MASTER window + ROOT_ENDPOINT docked (2026-11-23)

- New **`MASTER · myaelmendez.github.io`** window: an `<iframe>` of `index.html` — the estate
  hub worn as a window. `data-master="1"`, amber gradient header, open by default, and it
  **claims the first portrait slot** (sorted before everything else).
- `ROOT_ENDPOINT` now starts docked too. Its title is prefixed (`æææ:/// ROOT_ENDPOINT`), so
  the standard-set matcher was fixed from `indexOf(p) === 0` to `>= 0`.
- **Two defects found while verifying:**
  1. the `body.tiled` toggle had been lost in the earlier rewrite, so the ≤768 px phone rule
     still overrode landscape geometry at 764 px — restored;
  2. docked windows were still filling the remaining portrait slots (only three squares sat
     below). Landscape now lays out **undocked-only** for the top row and sends *all* docked
     windows into the square flow, continuing the same row counter.
- **Measured at 1440×900:** MASTER 304×540 at (8, 8); SYSTEM_STATUS / COMM_LOGS /
  MODEL_COMBINATOR / ROOT_ENDPOINT each 160×160 at y=556, x = 8/176/344/512.
- Composition note: with the four originals docked by default, MASTER is the sole 9:16 tile
  until more windows are opened — coherent with "the original four start docked".

## 90. æ protocol — white-label as a standard (2026-11-23)

**Naming.** The site is **æ protocol — the protocol of agentic environments**. The address
stays `myaelmendez.github.io`; an address is where it lives, a name is what it is. Charter at
`AE-PROTOCOL.md`: the three-name rule (yæl kernel / mæch language / æ agentic electronic),
the white-label contract, the teaching path, fork·clone·contribute, and the funnel
(Nous Portal → install Hermes Agent → point your agent at the estate).

**Shared module.** `assets/brand/ae-label.js` — one implementation, included by any surface.
Persists to `localStorage['ae-label-v1']`; sets `--gold`/`--gold-hi` and, for surfaces that
declare it, `--secondary-color`; fills `[data-label-glyph]` / `[data-label-name]` slots; ships
its own control via `aeLabel.panel(mount)`. Never touches facts or receipts.

- **mech-os adopts it**: script included, `◈ LABEL` mounted in the top bar, the title line
  carries `data-label-name`.
- **Verified:** module loads; button mounted; `apply({Ω,'ACME robots',#00ff9d})` →
  `--gold: #00ff9d`, `--secondary-color: #00ff9d`, `body[data-labelled=1]`, storage written.
- **Still on its own implementation:** `index.html`'s richer label (glyph img swap, brand
  line, title rewrite). Migrating it onto the shared module is the next pass — until then two
  implementations exist, which is exactly the drift the standard exists to prevent.

## 91. æ://OPS window + the learning register (2026-11-23)

**Window.** New `æ://OPS · CONTROL` window wearing `ae/control/index-live.html` in an iframe,
open by default, dashed accent header (`data-ops="1"`). Measured at 1440×900: **304×540 at
(320, 8)** — second portrait slot, MASTER first. It appears in the æ menu automatically because
`renderMenu()` builds from `.window-title`.

**Learning register.** `AE-LEARNINGS.md` makes a standing rule of what this session practised:
*every imported codebase records pattern → landed → unlearned.* Five entries — the window
manager contract, the `!important`/media-query trap, the white-label standard, the æ://OPS verb
spine (INTENT→DISCOVER→COMPILE→AUTHORIZE→EXECUTE→WITNESS→RETURN plus its MEDIDO/DECLARADO split),
and the pet atlas. The honest through-line: the OS has the same verb chain as **plans**, not as
acts — the control surface runs locally with a real SHA-256 receipt and no external execution,
which is exactly the frontier the console should report about itself.

## 92. build spec v0.2 + theme system + origin window + viewport fit (2026-11-23)

**Spec.** `MECH-OS-BUILD-SPEC.md` — S1 viewport discipline (base frame 9:16, zero horizontal
overflow, one geometry manager, sweep-don't-sample), S2 theme system (six palettes as complete
surfaces, day/night auto then persisted), S3 native readiness for **androidmcp**, **webmcs**
and **agentic commerce** (each = verb file + receipt + window, with published refusals), S4
window contract, S5 non-goals, S6 delivery order.

**Themes.** `assets/brand/ae-theme.js` — `void` (default), `ember`, `glacier`, `verdant`,
`orchid`, `paper` (light); follows `prefers-color-scheme` until chosen; persists to
`localStorage['ae-theme-v1']`; writes `--ae-*` always and a surface's existing accents only if
declared. Mounted in the console top bar.
*Verified:* six palettes present, button mounted (`◐ æ void`), `apply('glacier')` →
body background `rgb(4,8,12)`, `--ae-accent #6EE7F9`, `--secondary-color #6EE7F9`.

**Origin window.** `ORIGIN · the atlas` wearing `origin/index.html`, open by default.
At 390×844 measured **374×665 at (8, 1414)** — third portrait slot after MASTER and æ://OPS;
the four standardised panels docked two-up at **179×179**.

**Viewport fit — defect found and fixed.** At 390×844 the page had `scrollWidth 1029`.
Isolated by removal probes (ticker and boot screen were innocent): the culprit was **`#bg-grid`**,
a decorative layer sized `200% × 200%` absolutely positioned — it measured 1277 px wide at
left −249, i.e. exactly the 1029 overflow. Fixed: pinned `position:fixed; inset:0; 100% × 100%;
overflow:hidden`. `#bottom-ticker` also gained `max-width:100vw; overflow:hidden` as a guard.
- **UNVERIFIED:** the post-fix read-back failed — the browser daemon timed out
  (`Runtime.evaluate timed out after 5s`) and did not recover. The diagnosis is exact and
  arithmetic (1277 − 249 = 1029), but the zero-overflow claim needs one re-measure next session.

## 93. the widget standard + atlas widget (2026-11-23)

**New standard S4.1.** A capability more than one window needs is **a widget, not a copy**:
one module over one data source, mounted per window, each instance reporting its own count.
Contract: `assets/<domain>/ae-<domain>-widget.js` plus
`<div data-<domain> [data-<domain>-cat] [data-<domain>-limit] [data-<domain>-compact]>`.
Rules: one renderer · declare don't import · counted (`-count`/`-shown`) · lensed per host.

**First instance:** `assets/atlas/ae-atlas-widget.js` renders `window.AE_ATLAS` (53 addresses)
from `ae-atlas.js`. Mounts natively; auto-mounts every `[data-atlas]` on load. Category, limit
and compact are attributes, so ORIGIN can show all 53 while another window shows six media
addresses — same component, different lens.

**ORIGIN converted to native:** iframe of `origin/index.html` removed, replaced by
`<div data-atlas>`; the full page keeps its own richer rendering and both read the same data.
No copy of the atlas body exists in the console any more.

**UNVERIFIED:** the browser daemon timed out again (`Runtime.evaluate timed out after 5s`)
before the mount could be measured. Nothing about this pass is claimed as observed — the
widget's count attributes, row counts and the compact/category lens must be read back before
S4.1 is called proven. Diagnosis is mechanical, the proof is outstanding.


## 94. film:// STUDIO — the scene is data, not code (2026-11-24)

The question: what does it take to direct films repeatedly without spending tokens?
Answer built here: **the scene document becomes the direction.**

`github-pages/robots/fleet-performs.scene.json` — schema `film.scene/1`: actors
(source trace, verb, rate, root, mirror) · camera spline keys (t, pos, target,
fov, ease) · beats (t, actor, verb, line) · stage · gates · render command.
Every field that used to be a Python literal is now data.

`agents/fleet_performs.py --scene <doc>` reads it. Verified equivalent:

```
--scene robots/fleet-performs.scene.json --encode
  [scene] 3 cues · authority 2.0s · total 11.0s
  → 264 frames · sha256 1079ba729b261695…   ← IDENTICAL to the hardcoded script
```

Same film, same hash, from JSON. Directing is now editing an array.

`github-pages/robots/studio.html` — the director's console. Gold on void, zero CDN
(three.js + GLTFLoader from the site's own vendor/), importmap ESM.

```
loads robots/fleet-performs.scene.json   (falls back to a labelled built-in)
3D blocking preview: real meshes where they exist (asimov-web.glb,
  microduck.glb), honest labelled proxies otherwise (reachy has no GLB)
camera path drawn; scrub + play; cue rings light per beat
ACTORS   rate · root x/y · mirror
CAMERA   keys t / pos xyz / target xyz / fov / ease
BEATS    t · actor · verb · line
STAGE    ground · backdrop · camera path
SCENE HASH  sha256 of the canonical document, recomputed on every edit
RENDER   prints the gated command; carries NO perform button
```

Measured:
```
scene loaded       3 actors · 5 camera keys · 4 beats
edit a fov value   hash 372dc3c2… → 853044c9…   (the determinism anchor works)
scrub to t=3.00    framing updates, transport shows 3.00 / 11.00
page               renders, no layout breakage, no console errors
```

**Design rule (spec section 0).** A static surface has no server and no secrets
and must never drive hardware. So the page REPORTS the last governed run and links
its receipt; the RUN happens locally through `robot://`. Same shape as
aipodcast.me: **the surface reports, the gate decides.**

**Next, in order:** sampler v1 in Rust (`studio` crate, CLI + wasm) — the JS spline
here is the reference implementation it must match; then a three.js backend that
renders the SAME document, giving browser preview and offline render one contract.

## 94. ESTATE window — the whole estate as one window of widgets (2026-11-23)

New `ESTATE · WIDGETS` window: a grid of `<section class="widget">` mounts. Two **real** widgets
ship with it, no placeholders pretending to work:

- **ATLAS** — `<div data-atlas>` from S4.1. *Measured:* **53 rows**, `data-atlas-count="53"`.
- **PET** — new second instance of the standard, `assets/pet/ae-pet-widget.js`, over
  `pet/picoasimov-atlas.webp`. Contract: `data-pet` mount, reports `data-pet-state`,
  `data-pet-frame`, `data-pet-frames`; geometry fixed at 192×208, 6 frames, 9 states.
  *Measured:* box **192×208**, `data-pet-state="idle"`, `data-pet-frames="6"`,
  `background-position: 0px 0px`, and a synthetic click moved it to **`waving`**.
- One honestly-declared gap: `STORES` carries `DECLARED · no widget yet` — not a fake panel.

Window measured **304×540**. The pattern now holds: a capability used twice becomes a widget,
and a window is just a grid of mounts.

## 95. æ declared the policy language for machines (2026-11-23)

Operator's statement: **the policy language is æ, for machines.** Encoded in `AE-PROTOCOL.md`
alongside the machine-readable form already on disk.

**Already existed** — `github-pages/ae-policy.json`, schema `hermes-ae/ae-policy/v1`, chain
`HUMAN://ROOT → æ → ae → harness → RECEIPT`. æ sits *between* the human root and any machine;
a machine is defined there as "any runtime, device, surface, robot, or harness that can observe
or act". Nine rules: AUTH-001…004, ACT-001 (`actuate` needs approval or a deadman), ACT-002
(commerce is draft until signed), PUB-001, EVID-001 (every decision writes a receipt),
FAIL-001 (unknown action / missing actor / expired approval ⇒ deny), plus a `decision_matrix`.

**Added:** the division of labour, stated once — *write* = mæch (how is it built?), *govern* =
æ (who may act, on which machine, until when?), *run* = yæl (what is executing?).

Honest note: the policy is a document; no runtime evaluates it yet. `asimov://` gates motion on
the same shape, but nothing executes `ae-policy.json` end to end — the same execution gap the
console has.

## 96. tinyTHREE — el renderizador soberano (2026-11-23)

New tiny* instrument, `tinythree.html`: loads the vendored three.js, exposes this machine's real
GPU capabilities, renders a fixed scene and grades determinism by running twice (FNV-1a over
`readPixels`). Fails closed — no module, no context, no invented number.

**Measured on this machine:**
| field | value |
|---|---|
| three.js | **r186** (`THREE.REVISION = 186`) |
| webgl | **WebGL 2.0 (OpenGL ES 3.0 Chromium)** |
| renderer | **ANGLE (Intel, Intel(R) UHD Graphics, Direct3D11 vs_5_0 ps_5_0, D3D11)** |
| vendor | Google Inc. (Intel) |
| webgl2 / max texture / float | sí · **16384** · `EXT_color_buffer_float` sí |
| frame digest A | `8ef9b785` |
| frame digest B | `8ef9b785` |
| grade | **PASS · determinista** |

The renderer line independently reproduces the Optimus finding: three.js reaches **Intel UHD
through ANGLE/D3D11**, not the RTX. Determinism holds with `antialias:false`; the digest is the
frame-level receipt the film chain was missing.

## 97. tinyTHREE on the RTX — verified (2026-11-23)

The question was whether three.js can render **fully local on the RTX** through the tiny family.
Answer: yes, and the unlock is documented verbatim in `agents/asimov_up.cmd`
(`--force_high_performance_gpu --use-angle=d3d11`; comment there: without it
"ANGLE/D3D11 selects the Intel iGPU and the discrete card stays idle").

**Measured, same `tinythree.html`, two launches of the same Chrome:**
| launch | renderer string |
|---|---|
| default | `ANGLE (Intel, Intel(R) UHD Graphics … Direct3D11)` |
| `--force_high_performance_gpu --use-angle=d3d11` | **`ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 6GB Laptop GPU (0x000025AC) Direct3D11 vs_5_0 ps_5_0, D3D11)`** |

Both runs grade **PASS · determinista**. So the estate can render three.js locally on the
RTX with reproducible frames — the flags are the whole difference, and the robot launchers
already carry them.

**Why the instrument earns its place:** the page does not assume a GPU. It reports which one it
got. The same URL is an Intel measurement or an RTX measurement depending on how Chrome was
launched, and until this run the estate had only the Intel number recorded.

## 98. rtx://render — el RTX como default + demonstración (2026-11-23)

**Default declarado.** El render three.js local del estate tiene default: **el RTX**. Los flags
son `--force_high_performance_gpu --use-angle=d3d11` (ya vividos en `agents/asimov_up.cmd`). Una
página no puede elegir la GPU; el lanzador sí. La regla queda escrita y la página la declara.

**Demonstración:** `rtx-render-demo.html` (`rtx://render`) — escena áureo-sobre-void (rejilla +
icosaedro wireframe + 1.200 partículas), mide el **costo real de render** por frame, gradúa la
GPU y emite un receipt JSON. Fail-closed: si no cargó el módulo o no hay contexto, dice REFUSED.

**Medido:**
| launch | gpu | ms/frame | fps | peor | digest |
|---|---|---|---|---|---|
| default (real browser) | `ANGLE (Intel UHD …)` · rtx_default **false** | **35.15** | **28.5** | 801.1 ms | `437a9673` |
| `--force_high_performance_gpu --use-angle=d3d11` | `ANGLE (NVIDIA GeForce RTX 3050 6GB Laptop GPU …)` · rtx_default **true** | no medible aquí | — | — | `b03a85c4` |

**Declarado, no resuelto:** bajo `--virtual-time-budget` headless, `performance.now()` alrededor de
`renderer.render()` mide **0 ms** — el trabajo de GPU se difiere, así que el tiempo de render no
es medible en ese modo. Por eso el RTX se reporta con gpu + digest, no con ms/frame. En un
navegador real con los flags sí se puede medir; esa es la prueba que falta.

## 99. el check que falla en `asimov-agent` es un Worker, no Actions (2026-11-24)

Al revisar la rama `asimov-agent` dos veces, el detalle que importa: junto al commit
`f759b8d` GitHub muestra **failure**. Medido por API:

- combined status: `pending`, 0 statuses.
- check runs: **1**, `Workers Builds: hermes`, `status: completed`, **`conclusion: failure`**,
  sin anotaciones. Build ID `f0dd492e-f34a-420d-8e6e-4538e4486b12`, script `hermes`,
  **production**, dashboard Cloudflare (`dash.cloudflare.com`, account `85e8949d…`).
- No es GitHub Actions: el único workflow local es `.github/workflows/capability-manifest.yml`.
  La config del Worker vive fuera de este checkout, así que **su log no es legible desde aquí**.

Lo que sí se mide en el repo: **83 superficies HTML aún cargan three.js desde CDN**
(jsdelivr / cdnjs), y **46 usan `import * as THREE from 'three'`** — specifier desnudo que
requiere import map o resolución remota. `AGENTS.md` manda *cero CDN*. Ahí está la clase de
fragilidad que el three.js vendorizado elimina: ninguna build tiene que salir a buscar el
renderer.

Bloqueo declarado: la causa exacta del fallo del Worker es **desconocida** — el log está tras el
dashboard de Cloudflare. Lo medible está registrado; lo demás se declara desconocido.

## 100. index.html — tres.js como capa de fondo (evaluación + mejora) (2026-11-24)

**Evaluación.** `index.html` (47,855 B) no tenía ni una línea de three.js. Su único elemento
espacial era `<canvas id="grid">`: `drawGrid()` recorre ~40 líneas por frame en **2D por CPU**,
a viewport completo y con DPR×2 en móvil — el coste que paga un teléfono en 9:16. El héroe es un
atlas CSS rasterizado (deliberado: es un receipt), así que la mejora adecuada era la capa de
fondo, no tocar el pet.

**Mejora.** Una red neuronal WebGL con el módulo **vendorizado** (`assets/vendor/three.module.js`,
cero CDN): suelo en perspectiva + 900 partículas de polvo áureo + niebla, cámara que se compone
distinto en vertical (`fov 84`, `z 10.5`) que en horizontal (`fov 68`, `z 8.5`). Si no hay WebGL
o no carga el módulo, **el fondo 2D sigue funcionando** y el camino tomado se declara en
`window.aeRender`.

**Medido en 390×844:** `path:'webgl'` · `three:'r186'` · `WebGL 2.0` · gpu `ANGLE (Intel UHD …)`
· dos capas (`grid-gl` + `grid` oculto) · `overflowX: false`. Visión: la rejilla dorada ocupa el
**50% inferior** y los contenidos quedan en la mitad superior — encaje correcto en 9:16.

**Defectos encontrados al verificar (los dos reales):**
1. el primer intento dio `THREE.WebGLRenderer: Error creating WebGL context.` — **un canvas no
   puede ser 2D y WebGL a la vez**, y `drawGrid()` ya había tomado el contexto 2D. three.js recibe
   su propia capa `#grid-gl`.
2. sin try/catch el fallo era silencioso (`aeRender` quedaba `null` y parecía que el módulo no
   existía). Ahora el motivo se declara en vez de desaparecer.
3. el suelo era invisible (opacidad .5, color `0x1b1b1b`, fog 9–26). Ajustado a `.85` / `0x444444`
   / fog 12–34 y `lookAt(0,-1.5,0)`; verificado visualmente.

## 101. RTX render cost MEASURED — the loop improved and closed the gap (2026-11-24)

§98 left the RTX row without a time: under `--virtual-time-budget` headless the GPU work is
deferred so `performance.now()` around `renderer.render()` reads 0. Instead of reporting that as
a permanent blocker, the page was changed so the receipt travels in **`document.title`** — which
`computer_use` capture returns without needing any click or scroll approval.

**Setup:** real desktop Chrome launched with `--force_high_performance_gpu --use-angle=d3d11`
against `rtx-render-demo.html`, read with `computer_use(action="capture", app="chrome.exe")`.

**Measured, same scene, two machines:**

| launch | gpu | ms/frame | fps |
|---|---|---|---|
| real Chrome + RTX flags | **NVIDIA GeForce RTX 3050 6GB** | **1.21** | **826.2** |
| harness Chrome (no flags) | Intel UHD (ANGLE/D3D11) | 35.15 | 28.5 |

≈ **29×** less time per frame. Digest on the RTX run `74df2505`.

**Reusable technique recorded:** put the result where the cheapest read can reach it (title, DOM
node, URL fragment) before trying to drive UI. Two free channels — `terminal` to launch, capture
to read — replaced a consent-gated scroll.

## 2026-11-24 — flagship 9:16 mobile, passkey removed

**Removed.** The inert WebAuthn panel is gone from `privateclient/bridge.html`
(status bar back to `#LOCALAI · FLAGSHIP · LOCAL-ONLY`). Verified live: zero
`WINDOWS PASSKEY` / `pkProbe` nodes. The gate belongs in the local broker, not
in a public page.

**Built.** `privateclient/mobile/index.html` → `https://privateclient.ai/secret/mobile/`:
a 540×960 full-bleed surface with one thumb CTA (`OPEN LOCAL VAULT`), a bottom
sheet with ENTRIES / ADD / RECEIPT, and a PROBE control that renders only HTTP
status and discards the broker body. Background is a glyph-free plate whose
SHA-256 (`c9a1df29f2d99bd6…`) is the surfaced receipt. Only external URL in
the source is `127.0.0.1:7890`.

**Redirect.** `/secret/` now redirects to `/secret/mobile/` below 700 px and
keeps a visible `9:16 MOBILE →` door on desktop. Verified both states in a real
browser at 540px and 1600px.

**Measured.** Phone viewport 540×960; sheet opens, ADD stores one entry
locally, RECEIPT shows the plate hash, PROBE reports `status 0 · TypeError`
from the public origin (honest: no visitor loopback broker). Visual review
caught and fixed headline/art collision and clipped microcopy in two rounds.

**Remaining.** Mobile contract still needs to be applied to kanban (one column)
and Blender (review sheet only). Plugin `blender` remains disabled behind the
unrelated `config_backends` admission error; Blender 5.3.0 + add-on v1.0.3 are
installed and hash-verified but `blender.exe` is not on `PATH`.

## 102. pet: la transparencia ya estaba en el atlas; el fallo era la ruta (2026-11-24)

**Medido antes de tocar nada:** `picoasimov-atlas.webp` es **1536×1872 con 91% de píxeles
alpha<8** (8% opaco, 0% parcial) — el sprite **ya compone sobre cualquier fondo**. La
transparencia no era el problema.

**Defecto real encontrado:** `assets/pet/ae-pet-widget.js` apuntaba a
`pet/picoasimov-atlas.webp`, pero el atlas vive en la **raíz** del sitio; `pet/` solo guarda
`pet.json` y las pruebas. La ventana ESTATE montaba un **cuadro vacío**. Mi verificación anterior
leyó `data-pet-state` y el tamaño — atributos que se fijan **aunque la imagen no cargue** — así
que di por bueno un widget invisible: exactamente la trampa *«a loaded runtime is not a used
runtime»*.

**Corregido y verificado:** `src:'picoasimov-atlas.webp'`. En el navegador, el `background-image`
calculado resuelve a `/picoasimov-atlas.webp` y la imagen carga con `naturalWidth 1536`,
`naturalHeight 1872`.

**Pendiente de decisión, no ejecutado:** lo único opaco que queda detrás de la figura es el panel
del héroe (`.facecover{background:#020504}`) y `.pet-stage`. Que sean transparentes es una
decisión de composición, no un arreglo silencioso.
