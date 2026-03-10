#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction batch 2 : Aulas (Lyon), Pagès (Brest), Rolland (Nantes), Roumegas (Montpellier).
Sources : sites de campagne et presse locale.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


# ============================================================
# AULAS (Lyon) — coeurlyonnais.fr + lyoncapitale.fr
# ============================================================

MESURES_AULAS = {
    "police-municipale": [
        "Création d'une brigade de circulation municipale visible et formée, axée sur la prévention des incivilités et la protection des usagers vulnérables.",
    ],
    "prevention-mediation": [
        "Création d'un centre mobile de médiation de la rue avec médiateurs, agents formés à la désescalade et psychologues urbains.",
        "Élaboration d'une cartographie des tensions urbaines à partir des signalements réels pour guider l'action de terrain.",
        "Adoption d'une Charte lyonnaise du respect urbain, simple, visible et partagée.",
        "Lancement d'une semaine annuelle de la rue apaisée dans tous les arrondissements.",
        "Institution d'un brevet mobilité pour tous les enfants scolarisés à Lyon pour enseigner le civisme dans l'espace public.",
    ],
    "transports-en-commun": [
        "Extension du métro vers l'Est lyonnais : donner à l'Est le métro qu'il mérite.",
        "Maintien de plans ambitieux d'extension du métro vers l'Est et l'Ouest.",
        "Développement d'un réseau de transports en commun fiable, accessible et moderne sans endettement excessif.",
        "Rendre les transports abordables pour les jeunes et les familles.",
    ],
    "pietons-circulation": [
        "Construction d'un nouveau tunnel sous Fourvière de 8 km reliant Valvert à Saint-Fons avec sortie Presqu'île près de Perrache.",
    ],
    "espaces-verts": [
        "Végétalisation de la place Bellecour.",
    ],
    "budget-participatif": [
        "Instauration de référendums annuels sur les grands projets municipaux.",
        "Implication directe des associations et acteurs de terrain dans les décisions.",
    ],
    "commerce-local": [
        "Rétablissement de conditions favorables pour les commerçants et détaillants.",
        "Garantie de l'accessibilité du centre-ville pour le bon fonctionnement des commerces.",
    ],
    "attractivite": [
        "Positionnement de Lyon comme grand pôle économique axé sur l'innovation et la recherche.",
    ],
    "equipements-culturels": [
        "Renforcement de l'identité culturelle lyonnaise : théâtre, opéra, festivals de danse.",
        "Développement d'un grand pôle cinéma autour du projet Lumière.",
        "Restauration majeure du patrimoine de Fourvière.",
    ],
    "jeunesse": [
        "Création d'un pacte de confiance avec la jeunesse lyonnaise avec des opportunités élargies.",
        "Soutien aux programmes culturels, sportifs et associatifs pour les jeunes.",
    ],
    "aide-sociale": [
        "Soutien aux familles monoparentales en difficulté pour concilier travail et garde d'enfants.",
        "Accompagnement des personnes isolées et des jeunes en doute sur leur avenir.",
    ],
    "accessibilite": [
        "Priorité à l'accessibilité pour les personnes handicapées dans les transports et espaces publics.",
    ],
    "emploi-insertion": [
        "Soutien aux entrepreneurs, commerces et industries locales.",
        "Préparation de l'avenir par l'emploi des jeunes et l'attraction des talents.",
    ],
    "renovation-energetique": [
        "Réduction de la pollution par des techniques innovantes sans contraintes idéologiques.",
    ],
}


# ============================================================
# PAGES (Brest) — yvespages2026.fr
# ============================================================

MESURES_PAGES = {
    "police-municipale": [
        "Mise en place d'une police municipale de proximité armée et bien formée : 150 agents recrutés sur 3 ans.",
        "Réouverture des commissariats de quartier pour assurer la présence policière de proximité.",
    ],
    "videoprotection": [
        "Installation de caméras dans tous les quartiers avec un centre de contrôle centralisé connecté à l'IA pour une surveillance continue.",
    ],
    "transports-en-commun": [
        "Connexion de Brest à Rennes par la ligne à grande vitesse et l'autoroute gratuite.",
        "Rétablissement de la liaison aérienne Brest-Orly.",
    ],
    "velo-mobilites-douces": [
        "Création de pistes cyclables séparées et sécurisées sur l'ensemble de la ville.",
    ],
    "pietons-circulation": [
        "Ouverture des couloirs de bus au covoiturage pour fluidifier la circulation.",
    ],
    "stationnement": [
        "Augmentation des places de stationnement en centre-ville et baisse des tarifs horaires pour revitaliser le commerce de proximité.",
    ],
    "logement-social": [
        "Audit des attributions de logements sociaux pour plus de transparence.",
        "Rénovation des logements HLM vacants pour répondre aux milliers de demandeurs en attente.",
    ],
    "acces-logement": [
        "Programme majeur de construction neuve et de renouvellement urbain avec maintien de 25% de logement social.",
    ],
    "cantines-fournitures": [
        "Promotion de cantines scolaires bio et circuits courts dans les écoles.",
    ],
    "espaces-verts": [
        "Plantation d'arbres dans toute la ville et suppression des graffitis.",
    ],
    "proprete-dechets": [
        "Interdiction des sacs plastiques et promotion du recyclage.",
    ],
    "centres-sante": [
        "Création d'une clinique sans rendez-vous pour les patients ne pouvant accéder rapidement à un spécialiste.",
    ],
    "seniors": [
        "Bilans de condition physique gratuits pour les retraités.",
        "Développement de programmes de sport-santé adaptés pour le maintien à domicile des seniors.",
    ],
    "commerce-local": [
        "Baisse des tarifs de stationnement pour revitaliser les petits commerces de centre-ville.",
    ],
    "attractivite": [
        "Captation du trafic conteneurs de la Manche pour dynamiser le port commercial de Brest.",
        "Réouverture du terminal ferroviaire du port.",
        "Soutien à la R&D dans le secteur de l'industrie de défense et rétention des ingénieurs formés localement.",
    ],
    "pouvoir-achat": [
        "Aucune augmentation des impôts locaux, taxes et tarifs municipaux pour protéger le pouvoir d'achat.",
    ],
}


# ============================================================
# ROLLAND (Nantes) — francebleu.fr
# ============================================================

MESURES_ROLLAND = {
    "police-municipale": [
        "Poursuite de l'augmentation des effectifs de police municipale engagée depuis 2020.",
        "Création d'un commissariat dans un quartier prioritaire.",
        "Présence permanente de la police municipale en soirée près du Bouffay et du Hangar à bananes.",
    ],
    "violences-femmes": [
        "Création d'un lieu dédié aux mineurs victimes de violences sexuelles et sexistes.",
    ],
    "transports-en-commun": [
        "Extension de la gratuité des transports en commun à 15 000 usagers supplémentaires (30 000 bénéficiaires actuels).",
        "Déploiement de deux nouvelles lignes de tramway.",
    ],
    "velo-mobilites-douces": [
        "Ajout de 150 km de pistes cyclables supplémentaires sur le réseau nantais.",
    ],
    "stationnement": [
        "Mise en place d'un stationnement à tarif réduit pour les travailleurs en horaires décalés.",
    ],
    "logement-social": [
        "Production de 40% de logements sociaux supplémentaires.",
    ],
    "petite-enfance": [
        "Création de 700 nouvelles places en crèche.",
        "Mise en place d'un service de garde d'urgence pour les parents en situation de crise.",
        "Création d'une plateforme d'accompagnement des familles monoparentales.",
    ],
    "espaces-verts": [
        "Augmentation des espaces verts et de la végétalisation urbaine.",
        "Réduction des surfaces bitumées dans la ville.",
    ],
    "renovation-energetique": [
        "Diminution du parc de logements énergivores (passoires thermiques).",
    ],
}


# ============================================================
# ROUMEGAS (Montpellier) — echo-des-tribunes.com
# ============================================================

MESURES_ROUMEGAS = {
    "police-municipale": [
        "Recrutement de 100 policiers municipaux supplémentaires stationnés dans les quartiers.",
    ],
    "velo-mobilites-douces": [
        "Développement d'un réseau cyclable continu, sécurisé et utile sur l'ensemble de la ville.",
    ],
    "pietons-circulation": [
        "Révision du plan de circulation : réouverture de l'avenue Albert-Dubout et circulation en pétales sur quatre grands boulevards pour réduire le transit en centre-ville.",
    ],
    "logement-social": [
        "Permettre aux locataires de longue durée en logement social d'accéder à la propriété : objectif 4 000 acquisitions par mandat.",
    ],
    "petite-enfance": [
        "Gratuité du périscolaire avec horaires étendus de 7h à 19h.",
    ],
    "cantines-fournitures": [
        "Cantine scolaire gratuite avec horaires d'accueil étendus.",
    ],
    "espaces-verts": [
        "Instauration immédiate du zéro artificialisation nette sur Montpellier, arrêt de l'étalement urbain sur les espaces naturels et agricoles restants.",
    ],
    "centres-sante": [
        "Déploiement de centres de santé dans les quartiers en désert médical.",
    ],
    "prevention-sante": [
        "Création d'une ordonnance verte offrant des paniers bio aux femmes enceintes.",
    ],
    "budget-participatif": [
        "Création de sept parlements de quartier élus disposant d'un réel pouvoir de décision.",
        "Instauration du référendum d'initiative citoyenne au niveau municipal.",
    ],
    "commerce-local": [
        "Ouverture d'épiceries municipales fonctionnant à prix coûtant.",
    ],
    "amenagement-urbain": [
        "Zéro artificialisation nette : protection des espaces naturels et agricoles restants contre l'urbanisation.",
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
    print("  RÉ-EXTRACTION BATCH 2")
    print("=" * 60)

    # AULAS (Lyon)
    print("\n  AULAS (Lyon):")
    update_candidate(
        os.path.join(ROOT_DIR, "data", "elections", "lyon-2026.json"),
        "aulas", MESURES_AULAS,
        "Programme officiel 2026 — Jean-Michel Aulas",
        "https://coeurlyonnais.fr/"
    )

    # PAGES (Brest)
    print("\n  PAGES (Brest):")
    update_candidate(
        os.path.join(ROOT_DIR, "data", "elections", "brest-2026.json"),
        "pages", MESURES_PAGES,
        "Programme officiel 2026 — Yves Pagès",
        "https://yvespages2026.fr/"
    )

    # ROLLAND (Nantes)
    print("\n  ROLLAND (Nantes):")
    update_candidate(
        os.path.join(ROOT_DIR, "data", "elections", "nantes-2026.json"),
        "rolland", MESURES_ROLLAND,
        "Programme officiel 2026 — Johanna Rolland",
        "https://www.francebleu.fr/"
    )

    # ROUMEGAS (Montpellier)
    print("\n  ROUMEGAS (Montpellier):")
    update_candidate(
        os.path.join(ROOT_DIR, "data", "elections", "montpellier-2026.json"),
        "roumegas", MESURES_ROUMEGAS,
        "Programme officiel 2026 — Jean-Louis Roumegas",
        "https://echo-des-tribunes.com/"
    )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
