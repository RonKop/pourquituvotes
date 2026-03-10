#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de dossiers de presse par ville — #POURQUITUVOTES
==============================================================
Génère un fichier Markdown par ville avec stats clés, tableaux
comparatifs et questions prêtes à publier pour les rédactions locales.

Pré-requis : lancer d'abord scripts/calculer_metriques.py

Usage :
  python scripts/generer_dossier_presse.py                    # Toutes les villes
  python scripts/generer_dossier_presse.py --ville paris      # Une ville
"""

import argparse
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
METRIQUES_JSON = os.path.join(DATA_DIR, "metriques.json")
OUTPUT_DIR = os.path.join(DATA_DIR, "dossiers_presse")


def charger_metriques():
    if not os.path.exists(METRIQUES_JSON):
        print(f"ERREUR : {METRIQUES_JSON} introuvable. Lancez d'abord :")
        print("  python scripts/calculer_metriques.py")
        sys.exit(1)
    with open(METRIQUES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def slug_ville(ville_id):
    """Extrait le slug sans le suffixe -2026."""
    return ville_id.replace("-2026", "")


def generer_dossier(ville_data, national):
    """Génère le contenu Markdown pour une ville."""
    nom = ville_data["nom"]
    slug = slug_ville(ville_data["id"])
    candidats = ville_data["candidats"]
    total = ville_data["total_mesures"]

    # Filtrer candidats avec mesures
    candidats_actifs = [
        c for c in candidats if c["metriques"]["total_mesures"] > 0
    ]
    candidats_actifs.sort(key=lambda c: -c["metriques"]["total_mesures"])

    lignes = []
    lignes.append(f"# Municipales 2026 à {nom} — Les chiffres clés")
    lignes.append("")
    lignes.append(f"*Données #POURQUITUVOTES — pourquituvotes.fr*")
    lignes.append("")

    # Résumé
    lignes.append("## En bref")
    lignes.append("")
    lignes.append(f"- **{ville_data['nb_candidats']}** candidats déclarés")
    lignes.append(f"- **{ville_data['nb_complets']}** programmes complets analysés")
    lignes.append(f"- **{total}** propositions concrètes recensées")

    if ville_data.get("candidat_plus_detaille"):
        cpd = ville_data["candidat_plus_detaille"]
        lignes.append(
            f"- Programme le plus détaillé : **{cpd['nom']}** ({cpd['total_mesures']} mesures)"
        )

    if ville_data.get("theme_plus_couvert"):
        tpc = ville_data["theme_plus_couvert"]
        lignes.append(
            f"- Thème le plus abordé : **{tpc['nom']}** ({tpc['total_mesures']} mesures)"
        )

    lignes.append("")

    # Tableau comparatif
    if candidats_actifs:
        lignes.append("## Tableau comparatif des candidats")
        lignes.append("")
        lignes.append(
            "| Candidat | Liste | Mesures | Couverture | % Chiffré | % Échéance | Long. moy. |"
        )
        lignes.append(
            "|----------|-------|--------:|-----------:|----------:|-----------:|-----------:|"
        )
        for c in candidats_actifs:
            m = c["metriques"]
            couv = f"{m['couverture_sous_themes']}/{m['couverture_sous_themes_max']}"
            lignes.append(
                f"| {c['nom']} | {c['liste'][:30]} | {m['total_mesures']} | {couv} | {m['pct_mesures_chiffrees']}% | {m['pct_mesures_avec_echeance']}% | {m['longueur_moyenne_mesure']} car. |"
            )
        lignes.append("")

    # Top 3 thèmes par candidat
    if candidats_actifs:
        lignes.append("## Priorités thématiques par candidat")
        lignes.append("")
        for c in candidats_actifs:
            top3 = c["metriques"].get("top3_themes", [])
            if top3:
                themes_str = ", ".join(
                    f"{t['nom']} ({t['nb_mesures']})" for t in top3
                )
                lignes.append(f"- **{c['nom']}** : {themes_str}")
        lignes.append("")

    # Questions prêtes à publier
    lignes.append("## Questions prêtes à publier")
    lignes.append("")

    if ville_data.get("theme_plus_couvert"):
        tpc = ville_data["theme_plus_couvert"]
        lignes.append(
            f'- "À {nom}, **{tpc["nom"].lower()}** est le sujet qui génère le plus de propositions '
            f'({tpc["total_mesures"]} mesures au total)."'
        )

    if len(candidats_actifs) >= 2:
        c1 = candidats_actifs[0]
        c2 = candidats_actifs[-1]
        lignes.append(
            f'- "**{c1["nom"]}** propose {c1["metriques"]["total_mesures"]} mesures '
            f'contre {c2["metriques"]["total_mesures"]} pour **{c2["nom"]}** : '
            f'un écart de densité programmatique significatif."'
        )

    # Candidat le plus chiffré
    plus_chiffre = max(
        candidats_actifs,
        key=lambda c: c["metriques"]["pct_mesures_chiffrees"],
        default=None,
    )
    if plus_chiffre and plus_chiffre["metriques"]["pct_mesures_chiffrees"] > 0:
        lignes.append(
            f'- "Le programme le plus chiffré est celui de **{plus_chiffre["nom"]}** '
            f'({plus_chiffre["metriques"]["pct_mesures_chiffrees"]}% de mesures contenant un chiffre)."'
        )

    if ville_data.get("theme_plus_clivant") and ville_data["theme_plus_clivant"].get("nom"):
        tc = ville_data["theme_plus_clivant"]
        lignes.append(
            f'- "Le thème le plus clivant entre candidats est **{tc["nom"].lower()}** '
            f'(écart de {tc["ecart"]} points de couverture)."'
        )

    lignes.append("")

    # Contexte national
    lignes.append("## Contexte national")
    lignes.append("")
    lignes.append(
        f"Au niveau national, #POURQUITUVOTES a analysé **{national['total_mesures']}** "
        f"propositions de **{national['total_candidats']}** candidats dans **{national['total_villes']}** villes."
    )
    if national.get("themes_ranking"):
        top_nat = national["themes_ranking"][0]
        lignes.append(
            f"Le thème le plus abordé dans toute la France est **{top_nat['nom'].lower()}** "
            f"({top_nat['total_mesures']} mesures)."
        )
    lignes.append("")

    # Lien
    lignes.append("## Consulter le comparateur")
    lignes.append("")
    lignes.append(
        f"Comparez les programmes en détail : https://pourquituvotes.fr/municipales-2026/{slug}/"
    )
    lignes.append("")
    lignes.append("---")
    lignes.append(
        "*Données collectées et structurées par #POURQUITUVOTES — projet citoyen indépendant.*"
    )
    lignes.append(f"*Contact presse : contact@pourquituvotes.fr*")
    lignes.append("")

    return "\n".join(lignes)


def main():
    parser = argparse.ArgumentParser(
        description="Génère des dossiers de presse Markdown par ville"
    )
    parser.add_argument("--ville", help="Filtrer par nom ou slug de ville (partiel)")
    args = parser.parse_args()

    metriques = charger_metriques()
    national = metriques["national"]
    villes = metriques["villes"]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    nb_generes = 0
    for ville in villes:
        slug = slug_ville(ville["id"])
        nom = ville["nom"]

        if args.ville:
            filtre = args.ville.lower()
            if filtre not in nom.lower() and filtre not in slug.lower():
                continue

        # Ne générer que pour les villes avec des mesures
        if ville["total_mesures"] == 0:
            continue

        contenu = generer_dossier(ville, national)
        output_path = os.path.join(OUTPUT_DIR, f"{slug}.md")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(contenu)

        nb_generes += 1

    print(f"{nb_generes} dossier(s) de presse générés dans {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
