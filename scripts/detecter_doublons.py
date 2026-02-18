#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Détecteur de doublons dans les propositions électorales
Scanne tous les fichiers data/elections/*.json
"""

import json
import os
import sys
import io
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

# Force UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def similarity_ratio(text1, text2):
    """Calcule le ratio de similarité entre deux textes (0-1)"""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def normaliser_texte(texte):
    """Normalise le texte pour comparaison"""
    return ' '.join(texte.lower().split())

def main():
    # Chemin vers les données
    base_dir = Path(r"C:\Users\KOPELMANRon\Downloads\FR comp mun")
    elections_dir = base_dir / "data" / "elections"

    if not elections_dir.exists():
        print(f"❌ Dossier introuvable: {elections_dir}")
        return

    # Compteurs
    doublons_exacts = []
    doublons_similaires = []
    textes_courts = []
    doublons_entre_candidats = []

    # Dict pour stocker tous les textes par ville
    textes_par_ville = defaultdict(lambda: defaultdict(list))

    print("=" * 80)
    print("DÉTECTION DE DOUBLONS DANS LES PROPOSITIONS")
    print("=" * 80)
    print()

    # Parcourir tous les fichiers JSON
    fichiers_json = sorted(elections_dir.glob("*.json"))
    print(f"📁 Fichiers à scanner: {len(fichiers_json)}\n")

    for fichier in fichiers_json:
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                data = json.load(f)

            ville_nom = data.get('nom', fichier.stem)
            candidats = data.get('candidats', [])

            if not candidats:
                continue

            print(f"🔍 Analyse: {ville_nom} ({len(candidats)} candidats)")

            for candidat in candidats:
                nom_candidat = candidat.get('nom', 'Inconnu')
                propositions = candidat.get('propositions', {})

                # Collecter tous les textes de ce candidat
                textes_candidat = {}  # {sous_theme: texte}

                for categorie, sous_themes in propositions.items():
                    if isinstance(sous_themes, dict):
                        for sous_theme, texte in sous_themes.items():
                            if texte and isinstance(texte, str):
                                textes_candidat[f"{categorie}/{sous_theme}"] = texte

                                # Vérifier longueur
                                if len(texte.strip()) < 20:
                                    textes_courts.append({
                                        'ville': ville_nom,
                                        'candidat': nom_candidat,
                                        'sous_theme': f"{categorie}/{sous_theme}",
                                        'texte': texte,
                                        'longueur': len(texte.strip())
                                    })

                                # Stocker pour comparaison entre candidats
                                textes_par_ville[ville_nom][normaliser_texte(texte)].append({
                                    'candidat': nom_candidat,
                                    'sous_theme': f"{categorie}/{sous_theme}",
                                    'texte_original': texte
                                })

                # Détecter doublons pour ce candidat
                textes_vus = {}  # {texte_normalisé: [(sous_theme, texte_original)]}

                for sous_theme, texte in textes_candidat.items():
                    texte_norm = normaliser_texte(texte)

                    # Doublons exacts
                    if texte_norm in textes_vus:
                        doublons_exacts.append({
                            'ville': ville_nom,
                            'candidat': nom_candidat,
                            'sous_themes': [sous_theme] + [st for st, _ in textes_vus[texte_norm]],
                            'texte': texte
                        })
                    else:
                        textes_vus[texte_norm] = [(sous_theme, texte)]

                    # Doublons similaires (comparer avec tous les textes précédents)
                    for autre_texte_norm, occurrences in textes_vus.items():
                        if autre_texte_norm != texte_norm:
                            ratio = similarity_ratio(texte_norm, autre_texte_norm)
                            if ratio > 0.8:  # Plus de 80% similaire
                                doublons_similaires.append({
                                    'ville': ville_nom,
                                    'candidat': nom_candidat,
                                    'sous_theme1': sous_theme,
                                    'texte1': texte,
                                    'sous_theme2': occurrences[0][0],
                                    'texte2': occurrences[0][1],
                                    'similarite': f"{ratio*100:.1f}%"
                                })

        except Exception as e:
            print(f"⚠️  Erreur lecture {fichier.name}: {e}")

    print("\n" + "=" * 80)

    # Détecter doublons entre candidats
    for ville, textes_dict in textes_par_ville.items():
        for texte_norm, occurrences in textes_dict.items():
            if len(occurrences) > 1:
                # Vérifier si ce sont des candidats différents
                candidats_uniques = set(occ['candidat'] for occ in occurrences)
                if len(candidats_uniques) > 1:
                    doublons_entre_candidats.append({
                        'ville': ville,
                        'texte': occurrences[0]['texte_original'],
                        'occurrences': occurrences
                    })

    # AFFICHAGE DES RÉSULTATS
    print("\n" + "=" * 80)
    print("RÉSULTATS")
    print("=" * 80)
    print()

    # 1. DOUBLONS EXACTS
    if doublons_exacts:
        print(f"❌ DOUBLONS EXACTS: {len(doublons_exacts)} trouvés\n")
        for doublon in doublons_exacts:
            print(f"  📍 {doublon['ville']} - {doublon['candidat']}")
            print(f"     Texte: \"{doublon['texte'][:100]}...\"")
            print(f"     Présent dans {len(doublon['sous_themes'])} sous-thèmes:")
            for st in doublon['sous_themes']:
                print(f"       • {st}")
            print()
    else:
        print("✅ Aucun doublon exact détecté\n")

    # 2. DOUBLONS SIMILAIRES
    if doublons_similaires:
        print(f"⚠️  DOUBLONS SIMILAIRES (>80%): {len(doublons_similaires)} trouvés\n")
        for doublon in doublons_similaires:
            print(f"  📍 {doublon['ville']} - {doublon['candidat']}")
            print(f"     Similarité: {doublon['similarite']}")
            print(f"     Sous-thème 1: {doublon['sous_theme1']}")
            print(f"       → \"{doublon['texte1'][:80]}...\"")
            print(f"     Sous-thème 2: {doublon['sous_theme2']}")
            print(f"       → \"{doublon['texte2'][:80]}...\"")
            print()
    else:
        print("✅ Aucun doublon similaire détecté\n")

    # 3. TEXTES COURTS
    if textes_courts:
        print(f"⚠️  TEXTES TROP COURTS (<20 car.): {len(textes_courts)} trouvés\n")
        for court in textes_courts:
            print(f"  📍 {court['ville']} - {court['candidat']}")
            print(f"     {court['sous_theme']}: \"{court['texte']}\" ({court['longueur']} car.)")
            print()
    else:
        print("✅ Aucun texte trop court détecté\n")

    # 4. DOUBLONS ENTRE CANDIDATS
    if doublons_entre_candidats:
        print(f"🚨 DOUBLONS ENTRE CANDIDATS: {len(doublons_entre_candidats)} trouvés\n")
        for doublon in doublons_entre_candidats:
            print(f"  📍 {doublon['ville']}")
            print(f"     Texte: \"{doublon['texte'][:100]}...\"")
            print(f"     Présent chez {len(doublon['occurrences'])} candidats:")
            for occ in doublon['occurrences']:
                print(f"       • {occ['candidat']} ({occ['sous_theme']})")
            print()
    else:
        print("✅ Aucun doublon entre candidats détecté\n")

    # RÉSUMÉ FINAL
    print("=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    print(f"  Doublons exacts (même candidat):        {len(doublons_exacts)}")
    print(f"  Doublons similaires (même candidat):    {len(doublons_similaires)}")
    print(f"  Textes trop courts (<20 car.):          {len(textes_courts)}")
    print(f"  Doublons entre candidats différents:    {len(doublons_entre_candidats)}")
    print("=" * 80)

    total_problemes = (len(doublons_exacts) + len(doublons_similaires) +
                       len(textes_courts) + len(doublons_entre_candidats))

    if total_problemes == 0:
        print("\n✅ Aucun problème détecté!")
    else:
        print(f"\n⚠️  Total de problèmes détectés: {total_problemes}")

if __name__ == "__main__":
    main()
