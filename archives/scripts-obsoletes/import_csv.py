#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import de propositions depuis un fichier CSV vers JSON
Usage: python import_csv.py <ville> <fichier.csv>

Format CSV attendu:
candidat,categorie,sous_theme,texte,source,source_url

Exemple:
Anne Dupont,Transports & Mobilité,Tramway & Métro,Extension du tramway ligne C,Programme p.22,https://...
"""

import csv
import json
import sys
from pathlib import Path

def slugify(text):
    """Convertit un texte en slug"""
    import unicodedata
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = text.lower().strip()
    text = text.replace(' ', '-')
    text = text.replace('&', 'et')
    return text

def import_csv_to_json(ville_slug, csv_path):
    """Importe des propositions depuis un CSV vers le JSON de la ville"""

    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    json_path = project_dir / "data" / "elections" / "2026" / f"{ville_slug}.json"

    # Vérifier que le fichier JSON existe
    if not json_path.exists():
        print(f"❌ Erreur : Le fichier {json_path} n'existe pas")
        print(f"💡 Utilisez d'abord : python generate_city.py <ville>")
        return False

    # Charger le JSON existant
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Créer un mapping des candidats par nom
    candidats_map = {c['nom']: c['id'] for c in data['candidats']}

    # Créer un mapping des catégories et sous-thèmes
    categories_map = {}
    for cat in data['categories']:
        cat_nom = cat['nom']
        categories_map[cat_nom] = cat

        if 'sousThemes' in cat:
            cat['sousThemes_map'] = {st['nom']: st for st in cat['sousThemes']}

    # Lire le CSV
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du CSV : {e}")
        return False

    # Colonnes attendues
    required_columns = ['candidat', 'categorie', 'texte']
    if not all(col in reader.fieldnames for col in required_columns):
        print(f"❌ Colonnes manquantes. Colonnes requises : {', '.join(required_columns)}")
        print(f"📋 Colonnes trouvées : {', '.join(reader.fieldnames)}")
        return False

    # Traiter chaque ligne
    count_imported = 0
    count_skipped = 0

    for i, row in enumerate(rows, 1):
        candidat_nom = row.get('candidat', '').strip()
        categorie_nom = row.get('categorie', '').strip()
        sous_theme_nom = row.get('sous_theme', '').strip()
        texte = row.get('texte', '').strip()
        source = row.get('source', '').strip()
        source_url = row.get('source_url', '#').strip()

        # Vérifications
        if not candidat_nom or not categorie_nom or not texte:
            print(f"⚠️  Ligne {i} : candidat, catégorie ou texte manquant - ignorée")
            count_skipped += 1
            continue

        if candidat_nom not in candidats_map:
            print(f"⚠️  Ligne {i} : candidat '{candidat_nom}' inconnu - ignorée")
            count_skipped += 1
            continue

        if categorie_nom not in categories_map:
            print(f"⚠️  Ligne {i} : catégorie '{categorie_nom}' inconnue - ignorée")
            count_skipped += 1
            continue

        candidat_id = candidats_map[candidat_nom]
        categorie = categories_map[categorie_nom]

        # Proposition pour catégorie avec sous-thèmes
        if 'sousThemes' in categorie:
            if not sous_theme_nom:
                print(f"⚠️  Ligne {i} : sous-thème manquant pour catégorie '{categorie_nom}' - ignorée")
                count_skipped += 1
                continue

            if sous_theme_nom not in categorie.get('sousThemes_map', {}):
                print(f"⚠️  Ligne {i} : sous-thème '{sous_theme_nom}' inconnu - ignorée")
                count_skipped += 1
                continue

            sous_theme = categorie['sousThemes_map'][sous_theme_nom]

            # Ajouter la proposition
            sous_theme['propositions'][candidat_id] = {
                "texte": texte,
                "source": source or "Source à compléter",
                "sourceUrl": source_url or "#"
            }

        # Proposition pour catégorie avec liste directe
        else:
            if 'propositions' not in categorie:
                categorie['propositions'] = []

            categorie['propositions'].append({
                "candidatId": candidat_id,
                "texte": texte,
                "source": source or "Source à compléter",
                "sourceUrl": source_url or "#"
            })

        count_imported += 1

    # Nettoyer les mapping temporaires
    for cat in data['categories']:
        if 'sousThemes_map' in cat:
            del cat['sousThemes_map']

    # Sauvegarder le JSON mis à jour
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Import terminé !")
    print(f"📊 {count_imported} proposition(s) importée(s)")
    if count_skipped > 0:
        print(f"⚠️  {count_skipped} ligne(s) ignorée(s)")
    print(f"💾 Fichier mis à jour : {json_path}")

    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python import_csv.py <ville_slug> <fichier.csv>")
        print("Exemple: python import_csv.py bordeaux propositions.csv")
        print("\nFormat CSV attendu:")
        print("candidat,categorie,sous_theme,texte,source,source_url")
        sys.exit(1)

    ville_slug = sys.argv[1]
    csv_path = sys.argv[2]

    if not Path(csv_path).exists():
        print(f"❌ Erreur : Le fichier {csv_path} n'existe pas")
        sys.exit(1)

    success = import_csv_to_json(ville_slug, csv_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
