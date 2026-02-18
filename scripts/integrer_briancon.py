#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'intégration des propositions de François Briançon (PS - La gauche unie pour Toulouse)
Sources : vivremieuxtoulouse.fr + recherches web février 2026
"""

import json
import sys
import io

# Force UTF-8 pour stdout (Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Chemin du fichier JSON
JSON_PATH = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\toulouse-2026.json"

# Propositions de François Briançon par sous-thème
PROPOSITIONS = {
    # Sécurité & Prévention
    "police-municipale": {
        "texte": "Soutien aux moyens de la police municipale pour assurer la sécurité de proximité dans tous les quartiers",
        "source": "Révolution Permanente, février 2026",
        "sourceUrl": "https://www.revolutionpermanente.fr/Ex-patron-et-apparatchik-PS-qui-est-Francois-Briancon-candidat-de-la-gauche-unie-a-Toulouse"
    },

    # Transports & Mobilité
    "transports-en-commun": {
        "texte": "Soutien au Service Express Régional Métropolitain (SERM) et abandon du projet Jonction Est",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/"
    },
    "velo-mobilites-douces": {
        "texte": "Mise en place d'un réseau express vélo pour renforcer les mobilités douces et réduire la circulation automobile",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/occitanie/haute-garonne/toulouse/logement-transports-prepare-gauche-unie-vivre-mieux-toulouse-355876/"
    },
    "pietons-circulation": {
        "texte": "Ville à hauteur d'enfants : rues plus calmes, réduction de la circulation automobile, création de cheminements piétonniers et espaces publics avec un espace vert à moins de 300 mètres de chaque habitant",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/occitanie/haute-garonne/toulouse/logement-transports-prepare-gauche-unie-vivre-mieux-toulouse-355876/"
    },
    "tarifs-gratuite": {
        "texte": "Tarification sociale des transports en commun",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/"
    },

    # Logement
    "logement-social": {
        "texte": "15 000 nouveaux logements abordables sur le mandat, dont 7 500 via le Bail Réel Solidaire (BRS)",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/"
    },
    "logements-vacants": {
        "texte": "Réduction de la durée de location autorisée des meublés touristiques de 120 à 90 jours par an et renforcement des contrôles pour lutter contre les logements vacants",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/occitanie/haute-garonne/toulouse/crise-logement-toulouse-comment-gauche-unie-veut-changer-donne-357190/"
    },
    "encadrement-loyers": {
        "texte": "Candidature auprès de l'État pour expérimenter l'encadrement des loyers à Toulouse avant fin 2026",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/"
    },
    "acces-logement": {
        "texte": "Rénovation massive de 30 000 logements sur le mandat",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/"
    },

    # Éducation & Jeunesse
    "petite-enfance": {
        "texte": "1 000 places de crèche supplémentaires pour répondre aux besoins des familles toulousaines",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/occitanie/haute-garonne/toulouse/ecoles-creches-transports-gauche-unie-promet-grandir-mieux-toulouse-361559/"
    },
    "ecoles-renovation": {
        "texte": "Cours oasis dans chaque école : désimperméabilisation des cours pour remplacer l'asphalte par de la terre et des arbres, reconnectant les enfants à la nature",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/occitanie/haute-garonne/municipales-francois-briancon-toulouse-ville-jardin-357792/"
    },
    "cantines-fournitures": {
        "texte": "Gratuité des cantines scolaires et des goûters pour les familles gagnant moins de 1 200 €/mois dès septembre 2026, fournitures scolaires gratuites en CP",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/occitanie/haute-garonne/toulouse/ecoles-creches-transports-gauche-unie-promet-grandir-mieux-toulouse-361559/"
    },
    "jeunesse": {
        "texte": "Transports gratuits pour les moins de 18 ans",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/occitanie/haute-garonne/toulouse/ecoles-creches-transports-gauche-unie-promet-grandir-mieux-toulouse-361559/"
    },

    # Environnement & Transition écologique
    "espaces-verts": {
        "texte": "Toulouse ville-jardin : 3 arbres visibles depuis chaque logement, 30% de couverture végétale par quartier, espace vert à moins de 300m de chaque habitant",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/"
    },
    "climat-adaptation": {
        "texte": "Programme 'sols vivants' : désimperméabilisation de 300 000 m² de surfaces minérales sur le mandat pour favoriser l'infiltration des eaux de pluie et renforcer la biodiversité",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/occitanie/haute-garonne/municipales-francois-briancon-toulouse-ville-jardin-357792/"
    },

    # Démocratie & Vie citoyenne
    "services-publics": {
        "texte": "Retour en régie municipale de la gestion de l'eau et de l'assainissement",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/"
    },

    # Culture & Patrimoine
    "equipements-culturels": {
        "texte": "Augmentation des dépenses culturelles et gratuité totale des bibliothèques municipales",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/"
    },
    "evenements-creation": {
        "texte": "Plan ambitieux pour développer la langue et la culture occitanes du XXIe siècle : transmission de la langue, partage avec tous les habitants, nouvelle gouvernance concertée",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/occitanie/haute-garonne/toulouse/municipales-2026-toulouse-nouveau-ralliement-gauche-autour-francois-briancon-358467/"
    },

    # Solidarité & Égalité
    "pouvoir-achat": {
        "texte": "Suppression de la tarification saisonnière de l'eau pour protéger le pouvoir d'achat",
        "source": "Le Journal Toulousain, février 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/"
    }
}

def main():
    print("=== Intégration du programme de François Briançon ===\n")

    # Charger le JSON
    print(f"Lecture du fichier : {JSON_PATH}")
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Compteur de propositions intégrées
    count = 0

    # Parcourir toutes les catégories et sous-thèmes
    for categorie in data["categories"]:
        for sous_theme in categorie["sousThemes"]:
            sous_theme_id = sous_theme["id"]

            # Si on a une proposition pour ce sous-thème
            if sous_theme_id in PROPOSITIONS:
                # Vérifier si briancon existe déjà
                if "briancon" in sous_theme["propositions"]:
                    if sous_theme["propositions"]["briancon"] is not None:
                        print(f"⚠ Proposition existante pour {sous_theme_id}, remplacement...")

                # Ajouter la proposition
                sous_theme["propositions"]["briancon"] = PROPOSITIONS[sous_theme_id]
                count += 1
                print(f"✓ {categorie['nom']} > {sous_theme['nom']}")

    # Mettre à jour programmeComplet si assez de propositions
    for candidat in data["candidats"]:
        if candidat["id"] == "briancon":
            candidat["programmeComplet"] = count >= 15
            candidat["programmeUrl"] = "https://vivremieuxtoulouse.fr/"
            print(f"\n✓ programmeComplet = {candidat['programmeComplet']} ({count} propositions)")
            print(f"✓ programmeUrl = {candidat['programmeUrl']}")

    # Sauvegarder le JSON
    print(f"\nÉcriture du fichier : {JSON_PATH}")
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {count} propositions intégrées pour François Briançon")
    print("\n📋 Récapitulatif des thématiques couvertes :")
    print(f"   - Sécurité : 1 proposition")
    print(f"   - Transports : 4 propositions")
    print(f"   - Logement : 4 propositions")
    print(f"   - Éducation : 4 propositions")
    print(f"   - Environnement : 2 propositions")
    print(f"   - Démocratie : 1 proposition")
    print(f"   - Culture : 2 propositions")
    print(f"   - Solidarité : 1 proposition")

if __name__ == "__main__":
    main()
