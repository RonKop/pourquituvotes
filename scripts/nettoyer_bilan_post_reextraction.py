#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nettoyage ciblé des items bilan réintroduits par les scripts de ré-extraction.
Supprime les mesures qui sont clairement du bilan (statistiques passées, "déjà en place", etc.)
et non des propositions pour le mandat 2026-2032.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# Mesures à supprimer, identifiées par (ville, candidat_id, sous_theme_id, texte_exact)
BILAN_A_SUPPRIMER = [
    # ── MOUDENC (Toulouse) ──
    ("toulouse", "moudenc", "police-municipale",
     "Augmentation des effectifs de la police municipale de 165 à 390 agents depuis 2014, soit +136%."),
    ("toulouse", "moudenc", "videoprotection",
     "Passage de 21 caméras en 2014 à 710 caméras fin 2025."),
    ("toulouse", "moudenc", "videoprotection",
     "Utilisation de la vidéoprotection pour la détection de détresse : 500 situations détectées, 144 interventions."),
    ("toulouse", "moudenc", "videoprotection",
     "7 238 réquisitions judiciaires en 2025 ayant conduit à 1 038 interpellations."),
    ("toulouse", "moudenc", "prevention-mediation",
     "Triplement du budget sécurité : de 16,4 M€ à 42 M€ entre 2014 et 2026."),
    ("toulouse", "moudenc", "transports-en-commun",
     "Record de fréquentation du réseau de transports en commun atteint."),
    ("toulouse", "moudenc", "transports-en-commun",
     "Budget mobilité le plus élevé de France hors Paris."),
    ("toulouse", "moudenc", "logement-social",
     "Production de 10 147 logements sociaux entre 2014 et 2024."),
    ("toulouse", "moudenc", "logement-social",
     "Facilitation de 2 658 accessions sociales à la propriété depuis 2014."),
    ("toulouse", "moudenc", "cantines-fournitures",
     "Gel des tarifs de cantine scolaire et périscolaire depuis 2015."),

    # ── DELAFOSSE (Montpellier) ──
    ("montpellier", "delafosse", "tarifs-gratuite",
     "Gratuité des transports en commun déjà en place et défendue comme acquis social."),
    ("montpellier", "delafosse", "cantines-fournitures",
     "76% de produits durables et 37% bio dans les cantines scolaires, soit un doublement depuis 2020."),
    ("montpellier", "delafosse", "budget-participatif",
     "Mutuelle communale de santé déjà en place et maintenue."),
]


def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("  NETTOYAGE BILAN POST-RÉ-EXTRACTION")
    if dry_run:
        print("  (MODE DRY-RUN — aucune modification)")
    print("=" * 60)

    # Grouper par fichier
    fichiers = {}
    for ville, cid, st_id, texte in BILAN_A_SUPPRIMER:
        path = os.path.join(ROOT_DIR, "data", "elections", f"{ville}-2026.json")
        if path not in fichiers:
            fichiers[path] = []
        fichiers[path].append((cid, st_id, texte))

    total_removed = 0

    for path, items in fichiers.items():
        ville = os.path.basename(path).replace("-2026.json", "")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        removed_in_file = 0
        for cid, st_id, texte in items:
            for cat in data["categories"]:
                for st in cat["sousThemes"]:
                    if st["id"] != st_id:
                        continue
                    prop = st["propositions"].get(cid)
                    if prop is None or "mesures" not in prop:
                        continue
                    if texte in prop["mesures"]:
                        prop["mesures"].remove(texte)
                        removed_in_file += 1
                        print(f"  ✓ {ville}/{cid} [{st_id}]: supprimé")
                    else:
                        print(f"  ✗ {ville}/{cid} [{st_id}]: non trouvé")

        if removed_in_file > 0 and not dry_run:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")

        total_removed += removed_in_file
        print(f"  → {ville}: {removed_in_file} mesures bilan supprimées\n")

    print(f"  Total: {total_removed} mesures bilan supprimées")
    print("=" * 60)


if __name__ == "__main__":
    main()
