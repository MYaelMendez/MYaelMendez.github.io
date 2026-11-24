# Viewport DOM awareness

Asimov can now read a live viewport as structured DOM, not just pixels. The
`viewport_dom` op connects to a Chrome DevTools Protocol target and projects a
small, bounded snapshot:

```text
HUMAN://ROOT → ae → viewport_dom → CDP read → DOM digest → receipt
```

## Usage

```json
{"op": "viewport_dom", "endpoint": "http://127.0.0.1:9222", "match": "hermes", "selector": "main"}
```

The snapshot contains: title, URL, viewport and document size, focus, selection,
landmarks, controls, headings, `data-slot` hooks, and an optional selector probe.
It is deliberately **read-only** — no clicks, typing, or DOM mutation.

Every read emits a `VIEWPORT://DOM_AWARENESS` receipt with a SHA-256 digest of
the projected snapshot. A failed CDP connection is also receipted, with
`success:false`.

## Boundaries

- Never dump full `outerHTML`; the projection is capped at 24 landmarks, 48
  controls, 24 headings, and 48 slots.
- Match a specific page target with `match`; do not attach blindly to devtools or
  overlay targets.
- DOM facts are not visual judgement. The robot can say what is rendered; the
  human still decides whether it looks right.
- This is an OpenSourceWare capability envelope, not institutional endorsement.
