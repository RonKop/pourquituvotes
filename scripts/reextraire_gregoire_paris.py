#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction complète d'Emmanuel Grégoire (Paris) depuis emmanuel-gregoire-2026.fr/programme.
165 mesures extraites vs 90 actuellement.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "paris-2026.json")

SOURCE = "Programme officiel 2026 — Emmanuel Grégoire"
SOURCE_URL = "https://emmanuel-gregoire-2026.fr/programme"

MESURES = {
    # === PARIS POPULAIRE : LOGEMENT ===
    "logement-social": [
        "Création de 60 000 nouveaux logements sociaux et abordables (30 000 chaque catégorie).",
        "Taxation des logements vacants depuis plus de 5 ans.",
        "Réquisition des propriétés longuement vacantes.",
        "Interdiction des nouvelles résidences secondaires.",
        "Logements adaptés aux différentes étapes de la vie.",
        "Équipes rapides de réparations inter-bailleurs pour le logement social.",
        "Charte de qualité de service entre bailleurs et associations de locataires.",
    ],
    "logements-vacants": [
        "Taxation des logements vacants depuis plus de 5 ans.",
        "Réquisition des propriétés longuement vacantes.",
    ],
    "encadrement-loyers": [
        "Restriction des locations Airbnb aux résidences principales, maximum 90 jours par an.",
        "Création d'une Brigade de protection du logement pour l'application des règles et le soutien aux locataires.",
    ],
    "acces-logement": [
        "Assurance habitation municipale accessible à tous les résidents.",
        "Couverture punaises de lit incluse dans l'assurance municipale.",
        "Garantie municipale de loyers étendant le programme Visale.",
        "4 000 lits d'hébergement d'urgence répartis dans tous les arrondissements.",
        "Initiative « Zéro enfant à la rue » avec 1 000 lits dédiés.",
    ],

    # === PARIS POPULAIRE : ÉNERGIE & ENVIRONNEMENT ===
    "renovation-energetique": [
        "Rénovation complète et isolation de 35 000 logements sociaux.",
        "Aide à 200 000 rénovations de logements privés avec avances climatiques à taux zéro.",
        "Améliorations d'accessibilité pour les résidents seniors et handicapés dans les immeubles.",
        "Coopératives d'achat d'énergie renouvelable négociées par la ville.",
        "Extension des réseaux publics de chaleur et de fraîcheur.",
    ],
    "alimentation-durable": [
        "100% d'alimentation bio, locale et durable dans les écoles et crèches.",
        "Programmes municipaux de sécurité alimentaire et de nutrition.",
        "Réseau municipal d'épiceries coopératives et restaurants solidaires.",
        "Centres de ressources et ateliers de réparation dans chaque quartier.",
    ],
    "proprete-dechets": [
        "Brigades anti-incivilités au sein de la police municipale.",
        "Service de collecte à domicile des encombrants avec réemploi prioritaire.",
        "Amendes renforcées pour dépôts sauvages (500 € minimum particuliers, 1 000 € professionnels).",
        "Modernisation de l'application « Dans Ma Rue » avec fonctions participatives.",
        "Responsabilisation des propriétaires pour les tags sur les bâtiments vacants.",
        "Flotte 100% électrique pour les services de propreté.",
        "Réduction de 100 000 tonnes de déchets d'ici 2030.",
        "Compostage généralisé dans tous les quartiers.",
        "Tri à la source généralisé dans les logements et espaces publics.",
        "Campagnes zéro déchet dans les écoles et immeubles.",
        "Développement de l'emballage réutilisable et consigné, en commençant par la restauration rapide.",
    ],
    "climat-adaptation": [
        "Gagner 3°C dans les rues l'été grâce à la végétalisation grimpante, la désartificialisation des cours d'école et des solutions perméables.",
        "Sécurité climatique pour les bâtiments municipaux et logements (volets, toits frais).",
        "Priorité à la résilience climatique pour les écoles, crèches et structures pour personnes âgées.",
    ],

    # === PARIS POPULAIRE : PROTECTION SOCIALE ===
    "aide-sociale": [
        "Revenu Solidarité Jeunesse pour les jeunes sortant de la protection de l'enfance.",
        "100% d'accès aux aides municipales via procédures simplifiées et bureaux mobiles.",
        "Accompagnement personnalisé RSA avec parcours vers l'emploi.",
        "Équipes pluridisciplinaires de réduction des risques et sites dédiés.",
    ],
    "centres-sante": [
        "Mutuelle santé municipale abordable accessible à tous.",
        "100 nouveaux sites de soins en secteur 1 (sans dépassement), dont 7 centres de santé municipaux.",
    ],
    "prevention-sante": [
        "Plan ambitieux de santé sexuelle visant zéro nouvelle infection VIH d'ici 2030.",
        "Plan complet de santé mentale des jeunes.",
        "Services de santé scolaire renforcés avec bilans complets en maternelle et élémentaire.",
        "Parcours des 1 000 premiers jours de l'enfant via les centres PMI et maisons spécialisées.",
        "Accompagnement spécialisé pour les patientes atteintes d'endométriose.",
    ],
    "accessibilite": [
        "Bureaux MDPH (services handicap) étendus dans tous les arrondissements.",
        "Nouveaux quartiers d'accessibilité renforcée.",
        "Application collaborative informant en temps réel des conditions d'accessibilité PMR.",
    ],

    # === PARIS POPULAIRE : ÉDUCATION & JEUNESSE ===
    "ecoles-renovation": [
        "Défense des écoles publiques contre les fermetures de classes imposées par l'État.",
        "Modulation des subventions aux écoles privées selon les critères de mixité sociale.",
        "Rénovation majeure et verdissement des écoles et collèges.",
        "Cours « Oasis » dans les écoles pour la résilience climatique.",
        "50 nouvelles unités d'enseignement adaptées pour les élèves handicapés.",
        "Structures mixtes combinant écoles spécialisées et enseignement ordinaire.",
        "Protocoles de protection de l'enfance (jamais un adulte seul avec un enfant).",
        "Mécanismes de recueil de la parole de l'enfant dans chaque école.",
        "Formation à la protection de l'enfance pour tout le personnel.",
        "Inspections indépendantes régulières et rapports transparents.",
    ],
    "cantines-fournitures": [
        "Gel des tarifs de cantine scolaire.",
        "Extension de la gratuité des fournitures scolaires.",
    ],
    "periscolaire-loisirs": [
        "Convention citoyenne sur les rythmes scolaires (avril 2026).",
        "Programme « Un mois, une découverte » culturel et sportif pour les enfants.",
        "Sortie de terrain pour chaque élève de primaire au moins une fois.",
        "100% de contrats d'animation continus (pas à l'heure).",
        "Programmes « Péricollège » extrascolaires et vacances.",
    ],
    "petite-enfance": [
        "1 000 agents de petite enfance supplémentaires avec carrières améliorées.",
        "Multiplication des crèches « Oasis » adaptées au climat.",
        "Extension des maisons d'assistantes maternelles (MAM).",
        "Priorité d'accès en crèche pour les familles monoparentales.",
        "Tarifs adaptés pour les familles monoparentales dans les services municipaux.",
        "2 heures par semaine de garde d'enfant hors horaires scolaires traditionnels.",
    ],
    "jeunesse": [
        "Un « Quartier Jeunesse » par arrondissement offrant un accompagnement personnalisé.",
        "Tutorat élargi et formations courtes pour les jeunes.",
        "Augmentation des résidences étudiantes et jeunes travailleurs.",
        "Accès aux vacances abordable chaque année pour les jeunes.",
        "Statut formel et conditions améliorées pour les AESH (accompagnants handicap).",
    ],
    "seniors": [
        "Comités d'usagers seniors co-concevant les programmes.",
        "Engagement bénévole et civique facilité pour les seniors.",
        "Espaces résidence-autonomie transformés avec hébergement familial.",
        "Activités intergénérationnelles dans les résidences seniors.",
        "Espaces publics adaptés avec bancs réguliers pour les seniors.",
        "Journée annuelle de la « Connexion » pour identifier et soutenir les personnes isolées.",
        "Statut d'aidant et droits au répit.",
    ],

    # === PARIS POPULAIRE : SERVICES PUBLICS ===
    "services-publics": [
        "Guichet administratif unifié par arrondissement avec horaires étendus.",
        "Agents polyvalents gérant plusieurs services municipaux et étatiques.",
        "Accompagnement municipal par étape de vie (naissance, adolescence, séparation, décès).",
        "Application numérique municipale 100% accessible.",
        "Dossier scolaire numérique simplifié.",
        "Horaires étendus pour parcs, piscines, gymnases, bibliothèques et musées.",
        "Services funéraires solidaires pour les résidents précaires.",
        "Nouveaux espaces de cérémonie funéraire laïque.",
    ],

    # === PARIS VIVANTE : ESPACES VERTS ===
    "espaces-verts": [
        "1 000 rues piétonnes avec nouveaux centres de quartier verts.",
        "Principe de préservation des 200 000 arbres de Paris et 300 000 arbres des Bois.",
        "Création de 500 nouvelles bandes végétalisées à Paris.",
        "300 nouveaux hectares de jardins ouverts au public avec horaires étendus.",
        "10 nouveaux parcs remplaçant des voies automobiles sur certains boulevards.",
        "Objectif d'un trottoir ombragé par rue dans chaque quartier.",
        "Toitures partagées, accessibles et végétalisées en réseau.",
        "25 km de promenade végétalisée et accessible le long de la Seine.",
        "Site de baignade et loisirs « Plage Bastille » au Port de l'Arsenal.",
        "10 km supplémentaires de Petite Ceinture ouverts.",
        "Restauration de la rivière Bièvre et voie verte le long de son tracé historique.",
        "Plan de protection des oiseaux avec préservation des habitats.",
    ],
    "amenagement-urbain": [
        "Transformation des places République, Trocadéro, Concorde, Italie, Stalingrad et Gambetta.",
        "« Manifeste pour la Nouvelle Esthétique Parisienne » avec directeur artistique nommé.",
        "Refonte de la signalétique (suppression panneaux obsolètes, standards accessibles).",
        "10 nouvelles aires de jeux XXL co-conçues avec les enfants.",
        "Mini mobilier urbain à hauteur d'enfant dans les rues scolaires.",
        "Transformation du périphérique en boulevard urbain.",
        "Transformation des Portes de Paris en places du Grand Paris.",
        "Ceinture verte, culturelle et sportive reliant les portes.",
    ],

    # === PARIS VIVANTE : SÉCURITÉ ===
    "police-municipale": [
        "Recrutement de 1 000 policiers municipaux supplémentaires.",
        "Présence 24h/24 et 7j/7 dans tous les arrondissements.",
        "Kiosque de police dans chaque arrondissement et points sensibles.",
        "Brigades de nuit spécialisées pour réduire les nuisances.",
        "Patrouilles montées dans les Bois.",
        "Brigades de lutte contre les rodéos et violences motorisées.",
        "Formation de la police municipale aux discriminations et au sexisme.",
        "Plan de prévention du harcèlement de rue et pouvoir de verbalisation.",
        "Présence policière renforcée lors des événements culturels et fermetures nocturnes.",
    ],
    "videoprotection": [
        "500 nouvelles caméras mobiles tactiques dans les zones ciblées.",
        "Vidéo-verbalisation des infractions routières.",
    ],
    "prevention-mediation": [
        "Éclairage nocturne renforcé conçu avec les usagers.",
        "Dispositifs d'alerte dans les abribus reliés au centre de commandement.",
        "Référent médiation dans chaque école et équipement sportif.",
        "Coordination prévention en milieu scolaire.",
        "Plan « Zéro mort, zéro blessé grave » pour la sécurité routière.",
        "Nouveaux radars sur les grands axes accidentogènes.",
    ],
    "violences-femmes": [
        "Autorité de verbalisation pour le harcèlement de rue.",
        "Arrêts de bus à la demande la nuit.",
    ],

    # === PARIS VIVANTE : TRANSPORTS ===
    "transports-en-commun": [
        "15 lignes de bus express avec itinéraires sécurisés dédiés.",
        "Super-priorité bus aux carrefours avec vidéo-verbalisation.",
        "100% des arrêts de bus accessibles.",
        "Un bus toutes les 5 minutes sur les 15 lignes les plus fréquentées aux heures de pointe.",
        "Métro 24h/24 sur les lignes automatisées (1, 4, 14).",
        "Maintien de la gratuité Navigo pour les enfants, jeunes, seniors et personnes handicapées.",
        "Coordination renforcée de l'accessibilité des transports avec l'État et la Région.",
    ],
    "velo-mobilites-douces": [
        "Achèvement du réseau cyclable parisien sur les grandes avenues.",
        "Suppression des pistes cyclables sur trottoir (déplacement au niveau de la rue en voies protégées).",
        "Améliorations de sécurité aux carrefours et lieux accidentogènes.",
        "Vélo-école dans chaque arrondissement.",
        "Service Vélib performant avec responsabilisation de l'opérateur et pénalités.",
        "Tarifs Vélib abordables pour tous.",
        "Coopérative municipale du vélo avec location longue durée abordable et assurance.",
    ],
    "stationnement": [
        "Stationnement réservé aux artisans et professionnels de service.",
        "Au moins 25% du stationnement public réservé aux PMR, livraisons et usage professionnel.",
        "Tarifs de stationnement résidentiel abordables dans les parkings souterrains.",
        "Hubs de micro-logistique pour des livraisons groupées réduisant les nuisances.",
        "Développement du fret fluvial.",
    ],

    # === PARIS FIÈRE ===
    "egalite-discriminations": [
        "Égalité entre les femmes et les hommes intégrée à toutes les politiques.",
        "Standards d'accessibilité universelle maintenus.",
    ],
    "budget-participatif": [
        "Permis de piétonisation temporaire pour les événements communautaires.",
    ],
    "transparence": [
        "Réduction de la pollution de l'eau et de l'air (PFAS, pesticides, perturbateurs endocriniens).",
        "Contrôle de la pollution sonore via réseaux de capteurs et plans de réduction par quartier.",
    ],
    "vie-associative": [
        "Parcs ouverts aux chiens tenus en laisse avec espaces dédiés.",
        "Services de consultation vétérinaire dans la Maison de la Ville Animale.",
    ],
    "commerce-local": [
        "Bouclier de Sécurité pour l'économie locale : aide au financement de la sécurité des commerces.",
    ],
    "pouvoir-achat": [
        "Arrêts de bus à la demande la nuit pour la sécurité.",
    ],
}


def main():
    print("=" * 60)
    print("  RÉ-EXTRACTION GRÉGOIRE (Paris)")
    print("=" * 60)

    total = sum(len(v) for v in MESURES.values())
    print(f"\n  {total} mesures dans {len(MESURES)} sous-thèmes")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in MESURES and len(MESURES[st_id]) > 0:
                prop = st["propositions"].get("gregoire")
                if prop is None:
                    prop = {}
                    st["propositions"]["gregoire"] = prop

                old_count = len(prop.get("mesures", []))
                new_mesures = MESURES[st_id]

                if len(new_mesures) >= old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = SOURCE
                    prop["sourceUrl"] = SOURCE_URL
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} → {len(new_mesures)}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n    {updated} sous-thèmes mis à jour")
    print("=" * 60)


if __name__ == "__main__":
    main()
