#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajoute les pages résultats communes au sitemap.xml.
À lancer APRÈS generate_sitemap.py (qui gère les 103 villes principales).

Usage :
  python scripts/generate_sitemap_communes.py
"""

import sys
import io
import json
import os
from datetime import date
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse
import xml.dom.minidom

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
RESULTATS_DIR = os.path.join(DATA_DIR, "resultats-communes")
SITEMAP_PATH = os.path.join(ROOT_DIR, "sitemap.xml")

SITE_URL = "https://pourquituvotes.fr"
TODAY = date.today().isoformat()
NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # Charger les slugs des villes principales (déjà dans le sitemap)
    villes_path = os.path.join(DATA_DIR, "villes.json")
    existing_slugs = set()
    if os.path.exists(villes_path):
        for v in load_json(villes_path):
            existing_slugs.add(v["id"])

    # Collecter toutes les communes avec résultats
    communes_urls = []
    for filename in sorted(os.listdir(RESULTATS_DIR)):
        if not filename.endswith(".json"):
            continue
        dept_data = load_json(os.path.join(RESULTATS_DIR, filename))
        for commune in dept_data.get("communes", []):
            slug = commune["slug"]
            if slug in existing_slugs:
                continue
            if commune.get("resultats", {}).get("candidats"):
                communes_urls.append(f"{SITE_URL}/municipales-2026/{slug}/resultats/")

    print(f"Communes à ajouter au sitemap : {len(communes_urls)}")

    # Charger le sitemap existant
    urlset = Element("urlset")
    urlset.set("xmlns", NAMESPACE)

    # Copier les URLs existantes du sitemap
    if os.path.exists(SITEMAP_PATH):
        with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        # Parser les URLs existantes
        import re
        existing_locs = re.findall(r'<loc>(.*?)</loc>', content)
        for loc in existing_locs:
            url_el = SubElement(urlset, "url")
            SubElement(url_el, "loc").text = loc
            SubElement(url_el, "lastmod").text = TODAY
            # Garder les priorités existantes
            if "/resultats/" in loc:
                SubElement(url_el, "changefreq").text = "daily"
                SubElement(url_el, "priority").text = "0.95"
            elif "/candidats/" in loc:
                SubElement(url_el, "changefreq").text = "weekly"
                SubElement(url_el, "priority").text = "0.5"
            elif "/municipales-2026/" in loc:
                SubElement(url_el, "changefreq").text = "daily"
                SubElement(url_el, "priority").text = "0.8"
            elif "/enjeux-" in loc:
                SubElement(url_el, "changefreq").text = "weekly"
                SubElement(url_el, "priority").text = "0.6"
            elif loc == SITE_URL + "/":
                SubElement(url_el, "changefreq").text = "weekly"
                SubElement(url_el, "priority").text = "1.0"
            else:
                SubElement(url_el, "changefreq").text = "monthly"
                SubElement(url_el, "priority").text = "0.4"

    # Ajouter les communes
    for url in communes_urls:
        url_el = SubElement(urlset, "url")
        SubElement(url_el, "loc").text = url
        SubElement(url_el, "lastmod").text = TODAY
        SubElement(url_el, "changefreq").text = "weekly"
        SubElement(url_el, "priority").text = "0.6"

    # Écrire
    tree = ElementTree(urlset)
    buf = io.StringIO()
    tree.write(buf, encoding="unicode", xml_declaration=False)
    xml_str = buf.getvalue()

    dom = xml.dom.minidom.parseString(xml_str)
    pretty = dom.toprettyxml(indent="  ", encoding=None)
    lines = [line for line in pretty.split("\n") if line.strip()]
    if lines and lines[0].startswith("<?xml"):
        lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'

    final_xml = "\n".join(lines) + "\n"

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(final_xml)

    total = len(existing_locs) + len(communes_urls) if 'existing_locs' in dir() else len(communes_urls)
    print(f"Sitemap écrit : {SITEMAP_PATH}")
    print(f"URLs totales : ~{total}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
