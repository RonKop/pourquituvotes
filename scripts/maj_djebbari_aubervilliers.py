#!/usr/bin/env python3
"""
Intégration du programme de Nabila Djebbari (Reconnecter Aubervilliers)
dans aubervilliers-2026.json.

Source : PDF "Nabila Djebbari.pdf" — Programme complet municipales 2026
Site : https://www.reconnecteraubervilliers.org/
"""

import json
import sys
import io
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

JSON_PATH = "data/elections/aubervilliers-2026.json"
CANDIDAT_ID = "djebbari"
SOURCE = "Programme officiel 2026 — Nabila Djebbari"
SOURCE_URL = "https://www.reconnecteraubervilliers.org/"

# ─── Mapping des mesures par sous-thème ───

PROPOSITIONS = {
    # ═══ SÉCURITÉ ═══
    "police-municipale": [
        "Renégocier la convention entre police nationale et police municipale pour clarifier les missions de chacun.",
        "Mettre fin aux transferts de missions qui ne relèvent pas de la police municipale.",
        "Déployer une police municipale de proximité présente dans tous les quartiers, identifiable, à pied et à vélo.",
        "Former les agents de police municipale à la médiation et à la relation avec les habitants.",
        "Renforcer la capacité d'intervention de la police municipale sur les situations du quotidien.",
        "Sécuriser les abords des écoles, des transports, des commerces et des halls d'immeubles en tension.",
        "Exiger une présence effective de la police nationale pour les enquêtes, trafics et délinquance organisée.",
    ],
    "videoprotection": [
        "Entretenir, fiabiliser et évaluer régulièrement le réseau de vidéoprotection dans un cadre respectueux des libertés.",
    ],
    "prevention-mediation": [
        "Renforcer la médiation de rue et les équipes éducatives spécialisées.",
        "Soutenir les associations de terrain engagées dans la prévention.",
        "Développer des dispositifs de prévention précoce pour les jeunes en difficulté.",
        "Porter la création d'un Droit à la Sécurité Opposable (DASO) pour exiger une réponse effective de l'État.",
        "Activer le CLSPD comme organe central de coordination sécuritaire par quartier.",
    ],
    "violences-femmes": [
        "Créer une Maison des Femmes comme lieu d'accueil, d'écoute et d'accompagnement.",
        "Renforcer la lutte contre les violences sexistes et sexuelles avec des dispositifs d'alerte et d'hébergement.",
        "Développer des lieux d'écoute et de protection pour les victimes de violences.",
        "Renforcer la prévention du harcèlement scolaire.",
    ],

    # ═══ TRANSPORTS ═══
    "transports-en-commun": [
        "Créer un transport à la demande municipal gratuit pour les publics fragiles (seniors, personnes handicapées).",
        "Défendre les intérêts d'Aubervilliers dans les grands projets de transport comme la ligne 15.",
    ],
    "velo-mobilites-douces": [
        "Développer des pistes cyclables continues sur le territoire.",
        "Réduire le stationnement automobile sur l'espace public au bénéfice des mobilités douces en créant des parkings publics.",
    ],
    "pietons-circulation": [
        "Développer des zones piétonnes dans la ville.",
        "Apaiser la circulation et sécuriser les mobilités dans tous les quartiers.",
    ],
    "stationnement": [
        "Créer des parkings publics pour libérer l'espace public du stationnement automobile.",
    ],
    "tarifs-gratuite": [
        "Mettre en place la gratuité d'accès au service public pour les plus défavorisés selon le reste à vivre de chaque famille.",
    ],

    # ═══ LOGEMENT ═══
    "logement-social": [
        "Exiger un entretien régulier du parc HLM avec des engagements clairs des bailleurs.",
        "Prioriser la réhabilitation des immeubles les plus dégradés.",
        "Garantir la transparence sur l'attribution des logements sociaux.",
        "Fluidifier les parcours locatifs selon les situations de vie.",
    ],
    "logements-vacants": [
        "Généraliser le permis de louer à toute la ville pour lutter contre l'habitat indigne.",
        "Renforcer les contrôles et recruter des inspecteurs de salubrité.",
        "Sanctionner les propriétaires en infraction et mettre fin aux marchands de sommeil.",
        "Prévenir la dégradation des copropriétés privées et de l'habitat pavillonnaire par un accompagnement en amont.",
    ],
    "encadrement-loyers": [
        "Protéger les ménages de la spéculation immobilière.",
        "Limiter les hausses abusives de loyers commerciaux et lutter contre la spéculation qui chasse les commerces populaires.",
    ],
    "acces-logement": [
        "Développer l'accession sociale notamment par le Bail Réel Solidaire.",
        "Créer des offres de logements intermédiaires pour les ménages modestes et les classes moyennes.",
        "Sécuriser les parcours logement des jeunes, des femmes isolées et des personnes en situation de handicap.",
        "Développer des solutions pour la décohabitation des jeunes (foyer de jeunes travailleurs).",
    ],

    # ═══ ÉDUCATION ═══
    "petite-enfance": [
        "Créer Baby+, un service public de la petite enfance avec une offre variée de modes d'accueil adaptée aux contraintes des familles.",
        "Proposer des activités pour les familles sans place en crèche et des lieux d'éveil dans tous les quartiers.",
        "Prévenir l'exposition excessive aux écrans chez les tout-petits.",
        "Développer une maison des assistantes maternelles.",
        "Proposer des ateliers de soutien à la parentalité et des réseaux de parents.",
        "Renforcer l'accompagnement des enfants en situation de handicap et de leurs aidants dès la petite enfance.",
    ],
    "ecoles-renovation": [
        "Lancer un plan de rénovation des écoles intégrant la transition écologique et les évolutions démographiques.",
        "Transformer les cours d'écoles en espaces verts et ombragés, supprimer progressivement le bitume.",
        "Investir dans le matériel pédagogique et les salles spécialisées.",
        "Mettre en place un système d'entretien réactif et efficace des écoles.",
        "Faire entrer la biodiversité et les jardins potagers pédagogiques à l'école.",
        "Ouvrir à terme certaines cours d'écoles comme mini-parcs de quartier.",
    ],
    "cantines-fournitures": [
        "Améliorer la qualité des repas scolaires : plus de produits frais, de saison, bio et circuits courts.",
        "Instaurer une tarification plus juste de la restauration scolaire avec un quotient familial plus progressif.",
        "Renforcer le contrôle du prestataire : transparence, traçabilité, lutte contre le gaspillage alimentaire.",
        "Associer parents et enfants à l'amélioration des menus via des commissions restauration régulières.",
        "Étudier l'évolution vers une cuisine centrale ou une mutualisation territoriale pour maîtriser qualité et coûts.",
    ],
    "periscolaire-loisirs": [
        "Créer des lieux d'étude après l'école avec des équipes d'accompagnement pédagogique formées.",
        "Mettre en place des espaces numériques accessibles pour le périscolaire.",
        "Garantir l'accès aux activités périscolaires pour toutes les familles.",
        "Développer des partenariats culturels et sportifs accrus dans les écoles.",
    ],
    "jeunesse": [
        "Créer des parcours personnalisés pour les 16-25 ans (emploi, formation, logement, mobilité).",
        "Amplifier le mentorat avec des adultes engagés pour accompagner les jeunes.",
        "Favoriser les stages et emplois d'été locaux pour les jeunes.",
        "Développer l'apprentissage dans l'administration municipale.",
        "Rendre accessibles des formations innovantes (transition écologique, IA, agriculture urbaine).",
        "Développer des Maisons des jeunes comme espaces de projets.",
        "Créer des studios, salles de répétition et espaces artistiques pour les jeunes.",
        "Développer le permis de conduire citoyen pour les 16-25 ans.",
        "Favoriser un écosystème local dédié à l'entrepreneuriat jeune : micro-crédits, incubateurs de proximité.",
    ],

    # ═══ ENVIRONNEMENT ═══
    "espaces-verts": [
        "Stopper l'artificialisation des sols et encadrer strictement les nouvelles constructions.",
        "Ouvrir de nouveaux squares et transformer des friches en jardins publics.",
        "Désimperméabiliser les sols et planter massivement des arbres et des haies.",
        "Créer des îlots de fraîcheur : fontaines, brumisateurs, zones d'ombre.",
        "Imposer la plantation d'un arbre pour chaque nouveau logement construit.",
        "Créer des micro-parcs, caniparcs et petites places ombragées dans chaque quartier.",
        "Végétaliser les pieds d'immeubles et revaloriser les squares existants.",
        "Étudier la création d'une ferme pédagogique municipale.",
        "Soutenir et développer les jardins partagés et jardins ouvriers.",
        "Préserver les usages populaires des parcs : jeux, pique-niques, rencontres de quartier.",
    ],
    "proprete-dechets": [
        "Renforcer les moyens de nettoyage dans les quartiers les plus exposés.",
        "Adapter les fréquences de passage aux réalités de terrain.",
        "Mieux entretenir les trottoirs, pieds d'immeubles, abords des écoles et des commerces.",
        "Appliquer strictement le principe pollueur-payeur et verbaliser les dépôts sauvages.",
        "Coopérer avec les bailleurs pour responsabiliser les locataires sur la gestion des déchets.",
        "Déployer des outils simples de signalement des problèmes de propreté accessibles à tous.",
        "Créer une commission opérationnelle quotidienne Ville / Plaine Commune pour la propreté.",
        "Installer une antenne municipale mobile permanente aux Quatre-Chemins pour la propreté et la présence humaine.",
    ],
    "climat-adaptation": [
        "Déployer un plan canicule / grand froid avec lieux refuges et horaires adaptés.",
        "Cartographier les îlots de chaleur et les traiter en priorité.",
        "Faire de la lutte contre toutes les pollutions une priorité municipale.",
    ],
    "renovation-energetique": [
        "Accélérer la rénovation thermique et acoustique des logements pour réduire les charges.",
        "Accompagner les ménages dans la rénovation énergétique et simplifier l'accès aux aides.",
        "Prioriser les logements les plus énergivores pour la rénovation.",
    ],
    "alimentation-durable": [
        "Développer des jardins potagers pédagogiques dans les écoles et les quartiers.",
        "Promouvoir les circuits courts et les produits bio dans la restauration scolaire.",
    ],

    # ═══ SANTÉ ═══
    "centres-sante": [
        "Renforcer l'accès aux professionnels de santé dans tous les quartiers.",
        "Développer la prévention et la santé mentale avec des actions de proximité.",
    ],
    "prevention-sante": [
        "Développer des actions de prévention et d'écoute en santé mentale.",
        "Soutenir les jeunes et les familles en difficulté psychologique.",
        "Travailler avec les professionnels et associations spécialisées en santé.",
    ],
    "seniors": [
        "Adapter les logements et l'espace public au vieillissement.",
        "Lutter contre l'isolement des seniors en renforçant les séjours municipaux.",
        "Structurer un service municipal du quotidien pour les personnes âgées.",
        "Faire de la santé des seniors une priorité territoriale.",
    ],

    # ═══ DÉMOCRATIE ═══
    "budget-participatif": [
        "Lancer un budget participatif annuel avec une enveloppe dédiée répartie par quartier.",
        "Organiser un vote citoyen en ligne et en présentiel sur les projets proposés par les habitants.",
        "Créer un Observatoire indépendant des engagements citoyens avec tableau de bord public.",
    ],
    "transparence": [
        "Établir un bilan financier public en début de mandat.",
        "Publier des données budgétaires simples et lisibles.",
        "Réaliser une présentation annuelle du budget aux habitants par quartier.",
        "Engager un suivi public des engagements financiers du mandat.",
        "Obliger les adjoint·es à habiter Aubervilliers.",
        "Garantir la présence des élus dans chaque conseil municipal et instance où la ville est représentée.",
    ],
    "vie-associative": [
        "Créer une Maison du Peuple auto-gérée : espace de rencontre, d'organisation et d'éducation populaire.",
        "Organiser des États généraux associant culture, sport, ESS et vie de quartier en fin de première année.",
        "Instaurer une Soirée annuelle des bénévoles et de l'engagement.",
        "Soutenir les initiatives citoyennes pour l'amélioration du cadre de vie.",
    ],
    "services-publics": [
        "Créer une agence municipale de proximité dans chaque quartier (accueil, services, signalement).",
        "Simplifier et unifier les démarches en ligne municipales.",
        "Maintenir systématiquement une alternative humaine aux démarches numériques.",
        "Développer des permanences d'accompagnement au numérique dans les quartiers.",
        "Organiser des Assises du personnel dès les premiers mois pour améliorer le service public.",
        "Améliorer l'accueil et l'écoute dans les services administratifs.",
    ],

    # ═══ ÉCONOMIE ═══
    "commerce-local": [
        "Créer un accueil municipal dédié pour accompagner l'installation et la pérennité des commerces.",
        "Proposer des aides ciblées pour la rénovation des vitrines et façades commerciales.",
        "Attirer des activités manquantes : librairie, boulangerie, restauration de qualité, réparation vélo.",
        "Protéger les commerces de quartier historiques et les activités culturelles indépendantes.",
        "Sécuriser les abords des commerces en coordination avec la police municipale.",
    ],
    "emploi-insertion": [
        "Lancer des Assises locales de l'emploi et de la formation dès la première année du mandat.",
        "Conditionner les aides municipales à des retombées concrètes en emploi local.",
        "Soutenir la Mission locale et le service jeunesse pour l'orientation et l'accès à l'emploi.",
        "Repenser les parcours d'insertion en s'appuyant sur la régie de quartier.",
        "Développer des permanences de droit du travail de proximité (Bourse du travail).",
        "Favoriser l'emploi local sur les chantiers des grands projets.",
        "Stimuler les projets d'économie sociale et solidaire (ESS).",
    ],
    "attractivite": [
        "Développer l'attractivité économique pour créer des emplois locaux à Aubervilliers.",
        "Mettre en place une politique d'achats responsables favorisant les retombées locales.",
    ],

    # ═══ CULTURE ═══
    "equipements-culturels": [
        "Moderniser les équipements culturels en souffrance.",
        "Garantir le fonctionnement du Conservatoire et actualiser son projet d'établissement pour une plus grande accessibilité.",
        "Développer la lecture publique avec une médiathèque centrale et des médiathèques de quartier.",
        "Reconnaître et accompagner les structures culturelles locales.",
    ],
    "evenements-creation": [
        "Développer des événements culturels dans les rues, places et quartiers.",
        "Encourager les pratiques artistiques en plein air.",
        "Soutenir la création artistique issue du territoire et les projets portés par des artistes locaux.",
        "Valoriser l'histoire, les mémoires et les cultures populaires de la ville.",
        "Créer une équipe municipale dédiée aux projets culturels avec écoles, structures sociales et habitants.",
        "Créer un ticket culturel d'Aubervilliers pour faciliter la découverte des lieux culturels.",
    ],

    # ═══ SPORT ═══
    "equipements-sportifs": [
        "Développer des zones sportives de proximité dans tous les quartiers.",
        "Rénover et entretenir les équipements sportifs existants.",
        "Élargir les horaires d'ouverture des équipements pour favoriser la pratique libre et gratuite.",
        "Répondre aux besoins prioritaires : natation, sports en salle, danse, gymnastique.",
    ],
    "sport-pour-tous": [
        "Renforcer le soutien aux clubs et associations sportives.",
        "Faciliter l'inscription aux clubs et l'accès au sport pendant les vacances.",
        "Garantir l'égalité d'accès au sport pour les jeunes, les femmes, les seniors et les personnes handicapées.",
    ],

    # ═══ URBANISME ═══
    "amenagement-urbain": [
        "Refuser la densification excessive et protéger les espaces verts et la pleine terre.",
        "Imposer des exigences sociales et écologiques aux promoteurs immobiliers.",
        "Co-construire un scénario urbain avec les habitants pour un aménagement cohérent.",
        "Organiser des concertations réelles sur les projets structurants et garantir la transparence.",
        "Réaliser un plan de remise à niveau des trottoirs et de la voirie.",
        "Moderniser l'éclairage public pour le rendre fiable, économe et sécurisant.",
        "Défendre les riverains face aux nuisances des grands chantiers et exiger des compensations locales.",
    ],
    "accessibilite": [
        "Rendre accessibles progressivement les écoles, équipements et services publics aux personnes handicapées.",
        "Mettre en conformité trottoirs, passages piétons et arrêts de bus.",
        "Intégrer l'accessibilité dans tous les projets municipaux.",
        "Soutenir les AESH et accompagner les familles d'enfants en situation de handicap.",
    ],
    "quartiers-prioritaires": [
        "Installer une antenne municipale mobile permanente au quartier des Quatre-Chemins.",
        "Auditer chaque quartier pour prioriser les zones les plus bétonnées en végétalisation.",
        "Faire respecter l'identité de chaque quartier dans les choix d'aménagement.",
    ],

    # ═══ SOLIDARITÉ ═══
    "aide-sociale": [
        "Renforcer l'accompagnement social de proximité via le CCAS.",
        "Lutter contre le non-recours aux droits en allant vers les publics les plus éloignés.",
        "Soutenir l'aide alimentaire et les dispositifs d'urgence sociale.",
        "Accompagner les personnes sans domicile ou très précaires.",
        "Créer un guichet unique 'Parents solo' adossé à la Maison des Femmes.",
        "Proposer des espaces de répit, ateliers de parentalité et groupes de parole pour les mères isolées.",
        "Proposer des aides ciblées pour les charges essentielles et la garde d'enfants des familles monoparentales.",
    ],
    "egalite-discriminations": [
        "Relancer un comité interreligieux opérationnel pour le dialogue et la prévention des tensions.",
        "Valoriser les cultures du monde qui font Aubervilliers par des initiatives culturelles et éducatives.",
        "Organiser des visites guidées citoyennes et un livret d'accueil pour les nouveaux habitants.",
        "Créer des temps de transmission autour de l'histoire locale, des luttes sociales et des mémoires migratoires.",
        "Favoriser les rencontres intergénérationnelles et interculturelles.",
    ],
    "pouvoir-achat": [
        "Défendre une fiscalité locale juste et progressive.",
        "Défendre un prix de l'eau juste et lisible, prévenir les coupures pour les ménages en difficulté.",
        "Déployer des fontaines publiques et points d'eau dans l'espace public.",
        "Engager le désendettement de la ville pour dégager des marges au service des habitants.",
    ],
}

# ─── Intégration dans le JSON ───

def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Mettre à jour le candidat
    for candidat in data['candidats']:
        if candidat['id'] == CANDIDAT_ID:
            candidat['programmeUrl'] = SOURCE_URL
            candidat['programmeComplet'] = True
            candidat['programmePdfPath'] = "Nabila Djebbari.pdf"
            break

    # Injecter les propositions
    total = 0
    stats = {}
    for cat in data['categories']:
        cat_count = 0
        for st in cat['sousThemes']:
            st_id = st['id']
            if st_id in PROPOSITIONS:
                mesures = PROPOSITIONS[st_id]
                st['propositions'][CANDIDAT_ID] = {
                    "source": SOURCE,
                    "sourceUrl": SOURCE_URL,
                    "mesures": mesures
                }
                cat_count += len(mesures)
                total += len(mesures)
            # else: leave as null (no measures for this sub-theme)
        stats[cat['id']] = cat_count

    # Écriture
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Stats
    print(f"\n{'='*60}")
    print(f"  INTÉGRATION DJEBBARI — Aubervilliers")
    print(f"{'='*60}")
    print(f"\n  Total mesures : {total}")
    print(f"\n  Répartition par catégorie :")
    for cat_id, count in stats.items():
        bar = '█' * count
        print(f"    {cat_id:<25} {count:>3}  {bar}")
    print(f"\n  programmeComplet: true")
    print(f"  programmeUrl: {SOURCE_URL}")
    print(f"  programmePdfPath: Nabila Djebbari.pdf")
    print(f"{'='*60}\n")

    # Vérifier les sous-thèmes non couverts
    uncovered = []
    for cat in data['categories']:
        for st in cat['sousThemes']:
            if st['propositions'].get(CANDIDAT_ID) is None:
                uncovered.append(f"{cat['id']}/{st['id']}")
    if uncovered:
        print(f"  Sous-thèmes sans mesures ({len(uncovered)}) :")
        for u in uncovered:
            print(f"    - {u}")
    else:
        print("  Tous les sous-thèmes sont couverts !")
    print()


if __name__ == '__main__':
    main()
