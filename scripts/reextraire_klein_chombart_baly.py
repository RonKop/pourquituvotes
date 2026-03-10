#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction batch : Klein (Aix-en-Provence), Chombart (Nantes), Baly (Lille).
Sources : sites de campagne et presse locale.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


# ============================================================
# KLEIN (Aix-en-Provence) — philippe-klein.fr
# ============================================================

MESURES_KLEIN = {
    "police-municipale": [
        "Installer 150 bornes d'appel d'urgence (S.O.AIX) connectées à la police municipale dans les zones fréquentées.",
        "Recruter pour atteindre 1 policier municipal pour 800 habitants d'ici la fin du mandat.",
        "Rendre la police municipale opérationnelle 24h/24 sur tout le territoire.",
        "Créer un centre de formation municipale pour les policiers.",
        "Créer une brigade spécialisée anti-cambriolages.",
    ],
    "videoprotection": [
        "Quadrupler le rythme d'installation des caméras de vidéosurveillance.",
        "Réparer toutes les caméras défaillantes et déployer des technologies d'analyse avancée.",
    ],
    "prevention-mediation": [
        "Signer une convention avec la police nationale et le procureur pour des sanctions immédiates.",
        "Mettre en place des plans micro-territoriaux anti-stupéfiants avec convocation des contrevenants.",
        "Coordonner avec les bailleurs sociaux l'expulsion des trafiquants.",
    ],
    "velo-mobilites-douces": [
        "Créer des pistes cyclables dédiées reliant les quatre points cardinaux de la ville.",
    ],
    "transports-en-commun": [
        "Créer des voies de bus réservées sur la RD9 pour supprimer les embouteillages sous 2 ans.",
        "Développer des alternatives innovantes au BHNS (bus à haut niveau de service).",
    ],
    "encadrement-loyers": [
        "Réguler la location touristique des résidences secondaires pour protéger le parc résidentiel.",
    ],
    "logements-vacants": [
        "Transformer les bureaux vides en logements pour étudiants et jeunes actifs.",
    ],
    "amenagement-urbain": [
        "Conditionner toute construction à la création préalable des infrastructures (routes, réseaux, eaux pluviales).",
    ],
    "espaces-verts": [
        "Désimperméabiliser et végétaliser l'équivalent d'un second parc Jourdan.",
        "Valoriser l'Arc comme corridor de fraîcheur et de biodiversité.",
        "Planter massivement des espèces adaptées au climat méditerranéen dans les zones les plus exposées à la chaleur.",
    ],
    "climat-adaptation": [
        "Promouvoir l'architecture bioclimatique optimisant la circulation d'air et le rafraîchissement naturel.",
        "Protéger les ressources forestières avec une politique dédiée.",
    ],
    "centres-sante": [
        "Créer des centres de santé accessibles 7j/7.",
        "Renforcer l'aide à l'installation des professionnels de santé.",
    ],
    "budget-participatif": [
        "Allouer des budgets d'investissement directement à chaque conseil de quartier pour les décisions prioritaires.",
    ],
    "transparence": [
        "Placer la rigueur et la transparence financière au cœur de la gestion municipale.",
        "S'engager à ne pas augmenter les impôts locaux avec des baisses possibles.",
        "Réduire les dépenses de fonctionnement pour investir davantage.",
    ],
    "pouvoir-achat": [
        "Aucune augmentation des impôts locaux, avec possibilité de baisse.",
    ],
}


# ============================================================
# CHOMBART (Nantes) — foulqueschombartdelauwe.fr (4 pages)
# ============================================================

MESURES_CHOMBART = {
    "police-municipale": [
        "Armer la police municipale pour protéger les agents.",
        "Doubler les effectifs de police municipale à 450 agents, opérationnels 24h/24 et 7j/7.",
    ],
    "prevention-mediation": [
        "Exclure les délinquants des programmes de logement social.",
        "Appliquer une tolérance zéro contre la consommation de drogue dans toute la ville.",
        "Poursuivre systématiquement les auteurs de tags et dégradations.",
    ],
    "transports-en-commun": [
        "Lancer des lignes de chronobus circulaires pour connecter les quartiers entre eux.",
        "Mettre en place un ticket unique pour tous les modes de transport.",
    ],
    "velo-mobilites-douces": [
        "Maintenir et étendre le réseau Bicloo de vélos en libre-service dans tous les quartiers.",
        "Accélérer le déploiement de bornes de recharge pour véhicules électriques.",
    ],
    "logement-social": [
        "Permettre aux locataires de logements sociaux d'accéder à la propriété de leur logement.",
    ],
    "acces-logement": [
        "Réduire les délais de permis de construire à 3 mois pour les particuliers et 6 mois pour les promoteurs.",
    ],
    "petite-enfance": [
        "Créer 1 000 places de crèche supplémentaires d'ici 2030.",
    ],
    "centres-sante": [
        "Garantir une maison médicale à moins d'un kilomètre de chaque habitant.",
    ],
    "espaces-verts": [
        "Planter 100 000 arbres dans toute la ville.",
    ],
    "proprete-dechets": [
        "Passer le tri sélectif de 8% à 30% en un mandat.",
    ],
    "commerce-local": [
        "Rénover le marché de Talensac et construire de nouvelles halles au Bouffay.",
        "Rendre le centre-ville accessible, sûr et attractif pour les commerces.",
    ],
    "attractivite": [
        "Faire de Nantes la ville championne du naval, de l'aéronautique et de l'innovation en santé.",
        "Creuser un tunnel sous la Loire pour fluidifier la circulation.",
    ],
    "equipements-culturels": [
        "Préserver le budget culturel avec des critères transparents et un soutien aux artistes locaux.",
    ],
    "accessibilite": [
        "Intégrer le handicap dans toutes les politiques publiques, priorité à l'accessibilité des transports.",
    ],
    "pouvoir-achat": [
        "Baisser la taxe foncière à mi-mandat et réduire la CFE sous les 30%.",
        "Réduire la dette municipale.",
    ],
}


# ============================================================
# BALY (Lille) — lilledemain.fr
# ============================================================

MESURES_BALY = {
    "police-municipale": [
        "Atteindre 1 policier municipal pour 1 000 habitants.",
    ],
    "transports-en-commun": [
        "Rendre les bus gratuits sur l'ensemble du réseau.",
        "Améliorer la fiabilité du métro et renforcer la fréquence.",
        "Étendre le réseau de tramway.",
    ],
    "tarifs-gratuite": [
        "Gratuité des bus sur tout le réseau lillois.",
    ],
    "stationnement": [
        "Stationnement résidentiel à 1€/mois (premier échelon).",
        "Créer des pass visiteurs pour le stationnement.",
    ],
    "logement-social": [
        "Construire 2 000 logements abordables à moins de 300€/mois.",
    ],
    "cantines-fournitures": [
        "100% bio et local dans les cantines scolaires dès la crèche.",
    ],
    "espaces-verts": [
        "Créer un grand parc à Saint-Sauveur.",
        "Augmenter les espaces verts dans toute la ville dense.",
        "Développer des cœurs de quartier végétalisés et apaisés.",
    ],
    "centres-sante": [
        "Équiper chaque quartier d'un centre de santé.",
    ],
    "commerce-local": [
        "Plafonner les loyers commerciaux pour protéger la diversité des commerces.",
    ],
    "encadrement-loyers": [
        "Plafonner les loyers commerciaux pour soutenir les commerces de proximité.",
    ],
    "equipements-culturels": [
        "Ouvrir une grande médiathèque avec des horaires élargis.",
    ],
    "equipements-sportifs": [
        "Créer une zone de baignade gratuite dans la Deûle.",
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
                        print(f"    {st_id}: {old_count} -> {len(new_mesures)}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total = sum(len(v) for v in mesures_dict.values())
    print(f"    {updated} sous-thèmes mis à jour, {total} mesures total")
    return total


def main():
    print("=" * 60)
    print("  RÉ-EXTRACTION KLEIN, CHOMBART, BALY")
    print("=" * 60)

    # KLEIN (Aix-en-Provence)
    print("\n  KLEIN (Aix-en-Provence):")
    update_candidate(
        os.path.join(ROOT_DIR, "data", "elections", "aix-en-provence-2026.json"),
        "klein", MESURES_KLEIN,
        "Programme officiel 2026 — Philippe Klein",
        "https://www.philippe-klein.fr/"
    )

    # CHOMBART (Nantes)
    print("\n  CHOMBART (Nantes):")
    update_candidate(
        os.path.join(ROOT_DIR, "data", "elections", "nantes-2026.json"),
        "chombart", MESURES_CHOMBART,
        "Programme officiel 2026 — Foulques Chombart de Lauwe",
        "https://www.foulqueschombartdelauwe.fr/"
    )

    # BALY (Lille)
    print("\n  BALY (Lille):")
    update_candidate(
        os.path.join(ROOT_DIR, "data", "elections", "lille-2026.json"),
        "baly", MESURES_BALY,
        "Programme officiel 2026 — Stéphane Baly",
        "https://lilledemain.fr/notre-programme/"
    )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
