#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intègre les propositions de David Guiraud (Roubaix, LFI) extraites du
programme PDF officiel « Roubaix 2040 — Nos 400 propositions » (266 pages).

Source primaire : PDF téléchargé depuis guiraud2026.fr/programme
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "roubaix-2026.json")

SRC = "Programme David Guiraud, Fiers de Roubaix, 2026"
PDF = "https://guiraud2026.fr/wp-content/uploads/2026/02/Roubaix-2040-Nos-400-propositions.pdf"

def p(texte):
    return {"texte": texte, "source": SRC, "sourceUrl": PDF}


PROPS = {
    # ── SÉCURITÉ ──────────────────────────────────────────────────
    "police-municipale": p(
        "Créer une police municipale de proximité avec brigades à pied et à vélo, "
        "clarifier strictement les rôles entre police nationale et municipale, "
        "et défendre le maintien des effectifs de police nationale à Roubaix"
    ),
    "videoprotection": p(
        "Déployer la vidéoprotection de manière ciblée sur les points sensibles "
        "(parc de Barbieux, dépôts sauvages) en complément de la présence humaine"
    ),
    "prevention-mediation": p(
        "Créer des comités citoyens de la tranquillité publique dans chaque quartier, "
        "installer des cellules de médiation dans chaque mairie de quartier, "
        "lancer un plan « Aucun jeune laissé de côté » avec équipe éducative mobile, "
        "renforcer les Centres Sociaux avec psychologues et éducateurs, "
        "mettre fin aux rodéos urbains et prévenir les trafics par l'information et les parcours de sortie"
    ),
    "violences-femmes": p(
        "Renforcer la Maison des Femmes et coordonner la lutte contre les violences, "
        "créer un réseau de correspondants municipaux égalité dans chaque service, "
        "installer un Conseil local des femmes, sécuriser l'espace public (marches exploratoires, "
        "éclairage renforcé, label « Lieu Sûr », dispositif « demandez ANGELA »), "
        "expérimenter le congé menstruel pour les agentes et créer un espace de répit "
        "pour les femmes cheffes de famille"
    ),

    # ── TRANSPORTS ────────────────────────────────────────────────
    "transports-en-commun": p(
        "Réduire le coût des transports : gratuité pour les moins de 25 ans, les chômeurs "
        "et les ménages à faibles revenus, avancer vers la gratuité totale, "
        "rénover et renforcer les fréquences du réseau Ilévia, "
        "et créer un Pass Mobilité Solidaire à 1 €/mois pour les bénéficiaires de minima sociaux"
    ),
    "velo-mobilites-douces": p(
        "Lancer un grand plan vélo pour l'autonomie des jeunes, "
        "distribuer des bourses solidaires de vélos reconditionnés, "
        "créer un réseau cyclable sécurisé et rapide avec véloroutes continues, "
        "développer des stationnements sécurisés et des ateliers de réparation, "
        "et fonder un comité vélo citoyen"
    ),
    "pietons-circulation": p(
        "Piétonniser la Grand-Place, la Grand-Rue et la place de la Liberté, "
        "sécuriser l'avenue des Nations Unies avec mail piéton et zone 30, "
        "instaurer un code local de la rue (priorité piétons/PMR/cyclistes), "
        "créer des rues scolaires apaisées et redonner vie à la gare de Roubaix "
        "avec un tiers-lieu des mobilités"
    ),
    "stationnement": p(
        "Réduire le stationnement de surface en centre-ville au profit des piétons, "
        "et garantir un accès effectif au stationnement pour les personnes handicapées "
        "avec carte mobilité inclusion attachée à la personne"
    ),
    "tarifs-gratuite": p(
        "Instaurer la gratuité des transports pour les moins de 25 ans, les chômeurs "
        "et les ménages à faibles revenus, créer un Pass Mobilité Solidaire à 1 €/mois "
        "et avancer vers la gratuité totale des transports en commun"
    ),

    # ── LOGEMENT ──────────────────────────────────────────────────
    "logement-social": p(
        "Faire du logement une priorité municipale avec un adjoint dédié, "
        "exiger une répartition juste du logement social à l'échelle de la MEL, "
        "imposer des conventions d'objectifs contraignantes aux bailleurs, "
        "installer une cellule mobile de proximité dans les quartiers "
        "et créer une cellule municipale de prévention des expulsions"
    ),
    "logements-vacants": p(
        "Remettre en usage les logements vacants via une Mission Logement en transition, "
        "mobiliser des chantiers d'insertion avec des jeunes "
        "et renforcer massivement la lutte contre l'habitat indigne et les marchands de sommeil"
    ),
    "encadrement-loyers": p(
        "Demander officiellement à l'État et à la MEL l'extension de l'encadrement des loyers "
        "à Roubaix et adopter une charte du logement et de la ville durable "
        "refusant la densification excessive"
    ),
    "acces-logement": p(
        "Développer l'accession populaire et coopérative au logement : "
        "foncière solidaire à l'échelle MEL, bail réel solidaire, "
        "habitat coopératif et participatif, "
        "et créer un établissement municipal de prêt d'outillage pour la rénovation"
    ),

    # ── ÉDUCATION ─────────────────────────────────────────────────
    "petite-enfance": p(
        "Garantir une place d'accueil pour chaque enfant dès la petite enfance "
        "avec des modes d'accueil diversifiés, créer des espaces d'accompagnement à la parentalité "
        "dans chaque mairie de quartier et installer des aires de jeux inclusives "
        "et intergénérationnelles dans chaque quartier"
    ),
    "ecoles-renovation": p(
        "Transformer les cours d'école en Cours Oasis (débitumisation, sols perméables, "
        "plantations massives, coins calmes, potagers), rénover thermiquement toutes les écoles, "
        "créer 5 écoles pilotes de transition écologique « à énergie positive » "
        "et défendre chaque école publique et chaque classe contre les fermetures"
    ),
    "cantines-fournitures": p(
        "Instaurer la gratuité de la cantine scolaire pour les familles dans le besoin, "
        "augmenter la part bio et locale dans la restauration collective, "
        "étudier la reprise en régie de la cantine municipale "
        "et faire de l'école un lieu d'éducation alimentaire avec potagers biologiques"
    ),
    "periscolaire-loisirs": p(
        "Créer une Grande Maison des Devoirs avec antennes dans chaque quartier, "
        "renforcer les tarifs solidaires pour centres de loisirs, piscines et activités, "
        "et proposer des classes transplantées (mer, montagne, échanges internationaux)"
    ),
    "jeunesse": p(
        "Développer le service civique comme tremplin, ouvrir les grandes écoles aux lycéens "
        "(Cordées de la réussite, tutorat), démocratiser l'accès à Erasmus Pro, "
        "organiser une cérémonie annuelle des diplômés roubaisiens à la salle Watremez "
        "et créer un Pass Jeune Engagement Culture"
    ),

    # ── ENVIRONNEMENT ─────────────────────────────────────────────
    "espaces-verts": p(
        "Lancer un Plan Canopée : rues vertes, 15 forêts de poche d'ici fin de mandat, "
        "vergers communaux, forêt comestible au Cul-de-Four, "
        "protéger le parc de Barbieux (brigade de tranquillité, rénovation), "
        "créer un plan de trame verte urbaine et valoriser le canal de Roubaix "
        "comme lieu de nature populaire"
    ),
    "proprete-dechets": p(
        "Reprendre en main la propreté par une régie municipale renforcée, "
        "viser le label « Ville propre » et « Zéro déchet d'ici 2030 », "
        "lutter fermement contre les dépôts sauvages (amendes multipliées), "
        "créer un Chèque Réparation vélo et électroménager (30-50 €), "
        "installer des toilettes publiques dignes en centre-ville et parc Barbieux, "
        "et réorganiser la collecte avec conteneurs enterrés"
    ),
    "climat-adaptation": p(
        "Déclarer l'état d'urgence climatique à Roubaix, "
        "renforcer le plan canicule (lieux frais accessibles, suivi personnes isolées), "
        "installer des miroirs d'eau et îlots de fraîcheur dans chaque quartier, "
        "déployer des récupérateurs d'eau de pluie pour les usages municipaux "
        "et interdire les barbecues sauvages en créant des zones dédiées sécurisées"
    ),
    "renovation-energetique": p(
        "Rénover thermiquement toutes les écoles, installer des ombrières solaires "
        "sur parkings et bâtiments publics, créer un service municipal de l'énergie "
        "(diagnostics, petits travaux, formation écogestes), "
        "viser « zéro logement passoire ou bouilloire » avec cartographie et chantiers d'insertion, "
        "lancer un plan roubaisien des énergies renouvelables avec tarif social "
        "et étendre le réseau de chaleur urbain"
    ),
    "alimentation-durable": p(
        "Créer une filière alimentaire municipale locale (production fruits/légumes, "
        "vergers communaux, légumerie municipale), expérimenter une sécurité sociale "
        "de l'alimentation (~100 €/mois de crédit alimentaire), "
        "viser le « zéro gaspillage » et « zéro plastique » en restauration collective, "
        "planter des arbres fruitiers en ville à récolte libre "
        "et accompagner vers le « zéro phyto »"
    ),

    # ── SANTÉ ─────────────────────────────────────────────────────
    "centres-sante": p(
        "Garantir un médecin traitant pour chaque Roubaisien avec aides à l'installation, "
        "créer un réseau de centres de santé municipaux ou coopératifs "
        "(professionnels salariés, tiers payant intégral, offre pluridisciplinaire) "
        "et installer un Conseil des pharmacies en lien avec la CPTS"
    ),
    "prevention-sante": p(
        "Faire de la prévention une priorité municipale : dépistages mobiles, "
        "stands santé sur les marchés et dans les écoles, Pass Sport Santé "
        "(prescription d'activité physique par les médecins), "
        "créer des espaces d'écoute en santé mentale, "
        "lutter contre les addictions (protoxyde d'azote, tabac, alcool) "
        "et accompagner l'accès à la complémentaire santé solidaire"
    ),
    "seniors": p(
        "Refuser la privatisation des EHPAD publics et contrôler les établissements, "
        "développer le co-logement solidaire seniors-étudiants, "
        "renforcer la Maison des Aidants (accueil, orientation, temps de répit), "
        "relancer le service de taxi solidaire pour soins et démarches "
        "et créer un réseau de voisins bienveillants contre l'isolement"
    ),

    # ── DÉMOCRATIE ────────────────────────────────────────────────
    "budget-participatif": p(
        "Réformer les budgets participatifs sur le modèle de Porto Alegre : "
        "2 % du budget d'investissement citoyen (~900 000 €/an), "
        "créer une Grande Assemblée Citoyenne de 60 membres tirés au sort (dès 16 ans), "
        "instaurer un droit d'interpellation citoyenne (pétition 2 % = inscription à l'ordre du jour) "
        "et organiser des votations citoyennes orientantes sur les projets ANRU"
    ),
    "transparence": p(
        "Adopter une charte éthique anticorruption avec référent alerte indépendant, "
        "publier un budget annuel transparent des financements et projets obtenus "
        "et mettre en place des achats publics sociaux et écologiquement responsables (SPASER)"
    ),
    "vie-associative": p(
        "Garantir transparence et équité dans le soutien aux associations "
        "(critères objectifs, vote en Conseil municipal), simplifier les démarches, "
        "sécuriser les pôles associatifs durables, généraliser les conventions pluriannuelles, "
        "relancer les « Prodiges de la République » (30 lauréats/an) "
        "et protéger la liberté associative"
    ),
    "services-publics": p(
        "Ouvrir 5 mairies de quartier (guichet complet, accompagnement administratif, "
        "relais France Services), réinternaliser les services publics (propreté, entretien, restauration), "
        "garantir des réponses rapides aux habitants, "
        "développer une application municipale unique (RBX) pour démarches et démocratie locale "
        "et lutter contre la fracture numérique avec formations gratuites"
    ),

    # ── ÉCONOMIE ──────────────────────────────────────────────────
    "commerce-local": p(
        "Relancer le Crédit municipal de Roubaix (microcrédits, prêt sur gage, épargne solidaire), "
        "créer un guichet « Entreprendre à Roubaix », revitaliser les marchés, "
        "animer les rues commerçantes avec des équipes municipales dédiées, "
        "soutenir la filière textile et mode (ESMOD, Blanchemaille, Tissel) "
        "et créer une foncière commerciale solidaire avec boutiques à l'essai"
    ),
    "emploi-insertion": p(
        "Remobiliser la Mission locale avec plans quinquennaux d'insertion, "
        "organiser un Grand Forum annuel de l'Emploi, "
        "généraliser les clauses sociales d'insertion dans la commande publique, "
        "créer des parcours d'autonomie économique pour 100 femmes/an, "
        "cartographier les besoins en main-d'œuvre quartier par quartier "
        "et ouvrir des garages solidaires coopératifs"
    ),
    "attractivite": p(
        "Faire de Roubaix un carrefour stratégique Nord/Europe, "
        "moderniser les jumelages (échanges scolaires, projets environnementaux), "
        "créer une Halle de la Méditerranée et des produits du monde à l'Épeule, "
        "développer l'économie transfrontalière avec l'Eurométropole, "
        "proposer une Zone Franche Urbaine 2.0 (économie circulaire, numérique inclusif) "
        "et organiser un Festival « 70 Nations »"
    ),

    # ── CULTURE ───────────────────────────────────────────────────
    "equipements-culturels": p(
        "Rendre la pratique artistique accessible (Conservatoire, École de danse, associations), "
        "ouvrir les grands équipements aux quartiers (Condition Publique, Colisée, La Piscine), "
        "moderniser le théâtre Pierre-de-Roubaix et remettre en état le théâtre Pierre-Richard, "
        "renforcer la médiathèque avec horaires étendus, "
        "soutenir les librairies indépendantes et lancer un Salon BD"
    ),
    "evenements-creation": p(
        "Créer le Festival URBX vitrine des artistes roubaisiens, "
        "lancer POP-UP RBX (scènes ouvertes mensuelles dans les quartiers), "
        "le label « Cultures de Roubaix » avec bourses et mentorat, "
        "un festival annuel de théâtre populaire et de rue, "
        "un Grand festival des musiques des origines "
        "et un festival annuel de cinéma populaire en plein air"
    ),

    # ── SPORT ─────────────────────────────────────────────────────
    "equipements-sportifs": p(
        "Rendre le Parc des Sports aux Roubaisiens avec gestion concertée, "
        "lancer un plan pluriannuel de rénovation des équipements sportifs "
        "(Nabuchodonosor, Brossolette), étudier la rénovation du stade populaire "
        "et créer un centre de référence sport de haut niveau"
    ),
    "sport-pour-tous": p(
        "Rendre le sport populaire accessible à tous avec un Pass Sport Populaire municipal, "
        "ouvrir les équipements soir et week-end, proposer des activités gratuites "
        "dans l'espace public chaque semaine, lancer le programme « Sport avec elles » "
        "dans les quartiers populaires (créneaux sécurisés, self-défense), "
        "créer un urban trail roubaisien et ouvrir les équipements scolaires aux clubs"
    ),

    # ── URBANISME ─────────────────────────────────────────────────
    "amenagement-urbain": p(
        "Élaborer un Agenda Roubaix Avenir 2040 coproduit avec les habitants, "
        "piétonniser le centre-ville, appliquer le principe « une friche = un projet », "
        "créer une Régie locale des lieux publics vacants, "
        "valoriser le réseau des places roubaisiennes "
        "et libérer l'espace public de la publicité (interdiction pubs nocives près des écoles)"
    ),
    "accessibilite": p(
        "Lancer un plan pluriannuel d'accessibilité chiffré et priorisé, "
        "appliquer le design universel dans l'urbanisme et les services publics, "
        "rendre les écoles réellement inclusives (cellule municipale handicap-éducation), "
        "créer une bourse solidaire du matériel médical, "
        "développer le handisport et les clubs inclusifs, "
        "et faire de la mairie un employeur exemplaire en matière de handicap"
    ),
    "quartiers-prioritaires": p(
        "Refonder les projets ANRU Alma et Épeule avec ateliers populaires d'urbanisme, "
        "réviser les projets du Pile et Trois-Ponts, "
        "lancer un plan de rattrapage Cul-de-Four, Oran-Cartigny et Sartel-Carihem "
        "(forêt urbaine, ferme urbaine) et revaloriser la rue Jules-Guesde"
    ),

    # ── SOLIDARITÉ ────────────────────────────────────────────────
    "aide-sociale": p(
        "Revaloriser les aides du CCAS (300-500 €/famille/an), "
        "lutter contre le non-recours aux droits avec un guichet social de proximité "
        "dans chaque mairie de quartier, créer des permanences sociales de proximité, "
        "renforcer l'accueil de jour et l'hébergement d'urgence pour les sans-abri, "
        "et créer un Pôle municipal Droits et Dignité des Personnes Étrangères"
    ),
    "egalite-discriminations": p(
        "Faire de Roubaix une ville résolument antiraciste avec un Observatoire des discriminations, "
        "soutenir les associations contre les LGBTIphobies (écoute, mise à l'abri), "
        "former tous les agents municipaux à l'accueil inclusif, "
        "valoriser la mémoire coloniale et l'histoire des immigrations "
        "et promouvoir la laïcité comme principe de respect et d'égalité"
    ),
    "pouvoir-achat": p(
        "Instaurer une tarification sociale et progressive de l'eau "
        "(gratuité des premiers m³ vitaux), renforcer les tarifs solidaires familles, "
        "négocier des plans d'apurement EDF/Engie avec accompagnement personnalisé, "
        "créer un Chèque Réparation vélo et électroménager (30-50 €) "
        "et relancer le Crédit municipal (prêts à taux réduit, épargne solidaire)"
    ),
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    added = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            sid = st["id"]
            if sid in PROPS:
                old = st["propositions"].get("guiraud")
                st["propositions"]["guiraud"] = PROPS[sid]
                if old is None:
                    added += 1
                    print(f"  + {sid}: AJOUTÉ")
                else:
                    updated += 1
                    print(f"  ~ {sid}: MIS À JOUR")

    # Mettre à jour le candidat
    for c in data["candidats"]:
        if c["id"] == "guiraud":
            c["programmeComplet"] = True
            c["programmeUrl"] = "https://guiraud2026.fr/programme"
            c["programmePdfPath"] = "Roubaix-2040-Nos-400-propositions.pdf"
            c["siteCampagne"] = "https://guiraud2026.fr/"
            print(f"\n  programmeComplet -> true")
            print(f"  programmeUrl -> https://guiraud2026.fr/programme")
            break

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n  Résultat: {updated} mis à jour, {added} ajoutés")
    print(f"  Total sous-thèmes Guiraud: {updated + added}")


if __name__ == "__main__":
    main()
