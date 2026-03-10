"""Re-extract Bell-Lloch data from full 32-page PDF (94 propositions)."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/elections/vitry-sur-seine-2026.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

SRC = "Programme officiel 2026 (PDF)"
URL = "https://pbl2026.fr/Tract-Programme-PBL2026-NFPV.pdf"

def prop(mesures):
    return {"mesures": mesures, "source": SRC, "sourceUrl": URL}

# Update candidate metadata
for c in data["candidats"]:
    if c["id"] == "bell-lloch":
        c["programmeUrl"] = "https://pbl2026.fr/programme.html"
        c["programmeComplet"] = True
        break

# Full mapping from the 32-page PDF
bell_lloch = {
    "securite": {
        "police-municipale": prop([
            "Mobilisation pour l'ouverture d'un nouveau commissariat digne du dynamisme de la ville."
        ]),
        "videoprotection": prop([
            "Développement concerté de la vidéo-verbalisation pour limiter les incivilités et fluidifier la circulation."
        ]),
        "prevention-mediation": prop([
            "Création d'une équipe de médiateurs urbains de proximité pour prévenir les conflits et apaiser l'espace public.",
            "Intensifier la lutte contre les dépôts sauvages à l'aide de la brigade propreté et de caméras mobiles."
        ]),
        "violences-femmes": prop([
            "Extension et développement de la Maison des femmes avec un axe handicap renforcé.",
            "Sécuriser les femmes victimes de violences et faciliter leur accès aux droits (logement, santé, emploi)."
        ]),
    },
    "transports": {
        "transports-en-commun": prop([
            "Mobilisation pour renforcer les cadences du RER C, le prolongement des lignes 7 et 10, et désenclaver les quartiers du haut de Vitry.",
            "Réhabilitation de la passerelle reliant Alfortville à Vitry."
        ]),
        "velo-mobilites-douces": prop([
            "Développer massivement la pratique du vélo avec un réseau de pistes cyclables maillées, continues et sécurisées.",
            "Créer des espaces de stationnement vélo aux abords des transports en commun et partout en ville.",
            "Déployer des bornes de recharge électrique sur l'ensemble du territoire."
        ]),
        "pietons-circulation": prop([
            "Création de zones piétonnes pour lutter contre la pollution de l'air.",
            "Étude pour la piétonisation de la Départementale Paul Vaillant-Couturier.",
            "Encourager les expérimentations de mobilités partagées."
        ]),
        "stationnement": prop([
            "Concertation sur le plan de stationnement.",
            "Rénovation du parking souterrain du centre-ville."
        ]),
        "tarifs-gratuite": None,
    },
    "logement": {
        "logement-social": prop([
            "Construction de 2 000 nouveaux logements tout en préservant les zones pavillonnaires.",
            "Intensifier la rénovation des logements sociaux.",
            "Réhabilitation de la cité Ampère et étude pour une rénovation complète du quartier 8 mai 1945.",
            "Réhabilitation de Capra Gravier et rénovation de la galerie commerciale.",
            "Réhabilitation complète du quartier Moulin Vert (collectifs et pavillons)."
        ]),
        "logements-vacants": prop([
            "Moratoire d'un an pour un diagnostic sur les nouvelles constructions hors logements sociaux.",
            "Étude de la sous et sur-occupation des logements sociaux."
        ]),
        "encadrement-loyers": prop([
            "Mobilisation pour l'encadrement des loyers.",
            "Accompagnement d'une garantie de paiement des loyers."
        ]),
        "acces-logement": prop([
            "Des centaines de logements en accession sociale à la propriété pour les jeunes décohabitants et les ménages.",
            "Création des assises annuelles pour le logement durable.",
            "Création d'une plateforme dédiée à l'accompagnement des locataires et de leurs amicales auprès des bailleurs.",
            "Création d'une pension de famille pour l'hébergement d'urgence des personnes sans-domicile.",
            "Aide à la rénovation des copropriétés dégradées.",
            "Ouverture du bail mobilité pour les jeunes."
        ]),
    },
    "education": {
        "petite-enfance": prop([
            "Mobilisation pour de nouvelles crèches départementales, dont le financement de la crèche des Granges municipalisée.",
            "Publication d'un livret pour l'accompagnement à la parentalité.",
            "Sensibilisation à l'utilisation des écrans dès le plus jeune âge."
        ]),
        "ecoles-renovation": prop([
            "Amplifier la rénovation des écoles : végétalisation, rénovation thermique et cours dégenrées avec un niveau d'investissement élevé.",
            "Installation de panneaux photovoltaïques et toits végétalisés pour les écoles.",
            "Construction d'une nouvelle école pour désengorger le secteur Gare."
        ]),
        "cantines-fournitures": prop([
            "Améliorer la qualité de la cantine vers des produits 100 % bio et issus des circuits courts.",
            "Mise en place de l'étude scolaire gratuite et de l'aide aux devoirs pour toutes et tous."
        ]),
        "periscolaire-loisirs": prop([
            "Sensibilisation culture dès la maternelle : étendre le dispositif « graines de culture » avec plus de sorties culturelles."
        ]),
        "jeunesse": prop([
            "Mise en place d'un accompagnement face à Parcours Sup.",
            "Constitution d'un Conseil des jeunes de 15-18 ans.",
            "Ouverture des centres de quartier aux 15-17 ans.",
            "Création de plus d'espaces publics pour les jeunes."
        ]),
    },
    "environnement": {
        "espaces-verts": prop([
            "Création d'un grand parc en bord de Seine de 50 000 m², 2e plus grand parc naturel aménagé de la ville.",
            "5 600 m² d'espaces verts en cœur de ville dans le cadre du nouveau centre-ville.",
            "Plantation de plus de 1 000 arbres supplémentaires et milliers de m² désimperméabilisés.",
            "Développer l'agriculture urbaine : renforcer les jardins partagés et ouvriers, coopération avec la ferme de Villejuif.",
            "Création d'îlots de fraîcheur dans tous les quartiers.",
            "Bilan annuel complet du patrimoine arboré.",
            "Étendre les horaires d'ouverture des parcs durant l'été."
        ]),
        "proprete-dechets": prop([
            "Création d'une déchetterie-ressourcerie gratuite pour le recyclage.",
            "Renforcer le nettoiement des rues par la sensibilisation et l'action collective.",
            "Intensifier la lutte contre les dépôts sauvages avec brigade propreté et caméras mobiles."
        ]),
        "climat-adaptation": prop([
            "Installation de panneaux photovoltaïques sur les bâtiments communaux.",
            "Création d'une académie du climat pour la transition écologique populaire.",
            "Concertation pour un vrai espace de baignade dans la Seine.",
            "Sensibiliser et former à la bienveillance envers les animaux.",
            "Réévaluer les clauses sociales et environnementales des marchés publics."
        ]),
        "renovation-energetique": prop([
            "Géothermie pour passer à 95 % d'énergie locale et renouvelable, avec baisse des tarifs de chauffage urbain.",
            "Accélérer la réduction de la consommation énergétique des bâtiments publics."
        ]),
        "alimentation-durable": prop([
            "Étude pour une sécurité sociale alimentaire."
        ]),
    },
    "sante": {
        "centres-sante": prop([
            "Étude pour une annexe du Centre Municipal de Santé (CMS).",
            "Développer le CMPP pour agir sur la santé mentale.",
            "Extension du nombre de prises en charge à domicile en lien avec la CPAM 94."
        ]),
        "prevention-sante": prop([
            "Création d'une mutuelle de santé municipale."
        ]),
        "seniors": prop([
            "Création d'une nouvelle résidence seniors moderne conforme aux besoins d'aujourd'hui.",
            "Renforcer le service municipal des retraité·es avec un service spécifique pour l'ensemble des besoins.",
            "Extension du nombre de prises en charge et soins à domicile.",
            "Mobilisation pour le retour de la carte Améthyste."
        ]),
    },
    "democratie": {
        "budget-participatif": prop([
            "Création d'un budget participatif et démocratique : un budget dédié aux conseils de quartier avec propositions soumises au vote des Vitriots.",
            "Poursuite de la concertation sur les grands projets de la ville (projets participatifs, réunions, balades urbaines)."
        ]),
        "transparence": prop([
            "Diffusion en direct des conseils municipaux.",
            "Travailler à la systématisation des réponses aux usagers et usagères."
        ]),
        "vie-associative": prop([
            "Mise à disposition de 3 nouvelles salles municipales pour les associations (Ardoines, Moulin Vert, Fort).",
            "Création des « César » du bénévolat : cérémonie annuelle de valorisation des acteurs associatifs.",
            "Renforcement du Service à la Vie Associative (SVA).",
            "Évolution du Conseil local de l'environnement."
        ]),
        "services-publics": prop([
            "Mobilisation pour le maintien du service public postal.",
            "Mobilisation pour les AESH et une meilleure prise en compte des besoins dans les écoles.",
            "Refonte du RIFSEEP (grille de rémunération des agents) et mise en place du congé menstruel."
        ]),
    },
    "economie": {
        "commerce-local": prop([
            "Poursuivre la politique de préemption commerciale pour diversifier les commerces.",
            "Création d'un nouveau marché au Port à l'Anglais.",
            "Favoriser l'implantation des terrasses.",
            "Création d'un office du tourisme et mise en place d'un schéma touristique ambitieux."
        ]),
        "emploi-insertion": prop([
            "Accueillir 1 000 nouveaux emplois au quartier des Ardoines avec une pépinière d'entreprises (Fab-Lab).",
            "Création d'une régie de quartiers pour les petits travaux du quotidien et l'insertion des plus précaires."
        ]),
        "attractivite": prop([
            "Nouveau pôle commercial végétalisé avec équipements sportifs au quartier Malassis.",
            "Accueil du nouveau métro au quartier Balzac avec de nouveaux emplois et commerces.",
            "Rénovation de la galerie commerciale Auchan au quartier Commune de Paris."
        ]),
    },
    "culture": {
        "equipements-culturels": prop([
            "Concertation et rénovation des 3 Cinés Robespierre avec espace de formation.",
            "Rénovation de la Maison sociale du Moulin Vert mise à disposition des associations.",
            "Mise à disposition de plus d'équipements publics pour les Vitriots en multipliant les usages."
        ]),
        "evenements-creation": prop([
            "Gratuité des équipements culturels municipaux pour les moins de 26 ans.",
            "Sensibiliser à la culture dès la maternelle (dispositif « graines de culture »)."
        ]),
    },
    "sport": {
        "equipements-sportifs": prop([
            "Construction de 2 nouveaux gymnases.",
            "Construction de 4 nouveaux city stades (Fort, Centre ville, Square de l'Horloge, Germain Defresne).",
            "Extension des horaires du Centre aquatique et des autres équipements sportifs."
        ]),
        "sport-pour-tous": prop([
            "Maintien de l'été sportif et des pratiques adaptées à toutes et tous.",
            "Poursuite de l'investissement dans les équipements sportifs."
        ]),
    },
    "urbanisme": {
        "amenagement-urbain": prop([
            "Nouveau cœur de ville avec 5 600 m² d'espaces verts, commerces de proximité, terrasses, logements sociaux rénovés, 3 Cinés Robespierre modernisés et parking souterrain rénové.",
            "Création d'un centre de quartier aux Combattants.",
            "Développement du mobilier urbain intelligent pour les personnes en situation de handicap."
        ]),
        "accessibilite": prop([
            "Reconfiguration de l'accès à l'Hôtel de ville pour améliorer l'accessibilité.",
            "Instauration d'une commission autour du handicap avec les premiers concernés.",
            "Accueil d'une nouvelle structure pour les personnes en situation de handicap au Moulin Vert.",
            "Création d'une semaine de sensibilisation au handicap."
        ]),
        "quartiers-prioritaires": prop([
            "Réhabilitation de la cité Ampère et étude pour une rénovation complète du quartier 8 mai 1945.",
            "Réhabilitation de Capra Gravier.",
            "Réhabilitation complète du quartier Moulin Vert."
        ]),
    },
    "solidarite": {
        "aide-sociale": prop([
            "Création de la Maison de la Paix et de la solidarité internationale.",
            "Élargir la Conférence de la Paix par de nouveaux partenariats et coopérations décentralisées.",
            "Conforter le devoir de mémoire et transmettre l'Histoire des Vitriots."
        ]),
        "egalite-discriminations": prop([
            "Création d'une ligne d'écoute LGBTQIA+.",
            "Renforcement de la formation et de la sensibilisation aux luttes contre les discriminations."
        ]),
        "pouvoir-achat": prop([
            "Mise à jour du quotient familial, en particulier pour les familles monoparentales.",
            "Création d'une mutuelle de santé municipale.",
            "Développement du chauffage urbain écologique par géothermie avec baisse des tarifs."
        ]),
    },
}

# Apply
for cat in data["categories"]:
    cat_id = cat["id"]
    if cat_id in bell_lloch:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in bell_lloch[cat_id]:
                st["propositions"]["bell-lloch"] = bell_lloch[cat_id][st_id]

# Count
count = sum(
    len(val["mesures"])
    for cat in data["categories"]
    for st in cat["sousThemes"]
    for key, val in [("bell-lloch", st.get("propositions", {}).get("bell-lloch"))]
    if val is not None and val.get("mesures")
)
print(f"Bell-Lloch: {count} mesures extracted from full PDF")

with open('data/elections/vitry-sur-seine-2026.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Vitry JSON updated OK")
