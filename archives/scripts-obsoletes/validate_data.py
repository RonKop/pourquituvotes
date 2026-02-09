#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation des fichiers JSON d'élections
Usage: python validate_data.py
"""

import json
import os
from pathlib import Path
from urllib.parse import urlparse

class Colors:
    """Codes couleur ANSI pour le terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def validate_url(url):
    """Valide une URL (basique)"""
    if not url or url == "#":
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_election_file(file_path):
    """Valide un fichier JSON d'élection"""
    errors = []
    warnings = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"❌ JSON invalide : {e}"], []
    except Exception as e:
        return [f"❌ Erreur de lecture : {e}"], []

    # Vérifier les champs obligatoires
    required_fields = ['ville', 'annee', 'type', 'candidats', 'categories']
    for field in required_fields:
        if field not in data:
            errors.append(f"Champ obligatoire manquant : '{field}'")

    # Vérifier les candidats
    if 'candidats' in data:
        if not data['candidats']:
            warnings.append("Aucun candidat défini")

        candidat_ids = set()
        for i, candidat in enumerate(data['candidats']):
            # Vérifier les champs du candidat
            for field in ['id', 'nom', 'liste']:
                if field not in candidat:
                    errors.append(f"Candidat {i+1} : champ '{field}' manquant")

            # Vérifier l'unicité des IDs
            if 'id' in candidat:
                if candidat['id'] in candidat_ids:
                    errors.append(f"ID de candidat dupliqué : '{candidat['id']}'")
                candidat_ids.add(candidat['id'])

            # Vérifier l'URL du programme
            if 'programmeUrl' in candidat:
                if not validate_url(candidat['programmeUrl']):
                    warnings.append(f"Candidat '{candidat.get('nom', '?')}' : URL de programme invalide ou placeholder")

    # Vérifier les catégories
    if 'categories' in data:
        if not data['categories']:
            warnings.append("Aucune catégorie définie")

        for cat in data['categories']:
            cat_nom = cat.get('nom', '?')

            # Catégories avec sous-thèmes (format matriciel)
            if 'sousThemes' in cat:
                if not cat['sousThemes']:
                    warnings.append(f"Catégorie '{cat_nom}' : aucun sous-thème")

                for st in cat['sousThemes']:
                    st_nom = st.get('nom', '?')
                    if 'propositions' not in st:
                        errors.append(f"Catégorie '{cat_nom}' > Sous-thème '{st_nom}' : 'propositions' manquant")
                        continue

                    # Vérifier que tous les candidats sont présents
                    for candidat_id in candidat_ids:
                        if candidat_id not in st['propositions']:
                            warnings.append(f"Catégorie '{cat_nom}' > Sous-thème '{st_nom}' : candidat '{candidat_id}' manquant")

                    # Vérifier les propositions
                    for candidat_id, prop in st['propositions'].items():
                        if prop is not None:
                            if 'texte' not in prop:
                                errors.append(f"Catégorie '{cat_nom}' > Sous-thème '{st_nom}' > Candidat '{candidat_id}' : 'texte' manquant")
                            elif not prop['texte'].strip():
                                warnings.append(f"Catégorie '{cat_nom}' > Sous-thème '{st_nom}' > Candidat '{candidat_id}' : texte vide")

                            if 'source' not in prop:
                                warnings.append(f"Catégorie '{cat_nom}' > Sous-thème '{st_nom}' > Candidat '{candidat_id}' : source manquante")

                            if 'sourceUrl' in prop and not validate_url(prop['sourceUrl']):
                                warnings.append(f"Catégorie '{cat_nom}' > Sous-thème '{st_nom}' > Candidat '{candidat_id}' : sourceUrl invalide")

            # Catégories avec propositions directes (ancien format)
            elif 'propositions' in cat:
                for i, prop in enumerate(cat['propositions']):
                    if 'candidatId' not in prop:
                        errors.append(f"Catégorie '{cat_nom}' > Proposition {i+1} : 'candidatId' manquant")

                    if 'texte' not in prop:
                        errors.append(f"Catégorie '{cat_nom}' > Proposition {i+1} : 'texte' manquant")
                    elif not prop['texte'].strip():
                        warnings.append(f"Catégorie '{cat_nom}' > Proposition {i+1} : texte vide")

                    if 'source' not in prop:
                        warnings.append(f"Catégorie '{cat_nom}' > Proposition {i+1} : source manquante")

    return errors, warnings

def validate_all():
    """Valide tous les fichiers JSON d'élections"""
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    elections_dir = project_dir / "data" / "elections"

    if not elections_dir.exists():
        print(f"{Colors.RED}❌ Dossier 'data/elections' introuvable{Colors.RESET}")
        return False

    # Trouver tous les fichiers JSON
    json_files = list(elections_dir.rglob("*.json"))

    if not json_files:
        print(f"{Colors.YELLOW}⚠️  Aucun fichier JSON trouvé dans {elections_dir}{Colors.RESET}")
        return True

    print(f"{Colors.BOLD}🔍 Validation de {len(json_files)} fichier(s)...{Colors.RESET}\n")

    total_errors = 0
    total_warnings = 0

    for json_file in sorted(json_files):
        relative_path = json_file.relative_to(project_dir)
        print(f"{Colors.BLUE}📄 {relative_path}{Colors.RESET}")

        errors, warnings = validate_election_file(json_file)

        if errors:
            total_errors += len(errors)
            for error in errors:
                print(f"  {Colors.RED}❌ {error}{Colors.RESET}")

        if warnings:
            total_warnings += len(warnings)
            for warning in warnings:
                print(f"  {Colors.YELLOW}⚠️  {warning}{Colors.RESET}")

        if not errors and not warnings:
            print(f"  {Colors.GREEN}✅ Aucun problème détecté{Colors.RESET}")

        print()

    # Résumé
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    if total_errors == 0 and total_warnings == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ Tous les fichiers sont valides !{Colors.RESET}")
        return True
    else:
        print(f"{Colors.BOLD}📊 Résumé :{Colors.RESET}")
        if total_errors > 0:
            print(f"  {Colors.RED}❌ {total_errors} erreur(s){Colors.RESET}")
        if total_warnings > 0:
            print(f"  {Colors.YELLOW}⚠️  {total_warnings} avertissement(s){Colors.RESET}")
        return total_errors == 0

def main():
    success = validate_all()
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
