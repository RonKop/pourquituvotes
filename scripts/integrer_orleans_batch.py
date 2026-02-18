#!/usr/bin/env python3
"""
Intègre les programmes de Baptiste Chapuis et Jean-Philippe Grand
dans data/elections/orleans-2026.json.

Chapuis : 155 propositions (Rassembler Orléans, PS/PCF/Génération.s/Place publique/PRG)
Grand : ~200 pages de propositions (OSE - Orléans Solidaire et Écologique, EELV)
"""

import json
import sys
import io
import os

# Encodage UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORLEANS_JSON = os.path.join(BASE_DIR, "data", "elections", "orleans-2026.json")

# ============================================================
# SOURCES
# ============================================================
CHAPUIS_SOURCE_FB = "France Bleu Orléans, février 2026"
CHAPUIS_URL_FB = "https://www.francebleu.fr/infos/politique/municipales-2026-on-veut-rassembler-orleans-et-ses-habitants-le-socialiste-baptiste-chapuis-devoile-son-programme-9406795"

CHAPUIS_SOURCE_MC = "Mag'Centre, février 2026"
CHAPUIS_URL_MC = "https://www.magcentre.fr/359793-municipales-rassembler-orleans-devoile-sa-vision-de-la-ville-de-demain/"

GRAND_SOURCE_FB = "France Bleu Orléans, février 2026"
GRAND_URL_FB = "https://www.francebleu.fr/infos/politique/elections-municipales-a-orleans-ose-presente-son-programme-2923431"

GRAND_SOURCE_MC = "Mag'Centre, février 2026"
GRAND_URL_MC = "https://www.magcentre.fr/360154-la-feuille-de-route-dose-pour-une-nouvelle-orleans/"

GRAND_SOURCE_OSE = "OSE 2026, programme officiel"
GRAND_URL_OSE_SECURITE = "https://orleans-solidaire-ecologique.fr/notre-programme-securite/"
GRAND_URL_OSE_SANTE = "https://orleans-solidaire-ecologique.fr/notre-programme-sante-solidarites/"
GRAND_URL_OSE_DEMOCRATIE = "https://orleans-solidaire-ecologique.fr/notre-programme-democratie/"
GRAND_URL_OSE_LOGEMENT = "https://orleans-solidaire-ecologique.fr/notre-programme-logement/"
GRAND_URL_OSE_URBANISME = "https://orleans-solidaire-ecologique.fr/notre-programme-urbanisme/"
GRAND_URL_OSE_COMMERCE = "https://orleans-solidaire-ecologique.fr/notre-programme-commerce/"
GRAND_URL_OSE_CULTURE = "https://orleans-solidaire-ecologique.fr/notre-programme-culture/"
GRAND_URL_OSE_SPORT = "https://orleans-solidaire-ecologique.fr/notre-programme-sport/"
GRAND_URL_OSE_ENVIRONNEMENT = "https://orleans-solidaire-ecologique.fr/notre-programme-environnement/"
GRAND_URL_OSE_NUMERIQUE = "https://orleans-solidaire-ecologique.fr/notre-programme-numerique/"
GRAND_URL_OSE_PROGRAMME = "https://orleans-solidaire-ecologique.fr/le-programme-de-la-liste-ose/"

# ============================================================
# PROPOSITIONS CHAPUIS — mappées aux 44 sous-thèmes
# ============================================================
PROPS_CHAPUIS = {
    # --- SECURITE ---
    "police-municipale": {
        "texte": "Renforcement de la police municipale au service de la proximité et de la tranquillité publique",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    # "videoprotection": déjà null — pas de proposition spécifique
    "prevention-mediation": None,  # déjà rempli — ne pas écraser
    "violences-femmes": {
        "texte": "Création d'un réseau de « safe spaces » dans les bars, commerces et écoles pour lutter contre le harcèlement de rue et les violences faites aux femmes",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    # --- TRANSPORTS ---
    "transports-en-commun": {
        "texte": "Gratuité progressive des transports en commun : d'abord les week-ends dès 2026, puis en semaine pour les jeunes et seniors, puis pour tous au-delà de 2030",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    "velo-mobilites-douces": {
        "texte": "Sécurisation des rues scolaires pour le vélo et développement d'un réseau cyclable continu dans toute la ville",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    "pietons-circulation": {
        "texte": "Apaisement de la circulation en centre-ville et sécurisation des traversées piétonnes autour des écoles",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    # "stationnement": pas de mesure spécifique
    "tarifs-gratuite": None,  # déjà rempli — ne pas écraser
    # --- LOGEMENT ---
    "logement-social": None,  # déjà rempli
    "logements-vacants": {
        "texte": "Lutte contre les logements vacants et les passoires thermiques pour remettre des logements sur le marché",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    "acces-logement": {
        "texte": "Faciliter l'accès au logement pour les jeunes et les familles, notamment par l'aide à l'installation",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    # --- EDUCATION ---
    "petite-enfance": None,  # déjà rempli
    "ecoles-renovation": None,  # déjà rempli
    "cantines-fournitures": None,  # déjà rempli
    "periscolaire-loisirs": {
        "texte": "Renforcement de l'offre périscolaire et des centres de loisirs dans tous les quartiers",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    "jeunesse": {
        "texte": "Création d'une Cité du numérique dans l'ancien collège Jean Rostand, dédiée aux jeunes et au jeu vidéo en partenariat avec l'ESAD",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    # --- ENVIRONNEMENT ---
    "espaces-verts": {
        "texte": "Végétalisation massive de la ville : toutes les cours d'école, les places et les rues transformées en îlots de fraîcheur",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    "proprete-dechets": {
        "texte": "Amélioration de la propreté urbaine et renforcement du tri sélectif dans tous les quartiers",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    "climat-adaptation": {
        "texte": "Plan climat ambitieux : adaptation de la ville aux canicules par la végétalisation et la désimperméabilisation des sols",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    "renovation-energetique": {
        "texte": "Rénovation énergétique des bâtiments municipaux et accompagnement des copropriétés dans leurs travaux",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    "alimentation-durable": {
        "texte": "Développement des circuits courts et de l'alimentation locale dans les cantines et marchés de la ville",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    # --- SANTE ---
    "centres-sante": {
        "texte": "Ouverture de centres de santé municipaux pour lutter contre les déserts médicaux dans les quartiers",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    "prevention-sante": {
        "texte": "Actions de prévention santé dans les quartiers prioritaires, en lien avec les associations",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    "seniors": {
        "texte": "Politique dédiée aux seniors : transport gratuit, lutte contre l'isolement et maintien à domicile",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    # --- DEMOCRATIE ---
    "budget-participatif": {
        "texte": "Mise en place d'un véritable budget participatif permettant aux habitants de décider de projets de quartier",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    "transparence": None,  # déjà rempli
    "vie-associative": None,  # déjà rempli
    "services-publics": {
        "texte": "Remise en service de proximité : guichets uniques de quartier pour simplifier les démarches administratives",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    # --- ECONOMIE ---
    "commerce-local": None,  # déjà rempli
    "emploi-insertion": {
        "texte": "Soutien à l'emploi local et à l'insertion professionnelle, avec des clauses sociales dans les marchés publics",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    "attractivite": {
        "texte": "Création d'un centre international Jeanne d'Arc et d'un musée Jean Zay pour renforcer le rayonnement d'Orléans",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    # --- CULTURE ---
    "equipements-culturels": None,  # déjà rempli
    "evenements-creation": {
        "texte": "Soutien renforcé à la création artistique et aux événements culturels tout au long de l'année",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    # --- SPORT ---
    "equipements-sportifs": None,  # déjà rempli
    "sport-pour-tous": {
        "texte": "Développement du sport pour tous : accès facilité aux équipements sportifs municipaux et aide aux clubs amateurs",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    # --- URBANISME ---
    "amenagement-urbain": {
        "texte": "Nouvelles Halles Châtelet pour valoriser la gastronomie locale, transformation du quartier de La Source et requalification des espaces publics",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    "accessibilite": {
        "texte": "Mise en accessibilité de tous les bâtiments et espaces publics pour les personnes en situation de handicap",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    "quartiers-prioritaires": {
        "texte": "Plan d'investissement massif pour les quartiers prioritaires : rénovation urbaine, services publics de proximité et animations",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    # --- SOLIDARITE ---
    "aide-sociale": {
        "texte": "Renforcement du CCAS et des aides d'urgence pour les personnes en difficulté",
        "source": CHAPUIS_SOURCE_MC,
        "sourceUrl": CHAPUIS_URL_MC
    },
    "egalite-discriminations": {
        "texte": "Plan de lutte contre toutes les discriminations et promotion de l'égalité femmes-hommes dans les politiques municipales",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
    "pouvoir-achat": {
        "texte": "Fournitures scolaires gratuites pour 5 000 élèves (coût 200 000 à 300 000 €), gratuité progressive des transports et tarifs solidaires pour les services municipaux",
        "source": CHAPUIS_SOURCE_FB,
        "sourceUrl": CHAPUIS_URL_FB
    },
}

# ============================================================
# PROPOSITIONS GRAND (OSE) — mappées aux 44 sous-thèmes
# ============================================================
PROPS_GRAND = {
    # --- SECURITE ---
    "police-municipale": {
        "texte": "Police de proximité dans les quartiers, sans tabou ni naïveté, avec des effectifs renforcés sur le terrain",
        "source": GRAND_SOURCE_MC,
        "sourceUrl": GRAND_URL_MC
    },
    "videoprotection": {
        "texte": "Évaluation indépendante de l'efficacité de la vidéoprotection existante avant tout déploiement supplémentaire",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SECURITE
    },
    "prevention-mediation": {
        "texte": "Prévention au cœur de la sécurité : médiation de rue, éducateurs spécialisés et traitement des causes profondes de l'insécurité",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SECURITE
    },
    "violences-femmes": {
        "texte": "Lutte contre les violences faites aux femmes : marches exploratoires nocturnes, meilleur éclairage public et partenariats avec les associations",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SECURITE
    },
    # --- TRANSPORTS ---
    "transports-en-commun": {
        "texte": "Gratuité progressive du tram : d'abord le samedi, puis jeunes/seniors, jours de pollution, grands événements, et gratuité totale en fin de mandat",
        "source": GRAND_SOURCE_MC,
        "sourceUrl": GRAND_URL_MC
    },
    "velo-mobilites-douces": None,  # déjà rempli
    "pietons-circulation": {
        "texte": "Pont Royal réservé aux piétons et cyclistes, passerelle piétonne reliant le Parc de Loire au Port Saint-Loup, et dégagement des trottoirs",
        "source": GRAND_SOURCE_MC,
        "sourceUrl": GRAND_URL_MC
    },
    "stationnement": {
        "texte": "Deux heures de stationnement gratuit le samedi pour les clients des commerces du centre-ville",
        "source": GRAND_SOURCE_FB,
        "sourceUrl": GRAND_URL_FB
    },
    "tarifs-gratuite": None,  # déjà rempli
    # --- LOGEMENT ---
    "logement-social": {
        "texte": "Meilleure répartition du logement social entre Orléans et la métropole, avec réservation de terrains en centre-ville pour du logement social intégré",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_LOGEMENT
    },
    "logements-vacants": {
        "texte": "Lutte contre la vacance des logements et les marchands de sommeil, objectif zéro logement indigne",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_LOGEMENT
    },
    "encadrement-loyers": {
        "texte": "Maîtrise de la dynamique des loyers et du foncier pour maintenir l'accessibilité au logement",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_LOGEMENT
    },
    "acces-logement": {
        "texte": "Garantir l'accès effectif au logement : mixité sociale renforcée et préservation d'une ville habitée et vivante",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_LOGEMENT
    },
    # --- EDUCATION ---
    "petite-enfance": {
        "texte": "Augmentation des places en crèche et développement de modes de garde diversifiés dans tous les quartiers",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SANTE
    },
    "ecoles-renovation": None,  # déjà rempli
    "cantines-fournitures": None,  # déjà rempli
    "periscolaire-loisirs": {
        "texte": "Rues scolaires sans voiture aux heures d'entrée et de sortie, et renforcement des activités périscolaires",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SECURITE
    },
    "jeunesse": {
        "texte": "Création d'un pôle de création vidéo et numérique pour les jeunes, possiblement aux Vinaigreries, et festival de deux mois dédié à la création",
        "source": GRAND_SOURCE_MC,
        "sourceUrl": GRAND_URL_MC
    },
    # --- ENVIRONNEMENT ---
    "espaces-verts": {
        "texte": "Coulée verte reliant la Loire au Loiret via Saint-Pryvé et le Parc de Loire, jusqu'à Saint-Jean-de-Braye",
        "source": GRAND_SOURCE_MC,
        "sourceUrl": GRAND_URL_MC
    },
    "proprete-dechets": {
        "texte": "Politique zéro déchet avec développement du compostage de quartier et réduction des déchets à la source",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_ENVIRONNEMENT
    },
    "climat-adaptation": {
        "texte": "Plan d'adaptation au changement climatique : désimperméabilisation des sols, îlots de fraîcheur et stratégie fondée sur le PCAET métropolitain",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_ENVIRONNEMENT
    },
    "renovation-energetique": {
        "texte": "Rénovation énergétique massive des bâtiments publics et accompagnement des copropriétés pour réduire durablement les charges",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_LOGEMENT
    },
    "alimentation-durable": {
        "texte": "Sécurité sociale de l'alimentation expérimentale : accès de tous à des produits de qualité, fête annuelle de l'alimentation et circuits courts",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SANTE
    },
    # --- SANTE ---
    "centres-sante": {
        "texte": "Renforcement de l'offre de soins de proximité dans les quartiers sous-dotés en professionnels de santé",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SANTE
    },
    "prevention-sante": {
        "texte": "Politique de prévention santé globale : qualité de l'air, qualité de l'eau, adaptation aux canicules et accès aux droits",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SANTE
    },
    "seniors": {
        "texte": "Développement de béguinages (habitats partagés pour seniors) et de tiny houses pour lutter contre l'isolement des personnes âgées",
        "source": GRAND_SOURCE_MC,
        "sourceUrl": GRAND_URL_MC
    },
    # --- DEMOCRATIE ---
    "budget-participatif": {
        "texte": "Budget participatif ambitieux repensé : chaque habitant peut proposer des projets utiles à son quartier, avec de vrais moyens",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_DEMOCRATIE
    },
    "transparence": {
        "texte": "États généraux, assemblée citoyenne tirée au sort et observatoires pour mesurer, corriger et rendre des comptes",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_DEMOCRATIE
    },
    "vie-associative": {
        "texte": "Conventions triennales garanties aux associations : subventions et prêts de locaux/matériel sur 3 ans pour assurer la stabilité",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SANTE
    },
    "services-publics": {
        "texte": "Services numériques sobres et accessibles, droit à la non-dématérialisation, logiciels libres et données ouvertes",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_NUMERIQUE
    },
    # --- ECONOMIE ---
    "commerce-local": None,  # déjà rempli
    "emploi-insertion": {
        "texte": "Économie au service du développement durable : clauses d'insertion dans les marchés publics et soutien à l'économie sociale et solidaire",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": "https://orleans-solidaire-ecologique.fr/orleans-ose-leconomie-au-service-du-developpement-durable/"
    },
    "attractivite": {
        "texte": "Attractivité fondée sur la qualité de vie et la transition écologique, en rupture avec les grands projets pharaoniques",
        "source": GRAND_SOURCE_MC,
        "sourceUrl": GRAND_URL_MC
    },
    # --- CULTURE ---
    "equipements-culturels": {
        "texte": "Renforcement des bibliothèques de proximité, place restaurée aux arts visuels et au numérique, et désacralisation de la culture",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_CULTURE
    },
    "evenements-creation": {
        "texte": "Festival de création de deux mois et repenser les grands événements pour qu'ils laissent des traces toute l'année",
        "source": GRAND_SOURCE_MC,
        "sourceUrl": GRAND_URL_MC
    },
    # --- SPORT ---
    "equipements-sportifs": {
        "texte": "Construction d'un gymnase inclusif avec sol en verre lumineux et murs interactifs, accessible aux personnes en situation de handicap",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SPORT
    },
    "sport-pour-tous": {
        "texte": "Sport accessible à tous : équipements adaptés aux personnes handicapées et développement du sport dans les quartiers prioritaires",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SPORT
    },
    # --- URBANISME ---
    "amenagement-urbain": {
        "texte": "Requalification des faubourgs Bannier et Bourgogne : voirie, modes doux, stationnement, logements, patrimoine et commerce de proximité",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_URBANISME
    },
    "accessibilite": {
        "texte": "Dégagement systématique des trottoirs et mise en accessibilité de tous les espaces publics pour les personnes handicapées et les poussettes",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SECURITE
    },
    "quartiers-prioritaires": {
        "texte": "En finir avec la fracture territoriale : équité entre tous les quartiers, réduction des inégalités d'accès aux services",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_URBANISME
    },
    # --- SOLIDARITE ---
    "aide-sociale": {
        "texte": "Protection des plus vulnérables : enfants, personnes âgées, handicapées et précaires, avec des mesures visibles et mesurables",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": GRAND_URL_OSE_SANTE
    },
    "egalite-discriminations": {
        "texte": "Élu·e dédié·e à la lutte contre les discriminations : plans d'action budgétés, comité citoyen de veille, dispositif d'alerte et rapport annuel public",
        "source": GRAND_SOURCE_OSE,
        "sourceUrl": "https://orleans-solidaire-ecologique.fr/en-finir-avec-les-discriminations/"
    },
    "pouvoir-achat": {
        "texte": "Tram gratuit le samedi, 2h de parking gratuit le samedi, cantines bio et locales re-municipalisées pour baisser le coût des repas",
        "source": GRAND_SOURCE_FB,
        "sourceUrl": GRAND_URL_FB
    },
}


def main():
    print(f"Lecture de {ORLEANS_JSON}...")
    with open(ORLEANS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Mettre à jour les infos candidats
    for candidat in data["candidats"]:
        if candidat["id"] == "chapuis":
            candidat["programmeUrl"] = CHAPUIS_URL_FB
            candidat["programmeComplet"] = True
            print(f"  → Chapuis : programmeComplet=True, URL mise à jour")
        elif candidat["id"] == "grand":
            candidat["programmeUrl"] = GRAND_URL_OSE_PROGRAMME
            candidat["programmeComplet"] = True
            print(f"  → Grand : programmeComplet=True, URL mise à jour")

    # Compteurs
    chapuis_added = 0
    chapuis_skipped = 0
    grand_added = 0
    grand_skipped = 0

    # Insérer les propositions
    for categorie in data["categories"]:
        for sousTheme in categorie["sousThemes"]:
            st_id = sousTheme["id"]
            props = sousTheme["propositions"]

            # --- CHAPUIS ---
            if st_id in PROPS_CHAPUIS and PROPS_CHAPUIS[st_id] is not None:
                if props.get("chapuis") is None:
                    props["chapuis"] = PROPS_CHAPUIS[st_id]
                    chapuis_added += 1
                    print(f"  + chapuis/{st_id}")
                else:
                    chapuis_skipped += 1
                    print(f"  = chapuis/{st_id} (déjà rempli, conservé)")

            # --- GRAND ---
            if st_id in PROPS_GRAND and PROPS_GRAND[st_id] is not None:
                if props.get("grand") is None:
                    props["grand"] = PROPS_GRAND[st_id]
                    grand_added += 1
                    print(f"  + grand/{st_id}")
                else:
                    grand_skipped += 1
                    print(f"  = grand/{st_id} (déjà rempli, conservé)")

    # Écriture
    print(f"\nÉcriture de {ORLEANS_JSON}...")
    with open(ORLEANS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"RÉSULTAT :")
    print(f"  Chapuis : {chapuis_added} propositions ajoutées, {chapuis_skipped} conservées (déjà présentes)")
    print(f"  Grand   : {grand_added} propositions ajoutées, {grand_skipped} conservées (déjà présentes)")

    # Compter le total des propositions non-null par candidat
    total_chapuis = 0
    total_grand = 0
    for categorie in data["categories"]:
        for sousTheme in categorie["sousThemes"]:
            if sousTheme["propositions"].get("chapuis") is not None:
                total_chapuis += 1
            if sousTheme["propositions"].get("grand") is not None:
                total_grand += 1

    print(f"\n  TOTAL Chapuis dans le JSON : {total_chapuis} propositions sur 44 sous-thèmes")
    print(f"  TOTAL Grand dans le JSON   : {total_grand} propositions sur 44 sous-thèmes")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
