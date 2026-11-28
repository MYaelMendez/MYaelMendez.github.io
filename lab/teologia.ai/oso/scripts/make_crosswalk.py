import json
# code(USFM), osis, unbound, es name (1909 style), testament
P = [("GEN","Gen","01O","Génesis"),("EXO","Exod","02O","Éxodo"),("LEV","Lev","03O","Levítico"),("NUM","Num","04O","Números"),
("DEU","Deut","05O","Deuteronomio"),("JOS","Josh","06O","Josué"),("JDG","Judg","07O","Jueces"),("RUT","Ruth","08O","Rut"),
("1SA","1Sam","09O","1 Samuel"),("2SA","2Sam","10O","2 Samuel"),("1KI","1Kgs","11O","1 Reyes"),("2KI","2Kgs","12O","2 Reyes"),
("1CH","1Chr","13O","1 Crónicas"),("2CH","2Chr","14O","2 Crónicas"),("EZR","Ezra","15O","Esdras"),("NEH","Neh","16O","Nehemías"),
("EST","Esth","17O","Ester"),("JOB","Job","18O","Job"),("PSA","Ps","19O","Salmos"),("PRO","Prov","20O","Proverbios"),
("ECC","Eccl","21O","Eclesiastés"),("SNG","Song","22O","Cantares"),("ISA","Isa","23O","Isaías"),("JER","Jer","24O","Jeremías"),
("LAM","Lam","25O","Lamentaciones"),("EZK","Ezek","26O","Ezequiel"),("DAN","Dan","27O","Daniel"),("HOS","Hos","28O","Oseas"),
("JOL","Joel","29O","Joel"),("AMO","Amos","30O","Amós"),("OBA","Obad","31O","Abdías"),("JON","Jonah","32O","Jonás"),
("MIC","Mic","33O","Miqueas"),("NAM","Nah","34O","Nahum"),("HAB","Hab","35O","Habacuc"),("ZEP","Zeph","36O","Sofonías"),
("HAG","Hag","37O","Hageo"),("ZEC","Zech","38O","Zacarías"),("MAL","Mal","39O","Malaquías"),
("MAT","Matt","40N","San Mateo"),("MRK","Mark","41N","San Marcos"),("LUK","Luke","42N","San Lucas"),("JHN","John","43N","San Juan"),
("ACT","Acts","44N","Hechos"),("ROM","Rom","45N","Romanos"),("1CO","1Cor","46N","1 Corintios"),("2CO","2Cor","47N","2 Corintios"),
("GAL","Gal","48N","Gálatas"),("EPH","Eph","49N","Efesios"),("PHP","Phil","50N","Filipenses"),("COL","Col","51N","Colosenses"),
("1TH","1Thess","52N","1 Tesalonicenses"),("2TH","2Thess","53N","2 Tesalonicenses"),("1TI","1Tim","54N","1 Timoteo"),
("2TI","2Tim","55N","2 Timoteo"),("TIT","Titus","56N","Tito"),("PHM","Phlm","57N","Filemón"),("HEB","Heb","58N","Hebreos"),
("JAS","Jas","59N","Santiago"),("1PE","1Pet","60N","1 Pedro"),("2PE","2Pet","61N","2 Pedro"),("1JN","1John","62N","1 Juan"),
("2JN","2John","63N","2 Juan"),("3JN","3John","64N","3 Juan"),("JUD","Jude","65N","Judas"),("REV","Rev","66N","Apocalipsis")]
D = {  # deuterocanonicals present in 1569 (Vulgate-style placement inside the OT)
"MAN":("PrMan","83A","Oración de Manasés"),"1ES":("1Esd","81A","3 Esdras (Tercero libro de Esdras)"),
"2ES":("2Esd","82A","4 Esdras (Quarto libro de Esdras)"),"TOB":("Tob","67A","Tobías"),"JDT":("Jdt","68A","Judith"),
"ESG":("AddEsth","69A","Adiciones a Ester (Ester griego)"),"WIS":("Wis","70A","Sabiduría"),"SIR":("Sir","71A","Eclesiástico"),
"BAR":("Bar","72A","Baruc"),"LJE":("EpJer","73A","Epístola de Jeremías (Baruc 6 en orden Vulgata)"),
"S3Y":("PrAzar","74A","Oración de Azarías / Cántico de los tres (Dan 3:24-90 Vulgata)"),
"SUS":("Sus","75A","Susana (Dan 13 Vulgata)"),"BEL":("Bel","76A","Bel y el Dragón (Dan 14 Vulgata)"),
"1MA":("1Macc","77A","1 Macabeos"),"2MA":("2Macc","78A","2 Macabeos")}
order1569 = ["GEN","EXO","LEV","NUM","DEU","JOS","JDG","RUT","1SA","2SA","1KI","2KI","1CH","2CH","MAN","EZR","NEH","1ES","2ES",
 "TOB","JDT","EST","ESG","JOB","PSA","PRO","ECC","SNG","WIS","SIR","ISA","JER","LAM","BAR","LJE","EZK","DAN","S3Y","SUS","BEL",
 "HOS","JOL","AMO","OBA","JON","MIC","NAM","HAB","ZEP","HAG","ZEC","MAL","1MA","2MA"] + [p[0] for p in P[39:]]
books=[]
for i,(c,o,u,n) in enumerate(P):
    books.append({"code":c,"osis":o,"unbound":u,"name_es":n,"testament":"OT" if i<39 else "NT","canon":"protocanonical",
      "in_1569":True,"in_1602":True,"in_1909":True,"order_1909":i+1,"order_1569":order1569.index(c)+1})
for c,(o,u,n) in D.items():
    books.append({"code":c,"osis":o,"unbound":u,"name_es":n,"testament":"OT","canon":"deuterocanonical",
      "in_1569":True,"in_1602":True,"in_1909":False,"order_1909":None,"order_1569":order1569.index(c)+1,
      "placement_1569":"intercalado en el AT (orden Vulgata)","placement_1602":"agrupados entre AT y NT (Valera los apartó como 'apócrifos')"})
books.sort(key=lambda b:b["order_1569"])
cw={"schema":"ae.align.crosswalk/0.1","date":"2026-10-16",
 "id_format":"{edition}:{CODE}.{chapter}.{verse}","code_system":"USFM 3-letter book codes (Paratext); osis = OSIS book name",
 "editions":{"oso1569":{"books":len(order1569),"status":"L2 por construir"},"cantaro1602":{"books":len(order1569),"status":"sin texto PD verificado (ver align/README.md)"},
   "rv1909":{"books":66,"status":"src/rv1909/rv1909.jsonl"},"rvr1960":{"books":66,"status":"solo referencia; nunca se almacena texto"}},
 "notes":["order_1569 confirmado parcialmente con el OCR de archive.org (src/djvu.txt): Manasés tras 2 Crónicas; 3 y 4 Esdras tras Nehemías; Tobías, Judith, Ester; Sabiduría y Eclesiástico tras Cantares; Susana al final de Daniel; Macabeos tras Malaquías. BAR/LJE y S3Y/BEL: verificar fuente.",
  "En 1569 Ester griego, Azarías, Susana, Bel y Epístola de Jeremías pueden venir como capítulos dentro de EST/DAN/BAR (numeración Vulgata). La transcripción L2 debe registrar la numeración tal como aparece y mapearla aquí con verse_map."],
 "books":books,
 "verse_map":[]}
json.dump(cw,open("align/crosswalk.json","w"),ensure_ascii=False,indent=1)
print(len(books))
