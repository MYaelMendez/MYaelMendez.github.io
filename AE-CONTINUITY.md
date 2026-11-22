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
