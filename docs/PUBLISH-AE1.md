# æ1 · Privacy-Safe Fork & Publish Plan

**Status:** Review-ready proposal — not deployed  
**Project:** #OpenSourceWare → #InternetOfAgents  
**Source:** [MYaelMendez/MYaelMendez.github.io](https://github.com/MYaelMendez/MYaelMendez.github.io)  
**Review branch:** `feat/mcp-virtual-micro` · [PR #15](https://github.com/MYaelMendez/MYaelMendez.github.io/pull/15)

## Purpose

A newcomer can **Fork → Configure → Preview → Verify → Publish → Own** a mobile-first æ1 environment. This document authorizes **no merge, deployment, domain changes, GitHub Actions dispatch, or account linking**. Public repository metadata must never be treated as an authorization grant.

## Release boundaries

- **Public:** static UI, example floor names, nonsecret manifest, schema, documentation, demo data, code and verified receipts that contain no private inputs.
- **Private by default:** personal profile, health, faith, family, finances, contact details, access tokens, device identifiers, conversation history, consent records and real agent outputs.
- **Excluded from the first release:** automatic tool execution, live MCP sessions, OAuth, cloud accounts, wallet/key custody, unverified æQR resolution and privileged GitHub Actions.
- **Honest labels:** `prototype`, `simulation`, `planned`, `verified` as appropriate. The æQR symbolic address is not a live HTTPS resolver.

## Repository and fork approach

1. Open the upstream source and read its license, security guidance and files. **Before inviting broad reuse, verify the repository has a suitable explicit open-source license**; a public repository alone is not a reuse license.
2. Click GitHub **Fork** and create a repository under the newcomer's own account. Do not create the fork for them without their approval.
3. Use the fork's **own** configuration: replace author name, domains, principal display labels, outbound links, and brand-specific references. Do not impersonate the original creator or claim official OpenAI/GitHub affiliation.
4. Keep a `gh-pages` branch only if compatible with the fork's GitHub Pages settings; otherwise select the actual source branch in Settings → Pages. GitHub Pages availability and repository-name URL rules depend on account and settings.
5. Keep an upstream remote and preserve fork lineage, with contribution via reviewed pull requests.

## Proposed release structure

```text
/                   public landing and human-first navigation
/ae/                9:16 æ1 tower UI (12 configurable floors)
/mcp/               optional virtual Micro control surface
/pico/              future minimal portable runtime (not yet implemented)
/spec/              human-readable æ1 / æQR contracts
/.ae/public.json     public, nonsecret environment profile (proposed)
/docs/PUBLISH-AE1.md this plan
```

No files under `pico/`, `spec/` or `.ae/` are claimed to exist by this proposal. Avoid copying private configuration into any GitHub Pages build path.

## Privacy-by-design profile

A starter profile should contain only `schema`, `id`, `version`, `kind`, `floor_labels`, `public_capabilities`, `fork_source`, `published_url` (after verification), and `permissions: {inherit:false, default:"deny"}`. Personal identity, private context and secrets belong in private storage or a separately authorized service, not Git history, browser query strings, a QR payload or a public manifest. Never rely on a `.gitignore` rule to remove secrets already committed.

## Deployment review checklist

- [ ] Confirm source license permits intended forking and redistribution; add license if missing and authorized.
- [ ] Inspect the source and history for embedded credentials, PII, analytics identifiers and unexpected remote scripts.
- [ ] Make demo data generic; all 12 life floors optional and user-customizable.
- [ ] Ensure mobile 9:16 usability, accessibility, reduced-motion support and keyboard navigation.
- [ ] Ensure `$mcp` handoffs are visibly **prompt handoffs**, not real agent execution.
- [ ] Validate manifest JSON, same-origin references and all relative links in a fork's project-site URL.
- [ ] Verify a preview build with no privileged GitHub Actions or secrets.
- [ ] Review diff and obtain human approval before merge.
- [ ] Enable GitHub Pages on the fork via Settings → Pages, selecting the verified branch/folder.
- [ ] Visit the published HTTPS URL and check browser console, navigation, manifest, and no sensitive content.
- [ ] Record the deployed revision, public URL, test results and limitations as a Witness receipt.
- [ ] Add custom domain/DNS only in a separate explicitly authorized change, after verifying domain ownership and TLS.

## Acceptance test

A newcomer can fork the repo, edit a nonsecret display name and floor labels, preview a static æ1 interface, publish it on their own GitHub Pages address, and verify the deployed revision **without connecting any accounts, copying secrets, or inheriting the author's permissions**.

**Next implementation slice:** create a neutral `.ae/public.json` template and a browser-rendered floor selector with explicit demo-mode labels, then test in a fork-like project URL. This plan itself is not evidence that the release has passed those checks.

**Invariant:** Context may propagate; authority does not.  
**Motto:** Many agents. One principal. 🫵
