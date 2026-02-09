#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Angers dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== ANGERS ===")
insert_city(
    ville_id="angers",
    ville_nom="Angers",
    ville_cp="49000",
    candidats=[
        {"id": "bechu", "nom": "Christophe B\u00e9chu", "liste": "Angers pour vous (Horizons/Renaissance/MoDem)", "programmeUrl": "https://www.angersbechu.fr/", "programmeComplet": True, "programmePdfPath": None},
        {"id": "laveau", "nom": "Romain Laveau", "liste": "Demain Angers (gauche unie/\u00c9cologistes)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "saeidi", "nom": "Arash Saeidi", "liste": "Angers populaire (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "lahondes", "nom": "Aurore Lahond\u00e8s", "liste": "Rassemblement National", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "leandri", "nom": "Noam Leandri", "liste": "Angers Coop\u00e9rative (citoyen)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Bechu ---
        ("securite", "police-municipale", "bechu"): (
            "Augmenter les effectifs de la police municipale de 40 \u00e0 75 agents, cr\u00e9er des \u00e9quipes de nuit et une brigade cynophile",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-christophe-bechu-presente-ses-deux-nouveaux-colistiers/"
        ),
        ("securite", "videoprotection", "bechu"): (
            "Porter le r\u00e9seau de vid\u00e9oprotection \u00e0 300 cam\u00e9ras avec un centre de supervision op\u00e9rationnel",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-christophe-bechu-presente-ses-deux-nouveaux-colistiers/"
        ),
        ("securite", "prevention-mediation", "bechu"): (
            "Adopter un plan de lutte contre les incivilit\u00e9s et armer progressivement les policiers municipaux",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-christophe-bechu-presente-lensemble-de-ses-propositions/"
        ),
        ("transports", "transports-en-commun", "bechu"): (
            "Mettre en place la gratuit\u00e9 des transports en commun",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-christophe-bechu-presente-lensemble-de-ses-propositions/"
        ),
        ("transports", "velo-mobilites-douces", "bechu"): (
            "Ouvrir une maison du v\u00e9lo et des mobilit\u00e9s pr\u00e8s de la gare, atteindre 160 km de voies cyclables s\u00e9curis\u00e9es d'ici 2030",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-christophe-bechu-presente-lensemble-de-ses-propositions/"
        ),
        ("education", "petite-enfance", "bechu"): (
            "Faire de l'enfance et la jeunesse la grande cause du mandat : petite enfance, soutien \u00e0 la parentalit\u00e9, lutte contre la surexposition aux \u00e9crans",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-christophe-bechu-devoile-lensemble-de-sa-liste/"
        ),
        ("education", "ecoles-renovation", "bechu"): (
            "Recruter 35 ATSEM suppl\u00e9mentaires pour garantir un agent par classe, investir massivement dans la r\u00e9novation des \u00e9coles des quartiers prioritaires",
            "my-angers.info, 2026",
            "https://my-angers.info/01/16/municipales-a-angers-christophe-bechu-devoile-ses-deux-premiers-colistiers-securite-et-education-en-tete/176626"
        ),
        ("education", "cantines-fournitures", "bechu"): (
            "Poursuivre la mont\u00e9e en gamme de la restauration scolaire Papillote & Compagnie (42% de bio atteint)",
            "my-angers.info, 2026",
            "https://my-angers.info/01/16/municipales-a-angers-christophe-bechu-devoile-ses-deux-premiers-colistiers-securite-et-education-en-tete/176626"
        ),
        ("education", "periscolaire-loisirs", "bechu"): (
            "Maintenir la gratuit\u00e9 des activit\u00e9s p\u00e9riscolaires",
            "my-angers.info, 2026",
            "https://my-angers.info/01/16/municipales-a-angers-christophe-bechu-devoile-ses-deux-premiers-colistiers-securite-et-education-en-tete/176626"
        ),
        ("environnement", "climat-adaptation", "bechu"): (
            "Organiser des assises de la transition \u00e9cologique, poursuivre la cr\u00e9ation de nature en ville (68 ha cr\u00e9\u00e9s)",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-christophe-bechu-presente-deux-nouvelles-colistieres-pour-la-citoyennete-et-lecologie/"
        ),
        ("economie", "commerce-local", "bechu"): (
            "Renforcer les moyens pour le commerce local avec une responsabilit\u00e9 confi\u00e9e \u00e0 Aldev (agence de d\u00e9veloppement \u00e9conomique)",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-christophe-bechu-devoile-lensemble-de-sa-liste/"
        ),
        ("culture", "equipements-culturels", "bechu"): (
            "Transformer l'h\u00f4tel de la Godeline en salle de bal et de danse",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-christophe-bechu-presente-lensemble-de-ses-propositions/"
        ),
        ("sport", "sport-pour-tous", "bechu"): (
            "Organiser des \u00e9tats g\u00e9n\u00e9raux du football pour soutenir les clubs et reconna\u00eetre leur r\u00f4le \u00e9ducatif",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-christophe-bechu-presente-lensemble-de-ses-propositions/"
        ),
        ("urbanisme", "quartiers-prioritaires", "bechu"): (
            "Renouvellement urbain majeur des quartiers Belle-Beille et Monplaisir",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-christophe-bechu-presente-lensemble-de-ses-propositions/"
        ),
        # --- Laveau (Demain Angers) ---
        ("transports", "transports-en-commun", "laveau"): (
            "Cr\u00e9er des voies r\u00e9serv\u00e9es bus/covoiturage sur les bords de Maine et une ligne de bus circulaire reliant les quartiers p\u00e9riph\u00e9riques",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-demain-angers-propose-de-repenser-la-ville-autour-du-pieton/"
        ),
        ("transports", "velo-mobilites-douces", "laveau"): (
            "Renforcer les continuit\u00e9s cyclables et s\u00e9curiser les ronds-points dangereux pour les v\u00e9los",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-demain-angers-propose-de-repenser-la-ville-autour-du-pieton/"
        ),
        ("transports", "pietons-circulation", "laveau"): (
            "Multiplier les rues aux \u00e9coles o\u00f9 la circulation est restreinte aux heures d'entr\u00e9e et sortie",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-demain-angers-propose-de-repenser-la-ville-autour-du-pieton/"
        ),
        ("transports", "tarifs-gratuite", "laveau"): (
            "Baisser les tarifs des transports en commun, notamment pour les \u00e9tudiants ; navettes gratuites depuis les parkings relais du tramway",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-demain-angers-propose-de-repenser-la-ville-autour-du-pieton/"
        ),
        ("logement", "encadrement-loyers", "laveau"): (
            "Faire reconna\u00eetre Angers en zone tendue pour plafonner les loyers",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/elections-municipales-demain-angers-fait-du-logement-lune-de-ses-priorites/"
        ),
        ("securite", "violences-femmes", "laveau"): (
            "Faire de la lutte contre les violences faites aux femmes une priorit\u00e9 municipale",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/elections-municipales-demain-angers-devoile-ses-premiers-colistiers-et-ses-priorites/"
        ),
        ("solidarite", "aide-sociale", "laveau"): (
            "Soutenir les familles monoparentales, exp\u00e9rimenter une s\u00e9curit\u00e9 sociale de l'alimentation, cr\u00e9er une \u00e9picerie sociale par quartier",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/elections-municipales-la-liste-de-gauche-demain-angers-veut-renforcer-les-solidarites/"
        ),
        ("environnement", "alimentation-durable", "laveau"): (
            "Soutenir les fermes urbaines et exp\u00e9rimenter des caisses mutualis\u00e9es pour une alimentation durable",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/elections-municipales-la-liste-de-gauche-demain-angers-veut-renforcer-les-solidarites/"
        ),
        # --- Saeidi (LFI) ---
        ("transports", "tarifs-gratuite", "saeidi"): (
            "Gratuit\u00e9 progressive des transports en commun, des premiers m\u00e8tres cubes d'eau et de la cantine scolaire",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-la-liste-angers-populaire-lance-sa-campagne-avec-le-soutien-de-deputees-lfi/"
        ),
        ("sante", "centres-sante", "saeidi"): (
            "Cr\u00e9er des centres de sant\u00e9 municipaux avec m\u00e9decins salari\u00e9s, sans d\u00e9passements d'honoraires et avec tiers payant int\u00e9gral",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-la-france-insoumise-decline-ses-propositions-sur-le-theme-de-la-sante-a-angers/"
        ),
        ("sante", "prevention-sante", "saeidi"): (
            "Cr\u00e9er une mutuelle municipale avec tarifs pr\u00e9f\u00e9rentiels et renforcer les centres de planification familiale",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-la-france-insoumise-decline-ses-propositions-sur-le-theme-de-la-sante-a-angers/"
        ),
        ("logement", "encadrement-loyers", "saeidi"): (
            "Placer Angers en zone tendue pour encadrer les loyers, augmenter la part de logements sociaux",
            "Angers Infos, 2026",
            "https://angers-infos.fr/angers-populaire-devoile-son-binome-et-lance-sa-campagne-municipale/"
        ),
        ("environnement", "espaces-verts", "saeidi"): (
            "Plan ambitieux de v\u00e9g\u00e9talisation de la ville",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-la-liste-angers-populaire-lance-sa-campagne-avec-le-soutien-de-deputees-lfi/"
        ),
        ("solidarite", "pouvoir-achat", "saeidi"): (
            "Rendre la ville moins ch\u00e8re : gratuit\u00e9 des transports, de l'eau potable vitale, de la cantine et des fournitures scolaires",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-2026-la-liste-angers-populaire-lance-sa-campagne-avec-le-soutien-de-deputees-lfi/"
        ),
        # --- Lahondes (RN) ---
        ("securite", "police-municipale", "lahondes"): (
            "Doubler les effectifs de la police municipale et armer les agents d'armes l\u00e9tales d\u00e8s 2026",
            "my-angers.info, 2025",
            "https://my-angers.info/11/21/le-rassemblement-national-devoile-sa-candidate-pour-les-elections-municipales-dangers/173970"
        ),
        ("solidarite", "pouvoir-achat", "lahondes"): (
            "Am\u00e9liorer le pouvoir d'achat des Angevins et baisser les imp\u00f4ts locaux",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/municipales-le-rassemblement-national-veut-ameliorer-la-securite-des-angevins-et-baisser-les-impots/"
        ),
        # --- Leandri (Angers Cooperative) ---
        ("transports", "tarifs-gratuite", "leandri"): (
            "Gratuit\u00e9 totale ou partielle des transports en commun (95% des citoyens consult\u00e9s favorables)",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/elections-municipales-2026-angers-cooperative-passe-a-la-vitesse-superieure/"
        ),
        ("solidarite", "aide-sociale", "leandri"): (
            "Cr\u00e9er un bureau mobile pour accompagner les habitants dans les d\u00e9marches num\u00e9riques, lutter contre la grande pauvret\u00e9",
            "Angers Villactu, 2026",
            "https://www.angers.villactu.fr/elections-municipales-2026-angers-cooperative-passe-a-la-vitesse-superieure/"
        ),
    }
)
