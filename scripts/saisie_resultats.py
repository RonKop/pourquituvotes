#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Saisie manuelle des résultats électoraux — Municipales 2026
=============================================================
Pour le soir d'élection, avant la disponibilité des CSV officiels.
Écrit le bloc `resultats` dans les fichiers data/elections/{ville}-2026.json
et met à jour villes.json (résumé).

Usage :
  python scripts/saisie_resultats.py --tour 1 --ville paris
  python scripts/saisie_resultats.py --tour 2 --ville paris
  python scripts/saisie_resultats.py --tour 1  # mode interactif (choix ville)
"""

import sys
import io
import json
import os
import argparse
from datetime import datetime

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

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


def input_int(prompt, default=None):
    """Demande un entier, avec valeur par défaut optionnelle."""
    while True:
        suffix = f" [{default}]" if default is not None else ""
        val = input(f"{prompt}{suffix}: ").strip()
        if not val and default is not None:
            return default
        try:
            return int(val)
        except ValueError:
            print("  Veuillez entrer un nombre entier.")


def input_float(prompt):
    """Demande un flottant."""
    while True:
        val = input(f"{prompt}: ").strip()
        try:
            return float(val)
        except ValueError:
            print("  Veuillez entrer un nombre.")


def choisir_ville(villes):
    """Mode interactif : choisir une ville."""
    print("\nVilles disponibles :")
    for i, v in enumerate(villes):
        print(f"  {i+1:3d}. {v['nom']} ({v['id']})")
    while True:
        choix = input("\nNumero ou ID de la ville : ").strip()
        # Par numéro
        try:
            idx = int(choix) - 1
            if 0 <= idx < len(villes):
                return villes[idx]
        except ValueError:
            pass
        # Par ID
        for v in villes:
            if v["id"] == choix:
                return v
        print("  Ville non trouvée, réessayez.")


def saisir_resultats_tour(tour_num, candidats, resultats_existants=None):
    """Saisie interactive des résultats d'un tour."""
    tour_key = f"tour{tour_num}"
    print(f"\n{'='*60}")
    print(f"  SAISIE DU TOUR {tour_num}")
    print(f"{'='*60}")

    # Participation
    inscrits = input_int("Nombre d'inscrits")
    votants = input_int("Nombre de votants")
    blancs = input_int("Nombre de bulletins blancs", 0)
    nuls = input_int("Nombre de bulletins nuls", 0)
    exprimes = votants - blancs - nuls
    abstentions = inscrits - votants
    taux_participation = round(votants / inscrits * 100, 2) if inscrits > 0 else 0

    print(f"\n  Calculés : abstentions={abstentions}, exprimés={exprimes}, participation={taux_participation}%")

    # Résultats par candidat
    print(f"\n--- Voix par candidat ({len(candidats)} candidats) ---")
    resultats_candidats = []
    total_voix = 0

    for c in candidats:
        cid = c["id"]
        cnom = c["nom"]
        cliste = c.get("liste", "")

        # Pour le T2, ne demander que les candidats qualifiés
        if tour_num == 2 and resultats_existants:
            t1 = resultats_existants.get("tour1", {})
            t1_cands = {rc["id"]: rc for rc in t1.get("candidats", [])}
            if cid in t1_cands and not t1_cands[cid].get("qualifieT2", False):
                print(f"  {cnom} ({cliste}) — non qualifié au T1, skip")
                continue

        voix = input_int(f"  {cnom} ({cliste}) — voix")
        total_voix += voix

        pct = round(voix / exprimes * 100, 2) if exprimes > 0 else 0

        result_cand = {
            "id": cid,
            "voix": voix,
            "pourcentage": pct,
            "elu": False,
        }

        if tour_num == 1:
            qualifie = input(f"    Qualifié T2 ? (o/n) [o]: ").strip().lower()
            result_cand["qualifieT2"] = qualifie != "n"
        else:
            elu = input(f"    Élu ? (o/n) [n]: ").strip().lower()
            result_cand["elu"] = elu == "o"

            # Fusions de listes
            fusion = input(f"    Fusion avec d'autres listes ? (IDs séparés par virgule, vide si non): ").strip()
            if fusion:
                result_cand["fusionAvec"] = [x.strip() for x in fusion.split(",")]

        resultats_candidats.append(result_cand)

    # Vérification somme
    if total_voix != exprimes:
        print(f"\n  ATTENTION : somme des voix ({total_voix}) != exprimés ({exprimes})")
        print(f"  Différence : {total_voix - exprimes}")
        corriger = input("  Continuer quand même ? (o/n) [o]: ").strip().lower()
        if corriger == "n":
            return None

    # Trier par voix décroissant
    resultats_candidats.sort(key=lambda x: x["voix"], reverse=True)

    tour_data = {
        "date": DATES[str(tour_num)],
        "inscrits": inscrits,
        "abstentions": abstentions,
        "tauxParticipation": taux_participation,
        "votants": votants,
        "blancs": blancs,
        "nuls": nuls,
        "exprimes": exprimes,
        "candidats": resultats_candidats,
    }

    # Fusions de listes (T2)
    if tour_num == 2:
        fusions = []
        for rc in resultats_candidats:
            if rc.get("fusionAvec"):
                nom_fusion = input(f"  Nom de la fusion pour {rc['id']} + {rc['fusionAvec']} : ").strip()
                fusions.append({
                    "listePrincipale": rc["id"],
                    "listesFusionnees": rc["fusionAvec"],
                    "nomFusion": nom_fusion or f"Alliance {rc['id']}",
                })
        if fusions:
            tour_data["fusionsListes"] = fusions

    return tour_data


def update_villes_json(villes, ville_id, resultats):
    """Met à jour le résumé résultats dans villes.json."""
    for v in villes:
        if v["id"] == ville_id:
            res_summary = {
                "status": resultats.get("status", "provisoire"),
                "tour1": "tour1" in resultats,
                "tour2": "tour2" in resultats,
            }
            if resultats.get("eluMaire"):
                # Trouver le nom du maire élu
                elu_id = resultats["eluMaire"]
                elu_nom = elu_id
                el_file = os.path.join(ELECTIONS_DIR, f"{ville_id}-2026.json")
                if os.path.exists(el_file):
                    el_data = load_json(el_file)
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
            break


def bump_data_version():
    """Incrémente DATA_VERSION dans app.js et home.js."""
    new_version = datetime.now().strftime("%Y%m%d%H")
    for js_file in ["js/app.js", "js/home.js"]:
        path = os.path.join(ROOT_DIR, js_file)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Remplacer DATA_VERSION = 'XXXX' par la nouvelle
        import re
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
    parser = argparse.ArgumentParser(description="Saisie manuelle des résultats municipales 2026")
    parser.add_argument("--tour", type=int, choices=[1, 2], required=True, help="Numéro du tour (1 ou 2)")
    parser.add_argument("--ville", type=str, help="ID de la ville (kebab-case)")
    parser.add_argument("--no-bump", action="store_true", help="Ne pas bumper DATA_VERSION")
    args = parser.parse_args()

    # Charger villes
    villes = load_json(VILLES_JSON)

    # Choisir la ville
    if args.ville:
        ville_entry = None
        for v in villes:
            if v["id"] == args.ville:
                ville_entry = v
                break
        if not ville_entry:
            print(f"Ville '{args.ville}' introuvable dans villes.json")
            return 1
    else:
        ville_entry = choisir_ville(villes)

    vid = ville_entry["id"]
    vnom = ville_entry["nom"]
    print(f"\n{'='*60}")
    print(f"  RÉSULTATS — {vnom} — Tour {args.tour}")
    print(f"{'='*60}")

    # Charger l'élection
    el_file = os.path.join(ELECTIONS_DIR, f"{vid}-2026.json")
    if not os.path.exists(el_file):
        print(f"Fichier élection introuvable : {el_file}")
        return 1

    el_data = load_json(el_file)
    candidats = el_data.get("candidats", [])

    if not candidats:
        print("Aucun candidat dans ce fichier élection !")
        return 1

    # Résultats existants
    resultats = el_data.get("resultats", {})

    # Vérifications
    if args.tour == 2 and "tour1" not in resultats:
        print("ERREUR : pas de résultats du tour 1 ! Saisissez d'abord le T1.")
        return 1

    if f"tour{args.tour}" in resultats:
        print(f"\nDes résultats du tour {args.tour} existent déjà !")
        ecraser = input("Écraser ? (o/n) [n]: ").strip().lower()
        if ecraser != "o":
            print("Abandon.")
            return 0

    # Saisie
    tour_data = saisir_resultats_tour(args.tour, candidats, resultats)
    if tour_data is None:
        print("Abandon.")
        return 1

    # Écrire dans le JSON
    resultats[f"tour{args.tour}"] = tour_data
    resultats["status"] = "provisoire"

    # Maire élu ?
    if args.tour == 2:
        for rc in tour_data["candidats"]:
            if rc.get("elu"):
                resultats["eluMaire"] = rc["id"]
                print(f"\n  Maire élu : {rc['id']}")
                break
    elif args.tour == 1:
        # Vérifier si un candidat a > 50% au T1 (élu dès le T1, communes <1000)
        for rc in tour_data["candidats"]:
            if rc["pourcentage"] > 50:
                elu_t1 = input(f"\n  {rc['id']} a {rc['pourcentage']}% — Élu dès le T1 ? (o/n) [n]: ").strip().lower()
                if elu_t1 == "o":
                    rc["elu"] = True
                    resultats["eluMaire"] = rc["id"]
                    print(f"  Maire élu dès le T1 : {rc['id']}")
                break

    el_data["resultats"] = resultats
    save_json(el_file, el_data)
    print(f"\n  {el_file} mis à jour")

    # Mettre à jour villes.json
    update_villes_json(villes, vid, resultats)
    save_json(VILLES_JSON, villes)
    print(f"  {VILLES_JSON} mis à jour")

    # Bump DATA_VERSION
    if not args.no_bump:
        bump_data_version()

    # Résumé
    print(f"\n{'='*60}")
    print(f"  RÉSULTAT SAISI — {vnom} — Tour {args.tour}")
    print(f"{'='*60}")
    print(f"  Status : provisoire")
    print(f"  Inscrits : {tour_data['inscrits']}")
    print(f"  Votants : {tour_data['votants']} ({tour_data['tauxParticipation']}%)")
    print(f"  Exprimés : {tour_data['exprimes']}")
    print(f"\n  Classement :")
    for i, rc in enumerate(tour_data["candidats"]):
        elu_flag = " [ELU]" if rc.get("elu") else ""
        q_flag = " [Q-T2]" if rc.get("qualifieT2") else ""
        print(f"    {i+1}. {rc['id']} — {rc['voix']} voix ({rc['pourcentage']}%){elu_flag}{q_flag}")

    print(f"\nPensez à lancer :")
    print(f"  python scripts/valider_donnees.py")
    print(f"  python scripts/generate_static_shells.py")
    print(f"  python scripts/generate_sitemap.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
