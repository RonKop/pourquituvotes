#!/usr/bin/env python3
"""
Mise à jour Payet (Saint-Denis Réunion) — compléments sécurité et culture
envoyés par Giovanni Payet le 3 mars 2026.
"""
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

CANDIDAT_ID = "payet"
FICHIER = os.path.join(os.path.dirname(__file__), '..', 'data', 'elections', 'saint-denis-reunion-2026.json')

# Nouvelles mesures à AJOUTER (compléments au programme existant)
# On garde les mesures existantes et on ajoute celles qui manquent
NOUVELLES_MESURES = {
    # === SÉCURITÉ ===
    "police-municipale": [
        # existant: "Travailler main dans la main avec la Police Municipale..."
        # ajout:
        "Mettre en place un Contrat de Sécurité Intégré renforçant la coopération entre police municipale, police nationale, État et justice",
        "Créer une Réserve Communale de Sécurité Civile mobilisant des citoyens volontaires pour appuyer les secours et la gestion de crise",
    ],
    "videoprotection": [
        "Déployer le Plan Lumières : éclairage public massif pour sécuriser les trajets nocturnes et réduire le sentiment d'insécurité",
    ],
    "prevention-mediation": [
        # existant: app Saint-Denis Tranquille + 100 zafer ki dékon'
        # ajout:
        "Créer un réseau de médiateurs scolaires faisant le lien entre écoles, familles et quartiers pour prévenir la délinquance juvénile",
        "Prioriser la présence humaine et la médiation directement dans les quartiers, en complément des outils numériques",
    ],

    # === CULTURE ===
    "equipements-culturels": [
        # existant: candidature UNESCO
        # ajout:
        "Créer un Centre d'interprétation de l'architecture et du patrimoine (CIAP) multisites et renforcer les archives communales",
        "Transformer l'ancienne prison Juliette Dodu en lieu culturel vivant",
        "Reconvertir l'ancien Hôtel de Ville en lieu culturel structurant",
        "Renforcer le réseau de lecture publique et accueillir le Centre régional du livre à Saint-Denis",
        "Développer le dispositif « De l'écran au livre » pour ancrer les pratiques culturelles dans tous les quartiers",
        "Dimensionner l'école de musique et de danse Loulou Pitou à l'échelle de la commune",
    ],
    "evenements-creation": [
        # existant: festivités Saint-Denis 360
        # ajout:
        "Créer une biennale FONNKER valorisant poésie, oralité, fonnker, slam et création contemporaine",
        "Mettre en place un conventionnement pluriannuel pour cinq compagnies culturelles structurantes",
        "Développer un réseau d'écobox culturels et accompagner les tiers-lieux culturels",
        "Protéger et valoriser le street art dans une logique de musée à ciel ouvert",
        "Soutenir les pratiques amateurs : danse urbaine, maloya, percussions et arts émergents",
        "Intégrer le 1 % culturel dans les rénovations scolaires pour garantir l'éducation artistique à chaque jeune",
    ],

    # Mesures qui relèvent d'autres sous-thèmes
    "amenagement-urbain": [
        "Lancer le Plan ANBELI : transformer les « quartiers-béton » en « quartiers-jardins » avec espaces publics végétalisés et entretenus",
    ],
    "accessibilite": [
        "Réactiver la Commission Communale d'Accessibilité pour garantir la circulation sans risque des personnes en situation de handicap",
    ],
    "alimentation-durable": [
        "Expérimenter une Sécurité Sociale de l'Alimentation garantissant que chaque Dionysien puisse manger à sa faim",
    ],
}


def main():
    with open(FICHIER, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Vérifier que le candidat existe
    candidat = None
    for c in data['candidats']:
        if c['id'] == CANDIDAT_ID:
            candidat = c
            break
    if not candidat:
        print(f"ERREUR: candidat '{CANDIDAT_ID}' non trouvé")
        sys.exit(1)

    ajoutees = 0
    deja_presentes = 0

    for cat in data['categories']:
        for st in cat['sousThemes']:
            st_id = st['id']
            if st_id not in NOUVELLES_MESURES:
                continue

            props = st.setdefault('propositions', {})
            if CANDIDAT_ID not in props or not props[CANDIDAT_ID]:
                props[CANDIDAT_ID] = {"mesures": []}
            if 'mesures' not in props[CANDIDAT_ID]:
                props[CANDIDAT_ID]['mesures'] = []

            existantes = props[CANDIDAT_ID]['mesures']
            for nouvelle in NOUVELLES_MESURES[st_id]:
                # Vérifier si une mesure très similaire existe déjà (début de phrase)
                debut = nouvelle[:40].lower()
                doublon = False
                for e in existantes:
                    if e[:40].lower() == debut:
                        doublon = True
                        deja_presentes += 1
                        break
                if not doublon:
                    existantes.append(nouvelle)
                    ajoutees += 1

    # Sauvegarder
    with open(FICHIER, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Compter le total
    total = 0
    st_count = 0
    for cat in data['categories']:
        for st in cat['sousThemes']:
            props = st.get('propositions', {})
            if CANDIDAT_ID in props and props[CANDIDAT_ID] and props[CANDIDAT_ID].get('mesures'):
                total += len(props[CANDIDAT_ID]['mesures'])
                st_count += 1

    print(f"=== Mise à jour Payet (Saint-Denis Réunion) ===")
    print(f"Mesures ajoutées   : {ajoutees}")
    print(f"Déjà présentes     : {deja_presentes}")
    print(f"Total mesures      : {total}")
    print(f"Sous-thèmes        : {st_count}/44")


if __name__ == '__main__':
    main()
