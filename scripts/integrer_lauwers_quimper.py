#!/usr/bin/env python3
"""Intègre le programme de Marie Lauwers (Quimper) dans quimper-2026.json"""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

JSON_PATH = r"C:\Users\KOPELMANRon\projets perso\FR comp mun\data\elections\quimper-2026.json"

SOURCE = "Programme officiel (brochure PDF, 8 pages)"
SOURCE_URL = "https://quimper-solidaire-populaire.fr"

# Mapping: sous-thème -> liste de mesures
PROPS = {
    # SECURITE
    "police-municipale": [
        "Recentrer la mission de la police municipale vers une police de proximité pour assurer la tranquillité publique. Refuser l'armement létal."
    ],
    "prevention-mediation": [
        "Renforcer les médiateur·rices et éducateur·rices de rue par la création d'un club communal de prévention spécialisée, pour recréer du lien et de la confiance."
    ],
    "violences-femmes": [
        "Accueil et hébergement d'urgence 7j/7 et 24h/24 inconditionnel, au sein d'un espace transdisciplinaire, en lien avec l'ESCALE.",
        "Créer une Maison dédiée aux droits des femmes et des LGBTQI+ en lien avec les associations.",
        "Formation des agent·es sur les violences et les stéréotypes sexistes, contre le harcèlement et toutes formes de violences."
    ],

    # TRANSPORTS
    "transports-en-commun": [
        "Gratuité des transports en commun, tous les jours, pour toutes et tous.",
        "Faire du transport en commun un service public fort : augmentation de la fréquence, des amplitudes horaires, amélioration de l'interconnexion avec des parkings de délestage végétalisés en périphérie."
    ],
    "velo-mobilites-douces": [
        "Déployer un éclairage nocturne à détection de présence, sécurisant les déplacements tout en réduisant la pollution lumineuse et en protégeant la biodiversité."
    ],
    "pietons-circulation": [
        "Abaisser et faire respecter la vitesse sur les axes dangereux (Route de Douarnenez, Route de Pont-l'Abbé, etc.), en complément d'aménagements sécurisant piétons et cyclistes."
    ],
    "tarifs-gratuite": [
        "Gratuité des premiers m³ d'eau, tarification solidaire de l'eau, contrôle citoyen et préparation du retour en régie publique de l'eau et de l'assainissement."
    ],

    # LOGEMENT
    "logement-social": [
        "Objectif : 400 logements sociaux et très sociaux par an, avec une politique foncière volontariste (produire des HLM, préempter, réquisitionner et réhabiliter les logements existants).",
        "Gel des loyers OPAC (contre l'augmentation actuelle)."
    ],
    "logements-vacants": [
        "Réquisition d'une partie des logements vacants depuis plus de 2 ans (plus de 1000 à Quimper).",
        "Créer une brigade contre l'habitat indigne : service local dédié pour contrôler l'hygiène et la salubrité dans les locations privées, identifier les logements vacants et mobiliser ces biens."
    ],
    "encadrement-loyers": [
        "Renforcement de l'encadrement des meublés touristiques type AirBnB : contrôles systématiques des plateformes, sanctions en cas d'abus, réduction du quota de meublés de tourisme par propriétaire."
    ],
    "acces-logement": [
        "Arrêté de non mise à la rue : interdiction des expulsions locatives sans proposition de relogement.",
        "Réserver du foncier au logement étudiant et à destination des jeunes actif·ves.",
        "Développer des résidences et de l'habitat inclusif publics, accessibles et intergénérationnels."
    ],

    # EDUCATION
    "petite-enfance": [
        "Développer massivement des places de crèche publique, avec des horaires atypiques.",
        "Créer des crèches bilingues dont la collectivité est toujours dépourvue.",
        "Créer une délégation municipale de la protection de l'enfance chargée de lutter contre les violences et le harcèlement.",
        "Déployer un plan de sensibilisation des équipes municipales, éducatives et sportives afin de repérer, prévenir et agir face aux violences sexistes, sexuelles, discriminatoires et aux maltraitances à l'égard des enfants."
    ],
    "ecoles-renovation": [
        "Réhabiliter l'école de Pénanguer et maintien des écoles publiques de proximité dans tous les quartiers.",
        "Développer des filières bilingues en pérennisant le troisième site Diwan à Creac'h Gwenn. Planifier la politique de création de sites bilingues publics, en Centre-Ville, à Ergué-Armel et/ou à Penhars."
    ],
    "cantines-fournitures": [
        "Garantir l'égalité à l'école par la cantine gratuite 100% bio et local pour tous·tes, expérimenter les petits-déjeuners à l'école, et engager un travail pour des cours de récréation non-genrées."
    ],
    "periscolaire-loisirs": [
        "Créer des emplois stables pour les animateurs·rices, reconnaître leur temps de préparation et assurer leur formation continue.",
        "Créer un centre de loisirs bilingue dont la collectivité est toujours dépourvue.",
        "Assurer l'accueil des personnes en situation de handicap dès la petite enfance, par la formation à l'accueil dans les centres de loisirs, à l'école, etc."
    ],
    "jeunesse": [
        "Lancer un dialogue avec les jeunes afin qu'ils et elles prennent pleinement leur place dans la vie de la commune, en leur confiant des espaces pour se retrouver et en garantissant les conditions matérielles nécessaires à leur autonomie.",
        "Expérimenter la création d'une cantine solidaire municipale au service de tous les jeunes."
    ],

    # ENVIRONNEMENT
    "espaces-verts": [
        "Planifier la zéro artificialisation nette (ZAN) en sanctuarisant les espaces naturels, forestiers et agricoles et en stoppant l'étalement urbain."
    ],
    "climat-adaptation": [
        "Engager une bifurcation écologique, populaire et planifiée : agir sur les causes du dérèglement climatique à l'échelle du territoire."
    ],
    "alimentation-durable": [
        "Créer une ceinture alimentaire : protéger les terres agricoles, aider à l'installation d'agriculteur·ices et créer une régie municipale de l'alimentation pour produire, transformer et distribuer une nourriture saine, locale et accessible, avec un objectif 100% bio et local en restauration collective.",
        "Politique foncière de rachat de terres agricoles pour faciliter l'installation de jeunes agriculteur·ices.",
        "Mettre en place un atelier de transformation mutualisé (conserves et jus) accessible aux agriculteur·ices bio et associations de quartier.",
        "Valoriser les circuits courts en facilitant les conditions d'accès et d'installation des commerçant·es et artisan·es ambulant·es, notamment les agriculteur·ices bio en vente directe."
    ],

    # SANTE
    "centres-sante": [
        "Créer un centre de santé municipal en salariant des médecins et des spécialistes, avec une action pluridisciplinaire, pour lutter contre les déserts médicaux et assurer la continuité des soins, avec application du tiers payant.",
        "Développer des programmes de santé axés sur les risques environnementaux pour attirer des soignant·es engagé·es."
    ],
    "prevention-sante": [
        "Mettre en place un plan municipal de lutte contre l'isolement (visites à domicile, dispositifs d'écoute, repérage des situations de précarité)."
    ],
    "seniors": [
        "Renforcer le CCAS en développant un service public municipal de l'autonomie : aides à domicile renforcées, amélioration des conditions de travail, équipes stables et formées, soutien concret aux aidant·es.",
        "Valoriser l'engagement des seniors dans les associations, pour reconnaître pleinement leur rôle actif dans la cité, en facilitant la mise en relation."
    ],

    # DEMOCRATIE
    "budget-participatif": [
        "Renforcer les Conseils de Quartier et les budgets participatifs avec un réel partage du pouvoir décisionnel, et ouvrir un débouché institutionnel aux initiatives habitantes en favorisant la création d'assemblées citoyennes."
    ],
    "transparence": [
        "Instaurer le Référendum d'Initiative Citoyenne (RIC) : dès 6000 signatures, les Quimpérois·es pourront déclencher un référendum local sur tous les sujets, y compris la révocation d'un·e élu·e si 50% des inscrit·es participent.",
        "Créer une carte de citoyenneté municipale pour toute personne vivant sur la commune, quelle que soit sa nationalité, afin d'ouvrir des droits et permettre à chacun·e de prendre part à la vie démocratique."
    ],
    "vie-associative": [
        "Généraliser les conventions pluri-annuelles et garantir un financement stable de fonctionnement pour les associations.",
        "Remettre les salles municipales au service des associations et de la vie locale en reprenant en régie des salles comme le Chapeau Rouge."
    ],

    # ECONOMIE
    "commerce-local": [
        "Activer un droit de préemption sur les fonds de commerce, pour favoriser les commerces indépendants.",
        "Aider, par la mise à disposition de locaux, l'installation ou le maintien de petits commerces (librairie, boulangerie, boucherie, épicerie, etc.).",
        "Création d'un crédit municipal qui accompagne les TPE/PME dans leur activité et les soutienne sur des projets utiles et/ou d'intérêt public."
    ],
    "emploi-insertion": [
        "Faire entrer Quimper dans le dispositif « Territoire Zéro Chômeur de longue durée » (TZCLD).",
        "Créer une bourse du travail, de la solidarité et des initiatives, avec les syndicats et associations, à destination de tous·tes les travailleur·euses.",
        "Faire de la commande publique un levier de transition écologique et sociale : accès facilité aux SCOP, artisans et acteurs de l'ESS, critères environnementaux renforcés.",
        "Soutien aux initiatives citoyennes d'ateliers de réparations et de réemploi."
    ],

    # CULTURE
    "equipements-culturels": [
        "Favoriser la gratuité (notamment des médiathèques) et la tarification sociale des équipements culturels.",
        "Rapprocher l'art et la culture de la population par la mise en place d'espaces de création et d'expression artistique, favorisant la pratique directe, amateure, tous publics dans chaque quartier.",
        "Proposer aux artistes des lieux vacants comme espaces de création, permanents ou non."
    ],
    "evenements-creation": [
        "Organiser régulièrement, avec les associations locales et collectifs d'habitant·es et/ou d'artistes, des rendez-vous et animations dans les rues et sur les places pour faire de l'espace public un lieu vivant de culture, de loisirs, de débats et de rencontres.",
        "Créer un label de diffusion « Breizh 'n Concert » porté par la Ville, destiné à offrir à tous les artistes de Bretagne une programmation régulière tout au long de l'année.",
        "Impulser un plan de formation du personnel municipal au breton et satisfaire systématiquement les besoins selon la volonté exprimée des personnels.",
        "Aider et sensibiliser les acteurs économiques et les associations à l'usage du bilinguisme dans leurs communications."
    ],

    # SPORT
    "sport-pour-tous": [
        "Rendre la pratique sportive accessible à tous·tes par une tarification sociale.",
        "Créer une bourse municipale pour l'équipement sportif et, avec les recycleries, développer des filières de matériel reconditionné et de seconde main."
    ],

    # URBANISME
    "accessibilite": [
        "Accélérer les travaux d'accessibilité de l'espace urbain, des bâtiments publics, des transports, et soutenir l'adaptation des logements publics et privés pour les personnes en situation de handicap."
    ],

    # SOLIDARITE
    "aide-sociale": [
        "Reconnaître et soutenir les familles monoparentales (dont 80% sont des mères isolées) en créant une carte famille monoparentale donnant accès prioritaire aux crèches (même sans emploi) et aux logements sociaux."
    ],
    "egalite-discriminations": [
        "Mettre en place un Observatoire communal des discriminations : racisme, antisémitisme, islamophobie, sexisme, LGBTphobies, discriminations liées au handicap ou à la précarité. Actions de testing et mesures concrètes pour garantir l'égalité réelle."
    ],
}

# --- Chargement ---
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# --- Mise à jour candidat ---
for c in data["candidats"]:
    if c["id"] == "lauwers":
        c["programmeComplet"] = True
        c["programmeUrl"] = "https://quimper-solidaire-populaire.fr/programme/"
        c["programmePdfPath"] = "data/programmes/LAUW001 2026020238 Brochure uqsp 2(1).pdf"
        break

# --- Injection des propositions ---
total_mesures = 0
sous_themes_touches = 0

for cat in data["categories"]:
    for st in cat["sousThemes"]:
        if st["id"] in PROPS:
            mesures = PROPS[st["id"]]
            st["propositions"]["lauwers"] = {
                "source": SOURCE,
                "sourceUrl": SOURCE_URL,
                "mesures": mesures
            }
            total_mesures += len(mesures)
            sous_themes_touches += 1

# --- Vérification ---
all_st_ids = set()
for cat in data["categories"]:
    for st in cat["sousThemes"]:
        all_st_ids.add(st["id"])

missing = set(PROPS.keys()) - all_st_ids
if missing:
    print(f"ERREUR: sous-thèmes inconnus: {missing}")
    sys.exit(1)

print(f"Total mesures insérées : {total_mesures}")
print(f"Sous-thèmes touchés : {sous_themes_touches}")

# --- Sauvegarde ---
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f"Fichier sauvegardé : {JSON_PATH}")
