#!/usr/bin/env python3
"""
Mise à jour du programme complet de Guillaume Lescaut (Aubervilliers 2026).
Source : https://guillaumelescaut2026.fr/programme
"""

import json
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_DIR, "data", "elections", "aubervilliers-2026.json")

SOURCE = "Programme officiel 2026 — Guillaume Lescaut"
SOURCE_URL = "https://guillaumelescaut2026.fr/programme"

# ── Mapping: catégorie_id -> sous_theme_id -> liste de mesures ──

PROGRAMME = {
    "securite": {
        "police-municipale": [
            "Créer une police municipale de proximité axée sur le lien de confiance avec les habitants."
        ],
        "prevention-mediation": [
            "Développer des actions de prévention du racisme, du sexisme et des LGBTQIphobies.",
            "Engagement de la ville contre les violations du droit international et pour la paix."
        ],
        "violences-femmes": [
            "Créer des places d'hébergement d'urgence dédiées aux femmes et enfants victimes de violences."
        ]
    },
    "transports": {
        "velo-mobilites-douces": [
            "Créer des pistes cyclables dédiées reliant la commune à l'agglomération.",
            "Assurer la continuité et la sécurité du réseau cyclable sur toute la ville.",
            "Installer des stationnements vélo sécurisés (abris, consignes) dans chaque quartier.",
            "Proposer des subventions pour l'achat de vélos, vélos cargo et vélos à assistance électrique.",
            "Mettre en place des programmes d'éducation au vélo pour tous les âges."
        ],
        "pietons-circulation": [
            "Rendre les trottoirs accessibles aux poussettes et fauteuils roulants.",
            "Créer des tronçons piétons, rues-jardins et placettes dans les quartiers.",
            "Déployer une signalétique piétonne avec des itinéraires moins pollués.",
            "Instaurer un moratoire sur la ZFE jusqu'à ce que des alternatives de mobilité suffisantes soient déployées."
        ]
    },
    "logement": {
        "logement-social": [
            "Geler les loyers de l'OPH d'Aubervilliers pendant toute la durée du mandat.",
            "Tripler le nombre d'agents de proximité à l'OPH.",
            "Rendre la régularisation des charges locatives OPH compréhensible pour les locataires.",
            "Construire 1 000 nouveaux logements sociaux sur le mandat.",
            "Refuser toute vente de logements sociaux (avis conforme « zéro vente »).",
            "Exercer le droit de préemption pour maintenir les logements dans le secteur public."
        ],
        "logements-vacants": [
            "Réquisitionner les logements vides pour héberger les personnes sans-abri.",
            "Mettre en place une stratégie « logement d'abord » avec structures d'insertion (pensions de famille, maisons relais)."
        ],
        "encadrement-loyers": [
            "Appliquer strictement l'encadrement des loyers et accompagner les locataires dans leurs recours.",
            "Étendre le permis de louer à toute la ville avec des contrôles renforcés.",
            "Créer une brigade municipale de défense des locataires."
        ],
        "acces-logement": [
            "Lutter contre les passoires thermiques et l'habitat insalubre avec des moyens renforcés.",
            "Prendre des arrêtés anti-expulsion sans relogement préalable.",
            "Garantir le droit à la domiciliation pour les sans-abris, avec bagagerie, et refuser les arrêtés anti-mendicité et le mobilier anti-SDF."
        ]
    },
    "education": {
        "petite-enfance": [
            "Créer de nouvelles places en crèches publiques.",
            "Favoriser les structures petite enfance publiques et associatives plutôt que le privé lucratif.",
            "Ouvrir une Maison des assistantes maternelles.",
            "Lancer un plan de formation pour les métiers de la petite enfance et de l'animation."
        ],
        "ecoles-renovation": [
            "Rénover les écoles : isolation thermique, ventilation, végétalisation des cours de récréation.",
            "Garantir 1 ATSEM à plein temps par classe de maternelle.",
            "Organiser des classes transplantées pour tous les élèves."
        ],
        "cantines-fournitures": [
            "Instaurer la gratuité de la cantine scolaire dès 2027.",
            "Supprimer les pénalités d'absence à la cantine.",
            "Abolir le système Franclet de réservation cantine/périscolaire."
        ],
        "periscolaire-loisirs": [
            "Augmenter l'encadrement par enfant en recrutant, formant et titularisant des animateurs.",
            "Démocratiser l'accès aux centres de loisirs et aux vacances pour tous les enfants."
        ],
        "jeunesse": [
            "Défendre et développer les espaces et associations dédiés à la jeunesse."
        ]
    },
    "environnement": {
        "espaces-verts": [
            "Sanctuariser les Jardins ouvriers des Vertus (2 700 m²).",
            "Créer des îlots de fraîcheur, installer des fontaines et végétaliser l'espace public.",
            "Mettre en place un plan de renaturation des sols contre le ruissellement et les inondations.",
            "Développer des jardins partagés avec accès à l'eau.",
            "Créer des sanctuaires pour la faune urbaine et favoriser la biodiversité.",
            "Assurer une gestion humaine des nuisibles (sans cruauté)."
        ],
        "proprete-dechets": [
            "Ouvrir des ressourceries et recycleries municipales.",
            "Développer les filières de réemploi et de « mines urbaines » pour valoriser les déchets locaux."
        ],
        "climat-adaptation": [
            "Déclarer l'état d'urgence climatique dès le premier conseil municipal.",
            "Créer un Conseil citoyen de la transition écologique (CCTE).",
            "Mettre en place un budget vert classant les dépenses municipales selon leur impact carbone.",
            "Imposer un moratoire sur les constructions privées pour dédensifier la ville.",
            "Déployer un plan canicule : recensement des habitants vulnérables, lieux de fraîcheur, gratuité des piscines.",
            "Lancer un plan d'éducation populaire aux enjeux environnementaux.",
            "Intégrer des critères écologiques exigeants dans tous les marchés publics."
        ],
        "renovation-energetique": [
            "Élaborer un plan de transition énergétique : développement des énergies renouvelables et réduction de la consommation.",
            "Réaliser des audits énergétiques des logements et aider les habitants à accéder aux aides à la rénovation.",
            "Installer des systèmes de récupération d'eau de pluie sur les bâtiments municipaux et subventionner les installations résidentielles."
        ],
        "alimentation-durable": [
            "Créer une cuisine centrale municipale en reprenant la gestion de la restauration collective en régie.",
            "Maximiser la part de bio et bannir les produits ultra-transformés dans les cantines.",
            "Expérimenter une Sécurité sociale de l'alimentation à l'échelle municipale."
        ]
    },
    "sante": {
        "centres-sante": [
            "Ouvrir un centre de santé municipal gratuit.",
            "Nouer des partenariats médicaux avec l'ARS pour améliorer l'offre de soins."
        ],
        "prevention-sante": [
            "Développer la formation locale de professionnels de santé.",
            "Intégrer des normes de bien-être animal dans les marchés publics de la ville.",
            "Soutenir les services de sauvetage et d'adoption animale sur le territoire."
        ]
    },
    "democratie": {
        "budget-participatif": [
            "Installer des conseils citoyens dans les Maisons de quartier dotés de budgets participatifs.",
            "Instaurer une votation citoyenne annuelle sur les grands sujets municipaux (quorum 10 %).",
            "Créer un RIC municipal dont les résultats sont respectés dès 2 000 signatures."
        ],
        "transparence": [
            "Publier en ligne la transparence des votes municipaux.",
            "Créer un observatoire citoyen indépendant composé d'habitants tirés au sort.",
            "Instaurer un droit à la révocation des élus par pétition (seuil 10 %).",
            "Organiser des réunions de compte-rendu de mandat dans chaque quartier chaque année.",
            "Ouvrir le journal municipal à la contribution de tous les habitants."
        ],
        "vie-associative": [
            "Créer une carte citoyenne d'Aubervilliers (sans mention de genre ni de nationalité, accessible dès 16 ans).",
            "Instaurer un droit d'interpellation du maire (500 signatures).",
            "Promouvoir le droit de vote des étrangers extra-européens et les parrainages républicains.",
            "Mener des campagnes annuelles d'inscription sur les listes électorales."
        ],
        "services-publics": [
            "Installer des écrivains publics et travailleurs sociaux dans les Maisons de quartier.",
            "Reprendre en régie publique la gestion de l'eau, des déchets et des ascenseurs.",
            "Supprimer les contrats avec les cabinets de conseil.",
            "Créer un laboratoire d'innovation publique.",
            "Exiger auprès de l'État une augmentation des dotations (DGF).",
            "Plans de titularisation des agents municipaux et suppression du temps partiel imposé.",
            "Expérimenter la semaine de 32 heures pour les agents en postes difficiles."
        ]
    },
    "economie": {
        "emploi-insertion": [
            "Créer des structures d'insertion par l'activité économique (pensions de famille, maisons relais)."
        ]
    },
    "culture": {
        "equipements-culturels": [
            "Ouvrir des Maisons de quartier des arts et des cultures accessibles à tous."
        ]
    },
    "urbanisme": {
        "amenagement-urbain": [
            "Imposer un moratoire sur les constructions privées pour dédensifier la ville et préserver le cadre de vie."
        ],
        "accessibilite": [
            "Rendre l'ensemble des trottoirs et espaces publics accessibles aux personnes à mobilité réduite."
        ]
    },
    "solidarite": {
        "aide-sociale": [
            "Mettre en place une stratégie « logement d'abord » couplée à un accompagnement social renforcé.",
            "Garantir la domiciliation, la bagagerie et l'accès aux droits pour les personnes sans-abri."
        ],
        "egalite-discriminations": [
            "Créer un observatoire municipal des discriminations.",
            "Mener des actions de prévention contre le racisme, le sexisme et les LGBTQIphobies."
        ],
        "pouvoir-achat": [
            "Geler les loyers HLM et lutter contre les charges abusives pour préserver le pouvoir d'achat des habitants."
        ]
    }
}


def main():
    # Load JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update candidat metadata
    for c in data["candidats"]:
        if c["id"] == "lescaut":
            c["programmeUrl"] = "https://guillaumelescaut2026.fr/"
            c["programmeComplet"] = True
            break

    # Count measures before
    old_count = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            prop = st["propositions"].get("lescaut")
            if prop and isinstance(prop, dict) and prop.get("mesures"):
                old_count += len(prop["mesures"])

    # Apply new programme
    new_count = 0
    themes_touched = 0
    for cat in data["categories"]:
        cat_id = cat["id"]
        if cat_id not in PROGRAMME:
            continue
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in PROGRAMME[cat_id]:
                mesures = PROGRAMME[cat_id][st_id]
                st["propositions"]["lescaut"] = {
                    "source": SOURCE,
                    "sourceUrl": SOURCE_URL,
                    "mesures": mesures
                }
                new_count += len(mesures)
                themes_touched += 1

    # Write back
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Stats
    print(f"=== Mise à jour Lescaut (Aubervilliers) ===")
    print(f"Mesures avant : {old_count}")
    print(f"Mesures après : {new_count}")
    print(f"Sous-thèmes renseignés : {themes_touched}/44")
    print(f"programmeComplet : true")
    print(f"programmeUrl : https://guillaumelescaut2026.fr/")
    print(f"Fichier : {JSON_PATH}")

    # Detail by category
    print(f"\n--- Détail par catégorie ---")
    for cat in data["categories"]:
        cat_count = 0
        for st in cat["sousThemes"]:
            prop = st["propositions"].get("lescaut")
            if prop and isinstance(prop, dict) and prop.get("mesures"):
                cat_count += len(prop["mesures"])
        if cat_count > 0:
            print(f"  {cat['nom']}: {cat_count} mesures")


if __name__ == "__main__":
    main()
