#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Rouen dans app.js."""
import re

VILLE_ID = "rouen"
VILLE_NOM = "Rouen"
VILLE_CP = "76000"
ELECTION_ID = "rouen-2026"

CANDIDATS = [
    {"id": "mayer-rossignol", "nom": "Nicolas Mayer-Rossignol", "liste": "Fiers de Rouen (PS/EELV/PCF/PP)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "caron", "nom": "Marine Caron", "liste": "Horizons / LR", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "da-silva", "nom": "Maxime Da Silva", "liste": "Faire mieux \u00e0 Rouen (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "houdan", "nom": "Gr\u00e9goire Houdan", "liste": "RN/UDR", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "mazier", "nom": "Fr\u00e9d\u00e9ric Mazier", "liste": "Reconqu\u00eate", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "moisan", "nom": "\u00c9ric Moisan", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "vitard", "nom": "C\u00e9line Vitard", "liste": "Parti des travailleurs (POID)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "renauld", "nom": "Amaury Renauld", "liste": "NPA-R\u00e9volutionnaires", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
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
SRC_NMR_FB = ("France Bleu Normandie, janvier 2026", "https://www.francebleu.fr/infos/politique/municipales-rouen-nicolas-mayer-rossignol-candidat-pour-un-second-mandat-a-rouen-9664633")
SRC_NMR_TO = ("Tendance Ouest, janvier 2026", "https://www.tendanceouest.com/actualite-435238-municipales-2026-a-rouen-le-maire-sortant-nicolas-mayer-rossignol-officialise-sa-candidature")
SRC_NMR_SAN = ("Tendance Ouest, f\u00e9vrier 2026", "https://www.tendanceouest.com/actualite-436133-municipales-2026-mutuelle-communale-consultations-psychologiques-pour-les-jeunes-nicolas-mayer-rossignol-devoile-ses-propositions-pour-la-sante-a-rouen")
SRC_NMR_CUL = ("Tendance Ouest, juin 2025", "https://www.tendanceouest.com/actualite-430651-municipales-2026-le-maire-de-rouen-nicolas-mayer-rossignol-appelle-les-candidats-de-gauche-a-sanctuariser-les-budgets-pour-la-culture")
SRC_CAR_FB = ("France Bleu Normandie, janvier 2026", "https://www.francebleu.fr/infos/politique/securite-sante-impots-la-candidate-a-la-mairie-de-rouen-marine-caron-devoile-son-programme-4692010")
SRC_CAR_TO = ("Tendance Ouest, septembre 2025", "https://www.tendanceouest.com/actualite-432460-municipales-marine-caron-officialise-sa-candidature-a-rouen-et-met-l-accent-sur-la-securite")
SRC_DS_FB = ("France Bleu Normandie, novembre 2025", "https://www.francebleu.fr/emissions/ici-matin-l-invite-ici-normandie/nous-portons-un-projet-de-rupture-affirme-maxime-da-silva-candidat-lfi-aux-municipales-a-rouen-7041783")
SRC_DS_TO = ("Tendance Ouest, novembre 2025", "https://www.tendanceouest.com/actualite-433650-rouen-maxime-da-silva-de-la-france-insoumise-se-declare-officiellement-tete-de-liste-pour-les-municipales")
SRC_HOU_JDD = ("Le JDD, novembre 2025", "https://www.lejdd.fr/politique/gregoire-houdan-candidat-rn-aux-municipales-je-veux-faire-de-rouen-la-ville-la-plus-sure-de-france-164483")
SRC_HOU_FB = ("France Bleu Normandie, novembre 2025", "https://www.francebleu.fr/infos/politique/gregoire-houdan-sera-le-candidat-rn-a-rouen-pour-les-elections-municipales-2026-6495973")
SRC_MAZ_TO = ("Tendance Ouest, f\u00e9vrier 2026", "https://www.tendanceouest.com/actualite-434691-municipales-2026-frederic-mazier-tete-de-liste-reconquete-a-rouen-veut-regler-les-problemes-d-insecurite")
SRC_REN_NPA = ("NPA-R\u00e9volutionnaires, f\u00e9vrier 2026", "https://npa-revolutionnaires.org/a-rouen-aux-elections-municipales-de-2026-le-npa-revolutionnaires-presentera-une-liste-conduite-par-amaury-renauld-23-ans-etudiant/")
SRC_REN_TO = ("Tendance Ouest, f\u00e9vrier 2026", "https://www.tendanceouest.com/actualite-435585-municipales-2026-ce-qui-transformera-la-societe-ce-sera-la-lutte-amaury-renauld-est-tete-de-liste-npa-r-a-rouen")

PROPS = {
    # ===================== MAYER-ROSSIGNOL (PS) =====================
    # === SECURITE ===
    ("securite", "police-municipale", "mayer-rossignol"): (
        "Police municipale 24h/24, 7j/7, avec d\u00e9veloppement des brigades de nuit",
        *SRC_NMR_FB
    ),
    # === TRANSPORTS ===
    ("transports", "transports-en-commun", "mayer-rossignol"): (
        "Nouveau m\u00e9tro-tramway pour la m\u00e9tropole rouennaise",
        *SRC_NMR_FB
    ),
    ("transports", "tarifs-gratuite", "mayer-rossignol"): (
        "Extension de la gratuit\u00e9 des transports aux moins de 25 ans et aux plus de 65 ans (d\u00e9j\u00e0 gratuit pour les moins de 18 ans)",
        *SRC_NMR_FB
    ),
    # === EDUCATION ===
    ("education", "petite-enfance", "mayer-rossignol"): (
        "Mesures d'aide \u00e0 la garde d'enfants pour les familles monoparentales",
        *SRC_NMR_FB
    ),
    # === SANTE ===
    ("sante", "centres-sante", "mayer-rossignol"): (
        "Cr\u00e9ation d'un centre municipal de sant\u00e9 avec m\u00e9decins salari\u00e9s, deux nouvelles Maisons France Sant\u00e9 (Sapins et Saint-\u00c9loi), mutuelle communale pour faciliter l'acc\u00e8s aux soins",
        *SRC_NMR_SAN
    ),
    ("sante", "prevention-sante", "mayer-rossignol"): (
        "Consultations psychologiques gratuites pour les jeunes, parkings gratuits aux centres hospitaliers, sport sur ordonnance",
        *SRC_NMR_SAN
    ),
    # === CULTURE ===
    ("culture", "equipements-culturels", "mayer-rossignol"): (
        "Sanctuarisation et augmentation du budget culture de la ville et de la m\u00e9tropole",
        *SRC_NMR_CUL
    ),
    # === SPORT ===
    ("sport", "sport-pour-tous", "mayer-rossignol"): (
        "Faire de Rouen la capitale du sport f\u00e9minin",
        *SRC_NMR_TO
    ),
    # === ENVIRONNEMENT ===
    ("environnement", "climat-adaptation", "mayer-rossignol"): (
        "Programme de v\u00e9g\u00e9talisation urbaine pour la transition \u00e9cologique ; r\u00e9duction des NOx (Rouen pass\u00e9e de 3e \u00e0 14e ville la plus pollu\u00e9e)",
        *SRC_NMR_TO
    ),
    ("environnement", "alimentation-durable", "mayer-rossignol"): (
        "D\u00e9veloppement du bio sur ordonnance et alimentation saine dans les cantines municipales",
        *SRC_NMR_SAN
    ),

    # ===================== CARON (Horizons) =====================
    # === SECURITE ===
    ("securite", "police-municipale", "caron"): (
        "Augmentation des effectifs de police municipale de 72 \u00e0 100 agents d'ici 2030, \u00e9quipement avec des armes modernes et dissuasives",
        *SRC_CAR_FB
    ),
    ("securite", "videoprotection", "caron"): (
        "Quadruplement des cam\u00e9ras de vid\u00e9osurveillance : de 125 \u00e0 480 cam\u00e9ras d'ici la fin du mandat",
        *SRC_CAR_FB
    ),
    ("securite", "prevention-mediation", "caron"): (
        "R\u00e9tablissement de l'\u00e9clairage public la nuit et police de proximit\u00e9 ax\u00e9e sur la pr\u00e9vention",
        *SRC_CAR_FB
    ),
    # === SANTE ===
    ("sante", "centres-sante", "caron"): (
        "Cr\u00e9ation de centres de sant\u00e9 dans tous les quartiers pour lutter contre les d\u00e9serts m\u00e9dicaux",
        *SRC_CAR_FB
    ),
    # === TRANSPORTS ===
    ("transports", "stationnement", "caron"): (
        "Gratuit\u00e9 du stationnement pendant la pause d\u00e9jeuner",
        *SRC_CAR_FB
    ),
    ("transports", "transports-en-commun", "caron"): (
        "Cr\u00e9ation de navettes \u00e9cologiques de proximit\u00e9 \u00e0 la demande en centre-ville pour les personnes \u00e2g\u00e9es et les travailleurs de nuit",
        *SRC_CAR_FB
    ),

    # ===================== DA SILVA (LFI) =====================
    # === LOGEMENT ===
    ("logement", "encadrement-loyers", "da-silva"): (
        "Encadrement des loyers \u00e0 Rouen pour lutter contre l'explosion des prix",
        *SRC_DS_FB
    ),
    # === EDUCATION ===
    ("education", "cantines-fournitures", "da-silva"): (
        "Cantines scolaires gratuites, bio et locales pour tous ; gratuit\u00e9 compl\u00e8te de l'\u00e9cole (fournitures, sorties)",
        *SRC_DS_FB
    ),
    # === SANTE ===
    ("sante", "centres-sante", "da-silva"): (
        "Cr\u00e9ation de deux centres municipaux de sant\u00e9 (rive gauche et rive droite) avec m\u00e9decins salari\u00e9s sans d\u00e9passement d'honoraires, espace sant\u00e9 jeunes et consultations gratuites",
        *SRC_DS_FB
    ),
    # === TRANSPORTS ===
    ("transports", "tarifs-gratuite", "da-silva"): (
        "Gratuit\u00e9 des transports en commun pour les moins de 26 ans",
        *SRC_DS_FB
    ),
    # === DEMOCRATIE ===
    ("democratie", "budget-participatif", "da-silva"): (
        "Instauration d'un RIC municipal (r\u00e9f\u00e9rendum d'initiative citoyenne) pour les Rouennais",
        *SRC_DS_FB
    ),
    # === SOLIDARITE ===
    ("solidarite", "pouvoir-achat", "da-silva"): (
        "Gratuit\u00e9 des 15 premiers m\u00e8tres cubes d'eau pour all\u00e9ger les factures des Rouennais",
        *SRC_DS_FB
    ),

    # ===================== HOUDAN (RN) =====================
    # === SECURITE ===
    ("securite", "police-municipale", "houdan"): (
        "Faire de Rouen la ville la plus s\u00fbre de France d'ici 2032 : renforcement massif de la s\u00e9curit\u00e9",
        *SRC_HOU_JDD
    ),
    # === ECONOMIE ===
    ("economie", "attractivite", "houdan"): (
        "Restaurer l'ordre dans les finances de la ville et relancer l'attractivit\u00e9 \u00e9conomique",
        *SRC_HOU_FB
    ),

    # ===================== MAZIER (Reconqu\u00eate) =====================
    # === SECURITE ===
    ("securite", "police-municipale", "mazier"): (
        "R\u00e9gler les probl\u00e8mes d'ins\u00e9curit\u00e9 \u00e0 Rouen, priorit\u00e9 absolue du programme",
        *SRC_MAZ_TO
    ),
    # === ECONOMIE ===
    ("economie", "commerce-local", "mazier"): (
        "Relancer l'activit\u00e9 \u00e9conomique des commer\u00e7ants rouennais et restaurer la propret\u00e9 de la ville",
        *SRC_MAZ_TO
    ),

    # ===================== RENAULD (NPA-R) =====================
    # === LOGEMENT ===
    ("logement", "logements-vacants", "renauld"): (
        "R\u00e9quisition des logements vacants pour les sans-abri et les migrants priv\u00e9s de logement",
        *SRC_REN_TO
    ),
    # === SOLIDARITE ===
    ("solidarite", "pouvoir-achat", "renauld"): (
        "D\u00e9fense des int\u00e9r\u00eats des travailleurs et des jeunes face aux actionnaires ; prise de pouvoir par les travailleurs",
        *SRC_REN_NPA
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
    qid = f'"{cand_id}"' if '-' in cand_id else cand_id
    if key not in PROPS: return f"{sp}{qid}: null"
    texte, source, source_url = PROPS[key]
    return '\n'.join([f'{sp}{qid}: {{', f'{sp}  texte: "{escape_js(texte)}",', f'{sp}  source: "{escape_js(source)}",', f'{sp}  sourceUrl: "{escape_js(source_url)}"', f'{sp}}}'])

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
