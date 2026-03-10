#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corriger_audit.py — Correction automatique des problèmes détectés par l'audit
===============================================================================
Phase 1 : Suppression des doublons intra-candidat (similarité >= 0.92)
Phase 2 : Re-split des blocs monolithiques (>200 chars, avec séparateurs clairs)
Phase 3 : Reclassification des mesures mal classées (conservatif)
Phase 4 : Bilan — uniquement les cas les plus évidents (très conservatif)

Usage :
  python scripts/corriger_audit.py                    # Tout corriger (sauf Kobryn)
  python scripts/corriger_audit.py --dry-run          # Simuler sans écrire
  python scripts/corriger_audit.py --ville paris      # Filtrer par ville
  python scripts/corriger_audit.py --phase 1          # Une seule phase
"""

import argparse
import json
import os
import re
import sys
import io
from collections import defaultdict
from copy import deepcopy
from difflib import SequenceMatcher

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ELECTIONS_DIR = os.path.join(ROOT_DIR, "data", "elections")

# Candidats à ne PAS toucher
SKIP_CANDIDATS = {"kobryn"}

# Seuils
SIMILARITY_THRESHOLD = 0.88
MONOLITHIC_THRESHOLD = 200
MIN_MEASURE_LEN = 20

# Mots-clés AFFINÉS pour la correction automatique.
# Plus restrictifs que auditer_completude.py pour éviter les faux positifs.
# Retiré : mots trop génériques (municipale, sécurité, agent, place, quartier,
#          équipement, vert, nature, terrain, durable, etc.)
MOTS_CLES_PAR_ST = {
    "police-municipale": {"police", "policier", "patrouille", "effectif de police", "armement"},
    "videoprotection": {"caméra", "vidéo", "vidéoprotection", "vidéosurveillance"},
    "prevention-mediation": {"médiation", "médiateur", "sécurité routière", "éclairage public"},
    "violences-femmes": {"femme", "harcèlement", "violence conjugale", "sexiste", "sexuel", "féminicide"},
    "transports-en-commun": {"bus", "métro", "tramway", "transport en commun", "ligne de bus", "gare routière", "navigo"},
    "velo-mobilites-douces": {"vélo", "cyclable", "piste cyclable", "vélib", "trottinette"},
    "pietons-circulation": {"piéton", "trottoir", "zone 30", "circulation apaisée", "zone piétonne"},
    "stationnement": {"stationnement", "parking", "garer", "parcmètre"},
    "tarifs-gratuite": {"gratuit", "gratuité", "tarif social", "tarification solidaire"},
    "logement-social": {"logement social", "hlm", "bailleur social", "parc social"},
    "logements-vacants": {"logement vacant", "logement vide", "réquisition", "taxe sur les logements vacants", "airbnb", "meublé touristique"},
    "encadrement-loyers": {"loyer", "encadrement des loyers", "loyer commercial"},
    "acces-logement": {"hébergement d'urgence", "sans-abri", "sdf", "mise à l'abri", "accès au logement"},
    "petite-enfance": {"crèche", "petite enfance", "nourrice", "assistante maternelle", "berceau", "garde d'enfant"},
    "ecoles-renovation": {"école", "scolaire", "collège", "lycée", "rénovation scolaire"},
    "cantines-fournitures": {"cantine", "fourniture scolaire", "repas scolaire", "restauration scolaire"},
    "periscolaire-loisirs": {"périscolaire", "centre aéré", "colonie de vacances", "animation périscolaire"},
    "jeunesse": {"jeune", "étudiant", "jeunesse", "campus", "résidence étudiante"},
    "espaces-verts": {"parc", "jardin", "arbre", "végétalisation", "biodiversité", "forêt urbaine"},
    "proprete-dechets": {"propreté", "déchet", "poubelle", "tri sélectif", "compost", "recyclage", "dépôt sauvage"},
    "climat-adaptation": {"climat", "chaleur", "canicule", "îlot de chaleur", "adaptation climatique"},
    "renovation-energetique": {"rénovation énergétique", "isolation thermique", "passoire énergétique", "chauffage urbain"},
    "alimentation-durable": {"bio", "alimentation locale", "circuit court", "agriculture urbaine"},
    "centres-sante": {"centre de santé", "médecin", "hôpital", "dispensaire", "maison de santé"},
    "prevention-sante": {"santé mentale", "dépistage", "vih", "vaccination", "addiction", "prévention santé"},
    "seniors": {"senior", "personne âgée", "ehpad", "retraité", "aide à domicile", "aidant"},
    "budget-participatif": {"budget participatif", "participation citoyenne", "consultation citoyenne"},
    "transparence": {"transparence", "donnée ouverte", "open data", "éthique", "audit financier"},
    "vie-associative": {"association", "bénévole", "subvention associative", "vie associative"},
    "services-publics": {"service public", "guichet", "accueil en mairie", "démarche administrative"},
    "commerce-local": {"commerce", "commerçant", "artisan", "boutique", "marché local"},
    "emploi-insertion": {"emploi", "insertion", "chômage", "formation professionnelle", "apprentissage"},
    "attractivite": {"tourisme", "attractivité", "international", "entreprise", "innovation"},
    "equipements-culturels": {"musée", "bibliothèque", "théâtre", "conservatoire", "cinéma", "médiathèque"},
    "evenements-creation": {"festival", "spectacle", "artiste", "création artistique", "carnaval"},
    "equipements-sportifs": {"stade", "piscine", "gymnase", "terrain de sport", "équipement sportif"},
    "sport-pour-tous": {"sport", "handisport", "pratique sportive", "club sportif", "olympique"},
    "amenagement-urbain": {"aménagement urbain", "urbanisme", "espace public", "boulevard", "requalification"},
    "accessibilite": {"accessibilité", "handicap", "pmr", "rampe", "ascenseur", "mdph"},
    "quartiers-prioritaires": {"qpv", "quartier prioritaire", "politique de la ville"},
    "aide-sociale": {"rsa", "aide sociale", "minima sociaux", "précarité", "ccas"},
    "egalite-discriminations": {"discrimination", "diversité", "inclusion", "lgbtq", "racisme", "antiraciste"},
    "pouvoir-achat": {"pouvoir d'achat", "coût de la vie", "tarif social", "baisse d'impôt"},
}

# Regex bilan — uniquement les patterns les plus fiables (pas doublement/triplement)
# NB : "dès" est EXCLU car c'est forward-looking ("dès 2028" = engagement futur)
BILAN_STRICT = [
    re.compile(r"depuis\s+20[012]\d(?!\d)", re.IGNORECASE),
    re.compile(r"déjà en place", re.IGNORECASE),
    re.compile(r"\d+\s+déjà\s+installée?s", re.IGNORECASE),
    re.compile(r"augmentation.*depuis\s+20\d{2}", re.IGNORECASE),
    re.compile(r"pas réuni[es]?\s+depuis", re.IGNORECASE),
    re.compile(r"disparu[es]?\s+depuis", re.IGNORECASE),
]

# Contre-patterns : si présent, ce n'est PAS du bilan (forward-looking)
FORWARD_PATTERNS = [
    re.compile(
        r"objectif|ambition|viser|voulons|nous proposons|il faut|créer|"
        r"mettre en place|lancer|développer|instaurer|renforcer|déployer|"
        r"étendre|extension|poursuivre|candidature|expérimenter|"
        r"augmenter|élargir|élargissement|porter à|passer à|"
        r"doubler|tripler|atteindre|proposer|prévoir|engager|"
        r"réactiver|rétablir|rétablissement|réactivée?|restaurer",
        re.IGNORECASE,
    ),
]


def similarity_ratio(t1, t2):
    return SequenceMatcher(None, t1.lower(), t2.lower()).ratio()


def keyword_score(text, st_id):
    """Compte le nombre de mots-clés d'un sous-thème trouvés dans le texte."""
    if st_id not in MOTS_CLES_PAR_ST:
        return -1  # Pas de référentiel pour ce ST (custom)
    text_lower = text.lower()
    return sum(1 for mc in MOTS_CLES_PAR_ST[st_id] if mc in text_lower)


def split_monolithic(text):
    """Tente de découper un bloc monolithique en mesures individuelles.
    Reprend la logique de resplit_blocs.py avec quelques améliorations."""

    # Stratégie 0 : Marqueurs de liste (■, ●, ○, •, –, -)
    for marker in ["■", "●", "○", "•"]:
        if marker in text:
            parts = [p.strip() for p in text.split(marker) if p.strip()]
            if len(parts) >= 2:
                return _clean_parts(parts)

    # Stratégie 1 : Numérotation (1., 2., 3.)
    numbered = re.split(r"(?:^|\s)(\d+)\.\s+", text)
    # re.split with groups gives [pre, num, text, num, text, ...]
    if len(numbered) >= 5:  # At least 2 numbered items
        parts = []
        for i in range(2, len(numbered), 2):
            if numbered[i].strip():
                parts.append(numbered[i].strip())
        if len(parts) >= 2:
            # Prepend the intro text to the first part if it exists
            if numbered[0].strip():
                parts[0] = numbered[0].strip() + " " + parts[0]
            return _clean_parts(parts)

    # Stratégie 2 : ". " + majuscule/chiffre
    parts = re.split(r"\.\s+(?=[A-ZÉÈÊÀÂÔÙÇ0-9])", text)
    if len(parts) > 1:
        return _clean_parts(parts)

    # Stratégie 3 : "; " + minuscule
    parts = re.split(r";\s+(?=[a-zéèêàâ])", text)
    if len(parts) > 1:
        return _clean_parts(parts)

    # Stratégie 4 : " : " comme séparateur de liste
    if " : " in text and text.count(" : ") >= 2:
        parts = [p.strip() for p in text.split(" : ") if p.strip()]
        if len(parts) >= 3:
            return _clean_parts(parts)

    return [text]


def _clean_parts(parts):
    cleaned = []
    for part in parts:
        part = part.strip()
        if len(part) < MIN_MEASURE_LEN:
            continue
        if not part.endswith((".", "!", "?", ")")):
            part += "."
        cleaned.append(part)
    return cleaned if cleaned else [" ".join(p.strip() for p in parts)]


def find_st_in_categories(categories, target_st_id):
    """Trouve un sous-thème par ID dans les catégories. Retourne (cat_idx, st_idx) ou None."""
    for ci, cat in enumerate(categories):
        for si, st in enumerate(cat.get("sousThemes", [])):
            if st["id"] == target_st_id:
                return ci, si
    return None


def get_complet_candidats(data):
    """Retourne l'ensemble des IDs de candidats programmeComplet (hors skip list)."""
    return {
        c["id"]
        for c in data.get("candidats", [])
        if c.get("programmeComplet") and c["id"] not in SKIP_CANDIDATS
    }


# =============================================================================
# Phase 1 : Doublons
# =============================================================================
def phase1_doublons(data, complet_ids, changelog, ville):
    """Supprime les doublons intra-candidat (similarité >= seuil)."""
    categories = data.get("categories", [])
    total_removed = 0

    for cid in complet_ids:
        # Collect all measures with their location
        all_measures = []
        for ci, cat in enumerate(categories):
            for si, st in enumerate(cat.get("sousThemes", [])):
                prop = st.get("propositions", {}).get(cid)
                if not prop or prop is None:
                    continue
                mesures = prop.get("mesures", [])
                for mi, m in enumerate(mesures):
                    all_measures.append({
                        "ci": ci, "si": si, "mi": mi,
                        "text": m, "st_id": st["id"],
                        "norm": " ".join(m.lower().split()),
                    })

        # Find duplicates
        to_remove = set()  # (ci, si, mi) tuples to remove
        for i in range(len(all_measures)):
            if (all_measures[i]["ci"], all_measures[i]["si"], all_measures[i]["mi"]) in to_remove:
                continue
            for j in range(i + 1, len(all_measures)):
                if (all_measures[j]["ci"], all_measures[j]["si"], all_measures[j]["mi"]) in to_remove:
                    continue
                ratio = similarity_ratio(all_measures[i]["norm"], all_measures[j]["norm"])
                if ratio >= SIMILARITY_THRESHOLD:
                    # Keep the longer measure, remove the shorter (or the second if equal)
                    if len(all_measures[i]["text"]) >= len(all_measures[j]["text"]):
                        victim = all_measures[j]
                        keeper = all_measures[i]
                    else:
                        victim = all_measures[i]
                        keeper = all_measures[j]

                    to_remove.add((victim["ci"], victim["si"], victim["mi"]))
                    changelog.append(
                        f"  DOUBLON [{ville}/{cid}] supprimé {victim['st_id']}#{victim['mi']} "
                        f"(dup de {keeper['st_id']}#{keeper['mi']}, {ratio:.0%}): "
                        f"{victim['text'][:70]}..."
                    )

        # Remove measures (reverse order to preserve indices)
        if to_remove:
            # Group removals by (ci, si) and sort indices descending
            removals = defaultdict(list)
            for ci, si, mi in to_remove:
                removals[(ci, si)].append(mi)

            for (ci, si), indices in removals.items():
                st = categories[ci]["sousThemes"][si]
                prop = st["propositions"].get(cid)
                if not prop:
                    continue
                mesures = prop.get("mesures", [])
                for idx in sorted(indices, reverse=True):
                    if idx < len(mesures):
                        mesures.pop(idx)
                        total_removed += 1

                # Clean up empty propositions
                if not mesures:
                    del st["propositions"][cid]

    return total_removed


# =============================================================================
# Phase 2 : Blocs monolithiques
# =============================================================================
def phase2_blocs(data, complet_ids, changelog, ville):
    """Re-split les mesures > MONOLITHIC_THRESHOLD avec séparateurs clairs."""
    categories = data.get("categories", [])
    total_splits = 0
    total_new_measures = 0

    for cid in complet_ids:
        for cat in categories:
            for st in cat.get("sousThemes", []):
                prop = st.get("propositions", {}).get(cid)
                if not prop or prop is None:
                    continue
                mesures = prop.get("mesures", [])
                new_mesures = []
                changed = False

                for mi, m in enumerate(mesures):
                    if len(m) > MONOLITHIC_THRESHOLD:
                        parts = split_monolithic(m)
                        if len(parts) > 1:
                            new_mesures.extend(parts)
                            changed = True
                            total_splits += 1
                            total_new_measures += len(parts) - 1
                            changelog.append(
                                f"  BLOC [{ville}/{cid}] {st['id']}#{mi} "
                                f"({len(m)} chars) -> {len(parts)} mesures"
                            )
                        else:
                            new_mesures.append(m)
                    else:
                        new_mesures.append(m)

                if changed:
                    prop["mesures"] = new_mesures

    return total_splits, total_new_measures


# =============================================================================
# Phase 3 : Reclassification (conservatif)
# =============================================================================
def phase3_misclass(data, complet_ids, changelog, ville):
    """Déplace les mesures mal classées quand c'est sans ambiguïté.

    Critères pour déplacer :
      - 0 mots-clés du ST actuel trouvés dans la mesure
      - >= 2 mots-clés du ST suggéré trouvés dans la mesure
      - Le ST suggéré existe dans les catégories de cette ville
    """
    categories = data.get("categories", [])
    total_moved = 0

    for cid in complet_ids:
        moves = []  # [(source_ci, source_si, mi, target_ci, target_si, mesure, source_st_id, target_st_id)]

        for ci, cat in enumerate(categories):
            for si, st in enumerate(cat.get("sousThemes", [])):
                st_id = st["id"]
                if st_id not in MOTS_CLES_PAR_ST:
                    continue

                prop = st.get("propositions", {}).get(cid)
                if not prop or prop is None:
                    continue
                mesures = prop.get("mesures", [])

                for mi, m in enumerate(mesures):
                    m_lower = m.lower()
                    current_score = sum(1 for mc in MOTS_CLES_PAR_ST[st_id] if mc in m_lower)

                    if current_score > 0:
                        continue  # Has at least one keyword match — leave it

                    # Find best alternative ST
                    best_st = None
                    best_score = 0
                    for autre_st, autre_mots in MOTS_CLES_PAR_ST.items():
                        if autre_st == st_id:
                            continue
                        score = sum(1 for mc in autre_mots if mc in m_lower)
                        if score > best_score:
                            best_score = score
                            best_st = autre_st

                    if best_st and best_score >= 2:
                        # Extra safety: for STs with broad keywords, require higher score
                        min_score = 2
                        # Check target ST exists in this city's categories
                        target_loc = find_st_in_categories(categories, best_st)
                        if target_loc and best_score >= min_score:
                            tci, tsi = target_loc
                            moves.append((ci, si, mi, tci, tsi, m, st_id, best_st))

        # Apply moves (reverse order for source removal)
        # Group by source (ci, si) to remove in correct order
        if not moves:
            continue

        # Sort by source location descending (to not mess up indices when removing)
        moves.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)

        for source_ci, source_si, mi, target_ci, target_si, mesure, src_st_id, tgt_st_id in moves:
            source_st = categories[source_ci]["sousThemes"][source_si]
            target_st = categories[target_ci]["sousThemes"][target_si]

            source_prop = source_st.get("propositions", {}).get(cid)
            if not source_prop or mi >= len(source_prop.get("mesures", [])):
                continue

            # Get source metadata for the target
            source_info = {
                "source": source_prop.get("source", ""),
                "sourceUrl": source_prop.get("sourceUrl", ""),
            }

            # Remove from source
            source_prop["mesures"].pop(mi)

            # Clean up empty source
            if not source_prop["mesures"]:
                del source_st["propositions"][cid]

            # Add to target
            if "propositions" not in target_st:
                target_st["propositions"] = {}

            if cid not in target_st["propositions"] or target_st["propositions"][cid] is None:
                target_st["propositions"][cid] = {
                    "source": source_info["source"],
                    "sourceUrl": source_info["sourceUrl"],
                    "mesures": [mesure],
                }
            else:
                target_st["propositions"][cid]["mesures"].append(mesure)

            total_moved += 1
            changelog.append(
                f"  MOVE [{ville}/{cid}] {src_st_id} -> {tgt_st_id}: "
                f"{mesure[:70]}..."
            )

    return total_moved


# =============================================================================
# Phase 4 : Bilan (très conservatif)
# =============================================================================
def phase4_bilan(data, complet_ids, changelog, ville):
    """Supprime uniquement les mesures qui sont CLAIREMENT du bilan.

    Critères stricts :
      - La mesure matche un pattern bilan strict (depuis 20XX, déjà en place...)
      - La mesure ne contient AUCUN marqueur forward-looking
      - La mesure fait < 150 chars (les longues ont souvent les deux aspects)
    """
    categories = data.get("categories", [])
    total_removed = 0

    for cid in complet_ids:
        removals = []  # (ci, si, mi, mesure)

        for ci, cat in enumerate(categories):
            for si, st in enumerate(cat.get("sousThemes", [])):
                prop = st.get("propositions", {}).get(cid)
                if not prop or prop is None:
                    continue
                mesures = prop.get("mesures", [])

                for mi, m in enumerate(mesures):
                    # Check strict bilan patterns
                    is_bilan = any(p.search(m) for p in BILAN_STRICT)
                    if not is_bilan:
                        continue

                    # Check for forward-looking language
                    is_forward = any(p.search(m) for p in FORWARD_PATTERNS)
                    if is_forward:
                        continue  # Mixed bilan + proposal — keep it

                    # Only remove short measures (long ones are likely mixed)
                    if len(m) > 150:
                        continue

                    removals.append((ci, si, mi, m, st["id"]))

        # Remove (reverse order)
        for ci, si, mi, mesure, st_id in sorted(removals, key=lambda x: (x[0], x[1], x[2]), reverse=True):
            st = categories[ci]["sousThemes"][si]
            prop = st.get("propositions", {}).get(cid)
            if not prop or mi >= len(prop.get("mesures", [])):
                continue
            prop["mesures"].pop(mi)
            total_removed += 1
            changelog.append(
                f"  BILAN [{ville}/{cid}] supprimé {st_id}#{mi}: "
                f"{mesure[:70]}..."
            )

            if not prop["mesures"]:
                del st["propositions"][cid]

    return total_removed


# =============================================================================
# Main
# =============================================================================
def process_file(filepath, phases, dry_run=False):
    """Traite un fichier JSON d'élection."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    ville = data.get("ville", os.path.basename(filepath).replace(".json", ""))
    complet_ids = get_complet_candidats(data)

    if not complet_ids:
        return None

    changelog = []
    stats = {"doublons": 0, "blocs_split": 0, "new_measures": 0, "moved": 0, "bilan": 0}

    if 1 in phases:
        stats["doublons"] = phase1_doublons(data, complet_ids, changelog, ville)

    if 2 in phases:
        stats["blocs_split"], stats["new_measures"] = phase2_blocs(data, complet_ids, changelog, ville)

    if 3 in phases:
        stats["moved"] = phase3_misclass(data, complet_ids, changelog, ville)

    if 4 in phases:
        stats["bilan"] = phase4_bilan(data, complet_ids, changelog, ville)

    total_changes = stats["doublons"] + stats["blocs_split"] + stats["moved"] + stats["bilan"]

    if total_changes > 0 and not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")

    return {
        "ville": ville,
        "candidats": len(complet_ids),
        "stats": stats,
        "changelog": changelog,
        "total_changes": total_changes,
    }


def main():
    parser = argparse.ArgumentParser(description="Correction automatique de l'audit")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans écrire")
    parser.add_argument("--ville", help="Filtrer par nom de ville (partiel)")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4], help="Exécuter une seule phase")
    args = parser.parse_args()

    phases = {args.phase} if args.phase else {1, 2, 3, 4}
    phase_names = {1: "Doublons", 2: "Blocs", 3: "Misclass", 4: "Bilan"}

    print("\n" + "=" * 90)
    print(f"  CORRECTION AUTOMATIQUE — Phases: {', '.join(phase_names[p] for p in sorted(phases))}")
    if args.dry_run:
        print("  MODE DRY-RUN — Aucune modification ne sera écrite")
    print("=" * 90 + "\n")

    fichiers = sorted(
        f for f in os.listdir(ELECTIONS_DIR) if f.endswith(".json")
    )

    totals = {"doublons": 0, "blocs_split": 0, "new_measures": 0, "moved": 0, "bilan": 0}
    total_fichiers = 0
    all_changelog = []

    for fichier in fichiers:
        ville_id = fichier.replace(".json", "")
        filepath = os.path.join(ELECTIONS_DIR, fichier)

        if args.ville and args.ville.lower() not in ville_id.lower():
            continue

        result = process_file(filepath, phases, dry_run=args.dry_run)
        if not result or result["total_changes"] == 0:
            continue

        total_fichiers += 1
        s = result["stats"]
        print(f"  {result['ville']:<25} | doub:{s['doublons']:>3} | split:{s['blocs_split']:>3} (+{s['new_measures']:>3}) | move:{s['moved']:>3} | bilan:{s['bilan']:>3}")

        for k in totals:
            totals[k] += s[k]
        all_changelog.extend(result["changelog"])

    # Résumé
    print("\n" + "=" * 90)
    print(f"  Fichiers modifiés     : {total_fichiers}")
    print(f"  Doublons supprimés    : {totals['doublons']}")
    print(f"  Blocs re-découpés     : {totals['blocs_split']} (+ {totals['new_measures']} nouvelles mesures)")
    print(f"  Mesures reclassées    : {totals['moved']}")
    print(f"  Bilan supprimé        : {totals['bilan']}")
    total = totals["doublons"] + totals["blocs_split"] + totals["moved"] + totals["bilan"]
    print(f"  Total corrections     : {total}")
    print("=" * 90)

    # Changelog détaillé
    if all_changelog:
        print(f"\n  CHANGELOG DÉTAILLÉ ({len(all_changelog)} entrées):\n")
        for line in all_changelog:
            print(line)

    return total


if __name__ == "__main__":
    total = main()
    sys.exit(0 if total >= 0 else 1)
