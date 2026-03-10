#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ré-extraction des mesures de François Piquemal (Toulouse 2026)
Source : piquemal2026.fr + articles de presse (Mediacités, Le Journal Toulousain, etc.)
"""
import io, json, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "toulouse-2026.json")
SOURCE = "Programme officiel 2026 — François Piquemal"
SOURCE_URL = "https://piquemal2026.fr/le-programme/"
CANDIDAT_ID = "piquemal"

MESURES = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Recrutement de 100 policiers municipaux supplémentaires pour une police de proximité présente dans tous les quartiers.",
        "Déploiement de 4 agents de police municipale par quartier dans chacun des 84 quartiers de Toulouse.",
        "Création d'une antenne de police municipale dans chaque secteur.",
        "Police visible, à l'écoute et formée à la médiation plutôt qu'à la répression.",
    ],
    "videoprotection": [
        "Audit complet des 675 caméras de vidéosurveillance existantes sur la voie publique.",
        "Réorientation des 16 millions d'euros du marché des caméras vers le recrutement de 34 agents de police municipale supplémentaires.",
    ],
    "prevention-mediation": [
        "Rétablissement de l'Office municipal de médiation supprimé sous le mandat actuel.",
        "Priorité à la prévention, à la médiation et au renforcement du lien social plutôt qu'aux dispositifs technologiques et répressifs.",
    ],

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Création d'un RER métropolitain cadencé toutes les 15 minutes de 5h à minuit, avec trains compatibles vélos et synchronisation bus-train.",
        "Augmentation de 20 % des kilomètres commerciaux du réseau bus en trois ans.",
        "Création de nouvelles lignes Linéo avec voies dédiées et priorité aux feux.",
        "Étude du doublement des rames de la ligne B du métro.",
        "Réseau de bus renforcé dans les quartiers périphériques : plus d'arrêts, de fréquence et d'amplitude horaire.",
    ],
    "velo-mobilites-douces": [
        "Développement de 300 à 400 kilomètres de pistes cyclables sur la métropole.",
        "Développement massif de la marche et du vélo via les coopératives de quartier identifiant les zones à piétonniser.",
    ],
    "tarifs-gratuite": [
        "Gratuité de l'abonnement Tisséo pour les moins de 26 ans d'ici 2030, avec première réduction mensuelle dès septembre 2026.",
        "Retour de l'eau en régie publique à l'échéance de la DSP avec Véolia en 2030, avec tarification sociale : premiers 10 m³ gratuits et tarification progressive.",
    ],
    "stationnement": [
        "Création d'une régie publique de stationnement pour mettre fin au monopole de l'usage automobile.",
    ],

    # ── LOGEMENT ──
    "logement-social": [
        "Gel pluriannuel des loyers de Toulouse Métropole Habitat.",
        "Fin des démolitions d'immeubles HLM sans accord préalable des résidents.",
        "Transformation du « quota du maire » pour l'attribution des HLM en « quota du conseil municipal » avec critères transparents.",
    ],
    "logements-vacants": [
        "Limitation des locations Airbnb à 90 jours par an.",
        "Renforcement du permis de louer et généralisation à l'ensemble de la ville.",
    ],
    "encadrement-loyers": [
        "Mise en place de l'encadrement des loyers à Toulouse pour stopper la spéculation immobilière.",
    ],
    "acces-logement": [
        "Priorité à la rénovation thermique et acoustique des bâtiments existants plutôt qu'à la construction neuve.",
        "Exercice du droit de préemption municipal pour l'acquisition de biens immobiliers mis en vente.",
    ],

    # ── ÉDUCATION ──
    "petite-enfance": [
        "Augmentation des places en crèche municipale et associative dans les secteurs sous-équipés.",
        "Réouverture de la crèche Sainte-Lucie et création de crèches aux horaires décalés adaptés aux réalités sociales locales.",
        "Renforcement du soutien aux crèches associatives et parentales.",
    ],
    "ecoles-renovation": [
        "Audit complet des écoles (amiante, isolation thermique) avec tous les acteurs scolaires.",
        "Plan pluriannuel de rénovation massive des écoles avec calendrier transparent et public.",
    ],
    "cantines-fournitures": [
        "Gratuité progressive des cantines scolaires et des fournitures.",
        "100 % de produits issus de l'agriculture biologique et locale dans les cantines.",
        "Cuisine centrale (35 000 repas/jour) servant une large part de repas végétariens d'ici la fin du mandat.",
    ],
    "periscolaire-loisirs": [
        "Extension des horaires des CLAE pour les familles monoparentales.",
        "Création de jardins potagers scolaires avec compostage systématique des déchets verts.",
    ],
    "jeunesse": [
        "Création d'une carte municipale « famille monoparentale » facilitant l'accès aux services, aides et activités municipales à tarifs adaptés.",
        "Extension de la mutuelle municipale aux familles monoparentales à tarifs préférentiels.",
    ],

    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Transformation de l'hippodrome de la Cépière en « Grand Parc Rive Gauche » de 34 hectares avec piscine, équipements sportifs et végétation, ouverture progressive dès 2028.",
        "50 hectares de renaturalisation et désimperméabilisation des sols dans la ville.",
        "Plan massif de végétalisation des sols, voiries et bâtiments avec des espèces adaptées au changement climatique.",
        "Moratoire sur l'abattage des arbres, considérés comme un patrimoine précieux à protéger.",
    ],
    "proprete-dechets": [
        "Changement de paradigme en matière de déchets inspiré des propositions de l'association Zéro Waste.",
        "Service de propreté uniforme sur tout le territoire, y compris les quartiers populaires.",
    ],
    "climat-adaptation": [
        "Réduction de 55 % des émissions de gaz à effet de serre de la métropole d'ici 2030.",
        "Opposition aux grands projets d'écocide : autoroute A69, Jonction Est, tour Occitanie.",
        "Audits énergétiques quartier par quartier pour planifier la transition écologique.",
    ],
    "renovation-energetique": [
        "Plan de 300 millions d'euros sur 12 ans pour la rénovation énergétique des bâtiments publics et privés.",
        "Élimination des passoires thermiques (logements classés F et G) sur la durée du plan.",
    ],
    "alimentation-durable": [
        "100 % de produits issus de l'agriculture biologique et locale dans les cantines scolaires.",
        "Valorisation des agents techniques scolaires : missions élargies au compostage, à la transformation alimentaire sur place et à la réduction des déchets.",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Création de centres de santé municipaux avec professionnels salariés dans les quartiers en désert médical.",
        "Déploiement de bus santé mobiles pour aller vers les habitants des quartiers mal desservis.",
    ],
    "prevention-sante": [
        "Extension des soins de santé par des approches innovantes pour lutter contre les déserts médicaux.",
    ],
    "seniors": [
        "Lutte contre l'isolement des personnes âgées par des programmes de quartier.",
    ],

    # ── DÉMOCRATIE ──
    "budget-participatif": [
        "Création de 60 coopératives de quartier ouvertes à toute personne de plus de 16 ans vivant, étudiant ou travaillant dans le secteur.",
        "Budget de fonctionnement annuel de 500 000 à 1 million d'euros par coopérative de quartier.",
        "Pouvoir de décision des coopératives sur l'urbanisme, le logement, la mobilité, la sécurité et les équipements publics.",
    ],
    "transparence": [
        "Instauration de la parité sociale dans la gouvernance municipale (24 % d'ouvriers et employés sur la liste contre 3 % au conseil actuel).",
        "Mise en place du Référendum d'Initiative Citoyenne (RIC) local.",
    ],
    "services-publics": [
        "Retour de l'eau en régie publique à l'expiration de la DSP avec Véolia en 2030.",
        "Tarification sociale de l'eau : premiers 10 m³ gratuits correspondant au minimum vital, puis tarification progressive.",
    ],

    # ── ÉCONOMIE ──
    "commerce-local": [
        "Facilitation de l'accès des producteurs locaux aux marchés publics municipaux.",
    ],
    "emploi-insertion": [
        "Expérimentation du dispositif « Territoire Zéro Chômeur de Longue Durée » : embauche en CDI de personnes sans emploi depuis plus d'un an pour des activités d'utilité sociale.",
        "Création d'un fonds municipal d'appui à l'économie sociale et solidaire (ESS).",
        "Faire de Toulouse la capitale française de l'économie sociale et solidaire.",
    ],
    "attractivite": [
        "Construction d'une économie plus résiliente, inclusive et durable centrée sur l'ESS.",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Restauration et pérennisation des subventions aux associations culturelles (réduites de 20 à 40 % sous le mandat actuel) avec conventions pluriannuelles.",
        "Cours gratuits dans les équipements et espaces publics municipaux.",
    ],
    "evenements-creation": [
        "Plan « Un festival dans mon quartier » : création de 15 festivals dans 15 quartiers sur des thématiques variées (musique, rap, manga, street-art, cirque, danse, théâtre, stand-up, astronomie, écologie, cinéma, littérature).",
    ],

    # ── SPORT ──
    "equipements-sportifs": [
        "Construction d'une piscine et d'équipements sportifs dans le futur Grand Parc Rive Gauche.",
    ],
    "sport-pour-tous": [
        "Cours de sport gratuits dans les équipements publics avec créneaux réservés aux femmes.",
        "Places réservées et tarifs modulés selon les revenus dans les activités sportives municipales.",
    ],

    # ── URBANISME ──
    "amenagement-urbain": [
        "50 hectares de renaturalisation, désimperméabilisation des sols, micro-places plantées dans les quartiers denses.",
        "Plans de mobilité de quartier élaborés par les coopératives : délibérations sur les itinéraires, phases de test, horaires et « coupures urbaines » à traiter en priorité.",
    ],
    "quartiers-prioritaires": [
        "Lutte contre la gentrification : les résidents actuels des quartiers populaires doivent bénéficier en premier des améliorations urbaines.",
        "Réseau de bus prioritairement renforcé dans les quartiers périphériques et populaires.",
    ],

    # ── SOLIDARITÉ ──
    "aide-sociale": [
        "Carte municipale « famille monoparentale » donnant accès à des tarifs préférentiels sur les services municipaux.",
        "Mutuelle municipale ouverte aux familles monoparentales à tarifs préférentiels.",
    ],
    "egalite-discriminations": [
        "Test de parité sociale appliqué à la composition de la liste et aux instances de gouvernance.",
    ],
    "pouvoir-achat": [
        "Encadrement des loyers pour restaurer le pouvoir d'achat des 66 % de Toulousains locataires.",
        "Tarification sociale de l'eau avec premiers 10 m³ gratuits, économie estimée à 45 euros par an pour une famille de 4 personnes.",
    ],
}

def main():
    print("=" * 60)
    print(f"  RÉ-EXTRACTION {CANDIDAT_ID.upper()} (Toulouse)")
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
