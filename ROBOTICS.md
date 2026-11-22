# æ ROBOTICS — the estate, ordered

Every piece of robotics work in `C:\æ`, ordered **by data flow** so the next
development starts from the right link. Status is `PROVEN` (measured here),
`BUILT` (in the repo, not yet measured) or `OPEN` (a known gap).

The rule: **a thing that has not been checked back is not a thing.** Every entry
below names where it lives, what it measures, and the next step.

---

## 0 · Read this first — the chain

```
custody → format → gate → authority → contract → dispatch → publish → delivery → adoption
```

Robotics work in this estate is the same chain with robot names:

| link | robotics instance | file |
|---|---|---|
| custody | the CAD + the policies | `tinygpu/model/`, `policies/` |
| format | the trace + the receipt | `tinypython/`, `proof/` |
| gate | the supervision + the verdict | `supervisionvideo/`, `tinyvision/` |
| authority | the C2 + the refusals | `tinypolicy/`, `agents/asimov_protocol.py` |
| contract | the script + the spec | `actors/actor_script.py` |
| dispatch | the actor | `tinygpugbot/` |
| publish | the truth surface | `github-pages/` |
| delivery | the pane + the pet | VLC, `hermes-plugins/asimov-pet/` |
| adoption | the self-study | `tinylab/` |

---

## 1 · THE BODY — custody *(PROVEN)*

The physical subject. Menlo's CAD, not an illustration.

| asset | where | note |
|---|---|---|
| URDF + 26 STL meshes | `tinygpu/model/` (49 MB) | 26 links, 25 joints, 1,007,041 tris/frame |
| decimated CAD | `github-pages/assets/gltf/asimov-web.glb` (5 MB) | web-sized |
| full CAD | `github-pages/assets/gltf/asimov.glb` (18 MB) | |
| browser scene | `github-pages/asimov-companion/scene/` (6.1 MB) | manifest + per-link `.bin`, `--grid 0.008` |
| other morphologies | `github-pages/assets/gltf/{kira,Xbot,Soldier}.glb` | **unused** — the heterogeneous mixture |
| Reachy Mini / microduck | `reachy_mini/`, `agents/microduck/` | upstream sources, no policy |
| policy checkpoints | `policies/` (5) | **2 runnable** (78/23), 3 partial-body refused |
| locomotion policy | `Menlo/asimov1-locomotion-0818` | sha `47f70691…88a0c`, Apache-2.0 |
| saved gait | `github-pages/asimov-gait.json`, `asimov-urdf.json` | 23 joints, 480 frames, 20 s |

**Licence:** the hardware CAD is **CERN-OHL-S-2.0** (reciprocal). A rendered atlas
inherits it; the generators are MIT. See `NOTICES.md` in the petdex kit.

**Next:** give each morphology its own policy — that is the heterogeneous mixture.

---

## 2 · THE MOTION — simulation *(PROVEN)*

| instrument | measures | status |
|---|---|---|
| `tinypython` | the policy rollout → a trace; per-segment **body-frame** verdict | 30+ tests |
| `tinymujoco` | the motion grade (reward, max diff) | 21 tests |
| `tinyonnx` | the ONNX contract, read from the file; refuses mismatches | 10 tests |
| `tinypolicy` | the mobility.foundation C2: 14 verbs, deadman gate | 11 tests |
| `tinycan` | the command bus | 18 tests |

Measured: `walk` **+3.118 m**, `stand` holds, `turn` heading change, `strafe` +0.253 m,
`set_velocity` 3/3 segments obey. Baseline travel **+4.1868 m / 12 s** reproduces
the package exactly.

**The verdict bug, fixed:** the per-segment check compared *world* axes to a
*body-frame* command. Fixed in `tinypython.py`; both policies then obey 3/3.
Retracted in `CORRECTION/01` (§56).

**Next:** the 65-scenario locomotion bench is **unpulled** — robustness is unmeasured.

---

## 3 · THE PICTURE — render *(PROVEN)*

| instrument | what it does | status |
|---|---|---|
| `tinygpu/rtx_raster.py` | CUDA rasteriser, Z-up, shadows, PBR | PROVEN |
| `tinycuda` | pixel grading | 22 tests |
| `tinycudavideo` | emoji → frames → MP4 + receipt | 22 tests |
| `agents/rtx_asimov.py` | the real CAD from a policy trace; `--free-root`, `--az/--el/--dist` | PROVEN |
| `agents/asimov_studio{,2,3}.py` | the studio scenes | PROVEN |
| `proof/proof1.py` | the PROOF/1 renderer (spec → film → gate → receipt) | PROVEN |
| `agents/mixture_composite.py` | the 2×3 mixture canvas | PROVEN |

Studios: **9** (`studios.json`, `STUDIOS-AND-CAMERAS.md`) — asimov_studio v1/v2/v3,
rtx_studio, asimov_pet, tinyasimov, proof1, videolab, æRTXrender.
Cameras: free + 8 v2 presets + 9 v3. States: 8. Cast: 5.

**The camera fix:** the renderer used to pin the root and follow the body — the film
showed the gait and erased the path (21 px vs 3.118 m). `--free-root` gives
**589 px / 189 px/m**. Retracted in §47.

**Next:** a fixed-camera *world* shot per verb, so the traversal is comparable across actors.

---

## 4 · THE VERDICT — gate *(PROVEN)*

| instrument | measures | status |
|---|---|---|
| `supervisionvidaeo/` | luminance, contrast, motion, black, QR — from scratch, no ML | PROVEN |
| `vision-supervision/` | the shim over the engine | PROVEN |
| `tinyvision` | the policy's picture: gate + one tracked blob + `agree` | 7 tests |
| `tinycontinuum` | the time axis: freeze, gap, reversal | 15 tests |
| `tinyfilmmemory` | the film ledger: hash chain, drift, tamper | 9 tests |
| `tinyplugin` | silent install failures | 6 tests |

Thresholds: luminance > 20 · contrast > 8 · motion > 0.5 · black < 5%.
**Fix the scene, never the threshold.**

**Next:** a fleet gate — N performances, N verdicts, one gate. Thresholds need
recalibration for a grid (the mixture reports a structural WARN on motion).

---

## 5 · THE AUTHORITY — control *(PROVEN as refusal)*

| surface | what it says |
|---|---|
| `tinypolicy` | 14 verbs; motion refused `ACT-001/AUTH-002/DEAD-001`; `grants: false` |
| `agents/asimov_protocol.py` | the governed verb surface + ledger |
| `github-pages/ASIMOV_PROTOCOL.md` | the protocol |
| `github-pages/AE_ROBOT_VERBS.md` | the verb catalogue |

Hard limits: **no hardware, no Menlo SDK.** `asimov_exec` stays dry-run. Motion is
never granted; presence is not permission; a signature is not a self-grant.

**Next:** bind a real human signature — today's authority is declared, not enforced.

---

## 6 · THE ACTOR — dispatch *(PROVEN)*

| piece | what it does |
|---|---|
| `actors/actor_script.py` | `actor/script/1` → cues → clips → PROOF/1 film |
| `tinygpugbot` | the actor instrument: doctor / cast / perform / ledger (9 tests) |
| `actors/mixture-of-robots.script.json` | five bodies + the authority |
| `actors/the-first-script.json` | ACTOR/01 |
| `correction/correction-01.proof.json` | CORRECTION/01 |

Rule 5: **a bot's motion is its policy's** — a verb with no trace is refused, never invented.

**Next:** a second actor is a `cast` entry and a set of traces. Add the other morphologies.

---

## 7 · THE FORM — format *(PROVEN)*

| piece | what it does |
|---|---|
| `proof/FORMAT.md` | **PROOF/1** — the receipted film format |
| `proof/proof1.py` | spec → film → gate → receipt; in-frame digest `sha256[:32]` |
| `proof/instances/*.proof.json` | the published specs |
| receipts | `<film>.receipt.json` + `.meta.json`, citation `æ://film/<name>` |

A film is data: same spec + same sources → same bytes. The citation is the hash of
the delivered bytes, not of the source.

**Next:** a second implementation. One implementation is a file format; two is a standard.

---

## 8 · THE AUDIENCE — publish + delivery *(PROVEN)*

| surface | where |
|---|---|
| truth surface | `github-pages/` → `myaelmendez.github.io` |
| the post | `the-film-is-an-instrument.html` |
| studio browser | `studios.html` |
| companion (WebGL, DOM-aware) | `asimov-companion/` |
| viewports | `asimov-viewport/`, `asimov-viewport-v2/` |
| film studio | `film-studio.html` |
| pet | `hermes-plugins/asimov-pet/` (receipted, gait-faithful) |
| the pane | VLC at `127.0.0.1:8081` — the human visual gate |

**Next:** the companion's DOM awareness is page-local; inject it over CDP for any surface.

---

## 9 · THE SELF — adoption *(PROVEN)*

| piece | what it does |
|---|---|
| `tinylab` | the recursive self-study: `study` → receipt → `change` → `next` (6 tests) |
| the family | 13 instruments, **13/13 suites**, 169 tests, no zeroes |
| `agents/agent_pledge.py` | the pledge; the gate is `require --agent <id>` |
| `AE-CONTINUITY.md` | §1–§56, the dated record of every run |

**Next:** the loop closes on process. It has never closed on physics or hardware.

---

## 10 · THE MAP — index

**Films (this arc, all live):** `verbs-09` · `loop-09` · `actor-01` ·
`mixture-performed` · `correction-01` · `proof-09` · `chain-09` · `oracles-09` ·
`showreel-09` · `gait-09` · `policy-12s` · `mobility4d` · `holomesh-4d-916` ·
`core-registry-916`(+narrated) · `mixture-of-robots-916`.

**Earlier robotics films:** `asimov-walk-916` · `asimov-policy-walk-916` ·
`asimov-standing-916` · `asimov-free-walk-916` · `asimov-talk-walk-916` ·
`asimov-studio-v2-916` · `asimov-studio-model-916` · `asimov-dialogue-916` ·
`menlo-asimov-5s-916` · `tinyasimov-3s-916` · `robot-policy-studio-916` ·
`mixture-6panel-10s-916` · `moh-masterpiece-916` · `rtxmp4-raster-916`.

**The three things that are true and matter:**
1. The film is an **instrument** — the picture can contradict the physics.
2. The laboratory **grades itself** and instructs its own repair.
3. The robot is a **scripted actor** whose motion is its policy's.

**The three things that are not true:**
1. No hardware moved. Every number is a simulation trace.
2. The policies are Menlo's. We run them; we do not own the locomotion.
3. The loop closes on process, not physics.

---

*æ:// · GOVERNANCE AND PROVENANCE LABORATORY · #opensourceware*
