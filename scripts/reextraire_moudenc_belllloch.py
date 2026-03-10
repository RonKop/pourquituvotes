#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction des mesures de Moudenc (Toulouse) et Bell-Lloch (Vitry-sur-Seine)
depuis les sites de campagne moudenc2026.fr et pbl2026.fr.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# ============================================================
# MOUDENC (Toulouse) — moudenc2026.fr
# ============================================================

SOURCE_MOUDENC = "Programme officiel 2026 — Jean-Luc Moudenc"
SOURCE_URL_MOUDENC = "https://moudenc2026.fr/"

MESURES_MOUDENC = {
    "police-municipale": [
        "Augmentation des effectifs de la police municipale de 165 à 390 agents depuis 2014, soit +136%.",
        "Présence policière 24h/24 dans tous les quartiers de Toulouse.",
        "Déploiement d'unités motorisées spécialisées et de brigades VTT.",
        "Création de brigades de contact avec garantie d'intervention sous 72 heures.",
        "Armement permanent de la police municipale.",
        "Équipement des agents en pistolets à impulsions électriques.",
        "Dotation en lanceurs de balles de défense.",
        "Construction du commissariat central moderne à Basso Cambo.",
        "Recrutement de 115 policiers nationaux supplémentaires via les contrats de sécurité intégrée.",
        "Création de 22 postes de magistrats et assistants juridiques dédiés.",
        "Parcours de jogging sécurisés équipés de vidéoprotection et renforcement de la surveillance dans les parcs.",
    ],
    "videoprotection": [
        "Objectif 1 caméra par rue : déploiement massif de la vidéosurveillance dans toutes les rues de Toulouse.",
        "Passage de 21 caméras en 2014 à 710 caméras fin 2025.",
        "Déploiement de caméras mobiles pour les événements et zones sensibles.",
        "Vidéo-verbalisation des infractions routières.",
        "Utilisation de la vidéoprotection pour la détection de détresse : 500 situations détectées, 144 interventions.",
        "7 238 réquisitions judiciaires en 2025 ayant conduit à 1 038 interpellations.",
    ],
    "prevention-mediation": [
        "Renforcement de la lutte contre le narcotrafic en lien avec les forces de sécurité nationales.",
        "Triplement du budget sécurité : de 16,4 M€ à 42 M€ entre 2014 et 2026.",
    ],
    "violences-femmes": [
        "Lutte renforcée contre les violences sexistes et sexuelles.",
    ],
    "transports-en-commun": [
        "Prolongement du Téléo (téléphérique urbain) vers Malepère.",
        "Maintien du métro comme colonne vertébrale du réseau de transport.",
        "Soutien au projet de LGV pour relier Toulouse plus rapidement au réseau national.",
        "Doublement de la ligne B du métro pour augmenter les capacités.",
        "Création de 2 600 places de parking relais autour des stations de la future ligne C.",
        "Record de fréquentation du réseau de transports en commun atteint.",
        "Budget mobilité le plus élevé de France hors Paris.",
    ],
    "velo-mobilites-douces": [
        "Poursuite du Réseau Express Vélo (REV) : 370 km de pistes cyclables sécurisées sur l'ensemble de la métropole.",
    ],
    "pietons-circulation": [
        "Maintien de la vitesse à 50 km/h sur les grands axes et 90 km/h sur le périphérique.",
    ],
    "stationnement": [
        "Tarif de stationnement résidentiel parmi les plus bas de France : 100 €/an.",
        "Stationnement gratuit pour les véhicules électriques.",
        "Lutte contre le stationnement sauvage dans tous les quartiers.",
    ],
    "logement-social": [
        "Production de 10 147 logements sociaux entre 2014 et 2024.",
        "Obligation de 35% de logement social dans le PLUiH.",
        "25% de logements abordables exigés dans les programmes immobiliers.",
        "Facilitation de 2 658 accessions sociales à la propriété depuis 2014.",
    ],
    "encadrement-loyers": [
        "Refus de l'encadrement des loyers : privilégier la construction massive pour faire baisser les prix par l'offre.",
    ],
    "acces-logement": [
        "Création d'une assurance logement municipale pour les familles.",
    ],
    "espaces-verts": [
        "Ouverture du grand parc de l'île du Ramier et du parc des berges du Touch.",
        "Poursuite de la politique de végétalisation et de création d'espaces verts dans tous les quartiers.",
    ],
    "proprete-dechets": [
        "Plan propreté renforcé : ambassadeurs de la propreté dans chaque quartier (duo de référents par quartier).",
    ],
    "renovation-energetique": [
        "Lancement d'un cadastre solaire en ligne pour planifier les installations photovoltaïques.",
        "Partenariats avec des installateurs certifiés pour garantir les économies d'énergie.",
        "Subventions à la rénovation énergétique : en moyenne 3 776 € par projet.",
        "Subventions à l'achat de véhicules propres : en moyenne 2 960 € par véhicule.",
    ],
    "centres-sante": [
        "Généralisation de la mutuelle communale à tous les Toulousains (économie de 300 € par an et par personne).",
    ],
    "prevention-sante": [
        "Extension de la mutuelle communale à un plus grand nombre de Toulousains.",
        "Programme santé seniors avec accès facilité aux soins.",
    ],
    "seniors": [
        "Repas au restaurant seniors à 3,40 € (tarif gelé depuis 12 ans).",
    ],
    "budget-participatif": [
        "Généralisation des budgets participatifs par quartier : 8 millions d'euros par an.",
    ],
    "transparence": [
        "Questionnaire mensuel aux habitants sur les services publics municipaux et possibilité de retour direct.",
    ],
    "cantines-fournitures": [
        "Gel des tarifs de cantine scolaire et périscolaire depuis 2015.",
    ],
    "emploi-insertion": [
        "Priorité à la création d'emplois : Toulouse comme la ville de l'emploi, de l'innovation et de l'industrie.",
        "Soutien prioritaire à la filière aéronautique et aux entreprises locales.",
    ],
    "attractivite": [
        "Soutien à la LGV pour relier Toulouse plus rapidement, faire de Toulouse la métropole la plus attractive de France.",
        "Développement de l'industrie et de l'innovation comme moteurs économiques.",
    ],
    "equipements-culturels": [
        "Création d'un « Quartier de la culture » à Montaudran avec auditorium de musique classique et salle de concert de variété.",
    ],
    "equipements-sportifs": [
        "Agrandissement du Stadium de Toulouse.",
        "Piscines municipales à 3,40 € l'entrée.",
    ],
    "sport-pour-tous": [
        "Parcours sportifs sécurisés dans les espaces verts, salle de sport urbaine dans les quartiers.",
    ],
    "amenagement-urbain": [
        "Transformation de la gare Toulouse-Matabiau en pôle d'échanges multimodal.",
        "Protection de l'identité architecturale de la Ville Rose.",
    ],
    "pouvoir-achat": [
        "Aucune hausse de la taxe foncière jusqu'en 2032.",
        "Aucune hausse de la CFE (cotisation foncière des entreprises) jusqu'en 2032.",
        "Assurance logement communale pour réduire les dépenses mensuelles des ménages.",
        "Achats groupés communaux pour les produits du quotidien (moustiquaires, etc.).",
    ],
}


# ============================================================
# BELL-LLOCH (Vitry-sur-Seine) — pbl2026.fr
# ============================================================

SOURCE_BELLLLOCH = "Programme officiel 2026 — Pierre Bell-Lloch"
SOURCE_URL_BELLLLOCH = "https://pbl2026.fr/programme.html"

MESURES_BELLLLOCH = {
    "police-municipale": [
        "Renforcement de la présence policière de proximité dans tous les quartiers.",
    ],
    "videoprotection": [
        "Extension de la vidéoprotection et vidéoverbalisation des infractions routières.",
    ],
    "prevention-mediation": [
        "Création d'une équipe de médiateurs de proximité urbaine.",
        "Développement concerté de la vidéoverbalisation automatisée.",
    ],
    "transports-en-commun": [
        "Arrivée de la ligne 15 du métro automatique du Grand Paris Express avec 4 gares sur la commune.",
    ],
    "velo-mobilites-douces": [
        "Développement des pistes cyclables sécurisées dans toute la ville, création de stations de vélos en libre-service.",
    ],
    "logement-social": [
        "Construction de 2 000 logements tout en préservant les zones pavillonnaires, avec priorité au logement social.",
    ],
    "acces-logement": [
        "Délai moyen d'attribution réduit à 4 ans grâce à une commission d'attribution équitable.",
        "Attribution transparente de 500 logements par an.",
    ],
    "cantines-fournitures": [
        "Gratuité des fournitures scolaires pour plusieurs milliers d'élèves, cantines aux tarifs les plus bas d'Île-de-France.",
    ],
    "periscolaire-loisirs": [
        "Étude de la possibilité de rendre gratuite l'heure d'étude scolaire après la classe pour du soutien scolaire.",
        "Organisation de 2 000 séjours en vacances pour les jeunes Vitriots, activités périscolaires renforcées.",
    ],
    "espaces-verts": [
        "Création d'un grand parc en bord de Seine d'au moins 50 000 m² pour réconcilier la ville avec son fleuve.",
        "Transformation écologique des espaces verts du quartier Vilmorin.",
    ],
    "proprete-dechets": [
        "Création d'une déchetterie-ressourcerie pour le recyclage et la réutilisation.",
        "Mobilisation citoyenne pour la propreté des quartiers.",
    ],
    "climat-adaptation": [
        "Plan d'adaptation au changement climatique avec déminéralisation des sols.",
        "Création d'îlots de fraîcheur et plantation d'arbres dans tous les quartiers.",
    ],
    "renovation-energetique": [
        "Ouverture d'un site de géothermie pour chauffer les habitations et faire baisser durablement les factures d'énergie.",
    ],
    "seniors": [
        "Construction d'une nouvelle résidence sénior adaptée aux besoins et au confort des aînés.",
    ],
    "budget-participatif": [
        "Démocratie de proximité avec plus de 30 ateliers citoyens pour construire le projet.",
    ],
    "vie-associative": [
        "Réouverture de la maison sociale du Moulin Vert et ouverture de deux nouvelles salles municipales de quartier.",
    ],
    "services-publics": [
        "Création d'une Maison de la Paix pour la coopération internationale et l'engagement citoyen.",
    ],
    "commerce-local": [
        "Création d'un nouveau marché au quartier Jean Jaurès avec produits en circuit court à prix accessibles.",
    ],
    "emploi-insertion": [
        "Création d'une régie publique de quartier pour l'insertion professionnelle.",
        "Préparation de l'accueil de 1 000 nouveaux emplois dans la ville.",
    ],
    "equipements-culturels": [
        "Construction d'un complexe festif moderne pour les familles, mariages, anniversaires et événements.",
    ],
    "evenements-creation": [
        "Rendre l'accès à la culture totalement gratuit pour tous les jeunes Vitriots de moins de 26 ans.",
    ],
    "amenagement-urbain": [
        "Nouveau cœur de ville : 5 600 m² d'espaces verts, nouveaux commerces, terrasses, logements sociaux rénovés, cinéma modernisé.",
        "Rénovation du parking souterrain du centre-ville.",
        "Projet NPRU Cœur de Ville pour revitaliser le centre.",
    ],
    "egalite-discriminations": [
        "Lutte contre toutes les discriminations (racisme, sexisme, LGBTQIphobies), conseil citoyen et éducation à l'égalité.",
    ],
    "stationnement": [
        "Rénovation du parking souterrain et amélioration de l'offre de stationnement en centre-ville.",
    ],
}


def update_candidate(json_path, candidat_id, mesures_dict, source, source_url):
    """Met à jour les mesures d'un candidat dans le JSON."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in mesures_dict and len(mesures_dict[st_id]) > 0:
                prop = st["propositions"].get(candidat_id)
                if prop is None:
                    prop = {}
                    st["propositions"][candidat_id] = prop

                old_count = len(prop.get("mesures", []))
                new_mesures = mesures_dict[st_id]

                if len(new_mesures) >= old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = source
                    prop["sourceUrl"] = source_url
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} → {len(new_mesures)}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total = sum(len(v) for v in mesures_dict.values())
    print(f"    {updated} sous-thèmes mis à jour")
    return total


def main():
    print("=" * 60)
    print("  RÉ-EXTRACTION MOUDENC & BELL-LLOCH")
    print("=" * 60)

    # MOUDENC
    print("\n  MOUDENC (Toulouse):")
    total_m = sum(len(v) for v in MESURES_MOUDENC.values())
    print(f"    {total_m} mesures dans {len(MESURES_MOUDENC)} sous-thèmes")
    json_path = os.path.join(ROOT_DIR, "data", "elections", "toulouse-2026.json")
    update_candidate(json_path, "moudenc", MESURES_MOUDENC, SOURCE_MOUDENC, SOURCE_URL_MOUDENC)

    # BELL-LLOCH
    print("\n  BELL-LLOCH (Vitry-sur-Seine):")
    total_b = sum(len(v) for v in MESURES_BELLLLOCH.values())
    print(f"    {total_b} mesures dans {len(MESURES_BELLLLOCH)} sous-thèmes")
    json_path = os.path.join(ROOT_DIR, "data", "elections", "vitry-sur-seine-2026.json")
    update_candidate(json_path, "bell-lloch", MESURES_BELLLLOCH, SOURCE_BELLLLOCH, SOURCE_URL_BELLLLOCH)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
