# Asimov Stick Scenes

Three dependency-free `<canvas>` lessons built on the unmodified runtime from [nilbuild/stick-scene](https://github.com/nilbuild/stick-scene).

| Scene | Lesson | Source |
|---|---|---|
| `asimov-authority` | Command → private approval → Asimov acts → receipt | `scenes/asimov-authority.js` |
| `asimov-verbs` | Governed Menlo verbs behind one policy lever | `scenes/asimov-verbs.js` |
| `asimov-twin` | qpos frames → USD twin → visible robot | `scenes/asimov-twin.js` |

Live page: `/asimov-stick/`

Each scene was rendered frame-by-frame with the upstream `scripts/frames.mjs` workflow and checked with `scripts/motion.mjs`; all three report clean motion. The runtime is copied unchanged. Asimov scenes are authored for OpenSourceWare education.

Authority chain shown in every lesson:

```text
HUMAN://ROOT → æ POLICY → DAO BRAIN → ASIMOV → RECEIPT
```

Upstream runtime: MIT © Kamran Ahmed. See `LICENSE`. Independent build; no institutional endorsement claimed.
