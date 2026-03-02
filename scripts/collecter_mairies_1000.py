#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collecte les emails des mairies françaises via APIs publiques.
Étend le CSV existant (500 villes) pour atteindre 1000 villes.

Sources :
  - geo.api.gouv.fr : liste des communes avec population
  - etablissements-publics.api.gouv.fr : emails des mairies

Usage :
  python scripts/collecter_mairies_1000.py              # Collecte et génère le CSV
  python scripts/collecter_mairies_1000.py --dry-run     # Affiche sans écrire
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXISTING_CSV = os.path.join(ROOT, "data", "mairies_500_villes.csv")
OUTPUT_CSV = os.path.join(ROOT, "data", "mairies_1000_villes.csv")

GEO_API = "https://geo.api.gouv.fr"
ANNUAIRE_API = "https://etablissements-publics.api.gouv.fr/v3"


def fetch_json(url, retries=3):
    """Fetch JSON from URL with retries."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "PourQuiTuVotes/1.0 (contact@pourquituvotes.fr)")
            resp = urllib.request.urlopen(req, timeout=15)
            return json.loads(resp.read())
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                return None


def load_existing_cities():
    """Charge les villes déjà dans le CSV existant."""
    cities = {}
    if not os.path.exists(EXISTING_CSV):
        return cities
    with open(EXISTING_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["city_name"].strip()
            cities[name.lower()] = row
    return cities


def get_all_communes(min_pop=8000):
    """Récupère toutes les communes françaises au-dessus d'un seuil de population."""
    # L'API geo ne supporte pas de tri par population directement sur /communes
    # On récupère par département pour contourner la limite
    print("  Récupération des communes depuis geo.api.gouv.fr...")

    # D'abord, récupérer la liste des départements
    deps = fetch_json(f"{GEO_API}/departements")
    if not deps:
        print("  ERREUR: impossible de récupérer les départements")
        return []

    all_communes = []
    for i, dep in enumerate(deps):
        code = dep["code"]
        url = f"{GEO_API}/departements/{code}/communes?fields=nom,population,code,codesPostaux,codeDepartement&limit=500"
        communes = fetch_json(url)
        if communes:
            for c in communes:
                pop = c.get("population", 0)
                if pop and pop >= min_pop:
                    all_communes.append(c)
        if (i + 1) % 20 == 0:
            print(f"    {i+1}/{len(deps)} départements traités ({len(all_communes)} communes trouvées)")
        time.sleep(0.1)  # Rate limiting

    # Trier par population décroissante
    all_communes.sort(key=lambda c: -c.get("population", 0))
    print(f"  Total : {len(all_communes)} communes >= {min_pop:,} habitants")
    return all_communes


def get_mairie_email(code_insee):
    """Récupère l'email de la mairie via l'API annuaire (GeoJSON)."""
    url = f"{ANNUAIRE_API}/communes/{code_insee}/mairie"
    data = fetch_json(url)
    if not data:
        return None, None
    # Format GeoJSON FeatureCollection
    features = data.get("features", [])
    if not features:
        # Fallback ancien format (liste directe)
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("email") or data[0].get("adresseCourriel"), data[0].get("url")
        return None, None
    props = features[0].get("properties", {})
    email = props.get("email")
    website = props.get("url")
    return email, website


def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("  COLLECTE MAIRIES — Extension à 1000 villes")
    if dry_run:
        print("  MODE DRY-RUN")
    print("=" * 60)

    # Charger l'existant
    existing = load_existing_cities()
    print(f"\n  Villes existantes dans le CSV : {len(existing)}")

    # Charger toutes les entrées existantes (on les garde telles quelles)
    existing_rows = []
    with open(EXISTING_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_rows = list(reader)

    # Récupérer les communes
    communes = get_all_communes(min_pop=8000)

    # Filtrer celles déjà dans le CSV
    new_communes = []
    for c in communes:
        name = c["nom"]
        if name.lower() not in existing:
            new_communes.append(c)

    print(f"  Nouvelles communes à traiter : {len(new_communes)}")

    # Limiter pour atteindre ~1000 total
    target = 1000 - len(existing)
    if len(new_communes) > target:
        new_communes = new_communes[:target]
        print(f"  Limité à {target} nouvelles (objectif 1000 total)")

    # Récupérer les emails
    print(f"\n  Récupération des emails de mairies...")
    new_rows = []
    found = 0
    no_email = 0

    for i, c in enumerate(new_communes):
        name = c["nom"]
        code = c["code"]
        pop = c.get("population", 0)

        email, website = get_mairie_email(code)
        time.sleep(0.15)  # Rate limiting API annuaire

        status = "OK" if email else "PAS D'EMAIL"
        if email:
            found += 1
        else:
            no_email += 1

        if (i + 1) % 50 == 0 or email:
            print(f"  [{i+1:4d}/{len(new_communes)}] {name:30s} {pop:>8,} hab  {status}  {email or ''}")

        new_rows.append({
            "city_name": name,
            "population": str(pop),
            "email": email or "",
            "website": website or "",
            "email_verified": "api-lannuaire" if email else "",
        })

    print(f"\n  Résultat : {found} avec email, {no_email} sans email")
    print(f"  Total final : {len(existing) + len(new_rows)} villes")

    if dry_run:
        print("\n  [DRY-RUN] Aucun fichier écrit.")
        return

    # Écrire le nouveau CSV (existant + nouvelles)
    fieldnames = ["city_name", "population", "email", "website", "email_verified"]
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # D'abord les existantes
        for row in existing_rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})
        # Puis les nouvelles (triées par population décroissante)
        new_rows.sort(key=lambda r: -int(r["population"] or "0"))
        for row in new_rows:
            writer.writerow(row)

    print(f"\n  CSV écrit : {OUTPUT_CSV}")
    print(f"  {len(existing_rows)} existantes + {len(new_rows)} nouvelles = {len(existing_rows) + len(new_rows)} total")


if __name__ == "__main__":
    main()
