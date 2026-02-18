#!/usr/bin/env python3
"""Intègre les propositions de Nathalie Appéré (Rennes Solidaire) depuis l'OCR du programme."""
import json
import sys

JSON_PATH = "data/elections/rennes-2026.json"
SOURCE = "Programme Rennes Solidaire"
SOURCE_URL = "https://rennes-solidaire.fr/notre-programme/"

def prop(texte):
    return {"texte": texte, "source": SOURCE, "sourceUrl": SOURCE_URL}

# Mapping: sous-thème ID → proposition Appéré
PROPOSITIONS = {
    # SÉCURITÉ
    "police-municipale": prop(
        "Recrutement de 60 policiers municipaux supplémentaires. "
        "Création d'une police métropolitaine des transports. "
        "Ouverture d'un hôtel de police municipale au Palais Saint-Georges "
        "et d'un second poste mobile de proximité"
    ),
    "videoprotection": prop(
        "Déploiement de 80 nouvelles caméras de vidéoprotection"
    ),
    "prevention-mediation": prop(
        "25 nouveaux médiateurs et éducateurs dans les quartiers pour atteindre 175 postes. "
        "Face aux trafics de stupéfiants, actions à 360° : prévention, soin, éducation, "
        "soutien aux projets associatifs et citoyens, animation de l'espace public. "
        "Sensibilisation et formation pour mieux anticiper et réagir face aux risques majeurs"
    ),
    "violences-femmes": prop(
        "Consolidation de la Maison des femmes Gisèle Halimi. "
        "Lancement de « Safe place », réseau de lieux sûrs contre les violences sexistes, "
        "racistes et homophobes"
    ),

    # TRANSPORTS
    "transports-en-commun": prop(
        "Mise en service des 4 lignes de Trambus à fréquence élevée. "
        "Augmentation des dessertes de bus, maintien de la navette du centre-ville. "
        "Un métro toutes les minutes sur la ligne a. "
        "Arrêt à la demande et présence humaine renforcée sur le réseau"
    ),
    "velo-mobilites-douces": prop(
        "Finalisation du Réseau express vélo. "
        "Déploiement des Vélostar 100% électriques et de nouvelles stations. "
        "Plus de stationnements vélos, mieux sécurisés"
    ),
    "pietons-circulation": prop(
        "Renforcement des opérations de sécurité routière. "
        "Augmentation de l'éclairage autour des stations de métro et bus"
    ),
    # stationnement: rien de spécifique (vélo couvert dans velo-mobilites-douces)
    "tarifs-gratuite": prop(
        "Gratuité des transports en commun pour tous les étudiants boursiers. "
        "Tarif étudiants dans les piscines"
    ),

    # LOGEMENT
    "logement-social": prop(
        "500 nouveaux logements locatifs sociaux par an. "
        "300 nouveaux logements par an à loyers réduits. "
        "600 nouveaux logements par an pour devenir propriétaire au prix d'un loyer"
    ),
    "logements-vacants": prop(
        "Dès autorisation de l'État, réquisition des immeubles durablement vacants"
    ),
    "encadrement-loyers": prop(
        "Plafonnement des loyers du parc privé. "
        "Création d'un permis de louer pour garantir des logements dignes"
    ),
    "acces-logement": prop(
        "Création d'une bourse d'échange des logements sociaux "
        "pour s'adapter à l'évolution des besoins"
    ),

    # ÉDUCATION
    "petite-enfance": prop(
        "Nouvelles places d'accueil en crèche (Gros-Chêne, Kennedy, EuroRennes, "
        "crèche plein air Bois Perrin). Soutien aux structures innovantes pour les jeunes enfants"
    ),
    "ecoles-renovation": prop(
        "Nouvelle école Trégain, rénovation totale des écoles Colombier et Albert-de-Mun, "
        "nouveau collège de Beauregard. Végétalisation des cours, rues aux écoles, "
        "éducation à la nature, classes égalité"
    ),
    "cantines-fournitures": prop(
        "Ouverture de la nouvelle cuisine centrale. 100% de produits bio dans les cantines scolaires, "
        "second plat végétarien, sortie définitive du plastique"
    ),
    "periscolaire-loisirs": prop(
        "100% des petits Rennais sachant nager et faire du vélo à la fin du primaire. "
        "Ouverture mensuelle de la Halle Martenot et de la brasserie Saint-Hélier "
        "avec des espaces de jeux géants. Priorité à la santé physique et mentale, "
        "lutte contre les violences faites aux enfants, prévention du harcèlement, "
        "sensibilisation aux écrans"
    ),
    "jeunesse": prop(
        "Création d'un guichet unique jeunes et d'un bouclier anti-exclusion "
        "pour les 16-25 ans en difficulté. Renforcement des dispositifs d'accès au travail "
        "et aux stages. Poursuite de la rénovation des restaurants et résidences universitaires"
    ),

    # ENVIRONNEMENT
    "espaces-verts": prop(
        "Plantation de 400 000 arbres d'ici 10 ans sur le territoire métropolitain. "
        "Création d'un nouveau site de jardins familiaux au sud de Rennes. "
        "Nouveaux potagers citoyens, plantation d'arbres fruitiers"
    ),
    "proprete-dechets": prop(
        "Réduction des déchets. Nouveau service gratuit d'enlèvement des encombrants à domicile. "
        "Renforcement de la tri-troc mobile"
    ),
    "climat-adaptation": prop(
        "Protection des cours d'eau, territoire zéro pesticide en 2030. "
        "Étude de toutes les possibilités de baignade en zone naturelle. "
        "Création de l'Académie populaire du climat"
    ),
    "renovation-energetique": prop(
        "Rénovation thermique des équipements municipaux, développement du photovoltaïque. "
        "Accompagnement de la rénovation énergétique des copropriétés privées et logements sociaux. "
        "Raccordement de 16 000 nouveaux logements au réseau de chauffage urbain "
        "avec deux nouvelles chaufferies"
    ),
    "alimentation-durable": prop(
        "Développement d'une offre d'alimentation locale durable et accessible financièrement "
        "dans les quartiers populaires. Rennes ville pilote pour la santé environnementale et le bien manger"
    ),

    # SANTÉ
    "centres-sante": prop(
        "Accompagnement du projet de nouveau CHU, maintien d'activités de soin sur le site de l'Hôpital sud. "
        "Nouveau pôle de santé dalle Kennedy, soutien à l'installation de maisons de santé dans les quartiers. "
        "Création d'une offre de mutuelle santé municipale"
    ),
    "prevention-sante": prop(
        "Expérimentation d'un bus itinérant, conventionné avec plusieurs associations, "
        "pour de la prévention en santé et santé mentale"
    ),
    "seniors": prop(
        "Rénovation des EHPAD Champs-Manceaux, Raymond-Thomas, Saint-Cyr "
        "et de nouveaux logements adaptés. "
        "Création de « restaurants séniors » pour les personnes résidant à leur domicile. "
        "Généralisation de Vill'en Joie, dispositif visant à rompre l'isolement. "
        "Création d'un service public d'accompagnement numérique pour les personnes âgées"
    ),

    # DÉMOCRATIE
    "budget-participatif": prop(
        "Budget participatif tous les 2 ans et annuel pour les enfants"
    ),
    "transparence": prop(
        "Lancement de Rennes 2050, une large concertation pour définir le futur projet urbain. "
        "Création d'Explora'Rennes, comité citoyen des marches exploratoires pour des rues "
        "mieux adaptées aux besoins. Création de régies de quartier pour faciliter "
        "les initiatives citoyennes"
    ),
    "vie-associative": prop(
        "Protection des subventions aux associations malgré les restrictions budgétaires de l'État. "
        "Aide à l'emploi associatif et création d'un fonds de soutien à l'innovation associative. "
        "Nouveau pôle associatif à Baud-Chardonnet, tiers-lieu à Maurepas, "
        "rénovation de la maison de quartier de Villejean. "
        "Développement de conciergeries de quartier"
    ),
    "services-publics": prop(
        "Facilitation de l'accès aux droits : élargissement des horaires des services publics municipaux, "
        "renforcement de l'accueil humain et de l'accompagnement numérique"
    ),

    # ÉCONOMIE
    "commerce-local": prop(
        "Soutien aux commerces indépendants et à l'animation commerciale festive. "
        "Plus de commerces de quartier. Création d'un marché à destination des professionnels "
        "pour renforcer les circuits courts et l'accès aux produits locaux et bio"
    ),
    "emploi-insertion": prop(
        "3e plan emploi dans les quartiers populaires. "
        "Cité artisanale au Blosne et plateforme d'économie circulaire aux Halles en commun à la Courrouze. "
        "Soutien à l'économie sociale et solidaire. Création de la Maison des livreurs"
    ),
    "attractivite": prop(
        "Accompagnement renforcé des filières d'avenir : énergie, cybersécurité, IA souveraine et sobre, "
        "mobilités durables, aérospatial. "
        "Renforcement du pôle d'excellence industrielle de la Janais avec de nouvelles implantations d'usines"
    ),

    # CULTURE
    "equipements-culturels": prop(
        "Rénovation du Triangle et du Musée des beaux-arts. "
        "Nouvelles bibliothèques de quartier à Maurepas et à Beauregard. "
        "Ouverture du nouveau Musik Hall, salle de spectacle de 9 000 places"
    ),
    "evenements-creation": prop(
        "Soutien aux scènes ouvertes hors les murs et aux nouveaux plateaux de spectacle dans les parcs. "
        "Organisation des États généraux métropolitains de la culture. "
        "Plateforme pour faciliter les pratiques artistiques dans les locaux temporairement inoccupés. "
        "Conception d'un lieu des cultures de Bretagne"
    ),

    # SPORT
    "equipements-sportifs": prop(
        "Création d'un équipement couvert de glisse urbaine dans l'ancienne piscine de Villejean "
        "et d'une nouvelle salle au Haut-Sancé. "
        "Rénovation des piscines Saint-Georges et Bréquigny. "
        "Rénovation des infrastructures sportives : halle des Gayeulles, dojo à Bréquigny, "
        "skate-park Fresnais, gymnases du Blosne et Albert-de-Mun. "
        "En lien avec le Stade Rennais FC, augmentation de la jauge du Roazhon Park"
    ),
    "sport-pour-tous": prop(
        "Création de parcours sport-santé et d'installations de plein air en accès libre "
        "« à hauteur d'enfants ». Soutien à la pratique sportive des femmes et des filles"
    ),

    # URBANISME
    "amenagement-urbain": prop(
        "Aménagement des quais de Vilaine. Métamorphose de la place de la République. "
        "Réaménagement de la dalle du Colombier avec espaces de détente ombragés et pôle culturel. "
        "Transformation de la dalle du Gros-Chêne en un mail végétalisé avec commerces et équipements. "
        "Transformation du Palais du commerce, du Palais Saint-Melaine, de la chapelle Saint-Yves, "
        "de l'Hôtel-Dieu"
    ),
    "accessibilite": prop(
        "Rennes 100% accessible aux handicaps visibles et invisibles. "
        "Nouvelles places de stationnement PMR. Sensibilisation aux handicaps invisibles. "
        "Renforcement de l'accueil des enfants à besoins particuliers en centres de loisirs. "
        "Nouvelles aires de jeux inclusives"
    ),
    "quartiers-prioritaires": prop(
        "Maurepas, Villejean, Le Blosne, Cleunay : quartiers rénovés avec espaces publics verts, "
        "propres et agréables, logements de qualité, services publics renforcés, nouveaux commerces. "
        "À Bréquigny et Italie : lancement des opérations de rénovation"
    ),

    # SOLIDARITÉ
    "aide-sociale": prop(
        "Création de « restaurants séniors » pour les personnes résidant à leur domicile. "
        "Guichet unique jeunes et bouclier anti-exclusion pour les 16-25 ans. "
        "Nouveau lieu avec douches, bagagerie et laverie pour les personnes sans-abri. "
        "Accompagnement et soutien à l'hébergement des familles exilées. "
        "Accompagnement renforcé des familles monoparentales : tarifs solidaires, garde d'enfant, "
        "soutien scolaire, accès aux loisirs et aux vacances, droit au répit"
    ),
    "egalite-discriminations": prop(
        "Consolidation de la Maison des femmes Gisèle Halimi. "
        "Nouveau lieu métropolitain de ressources et d'accueil pour les victimes de discriminations, "
        "avec un bus de l'égalité itinérant. "
        "Renforcement des formations laïcité pour les agents et acteurs associatifs"
    ),
    "pouvoir-achat": prop(
        "Renforcement des gratuités et des tarifs solidaires, développement de la carte Sortir ! "
        "Facilitation de l'accès aux droits. Raccordement de 16 000 logements au réseau de chauffage urbain "
        "pour réduire les factures énergétiques"
    ),
}

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update candidat info
    for c in data["candidats"]:
        if c["id"] == "appere":
            c["programmeUrl"] = "https://rennes-solidaire.fr/notre-programme/"
            c["programmeComplet"] = True
            c["programmePdfPath"] = "data/programmes/appere-rennes-mesures.pdf"
            break

    # Count updates
    updated = 0
    not_found = []

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] in PROPOSITIONS:
                st["propositions"]["appere"] = PROPOSITIONS[st["id"]]
                updated += 1

    # Check for unmapped propositions
    all_st_ids = set()
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            all_st_ids.add(st["id"])

    for st_id in PROPOSITIONS:
        if st_id not in all_st_ids:
            not_found.append(st_id)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Propositions Appéré mises à jour : {updated}/{len(PROPOSITIONS)}")
    if not_found:
        print(f"Sous-thèmes non trouvés : {not_found}")

    # Count total Appéré propositions
    total = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["propositions"].get("appere") is not None:
                total += 1
    print(f"Total propositions Appéré dans le JSON : {total}")
    print(f"programmeComplet: True")

if __name__ == "__main__":
    main()
