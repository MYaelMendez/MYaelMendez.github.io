# Emoji plugin website · publication verification

**Status:** Review-only; PR #19 is draft and must not be merged for publication until the checks below are satisfied.

## Scope
🔍 Search, 📋 Capture, 🏎️ Motorsports, 📺 Television. The pages are factual draft descriptions of skills-only plugins; they are not an installed runtime, publisher attestation or legal approval.

## Canonical paths
- Directory: `/emoji-plugins/` (served from `emoji-plugins/index.html`). Removed redundant `/emoji-plugins/index/` source page.
- Landing pages: `/emoji-plugins/search/`, `/capture/`, `/motorsports/`, `/television/`.
- Notices: `/emoji-plugins/support/`, `/privacy/`, `/terms/`.

## Hosting and data handling · unresolved
A Cloudflare Workers build failure was reported on the draft PR, but neither that check nor the GitHub Pages repository name proves which service will serve production requests. GitHub's commit-status API reported no status contexts at the previously inspected revision; that endpoint does not enumerate all external provider checks. No Cloudflare deployment configuration or request/log retention settings have been confirmed.

Before legal approval, use the actual deployment provider dashboard to confirm the publishing host, routing, access/error logging, analytics, cookies, retention, subprocessors and user-facing contact/support route. Record evidence and update the draft privacy disclosure to match. Do not infer privacy guarantees or provider logging practices from a hostname, a build check, or these static files.

## Verification gates
- [ ] Diagnose the Cloudflare Workers failure using the provider build deployment log; document the failing command and environment.
- [ ] Confirm intended production host (GitHub Pages, Cloudflare, or other), source branch, build path and deployment trigger.
- [ ] Confirm actual data handling and legally review privacy and terms.
- [ ] Browser test unauthenticated HTTPS responses for all eight pages; confirm canonical URL and accessible navigation on mobile, desktop and keyboard.
- [ ] Verify full response body, not HTTP status alone; capture retrieval date and a source commit.
- [ ] Confirm publisher identity, rights, countries, commerce, listing category and icon legibility.
- [ ] Only then enter checked website/support/privacy/terms URLs in llm.store publication overlays and `verified_urls`.
- [ ] Run `python3 scripts/test_plugin_factory.py` and `python3 scripts/build_plugins.py` from the llm.store release branch, inspect ZIP receipts, and expect `--require-ready` to remain blocked until final portal review.

**Source verification is not browser verification. No merge, deployment, or submission is recorded by this document.**
