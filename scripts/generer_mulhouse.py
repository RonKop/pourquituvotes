#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère et insère Mulhouse dans app.js."""
import re

VILLE_ID = "mulhouse"
VILLE_NOM = "Mulhouse"
VILLE_CP = "68100"
ELECTION_ID = "mulhouse-2026"

CANDIDATS = [
    {"id": "lutz", "nom": "Mich\u00e8le Lutz", "liste": "Fiers de Mulhouse ! (LR)", "programmeUrl": "https://www.michelelutz.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "million", "nom": "Lara Million", "liste": "Mulhouse ensemble (Centriste et Territoires)", "programmeUrl": "https://laramillion2026.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "minery", "nom": "Lo\u00efc Minery", "liste": "Mulhouse en Commun (EELV/PS/PCF/G\u00e9n\u00e9ration.s/Place publique)", "programmeUrl": "https://loic-minery2026.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "ritz", "nom": "Christelle Ritz", "liste": "Rassemblement pour Mulhouse (RN)", "programmeUrl": "https://www.rassemblementpourmulhouse.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "taffarelli", "nom": "Emmanuel Taffarelli", "liste": "Restaurer Mulhouse (Reconqu\u00eate !)", "programmeUrl": "https://www.restaurermulhouse.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "gafanesch", "nom": "Eliot Gafanesch", "liste": "LFI", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "sassi", "nom": "Annouar Sassi", "liste": "Nous sommes Mulhouse (DVG)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "sornin", "nom": "C\u00e9cile Sornin", "liste": "Mulhouse au c\u0153ur (DVD)", "programmeUrl": "https://www.mulhouseaucoeur.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "fuchs", "nom": "Bruno Fuchs", "liste": "MoDem", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "marquet", "nom": "Fr\u00e9d\u00e9ric Marquet", "liste": "Mulhouse j'y crois (SE)", "programmeUrl": "https://marquet2026.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "keltoumi", "nom": "Salah Keltoumi", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "djehaf", "nom": "Kadhafi Djehaf", "liste": "Kadhafi pour Mulhouse (SE)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
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
SRC_LUTZ_FB = ("France Bleu Alsace, janvier 2026", "https://www.francebleu.fr/infos/politique/municipales-2026-quels-sont-les-candidats-declares-a-mulhouse-6254290")
SRC_LUTZ_F3 = ("France 3 Grand Est, d\u00e9cembre 2025", "https://france3-regions.franceinfo.fr/grand-est/haut-rhin/mulhouse/municipales-2026-a-mulhouse-michele-lutz-annonce-sa-candidature-pour-un-nouveau-mandat-3258649.html")
SRC_LUTZ_MP = ("M+, 2025", "https://www.mplusinfo.fr/la-securite-premiere-priorite-de-la-ville-8bc42430-64e6-4cad-aa89-c10942ab06f8")
SRC_MINERY_FB = ("France Bleu Alsace, f\u00e9vrier 2026", "https://www.francebleu.fr/infos/politique/municipales-2026-quels-sont-les-candidats-declares-a-mulhouse-6254290")
SRC_RITZ_FB = ("France Bleu Alsace, f\u00e9vrier 2026", "https://www.francebleu.fr/infos/politique/municipales-2026-quels-sont-les-candidats-declares-a-mulhouse-6254290")
SRC_MILLION_FB = ("France Bleu Alsace, janvier 2026", "https://www.francebleu.fr/infos/politique/municipales-2026-quels-sont-les-candidats-declares-a-mulhouse-6254290")
SRC_GAFANESCH_FB = ("France Bleu Alsace, f\u00e9vrier 2026", "https://www.francebleu.fr/infos/politique/municipales-2026-quels-sont-les-candidats-declares-a-mulhouse-6254290")
SRC_TAFFARELLI_FB = ("France Bleu Alsace, f\u00e9vrier 2026", "https://www.francebleu.fr/infos/politique/municipales-2026-quels-sont-les-candidats-declares-a-mulhouse-6254290")
SRC_MARQUET_FB = ("France Bleu Alsace, f\u00e9vrier 2026", "https://www.francebleu.fr/infos/politique/municipales-2026-quels-sont-les-candidats-declares-a-mulhouse-6254290")
SRC_SORNIN_AP = ("L'Alterpresse68, d\u00e9cembre 2025", "https://www.alterpresse68.info/2025/12/15/cecile-sornin-candidate-aux-elections-municipales-de-mulhouse-les-promesses-nengagent-que-ceux-qui-les-ecoutent-est-une-phrase-qui-me-donne-la-nausee/")

PROPS = {
    # === SECURITE ===
    ("securite", "police-municipale", "lutz"): (
        "Police municipale de 75 agents op\u00e9rationnelle 24h/24, r\u00e9armement progressif avec pistolets semi-automatiques 9 mm",
        *SRC_LUTZ_MP
    ),
    ("securite", "videoprotection", "lutz"): (
        "330 cam\u00e9ras de vid\u00e9oprotection op\u00e9rationnelles, 39 nouvelles d\u00e9ploy\u00e9es en 2025",
        *SRC_LUTZ_MP
    ),
    ("securite", "police-municipale", "ritz"): (
        "Doubler les effectifs de police municipale et cr\u00e9er un centre d'\u00e9loignement pour mineurs d\u00e9linquants r\u00e9cidivistes",
        *SRC_RITZ_FB
    ),
    ("securite", "prevention-mediation", "taffarelli"): (
        "Priorit\u00e9 \u00e0 la s\u00e9curit\u00e9, aux libert\u00e9s et \u00e0 l'identit\u00e9",
        *SRC_TAFFARELLI_FB
    ),

    # === TRANSPORTS ===
    ("transports", "tarifs-gratuite", "gafanesch"): (
        "Gratuit\u00e9 des transports en commun \u00e0 Mulhouse",
        *SRC_GAFANESCH_FB
    ),
    ("transports", "velo-mobilites-douces", "lutz"): (
        "Cr\u00e9ation de 15 km de pistes cyclables et 10 itin\u00e9raires continus pour le v\u00e9lo",
        *SRC_LUTZ_F3
    ),
    ("transports", "velo-mobilites-douces", "ritz"): (
        "D\u00e9veloppement des pistes cyclables et cr\u00e9ation de parkings relais aux entr\u00e9es de Mulhouse",
        *SRC_RITZ_FB
    ),
    ("transports", "stationnement", "ritz"): (
        "Pr\u00e9servation des places de stationnement en centre-ville",
        *SRC_RITZ_FB
    ),

    # === LOGEMENT ===

    # === EDUCATION ===
    ("education", "jeunesse", "million"): (
        "Priorit\u00e9 \u00e0 l'\u00e9ducation et \u00e0 la jeunesse",
        *SRC_MILLION_FB
    ),

    # === ENVIRONNEMENT ===
    ("environnement", "espaces-verts", "lutz"): (
        "Projet Mulhouse Diagonales : vaste d\u00e9marche de renaturation urbaine et v\u00e9g\u00e9talisation du centre-ville (9 000 m\u00b2 pi\u00e9tonnis\u00e9s)",
        *SRC_LUTZ_F3
    ),
    ("environnement", "climat-adaptation", "lutz"): (
        "D\u00e9fis climatique, social et patrimonial : reconversion des friches industrielles (DMC) en \u00ab laboratoires de ville durable \u00bb",
        *SRC_LUTZ_F3
    ),
    ("environnement", "climat-adaptation", "million"): (
        "Transition climatique et int\u00e9gration de l'intelligence artificielle au service de la ville",
        *SRC_MILLION_FB
    ),

    # === SANTE ===
    ("sante", "centres-sante", "marquet"): (
        "Urgence sant\u00e9 : am\u00e9liorer l'acc\u00e8s aux soins \u00e0 Mulhouse",
        *SRC_MARQUET_FB
    ),
    ("sante", "centres-sante", "million"): (
        "Priorit\u00e9 sant\u00e9 et bien vieillir",
        *SRC_MILLION_FB
    ),
    ("sante", "seniors", "million"): (
        "Politique d\u00e9di\u00e9e au bien vieillir \u00e0 Mulhouse",
        *SRC_MILLION_FB
    ),

    # === DEMOCRATIE ===
    ("democratie", "services-publics", "million"): (
        "Mairie mobile, \u00e9lus r\u00e9f\u00e9rents de quartier avec permanences r\u00e9guli\u00e8res, mairies annexes de quartier",
        *SRC_MILLION_FB
    ),
    ("democratie", "transparence", "sornin"): (
        "L'humain d'abord, la ville autrement : transparence et gouvernance ouverte apr\u00e8s avoir quitt\u00e9 la majorit\u00e9",
        *SRC_SORNIN_AP
    ),

    # === ECONOMIE ===
    ("economie", "attractivite", "million"): (
        "Faire de Mulhouse une capitale trinationale",
        *SRC_MILLION_FB
    ),

    # === URBANISME ===
    ("urbanisme", "amenagement-urbain", "lutz"): (
        "Extension des zones pi\u00e9tonnes (9 000 m\u00b2), plantations d'arbres et cr\u00e9ation d'espaces verts en centre-ville",
        *SRC_LUTZ_F3
    ),

    # === SOLIDARITE ===
    ("solidarite", "aide-sociale", "minery"): (
        "Lutte contre la pauvret\u00e9 (36 % de taux de pauvret\u00e9), priorit\u00e9 absolue du mandat",
        *SRC_MINERY_FB
    ),
    ("solidarite", "aide-sociale", "sassi"): (
        "Candidat des classes populaires : fiert\u00e9, dignit\u00e9 et justice pour les quartiers",
        *SRC_MINERY_FB
    ),

    # === PROPRETE ===
    ("environnement", "proprete-dechets", "marquet"): (
        "Urgence propret\u00e9 : nettoyage et entretien renforc\u00e9s de la ville",
        *SRC_MARQUET_FB
    ),
    ("environnement", "proprete-dechets", "million"): (
        "Collecte des d\u00e9chets \u00e0 domicile dans tout Mulhouse et cr\u00e9ation d'une brigade anti-incivilit\u00e9s",
        *SRC_MILLION_FB
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
