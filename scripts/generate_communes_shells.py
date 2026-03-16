#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère les shells HTML résultats pour toutes les communes de France.
Lit les données depuis data/resultats-communes/*.json.
Génère municipales-2026/{slug}/resultats/index.html pour chaque commune.

Usage :
  python scripts/generate_communes_shells.py
  python scripts/generate_communes_shells.py --dry-run
  python scripts/generate_communes_shells.py --dept 13
"""

import sys
import io
import json
import os
import re
from datetime import datetime
from html import escape
from urllib.parse import quote

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
RESULTATS_DIR = os.path.join(DATA_DIR, "resultats-communes")

BASE_URL = "https://pourquituvotes.fr"
TODAY = datetime.now().strftime("%Y-%m-%d")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    import unicodedata
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def make_commune_title(nom, elu_nom=None, max_len=60):
    if elu_nom:
        t = f"Résultats municipales 2026 {nom} — {elu_nom} élu(e)"
        if len(t) <= max_len:
            return t
    t = f"Résultats municipales 2026 {nom}"
    if len(t) <= max_len:
        return t
    return f"Résultats 2026 {nom}"[:max_len]


def make_commune_desc(nom, dept, taux, candidats, max_len=155):
    if candidats:
        top = candidats[0]
        desc = f"Résultats municipales 2026 à {nom} ({dept}) : {top['nom']} en tête avec {top['pourcentage']}%. Participation : {taux}%."
    else:
        desc = f"Résultats des élections municipales 2026 à {nom} ({dept}). Participation : {taux}%."
    return desc[:max_len]


def make_commune_jsonld(nom, dept, resultats, candidats):
    elu = None
    for c in candidats:
        if c.get("elu"):
            elu = c["nom"]
            break

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Event",
                "name": f"Élections municipales 2026 — {nom}",
                "startDate": "2026-03-15",
                "endDate": "2026-03-22",
                "eventStatus": "https://schema.org/EventCompleted",
                "location": {
                    "@type": "Place",
                    "name": nom,
                    "address": {"@type": "PostalAddress", "addressLocality": nom, "addressRegion": dept, "addressCountry": "FR"}
                },
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"Qui a gagné les municipales 2026 à {nom} ?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"{elu} a remporté les municipales 2026 à {nom}." if elu else f"Les résultats des municipales 2026 à {nom} sont disponibles."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"Quel est le taux de participation aux municipales 2026 à {nom} ?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Le taux de participation aux municipales 2026 à {nom} est de {resultats['tauxParticipation']}%."
                        }
                    }
                ]
            }
        ]
    }
    if elu:
        ld["@graph"][0]["performer"] = {"@type": "Person", "name": elu, "jobTitle": "Maire élu(e)"}

    return json.dumps(ld, ensure_ascii=False, indent=2)


def make_seo_content(nom, dept, resultats, candidats):
    taux = resultats["tauxParticipation"]
    inscrits = resultats["inscrits"]

    html = f"""  <section class="seo-content" aria-label="Résultats municipales 2026 à {escape(nom)}">
    <h2>Résultats des élections municipales 2026 à {escape(nom)}</h2>
    <p>Les élections municipales 2026 à {escape(nom)} (département {escape(dept)}) ont vu une participation de {taux}%
    ({inscrits} inscrits, {resultats['votants']} votants).</p>"""

    if candidats:
        top = candidats[0]
        elu_text = f"{escape(top['nom'])} ({escape(top.get('nuance', ''))}) arrive en tête avec {top['pourcentage']}% des voix ({top['voix']} voix)."
        if top.get("elu"):
            elu_text = f"{escape(top['nom'])} ({escape(top.get('nuance', ''))}) est élu(e) avec {top['pourcentage']}% des voix."
        html += f"\n    <p>{elu_text}</p>"

        html += f"""
    <h3>Classement complet — Municipales 2026 {escape(nom)}</h3>
    <ol>"""
        for c in candidats:
            elu_flag = " — élu(e)" if c.get("elu") else ""
            html += f"""
      <li><strong>{escape(c['nom'])}</strong> ({escape(c.get('liste', ''))}) — {c['pourcentage']}% ({c['voix']} voix){elu_flag}</li>"""
        html += """
    </ol>"""

    html += """
  </section>"""
    return html


def generate_shell(nom, slug, dept, resultats, candidats, template_head, template_body, dry_run=False):
    """Génère un shell HTML pour une commune."""
    taux = resultats["tauxParticipation"]

    elu_nom = None
    for c in candidats:
        if c.get("elu"):
            elu_nom = c["nom"]
            break

    title = make_commune_title(nom, elu_nom)
    desc = make_commune_desc(nom, dept, taux, candidats)
    url = f"{BASE_URL}/municipales-2026/{slug}/resultats/"
    og_img = f"{BASE_URL}/img/og/comparateur.jpg"
    jsonld = make_commune_jsonld(nom, dept, resultats, candidats)
    seo_content = make_seo_content(nom, dept, resultats, candidats)

    head_seo = f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{escape(url)}">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="#POURQUITUVOTES">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:url" content="{escape(url)}">
  <meta property="og:image" content="{escape(og_img)}">
  <meta property="og:locale" content="fr_FR">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(desc)}">

  <meta property="article:modified_time" content="{TODAY}T00:00:00+01:00">

  <script type="application/ld+json">
{jsonld}
  </script>"""

    # Injecter le SEO content avant le footer dans le body
    body = template_body
    footer_marker = '<footer class="footer"'
    if footer_marker in body:
        body = body.replace(footer_marker, f"{seo_content}\n\n  {footer_marker}")

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
{head_seo}
{template_head}
</head>
{body}
</html>
"""
    rel_path = f"municipales-2026/{slug}/resultats/index.html"
    out_path = os.path.join(ROOT_DIR, rel_path)

    if dry_run:
        return True

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--dept", type=str)
    args = parser.parse_args()

    # Charger le template résultats
    template_path = os.path.join(ROOT_DIR, "municipales", "2026", "resultats.html")
    if not os.path.exists(template_path):
        print("Template résultats introuvable")
        return 1

    with open(template_path, "r", encoding="utf-8-sig") as f:
        template_html = f.read()

    # Extraire les assets du head (CSS, fonts, GTM, consent)
    head_lines = []
    in_head = False
    in_jsonld = False
    for line in template_html.split("\n"):
        stripped = line.strip()
        if "<head" in stripped:
            in_head = True
            continue
        if "</head>" in stripped:
            break
        if not in_head:
            continue
        if '<script type="application/ld+json"' in stripped:
            in_jsonld = True
            continue
        if in_jsonld:
            if "</script>" in stripped:
                in_jsonld = False
            continue
        if any(x in stripped for x in [
            "<title", "<meta name=\"description", "<meta name=\"robots",
            "<meta property=\"og:", "<meta name=\"twitter:",
            "<link rel=\"canonical", "<meta charset=", "<meta name=\"viewport",
            "<link rel=\"icon", "<meta property=\"article:",
        ]):
            continue
        if stripped.startswith("<!--") and stripped.endswith("-->") and "<" not in stripped[4:-3]:
            continue
        if stripped:
            head_lines.append(line)
    template_head = "\n".join(head_lines)

    # Extraire le body
    start = template_html.find("<body")
    end = template_html.find("</body>") + len("</body>")
    template_body = template_html[start:end] if start != -1 else ""

    # Charger les résultats communes existantes (nos 133 villes)
    existing_slugs = set()
    villes_path = os.path.join(DATA_DIR, "villes.json")
    if os.path.exists(villes_path):
        villes = load_json(villes_path)
        for v in villes:
            existing_slugs.add(v["id"])

    # Parcourir les fichiers résultats par département
    count = 0
    skipped_existing = 0

    result_files = sorted(f for f in os.listdir(RESULTATS_DIR) if f.startswith("resultats-") and f.endswith(".json"))
    if not result_files:
        print("Aucun fichier résultats trouvé dans data/resultats-communes/")
        return 1

    for filename in result_files:
        dept_code = filename.replace("resultats-", "").replace("-t1.json", "").replace("-t2.json", "")
        if args.dept and dept_code != args.dept:
            continue

        filepath = os.path.join(RESULTATS_DIR, filename)
        dept_data = load_json(filepath)
        dept_communes = dept_data.get("communes", [])

        print(f"  [{dept_code}] {len(dept_communes)} communes...", end=" ", flush=True)
        dept_count = 0

        for commune in dept_communes:
            slug = commune["slug"]

            # Skip si c'est une ville déjà dans notre base (shell déjà généré par generate_static_shells.py)
            if slug in existing_slugs:
                skipped_existing += 1
                continue

            resultats = commune.get("resultats", {})
            candidats = resultats.get("candidats", [])

            if not candidats:
                continue

            generate_shell(
                commune["nom"], slug, dept_code, resultats, candidats,
                template_head, template_body, args.dry_run
            )
            dept_count += 1
            count += 1

        print(f"{dept_count} shells")

    print(f"\n=== Résumé ===")
    print(f"  Shells générés : {count}")
    print(f"  Villes existantes skippées : {skipped_existing}")
    if not args.dry_run:
        print(f"  Dossier : municipales-2026/*/resultats/")

    return 0


if __name__ == "__main__":
    sys.exit(main())
