#!/usr/bin/env python3
"""Intègre le programme de Jules Boyadjian (Valence) depuis le PDF reçu par mail."""
import json, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELECTION_PATH = os.path.join(BASE, "data", "elections", "valence-2026.json")

with open(ELECTION_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Mettre à jour le candidat ---
for c in data["candidats"]:
    if c["id"] == "boyadjian":
        c["liste"] = "Le Choix de Valence (collectif citoyen)"
        c["programmeUrl"] = "https://lechoixdevalence.fr/"
        c["programmeComplet"] = True
        c["programmePdfPath"] = "boyadjian_valence_2026.pdf"
        print(f"✓ Candidat mis à jour : {c['nom']}")
        break

# --- Propositions extraites du PDF (24 pages) ---
SOURCE = "Programme officiel 2026"
URL = "https://lechoixdevalence.fr/"

PROPS = {
    "securite": {
        "police-municipale": {
            "mesures": [
                "Renforcer les patrouilles pédestres et étendre les horaires de la police municipale en soirée et la nuit, notamment le week-end.",
                "Mettre en place des référents de proximité par secteur pour un lien direct avec les habitants, commerçants et associations.",
                "Créer des permanences de police municipale au cœur des quartiers, accessibles sans rendez-vous.",
                "Étudier le repositionnement du commissariat à Valence 2 pour renforcer la présence publique dans ce secteur."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "videoprotection": {
            "mesures": [
                "Maintenir et adapter la vidéoprotection sur les secteurs prioritaires, dans le respect strict des libertés publiques."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "prevention-mediation": {
            "mesures": [
                "Renforcer les équipes de médiateurs et les actions de prévention auprès des jeunes.",
                "Créer un comité citoyen police-population, présidé par un avocat, pour garantir le contrôle citoyen de la politique de sécurité locale.",
                "Réaliser une étude systématique des aménagements urbains aux abords des écoles : signalisation renforcée, zones apaisées, dispositifs de ralentissement.",
                "Déployer progressivement un éclairage LED performant avec priorité aux écoles, arrêts de bus, places et cheminements nocturnes.",
                "Renforcer le travail conjoint avec la police nationale et la justice pour lutter contre les trafics et les réseaux violents."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "violences-femmes": {
            "mesures": [
                "Créer une Maison de Santé des femmes dédiée au suivi gynécologique, à la prévention et à l'accompagnement des femmes victimes de violences, avec soutien psychologique."
            ],
            "source": SOURCE, "sourceUrl": URL
        }
    },
    "transports": {
        "transports-en-commun": {
            "mesures": [
                "Repenser les bus inter-quartiers pour faciliter les déplacements sans passage systématique par le centre.",
                "Mettre en place des bus de nuit et des navettes gratuites lors des grands événements.",
                "Rendre la gare de Valence-ville intermodale et accessible des deux côtés.",
                "Lancer un plan de mobilité concerté, quartier par quartier, soumis à référendum local."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "velo-mobilites-douces": {
            "mesures": [
                "Développer des vélorues et renforcer l'apaisement des vitesses, notamment aux abords des écoles.",
                "Multiplier les garages à vélos sécurisés près des gares, marchés, écoles et équipements publics."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "pietons-circulation": {
            "mesures": [
                "Déployer une signalétique indiquant les temps de marche entre les principaux lieux de la ville.",
                "Sécuriser les traversées piétonnes et cyclables, notamment l'avenue de Romans reconnectée aux quartiers."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "stationnement": {
            "mesures": [
                "Mettre en place 2 heures de stationnement gratuit en centre-ville.",
                "Reprendre les parkings Q-Park par la Ville à la fin de la concession."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "tarifs-gratuite": None
    },
    "logement": {
        "logement-social": {
            "mesures": [
                "Respecter un ratio d'un gardien pour 100 logements publics pour une présence quotidienne visible.",
                "Poursuivre les rénovations thermiques du parc public avec exigence de baisse réelle et mesurable des factures.",
                "Lancer dès le premier mois du mandat deux audits sur le chauffage urbain et l'évolution des charges locatives de Valence Romans Habitat."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "logements-vacants": None,
        "encadrement-loyers": None,
        "acces-logement": {
            "mesures": [
                "Construire des logements à taille humaine, durables et bien intégrés, conciliant confort de vie et transition écologique.",
                "Maîtriser le foncier pour limiter l'étalement urbain et favoriser un développement équilibré.",
                "Mettre en place un plan d'accompagnement des syndics bénévoles des copropriétés privées pour prévenir les impayés et les dégradations."
            ],
            "source": SOURCE, "sourceUrl": URL
        }
    },
    "education": {
        "petite-enfance": None,
        "ecoles-renovation": {
            "mesures": [
                "Construire une école publique à taille humaine et inclusive à La Bayot (quartier avec 650 logements réalisés).",
                "Désimperméabiliser les cours d'école pour lutter contre la chaleur urbaine."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "cantines-fournitures": {
            "mesures": [
                "Instaurer une restauration scolaire avec tarifs de 1 € à 4 € selon les ressources, avec alimentation bio, locale et durable."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "periscolaire-loisirs": {
            "mesures": [
                "Fixer un ratio d'1 adulte pour 10 enfants au périscolaire, avec formation et qualification renforcées des équipes.",
                "Garantir une heure de sport quotidienne pour chaque enfant avec des éducateurs sportifs dans toutes les écoles."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "jeunesse": {
            "mesures": [
                "Refondre le Contrat Municipal Étudiant pour doubler le nombre de bénéficiaires.",
                "Créer une classe à horaires aménagés théâtre au Conservatoire, dans une école en quartier prioritaire pour favoriser la mixité."
            ],
            "source": SOURCE, "sourceUrl": URL
        }
    },
    "environnement": {
        "espaces-verts": {
            "mesures": [
                "Planter des arbres en pleine terre sur les 7 places réaménagées et créer des espaces paysagers.",
                "Développer des jardins partagés dans les quartiers.",
                "Créer une coulée verte paysagère sous la ligne haute tension à Valence 2."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "proprete-dechets": {
            "mesures": [
                "Mettre en place la collecte des biodéchets dans chaque quartier."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "climat-adaptation": {
            "mesures": [
                "Créer des îlots de fraîcheur végétalisés pour lutter contre la chaleur urbaine.",
                "Installer des fontaines et brumisateurs dans les zones les plus exposées."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "renovation-energetique": {
            "mesures": [
                "Soutenir la rénovation énergétique des logements pour réduire les charges et la précarité énergétique."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "alimentation-durable": None
    },
    "sante": {
        "centres-sante": {
            "mesures": [
                "Créer 3 maisons de santé pluridisciplinaires réservées à l'accueil de nouveaux médecins.",
                "Lancer un plan d'attractivité pour les internes et professions de santé avec logements et aides à l'installation.",
                "Créer une permanence infirmière de proximité à 5 minutes de chez vous, en lien avec les Maisons Pour Tous.",
                "Reconvertir la Maison de l'Armée en pôle de santé pluridisciplinaire à l'entrée de la Promenade Maurice Clerc."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "prevention-sante": {
            "mesures": [
                "Afficher la qualité de l'air avec ATMO tous les jours.",
                "Soutenir les sages-femmes pour renforcer le suivi gynécologique."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "seniors": None
    },
    "democratie": {
        "budget-participatif": {
            "mesures": [
                "Organiser un référendum local sur le plan de mobilité.",
                "Mettre en place des concertations systématiques sur tous les projets d'urbanisme avec restitutions publiques obligatoires.",
                "Créer un comité indépendant chargé d'évaluer les projets portés par la municipalité.",
                "Déployer des questionnaires usagers réguliers pour évaluer les services municipaux."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "transparence": {
            "mesures": [
                "Lancer dès le premier mois deux audits (chauffage urbain, charges locatives) pour un état des lieux clair et partagé.",
                "Créer un comité consultatif des entreprises présidé par le Maire pour un dialogue permanent avec les acteurs économiques."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "vie-associative": {
            "mesures": [
                "Créer un service municipal dédié pour soutenir les associations dans la recherche de financements, la formation et la gestion.",
                "Accorder des dotations pluriannuelles indexées sur l'inflation aux centres sociaux.",
                "Rénover entièrement la Maison de la Vie Associative.",
                "Transformer la Maison Didier Guillaume en tiers-lieu avec bureaux et salles adaptées.",
                "Remettre en état les MJC Châteauvert et Grand Charran et la MPT du Plan.",
                "Renforcer l'autonomie des Maisons Pour Tous avec moyens accrus et ouvertures en soirée pour les jeunes.",
                "Créer une plateforme en ligne pour faciliter les missions bénévoles.",
                "Amplifier le Forum des associations avec la création d'un Prix de l'innovation sociale et environnementale."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "services-publics": {
            "mesures": [
                "Mettre en place des permanences de proximité (police, infirmière) dans les quartiers.",
                "Développer des tiers-lieux associatifs et favoriser l'installation de commerces en pied d'immeuble dans les quartiers."
            ],
            "source": SOURCE, "sourceUrl": URL
        }
    },
    "economie": {
        "commerce-local": {
            "mesures": [
                "Mobiliser la Foncière de Redynamisation pour faciliter la reprise des locaux vacants et préserver la diversité commerciale.",
                "Créer un plan dédié au commerce et à l'artisanat indépendant.",
                "Organiser des marchés de proximité dans les quartiers.",
                "Créer un marché alimentaire en circuit court devant le Parc de la Marquise.",
                "Revitaliser la rue Faventines et le faubourg Saint-Jacques pour soutenir les commerces.",
                "Créer un comité des fêtes présidé par un commerçant valentinois."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "emploi-insertion": {
            "mesures": [
                "Généraliser l'allotissement des marchés publics pour permettre aux TPE et PME locales de répondre plus facilement.",
                "Faciliter l'accès à des locaux adaptés pour les entreprises artisanales dans les quartiers.",
                "Créer un Office de l'Attractivité des entreprises (OAE) pour accompagner l'installation de nouvelles entreprises.",
                "Accompagner les 18-30 ans dans la création d'entreprises, notamment dans l'ESS et l'entrepreneuriat culturel.",
                "Développer des ateliers et chantiers d'insertion ainsi qu'une école de production pour les jeunes décrocheurs."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "attractivite": {
            "mesures": [
                "Aider les entreprises locales dans leur transition numérique, énergétique et RSE.",
                "Valoriser les talents valentinois pour faciliter leur insertion dans le tissu économique local."
            ],
            "source": SOURCE, "sourceUrl": URL
        }
    },
    "culture": {
        "equipements-culturels": {
            "mesures": [
                "Créer un département théâtre au Conservatoire de Valence.",
                "Maintenir le soutien aux scènes nationales pour une offre ambitieuse et accessible."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "evenements-creation": {
            "mesures": [
                "Déployer événements, spectacles et ateliers artistiques dans chaque quartier.",
                "Créer le festival « Le Souffle des beaux jours » de mai à septembre dans les parcs, du Parc de la Marquise au Parc Jean Perdrix."
            ],
            "source": SOURCE, "sourceUrl": URL
        }
    },
    "sport": {
        "equipements-sportifs": {
            "mesures": [
                "Réhabiliter la piscine Tournesol en équipement sportif et culturel.",
                "Construire une nouvelle piscine municipale et un pôle santé-sport sur l'ancien collège Rabelais."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "sport-pour-tous": {
            "mesures": [
                "Installer des city-stades inclusifs, parcours sportifs et équipements estivaux avec jeux d'eau dans tous les quartiers."
            ],
            "source": SOURCE, "sourceUrl": URL
        }
    },
    "urbanisme": {
        "amenagement-urbain": {
            "mesures": [
                "Réaménager 7 places emblématiques (Ferry, Algoud, Résistance, Montalivet, Jean Vilar, de la Paix, avenue de l'Yser) avec ombre, arbres, espaces enfants et marchés de quartier.",
                "Transformer Valence 2 en centralité vivante : commerces du quotidien, logements à taille humaine et parc habité.",
                "Transformer le boulevard Maurice Clerc en promenade végétalisée et conviviale avec terrasses, jeux et parcs à chiens sécurisés.",
                "Sécuriser le pôle bus par une réorganisation plus compacte, lisible et sécurisée."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "accessibilite": {
            "mesures": [
                "Réviser les aménagements non inclusifs, y compris l'escalier monumental.",
                "Garantir des cheminements continus et accessibles entre équipements publics, commerces et services.",
                "Créer un comité d'experts d'usage en situation de handicap consulté obligatoirement sur tous les projets d'aménagement."
            ],
            "source": SOURCE, "sourceUrl": URL
        },
        "quartiers-prioritaires": {
            "mesures": [
                "Développer des tiers-lieux associatifs et favoriser l'installation de commerces en pied d'immeuble dans les quartiers prioritaires.",
                "Ouvrir les MPT de Fontbarlettes et du Plan en soirée pour les jeunes."
            ],
            "source": SOURCE, "sourceUrl": URL
        }
    },
    "solidarite": {
        "aide-sociale": None,
        "egalite-discriminations": None,
        "pouvoir-achat": {
            "mesures": [
                "Financer l'ensemble du projet sans hausse d'impôts, par redéploiement des charges de fonctionnement existantes.",
                "Investir 70 millions d'euros sur l'ensemble du mandat, un projet ambitieux et financé."
            ],
            "source": SOURCE, "sourceUrl": URL
        }
    }
}

# --- Intégrer dans le JSON ---
count = 0
for cat in data["categories"]:
    cat_id = cat["id"]
    if cat_id not in PROPS:
        continue
    for st in cat["sousThemes"]:
        st_id = st["id"]
        if st_id in PROPS[cat_id]:
            prop = PROPS[cat_id][st_id]
            if prop is not None:
                st["propositions"]["boyadjian"] = prop
                count += len(prop["mesures"])

print(f"✓ {count} mesures intégrées pour Boyadjian")

# --- Sauvegarder ---
with open(ELECTION_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"✓ {ELECTION_PATH} sauvegardé")
