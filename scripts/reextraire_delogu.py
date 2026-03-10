#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction des mesures de Delogu (Marseille) depuis sebastiendelogu2026.fr.
Programme de 379 mesures en 4 chapitres. Extraction partielle (chapitres 1 partiels,
2 partiel, 3 partiel, 4 partiel) — à compléter ultérieurement.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "marseille-2026.json")

SOURCE = "Programme officiel 2026 — Sébastien Delogu"
SOURCE_URL = "https://sebastiendelogu2026.fr/programme/sommaire/"

MESURES = {
    # ===== CHAPITRE I — Rendre le pouvoir aux citoyens (mesures 1-17 sur 45) =====
    "budget-participatif": [
        "Mettre en place des comités de quartier dotés de budgets participatifs, réunissant habitants, associations et élus.",
        "Créer un comité populaire du budget et un comité populaire de la commande publique pour démocratiser les finances municipales.",
        "Faire appliquer le droit de pétition : au-delà de 10 000 signatures, le sujet doit être examiné par le Conseil municipal.",
        "Permettre les référendums locaux lorsqu'une pétition atteint 10% des électeurs, avec application du résultat si la participation dépasse 50%.",
        "Établir un diagnostic partagé des urgences locales via les comités de quartier.",
        "Créer un comité populaire de planification écologique co-construit avec associations et collectifs.",
    ],
    "transparence": [
        "Garantir une attribution juste et transparente des ressources publiques (logements, crèches, marchés publics) par les comités populaires.",
        "Mettre fin au clientélisme en suspendant les embauches municipales 3-6 mois avant/après les élections, sauf urgence avérée.",
        "Publier les rendez-vous des élus avec représentants privés et instaurer une détection des conflits d'intérêts avant chaque Conseil municipal.",
        "Imposer la sobriété des élus en rééquilibrant les indemnités et supprimant certaines primes.",
        "Créer une Maison des lanceurs d'alerte assurant protection juridique et confidentialité, avec service de déontologie indépendant.",
    ],
    "services-publics": [
        "Créer l'application « Marseille ma ville » et un guichet unique avec accompagnement aux droits dans chaque mairie de secteur.",
        "Soutenir les associations de traduction et d'apprentissage du français pour garantir l'accès aux services publics.",
        "Constituer des réserves municipales de biens essentiels mobilisables en urgence.",
        "Créer un réseau municipal d'entraide avec formation massive aux premiers secours.",
        "Renforcer la participation électorale par une grande campagne d'inscription sur les listes électorales.",
    ],
    "vie-associative": [
        "Mettre à disposition des salles municipales et développer l'éducation populaire (assemblées de quartier, enquêtes participatives).",
        "Créer des comités populaires liés aux délégations municipales pour suivre et co-piloter les politiques publiques.",
        "Renforcer l'Assemblée citoyenne avec 111 habitants tirés au sort disposant d'un droit d'initiative pour soumettre des délibérations.",
        "Lancer un plan d'éducation populaire à l'écologie avec budget dédié et Bibliothèque de l'écologie.",
        "Constituer un réseau de référents formés sur les thématiques écologiques dans les comités de quartier.",
    ],

    # ===== CHAPITRE II — Répondre aux besoins fondamentaux (mesures 46-57 sur 146) =====
    "logement-social": [
        "Créer 30 000 logements dont 70% sociaux, un tiers réservé aux ménages les plus modestes.",
        "Développer l'habitat participatif, coopératif et le bail réel solidaire.",
        "Transformer Marseille Habitat en outil public démocratisé.",
        "Exiger des financements de l'État à hauteur des besoins réels de la ville.",
    ],
    "logements-vacants": [
        "Réquisitionner les logements vacants et créer un registre public des logements inoccupés.",
    ],
    "acces-logement": [
        "Garantir l'accès au logement comme droit universel via une « sécurité sociale du logement ».",
        "Renforcer la direction municipale de l'habitat comme guichet unique pour tous les Marseillais.",
        "Transformer la brigade du logement en outil de défense du droit au logement.",
        "Organiser des Assises populaires du logement pour co-construire la politique habitat.",
        "Faire respecter le droit au logement digne par les bailleurs sociaux.",
        "Créer une régie municipale des ascenseurs pour les résidences sociales.",
        "Démocratiser le fonctionnement du logement social avec participation des locataires.",
    ],

    # ===== CHAPITRE III — Urgence écologique (mesures 192-208 sur 108) =====
    "climat-adaptation": [
        "Adopter un plan canicule renforcé avec lieux d'accueil frais pour les populations vulnérables.",
        "Élargir les horaires d'ouverture des parcs, plages et jardins durant les fortes chaleurs.",
        "Installer voiles, pergolas végétalisées et structures d'ombre dans les rues étroites.",
        "Transformer les espaces publics et constructions selon les principes architecturaux provençaux.",
        "Mettre à jour les cartes des risques et les intégrer obligatoirement dans les décisions d'urbanisme.",
        "Adopter un plan de reconstruction post-crise évitant les zones dangereuses.",
    ],
    "espaces-verts": [
        "Déployer une stratégie de végétalisation massive avec diagnostics par arrondissement et micro-forêts urbaines.",
        "Mobiliser des financements pour réintroduire massivement la nature dans les quartiers populaires.",
    ],
    "prevention-sante": [
        "Créer un Observatoire public Santé-Environnement pour surveiller la qualité de l'air, de l'eau, du bruit et des polluants.",
    ],
    "amenagement-urbain": [
        "Intensifier les clauses environnementales dans les marchés municipaux avec bilan carbone systématique.",
    ],

    # ===== CHAPITRE IV — Combattre les discriminations (mesures 300-313 sur 80) =====
    "egalite-discriminations": [
        "Créer un observatoire municipal des discriminations avec quatre pôles spécialisés (handicap, sexisme, racisme, LGBTI), aide juridique gratuite et ligne d'écoute.",
        "Désigner des référents discrimination dans chaque service municipal pour traiter les plaintes.",
        "Lancer des campagnes de sensibilisation publiques lors des dates clés (8 mars, 21 mars, Mois des Fiertés, 25 novembre).",
        "Reconnaître et préserver les histoires des mouvements féministes, antiracistes, LGBTQIA+ et de résistance dans l'espace public.",
        "Permettre à la municipalité de se constituer partie civile aux côtés des victimes de discrimination.",
        "Intégrer l'éducation anti-discrimination dans toute la programmation municipale.",
        "Mettre en place un budget genré pour évaluer l'impact des politiques sur les femmes et les hommes.",
        "Garantir l'égalité professionnelle des femmes dans les services municipaux : parité aux postes de direction et congé menstruel.",
        "Assurer que les espaces publics et équipements municipaux offrent sécurité, accessibilité et confort pour tous.",
        "Combattre les discriminations au logement par l'anonymisation partielle des dossiers et des critères transparents.",
        "Garantir les droits des gens du voyage avec des aires d'accueil dignes.",
        "Protéger la laïcité en garantissant un accès équitable aux équipements municipaux.",
    ],
    "violences-femmes": [
        "Financer la création d'un centre féministe offrant espace d'organisation, services de prévention et protection menstruelle gratuite.",
        "Renforcer l'hébergement d'urgence et l'accès au logement social pour les victimes de violences conjugales via un guichet unique.",
    ],
    "aide-sociale": [
        "Organiser l'accueil et la solidarité envers les populations les plus fragiles avec des dispositifs d'aide aux droits.",
    ],
}


def main():
    print("=" * 60)
    print("  RÉ-EXTRACTION DELOGU (Marseille)")
    print("=" * 60)

    total = sum(len(v) for v in MESURES.values())
    print(f"\n  {total} mesures dans {len(MESURES)} sous-thèmes")
    print("  (extraction partielle — 4 chapitres partiels sur 379 mesures)")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in MESURES and len(MESURES[st_id]) > 0:
                prop = st["propositions"].get("delogu")
                if prop is None:
                    prop = {}
                    st["propositions"]["delogu"] = prop

                old_count = len(prop.get("mesures", []))
                new_mesures = MESURES[st_id]

                if len(new_mesures) >= old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = SOURCE
                    prop["sourceUrl"] = SOURCE_URL
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} → {len(new_mesures)}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n    {updated} sous-thèmes mis à jour")
    print("=" * 60)


if __name__ == "__main__":
    main()
