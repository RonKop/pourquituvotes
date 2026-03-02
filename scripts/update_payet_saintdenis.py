#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Met à jour les propositions de Giovanni Payet (La Voix Citoyenne)
depuis le programme Word reçu par email le 01/03/2026.
"""

import json
import os
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "saint-denis-reunion-2026.json")
CANDIDAT_ID = "payet"

PROPOSITIONS = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Travailler main dans la main avec la Police Municipale et les forces de l'ordre nationales pour garantir la tranquillité de la commune.",
    ],
    "videoprotection": None,
    "prevention-mediation": [
        "Créer une application mobile et une ligne téléphonique dédiée (Saint-Denis Tranquille) pour signaler les problèmes, suivre les demandes en temps réel et obtenir des réponses.",
        "Lancer le programme « Les 100 zafer ki dékon' » : plan d'action contre la saleté, les violences, la drogue et les animaux errants, en lien avec les associations et la fourrière.",
    ],
    "violences-femmes": None,

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Créer 5 lignes de bus express : 1 sur le Boulevard Sud et 4 entre les hauts et les bas, opérationnelles dès août 2026.",
    ],
    "velo-mobilites-douces": [
        "Plan d'entretien des trottoirs, chemins, routes et pistes cyclables communales (Libéranoo), avec extension dans les quartiers prioritaires et suppression des zones de danger.",
    ],
    "pietons-circulation": None,
    "stationnement": None,
    "tarifs-gratuite": [
        "Instaurer la gratuité des transports en commun pour tous les Dionysiens, sans condition d'âge, de profession ou de condition sociale, dès août 2026.",
    ],

    # ── LOGEMENT ──
    "logement-social": [
        "Construire 1 500 logements d'ici 2030 dans de futurs quartiers-jardins (propres, plantés et fleuris).",
        "Construire 5 résidences pour personnes âgées et 1 foyer de jeunes travailleurs.",
        "Créer 100 chambres de colocation jeunes-séniors.",
    ],
    "logements-vacants": [
        "Réquisitionner les logements insalubres et reconvertir les commerces en pied d'immeubles en logements.",
    ],
    "encadrement-loyers": None,
    "acces-logement": None,

    # ── ÉDUCATION ──
    "petite-enfance": None,
    "ecoles-renovation": [
        "Lancer le plan « Mon lékol i refé 2026-2036 » : engagement sur 10 ans pour moderniser et rénover les écoles municipales, protéger les élèves des aléas climatiques (chaleur, froid, humidité) et du bruit dans les cantines.",
    ],
    "cantines-fournitures": [
        "Augmenter de 10 % le budget de la restauration scolaire.",
        "Atteindre 25 % de produits alimentaires issus de Saint-Denis dans les cantines grâce aux agriculteurs locaux.",
        "Réduire de 30 % le gaspillage alimentaire dans les cantines scolaires.",
    ],
    "periscolaire-loisirs": [
        "Installer, rénover et entretenir un réseau d'aires de jeux sécurisées à proximité de chaque quartier.",
    ],
    "jeunesse": [
        "Créer le Hub, espace municipal pour les 15-30 ans : lieu de vie, tremplin créatif et mise en réseau de la jeune garde dionysienne, avec un Marché des Jeunes Créateurs.",
        "Organiser « Les 4 lieux » : 4 fois par an, un lieu de Saint-Denis se transforme en grand espace festif sécurisé pour les jeunes (musique, danse, concerts, stand up, navettes bus).",
        "Accompagner techniquement et financièrement les propositions du Conseil des Jeunes Dionysiens.",
    ],

    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Planter 150 000 arbres vivants d'ici 2032, produits dans une pépinière municipale, pour répondre à l'urgence climatique et protéger les sols de l'érosion.",
        "Offrir 1 arbre à chaque étape clé de la vie d'un Dionysien (naissance, majorité, mariage, 100e bougie).",
    ],
    "proprete-dechets": [
        "Engager un curage et un nettoyage préventif régulier des caniveaux et ravines pour garantir l'évacuation des eaux pluviales et protéger les habitations.",
    ],
    "climat-adaptation": [
        "Réviser le PLU pour bâtir une « Commune-éponge » : désimperméabilisation des sols, jardins de pluie, zones d'apaisement végétalisées dans les quartiers.",
        "Réduire l'empreinte carbone des activités liées au mandat municipal (déplacements, événements, consommation d'énergie).",
    ],
    "renovation-energetique": None,
    "alimentation-durable": [
        "Protéger les terres agricoles contre l'urbanisation via le PLU pour gagner 100 hectares de surface cultivable et installer une nouvelle génération d'agriculteurs (ceinture verte dionysienne).",
        "Organiser chaque mois le « Proxi-vrac » : vente de produits sains en pied d'immeubles dans les quartiers prioritaires, à prix juste, pour les familles monoparentales, étudiants, seniors et demandeurs d'emploi.",
        "Instaurer la gratuité des 10 premiers m³ d'eau et une tarification progressive par paliers pour lutter contre le gaspillage.",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Négocier une mutuelle santé communale pour tous les Dionysiens (retraités, étudiants, demandeurs d'emploi, indépendants, agriculteurs) avec 20 à 30 % de réduction sur les cotisations, sans questionnaire de santé ni limite d'âge.",
    ],
    "prevention-sante": [
        "Créer la Maison dionysienne de la santé mentale : service public de proximité gratuit pour lutter contre l'isolement, l'anxiété et les suicides, avec soutien psychologique sans jugement.",
    ],
    "seniors": [
        "Construire 5 résidences adaptées pour personnes âgées.",
        "Développer la colocation intergénérationnelle jeunes-séniors (100 chambres).",
    ],

    # ── DÉMOCRATIE ──
    "budget-participatif": [
        "Créer l'Assemblée Citoyenne Extramunicipale, composée d'habitants tirés au sort, pour veiller au respect des engagements municipaux sur plusieurs mandats.",
        "Créer la Fabrique dionysienne : espace où les habitants fabriquent les projets, portent les décisions et actions qui impactent leur quartier, avec l'appui des services municipaux.",
    ],
    "transparence": [
        "Publier sur internet l'intégralité des indemnités des élus et leurs agendas professionnels.",
        "Plafonner les indemnités des élus à 5 000 euros brut/mois tout cumulé.",
        "Suspendre immédiatement tout élu mis en examen pour corruption, détournement ou harcèlement.",
        "Garantir que chaque décision (logement, emploi, subvention) soit prise selon des critères objectifs, transparents et publics.",
        "Signer la charte Anticor et interdire tout conflit d'intérêts dans les votes et délibérations.",
        "Interdire l'usage des moyens municipaux pour la promotion personnelle des élus ; information publique factuelle et respectueuse de l'opposition.",
        "Refuser l'utilisation des véhicules et frais municipaux à des fins personnelles ou partisanes.",
    ],
    "vie-associative": [
        "Sécuriser les associations avec des contrats de 3 ans et une charte des engagements réciproques, en garantissant leur liberté d'expression et de critique.",
    ],
    "services-publics": None,

    # ── ÉCONOMIE ──
    "commerce-local": [
        "Lancer le plan d'urgence « Richesse 2030 » pour redynamiser l'économie et le commerce des quartiers et du centre-ville, avec un manager de centre-ville et un plan d'embellissement.",
    ],
    "emploi-insertion": [
        "Créer l'incubateur PéIA : espace-tremplin vers les métiers de l'intelligence artificielle, ouvert à tous les publics (jeunes, demandeurs d'emploi, agents municipaux, entrepreneurs).",
        "Mettre en place le télétravail et le Forfait Mobilité Durable pour les agents de la Commune.",
    ],
    "attractivite": [
        "Développer un city-branding pour la Commune afin de valoriser l'image et l'attractivité de Saint-Denis.",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Candidater au label Ville apprenante UNESCO pour mobiliser toutes les forces éducatives, sportives, associatives, artistiques et culturelles, avec une priorité à la lecture publique.",
    ],
    "evenements-creation": [
        "Organiser les festivités « Saint-Denis 360 ! » en 2029 pour célébrer les 360 ans de la ville : politique culturelle, artistique et sportive articulée autour de cette date.",
    ],

    # ── SPORT ──
    "equipements-sportifs": None,
    "sport-pour-tous": [
        "Lancer le programme « Victoire » : soutien financier et technique aux disciplines sportives d'excellence (tir à l'arc, gym, volley, hand, rugby) pour propulser les champions dionysiens.",
    ],

    # ── URBANISME ──
    "amenagement-urbain": [
        "Reconquérir « La Rue aux Enfants » : créer des zones éclairées, apaisées et végétalisées où les familles peuvent se réapproprier l'espace public.",
    ],
    "accessibilite": [
        "Repenser l'espace urbain pour l'accès universel aux infrastructures et services publics, garantir l'autonomie des seniors et des personnes en situation de handicap (programme « La Commune sans limite »).",
    ],
    "quartiers-prioritaires": None,

    # ── SOLIDARITÉ ──
    "aide-sociale": None,
    "egalite-discriminations": [
        "Créer la Maison de l'accueil et de l'intégration dionysienne : accompagnement des nouveaux arrivants avec cours de créole, cafés débat culturels et parrainages-marrainages.",
        "Instaurer le Pacte de fraternité dionysienne obligatoire pour tout nouvel habitant.",
        "Sanctionner tout élu portant des propos sexistes, racistes ou discriminants, jusqu'à l'exclusion du conseil municipal.",
    ],
    "pouvoir-achat": [
        "Gratuité des transports en commun pour tous les Dionysiens.",
        "Gratuité des 10 premiers m³ d'eau avec tarification progressive.",
        "Mutuelle santé communale avec 20 à 30 % de réduction (jusqu'à 400 € d'économie par an).",
    ],
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for c in data["candidats"]:
        if c["id"] == CANDIDAT_ID:
            c["programmeUrl"] = "https://lavoixcitoyenne.re/"
            c["programmeComplet"] = True
            break

    updated = 0
    added = 0
    total_mesures = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id not in PROPOSITIONS:
                continue

            new_mesures = PROPOSITIONS[st_id]
            if new_mesures is None:
                continue

            if "propositions" not in st:
                st["propositions"] = {}

            had_before = (
                CANDIDAT_ID in st["propositions"]
                and st["propositions"][CANDIDAT_ID]
                and st["propositions"][CANDIDAT_ID].get("mesures")
            )

            st["propositions"][CANDIDAT_ID] = {"mesures": new_mesures}
            total_mesures += len(new_mesures)
            if had_before:
                updated += 1
            else:
                added += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"{'='*55}")
    print(f"  MISE À JOUR — Giovanni Payet (Saint-Denis Réunion)")
    print(f"{'='*55}")
    print(f"  Sous-thèmes mis à jour : {updated}")
    print(f"  Sous-thèmes ajoutés    : {added}")
    print(f"  Total mesures          : {total_mesures}")
    print(f"  JSON écrit : {JSON_PATH}")


if __name__ == "__main__":
    main()
