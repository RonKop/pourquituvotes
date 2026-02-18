#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du programme de François Cuillandre (Brest 2026).

Candidat : François Cuillandre, PS / Union gauche (9 formations), maire sortant
Programme : 60 mesures (livret 32 pages) + 84 mesures complémentaires

Sources :
  - France Bleu Bretagne (article 60 mesures, 9 fév 2026)
  - France 3 Bretagne (police municipale, jan 2026)
  - France Bleu (brigade tranquillité, jan 2026)
  - PS29 / UESR29 (accord PS-Écologistes)
  - Site officiel lagaucheuniepourbrest.fr / brest-ensemble.fr
"""

import json
import os
import sys
import io

# Fix encoding Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "elections")
JSON_PATH = os.path.join(DATA_DIR, "brest-2026.json")

CANDIDAT_ID = "cuillandre"

# Source principale : article France Bleu 60 mesures
SOURCE_FB_60 = "France Bleu, fév. 2026"
URL_FB_60 = "https://www.francebleu.fr/bretagne/finistere-29/brest/municipales-2026-a-brest-francois-cuillandre-devoile-son-programme-en-60-mesures-9898818"

# Source police municipale
SOURCE_F3 = "France 3 Bretagne, 2026"
URL_F3 = "https://france3-regions.franceinfo.fr/bretagne/finistere/brest/elections-municipales-2026-le-maire-de-brest-et-candidat-francois-cuillandre-veut-creer-une-police-municipale-de-50-agents-3277367.html"

SOURCE_FB_POLICE = "France Bleu, 2026"
URL_FB_POLICE = "https://www.francebleu.fr/emissions/l-info-d-ici-ici-breizh-izel/municipales-2026-a-brest-francois-cuillandre-promet-une-police-municipale-2030517"

# Source accord PS-Écologistes
SOURCE_PS29 = "PS29 / Accord PS-Écologistes, 2026"
URL_PS29 = "https://www.ps29.org/actualite/la-gauche-unie-pour-brest-socialistes-et-ecologistes-scellent-un-accord-pour-2026/"

# Site officiel campagne
SOURCE_OFFICIEL = "Programme officiel La gauche unie pour Brest, 2026"
URL_OFFICIEL = "https://lagaucheuniepourbrest.fr/"

# Métadonnées à mettre à jour
CUILLANDRE_METADATA = {
    "programmeComplet": True,
    "programmeUrl": "https://lagaucheuniepourbrest.fr/",
    "liste": "La gauche unie pour Brest (PS/EELV/PCF/PRG/UDB/Génération.s/GRS/Parti radical/NFP)",
}

# ============================================================
# 22 propositions mappées aux sous-thèmes communs
# ============================================================
# On remplace les entrées existantes (souvent vagues / a_verifier)
# par des mesures précises issues du programme de 60 mesures.

CUILLANDRE_PROPOSITIONS = {
    "securite": {
        "police-municipale": {
            "texte": (
                "Création d'une police municipale de proximité de 50 agents, "
                "équipés d'armes non létales (bâtons, menottes, bombes lacrymogènes) "
                "et de caméras-piétons. Coût estimé : 3 M\u20ac/an. "
                "Missions : prévention des tensions, lutte contre les incivilités, "
                "présence humaine et dialogue dans tous les quartiers"
            ),
            "source": SOURCE_F3,
            "sourceUrl": URL_F3,
        },
        "videoprotection": {
            "texte": (
                "Renforcement de la brigade de tranquillité urbaine à 25 agents "
                "et installation de nouvelles caméras de vidéoprotection "
                "pour répondre aux attentes croissantes des Brestois en matière de sécurité"
            ),
            "source": SOURCE_FB_POLICE,
            "sourceUrl": URL_FB_POLICE,
        },
        "prevention-mediation": {
            "texte": (
                "Renforcement de la prévention et de la médiation dans les quartiers, "
                "en complément de la police municipale. Approche fondée sur le dialogue, "
                "la présence humaine et la coordination entre tous les acteurs de la tranquillité publique"
            ),
            "source": SOURCE_FB_60,
            "sourceUrl": URL_FB_60,
        },
    },
    "transports": {
        "transports-en-commun": {
            "texte": (
                "Création d'une ligne de bus Est-Ouest via le boulevard de l'Europe réaménagé. "
                "Expérimentation d'une ligne de bateau-bus reliant le Moulin Blanc, "
                "le port de commerce et la plage de Sainte-Anne du Portzic. "
                "Construction d'un ascenseur urbain reliant la Carène au square Beautemps-Beaupré (gare)"
            ),
            "source": SOURCE_FB_60,
            "sourceUrl": URL_FB_60,
        },
        "velo-mobilites-douces": {
            "texte": (
                "Grand plan vélo de 30 millions d'euros : extension du réseau cyclable sécurisé, "
                "développement des mobilités douces dans tous les quartiers de la métropole"
            ),
            "source": SOURCE_FB_60,
            "sourceUrl": URL_FB_60,
        },
        "tarifs-gratuite": {
            "texte": (
                "Pass transport à 10 euros par mois pour tous les jeunes de moins de 26 ans"
            ),
            "source": SOURCE_FB_60,
            "sourceUrl": URL_FB_60,
        },
    },
    "logement": {
        "logement-social": {
            "texte": (
                "Plan d'urgence de 4 millions d'euros supplémentaires par an "
                "pour le logement social, afin de réduire les délais d'attente "
                "et augmenter l'offre de logements accessibles"
            ),
            "source": SOURCE_FB_60,
            "sourceUrl": URL_FB_60,
        },
        "acces-logement": {
            "texte": (
                "Ville accueillante où il est facile de se loger : "
                "soutien au logement et à l'habitat durable, "
                "lutte contre les logements vacants et accompagnement des primo-accédants"
            ),
            "source": SOURCE_OFFICIEL,
            "sourceUrl": URL_OFFICIEL,
        },
    },
    "education": {
        "petite-enfance": {
            "texte": (
                "Création de nouvelles places en crèches pour répondre aux besoins "
                "des familles brestoises et faciliter la conciliation vie professionnelle / vie familiale"
            ),
            "source": SOURCE_FB_60,
            "sourceUrl": URL_FB_60,
        },
        "cantines-fournitures": {
            "texte": (
                "Plan Alimentaire Territorial : objectif 100 % de produits bio, frais et locaux "
                "dans les cantines scolaires d'ici la fin du mandat. "
                "Renforcement de l'éducation à l'alimentation dans les écoles"
            ),
            "source": SOURCE_PS29,
            "sourceUrl": URL_PS29,
        },
    },
    "environnement": {
        "espaces-verts": {
            "texte": (
                "Construction d'une ville plus verte : protection et valorisation de la rade de Brest, "
                "développement des espaces verts et de la biodiversité urbaine, "
                "poursuite du contrat de rade signé en 2022"
            ),
            "source": SOURCE_OFFICIEL,
            "sourceUrl": URL_OFFICIEL,
        },
        "climat-adaptation": {
            "texte": (
                "Engagement renforcé dans la transition écologique : ville plus sobre "
                "et adaptée au changement climatique, mesures fortes pour l'écologie "
                "issues de l'accord avec les Écologistes"
            ),
            "source": SOURCE_PS29,
            "sourceUrl": URL_PS29,
        },
        "alimentation-durable": {
            "texte": (
                "Création d'un fonds en faveur des exploitations urbaines respectueuses de l'environnement, "
                "d'un incubateur de maraîchage et d'une ferme urbaine bio et pédagogique. "
                "Développement du Plan Alimentaire Territorial"
            ),
            "source": SOURCE_PS29,
            "sourceUrl": URL_PS29,
        },
    },
    "democratie": {
        "budget-participatif": {
            "texte": (
                "Poursuite et renforcement du budget participatif (saison 5 en cours, "
                "enveloppe portée à 2 millions d'euros) : les habitants imaginent et votent "
                "des projets d'intérêt général pour leur ville et leur quartier"
            ),
            "source": SOURCE_OFFICIEL,
            "sourceUrl": URL_OFFICIEL,
        },
        "transparence": {
            "texte": (
                "Gouvernance plus collective et moins verticale, "
                "redistribution des responsabilités au sein de la majorité. "
                "Agir au service des Brestois, à leur écoute et en toute transparence"
            ),
            "source": SOURCE_PS29,
            "sourceUrl": URL_PS29,
        },
        "vie-associative": {
            "texte": (
                "Soutien au tissu associatif brestois : chacun dispose d'une place "
                "pour s'engager dans une ville où il est possible de s'épanouir. "
                "Développement de la participation citoyenne dans tous les quartiers"
            ),
            "source": SOURCE_OFFICIEL,
            "sourceUrl": URL_OFFICIEL,
        },
    },
    "economie": {
        "attractivite": {
            "texte": (
                "Favoriser le dynamisme économique et culturel du territoire. "
                "Développer des espaces permettant aux habitants de se rencontrer, créer et célébrer. "
                "Relancer l'attractivité de Brest et de sa métropole"
            ),
            "source": SOURCE_OFFICIEL,
            "sourceUrl": URL_OFFICIEL,
        },
    },
    "culture": {
        "equipements-culturels": {
            "texte": (
                "Construction de deux salles culturelles de proximité "
                "dans les quartiers Europe et Saint-Pierre. "
                "Gratuité des médiathèques pour tous les Brestois"
            ),
            "source": SOURCE_FB_60,
            "sourceUrl": URL_FB_60,
        },
    },
    "sport": {
        "equipements-sportifs": {
            "texte": (
                "Construction du nouveau stade Arkéa Park (15 000 places) "
                "pour remplacer le stade Francis-Le Blé. "
                "Équipement multifonctionnel : sport, loisirs, restauration, bureaux"
            ),
            "source": SOURCE_FB_60,
            "sourceUrl": URL_FB_60,
        },
    },
    "solidarite": {
        "aide-sociale": {
            "texte": (
                "Consolidation des politiques sociales : renforcement des solidarités "
                "pour réduire les inégalités. Projet fondé sur la solidarité, "
                "la qualité de vie dans les quartiers et l'accès de tous à l'essentiel"
            ),
            "source": SOURCE_OFFICIEL,
            "sourceUrl": URL_OFFICIEL,
        },
        "egalite-discriminations": {
            "texte": (
                "Engagement pour l'égalité femmes-hommes comme priorité du mandat : "
                "la première adjointe sera issue des rangs écologistes, "
                "plan d'action transversal pour une ville pionnière en matière d'égalité"
            ),
            "source": SOURCE_PS29,
            "sourceUrl": URL_PS29,
        },
    },
}


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

    print("\n" + "=" * 60)
    print("CANDIDAT : François Cuillandre (cuillandre)")
    print("Programme : 60 mesures + 84 complémentaires")
    print("=" * 60)

    total = integrer_candidat(data, CANDIDAT_ID, CUILLANDRE_METADATA, CUILLANDRE_PROPOSITIONS)

    # Écriture du JSON
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"TERMINÉ ! Fichier écrit : {JSON_PATH}")
    print(f"  Cuillandre : {total} propositions intégrées")
    print(f"  programmeComplet = True (60 mesures >= seuil de 15)")
    print("=" * 60)


if __name__ == "__main__":
    main()
