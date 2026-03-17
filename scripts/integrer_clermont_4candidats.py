#!/usr/bin/env python3
"""Intègre les programmes de Bony, Darbois, Maximi et Cartailler dans clermont-2026.json."""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

JSON_PATH = r"C:\Users\KOPELMANRon\projets perso\FR comp mun\data\elections\clermont-2026.json"

# ── Mapping: candidat_id -> {sous_theme_id: [mesures]} ──

BONY_SOURCE = "Programme officiel"
BONY_URL = "https://bony2026.fr"

bony = {
    "police-municipale": [
        "Extension des horaires de présence de la police municipale la nuit",
        "+100 postes supplémentaires de policiers municipaux",
        "Armement et équipement complet de la police municipale",
        "Renforcement de la brigade canine",
        "Création d'un hôtel de police municipal adapté intégrant un Centre de Supervision Urbain opérationnel 24h/24",
        "Renforcement de la coopération avec l'État (police nationale, procureur)",
        "Création d'une brigade transports et de boutons d'alerte digitaux",
    ],
    "videoprotection": [
        "Espace public entièrement vidéoprotégé",
        "Installation de bornes d'appel d'urgence dans les secteurs sensibles",
    ],
    "prevention-mediation": [
        "Expulsion des logements sociaux des auteurs de troubles graves à l'ordre public et en lien avec le narcotrafic",
        "Sécurisation des abords des établissements scolaires et des crèches",
        "Mise en place d'un système d'alerte anti-intrusion dans toutes les écoles",
        "Lutter contre les cambriolages : mise en œuvre d'opérations Tranquillité Vacances",
        "Saisie systématique puis destruction des véhicules débridés utilisés lors de rodéos urbains",
        "En cas d'urgence, couvre-feu pour les mineurs de moins de 16 ans non accompagnés",
        "Fermeture des épiceries à 22h par arrêté municipal",
        "Rallumage de l'éclairage public partout et toute la nuit",
        "Mise en place d'heures de Travaux d'Intérêt Général pour responsabiliser. Celui qui dégrade, paie ou répare",
    ],
    "violences-femmes": [
        "Élargissement de l'arrêt à la demande après 20h pour les femmes dans les transports",
        "Déploiement du dispositif « Angela », favorisant la protection des femmes",
    ],
    "transports-en-commun": [
        "Lancement d'une étude pour remplacer le tramway et améliorer la ligne A à l'horizon 2035",
        "Favoriser l'intermodalité en déplaçant la gare routière",
        "Renforcement du dispositif BEN bus de nuit pour les étudiants",
    ],
    "velo-mobilites-douces": [
        "Augmentation du nombre de vélos en libre-service à assistance électrique",
        "Aide municipale pour l'achat de vélos à assistance électrique",
        "Accélération de la construction de garages sécurisés pour les vélos",
    ],
    "pietons-circulation": [
        "Assouplissement du plan de circulation pour améliorer la fluidité",
        "Suppression de la zone à trafic limité",
        "Réouverture des grands axes précédemment fermés (Carnot, Bergougnan, Libération, Mitterrand, Oradou)",
        "Rénovation des trottoirs, des parcours piétons et du mobilier urbain",
    ],
    "stationnement": [
        "Facilités de circulation et de stationnement pour les professionnels de santé",
        "30 premières minutes de stationnement gratuites",
        "Modernisation générale du parc des horodateurs",
        "Retour du forfait jour pour la tarification du stationnement résidentiel",
        "Création de parkings aériens végétalisés (Salins, Montferrand)",
        "Signalétique dynamique des parkings, rues commerçantes et sites culturels/touristiques",
    ],
    "tarifs-gratuite": [
        "Tarification famille des transports en commun (dégressif suivant nombre d'enfants)",
        "Mise en place d'un Pass-Sénior de -50% pour les +65 ans",
        "Mise en place d'un pass métropolitain pour les jeunes",
    ],
    "logement-social": [
        "Mise en place d'un dispositif d'aide au logement contre engagement citoyen pour étudiants",
    ],
    "logements-vacants": [
        "Réserve foncière pour entreprises et logement accessible",
    ],
    "acces-logement": [
        "Lutter contre l'habitat indigne avec la création d'une charte municipale dédiée",
    ],
    "petite-enfance": [
        "Construction de 2 nouvelles crèches",
        "Ouverture d'une crèche parentale à Montferrand",
    ],
    "ecoles-renovation": [
        "Garantie de la présence d'un ATSEM par classe",
        "Mise en œuvre de l'accessibilité totale dans l'ensemble des écoles",
    ],
    "cantines-fournitures": [
        "Mise en place de petits-déjeuners de produits locaux dans les écoles",
    ],
    "periscolaire-loisirs": [
        "Mise en place d'un service municipal de soutien scolaire",
        "Création d'un « Carrefour des Parents » pour accompagner la parentalité",
    ],
    "jeunesse": [
        "Développement de chantiers éducatifs à destination des jeunes et renforcement de l'École de la deuxième chance",
        "Mise en place de bourses au mérite pour les jeunes",
        "Aides financières pour l'obtention du permis de conduire pour les jeunes de moins de 26 ans",
        "Ouverture d'un centre d'accueil en gare pour étudiants internationaux",
    ],
    "espaces-verts": [
        "Plantation de 10 000 arbres",
        "Végétalisation des grandes places publiques (Jaude)",
        "Mise en valeur de la Tiretaine dans les projets urbains",
    ],
    "proprete-dechets": [
        "Amélioration de la propreté, de la sécurité et de l'accessibilité du centre-ville",
    ],
    "climat-adaptation": [
        "Aides financières aux particuliers pour récupérateurs d'eau",
        "Conversion intégrale de l'éclairage public en LED",
    ],
    "renovation-energetique": [
        "Rénovation thermique des bâtiments publics",
        "Panneaux photovoltaïques sur bâtiments municipaux",
    ],
    "centres-sante": [
        "Soutien aux maisons de santé pluridisciplinaires",
        "Création de box de téléconsultation dans les maisons de quartier et centres sociaux",
        "Déploiement d'un service mobile associant soins et accès aux droits dans les quartiers prioritaires",
    ],
    "seniors": [
        "Création d'une \"Maison des Aidants\" permettant aux proches de bénéficier de temps de répit",
    ],
    "transparence": [
        "Transparence dans le système d'attribution des subventions municipales",
        "Transparence municipale avec la publication des frais de mandat",
        "Fin du cumul des fonctions de maire et de président de la métropole",
        "Réduction du nombre d'adjoints au maire et baisse des indemnités allouées aux élus",
        "Réduction du train de vie de la municipalité",
        "Limitation stricte à deux mandats non-électifs rémunérés",
        "Bulletin municipal digital envoyé par mail",
        "Réduction du train de vie municipal / gains d'efficience (doublons ville-métropole)",
    ],
    "budget-participatif": [
        "Création d'une assemblée citoyenne tirée au sort",
    ],
    "vie-associative": [
        "Création d'une maison des associations",
        "Création d'une réserve communale (bénévolat, soutien scolaire, agents aidant les enfants)",
    ],
    "commerce-local": [
        "Création d'un Office municipal du commerce et de l'artisanat",
        "Utilisation renforcée du droit de préemption pour réduire la vacance commerciale",
        "Mise en place de boutiques test pour accompagner les jeunes entreprises et l'artisanat",
        "Rénovation des marchés Saint-Joseph et Saint-Pierre",
        "Programmation régulière d'animations et d'événements dans les rues commerçantes",
    ],
    "emploi-insertion": [
        "Faciliter l'accès des entreprises locales aux marchés publics",
        "Conférence économique métropolitaine",
    ],
    "attractivite": [
        "Marque territoriale + rattachement bureau des congrès",
        "Développement d'un parcours touristique reliant centre-ville et Montferrand",
        "Installation de l'antenne Office du tourisme du musée Quillot à la Maison de l'Apothicaire",
    ],
    "equipements-culturels": [
        "Création d'un musée consacré à Blaise Pascal",
        "Reconversion de l'ancienne prison en Maison des Illustres",
        "Mise en valeur du patrimoine religieux",
        "Dynamisation des trois musées par des expositions nationales",
        "Création d'un centre d'interprétation de l'art médiéval à Montferrand",
        "Relance et dynamisation de la Halle aux toiles",
    ],
    "evenements-creation": [
        "Création d'une biennale internationale de la sculpture",
        "Organisation d'un festival de street art",
        "Programmation municipale d'une saison théâtrale à prix accessibles",
    ],
    "equipements-sportifs": [
        "Rénovation et modernisation des équipements sportifs de quartier",
        "Abandon des phases 3 et 4 du projet d'extension du grand stade",
    ],
    "sport-pour-tous": [
        "Création de parcours de santé accessibles dans toute la ville",
        "Organisation d'une grande fête populaire du sport",
        "Création d'un marathon métropolitain",
    ],
    "amenagement-urbain": [
        "Redéfinition du projet de rénovation de la place Delille",
        "Rénovation de la rue et de la place de la Rodade à Montferrand",
    ],
    "accessibilite": [
        "Développement des bandes podotactiles et feux sonores pour les personnes malvoyantes",
        "Amélioration de l'accessibilité de l'espace public pour les personnes à mobilité réduite",
        "Installation de toilettes sur l'espace public accessibles aux PMR",
    ],
    "aide-sociale": [
        "Mise en place d'un Conseil des droits et devoirs des familles, conditionnalité des aides municipales",
        "Accompagnement des mamans isolées",
        "Mise en œuvre du plan de redressement du CCAS",
        "Mise en place d'un guichet unique de l'urgence sociale",
    ],
    "pouvoir-achat": [
        "Aucune hausse des taux municipaux de taxe foncière",
        "Maîtrise de la fiscalité locale pour préserver le pouvoir d'achat des habitants",
    ],
}

DARBOIS_SOURCE = "Radio RVA"
DARBOIS_URL = "https://www.radiorva.com/news/locales/23183/municipales-a-clermont-ferrand-les-propositions-d-antoine-darbois-candidat-remettre-clermont-en-ordre"

darbois = {
    "police-municipale": [
        "Recruter 100 policiers municipaux (objectif 150 formés et armés)",
        "Protection policière 24h/24, 7j/7",
        "Recruter 15-20 policiers municipaux dès les premiers mois",
        "Modifier le système d'indemnisation pour aligner les salaires de la police municipale",
    ],
    "videoprotection": [
        "Doubler les moyens de vidéoprotection",
    ],
    "prevention-mediation": [
        "Rétablir l'éclairage nocturne",
    ],
    "pietons-circulation": [
        "Corriger les erreurs du projet InspiRe en révisant le plan de circulation",
        "Adapter les règles de la ZTL",
    ],
    "amenagement-urbain": [
        "Interpréter le PLU de manière moins bureaucratique",
        "Reconversion des friches industrielles",
    ],
    "aide-sociale": [
        "Restaurer une gestion saine du CCAS",
    ],
    "centres-sante": [
        "Créer trois nouvelles maisons de santé",
    ],
    "ecoles-renovation": [
        "Assurer la présence d'une ATSEM par classe de maternelle",
    ],
    "seniors": [
        "Créer des places supplémentaires en EHPAD",
    ],
    "pouvoir-achat": [
        "Ne pas augmenter les dépenses de fonctionnement",
        "Ne pas augmenter les taux d'impôts locaux",
        "Résorber le surendettement",
    ],
    "emploi-insertion": [
        "Développer des technopoles sur les technologies nouvelles",
    ],
    "equipements-culturels": [
        "Créer un musée Blaise Pascal",
    ],
    "evenements-creation": [
        "Organiser un festival traditionnel auvergnat en centre-ville",
    ],
    "climat-adaptation": [
        "Poursuivre les plans de transition écologique en cours",
    ],
    "services-publics": [
        "Plan pour réduire les accidents du travail parmi les agents municipaux",
    ],
}

MAXIMI_SOURCE = "Programme officiel"
MAXIMI_URL = "https://mariannemaximi2026.fr/le-programme/"

maximi = {
    "cantines-fournitures": [
        "Gratuité des cantines scolaires pour tous les élèves",
        "Fournir un kit de rentrée à chaque élève",
    ],
    "periscolaire-loisirs": [
        "Davantage d'accompagnement dans les accueils périscolaires",
    ],
    "ecoles-renovation": [
        "S'opposer aux fermetures de classe",
    ],
    "logement-social": [
        "Construire des logements sociaux à bas loyer",
        "Mettre fin au clientélisme dans les attributions de logements sociaux",
        "Développer les pensions de famille",
    ],
    "encadrement-loyers": [
        "Encadrer les loyers sur l'ensemble de la ville",
        "Lutter contre les abus d'Airbnb",
    ],
    "acces-logement": [
        "Plan \"zéro enfants à la rue\" par réquisition de bâtiments vides",
    ],
    "climat-adaptation": [
        "Gratuité des premiers mètres cube d'eau",
        "Installer des récupérateurs d'eaux pluviales",
        "Favoriser l'installation de fontaines à eau potable publiques",
        "Mettre en place une régie publique de l'énergie",
    ],
    "renovation-energetique": [
        "Développer un parc photovoltaïque sur bâtiments municipaux",
    ],
    "proprete-dechets": [
        "Sortir de la dépendance des multinationales des déchets",
        "Moratoire sur l'augmentation du tonnage de l'incinérateur",
    ],
    "tarifs-gratuite": [
        "Gratuité complète des transports en commun pour tous",
    ],
    "transports-en-commun": [
        "Harmoniser les niveaux de service et amplitudes horaires",
        "Intégrer au PLUi le principe \"habitat/travail/loisirs à moins de 20 minutes\"",
        "Limiter les ruptures de correspondance",
    ],
    "centres-sante": [
        "Développer les centres de santé pluridisciplinaires",
        "S'opposer aux fermetures de services au CHU",
        "Instaurer une mutuelle municipale",
        "Créer un centre de santé municipale spécialisé en santé mentale",
    ],
    "prevention-sante": [
        "Prise en charge spécifique des problématiques féminines",
        "Campagnes de prévention (IST, VIH, consentement)",
    ],
    "aide-sociale": [
        "Carte municipale \"famille monoparentale\"",
        "Accès prioritaire aux crèches pour mères isolées",
        "Accès prioritaire au logement social et centres de santé",
        "Créer un service public funéraire",
    ],
    "accessibilite": [
        "Développer les toilettes publiques accessibles",
        "Acquérir des fauteuils handisport dans écoles et équipements sportifs",
    ],
    "egalite-discriminations": [
        "Créer un service public local d'accompagnement des résidents étrangers",
        "Jumeler Clermont-Ferrand avec une ville palestinienne",
    ],
    "vie-associative": [
        "Soutenir les associations via subventions pluriannuelles",
    ],
    "commerce-local": [
        "Défense du commerce local",
    ],
    "emploi-insertion": [
        "Priorité à l'emploi territorial",
    ],
    "videoprotection": [
        "Opposition à la vidéosurveillance",
    ],
}

CARTAILLER_SOURCE = "Programme officiel"
CARTAILLER_URL = "https://lereveilclermontois.fr/programme/"

cartailler = {
    "police-municipale": [
        "Recruter 30 policiers municipaux immédiatement, puis 10 par an",
        "Présence renforcée 7j/7 sur le terrain",
        "Structurer la prévention et renforcer les partenariats avec l'État",
        "Cellule anti-narcotrafic locale",
        "Élargir le pilotage territorial via CLSPD et CMSPD Métropolitain",
        "Publier annuellement un plan d'action chiffré et évalué",
    ],
    "emploi-insertion": [
        "Créer un Forum Économique Métropolitain",
        "Conciergerie Économique Métropolitaine (guichet unique)",
        "Commande publique locale avec clauses RSE obligatoires",
    ],
    "commerce-local": [
        "Étendre la monnaie locale \"La DOUME\"",
        "Créer un Observatoire du commerce",
        "Préemption stratégique pour locaux vacants",
        "Boutiques à l'essai",
        "Festival commerçant Place de la Rodade",
        "Tester Tram-Fret et Bus-Fret pour livraisons",
    ],
    "services-publics": [
        "Hébergement numérique en France",
    ],
    "pietons-circulation": [
        "Révision du plan de mobilité par consultations citoyennes",
        "Autoriser les professionnels de santé à circuler partout",
        "Droit à la mobilité garanti pour artisans et soignants",
        "\"Cockpit public des mobilités\"",
    ],
    "stationnement": [
        "Stationnement gratuit pour véhicules hybrides/électriques",
        "Réduire de 20% le temps de recherche de stationnement",
    ],
    "transports-en-commun": [
        "Transport nocturne à la demande",
    ],
    "espaces-verts": [
        "Supprimer les îlots de chaleur urbains",
        "Re-végétaliser globalement la ville",
        "Haies urbaines mellifères",
        "Jardin permanent Place de Jaude",
        "Transformer les friches en jardins maraîchers",
    ],
    "proprete-dechets": [
        "Retirer les équipements plastiques en urgence",
        "Filière de compostage + \"quartiers éponges\"",
    ],
    "equipements-culturels": [
        "Transformer le Jardin Botanique en musée à ciel ouvert",
        "Ouvrir les médiathèques le dimanche",
        "Redonner liberté de communication aux musées",
    ],
    "evenements-creation": [
        "Ouvrir les colonnes Morris pour spectacles vivants",
        "Espaces publicitaires réservés aux artistes locaux",
        "Partenariat avec Bourges, Capitale Européenne de la Culture",
        "Positionner Clermont comme \"ville de la pop culture\"",
    ],
    "logements-vacants": [
        "Remettre en location 6 000 logements vacants (objectif 15-20 ans)",
    ],
    "acces-logement": [
        "Privilégier réhabilitation plutôt que démolition",
    ],
    "petite-enfance": [
        "Créer une Maison de la Parentalité",
    ],
    "equipements-sportifs": [
        "Arrêter l'extension du Grand Stade",
    ],
    "sport-pour-tous": [
        "Organiser Marathon et Championnat EHPAD",
    ],
    "prevention-mediation": [
        "Cellule de protection animale",
        "Plan stérilisation chats",
        "Autoriser animaux dans transports en commun",
    ],
    "transparence": [
        "Simplifier la gouvernance",
        "Conventions citoyennes et conseils d'arrondissements",
        "Supprimer le SMTC",
        "Éliminer indemnisations des élus au SMTC",
        "Prévoir remplacement du tramway sur pneus",
        "Pilotage direct des mobilités par la Métropole",
    ],
    "budget-participatif": [
        "Conventions citoyennes et conseils d'arrondissements",
    ],
    "services-publics": [
        "Hébergement numérique en France",
        "Reconnaissance du travail des agents municipaux",
        "Audit qualité de vie au travail des agents",
    ],
    "accessibilite": [
        "Conseil municipal de l'accessibilité universelle",
        "Audit complet de voirie avec usagers en fauteuil",
        "Plan priorisé de mise en accessibilité",
        "Activités périscolaires inclusives renforcées",
        "Label \"Commerce accueillant\"",
        "Événements et équipements sportifs accessibles",
        "Site et services numériques 100% accessibles",
        "Simplifier les démarches et soutenir les aidants",
    ],
    "attractivite": [
        "Valoriser les atouts de capitale du Massif central",
        "Stratégie de développement et attractivité",
        "Logique \"ville en centre commercial ouvert\"",
        "Valoriser image, animation et activité touristique",
    ],
}

# Fix: cartailler has "services-publics" twice and "budget-participatif" duplicate with transparence
# Merge services-publics entries
cartailler["services-publics"] = [
    "Hébergement numérique en France",
    "Reconnaissance du travail des agents municipaux",
    "Audit qualité de vie au travail des agents",
]
# Remove duplicate from budget-participatif (already in transparence)
# Actually "Conventions citoyennes et conseils d'arrondissements" fits better in budget-participatif
# Let's keep it only in budget-participatif and remove from transparence
cartailler["transparence"] = [
    "Simplifier la gouvernance",
    "Supprimer le SMTC",
    "Éliminer indemnisations des élus au SMTC",
    "Prévoir remplacement du tramway sur pneus",
    "Pilotage direct des mobilités par la Métropole",
]
cartailler["budget-participatif"] = [
    "Conventions citoyennes et conseils d'arrondissements",
]

# ── Candidats config ──
CANDIDATS = [
    ("bony", bony, BONY_SOURCE, BONY_URL),
    ("darbois", darbois, DARBOIS_SOURCE, DARBOIS_URL),
    ("maximi", maximi, MAXIMI_SOURCE, MAXIMI_URL),
    ("cartailler", cartailler, CARTAILLER_SOURCE, CARTAILLER_URL),
]

# ── Load data ──
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# ── Set programmeComplet ──
for c in data["candidats"]:
    if c["id"] in ("bony", "darbois", "maximi", "cartailler"):
        c["programmeComplet"] = True
    if c["id"] == "darbois":
        c["programmeUrl"] = DARBOIS_URL
    if c["id"] == "maximi":
        c["programmeUrl"] = MAXIMI_URL
    if c["id"] == "cartailler":
        c["programmeUrl"] = CARTAILLER_URL

# ── Inject propositions ──
for cat in data["categories"]:
    for st in cat["sousThemes"]:
        st_id = st["id"]
        props = st["propositions"]
        for cand_id, mapping, source, url in CANDIDATS:
            if st_id in mapping:
                props[cand_id] = {
                    "mesures": mapping[st_id],
                    "source": source,
                    "sourceUrl": url,
                }
            else:
                # Only set null if currently null (don't overwrite existing data)
                if cand_id not in props or props[cand_id] is None:
                    props[cand_id] = None

# ── Count mesures per candidat ──
counts = {}
for cand_id, mapping, _, _ in CANDIDATS:
    total = sum(len(v) for v in mapping.values())
    counts[cand_id] = total

for cid, cnt in counts.items():
    print(f"{cid}: {cnt} mesures intégrées")

# ── Verify no bianchi data was touched ──
# (bianchi was not in CANDIDATS, so untouched by design)

# ── Save ──
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nFichier sauvegardé : {JSON_PATH}")
