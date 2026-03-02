#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Met à jour les propositions de Michel Haberstrau (Dijon change d'ère)
depuis le fichier argumentaire XLSX partagé par l'équipe de campagne.
"""

import json
import os
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "dijon-2026.json")
CANDIDAT_ID = "haberstrau"

# Mapping : sous-thème -> liste de mesures extraites du XLSX argumentaire
PROPOSITIONS = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Mettre en place une police municipale de proximité, en complémentarité avec un dispositif de prévention et de médiation.",
    ],
    "videoprotection": None,
    "prevention-mediation": [
        "Créer un service municipal permanent de prévention et de médiation dans l'espace public, associant éducateurs spécialisés diplômés et médiateurs professionnels, pour prévenir les incivilités et renforcer la tranquillité publique.",
    ],
    "violences-femmes": [
        "Repenser l'urbanisme pour la sécurité et l'autonomie des femmes : éclairage adapté, arrêt de bus à la demande de nuit, dispositif d'alerte en cas d'agression sur la voie publique.",
        "Généraliser les formations de prévention et de lutte contre les violences sexistes et sexuelles auprès des agents de la municipalité et des personnels de service public.",
    ],

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Questionner le tracé de la troisième ligne de tramway via un moratoire pour redonner la parole aux habitants et prioriser le désenclavement des quartiers (Fontaine-d'Ouche…).",
        "Étendre les horaires du réseau Divia pour améliorer la desserte des zones d'activités et faciliter l'accès aux lieux professionnels en horaires décalés.",
    ],
    "velo-mobilites-douces": [
        "Déployer un réseau continu, sécurisé et confortable pour le vélo à l'échelle de la ville et de la métropole.",
    ],
    "pietons-circulation": [
        "Sécuriser les abords d'écoles avec des rues scolaires apaisées, des places piétonnisées, de l'ombrage et des aménagements favorisant l'autonomie des enfants.",
        "Déployer un réseau continu et confortable pour la marche à l'échelle de la ville et de la métropole.",
    ],
    "stationnement": None,
    "tarifs-gratuite": [
        "Rendre les transports en commun et le vélo gratuits pour les moins de 26 ans, les personnes en situation de handicap et les bénéficiaires des minima sociaux.",
    ],

    # ── LOGEMENT ──
    "logement-social": [
        "Porter la part de logements sociaux à 25 % et soutenir l'accession sociale à la propriété.",
        "Augmenter le parc locatif en limitant les usages spéculatifs et temporaires.",
    ],
    "logements-vacants": [
        "Limiter les locations de courte durée (type Airbnb) via un régime déclaratif et une limitation stricte.",
    ],
    "encadrement-loyers": [
        "Solliciter la préfecture pour le classement de Dijon en zone tendue et appliquer l'encadrement des loyers dans les 6 premiers mois après obtention.",
    ],
    "acces-logement": None,

    # ── ÉDUCATION ──
    "petite-enfance": [
        "Garantir l'égalité d'accès aux crèches et services de proximité essentiels dans tous les quartiers.",
    ],
    "ecoles-renovation": [
        "Lancer un plan ambitieux 'Renov'École' pour accélérer la végétalisation et la rénovation thermique des écoles.",
        "Renforcer le nombre d'ATSEM dans les écoles maternelles pour tendre vers une ATSEM par classe.",
    ],
    "cantines-fournitures": [
        "Instaurer deux journées végétariennes hebdomadaires et une option végétarienne quotidienne dans les cantines scolaires.",
        "Instaurer une journée végétalienne hebdomadaire en restauration scolaire.",
        "Fixer un objectif de réduction de 50 % de la consommation de produits d'origine animale d'ici 2032 dans la restauration collective.",
    ],
    "periscolaire-loisirs": [
        "Faire la ville à hauteur d'enfants : aménagements favorisant l'autonomie des plus jeunes, places piétonnes ombragées.",
    ],
    "jeunesse": None,

    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Plan 'Dijon, Grandeur Nature' : désimperméabilisation, plantations massives (arbres, haies, micro-forêts, forêts comestibles, jardins partagés), pour que chacun soit à moins de 5 minutes d'un espace de nature.",
        "Rouvrir le Suzon et aménager des promenades végétalisées et continues le long de l'Ouche, pour remettre l'eau, la fraîcheur et le vivant au cœur de Dijon.",
        "Révision du PLUi-HD pour renforcer la protection des arbres et atteindre le zéro artificialisation brute.",
        "Engager des travaux au lac Kir pour améliorer la qualité de l'eau et favoriser la baignade, et à plus long terme, faire du Port-du-canal un espace de baignade.",
    ],
    "proprete-dechets": [
        "Reprendre en gestion municipale le service des déchets, aujourd'hui confié au privé.",
        "Installer des toilettes publiques et espaces bébés multipliés et adaptés dans l'ensemble de la ville.",
    ],
    "climat-adaptation": [
        "Organiser une convention citoyenne 'Dijon Cap 2050' pour décider des grandes orientations en matière de transitions écologique et sociale, d'autonomie alimentaire et d'adaptation de la ville aux conditions de vie en 2050.",
    ],
    "renovation-energetique": [
        "Rénovation massive du parc public et privé en priorité sur les passoires thermiques, avec exonération de taxe foncière pour les propriétaires engagés dans des travaux performants (matériaux biosourcés privilégiés).",
    ],
    "alimentation-durable": [
        "Lancer la Sécurité sociale de l'alimentation à Dijon pour faciliter l'accès de tous à une alimentation locale et de qualité.",
        "Proposer systématiquement une offre végétale significative dans les buffets des réceptions officielles de la ville.",
        "Exclure les produits issus de l'élevage sans accès au plein air et de la pisciculture dans les achats publics responsables.",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Soutenir l'implantation d'équipements de santé dans les quartiers les plus déficitaires et expérimenter la création d'un tiers-lieu en santé.",
    ],
    "prevention-sante": [
        "Généraliser la mise à disposition de protections périodiques dans les espaces publics, locaux municipaux et lieux d'enseignement.",
    ],
    "seniors": None,

    # ── DÉMOCRATIE ──
    "budget-participatif": [
        "Lancer un processus d'assemblées citoyennes régulières véritablement décisionnaires sur les grands projets de la ville (Cité de la Gastronomie, réseau de transports, urbanisme).",
    ],
    "transparence": [
        "Signer la charte de Transparency International et mettre en place un plan de prévention de la corruption.",
        "Créer un pôle d'audit interne, publier les rencontres des décideurs publics avec des représentants d'intérêts privés.",
        "Assurer une transparence totale des règles d'attribution des subventions aux associations.",
        "Encadrer le recours aux cabinets de conseil et aux collaborateurs de cabinet.",
        "Publier en début de mandat le montant de l'ensemble des indemnités perçues par les élus.",
    ],
    "vie-associative": [
        "Soutenir les associations en augmentant les budgets, simplifiant l'administration, mettant à disposition des locaux municipaux et en rendant visibles les dispositifs existants.",
    ],
    "services-publics": [
        "Engager un processus de reprise en gestion municipale des services publics essentiels aujourd'hui confiés au privé (eau, déchets, transports, petite enfance), avec gouvernance associant syndicats, collectifs d'usagers et collectivités.",
        "Instaurer la gratuité des premiers mètres cubes d'eau et la tarification progressive pour faire de l'accès à l'eau un droit fondamental effectif.",
    ],

    # ── ÉCONOMIE ──
    "commerce-local": [
        "Soutenir l'artisanat et le commerce de proximité dans le centre-ville et les quartiers, en maîtrisant les locaux commerciaux.",
        "Créer un dispositif de contrôle des baux commerciaux pour plafonner les loyers, favoriser la diversification des commerces et réguler l'implantation.",
    ],
    "emploi-insertion": [
        "Soutenir les projets de relance de l'activité industrielle par les salariés dans le cadre des SCOP et des SCIC.",
        "Conditionner les aides municipales aux entreprises à des engagements clairs : création d'emplois, critères sociaux et environnementaux, implantation durable sur le territoire.",
    ],
    "attractivite": [
        "Développer des coopérations territoriales au sens large (entreprise, artisanat, service public, enseignement).",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Lancer un plan pluriannuel de rénovation des infrastructures culturelles et d'accueil.",
    ],
    "evenements-creation": None,

    # ── SPORT ──
    "equipements-sportifs": [
        "Lancer un plan pluriannuel de rénovation des infrastructures sportives.",
    ],
    "sport-pour-tous": None,

    # ── URBANISME ──
    "amenagement-urbain": [
        "Arrêter les constructions de la phase II de l'écoquartier des Maraîchers pour d'abord améliorer les services, commerces et qualité de vie du quartier existant.",
    ],
    "accessibilite": [
        "Atteindre l'objectif de zéro rue non accessible aux personnes à mobilité réduite d'ici la fin du mandat.",
    ],
    "quartiers-prioritaires": [
        "Garantir l'égalité d'accès aux services de proximité essentiels dans tous les quartiers (crèches, services à la population).",
    ],

    # ── SOLIDARITÉ ──
    "aide-sociale": None,
    "egalite-discriminations": [
        "Faire de l'égalité femmes-hommes et de l'inclusion une priorité transversale du mandat, en coopération avec les partenaires institutionnels et associatifs.",
        "Soutenir les associations favorisant l'inclusion de toutes et tous : femmes, LGBTQIA+, personnes en situation de handicap, personnes racisées, parents isolés.",
        "Féminiser l'espace public : noms de rues, de salles, d'écoles, œuvres d'art.",
        "Revaloriser les métiers féminisés et favoriser l'évolution des carrières au sein de la collectivité.",
    ],
    "pouvoir-achat": [
        "Rendre les transports en commun gratuits pour les moins de 26 ans, les personnes en situation de handicap et les bénéficiaires des minima sociaux.",
        "Instaurer la gratuité des premiers mètres cubes d'eau pour faire de l'accès à l'eau un droit fondamental effectif.",
    ],
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Mettre à jour l'URL du programme
    for c in data["candidats"]:
        if c["id"] == CANDIDAT_ID:
            c["programmeUrl"] = "https://dijonchangedere.fr/"
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
    print(f"  MISE À JOUR — Michel Haberstrau (Dijon)")
    print(f"{'='*55}")
    print(f"  Sous-thèmes mis à jour : {updated}")
    print(f"  Sous-thèmes ajoutés    : {added}")
    print(f"  Total mesures          : {total_mesures}")
    print(f"  JSON écrit : {JSON_PATH}")


if __name__ == "__main__":
    main()
