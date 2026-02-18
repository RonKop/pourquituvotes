#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration des programmes de Stéphane Roudaut et Yves Pagès (Brest 2026).

Sources :
  - Roudaut : stephaneroudaut2026.fr, France Bleu Bretagne, Breizh-Info
  - Pagès   : yvespages2026.fr, France Bleu Bretagne, Breizh-Info, Candidator
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "elections")
JSON_PATH = os.path.join(DATA_DIR, "brest-2026.json")


# ============================================================
# CANDIDAT 1 : Stéphane Roudaut
# ============================================================

ROUDAUT_ID = "roudaut"
ROUDAUT_SOURCE = "Programme officiel 2026"
ROUDAUT_SOURCE_URL = "https://www.stephaneroudaut2026.fr/"
ROUDAUT_SECURITE_URL = "https://www.stephaneroudaut2026.fr/post/s%C3%A9curit%C3%A9-%C3%A0-brest-les-5-engagements-de-st%C3%A9phane-roudaut-pour-une-ville-plus-s%C3%BBre"

ROUDAUT_METADATA = {
    "programmeComplet": True,
    "programmeUrl": "https://www.stephaneroudaut2026.fr/",
}

# 21 mesures mappées aux sous-thèmes
# Note : police-municipale, accessibilite et egalite-discriminations existent déjà → on les met à jour
ROUDAUT_PROPOSITIONS = {
    "securite": {
        "police-municipale": {
            "texte": (
                "Création d'une Police Territoriale unifiée (police municipale, ASVP et brigade intercommunale de transport) "
                "avec objectif de 150 agents armés de proximité, soit 1 agent pour 1 000 habitants. "
                "Patrouilles de quartier 24h/24 le week-end. Missions : lutte contre les incivilités, "
                "sécurisation des écoles, contrôle du stationnement. Budget estimé : 7,5 M€"
            ),
            "source": "Programme officiel 2026 — 5 engagements sécurité",
            "sourceUrl": ROUDAUT_SECURITE_URL,
        },
        "videoprotection": {
            "texte": (
                "Déploiement de 300 points de vidéoprotection (1 000 caméras) dans les zones d'habitation, "
                "zones économiques et bâtiments publics. Création d'un Centre de Supervision Urbain (CSU) "
                "opérationnel 24h/24 pour une gestion intelligente de la sécurité"
            ),
            "source": "Programme officiel 2026 — 5 engagements sécurité",
            "sourceUrl": ROUDAUT_SECURITE_URL,
        },
        "prevention-mediation": {
            "texte": (
                "Doublement du nombre de médiateurs, de 25 à 50, concentrés dans les quartiers prioritaires, "
                "les écoles et les équipements publics. Objectif : 100 % des bailleurs sociaux engagés "
                "dans un programme « tranquillité résidentielle »"
            ),
            "source": "Programme officiel 2026 — 5 engagements sécurité",
            "sourceUrl": ROUDAUT_SECURITE_URL,
        },
        "violences-femmes": {
            "texte": (
                "Plan d'action ambitieux pour faire de Brest une ville pilote en matière de lutte "
                "contre les violences faites aux femmes, intégré à la politique d'égalité femmes-hommes"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": ROUDAUT_SOURCE_URL,
        },
    },
    "transports": {
        "transports-en-commun": {
            "texte": (
                "Amélioration de la desserte des transports en commun sur l'ensemble de la métropole, "
                "en lien avec le projet « Mon Réseau Grandit » et le développement des mobilités douces"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": ROUDAUT_SOURCE_URL,
        },
        "velo-mobilites-douces": {
            "texte": (
                "Développement des mobilités douces : extension du réseau cyclable sécurisé "
                "et encouragement des déplacements actifs dans tous les quartiers de la métropole"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": ROUDAUT_SOURCE_URL,
        },
    },
    "environnement": {
        "climat-adaptation": {
            "texte": (
                "Engagement fort dans la transition écologique pour une ville plus sobre "
                "et adaptée au changement climatique, sujet de prédilection identifié "
                "par le candidat parmi les priorités du mandat"
            ),
            "source": "France Bleu Bretagne, 2026",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-2026-stephane-roudaut-veut-ecrire-une-nouvelle-histoire-pour-brest-3205749",
        },
    },
    "education": {
        "jeunesse": {
            "texte": (
                "Programme jeunesse issu de la consultation de 1 500 habitants : "
                "accompagnement des jeunes dans la cité et développement de l'offre périscolaire et de loisirs"
            ),
            "source": "France Bleu Bretagne, 2026",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-2026-stephane-roudaut-veut-ecrire-une-nouvelle-histoire-pour-brest-3205749",
        },
    },
    "sante": {
        "prevention-sante": {
            "texte": (
                "Politique de prévention santé renforcée, travaillée avec les 16 groupes thématiques "
                "du collectif « Mon Brest », incluant un volet solidarité et accès aux soins"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": ROUDAUT_SOURCE_URL,
        },
    },
    "democratie": {
        "budget-participatif": {
            "texte": (
                "Consultation citoyenne élargie : plus de 1 500 personnes rencontrées via 16 groupes thématiques "
                "(solidarité, sécurité, transitions, etc.) pour co-construire le programme municipal"
            ),
            "source": "France Bleu Bretagne, 2026",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-2026-stephane-roudaut-veut-ecrire-une-nouvelle-histoire-pour-brest-3205749",
        },
        "transparence": {
            "texte": (
                "Gouvernance renouvelée : transparente, collaborative et tournée vers le bien commun. "
                "Financement de la politique de sécurité par une gestion municipale rigoureuse"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": ROUDAUT_SOURCE_URL,
        },
    },
    "culture": {
        "equipements-culturels": {
            "texte": (
                "Action culturelle identifiée comme sujet de prédilection : développement de l'offre culturelle "
                "et des équipements pour faire de Brest une ville où l'on se retrouve et où l'on grandit"
            ),
            "source": "France Bleu Bretagne, 2026",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-2026-stephane-roudaut-veut-ecrire-une-nouvelle-histoire-pour-brest-3205749",
        },
    },
    "urbanisme": {
        "accessibilite": {
            "texte": (
                "Faire de l'inclusion et du handicap la « grande cause » du mandat : "
                "garantir l'accès à tout pour tous, avec une approche transversale "
                "couvrant tous les sujets et compétences de la ville"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": ROUDAUT_SOURCE_URL,
        },
        "quartiers-prioritaires": {
            "texte": (
                "Renforcement de la présence dans les quartiers prioritaires : médiateurs dédiés, "
                "patrouilles de proximité et programme « tranquillité résidentielle » "
                "avec les bailleurs sociaux"
            ),
            "source": "Programme officiel 2026 — 5 engagements sécurité",
            "sourceUrl": ROUDAUT_SECURITE_URL,
        },
    },
    "solidarite": {
        "egalite-discriminations": {
            "texte": (
                "Plan ambitieux pour faire de Brest une ville pionnière en matière d'égalité femmes-hommes : "
                "« L'égalité femmes-hommes ne peut plus être un vœu pieux, "
                "elle doit devenir une réalité quotidienne »"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": ROUDAUT_SOURCE_URL,
        },
    },
    "economie": {
        "attractivite": {
            "texte": (
                "Relancer l'attractivité de Brest et de sa métropole : "
                "une ville plus juste, plus sûre et plus rayonnante, "
                "où les habitants et les entreprises choisissent de s'installer"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": ROUDAUT_SOURCE_URL,
        },
        "emploi-insertion": {
            "texte": (
                "Favoriser l'emploi et l'insertion par le dynamisme économique du territoire, "
                "en s'appuyant sur les conclusions des 16 groupes thématiques de consultation citoyenne"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": ROUDAUT_SOURCE_URL,
        },
    },
    "sport": {
        "sport-pour-tous": {
            "texte": (
                "Développement du sport pour tous dans les quartiers, "
                "en lien avec la politique d'inclusion et d'accessibilité universelle"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": ROUDAUT_SOURCE_URL,
        },
    },
}


# ============================================================
# CANDIDAT 2 : Yves Pagès
# ============================================================

PAGES_ID = "pages"
PAGES_SOURCE = "Programme officiel 2026"
PAGES_SOURCE_URL = "https://yvespages2026.fr/"

PAGES_METADATA = {
    "programmeComplet": True,
    "programmeUrl": "https://yvespages2026.fr/",
}

# 15 engagements mappés aux sous-thèmes
# Note : attractivite existe déjà → on le met à jour
PAGES_PROPOSITIONS = {
    "securite": {
        "police-municipale": {
            "texte": (
                "Création d'une police municipale armée pour Brest, "
                "dernière grande ville de France de plus de 100 000 habitants à ne pas en disposer. "
                "La sécurité au cœur de l'élection municipale"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
        "videoprotection": {
            "texte": (
                "Déploiement massif de la vidéoprotection dans l'ensemble des quartiers de Brest "
                "pour lutter contre la délinquance et les incivilités"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
    },
    "transports": {
        "pietons-circulation": {
            "texte": (
                "Mettre fin à la politique anti-voitures assumée qui a fait de Brest "
                "la 3e grande ville de France où la circulation automobile est la plus difficile, "
                "avec de nombreux bouchons. Rétablir une circulation fluide"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
        "stationnement": {
            "texte": (
                "Restaurer les centaines de places de stationnement sur voirie supprimées "
                "qui ont sinistré le petit commerce de proximité"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
    },
    "economie": {
        "commerce-local": {
            "texte": (
                "Sauver le petit commerce de proximité sinistré par la suppression des places de parking "
                "et accélérer la réouverture des commerces du marché Saint-Louis, "
                "fermés depuis trop longtemps à cause des retards de la municipalité"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
        "attractivite": {
            "texte": (
                "Enrayer le déclin démographique et relancer l'attractivité économique de Brest. "
                "Désenclaver la ville : Brest n'a ni TGV ni autoroute pour rejoindre rapidement Rennes. "
                "Développer le port de commerce, marginal avec 2,8 M de tonnes "
                "(contre 130 M au Havre), relancer le terminal ferroviaire à l'arrêt"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
        "emploi-insertion": {
            "texte": (
                "Lutter contre le chômage (13,7 %) et la pauvreté (19 %, jusqu'à 45 % dans certains quartiers). "
                "Retenir les jeunes talents formés par l'université qui quittent la ville"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
    },
    "urbanisme": {
        "amenagement-urbain": {
            "texte": (
                "Revoir l'aménagement urbain pour rétablir l'équilibre entre piétons, cyclistes et automobilistes. "
                "Mettre fin aux politiques qui ont dégradé la circulation et l'accès au centre-ville"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
        "quartiers-prioritaires": {
            "texte": (
                "Agir dans les quartiers prioritaires où la pauvreté atteint 45 % : "
                "renforcer la sécurité, l'emploi et les services de proximité"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
    },
    "solidarite": {
        "aide-sociale": {
            "texte": (
                "Priorité nationale dans l'accès aux aides sociales et au logement social "
                "pour les Brestois. Maîtrise de l'immigration : Brest est la 2e grande ville de France "
                "où l'immigration a le plus augmenté (+100 % entre 2006 et 2021)"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
        "pouvoir-achat": {
            "texte": (
                "Défendre le pouvoir d'achat des Brestois par une gestion rigoureuse des finances municipales "
                "et la baisse de la pression fiscale locale"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
    },
    "logement": {
        "logement-social": {
            "texte": (
                "Priorité nationale dans l'attribution des logements sociaux. "
                "Rétablir l'ordre et la tranquillité dans les résidences HLM"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
    },
    "education": {
        "jeunesse": {
            "texte": (
                "Retenir les jeunes talents à Brest : créer les conditions pour que les étudiants "
                "et jeunes diplômés trouvent un emploi et choisissent de rester dans la métropole"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
    },
    "democratie": {
        "transparence": {
            "texte": (
                "Renouvellement démocratique : transparence de la gestion municipale "
                "et fin du cumul des fonctions qui concentre trop de pouvoir"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
        "services-publics": {
            "texte": (
                "Améliorer l'efficacité des services publics municipaux "
                "et mettre fin aux retards qui pénalisent les habitants et les commerçants"
            ),
            "source": "Programme officiel 2026",
            "sourceUrl": PAGES_SOURCE_URL,
        },
    },
}


# ============================================================
# MAIN : intégration séquentielle des 2 candidats
# ============================================================

def integrer_candidat(data, candidat_id, metadata, propositions_dict):
    """Intègre les propositions d'un candidat dans le JSON."""
    # 1) Mise à jour des métadonnées du candidat
    found = False
    for candidat in data["candidats"]:
        if candidat["id"] == candidat_id:
            for key, value in metadata.items():
                candidat[key] = value
            print(f"  Métadonnées mises à jour : programmeComplet={candidat['programmeComplet']}")
            found = True
            break
    if not found:
        print(f"  ERREUR : candidat '{candidat_id}' introuvable !")
        return 0

    # 2) Insertion/mise à jour des propositions
    count_new = 0
    count_updated = 0
    count_errors = 0

    for cat in data["categories"]:
        cat_id = cat["id"]
        if cat_id not in propositions_dict:
            continue
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id not in propositions_dict[cat_id]:
                continue
            prop_data = propositions_dict[cat_id][st_id]
            existing = st["propositions"].get(candidat_id)
            if existing is not None:
                count_updated += 1
                action = "MAJ"
            else:
                count_new += 1
                action = "NOUVEAU"
            st["propositions"][candidat_id] = {
                "texte": prop_data["texte"],
                "source": prop_data["source"],
                "sourceUrl": prop_data["sourceUrl"],
            }
            print(f"    [{action}] {cat_id}/{st_id}")

    # 3) Vérification que tous les sous-thèmes ont été trouvés
    for cat_id, subs in propositions_dict.items():
        for st_id in subs:
            found_st = False
            for cat in data["categories"]:
                if cat["id"] == cat_id:
                    for st in cat["sousThemes"]:
                        if st["id"] == st_id:
                            found_st = True
                            break
            if not found_st:
                print(f"    ERREUR : sous-thème {cat_id}/{st_id} introuvable dans le JSON !")
                count_errors += 1

    total = count_new + count_updated
    print(f"  => Nouveau : {count_new}, Mis à jour : {count_updated}, Erreurs : {count_errors}")
    print(f"  => Total sous-thèmes avec propositions : {total}")
    return total


def main():
    print(f"Lecture de {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- Candidat 1 : Roudaut ---
    print("\n" + "=" * 60)
    print("CANDIDAT 1 : Stéphane Roudaut (roudaut)")
    print("=" * 60)
    total_roudaut = integrer_candidat(data, ROUDAUT_ID, ROUDAUT_METADATA, ROUDAUT_PROPOSITIONS)

    # --- Candidat 2 : Pagès ---
    print("\n" + "=" * 60)
    print("CANDIDAT 2 : Yves Pagès (pages)")
    print("=" * 60)
    total_pages = integrer_candidat(data, PAGES_ID, PAGES_METADATA, PAGES_PROPOSITIONS)

    # --- Écriture du JSON ---
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"TERMINÉ ! Fichier écrit : {JSON_PATH}")
    print(f"  Roudaut : {total_roudaut} propositions")
    print(f"  Pagès   : {total_pages} propositions")
    print("=" * 60)


if __name__ == "__main__":
    main()
