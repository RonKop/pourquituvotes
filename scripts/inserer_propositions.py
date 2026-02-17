#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insertion directe de propositions dans un fichier election JSON.
Utilise par les agents d'extraction automatique.

Usage:
  python scripts/inserer_propositions.py --ville nice --candidat estrosi --json '{"propositions": {...}}'
  python scripts/inserer_propositions.py --ville nice --candidat estrosi --file props_estrosi.json
"""

import argparse
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELECTIONS_DIR = os.path.join(BASE_DIR, "data", "elections")


def insert(ville_id, candidat_id, propositions, source_url=None):
    """Insere des propositions dans le JSON d'election.

    propositions: dict {"categorie/sous-theme": {"texte": "...", "source": "..."}}
    Retourne (inserted, updated, total_in_file).
    """
    path = os.path.join(ELECTIONS_DIR, f"{ville_id}-2026.json")
    if not os.path.exists(path):
        return 0, 0, 0

    with open(path, "r", encoding="utf-8") as f:
        election = json.load(f)

    # Trouver le candidat et sa source URL par defaut
    candidat = None
    for c in election.get("candidats", []):
        if c["id"] == candidat_id:
            candidat = c
            break
    if not candidat:
        print(f"  Candidat '{candidat_id}' introuvable dans {ville_id}")
        return 0, 0, 0

    default_url = source_url or candidat.get("programmeUrl", "#")

    inserted = 0
    updated = 0

    for cat in election["categories"]:
        for st in cat["sousThemes"]:
            key = f"{cat['id']}/{st['id']}"
            if key in propositions:
                prop = propositions[key]
                if not prop or not prop.get("texte"):
                    continue

                new_prop = {
                    "texte": prop["texte"],
                    "source": prop.get("source", "Programme officiel"),
                    "sourceUrl": prop.get("sourceUrl", default_url)
                }
                if prop.get("a_verifier"):
                    new_prop["a_verifier"] = True

                existing = st["propositions"].get(candidat_id)
                if existing and existing is not None and existing.get("texte"):
                    st["propositions"][candidat_id] = new_prop
                    updated += 1
                else:
                    st["propositions"][candidat_id] = new_prop
                    inserted += 1

    # Sauvegarder
    with open(path, "w", encoding="utf-8") as f:
        json.dump(election, f, ensure_ascii=False, indent=2)

    # Compter total propositions pour ce candidat
    total = 0
    for cat in election["categories"]:
        for st in cat["sousThemes"]:
            p = st["propositions"].get(candidat_id)
            if p and p is not None and p.get("texte"):
                total += 1

    # Mettre a jour programmeComplet si >= 15
    if total >= 15 and not candidat.get("programmeComplet"):
        candidat["programmeComplet"] = True
        with open(path, "w", encoding="utf-8") as f:
            json.dump(election, f, ensure_ascii=False, indent=2)
        print(f"  -> programmeComplet = true ({total} propositions)")

    return inserted, updated, total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ville", required=True)
    parser.add_argument("--candidat", required=True)
    parser.add_argument("--json", help="JSON inline")
    parser.add_argument("--file", help="Fichier JSON")
    parser.add_argument("--source-url", help="URL source")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif args.json:
        data = json.loads(args.json)
    else:
        print("Erreur: --json ou --file requis")
        sys.exit(1)

    props = data.get("propositions", data)
    ins, upd, total = insert(args.ville, args.candidat, props, args.source_url)
    print(f"  {args.candidat}@{args.ville}: +{ins} nouvelles, ~{upd} maj, {total} total")


if __name__ == "__main__":
    main()
