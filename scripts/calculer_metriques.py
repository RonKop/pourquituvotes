#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calcul des métriques agrégées pour #POURQUITUVOTES
====================================================
Lit tous les data/elections/*-2026.json, calcule des métriques
par candidat, par ville et au national. Écrit data/metriques.json.

Usage :
  python scripts/calculer_metriques.py
"""

import io
import json
import math
import os
import re
import sys
from collections import defaultdict

# Force UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
SCHEMA_JSON = os.path.join(DATA_DIR, "schema", "schema_elections.json")
OUTPUT_JSON = os.path.join(DATA_DIR, "metriques.json")

# Regex pour métriques de précision
RE_CHIFFRE = re.compile(r"\d+")
RE_ECHEANCE = re.compile(
    r"202[5-9]|203\d|d[''']ici\b|avant \d{4}|en \d{4}|fin \d{4}|"
    r"d[''']ici \d{4}|horizon \d{4}|à partir de \d{4}",
    re.IGNORECASE,
)


def charger_schema():
    """Charge le schéma et retourne {cat_id: {nom, sousThemes: {st_id: nom}}}."""
    with open(SCHEMA_JSON, "r", encoding="utf-8") as f:
        schema = json.load(f)
    categories = {}
    nb_sous_themes = 0
    for cat in schema["categories"]:
        sts = {}
        for st in cat["sousThemes"]:
            sts[st["id"]] = st["nom"]
            nb_sous_themes += 1
        categories[cat["id"]] = {"nom": cat["nom"], "sousThemes": sts}
    return categories, nb_sous_themes


def collecter_mesures_candidat(election, candidat_id):
    """Collecte toutes les mesures d'un candidat, groupées par catégorie/sous-thème.

    Returns:
        dict: {cat_id: {st_id: [mesure_text, ...]}}
    """
    resultat = defaultdict(lambda: defaultdict(list))
    for cat in election.get("categories", []):
        for st in cat.get("sousThemes", []):
            prop = st.get("propositions", {}).get(candidat_id)
            if not prop:
                continue
            mesures = prop.get("mesures", [])
            if mesures:
                resultat[cat["id"]][st["id"]] = list(mesures)
    return resultat


def calculer_metriques_candidat(mesures_par_cat, schema_cats, nb_st_total):
    """Calcule les métriques pour un candidat donné.

    Args:
        mesures_par_cat: {cat_id: {st_id: [mesures]}}
        schema_cats: schéma des catégories
        nb_st_total: nombre total de sous-thèmes standard (43)

    Returns:
        dict de métriques
    """
    toutes_mesures = []
    cats_couvertes = set()
    sts_couverts = set()
    mesures_par_categorie = {}
    mesures_par_sous_theme = {}

    for cat_id, sts in mesures_par_cat.items():
        cat_total = 0
        for st_id, mesures in sts.items():
            nb = len(mesures)
            if nb > 0:
                cats_couvertes.add(cat_id)
                sts_couverts.add(st_id)
                toutes_mesures.extend(mesures)
                cat_total += nb
                mesures_par_sous_theme[st_id] = nb
        if cat_total > 0:
            mesures_par_categorie[cat_id] = cat_total

    total = len(toutes_mesures)
    if total == 0:
        return {
            "total_mesures": 0,
            "couverture_sous_themes": 0,
            "couverture_sous_themes_max": nb_st_total,
            "couverture_categories": 0,
            "couverture_categories_max": 12,
            "pct_mesures_chiffrees": 0,
            "pct_mesures_avec_echeance": 0,
            "longueur_moyenne_mesure": 0,
            "top3_themes": [],
            "profil_thematique": {},
        }

    # Précision : % chiffré, % avec échéance
    nb_chiffrees = sum(1 for m in toutes_mesures if RE_CHIFFRE.search(m))
    nb_echeance = sum(1 for m in toutes_mesures if RE_ECHEANCE.search(m))
    longueur_moy = round(sum(len(m) for m in toutes_mesures) / total)

    # Top 3 thèmes (catégories) par volume
    cats_triees = sorted(mesures_par_categorie.items(), key=lambda x: -x[1])
    top3 = []
    for cat_id, nb in cats_triees[:3]:
        nom = schema_cats.get(cat_id, {}).get("nom", cat_id)
        top3.append({"id": cat_id, "nom": nom, "nb_mesures": nb})

    # Profil thématique : répartition en %
    profil = {}
    for cat_id, nb in mesures_par_categorie.items():
        profil[cat_id] = round(nb / total * 100, 1)

    return {
        "total_mesures": total,
        "couverture_sous_themes": len(sts_couverts),
        "couverture_sous_themes_max": nb_st_total,
        "couverture_categories": len(cats_couvertes),
        "couverture_categories_max": 12,
        "pct_mesures_chiffrees": round(nb_chiffrees / total * 100, 1),
        "pct_mesures_avec_echeance": round(nb_echeance / total * 100, 1),
        "longueur_moyenne_mesure": longueur_moy,
        "top3_themes": top3,
        "profil_thematique": profil,
    }


def calculer_theme_clivant(candidats_metriques):
    """Trouve le thème où l'écart de couverture est maximal entre candidats.

    Args:
        candidats_metriques: liste de dicts candidat avec profil_thematique

    Returns:
        {id, nom, ecart} ou None
    """
    if len(candidats_metriques) < 2:
        return None

    # Collecter toutes les catégories présentes
    all_cats = set()
    for c in candidats_metriques:
        all_cats.update(c["metriques"]["profil_thematique"].keys())

    meilleur = None
    meilleur_ecart = 0

    for cat_id in all_cats:
        pcts = [
            c["metriques"]["profil_thematique"].get(cat_id, 0)
            for c in candidats_metriques
        ]
        ecart = max(pcts) - min(pcts)
        if ecart > meilleur_ecart:
            meilleur_ecart = ecart
            meilleur = cat_id

    return {"id": meilleur, "ecart": round(meilleur_ecart, 1)} if meilleur else None


def main():
    if not os.path.exists(ELECTIONS_DIR):
        print(f"ERREUR : dossier introuvable : {ELECTIONS_DIR}")
        sys.exit(1)

    schema_cats, nb_st_total = charger_schema()

    fichiers = sorted(f for f in os.listdir(ELECTIONS_DIR) if f.endswith(".json"))

    villes = []
    tous_candidats_nationaux = []  # pour top10 et stats nationales
    mesures_par_theme_national = defaultdict(int)  # cat_id -> total mesures

    for fichier in fichiers:
        ville_id = fichier.replace(".json", "")
        path = os.path.join(ELECTIONS_DIR, fichier)

        with open(path, "r", encoding="utf-8") as f:
            election = json.load(f)

        ville_nom = election.get("ville", ville_id)
        candidats_ville = []

        for candidat in election.get("candidats", []):
            cid = candidat["id"]
            est_complet = candidat.get("programmeComplet", False)

            mesures_par_cat = collecter_mesures_candidat(election, cid)
            metriques = calculer_metriques_candidat(mesures_par_cat, schema_cats, nb_st_total)

            candidat_data = {
                "id": cid,
                "nom": candidat.get("nom", cid),
                "liste": candidat.get("liste", ""),
                "programmeComplet": est_complet,
                "metriques": metriques,
            }
            candidats_ville.append(candidat_data)

            # Accumuler pour les stats nationales
            if metriques["total_mesures"] > 0:
                tous_candidats_nationaux.append({
                    "id": cid,
                    "nom": candidat.get("nom", cid),
                    "ville": ville_nom,
                    "ville_id": ville_id,
                    "total_mesures": metriques["total_mesures"],
                    "pct_mesures_chiffrees": metriques["pct_mesures_chiffrees"],
                })
                for cat_id, pct in metriques["profil_thematique"].items():
                    mesures_par_theme_national[cat_id] += round(
                        pct / 100 * metriques["total_mesures"]
                    )

        # Métriques ville
        nb_candidats = len(candidats_ville)
        nb_complets = sum(1 for c in candidats_ville if c["programmeComplet"])
        nb_avec_mesures = sum(
            1 for c in candidats_ville if c["metriques"]["total_mesures"] > 0
        )
        total_mesures_ville = sum(
            c["metriques"]["total_mesures"] for c in candidats_ville
        )

        # Candidat le plus détaillé
        candidat_plus = max(
            candidats_ville,
            key=lambda c: c["metriques"]["total_mesures"],
            default=None,
        )
        candidat_plus_info = None
        if candidat_plus and candidat_plus["metriques"]["total_mesures"] > 0:
            candidat_plus_info = {
                "id": candidat_plus["id"],
                "nom": candidat_plus["nom"],
                "total_mesures": candidat_plus["metriques"]["total_mesures"],
            }

        # Thème le plus couvert (par volume total de mesures dans la ville)
        themes_ville = defaultdict(int)
        for c in candidats_ville:
            for cat_id, pct in c["metriques"]["profil_thematique"].items():
                themes_ville[cat_id] += round(
                    pct / 100 * c["metriques"]["total_mesures"]
                )
        theme_plus = None
        if themes_ville:
            top_cat = max(themes_ville.items(), key=lambda x: x[1])
            theme_plus = {
                "id": top_cat[0],
                "nom": schema_cats.get(top_cat[0], {}).get("nom", top_cat[0]),
                "total_mesures": top_cat[1],
            }

        # Thème le plus clivant
        theme_clivant = calculer_theme_clivant(candidats_ville)
        if theme_clivant and theme_clivant["id"]:
            theme_clivant["nom"] = schema_cats.get(
                theme_clivant["id"], {}
            ).get("nom", theme_clivant["id"])

        villes.append({
            "id": ville_id,
            "nom": ville_nom,
            "nb_candidats": nb_candidats,
            "nb_complets": nb_complets,
            "nb_avec_mesures": nb_avec_mesures,
            "total_mesures": total_mesures_ville,
            "candidat_plus_detaille": candidat_plus_info,
            "theme_plus_couvert": theme_plus,
            "theme_plus_clivant": theme_clivant,
            "candidats": candidats_ville,
        })

    # === Stats nationales ===
    total_villes = len(villes)
    total_candidats = sum(v["nb_candidats"] for v in villes)
    total_mesures = sum(v["total_mesures"] for v in villes)

    # Thèmes ranking national
    themes_ranking = []
    for cat_id, total in sorted(
        mesures_par_theme_national.items(), key=lambda x: -x[1]
    ):
        themes_ranking.append({
            "id": cat_id,
            "nom": schema_cats.get(cat_id, {}).get("nom", cat_id),
            "total_mesures": total,
        })

    # Top 10 candidats par volume
    top10 = sorted(
        tous_candidats_nationaux, key=lambda c: -c["total_mesures"]
    )[:10]

    # % moyen chiffré (pondéré par nombre de mesures)
    total_chiffre_pondere = sum(
        c["pct_mesures_chiffrees"] * c["total_mesures"]
        for c in tous_candidats_nationaux
    )
    pct_moyen_chiffre = (
        round(total_chiffre_pondere / total_mesures, 1) if total_mesures > 0 else 0
    )

    # Assemblage final
    metriques = {
        "genere_le": __import__("datetime").datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "national": {
            "total_villes": total_villes,
            "total_candidats": total_candidats,
            "total_mesures": total_mesures,
            "themes_ranking": themes_ranking,
            "top10_candidats": top10,
            "pct_moyen_chiffre": pct_moyen_chiffre,
        },
        "villes": villes,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(metriques, f, ensure_ascii=False, indent=2)

    print(f"Métriques générées : {OUTPUT_JSON}")
    print(f"  {total_villes} villes, {total_candidats} candidats, {total_mesures} mesures")
    print(f"  Top thème : {themes_ranking[0]['nom']} ({themes_ranking[0]['total_mesures']} mesures)" if themes_ranking else "")
    print(f"  % moyen chiffré : {pct_moyen_chiffre}%")


if __name__ == "__main__":
    main()
