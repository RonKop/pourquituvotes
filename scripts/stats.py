#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génération de statistiques sur les données d'élections
Usage: python stats.py
"""

import json
from pathlib import Path
from collections import defaultdict

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def count_propositions(data):
    """Compte les propositions par candidat"""
    counts = defaultdict(int)

    for cat in data.get('categories', []):
        # Format avec sous-thèmes
        if 'sousThemes' in cat:
            for st in cat['sousThemes']:
                for candidat_id, prop in st['propositions'].items():
                    if prop is not None and prop.get('texte'):
                        counts[candidat_id] += 1

        # Format avec propositions directes
        elif 'propositions' in cat:
            for prop in cat['propositions']:
                candidat_id = prop.get('candidatId')
                if candidat_id and prop.get('texte'):
                    counts[candidat_id] += 1

    return counts

def analyze_city(file_path):
    """Analyse un fichier de ville"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return None

    ville = data.get('ville', '?')
    candidats = data.get('candidats', [])
    counts = count_propositions(data)

    # Mapping ID -> nom
    candidats_map = {c['id']: c['nom'] for c in candidats}

    return {
        'ville': ville,
        'nb_candidats': len(candidats),
        'candidats': candidats_map,
        'propositions': counts,
        'total_propositions': sum(counts.values())
    }

def generate_stats():
    """Génère des statistiques globales"""
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    elections_dir = project_dir / "data" / "elections"

    if not elections_dir.exists():
        print(f"{Colors.RED}❌ Dossier 'data/elections' introuvable{Colors.RESET}")
        return

    # Trouver tous les fichiers JSON
    json_files = list(elections_dir.rglob("*.json"))

    if not json_files:
        print(f"{Colors.YELLOW}⚠️  Aucun fichier JSON trouvé{Colors.RESET}")
        return

    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}📊 STATISTIQUES COMPARATEUR MUNICIPAL{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

    # Analyser chaque ville
    villes_stats = []
    for json_file in sorted(json_files):
        stats = analyze_city(json_file)
        if stats:
            villes_stats.append(stats)

    # Statistiques globales
    total_villes = len(villes_stats)
    total_candidats = sum(s['nb_candidats'] for s in villes_stats)
    total_propositions = sum(s['total_propositions'] for s in villes_stats)

    print(f"{Colors.BOLD}📈 Vue d'ensemble{Colors.RESET}")
    print(f"  🏙️  Villes : {Colors.BOLD}{total_villes}{Colors.RESET}")
    print(f"  👥 Candidats : {Colors.BOLD}{total_candidats}{Colors.RESET}")
    print(f"  📝 Propositions : {Colors.BOLD}{total_propositions}{Colors.RESET}")
    print()

    # Détail par ville
    print(f"{Colors.BOLD}🏙️  Détail par ville{Colors.RESET}")
    print(f"{Colors.BOLD}{'─'*70}{Colors.RESET}")

    for stats in villes_stats:
        ville = stats['ville']
        nb_cand = stats['nb_candidats']
        total_prop = stats['total_propositions']

        # Barre de progression visuelle
        max_width = 30
        if total_propositions > 0:
            bar_width = int((total_prop / total_propositions) * max_width)
            bar = '█' * bar_width + '░' * (max_width - bar_width)
        else:
            bar = '░' * max_width

        print(f"\n{Colors.BLUE}{Colors.BOLD}{ville}{Colors.RESET}")
        print(f"  👥 {nb_cand} candidat(s)")
        print(f"  📊 {bar} {total_prop} propositions")

        # Détail par candidat
        for candidat_id, nom in stats['candidats'].items():
            count = stats['propositions'].get(candidat_id, 0)
            if count > 0:
                pct = (count / total_prop * 100) if total_prop > 0 else 0
                print(f"     • {nom}: {Colors.GREEN}{count}{Colors.RESET} ({pct:.1f}%)")
            else:
                print(f"     • {nom}: {Colors.YELLOW}0{Colors.RESET} (aucune proposition)")

    # Villes avec le plus de propositions
    print(f"\n{Colors.BOLD}🏆 Top 5 villes (nombre de propositions){Colors.RESET}")
    print(f"{Colors.BOLD}{'─'*70}{Colors.RESET}")

    top_villes = sorted(villes_stats, key=lambda x: x['total_propositions'], reverse=True)[:5]
    for i, stats in enumerate(top_villes, 1):
        medal = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][i-1]
        print(f"  {medal} {stats['ville']}: {Colors.GREEN}{Colors.BOLD}{stats['total_propositions']}{Colors.RESET} propositions")

    # Alertes
    print(f"\n{Colors.BOLD}⚠️  Alertes{Colors.RESET}")
    print(f"{Colors.BOLD}{'─'*70}{Colors.RESET}")

    villes_vides = [s['ville'] for s in villes_stats if s['total_propositions'] == 0]
    if villes_vides:
        print(f"  {Colors.YELLOW}📭 Villes sans propositions : {', '.join(villes_vides)}{Colors.RESET}")

    candidats_vides = []
    for stats in villes_stats:
        for candidat_id, nom in stats['candidats'].items():
            if stats['propositions'].get(candidat_id, 0) == 0:
                candidats_vides.append(f"{nom} ({stats['ville']})")

    if candidats_vides:
        print(f"  {Colors.YELLOW}👤 Candidats sans propositions : {len(candidats_vides)}{Colors.RESET}")
        if len(candidats_vides) <= 10:
            for cand in candidats_vides:
                print(f"     • {cand}")

    if not villes_vides and not candidats_vides:
        print(f"  {Colors.GREEN}✅ Aucune alerte !{Colors.RESET}")

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def main():
    generate_stats()

if __name__ == "__main__":
    main()
