# Asimov Avatar — USD Digital Twin

`asimov-avatar` is the USD projection of the official Asimov-1 body. It is authored from source, not invented geometry.

```text
HUMAN://ROOT → æ → Asimov Agent → asimov-avatar.usda → RECEIPT
```

## What ships

Package: `packages/asimov-twin/1.0.0/`

| File | Role |
|---|---|
| `asimov-avatar.usda` | USD ASCII stage: 26 link frames, 25 governed joints, 216 qpos frames |
| `manifest.json` | Hashes, counts, source provenance, receipt action |
| `meshes/*.STL` | 26 official Asimov-1 mesh references |
| `model/` | Copies of URDF, MJCF, and qpos trace |
| `README.md` | Quick package note |

## Contract

- `authority`: `HUMAN://ROOT`
- `source`: `menloresearch/asimov-1`
- `format`: USD ASCII
- `upAxis`: Z, `metersPerUnit`: 1
- `timeCodesPerSecond`: 24
- `receipt_action`: `AVATAR://USD_BIND`

The stage contains a `defaultPrim` `/Asimov`, link Xforms, nested joint Xforms with `inputs:qpos` time samples, and relative mesh assets. The mesh geometry stays in referenced STL files in this first slice.

## Ops

```json
ae({"op":"twin","action":"build"})
ae({"op":"twin","action":"verify"})
ae({"op":"twin","action":"info"})
```

`build` is reproducible: same URDF, MJCF, qpos trace, and mesh hashes produce the same stage hash.

## Verification

The bundled verifier checks header, default prim, authority marker, stage hash, link count, joint count, time samples, and mesh presence. With `usd-core` installed, the stage also opens in `pxr.Usd.Stage` with 52 Xforms, 1 Scope, 25 joint prims, and 216 qpos samples per joint.

## What this is not

This is a **robot digital twin**, not yet an NVIDIA ACE skinned human avatar. Omniverse/ACE avatar work still needs a self-contained USD with geometry, `SkelRoot` / `Skeleton` / `SkelJoints`, and retargeted human joints. This package is the honest first slice: transform hierarchy, governed joints, real qpos replay, mesh references, and receipts.
