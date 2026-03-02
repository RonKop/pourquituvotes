---
name: integrer
description: Intégrer le programme complet d'un candidat aux municipales 2026. S'active automatiquement quand l'utilisateur demande de checker un mail de candidat, intégrer un programme, ou traiter un PDF/Word/site web de programme électoral. Couvre tout le workflow : extraction, mapping aux 44 sous-thèmes, création du script, exécution, validation, commit, push et rédaction du mail de réponse.
---

# Intégration d'un programme candidat

Tu vas intégrer un programme candidat sur pourquituvotes.fr. Suis ce workflow étape par étape.

## Entrée attendue

L'utilisateur fournit : `$ARGUMENTS` (nom du candidat, ville, et/ou source : email, PDF, site web)

## Étape 1 — Identifier la source

- Si email mentionné : chercher le mail avec Gmail MCP tools
- Si PDF : chercher le fichier le plus récent dans `data/programmes/`
- Si site web : utiliser WebFetch pour extraire le contenu
- Si fichier Word (.docx) : utiliser python-docx pour extraire

## Étape 2 — Vérifier le candidat dans les données

```bash
python -c "
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('data/elections/{VILLE}-2026.json','r',encoding='utf-8') as f:
    data = json.load(f)
for c in data['candidats']:
    print(f\"{c['id']}: {c['nom']} - programmeComplet: {c.get('programmeComplet', False)}\")
"
```

Vérifier :
- Le candidat existe bien dans le JSON de la ville
- Son `id` (sera utilisé comme CANDIDAT_ID)
- Son statut actuel (programmeComplet, nombre de mesures existantes)

## Étape 3 — Extraire et compter les mesures

- Lire TOUT le contenu source (PDF complet, site entier)
- Compter le nombre total de propositions/mesures identifiables
- Si < 15 mesures concrètes → `programmeComplet: false`
- Si >= 15 mesures concrètes et chiffrées → `programmeComplet: true`

## Étape 4 — Mapper aux 44 sous-thèmes

Les 12 catégories et 44 sous-thèmes standard sont :

1. `securite` : police-municipale, videoprotection, prevention-mediation, violences-femmes
2. `transports` : transports-en-commun, velo-mobilites-douces, pietons-circulation, stationnement, tarifs-gratuite
3. `logement` : logement-social, logements-vacants, encadrement-loyers, acces-logement
4. `education` : petite-enfance, ecoles-renovation, cantines-fournitures, periscolaire-loisirs, jeunesse
5. `environnement` : espaces-verts, proprete-dechets, climat-adaptation, renovation-energetique, alimentation-durable
6. `sante` : centres-sante, prevention-sante, seniors
7. `democratie` : budget-participatif, transparence, vie-associative, services-publics
8. `economie` : commerce-local, emploi-insertion, attractivite
9. `culture` : equipements-culturels, evenements-creation
10. `sport` : equipements-sportifs, sport-pour-tous
11. `urbanisme` : amenagement-urbain, accessibilite, quartiers-prioritaires
12. `solidarite` : aide-sociale, egalite-discriminations, pouvoir-achat

Règles de mapping :
- **1 mesure = 1 seul sous-thème** (pas de doublons)
- Sous-thème `None` si aucune mesure ne correspond
- Filtrer les phrases de bilan/autosatisfaction (regex : "nous avons", "depuis 20", "grâce à notre")
- Reformuler en phrases concises commençant par un verbe d'action
- Vérifier que chaque texte correspond bien au nom du sous-thème

## Étape 5 — Créer le script Python

Créer `scripts/update_{candidat_id}_{ville}.py` en suivant exactement le pattern des scripts existants. Exemples de référence :
- `scripts/update_belhamiti_nantes.py`
- `scripts/update_payet_saintdenis.py`
- `scripts/update_dejenlis_amiens.py`

Structure obligatoire :
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, sys
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "{ville}-2026.json")
CANDIDAT_ID = "{id}"
PROPOSITIONS = { ... }  # dict sous-thème → liste mesures ou None
def main(): ...
```

## Étape 6 — Exécuter et valider

```bash
python scripts/update_{candidat_id}_{ville}.py
python scripts/valider_donnees.py
```

Vérifier que la validation passe (RÉSULTAT : TOUT EST OK).

## Étape 7 — Commit et push

```bash
git add data/elections/{ville}-2026.json scripts/update_{candidat_id}_{ville}.py
git commit -m "feat({ville}): intégrer programme complet {nom} ({N} mesures)

Source : {source}, reçu le {date}.
{M} sous-thèmes couverts, programmeComplet: {true/false}.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push
```

## Étape 8 — Rédiger le mail de réponse

Rédiger un mail de réponse poli et professionnel :
- Remercier pour l'envoi du programme
- Indiquer le nombre de mesures intégrées et les thématiques couvertes
- Mentionner que le programme est consultable sur pourquituvotes.fr
- Inviter à signaler toute correction
- Signer "Ron Kopelman, pourquituvotes.fr"
