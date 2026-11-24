# Runbook — a film from nothing to a live URL

The complete procedure. Every command here was executed and measured on the
Victus (i5-13420H, RTX 3050 6 GB, Windows 11 + git-bash). Follow it in order;
the gates are not optional and the human gate comes before the spend.

## 0. Environment (once per shell)

```bash
export HERMES_HOME="C:/Users/yaelm/AppData/Local/hermes"
export HERMES_AE_PYTHON="C:/gpu/Scripts/python.exe"   # has mujoco, numpy, PIL
export TINY_VOCA_HOME="$HERMES_HOME/tiny-voca"
SC="$HERMES_HOME/cache/scratch"
FF="$HERMES_HOME/tools/ffmpeg-7.1-nvenc/bin"          # 7.1 targets NVENC API 13.0
```

Native `C:/` paths for native tools. MSYS `/c/...` paths silently write to
`C:\c\Users\...`. ffmpeg 9.x requires API 13.1 and FAILS on driver 592.27.

## 1. Write the spec — the spec commands the film

Never edit a scene file to change a video. Copy `templates/spec-film.json`.

Scene fields: `speaker` (cast id), `state` (drives colour + face), `camera`
(`wide` | `face`), `kicker`, `lines[]`, `speak` (the spoken text — its audio
LENGTH sets the scene duration), optional `banner`, `prompt`.

Film fields: `title`, `tagline`, `footer`, `fps` (24), `separation` (0.45),
`distance` (4.5–4.8), `charge_start{}`.

The cast, fixed by role:

| id | head RGB | base voice | speed / shift / range | centroid |
|---|---|---|---|---|
| nous | 255,64,220 | F2 | 1.00 / 0.0 / 1.00 | 2663 Hz |
| hermes | 0,170,255 | M2 | 1.00 / 0.0 / 1.00 | 2906 Hz |
| wætz | 245,245,250 | M2 | 1.02 / +2.0 / 1.30 | 3491 Hz |
| menlo | 255,150,0 | M2 | 0.94 / −3.5 / 0.65 | 2363 Hz |
| asimov | 0,255,120 | F2 | 1.06 / −1.5 / 0.35 | 1459 Hz |

Spec-attach prefixes: nous `''`, hermes `b_`, wætz `c_`, menlo `d_`, asimov `e_`.
wætz is white and centre — the learner the others support.

## 2. BOARD — the human gate, ~15–21 s

```bash
C:/gpu/Scripts/python.exe C:/æ/agents/mp4_chain.py call film board "$SC/spec.json"
```

Writes a contact sheet to `$SC/preview/<spec-stem>-proof.png`, one cell per
scene at **720×1280 — identical to the film**. Returns `approved: false`.

Look at it (`vision_analyze` or your own eyes). Check: faces expressive in the
close-ups, nothing cropped, text legible, banners correct. Fix the SPEC and
re-board. Only then render. A machine PASS is never human approval.

## 3. RENDER — a background job, never a blocking call

```bash
C:/gpu/Scripts/python.exe C:/æ/agents/mp4_chain.py call receipt launch \
    charging_bay "$SC/spec.json" my-film
# → {job_id, pid, state:'running'}  returns in ~0.05 s
```

Cost model: five bodies = 245 geoms ≈ **2.2 s/frame**. A 40 s film at 24 fps is
967 frames ≈ 35 min. A solo robot is ~4× faster. `smoke=1` renders one scene
for a composition check.

Poll (do not sleep-loop in the foreground):

```bash
C:/gpu/Scripts/python.exe C:/æ/agents/mp4_chain.py call receipt status <job_id>
```

The gate runs AUTOMATICALLY on encode and records its verdict. Job files live
in `$SC/ae-renders/<job_id>/`, frames in `studio/frames/`, timings in
`studio/studio.json`.

## 4. VERIFY the deliverable, not the fix

```bash
"$FF/ffprobe.exe" -v error -count_frames -select_streams v:0 \
  -show_entries stream=nb_read_frames -of csv=p=0 film.mp4
ls "$SC/ae-renders/<job>/studio/frames"/*.png | wc -l   # must MATCH
```

Gate thresholds (never lowered to pass — fix the scene instead):
`luminancia_media > 20`, `contraste_medio > 10`, `movimiento_medio > 0.5`,
`frames_negros = 0`.

Per-scene audio, to prove every scene is audible:

```python
# decode to PCM, slice by wav length, report RMS per scene
# healthy scenes measure ~0.08–0.14 RMS
```

## 5. SOUND — leave the mute world

A speaking robot in a silent room is still mute. Derive the world from the
film's OWN timings so impacts land on cuts by construction.

```python
import sound_link as S, json, pathlib
meta = json.loads(pathlib.Path(f'{WD}/studio/studio.json').read_text())
spec = json.loads(pathlib.Path(f'{WD}/spec.json').read_text())
spec['_total'] = meta['total_s']
for s, m in zip(spec['scenes'], meta['scenes']):
    s['_t0'] = m['t0']; s['_dur'] = round(m['t1'] - m['t0'], 3)
a = S.spec_from_film(spec, texture='sci_fi', bed_db=-30.0)
S.render(a, pathlib.Path(f'{SC}/world.wav'))          # numpy only, torch False
S.mix(film, world_wav, out, voice_gain=1.0, bed_gain=0.5)
```

If `studio.json` is absent, derive timings from the wav byte lengths:
`dur = wav.stat().st_size / 48000.0`, accumulated in scene order.

Textures: `sci_fi`, `city_hum`, `room_cold`, `drone`, `rain`, `ocean`, `wind`.
State→sound mapping lives in `sound_link.STATE_SOUND`; the refusal gets
`sub_drop` + `bell` so governance is audible.

**Prove it worked** — count near-silent 100 ms windows:

```python
win = 2400  # 100 ms at 24 kHz
rms = np.sqrt((x[:n*win].reshape(n,win)**2).mean(axis=1))
quiet = (rms < 0.005).sum()
# silent film ~22%, world-filled 0%
```

Speech must stay intelligible: RMS rises modestly (~0.11 → ~0.13), peak stays
below 0.96. If words get buried, lower `bed_gain` — that is an ear judgment.

## 6. PLAY it for the human

```python
# kill stale listeners by PID THROUGH PYTHON (MSYS taskkill //F fails)
import subprocess
for pid in {l.split()[-1] for l in subprocess.run(['netstat','-ano'],
        capture_output=True,text=True).stdout.splitlines()
        if ':8081' in l and 'LISTENING' in l}:
    subprocess.run(['taskkill','/F','/PID',pid])
```

Start VLC with `--extraintf=http --http-port=8081 --http-password=<pw>`, then
load with **`in_play` over HTTP** (a CLI file argument leaves VLC `stopped`):

```
GET /requests/status.json?command=in_play&input=<urlencoded C:\path>
```

Confirm `state: playing` and BOTH streams (Video + Audio) in the status JSON.

## 7. PUBLISH — through the chain, never bare git push

```bash
cd C:/æ/github-pages
# copy artifacts, then APPEND a dated AE-CONTINUITY.md entry
# (never overwrite another agent's modification; stage only your own scope)
git add <your files>
git -c user.name="HUMAN://ROOT" -c user.email="yael@llm.store" commit -m "..."
C:/gpu/Scripts/python.exe C:/æ/agents/kanban_push.py push \
    --task <name> --branch gh-pages --assignee <agent> --detail "..."
```

Verify AUTHORITATIVELY first — the CDN lags:

```bash
gh api repos/MYaelMendez/MYaelMendez.github.io/contents/<file>?ref=gh-pages \
  --jq '"\(.size) B sha \(.sha[0:8])"'
```

If URLs 404 but the API confirms bytes, check the BUILD, do not re-push:

```bash
gh api repos/MYaelMendez/MYaelMendez.github.io/pages/builds/latest \
  --jq '{status,error:.error.message,commit}'
```

At most three status checks over two minutes. `building` → `built` → 200 is
the normal sequence and takes ~60–90 s.

## 8. Record what was measured

Report frames/expected, gate numbers, receipt hash, per-scene RMS, and the
near-silent percentage. State plainly what is NOT verified: browser playback
(the agent browser cannot initialise media), second-machine reproducibility,
and physical robot motion.
