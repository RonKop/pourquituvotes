#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Met à jour les propositions de Mounir Belhamiti (Nantes Mérite Mieux)
depuis le site nantesmeritemieux.fr reçu par email le 01/03/2026.
"""

import json
import os
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "nantes-2026.json")
CANDIDAT_ID = "belhamiti"

PROPOSITIONS = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Porter les effectifs de la police municipale à 300 agents, avec une présence 24h/24.",
        "Créer un poste fixe de police municipale dans le secteur Commerce.",
        "Armer et équiper modernement la police municipale.",
        "Créer des brigades cynophiles anti-stupéfiants.",
        "Déployer des véhicules-postes de proximité dans les quartiers.",
    ],
    "videoprotection": [
        "Déployer la vidéoprotection dans les zones sensibles.",
        "Renforcer la présence policière dans les transports, espaces publics et aux abords des écoles.",
    ],
    "prevention-mediation": [
        "Créer un service de médiateurs jeunes dans les zones festives.",
        "Mettre en place un service de médiation des conflits de voisinage.",
        "Créer une cellule municipale de lutte contre le cyberharcèlement.",
        "Appliquer une politique de tolérance zéro contre les trafics et les incivilités.",
    ],
    "violences-femmes": [
        "Développer le projet Citad'Elles pour l'accueil des femmes victimes de violences.",
    ],

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Rétablir la circulation sur le pont Anne-de-Bretagne.",
        "Lancer une étude pour de nouveaux franchissements de la Loire (pont ou téléphérique) et de l'Erdre.",
        "Renforcer les connexions Chronobus-Tramway-TER.",
        "Moderniser l'aéroport Nantes Atlantique.",
    ],
    "velo-mobilites-douces": [
        "Créer 200 km de pistes cyclables sécurisées.",
        "Déployer un plan sécurité vélo : signalisation renforcée, audits de pistes, prévention.",
        "Installer des bornes de recharge pour véhicules électriques.",
    ],
    "pietons-circulation": [
        "Mettre fin aux amendes automatiques injustifiées.",
    ],
    "stationnement": [
        "Instaurer la gratuité du stationnement de 12h à 14h pour soutenir les commerces.",
        "Rendre le stationnement gratuit pour les personnels de santé et les personnes en situation de handicap.",
    ],
    "tarifs-gratuite": [
        "Instaurer la gratuité totale des transports en commun pour les scolaires.",
        "Maintenir la gratuité des transports le week-end.",
    ],

    # ── LOGEMENT ──
    "logement-social": [
        "Construire 20 000 logements pendant le mandat, avec des logements diversifiés (familiaux, étudiants, seniors).",
        "Créer une foncière métropolitaine pour le rachat de foncier.",
    ],
    "logements-vacants": None,
    "encadrement-loyers": None,
    "acces-logement": [
        "Créer un cadre favorable pour les investisseurs et développer des partenariats avec les bailleurs et promoteurs.",
        "Réviser le Plan Local d'Urbanisme métropolitain pour faciliter la construction.",
        "Développer des logements adaptés au handicap et favoriser le maintien à domicile.",
    ],

    # ── ÉDUCATION ──
    "petite-enfance": [
        "Créer de nouvelles crèches.",
        "Proposer des goûters de qualité dans les structures d'accueil.",
    ],
    "ecoles-renovation": [
        "Lancer un plan pluriannuel de rénovation des écoles : confort thermique, végétalisation des cours, modernisation des équipements pédagogiques.",
    ],
    "cantines-fournitures": [
        "Garantir une restauration scolaire de qualité avec des produits locaux et bio.",
        "Mettre en place une tarification juste pour la cantine.",
    ],
    "periscolaire-loisirs": [
        "Stabiliser les équipes d'animation périscolaire.",
        "Développer des activités sportives et culturelles accessibles à tous les enfants.",
        "Organiser des classes de nature pour tous les enfants.",
        "Simplifier l'inscription aux centres de loisirs.",
    ],
    "jeunesse": [
        "Créer un festival annuel de la jeunesse nantaise.",
    ],

    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Créer de nouveaux parcs et forêts urbaines.",
        "Développer des équipements en accès libre le long de la Loire et de l'Erdre.",
    ],
    "proprete-dechets": [
        "Lancer un plan « Ville propre » et « Ville éclairée ».",
        "Améliorer la collecte et le tri des déchets.",
    ],
    "climat-adaptation": [
        "Viser la neutralité carbone municipale par la rénovation énergétique et le développement des énergies renouvelables.",
        "Élaborer un plan d'adaptation climatique sur 30 ans avec un plan canicule renforcé.",
    ],
    "renovation-energetique": [
        "Prioriser l'isolation des logements anciens.",
        "Améliorer l'isolation, l'adaptation à la chaleur et l'efficacité énergétique des logements neufs.",
    ],
    "alimentation-durable": [
        "Développer les produits locaux et bio dans les cantines scolaires et la restauration collective.",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Aider à l'installation de nouveaux médecins dans les quartiers sous-dotés.",
        "Soutenir les centres de santé pluridisciplinaires.",
    ],
    "prevention-sante": [
        "Lancer un plan municipal de santé mentale.",
        "Former les agents municipaux aux premiers secours en santé mentale.",
    ],
    "seniors": [
        "Créer une carte senior Nantes : tarifs réduits transports, accès gratuit ou prioritaire aux équipements culturels et sportifs, réductions chez les commerçants partenaires.",
        "Lancer le plan « Bien vieillir chez soi » : aides à l'adaptation des logements, financement d'équipements (monte-escaliers, douches).",
        "Créer une équipe dédiée à la lutte contre l'isolement des personnes âgées.",
        "Développer l'habitat inclusif, les résidences seniors et les logements intergénérationnels.",
        "Proposer des activités sport-santé gratuites pour les seniors.",
        "Lancer un plan numérique senior.",
        "Nommer un adjoint au maire dédié aux seniors.",
    ],

    # ── DÉMOCRATIE ──
    "budget-participatif": [
        "Instaurer un référendum local pour les grands projets municipaux.",
    ],
    "transparence": [
        "Réaliser un audit complet des finances de la ville.",
        "Engager une trajectoire de baisse progressive de la taxe foncière.",
        "Exonérer de taxe foncière les primo-accédants.",
        "Garantir la transparence des finances publiques.",
    ],
    "vie-associative": [
        "Instaurer un dialogue permanent avec les habitants, associations et commerçants.",
        "Organiser des concertations régulières avec suivi public des engagements.",
    ],
    "services-publics": None,

    # ── ÉCONOMIE ──
    "commerce-local": [
        "Créer un Grand Food Hall en centre-ville mêlant producteurs, restauration et culture.",
        "Utiliser le droit de préemption pour les commerces stratégiques.",
        "Développer une politique d'attractivité commerciale avec aides à l'installation et au maintien des commerçants indépendants.",
        "Organiser des animations commerciales et valoriser les pôles de quartiers.",
    ],
    "emploi-insertion": [
        "Renforcer le soutien aux associations d'insertion.",
        "Créer un dispositif d'inclusion et d'innovation sociale avec mentorat.",
    ],
    "attractivite": [
        "Réviser le PLU pour faciliter l'implantation d'entreprises.",
        "Attirer les investisseurs et promouvoir Nantes à l'international.",
        "Aider les entreprises nantaises à l'export (salons, forums).",
        "Structurer les filières d'avenir : santé/medtech, énergie, industrie durable, innovation.",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Construire un nouveau Conservatoire de musique.",
        "Rénover la médiathèque Jacques-Demy.",
        "Moderniser les centres sociaux, gymnases et piscines.",
        "Construire un Palais des Sports à Beaulieu.",
        "Rendre le Voyage à Nantes plus surprenant en valorisant les artistes nantais.",
        "Créer une œuvre emblématique pour Nantes (dans la lignée de l'arbre aux hérons).",
    ],
    "evenements-creation": [
        "Soutenir les associations culturelles et sportives.",
        "Créer de nouveaux événements populaires.",
    ],

    # ── SPORT ──
    "equipements-sportifs": [
        "Déployer de nouveaux équipements sportifs dans les quartiers.",
    ],
    "sport-pour-tous": [
        "Rééquilibrer les subventions entre sports collectifs et individuels.",
        "Prioriser les subventions aux sports amateurs.",
    ],

    # ── URBANISME ──
    "amenagement-urbain": [
        "Aménager le quartier du futur CHU en nouveau pôle de vie.",
        "Créer de nouveaux parcs, jardins et œuvres d'art dans l'espace public.",
    ],
    "accessibilite": [
        "Faire de l'inclusion une priorité transversale : accessibilité des espaces, transports et équipements.",
        "Créer un guichet unique accessibilité et autonomie.",
        "Lancer un plan pluriannuel d'accessibilité 2026-2032.",
        "Nommer un adjoint dédié au handicap avec une feuille de route.",
    ],
    "quartiers-prioritaires": [
        "Renforcer les actions dans les Quartiers Prioritaires de la Ville.",
    ],

    # ── SOLIDARITÉ ──
    "aide-sociale": [
        "Améliorer la coordination entre le CCAS et les associations.",
        "Protéger les sans-domicile, les jeunes en rupture et les enfants placés, avec priorité d'accès au logement.",
    ],
    "egalite-discriminations": [
        "Lutter contre toutes les discriminations.",
        "Soutenir les associations de défense des droits LGBT+.",
        "Accompagner les personnes en situation de handicap vers l'emploi et le logement.",
    ],
    "pouvoir-achat": [
        "Gratuité des transports pour les scolaires et le week-end.",
        "Gratuité du stationnement 12h-14h pour soutenir les commerces de proximité.",
        "Baisse progressive de la taxe foncière et exonération pour les primo-accédants.",
    ],
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for c in data["candidats"]:
        if c["id"] == CANDIDAT_ID:
            c["programmeUrl"] = "https://nantesmeritemieux.fr/"
            c["programmeComplet"] = True
            break

    updated = 0
    added = 0
    total_mesures = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id not in PROPOSITIONS:
                continue

            new_mesures = PROPOSITIONS[st_id]
            if new_mesures is None:
                continue

            if "propositions" not in st:
                st["propositions"] = {}

            had_before = (
                CANDIDAT_ID in st["propositions"]
                and st["propositions"][CANDIDAT_ID]
                and st["propositions"][CANDIDAT_ID].get("mesures")
            )

            st["propositions"][CANDIDAT_ID] = {"mesures": new_mesures}
            total_mesures += len(new_mesures)
            if had_before:
                updated += 1
            else:
                added += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"{'='*55}")
    print(f"  MISE À JOUR — Mounir Belhamiti (Nantes)")
    print(f"{'='*55}")
    print(f"  Sous-thèmes mis à jour : {updated}")
    print(f"  Sous-thèmes ajoutés    : {added}")
    print(f"  Total mesures          : {total_mesures}")
    print(f"  JSON écrit : {JSON_PATH}")


if __name__ == "__main__":
    main()
