#!/usr/bin/env python3
"""
Script pour ajouter 24 nouvelles propositions pour Hervé Gerbi
et passer programmeComplet à true dans grenoble-2026.json
"""

import json
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'elections', 'grenoble-2026.json')

# Les 15 nouvelles propositions (sous-thèmes actuellement null pour gerbi)
NOUVELLES_PROPOSITIONS = {
    "prevention-mediation": {
        "texte": "15 éducateurs de rue, médiateurs urbains, activités culturelles et sportives dans 10 quartiers prioritaires, soutien à France Victimes",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "pietons-circulation": {
        "texte": "Politique de mobilité équilibrée entre piétons, cyclistes, automobilistes et usagers des transports, espaces publics lisibles et partagés",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "logement-social": {
        "texte": "Urbanisme responsable et mesuré, quartiers mixtes et équilibrés intégrant mieux le logement social",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "acces-logement": {
        "texte": "Faciliter l'accès à la propriété pour les classes moyennes et les jeunes familles",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "jeunesse": {
        "texte": "Parcours de découverte des œuvres et du patrimoine sur temps scolaire, apprentissage artistique garanti dans le primaire, reconstruction des politiques d'éducation populaire",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "climat-adaptation": {
        "texte": "Écologie de solutions ancrée dans la recherche et l'innovation : rénovation des bâtiments, énergie, nature urbaine, qualité de l'air",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "budget-participatif": {
        "texte": "Comités de sécurité/prévention par quartier, concertation annuelle avec habitants et commerçants, évaluation publique annuelle",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "services-publics": {
        "texte": "Application citoyenne AllôGrenoble : alertes géolocalisées en un clic, suivi d'intervention en temps réel, cartographie des itinéraires sûrs, mode 'je rentre chez moi'",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "vie-associative": {
        "texte": "Partenariat stable, durable et transparent avec les associations, reconnaissance de la valeur du bénévolat et des initiatives de terrain",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "commerce-local": {
        "texte": "Soutenir l'économie de proximité et l'entrepreneuriat local, renforcer les centres commerciaux de quartier, faciliter l'installation des artisans",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "attractivite": {
        "texte": "Coopération métropolitaine : positionner Grenoble comme centre vivant en renforçant l'équilibre territorial avec les communes voisines",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "equipements-culturels": {
        "texte": "Création d'un office municipal de la culture autonome, plan stratégique culturel sur 5 ans, conventions pluriannuelles avec les acteurs culturels, simplification des procédures",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "evenements-creation": {
        "texte": "Charte de la nuit et conseil de la nuit, création d'un grand festival de musiques urbaines ancré dans les quartiers pour l'engagement des jeunes",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "accessibilite": {
        "texte": "Interconnexion renforcée entre modes de transport, accessibilité renforcée pour personnes âgées et à mobilité réduite",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
    "egalite-discriminations": {
        "texte": "Principes laïcs appliqués avec clarté dans les écoles et espaces publics, lutte contre toutes les discriminations, engagements concrets accessibilité, emploi, logement",
        "source": "Programme Hervé Gerbi 2026",
        "sourceUrl": "https://www.hervegerbi.fr/"
    },
}


def main():
    # Lire le fichier
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Passer programmeComplet à true pour gerbi
    for candidat in data['candidats']:
        if candidat['id'] == 'gerbi':
            candidat['programmeComplet'] = True
            print(f"programmeComplet passé à true pour {candidat['nom']}")
            break

    # 2. Ajouter les propositions sur les sous-thèmes vierges
    count_added = 0
    count_skipped = 0

    for categorie in data['categories']:
        for sous_theme in categorie['sousThemes']:
            st_id = sous_theme['id']
            if st_id in NOUVELLES_PROPOSITIONS:
                current_val = sous_theme['propositions'].get('gerbi')
                if current_val is None:
                    sous_theme['propositions']['gerbi'] = NOUVELLES_PROPOSITIONS[st_id]
                    count_added += 1
                    print(f"  + Ajouté : {categorie['id']}/{st_id}")
                else:
                    count_skipped += 1
                    print(f"  ~ Ignoré (déjà rempli) : {categorie['id']}/{st_id}")

    # 3. Écrire le fichier
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')  # newline finale

    print(f"\nRésumé : {count_added} propositions ajoutées, {count_skipped} ignorées (déjà remplies)")
    print(f"Fichier écrit : {os.path.abspath(FILE_PATH)}")

    # 4. Compter le total de propositions gerbi
    total_gerbi = 0
    for categorie in data['categories']:
        for sous_theme in categorie['sousThemes']:
            val = sous_theme['propositions'].get('gerbi')
            if val is not None:
                total_gerbi += 1
    print(f"Total propositions gerbi : {total_gerbi}")


if __name__ == '__main__':
    main()
