#!/usr/bin/env python3
"""
Met à jour les propositions de Mounir Ben Ammar (REV) dans aix-en-provence-2026.json.
Source : Programme de campagne 2026 (PDF 30 pages, 230+ mesures)
"""

import json
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "data", "elections", "aix-en-provence-2026.json")

SOURCE = "Programme de campagne 2026"
SOURCE_URL = "data/programmes/Programme Ben Ammar_compressed.pdf"

# Mapping sous-thème -> mesures
PROPOSITIONS = {
    # === SECURITE ===
    "police-municipale": [
        "Police municipale de proximité avec présence humaine visible dans tous les quartiers et villages, réouverture de postes de quartier (dont le Jas-de-Bouffan).",
        "Formation et valorisation des agents de la police municipale, recréation du lien entre la police et la population.",
        "Meilleures conditions de travail et coordination renforcée avec la police nationale."
    ],
    "videoprotection": [
        "Moratoire sur l'extension de la vidéoprotection et évaluation publique indépendante de son efficacité.",
        "Réorientation des moyens consacrés à la vidéosurveillance vers la présence humaine et la prévention."
    ],
    "prevention-mediation": [
        "Prévention spécialisée renforcée : plus d'éducateurs de rue, de médiateurs sociaux et de lieux ouverts pour les jeunes en soirée et pendant les vacances.",
        "Lutte ciblée contre le trafic de stupéfiants : coopération renforcée avec l'État et présence de proximité sur l'espace public.",
        "Prévenir l'entrée des jeunes dans le trafic avec des programmes de prévention dès le collège, en lien avec les associations et les familles.",
        "Traiter l'addiction comme une question de santé publique : création d'un CAARUD (Centre d'Accueil et d'Accompagnement à la Réduction des Risques).",
        "Éclairage public adapté et sécurisant ; aménagements immédiats des zones dangereuses pour la sécurité routière."
    ],
    "violences-femmes": [
        "Politique municipale ambitieuse contre les violences faites aux femmes et aux enfants, création d'une Maison des femmes.",
        "Expérimentation d'un parcours de prise en charge coordonnée des victimes de violences sexistes et sexuelles (VSS).",
        "Campagnes locales de sensibilisation sur la prévention des VSS et l'égalité de genre dès le plus jeune âge, dans les écoles, équipements sportifs et culturels, espace public et transports."
    ],

    # === TRANSPORTS ===
    "transports-en-commun": [
        "Gratuité totale des transports en commun municipaux.",
        "Renforcement des lignes, fréquences et horaires pour une offre attractive.",
        "Création d'une halte ferroviaire à Luynes et développement de pôles d'échanges intermodaux.",
        "Abandon du projet BHNS au Plan d'Aillane au profit du tram-train utilisant la voie ferrée existante Aix-Rognac, desservant Les Milles, la Duranne et la gare TGV."
    ],
    "velo-mobilites-douces": [
        "Développement massif des pistes cyclables continues et sécurisées.",
        "Campagnes de sensibilisation et de soutien aux mobilités actives (marche, vélo, covoiturage).",
        "Création de parcours sécurisés et ludiques de mobilité active pour les enfants sur le chemin de l'école (pédibus scolaires)."
    ],
    "pietons-circulation": [
        "Réduction ciblée du trafic automobile dans les zones sensibles avec limitation de la vitesse à 30 km/h (écoles, cœurs de quartiers, centres historiques).",
        "Sécurité routière : aménagements immédiats des zones dangereuses, lutte contre les rodéos urbains, protection des piétons et cyclistes."
    ],
    "stationnement": [
        "Baisse et gel des tarifs municipaux de stationnement.",
        "Privilégier la densification urbaine en centre-ville au lieu de l'étalement urbain, réduisant la dépendance automobile."
    ],
    "tarifs-gratuite": [
        "Gratuité totale des transports en commun municipaux.",
        "Tarification sociale de l'eau avec gratuité des premiers mètres cubes."
    ],

    # === LOGEMENT ===
    "logement-social": [
        "Respecter la loi SRU et rattraper le retard en construisant massivement des logements sociaux pour les familles, les étudiants et les jeunes travailleurs.",
        "Moratoire sur les projets immobiliers non concertés et sur les démolitions de logements sociaux.",
        "Soutien aux coopératives d'habitants, à l'habitat participatif et au logement coopératif (seniors/étudiants).",
        "Construire une nouvelle auberge de jeunesse."
    ],
    "logements-vacants": [
        "Mobiliser le stock de 7 521 logements vacants en accompagnant les propriétaires pour une remise sur le marché locatif.",
        "Limiter les résidences secondaires et les locations touristiques de type Airbnb.",
        "Surveillance du bâti existant et mobilisation du droit de préemption."
    ],
    "encadrement-loyers": [
        "Encadrement strict et contrôlé des loyers.",
        "Limiter les résidences secondaires et les locations touristiques de type Airbnb.",
        "Sécurisation des parcours résidentiels et encadrement de la revente pour éviter toute spéculation."
    ],
    "acces-logement": [
        "Développement du bail réel solidaire (BRS) et des dispositifs anti-spéculatifs.",
        "Soutien à la création d'un Office Foncier Solidaire (OFS).",
        "Accompagnement municipal des primo-accédants.",
        "Réserver un quota de logements accessibles dans chaque programme immobilier ; aide municipale pour adapter les logements existants."
    ],

    # === EDUCATION ===
    "petite-enfance": [
        "Augmentation du nombre de places en crèche publique, avec priorité aux familles aixoises.",
        "Remunicipalisation progressive des crèches.",
        "Tarification sociale renforcée pour assurer une accessibilité financière réelle.",
        "Amélioration des conditions de travail des professionnels de la petite enfance."
    ],
    "ecoles-renovation": [
        "Soutien financier renforcé aux écoles publiques, priorité aux établissements des quartiers populaires.",
        "Rénovation des écoles dégradées et amélioration des conditions d'accueil.",
        "Plan d'accueil adapté pour les élèves en situation de handicap avec mise aux normes des locaux.",
        "Obtenir le label « Cité éducative » avec un Programme de Réussite Éducative pour les enfants en échec scolaire."
    ],
    "cantines-fournitures": [
        "Gratuité totale des cantines scolaires pour tous, 100 % bio et local, avec option alimentaire végane quotidienne.",
        "Gratuité des fournitures scolaires essentielles.",
        "Repas à 1 € pour tous les étudiants en partenariat avec le CROUS."
    ],
    "periscolaire-loisirs": [
        "Écoles ouvertes après 18h30 pour accompagnement scolaire, activités culturelles et citoyennes.",
        "Pour chaque enfant de 6 à 18 ans : accès gratuit ou à tarif très modique à un cours de sport, de musique ou d'expression artistique.",
        "Soutien aux AESH et accompagnement municipal dans les écoles ; aménagement des cantines et activités périscolaires inclusives.",
        "Soutien renforcé aux centres de loisirs inclusifs."
    ],
    "jeunesse": [
        "Mise en place d'un revenu universel municipal pour les jeunes et les étudiants (expérimentation progressive avec évaluation publique annuelle).",
        "Création d'une École de la Deuxième Chance à Aix pour les jeunes de 16 à 25 ans sortis du système scolaire sans diplôme.",
        "Épiceries sociales et solidaires dans tous les quartiers et à proximité des résidences étudiantes.",
        "Développement d'espaces d'expression et de participation des enfants et des jeunes à la vie locale."
    ],

    # === ENVIRONNEMENT ===
    "espaces-verts": [
        "Végétalisation prioritaire des rues, cours d'écoles, places, parkings et zones commerciales.",
        "Déploiement d'îlots de fraîcheur accessibles à tous (zones ombragées, arbres d'alignement, jardins publics et partagés).",
        "Zéro bétonnage des terres agricoles et naturelles (Constance, Montaiguet, Arbois, Puyricard).",
        "Moratoire sur le projet d'aménagement de la Constance et création d'un Grand Parc Cézanne (habitat, nature, parcours santé, espaces culturels, jardins partagés).",
        "Développement et protection des trames vertes et bleues : corridors biologiques reliant parcs, collines, jardins et ruisseaux."
    ],
    "proprete-dechets": [
        "Renforcement des effectifs municipaux dédiés à la propreté et à l'hygiène urbaine avec présence quotidienne dans tous les quartiers.",
        "Plan municipal de lutte contre les dépôts sauvages : enlèvement rapide, sanctions ciblées, responsabilisation des professionnels et bailleurs.",
        "Tolérance zéro contre l'habitat indigne et les marchands de sommeil ; renforcement des contrôles sanitaires des logements.",
        "Campagnes municipales régulières de dératisation écologique et préventive, en priorité autour des écoles et crèches.",
        "Soutien à la création d'une ressourcerie favorisant le recyclage et le réemploi."
    ],
    "climat-adaptation": [
        "Désimperméabilisation massive des sols publics et privés pour réduire les îlots de chaleur.",
        "Création d'un plan municipal « Ville ombragée et fraîcheur urbaine ».",
        "Élaboration d'un Plan communal de résilience climatique et création de refuges climatiques municipaux.",
        "Gestion publique, économe et transparente de l'eau ; réduction des fuites et recyclage des eaux pluviales.",
        "Lutte contre les pollutions de l'air et du bruit avec capteurs municipaux dans tous les quartiers, données publiées en open data."
    ],
    "renovation-energetique": [
        "Plan municipal de rénovation énergétique de tous les bâtiments communaux.",
        "Soutien aux kits de rénovation énergétique pour les ménages modestes.",
        "Production locale d'énergie renouvelable (solaire, géothermie) sur les bâtiments communaux et toitures municipales.",
        "Création d'un service public communal de la rénovation énergétique avec guichet municipal unique."
    ],
    "alimentation-durable": [
        "Priorité aux produits locaux et paysans dans la restauration collective municipale (cantines scolaires, crèches, EHPAD).",
        "Développement de fermes municipales ou partenariats agricoles de proximité.",
        "Lutte contre la précarité alimentaire par l'accès à des produits locaux de qualité.",
        "Création d'un Conseil local de l'alimentation et de l'agriculture paysanne.",
        "Soutien aux pratiques agricoles favorables au vivant : agroécologie, agriculture biologique, respect des sols et de l'eau."
    ],

    # === SANTE ===
    "centres-sante": [
        "Maisons pluridisciplinaires de santé, au Jas-de-Bouffan par exemple.",
        "Faciliter l'accès aux soins dans une période de pénurie de soignants ; améliorer les liens avec les CPTS.",
        "Bus santé itinérants.",
        "Soutenir le Planning familial et les associations de prévention santé."
    ],
    "prevention-sante": [
        "Campagne municipale de prévention : sensibilisation aux risques des perturbateurs endocriniens, de la malbouffe et de toutes les addictions.",
        "Développer une vraie campagne de sensibilisation sur les problèmes de santé mentale.",
        "Mener avec les associations des études sur la santé environnementale (qualité de l'air, bruit).",
        "Promotion d'une alimentation saine, végétale et accessible."
    ],
    "seniors": [
        "Créer des structures publiques pour les personnes dépendantes avec une gestion associative ou coopérative.",
        "Développer des services d'aide à la personne et soutenir les aidants familiaux.",
        "Création de lieux de répit et d'accueil de jour ; maison municipale du handicap à Aix."
    ],

    # === DEMOCRATIE ===
    "budget-participatif": [
        "Budget participatif écologique dédié à des projets de nature, d'alimentation durable, de mobilité douce et de biodiversité.",
        "Commissions citoyennes locales pour co-construire les politiques climatiques et environnementales.",
        "Conseil municipal du handicap avec habitants et associations ; accessibilité aux réunions publiques et bureaux de vote."
    ],
    "transparence": [
        "Publication annuelle d'un bilan local de la sécurité et de la prévention.",
        "Baisse ciblée des impôts locaux (taxe foncière) et de la taxe sur les ordures ménagères ; aucune augmentation des impôts et tarifs.",
        "Transparence totale sur les budgets culturels municipaux.",
        "Documents en FALC (facile à lire et à comprendre) pour l'accessibilité de la démocratie."
    ],
    "vie-associative": [
        "Création d'une Maison municipale de la vie associative : lieu ressource avec bureaux partagés, salles de réunion, accompagnement administratif et juridique.",
        "Mise à disposition gratuite ou à tarif symbolique des salles municipales pour les associations locales.",
        "Réforme des subventions associatives sur des critères clairs, publics et équitables ; fin du clientélisme.",
        "Co-construction des politiques publiques avec les habitants, le monde associatif, les CIQ et les conseils de quartier."
    ],
    "services-publics": [
        "Guichets uniques de quartier et bus itinérant des droits.",
        "Lutte contre la précarité numérique et énergétique.",
        "Amélioration des conditions de travail des agents de propreté et valorisation de ces métiers essentiels.",
        "Création d'un poste d'adjoint(e) au respect du vivant, consulté(e) sur tous les projets d'aménagement ayant un impact écologique."
    ],

    # === ECONOMIE ===
    "commerce-local": [
        "Soutien actif aux artisans et commerçants de proximité avec politique de préemption commerciale.",
        "Aides ciblées à l'installation et à la transmission des commerces indépendants.",
        "Requalification des centres commerciaux de proximité (Valcros au Jas-de-Bouffan, Luynes) en véritables lieux de vie.",
        "Revitalisation des marchés de quartier avec priorité aux producteurs locaux."
    ],
    "emploi-insertion": [
        "Expérimentation du dispositif Territoire Zéro Chômeur de Longue Durée, en priorité dans les quartiers populaires.",
        "Création d'emplois municipaux dans les secteurs essentiels : propreté, rénovation énergétique, mobilités, restauration collective, médiation, culture.",
        "Soutien renforcé aux structures de l'ESS (associations, coopératives, entreprises d'insertion).",
        "Généralisation des clauses sociales et environnementales dans 100 % des marchés publics municipaux.",
        "Développement de parcours d'insertion et de formation en lien avec l'École de la Deuxième Chance."
    ],
    "attractivite": [
        "Création d'un pôle municipal dédié aux entrepreneurs, artisans et porteurs de projets dans les anciens locaux du CFA, avec loyers modérés.",
        "Réorientation des aides publiques vers les projets créateurs d'emplois durables, locaux et écologiquement responsables.",
        "Mise à disposition d'ateliers, bureaux partagés, espaces de formation et d'accompagnement."
    ],

    # === CULTURE ===
    "equipements-culturels": [
        "Création d'une Cité des arts et de la culture municipale : résidences d'artistes, ateliers, cinéma public de quartier, espaces de pratiques amateurs.",
        "Construction d'une antenne de la bibliothèque Méjanes au Jas-de-Bouffan ; rénovation de la bibliothèque des Deux Ormes.",
        "Déploiement de bibliobus municipaux dans tous les quartiers et villages.",
        "Implantation du Muséum d'Histoire naturelle sur le site de la Constance."
    ],
    "evenements-creation": [
        "Réorientation progressive des financements vers la culture de proximité, l'éducation populaire et la création.",
        "Conditionnement des grandes subventions culturelles à des engagements clairs d'accessibilité sociale, territoriale et tarifaire.",
        "Développement d'actions de médiation culturelle, de lecture publique et d'ateliers dans les quartiers populaires.",
        "Accès facilité et gratuit aux équipements culturels municipaux ; création d'un Pass culture-sport handicap."
    ],

    # === SPORT ===
    "equipements-sportifs": [
        "Accès PMR aux festivals d'Aix, Grand Théâtre et équipements sportifs.",
        "Création d'un Pass culture-sport handicap."
    ],
    "sport-pour-tous": [
        "Pour chaque enfant et adolescent de 6 à 18 ans : accès gratuit ou à tarif très modique à un cours de sport.",
        "Sensibilisation au respect du vivant et à la protection de l'environnement dans les activités sportives."
    ],

    # === URBANISME ===
    "amenagement-urbain": [
        "Privilégier la densification urbaine en centre-ville au lieu de l'étalement urbain.",
        "Création d'une Maison des Projets : espace d'information, de débats et de coconstruction de la ville avec les citoyens.",
        "Création d'un adjoint(e) au respect du vivant, consulté(e) sur tous les projets d'aménagement ayant un impact écologique."
    ],
    "accessibilite": [
        "Audit complet des bâtiments municipaux, écoles, équipements sportifs et culturels pour l'accessibilité.",
        "Mise aux normes des trottoirs, passages piétons, arrêts de bus et marchés.",
        "Accessibilité des bus et parkings PMR supplémentaires ; taxis solidaires municipaux pour personnes isolées.",
        "Plan municipal d'emploi handicap dans la mairie et les DSP ; création d'un guichet unique handicap."
    ],
    "quartiers-prioritaires": [
        "Soutien financier renforcé aux écoles publiques des quartiers populaires.",
        "Redéploiement des moyens de propreté vers les secteurs les plus en difficulté.",
        "Expérimentation Territoire Zéro Chômeur de Longue Durée en priorité dans les quartiers populaires.",
        "Revitalisation des marchés de quartier à Jas-de-Bouffan, Encagnane, Val-Saint-André, Luynes."
    ],

    # === SOLIDARITE ===
    "aide-sociale": [
        "Plan municipal de soutien aux familles monoparentales.",
        "Épiceries sociales et solidaires dans tous les quartiers et à proximité des résidences étudiantes.",
        "Audit généralisé des charges locatives facturées par les bailleurs sociaux de la Ville.",
        "Accueil digne et accompagnement des personnes réfugiées ou exilées, en lien avec les associations locales.",
        "Soutien aux associations de solidarité internationale, de défense des droits humains et d'éducation populaire."
    ],
    "egalite-discriminations": [
        "Plan municipal de lutte contre toutes les discriminations (racisme, antisémitisme, islamophobie, LGBTIphobies, sexisme, handicap).",
        "Former tous les agents municipaux à la prévention et à la prise en charge des VSS.",
        "Respect strict de la loi de 1905 : neutralité de la puissance publique, liberté de conscience et libre exercice des cultes.",
        "Soutien à la création d'un centre cultuel et culturel musulman d'excellence via bail emphytéotique, sans financement public du culte.",
        "Évaluer toutes les politiques municipales à l'aune de l'inclusion avec une grille de validation inclusive, antiraciste, féministe et anti-validiste."
    ],
    "pouvoir-achat": [
        "Mise en place d'un revenu universel municipal pour les jeunes et les étudiants.",
        "Baisse ciblée des impôts locaux (taxe foncière) et de la taxe sur les ordures ménagères.",
        "Baisse et gel des tarifs municipaux (stationnement, services funéraires, activités périscolaires).",
        "Gratuité totale des cantines scolaires 100 % bio et locales.",
        "Tarification sociale de l'eau avec gratuité des premiers mètres cubes."
    ],
}


def main():
    # Charger le JSON
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Trouver le candidat ben-ammar
    candidat_id = "ben-ammar"
    candidat = None
    for c in data["candidats"]:
        if c["id"] == candidat_id:
            candidat = c
            break

    if not candidat:
        print(f"ERREUR : candidat '{candidat_id}' non trouvé !")
        sys.exit(1)

    # Mettre à jour les métadonnées du candidat
    candidat["programmeComplet"] = True
    candidat["programmePdfPath"] = "data/programmes/Programme Ben Ammar_compressed.pdf"
    candidat["liste"] = "Aix vivante et populaire (REV)"
    print(f"Candidat trouvé : {candidat['nom']}")
    print(f"  programmeComplet = True")
    print(f"  programmePdfPath = {candidat['programmePdfPath']}")

    # Compteurs
    sous_themes_couverts = 0
    sous_themes_null = 0
    total_mesures = 0

    # Parcourir les catégories et sous-thèmes
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            props = st["propositions"]

            if st_id in PROPOSITIONS:
                mesures = PROPOSITIONS[st_id]
                props[candidat_id] = {
                    "source": SOURCE,
                    "sourceUrl": SOURCE_URL,
                    "mesures": mesures
                }
                sous_themes_couverts += 1
                total_mesures += len(mesures)
            else:
                # Laisser null si pas de mesure
                if candidat_id not in props or props[candidat_id] is None:
                    sous_themes_null += 1

    # Sauvegarder
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nRésultat :")
    print(f"  Sous-thèmes couverts : {sous_themes_couverts}")
    print(f"  Sous-thèmes sans mesure (null) : {sous_themes_null}")
    print(f"  Total mesures : {total_mesures}")
    print(f"\nFichier sauvegardé : {JSON_PATH}")


if __name__ == "__main__":
    main()
