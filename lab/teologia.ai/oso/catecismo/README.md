# Catecismo Menor · pasajes núcleo en la Biblia del Oso (1569)

`oso1569` · Casiodoro de Reina, Basilea 1569 · dominio público · facsímil: `archive.org/details/la-biblia-del-oso`

> **Estado: `corrected-proposed`.** Todo el texto `proposed` es una **propuesta de agente**. Nada está verificado.
> Una persona debe cotejar cada versículo con la hoja del facsímil (`page.leaf`, enlace `page.image`) antes de pasarlo a `corrected` y, con dos revisores, a `verified` (SPEC §5, CONTRIBUTING).
> Evidence ≠ Authority: el agente aporta evidencia; el humano decide.

## Mapa: pasaje → parte del Catecismo

| Parte del Catecismo Menor | Pasaje | Hoja(s) facsímil | Versículos |
|---|---|---|---|
| I. Los Diez **Mandamientos** | Éxodo 20:1-17 | 104, 105 | 17/17 |
| III. El **Padrenuestro** | Mateo 6:9-13 | 1030 | 5/5 |
| III. El **Padrenuestro** | Lucas 11:2-4 | 1092-1093 | 3/3 |
| IV. **Bautismo**: 1ª, qué es | Mateo 28:19 | 1057 | 1/1 |
| IV. **Bautismo**: 2ª, qué da | Marcos 16:16 | 1076 | 1/1 |
| IV. **Bautismo**: 3ª, cómo lo hace | Tito 3:5-8 | 1235 | 4/4 |
| IV. **Bautismo**: 4ª, qué significa | Romanos 6:4 | 1174 | 1/1 |
| V. **Confesión** / Oficio de las llaves | Juan 20:22-23 | 1135 | 2/2 |
| VI. **Santa Cena** | Mateo 26:26-28 | 1053 | 3/3 |
| VI. **Santa Cena** | 1 Corintios 11:23-25 | 1192 | 3/3 |

(II. El Credo no tiene un pasaje bíblico único en el Catecismo Menor; queda fuera de este lote.)

Total: 40 versículos, ninguno ausente ni ilegible.

## Archivos
- `passages.json`: por pasaje, la lista de versículos con el esquema SPEC §3 más `proposed`, `changes`, `confidence`.
- `build_passages.py`: genera `passages.json` (los textos están escritos a mano en el script; `changes` se calcula por diff de palabras).

## Campos
- `orig`: OCR de archive.org (`src/djvu.txt`) limpiado **solo** de glosas marginales, referencias al margen, ruido de fin de línea, números de versículo, reclamos (catchwords) y titulillos. Los errores del OCR se conservan.
- `proposed`: lectura propuesta en ortografía de 1569: ſ larga, u/v e i/j como en el impreso, abreviatura nasal como tilde (ã ẽ ũ q̃), acentos grave/agudo como se ven. Se omiten letras de nota y asteriscos de referencia. Los corchetes `[ ]` de Reina se conservan (1 Cor 11:24 `[y]`). Las palabras en cursiva (añadidas por Reina) se indican en `notes`.
- `changes`: cada diferencia OCR → propuesta, con su tipo (ſ larga, guion de línea unido, error de OCR corregido, texto tomado del facsímil, marca de nota eliminada).
- `page.leaf`: hoja del escaneo (índice IIIF), obtenida del índice hOCR de archive.org.
- Los límites de versículo vienen de la cuadrícula SSE 1569 (`src/sse_grid`); **no se copió ningún texto de ella**.

## Lo que el OCR no traía (leído en la imagen de la página, verificar)
- Éx 20:1: la `Y` capitular xilográfica.
- Éx 20:9: la línea final `bra,` (obra).
- Éx 20:17: la línea final `mo.` (proximo).
- Mt 26:26: la `y` antes de `auiendo`.

## Puntos para el revisor humano
1. Forma de la marca nasal: en este tipo a veces parece acento agudo (Vẽga, pã, potẽcia, tãbien, abundãtemẽte); se transcribe como tilde.
2. Acento de la preposición `a`: el impreso alterna `à` y `á` (Tit 3:8 tiene `á Dios` y `à los hombres`). Rom 6:4 `con el a muerte` no se revisó en la imagen.
3. Espaciado: se conservan las uniones del impreso (`enel`, `Elque`, `losque`, `Portanto`, `paraq̃`, `Anſimiſmo`); donde el impreso es solo apretado se separó (Tit 3:6 `por Ieſus el Chriſto Saluador`, 1 Cor 11:24 `es mi`).
4. Cursivas: identificadas a 1600 px; confirmar.

L:// Aprender · æ:// Construir · ☩ Soli Deo Gloria
