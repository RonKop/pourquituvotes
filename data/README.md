# Architecture des données — Pour qui tu votes

## Structure des fichiers

```
data/
  villes.json                  <- Index de toutes les villes (~38 KB)
  elections/
    bordeaux-2026.json         <- 1 fichier par ville/election (10-50 KB)
    paris-2026.json
    ...                        <- 34 fichiers
```

## Format : villes.json

Index leger charge au demarrage. Contient les metadonnees et une liste legere de candidats pour la recherche cross-villes.

```json
[
  {
    "id": "paris",
    "nom": "Paris",
    "codePostal": "75000",
    "departement": "75",
    "elections": ["paris-2026"],
    "stats": {
      "candidats": 6,
      "propositions": 94,
      "themes": 12,
      "complets": 2
    },
    "candidats": [
      { "id": "gregoire", "nom": "Emmanuel Gregoire", "liste": "Gauche unie" }
    ]
  }
]
```

## Format : election JSON

Donnees completes d'une election, chargees a la demande quand l'utilisateur selectionne une ville.

```json
{
  "ville": "Paris",
  "annee": 2026,
  "type": "Elections municipales",
  "dateVote": "2026-03-15T08:00:00",
  "candidats": [
    {
      "id": "gregoire",
      "nom": "Emmanuel Gregoire",
      "liste": "...",
      "programmeUrl": "https://...",
      "programmeComplet": true,
      "programmePdfPath": null
    }
  ],
  "categories": [
    {
      "id": "securite",
      "nom": "Securite & Prevention",
      "sousThemes": [
        {
          "id": "police-municipale",
          "nom": "Police municipale",
          "propositions": {
            "gregoire": {
              "mesures": [
                "Mesure concrete 1.",
                "Mesure concrete 2."
              ],
              "source": "Programme officiel 2026",
              "sourceUrl": "https://..."
            },
            "dati": null
          }
        }
      ]
    }
  ]
}
```

## Comment ajouter une ville

1. Creer un script `scripts/generer_maville.py` (copier un existant)
2. Definir `CANDIDATS` (liste de dicts) et `PROPS` (dict de propositions)
3. Appeler `insert_city(ville_id, ville_nom, ville_cp, CANDIDATS, PROPS)`
4. Executer le script : `python scripts/generer_maville.py`
5. Valider : `python scripts/valider_donnees.py`

Le `generateur_commun.py` :
- Ecrit `data/elections/{ville_id}-2026.json`
- Met a jour `data/villes.json` (stats + candidats legers)
- Incremente `DATA_VERSION` dans `app.js` et `home.js` (cache busting)

## Comment mettre a jour des propositions

Modifier le script generateur de la ville, puis le re-executer. Le fichier JSON sera ecrase avec les nouvelles donnees.

## Format des propositions (mesures[])

Chaque proposition d'un candidat pour un sous-theme utilise le format `mesures[]` :

```json
{
  "mesures": ["Mesure 1.", "Mesure 2."],
  "source": "Programme officiel 2026",
  "sourceUrl": "https://..."
}
```

- **mesures** : tableau de strings, chaque string = une mesure concrete et distincte
- **source** : nom du document source (PDF, site officiel)
- **sourceUrl** : URL de la source
- Une mesure = une phrase/action (pas de blocs monolithiques > 200 chars)
- Ancien format `texte` (string unique) encore present sur certains candidats non-complets

## Validation

```bash
python scripts/valider_donnees.py
```

Verifie :
- Coherence villes.json / fichiers elections
- Candidats fantomes (IDs invalides dans les propositions)
- Doublons de sous-themes
- Grille universelle (12 categories, meme ordre)
- Sous-themes communs presents
- Comptage des propositions par candidat

## Audit de completude

```bash
python scripts/auditer_completude.py                     # Tous les complets
python scripts/auditer_completude.py --ville paris       # Par ville
python scripts/auditer_completude.py --candidat gregoire # Par candidat
python scripts/auditer_completude.py --csv rapport.csv   # Export CSV
```

Detecte sur les candidats `programmeComplet: true` :
- Candidats avec < 20 mesures (extraction partielle ?)
- Marqueurs de bilan (track record melange aux propositions)
- Blocs monolithiques (mesures > 200 chars)
- Doublons intra-candidat (similarite > 85%)
- Misclassifications (mesure dans le mauvais sous-theme)
- Sources manquantes (source/sourceUrl vides)

## Autres outils

| Script | Usage |
|--------|-------|
| `detecter_doublons.py` | Detection doublons inter/intra candidats |
| `resplit_blocs.py` | Re-decoupe blocs monolithiques automatiquement |
| `nettoyer_bilan.py` | Suppression bilan et corrections manuelles |
| `template_reextraire.py` | Template pour script de re-extraction |

Voir `METHODOLOGIE_EXTRACTION.md` pour le guide complet d'extraction.

## Dev local

Le site utilise `fetch()` pour charger les donnees. Cela ne fonctionne pas en `file://`. Pour le developpement local :

```bash
cd "FR comp mun"
python -m http.server 8000
```

Puis ouvrir http://localhost:8000 dans le navigateur.

## Cache busting

Les fichiers JSON sont charges avec `?v=DATA_VERSION`. Cette version est incrementee automatiquement par `generateur_commun.py` a chaque mise a jour de donnees. Cela force les navigateurs a re-telecharger les fichiers modifies. 
