# rv1909 · Reina-Valera 1909 · fuente y licencia

**Licencia: dominio público.** Sociedad Bíblica Americana + Sociedad Bíblica Británica y Extranjera, 1909. Los derechos de autor vencieron hace mucho.

## Pruebas de la licencia
- eBible.org, página de copyright de spaRV1909: "Public Domain … Dominio Público" → https://ebible.org/spaRV1909/copyright.htm
- CrossWire SWORD, módulo SpaRV: "Distribution License: Public Domain" → http://www.crosswire.org/sword/copyright/ModInfoCopyright.jsp?modName=SpaRV
- Debian `sword-text-sparv`: "License: public-domain. This work is not copyrighted." → https://tracker.debian.org/media/packages/s/sword-text-sparv/copyright-2.87-1
- El dataset de HF k-mktr/spanish_rv1909_es dice "Public domain (1909 edition, copyright expired)" → https://huggingface.co/datasets/k-mktr/spanish_rv1909_es
- El archivo de origen (Unbound Bible) trae el campo `#copyright` **vacío** y su `.html` sólo pone el nombre de la edición. No afirma nada sobre la licencia, así que la licencia se apoya en las fuentes de arriba.

## Origen del archivo
- Descargado el 2026-10-16 de https://www.biblesupersearch.com/wp-json/bss/download-unbound/spanish_reina_valera_1909.zip (Unbound Bible / Biola, "Unmapped-BCVS", archivos fechados 2007-04-05)
- sha256 del zip: `b38089c0984eef74403359f777a8e56248d7808c506bcdd730ce2188104990ec` (borré el zip después de extraerlo)
- sha256 de `raw/spanish_reina_valera_1909_utf8.txt`: `4e03174db1e80f5f089348721f40eb29c2c6da6e84200ce945753ab3cc8b4a46`

## Normalización (`scripts/build_rv1909.py`)
- Una línea por versículo: `{"id":"rv1909:GEN.1.1","text":"…"}`. Los códigos de libro son USFM y vienen de `align/crosswalk.json`.
- Sólo se aplica NFC Unicode, se colapsan los espacios y se recortan los bordes. **La ortografía de 1909 queda como está** («crió», «fué», «á», versal inicial «EN»).
- Hay 31,102 versículos en 66 libros. No hay subversículos ni versículos vacíos. La sha256 del JSONL está en `stats.json`.
- El dataset de HF declara 31,084 filas. La diferencia de 18 no está conciliada: puede ser un tema de versificación, versículos fusionados o un error en el dataset. No se usó el dataset de HF como fuente.
