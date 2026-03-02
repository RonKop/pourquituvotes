---
name: audit
description: Auditer la qualité et la complétude d'un candidat ou d'une ville sur pourquituvotes.fr. S'active automatiquement quand l'utilisateur demande de vérifier, auditer ou contrôler un candidat ou une ville, ou après une intégration pour valider la qualité.
---

# Audit de complétude candidat/ville

Audite la qualité des données pour un candidat ou une ville.

## Entrée attendue

`$ARGUMENTS` : nom du candidat et/ou ville (ex: "belhamiti nantes", "paris", "dejenlis")

## Étape 1 — Identifier la cible

Si un candidat est spécifié, auditer ce candidat.
Si seule une ville est spécifiée, auditer tous les candidats de cette ville.

## Étape 2 — Charger les données

```bash
python -c "
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('data/elections/{ville}-2026.json','r',encoding='utf-8') as f:
    data = json.load(f)
# ... analyse
"
```

## Étape 3 — Vérifications

Pour chaque candidat audité, vérifier :

### 3a. Couverture des sous-thèmes
- Combien de sous-thèmes couverts sur 44 (ou sur le total de la ville si sous-thèmes spécifiques)
- Catégories entièrement vides (0 sous-thèmes)
- Score de couverture en %

### 3b. Doublons
- Chercher des mesures quasi-identiques (même début de phrase, cosinus similarity textuel simple)
- Mesures dupliquées dans plusieurs sous-thèmes

### 3c. Qualité des mesures
- Mesures trop courtes (< 30 caractères)
- Mesures trop longues (> 500 caractères)
- Mesures vagues sans verbe d'action ni chiffre
- Phrases de bilan/autosatisfaction (contenant "nous avons", "depuis 20", "grâce à")

### 3d. Cohérence du mapping
- Vérifier que les mesures correspondent au sous-thème (ex: une mesure transport dans "logement")
- Signaler les cas suspects

### 3e. Méta-données
- `programmeComplet` cohérent avec le nombre de mesures (>= 15 concrètes pour true)
- `programmeUrl` non vide et non "#"

## Étape 4 — Rapport

Afficher un rapport structuré :

```
=== AUDIT : {Candidat} ({Ville}) ===

Mesures totales    : XX
Sous-thèmes        : XX/44
Catégories          : XX/12
programmeComplet   : true/false

[ OK ] Pas de doublons détectés
[WARN] 2 mesures trop courtes :
  - "securite/police-municipale" : "Renforcer la police."
[WARN] 1 catégorie vide : sport
[ OK ] Pas de phrases de bilan
[WARN] programmeUrl manquant

Score qualité : X/10
```

## Étape 5 — Script automatisé (si disponible)

Si le script `scripts/auditer_completude.py` existe, l'utiliser :

```bash
python scripts/auditer_completude.py --ville {ville} --candidat {candidat_id}
```
