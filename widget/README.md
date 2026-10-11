# æ://widget — the portable, verifiable widget package

**Print → scan → inspect → authorize → run → share.**

A QR is only an **address**. It points at a *manifest*. The manifest carries
hashes. The human authorizes. This is capability-based security: the QR is a
capability *reference*, not the capability itself — it can be forged, copied or
stale, and it does not matter, because trust comes from re-hashing the module
and comparing to the manifest, **independently of the QR**.

## What a widget package contains

```
widget/
├── manifest.json          identity · capability · interface · trust
├── widget.html            the spatial interface (Three.js r147 UMD)
├── dist/
│   └── widget_compute.wasm  the computation layer (Rust → wasm32)
├── wasm/widget_compute/   the Rust source that builds the .wasm
├── verify_widget.py       trust, checked independently of the QR
├── make_widget_qr.py      renders the manifest envelope as a QR
├── widget.envelope.txt    the æ:// envelope the QR carries
└── widget-qr.svg          the printed address
```

## The manifest (four sections)

| Section | Carries | Example |
|---|---|---|
| **identity** | who published it | `id`, `version`, `publisher`, `glyph` |
| **capability** | what it computes | `wasm.module`, `wasm.hash`, `exports`, `inputs`, `outputs` |
| **interface** | how it looks | `scene`, `controls`, `viewport` (9:16), `renderer` |
| **trust** | what it may do | `permissions[]`, `module_hash`, `authority: human` |

## Trust model — checked independently of the QR

`verify_widget.py` re-hashes `dist/widget_compute.wasm` and compares it to
`trust.module_hash`. It never trusts the QR bytes.

```
$ python verify_widget.py
æ://widget/kaenbaen-widget@1.0.0  (publisher: yaelmendez)
  module     : dist/widget_compute.wasm
  declared   : 00d5500a58f66441d0318181da9061f9d36538e0c86c296960be3fd158bb7f2f
  actual     : 00d5500a58f66441d0318181da9061f9d36538e0c86c296960be3fd158bb7f2f
  permissions: wasm:instantiate, render:webgl, fetch:localhost
  ✓ VERIFIED  — hash verified
```

Tamper one byte of the module and the same command returns `✗ REJECTED`.

## The WASM ↔ Three.js bridge

- **WASM computes** — `wave(x, y, t, seed)` returns a deterministic scalar in
  `[-1, 1]`; `answer()` is the liveness probe.
- **Three.js displays** — every vertex of a 64×64 plane is displaced by
  `wave()`; the mesh *is* the computation, not a decoration.
- **Determinism** — same `(x, y, t, seed)` always yields the same frame, so the
  widget is reproducible and the `__renderFrame(i, total)` hook drives it headlessly.

`widget.html` verifies the module hash in-browser (`crypto.subtle`) *before*
instantiating — a module that fails verification is never run.

## Build & run

```bash
# 1) build the WASM (needs rustup target add wasm32-unknown-unknown)
cd wasm/widget_compute && cargo build --target wasm32-unknown-unknown --release
cp target/wasm32-unknown-unknown/release/widget_compute.wasm ../../dist/

# 2) verify trust (independent of the QR)
python verify_widget.py

# 3) render the QR that addresses the manifest
python make_widget_qr.py     # -> widget-qr.svg

# 4) serve and open
#    (any static server rooted at C:/æ)  ->  /widget/widget.html
```

## The flow

```
Print → Scan → Inspect → Authorize → Run → Share
  │       │        │          │          │       │
  │       │        │          │          │       └─ result gets its own receipt/QR
  │       │        │          │          └─ WASM + Three.js, hash-verified first
  │       │        │          └─ human approves the declared permissions
  │       │        └─ fetch manifest → show identity / capability / trust
  │       └─ camera reads the æ:// manifest envelope
  └─ QR on paper or screen (widget-qr.svg)
```

**Share capability. Preserve human authority.**
