#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrateur d'extraction de propositions.
Pre-filtre les candidats, detecte les sites Wix/JS-only,
corrige les URLs connues, et genere des batches prets a traiter.

Usage:
  python scripts/orchestrer_extraction.py                    # Scan complet
  python scripts/orchestrer_extraction.py --fix-urls         # Corrige les URLs dans les JSON
  python scripts/orchestrer_extraction.py --min-props 5      # Seuil minimum (defaut: 10)
  python scripts/orchestrer_extraction.py --test-urls        # Teste la crawlabilite des URLs
  python scripts/orchestrer_extraction.py --batch-size 3     # Taille des batches (defaut: 3)
"""

import argparse
import json
import os
import sys
import glob
import time
from urllib.parse import urlparse

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELECTIONS_DIR = os.path.join(BASE_DIR, "data", "elections")

# URLs connues comme fausses -> correctes
URL_FIXES = {
    "https://www.bechu2026.fr/": "https://angersbechu.fr/",
    "https://bechu2026.fr/": "https://angersbechu.fr/",
    "https://www.sophiejoissains.fr/": "https://sophiejoissains2026.fr/",
    "https://sophiejoissains.fr/": "https://sophiejoissains2026.fr/",
    "https://www.laveau2026.fr/": None,  # pas de site, presse locale
    "https://laveau2026.fr/": None,
}

# Signatures de sites JS-only (Wix, SPA, etc.)
WIX_SIGNATURES = [
    "wix-thunderbolt",
    "thunderboltTag",
    "X-Wix-",
    "wixCodeApi",
    "_wixCIDX",
    "platformServicesUrl",
]

SPA_SIGNATURES = [
    '<div id="app"></div>',
    '<div id="root"></div>',
    "window.__NEXT_DATA__",
    "window.__NUXT__",
]


def scan_candidates(min_props=10):
    """Scanne tous les candidats et retourne ceux avec URL + peu de props."""
    candidates = []
    for f in sorted(glob.glob(os.path.join(ELECTIONS_DIR, "*.json"))):
        data = json.load(open(f, encoding="utf-8"))
        ville = data.get("ville", "")
        ville_id = os.path.basename(f).replace("-2026.json", "")
        for c in data.get("candidats", []):
            url = c.get("programmeUrl", "")
            if not url or url == "#":
                continue
            total = 0
            for cat in data.get("categories", []):
                for st in cat.get("sousThemes", []):
                    p = st["propositions"].get(c["id"])
                    if p and p.get("texte"):
                        total += 1
            if total < min_props:
                candidates.append({
                    "ville": ville,
                    "ville_id": ville_id,
                    "candidat_id": c["id"],
                    "candidat_nom": c["nom"],
                    "url": url,
                    "props": total,
                    "programmeComplet": c.get("programmeComplet", False),
                })
    return candidates


def fix_urls(dry_run=False):
    """Corrige les URLs connues comme fausses dans les JSON."""
    fixed = 0
    for f in sorted(glob.glob(os.path.join(ELECTIONS_DIR, "*.json"))):
        data = json.load(open(f, encoding="utf-8"))
        modified = False
        for c in data.get("candidats", []):
            url = c.get("programmeUrl", "")
            if url in URL_FIXES:
                new_url = URL_FIXES[url]
                if new_url is None:
                    # URL invalide, on la supprime
                    if not dry_run:
                        c["programmeUrl"] = "#"
                    print(f"  {c['nom']:30s} : {url} -> SUPPRIME")
                else:
                    if not dry_run:
                        c["programmeUrl"] = new_url
                    print(f"  {c['nom']:30s} : {url} -> {new_url}")
                modified = True
                fixed += 1
        if modified and not dry_run:
            with open(f, "w", encoding="utf-8") as fout:
                json.dump(data, fout, ensure_ascii=False, indent=2)
    return fixed


def test_url_crawlable(url, timeout=10):
    """Teste si une URL est crawlable (pas Wix/JS-only).
    Retourne: ('crawlable', None) | ('js-only', 'wix'|'spa') | ('error', msg)
    """
    if not HAS_REQUESTS:
        return "unknown", "requests non installe"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; PourQuiTuVotes/1.0)"
        }
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if resp.status_code >= 400:
            return "error", f"HTTP {resp.status_code}"

        content = resp.text[:10000]  # Check first 10KB only

        # Check Wix
        for sig in WIX_SIGNATURES:
            if sig in content:
                return "js-only", "wix"

        # Check SPA
        for sig in SPA_SIGNATURES:
            if sig in content:
                # Next.js peut quand meme avoir du contenu SSR
                if "window.__NEXT_DATA__" in content and len(content) > 5000:
                    # Probablement SSR avec contenu
                    continue
                return "js-only", "spa"

        # Check contenu trop court (probablement JS-rendered)
        # Extraire le body approximativement
        body_start = content.find("<body")
        if body_start > 0:
            body_content = content[body_start:]
            # Compter les caracteres de texte visible (heuristique)
            import re
            text_only = re.sub(r'<[^>]+>', '', body_content)
            text_only = re.sub(r'\s+', ' ', text_only).strip()
            if len(text_only) < 200:
                return "js-only", "empty-body"

        return "crawlable", None

    except requests.exceptions.ConnectionError:
        return "error", "connection refused"
    except requests.exceptions.Timeout:
        return "error", "timeout"
    except Exception as e:
        return "error", str(e)[:50]


def test_all_urls(candidates):
    """Teste toutes les URLs et classe les candidats."""
    crawlable = []
    js_only = []
    errors = []

    seen_urls = {}
    for c in candidates:
        url = c["url"]
        domain = urlparse(url).netloc

        # Cache par domaine pour eviter de tester 2x le meme site
        if domain in seen_urls:
            status, detail = seen_urls[domain]
        else:
            print(f"  Test {domain:40s} ...", end=" ", flush=True)
            status, detail = test_url_crawlable(url)
            seen_urls[domain] = (status, detail)
            print(f"{status}" + (f" ({detail})" if detail else ""))
            time.sleep(0.5)  # rate limit

        c["status"] = status
        c["detail"] = detail

        if status == "crawlable":
            crawlable.append(c)
        elif status == "js-only":
            js_only.append(c)
        else:
            errors.append(c)

    return crawlable, js_only, errors


def generate_batches(candidates, batch_size=3):
    """Genere des batches de candidats pour les agents."""
    # Trier : plus de props existantes d'abord (plus de contexte)
    # puis par taille de ville (grandes villes prioritaires)
    candidates.sort(key=lambda c: (-c["props"], c["ville"]))

    batches = []
    for i in range(0, len(candidates), batch_size):
        batch = candidates[i:i + batch_size]
        batches.append(batch)
    return batches


def format_agent_prompt(batch):
    """Genere le prompt pour un agent d'extraction."""
    lines = []
    lines.append('Tu travailles sur le projet "Pour qui tu votes" dans `C:\\Users\\KOPELMANRon\\Downloads\\FR comp mun`.')
    lines.append("")
    lines.append("Ta tache : extraire les propositions de candidats depuis leurs sites web et les inserer dans les JSON d'election.")
    lines.append("")
    lines.append("**Candidats a traiter :**")
    for i, c in enumerate(batch, 1):
        lines.append(f"{i}. {c['candidat_nom']} ({c['ville']}) - {c['url']} - ville: {c['ville_id']}, candidat id: {c['candidat_id']} ({c['props']} props existantes)")
    lines.append("")
    lines.append("**Methode :**")
    lines.append("Pour chaque candidat :")
    lines.append("1. Fetch le site (et les sous-pages programme : /programme, /projet, /nos-engagements, /propositions, etc.)")
    lines.append("2. Si le site est JS-only ou vague, chercher dans la presse locale avec WebSearch : \"[nom] [ville] programme municipales 2026\"")
    lines.append("3. Extraire les propositions concretes (pas de declarations vagues)")
    lines.append("4. Les mapper aux sous-themes : \"categorie/sous-theme\"")
    lines.append("5. Ecrire scripts/tmp_{candidat_id}_props.json")
    lines.append("6. Executer : python scripts/inserer_propositions.py --ville {ville_id} --candidat {candidat_id} --file scripts/tmp_{candidat_id}_props.json")
    lines.append("")
    lines.append("**Format du JSON :**")
    lines.append("```json")
    lines.append('{')
    lines.append('  "categorie/sous-theme": {')
    lines.append('    "texte": "Description de la proposition",')
    lines.append('    "source": "Programme officiel",')
    lines.append('    "sourceUrl": "https://url-source"')
    lines.append('  }')
    lines.append('}')
    lines.append("```")
    lines.append("")
    lines.append("**Les 44 sous-themes :**")
    lines.append("securite: police-municipale, videoprotection, prevention-mediation, violences-femmes")
    lines.append("transports: transports-en-commun, velo-mobilites-douces, pietons-circulation, stationnement, tarifs-gratuite")
    lines.append("logement: logement-social, logements-vacants, encadrement-loyers, acces-logement")
    lines.append("education: petite-enfance, ecoles-renovation, cantines-fournitures, periscolaire-loisirs, jeunesse")
    lines.append("environnement: espaces-verts, proprete-dechets, climat-adaptation, renovation-energetique, alimentation-durable")
    lines.append("sante: centres-sante, prevention-sante, seniors")
    lines.append("democratie: budget-participatif, transparence, vie-associative, services-publics")
    lines.append("economie: commerce-local, emploi-insertion, attractivite")
    lines.append("culture: equipements-culturels, evenements-creation")
    lines.append("sport: equipements-sportifs, sport-pour-tous")
    lines.append("urbanisme: amenagement-urbain, accessibilite, quartiers-prioritaires")
    lines.append("solidarite: aide-sociale, egalite-discriminations, pouvoir-achat")
    lines.append("")
    lines.append("**Important :**")
    lines.append("- Si un site est inaccessible, chercher le bon URL ou utiliser la presse locale")
    lines.append("- Ne pas inserer de propositions trop vagues (\"une ville plus sure\" sans mesure concrete)")
    lines.append("- Privilegier les sous-pages thematiques du site plutot que la page d'accueil")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Orchestrateur d'extraction de propositions")
    parser.add_argument("--min-props", type=int, default=10, help="Seuil max de propositions (defaut: 10)")
    parser.add_argument("--fix-urls", action="store_true", help="Corrige les URLs connues comme fausses")
    parser.add_argument("--test-urls", action="store_true", help="Teste la crawlabilite des URLs")
    parser.add_argument("--batch-size", type=int, default=3, help="Taille des batches (defaut: 3)")
    parser.add_argument("--generate-prompts", action="store_true", help="Genere les prompts pour les agents")
    parser.add_argument("--output", help="Fichier de sortie JSON (defaut: stdout)")
    args = parser.parse_args()

    # Fix URLs si demande
    if args.fix_urls:
        print("=== CORRECTION DES URLs ===")
        fixed = fix_urls()
        print(f"\n  {fixed} URL(s) corrigee(s)")
        print()

    # Scan des candidats
    print("=== SCAN DES CANDIDATS ===")
    candidates = scan_candidates(args.min_props)
    print(f"  {len(candidates)} candidats avec URL et <{args.min_props} propositions")
    print()

    # Test URLs si demande
    if args.test_urls:
        if not HAS_REQUESTS:
            print("ERREUR: pip install requests requis pour --test-urls")
            sys.exit(1)
        print("=== TEST DE CRAWLABILITE ===")
        crawlable, js_only, errors = test_all_urls(candidates)
        print(f"\n  Crawlable : {len(crawlable)}")
        print(f"  JS-only   : {len(js_only)}")
        print(f"  Erreurs   : {len(errors)}")
        print()

        if js_only:
            print("=== SITES JS-ONLY (non crawlables, utiliser presse locale) ===")
            for c in js_only:
                print(f"  {c['candidat_nom']:30s} ({c['ville']:20s}) {c['url'][:50]} [{c['detail']}]")
            print()

        if errors:
            print("=== SITES EN ERREUR ===")
            for c in errors:
                print(f"  {c['candidat_nom']:30s} ({c['ville']:20s}) {c['url'][:50]} [{c['detail']}]")
            print()

        # Ne garder que les crawlables pour les batches
        candidates = crawlable

    # Generer les batches
    batches = generate_batches(candidates, args.batch_size)
    print(f"=== {len(batches)} BATCHES DE {args.batch_size} ===")
    for i, batch in enumerate(batches):
        print(f"\n  Batch {i+1}:")
        for c in batch:
            status = f" [{c.get('status', '?')}]" if args.test_urls else ""
            print(f"    {c['candidat_nom']:30s} ({c['ville']:20s}) {c['props']:2d} props{status}")

    # Generer les prompts si demande
    if args.generate_prompts:
        prompts_dir = os.path.join(BASE_DIR, "scripts", "prompts_agents")
        os.makedirs(prompts_dir, exist_ok=True)
        for i, batch in enumerate(batches):
            prompt = format_agent_prompt(batch)
            path = os.path.join(prompts_dir, f"batch_{i+1:02d}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(prompt)
        print(f"\n  Prompts generes dans {prompts_dir}/")

    # Sortie JSON si demande
    if args.output:
        output = {
            "total_candidates": len(candidates),
            "batches": batches,
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"\n  Sortie JSON : {args.output}")


if __name__ == "__main__":
    main()
