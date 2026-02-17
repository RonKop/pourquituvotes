#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complète les propositions de Christophe Bouchet (Tours) à partir de
tourspourtous.fr/#propositions (56 propositions officielles).
Met à jour tours-2026.json avec les 34 propositions manquantes.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "tours-2026.json")

SOURCE = "Programme Christophe Bouchet, Tours pour tous, 2026"
SOURCE_URL = "https://tourspourtous.fr/#propositions"

def make_prop(texte):
    return {"texte": texte, "source": SOURCE, "sourceUrl": SOURCE_URL}

# === UPDATES: sous-thèmes où Bouchet a déjà une entrée (texte enrichi) ===
UPDATES = {
    "police-municipale": make_prop(
        "Augmenter de 30 % les effectifs de police municipale, avec extension de leurs "
        "prérogatives au maximum légal, patrouilles mixtes police municipale/nationale, "
        "rondes nocturnes régulières et demander la construction d'une nouvelle prison de 350 cellules"
    ),
    "videoprotection": make_prop(
        "Installer 100 nouvelles caméras de vidéosurveillance par an dans les zones sensibles, "
        "équiper les horodateurs de bornes d'urgence connectées au CSU"
    ),
    "prevention-mediation": make_prop(
        "Verbaliser systématiquement les trottinettes et vélos en infraction sur les trottoirs, "
        "installer des radars pédagogiques dans les zones scolaires et agir pour la prévention "
        "de la délinquance juvénile"
    ),
    "transports-en-commun": make_prop(
        "Réduire le tracé de la 2e ligne de tramway au tronçon gare-hôpital Trousseau, "
        "réinvestir l'économie estimée à 200 M€ dans les équipements municipaux, "
        "mettre en place une navette rapide entre Tours et Saint-Pierre-des-Corps "
        "et créer une brigade métropolitaine des transports"
    ),
    "pietons-circulation": make_prop(
        "Rouvrir le pont Wilson à la circulation automobile dans le sens nord-sud, "
        "fluidifier les livraisons en centre-ville et améliorer la synchronisation des feux de circulation"
    ),
    "proprete-dechets": make_prop(
        "Assermenter les agents de propreté pour verbaliser les incivilités, "
        "lancer un plan de dératisation renforcé et sanctionner la présence de bacs à ordures sur les trottoirs"
    ),
    "climat-adaptation": make_prop(
        "Supprimer l'extinction nocturne de l'éclairage public, convertir l'ensemble du parc en LED "
        "et installer davantage de bornes de recharge pour véhicules électriques"
    ),
    "espaces-verts": make_prop(
        "Ouvrir des parcs à chiens dédiés, développer les parterres fleuris "
        "et améliorer le bien-être animal dans la ville"
    ),
    "amenagement-urbain": make_prop(
        "Reprendre le schéma de transformation des bords de Loire, développer l'accès au fleuve "
        "et lancer un plan de lutte contre le bruit"
    ),
    "logement-social": make_prop(
        "Renforcer les aides à l'amélioration de l'habitat avec la ville comme guichet unique "
        "et permettre l'achat des logements sociaux par leurs occupants"
    ),
    "ecoles-renovation": make_prop(
        "Poursuivre le plan écoles avec les rénovations scolaires, construire une école dans le "
        "quartier Deux-Lions, soutenir les sorties scolaires avec une aide aux enseignants "
        "et sécuriser le parcours des AESH"
    ),
    "centres-sante": make_prop(
        "Créer une mutuelle communale, installer des cabines de téléconsultation "
        "et offrir un stationnement gratuit pour les professionnels de santé"
    ),
    "prevention-sante": make_prop(
        "Soutenir le projet du nouvel hôpital Trousseau, revaloriser les salaires du personnel "
        "hospitalier et créer une maison métropolitaine du sport-santé"
    ),
    "vie-associative": make_prop(
        "Organiser des permanences mobiles dans les quartiers et maintenir un budget stable "
        "pour les associations"
    ),
    "services-publics": make_prop(
        "Moderniser les équipements de nettoyage de la ville (500 000 €/an), publier un calendrier "
        "de nettoyage des rues consultable par les citoyens et nommer un médiateur municipal"
    ),
    "commerce-local": make_prop(
        "Dynamiser le commerce local en lien avec la propreté et la sécurité, "
        "fluidifier les livraisons en centre-ville et créer un village d'artisans"
    ),
    "equipements-culturels": make_prop(
        "Construire une Arena multifonctionnelle de 7 000 à 10 000 places "
        "et rénover les équipements culturels majeurs de la ville"
    ),
    "attractivite": make_prop(
        "Repenser la place de la gare de Tours et l'îlot Vinci, développer l'incubateur MAME, "
        "construire une auberge de jeunesse, soutenir les grandes filières économiques du territoire, "
        "faire de Tours la capitale des châteaux de la Loire, développer l'activité de l'aéroport "
        "et créer un centre de ressources et d'information sur l'IA"
    ),
    "transparence": make_prop(
        "Garantir 0 % d'augmentation de la fiscalité municipale sur le mandat "
        "et publier des propositions intégralement chiffrées"
    ),
}

# === NEW: sous-thèmes où Bouchet était null ===
NEW_ENTRIES = {
    "petite-enfance": make_prop(
        "Ouvrir des crèches à horaires décalés et créer un espace-temps de répit pour les parents"
    ),
    "periscolaire-loisirs": make_prop(
        "Proposer des temps périscolaires plus éducatifs"
    ),
    "acces-logement": make_prop(
        "Développer le bail réel solidaire pour favoriser l'accession à la propriété"
    ),
    "logements-vacants": make_prop(
        "Rétablir les aides au ravalement de façades pour les propriétaires"
    ),
    "aide-sociale": make_prop(
        "Lancer un plan contre l'isolement des personnes vulnérables"
    ),
    "evenements-creation": make_prop(
        "Développer une culture hors les murs et organiser un Mondial des guinguettes"
    ),
    "emploi-insertion": make_prop(
        "Diminuer la Cotisation Foncière des Entreprises (CFE) pour soutenir les professionnels locaux"
    ),
    "jeunesse": make_prop(
        "Rétablir le Conseil municipal des jeunes"
    ),
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    added = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            sid = st["id"]
            props = st["propositions"]

            if sid in UPDATES:
                old = props.get("bouchet")
                props["bouchet"] = UPDATES[sid]
                if old is None:
                    added += 1
                    print(f"  + {sid}: AJOUTÉ")
                else:
                    updated += 1
                    print(f"  ~ {sid}: MIS À JOUR")

            elif sid in NEW_ENTRIES:
                if props.get("bouchet") is None:
                    props["bouchet"] = NEW_ENTRIES[sid]
                    added += 1
                    print(f"  + {sid}: AJOUTÉ")
                else:
                    print(f"  ? {sid}: déjà rempli, skip")

    # Mettre programmeComplet à true (56 propositions officielles)
    for c in data["candidats"]:
        if c["id"] == "bouchet":
            c["programmeComplet"] = True
            c["programmeUrl"] = "https://tourspourtous.fr/#propositions"
            print(f"\n  programmeComplet -> true")
            print(f"  programmeUrl -> https://tourspourtous.fr/#propositions")
            break

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n  Résultat: {updated} mis à jour, {added} ajoutés")
    print(f"  Total propositions Bouchet: {updated + added}")


if __name__ == "__main__":
    main()
