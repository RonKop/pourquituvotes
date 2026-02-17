# Méthodologie de recherche des programmes candidats

Guide interne pour la collecte et l'intégration des propositions candidates sur pourquituvotes.fr.

---

## 1. Hiérarchie des sources

Par ordre de fiabilité décroissante :

1. **Lien fourni directement par l'équipe de campagne** (email, formulaire de contact)
2. **PDF programme officiel** téléchargé depuis le site du candidat
3. **Page programme sur le site du candidat** (HTML statique ou CMS)
4. **Articles de presse locale** citant des propositions précises
5. **Réseaux sociaux** (Twitter/X, Facebook) — en dernier recours

**Règle d'or : quand un contact de campagne fournit un lien spécifique, c'est CE lien qui fait autorité.** Ne pas substituer une autre source (API interne, page secondaire, etc.) sans avoir d'abord épuisé le lien fourni.

---

## 2. Protocole d'extraction web

### 2.1 Avant de commencer
- [ ] Identifier la source primaire (cf. hiérarchie §1)
- [ ] Ouvrir le lien dans un navigateur pour vérifier ce qu'il contient réellement
- [ ] Noter si le site utilise un rendu JavaScript côté client (SPA, WordPress + page builder, React, etc.)

### 2.2 Chercher le PDF programme (PRIORITAIRE)
1. **Vérifier s'il existe un PDF programme** sur le site du candidat (lien "Télécharger le programme", "Notre projet", etc.)
2. Si un PDF existe → le télécharger dans `data/programmes/` et l'analyser page par page avec PyMuPDF
3. Le PDF est TOUJOURS la source la plus complète — ne jamais se contenter du site web si un PDF existe

### 2.3 Tentative d'extraction web (si pas de PDF)
1. **WebFetch** sur l'URL exacte fournie
2. Si le contenu est vide ou incomplet → le site est probablement rendu côté client (JS)
3. **Alternatives pour sites JS-heavy :**
   - WordPress : essayer l'API REST (`/wp-json/wp/v2/pages/` ou `/wp-json/wp/v2/posts/`)
   - Mais ATTENTION : l'API REST ne renvoie que les pages/articles individuels, **pas les sections dynamiques de la homepage** (shortcodes, page builders, widgets)
   - Demander à l'utilisateur de copier-coller le contenu depuis le navigateur
   - En dernier recours : utiliser un headless browser (Puppeteer/Playwright)

### 2.4 Validation post-extraction
- [ ] Compter le nombre total de propositions extraites
- [ ] Comparer avec le nombre annoncé par le candidat (s'il est indiqué sur le site)
- [ ] Si écart significatif → il manque probablement des propositions → revenir à la source

---

## 3. Mapping propositions → sous-thèmes

### 3.1 Inventaire exhaustif AVANT le mapping
- Lister TOUTES les propositions extraites dans un inventaire numéroté
- Ne commencer le mapping qu'une fois l'inventaire complet
- Vérifier que le nombre de propositions mappées = nombre total extrait

### 3.2 Règles de mapping
- **Une proposition = un seul sous-thème** (pas de doublons)
- Si une proposition couvre plusieurs thèmes, la placer dans le plus pertinent et agréger les détails
- Si une proposition ne rentre dans aucun sous-thème existant → créer un sous-thème spécifique (ville)
- Relire chaque mapping : le texte doit correspondre au nom du sous-thème

### 3.3 Seuils
- `programmeComplet: true` → au moins 15-20 mesures concrètes ET confirmation que c'est le programme officiel
- `programmeComplet: false` → propositions partielles, issues de presse, ou "grandes orientations" sans détails
- Un "Pacte" ou "Charte" avec 5-10 points généraux ≠ programme complet

---

## 4. Erreurs documentées et leçons apprises

### 4.1 Erreur Bouchet / Tours (février 2026)

**Contexte :** Mikael Rajaonarivony (équipe Bouchet) a fourni le lien `https://tourspourtous.fr/#propositions` contenant les 56 propositions officielles.

**Erreur :** WebFetch n'a pas pu extraire le contenu (site WordPress avec rendu JS côté client). Au lieu de signaler l'échec et demander un copier-coller, on a utilisé l'API REST WordPress (`/wp-json/wp/v2/pages/`) qui ne renvoyait que les pages internes (projet, sécurité), pas la section `#propositions` de la homepage.

**Conséquence :** Seulement 22 propositions intégrées sur 56 → 34 propositions manquantes (61% du programme ignoré).

**Résolution :** L'utilisateur a copié-collé les 56 propositions depuis le navigateur. Script `completer_bouchet.py` créé pour ajouter les 34 manquantes.

**Leçons :**
1. **TOUJOURS vérifier le nombre** : si le site annonce "56 propositions" et qu'on n'en extrait que 22, il y a un problème
2. **Ne pas contourner silencieusement** : si WebFetch échoue sur l'URL fournie, le signaler immédiatement et demander un copier-coller
3. **L'API REST WordPress ≠ le site visible** : les page builders (Elementor, WPBakery, Divi) injectent du contenu via shortcodes que l'API ne résout pas
4. **Le lien fourni par le contact fait autorité** : ne jamais le remplacer par une source alternative sans validation

### 4.2 Erreur Perrein / Montpellier (février 2026)

**Contexte :** L'équipe de campagne d'Isabelle Perrein a répondu par email avec un lien vers le site `isabelleperrein2026.fr`. Le programme PDF officiel (18 pages) était téléchargeable depuis le site.

**Erreur :** On a extrait les propositions uniquement depuis les pages web et des articles de presse (infoccitanie.fr, echo-des-tribunes.com), sans télécharger ni analyser le PDF programme. Résultat : 25 sous-thèmes couverts avec des textes souvent vagues.

**Conséquence :** 14 sous-thèmes entiers manquants (violences-femmes, culture, sport-pour-tous, santé, etc.) et les 25 existants étaient appauvris par rapport au PDF. Soit 39 sous-thèmes réels vs 25 intégrés (36% du programme ignoré).

**Résolution :** Téléchargement du PDF, extraction exhaustive page par page, script `completer_perrein.py` v2 créé avec les 39 sous-thèmes complets.

**Leçons :**
1. **TOUJOURS chercher le PDF programme** : c'est la source la plus complète et fiable. Vérifier s'il y a un lien de téléchargement sur le site du candidat
2. **Le site web ≠ le programme complet** : les pages web peuvent ne montrer qu'un résumé ou des thèmes phares. Le PDF contient généralement l'intégralité
3. **Ne pas se contenter des articles de presse** : la presse ne reprend que les propositions médiatiques, pas les détails sur santé, handicap, culture, etc.
4. **Comparer le nombre de sous-thèmes** : si un programme de 18 pages ne donne que 25 sous-thèmes, il manque probablement des sections entières

### 4.3 Erreur Knafo / Paris (février 2026)

**Contexte :** Le site de campagne redirige automatiquement vers une page différente.

**Leçon :** Toujours suivre les redirections et vérifier l'URL finale avant d'extraire.

### 4.4 Erreur agents parallèles / Marseille (février 2026)

**Contexte :** Plusieurs agents ont modifié le même fichier en parallèle.

**Conséquence :** Données Marseille corrompues (propositions dupliquées x4).

**Leçon :** JAMAIS d'agents parallèles sur le même fichier JSON. Sérialiser les modifications.

---

## 5. Checklist par candidat

Avant de considérer un candidat comme "intégré" :

- [ ] Source identifiée et documentée (URL, date d'accès)
- [ ] Toutes les propositions extraites (nombre vérifié)
- [ ] Mapping complet vers les sous-thèmes (inventaire = mappées)
- [ ] `programmeComplet` correctement évalué (true/false)
- [ ] `programmeUrl` renseigné
- [ ] Script Python créé et exécuté (`completer_[candidat].py`)
- [ ] `valider_donnees.py` passé sans erreur
- [ ] `suivi_candidats.csv` mis à jour (programme_complet, nb_propositions, statut)
- [ ] Commit + push staging + merge main

---

## 6. Workflow type pour un nouveau programme

```
1. Réception (email / découverte presse)
   ↓
2. Identifier la source primaire (lien fourni > site > presse)
   ↓
3. Tenter extraction (WebFetch → API REST → copier-coller)
   ↓
4. Inventaire exhaustif (compter TOUTES les propositions)
   ↓
5. Mapping sous-thèmes (1 proposition = 1 sous-thème)
   ↓
6. Créer script Python (completer_[candidat].py)
   ↓
7. Exécuter + valider (valider_donnees.py)
   ↓
8. Mettre à jour suivi_candidats.csv
   ↓
9. Commit + push + merge
```
