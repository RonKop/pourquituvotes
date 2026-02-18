#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration du programme complet de Patrick Indjian (Rueil-Malmaison 2026)
Source : PDF programme complet (27 pages) telecharge depuis patrickindjianrueil2026.fr/programme.pdf

Mapping des mesures du PDF aux 44 sous-themes communs.
Le PDF contient bien plus de 15 mesures concretes => programmeComplet: true
"""

import sys
import io
import json
import os

# Configuration UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Chemin du fichier JSON
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(SCRIPT_DIR, "..", "data", "elections", "rueil-malmaison-2026.json")

# Source
SOURCE = "Programme complet Rueil en Commun (PDF)"
SOURCE_URL = "https://www.patrickindjianrueil2026.fr/programme.pdf"
PROGRAMME_URL = "https://www.patrickindjianrueil2026.fr/programme.pdf"


def charger_json():
    """Charge le fichier JSON existant"""
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def sauvegarder_json(data):
    """Sauvegarde le fichier JSON avec UTF-8"""
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Fichier sauvegarde : {JSON_PATH}")


def mettre_a_jour_candidat(data):
    """Met a jour les informations du candidat Indjian"""
    for candidat in data['candidats']:
        if candidat['id'] == 'indjian':
            candidat['programmeUrl'] = "https://www.patrickindjianrueil2026.fr/"
            candidat['programmeComplet'] = True
            candidat['programmePdfPath'] = "indjian-rueil-programme.pdf"
            print(f"  Candidat mis a jour : programmeComplet=True, programmePdfPath ajoute")
            break


def ajouter_proposition(categorie, sous_theme_id, texte, source=SOURCE, source_url=SOURCE_URL, forcer=False):
    """
    Ajoute une proposition pour Indjian dans un sous-theme.
    Si forcer=True, ecrase la proposition existante.
    Si forcer=False (defaut), n'ecrase que si le nouveau texte est significativement plus complet.
    """
    for st in categorie['sousThemes']:
        if st['id'] == sous_theme_id:
            existant = st['propositions'].get('indjian')
            if existant and not forcer:
                # Ne remplacer que si le nouveau texte est significativement plus long (>50% plus long)
                if len(texte) <= len(existant['texte']) * 1.5:
                    return False  # On garde l'existant
            st['propositions']['indjian'] = {
                'texte': texte,
                'source': source,
                'sourceUrl': source_url
            }
            return True
    return False


def integrer_propositions(data):
    """Integre toutes les propositions d'Indjian depuis le PDF programme complet"""

    count = 0
    mis_a_jour = 0
    categories = {cat['id']: cat for cat in data['categories']}

    # ========================================================================
    # SECURITE & PREVENTION
    # ========================================================================

    # police-municipale : enrichi avec PDF (cellules specialisees + permanences)
    if ajouter_proposition(
        categories['securite'],
        'police-municipale',
        "Permanences hebdomadaires de police de proximite dans chaque quartier, co-animees par ASVP et policiers municipaux. Presence d'agents aux abords de toutes les ecoles aux heures d'entrees et de sorties",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : securite > police-municipale (enrichi avec PDF)")

    # videoprotection
    if ajouter_proposition(
        categories['securite'],
        'videoprotection',
        "Opposition a tout nouveau systeme de videosurveillance algorithmique (VSA). Audit independant et retrospectif sur 20 ans pour evaluer l'utilite et le cout reel de chaque camera"
    ):
        count += 1
        print("  Ajoute : securite > videoprotection")

    # prevention-mediation
    if ajouter_proposition(
        categories['securite'],
        'prevention-mediation',
        "Renforcement des equipes de mediateurs intervenant de maniere proactive dans la rue pour apaiser les tensions et creer du lien social. Patrouilles renforcees avec police nationale aux periodes et lieux strategiques contre les cambriolages"
    ):
        count += 1
        print("  Ajoute : securite > prevention-mediation")

    # violences-femmes
    if ajouter_proposition(
        categories['securite'],
        'violences-femmes',
        "Creation de deux cellules de police municipale specialisees dans la lutte contre les violences familiales et sexuelles, en coordination avec la police nationale. Agents formes a l'accueil, l'ecoute et l'orientation des victimes"
    ):
        count += 1
        print("  Ajoute : securite > violences-femmes")

    # ========================================================================
    # TRANSPORTS & MOBILITE
    # ========================================================================

    # transports-en-commun : enrichi
    if ajouter_proposition(
        categories['transports'],
        'transports-en-commun',
        "Navettes scolaires pour les lyceens, retour du petit bus pour personnes agees et en situation de handicap. Travail avec la region pour ameliorer la frequence et la desserte des bus sur toute la ville. Subvention du Pass Navigo pour les revenus les plus modestes",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : transports > transports-en-commun (enrichi avec PDF)")

    # velo-mobilites-douces : enrichi
    if ajouter_proposition(
        categories['transports'],
        'velo-mobilites-douces',
        "Voies cyclables temporaires des 2026, puis pistes cyclables a double sens sur grands axes avec carrefours hollandais. Service public communal du velo avec tarification attractive selon quotient familial. Mise a disposition d'un velo par collegien ou lyceen. Stationnements securises (box, cages) aux endroits strategiques",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : transports > velo-mobilites-douces (enrichi avec PDF)")

    # pietons-circulation
    if ajouter_proposition(
        categories['transports'],
        'pietons-circulation',
        "Passage de la ville en zone 30 (sauf Nationale). Securisation des acces aux ecoles (trottoirs larges, panneaux stop, espaces pietons). Generalisation des sas velo aux feux tricolores. Bataille pour limiter la vitesse sur l'A86 de 90 a 70 km/h"
    ):
        count += 1
        print("  Ajoute : transports > pietons-circulation")

    # stationnement
    if ajouter_proposition(
        categories['transports'],
        'stationnement',
        "Tolerance zero pour les abus de stationnement (double file, voies de velo). Stationnement a prix differencies pour favoriser les petites voitures. Reduction de l'emprise du stationnement en surface la ou les alternatives sont disponibles"
    ):
        count += 1
        print("  Ajoute : transports > stationnement")

    # tarifs-gratuite
    if ajouter_proposition(
        categories['transports'],
        'tarifs-gratuite',
        "Subvention du Pass Navigo pour les revenus les plus modestes. Service public communal du velo avec tarification accessible selon le quotient familial"
    ):
        count += 1
        print("  Ajoute : transports > tarifs-gratuite")

    # ========================================================================
    # LOGEMENT
    # ========================================================================

    # logement-social : enrichi
    if ajouter_proposition(
        categories['logement'],
        'logement-social',
        "Augmenter progressivement la part des logements aides de 25 a 35%, dont une part reservee aux logements les plus sociaux (PLAI). Priorite aux rehabilitations d'immeubles vetustes, conversion de bureaux et surelevation pour limiter la densification. Charte qualite imposee aux promoteurs (materiaux bas carbone, performance energetique, maitrise des prix)",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : logement > logement-social (enrichi avec PDF)")

    # logements-vacants
    if ajouter_proposition(
        categories['logement'],
        'logements-vacants',
        "Garantie municipale en cas d'impayes ou degradation en echange d'un loyer social inferieur au prix du marche, pour inciter les proprietaires de logements vacants a les proposer a la location. En deuxieme intention, declenchement de la requisition des logements vides (articles L641-1 et L641-2 du Code de la construction)"
    ):
        count += 1
        print("  Ajoute : logement > logements-vacants")

    # encadrement-loyers
    if ajouter_proposition(
        categories['logement'],
        'encadrement-loyers',
        "Demande de mise en place de regles specifiques d'encadrement des loyers (zone tres tendue). Prix plafonds au m2 negocies avec les promoteurs immobiliers pour les futurs logements. Developpement des baux reels solidaires (jusqu'a 20% en dessous des prix du marche)"
    ):
        count += 1
        print("  Ajoute : logement > encadrement-loyers")

    # acces-logement : enrichi
    if ajouter_proposition(
        categories['logement'],
        'acces-logement',
        "Soutien d'une association de locataires pour chaque ensemble de logements sociaux. Mise en place du permis de louer pour proteger les locataires contre l'habitat indigne. Observatoire du logement pour la transparence des attributions. 1000 logements d'urgence et logements passerelles pour les plus precaires. Developpement du pret a taux zero et des prets sociaux Location Accession",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : logement > acces-logement (enrichi avec PDF)")

    # ========================================================================
    # EDUCATION & JEUNESSE
    # ========================================================================

    # petite-enfance : enrichi
    if ajouter_proposition(
        categories['education'],
        'petite-enfance',
        "Reouverture de creches familiales gerees par la municipalite avec tarifs sur quotient familial. Metiers de la petite enfance plus attractifs : meilleure remuneration, acces facilite a un logement proche. Transparence dans l'attribution des places en creche via une commission a criteres publics",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : education > petite-enfance (enrichi avec PDF)")

    # ecoles-renovation
    if ajouter_proposition(
        categories['education'],
        'ecoles-renovation',
        "Redonner leurs vraies missions aux ATSEM : fiches de poste centrees sur l'accompagnement, effectifs suffisants par ecole maternelle, revalorisation salariale. Systematisation des etudes dirigees par les enseignants avec taux horaire revalorise"
    ):
        count += 1
        print("  Ajoute : education > ecoles-renovation")

    # cantines-fournitures : enrichi
    if ajouter_proposition(
        categories['education'],
        'cantines-fournitures',
        "Regie municipale pour les cantines : produits locaux, bio, alternative vegetarienne, gratuite selon quotient familial. Prise en charge d'une partie des fournitures scolaires a prix avantageux via appels d'offres publics annuels",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : education > cantines-fournitures (enrichi avec PDF)")

    # periscolaire-loisirs
    if ajouter_proposition(
        categories['education'],
        'periscolaire-loisirs',
        "Accueil periscolaire de 7h30 a 19h pour tous les eleves du primaire. Large choix d'activites : initiations sportives (danse, foot, velo) et artistiques (theatre, ecriture, chant). Subvention a 100% du BAFA pour les jeunes Rueillois en contrepartie d'heures dans les structures d'accueil"
    ):
        count += 1
        print("  Ajoute : education > periscolaire-loisirs")

    # jeunesse
    if ajouter_proposition(
        categories['education'],
        'jeunesse',
        "Antennes Informations Jeunesse dans tous les quartiers. Budget participatif Jeune de 20 000 euros/an pour des projets penses et realises par les jeunes. Deploiement d'activites culturelles des l'ecole primaire avec formation d'animateurs socio-culturels"
    ):
        count += 1
        print("  Ajoute : education > jeunesse")

    # ========================================================================
    # ENVIRONNEMENT & TRANSITION ECOLOGIQUE
    # ========================================================================

    # espaces-verts
    if ajouter_proposition(
        categories['environnement'],
        'espaces-verts',
        "Nouveaux jardins publics avec plantation d'arbres dans tous les quartiers (objectif 30% de couverture arboree par rue). Arbres fruitiers et espaces de production maraichere dans les parcs. Gestion forestiere respectueuse a Saint-Cucufa avec l'ONF. Reduction de la pollution lumineuse pour proteger la biodiversite"
    ):
        count += 1
        print("  Ajoute : environnement > espaces-verts")

    # proprete-dechets
    if ajouter_proposition(
        categories['environnement'],
        'proprete-dechets',
        "Renegociation du contrat dechets pour ramassage plus frequent dans les quartiers en croissance. Points de tri supplementaires (verre, compost). Politique zero dechet dans les etablissements municipaux et ecoles. Tolerance zero pour les incivilites liees aux dechets (jets de megots, papiers gras)"
    ):
        count += 1
        print("  Ajoute : environnement > proprete-dechets")

    # climat-adaptation : enrichi
    if ajouter_proposition(
        categories['environnement'],
        'climat-adaptation',
        "Plan d'urgence canicules pour creches, ecoles et EHPAD (ventilateurs, stores). Zones refuge climatisees ouvertes 24h/24 dans chaque village pendant les canicules. Fontaines d'eau potable dans tous les quartiers. Desimpermeabilisation des quartiers les plus denses. Sensibilisation au risque inondations et exercices de mise en surete pour les crues de la Seine. Plus de permis de construire en zone inondable",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : environnement > climat-adaptation (enrichi avec PDF)")

    # renovation-energetique : enrichi
    if ajouter_proposition(
        categories['environnement'],
        'renovation-energetique',
        "Grand plan de renovation energetique pour batiments publics et logements. Guichet unique de la renovation energetique. Integration d'une competence construction durable dans l'equipe municipale. Promotion de la production energetique individuelle locale et chantiers participatifs d'auto-renovation. Tarification progressive de l'eau selon la consommation",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : environnement > renovation-energetique (enrichi avec PDF)")

    # alimentation-durable
    if ajouter_proposition(
        categories['environnement'],
        'alimentation-durable',
        "Experimentation de la securite sociale de l'alimentation a l'echelle communale. Arbres fruitiers et espaces de maraichage dans les parcs pour alimenter la cantine municipale. AMAP et epiceries solidaires alimentees par des circuits locaux dans chaque quartier"
    ):
        count += 1
        print("  Ajoute : environnement > alimentation-durable")

    # ========================================================================
    # SANTE & ACCES AUX SOINS
    # ========================================================================

    # centres-sante : enrichi
    if ajouter_proposition(
        categories['sante'],
        'centres-sante',
        "Centre municipal de sante de medecins salaries (generalistes, dermatologues, gynecologues, ophtalmologistes), sans depassement d'honoraires. Creation d'un centre de sante sexuelle (consultations anonymes et gratuites, contraception, IVG). Guichet unique de la renovation energetique pour reduire les factures de sante liees a l'habitat",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : sante > centres-sante (enrichi avec PDF)")

    # prevention-sante
    if ajouter_proposition(
        categories['sante'],
        'prevention-sante',
        "Journees intergenerationnelles ecologie et solidarite avec les ecoles. Ateliers de formation contre la fracture numerique et l'illectronisme. Contrat d'assurance habitation negocie par la Mairie pour les habitants non assures"
    ):
        count += 1
        print("  Ajoute : sante > prevention-sante")

    # seniors
    if ajouter_proposition(
        categories['sante'],
        'seniors',
        "EHPAD publics avec augmentation des places et recrutement de personnel soignant. Residences services seniors de proximite. Renforcement des effectifs de la Maison de l'autonomie. Facilitation de l'acces aux services d'aide a domicile avec un referent specialiste du handicap au CCAS. Maintien du lien entre personnes agees et leurs animaux"
    ):
        count += 1
        print("  Ajoute : sante > seniors")

    # ========================================================================
    # DEMOCRATIE & VIE CITOYENNE
    # ========================================================================

    # budget-participatif : enrichi
    if ajouter_proposition(
        categories['democratie'],
        'budget-participatif',
        "Budget participatif annuel de 250 000 euros, avec montee en puissance possible jusqu'a 5% du budget d'investissement. Conseils de villages avec presidents elus par leurs membres (et non nommes par le maire). Referendum d'initiative citoyenne local des 10% de signatures. Votations citoyennes en amont des grands projets structurants",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : democratie > budget-participatif (enrichi avec PDF)")

    # transparence : enrichi
    if ajouter_proposition(
        categories['democratie'],
        'transparence',
        "Audit citoyen de la dette (171 M euros, 2100 euros/habitant) avec cabinet specialise. Recrutement d'un responsable probite. Signature de la charte Anticor. Transparence des rendez-vous avec les interets prives. Open data par defaut pour les finances, marches publics et frais de representation du maire. Suspension de mandat en cas de mise en examen",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : democratie > transparence (enrichi avec PDF)")

    # vie-associative : enrichi
    if ajouter_proposition(
        categories['democratie'],
        'vie-associative',
        "Maisons des associations et des syndicats. Mairies de quartier comme espaces d'echanges. Conventionnement des centres socioculturels avec la CAF. Soutien aux associations accueillant des exiles (mise a disposition de locaux). Tribune dans le Rueil-Info pour les conseils de village et le CMJ",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : democratie > vie-associative (enrichi avec PDF)")

    # services-publics
    if ajouter_proposition(
        categories['democratie'],
        'services-publics',
        "Renforcement des equipes d'assistantes sociales de la ville. Utilisation differente du budget du CCAS pour plus d'actions sociales. Tirage au sort pour inviter les habitants a rejoindre les conseils de village. Garde d'enfants et defraiement lors des reunions participatives"
    ):
        count += 1
        print("  Ajoute : democratie > services-publics")

    # ========================================================================
    # ECONOMIE & EMPLOI
    # ========================================================================

    # commerce-local : enrichi
    if ajouter_proposition(
        categories['economie'],
        'commerce-local',
        "Commerce durable de proximite : seconde main, reparation, artisanat local. Loyers moderes ou aides pour l'installation de nouveaux commerces. Boutiques ephemeres reparties sur toute la ville. Tarifs progressifs pour les nouveaux commercants sur les marches. Ressourceries et ateliers de reparation/recyclage dans chaque quartier",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : economie > commerce-local (enrichi avec PDF)")

    # emploi-insertion : enrichi
    if ajouter_proposition(
        categories['economie'],
        'emploi-insertion',
        "Maison de l'Emploi et de l'Insertion pour accompagnement social et professionnel. Engagement 'Territoire Zero Chomeurs de longue duree'. Clauses sociales d'insertion dans les marches publics. Bourse d'echange de l'emploi avec les entreprises locales. Espaces de coworking a tarifs progressifs. Incubateur d'entreprises. Ateliers de formation (Photoshop, Word, IA, WordPress)",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : economie > emploi-insertion (enrichi avec PDF)")

    # attractivite
    if ajouter_proposition(
        categories['economie'],
        'attractivite',
        "Accompagnement de l'economie dans la bifurcation ecologique : soutien aux entreprises de l'ESS, prets de locaux et vehicules. Achats publics respectueux de l'environnement et socialement responsables. Epiceries solidaires alimentees par des circuits locaux"
    ):
        count += 1
        print("  Ajoute : economie > attractivite")

    # ========================================================================
    # CULTURE & PATRIMOINE
    # ========================================================================

    # equipements-culturels
    if ajouter_proposition(
        categories['culture'],
        'equipements-culturels',
        "Creation de MJC dans chaque quartier. Ouverture plus large du Theatre Andre Malraux avec cours d'art dramatique a tarifs adaptes et troupe en residence. Developpement du Petit Theatre de Rueil. Creation d'une Maison des artistes. Bibliobus pour les quartiers eloignes des bibliotheques"
    ):
        count += 1
        print("  Ajoute : culture > equipements-culturels")

    # evenements-creation : enrichi
    if ajouter_proposition(
        categories['culture'],
        'evenements-creation',
        "Festival annuel 'Rueil en Scene' (theatre de rue, cinema plein air, concerts, arts de rue). Spectacles de rue et evenements culturels dans tous les quartiers en lien avec ecoles et associations. Ateliers periscolaires : spectacles, street art, theatre de marionnettes, notamment en haut de Rueil",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : culture > evenements-creation (enrichi avec PDF)")

    # ========================================================================
    # SPORT & LOISIRS
    # ========================================================================

    # equipements-sportifs
    if ajouter_proposition(
        categories['sport'],
        'equipements-sportifs',
        "Amelioration de la maintenance des equipements sportifs vetustes. Installations sportives dans les secteurs de logements sociaux avec coachs gratuits. Inventaire et redistribution equitable des terrains de sport. Hygiene renforcee des vestiaires et salles de sport"
    ):
        count += 1
        print("  Ajoute : sport > equipements-sportifs")

    # sport-pour-tous : enrichi
    if ajouter_proposition(
        categories['sport'],
        'sport-pour-tous',
        "Tarifs accessibles pour les familles aux bas revenus via revision des quotients familiaux. Accessibilite aux personnes en situation de handicap. Apprentissage de la natation garanti en primaire pour tous les enfants. Tarification culturelle et sportive adaptee aux revenus",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : sport > sport-pour-tous (enrichi avec PDF)")

    # ========================================================================
    # URBANISME & CADRE DE VIE
    # ========================================================================

    # amenagement-urbain
    if ajouter_proposition(
        categories['urbanisme'],
        'amenagement-urbain',
        "Limitation de la densification et de l'artificialisation des sols. Desimpermeabilisation des quartiers les plus denses et betonnes. Vegetalisation des facades et toits avec aide financiere. Amelioration de l'eclairage public avec lampadaires a detecteur de presence. Parcs canins publics repartis equitablement sur le territoire"
    ):
        count += 1
        print("  Ajoute : urbanisme > amenagement-urbain")

    # accessibilite
    if ajouter_proposition(
        categories['urbanisme'],
        'accessibilite',
        "Revue des espaces communs (aires de jeu, trottoirs, signalisation, photomatons) pour les adapter aux personnes en situation de handicap. Referent specialiste du handicap au CCAS. Accessibilite renforcee des equipements sportifs et culturels"
    ):
        count += 1
        print("  Ajoute : urbanisme > accessibilite")

    # quartiers-prioritaires
    if ajouter_proposition(
        categories['urbanisme'],
        'quartiers-prioritaires',
        "Egalite de traitement entre tous les quartiers : vegetalisation prioritaire des quartiers les moins dotes (Plaine Gare, Arsenal). Points d'accueil dans tous les quartiers pour les victimes de discriminations. Centres socioculturels conventionnes avec la CAF pour des activites accessibles a toutes et tous"
    ):
        count += 1
        print("  Ajoute : urbanisme > quartiers-prioritaires")

    # ========================================================================
    # SOLIDARITE & EGALITE
    # ========================================================================

    # aide-sociale
    if ajouter_proposition(
        categories['solidarite'],
        'aide-sociale',
        "Renforcement du CCAS pour plus d'actions sociales aupres des plus vulnerables. Facilitation de l'acces aux services d'aide a domicile. 1000 logements d'urgence et logements passerelles. Soutien aux associations d'aide aux exiles. Politique engagee pour le bien-etre des animaux domestiques avec aides municipales pour eviter les abandons"
    ):
        count += 1
        print("  Ajoute : solidarite > aide-sociale")

    # egalite-discriminations : enrichi
    if ajouter_proposition(
        categories['solidarite'],
        'egalite-discriminations',
        "Points d'accueil dans tous les quartiers pour les victimes de discriminations, harcelements et violences. Soutien systematique des victimes de racisme, sexisme et LGBTphobie par signalement au procureur (art. 40). Observatoires communaux des discriminations. Jumelage avec une ville palestinienne",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : solidarite > egalite-discriminations (enrichi avec PDF)")

    # pouvoir-achat : enrichi
    if ajouter_proposition(
        categories['solidarite'],
        'pouvoir-achat',
        "Elargissement du bareme du quotient familial pour tarifs reduits sur cantine, centre de loisirs et activites. Gratuite des cantines selon quotient familial. Prise en charge partielle des fournitures scolaires. Subvention BAFA a 100% pour les jeunes. Subvention du Pass Navigo pour les revenus modestes. Contrat d'assurance habitation negocie par la Mairie",
        forcer=True
    ):
        count += 1
        print("  Mis a jour : solidarite > pouvoir-achat (enrichi avec PDF)")

    print(f"\n  Total : {count} propositions ajoutees ou mises a jour")
    return count


def compter_propositions(data):
    """Compte le nombre de sous-themes couverts par Indjian"""
    total = 0
    null_count = 0
    for cat in data['categories']:
        for st in cat['sousThemes']:
            prop = st['propositions'].get('indjian')
            if prop is not None:
                total += 1
            else:
                null_count += 1
    return total, null_count


def main():
    """Fonction principale"""
    print("=" * 70)
    print("INTEGRATION DU PROGRAMME DE PATRICK INDJIAN (RUEIL-MALMAISON 2026)")
    print("=" * 70)
    print()

    # Chargement du JSON
    print("1. Chargement du fichier JSON...")
    data = charger_json()
    avant_total, avant_null = compter_propositions(data)
    print(f"   Fichier charge : {len(data['candidats'])} candidats, {len(data['categories'])} categories")
    print(f"   Propositions existantes pour Indjian : {avant_total} / {avant_total + avant_null} sous-themes")
    print()

    # Mise a jour du candidat
    print("2. Mise a jour des informations du candidat...")
    mettre_a_jour_candidat(data)
    print()

    # Integration des propositions
    print("3. Integration des propositions depuis le PDF...")
    count = integrer_propositions(data)
    print()

    # Sauvegarde
    print("4. Sauvegarde du fichier JSON...")
    sauvegarder_json(data)
    print()

    # Statistiques finales
    apres_total, apres_null = compter_propositions(data)
    print("=" * 70)
    print(f"TERMINE")
    print(f"  Propositions avant  : {avant_total} / {avant_total + avant_null}")
    print(f"  Propositions apres  : {apres_total} / {apres_total + apres_null}")
    print(f"  Nouvelles ajoutees  : {apres_total - avant_total}")
    print(f"  Mises a jour        : {count - (apres_total - avant_total)}")
    print(f"  Sous-themes vides   : {apres_null}")
    print("=" * 70)
    print()
    print("SOURCE : PDF programme complet (27 pages)")
    print(f"  {PROGRAMME_URL}")
    print()
    print("NOTES :")
    print("  - programmeComplet passe a True (44 sous-themes couverts)")
    print("  - Les propositions existantes ont ete enrichies quand le PDF apportait plus de details")
    print("  - Encodage UTF-8 sans accents dans les textes pour compatibilite maximale")
    print()


if __name__ == '__main__':
    main()
