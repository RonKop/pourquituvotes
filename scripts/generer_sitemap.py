#!/usr/bin/env python3
"""
Génère le fichier sitemap.xml à la racine du projet pourquituvotes.fr,
puis lance un Health Check asynchrone de toutes les URLs générées.

Inclut :
- Pages statiques (accueil, enjeux, comparateur, à propos, etc.)
- Pages enjeux (12 catégories issues du schéma)
- Pages villes (depuis villes.json)
- Pages candidats (depuis villes.json)

Usage :
  python scripts/generer_sitemap.py              # génère + health check
  python scripts/generer_sitemap.py --no-check   # génère sans health check
  python scripts/generer_sitemap.py --check-only  # health check seul (sitemap existant)
  python scripts/generer_sitemap.py --concurrency 20  # 20 requêtes simultanées
"""

import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent, parse

# --- Chemins ---
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
VILLES_JSON = os.path.join(DATA_DIR, "villes.json")
SCHEMA_JSON = os.path.join(DATA_DIR, "schema", "schema_elections.json")
OUTPUT_FILE = os.path.join(ROOT_DIR, "sitemap.xml")

BASE_URL = "https://pourquituvotes.fr"
XMLNS = "http://www.sitemaps.org/schemas/sitemap/0.9"

TODAY = datetime.now().strftime("%Y-%m-%d")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def add_url(urlset, loc, lastmod=None, priority=None):
    """Ajoute un élément <url> au <urlset>."""
    url_el = SubElement(urlset, "url")
    loc_el = SubElement(url_el, "loc")
    loc_el.text = loc

    if lastmod:
        lastmod_el = SubElement(url_el, "lastmod")
        lastmod_el.text = lastmod

    if priority is not None:
        priority_el = SubElement(url_el, "priority")
        priority_el.text = f"{priority:.1f}"


def generate_sitemap():
    """Génère sitemap.xml et retourne la liste de toutes les URLs."""
    villes = load_json(VILLES_JSON)
    schema = load_json(SCHEMA_JSON)
    categories = schema["categories"]

    urlset = Element("urlset")
    urlset.set("xmlns", XMLNS)

    all_urls = []

    # --- 1. Pages statiques ---
    static_pages = [
        ("/", 1.0),
        ("/enjeux-2026/", 0.9),
        ("/municipales/2026/", 0.8),
        ("/a-propos", 0.3),
        ("/methodologie", 0.3),
        ("/faq", 0.3),
        ("/presidentielle/2027/", 0.3),
    ]

    for path, priority in static_pages:
        url = f"{BASE_URL}{path}"
        add_url(urlset, url, lastmod=TODAY, priority=priority)
        all_urls.append(url)

    # --- 2. Pages enjeux (12 catégories) --- shells = dossiers → trailing slash
    for cat in categories:
        url = f"{BASE_URL}/enjeux-2026/{cat['id']}/"
        add_url(urlset, url, lastmod=TODAY, priority=0.8)
        all_urls.append(url)

    # --- 3. Pages villes --- shells = dossiers → trailing slash
    for ville in villes:
        ville_id = ville["id"]
        lastmod = ville.get("derniereMaj", TODAY)
        url = f"{BASE_URL}/municipales-2026/{ville_id}/"
        add_url(urlset, url, lastmod=lastmod, priority=0.7)
        all_urls.append(url)

        # --- 4. Pages candidats --- shells = dossiers → trailing slash
        for candidat in ville.get("candidats", []):
            candidat_id = candidat["id"]
            url = f"{BASE_URL}/municipales-2026/{ville_id}/candidats/{candidat_id}/"
            add_url(urlset, url, lastmod=lastmod, priority=0.5)
            all_urls.append(url)

    # --- Écriture du fichier ---
    tree = ElementTree(urlset)
    indent(tree, space="  ")

    with open(OUTPUT_FILE, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)

    n_villes = len(villes)
    n_candidats = len(all_urls) - len(static_pages) - len(categories) - n_villes
    print(f"Sitemap generee : {os.path.abspath(OUTPUT_FILE)}")
    print(f"  - {len(static_pages)} pages statiques")
    print(f"  - {len(categories)} pages enjeux")
    print(f"  - {n_villes} pages villes")
    print(f"  - {n_candidats} pages candidats")
    print(f"  => {len(all_urls)} URLs au total")

    return all_urls


# ─────────────────────────────────────────────────────────
# Health Check asynchrone
# ─────────────────────────────────────────────────────────

def extract_urls_from_sitemap():
    """Lit sitemap.xml et retourne la liste des <loc>."""
    tree = parse(OUTPUT_FILE)
    root = tree.getroot()
    ns = XMLNS
    urls = []
    for url_el in root.findall(f"{{{ns}}}url"):
        loc_el = url_el.find(f"{{{ns}}}loc")
        if loc_el is not None and loc_el.text:
            urls.append(loc_el.text.strip())
    return urls


async def check_url(session, url, semaphore, results):
    """Envoie une requête HEAD et classe le résultat."""
    async with semaphore:
        try:
            async with session.head(url, allow_redirects=False, timeout=15) as resp:
                status = resp.status
                if 200 <= status < 300:
                    results["ok"].append((url, status))
                elif status in (301, 302, 303, 307, 308):
                    location = resp.headers.get("Location", "???")
                    results["redirects"].append((url, status, location))
                else:
                    results["errors"].append((url, status, ""))
        except Exception as e:
            results["errors"].append((url, 0, str(e)))


async def run_health_check(urls, concurrency=10):
    """Lance le health check asynchrone sur toutes les URLs."""
    try:
        import aiohttp
    except ImportError:
        print("\n[!] aiohttp non installe. Installation en cours...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
        import aiohttp

    results = {"ok": [], "redirects": [], "errors": []}
    semaphore = asyncio.Semaphore(concurrency)

    print(f"\n{'='*60}")
    print(f"  HEALTH CHECK — {len(urls)} URLs (concurrence: {concurrency})")
    print(f"{'='*60}")

    start = time.time()

    connector = aiohttp.TCPConnector(limit=concurrency, ssl=False)
    timeout = aiohttp.ClientTimeout(total=30)
    headers = {"User-Agent": "PourQuiTuVotes-SitemapChecker/1.0"}

    async with aiohttp.ClientSession(
        connector=connector, timeout=timeout, headers=headers
    ) as session:
        tasks = [check_url(session, url, semaphore, results) for url in urls]
        done = 0
        total = len(tasks)
        for coro in asyncio.as_completed(tasks):
            await coro
            done += 1
            if done % 50 == 0 or done == total:
                print(f"  ... {done}/{total} testees", end="\r")

    elapsed = time.time() - start
    print(f"\n  Termine en {elapsed:.1f}s\n")

    # --- Rapport ---
    n_ok = len(results["ok"])
    n_redir = len(results["redirects"])
    n_err = len(results["errors"])

    print(f"  OK  {n_ok} pages (2xx)")
    if n_redir:
        print(f"  REDIR  {n_redir} redirections :")
        for url, status, dest in results["redirects"]:
            print(f"       {status} {url}")
            print(f"           -> {dest}")
    if n_err:
        print(f"  ERREUR  {n_err} erreurs :")
        for url, status, detail in results["errors"]:
            label = f"HTTP {status}" if status else "TIMEOUT/ERREUR"
            print(f"       {label} {url}")
            if detail:
                print(f"           {detail}")

    print(f"\n{'='*60}")
    if n_err == 0:
        print(f"  Toutes les {n_ok + n_redir} URLs sont accessibles !")
    else:
        print(f"  {n_err} URL(s) a corriger.")
    print(f"{'='*60}")

    return n_err


def main():
    parser = argparse.ArgumentParser(description="Genere sitemap.xml + health check")
    parser.add_argument(
        "--no-check", action="store_true",
        help="Generer le sitemap sans lancer le health check"
    )
    parser.add_argument(
        "--check-only", action="store_true",
        help="Lancer le health check seul (sitemap existant)"
    )
    parser.add_argument(
        "--concurrency", type=int, default=10,
        help="Nombre max de requetes simultanees (defaut: 10)"
    )
    args = parser.parse_args()

    urls = []

    if not args.check_only:
        urls = generate_sitemap()

    if not args.no_check:
        if not urls:
            if not os.path.exists(OUTPUT_FILE):
                print(f"[!] Sitemap introuvable : {OUTPUT_FILE}")
                sys.exit(1)
            urls = extract_urls_from_sitemap()
        n_err = asyncio.run(run_health_check(urls, concurrency=args.concurrency))
        sys.exit(1 if n_err > 0 else 0)


if __name__ == "__main__":
    main()
