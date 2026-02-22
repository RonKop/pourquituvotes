import json
import sys
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Lire le fichier JSON
with open(r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\frejus-2026.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Nouvelles propositions pour Bonnemain (basées sur les recherches)
new_propositions = {
    "stationnement": {
        "texte": "Proposer des solutions de stationnement réversibles et adaptables tenant compte des risques de submersion marine",
        "source": "notreparticestfrejus.fr",
        "sourceUrl": "https://www.notreparticestfrejus.fr/"
    },
    "equipements-culturels": {
        "texte": "Valoriser le patrimoine culturel exceptionnel de Fréjus (musées, théâtre romain, chapelle Cocteau) pour que chaque habitant en bénéficie pleinement",
        "source": "notreparticestfrejus.fr",
        "sourceUrl": "https://www.notreparticestfrejus.fr/"
    },
    "alimentation-durable": {
        "texte": "Soutenir les circuits courts et les producteurs locaux, encourager une alimentation durable et proximité avec les agriculteurs régionaux",
        "source": "notreparticestfrejus.fr",
        "sourceUrl": "https://www.notreparticestfrejus.fr/"
    },
    "budget-participatif": {
        "texte": "Impliquer les citoyens dans les décisions budgétaires locales et renforcer la démocratie participative à Fréjus",
        "source": "notreparticestfrejus.fr",
        "sourceUrl": "https://www.notreparticestfrejus.fr/"
    },
    "ecoles-renovation": {
        "texte": "Investir dans les écoles et offrir des apprentissages modernes et de qualité, garantir l'égalité et l'égalité des chances pour la réussite de tous",
        "source": "notreparticestfrejus.fr",
        "sourceUrl": "https://www.notreparticestfrejus.fr/"
    },
    "vie-associative": {
        "texte": "Renforcer la cohésion sociale en développant les relations entre quartiers et promouvoir les actions des associations fréjusiennes",
        "source": "notreparticestfrejus.fr",
        "sourceUrl": "https://www.notreparticestfrejus.fr/"
    }
}

# Parcourir les catégories et sous-thèmes pour ajouter les propositions
count_before = 0
count_after = 0

for category in data["categories"]:
    for sous_theme in category["sousThemes"]:
        sous_theme_id = sous_theme["id"]

        # Compter les propositions existantes pour Bonnemain avant
        if sous_theme["propositions"]["bonnemain"] is not None:
            count_before += 1

        # Ajouter la nouvelle proposition si elle est null et si elle existe dans new_propositions
        if sous_theme_id in new_propositions and sous_theme["propositions"]["bonnemain"] is None:
            sous_theme["propositions"]["bonnemain"] = new_propositions[sous_theme_id]
            count_after += 1

# Recompter toutes les propositions de Bonnemain
total_propositions = 0
for category in data["categories"]:
    for sous_theme in category["sousThemes"]:
        if sous_theme["propositions"]["bonnemain"] is not None:
            total_propositions += 1

# Écrire le fichier JSON modifié
with open(r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\frejus-2026.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✓ Modification complétée")
print(f"  - Propositions ajoutées: {count_after}")
print(f"  - Total propositions Bonnemain: {total_propositions}")
print(f"  - Statut programmeComplet: {data['candidats'][1]['programmeComplet']}")
