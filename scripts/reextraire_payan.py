#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction de Benoît Payan (Marseille)

Source   : Programme Pour Marseille 2026 + articles presse
URL      : https://www.pourmarseille.fr/
Date     : 2026-02-25
Mesures source : ~80 mesures identifiées dans les sources
Mesures extraites : 75 mesures mappées ci-dessous

Sources multiples :
- https://www.pourmarseille.fr/
- https://madeinmarseille.net/actualite/196062-municipales-2026-la-grande-interview-de-benoit-payan-et-ses-nouveaux-projets-pour-marseille/
- https://madeinmarseille.net/politique/municipales-2026/196724-transports-littoral-boulodrome-couvert-benoit-payan-devoile-son-programme/
- https://maritima.fr/actualites/politique/marseille/11629/municipales-2026-a-marseille-benoit-payan-devoile-son-plan-de-bataille-pour-une-ville-qui-protege
- https://www.francebleu.fr/provence-alpes-cote-d-azur/bouches-du-rhone-13/marseille/municipales-2026-a-marseille-benoit-payan-annonce-un-plan-proprete-et-assure-que-la-salete-n-est-pas-une-fatalite-4457723
- https://marsactu.fr/breve_de_campagne/benoit-payan-et-le-printemps-marseillais-presentent-les-grandes-lignes-de-leur-programme/
- https://madeinmarseille.net/actualite/194860-regie-publique-de-leau-et-mutuelle-municipale-au-programme-du-printemps-marseillais/
"""

import io
import json
import os
import sys

# Force UTF-8 pour Windows (cp1252 fix)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# === CONFIGURATION ===
CANDIDAT_ID = "payan"
VILLE_ID = "marseille-2026"
SOURCE = "Programme Pour Marseille 2026 — Benoît Payan"
SOURCE_URL = "https://www.pourmarseille.fr/"

JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", f"{VILLE_ID}.json")

# === MESURES ===
MESURES = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Doublement des effectifs de la police municipale de Marseille, passés de 400 à 800 agents.",
        "Objectif d'atteindre 1 600 policiers municipaux d'ici 2033.",
        "Création de 10 nouvelles antennes de police municipale d'ici la fin du mandat 2032.",
        "Création d'un commissariat de police municipale dans chaque arrondissement.",
    ],
    "videoprotection": [
        "Extension du réseau de vidéoprotection avec déploiement continu de caméras de surveillance.",
        "500 caméras de vidéoprotection installées lors du mandat précédent, poursuite du déploiement.",
    ],
    "prevention-mediation": [
        "Création d'une police de la propreté de 80 agents, placée sous le commandement de la police municipale, habilitée à dresser des PV.",
        "Lutte contre le narcotrafic : faire de Marseille la vitrine nationale de la lutte contre le narcotrafic, en lien avec le parquet national antistupéfiants.",
    ],

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Extension du tramway Nord jusqu'à La Bricarde, au-delà de la Castellane.",
        "Prolongement du tramway Belle-de-Mai jusqu'à Saint-Jérôme.",
        "Extension du tramway Est en direction de Saint-Loup et La Barasse.",
        "Extension du tramway Sud jusqu'à La Rouvière, après La Gaye.",
        "Refonte intégrale de la carte des bus selon la logique urbaine et les besoins des habitants.",
        "Élargissement des horaires de transports en commun le soir et le week-end.",
        "Développement de solutions de transport lourd pour désenclaver les quartiers Nord et Est.",
        "Billet unique métropolitain intégrant les gares ferroviaires au réseau urbain.",
        "Création d'une Société du Grand Marseille pour porter les grands projets de transport et d'aménagement.",
    ],
    "velo-mobilites-douces": [
        "Déploiement de davantage de vélos en libre-service comme alternative de mobilité.",
        "Suppression des trottinettes en libre-service si les conditions d'usage ne sont pas respectées.",
    ],
    "pietons-circulation": [
        "Renégociation des tarifs des tunnels Prado Carénage et Prado Sud.",
        "Tarif réduit à 1 euro par traversée du tunnel avec abonnement régulier.",
    ],
    "tarifs-gratuite": [
        "Gratuité des transports en commun pour les moins de 26 ans.",
        "Gratuité des transports en commun pour les demandeurs d'emploi.",
        "Étude de la gratuité totale des transports en commun en analysant les coûts réels.",
    ],

    # ── LOGEMENT ──
    "logement-social": [
        "Objectif de produire 4 500 logements par an dont 2 300 logements sociaux.",
        "Programme massif de réhabilitation de l'habitat indigne à Marseille : 5 000 logements indignes réhabilités.",
    ],
    "logements-vacants": [
        "Lutte contre les logements vacants dans le cadre du programme de réhabilitation massive.",
    ],
    "encadrement-loyers": [
        "Mise en place de l'encadrement des loyers à Marseille.",
        "Permis de louer renforcé avec contrôle triennal de l'état des logements.",
    ],
    "acces-logement": [
        "Création d'une assurance habitation municipale à tarifs négociés.",
    ],

    # ── ÉDUCATION ──
    "petite-enfance": [
        "Renforcement de l'offre de petite enfance et création de nouvelles places en crèche.",
    ],
    "ecoles-renovation": [
        "Poursuite du Plan écoles avec rénovation et modernisation de 188 écoles sur 15 ans.",
    ],
    "cantines-fournitures": [
        "Cantine gratuite pour 15 000 enfants marseillais chaque jour, contre 10 000 actuellement.",
        "Doublement de la part de bio dans les cantines scolaires.",
        "Test de la remunicipalisation de la restauration scolaire via des lots expérimentaux.",
        "Création de cuisines de proximité décentralisées pour améliorer la qualité des repas.",
        "Kit scolaire gratuit de rentrée augmenté de 80 euros à 150 euros par enfant.",
    ],
    "periscolaire-loisirs": [
        "Petits déjeuners gratuits pour 15 000 écoliers marseillais.",
    ],

    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Plantation de 300 000 arbres, arbustes et buissons à Marseille dans le cadre du Plan Arbres.",
        "Création d'un grand écoparc de plusieurs milliers d'hectares dans le massif de l'Étoile avec sentiers balisés, maison du parc, zones pédagogiques et aires de repos.",
        "Création d'une ferme pédagogique dans le parc du massif de l'Étoile.",
    ],
    "proprete-dechets": [
        "Reprise en main de la gouvernance de la propreté depuis la Métropole.",
        "Doublement de la fréquence des tournées de nettoyage urbain.",
        "Doublement du nombre de poubelles de rue, de 7 000 à 15 000 unités.",
        "Retour du cantonnier de quartier identifié pour chaque secteur.",
        "Mise en place de poubelles intelligentes connectées, communicant avec les agents pour optimiser la collecte.",
        "Réorganisation de la collecte des déchets par secteur selon la densité et l'activité des quartiers.",
        "Amélioration du tri sélectif, Marseille étant dernière de France avec 38 kg par habitant par an.",
    ],
    "climat-adaptation": [
        "Objectif de réduction de 30 % de la consommation d'eau de la ville.",
        "Sélection de plantes économes en eau et résistantes à la chaleur pour les espaces verts municipaux.",
    ],
    "alimentation-durable": [
        "Obligation annuelle de montée en qualité imposée aux prestataires de restauration scolaire.",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Création d'une mutuelle municipale complémentaire ouverte à tous les Marseillais, sans conditions de ressources.",
        "Tarifs de la mutuelle municipale de 20 % à 30 % moins chers que le marché.",
    ],
    "prevention-sante": [
        "Gratuité des premiers mètres cubes d'eau potable pour tous les Marseillais.",
    ],

    # ── DÉMOCRATIE ──
    "budget-participatif": [
        "Budgets participatifs déployés dans chaque mairie de secteur.",
        "Consultation de 15 000 Marseillais en 72 ateliers pour l'élaboration du programme.",
    ],
    "services-publics": [
        "Retour en régie publique de la gestion de l'eau potable à l'expiration du contrat Veolia/SEM en 2029.",
        "Négociation avec la SEMM pour rendre l'eau gratuite ou à tarif réduit sur les premiers mètres cubes.",
    ],

    # ── ÉCONOMIE ──
    "attractivite": [
        "Création d'une Société du Grand Marseille pour porter les grands projets de long terme.",
        "Création d'une zone franche urbaine pour encourager l'implantation d'entreprises commerciales.",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Implantation d'une philharmonie dans le Centre Bourse pour redynamiser le centre-ville.",
        "Création d'une Cité de la mer et des sciences, pôle culturel enfance dédié aux océans.",
        "Création d'une médiathèque à Capitaine-Gèze.",
        "Création d'une médiathèque à la Rose.",
        "Création d'une médiathèque au Vallon Régny.",
    ],

    # ── SPORT ──
    "equipements-sportifs": [
        "Construction du plus grand boulodrome couvert du monde à vocation internationale du côté de Saint-Marcel.",
        "Reconstruction de la piscine Nord.",
        "Reconstruction de la piscine Luminy.",
    ],

    # ── URBANISME ──
    "amenagement-urbain": [
        "Projet Grandes Rives de la Méditerranée : grande promenade littorale du Nord au Sud avec jardins, espaces paysagers et belvédères.",
        "Rénovation complète de la plage des Catalans.",
        "Cheminement et découverte de l'Anse du Pharo.",
        "Accès renouvelé à la Digue du Large.",
        "Agrandissement des plages Nord et Sud.",
        "Création d'un parc balnéaire à l'Estaque.",
        "Gare des plages à Corbières pour le train de la Côte Bleue.",
    ],
    "quartiers-prioritaires": [
        "Désenclavement des quartiers Nord et Est par le développement de transports lourds.",
    ],

    # ── SOLIDARITÉ ──
    "aide-sociale": [
        "525 places d'hébergement d'urgence créées pour les sans-abri et les personnes en situation de précarité.",
        "Poursuite des dispositifs d'accueil de jour et de nuit pour les personnes sans domicile.",
    ],
    "pouvoir-achat": [
        "Kit scolaire gratuit de rentrée porté à 150 euros par enfant.",
        "Gratuité de la cantine scolaire étendue de 10 000 à 15 000 enfants.",
        "Gratuité des transports pour les moins de 26 ans et les demandeurs d'emploi.",
    ],
}


def main():
    print("=" * 60)
    print(f"  RE-EXTRACTION {CANDIDAT_ID.upper()} ({VILLE_ID})")
    print("=" * 60)

    # Vérifier la configuration
    if "TODO" in (CANDIDAT_ID, VILLE_ID, SOURCE, SOURCE_URL):
        print("\n  ERREUR : remplir CANDIDAT_ID, VILLE_ID, SOURCE, SOURCE_URL")
        sys.exit(1)

    if not MESURES:
        print("\n  ERREUR : aucune mesure définie dans MESURES")
        sys.exit(1)

    total_new = sum(len(v) for v in MESURES.values())
    print(f"\n  {total_new} mesures dans {len(MESURES)} sous-thèmes")

    # Charger le JSON
    if not os.path.exists(JSON_PATH):
        print(f"\n  ERREUR : fichier introuvable : {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Compter les mesures existantes
    existing_total = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            prop = st["propositions"].get(CANDIDAT_ID)
            if prop and prop.get("mesures"):
                existing_total += len(prop["mesures"])

    # Safety check : abort si nouvelles mesures < 50% des existantes
    if existing_total > 0 and total_new < existing_total * 0.5:
        print(f"\n  SAFETY CHECK ECHOUE !")
        print(f"  Existantes : {existing_total} mesures")
        print(f"  Nouvelles  : {total_new} mesures ({total_new/existing_total*100:.0f}%)")
        print(f"  Seuil      : 50% minimum ({existing_total * 0.5:.0f})")
        print(f"\n  Abandon. Vérifiez que l'extraction est complète.")
        sys.exit(1)

    # Appliquer les nouvelles mesures
    updated = 0
    skipped = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id not in MESURES or not MESURES[st_id]:
                continue

            prop = st["propositions"].get(CANDIDAT_ID)
            if prop is None:
                prop = {}
                st["propositions"][CANDIDAT_ID] = prop

            old_count = len(prop.get("mesures", []))
            new_mesures = MESURES[st_id]

            if len(new_mesures) >= old_count:
                prop["mesures"] = new_mesures
                prop["source"] = SOURCE
                prop["sourceUrl"] = SOURCE_URL
                updated += 1
                if old_count != len(new_mesures):
                    print(f"    {st_id}: {old_count} -> {len(new_mesures)}")
            else:
                skipped += 1
                print(f"    SKIP {st_id}: {old_count} existantes > {len(new_mesures)} nouvelles")

    # Sauvegarder
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n  {updated} sous-thèmes mis à jour")
    if skipped:
        print(f"  {skipped} sous-thèmes ignorés (moins de mesures nouvelles)")

    print(f"\n  Prochaines étapes :")
    print(f"    python scripts/valider_donnees.py")
    print(f"    python scripts/auditer_completude.py --candidat {CANDIDAT_ID}")
    print("=" * 60)


if __name__ == "__main__":
    main()
