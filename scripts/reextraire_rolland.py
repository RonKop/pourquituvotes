#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction des propositions de Johanna Rolland (Nantes, municipales 2026).
Sources :
  - France Bleu Loire Océan (programme 2 février 2026)
  - Infos Média Nantes (entretien + programme)
  - Hello Gazette Nantes (mesures économie)
  - La Fibre du Tri (écologie populaire)
  - Vœux 2026 (infos-media-nantes)
  - Site lagaucheuniepournantes.fr
  - metropole.nantes.fr (annonces officielles)
"""
import io, json, os, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "nantes-2026.json")
SOURCE = "Programme officiel 2026 — Johanna Rolland"
SOURCE_URL = "https://lagaucheuniepournantes.fr/notre-projet/"
CANDIDAT_ID = "rolland"

MESURES = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Création d'un commissariat de police dans un quartier prioritaire de la ville.",
        "Présence permanente de la police municipale en soirée près du Bouffay et du Hangar à bananes.",
        "Maintien de 235 policiers municipaux avec coordination renforcée avec les services de l'État.",
    ],
    "prevention-mediation": [
        "Renforcement de la coordination entre police municipale et police nationale pour accroître la présence sur le terrain.",
        "Lutte renforcée contre le narcotrafic en coordination avec l'État.",
    ],
    "violences-femmes": [
        "Création d'un lieu dédié aux mineurs victimes de violences sexuelles et sexistes.",
        "Ouverture d'une structure Fercam dédiée aux jeunes filles victimes de violences sexuelles et sexistes sur l'île de Nantes dès 2026.",
    ],
    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Déploiement de deux nouvelles lignes de tramway (lignes 6 et 7), mise en service fin 2027.",
        "Création d'une ligne 8 de busway pour desservir le sud de l'agglomération.",
    ],
    "velo-mobilites-douces": [
        "Ajout de 150 km de pistes cyclables supplémentaires sur le réseau nantais.",
        "Création d'une piste cyclable reliant la gare à Bottière pour sécuriser les trajets à vélo.",
        "Livraison de 50 km de véloroutes (grands axes de circulation vélo) en 2026.",
    ],
    "stationnement": [
        "Mise en place d'un stationnement à tarif réduit pour les travailleurs en horaires décalés.",
    ],
    "tarifs-gratuite": [
        "Extension de la gratuité des transports en commun à 15 000 usagers supplémentaires à revenus modestes (30 000 bénéficiaires actuels).",
    ],
    # ── LOGEMENT ──
    "logement-social": [
        "Augmenter à 60 % la part de logements neufs régulés : 40 % de logements sociaux et 20 % de logements à prix maîtrisés.",
    ],
    "acces-logement": [
        "Création de plusieurs milliers de logements abordables sur le mandat.",
    ],
    # ── ÉDUCATION ──
    "petite-enfance": [
        "Création de 700 nouvelles places en crèche réparties sur tous les quartiers nantais.",
        "Mise en place d'un service de garde d'urgence pour les parents en situation de crise.",
        "Création d'une plateforme d'accompagnement des familles monoparentales.",
    ],
    "ecoles-renovation": [
        "Ouverture de l'école Joséphine-Baker sur l'île de Nantes : 400 élèves, matériaux biosourcés, cours végétalisées et inclusives.",
        "Modernisation des écoles Urbain-Leverrier et Beaujoire avec cours végétalisées adaptées aux usages scolaires.",
    ],
    "cantines-fournitures": [
        "Objectif de 60 % de produits bio dans les cantines scolaires en fin de mandat.",
    ],
    "jeunesse": [
        "Ouverture en septembre 2026 d'une Maison des enfants dédiée à la santé mentale des 6-11 ans sur l'île de Nantes (380 m², équipe pluridisciplinaire).",
    ],
    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Doublement de l'effort de débitumisation dans l'espace public.",
        "Faire de Nantes une référence européenne de la biodiversité via des corridors écologiques et la renaturation.",
        "Plantation de milliers d'arbres dans les quartiers et les cours d'école.",
        "Création du parc de la Confluence sur l'île de Nantes.",
        "Finalisation de la phase 2 du Jardin extraordinaire avec bassin public accessible.",
    ],
    "proprete-dechets": [
        "Ouverture de la première ressourcerie métropolitaine en septembre 2026 à Rezé.",
        "Poursuite du plan pleine terre : débitumisation du parc de Beaulieu et du cours des Verdiaux.",
    ],
    "climat-adaptation": [
        "Construire sans artificialiser les sols (sobriété foncière).",
        "Végétalisation du jardin de la Duchesse Anne pour créer un nouvel îlot de fraîcheur en centre-ville.",
    ],
    "renovation-energetique": [
        "Diminution du parc de logements énergivores (passoires thermiques) par des subventions municipales à la rénovation.",
    ],
    "alimentation-durable": [
        "Création de marchés bio en faveur des producteurs locaux et développement des circuits courts.",
        "Création de jardins partagés pour transformer les espaces urbains.",
        "Programmes de sensibilisation dans les écoles pour promouvoir une alimentation responsable.",
    ],
    # ── SANTÉ ──
    "centres-sante": [
        "Ouverture d'un centre de santé à la Bottière en mars 2026.",
        "Déploiement de centres et maisons de santé dans les quartiers prioritaires avec médiateurs santé.",
        "Installation de professionnels de santé au Clos Toreau avec accompagnement par des médiateurs.",
    ],
    "prevention-sante": [
        "Création d'un observatoire de la pauvreté pour mieux comprendre les réalités sociales et adapter les réponses.",
    ],
    "seniors": [
        "Préserver 100 % des services publics municipaux et sanctuariser les aides sociales du CCAS.",
    ],
    # ── DÉMOCRATIE ──
    "budget-participatif": [
        "Poursuite des budgets participatifs dans les 11 quartiers nantais (principe 50/50, 178 projets soutenus à ce jour).",
    ],
    "services-publics": [
        "Ouverture de la Locomotive et de la Maison des Haubans comme nouvelles maisons de quartier (Erdre et Malakoff).",
        "Ouverture d'équipements associatifs à Saint-Donatien et Nantes Nord, dont le pôle associatif du Coudray.",
        "Maintien du soutien aux associations du secteur culturel.",
    ],
    # ── ÉCONOMIE ──
    "commerce-local": [
        "Création d'une foncière commerciale pour lutter contre la vacance et favoriser la diversité des commerces.",
        "Rénovation du marché de Talensac et développement de marchés atypiques.",
        "Expérimentation de l'encadrement des baux commerciaux avec le législateur.",
    ],
    "emploi-insertion": [
        "Soutien à l'économie sociale et solidaire et création d'une ressourcerie par quartier.",
    ],
    "attractivite": [
        "Faire de Nantes un territoire pilote de l'économie régénérative.",
    ],
    # ── CULTURE ──
    "equipements-culturels": [
        "Poursuite du festival Débord de Loire comme événement culturel majeur du territoire.",
        "Végétalisation du Mail Frida Kahlo sur l'île de Nantes.",
    ],
    "evenements-creation": [
        "Accueil du spectacle « Apesanteur » de Royal de Luxe au parc de la Mouto.",
    ],
    # ── SPORT ──
    "equipements-sportifs": [
        "Création d'un city stade à Saint-Donatien pour renforcer la convivialité du quartier.",
    ],
    # ── URBANISME ──
    "amenagement-urbain": [
        "Création d'une piste cyclable parallèle à la Loire dans le sud de Nantes.",
        "Végétalisation de la place Rosa Parks, du quai des Pins et du parc de la Moutonnerie.",
        "Aménagement d'un cordon boisé à Pin Sec et de jardins familiaux aux Champs de Manœuvre.",
    ],
    "quartiers-prioritaires": [
        "Plan de 10 mesures spécifiques pour les quartiers populaires de Nantes.",
    ],
    # ── SOLIDARITÉ ──
    "aide-sociale": [
        "Plateforme d'accompagnement dédiée aux familles monoparentales : aide quotidienne et garde d'urgence.",
        "Sanctuarisation des aides sociales du CCAS dans le budget municipal.",
    ],
    "egalite-discriminations": [
        "Poursuite de l'Observatoire des discriminations créé en 2024.",
    ],
    "pouvoir-achat": [
        "Agir pour le pouvoir d'achat des classes moyennes et populaires via des mesures ciblées sur les transports et l'alimentation.",
    ],
}


def main():
    print("=" * 60)
    print(f"  RÉ-EXTRACTION {CANDIDAT_ID.upper()} (Nantes)")
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
