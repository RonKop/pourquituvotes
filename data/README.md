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
              "texte": "...",
              "source": "...",
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

## Dev local

Le site utilise `fetch()` pour charger les donnees. Cela ne fonctionne pas en `file://`. Pour le developpement local :

```bash
cd "FR comp mun"
python -m http.server 8000
```

Puis ouvrir http://localhost:8000 dans le navigateur.

## Cache busting

Les fichiers JSON sont charges avec `?v=DATA_VERSION`. Cette version est incrementee automatiquement par `generateur_commun.py` a chaque mise a jour de donnees. Cela force les navigateurs a re-telecharger les fichiers modifies. 
