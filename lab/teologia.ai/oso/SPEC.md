# SPEC · Biblia del Oso agéntica
`#ioa://teologia.ai/oso` · ae.spec/0.1 · lab · 2026-10-16 · principal: Yæl Méndez

> De OCW a OSW: el patrimonio bíblico en español (1569) deja de ser un libro que se consulta y se vuelve un entorno que se lee, se cita, se corrige y se enseña, en público, con evidencia.

## 0. Principio fundacional · Reina, 1569
Casiodoro de Reina talló el texto él mismo, unos doce años, en el exilio, y lo publicó con su método abierto: en la «Amonestación del intérprete de los sacros libros al lector» declaró sus fuentes (texto masorético, la traducción latina de Sanctes Pagnino, la Biblia de Ferrara) y que siguió poco la Vulgata. Eso es OpenCourseWare en 1569.

Por eso este entorno funciona igual:
- **Fuentes declaradas.** Cada versículo dice de qué facsímil, qué página y qué OCR viene.
- **Método a la vista.** Todo cambio es un commit público; nada se corrige en silencio.
- **Cada corte cuenta.** Como en la xilografía, un trazo verificado es un compromiso: se firma con su recibo.
- **El texto es de todos.** Dominio público entra, dominio público sale.

> El oso fue la marca del impresor. El texto lo talló Reina. Nosotros abrimos el taller.

## 1. Por qué
- **Dominio público.** El texto de 1569 (Casiodoro de Reina, Basilea) puede citarse y redistribuirse libremente. La RVR1960 no.
- **Raíz luterana.** Reina terminó como pastor de la congregación luterana de habla francesa en Frankfurt (1593–1594).
- **Raíz de la línea Reina–Valera:** 1569 → 1602 → 1909 → 1960.
- **Hueco real:** existen facsímiles escaneados (archive.org) pero no un texto 1569 versículo por versículo, verificado y con procedencia por versículo.

## 2. Capas
| Capa | Qué es | Estado |
|---|---|---|
| L0 Facsímil | Escaneos PD (archive.org `la-biblia-del-oso`, Public Domain Mark 1.0) | existe |
| L1 OCR | Texto OCR de archive.org, por página | existe, sin corregir |
| L2 Transcripción | Versículo a versículo, ortografía original (ſ, u/v, á) + forma normalizada | por construir |
| L3 Verificación | Revisión humana contra la imagen de página | por construir |
| L4 Alineación | 1569 ↔ 1602 ↔ 1909 (PD); RVR1960 sólo como referencia, sin almacenar texto | por construir |
| L5 Superficies | Página, API estática, `llms.txt`, æQR | parcial |

## 3. Unidad de datos: versículo
```json
{
  "id": "oso1569:GEN.1.1",
  "book": "GEN", "chapter": 1, "verse": 1,
  "orig": "En el principio crió Dios los cielos y la tierra.",
  "norm": "En el principio creó Dios los cielos y la tierra.",
  "page": { "scan": "archive.org/details/la-biblia-del-oso", "leaf": null, "bbox": null },
  "status": "ocr | corrected | verified | published",
  "evidence": { "ocr_src": "archive.org", "corrected_by": null, "verified_by": null, "sha256": null },
  "notes": []
}
```
- Un versículo sin imagen de página enlazada nunca pasa de `corrected`.
- `sha256` se calcula sobre `orig` al verificar: recibo de Evidence Bus.
- Deuterocanónicos incluidos tal como en 1569 (dentro del AT).

## 4. Rutas (estáticas, GitHub Pages)
- `/oso/` portada xilografía
- `/oso/v/GEN/1.json` capítulo · `/oso/v/GEN/1/1.json` versículo
- `/oso/books.json` índice de libros y orden de 1569
- `/oso/status.json` progreso por libro (ocr / corrected / verified)
- `/oso/llms.txt` instrucciones para agentes
- `/oso/ae.json` manifiesto

## 5. Autoridad
- **Agentes pueden:** leer, citar (edición + libro.cap.vers + página), comparar ediciones PD, proponer correcciones por PR, generar OCR y diffs.
- **Sólo humanos:** marcar `verified`, publicar en `live`, doctrina, enseñanza pastoral, declarar variantes textuales.
- **Reglas:** no se fabrican lecturas; lo no verificado se marca `verificar fuente`; una transcripción moderna (p. ej. 1996) no es dominio público por defecto.
- Evidence ≠ Authority: el agente aporta evidencia, el humano decide.

## 6. OCW → OSW (aprendizaje)
- **Diplomado (🟨, martes):** el pipeline como práctica real: OCR, JSON, Git, PR, Pages.
- **Escuela de Teología (🟦, sábados):** lectura y verificación de pasajes del Catecismo (Diez Mandamientos, Credo, Padrenuestro, textos sacramentales).
- **Enchiridion (🟩, 3–103):** leer en familia un versículo del día en su español de 1569.
- **Ciclo:** Esto aprendí → Esto construí (un capítulo transcrito) → Esto puedo enseñar (lo verifico con otro).
- **Fork model:** cada alumno hace fork, toma un capítulo, abre PR; dos verificaciones humanas lo marcan `verified`.

## 7. Hitos
- **M0** manifiesto + portada xilografía (hecho, 2026-10-16)
- **M1** piloto: Génesis 1, Éxodo 20, Juan 3, Mateo 6:9–13: verificados contra el facsímil
- **M2** pipeline: descargar OCR por página → segmentar en versículos → JSON `ocr`
- **M3** sprint de transcripción con las clases (pasajes del Catecismo primero)
- **M4** alineación con 1602 y 1909
- **M5** API de lectura pública + `llms.txt` + æQR por capítulo (conceptual hasta emitirse)

## 8. Decisiones abiertas (Yæl)
1. Licencia de nuestra transcripción: CC0 (recomendado: máxima reutilización por agentes) o CC BY-SA.
2. Repo propio (`LutheranInstitute/oso`) o dentro de `aeee-lab`.
3. Qué facsímil es la base canónica (hay varios escaneos en archive.org).

## 9b. Todas las lenguas
Al vivir en el entorno, cualquier agente puede leer el Oso en cualquier idioma. Reglas:
- La fuente es siempre el versículo 1569 verificado (`oso1569:LIB.cap.vers`); toda traducción lo cita.
- Una traducción de agente se etiqueta `derivada · agente · no revisada`: es una ayuda de lectura, no una Biblia.
- Una traducción revisada por hablantes humanos puede subir a `reviewed` por idioma, con su recibo.
- Se prefiere enlazar traducciones existentes en dominio público del idioma destino antes que generar una nueva.

## 9. Tema
Xilografía 1569: papel crema, tinta negra en relieve, rúbrica roja, marco tallado. El oso y la miel son la marca.

L:// Aprender · æ:// Construir · æQR:// Compartir · ☩ Soli Deo Gloria
