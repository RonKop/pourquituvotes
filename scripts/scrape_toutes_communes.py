#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrape les résultats T1 pour TOUTES les communes de France depuis le Ministère.
Sauvegarde dans data/resultats-communes/ (un JSON par département).

Usage :
  python scripts/scrape_toutes_communes.py --tour 1
  python scripts/scrape_toutes_communes.py --tour 1 --dept 75
  python scripts/scrape_toutes_communes.py --tour 1 --resume  (reprend là où ça s'est arrêté)
"""

import sys
import io
import json
import os
import re
import argparse
import time
import unicodedata
from datetime import datetime

try:
    import urllib.request
    import urllib.error
except ImportError:
    pass

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
COMMUNES_JSON = os.path.join(DATA_DIR, "communes_france.json")
OUTPUT_DIR = os.path.join(DATA_DIR, "resultats-communes")

BASE_URL = "https://www.resultats-elections.interieur.gouv.fr/municipales2026/ensemble_geographique"
DATES = {"1": "2026-03-15", "2": "2026-03-22"}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_html(url):
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'PQTV-Bot/1.0 (pourquituvotes.fr)')
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.read().decode('utf-8', errors='replace')
    except Exception:
        return None


def parse_number(text):
    text = text.replace('\xa0', '').replace(' ', '').replace('\u202f', '')
    text = text.replace(',', '.').replace('%', '').strip()
    try:
        if '.' in text:
            return float(text)
        return int(text)
    except ValueError:
        return 0


def clean(text):
    return re.sub(r'<[^>]+>', '', text).strip()


def normalize_nom(text):
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.lower().strip()


def slugify(text):
    text = normalize_nom(text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def parse_resultats_html(html, tour_num):
    """Parse le HTML — version allégée sans matching candidats (on garde les noms bruts)."""
    if not html:
        return None

    # Parse mentions (participation)
    mentions = {}
    mentions_match = re.search(r'<caption>\s*Mentions.*?</caption>(.*?)</table>', html, re.DOTALL)
    if mentions_match:
        rows = re.findall(r'<tr>(.*?)</tr>', mentions_match.group(1), re.DOTALL)
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 2:
                label = clean(cells[0]).lower()
                val = parse_number(clean(cells[1]))
                if 'inscrit' in label: mentions['inscrits'] = val
                elif 'abstention' in label: mentions['abstentions'] = val
                elif 'votant' in label: mentions['votants'] = val
                elif 'blanc' in label: mentions['blancs'] = val
                elif 'nul' in label: mentions['nuls'] = val
                elif 'exprim' in label: mentions['exprimes'] = val

    inscrits = mentions.get('inscrits', 0)
    votants = mentions.get('votants', 0)
    blancs = mentions.get('blancs', 0)
    nuls = mentions.get('nuls', 0)
    exprimes = mentions.get('exprimes', 0)

    if not inscrits:
        return None
    if not exprimes:
        exprimes = votants - blancs - nuls

    abstentions = inscrits - votants
    taux = round(votants / inscrits * 100, 2) if inscrits > 0 else 0

    # Parse candidats
    # Deux formats possibles :
    # Grandes villes (>= 6 cols) : Liste | Conduit par | Nuance | Voix | %Ins | %Exp [| Sièges...]
    # Petites communes (5 cols)  : Conduit par | Voix | %Ins | %Exp | Sièges
    candidats = []
    resultats_match = re.search(r'<caption>\s*R.sultats.*?</caption>(.*?)</table>', html, re.DOTALL)
    if resultats_match:
        # Détecter le format via les headers
        # Grandes villes (7+ cols) : Liste | Conduit par | Nuance | Voix | %Ins | %Exp | Sièges...
        # Petites communes (6 cols) : Liste | Conduit par | Voix | %Ins | %Exp | Sièges
        headers = re.findall(r'<th[^>]*>(.*?)</th>', resultats_match.group(1), re.DOTALL)
        header_texts = [clean(h).lower() for h in headers]
        has_nuance = any('nuance' in h for h in header_texts)

        rows = re.findall(r'<tr>(.*?)</tr>', resultats_match.group(1), re.DOTALL)
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)

            if has_nuance and len(cells) >= 6:
                # Format avec nuance : Liste | Conduit par | Nuance | Voix | %Ins | %Exp [| Sièges...]
                liste = clean(cells[0])
                conduit_par = re.sub(r'^(?:M\.|Mme|M)\s+', '', clean(cells[1])).strip()
                nuance = clean(cells[2])
                voix = parse_number(clean(cells[3]))
                pct_exprimes = parse_number(clean(cells[5]))
                sieges_idx = 6

            elif not has_nuance and len(cells) >= 5:
                # Format sans nuance : Liste | Conduit par | Voix | %Ins | %Exp [| Sièges]
                liste = clean(cells[0])
                conduit_par = re.sub(r'^(?:M\.|Mme|M)\s+', '', clean(cells[1])).strip()
                nuance = ""
                voix = parse_number(clean(cells[2]))
                pct_exprimes = parse_number(clean(cells[4]))
                sieges_idx = 5

            else:
                continue

            if voix <= 0:
                continue

            cand = {
                "nom": conduit_par,
                "liste": liste,
                "nuance": nuance,
                "voix": int(voix) if voix == int(voix) else voix,
                "pourcentage": round(pct_exprimes, 2),
                "elu": False,
            }

            # Sièges
            if len(cells) > sieges_idx:
                sieges = parse_number(clean(cells[sieges_idx]))
                if sieges > 0:
                    cand["elu"] = True

            candidats.append(cand)

    if not candidats:
        return None

    candidats.sort(key=lambda x: x["voix"], reverse=True)

    # Qualifié T2
    if tour_num == 1:
        for i, c in enumerate(candidats):
            seuil = inscrits * 0.1
            c["qualifieT2"] = (c["voix"] >= seuil) or (i < 2)
            if c["pourcentage"] > 50:
                c["elu"] = True

    return {
        "date": DATES[str(tour_num)],
        "inscrits": inscrits,
        "abstentions": abstentions,
        "tauxParticipation": taux,
        "votants": votants,
        "blancs": blancs,
        "nuls": nuls,
        "exprimes": exprimes,
        "candidats": candidats,
    }


def main():
    parser = argparse.ArgumentParser(description="Scrape résultats toutes communes")
    parser.add_argument("--tour", type=int, choices=[1, 2], required=True)
    parser.add_argument("--dept", type=str, help="Un seul département")
    parser.add_argument("--resume", action="store_true", help="Reprendre (skip départements déjà faits)")
    parser.add_argument("--delay", type=float, default=0.3)
    args = parser.parse_args()

    communes = load_json(COMMUNES_JSON)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"=== Scrape toutes communes — Tour {args.tour} ===")
    print(f"Communes : {len(communes)}")
    print(f"Delay : {args.delay}s\n")

    # Grouper par département
    by_dept = {}
    for c in communes:
        dept = c.get("departement", {}).get("code", c.get("codeDepartement", ""))
        if dept not in by_dept:
            by_dept[dept] = []
        by_dept[dept].append(c)

    total_imported = 0
    total_errors = 0
    total_404 = 0

    for dept in sorted(by_dept.keys()):
        if args.dept and dept != args.dept:
            continue

        output_file = os.path.join(OUTPUT_DIR, f"resultats-{dept}-t{args.tour}.json")

        # Resume : skip si fichier existe déjà
        if args.resume and os.path.exists(output_file):
            existing = load_json(output_file)
            n = len(existing.get("communes", []))
            print(f"  [{dept}] déjà fait ({n} communes), skip")
            total_imported += n
            continue

        dept_communes = by_dept[dept]
        region = dept_communes[0].get("region", {}).get("code", "")
        if not region:
            print(f"  [{dept}] pas de code région, skip")
            continue

        print(f"  [{dept}] {len(dept_communes)} communes...", end=" ", flush=True)

        dept_results = {
            "departement": dept,
            "tour": args.tour,
            "scrape_date": datetime.now().isoformat(),
            "communes": [],
        }

        imported = 0
        errors = 0

        for commune in dept_communes:
            code = commune["code"]
            nom = commune["nom"]
            url = f"{BASE_URL}/{region}/{dept}/{code}/index.html"

            html = fetch_html(url)
            if not html:
                total_404 += 1
                time.sleep(args.delay * 0.5)
                continue

            tour_data = parse_resultats_html(html, args.tour)
            if not tour_data:
                errors += 1
                time.sleep(args.delay * 0.5)
                continue

            dept_results["communes"].append({
                "code": code,
                "nom": nom,
                "slug": slugify(nom),
                "population": commune.get("population", 0),
                "resultats": tour_data,
            })
            imported += 1
            time.sleep(args.delay)

        save_json(output_file, dept_results)
        print(f"{imported} OK, {errors} erreurs")
        total_imported += imported
        total_errors += errors

    print(f"\n=== Résumé ===")
    print(f"  Communes importées : {total_imported}")
    print(f"  Erreurs parsing : {total_errors}")
    print(f"  404 : {total_404}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
