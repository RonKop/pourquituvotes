#!/usr/bin/env python3
"""
generer_themes.py — Génère 12 fichiers thématiques agrégés dans data/themes/
à partir des fichiers d'élections individuels (data/elections/*-2026.json).

Produit aussi une mise à jour de data/stats-global.json.

Usage : python scripts/generer_themes.py
"""

import json
import os
import glob
import random

# ── Chemins ──────────────────────────────────────────────────────────────────
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
THEMES_DIR = os.path.join(DATA_DIR, "themes")
VILLES_JSON = os.path.join(DATA_DIR, "villes.json")
SCHEMA_JSON = os.path.join(DATA_DIR, "schema", "schema_elections.json")
STATS_JSON = os.path.join(DATA_DIR, "stats-global.json")


def load_json(path):
    """Charge un fichier JSON en UTF-8."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    """Écrit un fichier JSON en UTF-8 (pretty-print, accents conservés)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> {os.path.relpath(path, ROOT_DIR)}")


def truncate_text(text, max_len=200):
    """Tronque un texte à max_len caractères en ajoutant '...' si nécessaire."""
    if len(text) <= max_len:
        return text
    # Coupe au dernier espace avant max_len pour ne pas couper un mot
    cut = text[:max_len].rfind(" ")
    if cut == -1:
        cut = max_len
    return text[:cut] + "..."


def main():
    print("=" * 60)
    print("Génération des fichiers thématiques")
    print("=" * 60)

    # ── 1. Charger le schéma (12 catégories) ────────────────────────────────
    print("\n1. Chargement du schéma...")
    schema = load_json(SCHEMA_JSON)
    categories_schema = {cat["id"]: cat for cat in schema["categories"]}
    print(f"   {len(categories_schema)} catégories trouvées dans le schéma")

    # ── 2. Charger villes.json pour le mapping id → nom ─────────────────────
    print("\n2. Chargement de villes.json...")
    villes_list = load_json(VILLES_JSON)
    villes_map = {v["id"]: v["nom"] for v in villes_list}
    print(f"   {len(villes_map)} villes référencées")

    # ── 3. Lister les fichiers d'élection ────────────────────────────────────
    print("\n3. Lecture des fichiers d'élection...")
    election_files = sorted(glob.glob(os.path.join(ELECTIONS_DIR, "*-2026.json")))
    print(f"   {len(election_files)} fichiers trouvés")

    # ── 4. Structure d'accumulation par thème ────────────────────────────────
    # theme_data[cat_id] = {
    #   "villes": { ville_id: { "nom", "candidats": { cand_id: { "nom", "liste", "nb" } }, "nb" } },
    #   "all_propositions": [ { villeId, ville, candidatId, candidat, liste, sousTheme, sousThemeNom, texte, source } ]
    # }
    theme_data = {}
    for cat_id in categories_schema:
        theme_data[cat_id] = {
            "villes": {},
            "all_propositions": []
        }

    # ── 5. Parcourir chaque fichier d'élection ───────────────────────────────
    for filepath in election_files:
        filename = os.path.basename(filepath)
        # Extraire l'id de la ville : "paris-2026.json" → "paris"
        ville_id = filename.replace("-2026.json", "")
        ville_nom = villes_map.get(ville_id, ville_id.replace("-", " ").title())

        try:
            election = load_json(filepath)
        except (json.JSONDecodeError, IOError) as e:
            print(f"   ERREUR lecture {filename}: {e}")
            continue

        # Index des candidats pour accès rapide
        candidats_index = {}
        for cand in election.get("candidats", []):
            candidats_index[cand["id"]] = cand

        # Parcourir les catégories de ce fichier
        for cat in election.get("categories", []):
            cat_id = cat["id"]
            if cat_id not in theme_data:
                # Catégorie spécifique à la ville, pas dans le schéma universel — ignorer
                continue

            td = theme_data[cat_id]

            for st in cat.get("sousThemes", []):
                st_id = st["id"]
                st_nom = st["nom"]
                propositions = st.get("propositions", {})

                for cand_id, prop in propositions.items():
                    # prop peut être null si le candidat n'a pas de proposition
                    if prop is None:
                        continue
                    texte = prop.get("texte", "")
                    if not texte or not texte.strip():
                        continue

                    # Récupérer les infos du candidat
                    cand_info = candidats_index.get(cand_id, {})
                    cand_nom = cand_info.get("nom", cand_id)
                    cand_liste = cand_info.get("liste", "")

                    # Accumuler dans la ville
                    if ville_id not in td["villes"]:
                        td["villes"][ville_id] = {
                            "nom": ville_nom,
                            "candidats": {},
                            "nb": 0
                        }
                    ville_entry = td["villes"][ville_id]
                    ville_entry["nb"] += 1

                    if cand_id not in ville_entry["candidats"]:
                        ville_entry["candidats"][cand_id] = {
                            "nom": cand_nom,
                            "liste": cand_liste,
                            "nb": 0
                        }
                    ville_entry["candidats"][cand_id]["nb"] += 1

                    # Stocker la proposition pour sélection des marquantes
                    td["all_propositions"].append({
                        "villeId": ville_id,
                        "ville": ville_nom,
                        "candidatId": cand_id,
                        "candidat": cand_nom,
                        "liste": cand_liste,
                        "sousTheme": st_id,
                        "sousThemeNom": st_nom,
                        "texte": texte,
                        "source": prop.get("source", "")
                    })

        print(f"   {filename} ({ville_nom})")

    # ── 6. Générer les fichiers thématiques ──────────────────────────────────
    print(f"\n4. Génération des {len(categories_schema)} fichiers thématiques...")
    os.makedirs(THEMES_DIR, exist_ok=True)

    stats_global_categories = []

    for cat_id, cat_schema in categories_schema.items():
        td = theme_data[cat_id]

        # Construire la liste des villes triée par nbPropositions décroissant
        villes_list_out = []
        for ville_id, ville_info in td["villes"].items():
            if ville_info["nb"] == 0:
                continue

            # Candidats avec au moins 1 proposition, triés par nb décroissant
            candidats_out = []
            for cand_id, cand_info in ville_info["candidats"].items():
                if cand_info["nb"] == 0:
                    continue
                candidats_out.append({
                    "id": cand_id,
                    "nom": cand_info["nom"],
                    "nbPropositions": cand_info["nb"]
                })
            candidats_out.sort(key=lambda c: c["nbPropositions"], reverse=True)

            villes_list_out.append({
                "id": ville_id,
                "nom": ville_info["nom"],
                "nbPropositions": ville_info["nb"],
                "candidats": candidats_out
            })

        # Tri par nbPropositions décroissant
        villes_list_out.sort(key=lambda v: v["nbPropositions"], reverse=True)

        # Statistiques
        total_propositions = sum(v["nbPropositions"] for v in villes_list_out)
        villes_avec_propositions = len(villes_list_out)
        candidats_avec_propositions = sum(
            len(v["candidats"]) for v in villes_list_out
        )

        # Sélection des propositions marquantes (jusqu'à 10, diversité de villes)
        propositions_marquantes = select_propositions_marquantes(
            td["all_propositions"], max_count=10
        )

        # Sous-thèmes depuis le schéma
        sous_themes_out = [
            {"id": st["id"], "nom": st["nom"]}
            for st in cat_schema["sousThemes"]
        ]

        # Construire le fichier de sortie
        theme_file = {
            "id": cat_id,
            "nom": cat_schema["nom"],
            "sousThemes": sous_themes_out,
            "stats": {
                "totalPropositions": total_propositions,
                "villesAvecPropositions": villes_avec_propositions,
                "candidatsAvecPropositions": candidats_avec_propositions
            },
            "villes": villes_list_out,
            "propositions_marquantes": propositions_marquantes
        }

        output_path = os.path.join(THEMES_DIR, f"{cat_id}.json")
        save_json(output_path, theme_file)

        stats_global_categories.append({
            "id": cat_id,
            "count": total_propositions
        })

        print(f"   {cat_schema['nom']}: {total_propositions} propositions, "
              f"{villes_avec_propositions} villes, "
              f"{candidats_avec_propositions} candidats")

    # ── 7. Mettre à jour stats-global.json ───────────────────────────────────
    print("\n5. Mise à jour de stats-global.json...")
    # Trier par count décroissant (comme le fichier existant)
    stats_global_categories.sort(key=lambda c: c["count"], reverse=True)
    stats_global = {"categories": stats_global_categories}
    save_json(STATS_JSON, stats_global)

    # ── 8. Résumé ────────────────────────────────────────────────────────────
    total_all = sum(c["count"] for c in stats_global_categories)
    print(f"\nTerminé ! {len(categories_schema)} fichiers thématiques générés.")
    print(f"Total général : {total_all} propositions")
    print("=" * 60)


def select_propositions_marquantes(all_propositions, max_count=10):
    """
    Sélectionne jusqu'à max_count propositions marquantes.
    Critères :
    - Diversité de villes (pas toutes de la même ville)
    - Préférence pour les textes plus courts et percutants
    - Tronque à 200 caractères si nécessaire
    """
    if not all_propositions:
        return []

    # Trier par longueur de texte (plus court = plus percutant en général)
    sorted_props = sorted(all_propositions, key=lambda p: len(p["texte"]))

    selected = []
    villes_used = {}  # ville_id → nombre de fois sélectionnée
    max_per_ville = 2  # Maximum 2 propositions par ville pour la diversité

    for prop in sorted_props:
        if len(selected) >= max_count:
            break

        ville_id = prop["villeId"]
        if villes_used.get(ville_id, 0) >= max_per_ville:
            continue

        villes_used[ville_id] = villes_used.get(ville_id, 0) + 1
        selected.append({
            "villeId": prop["villeId"],
            "ville": prop["ville"],
            "candidatId": prop["candidatId"],
            "candidat": prop["candidat"],
            "liste": prop["liste"],
            "sousTheme": prop["sousTheme"],
            "sousThemeNom": prop["sousThemeNom"],
            "texte": truncate_text(prop["texte"], 200),
            "source": prop["source"]
        })

    # Si on n'a pas assez de propositions (toutes les villes épuisées à max_per_ville),
    # relâcher la contrainte et en prendre d'autres
    if len(selected) < max_count:
        remaining = [
            p for p in sorted_props
            if not any(
                s["villeId"] == p["villeId"]
                and s["candidatId"] == p["candidatId"]
                and s["sousTheme"] == p["sousTheme"]
                for s in selected
            )
        ]
        for prop in remaining:
            if len(selected) >= max_count:
                break
            selected.append({
                "villeId": prop["villeId"],
                "ville": prop["ville"],
                "candidatId": prop["candidatId"],
                "candidat": prop["candidat"],
                "liste": prop["liste"],
                "sousTheme": prop["sousTheme"],
                "sousThemeNom": prop["sousThemeNom"],
                "texte": truncate_text(prop["texte"], 200),
                "source": prop["source"]
            })

    return selected


if __name__ == "__main__":
    main()
