#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Le Havre dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== LE HAVRE ===")
insert_city(
    ville_id="le-havre",
    ville_nom="Le Havre",
    ville_cp="76600",
    candidats=[
        {"id": "philippe", "nom": "\u00c9douard Philippe", "liste": "Le Havre! (Horizons)", "programmeUrl": "https://ep2026.fr/", "programmeComplet": True, "programmePdfPath": None},
        {"id": "lecoq", "nom": "Jean-Paul Lecoq", "liste": "Mieux vivre ensemble au Havre (Front populaire havrais/PCF)", "programmeUrl": "https://jplecoq2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "keller", "nom": "Franck Keller", "liste": "Alliance UDR-RN", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "boulogne", "nom": "Charlotte Boulogne", "liste": "Le Havre Insoumis! (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "zarifian", "nom": "Sophie Zarifian", "liste": "Le Havre en d\u00e9bat (citoyen)", "programmeUrl": "https://lhendebat.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "cauchois", "nom": "Magali Cauchois", "liste": "Lutte ouvri\u00e8re \u2013 le camp des travailleurs", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Philippe ---
        ("sante", "centres-sante", "philippe"): (
            "Cr\u00e9er une p\u00e9pini\u00e8re de m\u00e9decins g\u00e9n\u00e9ralistes juniors avec logements accessibles pour leur ann\u00e9e de stage",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/normandie/seine-maritime-76/le-havre/municipales-2026-au-havre-edouard-philippe-presente-son-programme-de-continuite-4763415"
        ),
        ("sante", "prevention-sante", "philippe"): (
            "Lancer un plan majeur de pr\u00e9vention sant\u00e9 (nutrition, activit\u00e9 physique, vaccination) avec tous les acteurs de sant\u00e9",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/normandie/seine-maritime-76/le-havre/municipales-2026-au-havre-edouard-philippe-presente-son-programme-de-continuite-4763415"
        ),
        ("transports", "transports-en-commun", "philippe"): (
            "Cr\u00e9er une nouvelle ligne C de tramway de 14 km et 17 stations entre Vall\u00e9e B\u00e9reult et Montivilliers",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/normandie/seine-maritime-76/le-havre/municipales-2026-au-havre-edouard-philippe-presente-son-programme-de-continuite-4763415"
        ),
        ("transports", "tarifs-gratuite", "philippe"): (
            "\u00c9tendre la gratuit\u00e9 du transport scolaire aux lieux culturels, cr\u00e9er un abonnement famille et gratuit\u00e9 jusqu'\u00e0 6 ans",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/normandie/seine-maritime-76/le-havre/municipales-2026-au-havre-edouard-philippe-presente-son-programme-de-continuite-4763415"
        ),
        ("economie", "commerce-local", "philippe"): (
            "Soutien financier aux associations de commer\u00e7ants, pas d'augmentation de la taxe fonci\u00e8re",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/normandie/seine-maritime-76/le-havre/municipales-2026-au-havre-edouard-philippe-presente-son-programme-de-continuite-4763415"
        ),
        ("economie", "attractivite", "philippe"): (
            "Atteindre 5 millions de conteneurs au port d'ici 2030 (cr\u00e9ation de 10 000 emplois), accompagner la d\u00e9carbonation industrielle et portuaire",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/normandie/seine-maritime-76/le-havre/municipales-2026-au-havre-edouard-philippe-presente-son-programme-de-continuite-4763415"
        ),
        ("urbanisme", "amenagement-urbain", "philippe"): (
            "R\u00e9novation lourde du centre ancien est, transformation du secteur des Magasins G\u00e9n\u00e9raux avec parc et logements neufs",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/normandie/seine-maritime-76/le-havre/municipales-2026-au-havre-edouard-philippe-presente-son-programme-de-continuite-4763415"
        ),
        ("environnement", "climat-adaptation", "philippe"): (
            "Adapter la ville aux transformations climatiques, accompagner la d\u00e9carbonation des activit\u00e9s industrielles et portuaires",
            "vert.eco, 2026",
            "https://vert.eco/articles/municipales-2026-dans-les-bastions-industriels-du-havre-et-de-rouen-les-candidats-promettent-de-mettre-lecologie-au-centre"
        ),
        ("culture", "equipements-culturels", "philippe"): (
            "Installer une seconde sc\u00e8ne du Volcan \u00e0 Mare Rouge, cr\u00e9er le centre d'exposition Antoine Rufenacht en partenariat avec le mus\u00e9e Guimet",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/normandie/seine-maritime-76/le-havre/municipales-2026-au-havre-edouard-philippe-presente-son-programme-de-continuite-4763415"
        ),
        # --- Lecoq (Front populaire havrais) ---
        ("sante", "centres-sante", "lecoq"): (
            "Ouvrir un centre de sant\u00e9 municipal avec m\u00e9decins salari\u00e9s et antennes d\u00e9centralis\u00e9es ou mobiles dans les quartiers",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-jean-paul-lecoq-candidat-de-la-gauche-a-lance-sa-campagne-au-havre-8468186"
        ),
        ("transports", "tarifs-gratuite", "lecoq"): (
            "Gratuit\u00e9 des transports en commun les mercredis, samedis et pour les scolaires, vers la gratuit\u00e9 totale progressive",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-jean-paul-lecoq-candidat-de-la-gauche-a-lance-sa-campagne-au-havre-8468186"
        ),
        ("environnement", "climat-adaptation", "lecoq"): (
            "Mesurer l'impact environnemental de chaque d\u00e9cision municipale, r\u00e9viser le PLU pour la transition \u00e9cologique",
            "vert.eco, 2026",
            "https://vert.eco/articles/municipales-2026-dans-les-bastions-industriels-du-havre-et-de-rouen-les-candidats-promettent-de-mettre-lecologie-au-centre"
        ),
        ("logement", "logement-social", "lecoq"): (
            "Garantir un logement digne pour tous, lutte contre les logements insalubres et les marchands de sommeil",
            "Tendance Ouest, 2026",
            "https://www.tendanceouest.com/actualite-435542-municipales-2026-jean-paul-lecoq-sera-le-candidat-du-front-populaire-havrais"
        ),
        ("education", "ecoles-renovation", "lecoq"): (
            "Plan de r\u00e9novation des b\u00e2timents municipaux avec effort particulier sur les \u00e9coles et gymnases",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-jean-paul-lecoq-candidat-de-la-gauche-a-lance-sa-campagne-au-havre-8468186"
        ),
        ("education", "cantines-fournitures", "lecoq"): (
            "Baisser les tarifs de cantine (parmi les plus \u00e9lev\u00e9s du d\u00e9partement) pour des tarifs plus justes",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-jean-paul-lecoq-candidat-de-la-gauche-a-lance-sa-campagne-au-havre-8468186"
        ),
        ("democratie", "transparence", "lecoq"): (
            "Changement d'approche : les propositions viennent des citoyens, fin de la gouvernance descendante du maire",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-jean-paul-lecoq-candidat-de-la-gauche-a-lance-sa-campagne-au-havre-8468186"
        ),
        ("solidarite", "pouvoir-achat", "lecoq"): (
            "Nouvelle tarification progressive de l'eau avec gratuit\u00e9 des premiers m\u00e8tres cubes",
            "France Bleu Normandie, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-jean-paul-lecoq-candidat-de-la-gauche-a-lance-sa-campagne-au-havre-8468186"
        ),
        # --- Keller (UDR-RN) ---
        ("securite", "police-municipale", "keller"): (
            "Faire de la s\u00e9curit\u00e9 un axe prioritaire : renforcement de la s\u00e9curit\u00e9 publique et de la propret\u00e9",
            "Tendance Ouest, 2026",
            "https://www.tendanceouest.com/actualite-435434-le-havre-qui-est-franck-keller-candidat-de-l-alliance-udr-rn-aux-municipales"
        ),
        ("sante", "centres-sante", "keller"): (
            "Cr\u00e9ation de centres de sant\u00e9 soutenus par la municipalit\u00e9",
            "Tendance Ouest, 2026",
            "https://www.tendanceouest.com/actualite-435434-le-havre-qui-est-franck-keller-candidat-de-l-alliance-udr-rn-aux-municipales"
        ),
        ("transports", "tarifs-gratuite", "keller"): (
            "Gratuit\u00e9 des transports en commun",
            "CNews, 2026",
            "https://www.cnews.fr/france/2026-01-31/municipales-2026-qui-sont-les-candidats-la-mairie-du-havre-1809627"
        ),
        ("economie", "emploi-insertion", "keller"): (
            "Lutter contre le taux de ch\u00f4mage \u00e9lev\u00e9, am\u00e9lioration globale des conditions de vie",
            "Tendance Ouest, 2026",
            "https://www.tendanceouest.com/actualite-435434-le-havre-qui-est-franck-keller-candidat-de-l-alliance-udr-rn-aux-municipales"
        ),
        # --- Zarifian (Le Havre en debat) ---
        ("democratie", "budget-participatif", "zarifian"): (
            "Cr\u00e9er un conseil municipal citoyen tir\u00e9 au sort pour proposer et contr\u00f4ler la politique municipale",
            "Tendance Ouest, 2026",
            "https://www.tendanceouest.com/actualite-436022-municipales-2026-avec-le-havre-en-debat-sophie-zarifian-entend-redonner-du-pouvoir-aux-citoyens"
        ),
        ("democratie", "transparence", "zarifian"): (
            "Renforcer les conseils de quartier pour que les projets ne soient plus pr\u00e9sent\u00e9s d\u00e9j\u00e0 ficell\u00e9s, redonner du pouvoir aux citoyens",
            "Tendance Ouest, 2026",
            "https://www.tendanceouest.com/actualite-436022-municipales-2026-avec-le-havre-en-debat-sophie-zarifian-entend-redonner-du-pouvoir-aux-citoyens"
        ),
        ("sante", "centres-sante", "zarifian"): (
            "R\u00e9pondre au probl\u00e8me de l'acc\u00e8s aux m\u00e9decins, enjeu sant\u00e9 au c\u0153ur du programme",
            "Tendance Ouest, 2026",
            "https://www.tendanceouest.com/actualite-436022-municipales-2026-avec-le-havre-en-debat-sophie-zarifian-entend-redonner-du-pouvoir-aux-citoyens"
        ),
        # --- Cauchois (Lutte ouvriere) ---
        ("solidarite", "pouvoir-achat", "cauchois"): (
            "\u00catre les yeux et les oreilles des travailleurs au conseil municipal, d\u00e9fendre la condition ouvri\u00e8re",
            "Tendance Ouest, 2026",
            "https://www.tendanceouest.com/actualite-436029-municipales-2026-au-havre-magali-cauchois-place-la-condition-des-travailleurs-au-coeur-de-la-campagne"
        ),
    }
)
