# Studios and camera shots — the resource inventory

Every renderer and every camera this estate can actually call, with the real
names and parameters from the code. Grounded 2026-11-21.

## Studios (renderers)

| studio | entry | renders | cast | status |
|---|---|---|---|---|
| **asimov_studio** (v1) | `agents/asimov_studio.py --spec S --out F` | Asimov CAD body, spec-driven, tinyVOCA voice, NVENC, SupervisorVideo gate | 1 | **PROVEN** — renders + gate PASS (live `asimov-studio-model-916` lum 62.35) |
| **asimov_studio2** (v2) | `agents/asimov_studio2.py --spec S --out F [--verify]` | one or two bodies, dialogue, camera presets | 2 | BUILT — renders; **output too dark** (live film lum 11.08, floor 20) |
| **asimov_studio3** (v3) | `agents/asimov_studio3.py --spec S --out F [--verify]` | five bodies, per-actor voices, face camera + face tablet | 5 | BUILT — **~12 s/frame**, not dependable |
| **rtx_studio** | `agents/rtx_studio.py --spec S --out F` | whole Asimov on the RTX via CuPy RawKernels (no OpenGL) | 1 | BUILT — deterministic |
| **asimov_pet** | `agents/asimov_pet.py --model-dir D --out F` | CAD pet atlas, 9 states × 6 frames, 192×208 | 1 | BUILT |
| **tinyasimov film** | `tinyasimov/tinyasimov.py film out.mp4` | walk + voice + gate + receipt | 1 | BUILT |
| **proof1** (PROOF/1) | `proof/proof1.py <name>.proof.json` | receipted montage from our own media assets | n | **PROVEN** — CHAIN/09, ORACLES/09 |
| **videolab render** | `videolab/render.py render <scene>` | telemetry-driven scene (mesh-addressable) | — | BUILT |
| **æRTXrender** | `store/mp4-factory-app/render.mjs` | HTML surface → MP4 via Chrome CDP | — | PROVEN |

## Camera shots

### v1 — free camera, spec parameters (no named presets)
`distance` 2.35 · `elevation` -4 · `azimuth` 104 (+ `sway` 8·sin).

### v2 — 8 presets
| name | az | el | dist | look |
|---|---|---|---|---|
| `front` | 180 | -3 | 3.0 | 0.70 |
| `three_quarter` | 155 | -4 | 3.0 | 0.70 |
| `side` | 90 | -3 | 3.0 | 0.70 |
| `back` | 0 | -3 | 3.0 | 0.70 |
| `low` | 180 | -14 | 2.8 | 0.55 |
| `high` | 180 | 16 | 3.2 | 0.80 |
| `close` | 180 | -2 | 1.9 | 1.02 |
| `orbit` | 180 | -3 | 3.0 | 0.70 (orbit 22) |

### v3 — 9 presets
All of v2 except `close`, plus:
| name | az | el | look | dist | notes |
|---|---|---|---|---|---|
| `orbit` | 180 | -3 | 0.70 | cast | orbit 20 |
| `face` | 180 | -2 | 0.03 | 0.62 | tracks the speaker |
| `pilot` | 180 | -2 | 0.30 | 1.55 | tracks `waetz` |

`DIST_BY_CAST`: solo 2.35 · pair 3.0 · five 4.8.

### rtx_studio — spec parameters
`azimuth` 0 (+ 4·sin sway) · `distance` 2.5 · `lookat_z` 0.95 · `fov` 45.

### emoji_scene — emoji-addressed camera
`az`, `el` derived from the emoji seed; `dist` 5.6 · `fov` 42.
Motion families: `orbit` | `pulse` | `drift` | `spin`.

## States (the robot's vocabulary)
`IDLE` · `LISTENING` · `SPEAKING` · `THINKING` · `AWAITING_APPROVAL` ·
`APPROVED` · `REFUSED` · `ERROR` — each drives head colour, yaw, pitch.

Pet rows: `idle` · `running-right` · `running-left` · `waving` · `jumping` ·
`failed` · `waiting` · `running` · `review`.

## Cast (who may speak)
`nous` (F2, magenta) · `hermes` (M2, cyan) · `waetz` (white, centre — the
learner) · `menlo` (orange) · `asimov` (green). Order: nous, hermes, waetz, menlo,
asimov.

## Choosing

- One body, must pass the gate → **v1**.
- Dialogue, two bodies → **v2** (brighten the scene first).
- Five bodies, face cam → **v3** (budget hours).
- Receipted montage from our own media → **proof1**.
- One symbol opens a film → **emoji_scene**.

## Known defects
- `asimov-studio-v2-916.mp4` is **live and fails the gate** (lum 11.08).
- v3 renders at ~12 s/frame — five bodies is the cost.
