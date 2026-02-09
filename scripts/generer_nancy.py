#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère et insère Nancy dans app.js."""
import re

VILLE_ID = "nancy"
VILLE_NOM = "Nancy"
VILLE_CP = "54000"
ELECTION_ID = "nancy-2026"

CANDIDATS = [
    {"id": "klein", "nom": "Mathieu Klein", "liste": "Nancy Grandit (PS/EELV/PCF/Place publique/PRG)", "programmeUrl": "https://mathieuklein.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "henart", "nom": "Laurent H\u00e9nart", "liste": "Nancy avec vous ! (LR/Horizons/Renaissance)", "programmeUrl": "https://www.laurenthenart2026.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "farghaly", "nom": "Sarah Farghaly", "liste": "Nancy Insoumise (LFI)", "programmeUrl": "https://nancy-insoumise.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "lacresse", "nom": "Emmanuel Lacresse", "liste": "Nancy en avant (SE)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "nimsgern", "nom": "Christiane Nimsgern", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
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
SRC_KLEIN_FB = ("France Bleu Lorraine, janvier 2026", "https://www.francebleu.fr/emissions/l-invite-de-la-redaction-ici-lorraine-meurthe-et-moselle-et-vosges/municipales-a-nancy-le-maire-sortant-et-candidat-mathieu-klein-veut-lutter-contre-les-logements-vacants-9873507")
SRC_KLEIN_ICN = ("Ici C Nancy, janvier 2026", "https://www.ici-c-nancy.fr/nancy/17784-municipales-2026-a-nancy-mathieu-klein-presente-sa-liste-nancy-grandit.html")
SRC_KLEIN_F3 = ("France 3 Grand Est, janvier 2026", "https://france3-regions.franceinfo.fr/grand-est/meurthe-et-moselle/nancy/municipales-2026-mathieu-klein-brigue-un-second-mandat-a-nancy-3283448.html")
SRC_HENART_FB = ("France Bleu Lorraine, janvier 2026", "https://www.francebleu.fr/infos/politique/municipales-a-nancy-laurent-henart-candidat-avec-un-choc-de-securite-et-le-retour-de-la-douceur-de-vivre-9914215")
SRC_HENART_FB2 = ("France Bleu Lorraine, janvier 2026", "https://www.francebleu.fr/emissions/l-invite-de-la-redaction-ici-lorraine-meurthe-et-moselle-et-vosges/des-chantiers-mis-en-pause-et-500-cameras-de-video-surveillance-laurent-henart-candidat-a-la-mairie-de-nancy-1618947")
SRC_FARGHALY_FB = ("France Bleu Lorraine, d\u00e9cembre 2025", "https://www.francebleu.fr/infos/politique/municipales-lfi-devoile-sa-tete-de-liste-a-nancy-1297462")

PROPS = {
    # === SECURITE ===
    ("securite", "police-municipale", "klein"): (
        "Augmentation de 50 % des effectifs d\u00e9di\u00e9s \u00e0 la s\u00e9curit\u00e9 en un mandat, seul poste de hausse des RH",
        *SRC_KLEIN_FB
    ),
    ("securite", "police-municipale", "henart"): (
        "Police municipale de proximit\u00e9 dans tous les quartiers : \u00eelotage, patrouilles \u00e0 pied, brigade canine et effectifs renforc\u00e9s",
        *SRC_HENART_FB
    ),
    ("securite", "videoprotection", "henart"): (
        "D\u00e9ploiement de 500 cam\u00e9ras de vid\u00e9osurveillance, vid\u00e9o-verbalisation et cam\u00e9ras mobiles",
        *SRC_HENART_FB2
    ),

    # === TRANSPORTS ===
    ("transports", "tarifs-gratuite", "klein"): (
        "Gratuit\u00e9 des transports pour les moins de 18 ans, \u00e9tendue aux plus de 65 ans d\u00e8s ao\u00fbt 2026",
        *SRC_KLEIN_FB
    ),
    ("transports", "transports-en-commun", "klein"): (
        "Nouveau r\u00e9seau de transport : ligne 1 en trolleybus 100 % \u00e9lectrique, lignes 2 \u00e0 5 en Bus \u00e0 Haut Niveau de Service",
        *SRC_KLEIN_F3
    ),
    ("transports", "velo-mobilites-douces", "klein"): (
        "200 km de pistes cyclables s\u00e9curis\u00e9es et plan v\u00e9lo express",
        *SRC_KLEIN_F3
    ),
    ("transports", "pietons-circulation", "klein"): (
        "Plus d'espace pour les pi\u00e9tons, ville plus apais\u00e9e avec meilleure combinaison des modes de d\u00e9placement",
        *SRC_KLEIN_FB
    ),

    # === LOGEMENT ===
    ("logement", "logements-vacants", "klein"): (
        "Cr\u00e9ation d'une brigade sp\u00e9cialis\u00e9e contre les 9 000 logements vacants : aller vers les propri\u00e9taires pour acc\u00e9l\u00e9rer les d\u00e9marches",
        *SRC_KLEIN_FB
    ),
    ("logement", "logements-vacants", "henart"): (
        "Pause sur les grands chantiers pour repenser l'urbanisme et le logement",
        *SRC_HENART_FB2
    ),

    # === EDUCATION ===
    ("education", "ecoles-renovation", "klein"): (
        "17 cours d'\u00e9cole v\u00e9g\u00e9talis\u00e9es et plantations de 300 arbres le long de la ligne 1",
        *SRC_KLEIN_F3
    ),

    # === ENVIRONNEMENT ===
    ("environnement", "espaces-verts", "klein"): (
        "V\u00e9g\u00e9talisation de la ville : arbres le long des lignes de transport et cours d'\u00e9cole vertes",
        *SRC_KLEIN_F3
    ),
    ("environnement", "climat-adaptation", "farghaly"): (
        "Plus d'ambition en \u00e9cologie et justice sociale pour Nancy",
        *SRC_FARGHALY_FB
    ),

    # === SANTE ===
    ("sante", "centres-sante", "klein"): (
        "D\u00e9veloppement de maisons de sant\u00e9 pluridisciplinaires",
        *SRC_KLEIN_FB
    ),

    # === DEMOCRATIE ===
    ("democratie", "transparence", "farghaly"): (
        "Plus de d\u00e9mocratie locale et de transparence dans la gestion municipale",
        *SRC_FARGHALY_FB
    ),

    # === ECONOMIE ===
    ("economie", "commerce-local", "klein"): (
        "Retour du commerce en centre-ville, revitalisation commerciale",
        *SRC_KLEIN_FB
    ),

    # === SOLIDARITE ===
    ("solidarite", "egalite-discriminations", "klein"): (
        "Ouverture de la Maison des femmes en novembre, lutte contre les violences et les discriminations",
        *SRC_KLEIN_FB
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
