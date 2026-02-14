# Documentation technique — Page Comparateur #POURQUITUVOTES

> Ce document décrit exhaustivement les fonctionnalités, données et composants de la page comparateur des municipales 2026.
> **Objectif** : permettre à un développeur ou une IA d'identifier des pistes d'optimisation (UX, performance, SEO, accessibilité, conversion).

---

## 1. Architecture technique

| Élément | Détail |
|---------|--------|
| **Stack** | HTML statique + CSS + JavaScript vanilla (ES5, pas de framework) |
| **Graphiques** | Chart.js (radar chart uniquement) |
| **Icônes** | Phosphor Icons (CDN, style regular) |
| **Polices** | Montserrat (titres, 900 italic) + DM Sans (corps, 400-700) — Google Fonts |
| **Données** | JSON externe dans `data/` — pas d'API, fichiers statiques |
| **Hébergement** | Cloudflare Pages (statique, CDN, gratuit) |
| **Analytics** | Google Tag Manager (GTM-T4CCTF6V) + GA4 via dataLayer |
| **Consentement** | CMP maison CNIL-compliant (Google Consent Mode V2) |

### Chargement des données
- `data/villes.json` (~38 KB) : index de toutes les villes avec stats résumées et liste des candidats (nom + liste)
- `data/elections/{ville}-2026.json` (10-50 KB chacun) : données complètes d'une élection (candidats, catégories, sous-thèmes, propositions)
- **Prefetch** : un script inline dans le `<head>` lance `fetch(villes.json)` immédiatement + `fetch(election.json)` si `?ville=` est présent dans l'URL (élimine la cascade séquentielle)
- **Cache** : les URLs ont un query param `?v=DATA_VERSION` (ex: `2026021002`) pour le cache busting
- **Cache mémoire** : `ELECTIONS_CACHE` en JS évite de re-fetch une ville déjà chargée

### Performance actuelle
- CSS critique inline dans le `<head>` pour un first paint instantané
- CSS complet chargé de manière non-bloquante (`media="print" onload="this.media='all'"`)
- Polices Google Fonts en mode non-bloquant (même technique)
- Loader overlay visible pendant le chargement
- Pas de minification JS (fichier `app.js` ~3900 lignes, ~125 KB)
- Pas de code splitting (tout le JS chargé en un seul fichier)
- Pas de lazy loading d'images (il n'y a pas d'images dans le comparateur)
- Pas de Service Worker ni de mode hors-ligne

---

## 2. Structure de la page (sections dans l'ordre d'affichage)

### 2.1 Header sticky
- Logo `#POURQUITUVOTES?` (blanc + rouge)
- Navigation desktop : À propos, Méthodologie, FAQ, Contact
- Burger menu mobile (overlay full-screen avec recherche de ville intégrée)
- **Compte à rebours** en temps réel : jours/heures/minutes/secondes avant le scrutin (15 mars 2026)
- Topbar mobile séparée pour le compte à rebours

### 2.2 Hero section (fond bleu `#002395`)
- **Titre dynamique** : "Municipales [Badge Ville] 2026"
- **Sous-titre** : "Le comparateur de programmes indépendant"
- **Barre de recherche universelle** : cherche simultanément par ville (nom ou code postal) et par nom de candidat
  - Autocomplétion avec suggestions (villes + candidats mélangés)
  - Navigation au clavier (flèches + Entrée)
  - Recherche de candidat : affiche le nom, la ville et le parti
  - Bouton "Rechercher" qui sélectionne la première suggestion
- **CTA Quiz** (visible après sélection d'une ville) : 2 boutons "Test Express (2 min)" et "Analyse Complète (5 min)" → redirigent vers le simulateur
- **Stats cards** (visibles après sélection) : nombre de candidats, propositions et thématiques
- **Fil d'Ariane** : Accueil > Municipales 2026 > [Ville]
- **Toolbar de partage** : boutons Copier lien, Facebook, X/Twitter, LinkedIn, WhatsApp
- Cercles décoratifs en arrière-plan (purement visuels)

### 2.3 Filtres candidats (chips)
- Chips avec nom du candidat, coche, couleur du parti politique
- Boutons "Tous" / "Aucun" (au moins 1 candidat doit rester sélectionné)
- **Couleurs automatiques** basées sur l'étiquette politique (LFI violet, PS rose, EELV vert, Renaissance jaune, LR bleu, RN bleu foncé, Reconquête orange, etc.)
- **Bottom sheet mobile** : version adaptée des filtres pour écrans tactiles (overlay + liste + bouton "Appliquer")

### 2.4 Répartition thématique (masquée par défaut)
Section cachée mais fonctionnelle, avec 3 modes de visualisation :
- **Barres groupées** : barres horizontales par catégorie, 1 barre par candidat, couleurs des partis, légende
- **Heatmap** : matrice candidat × catégorie avec intensité de couleur
- **Cartes individuelles** : une carte par candidat avec ses stats par catégorie

### 2.5 Radar chart — "Scanner de densité"
- **Chart.js radar** (type `radar`) avec grille circulaire
- 12 axes = les 12 catégories thématiques (labels courts : Sécurité, Transports, etc.)
- Échelle 0-10 (nombre de propositions par catégorie)
- **Zone grise** = moyenne de tous les candidats (dataset en arrière-plan, bordure en pointillés)
- **Sélection de candidats** : panel de chips à droite du radar, cocher/décocher pour superposer les tracés
- Couleurs = couleurs des partis politiques
- Tooltip : "Candidat — X propositions en Thème"
- **Encart méthodologique** sous le radar : "Équité de comparaison" — explique si les programmes sont complets ou partiels, avec badges "programme officiel" / "programme à venir" par candidat
- **Guide de lecture** : 3 blocs explicatifs (La Forme, La Couverture, Les Zones non couvertes)
- Masqué si < 10 propositions au total (petites villes sans données)

### 2.6 Treemap — "ADN Politique"
- Visualisation bento (blocs de tailles proportionnelles) montrant la répartition % des propositions par catégorie pour un candidat
- **Chips candidats** : sélectionner quel candidat afficher
- **Mode duel** : bouton "Comparer l'ADN" pour afficher 2 treemaps côte à côte
  - Sélecteur d'adversaire (dropdown)
  - Chaque treemap est cliquable → scroll vers la catégorie correspondante
- Blocs limités à 5 + "Autres" pour la lisibilité
- Chaque bloc affiche : icône Phosphor, label catégorie, nombre de propositions, pourcentage
- Nuances du parti (opacité décroissante du bloc principal aux secondaires)

### 2.7 Alerte programmes (lead capture)
- Bandeau compact : "X programmes sur Y officiels"
- Input email + bouton "M'alerter"
- Message de confirmation après soumission
- Tracking analytics : événement `lead_capture` avec email hashé SHA-256

### 2.8 Filtres catégories (navigation pills)
- Boutons de filtre par catégorie : "Toutes" + 1 bouton par catégorie thématique
- Filtre la grille de comparaison en dessous
- Avec icône et compteur de propositions

### 2.9 Grille de comparaison détaillée (section principale)
C'est le coeur du comparateur. Format **tableau matriciel** par catégorie :

- **Accordéon par catégorie** : chaque catégorie est une section repliable (la première est ouverte par défaut)
- **En-tête de catégorie** : icône + nom + mini-barres de répartition (barres horizontales montrant le nombre de propositions par candidat, avec couleurs des partis)
- **Tableau matriciel** à l'intérieur de chaque catégorie :
  - Colonnes = candidats (avec en-tête : nom, parti, badge "Officiel"/"À venir", barre de couverture X/Y thèmes abordés)
  - Lignes = sous-thèmes (ex: "Police municipale", "Vidéoprotection", etc.)
  - Cellules = texte de la proposition + source + lien "Voir le document"
  - Cases grises si le candidat n'a pas de proposition sur ce sous-thème
  - **Colonnes masquables** : bouton +/- pour replier/déplier la colonne d'un candidat (utile avec 14 candidats à Strasbourg)
  - Candidats sans aucune proposition = colonne pré-repliée
  - **Mode mobile** : accordéon par sous-thème (chaque sous-thème se déplie pour montrer les propositions des candidats en vertical)
- **Liens vers sources** : chaque proposition affiche sa source (ex: "Programme officiel 2026") et un lien cliquable vers le document original
- **Lien profil candidat** : le nom du candidat est cliquable → page candidat individuelle
- **Guide de lecture** : bannière explicative affichée la première fois, masquable (stockée dans localStorage)
- **Compteur** : "X candidats affichés sur Y" avec bouton "Afficher tous"

### 2.10 Progress dots (navigation latérale)
- Points de navigation fixés sur le côté droit de l'écran (desktop uniquement)
- Un point par catégorie visible
- Scroll spy : le point actif change en temps réel selon la position de scroll
- Clic sur un point → scroll smooth vers la catégorie
- Compteur affichant "3/12" (nombre de catégories avec propositions / total)

### 2.11 État vide
- Affiché quand aucune ville n'est sélectionnée
- Message + dates clés des municipales 2026 (inscription, dépôt candidatures, tours)

### 2.12 Message "aucun candidat"
- Affiché si la ville existe mais n'a aucun candidat déclaré
- Explique la date limite de dépôt (26 février 2026)

### 2.13 Footer riche
- 4 colonnes : Brand + liens sociaux, Municipales 2026 (7 grandes villes), Autres élections (Présidentielle 2027 "SOON"), Le projet
- Liens légaux : Mentions légales, Confidentialité, Gestion des cookies

---

## 3. Structure des données

### 3.1 Index des villes (`villes.json`)
```json
{
  "id": "paris",
  "nom": "Paris",
  "codePostal": "75000",
  "departement": "75",
  "elections": ["paris-2026"],
  "stats": { "candidats": 6, "propositions": 127, "themes": 12, "complets": 2 },
  "candidats": [
    { "id": "gregoire", "nom": "Emmanuel Grégoire", "liste": "Gauche unie (PS-Écologistes)" },
    ...
  ]
}
```
- 34 villes indexées
- Les stats sont pré-calculées pour éviter de charger chaque JSON
- Les candidats sont dupliqués (résumé dans villes.json + détails dans election.json) pour la recherche universelle sans charger tous les JSON

### 3.2 Données d'une élection (`elections/{ville}-2026.json`)
```json
{
  "ville": "Paris",
  "annee": 2026,
  "type": "Élections municipales",
  "dateVote": "2026-03-15T08:00:00",
  "candidats": [
    {
      "id": "gregoire",
      "nom": "Emmanuel Grégoire",
      "liste": "Gauche unie (PS-Écologistes)",
      "programmeUrl": "https://...",
      "programmeComplet": true,
      "programmePdfPath": "paris-gregoire.pdf"
    }
  ],
  "categories": [
    {
      "id": "securite",
      "nom": "Sécurité & Prévention",
      "sousThemes": [
        {
          "id": "police-municipale",
          "nom": "Police municipale",
          "propositions": {
            "gregoire": { "texte": "...", "source": "Programme officiel 2026", "sourceUrl": "https://..." },
            "dati": { "texte": "...", "source": "Tract Sécurité 2026", "sourceUrl": "https://..." },
            "chikirou": null
          }
        }
      ]
    }
  ]
}
```

### 3.3 Structure thématique universelle
**12 catégories, 44 sous-thèmes communs** — identiques pour toutes les villes :

| Catégorie | Sous-thèmes |
|-----------|-------------|
| Sécurité | police-municipale, videoprotection, prevention-mediation, violences-femmes |
| Transports | transports-en-commun, velo-mobilites-douces, pietons-circulation, stationnement, tarifs-gratuite |
| Logement | logement-social, logements-vacants, encadrement-loyers, acces-logement |
| Éducation | petite-enfance, ecoles-renovation, cantines-fournitures, periscolaire-loisirs, jeunesse |
| Environnement | espaces-verts, proprete-dechets, climat-adaptation, renovation-energetique, alimentation-durable |
| Santé | centres-sante, prevention-sante, seniors |
| Démocratie | budget-participatif, transparence, vie-associative, services-publics |
| Économie | commerce-local, emploi-insertion, attractivite |
| Culture | equipements-culturels, evenements-creation |
| Sport | equipements-sportifs, sport-pour-tous |
| Urbanisme | amenagement-urbain, accessibilite, quartiers-prioritaires |
| Solidarité | aide-sociale, egalite-discriminations, pouvoir-achat |

+ Des sous-thèmes spécifiques par ville peuvent être ajoutés après les communs (ex: baignades-seine pour Paris, tunnel-circulation pour Toulouse).

---

## 4. Fonctionnalités interactives détaillées

### 4.1 Recherche universelle
- **Input unique** qui cherche dans 2 dimensions :
  - Villes : par nom (`"Par"` → Paris, Perpignan...) ou code postal (`"75"` → Paris)
  - Candidats : par nom (`"Dati"` → Rachida Dati, Paris, LR)
- Les résultats villes et candidats sont mixés dans le même dropdown
- Sélectionner un candidat → charge la ville correspondante et pré-filtre sur ce candidat

### 4.2 URL et deep linking
- L'URL reflète l'état : `?ville=paris` charge directement Paris
- Hash `#securite` → scroll vers la catégorie Sécurité
- Au chargement, la page auto-scroll vers le contenu si `?ville=` est présent
- Mise à jour de l'URL sans rechargement (`history.pushState`)

### 4.3 SEO dynamique
- `<title>` mis à jour avec le nom de la ville
- `<meta description>` mis à jour
- **Schema.org FAQ** : script `application/ld+json` généré dynamiquement avec une entrée Q&A par candidat × catégorie ("Que propose X sur le thème Y à Z ?")
- Schema.org WebApplication sur la page

### 4.4 Partage social
- **Copier le lien** (clipboard API)
- **Facebook, Twitter/X, LinkedIn, WhatsApp** : ouverture d'un popup avec URL pré-remplie
- Open Graph tags statiques dans le `<head>`
- Analytics : événement `social_share` avec réseau + ville

### 4.5 Dark mode
- Toggle de thème (stocké dans localStorage)
- Couleurs radar/tooltips adaptées au thème

### 4.6 Modales
- **À propos** : présentation du projet
- **FAQ** : questions fréquentes
- **Méthodologie** : sources, collecte, neutralité
- **Signaler une erreur** : formulaire complet (ville, candidat, catégorie, description, source correcte, email) → génère un mailto

### 4.7 Alerte email
- Formulaire email dans la section alertes
- Hash SHA-256 de l'email avant envoi analytics
- Événement `lead_capture`

---

## 5. Analytics (dataLayer / GTM)

22 événements trackés via `window.PQTV_Analytics` :

| Événement | Quand | Paramètres clés |
|-----------|-------|-----------------|
| `page_view_custom` | Chargement | page_path, referrer |
| `scroll_depth` | Scroll 25/50/75/100% | depth_percent, time_on_page |
| `city_selected` | Sélection ville | city_name, election_id, candidate_count |
| `search_city` | Recherche ville | search_term, results_count |
| `candidate_filter` | Filtrage candidat | action (add/remove/all/none), candidate_name, active_count |
| `category_view` | Clic catégorie | category_name |
| `source_verification` | Clic "Voir le document" | candidate_name, source_type, url_domain |
| `view_mode_change` | Changement mode répartition | view_type |
| `outbound_click` | Lien externe | url, link_text |
| `social_share` | Partage réseau | network, city_name |
| `quiz_start` | Début quiz | mode, city_name |
| `quiz_step_complete` | Question quiz | step, category |
| `quiz_result` | Résultat quiz | top_candidate, match_percent |
| `quiz_early_exit` | Sortie anticipée quiz | questions_answered |
| `quiz_result_share` | Partage résultat quiz | network |
| `lead_capture` | Email alerte | email_hash (SHA-256) |
| `form_submit_report` | Signalement erreur | city, candidate |
| `faq_question_open` | Ouverture FAQ | question |
| `modal_open` | Ouverture modale | modal_name |
| `consent_update` | Choix cookies | analytics, marketing |
| `quiz_priorities_set` | Priorités quiz expert | priorities (array) |

---

## 6. Accessibilité actuelle

- Skip link "Aller au contenu principal"
- `aria-label` sur boutons d'icônes (burger, fermer, réseaux sociaux)
- `aria-expanded` sur le burger menu
- `role="contentinfo"` sur le footer
- Navigation au clavier dans les suggestions (flèches + Entrée + Escape)
- **Manques potentiels** : pas de `aria-live` pour les mises à jour dynamiques, pas de focus trap dans les modales, contrastes non audités formellement

---

## 7. Tailles des données (ordre de grandeur)

| Fichier | Taille |
|---------|--------|
| `app.js` | ~125 KB (non minifié) |
| `style.css` | ~60 KB (non minifié) |
| `analytics.js` | ~8 KB |
| `consent.js` | ~6 KB |
| `villes.json` | ~38 KB |
| Election JSON (grande ville) | ~30-50 KB |
| Election JSON (petite ville) | ~5-15 KB |
| Total first load (sans ville) | ~250 KB (JS+CSS+JSON+fonts) |
| Total avec une ville | +30-50 KB |

---

## 8. Pages annexes

| Page | URL | Contenu |
|------|-----|---------|
| Home | `/index.html` | Landing page avec aperçu, stats, CTA |
| Comparateur | `/municipales/2026/index.html` | **Cette page** |
| Simulateur/Quiz | `/municipales/2026/simulateur.html` | Quiz de convictions (en développement) |
| Profil candidat | `/municipales/2026/candidat.html?ville=X&candidat=Y` | Page individuelle candidat |
| Méthodologie | `/methodologie.html` | Page dédiée |
| FAQ | `/faq.html` | Page dédiée |
| À propos | `/a-propos.html` | Page dédiée |
| Mentions légales | `/mentions-legales.html` | Obligations légales |
| Confidentialité | `/confidentialite.html` | Politique de données |
| Présidentielle 2027 | `/presidentielle/2027/` | Page "Coming soon" |

---

## 9. Points de friction UX connus

1. **34 villes / 97 candidats seulement** — la plupart des villes de France ne sont pas encore couvertes
2. **Programmes partiels** — beaucoup de candidats n'ont que quelques propositions issues de la presse, pas de programme officiel
3. **Tableau matriciel large** — avec 14 candidats (Strasbourg), le tableau déborde et nécessite le masquage de colonnes
4. **Pas de système de comparaison directe 1v1** dans la grille principale (uniquement dans le treemap)
5. **Pas de recherche dans les propositions** (le champ recherche filtre les villes/candidats, pas le contenu des textes)
6. **Pas de favoris/bookmark** de candidats ou de sélection
7. **Loader global** même pour un changement de ville (pas de transition fluide)

---

## 10. Suggestions de pistes d'optimisation

### Performance
- Minification JS/CSS (webpack, esbuild, ou simple terser)
- Code splitting : séparer le code du radar Chart.js (lazy load)
- Service Worker pour le mode hors-ligne et le cache des JSON
- Preload des polices les plus critiques

### SEO
- Canonical URL dynamique avec `?ville=`
- Sitemap XML avec toutes les villes
- Pages statiques pré-rendues par ville pour le SSR-like
- Breadcrumb Schema.org (en plus du FAQ Schema)

### UX
- Recherche full-text dans les propositions
- Comparaison directe 2 candidats dans la grille
- Sauvegarde de la sélection (localStorage ou URL)
- Skeleton loading au lieu du loader overlay
- Animations de transition entre les sections
- Infinite scroll ou pagination pour les grandes grilles
- Mode "résumé" avec les propositions clés uniquement

### Accessibilité
- Audit WCAG 2.1 AA complet
- Focus trap dans les modales
- `aria-live="polite"` pour les mises à jour dynamiques
- Test lecteur d'écran (NVDA/VoiceOver)

### Conversion
- Push notifications (Web Push API) pour les mises à jour de programmes
- Partage avec résultat personnalisé (Open Graph dynamique via Cloudflare Workers)
- Widget embarquable pour les médias locaux
- A/B test sur le CTA quiz
