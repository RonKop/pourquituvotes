"""Integrate Fatah Aggoune (Gentilly Coeur Battant) program from PDF."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/elections/gentilly-2026.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

SRC = "Programme officiel 2026"
URL = "https://www.gentillycoeurbattant.fr/wp-content/uploads/2026/02/Programme-Fatah-Aggoune-Gentilly-Coeur-Battant_16p-A4-v4-2.pdf"

def prop(mesures):
    return {"mesures": mesures, "source": SRC, "sourceUrl": URL}

# Update candidate metadata
for c in data["candidats"]:
    if c["id"] == "aggoune":
        c["programmeUrl"] = "https://www.gentillycoeurbattant.fr/"
        c["programmeComplet"] = True
        c["programmePdfPath"] = URL
        break

# Full mapping from the 16-page PDF
aggoune_props = {
    "securite": {
        "police-municipale": prop([
            "Exiger un commissariat de plein exercice à Gentilly avec les moyens afférents.",
            "Poursuivre la coopération avec la Police nationale et demander plus d'effectifs de proximité dédiés à Gentilly."
        ]),
        "videoprotection": prop([
            "Revoir l'éclairage des rues pour renforcer la sécurité, en lien avec le schéma de vidéoprotection de la ville."
        ]),
        "prevention-mediation": prop([
            "Renforcer la présence des ASVP sur le terrain avec formation pour l'intervention, la prévention et la médiation.",
            "Poursuivre les missions du CLSPD pour la coordination de tous les acteurs de la sécurité et de la prévention.",
            "Lutter contre les incivilités (dépôts sauvages, déjections canines, jets de mégots, stationnement sauvage) avec verbalisation effective."
        ]),
        "violences-femmes": prop([
            "Organiser des marches exploratoires avec les femmes pour améliorer la sécurité, l'éclairage et les cheminements.",
            "Mener une politique féministe avec initiatives publiques autour de l'égalité femmes-hommes et de la lutte contre les violences.",
            "Renforcer le réseau municipal contre les violences faites aux femmes (bailleurs, associations, CCAS, CMS, services sociaux).",
            "Mobiliser des logements d'urgence pour les femmes victimes de violences.",
            "Accompagner les familles monoparentales par des dispositifs de soutien dédiés."
        ]),
    },
    "transports": {
        "transports-en-commun": prop([
            "Faire évoluer La Valouette en transport adapté (handicap, horaires écoles/marchés, véhicule électrique) avec service à la demande.",
            "Se mobiliser pour l'amélioration du réseau de transport : surcharge RER B, bus, prolongation ligne 5 du métro, tarif unique.",
            "Créer un Comité des usagers des transports collectifs pour rencontrer Île-de-France Mobilités."
        ]),
        "velo-mobilites-douces": prop([
            "Créer des pistes cyclables, zones piétonnes et apaisées, et sécuriser les itinéraires scolaires.",
            "Sensibiliser à la pratique du vélo et déployer du mobilier vélo et des ateliers de réparation."
        ]),
        "pietons-circulation": prop([
            "Piétonniser des voies suivant le parcours de la Bièvre."
        ]),
        "stationnement": prop([
            "Déployer des places de véhicules en auto-partage."
        ]),
        "tarifs-gratuite": None,
    },
    "logement": {
        "logement-social": prop([
            "Maintenir 50 % de logements sociaux et ne pas permettre la vente de logements sociaux.",
            "Améliorer les parcours résidentiels avec cotation transparente (composition familiale, revenus, handicap).",
            "Intervenir pour que les plafonds de ressources pour l'accès au logement social soient relevés."
        ]),
        "logements-vacants": prop([
            "Freiner les constructions de bureaux qui devront prévoir la réversibilité en logements dès leur conception."
        ]),
        "encadrement-loyers": prop([
            "Agir auprès de l'État pour obtenir un encadrement des loyers afin que familles et jeunes puissent rester à Gentilly."
        ]),
        "acces-logement": prop([
            "Créer un Conseil local du logement (élu·es, habitant·es, locataires, bailleurs, associations).",
            "Promouvoir l'accession sociale à la propriété par le Bail réel solidaire.",
            "Lutter contre les marchands de sommeil et l'habitat indigne, renforcer le permis de louer et informer sur les aides ANAH."
        ]),
    },
    "education": {
        "petite-enfance": prop([
            "Lancer un plan « Gentilly à hauteur d'enfants » en concertation avec parents et enfants (mobilités, jeux, espaces publics, pédibus).",
            "Renforcer l'offre petite enfance (crèche familiale, Nid d'éveil) par la création d'un Pôle de la petite enfance."
        ]),
        "ecoles-renovation": prop([
            "Poursuivre la politique de rénovation thermique des écoles et la création de cours Oasis."
        ]),
        "cantines-fournitures": prop([
            "Améliorer la qualité de la restauration collective et des repas scolaires (bio, saison, alternative végétarienne), étude d'une cuisine à Gentilly."
        ]),
        "periscolaire-loisirs": prop([
            "Poursuivre la politique sociale, culturelle, éducative et sportive pour l'enfance (sensibilisation propreté, violences, écrans)."
        ]),
        "jeunesse": prop([
            "Renforcer le parcours jeunesse 11-17 ans et rénover le Point J avec un projet pédagogique repensé.",
            "Mettre en place un Conseil des jeunes et soutenir les associations de jeunesse.",
            "Créer un lieu dédié à la jeunesse 16-28 ans (espace citoyen, emploi, alternance, permis de conduire).",
            "Aménager les horaires de la médiathèque et ludothèque pour les rendre plus accessibles aux jeunes.",
            "Réouvrir les antennes de quartier pour rapprocher les services publics des jeunes."
        ]),
    },
    "environnement": {
        "espaces-verts": prop([
            "Créer un Comité citoyen des espaces verts (fauche tardive, jardins partagés, espèces locales, sol vivant).",
            "Compléter le Plan Arbres en concertation (recensement, diagnostic, sauvegarde arbres remarquables, nouvelles plantations).",
            "Aménager des espaces refuges pour animaux sauvages dans les parcs (pollinisateurs, oiseaux, chauves-souris)."
        ]),
        "proprete-dechets": prop([
            "Poursuivre l'éducation au tri et aux biodéchets."
        ]),
        "climat-adaptation": prop([
            "Réaliser un bilan carbone et énergétique de l'administration communale (patrimoine, véhicules, numérique).",
            "Renforcer les plans Canicule et Grand Froid avec des lieux d'accueil adaptés dans chaque quartier.",
            "Intégrer des clauses environnementales, sociales et d'égalité dans les achats municipaux."
        ]),
        "renovation-energetique": prop([
            "Lancer une campagne de raccordement à la géothermie et au réseau de chaleur urbain.",
            "Mettre en place un programme « zéro précarité énergétique » pour la rénovation des logements privés.",
            "Étudier avec le SIPPEREC la possibilité de production d'énergie renouvelable sur la ville."
        ]),
        "alimentation-durable": prop([
            "Diversifier les marchés avec des stands bio/locaux et créer un réseau de producteurs bio à moins de 100 km.",
            "Éliminer les sacs plastiques et réduire les emballages sur les marchés.",
            "Expérimenter une Sécurité Sociale de l'Alimentation et soutenir la création d'une épicerie associative solidaire.",
            "Engager une politique de réduction du plastique et des perturbateurs endocriniens dans les services publics (charte villes sans perturbateurs endocriniens)."
        ]),
    },
    "sante": {
        "centres-sante": prop([
            "Doter le CMS d'un médecin de santé publique dédié à la prévention (alimentation, pollution, addictions).",
            "Poursuivre l'action contre le renoncement aux soins : aide aux RDV, transport, interprétariat, mammobus.",
            "Développer les partenariats pour compléter les spécialités non couvertes par le CMS.",
            "Adapter les consultations du CMS au diagnostic territorial de santé.",
            "Enrichir le CMS d'une cellule santé des femmes (contraception, IVG, dépistages, ordonnance verte)."
        ]),
        "prevention-sante": prop([
            "Agir pour la prévention des addictions au niveau intercommunal (sensibilisation, formations, réinsertion).",
            "Défendre la santé mentale, la psychiatrie et la pédopsychiatrie en lien avec la Fondation Vallée.",
            "Mettre en place des cellules santé mentale dans les écoles contre le harcèlement."
        ]),
        "seniors": prop([
            "Lutter contre l'isolement des personnes âgées et soutenir l'EHPAD et la résidence autonomie du Val de Bièvre.",
            "Développer des résidences intergénérationnelles intégrant les seniors.",
            "Accompagner les bailleurs pour adapter les logements sociaux aux personnes âgées (ascenseurs, douches, terrasses).",
            "Créer un centre d'accueil pour les aidants au sein du CCAS avec droit au répit.",
            "Mettre en place des ateliers intergénérationnels.",
            "Lutter contre la fracture numérique par un nouveau service numérique pour les seniors.",
            "Encourager les consultations et prélèvements médicaux à domicile."
        ]),
    },
    "democratie": {
        "budget-participatif": prop([
            "Organiser des votations citoyennes ouvertes aux résidents étrangers et aux mineurs de 16 ans sur les grands sujets communaux.",
            "Instaurer un droit d'interpellation des élu·es avec débat en Conseil Municipal dès pétition de 1 % du corps électoral."
        ]),
        "transparence": prop([
            "Assurer la transparence des actions municipales et rendre accessibles les retranscriptions des Conseils Municipaux (vidéos, réseaux sociaux).",
            "Mettre en place un Conseil local de suivi des engagements avec culture de l'évaluation."
        ]),
        "vie-associative": prop([
            "Créer une Maison des associations incluant une Maison des solidarités locales et internationales.",
            "Renforcer le volontariat et les services civiques, créer un Conseil des habitants étrangers.",
            "Organiser des universités populaires (séminaires formation-action avec élu·es, agent·es et habitant·es)."
        ]),
        "services-publics": prop([
            "Être réactif aux demandes des Conseils de quartier.",
            "Mener des actions « aller vers » dans les quartiers populaires avec permanences régulières d'élu·es.",
            "Organiser des chantiers ouverts aux habitants pour l'aménagement de l'espace public."
        ]),
    },
    "economie": {
        "commerce-local": prop([
            "Utiliser une foncière commerciale pour acquérir des commerces vacants et les louer à tarif solidaire.",
            "Associer les commerçants aux décisions municipales les concernant.",
            "Couvrir partiellement le marché du centre-ville et installer des sanitaires.",
            "Proposer des boutiques éphémères avec baux de courte durée dans les locaux des bailleurs.",
            "Développer la boucle commerciale en centre-ville avec commerces diversifiés."
        ]),
        "emploi-insertion": prop([
            "Poursuivre le PLIE et candidater au dispositif « territoires zéro chômeur de longue durée ».",
            "Soutenir les initiatives d'économie sociale et solidaire (ex : La Mine)."
        ]),
        "attractivite": None,
    },
    "culture": {
        "equipements-culturels": prop([
            "Travailler avec le Lavoir numérique pour diversifier la programmation cinématographique.",
            "Créer des ateliers d'artistes et mettre à disposition des lieux pour leurs expositions."
        ]),
        "evenements-creation": prop([
            "Créer un parcours interactif culturel avec fresques street art et semaine thématique annuelle.",
            "Renforcer les échanges culturels internationaux (correspondance entre écoles, projets artistiques).",
            "Favoriser les événements culturels participatifs (fresques, carnavals, concerts, fêtes de quartier, repas du monde).",
            "Associer les Jeunes Talents de Gentilly aux événements municipaux."
        ]),
    },
    "sport": {
        "equipements-sportifs": prop([
            "Maintenir le soutien aux associations sportives (subventions, équipements, minibus)."
        ]),
        "sport-pour-tous": prop([
            "Mettre en place une offre diversifiée d'activités physiques en libre accès, accessible à tous.",
            "Accueillir les personnes en situation de handicap dans les activités sportives."
        ]),
    },
    "urbanisme": {
        "amenagement-urbain": prop([
            "Créer un Atelier public de l'urbanisme et de l'habitat pour la co-construction avec les habitants.",
            "Créer des cœurs de quartier vivants, végétalisés, piétonnisés avec mobilier urbain (bancs, toilettes, kiosques).",
            "Renforcer les continuités écologiques entre quartiers (trame verte et bleue, îlots de fraîcheur).",
            "Mener une concertation sur la réouverture de la Bièvre, préserver les arbres du parc Pablo Picasso.",
            "Poursuivre les grands projets : couverture RER B, extension parc Picasso, aménagement Bièvre, requalification îlot Paix-Reims et avenue PVC, groupe scolaire sur site collège P. Curie, transformation du périphérique en boulevard urbain.",
            "Encadrer strictement les nouvelles constructions via le PLUi avec charte de construction durable (matériaux biosourcés, concertation habitants)."
        ]),
        "accessibilite": prop([
            "Créer une délégation Handicap et inclusion au Conseil Municipal avec plan d'accessibilité et pôle du handicap.",
            "Former les animateurs des centres de loisirs pour l'accueil des enfants en situation de handicap.",
            "Programmer la mise en accessibilité des espaces publics en concertation avec les associations.",
            "Favoriser une plateforme de covoiturage pour seniors et personnes en situation de handicap.",
            "Rapprocher les services municipaux de chaque quartier via un transport dédié."
        ]),
        "quartiers-prioritaires": None,
    },
    "solidarite": {
        "egalite-discriminations": prop([
            "Lutter contre toutes les discriminations, racismes, islamophobie et antisémitisme.",
            "Former les agents contre les discriminations LGBTQIA+ et les violences éducatives.",
            "Féminiser les noms de rues et espaces publics."
        ]),
        "aide-sociale": prop([
            "Renforcer l'aide aux personnes exilées : soutien juridique, parrainages, soutien au collectif Solidaire Régularisation de Séjour.",
            "Créer un Fonds municipal de solidarité internationale et renforcer les liens avec l'ANVITA.",
            "Relancer la coopération avec Duguwolowila (Mali) pour l'accès à l'eau.",
            "S'engager pour la paix avec un jumelage avec une ville palestinienne."
        ]),
        "pouvoir-achat": prop([
            "Lancer un programme « zéro précarité énergétique » pour accompagner les ménages modestes dans la rénovation de leurs logements."
        ]),
    },
}

# Apply propositions
for cat in data["categories"]:
    cat_id = cat["id"]
    if cat_id in aggoune_props:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in aggoune_props[cat_id]:
                st["propositions"]["aggoune"] = aggoune_props[cat_id][st_id]

# Count
count = sum(
    len(val["mesures"])
    for cat in data["categories"]
    for st in cat["sousThemes"]
    for key, val in [("aggoune", st.get("propositions", {}).get("aggoune"))]
    if val is not None and val.get("mesures")
)
print(f"Aggoune: {count} mesures extracted")

with open('data/elections/gentilly-2026.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Gentilly JSON updated OK")
