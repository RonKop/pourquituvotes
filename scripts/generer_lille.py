#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère et insère Lille dans app.js."""
import re

VILLE_ID = "lille"
VILLE_NOM = "Lille"
VILLE_CP = "59000"
ELECTION_ID = "lille-2026"

CANDIDATS = [
    {"id": "deslandes", "nom": "Arnaud Deslandes", "liste": "PS", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "baly", "nom": "St\u00e9phane Baly", "liste": "Lille demain (EELV)", "programmeUrl": "https://lilledemain.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "spillebout", "nom": "Violette Spillebout", "liste": "Renaissance", "programmeUrl": "https://vspillebout.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "addouche", "nom": "Lahouaria Addouche", "liste": "LFI", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "delemer", "nom": "Louis Delemer", "liste": "LR", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "valet", "nom": "Matthieu Valet", "liste": "RN", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "madelain", "nom": "Pierre Madelain", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "metschies", "nom": "David Metschies", "liste": "Lille Prosp\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "roussel", "nom": "Baptiste Roussel", "liste": "Au-del\u00e0 des partis", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
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

SRC_DESLANDES_F3 = ("France 3 Hauts-de-France, f\u00e9vrier 2026", "https://france3-regions.franceinfo.fr/")
SRC_DESLANDES_FI = ("France Info, f\u00e9vrier 2026", "https://www.franceinfo.fr/")
SRC_BALY_F3 = ("France 3 Hauts-de-France, f\u00e9vrier 2026", "https://france3-regions.franceinfo.fr/")
SRC_BALY_VERT = ("Vert, f\u00e9vrier 2026", "https://vert.eco/")
SRC_SPILLEBOUT_F3 = ("France 3 Hauts-de-France, f\u00e9vrier 2026", "https://france3-regions.franceinfo.fr/")
SRC_ADDOUCHE_FB = ("France Bleu Nord, janvier 2026", "https://www.francebleu.fr/")
SRC_ADDOUCHE_LI = ("L'Insoumission, janvier 2026", "https://linsoumission.fr/")
SRC_DELEMER_FB = ("France Bleu Nord, f\u00e9vrier 2026", "https://www.francebleu.fr/")
SRC_VALET_FB = ("France Bleu Nord, f\u00e9vrier 2026", "https://www.francebleu.fr/")

PROPS = {
    # === SECURITE ===
    ("securite", "police-municipale", "deslandes"): (
        "Porter \u00e0 230 policiers municipaux (1 pour 1 000 habitants) pour Lille, Lomme et Hellemmes",
        *SRC_DESLANDES_F3
    ),
    ("securite", "police-municipale", "spillebout"): (
        "100 policiers municipaux suppl\u00e9mentaires",
        *SRC_SPILLEBOUT_F3
    ),
    ("securite", "police-municipale", "valet"): (
        "Armement de la police municipale et priorit\u00e9 absolue \u00e0 la s\u00e9curit\u00e9",
        *SRC_VALET_FB
    ),
    ("securite", "videoprotection", "spillebout"): (
        "D\u00e9ploiement de 2 000 cam\u00e9ras de vid\u00e9osurveillance sur le territoire",
        *SRC_SPILLEBOUT_F3
    ),
    ("securite", "prevention-mediation", "baly"): (
        "Cr\u00e9ation de postes de pr\u00e9vention dans tous les quartiers de la ville",
        *SRC_BALY_F3
    ),

    # === LOGEMENT ===
    ("logement", "logements-vacants", "deslandes"): (
        "Requalifier 2 000 logements vacants sur les 7 000 recens\u00e9s",
        *SRC_DESLANDES_FI
    ),
    ("logement", "logements-vacants", "baly"): (
        "Remettre 3 000 logements vacants sur le march\u00e9 locatif",
        *SRC_BALY_VERT
    ),
    ("logement", "logements-vacants", "spillebout"): (
        "Remettre 8 000 logements vacants sur le march\u00e9",
        *SRC_SPILLEBOUT_F3
    ),

    # === URBANISME ===
    ("urbanisme", "amenagement-urbain", "valet"): (
        "Couverture du p\u00e9riph\u00e9rique pour cr\u00e9er de nouveaux espaces urbains",
        *SRC_VALET_FB
    ),

    # === SOLIDARITE ===
    ("solidarite", "aide-sociale", "addouche"): (
        "Plan d'urgence contre la pauvret\u00e9 : 50 000 personnes vivent sous le seuil \u00e0 Lille (27% de la population), priorit\u00e9 aux quartiers populaires",
        *SRC_ADDOUCHE_LI
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
