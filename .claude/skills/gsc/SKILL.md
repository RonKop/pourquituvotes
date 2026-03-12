---
name: gsc
description: Analyse Google Search Console pour identifier les opportunités SEO. S'active quand l'utilisateur demande de checker la GSC, analyser les performances, trouver des opportunités de mots-clés, ou optimiser le référencement basé sur les données réelles.
user-invocable: true
---

# Google Search Console — Analyse et Optimisation

Accès GSC via le service account du projet (`scripts/google_credentials.json`).
Site : `sc-domain:pourquituvotes.fr`

## Connexion

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
creds = service_account.Credentials.from_service_account_file(
    'scripts/google_credentials.json', scopes=SCOPES
)
service = build('searchconsole', 'v1', credentials=creds)
```

TOUJOURS : `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` (Windows cp1252)

## Étape 1 — Collecter les données brutes

Récupérer les 28 derniers jours, 1000 requêtes max :

```python
request = {
    'startDate': '{28 jours avant}',
    'endDate': '{hier}',
    'dimensions': ['query'],
    'rowLimit': 1000,
    'dataState': 'all'
}
response = service.searchanalytics().query(
    siteUrl='sc-domain:pourquituvotes.fr', body=request
).execute()
```

Aussi récupérer par PAGE pour croiser :

```python
request_pages = {
    'startDate': '{28 jours avant}',
    'endDate': '{hier}',
    'dimensions': ['page'],
    'rowLimit': 500,
    'dataState': 'all'
}
```

Et par QUERY + PAGE pour identifier quelle page se positionne sur quelle requête :

```python
request_query_page = {
    'startDate': '{28 jours avant}',
    'endDate': '{hier}',
    'dimensions': ['query', 'page'],
    'rowLimit': 2000,
    'dataState': 'all'
}
```

## Étape 2 — Identifier les 4 types d'opportunités

### A. Volume caché (impressions élevées, position > 7)
- Requêtes avec beaucoup d'impressions mais en page 2+
- **Action** : identifier la page qui se positionne, optimiser son `<title>` et `<meta description>` pour mieux matcher la requête
- **Seuil** : impressions >= 100 ET position > 7
- **Tri** : par impressions décroissantes

### B. CTR à améliorer (position < 5, CTR < 15%)
- On est bien placé mais les gens ne cliquent pas
- **Action** : réécrire le `<title>` et la `<meta description>` pour être plus attractifs, plus spécifiques
- **Seuil** : position < 5 ET CTR < 15% ET impressions >= 50
- **Tri** : par impressions décroissantes

### C. Presque page 1 (position 4-7, impressions significatives)
- Requêtes proches du top 3, un petit boost suffit
- **Action** : enrichir le contenu de la page (bloc SEO), améliorer le maillage interne, ajouter des mots-clés dans le H1/H2
- **Seuil** : position 4-7 ET impressions >= 80
- **Tri** : par impressions décroissantes

### D. Requêtes sans page dédiée
- Requêtes génériques ("programme municipales {ville}", "candidats {ville} 2026") où on n'a pas de page optimale
- **Action** : vérifier qu'une page ville existe et est bien optimisée, ou identifier un contenu manquant
- Croiser avec la dimension page pour voir quelle URL se positionne

## Étape 3 — Croiser avec les données du site

Pour chaque requête identifiée :
1. Identifier le candidat ou la ville mentionnée dans la requête
2. Vérifier si on a une page dédiée (shell statique dans `municipales-2026/`)
3. Lire le `<title>` et `<meta description>` actuels de cette page
4. Comparer avec la requête : est-ce que le title contient les mots-clés cherchés ?

## Étape 4 — Proposer des actions concrètes

Pour chaque opportunité, proposer UNE action parmi :

### Actions sur `generate_static_shells.py` (impact global)
- Modifier le template de titre des pages candidats (ex: ajouter "municipales 2026 {ville}")
- Modifier le template de meta description
- Ajouter des mots-clés dans les blocs SEO HTML (H2, H3)
- Améliorer le maillage interne (liens vers villes voisines, candidats similaires)

### Actions sur les données JSON (impact par candidat)
- Ajouter des alias ou le nom complet de la liste dans les métadonnées
- Compléter les infos candidat (nuance, étiquette) pour enrichir le contenu

### Actions structurelles
- Créer de nouvelles pages thématiques (enjeux par ville)
- Améliorer le sitemap
- Ajouter des liens internes depuis la home

## Étape 5 — Prioriser (score ICE)

Pour chaque action, calculer :
- **Impact** (1-5) : volume d'impressions touchées, potentiel de clics
- **Confidence** (1-5) : certitude que l'action aura un effet
- **Ease** (1-5) : facilité de mise en oeuvre (1=difficile, 5=trivial)

Score = I × C × E. Trier par score décroissant. Proposer le top 10.

## Étape 6 — Appliquer les changements

Si l'utilisateur valide :
1. Modifier `scripts/generate_static_shells.py` si changement de template
2. OU modifier les JSON si changement de données
3. Regénérer les shells : `python scripts/generate_static_shells.py`
4. Bumper DATA_VERSION dans `js/app.js` et `js/home.js`
5. Valider : `python scripts/valider_donnees.py`
6. Proposer de déployer via `/deploy`

## Étape 7 — Rapport

Afficher un tableau résumé :
```
| # | Requête | Impr | Pos | CTR | Action | Score ICE |
```

Et les totaux : impressions touchées, clics potentiels estimés.

## Patterns de requêtes typiques sur ce site

- `{nom candidat} programme` → page candidat
- `programme {nom candidat} {ville}` → page candidat
- `{nom candidat}` (nom seul) → page candidat
- `candidats municipales {ville} 2026` → page ville
- `municipales {ville} 2026` → page ville
- `programme municipales {ville}` → page ville
- `élections municipales {ville} 2026 candidats` → page ville

## Métriques de référence (mars 2026)

- **CTR moyen position 1** : 30-40%
- **CTR moyen position 2-3** : 15-25%
- **CTR moyen position 4-5** : 8-15%
- **CTR moyen position 6-10** : 3-8%
- **CTR moyen page 2** : 1-3%

Un CTR significativement en dessous de ces moyennes = title/meta à optimiser.
