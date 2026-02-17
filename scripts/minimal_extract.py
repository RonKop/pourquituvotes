#!/usr/bin/env python3
import json
import os
from pathlib import Path

SOUS_THEMES = {
    "police": "securite/police-municipale",
    "gendarme": "securite/police-municipale",
    "vidéo": "securite/videoprotection",
    "surveillance": "securite/videoprotection",
    "prévention": "securite/prevention-mediation",
    "médiation": "securite/prevention-mediation",
    "violences": "securite/violences-femmes",
    "transport": "transports/transports-en-commun",
    "bus": "transports/transports-en-commun",
    "tramway": "transports/transports-en-commun",
    "métro": "transports/transports-en-commun",
    "vélo": "transports/velo-mobilites-douces",
    "cyclable": "transports/velo-mobilites-douces",
    "mobilité": "transports/velo-mobilites-douces",
    "piéton": "transports/pietons-circulation",
    "marche": "transports/pietons-circulation",
    "stationnement": "transports/stationnement",
    "parking": "transports/stationnement",
    "tarif": "transports/tarifs-gratuite",
    "gratuit": "transports/tarifs-gratuite",
    "logement": "logement/logement-social",
    "habitation": "logement/logement-social",
    "maison": "logement/logement-social",
    "immeuble": "logement/logement-social",
    "loyer": "logement/encadrement-loyers",
    "locataire": "logement/encadrement-loyers",
    "vacant": "logement/logements-vacants",
    "école": "education/ecoles-renovation",
    "éducation": "education/ecoles-renovation",
    "crèche": "education/petite-enfance",
    "cantine": "education/cantines-fournitures",
    "périscolaire": "education/periscolaire-loisirs",
    "jeunesse": "education/jeunesse",
    "enfant": "education/jeunesse",
    "espace vert": "environnement/espaces-verts",
    "parc": "environnement/espaces-verts",
    "jardin": "environnement/espaces-verts",
    "arbre": "environnement/espaces-verts",
    "propreté": "environnement/proprete-dechets",
    "déchet": "environnement/proprete-dechets",
    "climat": "environnement/climat-adaptation",
    "rénovation": "environnement/renovation-energetique",
    "énergie": "environnement/renovation-energetique",
    "alimentation": "environnement/alimentation-durable",
    "centre santé": "sante/centres-sante",
    "hôpital": "sante/centres-sante",
    "médecin": "sante/centres-sante",
    "senior": "sante/seniors",
    "retraité": "sante/seniors",
    "budget participatif": "democratie/budget-participatif",
    "citoyen": "democratie/transparence",
    "transparence": "democratie/transparence",
    "association": "democratie/vie-associative",
    "services publics": "democratie/services-publics",
    "commerce": "economie/commerce-local",
    "emploi": "economie/emploi-insertion",
    "travail": "economie/emploi-insertion",
    "insertion": "economie/emploi-insertion",
    "attractivité": "economie/attractivite",
    "équipement culturel": "culture/equipements-culturels",
    "musée": "culture/equipements-culturels",
    "théâtre": "culture/equipements-culturels",
    "bibliothèque": "culture/equipements-culturels",
    "événement": "culture/evenements-creation",
    "festival": "culture/evenements-creation",
    "création": "culture/evenements-creation",
    "équipement sportif": "sport/equipements-sportifs",
    "gymnase": "sport/equipements-sportifs",
    "stade": "sport/equipements-sportifs",
    "piscine": "sport/equipements-sportifs",
    "aménagement": "urbanisme/amenagement-urbain",
    "urbanisme": "urbanisme/amenagement-urbain",
    "quartier": "urbanisme/quartiers-prioritaires",
    "rue": "urbanisme/amenagement-urbain",
    "accessibilité": "urbanisme/accessibilite",
    "aide": "solidarite/aide-sociale",
    "égalité": "solidarite/egalite-discriminations",
    "discrimination": "solidarite/egalite-discriminations",
    "pouvoir d'achat": "solidarite/pouvoir-achat",
}

def find_best_subtheme(text):
    lower = text.lower()
    scores = {}
    for keyword, subtheme in SOUS_THEMES.items():
        if keyword in lower:
            scores[subtheme] = scores.get(subtheme, 0) + 1
    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    return None

def is_concrete(text):
    if not text or len(text) < 20 or len(text) > 400:
        return False
    lower = text.lower()
    has_number = any(c.isdigit() for c in text)
    has_action = any(word in lower for word in [
        "créer", "construire", "rénover", "augmenter", "développer",
        "renforcer", "mettre", "établir", "installer", "ouvrir",
        "améliorer", "transformer", "lancer", "déployer"
    ])
    return has_number or has_action

def extract(cache_file):
    propositions = {}
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        all_text = []
        if data.get('pages') and isinstance(data['pages'], list):
            for page in data['pages']:
                if page.get('text'):
                    all_text.append(page['text'])

        combined = '\n\n'.join(all_text)
        sentences = combined.split('\n')

        count = 0
        for sent in sentences:
            if count >= 20:
                break
            sent = sent.strip()
            if is_concrete(sent):
                subtheme = find_best_subtheme(sent)
                if subtheme and subtheme not in propositions:
                    propositions[subtheme] = {
                        "texte": sent[:200],
                        "source": f"Site officiel {data.get('nom', '')}",
                        "sourceUrl": data.get('url', '')
                    }
                    count += 1
    except Exception as e:
        print(f"Erreur: {e}")

    return propositions

# Traiter les 5 candidats
candidates = [
    ('vitry-sur-seine', 'afflatet'),
    ('lille', 'spillebout'),
    ('toulouse', 'meilhac'),
    ('grenoble', 'belaid'),
    ('antibes', 'ducatel'),
]

base_path = Path(r"C:\Users\KOPELMANRon\Downloads\FR comp mun\scripts")
cache_dir = base_path / "crawl_cache"
results_dir = base_path / "crawl_results"

results_dir.mkdir(exist_ok=True)

print("=" * 80)
print("Extraction des propositions")
print("=" * 80)

total = 0
for ville, candidat in candidates:
    cache_file = cache_dir / f"{ville}_{candidat}.json"
    result_file = results_dir / f"{ville}_{candidat}.json"

    props = extract(str(cache_file))
    total += len(props)

    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(props, f, ensure_ascii=False, indent=2)

    print(f"✓ {ville}/{candidat}: {len(props)} propositions")

print("=" * 80)
print(f"Total: {total} propositions")
print("=" * 80)
