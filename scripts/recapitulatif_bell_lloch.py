import json
import sys
import io

# Configuration de l'encodage UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Chemin du fichier
path = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\vitry-sur-seine-2026.json"

# Charger le fichier JSON
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

candidat_id = "bell-lloch"

# Trouver le candidat
candidat = None
for c in data["candidats"]:
    if c["id"] == candidat_id:
        candidat = c
        break

print("=" * 70)
print("RÉCAPITULATIF - ENRICHISSEMENT PROGRAMME PIERRE BELL-LLOCH")
print("=" * 70)
print(f"\nCandidat : {candidat['nom']}")
print(f"Liste : {candidat['liste']}")
print(f"Programme complet : {candidat['programmeComplet']}")
print(f"URL du programme : {candidat['programmeUrl']}")

print("\n" + "=" * 70)
print("PROPOSITIONS PAR CATÉGORIE")
print("=" * 70)

total_propositions = 0

for categorie in data["categories"]:
    propositions_categorie = []

    for sous_theme in categorie["sousThemes"]:
        if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is not None:
            prop = sous_theme["propositions"][candidat_id]
            propositions_categorie.append({
                "sous_theme": sous_theme["nom"],
                "texte": prop["texte"][:100] + "..." if len(prop["texte"]) > 100 else prop["texte"]
            })

    if propositions_categorie:
        print(f"\n{categorie['nom']} ({len(propositions_categorie)} propositions)")
        print("-" * 70)
        for i, prop in enumerate(propositions_categorie, 1):
            print(f"  {i}. {prop['sous_theme']}")
            print(f"     {prop['texte']}")
        total_propositions += len(propositions_categorie)

print("\n" + "=" * 70)
print(f"TOTAL : {total_propositions} propositions")
print("=" * 70)

# Liste des nouveaux sous-thèmes enrichis
print("\n" + "=" * 70)
print("NOUVELLES PROPOSITIONS AJOUTÉES")
print("=" * 70)

nouveaux_sous_themes = [
    "cantines-fournitures",
    "periscolaire-loisirs",
    "acces-logement",
    "espaces-verts",
    "climat-adaptation",
    "transports-en-commun",
    "amenagement-urbain",
    "velo-mobilites-douces",
    "budget-participatif",
    "egalite-discriminations"
]

for categorie in data["categories"]:
    for sous_theme in categorie["sousThemes"]:
        if sous_theme["id"] in nouveaux_sous_themes:
            if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is not None:
                print(f"\n✓ {sous_theme['nom']} ({categorie['nom']})")
                print(f"  {sous_theme['propositions'][candidat_id]['texte'][:150]}...")
