# `ae` call examples

These are JSON argument objects passed to the single `ae` tool. Each call
returns `{"success", "op", "result", "receipt"}`.

## Inspect state

```json
{"op": "status"}
```
Returns version `2.2.0`, authority `HUMAN://ROOT`, the count of plugins on
disk, the sorted shortcut list, and the receipt-chain summary.

```json
{"op": "ops"}
```
Lists available shortcuts and the bundled local ops (`free_walk`,
`studio_video`).

```json
{"op": "receipts", "limit": 10}
```
Returns the last 10 ledger entries and the total count.

```json
{"op": "verify"}
```
Validates the hash chain; reports `count`, `head`, and `broken_at`.

## Render a video locally (no publish)

```json
{"op": "studio_video", "publish": false}
```
Runs the Studio v2.1 fixed-base physics + viseme pipeline and writes
`asimov-studio-v2-916.mp4`. The result includes SHA-256, physics parameters
(`nu`, frames, model), viseme source/event count, and QC checks.

```json
{"op": "free_walk", "publish": false, "authorization": "user"}
```
Runs the Studio v2.2 mocap-guided free-base pipeline and writes
`asimov-free-walk-916.mp4`. The result includes base/COM advance, `nq`, `nu`,
frame count, QC, and a receipt recording the authorization source.

## Render and publish

```json
{"op": "free_walk"}
```
`publish` defaults to `true`: the MP4 is copied to the gallery checkout,
`videos.html` is regenerated, and the change is committed and pushed to
`gh-pages`. The result's `publish` object reports raw/API status codes.

## Reach a legacy plugin via a shortcut

These require the corresponding plugin under `HERMES_AE_PLUGINS`.

```json
{"op": "speak", "text": "Hello, I am Asimov.", "voice": "M2"}
{"op": "voices"}
{"op": "robot_say", "text": "Authority remains human root."}
{"op": "robot_status"}
{"op": "render", "script": "intro.py", "output": "intro.mp4"}
{"op": "probe", "output": "intro.mp4"}
{"op": "vlc", "arg": "play intro.mp4"}
{"op": "physics", "steps": 500}
{"op": "studio", "action": "status"}
{"op": "chimera_speak", "text": "Receipts on every action."}
```

## General `call` escape hatch

Invoke any registered tool directly by plugin and tool name:

```json
{"op": "call", "plugin": "tiny-voca-voice", "tool": "tts_speak",
 "text": "Hello.", "voice": "M2"}
```

If the plugin or tool is missing, the error includes the list of available
tools for that plugin.

## Reading a failed call

```json
{"success": false, "op": "call",
 "result": {"success": false,
            "error": "tool 'nope' not in plugin 'tiny-voca-voice'",
            "available": ["tts_speak", "tts_voices"]},
 "receipt": {"action": "AE://CALL", "authority": "HUMAN://ROOT", "detail": {"ok": false}, "hash": "..."}}
```

Even failed calls are receipted, so attempts remain auditable in the ledger.
