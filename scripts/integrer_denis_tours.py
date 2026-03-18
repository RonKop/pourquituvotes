#!/usr/bin/env python3
"""Intègre le programme complet d'Emmanuel Denis dans tours-2026.json."""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = r"C:\Users\KOPELMANRon\projets perso\FR comp mun\data\elections\tours-2026.json"

SOURCE = "Programme Tours Inspire 2026"
SOURCE_URL = "https://toursinspire2026.fr"

# Mapping: sous-theme ID -> liste de mesures
PROPS = {
    # SÉCURITÉ
    "prevention-mediation": [
        "Rues apaisées, végétalisées, plus accueillantes avec ombre et bancs",
        "Recul de l'accidentologie routière",
    ],
    # TRANSPORTS
    "transports-en-commun": [
        "Création des lignes 2 et 2bis du tramway",
        "Service express régional métropolitain (SERM) avec gare place Verdun",
        "Nouvelles offres de bus",
    ],
    "velo-mobilites-douces": [
        "Poursuite du réseau cyclable Vélival",
    ],
    "pietons-circulation": [
        "Extension de la zone piétonne du Vieux-Tours",
        "Aménager des rues plus fraîches et plus sûres pour toutes les générations",
        "Apaisement piéton des cœurs de quartier",
    ],
    "stationnement": [
        "Baisse des tarifs des parkings souterrains",
    ],
    "tarifs-gratuite": [
        "Gratuité des transports tous les samedis (maintien)",
        "Gratuité des transports jusqu'à 11 ans (maintien)",
    ],
    # LOGEMENT
    "logement-social": [
        "Urbanisation des Casernes (dont logements sociaux)",
    ],
    # ÉDUCATION
    "petite-enfance": [
        "Prioriser l'accès aux crèches pour familles monoparentales",
    ],
    "ecoles-renovation": [
        "Rénovation et reconstruction des écoles Kléber, Curie, Rimbaud, Bastié, Mermoz, Vigny-Musset, Maupassant-Montjoyeux, Daudet, Mistral, Hugo et Flaubert",
    ],
    "cantines-fournitures": [
        "Restauration scolaire bio et de qualité via la nouvelle cuisine centrale",
    ],
    "periscolaire-loisirs": [
        "Éducation artistique et culturelle dans les écoles",
        "Penser la ville à hauteur d'enfants",
    ],
    # ENVIRONNEMENT
    "espaces-verts": [
        "Planter massivement des arbres (suite des 50 000 arbres depuis 2020)",
        "10 places végétalisées et apaisées",
        "Création d'un nouveau parc à Tours Nord et Saint-Éloi, vallon de Chatenay",
        "Embellissement de la place Velpeau, placettes du quartier Colbert",
        "Parc naturel métropolitain ligérien autour de la Loire et du Cher",
        "Aires de baignade, extension de Tours sur Loire sur l'île Balzac",
    ],
    "proprete-dechets": [
        "Gestion publique de l'eau",
        "Plans de sobriété énergétique et d'économie d'eau",
    ],
    "climat-adaptation": [
        "Amélioration durable de la qualité de l'air",
        "Lutte contre les perturbateurs endocriniens",
    ],
    "renovation-energetique": [
        "Investir dans les énergies propres et durables",
    ],
    "alimentation-durable": [
        "Ferme urbaine municipale au nord de la Cousinerie pour la cuisine centrale",
    ],
    # SANTÉ
    "centres-sante": [
        "Développer des quartiers en santé pour réduire les inégalités d'accès aux soins",
        "Centres et maisons de santé dans les quartiers",
    ],
    "prevention-sante": [
        "Prévention des cancers",
    ],
    "seniors": [
        "Renforcer le maintien à domicile des aînés",
        "Soutien concret aux aidants",
        "Mobilités adaptées et espaces publics plus accessibles pour les aînés",
    ],
    # DÉMOCRATIE
    "budget-participatif": [
        "Démocratie active associant réellement les habitants aux décisions",
        "Reconnaissance de l'expertise citoyenne",
    ],
    "transparence": [
        "Débat, transparence et partage du pouvoir d'agir",
        "Tours ville refuge pour le pluralisme",
        "Laïcité garantissant liberté de conscience et égalité",
    ],
    # ÉCONOMIE
    "commerce-local": [
        "Préserver et renforcer les commerces de proximité avec les foncières commerce",
        "Créer un office du commerce (animations, aide vitrines, soutien associations commerçants, enseignes éthiques)",
        "Relier et renforcer le centre-ville commerçant (Saint-Gatien, les Halles, haut de la Tranchée)",
        "Améliorer l'identité commerçante des quartiers hors centre",
    ],
    "emploi-insertion": [
        "Soutenir les filières locales non délocalisables : santé, alimentation, mobilité décarbonée, réemploi, artisanat",
        "Développer l'économie circulaire et l'insertion (emplois locaux, ESAT hors les murs)",
    ],
    "attractivite": [
        "Soutenir l'université : innovation issue de la recherche, programme d'incubation",
        "Améliorer l'accueil des étudiants et chercheurs étrangers",
    ],
    # CULTURE
    "equipements-culturels": [
        "Carré des musées avec centre d'exposition du Château",
        "Nouvelle Cité des paysages (muséum d'histoire naturelle + Centre d'interprétation architecture/paysage)",
    ],
    "evenements-creation": [
        "Résidences annuelles d'artistes dans les quartiers",
        "Soutenir les pratiques amateurs et associatives (sport et culture)",
        "Investir l'espace public pour la culture",
    ],
    # SPORT
    "equipements-sportifs": [
        "Skatepark des Fontaines",
        "Gymnases de la Rotonde, du Hallebardier, des Deux-Lions et des Casernes",
        "Piscine des Tourettes",
        "Aires de fitness de plein air",
        "Doublement des investissements sportifs",
    ],
    # URBANISME
    "amenagement-urbain": [
        "Concours international pour l'îlot Vinci / Blaise-Pascal",
        "Urbanisation des hauts de la Tranchée et de Sainte-Radegonde",
        "Carrefour de la Marne",
        "Construire un modèle de ville sobre",
        "Programme d'investissements ambitieux (tramway, SERM)",
        "Maîtriser le foncier urbain pour besoins productifs et souveraineté économique",
        "Organiser la logistique urbaine et livraison du dernier kilomètre",
        "Outils numériques publics responsables, souveraineté face aux GAFAM/IA",
    ],
    "quartiers-prioritaires": [
        "Poursuite du renouvellement urbain du Sanitas",
    ],
    # SOLIDARITÉ
    "aide-sociale": [
        "Créer des lieux de répit et d'entraide pour familles monoparentales",
    ],
}

# Comptage
total = sum(len(v) for v in PROPS.values())
print(f"Total mesures à intégrer : {total}")

with open(FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Mettre à jour le candidat denis
for c in data["candidats"]:
    if c["id"] == "denis":
        c["programmeComplet"] = True
        c["programmeUrl"] = SOURCE_URL
        c["siteCampagne"] = SOURCE_URL
        print(f"Candidat mis à jour : {c['nom']} -> programmeComplet=True")
        break

# 2. Injecter les propositions dans chaque sous-thème
updated_count = 0
for cat in data["categories"]:
    for st in cat["sousThemes"]:
        st_id = st["id"]
        if st_id in PROPS:
            st["propositions"]["denis"] = {
                "source": SOURCE,
                "sourceUrl": SOURCE_URL,
                "mesures": PROPS[st_id],
            }
            updated_count += 1
            print(f"  {cat['id']}/{st_id} : {len(PROPS[st_id])} mesures")
        # Si pas dans PROPS et actuellement null ou ancien contenu partiel de presse,
        # on laisse null (pas de mesure pour ce sous-thème)

print(f"\nSous-thèmes mis à jour : {updated_count}")
print(f"Sous-thèmes sans mesure Denis : {44 - updated_count}")

# Vérifier qu'on n'a pas de clé orpheline
schema_ids = set()
for cat in data["categories"]:
    for st in cat["sousThemes"]:
        schema_ids.add(st["id"])

orphans = set(PROPS.keys()) - schema_ids
if orphans:
    print(f"ERREUR : sous-thèmes inconnus dans PROPS : {orphans}")
    sys.exit(1)

with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\nFichier écrit avec succès.")
