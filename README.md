# asimov-agent

The coherent delivery of the Asimov volume: one authority chain, one head, one body, one environment, one ledger.

Authority: `HUMAN://ROOT → æ → ae → RECEIPT`

## Canonical surfaces

- Head lab: https://myaelmendez.github.io/asimov-head-lab.html
- Neon head studio: https://myaelmendez.github.io/asimov-head-webgl-neon.html
- Governed face: https://myaelmendez.github.io/asimov-governed-face.html
- Head CAD source: `cad/gltf/asimov-web.glb` → `neck_pitch_link`
- Full robot CAD: `cad/meshes/` (26 STL links) + `cad/gltf/asimov.glb`
- URDF/MJCF rig: `environments/ffmpeg-asimov/asimov_1_25dof.urdf`, `asimov_1_25dof.xml`
- Agent harness: `harness/hermes-ae/`
- Voice layer: `voice/tiny-voca/`
- Kaizen loop: `scripts/asimov_kaizen.py`, `receipts/asimov-kaizen.jsonl`

## Repository map

| Path | What it is |
| --- | --- |
| `pages/` | Delivered WebGL head surfaces and mask viewports |
| `environments/` | Three.js companion, viewport builds, RTX harness, ffmpeg/URDF rig |
| `cad/` | Official Asimov CAD: GLB, 26-link STL meshes, head700 shells, vendored Three.js |
| `plugins/` | `asimov-c2` control plugin and `hermes-asimov` SDK bridge |
| `policy/asimov-policy/` | æ policy model, agent/env YAML, ONNX policy |
| `simulator/asimov-simulator/` | Lightweight browser simulator and standing scene |
| `anim/` | Talk-walk, masterpiece, policy-physics traces and stills |
| `media/` | Receipted 9:16 films, GIFs, posters, viewport proofs |
| `docs/` | Protocol, twin, DAO brain, build plan, robotics doctrine |
| `manifests/` | Machine-readable manifests and capability state |
| `receipts/` | Hash-chained `ae-receipts.jsonl` and `asimov-kaizen.jsonl` |
| `scripts/` | Build/review/poster scripts |

## Run

```bash
python3 scripts/asimov_kaizen.py build
python3 scripts/asimov_kaizen.py review < review.json
python3 scripts/asimov_kaizen.py status
```

Serve any page over HTTP, not `file://`:

```bash
python3 -m http.server 8000 --directory .
# open http://127.0.0.1:8000/pages/asimov-head-lab.html
```

## Source lineage and licenses

- Menlo Research Asimov-1 CAD/URDF/MJCF: CERN-OHL-S-2.0.
- `harness/hermes-ae`: MIT, see `LICENSE.harmes-ae`.
- `voice/tiny-voca`: MIT, see `LICENSE.tiny-voca`; original tinyVOCA attribution preserved.
- Generated films/posters/scripts: MIT unless a source directory says otherwise.
- `æ` is the authority axis, not decoration. Agents execute under human approval; receipts stay public; authority is not transferable.

## Remote

Canonical remote: `git@github.com:MYaelMendez/asimov-agent.git`

Snapshot branch: https://github.com/MYaelMendez/MYaelMendez.github.io/tree/asimov-agent

If the canonical repository does not yet exist, create an empty GitHub repository named exactly `asimov-agent`, then:

```bash
git push -u origin main
```
