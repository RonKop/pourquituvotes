#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Aix-en-Provence dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== AIX-EN-PROVENCE ===")
insert_city(
    ville_id="aix-en-provence",
    ville_nom="Aix-en-Provence",
    ville_cp="13100",
    candidats=[
        {"id": "joissains", "nom": "Sophie Joissains", "liste": "UDI (Union de la droite et du centre)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "pena", "nom": "Marc P\u00e9na", "liste": "Aix en Partage (PS-PCF-EELV)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "klein", "nom": "Philippe Klein", "liste": "Horizons", "programmeUrl": "https://www.philippe-klein.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "boronad", "nom": "Julie Boronad", "liste": "Aix en commun (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "geiger", "nom": "Jean-Louis Geiger", "liste": "RN-UDR", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "ben-ammar", "nom": "Mounir Ben Ammar", "liste": "Aix-en-Provence ville vivante (REV)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Joissains (maire sortante) ---
        ("securite", "police-municipale", "joissains"): (
            "Renforcement de la police municipale avec 10 recrutements suppl\u00e9mentaires par an (138 agents actuellement) et d\u00e9ploiement de 500 cam\u00e9ras de vid\u00e9oprotection",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/provence-alpes-cote-d-azur/bouches-du-rhone-13/aix-en-provence/municipales-2026-qui-sont-les-candidats-declares-a-aix-en-provence-3346519"
        ),
        ("securite", "videoprotection", "joissains"): (
            "\u00c9quiper toutes les \u00e9coles primaires et maternelles de vid\u00e9osurveillance",
            "Marsactu, 2026",
            "https://marsactu.fr/breve_de_campagne/a-aix-la-maire-sortante-sophie-joissains-lance-sa-campagne-sur-le-theme-de-la-securite/"
        ),
        ("transports", "transports-en-commun", "joissains"): (
            "Poursuite du d\u00e9veloppement des transports en commun avec la ligne Aixpress (bus 100% \u00e9lectriques) et construction de parkings-relais",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/provence-alpes-cote-d-azur/bouches-du-rhone-13/aix-en-provence/municipales-2026-sophie-joissains-est-officiellement-candidate-a-aix-en-provence-5419741"
        ),
        ("transports", "velo-mobilites-douces", "joissains"): (
            "Plan v\u00e9lo ambitieux : 170 km d'infrastructures cyclables, 5 millions d'euros par an d\u00e9di\u00e9s et pi\u00e9tonnisation du centre historique",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/provence-alpes-cote-d-azur/bouches-du-rhone-13/aix-en-provence/municipales-2026-sophie-joissains-est-officiellement-candidate-a-aix-en-provence-5419741"
        ),
        ("logement", "logement-social", "joissains"): (
            "Construction de 900 logements par an, notamment dans le quartier Constance, avec proximit\u00e9 des \u00e9quipements \u00e0 15 minutes \u00e0 pied ou v\u00e9lo",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/provence-alpes-cote-d-azur/bouches-du-rhone-13/aix-en-provence/municipales-2026-sophie-joissains-est-officiellement-candidate-a-aix-en-provence-5419741"
        ),
        ("economie", "attractivite", "joissains"): (
            "Pas d'augmentation des imp\u00f4ts : engagement de stabilit\u00e9 fiscale pour maintenir l'attractivit\u00e9 d'Aix-en-Provence",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/provence-alpes-cote-d-azur/bouches-du-rhone-13/aix-en-provence/municipales-2026-sophie-joissains-est-officiellement-candidate-a-aix-en-provence-5419741"
        ),
        ("environnement", "espaces-verts", "joissains"): (
            "V\u00e9g\u00e9talisation des places publiques avec plantation d'arbres pour r\u00e9duire les temp\u00e9ratures de 2 \u00e0 4 degr\u00e9s",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/provence-alpes-cote-d-azur/bouches-du-rhone-13/aix-en-provence/municipales-2026-sophie-joissains-est-officiellement-candidate-a-aix-en-provence-5419741"
        ),
        ("urbanisme", "amenagement-urbain", "joissains"): (
            "Poursuite de la transformation de la place Rom\u00e9e de Villeneuve et de la requalification du Cours Sextius",
            "Marsactu, 2026",
            "https://marsactu.fr/breve_de_campagne/a-aix-la-maire-sortante-sophie-joissains-lance-sa-campagne-sur-le-theme-de-la-securite/"
        ),
        # --- Pena (Union de la gauche) ---
        ("securite", "police-municipale", "pena"): (
            "Renforcement de la police municipale et lutte contre le narcotrafic",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-provence/municipales-2026-a-aix-en-provence-marc-pena-invite-sur-ici-provence-7280497"
        ),
        ("logement", "encadrement-loyers", "pena"): (
            "R\u00e9guler les locations touristiques : r\u00e9duire la dur\u00e9e maximale de location \u00e0 90 jours et imposer la diversit\u00e9 sociale dans chaque op\u00e9ration de construction",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-provence/municipales-2026-a-aix-en-provence-marc-pena-invite-sur-ici-provence-7280497"
        ),
        ("transports", "velo-mobilites-douces", "pena"): (
            "Plan v\u00e9lo ambitieux en concertation avec les usagers, pistes cyclables de qualit\u00e9 entre quartiers, g\u00e9n\u00e9ralisation du 30 km/h",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-provence/municipales-2026-a-aix-en-provence-marc-pena-invite-sur-ici-provence-7280497"
        ),
        ("transports", "transports-en-commun", "pena"): (
            "D\u00e9velopper un r\u00e9seau de transports en commun couvrant int\u00e9gralement la zone urbaine, \u00e0 toute heure",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-provence/municipales-2026-a-aix-en-provence-marc-pena-invite-sur-ici-provence-7280497"
        ),
        ("transports", "stationnement", "pena"): (
            "Politique de stationnement incitative pour r\u00e9duire la d\u00e9pendance automobile et transf\u00e9rer les d\u00e9placements vers les modes doux",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-provence/municipales-2026-a-aix-en-provence-marc-pena-invite-sur-ici-provence-7280497"
        ),
        ("environnement", "renovation-energetique", "pena"): (
            "Programme ambitieux de r\u00e9duction de la consommation \u00e9nerg\u00e9tique des logements et b\u00e2timents publics, promotion des \u00e9nergies renouvelables",
            "Destimed, 2026",
            "https://www.destimed.fr/Tribune-Municipales-a-Aix-en-Provence-Ecologistes-avec-Marc-Pena-et-Aix-en/"
        ),
        # --- Klein (Horizons) ---
        ("environnement", "climat-adaptation", "klein"): (
            "Faire d'Aix-en-Provence une ville-refuge climatique : fin de la min\u00e9ralisation excessive, ombrage, eau, arbres et espaces publics de qualit\u00e9",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-provence/philippe-klein-candidat-horizon-a-la-mairie-d-aix-en-provence-5268735"
        ),
        ("urbanisme", "amenagement-urbain", "klein"): (
            "Proposer un cap exigeant conciliant qualit\u00e9 de vie, attractivit\u00e9 \u00e9conomique, transition \u00e9cologique et coh\u00e9sion interg\u00e9n\u00e9rationnelle",
            "France Bleu Provence, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-provence/philippe-klein-candidat-horizon-a-la-mairie-d-aix-en-provence-5268735"
        ),
        # --- Boronad (LFI) ---
        ("securite", "prevention-mediation", "boronad"): (
            "Cr\u00e9er une police de proximit\u00e9 dans chaque quartier, form\u00e9e \u00e0 la m\u00e9diation, pour recr\u00e9er le lien avec les habitants",
            "L'Affranchi Mag, 2026",
            "https://www.laffranchimag.fr/Municipales-2026-a-Aix-en-Provence-LFI-mise-sur-la-jeunesse-et-creuse-la-fracture-a-gauche_a571.html"
        ),
        ("logement", "acces-logement", "boronad"): (
            "Cr\u00e9er une r\u00e9gie du logement : face aux 40 000 \u00e9tudiants pour seulement 8 000 places en r\u00e9sidences, construire des logements g\u00e9r\u00e9s par le CROUS",
            "L'Affranchi Mag, 2026",
            "https://www.laffranchimag.fr/Municipales-2026-a-Aix-en-Provence-LFI-mise-sur-la-jeunesse-et-creuse-la-fracture-a-gauche_a571.html"
        ),
        # --- Geiger (RN) ---
        ("securite", "police-municipale", "geiger"): (
            "Obtenir 140 policiers nationaux suppl\u00e9mentaires pour Aix et cr\u00e9er une brigade anti-stup\u00e9fiants municipale sur le mod\u00e8le de B\u00e9ziers",
            "L'Affranchi Mag, 2026",
            "https://www.laffranchimag.fr/Municipales-2026-a-Aix-Jean-Louis-Geiger-l-union-des-droites-a-hauts-risques_a516.html"
        ),
    }
)
