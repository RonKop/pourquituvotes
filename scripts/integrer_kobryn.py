#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du programme complet de Florian Kobryn (LFI, Strasbourg)
15 livrets thématiques, ~400 mesures
Sources principales :
- https://www.rue89strasbourg.com/programme-florian-kobryn-municipales-2026-strasbourg-365805
- https://www.kobryn2026.eu/
- https://pokaa.fr/2025/10/23/un-programme-de-rupture-a-strasbourg-lfi-annonce-ses-mesures-pour-les-municipales-2026/
- Pokaa FACTU (janvier-février 2026)
"""
import json
import os
import sys
import io

# Encodage UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")
ELECTIONS_DIR = os.path.join(ROOT_DIR, "data", "elections")
JSON_PATH = os.path.join(ELECTIONS_DIR, "strasbourg-2026.json")

CANDIDAT_ID = "kobryn"

# Nouvelles propositions à ajouter ou enrichir
# Clé = sous-thème ID, valeur = proposition {texte, source, sourceUrl}
# Ne pas écraser les propositions existantes sauf enrichissement explicite
NOUVELLES_PROPOSITIONS = {
    # === SÉCURITÉ ===
    "police-municipale": {
        "texte": "Instauration d'un récépissé de contrôle à chaque contrôle de police, qu'il soit national ou municipal, pour lutter contre les discriminations et le contrôle au faciès",
        "source": "Rue89 Strasbourg et Pokaa, novembre 2025",
        "sourceUrl": "https://www.rue89strasbourg.com/programme-florian-kobryn-municipales-2026-strasbourg-365805"
    },
    "prevention-mediation": {
        "texte": "Maintien de la salle de consommation à moindre risque (SCMR) et renforcement de la politique de réduction des risques et de prévention en matière de santé publique",
        "source": "Rue89 Strasbourg, novembre 2025",
        "sourceUrl": "https://www.rue89strasbourg.com/programme-florian-kobryn-municipales-2026-strasbourg-365805"
    },

    # === TRANSPORTS ===
    "transports-en-commun": {
        "texte": "Gratuité des transports en commun pour les demandeurs d'emploi, les bénéficiaires du RSA et les personnes sans domicile fixe, et mise en place d'un service de bus 24h/24",
        "source": "Rue89 Strasbourg et Pokaa, octobre-novembre 2025",
        "sourceUrl": "https://pokaa.fr/2025/10/23/un-programme-de-rupture-a-strasbourg-lfi-annonce-ses-mesures-pour-les-municipales-2026/"
    },
    "stationnement": {
        "texte": "Tarification du stationnement résident progressive selon les revenus : gratuité pour les ménages les plus précaires, tarif de base à partir de 5€, et double tarification pour les propriétaires de SUV",
        "source": "Rue89 Strasbourg, novembre 2025",
        "sourceUrl": "https://www.rue89strasbourg.com/programme-florian-kobryn-municipales-2026-strasbourg-365805"
    },

    # === LOGEMENT ===
    "logements-vacants": {
        "texte": "Lutte contre le surtourisme et la conversion des logements en meublés touristiques type Airbnb (200 à 300 appartements perdus chaque année), avec financement de logements d'urgence grâce aux recettes du marché de Noël payant",
        "source": "Pokaa et Rue89 Strasbourg, décembre 2025",
        "sourceUrl": "https://pokaa.fr/2025/12/02/municipales-2026-florian-kobryn-lfi-veut-rendre-le-marche-de-noel-payant-aux-touristes/"
    },

    # === ÉDUCATION ===
    "petite-enfance": {
        "texte": "Garantie d'un mode de garde pour tous les parents, avec renforcement de l'offre de crèches municipales et développement de solutions d'accueil de la petite enfance",
        "source": "Rue89 Strasbourg, novembre 2025",
        "sourceUrl": "https://www.rue89strasbourg.com/programme-florian-kobryn-municipales-2026-strasbourg-365805"
    },
    "jeunesse": {
        "texte": "Stage garanti pour tous les jeunes, en particulier ceux issus des quartiers populaires, afin de lutter contre les inégalités d'accès aux stages et à l'insertion professionnelle",
        "source": "Pokaa et Rue89 Strasbourg, octobre 2025",
        "sourceUrl": "https://pokaa.fr/2025/10/23/un-programme-de-rupture-a-strasbourg-lfi-annonce-ses-mesures-pour-les-municipales-2026/"
    },

    # === ENVIRONNEMENT ===
    "espaces-verts": {
        "texte": "Interdiction progressive des panneaux publicitaires dans l'espace public pour réduire la pollution visuelle et la surconsommation, dans le cadre d'une planification écologique municipale",
        "source": "Rue89 Strasbourg, novembre 2025",
        "sourceUrl": "https://www.rue89strasbourg.com/programme-florian-kobryn-municipales-2026-strasbourg-365805"
    },

    # === SANTÉ ===
    "prevention-sante": {
        "texte": "Politique de prévention en santé publique renforcée, incluant le maintien de la salle de consommation à moindre risque et le développement de centres de santé municipaux accessibles à tous",
        "source": "Rue89 Strasbourg et Pokaa, novembre 2025",
        "sourceUrl": "https://www.rue89strasbourg.com/programme-florian-kobryn-municipales-2026-strasbourg-365805"
    },

    # === ÉCONOMIE ===
    "emploi-insertion": {
        "texte": "Création d'une « Maison des livreurs » pour accompagner et protéger les travailleurs précaires des plateformes numériques de livraison, et renforcement du contrôle des délégations de service public",
        "source": "Rue89 Strasbourg, novembre 2025",
        "sourceUrl": "https://www.rue89strasbourg.com/programme-florian-kobryn-municipales-2026-strasbourg-365805"
    },
    "attractivite": {
        "texte": "Marché de Noël payant (10€) le week-end pour les visiteurs extérieurs à l'Eurométropole afin de lutter contre le surtourisme, avec transports gratuits pendant l'événement et bons d'achat pour les ménages précaires",
        "source": "Pokaa et France 3 Grand Est, décembre 2025",
        "sourceUrl": "https://pokaa.fr/2025/12/02/municipales-2026-florian-kobryn-lfi-veut-rendre-le-marche-de-noel-payant-aux-touristes/"
    },

    # === CULTURE ===
    "evenements-creation": {
        "texte": "Repenser la rénovation de l'Opéra du Rhin en sortant de la course au gigantisme, et création d'un lieu dédié à la culture queer et LGBT permettant aux artistes de créer en sécurité",
        "source": "Rue89 Strasbourg et Pokaa, octobre-novembre 2025",
        "sourceUrl": "https://pokaa.fr/2025/10/23/un-programme-de-rupture-a-strasbourg-lfi-annonce-ses-mesures-pour-les-municipales-2026/"
    },

    # === URBANISME ===
    "quartiers-prioritaires": {
        "texte": "Ancrage prioritaire dans les 9 quartiers populaires de Strasbourg (QPV) avec des candidats issus de 13 quartiers différents et un programme co-construit avec les habitants des quartiers prioritaires",
        "source": "Pokaa, janvier 2026",
        "sourceUrl": "https://pokaa.fr/2026/01/28/municipales-2026-a-strasbourg-florian-kobryn-lfi-part-au-combat-avec-16-noms/"
    },
}

# Propositions existantes à enrichir (remplacer le texte par une version plus complète)
PROPOSITIONS_A_ENRICHIR = {
    "budget-participatif": {
        "texte": "Donner le pouvoir aux citoyens par l'intervention populaire directe : instauration d'un référendum révocatoire permettant de destituer un élu si 20% des électeurs le demandent, et création d'un référendum d'initiative locale",
        "source": "Rue89 Strasbourg et Pokaa, octobre-novembre 2025",
        "sourceUrl": "https://www.rue89strasbourg.com/programme-florian-kobryn-municipales-2026-strasbourg-365805"
    },
    "equipements-culturels": {
        "texte": "Décentraliser la culture et créer une bibliothèque dédiée aux mémoires coloniales, à l'immigration et à l'histoire de France pour lutter contre l'extrême droite, et ouvrir un lieu de culture queer et LGBT à Strasbourg",
        "source": "Rue89 Strasbourg et Pokaa, octobre-novembre 2025",
        "sourceUrl": "https://pokaa.fr/2025/10/23/un-programme-de-rupture-a-strasbourg-lfi-annonce-ses-mesures-pour-les-municipales-2026/"
    },
    "tarifs-gratuite": {
        "texte": "Gratuité des transports en commun pour les moins de 25 ans, les demandeurs d'emploi, les bénéficiaires du RSA et les personnes sans domicile fixe",
        "source": "Rue89 Strasbourg et France Bleu Alsace, octobre 2025 - janvier 2026",
        "sourceUrl": "https://www.rue89strasbourg.com/programme-florian-kobryn-municipales-2026-strasbourg-365805"
    },
}


def main():
    # Charger le JSON
    print(f"Chargement de {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Compteurs
    ajoutees = 0
    enrichies = 0
    ignorees = 0

    # Parcourir toutes les catégories et sous-thèmes
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            props = st["propositions"]

            # Vérifier s'il y a une nouvelle proposition à ajouter
            if st_id in NOUVELLES_PROPOSITIONS:
                if props.get(CANDIDAT_ID) is None:
                    # Ajouter la nouvelle proposition
                    props[CANDIDAT_ID] = NOUVELLES_PROPOSITIONS[st_id]
                    ajoutees += 1
                    print(f"  + Ajouté [{cat['id']}/{st_id}] : {NOUVELLES_PROPOSITIONS[st_id]['texte'][:80]}...")
                else:
                    print(f"  ~ Ignoré [{cat['id']}/{st_id}] : proposition existante non écrasée")
                    ignorees += 1

            # Vérifier s'il y a une proposition à enrichir
            if st_id in PROPOSITIONS_A_ENRICHIR:
                if props.get(CANDIDAT_ID) is not None:
                    ancien_texte = props[CANDIDAT_ID]["texte"][:60]
                    props[CANDIDAT_ID] = PROPOSITIONS_A_ENRICHIR[st_id]
                    enrichies += 1
                    print(f"  * Enrichi [{cat['id']}/{st_id}] : '{ancien_texte}...' -> nouveau texte")

    # Mettre à jour programmeComplet
    # Compter le nombre total de propositions
    total_propositions = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["propositions"].get(CANDIDAT_ID) is not None:
                total_propositions += 1

    print(f"\n=== RÉSUMÉ ===")
    print(f"Propositions ajoutées : {ajoutees}")
    print(f"Propositions enrichies : {enrichies}")
    print(f"Propositions ignorées (déjà existantes) : {ignorees}")
    print(f"Total propositions Kobryn : {total_propositions}")

    # Mettre à jour programmeComplet si >= 15
    for candidat in data["candidats"]:
        if candidat["id"] == CANDIDAT_ID:
            ancien_statut = candidat["programmeComplet"]
            if total_propositions >= 15:
                candidat["programmeComplet"] = True
                candidat["programmeUrl"] = "https://www.kobryn2026.eu/"
                print(f"programmeComplet : {ancien_statut} -> True ({total_propositions} propositions)")
            else:
                print(f"programmeComplet reste {ancien_statut} ({total_propositions} propositions, < 15)")
            break

    # Sauvegarder
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nFichier sauvegardé : {JSON_PATH}")
    print("DONE.")


if __name__ == "__main__":
    main()
