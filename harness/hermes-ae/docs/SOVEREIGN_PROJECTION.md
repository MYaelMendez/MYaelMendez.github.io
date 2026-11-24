# Sovereign projection

Projection is not a tenth harness. It is a governed composition of the harnesses
we already have.

```text
HUMAN://ROOT → viewport + robot + ffmpeg + publish → projection → receipt
```

| Principle | Implementation |
|---|---|
| Authority precedes capability | manifest authority is `HUMAN://ROOT`; every op receipts |
| Harnesses compose; plugins package | package uses viewport, robot, ffmpeg, publish, ledger |
| Live capture is pinned; replay is deterministic | hashed screenshots and face media feed a PIL/ffmpeg renderer |
| Receipts are proof | `PROJECTION://VERIFY`, `PROJECTION://RENDER`, publish receipts |
| QC fails closed | authority text, no scripts, no runtime fetch, theme vars, media, video specs, ledger chain |
| Aesthetics stay human | visual QA is reported, not automated away |

## Ops

```json
{"op": "projection"}
{"op": "projection_render", "publish": false}
```

## Limits

- Face states are displayed, not wired to a live approval gate.
- The demo is silent; two-voice narration remains optional.
- Custom-domain serving is user-side; raw URLs are the verifiable path.

Published package SHA-256: `9eb268e792feab671cdbb6e720f38a38aa6eeb86d7f9fde4b210df52ccbb0b8d`.
