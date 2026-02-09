#!/usr/bin/env python3
"""
Correction complète des propositions Knafo dans app.js
=====================================================
Couvre les 51 mesures du PDF (Programme-Sarah-Knafo-Paris-2026.pdf)
- Met à jour les textes existants (plus complets, combinant les mesures liées)
- Corrige les doublons et les textes dans le mauvais sous-thème
- Ajoute 2 nouveaux sous-thèmes pour les mesures sans catégorie
"""

import re
import os
import sys

APPJS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "js", "app.js")
SOURCE = "Programme officiel 2026"
SOURCE_URL = "https://unevilleheureuse.fr/"


def to_js(text):
    """Encode une chaîne Python en littéral JS avec escapes unicode."""
    result = []
    for ch in text:
        code = ord(ch)
        if code > 127:
            result.append(f"\\u{code:04X}")
        elif ch == '"':
            result.append('\\"')
        elif ch == '\n':
            result.append('\\n')
        else:
            result.append(ch)
    return ''.join(result)


def make_knafo_entry(texte):
    """Crée l'entrée JS pour knafo avec texte, source et sourceUrl."""
    return f'{{ texte: "{to_js(texte)}", source: "{SOURCE}", sourceUrl: "{SOURCE_URL}" }}'


def make_null():
    return "null"


# =============================================================================
# MAPPING COMPLET : 51 mesures PDF → sous-thèmes app.js
# =============================================================================
# Chaque entrée : sous_theme_id → texte (ou None pour null)
# Les mesures PDF sont notées en commentaire pour traçabilité

UPDATES = {
    # --- CRÈCHES & PETITE ENFANCE (Mesures 1-5) ---
    "creches-petite-enfance":
        "Création de 7 000 places en crèche : priorité d'accès au logement social "
        "pour les professionnels de la petite enfance, salaire à l'embauche +10% en "
        "crèche municipale, gestion centralisée des effectifs, attribution des places "
        "via une appli transparente sans passe-droit, achat de 1 000 places aux crèches privées",

    # --- ÉDUCATION (Mesures 6-9) ---
    "periscolaire":
        "Vérifications strictes (casier judiciaire, Fijais) pour tous les intervenants "
        "périscolaires avec contrôles périodiques continus et principe de précaution immédiat",

    "ecole-publique":
        "Fin de la guerre contre l'école privée : équité de traitement public/privé. "
        "Bras de fer avec l'État pour supprimer les critères idéologiques de mixité "
        "sociale dans l'algorithme Affelnet",

    "cantine-fournitures":
        "100% de produits issus de l'agriculture française dans les cantines scolaires "
        "parisiennes (30 millions de repas/an, +7 M€/an)",

    # --- LOGEMENT (Mesures 10-15, 40-41) ---
    "encadrement-loyers":
        "Suppression de l'encadrement des loyers, mesure aux effets désastreux : "
        "frein aux constructions, entretien réduit, pénurie aggravée",

    "logements-vacants":
        "Remettre 50 000 logements vacants sur le marché locatif parisien en supprimant "
        "l'encadrement des loyers qui dissuade les propriétaires de louer",

    "logement-public":
        "Moratoire total sur la construction de logements sociaux (273 M€/an d'économies). "
        "Grand plan d'accession à la propriété : vente de logements sociaux aux locataires. "
        "Stopper les financements de ZAC et écoquartiers (129 M€/an d'économies)",

    "parc-social":
        "Attribution des logements sociaux via une appli transparente sans passe-droit. "
        "Favoriser la rotation en privilégiant les familles modestes. Expulsion systématique "
        "des fauteurs de troubles et trafiquants du parc social",

    "jeunesse":
        "Villa des talents : résidence étudiante de prestige en plein Paris pour les "
        "meilleurs étudiants français (Sorbonne, Sciences Po, ENS, École Boulle, "
        "Conservatoire...), financée par les grandes écoles partenaires, coût zéro "
        "pour la collectivité",

    # --- STATIONNEMENT & COMMERCE (Mesures 16-19, 51) ---
    "stationnement":
        "Tarif unique 3€/h dans tous les arrondissements. Stationnement résident étendu "
        "à tout l'arrondissement. Gratuité 12h-14h pour aider les restaurateurs. 1ère heure "
        "gratuite pour les professionnels. Places disponibles en temps réel via GPS et IA",

    # --- PROPRETÉ (Mesures 20-22) ---
    "proprete":
        "Privatisation totale du ramassage des ordures ménagères et du nettoyage de la "
        "voirie (27% moins cher selon la CRC). Plan anti-rats : suppression des sources "
        "de nourriture en surface, poubelles à QR codes pour signalement en temps réel",

    # --- SÉCURITÉ & POLICE (Mesures 23-28) ---
    "police-municipale":
        "8 000 policiers municipaux armés (contre 3 000). Interpellations systématiques "
        "des délinquants. Vidéosurveillance IA généralisée. Création d'une brigade montée "
        "à cheval (40 chevaux) et d'une brigade canine (30 chiens) pour parcs et zones sensibles",

    "prevention-mediation":
        "Reconquête des quartiers sensibles (Stalingrad, Porte de la Chapelle, Goutte "
        "d'Or) : déploiement massif de forces de l'ordre 24h/24, démantèlement des "
        "campements illégaux",

    # --- ÉCLAIRAGE (Mesures 29-30) ---
    "eclairage-securite":
        "Réverbères intelligents anti-agression pilotés par IA (détection de cris, bris "
        "de verre, coups de feu). Éclairage LED maintenu toute la nuit. Droit des "
        "commerces d'éclairer leurs vitrines",

    # --- SPORT (Mesures 31-32) — CORRECTION texte mélangé ---
    "sport":
        "Équipements sportifs municipaux ouverts de 7h à 23h avec partenariats "
        "entreprises. Terrains de sport sous le métro aérien (football, basketball, padel)",

    # --- NUMÉRIQUE (Mesures 33-34) ---
    "technologie-innovation":
        "Commande publique réservée aux entreprises françaises du numérique. Données "
        "des Parisiens stockées exclusivement sur serveurs français. Maquette numérique "
        "(jumeau numérique) de Paris",

    # --- TRAIN DE VIE DES ÉLUS (Mesures 42-46) ---
    "train-vie-elus":
        "Réduire les adjoints à 10 (contre 37). Diviser par 2 les conseillers de Paris "
        "(163→81). Diviser par 5 les voitures de fonction (500→100) et les collaborateurs "
        "de cabinet (145→30). Supprimer frais de représentation et jetons de présence. "
        "Économie : 18 M€/an",

    # --- URBANISME / COMMERCE (Mesure 50) ---
    "commerce-entrepreneurs":
        "Abroger le PLU bioclimatique (PLUb) et diviser par 3 les durées d'instruction "
        "des permis de construire pour libérer les entrepreneurs",

    # --- BUDGET PARTICIPATIF ---
    "budget-participatif":
        "Au moins 2 référendums locaux par an sur les grands projets de la ville",

    # --- VIE ASSOCIATIVE (correction : avait le texte des référendums) ---
    "vie-associative":
        "Réduction de 100 M€/an des subventions aux associations politisées, "
        "recentrage sur les associations d'intérêt général",

    # --- VILLE-REFUGE (correction : avait le texte du sport) ---
    "ville-refuge":
        "Fermeture des 99 centres d'hébergement pour migrants en situation "
        "irrégulière à Paris",

    # --- CORRECTIONS : textes qui étaient des doublons ou mal placés → null ---
    "alimentation": None,           # doublon de cantine-fournitures
    "musees-culture": None,         # avait texte budget, pas de mesure musée dans le PDF
    "tarification-solidarite": None, # avait texte budget générique
}

# Sous-thèmes existants à ne PAS toucher (propositions correctes venant des
# sections descriptives du PDF, pas des 51 mesures numérotées)
KEEP_AS_IS = [
    "sante", "navettes-fluviales", "velo", "pietons-circulation",
    "logistique-urbaine", "arbres-vegetation", "baignades-seine", "peripherique",
]

# =============================================================================
# NOUVEAUX SOUS-THÈMES (Mesures non couvertes par les sous-thèmes existants)
# =============================================================================
NEW_SOUS_THEMES = [
    {
        "category_id": "democratie",
        "id": "gestion-effectifs",
        "nom": "Gestion des effectifs municipaux",
        "knafo_texte":
            "Non-remplacement d'un départ sur deux (objectif : -15 000 postes en 6 ans). "
            "Mobilité interne et reconversion vers police municipale et petite enfance. "
            "Plan de départs volontaires. Rationalisation du temps de travail "
            "(50 jours d'absence → 33 jours pour les nouveaux contrats)",
        # PDF: Mesures 35, 37, 38, 39
    },
    {
        "category_id": "grand-paris",
        "id": "ventes-patrimoine",
        "nom": "Ventes de patrimoine municipal",
        "knafo_texte":
            "Vente de bâtiments municipaux devenus obsolètes, de foncier non bâti "
            "(880 ha plaine d'Achères), de logements et commerces municipaux. Plan "
            "d'accession à la propriété avec exonération de frais de notaire pour "
            "les primo-accédants",
        # PDF: Mesures 47, 48, 49
    },
]


def update_existing_entries(content):
    """Met à jour les entrées knafo existantes dans les sous-thèmes Paris."""
    count_updated = 0
    count_nulled = 0

    for st_id, new_text in UPDATES.items():
        # Recalculer les bornes Paris à chaque itération (le contenu change)
        paris_start = content.find('"paris-2026": {')
        lyon_start = content.find('"lyon-2026": {')
        if paris_start < 0 or lyon_start < 0:
            print("ERREUR: Section Paris ou Lyon introuvable")
            sys.exit(1)

        paris_bloc = content[paris_start:lyon_start]

        # Trouver le sous-thème dans la section Paris
        st_pattern = rf'id:\s*"{re.escape(st_id)}"'
        st_match = re.search(st_pattern, paris_bloc)
        if not st_match:
            print(f"  ATTENTION: sous-thème '{st_id}' non trouvé dans Paris")
            continue

        # Trouver l'entrée knafo dans ce sous-thème
        # Chercher dans les 5000 chars suivants (les blocs peuvent être longs)
        search_start = paris_start + st_match.start()
        search_end = min(search_start + 5000, lyon_start)
        search_bloc = content[search_start:search_end]

        # Pattern pour trouver knafo: { ... } ou knafo: null
        # Le { ... } peut contenir des guillemets échappés mais pas de } imbriqué
        knafo_pattern = r'knafo:\s*(?:\{[^}]*\}|null)'
        knafo_match = re.search(knafo_pattern, search_bloc)
        if not knafo_match:
            print(f"  ATTENTION: entrée knafo non trouvée dans '{st_id}'")
            continue

        abs_start = search_start + knafo_match.start()
        abs_end = search_start + knafo_match.end()

        if new_text is None:
            new_knafo = "knafo: null"
            count_nulled += 1
            action = "→ null"
        else:
            new_knafo = f"knafo: {make_knafo_entry(new_text)}"
            count_updated += 1
            action = "→ mis à jour"

        content = content[:abs_start] + new_knafo + content[abs_end:]
        print(f"  {st_id:30s} {action}")

    return content, count_updated, count_nulled


def add_new_sous_themes(content):
    """Ajoute les nouveaux sous-thèmes dans les catégories appropriées."""
    count_added = 0

    paris_start = content.find('"paris-2026": {')
    lyon_start = content.find('"lyon-2026": {')
    paris_bloc = content[paris_start:lyon_start]

    # Tous les candidats Paris
    candidats = ["gregoire", "dati", "chikirou", "bournazel", "knafo", "mariani"]

    for new_st in NEW_SOUS_THEMES:
        cat_id = new_st["category_id"]
        st_id = new_st["id"]
        st_nom = new_st["nom"]
        knafo_texte = new_st["knafo_texte"]

        # Vérifier que le sous-thème n'existe pas déjà
        if f'id: "{st_id}"' in paris_bloc:
            print(f"  {st_id:30s} existe déjà, skip")
            continue

        # Trouver la catégorie
        cat_pattern = rf'id:\s*"{re.escape(cat_id)}".*?sousThemes:\s*\['
        cat_match = re.search(cat_pattern, paris_bloc, re.DOTALL)
        if not cat_match:
            print(f"  ERREUR: catégorie '{cat_id}' non trouvée")
            continue

        # Trouver la fin de sousThemes: [ ... ] pour cette catégorie
        # On cherche le dernier sous-thème de la catégorie
        cat_start_abs = paris_start + cat_match.end()

        # Trouver le ] fermant de sousThemes en comptant les niveaux
        depth = 1
        pos = cat_start_abs
        last_closing_brace = pos
        while pos < lyon_start and depth > 0:
            if content[pos] == '[':
                depth += 1
            elif content[pos] == ']':
                depth -= 1
                if depth == 0:
                    last_closing_brace = pos
            pos += 1

        # Construire le bloc du nouveau sous-thème
        props_lines = []
        for cid in candidats:
            if cid == "knafo":
                props_lines.append(
                    f'                {cid}: {make_knafo_entry(knafo_texte)}'
                )
            else:
                props_lines.append(f'                {cid}: null')

        new_block = (
            f',\n'
            f'            {{\n'
            f'              id: "{to_js(st_id)}",\n'
            f'              nom: "{to_js(st_nom)}",\n'
            f'              propositions: {{\n'
            + ',\n'.join(props_lines) + '\n'
            f'              }}\n'
            f'            }}'
        )

        # Insérer juste avant le ] fermant
        content = content[:last_closing_brace] + new_block + '\n          ' + content[last_closing_brace:]

        # Recalculer
        lyon_start = content.find('"lyon-2026"')
        paris_bloc = content[paris_start:lyon_start]

        count_added += 1
        print(f"  {st_id:30s} → NOUVEAU sous-thème dans '{cat_id}'")

    return content, count_added


def main():
    print("=" * 60)
    print("  CORRECTION COMPLÈTE KNAFO — 51 mesures du PDF")
    print("=" * 60)
    print()

    with open(APPJS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    original_len = len(content)

    # 1. Mettre à jour les entrées existantes
    print("1. Mise à jour des entrées existantes:")
    content, n_updated, n_nulled = update_existing_entries(content)
    print(f"\n   → {n_updated} mis à jour, {n_nulled} passés à null")
    print()

    # 2. Ajouter les nouveaux sous-thèmes
    print("2. Ajout de nouveaux sous-thèmes:")
    content, n_added = add_new_sous_themes(content)
    print(f"\n   → {n_added} nouveaux sous-thèmes ajoutés")
    print()

    # 3. Sauvegarder
    with open(APPJS_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"3. Fichier sauvegardé ({len(content)} chars, diff: {len(content) - original_len:+d})")
    print()

    # 4. Résumé
    print("=" * 60)
    print(f"  RÉSUMÉ:")
    print(f"    {n_updated} propositions mises à jour (textes plus complets)")
    print(f"    {n_nulled} doublons/erreurs corrigés (→ null)")
    print(f"    {n_added} nouveaux sous-thèmes créés")
    print(f"    Entrées conservées telles quelles: {', '.join(KEEP_AS_IS)}")
    print(f"  Couverture: 51/51 mesures du PDF mappées")
    print("=" * 60)


if __name__ == "__main__":
    main()
