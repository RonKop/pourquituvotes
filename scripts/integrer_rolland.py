#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script d'intégration du programme de Johanna Rolland pour Nantes 2026
Programme complet de 200 mesures annoncé le 2 février 2026
"""

import sys
import io
import json
from pathlib import Path

# Force UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Chemin vers le fichier JSON
JSON_PATH = Path(__file__).parent.parent / "data" / "elections" / "nantes-2026.json"

# Propositions de Johanna Rolland à intégrer
# Source : programme "La Gauche Unie pour Nantes" 200 mesures, février 2026
PROPOSITIONS_ROLLAND = {
    # SÉCURITÉ
    "police-municipale": {
        "texte": "Nouveau commissariat dans un quartier prioritaire et poste de police fixe nocturne au Bouffay et vers le Hangar à bananes",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://www.francebleu.fr/pays-de-la-loire/loire-atlantique-44/nantes/juste-ecologique-solidaire-a-nantes-la-maire-sortante-johanna-rolland-presente-son-programme-pour-les-municipales-6077033"
    },

    # TRANSPORTS
    "transports-en-commun": {
        "texte": "Mise en circulation de deux nouvelles lignes de tramway",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://www.francebleu.fr/pays-de-la-loire/loire-atlantique-44/nantes/juste-ecologique-solidaire-a-nantes-la-maire-sortante-johanna-rolland-presente-son-programme-pour-les-municipales-6077033"
    },
    "velo-mobilites-douces": {
        "texte": "150 kilomètres supplémentaires de pistes cyclables sur le mandat",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://www.francebleu.fr/pays-de-la-loire/loire-atlantique-44/nantes/juste-ecologique-solidaire-a-nantes-la-maire-sortante-johanna-rolland-presente-son-programme-pour-les-municipales-6077033"
    },
    "stationnement": {
        "texte": "Parking moins cher pour ceux qui travaillent tôt",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://infos-media-nantes.fr/programme-johanna-rolland-nantes-2026-2/"
    },
    "tarifs-gratuite": {
        "texte": "Étendre la gratuité des transports en commun à 15 000 personnes supplémentaires à revenus modestes",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://www.francebleu.fr/pays-de-la-loire/loire-atlantique-44/nantes/juste-ecologique-solidaire-a-nantes-la-maire-sortante-johanna-rolland-presente-son-programme-pour-les-municipales-6077033"
    },

    # LOGEMENT
    "logement-social": {
        "texte": "Atteindre 40% de logements sociaux et 20% de logements à prix maîtrisés, soit 60% de logements régulés",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://www.francebleu.fr/pays-de-la-loire/loire-atlantique-44/nantes/juste-ecologique-solidaire-a-nantes-la-maire-sortante-johanna-rolland-presente-son-programme-pour-les-municipales-6077033"
    },

    # ÉDUCATION
    "petite-enfance": {
        "texte": "Création de 700 places de crèches municipales et associatives, et service de garde d'urgence pour les familles monoparentales",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://infos-media-nantes.fr/programme-johanna-rolland-nantes-2026-2/"
    },

    # ENVIRONNEMENT
    "espaces-verts": {
        "texte": "Moins de bitume en ville et plus de végétalisation des espaces publics",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://www.francebleu.fr/pays-de-la-loire/loire-atlantique-44/nantes/juste-ecologique-solidaire-a-nantes-la-maire-sortante-johanna-rolland-presente-son-programme-pour-les-municipales-6077033"
    },
    "renovation-energetique": {
        "texte": "Accélérer la rénovation des passoires énergétiques",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://www.francebleu.fr/pays-de-la-loire/loire-atlantique-44/nantes/juste-ecologique-solidaire-a-nantes-la-maire-sortante-johanna-rolland-presente-son-programme-pour-les-municipales-6077033"
    },

    # SANTÉ
    "centres-sante": {
        "texte": "Ouverture d'un centre de santé à la Bottière en mars 2026 et soutien aux centres de santé de proximité dans les quartiers prioritaires",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://infos-media-nantes.fr/programme-johanna-rolland-nantes-2026-2/"
    },
    "prevention-sante": {
        "texte": "Création d'une structure Fercam dédiée aux jeunes filles victimes de violences sexuelles et sexistes, ouverture en 2026 sur l'île de Nantes",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://www.francebleu.fr/pays-de-la-loire/loire-atlantique-44/nantes/juste-ecologique-solidaire-a-nantes-la-maire-sortante-johanna-rolland-presente-son-programme-pour-les-municipales-6077033"
    },

    # ÉCONOMIE
    "commerce-local": {
        "texte": "Création d'une foncière commerciale pour lutter contre la vacance et favoriser la diversité. Rénovation du marché de Talensac et développement de marchés en soirée et de marchés atypiques",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://hellogazettenantes.fr/municipales-johanna-rolland-devoile-de-premieres-mesures-axees-economie/"
    },
    "emploi-insertion": {
        "texte": "Soutien à l'économie sociale et solidaire et création d'une ressourcerie par quartier",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://hellogazettenantes.fr/municipales-johanna-rolland-devoile-de-premieres-mesures-axees-economie/"
    },
    "attractivite": {
        "texte": "Faire de Nantes un territoire pilote de l'économie régénérative",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://hellogazettenantes.fr/municipales-johanna-rolland-devoile-de-premieres-mesures-axees-economie/"
    },

    # SOLIDARITÉ
    "aide-sociale": {
        "texte": "Plateforme d'accompagnement dédiée aux familles monoparentales : aide quotidienne et garde d'urgence",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://infos-media-nantes.fr/programme-johanna-rolland-nantes-2026-2/"
    },
    "violences-femmes": {
        "texte": "Structure dédiée Fercam pour les mineures victimes de violences sexuelles et sexistes, ouverture 2026 sur l'île de Nantes",
        "source": "Programme officiel 2026",
        "sourceUrl": "https://www.francebleu.fr/pays-de-la-loire/loire-atlantique-44/nantes/juste-ecologique-solidaire-a-nantes-la-maire-sortante-johanna-rolland-presente-son-programme-pour-les-municipales-6077033"
    },
}

def main():
    """Intégration des propositions de Johanna Rolland dans le JSON Nantes"""

    print("🔄 Intégration du programme de Johanna Rolland (200 mesures)...")
    print(f"📁 Fichier : {JSON_PATH}")

    # Charger le JSON
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Vérifier que le candidat existe
    candidat_trouve = False
    for candidat in data['candidats']:
        if candidat['id'] == 'rolland':
            candidat_trouve = True
            break

    if not candidat_trouve:
        print("❌ Erreur : candidat 'rolland' non trouvé dans le JSON")
        sys.exit(1)

    # Compteurs
    nb_ajouts = 0
    nb_mises_a_jour = 0
    nb_sans_changement = 0

    # Parcourir les catégories et intégrer les propositions
    for categorie in data['categories']:
        for sous_theme in categorie['sousThemes']:
            sous_theme_id = sous_theme['id']

            if sous_theme_id in PROPOSITIONS_ROLLAND:
                proposition_actuelle = sous_theme['propositions'].get('rolland')
                nouvelle_proposition = PROPOSITIONS_ROLLAND[sous_theme_id]

                if proposition_actuelle is None:
                    # Ajout d'une nouvelle proposition
                    sous_theme['propositions']['rolland'] = nouvelle_proposition
                    nb_ajouts += 1
                    print(f"  ✅ Ajouté : {categorie['id']} > {sous_theme_id}")
                elif proposition_actuelle != nouvelle_proposition:
                    # Mise à jour d'une proposition existante
                    sous_theme['propositions']['rolland'] = nouvelle_proposition
                    nb_mises_a_jour += 1
                    print(f"  🔄 Mis à jour : {categorie['id']} > {sous_theme_id}")
                else:
                    # Proposition identique, pas de changement
                    nb_sans_changement += 1

    # Mettre à jour programmeComplet si au moins 15 sous-thèmes
    nb_propositions_total = nb_ajouts + nb_mises_a_jour + nb_sans_changement

    for candidat in data['candidats']:
        if candidat['id'] == 'rolland':
            ancien_statut = candidat['programmeComplet']
            candidat['programmeComplet'] = nb_propositions_total >= 15

            if ancien_statut != candidat['programmeComplet']:
                print(f"\n  ℹ️  programmeComplet : {ancien_statut} → {candidat['programmeComplet']}")
            break

    # Sauvegarder le JSON
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Afficher le résumé
    print("\n" + "=" * 60)
    print("✅ INTÉGRATION TERMINÉE")
    print("=" * 60)
    print(f"  📊 Nouvelles propositions ajoutées : {nb_ajouts}")
    print(f"  🔄 Propositions mises à jour : {nb_mises_a_jour}")
    print(f"  ⏭️  Propositions sans changement : {nb_sans_changement}")
    print(f"  📈 Total propositions Rolland : {nb_propositions_total}")
    print(f"  📄 Programme complet : {'Oui' if nb_propositions_total >= 15 else 'Non'}")
    print("=" * 60)
    print("\n⚠️  PROCHAINES ÉTAPES :")
    print("  1. Exécuter : python scripts/valider_donnees.py")
    print("  2. Tester le site en local")
    print("=" * 60)

if __name__ == "__main__":
    main()
