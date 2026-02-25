#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le CSV mairies_500_villes.csv avec les 500 plus grandes villes de France.

Sources :
  - geo.api.gouv.fr : liste des communes + population + code INSEE
  - api-lannuaire.service-public.fr : email officiel des mairies

Usage :
  python scripts/generer_csv_500_villes.py
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_CSV = os.path.join(ROOT, "data", "mairies_500_villes.csv")
EXISTING_CSV = os.path.join(ROOT, "data", "mairies_150_villes.csv")


def fetch_json(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "PourQuiTuVotes/1.0 (contact@pourquituvotes.fr)")
            resp = urllib.request.urlopen(req, timeout=30)
            return json.loads(resp.read())
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return None


def load_existing_csv():
    existing = {}
    if not os.path.exists(EXISTING_CSV):
        return existing
    with open(EXISTING_CSV, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = row["city_name"].strip().lower()
            existing[key] = {
                "email": row.get("email", "").strip(),
                "website": row.get("website", "").strip(),
                "email_verified": row.get("email_verified", "").strip(),
            }
    return existing


def get_top_communes(limit=550):
    print("  Récupération des communes via geo.api.gouv.fr...")
    url = "https://geo.api.gouv.fr/communes?fields=nom,population,codesPostaux,codeDepartement,code"
    data = fetch_json(url)
    if not data:
        print("  [ERREUR] Impossible de récupérer les communes")
        sys.exit(1)

    communes = [c for c in data if c.get("population")]
    communes.sort(key=lambda c: -c["population"])
    print(f"  {len(communes)} communes récupérées, top {limit} sélectionnées")
    return communes[:limit]


def get_mairie_email_by_code(code_insee):
    """Récupère l'email d'une mairie par code INSEE."""
    params = urllib.parse.urlencode({
        "where": f'pivot like "mairie" AND code_insee_commune="{code_insee}"',
        "select": "nom,adresse_courriel,site_internet",
        "limit": 5,
    })
    url = f"https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets/api-lannuaire-administration/records?{params}"
    data = fetch_json(url)

    if not data or not data.get("results"):
        return None, None

    # Prendre le premier résultat avec un email
    for r in data["results"]:
        email = r.get("adresse_courriel", "") or ""
        site_raw = r.get("site_internet", "")
        website = ""
        if site_raw:
            try:
                sites = json.loads(site_raw) if isinstance(site_raw, str) else site_raw
                if isinstance(sites, list) and sites:
                    website = sites[0].get("valeur", "")
            except (json.JSONDecodeError, TypeError):
                pass
        if email:
            return email, website

    # Pas d'email trouvé mais peut-être un site
    for r in data["results"]:
        site_raw = r.get("site_internet", "")
        website = ""
        if site_raw:
            try:
                sites = json.loads(site_raw) if isinstance(site_raw, str) else site_raw
                if isinstance(sites, list) and sites:
                    website = sites[0].get("valeur", "")
            except (json.JSONDecodeError, TypeError):
                pass
        if website:
            return None, website

    return None, None


def main():
    print("=" * 60)
    print("  GÉNÉRATION CSV 500 VILLES")
    print("=" * 60)

    existing = load_existing_csv()
    print(f"  {len(existing)} villes dans le CSV existant")

    communes = get_top_communes(550)

    results = []
    reused = 0
    from_api = 0
    no_email = 0

    print(f"\n  Récupération des emails pour chaque ville...")

    for i, commune in enumerate(communes[:500]):
        nom = commune["nom"]
        population = commune["population"]
        code = commune["code"]
        key = nom.strip().lower()

        # Priorité 1 : CSV existant (emails vérifiés manuellement)
        if key in existing and existing[key]["email"] and "formulaire" not in existing[key]["email"].lower():
            email = existing[key]["email"]
            website = existing[key]["website"]
            verified = existing[key]["email_verified"]
            reused += 1
            status = "CSV"
        else:
            # Priorité 2 : API lannuaire par code INSEE
            email, website = get_mairie_email_by_code(code)
            if email:
                verified = "api-lannuaire"
                from_api += 1
                status = "API"
            else:
                email = ""
                website = website or ""
                verified = ""
                no_email += 1
                status = "MISS"

            # Rate limiting
            time.sleep(0.15)

        results.append({
            "city_name": nom,
            "population": population,
            "email": email or "",
            "website": website or "",
            "email_verified": verified,
        })

        if (i + 1) % 25 == 0:
            print(f"  [{i+1:3d}/500]  CSV:{reused}  API:{from_api}  MISS:{no_email}  — dernier: {nom}")
        elif status == "MISS" and population > 50000:
            print(f"  [{i+1:3d}] MISS  {nom:30s} pop={population:>10,}")

    # Écrire le CSV
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["city_name", "population", "email", "website", "email_verified"])
        writer.writeheader()
        writer.writerows(results)

    avec_email = sum(1 for r in results if r["email"])
    pop_min = results[-1]["population"] if results else 0

    print(f"\n{'=' * 60}")
    print(f"  CSV écrit : {OUTPUT_CSV}")
    print(f"  Total villes      : {len(results)}")
    print(f"  Avec email        : {avec_email}")
    print(f"  Sans email        : {len(results) - avec_email}")
    print(f"  Réutilisés (150)  : {reused}")
    print(f"  Nouveaux (API)    : {from_api}")
    print(f"  Population min    : {pop_min:,}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
