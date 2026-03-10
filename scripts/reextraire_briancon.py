#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ré-extraction des mesures de François Briançon (Toulouse 2026)
Source : vivremieuxtoulouse.fr/programme-en-bref/ + programme complet
"""
import io, json, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "toulouse-2026.json")
SOURCE = "Programme officiel 2026 — François Briançon"
SOURCE_URL = "https://vivremieuxtoulouse.fr/programme-en-bref/"
CANDIDAT_ID = "briancon"

MESURES = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Présence de police municipale de proximité dans tous les quartiers, avec un objectif d'un agent pour 1 000 habitants.",
        "Plan « Stop les deals » combinant sécurité, prévention, santé et cohésion sociale.",
        "Plan de réduction des nuisances sonores et de prévention des vols nocturnes.",
    ],
    "prevention-mediation": [
        "Création d'un service de médiation urbaine et de tranquillité publique.",
    ],
    "violences-femmes": [
        "Programme de lutte contre les violences sexistes et sexuelles dans l'espace public.",
    ],

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Augmentation de 20 % de la capacité des transports en commun en trois ans.",
        "Déploiement du Service Express Régional Métropolitain (SERM/RER) entre 2028 et 2040, budget de 4,8 milliards d'euros.",
        "Renforcement du réseau Linéo et bus avec plus de fréquence et de meilleures amplitudes horaires.",
        "Abandon du projet Jonction Est au profit d'alternatives de transport collectif.",
    ],
    "velo-mobilites-douces": [
        "Plan d'infrastructures cyclables avec éducation au vélo et espaces partagés.",
        "Plan de mobilité neutre en carbone à l'horizon 2050.",
    ],
    "pietons-circulation": [
        "Ville à hauteur d'enfants : rues plus calmes, zones piétonnes aux abords des écoles.",
        "Plan de mise en accessibilité des trottoirs pour les personnes en situation de handicap.",
    ],
    "stationnement": [
        "Tarification sociale et écologique du stationnement.",
        "Reprise en gestion publique des parkings actuellement concédés au privé.",
    ],
    "tarifs-gratuite": [
        "Gratuité des transports en commun pour les mineurs et les étudiants boursiers.",
        "Abonnement à 10 euros par mois pour les moins de 26 ans.",
        "Tarification solidaire des transports basée sur les revenus à partir de 2027.",
        "Gratuité des transports pour les moins de 18 ans.",
    ],

    # ── LOGEMENT ──
    "logement-social": [
        "Construction de 15 000 logements à loyers modérés sur le mandat.",
        "7 500 logements en accession sociale via le Bail Réel Solidaire (BRS) sur la métropole.",
        "500 logements de transition pour les personnes en situation de vulnérabilité.",
    ],
    "logements-vacants": [
        "Réduction de la durée de location autorisée des meublés touristiques de 120 à 90 jours par an.",
    ],
    "encadrement-loyers": [
        "Candidature auprès de l'État pour expérimenter l'encadrement des loyers à Toulouse dès fin 2026.",
    ],
    "acces-logement": [
        "Rénovation massive de 30 000 logements sur le mandat.",
        "Aide aux primo-accédants : cautions et aides à l'installation.",
        "Garantie zéro enfant à la rue : hébergement, repas et scolarisation assurés.",
    ],

    # ── ÉDUCATION ──
    "petite-enfance": [
        "Création de 1 000 places de crèche supplémentaires sur le mandat, avec priorité aux quartiers sous-dotés.",
        "Système d'attribution des places en crèche transparent et équitable.",
        "Renforcement de l'accompagnement des enfants en situation de handicap (personnel supplémentaire, coordination avec les familles).",
    ],
    "ecoles-renovation": [
        "Plan pluriannuel de rénovation des écoles adapté au changement climatique.",
        "Généralisation des cours oasis végétalisées dans chaque école.",
        "Un ATSEM par classe de maternelle sur tout le temps scolaire.",
    ],
    "cantines-fournitures": [
        "Gratuité des cantines scolaires pour les familles gagnant moins de 2 000 euros par mois.",
        "Goûter quotidien gratuit et équilibré dans les écoles, avec option végétarienne.",
        "Sortie culturelle ou artistique trimestrielle pour tous les élèves.",
    ],
    "periscolaire-loisirs": [
        "Tarification solidaire de l'ensemble des services municipaux selon les revenus des familles.",
    ],
    "jeunesse": [
        "Reconnaissance des droits des familles monoparentales dans l'accès aux services municipaux.",
        "Confirmation du hub Toulouse Culture Sourde.",
    ],

    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Toulouse ville-jardin : 3 arbres visibles depuis chaque logement, 30 % de couverture végétale par quartier, un espace vert à moins de 300 mètres de chaque habitation.",
        "Création d'un parc de 100 hectares à l'est de Toulouse.",
        "Développement d'une ceinture verte autour de la ville.",
        "Projet Étoile Verte : réaménagement paysager des boulevards, canaux et voies de pénétration.",
    ],
    "proprete-dechets": [
        "Service de propreté uniforme sur l'ensemble du territoire municipal.",
    ],
    "climat-adaptation": [
        "Programme « sols vivants » : désimperméabilisation de 300 000 m² de surfaces minéralisées.",
        "Végétalisation massive et équitable pour lutter contre les îlots de chaleur.",
        "Bouclier « santé-environnement » pour les établissements sensibles (crèches, écoles, centres de soins).",
    ],
    "renovation-energetique": [
        "Rénovation énergétique de 30 000 logements sur la durée du mandat.",
    ],
    "alimentation-durable": [
        "Prescriptions vertes : distribution de paniers bio gratuits pour les femmes enceintes.",
        "Programme de soutien à la sécurité alimentaire pour les familles en difficulté.",
        "Ticket transport pour les animaux de compagnie dans les transports en commun (laisse et muselière obligatoires).",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Création de centres de santé municipaux pour lutter contre les déserts médicaux.",
        "Plan municipal de santé mentale.",
        "Programme de santé scolaire dans les établissements.",
    ],
    "prevention-sante": [
        "Tarification progressive et écologique de l'eau avec retour en régie publique.",
    ],
    "seniors": [
        "Plan « Mieux Vieillir » de lutte contre l'isolement des personnes âgées.",
        "Accompagnement humain et solidaire des aînés dans tous les quartiers.",
    ],

    # ── DÉMOCRATIE ──
    "budget-participatif": [
        "Assemblée citoyenne de l'urgence climatique dotée de pouvoirs de proposition, suivi et contrôle.",
        "Assises de la « Démocratie Vivante » pour évaluer et améliorer la participation citoyenne.",
        "Fabrique Toulouse en continu : co-construction citoyenne permanente sur les grands projets.",
    ],
    "transparence": [
        "Code d'éthique et d'intégrité pour restaurer la confiance et lutter contre la corruption.",
        "Droit d'initiative citoyenne : examen municipal obligatoire des propositions soutenues par les habitants.",
    ],
    "vie-associative": [
        "Plan de soutien aux associations et aux services publics locaux.",
        "Observatoire local de la laïcité pour accompagner les situations sensibles et faire la pédagogie de la loi de 1905.",
        "Formation des élus et des agents municipaux à la laïcité.",
    ],
    "services-publics": [
        "Retour en régie municipale de la gestion de l'eau et de l'assainissement.",
        "Centre populaire de la biosphère pour l'éducation au climat et à la biodiversité, accueillant des associations.",
    ],

    # ── ÉCONOMIE ──
    "commerce-local": [
        "Soutien aux commerces et artisans de proximité dans les quartiers.",
    ],
    "emploi-insertion": [
        "Soutien à l'économie sociale et solidaire.",
    ],
    "attractivite": [
        "Soutien au secteur aéronautique et spatial toulousain.",
        "Diversification économique : santé, robotique, intelligence artificielle, cybersécurité, biotechnologies, énergies renouvelables.",
        "Création de « Campus du Futur » : pôles stratégiques d'innovation.",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Création de la Villa Tolosa, lieu de création artistique contemporaine accueillant artistes locaux et internationaux.",
        "Gratuité totale et maintien des horaires d'ouverture des bibliothèques municipales.",
        "Accès à la pratique artistique sur l'ensemble du territoire : possibilité d'une pratique hebdomadaire pour chaque habitant.",
    ],
    "evenements-creation": [
        "Valorisation des cultures urbaines : street art, fresques, hip-hop, rap.",
        "Plan ambitieux de développement de la langue et de la culture occitanes, en coordination avec les associations.",
        "Jumelages entre Toulouse et des villes partenaires (culturels, universitaires, économiques), dont création d'un jumelage avec une ville du Maghreb.",
        "Prix annuel « Toulouse Féministe » récompensant les initiatives d'égalité dans les domaines civique, culturel, sportif et économique.",
    ],

    # ── SPORT ──
    "equipements-sportifs": [
        "Ligue de quartier : tournois inter-écoles avec parrainage d'athlètes professionnels.",
    ],
    "sport-pour-tous": [
        "Plan de pratique sportive féminine avec budgets genrés et mentorat professionnel.",
        "Pass'Sport Toulouse : subvention à la licence sportive pour les familles modestes.",
    ],

    # ── URBANISME ──
    "amenagement-urbain": [
        "Suppression de la tarification saisonnière de l'eau pour protéger le pouvoir d'achat des ménages.",
    ],

    # ── SOLIDARITÉ ──
    "aide-sociale": [
        "Tarification solidaire des services municipaux basée sur les revenus des familles.",
    ],
    "egalite-discriminations": [
        "Observatoire anti-discriminations : racisme, antisémitisme, sexisme, LGBTphobies, discriminations d'origine sociale.",
        "Interventions en milieu scolaire et auprès des agents municipaux pour la prévention des discriminations.",
    ],
    "pouvoir-achat": [
        "Suppression de la tarification saisonnière de l'eau pour protéger le pouvoir d'achat des ménages.",
    ],
}

def main():
    print("=" * 60)
    print(f"  RÉ-EXTRACTION {CANDIDAT_ID.upper()} (Toulouse)")
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
                prop = st["propositions"].get(CANDIDAT_ID)
                if prop is None:
                    prop = {}
                    st["propositions"][CANDIDAT_ID] = prop
                old_count = len(prop.get("mesures", []))
                new_mesures = MESURES[st_id]
                if len(new_mesures) >= old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = SOURCE
                    prop["sourceUrl"] = SOURCE_URL
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} -> {len(new_mesures)}")
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"\n    {updated} sous-thèmes mis à jour")
    print("=" * 60)

if __name__ == "__main__":
    main()
