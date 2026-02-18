# -*- coding: utf-8 -*-
"""
Script d'intégration des programmes complets de 3 candidats à Marseille 2026
Candidats : Benoît Payan (PS), Martine Vassal (LR), Franck Allisio (RN)
"""

import json
import sys
import io
from pathlib import Path

# Configuration UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Chemins
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / 'data' / 'elections'
JSON_FILE = DATA_DIR / 'marseille-2026.json'

# Nouvelles propositions par candidat
PROPOSITIONS = {
    'payan': {
        # Sécurité
        'videoprotection': {
            'texte': 'Extension de la vidéoprotection dans le cadre du doublement de la police municipale',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        'prevention-mediation': {
            'texte': 'Création d\'une police de la propreté avec 80 agents pour lutter contre les incivilités',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        # Transports
        'stationnement': {
            'texte': 'Amélioration de la gestion du stationnement dans le cadre de la politique de mobilité',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        # Logement
        'logements-vacants': {
            'texte': 'Lutte contre les logements vacants dans le cadre du programme de réhabilitation massive',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        # Éducation
        'petite-enfance': {
            'texte': 'Renforcement de l\'offre de petite enfance et création de nouvelles places en crèche',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        'ecoles-renovation': {
            'texte': 'Nouveau plan écoles avec rénovation et modernisation des infrastructures scolaires',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        'periscolaire-loisirs': {
            'texte': 'Petits déjeuners gratuits pour 15 000 écoliers marseillais',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        # Environnement
        'climat-adaptation': {
            'texte': 'Création d\'un grand parc municipal dans le massif de l\'Étoile pour adapter la ville au changement climatique',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        'proprete-dechets': {
            'texte': 'Plan propreté avec création d\'une police de la propreté de 80 agents et renforcement des services de nettoyage',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        # Culture
        'equipements-culturels': {
            'texte': 'Développement des équipements culturels et renforcement de l\'offre culturelle pour tous',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        # Sport
        'equipements-sportifs': {
            'texte': 'Création du plus grand boulodrome couvert du monde à vocation internationale du côté de Saint-Marcel',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        # Urbanisme
        'amenagement-urbain': {
            'texte': 'Projet Grandes Rives de la Méditerranée : grande promenade littorale du Nord au Sud avec jardins, espaces paysagers, belvédères, offre sportive et commerciale',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
        # Economie
        'attractivite': {
            'texte': 'Création d\'une Société du Grand Marseille pour porter les grands projets de long terme',
            'source': 'Programme Pour Marseille 2026',
            'sourceUrl': 'https://www.pourmarseille.fr/'
        },
    },
    'vassal': {
        # Sécurité
        'videoprotection': {
            'texte': 'Relance massive de la vidéoprotection avec augmentation significative du parc de caméras',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        'prevention-mediation': {
            'texte': 'Plan Argos : dispositif à 15 millions d\'euros coordonnant Ville, école, justice, État et acteurs sociaux pour agir en amont sur la délinquance',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        # Transports
        'transports-en-commun': {
            'texte': 'Extension des horaires métro et tramway les vendredis et samedis soir (métro jusqu\'à 1h). Connexion de tous les quartiers par les transports',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        # Logement
        'logement-social': {
            'texte': 'Fin de l\'habitat indigne avec programme massif de réhabilitation',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        # Éducation
        'petite-enfance': {
            'texte': 'Doublement des places en crèche et investissement massif dans la petite enfance',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        'ecoles-renovation': {
            'texte': 'Plan Condorcet : audit général de la SPEM, rénovation et construction de 60 écoles par an',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        # Environnement
        'proprete-dechets': {
            'texte': 'Faire de Marseille une ville propre avec renforcement des services de nettoyage',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        # Culture
        'equipements-culturels': {
            'texte': 'Création d\'une école de cuisine sur une partie du Centre Bourse. Académie pour le sport féminin',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://marsactu.fr/municipales-2026-martine-vassal-devoile-un-peu-ses-ambitions-culturelles-pour-marseille/'
        },
        'evenements-creation': {
            'texte': 'Faire de Marseille une capitale culturelle et touristique. Accueil de tournois internationaux (football, e-sports)',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        # Sport
        'equipements-sportifs': {
            'texte': 'Projet de parc Borély du 22e siècle avec espaces numériques et inclusifs',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://marsactu.fr/municipales-2026-martine-vassal-devoile-un-peu-ses-ambitions-culturelles-pour-marseille/'
        },
        # Urbanisme
        'amenagement-urbain': {
            'texte': 'Plan Canebière : préemption de locaux vacants pour revitaliser le centre-ville',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        # Economie
        'commerce-local': {
            'texte': 'Soutien au commerce local via le Plan Canebière et baisse de la taxe foncière',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        'attractivite': {
            'texte': 'Installation d\'un casino à Marseille pour générer environ 120 millions d\'euros sur le mandat. Faire de Marseille une station balnéaire comme les grandes villes méditerranéennes',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
        # Solidarité
        'pouvoir-achat': {
            'texte': 'Réduction de la taxe foncière pour soutenir le pouvoir d\'achat des Marseillais',
            'source': 'Programme 13 axes prioritaires 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
        },
    },
    'allisio': {
        # Sécurité
        'videoprotection': {
            'texte': 'Doublement du nombre de caméras de vidéoprotection pour atteindre 4 000 caméras',
            'source': 'Programme Marseille en ordre 2026',
            'sourceUrl': 'https://franckallisio2026.fr/'
        },
        'prevention-mediation': {
            'texte': 'Couvre-feu pour les mineurs dans les zones de trafic intense. Création d\'un commissariat par arrondissement (contre trois actuellement)',
            'source': 'Programme Marseille en ordre 2026',
            'sourceUrl': 'https://www.lejdd.fr/politique/pass-anti-racaille-couvre-feu-pour-les-mineurs-les-mesures-de-franck-allisio-pour-restaurer-la-securite-a-marseille-166910'
        },
        # Transports
        'stationnement': {
            'texte': 'Arrêt de la suppression des places de stationnement (2 000 supprimées en 5 ans). Gratuité des 30 premières minutes dans les parkings payants pour aider les commerçants du centre-ville',
            'source': 'Programme Marseille en ordre 2026',
            'sourceUrl': 'https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-provence/radars-urbain-prix-des-parkings-le-candidat-rn-franck-allisio-veut-redonner-de-la-place-a-la-voiture-a-marseille-8148606'
        },
        'pietons-circulation': {
            'texte': 'Opposition aux radars urbains. Redonner de la place à la voiture à Marseille',
            'source': 'Programme Marseille en ordre 2026',
            'sourceUrl': 'https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-provence/radars-urbain-prix-des-parkings-le-candidat-rn-franck-allisio-veut-redonner-de-la-place-a-la-voiture-a-marseille-8148606'
        },
        # Logement
        'logement-social': {
            'texte': 'Programme de construction et de rénovation en hauteur tout en préservant les espaces verts. Simplification des permis de construire',
            'source': 'Programme Marseille en ordre 2026',
            'sourceUrl': 'https://madeinmarseille.net/politique/municipales-2026/196558-municipales-2026-la-grande-interview-de-franck-allisio-et-son-programme-pour-marseille/'
        },
        # Environnement
        'proprete-dechets': {
            'texte': 'Brigade anti-graffitis avec volet nettoyage et volet sanction. Amendes de 135 à 750 euros',
            'source': 'Programme Marseille en ordre 2026',
            'sourceUrl': 'https://franckallisio2026.fr/'
        },
        # Culture
        'evenements-creation': {
            'texte': 'Développement du tourisme sportif autour de Marcel Pagnol. Accueil de tournois internationaux de football et e-sports',
            'source': 'Programme Marseille en ordre 2026',
            'sourceUrl': 'https://lematindalgerie.com/marseille-franck-allisio-detaille-son-projet-economique-pour-les-municipales-2026/'
        },
        # Économie
        'emploi-insertion': {
            'texte': 'Développement de l\'emploi dans trois secteurs prioritaires : santé/biotechnologie, logistique/port, énergie/environnement',
            'source': 'Programme Marseille en ordre 2026',
            'sourceUrl': 'https://lematindalgerie.com/marseille-franck-allisio-detaille-son-projet-economique-pour-les-municipales-2026/'
        },
        'attractivite': {
            'texte': 'Faire de Marseille l\'autre capitale économique de France et du sud de l\'Europe. Clusters d\'entreprises et quartier start-up à la Joliette. Marina et port pour navettes maritimes. Tourisme d\'affaires',
            'source': 'Programme Marseille en ordre 2026',
            'sourceUrl': 'https://lematindalgerie.com/marseille-franck-allisio-detaille-son-projet-economique-pour-les-municipales-2026/'
        },
    }
}

def main():
    print("🔄 Intégration des programmes de Payan, Vassal et Allisio pour Marseille 2026")

    # Charger le JSON existant
    print(f"📖 Lecture de {JSON_FILE}")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Mettre à jour les URLs de programme
    print("🔗 Mise à jour des URLs de programme")
    for candidat in data['candidats']:
        if candidat['id'] == 'payan':
            candidat['programmeUrl'] = 'https://www.pourmarseille.fr/'
            candidat['programmeComplet'] = True  # ~40 projets détaillés
        elif candidat['id'] == 'vassal':
            candidat['programmeUrl'] = 'https://madeinmarseille.net/politique/196173-municipales-2026-martine-vassal-presente-les-13-axes-prioritaires-de-son-programme/'
            candidat['programmeComplet'] = False  # 13 axes mais pas encore le programme détaillé complet
        elif candidat['id'] == 'allisio':
            candidat['programmeUrl'] = 'https://franckallisio2026.fr/'
            candidat['programmeComplet'] = False  # Focus sécurité et économie principalement

    # Compteurs
    ajouts = 0
    mises_a_jour = 0

    # Intégrer les propositions
    print("✏️ Intégration des propositions")
    for categorie in data['categories']:
        for sous_theme in categorie['sousThemes']:
            sous_theme_id = sous_theme['id']

            # Pour chaque candidat
            for candidat_id in ['payan', 'vassal', 'allisio']:
                if candidat_id in PROPOSITIONS and sous_theme_id in PROPOSITIONS[candidat_id]:
                    proposition = PROPOSITIONS[candidat_id][sous_theme_id]

                    # Vérifier si c'est un ajout ou une mise à jour
                    if sous_theme['propositions'][candidat_id] is None:
                        ajouts += 1
                        action = "➕"
                    else:
                        mises_a_jour += 1
                        action = "🔄"

                    # Ajouter la proposition
                    sous_theme['propositions'][candidat_id] = proposition
                    print(f"  {action} {candidat_id.capitalize()} - {categorie['nom']} > {sous_theme['nom']}")

    # Sauvegarder
    print(f"\n💾 Sauvegarde dans {JSON_FILE}")
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Statistiques
    print("\n✅ TERMINÉ !")
    print(f"📊 Statistiques :")
    print(f"   - Nouvelles propositions : {ajouts}")
    print(f"   - Propositions mises à jour : {mises_a_jour}")
    print(f"   - Total modifications : {ajouts + mises_a_jour}")

    # Compter les propositions par candidat
    print(f"\n📈 Propositions par candidat :")
    for candidat_id in ['payan', 'vassal', 'allisio']:
        count = 0
        for categorie in data['categories']:
            for sous_theme in categorie['sousThemes']:
                if sous_theme['propositions'][candidat_id] is not None:
                    count += 1
        nom_candidat = next((c['nom'] for c in data['candidats'] if c['id'] == candidat_id), candidat_id)
        print(f"   - {nom_candidat} : {count} sous-thèmes couverts")

if __name__ == '__main__':
    main()
