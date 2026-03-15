#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrape les résultats live depuis le Ministère de l'Intérieur.
Source : resultats-elections.interieur.gouv.fr

Tourne automatiquement via GitHub Actions le soir d'élection.
Récupère les résultats disponibles, les injecte dans les JSON, et déploie.

Usage :
  python scripts/scrape_resultats_live.py --tour 1
  python scripts/scrape_resultats_live.py --tour 2
  python scripts/scrape_resultats_live.py --tour 1 --ville paris
"""

import sys
import io
import json
import os
import re
import argparse
import unicodedata
from datetime import datetime

try:
    import urllib.request
    import urllib.error
except ImportError:
    pass

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
VILLES_JSON = os.path.join(DATA_DIR, "villes.json")

DATES = {"1": "2026-03-15", "2": "2026-03-22"}

# API du Ministère de l'Intérieur — résultats en temps réel
# Format typique : JSON par département puis par commune
# L'URL exacte peut varier, voici les patterns connus
BASE_URLS = [
    "https://resultats-elections.interieur.gouv.fr/municipales-2026",
    "https://www.resultats-elections.interieur.gouv.fr/municipales-2026",
]

# Mapping département → code pour l'API
# L'API du Ministère utilise le code département dans l'URL


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def normalize(text):
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower().strip()
    text = re.sub(r"[-'\s]+", " ", text)
    text = re.sub(r"^(le |la |les |l )", "", text)
    return text


def fetch_json(url):
    """Fetch JSON depuis une URL."""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'PQTV-Bot/1.0 (pourquituvotes.fr)')
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None


def fetch_html(url):
    """Fetch HTML depuis une URL."""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'PQTV-Bot/1.0 (pourquituvotes.fr)')
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.read().decode('utf-8', errors='replace')
    except Exception:
        return None


def discover_api_format(tour):
    """Tente de découvrir le format de l'API du Ministère."""
    # Patterns connus des élections précédentes
    patterns = [
        # Format 2020/2024
        "{base}/resultats/tour{tour}/departement/{dept}.json",
        "{base}/data/tour{tour}/{dept}.json",
        "{base}/api/resultats/{tour}/{dept}",
        # Format alternatif
        "{base}/{tour}/{dept}/communes.json",
    ]

    # Tester avec Paris (75)
    for base in BASE_URLS:
        for pattern in patterns:
            url = pattern.format(base=base, tour=tour, dept="075")
            data = fetch_json(url)
            if data:
                print(f"  API trouvée : {pattern}")
                return pattern, base

    # Tenter de trouver l'API en scrapant la page d'accueil
    for base in BASE_URLS:
        html = fetch_html(base)
        if html:
            # Chercher des URLs JSON dans le HTML/JS
            json_urls = re.findall(r'["\'](https?://[^"\']*\.json)["\']', html)
            api_urls = re.findall(r'["\'](https?://[^"\']*(?:resultats|communes|tour)[^"\']*)["\']', html)
            if json_urls or api_urls:
                print(f"  URLs trouvées dans {base}:")
                for u in (json_urls + api_urls)[:5]:
                    print(f"    {u}")
                # Essayer la première
                for u in json_urls:
                    data = fetch_json(u)
                    if data:
                        return u, base

    return None, None


def match_candidat(nom_api, candidats):
    """Match un nom de l'API avec nos candidats."""
    norm = normalize(nom_api)
    # Match exact
    for c in candidats:
        if normalize(c["nom"]) == norm:
            return c["id"]
    # Match nom de famille
    famille = norm.split()[-1] if norm else ""
    matches = [c["id"] for c in candidats if normalize(c["nom"]).split()[-1] == famille]
    if len(matches) == 1:
        return matches[0]
    return None


def process_commune_data(commune_data, tour_num, candidats):
    """Transforme les données API d'une commune en notre format résultats."""
    # Le format exact dépend de l'API — on gère plusieurs variantes

    # Variante 1 : format standard Ministère
    inscrits = commune_data.get("inscrits", commune_data.get("nbInscrits", 0))
    votants = commune_data.get("votants", commune_data.get("nbVotants", 0))
    blancs = commune_data.get("blancs", commune_data.get("nbBlancs", 0))
    nuls = commune_data.get("nuls", commune_data.get("nbNuls", 0))
    exprimes = commune_data.get("exprimes", commune_data.get("nbExprimes", 0))

    if not inscrits:
        return None

    if not exprimes:
        exprimes = votants - blancs - nuls

    abstentions = inscrits - votants
    taux = round(votants / inscrits * 100, 2) if inscrits > 0 else 0

    # Extraire les candidats
    resultats_candidats = []
    candidats_api = commune_data.get("candidats", commune_data.get("listes", []))

    for cand_api in candidats_api:
        nom = cand_api.get("nom", cand_api.get("nomTeteListe", ""))
        prenom = cand_api.get("prenom", cand_api.get("prenomTeteListe", ""))
        nom_complet = f"{prenom} {nom}".strip() if prenom else nom

        voix = cand_api.get("voix", cand_api.get("nbVoix", 0))
        pct = cand_api.get("pourcentage", cand_api.get("pctVoixExprimees", 0))
        if isinstance(pct, str):
            pct = float(pct.replace(",", "."))
        elu = cand_api.get("elu", False)

        cid = match_candidat(nom_complet, candidats)
        if not cid:
            # Essayer juste le nom de famille
            cid = match_candidat(nom, candidats)

        if cid:
            result = {
                "id": cid,
                "voix": voix,
                "pourcentage": round(pct, 2) if pct else round(voix / exprimes * 100, 2) if exprimes > 0 else 0,
                "elu": bool(elu),
            }
            if tour_num == 1:
                # Qualifié si > 10% des inscrits (règle municipales > 1000 hab)
                seuil = inscrits * 0.1
                result["qualifieT2"] = voix >= seuil
            resultats_candidats.append(result)

    if not resultats_candidats:
        return None

    resultats_candidats.sort(key=lambda x: x["voix"], reverse=True)

    # Au T1 : max 2 candidats qualifiés automatiquement si personne n'a > 50%
    if tour_num == 1:
        top = resultats_candidats[0]
        if top["pourcentage"] <= 50:
            # Assurer que les 2 premiers sont qualifiés minimum
            for i, rc in enumerate(resultats_candidats):
                if i < 2:
                    rc["qualifieT2"] = True

    return {
        "date": DATES[str(tour_num)],
        "inscrits": inscrits,
        "abstentions": abstentions,
        "tauxParticipation": taux,
        "votants": votants,
        "blancs": blancs,
        "nuls": nuls,
        "exprimes": exprimes,
        "candidats": resultats_candidats,
    }


def update_villes_json(villes):
    """Met à jour villes.json avec les résumés résultats."""
    updated = 0
    for v in villes:
        el_file = os.path.join(ELECTIONS_DIR, f"{v['id']}-2026.json")
        if not os.path.exists(el_file):
            continue
        el_data = load_json(el_file)
        res = el_data.get("resultats")
        if not res:
            continue

        summary = {
            "status": res.get("status", "provisoire"),
            "tour1": "tour1" in res,
            "tour2": "tour2" in res,
        }
        if res.get("eluMaire"):
            elu_id = res["eluMaire"]
            elu_nom = elu_id
            for c in el_data.get("candidats", []):
                if c["id"] == elu_id:
                    elu_nom = c["nom"]
                    break
            summary["eluMaire"] = {"id": elu_id, "nom": elu_nom}
        if res.get("tour1"):
            summary["tauxParticipationT1"] = res["tour1"]["tauxParticipation"]
        if res.get("tour2"):
            summary["tauxParticipationT2"] = res["tour2"]["tauxParticipation"]

        v["resultats"] = summary
        updated += 1

    save_json(VILLES_JSON, villes)
    return updated


def main():
    parser = argparse.ArgumentParser(description="Scrape résultats live Ministère de l'Intérieur")
    parser.add_argument("--tour", type=int, choices=[1, 2], required=True)
    parser.add_argument("--ville", type=str, help="Une seule ville (ID)")
    args = parser.parse_args()

    villes = load_json(VILLES_JSON)
    print(f"=== Scrape résultats live — Tour {args.tour} ===")
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Villes : {len(villes)}\n")

    # Découvrir l'API
    print("Recherche de l'API du Ministère...")
    api_pattern, api_base = discover_api_format(args.tour)

    if not api_pattern:
        print("\n❌ API du Ministère non trouvée ou pas encore en ligne.")
        print("Les résultats seront probablement disponibles à partir de 20h.")
        print("\nAlternatives :")
        print("  - Saisie manuelle : python scripts/saisie_resultats.py --tour " + str(args.tour))
        print("  - Vérifier : https://resultats-elections.interieur.gouv.fr/")
        return 1

    print(f"\n✅ API trouvée")

    # Grouper les villes par département
    dept_villes = {}
    for v in villes:
        if args.ville and v["id"] != args.ville:
            continue
        dept = v.get("departement", "").zfill(2)
        if dept not in dept_villes:
            dept_villes[dept] = []
        dept_villes[dept].append(v)

    imported = 0
    errors = 0

    for dept, dept_v in sorted(dept_villes.items()):
        # Fetch données département
        if "{dept}" in api_pattern:
            url = api_pattern.format(base=api_base, tour=args.tour, dept=dept.zfill(3))
        else:
            url = api_pattern
        dept_data = fetch_json(url)
        if not dept_data:
            continue

        # Chercher les communes dans les données
        communes = dept_data if isinstance(dept_data, list) else dept_data.get("communes", dept_data.get("resultats", []))
        if not isinstance(communes, list):
            communes = [dept_data]

        # Indexer par nom normalisé
        communes_map = {}
        for c in communes:
            nom = c.get("libelle", c.get("nomCommune", c.get("nom", "")))
            if nom:
                communes_map[normalize(nom)] = c

        for v in dept_v:
            ville_norm = normalize(v["nom"])
            commune_data = communes_map.get(ville_norm)
            if not commune_data:
                continue

            # Charger l'élection
            el_file = os.path.join(ELECTIONS_DIR, f"{v['id']}-2026.json")
            if not os.path.exists(el_file):
                continue
            el_data = load_json(el_file)
            candidats = el_data.get("candidats", [])

            # Transformer
            tour_data = process_commune_data(commune_data, args.tour, candidats)
            if not tour_data:
                continue

            n_matched = len(tour_data["candidats"])
            n_total = len(candidats)

            # Écrire
            resultats = el_data.get("resultats", {})
            resultats[f"tour{args.tour}"] = tour_data
            resultats["status"] = "provisoire"

            # Maire élu ?
            for rc in tour_data["candidats"]:
                if rc.get("elu"):
                    resultats["eluMaire"] = rc["id"]
                    break

            el_data["resultats"] = resultats
            save_json(el_file, el_data)

            print(f"  ✅ {v['nom']} — {n_matched}/{n_total} candidats, {tour_data['tauxParticipation']}%")
            imported += 1

    # Mettre à jour villes.json
    if imported > 0:
        villes = load_json(VILLES_JSON)
        updated = update_villes_json(villes)
        print(f"\nvilles.json : {updated} villes mises à jour")

        # Générer résultats nationaux
        from import_resultats import generate_resultats_nationaux
        try:
            generate_resultats_nationaux(villes)
        except Exception:
            print("  (résultats nationaux : skip)")

    print(f"\n=== Résumé ===")
    print(f"  Importés : {imported}")
    print(f"  Erreurs : {errors}")

    if imported > 0:
        return 0
    else:
        print("\nAucun résultat trouvé. Peut-être pas encore disponible.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
