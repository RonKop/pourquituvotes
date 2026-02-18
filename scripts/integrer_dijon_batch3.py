#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration batch 3 - Dijon 2026
Complétion des programmes de Koenders et Haberstrau

KOENDERS (23 → 23 propositions) :
  Le site koenders2026.fr/programme/ affiche des tuiles thématiques visuelles
  (Pouvoir d'achat, Sécurité, Transition écologique, etc.) SANS sous-pages détaillées.
  Pas de nouvelles mesures structurées trouvées au-delà de la presse locale.
  programmeComplet reste false (pas de programme détaillé publié en ligne).

HABERSTRAU (22 → 28 propositions) :
  Le site dijonchangedere.fr/programme/ liste 28 mesures numérotées.
  Source : https://dijonchangedere.fr/programme/
  + PDF 28 mesures : https://dijonchangedere.fr/wp-content/uploads/2026/01/2026-01-16_28mesures.pdf
  → Mise à jour des textes existants avec les formulations officielles du site
  → Ajout des mesures manquantes
  → programmeComplet = True (28 mesures concrètes)
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

# Sources Haberstrau
HABERSTRAU_SOURCE = "Site officiel Dijon Change d'ère, 2026"
HABERSTRAU_SOURCE_URL = "https://dijonchangedere.fr/programme/"

# Sources Koenders (presse)
KOENDERS_SOURCE_INFOS = "Infos Dijon, 2026"
KOENDERS_SOURCE_URL_INFOS = "https://www.infos-dijon.com/news/vie-locale/vie-locale/dijon-nathalie-koenders-entre-en-campagne-avec-un-projet-et-une-liste.html"
KOENDERS_SOURCE_DA = "Dijon Actualités, 2026"
KOENDERS_SOURCE_URL_DA = "https://dijon-actualites.fr/2026/02/06/nathalie-koenders-un-meeting-a-plus-de-700-participants-dans-une-ambiance-de-campagne/"
KOENDERS_SOURCE_IB = "Info Beaune, 2026"
KOENDERS_SOURCE_URL_IB = "https://www.info-beaune.com/articles/2026/02/05/14211/municipales-2026-a-dijon-nathalie-koenders-entre-en-campagne-devant-plus-de-700-dijonnais/"


def charger_json():
    """Charge le fichier JSON existant"""
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def sauvegarder_json(data):
    """Sauvegarde le fichier JSON avec UTF-8"""
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Fichier sauvegardé : {JSON_PATH}")


def set_proposition(categories_dict, cat_id, st_id, candidat_id, texte, source, source_url):
    """
    Ajoute ou met à jour une proposition.
    Retourne 'new', 'updated' ou 'error'.
    """
    cat = categories_dict.get(cat_id)
    if not cat:
        print(f"  ERREUR : catégorie '{cat_id}' introuvable")
        return 'error'

    for st in cat['sousThemes']:
        if st['id'] == st_id:
            was_null = (st['propositions'].get(candidat_id) is None)
            st['propositions'][candidat_id] = {
                'texte': texte,
                'source': source,
                'sourceUrl': source_url
            }
            status = "AJOUTÉ" if was_null else "MIS À JOUR"
            print(f"  [{candidat_id}] {status} : {cat_id} > {st_id}")
            return 'new' if was_null else 'updated'

    print(f"  ERREUR : sous-thème '{st_id}' introuvable dans '{cat_id}'")
    return 'error'


def integrer_haberstrau(data, categories):
    """
    Intègre les 28 mesures officielles de Michel Haberstrau.
    Mise à jour des textes existants avec les formulations du site officiel,
    et ajout des mesures manquantes.
    """
    print("  --- HABERSTRAU : 28 mesures du site dijonchangedere.fr ---")
    count_new = 0
    count_updated = 0
    cid = "haberstrau"
    src = HABERSTRAU_SOURCE
    url = HABERSTRAU_SOURCE_URL

    # Mise à jour programmeUrl et programmeComplet
    for candidat in data['candidats']:
        if candidat['id'] == cid:
            candidat['programmeUrl'] = "https://dijonchangedere.fr/"
            candidat['programmeComplet'] = True  # 28 mesures = programme complet
            print(f"  Candidat mis à jour : programmeComplet=True, programmeUrl=https://dijonchangedere.fr/")
            break

    # =====================================================================
    # AXE 1 : Garantir l'accès aux services et aux besoins essentiels
    # =====================================================================

    # Mesure 1 : Gratuité premiers m³ d'eau + tarification progressive → pouvoir-achat (NOUVEAU)
    r = set_proposition(categories, 'solidarite', 'pouvoir-achat', cid,
        "Instaurer la gratuité des premiers mètres cubes d'eau et la tarification progressive "
        "des suivants, pour faire de l'accès à l'eau un droit fondamental effectif",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 2 : Transports gratuits → tarifs-gratuite (MISE À JOUR texte officiel)
    r = set_proposition(categories, 'transports', 'tarifs-gratuite', cid,
        "Rendre les transports en commun gratuits pour les moins de 26 ans, "
        "les personnes en situation de handicap et les bénéficiaires des minima sociaux",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 3 : Sécurité sociale de l'alimentation → alimentation-durable (MISE À JOUR)
    r = set_proposition(categories, 'environnement', 'alimentation-durable', cid,
        "Lancer la Sécurité sociale de l'alimentation à Dijon pour faciliter "
        "l'accès de toutes et tous à une alimentation locale et bonne pour la santé",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 4 : 10% budget aux associations → vie-associative (MISE À JOUR)
    r = set_proposition(categories, 'democratie', 'vie-associative', cid,
        "Porter à 10% la part du budget municipal consacrée aux associations "
        "culturelles, sportives, sociales et solidaires, piliers du lien social et de l'émancipation",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 5 : Reprise en gestion publique → services-publics (MISE À JOUR)
    r = set_proposition(categories, 'democratie', 'services-publics', cid,
        "Engager un processus de reprise en gestion municipale et métropolitaine des services publics essentiels "
        "aujourd'hui confiés au privé (eau, déchets, transports, petite enfance), "
        "dont la gouvernance sera coordonnée entre syndicats, collectifs d'usagers et collectivités",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 6 : ATSEM par classe → petite-enfance (MISE À JOUR)
    r = set_proposition(categories, 'education', 'petite-enfance', cid,
        "Renforcer le nombre d'ATSEM dans les écoles maternelles pour tendre vers une ATSEM par classe",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # =====================================================================
    # AXE 2 : Urbanisme et logement
    # =====================================================================

    # Mesure 7 : Encadrement des loyers → encadrement-loyers (MISE À JOUR, plus détaillé)
    r = set_proposition(categories, 'logement', 'encadrement-loyers', cid,
        "Solliciter la préfecture pour le classement de Dijon en zone tendue et appliquer "
        "l'encadrement des loyers dans les 6 premiers mois après son obtention ; "
        "réguler les locations de courte durée (type Airbnb) via un régime déclaratif et une limitation stricte",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 8 : Logements sociaux à 25% → logement-social (MISE À JOUR)
    r = set_proposition(categories, 'logement', 'logement-social', cid,
        "Agir pour l'accès de toutes et tous à un logement digne, en augmentant le parc locatif "
        "par la limitation des usages spéculatifs et temporaires, "
        "et en portant la part de logements sociaux à 25%",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 9 : Rénovation thermique massive → renovation-energetique (MISE À JOUR)
    r = set_proposition(categories, 'environnement', 'renovation-energetique', cid,
        "Rénovation massive du parc public et privé en priorité sur les passoires thermiques, "
        "avec exonération de taxe foncière pour les propriétaires engagés dans des travaux performants "
        "(matériaux biosourcés privilégiés)",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 10 : "Dijon, Grandeur Nature" → espaces-verts (MISE À JOUR, plus détaillé)
    r = set_proposition(categories, 'environnement', 'espaces-verts', cid,
        "\"Dijon, Grandeur Nature\" : désimperméabilisation, plantations massives "
        "(arbres, haies, micro-forêts, forêts comestibles, jardins partagés), "
        "révision du PLUi-HD (protection des arbres, zéro artificialisation brute), "
        "pour que chacun soit à moins de 5 minutes d'un espace de nature",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 11 : Rénov'École → ecoles-renovation (MISE À JOUR)
    r = set_proposition(categories, 'education', 'ecoles-renovation', cid,
        "Accélérer la végétalisation et la rénovation des écoles par un plan ambitieux \"Rénov'École\"",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 12 : Ville à hauteur d'enfants → pietons-circulation (NOUVEAU)
    r = set_proposition(categories, 'transports', 'pietons-circulation', cid,
        "\"Ville à hauteur d'enfants\" : sécurisation des abords d'écoles, "
        "places piétonnisées, ombrage, aménagements favorisant l'autonomie des plus jeunes",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 13 : Arrêt phase II Maraîchers → climat-adaptation (MISE À JOUR, plus spécifique)
    r = set_proposition(categories, 'environnement', 'climat-adaptation', cid,
        "Arrêt des constructions de la phase II de l'écoquartier des Maraîchers "
        "et révision du PLUi-HD avec objectif zéro artificialisation brute",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 14 : Rouvrir le Suzon → amenagement-urbain (NOUVEAU)
    r = set_proposition(categories, 'urbanisme', 'amenagement-urbain', cid,
        "Rouvrir le Suzon et aménager des promenades végétalisées et continues le long de l'Ouche, "
        "pour remettre l'eau, la fraîcheur et le vivant au cœur de Dijon",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # =====================================================================
    # AXE 3 : Retisser la ville, désenclaver et revitaliser
    # =====================================================================

    # Mesure 15 : Réseau marche et vélo → velo-mobilites-douces (MISE À JOUR)
    r = set_proposition(categories, 'transports', 'velo-mobilites-douces', cid,
        "Déployer un réseau continu, sécurisé et confortable, pour la marche et le vélo, "
        "à l'échelle de la ville et de la métropole",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 16 : Questionner tracé 3e ligne tramway → transports-en-commun (MISE À JOUR)
    r = set_proposition(categories, 'transports', 'transports-en-commun', cid,
        "Questionner le tracé de la troisième ligne de tramway, "
        "afin de redonner la parole aux citoyens et de prioriser le désenclavement "
        "des quartiers (Fontaine-d'Ouche...)",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 17 : Égalité d'accès services de proximité → quartiers-prioritaires (MISE À JOUR)
    r = set_proposition(categories, 'urbanisme', 'quartiers-prioritaires', cid,
        "Garantir l'égalité d'accès aux services de proximité essentiels dans tous les quartiers, "
        "tels que les crèches et les services à la population",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 18 : Équipements de santé dans quartiers déficitaires → centres-sante (MISE À JOUR)
    r = set_proposition(categories, 'sante', 'centres-sante', cid,
        "Soutenir l'implantation d'équipements de santé dans les quartiers les plus déficitaires, "
        "en lien avec les professionnels de santé et les habitants, "
        "et expérimenter la création d'un tiers-lieu en santé",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 19 : Prévention et médiation → prevention-mediation (MISE À JOUR, texte officiel complet)
    r = set_proposition(categories, 'securite', 'prevention-mediation', cid,
        "Mettre en place un dispositif municipal permanent de prévention et de médiation dans l'espace public, "
        "structuré autour d'un service de prévention associant éducateurs spécialisés diplômés et médiateurs professionnels, "
        "agissant en complémentarité avec une police municipale de proximité, "
        "afin de prévenir les incivilités, renforcer la tranquillité publique et rétablir durablement le lien social",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 20 : Soutenir artisanat et commerce → commerce-local (MISE À JOUR, enrichir)
    # L'existant parle des baux commerciaux (mesure 21), on fusionne les deux
    r = set_proposition(categories, 'economie', 'commerce-local', cid,
        "Soutenir les activités d'artisanat et de commerce dans le centre-ville et les quartiers ; "
        "créer un dispositif de contrôle des baux commerciaux pour plafonner les loyers, "
        "favoriser la diversification des commerces et réguler l'implantation de certains d'entre eux",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 21 : Baux commerciaux → fusionné dans commerce-local ci-dessus

    # =====================================================================
    # AXE 4 : Penser l'avenir ensemble, réparer, rafraîchir
    # =====================================================================

    # Mesure 22 : Assemblées citoyennes décisionnaires → budget-participatif (MISE À JOUR)
    r = set_proposition(categories, 'democratie', 'budget-participatif', cid,
        "Lancer un processus d'assemblées citoyennes régulières véritablement décisionnaires "
        "sur les grands projets de la ville, comme la Cité Internationale de la Gastronomie et du Vin, "
        "le réseau de transports et les projets d'urbanisme",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 23 : Plan pluriannuel rénovation infrastructures → equipements-sportifs (NOUVEAU)
    r = set_proposition(categories, 'sport', 'equipements-sportifs', cid,
        "Lancer un plan pluriannuel de rénovation des infrastructures sportives, culturelles et d'accueil",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 24 : Zéro rue non accessible PMR → accessibilite (MISE À JOUR)
    r = set_proposition(categories, 'urbanisme', 'accessibilite', cid,
        "Atteindre l'objectif de zéro rue non accessible aux personnes à mobilité réduite "
        "d'ici la fin du mandat",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 25 : Soutenir SCOP/SCIC → emploi-insertion (MISE À JOUR)
    # On fusionne mesures 25 et 26 (conditionnalité des aides)
    r = set_proposition(categories, 'economie', 'emploi-insertion', cid,
        "S'engager à soutenir les projets de relance de l'activité industrielle par les salariés "
        "dans le cadre des SCOP et des SCIC ; conditionner les aides municipales aux entreprises "
        "à des engagements clairs et durables : créer des emplois, respecter des critères sociaux "
        "et environnementaux, et rester implantées sur le territoire",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 26 : Conditionner aides → fusionné dans emploi-insertion ci-dessus

    # Mesure 27 : Coopérations territoriales → attractivite (NOUVEAU)
    r = set_proposition(categories, 'economie', 'attractivite', cid,
        "Développer des coopérations territoriales au sens large "
        "(entreprise, artisanat, service public, enseignement) "
        "pour renforcer l'ancrage local et la complémentarité entre acteurs du territoire",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    # Mesure 28 : Convention citoyenne Dijon Cap 2050 → transparence (NOUVEAU)
    # budget-participatif a déjà les assemblées citoyennes, on met Cap 2050 dans transparence
    r = set_proposition(categories, 'democratie', 'transparence', cid,
        "Organiser une convention citoyenne \"Dijon Cap 2050\", "
        "chargée de décider des grandes orientations de la ville en matière de transitions écologique "
        "et sociale, d'autonomie alimentaire et d'adaptation de la ville aux conditions de vie en 2050",
        src, url)
    if r == 'new': count_new += 1
    elif r == 'updated': count_updated += 1

    print()
    print(f"  HABERSTRAU : {count_new} nouvelles propositions, {count_updated} mises à jour")
    return count_new, count_updated


def integrer_koenders(data, categories):
    """
    Koenders : le site koenders2026.fr/programme/ n'a pas de mesures détaillées.
    Seules des tuiles thématiques visuelles sans sous-pages.
    On ne modifie PAS les propositions existantes (issues de la presse locale).
    On garde programmeComplet = false.

    Note : les Q&A du site (koenders2026.fr/categorie/question-reponse/)
    contiennent des positionnements généraux mais pas de mesures numérotées nouvelles.
    """
    print("  --- KOENDERS : Vérification du site koenders2026.fr ---")
    print("  Le site n'a pas de programme détaillé avec des mesures numérotées.")
    print("  Les 23 propositions existantes (issues de la presse locale) restent inchangées.")
    print("  programmeComplet reste false.")
    print()

    # Mise à jour de l'URL du programme (qui est la page programme du site)
    for candidat in data['candidats']:
        if candidat['id'] == 'koenders':
            candidat['programmeUrl'] = "https://koenders2026.fr/programme/"
            print(f"  programmeUrl mis à jour : https://koenders2026.fr/programme/")
            break

    return 0, 0


def verifier_couverture(data, candidat_id, candidat_nom):
    """Vérifie la couverture des sous-thèmes pour un candidat"""
    total = 0
    couverts = 0
    vides = []

    for cat in data['categories']:
        for st in cat['sousThemes']:
            total += 1
            prop = st['propositions'].get(candidat_id)
            if prop is not None:
                couverts += 1
            else:
                vides.append(f"{cat['id']} > {st['id']}")

    print(f"  {candidat_nom} : {couverts}/{total} sous-thèmes couverts")
    if vides:
        print(f"    Sous-thèmes sans proposition ({len(vides)}) :")
        for v in vides:
            print(f"      - {v}")
    return couverts


def main():
    """Fonction principale"""
    print("=" * 70)
    print("INTÉGRATION BATCH 3 - DIJON 2026")
    print("Complétion des programmes Koenders et Haberstrau")
    print("=" * 70)
    print()

    # Chargement
    print("1. Chargement du fichier JSON...")
    data = charger_json()
    print(f"   {len(data['candidats'])} candidats, {len(data['categories'])} catégories")
    print()

    categories = {cat['id']: cat for cat in data['categories']}

    # Intégration Koenders
    print("2. Intégration KOENDERS...")
    k_new, k_upd = integrer_koenders(data, categories)
    print()

    # Intégration Haberstrau
    print("3. Intégration HABERSTRAU...")
    h_new, h_upd = integrer_haberstrau(data, categories)
    print()

    # Vérification couverture
    print("4. Vérification de la couverture...")
    k_cov = verifier_couverture(data, 'koenders', 'Koenders')
    h_cov = verifier_couverture(data, 'haberstrau', 'Haberstrau')
    print()

    # Sauvegarde
    print("5. Sauvegarde du fichier JSON...")
    sauvegarder_json(data)
    print()

    # Résumé
    print("=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    print(f"  KOENDERS : {k_new} ajouts, {k_upd} mises à jour → {k_cov}/44 sous-thèmes")
    print(f"    programmeComplet = false (pas de programme détaillé en ligne)")
    print(f"  HABERSTRAU : {h_new} ajouts, {h_upd} mises à jour → {h_cov}/44 sous-thèmes")
    print(f"    programmeComplet = true (28 mesures officielles)")
    print()
    print("MAPPING DES 28 MESURES HABERSTRAU :")
    print("  AXE 1 - Accès aux services et besoins essentiels :")
    print("    1. pouvoir-achat : gratuité premiers m³ d'eau")
    print("    2. tarifs-gratuite : transports gratuits")
    print("    3. alimentation-durable : sécurité sociale de l'alimentation")
    print("    4. vie-associative : 10% budget aux associations")
    print("    5. services-publics : reprise en gestion publique")
    print("    6. petite-enfance : une ATSEM par classe")
    print("  AXE 2 - Urbanisme et logement :")
    print("    7. encadrement-loyers : zone tendue + Airbnb")
    print("    8. logement-social : 25% logements sociaux")
    print("    9. renovation-energetique : rénovation massive")
    print("    10. espaces-verts : Dijon Grandeur Nature")
    print("    11. ecoles-renovation : Rénov'École")
    print("    12. pietons-circulation : ville à hauteur d'enfants")
    print("    13. climat-adaptation : arrêt Maraîchers + PLUi")
    print("    14. amenagement-urbain : rouvrir le Suzon")
    print("  AXE 3 - Retisser la ville, désenclaver :")
    print("    15. velo-mobilites-douces : réseau marche/vélo")
    print("    16. transports-en-commun : questionner tracé T3")
    print("    17. quartiers-prioritaires : égalité d'accès services")
    print("    18. centres-sante : équipements de santé")
    print("    19. prevention-mediation : dispositif permanent")
    print("    20-21. commerce-local : artisanat + baux (fusionnés)")
    print("  AXE 4 - Penser l'avenir, réparer, rafraîchir :")
    print("    22. budget-participatif : assemblées décisionnaires")
    print("    23. equipements-sportifs : plan rénovation infra")
    print("    24. accessibilite : zéro rue non accessible")
    print("    25-26. emploi-insertion : SCOP/SCIC + aides conditionnées (fusionnés)")
    print("    27. attractivite : coopérations territoriales")
    print("    28. transparence : convention Dijon Cap 2050")
    print()


if __name__ == '__main__':
    main()
