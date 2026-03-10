# Méthodologie d'extraction des programmes candidats

Guide interne pour l'extraction fiable et la validation des propositions intégrées sur pourquituvotes.fr.
Companion de `METHODOLOGIE_RECHERCHE.md` (qui couvre la collecte/recherche).

---

## 1. Objectif et contexte

Ce document formalise les leçons apprises après les spot-checks de février 2026 sur les 69 candidats `programmeComplet: true`. Les spot-checks ont révélé **10 problèmes systémiques** : bilan mélangé aux propositions, WebFetch qui paraphrase/invente, extractions partielles, misclassifications, blocs monolithiques, etc.

**But :** fournir un cadre reproductible pour ré-extraire les programmes et en créer de nouveaux, avec des garde-fous automatisés.

---

## 2. Les 10 problèmes rencontrés et solutions

### 2.1 Sites SPA (DudaMobile, Elementor, React)

**Problème :** WebFetch retourne du contenu vide ou partiel sur les sites rendus côté client (JavaScript).

**Exemple projet :** `altrad2026.fr` (DudaMobile), `mariani-2026.fr` — WebFetch ne voyait qu'une coquille HTML vide.

**Solution :** Fallback vers le PDF hébergé sur le CDN DudaMobile (`irp.cdn-website.com/{siteAlias}/files/uploaded/`). Pour WordPress + Elementor, tenter l'API REST `/wp-json/wp/v2/pages/` mais attention : elle ne résout pas les shortcodes des page builders.

**Prévention :** Toujours vérifier le rendu dans un navigateur avant d'utiliser WebFetch. Si le site est dynamique → chercher le PDF d'abord.

### 2.2 Bilan mélangé aux propositions

**Problème :** Les candidats sortants présentent leurs réalisations (« depuis 2020, nous avons... ») au milieu de leurs engagements futurs.

**Exemple projet :** Moudenc (Toulouse) — « Augmentation des effectifs de 165 à 390 agents depuis 2014 » était intégré comme proposition alors que c'est un bilan.

**Solution :** Scanner les marqueurs temporels avec 10 regex (cf. `auditer_completude.py`) :
- `depuis 20\d{2}`, `déjà en place`, `record de`, `passage de .+ à .+`
- `fin 20\d{2}`, `actuellement`, `contre \d+ actuellement`
- `triplement|doublement`, `\d+ déjà installée?s`, `augmentation.*depuis`

Puis revue manuelle : reformuler en proposition (« Porter les effectifs à X ») ou supprimer.

**Prévention :** Exécuter `auditer_completude.py --candidat X` après chaque extraction pour détecter les marqueurs.

### 2.3 WebFetch paraphrase ou invente

**Problème :** WebFetch résume le contenu des pages au lieu de le retranscrire fidèlement, et peut ajouter des interprétations.

**Exemple projet :** Des mesures de Grégoire (Paris) étaient reformulées avec des nuances absentes du programme original.

**Solution :** JAMAIS faire confiance à WebFetch pour le texte exact des mesures. Toujours croiser avec le PDF ou la source originale.

**Prévention :** Utiliser PyMuPDF pour extraire le texte brut du PDF. Si pas de PDF, demander un copier-coller au lieu de paraphraser.

### 2.4 Extraction partielle

**Problème :** Le programme source contient N mesures mais on n'en extrait que N/2.

**Exemple projet :** Grégoire (Paris) — 90 mesures extraites initialement alors que le programme en contient 165.

**Solution :** **Compter les mesures dans la source AVANT de commencer l'extraction.** Comparer après.

**Prévention :** Checklist pré-extraction obligatoire (§5). Le template `template_reextraire.py` inclut un commentaire `# Source: X mesures, Extraites: Y mesures`.

### 2.5 Blocs monolithiques

**Problème :** Un sous-thème contient une seule « mesure » de 500+ caractères qui est en réalité 4-5 mesures concaténées.

**Exemple projet :** Plusieurs candidats post-batch avaient des mesures de 300-600 chars car WebFetch avait groupé des paragraphes.

**Solution :** `resplit_blocs.py` redécoupe automatiquement les blocs > 200 chars via split sur `". "` + majuscule ou `"; "` + minuscule.

**Prévention :** Seuil de 200 chars détecté par `auditer_completude.py`. Lors de l'écriture manuelle, une mesure = une phrase/action.

### 2.6 Misclassification

**Problème :** Une mesure est placée dans le mauvais sous-thème.

**Exemple projet :** Doucet (Lyon) — « Zoo Tête d'Or animaux en danger » dans `climat-adaptation`, « Charte droits Rhône et Saône » dans `transparence`.

**Solution :** Map de mots-clés par sous-thème (44 entrées) dans `auditer_completude.py`. Flag si 0 mot-clé match le ST assigné mais match un autre ST.

**Prévention :** Relire chaque mapping : le texte de la mesure doit clairement correspondre au nom du sous-thème.

### 2.7 PDF scannés (images)

**Problème :** Certains PDF sont des scans d'images, pas du texte sélectionnable.

**Exemple projet :** Tmimi (48 pages scannées) — PyMuPDF retourne des pages vides.

**Solution :** Utiliser Tesseract OCR via `pytesseract`. Sauvegarder le texte extrait dans `data/programmes/{candidat}_full_text.txt` pour référence.

**Prévention :** Tester `fitz.open(pdf).get_page_text(0)` avant de lancer l'extraction complète. Si vide → OCR.

### 2.8 Pages web longues

**Problème :** WebFetch tronque les pages très longues (programmes de 100+ propositions).

**Exemple projet :** Sites avec programme sur une seule page HTML très longue → résumé partiel.

**Solution :** Extraire section par section si le site a des ancres. Sinon, télécharger le PDF.

**Prévention :** Préférer systématiquement le PDF au site web pour les programmes longs.

### 2.9 Pas de traçabilité

**Problème :** Impossible de savoir quel script a généré les données d'un candidat, quelle source a été utilisée, quand.

**Exemple projet :** Après le batch de 10 agents parallèles, certaines villes avaient des données sans trace de l'origine.

**Solution :** 1 script par candidat `reextraire_{id}.py` avec docstring documentant source, URL, date, nombre de mesures.

**Prévention :** Utiliser `template_reextraire.py` comme base. Le template inclut les métadonnées obligatoires.

### 2.10 Doublons

**Problème :** La même mesure apparaît dans plusieurs sous-thèmes du même candidat.

**Exemple projet :** Certaines mesures transversales (« 100% bio dans les cantines ») copiées dans `cantines-fournitures` ET `alimentation-durable`.

**Solution :** `detecter_doublons.py` avec SequenceMatcher seuil 0.85.

**Prévention :** Règle : une mesure = un seul sous-thème. Si elle couvre plusieurs thèmes, la placer dans le plus pertinent.

---

## 3. Hiérarchie des sources

Par ordre de fiabilité décroissante :

| Rang | Source | Fiabilité | Risques |
|------|--------|-----------|---------|
| 1 | **PDF programme officiel** | Maximale | PDF scanné (→ OCR) |
| 2 | **Site officiel candidat** (HTML) | Haute | SPA, troncature, bilan mélangé |
| 3 | **Lien fourni par l'équipe** | Haute | Peut pointer vers un résumé |
| 4 | **Presse locale** | Moyenne | Sélection éditoriale, paraphrase |
| 5 | **Réseaux sociaux** | Faible | Fragmentaire, orienté communication |

**Règle d'or :** PDF > site > presse. Si un PDF existe, c'est la source primaire.

---

## 4. Pipeline d'extraction en 9 étapes

```
1. IDENTIFIER la source
   → Chercher le PDF sur le site, vérifier la hiérarchie §3

2. COMPTER les mesures source
   → Numéroter dans le PDF/site, noter le total AVANT d'extraire

3. EXTRAIRE le texte brut
   → PyMuPDF pour PDF texte, Tesseract pour PDF scanné, copier-coller pour sites JS

4. MAPPER vers les sous-thèmes
   → 1 mesure = 1 sous-thème, inventaire exhaustif

5. FILTRER le bilan
   → Scanner les 10 marqueurs temporels, reformuler ou supprimer

6. SPLITTER les blocs
   → Toute mesure > 200 chars → vérifier si c'est vraiment une seule mesure

7. VÉRIFIER la cohérence
   → Chaque mesure correspond-elle bien à son sous-thème ?

8. VALIDER techniquement
   → python scripts/valider_donnees.py (0 erreur)

9. AUDITER la complétude
   → python scripts/auditer_completude.py --candidat X
   → Vérifier : mesures source = mesures extraites, 0 bilan, 0 blocs, 0 doublons
```

---

## 5. Checklists qualité

### Pré-extraction (4 items)

- [ ] Source identifiée et classée selon la hiérarchie §3
- [ ] Nombre total de mesures dans la source compté et noté
- [ ] Site vérifié dans un navigateur (SPA ? bilan mélangé ?)
- [ ] PDF recherché et téléchargé s'il existe

### Post-extraction (8 items)

- [ ] Nombre de mesures extraites = nombre de mesures source (tolérance ±5%)
- [ ] `auditer_completude.py --candidat X` : 0 bilan détecté
- [ ] `auditer_completude.py --candidat X` : 0 bloc monolithique
- [ ] `detecter_doublons.py` : 0 doublon
- [ ] `valider_donnees.py` : 0 erreur
- [ ] Sources (`source` et `sourceUrl`) renseignées pour chaque sous-thème
- [ ] `programmeComplet` correctement évalué (true si ≥15-20 mesures concrètes)
- [ ] Script d'extraction sauvegardé (`reextraire_{id}.py` ou `completer_{id}.py`)

---

## 6. Format de script standardisé

Utiliser `scripts/template_reextraire.py` comme base pour tout nouveau script d'extraction.

Le template inclut :
- Docstring avec source, URL, date, nombre de mesures
- Dict `MESURES = { "sous-theme-id": ["Mesure 1.", "Mesure 2."] }`
- Safety check : abort si total nouvelles mesures < 50% du total existant
- Message SKIP quand `len(new) < len(old)` pour un sous-thème
- Rappel de validation en fin d'exécution
- UTF-8 stdout wrapper pour Windows

---

## 7. Outils disponibles

| Script | Usage | Quand l'exécuter |
|--------|-------|------------------|
| `valider_donnees.py` | Validation structure JSON | Après chaque modification |
| `auditer_completude.py` | Audit qualité des candidats complets | Après chaque extraction |
| `detecter_doublons.py` | Détection doublons inter/intra candidats | Après chaque extraction |
| `resplit_blocs.py` | Re-découpe blocs monolithiques | Si blocs détectés par l'audit |
| `nettoyer_bilan.py` | Suppression bilan, corrections manuelles | Si bilan détecté par l'audit |
| `template_reextraire.py` | Template script extraction | Pour chaque nouveau candidat |

---

## 8. Indicateurs de référence

### Seuils

| Indicateur | Seuil | Action si dépassé |
|------------|-------|-------------------|
| Mesures par candidat complet | ≥ 20 | Vérifier extraction partielle |
| Sous-thèmes couverts | ≥ 15/44 | Vérifier sections manquantes |
| Mesures > 200 chars | 0 | Passer `resplit_blocs.py` |
| Marqueurs bilan détectés | 0 | Passer `nettoyer_bilan.py` |
| Doublons (similarité > 0.85) | 0 | Supprimer le doublon |
| Sources vides | 0 | Renseigner source et sourceUrl |

### Statistiques de référence (février 2026)

- **Candidats complets** : 69 sur 548 candidats (12.6%)
- **Mesures moyennes par complet** : ~40-60
- **Sous-thèmes couverts moyens** : ~25/44
- **Candidat le plus complet** : Bournazel (Paris) ~200 mesures, Grégoire (Paris) ~165 mesures
- **Seuil programmeComplet** : ≥ 15-20 mesures concrètes et chiffrées
