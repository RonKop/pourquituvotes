#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction batch 3 : Delafosse (Montpellier), Oziol (Montpellier).
Sources : echo-des-tribunes.com, michaeldelafosse.fr, infoccitanie.fr.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


# ============================================================
# DELAFOSSE (Montpellier) — presse locale + site officiel
# ============================================================

MESURES_DELAFOSSE = {
    "police-municipale": [
        "Recrutement de 100 agents de sécurité supplémentaires (police municipale et métropole), soit 4 millions d'euros annuels.",
        "Maintien de l'armement de la police municipale.",
        "Demande de renforts de police nationale, gendarmerie et magistrats auprès de l'État.",
        "Restructuration des espaces publics dans les quartiers sensibles (Mosson, Montasinos, place Rosa-Parks) pour éliminer les zones de non-droit.",
    ],
    "videoprotection": [
        "Doublement du nombre de caméras de vidéosurveillance : passage de 500 à 1 000 unités, investissement de 3 millions d'euros.",
    ],
    "prevention-mediation": [
        "Extension du nombre de médiateurs de quartier de 12 à 30 agents.",
        "Passage de 100 à 4 000 heures de travaux d'intérêt général pour les mineurs délinquants.",
        "Campagnes de prévention ambitieuses contre les addictions, notamment la cocaïne.",
        "Lutte continue contre le narcotrafic.",
    ],
    "transports-en-commun": [
        "Maintien de la gratuité des transports en commun sur la métropole.",
    ],
    "tarifs-gratuite": [
        "Gratuité des transports en commun déjà en place et défendue comme acquis social.",
    ],
    "logement-social": [
        "Construction de 4 000 logements neufs en priorité par recyclage urbain plutôt que sur les terres agricoles.",
        "Création de 1 000 logements étudiants subventionnés répartis dans plusieurs quartiers (Ovalie, Mosson, Pompignane).",
        "Création de 500 logements adaptés pour les seniors dans quatre résidences sénior.",
    ],
    "logements-vacants": [
        "Création d'une Agence municipale du logement pour capter les logements vacants privés et sécuriser les propriétaires contre les impayés.",
    ],
    "encadrement-loyers": [
        "Maintien de l'encadrement des loyers pour lutter contre la spéculation.",
        "Renforcement de la lutte contre les locations touristiques type Airbnb pour préserver le parc résidentiel.",
        "Ciblage des logements indignes et lutte contre les marchands de sommeil.",
    ],
    "acces-logement": [
        "Création du « Pass Accession Montpelliérain » : prêt municipal à taux zéro de 10 000 € pour aider les jeunes à constituer un apport.",
        "Prise en charge des frais de notaire pour les primo-accédants de 18-30 ans sous conditions de revenus.",
        "Programme « Housing First » avec 7 nouvelles pensions familiales et baux glissants pour la transition vers le logement pérenne.",
    ],
    "petite-enfance": [
        "Installation de tables à langer dans les parcs publics pour les familles.",
    ],
    "cantines-fournitures": [
        "76% de produits durables et 37% bio dans les cantines scolaires, soit un doublement depuis 2020.",
        "Deux menus végétariens par semaine dans toutes les écoles et alternative végétarienne quotidienne.",
        "Programme « Ma cantine autrement » dans six écoles pilotes pour une restauration plus durable et inclusive.",
        "Interdiction des produits Mercosur dans les cantines scolaires.",
    ],
    "espaces-verts": [
        "Végétalisation renforcée et plan de bancs publics pour des espaces de repos dans toute la ville.",
    ],
    "centres-sante": [
        "Soutien à la création d'une clinique satellite du CHU dans le quartier Mosson (ancienne tour Assas).",
        "Déploiement de centres de santé pluridisciplinaires dans les quartiers prioritaires avec médecins salariés.",
        "Prise en charge des problèmes de santé mentale et lutte contre le non-recours aux soins.",
    ],
    "seniors": [
        "Création de 400 à 500 places dans quatre résidences sociales municipales pour seniors, à tarifs inférieurs au privé.",
        "Déploiement d'une application de détection des chutes pour les personnes âgées.",
        "Aide à l'adaptation des logements pour prévenir les accidents domestiques.",
        "Ajout de toilettes publiques adaptées aux personnes à mobilité réduite.",
    ],
    "budget-participatif": [
        "Mutuelle communale de santé déjà en place et maintenue.",
    ],
    "services-publics": [
        "Création de 50 postes de gardiens-concierges dans les résidences sociales avec rôle élargi d'animation.",
        "Groupe de Sécurité Résidentielle et d'Intervention (GSRI) coordonnant travail de terrain et médiation.",
        "Accès gratuit aux 15 bibliothèques municipales avec extension prévue à l'échelle métropolitaine.",
    ],
    "commerce-local": [
        "Création d'un Bureau municipal du pouvoir d'achat pour négocier des achats groupés.",
        "Achats groupés communaux pour assurances habitation, systèmes de sécurité, pompes à chaleur et ventilateurs.",
    ],
    "pouvoir-achat": [
        "Gratuité des transports en commun pour protéger le pouvoir d'achat.",
        "Tarification sociale de l'eau maintenue.",
        "Tarifs sociaux maintenus pour musées, piscines et cantines.",
    ],
    "accessibilite": [
        "Toilettes publiques supplémentaires adaptées aux personnes à mobilité réduite.",
    ],
    "aide-sociale": [
        "Soutien financier jusqu'à 25% pour les bailleurs privés mettant en place des concierges dans leurs résidences.",
        "Obligation pour les promoteurs privés construisant du logement social de participer aux programmes de sécurité résidentielle.",
    ],
}


# ============================================================
# OZIOL (Montpellier) — infoccitanie.fr + echo-des-tribunes.com
# ============================================================

MESURES_OZIOL = {
    "acces-logement": [
        "Création d'un guichet municipal des droits au logement pour faciliter l'accès aux droits, mobiliser les 12 000 à 18 000 logements vacants et réguler les loyers.",
    ],
    "alimentation-durable": [
        "Création d'un foncier agricole municipal pour acquérir des terres et les soustraire à la spéculation, permettant l'installation de nouveaux agriculteurs.",
    ],
    "equipements-culturels": [
        "Renforcement des Maisons pour tous comme lieux de vie culturelle.",
        "Transformation du MOCO en espaces dédiés aux cultures populaires accessibles.",
        "Augmentation des financements pour les associations culturelles de quartiers populaires.",
    ],
    "budget-participatif": [
        "Instauration du référendum d'initiative citoyenne municipale activé par pétition sur tout sujet.",
        "Mécanisme de révocation permettant aux citoyens de retirer leur confiance aux élus en cours de mandat.",
    ],
    "cantines-fournitures": [
        "Ouverture d'un restaurant municipal servant des repas bio locaux à bas prix quotidiennement.",
        "Subvention de l'accès aux cantines scolaires en dehors des heures de classe.",
    ],
    "accessibilite": [
        "Plan pluriannuel d'accessibilité : mise aux normes de tous les bâtiments municipaux et formation du personnel à l'accueil des personnes handicapées.",
    ],
    "vie-associative": [
        "Soutien accru aux organisations de quartiers populaires pour la pluralité culturelle.",
    ],
}


def update_candidate(json_path, candidat_id, mesures_dict, source, source_url):
    """Met à jour les mesures d'un candidat dans le JSON."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in mesures_dict and len(mesures_dict[st_id]) > 0:
                prop = st["propositions"].get(candidat_id)
                if prop is None:
                    prop = {}
                    st["propositions"][candidat_id] = prop

                old_count = len(prop.get("mesures", []))
                new_mesures = mesures_dict[st_id]

                if len(new_mesures) >= old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = source
                    prop["sourceUrl"] = source_url
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} → {len(new_mesures)}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total = sum(len(v) for v in mesures_dict.values())
    print(f"    {updated} sous-thèmes mis à jour, {total} mesures total")
    return total


def main():
    print("=" * 60)
    print("  RÉ-EXTRACTION BATCH 3")
    print("=" * 60)

    json_path = os.path.join(ROOT_DIR, "data", "elections", "montpellier-2026.json")

    # DELAFOSSE
    print("\n  DELAFOSSE (Montpellier):")
    update_candidate(
        json_path, "delafosse", MESURES_DELAFOSSE,
        "Programme officiel 2026 — Michaël Delafosse",
        "https://www.michaeldelafosse.fr/"
    )

    # OZIOL
    print("\n  OZIOL (Montpellier):")
    update_candidate(
        json_path, "oziol", MESURES_OZIOL,
        "Programme officiel 2026 — Nathalie Oziol",
        "https://infoccitanie.fr/"
    )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
