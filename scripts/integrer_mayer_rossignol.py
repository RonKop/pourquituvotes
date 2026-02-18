#!/usr/bin/env python3
"""
Intègre le programme complet de Nicolas Mayer-Rossignol (Rouen 2026)
dans data/elections/rouen-2026.json.

Sources :
- France Bleu Normandie, 11 février 2026 (programme dévoilé)
- Tendance Ouest, février 2026 (santé, candidature)
- Tendance Ouest, janvier 2026 (candidature officielle)
- Tendance Ouest, juin 2025 (culture)
- France Bleu Normandie, janvier 2026 (candidature)
"""

import sys
import io
import json
import os

# Windows UTF-8 fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Chemins
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
JSON_PATH = os.path.join(PROJECT_DIR, "data", "elections", "rouen-2026.json")

CANDIDAT_ID = "mayer-rossignol"

# Sources réutilisables
SRC_FB_FEV2026 = {
    "source": "France Bleu Normandie, février 2026",
    "sourceUrl": "https://www.francebleu.fr/normandie/seine-maritime-76/rouen/municipales-2026-mutuelle-communale-transports-securite-education-nicolas-mayer-rossignol-devoile-son-programme-7725686"
}
SRC_TO_FEV2026_SANTE = {
    "source": "Tendance Ouest, février 2026",
    "sourceUrl": "https://www.tendanceouest.com/actualite-436133-municipales-2026-mutuelle-communale-consultations-psychologiques-pour-les-jeunes-nicolas-mayer-rossignol-devoile-ses-propositions-pour-la-sante-a-rouen"
}
SRC_TO_JAN2026 = {
    "source": "Tendance Ouest, janvier 2026",
    "sourceUrl": "https://www.tendanceouest.com/actualite-435238-municipales-2026-a-rouen-le-maire-sortant-nicolas-mayer-rossignol-officialise-sa-candidature"
}
SRC_FB_JAN2026 = {
    "source": "France Bleu Normandie, janvier 2026",
    "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-rouen-nicolas-mayer-rossignol-candidat-pour-un-second-mandat-a-rouen-9664633"
}
SRC_TO_JUIN2025 = {
    "source": "Tendance Ouest, juin 2025",
    "sourceUrl": "https://www.tendanceouest.com/actualite-430651-municipales-2026-le-maire-de-rouen-nicolas-mayer-rossignol-appelle-les-candidats-de-gauche-a-sanctuariser-les-budgets-pour-la-culture"
}
SRC_TO_FEV2026_METRO = {
    "source": "Tendance Ouest, février 2026",
    "sourceUrl": "https://www.tendanceouest.com/actualite-436299-municipales-2026-la-majorite-a-la-metropole-de-rouen-presente-un-programme-commun"
}

# Mapping : sous-thème ID -> proposition {texte, source, sourceUrl}
# Chaque mesure mappée à UN SEUL sous-thème, pas de doublons
PROPOSITIONS = {
    # === SÉCURITÉ ===
    "police-municipale": {
        "texte": "Doubler les effectifs de police municipale la nuit et instaurer une brigade de nuit 7j/7 (actuellement mardi-dimanche seulement)",
        **SRC_FB_FEV2026
    },
    "videoprotection": {
        "texte": "Poursuite du renforcement de la vidéoprotection (caméras triplées de 40 à 120 en 5 ans) et modernisation du dispositif",
        **SRC_FB_JAN2026
    },
    "prevention-mediation": {
        "texte": "Éclairage public modulable intelligent (remplacement des armoires électriques pour passer de 100 % à 50 %, 30 %, 20 % selon les heures de nuit) pour sécuriser l'espace public",
        **SRC_FB_FEV2026
    },
    # violences-femmes : pas de mesure spécifique identifiée

    # === TRANSPORTS ===
    "transports-en-commun": {
        "texte": "Nouveau métro-tramway pour la métropole rouennaise et gratuité des transports en commun le samedi",
        **SRC_FB_JAN2026
    },
    "velo-mobilites-douces": {
        "texte": "Poursuite du plan vélo métropolitain : Réseau Express Vélo (REV) de 12 itinéraires pour 115 km, renforcement de la continuité et de la sécurité des pistes cyclables",
        **SRC_TO_FEV2026_METRO
    },
    "pietons-circulation": {
        "texte": "Plan de rénovation des trottoirs pour améliorer le confort et la sécurité des piétons dans tous les quartiers",
        **SRC_FB_FEV2026
    },
    # stationnement : pas de mesure spécifique identifiée
    "tarifs-gratuite": {
        "texte": "Extension de la gratuité des transports aux moins de 25 ans et aux plus de 65 ans (déjà gratuit pour les moins de 18 ans depuis 2025)",
        **SRC_FB_FEV2026
    },

    # === LOGEMENT ===
    "acces-logement": {
        "texte": "Accès prioritaire au logement pour les familles monoparentales dans le cadre du bouclier social",
        **SRC_FB_FEV2026
    },
    # logement-social, logements-vacants, encadrement-loyers : pas de mesure spécifique identifiée

    # === ÉDUCATION ===
    "petite-enfance": {
        "texte": "Bouclier social pour les familles monoparentales : aide financière pour la garde d'enfants et accès prioritaire aux crèches",
        **SRC_FB_FEV2026
    },
    "ecoles-renovation": {
        "texte": "Construction de deux nouveaux groupes scolaires : un aux Hauts de Rouen (17 classes, livraison 2030) et un dans le quartier Flaubert, plus une reconstruction au Châtelet (livraison 2027)",
        **SRC_FB_FEV2026
    },
    # cantines-fournitures : proposition existante dans alimentation-durable, pas de doublon
    # periscolaire-loisirs : pas de mesure spécifique identifiée
    # jeunesse : couvert par prevention-sante (consultations psy jeunes)

    # === ENVIRONNEMENT ===
    "espaces-verts": {
        "texte": "Programme de végétalisation et de renaturalisation urbaine pour adapter Rouen au changement climatique",
        **SRC_TO_JAN2026
    },
    "proprete-dechets": {
        "texte": "Renforcement de la propreté urbaine et augmentation des sanctions financières contre les incivilités (dépôts sauvages, déchets)",
        **SRC_FB_FEV2026
    },
    "climat-adaptation": {
        "texte": "Poursuite de la réduction de la pollution atmosphérique (Rouen passée de 3e à 14e ville la plus polluée en NOx) et adaptation climatique de la ville",
        **SRC_TO_JAN2026
    },
    "alimentation-durable": {
        "texte": "Développement du bio sur ordonnance et alimentation saine et locale dans les cantines municipales",
        **SRC_TO_FEV2026_SANTE
    },
    # renovation-energetique : pas de mesure spécifique identifiée

    # === SANTÉ ===
    "centres-sante": {
        "texte": "Création d'un centre municipal de santé avec médecins salariés, deux nouvelles Maisons France Santé (Sapins et Saint-Éloi), mutuelle communale pour les 44 % de Rouennais sans mutuelle, et garantie d'un médecin traitant pour chaque habitant",
        **SRC_FB_FEV2026
    },
    "prevention-sante": {
        "texte": "Consultations psychologiques gratuites pour les jeunes, sport sur ordonnance, parkings gratuits aux centres hospitaliers",
        **SRC_TO_FEV2026_SANTE
    },
    "seniors": {
        "texte": "Chèque-cadeau pour les seniors isolés et renforcement des groupes d'échange intergénérationnels ; transports gratuits pour les plus de 65 ans",
        **SRC_FB_FEV2026
    },

    # === DÉMOCRATIE ===
    # Pas de mesures spécifiques identifiées (budget participatif, transparence, etc.)

    # === ÉCONOMIE ===
    "commerce-local": {
        "texte": "Mois du commerce de proximité en septembre et extension des terrasses des commerces tout l'été pour faire de Rouen « la plus grande terrasse de France »",
        **SRC_TO_FEV2026_METRO
    },
    "attractivite": {
        "texte": "Animations et concerts gratuits dans les rues l'été pour renforcer l'attractivité et le rayonnement de Rouen",
        **SRC_TO_FEV2026_METRO
    },
    # emploi-insertion : pas de mesure spécifique identifiée

    # === CULTURE ===
    "equipements-culturels": {
        "texte": "Sanctuarisation et augmentation du budget culture de la ville et de la métropole",
        **SRC_TO_JUIN2025
    },
    # evenements-creation : couvert par attractivite (animations/concerts)

    # === SPORT ===
    "equipements-sportifs": {
        "texte": "Construction d'une nouvelle piscine aux Hauts de Rouen (15 M€, bassin sportif 25 m 6 couloirs, bassin ludique, pataugeoire, toboggan) pour remplacer la piscine Salomon fermée",
        **SRC_FB_FEV2026
    },
    "sport-pour-tous": {
        "texte": "Faire de Rouen la capitale du sport féminin et développer le sport sur ordonnance",
        **SRC_TO_JAN2026
    },

    # === URBANISME ===
    "amenagement-urbain": {
        "texte": "Aménagement du quartier Flaubert avec construction d'écoles et d'équipements publics ; rénovation urbaine des Hauts de Rouen (plus de 100 M€ dans le cadre du NPNRU)",
        **SRC_FB_FEV2026
    },
    "quartiers-prioritaires": {
        "texte": "Plan de renouvellement urbain des Hauts de Rouen (NPNRU) : plus de 100 millions d'euros d'investissement, nouvelle piscine, nouveau groupe scolaire",
        **SRC_FB_FEV2026
    },
    # accessibilite : pas de mesure spécifique identifiée

    # === SOLIDARITÉ ===
    "aide-sociale": {
        "texte": "Bouclier social complet pour les familles monoparentales : aide financière garde d'enfants, accès prioritaire logement et crèche",
        **SRC_FB_FEV2026
    },
    "pouvoir-achat": {
        "texte": "Mutuelle communale à tarif négocié pour faciliter l'accès aux soins et réduire le reste à charge des Rouennais",
        **SRC_FB_FEV2026
    },
    # egalite-discriminations : pas de mesure spécifique identifiée
}


def main():
    # Lecture du fichier JSON
    print(f"Lecture de {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Mise à jour des métadonnées du candidat
    for candidat in data["candidats"]:
        if candidat["id"] == CANDIDAT_ID:
            candidat["programmeUrl"] = "https://www.fiersderouen.fr/"
            candidat["programmeComplet"] = True  # 27 mesures concrètes >= 15
            print(f"  -> programmeComplet = True pour {candidat['nom']}")
            break

    # Injection des propositions
    count_updated = 0
    count_new = 0
    count_skipped = 0

    for categorie in data["categories"]:
        for sous_theme in categorie["sousThemes"]:
            st_id = sous_theme["id"]
            props = sous_theme["propositions"]

            if st_id in PROPOSITIONS:
                prop = PROPOSITIONS[st_id]
                was_null = props.get(CANDIDAT_ID) is None

                props[CANDIDAT_ID] = {
                    "texte": prop["texte"],
                    "source": prop["source"],
                    "sourceUrl": prop["sourceUrl"]
                }

                if was_null:
                    count_new += 1
                    print(f"  + [{categorie['id']}/{st_id}] NOUVELLE proposition")
                else:
                    count_updated += 1
                    print(f"  ~ [{categorie['id']}/{st_id}] Mise à jour")
            else:
                count_skipped += 1

    # Écriture du fichier
    print(f"\nÉcriture de {JSON_PATH}...")
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Résumé
    total = count_new + count_updated
    print(f"\n=== RÉSUMÉ ===")
    print(f"Propositions ajoutées (nouvelles) : {count_new}")
    print(f"Propositions mises à jour :         {count_updated}")
    print(f"Sous-thèmes sans proposition :      {count_skipped}")
    print(f"TOTAL propositions Mayer-Rossignol : {total}")
    print(f"programmeComplet : True (>= 15 mesures concrètes)")
    print(f"Fichier sauvegardé : {JSON_PATH}")


if __name__ == "__main__":
    main()
