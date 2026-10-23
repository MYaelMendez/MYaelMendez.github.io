# America250 · 250,000 new owners

Status: independent pilot implementation; 250,000 is an ambition, not an achieved count. This is Yael Méndez / æ Studio's proposed initiative, not an official America250 or OpenAI program.

## The culminating intent

Combine CLI.LLC's conversation-first interface, æ Studio's glass environment, #OSW ownership and #IoA collaboration into a repeatable path toward useful, human-owned enterprises.

One human intent → one glass conversation → three bounded workstreams → reviewable contributions → customer value → income → reinvestment.

The target is **250,000 new owners contributing to the next American century**. Success must be measured by first sales, sustained owner earnings, survival and retained ownership, not company registrations, model outputs or agent counts alone. No ownership outcomes are claimed by this pilot.

## Model foundation

Use OpenAI's **gpt-oss-20b**, served locally as `gpt-oss:20b`, as the initial open-weight engine. Keep the 120b option explicit for operators who choose suitable infrastructure. The model weights are Apache 2.0 licensed subject to the gpt-oss usage policy. The application and model licenses are separate; this pilot distributes no model weights or third-party code.

Official sources checked 2026-10-23:

- https://openai.com/index/gpt-oss-model-card/
- https://help.openai.com/en/articles/11870455-openai-open-weight-models-gpt-oss
- https://developers.openai.com/cookbook/articles/gpt-oss/run-locally-ollama

OpenAI's guide documents Ollama's local Chat Completions endpoint at `http://localhost:11434/v1` and model tag `gpt-oss:20b`. The weights run outside ChatGPT/OpenAI API hosting. Model availability does not provide compute, a connected endpoint or an execution grant. No Ollama runtime or model weights were found in the current build environment, so actual inference remains unverified.

## What this slice implements

- Browser-local contribution drafts: Build / Research / Review roles, human-set review state, one shared intent and explicit JSON export. No runtime is invoked by the static page.
- An economic scenario calculator with visible formulas and adjustable inputs; all values are illustrative assumptions. Revenue, gross profit, operating costs and potential owner earnings remain separate. These are not national accounts, GDP contributions, forecasts, investment returns or measured program outcomes.
- A Python standard-library adapter for **one explicitly requested text-only gpt-oss contribution** at a numeric loopback Chat Completions endpoint. No tools, browsing, shell execution, payments, filing or account creation. It rejects tool calls and invalid result schemas, bounds input/output size and time, refuses redirects and remote endpoints, and writes a new private receipt file without overwriting existing files.
- Each contribution returns summary, artifact text and reported evidence references. References remain unverified and outputs remain pending human review. A hash records content integrity, not authenticity, provenance attestation or proof that a named model's weights actually ran.
- Tests exercise the real adapter through a **mock local HTTP server**, plus request/response validation. Mock responses are not model-inference evidence.

The separate Codex/OpenClaw/Hermes viewports are a proposed runtime composition. This generic gpt-oss adapter does not connect or impersonate any of those systems. It supplies a shared open-weight engine pathway; each system still requires its own host, connection, permission boundary and demonstrated operation.

## Operator path

Use an already installed and authorized local runtime following the official guide. This repository does not install software or download weights automatically.

```bash
python3 america250/gpt_oss_adapter.py --input america250/example-task.json --dry-run
python3 america250/gpt_oss_adapter.py --input america250/example-task.json --output ./my-contribution.json
```

The second command sends the selected task to `http://127.0.0.1:11434/v1/chat/completions`. It requires the local server and the configured model to be running. Keep private receipts out of public Git history. Never interpret successful model output as customer validation or authority to execute the generated artifact. The browser page can export a selected task for this CLI and import the resulting receipt for inspection; it does not auto-contact localhost from a public website.

## Evidence and economic measurement

Collect opt-in, minimally necessary observations per owner/cohort: intent prepared, useful contribution accepted, first paid sale, retained ownership, 30/90/365-day survival, realized revenue, operating/compute costs and owner earnings. Define unique-owner deduplication, observation period, evidence source, consent and revocation before collecting a real cohort. Do not publish identifying customer or financial data in the public homebase. This pilot has no enrollment backend or independently verified outcome ledger.

Economic scenario:

`operating owners = target × activation fraction × retention fraction`

`annual gross revenue = operating owners × annual sales per operating owner`

`gross profit = gross revenue × gross margin fraction`

`operating surplus before tax = gross profit − operating owners × (annual other operating costs + annual compute costs)`

Negative surplus remains visible. Do not add revenue and earnings together or claim net-new national economic value without counterfactual evidence. Record denominators and missing observations when reporting real progress.

## Next verified milestone

One consenting operator runs one bounded task through an actually running gpt-oss endpoint, reviews the returned artifact and records a real acceptance/rejection. Then test a small voluntary cohort and measure useful customer outcomes before scaling. Initial completion of this code slice is not completion of the 250,000-owner ambition.

Context may propagate; authority does not.
