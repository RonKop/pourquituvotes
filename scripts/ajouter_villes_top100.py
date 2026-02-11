#!/usr/bin/env python3
"""
Ajoute les villes manquantes du top 100 français dans villes.json
et crée les fichiers JSON d'élection vides correspondants.
"""
import json
import os
import copy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VILLES_JSON = os.path.join(BASE_DIR, "data", "villes.json")
ELECTIONS_DIR = os.path.join(BASE_DIR, "data", "elections")
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "schema", "schema_elections.json")

# Villes manquantes du top 100 : (id, nom, codePostal, departement)
NOUVELLES_VILLES = [
    ("nimes", "Nîmes", "30000", "30"),
    ("argenteuil", "Argenteuil", "95100", "95"),
    ("saint-denis", "Saint-Denis", "93200", "93"),
    ("villeurbanne", "Villeurbanne", "69100", "69"),
    ("saint-denis-reunion", "Saint-Denis (La Réunion)", "97400", "974"),
    ("le-mans", "Le Mans", "72000", "72"),
    ("annecy", "Annecy", "74000", "74"),
    ("besancon", "Besançon", "25000", "25"),
    ("boulogne-billancourt", "Boulogne-Billancourt", "92100", "92"),
    ("montreuil", "Montreuil", "93100", "93"),
    ("saint-paul-reunion", "Saint-Paul (La Réunion)", "97460", "974"),
    ("tourcoing", "Tourcoing", "59200", "59"),
    ("roubaix", "Roubaix", "59100", "59"),
    ("nanterre", "Nanterre", "92000", "92"),
    ("asnieres-sur-seine", "Asnières-sur-Seine", "92600", "92"),
    ("vitry-sur-seine", "Vitry-sur-Seine", "94400", "94"),
    ("creteil", "Créteil", "94000", "94"),
    ("avignon", "Avignon", "84000", "84"),
    ("poitiers", "Poitiers", "86000", "86"),
    ("colombes", "Colombes", "92700", "92"),
    ("aubervilliers", "Aubervilliers", "93300", "93"),
    ("aulnay-sous-bois", "Aulnay-sous-Bois", "93600", "93"),
    ("dunkerque", "Dunkerque", "59140", "59"),
    ("saint-pierre-reunion", "Saint-Pierre (La Réunion)", "97410", "974"),
    ("versailles", "Versailles", "78000", "78"),
    ("rueil-malmaison", "Rueil-Malmaison", "92500", "92"),
    ("le-tampon", "Le Tampon (La Réunion)", "97430", "974"),
    ("courbevoie", "Courbevoie", "92400", "92"),
    ("beziers", "Béziers", "34500", "34"),
    ("pau", "Pau", "64000", "64"),
    ("la-rochelle", "La Rochelle", "17000", "17"),
    ("cherbourg-en-cotentin", "Cherbourg-en-Cotentin", "50100", "50"),
    ("merignac", "Mérignac", "33700", "33"),
    ("antibes", "Antibes", "06600", "06"),
    ("champigny-sur-marne", "Champigny-sur-Marne", "94500", "94"),
    ("saint-maur-des-fosses", "Saint-Maur-des-Fossés", "94100", "94"),
    ("ajaccio", "Ajaccio", "20000", "2A"),
    ("saint-nazaire", "Saint-Nazaire", "44600", "44"),
    ("fort-de-france", "Fort-de-France", "97200", "972"),
    ("cannes", "Cannes", "06400", "06"),
    ("noisy-le-grand", "Noisy-le-Grand", "93160", "93"),
    ("drancy", "Drancy", "93700", "93"),
    ("cergy", "Cergy", "95000", "95"),
    ("levallois-perret", "Levallois-Perret", "92300", "92"),
    ("issy-les-moulineaux", "Issy-les-Moulineaux", "92130", "92"),
    ("calais", "Calais", "62100", "62"),
    ("pessac", "Pessac", "33600", "33"),
    ("colmar", "Colmar", "68000", "68"),
    ("evry-courcouronnes", "Évry-Courcouronnes", "91000", "91"),
    ("quimper", "Quimper", "29000", "29"),
    ("bourges", "Bourges", "18000", "18"),
    ("venissieux", "Vénissieux", "69200", "69"),
    ("valence", "Valence", "26000", "26"),
    ("ivry-sur-seine", "Ivry-sur-Seine", "94200", "94"),
    ("antony", "Antony", "92160", "92"),
    ("clichy", "Clichy", "92110", "92"),
    ("montauban", "Montauban", "82000", "82"),
    ("la-seyne-sur-mer", "La Seyne-sur-Mer", "83500", "83"),
    ("villeneuve-d-ascq", "Villeneuve-d'Ascq", "59491", "59"),
    ("troyes", "Troyes", "10000", "10"),
    ("cayenne", "Cayenne", "97300", "973"),
    ("le-blanc-mesnil", "Le Blanc-Mesnil", "93150", "93"),
    ("pantin", "Pantin", "93500", "93"),
    ("niort", "Niort", "79000", "79"),
    ("chambery", "Chambéry", "73000", "73"),
    ("neuilly-sur-seine", "Neuilly-sur-Seine", "92200", "92"),
    ("frejus", "Fréjus", "83600", "83"),
    ("villejuif", "Villejuif", "94800", "94"),
    ("lorient", "Lorient", "56100", "56"),
]


def charger_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def creer_election_vide(ville_nom, schema):
    """Crée un JSON d'élection vide avec toutes les catégories/sous-thèmes."""
    categories = []
    for cat in schema["categories"]:
        sous_themes = []
        for st in cat["sousThemes"]:
            sous_themes.append({
                "id": st["id"],
                "nom": st["nom"],
                "propositions": {}
            })
        categories.append({
            "id": cat["id"],
            "nom": cat["nom"],
            "sousThemes": sous_themes
        })

    return {
        "ville": ville_nom,
        "annee": 2026,
        "type": "Élections municipales",
        "dateVote": "2026-03-15T08:00:00",
        "candidats": [],
        "categories": categories
    }


def main():
    # Charger villes existantes
    with open(VILLES_JSON, "r", encoding="utf-8") as f:
        villes = json.load(f)

    ids_existants = set(v["id"] for v in villes)
    schema = charger_schema()

    ajoutees = 0
    for ville_id, ville_nom, cp, dept in NOUVELLES_VILLES:
        if ville_id in ids_existants:
            print(f"  SKIP {ville_nom} (déjà présente)")
            continue

        # Ajouter dans villes.json
        election_id = f"{ville_id}-2026"
        villes.append({
            "id": ville_id,
            "nom": ville_nom,
            "codePostal": cp,
            "departement": dept,
            "elections": [election_id],
            "stats": {
                "candidats": 0,
                "propositions": 0,
                "themes": 12,
                "complets": 0
            },
            "candidats": []
        })

        # Créer fichier élection
        election_path = os.path.join(ELECTIONS_DIR, f"{election_id}.json")
        if not os.path.exists(election_path):
            election_data = creer_election_vide(ville_nom, schema)
            with open(election_path, "w", encoding="utf-8") as f:
                json.dump(election_data, f, ensure_ascii=False, indent=2)
            print(f"  + {ville_nom} ({election_id}.json)")
        else:
            print(f"  + {ville_nom} (JSON existait déjà)")

        ajoutees += 1

    # Trier par nom
    villes.sort(key=lambda v: v["nom"])

    # Sauvegarder
    with open(VILLES_JSON, "w", encoding="utf-8") as f:
        json.dump(villes, f, ensure_ascii=False, indent=2)

    print(f"\n=== {ajoutees} villes ajoutées, total: {len(villes)} ===")


if __name__ == "__main__":
    main()
