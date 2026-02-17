#!/usr/bin/env python3
"""
Complète l'export GTM avec tous les tags/triggers/variables manquants
depuis analytics.js
"""
import json, copy

INPUT  = r"C:\Users\KOPELMANRon\Downloads\GTM-T4CCTF6V_workspace3.json"
OUTPUT = r"C:\Users\KOPELMANRon\Downloads\GTM-T4CCTF6V_workspace3_complet.json"

ACCOUNT_ID   = "6337877513"
CONTAINER_ID = "243225258"
MEASUREMENT  = "{{Const - G-R6SL0ZWQQG}}"

# Compteurs IDs (après les max existants)
next_tag_id     = 44
next_trigger_id = 38
next_var_id     = 41
fp_counter      = 1771078400000

def next_fp():
    global fp_counter
    fp_counter += 1
    return str(fp_counter)

# ── Helpers pour construire les objets GTM ──

def make_param_map(name):
    return {
        "type": "MAP",
        "map": [
            {"type": "TEMPLATE", "key": "parameter", "value": name},
            {"type": "TEMPLATE", "key": "parameterValue", "value": "{{DLV - " + name + "}}"}
        ]
    }

def make_tag(tag_id, event_name, params, trigger_id):
    return {
        "accountId": ACCOUNT_ID,
        "containerId": CONTAINER_ID,
        "tagId": str(tag_id),
        "name": "GA4 - " + event_name,
        "type": "gaawe",
        "parameter": [
            {"type": "BOOLEAN", "key": "sendEcommerceData", "value": "false"},
            {"type": "LIST", "key": "eventSettingsTable", "list": [make_param_map(p) for p in params]},
            {"type": "TEMPLATE", "key": "eventName", "value": event_name},
            {"type": "TEMPLATE", "key": "measurementIdOverride", "value": MEASUREMENT}
        ],
        "fingerprint": next_fp(),
        "firingTriggerId": [str(trigger_id)],
        "tagFiringOption": "ONCE_PER_EVENT",
        "monitoringMetadata": {"type": "MAP"},
        "consentSettings": {"consentStatus": "NOT_SET"}
    }

def make_trigger(trigger_id, event_name):
    return {
        "accountId": ACCOUNT_ID,
        "containerId": CONTAINER_ID,
        "triggerId": str(trigger_id),
        "name": "CE - " + event_name,
        "type": "CUSTOM_EVENT",
        "customEventFilter": [{
            "type": "EQUALS",
            "parameter": [
                {"type": "TEMPLATE", "key": "arg0", "value": "{{_event}}"},
                {"type": "TEMPLATE", "key": "arg1", "value": event_name}
            ]
        }],
        "fingerprint": next_fp()
    }

def make_dlv(var_id, name):
    return {
        "accountId": ACCOUNT_ID,
        "containerId": CONTAINER_ID,
        "variableId": str(var_id),
        "name": "DLV - " + name,
        "type": "v",
        "parameter": [
            {"type": "INTEGER", "key": "dataLayerVersion", "value": "2"},
            {"type": "TEMPLATE", "key": "name", "value": name}
        ],
        "fingerprint": next_fp()
    }

# ── Charger l'export ──

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

cv = data["containerVersion"]
tags = cv["tag"]
triggers = cv["trigger"]
variables = cv["variable"]

existing_dlv_names = {v["name"].replace("DLV - ", "") for v in variables if v["name"].startswith("DLV - ")}
existing_trigger_map = {}

# Construire la map des triggers existants (nom → triggerId)
for t in triggers:
    existing_trigger_map[t["name"]] = t["triggerId"]

def ensure_dlv(name):
    """Ajoute une DLV si elle n'existe pas, retourne le nom GTM"""
    global next_var_id
    if name not in existing_dlv_names:
        variables.append(make_dlv(next_var_id, name))
        existing_dlv_names.add(name)
        next_var_id += 1

def add_params_to_tag(tag_name, new_params):
    """Ajoute des paramètres manquants à un tag existant"""
    for tag in tags:
        if tag["name"] == tag_name:
            for param in tag["parameter"]:
                if param.get("key") == "eventSettingsTable":
                    existing = set()
                    for item in param.get("list", []):
                        for m in item.get("map", []):
                            if m.get("key") == "parameter":
                                existing.add(m["value"])
                    for p in new_params:
                        if p not in existing:
                            param["list"].append(make_param_map(p))
                            ensure_dlv(p)
            break

def add_event(event_name, params):
    """Ajoute un tag + trigger + DLVs complets pour un nouvel événement"""
    global next_tag_id, next_trigger_id

    # Réutiliser un trigger existant s'il porte le même nom
    trigger_name = "CE - " + event_name
    if trigger_name in existing_trigger_map:
        trigger_id = existing_trigger_map[trigger_name]
    else:
        trigger_id = next_trigger_id
        triggers.append(make_trigger(trigger_id, event_name))
        existing_trigger_map[trigger_name] = str(trigger_id)
        next_trigger_id += 1

    tags.append(make_tag(next_tag_id, event_name, params, trigger_id))
    next_tag_id += 1

    for p in params:
        ensure_dlv(p)

# ══════════════════════════════════════════════
# 1. CORRIGER LE BUG search_city (eventName / measurementIdOverride inversés)
# ══════════════════════════════════════════════
for tag in tags:
    if tag["name"] == "GA4 - search_city":
        for param in tag["parameter"]:
            if param.get("key") == "eventName" and param["value"] == MEASUREMENT:
                param["value"] = "search_city"
            elif param.get("key") == "measurementIdOverride" and param["value"] == "G-XXXXXXXXXX":
                param["value"] = MEASUREMENT
        break

# ══════════════════════════════════════════════
# 2. AJOUTER LES PARAMÈTRES MANQUANTS AUX TAGS EXISTANTS
# ══════════════════════════════════════════════
add_params_to_tag("GA4 - scroll_depth",      ["time_on_page"])
add_params_to_tag("GA4 - search_city",        ["search_context", "page_path"])
add_params_to_tag("GA4 - outbound_click",     ["is_pdf", "is_source_verification", "page_path"])
add_params_to_tag("GA4 - social_share",       ["share_context", "page_path"])
add_params_to_tag("GA4 - city_selected",      ["page_path"])
add_params_to_tag("GA4 - candidate_filter",   ["candidates_selected", "candidates_available", "page_path"])
add_params_to_tag("GA4 - category_view",      ["time_on_page", "page_path"])
add_params_to_tag("GA4 - page_view_custom",   [])  # déjà complet

# ══════════════════════════════════════════════
# 3. AJOUTER LES ÉVÉNEMENTS MANQUANTS
# ══════════════════════════════════════════════

# Comparateur
add_event("consent_update", [
    "consent_analytics", "consent_marketing"
])

add_event("candidate_focus_change", [
    "selected_candidates_names", "selection_count", "page_path", "time_on_page"
])

add_event("source_verification", [
    "candidate_name", "category_id", "source_url", "time_on_page", "page_path"
])

add_event("view_mode_change", [
    "view_mode", "page_path"
])

# Simulateur (quiz)
add_event("quiz_start", [
    "city_name", "quiz_mode", "page_path"
])

add_event("quiz_step_complete", [
    "step_number", "total_steps", "category_id", "answer_value",
    "time_spent_seconds", "page_path"
])

add_event("quiz_answer_changed", [
    "step_number", "old_answer", "new_answer", "page_path"
])

add_event("quiz_priorities_set", [
    "priorities", "page_path"
])

add_event("quiz_result", [
    "city_name", "quiz_mode", "top_candidate", "top_match_pct",
    "podium_json", "questions_answered", "time_on_page", "page_path"
])

add_event("quiz_early_exit", [
    "step_at_exit", "total_steps", "completion_pct", "time_on_page", "page_path"
])

add_event("quiz_result_share", [
    "platform", "top_candidate", "top_match_pct", "page_path"
])

# FAQ
add_event("faq_question_open", [
    "question_id", "question_text", "page_path"
])

# Recherche
add_event("search_no_result", [
    "search_term", "page_path"
])

# Formulaires
add_event("lead_notification_request", [
    "requested_city", "email_hash", "page_path"
])

add_event("form_submit_report", [
    "report_city", "report_category", "time_on_page"
])

add_event("lead_capture", [
    "form_type", "page_path", "time_on_page"
])

# Modales
add_event("modal_open", [
    "modal_name", "page_path"
])

# Identification
add_event("user_identified", [
    "user_id_hashed", "method"
])

# ══════════════════════════════════════════════
# 4. ÉCRIRE LE RÉSULTAT
# ══════════════════════════════════════════════

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Stats
existing_tag_names = [t["name"] for t in tags if t["name"].startswith("GA4 - ")]
existing_trigger_names = [t["name"] for t in triggers if t["name"].startswith("CE - ")]
print(f"Tags GA4 :     {len(existing_tag_names)}")
print(f"Triggers CE :  {len(existing_trigger_names)}")
print(f"Variables DLV : {len([v for v in variables if v['name'].startswith('DLV - ')])}")
print(f"Fichier écrit : {OUTPUT}")
