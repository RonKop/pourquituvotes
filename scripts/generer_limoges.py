#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Limoges dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== LIMOGES ===")
insert_city(
    ville_id="limoges",
    ville_nom="Limoges",
    ville_cp="87000",
    candidats=[
        {"id": "lombertie", "nom": "\u00c9mile-Roger Lombertie", "liste": "LR (Droite sortante)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "guerin", "nom": "Guillaume Gu\u00e9rin", "liste": "LR dissident (Limoges M\u00e9tropole)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "maudet", "nom": "Damien Maudet", "liste": "Limoges Front Populaire (LFI-EELV)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "miguel", "nom": "Thierry Miguel", "liste": "Pour Limoges (PS-PCF-Place publique)", "programmeUrl": "https://www.pourlimoges.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "leonie", "nom": "Vincent L\u00e9onie", "liste": "R\u00e9unir (Centre)", "programmeUrl": "https://www.reunir-limoges.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "freychet", "nom": "Albin Freychet", "liste": "Limoges en Grand (RN)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "benzoni", "nom": "Julie Benzoni", "liste": "R\u00eavons Limoges (citoyen)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "faucon", "nom": "\u00c9lisabeth Faucon", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Lombertie (maire sortant) ---
        ("urbanisme", "quartiers-prioritaires", "lombertie"): (
            "Poursuite de la r\u00e9novation urbaine avec l'ANRU dans les quartiers Val de l'Aurence Sud et Beaubreuil",
            "France 3 Nouvelle-Aquitaine, 2026",
            "https://france3-regions.franceinfo.fr/nouvelle-aquitaine/haute-vienne/limoges/emile-roger-lombertie-se-declare-candidat-a-la-mairie-de-limoges-pour-les-prochaines-elections-municipales-3277712.html"
        ),
        ("economie", "attractivite", "lombertie"): (
            "Continuer la dynamique \u00e9conomique avec +4,4% d'emplois priv\u00e9s et un solde positif de 4 400 entreprises sur le mandat",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/infos/politique/je-n-ai-pas-transforme-limoges-pendant-2-mandatures-pour-abandonner-emile-roger-lombertie-determine-et-en-campagne-6978880"
        ),
        # --- Guerin (LR dissident) ---
        ("securite", "police-municipale", "guerin"): (
            "Renforcer les effectifs de la police municipale et cr\u00e9er un centre de supervision m\u00e9tropolitain pour mutualiser la vid\u00e9oprotection",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-limousin/municipales-a-limoges-guillaume-guerin-assez-meurtri-par-la-candidature-de-lombertie-veut-creer-une-dynamique-2492960"
        ),
        ("economie", "attractivite", "guerin"): (
            "Attirer les entreprises : implantation d'Herm\u00e8s et du groupe IMA en centre-ville, soit environ 800 emplois",
            "Flash FM, 2026",
            "https://www.flashfm.fr/municipales-guillaume-guerin-veut-creer-une-dynamique"
        ),
        # --- Maudet (LFI) ---
        ("transports", "tarifs-gratuite", "maudet"): (
            "Gratuit\u00e9 des transports en commun pour tous les Limougeauds",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-limousin/municipales-limoges-front-populaire-un-debut-de-programme-mais-pas-encore-de-tete-de-liste-5996749"
        ),
        ("transports", "velo-mobilites-douces", "maudet"): (
            "D\u00e9veloppement massif des pistes cyclables et pi\u00e9tonnisation du centre-ville",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-limousin/municipales-limoges-front-populaire-un-debut-de-programme-mais-pas-encore-de-tete-de-liste-5996749"
        ),
        ("sante", "centres-sante", "maudet"): (
            "Cr\u00e9ation de centres de sant\u00e9 municipaux pour lutter contre la d\u00e9sertification m\u00e9dicale",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-limousin/municipales-2026-salle-comble-pour-le-premier-meeting-de-damien-maudet-et-sa-liste-limoges-front-populaire-6347710"
        ),
        ("economie", "commerce-local", "maudet"): (
            "Concertations sur les baux commerciaux pour r\u00e9soudre la vacance commerciale en centre-ville",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-limousin/municipales-2026-salle-comble-pour-le-premier-meeting-de-damien-maudet-et-sa-liste-limoges-front-populaire-6347710"
        ),
        ("solidarite", "aide-sociale", "maudet"): (
            "Mettre \u00e0 disposition des b\u00e2timents municipaux pour h\u00e9berger en urgence les parents d'enfants sans domicile",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-limousin/municipales-2026-salle-comble-pour-le-premier-meeting-de-damien-maudet-et-sa-liste-limoges-front-populaire-6347710"
        ),
        ("democratie", "transparence", "maudet"): (
            "Plafonner les indemnit\u00e9s en cas de cumul de mandats \u00e0 2 800 \u20ac maximum",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-limousin/municipales-2026-candidat-a-limoges-damien-maudet-s-explique-sur-les-indemnites-et-le-cumul-des-mandats-7694759"
        ),
        # --- Miguel (PS) ---
        ("securite", "prevention-mediation", "miguel"): (
            "Lutte contre le narcotrafic par une meilleure coordination entre police nationale, police municipale et services fiscaux",
            "Pour Limoges, 2026",
            "https://www.pourlimoges.fr/"
        ),
        ("environnement", "climat-adaptation", "miguel"): (
            "Reconnecter Limoges \u00e0 la rivi\u00e8re, cr\u00e9er des fontaines et jeux d'eau pour lutter contre les \u00eelots de chaleur urbains",
            "Pour Limoges, 2026",
            "https://www.pourlimoges.fr/"
        ),
        ("education", "cantines-fournitures", "miguel"): (
            "Augmenter la part de bio et de produits locaux dans les cantines scolaires et lutter contre le gaspillage alimentaire",
            "Pour Limoges, 2026",
            "https://www.pourlimoges.fr/"
        ),
        ("transports", "transports-en-commun", "miguel"): (
            "Am\u00e9liorer les liaisons ferroviaires pour d\u00e9senclaver Limoges et r\u00e9duire son isolement",
            "Pour Limoges, 2026",
            "https://www.pourlimoges.fr/"
        ),
        ("economie", "commerce-local", "miguel"): (
            "Cr\u00e9er une soci\u00e9t\u00e9 publique locale pour lutter contre la vacance commerciale en centre-ville",
            "Pour Limoges, 2026",
            "https://www.pourlimoges.fr/"
        ),
        ("culture", "equipements-culturels", "miguel"): (
            "R\u00e9viser les budgets pour restaurer l'acc\u00e8s \u00e0 la culture pour tous les Limougeauds",
            "Pour Limoges, 2026",
            "https://www.pourlimoges.fr/"
        ),
        # --- Leonie (Centre) ---
        ("education", "cantines-fournitures", "leonie"): (
            "Gratuit\u00e9 des fournitures scolaires pour tous les \u00e9l\u00e8ves (co\u00fbt estim\u00e9 : 600 000 \u00e0 700 000 \u20ac) et baisse du tarif cantine \u00e0 4,40 \u20ac maximum",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-limousin/limoges-la-renovation-des-ecoles-au-coeur-de-l-election-municipale-2146396"
        ),
        ("education", "ecoles-renovation", "leonie"): (
            "R\u00e9nover l'int\u00e9gralit\u00e9 des \u00e9coles de Limoges d'ici 2030 : plan ambitieux de remise aux normes",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-limousin/limoges-la-renovation-des-ecoles-au-coeur-de-l-election-municipale-2146396"
        ),
        # --- Freychet (RN) ---
        ("securite", "police-municipale", "freychet"): (
            "Faire de la s\u00e9curit\u00e9 la priorit\u00e9 n\u00b01 : la d\u00e9linquance s'est d\u00e9grad\u00e9e et est devenue le point noir pour l'image de la ville",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-limousin/albin-freychet-candidat-rn-aux-municipales-2026-a-limoges-veut-creer-un-grand-rassemblement-de-patriotes-8376068"
        ),
        ("economie", "commerce-local", "freychet"): (
            "Redynamiser le commerce de centre-ville et faire de Limoges un point d'attraction touristique estival",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-limousin/albin-freychet-candidat-rn-aux-municipales-2026-a-limoges-veut-creer-un-grand-rassemblement-de-patriotes-8376068"
        ),
        ("sante", "centres-sante", "freychet"): (
            "Garantir l'acc\u00e8s aux soins et renforcer la pr\u00e9sence des services publics de sant\u00e9 face \u00e0 la d\u00e9sertification m\u00e9dicale",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-limousin/albin-freychet-candidat-rn-aux-municipales-2026-a-limoges-veut-creer-un-grand-rassemblement-de-patriotes-8376068"
        ),
        ("democratie", "budget-participatif", "freychet"): (
            "R\u00e9f\u00e9rendum d'initiative locale sur les sujets engageant les finances de la Ville, comme le projet du nouveau Beaublanc",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-limousin/albin-freychet-candidat-rn-aux-municipales-2026-a-limoges-veut-creer-un-grand-rassemblement-de-patriotes-8376068"
        ),
        ("education", "ecoles-renovation", "freychet"): (
            "Auditer chaque \u00e9cole avant d'estimer le co\u00fbt des r\u00e9parations n\u00e9cessaires",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-limousin/limoges-la-renovation-des-ecoles-au-coeur-de-l-election-municipale-2146396"
        ),
        ("urbanisme", "amenagement-urbain", "freychet"): (
            "R\u00e9habiliter les friches urbaines : friche des Ponts et ancienne clinique du Colombier comme priorit\u00e9s d'am\u00e9nagement",
            "France Bleu Limousin, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-limousin/albin-freychet-candidat-rn-aux-municipales-2026-a-limoges-veut-creer-un-grand-rassemblement-de-patriotes-8376068"
        ),
    }
)
