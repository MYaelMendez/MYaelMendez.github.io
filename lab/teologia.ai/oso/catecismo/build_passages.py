#!/usr/bin/env python3
"""Build catecismo/passages.json (Small Catechism core passages, Biblia del Oso 1569).
orig     = archive.org djvu.txt OCR, cleaned only of marginal glosses, cross-ref margins,
           line-end noise, verse numbers and page catchwords/headers (line breaks joined;
           hyphenation and all OCR errors kept).
proposed = agent's proposed 1569-orthography reading: OCR errors corrected using the OCR
           itself plus an agent look at the archive.org IIIF page image (1600px). NOT verified.
"""
import json, re, difflib, os
HERE = os.path.dirname(os.path.abspath(__file__))
SCAN = "archive.org/details/la-biblia-del-oso"
IIIF = "https://iiif.archive.org/iiif/la-biblia-del-oso%24{leaf}/full/1600,/0/default.jpg"

# (book, ch, v, leaf, djvu_lines, orig, proposed, notes, confidence)
V = [
("EXO",20,1,104,"15449-15450","Habló Dios todas eftas palabras, di- ziendo.",
 "Y Habló Dios todas eſtas palabras, diziendo.",
 ["Initial 'Y' is a large woodcut drop-cap absent from the OCR; seen on the page image (leaf 104). 'Habló' printed in capitals after the initial."],"high"),
("EXO",20,2,104,"15453-15455","Yo/fy IehouatuDios, quetefa- qué de la tierra de Egypto, de caía de (ier- yos,",
 "Yo ſoy Iehoua tu Dios, que te ſaqué de la tierra de Egypto, de caſa de ſieruos,",
 ["'ſoy' is set in italic (supplied word), per page image."],"high"),
("EXO",20,3,104,"15456-15458","* Notendrás diofes agenos delante de mi.",
 "No tendrás dioſes agenos delante de mi.",[],"high"),
("EXO",20,4,104,"15462-15466","*Noreharásimagé, ni ninguna feme- janga decofa quee/fié arriba enel ciclo, nia- baxo en la tierra, ni en las aguas debaxo de la tierra.",
 "No te harás imagẽ, ni ninguna ſemejança de coſa que eſté arriba enel cielo, ni abaxo en la tierra, ni en las aguas debaxo de la tierra.",
 ["'de coſa' and 'eſté' are set in italic (supplied words), per page image.","'enel' is printed joined (period usage), kept."],"high"),
("EXO",20,5,104,"15467-15470","Noteinclinarás 1 ellas , ni las honrra- rás : porque yo /oy Ichoua tu Dios, Fuerte, Zelofo , que vifito la maldad de los padres fobrelos hijos,h fobrelos terceros y fobre los quartos,1los que me aborrecen:",
 "No te inclinarás à ellas, ni las honrrarás: porque yo ſoy Iehoua tu Dios, Fuerte, Zeloſo, que viſito la maldad de los padres ſobre los hijos, ſobre los terceros y ſobre los quartos, à los que me aborrecen:",
 ["'ſoy' italic (supplied).","Superscript note letter 'h' before 'ſobre los terceros' omitted (margin: 'En la tercera y quarta generacion').","Verse continues into v6 with no full stop, as printed."],"high"),
("EXO",20,6,104,"15472-15474","Yquehago mifericordiaien millares 3los que meaman, y guardan mis manda- mientos.",
 "Y que hago miſericordia en millares à los que me aman, y guardan mis mandamientos.",
 ["Superscript note letter 'i' after 'miſericordia' omitted (margin: 'S. de generaciones')."],"high"),
("EXO",20,7,104,"15475-15478","*Notomarás el Nombre de lehoua tu Dios en vano: porque t no dará porinno- centeIehouaál que tomare fu Nombre en vano.",
 "No tomarás el Nombre de Iehoua tu Dios en vano: porque no dará por innocente Iehoua àl que tomare ſu Nombre en vano.",
 ["Dagger note mark after 'porque' omitted (margin: 'Heb. no absoluerá Iehoua &c.').","'àl' with grave accent as printed."],"high"),
("EXO",20,8,104,"15479-15481","» Acordartchás del dia del Sabbado, para fanétificarlo.",
 "Acordartehás del dia del Sabbado, para ſanctificarlo.",
 ["'Acordartehás' printed as one word (te + hás), per page image."],"high"),
("EXO",20,9,104,"15483","Seysdiasobrarás, y harás toda tu o-",
 "Seys dias obrarás, y harás toda tu obra,",
 ["OCR drops the second line 'bra,' (it was merged into the margin column). Line 'bra,' is visible on the page image, leaf 104. Not invented: read from facsimile; verify."],"high"),
("EXO",20,10,104,"15487-15491","MaselSeptimo diafera Sabbadoále- houa tu Dios: no hagas obra ninguna, tu, ni tuhijo,ni tu hija, n1 tu eruo, ni tu cria- da,ni ru bellia,ni tu eftrágero,que esta! de- tro de tus puertas.",
 "Mas el Septimo dia ſera Sabbado à Iehoua tu Dios: no hagas obra ninguna, tu, ni tu hijo, ni tu hija, ni tu ſieruo, ni tu criada, ni tu beſtia, ni tu eſtrãgero, que eſta dẽtro de tus puertas.",
 ["'ſera' and 'eſta' are italic (supplied); accentuation of italic forms not certain at this resolution.","Note letter 'l' after 'eſta' omitted (margin: 'En tus villas, o poblaciones').","Nasal abbreviation over a/e (eſtrãgero, dẽtro) rendered with tilde; in this typeface the mark can look acute/grave: verify glyph."],"high"),
("EXO",20,11,104,"15492-15496","*Porqueen feys dias hizo Ichoua los cielos y la tierra, la mar y todas las cofas 4 en ello ay: y enel dia Septimó repofó: por tanto Iehoua bendixo al día del Sabbado, y lo fanétificó..",
 "Porque en ſeys dias hizo Iehoua los cielos y la tierra, la mar y todas las coſas q̃ en ello ay: y en el dia Septimó repoſó: por tanto Iehoua bendixo àl dia del Sabbado, y lo ſanctificó.",
 ["OCR '4' is the abbreviation q̃ (que).","'ay' italic (supplied). Printed 'en ello' (not 'ellos').","Accent in 'Septimó' appears in the print; kept as seen, verify."],"high"),
("EXO",20,12,104,"15497-15499","*Honrraá tu padre y 3tu madre, por que tus dias fean alargados fobrela tierra, quelehoua tu Dios te dá.",
 "Honrra à tu padre y à tu madre, por que tus dias ſean alargados ſobre la tierra, que Iehoua tu Dios te dá.",
 ["'por que' split across a line break without hyphen; kept as two words, verify."],"high"),
("EXO",20,13,105,"15505","NO matarás.",
 "No matarás.",["Starts leaf 105 (printed page 139)."],"high"),
("EXO",20,14,105,"15506","Nocometerás adulterio.","No cometerás adulterio.",[],"high"),
("EXO",20,15,105,"15507","Nohurtarás.","No hurtarás.",[],"high"),
("EXO",20,16,105,"15508-15509","Nohablarás contratu proximo falío teflimonio.",
 "No hablarás contra tu proximo falſo teſtimonio.",[],"high"),
("EXO",20,17,105,"15511-15515","* No cobdiciarás la caía de tu proxi- MONO cobdiciarás la muger de tu pro- ximo, ni fu ieruo, ni fu criada, nifu buey, ni fu afno, ni.cofa alguna de tu proxi-",
 "No cobdiciarás la caſa de tu proximo, no cobdiciarás la muger de tu proximo, ni ſu ſieruo, ni ſu criada, ni ſu buey, ni ſu aſno, ni coſa alguna de tu proximo.",
 ["OCR 'MONO' = 'mo, no' (lower-case 'no' after a comma in the print).","Final line 'mo.' is missing from the OCR; read from the page image (leaf 105). Verify."],"high"),

("MAT",6,9,1030,"184733-184737","Vofotros pues orareys anfi:* Padre aueftro,que eltás en los cielos, Sea fanéti- ficado tu Nombre.",
 "Voſotros pues orareys anſi: Padre nueſtro, que eſtás en los cielos, Sea ſanctificado tu Nombre.",
 ["Cross-reference asterisk before 'Padre' omitted (margin: Luc. 11,2)."],"high"),
("MAT",6,10,1030,"184738-184739","VégatuReyno.Sea hecha tu volútad, como en el cielo,anfí tambien en la tierra.",
 "Vẽga tu Reyno. Sea hecha tu volũtad, como en el cielo, anſi tambien en la tierra.",
 ["'anſi' italic (supplied).","Nasal abbreviations (Vẽga = Venga, volũtad = voluntad) rendered with tilde; the mark on 'Vẽga' looks acute in this type: verify glyph."],"high"),
("MAT",6,11,1030,"184740","1 Danos oy nueftro pan quotidiano.","Danos oy nueſtro pan quotidiano.",[],"high"),
("MAT",6,12,1030,"184741-184744","Y fueltanos nueftras € deudas,como tambien nofotros foltamos d ánucítros deudores.",
 "Y ſueltanos nueſtras deudas, como tambien noſotros ſoltamos à nueſtros deudores.",
 ["Note letters 'c' (margin: 'Offenſas') and 'd' (margin: 'A los que nos han offendido') omitted."],"high"),
("MAT",6,13,1030,"184745-184748","Y nonos metas en tentacion: mas li- branos xk de mal : porque tuyo es el Rey- no, y la potécia,y la gloria, por todos los fi- glos.Amen.",
 "Y no nos metas en tentacion: mas libranos de mal: porque tuyo es el Reyno, y la potẽcia, y la gloria, por todos los ſiglos. Amen.",
 ["Cross-reference asterisk before 'de mal' omitted.","'todos' appears italic (supplied): verify.","'potẽcia' nasal mark looks acute in this type: verify glyph."],"high"),

("MAT",26,26,1053,"189325-189328","*Y comiendo ellos,tomó Iefus el pá, mauiendo hecho gracias, Ppartiólo,ydió a fus Difcipulos, y dixo,Tomad , comed: Oelto es mi cuerpo.",
 "Y comiendo ellos, tomó Ieſus el pã, y auiendo hecho gracias, partiólo, y dió à ſus Diſcipulos, y dixo, Tomad, comed: eſto es mi cuerpo.",
 ["The 'y' before 'auiendo' is lost in the OCR (stray '¿4' at line end); it is visible at the start of the line on the page image (leaf 1053).","Note letters m ('Ot. bendixo, y &c.'), n ('G. quebró'), o ('Ot. eſte') omitted.","'pã' (pan) nasal mark looks acute in this type: verify glyph."],"high"),
("MAT",26,27,1053,"189329-189330","Y tomandoel valo, y hechas gracias, dióles diziendo,Bcued decl todos.",
 "Y tomando el vaſo, y hechas gracias, dióles diziendo, Beued deel todos.",[],"high"),
("MAT",26,28,1053,"189331-189333","PorquePeltoes mifangre del Nueuo teltamento, la qual es derramada por mu- chos para remifsion delos peccados.",
 "Porque eſto es mi ſangre del Nueuo teſtamento, la qual es derramada por muchos para remiſsion de los peccados.",
 ["Note letter 'p' omitted (margin: 'Eſto es el Nueuo Teſ. (confirmado) con mi ſangre')."],"high"),

("MAT",28,19,1057,"190145-190147","*Portantoid, enfeñad a todas las gé- tes; baptizandolos ennombre del Padre, y del Hijo, y del Efpiritufantto:",
 "Portanto id, enſeñad à todas las gẽtes; baptizandolos en nombre del Padre, y del Hijo, y del Eſpiritu ſancto:",
 ["'Portanto' printed joined; kept.","'ſancto' lower-case as printed; OCR 'tt' = ct-ligature.","Verse ends with colon; sense continues into v20."],"high"),

("MRK",16,16,1076,"193905-193907","Elquecreycre,y fuere baptizado,ferá faluo: | mas elque no creyere,ferá conde- nado.",
 "Elque creyere, y fuere baptizado, ſerá ſaluo: mas elque no creyere, ſerá condenado.",
 ["'Elque'/'elque' printed joined; kept.","Dagger note mark before 'mas' (OCR '|') omitted."],"high"),

("LUK",11,2,1092,"196828-196834","Y dixoles, Quando orardes, dezid, Padre nueftro, que cftás enlos cielos, fea tu Nombre fanétificado:Venga tuReyno: fea hecha tu voluntad como enel cielo «rfi tambien en la tierra.",
 "Y dixoles, Quando orardes, dezid, Padre nueſtro, que eſtás en los cielos, ſea tu Nombre ſanctificado: Venga tu Reyno: ſea hecha tu voluntad como enel cielo anſi tambien en la tierra.",
 ["Cross-reference asterisk at verse start omitted (margin: Mat. 6,9).","'anſi' italic (supplied).","No comma before 'anſi' in the print (unlike Mat 6:10)."],"high"),
("LUK",11,3,1092,"196835-196836","El pannueltro de cada dia danos lo oy:",
 "El pan nueſtro de cada dia danos lo oy:",["'lo' italic (supplied)."],"high"),
("LUK",11,4,"1092-1093","196837-196845","E Y perdonanos mueftros peccados, por. que tambié nolorros perdonamos i todos losque nos deuen. Y no nos metas en ten- tacion,mas libranos de mal.",
 "Y perdonanos nueſtros peccados, porque tambiẽ noſotros perdonamos à todos losque nos deuen. Y no nos metas en tentacion, mas libranos de mal.",
 ["Verse crosses from leaf 1092 to 1093. 'losque' at the foot of leaf 1092 is the printer's catchword, repeated as the first word of leaf 1093; counted once. Running head '7 SEGUN $' removed from orig.","'losque' printed joined; kept."],"high"),

("JHN",20,22,1135,"204749-204750","Y como vuo dicho cfto,fopló,y dixo- les, Tomad el EfpirituSandto.",
 "Y como vuo dicho eſto, ſopló, y dixoles, Tomad el Eſpiritu Sancto.",
 ["OCR 'Za' = verse number 22. No 'les' before 'ſopló' in 1569."],"high"),
("JHN",20,23,1135,"204751-204753","Alosquefoltardeslos peccados, les fon fueltos : ¿los quelos retuuierdes, fe- rán retenidos .",
 "A los que ſoltardes los peccados, les ſon ſueltos: à los que los retuuierdes, ſerán retenidos.",[],"high"),

("ROM",6,4,1174,"212026-212030","*Porquefomos fepultados juntamen* te con el a muerte por cl Baptifmo, parag comoel' Chrifto refuftitó de los muertos ¿3 gloría del Padre, * anfí tambien nofo- tros 1 andemos en novedad de vida.",
 "Porque ſomos ſepultados juntamente con el a muerte por el Baptiſmo, paraq̃ como el Chriſto reſuſcitó de los muertos à gloria del Padre, anſi tambien noſotros andemos en nouedad de vida.",
 ["Note letters (k before 'Chriſto', i before 'à gloria', l before 'andemos') and cross-ref asterisk omitted.","'paraq̃' printed joined with q-tilde.","'nouedad' with u as printed (OCR gave 'novedad').","Accent on 'a muerte' not checked on the image; kept as OCR (no accent): verify."],"medium-high"),

("1CO",11,23,1192,"215307-215309","Porque yo recebi del Señor lod tam- bienhos he\"enfeñado¿Que el Señor Iefus, la noche que fueentregado ,tomó el pan:",
 "Porque yo recebi del Señor loq̃ tambien hos he enſeñado: Que el Señor Ieſus, la noche que fue entregado, tomó el pan:",
 ["OCR 'lod' = 'loq̃' (lo que), confirmed on page image.","Note letter before 'enſeñado' omitted."],"high"),
("1CO",11,24,1192,"215310-215313","Y auiédo hecho gracias lo partió, y di. xo,*Tomad,[y]comed:*elto esmi cuerpo que porvolotros es* partido : hazedefto er memoria de mi.",
 "Y auiẽdo hecho gracias lo partió, y dixo, Tomad, [y] comed: eſto es mi cuerpo que por voſotros es partido: hazed eſto en memoria de mi.",
 ["'[y]' is Reina's own bracket for a supplied word: printed, not editorial.","Cross-ref asterisks and note letter 'x' omitted.","'es mi' printed tight ('esmi'); separated: verify."],"high"),
("1CO",11,25,1192,"215315-215321","Anfimiímo tomó tábien el vafo,defpues deauercenado, diziendo, Elte vafo es el Nucuo teftaméto “en mi fangre: hazed ef- to todas las vezes que beuercys, eu memo ria de mi.",
 "Anſimiſmo tomó tãbien el vaſo, deſpues de auer cenado, diziendo, Eſte vaſo es el Nueuo teſtamẽto en mi ſangre: hazed eſto todas las vezes que beuereys, en memoria de mi.",
 ["'Anſimiſmo' printed joined; 'tomó' italic (supplied).","Note letter 'u' before 'en mi ſangre' omitted.","Nasal marks (tãbien, teſtamẽto) look acute in this type: verify glyph."],"high"),

("TIT",3,5,1235,"223423-223427","*Noporlas obras dejufticia quenofo- tros aujamos hecho,mas por fu mifericor- dia,nos faluó por el lauamiento b delare- generacion,y de la renouacion“del Efpiri- tuSantto,",
 "No por las obras de juſticia que noſotros auiamos hecho, mas por ſu miſericordia, nos ſaluó por el lauamiento de la regeneracion, y de la renouacion del Eſpiritu Sancto,",
 ["Note letters b, c and cross-ref asterisk omitted.","'juſticia' with j as printed."],"high"),
("TIT",3,6,1235,"223428-223429","El qual derramó en nofotros abundáte- méte porlefus el ChriftoSaluador nueftro:",
 "El qual derramó en noſotros abundãtemẽte por Ieſus el Chriſto Saluador nueſtro:",
 ["Print is tight ('porIeſus elChriſtoSaluador'); words separated: verify.","Nasal marks look acute in this type: verify glyph."],"high"),
("TIT",3,7,1235,"223431-223433","Para quejuftificados confu gracia, fea- mos hechos herederos fegun la efperanga dela vida eterna.",
 "Para que juſtificados con ſu gracia, ſeamos hechos herederos ſegun la eſperança de la vida eterna.",[],"high"),
("TIT",3,8,1235,"223434-223437","dPalabraficles,y efto quiero que affir- mes,Que los que creená Dios , procuren gouernaríe en buenas obras. clto eslo bue no y lo val a los hombres.",
 "Palabra fiel es, y eſto quiero que affirmes, Que los que creen á Dios, procuren gouernarſe en buenas obras. eſto es lo bueno y lo vtil à los hombres.",
 ["Note letter 'd' omitted (margin: 'Como 1. Tim. 1,15').","OCR 'val' = 'vtil', confirmed on page image. 'eſto' lower-case after full stop, as printed.","'á Dios' (acute) and 'à los hombres' (grave) as they appear: verify."],"high"),
]

BOOKNAME = {"EXO":"Éxodo","MAT":"Mateo","MRK":"Marcos","LUK":"Lucas","JHN":"Juan","ROM":"Romanos","1CO":"1 Corintios","TIT":"Tito"}

def classify(a, b):
    if a.replace("f", "ſ") == b: return "long-s: OCR 'f' → 'ſ'"
    if a.replace("-", "") == b or a.replace("- ", "") == b: return "line-break hyphen joined"
    if a.endswith("-") and b.startswith(a[:-1]): return "line completed from facsimile (missing in OCR)"
    return "OCR error corrected"

def changes(orig, prop):
    o = orig.replace("- ", "").split(); p = prop.split()
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, o, p, autojunk=False).get_opcodes():
        if tag == "equal": continue
        a = " ".join(o[i1:i2]); b = " ".join(p[j1:j2])
        kind = "added from facsimile / split" if tag == "insert" else ("removed (note mark / noise)" if tag == "delete" else classify(a, b))
        out.append({"ocr": a, "proposed": b, "kind": kind})
    return out

rows = []
for (bk, ch, vs, leaf, lines, orig, prop, notes, conf) in V:
    leaves = [int(x) for x in str(leaf).split("-")]
    rows.append({
        "id": f"oso1569:{bk}.{ch}.{vs}", "book": bk, "chapter": ch, "verse": vs,
        "orig": orig, "proposed": prop, "norm": None,
        "page": {"scan": SCAN, "leaf": leaves[0] if len(leaves) == 1 else leaves, "bbox": None,
                 "image": [IIIF.format(leaf=l) for l in leaves]},
        "status": "corrected-proposed",
        "evidence": {"ocr_src": SCAN + " (djvu.txt)", "djvu_lines": lines,
                     "corrected_by": "agent:hark (proposal; OCR + agent look at IIIF page image)",
                     "verified_by": None, "sha256": None},
        "confidence": conf,
        "changes": changes(orig, prop),
        "notes": notes + ["Human must verify 'proposed' against the facsimile before any status change (SPEC §5: only humans mark verified)."],
    })

PASSAGES = [
 ("Éxodo 20:1-17", "EXO", 20, range(1, 18), "Mandamientos"),
 ("Mateo 6:9-13", "MAT", 6, range(9, 14), "Padrenuestro"),
 ("Lucas 11:2-4", "LUK", 11, range(2, 5), "Padrenuestro"),
 ("Mateo 28:19", "MAT", 28, [19], "Bautismo (1ª parte: qué es)"),
 ("Marcos 16:16", "MRK", 16, [16], "Bautismo (2ª parte: qué da)"),
 ("Tito 3:5-8", "TIT", 3, range(5, 9), "Bautismo (3ª parte: cómo lo hace)"),
 ("Romanos 6:4", "ROM", 6, [4], "Bautismo (4ª parte: qué significa)"),
 ("Juan 20:22-23", "JHN", 20, [22, 23], "Confesión / Oficio de las llaves"),
 ("Mateo 26:26-28", "MAT", 26, range(26, 29), "Santa Cena"),
 ("1 Corintios 11:23-25", "1CO", 11, range(23, 26), "Santa Cena"),
]
out = {
  "edition": "Biblia del Oso, Casiodoro de Reina, Basilea 1569 (dominio público)",
  "scan": SCAN, "spec": "ae.spec/0.1 §3 (+ fields 'proposed', 'changes', 'confidence')",
  "status_note": "status 'corrected-proposed' = agent proposal, NOT verified. A human must check every 'proposed' against the facsimile leaf before marking 'corrected'/'verified'.",
  "conventions": {
    "orig": "OCR text cleaned only of margin glosses, cross-ref margins, line-end noise, verse numbers, catchwords and running heads; OCR errors and hyphens kept; in-line note marks kept as OCR'd.",
    "proposed": "1569 orthography: ſ (long s), u/v and i/j as printed, nasal abbreviation as tilde (ã ẽ ũ q̃), grave/acute accents as seen. Superscript note letters and cross-ref asterisks omitted. Reina's own [ ] kept. Italic (supplied) words listed in notes, not marked in text.",
    "verse_bounds": "from the SSE 1569 grid (boundaries only; no grid text used)."
  },
  "passages": [{"ref": r, "catechism_part": part,
                "verses": [x for x in rows if x["book"] == b and x["chapter"] == c and x["verse"] in vs]}
               for (r, b, c, vs, part) in PASSAGES],
}
json.dump(out, open(os.path.join(HERE, "passages.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(sum(len(p["verses"]) for p in out["passages"]), "verses")
