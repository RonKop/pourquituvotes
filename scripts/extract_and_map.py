#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract concrete propositions from crawl cache JSON files and map to sub-themes.
"""

import json
import os
from pathlib import Path

# Define sub-themes
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

CANDIDATES = [
    ("caen", "lecoutour", "Xavier Le Coutour"),
    ("la-rochelle", "batcabe", "Christophe Batcabé"),
    ("quimper", "assih", "Isabelle Assih"),
    ("mulhouse", "minery", "Loïc Minery"),
    ("toulouse", "cottrel", "Arthur Cottrel"),
    ("amiens", "caron", "Aurélien Caron"),
    ("lille", "spillebout", "Violette Spillebout"),
]

def extract_propositions_from_text(text, candidate_name):
    """
    Extract concrete propositions from raw text.
    Look for numbered lists, bullets, and specific action items with numbers/metrics.
    """
    propositions = []

    # Split into lines for processing
    lines = text.split('\n')

    # Collect candidate propositions
    current_prop = ""
    for line in lines:
        line = line.strip()

        # Skip empty lines and certain metadata
        if not line or line.startswith("---") or line.startswith("http"):
            if current_prop:
                propositions.append(current_prop.strip())
                current_prop = ""
            continue

        # Look for bullet points and numbered items
        if line.startswith('⊲') or line.startswith('•') or line.startswith('-'):
            if current_prop:
                propositions.append(current_prop.strip())
            current_prop = line[1:].strip()
        elif line.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')) and len(line) > 2 and line[1] in ('.', ')'):
            if current_prop:
                propositions.append(current_prop.strip())
            current_prop = line[2:].strip()
        elif current_prop and not line.startswith(('Toulouse', 'Lille', 'Amiens', 'Mulhouse', 'Caen', 'Quimper', 'La Rochelle', 'Page', 'Ne pas')):
            # Continue previous proposition
            current_prop += " " + line

    if current_prop:
        propositions.append(current_prop.strip())

    # Filter for concrete propositions (with numbers, metrics, or specific actions)
    concrete_props = []
    for prop in propositions:
        # Filter out very short or generic propositions
        if len(prop) < 15:
            continue
        # Keep if it has numbers, specific actions, or concrete details
        if any(c.isdigit() for c in prop) or "créer" in prop.lower() or "augmenter" in prop.lower() or "mettre" in prop.lower() or "développer" in prop.lower() or "installer" in prop.lower() or "rénover" in prop.lower():
            concrete_props.append(prop)

    return concrete_props

def map_to_subtheme(proposition, candidate_name):
    """
    Map a proposition to a sub-theme based on keywords.
    Returns (categorie/sous-theme, a_verifier_flag)
    """
    prop_lower = proposition.lower()

    # Keywords for each sub-theme
    keyword_map = {
        "police-municipale": ["police municipal", "police de proximité", "police terrasse", "îlotage"],
        "videoprotection": ["vidéoprotection", "caméra", "caméras", "surveillance"],
        "prevention-mediation": ["prévention", "médiation", "jeunesse", "incivilité"],
        "violences-femmes": ["violence", "femme", "féminicide", "viol", "agression sexuelle"],

        "transports-en-commun": ["transports en commun", "bus", "tram", "navette", "ter", "gratuit transport"],
        "velo-mobilites-douces": ["vélo", "piste cyclable", "véloibus", "mobilités douces", "cyclable"],
        "pietons-circulation": ["piéton", "circulation", "rue scolaire", "apaisement", "trottoir"],
        "stationnement": ["stationnement", "parking", "zone bleue"],
        "tarifs-gratuite": ["gratuité", "tarification", "réduit", "abonnement"],

        "logement-social": ["logement social", "hlm", "bail réel solidaire", "brs"],
        "logements-vacants": ["logements vacants", "squat", "inoccupé", "permis de louer"],
        "encadrement-loyers": ["loyer", "encadrement", "propriétaire", "locataire"],
        "acces-logement": ["accès au logement", "familles monoparentales"],

        "petite-enfance": ["crèche", "pouponnière", "assistante maternelle", "atsem", "enfants"],
        "ecoles-renovation": ["école", "rénovation", "bâtiments scolaires", "scolarité"],
        "cantines-fournitures": ["cantine", "fournitures", "repas", "restauration scolaire"],
        "periscolaire-loisirs": ["périscolaire", "loisirs", "centre de loisirs", "activités"],
        "jeunesse": ["jeunesse", "jeunes", "conseil municipal des jeunes"],

        "espaces-verts": ["parc", "jardin", "espace vert", "végétal", "arbre", "plantations"],
        "proprete-dechets": ["propreté", "nettoyage", "déchet", "tri", "poubelle"],
        "climat-adaptation": ["climatique", "climat", "réchauffement", "submersion", "inondation"],
        "renovation-energetique": ["rénovation", "énergétique", "énergie", "chauffage", "thermique"],
        "alimentation-durable": ["alimentation", "bio", "local", "circuit court", "fermier"],

        "centres-sante": ["santé", "médecin", "cabinet", "centre de santé", "hôpital"],
        "prevention-sante": ["prévention", "mutuelle", "ordonnance verte", "santé mentale"],
        "seniors": ["seniors", "aînés", "vieillissement", "ehpad", "maison de retraite"],

        "budget-participatif": ["budget participatif", "consultatif"],
        "transparence": ["transparence", "communication", "conseil municipal"],
        "vie-associative": ["association", "tissu associatif", "bénévole"],
        "services-publics": ["service public", "guichet", "dématérialisation"],

        "commerce-local": ["commerce", "commerçant", "artisan", "petit commerce", "indépendant"],
        "emploi-insertion": ["emploi", "chômage", "insertion", "formation"],
        "attractivite": ["attractivité", "économie", "entreprise", "investissement", "développement"],

        "equipements-culturels": ["musée", "théâtre", "cinéma", "bibliothèque", "salle de concert"],
        "evenements-creation": ["événement", "festival", "spectacle", "création artistique"],

        "equipements-sportifs": ["stade", "gymnase", "piscine", "court", "équipement sportif"],
        "sport-pour-tous": ["sport", "activité physique", "loisir sportif"],

        "amenagement-urbain": ["urbanisme", "aménagement", "quartier", "requalification", "friche"],
        "accessibilite": ["accessibilité", "handicap", "pmr", "obstacle"],
        "quartiers-prioritaires": ["quartier prioritaire", "quartier nord", "quartier politique de la ville"],

        "aide-sociale": ["aide sociale", "solidarité", "précarité", "sans-abri", "rsa"],
        "egalite-discriminations": ["égalité", "discrimination", "inclusio", "lgbtq", "racisé"],
        "pouvoir-achat": ["pouvoir d'achat", "crise", "tarification", "solidaire"],
    }

    # Try to find matching sub-theme
    best_match = None
    best_score = 0

    for subtheme, keywords in keyword_map.items():
        score = 0
        for keyword in keywords:
            if keyword in prop_lower:
                score += len(keyword.split())

        if score > best_score:
            best_score = score
            best_match = subtheme

    # Return result
    if best_match:
        categorie = [k for k, v in SOUS_THEMES.items() if best_match in v][0]
        return f"{categorie}/{best_match}", False

    # Could not clearly map
    return None, True

def process_candidate(ville_id, candidat_id, nom):
    """Process a single candidate's crawl cache file."""
    cache_file = f"crawl_cache/{ville_id}_{candidat_id}.json"

    if not os.path.exists(cache_file):
        print(f"ERROR: {cache_file} not found")
        return {}

    print(f"\nProcessing {nom} ({ville_id}/{candidat_id})...")

    with open(cache_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Combine all text from pages and PDFs
    all_text = ""
    source_info = ""

    for page in data.get('pages', []):
        all_text += page.get('text', '') + "\n"
        if not source_info and page.get('url'):
            source_info = f"Site officiel: {page.get('url', '')}"

    for pdf in data.get('pdfs', []):
        all_text += pdf.get('text', '') + "\n"
        if not source_info and pdf.get('url'):
            source_info = f"Programme PDF: {pdf.get('url', '')}"

    # Extract propositions
    propositions = extract_propositions_from_text(all_text, nom)
    print(f"  Extracted {len(propositions)} potential propositions")

    # Map to sub-themes
    result = {}
    mapped_count = 0

    for prop in propositions:
        subtheme, needs_check = map_to_subtheme(prop, nom)

        if subtheme:
            # Truncate to 2 sentences max (~150-200 chars)
            prop_text = prop[:200]
            if len(prop) > 200:
                prop_text += "..."

            key = subtheme
            result[key] = {
                "texte": prop_text,
                "source": "Site officiel" if "pages" in data else "Programme PDF",
                "sourceUrl": data.get('url', '')
            }
            if needs_check:
                result[key]["a_verifier"] = True
            mapped_count += 1

    print(f"  Mapped {mapped_count} propositions to sub-themes")

    return result

# Main
def main():
    """Process all 7 candidates."""
    os.chdir(Path(__file__).parent)

    for ville_id, candidat_id, nom in CANDIDATES:
        result = process_candidate(ville_id, candidat_id, nom)

        # Write result
        output_file = f"crawl_results/{ville_id}_{candidat_id}.json"
        os.makedirs("crawl_results", exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"  Wrote {len(result)} entries to {output_file}")

if __name__ == "__main__":
    main()
