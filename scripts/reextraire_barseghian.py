#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ré-extraction des propositions de Jeanne Barseghian (Strasbourg 2026)."""
import io, json, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "strasbourg-2026.json")
SOURCE = "Programme officiel 2026 — Jeanne Barseghian"
SOURCE_URL = "https://pokaa.fr/2026/01/07/municipales-2026-jeanne-barseghian-devoile-12-mesures-pour-etre-reelue-maire/"
CANDIDAT_ID = "barseghian"

MESURES = {
    # === SÉCURITÉ ===
    "prevention-mediation": [
        "Créer un centre-ressource de médiation et justice restaurative pour la prise en charge des conflits, du harcèlement, des violences sexistes et sexuelles, la prévention de la récidive et la réparation.",
        "Nommer un médiateur municipal indépendant, gratuit et accessible, pour faciliter le dialogue entre habitants et administration.",
    ],
    "violences-femmes": [
        "Lancer une campagne municipale gratuite de dépistage de l'endométriose dès 14 ans, en partenariat avec le CMCO, avec test salivaire et orientation rapide vers un suivi médical.",
    ],

    # === TRANSPORTS ===
    "transports-en-commun": [
        "Poursuivre l'extension du tramway vers le nord de Strasbourg (tram Nord vers Schiltigheim et Bischheim).",
        "Mettre en place un service de bus 24h/24 pour les quartiers mal desservis, avec arrêts à la demande, pour un coût estimé à 1 million d'euros par an.",
        "Renforcer l'offre de transports en soirée et la nuit pour répondre aux besoins des travailleurs de nuit, étudiants et personnel hospitalier.",
    ],
    "velo-mobilites-douces": [
        "Installer des stationnements vélo sécurisés dans tous les quartiers, y compris près des gares, parkings-silos et résidences sociales.",
        "Installer 3 000 places de stationnement vélo sécurisées sous la gare centrale.",
        "Étendre Vélhop avec retour gratuit des vélos sur tout le territoire.",
    ],
    "pietons-circulation": [
        "Instaurer progressivement la limitation à 30 km/h dans toute la ville, hors axes structurants majeurs.",
        "Poursuivre l'objectif Vision Zéro : zéro mort et zéro accident grave, avec tolérance zéro sur les comportements dangereux tous modes confondus.",
        "Créer une brigade piétonne de la police municipale pour cibler les cyclistes dangereux et protéger les piétons.",
        "Généraliser les rues scolaires (28 rues scolaires créées, avec réservation aux mobilités actives aux horaires d'entrée et sortie).",
    ],
    "stationnement": [
        "Instaurer une tarification solidaire et progressive du stationnement résident : de 5 € à 40 € par mois selon les revenus des ménages.",
    ],
    "tarifs-gratuite": [
        "Financer le service de bus de nuit 24h/24, estimé à 1 million d'euros par an, pour garantir l'accès aux transports à toute heure.",
    ],

    # === LOGEMENT ===
    "encadrement-loyers": [
        "Encadrer les loyers commerciaux pour protéger la diversité des commerces de proximité et lutter contre la vacance commerciale.",
        "Poursuivre l'encadrement des loyers résidentiels pour garantir des logements abordables.",
    ],
    "logement-social": [
        "Poursuivre la construction de logements sociaux (6 500 créés lors du premier mandat) pour résorber la liste d'attente de plus de 30 000 demandeurs.",
        "Développer l'habitat participatif avec le plus grand quartier en habitat participatif de France à l'horizon 2030.",
    ],

    # === ÉDUCATION ===
    "ecoles-renovation": [
        "Poursuivre la végétalisation des cours d'école (70 % végétalisées lors du premier mandat sur 140 établissements).",
        "Investir 810 millions d'euros sur le mandat pour l'éducation et la rénovation énergétique des bâtiments publics.",
    ],
    "cantines-fournitures": [
        "Atteindre 75 % de produits bio dans les cantines scolaires (contre 53 % actuellement).",
        "Réduire les portions de viande dans les cantines en cohérence avec le Traité Plant Based.",
        "Créer des cuisines municipales centrales pour préparer les repas sur place dans les écoles, crèches et EHPAD.",
    ],

    # === ENVIRONNEMENT ===
    "espaces-verts": [
        "Appliquer la règle 3-30-300 : chaque habitant voit 3 arbres de chez lui, vit dans un quartier à 30 % de canopée, et à moins de 300 m d'un parc.",
        "Créer de nouveaux parcs à Hautepierre, Plaine Élan (Neuhof), Cronenbourg et sur le site industriel du Schluthfeld.",
        "Développer des corridors de fraîcheur urbains dans toute la ville.",
    ],
    "proprete-dechets": [
        "Renforcer la propreté urbaine et la lutte contre les dépôts sauvages.",
    ],
    "climat-adaptation": [
        "Accélérer le verdissement de la ville avec des rues plus vertes et plus fraîches pour adapter Strasbourg au changement climatique.",
        "Créer une Maison de l'écologie populaire pour former les habitants des quartiers populaires aux enjeux climatiques et réduire les inégalités face aux îlots de chaleur.",
    ],
    "renovation-energetique": [
        "Renforcer la souveraineté énergétique en étendant et densifiant les réseaux de chaleur urbains (40 000 logements raccordés, 12 000 de plus qu'en 2020).",
        "Garantir des prix stables de l'énergie grâce au développement des énergies locales.",
    ],
    "alimentation-durable": [
        "Ouvrir des cantines de quartier proposant des repas abordables et de qualité pour renforcer le lien social et lutter contre l'isolement.",
        "Soutenir les supermarchés coopératifs et les coopératives alimentaires offrant des produits de qualité à prix maîtrisés.",
        "Renforcer le soutien aux épiceries solidaires et aux associations facilitant l'accès à une alimentation saine pour les populations vulnérables.",
        "Poursuivre l'expérimentation de la sécurité alimentaire pour tous.",
        "Développer l'agriculture urbaine sur le territoire strasbourgeois.",
    ],

    # === SANTÉ ===
    "prevention-sante": [
        "Lancer une campagne municipale de dépistage gratuit de l'endométriose dès 14 ans.",
        "Proposer des cours de sport gratuits et encadrés en plein air, avec accent sur le sport féminin et le sport adapté.",
    ],
    "seniors": [
        "Créer un Conseil des seniors, sur le modèle du Conseil des jeunes, pour associer les aînés aux décisions municipales les concernant.",
    ],
    "animaux-compagnie": [
        "Ouvrir un dispensaire vétérinaire municipal offrant des soins à tarif accessible quel que soit le revenu, pour lutter contre l'abandon des animaux.",
    ],

    # === DÉMOCRATIE ===
    "budget-participatif": [
        "Renforcer les budgets et pouvoirs des élus de quartier avec des permanences régulières et des Stammtisch mensuels.",
        "Créer des assemblées de quartier réformées avec tirage au sort de résidents pour assurer la diversité de la participation.",
        "Organiser des ateliers de conception urbaine pour les grands projets (Place de l'Homme de Fer, Parc de Haguenau, Place de Bordeaux).",
    ],
    "transparence": [
        "Instaurer un droit de pétition citoyenne : 5 % des inscrits (environ 7 400 signatures) déclenche une convention citoyenne, 10 % déclenche un vote citoyen local.",
        "Élargir le droit de vote aux résidents dès 16 ans et aux résidents étrangers pour les consultations locales.",
        "Organiser des conventions citoyennes sur les enjeux majeurs, dont l'incinérateur Sénerval.",
    ],

    # === ÉCONOMIE ===
    "commerce-local": [
        "Réduire la vacance commerciale (passée de 6,5 % à 5,3 %) en régulant les loyers commerciaux pour préserver la diversité des boutiques.",
        "Créer des espaces dédiés aux artisans avec des ateliers adaptés dans différents quartiers.",
    ],
    "emploi-insertion": [
        "Accélérer le développement de l'économie sociale et solidaire en renforçant le soutien municipal aux entreprises qui réinvestissent localement.",
        "Cibler l'accompagnement vers l'emploi des jeunes, des femmes et des migrants.",
        "Sanctuariser les zones d'activité économique stratégiques pour empêcher la spéculation foncière et maintenir la capacité productive.",
    ],
    "attractivite": [
        "Créer des aires de repos pour les livreurs et soutenir le développement d'applications de livraison locales.",
    ],

    # === CULTURE ===
    "equipements-culturels": [
        "Construire la médiathèque du Rhin au port, dans l'ancienne Cour des Douanes : équipement culturel franco-allemand de 20 000 m² pour un investissement de 15 millions d'euros.",
    ],
    "evenements-creation": [
        "Aménager un site permanent de 40 000 m² pour la Foire Saint-Jean à la Plaine des Bouchers (approbation début 2026, livraison visée 2027).",
    ],

    # === SPORT ===
    "sport-pour-tous": [
        "Proposer des cours de sport gratuits et encadrés en plein air dans les parcs, avec accent sur le sport féminin et le sport adapté.",
        "Instaurer des créneaux spécifiques dans les équipements sportifs pour les personnes en situation de handicap.",
        "Renforcer le soutien financier aux associations spécialisées et former des éducateurs au para-sport.",
    ],

    # === URBANISME ===
    "amenagement-urbain": [
        "Repenser l'espace public en donnant la priorité aux piétons dans la conception urbaine.",
        "Poursuivre la transformation de la gare de Strasbourg (projet Gare à 360 degrés).",
    ],
    "accessibilite": [
        "Créer un Conseil de l'accessibilité pour intégrer la question du handicap dans tous les projets municipaux futurs, avec visites de chantiers pour les personnes concernées.",
    ],
    "quartiers-prioritaires": [
        "Créer une Maison de l'écologie populaire dans les quartiers prioritaires pour former les habitants et réduire les inégalités climatiques.",
    ],

    # === SOLIDARITÉ ===
    "aide-sociale": [
        "Garantir à chacun l'accès effectif à une alimentation saine, durable et abordable tout en soutenant l'agriculture locale créatrice d'emplois.",
        "Développer un programme de vacances accessibles pour tous les enfants via les centres socioculturels.",
    ],
    "egalite-discriminations": [
        "Mettre en place un plan zéro discrimination avec un Observatoire local des discriminations, un baromètre annuel et des recommandations pour améliorer la lutte contre le sexisme, le racisme, l'antisémitisme et les LGBTIphobies.",
        "Renforcer les mesures anti-discrimination dans les recrutements municipaux.",
    ],
    "pouvoir-achat": [
        "Instaurer une tarification solidaire et progressive du stationnement résident de 5 € à 40 € par mois selon les revenus.",
    ],
}

def main():
    print("=" * 60)
    print(f"  RÉ-EXTRACTION {CANDIDAT_ID.upper()} (Strasbourg)")
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
