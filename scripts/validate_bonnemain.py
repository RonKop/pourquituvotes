import json
import sys
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Vérifier que le JSON est valide et compter les propositions
try:
    with open(r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\frejus-2026.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("✓ JSON valide")

    # Compter les propositions de Bonnemain
    bonnemain_data = None
    for candidat in data['candidats']:
        if candidat['id'] == 'bonnemain':
            bonnemain_data = candidat
            break

    propositions_count = 0
    propositions_list = []

    for category in data['categories']:
        for sous_theme in category['sousThemes']:
            if sous_theme['propositions']['bonnemain'] is not None:
                propositions_count += 1
                propositions_list.append(f"  - {category['nom']} > {sous_theme['nom']}")

    print(f"\n✓ Candidat: {bonnemain_data['nom']}")
    print(f"  Liste: {bonnemain_data['liste']}")
    print(f"  programmeComplet: {bonnemain_data['programmeComplet']}")
    print(f"\n✓ Total de propositions: {propositions_count}")
    print(f"\nDétail des propositions:")
    for prop in sorted(propositions_list):
        print(prop)

except json.JSONDecodeError as e:
    print(f"✗ Erreur JSON: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Erreur: {e}")
    sys.exit(1)
