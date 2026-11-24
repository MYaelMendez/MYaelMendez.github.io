# PROOF/1 — the receipted film format

A film format, de novo, built from the best practices and innovations of this
research programme. A film made in it is a **proof**.

- **Spec:** `proof/film/1` (JSON). One file commands the whole artefact.
- **Container:** `<name>.proof.json` (the spec) + `<name>.mp4` (the render) +
  `<name>.receipt.json` (the hash + gate) + `<name>.meta.json` (provenance).
- **Renderer:** `proof1.py` — deterministic. Same spec + same sources → same
  bytes, on any machine with the same assets.
- **Citation:** `æ://film/<name>`; the DOI is the SHA-256 of the delivered bytes.

## What the format encodes (each from a measured prior innovation)

| field | innovation it carries |
|---|---|
| `emoji` | **emoji-as-context** — one symbol fixes palette, camera and motion (`emoji_scene.py`). Same symbol → same film. |
| `beats.select: sort_sources_by_sha256` | **provenance-first composition** — the sources are chosen by hash, not by taste; the selection is provable. |
| `beats[].sha256` | **receipt-in-frame** — each second burns its source's hash into the picture (`PROOF/09`). |
| `voice.max_seconds` | **size the voice to the picture** — the line is written to fit, never synthesised long and trimmed (run-2 lesson). |
| `overlay.lower_third.fill = [22,19,13]` | **fix the scene, never the threshold** — void-black bands drop luminance under the floor and the gate refuses. |
| `overlay.lower_third.height = 250` | **clear the seam** — the source's own HUD text must not bleed into the footer. |
| `gates.*` | **the gate is part of the format** — luminance / contrast / motion / black / mux are declared, never lowered to pass. |
| `receipt` | **the DOI is the bytes** — the hash of the delivered artefact, not of the source. |

## Schema (v1)

```json
{
  "schema": "proof/film/1",
  "title": "CHAIN/09",
  "tagline": "nine links, nine seconds",
  "seconds": 9,
  "fps": 24,
  "size": [720, 1280],
  "emoji": {"symbol": "🤖", "seed": 9},
  "voice": {"text": "…", "voice": "hermes", "seed": 9, "max_seconds": 8.6},
  "beats": {
    "count": 9,
    "per_beat_seconds": 1.0,
    "select": "sort_sources_by_sha256",
    "sources_dir": "C:/æ/github-pages",
    "glob": "asimov-*.mp4",
    "labels": ["custody", "format", "gate", "authority", "contract",
               "dispatch", "publish", "delivery", "adoption"],
    "expected": [
      { "source": "asimov-free-walk-916.mp4", "sha256": "24dc87ed…" }
    ]
  },
  "overlay": {
    "beat_numeral": true,
    "source_block": {"sha256_chars": 32, "rect": [0, 540, 620, 720]},
    "progress_cells": "per_frame",
    "footer": "GPL · GOVERNANCE-AND-PROVENANCE LABORATORY",
    "lower_third": {"height": 250, "fill": [22, 19, 13]}
  },
  "gates": {"luminance": 20, "contrast": 10, "motion": 0.5,
            "black_pct": 5, "mux_delta_s": 0.15},
  "output": {"name": "chain-09", "receipt": true, "meta": true}
}
```

## Laws

1. The spec commands; the renderer follows. Never edit a render to change a
   film — change the spec.
2. Every source is cited **in-frame**, not only in the manifest.
3. A gate refusal is repaired in the spec (warmer panel, shorter voice, fewer
   beats) — never by lowering a threshold.
4. A proof without its receipt is not a proof. The in-frame digest is the first
   32 hex of the sha256 (128 bits — the width 720 can carry); the full 64 hex
   lives in the receipt. Never label a truncation as the whole hash.
5. **A source that no longer matches the spec's `expected` sha256 refuses to
   render.** The format does not silently re-source.
6. A run that uses the format appends **proved / broke / change** to the skill's
   run log.

## Status

- `proof-09` (PROOF/09) is the format's **precursor**, not yet a `proof/1`
  instance; its rules were derived from it.
- The first true `proof/1` instance is rendered by `proof1.py` from a
  `<name>.proof.json`.
