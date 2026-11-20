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
or a simulation. The integrated mobile preview reported no document overflow,
but physical mobile and live GitHub Pages behavior are separate verification
states. Live endpoint evidence is recorded only after the actual deployment
response is observed.
