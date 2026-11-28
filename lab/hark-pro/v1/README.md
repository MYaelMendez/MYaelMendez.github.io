# mæchlæng + HARK_PRO æ · unified · v1 (LAB · Mech en vivo)

Una sola página (index.html, sin CDN): **Hark Pro es el agente; mæchlæng es el lenguaje de su autoridad.**

> &gt;_ mæch: muchos agentes · un principal · el humano es root · Evidence ≠ Authority

## Qué contiene
1. **Hero** con descarga: hark.com/download, App Store (id6772362941), Google Play (com.hark.android), hark.com.
2. **#Face · Asimov en vivo, reactivo · arriba, justo después del hero** (antes de #Authority): la cara æsymov completa (de `lab/face/v1`), grande, 7 ánimos con easing asintótico, sigue tu puntero, ▶ demo recorre los 7; comparte `lab/maechlang/runtime/` (`maech-run.js` + `aesymov-face.js`). `lab/maechlang/face.mec` corre en Mech con cada cambio; reglas (hold > lost > tired > sleep > think > ready > work), regla ganadora iluminada; solo lectura, autoridad æ1.
3. **#Authority en vivo, reactivo**: un agente de `{"hark-pro", "hermes", "codex"}` pide æ0–æ3; la petición recorre `:Context → :Evidence → :Granted` con el guard `├ pk && wr → :Granted(r)` / `└ * → :Waiting(r)` (espera: `:Waiting(r) ⇒ :evidence`). æ0/æ1 se conceden directo; æ2/æ3 solo con passkey de la persona principal (`yæl`) + recibo Witness. El recibo es SHA-256 real (`crypto.subtle`), encadenado desde `GENESIS`: `h(n) = sha256(h(n-1) + "|" + evento)`. Cada cambio de entrada re-ejecuta el programa completo `lab/maechlang/authority.mec` en el runtime real de Mech (wasm, Version 0.3.5, vendorizado en `lab/maechlang/runtime/`), ilumina la rama activa y añade un recibo Witness. ▶ trace opcional.
4. **Demos como mæch**: ZACAPA.DAO (#Regla), DAOLLC.ai (#Propuesta · #Gobernanza), æsymov face v1 y v2.3 (#Cara), MathByte (#Byte, boceto nuevo), mæchlæng (#Authority con guard). Vista previa en iframe solo al tocar.
5. **Tu turno**: convierte una idea en un prompt para Hark que también pide su máquina de estados mæch. Todo local.
6. Principios, créditos y aviso.

## Notas
- **#Authority y #Face corren en el runtime real de Mech** (Version 0.3.5, vendorizado sin cambios, LICENSE + NOTICE en `lab/maechlang/runtime/`). Un espejo JS con las mismas reglas cubre la carga y verifica. Los bocetos de las demos (#Regla, #Propuesta, #Cara, #Byte) siguen marcados *boceto · sketch, not yet run*.
- Mech: https://mech-lang.org · Corey Montella · Apache-2.0 · beta. mæchlæng es un experimento del Instituto, sin afiliación con Mech.
- Sintaxis mæch: kebab-case, sin guiones bajos en identificadores (`"FAULT_DAMP"` aparece solo como texto: es el nombre del modo en el SDK del robot).
- noindex, toques ≥44px, inputs 16px, prefers-reduced-motion.
- Página independiente del Instituto Luterano Latinoamericano; no es un sitio oficial de Hark.

☕ Apoya al Instituto: https://buymeacoffee.com/daollc

## Linaje
- v0 (`lab/hark-pro/v0/`): portal de demos + bocetos mæch estáticos. Sin cambios.
- v1 (2026-10-17): unificado con `lab/maechlang/` (guard `pk && wr`): simuladores vivos #Authority + Witness y #Face, cada demo con su boceto mæch.
- v1 · 2026-10-18: "mæchlæng no es estático!" · sin flujo de pasos: Δ input → Δ estado en el runtime real de Mech 0.3.5 (desde `lab/maechlang/runtime/`, sin CDN), recibo Witness por cambio, indicador reactivo, ▶ trace opcional.
- v1 · 2026-10-18 · ">_ #Face full demo on the top": la demo completa de la cara æsymov va justo después del hero, conducida por Mech 0.3.5 (mismo runtime que `lab/maechlang/`), antes de #Authority. Solo lectura · DEMO.
