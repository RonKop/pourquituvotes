#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérifie si le CSV résultats municipales 2026 est disponible sur data.gouv.fr.
Si trouvé, le télécharge et lance l'import automatiquement.

Usage :
  python scripts/check_csv_datagouv.py --tour 1
  python scripts/check_csv_datagouv.py --tour 1 --auto-import
  python scripts/check_csv_datagouv.py --tour 2 --auto-import
"""

import sys
import io
import os
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "data")

# URLs connues pour les résultats municipales
# Le Ministère publie sur data.gouv.fr avec un dataset ID stable
# Format typique : resultats-du-premier-tour-des-elections-municipales-2026
DATASET_SEARCH_URLS = [
    "https://www.data.gouv.fr/api/1/datasets/?q=resultats+municipales+2026&page_size=5",
    "https://www.data.gouv.fr/api/1/datasets/?q=elections+municipales+2026+resultats&page_size=5",
]

# URLs directes connues (à mettre à jour quand le dataset est publié)
KNOWN_URLS = {
    "1": [
        "https://www.data.gouv.fr/fr/datasets/r/resultats-t1-municipales-2026.csv",
        "https://static.data.gouv.fr/resources/elections-municipales-2026/resultats-t1.csv",
    ],
    "2": [
        "https://www.data.gouv.fr/fr/datasets/r/resultats-t2-municipales-2026.csv",
        "https://static.data.gouv.fr/resources/elections-municipales-2026/resultats-t2.csv",
    ],
}


def check_url(url):
    """Vérifie si une URL est accessible (HEAD request)."""
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'PQTV-Bot/1.0 (pourquituvotes.fr)')
        resp = urllib.request.urlopen(req, timeout=10)
        content_type = resp.headers.get('Content-Type', '')
        content_length = resp.headers.get('Content-Length', '0')
        print(f"  {url}")
        print(f"    Status: {resp.status}, Type: {content_type}, Size: {content_length}")
        return resp.status == 200
    except (urllib.error.HTTPError, urllib.error.URLError, Exception) as e:
        print(f"  {url} → {e}")
        return False


def search_datagouv(tour):
    """Cherche le dataset résultats sur data.gouv.fr via l'API."""
    print("Recherche sur data.gouv.fr API...")
    tour_keywords = ["premier tour", "1er tour", "tour 1"] if tour == "1" else ["second tour", "2e tour", "tour 2"]

    for search_url in DATASET_SEARCH_URLS:
        try:
            req = urllib.request.Request(search_url)
            req.add_header('User-Agent', 'PQTV-Bot/1.0')
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode('utf-8'))

            for dataset in data.get("data", []):
                title = (dataset.get("title") or "").lower()
                desc = (dataset.get("description") or "").lower()

                # Vérifier si c'est un dataset de résultats
                if "résultat" not in title and "resultat" not in title:
                    continue

                print(f"\n  Dataset trouvé: {dataset.get('title')}")
                print(f"  URL: {dataset.get('page')}")

                # Chercher les ressources CSV
                for resource in dataset.get("resources", []):
                    res_title = (resource.get("title") or "").lower()
                    res_format = (resource.get("format") or "").lower()
                    res_url = resource.get("url", "")

                    if res_format in ("csv", "xlsx") or res_url.endswith(".csv"):
                        # Vérifier si c'est le bon tour
                        is_right_tour = any(kw in res_title or kw in title for kw in tour_keywords)
                        if is_right_tour or "tour" not in res_title.lower():
                            print(f"    Ressource: {resource.get('title')}")
                            print(f"    URL: {res_url}")
                            return res_url

        except Exception as e:
            print(f"  Erreur API: {e}")
            continue

    return None


def download_csv(url, tour):
    """Télécharge le CSV."""
    filename = f"resultats_T{tour}_{datetime.now().strftime('%Y%m%d')}.csv"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    print(f"\nTéléchargement → {filepath}")
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'PQTV-Bot/1.0')
        resp = urllib.request.urlopen(req, timeout=60)
        with open(filepath, 'wb') as f:
            f.write(resp.read())
        size = os.path.getsize(filepath)
        print(f"  OK — {size:,} bytes")
        return filepath
    except Exception as e:
        print(f"  Erreur téléchargement: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Vérifie la dispo CSV résultats data.gouv.fr")
    parser.add_argument("--tour", type=str, choices=["1", "2"], required=True)
    parser.add_argument("--auto-import", action="store_true", help="Lancer import_resultats.py si CSV trouvé")
    args = parser.parse_args()

    print(f"=== Vérification CSV résultats Tour {args.tour} ===")
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    csv_url = None

    # 1. Vérifier les URLs connues
    print("Vérification des URLs connues...")
    for url in KNOWN_URLS.get(args.tour, []):
        if check_url(url):
            csv_url = url
            break

    # 2. Chercher via l'API data.gouv.fr
    if not csv_url:
        csv_url = search_datagouv(args.tour)

    if not csv_url:
        print("\n❌ CSV non encore disponible.")
        print("Réessayez plus tard ou vérifiez manuellement :")
        print("  https://www.data.gouv.fr/fr/search/?q=resultats+municipales+2026")
        print("  https://resultats-elections.interieur.gouv.fr/")
        return 1

    print(f"\n✅ CSV trouvé : {csv_url}")

    # 3. Télécharger
    csv_path = download_csv(csv_url, args.tour)
    if not csv_path:
        return 1

    # 4. Auto-import
    if args.auto_import:
        print(f"\n=== Import automatique Tour {args.tour} ===")
        import subprocess
        result = subprocess.run(
            [sys.executable, "scripts/import_resultats.py", "--tour", args.tour, "--csv", csv_path],
            cwd=ROOT_DIR,
        )
        if result.returncode == 0:
            print("\n✅ Import réussi ! Lancez le pipeline de déploiement :")
            print("  bash scripts/deploy_resultats.sh \"feat: résultats définitifs T" + args.tour + " (CSV officiel)\"")
        return result.returncode
    else:
        print(f"\nCSV téléchargé. Pour importer :")
        print(f"  python scripts/import_resultats.py --tour {args.tour} --csv {csv_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
