#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère et insère Caen dans app.js."""
import re

VILLE_ID = "caen"
VILLE_NOM = "Caen"
VILLE_CP = "14000"
ELECTION_ID = "caen-2026"

CANDIDATS = [
    {"id": "olivier", "nom": "Aristide Olivier", "liste": "Caen ensemble (DVD)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "lorphelin", "nom": "Rudy L'Orphelin", "liste": "Caen nous rassemble (EELV/PS/PCF/Place publique)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "guidi", "nom": "Aur\u00e9lien Guidi", "liste": "Faire mieux pour Caen (LFI/G\u00e9n\u00e9ration.s)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "lecoutour", "nom": "Xavier Le Coutour", "liste": "Citoyens \u00e0 Caen (DVG)", "programmeUrl": "https://xavierlecoutour2026.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "casini", "nom": "Antoine Casini", "liste": "Le Caen de l'engagement (PRG/L'Engagement)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "henry", "nom": "Chantal Henry", "liste": "RN", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "chevalier", "nom": "Thomas Chevalier", "liste": "Caen dynamique ! (centre ind\u00e9pendant)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "lareynie", "nom": "B\u00e9rang\u00e8re Lareynie", "liste": "Caen ouvri\u00e8re et r\u00e9volutionnaires (NPA-R)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "casevitz", "nom": "Pierre Casevitz", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
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
SRC_OLIVIER_TO = ("Tendance Ouest, d\u00e9cembre 2025", "https://www.tendanceouest.com/actualite-434343-municipales-2026-doublement-des-cameras-retour-du-week-end-maritime-aristide-olivier-candidat-a-caen")
SRC_OLIVIER_FB = ("France Bleu Normandie, d\u00e9cembre 2025", "https://www.francebleu.fr/infos/politique/municipales-2026-aristide-olivier-maire-de-caen-officiellement-candidat-6669872")
SRC_LORPHELIN_TO = ("Tendance Ouest, 2025", "https://www.tendanceouest.com/actualite-425946-municipales-2026-a-caen-rudy-l-orphelin-veut-mettre-le-climat-a-l-agenda-et-rassembler-la-gauche")
SRC_LORPHELIN_FB = ("France Bleu Normandie, f\u00e9vrier 2026", "https://www.francebleu.fr/emissions/ici-matin-info-ici-normandie/municipales-a-caen-rudy-l-orphelin-promet-la-gratuite-des-transports-pour-les-etudiants-3419951")
SRC_GUIDI_FB = ("France Bleu Normandie, janvier 2026", "https://www.francebleu.fr/infos/politique/municipales-2026-aurelien-guidi-lfi-annonce-sa-candidature-a-caen-trois-listes-de-gauches-desormais-en-competition-8411799")
SRC_CASINI_TO = ("Tendance Ouest, novembre 2025", "https://www.tendanceouest.com/actualite-433509-politique-antoine-casini-se-lance-dans-la-course-des-municipales-a-caen")
SRC_CHEVALIER_TO = ("Tendance Ouest, janvier 2026", "https://www.tendanceouest.com/actualite-435534-municipales-2026-a-caen-evince-par-son-parti-thomas-chevalier-se-retrouve-deja-un-nouveau-soutien-ecologiste")

PROPS = {
    # === SECURITE ===
    ("securite", "police-municipale", "olivier"): (
        "Augmentation des effectifs de police municipale de 70 \u00e0 100 agents",
        *SRC_OLIVIER_TO
    ),
    ("securite", "videoprotection", "olivier"): (
        "Doublement des cam\u00e9ras de vid\u00e9osurveillance, de 100 \u00e0 200",
        *SRC_OLIVIER_TO
    ),

    # === TRANSPORTS ===
    ("transports", "tarifs-gratuite", "olivier"): (
        "Gratuit\u00e9 des transports en commun chaque samedi pendant la dur\u00e9e des travaux du tramway",
        *SRC_OLIVIER_TO
    ),
    ("transports", "tarifs-gratuite", "lorphelin"): (
        "Gratuit\u00e9 des transports en commun pour les moins de 26 ans",
        *SRC_LORPHELIN_FB
    ),
    ("transports", "transports-en-commun", "lorphelin"): (
        "Bus en site propre plut\u00f4t qu'un nouveau tramway, pour un co\u00fbt moindre et une desserte plus large",
        *SRC_LORPHELIN_TO
    ),
    ("transports", "tarifs-gratuite", "guidi"): (
        "Gratuit\u00e9 totale des transports en commun \u00e0 Caen",
        *SRC_GUIDI_FB
    ),

    # === LOGEMENT ===
    ("logement", "encadrement-loyers", "lorphelin"): (
        "Exp\u00e9rimentation de l'encadrement des loyers \u00e0 Caen",
        *SRC_LORPHELIN_TO
    ),
    ("logement", "acces-logement", "casini"): (
        "R\u00e9vision du plan local d'urbanisme pour r\u00e9pondre \u00e0 la crise du logement en zone tendue depuis 2023",
        *SRC_CASINI_TO
    ),
    ("logement", "logement-social", "casini"): (
        "R\u00e9novation \u00e9nerg\u00e9tique du parc social : lutter contre les passoires thermiques, priorit\u00e9 mal trait\u00e9e",
        *SRC_CASINI_TO
    ),

    # === EDUCATION ===
    ("education", "petite-enfance", "olivier"): (
        "D\u00e9veloppement de l'offre de places en cr\u00e8che et structures petite enfance",
        *SRC_OLIVIER_TO
    ),
    ("education", "ecoles-renovation", "olivier"): (
        "Reconstruction des \u00e9coles Millepertuis et Venoix",
        *SRC_OLIVIER_TO
    ),
    ("education", "jeunesse", "guidi"): (
        "Politique jeunesse ambitieuse et lutte contre le sans-abrisme",
        *SRC_GUIDI_FB
    ),

    # === ENVIRONNEMENT ===
    ("environnement", "espaces-verts", "lorphelin"): (
        "Ouverture de nouveaux parcs pour une ville toujours plus verte",
        *SRC_LORPHELIN_TO
    ),
    ("environnement", "climat-adaptation", "lorphelin"): (
        "Mettre le climat \u00e0 l'agenda : transformation \u00e9cologique et justice sociale comme priorit\u00e9s du mandat",
        *SRC_LORPHELIN_TO
    ),

    # === SANTE ===
    ("sante", "seniors", "olivier"): (
        "Ouverture d'une Maison des seniors dans l'ancien centre de jeunesse de la Prairie",
        *SRC_OLIVIER_TO
    ),

    # === CULTURE ===
    ("culture", "evenements-creation", "olivier"): (
        "Retour du Week-end Maritime, grand rassemblement de bateaux \u00e0 Caen",
        *SRC_OLIVIER_TO
    ),

    # === URBANISME ===
    ("urbanisme", "amenagement-urbain", "chevalier"): (
        "Cr\u00e9ation d'un parc animalier sur la Presqu'\u00eele de Caen avec centre de soins pour animaux sauvages, mini-ferme et restaurant",
        *SRC_CHEVALIER_TO
    ),

    # === SOLIDARITE ===
    ("solidarite", "aide-sociale", "lorphelin"): (
        "Plus de solidarit\u00e9 alors qu'un Caennais sur 5 vit sous le seuil de pauvret\u00e9",
        *SRC_LORPHELIN_TO
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
