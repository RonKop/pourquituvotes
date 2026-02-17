#!/usr/bin/env python3
"""Intègre les propositions de Bell-Lloch et Tmimi dans vitry-sur-seine-2026.json"""

import json
import os

FILEPATH = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\vitry-sur-seine-2026.json"

# Propositions Bell-Lloch (13)
BELL_LLOCH_PROPS = {
    "amenagement-urbain": {
        "texte": "Nouveau cœur de ville : 5 600 m² d'espaces verts, nouveaux commerces, terrasses, les 3 cinés Robespierre revisités et parking souterrain rénové",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "logement-social": {
        "texte": "Construction de 2 000 logements tout en préservant les zones pavillonnaires, avec des logements sociaux rénovés",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "prevention-mediation": {
        "texte": "Création d'une équipe de médiateurs de proximité urbaine et développement concerté de la vidéoverbalisation",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "espaces-verts": {
        "texte": "Création d'un grand parc en bord de Seine d'au moins 50 000 m² pour réconcilier la ville avec son fleuve",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "equipements-culturels": {
        "texte": "Construction d'un complexe festif moderne pour les familles, mariages, anniversaires et rencontres citoyennes",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "seniors": {
        "texte": "Construction d'une nouvelle résidence sénior adaptée aux besoins et au confort des aînés",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "proprete-dechets": {
        "texte": "Création d'une déchetterie-ressourcerie, vidéoverbalisation et mobilisation citoyenne pour une ville plus propre",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "vie-associative": {
        "texte": "Réouverture de la maison sociale du Moulin Vert et ouverture de deux nouvelles salles municipales associatives",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "emploi-insertion": {
        "texte": "Création d'une régie publique de quartier pour l'insertion professionnelle et préparation de l'installation de 1 000 emplois",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "periscolaire-loisirs": {
        "texte": "Étude de la possibilité de rendre gratuite l'heure d'étude scolaire après la classe",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "commerce-local": {
        "texte": "Création d'un nouveau marché au quartier Jean Jaurès proposant des produits issus de circuits courts à tarifs abordables",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "renovation-energetique": {
        "texte": "Ouverture d'un site de géothermie pour chauffer les habitations et faire baisser durablement les factures d'énergie",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    },
    "evenements-creation": {
        "texte": "Rendre l'accès à la culture totalement gratuit pour tous les jeunes Vitriots de moins de 26 ans",
        "source": "pbl2026.fr",
        "sourceUrl": "https://pbl2026.fr/programme.html"
    }
}

# Propositions Tmimi (22)
TMIMI_PROPS = {
    "climat-adaptation": {
        "texte": "Déminéraliser les sols, isoler le bâti et blanchir les surfaces pour l'objectif Vitry zéro carbone en 2050",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "espaces-verts": {
        "texte": "Planter des milliers d'arbres, créer des îlots de fraîcheur, jardins partagés et vergers urbains",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "proprete-dechets": {
        "texte": "Campagne pour la réduction des déchets, développer recycleries, circuits courts, ateliers de réparation",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "transports-en-commun": {
        "texte": "Interdire la circulation des poids lourds en ville, création d'une navette interquartier gratuite",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "velo-mobilites-douces": {
        "texte": "Plan vélo ambitieux, promotion de la marche, partage de l'espace public",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "logement-social": {
        "texte": "Maintenir un taux minimum de 40% de logements sociaux, investir dans la rénovation du parc existant",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "encadrement-loyers": {
        "texte": "Encadrer les loyers, soutenir l'habitat coopératif et social",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "renovation-energetique": {
        "texte": "Rénovation énergétique prioritaire, améliorer la performance du parc de logements",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "budget-participatif": {
        "texte": "Budgets participatifs, référendums locaux, conseils de quartier indépendants dotés de pouvoir",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "transparence": {
        "texte": "Charte éthique pour chaque élu, combattre le clientélisme, supprimer les avantages indus des élus",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "services-publics": {
        "texte": "Service public communal en régies publiques : eau, énergie, santé, propreté, transport, restauration scolaire",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "petite-enfance": {
        "texte": "Ville à hauteur d'enfant : crèches accessibles, cantines bio et locales progressivement gratuites",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "cantines-fournitures": {
        "texte": "Cantines de plus en plus bio et locales, avec options végétariennes",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "jeunesse": {
        "texte": "Appui réel aux adolescents : orientation, stages, apprentissage, emploi, logement, mobilité",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "prevention-sante": {
        "texte": "Ouverture d'un deuxième CMPP pour la santé mentale des jeunes",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "seniors": {
        "texte": "Maintien à domicile, solutions intergénérationnelles, ouverture d'un deuxième EHPAD",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "centres-sante": {
        "texte": "Renforcer le Centre municipal de santé et ouvrir des antennes de proximité",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "vie-associative": {
        "texte": "Égalité de traitement et transparence dans l'attribution des salles et subventions aux associations",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "egalite-discriminations": {
        "texte": "Observatoire local des discriminations et violences sexistes, lutte contre racisme, sexisme, LGBTQIphobies",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "amenagement-urbain": {
        "texte": "Quartier des Ardoines : quartier écologique au service des habitants, outil foncier solidaire",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "pietons-circulation": {
        "texte": "Créer des lieux de rencontre, placettes, rues piétonnes, espaces publics vivants",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    },
    "alimentation-durable": {
        "texte": "Jardins partagés, vergers urbains, agriculture urbaine, circuits courts",
        "source": "vitry2026.fr",
        "sourceUrl": "https://vitry2026.fr/"
    }
}

def main():
    # Charger le JSON
    with open(FILEPATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Mettre à jour programmeUrl pour bell-lloch et tmimi
    for candidat in data["candidats"]:
        if candidat["id"] == "bell-lloch":
            candidat["programmeUrl"] = "https://pbl2026.fr/programme.html"
        elif candidat["id"] == "tmimi":
            candidat["programmeUrl"] = "https://vitry2026.fr/"

    # Compteurs pour vérification
    bell_lloch_count = 0
    tmimi_count = 0

    # Parcourir toutes les catégories et sous-thèmes
    for categorie in data["categories"]:
        for sous_theme in categorie["sousThemes"]:
            st_id = sous_theme["id"]

            # Bell-Lloch
            if st_id in BELL_LLOCH_PROPS:
                sous_theme["propositions"]["bell-lloch"] = BELL_LLOCH_PROPS[st_id]
                bell_lloch_count += 1

            # Tmimi
            if st_id in TMIMI_PROPS:
                sous_theme["propositions"]["tmimi"] = TMIMI_PROPS[st_id]
                tmimi_count += 1

    # Vérification
    print(f"Bell-Lloch : {bell_lloch_count}/13 propositions insérées")
    print(f"Tmimi : {tmimi_count}/22 propositions insérées")

    if bell_lloch_count != 13:
        print(f"ATTENTION : Bell-Lloch attendu 13, trouvé {bell_lloch_count}")
    if tmimi_count != 22:
        print(f"ATTENTION : Tmimi attendu 22, trouvé {tmimi_count}")

    # Sauvegarder
    with open(FILEPATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Fichier sauvegardé : {FILEPATH}")

if __name__ == "__main__":
    main()
