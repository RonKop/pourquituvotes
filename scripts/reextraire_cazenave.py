#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ré-extraction des mesures de Thomas Cazenave (Bordeaux 2026)
Sources : fairegagnerbordeaux.fr, France Bleu Gironde, Rue89 Bordeaux, Le JDD
"""
import io, json, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "bordeaux-2026.json")
SOURCE = "Programme officiel 2026 — Thomas Cazenave"
SOURCE_URL = "https://www.fairegagnerbordeaux.fr/nos-priorites"
CANDIDAT_ID = "cazenave"

MESURES = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Armer l'ensemble de la police municipale.",
        "Doubler les effectifs de la police municipale pour atteindre 300 agents.",
        "Créer 4 antennes de police de proximité dans les quartiers.",
        "Installer une caserne de police municipale dans le quartier Victoire-Capucins.",
        "Créer une brigade de nuit dédiée à la sécurité nocturne.",
    ],
    "videoprotection": [
        "Doubler le nombre de caméras de vidéosurveillance dans Bordeaux.",
    ],
    "prevention-mediation": [
        "Déployer les mesures du plan sécurité dans les 100 premiers jours du mandat.",
    ],

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Mettre en service un tramway nouvelle génération avec des rames plus longues et des circulations plus fiables.",
        "Faire passer le tramway sur le pont Chaban-Delmas.",
        "Abandonner le projet de téléphérique sur la Garonne.",
        "Abandonner l'étude du métro bordelais.",
    ],
    "velo-mobilites-douces": [
        "Créer une passerelle piétons-vélos reliant les deux rives entre le pont de Pierre et le pont Chaban.",
        "Déployer des bornes de recharge pour véhicules électriques dans toute la ville.",
    ],
    "pietons-circulation": [
        "Réviser les plans de circulation pour désengorger Bordeaux, 2e ville la plus embouteillée de France.",
        "Rétablir intégralement l'éclairage nocturne dans toute la ville.",
        "Rénover les trottoirs dégradés dans tous les quartiers.",
    ],
    "stationnement": [
        "Instaurer la gratuité du stationnement le week-end dans les parkings publics.",
        "Décréter un moratoire sur la suppression de places de parking en surface.",
        "Réviser les tarifs de stationnement pour les rendre plus accessibles.",
    ],
    "tarifs-gratuite": [
        "Gratuité du stationnement le week-end dans les parkings publics pour soutenir les commerces.",
    ],

    # ── LOGEMENT ──
    "logement-social": [
        "Construire de nouveaux logements via la transformation de bureaux vacants, avec objectif de mixité sociale.",
    ],
    "logements-vacants": [
        "Transformer les bureaux vacants du centre-ville en près de 1 000 logements.",
    ],
    "acces-logement": [
        "Lancer un projet d'adaptation des logements pour les seniors.",
    ],

    # ── ÉDUCATION ──
    "cantines-fournitures": [
        "Geler les tarifs des cantines scolaires pour tout le mandat.",
        "Porter à 75 % la part de bio et local dans la restauration collective.",
    ],

    # ── ENVIRONNEMENT ──
    "proprete-dechets": [
        "Remunicipaliser la compétence propreté (fin de la délégation au privé).",
        "Créer des équipes d'intervention rapide dans chaque quartier contre les dépôts sauvages et l'accumulation de saletés.",
        "Mettre en place un plan « zéro débordement » autour des marchés.",
        "Enlever rapidement les encombrants dans tous les quartiers.",
    ],
    "climat-adaptation": [
        "Réutiliser les eaux usées pour la gestion des ressources en eau face au changement climatique.",
        "Réactiver les illuminations des monuments et places de Bordeaux.",
    ],
    "alimentation-durable": [
        "Garantir une majorité de places aux produits bio et locaux dans les marchés bordelais.",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Créer des centres municipaux de santé dans les quartiers en désert médical.",
    ],

    # ── DÉMOCRATIE ──
    "transparence": [
        "Lancer une grande consultation citoyenne pour construire le programme avec les Bordelais.",
        "Organiser l'opération « 1 quartier, 1 programme » : réunions publiques dans chaque quartier.",
    ],
    "services-publics": [
        "Créer 30 quartiers de vie pour rapprocher les services municipaux des habitants.",
    ],

    # ── ÉCONOMIE ──
    "commerce-local": [
        "Soutenir les commerçants via le gel des tarifs et l'amélioration de l'accessibilité.",
        "Redynamiser le commerce local en attirant de nouveaux commerces et entreprises.",
    ],
    "emploi-insertion": [
        "Accueillir 10 000 entrepreneurs à Bordeaux en six ans.",
        "Réconcilier Bordeaux avec le monde économique pour attirer les investissements.",
    ],
    "attractivite": [
        "Faire de Bordeaux une capitale européenne de la culture.",
        "Donner une ambition économique et culturelle de métropole européenne à Bordeaux.",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Lancer la candidature de Bordeaux pour devenir Capitale européenne de la culture.",
        "Développer les équipements culturels existants et soutenir la création locale.",
    ],

    # ── SPORT ──
    "equipements-sportifs": [
        "Renforcer le rayonnement sportif de Bordeaux et développer les infrastructures sportives.",
        "Organiser les « Jeux olympiques des quartiers » au stade Chaban-Delmas.",
    ],

    # ── URBANISME ──
    "amenagement-urbain": [
        "Arrêter les projets jugés inutiles comme le réaménagement des allées de Tourny.",
        "Donner la priorité à la rénovation et à la fluidité urbaine.",
    ],
    "quartiers-prioritaires": [
        "Rénover et sécuriser les quartiers Victoire et Capucins.",
        "Installer une caserne de police municipale dans les quartiers prioritaires.",
    ],

    # ── SOLIDARITÉ ──
    "pouvoir-achat": [
        "Geler les tarifs municipaux pour tout le mandat.",
        "Geler la taxe foncière pour tout le mandat.",
        "Supprimer les projets jugés inutiles pour réorienter le budget vers les besoins quotidiens.",
    ],
}


def main():
    print("=" * 60)
    print(f"  RÉ-EXTRACTION {CANDIDAT_ID.upper()} (Bordeaux)")
    print("=" * 60)
    total = sum(len(v) for v in MESURES.values())
    print(f"\n  {total} mesures dans {len(MESURES)} sous-thèmes")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in MESURES and len(MESURES[st_id]) > 0:
                prop = st["propositions"].get(CANDIDAT_ID)
                if prop is None:
                    prop = {}
                    st["propositions"][CANDIDAT_ID] = prop
                old_count = len(prop.get("mesures", []))
                new_mesures = MESURES[st_id]
                if len(new_mesures) >= old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = SOURCE
                    prop["sourceUrl"] = SOURCE_URL
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} -> {len(new_mesures)}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n    {updated} sous-thèmes mis à jour")
    print("=" * 60)


if __name__ == "__main__":
    main()
