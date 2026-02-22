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

# Identifier le candidat bell-lloch
candidat_id = "bell-lloch"

# Compter les propositions avant modification
propositions_avant = 0
for categorie in data["categories"]:
    for sous_theme in categorie["sousThemes"]:
        if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is not None:
            propositions_avant += 1

print(f"Propositions avant enrichissement : {propositions_avant}")

# Enrichir les propositions
for categorie in data["categories"]:
    for sous_theme in categorie["sousThemes"]:

        # Cantines & Fournitures (enrichir si existant)
        if sous_theme["id"] == "cantines-fournitures":
            if candidat_id in sous_theme["propositions"]:
                if sous_theme["propositions"][candidat_id] is None:
                    sous_theme["propositions"][candidat_id] = {
                        "texte": "Gratuité des fournitures scolaires pour plusieurs milliers d'élèves, cantines au quotient familial avec produits de qualité issus de circuits courts",
                        "source": "pbl2026.fr - Bilan et programme 2026",
                        "sourceUrl": "https://pbl2026.fr/programme.html"
                    }
                else:
                    # Enrichir le texte existant
                    texte_actuel = sous_theme["propositions"][candidat_id]["texte"]
                    sous_theme["propositions"][candidat_id]["texte"] = texte_actuel + ". Gratuité des fournitures scolaires pour plusieurs milliers d'élèves vitriots"

        # Périscolaire & Loisirs (enrichir si existant)
        elif sous_theme["id"] == "periscolaire-loisirs":
            if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is not None:
                texte_actuel = sous_theme["propositions"][candidat_id]["texte"]
                sous_theme["propositions"][candidat_id]["texte"] = texte_actuel + ". Organisation de 2 000 séjours en vacances pour les jeunes Vitriots, activités périscolaires accessibles à tous"

        # Accès au logement (nouveau)
        elif sous_theme["id"] == "acces-logement":
            if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is None:
                sous_theme["propositions"][candidat_id] = {
                    "texte": "Délai moyen d'attribution réduit à 4 ans grâce à une commission d'attribution équitable examinant chaque situation : composition familiale, ressources, type de logement demandé et ancienneté. Attribution transparente de 500 logements par an",
                    "source": "Mairie de Vitry-sur-Seine",
                    "sourceUrl": "https://www.vitry94.fr/vos-questions-sur-le-logement-en-direct/"
                }

        # Espaces verts (enrichir si existant)
        elif sous_theme["id"] == "espaces-verts":
            if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is not None:
                texte_actuel = sous_theme["propositions"][candidat_id]["texte"]
                sous_theme["propositions"][candidat_id]["texte"] = texte_actuel + ". Transformation écologique des espaces verts du quartier Vilmorin, développement du parc des Prairies du Fort comme 4ème plus grand espace vert de la ville, plantation d'arbres remarquables et création de prairies fleuries pour favoriser les pollinisateurs"

        # Climat & Adaptation (nouveau)
        elif sous_theme["id"] == "climat-adaptation":
            if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is None:
                sous_theme["propositions"][candidat_id] = {
                    "texte": "Plan d'adaptation au changement climatique avec déminéralisation des sols, création d'îlots de fraîcheur dans les quartiers, plantation massive d'arbres et végétalisation des cours d'école",
                    "source": "pbl2026.fr",
                    "sourceUrl": "https://pbl2026.fr/programme.html"
                }

        # Transports en commun (nouveau)
        elif sous_theme["id"] == "transports-en-commun":
            if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is None:
                sous_theme["propositions"][candidat_id] = {
                    "texte": "Arrivée de la ligne 15 du métro automatique du Grand Paris Express avec 4 gares à Vitry (2025-2030), amélioration des lignes de bus existantes, création de navettes de proximité pour relier les quartiers",
                    "source": "Ville de Vitry-sur-Seine",
                    "sourceUrl": "https://www.vitry94.fr/"
                }

        # Aménagement urbain (enrichir si existant)
        elif sous_theme["id"] == "amenagement-urbain":
            if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is not None:
                texte_actuel = sous_theme["propositions"][candidat_id]["texte"]
                sous_theme["propositions"][candidat_id]["texte"] = texte_actuel + ". Projet NPRU Cœur de Ville pour revitaliser le centre, développement équilibré du quartier des Ardoines avec concertation citoyenne sur l'avenir du quartier, refus de la bétonisation excessive"

        # Vélo & Mobilités douces (nouveau)
        elif sous_theme["id"] == "velo-mobilites-douces":
            if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is None:
                sous_theme["propositions"][candidat_id] = {
                    "texte": "Développement des pistes cyclables sécurisées dans toute la ville, création de stationnements vélos près des commerces et des gares du Grand Paris, promotion des mobilités douces avec aménagements piétons",
                    "source": "pbl2026.fr",
                    "sourceUrl": "https://pbl2026.fr/programme.html"
                }

        # Budget participatif (nouveau)
        elif sous_theme["id"] == "budget-participatif":
            if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is None:
                sous_theme["propositions"][candidat_id] = {
                    "texte": "Démocratie de proximité avec plus de 30 ateliers citoyens pour construire le projet municipal, conseils de quartier renforcés, consultation permanente des habitants sur les projets d'aménagement, co-construction de la ville avec les Vitriots",
                    "source": "pbl2026.fr - Démarche participative",
                    "sourceUrl": "https://pbl2026.fr/"
                }

        # Égalité & Discriminations (nouveau)
        elif sous_theme["id"] == "egalite-discriminations":
            if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is None:
                sous_theme["propositions"][candidat_id] = {
                    "texte": "Lutte contre toutes les discriminations (racisme, sexisme, LGBTQIphobies), conseil municipal paritaire avec 15 adjoints au maire, promotion de l'égalité femmes-hommes dans toutes les politiques municipales, soutien aux associations œuvrant pour l'inclusion",
                    "source": "Mairie de Vitry-sur-Seine",
                    "sourceUrl": "https://www.vitry94.fr/les-elus-du-conseil-municipal/"
                }

# Passer programmeComplet à true
for candidat in data["candidats"]:
    if candidat["id"] == candidat_id:
        candidat["programmeComplet"] = True
        print(f"\nprogrammeComplet passé à true pour {candidat['nom']}")

# Compter les propositions après modification
propositions_apres = 0
for categorie in data["categories"]:
    for sous_theme in categorie["sousThemes"]:
        if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is not None:
            propositions_apres += 1

print(f"Propositions après enrichissement : {propositions_apres}")
print(f"Nouvelles propositions ajoutées : {propositions_apres - propositions_avant}")

# Détail des propositions par catégorie
print("\n=== Détail des propositions par catégorie ===")
for categorie in data["categories"]:
    count = 0
    for sous_theme in categorie["sousThemes"]:
        if candidat_id in sous_theme["propositions"] and sous_theme["propositions"][candidat_id] is not None:
            count += 1
    if count > 0:
        print(f"{categorie['nom']} : {count} propositions")

# Sauvegarder le fichier
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✓ Fichier sauvegardé : {path}")
