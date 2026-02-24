#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration COMPLÈTE du programme de Florian Kobryn (LFI, Strasbourg)
PDF de 96 pages, ~400 mesures extraites et classées dans 44+ sous-thèmes.

Source unique : data/programmes/kobryn-strasbourg-programme.pdf
Site : https://www.kobryn2026.eu/
"""
import json
import os
import sys
import io

# Encodage UTF-8 pour Windows
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")
ELECTIONS_DIR = os.path.join(ROOT_DIR, "data", "elections")
JSON_PATH = os.path.join(ELECTIONS_DIR, "strasbourg-2026.json")

CANDIDAT_ID = "kobryn"
SOURCE = "Programme municipal Florian Kobryn 2026 (96 pages)"
SOURCE_URL = "https://www.kobryn2026.eu/"

# =============================================================================
# TOUTES LES PROPOSITIONS EXTRAITES DU PDF, CLASSÉES PAR SOUS-THÈME
# Format : sous-thème ID -> texte unique (concaténation de toutes les mesures)
# =============================================================================

PROPOSITIONS = {
    # =========================================================================
    # SÉCURITÉ
    # =========================================================================
    "police-municipale": {
        "texte": (
            "Développer une police municipale de proximité mieux rémunérée et formée, "
            "avec un plan de carrière pour les agents. Refuser l'armement létal et privilégier "
            "des moyens alternatifs (brigade cynophile, matériel de protection). Former les agents "
            "à la désescalade et à la gestion non violente des conflits. Instaurer un récépissé "
            "obligatoire lors de toute intervention de la police municipale et demander "
            "l'expérimentation du récépissé de contrôle d'identité par la police nationale sur "
            "le territoire communal. Former les agents à la lutte contre l'extrême droite et "
            "l'ultra-droite pour prévenir les agressions fascistes. "
            "Assurer une meilleure dotation logistique et matérielle. "
            "Engager un dialogue constant avec l'Etat et la préfecture pour évaluer la pertinence "
            "de dispositifs comme la présence de CRS dans certains quartiers."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "videoprotection": {
        "texte": (
            "Défendre un moratoire sur les caméras de vidéosurveillance pour empêcher "
            "toute nouvelle extension, tout en maintenant l'existant. Refuser tout recours "
            "à la biométrie et à la reconnaissance faciale dans le maintien de l'ordre, et "
            "s'opposer au recours aux drones pour contenir le mouvement social."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "prevention-mediation": {
        "texte": (
            "Renforcer massivement la présence des médiateurs de rue avec titularisation "
            "en tant qu'agents de la collectivité. Assurer le lien entre les acteurs de terrain "
            "(médiateurs, police, associations, éducateurs) via les Groupes de Partenariats "
            "Opérationnels. Créer un pôle municipal de lutte contre la solitude et pour la "
            "santé mentale. Elaborer un plan global de lutte contre le narcotrafic incluant "
            "une cartographie des lieux propices aux trafics et des rencontres populaires "
            "dans ces espaces. Proposer des formations de prévention (harcèlement de rue, "
            "violences sexistes, addictions). Maintenir la salle de consommation à moindre "
            "risque (SCMR). Associer les habitants au Conseil Local de Sécurité et de "
            "Prévention de la Délinquance. Créer des points d'écoute municipaux. "
            "Renforcer l'accompagnement des personnes vulnérables : politique Logement "
            "d'abord, financement de la prévention spécialisée, pérennisation des Haltes "
            "Soins Addiction."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "violences-femmes": {
        "texte": (
            "Mettre en place un plan de lutte contre le harcèlement de rue : dispositif "
            "discret co-construit avec des associations de femmes, arrêt à la demande "
            "dans le bus de 22h à 6h, annonces sonores sur les violences sexistes dans "
            "les transports en commun, campagnes de prévention. Initier des comités de "
            "défense des victimes de violences sexuelles pour le réexamen des plaintes "
            "classées sans suite. Soutenir la Maison des femmes et Solidarité femmes 67. "
            "Développer des mesures d'éloignement des conjoints violents et d'accompagnement "
            "des auteurs de violence. Créer une ordonnance menstruelle pour protections "
            "gratuites aux femmes précaires. Poursuivre le rapport de force pour un congé "
            "gynécologique. Penser l'espace urbain avec un prisme féministe : "
            "marches exploratoires genrées, études d'impact genrées pour tout aménagement. "
            "Engager un plan de rattrapage pour l'égalité salariale femmes-hommes dans "
            "la collectivité. Engager un plan de lutte contre le harcèlement sexuel au "
            "travail en lien avec les organisations syndicales."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # TRANSPORTS
    # =========================================================================
    "transports-en-commun": {
        "texte": (
            "Reprendre l'extension du réseau de tramway en commençant par le Tram Nord "
            "vecteur de transformation urbaine, en donnant la priorité aux quartiers "
            "populaires mal desservis. Augmenter le cadencement et l'amplitude des "
            "transports en commun, y compris en soirée, pour garantir l'égalité urbaine. "
            "Soutenir le projet Gare à 360 degrés sur son volet ferroviaire tout en "
            "refusant l'emprise du privé. Poursuivre le développement du REME et "
            "travailler avec la SNCF pour augmenter la fréquence des TER vers "
            "Krimmeri-Meinau. Défendre le maintien et la réouverture des guichets, gares "
            "et lignes locales de train ainsi que le transport fluvial de marchandises. "
            "Planifier le réseau pour une ville en 15 minutes. Renforcer l'accessibilité "
            "du Stade de la Meinau les soirs de match. Etudier l'accessibilité des lacs "
            "de l'Eurométropole en transport en commun en période estivale."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "velo-mobilites-douces": {
        "texte": (
            "Nouveau Plan vélo 2026-2032 priorisant les quartiers populaires. Massifier "
            "le stationnement vélo dans l'espace public, près des gares et arrêts de "
            "transport, avec places dédiées aux vélos cargos. Renforcer la tarification "
            "sociale de Velhop avec une première tranche à 0 euro et augmenter le parc. "
            "Faciliter l'acquisition de vélos en étendant les aides aux vélos musculaires "
            "et d'occasion. Créer un maillage d'espaces de réparation de vélo. "
            "Objectif 100% du Savoir Rouler à Vélo pour les élèves. Autoriser les chiens "
            "dans les bus selon les mêmes règles que dans le tram."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "pietons-circulation": {
        "texte": (
            "Assurer la mise en oeuvre du Plan piéton 2021-2030 avec une ligne de "
            "financement dédiée. Faire la Ville à 30 km/h comme norme, le 50 km/h "
            "comme exception. Etablir un plan Vision Zéro pour zéro accident grave ou "
            "mortel, en sanctionnant systématiquement les abus de stationnement aux "
            "heures de pointe et entrées/sorties d'écoles. Désencombrer les trottoirs "
            "des obstacles (arceaux vélo, panneaux, parcmètres, bornes de recharge). "
            "Tendre à la dé-motorisation de la Grande Ile en garantissant l'accès aux "
            "usages essentiels (handicap, riverains, livraisons, taxis). Sécuriser les "
            "carrefours dangereux en les transformant en profondeur. Assurer la "
            "continuité des itinéraires piétons et vélos pendant les chantiers en "
            "mettant fin aux panneaux cyclistes pieds à terre. Anticiper les conflits "
            "piétons-vélos par des aménagements et expérimenter les sanctions "
            "pédagogiques. Mettre en place des comités d'usagers pour les politiques "
            "de mobilités. Garantir un accès à la nature sans dépendre de la voiture."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "stationnement": {
        "texte": (
            "Mettre en place progressivement le doublement du prix du stationnement "
            "pour les SUV. Repenser les tranches de l'abonnement résident avec une "
            "première tranche gratuite pour les précaires puis 5 euros par mois. "
            "Tarification solidaire dans les parkings-silo municipaux. Repenser le "
            "stationnement des deux-roues motorisés avec espaces dédiés sur chaussée "
            "et stationnement payant effectif."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "tarifs-gratuite": {
        "texte": (
            "Viser la gratuité des transports en commençant par les moins de 25 ans "
            "et les demandeurs d'emploi. Renforcer la tarification solidaire avec un "
            "premier palier à 0 euro. Mettre le premier échelon de tarification sociale "
            "à 0 euro pour tous les services publics municipaux (parking, transport, "
            "cantine). Intégrer une tarification étudiante au Quotient familial unique."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # LOGEMENT
    # =========================================================================
    "logement-social": {
        "texte": (
            "Construire plus de logements sociaux que le seuil minimal imposé par l'Etat "
            "avec un plan ambitieux sur l'ensemble de la ville. Renforcer la mixité sociale "
            "en augmentant les pourcentages obligatoires de logements sociaux au-delà des "
            "planchers légaux, équitablement répartis sur tout le territoire. Engager un "
            "rapport de force avec les bailleurs sociaux pour la baisse des loyers des "
            "ménages les plus fragiles. Conditionner les soutiens (garanties, foncier, "
            "subventions) à des engagements sur les loyers. Adapter les zonages de mixité "
            "sociale du PLU. Accompagner l'habitat coopératif et participatif."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "logements-vacants": {
        "texte": (
            "Lutter contre le logement vacant : état des lieux précis du parc foncier "
            "et création d'une Brigade de lutte contre le logement vacant privé. "
            "Utiliser pleinement le droit de préemption pour acquérir des biens "
            "stratégiques. Combattre les meublés touristiques type Airbnb : quotas "
            "d'autorisations, limitation à 90 jours par an (au lieu de 120), renforcement "
            "des contrôles avec amendes de 10 000 à 20 000 euros, intégration au "
            "dispositif de la loi SREN obligeant les plateformes à transmettre leurs "
            "données. Information des copropriétés sur le droit d'interdire les meublés "
            "touristiques."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "encadrement-loyers": {
        "texte": (
            "Mettre en place l'encadrement des loyers et participer au plaidoyer pour "
            "la continuation du dispositif au-delà d'octobre 2026 sous une forme plus "
            "efficace. Prioriser le Bail Réel Solidaire (BRS) pour faciliter l'accès à "
            "la propriété avec un seuil minimal dans le PLU. Encadrer les prix de vente "
            "immobilière via une charte promoteur pour réguler les marges excessives. "
            "Mettre en place un observatoire des loyers commerciaux. Protéger les habitants "
            "face aux expulsions abusives : la Ville se constituera systématiquement partie "
            "civile pour défendre les locataires victimes."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "acces-logement": {
        "texte": (
            "Garantir un parcours résidentiel dans une logique Logement d'abord : "
            "faciliter l'accès au logement social pour les personnes reconnues DALO "
            "avec des quotas réservés. Créer 300 places d'hébergement d'urgence "
            "pendant le mandat. Agir pour mettre à l'abri les enfants à la rue avec "
            "une procédure de signalement et mise à l'abri dans les écoles hors horaires. "
            "Créer une délégation d'élu dédiée à la protection des enfants à la rue. "
            "Développer le logement intercalaire en partenariat avec les associations. "
            "Engager un rapport de force avec l'Etat sur l'hébergement d'urgence et "
            "le remboursement des frais engagés hors compétence. S'opposer à toute "
            "nouvelle artificialisation des terres. Politique volontariste de réquisition "
            "et mise à disposition d'équipements publics lors d'aléas climatiques "
            "(grand froid, canicule) pour les personnes vulnérables. Etendre le permis "
            "de louer pour responsabiliser les bailleurs. Renforcer les agents d'inspection "
            "des logements insalubres. Etablir un plan de lutte contre la précarité "
            "étudiante incluant le doublement des logements CROUS (objectif 10 000 places). "
            "S'opposer à la hausse des loyers des résidences universitaires."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # ÉDUCATION
    # =========================================================================
    "petite-enfance": {
        "texte": (
            "Permettre à 100% des parents d'obtenir une place pour leurs enfants en "
            "proposant des modes d'accueil diversifiés à taille humaine (crèches, "
            "multi-accueils, relais assistantes maternelles). Réduire le recours aux "
            "opérateurs privés lucratifs au profit des structures publiques et "
            "associatives. Favoriser l'accueil des enfants en situation de handicap "
            "dans les crèches publiques. Pérenniser la présence d'une ATSEM par "
            "classe de maternelle."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "ecoles-renovation": {
        "texte": (
            "Végétaliser l'ensemble des cours d'école non encore végétalisées pour "
            "créer des espaces de fraicheur ouverts aux habitants en été. Sécuriser "
            "les trajets vers l'école par des cheminements enfants reliant espaces "
            "verts et terrains de jeux par des voies piétonnes et cyclables. "
            "Supprimer toutes les aides extra-légales à l'enseignement privé. "
            "Développer des classes spécialisées pour l'accueil des enfants avec "
            "handicaps lourds (classes UEMA autisme). Construire une sectorisation "
            "qui mette fin à la ségrégation scolaire. Scolariser et ouvrir la cantine "
            "à tous les enfants présents sur le territoire, y compris Roms, étrangers, "
            "vivant en squat ou hôtels sociaux."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "cantines-fournitures": {
        "texte": (
            "Allouer à tous les élèves de maternelle une dotation de fournitures "
            "scolaires gratuites, avec expérimentation d'une extension à l'élémentaire. "
            "Grand plan de développement des cantines scolaires. Proposer une option "
            "végétarienne à chaque repas, deux jours tout-végétarien par semaine et "
            "un jour végétalien par mois. Ré-internaliser la production de repas en "
            "régie municipale via une cantine centrale publique. Instaurer la gratuité "
            "immédiate de la cantine pour les familles sous le seuil de pauvreté et "
            "tendre vers la gratuité générale. Faire du repas un moment d'éducation à "
            "l'alimentation et de lutte contre le gaspillage."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "periscolaire-loisirs": {
        "texte": (
            "Garantir un nombre suffisant d'animateurs périscolaires formés en emploi "
            "non précaire, en visant le temps plein. Garantir la neutralité du "
            "périscolaire en y refusant toute intervention d'associations religieuses, "
            "marchandes ou de lobbies patronaux. Proposer un plan d'éducation populaire "
            "aux enjeux environnementaux sur le temps périscolaire. Proposer un plan "
            "d'éducation au consentement. Ouvrir un espace parents animé dans chaque "
            "école. Créer des conseils de parents associés aux assemblées de quartier "
            "pour l'aménagement des aires de jeux, jardins et bibliothèques. Soutenir "
            "l'accompagnement à la parentalité dans les équipements municipaux (échanges, "
            "accueils-jeux, ateliers). Rendre plus transparente la procédure d'attribution "
            "des dérogations scolaires."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "jeunesse": {
        "texte": (
            "Permettre le droit aux vacances en organisant des colonies de vacances "
            "municipales avec quasi-gratuité pour les précaires et tarif dégressif selon "
            "le quotient familial pour les 10-16 ans. Accorder le droit de vote aux "
            "mineurs de plus de 16 ans dans les votations citoyennes. Développer des "
            "initiatives pour l'orientation et l'accès à l'emploi des jeunes : bourses "
            "aux stages, forums, aide à la rédaction de CV. Expérimenter l'ouverture "
            "d'équipements publics en soirée pour les jeunes (gymnases, maisons de "
            "quartier). Favoriser l'accueil en stage des jeunes des QPV au sein de la "
            "collectivité. Faciliter l'accès au Fonds d'aide aux jeunes."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # ENVIRONNEMENT
    # =========================================================================
    "espaces-verts": {
        "texte": (
            "Adopter une stratégie de lutte contre les ilots de chaleur urbains avec "
            "développement d'ilots de fraicheur végétaux et espaces verts. Adopter un "
            "plan de renaturation et régénération des sols urbains. Accompagner "
            "l'émergence d'un Parc Naturel Urbain entre le Neudorf, la Meinau et le "
            "Neuhof le long du Rhin Tortu. Continuer de créer et renforcer des corridors "
            "écologiques. Poursuivre le plan canopée ambitieux avec les bailleurs "
            "sociaux. Développer des espaces de jardinage urbain supplémentaires "
            "et jardins collectifs. Tendre vers l'interdiction de l'éclairage nocturne "
            "des magasins et panneaux publicitaires. Interdiction progressive des "
            "panneaux publicitaires dans l'espace public."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "proprete-dechets": {
        "texte": (
            "Mener un plan de municipalisation de l'usine de valorisation des déchets "
            "Sénerval : construire une nouvelle usine respectant les normes environnementales "
            "et mettre fin à la gestion par le groupe Séché. Développer massivement la "
            "filière du réemploi et du recyclage de matériaux dans les chantiers de travaux "
            "publics, espaces verts et bâtiment. Faire du Shadok un lieu pilote pour le "
            "réemploi avec un FabLab ouvert. Poursuivre le soutien à l'économie du prêt "
            "(ressourceries, recycleries, prêt d'outils). Mener une étude sur le recyclage "
            "des urines et matières fécales en engrais pour les agriculteurs du territoire. "
            "Mettre en oeuvre un inventaire et plan de mutualisation des équipements "
            "publics pour les ouvrir aux partenaires associatifs et citoyens. Etudier "
            "la réutilisation des eaux de pluie pour le nettoyage des rues et l'arrosage. "
            "Mettre à disposition de la vaisselle de prêt pour les associations. Lutte "
            "contre les nuisances des animaux liminaires : contraindre les bailleurs sociaux, "
            "développer les poubelles enterrées."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "climat-adaptation": {
        "texte": (
            "Organiser une convention citoyenne pour la bifurcation écologique. "
            "Réviser le Plan Climat Air Territorial (PCAET) avec trajectoire de réduction "
            "des émissions de gaz à effet de serre. Réaffirmer l'objectif zéro "
            "artificialisation nette d'ici 2050. Passer du budget vert à un Plan "
            "Pluriannuel d'Investissement aligné aux objectifs climat en expérimentant "
            "la comptabilité écologique. Refuser d'accorder des permis pour des activités "
            "polluantes et écocides. Améliorer le plan canicule avec des lieux frais "
            "(médiathèques, cinémas) pour la population vulnérable. Gestion de l'eau "
            "fondée sur la nature : infiltration des eaux pluviales, désimperméabilisation "
            "massive des espaces publics. Constituer des réserves stratégiques de biens "
            "essentiels (médicaments, denrées non périssables). Former massivement la "
            "population aux premiers secours à tous les âges. Etudier la création d'une "
            "réserve citoyenne de protection civile. Analyser l'impact du réchauffement "
            "sur les infrastructures, l'agriculture, les ressources en eau et la santé. "
            "Former les agents et partenaires de l'Eurométropole à une écologie populaire. "
            "Proposer un plan d'éducation populaire aux enjeux environnementaux avec "
            "ligne budgétaire dédiée."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "renovation-energetique": {
        "texte": (
            "Augmenter les moyens pour subventionner la rénovation du parc social et "
            "privé, en faisant de la rénovation énergétique une priorité du mandat. "
            "Structurer une filière du bâtiment avec des structures d'insertion "
            "professionnelle. Massifier l'accompagnement à la rénovation thermique en "
            "renforçant l'Agence du Climat et en l'intégrant au plan de municipalisation. "
            "Etablir un plan de sortie du fioul résidentiel et tertiaire. Agir contre "
            "l'habitat indigne et la précarité énergétique avec un plan de repérage, "
            "réhabilitation et sanction des logements non-décents. Développer des réseaux "
            "de chaleur urbains municipaux. Demander aux bailleurs d'intégrer la qualité "
            "de l'air intérieur dans les rénovations avec contrôle systématique de la "
            "ventilation. Protéger contre la précarité énergétique d'été avec un plan "
            "spécifique face aux épisodes de canicule. Adopter un plan de développement "
            "des énergies renouvelables avec les associations citoyennes, les coopératives "
            "et la SPL Strasbourg Energies Renouvelables Eurométropolitaines."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "alimentation-durable": {
        "texte": (
            "Initier le plan Alimentation Commune tendant vers la municipalisation "
            "de la production (fermes municipales sans élevage), la transformation "
            "(légumerie municipale) et la distribution de nourriture pour irriguer les "
            "cantines. Poursuivre les démarches sur l'agriculture bio et locale et la "
            "sécurité sociale de l'alimentation. Expérimenter des légumeries municipales "
            "à proximité de la ville. Mettre en place une cantine populaire écologique "
            "et sociale ouverte à tous avec produits locaux et de saison, incluant un "
            "service de livraison à vélo pour les personnes à domicile."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # SANTÉ
    # =========================================================================
    "centres-sante": {
        "texte": (
            "Créer des Centres de Santé Municipaux avec médecins généralistes, "
            "psychiatres, psychologues, dentistes, kinésithérapeutes, infirmiers, "
            "médiateurs et traducteurs en santé, en association avec les hôpitaux "
            "publics. Prise en compte des besoins des personnes transgenres et "
            "intersexes et attention aux problématiques spécifiques de santé sexuelle "
            "et reproductive. Mener une expérimentation sur la création d'une mutuelle "
            "municipale inspirée des caisses ouvrières. Lutter contre les suppressions "
            "de postes au CHU via la présidence du conseil de surveillance occupée "
            "par la mairie. Créer des bains-douches sécurisés aux horaires étendus."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "prevention-sante": {
        "texte": (
            "Appuyer le développement de Haltes Soins Addiction (salles de consommation) "
            "avec un espace non mixte pour les femmes. Appuyer les micro-structures "
            "associant médecins, psychologues et travailleurs sociaux dans les quartiers "
            "prioritaires. Lutter contre la pollution de l'air avec des capteurs de mesure "
            "fixes devant les écoles et zones industrielles. Agir pour la dépollution "
            "de l'avenue du Rhin (passage à 2x1 voie). Mettre en place des campagnes "
            "de prévention contre les IST, les addictions et les maladies liées à la "
            "pollution. Soutenir le Planning familial. Proposer des formations aux "
            "premiers secours en santé mentale."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "seniors": {
        "texte": (
            "Favoriser des activités physiques adaptées dans tous les territoires. "
            "Intégrer un service de livraison de repas à vélo pour les personnes âgées "
            "à domicile via les cantines populaires. Soutenir les associations de proches "
            "aidants. Faire respecter la loi Bien vieillir avec services de proximité, "
            "actions de prévention et lutte contre l'isolement. Favoriser l'accessibilité "
            "des transports en commun pour les seniors. Encourager la création de pôles "
            "gériatriques regroupant acteurs publics, associatifs et de santé. Développer "
            "les clubs seniors et l'accès aux activités culturelles. Développer un plan "
            "canicule efficace. Favoriser le lien intergénérationnel."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "animaux-compagnie": {
        "texte": (
            "Renouveler la délégation relative à la condition animale au conseil municipal. "
            "Proposer une option végétarienne quotidienne et deux jours végétariens par "
            "semaine dans les cantines scolaires, un jour végétalien par mois. "
            "Option végétalienne quotidienne dans les restaurants administratifs. "
            "Ne pas autoriser d'animations avec des animaux sur le domaine public. "
            "Intégrer des critères de bien-être animal dans tous les appels d'offres "
            "municipaux. Créer de nouveaux caniparcs et rénover les existants. Interdire "
            "tout événement reposant sur la captivité ou la mise en scène d'animaux. "
            "Exclure des budgets participatifs tout projet impliquant une exploitation "
            "animale."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # DÉMOCRATIE
    # =========================================================================
    "budget-participatif": {
        "texte": (
            "Réserver la totalité du budget participatif aux habitants des QPV et "
            "rendre plus transparente la procédure d'attribution. Faire évoluer les "
            "conseils de quartier en instances citoyennes composées d'habitants tirés "
            "au sort, ouverts dès 16 ans y compris aux résidents étrangers, avec droit "
            "d'interpellation et consultation obligatoire sur les projets de quartier. "
            "Mettre en place un référendum d'initiative citoyenne local accessible à "
            "10% du corps électoral, incluant les étrangers et les mineurs de plus de "
            "16 ans. S'engager sur la révocabilité des élus si 20% du corps électoral "
            "le demande par pétition vérifiée."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "transparence": {
        "texte": (
            "Signer la charte Anticor pour des communes plus éthiques. Plafonner les "
            "indemnités du maire à 3 fois le salaire de l'agent le moins payé. Exiger la "
            "publication de tous les rendez-vous des élus liés à leur mandat et le refus "
            "de tout cadeau d'entreprise. Rendre obligatoire la présence aux conseils "
            "d'administration quand une rémunération y est associée. Rendre accessible "
            "l'ordre du jour du conseil municipal et les documents. Rendre publiques les "
            "déclarations de patrimoine et les indemnités. Publier de nouvelles données en "
            "open data et simplifier l'accès. Renforcer la plateforme numérique citoyenne "
            "avec un module forum. Evaluer l'accessibilité de toutes les communications "
            "(langage facile, sous-titrage, LSF, braille). Avant l'élection, s'engager à "
            "signer une Charte de l'élu avec des règles d'exemplarité et de transparence. "
            "Lancer une campagne locale d'inscription sur les listes électorales."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "vie-associative": {
        "texte": (
            "Généraliser les conventions pluriannuelles pour un financement stable des "
            "associations. Mettre en régie municipale la Maison des associations pour en "
            "faire un lieu ressource. Organiser des Etats généraux de la vie associative "
            "avec un Conseil de la vie associative. Augmenter les moyens alloués au "
            "soutien administratif des associations avec attention prioritaire aux QPV. "
            "Créer un guichet unique facilitant la vie associative (création, subventions, "
            "salles). Expérimenter la mutualisation des fonctions supports pour les "
            "petites associations. Développer la gratuité de mise à disposition des "
            "infrastructures municipales (espaces publics, matériel, salles). Créer une "
            "commission diversité et inclusion pour accompagner les associations. "
            "Accompagner les expérimentations associatives innovantes en matière de "
            "transformation sociale et écologique. Mettre en place un dispositif de "
            "signalement des discriminations au sein des associations subventionnées. "
            "Adapter les horaires de rencontre aux besoins des associations. Contribuer "
            "au plaidoyer pour un meilleur financement et de meilleures conditions de "
            "travail pour les salariés associatifs."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "services-publics": {
        "texte": (
            "Etablir un plan de dé-privatisation des services publics pour mettre fin "
            "aux DSP et tendre vers des régies directes (eau, énergie, transport, "
            "déchets, alimentation, santé, petite enfance). Renforcer le contrôle des "
            "DSP existantes avec audit et clause de retour à meilleure fortune. "
            "Publier un état des lieux des services publics et de leur statut. "
            "Déclarer Strasbourg Zone hors-AGCS contre la mise en concurrence public-privé. "
            "Garantir un contrôle citoyen en ouvrant la CCSPL à toutes les associations "
            "et citoyens. Instaurer une échelle des salaires dans les entreprises "
            "publiques (1 à 3 maximum). Notre plan de re-municipalisation permettra une "
            "gestion plus transparente et démocratique."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # ÉCONOMIE
    # =========================================================================
    "commerce-local": {
        "texte": (
            "Encadrer le secteur privé via le foncier (droit de préemption et critères "
            "de location pour usage commercial), via le PLU avec conditions fortes pour "
            "les grands projets privés, via le Pacte pour une économie locale durable "
            "refondu, et via les critères de marchés publics (SPASER). Soutenir par la "
            "commande publique les entreprises utiles à la bifurcation écologique. "
            "Pour les investissements municipaux, privilégier les établissements bancaires "
            "vertueux sur le modèle de Besançon. Limiter les bateaux de croisière et "
            "freiner les Free Tours au profit des guides-conférenciers diplômés."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "emploi-insertion": {
        "texte": (
            "Créer un lieu ressource pour les livreurs à vélo : lieu de repos, accès "
            "à l'eau et à l'électricité, avec permanences juridiques, administratives "
            "et de santé pour les travailleurs ubérisés. Lutter contre la précarité des "
            "agents publics : plans de titularisation, éradication du temps partiel subi, "
            "négociations salariales, prévention des risques psycho-sociaux. Garantir "
            "l'égalité salariale femmes-hommes dans la collectivité. Affirmer le rôle de "
            "l'ESS dans la planification économique communale face aux acteurs privés. "
            "Soutenir les mutualisations entre acteurs de l'ESS et créer un service de "
            "R&D de l'ESS. Soutenir la monnaie locale en créant un poste de conseiller "
            "municipal délégué à la monnaie locale. Structurer une filière du bâtiment "
            "via des structures d'insertion pour rendre attractifs les métiers de la "
            "rénovation énergétique. Mesurer les discriminations à l'emploi au sein de "
            "la collectivité et réévaluer les processus de recrutement."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "attractivite": {
        "texte": (
            "Rendre payant l'accès au marché de Noël le week-end pour les personnes "
            "extérieures à l'Eurométropole, recettes investies dans la lutte contre "
            "les enfants à la rue, avec dispositifs de tarification solidaire. Mettre "
            "fin à la marque Strasbourg Capitale de Noël. Décentraliser le marché de "
            "Noël dans d'autres quartiers en logique de substitution. Développer le "
            "marché OFF pour la production locale. Poursuivre la promotion de produits "
            "locaux et durables à des prix accessibles dans les stands. Instaurer un "
            "péage pour les autocars de tourisme avec obligation de réservation et "
            "limite de stationnement. Rendre les institutions européennes plus "
            "accessibles aux Strasbourgeois. Affirmer une ligne politique populaire "
            "dans le contrat triennal européen. Requestionner la notabilité européenne "
            "avec transparence sur ses coûts (dont financement de l'Ecole européenne). "
            "Faire un état des lieux des réseaux de villes et évaluer les engagements "
            "pris dans ces cadres."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # CULTURE
    # =========================================================================
    "equipements-culturels": {
        "texte": (
            "Créer une bibliothèque dédiée à la mémoire coloniale et à l'histoire de "
            "l'immigration. Financer un tiers-lieu queer et intersectionnel avec "
            "programmation culturelle. Réinvestir le barrage Vauban comme espace "
            "d'exposition pour les jeunes artistes. Créer un espace dédié à la culture "
            "hip-hop à l'Elsau. Développer une stratégie de la filière jeu vidéo "
            "(accompagnement des créateurs, game jams, festivals). Profiter de la "
            "rénovation du musée alsacien pour en faire une vitrine de la création "
            "alsacienne. Soutenir les tiers-lieux proposant des activités culturelles. "
            "Renouveler le matériel informatique des médiathèques. Mettre en place une "
            "plateforme municipale de Places suspendues avec critères d'attribution selon "
            "le quotient familial. Favoriser la gratuité et la tarification sociale des "
            "équipements culturels. Afficher les prix étudiants sur les communications "
            "institutionnelles. Faire entrer l'art à l'école en invitant les artistes. "
            "Harmoniser l'offre de cours de musique et danse entre CSC. Développer des "
            "jumelages entre musées et CSC pour faire sortir le musée de ses murs."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "evenements-creation": {
        "texte": (
            "Concevoir un Opéra populaire du Rhin : arrêter la course au gigantisme, "
            "rénovation moins coûteuse, augmenter les représentations, transférer le "
            "budget non employé vers d'autres projets culturels. Décentraliser la "
            "culture : sanctuariser les budgets des associations des QPV, redynamiser "
            "le Théâtre de Hautepierre, donner aux CSC les moyens de leurs missions. "
            "Développer des musées de rue dédiés à l'art urbain au Port du Rhin. "
            "Favoriser des espaces de pratique culturelle en plein air (scènes de rue, "
            "théâtre de verdure, kiosques). Mettre à disposition des lieux municipaux "
            "vacants aux artistes pour la création et la recherche. Développer la couleur "
            "dans la ville en impliquant les conseils de quartier. Balisage historique "
            "par QR code. Déployer un plan de lutte contre les violences dans le secteur "
            "culturel. Agir pour l'égalité de genre dans la culture en favorisant les "
            "programmations paritaires. Refuser tout recours à l'IA dans les productions "
            "artistiques municipales. Favoriser l'implication citoyenne en matière de "
            "programmation artistique. Promouvoir les droits culturels par une charte "
            "municipale de coopération."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # SPORT
    # =========================================================================
    "equipements-sportifs": {
        "texte": (
            "Etablir un plan de rénovation des bâtiments publics sportifs avec "
            "redistribution des subventions selon les besoins des quartiers. "
            "Renforcer l'accessibilité du Stade de la Meinau les soirs de match "
            "(TER, tram, vélo, parking). Refuser le naming par des marques des "
            "équipements sportifs municipaux et leur privatisation. Aménager des "
            "espaces de baignade dans l'Ill pour que les Strasbourgeois se "
            "réapproprient leur rivière. Mettre en place un Plan Baignade avec "
            "espaces gratuits dans les gravières et rivières (Herrenwasser, presqu'ile "
            "Malraux). Augmenter les places de baby nageurs dans les piscines "
            "municipales. Simplifier la vie administrative des clubs en les intégrant "
            "à la politique de soutien de proximité aux associations. Repenser la "
            "tonte raisonnée aux abords des stades pour éviter la perte de matériel."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "sport-pour-tous": {
        "texte": (
            "Améliorer la bourse municipale au sport pour les 4-17 ans adossée au "
            "quotient familial, avec politique incitative pour combler l'écart de "
            "pratique entre filles et garçons. Déployer des aires de street workout "
            "dans les espaces publics sous-dotés en concertation avec les habitants. "
            "Augmenter les créneaux d'apprentissage à la natation pour les jeunes "
            "pendant les vacances. Organiser des groupes non-mixtes d'initiation au "
            "football pour les filles sur le temps périscolaire. Construire une charte "
            "de lutte contre les discriminations dans le sport avec les clubs, assortie "
            "de formations municipales pour les bénévoles. Favoriser la pratique du "
            "handisport avec une juste part du budget. Repenser la Maison sport santé "
            "en refusant tout partenariat privé et en développant une offre sportive "
            "gratuite pour les enfants et personnes en ALD dans les QPV. Participer "
            "au rapport de force pour la liberté vestimentaire des femmes dans le sport."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # URBANISME
    # =========================================================================
    "amenagement-urbain": {
        "texte": (
            "Poursuivre la transformation de la M35 en boulevard intégré au tissu "
            "urbain en s'appuyant sur l'ADEUS. Transformer l'avenue du Rhin en accélérant "
            "le passage à 2x1 voie pour développer les mobilités alternatives. Faire "
            "appliquer l'arrêté municipal d'interdiction de la circulation des poids lourds "
            "entre 22h et 6h. Mettre en place un plan spécial pour l'éclairage des rues "
            "conciliant tranquillité et transition écologique (télégestion, LED, détecteurs "
            "de mouvement), priorisé par quartier en co-construction. Mettre à disposition "
            "plus de toilettes publiques avec agent en journée, ouvertes la nuit. "
            "Nommer prioritairement les infrastructures avec des noms de femmes et de "
            "personnalités racisées. Sortir de la répression du monde de la nuit et "
            "apporter des réponses au cas par cas conciliant droit au silence, droit à "
            "la fête et droit au travail de nuit. Installer des toilettes publiques aux "
            "déposes d'autocars touristiques. Reprendre l'étude du désenclavement "
            "d'Ostwald Mairie par une passerelle douce vers Baggersee."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "accessibilite": {
        "texte": (
            "Porter un objectif zéro lieu inaccessible (lieux publics, transports, "
            "commerces, crèches). Lancer un plan pluriannuel d'accessibilité des locaux "
            "et former les agents à l'accueil des personnes en situation de handicap. "
            "Refonder la politique anti-validiste en révisant la Charte Ville et Handicap "
            "(inchangée depuis 2011). Créer des commissions locales d'accessibilité. "
            "Favoriser les bourses à matériel médical et ateliers de réparation. "
            "Respecter les obligations d'emploi de personnes handicapées à tous niveaux "
            "de responsabilité. Garantir le choix entre démarche physique ou "
            "dématérialisée pour chaque service public."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "quartiers-prioritaires": {
        "texte": (
            "Renforcer les mairies de quartier comme relais de la démocratie municipale "
            "avec permanences mensuelles des élus, salles gratuites pour les réunions "
            "d'habitants et cahiers de doléances. Convoquer des états généraux sur les "
            "grands sujets (culture, sport, vie associative). Attention prioritaire aux "
            "QPV pour le soutien aux associations. Prioriser les besoins de mobilité "
            "des quartiers populaires dans le plan vélo et le tramway. Chaque année "
            "proposer des spectacles du FARSE dans un quartier prioritaire. Ancrage "
            "prioritaire dans les 9 QPV de Strasbourg."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # =========================================================================
    # SOLIDARITÉ
    # =========================================================================
    "aide-sociale": {
        "texte": (
            "Mettre en place la gratuité des 30 premiers m3 d'eau pour les plus "
            "précaires. Prendre des arrêtés municipaux d'interdiction des coupures "
            "d'eau et d'énergie. Favoriser l'ouverture d'épiceries solidaires via mise "
            "à disposition de locaux, expérimenter une épicerie municipale. Mettre en "
            "place un service public et gratuit des obsèques pour les personnes en "
            "précarité. Refuser les dispositifs anti-SDF (arrêtés anti-mendicité, "
            "mobilier anti-SDF). Garantir la domiciliation des personnes sans abri et "
            "développer le service de bagagerie. Mener une campagne annuelle sur "
            "l'accès aux droits et aides sociales. Proposer une simulation mesaides.gouv "
            "à tout nouvel arrivant. Mettre en place un coffre-fort numérique pour "
            "les pièces administratives des plus démunis. Rendre les services sociaux "
            "municipaux plus accessibles (horaires, effectifs) et mettre en place des "
            "écrivains publics et des interprètes. Soutenir les associations de "
            "prévention spécialisée : pérenniser le schéma eurométropolitain, permettre "
            "les recrutements, renforcer les moyens, étendre aux territoires non couverts. "
            "Organiser une permanence pour l'accès aux droits des personnes privées "
            "d'emploi et précarisées."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "egalite-discriminations": {
        "texte": (
            "Créer un Office Municipal contre les Discriminations regroupant observation, "
            "formation et action. Mettre en place un cycle de formation aux "
            "discriminations (racisme, sexisme, LGBTIphobies, validisme) pour les agents "
            "de la collectivité. Anonymiser les CV pour le recrutement. Constituer le "
            "maire en partie civile lors de tout dépôt de plainte pour racisme, sexisme "
            "ou LGBTIphobies. Créer un Observatoire communal contre le racisme, "
            "l'islamophobie et l'antisémitisme. Sensibiliser les enfants aux "
            "discriminations et au consentement dans les écoles. Créer un colloque "
            "national de lutte contre tous les racismes. Soutenir financièrement les "
            "associations antiracistes et LGBTI+. Faciliter les démarches des personnes "
            "trans dans les services municipaux (formulaires non genrés, usage du prénom "
            "choisi). Développer des lieux d'hébergement d'urgence pour les jeunes LGBTI+ "
            "en rupture familiale. Financer un monument commémoratif des victimes de "
            "LGBTIphobies. Soutenir les Marches des Fiertés. Organiser une commémoration "
            "du 180e anniversaire de l'abolition de l'esclavage avec pose d'une stèle. "
            "Cesser la chasse aux Roms : villages d'insertion, scolarisation, campagnes "
            "de santé, interdiction des expulsions sans relogement. Renommer certaines "
            "rues avec des noms de personnalités racisées. Développer les lieux et "
            "campagnes d'information sur la santé sexuelle et reproductive."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    "pouvoir-achat": {
        "texte": (
            "Gratuité des 30 premiers m3 d'eau par foyer. Adopter un plan de "
            "développement des énergies renouvelables avec tarif social et progressif "
            "de l'énergie via les coopératives citoyennes. Mettre le premier échelon "
            "de la tarification sociale à 0 euro pour tous les services publics "
            "municipaux (parking, transport, cantine). Intégrer une tarification "
            "étudiante au Quotient familial unique. Etablir un plan de lutte contre "
            "la précarité étudiante (encadrement des loyers, tarification sociale, "
            "gratuité des transports). S'opposer à la hausse des loyers des résidences "
            "universitaires et défendre le retour du repas à 1 euro au CROUS. "
            "Doubler le nombre de logements CROUS pour atteindre 10 000 places. "
            "Arrêtés municipaux d'interdiction des coupures d'eau et d'énergie."
        ),
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
}

# =============================================================================
# SOUS-THÈMES SPÉCIFIQUES À STRASBOURG À CRÉER
# =============================================================================

SOUS_THEMES_SPECIFIQUES = {
    "solidarite": [
        {
            "id": "accueil-migrants",
            "nom": "Accueil des personnes exilées",
            "proposition": {
                "texte": (
                    "Se porter commune volontaire pour l'accueil de personnes migrantes. "
                    "Pérenniser la T'rève (lieu d'accueil) et ouvrir d'autres lieux similaires. "
                    "Renforcer les dispositifs d'accompagnement : cours de français, soutien "
                    "administratif, actions socio-éducatives. Scolariser de façon inconditionnelle "
                    "tous les enfants quel que soit leur statut administratif. Développer les "
                    "parrainages républicains de personnes sans papiers. Former les agents de la "
                    "collectivité à l'accueil des publics en situation de précarité et aux enjeux "
                    "de la migration. Améliorer les dispositifs d'accès aux droits."
                ),
                "source": SOURCE,
                "sourceUrl": SOURCE_URL
            }
        },
        {
            "id": "protection-enfance",
            "nom": "Protection de l'enfance",
            "proposition": {
                "texte": (
                    "Intégrer la lutte contre l'inceste dans la politique municipale de "
                    "l'enfance avec campagne annuelle multi-supports. Faire du 19 novembre "
                    "(journée internationale des droits de l'enfant) une journée de mobilisation "
                    "locale. Déployer un plan de formation obligatoire pour tout personnel en "
                    "contact avec des mineurs centré sur le repérage des violences sexuelles. "
                    "Créer une cellule municipale d'écoute et de signalement avec point de "
                    "contact unique. Développer un plan d'urgence enfants à la rue. "
                    "Organiser une permanence pour le respect du droit du travail des "
                    "lycéens professionnels."
                ),
                "source": SOURCE,
                "sourceUrl": SOURCE_URL
            }
        },
        {
            "id": "paix-international",
            "nom": "Paix & Solidarité internationale",
            "proposition": {
                "texte": (
                    "Faire voter une motion pour condamner le génocide et défendre la paix "
                    "à Gaza. Suspendre le partenariat avec la ville de Ramat Gan avec "
                    "conditions de reprise. Développer des jumelages avec des communes "
                    "soutenant les peuples opprimés. Etoffer le jumelage avec le camp "
                    "palestinien d'Aida avec aide financière. Créer un réseau international "
                    "de communes antifascistes. S'engager dans des actions de plaidoyer "
                    "et de solidarité internationale."
                ),
                "source": SOURCE,
                "sourceUrl": SOURCE_URL
            }
        },
    ],
    "democratie": [
        {
            "id": "lutte-surtourisme",
            "nom": "Lutte contre le surtourisme",
            "proposition": {
                "texte": (
                    "Définir des quotas de meublés de tourisme dans le PLU. Limiter la "
                    "location touristique à 90 jours par an. Renforcer les contrôles avec "
                    "amendes de 10 000 à 20 000 euros. Informer les copropriétés de leur "
                    "droit d'interdire les meublés touristiques. Instaurer un péage pour les "
                    "autocars de tourisme avec obligation de réservation. Limiter les escales "
                    "de bateaux de croisière. Travailler avec les agences de voyage pour "
                    "désengorger l'hypercentre. Freiner les Free Tours au profit des "
                    "guides-conférenciers diplômés."
                ),
                "source": SOURCE,
                "sourceUrl": SOURCE_URL
            }
        },
    ],
    "economie": [
        {
            "id": "municipalisation",
            "nom": "Municipalisation des services",
            "proposition": {
                "texte": (
                    "Plan de municipalisation des services publics : reprendre en régie directe "
                    "l'usine de valorisation des déchets (Sénerval), la station d'épuration de "
                    "la Wantzenau, la production de repas scolaires. Planifier la reprise de "
                    "la DSP de valorisation énergétique. Mettre fin aux délégations de service "
                    "public aux entreprises privées dans les domaines essentiels (eau, énergie, "
                    "logement, transport, alimentation, santé, déchets). Créer un service de "
                    "R&D de l'ESS. Développer une offre publique pour les secteurs où l'offre "
                    "privée est défaillante."
                ),
                "source": SOURCE,
                "sourceUrl": SOURCE_URL
            }
        },
    ],
    "urbanisme": [
        {
            "id": "fracture-numerique",
            "nom": "Lutte contre la fracture numérique",
            "proposition": {
                "texte": (
                    "Garantir le choix entre démarche physique ou dématérialisée pour tout "
                    "service public. Faciliter l'accès à des écrivains publics dans les lieux "
                    "gérés par la ville. Développer des espaces d'accès à Internet "
                    "confidentiels et gratuits respectant la neutralité du net. Développer le "
                    "réseau de médiateurs numériques. Mettre en place un coffre-fort numérique "
                    "pour conserver les pièces administratives des plus démunis."
                ),
                "source": SOURCE,
                "sourceUrl": SOURCE_URL
            }
        },
    ],
    "sante": [
        {
            "id": "laicite-cultes",
            "nom": "Laïcité & Cultes",
            "proposition": {
                "texte": (
                    "Favoriser un climat de dialogue et de coopération interreligieuse. "
                    "Garantir des relations apaisées et une égale considération envers "
                    "les cultes concordataires ou non. Utiliser les baux emphytéotiques "
                    "ou l'accompagnement administratif pour permettre à chaque culte "
                    "d'exercer dans des lieux dignes."
                ),
                "source": SOURCE,
                "sourceUrl": SOURCE_URL
            }
        },
    ],
}


def main():
    # Charger le JSON
    print(f"Chargement de {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Obtenir la liste des IDs de candidats depuis les données
    candidat_ids = [c["id"] for c in data["candidats"]]

    # Compteurs
    mises_a_jour = 0
    ajoutees = 0
    sous_themes_crees = 0

    # 1) Mettre à jour les propositions dans les sous-thèmes existants
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in PROPOSITIONS:
                st["propositions"][CANDIDAT_ID] = PROPOSITIONS[st_id]
                mises_a_jour += 1
                print(f"  [MAJ] {cat['id']}/{st_id}")

    # 2) Créer les sous-thèmes spécifiques et y ajouter les propositions
    # Fusionner les listes pour les catégories qui apparaissent plusieurs fois
    sous_themes_par_cat = {}
    for cat_id, st_list in SOUS_THEMES_SPECIFIQUES.items():
        if cat_id not in sous_themes_par_cat:
            sous_themes_par_cat[cat_id] = []
        sous_themes_par_cat[cat_id].extend(st_list)

    for cat in data["categories"]:
        cat_id = cat["id"]
        if cat_id in sous_themes_par_cat:
            for new_st in sous_themes_par_cat[cat_id]:
                # Vérifier si le sous-thème existe déjà
                existing = [s for s in cat["sousThemes"] if s["id"] == new_st["id"]]
                if existing:
                    # Mettre à jour la proposition existante
                    existing[0]["propositions"][CANDIDAT_ID] = new_st["proposition"]
                    mises_a_jour += 1
                    print(f"  [MAJ SPEC] {cat_id}/{new_st['id']}")
                else:
                    # Créer le sous-thème
                    propositions = {cid: None for cid in candidat_ids}
                    propositions[CANDIDAT_ID] = new_st["proposition"]
                    cat["sousThemes"].append({
                        "id": new_st["id"],
                        "nom": new_st["nom"],
                        "propositions": propositions
                    })
                    sous_themes_crees += 1
                    ajoutees += 1
                    print(f"  [NEW] {cat_id}/{new_st['id']}")

    # 3) Compter le total des propositions Kobryn
    total_propositions = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["propositions"].get(CANDIDAT_ID) is not None:
                total_propositions += 1

    # 4) Mettre à jour programmeComplet et URL
    for candidat in data["candidats"]:
        if candidat["id"] == CANDIDAT_ID:
            candidat["programmeComplet"] = True
            candidat["programmeUrl"] = "https://www.kobryn2026.eu/"
            candidat["programmePdfPath"] = "data/programmes/kobryn-strasbourg-programme.pdf"
            print(f"\nprogrammeComplet = True")
            break

    # Résumé
    print(f"\n{'='*50}")
    print(f"RÉSUMÉ INTÉGRATION KOBRYN")
    print(f"{'='*50}")
    print(f"Sous-thèmes existants mis à jour : {mises_a_jour}")
    print(f"Sous-thèmes spécifiques créés : {sous_themes_crees}")
    print(f"Total sous-thèmes avec proposition Kobryn : {total_propositions}")
    print(f"{'='*50}")

    # Compter les mesures approximatives (en comptant les phrases)
    total_mesures = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            prop = st["propositions"].get(CANDIDAT_ID)
            if prop is not None:
                # Compter approximativement les mesures (phrases terminées par .)
                texte = prop["texte"]
                mesures = len([s for s in texte.split(". ") if len(s) > 10])
                total_mesures += mesures
                print(f"  {cat['id']}/{st['id']}: ~{mesures} mesures")

    print(f"\nTotal estimé de mesures : ~{total_mesures}")

    # Sauvegarder
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nFichier sauvegardé : {JSON_PATH}")
    print("DONE.")


if __name__ == "__main__":
    main()
