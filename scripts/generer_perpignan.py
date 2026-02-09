#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Perpignan dans app.js."""
import re

VILLE_ID = "perpignan"
VILLE_NOM = "Perpignan"
VILLE_CP = "66000"
ELECTION_ID = "perpignan-2026"

CANDIDATS = [
    {"id": "aliot", "nom": "Louis Aliot", "liste": "Continuons ensemble (RN, sortant)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "nougayrede", "nom": "Bruno Nougayr\u00e8de", "liste": "100% Perpignan (LR-UDI-Horizons-MoDem-Renaissance)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "langevine", "nom": "Agn\u00e8s Langevine", "liste": "Perpignan la Catalane (Place Publique-Centre)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "blanc", "nom": "Mathias Blanc", "liste": "Perpignan Autrement (PS-PCF-PRG)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "idrac", "nom": "Micka\u00ebl Idrac", "liste": "Perpignan, Changez d'air ! (LFI-EELV-G.s)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    {"id": "ripoull", "nom": "Clotilde Ripoull", "liste": "Libres (sans \u00e9tiquette)", "programmeUrl": "https://www.clotilderipoull.fr/", "programmeComplet": False, "programmePdfPath": None},
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
SRC_ALIOT_FB = ("France Bleu Roussillon, janvier 2026", "https://www.francebleu.fr/")
SRC_ALIOT_F3 = ("France 3 Occitanie, 2025", "https://france3-regions.franceinfo.fr/")
SRC_ALIOT_MIP = ("Made in Perpignan, 2025", "https://madeinperpignan.com/")
SRC_NOUGAYREDE_MIP = ("Made in Perpignan, d\u00e9cembre 2025", "https://madeinperpignan.com/")
SRC_NOUGAYREDE_FB = ("France Bleu Roussillon, 2026", "https://www.francebleu.fr/")
SRC_LANGEVINE_FB = ("France Bleu Roussillon, janvier 2026", "https://www.francebleu.fr/")
SRC_LANGEVINE_MIP = ("Made in Perpignan, janvier 2026", "https://madeinperpignan.com/")
SRC_BLANC_FB = ("France Bleu Roussillon, 2026", "https://www.francebleu.fr/")
SRC_BLANC_MIP = ("Made in Perpignan, septembre 2025", "https://madeinperpignan.com/")
SRC_IDRAC_FB = ("France Bleu Roussillon, novembre 2025", "https://www.francebleu.fr/")
SRC_IDRAC_MIP = ("Made in Perpignan, 2025", "https://madeinperpignan.com/")

PROPS = {
    # ===================== SECURITE =====================
    ("securite", "police-municipale", "aliot"): (
        "Porter \u00e0 250 policiers municipaux d'ici la fin du prochain mandat (50 de plus qu'aujourd'hui), pr\u00e9sence 24h/24",
        *SRC_ALIOT_FB
    ),
    ("securite", "police-municipale", "nougayrede"): (
        "Cr\u00e9er des postes mobiles de police municipale dans les quartiers pour lutter contre le harc\u00e8lement de rue et le trafic de drogue",
        *SRC_NOUGAYREDE_MIP
    ),
    ("securite", "police-municipale", "blanc"): (
        "Red\u00e9ployer la police municipale vers une v\u00e9ritable police de proximit\u00e9 au c\u0153ur des quartiers",
        *SRC_BLANC_FB
    ),
    ("securite", "police-municipale", "idrac"): (
        "Retour d'une v\u00e9ritable police de proximit\u00e9, renforcement des \u00e9ducateurs de rue et politique de pr\u00e9vention transparente",
        *SRC_IDRAC_FB
    ),
    ("securite", "videoprotection", "aliot"): (
        "Installer 200 cam\u00e9ras de vid\u00e9osurveillance suppl\u00e9mentaires dans les quartiers",
        *SRC_ALIOT_FB
    ),
    ("securite", "prevention-mediation", "blanc"): (
        "Mettre en place un programme \u00e9ducatif de pr\u00e9vention des drogues et incivilit\u00e9s, de l'\u00e9cole primaire au lyc\u00e9e",
        *SRC_BLANC_FB
    ),

    # ===================== TRANSPORTS =====================
    ("transports", "transports-en-commun", "blanc"): (
        "D\u00e9velopper des lignes de bus \u00e0 haut niveau de service avec fr\u00e9quences renforc\u00e9es (70% des habitants d\u00e9pendent de la voiture)",
        *SRC_BLANC_FB
    ),
    ("transports", "transports-en-commun", "aliot"): (
        "Cr\u00e9er une nouvelle entr\u00e9e nord de la ville et un parking relais pour d\u00e9sengorger le centre",
        *SRC_ALIOT_MIP
    ),
    ("transports", "stationnement", "nougayrede"): (
        "Gratuit\u00e9 de la premi\u00e8re demi-heure de stationnement en centre-ville pour relancer le commerce",
        *SRC_NOUGAYREDE_MIP
    ),

    # ===================== LOGEMENT =====================
    ("logement", "acces-logement", "nougayrede"): (
        "Politique de retour des propri\u00e9taires occupants en centre-ville pour recr\u00e9er de la mixit\u00e9 sociale",
        *SRC_NOUGAYREDE_MIP
    ),

    # ===================== EDUCATION =====================
    ("education", "ecoles-renovation", "langevine"): (
        "R\u00e9nover les \u00e9coles pour les adapter aux hausses de temp\u00e9ratures, cr\u00e9er des \u00ab oasis \u00bb v\u00e9g\u00e9talis\u00e9es autour et dans les \u00e9coles",
        *SRC_LANGEVINE_MIP
    ),
    ("education", "ecoles-renovation", "blanc"): (
        "R\u00e9nover massivement les \u00e9coles pour les rendre vivables en \u00e9t\u00e9 comme en hiver",
        *SRC_BLANC_FB
    ),
    ("education", "cantines-fournitures", "langevine"): (
        "Petit-d\u00e9jeuner gratuit pour chaque \u00e9l\u00e8ve, kit de fournitures offert \u00e0 l'entr\u00e9e en CP d\u00e8s 2027",
        *SRC_LANGEVINE_MIP
    ),
    ("education", "cantines-fournitures", "idrac"): (
        "Cantines scolaires gratuites et bio, \u00e9cole ouverte d\u00e8s 7h",
        *SRC_IDRAC_FB
    ),
    ("education", "petite-enfance", "idrac"): (
        "Cr\u00e9ation de places de cr\u00e8che suppl\u00e9mentaires pour r\u00e9pondre \u00e0 la demande des familles",
        *SRC_IDRAC_FB
    ),
    ("education", "jeunesse", "langevine"): (
        "Ouverture des \u00e9coles d\u00e8s 7h, propositions cibl\u00e9es pour la jeunesse (mobilit\u00e9, emploi, loisirs)",
        *SRC_LANGEVINE_MIP
    ),

    # ===================== ENVIRONNEMENT =====================
    ("environnement", "climat-adaptation", "langevine"): (
        "Cr\u00e9er des \u00ab oasis \u00bb de fra\u00eecheur pour rafra\u00eechir la ville lors des canicules, d\u00e9simperh\u00e9abiliser les cours d'\u00e9cole et les espaces urbains",
        *SRC_LANGEVINE_FB
    ),
    ("environnement", "climat-adaptation", "blanc"): (
        "Cr\u00e9er une cellule municipale \u00ab climat \u00bb r\u00e9unissant urbanistes, hydrologues, botanistes, citoyens et agents municipaux",
        *SRC_BLANC_FB
    ),
    ("environnement", "espaces-verts", "blanc"): (
        "Planter massivement des arbres dans toute la ville pour lutter contre les \u00eelots de chaleur",
        *SRC_BLANC_FB
    ),
    ("environnement", "climat-adaptation", "nougayrede"): (
        "Plan ombre inspir\u00e9 de l'Andalousie pour faire face aux pics de chaleur",
        *SRC_NOUGAYREDE_MIP
    ),
    ("environnement", "renovation-energetique", "aliot"): (
        "Projet d'usine de dessalement de l'eau de mer estim\u00e9 \u00e0 40 millions d'euros pour s\u00e9curiser l'approvisionnement en eau",
        *SRC_ALIOT_F3
    ),
    ("environnement", "alimentation-durable", "blanc"): (
        "Fin du foie gras et 50% de v\u00e9g\u00e9talisation des buffets municipaux, campagne massive de st\u00e9rilisation des chats errants",
        *SRC_BLANC_MIP
    ),

    # ===================== SANTE =====================
    ("sante", "centres-sante", "blanc"): (
        "Recruter 15 m\u00e9decins pour garantir un suivi m\u00e9dical \u00e0 chacun (15 000 Perpignanais sans m\u00e9decin traitant)",
        *SRC_BLANC_FB
    ),
    ("sante", "centres-sante", "aliot"): (
        "Lutter contre la p\u00e9nurie de m\u00e9decins, priorit\u00e9 du prochain mandat",
        *SRC_ALIOT_F3
    ),
    ("sante", "centres-sante", "nougayrede"): (
        "R\u00e9cup\u00e9rer une facult\u00e9 de m\u00e9decine \u00e0 Perpignan pour former et fixer les m\u00e9decins localement",
        *SRC_NOUGAYREDE_FB
    ),

    # ===================== DEMOCRATIE =====================
    ("democratie", "budget-participatif", "blanc"): (
        "Cr\u00e9er des assembl\u00e9es citoyennes et populaires dans les quartiers avec pouvoir d\u00e9cisionnel et budget d\u00e9di\u00e9 de 4 millions d'euros/an (5% du budget municipal)",
        *SRC_BLANC_FB
    ),
    ("democratie", "services-publics", "blanc"): (
        "Redonner toute leur place aux maisons de quartier comme espaces de services publics, de solidarit\u00e9 et de citoyennet\u00e9",
        *SRC_BLANC_FB
    ),
    ("democratie", "transparence", "idrac"): (
        "D\u00e9mocratie participative et politique de pr\u00e9vention transparente dans tous les quartiers",
        *SRC_IDRAC_FB
    ),

    # ===================== ECONOMIE =====================
    ("economie", "commerce-local", "nougayrede"): (
        "Revitaliser le centre-ville historique : redonner vie et fiert\u00e9 au c\u0153ur de ville, tant sur le plan patrimonial que commercial",
        *SRC_NOUGAYREDE_MIP
    ),
    ("economie", "commerce-local", "aliot"): (
        "Cr\u00e9er une zone franche en centre-ville pour attirer les commerces et entreprises",
        *SRC_ALIOT_MIP
    ),
    ("economie", "attractivite", "nougayrede"): (
        "Am\u00e9liorer les conditions d'accueil des entreprises : ressources humaines, foncier, acc\u00e8s au capital et co\u00fbt de l'\u00e9nergie",
        *SRC_NOUGAYREDE_FB
    ),
    ("economie", "emploi-insertion", "idrac"): (
        "Relance \u00e9conomique par la consommation populaire, cr\u00e9ation d'un poste d'adjoint \u00ab ville productive \u00bb interlocuteur direct des artisans",
        *SRC_IDRAC_MIP
    ),
    ("economie", "attractivite", "langevine"): (
        "Mobiliser 1 000 places de stationnement en p\u00e9riode commerciale et relancer les grands \u00e9v\u00e9nements urbains pour l'attractivit\u00e9",
        *SRC_LANGEVINE_MIP
    ),

    # ===================== CULTURE =====================
    ("culture", "evenements-creation", "langevine"): (
        "Redonner une place importante aux f\u00eates catalanes, publier des manuels scolaires en catalan, personnel scolaire catalanophone dans les \u00e9coles immersives",
        *SRC_LANGEVINE_FB
    ),

    # ===================== SPORT =====================
    ("sport", "sport-pour-tous", "idrac"): (
        "Premi\u00e8re licence sportive gratuite pour les enfants",
        *SRC_IDRAC_FB
    ),

    # ===================== URBANISME =====================
    ("urbanisme", "amenagement-urbain", "idrac"): (
        "Changer radicalement l'urbanisme : stopper la b\u00e9tonisation et privil\u00e9gier un d\u00e9veloppement durable",
        *SRC_IDRAC_MIP
    ),
    ("urbanisme", "quartiers-prioritaires", "blanc"): (
        "R\u00e9investir les quartiers : redonner vie aux maisons de quartier comme lieux de proximit\u00e9 et d'animation",
        *SRC_BLANC_FB
    ),

    # ===================== SOLIDARITE =====================
    ("solidarite", "pouvoir-achat", "idrac"): (
        "Am\u00e9liorer le pouvoir d'achat des Perpignanais en priorit\u00e9, via la consommation locale",
        *SRC_IDRAC_MIP
    ),
    ("solidarite", "aide-sociale", "nougayrede"): (
        "Plan de lutte contre la pr\u00e9carit\u00e9, ne pas augmenter les imp\u00f4ts et envisager une baisse si les bases fiscales progressent",
        *SRC_NOUGAYREDE_MIP
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
