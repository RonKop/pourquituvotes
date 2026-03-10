#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour vérifier les propositions de Thomas Rousseau
"""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

JSON_PATH = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\rennes-2026.json"

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

candidat = [c for c in data['candidats'] if c['id'] == 'trousseau'][0]

print('='*70)
print('RÉSUMÉ - Thomas Rousseau (L\'Espoir Rennais - LR)')
print('='*70)
print(f'\nProgramme complet: {candidat["programmeComplet"]}')
print(f'\nNombre total de propositions: {sum(1 for cat in data["categories"] for st in cat["sousThemes"] if st["propositions"].get("trousseau"))}')
print('\nRépartition par catégorie:')
print('-'*70)

for cat in data['categories']:
    count = sum(1 for st in cat['sousThemes'] if st['propositions'].get('trousseau'))
    if count > 0:
        print(f'{cat["nom"]:45s} : {count:2d} proposition(s)')

print('='*70)
