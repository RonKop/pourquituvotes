#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corriger_manuels_v3.py — Corrections manuelles des derniers problèmes
=====================================================================
- 6 misclassifications confirmées par revue manuelle
- Reclassification ciblée par texte exact
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


def move_measure(data, candidat_id, src_st_id, dst_st_id, text_fragment):
    """Déplace une mesure d'un sous-thème vers un autre."""
    mesure_text = None
    source_info = {}

    # 1. Trouver et retirer de la source
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] != src_st_id:
                continue
            prop = st.get("propositions", {}).get(candidat_id)
            if not prop or not prop.get("mesures"):
                continue
            for i, m in enumerate(prop["mesures"]):
                if text_fragment in m:
                    mesure_text = prop["mesures"].pop(i)
                    source_info = {
                        "source": prop.get("source", ""),
                        "sourceUrl": prop.get("sourceUrl", ""),
                    }
                    if not prop["mesures"]:
                        del st["propositions"][candidat_id]
                    break
            if mesure_text:
                break
        if mesure_text:
            break

    if not mesure_text:
        return False, f"fragment non trouvé: {text_fragment[:50]}"

    # 2. Ajouter au sous-thème cible
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] != dst_st_id:
                continue
            if "propositions" not in st:
                st["propositions"] = {}
            if candidat_id not in st["propositions"] or st["propositions"][candidat_id] is None:
                st["propositions"][candidat_id] = {
                    "source": source_info.get("source", ""),
                    "sourceUrl": source_info.get("sourceUrl", ""),
                    "mesures": [mesure_text],
                }
            else:
                st["propositions"][candidat_id]["mesures"].append(mesure_text)
            return True, mesure_text

    return False, f"sous-thème cible non trouvé: {dst_st_id}"


def main():
    print("=" * 70)
    print("  CORRECTIONS MANUELLES V3 — Misclassifications confirmées")
    print("=" * 70)

    total = 0
    changelog = []

    # Format: (ville_id, candidat_id, src_st, dst_st, text_fragment)
    MOVES = [
        # Le Havre / philippe — alimentation-durable → proprete-dechets
        # "Promotion du tri des déchets et déploiement de points de collecte"
        ("le-havre-2026", "philippe", "alimentation-durable", "proprete-dechets",
         "tri des déchets"),

        # Montreuil / bessac — pouvoir-achat → cantines-fournitures
        # "Tarification solidaire au quotient familial pour cantines, périscolaire..."
        ("montreuil-2026", "bessac", "pouvoir-achat", "cantines-fournitures",
         "Tarification solidaire au quotient familial pour cantines"),

        # Paris / bournazel — prevention-mediation → police-municipale
        # "Un agent de sécurité municipale par station de métro le soir"
        ("paris-2026", "bournazel", "prevention-mediation", "police-municipale",
         "agent de sécurité municipale par station"),

        # Paris / dati — violences-femmes → police-municipale
        # "Dispositif de sécurisation du bois de Vincennes et du bois de Boulogne"
        ("paris-2026", "dati", "violences-femmes", "police-municipale",
         "Dispositif de sécurisation du bois de Vincennes"),

        # Paris / gregoire — proprete-dechets → police-municipale
        # "Brigades anti-incivilités au sein de la police municipale"
        ("paris-2026", "gregoire", "proprete-dechets", "police-municipale",
         "Brigades anti-incivilités au sein de la police municipale"),

        # Paris / mariani — quartiers-prioritaires → police-municipale
        # "Développer les Zones de Sécurité Prioritaires (ZSP)"
        ("paris-2026", "mariani", "quartiers-prioritaires", "police-municipale",
         "Zones de Sécurité Prioritaires"),

        # Rennes / appere — pietons-circulation → police-municipale
        # "Brigade de sécurité routière au sein de la police municipale"
        ("rennes-2026", "appere", "pietons-circulation", "police-municipale",
         "Brigade de sécurité routière au sein de la police municipale"),
    ]

    for ville_id, cid, src, dst, fragment in MOVES:
        data, path = load_json(ville_id)
        ok, result = move_measure(data, cid, src, dst, fragment)
        if ok:
            save_json(data, path)
            total += 1
            changelog.append(f"  MOVE [{ville_id}/{cid}] {src} → {dst}: {result[:70]}...")
        else:
            changelog.append(f"  SKIP [{ville_id}/{cid}] {src} → {dst}: {result}")

    print(f"\n  {total} mesures reclassées\n")
    for line in changelog:
        print(line)
    print("\n" + "=" * 70)

    return total


if __name__ == "__main__":
    main()
