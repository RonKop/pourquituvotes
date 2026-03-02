#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Envoie les emails aux 150 plus grandes mairies de France.
Deux versions :
  - Template 5 (Version A) : couverture complète (tous candidats programmeComplet)
  - Template 6 (Version B) : couverture partielle ou ville pas encore sur la plateforme

Usage :
  python scripts/envoyer_emails_mairies.py --dry-run         # Simule sans envoyer
  python scripts/envoyer_emails_mairies.py --preview Paris    # Prévisualise un email
  python scripts/envoyer_emails_mairies.py --send             # Envoie (confirmation demandée)
  python scripts/envoyer_emails_mairies.py --send --batch 10  # Envoie les N premières
  python scripts/envoyer_emails_mairies.py --test             # Test vers ronkopelman@gmail.com
"""

import csv
import glob
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# --- Config Brevo ---
API_KEY = os.environ.get("BREVO_API_KEY", "")
if not API_KEY:
    # Fallback: lire depuis brevo_setup.py (même dossier)
    try:
        import importlib.util
        _spec = importlib.util.spec_from_file_location("brevo_setup", os.path.join(os.path.dirname(os.path.abspath(__file__)), "brevo_setup.py"))
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        API_KEY = _mod.API_KEY
    except Exception:
        print("ERREUR: Clé API Brevo manquante. Définir BREVO_API_KEY ou créer scripts/brevo_setup.py")
        sys.exit(1)
BASE = "https://api.brevo.com/v3"
TEMPLATE_A = 5  # Couverture complète
TEMPLATE_B = 6  # Couverture partielle / nouvelle ville
DAILY_LIMIT = 295  # Brevo free plan = 300/jour, on garde une marge

# --- Chemins ---
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Utilise le fichier le plus large disponible
CSV_1000 = os.path.join(ROOT, "data", "mairies_1000_villes.csv")
CSV_500 = os.path.join(ROOT, "data", "mairies_500_villes.csv")
CSV_150 = os.path.join(ROOT, "data", "mairies_150_villes.csv")
CSV_PATH = CSV_1000 if os.path.exists(CSV_1000) else (CSV_500 if os.path.exists(CSV_500) else CSV_150)
ELECTIONS_DIR = os.path.join(ROOT, "data", "elections")
LOG_PATH = os.path.join(ROOT, "data", "emails_mairies_envoyes.json")

# Villes avec couverture complète (tous candidats ont programmeComplet: true)
VILLES_COMPLETE = {"paris", "vitry-sur-seine"}


# ═══════════════════════════════════════════════
# Brevo API
# ═══════════════════════════════════════════════

def brevo_api(method, path, data=None):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data else None
    req = urllib.request.Request(f"{BASE}{path}", data=body, method=method)
    req.add_header("api-key", API_KEY)
    req.add_header("Content-Type", "application/json; charset=utf-8")
    try:
        resp = urllib.request.urlopen(req)
        raw = resp.read()
        return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, json.loads(raw) if raw else {}


# ═══════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════

def normalize_slug(name):
    """Convertit un nom de ville en slug compatible avec nos fichiers."""
    import unicodedata
    slug = name.lower().strip()
    # Normaliser les accents
    slug = unicodedata.normalize("NFD", slug)
    slug = "".join(c for c in slug if unicodedata.category(c) != "Mn")
    slug = slug.replace(" ", "-").replace("'", "-").replace("(", "").replace(")", "")
    # Cas spéciaux
    slug = slug.replace("saint-", "saint-").replace("sainte-", "sainte-")
    return slug


def find_election_file(city_name):
    """Trouve le fichier election JSON pour une ville."""
    slug = normalize_slug(city_name)
    # Essai direct
    path = os.path.join(ELECTIONS_DIR, f"{slug}-2026.json")
    if os.path.exists(path):
        return path
    # Essai partiel
    for f in glob.glob(os.path.join(ELECTIONS_DIR, "*-2026.json")):
        f_slug = os.path.basename(f).replace("-2026.json", "")
        if slug in f_slug or f_slug in slug:
            return f
    return None


def get_city_stats(election_path):
    """Retourne les stats d'une ville (nb candidats, nb mesures, nb complets)."""
    with open(election_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    candidats = {}
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            for cid, prop in st.get("propositions", {}).items():
                if prop and prop.get("mesures"):
                    candidats[cid] = candidats.get(cid, 0) + len(prop["mesures"])

    nb_complets = 0
    for c in data.get("candidats", []):
        if c.get("programmeComplet"):
            nb_complets += 1

    # Slug from filename (e.g. "paris-2026.json" -> "paris")
    slug = os.path.basename(election_path).replace("-2026.json", "")

    return {
        "nb_candidats": len(data.get("candidats", [])),
        "nb_avec_mesures": len(candidats),
        "nb_mesures": sum(candidats.values()),
        "nb_complets": nb_complets,
        "ville_nom": data.get("ville", ""),
        "ville_slug": slug,
    }


def load_sent_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_sent_log(log):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def load_mairies():
    """Charge le CSV des mairies et enrichit avec les données de la plateforme."""
    mairies = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_email = row.get("email", "").strip()
            verified = row.get("email_verified", "").strip()

            # Ignorer les villes sans email valide
            if not raw_email or "formulaire" in raw_email.lower() or "contact form" in raw_email.lower():
                continue

            # Multi-emails : prendre le premier (séparateur ; ou ,)
            email = re.split(r"[;,]", raw_email)[0].strip()
            if verified and "no" in verified.lower() and "form" in verified.lower():
                continue

            city_name = row["city_name"].strip()
            population = int(row.get("population", "0").replace(",", "").strip() or "0")

            # Chercher le fichier election
            election_path = find_election_file(city_name)
            stats = get_city_stats(election_path) if election_path else None

            # Déterminer la version du template
            ville_slug = stats["ville_slug"] if stats else normalize_slug(city_name)
            is_complete = ville_slug in VILLES_COMPLETE
            on_platform = election_path is not None

            mairies.append({
                "city_name": city_name,
                "email": email,
                "population": population,
                "on_platform": on_platform,
                "is_complete": is_complete,
                "template_id": TEMPLATE_A if is_complete else TEMPLATE_B,
                "stats": stats,
                "ville_slug": ville_slug,
            })

    # Trier par population décroissante
    mairies.sort(key=lambda m: -m["population"])
    return mairies


def build_params(mairie):
    """Construit les paramètres Brevo pour une mairie."""
    stats = mairie["stats"]
    params = {
        "nom_ville": mairie["city_name"],
    }

    if stats and mairie["on_platform"]:
        slug = stats["ville_slug"] or mairie["ville_slug"]
        params["url_ville"] = f"https://pourquituvotes.fr/?ville={slug}"
        params["nb_candidats"] = stats["nb_candidats"]
        params["nb_avec_programme"] = stats["nb_complets"]
        params["nb_mesures"] = stats["nb_mesures"]
        params["sur_plateforme"] = "oui"
    else:
        params["url_ville"] = "https://pourquituvotes.fr"
        params["nb_candidats"] = 0
        params["nb_avec_programme"] = 0
        params["nb_mesures"] = 0
        params["sur_plateforme"] = "non"

    return params


# ═══════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════

def main():
    dry_run = "--dry-run" in sys.argv
    send = "--send" in sys.argv
    test_mode = "--test" in sys.argv
    preview_mode = "--preview" in sys.argv

    batch_size = None
    if "--batch" in sys.argv:
        idx = sys.argv.index("--batch")
        batch_size = int(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) else 10

    resume_mode = "--resume" in sys.argv

    if not dry_run and not send and not test_mode and not preview_mode and not resume_mode:
        print("Usage :")
        print("  --dry-run           Simule sans envoyer")
        print("  --preview VILLE     Prévisualise l'email pour une ville")
        print("  --send              Envoie vraiment (confirmation demandée)")
        print("  --send --batch 10   Envoie les N premières")
        print("  --resume            Reprend l'envoi (pour le lendemain)")
        print("  --test              Test vers ronkopelman@gmail.com")
        return

    # Test mode
    if test_mode:
        print("=" * 60)
        print("  MODE TEST — envoi à ronkopelman@gmail.com")
        print("=" * 60)

        # Test Version B (le plus courant)
        payload = {
            "templateId": TEMPLATE_B,
            "to": [{"email": "ronkopelman@gmail.com", "name": "Mairie Test"}],
            "params": {
                "nom_ville": "Lyon",
                "url_ville": "https://pourquituvotes.fr/?ville=lyon",
                "nb_candidats": 6,
                "nb_avec_programme": 4,
                "nb_mesures": 350,
                "sur_plateforme": "oui",
            },
        }
        status, data = brevo_api("POST", "/smtp/email", payload)
        if status in (200, 201):
            print(f"  [OK] Template B envoyé !")
        else:
            print(f"  [ERREUR {status}] {data}")

        # Test Version A
        payload["templateId"] = TEMPLATE_A
        payload["params"]["nom_ville"] = "Paris"
        payload["params"]["url_ville"] = "https://pourquituvotes.fr/?ville=paris"
        payload["params"]["nb_candidats"] = 6
        payload["params"]["nb_avec_programme"] = 6
        payload["params"]["nb_mesures"] = 900
        status, data = brevo_api("POST", "/smtp/email", payload)
        if status in (200, 201):
            print(f"  [OK] Template A envoyé !")
        else:
            print(f"  [ERREUR {status}] {data}")
        return

    # Charger les données
    mairies = load_mairies()
    sent_log = load_sent_log()

    # Exclure déjà envoyés
    mairies_to_send = [m for m in mairies if m["email"] not in sent_log]

    # Preview mode
    if preview_mode:
        idx = sys.argv.index("--preview")
        search = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        found = [m for m in mairies if search.lower() in m["city_name"].lower()]
        if not found:
            print(f"  Ville '{search}' non trouvée dans le CSV.")
            return
        m = found[0]
        params = build_params(m)
        tpl = "A (complète)" if m["is_complete"] else "B (partielle)"
        print(f"\n  {'='*50}")
        print(f"  PREVIEW — {m['city_name']}")
        print(f"  {'='*50}")
        print(f"  Email       : {m['email']}")
        print(f"  Population  : {m['population']:,}")
        print(f"  Template    : {tpl} (id: {m['template_id']})")
        print(f"  Sur plateforme : {'Oui' if m['on_platform'] else 'Non'}")
        if m["stats"]:
            s = m["stats"]
            print(f"  Candidats   : {s['nb_candidats']} ({s['nb_complets']} complets)")
            print(f"  Mesures     : {s['nb_mesures']}")
        print(f"\n  Params Brevo :")
        for k, v in params.items():
            print(f"    {k}: {v}")
        return

    # Batch
    if batch_size:
        mairies_to_send = mairies_to_send[:batch_size]

    print(f"{'='*60}")
    print(f"  EMAILS MAIRIES — Municipales 2026")
    if dry_run:
        print(f"  MODE DRY-RUN — aucun email ne sera envoyé")
    else:
        print(f"  MODE ENVOI RÉEL")
    print(f"{'='*60}")
    print(f"  Total mairies dans CSV     : {len(mairies)}")
    print(f"  Déjà envoyés               : {len(sent_log)}")
    print(f"  À envoyer                  : {len(mairies_to_send)}")
    if batch_size:
        print(f"  Batch                      : {batch_size}")

    # Stats
    version_a = [m for m in mairies_to_send if m["is_complete"]]
    version_b_on = [m for m in mairies_to_send if not m["is_complete"] and m["on_platform"]]
    version_b_off = [m for m in mairies_to_send if not m["is_complete"] and not m["on_platform"]]
    print(f"\n  Version A (couverture complète) : {len(version_a)}")
    print(f"  Version B (sur plateforme)      : {len(version_b_on)}")
    print(f"  Version B (pas sur plateforme)  : {len(version_b_off)}")
    print()

    # Afficher la liste
    for i, m in enumerate(mairies_to_send):
        tpl = "A" if m["is_complete"] else "B"
        plat = "PLT" if m["on_platform"] else "NEW"
        stats_str = ""
        if m["stats"]:
            s = m["stats"]
            stats_str = f"{s['nb_complets']}/{s['nb_candidats']} complets, {s['nb_mesures']} mes."
        print(f"  [{i+1:3d}] {tpl} {plat} {m['city_name']:28s} {m['population']:>10,}  {m['email']:45s}  {stats_str}")

    if dry_run:
        print(f"\n  [DRY-RUN] Aucun email envoyé.")
        return

    if send or resume_mode:
        # Calculer combien on peut envoyer aujourd'hui
        today = time.strftime("%Y-%m-%d")
        sent_today = sum(1 for v in sent_log.values() if v.get("sent_at", "").startswith(today))
        remaining_quota = max(0, DAILY_LIMIT - sent_today)

        actual_batch = mairies_to_send
        deferred = []
        if len(mairies_to_send) > remaining_quota:
            actual_batch = mairies_to_send[:remaining_quota]
            deferred = mairies_to_send[remaining_quota:]

        print(f"\n  Quota Brevo restant aujourd'hui : ~{remaining_quota}")
        print(f"  Envoi maintenant : {len(actual_batch)}")
        if deferred:
            print(f"  Reportés à demain : {len(deferred)}")

        if not actual_batch:
            print(f"\n  Quota épuisé pour aujourd'hui. Relancez demain avec :")
            print(f"    python scripts/envoyer_emails_mairies.py --resume")
            return

        confirm = input(f"\n  Envoyer {len(actual_batch)} emails maintenant ? (oui/non) : ").strip().lower()
        if confirm != "oui":
            print("  Annulé.")
            return

        success = 0
        errors = 0

        for i, m in enumerate(actual_batch):
            params = build_params(m)
            payload = {
                "templateId": m["template_id"],
                "to": [{"email": m["email"], "name": f"Mairie de {m['city_name']}"}],
                "params": params,
            }

            print(f"  [{i+1}/{len(actual_batch)}] {m['city_name']:25s}...", end=" ")

            status, data = brevo_api("POST", "/smtp/email", payload)
            sent_at = time.strftime("%Y-%m-%d %H:%M:%S")

            if status in (200, 201):
                print("OK")
                success += 1
                sent_log[m["email"]] = {
                    "ville": m["city_name"],
                    "template": m["template_id"],
                    "sent_at": sent_at,
                    "message_id": data.get("messageId", ""),
                }
                save_sent_log(sent_log)
            else:
                print(f"ERREUR {status} : {data}")
                errors += 1
                # Si erreur 429 (rate limit), on arrête
                if status == 429:
                    print(f"\n  Rate limit atteint ! {success} envoyé(s).")
                    print(f"  Relancez demain : python scripts/envoyer_emails_mairies.py --resume")
                    break

            # Pause entre les envois (rate limit Brevo)
            if i < len(actual_batch) - 1:
                time.sleep(1)

        print(f"\n{'='*60}")
        print(f"  Terminé : {success} envoyé(s), {errors} erreur(s)")
        if deferred:
            print(f"  {len(deferred)} emails reportés à demain.")
            print(f"  Relancez : python scripts/envoyer_emails_mairies.py --resume")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
