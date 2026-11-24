# æQR

**Resource addressing, verification, and audit for the æ constellation.**

æQR is one discovery layer across many resources — **without making every
resource public**. A QR is an address into the constellation, not permission to
access or execute. Integrity is proven by decoding the artifact back; authority
stays with the human.

> Scan → resolve resource → verify integrity → request authority → act.

Part of **Private Client AI** — the operator-owned interface to its agents,
compute, resources, and workflows. Private execution and secrets stay local.
GitHub.io is the published surface; it is not the runtime or the custody layer.

## What it is (and is not)

| It is | It is not |
|---|---|
| A registry of stable resource IDs → canonical routes + scope | A permission system |
| A produce-and-verify gate for QR artifacts (two real decoders) | A renderer that trusts its own bytes |
| A deterministic audit → snapshot → compare → repair queue | A claim that a fix landed |
| An explicit, default-deny authority model | An implicit grant from scanning |

## The pieces

| Module | Role |
|---|---|
| `ae/envelope.py` | the typed transport: `ae:1:<type>:<b64url(json)>` (8 types) |
| `ae/supervision.py` | SPEC → RENDER → SUPERVISE → (receipt \| refuse), 9 measurable checks, **cv2 AND pyzbar must agree** |
| `ae/registry.py` | stable IDs → canonical routes + scope (`public`/`local`/`private`/`hybrid`) |
| `ae/orchard.py` | audit → snapshot → compare → repair queue; planning ≠ verification |
| `ae/authority.py` | scanning never grants execution; gated actions require a capability |
| `ae/cli.py` | one command surface |

## Install

```bash
pip install -e ".[dev]"
```

Runtime deps: `qrcode`, `pillow`, `numpy`, `opencv-python`, `pyzbar`.
On Windows the QR gate runs under the GPU python (`C:/gpu/Scripts/python.exe`),
which has cv2/numpy/qrcode/pyzbar.

## Use

```bash
# the registry — 278 resources, 9 categories
aeqr registry --category threejs_scenes
aeqr resolve html-surfaces-teologia-calendar

# produce a QR only if it decodes back through two real decoders
python -m ae.supervision produce secret '{"name":"K","blob":{"n":"a","ct":"b"}}' --out k.png
python -m ae.supervision selftest        # proves it REFUSES the rune class

# audit a tree of HTML for inline-script syntax failures
aeqr orchard audit C:/æ/github-pages
aeqr orchard queue C:/æ/github-pages     # findings -> ordered repair tasks

# authority is default-deny for effectful actions
aeqr authority publish --id teologia-index            # denied
aeqr authority read --id teologia-index               # allowed
aeqr authority publish --id teologia-index --grant publish:teologia-index   # allowed
```

## The two load-bearing rules

1. **A QR that has not been decoded back is not a QR — it is a picture of one.**
   The gate decodes through **two** independent decoders. The rune magic `æ:`
   encodes fine and fails on scan (pyzbar mangles the UTF-8 bytes); a
   single-decoder check passes exactly the artifact that fails in the field.
   The transport magic is ASCII (`ae:`); the æ identity lives in the payload.

2. **Scanning never grants execution.** `resolve`, `read`, and `verify` are open.
   `publish`, `execute`, and `merge` require an explicit, scoped `Capability`.
   Planning a repair ("ready") is not proving it ("verified").

## Layout

```
ae/                 the package
  envelope.py  supervision.py  registry.py  orchard.py  authority.py  cli.py
registry/
  resources.json    269 resources, generated from the audited inventory
tests/              pytest suite (envelope, supervision, registry, authority, orchard)
docs/               the gate contract + the æQR registry contract
.github/workflows/  CI (ubuntu + windows)
```

## License

MIT — © 2026 Yæl Méndez. Open sourceware.
