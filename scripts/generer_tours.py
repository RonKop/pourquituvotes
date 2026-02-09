#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Tours dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== TOURS ===")
insert_city(
    ville_id="tours",
    ville_nom="Tours",
    ville_cp="37000",
    candidats=[
        {"id": "denis", "nom": "Emmanuel Denis", "liste": "Tours Inspire 2026 (EELV/PS/PCF)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "quinton", "nom": "Marie Quinton", "liste": "Faire mieux pour Tours (LFI)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "bouchet", "nom": "Christophe Bouchet", "liste": "Tours pour tous (Centre-droit/LR)", "programmeUrl": "https://tourspourtous.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "alfandari", "nom": "Henri Alfandari", "liste": "Naturellement Tours (Horizons)", "programmeUrl": "https://www.naturellement-tours.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "pierre", "nom": "Benoist Pierre", "liste": "Je m'engage pour Tours (Divers centre)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "nikolic", "nom": "Aleksandar Nikolic", "liste": "Rassemblement National", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "rouzier", "nom": "Bertrand Rouzier", "liste": "Tours, vivante ! (PRG)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "jouhannaud", "nom": "Thomas Jouhannaud", "liste": "Lutte Ouvri\u00e8re", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Denis (EELV, maire sortant) ---
        ("securite", "police-municipale", "denis"): (
            "Maintien de la ligne actuelle avec accent sur la pr\u00e9vention plut\u00f4t que l'augmentation massive des effectifs",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/municipales-a-tours-surenchere-de-campagne-autour-de-la-police-municipale/"
        ),
        ("transports", "transports-en-commun", "denis"): (
            "Mener \u00e0 bien la 2e ligne de tramway et acc\u00e9l\u00e9rer le RER m\u00e9tropolitain pour les trajets quotidiens",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-demmanuel-denis-candidat-aux-municipales-a-tours/"
        ),
        ("transports", "tarifs-gratuite", "denis"): (
            "Gratuit\u00e9 progressive des transports le samedi pour soutenir le commerce et tester le r\u00e9seau",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-demmanuel-denis-candidat-aux-municipales-a-tours/"
        ),
        ("transports", "pietons-circulation", "denis"): (
            "Plan pi\u00e9ton pour la marchabilit\u00e9, pens\u00e9 pour les enfants, les seniors et les personnes handicap\u00e9es",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-demmanuel-denis-candidat-aux-municipales-a-tours/"
        ),
        ("environnement", "espaces-verts", "denis"): (
            "Plantation de 40 000 arbres suppl\u00e9mentaires et cr\u00e9ation de nouveaux parcs et jardins",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-demmanuel-denis-candidat-aux-municipales-a-tours/"
        ),
        ("environnement", "renovation-energetique", "denis"): (
            "Acc\u00e9l\u00e9rer l'\u00e9nergie solaire et la r\u00e9habilitation thermique des \u00e9coles, cr\u00e8ches et \u00e9quipements publics",
            "Info Tours, 2025",
            "https://info-tours.fr/tours/2025/12/12/municipales-2026-le-maire-de-tours-emmanuel-denis-officiellement-candidat-a-sa-succession/"
        ),
        ("sante", "centres-sante", "denis"): (
            "Cr\u00e9ation de nouveaux centres de sant\u00e9 municipaux pour compenser 40% de d\u00e9parts de m\u00e9decins pr\u00e9vus",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-demmanuel-denis-candidat-aux-municipales-a-tours/"
        ),
        ("democratie", "budget-participatif", "denis"): (
            "Doublement de l'enveloppe du budget participatif jusqu'\u00e0 1 million d'euros par an",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-demmanuel-denis-candidat-aux-municipales-a-tours/"
        ),
        ("democratie", "transparence", "denis"): (
            "Mise en place du R\u00e9f\u00e9rendum d'Initiative Citoyenne pour permettre aux Tourangeaux de peser sur les grands projets",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-demmanuel-denis-candidat-aux-municipales-a-tours/"
        ),
        ("economie", "emploi-insertion", "denis"): (
            "Nouvelles actions pour l'emploi et acc\u00e9l\u00e9ration des dispositifs d'insertion",
            "France Bleu Touraine, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-touraine/emmanuel-denis-officiellement-candidat-a-un-second-mandat-la-ville-a-change-9855228"
        ),
        ("sport", "equipements-sportifs", "denis"): (
            "Plan massif d'investissement pour les infrastructures sportives et r\u00e9flexion sur une future Arena",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-demmanuel-denis-candidat-aux-municipales-a-tours/"
        ),
        ("logement", "logement-social", "denis"): (
            "Maintien de l'effort de construction de logements sociaux malgr\u00e9 la crise du secteur",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-demmanuel-denis-candidat-aux-municipales-a-tours/"
        ),
        # --- Quinton (LFI) ---
        ("logement", "acces-logement", "quinton"): (
            "R\u00e9quisitionner les logements vacants et mettre en place l'encadrement des loyers",
            "La France Insoumise, 2026",
            "https://linsoumission.fr/2025/12/01/baisse-loyers-tribune-lfi/"
        ),
        ("logement", "logement-social", "quinton"): (
            "Augmenter le parc de logements publics et d\u00e9velopper la propri\u00e9t\u00e9 non sp\u00e9culative via les offices fonciers solidaires",
            "LFI, 2026",
            "https://programme.lafranceinsoumise.fr/municipales-2026/"
        ),
        ("transports", "tarifs-gratuite", "quinton"): (
            "R\u00e9duction des tarifs vers la gratuit\u00e9, en commen\u00e7ant par les moins de 25 ans et les revenus modestes",
            "LFI, 2026",
            "https://programme.lafranceinsoumise.fr/municipales-2026/"
        ),
        ("education", "cantines-fournitures", "quinton"): (
            "Cantines scolaires bio et locales avec option v\u00e9g\u00e9tarienne quotidienne, gratuit\u00e9 progressive",
            "LFI, 2026",
            "https://programme.lafranceinsoumise.fr/municipales-2026/"
        ),
        ("solidarite", "pouvoir-achat", "quinton"): (
            "Lutte contre la vie ch\u00e8re avec renforcement des services publics locaux gratuits",
            "Anadolu Agency, 2026",
            "https://www.aa.com.tr/fr/politique/-france-municipales-2026-lfi-lance-sa-campagne-et-promet-une-rupture-sociale-/3751846"
        ),
        # --- Bouchet (Centre-droit/LR) ---
        ("securite", "police-municipale", "bouchet"): (
            "Porter les effectifs de la police municipale \u00e0 130 agents (contre 93 actuellement)",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/municipales-a-tours-surenchere-de-campagne-autour-de-la-police-municipale/"
        ),
        ("securite", "prevention-mediation", "bouchet"): (
            "Retour de l'\u00e9clairage public toute la nuit avec conversion int\u00e9grale en LED pour lutter contre l'ins\u00e9curit\u00e9",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/municipales-a-tours-christophe-bouchet-se-voit-en-haut-de-laffiche/"
        ),
        ("transports", "pietons-circulation", "bouchet"): (
            "R\u00e9ouverture du pont Wilson \u00e0 la circulation automobile dans le sens nord-sud",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/municipales-a-tours-christophe-bouchet-se-voit-en-haut-de-laffiche/"
        ),
        ("transports", "velo-mobilites-douces", "bouchet"): (
            "Remaniement du plan v\u00e9lo avec 40 km d'infrastructures cyclables repens\u00e9es",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/municipales-a-tours-christophe-bouchet-se-voit-en-haut-de-laffiche/"
        ),
        ("urbanisme", "amenagement-urbain", "bouchet"): (
            "Triplement du budget voirie pour r\u00e9nover les routes et trottoirs de la ville",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/municipales-a-tours-christophe-bouchet-se-voit-en-haut-de-laffiche/"
        ),
        ("sport", "equipements-sportifs", "bouchet"): (
            "Plan d'urgence : r\u00e9novation du stade Tonnell\u00e9 avec extension \u00e0 5 500 places (co\u00fbt 15 M\u20ac)",
            "Info Tours, 2025",
            "https://info-tours.fr/tours/2025/05/07/municipales-2026-a-tours-les-premieres-propositions-du-candidat-christophe-bouchet/"
        ),
        ("education", "periscolaire-loisirs", "bouchet"): (
            "Activit\u00e9s p\u00e9dagogiques, culturelles et sportives propos\u00e9es aux \u00e9l\u00e8ves hors temps scolaire",
            "France Bleu Touraine, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-tours-christophe-bouchet-lance-sa-campagne-mais-croit-toujours-en-une-union-de-la-droite-3848920"
        ),
        ("democratie", "transparence", "bouchet"): (
            "Z\u00e9ro hausse des imp\u00f4ts locaux pendant tout le mandat",
            "France Bleu Touraine, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-christophe-bouchet-annonce-sa-candidature-a-la-mairie-de-tours-3373653"
        ),
        # --- Alfandari (Horizons) ---
        ("securite", "police-municipale", "alfandari"): (
            "Augmenter imm\u00e9diatement les effectifs \u00e0 120 agents avec recrutement plus attractif",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/municipales-a-tours-surenchere-de-campagne-autour-de-la-police-municipale/"
        ),
        ("securite", "videoprotection", "alfandari"): (
            "G\u00e9n\u00e9ralisation de la vid\u00e9osurveillance avec infrarouge et \u00e9clairages LED \u00e0 d\u00e9tecteurs de mouvement",
            "France Bleu Touraine, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-touraine/l-invite-d-ici-matin-8950200"
        ),
        ("transports", "transports-en-commun", "alfandari"): (
            "Arr\u00eat des travaux de la ligne B du tramway pour r\u00e9viser le trac\u00e9 et r\u00e9duire les co\u00fbts",
            "Info Tours, 2025",
            "https://info-tours.fr/tours/2025/10/06/municipales-2026-a-tours-arena-de-20-000-places-referendums-tram-les-premieres-propositions-dhenri-alfandari/"
        ),
        ("sport", "equipements-sportifs", "alfandari"): (
            "Construction d'une ar\u00e9na de 20 000 places pour football, concerts et \u00e9v\u00e9nements sportifs",
            "Info Tours, 2025",
            "https://info-tours.fr/tours/2025/10/06/municipales-2026-a-tours-arena-de-20-000-places-referendums-tram-les-premieres-propositions-dhenri-alfandari/"
        ),
        ("urbanisme", "amenagement-urbain", "alfandari"): (
            "Grand plan d'embellissement : verdissement, r\u00e9novation fa\u00e7ades et devantures de commerces",
            "France Bleu Touraine, 2026",
            "https://www.francebleu.fr/infos/politique/le-depute-horizons-henri-alfandari-candidat-aux-municipales-a-tours-7885848"
        ),
        ("environnement", "espaces-verts", "alfandari"): (
            "V\u00e9g\u00e9talisation de chaque quartier avec cr\u00e9ation d'\u00eelots de fra\u00eecheur",
            "France Bleu Touraine, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-touraine/l-invite-d-ici-matin-8950200"
        ),
        ("democratie", "transparence", "alfandari"): (
            "Consultations publiques et r\u00e9f\u00e9rendums locaux sur les grands projets (tram, vid\u00e9oprotection)",
            "Info Tours, 2025",
            "https://info-tours.fr/tours/2025/10/06/municipales-2026-a-tours-arena-de-20-000-places-referendums-tram-les-premieres-propositions-dhenri-alfandari/"
        ),
        ("economie", "commerce-local", "alfandari"): (
            "Soutien aux commerces : la mairie partenaire du d\u00e9veloppement local avec aide \u00e0 la r\u00e9novation des devantures",
            "Naturellement Tours, 2026",
            "https://www.naturellement-tours.fr/"
        ),
        # --- Pierre (Divers centre) ---
        ("securite", "police-municipale", "pierre"): (
            "Porter les effectifs \u00e0 140 agents d'ici 2033, soit 50 recrutements par paliers (co\u00fbt 2 M\u20ac/an)",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/municipales-a-tours-surenchere-de-campagne-autour-de-la-police-municipale/"
        ),
        ("transports", "transports-en-commun", "pierre"): (
            "R\u00e9duire la ligne B du tramway : arr\u00eat \u00e0 l'H\u00f4pital Trousseau, \u00e9conomie de 150-200 M\u20ac r\u00e9investie dans 3 lignes suppl\u00e9mentaires",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-de-benoist-pierre-candidat-aux-municipales-a-tours/"
        ),
        ("transports", "velo-mobilites-douces", "pierre"): (
            "Moratoire imm\u00e9diat sur les am\u00e9nagements cyclables V\u00e9liVal pour \u00e9valuer l'existant",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-de-benoist-pierre-candidat-aux-municipales-a-tours/"
        ),
        ("transports", "stationnement", "pierre"): (
            "Demi-heure gratuite de stationnement le samedi en centre-ville pour soutenir le commerce local",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-de-benoist-pierre-candidat-aux-municipales-a-tours/"
        ),
        ("sport", "equipements-sportifs", "pierre"): (
            "Opposition au projet Arena ; investissement de 40-50 M\u20ac pour r\u00e9nover le Parc des Expositions",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-de-benoist-pierre-candidat-aux-municipales-a-tours/"
        ),
        ("economie", "commerce-local", "pierre"): (
            "Mise aux normes des Halles de Tours et relance du plan de r\u00e9novation des fa\u00e7ades du centre-ville",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-de-benoist-pierre-candidat-aux-municipales-a-tours/"
        ),
        ("logement", "logements-vacants", "pierre"): (
            "Valoriser les 8 000-10 000 logements vacants via le bail solidaire",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-de-benoist-pierre-candidat-aux-municipales-a-tours/"
        ),
        ("logement", "acces-logement", "pierre"): (
            "Utiliser l'EPFL pour pr\u00e9empter des terrains et construire des logements neufs",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/objectif-maire-la-grande-interview-de-benoist-pierre-candidat-aux-municipales-a-tours/"
        ),
        ("democratie", "transparence", "pierre"): (
            "Instaurer des r\u00e9f\u00e9rendums num\u00e9riques sur tous les grands projets municipaux",
            "Info Tours, 2025",
            "https://info-tours.fr/tours/2025/11/20/municipales-2026-a-tours-revision-de-la-2e-ligne-de-tramway-augmentation-du-nombre-de-policiers-municipaux-referendum-numerique-les-propositions-de-benoist-pierre/"
        ),
        ("urbanisme", "amenagement-urbain", "pierre"): (
            "R\u00e9nover la ville sans augmenter les imp\u00f4ts en r\u00e9duisant les d\u00e9penses sur les projets surdimensionn\u00e9s",
            "Info Tours, 2025",
            "https://info-tours.fr/tours/2025/11/20/municipales-2026-a-tours-revision-de-la-2e-ligne-de-tramway-augmentation-du-nombre-de-policiers-municipaux-referendum-numerique-les-propositions-de-benoist-pierre/"
        ),
        # --- Nikolic (RN) ---
        ("securite", "police-municipale", "nikolic"): (
            "Ratio d'un policier pour 600 habitants soit 225 agents (co\u00fbt 5,2 M\u20ac suppl\u00e9mentaires/an)",
            "37 degr\u00e9s mag, 2026",
            "https://www.37degres-mag.fr/politique/municipales-a-tours-surenchere-de-campagne-autour-de-la-police-municipale/"
        ),
        ("securite", "videoprotection", "nikolic"): (
            "Doublement des cam\u00e9ras et renforcement des patrouilles dans les secteurs commerciaux",
            "France Bleu Touraine, 2026",
            "https://www.francebleu.fr/infos/politique/tours-un-porte-parole-national-du-r-n-candidat-aux-municipales-2026-7247415"
        ),
        ("transports", "pietons-circulation", "nikolic"): (
            "R\u00e9f\u00e9rendum sur la r\u00e9ouverture du pont Wilson aux voitures et optimisation des feux de circulation",
            "France Bleu Touraine, 2026",
            "https://www.francebleu.fr/infos/elections/municipales-a-tours-le-candidat-rn-aleksandar-nikolic-rallie-trois-anciens-adjoints-de-serge-barbary-7669790"
        ),
        # --- Rouzier (PRG) ---
        ("democratie", "transparence", "rouzier"): (
            "Demande d'engagement du maire sortant \u00e0 ne pas s'allier avec LFI entre les deux tours",
            "Info Tours, 2026",
            "https://info-tours.fr/tours/2026/02/05/storiemunicipales2026-j-38-olivier-lebreton-va-mieux-le-rn-en-reunion-publique-a-tours-benoist-pierre-interpelle-sur-le-tram/"
        ),
        # --- Jouhannaud (LO) ---
        ("solidarite", "pouvoir-achat", "jouhannaud"): (
            "Revalorisation du SMIC \u00e0 2 000 euros nets et indexation des salaires sur la hausse des prix",
            "Lutte Ouvri\u00e8re, 2026",
            "https://www.lutte-ouvriere.org/portail/revue-de-presse/municipales-2026-tours-thomas-jouhannaud-candidat-lutte-ouvriere-veut-porter-voix-travailleurs-190974.html"
        ),
        ("economie", "emploi-insertion", "jouhannaud"): (
            "Municipalit\u00e9 au service des travailleurs : les yeux et les oreilles du monde du travail face aux patrons",
            "Lutte Ouvri\u00e8re, 2026",
            "https://www.lutte-ouvriere.org/portail/revue-de-presse/municipales-2026-tours-thomas-jouhannaud-candidat-lutte-ouvriere-veut-porter-voix-travailleurs-190974.html"
        ),
    }
)
