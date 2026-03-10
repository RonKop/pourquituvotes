#!/usr/bin/env python3
"""
Compare les données PQTV (villes.json + elections/*.json) avec les données officielles
du Ministère de l'intérieur (data.gouv.fr) pour les municipales 2026.

Produit un rapport :
1. Candidats manquants dans PQTV (présents dans l'officiel mais pas chez nous)
2. Candidats en trop dans PQTV (pas dans l'officiel — retirés ?)
3. Différences de noms (orthographe)
4. Nuances politiques officielles vs nos étiquettes
5. Villes candidates à ajouter (grandes villes absentes de PQTV)
"""

import csv
import json
import os
import sys
import io
from collections import defaultdict
from unicodedata import normalize

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VILLES_JSON = os.path.join(BASE_DIR, 'data', 'villes.json')
ELECTIONS_DIR = os.path.join(BASE_DIR, 'data', 'elections')
CSV_OFFICIEL = os.path.join(BASE_DIR, 'data', 'candidatures_officielles_2026_T1.csv')
CSV_PLM = os.path.join(BASE_DIR, 'data', 'candidatures_PLM_2026_T1.csv')


def normalize_name(name):
    """Normalise un nom pour comparaison (majuscules, accents, tirets)."""
    n = normalize('NFD', name.upper()).encode('ascii', 'ignore').decode('ascii')
    n = n.replace('-', ' ').replace("'", ' ').replace('  ', ' ').strip()
    return n


def load_pqtv_data():
    """Charge les données PQTV : villes.json + elections/*.json."""
    with open(VILLES_JSON, encoding='utf-8') as f:
        villes = json.load(f)

    pqtv = {}
    for ville in villes:
        ville_id = ville['id']
        nom = ville['nom']
        dept = ville.get('departement', '')
        candidats = []

        # Charger le fichier elections détaillé
        election_file = os.path.join(ELECTIONS_DIR, f"{ville_id}-2026.json")
        if os.path.exists(election_file):
            with open(election_file, encoding='utf-8') as f:
                election_data = json.load(f)
            for cand in election_data.get('candidats', []):
                candidats.append({
                    'id': cand.get('id', ''),
                    'nom': cand.get('nom', ''),
                    'liste': cand.get('liste', ''),
                })
        else:
            # Fallback sur villes.json
            for cand in ville.get('candidats', []):
                candidats.append({
                    'id': cand.get('id', ''),
                    'nom': cand.get('nom', ''),
                    'liste': cand.get('liste', ''),
                })

        # Clé unique = nom + département (pour gérer les homonymes)
        pqtv[(nom, dept)] = {
            'id': ville_id,
            'nom': nom,
            'codePostal': ville.get('codePostal', ''),
            'departement': dept,
            'candidats': candidats,
        }

    return pqtv


def load_official_data():
    """Charge les têtes de liste depuis le CSV officiel. Clé = (circo, dept)."""
    officiel = defaultdict(list)

    with open(CSV_OFFICIEL, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row.get('Tête de liste') == 'OUI':
                circo = row['Circonscription']
                dept = row['Code département'].strip()
                officiel[(circo, dept)].append({
                    'nom': row['Prénom sur le bulletin de vote'].strip() + ' ' + row['Nom sur le bulletin de vote'].strip(),
                    'nom_famille': row['Nom sur le bulletin de vote'].strip(),
                    'prenom': row['Prénom sur le bulletin de vote'].strip(),
                    'liste_abregee': row['Libellé abrégé de liste'].strip(),
                    'liste_complete': row['Libellé de la liste'].strip(),
                    'nuance_code': row.get('Code nuance de liste', '').strip(),
                    'nuance': row.get('Nuance de liste', '').strip(),
                    'code_circo': row['Code circonscription'].strip(),
                    'departement': dept,
                })

    return officiel


def match_ville(nom_pqtv, dept_pqtv, officiel_keys):
    """Trouve la correspondance entre une ville PQTV et le CSV officiel via (nom, dept)."""
    # Match exact par (nom, dept)
    if (nom_pqtv, dept_pqtv) in officiel_keys:
        return (nom_pqtv, dept_pqtv)

    # Essai par normalisation du nom, même département
    norm_pqtv = normalize_name(nom_pqtv)
    for (circo, dept) in officiel_keys:
        if dept == dept_pqtv and normalize_name(circo) == norm_pqtv:
            return (circo, dept)

    # Essai sans département (pour les villes au nom unique)
    matches_by_name = [(c, d) for (c, d) in officiel_keys if normalize_name(c) == norm_pqtv]
    if len(matches_by_name) == 1:
        return matches_by_name[0]

    return None


def match_candidat(cand_pqtv, officiels):
    """Trouve la correspondance d'un candidat PQTV dans la liste officielle."""
    nom_pqtv = normalize_name(cand_pqtv['nom'])

    for off in officiels:
        nom_off = normalize_name(off['nom'])
        nom_famille_off = normalize_name(off['nom_famille'])

        # Match par nom de famille
        if nom_famille_off in nom_pqtv or nom_pqtv.endswith(nom_famille_off):
            return off

        # Match complet
        if nom_off == nom_pqtv:
            return off

        # Match partiel (nom de famille du candidat PQTV)
        parts_pqtv = nom_pqtv.split()
        if len(parts_pqtv) >= 2:
            famille_pqtv = parts_pqtv[-1]  # dernier mot = nom de famille
            if famille_pqtv == nom_famille_off:
                return off
            # Essai avec les 2 derniers mots (noms composés)
            if len(parts_pqtv) >= 3:
                famille_pqtv_2 = ' '.join(parts_pqtv[-2:])
                if famille_pqtv_2 == nom_famille_off:
                    return off

    return None



# Grandes villes françaises > 40 000 hab NON dans PQTV qu'on pourrait ajouter
# Code INSEE -> (nom, département, population approx)
GRANDES_VILLES_FRANCE = {
    # > 100k
    '44109': ('Nantes', '44', 320000),
    '34172': ('Montpellier', '34', 295000),
    '06088': ('Nice', '06', 342000),
    '31555': ('Toulouse', '31', 493000),
    '13055': ('Marseille', '13', 873000),
    '69123': ('Lyon', '69', 516000),
    '75056': ('Paris', '75', 2161000),
    '33063': ('Bordeaux', '33', 259000),
    '59350': ('Lille', '59', 236000),
    '67482': ('Strasbourg', '67', 287000),
    '35238': ('Rennes', '35', 222000),
    '76540': ('Rouen', '76', 113000),
    '51454': ('Reims', '51', 182000),
    '42218': ('Saint-Étienne', '42', 174000),
    '87085': ('Limoges', '87', 132000),
    '63113': ('Clermont-Ferrand', '63', 147000),
    '37261': ('Tours', '37', 138000),
    '80021': ('Amiens', '80', 135000),
    '21231': ('Dijon', '21', 158000),
    '49007': ('Angers', '49', 155000),
    '72181': ('Le Mans', '72', 145000),
    '25056': ('Besançon', '25', 120000),
    '84007': ('Avignon', '84', 92000),
    '30189': ('Nîmes', '30', 151000),
    '66136': ('Perpignan', '66', 122000),
    '64445': ('Pau', '64', 77000),
    '17300': ('La Rochelle', '17', 78000),
    # 50k-100k villes pas encore dans PQTV potentiellement
    '91228': ('Évry-Courcouronnes', '91', 68000),
    '77288': ('Meaux', '77', 56000),
    '95268': ('Garges-lès-Gonesse', '95', 43000),
    '93029': ('Épinay-sur-Seine', '93', 55000),
    '93066': ('Saint-Denis', '93', 113000),
    '93048': ('Montreuil', '93', 109000),
    '93008': ('Bobigny', '93', 53000),
    '93053': ('Noisy-le-Grand', '93', 69000),
    '93055': ('Pantin', '93', 58000),
    '93073': ('Tremblay-en-France', '93', 38000),
    '94028': ('Créteil', '94', 92000),
    '94081': ('Vitry-sur-Seine', '94', 94000),
    '94041': ('Ivry-sur-Seine', '94', 61000),
    '92050': ('Nanterre', '92', 96000),
    '92051': ('Neuilly-sur-Seine', '92', 61000),
    '92063': ('Rueil-Malmaison', '92', 79000),
    '92044': ('Levallois-Perret', '92', 66000),
    '92040': ('Issy-les-Moulineaux', '92', 69000),
    '78646': ('Versailles', '78', 85000),
    '78586': ('Sartrouville', '78', 51000),
    '95585': ('Sarcelles', '95', 58000),
    '60057': ('Beauvais', '60', 56000),
    '02691': ('Saint-Quentin', '02', 55000),
    '57463': ('Metz', '57', 118000),
    '54395': ('Nancy', '54', 105000),
    '68224': ('Mulhouse', '68', 110000),
    '68066': ('Colmar', '68', 70000),
    '56260': ('Vannes', '56', 55000),
    '56121': ('Lorient', '56', 57000),
    '29019': ('Brest', '29', 139000),
    '22278': ('Saint-Brieuc', '22', 45000),
    '50129': ('Cherbourg-en-Cotentin', '50', 79000),
    '14118': ('Caen', '14', 108000),
    '76351': ('Le Havre', '76', 169000),
    '27229': ('Évreux', '27', 51000),
    '45234': ('Orléans', '45', 116000),
    '18033': ('Bourges', '18', 66000),
    '36044': ('Châteauroux', '36', 44000),
    '86194': ('Poitiers', '86', 90000),
    '16015': ('Angoulême', '16', 42000),
    '79191': ('Niort', '79', 60000),
    '24322': ('Périgueux', '24', 30000),
    '33281': ('Mérignac', '33', 72000),
    '33318': ('Pessac', '33', 65000),
    '40192': ('Mont-de-Marsan', '40', 32000),
    '64102': ('Bayonne', '64', 52000),
    '65440': ('Tarbes', '65', 41000),
    '81004': ('Albi', '81', 49000),
    '12202': ('Rodez', '12', 24000),
    '46042': ('Cahors', '46', 20000),
    '82121': ('Montauban', '82', 60000),
    '34032': ('Béziers', '34', 78000),
    '11262': ('Narbonne', '11', 55000),
    '11069': ('Carcassonne', '11', 47000),
    '13001': ('Aix-en-Provence', '13', 145000),
    '83137': ('Toulon', '83', 176000),
    '83061': ('Fréjus', '83', 54000),
    '06004': ('Antibes', '06', 74000),
    '06029': ('Cannes', '06', 75000),
    '20004': ('Ajaccio', '2A', 71000),
    '20033': ('Bastia', '2B', 48000),
    '97105': ('Pointe-à-Pitre', '971', 15000),
    '97209': ('Fort-de-France', '972', 78000),
    '97302': ('Cayenne', '973', 64000),
    '97411': ('Saint-Denis', '974', 154000),
    '97415': ('Saint-Paul', '974', 105000),
    '97416': ('Saint-Pierre', '974', 84000),
    '97422': ('Le Tampon', '974', 80000),
    '97608': ('Mamoudzou', '976', 71000),
    '01053': ('Bourg-en-Bresse', '01', 42000),
    '38185': ('Grenoble', '38', 158000),
    '73011': ('Chambéry', '73', 61000),
    '74010': ('Annecy', '74', 130000),
    '26362': ('Valence', '26', 65000),
    '43157': ('Le Puy-en-Velay', '43', 19000),
    '03185': ('Montluçon', '03', 35000),
    '03310': ('Vichy', '03', 25000),
    '69266': ('Villeurbanne', '69', 152000),
    '69259': ('Vénissieux', '69', 66000),
    '01283': ('Oyonnax', '01', 23000),
    '88160': ('Épinal', '88', 32000),
    '70550': ('Vesoul', '70', 15000),
    '39198': ('Dole', '39', 24000),
    '90010': ('Belfort', '90', 47000),
    '10387': ('Troyes', '10', 61000),
    '08105': ('Charleville-Mézières', '08', 47000),
    '59606': ('Villeneuve-d\'Ascq', '59', 62000),
    '59512': ('Roubaix', '59', 98000),
    '59599': ('Tourcoing', '59', 98000),
    '62041': ('Arras', '62', 41000),
    '62160': ('Calais', '62', 72000),
    '59178': ('Dunkerque', '59', 87000),
    '62498': ('Lens', '62', 31000),
    '59392': ('Maubeuge', '59', 29000),
    '02408': ('Laon', '02', 25000),
}


def find_large_cities_to_add(officiel, pqtv):
    """
    Identifie les grandes villes françaises absentes de PQTV
    en croisant notre liste de grandes villes avec le CSV officiel.
    """
    pqtv_keys_norm = set()
    for (nom, dept) in pqtv.keys():
        pqtv_keys_norm.add((normalize_name(nom), dept))

    # Aussi indexer par code circo pour les villes PQTV
    pqtv_circo_codes = set()
    for data in pqtv.values():
        cp = data.get('codePostal', '')
        if cp:
            pqtv_circo_codes.add(cp)

    candidates = []
    for code_insee, (nom_ref, dept_ref, pop) in GRANDES_VILLES_FRANCE.items():
        # Vérifier si déjà dans PQTV
        norm = normalize_name(nom_ref)
        if (norm, dept_ref) in pqtv_keys_norm:
            continue

        # Chercher dans le CSV officiel
        off_key = None
        for (circo, dept) in officiel.keys():
            if dept == dept_ref and normalize_name(circo) == norm:
                off_key = (circo, dept)
                break

        if off_key:
            listes = officiel[off_key]
            candidates.append({
                'nom': nom_ref,
                'departement': dept_ref,
                'population': pop,
                'code_insee': code_insee,
                'nb_listes': len(listes),
                'listes': [
                    f"{l['nom']} ({l['nuance'] or l['nuance_code'] or '?'})"
                    for l in listes
                ],
            })

    candidates.sort(key=lambda x: x['population'], reverse=True)
    return candidates


def main():
    print("=" * 80)
    print("COMPARAISON PQTV vs DONNÉES OFFICIELLES (data.gouv.fr)")
    print("=" * 80)

    print("\n📥 Chargement des données PQTV...")
    pqtv = load_pqtv_data()
    print(f"   {len(pqtv)} villes, {sum(len(v['candidats']) for v in pqtv.values())} candidats")

    print("\n📥 Chargement du CSV officiel...")
    officiel = load_official_data()
    print(f"   {len(officiel)} circonscriptions, {sum(len(v) for v in officiel.values())} têtes de liste")

    officiel_keys = set(officiel.keys())

    # =========================================================================
    # 1. COMPARAISON PAR VILLE
    # =========================================================================
    print("\n" + "=" * 80)
    print("1. COMPARAISON DES CANDIDATS PAR VILLE")
    print("=" * 80)

    total_manquants = 0
    total_en_trop = 0
    total_ok = 0
    villes_non_trouvees = []

    rapport_villes = []

    for (nom_ville, dept_ville), data in sorted(pqtv.items()):
        match = match_ville(nom_ville, dept_ville, officiel_keys)

        if not match:
            villes_non_trouvees.append(f"{nom_ville} (dép. {dept_ville})")
            continue

        off_listes = officiel[match]
        pqtv_cands = data['candidats']

        manquants = []
        en_trop = []
        matches = []
        nuances = []

        off_matched = set()

        for cand in pqtv_cands:
            off_match = match_candidat(cand, off_listes)
            if off_match:
                off_matched.add(off_match['nom'])
                matches.append((cand, off_match))
                if off_match.get('nuance'):
                    nuances.append({
                        'candidat': cand['nom'],
                        'nuance_officielle': off_match['nuance'],
                        'nuance_code': off_match['nuance_code'],
                        'liste_pqtv': cand['liste'],
                    })
            else:
                en_trop.append(cand)

        for off in off_listes:
            if off['nom'] not in off_matched:
                manquants.append(off)

        if manquants or en_trop:
            rapport_villes.append({
                'ville': nom_ville,
                'pqtv_count': len(pqtv_cands),
                'officiel_count': len(off_listes),
                'manquants': manquants,
                'en_trop': en_trop,
                'nuances': nuances,
            })

        total_manquants += len(manquants)
        total_en_trop += len(en_trop)
        total_ok += len(matches)

    # Afficher le rapport
    for r in rapport_villes:
        print(f"\n{'─' * 60}")
        print(f"🏙️  {r['ville']} — PQTV: {r['pqtv_count']} | Officiel: {r['officiel_count']}")

        if r['manquants']:
            print(f"  ❌ MANQUANTS dans PQTV ({len(r['manquants'])}):")
            for m in r['manquants']:
                nuance_str = f" [{m['nuance'] or m['nuance_code']}]" if (m['nuance'] or m['nuance_code']) else ""
                print(f"     + {m['nom']}{nuance_str}")
                print(f"       Liste: {m['liste_abregee']}")

        if r['en_trop']:
            print(f"  ⚠️  EN TROP dans PQTV ({len(r['en_trop'])}) — pas trouvé dans l'officiel:")
            for e in r['en_trop']:
                print(f"     - {e['nom']} ({e['liste']})")

    print(f"\n{'=' * 60}")
    print(f"BILAN CANDIDATS:")
    print(f"  ✅ Correspondances trouvées : {total_ok}")
    print(f"  ❌ Manquants dans PQTV      : {total_manquants}")
    print(f"  ⚠️  En trop dans PQTV        : {total_en_trop}")

    if villes_non_trouvees:
        print(f"\n  🔍 Villes PQTV non trouvées dans le CSV officiel ({len(villes_non_trouvees)}):")
        for v in villes_non_trouvees:
            print(f"     ? {v}")

    # =========================================================================
    # 2. NUANCES POLITIQUES
    # =========================================================================
    print("\n" + "=" * 80)
    print("2. NUANCES POLITIQUES OFFICIELLES")
    print("=" * 80)

    all_nuances = []
    for (nom_ville, dept_ville), data in sorted(pqtv.items()):
        match = match_ville(nom_ville, dept_ville, officiel_keys)
        if not match:
            continue
        for cand in data['candidats']:
            off = match_candidat(cand, officiel[match])
            if off and (off.get('nuance') or off.get('nuance_code')):
                all_nuances.append({
                    'ville': nom_ville,
                    'candidat': cand['nom'],
                    'nuance_code': off['nuance_code'],
                    'nuance': off['nuance'],
                    'liste_pqtv': cand['liste'],
                    'liste_officielle': off['liste_abregee'],
                })

    # Résumé par nuance
    nuance_counts = defaultdict(int)
    for n in all_nuances:
        key = f"{n['nuance_code']} — {n['nuance']}" if n['nuance'] else n['nuance_code']
        nuance_counts[key] += 1

    print(f"\n  Distribution des nuances ({len(all_nuances)} candidats avec nuance):")
    for nuance, count in sorted(nuance_counts.items(), key=lambda x: -x[1]):
        print(f"    {count:3d}x  {nuance}")

    # =========================================================================
    # 3. GRANDES VILLES À AJOUTER
    # =========================================================================
    print("\n" + "=" * 80)
    print("3. GRANDES VILLES FRANÇAISES À AJOUTER")
    print("=" * 80)

    new_cities = find_large_cities_to_add(officiel, pqtv)

    if new_cities:
        print(f"\n  {len(new_cities)} grandes villes absentes de PQTV (triées par population)")
        for i, city in enumerate(new_cities):
            print(f"\n  {i+1:2d}. {city['nom']} (dép. {city['departement']}, ~{city['population']//1000}k hab) — {city['nb_listes']} listes")
            for l in city['listes']:
                print(f"      • {l}")
    else:
        print("\n  ✅ Toutes les grandes villes de la liste de référence sont déjà dans PQTV !")


if __name__ == '__main__':
    main()
