# æQR³ · Recursive Environment Baseline

**Status:** Adopted design baseline · v0.1 specification (not a deployed resolver or runtime)  
**Notation:** `æQR^æQR^æQR` / `æQR³`  
**Scope:** æ1 · æPICO · #OpenSourceWare → #InternetOfAgents  
**Principal:** `HUMAN://principal`

## Canonical rule

**Every environment may discover another environment. Every environment has verifiable lineage. No environment automatically inherits human authority.**

`æQR³` is the minimum *illustrative* three-layer composition, not a fixed maximum depth or a claim that a QR symbol contains executable code.

```text
HUMAN://principal
    |
    v
L1  æQR ROOT       -> public æ1 environment manifest
    |
    v
L2  æQR CHILD      -> portable æPICO environment manifest
    |
    v
L3  æQR CAPABILITY -> $go / 围棋 strategy module manifest
    |
    v
WITNESS -> HUMAN://principal
```

## Baseline manifest contract (proposed)

Each independently resolvable node should expose:

- `schema`, `id`, `version`, `kind`, `public_url`
- `parent_id` (null only for a root), `children` (public references)
- `capabilities` (descriptions and nonsecret contracts; not implied activation)
- `provenance` (source repository and immutable revision where available)
- `permissions: {inherit:false, default:"deny"}`
- `witness` with explicit evidence state: proposed / simulated / verified
- `locale` (e.g., `en`, `zh-Hans` for bilingual modules)

A real scan must resolve a valid HTTPS URL to a versioned manifest; `aeqr://` notation remains symbolic until a resolver is implemented and verified. The QR payload should contain only a public resolver URL or equivalent nonsecret reference. QR patterns themselves are not authentication, proof of provenance, or executable authorization.

## Required invariants

1. **Human principal remains authority root.** Every consequential operation needs a separately verified grant.
2. **Context may propagate; authority does not.** No inherited tokens, credentials, private profiles, consent, or account access.
3. **Forking creates independent ownership.** Fork lineage and source attribution persist; permissions do not.
4. **Bound recursion.** Detect parent/child cycles, enforce traversal depth and resource limits, and handle unreachable nodes.
5. **Public by design, private by default.** Do not embed personal or confidential data in public manifests, QR payloads, logs, or Git history.
6. **Witness is evidence, not a promise.** Label proposals, simulations and actual verified executions distinctly.
7. **Human-readable fallback.** The æQR tree must be navigable via ordinary links and ASCII-compatible aliases, without scanning or typing the ligature.
8. **Portable localization.** A module such as `$go` can supply `en` and `zh-Hans` without duplicating the authority model.

## Reference example

`æQR(ROOT:æ1) → æQR(CHILD:æPICO) → æQR(CAPABILITY:$go)`

`$go` has two proposed functions: guided entry into the environment, and Go/围棋-based strategic education for a one-person company. Go gameplay and legal-move intelligence are not yet implemented; the existing chat board is illustrative.

## First acceptance path

**Discover → Resolve → Inspect → Traverse → Fork → Configure → Preview → Publish → Verify.**

A reviewer should be able to traverse three public manifests, validate parent-child references, fork without inheriting authority, publish under their own URL, and independently check provenance and the deployed revision. Until the resolver and manifests are built and tested, this is a specification only.

## Relationship to existing records

- `mcp/AEQR.md` — parent RFC and æ1 power-tower amendment.
- `mcp/manifest.json` — current prototype manifest; not yet this full recursive contract.
- `docs/PUBLISH-AE1.md` — privacy-safe fork and publication plan.
- `mcp/index.html` — virtual Micro interface prototype.

**Baseline motto:** Many environments. One principal. 🫵
