#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crawl des sites candidats + injection des propositions.

Etape 1 : --step crawl   — telecharge et nettoie le HTML des sites candidats
Etape 2 : (mapping fait par agents Haiku Claude Code, pas par ce script)
Etape 3 : --step inject  — injecte les JSON de crawl_results/ dans les elections

Usage:
  python scripts/crawl_et_extraire.py --step crawl
  python scripts/crawl_et_extraire.py --step crawl --max 10
  python scripts/crawl_et_extraire.py --step inject
  python scripts/crawl_et_extraire.py --step status
"""

import argparse
import json
import os
import re
import sys
import time
import glob
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Comment
import fitz  # PyMuPDF

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELECTIONS_DIR = os.path.join(BASE_DIR, "data", "elections")
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "schema", "schema_elections.json")
CRAWL_DIR = os.path.join(BASE_DIR, "scripts", "crawl_cache")
PDF_DIR = os.path.join(BASE_DIR, "scripts", "crawl_pdfs")
RESULTS_DIR = os.path.join(BASE_DIR, "scripts", "crawl_results")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.5",
}

PROGRAM_KEYWORDS = [
    "programme", "projet", "engagements", "propositions", "mesures",
    "priorites", "nos-actions", "nos-combats", "mon-projet", "vision",
    "ambition", "nos-engagements", "plan", "manifeste", "idees",
]

IGNORE_KEYWORDS = [
    "mentions-legales", "conditions-generales", "cookies", "confidentialite",
    "recrutement", "emploi", "don", "contact", "presse", "programme-tv",
    "cgu", "cgv", "login", "inscription", "panier", "cart",
]

JS_SIGNATURES = [
    "wix-thunderbolt", "thunderboltTag", "_wixCIDX",
    "__NEXT_DATA__", "window.__remixContext",
]


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    themes = []
    for cat in schema["categories"]:
        for st in cat["sousThemes"]:
            themes.append({
                "key": f"{cat['id']}/{st['id']}",
                "categorie": cat["nom"],
                "sous_theme": st["nom"],
            })
    return themes


def list_candidates(ville_filter=None, max_props=9):
    candidates = []
    for f in glob.glob(os.path.join(ELECTIONS_DIR, "*-2026.json")):
        data = json.load(open(f, encoding="utf-8"))
        ville_id = os.path.basename(f).replace("-2026.json", "")

        if ville_filter and ville_id != ville_filter:
            continue

        prop_count = {}
        for cat in data.get("categories", []):
            for sub in cat.get("sousThemes", []):
                for cid, prop in sub.get("propositions", {}).items():
                    if prop and isinstance(prop, dict) and prop.get("texte"):
                        prop_count[cid] = prop_count.get(cid, 0) + 1

        for c in data.get("candidats", []):
            url = c.get("programmeUrl", "")
            n = prop_count.get(c["id"], 0)
            if url and url != "#" and n <= max_props:
                candidates.append({
                    "ville_id": ville_id,
                    "candidat_id": c["id"],
                    "nom": c["nom"],
                    "url": url,
                    "props_existantes": n,
                })

    candidates.sort(key=lambda x: x["props_existantes"])
    return candidates


# =============================================================================
# CRAWL
# =============================================================================

def is_js_only(html):
    for sig in JS_SIGNATURES:
        if sig in html:
            return True
    try:
        soup = BeautifulSoup(html, "html.parser")
        body = soup.find("body")
        if body:
            text = body.get_text(strip=True)
            if len(text) < 200 and soup.find_all("script"):
                return True
    except Exception:
        return True  # Si on ne peut pas parser, considerer comme JS-only
    return False


def clean_html(html, url):
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return ""

    for tag in soup.find_all(["script", "style", "noscript", "iframe", "svg"]):
        tag.decompose()
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()
    for tag in soup.find_all(["nav", "footer", "header"]):
        tag.decompose()
    for tag in soup.find_all(attrs={"role": ["navigation", "banner", "contentinfo"]}):
        tag.decompose()
    for tag in soup.find_all(class_=re.compile(
        r"(nav|menu|footer|sidebar|cookie|banner|popup|modal|widget)", re.I
    )):
        tag.decompose()
    for tag in soup.find_all(id=re.compile(
        r"(nav|menu|footer|sidebar|cookie|banner|popup|modal)", re.I
    )):
        tag.decompose()

    lines = []
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "td", "blockquote"]):
        text = tag.get_text(separator=" ", strip=True)
        if len(text) > 15:
            prefix = ""
            if tag.name in ("h1", "h2", "h3", "h4"):
                prefix = f"[{tag.name.upper()}] "
            elif tag.name == "li":
                prefix = "- "
            lines.append(prefix + text)

    return "\n".join(lines)


def find_program_links(html, base_url):
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return []
    links = set()
    base_domain = urlparse(base_url).netloc

    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        if parsed.netloc != base_domain:
            continue

        path_lower = parsed.path.lower()

        if any(kw in path_lower for kw in IGNORE_KEYWORDS):
            continue

        link_text = a.get_text(strip=True).lower()
        if any(kw in path_lower or kw in link_text for kw in PROGRAM_KEYWORDS):
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if clean_url.rstrip("/") != base_url.rstrip("/"):
                links.add(clean_url)

    return list(links)[:10]


def find_pdf_links(html, base_url):
    """Trouve les liens vers des fichiers PDF sur la page."""
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return []

    pdfs = set()
    base_domain = urlparse(base_url).netloc

    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        # Accepter les PDF du meme domaine ou de domaines de stockage courants
        path_lower = parsed.path.lower()
        if not path_lower.endswith(".pdf"):
            continue

        # Ignorer les PDFs non pertinents
        fname_lower = os.path.basename(path_lower)
        if any(kw in fname_lower for kw in ["cgu", "rgpd", "mention", "cookie", "facture"]):
            continue

        pdfs.add(full_url)

    return list(pdfs)[:5]  # Max 5 PDFs par candidat


def download_pdf(url, session, candidat_id, ville_id, max_size_mb=50):
    """Telecharge un PDF et retourne le chemin local."""
    os.makedirs(PDF_DIR, exist_ok=True)

    try:
        # HEAD pour verifier la taille
        head = session.head(url, headers=HEADERS, timeout=10, allow_redirects=True)
        content_length = int(head.headers.get("Content-Length", 0))
        if content_length > max_size_mb * 1024 * 1024:
            return None

        # Telecharger
        resp = session.get(url, headers=HEADERS, timeout=30, allow_redirects=True, stream=True)
        resp.raise_for_status()

        # Verifier que c'est bien un PDF
        content_type = resp.headers.get("Content-Type", "")
        if "pdf" not in content_type and not url.lower().endswith(".pdf"):
            return None

        fname = f"{ville_id}_{candidat_id}_{os.path.basename(urlparse(url).path)}"
        # Nettoyer le nom de fichier
        fname = re.sub(r'[^\w\-.]', '_', fname)
        local_path = os.path.join(PDF_DIR, fname)

        with open(local_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        return local_path
    except Exception:
        return None


def extract_pdf_text(pdf_path, max_pages=80):
    """Extrait le texte d'un PDF via PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        pages_text = []
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            text = page.get_text("text")
            if text and len(text.strip()) > 50:
                pages_text.append(text.strip())
        doc.close()

        full_text = "\n\n--- PAGE ---\n\n".join(pages_text)

        # Nettoyage basique : supprimer les lignes repetitives courtes (headers/footers)
        lines = full_text.split("\n")
        if len(lines) > 20:
            # Compter les occurrences de chaque ligne
            from collections import Counter
            line_counts = Counter(line.strip() for line in lines if line.strip())
            # Supprimer les lignes qui apparaissent plus de 3 fois (headers/footers)
            threshold = max(3, len(pages_text) // 3)
            cleaned = []
            for line in lines:
                if line_counts.get(line.strip(), 0) <= threshold:
                    cleaned.append(line)
            full_text = "\n".join(cleaned)

        return full_text
    except Exception:
        return ""


def fetch_page(url, session, timeout=15):
    try:
        resp = session.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        return resp.text
    except Exception:
        return None


def crawl_candidate(candidate, session):
    url = candidate["url"]
    cid = candidate["candidat_id"]
    ville = candidate["ville_id"]
    result = {
        "candidat_id": cid,
        "ville_id": ville,
        "nom": candidate["nom"],
        "url": url,
        "pages": [],
        "pdfs": [],
        "js_only": False,
        "error": None,
    }

    html = fetch_page(url, session)
    if not html:
        result["error"] = "Impossible de charger la page"
        return result

    if is_js_only(html):
        result["js_only"] = True
        result["error"] = "Site JS-only (Wix/SPA)"
        return result

    text = clean_html(html, url)
    if text:
        result["pages"].append({"url": url, "text": text})

    # Chercher les PDFs sur la page d'accueil
    all_pdf_links = find_pdf_links(html, url)

    sub_links = find_program_links(html, url)

    for path in ["/programme", "/projet", "/nos-engagements", "/propositions", "/engagements"]:
        test_url = urljoin(url.rstrip("/") + "/", path.lstrip("/"))
        if test_url not in sub_links:
            sub_links.append(test_url)

    seen_urls = {url.rstrip("/")}
    for sub_url in sub_links[:12]:
        norm = sub_url.rstrip("/")
        if norm in seen_urls:
            continue
        seen_urls.add(norm)

        time.sleep(0.5)
        sub_html = fetch_page(sub_url, session)
        if sub_html and not is_js_only(sub_html):
            sub_text = clean_html(sub_html, sub_url)
            if sub_text and len(sub_text) > 100:
                existing_texts = {p["text"][:500] for p in result["pages"]}
                if sub_text[:500] not in existing_texts:
                    result["pages"].append({"url": sub_url, "text": sub_text})

            # Chercher aussi des PDFs dans les sous-pages
            sub_pdfs = find_pdf_links(sub_html, sub_url)
            for pdf_url in sub_pdfs:
                if pdf_url not in all_pdf_links:
                    all_pdf_links.append(pdf_url)

    # Telecharger et extraire les PDFs trouves
    for pdf_url in all_pdf_links[:5]:
        time.sleep(0.5)
        local_path = download_pdf(pdf_url, session, cid, ville)
        if local_path:
            pdf_text = extract_pdf_text(local_path)
            if pdf_text and len(pdf_text) > 200:
                result["pdfs"].append({
                    "url": pdf_url,
                    "local_path": local_path,
                    "text": pdf_text,
                    "chars": len(pdf_text),
                })

    return result


def crawl_all(candidates):
    os.makedirs(CRAWL_DIR, exist_ok=True)
    results = []

    print(f"\n{'='*60}")
    print(f"CRAWL de {len(candidates)} sites candidats")
    print(f"{'='*60}\n")

    session = requests.Session()

    for i, cand in enumerate(candidates):
        cache_path = os.path.join(CRAWL_DIR, f"{cand['ville_id']}_{cand['candidat_id']}.json")

        # Skip si deja en cache avec des pages ou PDFs
        if os.path.exists(cache_path):
            cached = json.load(open(cache_path, encoding="utf-8"))
            if (cached.get("pages") or cached.get("pdfs")) and not cached.get("error"):
                n_pdfs = len(cached.get("pdfs", []))
                pdf_str = f" + {n_pdfs} PDF" if n_pdfs else ""
                print(f"  [{i+1}/{len(candidates)}] {cand['nom']} ({cand['ville_id']})... CACHE ({len(cached.get('pages',[]))} pages{pdf_str})")
                results.append(cached)
                continue

        print(f"  [{i+1}/{len(candidates)}] {cand['nom']} ({cand['ville_id']})...", end=" ", flush=True)

        result = crawl_candidate(cand, session)

        if result["error"]:
            print(f"ERREUR: {result['error']}")
        else:
            total_chars = sum(len(p["text"]) for p in result["pages"])
            pdf_info = ""
            if result.get("pdfs"):
                pdf_chars = sum(p["chars"] for p in result["pdfs"])
                pdf_info = f" + {len(result['pdfs'])} PDF ({pdf_chars} chars)"
            print(f"OK ({len(result['pages'])} pages, {total_chars} chars{pdf_info})")

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        results.append(result)
        time.sleep(1)

    ok = sum(1 for r in results if not r["error"])
    js_only = sum(1 for r in results if r["js_only"])
    errors = sum(1 for r in results if r["error"] and not r["js_only"])

    print(f"\nResume: {ok} OK, {js_only} JS-only, {errors} erreurs")
    return results


# =============================================================================
# INJECTION (lit les fichiers de crawl_results/)
# =============================================================================

def inject_all():
    print(f"\n{'='*60}")
    print(f"INJECTION des resultats dans les JSON d'election")
    print(f"{'='*60}\n")

    sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
    from inserer_propositions import insert

    result_files = glob.glob(os.path.join(RESULTS_DIR, "*.json"))
    if not result_files:
        print("  Aucun fichier dans crawl_results/. Lancez le mapping d'abord.")
        return

    total_ins = 0
    total_upd = 0
    count = 0

    for f in sorted(result_files):
        fname = os.path.basename(f).replace(".json", "")
        parts = fname.split("_", 1)
        if len(parts) != 2:
            continue

        ville, cid = parts
        props = json.load(open(f, encoding="utf-8"))

        if not props:
            continue

        # Retrouver nom et URL
        election_path = os.path.join(ELECTIONS_DIR, f"{ville}-2026.json")
        nom, url = cid, "#"
        if os.path.exists(election_path):
            edata = json.load(open(election_path, encoding="utf-8"))
            for c in edata.get("candidats", []):
                if c["id"] == cid:
                    nom = c["nom"]
                    url = c.get("programmeUrl", "#")
                    break

        ins, upd, total = insert(ville, cid, props, url)
        print(f"  {nom} ({ville}): +{ins} nouvelles, ~{upd} maj, {total} total")
        total_ins += ins
        total_upd += upd
        count += 1

    print(f"\nResume: {count} candidats, +{total_ins} nouvelles, ~{total_upd} mises a jour")


# =============================================================================
# STATUS
# =============================================================================

def show_status():
    print(f"\n{'='*60}")
    print(f"STATUS")
    print(f"{'='*60}\n")

    # Fichiers caches
    cache_files = glob.glob(os.path.join(CRAWL_DIR, "*.json"))
    crawled_ok = 0
    crawled_js = 0
    crawled_err = 0
    with_pdfs = 0
    for f in cache_files:
        data = json.load(open(f, encoding="utf-8"))
        if data.get("js_only"):
            crawled_js += 1
        elif data.get("error"):
            crawled_err += 1
        elif data.get("pages") or data.get("pdfs"):
            crawled_ok += 1
            if data.get("pdfs"):
                with_pdfs += 1

    # Fichiers resultats (post-mapping)
    result_files = glob.glob(os.path.join(RESULTS_DIR, "*.json"))
    mapped = 0
    total_props = 0
    a_verifier = 0
    for f in result_files:
        props = json.load(open(f, encoding="utf-8"))
        if props:
            mapped += 1
            total_props += len(props)
            a_verifier += sum(1 for p in props.values() if isinstance(p, dict) and p.get("a_verifier"))

    # A mapper (en cache OK mais pas encore dans results)
    cache_ids = set()
    for f in cache_files:
        data = json.load(open(f, encoding="utf-8"))
        if not data.get("error") and (data.get("pages") or data.get("pdfs")):
            cache_ids.add(os.path.basename(f).replace(".json", ""))
    result_ids = {os.path.basename(f).replace(".json", "") for f in result_files}
    to_map = cache_ids - result_ids

    print(f"  Crawl cache:    {len(cache_files)} fichiers ({crawled_ok} OK dont {with_pdfs} avec PDF, {crawled_js} JS-only, {crawled_err} erreurs)")
    print(f"  A mapper:       {len(to_map)} candidats")
    print(f"  Deja mappes:    {mapped} candidats ({total_props} propositions, {a_verifier} a verifier)")
    print(f"  Resultats prets pour injection: {len(result_files)} fichiers")

    if to_map:
        print(f"\n  Candidats a mapper:")
        for cid in sorted(to_map)[:20]:
            print(f"    - {cid}")
        if len(to_map) > 20:
            print(f"    ... +{len(to_map)-20} de plus")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Crawl + injection propositions candidats")
    parser.add_argument("--step", choices=["crawl", "inject", "status"], default="status",
                        help="Etape a executer (defaut: status)")
    parser.add_argument("--ville", help="Filtrer par ville")
    parser.add_argument("--max", type=int, help="Nombre max de candidats a crawler")
    parser.add_argument("--max-props", type=int, default=9,
                        help="Seuil max de props existantes (defaut: 9)")
    args = parser.parse_args()

    if args.step == "status":
        show_status()
        return

    if args.step == "crawl":
        candidates = list_candidates(args.ville, args.max_props)
        if args.max:
            candidates = candidates[:args.max]
        print(f"Candidats a traiter: {len(candidates)}")
        crawl_all(candidates)
        print("\nCrawl termine. Les textes sont dans scripts/crawl_cache/")
        print("Lancez les agents Haiku Claude Code pour le mapping.")

    elif args.step == "inject":
        inject_all()


if __name__ == "__main__":
    main()
