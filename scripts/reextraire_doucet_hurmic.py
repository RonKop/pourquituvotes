#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction Doucet (Lyon) et Hurmic (Bordeaux) depuis leurs sites de campagne.
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SOURCE_DOUCET = "Programme officiel 2026 — Grégory Doucet"
SOURCE_URL_DOUCET = "https://www.pourvivrelyonmunicipales2026.fr/"
SOURCE_HURMIC = "Programme officiel 2026 — Pierre Hurmic"
SOURCE_URL_HURMIC = "https://pierrehurmic2026.fr/"

# ═══════════════════════════════════════════════════════════════
# DOUCET (Lyon) — extrait du site pourvivrelyonmunicipales2026.fr
# ═══════════════════════════════════════════════════════════════

DOUCET_MESURES = {
    "police-municipale": [
        "Augmenter les effectifs de police municipale à 400 policiers, soit +30% par rapport à 2024.",
        "Créer une deuxième brigade cycliste pour couvrir davantage de secteurs.",
        "Établir des postes de police municipale mobiles dans l'espace public.",
        "Former les policiers municipaux aux missions de dialogue et prévention.",
        "Créer une brigade anti-incivilités de 50 agents dédiés.",
        "Développer une brigade d'agents de sécurité et médiateurs pour les résidences sociales.",
    ],
    "videoprotection": [
        "Adapter le parc de caméras de vidéosurveillance selon les besoins de chaque quartier.",
        "Fusionner le centre de gestion de crise et le poste radio de la police municipale.",
    ],
    "prevention-mediation": [
        "Doubler le nombre de médiateurs sociaux dans toute la ville.",
        "Améliorer l'éclairage public dans les zones identifiées comme sensibles.",
        "Généraliser les diagnostics nocturnes pour identifier les zones à améliorer.",
        "Mettre en place un plan de prévention contre l'entrée des jeunes dans le narcotrafic.",
        "Créer un dispositif innovant pour repérer, extraire et protéger les jeunes exposés au trafic.",
        "Orienter systématiquement les usagers interpellés vers l'accompagnement sanitaire et social.",
    ],
    "violences-femmes": [
        "Créer des places d'accueil pour femmes victimes de violences et jeunes LGBTQ+.",
        "Étendre le dispositif Angela (lieux refuges) dans l'ensemble de la ville.",
        "Subventionner les initiatives de prévention en milieu festif.",
        "Créer un fonds municipal pour les victimes de violences conjugales.",
        "Poursuivre l'arrêt à la demande sur le réseau TCL pour la sécurité nocturne.",
    ],
    "transports-en-commun": [
        "Ouvrir le métro 24h/24 les week-ends.",
        "Créer le tramway ouest lyonnais reliant le plateau du 5e à la Presqu'île d'ici 2032.",
        "Créer le tramway T9 Charpennes — Vaulx-en-Velin.",
        "Créer le tramway T10 reliant le 7e arrondissement à Vénissieux et Saint-Fons.",
        "Augmenter la fréquence du métro C et du tramway T3.",
        "Doubler les rames des métros B et D pour augmenter la capacité.",
        "Climatiser les rames de métro et tramway.",
        "Rénover les ascenseurs et escalators du réseau TCL.",
        "Étendre la gratuité TCL aux moins de 18 ans avec un parent abonné.",
    ],
    "velo-mobilites-douces": [
        "Développer les Voies lyonnaises et pistes cyclables sécurisées.",
        "Créer de nouvelles stations Vélo'v dans les quartiers sous-équipés.",
    ],
    "pietons-circulation": [
        "Transformer les places de quartier avec végétation, assises et fontaines.",
        "Créer des itinéraires piétons continus reliant commerces, écoles et services.",
        "Élargir les trottoirs et installer une signalétique piétonne avec bancs.",
        "Créer 60 nouvelles rues aux enfants avec piétonisation et végétalisation.",
        "Sécuriser les abords des écoles, collèges et aires de jeux.",
    ],
    "stationnement": [
        "Créer 1 500 places de parking relais aux entrées de ville.",
        "Offrir 10 journées de stationnement gratuit par an aux ménages lyonnais.",
        "Créer un abonnement stationnement pour travailleurs en horaires décalés.",
    ],
    "tarifs-gratuite": [
        "Étendre la gratuité des transports en commun aux moins de 18 ans.",
    ],
    "logement-social": [
        "Doubler les investissements pour atteindre 1 500 logements sociaux par an jusqu'en 2040.",
        "Créer des logements étudiants dans les quartiers proches des universités.",
        "Produire des logements très sociaux pour les personnes les plus précaires.",
        "Transformer les bureaux vacants en logements sociaux.",
    ],
    "logements-vacants": [
        "Remettre les logements vacants sur le marché via un service de gestion locative clé en main.",
        "Créer une prime petits travaux pour transformer les grandes pièces en chambres étudiantes.",
    ],
    "encadrement-loyers": [
        "Encadrer les locations touristiques type Airbnb et renforcer les contrôles.",
        "Offrir un soutien juridique aux locataires sur l'encadrement des loyers.",
    ],
    "acces-logement": [
        "Développer le bail réel solidaire pour l'accession abordable à la propriété.",
        "Mettre en place une garantie municipale des loyers pour sécuriser les propriétaires.",
        "Créer une assurance habitation municipale à prix réduit.",
        "Augmenter le budget d'hébergement d'urgence de 40%.",
        "Créer une délégation dédiée à la lutte contre le sans-abrisme infantile.",
    ],
    "espaces-verts": [
        "Créer 6 nouveaux parcs d'ici 2032 dans les quartiers déficitaires en espaces verts.",
        "Développer des squares et jardins de proximité dans les secteurs carencés.",
        "Augmenter la végétalisation des espaces privés avec les bailleurs sociaux et copropriétés.",
        "Distribuer des arbres aux habitants et accompagner la végétalisation des cours collectives.",
        "Renforcer les continuités écologiques entre espaces favorables à la biodiversité.",
        "Installer nichoirs et plantations diversifiées dans les espaces verts.",
    ],
    "climat-adaptation": [
        "Créer un fonds municipal d'adaptation des logements à la chaleur.",
        "Transformer le zoo de la Tête d'Or en centre d'accueil pour animaux en danger.",
        "Créer des aires d'ébat canines et parcours d'agility.",
        "Poursuivre les campagnes de stérilisation des chats errants.",
    ],
    "renovation-energetique": [
        "Poursuivre le programme de rénovation énergétique Eco-rénov.",
        "Créer une aide financière pour l'adaptation des logements au handicap et à la perte d'autonomie.",
    ],
    "alimentation-durable": [
        "Ouvrir 10 cantines de quartier avec épicerie sociale, cuisine partagée et restauration sociale.",
        "Poursuivre les expérimentations de sécurité sociale de l'alimentation.",
        "Créer une ferme municipale à Cibeins pour approvisionner la restauration collective.",
        "Améliorer la qualité de la restauration collective avec davantage de bio et de local.",
        "Distribuer des paniers bio gratuits aux femmes enceintes et des réductions AMAP aux jeunes parents.",
    ],
    "centres-sante": [
        "Ouvrir au moins une maison de santé par arrondissement avec médecins et praticiens sans dépassement d'honoraires.",
        "Créer une mutuelle de santé municipale accessible à tous à prix réduit.",
        "Renforcer les liens entre médecine scolaire et médecine de ville.",
    ],
    "prevention-sante": [
        "Développer le sport sur ordonnance via une maison du sport-santé pour les malades chroniques.",
        "Mettre en œuvre une action contre le moustique tigre : information, prévention et moustiquaires.",
        "Renforcer la lutte contre les punaises de lit via dépistage et prêt de matériel.",
        "Développer des accueils de jour et séjours aidant-aidé pour soutenir les aidants.",
    ],
    "seniors": [
        "Établir des visites à domicile pour les personnes âgées isolées.",
        "Organiser des repas partagés le dimanche par quartier pour rompre l'isolement.",
        "Proposer des formations aux premiers secours en santé mentale.",
    ],
    "budget-participatif": [
        "Créer un conseil citoyen du Rhône et de la Saône pour gérer les enjeux collectifs des fleuves.",
    ],
    "transparence": [
        "Définir une charte des droits du Rhône et de la Saône pour la protection des cours d'eau.",
    ],
    "vie-associative": [
        "Renforcer le soutien aux clubs et associations sportives.",
    ],
    "services-publics": [
        "Renforcer les mairies d'arrondissement comme points d'accès aux démarches administratives.",
        "Proposer des permanences juridiques et sociales régulières dans chaque arrondissement.",
        "Créer une application collaborative pour l'accessibilité PMR des transports et équipements.",
    ],
    "commerce-local": [
        "Soutenir les commerces de proximité et les unions commerciales dans tous les quartiers.",
    ],
    "attractivite": [
        "Renforcer la participation de Lyon aux réseaux de villes pour le transfert de connaissances sur la transition écologique.",
        "Développer des jumelages et initiatives de coopération internationale.",
    ],
    "equipements-culturels": [
        "Reconstruire la médiathèque Champollion avec 4 000 m² supplémentaires.",
        "Créer un club gaming et un studio d'enregistrement dans la bibliothèque.",
        "Créer des salles de répétitions pour les pratiques amateures.",
        "Mettre en place un parcours d'éducation aux médias et à l'IA pour les primaires.",
        "Créer l'Atelier Lumière dédié au cinéma et à l'image.",
        "Ouvrir trois nouvelles bibliothèques : Confluence, Guillotière et Moulin à Vent-Grand Trou.",
        "Instaurer le prix libre dans les musées municipaux tous les mercredis.",
        "Rénover le musée Guimet pour en faire un haut lieu culturel.",
        "Créer un centre d'interprétation du patrimoine UNESCO.",
        "Réaliser des travaux d'embellissement à la Halle Tony Garnier.",
        "Permettre ponctuellement la traversée de l'Hôtel de Ville et l'ouverture des salons.",
        "Accompagner le développement de l'Institut Lumière.",
        "Créer un bureau d'aide au tournage pour les productions cinématographiques.",
    ],
    "evenements-creation": [
        "Réinventer la Fête des Lumières en fête populaire, créative et partout dans la ville.",
        "Renforcer le budget dédié à la Fête des Lumières avec carte blanche à un artiste.",
        "Multiplier les expositions et spectacles gratuits dans l'espace public.",
        "Développer des open airs musicaux dans tous les quartiers.",
        "Mettre à disposition des lieux pour les ateliers d'artistes.",
        "Renforcer l'hospitalité d'artistes en exil ou menacés.",
        "Opération « 1 bébé 1 livre » : offrir un livre à tous les petits Lyonnais.",
    ],
    "equipements-sportifs": [
        "Lancer un grand plan baignade avec deux baignades naturelles en Saône et au Rhône.",
        "Ouvrir la nouvelle piscine Kennedy dans le 8e arrondissement.",
        "Rénover les piscines CNTB, Charial, Saint-Exupéry et Mermoz.",
        "Construire de nouveaux équipements sportifs à Confluence, Kennedy, Montchat, Girondins et Mermoz.",
        "Développer un réseau d'espaces de pratique sportive en plein air inclusifs.",
        "Créer des city stades et skateparks dans les quartiers.",
    ],
    "sport-pour-tous": [
        "Généraliser l'apprentissage de la natation à l'école pour 100% de certification.",
        "Créer un pass'sport municipal avec réduction immédiate à l'inscription en club.",
        "Lancer des parcours sport municipaux pour découvrir plusieurs disciplines.",
        "Soutenir le développement du para-sport avec dotations accrues.",
        "Organiser les premiers Jeux Lyonnais, grand rendez-vous sportif amateur bisannuel.",
    ],
    "amenagement-urbain": [
        "Développer des circuits patrimoniaux dans chaque quartier de Lyon.",
        "Intégrer le patrimoine du XXe siècle dans la valorisation urbaine.",
        "Installer des panneaux historiques dans l'espace public.",
    ],
    "accessibilite": [
        "Créer une application collaborative pour l'accessibilité PMR des transports et équipements.",
    ],
    "aide-sociale": [
        "Ouvrir une deuxième structure municipale de bains-douches avec consigne à bagages.",
        "Créer un deuxième restaurant social pour les populations vulnérables.",
        "Former le personnel municipal à l'accueil des migrants et traduire les documents administratifs.",
    ],
    "egalite-discriminations": [
        "Mettre en place un plan municipal de lutte contre le racisme, l'antisémitisme et l'islamophobie.",
        "Créer l'espace égalité pour éduquer sur les discriminations et accompagner les victimes.",
        "Établir des Spot'Égalité offrant consultations juridiques gratuites dans chaque arrondissement.",
        "Ajouter du personnel spécialisé dans les commissariats pour les victimes de discriminations.",
        "Poursuivre le renforcement de la budgétisation sensible au genre.",
    ],
    "pouvoir-achat": [
        "Instaurer le prix libre dans les musées municipaux tous les mercredis.",
    ],
}

# ═══════════════════════════════════════════════════════════════
# HURMIC (Bordeaux) — extrait de pierrehurmic2026.fr/notre-programme/
# ═══════════════════════════════════════════════════════════════

HURMIC_MESURES = {
    "police-municipale": [
        "Augmenter les effectifs de policiers municipaux pour renforcer la présence de terrain.",
        "Augmenter les effectifs de médiateurs dans les quartiers sensibles.",
    ],
    "transports-en-commun": [
        "Étudier la gratuité des transports pour les enfants de moins de 10 ans.",
    ],
    "pietons-circulation": [
        "Sécuriser des itinéraires piétons végétalisés dans tous les quartiers.",
    ],
    "logement-social": [
        "Amplifier la production de logements sociaux dans tous les quartiers.",
    ],
    "encadrement-loyers": [
        "Poursuivre l'encadrement des loyers pour protéger les locataires.",
    ],
    "acces-logement": [
        "Développer l'accession sociale à la propriété pour les classes moyennes.",
    ],
    "petite-enfance": [
        "Créer plus de 200 places en crèches sur le mandat.",
        "Développer l'offre d'accueil périscolaire dans tous les quartiers.",
    ],
    "ecoles-renovation": [
        "Poursuivre la rénovation massive des écoles bordelaises.",
        "Améliorer le rafraîchissement estival et le confort hivernal des établissements scolaires.",
    ],
    "espaces-verts": [
        "Créer 7 nouveaux parcs dans les quartiers déficitaires en espaces verts.",
        "Réaménager 6 grandes places arborées pour lutter contre les îlots de chaleur.",
    ],
    "centres-sante": [
        "Développer des structures médicales de proximité dans les quartiers.",
        "Créer un centre municipal de santé aux Aubiers d'ici 2027.",
    ],
    "commerce-local": [
        "Dynamiser et protéger les commerces de proximité.",
        "Créer un Office du commerce pour soutenir l'activité locale.",
        "Expérimenter l'encadrement des loyers commerciaux.",
    ],
    "equipements-culturels": [
        "Garantir la liberté de création et d'expression artistique.",
        "Ouvrir la Bourse du travail aux pratiques artistiques amateurs.",
    ],
    "aide-sociale": [
        "Plan d'action commun avec l'État : zéro enfant sans abri à Bordeaux.",
    ],
    "pouvoir-achat": [
        "Soutenir le pouvoir d'achat via une tarification solidaire des services publics.",
    ],
    "amenagement-urbain": [
        "Créer 30 quartiers de vie pour plus de proximité et de convivialité.",
        "Grand projet urbain autour du lac avec quartier bas carbone.",
    ],
    "attractivite": [
        "Développer un pôle numérique souverain à Bordeaux.",
    ],
}


def update_candidate(data, cid, mesures_dict, source, source_url):
    """Met à jour les propositions d'un candidat avec les nouvelles mesures."""
    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id not in mesures_dict:
                continue
            new_mesures = mesures_dict[st_id]
            if not new_mesures:
                continue

            prop = st["propositions"].get(cid)
            if prop is None:
                prop = {}
                st["propositions"][cid] = prop

            old_count = len(prop.get("mesures", []))
            if len(new_mesures) >= old_count:
                prop["mesures"] = new_mesures
                prop["source"] = source
                prop["sourceUrl"] = source_url
                updated += 1
                if old_count != len(new_mesures):
                    print(f"    {st_id}: {old_count} → {len(new_mesures)}")

    return updated


def main():
    print("=" * 60)
    print("  RÉ-EXTRACTION DOUCET & HURMIC")
    print("=" * 60)

    # --- Doucet (Lyon) ---
    lyon_path = os.path.join(ROOT_DIR, "data", "elections", "lyon-2026.json")
    with open(lyon_path, "r", encoding="utf-8") as f:
        lyon = json.load(f)

    print("\n  DOUCET (Lyon):")
    total_new = sum(len(v) for v in DOUCET_MESURES.values())
    print(f"    {total_new} mesures dans {len(DOUCET_MESURES)} sous-thèmes")
    updated = update_candidate(lyon, "doucet", DOUCET_MESURES, SOURCE_DOUCET, SOURCE_URL_DOUCET)
    print(f"    {updated} sous-thèmes mis à jour")

    with open(lyon_path, "w", encoding="utf-8") as f:
        json.dump(lyon, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # --- Hurmic (Bordeaux) ---
    bordeaux_path = os.path.join(ROOT_DIR, "data", "elections", "bordeaux-2026.json")
    with open(bordeaux_path, "r", encoding="utf-8") as f:
        bordeaux = json.load(f)

    print("\n  HURMIC (Bordeaux):")
    total_new = sum(len(v) for v in HURMIC_MESURES.values())
    print(f"    {total_new} mesures dans {len(HURMIC_MESURES)} sous-thèmes")
    updated = update_candidate(bordeaux, "hurmic", HURMIC_MESURES, SOURCE_HURMIC, SOURCE_URL_HURMIC)
    print(f"    {updated} sous-thèmes mis à jour")

    with open(bordeaux_path, "w", encoding="utf-8") as f:
        json.dump(bordeaux, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
