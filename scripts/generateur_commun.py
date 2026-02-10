#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module commun pour générer et insérer des villes dans les fichiers JSON."""
import json
import os
import re
from datetime import datetime

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
VILLES_JSON = os.path.join(DATA_DIR, "villes.json")
APP_JS_PATH = os.path.join(ROOT_DIR, "js", "app.js")
HOME_JS_PATH = os.path.join(ROOT_DIR, "js", "home.js")

CATEGORIES = [
    ("securite", "Sécurité & Prévention", [("police-municipale", "Police municipale"), ("videoprotection", "Vidéoprotection"), ("prevention-mediation", "Prévention & Médiation"), ("violences-femmes", "Violences faites aux femmes")]),
    ("transports", "Transports & Mobilité", [("transports-en-commun", "Transports en commun"), ("velo-mobilites-douces", "Vélo & Mobilités douces"), ("pietons-circulation", "Piétons & Circulation"), ("stationnement", "Stationnement"), ("tarifs-gratuite", "Tarifs & Gratuité")]),
    ("logement", "Logement", [("logement-social", "Logement social"), ("logements-vacants", "Logements vacants"), ("encadrement-loyers", "Encadrement des loyers"), ("acces-logement", "Accès au logement")]),
    ("education", "Éducation & Jeunesse", [("petite-enfance", "Petite enfance"), ("ecoles-renovation", "Écoles & Rénovation"), ("cantines-fournitures", "Cantines & Fournitures"), ("periscolaire-loisirs", "Périscolaire & Loisirs"), ("jeunesse", "Jeunesse")]),
    ("environnement", "Environnement & Transition écologique", [("espaces-verts", "Espaces verts & Biodiversité"), ("proprete-dechets", "Propreté & Déchets"), ("climat-adaptation", "Climat & Adaptation"), ("renovation-energetique", "Rénovation énergétique"), ("alimentation-durable", "Alimentation durable")]),
    ("sante", "Santé & Accès aux soins", [("centres-sante", "Centres de santé"), ("prevention-sante", "Prévention santé"), ("seniors", "Seniors")]),
    ("democratie", "Démocratie & Vie citoyenne", [("budget-participatif", "Budget participatif"), ("transparence", "Transparence"), ("vie-associative", "Vie associative"), ("services-publics", "Services publics")]),
    ("economie", "Économie & Emploi", [("commerce-local", "Commerce local"), ("emploi-insertion", "Emploi & Insertion"), ("attractivite", "Attractivité")]),
    ("culture", "Culture & Patrimoine", [("equipements-culturels", "Équipements culturels"), ("evenements-creation", "Événements & Création")]),
    ("sport", "Sport & Loisirs", [("equipements-sportifs", "Équipements sportifs"), ("sport-pour-tous", "Sport pour tous")]),
    ("urbanisme", "Urbanisme & Cadre de vie", [("amenagement-urbain", "Aménagement urbain"), ("accessibilite", "Accessibilité"), ("quartiers-prioritaires", "Quartiers prioritaires")]),
    ("solidarite", "Solidarité & Égalité", [("aide-sociale", "Aide sociale"), ("egalite-discriminations", "Égalité & Discriminations"), ("pouvoir-achat", "Pouvoir d'achat")]),
]


def get_departement(cp):
    """Déduit le département du code postal."""
    if not cp:
        return ""
    if cp.startswith("20"):
        num = int(cp[:5])
        return "2A" if num <= 20190 else "2B"
    if cp.startswith("97") or cp.startswith("98"):
        return cp[:3]
    return cp[:2]


def build_election_json(election_id, ville_nom, candidats, cand_ids, props, categories=None):
    """Construit le dictionnaire JSON d'une élection."""
    if categories is None:
        categories = CATEGORIES

    election = {
        "ville": ville_nom,
        "annee": 2026,
        "type": "Élections municipales",
        "dateVote": "2026-03-15T08:00:00",
        "candidats": [],
        "categories": []
    }

    # Candidats
    for c in candidats:
        election["candidats"].append({
            "id": c["id"],
            "nom": c["nom"],
            "liste": c["liste"],
            "programmeUrl": c["programmeUrl"],
            "programmeComplet": c["programmeComplet"],
            "programmePdfPath": c["programmePdfPath"]
        })

    # Catégories et sous-thèmes
    for cat_id, cat_nom, sous_themes in categories:
        cat = {
            "id": cat_id,
            "nom": cat_nom,
            "sousThemes": []
        }
        for st_id, st_nom in sous_themes:
            st = {
                "id": st_id,
                "nom": st_nom,
                "propositions": {}
            }
            for cid in cand_ids:
                key = (cat_id, st_id, cid)
                if key in props:
                    texte, source, source_url = props[key]
                    st["propositions"][cid] = {
                        "texte": texte,
                        "source": source,
                        "sourceUrl": source_url
                    }
                else:
                    st["propositions"][cid] = None
            cat["sousThemes"].append(st)
        election["categories"].append(cat)

    return election


def compute_stats(election):
    """Calcule les statistiques d'une élection."""
    total_props = 0
    for cat in election["categories"]:
        for st in cat.get("sousThemes", []):
            for cid, prop in st.get("propositions", {}).items():
                if prop and prop.get("texte"):
                    total_props += 1

    complets = sum(1 for c in election["candidats"] if c.get("programmeComplet"))

    return {
        "candidats": len(election["candidats"]),
        "propositions": total_props,
        "themes": len(election["categories"]),
        "complets": complets
    }


def increment_data_version():
    """Incrémente DATA_VERSION dans app.js et home.js."""
    now = datetime.now()
    new_version = now.strftime("%Y%m%d") + "01"

    for js_path in [APP_JS_PATH, HOME_JS_PATH]:
        if not os.path.exists(js_path):
            continue
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Trouver et incrémenter DATA_VERSION
        m = re.search(r"var DATA_VERSION\s*=\s*'(\d+)'", content)
        if m:
            old_version = m.group(1)
            # Si même date, incrémenter le compteur
            if old_version[:8] == new_version[:8]:
                counter = int(old_version[8:]) + 1
                new_version = old_version[:8] + f"{counter:02d}"
            content = content[:m.start()] + f"var DATA_VERSION = '{new_version}'" + content[m.end():]
            with open(js_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  DATA_VERSION -> {new_version} dans {os.path.basename(js_path)}")

    return new_version


def insert_city(ville_id, ville_nom, ville_cp, candidats, props, categories=None):
    """Insère ou met à jour une ville dans les fichiers JSON."""
    election_id = f"{ville_id}-2026"
    cand_ids = [c["id"] for c in candidats]

    # Créer les répertoires si nécessaire
    os.makedirs(ELECTIONS_DIR, exist_ok=True)

    # 1. Construire et écrire le fichier élection JSON
    election = build_election_json(election_id, ville_nom, candidats, cand_ids, props, categories)
    election_path = os.path.join(ELECTIONS_DIR, f"{election_id}.json")
    with open(election_path, "w", encoding="utf-8") as f:
        json.dump(election, f, ensure_ascii=False, indent=2)
    print(f"  Election {election_id}.json écrite")

    # 2. Mettre à jour villes.json
    if os.path.exists(VILLES_JSON):
        with open(VILLES_JSON, "r", encoding="utf-8") as f:
            villes = json.load(f)
    else:
        villes = []

    # Calculer les stats
    stats = compute_stats(election)

    # Construire la liste légère de candidats
    candidats_leger = [{"id": c["id"], "nom": c["nom"], "liste": c["liste"]} for c in candidats]

    # Trouver ou créer l'entrée ville
    ville_entry = next((v for v in villes if v["id"] == ville_id), None)
    today = datetime.now().strftime("%Y-%m-%d")

    if ville_entry:
        # Mettre à jour
        ville_entry["stats"] = stats
        ville_entry["candidats"] = candidats_leger
        ville_entry["derniereMaj"] = today
        print(f"  Ville {ville_id} mise à jour dans villes.json (derniereMaj: {today})")
    else:
        # Créer
        ville_entry = {
            "id": ville_id,
            "nom": ville_nom,
            "codePostal": ville_cp,
            "departement": get_departement(ville_cp),
            "elections": [election_id],
            "stats": stats,
            "candidats": candidats_leger,
            "derniereMaj": today
        }
        villes.append(ville_entry)
        print(f"  Ville {ville_id} ajoutée dans villes.json (derniereMaj: {today})")

    with open(VILLES_JSON, "w", encoding="utf-8") as f:
        json.dump(villes, f, ensure_ascii=False, indent=2)

    # 3. Incrémenter DATA_VERSION pour le cache busting
    increment_data_version()

    # 4. Afficher les statistiques
    print(f"  Total: {len(props)} propositions")
    for cid in cand_ids:
        cn = next(c["nom"] for c in candidats if c["id"] == cid)
        count = sum(1 for k in props if k[2] == cid)
        print(f"    {cn}: {count}")
