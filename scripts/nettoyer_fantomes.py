#!/usr/bin/env python3
"""
Nettoie les propositions orphelines (IDs fantômes) dans les fichiers elections/*.json
après suppression de candidats par sync_datagouv.py.
"""

import json
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELECTIONS_DIR = os.path.join(BASE_DIR, 'data', 'elections')


def main():
    total_cleaned = 0
    files_modified = 0

    for filename in sorted(os.listdir(ELECTIONS_DIR)):
        if not filename.endswith('.json'):
            continue

        filepath = os.path.join(ELECTIONS_DIR, filename)
        with open(filepath, encoding='utf-8') as f:
            data = json.load(f)

        candidat_ids = {c['id'] for c in data.get('candidats', [])}
        categories = data.get('categories', [])
        modified = False

        for cat in categories:
            for st in cat.get('sousThemes', []):
                new_propositions = {}
                for cand_id, props in st.get('propositions', {}).items():
                    if cand_id in candidat_ids:
                        new_propositions[cand_id] = props
                    else:
                        total_cleaned += len(props) if isinstance(props, list) else 1
                        modified = True

                if len(new_propositions) != len(st.get('propositions', {})):
                    st['propositions'] = new_propositions

        if modified:
            files_modified += 1
            ville = data.get('ville', filename)
            print(f"  🧹 {ville}: propositions fantômes nettoyées")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'─' * 40}")
    print(f"  {total_cleaned} propositions orphelines supprimées")
    print(f"  {files_modified} fichiers modifiés")


if __name__ == '__main__':
    main()
