#!/usr/bin/env python3
"""
Met à jour les propositions de Sophia Chikirou dans paris-2026.json
avec l'extraction complète de sophiapourparis.fr (19 pages thématiques).
"""
import json
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'elections', 'paris-2026.json')

SOURCE = "Programme de campagne 2026"
SOURCE_URL = "https://sophiapourparis.fr/"

# Mapping complet des 44 sous-thèmes
PROPOSITIONS = {
    "securite": {
        "police-municipale": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-un-service-communal-de-prevention-et-de-surete/",
            "mesures": [
                "Police municipale sans arme létale, avec patrouilles à pied et à vélo et tenue moins militarisée.",
                "Augmentation des effectifs jusqu'à 3 500 agents de police municipale formés d'ici 2032.",
                "Création d'antennes de proximité dans les Maisons de quartier réunissant police, médiateurs, éducateurs et travailleurs sociaux.",
                "Affectation stable des agents à des secteurs définis pour une police territorialisée.",
                "Évaluations citoyennes annuelles via enquêtes de satisfaction."
            ]
        },
        "videoprotection": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-un-service-communal-de-prevention-et-de-surete/",
            "mesures": [
                "Arrêt du financement municipal de la vidéosurveillance.",
                "Moratoire sur les nouvelles caméras jusqu'à un audit d'efficacité indépendant.",
                "Interdiction de la reconnaissance faciale sur le territoire parisien."
            ]
        },
        "prevention-mediation": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-un-service-communal-de-prevention-et-de-surete/",
            "mesures": [
                "Recours obligatoire à la médiation avant verbalisation pour les infractions mineures.",
                "Doublement des éducateurs spécialisés et des médiateurs de rue d'ici 2029.",
                "Brigade spécialisée en santé mentale et addictions.",
                "Formation complète des agents en médiation citoyenne, premiers secours psychologiques et orientation sociale.",
                "Dispositif « premiers pas hors du trafic » pour les jeunes de 16-25 ans avec accompagnement social intensif."
            ]
        },
        "violences-femmes": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-paris-capitale-feministe/",
            "mesures": [
                "Création de Maisons des Femmes avec safe rooms, équipes pluridisciplinaires et activités culturelles.",
                "Brigade de police municipale spécialisée en violences sexistes et sexuelles (VSS).",
                "Création de 200 places d'hébergement supplémentaires pour les victimes de VSS.",
                "Cellules « dépôt de plainte facilité » dans tous les arrondissements pour doubler le taux de dépôt.",
                "Marches exploratoires féministes annuelles pour identifier les zones à risque.",
                "Doublement de l'éclairage public autour des sorties de métro à risque pour « zéro zone d'ombre » d'ici 2032."
            ]
        }
    },
    "transports": {
        "transports-en-commun": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-se-deplacer-et-circuler-mieux/",
            "mesures": [
                "Extension du réseau de Traverses jusqu'à vingt lignes.",
                "Doublement progressif de la fréquence des Traverses (de 12 à 6 minutes) et extension des horaires jusqu'à 23h.",
                "100 % de bus électriques à l'horizon 2032.",
                "Système municipal de gestion dynamique des feux avec « couloir vert » priorité systématique pour les bus et véhicules d'urgence."
            ]
        },
        "velo-mobilites-douces": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-se-deplacer-et-circuler-mieux/",
            "mesures": [
                "Création d'une régie publique du vélo avec tarification sociale et gratuité pour les moins de 26 ans.",
                "École municipale du vélo pour tous les âges et généralisation du « savoir rouler » dans les écoles.",
                "Réaménagement de 200 carrefours dangereux d'ici 2028.",
                "Expérimentation « vélo d'abord » dans 50 rues étroites avec feux décalés pour les cyclistes.",
                "Liaisons cyclables continues avec les villes voisines et vers les forêts et lieux de baignade."
            ]
        },
        "pietons-circulation": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-se-deplacer-et-circuler-mieux/",
            "mesures": [
                "Plan trottoir pour 100 % d'accessibilité aux fauteuils roulants et poussettes d'ici 2032.",
                "Création de « chemins piétons prioritaires » reliant les équipements du quotidien.",
                "Allongement du temps de feu vert piéton calibré sur 0,8 m/s.",
                "Piétonnisation partielle de 5 rues commerçantes dès 2027 et expérimentation de 5 quartiers « piétons d'abord ».",
                "Fermeture temporaire des axes aux véhicules motorisés aux horaires d'entrée/sortie d'école."
            ]
        },
        "stationnement": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-se-deplacer-et-circuler-mieux/",
            "mesures": [
                "Réduction du stationnement de surface au profit du stationnement souterrain.",
                "Reprise en gestion publique des parkings concédés à des opérateurs privés.",
                "Modulation de la tarification du stationnement résidentiel selon le quotient familial.",
                "Plateforme centralisée publique de réservation de stationnement."
            ]
        },
        "tarifs-gratuite": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-se-deplacer-et-circuler-mieux/",
            "mesures": [
                "Plaidoyer pour la gratuité des transports publics pour les moins de 25 ans via IDFM.",
                "Mobilisation des représentants de la Ville au CA d'IDFM pour geler les tarifs.",
                "Pass Paris Access' sans conditions de ressources pour les personnes en situation de handicap."
            ]
        }
    },
    "logement": {
        "logement-social": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-plan-durgence-communale-du-logement-a-paris/",
            "mesures": [
                "Acquisition de 5 000 biens pour doubler l'offre de logements publics d'ici 2032.",
                "Obligation de 10 % minimum de logements sociaux dans les nouveaux projets de 400 m², jusqu'à 55 % en zones déficitaires.",
                "Élargissement du droit de préemption renforcé de moins de 10 % à 50 % du territoire parisien.",
                "Gel des loyers sociaux la première année du mandat."
            ]
        },
        "logements-vacants": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-plan-durgence-communale-du-logement-a-paris/",
            "mesures": [
                "Brigade du Droit au Logement : tripler les agents municipaux pour identifier les 25 000 annonces Airbnb illégales.",
                "Reconversion de 50 000 logements touristiques en logements locatifs classiques.",
                "Moratoire de 3 ans sur tout nouveau logement touristique meublé.",
                "Identification des 264 000 logements vides et accompagnement des propriétaires vers la remise sur le marché.",
                "Modification du PLU bioclimatique pour interdire les nouveaux meublés touristiques dans tout Paris."
            ]
        },
        "encadrement-loyers": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-plan-durgence-communale-du-logement-a-paris/",
            "mesures": [
                "Renforcement des contrôles de l'encadrement des loyers pour éliminer les 31 % d'annonces non conformes.",
                "Défense de l'adoption d'une loi pérennisant l'encadrement des loyers.",
                "Clarification des compléments de loyer avec le Préfet.",
                "Aide directe au logement étendue à 50 000 bénéficiaires vulnérables."
            ]
        },
        "acces-logement": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-plan-durgence-communale-du-logement-a-paris/",
            "mesures": [
                "Création de la Régie Verte Populaire de Paris : structure publique de gestion locative avec commissions réduites.",
                "Programme d'incitation à la rénovation thermique couvrant 25 à 100 % des travaux sous conditions de loyers modérés.",
                "Acquisition et rénovation de copropriétés insalubres dédiées au logement social.",
                "Création d'un service municipal d'urgence pour le dépannage d'ascenseurs (parc social et copropriétés)."
            ]
        }
    },
    "education": {
        "petite-enfance": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-service-public-deducation-communale-a-paris/",
            "mesures": [
                "Une ATSEM par classe en maternelle, personnel formé pour l'hygiène et l'accompagnement.",
                "Ouverture de crèches publiques à horaires atypiques pour les parents en emploi décalé.",
                "Doublement de la pondération du critère familles monoparentales pour l'attribution en crèche (de 5 à 10 points).",
                "Médecine scolaire renforcée : une visite médicale annuelle par élève.",
                "Ouverture de 10 centres PMI jusqu'à 19h30 trois soirs par semaine et le samedi matin."
            ]
        },
        "ecoles-renovation": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-service-public-deducation-communale-a-paris/",
            "mesures": [
                "Transformation de 100 % des cours d'écoles, crèches et collèges en cours oasis avant 2040.",
                "Rénovation des sanitaires, insonorisation de la restauration, amélioration de la ventilation et du confort thermique.",
                "Plan de dépollution des sols prioritairement dans les établissements scolaires.",
                "Renforcement de l'accès aux équipements sportifs de proximité pour les écoles publiques."
            ]
        },
        "cantines-fournitures": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-service-public-deducation-communale-a-paris/",
            "mesures": [
                "Cantine gratuite pour les enfants de familles avec quotient familial de 1 à 3, tarifs progressifs ensuite.",
                "Petits-déjeuners gratuits pour tous les enfants bénéficiant de la cantine gratuite.",
                "Création d'un service municipal de soutien scolaire gratuit.",
                "Suppression du soutien municipal à l'école privée au-delà des obligations légales."
            ]
        },
        "periscolaire-loisirs": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-service-public-deducation-communale-a-paris/",
            "mesures": [
                "Recrutement de 10 000 animateurs périscolaires permanents d'ici la fin du mandat.",
                "Titularisation des 4 000 animateurs « faux vacataires » de la Ville.",
                "Taux d'encadrement : 1 pour 8 enfants de moins de 6 ans, 1 pour 12 au-delà.",
                "Ouverture des écoles les samedis et vacances pour les associations d'accompagnement scolaire, culturelles et sportives.",
                "Création d'une filière métiers de l'animation avec 5 niveaux de postes (catégories C à A)."
            ]
        },
        "jeunesse": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-faire-de-paris-la-capitale-de-lemancipation-des-jeunes/",
            "mesures": [
                "Allocation municipale équivalente au RSA pendant 12 mois (renouvelable) pour les 18-25 ans sans emploi ni formation.",
                "500 logements par an réservés aux jeunes + 5 % des nouvelles constructions, priorité boursiers.",
                "300 postes tremplins annuels : emplois municipaux pour les 21-25 ans avec accompagnement vers un CDI.",
                "5 nouvelles MJC d'envergure (coworking gratuit, salle de spectacle, espaces associatifs, cafétéria sociale).",
                "Bibliothèques ouvertes jusqu'à 22h dans les arrondissements étudiants et le dimanche après-midi.",
                "Fonds d'urgence : aide jusqu'à 1 000 € sous 72 heures (expulsion, rupture familiale, perte d'emploi)."
            ]
        }
    },
    "environnement": {
        "espaces-verts": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-lecologie-populaire-et-ladaptation-au-changement-climatique/",
            "mesures": [
                "Production de 200 hectares d'espaces verts supplémentaires durant la mandature (objectif : 10 m² par habitant, recommandation OMS).",
                "Principe « zéro artificialisation » des sols.",
                "Création de nouveaux boisements urbains denses d'au moins 1 hectare chacun.",
                "Remplacement des grands projets inutiles par des parcs (Porte de la Villette, Gare des mines, etc.).",
                "Végétalisation obligatoire des façades aveugles par modification du PLU bioclimatique."
            ]
        },
        "proprete-dechets": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-une-ville-propre-un-service-public-de-proximite/",
            "mesures": [
                "Remunicipalisation à 100 % du service de propreté d'ici 2030 (audit et non-renouvellement des DSP).",
                "Recrutement de 300 agents supplémentaires et investissement de 30 à 40 M€ en matériel.",
                "Réseau municipal de consigne pour bouteilles en verre et généralisation des bacs marron (compost) dans les copropriétés de plus de 10 logements.",
                "Plan de sortie de l'incinération : moratoire, baisse de 4-5 % par an des tonnages incinérés, investissement massif dans le tri.",
                "Régulation éthique des rongeurs : budget de 15 M€, méthodes non létales, grillages anti-remontée sur 10 000 plaques d'égout."
            ]
        },
        "climat-adaptation": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-lecologie-populaire-et-ladaptation-au-changement-climatique/",
            "mesures": [
                "Budget annuel carbone municipal contraignant avec plafonds d'émission par secteur et tableau de bord de suivi.",
                "Bilan carbone obligatoire pour tout projet d'investissement supérieur à 10 M€.",
                "Îlot de fraîcheur garanti dans un rayon de 300 mètres pour tous les Parisiens, avec cartographie en temps réel.",
                "Déploiement de toiles ombrières dans les rues exposées et extension du réseau municipal de froid urbain public.",
                "Tarification progressive de l'eau avec gratuité des 50 premiers litres par jour par personne.",
                "Interdiction de la circulation des véhicules thermiques en période de canicule sauf urgences médicales."
            ]
        },
        "renovation-energetique": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-lecologie-populaire-et-ladaptation-au-changement-climatique/",
            "mesures": [
                "Accélération de la rénovation des logements sociaux de 5 000 à 8 000 par an, objectif 100 % rénovés en 2055.",
                "Objectif de 40 000 logements rénovés par an d'ici 2032 via la régie publique de gestion locative.",
                "Création d'une grande école métropolitaine des métiers de la rénovation thermique.",
                "Prêt municipal à taux zéro sur 20 ans pour les copropriétés et primo-accédants, remboursé sur les économies d'énergie.",
                "Couverture de 400 à 500 toits d'établissements municipaux de panneaux photovoltaïques d'ici 2032.",
                "Création d'une société publique locale « Énergie de Paris » pour la production d'énergie renouvelable."
            ]
        },
        "alimentation-durable": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-relancer-lactivite-economique-de-proximite/",
            "mesures": [
                "Passage de 37 à 100 hectares dédiés à l'agriculture urbaine d'ici 2032.",
                "Réservation de 30 % des emplacements des marchés aux producteurs franciliens et 20 % aux commerces alimentaires indépendants.",
                "Création de 2 halles alimentaires couvertes (30-50 commerçants, 6j/7, loyers accessibles).",
                "Création d'un réseau d'épiceries solidaires municipales dans les quartiers populaires avec tarification selon quotient familial.",
                "Interdiction des plastiques à usage unique dans les marchés et événements municipaux, vaisselle réutilisable obligatoire."
            ]
        }
    },
    "sante": {
        "centres-sante": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-service-public-communal-de-la-sante/",
            "mesures": [
                "Densification des centres de santé municipaux polyvalents : un par arrondissement d'ici 2032.",
                "Unités mobiles de prévention et bus itinérants santé dans les quartiers prioritaires.",
                "Création de 5 maisons médicales de garde en partenariat avec l'AP-HP.",
                "Location de 20 % des locaux de Paris Commerces à des cabinets médicaux au tiers payant (loyers réduits de 50 %).",
                "Sauvetage des centres de santé associatifs par subventions et reprises municipales."
            ]
        },
        "prevention-sante": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-service-public-communal-de-la-sante/",
            "mesures": [
                "Recrutement de 2 psychologues par centre de santé d'ici 2032 et « Chèque Psy » de 20 €/séance selon le quotient familial.",
                "Généralisation des Conseils Locaux de Santé Mentale dans tous les arrondissements.",
                "Création d'une Complémentaire Populaire Communale pour les retraités et étudiants sans couverture.",
                "Cellule municipale « Urbanisme & Santé » et généralisation des études d'impact sanitaire pour les projets d'urbanisme.",
                "Renforcement du Service Parisien de Santé Environnementale (doublement des effectifs)."
            ]
        },
        "seniors": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-prendre-soin-des-personnes-agees/",
            "mesures": [
                "Généralisation des Conseils des Seniors dans tous les arrondissements avec rôle consultatif renforcé.",
                "Recrutement de 300 aides à domicile supplémentaires et 300 soignants en EHPAD.",
                "Investissement de 50 M€ pour la rénovation des EHPAD et 30 M€ pour les résidences autonomie.",
                "Création de 500 places supplémentaires en habitat inclusif et 15 000 bancs de repos d'ici 2032.",
                "Bilans de prévention gratuits (chutes, nutrition, mémoire, vue, audition) et « Rendez-vous des 65 ans ».",
                "Création d'un réseau « Voisins Solidaires et Bienveillants » et de « Commerces Sentinelles » pour lutter contre l'isolement."
            ]
        }
    },
    "democratie": {
        "budget-participatif": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-la-revolution-citoyenne-communale/",
            "mesures": [
                "Budget participatif porté de 5 % à 15 % du budget d'investissement (300 millions d'euros).",
                "Référendum communal d'initiative citoyenne : toute délibération soumise à référendum dès 100 000 signatures.",
                "Droit de révocation des élus après 3 ans si 10 % de l'électorat vote pour.",
                "Création de Maisons de quartier cogérées avec conseils de quartier, services publics et espaces communs.",
                "Renforcement des conseils de quartier : tirage au sort d'un tiers des membres, parité femme-homme."
            ]
        },
        "transparence": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-la-revolution-citoyenne-communale/",
            "mesures": [
                "Registre public des lobbys : publication obligatoire sous 72h de tout rendez-vous avec des représentants d'intérêts.",
                "Division par deux des dépenses en cabinets de conseil d'ici 2032.",
                "Réduction des frais de représentation : interdiction des achats vestimentaires, forfait de 25 € par repas professionnel.",
                "Open data : publication des délibérations, marchés publics, subventions et autorisations d'urbanisme.",
                "Déclaration patrimoniale annuelle des élus insoumis et restitution des indemnités satellites au budget municipal."
            ]
        },
        "vie-associative": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-la-revolution-citoyenne-communale/",
            "mesures": [
                "Création d'une Maison de la Presse et des Radios Associatives avec locaux et moyens techniques mutualisés.",
                "Fonds municipal de subvention des médias indépendants parisiens.",
                "Pépinière d'éditeurs : mise à disposition de locaux municipaux à loyers modérés pour jeunes maisons d'édition.",
                "Prix littéraire municipal récompensant annuellement 5 œuvres d'éditeurs indépendants parisiens.",
                "Protection juridique des librairies : fonds d'aide légale de 100 000 € annuels et garantie municipale des loyers."
            ]
        },
        "services-publics": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-la-revolution-citoyenne-communale/",
            "mesures": [
                "Garantie d'un accueil physique dans toutes les mairies d'arrondissement.",
                "Création d'un Conseil Économique, Social, Écologique Parisien (CESEP) consultatif sur les questions majeures.",
                "Remunicipalisation des activités privatisées (collecte des déchets, Vélib', marchés, etc.).",
                "Sessions citoyennes élargies : mairies d'arrondissement siégeant trimestriellement en format ouvert au public.",
                "Carte de résidence parisienne gratuite pour tous les résidents de plus de 16 ans, sans conditions de nationalité."
            ]
        }
    },
    "economie": {
        "commerce-local": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-relancer-lactivite-economique-de-proximite/",
            "mesures": [
                "Création d'un statut de « Commerce Essentiel de Quartier » (boulangerie, boucherie, épicerie, librairie, cordonnerie, etc.).",
                "Transformation de Paris Commerces en Régie Communale du Commerce avec objectif de 150 acquisitions annuelles (contre 40-50).",
                "Bail commercial d'utilité sociale avec loyer plafonné à 400 €/m²/an (200 €/m²/an pour les commerces essentiels).",
                "Généralisation du droit de préemption commercial dans tous les arrondissements.",
                "Lutte contre les dark stores et dark kitchens : astreintes financières et obligation de vitrine ouverte sur rue."
            ]
        },
        "emploi-insertion": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-relancer-lactivite-economique-de-proximite/",
            "mesures": [
                "Création de 3 « Manufactures Parisiennes » (1 000-2 000 m² chacune, 15-20 ateliers, équipements mutualisés).",
                "Programme « Paris Stages » : 1 000 stages rémunérés de 4 à 6 mois par an.",
                "Création d'une « Académie du service public parisien » regroupant formation continue, apprentissage et promotion.",
                "Garantie d'une rémunération mensuelle minimale de 1 600 € nets pour les agents municipaux, 1 800 € en fin de mandature.",
                "Titularisation progressive des vacataires et contractuels à partir de 2027."
            ]
        },
        "attractivite": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-relancer-lactivite-economique-de-proximite/",
            "mesures": [
                "Création du label « Véritable produit parisien » et demande d'IGP pour les champignons de Paris.",
                "Relocalisation de la production à Paris : textile, micro-distilleries, champignonnières urbaines souterraines.",
                "Moratoire sur les ventes et cessions de biens immobiliers et fonciers municipaux pendant la mandature.",
                "Fonds municipal pour sauvegarder les espaces culturels menacés et les librairies indépendantes."
            ]
        }
    },
    "culture": {
        "equipements-culturels": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-proteger-le-patrimoine-et-les-biens-communs-des-parisiens/",
            "mesures": [
                "Fonds municipal de sauvetage des espaces culturels menacés et des librairies indépendantes.",
                "Soutien aux cinémas indépendants et mobilisation des leviers municipaux (SCIC, municipalisation).",
                "Garantie municipale pour les loyers des artistes non-salariés et mise à disposition de lieux vacants pour la création.",
                "Fin de la mainmise d'entreprises (notamment LVMH) sur le patrimoine culturel municipal.",
                "Soutien à l'Atelier des Artistes en Exil : financement de 3 lieux supplémentaires d'ici 2032."
            ]
        },
        "evenements-creation": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-proteger-le-patrimoine-et-les-biens-communs-des-parisiens/",
            "mesures": [
                "Création d'espaces festifs autogérés gratuits et accessibles sur des friches ou dans des salles municipales.",
                "Conditionnement des subventions culturelles à des critères de parité et de diversité dans la programmation.",
                "Organisation annuelle du Festival « Paris Terre d'Exils » valorisant les cultures des diasporas.",
                "Prix parisien de la jeunesse antiraciste récompensant chaque année des projets de jeunes contre les discriminations."
            ]
        }
    },
    "sport": {
        "equipements-sportifs": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-faire-de-paris-la-capitale-de-lemancipation-des-jeunes/",
            "mesures": [
                "Ouverture des équipements sportifs municipaux jusqu'à 23h les vendredis et samedis pour les 18-25 ans.",
                "Refus du nommage des équipements sportifs par des marques commerciales.",
                "Renforcement de l'accès aux équipements sportifs de proximité pour les écoles publiques.",
                "Ouverture de salles municipales nocturnes pour activités non-marchandes (ateliers, cinéma, musique)."
            ]
        },
        "sport-pour-tous": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-faire-de-paris-la-capitale-de-lemancipation-des-jeunes/",
            "mesures": [
                "Gratuité de tous les équipements sportifs municipaux pour les 18-25 ans.",
                "Pass Sport Santé : accès gratuit pendant 6 mois à une activité sportive sur prescription médicale.",
                "Cours de sports adaptés aux seniors dans les Maisons de quartier.",
                "Renforcement des clubs inclusifs et sections handisport dans tous les arrondissements.",
                "Extension de la gratuité des piscines à tous les équipements sportifs et culturels pour les détenteurs de la carte CMI."
            ]
        }
    },
    "urbanisme": {
        "amenagement-urbain": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-se-deplacer-et-circuler-mieux/",
            "mesures": [
                "Concertation avec l'État, la Région et la Métropole pour la transformation du périphérique en boulevard urbain.",
                "Report du trafic de transit sur l'A86 et renforcement des dispositifs de réduction des nuisances.",
                "Moratoire complet sur la construction de nouveaux bureaux à Paris.",
                "Extension des journées « Paris Respire » et expérimentation de zones de circulation apaisée à 20 km/h."
            ]
        },
        "accessibilite": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/laccessibilite-universelle-notre-grande-cause-communale/",
            "mesures": [
                "Mise en conformité de 100 % des équipements municipaux d'ici la fin de la mandature.",
                "Actualisation du Plan de mise en accessibilité de la voirie avec calendrier 2032.",
                "Guichet unique handicap dans chaque mairie d'arrondissement.",
                "Pass Paris Access' sans conditions de ressources pour les personnes en situation de handicap.",
                "Objectif de 10 % d'agents municipaux en situation de handicap.",
                "100 % des élèves handicapés accueillis en périscolaire à l'horizon 2032."
            ]
        },
        "quartiers-prioritaires": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-service-public-communal-de-la-sante/",
            "mesures": [
                "Rééquilibrage des moyens et des équipements publics en faveur des arrondissements périphériques et des quartiers populaires.",
                "Bus itinérants santé dans les quartiers prioritaires.",
                "Permanences CASVP mensuelles dans les écoles, hebdomadaires en REP/REP+.",
                "Réseau d'épiceries solidaires municipales dans les quartiers populaires."
            ]
        }
    },
    "solidarite": {
        "aide-sociale": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-faire-de-paris-la-capitale-de-lemancipation-des-jeunes/",
            "mesures": [
                "Allocation municipale équivalente au RSA pour les 18-25 ans sortant de l'ASE.",
                "Centre Municipal de Premier Accueil (CMPA) de 500 places pour l'hébergement d'urgence des migrants.",
                "Carte Paris Solidaire : accès gratuit aux équipements municipaux (piscines, bibliothèques, musées) pour les migrants hébergés.",
                "Doublement de l'aide alimentaire pour les étudiants (de 405 000 € à 810 000 € dès 2026, 1,5 M€ en 2032).",
                "Hébergement inconditionnel d'urgence pour les mineurs non accompagnés (MNA).",
                "Présomption systématique de minorité pour les MNA jusqu'à décision judiciaire définitive."
            ]
        },
        "egalite-discriminations": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/notre-plan-pour-paris-capitale-antiraciste/",
            "mesures": [
                "Plan « Paris Capitale Antiraciste » avec délégation générale rattachée à la maire.",
                "Observatoire parisien des discriminations indépendant avec capacité de testing et publication autonome.",
                "Budgétisation sensible au genre : indicateurs transparents pour chaque euro dépensé.",
                "Carte de résidence parisienne donnant accès aux services municipaux sans condition de nationalité.",
                "Congé menstruel de 2 jours par mois pour les agentes de la Ville sur certificat médical.",
                "Anonymisation du recrutement généralisée et testing annuel interne des processus de recrutement."
            ]
        },
        "pouvoir-achat": {
            "source": SOURCE,
            "sourceUrl": "https://sophiapourparis.fr/pour-un-plan-durgence-communale-du-logement-a-paris/",
            "mesures": [
                "Gratuité des 50 premiers litres d'eau par jour par personne avec tarification progressive au-delà.",
                "Cantine gratuite pour les enfants des familles QF 1-3.",
                "Aide directe au logement étendue à 50 000 bénéficiaires vulnérables.",
                "Création d'une Complémentaire Populaire Communale pour les retraités et étudiants sans couverture.",
                "Repas à 1 euro généralisé dans les cantines municipales pour les 18-25 ans."
            ]
        }
    }
}


def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Trouver Chikirou
    candidat_found = False
    for candidat in data.get('candidats', []):
        if candidat['id'] == 'chikirou':
            candidat_found = True
            break

    if not candidat_found:
        print("ERREUR: Candidat 'chikirou' non trouvé dans le fichier!")
        sys.exit(1)

    # Indexer catégories et sous-thèmes (listes → dicts)
    cat_index = {}  # cat_id -> index dans data['categories']
    st_index = {}   # (cat_id, st_id) -> index dans cat['sousThemes']
    for i, cat in enumerate(data['categories']):
        cat_index[cat['id']] = i
        for j, st in enumerate(cat['sousThemes']):
            st_index[(cat['id'], st['id'])] = j

    # Compter les anciennes mesures
    old_count = 0
    old_st_count = 0
    for cat in data['categories']:
        for st in cat['sousThemes']:
            props = st.get('propositions', {})
            if 'chikirou' in props and props['chikirou'] is not None:
                old_count += len(props['chikirou'].get('mesures', []))
                old_st_count += 1

    print(f"Avant: {old_count} mesures sur {old_st_count}/44 sous-thèmes")

    # Appliquer les nouvelles propositions
    new_count = 0
    new_st_count = 0
    for cat_id, sous_themes in PROPOSITIONS.items():
        if cat_id not in cat_index:
            print(f"  WARN: catégorie '{cat_id}' non trouvée")
            continue
        ci = cat_index[cat_id]
        for st_id, prop_data in sous_themes.items():
            key = (cat_id, st_id)
            if key not in st_index:
                print(f"  WARN: sous-thème '{st_id}' non trouvé dans '{cat_id}'")
                continue
            si = st_index[key]
            data['categories'][ci]['sousThemes'][si]['propositions']['chikirou'] = prop_data
            new_count += len(prop_data['mesures'])
            new_st_count += 1

    print(f"Après: {new_count} mesures sur {new_st_count}/44 sous-thèmes")
    print(f"Gain: +{new_count - old_count} mesures, +{new_st_count - old_st_count} sous-thèmes")

    # Écrire le fichier
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nFichier mis à jour: {DATA_PATH}")


if __name__ == '__main__':
    main()
