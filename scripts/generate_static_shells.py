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
from urllib.parse import quote

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
# Comptage des propositions par candidat
# ─────────────────────────────────────────────────────────

def count_propositions(el_data, candidate_id):
    """Compte le nombre total de mesures d'un candidat dans les données élection."""
    total = 0
    for cat in el_data.get("categories", []):
        for st in cat.get("sousThemes", []):
            val = st.get("propositions", {}).get(candidate_id)
            if val and val.get("mesures"):
                total += len(val["mesures"])
    return total


def make_candidate_title(nom, ville, max_len=60):
    """Génère un titre SEO candidat qui tient dans max_len caractères.
    Le mot-clé 'Programme Municipales 2026' est placé en début ou milieu,
    jamais tronqué en fin de title."""
    # Format idéal : "Programme Nom — Municipales 2026 Ville"
    full = f"Programme {nom} — Municipales 2026 {ville}"
    if len(full) <= max_len:
        return full
    # Raccourci : "Nom — Programme Municipales 2026 Ville"
    short = f"{nom} — Programme Municipales 2026 {ville}"
    if len(short) <= max_len:
        return short
    # Compact : "Nom — Municipales 2026 Ville"
    compact = f"{nom} — Municipales 2026 {ville}"
    if len(compact) <= max_len:
        return compact
    # Minimal : "Nom — Municipales 2026"
    minimal = f"{nom} — Municipales 2026"
    if len(minimal) <= max_len:
        return minimal
    # Dernier recours : tronquer le nom
    remaining = max_len - len(" — Municipales 2026")
    return f"{nom[:remaining-1]}… — Municipales 2026"


def make_candidate_desc(nom, ville, n_props, liste="", max_len=155):
    """Génère une meta description conditionnelle selon le nombre de propositions.
    Inclut la liste politique pour les requêtes partisanes."""
    liste_short = f" ({liste})" if liste else ""
    if n_props > 0:
        desc = f"Programme de {nom}{liste_short} aux municipales 2026 à {ville} : {n_props} propositions analysées. Comparez les candidats."
        if len(desc) > max_len:
            desc = f"Programme de {nom} aux municipales 2026 à {ville} : {n_props} propositions. Comparez les candidats."
        if len(desc) > max_len:
            desc = f"Programme {nom} — Municipales 2026 {ville} : {n_props} propositions analysées."
    else:
        desc = f"{nom}{liste_short}, candidat aux municipales 2026 à {ville}. Comparez les programmes et suivez la campagne."
        if len(desc) > max_len:
            desc = f"{nom}, candidat aux municipales 2026 à {ville}. Comparez les programmes dès publication."
    return desc[:max_len]


def make_jsonld_candidate(nom, ville, liste, url, n_props, complet):
    """Génère un bloc JSON-LD Person + Event pour un candidat."""
    ld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": nom,
        "description": f"Candidat aux élections municipales 2026 à {ville}" + (f" — {liste}" if liste else ""),
        "url": url,
        "jobTitle": f"Candidat aux municipales 2026 à {ville}",
        "knowsAbout": [
            {
                "@type": "Event",
                "name": f"Élections municipales 2026 — {ville}",
                "description": f"Premier et second tour des élections municipales 2026 à {ville}, France.",
                "startDate": "2026-03-15",
                "endDate": "2026-03-22",
                "eventStatus": "https://schema.org/EventScheduled",
                "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "location": {
                    "@type": "Place",
                    "name": ville,
                    "address": {"@type": "PostalAddress", "addressLocality": ville, "addressCountry": "FR"}
                }
            }
        ]
    }
    if n_props > 0:
        ld["description"] += f". {n_props} propositions analysées"
    return json.dumps(ld, ensure_ascii=False, indent=2)


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

def make_head(title, description, url, og_image, og_type="website", og_image_alt=None, jsonld=None):
    """Génère un bloc <head> complet avec OG/Twitter en dur + JSON-LD optionnel."""
    alt = og_image_alt or title
    jsonld_block = ""
    if jsonld:
        jsonld_block = f"""
  <!-- Structured Data -->
  <script type="application/ld+json">
{jsonld}
  </script>
"""
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
{jsonld_block}"""


# ─────────────────────────────────────────────────────────
# Écriture des shells
# ─────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────
# Contenu SEO statique (crawlable par Google, unique par page)
# ─────────────────────────────────────────────────────────

def count_props_by_category(el_data, candidate_id):
    """Compte les mesures par catégorie pour un candidat. Retourne dict {cat_id: count}."""
    result = {}
    for cat in el_data.get("categories", []):
        n = 0
        for st in cat.get("sousThemes", []):
            val = st.get("propositions", {}).get(candidate_id)
            if val and val.get("mesures"):
                n += len(val["mesures"])
        if n > 0:
            result[cat["id"]] = n
    return result


def count_all_props_by_category(el_data):
    """Compte le total de mesures par catégorie (tous candidats). Retourne dict {cat_nom: count}."""
    result = {}
    for cat in el_data.get("categories", []):
        n = 0
        for st in cat.get("sousThemes", []):
            for cid, val in st.get("propositions", {}).items():
                if val and val.get("mesures"):
                    n += len(val["mesures"])
        if n > 0:
            result[cat["nom"]] = n
    return result


def make_city_seo_content(ville_data, el_data, schema_cats):
    """Génère un bloc HTML SEO unique pour une page ville."""
    vnom = ville_data["nom"]
    cp = ville_data.get("codePostal", "")
    dep = ville_data.get("departement", "")
    stats = ville_data.get("stats", {})
    n_cand = stats.get("candidats", 0)
    n_props = stats.get("propositions", 0)
    n_complets = stats.get("complets", 0)

    candidats = el_data.get("candidats", []) if el_data else []

    # Lister les candidats avec infos
    vid = ville_data["id"]
    cand_lines = []
    for c in candidats:
        n_p = count_propositions(el_data, c["id"]) if el_data else 0
        status = f"{n_p} propositions" if n_p > 0 else "programme en attente"
        if c.get("programmeComplet"):
            status += " — programme complet"
        cand_lines.append(f'      <li><a href="/municipales-2026/{escape(vid)}/candidats/{escape(c["id"])}/"><strong>{escape(c["nom"])}</strong></a> ({escape(c.get("liste", ""))}) — {status}</li>')
    cand_list = "\n".join(cand_lines)

    # Thèmes les plus couverts
    cat_counts = count_all_props_by_category(el_data) if el_data else {}
    top_themes = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    themes_text = ", ".join(f"{nom} ({n})" for nom, n in top_themes) if top_themes else "données en cours d'intégration"

    html = f"""  <section class="seo-content" aria-label="Informations sur les élections municipales 2026 à {escape(vnom)}">
    <h2>Élections municipales 2026 à {escape(vnom)}</h2>
    <p>Les élections municipales 2026 à {escape(vnom)} ({escape(cp)}) se tiendront les 15 et 22 mars 2026.
    {n_cand} candidat{"s" if n_cand > 1 else ""} {"sont" if n_cand > 1 else "est"} en lice pour cette élection.
    {f"Parmi eux, {n_complets} {'ont' if n_complets > 1 else 'a'} publié un programme complet, totalisant {n_props} propositions analysées sur notre plateforme." if n_props > 0 else "Les propositions et programmes seront analysés et comparés dès leur publication."}</p>
    <h3>Les candidats aux municipales 2026 à {escape(vnom)}</h3>
    <ul>
{cand_list}
    </ul>"""

    if top_themes:
        html += f"""
    <h3>Thèmes les plus abordés à {escape(vnom)}</h3>
    <p>Les thématiques les plus couvertes dans les programmes des candidats à {escape(vnom)} sont : {themes_text}.</p>"""

    html += """
  </section>"""
    return html


def make_candidate_seo_content(cand_data, ville_name, ville_id, el_data):
    """Génère un bloc HTML SEO unique pour une page candidat.
    Inclut des liens internes vers les autres candidats de la même ville."""
    cnom = cand_data.get("nom", "")
    cid = cand_data.get("id", "")
    cliste = cand_data.get("liste", "")
    complet = cand_data.get("programmeComplet", False)
    prog_url = cand_data.get("programmeUrl", "")

    n_props = count_propositions(el_data, cid) if el_data else 0
    cat_counts = count_props_by_category(el_data, cid) if el_data else {}

    # Mapper cat_id -> cat_nom depuis el_data
    cat_names = {cat["id"]: cat["nom"] for cat in el_data.get("categories", [])} if el_data else {}
    top_themes = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)

    html = f"""  <section class="seo-content" aria-label="Profil de {escape(cnom)}, candidat aux municipales 2026 à {escape(ville_name)}">
    <h2>{escape(cnom)} — Candidat aux municipales 2026 à {escape(ville_name)}</h2>
    <p>{escape(cnom)} se présente aux élections municipales 2026 à {escape(ville_name)} sous l'étiquette {escape(cliste)}."""

    if n_props > 0:
        n_themes = len(cat_counts)
        html += f""" Son programme comprend {n_props} propositions réparties sur {n_themes} thématique{"s" if n_themes > 1 else ""}."""
        if complet:
            html += " Le programme complet a été intégré et analysé sur notre plateforme."
    else:
        html += " Son programme n'a pas encore été intégré sur notre plateforme."

    if prog_url and prog_url != "#":
        html += f""" Site de campagne : <a href="{escape(prog_url)}" rel="nofollow noopener" target="_blank">{escape(prog_url)}</a>."""

    html += "</p>"

    if top_themes:
        html += f"""
    <h3>Répartition des propositions de {escape(cnom)} par thème</h3>
    <ul>"""
        for cat_id, count in top_themes:
            cat_nom = cat_names.get(cat_id, cat_id)
            html += f"""
      <li>{escape(cat_nom)} : {count} proposition{"s" if count > 1 else ""}</li>"""
        html += """
    </ul>"""

    # Liens internes vers les autres candidats de la même ville
    other_cands = [c for c in el_data.get("candidats", []) if c["id"] != cid]
    if other_cands:
        html += f"""
    <h3>Autres candidats aux municipales 2026 à {escape(ville_name)}</h3>
    <ul>"""
        for oc in other_cands:
            oc_n_props = count_propositions(el_data, oc["id"])
            oc_status = f"{oc_n_props} propositions" if oc_n_props > 0 else "programme en attente"
            html += f"""
      <li><a href="/municipales-2026/{escape(ville_id)}/candidats/{escape(oc['id'])}/">{escape(oc['nom'])}</a> ({escape(oc.get('liste', ''))}) — {oc_status}</li>"""
        html += """
    </ul>"""

    html += """
  </section>"""
    return html


def write_shell(rel_path, head_seo, head_assets, body, dry_run=False, seo_content="", hide_etat_vide=False):
    """Écrit un fichier HTML shell avec contenu SEO optionnel injecté avant </body>."""
    out_path = os.path.join(ROOT_DIR, rel_path)
    if hide_etat_vide:
        # Pages ville : masquer l'état vide par défaut (la ville est déjà chargée)
        body = body.replace('id="etat-vide" class="etat-vide"', 'id="etat-vide" class="etat-vide" hidden')
    if seo_content:
        # Injecter avant le footer (pas après)
        footer_marker = '<footer class="footer"'
        if footer_marker in body:
            body = body.replace(footer_marker, f"{seo_content}\n\n  {footer_marker}")
        else:
            body = body.replace("</body>", f"\n{seo_content}\n</body>")
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

        # Contenu SEO unique par ville
        el_file = os.path.join(ELECTIONS_DIR, f"{vid}-2026.json")
        el_data_city = load_json(el_file) if os.path.exists(el_file) else None
        city_seo = make_city_seo_content(ville, el_data_city, categories)

        write_shell(rel, head, comp_assets, comp_body, dry_run, seo_content=city_seo, hide_etat_vide=True)
        count += 1

        # --- 2. Shells candidats ---
        # Charger l'élection pour les détails candidat
        el_file = os.path.join(ELECTIONS_DIR, f"{vid}-2026.json")
        el_data = None
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

            # Compter les propositions
            n_props = count_propositions(el_data, cid) if el_data else 0

            # Titre SEO optimisé (max 60 chars)
            c_title = make_candidate_title(cnom, vnom)
            # Description conditionnelle (max 155 chars)
            c_desc = make_candidate_desc(cnom, vnom, n_props, liste=cliste)
            c_url = f"{BASE_URL}/municipales-2026/{vid}/candidats/{cid}/"
            c_og = f"{OG_BASE}{vid}-{cid}.jpg"

            # JSON-LD structured data
            jsonld = make_jsonld_candidate(cnom, vnom, cliste, c_url, n_props, complet)

            c_head = make_head(c_title, c_desc, c_url, c_og, og_type="profile", jsonld=jsonld)
            c_rel = f"municipales-2026/{vid}/candidats/{cid}/index.html"

            # Contenu SEO unique par candidat
            cand_seo = make_candidate_seo_content(el_cand, vnom, vid, el_data) if el_data else ""

            write_shell(c_rel, c_head, cand_assets, cand_body, dry_run, seo_content=cand_seo)
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
/mentions-legales.html  /mentions-legales  301
/confidentialite.html  /confidentialite  301
/enjeux-index.html  /enjeux-2026/  301

# Trailing slash canonicalization (evite duplication Google)
/municipales-2026/:ville/candidats/:candidat /municipales-2026/:ville/candidats/:candidat/ 301
/municipales-2026/:ville /municipales-2026/:ville/ 301
/enjeux-2026/:theme /enjeux-2026/:theme/ 301

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
