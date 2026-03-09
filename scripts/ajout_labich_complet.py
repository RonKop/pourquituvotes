"""Ajout des mesures supplémentaires du programme complet Labich (21p) - mars 2026."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/elections/saint-etienne-2026.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

SRC = "Programme complet 2026 (PDF)"
URL = "https://sihamlabich.fr/wp-content/uploads/2026/03/Programme-complet.pdf"

# Update programmeUrl to new complete PDF
for c in data["candidats"]:
    if c["id"] == "labich":
        c["programmeUrl"] = "https://www.sihamlabich.fr"
        break

ajouts = {
    "securite": {
        "police-municipale": [
            "Consolider la brigade spécifique de sécurisation des transports en commun pour garantir la sérénité des voyageurs et conducteurs sur le réseau STAS.",
        ],
        "prevention-mediation": [
            "Multiplier les dispositifs « voisins vigilants » pour lutter contre les cambriolages, notamment dans les zones pavillonnaires.",
            "Renforcer la police de proximité en étroite coordination avec les médiateurs et les éducateurs de rue (prévention spécialisée).",
            "Travailler en collaboration directe avec l'État et la justice pour lutter fermement contre les trafics en tout genre.",
            "Agir contre les nuisances liées à l'ouverture trop tardive de certaines épiceries de quartier, afin de préserver la tranquillité des riverains.",
        ],
        "videoprotection": [
            "Faciliter la mise à disposition des images de vidéoprotection à la justice lors d'infractions, pour accompagner les dépôts de plainte des victimes.",
        ],
    },
    "transports": {
        "tarifs-gratuite": [
            "Rendre gratuits les transports en commun pour les classes de primaire afin de faciliter l'apprentissage hors des murs.",
        ],
        "transports-en-commun": [
            "Renforcer le train avec davantage de cadences les jours de semaine, notamment en direction de Lyon, avec un train toutes les 15 minutes.",
            "Proposer des trajets de bus plus directs, plus rapides et plus fréquents, sur le modèle du futur Chronobus M6+ reliant la Cité du Design à la Métare.",
        ],
        "stationnement": [
            "Poursuivre la création de parkings-relais aux entrées de la ville et améliorer les grands axes routiers (RN88, A47) pour fluidifier le trafic.",
        ],
    },
    "logement": {
        "logements-vacants": [
            "Réhabiliter en urgence les 12 000 logements vacants de la ville afin de proposer davantage de solutions de relogement aux familles.",
        ],
        "acces-logement": [
            "Lutter contre l'insalubrité et les déperditions énergétiques en amplifiant les travaux dans les logements, tout en veillant à la non-augmentation des charges par les bailleurs.",
            "Travailler avec l'Union des syndicats de la métropole et les syndics de copropriété pour anticiper les difficultés et éviter les dégradations extrêmes.",
        ],
    },
    "education": {
        "ecoles-renovation": [
            "Améliorer la qualité et la réactivité des interventions techniques dans les écoles pour garantir sécurité, confort et continuité du service.",
            "Soutenir les directrices et directeurs d'école en leur apportant un appui humain et des outils informatiques performants.",
            "Aménager des espaces de repos pour les enfants en situation de handicap et des salles de motricité pérennes.",
            "Renforcer le partenariat avec les écoles en créant le conseil consultatif de l'éducation, composé d'ateliers de travail avec des élus formés et sectorisés.",
            "Soutenir la création et le fonctionnement des associations de parents d'élèves grâce à une enveloppe financière annuelle dédiée.",
        ],
        "petite-enfance": [
            "Augmenter le nombre d'ATSEM pour garantir l'épanouissement de tous les élèves dès le plus jeune âge.",
        ],
        "cantines-fournitures": [
            "Introduire une 3ème option poisson ou œuf en cantine scolaire, en complément des choix viande et végétarien.",
        ],
        "periscolaire-loisirs": [
            "Mettre en place le Pass Loisirs Enfant pour garantir à chaque enfant l'accès aux activités sportives, culturelles et éducatives, quels que soient les revenus.",
            "Rendre plus accessibles les centres de loisirs aux enfants en situation de handicap par la formation de personnel qualifié.",
        ],
        "jeunesse": [
            "Faciliter l'accès aux stages de 3e pour les collégiens, afin que plus aucun élève ne se retrouve sans solution faute de réseau.",
            "Proposer que chaque élu accueille deux fois par an des stagiaires pour rendre lisible le rôle des institutions et susciter l'engagement citoyen.",
        ],
    },
    "environnement": {
        "climat-adaptation": [
            "Lancer le grand plan « Îlots de fraîcheur » avec la plantation de 12 000 arbres dans tous les quartiers et le centre-ville.",
        ],
        "renovation-energetique": [
            "Lancer un vaste programme d'isolation thermique des logements, écoles et bâtiments municipaux, avec panneaux solaires et toits végétalisés.",
            "Lancer un projet de récupération de chaleur issue des anciennes galeries minières pour alimenter des bâtiments publics et réduire les dépenses énergétiques.",
        ],
        "proprete-dechets": [
            "Réorganiser le service pour déployer davantage d'agents sur le terrain et assurer une propreté optimale sur toutes les rues.",
            "Augmenter le nombre de corbeilles sur la place publique et améliorer la propreté et l'entretien des toilettes publiques.",
            "Soutenir l'augmentation du nombre de tournées de collecte des poubelles par les éboueurs de la Métropole.",
        ],
        "alimentation-durable": [
            "Étendre l'exigence de 70 % bio et 80 % de produits locaux des cantines aux centres de loisirs, pour une alimentation saine sur le temps périscolaire.",
            "Poursuivre le déploiement du Plan Alimentaire Territorial pour améliorer le bien manger et lutter contre l'obésité.",
        ],
    },
    "sante": {
        "seniors": [
            "Créer une deuxième résidence senior moderne « Cité des aînés » pour offrir des lieux de vie adaptés, ouverts et dignes.",
            "Mobiliser davantage le Gérontopole pour anticiper le vieillissement, prévenir les chutes et améliorer les conditions de vie à domicile.",
            "Encourager la solidarité intergénérationnelle par l'extension du réseau des bénévoles aux jeunes pour le soutien aux personnes isolées.",
            "Soutenir les associations proposant des projets à impact pour lutter contre l'isolement des personnes âgées.",
            "Créer une maison du répit pour les familles et les proches aidants.",
        ],
    },
    "democratie": {
        "budget-participatif": [
            "Mettre en place des conseils par quartier chaque trimestre afin de répondre aux préoccupations des habitants.",
            "Maintenir les ateliers et réunions publiques pour concerter et co-construire les projets structurants, secteur par secteur.",
        ],
        "vie-associative": [
            "Soutenir la vie associative par la mise à disposition gratuite de locaux pour favoriser le lien social et les événements festifs.",
            "Mettre en place un conseil de concertation avec les associations d'étudiants pour répondre à leurs besoins.",
            "Soutenir les associations qui interviennent auprès des publics les plus fragiles pour préserver leur dignité.",
        ],
        "transparence": [
            "Sanctionner les absences injustifiées et manquements répétés des élus au devoir de présence auprès des habitants.",
        ],
    },
    "economie": {
        "attractivite": [
            "Lancer un « Grand Plan Enseigne » des commerces du centre-ville avec une identité design pour améliorer l'esthétique et l'image de la ville.",
            "Défendre l'Aéroport de Bouthéon, essentiel pour l'attractivité économique du territoire.",
        ],
        "emploi-insertion": [
            "Mettre en place un groupe de travail avec la Fédération du Bâtiment, les chambres consulaires et les syndicats patronaux pour répondre aux attentes des entreprises.",
            "Soutenir les forums pour promouvoir l'emploi, organisés par les clubs d'entreprises ou les maisons de quartier.",
            "Poursuivre le soutien au développement des entreprises de l'économie sociale et solidaire.",
        ],
    },
    "culture": {
        "equipements-culturels": [
            "Créer un parcours culturel de la ville via une application sonore et vidéo « Saint-Étienne Culture et Patrimoine ».",
            "Valoriser le patrimoine et les monuments historiques par une mise en lumière ambitieuse et responsable.",
        ],
        "evenements-creation": [
            "Réaliser plusieurs fresques géantes de personnalités ayant marqué la ville pour donner une identité forte à Saint-Étienne.",
        ],
    },
    "sport": {
        "equipements-sportifs": [
            "Créer un espace aqualudique dans l'une des piscines stéphanoises.",
        ],
        "sport-pour-tous": [
            "Organiser chaque année une grande Fête du sport, populaire et fédératrice.",
        ],
    },
    "urbanisme": {
        "accessibilite": [
            "Améliorer et adapter les logements en fonction du handicap afin de favoriser l'autonomie et la sécurité des personnes.",
        ],
    },
    "solidarite": {
        "egalite-discriminations": [
            "Poursuivre l'organisation de temps forts de sensibilisation, de dialogue et de rencontre pour promouvoir le respect, la fraternité, la laïcité et l'harmonie.",
        ],
    },
}

added = 0
for cat in data["categories"]:
    cat_id = cat["id"]
    if cat_id not in ajouts:
        continue
    for st in cat["sousThemes"]:
        st_id = st["id"]
        if st_id not in ajouts[cat_id]:
            continue
        nouvelles = ajouts[cat_id][st_id]
        current = st["propositions"].get("labich")
        if current is None:
            st["propositions"]["labich"] = {
                "mesures": nouvelles,
                "source": SRC,
                "sourceUrl": URL,
            }
        elif isinstance(current, dict) and "mesures" in current:
            current["mesures"].extend(nouvelles)
            # Update source to new complete PDF
            current["source"] = SRC
            current["sourceUrl"] = URL
        else:
            st["propositions"]["labich"] = {
                "mesures": nouvelles,
                "source": SRC,
                "sourceUrl": URL,
            }
        added += len(nouvelles)
        print(f"  {cat_id}/{st_id}: +{len(nouvelles)}")

print(f"\nTotal: {added} mesures ajoutées")

# Count total
total = sum(
    len(st.get("propositions", {}).get("labich", {}).get("mesures", []))
    for cat in data["categories"]
    for st in cat["sousThemes"]
    if st.get("propositions", {}).get("labich") and isinstance(st["propositions"]["labich"], dict)
)
print(f"Total Labich après ajout: {total} mesures")

with open('data/elections/saint-etienne-2026.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("saint-etienne-2026.json mis à jour OK")
