#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du programme d'Aristide Olivier (Caen 2026)
150 mesures, 6 priorités, livret 24 pages présenté le 16 février 2026
Sources : France Bleu Normandie, Tendance Ouest, site officiel aristideolivier2026.fr
"""

import sys
import io
import json
import os

# Configuration UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Chemin du fichier JSON
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(SCRIPT_DIR, "..", "data", "elections", "caen-2026.json")

# Sources principales
SOURCE_FB = "France Bleu Normandie, février 2026"
URL_FB = "https://www.francebleu.fr/normandie/calvados-14/caen/municipales-2026-a-caen-le-maire-sortant-presente-150-mesures-pour-six-priorites-sans-hausses-d-impots-8683751"

SOURCE_TO_150 = "Tendance Ouest, février 2026"
URL_TO_150 = "https://www.tendanceouest.com/actualite-436501-caen-aristide-olivier-presente-150-projets-sans-impots-supplementaires"

SOURCE_TO_DEC = "Tendance Ouest, décembre 2025"
URL_TO_DEC = "https://www.tendanceouest.com/actualite-434343-municipales-2026-doublement-des-cameras-retour-du-week-end-maritime-aristide-olivier-candidat-a-caen"

SOURCE_SITE = "Site officiel Caen Passionnément"
URL_SITE = "https://www.aristideolivier2026.fr/"


def charger_json():
    """Charge le fichier JSON existant"""
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def sauvegarder_json(data):
    """Sauvegarde le fichier JSON avec UTF-8"""
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Fichier sauvegardé : {JSON_PATH}")


def mettre_a_jour_candidat(data):
    """Met à jour les informations du candidat Olivier"""
    for candidat in data['candidats']:
        if candidat['id'] == 'olivier':
            candidat['programmeUrl'] = URL_SITE
            candidat['programmeComplet'] = True
            candidat['programmePdfPath'] = None
            print(f"  Candidat mis à jour : programmeUrl={URL_SITE}")
            print(f"  programmeComplet passé à True (150 mesures, livret 24 pages)")
            break


def ajouter_proposition(categorie, sous_theme_id, texte, source, source_url):
    """Ajoute une proposition pour Olivier dans un sous-thème"""
    for st in categorie['sousThemes']:
        if st['id'] == sous_theme_id:
            st['propositions']['olivier'] = {
                'texte': texte,
                'source': source,
                'sourceUrl': source_url
            }
            return True
    return False


def integrer_propositions(data):
    """Intègre toutes les propositions d'Olivier dans le JSON"""

    count = 0
    count_existant = 0

    # Dictionnaire catégorie_id -> catégorie
    categories = {cat['id']: cat for cat in data['categories']}

    # =====================================================================
    # SÉCURITÉ (priorité n°1 du programme)
    # =====================================================================

    # police-municipale : DÉJÀ PRÉSENT - on ne touche pas
    print("  [existant] securite > police-municipale")
    count_existant += 1

    # videoprotection : DÉJÀ PRÉSENT - on ne touche pas
    print("  [existant] securite > videoprotection")
    count_existant += 1

    # prevention-mediation : NOUVEAU
    if ajouter_proposition(
        categories['securite'],
        'prevention-mediation',
        "Renforcement de la brigade de proximité dans les quartiers et augmentation de l'éclairage public dans les secteurs difficiles",
        SOURCE_FB,
        URL_FB
    ):
        count += 1
        print("  [ajouté] securite > prevention-mediation")

    # =====================================================================
    # TRANSPORTS & MOBILITÉ
    # =====================================================================

    # transports-en-commun : NOUVEAU
    if ajouter_proposition(
        categories['transports'],
        'transports-en-commun',
        "Soutien à l'extension du tramway pour améliorer la desserte des zones d'activités et des quartiers denses (Folie-Couvrechef, Saint-Contest)",
        SOURCE_TO_150,
        URL_TO_150
    ):
        count += 1
        print("  [ajouté] transports > transports-en-commun")

    # velo-mobilites-douces : NOUVEAU
    if ajouter_proposition(
        categories['transports'],
        'velo-mobilites-douces',
        "Triplement des pistes cyclables, de 54 km à 200 km sur l'agglomération",
        SOURCE_FB,
        URL_FB
    ):
        count += 1
        print("  [ajouté] transports > velo-mobilites-douces")

    # tarifs-gratuite : DÉJÀ PRÉSENT - on ne touche pas
    print("  [existant] transports > tarifs-gratuite")
    count_existant += 1

    # =====================================================================
    # LOGEMENT
    # =====================================================================

    # logement-social : NOUVEAU
    if ajouter_proposition(
        categories['logement'],
        'logement-social',
        "Construction de 700 logements étudiants dans les deux ans et diversification de l'offre avec des loyers acceptables pour les populations modestes",
        SOURCE_FB,
        URL_FB
    ):
        count += 1
        print("  [ajouté] logement > logement-social")

    # acces-logement : NOUVEAU
    if ajouter_proposition(
        categories['logement'],
        'acces-logement',
        "Requalification de la zone Mont Coco, de la ZAC Beaulieu, du quartier Langevin (Grâce de Dieu) et de l'ancienne maison d'arrêt pour diversifier l'offre de logements",
        SOURCE_TO_150,
        URL_TO_150
    ):
        count += 1
        print("  [ajouté] logement > acces-logement")

    # =====================================================================
    # ÉDUCATION & JEUNESSE
    # =====================================================================

    # petite-enfance : DÉJÀ PRÉSENT - on ne touche pas
    print("  [existant] education > petite-enfance")
    count_existant += 1

    # ecoles-renovation : DÉJÀ PRÉSENT - on ne touche pas
    print("  [existant] education > ecoles-renovation")
    count_existant += 1

    # =====================================================================
    # ENVIRONNEMENT & TRANSITION ÉCOLOGIQUE
    # =====================================================================

    # espaces-verts : NOUVEAU
    if ajouter_proposition(
        categories['environnement'],
        'espaces-verts',
        "Plantation de 10 000 arbres en ville et création d'un parc de 4 hectares à Mont Coco",
        SOURCE_FB,
        URL_FB
    ):
        count += 1
        print("  [ajouté] environnement > espaces-verts")

    # climat-adaptation : NOUVEAU
    if ajouter_proposition(
        categories['environnement'],
        'climat-adaptation',
        "Végétalisation massive de la ville pour lutter contre les îlots de chaleur, avec l'objectif de 10 000 nouveaux arbres plantés",
        SOURCE_TO_150,
        URL_TO_150
    ):
        count += 1
        print("  [ajouté] environnement > climat-adaptation")

    # renovation-energetique : NOUVEAU
    if ajouter_proposition(
        categories['environnement'],
        'renovation-energetique',
        "Programme de rénovation énergétique des bâtiments municipaux et des équipements sportifs pour réduire les consommations, sans hausse d'impôts",
        SOURCE_TO_150,
        URL_TO_150
    ):
        count += 1
        print("  [ajouté] environnement > renovation-energetique")

    # =====================================================================
    # SANTÉ & ACCÈS AUX SOINS
    # =====================================================================

    # seniors : DÉJÀ PRÉSENT - on ne touche pas
    print("  [existant] sante > seniors")
    count_existant += 1

    # =====================================================================
    # DÉMOCRATIE & VIE CITOYENNE
    # =====================================================================

    # transparence : NOUVEAU
    if ajouter_proposition(
        categories['democratie'],
        'transparence',
        "Réduction des frais de réception : 8,5 millions d'euros économisés sur deux mandats, engagement de ne pas augmenter les impôts locaux",
        SOURCE_FB,
        URL_FB
    ):
        count += 1
        print("  [ajouté] democratie > transparence")

    # =====================================================================
    # ÉCONOMIE & EMPLOI
    # =====================================================================

    # attractivite : NOUVEAU
    if ajouter_proposition(
        categories['economie'],
        'attractivite',
        "Facilitation de l'implantation d'entreprises, extension des zones d'activités et amélioration de la desserte en transports en commun pour renforcer l'attractivité économique",
        SOURCE_TO_150,
        URL_TO_150
    ):
        count += 1
        print("  [ajouté] economie > attractivite")

    # commerce-local : NOUVEAU
    if ajouter_proposition(
        categories['economie'],
        'commerce-local',
        "Soutien aux commerces de centre-ville et dynamisation de l'économie locale, notamment autour de la réhabilitation du port",
        SOURCE_TO_150,
        URL_TO_150
    ):
        count += 1
        print("  [ajouté] economie > commerce-local")

    # =====================================================================
    # CULTURE & PATRIMOINE
    # =====================================================================

    # evenements-creation : DÉJÀ PRÉSENT - on ne touche pas
    print("  [existant] culture > evenements-creation")
    count_existant += 1

    # equipements-culturels : NOUVEAU
    if ajouter_proposition(
        categories['culture'],
        'equipements-culturels',
        "Réhabilitation du port de Caen pour en faire un site emblématique, lieu de vie attractif pour les jeunes, les familles et les touristes",
        SOURCE_FB,
        URL_FB
    ):
        count += 1
        print("  [ajouté] culture > equipements-culturels")

    # =====================================================================
    # SPORT & LOISIRS
    # =====================================================================

    # equipements-sportifs : NOUVEAU
    if ajouter_proposition(
        categories['sport'],
        'equipements-sportifs',
        "Rénovation des équipements sportifs de la ville et développement de nouvelles infrastructures accessibles à tous les quartiers",
        SOURCE_TO_150,
        URL_TO_150
    ):
        count += 1
        print("  [ajouté] sport > equipements-sportifs")

    # =====================================================================
    # URBANISME & CADRE DE VIE
    # =====================================================================

    # amenagement-urbain : NOUVEAU
    if ajouter_proposition(
        categories['urbanisme'],
        'amenagement-urbain',
        "Grand projet de réhabilitation du port de Caen et aménagement de nouveaux espaces publics pour une ville plus belle et plus humaine",
        SOURCE_FB,
        URL_FB
    ):
        count += 1
        print("  [ajouté] urbanisme > amenagement-urbain")

    # quartiers-prioritaires : NOUVEAU
    if ajouter_proposition(
        categories['urbanisme'],
        'quartiers-prioritaires',
        "Requalification du quartier Langevin (Grâce de Dieu) et renforcement des actions dans tous les quartiers prioritaires de la ville",
        SOURCE_TO_150,
        URL_TO_150
    ):
        count += 1
        print("  [ajouté] urbanisme > quartiers-prioritaires")

    # =====================================================================
    # SOLIDARITÉ & ÉGALITÉ
    # =====================================================================

    # pouvoir-achat : NOUVEAU
    if ajouter_proposition(
        categories['solidarite'],
        'pouvoir-achat',
        "Engagement de ne pas augmenter les impôts locaux sur tout le mandat, pour préserver le pouvoir d'achat des Caennais",
        SOURCE_FB,
        URL_FB
    ):
        count += 1
        print("  [ajouté] solidarite > pouvoir-achat")

    print(f"\n  Total : {count} nouvelles propositions ajoutées, {count_existant} existantes conservées")
    return count


def main():
    """Fonction principale"""
    print("=" * 65)
    print("INTÉGRATION DU PROGRAMME D'ARISTIDE OLIVIER (CAEN 2026)")
    print("150 mesures, 6 priorités, livret 24 pages")
    print("=" * 65)
    print()

    # Chargement du JSON
    print("1. Chargement du fichier JSON...")
    data = charger_json()
    print(f"   {len(data['candidats'])} candidats, {len(data['categories'])} catégories")
    print()

    # Mise à jour du candidat
    print("2. Mise à jour des informations du candidat...")
    mettre_a_jour_candidat(data)
    print()

    # Intégration des propositions
    print("3. Intégration des propositions...")
    count = integrer_propositions(data)
    print()

    # Sauvegarde
    print("4. Sauvegarde du fichier JSON...")
    sauvegarder_json(data)
    print()

    # Résumé
    print("=" * 65)
    print(f"TERMINÉ : {count} nouvelles propositions intégrées")
    print("=" * 65)
    print()
    print("SOUS-THÈMES COUVERTS (total = 7 existants + nouvelles) :")
    print("  securite : police-municipale, videoprotection, prevention-mediation")
    print("  transports : transports-en-commun, velo-mobilites-douces, tarifs-gratuite")
    print("  logement : logement-social, acces-logement")
    print("  education : petite-enfance, ecoles-renovation")
    print("  environnement : espaces-verts, climat-adaptation, renovation-energetique")
    print("  sante : seniors")
    print("  democratie : transparence")
    print("  economie : attractivite, commerce-local")
    print("  culture : equipements-culturels, evenements-creation")
    print("  sport : equipements-sportifs")
    print("  urbanisme : amenagement-urbain, quartiers-prioritaires")
    print("  solidarite : pouvoir-achat")
    print()
    print("SOURCES :")
    print(f"  - France Bleu Normandie : {URL_FB}")
    print(f"  - Tendance Ouest (150 projets) : {URL_TO_150}")
    print(f"  - Tendance Ouest (déc. 2025) : {URL_TO_DEC}")
    print(f"  - Site officiel : {URL_SITE}")
    print()
    print("NOTE : programmeComplet passé à True (150 mesures dans un livret de 24 pages)")
    print()


if __name__ == '__main__':
    main()
