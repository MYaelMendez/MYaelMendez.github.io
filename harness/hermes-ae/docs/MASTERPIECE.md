# The v3.0.0 Masterpiece

> **Status: released in v3.0.0.** The film, course, hero page, harness registry,
> and receipts described below were produced by `ae({"op":"masterpiece"})` and
> verified before the release commit.

The masterpiece is the capstone of the Mixture of Harnesses: a single authored
command that composes several governed harnesses into one receipted, publishable
deliverable. It demonstrates the opensourceware formula end to end — mechanism,
human authority, and public proof in one chain.

## One command

```text
ae({"op": "masterpiece"})
```

The command orchestrates the registry in `harnesses.json` under `HUMAN://ROOT`:

- **voice** narrates with the two OpenSourceWare voices (nous-girl F2 and
  hermes-agent M2) via tiny-voca ONNX.
- **robot** + **physics** drive the 25-DOF Asimov-1 through MuJoCo 4.0.1
  (nu=25).
- **viewport** renders the qpos trace as 9:16 Three.js/WebGL frames.
- **media** encodes and QC-gates the film with ffmpeg-agentic.
- **course** renders the companion two-voice lesson.
- **publish** generates and publishes the hero page and gallery.
- **ledger** signs every step into the unified hash-chained `ae-receipts.jsonl`.

## Intended deliverables

| Deliverable | Description |
|---|---|
| Hero film | `moh-masterpiece-916.mp4` — a 30-second, 9:16 showcase film composed from the harness registry. |
| Course | `osw-103` — "The Harness Ontology", a two-voice lesson (F2 / M2) at speed 1.25, 30 seconds. |
| Harness registry | `harnesses.json` — the machine-readable registry of the nine harnesses. |
| Hero page | A GitHub Pages hero page that embeds the film and links the registry, course, and receipts. |
| Receipt proof | A `HUMAN://ROOT` hash-chained set of entries in `ae-receipts.jsonl` covering every step. |

## Acceptance criteria (target)

These are the checks the deliverable must pass. They are criteria to be met, not
results already observed.

| # | Check | Target | Status |
|---|---|---|---|
| 1 | Single entry point | One `ae({"op": "masterpiece"})` call drives the full composition | planned, not run |
| 2 | Hero film | `moh-masterpiece-916.mp4` exists, 9:16 (720×1280), ~30 s, passes ffmpeg QC | planned, not produced |
| 3 | Course | `courses/osw-103.json` is a valid two-voice lesson (F2/M2), 8–10 segments, 30 s | planned, not generated |
| 4 | Harness registry | `harnesses.json` lists exactly nine harnesses with all required fields | planned, not verified |
| 5 | Hero page | Published page embeds the film and links registry, course, and receipts | planned, not published |
| 6 | Authority | Every action attributed to `HUMAN://ROOT` | planned, not attested |
| 7 | Receipt proof | All steps appear in the hash-chained ledger and `verify` passes | planned, not verified |

## Verification

When the masterpiece is actually produced, proof is established by running the
receipt verification op and confirming that the chain resolves from `GENESIS`
with `HUMAN://ROOT` attribution, and by QC-ing the film with ffprobe. Until then
this page documents the intended shape of that proof only.

## See also

- [Mixture of Harnesses](HARNESSES.md) — plugin vs. harness and the nine envelopes.
- [Open courses](COURSES.md) — the two-voice template used by `osw-103`.
- [Receipt chain](RECEIPT_CHAIN.md) — the ledger the proof is written to.

## Release result

| Check | Result |
|---|---|
| Film | `moh-masterpiece-916.mp4`, 720×1280, 24 fps, 30.000 s, H.264 + AAC |
| Speech | 29.371 s, fits inside 30 s |
| Voices | `nous-girl` (F2) and `hermes-agent` (M2) |
| QC | mean −20.9 dB, peak −1.0 dB, 11,650 bright pixels |
| Publish | raw 200, API 200 |
| Receipt | `VIDEO://MOH_MASTERPIECE`, unified `HUMAN://ROOT` chain |

