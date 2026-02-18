#!/usr/bin/env python3
"""
Intégration des programmes de Laurence Ruffin et Nadia Belaïd
pour les élections municipales de Grenoble 2026.

Sources :
- Ruffin : https://oui-grenoble.fr/le-programme/ (33 propositions pour 2033, image infographique)
         + https://oui-grenoble.fr/wp-content/uploads/2026/01/OuiGrenoble_LivretSante.pdf
- Belaïd : https://www.grenoblealpescollectif.fr/les-15-mesures-phares-du-gac/ (15 mesures)
"""

import json
import os

JSON_PATH = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\grenoble-2026.json"

# ============================================================
# CANDIDAT 1 : Laurence Ruffin (id: ruffin)
# 33 propositions issues de l'infographie "Nos 33 propositions pour 2033"
# + détails du livret Santé (PDF)
# + données presse déjà dans le JSON
# ============================================================

RUFFIN_SOURCE = "Programme officiel 2026"
RUFFIN_URL = "https://oui-grenoble.fr/le-programme/"
RUFFIN_SANTE_URL = "https://oui-grenoble.fr/wp-content/uploads/2026/01/OuiGrenoble_LivretSante.pdf"

RUFFIN_PROPOSITIONS = {
    # --- SECURITE ---
    "police-municipale": {
        "texte": "Création d'une police municipale de quartier renforcée par 50 agents supplémentaires, axée sur la proximité et la prévention",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "prevention-mediation": {
        "texte": "Déployer des médiateurs et médiatrices sur toute la ville pour plus de prévention. Approche axée sur la médiation de proximité dans tous les quartiers",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "violences-femmes": {
        "texte": "Agents municipaux dédiés à la lutte contre les violences sexistes et sexuelles",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    # videoprotection : pas de proposition -> reste null

    # --- TRANSPORTS ---
    "transports-en-commun": {
        "texte": "Tarification sociale de l'autopartage pour se libérer des coûts et de la contrainte de la voiture individuelle",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "velo-mobilites-douces": {
        "texte": "Faire de Grenoble la capitale du vélo : entretien de toutes les pistes cyclables, tous les quartiers accessibles à vélo",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "tarifs-gratuite": {
        "texte": "Gratuité des transports en commun le week-end pour accéder au centre-ville et à la montagne",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    # pietons-circulation : pas de proposition spécifique -> reste null
    # stationnement : pas de proposition spécifique -> reste null

    # --- LOGEMENT ---
    "logements-vacants": {
        "texte": "Création d'une brigade municipale contre la vacance de logements",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "encadrement-loyers": {
        "texte": "Encadrer les loyers et rendre l'habitat durable pour protéger les locataires",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    # logement-social : pas de proposition spécifique -> reste null
    # acces-logement : pas de proposition spécifique -> reste null

    # --- EDUCATION ---
    "cantines-fournitures": {
        "texte": "Tarif parent solo pour la cantine et le périscolaire",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "periscolaire-loisirs": {
        "texte": "Renforcer le périscolaire contre les trous d'inter-scolaire : activités culturelles, sportives et vivantes. Permettre à tous les enfants grenoblois de partir en vacances (colonies, montagne)",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "jeunesse": {
        "texte": "Expérimenter un revenu de solidarité jeunes",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "ecoles-renovation": {
        "texte": "Accélérer la réhabilitation des écoles et des crèches : rénovation thermique, végétalisation et ombrage des cours, poursuite de « Place(s) aux Enfants »",
        "source": "Livret Santé - Oui Grenoble",
        "sourceUrl": RUFFIN_SANTE_URL
    },
    # petite-enfance : pas de proposition spécifique -> reste null

    # --- ENVIRONNEMENT ---
    "espaces-verts": {
        "texte": "Création d'une forêt urbaine. Ouverture de la baignade dans l'Isère (site Jean Bron, ouverte toute l'année). Un parc à moins de cinq minutes de chez soi. Ville engagée pour le bien-être animal",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "climat-adaptation": {
        "texte": "Développement d'un fonds d'épargne citoyen 100% au service de l'intérêt général pour accompagner la transition écologique. Urbanisme favorable à la santé, lutte contre les îlots de chaleur, espaces de rafraîchissement",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "renovation-energetique": {
        "texte": "Création d'un pôle public de l'énergie à coûts maîtrisés. Lutte contre la précarité énergétique par la rénovation des logements",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "alimentation-durable": {
        "texte": "Création d'une sécurité sociale de l'alimentation et d'un marché convivial en centre-ville. Paniers bio gratuits de saison pour les familles les plus modestes. Épiceries solidaires pour faire ses courses à prix juste",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "proprete-dechets": None,  # pas de proposition spécifique

    # --- SANTE ---
    "centres-sante": {
        "texte": "Un centre de santé dans chaque secteur de la ville. Soutenir les 5 centres de santé associatifs existants. Création d'un 6ème centre pédiatrique à l'Arlequin. Pôle d'accompagnement à l'installation des professionnels de santé",
        "source": "Livret Santé - Oui Grenoble",
        "sourceUrl": RUFFIN_SANTE_URL
    },
    "prevention-sante": {
        "texte": "Points d'écoute et de parole psychologique pour les jeunes et étudiants. Campagnes de prévention drogues/alcool. Objectif « Grenoble ville sans sida ». Développer le sport-santé à tous les âges. Ordonnances vertes pour les femmes enceintes",
        "source": "Livret Santé - Oui Grenoble",
        "sourceUrl": RUFFIN_SANTE_URL
    },
    "seniors": {
        "texte": "Bien vieillir dans la ville et prévenir la perte d'autonomie : actions de prévention auprès des personnes âgées, soutenir les aidants, permettre le droit au répit",
        "source": "Livret Santé - Oui Grenoble",
        "sourceUrl": RUFFIN_SANTE_URL
    },

    # --- DEMOCRATIE ---
    "budget-participatif": {
        "texte": "Des chantiers coopératifs pour améliorer ou construire des aménagements en bas de chez soi. Révolutionner la Fête des Tuiles avec un budget participatif culture",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "transparence": {
        "texte": "Votes ouverts dès 16 ans sur les questions municipales, y compris aux résidents étrangers. Référendums citoyens. Trois priorités budgétaires claires : solidarité/écologie, éducation/culture, participatif/égalité",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "vie-associative": {
        "texte": "Charte d'engagement avec le monde associatif pour renforcer le partenariat ville-associations",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "services-publics": {
        "texte": "Des permanences du quotidien pour accueillir et traiter les demandes des habitants. Des pactes grenoblois pour l'innovation, la solidarité et l'écologie dans l'administration des équipements publics",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },

    # --- ECONOMIE ---
    "commerce-local": {
        "texte": "Grand plan d'animations et de vitalisation des rues centrales pour le commerce de proximité. Halle ouverte et conviviale pour faire de la ville un lieu de rencontres",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "emploi-insertion": {
        "texte": "Développer l'emploi local et donner du sens à l'économie : réparer plutôt que jeter, développer les filières locales, savoir-faire et usage",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    # attractivite : pas de proposition spécifique -> reste null

    # --- CULTURE ---
    "equipements-culturels": {
        "texte": "Création d'un centre des cultures urbaines et de montagne pour rénover les cultures populaires",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "evenements-creation": {
        "texte": "Révolutionner la Fête des Tuiles : budget participatif dédié à la solidarité et à la culture",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },

    # --- SPORT ---
    # equipements-sportifs : pas de proposition spécifique -> reste null
    # sport-pour-tous : pas de proposition spécifique -> reste null

    # --- URBANISME ---
    # amenagement-urbain : pas de proposition spécifique -> reste null
    # accessibilite : pas de proposition spécifique -> reste null
    # quartiers-prioritaires : pas de proposition spécifique -> reste null

    # --- SOLIDARITE ---
    "aide-sociale": {
        "texte": "Permettre à tous les enfants grenoblois de partir en vacances. Paniers bio gratuits pour les familles modestes. Épiceries solidaires pour faire ses courses à prix juste",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    "pouvoir-achat": {
        "texte": "Épiceries solidaires pour faire ses courses à prix juste. Tarification sociale de l'autopartage. Pôle public de l'énergie à coûts maîtrisés",
        "source": RUFFIN_SOURCE,
        "sourceUrl": RUFFIN_URL
    },
    # egalite-discriminations : pas de proposition spécifique -> reste null
}


# ============================================================
# CANDIDAT 2 : Nadia Belaïd (id: belaid)
# 15 mesures phares du Grenoble Alpes Collectif
# Source : https://www.grenoblealpescollectif.fr/les-15-mesures-phares-du-gac/
# ============================================================

BELAID_SOURCE = "Programme officiel 2026 - 15 mesures phares du GAC"
BELAID_URL = "https://www.grenoblealpescollectif.fr/les-15-mesures-phares-du-gac/"

BELAID_PROPOSITIONS = {
    # --- SECURITE ---
    "prevention-mediation": {
        "texte": "Mettre en place une veille sécurité citoyenne et policière, espaces de dialogue par quartier entre habitants, police et professionnels pour identifier les enjeux de sécurité et co-construire des solutions adaptées avec la mairie et la préfecture",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    # police-municipale : pas de proposition spécifique -> reste null
    # videoprotection : pas de proposition spécifique -> reste null
    # violences-femmes : couvert par mesure discriminations -> reste null

    # --- TRANSPORTS ---
    "transports-en-commun": {
        "texte": "Organiser une assemblée citoyenne décisionnaire à l'échelle du SMMAG qui décide des projets structurants de transports (prolongement du tram, gratuité des transports, etc.)",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    # velo-mobilites-douces : pas de proposition spécifique -> reste null
    # tarifs-gratuite : couvert par assemblée citoyenne transports
    # pietons-circulation : pas de proposition spécifique -> reste null
    # stationnement : pas de proposition spécifique -> reste null

    # --- LOGEMENT ---
    "logement-social": {
        "texte": "Réguler le marché du logement : appliquer la taxe sur les logements vides et la taxe sur les friches commerciales, réguler les locations touristiques de type Airbnb",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "encadrement-loyers": {
        "texte": "Généraliser l'encadrement des loyers et le permis de louer à toute la ville",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "logements-vacants": {
        "texte": "Appliquer la taxe sur les logements vides pour lutter contre la vacance de logements",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    # acces-logement : pas de proposition spécifique -> reste null

    # --- EDUCATION ---
    "cantines-fournitures": {
        "texte": "Expérimenter des petits déjeuners gratuits dans les écoles REP",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "petite-enfance": {
        "texte": "Renforcer le soutien aux familles monoparentales par le CCAS",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    # ecoles-renovation : pas de proposition spécifique -> reste null
    # periscolaire-loisirs : pas de proposition spécifique -> reste null
    # jeunesse : pas de proposition spécifique -> reste null

    # --- ENVIRONNEMENT ---
    "espaces-verts": {
        "texte": "Renforcer la végétalisation de l'espace public et la désimperméabilisation des sols",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "climat-adaptation": {
        "texte": "Aménager une zone de baignade sécurisée dans l'Isère. Renforcer la végétalisation et la désimperméabilisation pour s'adapter aux conséquences du changement climatique et lutter contre les vagues de chaleur",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "renovation-energetique": {
        "texte": "Lancer un programme massif de rénovation énergétique des bâtiments publics et du parc social",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "alimentation-durable": {
        "texte": "Alimentation de qualité pour tous : expérimenter des petits déjeuners gratuits dans les écoles REP",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    # proprete-dechets : pas de proposition spécifique -> reste null

    # --- SANTE ---
    "centres-sante": {
        "texte": "Soutenir financièrement les projets d'habitants de centres de santé autogérés et maisons de santé. Mettre en place un tiers lieu en santé comme lieu ressource et de formation pour les soignants, les patients et les aidants",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    # prevention-sante : pas de proposition spécifique -> reste null
    # seniors : pas de proposition spécifique -> reste null

    # --- DEMOCRATIE ---
    "budget-participatif": {
        "texte": "Budget 100% citoyen : 350 citoyens tirés au sort, des agents et élus décident des projets structurants pour le mandat avec une validation par référendum",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "transparence": {
        "texte": "Charte publique des élus (engagement de transparence, responsabilité, respect des décisions prises par les habitants) et fonctionnement interne de la mairie plus démocratique. Partage du pouvoir avec les habitants",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "vie-associative": {
        "texte": "Redonner aux associations leur place dans la vie des quartiers en arrêtant la municipalisation des structures de jeunesse, culturelles ou citoyennes. Rendre les habitants et les associations co-gestionnaires des Maisons des Habitants",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "services-publics": {
        "texte": "Création de binômes de co-maires de quartier chargés d'organiser la démocratie locale",
        "source": "Place Gre'net, décembre 2025",
        "sourceUrl": "https://www.placegrenet.fr/2025/12/11/municipales-de-grenoble-nadia-belaid-et-thomas-simon-binome-tete-de-liste-du-grenoble-alpes-collectif/666845"
    },

    # --- ECONOMIE ---
    "commerce-local": {
        "texte": "Mettre en place un bureau des commerces comme espace d'échange entre commerçants, avec des interlocuteurs dédiés de la Ville pour soutenir l'installation et la vie des commerces",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "emploi-insertion": {
        "texte": "Mettre en place un Territoire Zéro Chômeurs de Longue Durée (TZCLD) à Grenoble",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    # attractivite : pas de proposition spécifique -> reste null

    # --- CULTURE ---
    "equipements-culturels": {
        "texte": "Créer les conditions d'une culture non pas administrée mais organisée par les acteurs et les habitants dans leur diversité, dans le respect des droits culturels",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    # evenements-creation : pas de proposition spécifique -> reste null

    # --- SPORT ---
    # equipements-sportifs : pas de proposition spécifique -> reste null
    # sport-pour-tous : pas de proposition spécifique -> reste null

    # --- URBANISME ---
    # amenagement-urbain : pas de proposition spécifique -> reste null
    # accessibilite : pas de proposition spécifique -> reste null
    # quartiers-prioritaires : pas de proposition spécifique -> reste null

    # --- SOLIDARITE ---
    "aide-sociale": {
        "texte": "Ouvrir une maison de l'Hospitalité à Grenoble, lieu d'accueil inconditionnel où accéder aux services essentiels (douches, repos, numérique, etc.), des informations et de l'accompagnement",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    "egalite-discriminations": {
        "texte": "Soutenir fortement les structures antiracistes et de prévention des risques (violences sexistes et sexuelles, drogues, addictions). Appliquer un plan de formation des agents aux oppressions systémiques. Parité sociale au sein des élus",
        "source": BELAID_SOURCE,
        "sourceUrl": BELAID_URL
    },
    # pouvoir-achat : pas de proposition spécifique -> reste null
}


def integrer_candidat(data, candidat_id, propositions, programme_complet):
    """Intègre les propositions d'un candidat dans le JSON."""
    # Mettre à jour programmeComplet
    for c in data["candidats"]:
        if c["id"] == candidat_id:
            c["programmeComplet"] = programme_complet
            print(f"  -> programmeComplet = {programme_complet}")
            break

    count_updated = 0
    count_new = 0
    count_skipped = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in propositions:
                prop = propositions[st_id]
                old_val = st["propositions"].get(candidat_id)

                if prop is None:
                    # Explicitement null, on ne touche pas
                    count_skipped += 1
                    continue

                if old_val is None:
                    count_new += 1
                    action = "NEW"
                else:
                    count_updated += 1
                    action = "UPD"

                st["propositions"][candidat_id] = prop
                print(f"  [{action}] {cat['id']}/{st_id}")

    print(f"  Total: {count_new} nouvelles, {count_updated} mises à jour, {count_skipped} ignorées (null)")
    return data


def main():
    # Lire le JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Fichier chargé: {JSON_PATH}")
    print(f"Ville: {data['ville']}, {len(data['candidats'])} candidats")
    print()

    # === CANDIDAT 1 : Ruffin ===
    print("=" * 60)
    print("CANDIDAT 1 : Laurence Ruffin (id: ruffin)")
    print(f"  33 propositions programme complet")
    print("=" * 60)
    data = integrer_candidat(data, "ruffin", RUFFIN_PROPOSITIONS, programme_complet=True)
    print()

    # === CANDIDAT 2 : Belaïd ===
    print("=" * 60)
    print("CANDIDAT 2 : Nadia Belaïd (id: belaid)")
    print(f"  15 mesures phares du GAC")
    print("=" * 60)
    data = integrer_candidat(data, "belaid", BELAID_PROPOSITIONS, programme_complet=True)
    print()

    # Écrire le JSON
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Fichier écrit: {JSON_PATH}")

    # Compter les propositions par candidat
    for cid in ["ruffin", "belaid"]:
        count = 0
        for cat in data["categories"]:
            for st in cat["sousThemes"]:
                if st["propositions"].get(cid) is not None:
                    count += 1
        print(f"  {cid}: {count} propositions non-null")


if __name__ == "__main__":
    main()
