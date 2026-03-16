#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrape les résultats T1/T2 depuis resultats-elections.interieur.gouv.fr
Format URL : /municipales2026/ensemble_geographique/{region}/{dept}/{code_commune}/index.html

Usage :
  python scripts/scrape_interieur_html.py --tour 1
  python scripts/scrape_interieur_html.py --tour 1 --ville paris
  python scripts/scrape_interieur_html.py --tour 1 --dry-run
"""

import sys
import io
import json
import os
import re
import argparse
import unicodedata
import time
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

BASE_URL = "https://www.resultats-elections.interieur.gouv.fr/municipales2026/ensemble_geographique"

# Mapping département → code région (INSEE)
# Source: https://www.insee.fr/fr/information/2560452
DEPT_TO_REGION = {
    "01": "84", "02": "32", "03": "84", "04": "93", "05": "93", "06": "93",
    "07": "84", "08": "44", "09": "76", "10": "44", "11": "76", "12": "76",
    "13": "93", "14": "28", "15": "84", "16": "75", "17": "75", "18": "24",
    "19": "75", "21": "27", "22": "53", "23": "75", "24": "75", "25": "27",
    "26": "84", "27": "28", "28": "24", "29": "53", "2A": "94", "2B": "94",
    "30": "76", "31": "76", "32": "76", "33": "75", "34": "76", "35": "53",
    "36": "24", "37": "24", "38": "84", "39": "27", "40": "75", "41": "24",
    "42": "84", "43": "84", "44": "52", "45": "24", "46": "76", "47": "75",
    "48": "76", "49": "52", "50": "28", "51": "44", "52": "44", "53": "52",
    "54": "44", "55": "44", "56": "53", "57": "44", "58": "27", "59": "32",
    "60": "32", "61": "28", "62": "32", "63": "84", "64": "75", "65": "76",
    "66": "76", "67": "44", "68": "44", "69": "84", "70": "27", "71": "27",
    "72": "52", "73": "84", "74": "84", "75": "11", "76": "28", "77": "11",
    "78": "11", "79": "75", "80": "32", "81": "76", "82": "76", "83": "93",
    "84": "93", "85": "52", "86": "75", "87": "75", "88": "44", "89": "27",
    "90": "27", "91": "11", "92": "11", "93": "11", "94": "11", "95": "11",
    "971": "01", "972": "02", "973": "03", "974": "04", "976": "06",
}

# Mapping code_postal → code_commune INSEE (pour les villes de notre base)
# On le construit dynamiquement depuis villes.json


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
    return text


def fetch_html(url):
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'PQTV-Bot/1.0 (pourquituvotes.fr)')
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except Exception:
        return None


def parse_number(text):
    """Parse un nombre depuis du texte HTML (gère les espaces insécables, %, etc.)."""
    text = text.replace('\xa0', '').replace(' ', '').replace('\u202f', '')
    text = text.replace(',', '.').replace('%', '').strip()
    try:
        if '.' in text:
            return float(text)
        return int(text)
    except ValueError:
        return 0


def match_candidat(nom_html, candidats):
    """Match un nom trouvé dans le HTML avec nos candidats."""
    norm = normalize(nom_html)
    # Match exact
    for c in candidats:
        if normalize(c["nom"]) == norm:
            return c["id"]
    # Match nom de famille (dernier mot)
    famille = norm.split()[-1] if norm else ""
    matches = [c["id"] for c in candidats if normalize(c["nom"]).split()[-1] == famille]
    if len(matches) == 1:
        return matches[0]
    # Match partiel (nom de famille dans le nom complet)
    for c in candidats:
        c_norm = normalize(c["nom"])
        if famille and famille in c_norm:
            return c["id"]
    return None


def parse_resultats_html(html, tour_num, candidats):
    """Parse le HTML de la page résultats du Ministère.

    Format HTML du Ministère (2026) :
    - Table 1 "Résultats" : <tr> avec <td>liste</td><td>M./Mme NOM</td><td>nuance</td><td>voix</td><td>%ins</td><td>%exp</td>
    - Table 2 "Mentions" : <tr> avec <td>label</td><td>nombre</td><td>%ins</td><td>%vot</td>
    """
    if not html:
        return None

    def clean(text):
        return re.sub(r'<[^>]+>', '', text).strip()

    # === Parse table "Mentions" (participation) ===
    mentions = {}
    mentions_match = re.search(r'<caption>\s*Mentions.*?</caption>(.*?)</table>', html, re.DOTALL)
    if mentions_match:
        rows = re.findall(r'<tr>(.*?)</tr>', mentions_match.group(1), re.DOTALL)
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 2:
                label = clean(cells[0]).lower()
                val = parse_number(clean(cells[1]))
                if 'inscrit' in label:
                    mentions['inscrits'] = val
                elif 'abstention' in label:
                    mentions['abstentions'] = val
                elif 'votant' in label:
                    mentions['votants'] = val
                elif 'blanc' in label:
                    mentions['blancs'] = val
                elif 'nul' in label:
                    mentions['nuls'] = val
                elif 'exprim' in label:
                    mentions['exprimes'] = val

    inscrits = mentions.get('inscrits', 0)
    votants = mentions.get('votants', 0)
    blancs = mentions.get('blancs', 0)
    nuls = mentions.get('nuls', 0)
    exprimes = mentions.get('exprimes', 0)

    if not inscrits or not votants:
        return None
    if not exprimes:
        exprimes = votants - blancs - nuls

    abstentions = inscrits - votants
    taux = round(votants / inscrits * 100, 2)

    # === Parse table "Résultats" (candidats) ===
    resultats_candidats = []
    resultats_match = re.search(r'<caption>\s*R.sultats.*?</caption>(.*?)</table>', html, re.DOTALL)
    if resultats_match:
        rows = re.findall(r'<tr>(.*?)</tr>', resultats_match.group(1), re.DOTALL)
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            # Format: liste, conduit par, nuance, voix, %inscrits, %exprimés [, sièges...]
            if len(cells) >= 6:
                conduit_par = clean(cells[1])
                # Enlever M./Mme
                conduit_par = re.sub(r'^(?:M\.|Mme|M)\s+', '', conduit_par).strip()
                voix = parse_number(clean(cells[3]))
                pct_exprimes = parse_number(clean(cells[5]))

                if voix <= 0:
                    continue

                cid = match_candidat(conduit_par, candidats)
                if cid:
                    resultats_candidats.append({
                        "id": cid,
                        "voix": voix,
                        "pourcentage": round(pct_exprimes, 2),
                        "elu": False,
                    })

    if not resultats_candidats:
        return None

    # Dédupliquer et trier
    seen = set()
    unique = []
    for rc in resultats_candidats:
        if rc["id"] not in seen:
            seen.add(rc["id"])
            unique.append(rc)
    resultats_candidats = unique
    resultats_candidats.sort(key=lambda x: x["voix"], reverse=True)

    # Qualifié T2 (T1 uniquement)
    if tour_num == 1:
        for i, rc in enumerate(resultats_candidats):
            seuil = inscrits * 0.1 if inscrits else 0
            rc["qualifieT2"] = (rc["voix"] >= seuil) or (i < 2)
            if rc["pourcentage"] > 50:
                rc["elu"] = True

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


def get_code_commune(ville):
    """Retourne le code commune INSEE à partir des données ville."""
    # Le code commune INSEE = département + code spécifique
    # Pour les villes de notre base, on le déduit du code postal
    cp = ville.get("codePostal", "")
    dept = ville.get("departement", "")

    # Cas spéciaux
    nom = ville.get("nom", "")
    ville_id = ville.get("id", "")

    # Paris, Lyon, Marseille ont des codes spéciaux
    if ville_id == "paris" or "Paris" in nom:
        return "75056"
    if ville_id == "lyon" or nom == "Lyon":
        return "69123"
    if ville_id == "marseille" or nom == "Marseille":
        return "13055"

    # Code INSEE = département (2 chars) + 3 chiffres du code postal
    if cp and len(cp) >= 5:
        # Le code commune est souvent le code postal lui-même pour les grandes villes
        # Mais il peut différer. On essaie d'abord avec le CP
        return cp[:5].replace(dept, dept.zfill(2), 1) if len(dept) < 2 else cp[:5]

    return None


def load_insee_mapping():
    """Charge le mapping ville_id → code INSEE depuis mapping_insee.json."""
    path = os.path.join(DATA_DIR, "mapping_insee.json")
    if os.path.exists(path):
        return load_json(path)
    return {}

INSEE_MAP = {}

def build_url(ville, tour_num=1):
    """Construit l'URL de la page résultats pour une ville."""
    global INSEE_MAP
    if not INSEE_MAP:
        INSEE_MAP = load_insee_mapping()

    vid = ville.get("id", "")
    info = INSEE_MAP.get(vid)
    if info:
        region = info["region"]
        dept = info["departement"]
        code = info["code_commune"]
        return f"{BASE_URL}/{region}/{dept}/{code}/index.html"

    # Fallback ancien code
    dept = ville.get("departement", "").zfill(2)
    region = DEPT_TO_REGION.get(dept, "")
    code_commune = get_code_commune(ville)

    if not region or not code_commune:
        return None

    return f"{BASE_URL}/{region}/{dept}/{code_commune}/index.html"


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
    parser = argparse.ArgumentParser(description="Scrape résultats depuis resultats-elections.interieur.gouv.fr")
    parser.add_argument("--tour", type=int, choices=[1, 2], required=True)
    parser.add_argument("--ville", type=str, help="Une seule ville (ID)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delay", type=float, default=0.5, help="Délai entre requêtes (secondes)")
    args = parser.parse_args()

    villes = load_json(VILLES_JSON)
    print(f"=== Scrape résultats Ministère — Tour {args.tour} ===")
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Villes : {len(villes)}\n")

    imported = 0
    skipped = 0
    errors = 0

    for v in villes:
        if args.ville and v["id"] != args.ville:
            continue

        url = build_url(v, args.tour)
        if not url:
            print(f"  {v['nom']} — URL non constructible (dept={v.get('departement')})")
            skipped += 1
            continue

        print(f"  {v['nom']}...", end=" ", flush=True)

        html = fetch_html(url)
        if not html:
            print("404/erreur")
            skipped += 1
            time.sleep(args.delay)
            continue

        # Charger les candidats
        el_file = os.path.join(ELECTIONS_DIR, f"{v['id']}-2026.json")
        if not os.path.exists(el_file):
            print("pas de fichier élection")
            skipped += 1
            continue

        el_data = load_json(el_file)
        candidats = el_data.get("candidats", [])

        tour_data = parse_resultats_html(html, args.tour, candidats)
        if not tour_data:
            print("parsing échoué")
            errors += 1
            time.sleep(args.delay)
            continue

        n_matched = len(tour_data["candidats"])
        n_total = len(candidats)

        if not args.dry_run:
            resultats = el_data.get("resultats", {})
            resultats[f"tour{args.tour}"] = tour_data
            resultats["status"] = "provisoire"

            for rc in tour_data["candidats"]:
                if rc.get("elu"):
                    resultats["eluMaire"] = rc["id"]
                    break

            el_data["resultats"] = resultats
            save_json(el_file, el_data)

        print(f"OK — {n_matched}/{n_total} candidats, {tour_data['tauxParticipation']}%")
        imported += 1
        time.sleep(args.delay)

    print(f"\n=== Résumé ===")
    print(f"  Importés : {imported}")
    print(f"  Skippés : {skipped}")
    print(f"  Erreurs parsing : {errors}")

    if not args.dry_run and imported > 0:
        villes = load_json(VILLES_JSON)
        updated = update_villes_json(villes)
        print(f"  villes.json : {updated} villes mises à jour")

    return 0 if imported > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
