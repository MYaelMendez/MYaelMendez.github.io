# mæchlæng · runtime (vendored Mech)

The real Mech runtime, compiled to WebAssembly, served from this repo (no CDN). See `NOTICE` and `LICENSE` (Apache-2.0, Corey Montella). mæchlæng is not affiliated with Mech.

- `mech_wasm.js` + `mech_wasm_bg.wasm.gz`: unmodified Mech wasm build (reports Version 0.3.5). The page gunzips it with `DecompressionStream` and verifies the sha256 before running.
- `maech-run.js`: mæchlæng bridge. Δ input → rewrite the `⟦inputs⟧` lines of `authority.mec` / `face.mec` → run the whole program on a fresh Mech interpreter (`WasmMech.run_program`) → read `out_string()` → Δ estado + Witness SHA-256 receipt. A JS mirror with the same rules covers the moments before the runtime loads, and cross-checks Mech after.
- `aesymov-face.js`: the 🤖æsymov_face (from `lab/face/v1`) as a reusable piece: SVG face, 7 moods, asymptotic easing (τ 0.18 s / 0.9 s), pointer follow, ▶ demo tour. `AesymovFace.boot({base})` mounts `maech-run.js` with an `onFace` hook, so the face shows exactly the mood Mech returned. Read-only (æ1): it never moves a robot.
- Test: `node ../test.mjs` runs every input combination (208 programs) on this runtime and checks no æ2/æ3 grant without `pk && wr`.
