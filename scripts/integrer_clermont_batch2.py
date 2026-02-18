#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script d'intégration des programmes de Julien Bony (LR) et Marianne Maximi (LFI)
pour les élections municipales 2026 à Clermont-Ferrand.

Basé sur les recherches web effectuées en février 2026.
"""

import json
import sys
import os

# Configuration UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Chemin du fichier JSON
JSON_PATH = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\clermont-2026.json"

# Nouvelles propositions pour Julien Bony (LR)
PROPOSITIONS_BONY = {
    # Sécurité (déjà présent mais on complète)
    # police-municipale: déjà intégré
    # videoprotection: déjà intégré
    # prevention-mediation: déjà intégré avec éclairage public et expulsions

    # Transports
    "pietons-circulation": {
        "texte": "Améliorer significativement la mobilité pour tous les usagers sans les opposer. Fin de la Zone à Trafic Limité (ZTL) pour fluidifier la circulation : « Assouplir pour fluidifier »",
        "source": "Lettre aux Clermontois, bony2026.fr | France 3 Auvergne-Rhône-Alpes, 11/01/2026",
        "sourceUrl": "https://bony2026.fr"
    },

    # Économie
    "commerce-local": {
        "texte": "Recréer un environnement économique propice à de nouvelles installations avec une vigilance particulière pour le commerce de centre-ville. Création d'un office municipal du commerce avec moyens propres et moyens juridiques pour fédérer et servir de moteur au commerce clermontois. Création d'une application dédiée aux commerces de Clermont-Ferrand",
        "source": "Lettre aux Clermontois, bony2026.fr | France 3 Auvergne-Rhône-Alpes, 11/01/2026",
        "sourceUrl": "https://bony2026.fr"
    },

    # Autres thèmes
    "petite-enfance": {
        "texte": "Services publics efficaces et de qualité pour les familles, accès aux services petite enfance",
        "source": "Lettre aux Clermontois, bony2026.fr",
        "sourceUrl": "https://bony2026.fr"
    },

    "espaces-verts": {
        "texte": "Moins de béton et plus de vert, mieux entretenir nos espaces publics et en garantir la propreté",
        "source": "Lettre aux Clermontois, bony2026.fr",
        "sourceUrl": "https://bony2026.fr"
    },

    "climat-adaptation": {
        "texte": "Préférer une politique pragmatique et inclusive à la promotion d'une écologie punitive",
        "source": "Lettre aux Clermontois, bony2026.fr",
        "sourceUrl": "https://bony2026.fr"
    },

    "centres-sante": {
        "texte": "Mener des politiques de santé ambitieuses et favoriser les infrastructures qui permettent d'améliorer la prise en charge médicale. Engagement contre les déserts médicaux et pour l'accès aux soins",
        "source": "Lettre aux Clermontois, bony2026.fr",
        "sourceUrl": "https://bony2026.fr"
    },

    "budget-participatif": {
        "texte": "Mise en place de consultations populaires, pas de décisions imposées d'en haut",
        "source": "Lettre aux Clermontois, bony2026.fr",
        "sourceUrl": "https://bony2026.fr"
    },

    "transparence": {
        "texte": "Réduction du train de vie de la municipalité, chasse aux gaspillages et transparence dans les attributions de marchés. « Tourner le dos aux grands projets et revenir à l'essentiel » en matière d'urbanisme et de budget",
        "source": "Lettre aux Clermontois, bony2026.fr | France 3 Auvergne-Rhône-Alpes, 11/01/2026",
        "sourceUrl": "https://bony2026.fr"
    },

    "attractivite": {
        "texte": "Politique de relance de l'attractivité, toujours aux côtés des commerces, entreprises et établissements universitaires",
        "source": "Lettre aux Clermontois, bony2026.fr",
        "sourceUrl": "https://bony2026.fr"
    },

    "evenements-creation": {
        "texte": "Valorisation de l'identité territoriale et du patrimoine pour attirer des commerces et talents",
        "source": "Lettre aux Clermontois, bony2026.fr",
        "sourceUrl": "https://bony2026.fr"
    },

    "amenagement-urbain": {
        "texte": "Moderniser nos espaces publics qui souffrent d'une forme d'abandon, de la propreté à l'accessibilité",
        "source": "Lettre aux Clermontois, bony2026.fr",
        "sourceUrl": "https://bony2026.fr"
    },

    "accessibilite": {
        "texte": "Améliorer le quotidien des personnes à mobilité réduite grâce à des aménagements parfaitement adaptés",
        "source": "Lettre aux Clermontois, bony2026.fr",
        "sourceUrl": "https://bony2026.fr"
    }
}

# Nouvelles propositions pour Marianne Maximi (LFI)
PROPOSITIONS_MAXIMI = {
    # Transports - déjà présent
    "tarifs-gratuite": {
        "texte": "Gratuité totale des transports en commun, au-delà de la seule gratuité du week-end",
        "source": "Déclaration de campagne (réunion publique, 15/11/2025)",
        "sourceUrl": "#"
    },

    # Logement
    "logement-social": {
        "texte": "Développement du logement social. Fin des politiques de démolition de logements. Cesser les politiques de casse du logement social telle que la métropole l'a mise en place depuis plusieurs années avec l'ANRU",
        "source": "France 3 Auvergne, février 2026 | Déclaration de campagne (réunion publique, 15/11/2025)",
        "sourceUrl": "https://france3-regions.franceinfo.fr/"
    },

    # Éducation
    "cantines-fournitures": {
        "texte": "Gratuité totale des cantines scolaires pour tous les élèves. Cantines bio et gratuites dans toutes les écoles municipales",
        "source": "France 3 Auvergne-Rhône-Alpes, 15/11/2025",
        "sourceUrl": "https://france3-regions.franceinfo.fr/auvergne-rhone-alpes/puy-de-dome/clermont-ferrand/municipales-2026-a-clermont-ferrand-marianne-maximi-candidate-pour-lfi-promet-un-programme-de-rupture-3249922.html"
    },

    # Santé
    "centres-sante": {
        "texte": "Développement de centres de santé municipaux",
        "source": "France 3 Auvergne-Rhône-Alpes, 15/11/2025",
        "sourceUrl": "https://france3-regions.franceinfo.fr/auvergne-rhone-alpes/puy-de-dome/clermont-ferrand/municipales-2026-a-clermont-ferrand-marianne-maximi-candidate-pour-lfi-promet-un-programme-de-rupture-3249922.html"
    },

    # Économie
    "emploi-insertion": {
        "texte": "Réorienter les financements publics vers les TPE et PME en difficulté plutôt que vers les grandes entreprises",
        "source": "France 3 Auvergne-Rhône-Alpes, 15/11/2025",
        "sourceUrl": "https://france3-regions.franceinfo.fr/auvergne-rhone-alpes/puy-de-dome/clermont-ferrand/municipales-2026-a-clermont-ferrand-marianne-maximi-candidate-pour-lfi-promet-un-programme-de-rupture-3249922.html"
    },

    # Solidarité
    "aide-sociale": {
        "texte": "Plan « zéro enfant à la rue » : une trentaine d'enfants dorment dans la rue depuis septembre à Clermont-Ferrand",
        "source": "France 3 Auvergne-Rhône-Alpes, 15/11/2025",
        "sourceUrl": "https://france3-regions.franceinfo.fr/auvergne-rhone-alpes/puy-de-dome/clermont-ferrand/municipales-2026-a-clermont-ferrand-marianne-maximi-candidate-pour-lfi-promet-un-programme-de-rupture-3249922.html"
    }
}


def charger_json():
    """Charge le fichier JSON existant"""
    print(f"Chargement de {JSON_PATH}...")
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def integrer_propositions(data):
    """Intègre les nouvelles propositions dans le JSON"""
    modif_count = 0

    for categorie in data['categories']:
        for sous_theme in categorie['sousThemes']:
            sous_theme_id = sous_theme['id']

            # Intégration pour Bony
            if sous_theme_id in PROPOSITIONS_BONY:
                prop = PROPOSITIONS_BONY[sous_theme_id]
                # Vérifier si déjà présent
                if sous_theme['propositions'].get('bony') is None:
                    sous_theme['propositions']['bony'] = prop
                    print(f"✓ Ajouté Bony → {categorie['id']}/{sous_theme_id}")
                    modif_count += 1
                elif sous_theme['propositions']['bony']['texte'] != prop['texte']:
                    # Mise à jour si texte différent
                    sous_theme['propositions']['bony'] = prop
                    print(f"↻ Mis à jour Bony → {categorie['id']}/{sous_theme_id}")
                    modif_count += 1

            # Intégration pour Maximi
            if sous_theme_id in PROPOSITIONS_MAXIMI:
                prop = PROPOSITIONS_MAXIMI[sous_theme_id]
                # Vérifier si déjà présent
                if sous_theme['propositions'].get('maximi') is None:
                    sous_theme['propositions']['maximi'] = prop
                    print(f"✓ Ajouté Maximi → {categorie['id']}/{sous_theme_id}")
                    modif_count += 1
                elif sous_theme['propositions']['maximi']['texte'] != prop['texte']:
                    # Mise à jour si texte différent
                    sous_theme['propositions']['maximi'] = prop
                    print(f"↻ Mis à jour Maximi → {categorie['id']}/{sous_theme_id}")
                    modif_count += 1

    return modif_count


def sauvegarder_json(data):
    """Sauvegarde le JSON modifié"""
    print(f"\nSauvegarde dans {JSON_PATH}...")
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✓ Fichier sauvegardé avec succès")


def afficher_resume(data):
    """Affiche un résumé des propositions par candidat"""
    print("\n" + "="*70)
    print("RÉSUMÉ DES PROPOSITIONS PAR CANDIDAT")
    print("="*70)

    for candidat_id in ['bianchi', 'bony', 'maximi', 'darbois']:
        count = 0
        for categorie in data['categories']:
            for sous_theme in categorie['sousThemes']:
                if sous_theme['propositions'].get(candidat_id) is not None:
                    count += 1

        candidat_nom = next(c['nom'] for c in data['candidats'] if c['id'] == candidat_id)
        print(f"{candidat_nom:25} : {count:2} propositions")

    print("="*70)


def main():
    """Fonction principale"""
    print("="*70)
    print("INTÉGRATION DES PROGRAMMES - CLERMONT-FERRAND 2026")
    print("Candidats : Julien Bony (LR) + Marianne Maximi (LFI)")
    print("="*70 + "\n")

    # Vérifier que le fichier existe
    if not os.path.exists(JSON_PATH):
        print(f"❌ ERREUR : Le fichier {JSON_PATH} n'existe pas")
        return 1

    # Charger les données
    data = charger_json()

    # Intégrer les propositions
    print("\nIntégration des propositions...\n")
    modif_count = integrer_propositions(data)

    print(f"\n→ Total : {modif_count} modification(s) effectuée(s)")

    # Sauvegarder
    sauvegarder_json(data)

    # Afficher le résumé
    afficher_resume(data)

    print("\n✓ Intégration terminée avec succès !")
    print("\nN'oubliez pas de lancer : python scripts/valider_donnees.py")

    return 0


if __name__ == '__main__':
    sys.exit(main())
