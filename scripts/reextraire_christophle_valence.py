#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction de Christophle (Valence)

Source   : Programme officiel 2026 — Paul Christophle
URL      : https://reunirvalence.fr/nos-propositions/
Date     : 2026-02-25
Mesures extraites : 38 mesures dans 14 sous-thèmes

Utilisation :
  1. Exécuter : python scripts/reextraire_christophle_valence.py
  2. Valider : python scripts/valider_donnees.py
  3. Auditer : python scripts/auditer_completude.py --candidat christophle
"""

import io
import json
import os
import sys

# Force UTF-8 pour Windows (cp1252 fix)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# === CONFIGURATION ===
CANDIDAT_ID = "christophle"
VILLE_ID = "valence-2026"
SOURCE = "Programme officiel 2026 — Paul Christophle"
SOURCE_URL = "https://reunirvalence.fr/nos-propositions/"

JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", f"{VILLE_ID}.json")

# === MESURES ===
MESURES = {
    "police-municipale": [
        "Créer des postes fixes et mobiles de police de proximité hors centre-ville.",
        "Expérimenter des brigades anti-incivilités.",
    ],
    "prevention-mediation": [
        "Déployer des médiateurs et éducateurs dans les quartiers délaissés pour la prévention des conflits.",
        "Organiser des semaines de prévention jeunesse avec activités et festivités.",
        "Lancer une grande consultation citoyenne sur l'insécurité avec ateliers et enquête population.",
        "Créer un observatoire de la tranquillité publique.",
        "Développer les travaux d'intérêt général via une convention Maire-Justice.",
    ],
    "violences-femmes": [
        "Ouvrir un centre d'accompagnement des victimes de violences (modèle Citad'elles de Nantes).",
        "Créer des espaces neutres pour déposer plainte hors commissariat.",
        "Former les agents municipaux au repérage des violences sexuelles et mutilations.",
        "Organiser des marches exploratoires de femmes contre le harcèlement dans les transports.",
    ],
    "transports-en-commun": [
        "Étendre le service de transport nocturne à la demande.",
    ],
    "pietons-circulation": [
        "Créer des rues aux enfants à proximité des écoles pour la sécurité et la mobilité active.",
    ],
    "ecoles-renovation": [
        "Réviser les projets de construction scolaire en priorisant efficacité énergétique et bien-être.",
        "Végétaliser 100% des cours d'école avec sols perméables, ombre et nature.",
        "Créer un service de maintenance rapide (factotum) pour les écoles.",
    ],
    "cantines-fournitures": [
        "Repenser les repas scolaires avec des menus flexitariens, bio et locaux.",
        "Distribuer des petits déjeuners gratuits universels en école élémentaire.",
    ],
    "periscolaire-loisirs": [
        "Revaloriser et former les animateurs périscolaires.",
        "Proposer des activités gratuites et diversifiées (artistiques, sportives, numériques, écologiques).",
        "Déployer des moniteurs sportifs municipaux.",
    ],
    "alimentation-durable": [
        "Convoquer une assemblée citoyenne municipale sur la transition écologique.",
        "Établir un droit universel à une alimentation saine avec un système à contribution unique selon les revenus.",
        "Développer les marchés à trois prix garantissant une rémunération juste des producteurs.",
    ],
    "egalite-discriminations": [
        "Faire du respect de l'égalité un critère d'attribution des subventions et marchés publics.",
        "Créer un Conseil municipal de l'égalité femmes-hommes.",
        "Former 100% du personnel municipal à la prévention des discriminations.",
        "Installer des distributeurs de protections menstruelles gratuites dans les toilettes municipales.",
        "Expérimenter le congé menstruel pour les agentes municipales.",
        "Garantir l'égalité salariale femmes-hommes dans l'emploi municipal.",
    ],
    "budget-participatif": [
        "Instaurer un droit de saisine citoyenne des conseils de quartier.",
    ],
    "aide-sociale": [
        "Créer des postes de médiateurs et éducateurs dans les écoles prioritaires.",
        "Mettre en place un plan « lectures » avec mini-bibliothèques dans les quartiers.",
        "Créer des écoles de parents renforçant le partenariat éducatif.",
    ],
    "services-publics": [
        "Renforcer la coopération avec les bailleurs sociaux contre la délinquance.",
    ],
    "accessibilite": [
        "Créer une Maison des femmes regroupant accompagnement juridique, médical et psychologique.",
    ],
}


def main():
    print("=" * 60)
    print(f"  RE-EXTRACTION {CANDIDAT_ID.upper()} ({VILLE_ID})")
    print("=" * 60)

    if not MESURES:
        print("\n  ERREUR : aucune mesure définie dans MESURES")
        sys.exit(1)

    total_new = sum(len(v) for v in MESURES.values())
    print(f"\n  {total_new} mesures dans {len(MESURES)} sous-thèmes")

    # Charger le JSON
    if not os.path.exists(JSON_PATH):
        print(f"\n  ERREUR : fichier introuvable : {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Compter les mesures existantes
    existing_total = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            prop = st["propositions"].get(CANDIDAT_ID)
            if prop and prop.get("mesures"):
                existing_total += len(prop["mesures"])

    # Safety check : abort si nouvelles mesures < 50% des existantes
    if existing_total > 0 and total_new < existing_total * 0.5:
        print(f"\n  SAFETY CHECK ECHOUE !")
        print(f"  Existantes : {existing_total} mesures")
        print(f"  Nouvelles  : {total_new} mesures ({total_new/existing_total*100:.0f}%)")
        print(f"  Seuil      : 50% minimum ({existing_total * 0.5:.0f})")
        print(f"\n  Abandon. Vérifiez que l'extraction est complète.")
        sys.exit(1)

    # Appliquer les nouvelles mesures
    updated = 0
    skipped = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id not in MESURES or not MESURES[st_id]:
                continue

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
            else:
                skipped += 1
                print(f"    SKIP {st_id}: {old_count} existantes > {len(new_mesures)} nouvelles")

    # Sauvegarder
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n  {updated} sous-thèmes mis à jour")
    if skipped:
        print(f"  {skipped} sous-thèmes ignorés (moins de mesures nouvelles)")

    print(f"\n  Prochaines étapes :")
    print(f"    python scripts/valider_donnees.py")
    print(f"    python scripts/auditer_completude.py --candidat {CANDIDAT_ID}")
    print("=" * 60)


if __name__ == "__main__":
    main()
