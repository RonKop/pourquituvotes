#!/usr/bin/env python3
"""
Ajoute 2 propositions pour Martine Vassal (id: vassal) dans marseille-2026.json.
- pietons-circulation
- vie-associative
Ne modifie que les sous-thèmes où vassal est actuellement null.
Ne touche à aucun autre candidat ni à programmeComplet.
"""

import json
import os

FICHIER = os.path.join(os.path.dirname(__file__), "..", "data", "elections", "marseille-2026.json")

NOUVELLES_PROPOSITIONS = {
    "pietons-circulation": {
        "texte": "Encadrement strict des trottinettes : verbalisation hors pistes dédiées, sur trottoirs et sans casque",
        "source": "Programme 13 axes prioritaires 2026",
        "sourceUrl": "https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/"
    },
    "vie-associative": {
        "texte": "Revitalisation de Marseille Espérance. Suppression des subventions aux associations jugées ambiguës, dont SOS Méditerranée",
        "source": "Programme 13 axes prioritaires 2026",
        "sourceUrl": "https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/"
    }
}


def main():
    # Charger le JSON
    with open(FICHIER, "r", encoding="utf-8") as f:
        data = json.load(f)

    modifs = 0

    for categorie in data["categories"]:
        for sous_theme in categorie["sousThemes"]:
            st_id = sous_theme["id"]
            if st_id in NOUVELLES_PROPOSITIONS:
                props = sous_theme["propositions"]
                if props.get("vassal") is None:
                    props["vassal"] = NOUVELLES_PROPOSITIONS[st_id]
                    modifs += 1
                    print(f"  [OK] {st_id} : proposition ajoutée pour vassal")
                else:
                    print(f"  [SKIP] {st_id} : vassal a déjà une proposition, on ne touche pas")

    if modifs == 0:
        print("\nAucune modification effectuée.")
        return

    # Sauvegarder
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n{modifs} proposition(s) ajoutée(s). Fichier sauvegardé.")


if __name__ == "__main__":
    main()
