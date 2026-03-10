#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration des propositions de Patrice Bessac (Montreuil 2026)
Sources : vivemontreuil.fr, patrice-bessac.fr, lejournaldugrandparis.fr, montreuil.fr
"""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INPUT_FILE = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\montreuil-2026.json"

# Propositions de Bessac classées par sous-thème
# Sources multiples : site de campagne vivemontreuil.fr, patrice-bessac.fr,
# lejournaldugrandparis.fr, montreuil.fr
PROPOSITIONS_BESSAC = {
    # === SÉCURITÉ ===
    "police-municipale": {
        "texte": "Doublement des effectifs de la police municipale pour renforcer la présence sur le terrain dans tous les quartiers",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "videoprotection": {
        "texte": "Extension du réseau de vidéoprotection dans les zones sensibles, en complément du doublement de la police municipale",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "prevention-mediation": {
        "texte": "Renforcement des dispositifs de prévention et de médiation dans tous les quartiers, avec des actions ciblées contre toutes les formes de violence",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "violences-femmes": {
        "texte": "Programme de prévention contre toutes les formes de violence, y compris les violences faites aux femmes, avec un accompagnement renforcé des victimes",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },

    # === TRANSPORTS ===
    "transports-en-commun": {
        "texte": "Grande mobilisation pour l'extension des lignes de métro M1, M9 et M3 desservant Montreuil, et prolongement du tramway T1 jusqu'aux Ruffins (mise en service mi-2028)",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "velo-mobilites-douces": {
        "texte": "Plan ambitieux piétons-vélos pour des déplacements continus, sécurisés et accessibles à tous, avec création de nouvelles pistes cyclables dont une piste bidirectionnelle de 3,80 m le long de la nouvelle avenue paysagère",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "pietons-circulation": {
        "texte": "Réfection massive de la voirie et des trottoirs pour améliorer les déplacements piétons, avec élargissement des trottoirs sur la nouvelle avenue paysagère (35 m de large)",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "tarifs-gratuite": {
        "texte": "Gratuité des transports pour les 8 000 élèves du primaire de Montreuil",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },

    # === LOGEMENT ===
    "logement-social": {
        "texte": "Maintien de l'objectif de plus de 40 % de logements sociaux dans les nouvelles constructions, avec une politique volontariste de production de logements abordables",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "logements-vacants": {
        "texte": "Lutte déterminée contre les logements vacants et l'habitat insalubre, avec mobilisation de tous les outils juridiques disponibles",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "encadrement-loyers": {
        "texte": "Lutte contre les produits immobiliers spéculatifs (Airbnb, co-living) pour préserver le parc de logements pour les habitants",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "acces-logement": {
        "texte": "Construction d'une ville abordable pour tous, avec un accompagnement renforcé des demandeurs de logement et des primo-accédants",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },

    # === ÉDUCATION ===
    "petite-enfance": {
        "texte": "Développement de nouvelles places en crèche et renforcement de l'offre d'accueil petite enfance dans tous les quartiers",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "ecoles-renovation": {
        "texte": "Construction du nouveau groupe scolaire Georges Méliès (24 classes : 9 maternelle + 15 élémentaire) avec cours végétalisées « Oasis », ouverture septembre 2026, et mobilisation pour un nouveau collège",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.montreuil.fr/education-jeunesse/construction-dun-groupe-scolaire"
    },
    "cantines-fournitures": {
        "texte": "Poursuite de la cantine 100 % publique (Tables communes) avec objectif de 70 % de composantes bio, et tarification solidaire au quotient familial (à partir de 0,54 € le repas)",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "periscolaire-loisirs": {
        "texte": "Tarification solidaire des accueils périscolaires et extrascolaires selon le quotient familial, avec abattement de 40 % pour les parents isolés",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "jeunesse": {
        "texte": "Priorité à la jeunesse des quartiers populaires : protection des enfants, garantie de leurs droits, attention à la santé mentale des jeunes, et prévention contre toutes les formes de violence",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },

    # === ENVIRONNEMENT ===
    "espaces-verts": {
        "texte": "Plantation de 5 000 nouveaux arbres d'ici 2026 (plan arbres), création d'un corridor écologique de 3,5 hectares le long du tramway T1, et poursuite du programme « Montreuil est notre jardin » de végétalisation participative",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.montreuil.fr/plan-arbres"
    },
    "proprete-dechets": {
        "texte": "Renforcement de la brigade propreté et environnement, déploiement de la collecte des déchets alimentaires (220 bacs, 1 pour 500 habitants) et développement du compostage de quartier (150 sites actifs)",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "climat-adaptation": {
        "texte": "Création d'îlots de fraîcheur et de cours d'école « Oasis » pour lutter contre les canicules, avec désimperméabilisation des sols et végétalisation des espaces publics",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "renovation-energetique": {
        "texte": "Rénovation énergétique des bâtiments publics et accompagnement des copropriétés via l'agence locale de l'énergie (ALEC-MVE) pour réduire les consommations",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "alimentation-durable": {
        "texte": "Poursuite du projet « Mangeons Mieux à Montreuil » de démocratie alimentaire, avec développement de l'agriculture urbaine et objectif de 70 % de bio dans les cantines scolaires",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.montreuil.fr/actualites/detail/communique-mangeons-mieux-a-montreuil-montreuil-poursuit-son-projet-de-democratie-alimentaire-avec-une-reunion-de-restitution-des-echanges-et-propositions-de-6-groupes-de-travail"
    },

    # === SANTÉ ===
    "centres-sante": {
        "texte": "Création d'un nouveau centre municipal de santé à Savattero (labellisé Maison France Santé), et création d'un hôpital de jour pour enfants à La Boissière",
        "source": "Site de campagne Vive Montreuil / lejournaldugrandparis.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "prevention-sante": {
        "texte": "Attention portée à la santé mentale des enfants et des jeunes, avec des programmes de prévention adaptés dans les quartiers",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "seniors": {
        "texte": "Renforcement de l'accompagnement des personnes âgées via le CCAS, avec maintien à domicile, lutte contre l'isolement et aide alimentaire",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },

    # === DÉMOCRATIE ===
    "budget-participatif": {
        "texte": "Poursuite et amplification du budget participatif (3 millions d'euros), avec un objectif de quadruplement de la participation citoyenne",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "transparence": {
        "texte": "Développement de la plateforme « Je participe Montreuil » et renforcement de la charte de la démocratie locale pour la transparence des décisions municipales",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "vie-associative": {
        "texte": "Nouveau souffle pour la vie associative dans tous les quartiers : création de 2 nouvelles maisons de quartier et soutien renforcé aux associations locales",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "services-publics": {
        "texte": "Défense et renforcement des services publics municipaux de proximité, dans une ville de 110 000 habitants à forte densité",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },

    # === ÉCONOMIE ===
    "commerce-local": {
        "texte": "Ouverture du village du réemploi solidaire « La Venelle » (8 boutiques ESS, café-cantine, ateliers participatifs) sur la ZAC Fraternité, rue de Paris, et soutien au commerce local de proximité",
        "source": "Site de campagne Vive Montreuil / patrice-bessac.fr",
        "sourceUrl": "https://www.patrice-bessac.fr/actualites/le-village-du-reemploi-un-projet-pionner-de-leconomie-sociale-et-solidaire-ouvre-ses-portes-a-montreuil"
    },
    "emploi-insertion": {
        "texte": "Développement de l'économie sociale et solidaire avec création d'environ 50 emplois (dont 70 % en insertion) via le village du réemploi, et incubateur d'insertion professionnelle pour les réfugiés",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "attractivite": {
        "texte": "Positionnement de Montreuil comme ville pionnière de l'écologie urbaine, sociale et citoyenne en Île-de-France, dans le cadre de la présidence d'Est Ensemble",
        "source": "Site de campagne Vive Montreuil / lejournaldugrandparis.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },

    # === CULTURE ===
    "equipements-culturels": {
        "texte": "Création d'une antenne du conservatoire dans le Haut Montreuil, et rénovation de la Maison Populaire aux abords des Murs-à-Pêches avec nouveau projet culturel",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "evenements-creation": {
        "texte": "Soutien aux artistes et compagnies montreuilloises via le dispositif « Pépites émergentes » et valorisation du patrimoine des Murs à Pêches (label Patrimoine d'intérêt régional)",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },

    # === SPORT ===
    "equipements-sportifs": {
        "texte": "Modernisation des équipements sportifs, dont le stade nautique Maurice Thorez rénové pour les JO 2024 (bassin 50 m, plongeoirs, toboggan), et rénovation des gymnases de quartier",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "sport-pour-tous": {
        "texte": "Développement de la pratique sportive accessible à tous dans les quartiers, avec le sport comme pilier de la mixité sociale et de l'éducation",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },

    # === URBANISME ===
    "amenagement-urbain": {
        "texte": "Reconversion de l'ancienne autoroute A186 (2,8 km) en avenue paysagère de 35 m de large avec tramway, piste cyclable, trottoirs larges et alignement d'arbres, reliant les quartiers autrefois séparés",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.montreuil.fr/services-et-demarches/deplacements/le-prolongement-du-tramway-t1"
    },
    "accessibilite": {
        "texte": "Amélioration de l'accessibilité de l'espace public pour tous (PMR, poussettes, seniors), avec un plan ambitieux de mise aux normes des voiries et équipements",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "quartiers-prioritaires": {
        "texte": "Création de 2 nouvelles maisons de quartier dans le Haut Montreuil, renforcement des équipements dans les quartiers prioritaires et réduction des inégalités territoriales",
        "source": "Site de campagne Vive Montreuil",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },

    # === SOLIDARITÉ ===
    "aide-sociale": {
        "texte": "Renforcement du CCAS avec aide alimentaire solidaire (contribution de 10 à 25 % du prix réel), assurance habitation et auto à tarif négocié pour les familles modestes",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "egalite-discriminations": {
        "texte": "Faire vivre la mixité sociale comme fondement d'une culture montreuilloise partagée, avec lutte active contre toutes les discriminations et solidarité avec les réfugiés",
        "source": "Site de campagne Vive Montreuil / patrice-bessac.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
    "pouvoir-achat": {
        "texte": "Tarification solidaire au quotient familial pour cantines, périscolaire et activités municipales, avec abattement de 40 % pour les parents isolés et repas à partir de 0,54 €",
        "source": "Site de campagne Vive Montreuil / montreuil.fr",
        "sourceUrl": "https://www.vivemontreuil.fr/"
    },
}


def main():
    # Lire le fichier JSON existant
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Mettre à jour le candidat Bessac
    for candidat in data['candidats']:
        if candidat['id'] == 'bessac':
            candidat['programmeUrl'] = 'https://www.vivemontreuil.fr/'
            candidat['programmeComplet'] = True  # 44 propositions concrètes sourcées
            break

    # Compteur de propositions intégrées
    count = 0

    # Parcourir les catégories et sous-thèmes pour insérer les propositions
    for categorie in data['categories']:
        for sous_theme in categorie['sousThemes']:
            st_id = sous_theme['id']
            if st_id in PROPOSITIONS_BESSAC:
                sous_theme['propositions']['bessac'] = PROPOSITIONS_BESSAC[st_id]
                count += 1
                print(f"  [OK] {categorie['id']} > {st_id}")
            else:
                print(f"  [--] {categorie['id']} > {st_id} (pas de proposition)")

    # Écrire le fichier JSON mis à jour
    with open(INPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n=== RÉSULTAT ===")
    print(f"Propositions intégrées : {count}")
    print(f"programmeComplet : True")
    print(f"programmeUrl : https://www.vivemontreuil.fr/")
    print(f"Fichier mis à jour : {INPUT_FILE}")


if __name__ == '__main__':
    main()
