#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Toulon dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== TOULON ===")
insert_city(
    ville_id="toulon",
    ville_nom="Toulon",
    ville_cp="83000",
    candidats=[
        {"id": "massi", "nom": "Jos\u00e9e Massi", "liste": "Toulon mon parti (sortante)", "programmeUrl": "https://joseemassi.com/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "lavalette", "nom": "Laure Lavalette", "liste": "Un avenir pour Toulon (soutenue par le RN)", "programmeUrl": "https://www.unavenirpourtoulon.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "bonnus", "nom": "Michel Bonnus", "liste": "Toulon en Grand (LR)", "programmeUrl": "https://toulonengrand.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "brunel", "nom": "Magali Brunel", "liste": "Toulon en Commun (PS-PCF-\u00c9cologistes)", "programmeUrl": "https://toulonencommun2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "cornil", "nom": "Isaline Cornil", "liste": "La France Insoumise", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "le-lostec", "nom": "Emmanuel Le Lostec", "liste": "En Avant Toulon-Isso Touloun", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Massi (sortante) ---
        ("securite", "police-municipale", "massi"): (
            "Passer de 152 \u00e0 200 policiers municipaux et cr\u00e9er des commissariats de quartier",
            "France Bleu / Info83, 2026",
            "https://www.info83.fr/municipales-2026-a-toulon-josee-massi-presente-un-programme-axe-sur-la-securite-la-proximite-et-lattractivite/"
        ),
        ("transports", "transports-en-commun", "massi"): (
            "Cr\u00e9er un bus \u00e0 haut niveau de service (BHNS) rapide avec un bus toutes les 10 minutes, et connecter 70 km de pistes cyclables entre elles",
            "RCF / Info83, 2026",
            "https://www.rcf.fr/articles/actualite/municipales-2026-a-toulon-la-maire-josee-massi-devoile-ses-priorites"
        ),
        ("democratie", "services-publics", "massi"): (
            "Lancer l'outil Toulon et vous pour maintenir le lien entre habitants et mairie sur les questions administratives et les services du quotidien",
            "RCF / Info83, 2026",
            "https://www.rcf.fr/articles/actualite/municipales-2026-a-toulon-la-maire-josee-massi-devoile-ses-priorites"
        ),
        ("economie", "attractivite", "massi"): (
            "Dynamiser l'\u00e9conomie avec la cr\u00e9ation de nouveaux secteurs, construction d'une r\u00e9sidence \u00e9tudiante, et verdissement des \u00e9coles",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-la-maire-de-toulon-josee-massi-candidate-9577017"
        ),
        # --- Lavalette (RN) ---
        ("securite", "police-municipale", "lavalette"): (
            "R\u00e9armer moralement la police municipale et recruter une soixantaine de policiers municipaux suppl\u00e9mentaires pour atteindre 200 agents",
            "CNews / France Bleu, 2026",
            "https://www.cnews.fr/france/2026-01-06/municipales-2026-la-securite-sera-le-fil-rouge-annonce-laure-lavalette-deputee-rn"
        ),
        ("urbanisme", "amenagement-urbain", "lavalette"): (
            "Plan de r\u00e9fection des routes et trottoirs, \u00e9galit\u00e9 de traitement entre tous les quartiers",
            "RCF, 2026",
            "https://www.rcf.fr/articles/actualite/municipales-2026-a-toulon-laure-lavalette-lance-officiellement-sa-campagne"
        ),
        ("education", "ecoles-renovation", "lavalette"): (
            "Climatiser toutes les \u00e9coles de Toulon",
            "RCF, 2026",
            "https://www.rcf.fr/articles/actualite/municipales-2026-a-toulon-laure-lavalette-lance-officiellement-sa-campagne"
        ),
        ("culture", "equipements-culturels", "lavalette"): (
            "Cr\u00e9ation d'un centre de la mer \u00e0 Toulon",
            "RCF, 2026",
            "https://www.rcf.fr/articles/actualite/municipales-2026-a-toulon-laure-lavalette-lance-officiellement-sa-campagne"
        ),
        ("democratie", "transparence", "lavalette"): (
            "Donner la parole aux Toulonnais par des consultations et des r\u00e9f\u00e9rendums locaux",
            "RCF, 2026",
            "https://www.rcf.fr/articles/actualite/municipales-2026-a-toulon-laure-lavalette-lance-officiellement-sa-campagne"
        ),
        # --- Bonnus (LR) ---
        ("securite", "police-municipale", "bonnus"): (
            "Recruter une dizaine de policiers municipaux par an, cr\u00e9er des \u00eelotiers, police municipale op\u00e9rationnelle jusqu'\u00e0 2h du matin",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-michel-bonnus-devoile-son-projet-pour-toulon-3077171"
        ),
        ("culture", "equipements-culturels", "bonnus"): (
            "Cr\u00e9er une cit\u00e9 des sciences et de la mer pour reconqu\u00e9rir le littoral et faire conna\u00eetre l'histoire de Toulon",
            "France Bleu / Info83, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-michel-bonnus-devoile-son-projet-pour-toulon-3077171"
        ),
        ("sante", "centres-sante", "bonnus"): (
            "Lutter contre la d\u00e9sertification m\u00e9dicale : cr\u00e9er une maison des internes et un bus m\u00e9dical pour pallier le manque de g\u00e9n\u00e9ralistes",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-michel-bonnus-devoile-son-projet-pour-toulon-3077171"
        ),
        ("economie", "commerce-local", "bonnus"): (
            "Soutien au commerce de proximit\u00e9 et dynamisation de tous les quartiers de Toulon",
            "Info83, 2026",
            "https://www.info83.fr/meeting-michel-bonnus-toulon-2026/"
        ),
        # --- Brunel (Toulon en Commun) ---
        ("transports", "transports-en-commun", "brunel"): (
            "Oui au tramway et aux transports gratuits, non au BHNS ; les Toulonnais perdent 72h par an dans les embouteillages",
            "RCF / France 3, 2026",
            "https://www.rcf.fr/articles/actualite/municipales-2026-a-toulon-magali-brunel-presente-son-programme-et-ses-soutiens"
        ),
        ("logement", "encadrement-loyers", "brunel"): (
            "Encadrer les loyers \u00e0 Toulon pour prot\u00e9ger les locataires et les salari\u00e9s face \u00e0 la hausse du co\u00fbt de la vie",
            "RCF / Info83, 2026",
            "https://www.rcf.fr/articles/actualite/municipales-2026-a-toulon-magali-brunel-presente-son-programme-et-ses-soutiens"
        ),
        ("education", "jeunesse", "brunel"): (
            "Priorit\u00e9 \u00e0 la jeunesse : plus de maisons de quartier faites pour et par les jeunes, sport pour tous",
            "France 3 / RCF, 2026",
            "https://france3-regions.franceinfo.fr/provence-alpes-cote-d-azur/var/toulon/il-est-temps-de-tourner-la-page-d-une-gestion-figee-la-candidate-de-gauche-magali-brunel-en-meeting-a-toulon-3285693.html"
        ),
        ("solidarite", "pouvoir-achat", "brunel"): (
            "Redonner du pouvoir d'achat, du pouvoir d'agir et de mieux vivre \u2014 lutte contre la pauvret\u00e9 (22% de la population sous le seuil)",
            "Toulon en Commun, 2026",
            "https://toulonencommun2026.fr/"
        ),
        # --- Cornil (LFI) ---
        ("transports", "tarifs-gratuite", "cornil"): (
            "Transports en commun gratuits et cr\u00e9ation d'un tramway \u00e0 Toulon",
            "Info83 / RCF, 2026",
            "https://www.info83.fr/municipales-2026-toulon-lfi-lance-sa-liste/"
        ),
        ("logement", "logement-social", "cornil"): (
            "D\u00e9veloppement du logement abordable et lutte contre la pauvret\u00e9 : 22% des Toulonnais vivent sous le seuil de pauvret\u00e9",
            "Info83 / RCF, 2026",
            "https://www.info83.fr/municipales-toulon-2026-lfi-toulon-cornil-denis/"
        ),
        ("sante", "prevention-sante", "cornil"): (
            "Cr\u00e9er des structures d'accompagnement des addictions dans les quartiers populaires",
            "Info83, 2026",
            "https://www.info83.fr/municipales-toulon-2026-lfi-toulon-cornil-denis/"
        ),
        # --- Le Lostec (En Avant Toulon) ---
        ("economie", "emploi-insertion", "le-lostec"): (
            "Cr\u00e9er un guichet unique municipal pour accompagner les jeunes entrepreneurs vers les financements",
            "Info83, 2026",
            "https://www.info83.fr/emmanuel-le-lostec-elections-municipales/"
        ),
        ("environnement", "climat-adaptation", "le-lostec"): (
            "\u00c9cologie non-punitive : \u00e9lectrification des quais et des ferries, ville bas carbone",
            "Info83, 2026",
            "https://www.info83.fr/emmanuel-le-lostec-elections-municipales/"
        ),
    }
)
