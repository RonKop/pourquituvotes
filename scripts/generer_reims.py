#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Reims dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== REIMS ===")
insert_city(
    ville_id="reims",
    ville_nom="Reims",
    ville_cp="51100",
    candidats=[
        {"id": "robinet", "nom": "Arnaud Robinet", "liste": "Horizons (soutenu par LR)", "programmeUrl": "https://www.arnaudrobinet2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "frigout", "nom": "Anne-Sophie Frigout", "liste": "Rassemblement National", "programmeUrl": "https://frigout2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "quenard", "nom": "\u00c9ric Qu\u00e9nard", "liste": "PS-\u00c9cologistes-PCF-Place Publique", "programmeUrl": "https://ericquenard.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "coradel", "nom": "Patricia Coradel", "liste": "La France Insoumise", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "lang", "nom": "St\u00e9phane Lang", "liste": "Les R\u00e9mois au c\u0153ur (LR dissident)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "mura", "nom": "S\u00e9bastien Mura", "liste": "Nous c'est Reims", "programmeUrl": "https://www.reims-2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "rose", "nom": "Thomas Rose", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Robinet ---
        ("securite", "police-municipale", "robinet"): (
            "Renforcement de la police municipale (de 30 \u00e0 130 agents depuis 2014) et de la vid\u00e9oprotection (de 30 \u00e0 250 cam\u00e9ras) sans augmentation d'imp\u00f4ts locaux",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-le-maire-de-reims-arnaud-robinet-officiellement-candidat-a-sa-reelection-6025232"
        ),
        ("securite", "videoprotection", "robinet"): (
            "Poursuite du d\u00e9veloppement massif de la vid\u00e9oprotection et \u00e9quipement de la police municipale, investissements de 7 millions d'euros pr\u00e9vus",
            "France Bleu, 2025",
            "https://www.francebleu.fr/emissions/l-invite-de-la-redaction-sur-france-bleu-champagne-ardenne/arnaud-robinet-maire-horizons-de-reims-8596574"
        ),
        ("solidarite", "aide-sociale", "robinet"): (
            "Faire de Reims une ville bienveillante : prot\u00e9ger, accompagner et soigner les habitants \u00e0 chaque \u00e9tape de leur vie",
            "France 3, 2026",
            "https://france3-regions.franceinfo.fr/grand-est/champagne-ardenne/arnaud-robinet-candidat-pour-un-troisieme-mandat-de-maire-a-reims-3279113.html"
        ),
        # --- Frigout (RN) ---
        ("securite", "police-municipale", "frigout"): (
            "Passer les effectifs de police municipale de 130 \u00e0 200 agents, avec cr\u00e9ation de deux commissariats de police municipale \u00e0 Wilson et Ch\u00e2tillons",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-couvre-feu-brigade-anti-incivilites-a-reims-la-candidate-rn-promet-un-choc-securitaire-1742754"
        ),
        ("securite", "prevention-mediation", "frigout"): (
            "Instaurer un couvre-feu pour les mineurs (amende de 35\u20ac en cas de non-respect) et cr\u00e9er des travaux \u00e9ducatifs d'int\u00e9r\u00eat g\u00e9n\u00e9ral pour les mineurs d\u00e9linquants",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-a-reims-anne-sophie-frigout-candidate-du-rn-veut-imposer-un-couvre-feu-pour-les-mineurs-4876523"
        ),
        ("environnement", "proprete-dechets", "frigout"): (
            "Cr\u00e9ation d'une brigade anti-incivilit\u00e9s contre les d\u00e9p\u00f4ts sauvages, le vandalisme, les nuisances de voisinage, les d\u00e9jections canines et les tags",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-couvre-feu-brigade-anti-incivilites-a-reims-la-candidate-rn-promet-un-choc-securitaire-1742754"
        ),
        # --- Quenard (PS-Ecologistes) ---
        ("transports", "velo-mobilites-douces", "quenard"): (
            "Cr\u00e9er un r\u00e9seau cyclable structurant, continu et s\u00e9curis\u00e9, avec l'objectif de passer de 3% \u00e0 10% de d\u00e9placements \u00e0 v\u00e9lo d'ici la fin du mandat",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-reims-les-ecologistes-rejoignent-les-socialistes-sur-une-liste-commune-portee-par-eric-quenard-8869238"
        ),
        ("transports", "transports-en-commun", "quenard"): (
            "Exp\u00e9rimenter la gratuit\u00e9 des transports en commun pendant un an, d'abord pour les moins de 25 ans et le week-end pour tous",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-reims-les-ecologistes-rejoignent-les-socialistes-sur-une-liste-commune-portee-par-eric-quenard-8869238"
        ),
        ("environnement", "renovation-energetique", "quenard"): (
            "Programme d'investissement thermique dans les b\u00e2timents publics, notamment les \u00e9coles",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-reims-les-ecologistes-rejoignent-les-socialistes-sur-une-liste-commune-portee-par-eric-quenard-8869238"
        ),
        ("sante", "centres-sante", "quenard"): (
            "Cr\u00e9ation d'une mutuelle municipale de sant\u00e9 pour prot\u00e9ger pr\u00e8s de 20 000 R\u00e9mois sans couverture",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-reims-les-ecologistes-rejoignent-les-socialistes-sur-une-liste-commune-portee-par-eric-quenard-8869238"
        ),
        # --- Coradel (LFI) ---
        ("transports", "tarifs-gratuite", "coradel"): (
            "Gratuit\u00e9 des transports pour les moins de 26 ans et les b\u00e9n\u00e9ficiaires des minima sociaux, puis convention citoyenne pour une nouvelle tarification",
            "Orange Actu, 2026",
            "https://actu.orange.fr/videos/actu-locale/municipales-2026-a-reims-patricia-coradel-candidate-lfi-presente-ses-3-priorites-CNT000002n487e.html"
        ),
        ("logement", "acces-logement", "coradel"): (
            "Le logement comme priorit\u00e9 n\u00b01 : am\u00e9liorer l'acc\u00e8s au logement pour tous les R\u00e9mois",
            "Orange Actu, 2026",
            "https://actu.orange.fr/videos/actu-locale/municipales-2026-a-reims-patricia-coradel-candidate-lfi-presente-ses-3-priorites-CNT000002n487e.html"
        ),
        ("education", "periscolaire-loisirs", "coradel"): (
            "Priorit\u00e9 aux enfants : cantines gratuites et d\u00e9veloppement des services p\u00e9riscolaires",
            "Orange Actu, 2026",
            "https://actu.orange.fr/videos/actu-locale/municipales-2026-a-reims-patricia-coradel-candidate-lfi-presente-ses-3-priorites-CNT000002n487e.html"
        ),
        # --- Lang (LR dissident) ---
        ("transports", "pietons-circulation", "lang"): (
            "Restaurer la fluidit\u00e9 du trafic automobile, contre la politique de r\u00e9duction de la place de la voiture men\u00e9e par Robinet",
            "France 3, 2026",
            "https://france3-regions.franceinfo.fr/grand-est/marne/reims/municipales-2026-lr-soutient-arnaud-robinet-pas-stephane-lang-a-reims-3286110.html"
        ),
        # --- Mura (Nous c'est Reims) ---
        ("solidarite", "egalite-discriminations", "mura"): (
            "D\u00e9fense des quartiers populaires, de la justice sociale, de la dignit\u00e9 et des droits humains ; politique de coop\u00e9ration et jumelages internationaux",
            "France Bleu, 2026",
            "https://www.francebleu.fr/infos/politique/municipale-2026-a-reims-sebastien-mura-ex-lfi-se-declare-candidat-avec-une-nouvelle-liste-a-gauche-9974988"
        ),
    }
)
