#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nettoyage : suppression du bilan (track record) et correction des
misclassifications dans les données issues de WebFetch.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def load_json(filename):
    path = os.path.join(ROOT_DIR, "data", "elections", filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), path


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def remove_mesures(data, candidat_id, removals):
    """Supprime des mesures spécifiques. removals = {st_id: [indices 0-based]}"""
    removed = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in removals:
                prop = st["propositions"].get(candidat_id)
                if prop and prop.get("mesures"):
                    old = prop["mesures"]
                    indices = sorted(removals[st_id], reverse=True)
                    for idx in indices:
                        if idx < len(old):
                            print(f"    ✗ [{st_id}] {old[idx][:80]}...")
                            old.pop(idx)
                            removed += 1
                    if not old:
                        # Sous-thème vide → mettre mesures à liste vide
                        prop["mesures"] = []
    return removed


def replace_mesures(data, candidat_id, st_id, new_mesures):
    """Remplace les mesures d'un sous-thème."""
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == st_id:
                prop = st["propositions"].get(candidat_id)
                if prop is None:
                    prop = {}
                    st["propositions"][candidat_id] = prop
                prop["mesures"] = new_mesures
                return


def move_mesure(data, candidat_id, from_st, from_idx, to_st):
    """Déplace une mesure d'un sous-thème à un autre."""
    mesure = None
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == from_st:
                prop = st["propositions"].get(candidat_id)
                if prop and prop.get("mesures") and from_idx < len(prop["mesures"]):
                    mesure = prop["mesures"].pop(from_idx)
                    break
    if mesure:
        for cat in data["categories"]:
            for st in cat["sousThemes"]:
                if st["id"] == to_st:
                    prop = st["propositions"].get(candidat_id)
                    if prop is None:
                        prop = {"mesures": [], "source": "", "sourceUrl": ""}
                        st["propositions"][candidat_id] = prop
                    if "mesures" not in prop:
                        prop["mesures"] = []
                    prop["mesures"].append(mesure)
                    print(f"    ↪ [{from_st}] → [{to_st}] {mesure[:60]}...")
                    return


def count_mesures(data, candidat_id):
    total = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            prop = st["propositions"].get(candidat_id)
            if prop and prop.get("mesures"):
                total += len(prop["mesures"])
    return total


def main():
    print("=" * 60)
    print("  NETTOYAGE BILAN & MISCLASSIFICATIONS")
    print("=" * 60)

    # ===== MOUDENC (Toulouse) =====
    print("\n  MOUDENC (Toulouse):")
    data, path = load_json("toulouse-2026.json")
    before = count_mesures(data, "moudenc")

    # Supprimer les mesures bilan
    removals = {
        "police-municipale": [
            0,  # "Augmentation des effectifs de 165 à 390 agents depuis 2014"
            4,  # "Armement permanent de la police municipale" (bilan 2014)
            5,  # "Équipement en pistolets à impulsions électriques" (bilan 2020-21)
            6,  # "Dotation en lanceurs de balles de défense" (bilan 2024)
            7,  # "Construction du commissariat Basso Cambo" (bilan 2023)
        ],
        "videoprotection": [
            1,  # "Passage de 21 à 710 caméras fin 2025" (bilan)
            4,  # "détection de détresse : 500 situations" (bilan)
            5,  # "7 238 réquisitions judiciaires en 2025" (bilan)
        ],
        "prevention-mediation": [
            1,  # "Triplement du budget sécurité 16,4→42M€" (bilan)
        ],
        "transports-en-commun": [
            5,  # "Record de fréquentation" (bilan)
            6,  # "Budget mobilité le plus élevé de France" (bilan/boast)
        ],
        "logement-social": [
            0,  # "Production de 10 147 logements entre 2014 et 2024" (bilan)
            3,  # "2 658 accessions sociales depuis 2014" (bilan)
        ],
        "cantines-fournitures": [
            0,  # "Gel des tarifs depuis 2015" (bilan)
        ],
        "renovation-energetique": [
            2,  # "Subventions rénovation 3 776 € par projet" (bilan chiffré)
            3,  # "Subventions véhicules propres 2 960 €" (bilan chiffré)
        ],
    }

    removed = remove_mesures(data, "moudenc", removals)

    # Aussi supprimer les mesures trop vagues / status quo
    removals2 = {
        "transports-en-commun": [1],  # "Maintien du métro comme colonne vertébrale" (vague)
        "pietons-circulation": [0],   # "Maintien de la vitesse à 50/90 km/h" (status quo)
    }
    removed += remove_mesures(data, "moudenc", removals2)

    # Reformuler certaines mesures bilan→proposition
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == "stationnement":
                prop = st["propositions"].get("moudenc")
                if prop and prop.get("mesures"):
                    # "Tarif parmi les plus bas : 100€" → "Maintenir le tarif à 100€"
                    for i, m in enumerate(prop["mesures"]):
                        if "100 €/an" in m:
                            prop["mesures"][i] = "Maintenir le tarif de stationnement résidentiel à 100 €/an."
                            print(f"    ✎ [stationnement] Reformulé en proposition")
            if st["id"] == "seniors":
                prop = st["propositions"].get("moudenc")
                if prop and prop.get("mesures"):
                    for i, m in enumerate(prop["mesures"]):
                        if "3,40 €" in m and "gelé" in m:
                            prop["mesures"][i] = "Maintenir le tarif des repas seniors à 3,40 €."
                            print(f"    ✎ [seniors] Reformulé en proposition")
            if st["id"] == "equipements-sportifs":
                prop = st["propositions"].get("moudenc")
                if prop and prop.get("mesures"):
                    for i, m in enumerate(prop["mesures"]):
                        if "3,40 € l'entrée" in m:
                            prop["mesures"][i] = "Maintenir le tarif des piscines municipales à 3,40 €."
                            print(f"    ✎ [equipements-sportifs] Reformulé en proposition")

    after = count_mesures(data, "moudenc")
    print(f"    Résultat : {before} → {after} mesures ({removed} supprimées)")
    save_json(data, path)

    # ===== DELAFOSSE (Montpellier) =====
    print("\n  DELAFOSSE (Montpellier):")
    data, path = load_json("montpellier-2026.json")
    before = count_mesures(data, "delafosse")

    removals = {
        "tarifs-gratuite": [
            0,  # "Gratuité déjà en place et défendue" (bilan)
        ],
        "budget-participatif": [
            0,  # "Mutuelle communale déjà en place et maintenue" (bilan + mauvais ST)
        ],
        "cantines-fournitures": [
            0,  # "76% de produits durables, doublement depuis 2020" (bilan)
        ],
        "prevention-mediation": [
            1,  # "Passage de 100 à 4 000 heures de TIG" (bilan)
        ],
    }
    removed = remove_mesures(data, "delafosse", removals)

    # Reformuler le "passage de 500 à 1000 caméras" → proposition
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == "videoprotection":
                prop = st["propositions"].get("delafosse")
                if prop and prop.get("mesures"):
                    for i, m in enumerate(prop["mesures"]):
                        if "passage de 500" in m.lower():
                            prop["mesures"][i] = "Doubler le nombre de caméras de vidéosurveillance pour atteindre 1 000 unités."
                            print(f"    ✎ [videoprotection] Reformulé (retiré bilan)")

    after = count_mesures(data, "delafosse")
    print(f"    Résultat : {before} → {after} mesures ({removed} supprimées)")
    save_json(data, path)

    # ===== DOUCET (Lyon) - misclassifications =====
    print("\n  DOUCET (Lyon) - corrections:")
    data, path = load_json("lyon-2026.json")
    before = count_mesures(data, "doucet")

    # 1. climat-adaptation contient des mesures animaux → les déplacer
    # Indices dans climat-adaptation AVANT déplacements :
    # 0: "fonds municipal d'adaptation logements chaleur" → OK
    # 1: "zoo Tête d'Or animaux en danger" → pas climat
    # 2: "aires d'ébat canines" → pas climat
    # 3: "stérilisation chats errants" → pas climat
    # On supprime 1, 2, 3 (pas de sous-thème adapté, ce ne sont pas des mesures municipales majeures)
    removals = {
        "climat-adaptation": [1, 2, 3],  # mesures animaux, pas climat
    }
    removed = remove_mesures(data, "doucet", removals)

    # 2. pouvoir-achat contient "prix libre musées" → doublon avec equipements-culturels, supprimer
    removals2 = {
        "pouvoir-achat": [0],  # "prix libre musées" déjà dans equipements-culturels
    }
    removed += remove_mesures(data, "doucet", removals2)

    # 3. transparence contient "charte droits Rhône et Saône" → pas de la transparence
    # Déplacer vers amenagement-urbain ou espaces-verts
    move_mesure(data, "doucet", "transparence", 0, "espaces-verts")

    # 4. Supprimer les 2 mesures douteuses de police-municipale (non trouvées sur le site)
    # "Créer une deuxième brigade cycliste" (idx 1) et "Former les policiers au dialogue" (idx 3)
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == "police-municipale":
                prop = st["propositions"].get("doucet")
                if prop and prop.get("mesures"):
                    to_remove = []
                    for i, m in enumerate(prop["mesures"]):
                        if "brigade cycliste" in m.lower():
                            to_remove.append(i)
                        elif "former les policiers" in m.lower() and "dialogue" in m.lower():
                            to_remove.append(i)
                    for idx in sorted(to_remove, reverse=True):
                        print(f"    ✗ [police-municipale] {prop['mesures'][idx][:80]}...")
                        prop["mesures"].pop(idx)
                        removed += 1

    # 5. prevention-mediation: "dispositif innovant repérer jeunes" semble un dédoublement du plan narcotrafic
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == "prevention-mediation":
                prop = st["propositions"].get("doucet")
                if prop and prop.get("mesures"):
                    to_remove = []
                    for i, m in enumerate(prop["mesures"]):
                        if "dispositif innovant" in m.lower() and "repérer" in m.lower():
                            to_remove.append(i)
                    for idx in sorted(to_remove, reverse=True):
                        print(f"    ✗ [prevention-mediation] {prop['mesures'][idx][:80]}...")
                        prop["mesures"].pop(idx)
                        removed += 1

    # 6. accessibilite doublon avec services-publics (application PMR)
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == "accessibilite":
                prop = st["propositions"].get("doucet")
                if prop and prop.get("mesures"):
                    to_remove = []
                    for i, m in enumerate(prop["mesures"]):
                        if "application collaborative" in m.lower() and "pmr" in m.lower():
                            # Vérifier si c'est aussi dans services-publics
                            to_remove.append(i)
                    for idx in sorted(to_remove, reverse=True):
                        print(f"    ✗ [accessibilite] doublon: {prop['mesures'][idx][:60]}...")
                        prop["mesures"].pop(idx)
                        removed += 1

    after = count_mesures(data, "doucet")
    print(f"    Résultat : {before} → {after} mesures ({removed} supprimées, 1 déplacée)")
    save_json(data, path)

    # ===== AULAS (Lyon) =====
    print("\n  AULAS (Lyon):")
    data, path = load_json("lyon-2026.json")
    before_a = count_mesures(data, "aulas")
    # "500 policiers d'ici 2033 (contre 311 actuellement)" → reformuler
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == "police-municipale":
                prop = st["propositions"].get("aulas")
                if prop and prop.get("mesures"):
                    for i, m in enumerate(prop["mesures"]):
                        if "actuellement" in m.lower() or "contre 311" in m.lower():
                            prop["mesures"][i] = "Porter les effectifs de police municipale à 500 agents d'ici 2033."
                            print(f"    ✎ [police-municipale] Reformulé (retiré chiffre bilan)")
    after_a = count_mesures(data, "aulas")
    print(f"    Résultat : {before_a} → {after_a} mesures")
    save_json(data, path)

    # ===== ROLLAND (Nantes) =====
    print("\n  ROLLAND (Nantes):")
    data, path = load_json("nantes-2026.json")
    before_r = count_mesures(data, "rolland")
    # "Poursuite augmentation engagée depuis 2020" → reformuler
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == "police-municipale":
                prop = st["propositions"].get("rolland")
                if prop and prop.get("mesures"):
                    for i, m in enumerate(prop["mesures"]):
                        if "depuis 2020" in m.lower():
                            prop["mesures"][i] = "Poursuivre le renforcement des effectifs de police municipale."
                            print(f"    ✎ [police-municipale] Reformulé (retiré date bilan)")
    after_r = count_mesures(data, "rolland")
    print(f"    Résultat : {before_r} → {after_r} mesures")
    save_json(data, path)

    print("\n" + "=" * 60)
    print("  NETTOYAGE TERMINÉ")
    print("=" * 60)


if __name__ == "__main__":
    main()
