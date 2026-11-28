# L4 · Alineación · 1569 ↔ 1602 ↔ 1909

`#ioa://teologia.ai/oso/align` · ae.spec/0.1 · lab · 2026-10-16

> El agente alinea, el humano decide. Una alineación es evidencia, no autoridad.

## 1. Ediciones
| id de edición | Obra | Libros | Texto almacenado | Licencia |
|---|---|---|---|---|
| `oso1569` | Biblia del Oso, Casiodoro de Reina, Basilea 1569 | 81 (con deuterocanónicos intercalados en el AT) | L2, por construir | dominio público; la transcripción propia será CC0 o CC BY-SA (decisión abierta) |
| `cantaro1602` | Biblia del Cántaro, Cipriano de Valera, Ámsterdam 1602 | 81 (los deuterocanónicos van entre AT y NT) | **ninguno** (no hay texto PD verificado, §5) | facsímiles PD |
| `rv1909` | Reina-Valera 1909, SBA/SBBE | 66 | `src/rv1909/rv1909.jsonl` | dominio público (`src/rv1909/SOURCE.md`) |
| `rvr1960` | Reina-Valera 1960 | 66 | **nunca** | © SBU. Sólo se guarda la referencia `rvr1960:JHN.3.16`, nunca el texto |

## 2. Identificadores
- Versículo: `{edición}:{LIBRO}.{cap}.{vers}`, por ejemplo `oso1569:GEN.1.1`, `rv1909:GEN.1.1`.
- `LIBRO` es un código USFM de 3 letras (GEN, EXO … 1MA, 2MA, MAN, SUS …). `crosswalk.json` también da el nombre OSIS (`Gen`, `1Macc`), el índice de Unbound Bible (`01O`, `77A`) y el nombre en español.
- Cada edición usa **su propia** numeración de capítulo y versículo. Los ids nunca se reescriben para que coincidan con otra edición. La equivalencia está en el crosswalk.

## 3. Modelo de crosswalk
Hay dos niveles:

**a) Libros** (`crosswalk.json → books[]`): una entrada por libro, con `in_1569 / in_1602 / in_1909`, `order_1569`, `order_1909` y `canon` (protocanonical | deuterocanonical).
- Los 66 libros protocanónicos se alinean por libro en las tres ediciones.
- Los 15 deuterocanónicos (MAN, 1ES = 3 Esdras, 2ES = 4 Esdras, TOB, JDT, ESG, WIS, SIR, BAR, LJE, S3Y, SUS, BEL, 1MA, 2MA) **sólo existen en 1569 y 1602**. Frente a rv1909 su alineación es `null`. No se trata como error: es la diferencia de canon documentada.

**b) Versículos** (`crosswalk.json → verse_map[]`, vacío por ahora): sólo se anotan las **excepciones**. Por defecto vale la identidad: `oso1569:B.c.v ≡ rv1909:B.c.v`. Una excepción se escribe así:
```json
{"from":"oso1569:DAN.13.1","to":["oso1569:SUS.1.1"],"type":"renumber","basis":"Susana como Dan 13 (orden Vulgata)","status":"proposed","evidence":{"leaf":null},"by":"agent"}
{"from":"oso1569:PSA.51.1","to":["rv1909:PSA.51.1","rv1909:PSA.51.2"],"type":"split","status":"proposed"}
```
- `type`: `identity | renumber | split | merge | absent | added`.
- `status`: `proposed` (lo propone un agente) → `verified` (lo confirma un humano contra el facsímil). El agente no marca `verified`.
- Casos que hay que revisar: títulos de Salmos (versículo 0 contra versículo 1), Mal 4 / Mal 3:19–24, Rom 16:25–27, 3 Jn 14–15, Ester griego y Daniel 3/13/14 (numeración Vulgata en 1569), Baruc 6 = Epístola de Jeremías.

## 4. Orden de libros de 1569
`order_1569` sigue el orden Vulgata y lo **confirmé en parte con el OCR** (`src/djvu.txt`, archive.org `la-biblia-del-oso`): Oración de Manasés después de 2 Crónicas, y 3 y 4 Esdras después de Nehemías («FIN DEL TERCERO / QVARTO LIBRO DE…»). Siguen Tobías, Judith y Ester; Sabiduría y Eclesiástico después de Cantares; Susana al final de Daniel; 1 y 2 Macabeos después de Malaquías y antes de S. Mattheo. BAR/LJE y la posición de S3Y/BEL: **verificar fuente** contra la imagen de página.

## 5. 1602 (Cántaro): qué existe
| Recurso | Qué es | Licencia | Uso |
|---|---|---|---|
| archive.org `reinavalera1602` | facsímil completo + OCR (`_djvu.txt`, `_hocr.html`) | **Public Domain Mark 1.0** | ✅ candidato a L0/L1 para 1602 (OCR sin corregir, igual que el de 1569) |
| archive.org `BibliaDelCntaro1602`, `LaBibliaDelCantaro_201608` | otros escaneos + OCR (tesseract 5.3) | sin campo de licencia (la obra es PD; el escaneo no declara nada) | sólo como referencia cruzada |
| Gutenberg #5877 | **sólo San Mateo**, transcripción diplomática de 1602 (valera1909.com) | "Public domain in the USA". El aviso pide conservarlo cuando se republique | ✅ utilizable para MAT, conservando el aviso. No se descargó |
| Valera 1602 **Purificada** (eBible `spav1602p`, valera1602.org, GitHub llromerorr/TextosBiblicos) | revisión moderna de 2007/2019/2024, **no es el texto de 1602** | © Iglesia Bautista Bíblica de la Gracia, «Todos los derechos reservados» (equivale a NC-ND) | ❌ no se usa |
| es.wikisource «Biblia Reina-Valera Edición 1602» | eran copias del texto de 1909 y se redirigieron | — | ❌ |

**Conclusión:** no existe un texto 1602 completo, versículo a versículo y legible por máquina, con licencia clara. La ruta es la misma que para 1569: el facsímil PD `reinavalera1602` → su OCR → L2. Por eso `cantaro1602` va detrás de `oso1569` en el plan.

## 6. Advertencia sobre `src/sse_grid/` (Unbound «Sagradas Escrituras 1569»)
Ese archivo **no es la ortografía de 1569**. Tiene ortografía moderna («creó», «la faz»), cursivas `<I>` de palabras añadidas, sólo 66 libros y ningún deuterocanónico, y el campo copyright vacío. Parece una edición moderna derivada (*Sagradas Escrituras 1569*, s. XX). La SPEC (§5) dice que una transcripción moderna no es PD por defecto, así que no debe usarse como `orig` de `oso1569` hasta aclarar su licencia. Sirve como guía de versificación.

## 7. Pipeline
1. `scripts/make_crosswalk.py` → `align/crosswalk.json`
2. `scripts/build_rv1909.py` → `src/rv1909/rv1909.jsonl` + `stats.json`
3. (M4) `oso1569` L2 → diff por id con `rv1909` → proponer `verse_map` → revisión humana.

L:// Aprender · æ:// Construir · ☩ Soli Deo Gloria
