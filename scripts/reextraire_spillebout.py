#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction complète de Violette Spillebout (Lille)

Source   : Programme officiel violette2026.fr (14 pages thématiques)
URL      : https://violette2026.fr
Date     : 2026-03-09
Mesures source : ~200 mesures identifiées sur les 14 pages
Mesures extraites : voir MESURES ci-dessous

Utilisation :
  1. Exécuter : python scripts/reextraire_spillebout.py
  2. Valider : python scripts/valider_donnees.py
  3. Auditer : python scripts/auditer_completude.py --candidat spillebout --ville lille
"""

import io
import json
import os
import sys

# Force UTF-8 pour Windows (cp1252 fix)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# === CONFIGURATION ===
CANDIDAT_ID = "spillebout"
VILLE_ID = "lille-2026"
SOURCE = "Programme officiel violette2026.fr"
SOURCE_URL = "https://violette2026.fr"
PROGRAMME_URL = "https://violette2026.fr"

JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", f"{VILLE_ID}.json")

# === MESURES ===
# Clé = ID du sous-thème
# Valeur = liste de mesures concrètes (verbe à l'infinitif) ou None
MESURES = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Recruter 100 policiers municipaux supplémentaires pour atteindre plus de 250 agents.",
        "Armer progressivement la police municipale (létal et non-létal) avec formation renforcée.",
        "Créer des unités mobiles de police municipale intervenant dans tous les quartiers.",
        "Stationner des policiers municipaux en permanence dans chaque mairie de quartier.",
        "Créer une direction de la Sécurité et de la Tranquillité publique coordonnant police, médiateurs, stationnement et vie nocturne.",
    ],
    "videoprotection": [
        "Installer 2 000 caméras de vidéoprotection sur Lille-Lomme-Hellemmes d'ici 2035, en priorité dans les zones sensibles.",
    ],
    "prevention-mediation": [
        "Soutenir les associations de prévention (médiation sociale, sport, culture, addictions).",
        "Déployer un plan de sécurité routière avec campagnes dans les écoles, apaisement de la circulation et radars municipaux.",
        "Lancer des campagnes de sensibilisation sur les dangers du protoxyde d'azote et des drogues.",
        "Permettre aux habitants de signaler les problèmes via l'application SignaLille en moins d'une minute, avec accès téléphonique 24h/24.",
        "Nommer des médiateurs de quartier pour gérer les conflits de voisinage et de vie nocturne.",
        "Créer un bouton d'alerte anti-agression pour les commerçants relié à la police municipale.",
        "Renforcer le Conseil lillois de prévention de la délinquance et de la radicalisation.",
        "Créer un Conseil lillois des religions et de la laïcité.",
        "Lancer une fonctionnalité « SOS Animal en danger » dans l'application SignaLille.",
    ],
    "violences-femmes": [
        "Renforcer la Maison des Femmes et les dispositifs d'aide aux victimes de violences conjugales.",
        "Labelliser Lille « Safe City » protégeant les droits LGBT+ et luttant contre les discriminations.",
        "Protéger les droits de l'enfant et maintenir le label UNICEF « Ville amie des enfants ».",
    ],

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Améliorer la fiabilité et la fréquence du métro en attendant les nouvelles lignes de tramway.",
        "Créer des mini-navettes électriques reliant les parkings relais au centre-ville.",
    ],
    "velo-mobilites-douces": [
        "Déployer des « Véloroutes Express Végétalisées » sécurisées et arborées sur les grands boulevards.",
        "Installer des stationnements vélos sécurisés dans les parkings existants.",
        "Agrandir les box vélos avec surveillance caméra et capacité pour vélos-cargos.",
        "Déployer 100 vélos-taxis avec cinq stations dans les zones piétonnes.",
        "Ajouter 7 nouvelles passerelles piétonnes et cyclables reliant les quartiers.",
    ],
    "pietons-circulation": [
        "Réviser le plan de circulation pour supprimer les goulots d'étranglement et réduire la pollution.",
        "Étendre les zones piétonnes et créer une promenade continue de 5 km de Saint-Sauveur au Port de Lille.",
        "Élargir les trottoirs avec des zones de circulation accessibles aux personnes à mobilité réduite.",
        "Promouvoir la livraison de colis par véhicules électriques et vélos-cargos.",
    ],
    "stationnement": [
        "Réduire le tarif du stationnement résidentiel à 10 €/mois avec droits égaux dans toutes les zones.",
        "Remplacer le contrôle automatisé LAPI par des agents de terrain privilégiant la prévention.",
        "Construire 5 parkings-silos multi-niveaux en périphérie du centre-ville avec connexion transport.",
        "Proposer un tarif préférentiel de 15 €/mois pour les entreprises et associations lilloises.",
        "Créer des espaces « Shop & Go » offrant 30 minutes gratuites pour les courses rapides.",
        "Instaurer la gratuité du stationnement de 12h à 14h dans les secteurs commerçants.",
    ],
    "tarifs-gratuite": [
        "Rendre les transports en commun gratuits pour les moins de 26 ans, les retraités et les personnes en situation de handicap.",
        "Instaurer la gratuité des transports le week-end pour tous.",
    ],

    # ── LOGEMENT ──
    "logement-social": [
        "Rétablir les postes de gardiens d'immeubles dans tous les ensembles de logements sociaux.",
        "Réformer l'attribution des logements sociaux en priorité pour les travailleurs modestes, les travailleurs en horaires décalés et les familles avec enfants en situation de handicap.",
    ],
    "logements-vacants": [
        "Réhabiliter 12 000 logements vacants via un plan d'urgence pour les remettre sur le marché.",
        "Transformer 45 000 m² de bureaux vacants en logements.",
    ],
    "encadrement-loyers": None,
    "acces-logement": [
        "Permettre la surélévation des bâtiments existants pour créer des logements tout en finançant la rénovation thermique.",
        "Simplifier les démarches administratives des promoteurs en réduisant les normes locales et les délais d'instruction des permis.",
        "Créer des logements adaptables conçus pour le handicap et le vieillissement.",
        "Construire de nouvelles résidences étudiantes intergénérationnelles favorisant la solidarité.",
        "Soutenir la rénovation des résidences CROUS et faciliter les projets de résidences étudiantes privées.",
    ],

    # ── ÉDUCATION ──
    "petite-enfance": [
        "Créer 300 places de crèche supplémentaires dans les quartiers sous-dotés, dont certaines adaptées aux horaires atypiques.",
        "Adapter les crèches à l'accueil des enfants en situation de handicap (équipements, personnel formé, suivi médico-social).",
        "Soutenir les réseaux d'assistantes maternelles et leur formation continue.",
        "Accompagner les parents pendant les 1 000 premiers jours via la coordination des professionnels de la petite enfance.",
    ],
    "ecoles-renovation": [
        "Vérifier systématiquement les antécédents des professionnels au contact des enfants et améliorer la sécurité aux abords des écoles.",
        "Déployer le programme « Papillons » avec des boîtes aux lettres dans chaque école pour signaler les violences.",
    ],
    "cantines-fournitures": [
        "Rendre la cantine scolaire gratuite pour tous les enfants des écoles publiques.",
        "Atteindre 75 % minimum de produits locaux et bio d'ici 2032, avec une option végétarienne quotidienne et une centrale de transformation de légumes frais.",
    ],
    "periscolaire-loisirs": [
        "Lancer « Lille numérique pour tous » : formation au numérique et esprit critique face aux réseaux sociaux dans les écoles.",
        "Mettre en place un programme de communication non-violente et un plan anti-harcèlement concret dans les écoles.",
    ],
    "jeunesse": [
        "Créer le programme « Lille Tremplin » avec des coachs pour raccrocher les 14-18 ans en décrochage scolaire.",
        "Lancer « 1 000 mentors pour 1 000 jeunes » appariant bénévoles et jeunes pour un accompagnement scolaire et professionnel.",
        "Ouvrir un « QG de la réussite » dans chaque mairie de quartier pour l'orientation, les stages, le logement étudiant et les démarches.",
        "Créer un passeport municipal du jeune citoyen avec instruction civique, secourisme et compétences numériques dès le primaire.",
        "Lancer « Finance ton permis » : financement du permis de conduire en échange d'un service civique.",
        "Mettre en place le plan « 1 étudiant / 1 stage » avec les institutions publiques et une plateforme d'offres en ligne.",
        "Renforcer les maisons de quartier pour l'engagement civique des collégiens et lycéens.",
        "Sécuriser les sorties nocturnes via le programme « Demandez Angela » dans les commerces partenaires.",
        "Développer des emplois municipaux et jobs étudiants adaptés aux horaires universitaires.",
    ],

    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Créer 50 « places de village » végétalisées avec jeux d'eau pour lutter contre les îlots de chaleur.",
        "Développer des bioparcs et forêts urbaines et planter un arbre par naissance chaque année.",
        "Créer un jardin de rue dans chaque quartier et des jardins familiaux dans les parcs.",
        "Augmenter les toitures et façades végétalisées et étendre les « permis de végétaliser ».",
        "Restaurer progressivement l'eau sur l'avenue du Peuple Belge (miroir d'eau d'ici 2032, restitution complète d'ici 2040).",
        "Créer une boucle verte continue reliant tous les quartiers avec des cheminements accessibles pour les mobilités douces.",
    ],
    "proprete-dechets": [
        "Créer une brigade de propreté pour réprimer les incivilités, coordonner le nettoyage et la dératisation.",
        "Tripler le nombre de poubelles de rue avec tri sélectif.",
        "Installer des micro-déchetteries dans chaque quartier offrant réparation, récupération et revente.",
        "Augmenter la collecte professionnelle des déchets des artisans et commerçants, objectif zéro plastique.",
        "Promouvoir le zéro déchet : services municipaux exemplaires, cantines sans gaspillage, 3 000 familles engagées.",
        "Installer 30 toilettes publiques dans toute la ville.",
        "Installer au moins une fontaine d'eau potable dans chaque parc et place.",
        "Développer des caniparcs dans les quartiers.",
    ],
    "climat-adaptation": [
        "Accompagner les familles et entreprises dans le remplacement des chauffages polluants.",
        "Réduire la consommation d'énergies fossiles et développer la production d'énergie renouvelable sur la métropole.",
    ],
    "renovation-energetique": [
        "Améliorer l'isolation, la ventilation et la gestion énergétique des bâtiments municipaux.",
        "Intégrer les énergies renouvelables (panneaux photovoltaïques, récupération d'eau de pluie) dans tous les nouveaux projets municipaux.",
        "Utiliser la maintenance prédictive des équipements pour réduire durablement les dépenses énergétiques.",
        "Encourager la rénovation énergétique des bâtiments publics et privés.",
    ],
    "alimentation-durable": [
        "Généraliser la récupération d'eau de pluie pour les jardins et les sanitaires publics et privés.",
        "Rendre l'eau adoucie accessible dans tous les logements.",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Créer un centre municipal de santé dans chaque quartier (consultations généralistes, psychologiques, soins infirmiers, protection maternelle et infantile).",
    ],
    "prevention-sante": [
        "Développer le soutien en santé mentale pour les jeunes et adultes en coordination avec le CHRU de Lille et les établissements scolaires.",
        "Mettre en place des programmes « sport sur ordonnance » permettant aux médecins d'orienter les patients vers des éducateurs formés.",
        "Ouvrir un lieu de halte soins addictions en partenariat avec les associations.",
    ],
    "seniors": [
        "Ouvrir deux nouveaux EHPAD pour personnes âgées dépendantes.",
        "Développer 6 000 logements intergénérationnels et adaptés aux seniors dans les quartiers d'ici 2040.",
        "Ouvrir une résidence intergénérationnelle pour seniors dans l'ancien lycée Michel Servet (Vauban) avec un système de visites à domicile par des jeunes en service civique.",
    ],

    # ── DÉMOCRATIE ──
    "budget-participatif": [
        "Doubler le budget participatif pour les projets proposés par les citoyens.",
        "Intégrer des clauses de consultation citoyenne dans les marchés publics et projets urbains.",
    ],
    "transparence": [
        "Publier des audits financiers annuels indépendants lors des votes budgétaires.",
        "Publier en temps réel des indicateurs municipaux de qualité (sécurité, propreté, mobilité, culture, solidarité, écoles).",
        "Confier des responsabilités réelles aux élus d'opposition pour le contrôle de l'usage des fonds publics et l'éthique municipale.",
        "Ne pas augmenter les impôts pendant tout le mandat 2026-2032.",
        "Créer un « comité anti-gaspi » composé d'élus et de citoyens pour identifier les dépenses inutiles.",
        "Publier la justification des frais de représentation du maire et des élus.",
    ],
    "vie-associative": [
        "Généraliser les conventions pluriannuelles d'objectifs pour le financement des associations.",
        "Co-signer une charte d'engagements avec les associations exigeant exemplarité salariale et responsabilité environnementale et sociale.",
    ],
    "services-publics": [
        "Créer des guichets multi-services dans chaque mairie de quartier (accès aux droits, démarches administratives, ateliers numériques, point police municipale).",
        "Généraliser la dématérialisation des actes et services administratifs, dont la carte Lille & Moi.",
        "Garantir une réponse en 72 heures aux demandes citoyennes en ligne et renforcer l'application SignaLille.",
        "Élargir les horaires d'ouverture des équipements municipaux pour mieux répondre aux besoins des habitants et associations.",
        "Instaurer un droit de pétition locale abaissé (50 signatures pour un quartier, 2 000 pour la ville) déclenchant un débat municipal.",
        "Organiser des réunions publiques mensuelles par quartier animées par les élus.",
        "Permettre à 10 citoyens d'interpeller le maire lors des séances du conseil municipal.",
        "Mettre en place des conventions citoyennes tirées au sort pour les grandes décisions urbaines.",
        "Réformer les conseils de quartier avec des membres élisant leur propre président.",
        "Créer un comité citoyen de vigilance pour l'accessibilité et la qualité de vie.",
    ],

    # ── ÉCONOMIE ──
    "commerce-local": [
        "Créer un fonds municipal d'immobilier commercial pour acquérir des locaux vacants et proposer des loyers adaptés aux commerçants.",
        "Offrir des aides au loyer aux commerces en difficulté ou impactés par des travaux de voirie.",
        "Soutenir les marchés de plein air et les halles couvertes avec des initiatives de fréquentation et de sécurité.",
        "Installer un marché de Noël agrandi dans les zones piétonnes.",
        "Désigner des managers de secteurs commerciaux pour animer la vie commerçante dans chaque quartier.",
        "Simplifier les démarches d'ouverture de commerces et de terrasses avec des délais réduits.",
        "Soutenir le développement de terrasses saisonnières sur des places de stationnement tout en respectant l'accès piéton.",
        "Créer un Conseil du Commerce et de la Vie Nocturne associant commerçants, marchands et centres commerciaux.",
        "Relancer le projet « Avenue des Modes » avec incubateur textile recyclé, boutiques de seconde main et vestiaire solidaire.",
    ],
    "emploi-insertion": [
        "Créer le « Lille Entreprendre Club » fédérant entreprises, acteurs de l'éducation, de l'emploi et associations.",
        "Ouvrir un guichet d'aide à l'entrepreneuriat dans chaque mairie de quartier.",
        "Ouvrir un incubateur-accélérateur d'entrepreneuriat social.",
        "Transformer la Fondation de Lille en « Fondation lilloise pour l'innovation sociale et environnementale ».",
    ],
    "attractivite": [
        "Revitaliser EuraTechnologies en élargissant les secteurs qualifiants au-delà du numérique pour remplir 35 000 m² de bureaux vacants.",
        "Anticiper la reconversion de Lillenium en « Cité Créative et Logistique » (logistique urbaine durable, ateliers artisanaux, espaces culturels).",
        "Sécuriser l'implantation du siège de l'Autorité européenne des douanes à Lille.",
        "Créer une plateforme métropolitaine européenne d'innovation fédérant startups, entreprises, centres de recherche et universités.",
        "Installer une résidence de chercheurs à EuraTechnologies pour attirer les talents internationaux.",
        "Renforcer la présence institutionnelle à Bruxelles pour capter les financements européens.",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Installer le Laboratoire Européen de l'Image au Tri Postal (éducation aux médias, création artistique, IA).",
        "Relancer la candidature UNESCO de la Citadelle de Vauban au patrimoine mondial.",
        "Protéger et rénover le patrimoine lillois existant, notamment les sites religieux et labellisés Art et Histoire.",
        "Développer les cultures urbaines au-delà de Flow avec la Maison du Hip Hop dans le quartier de Moulins.",
        "Créer une Académie des métiers du textile et de la mode alliant artisanat traditionnel et innovations.",
    ],
    "evenements-creation": [
        "Créer la Grande Parade Créative annuelle préparée toute l'année par les habitants avec les artistes et institutions locales.",
        "Organiser la Nuit des Arts chaque année : parcours artistique accessible avec studios, musées et galeries ouverts au public.",
        "Accueillir une grande exposition internationale tous les deux ans au Palais des Beaux-Arts.",
        "Organiser un Festival International de la BD et du Manga à Lille.",
        "Créer des parcours artistiques thématiques découvrant les œuvres dans l'espace public.",
        "Établir un Conseil lillois de la Culture évaluant la politique culturelle et instaurant des subventions pluriannuelles.",
    ],

    # ── SPORT ──
    "equipements-sportifs": [
        "Ouvrir les gymnases et installations sportives scolaires le soir, le week-end et pendant les vacances.",
        "Installer des équipements sportifs gratuits dans chaque quartier (parcours fitness, paniers de basket, parcours seniors, BMX, roller).",
        "Mettre à disposition une flotte partagée de 10 minibus électriques pour les clubs sportifs et associations de quartier.",
    ],
    "sport-pour-tous": [
        "Créer un Pass Sport municipal doublant l'aide nationale pour l'inscription en club des enfants et jeunes.",
        "Relancer les clubs sportifs de haut niveau en collaboration avec la métropole.",
        "Soutenir financièrement les postes d'éducateurs sportifs dans les associations.",
        "Labelliser des clubs « Clubs Inclusifs » pour accueillir les personnes en situation de handicap.",
        "Mettre en place les programmes « Tous nageurs » et « Tous cyclistes » pour les élèves du primaire.",
        "Soutenir les champions locaux par la mobilisation du parrainage local et l'aide à l'emploi.",
    ],

    # ── URBANISME ──
    "amenagement-urbain": [
        "Revitaliser trois quartiers (Fives, Moulins, Wazemmes) : réhabilitation de bâtiments, construction de logements neufs, végétalisation et commerces.",
        "Construire une nouvelle gare routière pour les autocars de tourisme.",
        "Installer des bornes de recharge pour véhicules électriques dans toutes les nouvelles constructions et rénovations de voirie.",
        "Créer une zone de covoiturage à proximité du centre-ville.",
    ],
    "accessibilite": [
        "Garantir une ville 100 % inclusive : expertise d'usage dans tous les comités de projet, communication FALC, événements entièrement accessibles.",
    ],
    "quartiers-prioritaires": [
        "Renforcer la présence de services publics et l'animation commerciale dans les quartiers prioritaires via les mairies de quartier.",
    ],

    # ── SOLIDARITÉ ──
    "aide-sociale": [
        "Créer 100 places d'hébergement d'urgence pour les femmes en danger avec accompagnement psychologique et social.",
        "Soutenir les sans-abri vers l'insertion via le projet « Carrefour des solidarités » (hébergement, douches, buanderie, espaces hygiène-santé).",
        "Créer 100 places d'hébergement d'urgence pour les demandeurs d'asile et réfugiés.",
        "Mettre en place un programme d'insertion des familles roms avec des « sas d'insertion » temporaires.",
        "Développer des services sociaux étudiants dans chaque « QG de la réussite » (accès santé, épicerie solidaire, vestiaire).",
    ],
    "egalite-discriminations": [
        "Déployer un plan ambitieux de lutte contre les discriminations, le racisme et l'antisémitisme avec les écoles et associations.",
    ],
    "pouvoir-achat": [
        "Rationaliser la flotte de véhicules municipaux en privilégiant le transport collectif, le vélo et le passage au tout-électrique.",
        "Optimiser les achats municipaux avec un objectif zéro plastique d'ici 2040.",
        "Rendre les événements municipaux éco-responsables avec engagement zéro déchet.",
        "Monter les projets en cofinancement (MEL, Département, Région, État, fonds européens et privés) pour limiter la pression sur les ressources municipales.",
    ],
}


def main():
    # Charger le JSON
    if not os.path.exists(JSON_PATH):
        print(f"ERREUR : fichier introuvable → {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    # Trouver le candidat et mettre à jour les métadonnées
    candidat_found = False
    for c in data["candidats"]:
        if c["id"] == CANDIDAT_ID:
            c["programmeUrl"] = PROGRAMME_URL
            c["programmeComplet"] = True
            candidat_found = True
            break

    if not candidat_found:
        print(f"ERREUR : candidat '{CANDIDAT_ID}' introuvable dans {VILLE_ID}")
        sys.exit(1)

    # Compteurs
    total_mesures = 0
    st_remplis = 0
    st_vides = 0
    st_inconnus = []

    # Parcourir toutes les catégories et sous-thèmes
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]

            if st_id in MESURES:
                mesures = MESURES[st_id]
                if mesures is None:
                    # Explicitement mis à None → pas de mesures
                    st["propositions"][CANDIDAT_ID] = None
                    st_vides += 1
                else:
                    st["propositions"][CANDIDAT_ID] = {
                        "source": SOURCE,
                        "sourceUrl": SOURCE_URL,
                        "mesures": mesures,
                    }
                    total_mesures += len(mesures)
                    st_remplis += 1
            else:
                # Sous-thème spécifique à la ville, non dans notre mapping
                if CANDIDAT_ID not in st["propositions"] or st["propositions"].get(CANDIDAT_ID) is None:
                    st["propositions"][CANDIDAT_ID] = None
                    st_vides += 1
                    st_inconnus.append(f"{cat['id']}/{st_id}")

    # Safety check : on doit avoir au moins 50 % des anciennes mesures (54)
    if total_mesures < 27:
        print(f"SAFETY CHECK FAIL : seulement {total_mesures} mesures (< 27 = 50% de 54 anciennes)")
        print("SKIP — vérifier le mapping MESURES")
        sys.exit(1)

    # Sauvegarder
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rapport
    print(f"{'=' * 60}")
    print(f"Ré-extraction terminée : {CANDIDAT_ID} ({VILLE_ID})")
    print(f"{'=' * 60}")
    print(f"  Total mesures        : {total_mesures}")
    print(f"  Sous-thèmes remplis  : {st_remplis}")
    print(f"  Sous-thèmes vides    : {st_vides}")
    print(f"  programmeUrl         : {PROGRAMME_URL}")
    print(f"  programmeComplet     : True")
    if st_inconnus:
        print(f"  ST spécifiques ville (non mappés) : {', '.join(st_inconnus)}")
    print(f"\n→ Lancer maintenant : python scripts/valider_donnees.py")


if __name__ == "__main__":
    main()
