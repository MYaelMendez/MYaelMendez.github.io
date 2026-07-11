# sovereign-state — the soft repo

>_æ: durable memory, externalized.

The agent's local memory is capped (~2.2k chars). Durable facts don't belong
there — they belong in version control, linkable and fetchable by both the
agent and the assured viewport.

## Files
- `memory.json` — structured durable facts (identity, stack, paths, conventions,
  viewport registry, chassis primitives). Machine-readable; fetched by the
  agent and rendered by `sovereign-state.html`.
- `ledger.csv` — real-data ledger. One row per sovereign event. No fabricated
  values; append only when something actually happens.
- `sovereign-state.html` — the viewport that reads `memory.json` live and
  renders the facts. Closes the loop: agent writes → soft repo → viewport proves.
- `README.md` — this file.

## How to reference
- From the agent: `fetch https://myaelmendez.github.io/sovereign-state/memory.json`
  instead of relying on capped local memory. Update by editing + pushing.
- From any viewport: `fetch('./sovereign-state/memory.json')` and render.

## Bar
Same as every assured viewport: render + decode/parse + live HTTP 200 before
anything here is called "true."
