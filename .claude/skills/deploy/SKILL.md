---
name: deploy
description: Pipeline de déploiement complet du site pourquituvotes.fr. S'active quand l'utilisateur demande de déployer, publier, pusher en prod, ou mettre en ligne. Vérifie tout avant de pusher.
---

# Pipeline de déploiement

Workflow complet de vérification et déploiement du site.

## Entrée

`$ARGUMENTS` : optionnel, message de contexte (ex: "après intégration Belhamiti")

## Étape 1 — Validation des données

```bash
python scripts/valider_donnees.py
```

Analyser le résultat :
- **Erreurs nouvelles** (liées aux changements en cours) : STOP et corriger avant de continuer
- **Erreurs préexistantes** (villes stub sans données, candidats à 0 propositions) : OK de continuer, les signaler
- Vérifier spécifiquement les fichiers modifiés : `python scripts/valider_donnees.py 2>&1 | grep -i "{ville}"` pour les villes touchées
- Les "0 categories" sur les villes stub ne sont PAS bloquantes (ce sont des villes sans programme intégré)

## Étape 2 — Regénérer les statistiques

```bash
python scripts/calculer_metriques.py
python scripts/regenerer_stats_villes.py --apply
```

Regénérer `stats-global.json` avec un script Python inline :
- Lire tous les fichiers `data/elections/*.json`
- Compter les mesures par catégorie, total candidats, total propositions, total complets
- Écrire le résultat dans `data/stats-global.json`
- (Voir le skill /stats pour le script complet)

## Étape 3 — Regénérer les shells statiques

```bash
python scripts/generate_static_shells.py
```

Vérifie que le `_redirects` n'a pas été écrasé (les redirects custom doivent rester).

## Étape 4 — Bumper DATA_VERSION

Incrémenter `DATA_VERSION` dans :
- `js/app.js`
- `js/home.js`

Format : `YYYYMMDDNN` (date + numéro séquentiel).

Vérifier aussi que les 103 pages SEO dans `municipales-2026/*/index.html` utilisent la version à jour dans leurs `?v=` query strings.

## Étape 5 — Vérifications SEO rapides

```bash
# Pas d'URLs .html dans le sitemap
grep '\.html</loc>' sitemap.xml

# Canonical cohérent sur la page principale
grep 'rel="canonical"' municipales/2026/index.html

# Pas de fichiers non-trackés sensibles
git status
```

## Étape 6 — Commit et push

```bash
git add -A
# Vérifier qu'on ne commite pas de fichiers sensibles (.env, credentials)
git status
git commit -m "deploy: mise à jour prod ({contexte})

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push
```

## Étape 7 — Vérification post-déploiement

Après le push (Cloudflare Pages déploie automatiquement) :
- Vérifier que le site répond sur https://pourquituvotes.fr
- Vérifier qu'une page ville charge correctement (ex: /municipales-2026/paris/)
- Vérifier que les stats sont à jour sur /stats.html
- Signaler si GA4/GTM risque d'être impacté

## Résumé final

Afficher :
- Nombre de fichiers modifiés
- Nouvelles stats (villes, candidats, mesures)
- DATA_VERSION actuelle
- URL du site live
