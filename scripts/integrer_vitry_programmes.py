#!/usr/bin/env python3
"""
Script d'intégration des programmes de Tmimi et Afflatet
pour Vitry-sur-Seine dans le comparateur municipal.

Sources :
- Tmimi : programme PDF 48 pages (OCR), site vitry2026.fr
- Afflatet : programme PDF 10 pages (texte), site vitryavenir.fr
"""

import json
import os

# Chemin du fichier JSON
JSON_PATH = r'C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\vitry-sur-seine-2026.json'

# Charger le JSON existant
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ============================================================
# TMIMI - Propositions à ajouter (sous-thèmes manquants)
# Source: Programme "Vitry demain 2025-2030" (PDF 48 pages)
# ============================================================

TMIMI_SOURCE = "Programme officiel 2026"
TMIMI_URL = "https://vitry2026.fr/"

tmimi_props = {
    # SÉCURITÉ
    "police-municipale": {
        "texte": "Création d'un deuxième commissariat, rénovation du commissariat actuel, police municipale centrée sur la prévention avec présence régulière et rassurante sur le terrain",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "prevention-mediation": {
        "texte": "Médiateurs présents au quotidien, gardiens d'immeuble, travailleurs sociaux et animateurs dans les quartiers, Conseil local de sécurité et de prévention de la délinquance renforcé",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "violences-femmes": {
        "texte": "Création d'une Maison des Femmes à Vitry : accompagnement pluridisciplinaire, hébergement d'urgence, observatoire contre les violences faites aux femmes, arrêt des bus à la demande après 22h",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    # TRANSPORTS
    "stationnement": {
        "texte": "Rénover, sécuriser et étendre les horaires des parkings en soirée avec deux heures gratuites, refus de la vidéo-verbalisation, stationnement vélo près des commerces et écoles",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "tarifs-gratuite": {
        "texte": "Obtenir les transports gratuits pour lycéens, chômeurs et foyers modestes, navette inter-quartiers gratuite, Vélib' gratuit pour les lycéens, prise en charge du Pass Navigo selon le quotient familial",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    # LOGEMENT
    "logements-vacants": {
        "texte": "Mobilisation des bureaux et logements vacants, dispositif « Louez Solidaire » pour intégrer 1 000 logements vacants au parc social (10 M€ d'investissement prévu)",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "acces-logement": {
        "texte": "Critères d'attribution lisibles (scoring), citoyens tirés au sort dans les commissions, bourse d'échange de logements sociaux, habitat coopératif et intergénérationnel, colocation encadrée",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    # ÉDUCATION
    "ecoles-renovation": {
        "texte": "Plan pluriannuel d'isolation des bâtiments scolaires (30 M€), déminéralisation et végétalisation des cours, îlots de fraîcheur, écoles ouvertes aux associations le soir et le week-end",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "periscolaire-loisirs": {
        "texte": "Gratuité de l'aide aux devoirs et du goûter dès la rentrée 2026, cantine au quotient familial dégressif selon le nombre d'enfants, activité physique quotidienne pour tous",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    # ÉCONOMIE
    "commerce-local": {
        "texte": "Promenade commerçante de la gare à la mairie, halles alimentaires au quartier 8 Mai 1945, piétonnisation le week-end, soutien aux marchés de quartier et petits commerces, charte de la distribution",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "emploi-insertion": {
        "texte": "Objectif « Territoire zéro chômeur de longue durée », parcours emploi-formation ancrés dans le territoire, campus métiers verts, foncière coopérative, monnaie locale citoyenne envisagée",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "attractivite": {
        "texte": "Industrie urbaine moderne : micro-usines, productions décarbonées, ateliers de réparation, fablabs, recycleries, maillage économique par quartiers (Ardoines innovation, centre-ville artisanat)",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    # CULTURE
    "equipements-culturels": {
        "texte": "Rénovation du 3 Cinés Robespierre, soutien au Kilowatt, 6BIS, La Kunda, L'Exploradôme, Gare au Théâtre, renforcement des EMA et classes artistiques (CHAM), soutien aux librairies indépendantes",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "evenements-creation": {
        "texte": "Création d'un festival international, concerts et spectacles dans les quartiers, gratuité du cinéma Robespierre et du théâtre Jean-Vilar pour les moins de 15 ans, guide d'art urbain pour enfants",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    # SPORT
    "equipements-sportifs": {
        "texte": "Modernisation des équipements sportifs (30 M€), nouvel équipement avec un Dojo aux Ardoines, gestion optimisée des créneaux, mutualisation entre scolaires, clubs et habitants, city-stades éclairés",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "sport-pour-tous": {
        "texte": "Objectif 100% savoir nager, Pass Jeunes Culture & Sport (12-25 ans), baignade gratuite dans la Seine en été, flotte municipale de vélos, sport-santé, créneaux inclusifs handicap, formation BPJEPS/BNSSA",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    # URBANISME
    "accessibilite": {
        "texte": "Guichet municipal Handicap & Autonomie, plan pluriannuel pour l'espace public accessible, navettes adaptées, numérique accessible, volet handicap obligatoire dans tout projet municipal",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "quartiers-prioritaires": {
        "texte": "Moratoire sur les démolitions de logements, renégociation des projets de rénovation urbaine, consultation citoyenne sur l'avenir des Ardoines, refus de la bétonisation excessive, 40 M€ pour le renouvellement urbain",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    # SOLIDARITÉ
    "aide-sociale": {
        "texte": "Lutte contre le non-recours aux aides (RSA, APL, AME), repérage des publics invisibles, Mairie mobile pour les parents seuls, hébergement d'urgence municipal, « Visa Parent Solo » pour les familles monoparentales",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
    "pouvoir-achat": {
        "texte": "Gratuité progressive des services (aide aux devoirs, goûter, cinéma pour les jeunes), cantines au quotient familial dégressif, abattement 25 à 40% pour familles monoparentales, halles alimentaires à prix justes",
        "source": TMIMI_SOURCE,
        "sourceUrl": TMIMI_URL
    },
}

# ============================================================
# AFFLATET - Propositions à ajouter
# Source: Programme PDF "Vitry À Venir" (10 pages)
# ============================================================

AFFLATET_SOURCE = "Programme officiel 2026"
AFFLATET_URL = "https://vitryavenir.fr/"

afflatet_props = {
    # SÉCURITÉ
    # police-municipale: EXISTE DÉJÀ
    "videoprotection": {
        "texte": "Installer la vidéoprotection réclamée par les Vitriots, devenue une nécessité pour la sérénité des habitants.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "prevention-mediation": {
        "texte": "Étendre les prérogatives de la police municipale et sa collaboration avec la police nationale, créer un complexe ouvert 24h/24 regroupant police nationale et municipale.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # TRANSPORTS
    "transports-en-commun": {
        "texte": "Dialoguer avec Île-de-France Mobilités pour la création de nouvelles lignes de bus dans Vitry, en connexion avec les gares internes et externes, favoriser une navette fluviale vers Paris.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "velo-mobilites-douces": {
        "texte": "Création d'une piste cyclable depuis l'avenue Jean Jaurès jusqu'à la gare des Ardoines, locaux à vélo obligatoires dans tous les logements pour inciter aux déplacements à vélo.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "pietons-circulation": {
        "texte": "Repenser le plan de circulation pour éviter que Vitry soit une ville de transit, remettre en état la voirie, trottoirs réaménagés.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "stationnement": {
        "texte": "Organiser le stationnement pour éviter les stationnements anarchiques, rouvrir les parkings condamnés par les bailleurs, créer des places aux alentours des futures gares du Grand Paris.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # LOGEMENT
    "logement-social": {
        "texte": "Réhabiliter le parc locatif existant avant d'envisager de nouvelles constructions, construire en offrant la possibilité aux locataires d'accéder à la propriété.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "logements-vacants": {
        "texte": "Créer une bourse d'échange de logements entre tous les bailleurs, privés et publics.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "acces-logement": {
        "texte": "Repenser la commission d'attribution des logements sociaux avec une charte d'attribution transparente et égalitaire, obliger les bailleurs à installer un gardien pour 100 logements.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # ÉDUCATION
    "petite-enfance": {
        "texte": "Augmenter le nombre de berceaux en aidant à la création de places en crèches par des subventions plutôt que de créer directement des crèches municipales.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "ecoles-renovation": {
        "texte": "Mener une campagne d'isolation et de rénovation de toutes les écoles pour réduire la consommation d'énergie, arborer les cours d'écoles avec ateliers jardinage.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "periscolaire-loisirs": {
        "texte": "Utiliser les salles d'école pour le soutien scolaire et l'aide à l'apprentissage des fondamentaux sous contrôle de professeurs volontaires rémunérés par la ville.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # jeunesse: EXISTE DÉJÀ
    # ENVIRONNEMENT
    # espaces-verts: EXISTE DÉJÀ
    "proprete-dechets": {
        "texte": "Nettoyer la ville avec de nouveaux outils connectés, plateforme de signalement des incivilit\u00e9s, construire une déchetterie éco-responsable avec tri sélectif et recyclage.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "climat-adaptation": {
        "texte": "Imposer pour chaque nouveau projet la prise en compte des enjeux écologiques : toitures végétalisées, récupérateurs d'eau, panneaux photovoltaïques, composteurs.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "renovation-energetique": {
        "texte": "Modification du PLU pour un plan d'obligation de rénovation harmonieuse des bâtiments, campagnes de sensibilisation aux enjeux écologiques.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "alimentation-durable": {
        "texte": "Arborer les cours d'écoles et mettre en place des ateliers jardinage pour les élèves, former les agents municipaux aux gestes écologiques.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # SANTÉ
    "centres-sante": {
        "texte": "Soutenir le maintien des deux cliniques existantes, favoriser l'installation de cabinets médicaux et paramédicaux, faciliter l'accès aux soins non programmés via une plateforme numérique.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "prevention-sante": {
        "texte": "Mettre en place une communauté professionnelle territoriale de santé (CPTS) pour favoriser la coordination des soins, rééquilibrer l'offre de soins sur toute la commune.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "seniors": {
        "texte": "Ouvrir un deuxième EHPAD dans le quartier du Plateau, mettre en place des représentations culturelles l'après-midi pour les séniors, développer la prise en charge du handicap.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # DÉMOCRATIE
    "budget-participatif": {
        "texte": "Création d'une maison de la démocratie pour accueillir partis politiques et associations, réorganisation des conseils de quartier avec présidence partagée entre élus et habitants.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "transparence": {
        "texte": "Repenser l'attribution des subventions aux associations en toute transparence, créer une commission d'attribution et contrôler chaque année les activités des associations.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "vie-associative": {
        "texte": "Instaurer une charte des associations, favoriser les associations ayant une action directe au bénéfice des habitants, les aider dans leurs recherches de nouveaux fonds.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "services-publics": {
        "texte": "Déployer les outils numériques de la smart-city pour faciliter l'accès à des services publics efficaces, avec une aide à l'appropriation de ces outils pour tous les habitants.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # ÉCONOMIE
    "commerce-local": {
        "texte": "Favoriser l'implantation d'activités économiques et commerciales dans les quartiers en manque de commerces, mettre à disposition une plateforme recensant les offres commerciales.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # emploi-insertion: EXISTE DÉJÀ
    "attractivite": {
        "texte": "Mener des actions pour attirer les entreprises et créer des emplois, aménager des salles pour événements privés, faciliter l'installation d'écoles privées, mettre en place des accès Internet gratuits.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # CULTURE
    "equipements-culturels": {
        "texte": "Redessiner l'axe palais des sports / Mac Val, créer un lieu culturel alternatif autour de Gare au Théâtre avec restauration, proposer un musée à ciel ouvert sur les berges de Seine.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "evenements-creation": {
        "texte": "Développer une politique culturelle élargie et pour tous publics, mettre en valeur le street-art, créer une maison d'échanges de maîtrises et de connaissances techniques.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # SPORT
    "equipements-sportifs": {
        "texte": "Ouvrir les stades en dehors des heures scolaires et pendant les vacances, aménager les bords de Seine pour clubs de sports nautiques, aménager le parc des Lilas pour le sport.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "sport-pour-tous": {
        "texte": "Favoriser l'émulation entre sportifs, organiser des événements inter-clubs ou inter-quartiers, aménager un parcours sportif en bord de Seine.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # URBANISME
    # amenagement-urbain: EXISTE DÉJÀ
    "accessibilite": {
        "texte": "Développer la prise en charge des personnes en situation de handicap, faciliter les moyens de déplacements (trottoirs adaptés, transports adaptés).",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "quartiers-prioritaires": {
        "texte": "Création de zones commerçantes dans les quartiers du Moulin Vert et Malassis pour redynamiser la vie de ces quartiers, restaurer la maison du Moulin Vert en espace de co-working.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    # SOLIDARITÉ
    "aide-sociale": {
        "texte": "Aides ciblées pour familles en difficulté, familles monoparentales, personnes isolées et jeunes : aide au logement, à la parentalité, au travail, à la santé, aux loisirs, au sport et à la culture.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "egalite-discriminations": {
        "texte": "Renforcer les actions de prévention, commission permanente pour suivre le quotidien des locataires avec les bailleurs, lutte contre l'isolement des personnes seules.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
    "pouvoir-achat": {
        "texte": "Stopper l'augmentation des impôts, développer le dynamisme économique pour générer des ressources propres, suivre les recommandations de la Chambre Régionale des Comptes.",
        "source": AFFLATET_SOURCE,
        "sourceUrl": AFFLATET_URL
    },
}

# ============================================================
# Application des propositions au JSON
# ============================================================

def set_proposition(data, candidat_id, sous_theme_id, proposition):
    """Insère une proposition pour un candidat dans un sous-thème."""
    for cat in data['categories']:
        for st in cat['sousThemes']:
            if st['id'] == sous_theme_id:
                if st['propositions'].get(candidat_id) is None:
                    st['propositions'][candidat_id] = proposition
                    return True
                else:
                    # Ne pas écraser une proposition existante
                    return False
    return False

# Compteurs
tmimi_added = 0
tmimi_skipped = 0
afflatet_added = 0
afflatet_skipped = 0

print("=" * 60)
print("INTÉGRATION DES PROGRAMMES - VITRY-SUR-SEINE")
print("=" * 60)

# 1. Tmimi
print("\n--- TMIMI (Hocine Tmimi) ---")
for st_id, prop in tmimi_props.items():
    result = set_proposition(data, 'tmimi', st_id, prop)
    if result:
        tmimi_added += 1
        print(f"  + {st_id}")
    else:
        tmimi_skipped += 1
        print(f"  ~ {st_id} (déjà rempli, ignoré)")

print(f"\nTmimi: {tmimi_added} ajoutées, {tmimi_skipped} ignorées (existantes)")

# 2. Afflatet
print("\n--- AFFLATET (Alain Afflatet) ---")
for st_id, prop in afflatet_props.items():
    result = set_proposition(data, 'afflatet', st_id, prop)
    if result:
        afflatet_added += 1
        print(f"  + {st_id}")
    else:
        afflatet_skipped += 1
        print(f"  ~ {st_id} (déjà rempli, ignoré)")

print(f"\nAfflatet: {afflatet_added} ajoutées, {afflatet_skipped} ignorées (existantes)")

# ============================================================
# Mise à jour des métadonnées des candidats
# ============================================================

for candidat in data['candidats']:
    if candidat['id'] == 'tmimi':
        # Compter les propositions de Tmimi
        count = 0
        for cat in data['categories']:
            for st in cat['sousThemes']:
                if st['propositions'].get('tmimi') is not None:
                    count += 1
        candidat['programmeComplet'] = count >= 15
        candidat['programmePdfPath'] = "tmimi-programme-vitry2026.pdf"
        print(f"\nTmimi: {count} propositions au total, programmeComplet={candidat['programmeComplet']}")

    elif candidat['id'] == 'afflatet':
        # Compter les propositions d'Afflatet
        count = 0
        for cat in data['categories']:
            for st in cat['sousThemes']:
                if st['propositions'].get('afflatet') is not None:
                    count += 1
        candidat['programmeComplet'] = count >= 15
        candidat['programmePdfPath'] = "afflatet-programme-vitryavenir.pdf"
        print(f"Afflatet: {count} propositions au total, programmeComplet={candidat['programmeComplet']}")

# ============================================================
# Sauvegarde
# ============================================================

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nFichier sauvegardé: {JSON_PATH}")
print("=" * 60)
print("INTÉGRATION TERMINÉE")
print("=" * 60)
