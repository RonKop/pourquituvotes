#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Saint-\u00c9tienne dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== SAINT-ETIENNE ===")
insert_city(
    ville_id="saint-etienne",
    ville_nom="Saint-\u00c9tienne",
    ville_cp="42000",
    candidats=[
        {"id": "cinieri", "nom": "Dino Cinieri", "liste": "Saint-\u00c9tienne Ensemble 2026 (LR/UDI/Horizons/Renaissance/MoDem)", "programmeUrl": "https://www.cinieri2026.com/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "juanico", "nom": "R\u00e9gis Juanico", "liste": "Rassembler Saint-\u00c9tienne (PS/EELV/PCF)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "le-jaouen", "nom": "\u00c9ric Le Jaouen", "liste": "Relevons Saint-\u00c9tienne (Horizons dissident)", "programmeUrl": "https://www.lejaouen2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "chassaubene", "nom": "Marc Chassaub\u00e9n\u00e9", "liste": "Majorit\u00e9 sortante (1er adjoint)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "labich", "nom": "Siham Labich", "liste": "Liste citoyenne (2e adjointe sortante)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "mercier", "nom": "Valentine Mercier", "liste": "La France Insoumise", "programmeUrl": "https://mercier2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "jousserand", "nom": "Corentin Jousserand", "liste": "Rassemblement National", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "brossard", "nom": "Romain Brossard", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Cinieri (Droite unie) ---
        ("securite", "police-municipale", "cinieri"): (
            "Renforcement de la s\u00e9curit\u00e9 en priorit\u00e9 avec des moyens accrus pour la police municipale",
            "France Bleu, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-saint-etienne-loire/municipales-a-saint-etienne-dino-cinieri-presente-sa-liste-8246239"
        ),
        ("economie", "commerce-local", "cinieri"): (
            "Relancer le commerce local et l'attractivit\u00e9 \u00e9conomique de Saint-\u00c9tienne",
            "France Bleu, 2025",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-saint-etienne-dino-cinieri-designe-tete-de-liste-de-la-droite-et-du-centre-par-un-sondage-9876142"
        ),
        ("environnement", "proprete-dechets", "cinieri"): (
            "Am\u00e9liorer la propret\u00e9 de la ville, axe prioritaire du programme",
            "Activ Radio, 2025",
            "https://www.activradio.com/municipales-2026-dino-cinieri-va-faire-campagne-pour-le-collectif-saint-etienne-ensemble-2026"
        ),
        # --- Juanico (Gauche unie) ---
        ("democratie", "transparence", "juanico"): (
            "R\u00e9duire de 15% l'indemnit\u00e9 du maire (de 4 000 \u00e0 3 500 \u20ac nets) pour restaurer la confiance apr\u00e8s l'affaire Perdriau",
            "France 3, 2026",
            "https://france3-regions.franceinfo.fr/auvergne-rhone-alpes/loire/saint-etienne/reduire-de-15-de-l-indemnite-du-maire-une-mesure-annoncee-par-regis-juanico-candidat-aux-municipales-de-saint-etienne-3290505.html"
        ),
        ("transports", "transports-en-commun", "juanico"): (
            "Gratuit\u00e9 des transports en commun le week-end",
            "France Bleu, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-saint-etienne-loire/l-invite-d-ici-matin-regis-juanico-chef-de-file-de-la-liste-rassembler-saint-etienne-3268244"
        ),
        ("sante", "centres-sante", "juanico"): (
            "D\u00e9ployer des m\u00e9dicobus pour rapprocher les soins des habitants \u00e9loign\u00e9s des services m\u00e9dicaux",
            "France Bleu, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-saint-etienne-loire/l-invite-d-ici-matin-regis-juanico-chef-de-file-de-la-liste-rassembler-saint-etienne-3268244"
        ),
        ("securite", "police-municipale", "juanico"): (
            "Cr\u00e9ation d'une police municipale communautaire de proximit\u00e9",
            "France Bleu, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-saint-etienne-loire/municipales-2026-la-gauche-stephanoise-unie-derriere-le-socialiste-regis-juanico-8849511"
        ),
        ("urbanisme", "amenagement-urbain", "juanico"): (
            "D\u00e9veloppement de zones pi\u00e9tonnes en centre-ville",
            "France Bleu, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-saint-etienne-loire/l-invite-d-ici-matin-regis-juanico-chef-de-file-de-la-liste-rassembler-saint-etienne-3268244"
        ),
        # --- Le Jaouen (Horizons dissident) ---
        ("economie", "attractivite", "le-jaouen"): (
            "Redonner un \u00e9lan \u00e9conomique \u00e0 Saint-\u00c9tienne, liste du renouveau de la droite et du centre",
            "France Bleu, 2025",
            "https://www.francebleu.fr/infos/politique/eric-le-jaouen-candidat-aux-municipales-a-saint-etienne-pour-redonner-un-elan-a-la-ville-6315268"
        ),
        # --- Chassaubene (1er adjoint sortant) ---
        ("logement", "acces-logement", "chassaubene"): (
            "Programme articul\u00e9 autour de grandir, vivre, transmettre avec le logement, la mobilit\u00e9 et la s\u00e9curit\u00e9 comme fil rouge",
            "Radio Scoop, 2025",
            "https://www.radioscoop.com/infos/municipales-2026-a-saint-etienne-marc-chassaubene-officialise-sa-candidature_344977"
        ),
        # --- Labich (2e adjointe sortante) ---
        ("democratie", "vie-associative", "labich"): (
            "Mener une liste citoyenne sans \u00e9tiquette politique, issue de la soci\u00e9t\u00e9 civile, soutenue par 12 \u00e9lus sortants",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-siham-labich-officiellement-candidate-deuxieme-liste-issue-de-la-majorite-a-saint-etienne-3748819"
        ),
        # --- Mercier (LFI) ---
        ("democratie", "budget-participatif", "mercier"): (
            "Instaurer des budgets participatifs dans les conseils de quartier et un r\u00e9f\u00e9rendum d'initiative citoyenne local",
            "TL7, 2026",
            "https://www.tl7.fr/replay/7-mn-chrono_8/saint-etienne-municipales-2026-valentine-mercier-lfi-devoile-son-programme-7-minutes-chrono_x9x4knu.html"
        ),
        ("education", "cantines-fournitures", "mercier"): (
            "Cantines bio et gratuites dans les \u00e9coles",
            "IF Saint-\u00c9tienne, 2025",
            "https://www.if-saint-etienne.fr/politique-societe/municipales-2026-a-saint-etienne-lfi-a-presente-ses-axes-programmatiques"
        ),
        ("sante", "centres-sante", "mercier"): (
            "Ouverture d'un centre de sant\u00e9 municipal \u00e0 C\u00f4te Chaude",
            "IF Saint-\u00c9tienne, 2025",
            "https://www.if-saint-etienne.fr/politique-societe/municipales-2026-a-saint-etienne-lfi-a-presente-ses-axes-programmatiques"
        ),
        ("securite", "police-municipale", "mercier"): (
            "Recentrer la police municipale sur ses missions de proximit\u00e9 et de pr\u00e9vention",
            "TL7, 2026",
            "https://www.tl7.fr/replay/7-mn-chrono_8/saint-etienne-municipales-2026-valentine-mercier-lfi-devoile-son-programme-7-minutes-chrono_x9x4knu.html"
        ),
        ("transports", "pietons-circulation", "mercier"): (
            "Pi\u00e9tonnisation massive du centre-ville et intensification des transports en commun",
            "IF Saint-\u00c9tienne, 2025",
            "https://www.if-saint-etienne.fr/politique-societe/municipales-2026-a-saint-etienne-lfi-a-presente-ses-axes-programmatiques"
        ),
        ("democratie", "transparence", "mercier"): (
            "Plafonner les indemnit\u00e9s des \u00e9lus, instaurer la r\u00e9vocabilit\u00e9 des \u00e9lus et limiter le cumul des mandats",
            "IF Saint-\u00c9tienne, 2025",
            "https://www.if-saint-etienne.fr/politique-societe/municipales-2026-a-saint-etienne-lfi-a-presente-ses-axes-programmatiques"
        ),
        # --- Jousserand (RN) ---
        ("economie", "attractivite", "jousserand"): (
            "Attirer l'activit\u00e9 \u00e9conomique \u00e0 Saint-\u00c9tienne et am\u00e9liorer l'image de la ville",
            "France Bleu, 2025",
            "https://www.francebleu.fr/infos/politique/municipales-a-saint-etienne-corentin-jousserand-28-ans-est-la-tete-de-liste-du-rassemblement-national-5554400"
        ),
        ("securite", "police-municipale", "jousserand"): (
            "Lutte contre l'ins\u00e9curit\u00e9 comme priorit\u00e9 absolue",
            "France Bleu, 2025",
            "https://www.francebleu.fr/infos/politique/municipales-a-saint-etienne-corentin-jousserand-28-ans-est-la-tete-de-liste-du-rassemblement-national-5554400"
        ),
        ("democratie", "transparence", "jousserand"): (
            "Cr\u00e9ation d'un comit\u00e9 d'\u00e9thique pour contr\u00f4ler la moralit\u00e9 des \u00e9lus",
            "France Bleu, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-saint-etienne-loire/le-candidat-rassemblement-national-a-la-mairie-de-saint-etienne-propose-un-comite-d-ethique-pour-la-moralite-des-elus-9039906"
        ),
        # --- Brossard (LO) ---
        ("solidarite", "pouvoir-achat", "brossard"): (
            "D\u00e9fendre le pouvoir d'achat des salari\u00e9s, ch\u00f4meurs et retrait\u00e9s face \u00e0 la hausse des prix et la stagnation des salaires",
            "Lutte Ouvri\u00e8re, 2025",
            "https://www.lutte-ouvriere.org/portail/revue-de-presse/municipales-2026-solutions-luttes-romain-brossard-repart-combat-saint-etienne-188071.html"
        ),
    }
)
