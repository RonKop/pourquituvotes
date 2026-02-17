#!/usr/bin/env python3
"""Fusionne contacts_candidats + suivi_candidats en un seul fichier trié par population."""
import csv
import os

BASE = os.path.join(os.path.dirname(__file__), '..')
SUIVI = os.path.join(BASE, 'data', 'suivi_candidats.csv')
CONTACTS = os.path.join(BASE, 'data', 'contacts_candidats.csv')
OUTPUT = os.path.join(BASE, 'data', 'candidats_municipales_2026.csv')

FRANCE_POP = 67_750_000  # population totale France 2024

# Populations communales (INSEE 2021-2022, arrondies)
POPULATIONS = {
    "Paris": 2_145_906,
    "Marseille": 873_076,
    "Lyon": 522_969,
    "Toulouse": 504_078,
    "Nice": 342_669,
    "Nantes": 320_732,
    "Montpellier": 295_542,
    "Strasbourg": 290_576,
    "Bordeaux": 260_958,
    "Lille": 236_234,
    "Rennes": 222_485,
    "Reims": 182_460,
    "Toulon": 176_198,
    "Saint-Étienne": 174_082,
    "Le Havre": 169_733,
    "Dijon": 159_346,
    "Grenoble": 158_198,
    "Angers": 155_850,
    "Villeurbanne": 154_781,
    "Saint-Denis (La Réunion)": 154_766,
    "Nîmes": 148_561,
    "Le Mans": 148_340,
    "Clermont-Ferrand": 147_865,
    "Aix-en-Provence": 147_477,
    "Brest": 142_722,
    "Tours": 136_463,
    "Amiens": 136_105,
    "Annecy": 133_926,
    "Limoges": 130_592,
    "Perpignan": 121_875,
    "Boulogne-Billancourt": 121_334,
    "Metz": 120_205,
    "Besançon": 119_199,
    "Orléans": 116_685,
    "Argenteuil": 113_816,
    "Rouen": 114_007,
    "Saint-Denis": 113_131,
    "Montreuil": 111_260,
    "Mulhouse": 108_038,
    "Caen": 106_260,
    "Saint-Paul (La Réunion)": 105_240,
    "Nancy": 104_885,
    "Roubaix": 99_301,
    "Tourcoing": 98_656,
    "Nanterre": 96_689,
    "Vitry-sur-Seine": 94_649,
    "Créteil": 93_057,
    "Avignon": 92_130,
    "Poitiers": 90_032,
    "Aubervilliers": 89_079,
    "Asnières-sur-Seine": 87_764,
    "Aulnay-sous-Bois": 86_752,
    "Dunkerque": 86_279,
    "Versailles": 85_272,
    "Colombes": 85_199,
    "Saint-Pierre (La Réunion)": 84_234,
    "Béziers": 79_563,
    "La Rochelle": 79_119,
    "Cherbourg-en-Cotentin": 78_875,
    "Champigny-sur-Marne": 77_890,
    "Saint-Maur-des-Fossés": 77_261,
    "Pau": 77_215,
    "Cannes": 74_285,
    "Mérignac": 74_348,
    "Antibes": 73_438,
    "Ajaccio": 73_822,
    "Saint-Nazaire": 73_546,
    "Calais": 72_929,
    "Drancy": 72_498,
    "Colmar": 70_284,
    "Issy-les-Moulineaux": 69_023,
    "Évry-Courcouronnes": 69_134,
    "Noisy-le-Grand": 68_238,
    "Vénissieux": 67_479,
    "Cergy": 67_311,
    "Bourges": 66_328,
    "Levallois-Perret": 66_082,
    "Pessac": 66_027,
    "La Seyne-sur-Mer": 65_105,
    "Valence": 65_313,
    "Cayenne": 64_709,
    "Quimper": 63_929,
    "Antony": 63_541,
    "Clichy": 63_329,
    "Montauban": 62_860,
    "Troyes": 62_612,
    "Villeneuve-d'Ascq": 62_308,
    "Ivry-sur-Seine": 62_695,
    "Le Tampon (La Réunion)": 81_614,
    "Chambéry": 60_590,
    "Niort": 60_775,
    "Neuilly-sur-Seine": 60_454,
    "Fort-de-France": 75_714,
    "Villejuif": 59_602,
    "Pantin": 58_924,
    "Lorient": 57_408,
    "Le Blanc-Mesnil": 57_246,
    "Fréjus": 55_735,
    "Rueil-Malmaison": 80_622,
    "Courbevoie": 81_905,
    "Le Chesnay-Rocquencourt": 29_290,
    "Puteaux": 45_448,
    "Volvic": 4_625,
}


def get_population(ville):
    """Cherche la population, avec fallback sur match partiel."""
    if ville in POPULATIONS:
        return POPULATIONS[ville]
    # Match partiel
    for key, pop in POPULATIONS.items():
        if ville in key or key in ville:
            return pop
    return 0


def main():
    # Lire suivi_candidats.csv (fichier maître)
    with open(SUIVI, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)

    # Enrichir depuis contacts_candidats.csv (emails manquants)
    contacts_map = {}
    with open(CONTACTS, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('email'):
                key = (row['nom'].strip().split()[-1].lower(), row['ville'].strip().lower())
                contacts_map[key] = row

    # Compléter les emails manquants
    enriched = 0
    for row in rows:
        if not row.get('email'):
            nom_famille = row['candidat'].strip().split()[-1].lower()
            ville = row['ville'].strip().lower()
            contact = contacts_map.get((nom_famille, ville))
            if contact and contact.get('email'):
                row['email'] = contact['email']
                row['type_email'] = contact.get('type_email', '')
                row['source_contact'] = contact.get('source', '')
                row['statut_contact'] = 'EMAIL OK'
                enriched += 1

    # Ajouter population et %
    for row in rows:
        pop = get_population(row['ville'])
        row['population'] = str(pop) if pop else ''
        row['pct_france'] = f"{pop / FRANCE_POP * 100:.2f}" if pop else ''

    # Trier par population décroissante, puis ville, puis candidat
    rows.sort(key=lambda r: (-int(r['population'] or '0'), r['ville'], r['candidat']))

    # Écrire le fichier final
    fieldnames = [
        'ville', 'population', 'pct_france',
        'candidat', 'id', 'liste',
        'programme_complet', 'nb_propositions', 'site_campagne',
        'email', 'type_email', 'twitter',
        'source_contact', 'statut_contact'
    ]

    with open(OUTPUT, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

    # Stats
    total = len(rows)
    villes = len(set(r['ville'] for r in rows))
    with_email = sum(1 for r in rows if r.get('email'))
    with_twitter = sum(1 for r in rows if r.get('twitter'))
    with_contact = sum(1 for r in rows if r.get('email') or r.get('twitter'))
    with_pop = sum(1 for r in rows if r.get('population') and r['population'] != '0')

    # Top 20 villes par population
    villes_pop = {}
    for r in rows:
        v = r['ville']
        if v not in villes_pop:
            villes_pop[v] = {
                'pop': int(r['population'] or '0'),
                'total': 0, 'email': 0, 'twitter': 0
            }
        villes_pop[v]['total'] += 1
        if r.get('email'):
            villes_pop[v]['email'] += 1
        if r.get('twitter'):
            villes_pop[v]['twitter'] += 1

    print(f"\n{'='*60}")
    print(f"FICHIER FUSIONNÉ : {os.path.basename(OUTPUT)}")
    print(f"{'='*60}")
    print(f"Total candidats : {total}")
    print(f"Total villes : {villes}")
    print(f"Avec population : {with_pop}")
    print(f"Avec email : {with_email} ({with_email*100//total}%)")
    print(f"Avec Twitter : {with_twitter} ({with_twitter*100//total}%)")
    print(f"Contactables : {with_contact} ({with_contact*100//total}%)")
    if enriched:
        print(f"Emails enrichis depuis contacts_candidats.csv : {enriched}")

    print(f"\n{'='*60}")
    print(f"TOP 20 VILLES PAR POPULATION (priorité contact)")
    print(f"{'='*60}")
    print(f"{'Ville':<30} {'Pop':>10} {'%FR':>6} {'Cand':>5} {'Email':>6} {'Twitter':>8}")
    print("-" * 70)

    sorted_villes = sorted(villes_pop.items(), key=lambda x: -x[1]['pop'])
    for ville, data in sorted_villes[:20]:
        pct = data['pop'] / FRANCE_POP * 100
        print(f"{ville:<30} {data['pop']:>10,} {pct:>5.2f}% {data['total']:>5} {data['email']:>6} {data['twitter']:>8}")

    print(f"\n{'='*60}")
    print(f"VILLES SANS AUCUN CONTACT EMAIL")
    print(f"{'='*60}")
    no_email_villes = [(v, d) for v, d in sorted_villes if d['email'] == 0 and d['pop'] > 50000]
    for ville, data in no_email_villes:
        print(f"  {ville:<30} {data['pop']:>10,} hab. — {data['total']} candidats, 0 email")

    print(f"\nFichier écrit : {OUTPUT}")
    print(f"→ Importable dans Google Sheets : Fichier > Importer > CSV, séparateur point-virgule")


if __name__ == '__main__':
    main()
