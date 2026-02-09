#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Dijon dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== DIJON ===")
insert_city(
    ville_id="dijon",
    ville_nom="Dijon",
    ville_cp="21000",
    candidats=[
        {"id": "koenders", "nom": "Nathalie Koenders", "liste": "Dijon \u00c9cologique, Sociale, Attractive (PS/MoDem/EELV)", "programmeUrl": "https://koenders2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "bichot", "nom": "Emmanuel Bichot", "liste": "Agir pour Dijon (LR/UDI/Horizons)", "programmeUrl": "https://www.bichot2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "coudert", "nom": "Thierry Coudert", "liste": "Rassemblement Dijonnais (UDR-RN)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "minard", "nom": "Olivier Minard", "liste": "Dijon Populaire (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "haberstrau", "nom": "Michel Haberstrau", "liste": "Dijon Change d'\u00e8re (EELV/PCF)", "programmeUrl": "https://dijonchangedere.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "goguel", "nom": "R\u00e9mi Goguel", "liste": "Dijon Avenir (citoyenne \u00e9cologiste)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "rocher", "nom": "Claire Rocher", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Koenders (PS, large rassemblement) ---
        ("securite", "police-municipale", "koenders"): (
            "Renforcer la police municipale \u00e0 104 agents mieux \u00e9quip\u00e9s et arm\u00e9s, avec pr\u00e9sence place de la R\u00e9publique jusqu'\u00e0 5h du matin",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-nathalie-koenders-entre-en-campagne-avec-un-projet-et-une-liste.html"
        ),
        ("securite", "videoprotection", "koenders"): (
            "Installer des cam\u00e9ras de surveillance devant chaque \u00e9cole et chaque cr\u00e8che",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/06/nathalie-koenders-un-meeting-a-plus-de-700-participants-dans-une-ambiance-de-campagne/"
        ),
        ("securite", "prevention-mediation", "koenders"): (
            "Renforcer la pr\u00e9vention comme pilier compl\u00e9mentaire de la politique de s\u00e9curit\u00e9",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-nathalie-koenders-entre-en-campagne-avec-un-projet-et-une-liste.html"
        ),
        ("transports", "transports-en-commun", "koenders"): (
            "Construire une troisi\u00e8me ligne de tramway m\u00e9tropolitain (T3) et augmenter la flotte de bus \u00e9lectriques",
            "Info Beaune, 2026",
            "https://www.info-beaune.com/articles/2026/02/05/14211/municipales-2026-a-dijon-nathalie-koenders-entre-en-campagne-devant-plus-de-700-dijonnais/"
        ),
        ("transports", "tarifs-gratuite", "koenders"): (
            "Baisser l'abonnement Divia pour les 18-25 ans",
            "Info Beaune, 2026",
            "https://www.info-beaune.com/articles/2026/02/05/14211/municipales-2026-a-dijon-nathalie-koenders-entre-en-campagne-devant-plus-de-700-dijonnais/"
        ),
        ("transports", "velo-mobilites-douces", "koenders"): (
            "Assurer la continuit\u00e9 des pistes cyclables sur l'ensemble de la ville",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-nathalie-koenders-entre-en-campagne-avec-un-projet-et-une-liste.html"
        ),
        ("transports", "pietons-circulation", "koenders"): (
            "\u00c9tendre les zones 30 dans tous les quartiers r\u00e9sidentiels",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/06/nathalie-koenders-un-meeting-a-plus-de-700-participants-dans-une-ambiance-de-campagne/"
        ),
        ("logement", "acces-logement", "koenders"): (
            "R\u00e9guler les locations de courte dur\u00e9e type Airbnb pour pr\u00e9server le parc r\u00e9sidentiel",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/06/nathalie-koenders-un-meeting-a-plus-de-700-participants-dans-une-ambiance-de-campagne/"
        ),
        ("education", "cantines-fournitures", "koenders"): (
            "Atteindre 75% de produits bio et locaux dans la restauration scolaire et fournir un kit de fournitures \u00e0 chaque \u00e9l\u00e8ve",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/06/nathalie-koenders-un-meeting-a-plus-de-700-participants-dans-une-ambiance-de-campagne/"
        ),
        ("education", "ecoles-renovation", "koenders"): (
            "Cr\u00e9er des rues aux \u00e9coles s\u00e9curis\u00e9es et pi\u00e9tonnis\u00e9es",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/06/nathalie-koenders-un-meeting-a-plus-de-700-participants-dans-une-ambiance-de-campagne/"
        ),
        ("education", "periscolaire-loisirs", "koenders"): (
            "Lancer un plan ambitieux contre le harc\u00e8lement scolaire",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/06/nathalie-koenders-un-meeting-a-plus-de-700-participants-dans-une-ambiance-de-campagne/"
        ),
        ("education", "petite-enfance", "koenders"): (
            "Plan ambitieux en faveur de l'enfance et de la petite enfance",
            "Info Beaune, 2026",
            "https://www.info-beaune.com/articles/2026/02/05/14211/municipales-2026-a-dijon-nathalie-koenders-entre-en-campagne-devant-plus-de-700-dijonnais/"
        ),
        ("education", "jeunesse", "koenders"): (
            "Accompagner les jeunes vers l'autonomie",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-nathalie-koenders-entre-en-campagne-avec-un-projet-et-une-liste.html"
        ),
        ("environnement", "espaces-verts", "koenders"): (
            "Planter au minimum 50 000 arbres et arbustes durant le mandat et d\u00e9simpermeabiliser le centre-ville",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-nathalie-koenders-entre-en-campagne-avec-un-projet-et-une-liste.html"
        ),
        ("environnement", "climat-adaptation", "koenders"): (
            "Transformer la Grande Orangerie de l'Arquebuse en lieu de r\u00e9f\u00e9rence d\u00e9di\u00e9 \u00e0 la transition \u00e9cologique",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-nathalie-koenders-entre-en-campagne-avec-un-projet-et-une-liste.html"
        ),
        ("sante", "centres-sante", "koenders"): (
            "Cr\u00e9er une mutuelle sant\u00e9 municipale pour les Dijonnais",
            "Info Beaune, 2026",
            "https://www.info-beaune.com/articles/2026/02/05/14211/municipales-2026-a-dijon-nathalie-koenders-entre-en-campagne-devant-plus-de-700-dijonnais/"
        ),
        ("culture", "equipements-culturels", "koenders"): (
            "R\u00e9nover les Halles centrales et le patrimoine (Saint-Philibert, Notre-Dame, Cellier de Clairvaux)",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/06/nathalie-koenders-un-meeting-a-plus-de-700-participants-dans-une-ambiance-de-campagne/"
        ),
        ("culture", "evenements-creation", "koenders"): (
            "Cr\u00e9er une f\u00eate populaire europ\u00e9enne autour de l'histoire des ducs de Bourgogne",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-nathalie-koenders-entre-en-campagne-avec-un-projet-et-une-liste.html"
        ),
        ("urbanisme", "amenagement-urbain", "koenders"): (
            "Pi\u00e9tonniser la cour d'honneur du Palais des Ducs de Bourgogne",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/06/nathalie-koenders-un-meeting-a-plus-de-700-participants-dans-une-ambiance-de-campagne/"
        ),
        ("urbanisme", "accessibilite", "koenders"): (
            "Plan ambitieux en faveur de l'accessibilit\u00e9 pour les personnes handicap\u00e9es",
            "Info Beaune, 2026",
            "https://www.info-beaune.com/articles/2026/02/05/14211/municipales-2026-a-dijon-nathalie-koenders-entre-en-campagne-devant-plus-de-700-dijonnais/"
        ),
        ("sport", "sport-pour-tous", "koenders"): (
            "R\u00e9tablir la Nuit du Sport",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-nathalie-koenders-entre-en-campagne-avec-un-projet-et-une-liste.html"
        ),
        ("solidarite", "pouvoir-achat", "koenders"): (
            "Pas d'augmentation des taux d'imp\u00f4ts municipaux",
            "Info Beaune, 2026",
            "https://www.info-beaune.com/articles/2026/02/05/14211/municipales-2026-a-dijon-nathalie-koenders-entre-en-campagne-devant-plus-de-700-dijonnais/"
        ),
        ("solidarite", "aide-sociale", "koenders"): (
            "Accompagner les familles monoparentales",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-nathalie-koenders-entre-en-campagne-avec-un-projet-et-une-liste.html"
        ),
        # --- Bichot (LR/droite unie) ---
        ("securite", "police-municipale", "bichot"): (
            "Doubler les effectifs de la police municipale \u00e0 200 agents avec brigade canine et anti-stup\u00e9fiants",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("securite", "videoprotection", "bichot"): (
            "Renforcer la vid\u00e9oprotection avec intelligence artificielle",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("securite", "prevention-mediation", "bichot"): (
            "Mener des op\u00e9rations r\u00e9guli\u00e8res contre le narcotrafic et les rod\u00e9os urbains",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("solidarite", "pouvoir-achat", "bichot"): (
            "Baisser la taxe fonci\u00e8re de 5% d\u00e8s 2026",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("environnement", "renovation-energetique", "bichot"): (
            "Exon\u00e9ration de taxe fonci\u00e8re pendant 3 ans pour les propri\u00e9taires r\u00e9alisant une r\u00e9novation \u00e9nerg\u00e9tique",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("transports", "stationnement", "bichot"): (
            "Gratuit\u00e9 de la premi\u00e8re demi-heure de stationnement et r\u00e9duction du forfait post-stationnement \u00e0 15\u20ac",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("transports", "transports-en-commun", "bichot"): (
            "Suspendre la 3\u00e8me ligne de tramway et \u00e9tendre les navettes \u00e9lectriques dans les quartiers",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("transports", "velo-mobilites-douces", "bichot"): (
            "\u00c9largir les itin\u00e9raires cyclables sur l'ensemble de la m\u00e9tropole",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("transports", "pietons-circulation", "bichot"): (
            "Am\u00e9liorer l'accessibilit\u00e9 pi\u00e9tons et r\u00e9nover les trottoirs (programme Ma rue, ma ville)",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("transports", "tarifs-gratuite", "bichot"): (
            "Gratuit\u00e9 des transports en commun pour les personnes handicap\u00e9es",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("urbanisme", "amenagement-urbain", "bichot"): (
            "R\u00e9duire les objectifs de constructions nouvelles et lutter contre la b\u00e9tonisation",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("environnement", "espaces-verts", "bichot"): (
            "Sauver le lac Kir et cr\u00e9er de nouveaux parcs canins et espaces verts",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("culture", "equipements-culturels", "bichot"): (
            "R\u00e9habiliter les Halles centrales, transformer la Cit\u00e9 de la Gastronomie et valoriser la Chartreuse de Champmol",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("sport", "equipements-sportifs", "bichot"): (
            "Reconstruire la patinoire, cr\u00e9er un parc aquatique et r\u00e9nover les salles sportives",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("sport", "sport-pour-tous", "bichot"): (
            "Accueillir des \u00e9v\u00e9nements sportifs d'envergure nationale",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("education", "petite-enfance", "bichot"): (
            "Faciliter l'acc\u00e8s aux cr\u00e8ches municipales",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("education", "ecoles-renovation", "bichot"): (
            "R\u00e9nover les \u00e9coles et \u00e9liminer les pr\u00e9fabriqu\u00e9s",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("education", "periscolaire-loisirs", "bichot"): (
            "Consulter les parents sur le retour \u00e0 la semaine de 4 jours",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("democratie", "transparence", "bichot"): (
            "R\u00e9duire le nombre d'adjoints de 22 \u00e0 15, diviser les d\u00e9penses de communication par 2 et auditer la gestion sortante",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("democratie", "budget-participatif", "bichot"): (
            "Renforcer le r\u00f4le des conseils de quartier",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("economie", "commerce-local", "bichot"): (
            "R\u00e9viser les redevances terrasses et enseignes pour soutenir les commer\u00e7ants",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("economie", "emploi-insertion", "bichot"): (
            "Faciliter l'acc\u00e8s des PME \u00e0 la commande publique municipale",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        ("economie", "attractivite", "bichot"): (
            "Soutenir les fili\u00e8res sant\u00e9 et agroalimentaire et d\u00e9fendre la zone franche de Fontaine-d'Ouche",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
        ),
        # --- Coudert (UDR-RN) ---
        ("securite", "police-municipale", "coudert"): (
            "Doubler les effectifs de la police municipale active 24h/24 avec \u00e9quipes cynophiles",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2025/08/18/thierry-coudert-a-loffensive-sur-la-securite-que-valent-vraiment-ses-6-propositions/"
        ),
        ("securite", "videoprotection", "coudert"): (
            "Multiplier par cinq le nombre de cam\u00e9ras de vid\u00e9oprotection",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2025/08/18/thierry-coudert-a-loffensive-sur-la-securite-que-valent-vraiment-ses-6-propositions/"
        ),
        ("solidarite", "aide-sociale", "coudert"): (
            "Supprimer les aides sociales municipales pour les personnes condamn\u00e9es",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2025/08/18/thierry-coudert-a-loffensive-sur-la-securite-que-valent-vraiment-ses-6-propositions/"
        ),
        ("solidarite", "pouvoir-achat", "coudert"): (
            "Baisser la taxe fonci\u00e8re de 5%",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/30/municipales-a-dijon-thierry-coudert-devoile-ses-premiers-colistiers/"
        ),
        ("democratie", "transparence", "coudert"): (
            "R\u00e9duire les indemnit\u00e9s d'\u00e9lus",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/30/municipales-a-dijon-thierry-coudert-devoile-ses-premiers-colistiers/"
        ),
        ("transports", "transports-en-commun", "coudert"): (
            "S'opposer \u00e0 la 3\u00e8me ligne de tramway et refondre les lignes de bus avec services nocturnes",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/30/municipales-a-dijon-thierry-coudert-devoile-ses-premiers-colistiers/"
        ),
        ("transports", "stationnement", "coudert"): (
            "Une heure gratuite de stationnement en surface, deux heures en parking souterrain",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/30/municipales-a-dijon-thierry-coudert-devoile-ses-premiers-colistiers/"
        ),
        ("urbanisme", "amenagement-urbain", "coudert"): (
            "Mettre fin \u00e0 la b\u00e9tonisation et renforcer la v\u00e9g\u00e9talisation de la ville",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2025/08/04/municipales-2026-entretien-avec-thierry-coudert-tete-de-liste-udr-rn-a-dijon/"
        ),
        ("environnement", "espaces-verts", "coudert"): (
            "R\u00e9fl\u00e9chir au retour de l'eau en surface, notamment pour le Suzon",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/30/municipales-a-dijon-thierry-coudert-devoile-ses-premiers-colistiers/"
        ),
        ("economie", "commerce-local", "coudert"): (
            "Cr\u00e9er une task force municipale pour l'attractivit\u00e9 et une SEM contre la vacance commerciale",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/30/municipales-a-dijon-thierry-coudert-devoile-ses-premiers-colistiers/"
        ),
        ("culture", "equipements-culturels", "coudert"): (
            "Cr\u00e9er un fonds municipal pour r\u00e9nover le patrimoine et arr\u00eater les d\u00e9penses pour la Cit\u00e9 de la gastronomie",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/30/municipales-a-dijon-thierry-coudert-devoile-ses-premiers-colistiers/"
        ),
        ("democratie", "vie-associative", "coudert"): (
            "Redonner un vrai r\u00f4le aux comit\u00e9s de quartier",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2025/08/04/municipales-2026-entretien-avec-thierry-coudert-tete-de-liste-udr-rn-a-dijon/"
        ),
        # --- Minard (LFI) ---
        ("transports", "tarifs-gratuite", "minard"): (
            "Gratuit\u00e9 progressive des transports en commen\u00e7ant par les jeunes et les personnes pr\u00e9caires",
            "France Bleu Bourgogne, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-ici-bourgogne/municipales-a-dijon-la-france-insoumise-et-sa-tete-de-liste-olivier-minard-proposent-la-gratuite-des-transports-5116616"
        ),
        ("transports", "transports-en-commun", "minard"): (
            "Modifier le trac\u00e9 de la troisi\u00e8me ligne de tramway",
            "France Bleu Bourgogne, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-la-france-insoumise-entre-en-campagne-a-dijon-et-presente-son-programme-4414470"
        ),
        ("logement", "logement-social", "minard"): (
            "Geler les loyers des logements sociaux comme premi\u00e8re mesure",
            "France Bleu Bourgogne, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-la-france-insoumise-entre-en-campagne-a-dijon-et-presente-son-programme-4414470"
        ),
        ("logement", "encadrement-loyers", "minard"): (
            "Mettre en place l'encadrement des loyers \u00e0 Dijon",
            "France Bleu Bourgogne, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-la-france-insoumise-entre-en-campagne-a-dijon-et-presente-son-programme-4414470"
        ),
        ("logement", "acces-logement", "minard"): (
            "Encadrer strictement les locations touristiques de courte dur\u00e9e (Airbnb)",
            "France Bleu Bourgogne, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-la-france-insoumise-entre-en-campagne-a-dijon-et-presente-son-programme-4414470"
        ),
        ("education", "cantines-fournitures", "minard"): (
            "Cantine gratuite et biologique pour tous les \u00e9l\u00e8ves et \u00e9limination des emballages \u00e0 la cuisine centrale",
            "France Bleu Bourgogne, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-ici-bourgogne/municipales-a-dijon-la-france-insoumise-et-sa-tete-de-liste-olivier-minard-proposent-la-gratuite-des-transports-5116616"
        ),
        ("securite", "prevention-mediation", "minard"): (
            "Augmenter les effectifs d'\u00e9ducateurs dans les quartiers plut\u00f4t que la r\u00e9pression polici\u00e8re",
            "France Bleu Bourgogne, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-ici-bourgogne/municipales-a-dijon-la-france-insoumise-et-sa-tete-de-liste-olivier-minard-proposent-la-gratuite-des-transports-5116616"
        ),
        ("securite", "police-municipale", "minard"): (
            "Police municipale d\u00e9sarm\u00e9e, mod\u00e8le de proximit\u00e9 et de lien social",
            "France Bleu Bourgogne, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-la-france-insoumise-entre-en-campagne-a-dijon-et-presente-son-programme-4414470"
        ),
        ("democratie", "budget-participatif", "minard"): (
            "Instaurer un r\u00e9f\u00e9rendum d'initiative citoyenne (RIC) local",
            "France Bleu Bourgogne, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-la-france-insoumise-entre-en-campagne-a-dijon-et-presente-son-programme-4414470"
        ),
        ("economie", "emploi-insertion", "minard"): (
            "Syst\u00e8me de points favorisant les entreprises d'insertion et \u00e9cologiques dans les march\u00e9s publics",
            "France Bleu Bourgogne, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-la-france-insoumise-entre-en-campagne-a-dijon-et-presente-son-programme-4414470"
        ),
        # --- Haberstrau (EELV/PCF) ---
        ("transports", "tarifs-gratuite", "haberstrau"): (
            "Transports gratuits pour les moins de 26 ans, les personnes handicap\u00e9es et les b\u00e9n\u00e9ficiaires de minima sociaux",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("transports", "transports-en-commun", "haberstrau"): (
            "Remettre \u00e0 plat le trac\u00e9 de la 3e ligne de tramway avec une nouvelle concertation citoyenne",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("transports", "velo-mobilites-douces", "haberstrau"): (
            "D\u00e9ployer un r\u00e9seau pi\u00e9ton-v\u00e9lo continu, s\u00e9curis\u00e9 et confortable sur toute la ville",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("environnement", "espaces-verts", "haberstrau"): (
            "D\u00e9simpermeabilisation massive, plantations d'arbres et micro-for\u00eats, espace nature \u00e0 moins de 5 minutes et r\u00e9ouverture du Suzon",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("environnement", "climat-adaptation", "haberstrau"): (
            "R\u00e9vision du PLUi-HD avec objectif z\u00e9ro artificialisation brute et arr\u00eat de la phase 2 de l'\u00e9coquartier des Mara\u00eechers",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("environnement", "alimentation-durable", "haberstrau"): (
            "Cr\u00e9er une s\u00e9curit\u00e9 sociale de l'alimentation locale \u00e0 l'\u00e9chelle dijonnaise",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("environnement", "renovation-energetique", "haberstrau"): (
            "R\u00e9novation thermique massive avec exon\u00e9ration de taxe fonci\u00e8re pour les propri\u00e9taires engag\u00e9s",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("logement", "encadrement-loyers", "haberstrau"): (
            "Demander le classement en zone tendue pour encadrer les loyers et r\u00e9guler Airbnb",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("logement", "logement-social", "haberstrau"): (
            "Porter la part de logements sociaux \u00e0 25% via r\u00e9habilitation de logements vacants",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("education", "petite-enfance", "haberstrau"): (
            "Renforcer les ATSEM en maternelle pour atteindre une ATSEM par classe",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("education", "ecoles-renovation", "haberstrau"): (
            "Plan acc\u00e9l\u00e9r\u00e9 R\u00e9nov'\u00c9cole avec v\u00e9g\u00e9talisation, adaptation aux chaleurs et pi\u00e9tonnisation des abords",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("sante", "centres-sante", "haberstrau"): (
            "Implanter des structures m\u00e9dicales de proximit\u00e9 dans les quartiers d\u00e9ficitaires",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("sante", "prevention-sante", "haberstrau"): (
            "Cr\u00e9er un tiers-lieu sant\u00e9 associant professionnels et habitants",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("securite", "prevention-mediation", "haberstrau"): (
            "Dispositif permanent de m\u00e9diation avec \u00e9ducateurs sp\u00e9cialis\u00e9s et m\u00e9diateurs professionnels",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("securite", "police-municipale", "haberstrau"): (
            "Police municipale de proximit\u00e9 sans d\u00e9magogie s\u00e9curitaire",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-les-propositions-de-michel-haberstrau-pour-les-municipales.html"
        ),
        ("democratie", "budget-participatif", "haberstrau"): (
            "Assembl\u00e9es citoyennes trimestrielles cod\u00e9cisionnaires et convention citoyenne Dijon cap 2050",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-les-propositions-de-michel-haberstrau-pour-les-municipales.html"
        ),
        ("democratie", "services-publics", "haberstrau"): (
            "Reprendre en gestion publique l'eau, les d\u00e9chets, les transports et la petite enfance",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("democratie", "vie-associative", "haberstrau"): (
            "Porter \u00e0 10% du budget municipal la part d\u00e9di\u00e9e aux associations culturelles, sportives et solidaires",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        ("economie", "commerce-local", "haberstrau"): (
            "Contr\u00f4le des baux commerciaux et plafonnement des loyers pour favoriser la diversit\u00e9 commerciale",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-les-propositions-de-michel-haberstrau-pour-les-municipales.html"
        ),
        ("economie", "emploi-insertion", "haberstrau"): (
            "Soutenir les SCOP et SCIC, aides aux entreprises conditionn\u00e9es \u00e0 des crit\u00e8res sociaux et environnementaux",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-les-propositions-de-michel-haberstrau-pour-les-municipales.html"
        ),
        ("urbanisme", "accessibilite", "haberstrau"): (
            "Z\u00e9ro rue non accessible aux personnes \u00e0 mobilit\u00e9 r\u00e9duite",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-les-propositions-de-michel-haberstrau-pour-les-municipales.html"
        ),
        ("urbanisme", "quartiers-prioritaires", "haberstrau"): (
            "Meilleure desserte des quartiers enclav\u00e9s comme Fontaine-d'Ouche",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/01/16/municipales-2026-a-dijon-la-liste-dijon-change-dere-devoile-un-programme-axe-sur-la-justice-sociale-et-la-transition-ecologique/"
        ),
        # --- Goguel (citoyenne ecologiste) ---
        ("environnement", "climat-adaptation", "goguel"): (
            "Transition vers un mod\u00e8le de post-croissance fond\u00e9 sur la sobri\u00e9t\u00e9 \u00e9nerg\u00e9tique et mat\u00e9rielle, protection contre les vagues de chaleur",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/02/remi-goguel-et-mathilde-mouchet-conduisent-la-liste-citoyenne-dijon-avenir/"
        ),
        ("economie", "emploi-insertion", "goguel"): (
            "Relocalisation de l'\u00e9conomie et cr\u00e9ation d'emplois locaux via l'\u00e9conomie circulaire et r\u00e9g\u00e9n\u00e9rative",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/02/remi-goguel-et-mathilde-mouchet-conduisent-la-liste-citoyenne-dijon-avenir/"
        ),
        ("environnement", "alimentation-durable", "goguel"): (
            "Acc\u00e8s de tous \u00e0 une alimentation de qualit\u00e9",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/02/remi-goguel-et-mathilde-mouchet-conduisent-la-liste-citoyenne-dijon-avenir/"
        ),
        ("logement", "acces-logement", "goguel"): (
            "Garantir un logement digne pour tous les Dijonnais",
            "Dijon Actualit\u00e9s, 2026",
            "https://dijon-actualites.fr/2026/02/02/remi-goguel-et-mathilde-mouchet-conduisent-la-liste-citoyenne-dijon-avenir/"
        ),
        # --- Rocher (LO) ---
        ("solidarite", "pouvoir-achat", "rocher"): (
            "Augmenter les salaires, interdire les licenciements et r\u00e9partir le travail entre tous",
            "Lutte Ouvri\u00e8re, 2026",
            "https://www.lutte-ouvriere.org/portail/municipales-2026/candidats.html"
        ),
        ("logement", "logement-social", "rocher"): (
            "Obliger les bailleurs sociaux \u00e0 r\u00e9parer et entretenir les logements des quartiers populaires",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/municipales-a-dijon-si-on-avait-une-mairie-avec-des-ouvriers-revolutionnaires-a-sa-tete-ca-changerait-la-donne-indique-claire-rocher.html"
        ),
        ("democratie", "services-publics", "rocher"): (
            "Mettre la mairie au service des travailleurs et des quartiers populaires",
            "Infos Dijon, 2026",
            "https://www.infos-dijon.com/news/vie-locale/vie-locale/municipales-a-dijon-si-on-avait-une-mairie-avec-des-ouvriers-revolutionnaires-a-sa-tete-ca-changerait-la-donne-indique-claire-rocher.html"
        ),
    }
)
