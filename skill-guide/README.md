# æ:// skill-guide — local skill library

**208 skills** across **37 groups** in `~/.hermes/skills/` — 501 references · 116 scripts · 103 templates · 56,170 lines of procedural memory.

## Two surfaces

| Surface | What it shows |
|---|---|
| **`skill-guide.html`** | The **catalog** — search, group filters, click-to-copy `skill_view(...)` |
| **`skill-graph.html`** | The **topology** — force-directed graph of how skills reference each other |

## The skill graph

**205 nodes · 255 edges.** An edge means one skill references another, from three signals:

1. **`related_skills` frontmatter** (184 edges, weight 2) — the declared, intentional link
2. **Prose backtick mentions** (109 edges, weight 1) — `` `other-skill` `` in the body
3. **Shared reference files** (26 edges, weight 1) — two skills pointing at the same `references/*.md`

### Hubs (most connected)

| Skill | Degree |
|---|---|
| `html-as-skill` | 14 |
| `hermes-agent` | 10 |
| `cuda` | 8 |
| `hermes-surface-development` | 8 |
| `claude-design` | 8 |
| `subagent-driven-development` | 8 |
| `glocal-mesh` | 7 |
| `excalidraw` | 7 |
| `agentic-entrepreneurship` | 7 |
| `deploy-surfaces` | 6 |
| `agentic-language-chassis` | 6 |
| `grounded-citations` | 6 |
| `github` | 6 |
| `requesting-code-review` | 6 |
| `systematic-debugging` | 6 |

### Isolated skills (46)

`agentic-html`, `agentic-interpreter`, `apple-reminders`, `baoyu-infographic`, `clip`, `code-review`, `cri-index`, `distributed-llm-pretraining-torchtitan`, `domain-intel`, `dspy`, `evaluating-llms-harness`, `faiss`, `findmy`, `gif-search`, `glocal-host-loop`, `huggingface-accelerate`, `hyperframes-audio`, `hyperframes-studio`, `imessage`, `instructor`, `jupyter-live-kernel`, `linear`, `local-secret-source`, `mail-agent`, `minecraft-modpack-server`, `nano-pdf`, `nemo-curator`, `openhue`, `peft-fine-tuning`, `petdex`, `pinecone`, `pokemon-player`, `polymarket`, `pytorch-lightning`, `qdrant-vector-search`, `qr`, `sdlc-review`, `segment-anything-model`, `simpo-training`, `slime-rl-training`, `sovereign-git-ops`, `spanish-rae`, `vscode-installer-and-vsix-packaging`, `weights-and-biases`, `whisper`, `yuanbao`

These have zero declared or inferred links — candidates for either a `related_skills` entry or acknowledging they're genuinely standalone.

### Reading the graph

- **Node size** ∝ degree (hubs are bigger); **color** = group
- **Hover** a node → detail panel shows group, degree, and neighbors
- **Click** a node → pin its neighborhood (edges light gold); click a neighbor name to jump
- **Drag** to pan, **scroll** to zoom
- **Legend** — click a group to hide/show it (isolate a cluster)
- **Search** — type a name to fly to it

*Regenerate with the extractor in `graph-raw.json` + `graph.json`.*

---


## Groups

| Group | Skills | Group | Skills |
|---|---|---|---|
| æ:// Sovereign Mesh | 4 | Business | 4 |
| Sovereign Compute (CUDA/GPU) | 3 | Dogfood | 2 |
| Hermes Surfaces & Operator Grammar | 3 | Email | 2 |
| QR Identity & Contracts | 2 | Gaming | 2 |
| Index Surfaces (CRI / Measurement) | 2 | Hermes | 2 |
| HyperFrames (video) | 10 | MCP | 2 |
| Business / Agentic | 1 | Security | 2 |
| QA & Verification | 1 | Social Media | 2 |
| Platform Integrations | 1 | Agentic | 1 |
| MLOps | 42 | Data Science | 1 |
| Software Development | 36 | Desktop | 1 |
| Creative | 19 | DevOps | 1 |
| Productivity | 19 | Leisure | 1 |
| Research | 11 | Local Secrets | 1 |
| Autonomous AI Agents | 6 | Note-taking | 1 |
| Sovereign | 6 | Smart Home | 1 |
| GitHub | 5 | Web | 1 |
| Media | 5 | inference.sh | 1 |
| Apple | 4 | | |

---

## æ:// Sovereign Mesh  <sub>(4)</sub>

- **`code-mode`** — Execute agent code against the æ mesh DSL in sandbox.
- **`computer-use`** — Drive the user's desktop in the background — clicking, typing, scrolling, dragging — without stealing the cursor, keyboard focus, or switching virtual… _(1ref)_
- **`keeper`** — Use when reporting system state or auditing the mesh.
- **`æ`** — Sovereign private client mesh of agentic engineering. Every install is its own bounded local-first mesh node: conductor + viewport + Monaco editor + QR… _(3ref)_

## Sovereign Compute (CUDA/GPU)  <sub>(3)</sub>

- **`cuda`** — Use when building NVIDIA/CUDA compute surfaces for Hermes — the >_n: NemoClaw operator grammar, nvidia-smi webview bridges, GPU telemetry tiles, and local… _(1ref)_
- **`llama-cpp-gpu`** — Generate code with llama.cpp GPU offload on RTX 3050. Part of PC://INFERENCE layer.
- **`sovereign-cuda-bridge`** — Bridge sovereign/local CUDA compute across nodes — a public droplet (brain/identity) dispatching CUDA jobs to a local GPU behind NAT (sovereign hands)… _(4ref, 1scr)_

## Hermes Surfaces & Operator Grammar  <sub>(3)</sub>

- **`hermes-desktop-plugins`** — Build Hermes desktop plugins with Python backend + ESM UI. _(2tpl)_
- **`hermes-native`** — Hermes Native: sovereign VS Code inference/runtime skill + blueprint. Use when the user invokes `remoteUse.hermesNative`, references Hermes Native,… _(2ref)_
- **`hermes-operator-grammar`** — Canonical Hermes operator grammar: c://, pc://, vscode://, hermes://, H://, NOUS://, daollc://, llc://, +æ://, H://cc, pc://run

## QR Identity & Contracts  <sub>(2)</sub>

- **`pc-qr-api`** — Create, sign, and verify QR contracts for PC:// authority.
- **`qr-as-skill`** — Use when building QR key/contract infrastructure.

## Index Surfaces (CRI / Measurement)  <sub>(2)</sub>

- **`cri-index`** — Use when building Consumer Redline Index.
- **`measurement-index`** — Use when building observation-based measurement indices.

## HyperFrames (video)  <sub>(10)</sub>

- **`hyperframes`** — Mandatory entry point: read this first for any request to make, create, edit, animate, or render a video, animation, or motion graphic, including a promo,… _(16ref, 3scr)_
- **`hyperframes-animation`** — All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND the… _(1ref, 6scr)_
- **`hyperframes-audio`** — Use when audio already placed in a HyperFrames composition needs to be mixed: fade-in/fade-out, crossfade, track gain or volume, volume automation,… _(4ref, 2scr)_
- **`hyperframes-cli`** — Use the HyperFrames CLI development loop: init, add, catalog, capture, lint, check, snapshot, compare, grade-compare, preview, play, present, beats,… _(10ref)_
- **`hyperframes-core`** — The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes, `class="clip"`,… _(10ref)_
- **`hyperframes-creative`** — Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat… _(16ref, 4scr, 1tpl)_
- **`hyperframes-keyframes`** — Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe, Ken Burns treatment, camera move, visual match/whip handoff, or other… _(1ref)_
- **`hyperframes-registry`** — Search, install, and wire registry blocks and components into HyperFrames compositions. Use BEFORE hand-building any named visual — whenever a brief, a… _(9ref)_
- **`hyperframes-studio`** — Use when working with a person on a HyperFrames project in Studio: first, whether their message asks for a change at all (questions, loose ideas and…
- **`media-use`** — Agent Media OS, the single skill for every media need in a HyperFrames project. Resolve BGM, SFX, image, icon, brand logo, voice, color grade, or LUT into… _(10ref, 14scr)_

## Business / Agentic  <sub>(1)</sub>

- **`mail-agent`** — Use when building agentic electronic engineering mail.

## QA & Verification  <sub>(1)</sub>

- **`dogfood`** — Systematic exploratory QA testing of web applications — find bugs, capture evidence, and generate structured reports _(1ref, 1tpl)_

## Platform Integrations  <sub>(1)</sub>

- **`yuanbao`** — Yuanbao (元宝) groups: @mention users, query info/members.

## MLOps  <sub>(42)</sub>

- **`audiocraft-audio-generation`** — AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. _(2ref)_
- **`axolotl`** — Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support _(4ref)_
- **`chroma`** — Open-source embedding database for AI applications. Store embeddings and metadata, perform vector and full-text search, filter by metadata. Simple… _(1ref)_
- **`clip`** — OpenAI's model connecting vision and language. Enables zero-shot image classification, image-text matching, and cross-modal retrieval. Trained on 400M… _(1ref)_
- **`cuda`** — Use when building NVIDIA/CUDA compute surfaces for Hermes — the >_n: NemoClaw operator grammar, nvidia-smi host bridges, GPU telemetry tiles, and local… _(1ref, 1tpl)_
- **`distributed-llm-pretraining-torchtitan`** — Provides PyTorch-native distributed LLM pretraining using torchtitan with 4D parallelism (FSDP2, TP, PP, CP). Use when pretraining Llama 3.1, DeepSeek V3,… _(4ref)_
- **`dspy`** — Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - Stanford NLP's… _(3ref)_
- **`evaluating-llms-harness`** — lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). _(4ref)_
- **`faiss`** — Facebook's library for efficient similarity search and clustering of dense vectors. Supports billions of vectors, GPU acceleration, and various index… _(1ref)_
- **`fine-tuning-with-trl`** — Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRPO for reward optimization, and… _(4ref)_
- **`gguf-quantization`** — GGUF format and llama.cpp quantization for efficient CPU/GPU inference. Use when deploying models on consumer hardware, Apple Silicon, or when needing… _(2ref)_
- **`grpo-rl-training`** — Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training _(1tpl)_
- **`guidance`** — Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with… _(3ref)_
- **`hermes-atropos-environments`** — Build, test, and debug Hermes Agent RL environments for Atropos training. Covers the HermesAgentBaseEnv interface, reward functions, agent loop… _(3ref)_
- **`huggingface-accelerate`** — Simplest distributed training API. 4 lines to add distributed support to any PyTorch script. Unified API for DeepSpeed/FSDP/Megatron/DDP. Automatic device… _(3ref)_
- **`huggingface-hub`** — HuggingFace hf CLI: search/download/upload models, datasets.
- **`huggingface-tokenizers`** — Fast tokenizers optimized for research and production. Rust-based implementation tokenizes 1GB in <20 seconds. Supports BPE, WordPiece, and Unigram… _(4ref)_
- **`instructor`** — Extract structured data from LLM responses with Pydantic validation, retry failed extractions automatically, parse complex JSON with type safety, and… _(3ref)_
- **`lambda-labs-gpu-cloud`** — Reserved and on-demand GPU cloud instances for ML training and inference. Use when you need dedicated GPU instances with simple SSH access, persistent… _(2ref)_
- **`llama-cpp`** — llama.cpp local GGUF inference + HF Hub model discovery. _(6ref)_
- **`llava`** — Large Language and Vision Assistant. Enables visual instruction tuning and image-based conversations. Combines CLIP vision encoder with Vicuna/LLaMA… _(1ref)_
- **`modal-serverless-gpu`** — Serverless GPU cloud platform for running ML workloads. Use when you need on-demand GPU access without infrastructure management, deploying ML models as… _(2ref)_
- **`nemo-curator`** — GPU-accelerated data curation for LLM training. Supports text/image/video/audio. Features fuzzy deduplication (16× faster), quality filtering (30+… _(2ref)_
- **`obliteratus`** — Remove refusal behaviors from open-weight LLMs using OBLITERATUS — mechanistic interpretability techniques (diff-in-means, SVD, whitened SVD, LEACE, SAE… _(2ref, 3tpl)_
- **`optimizing-attention-flash`** — Optimizes transformer attention with Flash Attention for 2-4x speedup and 10-20x memory reduction. Use when training/running transformers with long… _(2ref)_
- **`outlines`** — Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local models (Transformers, vLLM), and… _(3ref)_
- **`peft-fine-tuning`** — Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models (7B-70B) with limited GPU memory, when you… _(2ref)_
- **`pinecone`** — Managed vector database for production AI applications. Fully managed, auto-scaling, with hybrid search (dense + sparse), metadata filtering, and… _(1ref)_
- **`pytorch-fsdp`** — Expert guidance for Fully Sharded Data Parallel training with PyTorch FSDP - parameter sharding, mixed precision, CPU offloading, FSDP2 _(2ref)_
- **`pytorch-lightning`** — High-level PyTorch framework with Trainer class, automatic distributed training (DDP/FSDP/DeepSpeed), callbacks system, and minimal boilerplate. Scales… _(3ref)_
- **`qdrant-vector-search`** — High-performance vector similarity search engine for RAG and semantic search. Use when building production RAG systems requiring fast nearest neighbor… _(2ref)_
- **`segment-anything-model`** — SAM: zero-shot image segmentation via points, boxes, masks. _(2ref)_
- **`serving-llms-vllm`** — vLLM: high-throughput LLM serving, OpenAI API, quantization. _(4ref)_
- **`simpo-training`** — Simple Preference Optimization for LLM alignment. Reference-free alternative to DPO with better performance (+6.4 points on AlpacaEval 2.0). No reference… _(3ref)_
- **`slime-rl-training`** — Provides guidance for LLM post-training with RL using slime, a Megatron+SGLang framework. Use when training GLM models, implementing custom data… _(2ref)_
- **`sovereign-local-loop`** — Build bounded, fully-offline sovereign agent loops on a local machine — the +æ^glocal primitive (planner→executor→auditor→manifest) with local hands… _(2ref)_
- **`sparse-autoencoder-training`** — Provides guidance for training and analyzing Sparse Autoencoders (SAEs) using SAELens to decompose neural network activations into interpretable features.… _(3ref)_
- **`stable-diffusion-image-generation`** — State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. Use when generating images from text prompts, performing… _(2ref)_
- **`tensorrt-llm`** — Optimizes LLM inference with NVIDIA TensorRT for maximum throughput and lowest latency. Use for production deployment on NVIDIA GPUs (A100/H100), when you… _(3ref)_
- **`unsloth`** — Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization _(4ref)_
- **`weights-and-biases`** — W&B: log ML experiments, sweeps, model registry, dashboards. _(3ref)_
- **`whisper`** — OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six model… _(1ref)_

## Software Development  <sub>(36)</sub>

- **`agentic-chassis-surface`** — Extend the æ:// agentic-language-chassis in C:\æ\hermes-fork — add a new scheme/surface (file://, computer://, desktop://, +bæsic://, etc.) that routes to… _(8ref, 2scr, 1tpl)_
- **`browser-agent-loop`** — Use when running an agent loop in the browser tab.
- **`code-review`** — Guidelines for performing thorough code reviews with security and quality focus
- **`codebase-inspection`** — Inspect codebases w/ pygount: LOC, languages, ratios.
- **`cuda-victus-dev`** — Develop CUDA locally on the Victus sovereign node (RTX 3050 6GB, nvcc 13.3) as a repeatable, cloud-free workflow. Fronted by the Hermes agent, hands on… _(2ref)_
- **`github`** — GitHub via gh CLI: PRs, issues, reviews, repos, auth. _(10ref, 2scr, 4tpl)_
- **`github-pages-deploy`** — Build/copy deploy scripts that publish static HTML surfaces (neuromitosis, aggregate, blueprints, skill manifests) into a local github.io Pages repo as… _(3ref, 1scr, 1tpl)_
- **`glocal-host-loop`** — Build sovereign offline local agents on Victus (x86_64-pc-windows-msvc + NVIDIA CUDA) using the +æ^glocal LocalHostLoop primitive —… _(3ref, 1tpl)_
- **`hermes-agent-skill-authoring`** — Author in-repo SKILL.md files: frontmatter and structure.
- **`hermes-runtime-state`** — OS-aware local runtime detection and normalized state modules for Hermes on Windows. Use when adding a detector for a local tool/toolchain, exposing an…
- **`hermes-surface-development`** — Extend the Hermes agentic engineering surface stack: new conductor schemes, Hermes Code viewports, glocal bridge patterns, Monaco exports, QR primitives,… _(17ref)_
- **`hermes-vscode-incubator`** — VS Code as the Hermes incubator on local Windows hardware. Use when working in C:\æ\hermes-fork, packaging or extending vscode-remote-use, wiring… _(4ref, 1tpl)_
- **`inspecting-hermes-desktop-dom`** — Read the live Hermes desktop DOM/CSS over CDP.
- **`interpreter-dispatch-debugging`** — Debug line/dispatcher interpreters (BASIC-style chassis, command routers, state machines) where a statement reaches the dispatcher but its handler never… _(1ref)_
- **`local-agent-runtime`** — Build bounded, fully-offline sovereign agents on the local machine (Victus/RTX 3050) using the +æ^glocal LocalHostLoop primitive… _(4ref)_
- **`local-first-operator-surfaces`** — Use when building local-first operator surfaces that expose actuator/simulator bridges from Hermes into deterministic runtimes: FastAPI apps, simulator… _(3ref)_
- **`native-vision-from-first-principles`** — Build native computer vision from first principles, no ML.
- **`node-inspect-debugger`** — Debug Node.js via --inspect + Chrome DevTools Protocol CLI.
- **`plan`** — Plan mode for Hermes — inspect context, write a markdown plan into the active workspace's `.hermes/plans/` directory, and do not execute the work.
- **`python-debugpy`** — Debug Python: pdb REPL + debugpy remote (DAP).
- **`requesting-code-review`** — Use when completing tasks, implementing major features, or before merging. Validates work meets requirements through systematic review process.
- **`resource-absorb-and-rename`** — Use when renaming resource X to Y across clones/bundles.
- **`simplify-code`** — Parallel 4-agent cleanup of recent code changes.
- **`sovereign-atproto-network`** — Build our own sovereign ATProto (Bluesky protocol) network as the protocol form of the MoD — a federation of local-first PDS nodes holding signed records,… _(5ref)_
- **`sovereign-fork-commit`** — Commit session/sovereign development artifacts into a coherent local git commit on a long-lived feature branch of a sovereign development fork (e.g.… _(2ref)_
- **`sovereign-git-ops`** — Operating the sovereign agentic-engineering git fork (the `æ://` mesh) on Windows/MinGW: the real `æ`-character checkout path, in-repo vs sibling-dir… _(1ref)_
- **`sovereign-local-agent`** — Build and expose sovereign local agent surfaces for the +æ^glocal runtime (Yæl's glocal Victus stack): offline LocalHostLoop agents, a ZERO-DEPENDENCY… _(4ref)_
- **`sovereign-mcp-surface`** — Expose local agent hands (CUDA, Rust/WASM, shell, files) as MCP tools over stdio — a zero-dependency (stdlib-only) JSON-RPC server that is air-gappable… _(2ref, 1tpl)_
- **`sovereign-vscode-surface-dev`** — Develop, edit, and package sovereign local VS Code webview surfaces (Hermes Native family and any local-only VS Code extension that renders HTML in a… _(4ref, 2scr)_
- **`spike`** — Throwaway experiments to validate an idea before build.
- **`subagent-driven-development`** — Use when executing implementation plans with independent tasks. Dispatches fresh delegate_task per task with two-stage review (spec compliance then code…
- **`systematic-debugging`** — 4-phase root cause debugging: understand bugs before fixing.
- **`test-driven-development`** — TDD: enforce RED-GREEN-REFACTOR, tests before code.
- **`vscode-as-skill`** — VS Code as a first-class Hermes operator surface/primitive. Use when extending vscode-remote-use, packaging VS Code commands, wiring homeOS/local… _(5ref, 1scr)_
- **`vscode-installer-and-vsix-packaging`** — Package, install, and ship a VS Code extension as a VSIX, and understand how VS Code itself is installed/updated across all platforms. Use when…
- **`writing-plans`** — Use when you have a spec or requirements for a multi-step task. Creates comprehensive implementation plans with bite-sized tasks, exact file paths, and…

## Creative  <sub>(19)</sub>

- **`architecture-diagram`** — Dark-themed SVG architecture/cloud/infra diagrams as HTML. _(1tpl)_
- **`ascii-art`** — ASCII art: pyfiglet, cowsay, boxes, image-to-ascii.
- **`ascii-video`** — ASCII video: convert video/audio to colored ASCII MP4/GIF. _(8ref)_
- **`baoyu-infographic`** — Infographics: 21 layouts x 21 styles (信息图, 可视化). _(5ref)_
- **`claude-design`** — Design one-off HTML artifacts (landing, deck, prototype).
- **`comfyui`** — Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter injection. Uses the official comfy-cli… _(4ref, 11scr)_
- **`design-md`** — Author/validate/export Google's DESIGN.md token spec files. _(1tpl)_
- **`excalidraw`** — Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). _(3ref, 1scr)_
- **`html-as-skill`** — Use when treating HTML as the executable agentic viewport. _(9ref, 1scr)_
- **`humanizer`** — Humanize text: strip AI-isms and add real voice.
- **`manim-video`** — Manim CE animations: 3Blue1Brown math/algo videos. _(16ref, 2scr)_
- **`p5js`** — p5.js sketches: gen art, shaders, interactive, 3D. _(10ref, 4scr, 1tpl)_
- **`popular-web-designs`** — 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. _(54tpl)_
- **`pretext`** — Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flow around obstacles, text-as-geometry… _(1ref, 2tpl)_
- **`sketch`** — Throwaway HTML mockups: 2-3 design variants to compare.
- **`songwriting-and-ai-music`** — Songwriting craft and Suno AI music prompts.
- **`sovereign-browser-surface`** — Build sovereign gold-on-void HTML surfaces.
- **`spanish-rae`** — Spanish per RAE — orthography and grammar.
- **`touchdesigner-mcp`** — Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-time visuals. 36… _(21ref, 1scr)_

## Productivity  <sub>(19)</sub>

- **`airtable`** — Airtable REST API via curl. Records CRUD, filters, upserts.
- **`box`** — Box manages cloud files, sharing, search, and metadata. _(10ref)_
- **`document-to-action-items`** — Extract cited obligations, deadlines, tasks from documents.
- **`docx`** — Create, read, edit, template, and review Word .docx files. _(1ref, 8scr)_
- **`google-workspace`** — Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. _(2ref, 4scr)_
- **`linear`** — Manage Linear issues, projects, and teams via the GraphQL API. Create, update, search, and organize issues. Uses API key auth (no OAuth needed). All…
- **`maps`** — Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. _(1scr)_
- **`meeting-action-items`** — Turn meeting notes into cited decisions, owners, tickets.
- **`nano-pdf`** — Edit PDF text/typos/titles via nano-pdf CLI (NL prompts).
- **`notion`** — Notion API + ntn CLI: pages, databases, markdown, Workers. _(1ref)_
- **`ocr-and-documents`** — Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker-pdf for OCR/scanned docs. For… _(2scr)_
- **`pdf`** — PDF files: create, read, merge, fill, OCR, edit text. _(3ref, 15scr)_
- **`petdex`** — Install and select animated petdex mascots for Hermes.
- **`powerpoint`** — Create, read, edit .pptx decks with python-pptx. _(5scr)_
- **`product-price-monitor`** — Watch product, flight, or listing prices; alert on target.
- **`qr`** — Route printed QR scans to Hermes conductor schemes. _(1ref, 1scr)_
- **`teams-meeting-pipeline`** — Teams meeting summaries, job replay, Graph subscriptions.
- **`weekly-review-planning`** — Weekly reset: commitments, stalled work, next-week plan.
- **`xlsx`** — Create, read, edit Excel .xlsx workbooks and CSVs. _(1ref, 7scr)_

## Research  <sub>(11)</sub>

- **`arxiv`** — Search and retrieve academic papers from arXiv using their free REST API. No API key needed. Search by keyword, author, category, or ID. Combine with… _(1scr)_
- **`blogwatcher`** — Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI. Add blogs, scan for new articles, and track what you've read.
- **`competitor-news-monitor`** — Watch named companies for material news; cited digests.
- **`domain-intel`** — Passive domain reconnaissance using Python stdlib. Subdomain discovery, SSL certificate inspection, WHOIS lookups, DNS records, domain availability… _(1scr)_
- **`duckduckgo-search`** — Free web search via DuckDuckGo — text, news, images, videos. No API key needed. Use the Python DDGS library or CLI to search, then web_extract for full… _(1scr)_
- **`grounded-citations`** — Ground answers and documents in cited, verifiable sources. _(2ref, 3scr)_
- **`llm-wiki`** — Karpathy's LLM Wiki: build/query interlinked markdown KB.
- **`ml-paper-writing`** — Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Use when drafting papers from research repos, structuring arguments,… _(5ref, 7tpl)_
- **`parallel-cli`** — Optional vendor skill for Parallel CLI — agent-native web search, extraction, deep research, enrichment, FindAll, and monitoring. Prefer JSON output and…
- **`polymarket`** — Query Polymarket: markets, prices, orderbooks, history. _(1ref, 1scr)_
- **`research-paper-writing`** — Write ML papers for NeurIPS/ICML/ICLR: design→submit. _(9ref, 7tpl)_

## Autonomous AI Agents  <sub>(6)</sub>

- **`agentic-interpreter`** — Delegate coding and computer-use tasks to Agentic Interpreter (ÆL-NET fork of Open Interpreter) — a Rust-based terminal coding agent with harness… _(1ref)_
- **`claude-code`** — Delegate coding to Claude Code CLI (features, PRs).
- **`codex`** — Delegate coding to OpenAI Codex CLI (features, PRs).
- **`computer-use`** — Drive the desktop background-first; escalate on signal.
- **`hermes-agent`** — Use, configure, theme, extend, and orchestrate Hermes Agent. _(18ref, 3tpl)_
- **`opencode`** — Delegate coding to OpenCode CLI (features, PR review).

## Sovereign  <sub>(6)</sub>

- **`ae-as-skill`** — Use when working with the æ:// sovereign computing stack.
- **`deploy-surfaces`** — Publish HTML surfaces to github.io; TLS-proxy the droplet.
- **`glocal-mesh`** — Build/operate the GLOCAL sovereign agent compute mesh — Mixture of Devices (MoD) addressed as codemode routes. Covers droplet brain + local RTX hands +… _(5ref)_
- **`pc-inference`** — PC://INFERENCE — portable inference substrate.
- **`rtx-telemetry`** — Use when wiring live NVIDIA RTX 3050 telemetry from the Victus sovereign node into a surface, dashboard, or agent — via the public droplet MCP² broker… _(1ref, 1scr)_
- **`sovereign-resource-absorption`** — Absorb an external resource and rename it into æ://.

## GitHub  <sub>(5)</sub>

- **`github-auth`** — GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. _(1scr)_
- **`github-code-review`** — Review PRs: diffs, inline comments via gh or REST. _(1ref)_
- **`github-issues`** — Create, triage, label, assign GitHub issues via gh or REST. _(2tpl)_
- **`github-pr-workflow`** — GitHub PR lifecycle: branch, commit, open, CI, merge. _(2ref, 2tpl)_
- **`github-repo-management`** — Clone/create/fork repos; manage remotes, releases. _(1ref)_

## Media  <sub>(5)</sub>

- **`agentic-html`** — Build deterministic HTML media viewports (agentic.html) from Hermes media manifests for glocal distribution. _(1scr, 1tpl)_
- **`gif-search`** — Search/download GIFs from Tenor via curl + jq.
- **`heartmula`** — HeartMuLa: Suno-like song generation from lyrics + tags.
- **`songsee`** — Audio spectrograms/features (mel, chroma, MFCC) via CLI.
- **`youtube-content`** — YouTube transcripts to summaries, threads, blogs. _(1ref, 1scr)_

## Apple  <sub>(4)</sub>

- **`apple-notes`** — Manage Apple Notes via memo CLI: create, search, edit.
- **`apple-reminders`** — Apple Reminders via remindctl: add, list, complete.
- **`findmy`** — Track Apple devices/AirTags via FindMy.app on macOS.
- **`imessage`** — Send and receive iMessages/SMS via the imsg CLI on macOS.

## Business  <sub>(4)</sub>

- **`agentic-entrepreneurship`** — Use when building agentic businesses, deploying HTML skill viewports, routing formation/payments, generating videos, or operating in the Agentic… _(45ref)_
- **`domain-codemode`** — Use when working with a domain portfolio as an agentic syntax stack. One compact Code Mode interface searches/executes per-domain skills without loading…
- **`domains-to-github-pages`** — Route all domains to a single GitHub Pages site — primary serves content, others 301 redirect. Uses Cloudflare DNS API + Hostinger Forwarding API. _(1ref)_
- **`reachy-clerk`** — Use when building Reachy Mini as an agentic Stripe clerk / DAOLLC operator: embodied business interface, simulation-first, safe secret handling, $OS… _(2ref, 2tpl)_

## Dogfood  <sub>(2)</sub>

- **`hermes-agent-setup`** — Help users configure Hermes Agent — CLI usage, setup wizard, model/provider selection, tools, skills, voice/STT/TTS, gateway, and troubleshooting. Use…
- **`hermes-local-dev-bridge`** — Manage local Hermes Agent development workflow on Windows: repo checkout, editable install, VS Code terminal bridge, and bridge tasks. _(1ref)_

## Email  <sub>(2)</sub>

- **`email-inbox-triage`** — Triage an inbox: prioritize threads, draft replies safely.
- **`himalaya`** — Himalaya CLI: IMAP/SMTP email from terminal. _(2ref)_

## Gaming  <sub>(2)</sub>

- **`minecraft-modpack-server`** — Set up a modded Minecraft server from a CurseForge/Modrinth server pack zip. Covers NeoForge/Forge install, Java version, JVM tuning, firewall, LAN…
- **`pokemon-player`** — Play Pokemon games autonomously via headless emulation. Starts a game server, reads structured game state from RAM, makes strategic decisions, and sends…

## Hermes  <sub>(2)</sub>

- **`hermes-conductor-mesh`** — Extend Hermes conductor with custom schemes, MCP² surfaces, mech-lang primitives, and glocal bridge dispatch. _(2ref)_
- **`hermes-operator-grammar`** — Governs Hermes operator scheme design, standalone `SchemeDispatcher` architecture, scheme registration order/longest-prefix dispatch, surface shapes,… _(14ref)_

## MCP  <sub>(2)</sub>

- **`mcporter`** — Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type…
- **`native-mcp`** — Built-in MCP (Model Context Protocol) client that connects to external MCP servers, discovers their tools, and registers them as native Hermes Agent…

## Security  <sub>(2)</sub>

- **`glocal-secrets`** — GLOCAL secret-handoff model for sovereign agents. github.io is the SOURCE OF TRUTH for the secret-bridge SURFACE; the SECRET lives only on Victus… _(3ref, 1tpl)_
- **`local-secret-source`** — Build, verify, and ship local-facing secret-storage surfaces (the "secret-source bridge") that are efficacious within a GLOCAL (Mixture-of-Devices) agent… _(2ref, 1scr)_

## Social Media  <sub>(2)</sub>

- **`xitter`** — Interact with X/Twitter via the x-cli terminal client using official X API credentials. Use for posting, reading timelines, searching tweets, liking,…
- **`xurl`** — X/Twitter via xurl CLI: raw post search, posting, DM, media.

## Agentic  <sub>(1)</sub>

- **`agentic-language-chassis`** — Selecting and wiring language chassis (qc64 BASIC and mech-lang) for the plus-ae and ae and viewport agentic scheme grammar in hermes-fork; registering… _(7ref, 1scr)_

## Data Science  <sub>(1)</sub>

- **`jupyter-live-kernel`** — Iterative Python via live Jupyter kernel (hamelnb).

## Desktop  <sub>(1)</sub>

- **`windows-gui-automation`** — Windows-specific recovery patterns for GUI automation when cua-driver, computer_use, or browser targeting fails. Covers interactive-session restart,… _(2ref)_

## DevOps  <sub>(1)</sub>

- **`sdlc-review`** — Review Kanban handoffs and route verified outcomes.

## Leisure  <sub>(1)</sub>

- **`find-nearby`** — Find nearby places (restaurants, cafes, bars, pharmacies, etc.) using OpenStreetMap. Works with coordinates, addresses, cities, zip codes, or Telegram… _(1scr)_

## Local Secrets  <sub>(1)</sub>

- **`local-secret-source-bridge`** — Build, verify, and ship local-facing secret storage surfaces for Hermes. Covers plugin SecretSource actions, local HTTP bridge handler, skeptical UI… _(4ref, 1tpl)_

## Note-taking  <sub>(1)</sub>

- **`obsidian`** — Read, search, create, and edit notes in the Obsidian vault.

## Smart Home  <sub>(1)</sub>

- **`openhue`** — Control Philips Hue lights, scenes, rooms via OpenHue CLI.

## Web  <sub>(1)</sub>

- **`blocked-page-recovery`** — Use when a fetch fails: 403/429, paywall, WAF, bot wall. _(1scr)_

## inference.sh  <sub>(1)</sub>

- **`inference-sh-cli`** — Run 150+ AI apps via inference.sh CLI (infsh) — image generation, video creation, LLMs, search, 3D, social automation. Uses the terminal tool. Triggers:… _(4ref)_

---

*æ:// language is compute · #hermiphicationisinevitable*
