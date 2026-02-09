# Méthodologie de recherche des programmes candidats

> Guide interne pour collecter, vérifier et intégrer les propositions des candidats aux municipales 2026.

---

## 1. Identifier les candidats

**Recherche initiale :**
- `[ville] municipales 2026 candidats` sur Google
- Croiser avec la presse locale (France Bleu, France 3 régions, presse locale spécialisée)

**Pour chaque candidat, noter :**
- Nom complet
- Parti / coalition / étiquette
- Sortant ou non
- Nom de la liste

---

## 2. Trouver le site de campagne

**Requêtes à tester (dans l'ordre) :**
1. `[prénom nom] municipales 2026` (ex: "Thomas Cazenave municipales 2026")
2. `[prénom nom] programme 2026 [ville]`
3. `[prénom nom] site campagne`
4. `[nom de liste] 2026 [ville]`

**Endroits à vérifier :**
- Site de campagne dédié (ex: `bournazel.paris`, `fairegagnerbordeaux.fr`)
- Page dédiée sur le site du parti (ex: LFI, RN, Renaissance)
- Réseaux sociaux (X/Twitter, Facebook, Instagram) → souvent le lien vers le site y est
- Profil Google Knowledge Panel du candidat

**Résultat possible :**
- Site dédié trouvé → noter l'URL
- Pas de site → noter "Aucun site de campagne identifié"

---

## 3. Chercher le programme

### 3a. Programme complet (PDF ou page web structurée)

**Sur le site du candidat, chercher :**
- Onglet "Programme", "Nos propositions", "Notre projet", "Mes mesures"
- Bouton de téléchargement PDF
- Page listant les mesures de façon exhaustive et structurée

**ATTENTION — Liens et redirections :**
- Certains candidats ont un **site de campagne** (ex: `sarahpourparis.fr`) avec un lien "Programme" qui **redirige vers un autre site** (ex: `unevilleheureuse.fr`) où se trouve le programme complet en PDF.
- Il faut **toujours cliquer sur le lien "Programme"** du site principal et suivre la redirection.
- Ne JAMAIS conclure qu'un candidat n'a pas de programme complet sans avoir vérifié tous les liens du site.
- **Erreur type à éviter** : se contenter des mesures trouvées dans la presse alors qu'un PDF complet existe sur un site secondaire lié au site principal.

**Si PDF trouvé :**
1. Télécharger dans `data/programmes/`
2. Nommage : `Programme2026_PrenomNom.pdf`
3. Extraire le texte avec PyMuPDF (`python -u -X utf8`)
4. Marquer `programmeComplet: true` dans app.js

**Si programme web complet :**
1. Utiliser WebFetch pour extraire le contenu
2. Vérifier que c'est bien un programme structuré (pas juste un slogan)
3. Marquer `programmeComplet: true` + `programmeUrl` dans app.js

### 3b. Propositions partielles (pas de programme complet)

**Sources à explorer, dans l'ordre de fiabilité :**

| Priorité | Source | Fiabilité | Comment chercher |
|----------|--------|-----------|-----------------|
| 1 | Site de campagne (même sans programme complet) | Haute | Pages "actualités", articles, communiqués |
| 2 | Tracts thématiques (PDF) | Haute | Souvent dans une section "kit militant" ou "documents" |
| 3 | Interviews presse locale | Moyenne-haute | `[nom] interview programme [ville] 2026` |
| 4 | Articles de presse spécialisée | Moyenne-haute | Presse locale : Lyon Capitale, Rue89 Bordeaux, Marsactu, Made in Marseille, 7 Jours à Clermont... |
| 5 | Déclarations officielles / communiqués | Moyenne | Site du parti, réseaux sociaux |
| 6 | Débats / émissions TV-radio | Moyenne | YouTube, sites des chaînes locales |
| 7 | Pages Wikipedia / agrégateurs | Faible | Uniquement pour recouper, jamais comme source unique |

**Requêtes utiles :**
- `[nom] propositions [ville] 2026`
- `[nom] mesures municipales 2026`
- `[nom] programme [thème] 2026` (ex: "Dati sécurité Paris 2026")
- `site:[presse-locale.fr] [nom] programme` (ex: `site:lyoncapitale.fr Belouassa programme`)

---

## 4. Extraire et structurer les mesures

### Étape 1 — Inventaire exhaustif (OBLIGATOIRE pour les PDF)

**Avant de mapper quoi que ce soit**, faire un inventaire complet :
1. Extraire le texte du PDF avec PyMuPDF
2. Compter TOUTES les "Mesure n°X" / "Mesures concrètes" du document
3. Créer une checklist numérotée : `[ ] Mesure 1 : [titre]` pour chacune
4. Cocher chaque mesure au fur et à mesure de l'intégration dans app.js
5. À la fin, vérifier qu'il reste 0 mesure non cochée

**Pourquoi ?** Erreur Knafo : 51 mesures dans le PDF, seulement 32 intégrées à la première passe parce que pas de checklist systématique. 19 mesures oubliées.

### Étape 2 — Filtrer

**Ce qu'on garde :**
- Mesures concrètes et vérifiables (chiffres, engagements précis)
  - "5 000 policiers municipaux" ✅
  - "Gratuité des transports pour les moins de 26 ans" ✅
  - "Prêt à taux zéro pour les familles" ✅

**Ce qu'on ne garde PAS :**
- Slogans vagues sans engagement concret
  - "Rendre Paris aux Parisiens" ❌
  - "Une ville plus verte" ❌ (sauf si accompagné de mesures précises)
- Critiques des adversaires sans proposition alternative
- Informations purement biographiques

### Étape 3 — Mapper à la grille universelle

**Grille universelle : 12 catégories, 44 sous-thèmes communs** (identiques pour toutes les villes, dans cet ordre fixe) :

| # | ID | Nom | Sous-thèmes communs |
|---|-----|-----|---------------------|
| 1 | `securite` | Sécurité & Prévention | police-municipale, videoprotection, prevention-mediation, violences-femmes |
| 2 | `transports` | Transports & Mobilité | transports-en-commun, velo-mobilites-douces, pietons-circulation, stationnement, tarifs-gratuite |
| 3 | `logement` | Logement | logement-social, logements-vacants, encadrement-loyers, acces-logement |
| 4 | `education` | Éducation & Jeunesse | petite-enfance, ecoles-renovation, cantines-fournitures, periscolaire-loisirs, jeunesse |
| 5 | `environnement` | Environnement & Transition écologique | espaces-verts, proprete-dechets, climat-adaptation, renovation-energetique, alimentation-durable |
| 6 | `sante` | Santé & Accès aux soins | centres-sante, prevention-sante, seniors |
| 7 | `democratie` | Démocratie & Vie citoyenne | budget-participatif, transparence, vie-associative, services-publics |
| 8 | `economie` | Économie & Emploi | commerce-local, emploi-insertion, attractivite |
| 9 | `culture` | Culture & Patrimoine | equipements-culturels, evenements-creation |
| 10 | `sport` | Sport & Loisirs | equipements-sportifs, sport-pour-tous |
| 11 | `urbanisme` | Urbanisme & Cadre de vie | amenagement-urbain, accessibilite, quartiers-prioritaires |
| 12 | `solidarite` | Solidarité & Égalité | aide-sociale, egalite-discriminations, pouvoir-achat |

**Règle : chaque proposition va dans UN sous-thème commun existant.**

**Si une mesure ne rentre dans aucun sous-thème commun :**
→ Créer un sous-thème spécifique à la ville, APRÈS les communs dans la catégorie (ex: `baignades-seine` pour Paris dans `environnement`, `tunnel-circulation` pour Lyon dans `transports`)
→ Mettre `null` pour les autres candidats

### Format de la source

Chaque proposition doit avoir :
```javascript
{
  texte: "La mesure concrète en une phrase",
  source: "Nom de la source",
  sourceUrl: "https://..."
}
```

**Convention de nommage des sources :**
- `"Programme officiel 2026"` → programme complet (PDF ou site)
- `"Tract [Thème] 2026"` → tract thématique PDF
- `"Site de campagne 2026"` → mesure trouvée sur le site sans PDF complet
- `"[Nom du média], [mois] 2026"` → article de presse (ex: "Lyon Capitale, février 2026")
- `"Interview [média], [mois] 2026"` → interview spécifique

---

## 5. Classification du candidat

| Critère | `programmeComplet: true` | `programmeComplet: false` |
|---------|--------------------------|---------------------------|
| Programme PDF téléchargeable avec mesures numérotées | ✅ | |
| Page web avec liste exhaustive de mesures concrètes | ✅ | |
| Quelques mesures sur le site, pas de programme complet | | ✅ |
| "Pacte" / "Priorités" / grandes orientations sans mesures détaillées | | ✅ |
| Mesures connues uniquement via presse/interviews | | ✅ |
| Tracts thématiques mais pas de programme global | | ✅ |
| Aucune mesure trouvée | | ✅ (laisser `null` partout) |

**PIÈGE COURANT — "Pacte" ≠ Programme :**
Un site qui présente 5 grandes priorités thématiques (ex: "Sécurité", "Solidarité", "Culture") avec des textes d'intention mais sans liste de mesures concrètes numérotées n'est PAS un programme complet. C'est le cas du "Pacte Lyonnais" d'Aulas : des grandes orientations + quelques mesures phares, mais pas de programme structuré → `programmeComplet: false`.

**Critère simple :** Si tu ne peux pas extraire au moins 15-20 mesures concrètes et chiffrées du document/site, c'est probablement `false`.

**Important :** Un candidat peut passer de `false` à `true` quand il publie son programme complet. Revérifier régulièrement (surtout fin février / début mars).

---

## 6. Mettre à jour les fichiers

### Pour chaque candidat traité :

1. **app.js** — Ajouter/modifier les propositions dans les sous-thèmes
2. **PROGRAMMES_A_TELECHARGER.html** — Mettre à jour le statut (⏳ → 🌐 → ✅)
3. **PROGRAMMES_A_TELECHARGER.md** — Idem en markdown

### Vérifications après modification :
1. **Lancer `python scripts/valider_donnees.py`** (obligatoire après chaque modif de app.js)
   - Vérifie l'équilibre syntaxique, les candidats fantômes, les doublons, le comptage
2. Tester dans le navigateur (ouvrir index.html, sélectionner la ville)
3. Vérifier le radar, les filtres, la recherche

### Erreurs passées à ne pas reproduire :
- **Agents parallèles en ÉCRITURE sur app.js** : ne JAMAIS lancer plusieurs agents qui ÉCRIVENT dans app.js en même temps → bug propreté Marseille dupliquée dans 4 villes. Les agents en lecture seule (audit, comptage) peuvent tourner en parallèle sans risque
- **programmeComplet: true trop hâtif** : ne mettre `true` que si le programme est réellement structuré avec 15+ mesures concrètes (erreur Aulas : "Pacte" avec 7 mesures marqué complet)
- **Extraction PDF incomplète** : toujours faire l'inventaire exhaustif AVANT de mapper (voir §4 Étape 1). Erreur Knafo : 51 mesures dans le PDF, seulement 32 intégrées à cause d'un inventaire bâclé
- **Ignorer des mesures** : si une mesure ne rentre dans aucun sous-thème → créer un nouveau sous-thème, ne jamais ignorer
- **Doublons de texte** : ne JAMAIS copier le même texte dans 2 sous-thèmes différents. Si une mesure couvre 2 thèmes, choisir le plus pertinent et ne la mettre qu'une fois
- **Texte dans le mauvais sous-thème** : toujours relire le mapping final pour vérifier que chaque texte correspond bien au nom du sous-thème (erreur Knafo : texte "patrimoine" dans sous-thème "sport", texte "sport" dans "ville-refuge")

---

## 7. Calendrier de revérification

| Date | Action |
|------|--------|
| **Maintenant → 26 fév** | Chercher les programmes manquants, revérifier les sites régulièrement |
| **26 février 2026** | Date limite dépôt des candidatures → nouvelles listes possibles |
| **Début mars** | Professions de foi sur programme-candidats.interieur.gouv.fr |
| **~10 mars** | Dernier check complet avant le 1er tour |
| **15 mars** | 1er tour |
| **16-21 mars** | Vérifier les alliances / fusions de listes pour le 2e tour |
| **22 mars** | 2e tour |

---

## 8. Presse locale par ville (signets)

| Ville | Médias de référence |
|-------|-------------------|
| **Paris** | Le Journal du Grand Paris, France Bleu Paris, 94.citoyens.com |
| **Lyon** | Lyon Capitale, Lyon Mag, Tribune de Lyon, Lyon Demain, Figures Publiques |
| **Marseille** | Marsactu, Made in Marseille, Maritima, Gomet |
| **Bordeaux** | Rue89 Bordeaux, France Bleu Gironde |
| **Clermont-Ferrand** | 7 Jours à Clermont, France Bleu Auvergne, RCF |
| **Toulouse** | Mediacités Toulouse, Actu Toulouse, France Bleu Occitanie |
| **Nice** | Nice-Matin, France Bleu Azur |
| **Nantes** | Mediacités Nantes, Presse Océan, France Bleu Loire Océan |
| **Strasbourg** | Rue89 Strasbourg, DNA (Dernières Nouvelles d'Alsace) |
| **Lille** | Mediacités Lille, La Voix du Nord, France Bleu Nord |

---

## Résumé du workflow

```
1. Recherche candidat → Google "[nom] municipales 2026"
2. Site trouvé ?
   ├─ OUI → Programme/PDF dispo ?
   │        ├─ OUI → Télécharger + extraire → programmeComplet: true
   │        └─ NON → Scraper les mesures du site → programmeComplet: false
   └─ NON → Chercher dans la presse locale → programmeComplet: false
3. Extraire les mesures concrètes (chiffres, engagements)
4. Mapper aux catégories/sous-thèmes existants
5. Intégrer dans app.js + mettre à jour page téléchargements
6. Vérifier syntaxe + tester dans le navigateur
```
