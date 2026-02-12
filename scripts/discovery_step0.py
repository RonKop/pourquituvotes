#!/usr/bin/env python3
"""
#POURQUITUVOTES — Discovery Step 0
Crawl automatique de sites candidats pour détecter les pages programme & PDF.
NE FAIT PAS D'IA — uniquement requests + BeautifulSoup.

Usage:
  python scripts/discovery_step0.py
  python scripts/discovery_step0.py --seeds data/seeds.txt
  python scripts/discovery_step0.py --seeds data/seeds.txt --max-pages 200 --max-depth 1
  python scripts/discovery_step0.py --auto  (extrait les URLs depuis data/elections/*.json)
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse, urlunparse

# === Dépendances ===
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Erreur : installe les dépendances avec :")
    print("  pip install requests beautifulsoup4")
    sys.exit(1)

# === Configuration ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
REGISTRY_PATH = os.path.join(DATA_DIR, "crawl-registry.json")

USER_AGENT = "PourQuiTuVotes-Discovery/1.0 (+https://pourquituvotes.fr)"
RATE_LIMIT = 0.5  # secondes entre requêtes
TIMEOUT = 10  # secondes
SKIP_IF_CHECKED_DAYS = 7  # ne pas revérifier avant X jours

# Mots-clés pour détecter une page "programme"
PROGRAM_KEYWORDS = [
    "programme", "propositions", "projet", "nos-propositions", "mesures",
    "nos-mesures", "nos-engagements", "engagements", "nos-priorites",
    "priorites", "plan", "manifeste", "plateforme", "documents",
    "telecharger", "telechargement", "pdf",
]

# Domaines à exclure (réseaux sociaux, plateformes génériques)
SKIP_DOMAINS = {
    "facebook.com", "twitter.com", "x.com", "instagram.com", "linkedin.com",
    "youtube.com", "tiktok.com", "threads.net", "google.com", "wikipedia.org",
    "legifrance.gouv.fr", "senat.fr", "assemblee-nationale.fr",
}


def normalize_url(url):
    """Normalise une URL : schema+host+path, supprime fragments."""
    parsed = urlparse(url)
    # Forcer https
    scheme = "https"
    host = parsed.hostname or ""
    host = host.lower().rstrip(".")
    # Supprimer www. pour dédup
    if host.startswith("www."):
        host = host[4:]
    path = parsed.path.rstrip("/") or "/"
    # Conserver query si présente
    query = parsed.query
    return urlunparse((scheme, host, path, "", query, ""))


def is_skip_domain(url):
    """Vérifie si l'URL est sur un domaine à ignorer."""
    host = urlparse(url).hostname or ""
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]
    return any(host == d or host.endswith("." + d) for d in SKIP_DOMAINS)


def is_same_site(url, base_url):
    """Vérifie que l'URL est sur le même site que l'URL de base."""
    host1 = (urlparse(url).hostname or "").lower().replace("www.", "")
    host2 = (urlparse(base_url).hostname or "").lower().replace("www.", "")
    return host1 == host2


def is_program_link(url, text=""):
    """Détecte si un lien ressemble à une page programme."""
    url_lower = url.lower()
    text_lower = (text or "").lower()
    # Lien PDF
    if url_lower.endswith(".pdf"):
        return True
    # Mots-clés dans l'URL ou le texte du lien
    combined = url_lower + " " + text_lower
    return any(kw in combined for kw in PROGRAM_KEYWORDS)


def url_hash(url):
    """Hash court d'une URL pour dédup rapide."""
    return hashlib.md5(normalize_url(url).encode()).hexdigest()[:12]


# === Registre (crawl-registry.json) ===

def load_registry():
    """Charge le registre ou crée un nouveau."""
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "candidate_sources": [],
        "source_checks": [],
        "documents": [],
        "coverage_city": [],
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "last_run_at": None,
            "version": "1.0"
        }
    }


def save_registry(registry):
    """Sauvegarde le registre."""
    registry["metadata"]["last_run_at"] = datetime.now().isoformat()
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def was_recently_checked(registry, url, days=SKIP_IF_CHECKED_DAYS):
    """Vérifie si une URL a été vérifiée récemment."""
    norm = normalize_url(url)
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    for check in registry["source_checks"]:
        if normalize_url(check["url"]) == norm and check["checked_at"] > cutoff:
            return True
    return False


def add_source_check(registry, url, http_status, final_url, result, notes=""):
    """Ajoute un log de vérification."""
    registry["source_checks"].append({
        "url": url,
        "checked_at": datetime.now().isoformat(),
        "http_status": http_status,
        "final_url": final_url,
        "result": result,
        "notes": notes
    })


def add_candidate_source(registry, url, source_type="program_page_candidate",
                          candidate_id=None, city_id=None, confidence="medium"):
    """Ajoute une source candidat détectée (dédupliquée par URL normalisée)."""
    norm = normalize_url(url)
    for src in registry["candidate_sources"]:
        if normalize_url(src["url"]) == norm:
            return  # Déjà présent
    registry["candidate_sources"].append({
        "url": url,
        "normalized_url": norm,
        "source_type": source_type,
        "candidate_id": candidate_id,
        "city_id": city_id,
        "discovery_method": "step0",
        "confidence": confidence,
        "status": "new",
        "discovered_at": datetime.now().isoformat()
    })


def add_document(registry, url, doc_type="program_candidate", file_hash=None):
    """Ajoute un document détecté (dédupliqué par URL normalisée)."""
    norm = normalize_url(url)
    now = datetime.now().isoformat()
    for doc in registry["documents"]:
        if normalize_url(doc["url"]) == norm:
            doc["last_seen"] = now
            return  # Déjà présent, MAJ last_seen
    registry["documents"].append({
        "url": url,
        "normalized_url": norm,
        "doc_type": doc_type,
        "file_hash": file_hash,
        "first_seen": now,
        "last_seen": now,
        "status": "new"
    })


# === Extraction des seeds depuis les JSON élections ===

def extract_seeds_from_elections():
    """Extrait les programmeUrl de tous les candidats dans data/elections/*.json."""
    seeds = []
    if not os.path.isdir(ELECTIONS_DIR):
        return seeds
    for filename in sorted(os.listdir(ELECTIONS_DIR)):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(ELECTIONS_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue
        city_id = filename.replace("-2026.json", "")
        for candidat in data.get("candidats", []):
            url = candidat.get("programmeUrl", "")
            if url and url != "#" and url.startswith("http"):
                seeds.append({
                    "url": url,
                    "candidate_id": candidat.get("id"),
                    "city_id": city_id
                })
    return seeds


def load_seeds_file(path):
    """Charge les seeds depuis un fichier texte (1 URL par ligne)."""
    seeds = []
    if not os.path.exists(path):
        print(f"  Fichier seeds introuvable : {path}")
        return seeds
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and line.startswith("http"):
                seeds.append({"url": line, "candidate_id": None, "city_id": None})
    return seeds


# === Crawl ===

def fetch_page(url, session):
    """Fetch une URL et retourne (response, content_type) ou (None, None)."""
    try:
        resp = session.get(url, timeout=TIMEOUT, allow_redirects=True)
        content_type = resp.headers.get("Content-Type", "").lower()
        return resp, content_type
    except requests.RequestException as e:
        return None, str(e)


def extract_links(html, base_url):
    """Extrait tous les liens <a href> d'une page HTML."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue
        # Résoudre les URLs relatives
        full_url = urljoin(base_url, href)
        text = a.get_text(strip=True)[:100]
        links.append({"url": full_url, "text": text})
    return links


def crawl_seed(seed, registry, session, max_depth=1, stats=None):
    """Crawl une URL seed et ses liens programme (depth 1)."""
    url = seed["url"]
    candidate_id = seed.get("candidate_id")
    city_id = seed.get("city_id")

    # Skip si déjà vérifié récemment
    if was_recently_checked(registry, url):
        stats["skipped"] += 1
        return

    time.sleep(RATE_LIMIT)
    resp, content_type = fetch_page(url, session)

    if resp is None:
        add_source_check(registry, url, 0, "", "fail", notes=content_type)
        stats["errors"] += 1
        return

    final_url = resp.url
    status = resp.status_code

    if status >= 400:
        add_source_check(registry, url, status, final_url, "fail")
        stats["errors"] += 1
        return

    add_source_check(registry, url, status, final_url, "ok")
    stats["checked"] += 1

    # Cas PDF direct
    if "pdf" in content_type or url.lower().endswith(".pdf"):
        file_hash = hashlib.md5(resp.content).hexdigest() if len(resp.content) < 50_000_000 else None
        add_document(registry, final_url, file_hash=file_hash)
        add_candidate_source(registry, final_url, source_type="pdf_direct",
                              candidate_id=candidate_id, city_id=city_id,
                              confidence="high")
        stats["pdfs"] += 1
        return

    # Cas HTML
    if "html" not in content_type:
        return

    stats["html"] += 1
    html = resp.text

    # Extraire les liens
    links = extract_links(html, final_url)

    # Chercher les liens "programme" dans la page
    program_links = []
    for link in links:
        link_url = link["url"]
        link_text = link["text"]

        # Ignorer les domaines externes (sauf PDF)
        if not is_same_site(link_url, final_url) and not link_url.lower().endswith(".pdf"):
            continue
        if is_skip_domain(link_url):
            continue

        if is_program_link(link_url, link_text):
            program_links.append(link)

    # Enregistrer les liens programme trouvés
    for plink in program_links:
        purl = plink["url"]
        if purl.lower().endswith(".pdf"):
            add_document(registry, purl, doc_type="program_candidate")
            add_candidate_source(registry, purl, source_type="pdf_linked",
                                  candidate_id=candidate_id, city_id=city_id,
                                  confidence="high")
            stats["pdfs"] += 1
        else:
            add_candidate_source(registry, purl, source_type="program_page_candidate",
                                  candidate_id=candidate_id, city_id=city_id,
                                  confidence="medium")
            stats["program_links"] += 1

    # Depth 1 : crawler les liens programme trouvés
    if max_depth >= 1:
        for plink in program_links[:10]:  # Limiter à 10 liens par seed
            purl = plink["url"]
            if was_recently_checked(registry, purl):
                continue
            if purl.lower().endswith(".pdf"):
                # Télécharger le PDF pour obtenir le hash
                time.sleep(RATE_LIMIT)
                resp2, ct2 = fetch_page(purl, session)
                if resp2 and resp2.status_code < 400 and "pdf" in (ct2 or ""):
                    file_hash = hashlib.md5(resp2.content).hexdigest() if len(resp2.content) < 50_000_000 else None
                    add_document(registry, resp2.url, file_hash=file_hash)
                    add_source_check(registry, purl, resp2.status_code, resp2.url, "ok")
                elif resp2:
                    add_source_check(registry, purl, resp2.status_code, resp2.url, "fail")
                stats["checked"] += 1
            else:
                # Crawler la sous-page programme
                time.sleep(RATE_LIMIT)
                resp2, ct2 = fetch_page(purl, session)
                if resp2 and resp2.status_code < 400 and "html" in (ct2 or ""):
                    add_source_check(registry, purl, resp2.status_code, resp2.url, "ok")
                    # Chercher des PDF dans cette sous-page
                    sub_links = extract_links(resp2.text, resp2.url)
                    for sl in sub_links:
                        if sl["url"].lower().endswith(".pdf"):
                            add_document(registry, sl["url"], doc_type="program_candidate")
                            add_candidate_source(registry, sl["url"], source_type="pdf_linked_depth1",
                                                  candidate_id=candidate_id, city_id=city_id,
                                                  confidence="medium")
                            stats["pdfs"] += 1
                elif resp2:
                    add_source_check(registry, purl, resp2.status_code, resp2.url, "fail")
                stats["checked"] += 1


def update_city_coverage(registry):
    """Met à jour le tableau coverage_city depuis les données élections."""
    registry["coverage_city"] = []
    if not os.path.isdir(ELECTIONS_DIR):
        return
    for filename in sorted(os.listdir(ELECTIONS_DIR)):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(ELECTIONS_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue
        city_id = filename.replace("-2026.json", "")
        candidats = data.get("candidats", [])
        with_program = sum(1 for c in candidats if c.get("programmeUrl", "#") != "#")
        with_complete = sum(1 for c in candidats if c.get("programmeComplet", False))
        registry["coverage_city"].append({
            "city_id": city_id,
            "city_name": data.get("ville", city_id),
            "candidates_count": len(candidats),
            "with_url_count": with_program,
            "with_program_complete_count": with_complete,
            "last_full_review_at": None,
            "priority_score": max(0, len(candidats) - with_complete)
        })


# === Main ===

def main():
    parser = argparse.ArgumentParser(description="Discovery Step 0 — Crawl sites candidats")
    parser.add_argument("--seeds", type=str, default=None,
                        help="Fichier seeds (1 URL par ligne)")
    parser.add_argument("--auto", action="store_true",
                        help="Extraire les seeds depuis data/elections/*.json")
    parser.add_argument("--max-pages", type=int, default=500,
                        help="Nombre max de pages à crawler (défaut: 500)")
    parser.add_argument("--max-depth", type=int, default=1,
                        help="Profondeur de crawl (défaut: 1)")
    args = parser.parse_args()

    print("=" * 60)
    print("  POURQUITUVOTES — Discovery Step 0")
    print("=" * 60)

    # Charger le registre
    registry = load_registry()
    print(f"\nRegistre : {REGISTRY_PATH}")
    print(f"  Sources existantes : {len(registry['candidate_sources'])}")
    print(f"  Checks existants  : {len(registry['source_checks'])}")
    print(f"  Documents existants: {len(registry['documents'])}")

    # Collecter les seeds
    seeds = []
    if args.auto or (args.seeds is None):
        print("\nExtraction auto des seeds depuis data/elections/*.json...")
        seeds = extract_seeds_from_elections()
        print(f"  {len(seeds)} URLs de candidats trouvées")
    if args.seeds:
        print(f"\nChargement des seeds depuis {args.seeds}...")
        file_seeds = load_seeds_file(args.seeds)
        print(f"  {len(file_seeds)} URLs chargées")
        seeds.extend(file_seeds)

    if not seeds:
        print("\nAucune seed trouvée. Utilise --auto ou --seeds <fichier>.")
        sys.exit(0)

    # Dédupliquer les seeds par URL normalisée
    seen = set()
    unique_seeds = []
    for s in seeds:
        norm = normalize_url(s["url"])
        if norm not in seen and not is_skip_domain(s["url"]):
            seen.add(norm)
            unique_seeds.append(s)
    seeds = unique_seeds[:args.max_pages]
    print(f"\n{len(seeds)} seeds uniques à crawler (max: {args.max_pages})")

    # Session HTTP
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    # Stats
    stats = {
        "checked": 0, "html": 0, "pdfs": 0,
        "program_links": 0, "errors": 0, "skipped": 0
    }

    # Crawl
    print(f"\nCrawl en cours (depth={args.max_depth}, rate={RATE_LIMIT}s)...\n")
    for i, seed in enumerate(seeds):
        pct = round((i + 1) / len(seeds) * 100)
        host = urlparse(seed["url"]).hostname or "?"
        cid = seed.get("candidate_id") or "?"
        print(f"  [{i+1}/{len(seeds)}] {pct}% — {host} ({cid})", end="\r")

        try:
            crawl_seed(seed, registry, session, max_depth=args.max_depth, stats=stats)
        except Exception as e:
            print(f"\n  ERREUR sur {seed['url']}: {e}")
            stats["errors"] += 1

    # Mettre à jour la couverture villes
    update_city_coverage(registry)

    # Sauvegarder
    save_registry(registry)

    # === Résumé ===
    print("\n" + "=" * 60)
    print("  RÉSUMÉ")
    print("=" * 60)
    print(f"  Seeds traitées     : {len(seeds)}")
    print(f"  Pages vérifiées    : {stats['checked']}")
    print(f"  Pages HTML         : {stats['html']}")
    print(f"  PDFs détectés      : {stats['pdfs']}")
    print(f"  Liens programme    : {stats['program_links']}")
    print(f"  Erreurs            : {stats['errors']}")
    print(f"  Skippées (récent)  : {stats['skipped']}")
    print(f"\n  Total sources      : {len(registry['candidate_sources'])}")
    print(f"  Total documents    : {len(registry['documents'])}")
    print(f"  Total villes       : {len(registry['coverage_city'])}")

    # Top villes par priorité
    top = sorted(registry["coverage_city"], key=lambda c: c["priority_score"], reverse=True)[:10]
    if top:
        print("\n  Top 10 villes à compléter :")
        for c in top:
            print(f"    {c['city_name']:25s}  {c['candidates_count']} candidats, "
                  f"{c['with_program_complete_count']} complets, "
                  f"priorité={c['priority_score']}")

    # Top domaines
    domains = {}
    for src in registry["candidate_sources"]:
        host = urlparse(src["url"]).hostname or "?"
        domains[host] = domains.get(host, 0) + 1
    top_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]
    if top_domains:
        print("\n  Top 10 domaines :")
        for d, n in top_domains:
            print(f"    {d:40s}  {n} liens")

    print(f"\nRegistre sauvegardé : {REGISTRY_PATH}")
    print("Terminé.")


if __name__ == "__main__":
    main()
