#!/usr/bin/env python3
"""
Intégration du programme de Lambert Meilhac (Toulouse) - Site toulouse-nouvel-air.fr
6 thèmes : Hippodrome/forêt, Mobilité, Eau, Alimentation, Urbanisme, Sécurité

Sources :
- https://www.toulouse-nouvel-air.fr/notre-programme/transformer-hippodrome-en-foret-un-projet-emblematique
- https://www.toulouse-nouvel-air.fr/notre-programme/mobilite-fluidifier-le-trafic-et-rendre-l-espace-aux-usagers
- https://www.toulouse-nouvel-air.fr/notre-programme/eau-assurer-qualite-et-disponibilite
- https://www.toulouse-nouvel-air.fr/notre-programme/alimentation
- https://www.toulouse-nouvel-air.fr/notre-programme/urbanisme-stop-au-béton
- https://www.toulouse-nouvel-air.fr/notre-programme/sécurité-la-présence-plutôt-que-la-vidéosurveillance
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "elections")
JSON_PATH = os.path.join(DATA_DIR, "toulouse-2026.json")

CANDIDAT_ID = "meilhac"
SOURCE = "Programme officiel 2026"
SOURCE_URL = "https://www.toulouse-nouvel-air.fr/"

# Metadata updates
METADATA = {
    "programmeComplet": True,
    "programmeUrl": "https://www.toulouse-nouvel-air.fr/",
    "programmePdfPath": None,
}

# Propositions mapped to sub-themes (category_id -> sub_theme_id -> texte)
# Source: site de campagne toulouse-nouvel-air.fr, pages thématiques détaillées
PROPOSITIONS = {
    "securite": {
        "police-municipale": (
            "Réorienter le budget vidéosurveillance vers le recrutement de policiers municipaux "
            "de terrain pour une présence humaine renforcée dans les quartiers."
        ),
        "videoprotection": (
            "Stopper le déploiement massif de caméras de vidéosurveillance : réaffecter les budgets "
            "vers des agents de proximité plutôt que des dispositifs technologiques coûteux et peu efficaces."
        ),
        "prevention-mediation": (
            "Sécurité par la présence humaine plutôt que la vidéosurveillance : favoriser la médiation, "
            "la présence de terrain et le lien social dans tous les quartiers de Toulouse."
        ),
    },
    "transports": {
        "transports-en-commun": (
            "Réduire de 100 000 véhicules la circulation sur l'aire urbaine d'ici la fin du mandat, "
            "en développant les alternatives à la voiture individuelle et les transports en commun."
        ),
        "velo-mobilites-douces": (
            "Développer les infrastructures cyclables et les mobilités douces pour réduire la congestion "
            "automobile, avec des itinéraires sécurisés notamment aux abords des écoles."
        ),
        "pietons-circulation": (
            "Fluidifier le trafic et rendre l'espace aux piétons, cyclistes et transports en commun. "
            "Sécuriser les axes dangereux (avenue de Muret, Saint-Exupéry, Gloriette) pour redonner "
            "aux enfants leur autonomie de déplacement."
        ),
    },
    "logement": {
        "logement-social": (
            "Valoriser et réhabiliter le parc de logements existants plutôt que construire du neuf. "
            "Augmenter l'offre de logements sociaux pour les familles et les personnes en difficulté."
        ),
        "acces-logement": (
            "Priorité à la réhabilitation du parc existant plutôt qu'à la construction neuve : "
            "maîtriser les investissements en valorisant l'existant pour un accès au logement durable."
        ),
    },
    "education": {
        "cantines-fournitures": (
            "Approvisionner les cantines scolaires en légumes ultra-frais produits localement "
            "grâce à la régie municipale agricole de l'hippodrome (200 tonnes/an, "
            "soit 2 à 3 mois de repas pour les cantines scolaires)."
        ),
        "periscolaire-loisirs": (
            "Ouvrir l'espace de l'hippodrome transformé comme lieu d'éducation à la nature "
            "et à la santé pour les écoles, avec des activités périscolaires en plein air."
        ),
    },
    "environnement": {
        "espaces-verts": (
            "Transformer les 34 hectares de l'hippodrome de la Cépière en forêt urbaine : "
            "un îlot de fraîcheur en pleine ville, un espace vert public gratuit accessible à tous, "
            "là où 2 km d'habitations n'ont aujourd'hui aucun espace vert. "
            "Choix finaux soumis à consultation citoyenne."
        ),
        "proprete-dechets": (
            "Améliorer la propreté de la ville et mettre en place une gestion responsable des déchets, "
            "avec un renforcement du tri et du recyclage."
        ),
        "climat-adaptation": (
            "Assurer la qualité et la disponibilité de l'eau face au changement climatique : "
            "investir pour garantir la ressource à long terme alors que le volume disponible "
            "a diminué de 14 % en 15 ans et que les débits d'étiage de la Garonne "
            "pourraient baisser de 50 % d'ici 2050."
        ),
        "alimentation-durable": (
            "Retisser le lien entre citadins et agriculteurs : dédier 10 hectares de l'hippodrome "
            "au maraîchage via une régie municipale agricole (200 tonnes/an, soit 2 millions "
            "de portions de légumes). Développer les circuits courts et l'alimentation durable "
            "pour les cantines et les Toulousains."
        ),
    },
    "sante": {
        "prevention-sante": (
            "Faire de l'hippodrome transformé un lieu d'éducation à la santé : "
            "espaces de nature accessibles gratuitement pour les activités quotidiennes "
            "et le bien-être des habitants."
        ),
    },
    "democratie": {
        "budget-participatif": (
            "Soumettre les choix finaux d'aménagement de l'hippodrome à une consultation citoyenne : "
            "les habitants deviennent acteurs et pas seulement consommateurs des décisions environnementales."
        ),
        "transparence": (
            "Maîtriser les investissements publics et favoriser le dynamisme citoyen : "
            "une gestion pragmatique et responsable des finances municipales, "
            "en valorisant l'existant plutôt qu'en lançant de grands projets coûteux."
        ),
        "services-publics": (
            "Retour à une gestion publique de l'eau : investir dans les infrastructures "
            "pour garantir qualité et disponibilité de cette ressource vitale à long terme."
        ),
    },
    "economie": {
        "commerce-local": (
            "Favoriser le dynamisme économique local en soutenant les circuits courts "
            "et l'agriculture urbaine, notamment via la régie agricole municipale de l'hippodrome."
        ),
        "attractivite": (
            "Positionner Toulouse comme métropole responsable d'une grande région agricole : "
            "soutenir une agriculture vertueuse face aux défis climatiques "
            "et renforcer l'attractivité par la qualité de vie."
        ),
    },
    "culture": {
        "equipements-culturels": (
            "Créer des espaces dédiés aux initiatives culturelles dans le nouveau parc "
            "de l'hippodrome : un lieu ouvert à la création artistique et aux événements de quartier."
        ),
    },
    "sport": {
        "equipements-sportifs": (
            "Aménager des espaces sportifs en plein air dans le parc de l'hippodrome transformé : "
            "un lieu d'activités quotidiennes accessible gratuitement à tous les Toulousains."
        ),
    },
    "urbanisme": {
        "amenagement-urbain": (
            "Stop au béton : arrêt des projets de construction excessive. "
            "Valoriser l'existant et maîtriser les investissements plutôt que de multiplier "
            "les grands chantiers. Opposition au projet Jonction Est jugé coûteux et inutile."
        ),
    },
    "solidarite": {
        "pouvoir-achat": (
            "Maîtriser les dépenses publiques pour protéger le pouvoir d'achat des Toulousains : "
            "approvisionner les cantines en produits locaux à coût maîtrisé "
            "grâce à la régie agricole municipale."
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

    # Verify all proposed sub-themes were found in JSON
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
    print(f"Total sub-themes with Meilhac proposals: {total}")


if __name__ == "__main__":
    main()
