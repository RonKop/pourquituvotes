"""Integrate Siham Labich (Avec Coeur Stéphanois) program for Saint-Étienne from 17p PDF."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/elections/saint-etienne-2026.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

SRC = "Programme officiel 2026 (PDF)"
URL = "https://www.sihamlabich.fr"

def prop(mesures):
    return {"mesures": mesures, "source": SRC, "sourceUrl": URL}

# Update candidate metadata
for c in data["candidats"]:
    if c["id"] == "labich":
        c["programmeUrl"] = URL
        c["programmeComplet"] = True
        break

labich = {
    "securite": {
        "police-municipale": prop([
            "Recruter 30 policiers municipaux supplémentaires, principalement à pied, pour dissuader et rassurer.",
            "Renforcer la présence en soirée et la nuit, en centre-ville et dans les quartiers.",
            "Renforcer la sécurité aux abords des écoles aux heures d'entrée et de sortie.",
            "Déployer une application municipale de signalement géolocalisée reliée au Centre de Supervision Urbain.",
            "Mobilisation pour l'ouverture d'un nouveau commissariat.",
        ]),
        "videoprotection": prop([
            "Installer de nouvelles caméras de vidéoprotection pour mieux mailler le territoire, avec exploitation optimale dans le futur Centre de Supervision Urbain."
        ]),
        "prevention-mediation": prop([
            "Réorganiser les Conseils Locaux de Prévention de la Délinquance par quartier et de façon trimestrielle.",
            "Renforcer le plan lumière pour que chaque rue soit éclairée et garantisse la sécurité de tous.",
            "Mettre en place un dispositif de responsabilisation des mineurs et de leurs parents pour tout acte grave d'incivilité.",
            "Appliquer des travaux d'intérêt général avec sanction réparatrice immédiate pour les jeunes.",
            "Verbaliser les trottinettes et vélos sur les trottoirs ne respectant pas la vitesse légale."
        ]),
        "violences-femmes": prop([
            "Généraliser le dispositif « Demandez Angela » dans les commerces, bars, pharmacies et lieux culturels pour protéger les femmes du harcèlement de rue.",
            "Développer la Maison des femmes pour sécuriser les victimes de violences et faciliter leur accès aux droits."
        ]),
    },
    "transports": {
        "transports-en-commun": prop([
            "Poursuivre l'amélioration des transports en commun et de la desserte de tous les quartiers, sans opposer les usages."
        ]),
        "velo-mobilites-douces": prop([
            "Poursuivre le plan vélo en complémentarité avec les autres modes de déplacement.",
            "Poursuivre le déploiement de véhicules propres."
        ]),
        "pietons-circulation": prop([
            "Simplifier le plan de circulation, notamment les voies d'entrée en centre-ville, aujourd'hui trop complexes et dissuasives.",
            "Refuser la piétonnisation totale et dogmatique : ne pas opposer les mobilités pour garantir l'accessibilité à tous."
        ]),
        "stationnement": prop([
            "Engager un grand plan de restructuration du stationnement : réhabilitation du parking des Ursules et construction d'un nouveau parking.",
            "Places gratuites le week-end et le mercredi."
        ]),
        "tarifs-gratuite": None,
    },
    "logement": {
        "logement-social": prop([
            "Réduire le délai d'octroi des logements sociaux à moins d'un an, avec plateforme transparente des bailleurs.",
            "Démolir les immeubles insalubres pour laisser place à des parcs verts et aires de jeux.",
            "Construire davantage de T4 et T5 adaptés aux familles recomposées."
        ]),
        "logements-vacants": prop([
            "Lutter contre les marchands de sommeil avec mise en place du permis de louer.",
            "Vendre les biens immobiliers inutilisés de la Ville, coûteux et énergivores."
        ]),
        "encadrement-loyers": None,
        "acces-logement": prop([
            "Favoriser l'accès à la propriété pour les Stéphanois.",
            "Encourager le développement d'écoquartiers et de petites maisons pavillonnaires avec jardins.",
            "Poursuivre et renforcer les subventions pour les ravalements de façades et la rénovation énergétique des copropriétés dégradées."
        ]),
    },
    "education": {
        "petite-enfance": prop([
            "Augmenter le nombre de places en crèche et en halte-garderie, notamment pour les personnes en insertion professionnelle."
        ]),
        "ecoles-renovation": prop([
            "Poursuivre le plan de réhabilitation et construction des écoles avec 50 millions d'euros dédiés.",
            "Végétaliser les cours de récréation pour lutter contre les îlots de chaleur.",
            "Enveloppe de 30 millions d'euros pour la réhabilitation des structures d'éducation populaire."
        ]),
        "cantines-fournitures": None,
        "periscolaire-loisirs": prop([
            "Renforcer l'éducation populaire avec des activités périscolaires de qualité, portées par des étudiants dont le BAFA sera financé.",
            "Développer une véritable éducation culturelle sur le temps scolaire et périscolaire.",
            "Créer des espaces snoezelen dans les écoles pour les enfants autistes et faciliter l'accès aux centres de loisirs pour les enfants handicapés.",
            "Étudier l'ouverture des bibliothèques en soirée et le dimanche."
        ]),
        "jeunesse": prop([
            "Mettre en place un plan municipal de lutte contre le harcèlement, à l'école et sur les réseaux sociaux.",
            "Proposer des événements nombreux pour les étudiants, avec un dialogue constant via le conseil consultatif de la jeunesse.",
            "Organiser des temps de valorisation de la police municipale et des sapeurs-pompiers pour susciter les vocations chez les jeunes."
        ]),
    },
    "environnement": {
        "espaces-verts": prop([
            "Poursuivre et amplifier la végétalisation du centre-ville et des quartiers.",
            "Préserver la biodiversité, multiplier les parcs, jardins et aires de jeux de proximité végétalisées.",
            "Renforcer l'entretien des espaces verts, déployer des bacs à fleurs dans le centre-ville et les quartiers.",
            "Protéger l'animal en ville : signer la charte nationale de protection animale, lutter contre l'exploitation animale dans les cirques, renforcer le soutien à la SPA."
        ]),
        "proprete-dechets": prop([
            "Investir dans de nouvelles machines de nettoyage, étendre le lavage des trottoirs et mettre en place une task force anti-tags.",
            "Lutter contre les décharges sauvages en supprimant l'accès par QR Code aux déchetteries et en déployant des déchetteries mobiles par quartier.",
            "Instaurer des journées mensuelles de ramassage des déchets associant écoles, familles et habitants.",
            "Retirer les potelets et blocs de pierre inesthétiques."
        ]),
        "climat-adaptation": prop([
            "Renforcer les actions de sensibilisation à l'environnement et soutenir les associations de développement durable.",
            "Lutter contre les nuisances sonores."
        ]),
        "renovation-energetique": prop([
            "Poursuivre la rénovation énergétique des copropriétés dégradées, des bailleurs sociaux et du patrimoine municipal.",
            "Installer des panneaux solaires sur les bâtiments publics pour une énergie locale et décarbonée."
        ]),
        "alimentation-durable": None,
    },
    "sante": {
        "centres-sante": prop([
            "Développer de véritables maisons de santé municipales avec mise à disposition de bâtiments pour faciliter l'installation de médecins.",
            "Poursuivre le plan cancer, les actions de dépistage et de prévention en lien avec le CHU.",
            "Lutter contre les pollutions environnementales, le tabac dans les espaces publics et l'usage du protoxyde d'azote."
        ]),
        "prevention-sante": prop([
            "Porter une attention particulière à la santé mentale, notamment des jeunes et des enfants, en renforçant l'écoute, la prévention et l'accompagnement."
        ]),
        "seniors": None,
    },
    "democratie": {
        "budget-participatif": None,
        "transparence": prop([
            "Instaurer une charte de l'élu signée par chacun, engageant au respect, à la transparence et à la présence sur le terrain.",
            "Formations renforcées des élus dès le début du mandat sur leurs responsabilités et devoirs."
        ]),
        "vie-associative": prop([
            "Acter le financement pluriannuel des structures d'éducation populaire sur la durée de leur agrément.",
            "Accompagner la stabilité du modèle économique des associations via le conseil consultatif de l'éducation populaire."
        ]),
        "services-publics": prop([
            "Garantir une offre de service public de qualité en veillant au bien-être et à la reconnaissance des agents municipaux.",
            "Réduire les dépenses de communication.",
            "Réévaluer les clauses sociales et environnementales des marchés publics."
        ]),
    },
    "economie": {
        "commerce-local": prop([
            "Objectif « zéro vitrine vide » : mobiliser le droit de préemption, dispositifs d'accompagnement financier, coordonnateur dédié.",
            "Groupe de travail avec CCI et Chambre des métiers pour favoriser le retour de l'artisanat et des commerces de proximité.",
            "Implantation d'un centre d'activités commerciales et d'affaires de 30 000 m² sur le site de l'ancien hôpital de la Charité."
        ]),
        "emploi-insertion": prop([
            "Lancer un grand plan local de formation basé sur une cartographie des métiers en tension, en lien avec les 100 plus grandes entreprises de la métropole.",
            "Faire de l'apprentissage et de l'alternance un enjeu majeur en facilitant les mises en relation jeunes-employeurs.",
            "Intégrer des clauses sociales et d'emploi local dans les marchés publics municipaux.",
            "Faciliter l'implantation d'entreprises créatrices d'emplois durables sur le foncier libéré par les démolitions."
        ]),
        "attractivite": prop([
            "Organiser mensuellement des animations festives, culturelles et musicales en centre-ville.",
            "Valoriser la Cité du design comme outil de fierté locale et de rayonnement international.",
            "Créer une Cité circulaire et une matériauthèque du réemploi au quartier du Soleil, avec site dédié à l'économie sociale et solidaire."
        ]),
    },
    "culture": {
        "equipements-culturels": prop([
            "Valoriser la Cité du design pour qu'elle devienne un outil compris et approprié par les habitants."
        ]),
        "evenements-creation": prop([
            "Organiser mensuellement des animations festives et culturelles sur le modèle de la Fête du Livre, Noël, Carnaval.",
            "Développer une éducation culturelle accessible à tous, sortir d'une culture perçue comme élitiste."
        ]),
    },
    "sport": {
        "equipements-sportifs": prop([
            "Rénover les gymnases pour offrir des équipements modernes et adaptés.",
            "Entretenir les piscines.",
            "Construire une nouvelle patinoire fonctionnelle et écologiquement responsable."
        ]),
        "sport-pour-tous": prop([
            "Soutenir davantage les clubs sportifs."
        ]),
    },
    "urbanisme": {
        "amenagement-urbain": prop([
            "Revitaliser le centre-ville : pôle structurant sur le site de l'ancien hôpital de la Charité (30 000 m²).",
            "Remplacer les immeubles insalubres démolis par des parcs verts et aires de jeux, en concertation avec les riverains.",
            "Améliorer tous les quartiers via une politique d'animation résidentielle ambitieuse pour renforcer la mixité sociale."
        ]),
        "accessibilite": prop([
            "Lutter contre toutes les formes de discrimination envers les personnes en situation de handicap et les personnes âgées.",
            "Développer le mobilier urbain intelligent pour les personnes en situation de handicap."
        ]),
        "quartiers-prioritaires": prop([
            "Poursuivre la politique d'animation résidentielle pour revaloriser l'image des quartiers et maintenir la mixité sociale.",
            "Créer des zones d'activités économiques sur le foncier libéré par les démolitions (modèle ZAE Loti)."
        ]),
    },
    "solidarite": {
        "aide-sociale": None,
        "egalite-discriminations": prop([
            "Lutter contre toutes les formes de discrimination.",
            "Porter une attention particulière aux personnes fragilisées ou mises à l'écart."
        ]),
        "pouvoir-achat": prop([
            "Aucune augmentation d'impôts sur le mandat, et si possible baisse de la taxe foncière.",
            "Rechercher des cofinancements auprès des partenaires institutionnels."
        ]),
    },
}

# Apply
for cat in data["categories"]:
    cat_id = cat["id"]
    if cat_id in labich:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in labich[cat_id]:
                st["propositions"]["labich"] = labich[cat_id][st_id]

# Count
count = sum(
    len(val["mesures"])
    for cat in data["categories"]
    for st in cat["sousThemes"]
    for key, val in [("labich", st.get("propositions", {}).get("labich"))]
    if val is not None and val.get("mesures")
)
print(f"Labich: {count} mesures extracted from PDF")

with open('data/elections/saint-etienne-2026.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saint-Étienne JSON updated OK")
