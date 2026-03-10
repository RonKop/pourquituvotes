#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction des mesures d'Alfandari (Tours) depuis le PDF extrait.
Remplace les blocs monolithiques par des mesures individuelles.
"""

import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TEXTE_PATH = os.path.join(ROOT_DIR, "data", "programmes", "alfandari_tours_full_text.txt")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "tours-2026.json")

SECTIONS_MAPPING = {
    "police-municipale": {
        "keywords": ["police", "effectif", "proximité police", "agent", "patrouille",
                      "sortie des collèges", "carrière revalori"],
    },
    "videoprotection": {
        "keywords": ["caméra", "vidéoprotect", "éclairage public", "détecteur de mouvement",
                      "centre de contrôle"],
    },
    "prevention-mediation": {
        "keywords": ["tolérance zéro", "incivilité", "alcoolisation", "stupéfiant",
                      "dégradation", "TIG", "procureur", "sanctions", "nuisance"],
    },
    "violences-femmes": {
        "keywords": ["victime", "violence", "Maison d'accompagnement"],
    },
    "transports-en-commun": {
        "keywords": ["tramway", "tram", "transport en commun", "desserte", "RER",
                      "gare", "Saint-Pierre-des-Corps"],
    },
    "velo-mobilites-douces": {
        "keywords": ["navette", "téléport", "aéroport liaison", "automatique"],
    },
    "pietons-circulation": {
        "keywords": ["circulation", "feu", "synchronis", "plan de circulation",
                      "pont Wilson", "piéton", "contresens"],
    },
    "stationnement": {
        "keywords": ["parking", "stationnement", "place", "souterrain", "gratuité"],
    },
    "logement-social": {
        "keywords": ["logement étudiant", "logement social"],
    },
    "logements-vacants": {
        "keywords": ["friche", "Menneton", "Ilot Vinci", "réhabilit", "immobilier post-guerre"],
    },
    "acces-logement": {
        "keywords": ["réhabilitation", "façade", "isolation thermique", "ANAH",
                      "logement", "embellir"],
    },
    "petite-enfance": {
        "keywords": ["garde", "horaires décalés", "monoparentale", "crèche",
                      "enfant garde"],
    },
    "ecoles-renovation": {
        "keywords": ["rénovation école", "bâti scolaire", "confort thermique",
                      "pic de chaleur"],
    },
    "periscolaire-loisirs": {
        "keywords": ["périscolaire", "extrascolaire", "continuité éducative",
                      "égalité des chances"],
    },
    "jeunesse": {
        "keywords": ["jeune", "université", "partenariat international",
                      "accompagnement jeune", "études supérieures", "quartier emploi"],
    },
    "espaces-verts": {
        "keywords": ["arbre", "fleur", "jardin", "plantation", "ombre", "parc",
                      "Maison des Jardins", "semence", "végétal"],
    },
    "proprete-dechets": {
        "keywords": ["propreté", "nettoyage", "déchet", "dépôt sauvage", "nuisible",
                      "poubelle", "biodéchet", "balayage", "ramassage", "stérilisation"],
    },
    "climat-adaptation": {
        "keywords": ["climat", "rafraîchir", "chaleur"],
    },
    "renovation-energetique": {
        "keywords": ["isolation", "réhabilitation énergétique", "thermique"],
    },
    "centres-sante": {
        "keywords": ["maison de santé", "médecin", "généraliste", "installation médecin",
                      "pluridisciplinaire", "locaux adaptés"],
    },
    "prevention-sante": {
        "keywords": ["parcours santé", "prévention santé"],
    },
    "budget-participatif": {
        "keywords": ["référendum", "initiative locale", "comité de quartier",
                      "plateforme collaborative", "brigade citoyenne",
                      "commissions consultatives"],
    },
    "transparence": {
        "keywords": ["audit", "économie budget", "transparence", "gestion saine",
                      "plan d'économies", "charte d'achats"],
    },
    "vie-associative": {
        "keywords": ["association", "bénévolat", "salle municipale", "engagement local"],
    },
    "services-publics": {
        "keywords": ["mairie mobile", "numéro unique", "adjoint responsable",
                      "permanence", "service municipal", "quartier problème"],
    },
    "commerce-local": {
        "keywords": ["commerce", "commerçant", "halles", "foncière commerciale",
                      "fonds de commerce", "Pont Wilson commerce"],
    },
    "emploi-insertion": {
        "keywords": ["emploi", "insertion", "impôt entreprise", "création d'activité"],
    },
    "attractivite": {
        "keywords": ["pôle d'innovation", "Tech", "aéroport", "RH des armées",
                      "nucléaire", "IA", "attracti", "Parc Expo", "Arena",
                      "tourisme", "Jardins de la France destination"],
    },
    "equipements-culturels": {
        "keywords": ["Opéra", "Grand Théâtre", "Bibliothèque", "chorégraphique",
                      "école d'art", "Château de Tours", "musée", "auditorium"],
    },
    "evenements-creation": {
        "keywords": ["festival", "gastronomie", "Biennale", "forêt des livres",
                      "exposition", "artiste local", "capitale culturelle",
                      "européenne de la culture"],
    },
    "equipements-sportifs": {
        "keywords": ["patinoire", "piscine", "basketball", "volleyball", "Grenon",
                      "Arena sport", "équipement sportif"],
    },
    "sport-pour-tous": {
        "keywords": ["Olympiades", "licence", "sport enfant", "quartier prioritaire sport",
                      "mécénat sport"],
    },
    "amenagement-urbain": {
        "keywords": ["Loire", "Cher", "promenade", "quai", "ponton", "bord",
                      "aménagement urbain", "zone commerciale"],
    },
    "accessibilite": {
        "keywords": ["handicap", "PMR", "accessibilité", "obstacle"],
    },
    "quartiers-prioritaires": {
        "keywords": ["quartier", "responsable quartier", "réunion quartier"],
    },
    "aide-sociale": {
        "keywords": ["social", "solidarité"],
    },
    "pouvoir-achat": {
        "keywords": ["impôt", "hausse d'impôts", "économie budget", "pouvoir d'achat"],
    },
}


def load_text():
    """Charge le texte extrait du PDF."""
    with open(TEXTE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def extract_bullets_and_sections(text):
    """Extrait les mesures marquées par des bullets (•) et des sections (>)."""
    mesures = []
    lines = text.split("\n")
    current_bullet = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Détecter un nouveau bullet (• ou >)
        if line.startswith("•"):
            if current_bullet:
                mesures.append(clean_mesure(current_bullet))
            current_bullet = line[1:].strip()
        elif current_bullet is not None:
            # Fin de bullet si c'est un titre en majuscules, un marqueur de page ou section
            if line.startswith("===") or (line.isupper() and len(line) > 10):
                if current_bullet:
                    mesures.append(clean_mesure(current_bullet))
                current_bullet = None
            elif line.startswith(">"):
                if current_bullet:
                    mesures.append(clean_mesure(current_bullet))
                current_bullet = None
            elif line.startswith("Priorité n°"):
                if current_bullet:
                    mesures.append(clean_mesure(current_bullet))
                current_bullet = None
            else:
                current_bullet += " " + line

    if current_bullet:
        mesures.append(clean_mesure(current_bullet))

    # Extraire aussi les propositions structurées sans bullet
    # (paragraphes qui commencent par un verbe d'action après un titre)
    structured = extract_structured_proposals(text)
    mesures.extend(structured)

    return [m for m in mesures if m and len(m) >= 20]


def extract_structured_proposals(text):
    """Extrait les propositions structurées (non-bullet) du texte."""
    mesures = []
    lines = text.split("\n")

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Propositions avec format "Titre : Texte descriptif"
        # Ex: "800 places de parking supplémentaires : Création de deux parkings..."
        # Ex: "Création d'une Maison d'accompagnement des victimes..."
        if (line.startswith("Créer ") or line.startswith("Création ") or
            line.startswith("Développer ") or line.startswith("Transformer ") or
            line.startswith("Réhabiliter ") or line.startswith("Réouverture ") or
            line.startswith("Garantir ") or line.startswith("Assurer ") or
            line.startswith("Mobiliser ") or line.startswith("Permettre ") or
            line.startswith("Faciliter ")) and len(line) > 50:

            # Vérifier que ce n'est pas déjà un bullet
            prev_lines = [lines[j].strip() for j in range(max(0, i-3), i)]
            if not any(l.startswith("•") for l in prev_lines):
                # Accumuler les lignes suivantes si elles ne sont pas des titres
                proposal = line
                for j in range(i + 1, min(len(lines), i + 5)):
                    next_line = lines[j].strip()
                    if not next_line or next_line.startswith("•") or \
                       next_line.startswith("===") or next_line.isupper() or \
                       next_line.startswith(">"):
                        break
                    proposal += " " + next_line
                mesures.append(clean_mesure(proposal))

    return mesures


def clean_mesure(text):
    """Nettoie une mesure."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^[-–—]\s*", "", text)
    # Retirer les sous-titres redondants au début
    text = re.sub(r"^(Un |Une |Des |Le |La |Les )?signalement simple et direct\s*:\s*", "", text)

    if len(text) > 300:
        idx = text[:300].rfind(".")
        if idx > 100:
            text = text[:idx + 1]
        else:
            text = text[:297] + "..."
    if text and text[-1] not in ".!?)":
        text += "."
    return text


def classify_mesure(mesure, mapping):
    """Classifie une mesure dans le sous-thème le plus pertinent."""
    mesure_lower = mesure.lower()
    best_match = None
    best_score = 0

    for st_id, config in mapping.items():
        score = 0
        for kw in config["keywords"]:
            if kw.lower() in mesure_lower:
                score += 1
                if len(kw) > 10:
                    score += 0.5
        if score > best_score:
            best_score = score
            best_match = st_id

    return best_match, best_score


def main():
    print("=" * 60)
    print("  RÉ-EXTRACTION ALFANDARI (Tours)")
    print("=" * 60)
    print()

    text = load_text()
    print(f"  Texte chargé : {len(text)} caractères")

    mesures = extract_bullets_and_sections(text)
    print(f"  Mesures extraites : {len(mesures)}")
    print()

    # Dédupliquer
    seen = set()
    unique = []
    for m in mesures:
        key = m[:60].lower()
        if key not in seen:
            seen.add(key)
            unique.append(m)
    mesures = unique
    print(f"  Après déduplication : {len(mesures)}")

    classified = {}
    unclassified = []

    for m in mesures:
        st_id, score = classify_mesure(m, SECTIONS_MAPPING)
        if st_id and score >= 1:
            if st_id not in classified:
                classified[st_id] = []
            classified[st_id].append(m)
        else:
            unclassified.append(m)

    print("\n  Classification :")
    for st_id in sorted(classified.keys()):
        print(f"    {st_id}: {len(classified[st_id])} mesures")

    if unclassified:
        print(f"\n  Non classifiées ({len(unclassified)}) :")
        for m in unclassified:
            print(f"    - {m[:80]}...")

    # Charger le JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in classified and len(classified[st_id]) > 0:
                prop = st["propositions"].get("alfandari")
                if prop is None:
                    prop = {}
                    st["propositions"]["alfandari"] = prop

                old_count = len(prop.get("mesures", []))
                new_mesures = classified[st_id]

                if old_count <= 1 or len(new_mesures) > old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = "Programme officiel 2026 — Henri Alfandari"
                    prop["sourceUrl"] = "https://www.naturellement-tours.fr"
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} → {len(new_mesures)} mesures")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total_mesures = sum(len(v) for v in classified.values())
    print(f"\n  RÉSULTAT : {total_mesures} mesures extraites, {updated} sous-thèmes mis à jour")
    print("=" * 60)


if __name__ == "__main__":
    main()
