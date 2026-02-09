#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Grenoble dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== GRENOBLE ===")
insert_city(
    ville_id="grenoble",
    ville_nom="Grenoble",
    ville_cp="38000",
    candidats=[
        {"id": "ruffin", "nom": "Laurence Ruffin", "liste": "Oui Grenoble (EELV/PS/PCF/G\u00e9n\u00e9ration.s)", "programmeUrl": "https://oui-grenoble.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "carignon", "nom": "Alain Carignon", "liste": "R\u00e9concilier Grenoble (LR/Renaissance)", "programmeUrl": "https://reconciliergrenoble.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "gerbi", "nom": "Herv\u00e9 Gerbi", "liste": "Nous Grenoble (Horizons)", "programmeUrl": "https://www.hervegerbi.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "brunon", "nom": "Allan Brunon", "liste": "Faire mieux pour Grenoble (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "gentil", "nom": "Romain Gentil", "liste": "Grenoble Capitale Citoyenne (PRG/Place Publique)", "programmeUrl": "https://grenoble-capitale-citoyenne.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "gabriac", "nom": "Valentin Gabriac", "liste": "Grenoble Capitale des Alpes (RN/UDR)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "belaid", "nom": "Nadia Bela\u00efd", "liste": "Grenoble Alpes Collectif (citoyenne)", "programmeUrl": "https://www.grenoblealpescollectif.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "anglade", "nom": "Baptiste Anglade", "liste": "NPA-R\u00e9volutionnaires", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "brun", "nom": "Catherine Brun", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Ruffin (EELV/PS/PCF) ---
        ("securite", "police-municipale", "ruffin"): (
            "Cr\u00e9ation d'une police municipale de quartier renforc\u00e9e par 50 agents suppl\u00e9mentaires, ax\u00e9e sur la proximit\u00e9 et la pr\u00e9vention",
            "Place Gre'net, janvier 2026",
            "https://www.placegrenet.fr/2026/01/19/cameras-policiers-municipaux-rsa-jeune-ce-que-revele-la-fuite-du-projet-de-laurence-ruffin-pour-grenoble/669616"
        ),
        ("securite", "prevention-mediation", "ruffin"): (
            "Approche ax\u00e9e sur la pr\u00e9vention et la m\u00e9diation de proximit\u00e9 dans tous les quartiers de la ville",
            "Place Gre'net, septembre 2025",
            "https://www.placegrenet.fr/2025/09/25/cooperation-protection-et-sante-les-priorites-de-laurence-ruffin-candidate-aux-municipales-a-grenoble/660653"
        ),
        ("transports", "tarifs-gratuite", "ruffin"): (
            "Gratuit\u00e9 des transports en commun le week-end pour acc\u00e9der au centre-ville et \u00e0 la montagne",
            "T\u00e9l\u00e9Grenoble, f\u00e9vrier 2026",
            "https://tgplus.fr/article/au-palais-des-sports-laurence-ruffin-presente-sa-liste-et-son-projet-pour-grenoble/"
        ),
        ("logement", "logements-vacants", "ruffin"): (
            "Cr\u00e9ation d'une brigade municipale contre la vacance de logements",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/auvergne-rhone-alpes/isere-38/grenoble/municipales-2026-laurence-ruffin-lance-son-sprint-final-au-palais-des-sports-de-grenoble-9158572"
        ),
        ("education", "cantines-fournitures", "ruffin"): (
            "Tarif parent solo pour la cantine et le p\u00e9riscolaire",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/auvergne-rhone-alpes/isere-38/grenoble/municipales-2026-laurence-ruffin-lance-son-sprint-final-au-palais-des-sports-de-grenoble-9158572"
        ),
        ("education", "jeunesse", "ruffin"): (
            "Cr\u00e9ation d'un revenu de solidarit\u00e9 jeunes",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/auvergne-rhone-alpes/isere-38/grenoble/municipales-2026-laurence-ruffin-lance-son-sprint-final-au-palais-des-sports-de-grenoble-9158572"
        ),
        ("environnement", "espaces-verts", "ruffin"): (
            "Cr\u00e9ation d'une for\u00eat urbaine et ouverture de la baignade dans l'Is\u00e8re",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/auvergne-rhone-alpes/isere-38/grenoble/municipales-2026-laurence-ruffin-lance-son-sprint-final-au-palais-des-sports-de-grenoble-9158572"
        ),
        ("environnement", "climat-adaptation", "ruffin"): (
            "D\u00e9veloppement d'une \u00e9pargne citoyenne pour accompagner la transition \u00e9cologique, inspir\u00e9e de Bologne et Fribourg",
            "Place Gre'net, septembre 2025",
            "https://www.placegrenet.fr/2025/09/25/cooperation-protection-et-sante-les-priorites-de-laurence-ruffin-candidate-aux-municipales-a-grenoble/660653"
        ),
        ("environnement", "alimentation-durable", "ruffin"): (
            "Cr\u00e9ation d'une s\u00e9curit\u00e9 sociale de l'alimentation et d'un march\u00e9 convivial en centre-ville",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/auvergne-rhone-alpes/isere-38/grenoble/municipales-2026-laurence-ruffin-lance-son-sprint-final-au-palais-des-sports-de-grenoble-9158572"
        ),
        ("sante", "centres-sante", "ruffin"): (
            "Cr\u00e9ation de deux centres de sant\u00e9 municipaux, un centre de sant\u00e9 dans chaque secteur de la ville",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/auvergne-rhone-alpes/isere-38/grenoble/municipales-2026-laurence-ruffin-lance-son-sprint-final-au-palais-des-sports-de-grenoble-9158572"
        ),
        ("democratie", "transparence", "ruffin"): (
            "Votes ouverts d\u00e8s 16 ans sur les questions municipales, y compris aux r\u00e9sidents \u00e9trangers",
            "T\u00e9l\u00e9Grenoble, f\u00e9vrier 2026",
            "https://tgplus.fr/article/au-palais-des-sports-laurence-ruffin-presente-sa-liste-et-son-projet-pour-grenoble/"
        ),
        # --- Carignon (LR/Renaissance) ---
        ("securite", "police-municipale", "carignon"): (
            "Recrutement, formation et armement de 150 policiers municipaux suppl\u00e9mentaires, avec red\u00e9ploiement dans les quartiers sud apr\u00e8s 19h",
            "France Bleu Is\u00e8re, janvier 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-grenoble-alain-carignon-devoile-ses-principales-mesures-pour-lutter-contre-l-insecurite-6904960"
        ),
        ("securite", "videoprotection", "carignon"): (
            "D\u00e9ploiement de 300 cam\u00e9ras de vid\u00e9oprotection connect\u00e9es \u00e0 un centre de supervision 24h/24, assist\u00e9 par intelligence artificielle",
            "France Bleu Is\u00e8re, janvier 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-grenoble-alain-carignon-devoile-ses-principales-mesures-pour-lutter-contre-l-insecurite-6904960"
        ),
        ("solidarite", "pouvoir-achat", "carignon"): (
            "Engagement d'un mandat sans hausse d'imp\u00f4ts : blocage des taux d'imposition et mutualisation ville/m\u00e9tropole pour 80 M\u20ac d'\u00e9conomies",
            "Grenoble Mag, 2025",
            "https://www.grenoblemag.com/article/2156/municipales-a-grenoble-alain-carignon-s-engage-a-stopper-la-hausse-d-impots"
        ),
        # --- Gerbi (Horizons) ---
        ("securite", "police-municipale", "gerbi"): (
            "Plan s\u00e9curit\u00e9 chiffr\u00e9 \u00e0 10,8 millions d'euros : 176 policiers municipaux arm\u00e9s et commissariat ouvert 24h/24",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-de-6h30-et-8h30-ici-isere/municipales-2026-a-grenoble-qui-sont-les-candidats-et-que-proposent-ils-4413956"
        ),
        ("securite", "videoprotection", "gerbi"): (
            "Multiplication par cinq du nombre de cam\u00e9ras intelligentes, avec un centre de vid\u00e9oprotection op\u00e9rationnel en continu",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-de-6h30-et-8h30-ici-isere/municipales-2026-a-grenoble-qui-sont-les-candidats-et-que-proposent-ils-4413956"
        ),
        ("education", "cantines-fournitures", "gerbi"): (
            "Gratuit\u00e9 de la cantine scolaire pour rendre l'\u00e9cole accessible au plus grand nombre",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-de-6h30-et-8h30-ici-isere/municipales-2026-a-grenoble-qui-sont-les-candidats-et-que-proposent-ils-4413956"
        ),
        ("sante", "seniors", "gerbi"): (
            "Ch\u00e8que restaurant pour les plus de 70 ans",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-de-6h30-et-8h30-ici-isere/municipales-2026-a-grenoble-qui-sont-les-candidats-et-que-proposent-ils-4413956"
        ),
        ("urbanisme", "amenagement-urbain", "gerbi"): (
            "Urbanisme \u00e9quilibr\u00e9 garantissant le droit au logement et la proximit\u00e9 avec les habitants",
            "France Bleu Is\u00e8re, f\u00e9vrier 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-de-6h30-et-8h30-ici-isere/municipales-2026-a-grenoble-qui-sont-les-candidats-et-que-proposent-ils-4413956"
        ),
        ("solidarite", "pouvoir-achat", "gerbi"): (
            "Baisse de 10% de la taxe fonci\u00e8re, restitution du trop-per\u00e7u aux contribuables grenoblois",
            "Place Gre'net, novembre 2025",
            "https://www.placegrenet.fr/2025/11/03/municipales-a-grenoble-le-candidat-herve-gerbi-veut-rendre-le-trop-percu-de-la-taxe-fonciere/663544"
        ),
        # --- Brunon (LFI) ---
        ("transports", "tarifs-gratuite", "brunon"): (
            "Gratuit\u00e9 progressive des transports en commun : d'abord le week-end, puis pour les moins de 26 ans, puis gratuit\u00e9 totale",
            "T\u00e9l\u00e9Grenoble, f\u00e9vrier 2026",
            "https://tgplus.fr/article/manuel-bompard-en-visite-a-grenoble-pour-le-meeting-lfi-brunon-annonce-cantine-gratuite-et-transports-gratuits/"
        ),
        ("transports", "pietons-circulation", "brunon"): (
            "Refus de la Zone \u00e0 faibles \u00e9missions (ZFE) jug\u00e9e p\u00e9nalisante pour les travailleurs",
            "France Bleu Is\u00e8re, 2025",
            "https://www.francebleu.fr/infos/politique/elections-municipales-a-grenoble-lfi-fait-cavalier-seul-et-presente-une-liste-menee-par-allan-brunon-2636975"
        ),
        ("logement", "logements-vacants", "brunon"): (
            "R\u00e9quisition effective des logements vacants pour loger les sans-abri",
            "France Bleu Is\u00e8re, 2025",
            "https://www.francebleu.fr/infos/politique/elections-municipales-a-grenoble-lfi-fait-cavalier-seul-et-presente-une-liste-menee-par-allan-brunon-2636975"
        ),
        ("education", "cantines-fournitures", "brunon"): (
            "Gratuit\u00e9 totale de la cantine scolaire",
            "T\u00e9l\u00e9Grenoble, f\u00e9vrier 2026",
            "https://tgplus.fr/article/manuel-bompard-en-visite-a-grenoble-pour-le-meeting-lfi-brunon-annonce-cantine-gratuite-et-transports-gratuits/"
        ),
        ("democratie", "transparence", "brunon"): (
            "Mise en place de r\u00e9f\u00e9rendums locaux et d'un m\u00e9canisme de r\u00e9vocation des \u00e9lus",
            "France Bleu Is\u00e8re, 2025",
            "https://www.francebleu.fr/infos/politique/elections-municipales-a-grenoble-lfi-fait-cavalier-seul-et-presente-une-liste-menee-par-allan-brunon-2636975"
        ),
        # --- Gentil (PRG/Place Publique) ---
        ("securite", "police-municipale", "gentil"): (
            "Renforcement de la police municipale et cr\u00e9ation de 80 postes suppl\u00e9mentaires de m\u00e9diateurs et d'agents",
            "CNews, janvier 2026",
            "https://www.cnews.fr/france/2026-01-25/municipales-2026-qui-sont-les-candidats-la-mairie-de-grenoble-1806504"
        ),
        ("education", "cantines-fournitures", "gentil"): (
            "Gratuit\u00e9 r\u00e9elle de l'\u00e9cole incluant la cantine scolaire",
            "CNews, janvier 2026",
            "https://www.cnews.fr/france/2026-01-25/municipales-2026-qui-sont-les-candidats-la-mairie-de-grenoble-1806504"
        ),
        ("sante", "centres-sante", "gentil"): (
            "Cr\u00e9ation de centres de sant\u00e9 par secteur de la ville",
            "CNews, janvier 2026",
            "https://www.cnews.fr/france/2026-01-25/municipales-2026-qui-sont-les-candidats-la-mairie-de-grenoble-1806504"
        ),
        ("democratie", "services-publics", "gentil"): (
            "Renforcement des services publics de proximit\u00e9 dans chaque quartier",
            "CNews, janvier 2026",
            "https://www.cnews.fr/france/2026-01-25/municipales-2026-qui-sont-les-candidats-la-mairie-de-grenoble-1806504"
        ),
        # --- Gabriac (RN/UDR) ---
        ("securite", "police-municipale", "gabriac"): (
            "Recrutement de 150 agents suppl\u00e9mentaires pour la police municipale, arm\u00e9s, pr\u00e9sence 24h/24. Objectif : 250 policiers municipaux",
            "Grenoble Mag, 2026",
            "https://www.grenoblemag.com/article/2520/municipales-valentin-gabriac-rn-devoile-son-plan-grenoble-en-ordre-axe-sur-la-securite"
        ),
        ("securite", "videoprotection", "gabriac"): (
            "Renforcement massif de la vid\u00e9osurveillance sur l'ensemble du territoire communal",
            "Place Gre'net, octobre 2025",
            "https://www.placegrenet.fr/2025/10/13/municipales-le-rn-valentin-gabriac-veut-refaire-de-grenoble-la-capitale-des-alpes/661799"
        ),
        ("environnement", "proprete-dechets", "gabriac"): (
            "Lutte contre les tags et les incivilit\u00e9s, renforcement de la propret\u00e9 urbaine",
            "Place Gre'net, octobre 2025",
            "https://www.placegrenet.fr/2025/10/13/municipales-le-rn-valentin-gabriac-veut-refaire-de-grenoble-la-capitale-des-alpes/661799"
        ),
        ("economie", "commerce-local", "gabriac"): (
            "Soutien aux commer\u00e7ants locaux par une baisse de la fiscalit\u00e9 et une politique incitative",
            "Place Gre'net, octobre 2025",
            "https://www.placegrenet.fr/2025/10/13/municipales-le-rn-valentin-gabriac-veut-refaire-de-grenoble-la-capitale-des-alpes/661799"
        ),
        ("solidarite", "pouvoir-achat", "gabriac"): (
            "Baisse de la fiscalit\u00e9 locale pour redonner du pouvoir d'achat aux Grenoblois",
            "Place Gre'net, octobre 2025",
            "https://www.placegrenet.fr/2025/10/13/municipales-le-rn-valentin-gabriac-veut-refaire-de-grenoble-la-capitale-des-alpes/661799"
        ),
        # --- Belaid (Grenoble Alpes Collectif) ---
        ("democratie", "budget-participatif", "belaid"): (
            "Budget 100% citoyen : budget municipal enti\u00e8rement d\u00e9cid\u00e9 par une assembl\u00e9e de citoyens tir\u00e9s au sort, soumis \u00e0 r\u00e9f\u00e9rendum",
            "Place Gre'net, novembre 2025",
            "https://www.placegrenet.fr/2025/11/07/le-grenoble-alpes-collectif-presente-son-projet-de-budget-100-citoyen-soutenu-par-lex-adjoint-hakim-sabri/663882"
        ),
        ("democratie", "services-publics", "belaid"): (
            "Cr\u00e9ation de bin\u00f4mes de co-maires de quartier charg\u00e9s d'organiser la d\u00e9mocratie locale",
            "Place Gre'net, d\u00e9cembre 2025",
            "https://www.placegrenet.fr/2025/12/11/municipales-de-grenoble-nadia-belaid-et-thomas-simon-binome-tete-de-liste-du-grenoble-alpes-collectif/666845"
        ),
        # --- Anglade (NPA) ---
        ("transports", "tarifs-gratuite", "anglade"): (
            "Gratuit\u00e9 totale des transports en commun",
            "CNews, janvier 2026",
            "https://www.cnews.fr/france/2026-01-25/municipales-2026-qui-sont-les-candidats-la-mairie-de-grenoble-1806504"
        ),
        ("logement", "logements-vacants", "anglade"): (
            "R\u00e9quisition des logements vacants et baisse des loyers",
            "Place Gre'net, octobre 2025",
            "https://www.placegrenet.fr/2025/10/29/municipales-le-npa-revolutionnaires-entre-en-lice-avec-baptiste-anglade-pour-faire-entendre-la-voix-des-travailleurs/663261"
        ),
        ("education", "cantines-fournitures", "anglade"): (
            "Gratuit\u00e9 des cantines scolaires",
            "CNews, janvier 2026",
            "https://www.cnews.fr/france/2026-01-25/municipales-2026-qui-sont-les-candidats-la-mairie-de-grenoble-1806504"
        ),
        ("sante", "seniors", "anglade"): (
            "Gratuit\u00e9 des maisons de retraite",
            "CNews, janvier 2026",
            "https://www.cnews.fr/france/2026-01-25/municipales-2026-qui-sont-les-candidats-la-mairie-de-grenoble-1806504"
        ),
        ("economie", "emploi-insertion", "anglade"): (
            "Interdiction des licenciements, augmentation g\u00e9n\u00e9rale des salaires d'au moins 400 \u20ac/mois, aucun salaire inf\u00e9rieur \u00e0 2 000 \u20ac",
            "Le Travailleur alpin, novembre 2025",
            "https://travailleur-alpin.fr/2025/11/05/grenoble-le-npa-revolutionnaires-en-campagne-avec-baptiste-anglade/"
        ),
    }
)
