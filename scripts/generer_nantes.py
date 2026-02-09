#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère et insère Nantes dans app.js."""
import re

VILLE_ID = "nantes"
VILLE_NOM = "Nantes"
VILLE_CP = "44000"
ELECTION_ID = "nantes-2026"

CANDIDATS = [
    {"id": "rolland", "nom": "Johanna Rolland", "liste": "La gauche unie pour Nantes (PS/EELV/PCF)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "chombart", "nom": "Foulques Chombart de Lauwe", "liste": "Un nouveau souffle pour Nantes (LR/MoDem/Horizons)", "programmeUrl": "https://www.foulqueschombartdelauwe.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "aucant", "nom": "William Aucant", "liste": "Nouvelle Nantes (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "medkour", "nom": "Margot Medkour", "liste": "Nantes populaire", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "belhamiti", "nom": "Mounir Belhamiti", "liste": "Nantes m\u00e9rite mieux (Renaissance)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "hulot", "nom": "Jean-Claude Hulot", "liste": "Pour une Nantes s\u00fbre (RN)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "bazille", "nom": "Nicolas Bazille", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "gauvin", "nom": "Alexandre Gauvin", "liste": "Nantes ouvri\u00e8re et r\u00e9volutionnaire (NPA)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
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

SRC_ROLLAND_FB = ("France Bleu Loire Oc\u00e9an, f\u00e9vrier 2026", "https://www.francebleu.fr/")
SRC_ROLLAND_IM = ("Infos M\u00e9dia Nantes, f\u00e9vrier 2026", "https://infos-media-nantes.fr/")
SRC_CHOMBART_FB = ("France Bleu Loire Oc\u00e9an, f\u00e9vrier 2026", "https://www.francebleu.fr/")
SRC_CHOMBART_SITE = ("Site de campagne 2026", "https://www.foulqueschombartdelauwe.fr/")
SRC_AUCANT_FB = ("France Bleu Loire Oc\u00e9an, f\u00e9vrier 2026", "https://www.francebleu.fr/")
SRC_MEDKOUR_HG = ("Hello Gazette Nantes, f\u00e9vrier 2026", "https://hellogazettenantes.fr/")
SRC_BELHAMITI_HG = ("Hello Gazette Nantes, janvier 2026", "https://hellogazettenantes.fr/")
SRC_HULOT_FB = ("France Bleu Loire Oc\u00e9an, janvier 2026", "https://www.francebleu.fr/")

PROPS = {
    # === SECURITE ===
    ("securite", "police-municipale", "rolland"): (
        "Nouveau commissariat dans un quartier prioritaire et poste de police fixe nocturne au Bouffay et vers le Hangar \u00e0 bananes",
        *SRC_ROLLAND_FB
    ),
    ("securite", "police-municipale", "chombart"): (
        "Renforcement et armement de la police municipale",
        *SRC_CHOMBART_SITE
    ),
    ("securite", "police-municipale", "belhamiti"): (
        "Espace de police permanent au c\u0153ur de la ville et armement des policiers municipaux",
        *SRC_BELHAMITI_HG
    ),
    ("securite", "videoprotection", "chombart"): (
        "D\u00e9veloppement de la vid\u00e9osurveillance dans l'ensemble de la ville",
        *SRC_CHOMBART_SITE
    ),
    ("securite", "prevention-mediation", "chombart"): (
        "Lutte contre la consommation de drogue dans l'espace public",
        *SRC_CHOMBART_SITE
    ),
    ("securite", "prevention-mediation", "aucant"): (
        "Doubler le nombre de m\u00e9diateurs dans les rues, priorit\u00e9 \u00e0 la pr\u00e9vention plut\u00f4t qu'\u00e0 la r\u00e9pression",
        *SRC_AUCANT_FB
    ),

    # === TRANSPORTS ===
    ("transports", "transports-en-commun", "chombart"): (
        "D\u00e9veloppement des transports en commun et projet de tunnel sous la Loire",
        *SRC_CHOMBART_FB
    ),
    ("transports", "velo-mobilites-douces", "rolland"): (
        "150 kilom\u00e8tres suppl\u00e9mentaires de pistes cyclables sur le mandat",
        *SRC_ROLLAND_FB
    ),
    ("transports", "velo-mobilites-douces", "chombart"): (
        "S\u00e9curiser la pratique du v\u00e9lo dans toute la ville",
        *SRC_CHOMBART_SITE
    ),
    ("transports", "tarifs-gratuite", "rolland"): (
        "\u00c9tendre la gratuit\u00e9 des transports en commun \u00e0 15 000 personnes suppl\u00e9mentaires",
        *SRC_ROLLAND_FB
    ),
    ("transports", "tarifs-gratuite", "aucant"): (
        "Gratuit\u00e9 progressive des transports : d'abord pour les moins de 26 ans, les ch\u00f4meurs et les bas revenus",
        *SRC_AUCANT_FB
    ),

    # === LOGEMENT ===
    ("logement", "logement-social", "rolland"): (
        "Atteindre 40% de logements sociaux \u00e0 Nantes",
        *SRC_ROLLAND_FB
    ),
    ("logement", "encadrement-loyers", "aucant"): (
        "Mise en place de l'encadrement des loyers \u00e0 Nantes",
        *SRC_AUCANT_FB
    ),

    # === EDUCATION ===
    ("education", "petite-enfance", "rolland"): (
        "Service de garde d'urgence pour les familles monoparentales et d\u00e9veloppement des places en cr\u00e8che",
        *SRC_ROLLAND_IM
    ),

    # === ENVIRONNEMENT ===
    ("environnement", "espaces-verts", "rolland"): (
        "Moins de bitume en ville et plus de v\u00e9g\u00e9talisation des espaces publics",
        *SRC_ROLLAND_FB
    ),
    ("environnement", "espaces-verts", "chombart"): (
        "V\u00e9g\u00e9talisation des espaces publics dans une \u00e9cologie de bon sens",
        *SRC_CHOMBART_SITE
    ),
    ("environnement", "renovation-energetique", "rolland"): (
        "Acc\u00e9l\u00e9rer la r\u00e9novation des passoires \u00e9nerg\u00e9tiques",
        *SRC_ROLLAND_FB
    ),

    # === ECONOMIE ===
    ("economie", "attractivite", "chombart"): (
        "Faire de Nantes une ville \u00e9conomiquement rayonnante, on ne peut pas vivre que d'aides sociales",
        *SRC_CHOMBART_SITE
    ),

    # === CULTURE ===
    ("culture", "equipements-culturels", "medkour"): (
        "Cr\u00e9ation d'un centre d'arts et des savoirs communal au march\u00e9 de Feltre (quartier Bretagne)",
        *SRC_MEDKOUR_HG
    ),

    # === SOLIDARITE ===
    ("solidarite", "aide-sociale", "rolland"): (
        "Plateforme d'accompagnement d\u00e9di\u00e9e aux familles monoparentales : aide quotidienne et garde d'urgence",
        *SRC_ROLLAND_IM
    ),
}


def escape_js(s):
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
    key = (cat_id, st_id, cand_id)
    sp = ' ' * indent
    if key not in PROPS:
        return f"{sp}{cand_id}: null"
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
    lines.append('      ],')
    lines.append('      categories: [')
    lines.append(',\n'.join(gen_categorie(cid, cn, sts) for cid, cn, sts in CATEGORIES))
    lines += ['      ]', '    }']
    return '\n'.join(lines)

def main():
    app_js_path = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\js\app.js"
    with open(app_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if f'id: "{VILLE_ID}"' not in content[:content.find('var ELECTIONS')]:
        villes_end = content.find('  ];\n\n    var ELECTIONS')
        if villes_end == -1: villes_end = content.find('  ];\n\n  var ELECTIONS')
        entry = f'    ,{{\n      id: "{VILLE_ID}",\n      nom: "{escape_js(VILLE_NOM)}",\n      codePostal: "{VILLE_CP}",\n      elections: ["{ELECTION_ID}"]\n    }}'
        content = content[:villes_end] + entry + '\n' + content[villes_end:]
        print(f"Ville {VILLE_ID} ajoutee")
    else:
        print(f"Ville {VILLE_ID} existe deja")
    if f'    "{ELECTION_ID}": {{' not in content:
        m = re.search(r'\n  \};\n\n+  // === ', content)
        content = content[:m.start()] + ',\n' + gen_election() + content[m.start():]
        print(f"Election {ELECTION_ID} ajoutee")
    else:
        print(f"Election {ELECTION_ID} existe deja")
    with open(app_js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Total: {len(PROPS)} propositions")
    for cid in CAND_IDS:
        cn = next(c["nom"] for c in CANDIDATS if c["id"] == cid)
        print(f"  {cn}: {sum(1 for k in PROPS if k[2] == cid)}")

if __name__ == "__main__":
    main()
