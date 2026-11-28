# llm.store · LAB

**LAB · DEMO — not production.** A rebuild of the llm.store prototype ([chassis](https://myaelmendez.github.io/llm-store.html)) for Yael Méndez, L:// R&D LAB. Preview: https://lutheraninstitute.github.io/aeee-lab/lab/llm-store/ (`noindex`).

The old chassis looked right but showed invented tickers, stale leaderboards and made-up agent counts. This version keeps the look (void black, gold, monospace, the `æææ:///llm.store ⫸` command line, x₀y₀z₀) and shows only numbers that come from a live API, a dated snapshot, or a measurement on your own device.

## What's live and what isn't

| Part | Status |
|---|---|
| Model catalog | **LIVE** from the OpenRouter public models API (`https://openrouter.ai/api/v1/models`, no key). If that fetch fails, it falls back to `models.snapshot.json`, labelled **SNAPSHOT** with its `fetched_at`. |
| Filters | free (both prices 0), open weights* (OpenRouter lists a Hugging Face repo, which hints at open weights but doesn't check the license), ≥1M context, cheapest paid. |
| Run in your browser | **Real.** WebLLM `@mlc-ai/web-llm@0.2.89` on WebGPU. The default is `Qwen3-0.6B-q4f16_1-MLC`, and you can also pick Qwen3.5-0.8B, Llama-3.2-1B, Qwen2.5-0.5B or Qwen3-1.7B. If the GPU lacks `shader-f16`, the page switches to the q4f32 builds. Weights download from Hugging Face once and are cached. Prompts never leave the device. |
| Your own node | **Real, optional.** Ollama at `http://localhost:11434` (`/api/tags`, streaming `/api/chat`). |
| tok/s meter | **MEASURED** from the actual run: (tokens − 1) ÷ time from first to last token, with the runtime's own token count. It also shows the engine-reported figure (WebLLM `decode_tokens_per_s`, Ollama `eval_count/eval_duration`). |
| Receipts | **Real.** Each run writes a SHA-256 receipt chained to the previous one (`llm.store.receipt/0.1`). Receipts live in localStorage and can be verified and exported as JSON. Prompts are stored as hashes only. |
| Hugging Face trending | **LIVE** on demand from the HF API. No snapshot. |
| Cloud inference | **Not wired, on purpose.** There are no keys and no cloud rent. Model cards show a `curl` example that you run with your own key. |
| Prices, payments, checkout | None. |

## Files

- `index.html` is the whole app: one static file with no build step. WebLLM is imported from esm.run only when you press **load**.
- `models.snapshot.json` is the normalized OpenRouter catalog with `fetched_at`.
- `llms.txt` is for agents: what the store is, its commands, its data and its receipt format.
- `ae.json` is the `ae.manifest/0.1` manifest. Principal: Yael Méndez. Authority: æ1 LAB.

## Commands

`help` · `ls models [free|open|long|cheap]` · `search <q>` · `run <model>` · `ask <text>` · `local` · `node [url]` · `receipts [verify|export|clear]` · `agents` · `hf` · `lang en|es` · `clear`

You can also pass a command in the URL (`?cmd=ls%20models%20free`) or call `window.LLMSTORE.run("…")`. Add `?lang=es` for Spanish.

## Run it

- **Hosted:** open the preview URL. On a computer, use a recent Chrome or Edge for WebGPU. On iPhone, Safari 26 / iOS 26 includes WebGPU; on older iOS it may be behind a feature flag. Small models only on phones.
- **Locally:** `python3 -m http.server 8080` in this folder, then open http://localhost:8080/.
- **Ollama:** `OLLAMA_ORIGINS="https://lutheraninstitute.github.io,http://localhost:8080" ollama serve`, then `ollama pull qwen3:0.6b`, then type `node` and `run qwen3:0.6b`. Safari won't call `http://localhost` from an https page, so use Chrome there or run the page locally.

## Refresh the snapshot

```bash
curl -s https://openrouter.ai/api/v1/models > or.json
# then normalize with: id, name, ctx, mod, in/out (USD per 1M), hf, created, max_out, plus fetched_at
```

Evidence ≠ Authority: supervision informs, the human decides. · Make something agents want.
