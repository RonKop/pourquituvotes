#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intègre le programme de Mohed Altrad (Montpellier) dans le comparateur municipal.

Sources :
- Programme officiel : https://altrad2026.fr/
- InfocOccitanie : https://infoccitanie.fr/montpellier-les-premieres-propositions-du-candidat-mohed-altrad/
- France Bleu Hérault : https://www.francebleu.fr/infos/politique/municipales-2026-cette-ville-a-besoin-qu-on-la-releve-mohed-altrad-retente-sa-chance-a-montpellier-1699900
- InfocOccitanie (mobilités) : https://infoccitanie.fr/montpellier-a-50c-les-candidats-confrontent-leur-vision-sur-les-mobilites/
- montpellier-municipales.fr : https://montpellier-municipales.fr/en/listes/mohed-altrad/

8 thèmes sur le site : Sécurité, Logement & urbanisme, Économie & emploi,
Pouvoir d'achat, Mobilités & déplacements, Écologie & cadre de vie,
Culture & vie associative, Éducation & jeunesse (= Services publics).
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")
ELECTIONS_DIR = os.path.join(ROOT_DIR, "data", "elections")
JSON_PATH = os.path.join(ELECTIONS_DIR, "montpellier-2026.json")

# Propositions à intégrer pour Altrad
# Clé = sous-thème ID, valeur = dict {texte, source, sourceUrl}
# On ne touche PAS aux propositions déjà présentes (pas de doublons).
NOUVELLES_PROPOSITIONS = {
    # === TRANSPORTS ===
    "tarifs-gratuite": {
        "texte": "Maintenir la gratuité des transports en commun, considérée comme un acquis social à préserver",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://altrad2026.fr/"
    },
    # === LOGEMENT ===
    "acces-logement": {
        "texte": "Permettre aux locataires en HLM depuis 15 ans d'accéder à la propriété de leur logement, le logement social devant être un tremplin et non un enfermement",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://altrad2026.fr/"
    },
    # === ENVIRONNEMENT ===
    "espaces-verts": {
        "texte": "Lancer un plan de végétalisation massive de la ville pour créer des îlots de fraîcheur et améliorer le cadre de vie",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://altrad2026.fr/"
    },
    "climat-adaptation": {
        "texte": "Abandonner définitivement le projet de chaudière CSR (combustibles solides de récupération) : « La santé des Montpelliérains n'est pas négociable »",
        "source": "France Bleu Hérault, 2026",
        "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-2026-cette-ville-a-besoin-qu-on-la-releve-mohed-altrad-retente-sa-chance-a-montpellier-1699900"
    },
    # === ÉCONOMIE ===
    "commerce-local": {
        "texte": "Mettre en place un plan d'urgence pour le commerce de centre-ville avec un dialogue exigeant et permanent entre la mairie et les commerçants",
        "source": "InfocOccitanie, 2026",
        "sourceUrl": "https://infoccitanie.fr/montpellier-a-50c-les-candidats-confrontent-leur-vision-sur-les-mobilites/"
    },
    "attractivite": {
        "texte": "Faire de Montpellier une ville « zéro chômage » en attirant des entreprises et en développant l'économie locale",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://altrad2026.fr/"
    },
    # === SOLIDARITÉ ===
    "pouvoir-achat": {
        "texte": "Zéro hausse d'impôts locaux pendant tout le mandat, maintien de la gratuité des transports et de la cantine scolaire gratuite pour tous",
        "source": "France Bleu Hérault, 2026",
        "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-2026-cette-ville-a-besoin-qu-on-la-releve-mohed-altrad-retente-sa-chance-a-montpellier-1699900"
    },
}

# Propositions existantes à ENRICHIR (réécriture plus complète)
PROPOSITIONS_A_ENRICHIR = {
    "transports-en-commun": {
        "texte": "Maintenir la gratuité totale des transports en commun, renforcer la fréquence et la sécurité des bus, créer un véritable réseau de bus desservant tous les quartiers et faire du TER la colonne vertébrale du grand territoire",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://altrad2026.fr/"
    },
    "emploi-insertion": {
        "texte": "Créer 30 000 emplois et 10 000 contrats d'apprentissage en 5 ans pour atteindre l'objectif zéro chômage, en s'appuyant sur le tissu économique local",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://altrad2026.fr/"
    },
    "proprete-dechets": {
        "texte": "Abandonner le projet de chaudière CSR, créer une brigade municipale de propreté et lancer un plan de végétalisation massive de la ville",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://altrad2026.fr/"
    },
}


def main():
    # Charger le JSON
    if not os.path.exists(JSON_PATH):
        print(f"ERREUR : fichier introuvable : {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    candidat_id = "altrad"

    # Vérifier que le candidat existe
    candidat_trouve = False
    for c in data["candidats"]:
        if c["id"] == candidat_id:
            candidat_trouve = True
            break

    if not candidat_trouve:
        print(f"ERREUR : candidat '{candidat_id}' introuvable dans le JSON")
        sys.exit(1)

    # Compter les propositions avant
    nb_avant = 0
    nb_ajoutees = 0
    nb_enrichies = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if candidat_id in st["propositions"] and st["propositions"][candidat_id] is not None:
                nb_avant += 1

    print(f"Propositions Altrad avant intégration : {nb_avant}")

    # 1. Ajouter les NOUVELLES propositions (seulement si null)
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in NOUVELLES_PROPOSITIONS:
                current = st["propositions"].get(candidat_id)
                if current is None:
                    st["propositions"][candidat_id] = NOUVELLES_PROPOSITIONS[st_id]
                    nb_ajoutees += 1
                    print(f"  + AJOUT : {st_id} -> {NOUVELLES_PROPOSITIONS[st_id]['texte'][:60]}...")
                else:
                    print(f"  ~ EXISTANT (non écrasé) : {st_id}")

    # 2. Enrichir les propositions existantes (réécriture)
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in PROPOSITIONS_A_ENRICHIR:
                current = st["propositions"].get(candidat_id)
                if current is not None:
                    ancien_texte = current["texte"]
                    nouveau = PROPOSITIONS_A_ENRICHIR[st_id]
                    if len(nouveau["texte"]) > len(ancien_texte):
                        st["propositions"][candidat_id] = nouveau
                        nb_enrichies += 1
                        print(f"  * ENRICHI : {st_id} ({len(ancien_texte)} -> {len(nouveau['texte'])} car.)")
                    else:
                        print(f"  ~ PAS ENRICHI (déjà plus long) : {st_id}")
                else:
                    # Le sous-thème n'avait pas de proposition, on l'ajoute
                    st["propositions"][candidat_id] = PROPOSITIONS_A_ENRICHIR[st_id]
                    nb_ajoutees += 1
                    print(f"  + AJOUT (via enrichir) : {st_id}")

    # 3. Mettre à jour programmeComplet
    nb_apres = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if candidat_id in st["propositions"] and st["propositions"][candidat_id] is not None:
                nb_apres += 1

    programme_complet = nb_apres >= 15
    for c in data["candidats"]:
        if c["id"] == candidat_id:
            ancien_status = c["programmeComplet"]
            c["programmeComplet"] = programme_complet
            if ancien_status != programme_complet:
                print(f"\n  programmeComplet : {ancien_status} -> {programme_complet}")
            break

    # Écrire le JSON
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nRésultat :")
    print(f"  Propositions avant : {nb_avant}")
    print(f"  Ajoutées : {nb_ajoutees}")
    print(f"  Enrichies : {nb_enrichies}")
    print(f"  Total après : {nb_apres}")
    print(f"  programmeComplet : {programme_complet}")
    print(f"\nFichier mis à jour : {JSON_PATH}")


if __name__ == "__main__":
    main()
