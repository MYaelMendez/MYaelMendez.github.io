# Asimov Robot Stick Lessons

`tiny-voca-voice` 1.2.0 ships a first-class Hermes capability for narrated
OpenSourceWare education. It packages the upstream [nilbuild/stick-scene](https://github.com/nilbuild/stick-scene)
runtime unchanged, adds three Asimov scenes, synthesizes English narration with
tiny-voca, and writes a `LESSON://BUILD` receipt. The generated page displays
the voice → compute-layer map from `identity.json`.

## Tool

```json
{"op": "list"}
{"op": "build", "lesson": "all", "out": "/path/to/output", "speed": 1.25}
```

`tts_stick_lesson` accepts `op`, `lesson`, `out`, and `speed`. `list` needs no
output path. `build` requires `out`. The parser returns one JSON object.

## Lessons

| ID | Scene | Lesson | Lines |
|---|---|---|---|
| `asimov-authority` | `asimov-authority` | Commandprompt → private-client approval → Asimov acts | 2 |
| `asimov-verbs` | `asimov-verbs` | Governed Menlo verbs behind one policy lever | 1 |
| `asimov-twin` | `asimov-twin` | qpos → USD twin → visible robot | 2 |
| `all` | all three | Full lesson set | 5 |

## Output

```text
out/
  index.html
  stick.js                 # upstream runtime, copied byte-for-byte
  LICENSE                  # upstream MIT license
  scenes/asimov-authority.js
  scenes/asimov-verbs.js
  scenes/asimov-twin.js
  audio/<lesson>-<nn>.wav
  lesson.json
```

`lesson.json` carries the authority marker, lesson IDs, runtime SHA-256, each
narration line's canonical voice, duration, WAV path, SHA-256, and the receipt
hash returned by the TTS CLI. The page uses `no-font` on every `<stick-scene>`
so it has no CDN dependency.

## Authority

The human is the principal. The robot is an executor. Every lesson displays:

```text
HUMAN://ROOT → æ → RECEIPT
```

A lesson build never grants authority to the agent or the robot. Each
successful synthesis writes a `TTS://SPEAK` receipt; the completed bundle
writes one `LESSON://BUILD` receipt to the same hash-chained ledger at
`$HERMES_HOME/tiny-voca-receipts.jsonl`. `tts_verify({})` validates both.

## License

Plugin packaging: Apache-2.0. Skill documentation: MIT. The upstream
stick-scene runtime remains MIT © Kamran Ahmed; its LICENSE is copied with the
bundle. `HUMAN://ROOT` is an attribution marker, not a software license.
