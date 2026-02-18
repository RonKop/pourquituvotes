#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du programme complet de Frédéric Marquet (Mulhouse) - ~330 mesures
Source : https://marquet2026.fr/programme-frederic-marquet/
Programme structuré en 3 axes : Bien vivre, S'épanouir, Vibrer
+ Mairie plus proche, plus performante
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "elections")
JSON_PATH = os.path.join(DATA_DIR, "mulhouse-2026.json")

CANDIDAT_ID = "marquet"
SOURCE = "Programme officiel 2026"
SOURCE_URL = "https://marquet2026.fr/programme-frederic-marquet/"

# Metadata updates
METADATA = {
    "programmeComplet": True,
    "programmeUrl": "https://marquet2026.fr/programme-frederic-marquet/",
    "programmePdfPath": None,
}

# =============================================================================
# Propositions mapped to sub-themes (category_id -> sub_theme_id -> texte)
# ~330 mesures regroupées par sous-thème
# =============================================================================

PROPOSITIONS = {
    "securite": {
        "police-municipale": (
            "Recruter 25 agents supplémentaires pour une police municipale opérationnelle 24h/24. "
            "Assurer une intervention en 2 à 10 minutes sur toute la ville. "
            "Rééclairer la ville le soir et la nuit. "
            "Installer une brigade montée à cheval (modèle Cannes). "
            "Mettre en place des gardiens de square reliés à la police. "
            "Obtenir des renforts d'effectifs avec l'État. "
            "Favoriser la synergie avec Police nationale et Justice."
        ),
        "prevention-mediation": (
            "Lutter contre les incivilités avec tolérance zéro. "
            "Créer un dispositif de parents-relais dans les quartiers (modèle Orléans). "
            "Développer les travaux d'intérêt général pour réparer les dégradations. "
            "Déployer un plan global de prévention contre les stupéfiants et les incivilités."
        ),
        "violences-femmes": (
            "Déployer un plan global de prévention des violences intrafamiliales. "
            "Prévoir des logements pour isoler le conjoint violent."
        ),
    },
    "transports": {
        "transports-en-commun": (
            "Augmenter la fréquence des bus et tram en soirée (un tram toutes les 20 minutes). "
            "Accélérer l'étude des extensions du tram. "
            "Relancer le projet de liaison ferroviaire directe avec l'aéroport. "
            "Mettre en place une navette fluviale électrique. "
            "Étudier l'opportunité d'un téléphérique urbain. "
            "Soutenir les liaisons ferroviaires vers l'Allemagne et la Suisse, adaptées aux travailleurs et étudiants transfrontaliers."
        ),
        "velo-mobilites-douces": (
            "Faciliter l'usage du vélo en sécurisant les itinéraires, notamment vers les écoles. "
            "Créer une zone « pied à terre » pour vélos et trottinettes en centre-ville (10h-20h)."
        ),
        "pietons-circulation": (
            "Adapter le plan de circulation à la vie réelle. "
            "Étudier la réintroduction d'une voie de circulation sur l'axe Briand-Franklin. "
            "Mieux entretenir la voirie dans tous les quartiers. "
            "Piétonniser des rues avec bon sens pour améliorer la vie des habitants et des commerces. "
            "Fermer temporairement certaines rues à la circulation le dimanche pour créer de grands ensembles piétons."
        ),
        "stationnement": (
            "Développer l'offre de stationnement en pourtour de la zone piétonne. "
            "Rendre gratuite la 2ème heure de stationnement pour dynamiser le commerce."
        ),
        "tarifs-gratuite": (
            "Maintenir la gratuité des transports pour les seniors. "
            "Étendre la gratuité des transports aux jeunes."
        ),
    },
    "logement": {
        "logement-social": (
            "Travailler en synergie avec les bailleurs sociaux pour assurer la qualité des logements. "
            "Assurer l'entretien et la sécurité des logements sociaux. "
            "Donner la parole aux habitants des grands ensembles et les associer aux décisions sur leur quartier."
        ),
        "logements-vacants": (
            "Rénover les bâtiments anciens et réinvestir les friches industrielles. "
            "Combattre l'habitat indigne dans toute la ville. "
            "Accélérer la reconversion des friches pour créer de nouveaux espaces de vie."
        ),
        "acces-logement": (
            "Favoriser le logement étudiant. "
            "Aider les copropriétés au patrimoine remarquable à rénover."
        ),
    },
    "education": {
        "ecoles-renovation": (
            "Accélérer la rénovation et la modernisation des écoles. "
            "Végétaliser les écoles. "
            "Sécuriser tous les accès aux établissements scolaires avec une présence renforcée d'adultes aux heures d'entrée/sortie. "
            "Réguler la circulation devant les écoles. "
            "Garantir à chaque élève le matériel scolaire nécessaire. "
            "Créer un « KM0 de l'éducation » (lieu de ressources pédagogiques). "
            "Développer les « savoir être » : respect, entraide, ouverture. "
            "Soutenir les projets innovants des enseignants."
        ),
        "cantines-fournitures": (
            "Optimiser l'approvisionnement des restaurants scolaires en circuit court. "
            "Faire du bien-manger une philosophie partagée et développer des passerelles pédagogiques entre cuisine et enseignement."
        ),
        "jeunesse": (
            "Développer au moins deux nouvelles filières d'études supérieures. "
            "Lancer un plan « Vie étudiante » et favoriser la poursuite d'études à Mulhouse. "
            "Relier universités, écoles et entreprises par un programme « Innovation et emploi ». "
            "Étendre le parcours SIM aux décrocheurs scolaires dans tous les collèges. "
            "Soutenir les CFA, l'AFPA et les centres de formation dans leurs projets de développement. "
            "Proposer des chantiers-écoles pour apprendre en rénovant la ville. "
            "Formaliser les échanges avec le conseil des jeunes. "
            "Attirer les étudiants en ville et faciliter l'accès aux transports pour étudiants."
        ),
    },
    "environnement": {
        "espaces-verts": (
            "Végétaliser le plus possible les rues et verdir les rues dans tous les quartiers. "
            "Valoriser le parc de la Bourse et en faire un parc majeur sur le cheminement gare-plateau piéton. "
            "Dessiner une allée-promenade verte piétonne Salvator-Fonderie. "
            "Recréer un parc entre Mairie et Bains municipaux (rue Pierre et Marie Curie). "
            "Créer des espaces publics de quiétude calmes et ombragés dans tous les quartiers. "
            "Planter des arbres fruitiers en libre accès dans parcs et espaces publics. "
            "Soutenir les potagers urbains, la permaculture et les fermes innovantes. "
            "Faire réapparaître l'eau dans la ville (canaux, fontaines). "
            "Remettre de l'eau dans l'ensemble des parcs. "
            "Créer un parcours d'éveil dans un parc. "
            "Mener des actions pour le bien-être animal."
        ),
        "proprete-dechets": (
            "Refaire de la propreté un essentiel dans tous les quartiers. "
            "Augmenter les équipes de terrain pour le nettoyage et mieux soutenir les agents municipaux de propreté (moyens et reconnaissance). "
            "Mettre en place une collecte des encombrants sur rendez-vous. "
            "Remplacer les corbeilles de déchets par des corbeilles de tri. "
            "Faire de Mulhouse la première ville sans bouteilles plastiques en 10 ans."
        ),
        "climat-adaptation": (
            "Intégrer rivières et canaux dans la transformation urbaine. "
            "Créer des espaces de baignade. "
            "Développer le port urbain. "
            "Transformer la ville en « ville d'eau » à l'horizon 2040. "
            "Porter un axe de développement stratégique autour de l'eau."
        ),
        "renovation-energetique": (
            "Accélérer le déploiement des solutions énergétiques nouvelles. "
            "Rénover les bâtiments anciens pour améliorer leur performance énergétique."
        ),
        "alimentation-durable": (
            "Protéger la qualité de l'eau du robinet. "
            "Expérimenter la sécurité sociale de l'alimentation (modèle Strasbourg). "
            "Cultiver une ceinture nourricière autour de la ville et réserver des terrains à l'agriculture."
        ),
    },
    "sante": {
        "centres-sante": (
            "Doubler le nombre de médecins en 10 ans avec aide à l'installation. "
            "Accompagner l'installation de la 1ère promotion UHA d'étudiants en médecine à Mulhouse. "
            "Créer un pôle d'innovation en santé numérique et neuroscience. "
            "Assurer un accueil adapté pour tous (personnes âgées, mobilité réduite). "
            "Renforcer l'offre de soins pour les plus fragiles. "
            "Garantir une fin de vie digne avec soins palliatifs. "
            "Proposer la formation « Médecin maître de stage » à Mulhouse."
        ),
        "prevention-sante": (
            "Déployer un plan local de santé mentale. "
            "Intensifier les campagnes de prévention (nutrition, activité physique, addictions, maladies chroniques). "
            "Développer un plan « Mulhouse Sport Santé 2040 » et encourager la pratique sportive à tout âge."
        ),
        "seniors": (
            "Recréer un conseil des anciens. "
            "Mettre en place un parrainage seniors/étudiants. "
            "Développer les échanges entre écoles et maisons de retraite. "
            "Faciliter les accès aux lieux de quiétude pour personnes à mobilité réduite."
        ),
    },
    "democratie": {
        "budget-participatif": (
            "Coconstruire les décisions avec les habitants. "
            "Réinstaller les « conseils de quartiers ». "
            "Assurer une permanence mensuelle du Maire accessible sans rendez-vous. "
            "Désigner pour chaque quartier un adjoint référent. "
            "Organiser chaque mois une réunion publique dans un quartier différent."
        ),
        "transparence": (
            "Réaliser un audit complet des finances municipales et le rendre public. "
            "Stabiliser les impôts locaux et réaliser des économies. "
            "Mettre en place une équipe spécialisée dans la recherche de subventions (État, Europe, Fondations). "
            "Créer un fonds « Innovation Mulhouse 2050 » pour financer les grands projets, alimenté par la Ville, la M2A, la Région, l'État et des partenaires privés sous contrôle. "
            "Mettre en place un « Indice du Bonheur mulhousien » mesurant régulièrement le bien-être, la santé, la cohésion sociale, l'accès à la culture, le niveau de confiance et le sentiment de sécurité, publié chaque année le 20 mars."
        ),
        "vie-associative": (
            "Soumettre une charte municipale des valeurs républicaines aux associations. "
            "Soutenir les associations et collectifs mulhousiens. "
            "Encourager le dialogue interreligieux et créer un forum consultatif des cultes et de la fraternité."
        ),
        "services-publics": (
            "Créer des mairies de quartiers. "
            "Simplifier, accélérer et humaniser les démarches administratives. "
            "Créer une plateforme numérique unique et un portail unique pour les démarches. "
            "Proposer les documents administratifs en plusieurs langues (anglais, allemand, italien, espagnol, arabe, turc, portugais). "
            "Ajuster l'action publique sur résultats concrets."
        ),
    },
    "economie": {
        "commerce-local": (
            "Lancer la « Mission Commerce Mulhouse » avec une stratégie opérationnelle. "
            "Dédier des équipes au commerce du centre-ville, des quartiers et des marchés. "
            "Soutenir le marché de Mulhouse et élaborer un projet avec les commerçants du marché. "
            "Créer une halle gourmande des cuisines du monde dans un lieu central. "
            "Soutenir les initiatives culinaires d'insertion et créant du lien social. "
            "Redonner vie au Réfectoire de DMC avec un projet culinaire et culturel."
        ),
        "emploi-insertion": (
            "Recruter un Manager de l'Industrie. "
            "Accélérer la reconversion des friches industrielles. "
            "Mettre en place une équipe dédiée à l'implantation et au développement des entreprises. "
            "Coordonner avec la CCI et l'ADIRA. "
            "Faciliter les démarches administratives des entrepreneurs. "
            "Proposer un programme commun d'emploi transfrontalier avec Bâle et Freiburg."
        ),
        "attractivite": (
            "Créer un Conseil créatif pour l'économie et associer les acteurs économiques à la décision municipale. "
            "Bâtir une vision stratégique novatrice pour l'attractivité de Mulhouse. "
            "Engager un plan « Image et attractivité ». "
            "Ouvrir une boutique-accueil Office du Tourisme place de la Réunion. "
            "Déterminer une stratégie d'agglomération avec des objectifs chiffrés. "
            "Renforcer les relations avec la Région et la Collectivité européenne d'Alsace. "
            "Mettre en œuvre une stratégie partagée de rayonnement sur le Rhin supérieur. "
            "Se positionner pour accueillir des équipements et fonctions départementales."
        ),
    },
    "culture": {
        "equipements-culturels": (
            "Équiper Mulhouse d'une médiathèque nouvelle génération dans un bâtiment central, "
            "ouverte le week-end, avec espace de coworking, café, salle de projection. "
            "Rendre l'entrée des musées gratuite pour les Mulhousiens. "
            "Offrir le Pass Musée à chaque famille d'enfant en maternelle et en primaire. "
            "Soutenir la modernisation des musées et des parcours de visite. "
            "Étudier la création d'un grand musée national de l'histoire industrielle. "
            "Devenir capitale européenne des arts visuels et de l'image. "
            "Étendre MOTOCO avec un pôle des arts visuels et scéniques. "
            "Attirer l'industrie de l'audiovisuel sur le site DMC. "
            "Étudier les possibilités pour le Noumatrouff. "
            "Doter Mulhouse d'un Zénith modulable de 2 000 à 8 000 places, financé à 60 % par partenaires extérieurs."
        ),
        "evenements-creation": (
            "Créer un kiosque place de la Réunion avec billetterie pour valoriser l'offre culturelle. "
            "Proposer un concert chaque vendredi soir (juin à septembre) et un grand concert annuel place de la Réunion. "
            "Soutenir et valoriser les artistes locaux. "
            "Organiser un grand marché des créateurs et artisans locaux et du monde, dans les rues du centre-ville tout l'été. "
            "Lancer une biennale de la photographie industrielle et manufacturière. "
            "Créer des lieux de cinéma en plein air tout l'été. "
            "Faire de Mulhouse « ville de la fête » avec événements et festivals de quartier, animations saisonnières. "
            "Proposer chaque été une grande fête dans un quartier différent. "
            "Relancer le Festival Automobile en y ajoutant cuisines et musiques du monde. "
            "Illuminer les espaces publics et moderniser les infrastructures du port. "
            "Installer une péniche bar-restaurant. "
            "Valoriser l'histoire et l'identité de Mulhouse, mettre à l'honneur les Mulhousiens célèbres. "
            "Ouvrir une annexe de la « maison de l'Alsace » et promouvoir la culture alsacienne. "
            "Soutenir les sections bilingues et les échanges scolaires internationaux."
        ),
    },
    "sport": {
        "equipements-sportifs": (
            "Augmenter de 50 % le budget Sport avec des objectifs clairs, une gestion transparente et un contrôle de l'utilisation. "
            "Monter un « village multi-sports » pour l'été 2026 avec terrains et écran géant pour les grands événements sportifs. "
            "Doter Mulhouse d'un Zénith modulable pouvant accueillir des événements sportifs. "
            "Ouvrir davantage les équipements sportifs en soirée, le week-end et pendant les vacances scolaires. "
            "Lancer un concours pour réhabiliter les Bains municipaux en conservant la dimension piscine."
        ),
        "sport-pour-tous": (
            "Proposer un abonnement commun pour les événements sportifs mulhousiens. "
            "Renforcer les liens entre clubs d'élite et associations de quartier. "
            "Développer un plan « Mulhouse Sport Santé 2040 » et encourager la pratique sportive à tout âge. "
            "Créer un club des partenaires de l'agglomération pour faciliter la recherche de financements. "
            "Soutenir le sport de haut niveau et s'engager pour que le football retrouve le plus haut niveau. "
            "Valoriser le sport comme vecteur d'image et renforcer la fierté d'appartenance."
        ),
    },
    "urbanisme": {
        "amenagement-urbain": (
            "Protéger l'identité patrimoniale bâtie et la richesse naturelle des quartiers. "
            "Redonner toute sa dimension à la Tour de l'Europe et en faire un symbole vivant de la ville. "
            "Faire se croiser les énergies créatives (Motoco et KM0). "
            "Développer les voies fluviales et le port urbain. "
            "Redynamiser les relations avec les villes jumelées et fixer des programmes communs (culture, sport, économie). "
            "Faire réapparaître l'eau dans la ville (canaux, fontaines) et transformer Mulhouse en « ville d'eau » à l'horizon 2040."
        ),
        "accessibilite": (
            "Faciliter les accès aux lieux de quiétude pour personnes à mobilité réduite. "
            "Assurer un accueil adapté pour tous, personnes âgées et mobilité réduite."
        ),
        "quartiers-prioritaires": (
            "Créer des espaces publics de quiétude calmes et ombragés dans tous les quartiers. "
            "Soutenir les échanges entre écoles des différents quartiers. "
            "Développer les projets autour de l'image dans tous les quartiers."
        ),
    },
    "solidarite": {
        "aide-sociale": (
            "Coordonner l'action de tous les acteurs sociaux. "
            "Renforcer l'apprentissage du français. "
            "Soumettre une charte municipale des valeurs républicaines aux nouveaux habitants. "
            "Garantir la laïcité. "
            "Mettre en place un pôle d'innovation juridique pour la protection des droits de l'homme."
        ),
        "egalite-discriminations": (
            "Encourager le dialogue interreligieux. "
            "Créer un forum consultatif des cultes et de la fraternité. "
            "Soutenir les échanges entre écoles des différents quartiers. "
            "Valoriser l'apprentissage des langues étrangères et soutenir les sections bilingues."
        ),
        "pouvoir-achat": (
            "Créer un Office du Pouvoir d'Achat permettant aux habitants de bénéficier de tarifs réduits "
            "et offrant des conseils en gestion de budget. "
            "Tendre à la gratuité de l'eau pour consommation vitale : instaurer une première tranche gratuite, "
            "puis progressivement étendre la gratuité pour tous (objectif 10 m³/an/personne gratuits). "
            "Alléger la charge des contribuables en stabilisant les impôts locaux."
        ),
    },
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update candidate metadata
    for candidat in data["candidats"]:
        if candidat["id"] == CANDIDAT_ID:
            for key, value in METADATA.items():
                candidat[key] = value
            print(f"Metadata updated: programmeComplet={candidat['programmeComplet']}")
            break
    else:
        print(f"ERROR: Candidat {CANDIDAT_ID} not found!")
        return

    # Insert/update proposals
    count_updated = 0
    count_new = 0
    count_errors = 0

    for cat in data["categories"]:
        cat_id = cat["id"]
        if cat_id not in PROPOSITIONS:
            continue
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id not in PROPOSITIONS[cat_id]:
                continue
            texte = PROPOSITIONS[cat_id][st_id]
            existing = st["propositions"].get(CANDIDAT_ID)
            if existing is not None:
                count_updated += 1
                action = "UPDATED"
            else:
                count_new += 1
                action = "NEW"
            st["propositions"][CANDIDAT_ID] = {
                "texte": texte,
                "source": SOURCE,
                "sourceUrl": SOURCE_URL
            }
            print(f"  [{action}] {cat_id}/{st_id}")

    # Verify all proposed sub-themes were found
    for cat_id, subs in PROPOSITIONS.items():
        for st_id in subs:
            found = False
            for cat in data["categories"]:
                if cat["id"] == cat_id:
                    for st in cat["sousThemes"]:
                        if st["id"] == st_id:
                            found = True
                            break
            if not found:
                print(f"  ERROR: Sub-theme {cat_id}/{st_id} not found in JSON!")
                count_errors += 1

    # Write back
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Updated: {count_updated}, New: {count_new}, Errors: {count_errors}")
    total = count_updated + count_new
    print(f"Total sub-themes with Marquet proposals: {total}")

    # Summary of coverage
    all_st = set()
    for cat_id, subs in PROPOSITIONS.items():
        for st_id in subs:
            all_st.add(f"{cat_id}/{st_id}")
    print(f"\nCoverage: {len(all_st)} sub-themes covered across {len(PROPOSITIONS)} categories")
    print("Categories covered:", ", ".join(sorted(PROPOSITIONS.keys())))


if __name__ == "__main__":
    main()
