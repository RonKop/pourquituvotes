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


def make_jsonld_candidate(nom, ville, liste, url, n_props, complet, has_resultats=False, cand_result=None):
    """Génère un bloc JSON-LD Person + Event pour un candidat."""
    event_status = "https://schema.org/EventCompleted" if has_resultats else "https://schema.org/EventScheduled"

    desc = f"Candidat aux élections municipales 2026 à {ville}" + (f" — {liste}" if liste else "")
    if n_props > 0:
        desc += f". {n_props} propositions analysées"
    if cand_result:
        pct = cand_result.get("pourcentage", 0)
        if cand_result.get("elu"):
            desc += f". Élu(e) avec {pct}% des voix"
        else:
            desc += f". Résultat : {pct}% des voix"

    ld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": nom,
        "description": desc,
        "url": url,
        "jobTitle": f"Maire élu(e) de {ville}" if (cand_result and cand_result.get("elu")) else f"Candidat aux municipales 2026 à {ville}",
        "knowsAbout": [
            {
                "@type": "Event",
                "name": f"Élections municipales 2026 — {ville}",
                "description": f"Premier et second tour des élections municipales 2026 à {ville}, France.",
                "startDate": "2026-03-15",
                "endDate": "2026-03-22",
                "eventStatus": event_status,
                "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "location": {
                    "@type": "Place",
                    "name": ville,
                    "address": {"@type": "PostalAddress", "addressLocality": ville, "addressCountry": "FR"}
                }
            }
        ]
    }
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

    # Résultats si disponibles
    if el_data and el_data.get("resultats", {}).get("tour1"):
        resultats = el_data["resultats"]
        elu_id = resultats.get("eluMaire")
        if elu_id:
            el_cands = {c["id"]: c for c in el_data.get("candidats", [])}
            elu_cand = el_cands.get(elu_id, {})
            elu_nom = elu_cand.get("nom", elu_id)
            tour_data = resultats.get("tour2") or resultats.get("tour1", {})
            elu_pct = 0
            for rc in tour_data.get("candidats", []):
                if rc["id"] == elu_id:
                    elu_pct = rc["pourcentage"]
                    break
            html += f"""
    <h3>Résultats des municipales 2026 à {escape(vnom)}</h3>
    <p>{escape(elu_nom)} a remporté les élections municipales 2026 à {escape(vnom)} avec {elu_pct}% des voix.
    <a href="/municipales-2026/{escape(vid)}/resultats/">Voir tous les résultats</a>.</p>"""

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

    # Résultat du candidat si disponible
    if el_data and el_data.get("resultats", {}).get("tour1"):
        resultats = el_data["resultats"]
        tour_data = resultats.get("tour2") or resultats.get("tour1", {})
        for rc in tour_data.get("candidats", []):
            if rc["id"] == cid:
                elu_text = "a été élu(e) maire" if rc.get("elu") else "a obtenu"
                html += f"""
    <h3>Résultat de {escape(cnom)} aux municipales 2026</h3>
    <p>{escape(cnom)} {elu_text} avec {rc['pourcentage']}% des voix ({rc['voix']} voix) aux municipales 2026 à {escape(ville_name)}.
    <a href="/municipales-2026/{escape(ville_id)}/resultats/">Voir tous les résultats</a>.</p>"""
                break

    html += """
  </section>"""
    return html


# ─────────────────────────────────────────────────────────
# Résultats électoraux — SEO shells
# ─────────────────────────────────────────────────────────

def make_results_title(ville, elu_nom=None, has_tour2=False, max_len=60):
    """Génère un titre SEO pour la page résultats d'une ville."""
    if has_tour2 and elu_nom:
        full = f"Résultats municipales 2026 {ville} — {elu_nom} élu(e) | #POURQUITUVOTES"
        if len(full) <= max_len:
            return full
        short = f"Résultats municipales 2026 {ville} — {elu_nom} élu(e)"
        if len(short) <= max_len:
            return short
        compact = f"Résultats {ville} — {elu_nom} élu(e)"
        if len(compact) <= max_len:
            return compact
    else:
        full = f"Résultats 1er tour municipales 2026 {ville} | #POURQUITUVOTES"
        if len(full) <= max_len:
            return full
        short = f"Résultats 1er tour municipales 2026 {ville}"
        if len(short) <= max_len:
            return short

    minimal = f"Résultats municipales 2026 {ville}"
    return minimal[:max_len]


def make_results_desc(ville, elu_nom=None, pct=None, taux_participation=None, max_len=155):
    """Génère une meta description pour la page résultats."""
    if elu_nom and pct:
        desc = f"Résultats des municipales 2026 à {ville} : {elu_nom} élu(e) avec {pct}% des voix."
        if taux_participation:
            desc += f" Participation : {taux_participation}%."
        desc += " Tous les scores."
    else:
        desc = f"Résultats du 1er tour des municipales 2026 à {ville}."
        if taux_participation:
            desc += f" Participation : {taux_participation}%."
        desc += " Classement et scores de tous les candidats."
    return desc[:max_len]


def make_jsonld_results(ville, resultats, candidats_map):
    """Génère un bloc JSON-LD Event + FAQPage pour une page résultats."""
    elu_id = resultats.get("eluMaire")
    elu_nom = None
    if elu_id and elu_id in candidats_map:
        elu_nom = candidats_map[elu_id].get("nom", elu_id)

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Event",
                "name": f"Élections municipales 2026 — {ville}",
                "description": f"Résultats des élections municipales 2026 à {ville}, France.",
                "startDate": "2026-03-15",
                "endDate": "2026-03-22",
                "eventStatus": "https://schema.org/EventCompleted",
                "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "location": {
                    "@type": "Place",
                    "name": ville,
                    "address": {"@type": "PostalAddress", "addressLocality": ville, "addressCountry": "FR"}
                },
                "organizer": {
                    "@type": "GovernmentOrganization",
                    "name": "Ministère de l'Intérieur"
                },
            },
        ]
    }

    if elu_nom:
        ld["@graph"][0]["performer"] = {
            "@type": "Person",
            "name": elu_nom,
            "jobTitle": "Maire élu(e)"
        }

    # FAQPage pour featured snippets
    faq = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"Qui a gagné les municipales 2026 à {ville} ?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{elu_nom} a remporté les élections municipales 2026 à {ville}." if elu_nom else f"Les résultats des municipales 2026 à {ville} sont en cours de publication."
                }
            }
        ]
    }

    # Ajouter taux participation dans FAQ si T1 dispo
    t1 = resultats.get("tour1", {})
    if t1.get("tauxParticipation"):
        faq["mainEntity"].append({
            "@type": "Question",
            "name": f"Quel est le taux de participation aux municipales 2026 à {ville} ?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"Le taux de participation au 1er tour des municipales 2026 à {ville} est de {t1['tauxParticipation']}%."
            }
        })

    # FAQ "Qui est au second tour ?" si T1 mais pas T2
    if t1 and not resultats.get("tour2"):
        qualifies = []
        for rc in t1.get("candidats", []):
            if rc.get("qualifieT2") and rc["id"] in candidats_map:
                qualifies.append(candidats_map[rc["id"]].get("nom", rc["id"]))
        if qualifies:
            faq["mainEntity"].append({
                "@type": "Question",
                "name": f"Qui est au second tour des municipales 2026 à {ville} ?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Les candidats qualifiés pour le second tour des municipales 2026 à {ville} sont : {', '.join(qualifies)}."
                }
            })

    ld["@graph"].append(faq)
    return json.dumps(ld, ensure_ascii=False, indent=2)


def make_results_seo_content(ville_data, el_data, resultats):
    """Génère un bloc HTML SEO unique pour une page résultats ville."""
    vnom = ville_data["nom"]
    vid = ville_data["id"]
    candidats_map = {c["id"]: c for c in el_data.get("candidats", [])}

    elu_id = resultats.get("eluMaire")
    elu_nom = candidats_map.get(elu_id, {}).get("nom", elu_id) if elu_id else None

    # Tour le plus récent
    tour_data = resultats.get("tour2") or resultats.get("tour1", {})
    taux = tour_data.get("tauxParticipation", 0)
    tour_label = "second tour" if resultats.get("tour2") else "premier tour"

    html = f"""  <section class="seo-content" aria-label="Résultats des élections municipales 2026 à {escape(vnom)}">
    <h2>Résultats des élections municipales 2026 à {escape(vnom)}</h2>
    <p>"""

    if elu_nom:
        elu_cand = candidats_map.get(elu_id, {})
        elu_pct = 0
        for rc in tour_data.get("candidats", []):
            if rc["id"] == elu_id:
                elu_pct = rc["pourcentage"]
                break
        html += f"""{escape(elu_nom)} ({escape(elu_cand.get('liste', ''))}) a remporté les élections municipales 2026 à {escape(vnom)} au {tour_label} avec {elu_pct}% des voix exprimées. """
    else:
        html += f"""Les résultats du {tour_label} des élections municipales 2026 à {escape(vnom)} sont disponibles. """

    html += f"""Le taux de participation s'est établi à {taux}%.</p>"""

    # Liste ordonnée des candidats
    cands_sorted = sorted(tour_data.get("candidats", []), key=lambda x: x.get("voix", 0), reverse=True)
    if cands_sorted:
        html += f"""
    <h3>Classement des candidats aux municipales 2026 à {escape(vnom)}</h3>
    <ol>"""
        for rc in cands_sorted:
            cand = candidats_map.get(rc["id"], {})
            elu_text = " — élu(e)" if rc.get("elu") else ""
            html += f"""
      <li><a href="/municipales-2026/{escape(vid)}/candidats/{escape(rc['id'])}/">{escape(cand.get('nom', rc['id']))}</a> ({escape(cand.get('liste', ''))}) — {rc.get('pourcentage', 0)}% ({rc.get('voix', 0)} voix){elu_text}</li>"""
        html += """
    </ol>"""

    # Si les deux tours existent, ajouter un résumé du T1
    if resultats.get("tour2") and resultats.get("tour1"):
        t1 = resultats["tour1"]
        t1_taux = t1.get("tauxParticipation", 0)
        html += f"""
    <h3>Premier tour des municipales 2026 à {escape(vnom)}</h3>
    <p>Au premier tour (15 mars 2026), le taux de participation était de {t1_taux}%.</p>
    <ol>"""
        t1_sorted = sorted(t1.get("candidats", []), key=lambda x: x.get("voix", 0), reverse=True)
        for rc in t1_sorted:
            cand = candidats_map.get(rc["id"], {})
            q_text = " — qualifié(e) au second tour" if rc.get("qualifieT2") else ""
            html += f"""
      <li>{escape(cand.get('nom', rc['id']))} — {rc.get('pourcentage', 0)}% ({rc.get('voix', 0)} voix){q_text}</li>"""
        html += """
    </ol>"""

    # Lien vers comparateur
    html += f"""
    <h3>Comparer les programmes</h3>
    <p>Retrouvez l'analyse complète des programmes des candidats à {escape(vnom)} sur notre <a href="/municipales-2026/{escape(vid)}/">comparateur de programmes</a>.</p>"""

    # Fusions
    if resultats.get("tour2", {}).get("fusionsListes"):
        html += f"""
    <h3>Fusions de listes au second tour à {escape(vnom)}</h3>
    <ul>"""
        for f in resultats["tour2"]["fusionsListes"]:
            principal = candidats_map.get(f["listePrincipale"], {}).get("nom", f["listePrincipale"])
            fusionnees = ", ".join(candidats_map.get(lid, {}).get("nom", lid) for lid in f.get("listesFusionnees", []))
            html += f"""
      <li><strong>{escape(f.get('nomFusion', 'Fusion'))}</strong> : {escape(principal)} + {escape(fusionnees)}</li>"""
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

        # Adapter titre/desc si résultats T1 disponibles (mode second tour)
        el_file_check = os.path.join(ELECTIONS_DIR, f"{vid}-2026.json")
        el_data_check = load_json(el_file_check) if os.path.exists(el_file_check) else None
        res_check = el_data_check.get("resultats", {}) if el_data_check else {}
        has_t1 = bool(res_check.get("tour1"))
        has_t2 = bool(res_check.get("tour2"))

        if has_t1 and not has_t2:
            # Mode second tour : mettre en avant les qualifiés
            qualifies = [rc for rc in res_check["tour1"].get("candidats", []) if rc.get("qualifieT2")]
            n_q = len(qualifies)
            title = f"Municipales 2026 {vnom} — Comparez les {n_q} candidats du second tour | #POURQUITUVOTES"
            if len(title) > 60:
                title = f"Second tour municipales 2026 {vnom} — {n_q} candidats"
            noms_q = []
            for rc in qualifies[:3]:
                for c in (el_data_check or {}).get("candidats", []):
                    if c["id"] == rc["id"]:
                        noms_q.append(c["nom"].split()[-1])
                        break
            desc = f"Second tour le 22 mars. Comparez les programmes de {', '.join(noms_q)}{'...' if n_q > 3 else ''} à {vnom}."
        elif has_t2 and res_check.get("eluMaire"):
            elu_id = res_check["eluMaire"]
            elu_nom = elu_id
            for c in (el_data_check or {}).get("candidats", []):
                if c["id"] == elu_id:
                    elu_nom = c["nom"]
                    break
            title = f"Municipales 2026 {vnom} — {elu_nom} élu(e) | #POURQUITUVOTES"
            if len(title) > 60:
                title = f"Municipales 2026 {vnom} — {elu_nom} élu(e)"
            desc = f"{elu_nom} élu(e) à {vnom}. Comparez les programmes des {n_cand} candidats aux municipales 2026."
        else:
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

            # JSON-LD structured data (avec résultats si dispo)
            has_res = bool(el_data and el_data.get("resultats", {}).get("tour1"))
            cand_result = None
            if has_res:
                res_data = el_data["resultats"]
                tour_res = res_data.get("tour2") or res_data.get("tour1", {})
                for rc in tour_res.get("candidats", []):
                    if rc["id"] == cid:
                        cand_result = rc
                        break
            jsonld = make_jsonld_candidate(cnom, vnom, cliste, c_url, n_props, complet, has_res, cand_result)

            # Meta description enrichie avec résultat
            if cand_result:
                pct = cand_result.get("pourcentage", 0)
                if cand_result.get("elu"):
                    c_desc = f"{cnom}, élu(e) maire de {vnom} avec {pct}% — municipales 2026. {n_props} propositions analysées."
                else:
                    c_desc = f"{cnom} aux municipales 2026 à {vnom} : {pct}% des voix. {n_props} propositions analysées."
                c_desc = c_desc[:155]

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

    # --- 5. Shells résultats ---
    print("=== Shells résultats ===")

    # Lire le template résultats
    resultats_html_path = os.path.join(ROOT_DIR, "municipales", "2026", "resultats.html")
    if os.path.exists(resultats_html_path):
        resultats_html = read_template("municipales/2026/resultats.html")
        res_assets = extract_head_assets(resultats_html)
        res_body = extract_body(resultats_html)

        for ville in villes:
            vid = ville["id"]
            vnom = ville["nom"]

            # Charger résultats depuis l'élection JSON
            el_file = os.path.join(ELECTIONS_DIR, f"{vid}-2026.json")
            if not os.path.exists(el_file):
                continue
            el_data = load_json(el_file)
            resultats = el_data.get("resultats")
            if not resultats or not resultats.get("tour1"):
                continue  # Pas encore de résultats

            candidats_map = {c["id"]: c for c in el_data.get("candidats", [])}
            elu_id = resultats.get("eluMaire")
            elu_nom = candidats_map.get(elu_id, {}).get("nom") if elu_id else None
            has_tour2 = "tour2" in resultats

            # Tour le plus récent
            tour_data = resultats.get("tour2") or resultats.get("tour1", {})
            elu_pct = None
            if elu_id:
                for rc in tour_data.get("candidats", []):
                    if rc["id"] == elu_id:
                        elu_pct = rc["pourcentage"]
                        break
            taux = tour_data.get("tauxParticipation")

            # SEO
            r_title = make_results_title(vnom, elu_nom, has_tour2)
            r_desc = make_results_desc(vnom, elu_nom, elu_pct, taux)
            r_url = f"{BASE_URL}/municipales-2026/{vid}/resultats/"
            r_og = f"{OG_BASE}{vid}.jpg"  # Fallback sur l'image ville
            r_jsonld = make_jsonld_results(vnom, resultats, candidats_map)

            r_head = make_head(r_title, r_desc, r_url, r_og, jsonld=r_jsonld)
            r_rel = f"municipales-2026/{vid}/resultats/index.html"

            # Contenu SEO
            r_seo = make_results_seo_content(ville, el_data, resultats)

            write_shell(r_rel, r_head, res_assets, res_body, dry_run, seo_content=r_seo)
            count += 1

        print(f"  Shells résultats générés")
    else:
        print(f"  Template résultats introuvable ({resultats_html_path}), skip")

    # --- 6. Shell résultats national ---
    print("=== Shell résultats national ===")
    national_html_path = os.path.join(ROOT_DIR, "municipales", "2026", "resultats-national.html")
    if os.path.exists(national_html_path):
        national_html = read_template("municipales/2026/resultats-national.html")
        nat_assets = extract_head_assets(national_html)
        nat_body = extract_body(national_html)

        # Compter les villes avec résultats pour le SEO content
        villes_avec_res = []
        for v in villes:
            el_f = os.path.join(ELECTIONS_DIR, f"{v['id']}-2026.json")
            if os.path.exists(el_f):
                el_d = load_json(el_f)
                if el_d.get("resultats", {}).get("tour1"):
                    villes_avec_res.append(v)

        n_title = "Résultats municipales 2026 — Toutes les villes | #POURQUITUVOTES"
        n_desc = f"Résultats des municipales 2026 dans {len(villes_avec_res)} villes. Scores, participation et maires élus."
        if len(n_desc) > 155:
            n_desc = f"Résultats municipales 2026 : {len(villes_avec_res)} villes. Scores, participation, maires élus."
        n_url = f"{BASE_URL}/municipales-2026/resultats/"
        n_og = f"{OG_BASE}comparateur.jpg"

        # JSON-LD national
        nat_jsonld = json.dumps({
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Résultats des élections municipales 2026",
            "description": f"Résultats des élections municipales 2026 dans {len(villes_avec_res)} villes de France.",
            "url": n_url,
            "isPartOf": {"@type": "WebSite", "name": "#POURQUITUVOTES", "url": BASE_URL},
        }, ensure_ascii=False, indent=2)

        n_head = make_head(n_title, n_desc, n_url, n_og, jsonld=nat_jsonld)

        # SEO content national
        nat_seo = f"""  <section class="seo-content" aria-label="Résultats des élections municipales 2026 en France">
    <h2>Résultats des élections municipales 2026</h2>
    <p>Retrouvez les résultats des élections municipales 2026 dans {len(villes_avec_res)} villes de France.
    Le premier tour a eu lieu le 15 mars 2026 et le second tour le 22 mars 2026.</p>
    <h3>Villes avec résultats disponibles</h3>
    <ul>"""
        for v in villes_avec_res[:30]:
            nat_seo += f"""
      <li><a href="/municipales-2026/{escape(v['id'])}/resultats/">Résultats municipales 2026 {escape(v['nom'])}</a></li>"""
        if len(villes_avec_res) > 30:
            nat_seo += f"""
      <li>... et {len(villes_avec_res) - 30} autres villes</li>"""
        nat_seo += """
    </ul>
  </section>"""

        write_shell("municipales-2026/resultats/index.html", n_head, nat_assets, nat_body, dry_run, seo_content=nat_seo)
        count += 1
        print(f"  Shell national généré ({len(villes_avec_res)} villes)")
    else:
        print(f"  Template national introuvable, skip")

    # --- 7. Mettre à jour _redirects ---
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
/municipales-2026/:ville/resultats /municipales-2026/:ville/resultats/ 301
/municipales-2026/resultats /municipales-2026/resultats/ 301
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
