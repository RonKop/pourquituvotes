"""Ajouter les têtes de liste manquantes depuis le CSV data.gouv.fr des candidatures municipales 2026."""
import json, csv, sys, io, re, os, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def slugify(text):
    """Convert text to a slug ID."""
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def make_candidate_id(nom, prenom):
    """Create candidate ID from last name (or first+last if collision)."""
    return slugify(nom)

# Nuance code to human-readable label
NUANCE_LABELS = {
    'LEXG': 'Extrême gauche',
    'LCOM': 'Parti Communiste',
    'LFI': 'La France Insoumise',
    'LSOC': 'Parti Socialiste',
    'LDVG': 'Divers gauche',
    'LVEC': 'Écologistes',
    'LECO': 'Écologistes',
    'LRDG': 'Parti Radical de Gauche',
    'LUG': 'Union de la gauche',
    'LDVC': 'Divers centre',
    'LREM': 'Renaissance',
    'LMDM': 'MoDem',
    'LHZN': 'Horizons',
    'LUC': 'Union du centre',
    'LLR': 'Les Républicains',
    'LUDI': 'Union de la droite et du centre',
    'LUD': 'Union de la droite',
    'LDVD': 'Divers droite',
    'LRN': 'Rassemblement National',
    'LREC': 'Reconquête',
    'LEXD': 'Extrême droite',
    'LDIV': 'Divers',
    'LDSV': 'Divers souverainiste',
    'LUXD': 'Union extrême droite',
}

# Load our cities
with open(os.path.join(BASE, 'data/villes.json'), 'r', encoding='utf-8') as f:
    villes = json.load(f)

# Build name -> ville mapping
name_to_ville = {}
for v in villes:
    base = re.sub(r'\s*\(.*?\)', '', v['nom']).strip().lower()
    name_to_ville[base] = v
    name_to_ville[v['nom'].lower()] = v

# Special cases for CSV names that differ
SPECIAL_MAPPINGS = {
    'saint-denis': None,  # Ambiguous (93 vs Réunion), skip
    'saint-etienne': None,  # Accent issue
    'evry-courcouronnes': None,  # Accent issue
}

# Try to fix accent issues
for v in villes:
    base = re.sub(r'\s*\(.*?\)', '', v['nom']).strip()
    base_no_accent = unicodedata.normalize('NFD', base)
    base_no_accent = ''.join(c for c in base_no_accent if unicodedata.category(c) != 'Mn').lower()
    if base_no_accent not in name_to_ville:
        name_to_ville[base_no_accent] = v

# Parse CSV - collect heads of list per city
csv_path = os.path.join(BASE, 'data/candidatures-municipales-2026.csv')
tetes_by_ville = {}

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    seen = set()
    for row in reader:
        circ = row.get('Circonscription', '').strip().strip('"')
        tete = row.get('Tête de liste', '').strip().strip('"')
        ordre = row.get('Ordre', '').strip().strip('"')
        if tete == 'Oui' or ordre == '1':
            nom = row.get('Nom sur le bulletin de vote', '').strip().strip('"')
            prenom = row.get('Prénom sur le bulletin de vote', '').strip().strip('"')
            liste = row.get('Libellé de la liste', '').strip().strip('"')
            nuance = row.get('Code nuance de liste', '').strip().strip('"')
            key = (circ, nom, prenom)
            if key not in seen:
                seen.add(key)
                circ_lower = circ.lower()
                ville = name_to_ville.get(circ_lower)
                if not ville:
                    # Try without accents
                    circ_no_accent = unicodedata.normalize('NFD', circ_lower)
                    circ_no_accent = ''.join(c for c in circ_no_accent if unicodedata.category(c) != 'Mn')
                    ville = name_to_ville.get(circ_no_accent)
                if ville:
                    vid = ville['id']
                    if vid not in tetes_by_ville:
                        tetes_by_ville[vid] = []
                    tetes_by_ville[vid].append({
                        'nom': nom,
                        'prenom': prenom,
                        'nom_complet': f'{prenom} {nom}'.strip().title(),
                        'liste_label': liste,
                        'nuance': nuance,
                    })

print(f"Villes matchées dans CSV: {len(tetes_by_ville)}")

# Process each city
total_added = 0
villes_modified = 0

for v in villes:
    vid = v['id']
    eid = v['elections'][0] if v.get('elections') else None
    if not eid:
        continue

    fpath = os.path.join(BASE, f'data/elections/{eid}.json')
    if not os.path.exists(fpath):
        continue

    csv_cands = tetes_by_ville.get(vid, [])
    if not csv_cands:
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    existing_names = set()
    existing_ids = set()
    for c in data.get('candidats', []):
        # Store last name lowercase for matching
        parts = c['nom'].split()
        for p in parts:
            existing_names.add(p.lower())
        existing_ids.add(c['id'])

    # Find missing candidates
    missing = []
    for cc in csv_cands:
        last_name_lower = cc['nom'].lower()
        # Check if last name matches any existing candidate
        if last_name_lower not in existing_names:
            missing.append(cc)

    if not missing:
        continue

    villes_modified += 1
    print(f"\n{v['nom']} (+{len(missing)} candidats):")

    for cc in missing:
        # Generate unique ID
        cand_id = slugify(cc['nom'])
        if cand_id in existing_ids:
            cand_id = slugify(f"{cc['prenom']}-{cc['nom']}")
        if cand_id in existing_ids:
            cand_id = slugify(f"{cc['prenom']}-{cc['nom']}-2")
        existing_ids.add(cand_id)

        # Build liste label
        nuance_label = NUANCE_LABELS.get(cc['nuance'], cc['nuance'])
        liste_display = f"{nuance_label}" if nuance_label else "Divers"
        if cc['liste_label']:
            # Use nuance + list name for clarity
            liste_display = f"{nuance_label}, {cc['liste_label']}" if nuance_label else cc['liste_label']

        # Add candidate metadata
        new_cand = {
            "id": cand_id,
            "nom": cc['nom_complet'],
            "liste": liste_display,
            "programmeUrl": "#",
            "programmeComplet": False,
            "programmePdfPath": None,
        }
        data['candidats'].append(new_cand)

        # Add null propositions for all sous-thèmes
        for cat in data['categories']:
            for st in cat['sousThemes']:
                st['propositions'][cand_id] = None

        print(f"  + {cc['nom_complet']} ({nuance_label}) — {cc['liste_label'][:60]}")
        total_added += 1

    # Save
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"TOTAL: {total_added} candidats ajoutés dans {villes_modified} villes")
print(f"{'='*60}")
