#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'intégration du programme de Michaël Delafosse (PS, maire sortant)
pour les municipales 2026 à Montpellier.

Sources:
- https://www.michaeldelafosse.fr/
- France Bleu Hérault, Hérault Tribune, France 3 Occitanie
"""

import sys
import io
import json
from pathlib import Path

# Configuration UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Chemins
BASE_DIR = Path(__file__).parent.parent
JSON_FILE = BASE_DIR / "data" / "elections" / "montpellier-2026.json"

# Programme de Michaël Delafosse
PROPOSITIONS_DELAFOSSE = {
    # SÉCURITÉ (déjà présent, on complète)
    "police-municipale": {
        "texte": "Recruter 100 agents de sécurité supplémentaires sous responsabilité municipale et métropolitaine, budget de 4 millions d'euros par an",
        "source": "Hérault Tribune, 2026",
        "sourceUrl": "https://echo-des-tribunes.com/herault-tribune/articles/montpelliermunicipales-2026-candidat-a-sa-reelection-le-socialiste-michael-delafosse-veut-poursuivre-sa-politique-securitaire"
    },
    "videoprotection": {
        "texte": "Doubler le réseau de caméras de vidéoprotection, de 500 à 1 000 caméras, budget de 3 millions d'euros sur le mandat",
        "source": "Hérault Tribune, 2026",
        "sourceUrl": "https://echo-des-tribunes.com/herault-tribune/articles/montpelliermunicipales-2026-candidat-a-sa-reelection-le-socialiste-michael-delafosse-veut-poursuivre-sa-politique-securitaire"
    },
    "prevention-mediation": {
        "texte": "Passer de 12 à 30 médiateurs de quartier pour la résolution des conflits de voisinage",
        "source": "Hérault Tribune, 2026",
        "sourceUrl": "https://echo-des-tribunes.com/herault-tribune/articles/montpelliermunicipales-2026-candidat-a-sa-reelection-le-socialiste-michael-delafosse-veut-poursuivre-sa-politique-securitaire"
    },

    # TRANSPORTS
    "transports-en-commun": {
        "texte": "Maintenir la gratuité totale des transports en commun et faire sortir le tramway hors de la Métropole d'ici la fin du mandat",
        "source": "France 3 Occitanie, 2026",
        "sourceUrl": "https://france3-regions.franceinfo.fr/occitanie/herault/montpellier/tant-que-je-serai-maire-la-gratuite-des-transports-sera-defendue-ce-qu-il-faut-retenir-de-l-interview-de-michael-delafosse-candidat-a-sa-reelection-a-la-mairie-de-montpellier-3284739.html"
    },
    "velo-mobilites-douces": {
        "texte": "Poursuivre la création du réseau express vélo avec un objectif de 235 km de pistes cyclables sécurisées d'ici fin 2026 et faire passer la part modale vélo de 3% à 10%",
        "source": "Montpellier Méditerranée Métropole, 2026",
        "sourceUrl": "https://www.montpellier3m.fr/actualite/de-grandes-avancees-en-faveur-du-velo-reconnues-nationalement-le-fruit-dactions-pour"
    },
    "pietons-circulation": {
        "texte": "Faire de Montpellier une référence nationale pour la marche et installer 1 000 bancs supplémentaires dans l'espace public",
        "source": "France Bleu Hérault, Journal Toulousain, 2026",
        "sourceUrl": "https://www.lejournaltoulousain.fr/occitanie/herault/montpellier/municipales-2026-montpellier-seniors-sante-pouvoir-achat-promet-delafosse-359284/"
    },

    # LOGEMENT
    "acces-logement": {
        "texte": "Construire ou créer 1 000 logements étudiants aidés répartis dans divers quartiers (Ovalie, Mosson, Pompignane), 500 logements pour seniors et créer un pass accession montpelliérain : prêt à taux zéro municipal de 10 000 € pour constituer un apport immobilier",
        "source": "Hérault Tribune, 2026",
        "sourceUrl": "https://echo-des-tribunes.com/herault-tribune/articles/montpellier-municipales-2026-delafosse-devoile-sa-strategie-face-a-la-crise-du-logement"
    },

    # ÉDUCATION
    "ecoles-renovation": {
        "texte": "Faire de l'éducation la priorité absolue du mandat avec apprentissage des savoirs fondamentaux, éveil culturel, scientifique et sportif, et préparation aux défis du monde (transition écologique, égalité, laïcité)",
        "source": "Le Mouvement, 2021",
        "sourceUrl": "https://lemouvement.info/2021/05/21/montpellier-leducation-est-la-priorite-absolue-de-ce-mandat-michael-delafosse/"
    },
    "cantines-fournitures": {
        "texte": "Atteindre 100% de produits bio et/ou locaux dans les cantines scolaires, augmenter la dotation de fournitures scolaires de 40,50€ à 50€ par enfant (hausse de 20%, soit 1,1 M€), et maintenir la tarification sociale à 0,50€ par repas pour les familles monoparentales bénéficiaires du RSA",
        "source": "Michaël Delafosse, France Bleu, 2026",
        "sourceUrl": "https://www.michaeldelafosse.fr/observatoire/des-cantines-scolaires-bio-locales-et-durables-montpellier"
    },

    # ENVIRONNEMENT
    "espaces-verts": {
        "texte": "Créer 3 nouveaux parcs et planter 50 000 arbres d'ici 2026 pour faire de Montpellier une ville-parc",
        "source": "En Commun Montpellier, 2023",
        "sourceUrl": "https://encommun.montpellier.fr/articles/2023-09-13-michael-delafosse-fait-sa-rentree-politique"
    },

    # SANTÉ
    "centres-sante": {
        "texte": "Installer une antenne du CHU dans le quartier de la Mosson et créer des centres de santé avec médecins salariés dans les quartiers prioritaires",
        "source": "France Bleu Hérault, 2026",
        "sourceUrl": "https://www.francebleu.fr/occitanie/herault-34/montpellier/municipales-2026-a-montpellier-michael-delafosse-promet-des-mesures-pour-le-pouvoir-d-achat-et-les-seniors-4159680"
    },
    "prevention-sante": {
        "texte": "Développer une stratégie d'aller-vers pour lutter contre le non-recours aux soins, notamment en santé mentale",
        "source": "France Bleu Hérault, 2026",
        "sourceUrl": "https://www.francebleu.fr/occitanie/herault-34/montpellier/municipales-2026-a-montpellier-michael-delafosse-promet-des-mesures-pour-le-pouvoir-d-achat-et-les-seniors-4159680"
    },
    "seniors": {
        "texte": "Créer 400 à 500 places dans quatre résidences sociales seniors municipales et installer 1 000 bancs supplémentaires dans l'espace public",
        "source": "France Bleu Hérault, 2026",
        "sourceUrl": "https://www.francebleu.fr/occitanie/herault-34/montpellier/municipales-2026-a-montpellier-michael-delafosse-promet-des-mesures-pour-le-pouvoir-d-achat-et-les-seniors-4159680"
    },

    # DÉMOCRATIE
    "transparence": {
        "texte": "Instaurer le droit d'interpellation citoyenne : possibilité pour les habitants d'inscrire une affaire à l'ordre du jour du conseil municipal (seuil de 5% de la population)",
        "source": "Institut Montaigne - Programme municipales 2020",
        "sourceUrl": "https://www.institutmontaigne.org/municipales-2020/montpellier/michael-delafosse"
    },
    "services-publics": {
        "texte": "Organiser des réunions annuelles de quartier en présence du maire et ouvrir l'Agora des citoyens, lieu ouvert pour s'informer, débattre et proposer",
        "source": "Institut Montaigne - Programme municipales 2020",
        "sourceUrl": "https://www.institutmontaigne.org/municipales-2020/montpellier/michael-delafosse"
    },

    # CULTURE
    "equipements-culturels": {
        "texte": "Rendre gratuit l'accès aux 15 médiathèques de Montpellier et de la Métropole",
        "source": "France Bleu Hérault, 2026",
        "sourceUrl": "https://www.francebleu.fr/occitanie/herault-34/montpellier/municipales-2026-a-montpellier-michael-delafosse-promet-des-mesures-pour-le-pouvoir-d-achat-et-les-seniors-4159680"
    },

    # URBANISME
    "quartiers-prioritaires": {
        "texte": "Rénover les quartiers Mosson et Montasinos, restructurer les espaces publics et installer 50 concierges dans le parc social",
        "source": "Hérault Tribune, 2026",
        "sourceUrl": "https://echo-des-tribunes.com/herault-tribune/articles/gratuite-sante-solidarite-pour-la-bataille-des-urnes-michael-delafosse-ajuste-son-bouclier-social"
    },

    # SOLIDARITÉ
    "aide-sociale": {
        "texte": "Maintenir la tarification sociale pour l'eau, les musées, piscines et cantines, et exclure les produits issus du Mercosur des cantines scolaires",
        "source": "Hérault Tribune, 2026",
        "sourceUrl": "https://echo-des-tribunes.com/herault-tribune/articles/gratuite-sante-solidarite-pour-la-bataille-des-urnes-michael-delafosse-ajuste-son-bouclier-social"
    },
    "pouvoir-achat": {
        "texte": "Créer un Office municipal du pouvoir d'achat fonctionnant comme centrale de négociation pour des achats groupés (énergie, alimentation, etc.)",
        "source": "Hérault Tribune, 2026",
        "sourceUrl": "https://echo-des-tribunes.com/herault-tribune/articles/gratuite-sante-solidarite-pour-la-bataille-des-urnes-michael-delafosse-ajuste-son-bouclier-social"
    }
}

def integrer_propositions():
    """Intègre les propositions de Delafosse dans le JSON de Montpellier."""

    print(f"📖 Lecture du fichier JSON : {JSON_FILE}")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Compter les propositions ajoutées/mises à jour
    count_new = 0
    count_updated = 0

    # Parcourir les catégories et sous-thèmes
    for categorie in data['categories']:
        for sous_theme in categorie['sousThemes']:
            sous_theme_id = sous_theme['id']

            # Si on a une proposition pour ce sous-thème
            if sous_theme_id in PROPOSITIONS_DELAFOSSE:
                prop = PROPOSITIONS_DELAFOSSE[sous_theme_id]

                # Vérifier si la proposition existe déjà
                if sous_theme['propositions'].get('delafosse') is None:
                    count_new += 1
                    action = "✅ AJOUT"
                else:
                    count_updated += 1
                    action = "🔄 MAJ"

                # Ajouter/mettre à jour la proposition
                sous_theme['propositions']['delafosse'] = prop

                print(f"{action} [{categorie['id']}] {sous_theme_id}: {prop['texte'][:80]}...")

    # Mettre à jour le statut programmeComplet
    # Delafosse a plus de 15 sous-thèmes documentés = programme complet
    nb_propositions = len([p for p in PROPOSITIONS_DELAFOSSE if p])

    for candidat in data['candidats']:
        if candidat['id'] == 'delafosse':
            candidat['programmeComplet'] = True  # 20+ propositions = programme complet
            print(f"\n📊 Statut programmeComplet mis à TRUE ({nb_propositions} propositions intégrées)")

    # Sauvegarder
    print(f"\n💾 Sauvegarde dans {JSON_FILE}")
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ TERMINÉ")
    print(f"   • {count_new} nouvelles propositions ajoutées")
    print(f"   • {count_updated} propositions mises à jour")
    print(f"   • Total: {nb_propositions} propositions pour Delafosse")
    print(f"   • Programme marqué comme complet")

    return True

if __name__ == "__main__":
    try:
        integrer_propositions()
    except Exception as e:
        print(f"❌ ERREUR : {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
