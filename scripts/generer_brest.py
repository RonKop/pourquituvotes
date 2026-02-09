#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Brest dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== BREST ===")
insert_city(
    ville_id="brest",
    ville_nom="Brest",
    ville_cp="29200",
    candidats=[
        {"id": "cuillandre", "nom": "Fran\u00e7ois Cuillandre", "liste": "La gauche unie pour Brest (PS/EELV/PRG/PCF)", "programmeUrl": "https://www.brest-ensemble.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "roudaut", "nom": "St\u00e9phane Roudaut", "liste": "Une nouvelle histoire pour Brest (DVD/UDI/Horizons/LR)", "programmeUrl": "https://www.stephaneroudaut2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "beaudouin", "nom": "C\u00e9cile Beaudouin", "liste": "Brest Insoumise (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "muscat", "nom": "S\u00e9bastien Muscat", "liste": "Brest Nouvelle Vague (citoyen gauche)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "pages", "nom": "Yves Pag\u00e8s", "liste": "Rassemblement National", "programmeUrl": "https://yvespages2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "yenier", "nom": "Nazim Yenier", "liste": "La Vague citoyenne (sans \u00e9tiquette)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Cuillandre (Gauche unie) ---
        ("securite", "police-municipale", "cuillandre"): (
            "Cr\u00e9ation d'une police municipale de proximit\u00e9 de 50 agents, \u00e9quip\u00e9s d'armes non l\u00e9tales et de cam\u00e9ras-pi\u00e9tons, co\u00fbt 3 M\u20ac/an",
            "France 3 Bretagne, 2026",
            "https://france3-regions.franceinfo.fr/bretagne/finistere/brest/elections-municipales-2026-le-maire-de-brest-et-candidat-francois-cuillandre-veut-creer-une-police-municipale-de-50-agents-3277367.html"
        ),
        ("securite", "videoprotection", "cuillandre"): (
            "Renforcement de la brigade de tranquillit\u00e9 urbaine \u00e0 25 agents et installation de nouvelles cam\u00e9ras de vid\u00e9oprotection",
            "France Bleu, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-breizh-izel/municipales-2026-a-brest-francois-cuillandre-promet-une-police-municipale-2030517"
        ),
        ("sport", "equipements-sportifs", "cuillandre"): (
            "Construction du nouveau stade Ark\u00e9a Park pour remplacer le stade Francis-Le Bl\u00e9",
            "UESR29, 2025",
            "https://uesr29.fr/entre-grands-projets-et-enjeux-politiques-francois-cuillandre-trace-la-voie-pour-brest/"
        ),
        ("transports", "transports-en-commun", "cuillandre"): (
            "Deuxi\u00e8me ligne de tramway et bus \u00e0 haut niveau de service (BHNS) pour transformer les d\u00e9placements",
            "UESR29, 2025",
            "https://uesr29.fr/entre-grands-projets-et-enjeux-politiques-francois-cuillandre-trace-la-voie-pour-brest/"
        ),
        ("environnement", "climat-adaptation", "cuillandre"): (
            "Transition \u00e9cologique renforc\u00e9e et d\u00e9veloppement de la mobilit\u00e9 durable, base programmatique commune PS-EELV",
            "PS29, 2025",
            "https://www.ps29.org/actualite/la-gauche-unie-pour-brest-socialistes-et-ecologistes-scellent-un-accord-pour-2026/"
        ),
        # --- Roudaut (Droite/Centre) ---
        ("securite", "police-municipale", "roudaut"): (
            "Cr\u00e9ation d'une Police Territoriale unifi\u00e9e (police municipale + ASVP + brigade transport) avec patrouilles 24h/24 le week-end et armement des agents",
            "stephaneroudaut2026.fr, 2026",
            "https://www.stephaneroudaut2026.fr/post/s%C3%A9curit%C3%A9-%C3%A0-brest-les-5-engagements-de-st%C3%A9phane-roudaut-pour-une-ville-plus-s%C3%BBre"
        ),
        ("solidarite", "egalite-discriminations", "roudaut"): (
            "Plan ambitieux pour faire de Brest une ville pionni\u00e8re en mati\u00e8re d'\u00e9galit\u00e9 femmes-hommes",
            "stephaneroudaut2026.fr, 2026",
            "https://www.stephaneroudaut2026.fr/"
        ),
        ("urbanisme", "accessibilite", "roudaut"): (
            "Faire de l'inclusion et du handicap la grande cause du mandat",
            "stephaneroudaut2026.fr, 2026",
            "https://www.stephaneroudaut2026.fr/"
        ),
        # --- Beaudouin (LFI) ---
        ("transports", "tarifs-gratuite", "beaudouin"): (
            "Gratuit\u00e9 totale des transports en commun avec garantie de qualit\u00e9 de service et de conditions de travail",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-brest-la-liste-lfi-de-cecile-beaudouin-promet-une-revolution-citoyenne-1075453"
        ),
        ("education", "cantines-fournitures", "beaudouin"): (
            "Cantines scolaires 100% bio et enti\u00e8rement gratuites",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-brest-la-liste-lfi-de-cecile-beaudouin-promet-une-revolution-citoyenne-1075453"
        ),
        ("logement", "acces-logement", "beaudouin"): (
            "Politique du logement garantissant un logement digne pour tous et lutte contre la sp\u00e9culation immobili\u00e8re",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-brest-la-liste-lfi-de-cecile-beaudouin-promet-une-revolution-citoyenne-1075453"
        ),
        ("securite", "prevention-mediation", "beaudouin"): (
            "Pr\u00e9vention, m\u00e9diation et \u00e9ducation coordonn\u00e9es entre tous les acteurs sociaux pour une ville plus s\u00fbre",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-brest-la-liste-lfi-de-cecile-beaudouin-promet-une-revolution-citoyenne-1075453"
        ),
        ("democratie", "transparence", "beaudouin"): (
            "S\u00e9parer les fonctions de maire de Brest et pr\u00e9sident de la m\u00e9tropole, limiter \u00e0 deux mandats maximum",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-brest-la-liste-lfi-de-cecile-beaudouin-promet-une-revolution-citoyenne-1075453"
        ),
        # --- Muscat (Brest Nouvelle Vague) ---
        ("democratie", "vie-associative", "muscat"): (
            "Liste citoyenne de gauche port\u00e9e par la soci\u00e9t\u00e9 civile, soutenue par G\u00e9n\u00e9ration.s et les Radicaux de Gauche",
            "France Bleu, 2026",
            "https://www.francebleu.fr/bretagne/finistere-29/brest/municipales-2026-a-brest-isabelle-montanari-rejoint-la-liste-citoyenne-de-gauche-4884570"
        ),
        # --- Pages (RN) ---
        ("economie", "attractivite", "pages"): (
            "Enrayer le d\u00e9clin d\u00e9mographique et relancer l'attractivit\u00e9 \u00e9conomique de Brest",
            "yvespages2026.fr, 2026",
            "https://yvespages2026.fr/"
        ),
        # --- Yenier (Divers) ---
        ("securite", "police-municipale", "yenier"): (
            "Cr\u00e9ation d'une police municipale arm\u00e9e de 100 agents, avec un commissariat central au port et deux antennes \u00e0 Bellevue et Pontan\u00e9zen",
            "France Bleu, 2026",
            "https://www.francebleu.fr/bretagne/finistere-29/brest/municipales-2026-a-brest-nazim-yenier-l-electron-libre-qui-veut-faire-chuter-francois-cuillandre-3435072"
        ),
        ("logement", "logement-social", "yenier"): (
            "R\u00e9habilitation des logements sociaux dans les quartiers populaires",
            "France Bleu, 2026",
            "https://www.francebleu.fr/bretagne/finistere-29/brest/municipales-2026-a-brest-nazim-yenier-l-electron-libre-qui-veut-faire-chuter-francois-cuillandre-3435072"
        ),
    }
)
