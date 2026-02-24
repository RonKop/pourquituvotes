#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration texte → mesures[]
============================
Transforme chaque proposition { texte: "..." } en { mesures: ["...", "..."] }
dans tous les fichiers data/elections/*.json.

Split best-effort : sépare sur `. ` suivi d'une majuscule.
Seuil minimum 15 caractères par mesure. Fallback : garder le bloc entier.
"""

import io
import json
import os
import re
import sys

# Forcer UTF-8 sur Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ELECTIONS_DIR = os.path.join(ROOT_DIR, "data", "elections")

# Pattern : `. ` suivi d'une majuscule (y compris accentuées)
SPLIT_RE = re.compile(r'\.\s+(?=[A-ZÉÈÊÀÂÔÙÇÎÏÜ])')

SEUIL_MIN = 15  # Caractères minimum par mesure


def split_texte(texte):
    """Découpe un bloc de texte en mesures individuelles."""
    if not texte or not texte.strip():
        return []

    # Essayer le split
    parts = SPLIT_RE.split(texte.strip())

    # Nettoyer : ajouter le point final si manquant, strip
    mesures = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if not p.endswith(".") and not p.endswith("!") and not p.endswith(")"):
            p += "."
        mesures.append(p)

    # Si toutes les mesures sont trop courtes après split, fallback
    if len(mesures) > 1:
        # Vérifier que chaque mesure fait au moins SEUIL_MIN caractères
        toutes_ok = all(len(m) >= SEUIL_MIN for m in mesures)
        if not toutes_ok:
            # Re-fusionner les mesures trop courtes avec la précédente
            merged = []
            for m in mesures:
                if merged and len(m) < SEUIL_MIN:
                    merged[-1] = merged[-1].rstrip(".") + ". " + m
                else:
                    merged.append(m)
            mesures = merged

    # Fallback : si le split n'a rien produit, garder le bloc entier
    if not mesures:
        mesures = [texte.strip()]

    return mesures


def migrer_fichier(filepath):
    """Migre un fichier JSON de texte vers mesures[]."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    nb_migrees = 0
    nb_deja = 0
    nb_null = 0

    for cat in data.get("categories", []):
        for st in cat.get("sousThemes", []):
            for cid, prop in st.get("propositions", {}).items():
                if prop is None:
                    nb_null += 1
                    continue

                # Déjà migré ?
                if "mesures" in prop:
                    nb_deja += 1
                    continue

                # Migration
                texte = prop.get("texte", "")
                mesures = split_texte(texte)

                # Remplacer texte par mesures
                prop["mesures"] = mesures
                if "texte" in prop:
                    del prop["texte"]

                nb_migrees += 1

    # Écrire le fichier modifié
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return nb_migrees, nb_deja, nb_null


def main():
    print("=" * 60)
    print("  MIGRATION texte → mesures[]")
    print("=" * 60)
    print()

    if not os.path.isdir(ELECTIONS_DIR):
        print(f"ERREUR : {ELECTIONS_DIR} introuvable !")
        return 1

    fichiers = sorted(f for f in os.listdir(ELECTIONS_DIR) if f.endswith(".json"))
    print(f"  {len(fichiers)} fichiers JSON trouvés")
    print()

    total_migrees = 0
    total_deja = 0
    total_null = 0

    for f in fichiers:
        filepath = os.path.join(ELECTIONS_DIR, f)
        nb_migrees, nb_deja, nb_null = migrer_fichier(filepath)
        total_migrees += nb_migrees
        total_deja += nb_deja
        total_null += nb_null
        if nb_migrees > 0:
            print(f"  {f}: {nb_migrees} propositions migrées")
        elif nb_deja > 0:
            print(f"  {f}: déjà migré ({nb_deja} mesures)")

    print()
    print("=" * 60)
    print(f"  RÉSULTAT : {total_migrees} propositions migrées")
    print(f"  ({total_deja} déjà migrées, {total_null} null)")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
