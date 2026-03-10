#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction des mesures de Mathieu Morel (Issy-les-Moulineaux)
depuis le programme officiel issyecoloetsocial.fr.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "issy-les-moulineaux-2026.json")

SOURCE = "Programme officiel 2026 — Mathieu Morel"
SOURCE_URL = "https://issyecoloetsocial.fr/notre-programme/"

MESURES = {
    "budget-participatif": [
        "Transformer les 4 conseils de quartier en 6 conseils citoyens autonomes, décentralisés et ouverts à tous.",
        "Instaurer un droit de saisine citoyenne permettant aux conseils de soumettre des projets au vote du Conseil municipal.",
        "Organiser des référendums locaux sur l'urbanisme, la sécurité et les grands projets structurants.",
    ],
    "vie-associative": [
        "Contrats d'objectifs pluriannuels et mise à disposition de locaux pour les associations.",
        "Transparence totale des subventions municipales.",
    ],
    "egalite-discriminations": [
        "Plan global contre les violences et discriminations : prévention des violences intrafamiliales, lutte contre sexisme, racisme, antisémitisme et discriminations envers LGBTQIA+ et personnes handicapées.",
    ],
    "services-publics": [
        "Remunicipaliser les services essentiels (eau, équipements sportifs et culturels) à la fin des délégations de service public.",
    ],
    "pietons-circulation": [
        "Autoriser les collectifs d'habitants à transformer temporairement les rues en zones piétonnes.",
        "Créer des rues aux écoles avec piétonisation aux heures d'entrée et sortie.",
        "Élargir les trottoirs pour l'accessibilité PMR.",
    ],
    "velo-mobilites-douces": [
        "Développer un réseau cyclable sécurisé connecté aux villes voisines avec stationnements vélos.",
    ],
    "renovation-energetique": [
        "Rénovation énergétique massive des bâtiments municipaux et logements, aide renforcée à l'isolation thermique.",
        "Objectif neutralité carbone avant 2050.",
    ],
    "espaces-verts": [
        "Plantation de 2000 arbres par an avec désimperméabilisation massive.",
        "Réaliser un atlas de la biodiversité communale pour diagnostiquer et végétaliser les espaces publics.",
    ],
    "alimentation-durable": [
        "Généralisation des circuits courts et produits bio dans les cantines scolaires et maisons de retraite.",
    ],
    "proprete-dechets": [
        "Objectif zéro déchet d'ici 2040 : élimination du plastique à usage unique, tarification incitative au poids.",
        "Ramassage des encombrants sur rendez-vous sous 24h.",
    ],
    "encadrement-loyers": [
        "Plafonnement des loyers et limitation des locations touristiques de courte durée.",
    ],
    "logements-vacants": [
        "Lutte contre les logements vacants et transformation de bureaux en logements.",
    ],
    "acces-logement": [
        "Développer le Bail Réel Solidaire pour l'accession à la propriété à prix maîtrisé.",
        "Développer l'habitat intergénérationnel et les logements très sociaux.",
    ],
    "aide-sociale": [
        "Créer un bus des solidarités mobile pour informer sur les droits sociaux et accompagner les démarches.",
        "Plan municipal pour mères isolées avec objectifs chiffrés (logement, garde d'enfants, accès aux droits).",
    ],
    "commerce-local": [
        "Soutien aux commerces indépendants et développement de l'économie sociale et solidaire.",
    ],
    "centres-sante": [
        "Créer un centre municipal de santé regroupant soignants spécialistes.",
    ],
    "evenements-creation": [
        "Animer les berges de Seine avec guinguettes, fête de la Seine et site de baignade.",
    ],
    "sport-pour-tous": [
        "Garantir que chaque enfant participe à une classe de découverte et ait accès au sport.",
    ],
    "accessibilite": [
        "Installer un ascenseur à la station de métro Mairie d'Issy et aménager la rue Minard.",
    ],
}


def main():
    print("=" * 60)
    print("  RÉ-EXTRACTION MOREL (Issy-les-Moulineaux)")
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
                prop = st["propositions"].get("morel")
                if prop is None:
                    prop = {}
                    st["propositions"]["morel"] = prop

                old_count = len(prop.get("mesures", []))
                new_mesures = MESURES[st_id]

                if len(new_mesures) >= old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = SOURCE
                    prop["sourceUrl"] = SOURCE_URL
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} → {len(new_mesures)}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n    {updated} sous-thèmes mis à jour")
    print("=" * 60)


if __name__ == "__main__":
    main()
