# Homepage migration · working glass and preserved origin

The old public homepage is retained at `origin/index.html` from source revision `7befaf5dafce517393261d5b4bb50f9b0e679cee`. Compatibility edits are enumerated in `origin/README.md`. Root assets and every pre-existing destination remain in place. `/origin/` is distinct from the still-unmerged `/origins/` animation proposal.

The replacement root index reuses the working local glass interface from ae-cockpit PR #4, commit `3969eea0d10e9c5b49c9f7fd78b466c04e816425`. Its `base` resolves shared assets from `work/`. The same workspace opens at `/work/`. Chat remains a peer operating destination; the original OpenAI Site is an optional link, not a compulsory redirect.

Implemented: one intent, selected brief, three workstreams (Build, Inspect, human Review), two deterministic text tools, revision-bound local approvals, expiry/revocation/cancellation, contribution tray and evidence export. No models, external agents, runtime sandboxing, authenticated identity, persistence or cross-host synchronization connected.

Checks: ten local tests passed. Browser verified the replacement root's local draft/receipt flow and followed its origin link. The archived atlas populated, help command worked and theme state changed. Preview lacked WebGL; the static fallback worked. Physical mobile/screen-reader tests remain pending. The old destination pages are retained, but were not all browser-tested by this migration.

API integration is not completed by this homepage change. Do not publish API keys in GitHub Pages. CI evidence is separate from local checks; inspect the resulting pull request's exact-head run. Existing homebase PRs #29/#30 also alter the root and need reconciliation with this replacement before merging.
