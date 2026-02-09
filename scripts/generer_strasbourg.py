#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère et insère Strasbourg dans app.js."""
import re

VILLE_ID = "strasbourg"
VILLE_NOM = "Strasbourg"
VILLE_CP = "67000"
ELECTION_ID = "strasbourg-2026"

CANDIDATS = [
    {"id": "barseghian", "nom": "Jeanne Barseghian", "liste": "Strasbourg juste et vivante (EELV)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "trautmann", "nom": "Catherine Trautmann", "liste": "PS", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "vetter", "nom": "Jean-Philippe Vetter", "liste": "Aimer Strasbourg (LR)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "joron", "nom": "Virginie Joron", "liste": "Sauver Strasbourg (RN)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "kobryn", "nom": "Florian Kobryn", "liste": "Strasbourg fi\u00e8re et solidaire (LFI)", "programmeUrl": "http://kobryn2026.eu/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "jakubowicz", "nom": "Pierre Jakubowicz", "liste": "Strasbourg on y croit ! (Horizons)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "ibiem", "nom": "Linda Ibiem", "liste": "Strasbourg vivant (PS/Convergence)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "vinci", "nom": "Thibaut Vinci", "liste": "PRG", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "becherirat", "nom": "Isma\u00efl Becherirat", "liste": "Unis pour Strasbourg", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "sylla", "nom": "Mohamed Sylla", "liste": "Utiles Bas-Rhin", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "muhammad", "nom": "Fahad Raja Muhammad", "liste": "Strasbourg sans fronti\u00e8res (MPI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "feve", "nom": "Louise F\u00e8ve", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "yoldas", "nom": "Cem Yoldas", "liste": "Strasbourg c'est nous (NPA)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "soubise", "nom": "Cl\u00e9ment Soubise", "liste": "NPA-R\u00e9volutionnaires", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
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

SRC_BARSEGHIAN_PK = ("Pokaa, janvier 2026", "https://pokaa.fr/")
SRC_BARSEGHIAN_R89 = ("Rue89 Strasbourg, janvier 2026", "https://www.rue89strasbourg.com/")
SRC_TRAUTMANN_PK = ("Pokaa, d\u00e9cembre 2025", "https://pokaa.fr/")
SRC_TRAUTMANN_F3 = ("France 3 Grand Est, octobre 2025", "https://france3-regions.franceinfo.fr/")
SRC_JORON_PK = ("Pokaa, janvier 2026", "https://pokaa.fr/")
SRC_KOBRYN_R89 = ("Rue89 Strasbourg, janvier 2026", "https://www.rue89strasbourg.com/")
SRC_KOBRYN_FB = ("France Bleu Alsace, janvier 2026", "https://www.francebleu.fr/")

PROPS = {
    # === SECURITE ===
    ("securite", "police-municipale", "trautmann"): (
        "Renforcement de la pr\u00e9sence de la police municipale et r\u00e9tablissement de l'\u00e9clairage public dans toutes les rues \u00e0 toute heure",
        *SRC_TRAUTMANN_PK
    ),
    ("securite", "police-municipale", "joron"): (
        "R\u00e9tablissement d'un arr\u00eat\u00e9 anti-mendicit\u00e9 et renforcement de la s\u00e9curit\u00e9 dans les quartiers sensibles",
        *SRC_JORON_PK
    ),
    ("securite", "videoprotection", "trautmann"): (
        "Installation de pi\u00e8ges photo (photo traps) dans les zones de d\u00e9p\u00f4ts sauvages et d'incivilit\u00e9s",
        *SRC_TRAUTMANN_PK
    ),

    # === TRANSPORTS ===
    ("transports", "transports-en-commun", "barseghian"): (
        "Poursuite de l'extension du tramway vers le nord de Strasbourg et transformation de la gare",
        *SRC_BARSEGHIAN_R89
    ),
    ("transports", "stationnement", "barseghian"): (
        "Tarification solidaire du stationnement r\u00e9sident : de 5\u20ac \u00e0 40\u20ac par mois selon les revenus",
        *SRC_BARSEGHIAN_PK
    ),
    ("transports", "tarifs-gratuite", "kobryn"): (
        "Gratuit\u00e9 des transports en commun pour les moins de 25 ans",
        *SRC_KOBRYN_FB
    ),

    # === LOGEMENT ===
    ("logement", "encadrement-loyers", "barseghian"): (
        "Encadrement des loyers pour garantir des logements et commerces abordables et pr\u00e9server leur diversit\u00e9",
        *SRC_BARSEGHIAN_PK
    ),
    ("logement", "encadrement-loyers", "kobryn"): (
        "Mise en place de l'encadrement des loyers \u00e0 Strasbourg",
        *SRC_KOBRYN_R89
    ),

    # === EDUCATION ===
    ("education", "cantines-fournitures", "barseghian"): (
        "Cantines de quartier accessibles \u00e0 tous : manger bien et pas cher. Objectif 75% de bio dans les cantines scolaires (contre 53% actuellement)",
        *SRC_BARSEGHIAN_PK
    ),

    # === ENVIRONNEMENT ===
    ("environnement", "espaces-verts", "barseghian"): (
        "Acc\u00e9l\u00e9rer la v\u00e9g\u00e9talisation : nouveaux parcs et rues plus vertes dans tous les quartiers",
        *SRC_BARSEGHIAN_PK
    ),
    ("environnement", "alimentation-durable", "barseghian"): (
        "D\u00e9velopper l'alimentation saine et locale pour tous les Strasbourgeois via des cantines de quartier",
        *SRC_BARSEGHIAN_PK
    ),

    # === SPORT ===
    ("sport", "sport-pour-tous", "barseghian"): (
        "Sport encadr\u00e9 en acc\u00e8s libre dans les parcs avec des coachs sportifs municipaux",
        *SRC_BARSEGHIAN_PK
    ),

    # === DEMOCRATIE ===
    ("democratie", "transparence", "joron"): (
        "Audit financier complet de la gestion municipale",
        *SRC_JORON_PK
    ),

    # === SOLIDARITE ===
    ("solidarite", "aide-sociale", "barseghian"): (
        "Garantir le droit aux vacances pour toutes et tous : s\u00e9jours accessibles pour les familles modestes",
        *SRC_BARSEGHIAN_PK
    ),
    ("solidarite", "pouvoir-achat", "trautmann"): (
        "Lutte contre la paup\u00e9risation : modifier les politiques tarifaires et le co\u00fbt de la mobilit\u00e9 sans alourdir la fiscalit\u00e9",
        *SRC_TRAUTMANN_F3
    ),
    ("solidarite", "pouvoir-achat", "kobryn"): (
        "Gratuit\u00e9 de l'eau pour les 30 premiers m\u00e8tres cubes de chaque foyer",
        *SRC_KOBRYN_R89
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
        content = content[:m.start()] + ',\n' + gen_election() + content[m.start()]
        print(f"Election {ELECTION_ID} ajoutee")
    else: print(f"Election {ELECTION_ID} existe deja")
    with open(app_js_path, 'w', encoding='utf-8') as f: f.write(content)
    print(f"Total: {len(PROPS)} propositions")
    for cid in CAND_IDS:
        cn = next(c["nom"] for c in CANDIDATS if c["id"] == cid)
        print(f"  {cn}: {sum(1 for k in PROPS if k[2] == cid)}")

if __name__ == "__main__":
    main()
