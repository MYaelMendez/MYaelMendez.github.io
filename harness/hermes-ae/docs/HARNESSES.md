# Mixture of Harnesses (MoH)

`hermes-ae` is a **plugin** that packages a **Mixture of Harnesses**. The two
words are not interchangeable:

- **Plugin = packaging.** The plugin is the unit Hermes loads: a directory of
  code, manifests, scripts, and docs behind the single `ae` tool. Packaging says
  *how the capability is shipped*.
- **Harness = governed capability envelope.** A harness is one bounded way of
  acting: it declares its runtime, the inputs it accepts, the outputs it may
  emit, the receipt action it writes, and the fallback it takes when its runtime
  is unavailable. A harness says *what the capability is allowed to do, and how
  that action is proven*.

A model can answer questions. A harness is what lets an agent **act** with a
runtime, under an authority, and leave a verifiable proof. Routing among the nine
harnesses is the Mixture of Harnesses: `ae` selects the envelope, the envelope
constrains the action, and the ledger records it.

## The opensourceware formula

> **mechanism + authority + receipt = opensourceware**

- **mechanism** — the harness runtime and its declared envelope (the *how*).
- **authority** — every harness is rooted at `HUMAN://ROOT`; the human is the
  origin of permission (the *who*).
- **receipt** — every action writes a `HUMAN://ROOT` entry to the unified
  hash-chained ledger (the *proof*).

Source, authority, and proof are all inspectable. That is what makes the result
opensourceware rather than merely open-source code.

## The nine harnesses

| Harness | Runtime envelope | Inputs → outputs | Receipt action |
|---|---|---|---|
| `voice` | tiny-voca ONNX (nous-girl F2 / hermes-agent M2, 24 kHz) | text, voice, speed → wav, visemes | `TTS://SPEAK` |
| `ffmpeg` (alias `media`) | ffmpeg + ffprobe, libx264/aac | frame sequence, audio, profile, QC policy → mp4, probe and volume reports, sha256 | `VIDEO://RENDER` |
| `control` | vlc-mesh | media URI, command → playback state | `VLC://CONTROL` |
| `physics` | MuJoCo 4.0.1 (nu=25) | model, qpos, controls → trajectory, qpos series | `PHYSICS://STEP` |
| `viewport` | Three.js / WebGL qpos viewer | qpos series, meshes → frames, camera | `VIEWPORT://RENDER` |
| `robot` | hermes-asimov / Asimov-1 (25-DOF) | pose, gait → qpos, end-effector states | `ROBOT://POSE` |
| `publish` | GitHub Pages + generate_gallery | artifacts, gallery repo → URL, index | `PUBLISH://GALLERY` |
| `course` | two-voice open courses (tiny-voca F2/M2) | lesson JSON, voice map → course mp4, receipt | `COURSE://<ID>` |
| `ledger` | unified hash-chained ae-receipts.jsonl | action, authority, payload → receipt, chain head | `LEDGER://APPEND` |

The machine-readable source of truth is `harnesses.json` at the repository
root. Each entry there carries the full `name`, `authority`, `runtime`,
`inputs`, `outputs`, `receipt_action`, `fallback`, and `description` fields; this
table is the human-facing summary.

## ffmpeg harness contract

ffmpeg is no longer a loose utility. It is the `media` harness promoted to a
governed envelope with the same authority chain as every other harness:

```text
HUMAN://ROOT → ae → ffmpeg harness → frames + audio → H.264/AAC artifact → receipt
```

| Field | Value |
|---|---|
| Name | `ffmpeg` |
| Alias | `media` |
| Authority | `HUMAN://ROOT` |
| Runtime | ffmpeg + ffprobe, libx264/aac profile |
| Inputs | frame sequence, audio tracks, codec profile, QC policy |
| Outputs | mp4, probe report, volume report, sha256 |
| Receipt action | `VIDEO://RENDER` |
| Fallback | fixed libx264/aac pipeline without agentic repair; degraded mode recorded in receipt |

Inspect it with:

```json
{"op": "harness", "name": "ffmpeg"}
{"op": "ffmpeg"}
{"op": "run_harness", "chain": ["voice", "ffmpeg", "ledger"]}
```

Run the proof clip with `ae({"op":"ffmpeg_demo"})`. It shows Asimov walking
front-facing while `hermes-agent` narrates
`FRAMES → ENCODE → PROBE → WITNESS → RECEIPT`, produced by the same ffmpeg
harness it describes.

The harness probe verifies ffmpeg/ffprobe versions and required encoders before
declaring readiness. Video acceptance still fails closed on duration, frame
count, codec, audio levels, bright pixels, sha256, and ledger linkage.


## Contract of a harness

Every harness declares:

1. **authority** — always `HUMAN://ROOT`.
2. **runtime** — the concrete mechanism it may invoke.
3. **inputs / outputs** — the capability envelope; nothing outside it is
   implicitly permitted.
4. **receipt_action** — the action tag written to the ledger for each run.
5. **fallback** — the degraded but still receipted behavior when the runtime is
   unavailable.

Fallbacks are part of governance: a harness never silently fails. It degrades to
a declared mode and records that mode in the receipt, so the proof remains
honest about what actually ran.

## See also

- [Receipts](RECEIPTS.md) — the `HUMAN://ROOT` hash-chained ledger.
- [Receipt chain](RECEIPT_CHAIN.md) — a sanitized snapshot of real entries.
- [Open courses](COURSES.md) — the two-voice lesson template.
- [The v3.0.0 masterpiece target](MASTERPIECE.md).
