#!/usr/bin/env python3
"""Intégrer le programme complet de Charles Compagnon (Rennes) — PDF 6 pages."""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "elections")
FICHIER = os.path.join(DATA_DIR, "rennes-2026.json")

SOURCE = "Programme « Vivre Rennes ! » (PDF officiel, février 2026)"
SOURCE_URL = "https://vivre-rennes.fr/wp-content/uploads/2026/02/VIVRE-RENNES-AVEC-CHARLES-COMPAGNON-Notre-programme-web.pdf"

PROPOSITIONS = {
    "securite": {
        "police-municipale": "Doublement des effectifs de la police municipale avec présence 24h/24 dans tous les quartiers, armement et formation renforcée. Création de 4 commissariats de proximité (Maurepas, Villejean, Cleunay, Le Blosne). Création d'une police métropolitaine des transports (métro, bus, trambus).",
        "videoprotection": "Triplement des caméras de vidéoprotection avec opérateurs dédiés. Éclairage nocturne renforcé et expérimentation de systèmes d'éclairage intelligent (détection de mouvement).",
        "prevention-mediation": "Brigade de prévention et de médiation déployée dans les logements sociaux en lien avec les bailleurs. Lutte ciblée contre les trafics dans les halls et parkings. Agents de quartier clairement identifiés et présents.",
    },
    "transports": {
        "transports-en-commun": "Études pour prolonger le métro au-delà de la rocade (aéroport, parc-expo, Ker Lann). Lignes de trambus vers Bruz, Pacé, Liffré, Châteaugiron avec parkings relais en périphérie. Relance du RER métropolitain. Métro et bus jusqu'à 3h du matin le week-end. Bus circulaire de première couronne. Navettes fluviales sur la Vilaine.",
        "velo-mobilites-douces": "Mise en œuvre d'un plan vélo sécurisé et apaisé dans toute la ville.",
        "pietons-circulation": "Opération SARA (Sainte-Anne et République Apaisées) : espaces sûrs, propres et accueillants dans le centre-ville.",
        "stationnement": "Surélévation du parking Kléber (+120 places) et végétalisation. Création d'un stationnement résident pour la 2e voiture. Pass pro stationnement pour les commerçants et professions libérales.",
        "tarifs-gratuite": "Gratuité des transports en commun lors des temps forts commerciaux et culturels (soldes, Noël, etc.).",
    },
    "logement": {
        "logement-social": "Réserver un logement sur trois aux actifs travaillant à Rennes. Logements accessibles pour les actifs et les classes moyennes.",
        "logements-vacants": "Priorité à la réhabilitation et au recyclage urbain avant toute extension de la ville. Fin de la bétonisation brutale et des projets imposés sans concertation.",
        "encadrement-loyers": "Révision des règles d'urbanisme (PLUi et PLH) pour mieux organiser la construction et le logement sur le territoire.",
        "acces-logement": "Développement massif du Bail Réel Solidaire pour réduire durablement le coût du foncier. Plan logement étudiant en partenariat avec le CROUS et les bailleurs.",
    },
    "education": {
        "petite-enfance": "Augmenter de 30 % les capacités d'accueil de la petite enfance sur le mandat. Développement de crèches aux horaires élargis (soir, week-end) pour les familles aux horaires atypiques.",
        "jeunesse": "Création d'un Conseil municipal de la jeunesse doté d'un véritable pouvoir de proposition. Déploiement de tiers-lieux jeunesse dans les quartiers. Extension de la Carte Sortir aux étudiants boursiers échelon 1 et 0 bis.",
        "periscolaire-loisirs": "Organisation du « Temps des enfants » : redonner la parole aux familles sur l'organisation du périscolaire et des loisirs.",
    },
    "environnement": {
        "espaces-verts": "Moratoire sur l'abattage des arbres. Création d'un îlot de fraîcheur par quartier. Végétalisation massive des cours d'école, des parkings et des trottoirs.",
        "proprete-dechets": "Opération choc de propreté dès le début du mandat. Tolérance zéro pour les dégradations et dépôts sauvages. Rétablissement du ramassage des déchets verts. Arrêtés anti-tags avec nettoyage immédiat des dégradations.",
        "climat-adaptation": "Construction d'une usine de méthanisation métropolitaine (biogaz).",
        "renovation-energetique": "Plan de rénovation énergétique des bâtiments municipaux. Mise en place d'un réseau de réemploi (recyclerie) près des écoles.",
    },
    "sante": {
        "centres-sante": "Ouverture de maisons de santé et de solidarité dans les quartiers prioritaires.",
        "prevention-sante": "Déploiement du programme « Rennes bouge pour sa santé » : activités physiques adaptées, alimentation durable, prévention des addictions.",
    },
    "democratie": {
        "budget-participatif": "Budget participatif par quartier. Référendums populaires locaux sur les grands projets.",
        "transparence": "Aucune hausse d'impôts sur le mandat, des priorités claires et évaluées. Concerter avant de décider, pas après. Charte de la construction et de la citoyenneté rendue opposable juridiquement.",
        "vie-associative": "Rénovation et extension de la Maison des associations. Budget global maintenu, subventions attribuées en fonction de l'utilité locale et du respect des valeurs républicaines.",
        "services-publics": "Décider au plus près des quartiers (subsidiarité, conseils de quartier renforcés). Redonner la parole aux Rennais sur les décisions structurantes.",
    },
    "economie": {
        "commerce-local": "Plan « Quartiers vivants » pour le commerce. Centre-ville et quartiers commerçants vivants et attractifs.",
        "emploi-insertion": "Plan local d'insertion pour les jeunes et les seniors. Renforcement des liens entreprises/formation/alternance. Soutien aux structures de l'économie sociale et solidaire. Création d'un permis de conduire civique pour faciliter l'accès à l'emploi.",
        "attractivite": "Création d'un fonds d'innovation et de transition économique. Relocalisation industrielle ciblée (objectif : 10 000 emplois en 6 ans). Création d'une maison citoyenne de l'Intelligence Artificielle.",
    },
    "culture": {
        "equipements-culturels": "Construction d'un Zénith (12 000 à 15 000 places), équipement métropolitain structurant. Soutien au projet de musée de la Justice sur le site de la prison Jacques Cartier.",
        "evenements-creation": "Candidature de Rennes au titre de Capitale européenne de la culture. Soutien renforcé à la création artistique locale. Développement du tourisme urbain et culturel. Ouverture d'une antenne de l'office de tourisme près de la gare.",
    },
    "sport": {
        "equipements-sportifs": "Construction d'un nouveau stade Roazhon Park II financé par le propriétaire du Stade Rennais. Roazhon Park I consacré au rugby et aux pratiques sportives féminines. Installation de bassins de natation mobiles et extension des horaires des piscines. Rénovation et modernisation des équipements sportifs existants.",
        "sport-pour-tous": "Développement du sport pour tous, du handisport et du sport inclusif. Première licence sportive gratuite pour les enfants de 6 ans.",
    },
    "urbanisme": {
        "amenagement-urbain": "Moratoire sur la construction d'immeubles de grande hauteur dans les quartiers pavillonnaires. Respect du cadre de vie existant. Création de comités locaux d'urbanisme avec droit d'initiative citoyenne.",
        "accessibilite": "Amélioration de l'accessibilité pour les personnes âgées et en situation de handicap dans les transports et espaces publics.",
        "quartiers-prioritaires": "Création d'un quartier des stades autour de la route de Lorient. Parkings relais en périphérie connectés aux quartiers rennais.",
    },
}


def main():
    with open(FICHIER, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Mettre à jour le candidat
    for c in data["candidats"]:
        if c["id"] == "compagnon":
            c["liste"] = "Vivre Rennes ! (Union centre, droite et société civile)"
            c["programmeUrl"] = "https://vivre-rennes.fr/"
            c["programmeComplet"] = True
            c["programmePdfPath"] = "compagnon-rennes-programme.pdf"
            c["soutiens"] = "Horizons, Renaissance, MoDem, UDI, Parti Breton, Nouvelle Énergie, Démocrates et Progressistes, Démocrates pour la Planète"
            break

    # 2. Insérer les propositions
    count = 0
    for cat in data["categories"]:
        cat_props = PROPOSITIONS.get(cat["id"], {})
        for st in cat["sousThemes"]:
            texte = cat_props.get(st["id"])
            if texte:
                st["propositions"]["compagnon"] = {
                    "texte": texte,
                    "source": SOURCE,
                    "sourceUrl": SOURCE_URL,
                }
                count += 1

    # 3. Écrire
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"OK - {count} propositions inserees pour Compagnon (Rennes)")
    print(f"  programmeComplet: true")
    print(f"  Liste: Vivre Rennes ! (Union centre, droite et societe civile)")


if __name__ == "__main__":
    main()
