#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Envoie le template 4 (Programme publié) aux candidats avec programme complet.
Utilise l'API Brevo pour envoyer via le template déjà configuré.

Usage :
  python scripts/envoyer_template4.py --dry-run    # Affiche la liste sans envoyer
  python scripts/envoyer_template4.py --send        # Envoie réellement les emails
  python scripts/envoyer_template4.py --test        # Envoie 1 test à ronkopelman@gmail.com
"""

import sys
import io
import os
import csv
import json
import time
import urllib.request
import urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Clé API Brevo : lue depuis variable d'env ou depuis brevo_setup.py
API_KEY = os.environ.get("BREVO_API_KEY", "")
if not API_KEY:
    # Fallback: lire depuis brevo_setup.py (même dossier)
    import importlib.util
    _spec = importlib.util.spec_from_file_location("brevo_setup", os.path.join(os.path.dirname(__file__), "brevo_setup.py"))
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    API_KEY = _mod.API_KEY

BASE = "https://api.brevo.com/v3"
TEMPLATE_ID = 4
BASE_URL = "https://pourquituvotes.fr/municipales-2026"

# Civilités — liste manuelle des candidats féminins
FEMININS = {
    "appere", "assih", "chesnel", "chikirou", "dati", "frigout",
    "knafo", "lucas", "oziol", "perrein", "rolland", "spillebout",
}

# Statuts à EXCLURE de l'envoi (déjà contactés ou répondus)
EXCLURE_STATUTS = {"RÉPONDU", "PROGRAMME INTEGRE"}


def api_post(path, data):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(f"{BASE}{path}", data=body, method="POST")
    req.add_header("api-key", API_KEY)
    req.add_header("Content-Type", "application/json; charset=utf-8")
    try:
        resp = urllib.request.urlopen(req)
        raw = resp.read()
        return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, json.loads(raw) if raw else {}


def charger_candidats():
    """Charge les candidats avec programme complet + email depuis le CSV."""
    candidats = []
    with open("data/suivi_candidats.csv", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for r in reader:
            if r["programme_complet"] != "OUI":
                continue
            email = r.get("email", "").strip()
            if not email:
                continue
            cid = r["id"].strip()
            nom = r["candidat"].strip()
            ville = r["ville"].strip()
            statut = r.get("statut_contact", "").strip()

            # Déterminer la civilité
            civilite = "Mme" if cid in FEMININS else "M."

            # Construire l'URL de la fiche candidat
            ville_slug = ville.lower().replace(" ", "-").replace("'", "-")
            url_candidat = f"{BASE_URL}/{ville_slug}/candidats/{cid}/"

            candidats.append({
                "nom": nom,
                "ville": ville,
                "id": cid,
                "email": email,
                "civilite": civilite,
                "url_candidat": url_candidat,
                "statut": statut,
            })
    return candidats


def envoyer_email(candidat, dry_run=False):
    """Envoie le template 4 à un candidat."""
    payload = {
        "templateId": TEMPLATE_ID,
        "to": [{"email": candidat["email"], "name": candidat["nom"]}],
        "params": {
            "civilite": candidat["civilite"],
            "nom_candidat": candidat["nom"],
            "ville": candidat["ville"],
            "url_candidat": candidat["url_candidat"],
        },
    }

    if dry_run:
        print(f"  [DRY] {candidat['ville']:20s} {candidat['nom']:30s} → {candidat['email']}")
        return True

    status, data = api_post("/smtp/email", payload)
    if status in (200, 201):
        print(f"  [OK]  {candidat['ville']:20s} {candidat['nom']:30s} → {candidat['email']}")
        return True
    else:
        print(f"  [ERR] {candidat['ville']:20s} {candidat['nom']:30s} → {status}: {data}")
        return False


def main():
    mode = "--dry-run"
    if "--send" in sys.argv:
        mode = "--send"
    elif "--test" in sys.argv:
        mode = "--test"

    candidats = charger_candidats()

    if mode == "--test":
        print("=" * 60)
        print("  MODE TEST — envoi à ronkopelman@gmail.com uniquement")
        print("=" * 60)
        test_candidat = {
            "nom": "Test Candidat",
            "ville": "Paris",
            "id": "gregoire",
            "email": "ronkopelman@gmail.com",
            "civilite": "M.",
            "url_candidat": f"{BASE_URL}/paris/candidats/gregoire/",
            "statut": "",
        }
        envoyer_email(test_candidat)
        return

    # Filtrer les statuts déjà traités
    a_envoyer = [c for c in candidats if c["statut"] not in EXCLURE_STATUTS]
    exclus = [c for c in candidats if c["statut"] in EXCLURE_STATUTS]

    print("=" * 60)
    if mode == "--dry-run":
        print("  MODE DRY-RUN — aucun email ne sera envoyé")
    else:
        print("  MODE ENVOI RÉEL — les emails vont partir !")
    print("=" * 60)

    print(f"\n  Total candidats avec programme + email : {len(candidats)}")
    print(f"  Exclus (déjà contactés/répondus)       : {len(exclus)}")
    print(f"  À envoyer                              : {len(a_envoyer)}")

    if exclus:
        print(f"\n  Exclus :")
        for c in exclus:
            print(f"    {c['ville']:20s} {c['nom']:30s} ({c['statut']})")

    print(f"\n  Envois :")
    ok = 0
    err = 0
    for c in a_envoyer:
        success = envoyer_email(c, dry_run=(mode == "--dry-run"))
        if success:
            ok += 1
        else:
            err += 1
        if mode == "--send":
            time.sleep(0.5)  # Rate limiting Brevo

    print(f"\n  Résultat : {ok} OK, {err} erreurs")


if __name__ == "__main__":
    main()
