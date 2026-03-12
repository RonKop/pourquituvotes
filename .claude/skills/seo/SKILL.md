---
name: seo
description: Expert SEO technique résident. S'active automatiquement quand on modifie des fichiers HTML, le sitemap, les redirects, les meta tags, les données structurées schema.org, ou le robots.txt. Vérifie aussi avant chaque push que le SEO n'est pas cassé.
user-invocable: false
---

# SEO Expert Résident

Tu es un **expert SEO technique** en plus d'être développeur. Chaque page HTML, chaque modification de structure doit préserver et améliorer le référencement.

## Quand ce skill s'active

Automatiquement quand la tâche touche à :
- Fichiers HTML (meta tags, headings, canonical, OG, structured data)
- `sitemap.xml`, `robots.txt`, `_redirects`
- Données structurées (JSON-LD, schema.org)
- Structure d'URLs, redirections, liens internes
- Performance (lazy loading, taille des ressources)

## Checklist SEO — Vérifier AVANT chaque modification

### 1. Meta Tags (sur chaque page HTML)
- [ ] `<title>` unique, 50-60 caractères, mot-clé principal en premier
- [ ] `<meta name="description">` unique, 150-160 caractères, call-to-action
- [ ] `<link rel="canonical">` présent et correct (URL finale, pas de redirect)
- [ ] `<meta name="robots" content="index, follow">` (sauf pages à exclure)
- [ ] `<html lang="fr">`

### 2. Open Graph + Twitter Cards
- [ ] `og:title`, `og:description`, `og:url`, `og:image` (1200×630px)
- [ ] `og:type` = "website" ou "article"
- [ ] `twitter:card` = "summary_large_image"
- [ ] `og:url` = canonical (identiques)

### 3. Données structurées (JSON-LD)
- [ ] Valide sur https://validator.schema.org/
- [ ] Champs requis présents selon le type :
  - **Event** : name, startDate, endDate, location, eventStatus, eventAttendanceMode, description
  - **Person** : name, description, url, jobTitle
  - **BreadcrumbList** : itemListElement avec position, name, item (avec href)
  - **WebSite** : name, url, potentialAction (SearchAction)
- [ ] Pas de nesting invalide (ex: Event dans knowsAbout est non-standard)
- [ ] Dates en ISO 8601 (YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS)

### 4. Structure HTML
- [ ] Un seul `<h1>` par page
- [ ] Hiérarchie h1 > h2 > h3 sans saut
- [ ] Attributs `alt` sur toutes les images
- [ ] Liens internes avec texte d'ancrage descriptif (pas "cliquez ici")
- [ ] Pas de liens cassés (href="#" sur des liens réels)

### 5. URLs et Redirections
- [ ] URLs propres, en minuscules, avec tirets (pas de underscores)
- [ ] Trailing slash cohérent (toujours ou jamais, pas les deux)
- [ ] Redirections 301 (pas 302) pour les URLs permanentes
- [ ] Sitemap ne contient QUE des URLs finales (pas d'URLs qui redirigent)
- [ ] Canonical = URL dans le sitemap = og:url

### 6. Sitemap
- [ ] Toutes les pages indexables sont dans le sitemap
- [ ] Aucune page noindex dans le sitemap
- [ ] Aucune URL qui redirige dans le sitemap
- [ ] `<lastmod>` à jour
- [ ] Pas d'URLs .html si des clean URLs existent

### 7. Performance SEO
- [ ] LCP ≤ 2.5s (images optimisées, fonts preload)
- [ ] CLS ≤ 0.1 (dimensions sur images/iframes, font-display: swap)
- [ ] Pas de render-blocking CSS/JS inutile
- [ ] `<link rel="preload">` pour les fonts critiques
- [ ] `loading="lazy"` sur les images below-the-fold

### 8. _redirects (Cloudflare Pages)
- [ ] Toutes les anciennes URLs ont un redirect 301
- [ ] Pas de chaînes de redirections (A→B→C)
- [ ] Redirect `.html` → clean URL pour toutes les pages
- [ ] Le script `generate_static_shells.py` n'écrase pas les redirects custom

### 9. Indexation
- [ ] Pas de `noindex` accidentel
- [ ] Pas de canonical pointant vers une autre page par erreur
- [ ] Pas de pages orphelines (liées nulle part)
- [ ] Fil d'Ariane Schema.org BreadcrumbList sur toutes les pages profondes

## Règles spécifiques au projet

- **135 pages villes** dans `municipales-2026/*/index.html` : chacune a son canonical, ses meta, son JSON-LD
- **853 pages candidats** dans `municipales-2026/*/candidats/*/index.html` : JSON-LD Person + Event
- **Cache busting** : `?v=DATA_VERSION` sur CSS/JS, mis à jour par `generateur_commun.py`
- **Jamais de CSP** sur ce projet (GTM injecte des scripts dynamiques)
- **Google Search Console** : vérifier que les changements ne créent pas de nouveaux problèmes d'indexation

## Insights vérifiés (sources : Google documentation, Reddit r/SEO, r/TechSEO — mars 2026)

### Core Web Vitals — Signal de départage confirmé
- CWV est un **tiebreaker** : à contenu égal, le site plus rapide gagne
- **INP (Interaction to Next Paint)** remplace FID depuis mars 2024 — seuil ≤ 200ms
- Techniques INP : `requestAnimationFrame`, `scheduler.yield()`, éviter les long tasks JS > 50ms
- **LCP** : preload l'image LCP, `fetchpriority="high"`, éviter lazy-load au-dessus du fold
- **CLS** : dimensions explicites sur images/iframes, `font-display: swap`, réserver l'espace des ads

### Schema.org / Données structurées — Bonnes pratiques confirmées
- **JSON-LD** est le format préféré par Google (pas Microdata, pas RDFa)
- Les données structurées sont l'**"API pour l'IA"** — utilisées par les moteurs IA (SearchGPT, Gemini, Perplexity)
- Types dépréciés à éviter : vérifier les annonces Google (juin 2025, jan 2026)
- **Toujours valider** sur https://validator.schema.org/ ET avec le Rich Results Test
- Chaque entité doit avoir un `@id` unique pour le knowledge graph
- Ne PAS imbriquer des types non-standard (ex: Event dans knowsAbout → non-standard)

### Sitemap — Ce que Google ignore vraiment
- **`priority` et `changefreq` sont IGNORÉS** par Google — ne pas perdre de temps dessus
- Seul `<lastmod>` est utile (et seulement si la date est fiable/exacte)
- Ne mettre QUE les URLs indexables (pas de noindex, pas de redirections, pas de 404)
- Taille max : 50 000 URLs ou 50 Mo non compressé
- Soumettre via Google Search Console ET dans `robots.txt`

### Canonical — Règles strictes
- **Self-referencing canonical sur CHAQUE page** (même la page d'accueil)
- Toujours en **URL absolue** (pas relative)
- canonical = og:url = URL dans le sitemap — les 3 DOIVENT correspondre
- Un canonical vers une autre page = "cette page est un doublon de X" → attention aux erreurs
- Si canonical pointe vers une page noindex → Google est confus → bug d'indexation

### Liens internes — Architecture plate confirmée
- **3 à 5 liens internes pertinents par page** (vérifier les pages orphelines)
- Architecture plate : toute page indexable accessible en **≤ 3 clics** depuis l'accueil
- Topic clusters : page pilier → pages satellites → maillage croisé
- Texte d'ancrage descriptif (jamais "cliquez ici", "en savoir plus")
- Les liens internes distribuent le PageRank — ne pas gaspiller sur des pages noindex

### Tueurs d'indexation — Erreurs critiques
- Canonical conflictuel (pointant vers mauvaise page) = désindexation silencieuse
- `noindex` accidentel (hérité d'un template, d'un meta robots, ou d'un x-robots-tag HTTP)
- Contenu JS-only : Googlebot crawle le JS **9x plus lentement** — servir le HTML critique côté serveur
- Chaînes de redirections (A→B→C) : Google suit max 5 sauts, perte de crawl budget
- Pages soft-404 (200 OK mais contenu vide/erreur) → gaspillent le crawl budget

### Mobile-First Indexing — Obligatoire
- Google utilise la version mobile pour l'indexation — **parité de contenu obligatoire**
- Mêmes données structurées sur mobile ET desktop
- Pas de contenu caché derrière des accordéons/tabs sur mobile (Google le crawle mais peut le dévaloriser)
- Viewport meta tag obligatoire : `<meta name="viewport" content="width=device-width, initial-scale=1">`

### Spécifique au projet pourquituvotes.fr
- 103 pages villes + 548 pages candidats = **maillage interne critique**
- Chaque page ville doit lier vers ses candidats ET vers les villes voisines/similaires
- Les pages candidats doivent avoir un lien retour vers la page ville
- Le fil d'Ariane (BreadcrumbList) assure la hiérarchie : Accueil → Municipales 2026 → Ville → Candidat
- `_redirects` Cloudflare : toujours 301 (permanent), jamais 302
- Pas de CSP (GTM injecte des scripts dynamiques) — vérifier avant tout changement d'headers

## Optimisation des titles/meta depuis les données GSC

Quand les données GSC révèlent des opportunités (voir skill `/gsc`), voici comment agir :

### Templates de titres — `generate_static_shells.py`

Les titles sont générés par `make_candidate_title()` (4 niveaux de fallback, max 60 chars).
Les meta descriptions par `make_candidate_desc()` (max 155 chars).

**Principes pour optimiser les templates** :
- Le mot-clé principal DOIT être en début de title (pas à la fin)
- Pattern performant : `{Nom} — Programme Municipales 2026 {Ville} | PQTV`
- La meta description doit contenir : nom, ville, nombre de propositions, et un call-to-action ("Comparez")
- Ajouter "municipales 2026" dans TOUS les titles candidats (les requêtes le contiennent presque toujours)
- Ajouter le nom de la ville dans TOUS les titles candidats
- Le nom de la liste politique est un signal de pertinence pour les requêtes partisanes

**Quand modifier le template vs. les données** :
- Template (`generate_static_shells.py`) : si le changement s'applique à TOUS les candidats/villes
- Données JSON : si c'est spécifique à un candidat (ex: alias, nom alternatif)

### Bloc SEO HTML (avant le footer)

Le générateur injecte des blocs `<h2>`, `<h3>` et du texte dans chaque shell.
Ces blocs sont le seul contenu textuel visible par Googlebot (le reste est chargé en JS).

**Enrichir ces blocs** :
- Ajouter le nom de la liste politique dans le H2 candidat
- Ajouter le nombre de propositions par top thème
- Ajouter des liens internes vers les candidats concurrents de la même ville
- Ajouter un lien vers la page enjeux correspondant au thème principal du candidat

### Après modification des templates

TOUJOURS :
1. Regénérer : `python scripts/generate_static_shells.py`
2. Spot-check 3-4 pages pour vérifier les titles/meta
3. Bumper DATA_VERSION
4. Déployer via `/deploy`

## Si un problème SEO est détecté

1. Signaler le problème AVANT de coder
2. Expliquer l'impact SEO (perte d'indexation, duplicate content, etc.)
3. Proposer la correction
4. Après correction, vérifier la cohérence canonical/sitemap/og:url
