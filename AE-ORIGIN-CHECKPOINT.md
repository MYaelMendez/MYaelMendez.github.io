# Origin -> public review / Open Sovereign checkpoint

Recorded 2026-10-19. Implementation scope: canonical GitHub homepage, its local
console, the optional read-only WebMCP adapter, and tests. Source baseline:
`151c6b3a4dd85fadace959cb85bd3028e28c765e` on `gh-pages`.

This supplements `AE-CONTINUITY.md`; it does not supersede the two-destination
architecture or transfer authority. The existing OpenAI Site remains a peer of
chat. No Site source or deployment was edited, and no replacement Site was made.

## User notation (preserved exactly by the resolver)

- Origin: `x0:y0:z0:æ:æ` (exact user notation).
- Public: `x0:y0:z:0:æ:æ:æ` (exact user notation).

The literal Unicode spellings are constants `origin` and `publicAddress` in
`ae-origin.js`. An extra colon in `z:0` is accepted deliberately. Neither this
notation nor the number of ligatures is a permission level or login credential.
The older numeric atlas coordinates remain supported separately, bounded to
x/y/z -999..999 and navigation layer 0..3.

## Implemented

- Fixed the root boot fault: the original theme setup called `$()` before the
  assigned helper existed. `origin-console.js` now uses a hoisted declaration.
- Kept the living face, coordinate display, atlas, legacy destinations, themes,
  ticker, announcements and motion; added keyboard-safe control handling,
  meaningful pause/reduced-motion behavior and readable mobile styling.
- Split inline scene/runtime into reviewable files. Command, ticker and atlas
  content use text nodes; unsafe destination schemes are rejected.
- The heart entry (`$❤️`) focuses human intention, not a
  health-only workflow. It does not update the installed Heart Care plugin.
- Local alias `æ`, `$ae`, `$mcp`, `&mcp`, compatibility `$mpc` / `&mpc`
  open one local origin. No automatic navigation and no platform registration.
- Human intention is tab-local. Only theme and executor preferences are saved
  locally. This is not secure storage: do not enter sensitive records.
- Public review exports only an allowlisted draft after review of its exact
  fields. Editing inputs invalidates approval. Intention, credentials, grants,
  private history, and provider success are not included.
- Codex is a selectable saved preference, not a connected runtime or new grant.
- The existing `ae-destinations.json` is now consumed by the homepage. Invalid or
  unavailable peer contract disables Site handoff and public export. Chat has
  no invented entry URL; cross-surface session synchronization is not claimed.
- `scan` and WebMCP `verify_chain` no longer fabricate a 10/10 success. Optional
  WebMCP tracks actual host-accepted registrations, handles errors, projects
  public descriptions only, and makes `open_surface` non-navigating.

## Tests and exact evidence limits

- 26 Node unit tests passed: resolver, coordinates, unsafe URLs, fail-closed peer
  contracts, public projection, unchanged authority under preference switching,
  the original boot error reproduction, and WebMCP registration/tool mocks.
- 55 offline Chromium DOM assertions passed at 360x640, 390x844 and 1440x900.
  Actual changed scripts ran, with explicitly stubbed fetch, storage and file
  download boundaries, using small public fixtures. Layout screenshots reviewed.
- The normal HTTP smoke test could NOT run in this environment: Chromium
  returned `ERR_BLOCKED_BY_ADMINISTRATOR` for navigation. No policy was changed.
  `tests/origin-browser.py` is supplied to run that test in an authorized browser.
- No live Safari/iPhone, authentication, external Site, provider iFrame, doola
  transaction, native WebMCP agent host or complete repository audit was tested.
- These checks are NOT a security certification or cryptographic attestation.

Run the self-contained checks from the repo root:

```sh
node --test tests/origin-public.test.cjs
python tests/origin-dom.py
```

The optional Python checks need Playwright and Chromium. The HTTP browser suite:

```sh
python tests/origin-browser.py --chromium /path/to/chromium
```

Test fixtures are not live atlas/manifest replacements. Do not deploy fixture
responses as production metadata. Evidence outputs are generated locally beside
this checkout. The accompanying local review bundle contains actual test output.

## Remaining release gates

1. Review the refreshed PR against the latest `gh-pages`; preserve intervening
   changes. No unrelated PR is approved by this checkpoint.
2. Run the HTTP browser suite with real public source files as an additional
   integration pass; test Safari/mobile behavior and actual destination loading.
3. Verify native WebMCP only in a supported, authorized host. Current draft uses
   `document.modelContext`; the compatibility navigator path is feature-detected.
4. OpenAI Site source changes require the existing Site editor/project access;
   current Studio preparation tools do not provide that capability.
5. Obtain explicit production release approval. A public draft export is not a
   GitHub commit, deployment, provider purchase, filing, or permission grant.

## Source references

- Existing project decisions: `AGENTS.md`, `AE-CONTINUITY.md`, `ae-destinations.json`.
- Original root and WebMCP implementation inspected at the source baseline above.
- WebMCP Draft Community Group Report, 2026-10-16:
  https://webmachinelearning.github.io/webmcp/ (checked 2026-10-19).
  Draft, not a W3C standard; host availability must be detected, not assumed.

**Context may propagate; authority does not. Return value to the human.**
