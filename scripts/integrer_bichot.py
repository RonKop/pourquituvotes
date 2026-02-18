#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du programme complet d'Emmanuel Bichot (Dijon 2026)
122 propositions - Programme "Agir pour Dijon"
Source principale : https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/
Site officiel : https://www.bichot2026.fr/
"""

import sys
import io
import json
import os

# Configuration UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Chemin du fichier JSON
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(SCRIPT_DIR, "..", "data", "elections", "dijon-2026.json")

# Sources
SOURCE_PRINCIPALE = "Dijon Actualités, 3 février 2026"
SOURCE_URL_PRINCIPALE = "https://dijon-actualites.fr/2026/02/03/municipales-2026-a-dijon-emmanuel-bichot-devoile-un-programme-axe-sur-lordre-la-securite-et-le-pouvoir-dachat/"
SOURCE_SITE = "Site officiel Bichot 2026"
SOURCE_URL_SITE = "https://www.bichot2026.fr/"

CANDIDAT_ID = "bichot"


def charger_json():
    """Charge le fichier JSON existant"""
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def sauvegarder_json(data):
    """Sauvegarde le fichier JSON avec UTF-8"""
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Fichier sauvegardé : {JSON_PATH}")


def mettre_a_jour_candidat(data):
    """Met à jour les informations du candidat Bichot"""
    for candidat in data['candidats']:
        if candidat['id'] == CANDIDAT_ID:
            candidat['programmeUrl'] = SOURCE_URL_SITE
            candidat['programmeComplet'] = True  # 122 propositions = programme complet
            print(f"  Candidat mis à jour : programmeComplet=True")
            break


def set_proposition(categories_dict, cat_id, st_id, texte, source=None, source_url=None):
    """
    Ajoute ou met à jour une proposition pour Bichot.
    Retourne True si ajout (n'existait pas), False si mise à jour.
    """
    if source is None:
        source = SOURCE_PRINCIPALE
    if source_url is None:
        source_url = SOURCE_URL_PRINCIPALE

    cat = categories_dict.get(cat_id)
    if not cat:
        print(f"  ERREUR : catégorie '{cat_id}' introuvable")
        return None

    for st in cat['sousThemes']:
        if st['id'] == st_id:
            was_new = (st['propositions'].get(CANDIDAT_ID) is None)
            st['propositions'][CANDIDAT_ID] = {
                'texte': texte,
                'source': source,
                'sourceUrl': source_url
            }
            status = "AJOUTÉ" if was_new else "MIS À JOUR"
            print(f"  {status} : {cat_id} > {st_id}")
            return was_new

    print(f"  ERREUR : sous-thème '{st_id}' introuvable dans '{cat_id}'")
    return None


def integrer_propositions(data):
    """Intègre toutes les propositions de Bichot dans le JSON"""

    count_new = 0
    count_updated = 0
    categories = {cat['id']: cat for cat in data['categories']}

    # =====================================================================
    # SÉCURITÉ & PRÉVENTION
    # =====================================================================

    # police-municipale : ENRICHIR (propositions 1, 8, 10-13)
    # Existant : "Doubler les effectifs de la police municipale à 200 agents avec brigade canine et anti-stupéfiants"
    # Enrichir avec plus de détail
    r = set_proposition(categories, 'securite', 'police-municipale',
        "Doubler les effectifs de la police municipale à 200 agents, créer une brigade canine (5 chiens), "
        "une brigade anti-stupéfiants, un officier de liaison scolaire et une police métropolitaine des transports Divia")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # videoprotection : ENRICHIR (proposition 5)
    # Existant : "Renforcer la vidéoprotection avec intelligence artificielle"
    # Pas de changement majeur, garder tel quel — OK

    # prevention-mediation : ENRICHIR (propositions 2-4, 14-20)
    # Existant : "Mener des opérations régulières contre le narcotrafic et les rodéos urbains"
    # Enrichir avec la prévention + lutte contre trafics
    r = set_proposition(categories, 'securite', 'prevention-mediation',
        "Prévention familiale inspirée du modèle orléanais (Conseil des droits et devoirs des familles), "
        "opérations régulières contre le narcotrafic et les rodéos urbains, "
        "campagnes de dissuasion de la consommation de drogue et partage d'informations avec l'État contre le blanchiment")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # violences-femmes : NOUVEAU (proposition 21)
    r = set_proposition(categories, 'securite', 'violences-femmes',
        "Renforcer l'accompagnement des victimes, en particulier les femmes et les jeunes, "
        "avec un dispositif dédié au sein de la police municipale")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # =====================================================================
    # TRANSPORTS & MOBILITÉ
    # =====================================================================

    # transports-en-commun : ENRICHIR (propositions 43-44, 47-48)
    r = set_proposition(categories, 'transports', 'transports-en-commun',
        "Suspendre la 3e ligne de tramway et élaborer un nouveau plan de mobilité fondé sur les besoins des citoyens, "
        "avec arrêts de bus à la demande après 22h et extension des navettes électriques vers le centre-ville et les Halles")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # velo-mobilites-douces : ENRICHIR (proposition 49)
    r = set_proposition(categories, 'transports', 'velo-mobilites-douces',
        "Développer des itinéraires cyclables continus et sécurisés sur l'ensemble de la métropole")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # pietons-circulation : ENRICHIR (propositions 31, 45-46, 50, 54-55)
    r = set_proposition(categories, 'transports', 'pietons-circulation',
        "Programme \"Ma rue, ma ville\" de rénovation pluriannuelle des voiries et trottoirs, "
        "création de cheminements piétons antidérapants (axe Darcy-Liberté), "
        "résolution des points de congestion (gare, place du 30-Octobre), "
        "élargissement de la LiNO à 2x2 voies et équipement des feux tricolores en signaux sonores pour malvoyants")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # stationnement : ENRICHIR (propositions 51-52, 73)
    r = set_proposition(categories, 'transports', 'stationnement',
        "Gratuité de la première demi-heure de stationnement en surface, "
        "réduction du forfait post-stationnement à 15 euros, "
        "création de 4 nouveaux parkings dans les zones en tension "
        "et amélioration du stationnement pour les professionnels de santé et artisans")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # tarifs-gratuite : conserver (proposition intégrée déjà)
    # Existant : "Gratuité des transports en commun pour les personnes handicapées"
    # Pas de changement majeur

    # =====================================================================
    # LOGEMENT
    # =====================================================================

    # logement-social : NOUVEAU (propositions 29, 80-81)
    r = set_proposition(categories, 'logement', 'logement-social',
        "Augmenter l'offre de maisons individuelles et grands logements familiaux, "
        "rétablir la jouissance paisible des logements sociaux "
        "et sécuriser les interventions professionnelles et délais d'ascenseurs dans le parc HLM")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # logements-vacants : NOUVEAU (propositions 26-27)
    r = set_proposition(categories, 'logement', 'logements-vacants',
        "Renforcer les normes d'habitabilité des logements locatifs "
        "et prioriser la rénovation du bâti existant avec accompagnement des propriétaires")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # acces-logement : NOUVEAU (proposition 28)
    r = set_proposition(categories, 'logement', 'acces-logement',
        "Adopter des règles architecturales harmonieuses respectant l'identité des quartiers "
        "et adapter les constructions neuves aux besoins réels des Dijonnais")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # =====================================================================
    # ÉDUCATION & JEUNESSE
    # =====================================================================

    # petite-enfance : ENRICHIR (propositions 91-93)
    r = set_proposition(categories, 'education', 'petite-enfance',
        "Faciliter l'accès aux crèches municipales pour les parents actifs, "
        "améliorer les conditions de travail des professionnels de la petite enfance "
        "et renforcer le contrôle des établissements d'accueil")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # ecoles-renovation : ENRICHIR (proposition 89)
    r = set_proposition(categories, 'education', 'ecoles-renovation',
        "Accélérer la rénovation des écoles et éliminer les préfabriqués, "
        "maintenir un personnel formé suffisant pour la lutte contre le harcèlement scolaire")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # periscolaire-loisirs : conserver (proposition 88)
    # Existant : "Consulter les parents sur le retour à la semaine de 4 jours"

    # jeunesse : NOUVEAU (proposition 79)
    r = set_proposition(categories, 'education', 'jeunesse',
        "Faciliter l'insertion professionnelle des étudiants et apprentis dijonnais")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # =====================================================================
    # ENVIRONNEMENT & TRANSITION ÉCOLOGIQUE
    # =====================================================================

    # espaces-verts : ENRICHIR (propositions 23, 34-40)
    r = set_proposition(categories, 'environnement', 'espaces-verts',
        "Sauver le lac Kir de l'envasement, protéger les espaces verts existants et en créer de nouveaux, "
        "mieux entretenir les parcs et vallées municipaux, "
        "rendre inconstructible la zone naturelle des Lentillères pour le maraîchage, "
        "créer 10 grands parcs canins et installer des distributeurs de sacs dans tous les quartiers")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # proprete-dechets : NOUVEAU (propositions 30, 33, 41)
    r = set_proposition(categories, 'environnement', 'proprete-dechets',
        "Renforcer les équipes de nettoyage quotidien des rues, "
        "améliorer l'éclairage des rues et espaces publics "
        "et installer des distributeurs de sacs à déjections canines dans tous les quartiers")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # climat-adaptation : NOUVEAU (propositions 25, 32)
    r = set_proposition(categories, 'environnement', 'climat-adaptation',
        "Réduire les îlots de chaleur par la végétalisation et l'aménagement paysager adapté, "
        "et lutter contre la prolifération du moustique tigre par des actions de prévention")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # renovation-energetique : conserver (proposition 24)
    # Existant : "Exonération de taxe foncière pendant 3 ans pour les propriétaires réalisant une rénovation énergétique"

    # alimentation-durable : pas de proposition spécifique dans le programme

    # =====================================================================
    # SANTÉ & ACCÈS AUX SOINS
    # =====================================================================

    # centres-sante : NOUVEAU (propositions 84-85, 97)
    r = set_proposition(categories, 'sante', 'centres-sante',
        "Faciliter l'installation de professionnels de santé dans les quartiers sous-dotés, "
        "coordonner avec les professionnels pour un accès équitable et rapide aux soins de qualité "
        "et créer une mutuelle santé complémentaire municipale")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # prevention-sante : NOUVEAU (proposition 74)
    r = set_proposition(categories, 'sante', 'prevention-sante',
        "Soutenir les projets de développement du CHU de Dijon")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # seniors : NOUVEAU (propositions 95-96)
    r = set_proposition(categories, 'sante', 'seniors',
        "Garantir le bien-être des résidents dans les EHPAD municipaux "
        "et développer des programmes de visites pour lutter contre l'isolement des personnes âgées")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # =====================================================================
    # DÉMOCRATIE & VIE CITOYENNE
    # =====================================================================

    # budget-participatif : ENRICHIR (proposition 62)
    r = set_proposition(categories, 'democratie', 'budget-participatif',
        "Renforcer le rôle des conseils de quartier "
        "et associer les citoyens aux grandes décisions par des référendums locaux")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # transparence : ENRICHIR (propositions 57-61)
    r = set_proposition(categories, 'democratie', 'transparence',
        "Baisser la taxe foncière de 5% dès 2026, réduire le nombre d'adjoints de 22 à 15, "
        "diviser les dépenses de communication par 2, supprimer les frais de représentation du maire "
        "et renégocier les contrats coûteux (OnDijon, hydrogène, Cité de la Gastronomie)")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # vie-associative : NOUVEAU (propositions 66, 86)
    r = set_proposition(categories, 'democratie', 'vie-associative',
        "Garantir un financement équitable et transparent des associations "
        "et encourager le bénévolat et l'engagement citoyen à tous les âges")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # services-publics : NOUVEAU (propositions 64-65, 82-83)
    r = set_proposition(categories, 'democratie', 'services-publics',
        "Améliorer et simplifier le premier contact dans tous les services municipaux, "
        "renforcer les compétences et le respect du personnel municipal, "
        "établir une antenne physique du CCAS dans chacun des 9 quartiers "
        "et conditionner la solidarité municipale au respect des devoirs")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # =====================================================================
    # ÉCONOMIE & EMPLOI
    # =====================================================================

    # commerce-local : ENRICHIR (propositions 69-71, 78)
    r = set_proposition(categories, 'economie', 'commerce-local',
        "Réviser les redevances terrasses et enseignes, "
        "soutenir les commerces de proximité par une écoute active, "
        "valoriser l'artisanat local et le \"Made in Dijon\" "
        "et améliorer l'offre d'immobilier commercial en qualité et en prix")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # emploi-insertion : ENRICHIR (propositions 68, 87)
    r = set_proposition(categories, 'economie', 'emploi-insertion',
        "Faciliter l'accès des PME locales à la commande publique municipale "
        "et faire de l'emploi la priorité contre la pauvreté et l'exclusion sociale")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # attractivite : ENRICHIR (propositions 56, 67, 72, 75-77)
    r = set_proposition(categories, 'economie', 'attractivite',
        "Soutenir les filières d'excellence (santé, agroalimentaire), attirer l'industrie de défense, "
        "défendre la zone franche de Fontaine-d'Ouche avec des avantages fiscaux, "
        "défendre la desserte ferroviaire vers Paris-CDG et Lyon, "
        "créer un complexe intégré exposition-congrès-sport "
        "et développer une stratégie touristique concertée avec les acteurs locaux")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # =====================================================================
    # CULTURE & PATRIMOINE
    # =====================================================================

    # equipements-culturels : ENRICHIR (propositions 98-104, 108-111)
    r = set_proposition(categories, 'culture', 'equipements-culturels',
        "Réhabiliter les Halles centrales comme coeur gastronomique de la ville, "
        "mettre fin à l'échec de la Cité de la Gastronomie et lui donner une nouvelle vocation utile, "
        "valoriser la Chartreuse de Champmol et le Puits de Moïse, "
        "ouvrir le Palais des Ducs aux visiteurs, "
        "plan pluriannuel d'investissement pour la rénovation du patrimoine "
        "et création d'un espace dédié à l'héritage de Gustave Eiffel")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # evenements-creation : NOUVEAU (propositions 101, 105-107, 109, 111)
    r = set_proposition(categories, 'culture', 'evenements-creation',
        "Accueillir la fête tournante de la Saint-Vincent et raviver les fêtes viticoles, "
        "créer un réseau de villes européennes lié à l'histoire des ducs de Bourgogne, "
        "développer l'offre de \"théâtre de boulevard\", "
        "soutenir les associations culturelles et artistes locaux "
        "et revitaliser l'enseignement artistique municipal et le chant choral")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # =====================================================================
    # SPORT & LOISIRS
    # =====================================================================

    # equipements-sportifs : ENRICHIR (propositions 112-113, 121-122)
    r = set_proposition(categories, 'sport', 'equipements-sportifs',
        "Programme majeur de rénovation des salles sportives municipales, "
        "création d'un parc aquatique connecté au réseau de chaleur urbain, "
        "reconstruction de la patinoire "
        "et soutien à la construction d'une salle d'athlétisme couverte et d'une enceinte de handball professionnel")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # sport-pour-tous : ENRICHIR (propositions 114-120)
    r = set_proposition(categories, 'sport', 'sport-pour-tous',
        "Relancer \"Dijon Sport Découverte\" pendant les vacances scolaires, "
        "renforcer l'apprentissage de la natation pour que chaque élève sache nager en fin de primaire, "
        "accompagner les sportifs dijonnais jusqu'au haut niveau, "
        "créer un trail métropolitain valorisant le patrimoine naturel, "
        "accueillir des événements sportifs nationaux (Tour de France, championnats) "
        "et accroître l'implication municipale dans le sport amateur et le handisport")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # =====================================================================
    # URBANISME & CADRE DE VIE
    # =====================================================================

    # amenagement-urbain : ENRICHIR (propositions 22, 37-38)
    r = set_proposition(categories, 'urbanisme', 'amenagement-urbain',
        "Réviser le PLUi pour réduire les objectifs de constructions nouvelles et lutter contre la bétonisation, "
        "poursuivre l'embellissement et la végétalisation de la place Grangier "
        "et mener une réflexion approfondie sur le devenir du site de la Porte-Neuve")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # accessibilite : NOUVEAU (propositions 46, 55)
    r = set_proposition(categories, 'urbanisme', 'accessibilite',
        "Garantir des trottoirs accessibles et sécurisés pour les personnes âgées et handicapées "
        "et équiper les feux tricolores de signaux sonores pour les personnes malvoyantes")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # quartiers-prioritaires : NOUVEAU (propositions 72, 82, 94)
    r = set_proposition(categories, 'urbanisme', 'quartiers-prioritaires',
        "Défendre la zone franche urbaine de Fontaine-d'Ouche, "
        "installer une antenne du CCAS dans chaque quartier "
        "et déplacer les hébergements d'urgence vers des espaces plus adaptés")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # =====================================================================
    # SOLIDARITÉ & ÉGALITÉ
    # =====================================================================

    # aide-sociale : NOUVEAU (propositions 82-83, 87, 94)
    r = set_proposition(categories, 'solidarite', 'aide-sociale',
        "Présence physique du CCAS dans les 9 quartiers, "
        "priorité à l'emploi contre la pauvreté et l'exclusion sociale "
        "et relocalisation des hébergements d'urgence dans des espaces plus adaptés")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # pouvoir-achat : ENRICHIR (proposition 57)
    # Existant : "Baisser la taxe foncière de 5% dès 2026"
    r = set_proposition(categories, 'solidarite', 'pouvoir-achat',
        "Baisser la taxe foncière de 5% dès 2026, "
        "gratuité de la première demi-heure de stationnement, "
        "réduction du forfait post-stationnement à 15 euros "
        "et exonération de taxe foncière pendant 3 ans pour rénovation énergétique")
    if r is True: count_new += 1
    elif r is False: count_updated += 1

    # egalite-discriminations : pas de proposition spécifique identifiée

    print()
    print(f"  Total : {count_new} nouvelles propositions ajoutées, {count_updated} mises à jour")
    return count_new + count_updated


def verifier_couverture(data):
    """Vérifie la couverture des sous-thèmes pour Bichot"""
    total = 0
    couverts = 0
    vides = []

    for cat in data['categories']:
        for st in cat['sousThemes']:
            total += 1
            prop = st['propositions'].get(CANDIDAT_ID)
            if prop is not None:
                couverts += 1
            else:
                vides.append(f"{cat['id']} > {st['id']}")

    print(f"  Couverture : {couverts}/{total} sous-thèmes")
    if vides:
        print(f"  Sous-thèmes sans proposition ({len(vides)}) :")
        for v in vides:
            print(f"    - {v}")
    return couverts


def main():
    """Fonction principale"""
    print("=" * 70)
    print("INTÉGRATION DU PROGRAMME D'EMMANUEL BICHOT (DIJON 2026)")
    print("122 propositions - Agir pour Dijon (LR/UDI/Horizons)")
    print("=" * 70)
    print()

    # Chargement du JSON
    print("1. Chargement du fichier JSON...")
    data = charger_json()
    print(f"   {len(data['candidats'])} candidats, {len(data['categories'])} catégories")
    print()

    # Mise à jour du candidat
    print("2. Mise à jour des informations du candidat...")
    mettre_a_jour_candidat(data)
    print()

    # Intégration des propositions
    print("3. Intégration des propositions...")
    count = integrer_propositions(data)
    print()

    # Vérification de la couverture
    print("4. Vérification de la couverture...")
    couverts = verifier_couverture(data)
    print()

    # Sauvegarde
    print("5. Sauvegarde du fichier JSON...")
    sauvegarder_json(data)
    print()

    print("=" * 70)
    print(f"TERMINÉ : {count} propositions intégrées/mises à jour")
    print(f"Couverture : {couverts} sous-thèmes sur 44")
    print(f"programmeComplet = True (122 propositions)")
    print("=" * 70)
    print()
    print("MAPPING DES 122 PROPOSITIONS PAR THÈME :")
    print("- Sécurité (1-21) : police-municipale, videoprotection, prevention-mediation, violences-femmes")
    print("- Cadre de vie (22-41) : espaces-verts, proprete-dechets, climat-adaptation, renovation-energetique,")
    print("                         amenagement-urbain, logement-social, logements-vacants, acces-logement")
    print("- Mobilité (42-55) : transports-en-commun, pietons-circulation, velo-mobilites-douces, stationnement,")
    print("                     tarifs-gratuite, accessibilite")
    print("- Gestion (56-66) : transparence, budget-participatif, pouvoir-achat, services-publics")
    print("- Économie (67-79) : attractivite, commerce-local, emploi-insertion, jeunesse")
    print("- Social (80-97) : logement-social, aide-sociale, petite-enfance, ecoles-renovation, centres-sante,")
    print("                   prevention-sante, seniors, quartiers-prioritaires")
    print("- Culture (98-111) : equipements-culturels, evenements-creation")
    print("- Sport (112-122) : equipements-sportifs, sport-pour-tous")
    print()
    print("SOURCES :")
    print(f"- {SOURCE_PRINCIPALE}")
    print(f"  {SOURCE_URL_PRINCIPALE}")
    print(f"- {SOURCE_SITE}")
    print(f"  {SOURCE_URL_SITE}")
    print()
    print("SOUS-THÈMES NON COUVERTS (pas de proposition identifiée) :")
    print("- encadrement-loyers : pas de mesure d'encadrement des loyers")
    print("- cantines-fournitures : pas de mesure spécifique sur les cantines")
    print("- alimentation-durable : pas de mesure sur l'alimentation durable")
    print("- egalite-discriminations : pas de mesure spécifique identifiée")
    print()


if __name__ == '__main__':
    main()
