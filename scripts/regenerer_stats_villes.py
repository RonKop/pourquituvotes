#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de régénération des statistiques de villes.json
Recalcule candidats, propositions, themes, complets pour chaque ville
"""

import sys
import io
import json
import os
from pathlib import Path
from collections import defaultdict

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def compter_propositions(categories):
    """Compte le nombre total de mesures dans toutes les catégories."""
    total = 0
    for categorie in categories:
        for sous_theme in categorie.get('sousThemes', []):
            propositions = sous_theme.get('propositions', {})
            for candidat_id, prop in propositions.items():
                if prop and prop.get('mesures'):
                    total += len(prop['mesures'])
    return total

def compter_themes(categories):
    """Compte le nombre de catégories ayant au moins une mesure."""
    themes_avec_props = 0
    for categorie in categories:
        a_une_proposition = False
        for sous_theme in categorie.get('sousThemes', []):
            propositions = sous_theme.get('propositions', {})
            if any(prop and prop.get('mesures') for prop in propositions.values()):
                a_une_proposition = True
                break
        if a_une_proposition:
            themes_avec_props += 1
    return themes_avec_props

def compter_complets(candidats):
    """Compte le nombre de candidats avec programmeComplet: true."""
    return sum(1 for c in candidats if c.get('programmeComplet', False))

def calculer_stats_ville(ville_data):
    """Calcule les stats pour une ville."""
    candidats = ville_data.get('candidats', [])
    categories = ville_data.get('categories', [])

    return {
        'candidats': len(candidats),
        'propositions': compter_propositions(categories),
        'themes': compter_themes(categories),
        'complets': compter_complets(candidats)
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Régénère les stats de villes.json')
    parser.add_argument('--apply', action='store_true', help='Applique vraiment les changements (sinon dry-run)')
    args = parser.parse_args()

    # Chemins
    base_dir = Path(__file__).resolve().parent.parent
    elections_dir = base_dir / 'data' / 'elections'
    villes_path = base_dir / 'data' / 'villes.json'

    if not elections_dir.exists():
        print(f"❌ Dossier introuvable: {elections_dir}")
        return 1

    if not villes_path.exists():
        print(f"❌ Fichier introuvable: {villes_path}")
        return 1

    # Charger villes.json
    print(f"📖 Lecture de {villes_path}")
    with open(villes_path, 'r', encoding='utf-8') as f:
        villes = json.load(f)

    print(f"   → {len(villes)} villes trouvées\n")

    # Map pour accès rapide par election_id
    # Une ville peut avoir plusieurs élections (ex: ["paris-2026"])
    # On crée une map: election_id -> ville_entry
    election_to_ville = {}
    for ville in villes:
        for election_id in ville.get('elections', []):
            election_to_ville[election_id] = ville

    # Lire tous les fichiers elections/*.json
    elections_files = sorted(elections_dir.glob('*.json'))
    print(f"📂 Fichiers elections trouvés: {len(elections_files)}\n")

    changements = []
    aucun_changement = []

    for filepath in elections_files:
        print(f"🔍 {filepath.name}")

        with open(filepath, 'r', encoding='utf-8') as f:
            ville_data = json.load(f)

        # L'ID est le nom du fichier sans .json
        election_id = filepath.stem
        ville_nom = ville_data.get('ville')

        if election_id not in election_to_ville:
            print(f"   ⚠️  Election '{election_id}' pas dans villes.json, skip\n")
            continue

        # Calculer nouvelles stats
        nouvelles_stats = calculer_stats_ville(ville_data)

        # Comparer avec l'existant
        ville_entry = election_to_ville[election_id]
        anciennes_stats = ville_entry.get('stats', {})
        if not anciennes_stats:
            # Si pas de stats, créer structure vide
            anciennes_stats = {
                'candidats': 0,
                'propositions': 0,
                'themes': 0,
                'complets': 0
            }

        # Vérifier si changement
        a_change = False
        details = []
        for key in ['candidats', 'propositions', 'themes', 'complets']:
            ancien = anciennes_stats[key]
            nouveau = nouvelles_stats[key]
            if ancien != nouveau:
                a_change = True
                details.append(f"   • {key}: {ancien} → {nouveau}")

        if a_change:
            print(f"   ✏️  {ville_nom} ({election_id})")
            for detail in details:
                print(detail)
            changements.append({
                'election_id': election_id,
                'ville_id': ville_entry['id'],
                'nom': ville_nom,
                'stats': nouvelles_stats,
                'details': details
            })
        else:
            print(f"   ✓ Aucun changement ({nouvelles_stats['candidats']} candidats, {nouvelles_stats['propositions']} props)")
            aucun_changement.append(ville_nom)

        print()

    # Résumé
    print("=" * 70)
    print(f"📊 RÉSUMÉ")
    print("=" * 70)
    print(f"Villes avec changements: {len(changements)}")
    print(f"Villes sans changement: {len(aucun_changement)}")
    print()

    if changements:
        print("🔄 Changements détectés:")
        for ch in changements:
            print(f"\n{ch['nom']} ({ch['election_id']}):")
            for detail in ch['details']:
                print(detail)

        if args.apply:
            # Appliquer les changements
            print("\n" + "=" * 70)
            print("✍️  APPLICATION DES CHANGEMENTS...")
            print("=" * 70)

            for ch in changements:
                # Trouver la ville dans la liste
                ville_entry = election_to_ville[ch['election_id']]
                # Mettre à jour stats
                if 'stats' not in ville_entry:
                    ville_entry['stats'] = {}
                for key, value in ch['stats'].items():
                    ville_entry['stats'][key] = value

            # Écrire villes.json
            with open(villes_path, 'w', encoding='utf-8') as f:
                json.dump(villes, f, ensure_ascii=False, indent=2)

            print(f"✅ {villes_path} mis à jour ({len(changements)} villes modifiées)")
        else:
            print("\n" + "=" * 70)
            print("🔍 MODE DRY-RUN (pas de modifications)")
            print("   Relancez avec --apply pour appliquer les changements")
            print("=" * 70)
    else:
        print("✅ Toutes les stats sont à jour!")

    return 0

if __name__ == '__main__':
    sys.exit(main())
