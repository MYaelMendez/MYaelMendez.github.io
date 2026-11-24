# tinyTELEPROMPTER

`tinyTELEPROMPTER` is a 9:16 narrated prompt surface powered by tinyVOCA. It turns
a deterministic script JSON into a self-contained HTML teleprompter with
TTS-synced lines, keyboard controls, progress/ETA, and hash-chained receipts.

It is a **command glass**, not an authority source. It queues and presents human
intent; it does not sign. `HUMAN://ROOT` remains root.

## Tool

```text
tts_teleprompt({"op":"list"})
tts_teleprompt({"op":"build","script":"sovereignty","out":"..."})
tts_teleprompt({"op":"build","script":"asimov-voice-map","out":"...","speed":1.25})
```

`script` also accepts a path to a custom JSON file:

```json
{
  "title": "My script",
  "subtitle": "tinyVOCA powered",
  "lines": [
    {"voice": "F2", "text": "The human decides."},
    {"voice": "M2", "text": "The agent asks, then executes."}
  ]
}
```

## Output

```text
out/
  index.html      # self-contained 9:16 teleprompter
  audio/00.wav…
  script.json     # durations, voice IDs, SHA-256, receipt hashes
```

## Controls

- `Space` — play/pause
- `←` / `→` — previous/next line
- `+` / `-` — speed
- `R` — reset
- Line picker — jump to any line
- **VOICE** — toggle tinyVOCA narration on/off
- **Aa** — cycle font size

The active line is highlighted inside a horizontal read band at 42% height.
Progress, line number, ETA, speed, and the current line's receipt hash stay
visible in the footer. Reduced-motion preference is honored.

## Receipts

Each line is synthesized through the tiny-voca CLI and writes a `TTS://SPEAK`
receipt. The completed build writes one `PROMPT://BUILD` receipt to the same
hash-chained ledger. `tts_verify({})` validates the whole chain.

## Design notes

The prototype audit found the key UX failures: vertical guide lines cutting
through text, empty start states, unlabeled controls, CDN-dependent fonts/QR
codes, and no ETA. tinyTELEPROMPTER fixes those with a horizontal read band,
active-line highlighting, deterministic local assets, explicit controls, and
real receipts.

`HUMAN://ROOT → æ → RECEIPT`

#opensourceware #internetofagents
