#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corriger_manuels_v2.py — Corrections manuelles issues de la revue détaillée
============================================================================
Traite les cas que corriger_audit.py ne peut pas gérer automatiquement :
- Doublons < 0.88 similarité mais confirmés manuellement
- Bilan confirmé (2 cas)
- Suppressions ciblées

NE TOUCHE PAS Kobryn (Strasbourg).
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ELECTIONS_DIR = os.path.join(ROOT_DIR, "data", "elections")


def load_json(ville_id):
    path = os.path.join(ELECTIONS_DIR, f"{ville_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), path


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def find_and_remove(data, candidat_id, st_id, text_fragment):
    """Trouve et supprime une mesure par candidat, sous-thème et fragment de texte.
    Retourne True si trouvée et supprimée."""
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] != st_id:
                continue
            prop = st.get("propositions", {}).get(candidat_id)
            if not prop or not prop.get("mesures"):
                continue
            for i, m in enumerate(prop["mesures"]):
                if text_fragment in m:
                    removed = prop["mesures"].pop(i)
                    if not prop["mesures"]:
                        del st["propositions"][candidat_id]
                    return True, removed
    return False, None


def main():
    print("=" * 70)
    print("  CORRECTIONS MANUELLES V2 — Doublons + Bilan confirmés")
    print("=" * 70)

    total = 0
    changelog = []

    # ================================================================
    # DOUBLONS CONFIRMÉS (hors Kobryn, hors ceux déjà traités par corriger_audit)
    # Format: (ville_id, candidat_id, st_to_remove_from, text_fragment)
    # ================================================================
    DOUBLONS = [
        # Aix-en-Provence / klein — jeunesse#1 dup of #0
        ("aix-en-provence-2026", "klein", "jeunesse",
         "Transformer les bureaux vides en logements pour étudiants"),

        # Grenoble / ruffin — pouvoir-achat#1 dup of renovation-energetique#0
        ("grenoble-2026", "ruffin", "pouvoir-achat",
         "pôle public de l'énergie"),

        # Le Chesnay / democratie-courtoise — commerce-local#3 dup of pouvoir-achat#0
        ("chesnay-rocquencourt-2026", "democratie-courtoise", "commerce-local",
         "chèques d'achat aux habitants défavorisés"),

        # Le Havre / zarifian — alimentation-durable#1 dup of cantines-fournitures#1
        ("le-havre-2026", "zarifian", "alimentation-durable",
         "circuits courts dans les cantines"),

        # Limoges / miguel — aide-sociale#2 dup of pouvoir-achat#0
        ("limoges-2026", "miguel", "aide-sociale",
         "coopérative du pouvoir d'achat"),

        # Orléans / chapuis — prevention-mediation#0 dup of violences-femmes#0
        ("orleans-2026", "chapuis", "prevention-mediation",
         "safe spaces"),

        # Paris / dati — alimentation-durable#1 dup of prevention-sante#1
        ("paris-2026", "dati", "alimentation-durable",
         "nuisibles"),

        # Paris / mariani — quartiers-prioritaires#1 dup of emploi-insertion#1
        ("paris-2026", "mariani", "quartiers-prioritaires",
         "zones franches pour revitaliser"),

        # Rennes / trousseau — amenagement-urbain#0 dup of climat-adaptation#0
        ("rennes-2026", "trousseau", "amenagement-urbain",
         "Aménagement du territoire en adéquation avec les enjeux environnementaux"),

        # Rouen / mayer-rossignol — petite-enfance#1 dup of petite-enfance#0
        ("rouen-2026", "mayer-rossignol", "petite-enfance",
         "Bouclier social complet pour les familles monoparentales"),

        # Rueil-Malmaison / indjian — quartiers-prioritaires#1 dup of egalite-discriminations#0
        ("rueil-malmaison-2026", "indjian", "quartiers-prioritaires",
         "victimes de discriminations"),
    ]

    for ville_id, cid, st_id, fragment in DOUBLONS:
        data, path = load_json(ville_id)
        ok, removed = find_and_remove(data, cid, st_id, fragment)
        if ok:
            save_json(data, path)
            total += 1
            changelog.append(f"  DOUBLON [{ville_id}/{cid}] supprimé {st_id}: {removed[:70]}...")
        else:
            changelog.append(f"  SKIP [{ville_id}/{cid}] {st_id}: fragment non trouvé: {fragment[:50]}")

    # ================================================================
    # BILAN CONFIRMÉ (2 cas identifiés par analyse)
    # ================================================================
    BILAN = [
        # Quimper / assih — budget-participatif#0 : backward-looking "49 projets depuis 2020"
        ("quimper-2026", "assih", "budget-participatif",
         "49 projets citoyens réalisés ou engagés"),

        # Reims / robinet — police-municipale#0 : backward-looking "de 30 à 130 agents depuis 2014"
        ("reims-2026", "robinet", "police-municipale",
         "de 30 à 130 agents depuis 2014"),
    ]

    for ville_id, cid, st_id, fragment in BILAN:
        data, path = load_json(ville_id)
        ok, removed = find_and_remove(data, cid, st_id, fragment)
        if ok:
            save_json(data, path)
            total += 1
            changelog.append(f"  BILAN [{ville_id}/{cid}] supprimé {st_id}: {removed[:70]}...")
        else:
            changelog.append(f"  SKIP [{ville_id}/{cid}] {st_id}: fragment non trouvé: {fragment[:50]}")

    # ================================================================
    # Résumé
    # ================================================================
    print(f"\n  {total} corrections appliquées\n")
    for line in changelog:
        print(line)
    print("\n" + "=" * 70)

    return total


if __name__ == "__main__":
    main()
