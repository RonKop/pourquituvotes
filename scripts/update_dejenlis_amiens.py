#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Met à jour les propositions d'Hubert de Jenlis (Nous, les Amiénois)
depuis le programme PDF reçu par email le 02/03/2026.
"""

import json
import os
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "amiens-2026.json")
CANDIDAT_ID = "dejenlis"

PROPOSITIONS = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Doubler les effectifs de la police municipale pour atteindre 140 agents d'ici 2032, avec une présence renforcée de nuit.",
        "Armer la police municipale dans les 100 premiers jours du mandat.",
        "Créer une brigade municipale canine dédiée à la lutte contre les trafics et la consommation de stupéfiants.",
        "Déployer un poste de police municipale mobile dans le quartier Saint-Leu.",
    ],
    "videoprotection": [
        "Déployer 500 caméras de vidéoprotection d'ici 2032 pour une meilleure couverture de tous les quartiers.",
    ],
    "prevention-mediation": [
        "Doubler le nombre de médiateurs sociaux, notamment aux abords des collèges et lycées.",
        "Lutter contre la mendicité agressive dans le centre-ville en lien avec les commerçants et les acteurs sociaux.",
        "Développer une politique de protection et de sensibilisation contre la cybercriminalité pour protéger entreprises, services publics et habitants.",
    ],
    "violences-femmes": [
        "Accompagner les victimes de violences intrafamiliales et soutenir les associations, y compris pour la mise à disposition de logements d'urgence.",
    ],

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Améliorer la desserte en bus, notamment vers l'Espace Industriel Nord, renforcer la fréquence dans les quartiers et poursuivre l'achat de bus moins polluants.",
        "Valoriser et renforcer le service de transport adapté pour les personnes à mobilité réduite.",
    ],
    "velo-mobilites-douces": [
        "Poursuivre le Plan Vélo avec des aménagements cyclables sécurisés et continus, l'installation de consignes à vélos et la location Buscyclette sans limitation de durée.",
        "Aménager un anneau vert cyclable en centre-ville pour sécuriser les déplacements et relier les quartiers.",
        "Accélérer l'installation de 400 bornes de recharge supplémentaires pour véhicules électriques.",
    ],
    "pietons-circulation": [
        "Mettre en œuvre un Plan piéton : trottoirs en bon état, passages piétons mieux visibles, éclairage renforcé, bancs pour se reposer et cohabitation organisée entre piétons, trottinettes, vélos et voitures.",
    ],
    "stationnement": [
        "Rendre gratuit le stationnement de moins d'une heure dans les 8 parkings souterrains (4 500 places).",
        "Étendre le stationnement résidentiel dans les quartiers où les habitants le demandent.",
    ],
    "tarifs-gratuite": None,

    # ── LOGEMENT ──
    "logement-social": None,
    "logements-vacants": None,
    "encadrement-loyers": None,
    "acces-logement": None,

    # ── ÉDUCATION ──
    "petite-enfance": [
        "Encourager la création de places en crèche et renforcer l'accompagnement des parents durant les 1 000 premiers jours.",
        "Développer des solutions de garde à temps partiel pour les familles, en particulier les familles monoparentales.",
        "Accompagner les enfants en situation de handicap en développant leur accueil dans les crèches municipales et en créant des aires de jeux inclusives.",
    ],
    "ecoles-renovation": [
        "Poursuivre la rénovation des écoles en priorisant l'isolation thermique et le confort des élèves et des enseignants.",
        "Végétaliser 100 % des cours d'écoles d'ici 2032.",
    ],
    "cantines-fournitures": [
        "Baisser le prix moyen de la cantine scolaire en adaptant les tarifs aux revenus avec de nouvelles tranches intermédiaires, sans hausse pour aucun foyer.",
    ],
    "periscolaire-loisirs": [
        "Renforcer le soutien scolaire et l'aide aux devoirs en lien avec les associations et l'engagement citoyen (enseignants retraités, étudiants, acteurs éducatifs).",
    ],
    "jeunesse": [
        "Créer une Académie des arts pour détecter et accompagner les talents des jeunes, notamment dans les quartiers.",
        "Dédier une enveloppe du budget participatif aux projets portés par les jeunes Amiénois.",
        "Mieux préparer l'orientation et l'insertion en travaillant étroitement avec les lycées professionnels pour adapter les formations aux besoins des entreprises locales.",
        "Créer un Pass Étudiant donnant un accès privilégié aux équipements culturels et sportifs amiénois.",
        "Doubler le nombre de bénéficiaires du Pass'ton Permis (1 200 bénéficiaires) pour lever un frein majeur à l'emploi.",
    ],

    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Planter 24 000 arbres et végétaliser toutes les rues pour qu'aucune ne soit sans végétation.",
        "Aménager les bords de Somme : végétalisation, accès au fleuve, limitation du béton, déplacements à pied et à vélo.",
        "Créer un corridor végétal reliant les Hortillonnages au parc de la Hotoie.",
        "Rénover et valoriser les grands parcs urbains : la Hotoie, le parc Saint-Pierre, le Marais des Trois Vaches, la plaine Victorine-Autier et la place-parc du Colvert.",
        "Tester l'ouverture de certaines cours d'écoles végétalisées le week-end dans les quartiers manquant d'espaces verts.",
    ],
    "proprete-dechets": [
        "Renforcer les moyens des opérations propreté avec des caméras mobiles et intelligentes pour identifier les auteurs de dépôts sauvages.",
        "Intensifier la lutte contre les incivilités via la Brigade verte : tags, autocollants et dégradations.",
        "Lancer des opérations propreté dans les cimetières.",
        "Doubler le nombre de passages autorisés en déchetterie (de 26 à 52 par an).",
        "Développer l'offre de toilettes publiques.",
        "Mobiliser massivement les services municipaux tous les 15 jours pour nettoyer, réparer et améliorer un quartier.",
    ],
    "climat-adaptation": None,
    "renovation-energetique": [
        "Aider financièrement à la rénovation énergétique de 1 000 logements publics et privés par an pour améliorer le confort et réduire les factures d'énergie.",
        "Développer les énergies renouvelables en étendant le réseau de chaleur urbain et en installant des panneaux solaires sur les bâtiments municipaux.",
    ],
    "alimentation-durable": [
        "Mettre en place une sécurité sociale de l'alimentation pour un accès de tous à une alimentation saine, locale et durable, à un prix adapté aux revenus.",
        "Développer les cueillettes solidaires pour valoriser les surplus agricoles et distribuer des paniers de fruits et légumes aux familles en difficulté.",
        "Faciliter l'installation de maraîchers supplémentaires, notamment dans les Hortillonnages, pour alimenter les restaurants scolaires en légumes frais.",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Créer des centres municipaux de santé avec des médecins salariés par la Ville, sans dépassement d'honoraires et avec des délais de rendez-vous réduits.",
        "Développer la mutuelle solidaire pour une couverture santé de qualité à un coût maîtrisé.",
    ],
    "prevention-sante": [
        "Faire de la santé mentale une priorité en renforçant la présence de psychologues dans les structures municipales et les établissements scolaires.",
        "Mettre en place un forum de prévention santé rassemblant l'ensemble des partenaires du Contrat local de santé.",
        "Développer la prévention santé et l'activité physique grâce au programme « Ville en Forme » et aux formations aux gestes qui sauvent.",
        "Former 3 000 Amiénois aux gestes de premiers secours.",
    ],
    "seniors": [
        "Doubler le nombre de places d'animations pour les séniors (50 000 places par an).",
        "Créer un Pass Séniors facilitant l'accès aux équipements municipaux et aux activités culturelles et sportives.",
        "Mettre en place une cantine pour les séniors avec des repas à prix très accessibles.",
        "Développer des temps de restauration partagés entre élèves et séniors pour renforcer le lien intergénérationnel.",
        "Aider financièrement à l'adaptation des logements au vieillissement et au handicap.",
        "Développer le portage de repas à domicile pour favoriser le maintien à domicile.",
        "Créer des solutions d'accueil temporaire pour les personnes malades afin d'offrir du répit aux proches aidants.",
        "Créer un Café des aidants, lieu convivial d'information, d'échange et de rencontre.",
    ],

    # ── DÉMOCRATIE ──
    "budget-participatif": None,
    "transparence": None,
    "vie-associative": [
        "Développer le Cloître Dewailly comme lieu central pour les associations avec des espaces de travail mutualisés et une meilleure visibilité de la Maison des Associations.",
    ],
    "services-publics": [
        "Moderniser les services publics de proximité en rénovant les mairies de quartier, en créant un pôle de services publics à Pierre Rollin et en déployant des espaces numériques accompagnés.",
        "Simplifier et dématérialiser les démarches administratives (urbanisme, crèche, cantine, périscolaire, eau…) avec mensualisation des factures.",
        "Mettre en place un médiateur municipal pour faciliter les relations entre les habitants et les services municipaux.",
        "Mettre l'intelligence artificielle au service des Amiénois pour simplifier l'accès aux services publics et améliorer les délais de réponse.",
    ],

    # ── ÉCONOMIE ──
    "commerce-local": [
        "Soutenir l'installation de commerces de proximité dans chaque quartier avec des aides dédiées et un droit de préemption sur les baux commerciaux et fonds de commerce.",
        "Faire d'Amiens une ville animée tout au long de l'année : marché de Noël, activités estivales, guinguettes, animations le samedi en centre-ville.",
    ],
    "emploi-insertion": [
        "Poursuivre et amplifier les dispositifs d'aides aux TPE et PME qui recrutent localement et créent des emplois durables.",
        "Renforcer les coopérations entre l'Université, la Région et Amiens Métropole pour transformer l'excellence scientifique en innovations et en emplois.",
        "Poursuivre la reconversion des friches économiques (ancien hôpital nord, site Cosserat) pour accueillir de nouveaux projets créateurs d'emplois.",
        "Créer de l'activité et des emplois locaux autour de l'intelligence artificielle.",
    ],
    "attractivite": [
        "Faire de l'arrivée du TGV une opportunité pour Amiens : développer l'accueil d'entreprises sur la ZAC Gare-la-Vallée et créer de l'emploi au cœur de la ville.",
        "Développer le tourisme d'affaires en renforçant l'attractivité de Mégacité et l'accueil de congrès et d'événements professionnels.",
        "Soutenir en priorité les filières qui recrutent : santé, agroalimentaire, numérique, recherche, transition écologique, logistique, industries culturelles et créatives.",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Mettre en lumière les grands monuments d'Amiens (Cathédrale, Beffroi, tour Perret) grâce à un éclairage peu énergivore.",
        "Rouvrir le Cirque Jules Verne à davantage de concerts et d'événements populaires.",
        "Lancer la rénovation de la bibliothèque Louis Aragon.",
        "Rouvrir l'Hôtel de Berny au public et y installer un musée consacré à l'histoire d'Amiens.",
    ],
    "evenements-creation": [
        "Lancer un grand carnaval populaire construit avec chacun des quartiers, les habitants et les associations.",
        "Continuer d'accueillir de grands événements culturels et sportifs populaires et fédérateurs.",
    ],

    # ── SPORT ──
    "equipements-sportifs": [
        "Poursuivre la rénovation des équipements sportifs de proximité (gymnases, terrains de football).",
        "Créer un skatepark couvert à l'ouest d'Amiens sur le site des Astelles.",
    ],
    "sport-pour-tous": [
        "Développer l'accès au sport dès le plus jeune âge en renforçant l'intervention des animateurs sportifs dans les écoles et les quartiers et en ouvrant les équipements sportifs en soirée pour les adolescents.",
        "Développer le sport-santé et les pratiques adaptées pour les séniors et les publics éloignés de la pratique sportive.",
    ],

    # ── URBANISME ──
    "amenagement-urbain": [
        "Créer dans chaque quartier un esprit « place de village » : espaces de convivialité, aires de jeux, bancs, tables de pique-nique, boulodromes, agrès sportifs.",
        "Engager la rénovation du centre-ville piéton : rénovation de la place Léon-Debouverie, zone piétonne réaménagée, végétalisée et plus accessible.",
    ],
    "accessibilite": [
        "Rendre accessibles aux personnes à mobilité réduite les équipements municipaux et les manifestations organisées par la Ville.",
        "Renforcer l'accessibilité pour tous les handicaps : trottoirs sans obstacles, cheminements continus, feux sonores, signalétique lisible et zones de repos.",
        "Créer un Conseil local du handicap rassemblant les associations pour améliorer la vie quotidienne des personnes en situation de handicap.",
        "Former davantage les agents municipaux à l'accueil et à la prise en compte des situations de handicap.",
    ],
    "quartiers-prioritaires": None,

    # ── SOLIDARITÉ ──
    "aide-sociale": [
        "Installer un guichet unique des aides sociales, visible et accessible, pour renforcer l'accès aux droits.",
        "Créer une banque vestimentaire solidaire dans une logique de réemploi et de dignité.",
    ],
    "egalite-discriminations": None,
    "pouvoir-achat": [
        "Ne pas augmenter les impôts ni les tarifs municipaux sur la durée du mandat (cantine, crèche, centres de loisirs…).",
        "Baisser le prix moyen de la cantine scolaire en adaptant davantage les tarifs aux revenus.",
        "Mettre en place des groupements d'achats pour faire baisser les factures d'énergie des Amiénois.",
    ],
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for c in data["candidats"]:
        if c["id"] == CANDIDAT_ID:
            c["programmeUrl"] = "https://hubertdejenlis.fr/"
            c["programmeComplet"] = True
            break

    updated = 0
    added = 0
    total_mesures = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id not in PROPOSITIONS:
                continue

            new_mesures = PROPOSITIONS[st_id]
            if new_mesures is None:
                continue

            if "propositions" not in st:
                st["propositions"] = {}

            had_before = (
                CANDIDAT_ID in st["propositions"]
                and st["propositions"][CANDIDAT_ID]
                and st["propositions"][CANDIDAT_ID].get("mesures")
            )

            st["propositions"][CANDIDAT_ID] = {"mesures": new_mesures}
            total_mesures += len(new_mesures)
            if had_before:
                updated += 1
            else:
                added += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"{'='*55}")
    print(f"  MISE À JOUR — Hubert de Jenlis (Amiens)")
    print(f"{'='*55}")
    print(f"  Sous-thèmes mis à jour : {updated}")
    print(f"  Sous-thèmes ajoutés    : {added}")
    print(f"  Total mesures          : {total_mesures}")
    print(f"  JSON écrit : {JSON_PATH}")


if __name__ == "__main__":
    main()
