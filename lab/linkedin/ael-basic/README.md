# æl.net · Prompt-BÆSIC MCP64 v1

A fixed 300×500, self-contained, dependency-free HTML micro-kernel widget.

## Operation
- ARRIVE sets ACTIVE (💧).
- MOLT sets PAUSED (❄️).
- EXIT sets ARCHIVED (📖).
- When ARCHIVED, only ARRIVE is accepted.
- COPY|FORK exports the state and in-memory event sequence as text.
- ROOT and ARRIVAL links navigate to the canonical surfaces.

## Scope and limits
This is a local deterministic finite-state-machine demo. It has no persistence across reloads, no cryptographic hashes, no identity verification, no credential issuance, no notarization, no MCP server connection, and no authority delegation. The export is an informational receipt, not proof of integrity. The UI has no animation. It uses no external scripts, fonts, or assets. It is not a blockchain.

## Deploy
Copy `index.html` into any static web host, including GitHub Pages. For embedding, use a 300×500 iframe. Clipboard write may require HTTPS or localhost; the legacy fallback is best-effort.

## Freeze
After final edits: `wc -c < index.html` and `sha256sum index.html`. Record the output in a separate external receipt. Until then: FREEZE-READY.
