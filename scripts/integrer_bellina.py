#!/usr/bin/env python3
"""
Intégration du programme de Julia Bellina (Amiens au Coeur) dans le comparateur municipal.
Source : https://amiensaucoeur.fr/priorites/ et https://amiensaucoeur.fr/convictions/
"""

import json
import os
import sys

# Chemin vers le JSON Amiens
JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "data", "elections", "amiens-2026.json")

CANDIDAT_ID = "bellina"
SOURCE = "Programme officiel 2026"
SOURCE_URL = "https://amiensaucoeur.fr/priorites/"
SOURCE_URL_CONVICTIONS = "https://amiensaucoeur.fr/convictions/"

# Mapping des propositions de Bellina par sous-thème
# Extrait de https://amiensaucoeur.fr/priorites/ (10 priorités) et /convictions/
PROPOSITIONS = {
    # === SÉCURITÉ ===
    "police-municipale": {
        "texte": "Recruter 30 nouveaux policiers municipaux, armement immédiat de la police municipale, patrouilles renforcées dans les quartiers et aux abords des établissements scolaires, tolérance zéro pour les incivilités et violences urbaines",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "videoprotection": {
        "texte": "Installation de 50 nouvelles caméras de surveillance, vidéosurveillance intelligente dans tous les points sensibles, caméras avec intelligence artificielle pour détecter les infractions et identifier les contrevenants aux dépôts sauvages",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "prevention-mediation": {
        "texte": "Verbalisation systématique des infractions et des incivilités, application ferme de la réglementation pour une ville apaisée",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    # violences-femmes : pas de proposition spécifique

    # === TRANSPORTS ===
    "transports-en-commun": {
        "texte": "Amélioration des transports en commun pour réduire les coûts de déplacement, transport public décarboné progressif",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "velo-mobilites-douces": {
        "texte": "Développement des mobilités douces dont la marche à qui elle veut redonner toute sa place, développement du covoiturage municipal et des mobilités partagées",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    # pietons-circulation : pas de proposition spécifique distincte
    "stationnement": {
        "texte": "Gratuité étendue du stationnement courte durée en centre-ville, pérennisation de la gratuité du stationnement pour les soignants à domicile (de 350€ à 1€ par an), facilitation du stationnement pour l'accès aux services",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "tarifs-gratuite": {
        "texte": "Tarification sociale renforcée pour les familles modestes (restauration scolaire, activités périscolaires), gratuité étendue pour certains services essentiels",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # === LOGEMENT ===
    # logement-social : pas de proposition spécifique
    # logements-vacants : pas de proposition spécifique
    # encadrement-loyers : pas de proposition spécifique
    "acces-logement": {
        "texte": "Reconquête du parc de logements anciens, compétence habitat exercée via la présidence unifiée ville-métropole pour une politique cohérente du logement",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL_CONVICTIONS
    },

    # === ÉDUCATION ===
    "petite-enfance": {
        "texte": "Espaces de jeux sécurisés et équipements sportifs de proximité pour les plus jeunes, politique familiale globale pour tous les âges",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    # ecoles-renovation : pas de proposition spécifique
    "cantines-fournitures": {
        "texte": "Amélioration de la restauration scolaire avec circuits courts et bio, refonte de la tarification, objectif de 50% de bio et circuits courts dans la restauration collective",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "periscolaire-loisirs": {
        "texte": "Activités périscolaires innovantes dans tous les quartiers pour apprendre aux jeunes à aimer Amiens, tarification sociale renforcée pour les activités périscolaires",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "jeunesse": {
        "texte": "Politique familiale globale avec 25% de la population amiénoise de moins de 25 ans : services adaptés, espaces de jeux sécurisés et équipements sportifs de proximité dans tous les quartiers",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # === ENVIRONNEMENT ===
    "espaces-verts": {
        "texte": "Développement accéléré de la plantation d'arbres pour faire baisser la température en ville, espaces verts préservés et végétalisation urbaine généralisée",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "proprete-dechets": {
        "texte": "Service de nettoiement quotidien dans tous les quartiers (fin des opérations propreté ponctuelles), lutte contre les dépôts sauvages avec caméras intelligentes et IA, tournées optimisées et équipes renforcées, application mobile citoyenne pour signaler les problèmes",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "climat-adaptation": {
        "texte": "Objectif neutralité carbone municipale d'ici 2040, acceptation pleine de la réalité scientifique du réchauffement climatique dans les décisions municipales",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "renovation-energetique": {
        "texte": "Rénovation énergétique des bâtiments municipaux, réduction de 30% de la consommation énergétique des bâtiments publics",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "alimentation-durable": {
        "texte": "Développer un réseau de maraîchage solidaire sur des parcelles municipales, marchés de producteurs locaux pour des prix plus accessibles, circuits courts alimentaires dans la restauration collective",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # === SANTÉ ===
    # centres-sante : pas de proposition spécifique
    # prevention-sante : pas de proposition spécifique
    "seniors": {
        "texte": "Création du Conseil des Sages municipal pour donner une voix institutionnelle aux aînés, services de maintien à domicile renforcés, lutte contre l'isolement avec des programmes de lien social, accessibilité universelle aux équipements publics",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # === DÉMOCRATIE ===
    "budget-participatif": {
        "texte": "Consultations citoyennes régulières sur les grands projets, droit de pétition pour les habitants sur les sujets municipaux, consultation citoyenne sur les grands investissements",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "transparence": {
        "texte": "Publication intégrale et publique des déclarations d'intérêts et de patrimoine, attribution transparente des subventions selon des critères objectifs, comptes-rendus publics de toutes les décisions municipales, publication détaillée de tous les postes budgétaires, aucun adjoint ne pourra se porter candidat à une autre élection pendant le mandat",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "vie-associative": {
        "texte": "Attribution transparente des subventions aux associations selon des critères objectifs et publics, appliqués de manière équitable pour éviter toute forme de clientélisme",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL_CONVICTIONS
    },
    "services-publics": {
        "texte": "Adoption de l'intelligence artificielle « Albert » pour transformer l'efficacité des services municipaux : réduction des délais de réponse, service 24h/24 pour les demandes courantes, guichet unique, prise de rendez-vous en ligne, réponse garantie sous 48h, services mobiles pour les personnes à mobilité réduite",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # === ÉCONOMIE ===
    "commerce-local": {
        "texte": "Soutien renforcé aux commerces de proximité, préservation de la zone piétonne commerciale, reprendre la main sur le laisser-aller du centre-ville commercial, lutte contre la vie chère en favorisant la concurrence commerciale",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "emploi-insertion": {
        "texte": "Attraction d'entreprises innovantes dans les secteurs d'avenir, soutien aux créateurs d'entreprises avec des dispositifs d'accompagnement, anticiper les besoins de formation, poursuivre le soutien aux employeurs du territoire",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "attractivite": {
        "texte": "Amiens doit retrouver son rang de capitale économique des Hauts-de-France en s'appuyant sur ses atouts géographiques entre Paris, Bruxelles et Londres, développement de l'écosystème universitaire avec l'UPJV",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },

    # === CULTURE ===
    # equipements-culturels : pas de proposition spécifique
    # evenements-creation : pas de proposition spécifique

    # === SPORT ===
    "equipements-sportifs": {
        "texte": "Espaces de jeux sécurisés et équipements sportifs de proximité dans tous les quartiers",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    # sport-pour-tous : pas de proposition spécifique distincte

    # === URBANISME ===
    "amenagement-urbain": {
        "texte": "Gouvernance unifiée maire-présidente de métropole pour une vision cohérente de l'aménagement urbain, compétences structurantes concentrées : développement économique, aménagement, mobilité, habitat",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    "accessibilite": {
        "texte": "Accessibilité universelle aux équipements publics, services mobiles pour les personnes à mobilité réduite, accompagnement numérique pour les moins familiers des outils digitaux, horaires d'ouverture étendus adaptés aux contraintes professionnelles",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
    # quartiers-prioritaires : pas de proposition spécifique

    # === SOLIDARITÉ ===
    # aide-sociale : pas de proposition spécifique distincte
    # egalite-discriminations : pas de proposition spécifique
    "pouvoir-achat": {
        "texte": "Engagement formel de ne pas augmenter les impôts locaux pendant tout le mandat, tarification sociale renforcée pour les familles modestes, réduction des coûts administratifs par l'automatisation intelligente, plateforme d'échange de services entre Amiénois, réseau de maraîchage solidaire pour des légumes à meilleur prix dans les écoles",
        "source": SOURCE,
        "sourceUrl": SOURCE_URL
    },
}


def main():
    # Charger le JSON
    print(f"Chargement de {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Trouver le candidat bellina et mettre à jour ses metadata
    candidat_found = False
    for candidat in data["candidats"]:
        if candidat["id"] == CANDIDAT_ID:
            candidat_found = True
            candidat["programmeUrl"] = "https://amiensaucoeur.fr/"
            # 29 propositions concrètes >= 15 => programmeComplet = true
            candidat["programmeComplet"] = True
            print(f"Candidat '{candidat['nom']}' trouvé, programmeComplet = True")
            break

    if not candidat_found:
        print(f"ERREUR: Candidat '{CANDIDAT_ID}' non trouvé dans le JSON!")
        sys.exit(1)

    # Insérer les propositions dans chaque sous-thème
    nb_inserts = 0
    nb_updated = 0
    nb_themes_total = 0

    for categorie in data["categories"]:
        for sous_theme in categorie["sousThemes"]:
            nb_themes_total += 1
            st_id = sous_theme["id"]

            if st_id in PROPOSITIONS:
                prop = PROPOSITIONS[st_id]
                old_value = sous_theme["propositions"].get(CANDIDAT_ID)

                sous_theme["propositions"][CANDIDAT_ID] = prop

                if old_value is None:
                    nb_inserts += 1
                    print(f"  + [{categorie['id']}] {st_id}: INSÉRÉ")
                else:
                    nb_updated += 1
                    print(f"  ~ [{categorie['id']}] {st_id}: MIS À JOUR")
            else:
                # Garder null si pas de proposition
                if CANDIDAT_ID not in sous_theme["propositions"]:
                    sous_theme["propositions"][CANDIDAT_ID] = None

    # Sauvegarder
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"RÉSULTAT:")
    print(f"  Sous-thèmes totaux:   {nb_themes_total}")
    print(f"  Propositions insérées: {nb_inserts}")
    print(f"  Propositions mises à jour: {nb_updated}")
    print(f"  Sous-thèmes remplis:  {nb_inserts + nb_updated} / {nb_themes_total}")
    print(f"  programmeComplet:     True")
    print(f"  programmeUrl:         https://amiensaucoeur.fr/")
    print(f"\nJSON sauvegardé: {JSON_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
