"""
Script pour ajouter des propositions à 3 candidats dans lyon-2026.json :
- Belouassa : programmeComplet -> true, +10 propositions
- Perrin-Gilbert : programmeComplet -> true, +11 propositions
- Képénékian : programmeComplet reste false, +7 propositions
"""

import json
import os

FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "data", "elections", "lyon-2026.json")

with open(FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- 1. Mettre programmeComplet à true pour belouassa et perrin-gilbert ---
for c in data["candidats"]:
    if c["id"] == "belouassa":
        c["programmeComplet"] = True
    elif c["id"] == "perrin-gilbert":
        c["programmeComplet"] = True

# --- Helper : trouver un sous-thème par id ---
def get_sous_theme(data, sous_theme_id):
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] == sous_theme_id:
                return st
    raise KeyError(f"Sous-thème '{sous_theme_id}' introuvable")

# --- 2. Propositions Belouassa (10) ---
belouassa_props = {
    "police-municipale": {
        "texte": "Désarmement de la police municipale : retirer l'arme létale aux policiers municipaux dont les compétences ne sont pas d'agir sur des lieux de crime",
        "source": "Programme Lyon Fière et Populaire 2026",
        "sourceUrl": "https://lafranceinsoumise.fr/"
    },
    "prevention-mediation": {
        "texte": "Priorité à la prévention plutôt qu'à la répression : restaurer la confiance entre citoyens et police municipale",
        "source": "Programme Lyon Fière et Populaire 2026",
        "sourceUrl": "https://lafranceinsoumise.fr/"
    },
    "encadrement-loyers": {
        "texte": "Encadrement strict des loyers contre la spéculation immobilière et la multipropriété",
        "source": "Programme Lyon Fière et Populaire 2026",
        "sourceUrl": "https://lafranceinsoumise.fr/"
    },
    "periscolaire-loisirs": {
        "texte": "Statut pour les familles monoparentales avec carte spécialisée donnant des droits concrets (cantine, périscolaire, colonies de vacances municipales)",
        "source": "Programme Lyon Fière et Populaire 2026",
        "sourceUrl": "https://lafranceinsoumise.fr/"
    },
    "ecoles-renovation": {
        "texte": "Restauration scolaire en régie municipale directe, fin de la délégation au privé",
        "source": "Programme Lyon Fière et Populaire 2026",
        "sourceUrl": "https://lafranceinsoumise.fr/"
    },
    "climat-adaptation": {
        "texte": "Écologie populaire qui ne pénalise pas les populations précaires, végétalisation prioritaire des quartiers populaires",
        "source": "Programme Lyon Fière et Populaire 2026",
        "sourceUrl": "https://lafranceinsoumise.fr/"
    },
    "aide-sociale": {
        "texte": "Hébergement de tous les enfants sans-abri et de leurs familles (environ 200 enfants et familles actuellement à la rue à Lyon)",
        "source": "Programme Lyon Fière et Populaire 2026",
        "sourceUrl": "https://lafranceinsoumise.fr/"
    },
    "pouvoir-achat": {
        "texte": "Gratuité des cantines = 550 € de pouvoir d'achat par an et par enfant. Coût estimé à 8 M€, avec création de 100-125 ETP",
        "source": "Programme Lyon Fière et Populaire 2026",
        "sourceUrl": "https://lafranceinsoumise.fr/"
    },
    "commerce-local": {
        "texte": "Création de maisons des communs inspirées des maisons du peuple : lieux d'engagement civique et de restauration solidaire dans chaque quartier",
        "source": "Programme Lyon Fière et Populaire 2026",
        "sourceUrl": "https://lafranceinsoumise.fr/"
    },
    "tarifs-gratuite": {
        "texte": "Gratuité des transports pour les moins de 26 ans dans un premier temps, puis gratuité totale progressive du réseau TCL",
        "source": "Programme Lyon Fière et Populaire 2026",
        "sourceUrl": "https://lafranceinsoumise.fr/"
    },
}

# --- 3. Propositions Perrin-Gilbert (11) ---
perrin_gilbert_props = {
    "violences-femmes": {
        "texte": "Centre d'hébergement d'urgence pour les femmes victimes de violences, réseau de logements-relais, brigade municipale des femmes et des familles",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
    "commerce-local": {
        "texte": "Fonds annuel de soutien de 3,5 M€ pour les artisans et commerçants indépendants impactés par les travaux et chantiers urbains",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
    "amenagement-urbain": {
        "texte": "Ralentir les chantiers en cours, achever les travaux actuels et adapter les projets avant d'en lancer de nouveaux",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
    "accessibilite": {
        "texte": "Technicien de quartier dans chaque maison de quartier pour traiter les réclamations voirie, propreté et stationnement",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
    "seniors": {
        "texte": "Grand plan de formation pour les métiers du grand âge, opposition à la marchandisation du secteur de la dépendance",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
    "transparence": {
        "texte": "Création d'un Conseil Économique, Social et Environnemental Municipal (CESEM) composé de 4 collèges, consulté avant chaque vote de budget",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
    "ecoles-renovation": {
        "texte": "Travaux prioritaires de rénovation dans les bâtiments scolaires dégradés, crédits d'investissement votés dès les premières semaines du mandat",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
    "attractivite": {
        "texte": "Faire de Lyon une capitale européenne des secteurs santé, numérique et innovation pour créer des emplois locaux",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
    "jeunesse": {
        "texte": "Étages du CLIP dédiés au logement des jeunes, avec médiathèque et espace jeux vidéo au rez-de-chaussée",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
    "proprete-dechets": {
        "texte": "Technicien de quartier dans chaque maison de quartier dédié au suivi de la propreté urbaine et de la collecte",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
    "pouvoir-achat": {
        "texte": "Engagement à ne pas faire d'annonces non finançables, refus de vendre le patrimoine municipal (Halle Tony Garnier, musée Guimet)",
        "source": "Programme Lyon en commun 2026",
        "sourceUrl": "https://tribunedelyon.fr/"
    },
}

# --- 4. Propositions Képénékian (7) ---
kepenekian_props = {
    "climat-adaptation": {
        "texte": "Plan Lyon Fraîcheur 2030 de 50 M€ : réseau de mini-canaux dans 50 rues, 12 bassins de rafraîchissement par arrondissement, plages urbaines et 15 000 kits climatiques gratuits",
        "source": "Lyon Capitale, février 2026",
        "sourceUrl": "https://www.lyoncapitale.fr/"
    },
    "renovation-energetique": {
        "texte": "Subventions pour la remise en place de persiennes et volets lyonnais, VMC double flux et géothermie dans les bâtiments publics",
        "source": "Lyon Capitale, février 2026",
        "sourceUrl": "https://www.lyoncapitale.fr/"
    },
    "amenagement-urbain": {
        "texte": "Voilages intelligents (ombrages déployés) sur 30 axes commerciaux (5 M€), réseau de référents climat dans chaque immeuble",
        "source": "Lyon Capitale, février 2026",
        "sourceUrl": "https://www.lyoncapitale.fr/"
    },
    "transparence": {
        "texte": "Tirage au sort de 100 Lyonnais pour débattre des nouveaux projets municipaux et les présenter au conseil municipal",
        "source": "Lyon Capitale, février 2026",
        "sourceUrl": "https://www.lyoncapitale.fr/"
    },
    "emploi-insertion": {
        "texte": "Incubateur d'entreprises dans chaque quartier prioritaire de la politique de la ville",
        "source": "Lyon Capitale, février 2026",
        "sourceUrl": "https://www.lyoncapitale.fr/"
    },
    "velo-mobilites-douces": {
        "texte": "Maintien des pistes cyclables, équilibre ville pour tous entre vélo, piétons et voitures",
        "source": "Lyon Capitale, février 2026",
        "sourceUrl": "https://www.lyoncapitale.fr/"
    },
    "prevention-sante": {
        "texte": "Programme de prévention majeur, Lyon capitale du soin",
        "source": "Lyon Capitale, février 2026",
        "sourceUrl": "https://www.lyoncapitale.fr/"
    },
}

# --- Appliquer les propositions ---
def apply_props(data, candidat_id, props_dict):
    count = 0
    for sous_theme_id, prop in props_dict.items():
        st = get_sous_theme(data, sous_theme_id)
        old_val = st["propositions"].get(candidat_id)
        if old_val is not None:
            print(f"  ATTENTION : {candidat_id}/{sous_theme_id} avait déjà une proposition, elle sera REMPLACÉE")
        st["propositions"][candidat_id] = prop
        count += 1
    print(f"  -> {count} propositions ajoutées pour {candidat_id}")

print("=== Belouassa ===")
apply_props(data, "belouassa", belouassa_props)

print("=== Perrin-Gilbert ===")
apply_props(data, "perrin-gilbert", perrin_gilbert_props)

print("=== Képénékian ===")
apply_props(data, "kepenekian", kepenekian_props)

# --- Vérifications ---
print("\n=== Vérification programmeComplet ===")
for c in data["candidats"]:
    print(f"  {c['id']}: programmeComplet = {c['programmeComplet']}")

# --- Écriture ---
with open(FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nFichier écrit : {FILE}")
print("Terminé !")
