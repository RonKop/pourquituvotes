#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'intégration des programmes de Stéphane Baly et Violette Spillebout
pour les municipales 2026 à Lille

Ce script ajoute les propositions détaillées de ces deux candidats
dans le fichier JSON lille-2026.json
"""

import sys
import io
import json
from pathlib import Path

# Configuration UTF-8 pour stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Chemins des fichiers
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "elections"
JSON_FILE = DATA_DIR / "lille-2026.json"

# Propositions pour Stéphane Baly (EELV)
PROPS_BALY = {
    # Sécurité & Prévention
    "police-municipale": {
        "texte": "Garantir la tranquillité publique avec 1 policier municipal pour 1 000 habitants",
        "source": "lilledemain.fr - Notre programme, 10 mesures phares",
        "sourceUrl": "https://lilledemain.fr/notre-programme/"
    },
    "prevention-mediation": {
        "texte": "Création de postes de prévention dans tous les quartiers de la ville",
        "source": "France 3 Hauts-de-France, février 2026",
        "sourceUrl": "https://france3-regions.franceinfo.fr/"
    },

    # Transports & Mobilité
    "transports-en-commun": {
        "texte": "Rendre les bus gratuits et le métro fiable au sein d'un réseau renforcé. Créer une ceinture verte de la Deûle à Euralille avec un tramway reliant Wambrechies aux gares",
        "source": "lilledemain.fr et Mediacités",
        "sourceUrl": "https://www.mediacites.fr/enquete/lille/2026/02/13/municipales-2026-a-lille-le-baly-2026-peut-il-faire-mieux-que-le-baly-2020/"
    },
    "velo-mobilites-douces": {
        "texte": "Développer les infrastructures cyclables et la logistique du dernier kilomètre en mode durable (vélos, triporteurs, camionnettes électriques)",
        "source": "Interview Daily N, février 2026",
        "sourceUrl": "https://dailyn.app/lille/blog/stephane-baly-candidat-eelv-lille-interview-commercants"
    },
    "pietons-circulation": {
        "texte": "Créer 10 cœurs de quartiers apaisés et végétalisés, piétonniser la place Schuman dans le Vieux-Lille. Transformer le boulevard Schuman en boulevard urbain",
        "source": "France Bleu Nord et Mediacités",
        "sourceUrl": "https://www.mediacites.fr/enquete/lille/2026/02/13/municipales-2026-a-lille-le-baly-2026-peut-il-faire-mieux-que-le-baly-2020/"
    },
    "stationnement": {
        "texte": "Instaurer 1€/mois de stationnement résidentiel et un pass visiteur",
        "source": "lilledemain.fr - Notre programme, 10 mesures phares",
        "sourceUrl": "https://lilledemain.fr/notre-programme/"
    },
    "tarifs-gratuite": {
        "texte": "Gratuité des transports en commun pour tous les usagers",
        "source": "Nord Actu, février 2026",
        "sourceUrl": "https://nordactu.fr/elections-municipales-2026-a-lille-le-baly-2026-saura-t-il-surpasser-les-resultats-de-2020/"
    },

    # Logement
    "logements-vacants": {
        "texte": "Remettre 3 000 logements vacants sur le marché locatif",
        "source": "Vert, février 2026",
        "sourceUrl": "https://vert.eco/"
    },
    "acces-logement": {
        "texte": "Créer des logements abordables et de qualité, dont 2 000 à moins de 300€/mois",
        "source": "lilledemain.fr - Notre programme, 10 mesures phares",
        "sourceUrl": "https://lilledemain.fr/notre-programme/"
    },
    "encadrement-loyers": {
        "texte": "Mettre en place un encadrement des loyers pour limiter les hausses excessives",
        "source": "lilledemain.fr - Programme logement",
        "sourceUrl": "https://lilledemain.fr/notre-programme/"
    },

    # Éducation & Jeunesse
    "petite-enfance": {
        "texte": "Accompagnement des enfants dès la petite enfance pour garantir épanouissement et réussite scolaire",
        "source": "lilledemain.fr - Notre programme, Éducation & Jeunesse",
        "sourceUrl": "https://lilledemain.fr/notre-programme/"
    },
    "cantines-fournitures": {
        "texte": "Servir des repas 100% bios et locaux dans les cantines, dès la crèche",
        "source": "lilledemain.fr - Notre programme, 10 mesures phares",
        "sourceUrl": "https://lilledemain.fr/notre-programme/"
    },

    # Environnement & Transition écologique
    "espaces-verts": {
        "texte": "Ouvrir un grand parc à Saint-Sauveur et un espace de baignade gratuit dans la Deûle. Garantir un espace vert à moins de 3 minutes de chez soi avec débitumage massif. Créer 10 cœurs de quartiers végétalisés",
        "source": "lilledemain.fr et France Bleu Nord",
        "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-lille-ce-qu-il-faut-retenir-du-programme-d-eelv-1580594068"
    },
    "climat-adaptation": {
        "texte": "Accélérer la transition écologique de Lille avec un plan ambitieux d'adaptation au changement climatique",
        "source": "lilledemain.fr - Programme environnement",
        "sourceUrl": "https://lilledemain.fr/notre-programme/"
    },
    "alimentation-durable": {
        "texte": "Promouvoir l'alimentation durable et circuits courts dans la restauration collective",
        "source": "lilledemain.fr - Programme environnement",
        "sourceUrl": "https://lilledemain.fr/notre-programme/"
    },

    # Santé & Accès aux soins
    "centres-sante": {
        "texte": "Équiper chaque quartier de la ville d'une maison de santé pour renforcer l'offre médicale. Faire de la santé une priorité municipale",
        "source": "lilledemain.fr et Mediacités",
        "sourceUrl": "https://www.mediacites.fr/enquete/lille/2026/02/13/municipales-2026-a-lille-le-baly-2026-peut-il-faire-mieux-que-le-baly-2020/"
    },

    # Démocratie & Vie citoyenne
    "budget-participatif": {
        "texte": "Donner aux Lillois leur mot à dire sur les projets structurants via des mécanismes de démocratie participative renforcée",
        "source": "France Bleu Nord, février 2026",
        "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-lille-ce-qu-il-faut-retenir-du-programme-d-eelv-1580594068"
    },

    # Économie & Emploi
    "commerce-local": {
        "texte": "Encadrer les loyers des commerces via la préemption commerciale pour soutenir leur diversité et lutter contre les hausses excessives",
        "source": "Daily N et lilledemain.fr",
        "sourceUrl": "https://dailyn.app/lille/blog/stephane-baly-candidat-eelv-lille-interview-commercants"
    },

    # Culture & Patrimoine
    "equipements-culturels": {
        "texte": "Ouvrir une grande médiathèque aux horaires étendus",
        "source": "lilledemain.fr - Notre programme, 10 mesures phares",
        "sourceUrl": "https://lilledemain.fr/notre-programme/"
    },

    # Urbanisme & Cadre de vie
    "amenagement-urbain": {
        "texte": "Couvrir le périphérique pour relier Lille-Sud à Wazemmes et créer de nouveaux espaces de vie",
        "source": "Mediacités, février 2026",
        "sourceUrl": "https://www.mediacites.fr/enquete/lille/2026/02/13/municipales-2026-a-lille-le-baly-2026-peut-il-faire-mieux-que-le-baly-2020/"
    },

    # Solidarité & Égalité
    "aide-sociale": {
        "texte": "Combattre les précarités avec des services adaptés aux besoins locaux (27% des habitants sous le seuil de pauvreté). Renforcer la solidarité entre habitants",
        "source": "lilledemain.fr - Notre programme, Lutte contre les inégalités",
        "sourceUrl": "https://lilledemain.fr/notre-programme/"
    },
}

# Propositions pour Violette Spillebout (Renaissance)
PROPS_SPILLEBOUT = {
    # Sécurité & Prévention
    "police-municipale": {
        "texte": "Recruter 100 policiers municipaux supplémentaires et créer une police municipale montée pour renforcer la sécurité",
        "source": "vspillebout.fr et France 3 Hauts-de-France",
        "sourceUrl": "https://france3-regions.franceinfo.fr/hauts-de-france/nord-0/lille/municipales-2026-la-securite-grand-theme-de-campagne-que-proposent-les-candidats-a-lille-3279884.html"
    },
    "videoprotection": {
        "texte": "Déploiement de 2 000 caméras de vidéosurveillance sur le territoire lillois pour lutter contre la délinquance",
        "source": "France 3 Hauts-de-France et fairerespirer.fr",
        "sourceUrl": "https://fairerespirer.fr/2025/10/videoprotection/"
    },
    "prevention-mediation": {
        "texte": "Créer une brigade de tranquillité pour lutter contre les incivilités et la délinquance dans les quartiers",
        "source": "vspillebout.fr - Programme sécurité",
        "sourceUrl": "https://vspillebout.fr/2020/01/reprendre-la-securite-de-lille-en-main/"
    },

    # Transports & Mobilité
    "transports-en-commun": {
        "texte": "Décarboner la métropole avec plus de transports publics. Négocier une garantie de ponctualité avec Ilévia, similaire à celle de la SNCF, pour compenser en cas de défaut de service",
        "source": "Péperenews et vspillebout.fr",
        "sourceUrl": "https://www.peperenews.fr/violette-spillebout-la-deputee-candidate-de-lille-garantit-que-rien-nest-joue-pour-2026/"
    },
    "stationnement": {
        "texte": "Faciliter la circulation et le stationnement pour les automobilistes lillois",
        "source": "violette2026.fr - Programme mobilité",
        "sourceUrl": "https://violette2026.fr/"
    },

    # Logement
    "logement-social": {
        "texte": "Augmenter le nombre de logements sociaux pour répondre aux besoins des habitants de Lille",
        "source": "Site officiel Violette Spillebout",
        "sourceUrl": "https://vspillebout.fr/"
    },
    "logements-vacants": {
        "texte": "Remettre 8 000 logements vacants sur le marché, dont certains sont vacants depuis plusieurs décennies",
        "source": "France 3 Hauts-de-France, février 2026",
        "sourceUrl": "https://france3-regions.franceinfo.fr/"
    },
    "acces-logement": {
        "texte": "Mieux loger les Lilloises et Lillois avec des logements de qualité et accessibles",
        "source": "violette2026.fr - Programme logement",
        "sourceUrl": "https://violette2026.fr/"
    },

    # Éducation & Jeunesse
    "ecoles-renovation": {
        "texte": "Rénover et améliorer les établissements scolaires pour offrir un meilleur cadre d'apprentissage",
        "source": "Site officiel Violette Spillebout",
        "sourceUrl": "https://vspillebout.fr/"
    },
    "jeunesse": {
        "texte": "Protéger et éduquer les jeunes avec des programmes adaptés à leurs besoins",
        "source": "violette2026.fr - Programme jeunesse",
        "sourceUrl": "https://violette2026.fr/"
    },

    # Environnement & Transition écologique
    "espaces-verts": {
        "texte": "Créer et développer les espaces verts pour améliorer la qualité de vie urbaine et végétaliser Lille",
        "source": "violette2026.fr - Lille verte et bleue",
        "sourceUrl": "https://vspillebout.fr/municipales-2020/programme/lille-verte-et-bleue/"
    },
    "proprete-dechets": {
        "texte": "Créer un Comité anti-déchets sauvages et sanctionner les dépôts illégaux comme à Tourcoing (426 caméras et vidéo-verbalisation depuis 2024). Faire de la propreté une priorité",
        "source": "vspillebout.fr et France 3 HDF",
        "sourceUrl": "https://vspillebout.fr/2024/10/14702/"
    },

    # Santé & Accès aux soins
    "prevention-sante": {
        "texte": "Promouvoir le sport-santé et développer la prévention sanitaire pour tous",
        "source": "violette2026.fr - Programme santé",
        "sourceUrl": "https://violette2026.fr/"
    },

    # Économie & Emploi
    "emploi-insertion": {
        "texte": "Développer l'emploi et soutenir l'insertion professionnelle des jeunes et des demandeurs d'emploi. Retrouver un dynamisme économique",
        "source": "violette2026.fr - Programme économie",
        "sourceUrl": "https://violette2026.fr/"
    },
    "commerce-local": {
        "texte": "Soutenir le commerce local et l'attractivité des centres-villes",
        "source": "violette2026.fr - Programme commerce",
        "sourceUrl": "https://violette2026.fr/"
    },
    "attractivite": {
        "texte": "Promouvoir Lille en Europe et renforcer son attractivité internationale",
        "source": "violette2026.fr - Programme attractivité",
        "sourceUrl": "https://violette2026.fr/"
    },

    # Culture & Patrimoine
    "equipements-culturels": {
        "texte": "Développer l'accès à la culture pour tous avec de nouveaux équipements culturels",
        "source": "violette2026.fr - Programme culture",
        "sourceUrl": "https://violette2026.fr/"
    },

    # Sport & Loisirs
    "sport-pour-tous": {
        "texte": "Promouvoir le sport pour tous et développer les activités sportives accessibles à toute la population",
        "source": "violette2026.fr - Programme sport",
        "sourceUrl": "https://violette2026.fr/"
    },

    # Solidarité & Égalité
    "aide-sociale": {
        "texte": "Lutter contre la pauvreté et les discriminations. Renforcer l'aide sociale pour les plus démunis",
        "source": "violette2026.fr - Programme solidarité",
        "sourceUrl": "https://violette2026.fr/"
    },
    "egalite-discriminations": {
        "texte": "Combattre les discriminations et promouvoir l'égalité pour tous les Lillois",
        "source": "violette2026.fr - Programme égalité",
        "sourceUrl": "https://violette2026.fr/"
    },

    # Démocratie & Vie citoyenne
    "transparence": {
        "texte": "Garantir une mairie exemplaire avec plus de transparence dans la gestion municipale",
        "source": "vspillebout.fr - Une mairie exemplaire",
        "sourceUrl": "https://vspillebout.fr/municipales-2020/programme/une-mairie-exemplaire/"
    },
}

def main():
    """Fonction principale"""
    print("=" * 80)
    print("INTÉGRATION DES PROGRAMMES - Stéphane Baly et Violette Spillebout")
    print("Lille - Municipales 2026")
    print("=" * 80)

    # Vérification du fichier JSON
    if not JSON_FILE.exists():
        print(f"\n❌ ERREUR : Le fichier {JSON_FILE} n'existe pas")
        return 1

    print(f"\n📖 Lecture du fichier : {JSON_FILE}")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"   Ville : {data['ville']}")
    print(f"   Candidats actuels : {len(data['candidats'])}")
    print(f"   Catégories : {len(data['categories'])}")

    # Intégration des propositions
    candidats_integres = []

    for candidat_id, props in [("baly", PROPS_BALY), ("spillebout", PROPS_SPILLEBOUT)]:
        # Trouver le nom du candidat
        candidat = next((c for c in data['candidats'] if c['id'] == candidat_id), None)
        if not candidat:
            print(f"\n⚠️  Candidat {candidat_id} non trouvé dans le JSON")
            continue

        print(f"\n📝 Intégration de {candidat['nom']} ({candidat['liste']})")
        print(f"   {len(props)} propositions à intégrer")

        count = 0
        for categorie in data['categories']:
            for sous_theme in categorie['sousThemes']:
                if sous_theme['id'] in props:
                    # Mettre à jour ou ajouter la proposition
                    sous_theme['propositions'][candidat_id] = props[sous_theme['id']]
                    count += 1

        print(f"   ✅ {count} propositions intégrées")
        candidats_integres.append(candidat['nom'])

        # Mettre à jour programmeComplet si applicable
        # Baly : 21 propositions détaillées → programmeComplet = true
        # Spillebout : 16 propositions détaillées → programmeComplet = true
        if candidat_id == "baly" and count >= 15:
            candidat['programmeComplet'] = True
            print(f"   ✅ programmeComplet = true ({count} propositions)")
        elif candidat_id == "spillebout" and count >= 15:
            candidat['programmeComplet'] = True
            print(f"   ✅ programmeComplet = true ({count} propositions)")

    # Sauvegarde du fichier JSON
    print(f"\n💾 Sauvegarde du fichier JSON...")
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Fichier sauvegardé : {JSON_FILE}")

    # Résumé
    print("\n" + "=" * 80)
    print("✅ INTÉGRATION TERMINÉE")
    print("=" * 80)
    print(f"\nCandidats intégrés : {', '.join(candidats_integres)}")
    print("\nPROCHAINES ÉTAPES :")
    print("1. Lancer la validation : python scripts/valider_donnees.py")
    print("2. Tester le site : python -m http.server 8000")
    print("3. Vérifier l'affichage des propositions sur le comparateur")
    print("\n" + "=" * 80)

    return 0

if __name__ == "__main__":
    sys.exit(main())
