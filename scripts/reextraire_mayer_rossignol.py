#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ré-extraction des propositions de Nicolas Mayer-Rossignol (Rouen 2026)."""
import io, json, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "rouen-2026.json")
SOURCE = "Programme officiel 2026 — Nicolas Mayer-Rossignol"
SOURCE_URL = "https://www.fiersderouen.fr/"
CANDIDAT_ID = "mayer-rossignol"

MESURES = {
    # === SÉCURITÉ ===
    "police-municipale": [
        "Doubler les effectifs de la police municipale de nuit pour assurer une présence 7 jours sur 7 (actuellement mardi-dimanche seulement).",
        "Créer une brigade de nuit permanente de la police municipale pour couvrir l'ensemble de la semaine.",
    ],
    "videoprotection": [
        "Poursuivre le déploiement de la vidéoprotection dans les quartiers sensibles de Rouen.",
    ],
    "prevention-mediation": [
        "Renforcer la médiation et la prévention de la délinquance dans les quartiers prioritaires.",
    ],

    # === TRANSPORTS ===
    "transports-en-commun": [
        "Lancer le projet d'un nouveau métro-tramway pour renforcer le réseau de transports en commun rouennais.",
        "Maintenir la gratuité des transports en commun le samedi pour tous, sans conditions.",
    ],
    "velo-mobilites-douces": [
        "Poursuivre le développement des pistes cyclables sur le modèle du boulevard de l'Europe, parmi les meilleures de la métropole.",
        "Développer les infrastructures de mobilités douces pour favoriser les déplacements à vélo.",
    ],
    "pietons-circulation": [
        "Rénover les trottoirs pour améliorer le confort et la sécurité des piétons.",
        "Développer l'éclairage intelligent (« éclairage malin ») modulant l'intensité lumineuse selon les heures : 100 %, 50 %, 30 %, 20 %.",
    ],
    "tarifs-gratuite": [
        "Instaurer la gratuité des transports en commun pour les moins de 25 ans et les plus de 65 ans.",
    ],

    # === LOGEMENT ===
    "acces-logement": [
        "Créer un bouclier social pour les familles monoparentales avec aide financière à la garde d'enfants et accès prioritaire au logement et aux crèches.",
        "Expérimenter un permis de louer, sur le modèle d'Elbeuf et Saint-Étienne-du-Rouvray, pour lutter contre l'habitat indigne.",
    ],
    "logement-social": [
        "Poursuivre la construction de logements sociaux pour répondre aux besoins des habitants de Rouen.",
    ],

    # === ÉDUCATION ===
    "petite-enfance": [
        "Créer un nouveau groupe scolaire sur les hauteurs de Rouen.",
        "Créer un nouveau groupe scolaire dans le quartier Flaubert avec 17 classes, livraison prévue d'ici 2030.",
        "Accorder un accès prioritaire aux crèches pour les familles monoparentales dans le cadre du bouclier social.",
    ],
    "ecoles-renovation": [
        "Investir dans la rénovation et la construction d'écoles pour offrir un meilleur cadre d'apprentissage.",
    ],
    "cantines-fournitures": [
        "Développer l'alimentation saine dans les cantines scolaires avec davantage de produits bio et locaux.",
        "Mettre en place le « bio sur ordonnance » pour promouvoir une alimentation de qualité.",
    ],

    # === ENVIRONNEMENT ===
    "espaces-verts": [
        "Poursuivre la renaturation de Rouen avec un programme ambitieux de végétalisation de la ville.",
        "Créer une forêt urbaine dans le quartier Flaubert comme poumon vert à proximité des anciennes installations industrielles.",
    ],
    "proprete-dechets": [
        "Augmenter les sanctions financières contre les incivilités et les dépôts sauvages.",
        "Rénover les trottoirs et améliorer la propreté dans tous les quartiers de la ville.",
    ],
    "climat-adaptation": [
        "Viser la réduction de moitié du nombre de jours de dépassement des seuils de pollution atmosphérique.",
        "Atteindre le zéro artificialisation nette sur l'ensemble du territoire métropolitain.",
        "Amplifier l'acquisition et la dépollution des friches industrielles pour transformer ces sites en espaces utiles.",
    ],
    "renovation-energetique": [
        "Accélérer la rénovation énergétique des bâtiments publics et des logements.",
    ],
    "alimentation-durable": [
        "Développer l'agriculture urbaine et les circuits courts sur le territoire métropolitain.",
        "Promouvoir l'économie circulaire avec le transport fluvial de marchandises.",
    ],

    # === SANTÉ ===
    "centres-sante": [
        "Créer un centre de santé municipal avec des médecins salariés par la ville pour garantir à chaque Rouennais un médecin traitant.",
        "Ouvrir deux nouvelles maisons France Santé dans les quartiers des Sapins et de Saint-Éloi pour des consultations rapides de premier recours.",
    ],
    "prevention-sante": [
        "Mettre en place une mutuelle communale pour faciliter l'accès aux soins des 44 % de Rouennais sans couverture complémentaire.",
        "Offrir la première consultation psychologique gratuite pour les moins de 25 ans.",
        "Renforcer le soutien à la Maison des adolescents pour la santé mentale des jeunes.",
        "Développer le « sport sur ordonnance » avec des activités adaptées notamment pour les seniors.",
        "Rendre le stationnement gratuit dans les établissements de santé pour faciliter l'accès aux soins.",
    ],
    "seniors": [
        "Distribuer des chèques-cadeaux aux seniors isolés pour lutter contre l'isolement.",
        "Renforcer les groupes d'échange et de convivialité pour les seniors.",
        "Faire de Rouen une ville pour bien vieillir avec des services et infrastructures adaptés.",
    ],

    # === DÉMOCRATIE ===
    "budget-participatif": [
        "Créer un conseil citoyen chargé de formuler des propositions sur les politiques publiques pour associer les habitants aux décisions.",
    ],
    "transparence": [
        "Garantir la transparence dans la gestion municipale avec une gouvernance ouverte.",
    ],

    # === ÉCONOMIE ===
    "commerce-local": [
        "Soutenir le commerce local et la diversité commerciale en centre-ville.",
    ],
    "emploi-insertion": [
        "Expérimenter le dispositif « Territoires zéro chômeur de longue durée » dans les quartiers prioritaires.",
        "Développer l'économie circulaire et l'agriculture urbaine comme leviers d'emploi local.",
    ],
    "attractivite": [
        "Faire de Rouen la capitale du sport féminin.",
        "Sanctuariser les budgets culturels de la ville et de la métropole comme levier d'attractivité.",
    ],

    # === CULTURE ===
    "equipements-culturels": [
        "Sanctuariser et augmenter les budgets dédiés à la culture pour la ville et la métropole de Rouen.",
        "Poursuivre la restauration de l'abbatiale Saint-Ouen comme symbole du renouveau de la ville.",
    ],

    # === SPORT ===
    "equipements-sportifs": [
        "Développer les infrastructures sportives pour faire de Rouen une ville de référence pour le sport.",
    ],
    "sport-pour-tous": [
        "Développer le sport pour tous avec un accent particulier sur le sport féminin et le sport adapté.",
        "Promouvoir le sport-santé avec des programmes accessibles à toutes les tranches d'âge.",
    ],

    # === URBANISME ===
    "amenagement-urbain": [
        "Poursuivre l'aménagement de l'écoquartier Flaubert avec logements, espaces verts et équipements publics.",
        "Développer le transport fluvial de marchandises et valoriser les bords de Seine.",
    ],
    "quartiers-prioritaires": [
        "Expérimenter le dispositif « Territoires zéro chômeur de longue durée » dans les quartiers prioritaires de Rouen.",
        "Renforcer les services publics de proximité dans les quartiers populaires.",
    ],

    # === SOLIDARITÉ ===
    "aide-sociale": [
        "Mettre en place un bouclier social pour les familles monoparentales avec aide financière à la garde d'enfants, accès prioritaire au logement et aux crèches.",
    ],
    "pouvoir-achat": [
        "Instaurer la gratuité des transports pour les moins de 25 ans et plus de 65 ans pour réduire les dépenses des familles.",
        "Créer une mutuelle communale à tarif accessible pour les habitants sans couverture complémentaire.",
    ],
    "egalite-discriminations": [
        "Mener une politique féministe et inclusive, et lutter contre toutes les formes de discriminations.",
    ],
}

def main():
    print("=" * 60)
    print(f"  RÉ-EXTRACTION {CANDIDAT_ID.upper()} (Rouen)")
    print("=" * 60)
    total = sum(len(v) for v in MESURES.values())
    print(f"\n  {total} mesures dans {len(MESURES)} sous-thèmes")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in MESURES and len(MESURES[st_id]) > 0:
                prop = st["propositions"].get(CANDIDAT_ID)
                if prop is None:
                    prop = {}
                    st["propositions"][CANDIDAT_ID] = prop
                old_count = len(prop.get("mesures", []))
                new_mesures = MESURES[st_id]
                if len(new_mesures) >= old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = SOURCE
                    prop["sourceUrl"] = SOURCE_URL
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} -> {len(new_mesures)}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n    {updated} sous-thèmes mis à jour")
    print("=" * 60)

if __name__ == "__main__":
    main()
