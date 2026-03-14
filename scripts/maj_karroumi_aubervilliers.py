#!/usr/bin/env python3
"""
Intégration du programme complet de Sofienne Karroumi (Aubervilliers 2026)
Source : PDF "sofienne karroumi.pdf"
"""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

JSON_PATH = "data/elections/aubervilliers-2026.json"
CANDIDAT_ID = "karroumi"
SOURCE = "Programme officiel 2026 — Sofienne Karroumi"
SOURCE_URL = "#"

# Mapping des mesures concrètes par sous-thème
PROPOSITIONS = {
    "securite": {
        "police-municipale": [
            "Doubler les effectifs de la police municipale pour atteindre 1 agent pour 1 000 habitants, soit 100 agents au total.",
            "Le maire assumera directement la délégation sécurité et propreté.",
            "Clarifier la stratégie de sécurité en définissant l'articulation entre Police nationale et municipale, et l'équilibre entre répression et prévention.",
            "Mettre en place un numéro simple pour joindre la police municipale 24h/24, 7j/7.",
            "Renforcer le poste mobile de police municipale et créer plusieurs annexes pour mieux couvrir le territoire.",
            "Organiser une réunion annuelle entre la population et la police municipale pour partager constats et solutions.",
            "Adopter un code de déontologie et créer une Commission locale de tranquillité et de sécurité.",
            "Faire de la sécurisation du secteur Villette – Quatre Chemins une priorité du mandat, en coordination avec Pantin et la Police nationale.",
        ],
        "videoprotection": [
            "Renforcer la vidéoprotection là où c'est utile et évaluer le dispositif actuel pour privilégier l'efficacité sur la communication.",
            "Renforcer la vidéo-verbalisation pour lutter contre les dépôts sauvages et la mécanique sauvage.",
        ],
        "prevention-mediation": [
            "Améliorer la présence, la formation et la stratégie des agents de médiation pour la tranquillité publique et la gestion des conflits du quotidien.",
            "Mettre en place le dispositif Angela pour lutter contre le harcèlement de rue (réseau de commerces pour la mise à l'abri).",
            "Sécuriser les abords des écoles, collèges et lycées par un dispositif concerté de présence humaine (commerçants volontaires, médiateurs).",
            "Faire de la lutte contre le harcèlement scolaire une priorité avec des dispositifs d'écoute et d'accompagnement.",
            "Combattre les rixes en créant des projets inter-quartiers (sportifs, culturels, séjours communs).",
        ],
        "violences-femmes": [
            "Créer une Maison des Femmes pour assurer un soutien psychologique, médical et juridique permanent aux victimes de violences.",
            "Articuler cette Maison des Femmes au Pôle santé des femmes du Centre municipal de santé.",
        ],
    },
    "transports": {
        "transports-en-commun": [
            "Repenser le centre-ville autour de la future gare de la ligne 15 du Grand Paris Express avec renforcement de l'offre de transports.",
            "Piétonniser le quartier de gare pour une révolution des mobilités à Aubervilliers.",
        ],
        "velo-mobilites-douces": [
            "Créer une stratégie vélo pour faire d'Aubervilliers une ville 100 % cyclable d'ici la fin du mandat, avec des pistes de qualité.",
            "S'engager dans une politique de santé par le sport en sécurisant les mobilités douces comme le vélo et la marche.",
        ],
        "pietons-circulation": [
            "Réviser le plan de circulation d'Aubervilliers pour fluidifier le trafic, sécuriser les mobilités et apaiser les quartiers.",
            "Priorité aux piétons : aménager trottoirs et rues pour les rendre plus sûrs et accessibles, notamment aux personnes à mobilité réduite.",
            "Expérimenter la piétonisation des abords des écoles.",
        ],
        "stationnement": None,
        "tarifs-gratuite": None,
    },
    "logement": {
        "logement-social": [
            "Bouclier logement : mettre fin aux hausses automatiques de loyers de l'OPH après 5 ans d'augmentation.",
            "Rétablir la règle d'un gardien pour 100 logements dans le parc social, avec un retour des gardiens en loge.",
            "Priorité à l'entretien quotidien de l'OPH : ascenseurs, chauffage, nettoyage des parties communes, dératisation.",
            "Organiser un suivi annuel par site pour renouer la confiance avec les locataires.",
            "Revoir les statuts et la gouvernance de l'OPH pour se conformer à la loi ELAN et capter les aides nationales à la rénovation.",
            "Lancer un grand plan de réhabilitation du parc social pour baisser les factures énergétiques et améliorer le confort (isolation, accessibilité).",
            "Reprendre les projets NPNRU des quartiers Fort d'Aubervilliers et Villette pour donner une véritable voix aux locataires dans la concertation.",
        ],
        "logements-vacants": [
            "Généraliser le permis de louer à toute la ville pour lutter contre l'habitat indigne et les marchands de sommeil.",
        ],
        "encadrement-loyers": [
            "Imposer une charte de la construction à tous les constructeurs pour maîtriser les prix avec des périodes de pré-commercialisation réservées aux habitants.",
        ],
        "acces-logement": [
            "Développer le foncier solidaire pour permettre un prix à l'achat 15 à 40 % plus bas que le marché, en rattrapant le retard sur Saint-Denis.",
            "Développer une assistance spécifique pour les copropriétés gérées par des syndics bénévoles ou sans syndic.",
            "Adapter l'offre de logement aux besoins de la population dans le cadre du réaménagement du centre-ville (ligne 15).",
        ],
    },
    "education": {
        "petite-enfance": [
            "Augmenter de 20 % à 40 % l'offre d'accueil de la petite enfance d'ici la fin du mandat.",
            "Imposer aux promoteurs immobiliers l'intégration de crèches en pied d'immeuble pour tout projet d'envergure.",
            "Créer un dispositif transversal d'accompagnement et d'aide à la parentalité dans les Maisons pour Tous.",
            "Développer les Lieux d'Accueil Enfants-Parents (LAEP) avec des horaires élargis dans tous les quartiers.",
            "Proposer une programmation culturelle spécifique aux 0-3 ans.",
        ],
        "ecoles-renovation": [
            "Lancer un diagnostic global des écoles et un plan pluriannuel de réhabilitation du bâti scolaire (rénovation, végétalisation, réduction énergétique, construction).",
            "Revoir la carte scolaire pour un meilleur équilibre des quartiers et une vraie mixité scolaire.",
            "Mettre en place une prospective scolaire fiable pour éviter les fermetures de classe.",
            "Augmenter la dotation par élève pour un meilleur accès aux fournitures scolaires et développer les initiatives pédagogiques.",
            "Augmenter la présence d'ATSEM en maternelle et valoriser leurs missions.",
            "Aider les parents d'enfants en situation de handicap et améliorer leur accueil dans les structures scolaires.",
        ],
        "cantines-fournitures": [
            "Rendre la cantine gratuite pour les familles qui en ont le plus besoin.",
            "Proposer un petit-déjeuner scolaire gratuit dans chaque école.",
            "Améliorer la qualité des repas scolaires avec des menus bio, une alternative végétarienne systématique et des circuits de proximité.",
            "Étudier la possibilité d'une cuisine centrale municipale.",
            "Supprimer le système de réservation obligatoire en ligne pour la cantine et le remplacer par une inscription annuelle unique.",
            "Supprimer progressivement le plastique dans la restauration scolaire.",
        ],
        "periscolaire-loisirs": [
            "Garantir un encadrement de 1 animateur pour 10 enfants en maternelle et 1 pour 14 en élémentaire.",
            "Faire de la pause méridienne un temps scolaire utile : activités sportives et culturelles, soutien scolaire, découverte des métiers.",
            "Renforcer et coordonner le soutien scolaire en s'appuyant sur les équipes pédagogiques et les associations.",
            "Relancer le programme municipal de classes de neige, de mer ou nature.",
            "Simplifier l'accès des enseignants aux projets pédagogiques de la ville et doubler ces moyens.",
            "Offrir un ouvrage à tous les élèves des écoles publiques avant les vacances d'hiver et d'été.",
        ],
        "jeunesse": [
            "Créer l'Auber'Pass : aide financière pour licence sportive et accès aux structures culturelles pour les 11-20 ans.",
            "Renouer avec une politique populaire de colonies de vacances avec des partenariats élargis.",
            "Remettre à plat la politique tarifaire et les conditions d'inscription aux séjours et activités.",
            "Créer un guichet unique pour les jeunes coordonnant information, orientation, accompagnement, stages et accès au logement dès 18 ans.",
            "Développer les dispositifs municipaux pour les jeunes entrant dans la vie active : permis de conduire, BAFA, forums emploi, emplois saisonniers, service civique.",
            "Augmenter l'enveloppe dédiée au soutien des initiatives portées par la jeunesse.",
            "Ouvrir une antenne jeunesse dans le quartier Cochennec/Péri et veiller au devenir des Maisons de Jeunes dans les quartiers NPNRU.",
            "Créer une structure jeunesse et des équipements sportifs dans le quartier Vallès (square Lucien Brun).",
            "Favoriser les synergies avec le Campus Condorcet au bénéfice de la jeunesse d'Aubervilliers.",
        ],
    },
    "environnement": {
        "espaces-verts": [
            "Dédier 10 % de la surface communale aux espaces verts d'ici 2036 (contre 5 % aujourd'hui), soit 25 hectares supplémentaires.",
            "Créer « L'Échappée verte » : trame verte reliant le Fort d'Aubervilliers et le Canal Saint-Denis.",
            "Adopter une charte de l'arbre avec l'objectif de planter 300 arbres par an, en évitant les essences allergènes.",
            "Végétaliser systématiquement chaque intervention de voirie, aménagement, bâtiment municipal, cour d'école et place de stationnement.",
            "Rénover et agrandir le square Lucien Brun, poumon vert laissé à l'abandon.",
            "Ouvrir le Canal Saint-Denis sur la ville pour en faire un lieu de vie, avec fontaines, miroirs d'eau et brumisateurs.",
        ],
        "proprete-dechets": [
            "Assurer la propreté aux abords des écoles en priorité immédiate.",
            "Lutter contre les dépôts sauvages par le renforcement de la vidéo-verbalisation.",
            "Intensifier le nettoyage des squares et parcs aux beaux jours.",
            "Lancer une stratégie de prévention et de communication associant la population à la propreté (« Aubervilliers ville propre »).",
            "Organiser un grand concours scolaire de l'école et du quartier le plus propre.",
            "Adapter les fréquences de nettoiement à la réalité des quartiers.",
            "Renforcer la coordination avec les bailleurs sociaux pour la propreté des espaces résidentiels.",
            "Développer des caniparcs avec distributeurs de sacs dans les espaces verts.",
            "Organiser une mobilisation citoyenne permanente pour la propreté avec les Conseils de quartier.",
            "Augmenter le nombre de composteurs distribués dans les immeubles.",
            "Augmenter significativement le nombre de poubelles sur l'espace public.",
        ],
        "climat-adaptation": [
            "Se préparer à vivre à Aubervilliers en 2050 avec des étés à +4 °C : normes environnementales ambitieuses pour les constructions, adaptation aux canicules.",
            "Stopper la bétonisation sauvage et préférer les îlots de fraîcheur aux promoteurs immobiliers.",
        ],
        "renovation-energetique": [
            "Lancer un plan de réhabilitation massif de l'OPH pour baisser les factures énergétiques et améliorer l'isolation.",
            "Intégrer la réduction des factures énergétiques dans le plan pluriannuel de réhabilitation du bâti scolaire.",
        ],
        "alimentation-durable": [
            "Lancer un marché artisanal et bio en circuit court avec producteurs locaux, artisans et créateurs.",
            "Favoriser le bio et les circuits de proximité dans la restauration scolaire, avec développement de l'emploi local.",
        ],
    },
    "sante": {
        "centres-sante": [
            "Créer une antenne supplémentaire au Centre municipal de santé (CMS) pour mieux répondre aux besoins.",
            "Mettre en place des permanences mobiles d'accès aux soins (dispositifs d'aller-vers).",
            "Renforcer la présence de professionnels de santé en mobilisant l'ARS et le programme « Docteur junior ».",
            "Accompagner les professionnels de santé dans la recherche de locaux pour exercer.",
        ],
        "prevention-sante": [
            "Sensibiliser les habitants de tous âges aux enjeux de santé : prévention, dépistage, pollution, addictions, protoxyde d'azote.",
            "Faire de la santé mentale une grande priorité : réseau d'ambassadeurs, point d'écoute gratuit et anonyme pour les jeunes.",
            "Soutenir le projet d'un second Centre médico-psychologique (CMP) face à la croissance des besoins.",
            "S'engager dans une politique de santé par le sport avec les écoles et associations.",
            "Mettre en place un contrôle médical annuel pour chaque licencié des clubs sportifs (dispositif Ousmane Diaby).",
            "Renforcer le service communal d'hygiène et de santé et l'équipe des inspecteurs de salubrité.",
        ],
        "seniors": [
            "Favoriser l'implication des seniors dans la vie de la ville et les événements municipaux, y compris les résidents en EHPAD.",
            "Réinstaurer le traditionnel banquet des seniors de janvier.",
            "Optimiser l'accueil dans les clubs de seniors en facilitant l'accès aux activités et séjours.",
            "Faire émerger des lieux de vie partagés et intergénérationnels valorisant l'expérience des seniors.",
            "Réhabiliter et sécuriser la résidence Salvador Allende pour les seniors autonomes.",
            "Améliorer le service d'aide à domicile pour garantir un accompagnement régulier et adapté.",
            "Soutenir les associations de lutte contre l'isolement social des seniors.",
            "Aménager l'espace public avec zones de repos et commerces accessibles pour les personnes âgées.",
        ],
    },
    "democratie": {
        "budget-participatif": [
            "Créer un dispositif de budget participatif incluant un volet quartiers et un volet général, mobilisant une part significative du budget d'investissement dès 2026-2027.",
            "Engager des assises de la démocratie participative dès le début du mandat.",
            "Constituer une assemblée citoyenne tirée au sort pour produire des avis sur les stratégies urbaines et observer les engagements.",
        ],
        "transparence": [
            "Prévoir un examen public du compte-rendu de mandat tous les 2 ans avec débat citoyen.",
            "Mettre en place une gestion municipale transparente en associant les habitants à l'élaboration du budget.",
            "Pas d'augmentation de la taxe foncière pendant le mandat.",
            "Évaluer les délégations de service public confiées aux opérateurs privés, avec possibilité de retour en gestion publique.",
        ],
        "vie-associative": [
            "Organiser une cérémonie des bénévoles chaque année.",
            "Mettre à disposition des locaux municipaux pour soutenir les activités citoyennes, Conseils de quartier et assemblées générales.",
            "Sanctuariser la Bourse du travail d'Aubervilliers et fêter ses 120 ans en 2026.",
            "Rénover profondément les Conseils de quartier pour stimuler la participation et leur assurer des moyens opérationnels.",
            "Stimuler le mécénat d'entreprise à objet social, culturel ou éducatif.",
        ],
        "services-publics": [
            "Renouer le dialogue social avec les agents municipaux et leurs représentants syndicaux.",
            "Organiser des assises du personnel dès le début du mandat.",
            "Privilégier la gestion en régie directe plutôt que le recours à des prestataires privés.",
            "Mettre en place « Auber Mobile » : permanences mobiles gratuites et sans rendez-vous pour accompagner les habitants dans leurs démarches.",
            "Remettre en place la conférence des cadres et présenter la feuille de route du mandat.",
            "Organiser un lieu de restauration collective pour les personnels municipaux.",
            "Réintroduire les trois mois de départ anticipé avant la retraite pour les agents municipaux.",
        ],
    },
    "economie": {
        "commerce-local": [
            "Plan zéro rideau baissé : créer une foncière commerciale municipale pour acquérir des locaux et les louer à tarifs modérés.",
            "Créer un Conseil local du commerce pour diversifier les enseignes dans tous les quartiers.",
            "Favoriser le retour des commerces et marchés de bouche dans les quartiers délaissés ; rouvrir le marché des 4 Chemins sur la dalle Villette.",
            "Intégrer la diversification commerciale dans les opérations de rénovation urbaine (Maladrerie, Émile Dubois, Gabriel Péri).",
            "Faire de la rue du Moutier le véritable poumon commerçant de la ville avec diversification des enseignes.",
            "Accompagner les commerçants et artisans dans leur transition écologique (diagnostics gratuits, aides, formations).",
            "Assurer des animations et illuminations de fête dans tous les quartiers.",
            "Traiter en priorité la revitalisation du centre commercial le Millénaire (attractivité, accessibilité, diversification).",
        ],
        "emploi-insertion": [
            "Créer un incubateur municipal pour faire émerger les créateurs d'entreprise d'Aubervilliers.",
            "Organiser des forums emploi deux fois par an.",
            "Développer les clauses d'insertion avec les grandes opérations pour favoriser l'emploi local.",
            "Favoriser les chantiers éducatifs et d'insertion avec job dating par quartier, forums et stages pour les collégiens et lycéens.",
            "Soutenir les entreprises de l'économie sociale et solidaire (coopératives, ressourceries, circuits courts) et les entreprises à but d'emploi.",
        ],
        "attractivite": [
            "Créer une cité de la mode et de l'artisanat éthique et solidaire à la Porte d'Aubervilliers, avec des partenaires comme Chanel et le lycée d'Alembert.",
            "Développer les industries qui font l'identité d'Aubervilliers : luxe, textile, création cinématographique.",
            "Développer les relations de travail avec les partenaires (villes, Plaine Commune, Département, ANRU) pour sortir Aubervilliers de l'isolement.",
            "Créer une entrée de ville apaisée à la Porte de la Villette en coordination avec Paris.",
        ],
    },
    "culture": {
        "equipements-culturels": [
            "Sauver le cinéma Le Studio en augmentant le nombre de salles et en diversifiant son utilisation.",
            "Créer un réseau de médiathèques structurant dans chaque quartier, avec rénovation des existantes et création d'une médiathèque centrale.",
            "Installer un équipement culturel métropolitain à la Porte de la Villette.",
            "Préserver les friches culturelles d'Aubervilliers (Villa Mais d'ici, les Poussières, le Point Fort, les Laboratoires, le CAPA).",
            "Obtenir des financements de la Région et de l'État pour le Conservatoire à rayonnement régional.",
            "Faciliter la création d'ateliers d'artistes.",
        ],
        "evenements-creation": [
            "Mettre en place un Pass Culture : tarif préférentiel pour les habitants aux grands lieux culturels d'Aubervilliers.",
            "Créer un grand rendez-vous annuel pour célébrer les talents d'Aubervilliers (artistes, artisans, sportifs).",
            "Valoriser le patrimoine et l'histoire d'Aubervilliers par un inventaire du patrimoine.",
            "Distribuer un agenda culturel gratuit au moins deux fois par an.",
            "Travailler en étroite collaboration avec les associations culturelles.",
            "Renforcer la relation entre écoles et Conservatoire pour le rendre accessible à tous.",
        ],
    },
    "sport": {
        "equipements-sportifs": [
            "Rouvrir la piscine de centre-ville Marlène Peratou pour l'apprentissage scolaire du savoir nager.",
            "Rénover les gymnases Manouchian et Robespierre, dont une rénovation spécifiquement dédiée au handisport.",
            "Étudier le transfert de gestion des piscines municipales à Plaine Commune pour un meilleur entretien.",
            "Embellir l'espace public par des équipements sportifs en plein air.",
        ],
        "sport-pour-tous": [
            "Renforcer le soutien aux clubs et associations sportives pour augmenter la pratique et faire émerger des équipes de haut niveau.",
            "Soutenir les clubs qui développent la pratique féminine.",
            "Intégrer les sportifs handisport par l'aménagement des espaces et équipements.",
            "Garantir une égalité de traitement dans l'accompagnement des associations sportives.",
            "Mettre en place un grand plan annuel de redynamisation par le sport pour tous les publics (femmes, seniors), dans tous les quartiers.",
            "Recréer un lien fort entre habitants et sections sportives par des événements culinaires et culturels lors des matchs.",
        ],
    },
    "urbanisme": {
        "amenagement-urbain": [
            "Stopper la bétonisation sauvage : préférer les îlots de fraîcheur aux promoteurs dans une ville à 16 000 hab/km².",
            "Aucune décision d'aménagement sans dialogue avec la population.",
            "Repenser le centre-ville autour de la gare de la ligne 15 : logement adapté, services publics, offre commerciale diversifiée, végétalisation.",
            "Repenser les entrées de commune (Porte de la Villette, Porte d'Aubervilliers) pour retrouver la fierté d'habiter à Aubervilliers.",
            "Imposer une charte de la construction avec haut niveau d'exigence architecturale et environnementale.",
        ],
        "accessibilite": [
            "Créer une commission citoyenne d'accessibilité composée d'habitants en situation de handicap, consultée sur chaque projet de voirie.",
            "Repenser les aires de jeux avec des équipements adaptés aux enfants handicapés ; prévoir une aire 100 % accessible au square Lucien Brun.",
            "Doter les écoles, accueils de loisirs et école municipale des sports de matériels adaptés.",
            "Équiper l'ensemble des commerces, centres médicaux et pharmacies en rampes d'accès mobiles via un chantier d'insertion.",
            "Former chaque agent municipal en contact avec le public aux différents types de handicaps.",
            "Faire des espaces publics inclusifs : aménagements en faveur du handicap, de l'égalité femmes-hommes et à hauteur d'enfants.",
        ],
        "quartiers-prioritaires": [
            "Reprendre les projets de rénovation urbaine NPNRU des quartiers Fort d'Aubervilliers, Villette et Maladrerie avec une vraie concertation.",
            "Créer une antenne jeunesse et des équipements sportifs dans le quartier Vallès (square Lucien Brun).",
            "Ouvrir un local ouvert aux jeunes dans le quartier Francis de Pressensé.",
        ],
    },
    "solidarite": {
        "aide-sociale": [
            "Ouvrir un gymnase pour les sans-abris en cas de grand froid avec repas de solidarité et douches chaque jour de 22h à 7h.",
            "Lutter contre le non-recours aux aides via les permanences mobiles « Auber Mobile ».",
            "Renforcer le soutien aux associations agissant pour le bien-être des animaux errants (stérilisation, accueil, refuge).",
            "Aider les personnes vulnérables qui ont des difficultés à s'occuper de leurs animaux.",
        ],
        "egalite-discriminations": [
            "Renforcer l'égalité, la laïcité et la diversité en agissant contre toutes les formes de discrimination.",
            "Développer le dialogue avec les représentants de toutes les communautés religieuses dans un esprit républicain et laïque.",
            "Objectif Aubervilliers 100 % inclusif pour les personnes en situation de handicap.",
        ],
        "pouvoir-achat": [
            "Bouclier logement : fin des hausses automatiques de loyers de l'OPH.",
            "Pas d'augmentation de la taxe foncière pendant le mandat.",
            "Développer le foncier solidaire pour permettre l'accession à la propriété 15 à 40 % en dessous du prix du marché.",
        ],
    },
}

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update candidat metadata
    for candidat in data["candidats"]:
        if candidat["id"] == CANDIDAT_ID:
            candidat["programmeComplet"] = True
            candidat["programmePdfPath"] = "sofienne karroumi.pdf"
            # Keep programmeUrl as "#" (no campaign site found in PDF)
            break

    # Update propositions
    total_mesures = 0
    sous_themes_remplis = 0
    for categorie in data["categories"]:
        cat_id = categorie["id"]
        if cat_id not in PROPOSITIONS:
            continue
        for st in categorie["sousThemes"]:
            st_id = st["id"]
            if cat_id in PROPOSITIONS and st_id in PROPOSITIONS[cat_id]:
                mesures = PROPOSITIONS[cat_id][st_id]
                if mesures is not None:
                    st["propositions"][CANDIDAT_ID] = {
                        "source": SOURCE,
                        "sourceUrl": SOURCE_URL,
                        "mesures": mesures,
                    }
                    total_mesures += len(mesures)
                    sous_themes_remplis += 1
                # If None, leave as null (don't touch)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"=== Intégration Sofienne Karroumi — Aubervilliers ===")
    print(f"Sous-thèmes remplis : {sous_themes_remplis}")
    print(f"Total mesures : {total_mesures}")
    print(f"programmeComplet : True")
    print(f"programmePdfPath : sofienne karroumi.pdf")
    print(f"Fichier écrit : {JSON_PATH}")

if __name__ == "__main__":
    main()
