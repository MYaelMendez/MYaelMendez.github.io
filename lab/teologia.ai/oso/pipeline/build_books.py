#!/usr/bin/env python3
"""Build books.json and status.json from pipeline/book_anchors.py + src/djvu.txt + leafmap."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from book_anchors import ANCHORS, END_LINE_EXCLUSIVE
import leafmap

# osis -> (USFM-style code used by SPEC routes, modern Spanish name, testament, deutero, title_1569 cleaned,
#          expected chapters, chapters_note)
# title_1569: transcribed from the OCR title block, long-s/OCR slips silently normalised (f->s where
# it is a long s, l/I/T->I at word start, broken words joined). NOT yet checked against the leaf image.
META = {
 "Gen":("GEN","Génesis","OT",False,"Primero libro de Moysen, llamado comunmente Genesis",50,None),
 "Exod":("EXO","Éxodo","OT",False,"El Segundo libro de Moysen, llamado Exodo",40,None),
 "Lev":("LEV","Levítico","OT",False,"El Tercero libro de Moysen, llamado comunmente Leuitico",27,None),
 "Num":("NUM","Números","OT",False,"El Quarto libro de Moysen [llamado Numeros]",36,"title continuation not read"),
 "Deut":("DEU","Deuteronomio","OT",False,"El Quinto libro de Moysen [llamado Deuteronomio]",34,"title continuation not read"),
 "Josh":("JOS","Josué","OT",False,"El libro de Iosue",24,None),
 "Judg":("JDG","Jueces","OT",False,"El libro de los Iuezes",21,None),
 "Ruth":("RUT","Rut","OT",False,"El libro de Ruth",4,None),
 "1Sam":("1SA","1 Samuel","OT",False,"El primero libro de Samuel, llamado comunmente Primero delos reyes",31,None),
 "2Sam":("2SA","2 Samuel","OT",False,"El libro Segundo de Samuel, o, de los reyes",24,None),
 "1Kgs":("1KI","1 Reyes","OT",False,"El tercero libro de los reyes, y primero segun los Ebreos",22,None),
 "2Kgs":("2KI","2 Reyes","OT",False,"Segundo libro de los reyes",25,"1569 colophons number Kings by the Hebrew count (FIN DEL PRIMERO / SEGVNDO LIBRO de los reyes)"),
 "1Chr":("1CH","1 Crónicas","OT",False,"Libro primero de las Chronicas",29,"title read from running head; title block not isolated in OCR"),
 "2Chr":("2CH","2 Crónicas","OT",False,"El Segundo libro de las Chronicas",36,None),
 "PrMan":("MAN","Oración de Manasés","OT",True,"La Oracion conque Manasse Rey de Iuda oró estando preso en Babylonia: laqual por no hallarse en el texto Hebreo, se suele contar con los libros apochryphos",1,"single prayer, no chapter division expected; 1569 note says it is not found in the Hebrew text and is counted among the apocryphal books"),
 "Ezra":("EZR","Esdras","OT",False,"El libro de Esdras dicho comunmente el Primero",10,None),
 "Neh":("NEH","Nehemías","OT",False,"El libro de Nehemias comunmente dicho Segundo de Esdras",13,None),
 "1Esd":("1ES","3 Esdras","OT",True,"El Tercero libro de [Esdras] apochrypho",9,"OSIS 1Esd = Vulgate 3 Esdras; colophon reads 'FIN DEL TERCERO LIBRO DE Esdras apochrypho'"),
 "2Esd":("2ES","4 Esdras","OT",True,"El quarto libro de Esdras",16,"OSIS 2Esd = Vulgate 4 Esdras"),
 "Tob":("TOB","Tobías","OT",True,"El libro de Tobias",14,None),
 "Jdt":("JDT","Judit","OT",True,"El libro de Iudith",16,None),
 "Esth":("EST","Ester (con los pasajes griegos)","OT",False,"El libro de Esther",None,"canonical book with the Greek additions (Wikipedia list); how 1569 divides/places the Greek passages not yet checked, so chapter count left null"),
 "Job":("JOB","Job","OT",False,"El libro [de Iob]",42,"title word after 'El libro' not legible in OCR"),
 "Ps":("PSA","Salmos","OT",False,"Los Psalmos de Dauid",150,"printed in five books (Libro Segundo, tercero, ... quinto colophons found)"),
 "Prov":("PRO","Proverbios","OT",False,"Los prouerbios de Salomon",31,"incipit used as title; separate title line not isolated"),
 "Eccl":("ECC","Eclesiastés","OT",False,"Ecclesiaste, o el Predicador de Salomon",12,None),
 "Song":("SNG","Cantares","OT",False,"El libro delos Cantares de Salomon",8,None),
 "Wis":("WIS","Sabiduría","OT",True,"El libro dela Sabiduria comunmente dicho, de Salomon",19,None),
 "Sir":("SIR","Eclesiástico","OT",True,"El libro de la Sabiduria de Iesus hijo de Sirach, llamado comunmente Ecclesiastico",51,"preceded by 'La prefacio del autor'"),
 "Isa":("ISA","Isaías","OT",False,"[Las prophecias de] Isayas",66,"no title line isolated in OCR; name from colophon 'FIN DE LAS PROPHECIAS de Isayas'"),
 "Jer":("JER","Jeremías","OT",False,"El libro delas prophecias de Ieremias",52,None),
 "Lam":("LAM","Lamentaciones","OT",False,"Las Lamentaciones, o, Endechas de Ieremias",5,None),
 "Bar":("BAR","Baruc","OT",True,"La prophecia de Baruch",None,"whether the Epistle of Jeremiah is printed as Baruch ch. 6 not yet checked"),
 "Ezek":("EZK","Ezequiel","OT",False,"[La prophecia de] Ezechiel",48,None),
 "Dan":("DAN","Daniel (con los pasajes griegos)","OT",False,"La prophecia de Daniel",None,"canonical book with Azarias/Tres jovenes, Susana, Bel y el Dragon (Wikipedia list); 1569 chapter division of the Greek parts not yet checked"),
 "Hos":("HOS","Oseas","OT",False,"Las prophecias de Oseas",14,"opens the section 'El libro delos doze Prophetas, que llaman Menores'"),
 "Joel":("JOL","Joel","OT",False,"La prophecia de Ioel",3,None),
 "Amos":("AMO","Amós","OT",False,"Amos Propheta",9,None),
 "Obad":("OBA","Abdías","OT",False,"Prophecia de Abdias",1,None),
 "Jonah":("JON","Jonás","OT",False,"Prophecia de Ionas Propheta",4,None),
 "Mic":("MIC","Miqueas","OT",False,"La prophecia de [Micheas]",7,None),
 "Nah":("NAM","Nahúm","OT",False,"Nahum Propheta",3,None),
 "Hab":("HAB","Habacuc","OT",False,"Habacuc Propheta",3,None),
 "Zeph":("ZEP","Sofonías","OT",False,"Sophonias",3,"previous book colophon on the same leaf reads FIN DE HABACVC"),
 "Hag":("HAG","Hageo","OT",False,"El Propheta Aggeo",2,None),
 "Zech":("ZEC","Zacarías","OT",False,"Zacharias Propheta",14,None),
 "Mal":("MAL","Malaquías","OT",False,"La prophecia de Malachias",4,None),
 "1Macc":("1MA","1 Macabeos","OT",True,"El primer libro delos Machabeos",16,None),
 "2Macc":("2MA","2 Macabeos","OT",True,"El segundo libro delos Machabeos",15,None),
 "Matt":("MAT","Mateo","NT",False,"El Sancto Euangelio de nuestro Señor Iesu Christo segun S. Mattheo",28,None),
 "Mark":("MRK","Marcos","NT",False,"El Sancto Euangelio de nuestro Señor Iesu Christo segun S. Marcos",16,None),
 "Luke":("LUK","Lucas","NT",False,"[El Sancto Euangelio ... segun] S. Lucas",24,"title block not isolated in OCR; name from colophon"),
 "John":("JHN","Juan","NT",False,"El Sancto Euangelio de nuestro Señor Iesu Christo segun S. Ioan",21,None),
 "Acts":("ACT","Hechos","NT",False,"El Segundo libro de S. Lucas llamado los Actos de los Apostoles",28,None),
 "Rom":("ROM","Romanos","NT",False,"La epistola del Apostol S. Paulo alos Romanos",16,"preceded by the section title 'Las epistolas delos Apostoles'"),
 "1Cor":("1CO","1 Corintios","NT",False,"La Primera epistola del Apostol S. Paulo a los Corinthios",16,None),
 "2Cor":("2CO","2 Corintios","NT",False,"La Segunda Epistola del Apostol S. Paulo a los Corinthios",13,None),
 "Gal":("GAL","Gálatas","NT",False,"La Epistola del Apostol S. Paulo alos Galatas",6,None),
 "Eph":("EPH","Efesios","NT",False,"La Epistola del Apostol S. Paulo alos Ephesios",6,None),
 "Phil":("PHP","Filipenses","NT",False,"La Epistola del Apostol S. Paulo a los Philippenses",4,None),
 "Col":("COL","Colosenses","NT",False,"La Epistola del Apostol S. Paulo alos Colossenses",4,None),
 "1Thess":("1TH","1 Tesalonicenses","NT",False,"La Primera epistola del Apostol S. Paulo alos Thessalonicenses",5,None),
 "2Thess":("2TH","2 Tesalonicenses","NT",False,"La Segunda Epistola del Apostol S. Paulo a los Thessalonicenses",3,None),
 "1Tim":("1TI","1 Timoteo","NT",False,"La Primera Epistola del Apostol S. Paulo a Timotheo",6,None),
 "2Tim":("2TI","2 Timoteo","NT",False,"La Segunda Epistola del Apostol S. Paulo a Timotheo",4,None),
 "Titus":("TIT","Tito","NT",False,"La epistola del Apostol S. Paulo a Tito",3,None),
 "Phlm":("PHM","Filemón","NT",False,"[La epistola del Apostol S. Paulo] a Philemon",1,"title block not isolated in OCR"),
 "Heb":("HEB","Hebreos","NT",False,"La Epistola del Apostol S. Paulo a los Hebreos",13,None),
 "Jas":("JAS","Santiago","NT",False,"La Epistola vniuersal de S. Tiago",5,None),
 "1Pet":("1PE","1 Pedro","NT",False,"La Primera epistola Vniuersal de S. Pedro Apostol",5,None),
 "2Pet":("2PE","2 Pedro","NT",False,"La segunda epistola Vniuersal de S. Pedro Apostol",3,None),
 "1John":("1JN","1 Juan","NT",False,"La primera Epistola Vniuersal de San Ioan Apostol",5,None),
 "2John":("2JN","2 Juan","NT",False,"La Segunda Epistola de San Ioan Apostol",1,None),
 "3John":("3JN","3 Juan","NT",False,"La Tercera Epistola de San Ioan Apostol",1,None),
 "Jude":("JUD","Judas","NT",False,"La Epistola Vniuersal de S. Iudas Apostol",1,None),
 "Rev":("REV","Apocalipsis","NT",False,"El Apocalypsi, o, Reuelacion de S. Ioan el Theologo",22,None),
}
# books that are (or contain) deuterocanonical material per es.wikipedia 'Biblia del oso'
GREEK_PARTS = {"Esth": "pasajes griegos de Ester", "Dan": "Oracion de Azarias y Cantico de los tres jovenes, Susana, Bel y el Dragon"}

IMG_CHECKED = {"Gen","PrMan","Esth","Zeph","Rev"}  # leaf images viewed 2026-10-16: n36, n464, n558, n959, n1262

djvu = open(os.path.join(ROOT, "src", "djvu.txt"), encoding="utf-8").read()
lines = djvu.split("\n")
line_off = [0]
for l in lines:
    line_off.append(line_off[-1] + len(l) + 1)

# OCR chapter-heading census (corroboration only)
ROM = {"I":1,"V":5,"X":10,"L":50,"C":100}
def roman(s):
    s = s.upper().replace("1","I").replace("Í","I")
    s = re.sub(r"[^IVXLC]", "", s)
    if not s or not re.fullmatch(r"C{0,1}(XC|XL|L?X{0,3})(IX|IV|V?I{0,4})", s): return None
    t = 0
    for i, c in enumerate(s):
        v = ROM[c]; t += -v if i+1 < len(s) and ROM[s[i+1]] > v else v
    return t or None
HEAD = re.compile(r"^\s*C\s*A\s*P\s*I\s*T\s*[VU]?\s*L?\s*O?\s*[\.,:]?\s*([IVXLC1]{1,8})[\.,:]?\s*$")

order = []
for k, (osis, ln, kind, hint) in enumerate(ANCHORS):
    nxt = ANCHORS[k+1][1] if k+1 < len(ANCHORS) else END_LINE_EXCLUSIVE
    s, e = line_off[ln-1], line_off[nxt-1]   # [s, e)
    order.append((osis, ln, nxt, s, e, kind, hint))

books = []
for i, (osis, ln, nxt, s, e, kind, hint) in enumerate(order, 1):
    code, es, test, deut, title, ch, chnote = META[osis]
    lf_s, lf_e = leafmap.offset_to_leaf(s), leafmap.offset_to_leaf(max(s, e-1))
    # if the anchor sits in the last few hundred chars of a leaf (after the previous book's
    # colophon), the book's own text begins on the next leaf
    LO = leafmap._data()["leaf_start_offset"]
    if lf_s + 1 < len(LO) and len(re.sub(r"\s", "", djvu[s:LO[lf_s+1]])) < 300 and lf_s < lf_e:
        lf_s += 1
    notes = []
    if chnote: notes.append(chnote)
    if osis in GREEK_PARTS: notes.append("contains deuterocanonical Greek passages: " + GREEK_PARTS[osis])
    notes.append("boundary anchor (%s): %s" % (kind, hint))
    books.append({
        "n": i,
        "osis": osis,
        "code": code,
        "title_1569": title,
        "title_1569_status": ("checked against leaf image" if osis in IMG_CHECKED else "cleaned from OCR, not yet checked against leaf image"),
        "name_es": es,
        "testament": test,
        "deuterocanonical": deut or osis in GREEK_PARTS,
        "deuterocanonical_kind": ("whole book" if deut else ("Greek additions inside canonical book" if osis in GREEK_PARTS else None)),
        "chapters": ch,
        "chapters_source": ("traditional division, expected; not yet counted in the facsimile" if ch is not None else None),
        "djvu": {"line_start": ln, "line_end_exclusive": nxt, "char_start": s, "char_end_exclusive": e,
                 "precision": "about one leaf: two-column OCR interleaves text at transitions"},
        "leaves": {"start": lf_s, "end": lf_e,
                   "start_url": leafmap.leaf_url(lf_s), "end_url": leafmap.leaf_url(lf_e)},
        "printed_pages": None,
        "notes": notes,
    })

out = {
    "edition": "La Biblia, que es, los sacros libros del Viejo y Nuevo Testamento. Trasladada en Español. [Basilea], 1569 (Casiodoro de Reina) - Biblia del Oso",
    "source": {"facsimile": "https://archive.org/details/la-biblia-del-oso", "ocr": "src/djvu.txt (archive.org 'La Biblia del Oso_djvu.txt')",
               "leaf_index": "archive.org _hocr_pageindex.json.gz via pipeline/leafmap.py", "license": "Public Domain Mark 1.0 (archive.org item)"},
    "generated": "2026-10-16",
    "book_count": len(books),
    "order_note": "Printed 1569 order (from OCR title blocks and FIN DEL... colophons). Deuterocanonical books sit inside the Old Testament in the Vulgate-style order; NT follows the traditional order with Hebrews after Philemon.",
    "printed_pages_note": "archive.org page_numbers.json detected no printed folio numbers for this item (all null), so printed_pages is null; leaves are archive.org 0-based leafNum.",
    "front_matter": {"djvu": {"line_start": 1, "line_end_exclusive": ANCHORS[0][1], "char_start": 0, "char_end_exclusive": line_off[ANCHORS[0][1]-1]},
                     "leaves": {"start": 0, "end": leafmap.offset_to_leaf(line_off[ANCHORS[0][1]-1]-1)},
                     "contents": "title page, Tridentine decree, Latin Praefatio, Amonestacion, annotations ('El fin.' line 2989)"},
    "back_matter": {"djvu": {"line_start": END_LINE_EXCLUSIVE, "char_start": line_off[END_LINE_EXCLUSIVE-1], "char_end_exclusive": len(djvu)},
                    "leaves": {"start": leafmap.offset_to_leaf(line_off[END_LINE_EXCLUSIVE-1]), "end": leafmap.offset_to_leaf(len(djvu)-1)},
                    "contents": "errata table 'Los errores que en la impression no se pudieron escusar...' and after"},
    "books": books,
}
json.dump(out, open(os.path.join(ROOT, "books.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

status = {"generated": "2026-10-16", "unit": "verse",
          "note": "Counts are verses per status. All 0: no verse has been segmented into the oso1569 store as of this file (pipeline/segment.py drafts are not counted). 'verified' only by humans (SPEC 5).",
          "totals": {"ocr": 0, "corrected": 0, "verified": 0},
          "books": [{"osis": b["osis"], "code": b["code"], "ocr": 0, "corrected": 0, "verified": 0} for b in books]}
json.dump(status, open(os.path.join(ROOT, "status.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for b in books:
    print(b["n"], b["osis"], b["code"], b["deuterocanonical"], b["chapters"], b["leaves"]["start"], b["leaves"]["end"], b["djvu"]["char_end_exclusive"]-b["djvu"]["char_start"])
