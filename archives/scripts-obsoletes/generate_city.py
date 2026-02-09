#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de fichier JSON pour une nouvelle ville
Usage: python generate_city.py <nom_ville> [candidat1] [candidat2] ...
Exemple: python generate_city.py Paris "Anne Martin" "Pierre Dupont"
"""

import json
import os
import sys
from pathlib import Path

def slugify(text):
    """Convertit un texte en slug (minuscules, sans accents, tirets)"""
    import unicodedata
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = text.lower().strip()
    text = text.replace(' ', '-')
    return text

def generate_city(ville_nom, candidats_noms):
    """Génère un fichier JSON pour une nouvelle ville"""

    # Chemins
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    template_path = project_dir / "templates" / "city_template.json"
    output_dir = project_dir / "data" / "elections" / "2026"

    # Créer le dossier si nécessaire
    output_dir.mkdir(parents=True, exist_ok=True)

    # Charger le template
    if not template_path.exists():
        print(f"❌ Erreur : Template introuvable à {template_path}")
        return False

    with open(template_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Remplir les informations de base
    data['ville'] = ville_nom

    # Ajouter les candidats
    data['candidats'] = []
    for nom in candidats_noms:
        candidat_id = slugify(nom.split()[0])  # Premier mot du nom comme ID
        data['candidats'].append({
            "id": candidat_id,
            "nom": nom,
            "liste": f"Liste {nom}",  # À personnaliser
            "programmeUrl": "#"
        })

    # Initialiser les propositions pour chaque candidat
    for categorie in data['categories']:
        if 'sousThemes' in categorie:
            for sous_theme in categorie['sousThemes']:
                for candidat in data['candidats']:
                    sous_theme['propositions'][candidat['id']] = None

    # Nom du fichier de sortie
    ville_slug = slugify(ville_nom)
    output_path = output_dir / f"{ville_slug}.json"

    # Vérifier si le fichier existe déjà
    if output_path.exists():
        reponse = input(f"⚠️  Le fichier {output_path.name} existe déjà. Écraser ? (o/N) : ")
        if reponse.lower() != 'o':
            print("❌ Annulé")
            return False

    # Écrire le fichier
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Fichier créé : {output_path}")
    print(f"📝 Ville : {ville_nom}")
    print(f"👥 Candidats : {', '.join(candidats_noms)}")
    print(f"\n💡 Prochaine étape : Éditer {output_path.name} pour ajouter les propositions")

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_city.py <nom_ville> [candidat1] [candidat2] ...")
        print("Exemple: python generate_city.py Paris \"Anne Martin\" \"Pierre Dupont\"")
        sys.exit(1)

    ville_nom = sys.argv[1]
    candidats_noms = sys.argv[2:] if len(sys.argv) > 2 else []

    if not candidats_noms:
        print("⚠️  Aucun candidat spécifié. Le fichier sera créé avec une liste vide.")
        reponse = input("Continuer ? (o/N) : ")
        if reponse.lower() != 'o':
            print("❌ Annulé")
            sys.exit(0)

    success = generate_city(ville_nom, candidats_noms)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
