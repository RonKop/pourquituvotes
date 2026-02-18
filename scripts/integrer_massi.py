#!/usr/bin/env python3
"""
Intégration du programme de Josée Massi (Toulon) - Site officiel + presse locale
Sources :
  - https://joseemassi.com/ (12 axes thématiques)
  - Info83, RCF, France Bleu (articles de presse 2026)

15 propositions mappées aux sous-thèmes existants.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "elections")
JSON_PATH = os.path.join(DATA_DIR, "toulon-2026.json")

CANDIDAT_ID = "massi"
SOURCE = "Programme officiel 2026"
SOURCE_URL = "https://joseemassi.com/"

# Metadata updates
METADATA = {
    "programmeComplet": True,
    "programmeUrl": "https://joseemassi.com/",
    "liste": "Toulon mon parti (sortante)",
}

# Propositions mapped to sub-themes (category_id -> sub_theme_id -> texte)
PROPOSITIONS = {
    "securite": {
        "police-municipale": (
            "Passer de 152 à 200 policiers municipaux d'ici la fin du mandat. "
            "Créer des commissariats de quartier et implanter des policiers municipaux "
            "dans les mairies annexes du Pont-du-Las, de Saint-Jean-du-Var, de la Rode "
            "et dans d'autres secteurs"
        ),
        "videoprotection": (
            "Renforcement massif de la vidéoprotection sur l'ensemble de la ville, "
            "dans la continuité des investissements du mandat 2020-2025"
        ),
        "prevention-mediation": (
            "Politique de sécurité locale combinant prévention, dissuasion et présence "
            "de proximité dans tous les quartiers de Toulon"
        ),
    },
    "transports": {
        "transports-en-commun": (
            "Créer un bus à haut niveau de service (BHNS) rapide avec un bus "
            "toutes les 10 minutes sur les axes principaux"
        ),
        "velo-mobilites-douces": (
            "Connecter les 70 km de pistes cyclables entre elles pour créer "
            "un réseau continu de mobilités douces à Toulon"
        ),
    },
    "logement": {
        "logement-social": (
            "Imposer 30 % de logements sociaux dans toute nouvelle construction "
            "de plus de 800 m². Fin des grands ensembles et répartition des logements "
            "sociaux dans tous les quartiers de Toulon"
        ),
        "acces-logement": (
            "Conversion de l'ancien bâtiment de la CAF à La Rode en résidence "
            "de 180 logements étudiants pour renforcer l'attractivité universitaire"
        ),
    },
    "education": {
        "petite-enfance": (
            "Plan petite enfance : création de nouvelles places en crèche "
            "pour faciliter l'accès à l'emploi des parents toulonnais"
        ),
        "ecoles-renovation": (
            "Végétalisation des cours d'école : îlots de fraîcheur, espaces ombragés, "
            "coins lecture, potagers et aires de jeux partagées. "
            "Verdissement déjà réalisé dans plusieurs établissements, à étendre à toutes les écoles"
        ),
    },
    "environnement": {
        "espaces-verts": (
            "Végétalisation de la ville : développement des espaces verts, "
            "préservation de la rade et du littoral toulonnais"
        ),
        "climat-adaptation": (
            "Adaptation de la ville aux risques climatiques : protection du littoral, "
            "mobilités douces et préservation de la rade de Toulon"
        ),
    },
    "sante": {
        "centres-sante": (
            "Renforcer la santé de proximité : rapprocher les Toulonnais du soin "
            "en densifiant l'offre de soins dans les quartiers, face à une densité "
            "de médecins généralistes inférieure à la moyenne (86,3 pour 100 000 habitants)"
        ),
    },
    "democratie": {
        "budget-participatif": (
            "Plateforme numérique « Toulon & Vous » pour la participation, "
            "la consultation et la concertation citoyenne. "
            "Conseils de quartier renforcés et présence accrue des services municipaux sur le terrain"
        ),
        "services-publics": (
            "Lancer l'outil « Toulon & Vous » pour maintenir le lien entre habitants "
            "et mairie sur les questions administratives et les services du quotidien"
        ),
    },
    "economie": {
        "attractivite": (
            "Dynamiser l'économie avec la création de nouveaux secteurs économiques, "
            "construction d'une résidence étudiante de 180 logements, "
            "et verdissement des écoles. Faire de Toulon une capitale méditerranéenne "
            "entreprenante, durable et accueillante"
        ),
    },
    "solidarite": {
        "aide-sociale": (
            "Programme « Rebond Solo » d'accompagnement des parents monoparentaux. "
            "Pass solidaire pour les jeunes, parents solo et travailleurs pauvres. "
            "Une ville qui protège, qui accompagne et qui relie"
        ),
    },
    "urbanisme": {
        "quartiers-prioritaires": (
            "Projets spécifiques pour chaque quartier : valoriser chaque identité "
            "de quartier tout en renforçant l'unité de la ville. "
            "Le centre-ville redevenu un cœur vivant, habité et attractif"
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
    print(f"Total sub-themes with Massi proposals: {total}")


if __name__ == "__main__":
    main()
