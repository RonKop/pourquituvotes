#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction des mesures de Perrein (Montpellier) depuis le PDF extrait.
Remplace les blocs monolithiques par des mesures individuelles.
"""

import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TEXTE_PATH = os.path.join(ROOT_DIR, "data", "programmes", "perrein_montpellier_full_text.txt")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "montpellier-2026.json")

# Mapping des sections PDF vers les sous-thèmes
# Chaque entrée : (sous_theme_ids, keywords_pour_distribution)
SECTIONS_MAPPING = {
    "police-municipale": {
        "keywords": ["police", "effectif", "patrouill", "GSO", "poste central", "cadet",
                      "maillage", "présence renforcée", "proche des habitants"],
    },
    "videoprotection": {
        "keywords": ["caméra", "CSU", "supervision", "vidéo", "écran", "360",
                      "lecture automatique", "plaque"],
    },
    "prevention-mediation": {
        "keywords": ["tolérance zéro", "couvre-feu", "incivilité", "récidiviste",
                      "exclusion", "épicerie de nuit", "drogue", "trafic",
                      "partie civile", "procureur", "identité"],
    },
    "violences-femmes": {
        "keywords": ["femme", "violence", "hébergement sécurisé", "agresseur",
                      "harcèlement", "consentement", "sexist", "mariage",
                      "référent", "accompagnant"],
    },
    "transports-en-commun": {
        "keywords": ["tram", "bus", "minibus", "ligne", "transport en commun",
                      "dessert", "cadence", "amplitude"],
    },
    "velo-mobilites-douces": {
        "keywords": ["cycla", "vélo", "piste", "balisage", "sens interdit",
                      "trottinett", "stationnement vélo"],
    },
    "pietons-circulation": {
        "keywords": ["piéton", "PMR", "trottoir", "cheminement", "passage piéton",
                      "anneau de circulation", "tunnel", "désengorger", "feu",
                      "réouverture", "pont", "dégagement", "circulation"],
    },
    "stationnement": {
        "keywords": ["parking", "stationnement", "livraison", "gratuité parking",
                      "Marché aux Fleurs", "tarif", "parkings aériens"],
    },
    "tarifs-gratuite": {
        "keywords": ["gratuité transport", "tarif transport", "solidaire transport"],
    },
    "logement-social": {
        "keywords": ["logement social", "HLM", "gardien", "réhabilit"],
    },
    "acces-logement": {
        "keywords": ["propriétaire", "densification", "prix abordable",
                      "accès logement", "primo-accédant"],
    },
    "petite-enfance": {
        "keywords": ["crèche", "assistante maternelle", "petite enfance",
                      "tout-petit", "garde d'enfant"],
    },
    "ecoles-renovation": {
        "keywords": ["école", "scolaire", "rénovation école", "climatisation",
                      "salle de classe", "bibliothèque école"],
    },
    "cantines-fournitures": {
        "keywords": ["cantine", "fourniture", "restauration scolaire"],
    },
    "periscolaire-loisirs": {
        "keywords": ["périscolaire", "activités éducatives", "vacances scolaires",
                      "maison pour tous", "atelier"],
    },
    "jeunesse": {
        "keywords": ["jeune", "stagiaire", "passeport", "permis", "plateforme numérique",
                      "métier", "formation jeune", "16 à 25"],
    },
    "espaces-verts": {
        "keywords": ["parc", "jardin", "potager", "espaces verts", "Peyrou",
                      "Montcalm", "fontaine", "arbre"],
    },
    "proprete-dechets": {
        "keywords": ["propreté", "nettoyage", "déchet", "tri", "compost",
                      "Amétyst", "incinérateur", "poubelle", "corbeille",
                      "économie circulaire", "recyclage"],
    },
    "climat-adaptation": {
        "keywords": ["climat", "îlot de fraîcheur", "ombre", "chaleur"],
    },
    "renovation-energetique": {
        "keywords": ["data center", "chaleur urbain", "énergi", "photovoltaïque",
                      "isolation", "rénovation énergétique"],
    },
    "alimentation-durable": {
        "keywords": ["épicerie solidaire", "producteur local", "alimentation",
                      "bio", "circuit court"],
    },
    "centres-sante": {
        "keywords": ["maison de santé", "médecin", "urgence", "soin",
                      "pluridisciplinaire", "hôpital"],
    },
    "prevention-sante": {
        "keywords": ["prévention", "drogue", "santé publique", "information santé",
                      "renoncement aux soins", "bulletin municipal"],
    },
    "seniors": {
        "keywords": ["senior", "aîné", "âgé", "isolement", "maintien à domicile",
                      "restauration collective", "maison de l'âge"],
    },
    "budget-participatif": {
        "keywords": ["financement participatif", "budget participatif"],
    },
    "transparence": {
        "keywords": ["audit", "transparence", "finance", "subvention transparent",
                      "rapport public"],
    },
    "vie-associative": {
        "keywords": ["association", "bénévol", "subvention association",
                      "maison des associations"],
    },
    "services-publics": {
        "keywords": ["médiathèque", "service public", "adjoint", "compétence",
                      "guichet unique", "CCAS"],
    },
    "commerce-local": {
        "keywords": ["commerce", "marché", "commerçant", "consommer local",
                      "halles"],
    },
    "emploi-insertion": {
        "keywords": ["emploi", "insertion", "chômage", "formation professionnelle",
                      "France Travail", "stagiaire", "apprenti"],
    },
    "attractivite": {
        "keywords": ["filière", "excellence", "IA", "agroalimentaire", "cinéma",
                      "aéronautique", "attracti", "lycée international",
                      "data center économ"],
    },
    "equipements-culturels": {
        "keywords": ["kiosque", "médiathèque culture", "musée", "galerie",
                      "théâtre", "centre d'art", "bibliothèque culture",
                      "lieu culturel"],
    },
    "evenements-creation": {
        "keywords": ["festival", "concert", "talent", "artiste", "événement culturel",
                      "comité artistique", "création artistique"],
    },
    "equipements-sportifs": {
        "keywords": ["Cité du Sport", "équipement sportif", "stade", "salle de sport"],
    },
    "sport-pour-tous": {
        "keywords": ["sport école", "City Parc", "HandiPass sport", "Pass Montpellier Sport",
                      "Street Ball", "Futsal", "sport pour tous", "champion"],
    },
    "amenagement-urbain": {
        "keywords": ["urbanisme", "densification", "îlot", "schéma directeur",
                      "PLUI", "zone d'activité", "aménagement"],
    },
    "accessibilite": {
        "keywords": ["accessibilité", "handicap", "PMR", "fauteuil roulant",
                      "ascenseur", "monte-charge", "ERP"],
    },
    "quartiers-prioritaires": {
        "keywords": ["quartier prioritaire", "quartier", "cœur battant",
                      "place animée"],
    },
    "aide-sociale": {
        "keywords": ["CCAS", "sans abri", "domiciliation", "aide sociale",
                      "bénéficiaire", "accompagnement social"],
    },
    "egalite-discriminations": {
        "keywords": ["handicap inclusion", "autonomie handicap", "discrimination",
                      "égalité", "maison du handicap", "référent handicap"],
    },
    "pouvoir-achat": {
        "keywords": ["pouvoir d'achat", "TEOM", "facture", "eau", "énergie",
                      "chauffage", "compteur", "épicerie solidaire prix"],
    },
}


def load_text():
    """Charge le texte extrait du PDF."""
    with open(TEXTE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def extract_bullets(text):
    """Extrait toutes les mesures marquées par des bullets (•)."""
    mesures = []
    # Pattern : • suivi de texte jusqu'au prochain • ou fin de section
    lines = text.split("\n")
    current_bullet = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Détecter un nouveau bullet
        if line.startswith("•"):
            if current_bullet:
                mesures.append(clean_mesure(current_bullet))
            current_bullet = line[1:].strip()
        elif current_bullet is not None:
            # Continuation du bullet précédent si la ligne ne commence pas par
            # un titre en majuscules ou un marqueur de section
            if (line.isupper() and len(line) > 10) or line.startswith("==="):
                if current_bullet:
                    mesures.append(clean_mesure(current_bullet))
                current_bullet = None
            elif line.startswith("CONSTAT") or line.startswith("RÉSULTAT") or \
                 line.startswith("NOS SOLUTIONS") or line.startswith("NOTRE OBJECTIF"):
                if current_bullet:
                    mesures.append(clean_mesure(current_bullet))
                current_bullet = None
            else:
                current_bullet += " " + line

    if current_bullet:
        mesures.append(clean_mesure(current_bullet))

    return [m for m in mesures if m and len(m) >= 15]


def clean_mesure(text):
    """Nettoie une mesure."""
    text = re.sub(r"\s+", " ", text).strip()
    # Retirer les tirets en début
    text = re.sub(r"^[-–—]\s*", "", text)
    # Tronquer à max 300 chars
    if len(text) > 300:
        # Couper à la dernière phrase complète avant 300 chars
        idx = text[:300].rfind(".")
        if idx > 100:
            text = text[:idx + 1]
        else:
            text = text[:297] + "..."
    # Ajouter un point final si manquant
    if text and not text[-1] in ".!?)":
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
                # Bonus pour les mots-clés plus longs (plus spécifiques)
                if len(kw) > 10:
                    score += 0.5
        if score > best_score:
            best_score = score
            best_match = st_id

    return best_match, best_score


def main():
    print("=" * 60)
    print("  RÉ-EXTRACTION PERREIN (Montpellier)")
    print("=" * 60)
    print()

    # 1. Charger le texte PDF
    text = load_text()
    print(f"  Texte chargé : {len(text)} caractères")

    # 2. Extraire les bullets
    mesures = extract_bullets(text)
    print(f"  Bullets (•) extraits : {len(mesures)}")
    print()

    # 3. Classifier chaque mesure
    classified = {}  # st_id -> [mesures]
    unclassified = []

    for m in mesures:
        st_id, score = classify_mesure(m, SECTIONS_MAPPING)
        if st_id and score >= 1:
            if st_id not in classified:
                classified[st_id] = []
            classified[st_id].append(m)
        else:
            unclassified.append(m)

    print("  Classification :")
    for st_id in sorted(classified.keys()):
        print(f"    {st_id}: {len(classified[st_id])} mesures")

    if unclassified:
        print(f"\n  Non classifiées ({len(unclassified)}) :")
        for m in unclassified:
            print(f"    - {m[:80]}...")

    # 4. Charger le JSON et mettre à jour
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in classified and len(classified[st_id]) > 0:
                prop = st["propositions"].get("perrein")
                if prop is None:
                    prop = {}
                    st["propositions"]["perrein"] = prop

                old_count = len(prop.get("mesures", []))
                new_mesures = classified[st_id]

                # Ne remplacer que si on a plus de mesures ou si c'était un bloc monolithique
                if old_count <= 1 or len(new_mesures) > old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = "Programme officiel 2026 — Isabelle Perrein"
                    prop["sourceUrl"] = "https://isabelleperrein.fr"
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} → {len(new_mesures)} mesures")

    # 5. Sauvegarder
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total_mesures = sum(len(v) for v in classified.values())
    print(f"\n  RÉSULTAT : {total_mesures} mesures extraites, {updated} sous-thèmes mis à jour")
    print("=" * 60)


if __name__ == "__main__":
    main()
