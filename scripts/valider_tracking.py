#!/usr/bin/env python3
"""
Audit de cohérence tracking : analytics.js ↔ app.js/simulateur.js/HTML ↔ GTM ↔ GA4
Lance après chaque modif de analytics.js, app.js, simulateur.js ou du GTM.

Usage : python scripts/valider_tracking.py
        python scripts/valider_tracking.py --fix-gtm   (vérifie aussi le GTM via API)
        python scripts/valider_tracking.py --check-ga4  (vérifie que GA4 reçoit bien les events)
"""
import sys
import io
import os
import re
import json
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS_DIR = os.path.join(PROJECT, "js")
HTML_DIR = PROJECT

# ══════════════════════════════════════════════
# 1. PARSER analytics.js — extraire tous les events et leur mode de déclenchement
# ══════════════════════════════════════════════

def parse_analytics_js():
    """Parse analytics.js et retourne la liste des events avec leur type de déclenchement."""
    path = os.path.join(JS_DIR, "analytics.js")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    events = {}

    # 1a. Events auto-déclenchés (sendAnalyticsEvent appelé directement dans analytics.js)
    # Ces events se déclenchent via des listeners DOM dans analytics.js
    auto_patterns = {
        "page_view_custom": {"trigger": "auto:page_load", "needs_html": False},
        "scroll_depth": {"trigger": "auto:scroll", "needs_html": False},
        "outbound_click": {"trigger": "auto:click a[target=_blank]", "needs_html": False},
    }

    # Détection des listeners de formulaire
    if 'form.id === "form-signalement"' in content:
        auto_patterns["form_submit_report"] = {"trigger": "auto:submit #form-signalement", "needs_html": True, "html_selector": "form#form-signalement"}
    if 'form.id === "form-alerte"' in content or 'form.id === "form-newsletter"' in content:
        auto_patterns["lead_capture"] = {"trigger": "auto:submit #form-alerte|#form-newsletter", "needs_html": True, "html_selector": "form#form-alerte, form#form-newsletter"}
    if "data-modal" in content:
        auto_patterns["modal_open"] = {"trigger": "auto:click [data-modal]", "needs_html": True, "html_selector": "[data-modal]"}
    if "search-ville" in content:
        auto_patterns["search_city"] = {"trigger": "auto:input #search-ville|#sim-search|.search-float__input", "needs_html": True, "html_selector": "#search-ville, #sim-search, .search-float__input"}
    if "partage-btn" in content or "social_share" in content:
        auto_patterns["social_share"] = {"trigger": "auto:click .partage-btn|.sim-share__btn", "needs_html": True, "html_selector": ".partage-btn, .sim-share__btn, [data-track-event='social_share']"}
    if "search_no_result" in content:
        auto_patterns["search_no_result"] = {"trigger": "api:renderNoResult", "needs_html": False}
    if "lead_notification_request" in content:
        auto_patterns["lead_notification_request"] = {"trigger": "api:renderNoResult form submit", "needs_html": False}
    if "user_identified" in content:
        auto_patterns["user_identified"] = {"trigger": "auto:form with email", "needs_html": False}

    events.update(auto_patterns)

    # 1b. Events exposés via PQTV_Analytics (API publique = doivent être appelés par app.js/simulateur.js)
    api_pattern = re.compile(r'(track\w+):\s*function\s*\([^)]*\)\s*\{[^}]*sendAnalyticsEvent\("(\w+)"', re.DOTALL)
    for match in api_pattern.finditer(content):
        func_name = match.group(1)
        event_name = match.group(2)
        if event_name not in events:
            events[event_name] = {"trigger": f"api:PQTV_Analytics.{func_name}", "needs_call": True, "func_name": func_name}

    return events


# ══════════════════════════════════════════════
# 2. VÉRIFIER que chaque event API est appelé dans le code
# ══════════════════════════════════════════════

def check_api_calls(events):
    """Vérifie que chaque fonction PQTV_Analytics.trackX est appelée quelque part."""
    js_files = []
    for f in os.listdir(JS_DIR):
        if f.endswith(".js") and f != "analytics.js":
            js_files.append(os.path.join(JS_DIR, f))

    # Also check inline scripts in key HTML files
    html_with_scripts = [
        os.path.join(PROJECT, "faq.html"),
        os.path.join(PROJECT, "index.html"),
        os.path.join(PROJECT, "municipales", "2026", "index.html"),
        os.path.join(PROJECT, "municipales", "2026", "simulateur.html"),
    ]

    all_js_content = ""
    for path in js_files:
        with open(path, "r", encoding="utf-8") as f:
            all_js_content += f.read() + "\n"
    for path in html_with_scripts:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                all_js_content += f.read() + "\n"

    results = {}
    for event_name, info in events.items():
        if not info.get("needs_call"):
            continue
        func_name = info["func_name"]
        # Chercher PQTV_Analytics.trackX( dans tout le JS
        pattern = rf"PQTV_Analytics\.{func_name}\s*\("
        matches = re.findall(pattern, all_js_content)
        results[event_name] = {
            "func": func_name,
            "calls_found": len(matches),
            "ok": len(matches) > 0
        }

    return results


# ══════════════════════════════════════════════
# 3. VÉRIFIER que les éléments HTML existent pour les auto-listeners
# ══════════════════════════════════════════════

def check_html_elements(events):
    """Vérifie que les sélecteurs HTML ciblés par les auto-listeners existent.
    On ne check qu'un sample de pages (pas les 103 villes identiques)."""
    # Pages représentatives (pas besoin de lire les 103 dossiers villes)
    sample_pages = [
        os.path.join(PROJECT, "index.html"),
        os.path.join(PROJECT, "municipales", "2026", "index.html"),
        os.path.join(PROJECT, "municipales", "2026", "simulateur.html"),
        os.path.join(PROJECT, "municipales-2026", "paris", "index.html"),
        os.path.join(PROJECT, "methodologie.html"),
        os.path.join(PROJECT, "faq.html"),
        os.path.join(PROJECT, "a-propos.html"),
    ]

    all_html = ""
    for path in sample_pages:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                all_html += f.read() + "\n"

    results = {}
    selector_checks = {
        "form#form-signalement": r'id=["\']form-signalement["\']',
        "form#form-alerte, form#form-newsletter": r'id=["\']form-(alerte|newsletter)["\']',
        "[data-modal]": r'data-modal',
        "#search-ville, #sim-search, .search-float__input": r'(id=["\']search-ville["\']|id=["\']sim-search["\']|search-float__input)',
        ".partage-btn, .sim-share__btn, [data-track-event='social_share']": r'(partage-btn|sim-share__btn|data-track-event=["\']social_share["\'])',
    }

    for event_name, info in events.items():
        if not info.get("needs_html"):
            continue
        selector = info.get("html_selector", "")
        regex = selector_checks.get(selector)
        if regex:
            matches = re.findall(regex, all_html)
            results[event_name] = {
                "selector": selector,
                "found": len(matches),
                "ok": len(matches) > 0
            }

    return results


# ══════════════════════════════════════════════
# 4. VÉRIFIER GTM via API (optionnel)
# ══════════════════════════════════════════════

def check_gtm(events):
    """Vérifie que chaque event a un tag + trigger dans GTM."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("  ⚠️  google-api-python-client non installé, skip GTM check")
        return {}

    creds_path = os.path.join(PROJECT, "scripts", "google_credentials.json")
    creds = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=["https://www.googleapis.com/auth/tagmanager.edit.containers"]
    )
    service = build("tagmanager", "v2", credentials=creds)
    path = "accounts/6337877513/containers/243225258"

    live = service.accounts().containers().versions().live(parent=path).execute()

    live_tags = {t.get("name", "").replace("GA4 - ", ""): t for t in live.get("tag", []) if t.get("name", "").startswith("GA4 - ")}
    live_triggers = {t.get("name", "").replace("CE - ", ""): t for t in live.get("trigger", []) if t.get("name", "").startswith("CE - ")}

    results = {}
    for event_name in events:
        has_tag = event_name in live_tags
        has_trigger = event_name in live_triggers
        results[event_name] = {
            "tag": has_tag,
            "trigger": has_trigger,
            "ok": has_tag and has_trigger
        }

    return results


# ══════════════════════════════════════════════
# 5. VÉRIFIER GA4 — est-ce que les events arrivent ? (optionnel)
# ══════════════════════════════════════════════

def check_ga4(events):
    """Vérifie dans GA4 quels events ont des données (derniers 7 jours)."""
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            RunReportRequest, DateRange, Dimension, Metric, FilterExpression, Filter
        )
        from google.oauth2 import service_account
    except ImportError:
        print("  ⚠️  google-analytics-data non installé, skip GA4 check")
        return {}

    creds_path = os.path.join(PROJECT, "scripts", "google_credentials.json")
    creds = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )
    client = BetaAnalyticsDataClient(credentials=creds)

    # Get all events from last 7 days
    request = RunReportRequest(
        property="properties/524766237",
        dimensions=[Dimension(name="eventName")],
        metrics=[Metric(name="eventCount")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        limit=100,
    )
    response = client.run_report(request)

    ga4_events = {}
    for row in response.rows:
        ga4_events[row.dimension_values[0].value] = int(row.metric_values[0].value)

    results = {}
    for event_name in events:
        count = ga4_events.get(event_name, 0)
        results[event_name] = {
            "count_7d": count,
            "ok": count > 0
        }

    return results


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Audit tracking analytics.js ↔ JS ↔ HTML ↔ GTM ↔ GA4")
    parser.add_argument("--fix-gtm", action="store_true", help="Vérifie aussi la config GTM via API")
    parser.add_argument("--check-ga4", action="store_true", help="Vérifie aussi que GA4 reçoit les events")
    args = parser.parse_args()

    print("=" * 70)
    print("  AUDIT TRACKING — pourquituvotes.fr")
    print("=" * 70)

    # 1. Parse analytics.js
    events = parse_analytics_js()
    print(f"\n📋 {len(events)} events définis dans analytics.js\n")

    # 2. Check API calls
    print("─" * 70)
    print("VÉRIFICATION 1 : Fonctions PQTV_Analytics appelées dans le code JS")
    print("─" * 70)
    api_results = check_api_calls(events)
    errors_api = 0
    for event_name, result in sorted(api_results.items()):
        status = "✅" if result["ok"] else "❌"
        if not result["ok"]:
            errors_api += 1
        print(f"  {status} {event_name} (PQTV_Analytics.{result['func']}) — {result['calls_found']} appel(s)")

    # 3. Check HTML
    print(f"\n{'─' * 70}")
    print("VÉRIFICATION 2 : Éléments HTML pour les auto-listeners")
    print("─" * 70)
    html_results = check_html_elements(events)
    errors_html = 0
    for event_name, result in sorted(html_results.items()):
        status = "✅" if result["ok"] else "❌"
        if not result["ok"]:
            errors_html += 1
        print(f"  {status} {event_name} ({result['selector']}) — {result['found']} élément(s)")

    # 4. Check GTM (optional)
    gtm_results = {}
    errors_gtm = 0
    if args.fix_gtm:
        print(f"\n{'─' * 70}")
        print("VÉRIFICATION 3 : Tags et triggers GTM")
        print("─" * 70)
        gtm_results = check_gtm(events)
        for event_name, result in sorted(gtm_results.items()):
            status = "✅" if result["ok"] else "❌"
            if not result["ok"]:
                errors_gtm += 1
            tag_status = "tag ✅" if result["tag"] else "tag ❌"
            trigger_status = "trigger ✅" if result["trigger"] else "trigger ❌"
            print(f"  {status} {event_name} — {tag_status}, {trigger_status}")

    # 5. Check GA4 (optional)
    ga4_results = {}
    errors_ga4 = 0
    if args.check_ga4:
        print(f"\n{'─' * 70}")
        print("VÉRIFICATION 4 : Events reçus dans GA4 (7 derniers jours)")
        print("─" * 70)
        ga4_results = check_ga4(events)
        for event_name, result in sorted(ga4_results.items()):
            status = "✅" if result["ok"] else "⚠️ "
            if not result["ok"]:
                errors_ga4 += 1
            print(f"  {status} {event_name} — {result['count_7d']} events")

    # Résumé
    total_errors = errors_api + errors_html + errors_gtm + errors_ga4
    print(f"\n{'═' * 70}")
    print(f"  RÉSUMÉ")
    print(f"{'═' * 70}")
    print(f"  Appels JS manquants : {errors_api}")
    print(f"  Éléments HTML manquants : {errors_html}")
    if args.fix_gtm:
        print(f"  Tags/triggers GTM manquants : {errors_gtm}")
    if args.check_ga4:
        print(f"  Events absents dans GA4 : {errors_ga4}")
    print()

    if total_errors > 0:
        print(f"  ⚠️  {total_errors} problème(s) détecté(s)")
        print()
        if errors_api > 0:
            print("  → Ajouter les appels PQTV_Analytics.trackX() dans app.js/simulateur.js")
        if errors_html > 0:
            print("  → Ajouter les attributs HTML manquants (data-modal, partage-btn, etc.)")
        if errors_gtm > 0:
            print("  → Créer les tags/triggers manquants dans GTM (ou lancer fix_gtm.py)")
        if errors_ga4 > 0:
            print("  → Vérifier que la chaîne JS→dataLayer→GTM→GA4 fonctionne")
        sys.exit(1)
    else:
        print("  ✅ Tout est OK")
        sys.exit(0)


if __name__ == "__main__":
    main()
