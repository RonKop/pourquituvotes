#!/usr/bin/env python3
"""
Validation des données JSON — Comparateur Municipal
=====================================================
Vérifie la cohérence des données après chaque modification.
Exécuter : python scripts/valider_donnees.py (depuis la racine du projet)

Détecte :
- Candidats fantômes (IDs dans les propositions qui n'existent pas dans la liste des candidats)
- Candidats manquants (IDs de la liste absents d'un sous-thème)
- Doublons de sous-thèmes dans une même catégorie
- Nombre de propositions par candidat (alerte si programmeComplet=true avec <10 propositions)
- Grille universelle : 12 catégories identiques dans le même ordre pour chaque ville
- Sous-thèmes communs présents dans chaque ville
- Cohérence villes.json / elections/*.json
- Fichiers référencés (PDF, images) existent sur le disque
- IDs en kebab-case valide (a-z, 0-9, tirets)
"""

import json
import os
import re
import sys

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
VILLES_JSON = os.path.join(DATA_DIR, "villes.json")
SCHEMA_JSON = os.path.join(DATA_DIR, "schema", "schema_elections.json")
PROGRAMMES_DIR = os.path.join(DATA_DIR, "programmes")

KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def charger_schema():
    """Charge le schéma et retourne (categories_attendues, sous_themes_communs)."""
    with open(SCHEMA_JSON, "r", encoding="utf-8") as f:
        schema = json.load(f)
    categories_attendues = [cat["id"] for cat in schema["categories"]]
    sous_themes_communs = {}
    for cat in schema["categories"]:
        sous_themes_communs[cat["id"]] = [st["id"] for st in cat["sousThemes"]]
    return categories_attendues, sous_themes_communs


def charger_villes():
    """Charge villes.json."""
    with open(VILLES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def charger_election(election_id):
    """Charge un fichier election JSON."""
    path = os.path.join(ELECTIONS_DIR, f"{election_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def verifier_propositions(ville, election):
    """Vérifie que les IDs dans les propositions correspondent aux candidats."""
    erreurs = []
    avertissements = []
    candidats = {c["id"] for c in election["candidats"]}

    if not candidats:
        avertissements.append(f"  [{ville}] Aucun candidat trouvé")
        return erreurs, avertissements

    for cat in election.get("categories", []):
        for st in cat.get("sousThemes", []):
            st_id = st["id"]
            ids_dans_props = set(st.get("propositions", {}).keys())

            # Fantômes
            fantomes = ids_dans_props - candidats
            if fantomes:
                erreurs.append(
                    f"  [{ville}] sous-thème \"{st_id}\" : "
                    f"IDs FANTÔMES {sorted(fantomes)} "
                    f"(attendus: {sorted(candidats)})"
                )

            # Manquants
            manquants = candidats - ids_dans_props
            if manquants:
                avertissements.append(
                    f"  [{ville}] sous-thème \"{st_id}\" : "
                    f"candidats absents {sorted(manquants)}"
                )

    return erreurs, avertissements


def verifier_doublons_sous_themes(ville, election):
    """Vérifie qu'il n'y a pas de sous-thèmes en double."""
    erreurs = []
    for cat in election.get("categories", []):
        cat_id = cat["id"]
        st_ids = [st["id"] for st in cat.get("sousThemes", [])]
        vus = set()
        for st_id in st_ids:
            if st_id in vus:
                erreurs.append(f"  [{ville}] catégorie \"{cat_id}\" : sous-thème \"{st_id}\" EN DOUBLE")
            vus.add(st_id)
    return erreurs


def verifier_grille_universelle(ville, election, categories_attendues, sous_themes_communs):
    """Vérifie que la ville a les 12 catégories dans le même ordre."""
    erreurs = []
    avertissements = []

    categories_trouvees = [cat["id"] for cat in election.get("categories", [])]

    if len(categories_trouvees) != 12:
        erreurs.append(
            f"  [{ville}] {len(categories_trouvees)} catégories (attendu : 12)"
            f" -> {categories_trouvees}"
        )

    if categories_trouvees != categories_attendues:
        erreurs.append(
            f"  [{ville}] Ordre des catégories incorrect :"
            f"\n    Trouvé  : {categories_trouvees}"
            f"\n    Attendu : {categories_attendues}"
        )

    # Vérifier les sous-thèmes communs
    for cat in election.get("categories", []):
        cat_id = cat["id"]
        st_ids = [st["id"] for st in cat.get("sousThemes", [])]
        if cat_id in sous_themes_communs:
            for st_commun in sous_themes_communs[cat_id]:
                if st_commun not in st_ids:
                    avertissements.append(
                        f"  [{ville}] catégorie \"{cat_id}\" : sous-thème commun \"{st_commun}\" absent"
                    )

    return erreurs, avertissements


def compter_propositions(ville, election):
    """Compte les propositions non-null par candidat."""
    erreurs = []
    avertissements = []
    stats = {}

    candidats = {c["id"]: c for c in election["candidats"]}
    compteurs = {cid: 0 for cid in candidats}

    for cat in election.get("categories", []):
        for st in cat.get("sousThemes", []):
            for cid, prop in st.get("propositions", {}).items():
                if cid in compteurs and prop and prop.get("texte"):
                    compteurs[cid] += 1

    for cid in sorted(candidats):
        c = candidats[cid]
        n = compteurs[cid]
        pc = c.get("programmeComplet", False)
        stats[cid] = {"propositions": n, "complet": pc}

        if pc and n < 10:
            erreurs.append(
                f"  [{ville}] {cid} : programmeComplet=true mais seulement {n} propositions ! "
                f"(minimum attendu : ~15-20)"
            )
        elif not pc and n == 0:
            avertissements.append(f"  [{ville}] {cid} : 0 propositions (aucune mesure trouvée)")

    return stats, erreurs, avertissements


def verifier_coherence_villes(villes, elections):
    """Vérifie la cohérence entre villes.json et les fichiers élections."""
    erreurs = []
    for v in villes:
        for eid in v.get("elections", []):
            if eid not in elections:
                erreurs.append(f"  [{v['nom']}] élection \"{eid}\" référencée mais fichier manquant")
    return erreurs


def verifier_fichiers_references(ville, election):
    """Vérifie que les fichiers référencés (PDF, images) existent."""
    erreurs = []
    for c in election["candidats"]:
        pdf = c.get("programmePdfPath")
        if pdf:
            pdf_path = os.path.join(PROGRAMMES_DIR, pdf)
            if not os.path.exists(pdf_path):
                erreurs.append(
                    f"  [{ville}] {c['id']} : programmePdfPath \"{pdf}\" — fichier introuvable"
                )

        img = c.get("image_url")
        if img:
            img_path = os.path.join(ROOT_DIR, img)
            if not os.path.exists(img_path):
                erreurs.append(
                    f"  [{ville}] {c['id']} : image_url \"{img}\" — fichier introuvable"
                )
    return erreurs


def verifier_kebab_case(ville, election):
    """Vérifie que tous les IDs sont en kebab-case valide."""
    erreurs = []
    for c in election["candidats"]:
        if not KEBAB_RE.match(c["id"]):
            erreurs.append(
                f"  [{ville}] candidat ID \"{c['id']}\" n'est pas en kebab-case"
            )
    for cat in election.get("categories", []):
        if not KEBAB_RE.match(cat["id"]):
            erreurs.append(
                f"  [{ville}] catégorie ID \"{cat['id']}\" n'est pas en kebab-case"
            )
        for st in cat.get("sousThemes", []):
            if not KEBAB_RE.match(st["id"]):
                erreurs.append(
                    f"  [{ville}] sous-thème ID \"{st['id']}\" n'est pas en kebab-case"
                )
    return erreurs


def main():
    print("=" * 60)
    print("  VALIDATION DES DONNÉES — Comparateur Municipal")
    print("=" * 60)
    print()

    total_erreurs = 0
    total_avert = 0

    # 1. Charger les données
    print("1. Chargement des données JSON")
    if not os.path.exists(SCHEMA_JSON):
        print(f"  ERREUR : {SCHEMA_JSON} introuvable !")
        return 1
    categories_attendues, sous_themes_communs = charger_schema()

    if not os.path.exists(VILLES_JSON):
        print(f"  ERREUR : {VILLES_JSON} introuvable !")
        return 1

    villes = charger_villes()
    elections = {}
    for v in villes:
        for eid in v.get("elections", []):
            election = charger_election(eid)
            if election:
                elections[eid] = election
    print(f"  {len(villes)} villes, {len(elections)} élections chargées")
    print()

    # 2. Cohérence villes.json / fichiers
    print("2. Cohérence villes.json / fichiers élections")
    err_coh = verifier_coherence_villes(villes, elections)
    if err_coh:
        print(f"  ERREURS ({len(err_coh)}) :")
        for e in err_coh:
            print(e)
        total_erreurs += len(err_coh)
    else:
        print("  OK — Tous les fichiers élections existent")
    print()

    # 3. Élections détectées
    print("3. Élections détectées")
    for eid in sorted(elections.keys()):
        e = elections[eid]
        cands = sorted([c["id"] for c in e["candidats"]])
        print(f"  {e['ville']} ({eid}) : {len(cands)} candidats — {cands}")
    print()

    # 4. Cohérence des propositions
    print("4. Cohérence candidats / propositions")
    all_err_prop = []
    all_avert_prop = []
    for eid, election in sorted(elections.items()):
        err, avert = verifier_propositions(election["ville"], election)
        all_err_prop.extend(err)
        all_avert_prop.extend(avert)

    if all_err_prop:
        print(f"  ERREURS ({len(all_err_prop)}) :")
        for e in all_err_prop:
            print(e)
        total_erreurs += len(all_err_prop)
    else:
        print("  OK — Aucun candidat fantôme détecté")

    if all_avert_prop:
        print(f"\n  Avertissements ({len(all_avert_prop)}) — candidats absents de certains sous-thèmes :")
        for a in all_avert_prop:
            print(a)
        total_avert += len(all_avert_prop)
    print()

    # 5. Doublons
    print("5. Doublons de sous-thèmes")
    all_err_doub = []
    for eid, election in sorted(elections.items()):
        all_err_doub.extend(verifier_doublons_sous_themes(election["ville"], election))

    if all_err_doub:
        print(f"  ERREURS ({len(all_err_doub)}) :")
        for e in all_err_doub:
            print(e)
        total_erreurs += len(all_err_doub)
    else:
        print("  OK — Aucun doublon détecté")
    print()

    # 6. Grille universelle
    print("6. Grille universelle (12 catégories, même ordre)")
    all_err_grille = []
    all_avert_grille = []
    for eid, election in sorted(elections.items()):
        err, avert = verifier_grille_universelle(election["ville"], election, categories_attendues, sous_themes_communs)
        all_err_grille.extend(err)
        all_avert_grille.extend(avert)

    if all_err_grille:
        print(f"  ERREURS ({len(all_err_grille)}) :")
        for e in all_err_grille:
            print(e)
        total_erreurs += len(all_err_grille)
    else:
        print("  OK — 12 catégories dans le même ordre pour chaque ville")
    if all_avert_grille:
        print(f"\n  Avertissements ({len(all_avert_grille)}) :")
        for a in all_avert_grille:
            print(a)
        total_avert += len(all_avert_grille)
    print()

    # 7. Comptage des propositions
    print("7. Propositions par candidat")
    all_stats = {}
    all_err_count = []
    all_avert_count = []
    for eid, election in sorted(elections.items()):
        ville = election["ville"]
        stats, err, avert = compter_propositions(ville, election)
        all_stats[ville] = stats
        all_err_count.extend(err)
        all_avert_count.extend(avert)

    for ville in sorted(all_stats.keys()):
        print(f"  {ville}:")
        for cid in sorted(all_stats[ville].keys()):
            info = all_stats[ville][cid]
            flag = " [COMPLET]" if info["complet"] else ""
            print(f"    {cid}: {info['propositions']} propositions{flag}")

    if all_err_count:
        print(f"\n  ERREURS ({len(all_err_count)}) :")
        for e in all_err_count:
            print(e)
        total_erreurs += len(all_err_count)
    if all_avert_count:
        print(f"\n  Avertissements ({len(all_avert_count)}) :")
        for a in all_avert_count:
            print(a)
        total_avert += len(all_avert_count)
    print()

    # 8. Fichiers référencés
    print("8. Fichiers référencés (PDF, images)")
    all_err_fichiers = []
    for eid, election in sorted(elections.items()):
        all_err_fichiers.extend(verifier_fichiers_references(election["ville"], election))

    if all_err_fichiers:
        print(f"  ERREURS ({len(all_err_fichiers)}) :")
        for e in all_err_fichiers:
            print(e)
        total_erreurs += len(all_err_fichiers)
    else:
        print("  OK — Tous les fichiers référencés existent")
    print()

    # 9. Validation kebab-case des IDs
    print("9. Validation kebab-case des IDs")
    all_err_kebab = []
    for eid, election in sorted(elections.items()):
        all_err_kebab.extend(verifier_kebab_case(election["ville"], election))

    if all_err_kebab:
        print(f"  ERREURS ({len(all_err_kebab)}) :")
        for e in all_err_kebab:
            print(e)
        total_erreurs += len(all_err_kebab)
    else:
        print("  OK — Tous les IDs sont en kebab-case valide")
    print()

    # Résumé
    print("=" * 60)
    if total_erreurs == 0:
        print(f"  RÉSULTAT : TOUT EST OK")
        if total_avert:
            print(f"  ({total_avert} avertissements mineurs)")
    else:
        print(f"  RÉSULTAT : {total_erreurs} ERREUR(S) DÉTECTÉE(S)")
        if total_avert:
            print(f"  + {total_avert} avertissements")
    print("=" * 60)

    return 1 if total_erreurs > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
