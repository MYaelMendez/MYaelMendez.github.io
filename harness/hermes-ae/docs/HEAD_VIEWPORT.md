# Native Asimov Head Viewport

The Asimov-1 head has a mask planned as a programmable viewport. There is no separate tablet face.[unverified]

```text
HUMAN://ROOT → æ → Asimov Agent → head viewport → RECEIPT
```

The face is one program. The head is the surface.[unverified]

## Exterior shell pieces

Menlo's head checklist lists eight manufactured/bought-in ASV1 parts in the head module: `700_01B`, `700_02B`, `700_03C`, `700_04C`, `700_05C`, `700_06C`, `700_07C`, and the `700_08X` camera.[1] The assembly instructions identify **three head covers** — top `700_04C`, left `700_06C`, and right `700_07C` — installed onto the prepared head assembly.[3] The build inventory names `700_03C` as the head base, `700_04C` as the top head cover, `700_06C` as the left head cover, and `700_07C` as the right head cover.[2]

Therefore the exterior shell count is **four pieces**.[1][2][3]

| Zone | Part | Role |
|---|---|---|
| `front_mask` | `ASV1_700_03C` | head base; primary front mask viewport |
| `top_cover` | `ASV1_700_04C` | top status strip |
| `left_cover` | `ASV1_700_06C` | left side status strip |
| `right_cover` | `ASV1_700_07C` | right side status strip |

`700_05C` is the head carrier, `700_08X` is the camera, and `700_12X` / `700_13X` are standoffs and the neck-pitch actuator — not exterior shell pieces.[1][2] Menlo also describes the head as containing the Pi 5, camera, and stereo microphone array, which are capability modules inside that shell.[2]

## Viewport doctrine

- One authority: `HUMAN://ROOT`.[unverified]
- Four exterior shell zones, each an address.[2][3]
- Programs are swappable: face, text, telemetry, QR/code, warning, off.[unverified]
- A face state is a policy outcome, never a signature.[unverified]
- The mask is part of the robot head, not a detachable tablet.[unverified]

## DOM awareness

The native head viewport can read a live page as a bounded, read-only DOM projection. It never clicks, types, or mutates the page; the projection is capped and receipted as `VIEWPORT://DOM_AWARENESS`.[unverified]

```json
ae({"op":"head","action":"dom","endpoint":"http://127.0.0.1:9222","match":"asimov","selector":"main"})
ae({"op":"head_dom","endpoint":"http://127.0.0.1:9222","match":"asimov"})
```

The HTML projection also exposes a self-DOM digest, proving the viewport can describe its own rendered controls, program, state, and exterior-zone bindings.[unverified]

## Ops

```json
ae({"op":"head","action":"status"})
ae({"op":"head","action":"enable"})
ae({"op":"head","action":"disable"})
ae({"op":"head","action":"voice","text":"Asimov online. Awaiting authorization.","voice":"M2"})
ae({"op":"head","action":"teleop","key":"w","arm":true,"deadman":true})
```

`ae({"op":"face", ...})` remains as a compatibility alias.[unverified]

Receipt actions: `VIEWPORT://ENABLE`, `VIEWPORT://DISABLE`, `VIEWPORT://VOICE_REPLY`, `VIEWPORT://TELEOP`, `VIEWPORT://TELEOP_DENIED`.[unverified]

## Safety

Motion requires arm + deadman. Denied teleop still writes a receipt. Wake word and speech-to-text come from the phone / Android MCP layer; tiny-voca supplies speech output only.[unverified]

## HTML

The self-contained projection is `https://myaelmendez.github.io/asimov-governed-face.html`. It renders a 32×28 LED matrix inside the native mask and exposes the four exterior zones as the shell map.[unverified]

## Sources

[1] https://docs.menlo.ai/asimov/1/build/assembly-preparations/part-organisation/head — Menlo Asimov head parts checklist
[2] https://www.humanoidrobot.build/menlo/asimov — Build Asimov 1 part inventory
[3] https://docs.menlo.ai/llms-full.txt — Menlo Docs complete text
