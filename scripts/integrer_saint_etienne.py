#!/usr/bin/env python3
"""
Intégration des programmes Juanico, Le Jaouen et Chassaubéné
pour Saint-Étienne 2026.
Lit les mappings générés par les agents et les injecte dans le JSON.
"""
import json
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
ELECTION_FILE = os.path.join(DATA_DIR, "elections", "saint-etienne-2026.json")

# Load mappings
def load_mapping(filename, var_name):
    filepath = os.path.join(DATA_DIR, "programmes", filename)
    ns = {}
    with open(filepath, encoding='utf-8') as f:
        exec(f.read(), ns)
    return ns[var_name]

print("Chargement des mappings...")
juanico = load_mapping("juanico_mapping.py", "JUANICO_MEASURES")
le_jaouen = load_mapping("le_jaouen_mapping.py", "LE_JAOUEN_MEASURES")
chassaubene = load_mapping("chassaubene_mapping.py", "CHASSAUBENE_MEASURES")

print(f"  Juanico: {sum(len(v) for v in juanico.values())} mesures")
print(f"  Le Jaouen: {sum(len(v) for v in le_jaouen.values())} mesures")
print(f"  Chassaubéné: {sum(len(v) for v in chassaubene.values())} mesures")

# Load election data
with open(ELECTION_FILE, encoding='utf-8') as f:
    data = json.load(f)

# Mapping: candidate_id -> measures dict
CANDIDATES = {
    "juanico": juanico,
    "le-jaouen": le_jaouen,
    "chassaubene": chassaubene,
}

# Count before
def count_measures(data, cid):
    total = 0
    for cat in data.get("categories", []):
        for st in cat.get("sousThemes", []):
            val = st.get("propositions", {}).get(cid)
            if val and val.get("mesures"):
                total += len(val["mesures"])
    return total

for cid in CANDIDATES:
    print(f"  {cid} avant: {count_measures(data, cid)} mesures")

# Inject measures
for cat in data.get("categories", []):
    for st in cat.get("sousThemes", []):
        st_id = st["id"]
        if "propositions" not in st:
            st["propositions"] = {}

        for cid, measures_dict in CANDIDATES.items():
            if st_id in measures_dict and measures_dict[st_id]:
                mesures_list = [{"texte": m} for m in measures_dict[st_id]]
                st["propositions"][cid] = {
                    "mesures": mesures_list,
                    "source": None
                }

# Update candidat metadata
for c in data["candidats"]:
    if c["id"] in CANDIDATES:
        c["programmeComplet"] = True
        if c["id"] == "juanico":
            c["programmeUrl"] = "https://juanico2026.fr/programme/"
            c["programmePdfPath"] = "data/programmes/juanico_programme_2026.pdf"
        elif c["id"] == "le-jaouen":
            c["programmeUrl"] = "https://www.lejaouen2026.fr/wp-content/uploads/2026/02/PROJET-ELJ-V4.pdf"
            c["programmePdfPath"] = "data/programmes/le_jaouen_projet_v4.pdf"
        elif c["id"] == "chassaubene":
            c["programmeUrl"] = "https://www.marc-chassaubene-2026.fr/#programme"
            c["programmePdfPath"] = "data/programmes/chassaubene_programme_2026.pdf"

# Count after
for cid in CANDIDATES:
    print(f"  {cid} après: {count_measures(data, cid)} mesures")

# Safety check
for cid, measures_dict in CANDIDATES.items():
    expected = sum(len(v) for v in measures_dict.values())
    actual = count_measures(data, cid)
    if actual < expected * 0.5:
        print(f"ERREUR: {cid} n'a que {actual}/{expected} mesures intégrées!")
        sys.exit(1)

# Write
with open(ELECTION_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nFichier écrit: {ELECTION_FILE}")
print("OK!")
