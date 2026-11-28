# Contribuir · Biblia del Oso 1569
`#ioa://teologia.ai/oso` · repo `LutheranInstitute/aeee-lab` · rama `lab` · ruta `lab/teologia.ai/oso/`

> Reina talló el texto con su método a la vista. Nosotros abrimos el taller: cada versículo se corrige en público, contra el facsímil, y se firma con su recibo.

## Flujo (5 pasos)

1. **Fork.** Haz fork de `LutheranInstitute/aeee-lab` y trabaja en una rama propia (`oso/Gen-1`, por ejemplo).
2. **Toma un capítulo con un issue.** Abre un issue titulado `Tomar capítulo · oso1569:<OSIS>.<cap>` (ej. `oso1569:Gen.1`). Revisa antes que nadie lo haya tomado. Un capítulo, una persona; si en 14 días no hay PR, el capítulo se libera.
3. **Transcribe / corrige contra el facsímil.** Edita `v/<OSIS>/<cap>.json`:
   - `orig`: exactamente lo impreso en 1569 (ſ, u/v, acentos y abreviaturas como estén). `norm`: forma normalizada.
   - `page.leaf`: la hoja del facsímil (`archive.org/details/la-biblia-del-oso`) donde lo leíste. Sin hoja enlazada, el versículo no pasa de `corrected`.
   - `status`: de `ocr` a `corrected`. Nunca escribas `verified` tú mismo.
   - Lo dudoso va en `notes` con «verificar fuente». No inventes lecturas ni copies de la RVR1960 ni de transcripciones modernas con derechos.
4. **Pull request.** Un PR por capítulo, título `oso1569:<OSIS>.<cap> · corrected`, enlazando el issue. Describe qué cambiaste y qué hojas consultaste.
5. **Dos verificaciones humanas.** Dos personas distintas a quien transcribió revisan cada versículo contra la imagen de la página y aprueban el PR. Entonces un mantenedor marca `status: "verified"`, llena `evidence.verified_by` (ambos) y `evidence.sha256` (SHA-256 de `orig` en UTF-8: el recibo), y hace merge.

```bash
printf '%s' "En el principio ..." | sha256sum   # recibo sobre el campo orig, sin salto de línea final
```

## Agentes
Los agentes **sólo pueden abrir PRs** (OCR, segmentación, diffs, correcciones propuestas), identificándose como agente en el PR. No toman capítulos a nombre de nadie, no aprueban, no marcan `verified`, no hacen merge ni publican. Ver `llms.txt`.

## Autoridad
Evidence ≠ Authority: el agente aporta evidencia, el humano decide. Doctrina, enseñanza pastoral y variantes textuales son sólo humanas.

## Licencia
El texto de 1569 es dominio público. La licencia de nuestra transcripción está por decidir (CC0 propuesta); al contribuir aceptas publicarla bajo la que se adopte.

---

## English (short)

1. **Fork** `LutheranInstitute/aeee-lab`, branch `lab`.
2. **Claim a chapter** by opening an issue `Tomar capítulo · oso1569:<OSIS>.<ch>`. One chapter, one person; unclaimed after 14 days without a PR.
3. **Transcribe/correct against the facsimile** in `v/<OSIS>/<ch>.json`: exact 1569 text in `orig`, normalized in `norm`, the facsimile leaf in `page.leaf`, status `corrected`. Never invent readings; flag doubts with "verificar fuente".
4. **Open a PR**, one per chapter, linking the issue.
5. **Two human verifiers** (not the transcriber) check each verse against the page image; a maintainer then sets `verified`, records both in `evidence.verified_by`, adds the `sha256` receipt of `orig`, and merges.

**Agents may only open PRs.** They never claim, approve, verify, merge or publish.

L:// Aprender · æ:// Construir · æQR:// Compartir · ☩ Soli Deo Gloria
