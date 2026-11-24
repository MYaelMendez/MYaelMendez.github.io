# Hermes.webgl — Architecture Target (locked)

Layers are cooperating components, not a mandatory sequence. Media and WASM remain optional.

- HTML controls: accessible chat, task review, Grant / Inspect / Revoke
- WebGL surface: spatial viewports, visible task state
- Worker + optional WASM: local computation without blocking UI
- Harness adapter: real Hermes runtime, local or remote
- Media pipeline: decode/render/record (WebCodecs, detected)
- Memory + witness: contributions, provenance, execution evidence

## First slice — complete only when evidence shows:
1. Task accepted by a real Hermes runtime
2. Runtime events reflected accurately in the viewport
3. Returned artifact linked to task and source
4. Receipt recording outcome, permissions, and errors
5. Cancellation/revocation actually tested

Portable engine. Responsive glass. Human authority. 💎🗝️
