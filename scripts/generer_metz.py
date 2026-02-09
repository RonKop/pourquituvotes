#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Metz dans app.js."""
import re

VILLE_ID = "metz"
VILLE_NOM = "Metz"
VILLE_CP = "57000"
ELECTION_ID = "metz-2026"

CANDIDATS = [
    {"id": "grosdidier", "nom": "Fran\u00e7ois Grosdidier", "liste": "J'aime Metz (DVD)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "leduc", "nom": "Charlotte Leduc", "liste": "Metz en commun (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "roques", "nom": "J\u00e9r\u00e9my Roques", "liste": "Maintenant pour Metz (EELV/PCF)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "mertz", "nom": "Bertrand Mertz", "liste": "PS / Place publique", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "mendes", "nom": "Ludovic Mendes", "liste": "Metz Ensemble (Renaissance)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "anstett", "nom": "\u00c9tienne Anstett", "liste": "RN/UDR", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "rinaldi", "nom": "Mario Rinaldi", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "diaferia", "nom": "Ga\u00ebl Diaferia", "liste": "NPA-R\u00e9volutionnaires", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
]

CAND_IDS = [c["id"] for c in CANDIDATS]

CATEGORIES = [
    ("securite", "S\u00e9curit\u00e9 & Pr\u00e9vention", [("police-municipale", "Police municipale"), ("videoprotection", "Vid\u00e9oprotection"), ("prevention-mediation", "Pr\u00e9vention & M\u00e9diation"), ("violences-femmes", "Violences faites aux femmes")]),
    ("transports", "Transports & Mobilit\u00e9", [("transports-en-commun", "Transports en commun"), ("velo-mobilites-douces", "V\u00e9lo & Mobilit\u00e9s douces"), ("pietons-circulation", "Pi\u00e9tons & Circulation"), ("stationnement", "Stationnement"), ("tarifs-gratuite", "Tarifs & Gratuit\u00e9")]),
    ("logement", "Logement", [("logement-social", "Logement social"), ("logements-vacants", "Logements vacants"), ("encadrement-loyers", "Encadrement des loyers"), ("acces-logement", "Acc\u00e8s au logement")]),
    ("education", "\u00c9ducation & Jeunesse", [("petite-enfance", "Petite enfance"), ("ecoles-renovation", "\u00c9coles & R\u00e9novation"), ("cantines-fournitures", "Cantines & Fournitures"), ("periscolaire-loisirs", "P\u00e9riscolaire & Loisirs"), ("jeunesse", "Jeunesse")]),
    ("environnement", "Environnement & Transition \u00e9cologique", [("espaces-verts", "Espaces verts & Biodiversit\u00e9"), ("proprete-dechets", "Propret\u00e9 & D\u00e9chets"), ("climat-adaptation", "Climat & Adaptation"), ("renovation-energetique", "R\u00e9novation \u00e9nerg\u00e9tique"), ("alimentation-durable", "Alimentation durable")]),
    ("sante", "Sant\u00e9 & Acc\u00e8s aux soins", [("centres-sante", "Centres de sant\u00e9"), ("prevention-sante", "Pr\u00e9vention sant\u00e9"), ("seniors", "Seniors")]),
    ("democratie", "D\u00e9mocratie & Vie citoyenne", [("budget-participatif", "Budget participatif"), ("transparence", "Transparence"), ("vie-associative", "Vie associative"), ("services-publics", "Services publics")]),
    ("economie", "\u00c9conomie & Emploi", [("commerce-local", "Commerce local"), ("emploi-insertion", "Emploi & Insertion"), ("attractivite", "Attractivit\u00e9")]),
    ("culture", "Culture & Patrimoine", [("equipements-culturels", "\u00c9quipements culturels"), ("evenements-creation", "\u00c9v\u00e9nements & Cr\u00e9ation")]),
    ("sport", "Sport & Loisirs", [("equipements-sportifs", "\u00c9quipements sportifs"), ("sport-pour-tous", "Sport pour tous")]),
    ("urbanisme", "Urbanisme & Cadre de vie", [("amenagement-urbain", "Am\u00e9nagement urbain"), ("accessibilite", "Accessibilit\u00e9"), ("quartiers-prioritaires", "Quartiers prioritaires")]),
    ("solidarite", "Solidarit\u00e9 & \u00c9galit\u00e9", [("aide-sociale", "Aide sociale"), ("egalite-discriminations", "\u00c9galit\u00e9 & Discriminations"), ("pouvoir-achat", "Pouvoir d'achat")]),
]

# === Sources ===
SRC_GR_CM = ("Le Courrier Messin, f\u00e9vrier 2026", "https://courriermessin.fr/francois-grosdidier-metz-2026/")
SRC_GR_MO = ("Moselle.tv, f\u00e9vrier 2026", "https://moselle.tv/securite-transports-quartiers-grosdidier-dessine-le-metz-de-demain/")
SRC_GR_FR = ("France 3 Grand Est, f\u00e9vrier 2026", "https://france3-regions.franceinfo.fr/grand-est/moselle/metz/")
SRC_LED_TM = ("Tout-Metz, janvier 2026", "https://tout-metz.com/municipales-2026-metz-charlotte-leduc-lfi-veut-faire-voter-messins-avant-heure-2026-842695")
SRC_LED_INS = ("L'insoumission, janvier 2026", "https://linsoumission.fr/2026/01/17/municipales-metz-bompard-leduc/")
SRC_LED_MO = ("Moselle.tv, d\u00e9cembre 2025", "https://moselle.tv/metz-en-commun-charlotte-leduc-veut-agir-sur-le-terrain/")
SRC_ROQ_MO = ("Moselle.tv, septembre 2025", "https://moselle.tv/jeremy-roques-lance-sa-campagne-avec-maintenant-pour-metz/")
SRC_ROQ_TM = ("Tout-Metz, septembre 2025", "https://tout-metz.com/municipales-2026-jeremy-roques-candidat-etiquette-maintenant-metz-845313")
SRC_MER_TM = ("Tout-Metz, d\u00e9cembre 2025", "https://tout-metz.com/municipales-2026-metz-bertrand-mertz-detaille-projets-metropole-2025-846298")
SRC_MER_FB = ("France Bleu Lorraine, d\u00e9cembre 2025", "https://www.francebleu.fr/emissions/l-info-d-ici-ici-lorraine-moselle-et-pays-haut/municipales-2026-avec-la-candidature-de-bertrand-mertz-la-gauche-part-pour-l-instant-divisee-4761222")
SRC_MEN_MO = ("Moselle.tv, octobre 2025", "https://moselle.tv/le-groupe-fabert-devient-metz-ensemble-avec-ludovic-mendes/")
SRC_MEN_FB = ("France Bleu Lorraine, octobre 2025", "https://www.francebleu.fr/infos/politique/ludovic-mendes-se-lance-dans-la-course-aux-municipales-a-metz-4204092")
SRC_ANS_TM = ("Tout-Metz, janvier 2026", "https://tout-metz.com/municipales-2026-metz-etienne-anstett-rn-presente-premieres-mesures-programme-254563")
SRC_ANS_FB = ("France Bleu Lorraine, octobre 2025", "https://www.francebleu.fr/infos/politique/etienne-anstett-candidat-rn-aux-municipales-2026-a-metz-mon-ambition-est-d-arriver-premier-au-premier-tour-4508130")

PROPS = {
    # ===================== GROSDIDIER =====================
    # === SECURITE ===
    ("securite", "police-municipale", "grosdidier"): (
        "Augmentation de 25 % des effectifs de police municipale et cr\u00e9ation de brigades sp\u00e9cialis\u00e9es (canine, cycliste, s\u00e9curit\u00e9 routi\u00e8re) ; cr\u00e9ation d'une police m\u00e9tropolitaine d\u00e9di\u00e9e aux transports et \u00e0 l'environnement",
        *SRC_GR_CM
    ),
    ("securite", "videoprotection", "grosdidier"): (
        "Objectif 1 000 cam\u00e9ras de vid\u00e9osurveillance sur la ville d'ici 2026, r\u00e9flexion sur la reconnaissance faciale encadr\u00e9e par la loi",
        *SRC_GR_CM
    ),
    # === TRANSPORTS ===
    ("transports", "transports-en-commun", "grosdidier"): (
        "Poursuite du d\u00e9veloppement du r\u00e9seau Mettis et des pistes cyclables, notamment le long des berges de la Seille de Magny \u00e0 Ranconval",
        *SRC_GR_CM
    ),
    ("transports", "velo-mobilites-douces", "grosdidier"): (
        "Plan v\u00e9lo 2030 revu \u00e0 la hausse avec de nouveaux itin\u00e9raires cyclables structurants dans la ville",
        *SRC_GR_MO
    ),
    # === URBANISME ===
    ("urbanisme", "amenagement-urbain", "grosdidier"): (
        "Pi\u00e9tonnisation de l'axe Cath\u00e9drale-Porte des Allemands avec cr\u00e9ation d'une nouvelle place des Paraiges",
        *SRC_GR_CM
    ),
    # === SANTE ===
    ("sante", "centres-sante", "grosdidier"): (
        "R\u00e9investir les h\u00f4pitaux pour ramener des activit\u00e9s de soins en centre-ville ; centre de bien-\u00eatre pr\u00e8s de la piscine Lothaire",
        *SRC_GR_CM
    ),
    # === SPORT ===
    ("sport", "equipements-sportifs", "grosdidier"): (
        "Ouverture de l'Espace Gymnique au printemps 2026 et nouveau centre de bien-\u00eatre aquatique",
        *SRC_GR_CM
    ),

    # ===================== LEDUC (LFI) =====================
    # === TRANSPORTS ===
    ("transports", "tarifs-gratuite", "leduc"): (
        "Gratuit\u00e9 progressive des transports en commun sur le mandat, en commen\u00e7ant par les jeunes et les m\u00e9nages modestes",
        *SRC_LED_TM
    ),
    # === EDUCATION ===
    ("education", "cantines-fournitures", "leduc"): (
        "Cantines 100 % bio et locales gratuites pour tous les \u00e9coliers d\u00e8s la rentr\u00e9e 2026",
        *SRC_LED_INS
    ),
    # === LOGEMENT ===
    ("logement", "logements-vacants", "leduc"): (
        "Utiliser le pouvoir de r\u00e9quisition du maire pour les b\u00e2timents vides et mettre \u00e0 disposition les b\u00e2timents publics inutilis\u00e9s, objectif z\u00e9ro sans-abri",
        *SRC_LED_INS
    ),
    ("logement", "logement-social", "leduc"): (
        "Plan d'urgence pour le logement social face aux 8 300 demandes en attente \u00e0 Metz",
        *SRC_LED_INS
    ),
    # === DEMOCRATIE ===
    ("democratie", "budget-participatif", "leduc"): (
        "Instauration d'un RIC municipal (r\u00e9f\u00e9rendum d'initiative citoyenne) et budget participatif avec vote des habitants",
        *SRC_LED_TM
    ),
    # === SOLIDARITE ===
    ("solidarite", "egalite-discriminations", "leduc"): (
        "Faire de Metz une municipalit\u00e9 antiraciste, inclusive et f\u00e9ministe",
        *SRC_LED_MO
    ),

    # ===================== ROQUES (EELV) =====================
    # === TRANSPORTS ===
    ("transports", "tarifs-gratuite", "roques"): (
        "Gratuit\u00e9 progressive des transports en commun \u00e0 partir de 2026",
        *SRC_ROQ_MO
    ),
    # === ENVIRONNEMENT ===
    ("environnement", "espaces-verts", "roques"): (
        "Ouverture de la baignade dans la Moselle en centre-ville d\u00e8s 2027 ; cr\u00e9ation d'une ferme urbaine d'ici 2029",
        *SRC_ROQ_MO
    ),
    # === SANTE ===
    ("sante", "centres-sante", "roques"): (
        "Cr\u00e9ation d'un campus sant\u00e9 \u00e0 Bridoux pour former des m\u00e9decins localement d'ici 2031",
        *SRC_ROQ_MO
    ),
    # === DEMOCRATIE ===
    ("democratie", "vie-associative", "roques"): (
        "Conversion de l'ancienne caserne de Ranconval en site associatif central d'ici 2028 ; ouverture des \u00e9coles aux associations hors temps scolaire d\u00e8s 2030",
        *SRC_ROQ_MO
    ),
    # === ECONOMIE ===
    ("economie", "attractivite", "roques"): (
        "Cr\u00e9ation d'un hub num\u00e9rique \u00e0 la basilique Saint-Vincent avant 2032",
        *SRC_ROQ_MO
    ),

    # ===================== MERTZ (PS) =====================
    # === TRANSPORTS ===
    ("transports", "transports-en-commun", "mertz"): (
        "Extension de la ligne Mettis pour am\u00e9liorer la desserte des quartiers",
        *SRC_MER_TM
    ),
    # === SECURITE ===
    ("securite", "police-municipale", "mertz"): (
        "Coordination renforc\u00e9e entre police municipale et police nationale, actions de s\u00e9curit\u00e9 dans chaque quartier",
        *SRC_MER_FB
    ),
    # === DEMOCRATIE ===
    ("democratie", "transparence", "mertz"): (
        "Gouvernance participative et transparente : association des citoyens \u00e0 chaque \u00e9tape des d\u00e9cisions municipales",
        *SRC_MER_TM
    ),
    # === SOLIDARITE ===
    ("solidarite", "pouvoir-achat", "mertz"): (
        "Z\u00e9ro augmentation d'imp\u00f4ts locaux sur le mandat",
        *SRC_MER_FB
    ),
    # === EDUCATION ===
    ("education", "jeunesse", "mertz"): (
        "Politique ambitieuse pour la jeunesse : faire de la jeunesse la priorit\u00e9 transversale du mandat",
        *SRC_MER_TM
    ),

    # ===================== MENDES (Renaissance) =====================
    # === SECURITE ===
    ("securite", "prevention-mediation", "mendes"): (
        "Pacte s\u00e9curit\u00e9 : renforcement de la pr\u00e9vention et de la m\u00e9diation dans tous les quartiers",
        *SRC_MEN_MO
    ),
    # === ECONOMIE ===
    ("economie", "attractivite", "mendes"): (
        "Redonner \u00e0 Metz une place de premier plan au niveau national et europ\u00e9en, en s'appuyant sur son histoire particuli\u00e8re",
        *SRC_MEN_FB
    ),
    # === ENVIRONNEMENT ===
    ("environnement", "climat-adaptation", "mendes"): (
        "Pacte \u00e9cologique : \u00e9cologie positive et non punitive, int\u00e9gr\u00e9e dans tous les projets de la ville",
        *SRC_MEN_MO
    ),
    # === DEMOCRATIE ===
    ("democratie", "transparence", "mendes"): (
        "Pacte d\u00e9mocratique : liste citoyenne transpartisane, 90 % des co-listiers sans \u00e9tiquette politique",
        *SRC_MEN_MO
    ),

    # ===================== ANSTETT (RN) =====================
    # === SECURITE ===
    ("securite", "police-municipale", "anstett"): (
        "Renforcement massif de la s\u00e9curit\u00e9 et lutte contre l'ins\u00e9curit\u00e9 au-del\u00e0 du centre-ville",
        *SRC_ANS_TM
    ),
    # === ECONOMIE ===
    ("economie", "commerce-local", "anstett"): (
        "Lutte contre la d\u00e9sertification commerciale et relance de l'attractivit\u00e9 des commerces de proximit\u00e9",
        *SRC_ANS_TM
    ),
    # === SOLIDARITE ===
    ("solidarite", "pouvoir-achat", "anstett"): (
        "D\u00e9fense du pouvoir d'achat des m\u00e9nages messins, priorit\u00e9 du programme",
        *SRC_ANS_FB
    ),
    # === ENVIRONNEMENT ===
    ("environnement", "proprete-dechets", "anstett"): (
        "Am\u00e9lioration de la propret\u00e9 dans tous les quartiers de Metz",
        *SRC_ANS_TM
    ),
}


def escape_js(s):
    result = []
    for ch in s:
        cp = ord(ch)
        if cp > 127: result.append(f"\\u{cp:04X}")
        elif ch == '"': result.append('\\"')
        elif ch == '\\': result.append('\\\\')
        elif ch == '\n': result.append('\\n')
        else: result.append(ch)
    return ''.join(result)

def gen_proposition(cat_id, st_id, cand_id, indent=16):
    key = (cat_id, st_id, cand_id); sp = ' ' * indent
    if key not in PROPS: return f"{sp}{cand_id}: null"
    texte, source, source_url = PROPS[key]
    return '\n'.join([f'{sp}{cand_id}: {{', f'{sp}  texte: "{escape_js(texte)}",', f'{sp}  source: "{escape_js(source)}",', f'{sp}  sourceUrl: "{escape_js(source_url)}"', f'{sp}}}'])

def gen_sous_theme(cat_id, st_id, st_nom, indent=12):
    sp = ' ' * indent
    lines = [f'{sp}{{', f'{sp}  id: "{st_id}",', f'{sp}  nom: "{escape_js(st_nom)}",', f'{sp}  propositions: {{']
    lines.append(',\n'.join(gen_proposition(cat_id, st_id, cid) for cid in CAND_IDS))
    lines += [f'{sp}  }}', f'{sp}}}']
    return '\n'.join(lines)

def gen_categorie(cat_id, cat_nom, sous_themes, indent=8):
    sp = ' ' * indent
    lines = [f'{sp}{{', f'{sp}  id: "{cat_id}",', f'{sp}  nom: "{escape_js(cat_nom)}",', f'{sp}  sousThemes: [']
    lines.append(',\n'.join(gen_sous_theme(cat_id, sid, sn) for sid, sn in sous_themes))
    lines += [f'{sp}  ]', f'{sp}}}']
    return '\n'.join(lines)

def gen_candidat(c):
    pdf = "null" if c["programmePdfPath"] is None else f'"{escape_js(c["programmePdfPath"])}"'
    complet = "true" if c["programmeComplet"] else "false"
    return (f'        {{ id: "{c["id"]}", nom: "{escape_js(c["nom"])}", liste: "{escape_js(c["liste"])}", programmeUrl: "{escape_js(c["programmeUrl"])}", programmeComplet: {complet}, programmePdfPath: {pdf} }}')

def gen_election():
    lines = [f'    "{ELECTION_ID}": {{', f'      ville: "{escape_js(VILLE_NOM)}",', '      annee: 2026,', '      type: "\\u00C9lections municipales",', '      dateVote: "2026-03-15T08:00:00",', '      candidats: [']
    lines.append(',\n'.join(gen_candidat(c) for c in CANDIDATS))
    lines.append('      ],'); lines.append('      categories: [')
    lines.append(',\n'.join(gen_categorie(cid, cn, sts) for cid, cn, sts in CATEGORIES))
    lines += ['      ]', '    }']
    return '\n'.join(lines)

def main():
    app_js_path = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\js\app.js"
    with open(app_js_path, 'r', encoding='utf-8') as f: content = f.read()
    if f'id: "{VILLE_ID}"' not in content[:content.find('var ELECTIONS')]:
        villes_end = content.find('  ];\n\n    var ELECTIONS')
        if villes_end == -1: villes_end = content.find('  ];\n\n  var ELECTIONS')
        entry = f'    ,{{\n      id: "{VILLE_ID}",\n      nom: "{escape_js(VILLE_NOM)}",\n      codePostal: "{VILLE_CP}",\n      elections: ["{ELECTION_ID}"]\n    }}'
        content = content[:villes_end] + entry + '\n' + content[villes_end:]
        print(f"Ville {VILLE_ID} ajoutee")
    else: print(f"Ville {VILLE_ID} existe deja")
    if f'    "{ELECTION_ID}": {{' not in content:
        m = re.search(r'\n  \};\n\n+  // === ', content)
        content = content[:m.start()] + ',\n' + gen_election() + content[m.start():]
        print(f"Election {ELECTION_ID} ajoutee")
    else: print(f"Election {ELECTION_ID} existe deja")
    with open(app_js_path, 'w', encoding='utf-8') as f: f.write(content)
    print(f"Total: {len(PROPS)} propositions")
    for cid in CAND_IDS:
        cn = next(c["nom"] for c in CANDIDATS if c["id"] == cid)
        print(f"  {cn}: {sum(1 for k in PROPS if k[2] == cid)}")

if __name__ == "__main__":
    main()
