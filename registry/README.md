# æQR registry · skills → capabilities → kænbæn

`registry.json` is the canonical generated contract for navigation, capability
contexts, HTTPS QR destinations, and the sitemap. Generated outputs are not
edited by hand. Inputs are source HTML, `source-surfaces.json` (the retained legacy
catalog), `.well-known/skills/index.json`, `skill-guide/capability-mesh.json`,
`overrides.json`, and revision-bound `evidence/page-audit.json`.

The skill mesh contains **221 records**, including four names occurring in two
categories. IDs include the category to preserve those distinct records. The
eight primitive/skill/blueprint declarations are a separate catalog. Exact
reviewed bindings live in `overrides.json`; similar names do not establish that
a surface implements a skill. Default page classification is discovery/demo
until explicitly reviewed. Existing LLM.store knowledge/discovery and æ.store
execution/agency meanings are preserved.

## Contract

Every entry carries stable ID, canonical HTTPS URL, purpose (`yellow`, `blue`,
`green`), document type (`tool`, `demo`, `spec`, `embed`, `redirect`), dependencies,
authority requirements, source revision/hash or catalog reference, verification
date, and independent availability and functional statuses. `source.revision`
is the reconciliation base commit; page bytes are identified separately by
SHA-256. The generated artifacts must be committed together. The generator
records its own source path rather than a self-referential output hash.

- `available`: matching page bytes returned HTTP 200 in the recorded audit.
- `source_present`: a resource exists in source but was not checked live.
- `not_checked`: no applicable live evidence (including newly generated pages).
- `unavailable`: a declared resource is missing from source.
- Functional `blocked`: revision-matched audit evidence found a blocker.
- Functional `not_verified`: no successful execution proof. HTTP 200, a skill
  listing, a source indicator, or moving a board card cannot upgrade it.

Changed page bytes invalidate inherited verification automatically. Audit dates
are observation dates; generation does not stamp today's date as verification.
No record contains an execution grant. The legacy `surface-manifest.json`
projection keeps existing IDs/categories and external catalog links, exposes
full page coverage, and reports agent access as public read. The original
catalog's `agent_access` claims remain in `source-surfaces.json` for review.

## Generate and verify

```sh
python3 scripts/build_aeqr_registry.py
python3 -m unittest discover -s tests -p 'test_aeqr_registry.py'
node tests/aeqr-card-contract.cjs
node --check registry/registry.js
```

`registry/index.html` and `sitemap.xml` are generated from the same entries.
`index.template.html` is a template asset and deliberately omitted from discovery.
404 pages and explicitly classified embeds are not included in the sitemap.
The original landing page links to the generated catalog. The catalog also
contains literal anchors so page discovery does not depend on JavaScript.

## QR kænbæn

Context QR: `/registry/#entry/<stable-id>`.
Task QR: `/registry/#card/<UTF-8-base64url-snapshot>`.
Both are HTTPS URLs that open in standard scanners. Cards use version 1 with
`id`, `entry_id`, `title`, `purpose`, `stage`, and `notes`. Opening a snapshot
only displays it; saving a local copy requires a button click and a new ID.
Canonical capability URLs come from the registry, not user-supplied QR URLs.
The QR has an opaque white background and a four-module quiet zone. SVG
exports use the same payload. Progress is browser-local, with JSON export and
no cross-device synchronization.

Stages: audit → repair → verify → publish → audit. `publish` is a planning
column, not an automatic deployment. Classification/verification are not
changed by board progress. The physical `agents/qr_kanban.py` route-envelope
pipeline is documented but not invoked by this browser board; its Hermes,
camera, supervision and authorization requirements remain independent.

## Verification limits

The inherited audit checked 171 HTML documents, their source/live hashes,
literal HTML references, some literal JS routes and inline syntax. Browser
interactions, camera scans, visuals, DNS, external CDN/import/CSS dependency
closure, backend execution, and dynamic routes remain unverified. A repair
must be re-audited before it receives fresh evidence. This is the red loop:
**audit → repair → verify → publish → audit**.
