# Sovereign Projection

A governed public projection of the capability stack.

```text
HUMAN://ROOT → viewport + robot + ffmpeg + publish → projection → receipt
```

This is not a tenth harness. It is a composition of existing harnesses that
turns invisible governance into a viewable, playable, receipted artifact.

## First principles

1. Authority precedes capability.
2. Harnesses compose; plugins only package.
3. Live capture is pinned as hashed inputs; replay is deterministic.
4. Receipts are the proof, not the marketing.
5. QC fails closed; humans judge aesthetics.

## Run

```bash
python3 scripts/sovereign_projection.py '{"action":"verify"}'
python3 scripts/sovereign_projection.py '{"action":"render","publish":false}'
```

## Boundaries

No runtime API calls in the published HTML. No full-DOM dump. No live approval
gate wired to the face states. No institutional endorsement claimed.
