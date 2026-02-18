#!/usr/bin/env python3
"""
Integration du programme d'Eric Ducatel (Antibes) - Site WordPress
Source : https://ericducatel.wordpress.com/elections-municipales-2026-a-antibes-juan-les-pins/programme/

Programme complet avec de nombreuses mesures concretes reparties sur :
- Transparence et democratie participative
- Securite et tranquillite
- Proprete
- Sante / environnement
- Logement
- Urbanisme et cadre de vie
- Transports et mobilites douces
- Environnement
- Exigences civiques
- Projets bonus (lignes maritimes, telepherique, etc.)

Bien plus de 15 mesures concretes => programmeComplet = True
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "elections")
JSON_PATH = os.path.join(DATA_DIR, "antibes-2026.json")

CANDIDAT_ID = "ducatel"
SOURCE = "Programme officiel 2026"
SOURCE_URL = "https://ericducatel.wordpress.com/elections-municipales-2026-a-antibes-juan-les-pins/programme/"

# Metadata updates
METADATA = {
    "programmeComplet": True,
    "programmeUrl": "https://ericducatel.wordpress.com/elections-municipales-2026-a-antibes-juan-les-pins/",
}

# Propositions mapped to sub-themes (category_id -> sub_theme_id -> texte)
PROPOSITIONS = {
    "securite": {
        "police-municipale": (
            "Rouvrir des postes de police municipale dans tous les quartiers. "
            "Les adjoints sont garants et acteurs du maintien de l\u2019ordre public. "
            "Recruter des bin\u00f4mes ASVP dans un mode \u00ab service civique municipal \u00bb. "
            "Multiplier les contr\u00f4les inopin\u00e9s sur les axes routiers, nuit et jour."
        ),
        "prevention-mediation": (
            "Renforcer la pr\u00e9vention par des radars p\u00e9dagogiques et des sensibilisations "
            "sur les panneaux publicitaires. "
            "Intransigeance sur la vitesse excessive pr\u00e8s des \u00e9coles pour tous les engins motoris\u00e9s. "
            "Intransigeance sur le non-respect du code de la route et les incivilit\u00e9s routi\u00e8res, "
            "y compris par les cyclistes et pilotes d\u2019engins motoris\u00e9s."
        ),
    },
    "transports": {
        "transports-en-commun": (
            "\u00c9tudier la gratuit\u00e9 des transports en commun sur le territoire de la CASA. "
            "Faire cr\u00e9er une passerelle d\u2019acc\u00e8s aux quais de la gare SNCF depuis la zone multimodale. "
            "\u00c9tudier la r\u00e9alisation d\u2019un t\u00e9l\u00e9ph\u00e9rique entre la gare de Biot et Sophia-Antipolis. "
            "\u00c9tudier l\u2019ouverture de 2 lignes maritimes : "
            "avec les \u00eeles de L\u00e9rins depuis Juan-les-Pins, et avec Nice depuis le port Vauban."
        ),
        "velo-mobilites-douces": (
            "Am\u00e9nager une voie cyclable traversante de la Fontonne au parc Exflora "
            "via la gare multimodale et la gare de Juan, "
            "entre Juan-les-Pins et les 3 Moulins, "
            "et entre Antibes centre et les 3 Moulins. "
            "Autoriser les v\u00e9los et EDPM en sens interdit sur certaines voies."
        ),
        "pietons-circulation": (
            "Ouvrir des chemins pi\u00e9tons qui existaient jadis. "
            "\u00c9tudier l\u2019avenir de l\u2019ancienne RN7 (route de Nice) et de la D85 (route de Grasse). "
            "R\u00e9aliser un trafic routier sur une ann\u00e9e enti\u00e8re "
            "pour envisager un plan global de circulation. "
            "Collecte de donn\u00e9es d\u2019accidentologie."
        ),
        "stationnement": (
            "D\u00e9finir un syst\u00e8me de tarification de stationnement pour les r\u00e9sidents."
        ),
        "tarifs-gratuite": (
            "\u00c9tudier la gratuit\u00e9 des transports en commun sur le territoire de la CASA."
        ),
    },
    "logement": {
        "logement-social": (
            "Faire un \u00e9tat des lieux pr\u00e9cis des environ 4 500 logements en gestion par les bailleurs sociaux. "
            "Publier les listes d\u2019attente publiques, anonymis\u00e9es et dat\u00e9es pour l\u2019acc\u00e8s au logement social."
        ),
        "acces-logement": (
            "Conditionner la r\u00e9alisation d\u2019Ecotone (30 000 m\u00b2 de bureaux aux 3 Moulins) "
            "\u00e0 la transformation de surfaces commerciales en logements \u00e0 Sophia Antipolis. "
            "Ouvrir les maisons de retraite et \u00e9tablissements sp\u00e9cialis\u00e9s \u00e0 l\u2019accueil de situations d\u2019urgence, "
            "et contribuer au maintien \u00e0 domicile."
        ),
    },
    "environnement": {
        "espaces-verts": (
            "Entretenir les arbres pour les pr\u00e9server (\u00e9lagage et nettoyage de tous les arbres d\u00e8s 2026). "
            "Aider \u00e0 l\u2019entretien des grands arbres des copropri\u00e9t\u00e9s. "
            "D\u00e9bitumer certains squares ou places (Ren\u00e9 Cassin, Vautrin\u2026). "
            "R\u00e9habiliter le parc Exflora."
        ),
        "proprete-dechets": (
            "Une ville propre par des am\u00e9nagements en nombre suffisant. "
            "Sensibiliser les touristes, dont les pratiques diff\u00e8rent. "
            "Intransigeance sur les d\u00e9p\u00f4ts sauvages et le non-respect des consignes de tri. "
            "Intransigeance sur les d\u00e9jections canines et autres d\u00e9chets jet\u00e9s \u00e0 m\u00eame le sol."
        ),
        "climat-adaptation": (
            "Accompagner les copropri\u00e9t\u00e9s dans la r\u00e9cup\u00e9ration d\u2019eau de pluie. "
            "Pr\u00e9parer la fin de l\u2019incin\u00e9rateur des Semboules, "
            "dont la nocivit\u00e9 n\u2019a jamais voulu \u00eatre \u00e9tudi\u00e9e par la municipalit\u00e9."
        ),
        "renovation-energetique": (
            "Orienter les nouvelles constructions vers l\u2019utilisation de la g\u00e9othermie passive. "
            "R\u00e9habiliter les logements existants, arr\u00eater de construire pour construire."
        ),
        "alimentation-durable": (
            "Cr\u00e9er un march\u00e9 alimentaire \u00e0 Juan-les-Pins "
            "port\u00e9 par des producteurs locaux."
        ),
    },
    "sante": {
        "prevention-sante": (
            "Pr\u00e9parer la fin de l\u2019incin\u00e9rateur des Semboules, "
            "dont la nocivit\u00e9 n\u2019a jamais voulu \u00eatre \u00e9tudi\u00e9e par la municipalit\u00e9. "
            "Faire pression contre toutes les sources de nuisances sonores. "
            "Combattre naturellement la prolif\u00e9ration de nuisibles vecteurs potentiels de maladie."
        ),
        "seniors": (
            "Ouvrir les maisons de retraite ou \u00e9tablissements sp\u00e9cialis\u00e9s "
            "\u00e0 l\u2019accueil de situations d\u2019urgence, et contribuer au maintien \u00e0 domicile. "
            "Renforcer les services publics autour des plus ag\u00e9(e)s."
        ),
    },
    "democratie": {
        "budget-participatif": (
            "Mettre en place un budget et un financement participatifs. "
            "Sonder les habitants chaque ann\u00e9e sur les sujets susceptibles de justifier une hausse d\u2019imp\u00f4ts. "
            "\u00c9tudier la possibilit\u00e9 de financement participatif pour des projets de la ville et de la CASA, "
            "au moyen d\u2019outils financiers de placement. "
            "Organiser 2 r\u00e9f\u00e9rendums par an, sur propositions citoyennes. "
            "Tenir 2 conventions annuelles de 50 citoyen(ne)s tir\u00e9(e)s au sort."
        ),
        "transparence": (
            "Favoriser l\u2019information publique en la rendant accessible et lisible. "
            "Lancer plusieurs \u00e9tudes et analyses sur les 2 premi\u00e8res ann\u00e9es du mandat. "
            "Publier les listes d\u2019attente publiques, anonymis\u00e9es et dat\u00e9es "
            "(logement social, \u00e9coles, cantines, places de port). "
            "Publier et notifier les tarifs en fin d\u2019ann\u00e9e par tout moyen. "
            "Revoir toutes les d\u00e9lib\u00e9rations 2024-2025 non unanimes et non d\u00e9finitives "
            "pour les proposer \u00e0 nouveau \u00e0 la d\u00e9lib\u00e9ration. "
            "Partager les plans et objectifs concrets pour la dur\u00e9e du mandat."
        ),
        "services-publics": (
            "Faire une pause sur les investissements pour ramener l\u2019endettement "
            "\u00e0 moins de 100 % du budget de fonctionnement. "
            "Renforcer les services publics autour des plus jeunes et des plus \u00e2g\u00e9s. "
            "Ne pas augmenter les imp\u00f4ts. "
            "Lancer un questionnaire d\u00e8s les 6 premiers mois du mandat."
        ),
    },
    "economie": {
        "commerce-local": (
            "Cr\u00e9er un march\u00e9 alimentaire \u00e0 Juan-les-Pins port\u00e9 par des producteurs locaux. "
            "Affirmer un cap nouveau vers une \u00e9conomie plus locale "
            "port\u00e9e par les atouts d\u2019une ville aux multiples facettes, "
            "et forte de ses connexions internationales."
        ),
        "attractivite": (
            "Sortir d\u2019une d\u00e9rive tout tourisme. "
            "Cr\u00e9er des quartiers-villages pour m\u00e9riter le qualificatif de village. "
            "R\u00e9ouverture du \u00ab quai des milliardaires \u00bb, dont aucun acte officiel n\u2019interdit l\u2019acc\u00e8s."
        ),
    },
    "culture": {
        "equipements-culturels": (
            "S\u00e9curiser le patrimoine et les rappels patrimoniaux."
        ),
    },
    "sport": {
        "equipements-sportifs": (
            "R\u00e9habiliter le centre INRA pour le r\u00e9orienter vers des pratiques sportives."
        ),
    },
    "urbanisme": {
        "amenagement-urbain": (
            "Synth\u00e9tiser le Plan Local d\u2019Urbanisme et rendre l\u2019avenir urbain plus lisible. "
            "Orienter les nouvelles constructions vers la g\u00e9othermie passive. "
            "R\u00e9habiliter les logements, arr\u00eater de construire pour construire. "
            "\u00c9tudier l\u2019avenir de l\u2019ancienne RN7 (route de Nice) et de la D85 (route de Grasse). "
            "\u00c9tudier la r\u00e9alisation d\u2019un espace s\u00e9curis\u00e9 de conduite automobile sur le territoire de la CASA, "
            "en gestion confi\u00e9e \u00e0 une association."
        ),
    },
    "solidarite": {
        "pouvoir-achat": (
            "Ne pas augmenter les imp\u00f4ts. "
            "Faire une pause sur les investissements pour ramener l\u2019endettement "
            "\u00e0 moins de 100 % du budget de fonctionnement."
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
    print(f"Total sub-themes with Ducatel proposals: {total}")


if __name__ == "__main__":
    main()
