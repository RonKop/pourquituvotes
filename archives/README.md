# 🐍 Scripts Python - Comparateur Municipal

Outils pour gérer les données d'élections municipales.

## 📋 Scripts disponibles

### 1. `generate_city.py` - Créer une nouvelle ville

Génère un fichier JSON vide pour une nouvelle ville avec candidats.

**Usage :**
```bash
python generate_city.py <nom_ville> [candidat1] [candidat2] ...
```

**Exemples :**
```bash
# Créer Paris avec 3 candidats
python generate_city.py Paris "Anne Martin" "Pierre Dupont" "Marie Leroy"

# Créer Lyon sans candidats (à ajouter manuellement)
python generate_city.py Lyon
```

**Sortie :** `data/elections/2026/paris.json`

---

### 2. `validate_data.py` - Valider les données

Vérifie tous les fichiers JSON pour détecter les erreurs et problèmes.

**Usage :**
```bash
python validate_data.py
```

**Vérifie :**
- ✅ Structure JSON valide
- ✅ Champs obligatoires présents
- ✅ Cohérence des IDs candidats
- ✅ URLs valides
- ⚠️  Sources manquantes
- ⚠️  Propositions vides

---

### 3. `import_csv.py` - Importer depuis CSV

Importe des propositions depuis un fichier CSV/Excel.

**Usage :**
```bash
python import_csv.py <ville_slug> <fichier.csv>
```

**Format CSV attendu :**
```csv
candidat,categorie,sous_theme,texte,source,source_url
Anne Dupont,Transports & Mobilité,Tramway & Métro,Extension du tramway ligne C,Programme p.22,https://...
Pierre Martin,Environnement & Transition écologique,Espaces verts & Biodiversité,10000 arbres plantés,Programme p.15,#
```

**Exemple :**
```bash
python import_csv.py bordeaux propositions.csv
```

**💡 Astuce :** Créez votre CSV dans Excel, puis exportez en UTF-8.

---

### 4. `stats.py` - Statistiques

Affiche des statistiques sur toutes les villes.

**Usage :**
```bash
python stats.py
```

**Affiche :**
- 📊 Nombre total de villes, candidats, propositions
- 🏙️  Détail par ville
- 🏆 Top 5 villes
- ⚠️  Alertes (villes/candidats sans propositions)

---

## 🚀 Workflow recommandé

### Ajouter une nouvelle ville :

```bash
# 1. Générer le template
python generate_city.py Lyon "Sophie Blanc" "Thomas Noir"

# 2. Remplir les propositions (éditer le JSON ou utiliser CSV)
python import_csv.py lyon propositions_lyon.csv

# 3. Valider
python validate_data.py

# 4. Vérifier les stats
python stats.py
```

---

## 📦 Installation

Aucune dépendance externe requise (Python 3.6+).

Si vous voulez des couleurs dans le terminal Windows :
```bash
pip install colorama
```

---

## 📁 Structure des fichiers

```
FR comp mun/
├── data/
│   └── elections/
│       └── 2026/
│           ├── bordeaux.json
│           ├── paris.json
│           └── ...
├── scripts/
│   ├── generate_city.py
│   ├── validate_data.py
│   ├── import_csv.py
│   ├── stats.py
│   └── README.md
└── templates/
    └── city_template.json
```

---

## 🆘 Aide

Pour voir l'aide d'un script :
```bash
python generate_city.py
python import_csv.py
```

---

## 📝 Notes

- Les fichiers JSON utilisent l'encodage UTF-8
- Les slugs de ville sont en minuscules sans accents (ex: "Saint-Étienne" → "saint-etienne")
- Le format CSV doit utiliser la virgule comme séparateur
