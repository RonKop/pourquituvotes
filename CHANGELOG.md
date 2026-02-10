# Changelog — #POURQUITUVOTES

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
