#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'intégration batch 2 pour Lyon - Compléter Aulas et Perrin-Gilbert
Complète les propositions de Jean-Michel Aulas et Nathalie Perrin-Gilbert
"""

import sys
import io
import json
import os

# Forcer l'encodage UTF-8 pour stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Chemins
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
JSON_PATH = os.path.join(PROJECT_ROOT, 'data', 'elections', 'lyon-2026.json')

def charger_json():
    """Charge le fichier JSON de Lyon"""
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def sauvegarder_json(data):
    """Sauvegarde le fichier JSON avec indentation"""
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def trouver_sous_theme(categories, cat_id, st_id):
    """Trouve un sous-thème dans les catégories"""
    for cat in categories:
        if cat['id'] == cat_id:
            for st in cat['sousThemes']:
                if st['id'] == st_id:
                    return st
    return None

def ajouter_proposition(sous_theme, candidat_id, texte, source, source_url):
    """Ajoute ou met à jour une proposition pour un candidat"""
    if sous_theme['propositions'][candidat_id] is None:
        # Nouveau sous-thème vide
        sous_theme['propositions'][candidat_id] = {
            "texte": texte,
            "source": source,
            "sourceUrl": source_url
        }
        return "AJOUTÉ"
    else:
        # Sous-thème existant - remplacer si le nouveau est plus complet
        ancien_texte = sous_theme['propositions'][candidat_id]['texte']
        if len(texte) > len(ancien_texte) or 'a_verifier' in sous_theme['propositions'][candidat_id]:
            sous_theme['propositions'][candidat_id] = {
                "texte": texte,
                "source": source,
                "sourceUrl": source_url
            }
            return "REMPLACÉ"
        else:
            return "CONSERVÉ (ancien plus complet)"

def main():
    print("=" * 80)
    print("INTÉGRATION BATCH 2 - LYON 2026")
    print("Complétion des programmes de Jean-Michel Aulas et Nathalie Perrin-Gilbert")
    print("=" * 80)
    print()

    # Charger les données
    print("📁 Chargement du JSON...")
    data = charger_json()
    categories = data['categories']

    # Compteur de modifications
    compteur = {'aulas': 0, 'perrin-gilbert': 0}

    print("\n" + "=" * 80)
    print("JEAN-MICHEL AULAS (Cœur Lyonnais) - COMPLÉTION")
    print("=" * 80)

    # AULAS - Nouvelles propositions détaillées
    propositions_aulas = [
        # Sécurité
        {
            'cat': 'securite', 'st': 'police-municipale',
            'texte': "500 policiers municipaux d'ici 2033 (contre 311 actuellement), création d'unités spécialisées et police municipale des transports dans métros, bus et gares. Création d'un 'Hôtel de la Police' mutualisant forces nationales et municipales",
            'source': "Lyon Capitale, février 2026",
            'url': "https://www.lyoncapitale.fr/actualite/municipales-2026-a-lyon-jean-michel-aulas-degaine-ses-propositions-de-campagne-sur-la-securite"
        },
        {
            'cat': 'securite', 'st': 'videoprotection',
            'texte': "Doublement du réseau de caméras de surveillance : 1200 caméras déployées",
            'source': "Lyon Capitale, février 2026",
            'url': "https://www.lyoncapitale.fr/actualite/municipales-2026-a-lyon-jean-michel-aulas-degaine-ses-propositions-de-campagne-sur-la-securite"
        },
        {
            'cat': 'securite', 'st': 'prevention-mediation',
            'texte': "Charte lyonnaise du respect urbain, diplôme de mobilité pour tous les écoliers lyonnais (citoyenneté dès l'enfance), semaine annuelle des rues apaisées dans tous les arrondissements",
            'source': "Lyon Capitale, février 2026",
            'url': "https://www.lyoncapitale.fr/actualite/municipales-2026-les-six-propositions-de-jean-michel-aulas-pour-apaiser-la-rue-a-lyon"
        },
        # Transports
        {
            'cat': 'transports', 'st': 'transports-en-commun',
            'texte': "Gratuité des transports en commun pour les Lyonnais gagnant moins de 2 500€ par mois. Projet de nouvelle ligne de métro Est-Ouest",
            'source': "Lyon Capitale, février 2026",
            'url': "https://www.lyoncapitale.fr/actualite/municipales-2026-les-propositions-des-principaux-candidats"
        },
        {
            'cat': 'transports', 'st': 'tunnel-circulation',
            'texte': "Nouveau tunnel de 8 km entre Tassin et Saint-Fons (budget 1,4 milliard d'euros) pour désengorger le tunnel de Fourvière (110 000 véhicules/jour), libérant 45 hectares d'espaces",
            'source': "Lyon Capitale, février 2026",
            'url': "https://www.lyoncapitale.fr/actualite/municipales-2026-les-propositions-des-principaux-candidats"
        },
        # Logement
        {
            'cat': 'logement', 'st': 'encadrement-loyers',
            'texte': "Charte de modération des loyers obligatoire, construite localement et basée sur les travaux de l'Observatoire local des loyers",
            'source': "Lyon Capitale, février 2026",
            'url': "https://www.lyoncapitale.fr/elections-2026/ce-que-jean-michel-aulas-propose-et-ce-qu-il-veut-supprimer"
        },
        # Culture
        {
            'cat': 'culture', 'st': 'equipements-culturels',
            'texte': "Rénovation et agrandissement de la bibliothèque municipale de la Part-Dieu (3e arr.) : 140 millions d'euros investis, au moins 4 000 m² d'espace supplémentaire",
            'source': "Lyon Capitale, février 2026",
            'url': "https://www.lyoncapitale.fr/actualite/municipales-2026-les-propositions-des-principaux-candidats"
        },
    ]

    for prop in propositions_aulas:
        st = trouver_sous_theme(categories, prop['cat'], prop['st'])
        if st:
            statut = ajouter_proposition(st, 'aulas', prop['texte'], prop['source'], prop['url'])
            print(f"✓ {prop['cat']}/{prop['st']}: {statut}")
            if statut != "CONSERVÉ (ancien plus complet)":
                compteur['aulas'] += 1
        else:
            print(f"⚠ Sous-thème {prop['cat']}/{prop['st']} non trouvé!")

    print("\n" + "=" * 80)
    print("NATHALIE PERRIN-GILBERT (Lyon en commun)")
    print("=" * 80)

    # PERRIN-GILBERT - Nouvelles propositions
    propositions_perrin_gilbert = [
        # Logement
        {
            'cat': 'logement', 'st': 'logement-social',
            'texte': "Fonds de rénovation pour les bailleurs de logement social afin de soutenir la rénovation des logements. Modèle 1/3 social, 1/3 libre, 1/3 accession à la propriété et contrôle strict des loyers",
            'source': "Lyon Capitale, février 2026",
            'url': "https://www.lyoncapitale.fr/actualite/municipales-2026-les-propositions-des-principaux-candidats"
        },
        # Solidarité
        {
            'cat': 'solidarite', 'st': 'aide-sociale',
            'texte': "Objectif zéro enfant à la rue : en 2026 il ne devrait pas être possible que des enfants dorment dans la rue. Mobilisation du patrimoine municipal pour héberger les enfants et leurs familles",
            'source': "Lyon Capitale & RCF Lyon, février 2026",
            'url': "https://www.lyoncapitale.fr/actualite/justice-sociale-mobilites-securite-a-lyon-nathalie-perrin-gilbert-lance-sa-campagne-pour-les-municipales-2026"
        },
        # Culture
        {
            'cat': 'culture', 'st': 'equipements-culturels',
            'texte': "Création d'un musée des sciences dans l'ancien musée Guimet (Exploratorium inspiré de San Francisco). Grands projets pour la halle Tony-Garnier, le musée Guimet et l'École Nationale des Beaux-Arts sur le site Neyret. Médiathèque à la Guillotière",
            'source': "Lyon Mag & Tribune de Lyon, février 2026",
            'url': "https://www.lyonmag.com/article/144949/municipales-2026-a-lyon-nathalie-perrin-gilbert-a-un-projet-couteux-pour-rouvrir-le-musee-guimet"
        },
        {
            'cat': 'culture', 'st': 'evenements-creation',
            'texte': "Réouverture du musée Guimet en Exploratorium dédié aux sciences. Révision de la Fête des Lumières avec festival intérieur à la Halle Tony-Garnier. Médiathèque à la Guillotière",
            'source': "Tribune de Lyon, février 2026",
            'url': "https://tribunedelyon.fr/politique/municipales-2026-nathalie-perrin-gilbert-lance-sa-campagne-samedi-a-la-guillotiere/"
        },
        # Éducation
        {
            'cat': 'education', 'st': 'petite-enfance',
            'texte': "Droit opposable à une place en crèche garantie d'ici 2030. Opposition à la marchandisation de la petite enfance. Grand plan de formation pour les métiers de la petite enfance et du grand âge",
            'source': "Lyon Capitale & Tribune de Lyon, février 2026",
            'url': "https://www.lyoncapitale.fr/actualite/municipales-2026-les-propositions-des-principaux-candidats"
        },
        # Sécurité
        {
            'cat': 'securite', 'st': 'prevention-mediation',
            'texte': "Remise à plat des relations avec la préfecture. Vidéosurveillance au cas par cas, refus d'en faire une solution miracle. Priorité à la prévention et la médiation",
            'source': "Tribune de Lyon, février 2026",
            'url': "https://tribunedelyon.fr/politique/municipales-2026-nathalie-perrin-gilbert-lance-sa-campagne-samedi-a-la-guillotiere/"
        },
        # Démocratie
        {
            'cat': 'democratie', 'st': 'budget-participatif',
            'texte': "Réduction de l'exécutif à 16 adjoints et 4 conseillers délégués (contre 20 + 3 actuellement) pour mettre fin à l'émiettement et réaliser des économies de fonctionnement",
            'source': "Tribune de Lyon, février 2026",
            'url': "https://tribunedelyon.fr/politique/municipales-2026-nathalie-perrin-gilbert-lance-sa-campagne-samedi-a-la-guillotiere/"
        },
    ]

    for prop in propositions_perrin_gilbert:
        st = trouver_sous_theme(categories, prop['cat'], prop['st'])
        if st:
            statut = ajouter_proposition(st, 'perrin-gilbert', prop['texte'], prop['source'], prop['url'])
            print(f"✓ {prop['cat']}/{prop['st']}: {statut}")
            if statut != "CONSERVÉ (ancien plus complet)":
                compteur['perrin-gilbert'] += 1
        else:
            print(f"⚠ Sous-thème {prop['cat']}/{prop['st']} non trouvé!")

    # Vérifier si Aulas doit passer à programmeComplet: true
    print("\n" + "=" * 80)
    print("VÉRIFICATION programmeComplet")
    print("=" * 80)

    # Compter les sous-thèmes remplis pour Aulas
    count_aulas = 0
    for cat in categories:
        for st in cat['sousThemes']:
            if st['propositions']['aulas'] is not None:
                count_aulas += 1

    print(f"\nAulas : {count_aulas} sous-thèmes remplis")

    # Mettre à jour programmeComplet si >= 15 sous-thèmes
    for candidat in data['candidats']:
        if candidat['id'] == 'aulas' and count_aulas >= 15:
            ancien_statut = candidat['programmeComplet']
            candidat['programmeComplet'] = True
            print(f"→ Aulas programmeComplet: {ancien_statut} → True (≥15 sous-thèmes)")

    # Sauvegarder
    print("\n" + "=" * 80)
    print("SAUVEGARDE")
    print("=" * 80)
    print(f"💾 Sauvegarde de {JSON_PATH}...")
    sauvegarder_json(data)

    print("\n" + "=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    print(f"✓ Aulas : {compteur['aulas']} nouvelles propositions ajoutées/mises à jour")
    print(f"✓ Perrin-Gilbert : {compteur['perrin-gilbert']} nouvelles propositions ajoutées/mises à jour")
    print(f"✓ Total Aulas : {count_aulas} sous-thèmes remplis")
    print("\n✅ Intégration terminée avec succès!")
    print()

if __name__ == '__main__':
    main()
