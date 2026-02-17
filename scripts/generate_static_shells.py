#!/usr/bin/env python3
"""
Génère des "HTML Shells" statiques pour le SEO.

Les robots (X/Twitter, LinkedIn, WhatsApp, Facebook) n'exécutent pas le JS.
Ils ont besoin de balises OG en dur dans le HTML. Ce script génère un fichier
index.html physique pour chaque URL du silo, avec les bonnes métadonnées,
puis le même body que la SPA pour que le JS prenne le relais.

Structure générée :
  municipales-2026/{ville}/index.html
  municipales-2026/{ville}/candidats/{candidat}/index.html
  enjeux-2026/index.html
  enjeux-2026/{theme}/index.html

Usage :
  python scripts/generate_static_shells.py
  python scripts/generate_static_shells.py --dry-run    # affiche sans écrire
"""

import json
import os
import sys
from datetime import datetime
from html import escape

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
VILLES_JSON = os.path.join(DATA_DIR, "villes.json")
SCHEMA_JSON = os.path.join(DATA_DIR, "schema", "schema_elections.json")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")

BASE_URL = "https://pourquituvotes.fr"
OG_BASE = BASE_URL + "/img/og/"
TODAY = datetime.now().strftime("%Y-%m-%d")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ─────────────────────────────────────────────────────────
# Templates HTML — lus depuis les vrais fichiers du projet
# ─────────────────────────────────────────────────────────

def read_template(name):
    """Lit un fichier HTML du projet et le découpe en head_top / head_bottom / body."""
    path = os.path.join(ROOT_DIR, name)
    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    return content


def extract_body(html):
    """Extrait tout depuis <body> jusqu'à </body> inclus."""
    start = html.find("<body")
    end = html.find("</body>") + len("</body>")
    if start == -1 or end < len("</body>"):
        return ""
    return html[start:end]


def extract_head_assets(html):
    """Extrait les lignes du <head> qui sont des assets (CSS, fonts, scripts inline, GTM).
    Skip les meta SEO (on les réécrit), les doublons charset/viewport, et les commentaires vides."""
    lines = []
    in_head = False
    in_jsonld = False
    for line in html.split("\n"):
        stripped = line.strip()
        if "<head" in stripped:
            in_head = True
            continue
        if "</head>" in stripped:
            break
        if not in_head:
            continue

        # Skip JSON-LD block
        if '<script type="application/ld+json"' in stripped:
            in_jsonld = True
            continue
        if in_jsonld:
            if "</script>" in stripped:
                in_jsonld = False
            continue

        # Skip les meta qu'on réécrit dans make_head()
        if any(x in stripped for x in [
            "<title", "<meta name=\"description",
            "<meta name=\"keywords", "<meta name=\"author",
            "<meta name=\"robots", "<meta name=\"twitter:",
            "<meta property=\"og:", "<meta property=\"article:",
            "<link rel=\"canonical", "<link rel=\"alternate",
            "<meta charset=", "<meta name=\"viewport",
            "<link rel=\"icon",
        ]):
            continue

        # Skip les commentaires HTML purs (ex: <!-- SEO de base -->)
        if stripped.startswith("<!--") and stripped.endswith("-->") and "<" not in stripped[4:-3]:
            continue

        # Keep everything else (CSS, fonts, consent, GTM, inline styles)
        if stripped:
            lines.append(line)
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────
# Générateur de <head> SEO
# ─────────────────────────────────────────────────────────

def make_head(title, description, url, og_image, og_type="website", og_image_alt=None):
    """Génère un bloc <head> complet avec OG/Twitter en dur."""
    alt = og_image_alt or title
    return f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, interactive-widget=resizes-content">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{escape(url)}">

  <!-- Open Graph -->
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="#POURQUITUVOTES">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{escape(url)}">
  <meta property="og:image" content="{escape(og_image)}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{escape(alt)}">
  <meta property="og:locale" content="fr_FR">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(description)}">
  <meta name="twitter:image" content="{escape(og_image)}">
  <meta name="twitter:image:alt" content="{escape(alt)}">

  <meta property="article:modified_time" content="{TODAY}T00:00:00+01:00">
"""


# ─────────────────────────────────────────────────────────
# Écriture des shells
# ─────────────────────────────────────────────────────────

def write_shell(rel_path, head_seo, head_assets, body, dry_run=False):
    """Écrit un fichier HTML shell."""
    out_path = os.path.join(ROOT_DIR, rel_path)
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
{head_seo}
{head_assets}
</head>
{body}
</html>
"""
    if dry_run:
        print(f"  [dry-run] {rel_path}")
        return

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    dry_run = "--dry-run" in sys.argv

    villes = load_json(VILLES_JSON)
    schema = load_json(SCHEMA_JSON)
    categories = schema["categories"]

    # Lire les templates sources
    comparateur_html = read_template("municipales/2026/index.html")
    candidat_html = read_template("municipales/2026/candidat.html")
    thematique_html = read_template("thematique.html")
    enjeux_index_html = read_template("enjeux-index.html")

    comp_assets = extract_head_assets(comparateur_html)
    comp_body = extract_body(comparateur_html)
    cand_assets = extract_head_assets(candidat_html)
    cand_body = extract_body(candidat_html)
    theme_assets = extract_head_assets(thematique_html)
    theme_body = extract_body(thematique_html)
    enjeux_assets = extract_head_assets(enjeux_index_html)
    enjeux_body = extract_body(enjeux_index_html)

    count = 0

    # --- 1. Shells villes ---
    print("=== Shells villes ===")
    for ville in villes:
        vid = ville["id"]
        vnom = ville["nom"]
        n_cand = ville.get("stats", {}).get("candidats", len(ville.get("candidats", [])))

        title = f"Municipales 2026 {vnom} — Comparez les {n_cand} candidats | #POURQUITUVOTES"
        desc = f"Comparez les programmes des {n_cand} candidats aux municipales 2026 à {vnom}. Outil citoyen, neutre et factuel."
        url = f"{BASE_URL}/municipales-2026/{vid}/"
        og_img = f"{OG_BASE}{vid}.jpg"

        head = make_head(title, desc, url, og_img)
        rel = f"municipales-2026/{vid}/index.html"
        write_shell(rel, head, comp_assets, comp_body, dry_run)
        count += 1

        # --- 2. Shells candidats ---
        # Charger l'élection pour les détails candidat
        el_file = os.path.join(ELECTIONS_DIR, f"{vid}-2026.json")
        el_candidats = []
        if os.path.exists(el_file):
            el_data = load_json(el_file)
            el_candidats = el_data.get("candidats", [])

        # Index par ID pour accès rapide
        el_map = {c["id"]: c for c in el_candidats}

        for cand_info in ville.get("candidats", []):
            cid = cand_info["id"]
            cnom = cand_info["nom"]
            cliste = cand_info.get("liste", "")

            # Enrichir depuis l'élection JSON si dispo
            el_cand = el_map.get(cid, {})
            complet = el_cand.get("programmeComplet", False)
            badge = "Programme complet" if complet else "Propositions"

            c_title = f"{cnom} — Municipales 2026 {vnom} | #POURQUITUVOTES"
            c_desc = f"{badge} de {cnom} ({cliste}) aux municipales 2026 à {vnom}. Comparez avec les autres candidats."
            c_url = f"{BASE_URL}/municipales-2026/{vid}/candidats/{cid}/"
            c_og = f"{OG_BASE}{vid}-{cid}.jpg"

            c_head = make_head(c_title, c_desc, c_url, c_og, og_type="profile")
            c_rel = f"municipales-2026/{vid}/candidats/{cid}/index.html"
            write_shell(c_rel, c_head, cand_assets, cand_body, dry_run)
            count += 1

    # --- 3. Shell enjeux index ---
    print("=== Shells enjeux ===")
    e_title = "Enjeux Municipales 2026 — 12 thématiques clés | #POURQUITUVOTES"
    e_desc = "Découvrez les 12 enjeux majeurs des municipales 2026 : sécurité, transports, logement, éducation, environnement et plus."
    e_url = f"{BASE_URL}/enjeux-2026/"
    e_og = f"{OG_BASE}comparateur.jpg"
    e_head = make_head(e_title, e_desc, e_url, e_og)
    write_shell("enjeux-2026/index.html", e_head, enjeux_assets, enjeux_body, dry_run)
    count += 1

    # --- 4. Shells enjeux thématiques ---
    for cat in categories:
        cat_id = cat["id"]
        cat_nom = cat["nom"]

        t_title = f"{cat_nom} — Enjeux Municipales 2026 | #POURQUITUVOTES"
        t_desc = f"Comparez les propositions des candidats aux municipales 2026 sur le thème : {cat_nom}."
        t_url = f"{BASE_URL}/enjeux-2026/{cat_id}/"
        t_og = f"{OG_BASE}comparateur.jpg"

        t_head = make_head(t_title, t_desc, t_url, t_og, og_type="article")
        t_rel = f"enjeux-2026/{cat_id}/index.html"
        write_shell(t_rel, t_head, theme_assets, theme_body, dry_run)
        count += 1

    # --- 5. Mettre à jour _redirects ---
    update_redirects(dry_run)

    print(f"\n=== Termine ===")
    print(f"{count} shells generes")
    if not dry_run:
        print(f"Dossiers : municipales-2026/, enjeux-2026/")


def update_redirects(dry_run=False):
    """Met à jour _redirects : supprime les rewrites wildcard (les shells physiques prennent le relais)."""
    redirects_path = os.path.join(ROOT_DIR, "_redirects")
    new_content = """# Les shells HTML statiques dans municipales-2026/ et enjeux-2026/
# sont servis directement par Cloudflare Pages (fichiers physiques).
# Plus besoin de rewrites wildcard pour ces chemins.

# Pages statiques .html -> clean URL
/a-propos.html  /a-propos  301
/methodologie.html  /methodologie  301
/faq.html  /faq  301

# Legacy
/home /  301
/home.html /  301

# Ancien comparateur racine
/index.html?ville=:ville /municipales/2026/?ville=:ville 301
"""

    if dry_run:
        print("\n  [dry-run] _redirects serait mis a jour")
        return

    with open(redirects_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("\n  _redirects mis a jour (rewrites wildcard supprimes)")


if __name__ == "__main__":
    main()
