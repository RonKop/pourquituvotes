#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#POURQUITUVOTES — Extracteur de propositions semi-automatique

Workflow en 3 étapes :
  1. EXTRACT : PDF/URL -> texte -> prompt prêt à coller dans Claude.ai
  2. (Manuel) : coller le prompt, récupérer la réponse JSON de Claude
  3. IMPORT  : réponse JSON de Claude -> validation -> insertion dans l'élection JSON

Usage :
  # Étape 1 : générer le prompt depuis un PDF
  python scripts/extraire_propositions.py extract --pdf data/programmes/clermont-bianchi.pdf --ville clermont --candidat bianchi

  # Étape 1 bis : depuis une URL
  python scripts/extraire_propositions.py extract --url https://bianchi2026.fr/programme --ville clermont --candidat bianchi

  # Étape 3 : importer la réponse de Claude
  python scripts/extraire_propositions.py import --reponse reponse_claude.json --ville clermont --candidat bianchi

  # Voir les candidats sans propositions
  python scripts/extraire_propositions.py status --ville clermont
"""

import argparse
import json
import os
import re
import sys
import textwrap
from datetime import datetime

# === Dépendances optionnelles ===
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# === Chemins ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
PROGRAMMES_DIR = os.path.join(DATA_DIR, "programmes")
SCHEMA_PATH = os.path.join(DATA_DIR, "schema", "schema_elections.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "scripts", "prompts_generated")


def load_schema():
    """Charge le schéma des catégories/sous-thèmes."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_election(ville_id):
    """Charge le JSON d'une élection."""
    path = os.path.join(ELECTIONS_DIR, f"{ville_id}-2026.json")
    if not os.path.exists(path):
        print(f"Erreur : fichier introuvable -> {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), path


def get_candidate_info(election, candidat_id):
    """Récupère les infos d'un candidat."""
    for c in election.get("candidats", []):
        if c["id"] == candidat_id:
            return c
    return None


# === Extraction de texte ===

def extract_text_from_pdf(pdf_path):
    """Extrait le texte d'un PDF avec PyMuPDF."""
    if not HAS_PYMUPDF:
        print("Erreur : PyMuPDF non installé. pip install PyMuPDF")
        sys.exit(1)
    if not os.path.exists(pdf_path):
        print(f"Erreur : PDF introuvable -> {pdf_path}")
        sys.exit(1)

    doc = fitz.open(pdf_path)
    pages = []
    page_count = len(doc)
    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            pages.append(f"--- PAGE {i+1} ---\n{text.strip()}")
    doc.close()

    full_text = "\n\n".join(pages)
    print(f"  PDF : {page_count} pages, {len(full_text)} caracteres extraits")
    return full_text


def extract_text_from_url(url):
    """Extrait le texte d'une page web."""
    if not HAS_REQUESTS:
        print("Erreur : requests/bs4 non installés. pip install requests beautifulsoup4")
        sys.exit(1)

    print(f"  Téléchargement de {url}...")
    resp = requests.get(url, timeout=15, headers={
        "User-Agent": "PourQuiTuVotes-Extractor/1.0"
    })
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Supprimer les éléments non pertinents
    for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # Extraire le texte du body
    body = soup.find("body")
    if not body:
        body = soup

    text = body.get_text(separator="\n", strip=True)
    # Nettoyer les lignes vides multiples
    text = re.sub(r"\n{3,}", "\n\n", text)

    print(f"  Page web : {len(text)} caractères extraits")
    return text


# === Génération du prompt ===

def build_prompt(text, ville_nom, candidat_nom, candidat_liste, source_label, schema):
    """Construit le prompt optimisé pour Claude.ai."""

    # Construire la liste des sous-thèmes
    themes_text = ""
    for cat in schema["categories"]:
        themes_text += f"\n### {cat['id']} — {cat['nom']}\n"
        for st in cat["sousThemes"]:
            themes_text += f"- `{cat['id']}/{st['id']}` -> {st['nom']}\n"

    # Tronquer le texte si trop long (Claude.ai a une limite)
    max_chars = 80000
    if len(text) > max_chars:
        text = text[:max_chars] + f"\n\n[... TRONQUÉ — {len(text) - max_chars} caractères restants]"

    prompt = f"""Tu es un assistant spécialisé dans l'analyse de programmes électoraux municipaux français.

## Ta mission

Extraire TOUTES les propositions concrètes du texte ci-dessous et les classer dans les sous-thèmes prédéfinis.

## Candidat
- **Nom** : {candidat_nom}
- **Liste** : {candidat_liste}
- **Ville** : {ville_nom}
- **Source** : {source_label}

## Les 12 catégories et 44 sous-thèmes
{themes_text}

## Règles STRICTES

1. **UNE mesure = UN seul sous-thème** (pas de doublons)
2. **Résumé fidèle** : reformule de façon concise mais garde les chiffres, montants, délais
3. **Regroupe** les mesures qui concernent le même sous-thème en UN seul texte (séparées par ". ")
4. **Source** : indique la page du PDF ou la section du site web
5. **Si une mesure ne rentre dans aucun sous-thème existant**, propose un nouveau sous-thème spécifique à la ville avec le format `categorie/nouveau-sous-theme`
6. **N'invente rien** : si le texte ne mentionne pas un thème, ne le remplis pas
7. **Inclus les petites mesures** : même une mention brève d'un sujet compte

## Format de sortie OBLIGATOIRE (JSON)

Réponds UNIQUEMENT avec ce JSON, sans texte autour :

```json
{{
  "propositions": {{
    "securite/police-municipale": {{
      "texte": "Résumé concis de la/des proposition(s) sur ce sous-thème",
      "source": "Programme officiel p. X"
    }},
    "transports/velo-mobilites-douces": {{
      "texte": "...",
      "source": "Programme officiel p. Y"
    }}
  }},
  "sous_themes_specifiques": [
    {{
      "id": "categorie/nouveau-id",
      "nom": "Nom du nouveau sous-thème",
      "texte": "...",
      "source": "..."
    }}
  ],
  "stats": {{
    "total_propositions": 25,
    "categories_couvertes": 8,
    "mesures_ignorees": "Liste de mesures qui ne rentrent nulle part (si applicable)"
  }}
}}
```

## TEXTE DU PROGRAMME À ANALYSER

{text}
"""
    return prompt


# === Import de la réponse Claude ===

def parse_claude_response(response_path):
    """Parse la réponse JSON de Claude (depuis un fichier)."""
    with open(response_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Essayer de trouver le JSON dans le texte (Claude met parfois du texte autour)
    # Chercher le bloc ```json ... ```
    json_match = re.search(r"```json\s*\n?(.*?)\n?```", content, re.DOTALL)
    if json_match:
        content = json_match.group(1)

    # Ou chercher directement un objet JSON
    if not content.strip().startswith("{"):
        # Chercher le premier { et le dernier }
        start = content.find("{")
        end = content.rfind("}")
        if start >= 0 and end > start:
            content = content[start:end+1]

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Erreur JSON : {e}")
        print("Astuce : copie la réponse de Claude dans un fichier .json et vérifie le format")
        sys.exit(1)

    return data


def validate_propositions(data, schema):
    """Valide les propositions extraites par Claude."""
    # Construire le set de sous-thèmes valides
    valid_keys = set()
    for cat in schema["categories"]:
        for st in cat["sousThemes"]:
            valid_keys.add(f"{cat['id']}/{st['id']}")

    props = data.get("propositions", {})
    errors = []
    warnings = []
    valid_props = {}

    for key, val in props.items():
        if key not in valid_keys:
            warnings.append(f"  Sous-thème inconnu : {key} (sera ignoré, à ajouter comme spécifique ?)")
            continue
        if not val or not val.get("texte"):
            warnings.append(f"  Proposition vide pour {key}")
            continue
        if len(val["texte"]) < 10:
            warnings.append(f"  Proposition très courte pour {key} : '{val['texte']}'")
        valid_props[key] = val

    # Sous-thèmes spécifiques
    specifics = data.get("sous_themes_specifiques", [])

    # Stats
    stats = data.get("stats", {})

    return valid_props, specifics, stats, errors, warnings


def import_propositions(election, election_path, candidat_id, valid_props, source_url, specifics=None):
    """Insère les propositions dans le JSON d'élection."""
    candidat = get_candidate_info(election, candidat_id)
    if not candidat:
        print(f"Erreur : candidat '{candidat_id}' introuvable dans l'élection")
        sys.exit(1)

    inserted = 0
    updated = 0

    for cat in election["categories"]:
        for st in cat["sousThemes"]:
            key = f"{cat['id']}/{st['id']}"
            if key in valid_props:
                prop = valid_props[key]
                existing = st["propositions"].get(candidat_id)

                new_prop = {
                    "texte": prop["texte"],
                    "source": prop.get("source", "Programme officiel"),
                    "sourceUrl": source_url or candidat.get("programmeUrl", "#")
                }

                if existing and existing is not None:
                    # Mise à jour
                    st["propositions"][candidat_id] = new_prop
                    updated += 1
                else:
                    # Insertion
                    st["propositions"][candidat_id] = new_prop
                    inserted += 1

    # Ajouter les sous-thèmes spécifiques si besoin
    added_specifics = 0
    if specifics:
        for spec in specifics:
            spec_id = spec.get("id", "")
            if "/" not in spec_id:
                continue
            cat_id, st_id = spec_id.split("/", 1)

            # Trouver la catégorie
            target_cat = None
            for cat in election["categories"]:
                if cat["id"] == cat_id:
                    target_cat = cat
                    break

            if not target_cat:
                print(f"  Catégorie inconnue pour sous-thème spécifique : {cat_id}")
                continue

            # Vérifier si le sous-thème existe déjà
            exists = any(st["id"] == st_id for st in target_cat["sousThemes"])
            if not exists:
                # Créer le sous-thème avec des propositions null pour tous les candidats
                new_st = {
                    "id": st_id,
                    "nom": spec.get("nom", st_id),
                    "propositions": {}
                }
                for c in election["candidats"]:
                    new_st["propositions"][c["id"]] = None
                # Ajouter la proposition pour ce candidat
                new_st["propositions"][candidat_id] = {
                    "texte": spec["texte"],
                    "source": spec.get("source", "Programme officiel"),
                    "sourceUrl": source_url or candidat.get("programmeUrl", "#")
                }
                target_cat["sousThemes"].append(new_st)
                added_specifics += 1
                print(f"  + Nouveau sous-thème spécifique : {spec_id} ({spec.get('nom', '')})")

    # Sauvegarder
    with open(election_path, "w", encoding="utf-8") as f:
        json.dump(election, f, ensure_ascii=False, indent=2)

    return inserted, updated, added_specifics


# === Status : voir ce qui manque ===

def show_status(election, ville_id):
    """Affiche le status des propositions par candidat."""
    candidats = election.get("candidats", [])
    print(f"\n{'='*60}")
    print(f"  {election.get('ville', ville_id)} — Status des propositions")
    print(f"{'='*60}\n")

    # Compter les propositions par candidat
    counts = {c["id"]: {"filled": 0, "total": 0, "nom": c["nom"]} for c in candidats}

    for cat in election.get("categories", []):
        for st in cat.get("sousThemes", []):
            for cid in counts:
                counts[cid]["total"] += 1
                prop = st.get("propositions", {}).get(cid)
                if prop and prop is not None and prop.get("texte"):
                    counts[cid]["filled"] += 1

    for cid, info in counts.items():
        pct = round(info["filled"] / info["total"] * 100) if info["total"] > 0 else 0
        complet = next((c.get("programmeComplet", False) for c in candidats if c["id"] == cid), False)
        bar = "#" * (pct // 5) + "." * (20 - pct // 5)
        tag = " [complet]" if complet else ""
        print(f"  {info['nom']:25s} {bar} {info['filled']:3d}/{info['total']} ({pct}%){tag}")

    # Catégories les moins couvertes
    print(f"\n  Catégories les moins couvertes :")
    cat_stats = []
    for cat in election.get("categories", []):
        filled = 0
        total = 0
        for st in cat.get("sousThemes", []):
            for cid in counts:
                total += 1
                prop = st.get("propositions", {}).get(cid)
                if prop and prop is not None:
                    filled += 1
        cat_stats.append((cat["nom"], filled, total))

    cat_stats.sort(key=lambda x: x[1] / x[2] if x[2] > 0 else 0)
    for nom, filled, total in cat_stats[:5]:
        pct = round(filled / total * 100) if total > 0 else 0
        print(f"    {nom:40s} {filled}/{total} ({pct}%)")


# === Main ===

def cmd_extract(args):
    """Commande extract : PDF/URL -> prompt."""
    schema = load_schema()
    election, _ = load_election(args.ville)
    candidat = get_candidate_info(election, args.candidat)

    if not candidat:
        print(f"Erreur : candidat '{args.candidat}' introuvable dans {args.ville}")
        print(f"  Candidats disponibles : {', '.join(c['id'] for c in election['candidats'])}")
        sys.exit(1)

    # Extraire le texte
    if args.pdf:
        # Chercher le PDF dans data/programmes/ si chemin relatif
        pdf_path = args.pdf
        if not os.path.isabs(pdf_path):
            alt = os.path.join(PROGRAMMES_DIR, pdf_path)
            if os.path.exists(alt):
                pdf_path = alt
        text = extract_text_from_pdf(pdf_path)
        source_label = f"Programme PDF ({os.path.basename(pdf_path)})"
    elif args.url:
        text = extract_text_from_url(args.url)
        source_label = f"Site web ({args.url})"
    else:
        print("Erreur : spécifie --pdf ou --url")
        sys.exit(1)

    # Construire le prompt
    prompt = build_prompt(
        text=text,
        ville_nom=election.get("ville", args.ville),
        candidat_nom=candidat["nom"],
        candidat_liste=candidat.get("liste", ""),
        source_label=source_label,
        schema=schema
    )

    # Sauvegarder le prompt
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"prompt_{args.ville}_{args.candidat}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    # Aussi copier dans le presse-papier si possible
    try:
        import subprocess
        process = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
        process.communicate(prompt.encode("utf-16-le"))
        clipboard_ok = True
    except Exception:
        clipboard_ok = False

    print(f"\n{'='*60}")
    print(f"  PROMPT GÉNÉRÉ")
    print(f"{'='*60}")
    print(f"  Candidat  : {candidat['nom']} ({candidat.get('liste', '')})")
    print(f"  Ville     : {election.get('ville', args.ville)}")
    print(f"  Source    : {source_label}")
    print(f"  Texte     : {len(text)} caractères")
    print(f"  Prompt    : {len(prompt)} caractères")
    print(f"  Fichier   : {output_path}")
    if clipboard_ok:
        print(f"  Presse-papier : copié !")
    print(f"\n  -> Colle ce prompt dans Claude.ai")
    print(f"  -> Copie la réponse JSON dans un fichier (ex: reponse.json)")
    print(f"  -> Lance : python scripts/extraire_propositions.py import --reponse reponse.json --ville {args.ville} --candidat {args.candidat}")


def cmd_import(args):
    """Commande import : réponse Claude -> insertion."""
    schema = load_schema()
    election, election_path = load_election(args.ville)
    candidat = get_candidate_info(election, args.candidat)

    if not candidat:
        print(f"Erreur : candidat '{args.candidat}' introuvable dans {args.ville}")
        sys.exit(1)

    # Parser la réponse
    print(f"  Lecture de {args.reponse}...")
    data = parse_claude_response(args.reponse)

    # Valider
    print(f"  Validation des propositions...")
    valid_props, specifics, stats, errors, warnings = validate_propositions(data, schema)

    if errors:
        print(f"\n  ERREURS :")
        for e in errors:
            print(f"    {e}")
        sys.exit(1)

    if warnings:
        print(f"\n  AVERTISSEMENTS :")
        for w in warnings:
            print(f"    {w}")

    print(f"\n  Propositions valides : {len(valid_props)}")
    if specifics:
        print(f"  Sous-thèmes spécifiques : {len(specifics)}")
    if stats:
        print(f"  Stats Claude : {stats}")

    # Confirmer
    if not args.yes:
        print(f"\n  Insérer {len(valid_props)} propositions pour {candidat['nom']} dans {args.ville} ?")
        confirm = input("  [O/n] > ").strip().lower()
        if confirm and confirm != "o" and confirm != "oui" and confirm != "y":
            print("  Annulé.")
            return

    # Insérer
    source_url = args.source_url or candidat.get("programmeUrl", "#")
    inserted, updated, added_spec = import_propositions(
        election, election_path, args.candidat, valid_props, source_url, specifics
    )

    # Mettre à jour programmeComplet si assez de propositions
    if len(valid_props) >= 15 and not candidat.get("programmeComplet"):
        candidat["programmeComplet"] = True
        with open(election_path, "w", encoding="utf-8") as f:
            json.dump(election, f, ensure_ascii=False, indent=2)
        print(f"  -> programmeComplet mis à true ({len(valid_props)} propositions)")

    print(f"\n{'='*60}")
    print(f"  IMPORT TERMINÉ")
    print(f"{'='*60}")
    print(f"  Candidat           : {candidat['nom']}")
    print(f"  Propositions ajoutées : {inserted}")
    print(f"  Propositions maj      : {updated}")
    if added_spec:
        print(f"  Sous-thèmes ajoutés   : {added_spec}")
    print(f"  Fichier : {election_path}")
    print(f"\n  -> Lance : python scripts/valider_donnees.py  pour vérifier")


def cmd_status(args):
    """Commande status : voir les propositions manquantes."""
    if args.ville == "all":
        # Toutes les villes
        for f in sorted(os.listdir(ELECTIONS_DIR)):
            if f.endswith("-2026.json"):
                ville_id = f.replace("-2026.json", "")
                election, _ = load_election(ville_id)
                show_status(election, ville_id)
    else:
        election, _ = load_election(args.ville)
        show_status(election, args.ville)


def main():
    parser = argparse.ArgumentParser(
        description="Extracteur de propositions semi-automatique",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
Exemples :
  # Générer le prompt depuis un PDF
  python scripts/extraire_propositions.py extract --pdf clermont-bianchi.pdf --ville clermont --candidat bianchi

  # Générer le prompt depuis une URL
  python scripts/extraire_propositions.py extract --url https://bianchi2026.fr --ville clermont --candidat bianchi

  # Importer la réponse de Claude
  python scripts/extraire_propositions.py import --reponse reponse.json --ville clermont --candidat bianchi

  # Voir le status d'une ville
  python scripts/extraire_propositions.py status --ville clermont

  # Voir le status de toutes les villes
  python scripts/extraire_propositions.py status --ville all
        """)
    )

    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")

    # extract
    p_extract = subparsers.add_parser("extract", help="Extraire texte et générer le prompt")
    p_extract.add_argument("--pdf", help="Chemin vers le PDF du programme")
    p_extract.add_argument("--url", help="URL de la page programme")
    p_extract.add_argument("--ville", required=True, help="ID de la ville (ex: clermont, paris)")
    p_extract.add_argument("--candidat", required=True, help="ID du candidat (ex: bianchi)")

    # import
    p_import = subparsers.add_parser("import", help="Importer la réponse JSON de Claude")
    p_import.add_argument("--reponse", required=True, help="Fichier JSON de la réponse de Claude")
    p_import.add_argument("--ville", required=True, help="ID de la ville")
    p_import.add_argument("--candidat", required=True, help="ID du candidat")
    p_import.add_argument("--source-url", help="URL source (défaut: programmeUrl du candidat)")
    p_import.add_argument("--yes", "-y", action="store_true", help="Pas de confirmation")

    # status
    p_status = subparsers.add_parser("status", help="Voir le status des propositions")
    p_status.add_argument("--ville", required=True, help="ID de la ville (ou 'all')")

    args = parser.parse_args()

    if args.command == "extract":
        cmd_extract(args)
    elif args.command == "import":
        cmd_import(args)
    elif args.command == "status":
        cmd_status(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
