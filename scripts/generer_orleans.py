#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère et insère Orléans dans app.js."""
import re

VILLE_ID = "orleans"
VILLE_NOM = "Orl\u00e9ans"
VILLE_CP = "45000"
ELECTION_ID = "orleans-2026"

CANDIDATS = [
    {"id": "grouard", "nom": "Serge Grouard", "liste": "Ici, c'est Orl\u00e9ans (DVD)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "janvier", "nom": "Caroline Janvier", "liste": "Vivons Orl\u00e9ans (centre)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "chapuis", "nom": "Baptiste Chapuis", "liste": "Rassembler Orl\u00e9ans (PS/PCF/G\u00e9n\u00e9ration.s/Place publique/PRG)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "grand", "nom": "Jean-Philippe Grand", "liste": "OSE - Orl\u00e9ans Solidaire et \u00c9cologique (EELV)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "pele", "nom": "Valentin Pel\u00e9", "liste": "Orl\u00e9ans en commun (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "rabault", "nom": "Tiffanie Rabault", "liste": "Orl\u00e9ans, nouvel \u00e9lan (RN)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "meyer", "nom": "Gr\u00e9gory Meyer", "liste": "Notre ville plus que jamais vivante (Horizons)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "lamarque", "nom": "Isabelle Lamarque", "liste": "\u00c0 la reconqu\u00eate d'Orl\u00e9ans (Reconqu\u00eate !)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "megdoud", "nom": "Farida Megdoud", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
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
SRC_GROUARD_FB = ("France Bleu Orl\u00e9ans, janvier 2026", "https://www.francebleu.fr/infos/politique/municipales-2026-le-maire-d-orleans-serge-grouard-brigue-bien-un-nouveau-mandat-3755390")
SRC_GROUARD_F3 = ("France 3 Centre, janvier 2026", "https://france3-regions.franceinfo.fr/centre-val-de-loire/loiret/orleans/municipales-2026-sans-surprise-serge-grouard-candidat-a-sa-reelection-a-orleans-3278198.html")
SRC_CHAPUIS_FB = ("France Bleu Orl\u00e9ans, f\u00e9vrier 2026", "https://www.francebleu.fr/infos/politique/municipales-2026-on-veut-rassembler-orleans-et-ses-habitants-le-socialiste-baptiste-chapuis-devoile-son-programme-9406795")
SRC_GRAND_FB = ("France Bleu Orl\u00e9ans, janvier 2026", "https://www.francebleu.fr/infos/politique/elections-municipales-a-orleans-ose-presente-son-programme-2923431")
SRC_GRAND_MC = ("Mag'Centre, f\u00e9vrier 2026", "https://www.magcentre.fr/360154-la-feuille-de-route-dose-pour-une-nouvelle-orleans/")
SRC_PELE_MC = ("Mag'Centre, janvier 2026", "https://www.magcentre.fr/349158-valentin-pele-tete-de-liste-lfi-aux-municipales-a-orleans-nous-serons-en-tete-a-lissue-du-1er-tour/")
SRC_PELE_FB = ("France Bleu Orl\u00e9ans, octobre 2025", "https://www.francebleu.fr/infos/politique/municipales-a-orleans-l-insoumis-valentin-pele-designe-comme-tete-de-liste-pour-orleans-en-commun-7346263")
SRC_JANVIER_FB = ("France Bleu Orl\u00e9ans, janvier 2026", "https://www.francebleu.fr/infos/politique/je-suis-la-seule-a-avoir-battu-serge-grouard-caroline-janvier-officialise-sa-candidature-aux-municipales-a-orleans-6202892")
SRC_RABAULT_FB = ("France Bleu Orl\u00e9ans, novembre 2025", "https://www.francebleu.fr/infos/politique/orleans-le-rn-choisit-tiffanie-rabault-ex-candidate-aux-legislatives-pour-mener-la-liste-des-municipales-en-2026-3264954")
SRC_MEYER_FB = ("France Bleu Orl\u00e9ans, septembre 2025", "https://www.francebleu.fr/infos/politique/oui-je-suis-pret-a-devenir-le-prochain-maire-d-orleans-l-avocat-gregory-meyer-candidat-pour-mars-2026-6599583")

PROPS = {
    # === SECURITE ===
    ("securite", "police-municipale", "pele"): (
        "D\u00e9sarmement de la police municipale pour les armes l\u00e9tales",
        *SRC_PELE_MC
    ),
    ("securite", "prevention-mediation", "chapuis"): (
        "Cr\u00e9ation d'un r\u00e9seau de \u00ab safe spaces \u00bb dans les bars, commerces et \u00e9coles pour lutter contre le harc\u00e8lement de rue",
        *SRC_CHAPUIS_FB
    ),
    ("securite", "prevention-mediation", "rabault"): (
        "Renforcement de la s\u00e9curit\u00e9 dans les rues d'Orl\u00e9ans, priorit\u00e9 \u00e0 la tranquillit\u00e9 publique",
        *SRC_RABAULT_FB
    ),
    ("securite", "prevention-mediation", "grouard"): (
        "Poursuite de la politique de proximit\u00e9 : propret\u00e9, s\u00e9curit\u00e9 et restauration du patrimoine",
        *SRC_GROUARD_FB
    ),

    # === TRANSPORTS ===
    ("transports", "tarifs-gratuite", "chapuis"): (
        "Gratuit\u00e9 progressive des transports en commun : d'abord les week-ends, puis en semaine pour les jeunes et les seniors",
        *SRC_CHAPUIS_FB
    ),
    ("transports", "tarifs-gratuite", "pele"): (
        "Gratuit\u00e9 totale des transports en commun et cr\u00e9ation d'une r\u00e9gie publique des transports",
        *SRC_PELE_MC
    ),
    ("transports", "transports-en-commun", "pele"): (
        "Construction d'une troisi\u00e8me ligne de tramway",
        *SRC_PELE_MC
    ),
    ("transports", "velo-mobilites-douces", "grand"): (
        "Cr\u00e9ation de vraies v\u00e9lo-routes s\u00e9curis\u00e9es dans toute la ville",
        *SRC_GRAND_FB
    ),
    ("transports", "tarifs-gratuite", "grand"): (
        "Tram gratuit le samedi et deux heures de stationnement gratuit pour les clients des commerces le samedi",
        *SRC_GRAND_FB
    ),
    ("transports", "transports-en-commun", "janvier"): (
        "Am\u00e9lioration de la mobilit\u00e9 au quotidien, avec un r\u00e9seau de transports plus performant",
        *SRC_JANVIER_FB
    ),

    # === LOGEMENT ===
    ("logement", "logement-social", "chapuis"): (
        "Augmentation du parc de logements sociaux dans la ville",
        *SRC_CHAPUIS_FB
    ),

    # === EDUCATION ===
    ("education", "petite-enfance", "chapuis"): (
        "Priorit\u00e9 \u00e0 l'enfance : cr\u00e9ation de places suppl\u00e9mentaires en cr\u00e8che et d\u00e9marchandisation du secteur",
        *SRC_CHAPUIS_FB
    ),
    ("education", "cantines-fournitures", "chapuis"): (
        "Fournitures scolaires gratuites (crayons, cahiers, gommes) pour environ 5 000 \u00e9l\u00e8ves, co\u00fbt estim\u00e9 200 000 \u00e0 300 000 \u20ac",
        *SRC_CHAPUIS_FB
    ),
    ("education", "cantines-fournitures", "grand"): (
        "Remunicipalisation des cantines scolaires et passage \u00e0 40 puis 50 % de produits bio et locaux",
        *SRC_GRAND_MC
    ),
    ("education", "cantines-fournitures", "pele"): (
        "Gratuit\u00e9 des cantines scolaires",
        *SRC_PELE_MC
    ),
    ("education", "ecoles-renovation", "grand"): (
        "V\u00e9g\u00e9talisation de toutes les cours d'\u00e9cole",
        *SRC_GRAND_MC
    ),
    ("education", "ecoles-renovation", "chapuis"): (
        "V\u00e9g\u00e9talisation de toutes les cours d'\u00e9cole et s\u00e9curisation des rues scolaires pour le v\u00e9lo",
        *SRC_CHAPUIS_FB
    ),

    # === ENVIRONNEMENT ===
    ("environnement", "climat-adaptation", "janvier"): (
        "Transition \u00e9cologique et lutte contre le d\u00e9r\u00e8glement climatique et ses effets sur la ville",
        *SRC_JANVIER_FB
    ),

    # === SANTE ===
    ("sante", "centres-sante", "pele"): (
        "Cr\u00e9ation d'un r\u00e9seau de centres de sant\u00e9 municipaux",
        *SRC_PELE_MC
    ),
    ("sante", "centres-sante", "janvier"): (
        "Am\u00e9lioration de l'acc\u00e8s aux soins pour tous les Orl\u00e9anais",
        *SRC_JANVIER_FB
    ),

    # === DEMOCRATIE ===
    ("democratie", "transparence", "pele"): (
        "Organisation de votations citoyennes et transparence des d\u00e9penses publiques",
        *SRC_PELE_MC
    ),
    ("democratie", "transparence", "chapuis"): (
        "Audit des projets existants d\u00e8s la prise de fonction",
        *SRC_CHAPUIS_FB
    ),
    ("democratie", "vie-associative", "chapuis"): (
        "Pactes financiers de 3 \u00e0 4 ans avec les associations pour leur donner stabilit\u00e9 et visibilit\u00e9",
        *SRC_CHAPUIS_FB
    ),
    ("democratie", "transparence", "meyer"): (
        "Changement de gouvernance : projets construits avec \u00e9lus, habitants et services municipaux, et non impos\u00e9s d'en haut",
        *SRC_MEYER_FB
    ),
    ("democratie", "services-publics", "pele"): (
        "Cr\u00e9ation d'un service public municipal des pompes fun\u00e8bres",
        *SRC_PELE_MC
    ),

    # === ECONOMIE ===
    ("economie", "commerce-local", "grand"): (
        "Remplacement du projet Halles Ch\u00e2telet par des \u00ab march\u00e9s populaires \u00bb et r\u00e9vision compl\u00e8te du projet de requalification des Mails",
        *SRC_GRAND_MC
    ),
    ("economie", "commerce-local", "chapuis"): (
        "Nouvelles Halles Ch\u00e2telet pour valoriser la gastronomie locale et l'artisanat",
        *SRC_CHAPUIS_FB
    ),
    ("economie", "attractivite", "grouard"): (
        "Grands projets : restructuration de la place d'Arc, Cit\u00e9 Jeanne d'Arc \u00e0 Charbonni\u00e8re, mus\u00e9e des Beaux-Arts r\u00e9nov\u00e9",
        *SRC_GROUARD_F3
    ),
    ("economie", "attractivite", "janvier"): (
        "R\u00e9industrialisation de la m\u00e9tropole et d\u00e9veloppement du tourisme",
        *SRC_JANVIER_FB
    ),
    ("economie", "attractivite", "rabault"): (
        "D\u00e9veloppement \u00e9conomique d'Orl\u00e9ans et politique inclusive",
        *SRC_RABAULT_FB
    ),

    # === CULTURE ===
    ("culture", "equipements-culturels", "chapuis"): (
        "Cr\u00e9ation d'un centre international Jeanne d'Arc et d'une Cit\u00e9 du num\u00e9rique dans l'ancien coll\u00e8ge Jean Rostand",
        *SRC_CHAPUIS_FB
    ),
    ("culture", "equipements-culturels", "grouard"): (
        "Cit\u00e9 Jeanne d'Arc \u00e0 Charbonni\u00e8re et r\u00e9novation du mus\u00e9e des Beaux-Arts",
        *SRC_GROUARD_F3
    ),

    # === SPORT ===
    ("sport", "equipements-sportifs", "chapuis"): (
        "R\u00e9novation du stade de La Source pour l'USO et le RCO",
        *SRC_CHAPUIS_FB
    ),

    # === URBANISME ===
    ("urbanisme", "amenagement-urbain", "grouard"): (
        "La \u00ab beaut\u00e9 comme projet politique \u00bb : r\u00e9novation des fa\u00e7ades, restauration des \u00e9difices historiques et des \u00e9glises",
        *SRC_GROUARD_F3
    ),

    # === SOLIDARITE ===
    ("solidarite", "pouvoir-achat", "pele"): (
        "Gratuit\u00e9 des premiers m\u00e8tres cubes d'eau pour tous les m\u00e9nages",
        *SRC_PELE_MC
    ),
    ("solidarite", "aide-sociale", "pele"): (
        "Cr\u00e9ation d'une r\u00e9gie mara\u00eech\u00e8re municipale pour l'acc\u00e8s \u00e0 une alimentation de qualit\u00e9",
        *SRC_PELE_MC
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
