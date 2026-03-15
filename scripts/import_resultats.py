#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import automatique des résultats électoraux depuis data.gouv.fr
================================================================
Télécharge le CSV résultats du Ministère de l'Intérieur et met à jour
les fichiers data/elections/{ville}-2026.json + villes.json.

Sources :
  - https://www.data.gouv.fr/fr/datasets/elections-municipales-2026-resultats/
  - https://resultats-elections.interieur.gouv.fr/

Usage :
  python scripts/import_resultats.py --tour 1 --csv resultats_T1.csv
  python scripts/import_resultats.py --tour 2 --csv resultats_T2.csv
  python scripts/import_resultats.py --tour 1 --csv resultats_T1.csv --ville paris --dry-run
"""

import sys
import io
import json
import os
import csv
import re
import argparse
import unicodedata
from datetime import datetime

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
VILLES_JSON = os.path.join(DATA_DIR, "villes.json")

DATES = {"1": "2026-03-15", "2": "2026-03-22"}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def normalize(text):
    """Normalise un texte pour comparaison (sans accents, lowercase, sans tirets)."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower().strip()
    text = re.sub(r"[-'\s]+", " ", text)
    text = re.sub(r"^(le |la |les |l )", "", text)
    return text


def match_candidat(nom_csv, candidats):
    """Tente de matcher un nom du CSV avec un candidat existant."""
    norm_csv = normalize(nom_csv)
    # Match exact sur nom normalisé
    for c in candidats:
        if normalize(c["nom"]) == norm_csv:
            return c["id"]
    # Match par nom de famille
    nom_famille_csv = norm_csv.split()[-1] if norm_csv else ""
    matches = []
    for c in candidats:
        nom_famille = normalize(c["nom"]).split()[-1]
        if nom_famille == nom_famille_csv:
            matches.append(c["id"])
    if len(matches) == 1:
        return matches[0]
    return None


def parse_csv_resultats(csv_path, encoding="utf-8"):
    """Parse le CSV résultats du Ministère.

    Le format exact peut varier, mais typiquement :
    - Colonnes communes : Code département, Libellé commune, Inscrits, Abstentions, Votants, Blancs, Nuls, Exprimés
    - Puis colonnes répétées par candidat : Nom, Prénom, Nuance, Voix, % Voix/Exp, Elu

    Retourne un dict : {(dept, commune_normalisee): {participation, candidats[]}}
    """
    resultats = {}

    # Essayer plusieurs encodings
    for enc in [encoding, "utf-8-sig", "latin-1", "cp1252"]:
        try:
            with open(csv_path, "r", encoding=enc) as f:
                reader = csv.reader(f, delimiter=";")
                headers = next(reader)
                # Normaliser les headers
                headers = [h.strip().lower() for h in headers]
                break
        except (UnicodeDecodeError, StopIteration):
            continue
    else:
        print(f"ERREUR : impossible de lire {csv_path} (encoding)")
        return {}

    # Identifier les colonnes
    col_map = {}
    for i, h in enumerate(headers):
        if "code" in h and ("dep" in h or "département" in h):
            col_map["dept"] = i
        elif "libellé" in h and "commune" in h:
            col_map["commune"] = i
        elif h in ("inscrits", "nb inscrits"):
            col_map["inscrits"] = i
        elif h in ("abstentions", "nb abstentions"):
            col_map["abstentions"] = i
        elif h in ("votants", "nb votants"):
            col_map["votants"] = i
        elif h in ("blancs", "nb blancs"):
            col_map["blancs"] = i
        elif h in ("nuls", "nb nuls"):
            col_map["nuls"] = i
        elif "exprimés" in h or "exprimes" in h:
            col_map["exprimes"] = i

    if "dept" not in col_map or "commune" not in col_map:
        print(f"ERREUR : colonnes département/commune introuvables dans le CSV")
        print(f"  Headers trouvés : {headers}")
        return {}

    # Identifier les blocs candidat (colonnes répétées)
    # Chercher les colonnes "nom", "prénom", "voix" qui se répètent
    cand_blocks = []
    i = 0
    while i < len(headers):
        if headers[i] in ("nom", "nom candidat"):
            block = {"nom": i}
            for j in range(i+1, min(i+10, len(headers))):
                h = headers[j]
                if "prénom" in h or "prenom" in h:
                    block["prenom"] = j
                elif h == "nuance" or "nuance" in h:
                    block["nuance"] = j
                elif h in ("voix", "nb voix"):
                    block["voix"] = j
                elif "% voix" in h or "% exp" in h:
                    block["pct"] = j
                elif h in ("elu", "élu", "elu(e)"):
                    block["elu"] = j
            if "voix" in block:
                cand_blocks.append(block)
                i = max(block.values()) + 1
                continue
        i += 1

    if not cand_blocks:
        print("ERREUR : impossible d'identifier les blocs candidat dans le CSV")
        return {}

    print(f"  CSV parsé : {len(col_map)} colonnes communes, {len(cand_blocks)} blocs candidat")

    # Parser les lignes
    with open(csv_path, "r", encoding=enc) as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # skip header
        for row in reader:
            if len(row) < max(col_map.values()) + 1:
                continue

            dept = row[col_map["dept"]].strip().zfill(2)
            commune = row[col_map["commune"]].strip()
            key = (dept, normalize(commune))

            if key not in resultats:
                resultats[key] = {
                    "inscrits": int(row[col_map.get("inscrits", 0)] or 0),
                    "votants": int(row[col_map.get("votants", 0)] or 0),
                    "blancs": int(row[col_map.get("blancs", 0)] or 0),
                    "nuls": int(row[col_map.get("nuls", 0)] or 0),
                    "exprimes": int(row[col_map.get("exprimes", 0)] or 0),
                    "candidats_csv": [],
                }

            # Extraire les candidats
            for block in cand_blocks:
                nom = row[block["nom"]].strip() if block["nom"] < len(row) else ""
                if not nom:
                    continue
                prenom = row[block.get("prenom", 0)].strip() if "prenom" in block and block["prenom"] < len(row) else ""
                voix_str = row[block["voix"]].strip() if block["voix"] < len(row) else "0"
                voix = int(voix_str) if voix_str else 0

                pct_str = row[block.get("pct", 0)].strip() if "pct" in block and block["pct"] < len(row) else ""
                pct = float(pct_str.replace(",", ".")) if pct_str else 0.0

                elu_str = row[block.get("elu", 0)].strip().lower() if "elu" in block and block["elu"] < len(row) else ""
                elu = elu_str in ("oui", "o", "true", "1", "élu", "elu")

                nuance = row[block.get("nuance", 0)].strip() if "nuance" in block and block["nuance"] < len(row) else ""

                nom_complet = f"{prenom} {nom}".strip() if prenom else nom

                resultats[key]["candidats_csv"].append({
                    "nom_complet": nom_complet,
                    "voix": voix,
                    "pourcentage": pct,
                    "elu": elu,
                    "nuance": nuance,
                })

    print(f"  {len(resultats)} communes parsées")
    return resultats


def build_ville_key_map(villes):
    """Construit un mapping (dept, commune_normalisee) -> ville_id."""
    mapping = {}
    for v in villes:
        dept = v.get("departement", "").zfill(2)
        nom_norm = normalize(v["nom"])
        mapping[(dept, nom_norm)] = v["id"]
    return mapping


def import_resultats_ville(ville_id, tour_num, csv_data, dry_run=False):
    """Importe les résultats d'une ville depuis les données CSV parsées."""
    el_file = os.path.join(ELECTIONS_DIR, f"{ville_id}-2026.json")
    if not os.path.exists(el_file):
        return None, f"Fichier élection introuvable : {el_file}"

    el_data = load_json(el_file)
    candidats = el_data.get("candidats", [])

    # Matcher les candidats CSV avec nos IDs
    resultats_candidats = []
    non_matches = []
    for csv_cand in csv_data["candidats_csv"]:
        cid = match_candidat(csv_cand["nom_complet"], candidats)
        if cid:
            result = {
                "id": cid,
                "voix": csv_cand["voix"],
                "pourcentage": csv_cand["pourcentage"],
                "elu": csv_cand["elu"],
            }
            if tour_num == 1:
                # Qualifié T2 si > 10% des inscrits ou dans les 2 premiers
                result["qualifieT2"] = True  # sera affiné manuellement si besoin
            resultats_candidats.append(result)
        else:
            non_matches.append(csv_cand["nom_complet"])

    if non_matches:
        print(f"    Non matchés : {non_matches}")

    # Trier par voix décroissant
    resultats_candidats.sort(key=lambda x: x["voix"], reverse=True)

    inscrits = csv_data["inscrits"]
    votants = csv_data["votants"]
    abstentions = inscrits - votants
    taux = round(votants / inscrits * 100, 2) if inscrits > 0 else 0

    tour_data = {
        "date": DATES[str(tour_num)],
        "inscrits": inscrits,
        "abstentions": abstentions,
        "tauxParticipation": taux,
        "votants": votants,
        "blancs": csv_data["blancs"],
        "nuls": csv_data["nuls"],
        "exprimes": csv_data["exprimes"],
        "candidats": resultats_candidats,
    }

    # Écrire
    if not dry_run:
        resultats = el_data.get("resultats", {})
        resultats[f"tour{tour_num}"] = tour_data
        resultats["status"] = "definitif"

        # Maire élu
        for rc in resultats_candidats:
            if rc.get("elu"):
                resultats["eluMaire"] = rc["id"]
                break

        el_data["resultats"] = resultats
        save_json(el_file, el_data)

    return tour_data, None


def update_villes_json_from_elections(villes, dry_run=False):
    """Met à jour les résumés résultats dans villes.json depuis les JSON élections."""
    updated = 0
    for v in villes:
        vid = v["id"]
        el_file = os.path.join(ELECTIONS_DIR, f"{vid}-2026.json")
        if not os.path.exists(el_file):
            continue
        el_data = load_json(el_file)
        resultats = el_data.get("resultats")
        if not resultats:
            continue

        res_summary = {
            "status": resultats.get("status", "provisoire"),
            "tour1": "tour1" in resultats,
            "tour2": "tour2" in resultats,
        }
        if resultats.get("eluMaire"):
            elu_id = resultats["eluMaire"]
            elu_nom = elu_id
            for c in el_data.get("candidats", []):
                if c["id"] == elu_id:
                    elu_nom = c["nom"]
                    break
            res_summary["eluMaire"] = {"id": elu_id, "nom": elu_nom}

        if resultats.get("tour1"):
            res_summary["tauxParticipationT1"] = resultats["tour1"]["tauxParticipation"]
        if resultats.get("tour2"):
            res_summary["tauxParticipationT2"] = resultats["tour2"]["tauxParticipation"]

        v["resultats"] = res_summary
        updated += 1

    if not dry_run:
        save_json(VILLES_JSON, villes)
    return updated


def generate_resultats_nationaux(villes, dry_run=False):
    """Génère data/resultats-nationaux.json avec les agrégats."""
    stats = {
        "derniereMaj": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "villesCouvertes": 0,
        "participationMoyenneT1": 0,
        "participationMoyenneT2": 0,
        "villesAvecT2": 0,
        "nuances": {},
        "elusParNuance": {},
    }

    taux_t1 = []
    taux_t2 = []

    for v in villes:
        res = v.get("resultats")
        if not res or not res.get("tour1"):
            continue
        stats["villesCouvertes"] += 1
        if res.get("tauxParticipationT1"):
            taux_t1.append(res["tauxParticipationT1"])
        if res.get("tauxParticipationT2"):
            taux_t2.append(res["tauxParticipationT2"])
            stats["villesAvecT2"] += 1

        # Nuance du maire élu
        if res.get("eluMaire"):
            elu_id = res["eluMaire"]["id"]
            el_file = os.path.join(ELECTIONS_DIR, f"{v['id']}-2026.json")
            if os.path.exists(el_file):
                el_data = load_json(el_file)
                for c in el_data.get("candidats", []):
                    if c["id"] == elu_id:
                        nuance = c.get("nuanceLibelle", c.get("nuanceOfficielle", "Autre"))
                        stats["elusParNuance"][nuance] = stats["elusParNuance"].get(nuance, 0) + 1
                        break

    stats["participationMoyenneT1"] = round(sum(taux_t1) / len(taux_t1), 2) if taux_t1 else 0
    stats["participationMoyenneT2"] = round(sum(taux_t2) / len(taux_t2), 2) if taux_t2 else 0

    if not dry_run:
        output_path = os.path.join(DATA_DIR, "resultats-nationaux.json")
        save_json(output_path, stats)
        print(f"  resultats-nationaux.json généré ({stats['villesCouvertes']} villes)")

    return stats


def bump_data_version():
    """Incrémente DATA_VERSION dans app.js et home.js."""
    new_version = datetime.now().strftime("%Y%m%d%H")
    for js_file in ["js/app.js", "js/home.js"]:
        path = os.path.join(ROOT_DIR, js_file)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r"(var DATA_VERSION\s*=\s*')[^']+(')",
            rf"\g<1>{new_version}\2",
            content,
            count=1,
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"  DATA_VERSION bumped to {new_version}")


def main():
    parser = argparse.ArgumentParser(description="Import résultats municipales depuis CSV data.gouv.fr")
    parser.add_argument("--tour", type=int, choices=[1, 2], required=True)
    parser.add_argument("--csv", type=str, required=True, help="Chemin vers le CSV résultats")
    parser.add_argument("--ville", type=str, help="Importer uniquement cette ville (ID)")
    parser.add_argument("--dry-run", action="store_true", help="Afficher sans écrire")
    parser.add_argument("--no-bump", action="store_true", help="Ne pas bumper DATA_VERSION")
    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print(f"ERREUR : fichier CSV introuvable : {args.csv}")
        return 1

    # Charger données
    villes = load_json(VILLES_JSON)
    ville_key_map = build_ville_key_map(villes)

    print(f"=== Import résultats Tour {args.tour} ===")
    print(f"CSV : {args.csv}")
    print(f"Mode : {'DRY-RUN' if args.dry_run else 'ÉCRITURE'}")
    print()

    # Parser le CSV
    csv_data = parse_csv_resultats(args.csv)
    if not csv_data:
        return 1

    # Importer
    imported = 0
    skipped = 0
    errors = 0

    for (dept, commune_norm), data in csv_data.items():
        ville_id = ville_key_map.get((dept, commune_norm))
        if not ville_id:
            continue  # Commune pas dans notre base

        if args.ville and ville_id != args.ville:
            continue

        print(f"  {ville_id} ({dept})...", end=" ")
        tour_data, err = import_resultats_ville(ville_id, args.tour, data, args.dry_run)
        if err:
            print(f"ERREUR : {err}")
            errors += 1
        elif tour_data:
            n_cands = len(tour_data["candidats"])
            print(f"OK ({n_cands} candidats, {tour_data['tauxParticipation']}%)")
            imported += 1
        else:
            print("skip")
            skipped += 1

    print(f"\n=== Résumé ===")
    print(f"  Importés : {imported}")
    print(f"  Skippés : {skipped}")
    print(f"  Erreurs : {errors}")

    if not args.dry_run and imported > 0:
        # Mettre à jour villes.json
        villes = load_json(VILLES_JSON)  # Recharger car modifié
        updated = update_villes_json_from_elections(villes)
        print(f"  villes.json : {updated} villes mises à jour")

        # Générer agrégats nationaux
        villes = load_json(VILLES_JSON)
        generate_resultats_nationaux(villes)

        # Bump version
        if not args.no_bump:
            bump_data_version()

    print(f"\nPensez à lancer :")
    print(f"  python scripts/valider_donnees.py")
    print(f"  python scripts/generate_static_shells.py")
    print(f"  python scripts/generate_sitemap.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
