# >_æææ.com · Laboratorio

Mismo sistema que `LutheranInstitute/bookstores`: el repo es a la vez **en vivo** y **laboratorio**.

| Superficie | En vivo | Laboratorio |
|---|---|---|
| æææ.com | [`/`](https://myaelmendez.github.io/) | [`/lab/`](https://myaelmendez.github.io/lab/) |

## Flujo
issue → rama → cambios en `lab/` (visible en su enlace) → PR que copia a `/` → **Yæl aprueba y fusiona** → en vivo.

## Cómo funciona `lab/index.html`
- Copia exacta de `index.html` con `<base href="../">`, así lee los mismos manifiestos, scripts y superficies que producción.
- Franja **LAB** arriba y `<meta name="robots" content="noindex">`.
- Evidence ≠ Authority: los agentes proponen en `lab/`; solo Yæl decide qué pasa a vivo.

Make something agents want. · #ioa
