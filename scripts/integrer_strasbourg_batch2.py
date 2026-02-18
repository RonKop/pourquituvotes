#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'intégration des programmes de Catherine Trautmann et Jeanne Barseghian
pour les municipales 2026 à Strasbourg
"""

import json
import sys
from pathlib import Path

# Configuration UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Chemins
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "elections"
JSON_PATH = DATA_DIR / "strasbourg-2026.json"

# Propositions Catherine Trautmann (PS)
PROPOSITIONS_TRAUTMANN = {
    "police-municipale": {
        "texte": "Renforcement de la présence de la police municipale avec patrouilles régulières et visibles dans tous les quartiers, et création de postes de police municipale de proximité",
        "source": "Pokaa et Rue89 Strasbourg, décembre 2025 - février 2026",
        "sourceUrl": "https://pokaa.fr/2025/12/12/municipales-2026-a-strasbourg-catherine-trautmann-veut-simposer-sur-la-securite/"
    },
    "videoprotection": {
        "texte": "Installation de pièges photographiques dans les zones de dépôts sauvages et d'incivilités",
        "source": "Pokaa et Rue89 Strasbourg, décembre 2025",
        "sourceUrl": "https://www.rue89strasbourg.com/securite-catherine-trautmann-strasbourg-2026-368996"
    },
    "transports-en-commun": {
        "texte": "Réalisation du tramway Nord vers Schiltigheim et Bischheim via boulevard Wilson, et développement du réseau de tramway vers le sud de Neuhof",
        "source": "Pokaa, février 2026",
        "sourceUrl": "https://pokaa.fr/2026/02/10/municipales-2026-en-voiture-ou-en-tram-trautmann-veut-un-strasbourg-qui-bouge/"
    },
    "stationnement": {
        "texte": "Réduction des tarifs de stationnement résident dès 2026, et 30 minutes de stationnement gratuit dans toutes les zones payantes",
        "source": "Pokaa et Rue89 Strasbourg, janvier-février 2026",
        "sourceUrl": "https://pokaa.fr/2026/01/14/municipales-2026-a-strasbourg-catherine-trautmann-ps-mise-sur-le-pouvoir-de-vivre/"
    },
    "tarifs-gratuite": {
        "texte": "Transports en commun gratuits pour les plus de 65 ans",
        "source": "Pokaa et Rue89 Strasbourg, janvier 2026",
        "sourceUrl": "https://www.rue89strasbourg.com/catherine-trautmann-droits-essentiels-municipales-strasbourg-377114"
    },
    "cantines-fournitures": {
        "texte": "Fournitures scolaires gratuites pour tous les enfants à chaque rentrée scolaire",
        "source": "Pokaa, janvier 2026",
        "sourceUrl": "https://pokaa.fr/2026/01/14/municipales-2026-a-strasbourg-catherine-trautmann-ps-mise-sur-le-pouvoir-de-vivre/"
    },
    "pouvoir-achat": {
        "texte": "Programme 'Pouvoir de Vivre' : 15 m³ d'eau gratuits pour tous les foyers strasbourgeois",
        "source": "Pokaa et Rue89 Strasbourg, janvier 2026",
        "sourceUrl": "https://www.rue89strasbourg.com/catherine-trautmann-droits-essentiels-municipales-strasbourg-377114"
    }
}

# Propositions Jeanne Barseghian (EELV, maire sortante)
PROPOSITIONS_BARSEGHIAN = {
    "stationnement": {
        "texte": "Tarification solidaire et progressive du stationnement résident : de 5€ à 40€ par mois selon les revenus des ménages",
        "source": "Pokaa et Rue89 Strasbourg, janvier 2026",
        "sourceUrl": "https://pokaa.fr/2026/01/07/municipales-2026-jeanne-barseghian-devoile-12-mesures-pour-etre-reelue-maire/"
    },
    "encadrement-loyers": {
        "texte": "Encadrement des loyers pour les logements et les commerces afin de garantir leur accessibilité et préserver la diversité",
        "source": "Pokaa et France 3 Grand Est, janvier 2026",
        "sourceUrl": "https://france3-regions.franceinfo.fr/grand-est/bas-rhin/strasbourg-0/l-encadrement-des-loyers-au-programme-de-la-maire-sortante-de-strasbourg-argument-electoral-ou-mesure-efficace-3278660.html"
    },
    "cantines-fournitures": {
        "texte": "Objectif de 75% de bio dans les cantines scolaires (contre 53% actuellement), et développement de cantines de quartier accessibles à tous pour manger bien et pas cher",
        "source": "Pokaa et Rue89 Strasbourg, janvier-février 2026",
        "sourceUrl": "https://pokaa.fr/2026/02/02/municipales-2026-jeanne-barseghian-veut-une-alimentation-saine-pour-tout-strasbourg/"
    },
    "espaces-verts": {
        "texte": "Accélération de la végétalisation : création de nouveaux parcs et rues plus vertes dans tous les quartiers",
        "source": "Pokaa et Rue89 Strasbourg, janvier 2026",
        "sourceUrl": "https://www.rue89strasbourg.com/jeanne-barseghian-premieres-mesures-strasbourg-376685"
    },
    "alimentation-durable": {
        "texte": "Développement de l'alimentation saine et locale pour tous les Strasbourgeois via des cantines de quartier et soutien renforcé aux épiceries solidaires",
        "source": "Pokaa, février 2026",
        "sourceUrl": "https://pokaa.fr/2026/02/02/municipales-2026-jeanne-barseghian-veut-une-alimentation-saine-pour-tout-strasbourg/"
    },
    "budget-participatif": {
        "texte": "Nouvelles assemblées de quartier avec davantage de moyens pour les élu(e)s de quartier, droit d'interpellation citoyen, et tirage au sort pour diversifier la participation",
        "source": "Pokaa, janvier-février 2026",
        "sourceUrl": "https://pokaa.fr/2026/02/16/municipales-2026-jeanne-barseghian-veut-accelerer-la-democratie-locale-a-strasbourg/"
    },
    "sport-pour-tous": {
        "texte": "Sport encadré en accès libre dans les parcs avec des coachs sportifs municipaux",
        "source": "Pokaa et Rue89 Strasbourg, janvier 2026",
        "sourceUrl": "https://www.rue89strasbourg.com/jeanne-barseghian-premieres-mesures-strasbourg-376685"
    },
    "aide-sociale": {
        "texte": "Garantir le droit aux vacances pour toutes et tous avec des séjours accessibles pour les familles modestes",
        "source": "Pokaa et Rue89 Strasbourg, janvier 2026",
        "sourceUrl": "https://www.rue89strasbourg.com/jeanne-barseghian-premieres-mesures-strasbourg-376685"
    },
    "prevention-sante": {
        "texte": "Campagne municipale gratuite de dépistage de l'endométriose pour les personnes de 14 ans et plus, en partenariat avec le CMCO (tests salivaires pour orientation rapide vers les soins)",
        "source": "Pokaa et Rue89 Strasbourg, janvier 2026",
        "sourceUrl": "https://pokaa.fr/2026/01/07/municipales-2026-jeanne-barseghian-devoile-12-mesures-pour-etre-reelue-maire/"
    },
    "seniors": {
        "texte": "Création d'un conseil des seniors sur le modèle du conseil des jeunes, pour impliquer les seniors dans les décisions qui les concernent",
        "source": "Pokaa et Rue89 Strasbourg, janvier 2026",
        "sourceUrl": "https://www.rue89strasbourg.com/jeanne-barseghian-premieres-mesures-strasbourg-376685"
    },
    "velo-mobilites-douces": {
        "texte": "Stationnements vélo sécurisés dans tous les quartiers pour lutter contre le vol de vélos",
        "source": "Pokaa et Rue89 Strasbourg, janvier 2026",
        "sourceUrl": "https://www.rue89strasbourg.com/jeanne-barseghian-premieres-mesures-strasbourg-376685"
    }
}

# Sous-thème spécifique créé pour cette mesure originale
BARSEGHIAN_DISPENSAIRE_ANIMAUX = {
    "texte": "Dispensaire municipal pour animaux avec soins vétérinaires accessibles à tous les Strasbourgeois quel que soit leur revenu, pour lutter contre l'abandon et la maltraitance",
    "source": "Pokaa et Rue89 Strasbourg, janvier 2026",
    "sourceUrl": "https://pokaa.fr/2026/01/07/municipales-2026-jeanne-barseghian-devoile-12-mesures-pour-etre-reelue-maire/"
}


def main():
    print("🔄 Intégration des programmes Trautmann et Barseghian pour Strasbourg 2026...")

    # Lecture du JSON
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Compteurs
    compteur_trautmann = 0
    compteur_barseghian = 0
    sous_theme_ajoute = False

    # Intégration des propositions dans les catégories existantes
    for categorie in data['categories']:
        for sous_theme in categorie['sousThemes']:
            sous_theme_id = sous_theme['id']

            # Trautmann
            if sous_theme_id in PROPOSITIONS_TRAUTMANN:
                sous_theme['propositions']['trautmann'] = PROPOSITIONS_TRAUTMANN[sous_theme_id]
                compteur_trautmann += 1
                print(f"✅ Trautmann - {categorie['nom']} > {sous_theme['nom']}")

            # Barseghian
            if sous_theme_id in PROPOSITIONS_BARSEGHIAN:
                sous_theme['propositions']['barseghian'] = PROPOSITIONS_BARSEGHIAN[sous_theme_id]
                compteur_barseghian += 1
                print(f"✅ Barseghian - {categorie['nom']} > {sous_theme['nom']}")

    # Ajout du sous-thème spécifique "Animaux de compagnie" pour le dispensaire vétérinaire de Barseghian
    # On l'ajoute dans la catégorie "Santé & Accès aux soins"
    for categorie in data['categories']:
        if categorie['id'] == 'sante':
            # Vérifier si le sous-thème existe déjà
            if not any(st['id'] == 'animaux-compagnie' for st in categorie['sousThemes']):
                nouveau_sous_theme = {
                    "id": "animaux-compagnie",
                    "nom": "Animaux de compagnie",
                    "propositions": {}
                }

                # Initialiser tous les candidats à null
                for candidat in data['candidats']:
                    nouveau_sous_theme['propositions'][candidat['id']] = None

                # Ajouter la proposition de Barseghian
                nouveau_sous_theme['propositions']['barseghian'] = BARSEGHIAN_DISPENSAIRE_ANIMAUX

                categorie['sousThemes'].append(nouveau_sous_theme)
                sous_theme_ajoute = True
                compteur_barseghian += 1
                print(f"✅ Barseghian - Santé & Accès aux soins > Animaux de compagnie (nouveau sous-thème)")

    # Mise à jour du statut programmeComplet
    for candidat in data['candidats']:
        if candidat['id'] == 'trautmann':
            candidat['programmeComplet'] = False  # 7 mesures (moins de 15)
            candidat['programmeUrl'] = 'https://pokaa.fr/2026/01/14/municipales-2026-a-strasbourg-catherine-trautmann-ps-mise-sur-le-pouvoir-de-vivre/'
        elif candidat['id'] == 'barseghian':
            candidat['programmeComplet'] = False  # 12 mesures annoncées (moins de 15 complètes et chiffrées)
            candidat['programmeUrl'] = 'https://pokaa.fr/2026/01/07/municipales-2026-jeanne-barseghian-devoile-12-mesures-pour-etre-reelue-maire/'

    # Sauvegarde
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Intégration terminée !")
    print(f"   📊 Catherine Trautmann : {compteur_trautmann} propositions")
    print(f"   📊 Jeanne Barseghian : {compteur_barseghian} propositions")
    if sous_theme_ajoute:
        print(f"   ➕ 1 nouveau sous-thème ajouté (Animaux de compagnie)")
    print(f"   💾 Fichier sauvegardé : {JSON_PATH}")


if __name__ == "__main__":
    main()
