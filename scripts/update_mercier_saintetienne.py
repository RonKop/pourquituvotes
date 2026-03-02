#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intègre les propositions de Valentine Mercier (Saint-Étienne, LFI) extraites
du programme PDF officiel « Plus de 400 mesures pour changer Saint-Étienne »
(25 pages, 26 chapitres).

Source primaire : mercier2026.fr
"""

import json
import os
import sys

# Windows UTF-8 fix
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "saint-etienne-2026.json")

SRC = "Programme Valentine Mercier, Saint-Étienne insoumise, 2026"
SRC_URL = "https://mercier2026.fr/"

# ═══════════════════════════════════════════════════════════════════════════
# PROPOSITIONS extraites du PDF (25 pages, 26 chapitres)
# Chaque clé = ID de sous-thème, valeur = liste de mesures reformulées
# ═══════════════════════════════════════════════════════════════════════════

PROPOSITIONS = {
    # ── SÉCURITÉ ──────────────────────────────────────────────────────────
    "police-municipale": [
        "Recentrer la police municipale sur ses missions de proximité et de tranquillité publique (application des arrêtés municipaux, constatation d'infractions), sans armement létal.",
        "Redéployer les équipes de police municipale dans chaque quartier, à pied et à vélo, sur des plages horaires étendues, avec réouverture d'antennes de proximité.",
        "Former les agents de la police municipale à la désescalade, aux questions de genre, aux enjeux de santé mentale et à l'accueil des personnes LGBTIQI+.",
        "Créer des conseils de secteur de la tranquillité publique réunissant habitants, commerçants, associations, police nationale et police municipale dans chaque quartier.",
    ],

    "videoprotection": [
        "Instaurer un moratoire sur la vidéosurveillance : aucune nouvelle caméra durant le mandat, non-remplacement des caméras hors service, utilisation limitée à la levée de doute.",
        "Refuser toute utilisation d'outils algorithmiques et de reconnaissance faciale sur la voie publique.",
    ],

    "prevention-mediation": [
        "Déployer des médiateurs de rue (jour et nuit) et des éducateurs spécialisés de rue pour aller vers la jeunesse.",
        "Développer les emplois de médiation scolaire et soutenir les clubs de prévention.",
        "Lancer des campagnes de sensibilisation et de lutte contre les addictions (protoxyde d'azote, stupéfiants) en articulation avec la police nationale.",
    ],

    "violences-femmes": [
        "Créer ou soutenir des lieux d'accueil d'urgence pour les femmes victimes de violences, avec ou sans enfant, en partenariat avec les acteurs compétents.",
        "Soutien renforcé aux associations féministes et de lutte contre les violences conjugales (SOS Violences Conjugales 42, Planning Familial, etc.).",
        "Constitution de la Maire en partie civile en cas de procès pour discrimination.",
    ],

    # ── TRANSPORTS ────────────────────────────────────────────────────────
    "transports-en-commun": [
        "Augmenter l'amplitude horaire, le réseau et les fréquences des bus, avec création de voies réservées et interdiction stricte du stationnement sur les trajets de bus.",
        "Étudier le prolongement de la ligne BHNS M6+ jusqu'à Montreynaud et passer les lignes 10 et 16 en lignes M.",
        "Préparer le retour en régie publique de la STAS à l'échéance de la délégation de service public avec Transdev.",
        "Interdire le dépassement des bus aux arrêts par aménagement de la chaussée.",
        "Plaider au niveau national pour un doublement du plafond du versement transport des entreprises.",
    ],

    "velo-mobilites-douces": [
        "Investir 35 millions d'euros sur le mandat pour un réseau de voies cyclables continu, sécurisé et connecté (doublement par rapport au mandat précédent).",
        "Déployer une signalétique dédiée au réseau cyclable pour une meilleure lisibilité et priorisation des mobilités douces.",
        "Installer massivement du mobilier urbain dédié aux vélos (stationnement, racks).",
        "Encourager la création de structures de réparation et d'entretien de vélos dans chaque quartier.",
        "Étendre le réseau Vélivert et améliorer sa maintenance.",
        "Créer des espaces d'apprentissage libre sécurisés pour les mobilités douces sur l'espace public.",
    ],

    "pietons-circulation": [
        "Systématiser la priorité piétonne aux feux (traversée en 3 secondes, temps adapté aux plus fragiles, traversées diagonales).",
        "Mettre aux normes tous les passages piétons d'ici fin 2026 pour les personnes malvoyantes, à mobilité réduite, âgées et les enfants.",
        "Rendre les trottoirs accessibles (minimum 2 mètres de large, matériaux non glissants, déplacement des obstacles).",
        "Piétonniser le centre-ville : remise en service et extension du plateau piéton, création d'une magistrale piétonne entre Le Clapier et Châteaucreux.",
        "Créer des rues scolaires apaisées avec piétonnisation des accès aux écoles.",
        "Extension du 30 km/h à l'ensemble de la ville hors grands axes pénétrants et structurants.",
        "Rétrécir les chaussées à 2,5 m maximum pour empêcher les survitesses et libérer de l'espace pour piétons et vélos.",
        "Négocier le passage de la RN88 à 50 km/h entre Solaure et Terrenoire.",
    ],

    "stationnement": [
        "Gratuité du stationnement toute la journée le samedi à l'extérieur du boulevard urbain.",
        "Sanctuariser et augmenter les places de livraison et de stationnement professionnel (artisans, métiers du soin).",
        "Créer de nouveaux parkings relais le long du boulevard urbain intégrant des parcs à vélos.",
        "Refondre la tarification du stationnement en prenant en compte le poids et le gabarit des véhicules (surcoût pour les SUV).",
        "Tolérance zéro pour les stationnements dangereux sur les pistes cyclables et arrêts de bus.",
    ],

    "tarifs-gratuite": [
        "Instaurer la gratuité des transports en commun le week-end pour soutenir la mobilité vers les lieux culturels, sportifs et les commerces.",
        "Viser à terme la gratuité totale des transports, via le doublement du versement transport.",
    ],

    # ── LOGEMENT ──────────────────────────────────────────────────────────
    "logement-social": [
        "Relancer la production de logement public et social en priorisant la rénovation de l'existant, avec un objectif de 40 % de logement social d'ici 2040 (doublement).",
        "Insérer des servitudes de logement social dans le PLUi en cours d'élaboration.",
        "Relancer la production de logement social étudiant et senior en lien avec le CROUS.",
        "Imposer 20 % de logements accessibles PMR par opération neuve (et non au global).",
        "Développer l'accession sociale non spéculative via le Bail Réel Solidaire (BRS) et les Offices Fonciers Solidaires.",
        "Soutenir les projets de logement participatif, autoporté et autogéré.",
    ],

    "logements-vacants": [
        "Réquisitionner les logements vacants pour la mise à l'abri de familles en urgence (logements communaux et publics en priorité).",
        "Créer des places pérennes d'hébergement d'urgence et de réinsertion sociale avec capacité d'extension rapide.",
    ],

    "encadrement-loyers": [
        "Mettre en place le permis de louer avec une brigade dédiée pour contrôler la salubrité et la décence de tout logement mis en location.",
        "Poursuivre les opérations de rénovation des quartiers anciens (ORI, OPAH-RU) pour lutter contre l'habitat insalubre.",
        "Adopter une charte de bonnes pratiques environnementales avec les bailleurs et promoteurs, avec un service de contrôle dédié.",
    ],

    "acces-logement": [
        "Créer une cellule de défense des droits des locataires avec une brigade du logement pour visiter les logements à la demande.",
        "Réserver du foncier au logement étudiant et à destination des jeunes actifs.",
    ],

    # ── ÉDUCATION ─────────────────────────────────────────────────────────
    "petite-enfance": [
        "Développer le service public local de la petite enfance pour permettre à 100 % des parents d'obtenir une place (crèches, multi-accueils, relais assistantes maternelles).",
        "Arrêter de recourir aux opérateurs privés lucratifs pour les crèches, au profit de structures publiques et associatives.",
        "Créer un guichet unique de demande de place en crèche pour plus de transparence et de rapidité.",
        "Favoriser l'accueil des enfants handicapés dans les crèches publiques avec personnels spécialisés.",
        "Créer une crèche supplémentaire en centre-ville (site de la Charité à l'étude).",
        "Soutenir et développer l'accompagnement à la parentalité dans les équipements municipaux.",
        "Améliorer les aires de jeux pour les rendre naturelles, intergénérationnelles et accessibles aux enfants handicapés.",
    ],

    "ecoles-renovation": [
        "Réaliser un diagnostic global du bâti scolaire (amiante, classes surchargées, chauffage, usages souhaités).",
        "Sanctuariser 60 millions d'euros minimum sur le mandat pour la rénovation lourde des écoles publiques et la construction de nouvelles écoles.",
        "Transformer les cours d'école en cours oasis végétalisées et ombragées, co-construites avec les enfants.",
        "Augmenter d'au moins 50 % le nombre d'ATSEM, en priorisant les écoles REP et REP+.",
    ],

    "cantines-fournitures": [
        "Instaurer la gratuité des cantines pour les plus précaires dès la rentrée 2026, puis pour tous d'ici la fin du mandat.",
        "Atteindre 100 % de produits bio ou durables, locaux et de saison dans les cantines scolaires.",
        "Instaurer 2 journées végétariennes par semaine et garantir l'option végétarienne quotidienne.",
        "Retour en régie publique de la cantine à l'horizon 2031 (fin de la DSP Élior).",
        "Objectif de relocalisation des cuisines dans chaque école à l'horizon 2031.",
        "Objectif zéro plastique dans les cantines et les réceptions municipales.",
        "Gratuité des fournitures scolaires allouées à tous les élèves.",
        "Allouer 300 000 euros minimum par an pour les projets pédagogiques des écoles publiques.",
    ],

    "periscolaire-loisirs": [
        "Garantir un accueil périscolaire inconditionnel matin et soir dans chaque école.",
        "Augmenter et améliorer l'encadrement des enfants sur le temps méridien avec du personnel dédié et formé.",
        "Revaloriser les conseils d'école et impliquer les établissements au sein des conseils de quartier.",
        "Retour du prêt enseignant gratuit dans les bibliothèques et gratuité d'accès aux services municipaux dans le cadre scolaire.",
        "Fin du financement non-obligatoire des établissements privés sous contrat.",
    ],

    "jeunesse": [
        "Lancer un grand plan pour la jeunesse avec financement de postes d'animateurs et d'éducateurs professionnels pour les 12-17 ans.",
        "Rouvrir des espaces jeunesse 12-17 ans avec accueil en soirée, le samedi et une présence hors les murs.",
        "Expérimenter des cantines populaires à proximité des universités pour pallier l'absence de restauration universitaire.",
        "Expérimenter l'ouverture d'équipements publics en soirée pour les jeunes et les associations (gymnases, maisons de quartier).",
    ],

    # ── ENVIRONNEMENT ─────────────────────────────────────────────────────
    "espaces-verts": [
        "Végétaliser et reboiser la ville : protéger les arbres existants, créer des continuités végétales, planter massivement pour rafraîchir le milieu urbain.",
        "Planter des essences comestibles productives (vergers urbains) notamment à proximité des écoles.",
        "Créer un parc urbain sur le site de la Charité, maximisant la part végétalisée.",
        "Créer un parc humide le long du Furan dans le quartier de la Rivière en valorisant la friche Peugeot.",
        "Replanter des haies sur les terres agricoles municipales et les classer dans le PLU.",
        "Aménager des espaces refuges pour les animaux sauvages et maintenir des friches favorables à la biodiversité.",
    ],

    "proprete-dechets": [
        "Soutenir les ressourceries, lieux de réparation et de réemploi.",
        "Refuser le projet d'incinérateur à Unieux, préférer le partage des déchets avec l'incinérateur Lyon-Gerland en sous-régime, via le rail de nuit.",
        "Fixer un objectif de réduction de 50 % de la consommation de produits d'origine animale d'ici 2032 dans la politique alimentaire urbaine.",
        "Récupérer les eaux de pluie pour le nettoyage des rues.",
    ],

    "climat-adaptation": [
        "Adopter un plan canicule avec recensement et création de lieux d'accueil adaptés pour les personnes vulnérables.",
        "Exiger la sobriété foncière renforcée : éviter d'urbaniser toute parcelle non bâtie, privilégier la requalification des friches.",
        "Valoriser les toitures comme « cinquième façade » : obligation dans le PLUi de végétalisation, production énergétique ou espaces d'agrément pour les constructions neuves.",
        "Réaliser dès la première année un diagnostic écologique citoyen du territoire.",
        "Faire de la biodiversité un critère d'analyse de tous les projets et actions de la ville.",
        "Valoriser les friches industrielles : dépollution et renaturation ou reconstruction sur terrains déjà artificialisés (objectif Zéro Artificialisation).",
        "Bannir tous les produits phytosanitaires et toxiques sur le territoire communal.",
    ],

    "renovation-energetique": [
        "Lancer un grand plan de rénovation thermique du parc public pour réduire les charges locatives et la consommation d'énergie.",
        "Améliorer l'habitat en centre ancien avec des opérations de rénovation garantissant le confort thermique été comme hiver.",
    ],

    "alimentation-durable": [
        "Créer des espaces tests agricoles et des outils mutualisés de production et transformation pour les jeunes paysans (maraîchage bio).",
        "Étudier la réouverture des serres municipales et l'ouverture d'une ferme en régie publique.",
        "Protéger et augmenter les terres agricoles par transfert de zonages vers le A (agricole) dans le PLUi.",
        "Mener une politique d'acquisition de foncier agricole pour favoriser la création de petites unités de maraîchage.",
        "Aider à l'installation d'épiceries locales, biologiques, vrac ou solidaires.",
        "Soutenir les initiatives d'entraide alimentaire (association VRAC, expérimentation de Caisse Sociale de l'Alimentation).",
        "Intégrer des critères éthiques liés au bien-être animal dans les marchés publics (exclusion élevage sans plein air, pisciculture intensive, foie gras).",
    ],

    # ── SANTÉ ─────────────────────────────────────────────────────────────
    "centres-sante": [
        "Créer un premier centre de soins municipal inclusif avec médecins salariés, portant aussi des politiques de prévention.",
        "Faciliter l'installation de professionnels libéraux dans des cabinets collectifs de santé clé en main pour lutter contre la désertification médicale.",
    ],

    "prevention-sante": [
        "Dynamiser le contrat local de santé et le contrat de santé mentale en concertation avec les acteurs (associations, médecins, préfecture, département).",
        "Former la police municipale aux enjeux de santé mentale (plus de 30 % des interventions concernent des personnes en crise psychiatrique).",
        "Expérimenter une intermédiation vers le dispositif MonPsy avec avance d'honoraires pour des consultations psychologiques.",
        "Soutien renforcé aux associations locales de santé sexuelle (Planning Familial, Enipse, Aides).",
        "Lancer des campagnes de lutte contre les addictions (protoxyde d'azote, stupéfiants).",
    ],

    "seniors": [
        "Mettre en place un service d'aide aux aidants avec 8 sessions de formation gratuites par an.",
        "Créer une Maison des aînés et aidants regroupant tous les services pour les seniors.",
        "Poser les bases d'un service non lucratif d'aide à la personne par articulation des acteurs non lucratifs.",
        "Ouvrir la restauration scolaire aux groupes de personnes âgées une fois par mois pour des échanges intergénérationnels.",
        "Soutenir les projets de logements sociaux partagés adaptés pour les seniors, avec normes d'accessibilité dès la construction.",
        "Favoriser les colocations seniors ou seniors-étudiants et le logement partagé.",
        "Intégrer usagers et associations aux conseils d'administration des EHPAD pour un contrôle citoyen.",
    ],

    # ── DÉMOCRATIE ────────────────────────────────────────────────────────
    "budget-participatif": [
        "Ouvrir la participation aux votations et commissions dès 16 ans et quelle que soit la nationalité.",
        "Instaurer un Référendum d'Initiative Citoyenne (RIC) municipal dès qu'une pétition réunit 10 % des habitants.",
        "Créer un droit de saisine du conseil municipal par pétition citoyenne (seuil de 5 % des habitants).",
        "Doubler le nombre de quartiers et de conseils de quartier, avec budget de fonctionnement et d'investissement propre.",
        "Redéfinir les conseils de quartier avec collèges (associations, acteurs culturels, économiques, habitants), tirage au sort pour moitié, garde d'enfant et transport gratuits.",
        "Créer des commissions thématiques consultatives municipales ouvertes aux associations, chercheurs et habitants.",
        "Donner une voix délibérative aux citoyens et associations dans les instances de projet et les commissions consultatives des services publics locaux.",
        "Instaurer un référendum révocatoire à partir de la mi-mandat sur pétition de 10 % du corps électoral.",
    ],

    "transparence": [
        "Non-cumul des mandats et des fonctions exécutives entre Mairie et Métropole.",
        "Publier le budget prévisionnel et rendre transparents les critères d'attribution des subventions.",
        "Baisser l'indemnité de la Maire (plafond à 3 500 euros net vs 7 100 euros cumulés précédemment).",
        "Publier les indemnités des élus, les rendez-vous avec les représentants d'intérêts privés et refuser tout cadeau d'entreprise.",
        "Réaliser une cartographie des risques de corruption et un code de conduite anticorruption avec référent déontologue indépendant.",
        "Limiter le recours aux consultants privés en privilégiant les expertises universitaires et d'agences publiques.",
    ],

    "vie-associative": [
        "Instaurer des financements pluriannuels aux associations et amicales sur la base de leur propre projet, avec garantie d'indépendance.",
        "Publier annuellement la liste de toutes les subventions versées avec critères d'attribution transparents.",
        "Apporter un soutien administratif aux associations pour l'ingénierie financière et la recherche de subventions.",
        "Lancer un plan de rénovation des amicales laïques et du bâti municipal à destination des associations.",
        "Soutenir les associations de protection animale par le financement et la mise à disposition de locaux municipaux.",
        "Soutenir les associations de lutte contre les discriminations, notamment de testing.",
    ],

    "services-publics": [
        "Préparer le retour en régie publique de l'eau à l'échéance de la DSP avec la SAUR, avec tarification progressive (15 premiers m3 gratuits, gaspillage surfacturé).",
        "Créer un service public funéraire municipal pour une inhumation digne et à tarification accessible.",
        "Sortir progressivement de la dépendance aux GAFAM : privilégier les solutions numériques libres, écologiquement responsables et françaises ou européennes.",
        "Réaliser un audit général des services municipaux pour identifier les risques psychosociaux et ajuster l'organisation du travail.",
        "Mettre en place le projet Territoire Zéro Non-Recours (TZNR) décentralisé via les centres sociaux pour lutter contre le non-recours aux droits.",
    ],

    # ── ÉCONOMIE ──────────────────────────────────────────────────────────
    "commerce-local": [
        "Interdire les nouvelles grandes surfaces commerciales dans le PLUi.",
        "Supprimer progressivement les panneaux publicitaires dans l'espace public.",
        "Étendre le périmètre de préemption commerciale aux quartiers non centraux pour prévenir la désertification commerciale.",
        "Aider à l'installation de commerces indépendants écologiquement et socialement responsables (vrac, bio, local).",
        "Revitaliser le centre-ville en utilisant les espaces vides pour l'artisanat, l'art, les associations et l'ESS.",
        "Doubler la taxe sur les commerces vacants dont l'inaction du propriétaire est confirmée.",
        "Faciliter les initiatives d'animation de quartier avec appui logistique de la ville.",
        "Proposer des baux progressifs (loyers faibles au démarrage, puis indexés sur le chiffre d'affaires) pour les commerces.",
        "Prioriser les marchands alimentaires et produits locaux sur les marchés.",
    ],

    "emploi-insertion": [
        "Intégrer l'initiative Territoire Zéro Chômeur Longue Durée (projet prêt à démarrer à Montreynaud).",
        "Soutenir les projets coopératifs (SCOP, SCIC) avec information renforcée et appui administratif et juridique.",
        "Intégrer systématiquement des clauses d'insertion sociale et des exigences écologiques dans les marchés publics.",
        "Créer une foncière économique et commerciale pour préserver les terrains et bâtiments industriels et soutenir l'ESS.",
        "Remettre en place la commission économique consultative métropolitaine avec les organisations syndicales et patronales.",
    ],

    "attractivite": [
        "Optimiser le foncier d'activité existant pour limiter l'artificialisation des sols dans une logique de sobriété foncière.",
        "Mettre fin aux campagnes publicitaires d'attractivité coûteuses et aux constructions de prestige inutiles.",
        "Suppression des financements à l'aéroport d'Andrézieux-Bouthéon, chroniquement déficitaire.",
        "Se mobiliser auprès des partenaires pour le retour d'une connexion ferroviaire à Clermont-Ferrand (réouverture Boën-sur-Lignon – Thiers).",
    ],

    # ── CULTURE ───────────────────────────────────────────────────────────
    "equipements-culturels": [
        "Organiser des Assises de la culture dans les quartiers pour identifier les besoins en production, diffusion et formation.",
        "Faciliter l'installation d'une ou plusieurs friches artistiques autogérées (ateliers, locaux de répétition, salles de diffusion).",
        "Créer des postes de médiation culturelle de proximité pour mettre en lien cultures populaires et savantes.",
        "Déménager le Conservatoire Massenet dans un nouveau bâtiment à La Charité.",
        "Étendre le dispositif de classes orchestres et souscrire au dispositif DEMOS (prêt d'instruments gratuit aux enfants de quartiers prioritaires).",
        "Instaurer la gratuité des médiathèques pour tous.",
        "Rénover la médiathèque de Tarentaize et redéfinir son accessibilité en transports en commun.",
        "Étudier la réunion de la médiathèque de Carnot avec la biblio-matériauthèque de la Cité du Design.",
    ],

    "evenements-creation": [
        "Créer un Laboratoire des récits stéphanois : programme de collecte et mise en récit des mémoires ouvrières, migratoires et populaires.",
        "Mobiliser les outils culturels et artistiques au service de la démocratie via des résidences artistiques de long terme dans les quartiers.",
    ],

    # ── SPORT ─────────────────────────────────────────────────────────────
    "equipements-sportifs": [
        "Réaliser un diagnostic global des équipements sportifs pour prioriser le programme de rénovation en fonction de la vétusté et des besoins.",
        "Lancer une rénovation lourde des équipements sportifs de proximité (gymnases, terrains extérieurs).",
        "Maintenir ouvertes les piscines existantes et créer une ou plusieurs piscines naturelles ou bassins de baignade urbains surveillés.",
    ],

    "sport-pour-tous": [
        "Développer des animations physiques intergénérationnelles dans les quartiers pour lutter contre la sédentarité et l'isolement.",
        "Créer des aires de fitness seniors à proximité des jeux d'enfants.",
    ],

    # ── URBANISME ─────────────────────────────────────────────────────────
    "amenagement-urbain": [
        "Aménager le site de la Charité : parc urbain, ouverture piétonne et cycliste, équipements publics à vocation sociale et culturelle, aucune privatisation résidentielle.",
        "Réhabiliter la Bourse du Travail pour lui rendre sa fonction d'outil pour les travailleurs, en collaboration avec les syndicats.",
        "Reprendre intégralement la plateforme du tramway entre Place du Peuple et Carnot, avec étude de faisabilité pour maintenir le tramway pendant les travaux.",
        "Mettre en valeur le Furan dans le quartier de la Rivière par un parc humide avec relocalisation concertée des entreprises le long du lit.",
        "Restructurer le parking des Ursules : démolition partielle pour recréer un espace public de qualité, conservation des niveaux souterrains.",
        "Poursuivre les études de la place Massenet pour en faire un véritable pôle multimodal et espace de vie de quartier.",
        "Penser la ville à hauteur d'enfants et d'aînés : plus de bancs le long des itinéraires piétons, espaces ludiques co-construits, espaces pour les adolescents.",
    ],

    "accessibilite": [
        "Repenser en profondeur la commission communale pour l'accessibilité avec des personnes concernées, un numéro vert et un outil numérique de signalement.",
        "Améliorer l'accessibilité des lieux publics pour les personnes handicapées, avec soutien aux petites structures n'ayant pas les moyens.",
        "Développer les marches exploratoires sous le prisme des différentes discriminations pour identifier les aménagements nécessaires.",
    ],

    "quartiers-prioritaires": [
        "Lutter activement contre la ségrégation spatiale par la relocalisation de services publics et de commerces dans les quartiers populaires.",
        "Redéfinir l'offre de transports en commun pour mieux desservir les quartiers populaires.",
    ],

    # ── SOLIDARITÉ ────────────────────────────────────────────────────────
    "aide-sociale": [
        "Créer un guichet municipal d'accès aux droits (domiciliation rapide, accompagnement numérique, accès aux soins).",
        "Mettre en place des contrats territoriaux d'accueil et d'intégration en co-construction avec la préfecture.",
        "Créer une carte municipale d'habitant ouvrant l'accès aux équipements et services municipaux et le droit de participer aux votations.",
        "Mettre à disposition des bâtiments municipaux pour loger les demandeurs d'asile en mobilisant la vacance du parc public.",
        "Sécuriser le parcours des publics hors conventionnement en mobilisant la vacance structurelle du parc social via intermédiation locative.",
        "Évaluer la faisabilité d'un soutien financier aux hôtes solidaires via un coupon pour la sécurité sociale de l'alimentation.",
        "Mobiliser les fonds européens dédiés aux personnes exilées pour soulager les dispositifs non spécialisés.",
    ],

    "egalite-discriminations": [
        "Créer un bureau des discriminations composé de personnes concernées et de spécialistes pour accompagner les victimes (écoute, soutien juridique, signalement).",
        "Réaliser un audit des pratiques d'accueil dans les services municipaux (mairie, CCAS, maisons de quartier).",
        "Élaborer une budgétisation sensible au genre pour évaluer l'égalité d'accès des femmes aux politiques publiques.",
        "Adopter une charte de nomination des noms de rues pour une réelle représentativité de toutes et tous.",
        "Signer la charte d'engagement LGBTQI+ de L'Autre Cercle.",
        "Soutien renforcé aux associations LGBTQIA++ (TransAide, le Refuge, etc.).",
        "Interdire les cirques exploitant des animaux sauvages et toute exploitation d'animaux sauvages à des fins de représentation sur le territoire communal.",
    ],

    "pouvoir-achat": [
        "Instaurer un salaire plancher de 1 600 euros net pour les agents municipaux dès janvier 2027.",
        "Payer trois jours de carence par an aux agents municipaux dès 2027.",
        "Proposer le congé paternité de 10 semaines et le congé menstruel pour les agents municipaux.",
        "Proposer une part de rémunération en monnaie locale (LIEN) sur base du volontariat (jusqu'à 10 % bonifié).",
        "Organiser les États généraux de la dignité pour une réponse collective autour du droit au toit, à l'accès aux droits et à l'insertion.",
        "Lutte contre la pollution lumineuse : extinction nocturne des enseignes commerciales et de l'éclairage public de minuit à 6h, avec éclairage à la demande.",
    ],
}

# ═══════════════════════════════════════════════════════════════════════════


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    added = 0
    nb_mesures_total = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            sid = st["id"]
            if sid in PROPOSITIONS:
                mesures = PROPOSITIONS[sid]
                nb_mesures_total += len(mesures)
                old = st["propositions"].get("mercier")

                st["propositions"]["mercier"] = {
                    "source": SRC,
                    "sourceUrl": SRC_URL,
                    "mesures": mesures,
                }

                if old is None:
                    added += 1
                    print(f"  + {sid}: AJOUTÉ ({len(mesures)} mesures)")
                else:
                    updated += 1
                    old_count = len(old.get("mesures", [])) if isinstance(old, dict) else 0
                    print(f"  ~ {sid}: MIS À JOUR ({old_count} -> {len(mesures)} mesures)")

    # Mettre à jour le candidat
    for c in data["candidats"]:
        if c["id"] == "mercier":
            c["programmeComplet"] = True
            c["programmeUrl"] = "https://mercier2026.fr/"
            print(f"\n  programmeComplet -> true")
            print(f"  programmeUrl -> https://mercier2026.fr/")
            break

    # Sauvegarder
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Vérifier les sous-thèmes non couverts
    couverts = set(PROPOSITIONS.keys())
    tous_st = set()
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            tous_st.add(st["id"])

    non_couverts = tous_st - couverts
    non_existants = couverts - tous_st

    print(f"\n{'='*60}")
    print(f"  RÉSUMÉ Valentine Mercier (Saint-Étienne)")
    print(f"{'='*60}")
    print(f"  Sous-thèmes couverts : {len(couverts)}/44")
    print(f"  Mesures totales : {nb_mesures_total}")
    print(f"  Ajoutés : {added}, Mis à jour : {updated}")

    if non_couverts:
        print(f"\n  Sous-thèmes non couverts ({len(non_couverts)}):")
        for s in sorted(non_couverts):
            print(f"    - {s}")

    if non_existants:
        print(f"\n  ATTENTION - sous-thèmes inexistants dans le JSON ({len(non_existants)}):")
        for s in sorted(non_existants):
            print(f"    - {s}")

    print(f"\n  Fichier sauvegardé : {JSON_PATH}")


if __name__ == "__main__":
    main()
