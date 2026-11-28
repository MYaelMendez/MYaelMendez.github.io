# 🟨 Taller: Biblia del Oso agéntica · Diplomado en Transformación Digital

**Martes 7 p. m. (hora de Texas) · 60 minutos · práctico** · `#ioa://teologia.ai/oso`

> *EN summary:* A 60-minute hands-on lab. Each student forks the repo, takes one chapter of the 1569 Spanish Bible, compares the facsimile scan with the raw OCR, fixes long-s errors (ſ misread as **f**), edits the chapter JSON and opens a pull request. Agents may propose; only humans verify.

## Por qué este texto
La Biblia del Oso (Casiodoro de Reina, Basilea, 28 sep 1569) usó la **ese larga «ſ»**, que en reproducciones posteriores se confunde con la **f** ([Wikipedia](https://es.wikipedia.org/wiki/Biblia_del_Oso)). Ese error es justo lo que corrige un OCR humano + agente.

## Antes de clase
- Cuenta de GitHub con sesión iniciada.
- Facsímil (dominio público): https://archive.org/details/la-biblia-del-oso
- Repositorio del proyecto: *por confirmar* (`LutheranInstitute/oso` o dentro de `aeee-lab`).

## Agenda (60 min)
| Min | Paso | Qué haces |
|---|---|---|
| 0–5 | Contexto | Reina declaró sus fuentes y su método: eso es código abierto en 1569. |
| 5–10 | **Fork** | Haz fork del repo y abre tu capítulo asignado (`v/LIB/cap.json`). |
| 10–25 | **Facsímil vs OCR** | Abre la página escaneada al lado del texto OCR. Lee línea por línea. |
| 25–40 | **Corrige ſ→f** | Busca palabras con **f** que deberían llevar **s**. |
| 40–50 | **Edita JSON** | Cambia `orig` (ortografía de 1569) y `status: "corrected"`; anota la hoja escaneada en `page.leaf`. |
| 50–60 | **Pull Request** | Commit con mensaje claro → PR → pide revisión a un compañero. |

## Errores reales del OCR de este facsímil
| OCR | Lectura probable | Nota |
|---|---|---|
| `fu`, `fus` | su, sus | ſu → fu |
| `fobre` | sobre | ſobre |
| `efta`, `efte` | esta, este | eſta |
| `feñor` | señor | ſeñor |
| `efpecias` | especias | eſpecias |

Regla: si no se lee en la imagen, **no se adivina**: pon `"notes": ["verificar fuente"]`.

## Ejemplo de JSON
```json
{ "id": "oso1569:GEN.1.1", "orig": "…", "status": "corrected",
  "page": { "scan": "archive.org/details/la-biblia-del-oso", "leaf": 12 },
  "evidence": { "corrected_by": "tu-usuario", "verified_by": null } }
```
Sin página enlazada, un versículo **nunca** pasa de `corrected`. `verified` lo marcan dos personas, no el agente.

## Resultados de aprendizaje
1. Usar fork, commit y pull request en un proyecto público real.
2. Leer un facsímil y distinguir error de OCR y ortografía antigua.
3. Editar datos estructurados (JSON) sin romper el esquema.
4. Aplicar *Evidence ≠ Authority*: el agente aporta evidencia, el humano decide.

## Ciclo
**Esto aprendí** (ſ ≠ f, fork/PR) → **Esto construí** (un capítulo corregido en mi PR) → **Esto puedo enseñar** (reviso el PR de otro compañero).

---
L:// Aprender · æ:// Construir · æQR:// Compartir · ☩ Soli Deo Gloria
