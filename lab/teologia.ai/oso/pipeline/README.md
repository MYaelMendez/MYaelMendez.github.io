# pipeline · Biblia del Oso 1569 → verse JSON (`status: ocr`)

## Run
```bash
cd /workspace/work/aeee/teo/oso
python3 pipeline/segment.py GEN 1 2          # writes v/GEN/1.json, v/GEN/2.json
python3 pipeline/segment.py GEN 1 --debug    # prints every KEEP / DROP line decision
```
Python 3 stdlib only. Inputs: `src/djvu.txt` (archive.org OCR, item `la-biblia-del-oso`) and
`src/sse_grid/spanish_sagradas_escrituras_1569_utf8.txt` (modernized grid, guide only).
To add a book, add a line to `BOOKS` in `segment.py`: OSIS code → (grid book index, regex for the
book's title line in djvu.txt, regex for the next book's title line).

## How it works
1. **Chapter window.** Every `CAPIT…` heading in the book is a candidate; the chapter starts at the
   heading whose next 60 lines share the most 5-grams with the guide's first verses, and ends at
   the heading that best matches the next chapter. (Many headings are OCR-mangled or missing —
   `CA PIT TL`, `CAPIT RLTIL` — and some sit mid-line, so heading counting alone is unreliable.)
2. **Skeleton matching.** OCR and guide text are folded to a spelling-neutral skeleton (accents
   off, f/ſ→s, v→u, y→i, z→c, j/g/x merged, h dropped, b→u, doubled letters collapsed, no spaces
   or punctuation). This lets `eftendimiento` match `extendimiento` without correcting anything.
3. **Verse openers.** For each verse in order, find the line whose first tokens hold the printed
   number (OCR confusions such as `34`→24, `“M2`→12 accepted) and whose following text matches
   the guide incipit. Fallbacks: incipit match without a number (whole line or mid-line split),
   then an opener printed out of reading order elsewhere in the chapter (column interleave).
4. **Span filtering.** Lines between two openers are aligned against the guide verse(s) of that
   span; only the aligned run of each line is kept (trimmed to whole words), which strips margin
   cross-refs, glosses, Roman section numerals and column noise. Lines that match nothing are
   dropped, unless they sit between two body lines of the same verse (kept, with a note). A
   strongly and uniquely matching line found in the wrong span is reattached, with a note.
5. **Output.** Fragments are joined (line-end `-`/`=` hyphens removed, words rejoined), the
   printed number is removed, pilcrow OCR forms (`€]`, `4]`, `G|`) become `¶`, a leading `*`
   callout is removed. Every character of `orig` comes from djvu.txt; the guide's text is never
   written. Notes record every heuristic decision and the djvu.txt line range used.

## Known OCR quirks (1569 facsimile)
- Long s `ſ` is OCR'd as `f` (`fobre`, `fegun`); `ç` often `g` (`produzga`, `verguença`→`vergongauan`).
- u/v and i/j/y are period spellings (`vido`, `auia`, `ymagen`); keep them — `orig` is not corrected.
- Words fuse across missing spaces (`YllamóDiosaleltendimiento`), and `Iehoua` is often `lehoua` /
  `Ichoua` / `lchoua`.
- Verse 1 of each chapter opens with a woodcut initial: the first letter is lost or garbled
  (`=2A=> 0 Nx el principio`), so `orig` for v1 usually begins mid-word.
- Two text columns + outer margin notes are interleaved line by line; margin text often rides at
  the end (or start) of a body line (`… era bueno. y Heb.to-`). Occasionally a whole body line is
  emitted out of order (Gen 1:22's first line appears inside 1:12).
- Superscript gloss letters fuse into words (`aguasb que`, `Diosflas`); these are NOT removed.
- No page breaks (`\f`) in djvu.txt, so `page.leaf` stays `null`. Linking leaves needs the
  per-page OCR (`_djvu.xml` / hOCR) from archive.org.
- Where 1569 wording differs from the modern guide (word order, different words), the guide can't
  vouch for a line; such lines are dropped or kept "by context" — check notes.

## Limits
Heuristic and tuned on Genesis 1–2 only. `status` stays `ocr`; every verse needs human correction
against the page image before `corrected`/`verified` (SPEC §3, §5).
