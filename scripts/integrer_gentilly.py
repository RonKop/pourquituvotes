#!/usr/bin/env python3
"""Intègre les 3 candidats de Gentilly dans gentilly-2026.json"""
import json, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELECTION_PATH = os.path.join(BASE, "data", "elections", "gentilly-2026.json")
VILLES_PATH = os.path.join(BASE, "data", "villes.json")

# Charger le fichier existant (Crespin uniquement)
with open(ELECTION_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Ajouter les candidats manquants ---
existing_ids = {c["id"] for c in data["candidats"]}

new_candidats = [
    {
        "id": "aggoune",
        "nom": "Fatah Aggoune",
        "liste": "Gentilly cœur battant",
        "programmeUrl": None,
        "programmeComplet": False,
        "programmePdfPath": None
    },
    {
        "id": "godard",
        "nom": "Thomas Godard",
        "liste": "Gentilly Respire",
        "programmeUrl": "https://gentillyrespire.fr/",
        "programmeComplet": True,
        "programmePdfPath": None
    }
]

for c in new_candidats:
    if c["id"] not in existing_ids:
        data["candidats"].append(c)
        print(f"+ Candidat ajouté : {c['nom']}")

# Réordonner : aggoune, crespin, godard (alphabétique)
data["candidats"].sort(key=lambda c: c["id"])

# --- Propositions Godard ---
GODARD_PROPS = {
    "securite": {
        "police-municipale": {
            "mesures": [
                "Recruter des gardes urbains agissant en binômes sur des secteurs d'intervention privilégiés, assurant des missions de prévention et de médiation.",
                "Coordonner l'action des différents acteurs (ASVP, services municipaux) dans la gestion des infractions sur l'espace public.",
                "Permettre au maire de prononcer des rappels à l'ordre et développer les travaux d'intérêt général (TIG) dans les services municipaux."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "videoprotection": {
            "mesures": [
                "Évaluer l'efficacité du système de vidéosurveillance actuel pour le faire évoluer si besoin."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "prevention-mediation": {
            "mesures": [
                "Lutter et sensibiliser contre les incivilités dans l'espace public.",
                "Créer des liens de confiance entre gardes urbains et résidents, gardiens et bailleurs.",
                "Engager des actions de sensibilisation au collège et au lycée contre l'usage du protoxyde d'azote et des stupéfiants.",
                "Rejoindre l'association des maires qui agissent contre le narcotrafic lancée par Amine Kessaci.",
                "Développer des dispositifs de soutien pour les parents de jeunes engagés dans un parcours délinquant.",
                "Lutter contre le bruit environnant avec une cartographie du bruit en ville et rechercher des solutions pratiques."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "violences-femmes": {
            "mesures": [
                "Créer un accueil intercommunal pour les femmes victimes de violences conjugales.",
                "Renforcer la formation des personnels municipaux aux violences sexistes et sexuelles (VSS)."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        }
    },
    "transports": {
        "transports-en-commun": None,
        "velo-mobilites-douces": {
            "mesures": [
                "Élaborer un plan vélo et mener des actions urgentes pour sécuriser les cyclistes, notamment aux carrefours dangereux.",
                "Aménager des pistes cyclables sécurisées : en urgence la traversée Est-Ouest (Paul Vaillant Couturier - Jean Jaurès).",
                "Développer le stationnement vélo sécurisé (parking vélo fermé).",
                "S'assurer que tous les enfants sachent faire du vélo en fin de primaire."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "pietons-circulation": {
            "mesures": [
                "Créer une zone à faible trafic en centre-ville pour encourager les déplacements à pied.",
                "Aménager des parcours piétonniers accompagnés d'équipements (bancs, points d'eau, sanitaires publics).",
                "Abaisser le flux des véhicules traversant Gentilly pour apaiser la circulation.",
                "Passer la ville à 30 km/h partout pour limiter la vitesse et diminuer la pollution.",
                "Apaiser les abords des écoles avec des rues aux enfants fermées à la circulation et végétalisées.",
                "Sécuriser les déplacements de nuit par des cheminements piétonniers illuminés.",
                "Améliorer les conditions de déplacements pour les personnes à mobilité réduite."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "stationnement": None,
        "tarifs-gratuite": None
    },
    "logement": {
        "logement-social": {
            "mesures": [
                "Mettre en place avec Valdevy et CDC Habitat une convention d'objectifs et suivre les préconisations de l'ANCOLS.",
                "Créer une régie locale dans chaque quartier pour offrir un logement digne à tous.",
                "Étudier la sortie de Valdevy en cas de manquements répétés pour se rapprocher d'un bailleur social solide.",
                "Garantir la transparence dans l'attribution des logements sociaux avec des critères strictement définis.",
                "Faire adhérer Valdevy à la bourse d'échange d'Île-de-France « Échanger Habiter ».",
                "Apporter une aide au déménagement des locataires âgés ou en difficulté.",
                "Inciter les bailleurs sociaux à réaliser des résidences intergénérationnelles et des colocations pour familles monoparentales.",
                "Transformer des rez-de-chaussée d'immeubles sociaux en locaux d'activités ou associatifs.",
                "Exiger la rénovation énergétique urgente des logements sociaux via un comité de suivi.",
                "Équiper les logements sociaux de volets pour lutter contre la chaleur et le froid."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "logements-vacants": None,
        "encadrement-loyers": None,
        "acces-logement": {
            "mesures": [
                "Soutenir l'accession sociale à la propriété avec le bail réel solidaire (BRS).",
                "Imposer aux promoteurs des baux solidaires et des prix maîtrisés pour les primo-accédants.",
                "Autoriser la construction de logements à taille humaine en régulant la hauteur des bâtiments."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        }
    },
    "education": {
        "petite-enfance": {
            "mesures": [
                "Ouvrir une crèche multi-accueil avec amplitude horaire élargie et différents types d'accueil.",
                "Réserver un quota de places en crèche pour les enfants de familles monoparentales ou en situation de handicap.",
                "Créer une halte-garderie offrant un droit au répit aux familles monoparentales.",
                "Mettre en place un lieu d'accueil dédié aux parents (écoute, partage, accompagnement)."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "ecoles-renovation": {
            "mesures": [
                "Rénover la Maison de l'enfance et revoir l'organisation autour de ce lieu d'accueil unique.",
                "Accélérer les travaux d'isolation dans les écoles et transformer les cours en cours oasis.",
                "Créer un conseil de vie scolaire réunissant enseignants, animateurs, services de la ville et associations."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "cantines-fournitures": {
            "mesures": [
                "Revoir l'approvisionnement des cuisines avec des marchés réguliers avec des producteurs locaux et bio.",
                "Améliorer l'offre végétarienne et proposer du pain de qualité dans les cantines.",
                "Stopper l'utilisation de plastiques et de produits transformés dans la restauration scolaire.",
                "Réduire le gaspillage alimentaire en adaptant les quantités selon les âges.",
                "Renforcer la commission menus et étudier la création d'une cuisine autonome pour les écoles et l'EHPAD."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "periscolaire-loisirs": {
            "mesures": [
                "Mieux adapter les rythmes scolaires aux temps d'apprentissage des enfants.",
                "Garantir une offre périscolaire riche avec des associations culturelles et sportives reconnues.",
                "Former et professionnaliser les animateurs et recruter des encadrants qualifiés.",
                "Renforcer l'aide aux devoirs avec des études dirigées et du matériel pédagogique innovant.",
                "Sensibiliser contre les discriminations, la surexposition aux écrans et former des enfants à la médiation.",
                "Renforcer la place des arts et de la culture à l'école avec des interventions d'artistes."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "jeunesse": {
            "mesures": [
                "Redynamiser le Point J et recruter des encadrants qualifiés pour les jeunes.",
                "Créer un service de mentorat municipal pour les jeunes en recherche de stage ou d'orientation.",
                "Améliorer l'information sur les droits des 16-18 ans via des stands itinérants.",
                "Mettre en place un dispositif « Argent de poche » pour les 14-17 ans : missions d'intérêt général contre indemnisation.",
                "Installer un Conseil Municipal des Jeunes (CMJ) doté d'un budget propre.",
                "Créer un espace jeunes dédié dans l'ancien collège Pierre-Curie."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        }
    },
    "environnement": {
        "espaces-verts": {
            "mesures": [
                "Lancer un plan arbres massif : inventorier, protéger et renforcer la présence d'arbres sur les sites clés.",
                "Planter en priorité 200 arbres sur les deux stades, véritables îlots de chaleur.",
                "Créer des chemins de fraîcheur en arborant les rues.",
                "Développer le corridor vert de la Bièvre comme corridor de biodiversité et poumon vert.",
                "Modifier le PLUi pour imposer une bande non constructible le long de la Bièvre.",
                "Rendre obligatoire la préservation des grands arbres existants au sein des parcelles privées.",
                "Préserver l'îlot Paix-Reims comme poumon vert et y créer une ferme pédagogique.",
                "Organiser des potagers de pieds d'immeuble et des composts collectifs."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "proprete-dechets": {
            "mesures": [
                "Verbaliser les contrevenants pour dépôts sauvages, véhicules épaves et nuisances.",
                "Sensibiliser les habitants à la gestion des ordures ménagères avec les associations."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "climat-adaptation": {
            "mesures": [
                "Créer des îlots refuges dans les parcs et cours d'école pour l'été via la végétalisation.",
                "Inclure une salle refuge pour les seniors dans les écoles l'été lors de la rénovation thermique."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "renovation-energetique": {
            "mesures": [
                "Accélérer la rénovation thermique des bâtiments municipaux en commençant par les écoles.",
                "Privilégier la ventilation naturelle, les énergies renouvelables et le réemploi de matériaux biosourcés.",
                "Créer un point d'accueil municipal sur les travaux d'isolation et les aides financières mobilisables."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "alimentation-durable": {
            "mesures": [
                "Renforcer l'éducation alimentaire sur les bienfaits d'une alimentation saine pour la santé."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        }
    },
    "sante": {
        "centres-sante": None,
        "prevention-sante": {
            "mesures": [
                "Développer un parcours sport-santé et un parcours running dans la ville.",
                "S'assurer que tous les enfants sachent nager et courir en fin de primaire."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "seniors": {
            "mesures": [
                "Augmenter l'offre de loisirs « Tournesol » pour les anciens à des prix abordables.",
                "Développer le logement intergénérationnel ou l'entraide entre étudiants et personnes âgées.",
                "Repérer les personnes isolées et fragilisées avec des associations et bénévoles."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        }
    },
    "democratie": {
        "budget-participatif": {
            "mesures": [
                "Instaurer des consultations citoyennes sous forme de référendums ou conventions citoyennes.",
                "Mettre en place le tirage au sort des citoyens pour chaque consultation.",
                "Lancer des consultations citoyennes sur trois sites à enjeu fort."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "transparence": {
            "mesures": [
                "Organiser un compte-rendu annuel de mandat ouvert aux habitants.",
                "Faire signer aux élus la charte anticorruption Anticor.",
                "Limiter les délégations permettant au Maire de décider seul.",
                "Donner aux adjoints des délégations aux périmètres clairement définis.",
                "Garantir la transparence des rémunérations et frais des élus.",
                "Favoriser l'ouverture des données publiques (open data) sur le site de la Mairie.",
                "Garantir les droits de l'opposition et son information en temps et en heure.",
                "Donner un droit d'interpellation des citoyens au Conseil municipal."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "vie-associative": {
            "mesures": [
                "Convertir les anciens ateliers de l'îlot Paix-Reims en Maison des Associations.",
                "Créer un conseil des associations autonome avec une charte d'engagements réciproques.",
                "Attribuer les subventions avec transparence sur la base de critères travaillés avec le conseil.",
                "Privilégier les conventions pluriannuelles d'objectifs et de moyens pour les associations.",
                "Ouvrir un café associatif pour créer un lieu de convivialité."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "services-publics": {
            "mesures": [
                "Faciliter l'accès à l'administration avec un organigramme clair et un site internet repensé.",
                "Garantir une réponse aux demandes des Gentilléens dans un délai imparti.",
                "Donner plus d'initiatives aux agents municipaux vis-à-vis des demandes des habitants.",
                "Favoriser la montée en compétences et le bien-être au travail des agents municipaux.",
                "Former l'ensemble des personnels municipaux à l'accueil de tous les publics.",
                "Veiller à ce que les formulaires municipaux prennent en compte toutes les familles.",
                "Réduire le nombre de Conseils de quartier à 4 ou 5 pour renforcer leur rôle.",
                "Créer un Conseil des étrangers pour associer aux décisions les résidents sans droit de vote.",
                "Créer une maison de la citoyenneté dans l'ancien centre culturel."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        }
    },
    "economie": {
        "commerce-local": {
            "mesures": [
                "Accompagner une dynamique commerciale autour d'un centre-ville attractif et embelli.",
                "Encourager l'implantation d'activités diversifiées, culturelles ou associatives.",
                "Utiliser le droit de préemption des locaux commerciaux pour maîtriser le choix des commerces.",
                "Lutter contre la vacance commerciale en accompagnant les porteurs de projet.",
                "Permettre l'ouverture de boutiques éphémères pour les créateurs et entrepreneurs locaux."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "emploi-insertion": {
            "mesures": [
                "Créer un lieu d'Économie Sociale et Solidaire (ESS) dans l'ancien collège Pierre-Curie.",
                "Faciliter l'installation de petites entreprises grâce à des baux avantageux dans des locaux municipaux.",
                "Réserver des espaces dédiés aux micro-entreprises avec aide administrative et coworking.",
                "Faciliter l'accès des porteurs de projet aux formations du Grand-Orly Seine Bièvre.",
                "Inciter l'implantation de projets ESS dans les bâtiments de bureaux vides."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "attractivite": None
    },
    "culture": {
        "equipements-culturels": {
            "mesures": [
                "Créer l'Université populaire gentilléenne en s'appuyant sur les universitaires locaux.",
                "Établir des critères équitables et transparents dans l'attribution des ateliers d'artistes.",
                "Maintenir les activités artistiques et culturelles dans l'ancien collège Pierre-Curie."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "evenements-creation": {
            "mesures": [
                "Créer un chèque culture municipal pour tous les collégiens.",
                "Multiplier les opérations culture ouverte avec les bailleurs sociaux.",
                "Initier une Fête du livre associant les acteurs locaux.",
                "Développer les actions d'éducation à l'image en lien avec la Maison Doisneau.",
                "Mettre en valeur le patrimoine historique de Gentilly avec un parcours historique.",
                "Mettre en place un projet artistique inter-écoles complet.",
                "Mettre en valeur la diversité des langues parlées à Gentilly avec une semaine culturelle."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        }
    },
    "sport": {
        "equipements-sportifs": {
            "mesures": [
                "Rénover le Stade Maurice Baquet.",
                "Ouvrir des équipements pour une pratique sportive libre toute l'année (Basket 3x3, Foot 5x5)."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "sport-pour-tous": {
            "mesures": [
                "Créer une aide financière à l'inscription sportive pour les familles modestes.",
                "Soutenir la création d'un club handisport à Gentilly.",
                "Garantir le partage équitable des installations sportives entre garçons et filles.",
                "Améliorer la compétitivité des clubs en favorisant les ententes avec les villes voisines.",
                "Débloquer des financements favorisant la professionnalisation du mouvement sportif."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        }
    },
    "urbanisme": {
        "amenagement-urbain": {
            "mesures": [
                "Revoir les orientations du PLUi pour rééquilibrer l'espace construit avec la protection du patrimoine.",
                "Arrêter la construction de résidences services qui ne bénéficient pas aux Gentilléens.",
                "Améliorer les espaces extérieurs avec des jeux pour les enfants et des équipements sportifs.",
                "Créer un groupe référent d'habitants dans chaque quartier pour suivre les projets urbains."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "accessibilite": {
            "mesures": [
                "Améliorer les déplacements des personnes à mobilité réduite (trottoirs, bancs publics)."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "quartiers-prioritaires": {
            "mesures": [
                "Revitaliser les 5 grandes cités grâce à des assemblées de quartier régulières."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        }
    },
    "solidarite": {
        "aide-sociale": {
            "mesures": [
                "Créer une carte parent solo avec tarification différenciée pour crèches, cantines et périscolaire.",
                "Accompagner les familles monoparentales pour l'accès au logement et aux soins.",
                "Créer un guichet unique pour les démarches administratives, viser un territoire zéro non-recours.",
                "Garantir une sécurité alimentaire avec les associations et soutenir une épicerie solidaire.",
                "Mieux accompagner les allocataires des minima sociaux avec le CCAS.",
                "Garantir la domiciliation des exilés et précaires avec un service de bagagerie solidaire.",
                "Créer un service d'aide à la parentalité."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "egalite-discriminations": {
            "mesures": [
                "Lutter contre toutes les discriminations en collaboration avec les associations.",
                "Former une commune antiraciste, féministe et inclusive."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        },
        "pouvoir-achat": {
            "mesures": [
                "Stopper l'augmentation de la taxe foncière.",
                "Réduire l'endettement et les coûts de fonctionnement sur toute la mandature.",
                "Mettre en place un Plan pluriannuel d'investissement.",
                "Rechercher systématiquement des cofinancements pour tout nouveau projet.",
                "Favoriser les dépenses partagées avec les villes voisines.",
                "Soutenir les réseaux de voisinage et de solidarité locale.",
                "Expérimenter l'heure civique : une heure par mois donnée à une action de solidarité."
            ],
            "source": "Programme officiel 2026",
            "sourceUrl": "https://gentillyrespire.fr/"
        }
    }
}

# --- Intégrer Godard dans chaque sous-thème ---
godard_count = 0
for cat in data["categories"]:
    cat_id = cat["id"]
    if cat_id not in GODARD_PROPS:
        continue
    for st in cat["sousThemes"]:
        st_id = st["id"]
        if st_id in GODARD_PROPS[cat_id]:
            prop = GODARD_PROPS[cat_id][st_id]
            if prop is not None:
                st["propositions"]["godard"] = prop
                godard_count += len(prop["mesures"])
            # Si None, on ne met rien (pas de clé godard)

print(f"+ Godard : {godard_count} mesures intégrées")

# Compter Crespin
crespin_count = 0
for cat in data["categories"]:
    for st in cat["sousThemes"]:
        if "crespin" in st["propositions"] and st["propositions"]["crespin"] is not None:
            crespin_count += len(st["propositions"]["crespin"]["mesures"])

print(f"  Crespin : {crespin_count} mesures (existantes)")
print(f"  Aggoune : 0 mesures (pas de programme)")

# --- Sauvegarder ---
with open(ELECTION_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\n✓ {ELECTION_PATH} sauvegardé")

# --- Mettre à jour villes.json ---
with open(VILLES_PATH, "r", encoding="utf-8") as f:
    villes = json.load(f)

# Calculer stats
total_props = godard_count + crespin_count
themes_with_props = set()
for cat in data["categories"]:
    for st in cat["sousThemes"]:
        for cand_id, prop in st["propositions"].items():
            if prop is not None and len(prop.get("mesures", [])) > 0:
                themes_with_props.add(cat["id"])

complets = sum(1 for c in data["candidats"] if c.get("programmeComplet"))

gentilly_entry = {
    "id": "gentilly",
    "nom": "Gentilly",
    "codePostal": "94250",
    "departement": "94",
    "elections": ["gentilly-2026"],
    "stats": {
        "candidats": len(data["candidats"]),
        "propositions": total_props,
        "themes": len(themes_with_props),
        "complets": complets
    },
    "candidats": [
        {"id": c["id"], "nom": c["nom"], "liste": c["liste"]}
        for c in data["candidats"]
    ],
    "derniereMaj": "2026-03-04"
}

# Vérifier si Gentilly existe déjà
existing_idx = None
for i, v in enumerate(villes):
    if v["id"] == "gentilly":
        existing_idx = i
        break

if existing_idx is not None:
    villes[existing_idx] = gentilly_entry
    print("✓ Gentilly mis à jour dans villes.json")
else:
    # Insérer en ordre alphabétique
    inserted = False
    for i, v in enumerate(villes):
        if v["id"] > "gentilly":
            villes.insert(i, gentilly_entry)
            inserted = True
            break
    if not inserted:
        villes.append(gentilly_entry)
    print("✓ Gentilly ajouté dans villes.json")

with open(VILLES_PATH, "w", encoding="utf-8") as f:
    json.dump(villes, f, ensure_ascii=False, indent=2)

print(f"\nStats Gentilly : {len(data['candidats'])} candidats, {total_props} propositions, {len(themes_with_props)} thèmes, {complets} complets")
