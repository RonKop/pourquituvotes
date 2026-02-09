#!/usr/bin/env python3
"""
Complément d'intégration du programme Knafo — mesures manquantes.
1. Remplit les sous-thèmes existants laissés à null
2. Crée de nouveaux sous-thèmes pour les mesures sans correspondance
"""

import re
import os

APPJS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "js", "app.js")
SRC = "Programme officiel 2026"
SRC_URL = "https://unevilleheureuse.fr/"

def to_js(text):
    result = []
    for ch in text:
        cp = ord(ch)
        if cp > 127:
            result.append('\\u{:04X}'.format(cp))
        else:
            result.append(ch)
    return ''.join(result)

# === PARTIE 1 : Remplir les null existants ===
FILL_NULLS = {
    "jeunesse": (
        "Villa des talents : r\\u00E9sidence \\u00E9tudiante de grande qualit\\u00E9 pour les meilleurs \\u00E9tudiants fran\\u00E7ais, "
        "financ\\u00E9e par les grandes \\u00E9coles partenaires (Sorbonne, Sciences Po, ENS, Mines, Conservatoire\\u2026). "
        "Co\\u00FBt z\\u00E9ro pour la collectivit\\u00E9"
    ),
    "baignades-seine": (
        "Suppression du programme de baignade dans la Seine (47 M\\u20AC sur le mandat d\\u2019\\u00E9conomies)"
    ),
    "prevention-mediation": (
        "D\\u00E9mant\\u00E8lement des 99 centres pour migrants ill\\u00E9gaux. "
        "Fin de toute subvention municipale aux associations favorisant l\\u2019immigration clandestine (22 M\\u20AC/an d\\u2019\\u00E9conomies). "
        "Contr\\u00F4le strict des attestations d\\u2019accueil (visas) et du regroupement familial"
    ),
    "handicap-scolaire": None,  # skip
    "logements-vacants": (
        "Suppression de l\\u2019encadrement des loyers pour remettre 50 000 logements vacants sur le march\\u00E9 locatif. "
        "Suppression de la taxe sur les logements vacants (effet contre-productif)"
    ),
}

# === PARTIE 2 : Nouveaux sous-thèmes à créer ===
# Format: (category_id_to_insert_after_last_soustheme, new_soustheme_id, new_soustheme_nom, knafo_texte)
NEW_SOUS_THEMES = [
    # Stationnement dans Transports
    ("transports", "stationnement", "Stationnement",
     "Tarif unique 3\\u20AC/h dans tous les arrondissements, tous v\\u00E9hicules. "
     "1\\u00E8re heure gratuite. Gratuit\\u00E9 entre 12h et 14h pour les restaurateurs. "
     "Stationnement r\\u00E9sident \\u00E9tendu \\u00E0 tout l\\u2019arrondissement. "
     "Places disponibles en temps r\\u00E9el via IA et GPS (Waze, Maps). "
     "15 000 nouvelles places cr\\u00E9\\u00E9es. Amende ramen\\u00E9e \\u00E0 30\\u20AC"
    ),
    # Technologie dans Grand Paris & Métropole (ou un existant)
    ("grand-paris", "technologie-innovation", "Technologie & Innovation",
     "Maquette num\\u00E9rique (jumeau num\\u00E9rique) de Paris pour simuler tous les projets avant travaux (2 M\\u20AC). "
     "Souverainet\\u00E9 num\\u00E9rique : donn\\u00E9es municipales sur serveurs fran\\u00E7ais SecNumCloud, commande publique r\\u00E9serv\\u00E9e aux entreprises fran\\u00E7aises. "
     "Paiement du stationnement en bitcoin autoris\\u00E9"
    ),
    # Train de vie des élus dans Démocratie
    ("democratie", "train-vie-elus", "Train de vie des \\u00E9lus",
     "R\\u00E9duire le nombre d\\u2019adjoints \\u00E0 10 (contre 37 sous Hidalgo). "
     "Diviser par 2 le nombre de conseillers de Paris (163 \\u2192 81). "
     "Diviser par 5 les voitures de fonction (500 \\u2192 100). "
     "Diviser par 5 les collaborateurs de cabinet (353 \\u2192 \\u223C100). "
     "Supprimer les frais de repr\\u00E9sentation et jetons de pr\\u00E9sence. "
     "\\u00C9conomie : 18 M\\u20AC/an"
    ),
    # Entrepreneurs / Commerce dans Grand Paris
    ("grand-paris", "commerce-entrepreneurs", "Commerce & Entrepreneurs",
     "Lib\\u00E9rer les entrepreneurs : abroger le PLUb, simplifier les r\\u00E8gles d\\u2019urbanisme. "
     "Diviser par 2 les dur\\u00E9es d\\u2019instruction des permis de construire. "
     "Commande publique r\\u00E9serv\\u00E9e aux entreprises fran\\u00E7aises. "
     "Terrasses chauff\\u00E9es autoris\\u00E9es (bras de fer avec l\\u2019\\u00C9tat). "
     "1\\u00E8re heure de stationnement gratuite et gratuit\\u00E9 12h-14h pour soutenir les restaurateurs"
    ),
]


def fill_existing_nulls(content, paris_start, paris_end):
    """Remplit les knafo: null existants dans la section Paris."""
    section = content[paris_start:paris_end]
    count = 0

    src = to_js(SRC)

    for st_id, texte in FILL_NULLS.items():
        if texte is None:
            continue

        pattern = f'id: "{st_id}"'
        pos = section.find(pattern)
        if pos == -1:
            print(f"  SKIP: sous-thème '{st_id}' non trouvé")
            continue

        search_area = section[pos:pos+3000]
        knafo_null = search_area.find('knafo: null')
        if knafo_null == -1 or knafo_null > 2000:
            # Vérifier si knafo a déjà une valeur
            knafo_obj = re.search(r'knafo: \{', search_area[:2000])
            if knafo_obj:
                print(f"  SKIP: '{st_id}' a déjà une valeur")
            else:
                print(f"  WARN: '{st_id}' — knafo non trouvé")
            continue

        abs_pos = pos + knafo_null
        old = 'knafo: null'
        new_val = f'knafo: {{ texte: "{texte}", source: "{src}", sourceUrl: "{SRC_URL}" }}'
        section = section[:abs_pos] + new_val + section[abs_pos + len(old):]
        count += 1
        print(f"  + {st_id}: rempli")

    return content[:paris_start] + section + content[paris_end:], count


def add_new_sous_themes(content, paris_start, paris_end):
    """Ajoute de nouveaux sous-thèmes dans les catégories existantes."""
    section = content[paris_start:paris_end]
    count = 0
    src = to_js(SRC)
    candidates = ["gregoire", "dati", "chikirou", "bournazel", "knafo", "mariani"]

    for cat_id, st_id, st_nom, knafo_texte in NEW_SOUS_THEMES:
        # Vérifier que le sous-thème n'existe pas déjà
        if f'id: "{st_id}"' in section:
            print(f"  SKIP: sous-thème '{st_id}' existe déjà")
            continue

        # Trouver la catégorie. On cherche le pattern: id: "cat_id" ou un id qui contient cat_id
        # Les catégories ont des IDs variés, cherchons plus flexible
        cat_pattern = f'id: "{cat_id}"'
        cat_pos = section.find(cat_pattern)

        # Si pas trouvé, chercher par nom partiel
        if cat_pos == -1:
            # Essayons avec des variantes
            for variant in [cat_id, cat_id.replace("-", ""), cat_id + "-paris"]:
                cat_pattern = f'id: "{variant}"'
                cat_pos = section.find(cat_pattern)
                if cat_pos != -1:
                    break

        if cat_pos == -1:
            print(f"  WARN: catégorie '{cat_id}' non trouvée, recherche par sousThemes...")
            # Chercher la dernière sousThemes d'une catégorie approchante
            continue

        # Trouver la fin des sousThemes de cette catégorie
        # On cherche le pattern ]\n        }\n (fin du tableau sousThemes + fin de la catégorie)
        # À partir de la catégorie, chercher le prochain "]\n        }" qui ferme sousThemes
        search_from = cat_pos
        # On doit trouver le sousThemes: [ de cette catégorie
        st_array_start = section.find('sousThemes: [', search_from)
        if st_array_start == -1:
            print(f"  WARN: sousThemes non trouvé pour catégorie '{cat_id}'")
            continue

        # Trouver la fin du tableau sousThemes
        # On parcourt les [ et ] pour trouver le ] correspondant
        depth = 0
        pos = st_array_start + len('sousThemes: [')
        depth = 1
        while pos < len(section) and depth > 0:
            if section[pos] == '[':
                depth += 1
            elif section[pos] == ']':
                depth -= 1
            pos += 1
        # pos est maintenant juste après le ] fermant de sousThemes
        insert_pos = pos - 1  # juste avant le ]

        # Construire le nouveau sous-thème
        nom_js = st_nom  # déjà en unicode escapes si besoin
        props_lines = []
        for cand in candidates:
            if cand == "knafo":
                props_lines.append(
                    f'                {cand}: {{ texte: "{knafo_texte}", source: "{src}", sourceUrl: "{SRC_URL}" }}'
                )
            else:
                props_lines.append(f'                {cand}: null')

        new_st = (
            ',\n'
            '            {\n'
            f'              id: "{st_id}",\n'
            f'              nom: "{nom_js}",\n'
            '              propositions: {\n'
            + ',\n'.join(props_lines) + '\n'
            '              }\n'
            '            }\n'
            '          '
        )

        section = section[:insert_pos] + new_st + section[insert_pos:]
        count += 1
        print(f"  + NOUVEAU sous-thème '{st_id}' dans catégorie '{cat_id}'")

    return content[:paris_start] + section + content[paris_end:], count


def main():
    with open(APPJS, "r", encoding="utf-8") as f:
        content = f.read()

    paris_start = content.find('"paris-2026": {')
    paris_end = content.find('"lyon-2026": {')

    print("=== Partie 1 : Remplir les null existants ===")
    content, n1 = fill_existing_nulls(content, paris_start, paris_end)

    # Recalculer les bornes après modification
    paris_start = content.find('"paris-2026": {')
    paris_end = content.find('"lyon-2026": {')

    print("\n=== Partie 2 : Nouveaux sous-thèmes ===")
    content, n2 = add_new_sous_themes(content, paris_start, paris_end)

    with open(APPJS, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n=== Résultat ===")
    print(f"  {n1} null remplis + {n2} sous-thèmes créés = {n1 + n2} modifications")


if __name__ == "__main__":
    main()
