#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit de complétude des candidats programmeComplet: true
=========================================================
Détecte les problèmes systémiques : bilan, blocs monolithiques,
doublons, misclassifications, sources manquantes, extraction partielle.

Usage :
  python scripts/auditer_completude.py                        # Tous les complets
  python scripts/auditer_completude.py --ville paris          # Filtrer par ville
  python scripts/auditer_completude.py --candidat gregoire    # Filtrer par candidat
  python scripts/auditer_completude.py --csv rapport.csv      # Export CSV
"""

import argparse
import csv
import io
import json
import os
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher

# Force UTF-8 pour Windows (cp1252 fix)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Chemins (pattern de valider_donnees.py)
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
SCHEMA_JSON = os.path.join(DATA_DIR, "schema", "schema_elections.json")
SUIVI_CSV = os.path.join(DATA_DIR, "suivi_candidats.csv")

# Seuils
MONOLITHIC_THRESHOLD = 250  # relevé de 200 : beaucoup de mesures détaillées font 200-250 chars
SIMILARITY_THRESHOLD = 0.85  # même seuil que detecter_doublons.py
MIN_MESURES_COMPLET = 20

# Regex de détection du bilan (marqueurs temporels)
BILAN_PATTERNS = [
    re.compile(r"depuis 20\d{2}", re.IGNORECASE),
    re.compile(r"d[ée]j[aà] en place", re.IGNORECASE),
    re.compile(r"record de", re.IGNORECASE),
    re.compile(r"fin 20\d{2}", re.IGNORECASE),
    re.compile(r"actuellement", re.IGNORECASE),
    re.compile(r"contre \d+ actuellement", re.IGNORECASE),
    re.compile(r"\d+ d[ée]j[àa] install[ée]e?s", re.IGNORECASE),
    re.compile(r"augmentation.*depuis", re.IGNORECASE),
]

# Contre-patterns : si présent, la mesure est forward-looking (pas du bilan)
BILAN_FORWARD_PATTERNS = re.compile(
    r"objectif|ambition|viser|voulons|nous proposons|il faut|créer|"
    r"mettre en place|lancer|développer|instaurer|renforcer|déployer|"
    r"étendre|extension|poursuivre|candidature|expérimenter|"
    r"augmenter|élargir|porter à|passer à|atteindre|proposer|"
    r"prévoir|engager|réactiver|rétablir|restaurer|refonder|"
    r"comme à .+ depuis",  # "comme à Paris depuis 2024" = référence, pas bilan
    re.IGNORECASE,
)

# "Doublement/Triplement" en début de mesure = proposition de doubler/tripler
# "passage de X à Y" = objectif chiffré forward-looking
BILAN_PROPOSAL_PATTERNS = [
    re.compile(r"^(doublement|triplement)\b", re.IGNORECASE),
    re.compile(r"^passage de .+ [àa] .+", re.IGNORECASE),
]

# Mots-clés par sous-thème pour vérification de cohérence
# Chaque entrée : sous-thème → ensemble de mots-clés attendus
MOTS_CLES_PAR_ST = {
    "police-municipale": {"police", "policier", "agent", "effectif", "patrouille", "brigade", "municipale", "sécurité"},
    "videoprotection": {"caméra", "vidéo", "vidéoprotection", "vidéosurveillance", "surveillance"},
    "prevention-mediation": {"médiation", "médiateur", "prévention", "éclairage", "alerte", "sécurité routière"},
    "violences-femmes": {"femme", "harcèlement", "violence", "conjugale", "sexiste", "sexuel"},
    "transports-en-commun": {"bus", "métro", "tramway", "transport", "ligne", "gare", "navigo", "ratp"},
    "velo-mobilites-douces": {"vélo", "cyclable", "piste", "vélib", "trottinette", "mobilité douce"},
    "pietons-circulation": {"piéton", "trottoir", "passage", "traversée", "circulation", "zone 30", "apaisée"},
    "stationnement": {"stationnement", "parking", "livraison", "garer", "place"},
    "tarifs-gratuite": {"gratuit", "tarif", "navigo", "gratuité", "prix"},
    "logement-social": {"logement social", "hlm", "bailleur", "construction", "parc social"},
    "logements-vacants": {"vacant", "vide", "inoccupé", "réquisition", "taxation"},
    "encadrement-loyers": {"loyer", "airbnb", "encadrement", "location", "meublé"},
    "acces-logement": {"hébergement", "sans-abri", "sdf", "urgence", "accès logement", "garantie"},
    "petite-enfance": {"crèche", "petite enfance", "nourrice", "assistante maternelle", "berceau"},
    "ecoles-renovation": {"école", "rénovation", "classe", "scolaire", "collège", "lycée"},
    "cantines-fournitures": {"cantine", "fourniture", "repas", "restauration scolaire", "tarif"},
    "periscolaire-loisirs": {"périscolaire", "loisir", "vacances", "animation", "centre aéré", "colonie"},
    "jeunesse": {"jeune", "étudiant", "jeunesse", "campus", "résidence étudiante", "tutorat"},
    "espaces-verts": {"parc", "jardin", "arbre", "végétal", "vert", "nature", "biodiversité"},
    "proprete-dechets": {"propret", "déchet", "poubelle", "tri", "compost", "recyclage", "collecte"},
    "climat-adaptation": {"climat", "chaleur", "canicule", "adaptation", "température", "îlot de chaleur"},
    "renovation-energetique": {"rénovation énergétique", "isolation", "énergie", "thermique", "chauffage"},
    "alimentation-durable": {"bio", "alimentation", "circuit court", "agriculture", "durable"},
    "centres-sante": {"centre de santé", "médecin", "hôpital", "dispensaire", "soin", "consultation"},
    "prevention-sante": {"prévention", "santé mentale", "dépistage", "vih", "vaccination", "addiction"},
    "seniors": {"senior", "âgé", "ehpad", "retraité", "vieillissement", "aide à domicile", "aidant"},
    "budget-participatif": {"budget participatif", "consultation", "citoyen", "participation"},
    "transparence": {"transparence", "donnée ouverte", "open data", "éthique", "audit"},
    "vie-associative": {"association", "bénévole", "subvention", "vie associative"},
    "services-publics": {"service public", "guichet", "numérique", "administration", "accueil", "mairie"},
    "commerce-local": {"commerce", "commerçant", "artisan", "boutique", "marché", "foncier commercial"},
    "emploi-insertion": {"emploi", "insertion", "chômage", "formation", "apprentissage"},
    "attractivite": {"tourisme", "attractivité", "international", "économique", "entreprise", "innovation"},
    "equipements-culturels": {"musée", "bibliothèque", "théâtre", "conservatoire", "culture", "cinéma"},
    "evenements-creation": {"festival", "événement", "spectacle", "artiste", "création", "carnaval"},
    "equipements-sportifs": {"stade", "piscine", "gymnase", "terrain", "sportif", "équipement"},
    "sport-pour-tous": {"sport", "handisport", "pratique sportive", "club", "olympique"},
    "amenagement-urbain": {"place", "boulevard", "aménagement", "urbanisme", "espace public", "quartier"},
    "accessibilite": {"accessibilité", "handicap", "pmr", "rampe", "ascenseur", "mdph"},
    "quartiers-prioritaires": {"qpv", "quartier prioritaire", "politique de la ville", "banlieue"},
    "aide-sociale": {"rsa", "aide sociale", "solidarité", "minima sociaux", "précarité", "pauvreté"},
    "egalite-discriminations": {"égalité", "discrimination", "diversité", "inclusion", "lgbtq", "racisme"},
    "pouvoir-achat": {"pouvoir d'achat", "prix", "coût de la vie", "tarif social"},
}


def charger_schema():
    """Charge le schéma et retourne les sous-thèmes communs."""
    with open(SCHEMA_JSON, "r", encoding="utf-8") as f:
        schema = json.load(f)
    sous_themes_communs = set()
    for cat in schema["categories"]:
        for st in cat["sousThemes"]:
            sous_themes_communs.add(st["id"])
    return sous_themes_communs


def charger_tous_candidats_complets(filtre_ville=None, filtre_candidat=None):
    """Itère elections/*.json et retourne les candidats programmeComplet: true.

    Returns:
        list of dict: [{ville, ville_id, candidat_id, candidat_nom, data, election}]
    """
    resultats = []
    fichiers = sorted(f for f in os.listdir(ELECTIONS_DIR) if f.endswith(".json"))

    for fichier in fichiers:
        ville_id = fichier.replace(".json", "")
        path = os.path.join(ELECTIONS_DIR, fichier)

        with open(path, "r", encoding="utf-8") as f:
            election = json.load(f)

        ville_nom = election.get("ville", ville_id)

        if filtre_ville and filtre_ville.lower() not in ville_nom.lower() and filtre_ville.lower() not in ville_id.lower():
            continue

        for candidat in election.get("candidats", []):
            if not candidat.get("programmeComplet", False):
                continue

            cid = candidat["id"]
            if filtre_candidat and filtre_candidat.lower() not in cid.lower():
                continue

            resultats.append({
                "ville": ville_nom,
                "ville_id": ville_id,
                "candidat_id": cid,
                "candidat_nom": candidat.get("nom", cid),
                "candidat": candidat,
                "election": election,
            })

    return resultats


def compter_mesures_detaillees(election, candidat_id):
    """Compte les mesures par catégorie et sous-thème.

    Returns:
        (total, st_couverts, details) where details = {cat_id: {st_id: count}}
    """
    total = 0
    st_couverts = 0
    details = defaultdict(dict)

    for cat in election.get("categories", []):
        for st in cat.get("sousThemes", []):
            prop = st.get("propositions", {}).get(candidat_id)
            count = 0
            if prop:
                if prop.get("mesures"):
                    count = len(prop["mesures"])
                elif prop.get("texte"):
                    count = 1
            details[cat["id"]][st["id"]] = count
            total += count
            if count > 0:
                st_couverts += 1

    return total, st_couverts, details


def detecter_bilan(election, candidat_id):
    """Détecte les mesures contenant des marqueurs de bilan.

    Exclut les faux positifs courants :
    - "Doublement/Triplement" en début = proposition forward-looking
    - "passage de X à Y" en début = objectif chiffré
    - Mesures contenant un verbe d'action forward-looking

    Returns:
        list of (st_id, mesure_idx, mesure_text, pattern_matched)
    """
    detections = []

    for cat in election.get("categories", []):
        for st in cat.get("sousThemes", []):
            prop = st.get("propositions", {}).get(candidat_id)
            if not prop:
                continue
            mesures = prop.get("mesures", [])
            for idx, mesure in enumerate(mesures):
                for pattern in BILAN_PATTERNS:
                    match = pattern.search(mesure)
                    if match:
                        # Vérifier si c'est un faux positif forward-looking
                        if _is_forward_looking(mesure, match.group()):
                            break  # Skip this measure entirely
                        detections.append((st["id"], idx, mesure, match.group()))
                        break  # Un seul match par mesure suffit

    return detections


def _is_forward_looking(mesure, matched_pattern):
    """Vérifie si une mesure flaggée bilan est en réalité forward-looking."""
    matched_lower = matched_pattern.lower()

    # "Doublement/Triplement" en début de mesure = proposition (pas bilan)
    for p in BILAN_PROPOSAL_PATTERNS:
        if p.search(mesure):
            return True

    # "doublement/triplement" ailleurs dans le texte mais avec verbe d'action
    if matched_lower in ("doublement", "triplement"):
        if BILAN_FORWARD_PATTERNS.search(mesure):
            return True

    # "actuellement" dans un contexte de proposition (avec un objectif chiffré ou contextuel)
    # Presque toujours du contexte pour une proposition, pas du bilan
    if matched_lower == "actuellement":
        return True  # "actuellement" est quasi-systématiquement contextuel

    # "fin 2026/2027/2028" = date cible future
    if re.match(r"fin 20(2[6-9]|3\d)", matched_lower):
        return True

    # "passage de X à Y" avec verbe forward ou en début
    if matched_lower.startswith("passage de"):
        if BILAN_FORWARD_PATTERNS.search(mesure):
            return True

    # "depuis" dans un contexte de référence externe ou parenthétique
    if "depuis" in matched_lower:
        if re.search(r"comme [àa] .+ depuis", mesure, re.IGNORECASE):
            return True
        # "disparu depuis" / "pas réuni depuis" / "inchangé depuis" = critique, pas bilan
        if re.search(r"(disparu|pas réuni|inchang[ée]|inexistant).*depuis", mesure, re.IGNORECASE):
            return True
        # "déjà gratuit/en place... depuis" en parenthèse dans une mesure forward-looking
        if re.search(r"\(.*depuis\s+20\d{2}\)", mesure):
            if BILAN_FORWARD_PATTERNS.search(mesure):
                return True

    return False


def detecter_blocs_monolithiques(election, candidat_id):
    """Détecte les mesures > MONOLITHIC_THRESHOLD caractères.

    Returns:
        list of (st_id, mesure_idx, longueur, mesure_text)
    """
    blocs = []

    for cat in election.get("categories", []):
        for st in cat.get("sousThemes", []):
            prop = st.get("propositions", {}).get(candidat_id)
            if not prop:
                continue
            mesures = prop.get("mesures", [])
            for idx, mesure in enumerate(mesures):
                if len(mesure) > MONOLITHIC_THRESHOLD:
                    blocs.append((st["id"], idx, len(mesure), mesure))

    return blocs


def similarity_ratio(text1, text2):
    """Calcule le ratio de similarité entre deux textes (0-1).
    Réutilise la logique de detecter_doublons.py L19-21."""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def detecter_doublons_candidat(election, candidat_id):
    """Détecte les doublons intra-candidat (mesures similaires > seuil).

    Returns:
        list of (st1_id, idx1, st2_id, idx2, ratio, texte1, texte2)
    """
    doublons = []
    toutes_mesures = []  # [(st_id, idx, texte)]

    for cat in election.get("categories", []):
        for st in cat.get("sousThemes", []):
            prop = st.get("propositions", {}).get(candidat_id)
            if not prop:
                continue
            mesures = prop.get("mesures", [])
            for idx, mesure in enumerate(mesures):
                toutes_mesures.append((st["id"], idx, mesure))

    # Comparaison O(n^2) — acceptable pour ~200 mesures max
    for i in range(len(toutes_mesures)):
        for j in range(i + 1, len(toutes_mesures)):
            st1, idx1, t1 = toutes_mesures[i]
            st2, idx2, t2 = toutes_mesures[j]
            ratio = similarity_ratio(t1, t2)
            if ratio >= SIMILARITY_THRESHOLD:
                doublons.append((st1, idx1, st2, idx2, ratio, t1, t2))

    return doublons


def verifier_coherence_classification(election, candidat_id):
    """Vérifie que les mesures sont dans le bon sous-thème via mots-clés.

    Returns:
        list of (st_id, mesure_idx, mesure_text, meilleur_st_suggere)
    """
    suspects = []

    for cat in election.get("categories", []):
        for st in cat.get("sousThemes", []):
            st_id = st["id"]
            if st_id not in MOTS_CLES_PAR_ST:
                continue

            prop = st.get("propositions", {}).get(candidat_id)
            if not prop:
                continue
            mesures = prop.get("mesures", [])

            mots_cles_st = MOTS_CLES_PAR_ST[st_id]

            for idx, mesure in enumerate(mesures):
                mesure_lower = mesure.lower()
                # La mesure matche-t-elle au moins un mot-clé de son ST ?
                match_propre = any(mc in mesure_lower for mc in mots_cles_st)

                if match_propre:
                    continue  # OK, bien classée

                # Chercher un meilleur ST
                meilleur_st = None
                meilleur_score = 0
                for autre_st, autre_mots in MOTS_CLES_PAR_ST.items():
                    if autre_st == st_id:
                        continue
                    score = sum(1 for mc in autre_mots if mc in mesure_lower)
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_st = autre_st

                if meilleur_st and meilleur_score >= 3:
                    suspects.append((st_id, idx, mesure, meilleur_st))

    return suspects


def verifier_sources(election, candidat_id):
    """Vérifie que source et sourceUrl sont renseignés.

    Returns:
        list of st_id avec source ou sourceUrl vides
    """
    vides = []

    for cat in election.get("categories", []):
        for st in cat.get("sousThemes", []):
            prop = st.get("propositions", {}).get(candidat_id)
            if not prop:
                continue
            if not prop.get("mesures") and not prop.get("texte"):
                continue  # Pas de contenu, pas besoin de source
            source = prop.get("source", "")
            source_url = prop.get("sourceUrl", "")
            if not source or not source_url:
                vides.append(st["id"])

    return vides


def comparer_csv(candidat_id, total_mesures):
    """Compare le nombre de mesures JSON avec le CSV de suivi.

    Returns:
        (csv_count, ecart) or (None, None) si pas trouvé
    """
    if not os.path.exists(SUIVI_CSV):
        return None, None

    try:
        with open(SUIVI_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("id", "").strip() == candidat_id:
                    csv_count = row.get("nb_propositions", "").strip()
                    if csv_count and csv_count.isdigit():
                        csv_count = int(csv_count)
                        return csv_count, total_mesures - csv_count
    except Exception:
        pass

    return None, None


def generer_rapport(resultats_audit, csv_path=None):
    """Affiche le tableau console et exporte en CSV optionnel."""

    # En-tête
    print("\n" + "=" * 100)
    print("  AUDIT DE COMPLETUDE — Candidats programmeComplet: true")
    print("=" * 100)
    print(f"\n  {len(resultats_audit)} candidats audités\n")

    # Tableau
    header = f"{'Ville':<16} | {'Candidat':<14} | {'Mesures':>7} | {'ST':>7} | {'Bilan':>5} | {'Blocs':>5} | {'Doubl':>5} | {'Classif':>7} | {'Sources':<10}"
    print(header)
    print("-" * len(header))

    total_problemes = 0

    for r in resultats_audit:
        sources_str = f"{r['sources_vides']} vides" if r["sources_vides"] > 0 else "OK"
        ligne = (
            f"{r['ville']:<16} | "
            f"{r['candidat_id']:<14} | "
            f"{r['total_mesures']:>7} | "
            f"{r['st_couverts']:>4}/44 | "
            f"{r['nb_bilan']:>5} | "
            f"{r['nb_blocs']:>5} | "
            f"{r['nb_doublons']:>5} | "
            f"{r['nb_misclass']:>7} | "
            f"{sources_str:<10}"
        )
        print(ligne)

        total_problemes += r["nb_bilan"] + r["nb_blocs"] + r["nb_doublons"] + r["nb_misclass"] + r["sources_vides"]

    # Résumé
    print("\n" + "=" * 100)
    total_mesures = sum(r["total_mesures"] for r in resultats_audit)
    total_bilan = sum(r["nb_bilan"] for r in resultats_audit)
    total_blocs = sum(r["nb_blocs"] for r in resultats_audit)
    total_doublons = sum(r["nb_doublons"] for r in resultats_audit)
    total_misclass = sum(r["nb_misclass"] for r in resultats_audit)
    total_sources = sum(r["sources_vides"] for r in resultats_audit)
    faible_mesures = sum(1 for r in resultats_audit if r["total_mesures"] < MIN_MESURES_COMPLET)

    print(f"  Total mesures        : {total_mesures}")
    print(f"  Candidats < {MIN_MESURES_COMPLET} mesures : {faible_mesures}")
    print(f"  Marqueurs bilan      : {total_bilan}")
    print(f"  Blocs monolithiques  : {total_blocs}")
    print(f"  Doublons             : {total_doublons}")
    print(f"  Misclassifications   : {total_misclass}")
    print(f"  Sources vides        : {total_sources}")
    print(f"  Total problèmes      : {total_problemes}")
    print("=" * 100)

    if total_problemes == 0:
        print("\n  Aucun problème détecté !")
    else:
        print(f"\n  {total_problemes} problème(s) à corriger.")

    # Détails des problèmes
    for r in resultats_audit:
        has_issues = (r["nb_bilan"] + r["nb_blocs"] + r["nb_doublons"] + r["nb_misclass"] + r["sources_vides"]) > 0
        if not has_issues and r["total_mesures"] >= MIN_MESURES_COMPLET:
            continue

        print(f"\n  --- {r['ville']} / {r['candidat_id']} ---")

        if r["total_mesures"] < MIN_MESURES_COMPLET:
            print(f"    ALERTE : seulement {r['total_mesures']} mesures (seuil: {MIN_MESURES_COMPLET})")

        for item in r.get("details_bilan", []):
            st_id, idx, texte, pattern = item
            print(f"    BILAN [{st_id}#{idx}] pattern='{pattern}' : {texte[:80]}...")

        for item in r.get("details_blocs", []):
            st_id, idx, longueur, texte = item
            print(f"    BLOC [{st_id}#{idx}] {longueur} chars : {texte[:80]}...")

        for item in r.get("details_doublons", []):
            st1, idx1, st2, idx2, ratio, t1, t2 = item
            print(f"    DOUBLON [{st1}#{idx1}] ~ [{st2}#{idx2}] ({ratio:.0%}) : {t1[:60]}...")

        for item in r.get("details_misclass", []):
            st_id, idx, texte, meilleur = item
            print(f"    MISCLASS [{st_id}#{idx}] -> {meilleur} ? : {texte[:60]}...")

        csv_count, ecart = r.get("csv_count"), r.get("csv_ecart")
        if csv_count is not None and ecart != 0:
            print(f"    ECART CSV : JSON={r['total_mesures']}, CSV={csv_count}, diff={ecart:+d}")

    # Export CSV
    if csv_path:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "ville", "candidat_id", "candidat_nom", "total_mesures", "st_couverts",
                "nb_bilan", "nb_blocs", "nb_doublons", "nb_misclass", "sources_vides",
                "csv_count", "csv_ecart"
            ])
            writer.writeheader()
            for r in resultats_audit:
                writer.writerow({
                    "ville": r["ville"],
                    "candidat_id": r["candidat_id"],
                    "candidat_nom": r["candidat_nom"],
                    "total_mesures": r["total_mesures"],
                    "st_couverts": r["st_couverts"],
                    "nb_bilan": r["nb_bilan"],
                    "nb_blocs": r["nb_blocs"],
                    "nb_doublons": r["nb_doublons"],
                    "nb_misclass": r["nb_misclass"],
                    "sources_vides": r["sources_vides"],
                    "csv_count": r.get("csv_count", ""),
                    "csv_ecart": r.get("csv_ecart", ""),
                })
        print(f"\n  Rapport CSV exporté : {csv_path}")


def main():
    parser = argparse.ArgumentParser(description="Audit de complétude des candidats programmeComplet")
    parser.add_argument("--ville", help="Filtrer par nom de ville (partiel)")
    parser.add_argument("--candidat", help="Filtrer par ID candidat (partiel)")
    parser.add_argument("--csv", help="Chemin du fichier CSV de rapport")
    args = parser.parse_args()

    # Vérifications
    if not os.path.exists(ELECTIONS_DIR):
        print(f"ERREUR : dossier introuvable : {ELECTIONS_DIR}")
        sys.exit(1)
    if not os.path.exists(SCHEMA_JSON):
        print(f"ERREUR : schéma introuvable : {SCHEMA_JSON}")
        sys.exit(1)

    # Charger les candidats complets
    candidats = charger_tous_candidats_complets(
        filtre_ville=args.ville,
        filtre_candidat=args.candidat,
    )

    if not candidats:
        print("Aucun candidat programmeComplet trouvé avec ces filtres.")
        sys.exit(0)

    # Auditer chaque candidat
    resultats_audit = []

    for c in candidats:
        election = c["election"]
        cid = c["candidat_id"]

        total, st_couverts, details = compter_mesures_detaillees(election, cid)
        bilans = detecter_bilan(election, cid)
        blocs = detecter_blocs_monolithiques(election, cid)
        doublons = detecter_doublons_candidat(election, cid)
        misclass = verifier_coherence_classification(election, cid)
        sources = verifier_sources(election, cid)
        csv_count, csv_ecart = comparer_csv(cid, total)

        resultats_audit.append({
            "ville": c["ville"],
            "ville_id": c["ville_id"],
            "candidat_id": cid,
            "candidat_nom": c["candidat_nom"],
            "total_mesures": total,
            "st_couverts": st_couverts,
            "nb_bilan": len(bilans),
            "nb_blocs": len(blocs),
            "nb_doublons": len(doublons),
            "nb_misclass": len(misclass),
            "sources_vides": len(sources),
            "csv_count": csv_count,
            "csv_ecart": csv_ecart,
            "details_bilan": bilans,
            "details_blocs": blocs,
            "details_doublons": doublons,
            "details_misclass": misclass,
        })

    # Trier par ville puis candidat
    resultats_audit.sort(key=lambda r: (r["ville"].lower(), r["candidat_id"]))

    # Générer le rapport
    generer_rapport(resultats_audit, csv_path=args.csv)


if __name__ == "__main__":
    main()
