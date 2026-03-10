#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEMPLATE — Ré-extraction de [NOM CANDIDAT] ([VILLE])

Source   : [Titre du document / page web]
URL      : [URL exacte]
Date     : [Date d'accès]
Mesures source : [X mesures identifiées dans la source]
Mesures extraites : [Y mesures mappées ci-dessous]

Utilisation :
  1. Copier ce fichier → scripts/reextraire_{candidat_id}_{ville_id}.py
  2. Remplir CANDIDAT_ID, VILLE_ID, SOURCE, SOURCE_URL
  3. Remplir MESURES avec les propositions exactes (pas de paraphrase)
  4. Exécuter : python scripts/reextraire_{candidat_id}_{ville_id}.py
  5. Valider : python scripts/valider_donnees.py
  6. Auditer : python scripts/auditer_completude.py --candidat {candidat_id}
"""

import io
import json
import os
import sys

# Force UTF-8 pour Windows (cp1252 fix)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# === CONFIGURATION (à remplir) ===
CANDIDAT_ID = "TODO"          # ex: "gregoire"
VILLE_ID = "TODO"             # ex: "paris-2026"
SOURCE = "TODO"               # ex: "Programme officiel 2026 — Emmanuel Grégoire"
SOURCE_URL = "TODO"           # ex: "https://example.com/programme"

JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", f"{VILLE_ID}.json")

# === MESURES (à remplir) ===
# Clé = ID du sous-thème (cf. data/schema/schema_elections.json)
# Valeur = liste de mesures exactes (texte fidèle à la source, pas de paraphrase)
#
# Les 44 sous-thèmes communs :
#   securite      : police-municipale, videoprotection, prevention-mediation, violences-femmes
#   transports    : transports-en-commun, velo-mobilites-douces, pietons-circulation, stationnement, tarifs-gratuite
#   logement      : logement-social, logements-vacants, encadrement-loyers, acces-logement
#   education     : petite-enfance, ecoles-renovation, cantines-fournitures, periscolaire-loisirs, jeunesse
#   environnement : espaces-verts, proprete-dechets, climat-adaptation, renovation-energetique, alimentation-durable
#   sante         : centres-sante, prevention-sante, seniors
#   democratie    : budget-participatif, transparence, vie-associative, services-publics
#   economie      : commerce-local, emploi-insertion, attractivite
#   culture       : equipements-culturels, evenements-creation
#   sport         : equipements-sportifs, sport-pour-tous
#   urbanisme     : amenagement-urbain, accessibilite, quartiers-prioritaires
#   solidarite    : aide-sociale, egalite-discriminations, pouvoir-achat

MESURES = {
    # "police-municipale": [
    #     "Mesure exacte 1.",
    #     "Mesure exacte 2.",
    # ],
}


def main():
    print("=" * 60)
    print(f"  RE-EXTRACTION {CANDIDAT_ID.upper()} ({VILLE_ID})")
    print("=" * 60)

    # Vérifier la configuration
    if "TODO" in (CANDIDAT_ID, VILLE_ID, SOURCE, SOURCE_URL):
        print("\n  ERREUR : remplir CANDIDAT_ID, VILLE_ID, SOURCE, SOURCE_URL")
        sys.exit(1)

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
