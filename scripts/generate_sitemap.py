#!/usr/bin/env python3
"""
Génère le fichier sitemap.xml pour pourquituvotes.fr.

Lit les données depuis :
  - data/schema/schema_elections.json (catégories thématiques)
  - data/villes.json (index des villes et candidats)
  - data/elections/{ville_id}-2026.json (détails candidats, programmeComplet)

Usage :
  python scripts/generate_sitemap.py
"""

import json
import os
from datetime import date
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xml.dom.minidom

# Chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "schema", "schema_elections.json")
VILLES_PATH = os.path.join(BASE_DIR, "data", "villes.json")
ELECTIONS_DIR = os.path.join(BASE_DIR, "data", "elections")
OUTPUT_PATH = os.path.join(BASE_DIR, "sitemap.xml")

SITE_URL = "https://pourquituvotes.fr"
TODAY = date.today().isoformat()

NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def add_url(urlset, loc, lastmod, changefreq, priority):
    """Ajoute un élément <url> au urlset."""
    url_el = SubElement(urlset, "url")
    SubElement(url_el, "loc").text = loc
    SubElement(url_el, "lastmod").text = lastmod
    SubElement(url_el, "changefreq").text = changefreq
    SubElement(url_el, "priority").text = str(priority)


def build_programme_complet_map(ville_id):
    """
    Charge le fichier election d'une ville et retourne un dict
    {candidat_id: bool(programmeComplet)}.
    """
    election_file = os.path.join(ELECTIONS_DIR, f"{ville_id}-2026.json")
    if not os.path.exists(election_file):
        return {}
    data = load_json(election_file)
    result = {}
    for candidat in data.get("candidats", []):
        result[candidat["id"]] = bool(candidat.get("programmeComplet", False))
    return result


def generate_sitemap():
    count = 0

    # Racine XML
    urlset = Element("urlset")
    urlset.set("xmlns", NAMESPACE)

    # ──────────────────────────────────────────────
    # 1. Pages statiques principales
    # ──────────────────────────────────────────────
    static_pages = [
        ("/", "weekly", 1.0),
        ("/municipales/2026/", "daily", 0.9),
        ("/methodologie.html", "monthly", 0.4),
        ("/faq.html", "monthly", 0.4),
        ("/a-propos.html", "monthly", 0.4),
        ("/mentions-legales.html", "yearly", 0.2),
        ("/confidentialite.html", "yearly", 0.2),
        ("/enjeux-index.html", "weekly", 0.6),
    ]

    for path, changefreq, priority in static_pages:
        add_url(urlset, f"{SITE_URL}{path}", TODAY, changefreq, priority)
        count += 1

    # ──────────────────────────────────────────────
    # 2. Pages enjeux thématiques (12 catégories)
    # ──────────────────────────────────────────────
    schema = load_json(SCHEMA_PATH)
    for category in schema["categories"]:
        cat_id = category["id"]
        add_url(urlset, f"{SITE_URL}/enjeux-2026/{cat_id}/", TODAY, "weekly", 0.6)
        count += 1

    # ──────────────────────────────────────────────
    # 3. Pages ville
    # ──────────────────────────────────────────────
    villes = load_json(VILLES_PATH)
    for ville in villes:
        ville_id = ville["id"]
        add_url(urlset, f"{SITE_URL}/municipales-2026/{ville_id}/", TODAY, "daily", 0.8)
        count += 1

        # ──────────────────────────────────────────
        # 4. Pages candidat pour cette ville
        # ──────────────────────────────────────────
        programme_map = build_programme_complet_map(ville_id)
        for candidat in ville.get("candidats", []):
            candidat_id = candidat["id"]
            is_complet = programme_map.get(candidat_id, False)
            priority = 0.7 if is_complet else 0.5
            add_url(
                urlset,
                f"{SITE_URL}/municipales-2026/{ville_id}/candidats/{candidat_id}/",
                TODAY,
                "weekly",
                priority,
            )
            count += 1

    # ──────────────────────────────────────────────
    # 5. Pages résultats ville
    # ──────────────────────────────────────────────
    for ville in villes:
        ville_id = ville["id"]
        # Vérifier si des résultats existent
        election_file = os.path.join(ELECTIONS_DIR, f"{ville_id}-2026.json")
        if os.path.exists(election_file):
            el_data = load_json(election_file)
            if el_data.get("resultats", {}).get("tour1"):
                add_url(
                    urlset,
                    f"{SITE_URL}/municipales-2026/{ville_id}/resultats/",
                    TODAY,
                    "daily",
                    0.95,
                )
                count += 1

    # ──────────────────────────────────────────────
    # 6. Page résultats nationale
    # ──────────────────────────────────────────────
    national_results = os.path.join(BASE_DIR, "municipales-2026", "resultats", "index.html")
    if os.path.exists(national_results):
        add_url(urlset, f"{SITE_URL}/municipales-2026/resultats/", TODAY, "daily", 1.0)
        count += 1

    # ──────────────────────────────────────────────
    # Ecriture du fichier XML
    # ──────────────────────────────────────────────
    import io

    # Serialiser le XML brut (sans declaration)
    tree = ElementTree(urlset)
    buf = io.StringIO()
    tree.write(buf, encoding="unicode", xml_declaration=False)
    xml_str = buf.getvalue()

    # Reformater avec minidom pour une indentation propre
    dom = xml.dom.minidom.parseString(xml_str)
    pretty = dom.toprettyxml(indent="  ", encoding=None)

    # Supprimer les lignes vides superflues ajoutees par minidom
    lines = [line for line in pretty.split("\n") if line.strip()]

    # Remplacer la declaration XML de minidom par la bonne (avec encoding)
    if lines and lines[0].startswith("<?xml"):
        lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'

    final_xml = "\n".join(lines) + "\n"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(final_xml)

    print(f"Sitemap genere : {OUTPUT_PATH}")
    print(f"URLs totales : {count}")


if __name__ == "__main__":
    generate_sitemap()
