#!/usr/bin/env python3
"""Intégration du programme de Corentin Jousserand (RN) - Saint-Étienne 2026"""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = r"C:\Users\KOPELMANRon\projets perso\FR comp mun\data\elections\saint-etienne-2026.json"

# Mapping: sous-thème -> liste de mesures (texte complet)
PROPOSITIONS = {
    "police-municipale": [
        "Tripler les effectifs de la police municipale, passant de 85 à 250 agents, en s'appuyant sur le recrutement et la mutualisation métropolitaine",
        "Créer une brigade canine municipale et une brigade équestre pour renforcer la présence dissuasive dans les quartiers sensibles et les espaces verts",
        "Mettre en place des patrouilles de nuit dans les quartiers les plus exposés, en lien avec la police nationale",
    ],
    "videoprotection": [
        "Déployer un réseau de 1500 caméras de vidéoprotection sur l'ensemble de la ville, contre 500 actuellement",
        "Installer un centre de supervision urbain (CSU) modernisé fonctionnant 24h/24",
    ],
    "prevention-mediation": [
        "Lancer une opération \"Quartiers propres\" visant à démanteler les points de deal en coordination avec les forces de l'État",
        "Mettre en place une politique de tolérance zéro contre les rodéos urbains, les dépôts sauvages et les occupations illicites de halls d'immeuble",
        "Instaurer un couvre-feu pour les mineurs non accompagnés de moins de 13 ans après 23h dans les zones les plus sensibles",
        "Renforcer l'éclairage public dans les zones identifiées comme à risque",
        "Créer un conseil local de sécurité et de prévention de la délinquance (CLSPD) renforcé, avec des réunions mensuelles ouvertes aux habitants",
    ],
    "transports-en-commun": [
        "Exiger des comptes de la Métropole sur le RER métropolitain et les 400 M€ promis après l'obtention du label RER",
        "Finaliser l'échangeur nº16 de l'A72 pour désengorger la Terrasse et améliorer l'accès au sud de la ville (434 M€ déjà mobilisés)",
        "Augmenter la fréquence des tramways sur les heures de pointe et en soirée",
    ],
    "velo-mobilites-douces": [
        "Construire un vrai réseau cyclable continu et sécurisé, sans coupures inutiles",
    ],
    "stationnement": [
        "Créer de nouveaux parkings relais en entrées de ville et transformer le parking des Ursules en grand parc-auto gratuit et sécurisé, ouvert à tous les Stéphanois",
        "Faciliter le stationnement pour les motos et scooters, amélioration des aires de circulation dans l'hyper-centre",
        "Garantir deux heures de stationnement gratuit dans les principaux axes commerciaux de la ville",
    ],
    "logements-vacants": [
        "Réorienter le PLU avec la Métropole pour faciliter la rénovation des immeubles existants et remises sur le marché des logements vacants",
        "Lancer un plan de reconquête du centre ancien : racheter stratégiquement les immeubles les plus dégradés, les rénover et élargir le système de l'habitat indigne",
        "Agir fermement contre les copropriétés défaillantes et l'habitat insalubre en utilisant pleinement les outils juridiques existants",
        "Reprendre 100 pieds d'immeubles en centre-ville sur le mandat pour réaffecter officiellement l'espace public à coût maîtrisé",
    ],
    "amenagement-urbain": [
        "Redonner vie à l'Hôpital de la Charité et la Bourse du travail en en faisant des lieux attractifs : maison de santé, espaces associatifs, co-working, culture et événements",
    ],
    "ecoles-renovation": [
        "Priorité à la qualité des écoles : rénovation des bâtiments, sécurisation des abords, végétalisation des cours et climatisation des établissements les plus exposés aux fortes chaleurs",
    ],
    "cantines-fournitures": [
        "Augmenter la part des produits issus de circuits courts dans les cantines scolaires",
    ],
    "periscolaire-loisirs": [
        "Développer l'offre de centres aérés pour mieux accompagner les familles",
        "Mettre en place des parcours éducatifs municipaux (sport, culture, citoyenneté) en partenariat avec les associations locales, évolutifs sur les niveaux éducatifs",
    ],
    "jeunesse": [
        "Renforcer la prévention de la violence et de l'alcoolémie scolaire en lien avec les établissements",
    ],
    "espaces-verts": [
        "Développer l'agriculture urbaine citoyenne dans les quartiers – réhabilitation de friches, création de jardins partagés, installation de fermes urbaines en lien avec les associations et les enfants dans la cour d'école",
        "Planter des arbres et ombrager les espaces publics de la ville en lien avec la Charte de l'environnement et l'aération de la ville",
    ],
    "climat-adaptation": [
        "Faciliter l'installation de fontaines et aires de rafraîchissement, installation de fontaines et d'aires de brumisation pour s'adapter au changement climatique",
    ],
    "centres-sante": [
        "Créer 2 ou 3 centres municipaux de santé pluriprofessionnels, accueillant 10 à 15 médecins généralistes, infirmières, kinés et sages-femmes",
        "Intégrer la santé mentale de proximité (psychologues, art-thérapie) pour désencombrer le CHU et répondre aux besoins urgents",
        "Renforcer le lien entre le CHU et la ville pour attirer durablement les jeunes médecins (exercice mixte, accompagnement à l'installation, logement)",
        "Mettre en place une mutuelle municipale",
    ],
    "prevention-sante": [
        "Déployer des centres de prévention ciblés (ex : addictions, santé mentale des jeunes et risques cardiovasculaires)",
    ],
    "budget-participatif": [
        "Créer un budget participatif de 2 millions d'euros par an, dédié à des projets concrets d'investissement proposés et choisis par les habitants",
        "Instaurer un droit d'interpellation : toute pétition dépassant 1600 signatures sera mise à l'ordre du jour du conseil municipal",
    ],
    "transparence": [
        "Consulter les Stéphanois avant tout grand projet de plus de 5 millions d'euros, avec une concertation organisée et une décision finale publique et motivée",
        "Garantir une transparence totale sur le financement des projets, les délais et l'utilisation des fonds publics",
    ],
    "commerce-local": [
        "Lancer un grand plan de retour et de développement du commerce en centre-ville de Saint-Étienne : réhabilitation de locaux vacants non adaptés, ouverture d'un commerce financé par la mairie qui commercialiserait les moyens dans l'hyper-centre",
        "Augmentation de la taxe sur les locaux vacants",
        "Utilisation du droit de préemption de la mairie pour le commerce en centre-ville",
        "Exemption totale de taxe foncière pendant trois ans après l'installation d'un commerce",
        "Reconcentrer le cœur d'activité de Steel sur l'accueil des très grandes enseignes, facilité industrielle/entrepôts/logistique et inclure les enseignes de taille intermédiaire à revenir en centre-ville",
    ],
    "emploi-insertion": [
        "Mise en place d'un guichet unique municipal pour les entrepreneurs, couplé à une coopérative de services mutualisés (comptabilité, communication, outils numériques, etc.)",
        "Aucune taxe foncière pendant 3 ans après l'installation d'une entreprise",
        "Gel de la taxe foncière sur tout le mandat",
    ],
    "equipements-culturels": [
        "Refondre la Cité du design en \"Cité du design industriel\" pour la reconnecter à l'histoire ouvrière et industrielle de Saint-Étienne et en faire un lieu ouvert, populaire et accessible",
    ],
    "equipements-sportifs": [
        "Mise en place d'un plan de rénovation ciblé des équipements sportifs existants, notamment les Champs-Beauly, le dojo de Molina, avec un soutien ciblé aux clubs féminins",
    ],
    "sport-pour-tous": [
        "Booster le développement du sport-santé en finançant des formations permettant d'encadrer l'activité physique sur prescription et pour les publics fragiles",
    ],
    "aide-sociale": [
        "Développer des équipements et services intergénérationnels associant petite enfance, seniors et personnes en situation de handicap, pour lutter contre l'isolement",
        "Créer un cimetière animalier municipal",
        "Soutenir financièrement les associations locales engagées pour la protection et le bien-être animal",
        "Aménager de nouveaux espaces canins adaptés et entretenus",
    ],
    "accessibilite": [
        "Mise en accessibilité progressive et prioritaire des équipements municipaux et sportifs, avec un accès facilité au sport pour les personnes handicapées, en lien avec les clubs",
    ],
}

SOURCE = "Programme officiel Corentin Jousserand"
SOURCE_URL = "#"

# Load
with open(FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Set programmeComplet to true
for candidat in data['candidats']:
    if candidat['id'] == 'jousserand':
        candidat['programmeComplet'] = True
        print(f"✓ programmeComplet = true pour {candidat['nom']}")
        break

# Insert propositions
count = 0
for cat in data['categories']:
    for st in cat['sousThemes']:
        if st['id'] in PROPOSITIONS:
            st['propositions']['jousserand'] = {
                'mesures': PROPOSITIONS[st['id']],
                'source': SOURCE,
                'sourceUrl': SOURCE_URL,
            }
            count += len(PROPOSITIONS[st['id']])
            print(f"  {cat['id']} > {st['id']} : {len(PROPOSITIONS[st['id']])} mesures")

print(f"\nTotal : {count} mesures intégrées dans {len(PROPOSITIONS)} sous-thèmes")

# Save
with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✓ Fichier sauvegardé : {FILE}")
