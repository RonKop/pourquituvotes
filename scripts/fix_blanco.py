"""Remplacer les propositions presse de Richard Blanco (Montauban) par le contenu de sa circulaire officielle."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/elections/montauban-2026.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

SRC = "Circulaire officielle Lutte Ouvrière – Municipales 2026"
URL = "https://lutte-ouvriere.org"

# Nouvelles propositions extraites de la circulaire
blanco = {
    "solidarite": {
        "pouvoir-achat": {
            "mesures": [
                "Indexer les salaires, les pensions et les allocations sur les prix pour protéger le pouvoir d'achat des travailleurs."
            ],
            "source": SRC,
            "sourceUrl": URL,
        },
        "egalite-discriminations": {
            "mesures": [
                "Rejeter le racisme, l'antisémitisme, la xénophobie et tout ce qui divise les travailleurs."
            ],
            "source": SRC,
            "sourceUrl": URL,
        },
    },
    "economie": {
        "emploi-insertion": {
            "mesures": [
                "Répartir le travail entre tous, sans perte de salaire, pour lutter contre le chômage et la précarité."
            ],
            "source": SRC,
            "sourceUrl": URL,
        },
    },
}

# Supprimer toutes les anciennes propositions "blanco"
for cat in data["categories"]:
    for st in cat["sousThemes"]:
        if "blanco" in st.get("propositions", {}):
            st["propositions"]["blanco"] = None

# Appliquer les nouvelles
for cat in data["categories"]:
    cat_id = cat["id"]
    if cat_id in blanco:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in blanco[cat_id]:
                st["propositions"]["blanco"] = blanco[cat_id][st_id]
                print(f"  {cat_id}/{st_id}: {len(blanco[cat_id][st_id]['mesures'])} mesures")

# Update candidate metadata
for c in data["candidats"]:
    if c["id"] == "blanco":
        c["programmeUrl"] = URL
        c["programmePdfPath"] = "data/programmes/82_82121_circulaire_Montauban-2.pdf"
        # programmeComplet reste false — circulaire idéologique, pas programme municipal
        break

# Count
count = sum(
    len(st.get("propositions", {}).get("blanco", {}).get("mesures", []))
    for cat in data["categories"]
    for st in cat["sousThemes"]
    if st.get("propositions", {}).get("blanco") and isinstance(st["propositions"]["blanco"], dict)
)
print(f"\nTotal Blanco: {count} mesures (circulaire officielle)")

with open('data/elections/montauban-2026.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("montauban-2026.json mis à jour OK")
