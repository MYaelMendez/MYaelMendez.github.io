# Receipts

Every `ae` call appends exactly one record to a hash-chained ledger. Finished
videos append an additional detailed record. The chain is designed to make
silent edits detectable: each entry commits to the one before it.

## Storage

- Default path: `$HERMES_HOME/ae-receipts.jsonl` (override with
  `HERMES_AE_LEDGER`).
- Format: one JSON object per line (JSONL).
- Authority marker: `HUMAN://ROOT` on every entry, attributed to human
  authorization of agent actions.

## Entry shape

```json
{
  "ts": "2026-11-17T00:00:00Z",
  "action": "AE://FREE_WALK",
  "authority": "HUMAN://ROOT",
  "prev": "<sha256 of previous entry>",
  "detail": {"ok": true},
  "hash": "<sha256 of this entry>"
}
```

- `ts` — UTC timestamp, ISO-8601 with `Z`.
- `action` — an `AE://<OP>` action for dispatcher calls, or a domain action such
  as `VIDEO://ASIMOV_STUDIO_V2` / `VIDEO://ASIMOV_FREE_WALK_916` for videos.
- `prev` — the previous entry's `hash`, or the literal `GENESIS` for the first.
- `detail` — action-specific data. Dispatcher calls record `{"ok": bool}`; video
  receipts record output path, SHA-256 of the MP4, physics parameters, phoneme
  hashes, QC results, and publish status.
- `hash` — SHA-256 of all other fields, serialized as compact JSON (`separators
  (',', ':')`) with sorted keys and `ensure_ascii=False`. The `hash` field itself
  is excluded from the digest.

## Verification

`_verify_chain()` walks the ledger from `GENESIS`, checking for each line that
`prev` equals the running head and that the recomputed digest equals the stored
`hash`. A missing or empty ledger is valid with `head: GENESIS`.

```text
ae({"op": "verify"})
ae({"op": "receipts", "limit": 10})
ae({"op": "status"})     # includes the chain summary
```

`verify` returns:

```json
{"success": true, "count": 42, "head": "<head hash>", "broken_at": null}
```

If the chain is broken, `success` is `false` and `broken_at` is the zero-based
line index where the mismatch occurred.

## Guarantees and limits

- The chain is tamper-**evident**, not cryptographically signed: anyone who can
  rewrite the ledger can recompute subsequent hashes. It proves continuity, not
  identity. Keep the ledger on trusted storage and back it up if integrity
  matters.
- `HUMAN://ROOT` is an attribution marker for human authority, not a digital
  signature.
- Concurrent writers can race on the append; treat the ledger as single-writer
  in normal operation.
- Video receipts store the MP4's SHA-256 so a published file can be matched
  against the recorded render.
