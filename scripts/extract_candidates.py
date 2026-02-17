#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from pathlib import Path

# Configuration des sous-thèmes par catégorie
SOUS_THEMES = {
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

CANDIDATS = [
    ("vitry-sur-seine", "afflatet"),
    ("lille", "spillebout"),
    ("toulouse", "meilhac"),
    ("grenoble", "belaid"),
    ("antibes", "ducatel"),
]

def extract_propositions(text, ville, candidat):
    """Extract concrete propositions from crawled text."""
    propositions = {}

    if not text or len(text.strip()) == 0:
        return propositions

    # Patterns pour identifier les propositions concrètes
    # On cherche des lignes avec verbes d'action et des chiffres
    sentences = re.split(r'[.\n]', text)

    proposition_count = 0
    for sentence in sentences:
        sentence = sentence.strip()

        # Ignorer les phrases vides ou trop courtes
        if len(sentence) < 20 or len(sentence) > 500:
            continue

        # Ignorer les déclarations vagues sans chiffres ou détails concrets
        if not any(char.isdigit() for char in sentence) and not any(keyword in sentence.lower() for keyword in
                                                                       ["créer", "construire", "rénover", "augmenter", "développer", "renforcer", "mettre", "établir", "installer", "ouvrir"]):
            continue

        # Mapper aux sous-thèmes
        best_subtheme = None
        for categorie, subthemes in SOUS_THEMES.items():
            for subtheme in subthemes:
                if subtheme.replace("-", " ") in sentence.lower() or subtheme in sentence.lower():
                    best_subtheme = f"{categorie}/{subtheme}"
                    break
            if best_subtheme:
                break

        if best_subtheme and best_subtheme not in propositions:
            proposition_count += 1
            propositions[best_subtheme] = {
                "texte": sentence[:200],
                "source": f"Site officiel {candidat.capitalize()}",
                "sourceUrl": "",
            }

    return propositions

def process_candidate(ville, candidat):
    """Process a single candidate."""
    cache_path = Path(r"C:\Users\KOPELMANRon\Downloads\FR comp mun\scripts\crawl_cache") / f"{ville}_{candidat}.json"
    results_dir = Path(r"C:\Users\KOPELMANRon\Downloads\FR comp mun\scripts\crawl_results")
    results_dir.mkdir(exist_ok=True)

    results_file = results_dir / f"{ville}_{candidat}.json"

    print(f"\nTraitement: {ville}_{candidat}")
    print(f"Cache path: {cache_path}")
    print(f"Results file: {results_file}")

    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Chercher le contenu principal
        content = ""
        for key in ["content", "text", "body", "main"]:
            if key in data and isinstance(data[key], str):
                content = data[key]
                break

        # Si pas trouvé, prendre la plus grande clé string
        if not content:
            for key, value in data.items():
                if isinstance(value, str) and len(value) > len(content):
                    content = value

        print(f"Content length: {len(content)} chars")
        print(f"Content preview: {content[:200]}...")

        # Extraire les propositions
        propositions = extract_propositions(content, ville, candidat)
        print(f"Propositions found: {len(propositions)}")

        # Écrire le résultat
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(propositions, f, ensure_ascii=False, indent=2)

        print(f"✓ Résultat écrit dans {results_file}")
        return True

    except Exception as e:
        print(f"✗ Erreur: {e}")
        # Écrire un fichier vide en cas d'erreur
        results_file = results_dir / f"{ville}_{candidat}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return False

if __name__ == "__main__":
    print("="*80)
    print("Extraction des propositions des candidats")
    print("="*80)

    success_count = 0
    for ville, candidat in CANDIDATS:
        if process_candidate(ville, candidat):
            success_count += 1

    print(f"\n{'='*80}")
    print(f"Résumé: {success_count}/{len(CANDIDATS)} candidats traités avec succès")
    print(f"{'='*80}")
