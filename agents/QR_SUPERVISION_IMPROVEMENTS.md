# Potential improvements — qr supervision

Ranked by **actual risk**, verified against the code, not speculated. Each item
below was reproduced before being written down; where a suspicion turned out to
be already handled, it says so.

---

## CRITICAL

### 1. The gate is not reachable from a running agent

`qr_supervision.py` is a module + CLI. Nothing calls it automatically.

`qr_kanban.mint_card()` supervises — but **only because it imports the module
directly**. `qr_mail.py`, `qr_sms.py`, `contract_qr.py`, `qr_key_manager.py`, and
every other producer still render QR with no gate. They are exactly as exposed to
the §5.3 failure class as `qr_kanban` was before this change.

**Fix:** register `qrsupervision://` in the conductor and route every QR render
through it. Until then the gate protects one caller, not the pipeline.

**Status:** the contract doc exists; the scheme is not registered.

---

### 2. SMS reassembly can silently corrupt an envelope

Verified. Two multi-segment messages with the **same** chunk count interleave and
`reassemble()` produces a **spliced envelope that still passes `is_envelope()`
and decodes without error**:

```
msg1 = 3 segs, msg2 = 3 segs
reassemble([s1[0], s1[1], s2[2]])  ->  len=310, != msg1, != msg2
    looks valid? True
    decodes as route: {'cmd': 'kanban://list AAAA…'}
```

The chunk marker `ae:1:<type>:chunk:<i>/<n>:<part>` carries **no message
identifier**, so chunks from different messages with the same N are
indistinguishable. `reassemble()` refuses *incomplete* sets (6/3 → error) but
cannot detect *mixed* sets.

This is worse than a failure — it is a **wrong-but-valid** result. A secret or a
route command can be silently corrupted into another plausible one.

**Fix:** add a per-message id to the chunk marker:
`ae:1:<type>:chunk:<msgid>:<i>/<n>:<part>`, and make `reassemble()` group by
`msgid` and refuse a set containing more than one. ~15 lines in `qr_sms.py`.

**This is the highest-value fix on the list**, because the failure is silent and
the affected domain is secrets.

---

### 3. Kanban cards are unauthenticated

Verified: `qr_kanban.py` contains **no** signature check. Any QR with a valid
`route` envelope dispatches a board mutation. A photograph of someone's card, a
printed copy, a screenshot — all work.

`contract_qr.py` already ships `sign_contract()` / `verify_contract()` /
`verify_signature_raw()` (Ed25519), and the `capability` envelope type exists for
exactly this. The pieces are present and unwired.

**Fix:** sign the card payload at mint; verify at read. The `capability` type
carries `{grant, subject, expires}` — a card should be a signed capability, not a
bare route.

**Status:** not started. Auth infra exists; integration does not.

---

## HIGH

### 4. The receipt chain does not chain

`_chain()` is called once with `""` as the previous value:

```python
receipt.chain = _chain("", {"kind": kind, "attempt": attempt}, …)
```

So each receipt is a self-contained hash, not a link in a chain. Two receipts for
the same artifact are indistinguishable from two independent runs; there is no way
to prove *order* or detect *omission*.

**Fix:** persist the last chain value (a receipt log) and seed `prev` from it. The
hash function is already shaped for it — only the plumbing is missing.

### 5. `module_size` is a hardcoded proxy, not the real version

```python
modules_side = 21  # conservative floor (v1)
mod = edge / modules_side
```

The check divides the detected edge by **21** regardless of the actual QR version.
A v10 code (57 modules) reports a module pitch ~2.7× too large, so a genuinely
too-small code can pass.

The true module count is known at render time (`qr.modules_count`) and can be
recovered from the image. Using the real value makes the check honest.

**Fix:** pass the version through, or estimate modules from the finder patterns.

### 6. Single sample per artifact — no adversarial or camera-path testing

Every check runs on **one clean, axis-aligned, synthetic PNG**. Never tested:
rotation, perspective, motion blur, glare, partial occlusion, print-then-scan,
or a phone camera. §6.3 of the paper already concedes the camera path is
unmeasured; the supervisor inherits that gap.

The paper reports a finding that cv2 loses cards on dense boards at native
resolution. The same class of finding almost certainly exists for camera capture,
and the supervisor would not catch it because it never sees a camera frame.

**Fix:** a corpus of degraded captures (rotate/blur/glare/print-scan) as a
regression suite; report the pass rate as a measured property.

---

## MEDIUM

### 7. The supervisor is not itself supervised

The checks have no tests. `selftest()` proves the rune case refuses and all eight
types pass — that is a smoke test, not a suite. A regression in `_contrast()`
would go unnoticed.

**Fix:** pytest over `supervise()` with fixtures for each refusal class
(too-small, low-contrast, no quiet zone, payload mismatch).

### 8. `MIN_QUIET_MODULES` is dead

Defined at line 59, referenced nowhere. The quiet-zone check is a binary
luminance test, not a module-count measurement, so the constant is aspirational.

**Fix:** either measure the actual border width in modules and compare, or delete
the constant so the code stops implying a check it does not perform.

### 9. Cross-decoder check depends on a non-stdlib decoder

If `pyzbar` is absent, `cross_decoder` **fails closed** — verified, and that is
the correct behavior. But it means the gate cannot run at all on a machine
without pyzbar, and the failure mode is a hard refuse rather than a degraded pass.

**Fix:** treat a missing second decoder as an explicit, loud configuration error
rather than a check failure, so the operator knows the difference between "the
artifact is bad" and "the gate is unarmed."

### 10. No concurrency guard on the board

`read_card` + `dispatch` is read-then-write with no lock. Two cameras, or one
camera seeing the same card twice inside the cooldown window, can double-dispatch.
The cooldown is time-based (8 s) and per-process — it does not survive a restart.

**Fix:** make the cooldown persistent (a seen-cards file) and make dispatch
idempotent where the verb allows.

---

## LOW

### 11. Dead code and duplicate imports

`_module_size_px` is defined but unused (the logic is inlined in `supervise`).
`import numpy as np` appears inside five separate functions. Both are harmless;
both make the file harder to read.

### 12. Rune acceptance is asymmetric

`qr_envelope.decode()` accepts the rune form for backward compatibility, but the
supervisor **refuses** it on the produce path. That is correct — but it means a
legacy rune envelope can be decoded and stored while being un-reproducible by the
gate. Worth an explicit note in the contract.

---

## What is already correct

Checked and confirmed, so it does not need work:

- **pyzbar absent → fails closed.** `cross_decoder` returns `1/2` and refuses.
  Correct, not a gap.
- **`reassemble()` refuses incomplete sets.** `6/3 segments` → `ValueError`.
  The hole is only in the *same-N mixed* case (item 2).
- **`verify-before-store` in `qr_mail`.** A probe decrypt (`open_entry(key,
  "__check__", chk)`) gates import; a blob sealed under a different passphrase is
  skipped.
- **The gate refuses the rune class.** Verified as a controlled experiment:
  identical payload, rune → REFUSED, ASCII → PASS.
- **8/8 envelope types pass; exit codes are 0/1.** Usable as a real gate.

---

## Recommended order

| # | Item | Effort | Why now |
|---|---|---|---|
| 1 | SMS message id | ~15 lines | silent corruption of secrets |
| 2 | Register `qrsupervision://` | small | gate protects one caller today |
| 3 | Sign kanban cards | medium | auth infra already exists |
| 4 | Real `module_size` | small | check currently overstates safety |
| 5 | Chain the receipts | small | hash function already shaped for it |
| 6 | Degraded-capture corpus | large | the finding class that produced §5.3 |

Items 1 and 2 are the ones I would not ship without.
