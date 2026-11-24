# Media Capabilities — Focus

One hub for everything Neon Command Lines can make. All paths relative to repo root.

## 1. ImageGen (9:16 AI)
- Tool: `image_generate` (fal backend), `aspect_ratio: portrait`
- Style lock: `Picasso line minimalism, single continuous neon line drawing, ice-cyan neon on deep royal blue background #01015e, minimalist cubist line art`
- Subject lock: `a young man with wavy dark hair in a black hoodie`
- Swap only the scene. Text-to-image only — local photos can't be references (fal file_download_error).

## 2. TraceGen (true likeness, local)
- Input: any photo → Canny edges → contours → SVG paths → neon / pencil / twin / holomesh
- Scripts: `/tmp/trace2.py`, `/tmp/pencil.py`, `/tmp/holomesh.py` (logic lives in session; re-create from artifacts below)
- Outputs: `attachments/aesymov-neon.svg`, `aesymov-pencil.svg`, `aesymov-digital-twin.svg`, `yael-holomesh.svg` (+ PNG previews via cairosvg)

## 3. VideoGen (9:16 MP4)
- Plugin tool: `neon_videogen(images="a.png,b.png", output="...")`
- Spec: 720×1280, H.264 yuv420p, 30fps, Ken Burns (1.0→1.12 zoom), 15-frame crossfade
- Verify: `ffprobe -show_entries stream=width,height,codec_name,r_frame_rate`
- Demo: `attachments/neon-command-lines-9x16.mp4` (15s, 450 frames)

## 4. 3D Neon Sign (Three.js)
- `attachments/yael-neon-threejs.html` — SVG paths → TubeGeometry, orbit/pulse/glow, palette #85e9fc/#01015e
- Backups: `.v1.html`, `.v2.html`

## 5. Goals
- `goal_set / goal_list / goal_progress` (plugin-data JSON, 0–100 clamp)
- Milestone loop: set goal → prompt → image → video → progress 25/50/75/100

## Plugin
`plugins/neon-command-lines/` — 5 tools + bundled skill, tested (`test_plugin.py` → ok).
CI note: GitHub Actions access incoming — add `hermes plugins validate` + `test_plugin.py` + ffprobe check as CI steps on PR.

## Quick commands
```bash
python3 plugins/neon-command-lines/test_plugin.py
ffprobe attachments/neon-command-lines-9x16.mp4
python3 -m http.server 8765 --directory attachments  # demo: /yael-neon-demo.html
```

## 6. Pixel Animation (CUDA tiles)
- No GPU in this container (no nvidia-smi / CUDA) — implemented the CUDA tile model on CPU with numpy: image split into 32×32 tiles (CUDA blocks), per-pixel kernel (glow pulse + scan wave), tiled loop identical to a `__global__ void kernel(float* img)` where each thread does one pixel.
- Port path: same kernel → CUDA C (`nvcc`), tiles = `blockIdx`, pixels = `threadIdx`, shared mem = tile buffer. Runs on any NVIDIA GPU (Omniverse / RTX) or GitHub Actions GPU runner.
- Effect: per-tile gain `0.85+0.25*sin(t+ (bx+by)/180)`, cyan channel boost.
- Demo: `attachments/aesymov-pixel-anim.mp4` — 3s, 90 frames, 720×1280, generated tile-by-tile from `aesymov-neon.png`.
- Script: `/tmp/pixel_anim.py` (CPU reference implementation).

## 7. Motion design patterns (from 15-repo list)
- Ship launch: script + voiceover + camera moves as code, film-grade, no After Effects
- Edit footage: cut dead air/mistakes first, then add motion graphics + B-roll timed to words
- Shorts: storyboard first, 7 styles (cut paper to riso to pixel), self-check frames
- Animate site: one sentence -> site animation (motion, GSAP)
- Official blocks: HyperFrames (HTML->video), Remotion (React->video), GSAP skills, LottieFiles Disney 12 principles for agents
- Patterns to steal: stage gates, beat-synced cuts, HTML as source of truth, window.seek() export, official best-practice skills

## 8. æ Studio MP4 v1.0 — recommendations (2026-11-05)
Priority: turn video production into a reproducible, verifiable cinematic factory connected to agentic environments.
1. Audio sincronizado (max priority): ElevenLabs bilingual narration, AAC 48kHz, volume-controlled mixes, keep silent autoplay version.
2. Motor cinematográfico 9:16: standardize scenes, camera moves, lighting, particles, transitions. 720p preview / 1080p publish.
3. Personaje @YÆL: reusable movement library (walk, point, present, build, activate interfaces), æ identity everywhere.
4. GitHub Actions factory: JSON config per production, versioned assets, automated tests, downloadable artifacts. Heavy renders on specialized runner.
5. Witness per MP4: SHA-256, resolution, duration, codec, FPS, generator version, asset origin, loop continuity check.
First production: @YÆL · Contribution City — 9s, 270 frames, perfect loop. Robot æ crosses a city of contributions, buildings light up, DNA helix appears, ends "Many agents. One principal."
Quality: reported 8.5/10, engineering goal 9.5/10 (needs audio, performance, mobile compatibility, reproducibility — not yet reached).
Architecture decision: no initial GPU / generative video dependency. CPU reproducible factory first, GPU + motion generation as optional later.
Tinker -> Make -> Engineer -> Witness -> æ

## 9. Navier Engine v0.1 — Navier-Stokes x æ Studio
Equation: rho(du/dt + u·grad u) = -grad p + mu*laplacian u + f
In plain terms: Movimiento = presion + viscosidad + fuerzas externas.
Cinematic application: procedural physical-looking motion for 9:16 factory.
- Agua: ondas y remolinos
- Atmosfera: humo y niebla
- Vortices: energia y particulas
- Cine 9:16: loops reproducibles
Technical: 2D Stable Fluids solver (advection, diffusion, pressure projection) + visual particles.
9s @ 30fps: 270 frames deterministic, periodic boundaries for seamless loops, CPU 720x1280, H.264 + ffprobe, Witness params + seed.
Disclaimer: physically inspired, not a scientific Navier-Stokes solution.
First scene: @YÆL emerges from a luminous fluid vortex and materializes in Contribution City.
🌊 -> 🧬 -> 🤖 -> 🏙️ -> æ
