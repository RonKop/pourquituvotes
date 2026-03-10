#!/usr/bin/env python3
"""
Re-extraction du programme de Nathalie Koenders (Dijon) — 165 propositions
Source : https://koenders2026.fr/programme/ (14 thèmes, 165 propositions numérotées)
Date d'extraction : 24 février 2026

Ce script remplace toutes les mesures Koenders dans dijon-2026.json
par les propositions individuelles extraites du site officiel.
"""

import sys
import io
import os
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

SOURCE = "Programme officiel 2026 — Nathalie Koenders"
SOURCE_URL = "https://koenders2026.fr/programme/"

# ============================================================================
# 165 propositions mappées sur les 44 sous-thèmes standard
# ============================================================================

PROPOSITIONS = {
    # ── SÉCURITÉ ──────────────────────────────────────────────────────────
    "police-municipale": [
        # 10
        "Étendre les horaires de la police municipale jusqu'à 5h du matin les jeudi, vendredi et samedi soir.",
        # 11
        "Créer une brigade dédiée à la lutte contre les incivilités et lutter contre les rodéos urbains.",
        # 13
        "Renforcer les moyens de la Police municipale armée et poursuivre sa professionnalisation.",
    ],
    "videoprotection": [
        # 12
        "Expérimenter un poste de police municipale mobile et achever l'installation des caméras.",
        # 17
        "Lutter contre les nuisances sonores et mettre en place des radars sonores.",
    ],
    "prevention-mediation": [
        # 14
        "Renforcer les actions de médiation et de prévention contre les addictions.",
        # 15
        "Encadrer plus strictement l'usage des trottinettes et autres engins électriques.",
        # 16
        "Créer une réserve communale de sécurité civile et développer des formations aux premiers secours.",
        # 18
        "Augmenter le nombre de jeunes en Travaux d'Intérêt Général accueillis.",
    ],
    "violences-femmes": [
        # 107 (from "Grandir" theme but maps to violences-femmes)
        "Engager un plan de lutte contre le harcèlement et les violences envers les enfants.",
    ],

    # ── TRANSPORTS ────────────────────────────────────────────────────────
    "transports-en-commun": [
        # 43
        "Construire la troisième ligne de tramway T3 en intégrant les conclusions de la concertation.",
        # 48
        "Achever la mise en accessibilité des arrêts de bus et renforcer le service DiviAccès.",
        # 51
        "Étendre la flotte des bus électriques.",
        # 53
        "Créer un Service Express Régional Métropolitain avec la Région Bourgogne-Franche-Comté.",
        # 157
        "Poursuivre la mobilisation pour obtenir la réouverture d'une liaison TGV.",
    ],
    "velo-mobilites-douces": [
        # 44
        "Accélérer la politique vélo et assurer la continuité des voies cyclables.",
        # 45
        "Étendre l'offre de location Diviavélo avec une flotte de vélos électriques.",
        # 50
        "Aménager des zones de livraison et d'attente spécifiques pour les livreurs à vélo.",
    ],
    "pietons-circulation": [
        # 46
        "Déployer des zones 30 dans tous les quartiers résidentiels.",
        # 47
        "Améliorer la cohabitation, la sécurité et la courtoisie entre usagers de la route.",
        # 49
        "Établir un schéma directeur d'entretien de la voirie et sécuriser les piétons.",
        # 52
        "Encourager les modes de livraisons propres, coordonnés, et silencieux.",
    ],
    "stationnement": [
        # 146
        "Instaurer les 15 minutes de stationnement gratuit dans les zones payantes.",
        # 145
        "Faciliter l'intervention des artisans au centre-ville par des solutions de mobilité adaptées.",
    ],
    "tarifs-gratuite": [
        # 3
        "Réduire le prix de l'abonnement Divia pour les jeunes de 18 à 25 ans et conserver un prix de ticket parmi les moins chers de France.",
    ],

    # ── LOGEMENT ──────────────────────────────────────────────────────────
    "logement-social": [
        # 36
        "Combattre la crise du logement en soutenant la construction et la rénovation énergétique.",
        # 38
        "Poursuivre la construction de logements adaptés aux évolutions de la société.",
        # 40
        "Inciter les promoteurs à penser la sécurité des logements dès la conception.",
        # 92
        "Développer l'accession abordable à la propriété.",
    ],
    "logements-vacants": [
        # 41
        "Aider à la structuration de la filière d'approvisionnement en matériaux durables.",
    ],
    "encadrement-loyers": [
        # 37
        "Organiser des Assises du logement et de l'architecture pour associer les habitants.",
        # 42
        "Réguler les locations de courte durée type Airbnb pour préserver le logement résidentiel.",
    ],
    "acces-logement": [
        # 39
        "Créer un poste d'écologue municipal pour prendre en compte la biodiversité.",
        # 84
        "Finaliser l'éco-quartier Arsenal en lien avec les besoins des habitants.",
    ],

    # ── ÉDUCATION ─────────────────────────────────────────────────────────
    "petite-enfance": [
        # 116
        "Adapter l'offre d'accueil de petite enfance aux évolutions démographiques.",
        # 117
        "Élaborer une charte qualité de l'accueil du jeune enfant.",
        # 118
        "Favoriser les passerelles entre crèches et écoles en encourageant les projets communs.",
        # 89
        "Créer un relais d'assistante maternelle et un centre médical.",
    ],
    "ecoles-renovation": [
        # 109
        "Achever la suppression des préfabriqués et la rénovation des écoles.",
        # 73
        "Achever la rénovation de l'école Joséphine Baker.",
        # 80
        "Rénover l'école Lallemant.",
        # 99
        "Rénover l'école Voltaire.",
        # 103
        "Rénover l'école de la Colombière.",
    ],
    "cantines-fournitures": [
        # 106
        "Proposer un kit de fournitures scolaires essentielles aux élèves des écoles élémentaires.",
        # 112
        "Viser l'objectif de 75% de produits bio ou locaux dans la restauration scolaire.",
        # 113
        "Initier un plan de lutte contre la sédentarité et d'éducation à l'alimentation.",
    ],
    "periscolaire-loisirs": [
        # 108
        "Lutter contre les addictions aux écrans dès le plus jeune âge.",
        # 110
        "Mieux répondre aux besoins de toutes les familles qui souhaitent inscrire leurs enfants.",
        # 111
        "Soutenir la place et le rôle des parents dans l'éducation des enfants.",
        # 114
        "Renforcer la sécurité des trajets piétons domicile-école et soutenir la création de Pédibus.",
        # 115
        "Créer des rues aux écoles et installer du mobilier à hauteur d'enfant.",
    ],
    "jeunesse": [
        # 54
        "Prévenir la pauvreté et soutenir l'installation et l'accès à l'autonomie des jeunes.",
        # 133
        "Relancer la pratique sportive chez les adolescents en proposant des loisirs attractifs.",
    ],

    # ── ENVIRONNEMENT ─────────────────────────────────────────────────────
    "espaces-verts": [
        # 19
        "Conforter le Jardin de l'Arquebuse en grand pôle dijonnais de la biodiversité.",
        # 20
        "Poursuivre la désimperméabilisation des sols et la végétalisation de la ville et du centre-ville.",
        # 22
        "Développer les jardins partagés et potagers urbains dans tous les quartiers de la ville.",
        # 28
        "Planter 50 000 arbres et arbustes durant le mandat et développer le permis citoyen de végétaliser.",
        # 30
        "Préserver et prendre soin des grands espaces de pleine terre, des parcs, combes et jardins.",
        # 31
        "Défendre la cause des animaux et aménager des espaces de liberté pour les chiens.",
        # 35
        "Créer un comité citoyen de la biodiversité en lien avec le Jardin de l'Arquebuse.",
        # 87
        "Créer un verger conservatoire dans le quartier des Varennes.",
        # 101
        "Créer un grand parc urbain dans le quartier Eco-cité jardin des maraîchers.",
    ],
    "proprete-dechets": [
        # 24
        "Rénover l'usine d'incinération des ordures ménagères pour améliorer ses performances.",
        # 33
        "Maintenir le haut niveau de propreté de la ville et renforcer la lutte contre les tags.",
        # 34
        "Supprimer les contenants en plastique à usage unique dans tous les services municipaux.",
    ],
    "climat-adaptation": [
        # 23
        "Viser la neutralité carbone à l'horizon 2050 et déployer 250 hectares de panneaux photovoltaïques.",
        # 25
        "Améliorer encore la qualité de l'air, de l'eau et de l'alimentation par le plan Climat.",
        # 29
        "Créer davantage d'îlots de fraîcheurs et installer des brumisateurs.",
    ],
    "renovation-energetique": [
        # 4
        "Proposer des espaces conseil et d'accompagnement à la maîtrise des dépenses énergétiques.",
        # 5
        "Développer le réseau de chaleur urbain, levier de transition et de stabilité des coûts énergétiques.",
        # 81
        "Accompagner la rénovation énergétique des grandes copropriétés.",
        # 9
        "Préserver un important budget d'investissement pour soutenir la transition écologique.",
    ],
    "alimentation-durable": [
        # 21
        "Assurer l'accès à une alimentation locale de qualité pour les enfants en restauration scolaire.",
        # 27
        "Conforter le rôle de la légumerie métropolitaine et accroître la relocalisation agricole.",
        # 124
        "Développer la culture populaire autour de l'alimentation et du vin.",
        # 149
        "Accompagner la création de marchés de producteurs locaux dans tous les quartiers.",
    ],

    # ── SANTÉ ─────────────────────────────────────────────────────────────
    "centres-sante": [
        # 62
        "Faciliter l'accès aux soins et soutenir l'installation des maisons France Santé.",
        # 161
        "Ouvrir une école publique de kinésithérapie et développer filières de santé.",
    ],
    "prevention-sante": [
        # 2
        "Créer une mutuelle municipale pour offrir une complémentaire santé moins chère pour tous.",
        # 63
        "Développer les espaces sans tabac et soutenir la lutte contre le cancer.",
    ],
    "seniors": [
        # 57
        "Développer l'entraide intergénérationnelle et lutter contre l'isolement des séniors.",
        # 58
        "Rénover la Maison des Séniors pour en faire un lieu ressource modernisé.",
        # 59
        "Expérimenter le service civique séniors pour les retraités qui souhaitent s'investir.",
    ],

    # ── DÉMOCRATIE ────────────────────────────────────────────────────────
    "budget-participatif": [
        # 66
        "Conforter le rôle des Ateliers de quartier et les budgets participatifs.",
    ],
    "transparence": [
        # 67
        "Ouvrir une agora citoyenne – tiers lieu, espace de dialogue direct entre les élus et la population.",
        # 1
        "Poursuivre une gestion rigoureuse et responsable des deniers publics sans augmentation des taux des impôts municipaux.",
    ],
    "vie-associative": [
        # 65
        "Conforter le rôle de la Maison des Associations rénovée et affirmer le soutien au tissu associatif.",
        # 74
        "Ouvrir un nouvel espace associatif aux Marmuzots.",
        # 86
        "Créer un espace dédié aux associations et aux habitants au sein du Château de Pouilly.",
    ],
    "services-publics": [
        # 56
        "Promouvoir l'action du Centre Communal d'Action Sociale et conforter le rôle des travailleurs sociaux.",
        # 96
        "Rénover la bibliothèque et la mairie de quartier Mansart.",
        # 98
        "Ouvrir une maison des habitants à Hyacinthe Vincent.",
        # 100
        "Ouvrir un point d'accès aux droits boulevard de l'Université.",
    ],

    # ── ÉCONOMIE ──────────────────────────────────────────────────────────
    "commerce-local": [
        # 147
        "Soutenir le commerce de proximité et la fédération Shop'in Dijon.",
        # 148
        "Étudier la création d'une foncière commerciale pour développer les commerces.",
        # 78
        "Accompagner la réinstallation de commerces de proximité et de services au cœur du quartier.",
        # 90
        "Inciter à la rénovation du centre commercial Epirey.",
    ],
    "emploi-insertion": [
        # 142
        "Soutenir le développement des compétences en rapport avec les besoins du secteur économique.",
        # 143
        "Accompagner l'investissement dans l'Intelligence Artificielle avec une approche éthique.",
        # 144
        "Valoriser les entreprises patrimoniales en s'appuyant sur les chambres consulaires.",
    ],
    "attractivite": [
        # 140
        "Renforcer les filières d'excellence (santé, agroalimentaire, numérique et tourisme).",
        # 141
        "S'engager pour une croissance sûre et durable dans un environnement favorable.",
        # 158
        "Promouvoir la fierté d'être dijonnais, cité internationale de la gastronomie et du vin.",
        # 159
        "Créer un circuit touristique pédestre autour de l'histoire des Ducs de Bourgogne.",
        # 160
        "Conforter le rôle moteur de l'Université Bourgogne Europe.",
        # 162
        "Poursuivre l'accueil des étudiants étrangers pour faire rayonner l'excellence.",
        # 163
        "Développer une stratégie de communication ciblée pour positionner Dijon comme destination.",
        # 164
        "Initier un réseau international des villes vini-viticoles et faire vivre les jumelages.",
        # 165
        "Valoriser davantage Gustave Eiffel, le plus célèbre des dijonnais.",
    ],

    # ── CULTURE ───────────────────────────────────────────────────────────
    "equipements-culturels": [
        # 119
        "Reconstruire la médiathèque Champollion, nouvel espace de lecture convivial.",
        # 120
        "Confirmer et amplifier le rôle de l'Opéra de Dijon comme scène lyrique de référence nationale.",
        # 121
        "Faire rayonner les grands équipements culturels.",
        # 125
        "Conforter le pôle culturel de la Cité Internationale de la gastronomie et du vin.",
        # 127
        "Créer une agora culturelle avec la rénovation de la bibliothèque Colette.",
        # 128
        "Ouvrir le Dancing, Centre de développement chorégraphique national.",
        # 130
        "Soutenir la rénovation et l'agrandissement du Consortium.",
        # 154
        "Mettre en valeur tous nos musées et leurs collections.",
    ],
    "evenements-creation": [
        # 122
        "Soutenir toutes les formes de cultures et de création artistique.",
        # 123
        "Créer une fête populaire à dimension européenne autour de l'histoire des Ducs de Bourgogne.",
        # 126
        "Organiser et soutenir les grands évènements culturels et populaires.",
        # 129
        "Installer des œuvres d'art dans l'espace public et dans les lieux de vie.",
        # 79
        "Accompagner la compagnie Cirq'ônflex dans le développement de ses activités circassiennes.",
    ],

    # ── SPORT ─────────────────────────────────────────────────────────────
    "equipements-sportifs": [
        # 131
        "Poursuivre la rénovation du patrimoine sportif et créer des espaces dédiés.",
        # 132
        "Engager une réflexion partagée sur la création d'équipements sportifs majeurs.",
        # 135
        "Créer et aménager des espaces sécurisés pour la course, la marche, le trail, le VTT.",
    ],
    "sport-pour-tous": [
        # 134
        "Encourager l'activité physique pour toutes et tous adaptée aux capacités de chacun.",
        # 136
        "Relancer la Nuit du sport pour célébrer nos clubs et nos sportifs.",
        # 137
        "Poursuivre l'engagement municipal en faveur du sport pour toutes et tous.",
        # 138
        "Maintenir l'aide au paiement des cotisations pour les jeunes et les séniors.",
        # 139
        "Accueillir de grands évènements populaires comme le Tour de France.",
    ],

    # ── URBANISME ─────────────────────────────────────────────────────────
    "amenagement-urbain": [
        # 68
        "Installer des bacs-arborés rue de la Liberté.",
        # 69
        "Renouveler chaque année le jardin éphémère de la place de la Sainte Chapelle.",
        # 70
        "Déployer des voiles d'ombrages dans l'espace public.",
        # 71
        "Végétaliser la cour de la bibliothèque patrimoniale.",
        # 72
        "Piétonniser la rue Auguste Comte et la place des Halles Champeaux.",
        # 75
        "Embellir la place Barbe.",
        # 76
        "Poursuivre l'aménagement et la valorisation du parc des carrières Bacquin.",
        # 82
        "Créer une nouvelle coulée verte rue de l'île.",
        # 83
        "Profiter du passage du Tour de France féminin pour revaloriser l'avenue Eiffel.",
        # 85
        "Développer l'agrément et la convivialité du port du canal.",
        # 88
        "Poursuivre la valorisation du parc de la Toison d'Or.",
        # 93
        "Végétaliser le parking du Conservatoire tout en maintenant le stationnement.",
        # 94
        "Créer un nouveau parc urbain à la place du parking de Dijon métropole.",
        # 95
        "Réinvestir et sécuriser le square Clemenceau avec les habitants.",
        # 97
        "Engager un plan d'aménagement pour le devenir des terrains SNCF de Porte Neuve.",
        # 102
        "Sortir de l'occupation illégale des Lentillères et maintenir la fonction nourricière.",
        # 105
        "Aménager et sécuriser la place Wilson pour en permettre l'animation.",
        # 150
        "Poursuivre la rénovation et faire vivre le patrimoine dijonnais (églises).",
        # 151
        "Lancer la rénovation des Halles centrales dans le prolongement de l'étude réalisée.",
        # 152
        "Poursuivre l'opération de rénovation des façades en centre-ville.",
        # 153
        "Piétonniser la cour d'honneur du Palais des Ducs et des États de Bourgogne.",
        # 155
        "Rénover le Parc des Expositions et des Congrès et l'adapter aux nouveaux usages.",
        # 156
        "Créer un passeport mémoriel pour encourager la participation aux cérémonies patriotiques.",
    ],
    "accessibilite": [
        # 60
        "Rendre tous les services publics municipaux accessibles aux personnes en situation de handicap.",
        # 32
        "Installer de nouvelles fontaines à eau et des bancs avec accoudoirs.",
        # 61
        "Installer davantage de toilettes publiques accessibles et créer des espaces bébé.",
        # 104
        "Améliorer la sécurité routière pour les piétons et les cyclistes aux allées du Parc.",
    ],
    "quartiers-prioritaires": [
        # 77
        "Lancer une étude pour améliorer la qualité de l'eau du lac Kir.",
        # 26
        "Investir pour poursuivre l'amélioration de la qualité de l'eau distribuée.",
    ],

    # ── SOLIDARITÉ ────────────────────────────────────────────────────────
    "aide-sociale": [
        # 55
        "Soutenir les familles, dans toute leur diversité, face aux difficultés de la vie quotidienne.",
    ],
    "egalite-discriminations": [
        # 64
        "Lutter contre toutes les formes de discriminations dans le respect de la laïcité.",
    ],
    "pouvoir-achat": [
        # 1 (already in transparence, but the core purchasing power ones below)
        # 6
        "Maintenir un prix de l'eau juste et consolider la gestion du service public de l'eau.",
        # 7
        "Maintenir la gratuité des bibliothèques et des musées.",
        # 8
        "Préserver la tarification progressive des services publics municipaux adaptée aux revenus.",
    ],
}


def main():
    json_path = os.path.join(ROOT_DIR, "data", "elections", "dijon-2026.json")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Compter les mesures totales pour vérification
    total_mesures = sum(len(v) for v in PROPOSITIONS.values())
    print(f"Nombre total de mesures à injecter : {total_mesures}")
    print(f"Sous-thèmes touchés : {len(PROPOSITIONS)}")

    # Parcourir toutes les catégories et sous-thèmes
    updated = 0
    set_null = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in PROPOSITIONS:
                st["propositions"]["koenders"] = {
                    "source": SOURCE,
                    "sourceUrl": SOURCE_URL,
                    "mesures": PROPOSITIONS[st_id],
                }
                updated += 1
                print(f"  [OK] {st_id} : {len(PROPOSITIONS[st_id])} mesures")
            else:
                # Sous-thème sans proposition Koenders → mettre à null
                st["propositions"]["koenders"] = None
                set_null += 1
                print(f"  [--] {st_id} : aucune mesure (null)")

    print(f"\nSous-thèmes mis à jour : {updated}")
    print(f"Sous-thèmes mis à null  : {set_null}")
    print(f"Total sous-thèmes       : {updated + set_null}")

    # Sauvegarder
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nFichier sauvegardé : {json_path}")


if __name__ == "__main__":
    main()
