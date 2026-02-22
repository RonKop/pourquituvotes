#!/usr/bin/env python3
"""Ajoute des propositions pour Brunel et Lavalette dans toulon-2026.json.
Ne modifie que les sous-thèmes où la valeur actuelle est null.
Ne change PAS programmeComplet."""

import json
import os

FICHIER = os.path.join(os.path.dirname(__file__), "..", "data", "elections", "toulon-2026.json")

# Propositions à ajouter pour Brunel (seulement si null)
BRUNEL_PROPS = {
    "prevention-mediation": {
        "texte": "Police de proximité communautaire travaillant avec les éducateurs, présence humaine renforcée jour et nuit, formation spécifique sur les violences domestiques",
        "source": "Site officiel Toulon en Commun / RCF, 2026",
        "sourceUrl": "https://toulonencommun2026.fr/"
    },
    "logement-social": {
        "texte": "Lutte contre l'habitat indigne, développement du logement social, permis de louer pour combattre les logements insalubres",
        "source": "Site officiel Toulon en Commun / RCF, 2026",
        "sourceUrl": "https://toulonencommun2026.fr/"
    },
    "cantines-fournitures": {
        "texte": "Végétalisation des cantines scolaires, circuits courts, moins de viande, alimentation de qualité et de saison",
        "source": "Site officiel Toulon en Commun / RCF, 2026",
        "sourceUrl": "https://toulonencommun2026.fr/"
    },
    "espaces-verts": {
        "texte": "Projet Bord de Rade pour offrir la mer à tous les Toulonnais : aménagement du littoral accessible, nouveaux espaces publics en bord de rade",
        "source": "Site officiel Toulon en Commun / RCF, 2026",
        "sourceUrl": "https://toulonencommun2026.fr/"
    },
    "centres-sante": {
        "texte": "Amélioration de l'accès aux soins dans les quartiers, dénonciation du manque de moyens à l'hôpital Sainte-Musse",
        "source": "Site officiel Toulon en Commun / RCF, 2026",
        "sourceUrl": "https://toulonencommun2026.fr/"
    },
}

# Propositions à ajouter pour Lavalette (seulement si null)
LAVALETTE_PROPS = {
    "videoprotection": {
        "texte": "Plan de vidéoprotection renforcé sur l'ensemble de la ville, police municipale présente 24h/24",
        "source": "Info83 / CNews, 2026",
        "sourceUrl": "https://www.info83.fr/laure-lavalette-toulon-2026-premier-meeting/"
    },
    "prevention-mediation": {
        "texte": "Application mobile citoyenne pour signaler les dysfonctionnements et nuisances, simplification du travail des services d'intervention",
        "source": "Info83 / CNews, 2026",
        "sourceUrl": "https://www.info83.fr/laure-lavalette-toulon-2026-premier-meeting/"
    },
    "espaces-verts": {
        "texte": "Plan de réhabilitation des rues avec création d'espaces verts, adjoint dédié à la protection du patrimoine naturel et au verdissement",
        "source": "Info83 / CNews, 2026",
        "sourceUrl": "https://www.info83.fr/laure-lavalette-toulon-2026-premier-meeting/"
    },
    "quartiers-prioritaires": {
        "texte": "Chaque quartier traité avec le même intérêt et les mêmes moyens, rééquilibrage des investissements entre centre-ville et quartiers périphériques",
        "source": "Info83 / CNews, 2026",
        "sourceUrl": "https://www.info83.fr/laure-lavalette-toulon-2026-premier-meeting/"
    },
    "equipements-sportifs": {
        "texte": "Développement des équipements sportifs dans chaque quartier, tournois internationaux, lien avec les JO 2030 en région",
        "source": "Info83 / CNews, 2026",
        "sourceUrl": "https://www.info83.fr/laure-lavalette-toulon-2026-premier-meeting/"
    },
    "vie-associative": {
        "texte": "Délégation adjointe au bien-être animal, coordination des politiques de protection animale, liens renforcés avec les associations",
        "source": "Info83 / CNews, 2026",
        "sourceUrl": "https://www.info83.fr/laure-lavalette-toulon-2026-premier-meeting/"
    },
}


def trouver_sous_theme(data, sous_theme_id):
    """Cherche un sous-thème par son id dans toutes les catégories."""
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == sous_theme_id:
                return st
    return None


def main():
    # Lire le fichier
    with open(FICHIER, "r", encoding="utf-8") as f:
        data = json.load(f)

    modifs_brunel = 0
    modifs_lavalette = 0
    skipped_brunel = []
    skipped_lavalette = []

    # Ajouter les propositions Brunel
    for st_id, prop in BRUNEL_PROPS.items():
        st = trouver_sous_theme(data, st_id)
        if st is None:
            print(f"  ERREUR: sous-thème '{st_id}' introuvable !")
            continue
        if st["propositions"].get("brunel") is None:
            st["propositions"]["brunel"] = prop
            modifs_brunel += 1
            print(f"  [brunel] {st_id} : AJOUTÉ")
        else:
            skipped_brunel.append(st_id)
            print(f"  [brunel] {st_id} : IGNORÉ (déjà rempli)")

    # Ajouter les propositions Lavalette
    for st_id, prop in LAVALETTE_PROPS.items():
        st = trouver_sous_theme(data, st_id)
        if st is None:
            print(f"  ERREUR: sous-thème '{st_id}' introuvable !")
            continue
        if st["propositions"].get("lavalette") is None:
            st["propositions"]["lavalette"] = prop
            modifs_lavalette += 1
            print(f"  [lavalette] {st_id} : AJOUTÉ")
        else:
            skipped_lavalette.append(st_id)
            print(f"  [lavalette] {st_id} : IGNORÉ (déjà rempli)")

    # Vérifier que programmeComplet n'a pas changé
    for c in data["candidats"]:
        if c["id"] == "brunel":
            assert c["programmeComplet"] == False, "programmeComplet de brunel a changé !"
        if c["id"] == "lavalette":
            assert c["programmeComplet"] == False, "programmeComplet de lavalette a changé !"

    # Écrire le fichier
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")  # newline finale

    print(f"\nRésumé :")
    print(f"  Brunel   : {modifs_brunel} ajoutées, {len(skipped_brunel)} ignorées {skipped_brunel}")
    print(f"  Lavalette: {modifs_lavalette} ajoutées, {len(skipped_lavalette)} ignorées {skipped_lavalette}")
    print(f"  Fichier sauvegardé : {os.path.abspath(FICHIER)}")


if __name__ == "__main__":
    main()
