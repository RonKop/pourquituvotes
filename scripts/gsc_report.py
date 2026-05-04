"""
Agent SEO — Google Search Console pour pourquituvotes.fr
Usage:
    python scripts/gsc_report.py                  # Rapport complet
    python scripts/gsc_report.py --indexation      # Focus problèmes d'indexation
    python scripts/gsc_report.py --opportunities   # Focus opportunités mots-clés
    python scripts/gsc_report.py --positions        # Focus positions actuelles
    python scripts/gsc_report.py --cannibalisation  # Détection cannibalisation
    python scripts/gsc_report.py --compare          # Comparaison période précédente
    python scripts/gsc_report.py --export           # Export CSV des données brutes
"""
import sys
import io
import os
import json
import csv
import argparse
from datetime import datetime, timedelta
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2 import service_account
from googleapiclient.discovery import build

# ── Config ────────────────────────────────────────────────────────────
SITE_URL = "sc-domain:pourquituvotes.fr"  # Domain property
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "google_credentials.json")
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "seo-reports")

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
)
service = build("searchconsole", "v1", credentials=credentials)


# ── Helpers ───────────────────────────────────────────────────────────

def date_str(days_ago):
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")


def query_gsc(start_days_ago=90, end_days_ago=0, dimensions=None, row_limit=1000,
              filters=None, search_type="web"):
    """Query GSC Search Analytics."""
    body = {
        "startDate": date_str(start_days_ago),
        "endDate": date_str(end_days_ago),
        "dimensions": dimensions or ["query"],
        "rowLimit": row_limit,
        "searchType": search_type,
    }
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    return service.searchanalytics().query(siteUrl=SITE_URL, body=body).execute()


def fmt_num(n):
    if isinstance(n, float):
        if n < 1:
            return f"{n:.2%}" if n > 0 else "0%"
        return f"{n:.1f}"
    return f"{n:,}".replace(",", " ")


def print_header(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def print_table(headers, rows, col_widths=None):
    if not rows:
        print("  (aucune donnée)")
        return
    if not col_widths:
        col_widths = []
        for i, h in enumerate(headers):
            max_w = len(h)
            for r in rows[:50]:
                max_w = max(max_w, len(str(r[i])))
            col_widths.append(min(max_w, 60))
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(f"  {header_line}")
    print(f"  {'-' * len(header_line)}")
    for row in rows:
        line = " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row))
        print(f"  {line}")


# ── Rapports ──────────────────────────────────────────────────────────

def report_overview():
    """Vue d'ensemble: impressions, clics, CTR, position moyenne."""
    print_header("VUE D'ENSEMBLE (28 derniers jours)")
    # Agréger via dimensions=["date"] (dimensions=[] ne renvoie qu'une ligne)
    data = query_gsc(28, 0, dimensions=["date"], row_limit=30)
    rows = data.get("rows", [])
    if rows:
        clicks = sum(r["clicks"] for r in rows)
        imp = sum(r["impressions"] for r in rows)
        ctr = clicks / imp if imp else 0
        pos = sum(r["position"] * r["impressions"] for r in rows) / imp if imp else 0
        print(f"  Clics:        {fmt_num(clicks)}")
        print(f"  Impressions:  {fmt_num(imp)}")
        print(f"  CTR moyen:    {ctr:.2%}")
        print(f"  Position moy: {pos:.1f}")

    # Evolution par jour
    print_header("ÉVOLUTION QUOTIDIENNE (28j)")
    data = query_gsc(28, 0, dimensions=["date"], row_limit=28)
    rows = []
    for r in sorted(data.get("rows", []), key=lambda x: x["keys"][0]):
        rows.append((
            r["keys"][0],
            fmt_num(r["clicks"]),
            fmt_num(r["impressions"]),
            f"{r['ctr']:.1%}",
            f"{r['position']:.1f}"
        ))
    print_table(["Date", "Clics", "Impressions", "CTR", "Position"], rows)


def report_positions():
    """Top mots-clés par clics et positions."""
    print_header("TOP 50 MOTS-CLÉS PAR CLICS (28j)")
    data = query_gsc(28, 0, dimensions=["query"], row_limit=50)
    rows = []
    for r in sorted(data.get("rows", []), key=lambda x: -x["clicks"]):
        rows.append((
            r["keys"][0][:55],
            fmt_num(r["clicks"]),
            fmt_num(r["impressions"]),
            f"{r['ctr']:.1%}",
            f"{r['position']:.1f}"
        ))
    print_table(["Mot-clé", "Clics", "Impressions", "CTR", "Position"], rows)

    print_header("TOP 30 PAGES PAR CLICS (28j)")
    data = query_gsc(28, 0, dimensions=["page"], row_limit=30)
    rows = []
    for r in sorted(data.get("rows", []), key=lambda x: -x["clicks"]):
        page = r["keys"][0].replace("https://pourquituvotes.fr", "")
        rows.append((
            page[:55] or "/",
            fmt_num(r["clicks"]),
            fmt_num(r["impressions"]),
            f"{r['ctr']:.1%}",
            f"{r['position']:.1f}"
        ))
    print_table(["Page", "Clics", "Impressions", "CTR", "Position"], rows)


def report_opportunities():
    """Mots-clés à fort potentiel: impressions élevées mais position > 10 ou CTR faible."""
    print_header("OPPORTUNITÉS — Impressions élevées, position > 10 (à améliorer)")
    data = query_gsc(28, 0, dimensions=["query"], row_limit=1000)
    opps = []
    for r in data.get("rows", []):
        if r["impressions"] >= 20 and r["position"] > 10:
            opps.append(r)
    opps.sort(key=lambda x: -x["impressions"])

    rows = []
    for r in opps[:40]:
        rows.append((
            r["keys"][0][:55],
            fmt_num(r["impressions"]),
            fmt_num(r["clicks"]),
            f"{r['position']:.1f}",
            f"{r['ctr']:.1%}"
        ))
    print_table(["Mot-clé", "Impressions", "Clics", "Position", "CTR"], rows)
    print(f"\n  → {len(opps)} mots-clés avec potentiel d'amélioration")

    print_header("OPPORTUNITÉS — CTR faible en top 10 (< 3%)")
    low_ctr = []
    for r in data.get("rows", []):
        if r["position"] <= 10 and r["ctr"] < 0.03 and r["impressions"] >= 50:
            low_ctr.append(r)
    low_ctr.sort(key=lambda x: -x["impressions"])

    rows = []
    for r in low_ctr[:30]:
        rows.append((
            r["keys"][0][:55],
            fmt_num(r["impressions"]),
            f"{r['ctr']:.1%}",
            f"{r['position']:.1f}",
            fmt_num(r["clicks"])
        ))
    print_table(["Mot-clé", "Impressions", "CTR", "Position", "Clics"], rows)
    print(f"\n  → {len(low_ctr)} mots-clés avec CTR à améliorer (title/description)")

    # Quick wins: position 11-20 avec beaucoup d'impressions
    print_header("QUICK WINS — Position 11-20, fort volume")
    quick = [r for r in data.get("rows", [])
             if 10 < r["position"] <= 20 and r["impressions"] >= 30]
    quick.sort(key=lambda x: -x["impressions"])
    rows = []
    for r in quick[:25]:
        rows.append((
            r["keys"][0][:55],
            fmt_num(r["impressions"]),
            f"{r['position']:.1f}",
            fmt_num(r["clicks"]),
            f"{r['ctr']:.1%}"
        ))
    print_table(["Mot-clé", "Impressions", "Position", "Clics", "CTR"], rows)
    print(f"\n  → {len(quick)} quick wins (un petit boost de contenu/liens suffit)")


def report_cannibalisation():
    """Détecte quand plusieurs pages se battent pour le même mot-clé."""
    print_header("CANNIBALISATION — Mots-clés multi-pages")
    data = query_gsc(28, 0, dimensions=["query", "page"], row_limit=5000)

    # Grouper par query
    by_query = defaultdict(list)
    for r in data.get("rows", []):
        by_query[r["keys"][0]].append({
            "page": r["keys"][1].replace("https://pourquituvotes.fr", ""),
            "clicks": r["clicks"],
            "impressions": r["impressions"],
            "position": r["position"],
        })

    # Filtrer: >= 2 pages avec >= 5 impressions chacune
    cannibals = {}
    for query, pages in by_query.items():
        significant = [p for p in pages if p["impressions"] >= 5]
        if len(significant) >= 2:
            cannibals[query] = sorted(significant, key=lambda x: -x["impressions"])

    # Trier par impressions totales
    sorted_cannibals = sorted(cannibals.items(),
                               key=lambda x: -sum(p["impressions"] for p in x[1]))

    count = 0
    for query, pages in sorted_cannibals[:20]:
        total_imp = sum(p["impressions"] for p in pages)
        print(f"\n  [{query}] — {len(pages)} pages, {total_imp} impressions totales")
        for p in pages[:4]:
            print(f"    {p['page'][:55]:55s} pos={p['position']:.1f}  imp={p['impressions']}  clics={p['clicks']}")
        count += 1

    if count == 0:
        print("  Aucune cannibalisation détectée (bon signe!)")
    else:
        print(f"\n  → {len(cannibals)} mots-clés cannibalisés détectés")


def report_compare():
    """Compare les 28 derniers jours vs les 28 jours précédents."""
    print_header("COMPARAISON — 28 derniers jours vs 28 jours précédents")

    current = query_gsc(28, 0, dimensions=["query"], row_limit=2000)
    previous = query_gsc(56, 28, dimensions=["query"], row_limit=2000)

    curr_map = {r["keys"][0]: r for r in current.get("rows", [])}
    prev_map = {r["keys"][0]: r for r in previous.get("rows", [])}

    # Mots-clés en hausse (gain de clics)
    gains = []
    for q, r in curr_map.items():
        prev = prev_map.get(q, {"clicks": 0, "impressions": 0, "position": 50})
        delta_clicks = r["clicks"] - prev["clicks"]
        delta_pos = prev.get("position", 50) - r["position"]  # positif = amélioration
        if delta_clicks > 0 and r["clicks"] >= 3:
            gains.append((q, r["clicks"], delta_clicks, r["position"], delta_pos, r["impressions"]))
    gains.sort(key=lambda x: -x[2])

    print_header("EN HAUSSE (gain de clics)")
    rows = [(g[0][:45], fmt_num(g[1]), f"+{g[2]}", f"{g[3]:.1f}", f"{g[4]:+.1f}") for g in gains[:25]]
    print_table(["Mot-clé", "Clics", "Delta", "Position", "DeltaPos"], rows)

    # Mots-clés en baisse
    losses = []
    for q, r in prev_map.items():
        curr = curr_map.get(q, {"clicks": 0, "impressions": 0, "position": 50})
        delta_clicks = curr["clicks"] - r["clicks"]
        if delta_clicks < 0 and r["clicks"] >= 3:
            losses.append((q, curr["clicks"], delta_clicks, curr.get("position", 50), r["position"]))
    losses.sort(key=lambda x: x[2])

    print_header("EN BAISSE (perte de clics)")
    rows = [(l[0][:45], fmt_num(l[1]), str(l[2]), f"{l[3]:.1f}", f"{l[4]:.1f}") for l in losses[:25]]
    print_table(["Mot-clé", "Clics actuel", "Delta", "Pos actuelle", "Pos avant"], rows)

    # Nouveaux mots-clés
    new_queries = [(q, r) for q, r in curr_map.items()
                   if q not in prev_map and r["clicks"] >= 2]
    new_queries.sort(key=lambda x: -x[1]["clicks"])

    print_header("NOUVEAUX MOTS-CLÉS (absents avant)")
    rows = [(q[:50], fmt_num(r["clicks"]), fmt_num(r["impressions"]), f"{r['position']:.1f}")
            for q, r in new_queries[:20]]
    print_table(["Mot-clé", "Clics", "Impressions", "Position"], rows)

    # Mots-clés disparus
    lost = [(q, r) for q, r in prev_map.items()
            if q not in curr_map and r["clicks"] >= 2]
    lost.sort(key=lambda x: -x[1]["clicks"])

    print_header("MOTS-CLÉS DISPARUS")
    rows = [(q[:50], fmt_num(r["clicks"]), fmt_num(r["impressions"]), f"{r['position']:.1f}")
            for q, r in lost[:20]]
    print_table(["Mot-clé", "Clics avant", "Impressions", "Position avant"], rows)


def report_indexation():
    """Vérifie l'état des sitemaps et inspecte les URLs problématiques."""
    print_header("ÉTAT DES SITEMAPS")
    try:
        sitemaps = service.sitemaps().list(siteUrl=SITE_URL).execute()
        for s in sitemaps.get("sitemap", []):
            submitted = s.get("contents", [{}])[0].get("submitted", "?")
            indexed = s.get("contents", [{}])[0].get("indexed", "?")
            print(f"  {s['path']}")
            print(f"    Soumises: {submitted} | Indexées: {indexed}")
            print(f"    Dernière soumission: {s.get('lastSubmitted', '?')}")
            print(f"    Dernière lecture: {s.get('lastDownloaded', '?')}")
            if s.get("warnings"):
                print(f"    ⚠ Warnings: {s['warnings']}")
            if s.get("errors"):
                print(f"    ❌ Erreurs: {s['errors']}")
    except Exception as e:
        print(f"  Erreur sitemaps: {e}")

    # Pages avec impressions mais 0 clics (possibles problèmes d'affichage)
    print_header("PAGES VISIBLES MAIS 0 CLICS (problème title/description?)")
    data = query_gsc(28, 0, dimensions=["page"], row_limit=500)
    zero_click = [r for r in data.get("rows", [])
                  if r["clicks"] == 0 and r["impressions"] >= 10]
    zero_click.sort(key=lambda x: -x["impressions"])

    rows = []
    for r in zero_click[:30]:
        page = r["keys"][0].replace("https://pourquituvotes.fr", "")
        rows.append((page[:55] or "/", fmt_num(r["impressions"]), f"{r['position']:.1f}"))
    print_table(["Page", "Impressions", "Position"], rows)

    # Inspection d'URL (API URL Inspection) — on inspecte les pages principales
    print_header("INSPECTION D'INDEXATION — Pages clés")
    key_pages = [
        "https://pourquituvotes.fr/",
        "https://pourquituvotes.fr/municipales/2026/",
        "https://pourquituvotes.fr/municipales/2026/simulateur.html",
        "https://pourquituvotes.fr/municipales/2026/resultats.html",
        "https://pourquituvotes.fr/methodologie",
        "https://pourquituvotes.fr/presidentielle/2027/",
    ]

    # Ajouter quelques pages villes populaires
    try:
        villes_path = os.path.join(os.path.dirname(__file__), "..", "data", "villes.json")
        with open(villes_path, "r", encoding="utf-8") as f:
            villes_data = json.load(f)
        top_villes = sorted(villes_data.get("villes", []),
                           key=lambda v: -v.get("population", 0))[:10]
        for v in top_villes:
            key_pages.append(f"https://pourquituvotes.fr/municipales/2026/{v['id']}/comparateur")
    except Exception:
        pass

    try:
        url_inspection = build("searchconsole", "v1", credentials=credentials)
        for url in key_pages[:15]:
            try:
                result = url_inspection.urlInspection().index().inspect(
                    body={"inspectionUrl": url, "siteUrl": SITE_URL}
                ).execute()
                inspection = result.get("inspectionResult", {})
                index_status = inspection.get("indexStatusResult", {})
                verdict = index_status.get("verdict", "?")
                coverage = index_status.get("coverageState", "?")
                crawled = index_status.get("lastCrawlTime", "?")
                robots = index_status.get("robotsTxtState", "?")
                indexing = index_status.get("indexingState", "?")

                short_url = url.replace("https://pourquituvotes.fr", "")
                status_icon = "✅" if verdict == "PASS" else "⚠️" if verdict == "NEUTRAL" else "❌"
                print(f"  {status_icon} {short_url or '/'}")
                print(f"     Verdict: {verdict} | Couverture: {coverage}")
                print(f"     Indexation: {indexing} | Robots: {robots}")
                print(f"     Dernier crawl: {crawled[:10] if crawled != '?' else '?'}")
            except Exception as e:
                short_url = url.replace("https://pourquituvotes.fr", "")
                print(f"  ⚠ {short_url}: {str(e)[:80]}")
    except Exception as e:
        print(f"  Inspection API non disponible: {e}")


def report_devices():
    """Performances par device (mobile vs desktop)."""
    print_header("PERFORMANCES PAR APPAREIL (28j)")
    for device in ["MOBILE", "DESKTOP", "TABLET"]:
        data = query_gsc(28, 0, dimensions=["query"], row_limit=1,
                        filters=[{"dimension": "device", "expression": device}])
        # Get totals
        total = query_gsc(28, 0, dimensions=[], row_limit=1,
                         filters=[{"dimension": "device", "expression": device}])
        if total.get("rows"):
            r = total["rows"][0]
            print(f"  {device:8s}: {fmt_num(r['clicks']):>8s} clics | {fmt_num(r['impressions']):>10s} imp | CTR {r['ctr']:.1%} | pos {r['position']:.1f}")


def report_countries():
    """Performances par pays."""
    print_header("PERFORMANCES PAR PAYS (28j)")
    data = query_gsc(28, 0, dimensions=["country"], row_limit=15)
    rows = []
    for r in sorted(data.get("rows", []), key=lambda x: -x["clicks"]):
        rows.append((
            r["keys"][0],
            fmt_num(r["clicks"]),
            fmt_num(r["impressions"]),
            f"{r['ctr']:.1%}",
            f"{r['position']:.1f}"
        ))
    print_table(["Pays", "Clics", "Impressions", "CTR", "Position"], rows)


def export_csv():
    """Exporte toutes les données brutes en CSV."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")

    # Keywords
    data = query_gsc(28, 0, dimensions=["query"], row_limit=5000)
    path = os.path.join(EXPORT_DIR, f"gsc_keywords_{today}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["query", "clicks", "impressions", "ctr", "position"])
        for r in data.get("rows", []):
            w.writerow([r["keys"][0], r["clicks"], r["impressions"],
                       f"{r['ctr']:.4f}", f"{r['position']:.1f}"])
    print(f"  ✓ {path} ({len(data.get('rows', []))} lignes)")

    # Pages
    data = query_gsc(28, 0, dimensions=["page"], row_limit=5000)
    path = os.path.join(EXPORT_DIR, f"gsc_pages_{today}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["page", "clicks", "impressions", "ctr", "position"])
        for r in data.get("rows", []):
            w.writerow([r["keys"][0], r["clicks"], r["impressions"],
                       f"{r['ctr']:.4f}", f"{r['position']:.1f}"])
    print(f"  ✓ {path} ({len(data.get('rows', []))} lignes)")

    # Keywords x Pages
    data = query_gsc(28, 0, dimensions=["query", "page"], row_limit=5000)
    path = os.path.join(EXPORT_DIR, f"gsc_keywords_pages_{today}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["query", "page", "clicks", "impressions", "ctr", "position"])
        for r in data.get("rows", []):
            w.writerow([r["keys"][0], r["keys"][1], r["clicks"], r["impressions"],
                       f"{r['ctr']:.4f}", f"{r['position']:.1f}"])
    print(f"  ✓ {path} ({len(data.get('rows', []))} lignes)")


# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Agent SEO — Google Search Console")
    parser.add_argument("--indexation", action="store_true", help="Focus indexation")
    parser.add_argument("--opportunities", action="store_true", help="Focus opportunités")
    parser.add_argument("--positions", action="store_true", help="Focus positions")
    parser.add_argument("--cannibalisation", action="store_true", help="Détection cannibalisation")
    parser.add_argument("--compare", action="store_true", help="Comparaison période")
    parser.add_argument("--export", action="store_true", help="Export CSV")
    args = parser.parse_args()

    print(f"╔══════════════════════════════════════════════════════════════════════╗")
    print(f"║  Agent SEO — pourquituvotes.fr — {datetime.now().strftime('%d/%m/%Y %H:%M'):>20s}              ║")
    print(f"╚══════════════════════════════════════════════════════════════════════╝")

    has_flag = any([args.indexation, args.opportunities, args.positions,
                    args.cannibalisation, args.compare, args.export])

    if not has_flag:
        # Rapport complet
        report_overview()
        report_positions()
        report_opportunities()
        report_cannibalisation()
        report_compare()
        report_indexation()
        report_devices()
        report_countries()
        print(f"\n{'='*70}")
        print("  FIN DU RAPPORT COMPLET")
        print(f"{'='*70}")
    else:
        if args.indexation:
            report_indexation()
        if args.positions:
            report_overview()
            report_positions()
            report_devices()
            report_countries()
        if args.opportunities:
            report_opportunities()
        if args.cannibalisation:
            report_cannibalisation()
        if args.compare:
            report_compare()
        if args.export:
            print_header("EXPORT CSV")
            export_csv()


if __name__ == "__main__":
    main()
