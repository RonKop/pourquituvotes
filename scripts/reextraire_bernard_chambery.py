#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction des mesures de Bernard (Chambéry) depuis le programme officiel.
Mesures classifiées manuellement dans les sous-thèmes standard.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

MESURES = {
    # === Sécurité ===
    "police-municipale": [
        "Recruter 25 policiers municipaux supplémentaires avec des postes de quartier.",
        "Créer des brigades de soirée et de nuit opérant 7j/7.",
        "Armer la police municipale et doter les agents d'équipement complet.",
        "Créer une brigade canine municipale.",
        "Créer une brigade spécialisée anti-stupéfiants.",
    ],
    "videoprotection": [
        "Installer 250 caméras de vidéoprotection avec un centre de supervision actif.",
    ],
    "prevention-mediation": [
        "Mettre en place un dispositif anti-harcèlement de rue Angela.",
        "Lancer un réseau « Voisins vigilants et solidaires » dans tous les quartiers.",
        "Saisir systématiquement les véhicules en cas de rodéos urbains.",
    ],
    "violences-femmes": [
        "Étendre le réseau Angela contre le harcèlement de rue.",
    ],

    # === Développement économique ===
    "emploi-insertion": [
        "Ouvrir un guichet unique « Entreprendre à Chambéry » pour les créateurs.",
        "Créer des incubateurs municipaux avec loyers progressifs.",
        "Mettre en place une bourse municipale de l'emploi et de l'apprentissage.",
        "Réduire la Cotisation Foncière des Entreprises (CFE).",
    ],
    "commerce-local": [
        "Baisser les redevances de terrasse de 50% la première année.",
        "Soutenir la revitalisation des commerces de quartier.",
        "Développer un label « Produit local chambérien ».",
        "Organiser un marché hebdomadaire de producteurs locaux.",
    ],
    "attractivite": [
        "Étudier une liaison par câble vers les Bauges/La Féclaz.",
        "Créer un prix de l'innovation pour les entreprises locales.",
    ],

    # === Santé et solidarité ===
    "centres-sante": [
        "Créer des cliniques municipales de santé dans les quartiers.",
        "Déployer un bus médical mobile (unité de santé itinérante).",
        "Lancer une campagne de prévention en santé mentale.",
    ],
    "prevention-sante": [
        "Développer la mutuelle communale de santé.",
    ],
    "seniors": [
        "Mettre en place le programme « Bien vieillir à Chambéry ».",
        "Créer un réseau de « Voisins solidaires » pour les personnes isolées.",
        "Distribuer des paniers de Noël aux personnes de plus de 80 ans.",
        "Créer une carte « Aidant » avec des avantages pour les aidants familiaux.",
    ],

    # === Enfance et éducation ===
    "petite-enfance": [
        "Distribuer une carte cadeau naissance de 100€.",
        "Créer des ateliers parents-école.",
        "Soutenir la création de crèches d'entreprise.",
    ],
    "ecoles-renovation": [
        "Lancer le plan « Écoles 2033 » de rénovation et sécurisation.",
        "Augmenter le nombre d'ATSEM dans les écoles maternelles.",
    ],
    "periscolaire-loisirs": [
        "Étendre les horaires de l'accueil périscolaire.",
        "Créer un programme anti-harcèlement scolaire et cyberharcèlement.",
    ],
    "jeunesse": [
        "Créer une Maison des étudiants et de la jeunesse ouverte 7j/7.",
        "Offrir un pass culture et transport étudiant.",
        "Attribuer des bourses au mérite de 250€.",
        "Créer une plateforme de tutorat solidaire étudiante.",
    ],

    # === Gestion financière et gouvernance ===
    "transparence": [
        "Commander un audit financier indépendant dans les 100 premiers jours.",
        "S'engager à ne pas augmenter les impôts locaux pendant le mandat.",
        "Lancer un plan de réduction des dépenses de fonctionnement.",
    ],
    "services-publics": [
        "Nommer un médiateur déontologue.",
        "Créer une charte d'intégrité des élus.",
    ],

    # === Alimentation ===
    "alimentation-durable": [
        "Mettre en place le plan « Manger savoyard » dans les cantines scolaires.",
        "Créer une Maison des producteurs et artisans savoyards.",
        "Garantir le « Zéro gaspillage alimentaire » dans les cantines scolaires.",
    ],
    "cantines-fournitures": [
        "Réformer la tarification des cantines scolaires vers plus d'équité.",
    ],

    # === Culture ===
    "evenements-creation": [
        "Développer des festivals populaires (Fête des fleurs, Médiévale du château, Fête des éléphants).",
        "Organiser un bal populaire et une guinguette sur la place principale.",
        "Lancer un événement annuel « Printemps des talents chambériens ».",
    ],
    "equipements-culturels": [
        "Rénover les infrastructures culturelles.",
        "Renforcer le Conservatoire avec des bourses d'accès.",
        "Créer le programme « Street Art dans nos rues ».",
    ],

    # === Mobilité ===
    "stationnement": [
        "Offrir la première heure de stationnement gratuit en centre-ville.",
        "Créer une carte « Pro-Santé » de stationnement à 20€/an.",
        "Créer une carte « Pro-Commerçant et Artisan » de stationnement.",
        "Simplifier les tarifs du stationnement résidentiel.",
    ],
    "transports-en-commun": [
        "Rendre gratuit le bus seniors en centre-ville.",
        "Créer une navette électrique centre-ville/hôpital/gare.",
    ],
    "velo-mobilites-douces": [
        "Développer un réseau cyclable sécurisé connecté aux villes voisines.",
    ],
    "pietons-circulation": [
        "Synchroniser intelligemment les feux de circulation.",
        "Restaurer un programme complet d'entretien des routes.",
        "Sécuriser les abords des écoles.",
    ],

    # === Environnement ===
    "espaces-verts": [
        "Planter un arbre pour chaque naissance à Chambéry (« Printemps des familles »).",
        "Renforcer l'entretien des parcs et le fleurissement durable.",
        "Développer des jardins partagés et familiaux.",
    ],
    "proprete-dechets": [
        "Lancer un Plan propreté global avec une Brigade verte municipale.",
        "Objectif zéro dépôt sauvage avec sanctions systématiques.",
    ],
    "climat-adaptation": [
        "Créer des espaces rafraîchissants pour les épisodes de chaleur.",
    ],
    "renovation-energetique": [
        "Rénover énergétiquement les bâtiments municipaux.",
        "Moderniser l'éclairage public avec des LED intelligentes.",
        "Installer des bornes de recharge pour véhicules électriques.",
    ],

    # === Sports ===
    "equipements-sportifs": [
        "Rénover les équipements sportifs municipaux.",
        "Créer des espaces « Sport-Santé ».",
    ],
    "sport-pour-tous": [
        "Créer un Pass « Sport-Chambéry » accessible à tous.",
        "Développer l'accessibilité universelle au sport.",
    ],

    # === Urbanisme ===
    "amenagement-urbain": [
        "Développer des circuits patrimoniaux (industriel, ferroviaire).",
    ],

    # === Solidarité ===
    "accessibilite": [
        "Mettre en place une politique d'accessibilité universelle (trottoirs, transports).",
        "Créer un agent municipal de liaison handicap.",
    ],
    "aide-sociale": [
        "Distribuer un chèque « Solidarité énergie » aux ménages en difficulté.",
        "Soutenir directement les associations caritatives locales.",
    ],
    "pouvoir-achat": [
        "S'engager à ne pas augmenter les impôts locaux pendant le mandat.",
    ],
    "acces-logement": [
        "Créer un programme de logement intergénérationnel.",
    ],
    "vie-associative": [
        "Créer un programme d'engagement civique jeunesse.",
    ],
}


def update_candidate(json_path, candidat_id, mesures_dict, source, source_url):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in mesures_dict and len(mesures_dict[st_id]) > 0:
                prop = st["propositions"].get(candidat_id)
                if prop is None:
                    prop = {}
                    st["propositions"][candidat_id] = prop

                old_count = len(prop.get("mesures", []))
                new_mesures = mesures_dict[st_id]

                if len(new_mesures) >= old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = source
                    prop["sourceUrl"] = source_url
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} -> {len(new_mesures)}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total = sum(len(v) for v in mesures_dict.values())
    print(f"    {updated} sous-themes mis a jour, {total} mesures total")
    return total


def main():
    print("=" * 60)
    print("  RE-EXTRACTION BERNARD (Chambery)")
    print("=" * 60)

    json_path = os.path.join(ROOT_DIR, "data", "elections", "chambery-2026.json")
    update_candidate(
        json_path,
        "bernard",
        MESURES,
        "Programme officiel 2026 — Brice Bernard",
        "https://brice-bernard.fr/programme.html",
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
