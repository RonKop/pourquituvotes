#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Amiens dans app.js."""
import re

VILLE_ID = "amiens"
VILLE_NOM = "Amiens"
VILLE_CP = "80000"
ELECTION_ID = "amiens-2026"

CANDIDATS = [
    {"id": "dejenlis", "nom": "Hubert de Jenlis", "liste": "Majorit\u00e9 pr\u00e9sidentielle (sortant)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "fauvet", "nom": "Fr\u00e9d\u00e9ric Fauvet", "liste": "Pour Amiens en Mieux (PS-PCF-EELV-PP)", "programmeUrl": "https://www.pouramiens.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "caron", "nom": "Aur\u00e9lien Caron", "liste": "Amiens Ville d'Avenir (LR)", "programmeUrl": "https://amiensvilledavenir.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "mercuzot", "nom": "Beno\u00eet Mercuzot", "liste": "Amiens en Mouvement", "programmeUrl": "https://www.amiensenmouvement.com/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "toumi", "nom": "Damien Toumi", "liste": "Amiens Pour Vous (RN)", "programmeUrl": "https://www.amienspourvous.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "olivier", "nom": "Samy Olivier", "liste": "Amiens en Commun (LFI-G.s)", "programmeUrl": "https://amiensencommun.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "decle", "nom": "Paul-\u00c9ric D\u00e8cle", "liste": "Les Centristes", "programmeUrl": "https://www.paulericdecle2026.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "bellina", "nom": "Julia Bellina", "liste": "Amiens au C\u0153ur (sans \u00e9tiquette)", "programmeUrl": "https://amiensaucoeur.fr/", "programmeComplet": False, "programmePdfPath": None},
    {"id": "farhat", "nom": "Ridha Farhat", "liste": "Les Enfants de la R\u00e9publique - Amiens pour tous", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "baudry", "nom": "Jean-Jacques Baudry", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
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

# --- Sources ---
SRC_JENLIS_FB = ("France Bleu Picardie, janvier 2026", "https://www.francebleu.fr/")
SRC_JENLIS_F3 = ("France 3 Hauts-de-France, 2025", "https://france3-regions.franceinfo.fr/")
SRC_JENLIS_MAIRIE = ("Mairie d'Amiens, 2025", "https://www.amiens.fr/")
SRC_FAUVET_FB = ("France Bleu Picardie, f\u00e9vrier 2026", "https://www.francebleu.fr/")
SRC_FAUVET_SITE = ("Pour Amiens, 2026", "https://www.pouramiens.fr/")
SRC_CARON_FB = ("France Bleu Picardie, septembre 2025", "https://www.francebleu.fr/")
SRC_CARON_SITE = ("Amiens Ville d'Avenir, 2025", "https://amiensvilledavenir.fr/")
SRC_MERCUZOT_FB = ("France Bleu Picardie, 2025", "https://www.francebleu.fr/")
SRC_MERCUZOT_SITE = ("Amiens en Mouvement, 2025", "https://www.amiensenmouvement.com/")
SRC_TOUMI_FB = ("France Bleu Picardie, mars 2025", "https://www.francebleu.fr/")
SRC_OLIVIER_FB = ("France Bleu Picardie, novembre 2025", "https://www.francebleu.fr/")
SRC_OLIVIER_SITE = ("Amiens en Commun, 2026", "https://amiensencommun.fr/")
SRC_DECLE_FB = ("France Bleu Picardie, mai 2025", "https://www.francebleu.fr/")
SRC_DECLE_SITE = ("Paul-\u00c9ric D\u00e8cle 2026, 2026", "https://www.paulericdecle2026.fr/")
SRC_BELLINA_SITE = ("Amiens au C\u0153ur, 2025", "https://amiensaucoeur.fr/")
SRC_FARHAT_FB = ("France Bleu Picardie, novembre 2024", "https://www.francebleu.fr/")

PROPS = {
    # ===================== SECURITE =====================
    ("securite", "police-municipale", "dejenlis"): (
        "Armement de la police municipale avec des armes l\u00e9tales, cr\u00e9ation d'une brigade canine et d'une brigade \u00e9questre",
        *SRC_JENLIS_MAIRIE
    ),
    ("securite", "police-municipale", "caron"): (
        "Doubler la pr\u00e9sence de la police municipale 7 jours sur 7 dans les rues, cr\u00e9er des brigades canine et \u00e9questre sp\u00e9cialis\u00e9es",
        *SRC_CARON_FB
    ),
    ("securite", "police-municipale", "fauvet"): (
        "Revoir le fonctionnement de la police municipale avec des postes dans les quartiers qui en ont besoin",
        *SRC_FAUVET_FB
    ),
    ("securite", "police-municipale", "toumi"): (
        "Priorit\u00e9 absolue \u00e0 la s\u00e9curit\u00e9 : renforcer la police municipale pour une ville plus s\u00fbre",
        *SRC_TOUMI_FB
    ),
    ("securite", "police-municipale", "decle"): (
        "Augmenter les effectifs de la police municipale et leur pr\u00e9sence sur le terrain",
        *SRC_DECLE_FB
    ),
    ("securite", "videoprotection", "caron"): (
        "Doubler le nombre de cam\u00e9ras de vid\u00e9osurveillance dans la ville",
        *SRC_CARON_FB
    ),
    ("securite", "prevention-mediation", "decle"): (
        "Renforcer les liens entre jeunes et police via des associations sportives \u00e0 vis\u00e9e pr\u00e9ventive",
        *SRC_DECLE_SITE
    ),

    # ===================== TRANSPORTS =====================
    ("transports", "transports-en-commun", "dejenlis"): (
        "Refonte du r\u00e9seau de bus am\u00e9lien pour am\u00e9liorer la r\u00e9gularit\u00e9 et la couverture des quartiers",
        *SRC_JENLIS_FB
    ),
    ("transports", "transports-en-commun", "fauvet"): (
        "Am\u00e9liorer la r\u00e9gularit\u00e9 et l'efficacit\u00e9 des transports en commun, v\u00e9cu au quotidien comme un probl\u00e8me majeur",
        *SRC_FAUVET_SITE
    ),
    ("transports", "transports-en-commun", "mercuzot"): (
        "Am\u00e9liorer les mobilit\u00e9s et la fluidit\u00e9 des d\u00e9placements, renforcer l'accessibilit\u00e9 \u00e0 Amiens notamment via la liaison ferroviaire Roissy-Picardie",
        *SRC_MERCUZOT_SITE
    ),
    ("transports", "tarifs-gratuite", "olivier"): (
        "\u00c9tendre la gratuit\u00e9 du bus les mercredis et dimanches, gratuit\u00e9 totale pour les moins de 25 ans",
        *SRC_OLIVIER_SITE
    ),
    ("transports", "pietons-circulation", "dejenlis"): (
        "Obligation de descendre de v\u00e9lo et trottinette en zone pi\u00e9tonne entre la tour Perret et la mairie, de 10h \u00e0 19h",
        *SRC_JENLIS_MAIRIE
    ),
    ("transports", "velo-mobilites-douces", "dejenlis"): (
        "Cr\u00e9ation de places de stationnement pour v\u00e9los et trottinettes en centre-ville",
        *SRC_JENLIS_MAIRIE
    ),

    # ===================== LOGEMENT =====================
    ("logement", "acces-logement", "mercuzot"): (
        "Reconqu\u00eate du parc de logements anciens pour offrir du travail aux entreprises locales et du pouvoir d'achat aux habitants",
        *SRC_MERCUZOT_SITE
    ),
    ("logement", "logement-social", "decle"): (
        "Faciliter l'acc\u00e8s au logement social pour les m\u00e9nages actifs",
        *SRC_DECLE_SITE
    ),
    ("logement", "acces-logement", "olivier"): (
        "R\u00e9quisitionner les logements vacants pour qu'aucun enfant ne dorme \u00e0 la rue",
        *SRC_OLIVIER_SITE
    ),

    # ===================== EDUCATION =====================
    ("education", "ecoles-renovation", "fauvet"): (
        "Augmenter massivement l'investissement pour l'entretien des \u00e9coles (1,14% du budget actuellement jug\u00e9 insuffisant)",
        *SRC_FAUVET_SITE
    ),
    ("education", "cantines-fournitures", "olivier"): (
        "Rendre l'\u00e9cole vraiment gratuite : cantine et fournitures scolaires prises en charge",
        *SRC_OLIVIER_SITE
    ),
    ("education", "jeunesse", "farhat"): (
        "Cr\u00e9er des maisons de la jeunesse et de la citoyennet\u00e9 et assurer la protection municipale de la jeunesse",
        *SRC_FARHAT_FB
    ),

    # ===================== ENVIRONNEMENT =====================
    ("environnement", "proprete-dechets", "dejenlis"): (
        "Op\u00e9rations de nettoyage renforc\u00e9es dans les quartiers pour am\u00e9liorer la propret\u00e9 urbaine",
        *SRC_JENLIS_MAIRIE
    ),
    ("environnement", "proprete-dechets", "toumi"): (
        "Faire de la propret\u00e9 une priorit\u00e9 : une ville plus propre et plus accessible",
        *SRC_TOUMI_FB
    ),
    ("environnement", "climat-adaptation", "mercuzot"): (
        "Politique \u00e9nerg\u00e9tique ambitieuse et d\u00e9veloppement du patrimoine naturel et architectural",
        *SRC_MERCUZOT_SITE
    ),
    ("environnement", "espaces-verts", "decle"): (
        "Lancer une op\u00e9ration massive de v\u00e9g\u00e9talisation de la ville et de ses toitures pour acc\u00e9l\u00e9rer la transition \u00e9cologique",
        *SRC_DECLE_SITE
    ),

    # ===================== SANTE =====================

    # ===================== DEMOCRATIE =====================
    ("democratie", "budget-participatif", "caron"): (
        "Instaurer des r\u00e9f\u00e9rendums locaux sur les grands projets structurants et renforcer la consultation citoyenne",
        *SRC_CARON_SITE
    ),
    ("democratie", "transparence", "bellina"): (
        "D\u00e9cisions prises en concertation avec les comit\u00e9s de quartier, chaque euro investi selon les besoins r\u00e9els du terrain",
        *SRC_BELLINA_SITE
    ),
    ("democratie", "vie-associative", "olivier"): (
        "Mettre fin \u00e0 la mise en concurrence des associations et \u00e0 la baisse syst\u00e9matique de leurs subventions",
        *SRC_OLIVIER_SITE
    ),
    ("democratie", "services-publics", "fauvet"): (
        "Construire une ville qui prot\u00e8ge avec des services publics locaux r\u00e9pondant aux besoins essentiels",
        *SRC_FAUVET_SITE
    ),

    # ===================== ECONOMIE =====================
    ("economie", "commerce-local", "caron"): (
        "Cr\u00e9er un p\u00f4le cr\u00e9atif, num\u00e9rique et cybercurit\u00e9 \u00e0 la Halle Freyssinet pour dynamiser l'\u00e9conomie locale",
        *SRC_CARON_FB
    ),
    ("economie", "attractivite", "mercuzot"): (
        "Garantir une qualit\u00e9 de ville unique en d\u00e9veloppant le patrimoine naturel et architectural, revitaliser le centre-ville",
        *SRC_MERCUZOT_SITE
    ),

    # ===================== CULTURE =====================

    # ===================== SPORT =====================

    # ===================== URBANISME =====================
    ("urbanisme", "amenagement-urbain", "mercuzot"): (
        "Embellir les espaces publics et cr\u00e9er une ville plus s\u00fbre et plus apais\u00e9e",
        *SRC_MERCUZOT_SITE
    ),
    ("urbanisme", "accessibilite", "decle"): (
        "Promouvoir et faciliter le quotidien des personnes en situation de handicap par des actions de sensibilisation et d'accessibilit\u00e9",
        *SRC_DECLE_SITE
    ),
    ("urbanisme", "quartiers-prioritaires", "caron"): (
        "Pacte de solidarit\u00e9 majeur pour les quartiers prioritaires de la ville",
        *SRC_CARON_SITE
    ),
    ("urbanisme", "amenagement-urbain", "decle"): (
        "Simplifier les r\u00e8gles d'urbanisme en accordant des d\u00e9rogations mineures pour faciliter les projets",
        *SRC_DECLE_SITE
    ),

    # ===================== SOLIDARITE =====================
    ("solidarite", "pouvoir-achat", "fauvet"): (
        "Lutter contre la baisse du pouvoir d'achat, la hausse des prix du logement et l'insalubrit\u00e9",
        *SRC_FAUVET_SITE
    ),
    ("solidarite", "pouvoir-achat", "farhat"): (
        "Augmenter le niveau de vie des Am\u00e9nois, priorit\u00e9 aux habitants des quartiers populaires",
        *SRC_FARHAT_FB
    ),
    ("solidarite", "aide-sociale", "olivier"): (
        "Cr\u00e9er un syst\u00e8me de s\u00e9curit\u00e9 alimentaire : alimentation locale \u00e0 prix fix\u00e9s",
        *SRC_OLIVIER_SITE
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
