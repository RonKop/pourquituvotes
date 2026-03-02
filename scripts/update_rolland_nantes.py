#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Met à jour les propositions de Johanna Rolland (Nantes) depuis le programme officiel
https://lagaucheuniepournantes.fr/notre-projet/nos-engagements/
"""

import json
import os
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "nantes-2026.json")
CANDIDAT_ID = "rolland"

# Mapping : sous-thème -> liste de mesures (texte officiel du programme)
PROPOSITIONS = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Renforcer les effectifs de police municipale et de l'unité métropolitaine des transports en commun.",
        "Mettre à disposition de l'État des locaux pour la création d'un commissariat de police nationale de proximité.",
        "Renforcer la sécurité nocturne par un poste fixe de la Police Municipale en soirée, à Bouffay et au Hangar à Bananes.",
    ],
    "videoprotection": None,  # Pas de proposition
    "prevention-mediation": [
        "Augmenter le nombre de médiateurs et de médiatrices de quartier.",
        "Des parcours lumineux renforcés pour améliorer la sécurité dans l'espace public en soirée et la nuit.",
        "Mener un plan municipal de lutte contre les violences faites aux enfants.",
    ],
    "violences-femmes": [
        "Maintenir le soutien à Citad'elles, lieu d'accueil des femmes victimes de violences.",
        "Accompagner l'émergence d'un lieu dédié aux mineures victimes de violences.",
        "Doter tous les grands événements organisés sur l'espace public de protocoles de lutte contre les violences sexistes et sexuelles.",
        "Prendre en compte le genre dans chaque action de la Ville (budget, urbanisme, sport…).",
    ],

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Mettre en circulation les nouvelles lignes de tramway 6 et 7.",
        "Favoriser l'usage des P+R et développer des lignes de covoiturage.",
    ],
    "velo-mobilites-douces": [
        "Doubler le budget vélo et créer 150 kilomètres de nouvelles liaisons vélo sécurisées.",
    ],
    "pietons-circulation": [
        "Faire un nouveau plan piéton pour des rues plus accessibles à toutes et tous.",
    ],
    "stationnement": [
        "Expérimenter un tarif préférentiel de stationnement dans les parkings publics pour les travailleurs en horaires décalés.",
    ],
    "tarifs-gratuite": [
        "Élargir la gratuité des transports en commun à 15 000 personnes supplémentaires.",
        "Transports en commun gratuits sur présentation d'un billet de spectacle.",
    ],

    # ── LOGEMENT ──
    "logement-social": [
        "Produire 40 % de logements sociaux et 20 % de logements abordables pour les classes moyennes et populaires dans les programmes neufs.",
        "Soutenir le plan de lutte contre l'humidité porté par Nantes Métropole Habitat.",
    ],
    "logements-vacants": None,
    "encadrement-loyers": None,
    "acces-logement": [
        "Créer 700 nouvelles places en résidences universitaires.",
        "En lien avec l'État, doubler le nombre de places d'hébergement d'urgence pour les familles, avec pour ambition zéro enfant à la rue.",
    ],

    # ── ÉDUCATION ──
    "petite-enfance": [
        "Créer 700 places en crèche.",
        "Créer un service d'urgence de garde d'enfants pour les parents solo.",
    ],
    "ecoles-renovation": [
        "Continuer à faire de l'éducation la première priorité du budget de la Ville.",
        "Renforcer l'inclusion des enfants en situation de handicap.",
        "Lancer un grand plan Fraîcheur : rénovation des écoles, parcours ombragés en centre-ville, lieux de fraîcheur pour les personnes fragiles.",
    ],
    "cantines-fournitures": [
        "Distribuer un kit de rentrée scolaire à tous les élèves entrant en CP.",
        "Proposer un goûter gratuit et équilibré dans les écoles.",
        "Fixer l'objectif de 100 % de produits bio et locaux dans les cantines scolaires.",
    ],
    "periscolaire-loisirs": [
        "Faire la ville à hauteur d'enfants.",
    ],
    "jeunesse": [
        "Ouvrir un nouveau lieu en centre-ville dédié aux jeunes Nantaises et Nantais de 16 à 25 ans : espaces de travail, de rencontres, accès aux droits et aux loisirs.",
        "Créer un parcours de réussite pour les jeunes des quartiers populaires (orientation scolaire, recherche de stages…).",
    ],

    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Ouvrir un nouveau jardin dans chaque quartier.",
        "Débitumer deux fois plus d'espaces.",
        "Végétaliser les berges et les quais de Loire.",
        "Tripler l'opération 'Ma rue est un jardin'.",
        "Objectif : rendre à terme l'Erdre baignable.",
    ],
    "proprete-dechets": [
        "Accroître les moyens de la brigade verte pour la propreté.",
        "Mailler tous les quartiers d'un réseau de toilettes publiques.",
    ],
    "climat-adaptation": [
        "Construire sans artificialiser les sols pour préserver les espaces naturels et agricoles.",
        "Tenir l'engagement de Nantes ville neutre en carbone en 2050 en accélérant le plan Climat.",
        "Mettre en œuvre le plan 'Place à l'eau' : restaurer les rivières, créer des mares, favoriser l'infiltration des eaux de pluie, dépolluer les cours d'eau.",
        "Renforcer le service public de l'eau pour garantir l'accès à une eau potable de qualité.",
    ],
    "renovation-energetique": [
        "Massifier la rénovation thermique des bâtiments face au dérèglement climatique.",
        "Garantir l'accès aux financements de transition écologique pour réduire la facture énergétique des Nantais.",
        "Mobiliser la finance locale pour la rénovation des logements et le développement des énergies renouvelables.",
    ],
    "alimentation-durable": [
        "Étendre la sécurité sociale de l'alimentation à trois fois plus d'habitants.",
        "Ouvrir 6 nouvelles épiceries solidaires de produits bios en vrac.",
        "Créer un partenariat '1 école — 1 potager' avec les jardins partagés.",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Créer un équipement de santé dans chaque quartier populaire.",
        "Aider les professionnels de santé à s'installer dans tous les quartiers.",
    ],
    "prevention-sante": [
        "Faire de la santé mentale une priorité, en particulier celle des jeunes, en ouvrant une Maison de l'enfant.",
        "Déployer une équipe de rue spécialisée en santé mentale.",
        "Tripler le nombre de bénéficiaires de la mutuelle de santé communale.",
    ],
    "seniors": [
        "Faciliter la vie des seniors avec le projet Vill'âge : plus de 160 places en EHPAD et résidence autonomie, un accueil de jour et un restaurant.",
        "Soutenir l'aide aux courses quotidiennes et expérimenter une offre de commerces ambulants.",
        "Renforcer le service Proxibus dédié aux personnes à mobilité réduite avec 15 000 courses supplémentaires par an.",
    ],

    # ── DÉMOCRATIE ──
    "budget-participatif": [
        "Instaurer une Assemblée citoyenne mixte dans chaque quartier pour échanger, interpeller les élus et co-décider d'investissements de proximité.",
    ],
    "transparence": [
        "Adopter des économies de 3 M€ sur les dépenses de fonctionnement pour 2026 afin de maintenir la capacité d'investissement.",
    ],
    "vie-associative": [
        "Maintenir le soutien au monde associatif, premier acteur des solidarités.",
        "Accompagner son développement dans le cadre de la coopérative nantaise des solidarités.",
        "Faciliter la vie des associations par l'expérimentation d'une régie de matériels.",
    ],
    "services-publics": [
        "Créer une plateforme parents solo : numéro unique, service d'urgence de garde d'enfants, accompagnement vers des séjours de répit.",
    ],

    # ── ÉCONOMIE ──
    "commerce-local": [
        "Redonner au marché de Talensac une nouvelle jeunesse.",
        "Soutenir les commerces de proximité et créer un label 'Produit à Nantes'.",
        "Mettre en œuvre des opérations 'J'achète local'.",
        "Étudier l'encadrement des baux commerciaux avec les associations de commerçants.",
        "Créer une foncière commerciale pour faciliter les installations.",
    ],
    "emploi-insertion": [
        "Accompagner un développement économique responsable, créateur d'emplois : réemploi, numérique éthique, mode durable, éco-construction.",
        "Accompagner le projet de Maison des livreurs.",
        "Faciliter l'accès au foncier pour les structures sociales et solidaires.",
    ],
    "attractivite": [
        "Favoriser le maintien des activités industrielles et artisanales.",
        "Renforcer les partenariats en matière d'économie, d'alimentation, d'emploi et de mobilités avec les territoires voisins.",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Un nouveau Conservatoire à Nantes Nord.",
        "La Cité des Imaginaires.",
        "La modernisation du Lieu Unique.",
        "Les Nefs comme grand forum pour la culture, la citoyenneté et les pratiques libres.",
        "Accompagner le projet Kejadenn, espace dédié aux langues, entreprises et culture bretonne.",
    ],
    "evenements-creation": [
        "Continuer à soutenir la création, la diffusion et l'accès du plus grand nombre à la pratique artistique.",
        "La Maison de la Poésie.",
        "Le Port des arts nomades.",
    ],

    # ── SPORT ──
    "equipements-sportifs": [
        "Rénover les équipements sportifs de proximité dans plusieurs quartiers.",
        "Créer une salle de boxe à Nantes Nord.",
        "Ouvrir un nouveau lieu pour les pratiques sportives libres sur l'Île de Nantes.",
    ],
    "sport-pour-tous": [
        "Étendre les horaires des piscines en soirée.",
        "Soutenir l'ouverture de deux nouvelles maisons sport-santé.",
    ],

    # ── URBANISME ──
    "amenagement-urbain": [
        "Garantir l'accessibilité universelle de tout aménagement.",
    ],
    "accessibilite": [
        "Garantir l'accessibilité universelle de tout aménagement et faire la ville à hauteur d'enfants.",
    ],
    "quartiers-prioritaires": [
        "Plan de 10 mesures spécifiques pour les quartiers populaires de Nantes.",
    ],

    # ── SOLIDARITÉ ──
    "aide-sociale": [
        "Doubler le nombre de places d'hébergement d'urgence pour les familles, avec pour ambition zéro enfant à la rue.",
        "Séjours de répit pour les familles monoparentales.",
    ],
    "egalite-discriminations": [
        "Renforcer le soutien aux personnes victimes de racisme et de discrimination : dispositifs d'accueil de la parole, soutien aux associations, formation des agents.",
        "Prendre en compte le genre dans chaque action de la Ville.",
    ],
    "pouvoir-achat": [
        "Distribuer un kit de rentrée scolaire à tous les élèves entrant en CP.",
        "Proposer un goûter gratuit et équilibré dans les écoles.",
        "Élargir la gratuité des transports en commun à 15 000 personnes supplémentaires.",
        "Garantir l'accès aux financements de transition écologique pour réduire la facture énergétique.",
    ],
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Mettre à jour l'URL du programme
    for c in data["candidats"]:
        if c["id"] == CANDIDAT_ID:
            c["programmeUrl"] = "https://lagaucheuniepournantes.fr/notre-projet/nos-engagements/"
            c["programmeComplet"] = True
            break

    # Compteurs
    updated = 0
    added = 0
    total_mesures = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id not in PROPOSITIONS:
                continue

            new_mesures = PROPOSITIONS[st_id]

            if "propositions" not in st:
                st["propositions"] = {}

            if new_mesures is None:
                # Pas de proposition pour ce sous-thème
                if CANDIDAT_ID in st["propositions"] and st["propositions"][CANDIDAT_ID]:
                    pass  # Ne pas supprimer les existantes
                continue

            had_before = (
                CANDIDAT_ID in st["propositions"]
                and st["propositions"][CANDIDAT_ID]
                and st["propositions"][CANDIDAT_ID].get("mesures")
            )

            st["propositions"][CANDIDAT_ID] = {
                "mesures": new_mesures
            }

            total_mesures += len(new_mesures)
            if had_before:
                updated += 1
            else:
                added += 1

    # Écrire
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"{'='*55}")
    print(f"  MISE À JOUR — Johanna Rolland (Nantes)")
    print(f"{'='*55}")
    print(f"  Sous-thèmes mis à jour  : {updated}")
    print(f"  Sous-thèmes ajoutés     : {added}")
    print(f"  Total mesures           : {total_mesures}")
    print(f"  JSON écrit : {JSON_PATH}")


if __name__ == "__main__":
    main()
