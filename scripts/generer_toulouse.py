#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le bloc JS d'une élection pour une ville et l'insère dans app.js.
Usage: python -X utf8 scripts/generer_ville.py
"""

import re
import json

# === Configuration de la ville ===

VILLE_ID = "toulouse"
VILLE_NOM = "Toulouse"
VILLE_CP = "31000"
ELECTION_ID = "toulouse-2026"

CANDIDATS = [
    {
        "id": "moudenc",
        "nom": "Jean-Luc Moudenc",
        "liste": "Prot\u00e9geons l'avenir (DVD)",
        "programmeUrl": "https://moudenc2026.fr/",
        "programmeComplet": False,
        "programmePdfPath": None
    },
    {
        "id": "briancon",
        "nom": "Fran\u00e7ois Brian\u00e7on",
        "liste": "La gauche unie pour Toulouse (PS/EELV/PCF)",
        "programmeUrl": "#",
        "programmeComplet": False,
        "programmePdfPath": None
    },
    {
        "id": "piquemal",
        "nom": "Fran\u00e7ois Piquemal",
        "liste": "Demain Toulouse (LFI)",
        "programmeUrl": "https://piquemal2026.fr/le-programme/",
        "programmeComplet": False,
        "programmePdfPath": None
    },
    {
        "id": "leonardelli",
        "nom": "Julien Leonardelli",
        "liste": "Le bon sens toulousain (RN)",
        "programmeUrl": "https://www.lebonsenstoulousain.fr/",
        "programmeComplet": False,
        "programmePdfPath": None
    },
    {
        "id": "cottrel",
        "nom": "Arthur Cottrel",
        "liste": "J'aime Toulouse (Reconqu\u00eate)",
        "programmeUrl": "https://reconquete-toulouse.fr/",
        "programmeComplet": False,
        "programmePdfPath": None
    },
    {
        "id": "adrada",
        "nom": "Malena Adrada",
        "liste": "Le camp des travailleurs (LO)",
        "programmeUrl": "#",
        "programmeComplet": False,
        "programmePdfPath": None
    },
    {
        "id": "meilhac",
        "nom": "Lambert Meilhac & Domitille Allorant",
        "liste": "Nouvel Air (\u00c9quinoxe)",
        "programmeUrl": "https://www.toulouse-nouvel-air.fr/",
        "programmeComplet": False,
        "programmePdfPath": None
    }
]

CAND_IDS = [c["id"] for c in CANDIDATS]

# === Grille universelle ===

CATEGORIES = [
    ("securite", "S\u00e9curit\u00e9 & Pr\u00e9vention", [
        ("police-municipale", "Police municipale"),
        ("videoprotection", "Vid\u00e9oprotection"),
        ("prevention-mediation", "Pr\u00e9vention & M\u00e9diation"),
        ("violences-femmes", "Violences faites aux femmes"),
    ]),
    ("transports", "Transports & Mobilit\u00e9", [
        ("transports-en-commun", "Transports en commun"),
        ("velo-mobilites-douces", "V\u00e9lo & Mobilit\u00e9s douces"),
        ("pietons-circulation", "Pi\u00e9tons & Circulation"),
        ("stationnement", "Stationnement"),
        ("tarifs-gratuite", "Tarifs & Gratuit\u00e9"),
    ]),
    ("logement", "Logement", [
        ("logement-social", "Logement social"),
        ("logements-vacants", "Logements vacants"),
        ("encadrement-loyers", "Encadrement des loyers"),
        ("acces-logement", "Acc\u00e8s au logement"),
    ]),
    ("education", "\u00c9ducation & Jeunesse", [
        ("petite-enfance", "Petite enfance"),
        ("ecoles-renovation", "\u00c9coles & R\u00e9novation"),
        ("cantines-fournitures", "Cantines & Fournitures"),
        ("periscolaire-loisirs", "P\u00e9riscolaire & Loisirs"),
        ("jeunesse", "Jeunesse"),
    ]),
    ("environnement", "Environnement & Transition \u00e9cologique", [
        ("espaces-verts", "Espaces verts & Biodiversit\u00e9"),
        ("proprete-dechets", "Propret\u00e9 & D\u00e9chets"),
        ("climat-adaptation", "Climat & Adaptation"),
        ("renovation-energetique", "R\u00e9novation \u00e9nerg\u00e9tique"),
        ("alimentation-durable", "Alimentation durable"),
    ]),
    ("sante", "Sant\u00e9 & Acc\u00e8s aux soins", [
        ("centres-sante", "Centres de sant\u00e9"),
        ("prevention-sante", "Pr\u00e9vention sant\u00e9"),
        ("seniors", "Seniors"),
    ]),
    ("democratie", "D\u00e9mocratie & Vie citoyenne", [
        ("budget-participatif", "Budget participatif"),
        ("transparence", "Transparence"),
        ("vie-associative", "Vie associative"),
        ("services-publics", "Services publics"),
    ]),
    ("economie", "\u00c9conomie & Emploi", [
        ("commerce-local", "Commerce local"),
        ("emploi-insertion", "Emploi & Insertion"),
        ("attractivite", "Attractivit\u00e9"),
    ]),
    ("culture", "Culture & Patrimoine", [
        ("equipements-culturels", "\u00c9quipements culturels"),
        ("evenements-creation", "\u00c9v\u00e9nements & Cr\u00e9ation"),
    ]),
    ("sport", "Sport & Loisirs", [
        ("equipements-sportifs", "\u00c9quipements sportifs"),
        ("sport-pour-tous", "Sport pour tous"),
    ]),
    ("urbanisme", "Urbanisme & Cadre de vie", [
        ("amenagement-urbain", "Am\u00e9nagement urbain"),
        ("accessibilite", "Accessibilit\u00e9"),
        ("quartiers-prioritaires", "Quartiers prioritaires"),
    ]),
    ("solidarite", "Solidarit\u00e9 & \u00c9galit\u00e9", [
        ("aide-sociale", "Aide sociale"),
        ("egalite-discriminations", "\u00c9galit\u00e9 & Discriminations"),
        ("pouvoir-achat", "Pouvoir d'achat"),
    ]),
]

# === Propositions par (categorie_id, sous_theme_id, candidat_id) ===
# Valeur: (texte, source, sourceUrl) ou None

SRC_MOUDENC = ("Le Journal Toulousain, f\u00e9vrier 2026", "https://www.lejournaltoulousain.fr/")
SRC_MOUDENC_SITE = ("Site de campagne 2026", "https://moudenc2026.fr/")
SRC_BRIANCON = ("Le Journal Toulousain, f\u00e9vrier 2026", "https://www.lejournaltoulousain.fr/")
SRC_BRIANCON_FB = ("France Bleu Occitanie, f\u00e9vrier 2026", "https://www.francebleu.fr/")
SRC_PIQUEMAL = ("Mediacit\u00e9s Toulouse, janvier 2026", "https://www.mediacites.fr/")
SRC_PIQUEMAL_SITE = ("Site de campagne 2026", "https://piquemal2026.fr/")
SRC_PIQUEMAL_JT = ("Le Journal Toulousain, f\u00e9vrier 2026", "https://www.lejournaltoulousain.fr/")
SRC_LEONARDELLI = ("France Bleu Occitanie, janvier 2026", "https://www.francebleu.fr/")
SRC_COTTREL = ("Le Journal Toulousain, septembre 2025", "https://www.lejournaltoulousain.fr/")
SRC_NOUVEL_AIR = ("Le Journal Toulousain, octobre 2025", "https://www.lejournaltoulousain.fr/")
SRC_NOUVEL_AIR_F3 = ("France 3 Occitanie, octobre 2025", "https://france3-regions.franceinfo.fr/")

PROPS = {
    # === SECURITE ===
    ("securite", "police-municipale", "piquemal"): (
        "Police de proximit\u00e9 renforc\u00e9e, priorit\u00e9 \u00e0 la pr\u00e9vention et au lien social plut\u00f4t qu'aux dispositifs r\u00e9pressifs",
        *SRC_PIQUEMAL_JT
    ),
    ("securite", "police-municipale", "leonardelli"): (
        "Pr\u00e9sence polici\u00e8re renforc\u00e9e aux abords des \u00e9coles",
        *SRC_LEONARDELLI
    ),
    ("securite", "police-municipale", "meilhac"): (
        "R\u00e9orienter le budget vid\u00e9osurveillance vers le recrutement de policiers municipaux",
        *SRC_NOUVEL_AIR
    ),
    ("securite", "videoprotection", "moudenc"): (
        "Installer une cam\u00e9ra de vid\u00e9osurveillance dans chaque rue de Toulouse",
        *SRC_MOUDENC
    ),
    ("securite", "prevention-mediation", "piquemal"): (
        "Cr\u00e9ation d'un office municipal de m\u00e9diation pour r\u00e9soudre les conflits de voisinage et les incivilit\u00e9s",
        *SRC_PIQUEMAL_JT
    ),

    # === TRANSPORTS ===
    ("transports", "transports-en-commun", "moudenc"): (
        "Prolongement du t\u00e9l\u00e9ph\u00e9rique T\u00e9l\u00e9o vers Malep\u00e8re pour desservir un nouveau quartier de 15 000 habitants",
        *SRC_MOUDENC
    ),
    ("transports", "transports-en-commun", "briancon"): (
        "Soutien au Service Express R\u00e9gional M\u00e9tropolitain (SERM) et abandon du projet Jonction Est",
        *SRC_BRIANCON
    ),
    ("transports", "transports-en-commun", "piquemal"): (
        "Cr\u00e9ation d'un RER m\u00e9tropolitain comme colonne vert\u00e9brale pour d\u00e9sengorger la m\u00e9tropole",
        *SRC_PIQUEMAL_JT
    ),
    ("transports", "velo-mobilites-douces", "meilhac"): (
        "Convertir les routes p\u00e9n\u00e9trantes en sens unique pour cr\u00e9er des voies bus et pistes cyclables",
        *SRC_NOUVEL_AIR
    ),
    ("transports", "pietons-circulation", "meilhac"): (
        "R\u00e9duire de 100 000 voitures dans l'aire urbaine d'ici 2032",
        *SRC_NOUVEL_AIR
    ),
    ("transports", "tarifs-gratuite", "briancon"): (
        "Tarification sociale des transports en commun",
        *SRC_BRIANCON
    ),
    ("transports", "tarifs-gratuite", "piquemal"): (
        "Gratuit\u00e9 des transports pour les moins de 26 ans d'ici 2030, avec r\u00e9duction mensuelle d\u00e8s septembre 2026",
        *SRC_PIQUEMAL
    ),

    # === LOGEMENT ===
    ("logement", "logement-social", "briancon"): (
        "15 000 nouveaux logements abordables sur le mandat, dont 7 500 via le Bail R\u00e9el Solidaire (BRS)",
        *SRC_BRIANCON
    ),
    ("logement", "encadrement-loyers", "moudenc"): (
        "Refus de l'encadrement des loyers : privil\u00e9gier la construction pour faire baisser les prix",
        *SRC_MOUDENC
    ),
    ("logement", "encadrement-loyers", "briancon"): (
        "Candidature aupr\u00e8s de l'\u00c9tat pour exp\u00e9rimenter l'encadrement des loyers \u00e0 Toulouse avant fin 2026",
        *SRC_BRIANCON
    ),
    ("logement", "encadrement-loyers", "piquemal"): (
        "Mise en place de l'encadrement des loyers \u00e0 Toulouse",
        *SRC_PIQUEMAL_JT
    ),
    ("logement", "acces-logement", "moudenc"): (
        "Cr\u00e9ation d'une assurance logement municipale pour les familles",
        *SRC_MOUDENC
    ),
    ("logement", "acces-logement", "briancon"): (
        "R\u00e9novation massive de 30 000 logements sur le mandat",
        *SRC_BRIANCON
    ),
    ("logement", "acces-logement", "meilhac"): (
        "Priorit\u00e9 \u00e0 la r\u00e9habilitation du parc existant plut\u00f4t qu'\u00e0 la construction neuve",
        *SRC_NOUVEL_AIR
    ),

    # === EDUCATION ===
    ("education", "ecoles-renovation", "leonardelli"): (
        "Instaurer l'uniforme dans les \u00e9coles de Toulouse",
        *SRC_LEONARDELLI
    ),
    ("education", "cantines-fournitures", "piquemal"): (
        "Gratuit\u00e9 des cantines scolaires et des fournitures pour toutes les familles",
        *SRC_PIQUEMAL
    ),

    # === ENVIRONNEMENT ===
    ("environnement", "espaces-verts", "briancon"): (
        "Toulouse ville-jardin : 3 arbres visibles depuis chaque logement, 30% de couverture v\u00e9g\u00e9tale par quartier, espace vert \u00e0 moins de 300m de chaque habitant",
        *SRC_BRIANCON
    ),
    ("environnement", "espaces-verts", "meilhac"): (
        "V\u00e9g\u00e9talisation intensive : toits, rues et espaces publics, inspir\u00e9e d'exp\u00e9riences d'autres villes europ\u00e9ennes",
        *SRC_NOUVEL_AIR
    ),
    ("environnement", "climat-adaptation", "piquemal"): (
        "R\u00e9duction de 55% des \u00e9missions de gaz \u00e0 effet de serre de la m\u00e9tropole d'ici 2030",
        *SRC_PIQUEMAL
    ),

    # === SANTE ===
    ("sante", "centres-sante", "piquemal"): (
        "Cr\u00e9ation de centres de sant\u00e9 municipaux dans les quartiers",
        *SRC_PIQUEMAL
    ),
    ("sante", "prevention-sante", "moudenc"): (
        "Extension de la mutuelle municipale au-del\u00e0 des seniors",
        *SRC_MOUDENC
    ),

    # === DEMOCRATIE ===
    ("democratie", "budget-participatif", "piquemal"): (
        "Cr\u00e9ation de 60 coop\u00e9ratives de quartier avec pouvoir de d\u00e9cision sur l'urbanisme et la mobilit\u00e9",
        *SRC_PIQUEMAL_JT
    ),
    ("democratie", "services-publics", "briancon"): (
        "Retour en r\u00e9gie municipale de la gestion de l'eau et de l'assainissement",
        *SRC_BRIANCON
    ),

    # === ECONOMIE ===
    ("economie", "emploi-insertion", "moudenc"): (
        "Soutien \u00e0 l'a\u00e9ronautique (Airbus, Safran) et \u00e0 l'industrie locale, seule liste pro-entreprise et pro-emploi",
        *SRC_MOUDENC
    ),

    # === CULTURE ===
    ("culture", "equipements-culturels", "briancon"): (
        "Augmentation des d\u00e9penses culturelles et gratuit\u00e9 totale des biblioth\u00e8ques municipales",
        *SRC_BRIANCON
    ),

    # === SPORT ===
    ("sport", "equipements-sportifs", "moudenc"): (
        "Agrandissement du Stadium de Toulouse",
        *SRC_MOUDENC_SITE
    ),

    # === URBANISME ===
    ("urbanisme", "amenagement-urbain", "leonardelli"): (
        "Cr\u00e9ation d'arrondissements \u00e0 Toulouse, troisi\u00e8me ville de France, pour plus de proximit\u00e9 et de vie de quartier",
        *SRC_LEONARDELLI
    ),
    ("urbanisme", "amenagement-urbain", "cottrel"): (
        "Cr\u00e9ation de districts sur le mod\u00e8le de Paris, Lyon et Marseille pour favoriser la vie de quartier",
        *SRC_COTTREL
    ),

    # === SOLIDARITE ===
    ("solidarite", "pouvoir-achat", "moudenc"): (
        "Aucune hausse des imp\u00f4ts locaux sur le mandat",
        *SRC_MOUDENC_SITE
    ),
    ("solidarite", "pouvoir-achat", "briancon"): (
        "Suppression de la tarification saisonni\u00e8re de l'eau pour prot\u00e9ger le pouvoir d'achat",
        *SRC_BRIANCON
    ),
    ("solidarite", "pouvoir-achat", "leonardelli"): (
        "Priorit\u00e9 au pouvoir d'achat des familles toulousaines",
        *SRC_LEONARDELLI
    ),
}


def escape_js(s):
    """Encode une chaîne Python en chaîne JS avec \\uXXXX escapes."""
    result = []
    for ch in s:
        cp = ord(ch)
        if cp > 127:
            result.append(f"\\u{cp:04X}")
        elif ch == '"':
            result.append('\\"')
        elif ch == '\\':
            result.append('\\\\')
        elif ch == '\n':
            result.append('\\n')
        else:
            result.append(ch)
    return ''.join(result)


def gen_proposition(cat_id, st_id, cand_id, indent=16):
    """Génère le JS pour une proposition d'un candidat."""
    key = (cat_id, st_id, cand_id)
    sp = ' ' * indent
    if key not in PROPS:
        return f"{sp}{cand_id}: null"
    texte, source, source_url = PROPS[key]
    lines = [
        f'{sp}{cand_id}: {{',
        f'{sp}  texte: "{escape_js(texte)}",',
        f'{sp}  source: "{escape_js(source)}",',
        f'{sp}  sourceUrl: "{escape_js(source_url)}"',
        f'{sp}}}'
    ]
    return '\n'.join(lines)


def gen_sous_theme(cat_id, st_id, st_nom, indent=12):
    sp = ' ' * indent
    lines = [
        f'{sp}{{',
        f'{sp}  id: "{st_id}",',
        f'{sp}  nom: "{escape_js(st_nom)}",',
        f'{sp}  propositions: {{'
    ]
    props = []
    for cid in CAND_IDS:
        props.append(gen_proposition(cat_id, st_id, cid))
    lines.append(',\n'.join(props))
    lines.append(f'{sp}  }}')
    lines.append(f'{sp}}}')
    return '\n'.join(lines)


def gen_categorie(cat_id, cat_nom, sous_themes, indent=8):
    sp = ' ' * indent
    lines = [
        f'{sp}{{',
        f'{sp}  id: "{cat_id}",',
        f'{sp}  nom: "{escape_js(cat_nom)}",',
        f'{sp}  sousThemes: ['
    ]
    sts = []
    for st_id, st_nom in sous_themes:
        sts.append(gen_sous_theme(cat_id, st_id, st_nom))
    lines.append(',\n'.join(sts))
    lines.append(f'{sp}  ]')
    lines.append(f'{sp}}}')
    return '\n'.join(lines)


def gen_candidat(c):
    pdf = "null" if c["programmePdfPath"] is None else f'"{escape_js(c["programmePdfPath"])}"'
    complet = "true" if c["programmeComplet"] else "false"
    return (
        f'        {{ id: "{c["id"]}", nom: "{escape_js(c["nom"])}", '
        f'liste: "{escape_js(c["liste"])}", '
        f'programmeUrl: "{escape_js(c["programmeUrl"])}", '
        f'programmeComplet: {complet}, programmePdfPath: {pdf} }}'
    )


def gen_election():
    lines = [
        f'    "{ELECTION_ID}": {{',
        f'      ville: "{escape_js(VILLE_NOM)}",',
        f'      annee: 2026,',
        f'      type: "\\u00C9lections municipales",',
        f'      dateVote: "2026-03-15T08:00:00",',
        f'      candidats: ['
    ]
    cands = [gen_candidat(c) for c in CANDIDATS]
    lines.append(',\n'.join(cands))
    lines.append('      ],')
    lines.append('      categories: [')
    cats = []
    for cat_id, cat_nom, sts in CATEGORIES:
        cats.append(gen_categorie(cat_id, cat_nom, sts))
    lines.append(',\n'.join(cats))
    lines.append('      ]')
    lines.append('    }')
    return '\n'.join(lines)


def main():
    app_js_path = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\js\app.js"

    with open(app_js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ajouter la ville dans VILLES (avant le ];)
    villes_entry = (
        f'    ,{{\n'
        f'      id: "{VILLE_ID}",\n'
        f'      nom: "{escape_js(VILLE_NOM)}",\n'
        f'      codePostal: "{VILLE_CP}",\n'
        f'      elections: ["{ELECTION_ID}"]\n'
        f'    }}'
    )

    # Trouver la fin de VILLES (le ];\n avant var ELECTIONS)
    villes_end = content.find('  ];\n\n    var ELECTIONS')
    if villes_end == -1:
        villes_end = content.find('  ];\n\n  var ELECTIONS')
    if villes_end == -1:
        print("ERREUR: Impossible de trouver la fin de VILLES")
        return

    # Vérifier si la ville existe déjà
    if f'id: "{VILLE_ID}"' in content[:villes_end + 10]:
        print(f"La ville {VILLE_ID} existe d\u00e9j\u00e0 dans VILLES, on passe.")
    else:
        # Insérer juste avant le ];
        content = content[:villes_end] + villes_entry + '\n' + content[villes_end:]
        print(f"Ville {VILLE_ID} ajout\u00e9e \u00e0 VILLES")

    # 2. Ajouter l'élection dans ELECTIONS (avant le };)
    election_data = gen_election()

    # Trouver la fin de ELECTIONS (le }; qui ferme l'objet)
    # C'est le "  };" sur sa propre ligne après les données
    elections_end_pattern = re.search(r'\n  \};\n\n\n  // === ', content)
    if not elections_end_pattern:
        elections_end_pattern = re.search(r'\n  \};\n\n  // === ', content)
    if not elections_end_pattern:
        print("ERREUR: Impossible de trouver la fin de ELECTIONS")
        return

    insert_pos = elections_end_pattern.start()

    # Vérifier si l'élection existe déjà (chercher la clé dans ELECTIONS, pas dans VILLES)
    if f'    "{ELECTION_ID}": {{' in content:
        print(f"L'\u00e9lection {ELECTION_ID} existe d\u00e9j\u00e0, on passe.")
    else:
        election_block = ',\n' + election_data
        content = content[:insert_pos] + election_block + content[insert_pos:]
        print(f"\u00c9lection {ELECTION_ID} ajout\u00e9e")

    # 3. Écrire le fichier
    with open(app_js_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("app.js mis \u00e0 jour avec succ\u00e8s!")

    # Compter les propositions
    count = sum(1 for k in PROPS if PROPS[k] is not None)
    print(f"Propositions int\u00e9gr\u00e9es : {count}")
    for cid in CAND_IDS:
        c_count = sum(1 for k in PROPS if k[2] == cid)
        c_name = next(c["nom"] for c in CANDIDATS if c["id"] == cid)
        print(f"  {c_name}: {c_count} propositions")


if __name__ == "__main__":
    main()
