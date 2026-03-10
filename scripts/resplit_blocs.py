#!/usr/bin/env python3
"""
resplit_blocs.py — Re-découpe les blocs monolithiques dans les JSON élections.

Parcourt tous les fichiers data/elections/*.json et cherche les tableaux
de mesures contenant un seul élément de plus de 200 caractères.
Tente de le re-découper en mesures individuelles selon plusieurs stratégies.
"""

import sys
import io
import os
import re
import json
import glob

# Encodage console Windows (cp1252 → utf-8)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ELECTIONS_DIR = os.path.join(ROOT_DIR, "data", "elections")

MIN_MEASURE_LEN = 20
MONOLITHIC_THRESHOLD = 200


def split_monolithic(text):
    """Tente de découper un bloc monolithique en mesures individuelles.

    Stratégies (dans l'ordre) :
      a) Split sur ". " suivi d'une majuscule ou d'un chiffre
      b) Split sur "; " suivi d'une minuscule (listes séparées par points-virgules)
      c) Retourne le texte original si aucune stratégie ne produit >1 résultat

    Retourne une liste de mesures nettoyées.
    """

    # Stratégie a : ". " + majuscule/chiffre
    parts = re.split(r"\.\s+(?=[A-ZÉÈÊÀÂÔÙÇ0-9])", text)
    if len(parts) > 1:
        return _clean_parts(parts)

    # Stratégie b : "; " + minuscule
    parts = re.split(r";\s+(?=[a-zéèêàâ])", text)
    if len(parts) > 1:
        return _clean_parts(parts)

    # Aucune stratégie n'a fonctionné → garder tel quel
    return [text]


def _clean_parts(parts):
    """Nettoie les sous-mesures issues du split.

    - Supprime les espaces en début/fin
    - Filtre les sous-mesures de moins de MIN_MEASURE_LEN caractères
    - Ajoute un "." final si la mesure ne termine pas par . ! ? )
    """
    cleaned = []
    for part in parts:
        part = part.strip()
        if len(part) < MIN_MEASURE_LEN:
            continue
        if not part.endswith((".", "!", "?", ")")):
            part += "."
        cleaned.append(part)
    return cleaned if cleaned else parts  # fallback : renvoyer l'original si tout filtré


def process_file(filepath):
    """Traite un fichier JSON d'élection. Retourne (modifications, ville)."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    ville = data.get("ville", os.path.basename(filepath))
    candidats_map = {c["id"]: c["nom"] for c in data.get("candidats", [])}
    modifications = []
    changed = False

    for cat in data.get("categories", []):
        for st in cat.get("sousThemes", []):
            propositions = st.get("propositions", {})
            for candidat_id, prop in propositions.items():
                mesures = prop.get("mesures", [])
                if len(mesures) != 1:
                    continue
                texte = mesures[0]
                if len(texte) <= MONOLITHIC_THRESHOLD:
                    continue

                # Bloc monolithique détecté — tenter le split
                nouvelles = split_monolithic(texte)
                if len(nouvelles) > 1:
                    prop["mesures"] = nouvelles
                    changed = True
                    nom_candidat = candidats_map.get(candidat_id, candidat_id)
                    modifications.append(
                        (nom_candidat, cat["id"], st["id"], 1, len(nouvelles))
                    )

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")

    return modifications, ville


def main():
    pattern = os.path.join(ELECTIONS_DIR, "*.json")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"Aucun fichier trouvé dans {ELECTIONS_DIR}")
        sys.exit(1)

    print(f"Scan de {len(files)} fichiers dans {ELECTIONS_DIR}\n")

    total_blocs = 0
    total_mesures = 0
    total_fichiers_modifies = 0

    for filepath in files:
        modifications, ville = process_file(filepath)
        if modifications:
            total_fichiers_modifies += 1
            for nom, cat_id, st_id, nb_blocs, nb_mesures in modifications:
                print(
                    f"  {ville} - {nom} [{cat_id}/{st_id}]: "
                    f"{nb_blocs} bloc → {nb_mesures} mesures"
                )
                total_blocs += nb_blocs
                total_mesures += nb_mesures

    print(f"\n{'='*60}")
    print(f"Résumé :")
    print(f"  Fichiers scannés     : {len(files)}")
    print(f"  Fichiers modifiés    : {total_fichiers_modifies}")
    print(f"  Blocs re-découpés    : {total_blocs}")
    print(f"  Mesures produites    : {total_mesures}")
    if total_blocs > 0:
        print(f"  Ratio moyen          : 1 bloc → {total_mesures / total_blocs:.1f} mesures")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
