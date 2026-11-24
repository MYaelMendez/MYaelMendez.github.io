# Attribution

`tiny-voca-voice` is an integration and governance layer. The voice model,
phonemizer, and canvas runtime come from upstream open-source projects. We are
grateful for their work and keep their licenses intact.

## Thank you

**Thank you to the original [tiny-voca](https://github.com/n4ze3m/tiny-voca)
project and its authors.** The model and weights make local English speech
possible without a cloud API key. We wrapped them with a Hermes provider
contract, alias normalization, receipts, identity bindings, tests, and a Desktop
dock — but the source voice belongs to them.

**Thank you to [dizione](https://github.com/n4ze3m/dizione)** for the English
phonemizer used at runtime.

**Thank you to [nilbuild/stick-scene](https://github.com/nilbuild/stick-scene)**
and Kamran Ahmed for the dependency-free canvas runtime behind the Asimov
educational lessons.

## Upstream licenses

- `n4ze3m/tiny-voca` — Apache-2.0 (model and weights; downloaded and verified, not vendored).
- `n4ze3m/dizione` — Apache-2.0 (phonemizer; provisioned at runtime).
- `nilbuild/stick-scene` — MIT © Kamran Ahmed (runtime copied unchanged into `assets/stick-scene/`).
- NumPy, ONNX Runtime — installed separately under their own licenses.

## What we added

- Hermes plugin: five tools, native TTS provider contract, hash-chained receipts.
- Voice identity: `identity.json` binding voice → principal → compute layer.
- Hermes Desktop half: docked pane, statusbar chip, palette command, scoped backend.
- Asimov education: three narrated stick lessons with governed identity figures.
- Repo artifacts: 1:1 explainer film, logo, self-contained preview page.

Authority remains with the human. `HUMAN://ROOT` is an attribution marker for
the receipt ledger, not a software license and not a claim over upstream work.

#opensourceware #internetofagents
