#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère et insère Nice dans app.js."""

import re

VILLE_ID = "nice"
VILLE_NOM = "Nice"
VILLE_CP = "06000"
ELECTION_ID = "nice-2026"

CANDIDATS = [
    {"id": "estrosi", "nom": "Christian Estrosi", "liste": "Nice au coeur (Horizons)", "programmeUrl": "https://estrosi2026.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "ciotti", "nom": "\u00c9ric Ciotti", "liste": "Ciotti 2026 (UDR/RN)", "programmeUrl": "https://www.ciotti2026.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "chesnel", "nom": "Juliette Chesnel-Le Roux", "liste": "Unis pour Nice (\u00c9cologistes/PS/PCF)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "damiano", "nom": "Mireille Damiano", "liste": "Nice Front Populaire (LFI/ViVA!)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "governatori", "nom": "Jean-Marc Governatori", "liste": "L'\u00e9cologie au centre", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "granouillac", "nom": "H\u00e9l\u00e8ne Granouillac", "liste": "Vivre Nice", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "dloussky", "nom": "Nathalie Dloussky", "liste": "Ensemble pour la grandeur de la France", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "vella", "nom": "C\u00e9dric Vella", "liste": "Reconqu\u00eate", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
]

CAND_IDS = [c["id"] for c in CANDIDATS]

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

# Sources
SRC_ESTROSI_FB = ("France Bleu Azur, f\u00e9vrier 2026", "https://www.francebleu.fr/")
SRC_ESTROSI_NP = ("Nice Premium, f\u00e9vrier 2026", "https://www.nicepremium.fr/")
SRC_ESTROSI_SITE = ("Site de campagne 2026", "https://estrosi2026.fr/")
SRC_CIOTTI_FB = ("France Bleu Azur, f\u00e9vrier 2026", "https://www.francebleu.fr/")
SRC_CIOTTI_NP = ("Nice Presse, f\u00e9vrier 2026", "https://nicepresse.com/")
SRC_CIOTTI_SITE = ("Site de campagne 2026", "https://www.ciotti2026.fr/")
SRC_CHESNEL_FB = ("France Bleu Azur, f\u00e9vrier 2026", "https://www.francebleu.fr/")
SRC_CHESNEL_NP = ("Nice Presse, f\u00e9vrier 2026", "https://nicepresse.com/")
SRC_DAMIANO_FB = ("France Bleu Azur, f\u00e9vrier 2026", "https://www.francebleu.fr/")
SRC_DAMIANO_NP = ("Nice Presse, f\u00e9vrier 2026", "https://nicepresse.com/")
SRC_GOVERNATORI_NP = ("Nice Premium, janvier 2026", "https://www.nicepremium.fr/")
SRC_GRANOUILLAC_NP = ("Nice Premium, janvier 2026", "https://www.nicepremium.fr/")
SRC_DLOUSSKY_NP = ("Nice Premium, janvier 2026", "https://www.nicepremium.fr/")

PROPS = {
    # === SECURITE ===
    ("securite", "police-municipale", "ciotti"): (
        "100 policiers municipaux suppl\u00e9mentaires d\u00e9ploy\u00e9s dans tous les quartiers de Nice",
        *SRC_CIOTTI_FB
    ),
    ("securite", "prevention-mediation", "chesnel"): (
        "Renforcement de la police de proximit\u00e9 et s\u00e9curit\u00e9 repens\u00e9e au service des habitants",
        *SRC_CHESNEL_NP
    ),
    ("securite", "prevention-mediation", "damiano"): (
        "S\u00e9curit\u00e9 publique bas\u00e9e sur la pr\u00e9vention et le travail social, refus de la s\u00e9curit\u00e9 priv\u00e9e",
        *SRC_DAMIANO_NP
    ),
    ("securite", "violences-femmes", "chesnel"): (
        "Doubler les places d'h\u00e9bergement d'urgence pour les femmes victimes de violences (de 80 \u00e0 160 places)",
        *SRC_CHESNEL_FB
    ),

    # === TRANSPORTS ===
    ("transports", "tarifs-gratuite", "chesnel"): (
        "Gratuit\u00e9 des transports en commun pour tous les Ni\u00e7ois",
        *SRC_CHESNEL_NP
    ),
    ("transports", "tarifs-gratuite", "damiano"): (
        "Gratuit\u00e9 progressive des transports : d'abord les week-ends, puis g\u00e9n\u00e9ralisation, financ\u00e9e par la taxe mobilit\u00e9 et la taxe de s\u00e9jour",
        *SRC_DAMIANO_NP
    ),

    # === LOGEMENT ===
    ("logement", "logement-social", "chesnel"): (
        "Application de la loi SRU : atteindre 25% de logements sociaux (contre 14% aujourd'hui), pr\u00e9emption de b\u00e2timents vacants",
        *SRC_CHESNEL_FB
    ),
    ("logement", "logement-social", "ciotti"): (
        "Vente des logements sociaux de C\u00f4te d'Azur Habitat hors m\u00e9tropole (400 M\u20ac) pour construire et r\u00e9nover du logement \u00e0 Nice",
        *SRC_CIOTTI_NP
    ),
    ("logement", "logements-vacants", "granouillac"): (
        "Transformer les bureaux vacants en logements et r\u00e9guler strictement les locations saisonni\u00e8res de type Airbnb",
        *SRC_GRANOUILLAC_NP
    ),
    ("logement", "encadrement-loyers", "chesnel"): (
        "Mise en place de l'encadrement des loyers \u00e0 Nice",
        *SRC_CHESNEL_NP
    ),
    ("logement", "encadrement-loyers", "damiano"): (
        "Encadrement des loyers et r\u00e9quisition de logements vacants",
        *SRC_DAMIANO_NP
    ),

    # === EDUCATION ===
    ("education", "ecoles-renovation", "estrosi"): (
        "Poursuite de la r\u00e9novation des \u00e9coles : 150 \u00e9tablissements r\u00e9nov\u00e9s depuis 2008, objectif de continuer sur le mandat",
        *SRC_ESTROSI_NP
    ),

    # === ENVIRONNEMENT ===
    ("environnement", "espaces-verts", "damiano"): (
        "Cr\u00e9ation de jardins partag\u00e9s et d'un r\u00e9seau vert urbain pour la biodiversit\u00e9 et le rafra\u00eechissement de la ville",
        *SRC_DAMIANO_NP
    ),
    ("environnement", "climat-adaptation", "chesnel"): (
        "Hausse de la taxe mobilit\u00e9 de 2% \u00e0 3,2% (60 M\u20ac d'investissement) et hausse de la taxe de s\u00e9jour au plafond l\u00e9gal pour financer la transition",
        *SRC_CHESNEL_FB
    ),
    ("environnement", "climat-adaptation", "granouillac"): (
        "Transition climatique prioritaire : gestion durable de l'eau face au stress hydrique",
        *SRC_GRANOUILLAC_NP
    ),
    ("environnement", "renovation-energetique", "governatori"): (
        "Autonomie \u00e9nerg\u00e9tique solaire : bornes solaires dans chaque quartier, impliquer les ultra-riches dans le financement",
        *SRC_GOVERNATORI_NP
    ),

    # === SANTE ===
    ("sante", "centres-sante", "estrosi"): (
        "Cr\u00e9ation de 8 maisons de sant\u00e9 d'ici 2030 (Ariane, Nice Nord...) et d'une maison m\u00e9dicale mobile \u00e0 domicile",
        *SRC_ESTROSI_FB
    ),

    # === DEMOCRATIE ===
    ("democratie", "transparence", "estrosi"): (
        "Chaque adjoint rencontre les Ni\u00e7ois 2 fois par an. Journ\u00e9e annuelle de r\u00e9f\u00e9rendums locaux",
        *SRC_ESTROSI_NP
    ),
    ("democratie", "transparence", "chesnel"): (
        "Code \u00e9thique de 12 pages : r\u00e9duction de 50% des indemnit\u00e9s des \u00e9lus municipaux",
        *SRC_CHESNEL_NP
    ),
    ("democratie", "transparence", "dloussky"): (
        "Commission d'observation de l'emploi public : audit des 8 500 employ\u00e9s municipaux avec experts ind\u00e9pendants et citoyens tir\u00e9s au sort",
        *SRC_DLOUSSKY_NP
    ),

    # === ECONOMIE ===
    ("economie", "attractivite", "ciotti"): (
        "Nouveau centre des congr\u00e8s et des expositions, projet \u00e9conomique majeur sur le site du March\u00e9 d'Int\u00e9r\u00eat National",
        *SRC_CIOTTI_NP
    ),
    ("economie", "attractivite", "damiano"): (
        "R\u00e9guler le tourisme polluant (jets priv\u00e9s, yachts, croisi\u00e8res) et d\u00e9velopper un tourisme \u00e9coresponsable",
        *SRC_DAMIANO_NP
    ),

    # === CULTURE ===
    ("culture", "equipements-culturels", "estrosi"): (
        "100 M\u20ac investis dans la culture sur le mandat. Palais des Arts et de la Culture : salle de th\u00e9\u00e2tre de 850 places sous la vo\u00fbte du palais des expositions",
        *SRC_ESTROSI_FB
    ),
    ("culture", "equipements-culturels", "ciotti"): (
        "Nouveau th\u00e9\u00e2tre sur le site de la Gare du Sud",
        *SRC_CIOTTI_NP
    ),

    # === URBANISME ===
    ("urbanisme", "quartiers-prioritaires", "ciotti"): (
        "Grand plan d'investissement pour les quartiers p\u00e9riph\u00e9riques : une ville \u00e0 deux vitesses n'est pas acceptable",
        *SRC_CIOTTI_NP
    ),

    # === SOLIDARITE ===
    ("solidarite", "aide-sociale", "chesnel"): (
        "Doubler les places d'h\u00e9bergement d'urgence et renforcer les dispositifs d'aide aux plus pr\u00e9caires",
        *SRC_CHESNEL_FB
    ),
    ("solidarite", "pouvoir-achat", "ciotti"): (
        "Annulation de la hausse de la taxe fonci\u00e8re vot\u00e9e l'ann\u00e9e pr\u00e9c\u00e9dente",
        *SRC_CIOTTI_FB
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
    return '\n'.join([
        f'{sp}{cand_id}: {{',
        f'{sp}  texte: "{escape_js(texte)}",',
        f'{sp}  source: "{escape_js(source)}",',
        f'{sp}  sourceUrl: "{escape_js(source_url)}"',
        f'{sp}}}'
    ])


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
    return (f'        {{ id: "{c["id"]}", nom: "{escape_js(c["nom"])}", '
            f'liste: "{escape_js(c["liste"])}", '
            f'programmeUrl: "{escape_js(c["programmeUrl"])}", '
            f'programmeComplet: {complet}, programmePdfPath: {pdf} }}')


def gen_election():
    lines = [
        f'    "{ELECTION_ID}": {{',
        f'      ville: "{escape_js(VILLE_NOM)}",',
        f'      annee: 2026,',
        f'      type: "\\u00C9lections municipales",',
        f'      dateVote: "2026-03-15T08:00:00",',
        f'      candidats: ['
    ]
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

    # 1. VILLES
    villes_entry = (f'    ,{{\n      id: "{VILLE_ID}",\n      nom: "{escape_js(VILLE_NOM)}",\n'
                    f'      codePostal: "{VILLE_CP}",\n      elections: ["{ELECTION_ID}"]\n    }}')
    if f'id: "{VILLE_ID}"' not in content[:content.find('var ELECTIONS')]:
        villes_end = content.find('  ];\n\n    var ELECTIONS')
        if villes_end == -1:
            villes_end = content.find('  ];\n\n  var ELECTIONS')
        content = content[:villes_end] + villes_entry + '\n' + content[villes_end:]
        print(f"Ville {VILLE_ID} ajoutee")
    else:
        print(f"Ville {VILLE_ID} existe deja")

    # 2. ELECTIONS
    if f'    "{ELECTION_ID}": {{' not in content:
        m = re.search(r'\n  \};\n\n+  // === ', content)
        if not m:
            print("ERREUR: fin ELECTIONS non trouvee")
            return
        content = content[:m.start()] + ',\n' + gen_election() + content[m.start():]
        print(f"Election {ELECTION_ID} ajoutee")
    else:
        print(f"Election {ELECTION_ID} existe deja")

    with open(app_js_path, 'w', encoding='utf-8') as f:
        f.write(content)

    count = len(PROPS)
    print(f"Total: {count} propositions")
    for cid in CAND_IDS:
        cn = next(c["nom"] for c in CANDIDATS if c["id"] == cid)
        cc = sum(1 for k in PROPS if k[2] == cid)
        print(f"  {cn}: {cc}")


if __name__ == "__main__":
    main()
