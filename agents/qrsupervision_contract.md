# qrsupervision:// — Scheme Contract Index

> Produce-and-verify for QR artifacts. The same discipline as
> **supervisionvidaeo://**, applied to the QR domain.
>
> Canonical source: `C:\æ\agents\qr_supervision.py`

---

## 1. The cycle

```
SPEC → RENDER → SUPERVISE → (PASS: emit QRReceipt) | (FAIL: raise QRRefused)
```

- The producer **proposes** a QR; the supervisor **disposes**.
- The verifier is **deterministic** — OpenCV + pyzbar + statistics, **no ML**.
  Every verdict traces to a measurable threshold, so it is auditable.
- A stage advances when its gate passes, never on a timer.
- **PASS** ⇒ `QRReceipt`; **FAIL** ⇒ `QRRefused`. There is **no code path that
  returns a path to a QR that does not decode.** That is the whole point.

---

## 2. Why this exists

The Physical Air-Gap paper (§5.3) reports a **silent failure class**: an envelope
whose magic was the rune `æ:` **encodes correctly**, renders a valid-looking QR,
and **fails on scan**. pyzbar re-interprets the two UTF-8 bytes of `æ` as
halfwidth katakana; `is_envelope()` returns false.

An in-memory `encode → decode` round trip **passes**. Only a real decoder in the
loop catches it. That failure reached a draft paper because **nothing supervised
the artifact**.

This module is the fix.

---

## 3. API surface

### `produce(kind, payload, out_path=None, *, max_attempts=2, box_size=10, ecc="M") -> QRReceipt`

Renders and supervises. Returns a `QRReceipt` **only on PASS**; raises
`QRRefused(reason, report)` otherwise.

On FAIL it retries with a larger `box_size` (a real remedy for a module-size or
contrast refusal) up to `max_attempts`. A **charset** refusal is **not retried** —
the payload itself is wrong and no rendering fixes it.

### `supervise(image_path, expect_kind=None, expect_payload=None, envelope=None) -> QRReport`

Never raises. Returns a report with per-check verdicts.

### `QRReceipt`

Emitted only on PASS. Carries `envelope_sha256`, `image_sha256`, the full report,
and a **hash chain**:

```
chain = H(prev ∥ intent ∥ ops ∥ result ∥ state ∥ evidence)
```

### `QRRefused`

Carries `.reason` (a string) and `.report` (the failing `QRReport`).

---

## 4. The nine checks

| # | Check | Threshold | Catches |
|---|---|---|---|
| 1 | `charset` | pure ASCII | **the rune class, up front** |
| 2 | `version` | envelope decodes, type known | malformed envelope |
| 3 | `roundtrip` | rendered PNG decodes back exactly | render corruption |
| 4 | `cross_decoder` | **cv2 AND pyzbar** agree | **single-decoder mangling** |
| 5 | `payload_match` | decoded == requested | wrong payload rendered |
| 6 | `type_fidelity` | decoded type == declared | type confusion |
| 7 | `module_size` | ≥ 3 px/module | too small to scan |
| 8 | `quiet_zone` | light border present | code touching the edge |
| 9 | `contrast` | (light−dark)/(light+dark) ≥ 0.35 | washed-out or inverted |

Checks 1 and 4 are the load-bearing pair: 1 refuses the rune **before** rendering,
4 refuses it **after** if anything else ever produces one.

---

## 5. Verified behaviour

The controlled experiment — **identical payload, two magics**:

| Envelope magic | Verdict | Decoders |
|---|---|---|
| `æ:1:route:…` (rune) | **REFUSED** — `charset`, `cross_decoder: 1/2` | cv2 only |
| `ae:1:route:…` (ASCII) | **PASS** | cv2 + pyzbar (2/2) |

The failure is real and the gate catches it: **cv2 decodes the rune fine, pyzbar
mangles it.** Requiring both decoders is what turns that into a refusal.

Other verified results:

- **10/10 checks** on a supervised kanban card, both decoders, hash-chained receipt.
- **8/8 envelope types** pass the gate.
- A payload mismatch is refused (`payload_match`).
- A non-envelope image is refused (`envelope`), exit code 1.
- CLI exit codes: **0 = PASS, 1 = REFUSED** — usable as a real gate.

---

## 6. Integration

`qr_kanban.py` mints cards **supervised by default**:

```python
receipt = qs.produce("route", payload, out_path=dest)   # raises QRRefused on FAIL
```

If supervision refuses, the card is **not handed back** — a card that does not
scan is worse than no card.

The read side mirrors check 4: `read_card(..., require_both=True)` accepts a card
only when **both** decoders return it, rejecting a card whose magic one decoder
mangles. Off by default (pyzbar is slower); on for a trusted board.

---

## 7. Usage

```bash
# produce (exit 0 on PASS, 1 on REFUSED)
python qr_supervision.py produce secret '{"name":"K","blob":{"n":"a","ct":"b"}}' --out k.png

# verify an existing artifact
python qr_supervision.py supervise k.png --expect-kind secret

# prove the supervisor works, including that it refuses the rune class
python qr_supervision.py selftest
```

---

## 8. The rule

> **A QR that has not been decoded back is not a QR. It is a picture of one.**

The producer proposes; the supervisor disposes; only a receipt proves a card
works. Same rule as `supervisionvidaeo://`, same reason: a broken artifact that
looks fine is the failure mode worth engineering against.
