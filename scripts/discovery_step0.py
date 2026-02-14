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
  python scripts/discovery_step0.py --auto --workers 5 --purge-days 30
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import sys
import threading
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
RATE_LIMIT = 0.5  # secondes entre requêtes par domaine
TIMEOUT = 10  # secondes
SKIP_IF_CHECKED_DAYS = 7  # ne pas revérifier avant X jours
MAX_PDF_SIZE = 100 * 1024 * 1024  # 100 MB
STREAM_THRESHOLD = 10 * 1024 * 1024  # 10 MB — streaming au-delà

# Mots-clés pour détecter une page "programme"
PROGRAM_KEYWORDS = [
    "programme", "propositions", "projet", "nos-propositions", "mesures",
    "nos-mesures", "nos-engagements", "engagements", "nos-priorites",
    "priorites", "plan", "manifeste", "plateforme", "documents",
    "telecharger", "telechargement", "pdf",
    "nos-actions", "mon-projet", "vision", "ambition", "tract",
    "kit-militant", "campagne", "nos-combats", "enjeux",
]

# Pattern numérique type "132-propositions"
PROGRAM_NUMERIC_RE = re.compile(r"\d+-propositions?|\d+-mesures?|\d+-engagements?")

# Faux positifs à exclure
FALSE_POSITIVE_KEYWORDS = [
    "programme-tv", "mentions-legales", "conditions-generales",
    "cookies", "confidentialite", "recrutement", "emploi",
    "don", "contact", "politique-de-confidentialite",
]

# Domaines à exclure (réseaux sociaux, plateformes génériques)
SKIP_DOMAINS = {
    "facebook.com", "twitter.com", "x.com", "instagram.com", "linkedin.com",
    "youtube.com", "tiktok.com", "threads.net", "google.com", "wikipedia.org",
    "legifrance.gouv.fr", "senat.fr", "assemblee-nationale.fr",
}

# === Rate limiter par domaine ===
_domain_locks = {}
_domain_lock_mutex = threading.Lock()
_domain_last_request = {}


def domain_rate_limit(url):
    """Attend si nécessaire pour respecter le rate limit par domaine."""
    host = (urlparse(url).hostname or "").lower()
    with _domain_lock_mutex:
        if host not in _domain_locks:
            _domain_locks[host] = threading.Lock()
    lock = _domain_locks[host]
    with lock:
        now = time.monotonic()
        last = _domain_last_request.get(host, 0)
        wait = RATE_LIMIT - (now - last)
        if wait > 0:
            time.sleep(wait)
        _domain_last_request[host] = time.monotonic()


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
    combined = url_lower + " " + text_lower

    # Exclure les faux positifs
    if any(fp in combined for fp in FALSE_POSITIVE_KEYWORDS):
        return False

    # Lien PDF
    if url_lower.endswith(".pdf"):
        return True

    # Pattern numérique (ex: "132-propositions")
    if PROGRAM_NUMERIC_RE.search(combined):
        return True

    # Mots-clés dans l'URL ou le texte du lien
    return any(kw in combined for kw in PROGRAM_KEYWORDS)


def url_hash(url):
    """Hash court d'une URL pour dédup rapide."""
    return hashlib.md5(normalize_url(url).encode()).hexdigest()[:12]


# === Analyse du contenu HTML ===

ELECTORAL_WORDS = [
    "proposition", "mesure", "engagement", "candidat", "municipale",
    "élection", "mandat", "programme", "liste", "électeur",
    "promesse", "priorité", "action", "réalisation", "projet",
]


def analyze_page_content(html):
    """Analyse le contenu HTML et retourne un score de pertinence (0-100)."""
    soup = BeautifulSoup(html, "html.parser")
    score = 0

    # Signal 1 : mots-clés dans les titres (h1-h3)
    for tag in soup.find_all(["h1", "h2", "h3"]):
        title_text = tag.get_text(strip=True).lower()
        for word in ELECTORAL_WORDS:
            if word in title_text:
                score += 10
                break  # max 10 par titre

    # Signal 2 : listes longues (>5 éléments li)
    for ul in soup.find_all(["ul", "ol"]):
        items = ul.find_all("li")
        if len(items) > 5:
            score += 10
            # Bonus si les items contiennent des mots-clés
            items_text = " ".join(li.get_text(strip=True).lower() for li in items[:10])
            if any(w in items_text for w in ELECTORAL_WORDS):
                score += 10

    # Signal 3 : densité de mots-clés dans le corps
    body_text = soup.get_text(separator=" ", strip=True).lower()
    keyword_count = sum(body_text.count(w) for w in ELECTORAL_WORDS)
    if keyword_count > 20:
        score += 20
    elif keyword_count > 10:
        score += 10
    elif keyword_count > 5:
        score += 5

    # Signal 4 : présence de PDF links
    pdf_links = [a for a in soup.find_all("a", href=True) if a["href"].lower().endswith(".pdf")]
    if pdf_links:
        score += 10

    return min(score, 100)


def content_score_to_confidence(score):
    """Convertit un score de contenu en niveau de confiance."""
    if score > 50:
        return "high"
    elif score >= 20:
        return "medium"
    return "low"


# === Détection JS-rendered / Cloudflare ===

def detect_js_rendered(html):
    """Détecte si une page nécessite JavaScript pour afficher son contenu."""
    if not html:
        return False
    lower = html.lower()
    # Body très court avec des scripts → probablement une SPA
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("body")
    if body:
        body_text = body.get_text(strip=True)
        scripts = body.find_all("script")
        if len(body_text) < 500 and len(scripts) > 0:
            return True
    # Noscript avec message JavaScript
    for noscript in soup.find_all("noscript"):
        ns_text = noscript.get_text(strip=True).lower()
        if "javascript" in ns_text or "enable javascript" in ns_text or "activer javascript" in ns_text:
            return True
    return False


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
            "version": "2.0"
        }
    }


def save_registry(registry):
    """Sauvegarde le registre."""
    registry["metadata"]["last_run_at"] = datetime.now().isoformat()
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def purge_old_checks(registry, keep_days=30):
    """Purge les source_checks plus vieux que keep_days jours."""
    cutoff = (datetime.now() - timedelta(days=keep_days)).isoformat()
    before = len(registry["source_checks"])
    registry["source_checks"] = [
        c for c in registry["source_checks"] if c.get("checked_at", "") > cutoff
    ]
    after = len(registry["source_checks"])
    purged = before - after
    if purged > 0:
        print(f"  Purge : {purged} checks supprimés (>{keep_days} jours)")
    return purged


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


def add_document(registry, url, doc_type="program_candidate", file_hash=None, run_changes=None):
    """Ajoute un document détecté (dédupliqué par URL normalisée).
    Détecte les changements de hash pour les documents existants."""
    norm = normalize_url(url)
    now = datetime.now().isoformat()
    for doc in registry["documents"]:
        if normalize_url(doc["url"]) == norm:
            doc["last_seen"] = now
            # Détection de changement de hash
            if file_hash and doc.get("file_hash") and doc["file_hash"] != file_hash:
                old_hash = doc["file_hash"]
                doc["previous_hash"] = old_hash
                doc["file_hash"] = file_hash
                doc["status"] = "updated"
                # Historique des changements
                if "change_history" not in doc:
                    doc["change_history"] = []
                doc["change_history"].append({
                    "date": now,
                    "old_hash": old_hash,
                    "new_hash": file_hash
                })
                if run_changes is not None:
                    run_changes["updated_docs"].append(doc["url"])
            elif file_hash and not doc.get("file_hash"):
                doc["file_hash"] = file_hash
            return  # Existant, mis à jour
    registry["documents"].append({
        "url": url,
        "normalized_url": norm,
        "doc_type": doc_type,
        "file_hash": file_hash,
        "first_seen": now,
        "last_seen": now,
        "status": "new"
    })
    if run_changes is not None:
        run_changes["new_sources"].append(url)


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


# === Fetch avec retry ===

def fetch_with_retry(url, session, retries=2, backoff=1.0):
    """Fetch une URL avec retry et backoff exponentiel.
    3 tentatives max (1 initiale + 2 retries), délai 1s → 2s."""
    last_error = None
    for attempt in range(1 + retries):
        try:
            resp = session.get(url, timeout=TIMEOUT, allow_redirects=True)
            return resp
        except requests.RequestException as e:
            last_error = e
            if attempt < retries:
                wait = backoff * (2 ** attempt)
                time.sleep(wait)
    raise last_error


def check_pdf_size(url, session):
    """Vérifie la taille d'un PDF via HEAD avant le GET.
    Retourne (ok, size) — ok=False si > MAX_PDF_SIZE."""
    try:
        head = session.head(url, timeout=TIMEOUT, allow_redirects=True)
        content_length = head.headers.get("Content-Length")
        if content_length:
            size = int(content_length)
            return size <= MAX_PDF_SIZE, size
        # Pas de Content-Length → on accepte
        return True, 0
    except (requests.RequestException, ValueError):
        return True, 0  # En cas d'erreur HEAD, on tente quand même


def download_pdf_content(url, session):
    """Télécharge un PDF, en streaming si > STREAM_THRESHOLD.
    Retourne le contenu bytes ou None."""
    # Vérifier la taille d'abord
    ok, size = check_pdf_size(url, session)
    if not ok:
        return None, f"PDF trop gros ({size / 1024 / 1024:.0f} MB > {MAX_PDF_SIZE / 1024 / 1024:.0f} MB)"

    resp = fetch_with_retry(url, session)
    if resp.status_code >= 400:
        return None, f"HTTP {resp.status_code}"

    content_type = resp.headers.get("Content-Type", "").lower()
    if "pdf" not in content_type and not url.lower().endswith(".pdf"):
        return None, "not_pdf"

    # Pour les gros fichiers, re-télécharger en streaming
    actual_size = len(resp.content)
    if actual_size > MAX_PDF_SIZE:
        return None, f"PDF trop gros ({actual_size / 1024 / 1024:.0f} MB)"

    return resp, None


# === Crawl ===

def fetch_page(url, session):
    """Fetch une URL avec retry et retourne (response, content_type) ou (None, error_str)."""
    try:
        domain_rate_limit(url)
        resp = fetch_with_retry(url, session)
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


# Lock pour protéger les écritures concurrentes sur le registre
_registry_lock = threading.Lock()


def crawl_seed(seed, registry, session, max_depth=1, stats=None, run_changes=None):
    """Crawl une URL seed et ses liens programme (depth 1)."""
    url = seed["url"]
    candidate_id = seed.get("candidate_id")
    city_id = seed.get("city_id")

    # Skip si déjà vérifié récemment
    with _registry_lock:
        if was_recently_checked(registry, url):
            stats["skipped"] += 1
            return

    resp, content_type = fetch_page(url, session)

    if resp is None:
        with _registry_lock:
            add_source_check(registry, url, 0, "", "fail", notes=content_type)
            stats["errors"] += 1
        return

    final_url = resp.url
    status = resp.status_code

    if status >= 400:
        with _registry_lock:
            add_source_check(registry, url, status, final_url, "fail")
            stats["errors"] += 1
        return

    # Cas PDF direct
    if "pdf" in content_type or url.lower().endswith(".pdf"):
        file_hash = hashlib.md5(resp.content).hexdigest() if len(resp.content) < 50_000_000 else None
        with _registry_lock:
            add_source_check(registry, url, status, final_url, "ok")
            stats["checked"] += 1
            add_document(registry, final_url, file_hash=file_hash, run_changes=run_changes)
            add_candidate_source(registry, final_url, source_type="pdf_direct",
                                  candidate_id=candidate_id, city_id=city_id,
                                  confidence="high")
            stats["pdfs"] += 1
        return

    # Cas HTML
    if "html" not in content_type:
        with _registry_lock:
            add_source_check(registry, url, status, final_url, "ok")
            stats["checked"] += 1
        return

    html = resp.text

    # Détection JS-rendered
    js_required = detect_js_rendered(html)

    # Analyse du contenu
    content_score = analyze_page_content(html)

    with _registry_lock:
        result = "js_required" if js_required else "ok"
        notes = f"content_score={content_score}"
        if js_required:
            notes += " (JS required)"
            run_changes["js_only_sites"].add(urlparse(url).hostname or url)
        add_source_check(registry, url, status, final_url, result, notes=notes)
        stats["checked"] += 1
        stats["html"] += 1

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

    # Enregistrer les liens programme trouvés avec scoring intelligent
    with _registry_lock:
        for plink in program_links:
            purl = plink["url"]
            if purl.lower().endswith(".pdf"):
                add_document(registry, purl, doc_type="program_candidate", run_changes=run_changes)
                # PDF lié depuis une page programme → high
                confidence = "high"
                add_candidate_source(registry, purl, source_type="pdf_linked",
                                      candidate_id=candidate_id, city_id=city_id,
                                      confidence=confidence)
                stats["pdfs"] += 1
            else:
                # Scoring basé sur le contenu de la page source
                confidence = content_score_to_confidence(content_score)
                add_candidate_source(registry, purl, source_type="program_page_candidate",
                                      candidate_id=candidate_id, city_id=city_id,
                                      confidence=confidence)
                stats["program_links"] += 1

    # Depth 1 : crawler les liens programme trouvés
    if max_depth >= 1:
        for plink in program_links[:10]:  # Limiter à 10 liens par seed
            purl = plink["url"]
            with _registry_lock:
                if was_recently_checked(registry, purl):
                    continue
            if purl.lower().endswith(".pdf"):
                # Télécharger le PDF pour obtenir le hash
                resp2, error = download_pdf_content(purl, session)
                with _registry_lock:
                    if resp2 and not error:
                        file_hash = hashlib.md5(resp2.content).hexdigest() if len(resp2.content) < 50_000_000 else None
                        add_document(registry, resp2.url, file_hash=file_hash, run_changes=run_changes)
                        add_source_check(registry, purl, resp2.status_code, resp2.url, "ok")
                    elif error:
                        add_source_check(registry, purl, 0, "", "fail", notes=error)
                    stats["checked"] += 1
            else:
                # Crawler la sous-page programme
                resp2, ct2 = fetch_page(purl, session)
                with _registry_lock:
                    if resp2 and resp2.status_code < 400 and "html" in (ct2 or ""):
                        sub_html = resp2.text
                        sub_score = analyze_page_content(sub_html)
                        sub_js = detect_js_rendered(sub_html)

                        result = "js_required" if sub_js else "ok"
                        notes = f"content_score={sub_score}"
                        if sub_js:
                            notes += " (JS required)"
                            run_changes["js_only_sites"].add(urlparse(purl).hostname or purl)
                        add_source_check(registry, purl, resp2.status_code, resp2.url, result, notes=notes)

                        # Chercher des PDF dans cette sous-page
                        sub_links = extract_links(sub_html, resp2.url)
                        for sl in sub_links:
                            if sl["url"].lower().endswith(".pdf"):
                                add_document(registry, sl["url"], doc_type="program_candidate", run_changes=run_changes)
                                # PDF trouvé en depth 1 → medium
                                add_candidate_source(registry, sl["url"], source_type="pdf_linked_depth1",
                                                      candidate_id=candidate_id, city_id=city_id,
                                                      confidence="medium")
                                stats["pdfs"] += 1

                        # Enregistrer la page elle-même si score élevé
                        if sub_score > 20:
                            sub_confidence = content_score_to_confidence(sub_score)
                            add_candidate_source(registry, purl, source_type="program_page_confirmed",
                                                  candidate_id=candidate_id, city_id=city_id,
                                                  confidence=sub_confidence)
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


def update_last_full_review(registry, checked_seeds):
    """Met à jour last_full_review_at pour les villes dont tous les candidats ont été vérifiés."""
    # Grouper les seeds vérifiés par ville
    checked_by_city = {}
    for seed in checked_seeds:
        cid = seed.get("city_id")
        if cid:
            checked_by_city.setdefault(cid, set()).add(seed.get("candidate_id"))

    now = datetime.now().isoformat()
    for city in registry["coverage_city"]:
        city_id = city["city_id"]
        if city_id not in checked_by_city:
            continue
        # Charger les candidats de cette ville
        filepath = os.path.join(ELECTIONS_DIR, f"{city_id}-2026.json")
        if not os.path.exists(filepath):
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue
        all_candidates = {c.get("id") for c in data.get("candidats", []) if c.get("programmeUrl", "#") != "#"}
        if all_candidates and all_candidates.issubset(checked_by_city[city_id]):
            city["last_full_review_at"] = now


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
    parser.add_argument("--workers", type=int, default=5,
                        help="Nombre de threads parallèles (défaut: 5)")
    parser.add_argument("--purge-days", type=int, default=30,
                        help="Supprimer les checks plus vieux que N jours (défaut: 30)")
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

    # Purge des vieux checks
    purge_old_checks(registry, keep_days=args.purge_days)

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

    # Stats (thread-safe via lock)
    stats = {
        "checked": 0, "html": 0, "pdfs": 0,
        "program_links": 0, "errors": 0, "skipped": 0
    }

    # Suivi des changements pour ce run
    run_changes = {
        "new_sources": [],
        "updated_docs": [],
        "js_only_sites": set(),
    }

    # Compteur de progression (thread-safe)
    progress_lock = threading.Lock()
    progress = {"done": 0}

    def process_seed(seed):
        """Wrapper pour le traitement d'une seed dans un thread."""
        try:
            crawl_seed(seed, registry, session, max_depth=args.max_depth,
                       stats=stats, run_changes=run_changes)
        except Exception as e:
            with _registry_lock:
                stats["errors"] += 1
            print(f"\n  ERREUR sur {seed['url']}: {e}")
        with progress_lock:
            progress["done"] += 1
            done = progress["done"]
        pct = round(done / len(seeds) * 100)
        host = urlparse(seed["url"]).hostname or "?"
        cid = seed.get("candidate_id") or "?"
        print(f"  [{done}/{len(seeds)}] {pct}% — {host} ({cid})          ", end="\r")

    # Crawl parallèle
    start_time = time.monotonic()
    print(f"\nCrawl en cours (depth={args.max_depth}, workers={args.workers}, rate={RATE_LIMIT}s/domaine)...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_seed, seed): seed for seed in seeds}
        concurrent.futures.wait(futures)

    elapsed = time.monotonic() - start_time

    # Mettre à jour la couverture villes
    update_city_coverage(registry)

    # Mettre à jour last_full_review_at
    update_last_full_review(registry, seeds)

    # Sauvegarder
    save_registry(registry)

    # === Résumé ===
    print("\n\n" + "=" * 60)
    print("  RÉSUMÉ")
    print("=" * 60)
    print(f"  Seeds traitées     : {len(seeds)}")
    print(f"  Pages vérifiées    : {stats['checked']}")
    print(f"  Pages HTML         : {stats['html']}")
    print(f"  PDFs détectés      : {stats['pdfs']}")
    print(f"  Liens programme    : {stats['program_links']}")
    print(f"  Erreurs            : {stats['errors']}")
    print(f"  Skippées (récent)  : {stats['skipped']}")
    print(f"  Durée              : {elapsed:.1f}s ({args.workers} workers)")
    print(f"\n  Total sources      : {len(registry['candidate_sources'])}")
    print(f"  Total documents    : {len(registry['documents'])}")
    print(f"  Total villes       : {len(registry['coverage_city'])}")

    # === Rapport de changements ===
    print("\n" + "-" * 60)
    print("  CHANGEMENTS CE RUN")
    print("-" * 60)

    new_sources = run_changes["new_sources"]
    updated_docs = run_changes["updated_docs"]
    js_sites = run_changes["js_only_sites"]

    if new_sources:
        print(f"\n  Nouvelles sources découvertes ({len(new_sources)}) :")
        for src in new_sources[:20]:
            print(f"    + {src}")
        if len(new_sources) > 20:
            print(f"    ... et {len(new_sources) - 20} autres")
    else:
        print("\n  Aucune nouvelle source découverte")

    if updated_docs:
        print(f"\n  Documents mis à jour — hash changé ({len(updated_docs)}) :")
        for doc in updated_docs:
            print(f"    ~ {doc}")
    else:
        print("  Aucun document mis à jour")

    if js_sites:
        print(f"\n  Sites JS-only détectés ({len(js_sites)}) — à crawler manuellement :")
        for site in sorted(js_sites):
            print(f"    ! {site}")

    # Top villes par priorité (programmes manquants)
    top = sorted(registry["coverage_city"], key=lambda c: c["priority_score"], reverse=True)[:10]
    if top and top[0]["priority_score"] > 0:
        print(f"\n  Top villes avec programmes manquants :")
        for c in top:
            if c["priority_score"] == 0:
                break
            reviewed = " (reviewed)" if c.get("last_full_review_at") else ""
            print(f"    {c['city_name']:25s}  {c['candidates_count']} candidats, "
                  f"{c['with_program_complete_count']} complets, "
                  f"priorité={c['priority_score']}{reviewed}")

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
