---
name: stats
description: Regénérer toutes les statistiques du site pourquituvotes.fr. S'active automatiquement après chaque intégration de programme candidat (après /integrer) ou quand l'utilisateur demande de mettre à jour les stats, métriques ou chiffres du site.
allowed-tools: Bash, Read, Grep
---

# Regénération des statistiques

Regénère toutes les statistiques du projet en séquence et affiche un résumé.

## Étape 1 — Regénérer metriques.json

```bash
python scripts/calculer_metriques.py
```

Ce script lit tous les `data/elections/*.json` et génère `data/metriques.json` (métriques nationales, par ville, par candidat).

## Étape 2 — Regénérer stats-global.json

```bash
python -c "
import json, sys, os
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
counts = defaultdict(int)
for f in os.listdir('data/elections'):
    if not f.endswith('.json'): continue
    with open(os.path.join('data/elections', f), 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    for cat in data.get('categories', []):
        for st in cat.get('sousThemes', []):
            for cid, prop in st.get('propositions', {}).items():
                if prop and prop.get('mesures'):
                    counts[cat['id']] += len(prop['mesures'])
sorted_cats = sorted(counts.items(), key=lambda x: -x[1])
result = {'categories': [{'id': cid, 'count': cnt} for cid, cnt in sorted_cats]}
with open('data/stats-global.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print('stats-global.json regénéré')
for cid, cnt in sorted_cats:
    print(f'  {cid}: {cnt}')
print(f'Total: {sum(counts.values())}')
"
```

## Étape 3 — Regénérer villes.json

```bash
python scripts/regenerer_stats_villes.py --apply
```

## Étape 4 — Résumé

Afficher un résumé avec :
- Nombre total de villes, candidats, mesures
- Top 3 thèmes
- Nombre de candidats avec programmeComplet: true
- Changements par rapport aux stats précédentes si possible

## Étape 5 — Commit (optionnel)

Demander à l'utilisateur s'il veut commiter les stats mises à jour. Si oui :

```bash
git add data/metriques.json data/stats-global.json data/villes.json
git commit -m "chore: regénérer stats (X mesures, Y candidats complets)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```
