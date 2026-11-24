# tinyVOICE starter examples

- `consent.template.txt` — explicit `VOICE://BIND` consent template.
- `prompt_text.template.txt` — exact-transcript template for VoxMel cloning.
- `sovereignty.zh.json` — Chinese starter script for the `SOVÆREIGN` digital-twin voice.

Run the shipped local starter:

```sh
python3 scripts/tiny_voice.py --op go
```

That produces `go.wav`, `go.json`, and two `TTS://SPEAK` receipts with tiny-voca.
VoxMel is gated until the model, Vocos, reference pair, and consent are provisioned.

`HUMAN://ROOT → æ → RECEIPT`

#opensourceware #internetofagents
