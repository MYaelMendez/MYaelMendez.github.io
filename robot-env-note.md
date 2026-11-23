# robot:// — the environment, the address space, the gate

**A note on what was built, and why it is the beginning of something.**

Recorded 2026-11-22. Surfaces: `aipodcast.me` (the demo), `myaelmendez.github.io`
(the truth surface). Nothing here is a plan — everything below was executed and
measured.

---

## The through-line

Three separate threads converged on one idea: **the estate's robots stop being a
collection and become a fleet when they share an address space, a physics world,
and a gate.**

| Thread | Before | After |
|---|---|---|
| **The environment** | each robot rendered alone | **one MuJoCo world**, three bodies, one camera, one trace |
| **The address space** | three dialects, three consoles | **`robot://`**, longest-prefix routed, six bodies, one fleet receipt |
| **The gate** | films published because they existed | **produce → Receipt, or refuse**; a failing film is not published |
| **The mesh bodies** | "mesh only — no dialect, no policy, no ledger" | **`meshbot://`**, seven routes, refusals named not crashed |
| **The destination** | films scattered across the estate | **`aipodcast.me`**, one wired publish path |

None of these is a feature. Together they are a **governance substrate**: every
body addressable, every act recorded, every artifact gated.

---

## 1. One environment — `robot-env.mp4`

`agents/robot_env_film.py`

```
one world   nbody 64 · ngeom 307 · nq 125 · nu 23
  asimov    x -0.42   1.25 m   26 mesh geoms   1,007,041 tris   0 actuators
  reachy    x  0.00   0.39 m  173 mesh geoms     940,986 tris   9 actuators
  microduck x  0.42   0.26 m   81 mesh geoms     980,836 tris  14 actuators
camera (0,-3.2,0.85) → (0,-0.05,0.38) · 720×1280 · 24 fps · seed 0
```

MuJoCo supplies the geometry; **tinyCUDA's CuPy raster** supplies the pixels. No
OpenGL — this Optimus laptop has no registered NVIDIA ICD, so MuJoCo's own
renderer is unusable here.

**Gate: PASS.**

```
luminancia_media  43.7   (> 20)
contraste_medio   43.98  (> 8)
movimiento_medio  1.216  (> 0.5)
frames_negros     0 / 5
```

Two defects were found by measurement, not by looking:

1. **Depth stagger only reads at one distance.** Robots placed at
   y = 0 / −1.15 / −0.80: move closer and the forward body fills the frame while
   the other two leave it. They now stand on **one plane, in a line**.
2. **A 9:16 frame holding three bodies of different sizes is mostly
   background**, and the gate measures the frame. A **ground plane** was added.
   Testing it exposed a silent raster defect: the CuPy raster **drops triangles
   past a screen bound** — `half=3.0` draws, `half=6.0` disappears with no error.

Tests: `agents/test_robot_env_film.py` — 6/6, including *the trace is byte-identical
for a seed and differs for another*.

---

## 2. One address space — `robot://`

`agents/robot_protocol.py`, `agents/robot_bridge.py`, `github-pages/robots.html`

Six bodies. Every dialect keeps its own verbs; `robot://` is the single front
door and adds a fleet receipt on every route.

```
robot://asimov     14 verbs   udp · hybrid · livekit · sim     100%
robot://reachy     27 verbs   daemon · sim · mujoco           100%
robot://microduck  22 verbs   ble · udp · webrtc · sim         100%
robot://Soldier     7 verbs   mesh                             71%
robot://Xbot        7 verbs   mesh                             71%
robot://kira        7 verbs   mesh                             71%
```

**The rule the index encodes:** *whatever is built for one robot is provided for
all — a missing verb is a named refusal, never a crash.*

So the mesh bodies got the same seven routes. `meshbot://` reports what is on
disk (Soldier: 4 clips — Idle, Run, TPose, Walk; Xbot: 7 clips; kira: rigged, no
clips) and refuses the rest by name:

```
plan animate walk   → allow    render plan, no hardware
plan animate nope   → refused  "Xbot has no clip 'nope'"
sim Walk            → refused  "no physics model — mesh only"
exec walk           → refused  "no actuators and no body — mesh only"
```

**Coverage is 71%, not 100.** `sim` and `exec` are genuinely absent, and the
roster shows `·` for them. Declaring them "provided" would have been exactly the
false claim the page warns about.

Fleet ledger: `robot://fleet/ledger` anchors all dialect ledgers into one
`combined_sha256`, so a fleet action is itself recorded.

---

## 3. One gate — produce, or refuse

`agents/publish_robot_env.py`

The gate runs **first**. PASS → receipt + copy + manifest entry. FAIL → REFUSED
receipt, nothing copied, exit 1.

**The gate is never adjusted to fit the film.** When a film fails, the scene is
fixed and the film is re-made. That is why the ground plane exists and why the
stagger was removed — the first cut failed, and the failure was real.

---

## 4. One destination — aipodcast.me

`github-pages/aipodcast_me/`

```
spec-robot-env.json       the spec
robot-env.mp4             the film   sha256 0a98fc6b…
robot-env-poster.png      a real frame (n=48)
robot-env.receipt.json    gate + ffprobe + supervision receipt
robot-env-demo.html       the demo
media-manifest.json       13 videos
```

---

## Links

| What | Local | Production |
|---|---|---|
| **The demo** | `http://127.0.0.1:8125/aipodcast_me/robot-env-demo.html` | `https://myaelmendez.github.io/aipodcast_me/robot-env-demo.html` |
| The film | `http://127.0.0.1:8125/aipodcast_me/robot-env.mp4` | `https://myaelmendez.github.io/aipodcast_me/robot-env.mp4` |
| The receipt | `http://127.0.0.1:8125/aipodcast_me/robot-env.receipt.json` | `https://myaelmendez.github.io/aipodcast_me/robot-env.receipt.json` |
| The spec | `http://127.0.0.1:8125/aipodcast_me/spec-robot-env.json` | `https://myaelmendez.github.io/aipodcast_me/spec-robot-env.json` |
| Fleet index | `http://127.0.0.1:8125/robots.html` | `https://myaelmendez.github.io/robots.html` |
| Fleet data | `http://127.0.0.1:8125/robots/index.json` | `https://myaelmendez.github.io/robots/index.json` |
| This note | `http://127.0.0.1:8125/robot-env-note.html` | `https://myaelmendez.github.io/robot-env-note.html` |

Local server: `python agents/serve_pages.py C:/æ/github-pages 8125`
(Range-capable — Python's `http.server` answers 200 to every Range request,
which stalls Chrome's media stack.)

---

## Honest limits

- **Film playback was not verified in the automation browser.** It reports
  `document.visibilityState === 'hidden'`, and Chrome suspends media loading for
  hidden documents — the `<video>` never issues a request. The bytes are
  reachable, and the film is verified by the gate, by ffprobe, and by an
  extracted frame. Playback in a visible tab is expected but unmeasured there.
- **`media-manifest.json` reports `all_pass: false`** — from five older entries
  that carry no `vision` block. Pre-existing, not this film.
- **Xbot and Soldier ship animation clips and nothing plays them yet.**
  `meshbot://` plans them; rendering them is the next link.
- **Nothing is pushed.** Every artifact above is local. Publishing is a separate,
  explicit step.

---

## Why this is the beginning

The estate's robots were **things on disk**. They are becoming **bodies in an
address space**: addressable by one scheme, standing in one world, recorded in
one ledger, published through one gate.

That is the difference between a project and a platform. The next links are
obvious once the substrate exists: play the clips, give the mesh bodies physics,
drive the fleet from one console, and let the gate decide what ships.
