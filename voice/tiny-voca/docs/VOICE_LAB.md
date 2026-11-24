# tinyVOICE Voice Lab

The Voice Lab binds a human-approved VoxMel clone to the `SOVÆREIGN` identity and prepares the Chinese ad for the one-person company movement.

```text
HUMAN://ROOT → explicit consent → VOICE://BIND → VOICE://SPEAK → RECEIPT
```

The lab never clones a voice from a model file alone. It requires:

1. a clean WAV reference of your voice;
2. the exact word-for-word transcript of that WAV;
3. an explicit consent file containing `HUMAN://ROOT` and consent;
4. a provisioned local VoxMel runtime with model, Vocos, tokenizer, and reference pair.

## Tool

```text
tts_lab({op:"card"})
tts_lab({op:"provision"})
tts_lab({op:"bind", reference:"...", transcript:"...", consent:"..."})
tts_lab({op:"ad", out:"...", build_audio:true})
```

## Lab steps

### 1. Check readiness

```text
tts_lab({op:"card"})
tts_lab({op:"provision"})
```

The report shows whether `SOVÆREIGN` is bound and which VoxMel environment variables are missing.

### 2. Bind your voice

Prepare three files:

- `reference.wav` — clean voice sample, at least 3 seconds, 16 kHz or better.
- `transcript.txt` — exact words spoken in the WAV.
- `consent.txt` — explicit consent using `examples/tiny-voice/consent.template.txt`.

Then:

```text
tts_lab({
  op:"bind",
  reference:"/path/to/reference.wav",
  transcript:"/path/to/transcript.txt",
  consent:"/path/to/consent.txt"
})
```

This writes `$HERMES_HOME/tiny-voice-lab/voice-card.json` and a `VOICE://BIND` receipt. It does **not** send audio anywhere.

### 3. Provision VoxMel

Set:

- `VOXMEL_REPO`
- `VOXMEL_MODEL_DIR`
- `VOXMEL_VOCOS_DIR`
- `VOXMEL_TOKENIZER_PATH`
- `VOXMEL_PROMPT_AUDIO`
- `VOXMEL_PROMPT_TEXT`
- `VOXMEL_CONSENT`
- `VOXMEL_PYTHON`

VoxMel requires Python 3.10–3.12, torch/torchaudio, Vocos, model weights, and the Qwen tokenizer. No weights are vendored.

### 4. Build the Chinese ad audio

The ad script is:

```text
examples/tiny-voice/chinese-one-person-company.json
```

```text
tts_lab({op:"ad", out:"/path/to/chinese-ad", build_audio:true})
```

This writes `narration.wav` and `render-plan.json`, with one `VOICE://SPEAK` receipt per line.

## Ad copy

The ad says, in Chinese:

> One person can still run a company. Use open source software to keep authority in your own hands. The human is root; agents only execute. Every action leaves a receipt. Download tinyVOCA and hermes-ae and begin your Internet of Agents. Authority is not transferable. Receipts are public.

## Default timbre

After binding, three signal-derived variants are available: `low`, `bright`,
and `broadcast`. **Broadcast** is the digital-twin default. Low and bright are
alternates. The VoxMel router reads the default from the local voice card.

## Governance

The clone is a digital twin, not the root. It never signs. It speaks only inside the bound scope, and every generated line is receipted.

`HUMAN://ROOT → æ → RECEIPT`

#opensourceware #internetofagents
