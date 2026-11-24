# Third-Party Notices

> **Thank you to the original [tiny-voca](https://github.com/n4ze3m/tiny-voca)
> project and its authors.** This integration exists because you released the
> model and weights openly. Thank you also to
> [dizione](https://github.com/n4ze3m/dizione) for the phonemizer and
> [nilbuild/stick-scene](https://github.com/nilbuild/stick-scene) for the canvas
> runtime. We built the governance layer; you built the source.
>
> #opensourceware #internetofagents

`tiny-voca-voice` is a packaging and integration layer. It does not contain the
weights or the phonemizer implementation; those are upstream works used at
runtime under their own licenses. See [docs/ATTRIBUTION.md](docs/ATTRIBUTION.md).

## Apache-2.0 upstreams

### n4ze3m/tiny-voca

- **Source:** <https://github.com/n4ze3m/tiny-voca>
- **Weights:** <https://huggingface.co/n4ze3m/tiny-voca/resolve/main/onnx/model.onnx>
- **SHA-256:** `fe6d918791a15b82e37465981d7f27a070e46b46635e5a3482fc8dff87a1ae46`
- **License:** Apache License, Version 2.0.
- The `onnx/model.onnx` artifact is downloaded and verified at install time and
  is not redistributed in this repository.

### n4ze3m/dizione

- **Source:** <https://github.com/n4ze3m/dizione>
- **License:** Apache License, Version 2.0.
- Supplies the English phonemizer (`dizione.phonemize`) used by the CLI. Its
  data directory is derived from the runtime root (`$DIZIONE_DATA`).

A copy of the Apache License, Version 2.0 text is provided in [LICENSE](LICENSE).

## MIT upstream: nilbuild/stick-scene

- **Source:** <https://github.com/nilbuild/stick-scene>
- **Runtime:** `assets/stick-scene/stick.js`, copied unchanged.
- **Scenes:** three Asimov lesson scenes authored in this repository.
- **License:** MIT © Kamran Ahmed. The upstream LICENSE is copied into
  `assets/stick-scene/LICENSE` and into every generated lesson bundle.

## Runtime dependencies (not vendored)

Used at runtime but installed separately, each under its own license:

- **NumPy** — array operations and PCM conversion.
- **ONNX Runtime** — CPU inference backend.
- **Python standard library** — `wave`, `hashlib`, `json`, `argparse`, `pathlib`.

## Attribution note

`HUMAN://ROOT` is the receipt ledger's attribution marker for human authority;
it is not a software license. The `license: MIT` field in
`skills/tiny-voca-voice/SKILL.md` is the Hermes skill-authoring marker for that
document; it does not change the Apache-2.0 terms of the upstream model and
phonemizer described above.
