#!/usr/bin/env python3
"""
Mise à jour des propositions de Sophie Joissains (Aix-en-Provence)
Source : Programme de campagne 2026 (courrier PDF scanné, 16 pages OCR)
"""

import json
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
JSON_PATH = os.path.join(DATA_DIR, 'elections', 'aix-en-provence-2026.json')

SOURCE = "Programme de campagne 2026 (courrier)"
SOURCE_URL = "https://www.sophiejoissains2026.fr/programme"

# Mapping complet des mesures extraites du PDF OCR (16 pages)
PROPOSITIONS = {
    # === SÉCURITÉ ===
    "police-municipale": [
        "Recruter 10 agents de police municipale supplémentaires par an.",
        "Créer un nouveau commissariat de police municipale.",
        "Créer un nouveau centre de supervision urbain agrandi et modernisé.",
        "Créer 3 nouvelles bases territoriales de police municipale, avec la rénovation complète de celle du centre-ville.",
        "Intensifier la présence policière dans chaque quartier et village, avec une réorganisation des patrouilles de jour et de nuit et le déploiement de Postes Mobiles Opérationnels (PMO).",
        "Renforcer les formations des agents de police municipale.",
    ],
    "videoprotection": [
        "Déployer davantage de caméras de vidéoprotection sur le territoire.",
        "Sécuriser prioritairement les parvis des écoles avec la vidéoprotection et le déploiement du dispositif « rue scolaire ».",
    ],
    "prevention-mediation": [
        "Doubler les dispositifs « Participation Citoyenne » pour couvrir la totalité du territoire aixois et promouvoir la participation citoyenne dans la sécurisation des habitations.",
        "Renforcer les missions de la Maison de la Justice et du Droit (soutien aux victimes).",
        "Projet LIMITS : détecter et limiter l'implication des mineurs dans le trafic de stupéfiants, avec la signature d'une convention étatique.",
    ],
    "violences-femmes": [
        "Créer un 2e centre d'accueil d'urgence pour les femmes victimes de violences.",
    ],

    # === TRANSPORTS ===
    "transports-en-commun": [
        "Extension de la ligne Aixpress jusqu'à Malacrida, vers les quartiers nord.",
        "Création d'une voie de Bus à Haut Niveau de Service (BHNS) entre la Constance, le Pôle d'Activité d'Aix et la Duranne, avec des bus de 18 mètres.",
        "Créer deux nouvelles lignes de Bus à Haut Niveau de Service, au nord et au sud de la Ville.",
        "Obtenir 3 haltes ferrées dans le prochain Schéma d'Armature Ferroviaire métropolitain : La Calade, Les Milles et Plan d'Aillane.",
    ],
    "velo-mobilites-douces": [
        "Apaiser l'espace public grâce à une extension des zones piétonnes et à la requalification des espaces publics en mode doux.",
    ],
    "pietons-circulation": [
        "Réaménager l'échangeur du Pont de l'Arc et accompagner la nouvelle bretelle A8/A51.",
    ],
    "stationnement": [
        "Proposer aux Aixois 2 nouveaux parkings sur le pourtour du centre-ville.",
        "Renforcer l'offre de parcs-relais au sud de la Ville et construire un nouveau parking-relais en lien avec le BHNS à venir.",
    ],

    # === LOGEMENT ===
    "logement-social": [
        "Construction de logements dans le cadre de la rénovation urbaine d'Encagnane (424 logements prévus) et du quartier du Faubourg.",
    ],
    "acces-logement": [
        "Mettre en place un partenariat structuré entre la Ville, Aix-Marseille Université, le CROUS et les acteurs associatifs pour développer des solutions de logement étudiant et intergénérationnel.",
    ],

    # === ÉDUCATION ===
    "ecoles-renovation": [
        "Accélérer le plan de rénovation thermique des écoles, optimiser l'entretien des cours d'école végétalisées et créer des salles refuges climatisées dans chaque école.",
        "Renforcer le parcours de réussite de l'enfant grâce aux dispositifs « Coup de pouce », d'Enseignement Artistique et Culturel (Label 100% EAC) et le « Savoir Rouler à Vélo ».",
    ],
    "cantines-fournitures": [
        "Maintenir et augmenter la qualité de la restauration scolaire : 57% de produits durables et de qualité, 36% de produits bio. Refus des produits issus d'accords internationaux mettant en difficulté nos agriculteurs.",
    ],
    "periscolaire-loisirs": [
        "Renforcer les activités périscolaires, culturelles, sportives et l'aide aux devoirs sur des horaires élargis.",
    ],
    "jeunesse": [
        "Faire évoluer les missions du Repère (lieu d'information et d'accueil des étudiants) comme un lieu d'écoute, d'accompagnement et de prévention pour les étudiants.",
    ],

    # === ENVIRONNEMENT ===
    "espaces-verts": [
        "Planter 400 arbres par an, d'essences adaptées au climat, pendant toute la durée du mandat.",
        "Poursuivre la réhabilitation et la modernisation des parcs et jardins (Parc Jourdan, Parc de la Torse, Parc Villers).",
        "Créer un Plan « Ombrage et fontaines » pour un rafraîchissement urbain et le confort des habitants.",
        "Poursuivre la mise en circuit fermé des fontaines et cartographier les fontaines potables en centre-ville et dans les quartiers et villages.",
    ],
    "proprete-dechets": [
        "Multiplier les campagnes de communication pour lutter contre les incivilités et les bonnes conduites en matière de dépôts d'ordures ménagères.",
        "Maximiser l'utilisation de la plateforme « Je signale » pour optimiser la carte interactive de signalement et de suivi des dépôts sauvages.",
        "Moderniser les moyens de la propreté urbaine avec une transition progressive vers des véhicules propres.",
        "Renforcer les prérogatives d'investigation, de verbalisation et les moyens de la Brigade de l'environnement, avec le déploiement de caméras sur les secteurs de dépôts sauvages.",
    ],
    "climat-adaptation": [
        "Créer des îlots de fraîcheur hors-sol, notamment sur les Places Comtales et la Place Romée-de-Villeneuve.",
        "Mettre en place un comité scientifique et écologique pour apprécier l'impact des politiques publiques.",
        "Mettre en place des salles climatisées sur l'ensemble de la Ville pour les périodes de canicule.",
    ],
    "renovation-energetique": [
        "Déployer de nouvelles solutions énergétiques renouvelables (géothermie, photovoltaïque, biogaz, bois) et refaire d'Aix-en-Provence une cité thermale.",
        "Moderniser l'éclairage public pour atteindre 100% d'éclairage LED.",
        "Développer la géothermie pour que le réseau de chaleur urbain atteigne 80% d'énergie verte.",
        "Mise en place d'une ferme photovoltaïque sur le secteur de l'Arbois, produisant 30 MW d'électricité verte (équivalent des besoins de 30 000 habitants).",
    ],

    # === SANTÉ ===
    "centres-sante": [
        "Renforcer l'offre de soins avec le développement des maisons de santé dans les quartiers et villages (6 déjà installées, dont 2 labellisées France Santé).",
        "Poursuivre l'accompagnement des établissements de santé publics et privés.",
        "Retrouver le label thermal de la Ville d'Aix-en-Provence.",
    ],
    "seniors": [
        "Renforcer une politique globale à destination des aînés : animations et billetterie à tarifs préférentiels ou gratuits, lutte contre l'isolement, aide à domicile, soins.",
    ],

    # === DÉMOCRATIE ===
    "budget-participatif": [
        "Poursuivre les concertations citoyennes sur les projets d'urbanisme majeurs afin d'intégrer chaque Aixois aux idées de renouveau urbain.",
    ],
    "transparence": [
        "Pas d'augmentation des impôts communaux pendant toute la durée du mandat (engagement maintenu depuis près de 30 ans).",
    ],
    "vie-associative": [
        "Développer un réseau de bénévoles et d'accompagnement citoyen pour soutenir les personnes les plus isolées.",
    ],

    # === ÉCONOMIE ===
    "emploi-insertion": [
        "Projet de Tech Valley (terrain de l'ENSOSP, labellisé France 2030) : pôle d'excellence dédié à l'aéronautique, la cybersécurité, l'intelligence artificielle et la défense spatiale.",
        "Projet d'Energy Valley au sein du Pôle d'Activités d'Aix-en-Provence : hub d'innovation consacré aux énergies renouvelables et à la transition énergétique.",
    ],
    "attractivite": [
        "Valoriser une offre touristique culturelle et patrimoniale d'excellence en cohérence avec l'identité aixoise et les grands équipements.",
    ],

    # === CULTURE ===
    "equipements-culturels": [
        "Ouverture de la Bibliothèque Méjanes rénovée : lieu de lecture publique gratuite, de découverte et de vie.",
        "Ouvrir un Muséum d'histoire naturelle à Aix-en-Provence (3 sites à l'étude, notamment à La Constance).",
        "Ouverture d'un parcours cézannien unique au monde pour visiter l'ensemble des lieux de vie et de travail de Paul Cézanne.",
        "Dégagement et dévoilement du théâtre antique de la SEDS (diamètre de 100 mètres, Ier siècle av. J.-C.).",
    ],
    "evenements-creation": [
        "Affirmer la culture comme une politique centrale du projet municipal au service de l'émancipation, de l'éducation et du vivre ensemble.",
        "Ancrer la Biennale d'Aix comme un rendez-vous majeur de création dans l'espace public, faisant dialoguer patrimoine et création.",
        "Structurer l'accompagnement des compagnies en complément de la programmation du Théâtre du Bois de l'Aune.",
    ],

    # === SPORT ===
    "equipements-sportifs": [
        "Rénover et moderniser l'intégralité des stades et gymnases communaux, avec une exigence pour l'accessibilité et la rénovation énergétique.",
        "Passer la capacité du Stade Maurice David à plus de 10 000 places pour répondre aux critères du TOP 14.",
    ],
    "sport-pour-tous": [
        "Rendre l'information sportive plus accessible avec la création d'un agenda sportif en ligne et une carte des équipements sportifs.",
        "Poursuivre la création et l'animation d'équipements sportifs de proximité dans les quartiers et villages.",
    ],

    # === URBANISME ===
    "amenagement-urbain": [
        "Requalification bioclimatique du Cours Sextius : couture urbaine entre les Thermes, le Cours Sextius et le Boulevard de la République, avec cours d'eau urbain et renforcement des continuités vertes.",
        "Faire du quartier de La Constance un modèle de développement concerté, équilibré, accessible et intégré (écoquartier bioclimatique et culturel unique en France, urbanisme inspiré du quartier Mazarin).",
        "Achever la rénovation urbaine d'Encagnane (programme chiffré à plus de 158 millions d'euros) et du quartier du Faubourg.",
        "Transformer la charte du « Bien construire » en charte du « Bien et Beau construire » avec l'intégration de normes écologiques, thermiques et énergétiques.",
    ],
    "accessibilite": [
        "Optimiser l'accès aux bâtiments publics aux personnes en situation de handicap.",
        "Autoriser les transports spécialisés pour les personnes en situation de handicap à emprunter les couloirs de bus.",
    ],

    # === SOLIDARITÉ ===
    "aide-sociale": [
        "Poursuivre une politique de protection animale avec un cimetière animalier, un sanctuaire, l'ouverture de 2 parcs canins et un renouvellement des labels « Bien-être animal ».",
    ],
    "pouvoir-achat": [
        "Continuer de valoriser le patrimoine auprès des Aixois via des tarifs préférentiels et des gratuités.",
    ],
}


def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Mettre à jour le candidat
    for candidat in data['candidats']:
        if candidat['id'] == 'joissains':
            candidat['programmeComplet'] = True
            candidat['programmePdfPath'] = "data/programmes/Programme Joissains_compressed.pdf"
            break

    # Compter les mesures
    total_mesures = sum(len(m) for m in PROPOSITIONS.values())
    print(f"Total mesures dans le mapping : {total_mesures}")

    # Mettre à jour les propositions
    updated = 0
    for cat in data['categories']:
        for st in cat['sousThemes']:
            st_id = st['id']
            if st_id in PROPOSITIONS:
                st['propositions']['joissains'] = {
                    "source": SOURCE,
                    "sourceUrl": SOURCE_URL,
                    "mesures": PROPOSITIONS[st_id]
                }
                updated += 1
                print(f"  {cat['id']}/{st_id}: {len(PROPOSITIONS[st_id])} mesures")

    # Nettoyer les anciens sous-thèmes qui ne sont plus dans le mapping
    for cat in data['categories']:
        for st in cat['sousThemes']:
            if st['id'] not in PROPOSITIONS and 'joissains' in st['propositions']:
                old = st['propositions']['joissains']
                if old is not None:
                    print(f"  CONSERVÉ (ancien) {cat['id']}/{st['id']}")

    print(f"\nSous-thèmes mis à jour : {updated}")
    print(f"Total mesures : {total_mesures}")

    # Écrire le fichier
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nFichier sauvegardé : {JSON_PATH}")


if __name__ == '__main__':
    main()
