#!/usr/bin/env python3
"""
Synchronise les données PQTV avec les données officielles data.gouv.fr.

Actions :
1. Corrige le matching La Réunion (suffixe "(La Réunion)" dans les noms PQTV)
2. Retire les candidats non officiellement déclarés (65 "en trop")
3. Ajoute les nuances politiques officielles
4. Crée les fichiers pour les nouvelles villes à intégrer

Usage : python scripts/sync_datagouv.py [--dry-run] [--add-cities]
"""

import csv
import json
import os
import sys
import io
import re
import argparse
from collections import defaultdict
from unicodedata import normalize
from datetime import date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VILLES_JSON = os.path.join(BASE_DIR, 'data', 'villes.json')
ELECTIONS_DIR = os.path.join(BASE_DIR, 'data', 'elections')
CSV_OFFICIEL = os.path.join(BASE_DIR, 'data', 'candidatures_officielles_2026_T1.csv')

TODAY = date.today().isoformat()


def normalize_name(name):
    """Normalise un nom pour comparaison."""
    n = normalize('NFD', name.upper()).encode('ascii', 'ignore').decode('ascii')
    n = n.replace('-', ' ').replace("'", ' ').replace('  ', ' ').strip()
    return n


def clean_ville_name(nom):
    """Retire les suffixes comme '(La Réunion)' pour le matching."""
    return re.sub(r'\s*\(.*?\)\s*$', '', nom).strip()


def load_official_heads():
    """Charge toutes les têtes de liste du CSV officiel, indexées par (nom_circo_normalisé, dept)."""
    officiel = defaultdict(list)
    with open(CSV_OFFICIEL, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row.get('Tête de liste') == 'OUI':
                circo = row['Circonscription'].strip()
                dept = row['Code département'].strip()
                officiel[(normalize_name(circo), dept)].append({
                    'nom_complet': row['Prénom sur le bulletin de vote'].strip() + ' ' + row['Nom sur le bulletin de vote'].strip(),
                    'nom_famille': row['Nom sur le bulletin de vote'].strip(),
                    'prenom': row['Prénom sur le bulletin de vote'].strip(),
                    'liste_abregee': row['Libellé abrégé de liste'].strip(),
                    'liste_complete': row['Libellé de la liste'].strip(),
                    'nuance_code': row.get('Code nuance de liste', '').strip(),
                    'nuance': row.get('Nuance de liste', '').strip(),
                    'code_circo': row['Code circonscription'].strip(),
                })
    return officiel


def find_official_match(nom_ville, dept, officiel):
    """Trouve les listes officielles pour une ville PQTV."""
    clean = clean_ville_name(nom_ville)
    norm = normalize_name(clean)

    # Match direct par (nom normalisé, dept)
    if (norm, dept) in officiel:
        return officiel[(norm, dept)]

    # Essai sans département si nom unique
    matches = [(k, v) for k, v in officiel.items() if k[0] == norm]
    if len(matches) == 1:
        return matches[0][1]

    return None


def match_candidat(cand_nom, officiels):
    """Trouve un candidat PQTV dans la liste officielle. Retourne l'entrée officielle ou None."""
    norm = normalize_name(cand_nom)
    parts = norm.split()

    for off in officiels:
        off_famille = normalize_name(off['nom_famille'])
        off_complet = normalize_name(off['nom_complet'])

        # Match nom de famille dans le nom PQTV
        if off_famille in norm or norm.endswith(off_famille):
            return off
        if off_complet == norm:
            return off
        # Match nom de famille PQTV (dernier mot) vs nom officiel
        if len(parts) >= 2:
            if parts[-1] == off_famille:
                return off
            if len(parts) >= 3 and ' '.join(parts[-2:]) == off_famille:
                return off

    return None


def make_city_id(nom):
    """Génère un ID de ville à partir du nom."""
    n = normalize('NFD', nom.lower()).encode('ascii', 'ignore').decode('ascii')
    n = re.sub(r'[^a-z0-9]+', '-', n).strip('-')
    return n


def format_candidat_name(prenom, nom_famille):
    """Formate Prénom Nom en title case propre."""
    def titlecase_part(s):
        # Gère les noms composés avec tirets
        return '-'.join(w.capitalize() for w in s.split('-'))

    parts = []
    for p in prenom.split():
        parts.append(titlecase_part(p))
    nom_parts = []
    for p in nom_famille.split():
        if p.lower() in ('de', 'du', 'des', 'le', 'la', 'les', "d'", "l'"):
            nom_parts.append(p.lower())
        else:
            nom_parts.append(titlecase_part(p))
    return ' '.join(parts) + ' ' + ' '.join(nom_parts)


# Mapping département -> code postal principal (approximatif, pour les nouvelles villes)
DEPT_TO_CP = {
    '01': '01000', '02': '02000', '03': '03100', '06': '06000', '08': '08000',
    '11': '11000', '12': '12000', '16': '16000', '22': '22000', '24': '24000',
    '27': '27000', '2B': '20200', '30': '30000', '31': '31000', '36': '36000',
    '39': '39100', '40': '40000', '43': '43000', '46': '46000', '56': '56000',
    '57': '57000', '59': '59000', '60': '60000', '62': '62000', '64': '64100',
    '65': '65000', '70': '70000', '77': '77100', '78': '78500', '79': '79000',
    '81': '81000', '82': '82000', '88': '88000', '90': '90000', '91': '91000',
    '93': '93000', '95': '95200', '974': '97400', '971': '97110', '976': '97600',
    '10': '10000',
}

# Codes postaux spécifiques pour les villes qu'on ajoute
CITY_CP = {
    'Mamoudzou': '97600',
    'Sarcelles': '95200',
    'Meaux': '77100',
    'Beauvais': '60000',
    'Épinay-sur-Seine': '93800',
    'Saint-Quentin': '02100',
    'Vannes': '56000',
    'Narbonne': '11100',
    'Bobigny': '93000',
    'Bayonne': '64100',
    'Sartrouville': '78500',
    'Évreux': '27000',
    'Albi': '81000',
    'Bastia': '20200',
    'Carcassonne': '11000',
    'Belfort': '90000',
    'Charleville-Mézières': '08000',
    'Saint-Brieuc': '22000',
    'Châteauroux': '36000',
    'Garges-lès-Gonesse': '95140',
    'Angoulême': '16000',
    'Bourg-en-Bresse': '01000',
    'Tarbes': '65000',
    'Arras': '62000',
    'Tremblay-en-France': '93290',
    'Montluçon': '03100',
    'Mont-de-Marsan': '40000',
    'Épinal': '88000',
    'Lens': '62300',
    'Périgueux': '24000',
    'Maubeuge': '59600',
    'Vichy': '03200',
    'Laon': '02000',
    'Rodez': '12000',
    'Dole': '39100',
    'Oyonnax': '01100',
    'Cahors': '46000',
    'Le Puy-en-Velay': '43000',
    'Pointe-à-Pitre': '97110',
    'Vesoul': '70000',
    'Montauban': '82000',
    'Niort': '79000',
    'Lorient': '56100',
    'Troyes': '10000',
}

# Villes à ajouter avec leur population approximative
CITIES_TO_ADD = {
    'Mamoudzou': ('976', 71000),
    'Sarcelles': ('95', 58000),
    'Meaux': ('77', 56000),
    'Beauvais': ('60', 56000),
    'Épinay-sur-Seine': ('93', 55000),
    'Saint-Quentin': ('02', 55000),
    'Vannes': ('56', 55000),
    'Narbonne': ('11', 55000),
    'Bobigny': ('93', 53000),
    'Bayonne': ('64', 52000),
    'Sartrouville': ('78', 51000),
    'Évreux': ('27', 51000),
    'Albi': ('81', 49000),
    'Bastia': ('2B', 48000),
    'Carcassonne': ('11', 47000),
    'Belfort': ('90', 47000),
    'Charleville-Mézières': ('08', 47000),
    'Saint-Brieuc': ('22', 45000),
    'Châteauroux': ('36', 44000),
    'Garges-lès-Gonesse': ('95', 43000),
    'Angoulême': ('16', 42000),
    'Bourg-en-Bresse': ('01', 42000),
    'Tarbes': ('65', 41000),
    'Arras': ('62', 41000),
    'Tremblay-en-France': ('93', 38000),
    'Montluçon': ('03', 35000),
    'Mont-de-Marsan': ('40', 32000),
    'Épinal': ('88', 32000),
    'Lens': ('62', 31000),
    'Périgueux': ('24', 30000),
    'Maubeuge': ('59', 29000),
    'Montauban': ('82', 60000),
    'Niort': ('79', 60000),
    'Lorient': ('56', 57000),
    'Troyes': ('10', 61000),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Afficher les changements sans modifier les fichiers')
    parser.add_argument('--no-add-cities', action='store_true', help='Ne pas ajouter de nouvelles villes')
    parser.add_argument('--min-pop', type=int, default=30000, help='Population minimum pour les nouvelles villes (défaut: 30000)')
    args = parser.parse_args()

    print("=" * 80)
    print("SYNCHRONISATION PQTV ← DATA.GOUV.FR")
    print(f"Mode: {'DRY RUN (aucune modification)' if args.dry_run else 'MODIFICATION DES FICHIERS'}")
    print("=" * 80)

    # Charger données officielles
    print("\n📥 Chargement du CSV officiel...")
    officiel = load_official_heads()
    print(f"   {sum(len(v) for v in officiel.values())} têtes de liste chargées")

    # Charger villes.json
    print("\n📥 Chargement de villes.json...")
    with open(VILLES_JSON, encoding='utf-8') as f:
        villes = json.load(f)
    print(f"   {len(villes)} villes")

    # =========================================================================
    # ÉTAPE 1 & 2 & 3 : Pour chaque ville existante, comparer et corriger
    # =========================================================================
    print("\n" + "=" * 80)
    print("ÉTAPE 1-3 : NETTOYAGE + NUANCES pour les villes existantes")
    print("=" * 80)

    total_removed = 0
    total_nuances_added = 0
    villes_modifiees = []
    villes_non_trouvees = []

    for ville in villes:
        ville_id = ville['id']
        nom = ville['nom']
        dept = ville.get('departement', '')

        # Trouver correspondance officielle
        off_listes = find_official_match(nom, dept, officiel)
        if not off_listes:
            villes_non_trouvees.append(f"{nom} (dép. {dept})")
            continue

        # Charger le JSON election
        election_file = os.path.join(ELECTIONS_DIR, f"{ville_id}-2026.json")
        if not os.path.exists(election_file):
            print(f"  ⚠️  Fichier manquant: {election_file}")
            continue

        with open(election_file, encoding='utf-8') as f:
            election_data = json.load(f)

        candidats = election_data.get('candidats', [])
        modified = False
        removed_names = []
        nuances_added = []

        # Identifier les candidats à garder/retirer et ajouter les nuances
        new_candidats = []
        for cand in candidats:
            off = match_candidat(cand['nom'], off_listes)
            if off:
                # Candidat confirmé — ajouter nuance si disponible
                if off.get('nuance_code') and 'nuanceOfficielle' not in cand:
                    cand['nuanceOfficielle'] = off['nuance_code']
                    cand['nuanceLibelle'] = off['nuance']
                    nuances_added.append(f"{cand['nom']}: {off['nuance_code']} ({off['nuance']})")
                    modified = True
                    total_nuances_added += 1
                new_candidats.append(cand)
            else:
                # Candidat pas dans l'officiel — à retirer
                removed_names.append(f"{cand['nom']} ({cand.get('liste', '?')})")
                total_removed += 1
                modified = True

        if modified:
            election_data['candidats'] = new_candidats
            villes_modifiees.append(nom)

            if removed_names:
                print(f"\n  🗑️  {nom}: {len(removed_names)} candidat(s) retiré(s)")
                for r in removed_names:
                    print(f"      - {r}")

            if nuances_added:
                print(f"  🏷️  {nom}: {len(nuances_added)} nuance(s) ajoutée(s)")

            if not args.dry_run:
                with open(election_file, 'w', encoding='utf-8') as f:
                    json.dump(election_data, f, ensure_ascii=False, indent=2)

        # Mettre à jour stats dans villes.json
        new_count = len(new_candidats)
        if ville.get('candidats'):
            # Filtrer aussi la liste dans villes.json
            off_names_norm = {normalize_name(c['nom']) for c in new_candidats}
            ville['candidats'] = [
                c for c in ville['candidats']
                if normalize_name(c['nom']) in off_names_norm
            ]
        if 'stats' in ville:
            ville['stats']['candidats'] = new_count
            # Recompter les complets
            complets = sum(1 for c in new_candidats if c.get('programmeComplet'))
            ville['stats']['complets'] = complets

    print(f"\n{'─' * 60}")
    print(f"BILAN NETTOYAGE:")
    print(f"  🗑️  {total_removed} candidats retirés (non officiellement déclarés)")
    print(f"  🏷️  {total_nuances_added} nuances politiques ajoutées")
    print(f"  📝 {len(villes_modifiees)} fichiers modifiés")

    if villes_non_trouvees:
        print(f"\n  ⚠️  Villes non matchées ({len(villes_non_trouvees)}):")
        for v in villes_non_trouvees:
            print(f"     ? {v}")

    # =========================================================================
    # ÉTAPE 4 : Ajouter de nouvelles villes
    # =========================================================================
    if not args.no_add_cities:
        print("\n" + "=" * 80)
        print("ÉTAPE 4 : AJOUT DE NOUVELLES VILLES")
        print("=" * 80)

        cities_added = 0
        for city_name, (dept, pop) in sorted(CITIES_TO_ADD.items(), key=lambda x: -x[1][1]):
            if pop < args.min_pop:
                continue

            # Vérifier pas déjà dans PQTV
            city_id = make_city_id(city_name)
            already_exists = any(v['id'] == city_id for v in villes)
            if already_exists:
                continue

            # Trouver dans l'officiel
            off_listes = find_official_match(city_name, dept, officiel)
            if not off_listes:
                print(f"  ⚠️  {city_name} (dép. {dept}): non trouvé dans le CSV officiel")
                continue

            cp = CITY_CP.get(city_name, DEPT_TO_CP.get(dept, f'{dept}000'))

            # Créer le JSON election
            candidats_json = []
            candidats_villes = []
            for off in off_listes:
                cand_name = format_candidat_name(off['prenom'], off['nom_famille'])
                cand_id = make_city_id(off['nom_famille'])

                candidats_json.append({
                    'id': cand_id,
                    'nom': cand_name,
                    'liste': off['liste_abregee'],
                    'programmeUrl': None,
                    'programmeComplet': False,
                    'programmePdfPath': None,
                    'nuanceOfficielle': off['nuance_code'],
                    'nuanceLibelle': off['nuance'],
                })
                candidats_villes.append({
                    'id': cand_id,
                    'nom': cand_name,
                    'liste': off['liste_abregee'],
                })

            election_data = {
                'ville': city_name,
                'annee': 2026,
                'type': 'municipales',
                'dateVote': '2026-03-15',
                'candidats': candidats_json,
                'categories': [],
            }

            election_file = os.path.join(ELECTIONS_DIR, f"{city_id}-2026.json")

            print(f"\n  ➕ {city_name} (dép. {dept}, ~{pop//1000}k hab) — {len(off_listes)} candidats")
            for c in candidats_json:
                nuance = f" [{c['nuanceOfficielle']}]" if c.get('nuanceOfficielle') else ""
                print(f"      • {c['nom']}{nuance} — {c['liste']}")

            if not args.dry_run:
                with open(election_file, 'w', encoding='utf-8') as f:
                    json.dump(election_data, f, ensure_ascii=False, indent=2)

            # Ajouter à villes.json
            ville_entry = {
                'id': city_id,
                'nom': city_name,
                'codePostal': cp,
                'departement': dept,
                'elections': [f"{city_id}-2026"],
                'stats': {
                    'candidats': len(candidats_json),
                    'propositions': 0,
                    'themes': 0,
                    'complets': 0,
                },
                'candidats': candidats_villes,
                'derniereMaj': TODAY,
            }
            villes.append(ville_entry)
            cities_added += 1

        # Trier villes par nom
        villes.sort(key=lambda v: v['nom'])

        print(f"\n{'─' * 60}")
        print(f"  ➕ {cities_added} nouvelles villes ajoutées")

    # =========================================================================
    # Sauvegarder villes.json
    # =========================================================================
    if not args.dry_run:
        print("\n💾 Sauvegarde de villes.json...")
        with open(VILLES_JSON, 'w', encoding='utf-8') as f:
            json.dump(villes, f, ensure_ascii=False, indent=2)
        print("   ✅ Sauvegardé")

    print(f"\n{'=' * 80}")
    print(f"RÉSUMÉ FINAL:")
    print(f"  • {len(villes)} villes au total")
    print(f"  • {sum(len(v.get('candidats', [])) for v in villes)} candidats au total")
    print(f"  • {total_removed} candidats retirés")
    print(f"  • {total_nuances_added} nuances ajoutées")
    if not args.no_add_cities:
        print(f"  • {cities_added} nouvelles villes")
    print("=" * 80)

    if args.dry_run:
        print("\n⚠️  MODE DRY RUN — aucun fichier modifié. Relancer sans --dry-run pour appliquer.")


if __name__ == '__main__':
    main()
