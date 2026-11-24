# Install

## 1. Place the plugin

Install this directory where Hermes Agent discovers plugins, so that
`__init__.py` is loadable. With the default plugin root, that is:

```text
$HERMES_HOME/plugins/hermes-ae/
```

`plugin.yaml` declares one tool, `ae`; no registration commands are needed
beyond normal plugin loading.

## 2. Install dependencies

```bash
python3 -m pip install numpy pillow mujoco onnxruntime dizione
```

Also required on the host:

- `ffmpeg` and `ffprobe` (encoding and QC).
- `git` configured with push access, if you publish videos.
- Self-hosted `tiny-voca` weights (ONNX model + `config.json` + `dizione`
  phonemizer data), with voices `F2` / `M2` at 24 kHz.
- STL meshes for the Asimov-1 links, placed in `HERMES_AE_MESHES`.

The repository ships XML/URDF manifests under `model/` but **not** binary STL
meshes or finished videos. The model source is
[menloresearch/asimov-1](https://github.com/menloresearch/asimov-1) (model
license CERN-OHL-S-2.0); see THIRD_PARTY_NOTICES.md.

## 3. Configure paths

All locations are optional and default to values derived from `HERMES_HOME`:

| Variable | Purpose | Default |
| --- | --- | --- |
| `HERMES_HOME` | Hermes install root | `~/.hermes` |
| `HERMES_AE_HOME` | Runtime root | `$HERMES_HOME/ae` |
| `HERMES_AE_ANIM` | Animation/frame artifacts | `$HERMES_AE_HOME/asimov-anim` |
| `HERMES_AE_MODEL` | Runtime model dir | `$HERMES_AE_HOME/model` |
| `HERMES_AE_MESHES` | STL mesh dir | `$HERMES_AE_MODEL/meshes` |
| `HERMES_AE_GALLERY` | Gallery repo checkout | `$HERMES_AE_HOME/gallery` |
| `HERMES_AE_LEDGER` | Receipt ledger file | `$HERMES_HOME/ae-receipts.jsonl` |
| `HERMES_AE_PLUGINS` | Legacy plugin dir (dispatcher) | `$HERMES_HOME/plugins` |
| `HERMES_AE_PYTHON` | Python for bundled subprocesses | `/usr/local/bin/python3` |

Set `HERMES_AE_PYTHON` to the interpreter that actually has the dependencies
above; bundled ops spawn it as a subprocess. `HERMES_AE_PLUGINS` is used by the
dispatcher for shortcut/`call` routing to optional legacy plugins; the two
bundled local ops need no legacy plugins.

The gallery repo at `HERMES_AE_GALLERY` should be a checkout of the `gh-pages`
branch with a configured `origin` remote. Publishing copies the MP4 there,
regenerates `videos.html`, commits, and pushes.

## 4. Verify the installation

```text
ae({"op": "status"})   # version 2.2.0, authority HUMAN://ROOT, chain head
ae({"op": "ops"})      # shortcuts + bundled local ops
ae({"op": "verify"})   # receipt chain is valid (count 0 on a fresh install)
```

A smoke render without publishing:

```text
ae({"op": "free_walk", "publish": false})
```

## Troubleshooting

- **"missing dependency" from TTS** — install `onnxruntime` and `dizione` into
  the `HERMES_AE_PYTHON` interpreter and confirm the tiny-voca weights path.
- **`bundled script missing`** — the repository is incomplete; ensure
  `scripts/` is present alongside `__init__.py`.
- **QC fails with bright_pixels too low** — verify STL meshes exist in
  `HERMES_AE_MESHES` and that `HERMES_AE_MODEL` does not shadow them.
- **Publish errors** — check `git` credentials and the `origin` remote in the
  gallery checkout, or pass `publish: false`.
