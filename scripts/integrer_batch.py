#!/usr/bin/env python3
"""Intègre en batch les propositions extraites par les agents d'exploration."""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELECTIONS = os.path.join(BASE, "data", "elections")

def update_city(filename, updates):
    """
    updates = {
        "candidat_id": {
            "programmeUrl": "...",
            "programmeComplet": True/False,
            "propositions": {
                "sous-theme-id": {"texte": "...", "source": "...", "sourceUrl": "..."},
                ...
            }
        }
    }
    """
    filepath = os.path.join(ELECTIONS, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for cand_id, cand_updates in updates.items():
        # Update candidat metadata
        for c in data["candidats"]:
            if c["id"] == cand_id:
                if "programmeUrl" in cand_updates:
                    c["programmeUrl"] = cand_updates["programmeUrl"]
                if "programmeComplet" in cand_updates:
                    c["programmeComplet"] = cand_updates["programmeComplet"]
                break
        else:
            print(f"  ERREUR: candidat {cand_id} non trouvé dans {filename}")
            continue

        # Update propositions
        props = cand_updates.get("propositions", {})
        count = 0
        for cat in data["categories"]:
            for st in cat["sousThemes"]:
                if st["id"] in props:
                    st["propositions"][cand_id] = props[st["id"]]
                    count += 1
        print(f"  {cand_id}: {count} propositions intégrées")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> {filename} sauvegardé")


# =============================================================================
# 1. VITRY-SUR-SEINE : Bell-Lloch (13) + Tmimi (22)
# =============================================================================
print("\n=== VITRY-SUR-SEINE ===")
update_city("vitry-sur-seine-2026.json", {
    "bell-lloch": {
        "programmeUrl": "https://pbl2026.fr/programme.html",
        "programmeComplet": False,
        "propositions": {
            "amenagement-urbain": {"texte": "Nouveau cœur de ville : 5 600 m² d'espaces verts, nouveaux commerces, terrasses, cinés Robespierre revisités et parking souterrain rénové", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "logement-social": {"texte": "Construction de 2 000 logements tout en préservant les zones pavillonnaires, avec des logements sociaux rénovés", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "prevention-mediation": {"texte": "Création d'une équipe de médiateurs de proximité urbaine et développement concerté de la vidéoverbalisation", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "espaces-verts": {"texte": "Création d'un grand parc en bord de Seine d'au moins 50 000 m² pour réconcilier la ville avec son fleuve", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "equipements-culturels": {"texte": "Construction d'un complexe festif moderne pour les familles, mariages, anniversaires et rencontres citoyennes", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "seniors": {"texte": "Construction d'une nouvelle résidence sénior adaptée aux besoins et au confort des aînés", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "proprete-dechets": {"texte": "Création d'une déchetterie-ressourcerie, vidéoverbalisation et mobilisation citoyenne pour une ville plus propre", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "vie-associative": {"texte": "Réouverture de la maison sociale du Moulin Vert et ouverture de deux nouvelles salles municipales associatives", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "emploi-insertion": {"texte": "Création d'une régie publique de quartier pour l'insertion professionnelle et préparation de 1 000 emplois", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "periscolaire-loisirs": {"texte": "Étude de la possibilité de rendre gratuite l'heure d'étude scolaire après la classe", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "commerce-local": {"texte": "Création d'un nouveau marché au quartier Jean Jaurès avec produits issus de circuits courts à tarifs abordables", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "renovation-energetique": {"texte": "Ouverture d'un site de géothermie pour chauffer les habitations et faire baisser les factures d'énergie", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
            "evenements-creation": {"texte": "Rendre l'accès à la culture totalement gratuit pour tous les jeunes Vitriots de moins de 26 ans", "source": "pbl2026.fr", "sourceUrl": "https://pbl2026.fr/programme.html"},
        }
    },
    "tmimi": {
        "programmeUrl": "https://vitry2026.fr/",
        "programmeComplet": False,
        "propositions": {
            "climat-adaptation": {"texte": "Déminéraliser les sols, isoler le bâti et blanchir les surfaces pour Vitry zéro carbone en 2050", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "espaces-verts": {"texte": "Planter des milliers d'arbres, créer des îlots de fraîcheur, jardins partagés et vergers urbains", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "proprete-dechets": {"texte": "Campagne pour la réduction des déchets, développer recycleries, circuits courts, ateliers de réparation", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "transports-en-commun": {"texte": "Interdire la circulation des poids lourds en ville, création d'une navette interquartier gratuite", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "velo-mobilites-douces": {"texte": "Plan vélo ambitieux, promotion de la marche, partage de l'espace public", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "logement-social": {"texte": "Maintenir un taux minimum de 40% de logements sociaux, investir dans la rénovation du parc existant", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "encadrement-loyers": {"texte": "Encadrer les loyers, soutenir l'habitat coopératif et social", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "renovation-energetique": {"texte": "Rénovation énergétique prioritaire, améliorer la performance du parc de logements", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "budget-participatif": {"texte": "Budgets participatifs, référendums locaux, conseils de quartier indépendants dotés de pouvoir", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "transparence": {"texte": "Charte éthique pour chaque élu, combattre le clientélisme, supprimer les avantages indus des élus", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "services-publics": {"texte": "Service public communal en régies publiques : eau, énergie, santé, propreté, transport, restauration scolaire", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "petite-enfance": {"texte": "Ville à hauteur d'enfant : crèches accessibles, cantines bio et locales progressivement gratuites", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "cantines-fournitures": {"texte": "Cantines de plus en plus bio et locales, avec options végétariennes", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "jeunesse": {"texte": "Appui réel aux adolescents : orientation, stages, apprentissage, emploi, logement, mobilité", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "prevention-sante": {"texte": "Ouverture d'un deuxième CMPP pour la santé mentale des jeunes", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "seniors": {"texte": "Maintien à domicile, solutions intergénérationnelles, ouverture d'un deuxième EHPAD", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "centres-sante": {"texte": "Renforcer le Centre municipal de santé et ouvrir des antennes de proximité", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "vie-associative": {"texte": "Égalité de traitement et transparence dans l'attribution des salles et subventions aux associations", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "egalite-discriminations": {"texte": "Observatoire local des discriminations et violences sexistes, lutte contre racisme, sexisme, LGBTQIphobies", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "amenagement-urbain": {"texte": "Quartier des Ardoines : quartier écologique au service des habitants, outil foncier solidaire", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "pietons-circulation": {"texte": "Créer des lieux de rencontre, placettes, rues piétonnes, espaces publics vivants", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
            "alimentation-durable": {"texte": "Jardins partagés, vergers urbains, agriculture urbaine, circuits courts", "source": "vitry2026.fr", "sourceUrl": "https://vitry2026.fr/"},
        }
    }
})

# =============================================================================
# 2. ÉVRY-COURCOURONNES : Amrani (10)
# =============================================================================
print("\n=== ÉVRY-COURCOURONNES ===")
update_city("evry-courcouronnes-2026.json", {
    "amrani": {
        "programmeUrl": "https://faridaamrani2026.fr/",
        "programmeComplet": False,
        "propositions": {
            "proprete-dechets": {"texte": "Grand plan propreté et dératisation", "source": "faridaamrani2026.fr", "sourceUrl": "https://faridaamrani2026.fr/"},
            "encadrement-loyers": {"texte": "Mise en place de l'encadrement des loyers", "source": "faridaamrani2026.fr", "sourceUrl": "https://faridaamrani2026.fr/"},
            "logement-social": {"texte": "Convocation des bailleurs sociaux : audit, charges, propreté et entretien", "source": "faridaamrani2026.fr", "sourceUrl": "https://faridaamrani2026.fr/"},
            "cantines-fournitures": {"texte": "Gratuité de la cantine scolaire", "source": "faridaamrani2026.fr", "sourceUrl": "https://faridaamrani2026.fr/"},
            "prevention-mediation": {"texte": "Déploiement d'un plan tranquillité publique avec médiateurs", "source": "faridaamrani2026.fr", "sourceUrl": "https://faridaamrani2026.fr/"},
            "tarifs-gratuite": {"texte": "Remboursement du Pass Navigo pour les moins de 26 ans", "source": "faridaamrani2026.fr", "sourceUrl": "https://faridaamrani2026.fr/"},
            "prevention-sante": {"texte": "Plan d'action pour la santé mentale des jeunes", "source": "faridaamrani2026.fr", "sourceUrl": "https://faridaamrani2026.fr/"},
            "services-publics": {"texte": "Restructuration de toutes les Maisons de Quartier", "source": "faridaamrani2026.fr", "sourceUrl": "https://faridaamrani2026.fr/"},
            "transparence": {"texte": "Référendums locaux pour tous les projets structurants", "source": "faridaamrani2026.fr", "sourceUrl": "https://faridaamrani2026.fr/"},
            "vie-associative": {"texte": "Création d'une maison des associations", "source": "faridaamrani2026.fr", "sourceUrl": "https://faridaamrani2026.fr/"},
        }
    }
})

# =============================================================================
# 3. ISSY-LES-MOULINEAUX : Morel (21)
# =============================================================================
print("\n=== ISSY-LES-MOULINEAUX ===")
update_city("issy-les-moulineaux-2026.json", {
    "morel": {
        "programmeUrl": "https://issyecoloetsocial.fr/notre-programme/",
        "programmeComplet": True,
        "propositions": {
            "pietons-circulation": {"texte": "Le permis de piétonniser : dispositif permettant aux habitants de transformer temporairement leur rue en zone piétonne", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "vie-associative": {"texte": "Contrats d'objectifs pluriannuels, mise à disposition de locaux et transparence totale des subventions pour les associations", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "budget-participatif": {"texte": "Transformation des conseils de quartier en 6 véritables conseils citoyens indépendants, décentralisés, dotés de moyens propres", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "violences-femmes": {"texte": "Plan global de prévention contre les violences intrafamiliales et les discriminations", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "egalite-discriminations": {"texte": "Politique de promotion de l'égalité des droits et lutte contre toutes les discriminations : sexisme, racisme, antisémitisme, LGBTQIphobies", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "services-publics": {"texte": "Remunicipalisation des services essentiels (eau, équipements sportifs, culturels) à la fin des délégations de service public", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "transparence": {"texte": "Droit de saisine citoyenne et référendums locaux sur les sujets structurants", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "renovation-energetique": {"texte": "Neutralité carbone avant 2050 : massification de la rénovation énergétique, priorité aux passoires thermiques", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "velo-mobilites-douces": {"texte": "Réseau cyclable sécurisé et continu connecté aux villes voisines, stationnements vélos suffisants, trottoirs élargis", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "espaces-verts": {"texte": "2 000 arbres plantés par an, atlas de la biodiversité communale, désimperméabilisation et végétalisation massives", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "alimentation-durable": {"texte": "Cantines scolaires : généralisation des circuits courts et produits bios, commerces bio accessibles dans tous les quartiers", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "proprete-dechets": {"texte": "Objectif zéro plastique à usage unique d'ici 2040, tarification incitative au poids des déchets", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "logement-social": {"texte": "Plafonnement des loyers, lutte contre logements vacants, limitation locations touristiques, logements très sociaux pour mères isolées", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "logements-vacants": {"texte": "Transformation de bureaux vides en logements, Bail Réel Solidaire (BRS) pour accession à prix maîtrisé", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "aide-sociale": {"texte": "Bus des solidarités : dispositif mobile pour informer sur les droits sociaux et accompagner les démarches administratives", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "commerce-local": {"texte": "Soutien aux commerces indépendants, artisanat et ESS, maîtrise foncière pour préserver l'économie de proximité", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "pouvoir-achat": {"texte": "Plan municipal dédié aux familles monoparentales et mères isolées : logement, garde d'enfants, accès aux droits", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "evenements-creation": {"texte": "Berges de Seine animées par guinguettes, fête de la Seine, site de baignade, musiques actuelles et comédie musicale", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "centres-sante": {"texte": "Création d'un Centre municipal de santé regroupant des soignants spécialistes, droit au non-numérique", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "sport-pour-tous": {"texte": "Chaque enfant isséen doit pouvoir partir au moins une fois en classe de découverte, accès facilité au sport", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
            "ecoles-renovation": {"texte": "Rues aux écoles : fermeture de la circulation aux abords des écoles aux heures d'entrée et sortie", "source": "issyecoloetsocial.fr", "sourceUrl": "https://issyecoloetsocial.fr/notre-programme/"},
        }
    }
})

# =============================================================================
# 4. ANNECY : Armand (25) + Roit-Lévêque (21)
# =============================================================================
print("\n=== ANNECY ===")
update_city("annecy-2026.json", {
    "armand": {
        "programmeUrl": "https://acteursannecy.fr/programme",
        "programmeComplet": True,
        "propositions": {
            "police-municipale": {"texte": "Police municipale présente jusqu'à 4h du matin en été, renforcement zones sensibles, présence dans les bus après 22h", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "videoprotection": {"texte": "Installation de 100 nouvelles caméras d'ici la fin du mandat, conservation des images portée à 30 jours", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "prevention-mediation": {"texte": "Nettoyage quotidien centre-ville et 3x/semaine dans les quartiers, intervention sous 24h pour tags et dépôts sauvages", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "logement-social": {"texte": "Construction de 500 logements sociaux par an avec mixité sociale dans tous les quartiers", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "renovation-energetique": {"texte": "Aide majorée pour la rénovation énergétique des logements, accompagnement technique et financier des propriétaires", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "velo-mobilites-douces": {"texte": "50 km de pistes cyclables sécurisées d'ici la fin du mandat, priorité aux axes domicile-travail", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "stationnement": {"texte": "Durée maximale portée à 3h en zone rouge, création de parkings relais aux entrées de ville", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "climat-adaptation": {"texte": "Transition énergétique des bâtiments publics et développement des mobilités douces", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "commerce-local": {"texte": "Stationnement facilité, animations commerciales, lutte contre la vacance commerciale et accompagnement artisans locaux", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "services-publics": {"texte": "Carte citoyen unique pour tous les services municipaux (piscines, médiathèques, sport) avec tarification solidaire", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "equipements-culturels": {"texte": "Culture accessible à tous, soutien aux associations culturelles et programmation diversifiée", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "budget-participatif": {"texte": "100% de réponses aux avis Agate, budgets participatifs et concertation systématique sur les grands projets", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "transparence": {"texte": "Tableau de bord public, bilans réguliers et gel de toute augmentation d'impôt pendant le mandat", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "jeunesse": {"texte": "Espaces dédiés, soutien aux initiatives jeunesse, partenariats avec entreprises locales pour l'insertion", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "petite-enfance": {"texte": "Augmentation des places en crèche, soutien aux assistantes maternelles et tarification solidaire", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "espaces-verts": {"texte": "Zones de biodiversité préservées, plan de végétalisation urbaine et protection renforcée du lac d'Annecy", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "proprete-dechets": {"texte": "Renfort de 10-15% des équipes en été, doublement collecte en zones touristiques, compostage et recyclage", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "aide-sociale": {"texte": "Plan d'action dès les 100 premiers jours pour les personnes à la rue, maraudes renforcées et hébergement d'urgence", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "emploi-insertion": {"texte": "Attractivité économique, soutien aux entreprises innovantes, stratégie 'Territoire intelligent' et soutien aux startups", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "vie-associative": {"texte": "Subventions augmentées de 20% sur le mandat, guichet unique pour les associations et simplification des démarches", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "equipements-sportifs": {"texte": "Plan de rénovation des équipements sportifs, priorité aux vestiaires et installations vieillissantes", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "sport-pour-tous": {"texte": "Accès facilité aux équipements, créneaux horaires élargis et soutien renforcé aux associations sportives", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "ecoles-renovation": {"texte": "10 écoles rénovées d'ici la fin du mandat, isolation thermique et végétalisation des cours", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "periscolaire-loisirs": {"texte": "Activités périscolaires gratuites pour tous avec éducation artistique et culturelle garantie", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
            "accessibilite": {"texte": "Mise aux normes progressive de tous les équipements publics et accessibilité numérique des services", "source": "acteursannecy.fr", "sourceUrl": "https://acteursannecy.fr/programme"},
        }
    },
    "roit-leveque": {
        "programmeUrl": "https://retrouvons-annecy.fr/le-programme/",
        "programmeComplet": True,
        "propositions": {
            "police-municipale": {"texte": "Recruter 20 policiers municipaux supplémentaires (80 à 100 agents), patrouilles de soirée et couverture élargie", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "videoprotection": {"texte": "100 caméras supplémentaires sur zones sensibles, abords d'écoles et parkings, modernisation du CSU avec IA", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "prevention-mediation": {"texte": "Brigade de tranquillité nocturne (8 agents, 18h-2h), cellule anti-incivilités (bruit, dégradations, squats)", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "ecoles-renovation": {"texte": "Rénovation thermique de 20 écoles et crèches prioritaires (isolation, fenêtres, ventilation - 2M€)", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "periscolaire-loisirs": {"texte": "Prise en charge jusqu'à 50% des frais d'inscription extrascolaires pour familles modestes (150 000 €/an)", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "seniors": {"texte": "Programme intergénérationnel écoles-seniors, visites de convivialité, plan tranquillité senior avec boutons d'alerte", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "commerce-local": {"texte": "Plan 'Achetons Savoyard' (relocalisation 30% achats), Maison de l'Artisanat Savoyard, marchés '100% locaux'", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "attractivite": {"texte": "Prix de l'innovation annécienne (35 000 €/an) pour startups, TPE et artisans innovants", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "acces-logement": {"texte": "Aide accession à la propriété jusqu'à 10 000 € pour primo-accédants, priorité jeunes couples annéciens", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "logement-social": {"texte": "20 logements sociaux réservés aux agents essentiels (policiers, enseignants, soignants), habitat intergénérationnel", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "logements-vacants": {"texte": "Maintien et durcissement du plafond Airbnb (120 jours/an), contrôles renforcés et amendes systématiques", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "equipements-culturels": {"texte": "Label 'Culture Savoyarde', subventions majorées pour associations culturelles, priorité aux artistes locaux", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "evenements-creation": {"texte": "Refonte du Marché de Noël (70% stands locaux), Fête de l'identité annécienne et savoyarde", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "amenagement-urbain": {"texte": "Maîtrise de la croissance urbaine : opposition aux projets de bétonisation qui bouleversent l'équilibre des quartiers", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "velo-mobilites-douces": {"texte": "Plan pluriannuel de 10 km de pistes cyclables interconnectées (1,5M€), parkings vélos", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "pietons-circulation": {"texte": "Refonte du plan de circulation, réautoriser les traversées, deux parkings souterrains en cœur de ville", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "stationnement": {"texte": "Création de deux parkings souterrains en cœur de ville pour augmenter la capacité de stationnement", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "climat-adaptation": {"texte": "Plan 'fraîcheur urbaine' : désimperméabilisation cours d'école, zones d'ombre, brumisateurs (700 000 €/an)", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "services-publics": {"texte": "Guichet unique 'Mon Annecy' physique et en ligne pour toutes les démarches municipales (120 000 €)", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "transparence": {"texte": "Charte de transparence : absences publiées, subventions accessibles, conflits d'intérêts déclarés", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
            "budget-participatif": {"texte": "Budget annuel de 300 000 € pour les projets de participation citoyenne", "source": "retrouvons-annecy.fr", "sourceUrl": "https://retrouvons-annecy.fr/le-programme/"},
        }
    }
})

# =============================================================================
# 5. CHAMBÉRY : Bernard (24)
# =============================================================================
print("\n=== CHAMBÉRY ===")
update_city("chambery-2026.json", {
    "bernard": {
        "programmeUrl": "https://brice-bernard.fr/programme.html",
        "programmeComplet": True,
        "propositions": {
            "police-municipale": {"texte": "Recrutement de +25 agents (seuil 1 policier/1000 hab.), police de quartier, brigade de nuit 7j/7, armement complet", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "videoprotection": {"texte": "Passage de 91 à plus de 250 caméras, installation autour des écoles, gares et quartiers sensibles", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "prevention-mediation": {"texte": "Unité cynophile municipale, cellule anti-stupéfiants, lutte contre rodéos urbains, brigade 'Propreté express 24h'", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "violences-femmes": {"texte": "Présence policière renforcée le soir, boutons d'alerte pour les commerces", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "commerce-local": {"texte": "Guichet unique 'Entreprendre à Chambéry', pacte fiscal Pro-TPE, revitalisation cellules commerciales vides, label 'Produit à Chambéry'", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "emploi-insertion": {"texte": "'Tremplins chambériens' : locaux à loyers progressifs pour jeunes créateurs avec mentorat, bourse municipale de l'emploi", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "attractivite": {"texte": "Prix de l'innovation locale, produits régionaux dans les cantines, marchés publics valorisant les entreprises locales", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "ecoles-renovation": {"texte": "Plan 'Écoles 2033' : audit et rénovation thermique et électrique des établissements, sécurisation des accès", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "petite-enfance": {"texte": "Aide municipale ciblée à la garde d'enfants (400 €/an/foyer) pour soignants, policiers, familles à horaires décalés", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "periscolaire-loisirs": {"texte": "Extension des horaires périscolaires (matin et soir), recrutement d'animateurs, tarifs modulés selon les revenus", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "jeunesse": {"texte": "Pass Jeunes Chambéry (sport, culture, engagement citoyen), Maison de la Jeunesse et des Étudiants", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "centres-sante": {"texte": "Maisons municipales de santé, carte Pro-Santé stationnement 20€/an, bus médical, plan 'Médecins à Chambéry'", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "prevention-sante": {"texte": "Plan santé mentale et prévention du mal-être, mutuelle communale étendue aux seniors et étudiants", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "seniors": {"texte": "Plan 'Bien vieillir' : service d'aide quotidienne, réseau voisins solidaires, résidences intergénérationnelles, chèque énergie", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "espaces-verts": {"texte": "1 enfant né = 1 arbre planté, entretien renforcé, fleurissement durable espèces locales, jardins partagés chaque quartier", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "proprete-dechets": {"texte": "Plan Propreté équipes renforcées, brigade anti-tags (enlèvement 24h), objectif zéro dépôt sauvage, déchetteries mobiles", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "climat-adaptation": {"texte": "Brigade verte municipale assermentée, rénovation énergétique bâtiments municipaux, modernisation éclairage public", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "transports-en-commun": {"texte": "Navette électrique centre-ville/hôpital/gare/Bissy, transport à la demande pour seniors avec tarification solidaire", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "stationnement": {"texte": "Parking à deux étages en centre-ville, plan municipal de bornes de recharge pour véhicules électriques", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "pietons-circulation": {"texte": "Sécurisation abords d'écoles : signalétique renforcée, zones apaisées avec ralentisseurs et vidéoprotection", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "equipements-sportifs": {"texte": "Plan de rénovation des équipements sportifs existants, audit complet des infrastructures", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "sport-pour-tous": {"texte": "Tarifs préférentiels jeunes et familles modestes, Pass Sport Chambéry, charte municipale du sport", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "transparence": {"texte": "Audit des finances dans les 100 premiers jours, plateforme 'Chambéry Transparence', charte d'intégrité et d'éthique", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "pouvoir-achat": {"texte": "Aucune hausse d'impôts municipaux durant le mandat, réduction ciblée des dépenses de fonctionnement", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "aide-sociale": {"texte": "Mutuelle communale renforcée, carte 'Aidant Chambéry', soutien aux associations de terrain (Restos du Cœur, Croix-Rouge)", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "accessibilite": {"texte": "Amélioration des trottoirs, transports et bâtiments pour l'accessibilité universelle, aires de jeux adaptées", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
            "services-publics": {"texte": "Valorisation des agents municipaux, simplification des procédures, journée des agents de la Ville", "source": "brice-bernard.fr", "sourceUrl": "https://brice-bernard.fr/programme.html"},
        }
    }
})

# =============================================================================
# 6. LA SEYNE-SUR-MER : Minniti (19) + Mansour (14)
# =============================================================================
print("\n=== LA SEYNE-SUR-MER ===")
update_city("la-seyne-sur-mer-2026.json", {
    "minniti": {
        "programmeUrl": "https://josephminniti2026.fr/",
        "programmeComplet": False,
        "propositions": {
            "police-municipale": {"texte": "Sécurité renforcée avec une police municipale H24 et des bornes d'appel d'urgence", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "videoprotection": {"texte": "136 caméras déjà installées, poursuite du développement de la vidéoprotection", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "pietons-circulation": {"texte": "Rénovation de la traversée du port et corniche de Tamaris (12,5 km de routes, 16,2 km de trottoirs)", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "stationnement": {"texte": "326 places de parking créées (Esplageolles, Renan, Gare SNCF, Aristide Briand, Bourse)", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "velo-mobilites-douces": {"texte": "Poursuite du développement des pistes cyclables (3,2 km déjà créés)", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "equipements-sportifs": {"texte": "Rénovation de la piscine municipale, stade Léry et nouvelle pelouse au stade Squilaci", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "centres-sante": {"texte": "Création d'une nouvelle maison de santé", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "petite-enfance": {"texte": "Relais petite enfance dans les quartiers Nord et pépinière étudiante", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "ecoles-renovation": {"texte": "Budget d'investissement triplé pour les écoles, création de la cantine Verne", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "periscolaire-loisirs": {"texte": "100 places supplémentaires dans les centres aérés", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "vie-associative": {"texte": "Création d'une maison des associations", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "proprete-dechets": {"texte": "Lutte contre les dépôts sauvages, poubelles enterrées, brigade de propreté (6 agents)", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "espaces-verts": {"texte": "Nouvelles plantations (25 520 déjà réalisées) et création d'une ferme pédagogique", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "amenagement-urbain": {"texte": "Projet des ateliers mécaniques, rénovation espace public et cœur des Sablettes, nouveau port de plaisance", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "commerce-local": {"texte": "Label de qualité aquaculture et création d'une pépinière d'entreprises", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "seniors": {"texte": "Conseil municipal des aînés, 40 logements seniors rénovés, 500 adhérents CCAS", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "services-publics": {"texte": "Mairie annexe et antenne de Police municipale dans les quartiers Sud", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "transparence": {"texte": "Budget maîtrisé : pas d'augmentation des impôts communaux", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
            "evenements-creation": {"texte": "Poursuite de La Kermesse (30 000 spectateurs) et musée immersif à Balaguier", "source": "josephminniti2026.fr", "sourceUrl": "https://josephminniti2026.fr/"},
        }
    },
    "mansour": {
        "programmeUrl": "https://cheikhmansourmunicipales2026.fr/",
        "programmeComplet": False,
        "propositions": {
            "police-municipale": {"texte": "Renforcer le nombre de policiers municipaux et augmenter le budget dédié à la sécurité", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "videoprotection": {"texte": "Continuer à développer la vidéoprotection et renforcer l'éclairage public", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "prevention-mediation": {"texte": "Sécuriser toutes les écoles, lutter contre les incivilités par politique répressive et pouvoirs de police du Maire", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "pietons-circulation": {"texte": "Rénovation corniche de Tamaris (39M€), fluidification des réseaux routiers primaires et secondaires", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "amenagement-urbain": {"texte": "Connecter avenue Mazen à avenue Gagarine pour réduire embouteillages, élargissement avenue Henri Guillaume", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "quartiers-prioritaires": {"texte": "Désenclaver le nord de Berthe en créant une voie connectée aux grands axes pour ramener sécurité et commerce", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "equipements-sportifs": {"texte": "Réouverture de la piscine municipale, trouver un repreneur en accord avec TPM", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "centres-sante": {"texte": "Faciliter la création de maisons de santé en locaux municipaux, centre de soins pour désengorger les urgences", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "prevention-sante": {"texte": "Encourager le retour des médecins de nuit, soutenir les consultations à distance et l'IA encadrée", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "espaces-verts": {"texte": "Végétalisation des cours d'école, trottoirs et places pour rafraîchir la ville et améliorer la santé", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "attractivite": {"texte": "Réhabilitation ateliers mécaniques (projet économique, touristique et culturel), nouveau port autour de Grimaud", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "evenements-creation": {"texte": "Poursuite de la Kermesse, festival des fresques et ouverture du Fort Napoléon avec programmation culturelle", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "proprete-dechets": {"texte": "Politique répressive contre décharges sauvages, tags et dégradations via vidéosurveillance", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
            "transparence": {"texte": "Rompre avec la vieille politique, des élus responsables et loyaux envers les électeurs", "source": "cheikhmansourmunicipales2026.fr", "sourceUrl": "https://cheikhmansourmunicipales2026.fr/"},
        }
    }
})

# =============================================================================
# 7. FRÉJUS : Bonnemain (14)
# =============================================================================
print("\n=== FRÉJUS ===")
update_city("frejus-2026.json", {
    "bonnemain": {
        "programmeUrl": "https://www.notreparticestfrejus.fr/",
        "programmeComplet": False,
        "propositions": {
            "police-municipale": {"texte": "Augmenter les agents de police municipale sur le terrain, réinstaurer un véritable îlotage", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "proprete-dechets": {"texte": "Augmenter les poubelles en ville et abords d'écoles, multiplier les points de collecte d'encombrants", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "prevention-mediation": {"texte": "Interventions dans les écoles primaires pour sensibiliser les élèves à la propreté de leur ville", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "climat-adaptation": {"texte": "Rendre Fréjus ville éponge : zones de rétention d'eau, toits verts, revêtements perméables, jardins de pluie", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "espaces-verts": {"texte": "Promotion des espaces verts (parcs, jardins, micro-forêts), murs végétalisés et fossés plantés", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "renovation-energetique": {"texte": "Transition énergétique vers les renouvelables, réduire la consommation d'énergie des bâtiments publics", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "commerce-local": {"texte": "Stimuler l'activité économique locale, programmes de promotion des commerces locaux", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "emploi-insertion": {"texte": "Faciliter l'implantation d'entreprises, simplifier les procédures, soutien financier et logistique", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "attractivite": {"texte": "Développer le tourisme, améliorer les infrastructures touristiques, organiser événements et festivals", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "velo-mobilites-douces": {"texte": "Dossier mobilité douce : marche, vélo, transports publics pour réduire la dépendance automobile", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "amenagement-urbain": {"texte": "Réviser le PLU, soutenir la rénovation des quartiers existants plutôt que l'expansion urbaine", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "transparence": {"texte": "Audit de la dette de 159M€, nouvelle méthode : associer citoyens et acteurs locaux, charte éthique", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "sport-pour-tous": {"texte": "Sport inclusif, les personnes handicapées doivent pouvoir trouver l'activité sportive de leur choix", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
            "jeunesse": {"texte": "Les jeunes doivent trouver leur place : loisirs, transports, participation à la vie citoyenne", "source": "notreparticestfrejus.fr", "sourceUrl": "https://www.notreparticestfrejus.fr/"},
        }
    }
})

# =============================================================================
# 8. ANTONY : Precetti (10)
# =============================================================================
print("\n=== ANTONY ===")
update_city("antony-2026.json", {
    "precetti": {
        "programmeUrl": "https://www.antonyavenir.fr/programme",
        "programmeComplet": False,
        "propositions": {
            "budget-participatif": {"texte": "Mettre en place des conseils de quartier avec des élus référents", "source": "antonyavenir.fr", "sourceUrl": "https://www.antonyavenir.fr/programme"},
            "police-municipale": {"texte": "Renforcer les effectifs et les moyens pour la sécurité et la tranquillité publique", "source": "antonyavenir.fr", "sourceUrl": "https://www.antonyavenir.fr/programme"},
            "transports-en-commun": {"texte": "Renforcer la mobilité pour tous et partout, dans nos quartiers comme au cœur de ville", "source": "antonyavenir.fr", "sourceUrl": "https://www.antonyavenir.fr/programme"},
            "petite-enfance": {"texte": "Chercher activement des solutions pour augmenter l'offre d'accueil de la petite enfance", "source": "antonyavenir.fr", "sourceUrl": "https://www.antonyavenir.fr/programme"},
            "jeunesse": {"texte": "Développer des tiers lieux et des lieux de convivialité accessibles à la jeunesse", "source": "antonyavenir.fr", "sourceUrl": "https://www.antonyavenir.fr/programme"},
            "seniors": {"texte": "Valoriser l'expérience de nos seniors et renforcer les liens intergénérationnels", "source": "antonyavenir.fr", "sourceUrl": "https://www.antonyavenir.fr/programme"},
            "amenagement-urbain": {"texte": "Accompagner le développement de Jean Zay et Antonypole, accélérer la rénovation des quartiers vieillissants", "source": "antonyavenir.fr", "sourceUrl": "https://www.antonyavenir.fr/programme"},
            "climat-adaptation": {"texte": "Préparer la ville au défi climatique : végétalisation, fraîcheur urbaine, gestion de l'eau, rénovation bâtiments", "source": "antonyavenir.fr", "sourceUrl": "https://www.antonyavenir.fr/programme"},
            "attractivite": {"texte": "Relancer le développement économique et devenir la smart city du sud 92 avec partenariats Saclay", "source": "antonyavenir.fr", "sourceUrl": "https://www.antonyavenir.fr/programme"},
            "transparence": {"texte": "Adopter une charte éthique des élus et de la municipalité", "source": "antonyavenir.fr", "sourceUrl": "https://www.antonyavenir.fr/programme"},
        }
    }
})

# =============================================================================
# 9. RUEIL-MALMAISON : Indjian (19)
# =============================================================================
print("\n=== RUEIL-MALMAISON ===")
update_city("rueil-malmaison-2026.json", {
    "indjian": {
        "programmeUrl": "https://www.patrickindjianrueil2026.fr/",
        "programmeComplet": False,
        "propositions": {
            "budget-participatif": {"texte": "Conseils de villages élisant leurs représentants, budget participatif de 250 000€/an et référendum d'initiative citoyenne", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "logement-social": {"texte": "Augmenter la part des logements aidés de 25 à 35% en favorisant réhabilitations et reconversion de bureaux", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "acces-logement": {"texte": "Défendre les intérêts des locataires face aux bailleurs sociaux, soutenir une association de locataires par ensemble", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "velo-mobilites-douces": {"texte": "Voies cyclables temporaires dès 2026, pistes cyclables et parkings vélos sécurisés, cohabitation apaisée avec la voiture", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "transports-en-commun": {"texte": "Plan global de transport : réseau dense et fréquent, petit bus interne à la ville", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "climat-adaptation": {"texte": "Plan d'urgence canicules (ventilateurs, stores pour écoles/crèches/EHPAD), végétalisation des quartiers", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "renovation-energetique": {"texte": "Grand plan de rénovation énergétique pour bâtiments publics et logements, réduire les factures", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "centres-sante": {"texte": "Centre municipal de santé de médecins salariés (généralistes, spécialistes), sans dépassement d'honoraires", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "cantines-fournitures": {"texte": "Régie municipale pour les cantines : produits locaux, bio, alternative végétarienne, gratuité selon quotient familial", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "petite-enfance": {"texte": "Métiers de la petite enfance plus attractifs : meilleure rémunération, accès facilité à un logement proche", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "pouvoir-achat": {"texte": "Élargir le barème du quotient familial pour tarifs réduits sur cantine, centres de loisirs, activités", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "sport-pour-tous": {"texte": "Tarifs plus accessibles pour familles aux bas revenus, maintenance des équipements et accessibilité handicap", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "evenements-creation": {"texte": "Rétablir les MJC et le festival Rueil en scène (théâtre de rue, cinéma plein air, concerts)", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "egalite-discriminations": {"texte": "Jumeler Rueil avec une ville palestinienne pour affirmer la place de Rueil aux côtés des peuples opprimés", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "commerce-local": {"texte": "Soutenir un commerce durable de proximité : seconde main, réparation, artisanat local", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "emploi-insertion": {"texte": "Créer une Maison de l'Emploi et de l'Insertion pour accompagnement social et professionnel", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "police-municipale": {"texte": "Permanences hebdomadaires de police de proximité co-animées par ASVP et policiers dans chaque quartier", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "vie-associative": {"texte": "Maison commune pour associations et syndicats, mairies de quartier comme espaces d'échanges", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
            "transparence": {"texte": "Audit des finances de la ville (170M€ de dette, 2100€/habitant) pour gestion budgétaire rigoureuse", "source": "patrickindjianrueil2026.fr", "sourceUrl": "https://www.patrickindjianrueil2026.fr/"},
        }
    }
})

# =============================================================================
# RÉSUMÉ FINAL
# =============================================================================
print("\n" + "=" * 60)
print("INTÉGRATION TERMINÉE")
print("=" * 60)

# Recompte total
total = 0
for filename in os.listdir(ELECTIONS):
    if not filename.endswith(".json"):
        continue
    with open(os.path.join(ELECTIONS, filename), "r", encoding="utf-8") as f:
        d = json.load(f)
    for cat in d.get("categories", []):
        for st in cat.get("sousThemes", []):
            for v in st.get("propositions", {}).values():
                if v is not None:
                    total += 1

print(f"\nTotal propositions dans le comparateur : {total}")
