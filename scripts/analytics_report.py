"""
Rapport GA4 pour pourquituvotes.fr
Usage: python scripts/analytics_report.py
"""
import sys
import io
import os
import json
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Dimension, Metric, OrderBy, FilterExpression,
    Filter
)
from google.oauth2 import service_account

PROPERTY_ID = "524766237"
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "google_credentials.json")

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/analytics.readonly"]
)
client = BetaAnalyticsDataClient(credentials=credentials)


def run_report(dimensions, metrics, date_range="90daysAgo", limit=20, order_by_metric=None, dim_filter=None):
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=date_range, end_date="today")],
        limit=limit,
    )
    if order_by_metric:
        request.order_bys = [OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_by_metric), desc=True)]
    if dim_filter:
        request.dimension_filter = dim_filter
    return client.run_report(request)


def print_report(title, response, dimensions, metrics):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    headers = dimensions + metrics
    col_widths = [max(len(h), 12) for h in headers]
    # Adjust first col wider
    col_widths[0] = max(col_widths[0], 40)
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))
    for row in response.rows:
        vals = [dv.value for dv in row.dimension_values] + [mv.value for mv in row.metric_values]
        line = " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(vals))
        print(line)


def report_custom_events():
    """Events custom et leur volume"""
    print(f"\nRapport GA4 AVANCÉ — pourquituvotes.fr — {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Events custom
    r = run_report(["eventName"], ["eventCount", "activeUsers"], "90daysAgo", 50, "eventCount")
    print_report("TOUS LES EVENTS (top 50)", r, ["eventName"], ["count", "users"])

    # Events par page
    r = run_report(["eventName", "pagePath"], ["eventCount"], "90daysAgo", 30, "eventCount")
    print_report("EVENTS x PAGES (top 30)", r, ["event", "page"], ["count"])

    # Custom dimensions - essayer les plus courants
    for dim_name in ["customEvent:ville", "customEvent:candidat", "customEvent:categorie",
                     "customEvent:action_type", "customEvent:search_term",
                     "customUser:user_type"]:
        try:
            r = run_report([dim_name], ["eventCount", "activeUsers"], "90daysAgo", 20, "eventCount")
            if r.rows:
                print_report(f"DIMENSION: {dim_name}", r, [dim_name], ["count", "users"])
        except Exception as e:
            pass  # dimension doesn't exist

    # Engagement par jour (derniers 30 jours) pour voir la courbe
    r = run_report(["date"], ["activeUsers", "sessions", "screenPageViews", "eventCount"], "30daysAgo", 31, "sessions")
    print_report("ÉVOLUTION QUOTIDIENNE (30j)", r, ["date"], ["users", "sessions", "pageViews", "events"])

    # Funnel: landing → event conversion
    # Pages avec le plus d'events (engagement)
    r = run_report(["pagePath"], ["eventCount", "activeUsers", "engagedSessions"], "30daysAgo", 20, "eventCount")
    print_report("PAGES PAR ENGAGEMENT (events, 30j)", r, ["page"], ["events", "users", "engagedSessions"])

    # Nouveaux vs retour
    r = run_report(["newVsReturning"], ["activeUsers", "sessions", "averageSessionDuration"], "90daysAgo", 5, "sessions")
    print_report("NOUVEAUX vs RETOUR", r, ["type"], ["users", "sessions", "avgDuration"])

    # Heures de la journée
    r = run_report(["hour"], ["activeUsers", "sessions"], "30daysAgo", 24, "sessions")
    print_report("HEURES DE VISITE (30j)", r, ["heure"], ["users", "sessions"])

    # Requêtes de recherche interne (si configuré)
    try:
        search_filter = FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.EXACT,
                    value="search"
                )
            )
        )
        r = run_report(["searchTerm"], ["eventCount"], "90daysAgo", 20, "eventCount")
        if r.rows:
            print_report("RECHERCHES INTERNES", r, ["terme"], ["count"])
    except:
        pass


def report_deep_dive():
    """Analyse croisée tracking x features"""
    print(f"\nRapport GA4 DEEP DIVE — {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # 1. Events manquants vs plan de tracking
    # candidate_filter, category_view, view_mode_change, source_verification, social_share, lead_capture
    for event in ["candidate_filter", "category_view", "view_mode_change", "source_verification",
                  "social_share", "lead_capture", "form_submit_report", "lead_notification_request",
                  "quiz_step_complete", "quiz_early_exit", "quiz_priorities_set", "quiz_answer_changed",
                  "quiz_result_share"]:
        try:
            r = run_report(["eventName"], ["eventCount", "activeUsers"], "90daysAgo", 1, "eventCount",
                          FilterExpression(filter=Filter(field_name="eventName",
                              string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value=event))))
            if r.rows:
                print(f"  {event}: {r.rows[0].metric_values[0].value} events, {r.rows[0].metric_values[1].value} users")
            else:
                print(f"  {event}: 0 events ❌")
        except:
            print(f"  {event}: erreur requête")

    # 2. city_selected - quelles villes sont sélectionnées
    try:
        r = run_report(["customEvent:city_name"], ["eventCount", "activeUsers"], "90daysAgo", 30, "eventCount",
                      FilterExpression(filter=Filter(field_name="eventName",
                          string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value="city_selected"))))
        if r.rows:
            print_report("VILLES SÉLECTIONNÉES (city_selected)", r, ["city_name"], ["count", "users"])
    except:
        print("  city_name dimension non disponible")

    # 3. scroll_depth breakdown
    try:
        r = run_report(["customEvent:depth_percent"], ["eventCount", "activeUsers"], "90daysAgo", 10, "eventCount",
                      FilterExpression(filter=Filter(field_name="eventName",
                          string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value="scroll_depth"))))
        if r.rows:
            print_report("SCROLL DEPTH BREAKDOWN", r, ["depth_%"], ["count", "users"])
    except:
        print("  depth_percent dimension non disponible")

    # 4. candidate_focus_change - combien de candidats sélectionnés
    try:
        r = run_report(["customEvent:selection_count"], ["eventCount", "activeUsers"], "90daysAgo", 10, "eventCount",
                      FilterExpression(filter=Filter(field_name="eventName",
                          string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value="candidate_focus_change"))))
        if r.rows:
            print_report("FOCUS CHANGE - NB CANDIDATS SÉLECTIONNÉS", r, ["nb_selected"], ["count", "users"])
    except:
        print("  selection_count non disponible")

    # 5. search_no_result - termes recherchés
    try:
        r = run_report(["customEvent:search_term"], ["eventCount"], "90daysAgo", 30, "eventCount",
                      FilterExpression(filter=Filter(field_name="eventName",
                          string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value="search_no_result"))))
        if r.rows:
            print_report("RECHERCHES SANS RÉSULTAT", r, ["terme"], ["count"])
    except:
        print("  search_term sur no_result non disponible")

    # 6. outbound_click - quels liens
    try:
        r = run_report(["customEvent:link_url"], ["eventCount"], "90daysAgo", 20, "eventCount",
                      FilterExpression(filter=Filter(field_name="eventName",
                          string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value="outbound_click"))))
        if r.rows:
            print_report("LIENS SORTANTS CLIQUÉS", r, ["url"], ["count"])
    except:
        print("  link_url non disponible")

    # 7. Funnel: city_selected → candidate_focus_change → category_view
    print(f"\n{'='*60}")
    print("  FUNNEL ENGAGEMENT")
    print(f"{'='*60}")
    for event in ["city_selected", "candidate_focus_change", "candidate_filter",
                  "category_view", "view_mode_change", "source_verification",
                  "quiz_start", "quiz_result", "social_share", "outbound_click"]:
        try:
            r = run_report(["eventName"], ["eventCount", "activeUsers"], "90daysAgo", 1, "eventCount",
                          FilterExpression(filter=Filter(field_name="eventName",
                              string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value=event))))
            if r.rows:
                print(f"  {event:30s} → {r.rows[0].metric_values[0].value:>8s} events, {r.rows[0].metric_values[1].value:>6s} users")
            else:
                print(f"  {event:30s} → {'0':>8s} events")
        except:
            pass

    # 8. Pages candidats les plus visitées (pour voir si c'est les T2)
    candidat_filter = FilterExpression(
        filter=Filter(field_name="pagePath",
            string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.CONTAINS, value="/candidats/")))
    r = run_report(["pagePath"], ["screenPageViews", "activeUsers"], "7daysAgo", 30, "screenPageViews", candidat_filter)
    print_report("TOP PAGES CANDIDATS (7 derniers jours)", r, ["page"], ["vues", "users"])

    # 9. Évolution quotidienne dernière semaine (entre les 2 tours)
    r = run_report(["date"], ["activeUsers", "sessions", "eventCount"], "7daysAgo", 7, "sessions")
    print_report("ÉVOLUTION ENTRE LES 2 TOURS (7j)", r, ["date"], ["users", "sessions", "events"])


def main():
    report_deep_dive()
    return

    print(f"Rapport GA4 — pourquituvotes.fr — {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # 1. Vue d'ensemble
    r = run_report([], ["activeUsers", "sessions", "screenPageViews", "averageSessionDuration", "bounceRate"], "90daysAgo", 1)
    print(f"\n{'='*60}")
    print("  VUE D'ENSEMBLE (90 derniers jours)")
    print(f"{'='*60}")
    if r.rows:
        vals = [mv.value for mv in r.rows[0].metric_values]
        labels = ["Utilisateurs actifs", "Sessions", "Pages vues", "Durée moy. session (s)", "Taux de rebond"]
        for label, val in zip(labels, vals):
            if "rebond" in label or "Durée" in label:
                val = f"{float(val):.1f}{'%' if 'rebond' in label else 's'}"
            print(f"  {label}: {val}")

    # 2. Top pages
    r = run_report(["pagePath"], ["screenPageViews", "activeUsers", "averageSessionDuration"], "90daysAgo", 20, "screenPageViews")
    print_report("TOP 20 PAGES", r, ["pagePath"], ["pageViews", "users", "avgDuration"])

    # 3. Sources de trafic
    r = run_report(["sessionSource", "sessionMedium"], ["sessions", "activeUsers"], "90daysAgo", 15, "sessions")
    print_report("SOURCES DE TRAFIC", r, ["source", "medium"], ["sessions", "users"])

    # 4. Pages candidats/villes les plus vues
    ville_filter = FilterExpression(
        filter=Filter(
            field_name="pagePath",
            string_filter=Filter.StringFilter(
                match_type=Filter.StringFilter.MatchType.CONTAINS,
                value="/municipales/2026/"
            )
        )
    )
    r = run_report(["pagePath"], ["screenPageViews", "activeUsers"], "90daysAgo", 20, "screenPageViews", ville_filter)
    print_report("TOP PAGES MUNICIPALES", r, ["pagePath"], ["pageViews", "users"])

    # 5. Évolution hebdomadaire
    r = run_report(["week"], ["activeUsers", "sessions", "screenPageViews"], "90daysAgo", 15, "sessions")
    # Sort by week
    print_report("ÉVOLUTION HEBDOMADAIRE", r, ["semaine"], ["users", "sessions", "pageViews"])

    # 6. Appareils
    r = run_report(["deviceCategory"], ["sessions", "activeUsers", "bounceRate"], "90daysAgo", 5, "sessions")
    print_report("APPAREILS", r, ["device"], ["sessions", "users", "bounceRate"])

    # 7. Pays / Villes
    r = run_report(["city"], ["activeUsers", "sessions"], "90daysAgo", 15, "activeUsers")
    print_report("TOP VILLES (géo)", r, ["city"], ["users", "sessions"])

    # 8. Landing pages (pages d'entrée)
    r = run_report(["landingPage"], ["sessions", "activeUsers", "bounceRate"], "90daysAgo", 15, "sessions")
    print_report("PAGES D'ENTRÉE (landing pages)", r, ["landingPage"], ["sessions", "users", "bounceRate"])

    print(f"\n{'='*60}")
    print("  FIN DU RAPPORT")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
