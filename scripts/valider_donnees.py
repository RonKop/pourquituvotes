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
"""

import json
import os
import sys

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
VILLES_JSON = os.path.join(DATA_DIR, "villes.json")

# Grille universelle attendue (ordre fixe)
CATEGORIES_ATTENDUES = [
    "securite", "transports", "logement", "education", "environnement",
    "sante", "democratie", "economie", "culture", "sport", "urbanisme", "solidarite"
]

SOUS_THEMES_COMMUNS = {
    "securite": ["police-municipale", "videoprotection", "prevention-mediation", "violences-femmes"],
    "transports": ["transports-en-commun", "velo-mobilites-douces", "pietons-circulation", "stationnement", "tarifs-gratuite"],
    "logement": ["logement-social", "logements-vacants", "encadrement-loyers", "acces-logement"],
    "education": ["petite-enfance", "ecoles-renovation", "cantines-fournitures", "periscolaire-loisirs", "jeunesse"],
    "environnement": ["espaces-verts", "proprete-dechets", "climat-adaptation", "renovation-energetique", "alimentation-durable"],
    "sante": ["centres-sante", "prevention-sante", "seniors"],
    "democratie": ["budget-participatif", "transparence", "vie-associative", "services-publics"],
    "economie": ["commerce-local", "emploi-insertion", "attractivite"],
    "culture": ["equipements-culturels", "evenements-creation"],
    "sport": ["equipements-sportifs", "sport-pour-tous"],
    "urbanisme": ["amenagement-urbain", "accessibilite", "quartiers-prioritaires"],
    "solidarite": ["aide-sociale", "egalite-discriminations", "pouvoir-achat"],
}


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


def verifier_grille_universelle(ville, election):
    """Vérifie que la ville a les 12 catégories dans le même ordre."""
    erreurs = []
    avertissements = []

    categories_trouvees = [cat["id"] for cat in election.get("categories", [])]

    if len(categories_trouvees) != 12:
        erreurs.append(
            f"  [{ville}] {len(categories_trouvees)} catégories (attendu : 12)"
            f" -> {categories_trouvees}"
        )

    if categories_trouvees != CATEGORIES_ATTENDUES:
        erreurs.append(
            f"  [{ville}] Ordre des catégories incorrect :"
            f"\n    Trouvé  : {categories_trouvees}"
            f"\n    Attendu : {CATEGORIES_ATTENDUES}"
        )

    # Vérifier les sous-thèmes communs
    for cat in election.get("categories", []):
        cat_id = cat["id"]
        st_ids = [st["id"] for st in cat.get("sousThemes", [])]
        if cat_id in SOUS_THEMES_COMMUNS:
            for st_commun in SOUS_THEMES_COMMUNS[cat_id]:
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


def main():
    print("=" * 60)
    print("  VALIDATION DES DONNÉES — Comparateur Municipal")
    print("=" * 60)
    print()

    total_erreurs = 0
    total_avert = 0

    # 1. Charger les données
    print("1. Chargement des données JSON")
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
        err, avert = verifier_grille_universelle(election["ville"], election)
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
