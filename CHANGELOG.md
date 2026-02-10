# Changelog — #POURQUITUVOTES

## [2026-02-10] Audit technique + optimisations perf/SEO/A11y

### Performance (Core Web Vitals)
- Google Fonts chargées en non-bloquant (`preload` + `media="print"` trick)
- Phosphor Icons CSS chargé en async (non-bloquant)
- `defer` ajouté sur tous les scripts (`home.js`, `app.js`, `chart.js`)
- `min-height` sur grilles JS (elections, tendances) pour réduire le CLS
- Suppression du design panel de production (~140 lignes HTML en moins)

### SEO
- Title home optimisé : "Municipales 2026 — Comparez les programmes des candidats"
- `robots.txt` créé avec référence au sitemap
- `sitemap.xml` créé avec les 34 villes + home + présidentielle
- Canonical URL du comparateur utilise désormais `villeSelectionnee.id`
- `og:image:alt` ajouté sur home et présidentielle
- `favicon.svg` créé et référencé sur les 3 pages

### Accessibilité
- `<h1>` ajouté au comparateur (manquait — critique pour SEO et lecteurs d'écran)
- Skip link ajouté au comparateur + CSS dans `style.css`
- `<header class="hero">` remplacé par `<section>` (double header)
- Burger menu mobile ajouté au comparateur (nav masquée sur mobile)

### Mobile
- Nav desktop masquée sur mobile, remplacée par burger menu
- Header comparateur compact (1 ligne au lieu de 2)

### OG Images
- Dossier `/og/` créé (images placeholder à fournir)
- Références unifiées (`/og/home.png`, `/og/presidentielle-2027.png`)

---

## [2026-02-10] Restructuration URLs + SEO

### URLs "poupée russe" (Phase 1)
- `/` → Portail home (ex `home.html`)
- `/municipales/2026/?ville=paris` → Comparateur (ex `index.html`)
- `/presidentielle/2027/` → Inchangé, liens mis à jour vers chemins absolus
- Tous les liens internes (HTML + JS) convertis en chemins absolus
- `DATA_BASE_URL` passé de `data/` à `/data/` (app.js, home.js)

### Partage viral
- Support du paramètre `?theme=` comme alias de `?categorie=` dans l'URL
- Alias viraux : `ecologie` → environnement, `transport` → transports, `emploi` → economie
- `mettreAJourURL()` génère `?theme=` au lieu de `?categorie=`
- Rétrocompatibilité : `?categorie=` continue de fonctionner

### SEO
- Schema.org `FAQPage` généré automatiquement par ville (un Q&A par candidat × catégorie)
- `<meta name="last-modified">` injecté dynamiquement avec la date de dernière mise à jour de la ville
- Champ `derniereMaj` ajouté à chaque ville dans `villes.json`
- `generateur_commun.py` met à jour `derniereMaj` automatiquement à chaque génération

### Fix
- Suppression du contour orange (`focus-visible`) sur la barre de recherche home

---

## [2026-02-09] Migration JSON

### Architecture données
- Données extraites de `app.js` vers fichiers JSON séparés dans `data/`
- `data/villes.json` — index léger des 34 villes
- `data/elections/*.json` — un fichier par élection
- `DATA_VERSION` pour cache busting (incrémenté auto par `generateur_commun.py`)
