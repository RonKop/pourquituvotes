#!/usr/bin/env python3
"""
Migration vers la grille universelle de 12 cat\u00e9gories / 44 sous-th\u00e8mes communs.
=====================================================================================
Lit js/app.js, applique le mapping et produit js/app_migrated.js.
Produit un rapport de comptages avant/apr\u00e8s.

Ex\u00e9cuter depuis la racine du projet :
    python -X utf8 scripts/migrate_structure.py
"""

import re
import os
import sys
import json
import copy

APPJS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "js", "app.js")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "js", "app_migrated.js")

# ============================================================
# GRILLE UNIVERSELLE : 12 cat\u00e9gories, 44 sous-th\u00e8mes communs
# ============================================================
# Ordre fixe pour le radar
CATEGORIES_UNIVERSELLES = [
    {
        "id": "securite",
        "nom": "S\\u00E9curit\\u00E9 & Pr\\u00E9vention",
        "sousThemesCommuns": [
            ("police-municipale", "Police municipale"),
            ("videoprotection", "Vid\\u00E9oprotection"),
            ("prevention-mediation", "Pr\\u00E9vention & M\\u00E9diation"),
            ("violences-femmes", "Violences faites aux femmes"),
        ]
    },
    {
        "id": "transports",
        "nom": "Transports & Mobilit\\u00E9",
        "sousThemesCommuns": [
            ("transports-en-commun", "Transports en commun"),
            ("velo-mobilites-douces", "V\\u00E9lo & Mobilit\\u00E9s douces"),
            ("pietons-circulation", "Pi\\u00E9tons & Circulation"),
            ("stationnement", "Stationnement"),
            ("tarifs-gratuite", "Tarifs & Gratuit\\u00E9"),
        ]
    },
    {
        "id": "logement",
        "nom": "Logement",
        "sousThemesCommuns": [
            ("logement-social", "Logement social"),
            ("logements-vacants", "Logements vacants"),
            ("encadrement-loyers", "Encadrement des loyers"),
            ("acces-logement", "Acc\\u00E8s au logement"),
        ]
    },
    {
        "id": "education",
        "nom": "\\u00C9ducation & Jeunesse",
        "sousThemesCommuns": [
            ("petite-enfance", "Petite enfance"),
            ("ecoles-renovation", "\\u00C9coles & R\\u00E9novation"),
            ("cantines-fournitures", "Cantines & Fournitures"),
            ("periscolaire-loisirs", "P\\u00E9riscolaire & Loisirs"),
            ("jeunesse", "Jeunesse"),
        ]
    },
    {
        "id": "environnement",
        "nom": "Environnement & Transition \\u00E9cologique",
        "sousThemesCommuns": [
            ("espaces-verts", "Espaces verts"),
            ("proprete-dechets", "Propret\\u00E9 & D\\u00E9chets"),
            ("climat-adaptation", "Climat & Adaptation"),
            ("renovation-energetique", "R\\u00E9novation \\u00E9nerg\\u00E9tique"),
            ("alimentation-durable", "Alimentation durable"),
        ]
    },
    {
        "id": "sante",
        "nom": "Sant\\u00E9 & Acc\\u00E8s aux soins",
        "sousThemesCommuns": [
            ("centres-sante", "Centres de sant\\u00E9"),
            ("prevention-sante", "Pr\\u00E9vention sant\\u00E9"),
            ("seniors", "Seniors"),
        ]
    },
    {
        "id": "democratie",
        "nom": "D\\u00E9mocratie & Vie citoyenne",
        "sousThemesCommuns": [
            ("budget-participatif", "Budget participatif"),
            ("transparence", "Transparence"),
            ("vie-associative", "Vie associative"),
            ("services-publics", "Services publics"),
        ]
    },
    {
        "id": "economie",
        "nom": "\\u00C9conomie & Emploi",
        "sousThemesCommuns": [
            ("commerce-local", "Commerce local"),
            ("emploi-insertion", "Emploi & Insertion"),
            ("attractivite", "Attractivit\\u00E9"),
        ]
    },
    {
        "id": "culture",
        "nom": "Culture & Patrimoine",
        "sousThemesCommuns": [
            ("equipements-culturels", "\\u00C9quipements culturels"),
            ("evenements-creation", "\\u00C9v\\u00E9nements & Cr\\u00E9ation"),
        ]
    },
    {
        "id": "sport",
        "nom": "Sport & Loisirs",
        "sousThemesCommuns": [
            ("equipements-sportifs", "\\u00C9quipements sportifs"),
            ("sport-pour-tous", "Sport pour tous"),
        ]
    },
    {
        "id": "urbanisme",
        "nom": "Urbanisme & Cadre de vie",
        "sousThemesCommuns": [
            ("amenagement-urbain", "Am\\u00E9nagement urbain"),
            ("accessibilite", "Accessibilit\\u00E9"),
            ("quartiers-prioritaires", "Quartiers prioritaires"),
        ]
    },
    {
        "id": "solidarite",
        "nom": "Solidarit\\u00E9 & \\u00C9galit\\u00E9",
        "sousThemesCommuns": [
            ("aide-sociale", "Aide sociale"),
            ("egalite-discriminations", "\\u00C9galit\\u00E9 & Discriminations"),
            ("pouvoir-achat", "Pouvoir d\\u2019achat"),
        ]
    },
]

# ============================================================
# MAPPING : ancien sous-th\u00e8me -> (nouvelle cat\u00e9gorie, nouveau sous-th\u00e8me)
# ============================================================
# Format: (old_election_prefix, old_cat_id, old_st_id) -> (new_cat_id, new_st_id)
# Si old_st_id est None, c'est pour le format flat (Clermont)
# Le pr\u00e9fixe est la ville pour d\u00e9sambiguer les IDs identiques entre villes

MAPPING = {
    # ======================
    # BORDEAUX
    # ======================
    # amenagement
    ("bordeaux", "amenagement", "quartiers-de-vie"): ("urbanisme", "amenagement-urbain"),
    ("bordeaux", "amenagement", "projet-urbain-lac"): ("urbanisme", "amenagement-urbain"),
    ("bordeaux", "amenagement", "proprete-bordeaux"): ("environnement", "proprete-dechets"),
    # transports
    ("bordeaux", "transports", "mobilites-douces"): ("transports", "velo-mobilites-douces"),
    ("bordeaux", "transports", "tarifs-gratuite"): ("transports", "tarifs-gratuite"),
    # logement
    ("bordeaux", "logement", "logement-social"): ("logement", "logement-social"),
    # economie
    ("bordeaux", "economie", "commerce-local"): ("economie", "commerce-local"),
    ("bordeaux", "economie", "tarifs-municipaux"): ("solidarite", "pouvoir-achat"),
    # sante
    ("bordeaux", "sante", "structures-medicales"): ("sante", "centres-sante"),
    # education
    ("bordeaux", "education", "creches"): ("education", "petite-enfance"),
    ("bordeaux", "education", "ecoles"): ("education", "ecoles-renovation"),
    # culture
    ("bordeaux", "culture", "creation-artistique"): ("culture", "evenements-creation"),
    # solidarite
    ("bordeaux", "solidarite", "enfants-sans-abri"): ("solidarite", "aide-sociale"),
    # securite
    ("bordeaux", "securite", "police-mediation"): ("securite", "police-municipale"),

    # ======================
    # CLERMONT - sousThemes format
    # ======================
    # securite
    ("clermont", "securite", "police-effectifs"): ("securite", "police-municipale"),
    ("clermont", "securite", "videoprotection"): ("securite", "videoprotection"),
    ("clermont", "securite", "commissariats"): ("securite", "police-municipale"),
    ("clermont", "securite", "prevention-mediation"): ("securite", "prevention-mediation"),
    ("clermont", "securite", "securite-routiere"): ("transports", "pietons-circulation"),
    ("clermont", "securite", "narcotrafic"): ("securite", "police-municipale"),
    ("clermont", "securite", "eclairage-public"): ("securite", "prevention-mediation"),
    ("clermont", "securite", "brigades-specialisees"): ("securite", "police-municipale"),
    ("clermont", "securite", "proprete"): ("environnement", "proprete-dechets"),
    # transports
    ("clermont", "transports", "gratuite-tarifs"): ("transports", "tarifs-gratuite"),
    ("clermont", "transports", "velo-mobilites-douces"): ("transports", "velo-mobilites-douces"),
    ("clermont", "transports", "circulation-ztl"): ("transports", "pietons-circulation"),
    ("clermont", "transports", "stationnement"): ("transports", "stationnement"),
    # logement
    ("clermont", "logement", "acces-logement"): ("logement", "acces-logement"),
    ("clermont", "logement", "production-logements"): ("logement", "logement-social"),
    ("clermont", "logement", "lutte-vacance"): ("logement", "logements-vacants"),
    ("clermont", "logement", "politiques-attribution"): ("logement", "logement-social"),
    ("clermont", "logement", "urgence-sociale"): ("solidarite", "aide-sociale"),
    # sante
    ("clermont", "sante", "centres-sante"): ("sante", "centres-sante"),
    ("clermont", "sante", "sante-scolaire"): ("sante", "prevention-sante"),
    ("clermont", "sante", "seniors-accompagnement"): ("sante", "seniors"),

    # ======================
    # PARIS
    # ======================
    # logement
    ("paris", "logement", "logement-public"): ("logement", "logement-social"),
    ("paris", "logement", "logements-vacants"): ("logement", "logements-vacants"),
    ("paris", "logement", "encadrement-loyers"): ("logement", "encadrement-loyers"),
    ("paris", "logement", "assurance-habitation"): ("logement", "acces-logement"),
    ("paris", "logement", "parc-social"): ("logement", "logement-social"),
    # ecologie-pouvoir-achat
    ("paris", "ecologie-pouvoir-achat", "renovation-energetique"): ("environnement", "renovation-energetique"),
    ("paris", "ecologie-pouvoir-achat", "energie-renouvelable"): ("environnement", "renovation-energetique"),
    ("paris", "ecologie-pouvoir-achat", "pollution-bruit"): ("environnement", "climat-adaptation"),
    ("paris", "ecologie-pouvoir-achat", "alimentation"): ("environnement", "alimentation-durable"),
    ("paris", "ecologie-pouvoir-achat", "dechets-reparation"): ("environnement", "proprete-dechets"),
    ("paris", "ecologie-pouvoir-achat", "cooperative-velo"): ("transports", "velo-mobilites-douces"),
    # bouclier-social
    ("paris", "bouclier-social", "hebergement-urgence"): ("solidarite", "aide-sociale"),
    ("paris", "bouclier-social", "jeunesse-solidarite"): ("solidarite", "aide-sociale"),
    ("paris", "bouclier-social", "acces-droits"): ("democratie", "services-publics"),
    ("paris", "bouclier-social", "sante"): ("sante", "centres-sante"),
    ("paris", "bouclier-social", "sante-sexuelle-specifique"): ("sante", "prevention-sante"),
    # education-jeunesse
    ("paris", "education-jeunesse", "creches-petite-enfance"): ("education", "petite-enfance"),
    ("paris", "education-jeunesse", "ecole-publique"): ("education", "ecoles-renovation"),
    ("paris", "education-jeunesse", "handicap-scolaire"): ("education", "ecoles-renovation"),
    ("paris", "education-jeunesse", "cantine-fournitures"): ("education", "cantines-fournitures"),
    ("paris", "education-jeunesse", "renovation-ecoles"): ("education", "ecoles-renovation"),
    ("paris", "education-jeunesse", "periscolaire"): ("education", "periscolaire-loisirs"),
    ("paris", "education-jeunesse", "jeunesse"): ("education", "jeunesse"),
    # transports
    ("paris", "transports", "bus-express"): ("transports", "transports-en-commun"),
    ("paris", "transports", "metro"): ("transports", "transports-en-commun"),
    ("paris", "transports", "navettes-fluviales"): ("transports", "transports-en-commun"),
    ("paris", "transports", "velo"): ("transports", "velo-mobilites-douces"),
    ("paris", "transports", "pietons-circulation"): ("transports", "pietons-circulation"),
    ("paris", "transports", "logistique-urbaine"): ("transports", "pietons-circulation"),
    ("paris", "transports", "stationnement"): ("transports", "stationnement"),
    # environnement
    ("paris", "environnement", "arbres-vegetation"): ("environnement", "espaces-verts"),
    ("paris", "environnement", "baignades-seine"): ("environnement", "baignades-seine"),  # sp\u00e9cifique Paris
    ("paris", "environnement", "biodiversite"): ("environnement", "espaces-verts"),
    ("paris", "environnement", "peripherique"): ("urbanisme", "amenagement-urbain"),
    ("paris", "environnement", "proprete"): ("environnement", "proprete-dechets"),
    # securite
    ("paris", "securite", "police-municipale"): ("securite", "police-municipale"),
    ("paris", "securite", "eclairage-securite"): ("securite", "videoprotection"),
    ("paris", "securite", "violences-femmes"): ("securite", "violences-femmes"),
    ("paris", "securite", "prevention-mediation"): ("securite", "prevention-mediation"),
    # democratie
    ("paris", "democratie", "mairies-arrondissement"): ("democratie", "services-publics"),
    ("paris", "democratie", "budget-participatif"): ("democratie", "budget-participatif"),
    ("paris", "democratie", "vie-associative"): ("democratie", "vie-associative"),
    ("paris", "democratie", "train-vie-elus"): ("democratie", "transparence"),
    ("paris", "democratie", "gestion-effectifs"): ("democratie", "services-publics"),
    # culture-sport
    ("paris", "culture-sport", "musees-culture"): ("culture", "equipements-culturels"),
    ("paris", "culture-sport", "sport"): ("sport", "equipements-sportifs"),
    # egalite-droits
    ("paris", "egalite-droits", "ville-refuge"): ("solidarite", "aide-sociale"),
    ("paris", "egalite-droits", "lutte-discriminations"): ("solidarite", "egalite-discriminations"),
    ("paris", "egalite-droits", "accessibilite"): ("urbanisme", "accessibilite"),
    # grand-paris
    ("paris", "grand-paris", "gouvernance-metropolitaine"): ("democratie", "transparence"),
    ("paris", "grand-paris", "tarification-solidarite"): ("transports", "tarifs-gratuite"),
    ("paris", "grand-paris", "technologie-innovation"): ("economie", "attractivite"),
    ("paris", "grand-paris", "commerce-entrepreneurs"): ("economie", "commerce-local"),
    ("paris", "grand-paris", "ventes-patrimoine"): ("economie", "attractivite"),

    # ======================
    # LYON
    # ======================
    # securite
    ("lyon", "securite", "police-municipale"): ("securite", "police-municipale"),
    ("lyon", "securite", "brigade-anti-incivilites"): ("securite", "police-municipale"),
    ("lyon", "securite", "videosurveillance"): ("securite", "videoprotection"),
    ("lyon", "securite", "protection-femmes"): ("securite", "violences-femmes"),
    ("lyon", "securite", "prevention-mediation"): ("securite", "prevention-mediation"),
    # transports
    ("lyon", "transports", "transports-en-commun"): ("transports", "transports-en-commun"),
    ("lyon", "transports", "tunnel-circulation"): ("transports", "tunnel-circulation"),  # sp\u00e9cifique Lyon
    ("lyon", "transports", "stationnement"): ("transports", "stationnement"),
    # logement
    ("lyon", "logement", "logement-social-construction"): ("logement", "logement-social"),
    # environnement
    ("lyon", "environnement", "espaces-verts-parcs"): ("environnement", "espaces-verts"),
    ("lyon", "environnement", "adaptation-climatique"): ("environnement", "climat-adaptation"),
    ("lyon", "environnement", "environnement-animaux"): ("environnement", "protection-animale"),  # sp\u00e9cifique Lyon
    # education
    ("lyon", "education", "cantines-fournitures"): ("education", "cantines-fournitures"),
    ("lyon", "education", "loisirs-enfants"): ("education", "periscolaire-loisirs"),
    ("lyon", "education", "petite-enfance"): ("education", "petite-enfance"),
    ("lyon", "education", "creches-petite-enfance"): ("education", "petite-enfance"),
    # sante
    ("lyon", "sante", "centres-de-sante"): ("sante", "centres-sante"),
    ("lyon", "sante", "sante-acces"): ("sante", "centres-sante"),
    # economie
    ("lyon", "economie", "alimentation-solidaire"): ("environnement", "alimentation-durable"),
    ("lyon", "economie", "pouvoir-achat"): ("solidarite", "pouvoir-achat"),
    ("lyon", "economie", "alimentation"): ("environnement", "alimentation-durable"),
    # culture
    ("lyon", "culture", "equipements-culturels"): ("culture", "equipements-culturels"),
    ("lyon", "culture", "culture-projets"): ("culture", "evenements-creation"),
    # evenementiel
    ("lyon", "evenementiel", "jo-evenements"): ("sport", "sport-pour-tous"),
    # services-familles
    ("lyon", "services-familles", "horaires-atypiques"): ("democratie", "services-publics"),
    # democratie
    ("lyon", "democratie", "democratie-participative"): ("democratie", "budget-participatif"),

    # ======================
    # MARSEILLE
    # ======================
    # democratie
    ("marseille", "democratie", "participation-citoyenne"): ("democratie", "budget-participatif"),
    ("marseille", "democratie", "assemblee-citoyenne"): ("democratie", "budget-participatif"),
    ("marseille", "democratie", "transparence-elus"): ("democratie", "transparence"),
    ("marseille", "democratie", "referendums-locaux"): ("democratie", "budget-participatif"),
    # logement
    ("marseille", "logement", "construction-logements"): ("logement", "logement-social"),
    ("marseille", "logement", "logements-vacants"): ("logement", "logements-vacants"),
    ("marseille", "logement", "encadrement-loyers"): ("logement", "encadrement-loyers"),
    ("marseille", "logement", "habitat-alternatif"): ("logement", "acces-logement"),
    # securite
    ("marseille", "securite", "tranquillite-publique"): ("securite", "prevention-mediation"),
    ("marseille", "securite", "police-municipale"): ("securite", "police-municipale"),
    # education
    ("marseille", "education", "ecole-publique"): ("education", "ecoles-renovation"),
    ("marseille", "education", "cantines"): ("education", "cantines-fournitures"),
    # sante
    ("marseille", "sante", "acces-soins"): ("sante", "centres-sante"),
    # environnement
    ("marseille", "environnement", "planification-ecologique"): ("environnement", "climat-adaptation"),
    ("marseille", "environnement", "adaptation-climatique"): ("environnement", "climat-adaptation"),
    ("marseille", "environnement", "nature-en-ville"): ("environnement", "espaces-verts"),
    ("marseille", "environnement", "observatoire-sante-environnement"): ("sante", "prevention-sante"),
    ("marseille", "environnement", "proprete"): ("environnement", "proprete-dechets"),
    # transports
    ("marseille", "transports", "transports-gratuits"): ("transports", "tarifs-gratuite"),
    # services-publics
    ("marseille", "services-publics", "gestion-publique"): ("democratie", "services-publics"),
    # culture-sport
    ("marseille", "culture-sport", "sport-pour-tous"): ("sport", "sport-pour-tous"),
    # solidarite
    ("marseille", "solidarite", "aide-sociale"): ("solidarite", "aide-sociale"),
    # economie
    ("marseille", "economie", "developpement-economique"): ("economie", "attractivite"),
    # tourisme-loisirs
    ("marseille", "tourisme-loisirs", "tourisme"): ("economie", "attractivite"),
    # egalite
    ("marseille", "egalite", "observatoire-discriminations"): ("solidarite", "egalite-discriminations"),
    ("marseille", "egalite", "egalite-femmes-hommes"): ("solidarite", "egalite-discriminations"),
    ("marseille", "egalite", "lutte-racisme"): ("solidarite", "egalite-discriminations"),
    ("marseille", "egalite", "lutte-antisemitisme"): ("solidarite", "egalite-discriminations"),
}

# ======================
# CLERMONT flat-format mapping
# Chaque proposition (candidatId, texte_start) -> (new_cat_id, new_st_id)
# We map by category + candidat + sequential index
# ======================
# We'll handle flat format by mapping each proposition based on keyword analysis
CLERMONT_FLAT_MAPPING = {
    # education flat propositions -> new targets
    "education": [
        # bianchi: "Deux nouvelles cr\u00e8ches" -> petite-enfance
        ("bianchi", 0, "education", "petite-enfance"),
        # bianchi: "Augmentation des places en centres de loisirs" -> periscolaire-loisirs
        ("bianchi", 1, "education", "periscolaire-loisirs"),
        # bianchi: "kit de fournitures scolaires" -> cantines-fournitures
        ("bianchi", 2, "education", "cantines-fournitures"),
        # bianchi: "ATSEM par classe maternelle" -> ecoles-renovation
        ("bianchi", 3, "education", "ecoles-renovation"),
        # bianchi: "Nouvelle \u00e9cole maternelle" -> ecoles-renovation
        ("bianchi", 4, "education", "ecoles-renovation"),
        # bianchi: "Alternative v\u00e9g\u00e9tarienne restauration scolaire" -> cantines-fournitures
        ("bianchi", 5, "education", "cantines-fournitures"),
        # bianchi: "go\u00fbter sain" -> cantines-fournitures
        ("bianchi", 6, "education", "cantines-fournitures"),
        # bianchi: "guichet jeunes" -> jeunesse
        ("bianchi", 7, "education", "jeunesse"),
        # bianchi: "v\u00e9g\u00e9talisation des cours d'\u00e9cole" -> ecoles-renovation
        ("bianchi", 8, "education", "ecoles-renovation"),
        # maximi: "Gratuit\u00e9 cantines" -> cantines-fournitures
        ("maximi", 9, "education", "cantines-fournitures"),
        # maximi: "Cantines bio et gratuites" -> cantines-fournitures
        ("maximi", 10, "education", "cantines-fournitures"),
        # bony: "Services publics familles, petite enfance" -> petite-enfance
        ("bony", 11, "education", "petite-enfance"),
    ],
    # environnement flat propositions
    "environnement": [
        # bianchi: "Plan fra\u00eecheur" -> climat-adaptation
        ("bianchi", 0, "environnement", "climat-adaptation"),
        # bianchi: "Ouverture du parc de la Muraille" -> espaces-verts
        ("bianchi", 1, "environnement", "espaces-verts"),
        # bianchi: "V\u00e9g\u00e9talisation des places" -> espaces-verts
        ("bianchi", 2, "environnement", "espaces-verts"),
        # bianchi: "\u00e9clairage 100% LED" -> renovation-energetique
        ("bianchi", 3, "environnement", "renovation-energetique"),
        # bianchi: "R\u00e9novation \u00e9nerg\u00e9tique des b\u00e2timents" -> renovation-energetique
        ("bianchi", 4, "environnement", "renovation-energetique"),
        # bianchi: "\u00e9nergies renouvelables, photovolta\u00efque" -> renovation-energetique
        ("bianchi", 5, "environnement", "renovation-energetique"),
        # bianchi: "propri\u00e9taires priv\u00e9s r\u00e9novation \u00e9nerg\u00e9tique" -> renovation-energetique
        ("bianchi", 6, "environnement", "renovation-energetique"),
        # bianchi: "Protection eau potable" -> climat-adaptation
        ("bianchi", 7, "environnement", "climat-adaptation"),
        # bianchi: "Pr\u00e9vention risques naturels" -> climat-adaptation
        ("bianchi", 8, "environnement", "climat-adaptation"),
        # bianchi: "ceinture mara\u00eech\u00e8re" -> alimentation-durable
        ("bianchi", 9, "environnement", "alimentation-durable"),
        # bianchi: "caisse alimentaire locale" -> alimentation-durable
        ("bianchi", 10, "environnement", "alimentation-durable"),
        # bony: "Moins de b\u00e9ton et plus de vert" -> espaces-verts
        ("bony", 11, "environnement", "espaces-verts"),
        # bony: "politique pragmatique \u00e9cologie" -> climat-adaptation
        ("bony", 12, "environnement", "climat-adaptation"),
    ],
    # culture flat propositions
    "culture": [
        # bianchi: "R\u00e9novation Op\u00e9ra et Coop\u00e9rative de Mai" -> equipements-culturels
        ("bianchi", 0, "culture", "equipements-culturels"),
        # bianchi: "Cit\u00e9 du court et Lieu-dit" -> equipements-culturels
        ("bianchi", 1, "culture", "equipements-culturels"),
        # bianchi: "Soutien \u00e9quipes artistiques" -> evenements-creation
        ("bianchi", 2, "culture", "evenements-creation"),
        # bianchi: "mille formes art 0-6 ans" -> evenements-creation
        ("bianchi", 3, "culture", "evenements-creation"),
        # bianchi: "Programmation culturelle publique" -> evenements-creation
        ("bianchi", 4, "culture", "evenements-creation"),
        # darbois: "mus\u00e9e Blaise Pascal" -> equipements-culturels
        ("darbois", 5, "culture", "equipements-culturels"),
        # bony: "Valorisation patrimoine" -> evenements-creation
        ("bony", 6, "culture", "evenements-creation"),
    ],
    # sport flat propositions
    "sport": [
        # bianchi: "Clermont bouge sport-sant\u00e9" -> sport-pour-tous
        ("bianchi", 0, "sport", "sport-pour-tous"),
        # bianchi: "gymnase dimanche" -> equipements-sportifs
        ("bianchi", 1, "sport", "equipements-sportifs"),
        # bianchi: "gymnase Montpied et pumptrack" -> equipements-sportifs
        ("bianchi", 2, "sport", "equipements-sportifs"),
        # bianchi: "ch\u00e8que premi\u00e8re licence" -> sport-pour-tous
        ("bianchi", 3, "sport", "sport-pour-tous"),
        # bianchi: "patinoire Papadakis-Cizeron" -> equipements-sportifs
        ("bianchi", 4, "sport", "equipements-sportifs"),
        # bianchi: "village de loisirs gratuit" -> sport-pour-tous
        ("bianchi", 5, "sport", "sport-pour-tous"),
    ],
    # economie flat propositions
    "economie": [
        # bianchi: "office du commerce et artisanat" -> commerce-local
        ("bianchi", 0, "economie", "commerce-local"),
        # bianchi: "boutiques \u00e0 l'essai" -> commerce-local
        ("bianchi", 1, "economie", "commerce-local"),
        # bianchi: "march\u00e9s alimentaires Halle Saint-Pierre" -> commerce-local
        ("bianchi", 2, "economie", "commerce-local"),
        # bianchi: "fonds m\u00e9tropolitain ESS" -> emploi-insertion
        ("bianchi", 3, "economie", "emploi-insertion"),
        # bianchi: "150 hectares foncier \u00e9conomique" -> attractivite
        ("bianchi", 4, "economie", "attractivite"),
        # bianchi: "Maison insertion et emploi" -> emploi-insertion
        ("bianchi", 5, "economie", "emploi-insertion"),
        # bianchi: "fili\u00e8res r\u00e9emploi" -> emploi-insertion
        ("bianchi", 6, "economie", "emploi-insertion"),
        # darbois: "technocentres Charade" -> attractivite
        ("darbois", 7, "economie", "attractivite"),
        # maximi: "TPE PME" -> emploi-insertion
        ("maximi", 8, "economie", "emploi-insertion"),
        # bony: "relance attractivit\u00e9" -> attractivite
        ("bony", 9, "economie", "attractivite"),
        # bony: "environnement \u00e9conomique commerce" -> commerce-local
        ("bony", 10, "economie", "commerce-local"),
        # bony: "office municipal du commerce" -> commerce-local
        ("bony", 11, "economie", "commerce-local"),
        # bony: "application commerces" -> commerce-local
        ("bony", 12, "economie", "commerce-local"),
    ],
    # urbanisme flat propositions
    "urbanisme": [
        # bianchi: "renouvellement urbain Vergnes, Gauthi\u00e8re, Saint-Jacques" -> quartiers-prioritaires
        ("bianchi", 0, "urbanisme", "quartiers-prioritaires"),
        # bianchi: "Plan Montferrand" -> amenagement-urbain
        ("bianchi", 1, "urbanisme", "amenagement-urbain"),
        # bianchi: "place Delille" -> amenagement-urbain
        ("bianchi", 2, "urbanisme", "amenagement-urbain"),
        # bianchi: "Maison de quartier Croix-Neyrat" -> quartiers-prioritaires
        ("bianchi", 3, "urbanisme", "quartiers-prioritaires"),
        # bianchi: "accessibilit\u00e9 handicap" -> accessibilite
        ("bianchi", 4, "urbanisme", "accessibilite"),
        # bony: "espaces publics propret\u00e9 accessibilit\u00e9" -> amenagement-urbain
        ("bony", 5, "urbanisme", "amenagement-urbain"),
        # bony: "personnes \u00e0 mobilit\u00e9 r\u00e9duite" -> accessibilite
        ("bony", 6, "urbanisme", "accessibilite"),
        # darbois: "Renommer Avenue Union Sovi\u00e9tique" -> amenagement-urbain
        ("darbois", 7, "urbanisme", "amenagement-urbain"),
    ],
    # democratie flat propositions
    "democratie": [
        # bianchi: "Conseil des a\u00een\u00e9s" -> budget-participatif
        ("bianchi", 0, "democratie", "budget-participatif"),
        # bianchi: "\u00e9tats g\u00e9n\u00e9raux quartiers" -> budget-participatif
        ("bianchi", 1, "democratie", "budget-participatif"),
        # bianchi: "budget participatif" -> budget-participatif
        ("bianchi", 2, "democratie", "budget-participatif"),
        # bianchi: "Convention IA" -> transparence
        ("bianchi", 3, "democratie", "transparence"),
        # bianchi: "Clermontois engag\u00e9" -> vie-associative
        ("bianchi", 4, "democratie", "vie-associative"),
        # bianchi: "Accueil centralis\u00e9 d\u00e9marches" -> services-publics
        ("bianchi", 5, "democratie", "services-publics"),
        # bianchi: "Maison des associations" -> vie-associative
        ("bianchi", 6, "democratie", "vie-associative"),
        # bianchi: "Conseil de la nuit" -> vie-associative
        ("bianchi", 7, "democratie", "vie-associative"),
        # darbois: "finances ville surendettement" -> transparence
        ("darbois", 8, "democratie", "transparence"),
        # bony: "consultations populaires" -> budget-participatif
        ("bony", 9, "democratie", "budget-participatif"),
        # bony: "R\u00e9duction train de vie" -> transparence
        ("bony", 10, "democratie", "transparence"),
        # bony: "Tourner le dos grands projets" -> transparence
        ("bony", 11, "democratie", "transparence"),
    ],
}


def lire_fichier():
    with open(APPJS_PATH, "r", encoding="utf-8") as f:
        return f.read()


def extraire_donnees_js(contenu):
    """
    Parse le bloc ELECTIONS du fichier app.js.
    Retourne un dict des \u00e9lections avec leur structure brute.
    On va travailler au niveau logique, pas au niveau texte.
    """
    # On utilise une approche : extraire la portion JSON-like de ELECTIONS
    # et la parser manuellement via regex
    elections = {}

    # Trouver chaque \u00e9lection
    election_starts = list(re.finditer(r'"([a-z]+-2026)":\s*\{', contenu))

    for i, m in enumerate(election_starts):
        eid = m.group(1)
        ville_prefix = eid.replace("-2026", "")
        start = m.start()

        # D\u00e9terminer la fin (d\u00e9but du suivant ou fin de ELECTIONS)
        if i + 1 < len(election_starts):
            end = election_starts[i + 1].start()
        else:
            # Trouver }; apr\u00e8s le dernier
            end = contenu.find("};", start)
            if end == -1:
                end = len(contenu)

        bloc = contenu[start:end]

        # Extraire candidats
        candidats = []
        cand_pattern = r'\{\s*id:\s*"([^"]+)",\s*nom:\s*"([^"]+)",\s*liste:\s*"([^"]+)",\s*programmeUrl:\s*"([^"]+)",\s*programmeComplet:\s*(true|false),\s*programmePdfPath:\s*("([^"]*)"|(null))\s*\}'
        for cm in re.finditer(cand_pattern, bloc):
            candidats.append({
                "id": cm.group(1),
                "nom": cm.group(2),
                "liste": cm.group(3),
                "programmeUrl": cm.group(4),
                "programmeComplet": cm.group(5) == "true",
                "programmePdfPath": cm.group(7) if cm.group(7) else None,
            })

        candidat_ids = [c["id"] for c in candidats]

        # Extraire les cat\u00e9gories
        categories = []
        # Find categories: [ ... ]
        cat_list_match = re.search(r'categories:\s*\[', bloc)
        if not cat_list_match:
            continue

        cat_start = cat_list_match.end()

        # Parse chaque cat\u00e9gorie dans le bloc
        # Cat\u00e9gories = { id: "...", nom: "...", sousThemes: [...] } ou { id: "...", nom: "...", propositions: [...] }
        cat_pattern = r'\{\s*\n\s*id:\s*"([^"]+)",\s*\n\s*nom:\s*"([^"]+)",\s*\n\s*(sousThemes|propositions):\s*\['
        cat_matches = list(re.finditer(cat_pattern, bloc[cat_start:]))

        for ci, cm in enumerate(cat_matches):
            cat_id = cm.group(1)
            cat_nom = cm.group(2)
            format_type = cm.group(3)

            cat_data = {"id": cat_id, "nom": cat_nom, "format": format_type}

            content_start = cat_start + cm.end()

            # D\u00e9terminer la fin du contenu de cette cat\u00e9gorie
            if ci + 1 < len(cat_matches):
                content_end = cat_start + cat_matches[ci + 1].start()
            else:
                content_end = len(bloc)

            content_bloc = bloc[content_start:content_end]

            if format_type == "sousThemes":
                # Parse les sous-th\u00e8mes
                sous_themes = []
                st_pattern = r'id:\s*"([^"]+)",\s*\n\s*nom:\s*"([^"]+)",\s*\n\s*propositions:\s*\{'
                st_matches = list(re.finditer(st_pattern, content_bloc))

                for si, sm in enumerate(st_matches):
                    st_id = sm.group(1)
                    st_nom = sm.group(2)

                    # Extraire le bloc propositions
                    prop_start = sm.end()
                    depth = 1
                    pos = prop_start
                    while pos < len(content_bloc) and depth > 0:
                        if content_bloc[pos] == '{':
                            depth += 1
                        elif content_bloc[pos] == '}':
                            depth -= 1
                        pos += 1
                    prop_bloc = content_bloc[prop_start:pos-1]

                    # Parser les propositions
                    propositions = {}
                    for cid in candidat_ids:
                        cid_escaped = re.escape(cid)
                        # Chercher cid: { texte: "..." } ou cid: null ou "cid": { texte: "..." } ou "cid": null
                        pattern = rf'(?:"{cid_escaped}"|\b{cid_escaped})\s*:\s*(\{{[^}}]*\}}|null)'
                        pm = re.search(pattern, prop_bloc, re.DOTALL)
                        if pm:
                            val = pm.group(1).strip()
                            if val == "null":
                                propositions[cid] = None
                            else:
                                # Extraire texte, source, sourceUrl
                                texte_m = re.search(r'texte:\s*"((?:[^"\\]|\\.)*)",\s*source:', val, re.DOTALL)
                                source_m = re.search(r',\s*source:\s*"((?:[^"\\]|\\.)*)",\s*sourceUrl:', val)
                                sourceUrl_m = re.search(r'sourceUrl:\s*"((?:[^"\\]|\\.)*)"', val)
                                if texte_m:
                                    propositions[cid] = {
                                        "texte": texte_m.group(1),
                                        "source": source_m.group(1) if source_m else "",
                                        "sourceUrl": sourceUrl_m.group(1) if sourceUrl_m else "",
                                    }
                                else:
                                    propositions[cid] = None
                        else:
                            propositions[cid] = None

                    sous_themes.append({
                        "id": st_id,
                        "nom": st_nom,
                        "propositions": propositions,
                    })

                cat_data["sousThemes"] = sous_themes

            elif format_type == "propositions":
                # Format flat (Clermont)
                flat_props = []
                fp_pattern = r'\{\s*candidatId:\s*"([^"]+)",\s*texte:\s*"((?:[^"\\]|\\.)*)",\s*source:\s*"((?:[^"\\]|\\.)*)",\s*sourceUrl:\s*"((?:[^"\\]|\\.)*)"\s*\}'
                for fp in re.finditer(fp_pattern, content_bloc):
                    flat_props.append({
                        "candidatId": fp.group(1),
                        "texte": fp.group(2),
                        "source": fp.group(3),
                        "sourceUrl": fp.group(4),
                    })
                cat_data["propositions"] = flat_props

            categories.append(cat_data)

        # Extraire ville et dateVote
        ville_m = re.search(r'ville:\s*"([^"]+)"', bloc)
        date_m = re.search(r'dateVote:\s*"([^"]+)"', bloc)

        elections[eid] = {
            "ville": ville_m.group(1) if ville_m else "",
            "ville_prefix": ville_prefix,
            "annee": 2026,
            "dateVote": date_m.group(1) if date_m else "",
            "candidats": candidats,
            "candidat_ids": candidat_ids,
            "categories": categories,
        }

    return elections


def compter_propositions_avant(elections):
    """Compte les propositions non-null par candidat avant migration."""
    stats = {}
    for eid, edata in elections.items():
        ville = edata["ville"]
        stats[ville] = {cid: 0 for cid in edata["candidat_ids"]}
        for cat in edata["categories"]:
            if cat["format"] == "sousThemes":
                for st in cat["sousThemes"]:
                    for cid, prop in st["propositions"].items():
                        if prop is not None:
                            stats[ville][cid] = stats[ville].get(cid, 0) + 1
            elif cat["format"] == "propositions":
                for fp in cat["propositions"]:
                    cid = fp["candidatId"]
                    stats[ville][cid] = stats[ville].get(cid, 0) + 1
    return stats


def migrer_election(eid, edata):
    """
    Migre une \u00e9lection vers la grille universelle.
    Retourne la liste des nouvelles cat\u00e9gories.
    """
    ville_prefix = edata["ville_prefix"]
    candidat_ids = edata["candidat_ids"]

    # Cr\u00e9er la structure vide pour les 12 cat\u00e9gories
    # Dict: new_cat_id -> { sous_themes: { new_st_id -> { candidat_id -> [propositions] } } }
    new_structure = {}
    for cat_def in CATEGORIES_UNIVERSELLES:
        new_cat_id = cat_def["id"]
        new_structure[new_cat_id] = {}
        for st_id, st_nom in cat_def["sousThemesCommuns"]:
            new_structure[new_cat_id][st_id] = {cid: [] for cid in candidat_ids}

    # Set pour tracker les sous-th\u00e8mes sp\u00e9cifiques ajout\u00e9s
    specific_st_noms = {}  # (cat_id, st_id) -> nom

    # Migrer chaque cat\u00e9gorie
    unmapped = []

    for cat in edata["categories"]:
        old_cat_id = cat["id"]

        if cat["format"] == "sousThemes":
            for st in cat["sousThemes"]:
                old_st_id = st["id"]
                key = (ville_prefix, old_cat_id, old_st_id)

                if key in MAPPING:
                    new_cat_id, new_st_id = MAPPING[key]

                    # V\u00e9rifier si c'est un sous-th\u00e8me sp\u00e9cifique (pas dans les communs)
                    common_ids = set()
                    for cat_def in CATEGORIES_UNIVERSELLES:
                        if cat_def["id"] == new_cat_id:
                            common_ids = {s[0] for s in cat_def["sousThemesCommuns"]}
                            break

                    if new_st_id not in common_ids:
                        # Sous-th\u00e8me sp\u00e9cifique \u00e0 cette ville
                        if new_cat_id not in new_structure:
                            new_structure[new_cat_id] = {}
                        if new_st_id not in new_structure[new_cat_id]:
                            new_structure[new_cat_id][new_st_id] = {cid: [] for cid in candidat_ids}
                        specific_st_noms[(new_cat_id, new_st_id)] = st["nom"]

                    # V\u00e9rifier que la cible existe
                    if new_st_id not in new_structure.get(new_cat_id, {}):
                        new_structure.setdefault(new_cat_id, {})[new_st_id] = {cid: [] for cid in candidat_ids}

                    # Ajouter les propositions
                    for cid, prop in st["propositions"].items():
                        if prop is not None and cid in new_structure[new_cat_id][new_st_id]:
                            new_structure[new_cat_id][new_st_id][cid].append(prop)
                else:
                    unmapped.append(f"  [{edata['ville']}] {old_cat_id}/{old_st_id}")

        elif cat["format"] == "propositions":
            # Format flat (Clermont)
            if ville_prefix == "clermont" and old_cat_id in CLERMONT_FLAT_MAPPING:
                mapping_list = CLERMONT_FLAT_MAPPING[old_cat_id]
                for idx, fp in enumerate(cat["propositions"]):
                    # Trouver le mapping pour cette proposition
                    mapped = False
                    for m_cid, m_idx, m_cat, m_st in mapping_list:
                        if m_idx == idx:
                            if m_cat not in new_structure:
                                new_structure[m_cat] = {}
                            if m_st not in new_structure[m_cat]:
                                new_structure[m_cat][m_st] = {cid: [] for cid in candidat_ids}
                            new_structure[m_cat][m_st][fp["candidatId"]].append({
                                "texte": fp["texte"],
                                "source": fp["source"],
                                "sourceUrl": fp["sourceUrl"],
                            })
                            mapped = True
                            break
                    if not mapped:
                        unmapped.append(f"  [{edata['ville']}] {old_cat_id} proposition #{idx} ({fp['candidatId']}): {fp['texte'][:50]}...")
            else:
                unmapped.append(f"  [{edata['ville']}] cat\u00e9gorie flat non g\u00e9r\u00e9e: {old_cat_id}")

    if unmapped:
        print("ATTENTION - Propositions non mapp\u00e9es :")
        for u in unmapped:
            print(u)

    # Construire la sortie
    result_categories = []
    for cat_def in CATEGORIES_UNIVERSELLES:
        new_cat_id = cat_def["id"]
        if new_cat_id not in new_structure:
            continue

        sous_themes = []
        # D'abord les sous-th\u00e8mes communs
        for st_id, st_nom in cat_def["sousThemesCommuns"]:
            if st_id in new_structure[new_cat_id]:
                props = {}
                for cid in candidat_ids:
                    prop_list = new_structure[new_cat_id][st_id].get(cid, [])
                    if len(prop_list) == 0:
                        props[cid] = None
                    elif len(prop_list) == 1:
                        props[cid] = prop_list[0]
                    else:
                        # Fusionner les textes
                        merged_texte = ". ".join(p["texte"] for p in prop_list)
                        # Fusionner les sources
                        sources = list(dict.fromkeys(p["source"] for p in prop_list))
                        merged_source = " | ".join(sources)
                        source_urls = list(dict.fromkeys(p["sourceUrl"] for p in prop_list))
                        merged_url = source_urls[0] if source_urls else ""
                        props[cid] = {
                            "texte": merged_texte,
                            "source": merged_source,
                            "sourceUrl": merged_url,
                        }
                sous_themes.append({
                    "id": st_id,
                    "nom": st_nom,
                    "propositions": props,
                })

        # Ensuite les sous-th\u00e8mes sp\u00e9cifiques
        for st_id, st_data in new_structure[new_cat_id].items():
            # V\u00e9rifier que ce n'est pas d\u00e9j\u00e0 un commun
            is_common = any(s[0] == st_id for s in cat_def["sousThemesCommuns"])
            if not is_common:
                st_nom = specific_st_noms.get((new_cat_id, st_id), st_id)
                props = {}
                for cid in candidat_ids:
                    prop_list = st_data.get(cid, [])
                    if len(prop_list) == 0:
                        props[cid] = None
                    elif len(prop_list) == 1:
                        props[cid] = prop_list[0]
                    else:
                        merged_texte = ". ".join(p["texte"] for p in prop_list)
                        sources = list(dict.fromkeys(p["source"] for p in prop_list))
                        merged_source = " | ".join(sources)
                        source_urls = list(dict.fromkeys(p["sourceUrl"] for p in prop_list))
                        merged_url = source_urls[0] if source_urls else ""
                        props[cid] = {
                            "texte": merged_texte,
                            "source": merged_source,
                            "sourceUrl": merged_url,
                        }
                sous_themes.append({
                    "id": st_id,
                    "nom": st_nom,
                    "propositions": props,
                })

        result_categories.append({
            "id": new_cat_id,
            "nom": cat_def["nom"],
            "sousThemes": sous_themes,
        })

    return result_categories


def generer_js_proposition(prop, indent):
    """G\u00e9n\u00e8re le code JS pour une proposition."""
    if prop is None:
        return "null"
    return (
        f'{{\n'
        f'{indent}  texte: "{prop["texte"]}",\n'
        f'{indent}  source: "{prop["source"]}",\n'
        f'{indent}  sourceUrl: "{prop["sourceUrl"]}"\n'
        f'{indent}}}'
    )


def generer_js_elections(elections_migrees):
    """G\u00e9n\u00e8re le code JS pour le bloc ELECTIONS migr\u00e9."""
    lines = []
    lines.append("  var ELECTIONS = {")

    election_items = list(elections_migrees.items())
    for ei, (eid, edata) in enumerate(election_items):
        lines.append(f'    "{eid}": {{')
        lines.append(f'      ville: "{edata["ville"]}",')
        lines.append(f'      annee: {edata["annee"]},')
        lines.append(f'      type: "\\u00C9lections municipales",')
        lines.append(f'      dateVote: "{edata["dateVote"]}",')

        # Candidats
        lines.append('      candidats: [')
        for ci, c in enumerate(edata["candidats"]):
            pdf = f'"{c["programmePdfPath"]}"' if c["programmePdfPath"] else "null"
            pc = "true" if c["programmeComplet"] else "false"
            comma = "," if ci < len(edata["candidats"]) - 1 else ""
            lines.append(
                f'        {{ id: "{c["id"]}", nom: "{c["nom"]}", liste: "{c["liste"]}", '
                f'programmeUrl: "{c["programmeUrl"]}", programmeComplet: {pc}, '
                f'programmePdfPath: {pdf} }}{comma}'
            )
        lines.append('      ],')

        # Cat\u00e9gories
        lines.append('      categories: [')
        for cati, cat in enumerate(edata["new_categories"]):
            lines.append('        {')
            lines.append(f'          id: "{cat["id"]}",')
            lines.append(f'          nom: "{cat["nom"]}",')
            lines.append('          sousThemes: [')

            for sti, st in enumerate(cat["sousThemes"]):
                lines.append('            {')
                lines.append(f'              id: "{st["id"]}",')
                lines.append(f'              nom: "{st["nom"]}",')
                lines.append('              propositions: {')

                candidat_ids = edata["candidat_ids"]
                for pi, cid in enumerate(candidat_ids):
                    prop = st["propositions"].get(cid)
                    # Pour les IDs avec tirets, il faut les mettre entre guillemets
                    needs_quotes = "-" in cid
                    key = f'"{cid}"' if needs_quotes else cid
                    val = generer_js_proposition(prop, "                ")
                    comma = "," if pi < len(candidat_ids) - 1 else ""
                    if prop is None:
                        lines.append(f'                {key}: null{comma}')
                    else:
                        lines.append(f'                {key}: {val}{comma}')

                st_comma = "," if sti < len(cat["sousThemes"]) - 1 else ""
                lines.append('              }')
                lines.append(f'            }}{st_comma}')

            cat_comma = "," if cati < len(edata["new_categories"]) - 1 else ""
            lines.append('          ]')
            lines.append(f'        }}{cat_comma}')

        lines.append('      ]')
        el_comma = "," if ei < len(election_items) - 1 else ""
        lines.append(f'    }}{el_comma}')

    lines.append("  };")
    return "\n".join(lines)


def compter_propositions_apres(elections_migrees):
    """Compte les propositions apr\u00e8s migration."""
    stats = {}
    for eid, edata in elections_migrees.items():
        ville = edata["ville"]
        stats[ville] = {cid: 0 for cid in edata["candidat_ids"]}
        for cat in edata["new_categories"]:
            for st in cat["sousThemes"]:
                for cid, prop in st["propositions"].items():
                    if prop is not None:
                        stats[ville][cid] = stats[ville].get(cid, 0) + 1
    return stats


def main():
    print("=" * 60)
    print("  MIGRATION VERS GRILLE UNIVERSELLE")
    print("=" * 60)
    print()

    # 1. Lire et parser
    print("1. Lecture de app.js...")
    contenu = lire_fichier()
    elections = extraire_donnees_js(contenu)
    print(f"   {len(elections)} \u00e9lections trouv\u00e9es")
    for eid, edata in elections.items():
        print(f"   - {edata['ville']} : {len(edata['candidat_ids'])} candidats, {len(edata['categories'])} cat\u00e9gories")
    print()

    # 2. Compter avant
    print("2. Comptage AVANT migration :")
    stats_avant = compter_propositions_avant(elections)
    for ville in sorted(stats_avant):
        for cid in sorted(stats_avant[ville]):
            print(f"   {ville}/{cid}: {stats_avant[ville][cid]}")
    print()

    # 3. Migrer
    print("3. Migration en cours...")
    for eid, edata in elections.items():
        new_cats = migrer_election(eid, edata)
        edata["new_categories"] = new_cats
        print(f"   {edata['ville']} : {len(new_cats)} cat\u00e9gories (12 universelles)")
    print()

    # 4. Compter apr\u00e8s
    print("4. Comptage APR\u00c8S migration :")
    stats_apres = compter_propositions_apres(elections)
    for ville in sorted(stats_apres):
        for cid in sorted(stats_apres[ville]):
            print(f"   {ville}/{cid}: {stats_apres[ville][cid]}")
    print()

    # 5. Comparer
    print("5. Comparaison AVANT / APR\u00c8S :")
    all_ok = True
    for ville in sorted(stats_avant):
        for cid in sorted(stats_avant[ville]):
            avant = stats_avant[ville][cid]
            apres = stats_apres.get(ville, {}).get(cid, 0)
            status = "OK" if avant == apres else f"DIFF ({avant} -> {apres})"
            if avant != apres:
                all_ok = False
            # Note: apr\u00e8s fusion de sous-th\u00e8mes, le nombre peut diminuer
            # car 2 anciens sous-th\u00e8mes -> 1 nouveau avec texte concat\u00e9n\u00e9
            # C'est normal et attendu. On ne doit PAS perdre de CANDIDATS.
            print(f"   {ville}/{cid}: {avant} -> {apres} [{status}]")

    if not all_ok:
        print()
        print("   NOTE: Les diff\u00e9rences sont attendues quand des sous-th\u00e8mes")
        print("   fusionnent (2 propositions d'un m\u00eame candidat concat\u00e9n\u00e9es en 1).")
        print("   V\u00e9rifier qu'aucune proposition n'a \u00e9t\u00e9 perdue.")
    print()

    # 6. G\u00e9n\u00e9rer le fichier de sortie
    print("6. G\u00e9n\u00e9ration de app_migrated.js...")

    # Extraire la partie avant ELECTIONS et la partie apr\u00e8s
    elections_start = contenu.find("var ELECTIONS = {")
    if elections_start == -1:
        print("   ERREUR: Impossible de trouver 'var ELECTIONS = {'")
        return 1

    # Trouver la fin de ELECTIONS : };  suivi de // ===
    # On cherche la premi\u00e8re ligne qui commence par "  // ===" apr\u00e8s ELECTIONS
    elections_end_pattern = re.search(r'\n  // === \u00C9l\u00E9ments DOM ===', contenu)
    if not elections_end_pattern:
        # Fallback: chercher };
        elections_end_pattern = re.search(r'\n  };\n', contenu[elections_start + 100:])
        if elections_end_pattern:
            elections_end = elections_start + 100 + elections_end_pattern.end()
        else:
            print("   ERREUR: Impossible de trouver la fin de ELECTIONS")
            return 1
    else:
        elections_end = elections_end_pattern.start()

    before = contenu[:elections_start]
    after = contenu[elections_end:]

    new_elections_js = generer_js_elections(elections)

    output = before + new_elections_js + "\n\n" + after

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"   \u00c9crit dans {OUTPUT_PATH}")
    print(f"   Taille : {len(output)} caract\u00e8res")
    print()

    print("=" * 60)
    print("  MIGRATION TERMIN\u00c9E")
    print("  V\u00e9rifier le fichier g\u00e9n\u00e9r\u00e9, puis remplacer app.js")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
