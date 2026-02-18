#!/usr/bin/env python3
"""Enrichit les propositions d'Appéré avec les détails du programme complet (76 pages OCR)."""
import json

JSON_PATH = "data/elections/rennes-2026.json"
SOURCE = "Programme complet Rennes Solidaire (76 pages)"
SOURCE_URL = "https://rennes-solidaire.fr/notre-programme/"

def prop(texte):
    return {"texte": texte, "source": SOURCE, "sourceUrl": SOURCE_URL}

# Propositions enrichies avec le programme complet
ENRICHISSEMENTS = {
    "police-municipale": prop(
        "Recrutement de 60 policiers municipaux supplémentaires (effectif porté à 175), "
        "avec élargissement des horaires notamment en début de semaine et dans les quartiers prioritaires. "
        "Création d'une police métropolitaine des transports et d'une brigade de sécurité routière. "
        "Ouverture d'un hôtel de police municipale au Palais Saint-Georges "
        "et d'un second poste mobile de proximité"
    ),
    "prevention-mediation": prop(
        "25 nouveaux médiateurs et éducateurs dans les quartiers pour atteindre 175 postes, "
        "y compris dans les piscines, bibliothèques et espaces sociaux communs. "
        "Face aux trafics de stupéfiants, actions à 360° : prévention, soin, éducation, "
        "soutien au CAARUD, ouverture d'un 2e CAARUD et expérimentation d'une Halte soin addiction (HSA). "
        "Formation des agents à la gestion de conflit et à la santé mentale. "
        "Nouvelle Charte de la vie nocturne avec maraudes spécialisées"
    ),
    "violences-femmes": prop(
        "Consolidation de la Maison des femmes Gisèle Halimi en lien avec le nouveau Pôle Mère/Enfant du CHU. "
        "Lancement de « Safe place », réseau de lieux sûrs contre les violences sexistes, racistes et homophobes. "
        "Bus mutualisé conventionné pour la prévention VSS, santé sexuelle, santé mentale et addictions. "
        "Généralisation des référents VSS dans les équipements municipaux. "
        "Campagne culture du consentement dans le monde étudiant"
    ),
    "transports-en-commun": prop(
        "Mise en service des 4 lignes de Trambus (55 km, 100% électrique, fréquence jusqu'à 4 min en pointe). "
        "Métro toutes les minutes sur la ligne A dès 2028. "
        "Flotte de bus 100% propre (électrique ou gaz renouvelable) à l'horizon 2030. "
        "Augmentation des dessertes, maintien de la navette du centre-ville pour les personnes âgées et PMR. "
        "Arrêt à la demande et présence humaine renforcée sur le réseau. "
        "Défense du réseau ferroviaire métropolitain et des trains de nuit"
    ),
    "velo-mobilites-douces": prop(
        "Finalisation du Réseau express vélo (14 communes connectées en moins de 20 min, 200 km d'infrastructures). "
        "Déploiement des Vélostar 100% électriques (76 stations, y compris hors Rennes, 2 500 VAE en location). "
        "Plus de stationnements vélos sécurisés (C Park vélo), consultation citoyenne « Un arceau dans ma rue ». "
        "Apprentissage du vélo dans les écoles, bourses vélos, ateliers de réparation dans tous les quartiers"
    ),
    "pietons-circulation": prop(
        "Brigade de sécurité routière au sein de la police municipale. "
        "Multiplication des zones de partage et des rues aux écoles. "
        "Éclairage renforcé aux abords des stations de métro et arrêts de bus. "
        "Voies réservées bus et covoiturage pour réduire les embouteillages. "
        "Parkings relais ouverts le week-end avec possibilité de laisser sa voiture la nuit"
    ),
    "tarifs-gratuite": prop(
        "Gratuité des transports en commun pour tous les étudiants boursiers. "
        "Extension des périodes de gratuité (certains samedis, grands événements). "
        "Tarif étudiant dans les piscines. "
        "Carte Sortir ! ouverte à tous les étudiants boursiers et aux communes de Rennes Métropole"
    ),
    "logement-social": prop(
        "500 nouveaux logements locatifs sociaux par an. "
        "300 logements intermédiaires à loyer encadré par an. "
        "600 logements en accession BRS par an (prix plafonné 2 800-4 200 €/m², 80% de la population éligible). "
        "Mise en œuvre du loyer unique dans le logement social. "
        "Développement de l'habitat partagé et participatif (Triangle, Bois Perrin, Courrouze). "
        "Schéma d'accueil des gens du voyage (4 terrains de grand passage, aire permanente, 9 terrains familiaux)"
    ),
    "acces-logement": prop(
        "Création d'une bourse d'échanges des logements sociaux pour s'adapter à l'évolution des besoins. "
        "Transformation de bureaux inoccupés en logements. "
        "Accompagnement des coopératives d'habitantes et d'habitants pour des loyers maîtrisés. "
        "Application de la charte construction et citoyenneté"
    ),
    "petite-enfance": prop(
        "Nouvelles places d'accueil en crèche (Gros-Chêne, Kennedy, EuroRennes, crèche plein air Bois Perrin). "
        "Soutien aux structures innovantes et associatives d'accueil du jeune enfant à but non lucratif. "
        "Renforcement de l'Observatoire de la petite enfance pour garantir la qualité dans le public et le privé. "
        "Inclusion des enfants en situation de handicap en crèche"
    ),
    "ecoles-renovation": prop(
        "Nouvelle école Trégain, rénovation totale des écoles Colombier et Albert-de-Mun, "
        "nouveau collège de Beauregard. Végétalisation des cours, rues aux écoles, éducation à la nature. "
        "Plan Santé à l'École (accès aux soins, prévention, santé mentale, lutte contre le harcèlement). "
        "Fournitures scolaires gratuites. Rénovation du patrimoine scolaire (2M€/an pour le centre ancien). "
        "Parcours citoyen intégrant éducation artistique et aux médias"
    ),
    "cantines-fournitures": prop(
        "Ouverture de la nouvelle cuisine centrale. Objectif 100% de produits bio dans les cantines d'ici 2032. "
        "Deuxième plat végétarien par semaine dès 2029. Sortie définitive du plastique en 2029. "
        "Augmentation de la part de produits Terre de Sources. "
        "Plan arbres fruitiers dans toute la ville et jardins potagers biologiques cultivés par les élèves"
    ),
    "periscolaire-loisirs": prop(
        "100% des petits Rennais sachant nager et faire du vélo à la fin du primaire. "
        "Ouverture mensuelle de la Halle Martenot et brasserie Saint-Hélier avec espaces de jeux géants. "
        "Plan de lutte contre les violences faites aux enfants, prévention du harcèlement, sensibilisation aux écrans. "
        "Droit aux vacances pour tous (séjours pour enfants ne partant pas). "
        "Ouverture des cours d'école hors temps scolaire (au moins une par quartier)"
    ),
    "jeunesse": prop(
        "Guichet unique d'accès aux droits pour les jeunesses. "
        "Bouclier anti-exclusion pour les 16-25 ans : logement temporaire, mutuelle gratuite, "
        "gratuité transports, accès alimentation/culture/services sociaux. "
        "Convention des jeunesses dédiée à la participation citoyenne. "
        "150 places de logement social pour les jeunes en grande exclusion. "
        "Campagne « Limit's » portée par des jeunes sur santé mentale et écrans. "
        "Poursuite de la rénovation des restaurants et résidences universitaires"
    ),
    "espaces-verts": prop(
        "Plantation de 400 000 arbres d'ici 10 ans sur le territoire métropolitain. "
        "Principe des 3-30-300 : 3 arbres visibles de sa fenêtre, 30% de canopée par quartier, "
        "un espace vert à moins de 300m. "
        "Nouveau site de jardins familiaux au sud de Rennes, potagers citoyens, arbres fruitiers. "
        "Parcours oasis pendant les fortes chaleurs avec cheminements végétalisés et lieux de repos ombragés"
    ),
    "proprete-dechets": prop(
        "Nouveau service gratuit d'enlèvement des encombrants à domicile dans toutes les communes. "
        "Renforcement de la tri-troc mobile et des locaux de réemploi en déchèterie. "
        "Halles en Commun : vitrine de l'économie circulaire avec marché métropolitain du réemploi. "
        "Repair-quartiers et repair-cafés dans chaque quartier (dont Gros-Chêne). "
        "Objectif 412 kg de déchets par habitant/an en 2030 (contre 469 en 2019). "
        "Consigne en verre, lutte contre la fast-fashion"
    ),
    "climat-adaptation": prop(
        "Protection des cours d'eau, territoire zéro pesticide de synthèse en 2030. "
        "Étude de toutes les possibilités de baignade en zone naturelle à l'échelle métropolitaine. "
        "Création de l'Académie populaire du climat : lieu ouvert à tous pour se former et agir. "
        "Exercices citoyens de résilience climatique (inondations, pénurie d'eau, coupures d'électricité). "
        "Aménagement des abords de l'étang des Bougrières. "
        "Baisse de 10% des prélèvements d'eau d'ici 2030"
    ),
    "renovation-energetique": prop(
        "Grand plan de rénovation de 35 équipements municipaux (crèches, écoles, gymnases, EHPAD, maisons de quartier). "
        "Installation de panneaux solaires sur bâtiments publics, stations de métro et parkings. "
        "Raccordement de 16 000 logements au réseau de chauffage urbain avec 2 nouvelles chaufferies biomasse "
        "(Blosne et Courrouze, 100% énergie renouvelable). "
        "Accompagnement de la rénovation énergétique des copropriétés privées et logements sociaux. "
        "Ouverture de l'Unité de Valorisation Énergétique rénovée (25 000 logements alimentés)"
    ),
    "alimentation-durable": prop(
        "Service public de l'alimentation durable et locale dans les quartiers populaires. "
        "Plateforme logistique alimentaire durable métropolitaine pour les circuits courts. "
        "Rennes ville pilote pour la santé environnementale et le bien manger. "
        "École municipale de cuisine ouverte à de nouveaux publics. "
        "Festival « Tout Rennes à table » et plan manger/bouger dans les quartiers. "
        "Soutien à l'agriculture bio et à la Maison du vivant et des semences paysannes (Prévalaye)"
    ),
    "centres-sante": prop(
        "Accompagnement du projet de nouveau CHU, maintien d'activités de soin sur le site de l'Hôpital sud. "
        "Nouveau pôle de santé dalle Kennedy (8 Bourbonnais), en lien avec Espacil. "
        "Soutien à l'implantation de maisons de santé dans les quartiers (enjeu particulier sur Maurepas). "
        "Création d'une offre de mutuelle santé municipale à prix inférieurs au marché. "
        "Temps fort annuel de la santé publique en partenariat avec l'EHESP"
    ),
    "prevention-sante": prop(
        "Bus itinérant mutualisé pour la prévention en santé, santé mentale et addictions. "
        "Ouverture d'un 2e CAARUD et expérimentation d'une Halte soin addiction (HSA). "
        "Réseau de référents premiers secours en santé mentale dans les services municipaux. "
        "Actions de prévention de la sédentarité et de l'obésité (sport sur ordonnance, Maison Sport-Santé). "
        "Sensibilisation à l'usage des écrans et au droit à la déconnexion"
    ),
    "seniors": prop(
        "Rénovation énergétique des EHPAD Champs-Manceaux, Raymond-Thomas et Saint-Cyr. "
        "Création de « restaurants séniors » : restauration municipale bio et locale pour les personnes à domicile. "
        "Généralisation de Vill'en Joie : ateliers bien-être, moments conviviaux, visites à domicile, "
        "accompagnement administratif pour rompre l'isolement. "
        "Service public d'accompagnement numérique pour les personnes âgées. "
        "Maintien de la navette du centre-ville. Développement du logement adapté et intergénérationnel"
    ),
    "budget-participatif": prop(
        "Budget participatif renouvelé en biennale, avec une édition annualisée pour les enfants en lien avec les écoles. "
        "Amélioré par des entrées thématiques, par public ou par territoire. "
        "Assemblées de quartier dotées d'un budget propre en investissement et fonctionnement"
    ),
    "transparence": prop(
        "Lancement de Rennes 2050 : large concertation citoyenne pour définir le futur projet urbain. "
        "Création d'Explora'Rennes, comité citoyen des marches exploratoires. "
        "Régies de quartier pour faciliter les initiatives citoyennes. "
        "Convention des jeunesses dédiée à la démocratie locale. "
        "Évaluation participative de tous les dispositifs de la Fabrique citoyenne. "
        "Renouvellement de la Charte de la démocratie locale"
    ),
    "vie-associative": prop(
        "Sanctuarisation des budgets associatifs avec conventions pluriannuelles d'objectifs. "
        "Fonds de dotation et de soutien à l'innovation associative ouvert au mécénat local. "
        "Nouveau pôle associatif à Baud-Chardonnet, tiers-lieu à Maurepas, rénovation maison de quartier Villejean. "
        "Conciergeries de quartier (prêt matériel, mobilier, salles). "
        "Renforcement du pôle 360 de ressources, formation et valorisation de la vie associative. "
        "Ouverture des cours d'école pour les activités associatives. "
        "Lancement de « Ma rue est une fête » avec permis de piétonniser"
    ),
    "services-publics": prop(
        "Élargissement des horaires de certains services publics municipaux. "
        "24 conseillers numériques métropolitains pour l'accompagnement des personnes éloignées du numérique. "
        "Maintien systématique d'un accès non-numérique aux guichets et par téléphone (pas de répondeurs IA). "
        "Territoire zéro non-recours : simplification des démarches, accès aux droits. "
        "Points d'Accès au Droit et Maisons de Justice dans les quartiers populaires"
    ),
    "commerce-local": prop(
        "Rénovation complète du pôle commercial du Gros-Chêne en mail végétalisé. "
        "Ouverture de l'Hôtel-Dieu (restaurants, escalade, co-working, hostellerie). "
        "Projet Palais du Commerce avec commerces, restaurants et hôtellerie. "
        "Soutien aux commerces indépendants dans le centre-ville et les quartiers. "
        "Création d'un marché professionnel pour les circuits courts et produits locaux/bio. "
        "Conseil rennais de l'animation commerciale. "
        "Plaidoyer pour l'encadrement des loyers commerciaux"
    ),
    "emploi-insertion": prop(
        "3e plan Emploi-Quartier pour rapprocher entreprises et demandeurs d'emploi des quartiers prioritaires. "
        "Cité artisanale au Blosne, plateforme d'économie circulaire Halles en Commun (Courrouze). "
        "Maison des livreurs : lieu de repos, accès aux droits et insertion. "
        "Expérimentation Territoire zéro chômeur de longue durée (2e entreprise à but d'emploi). "
        "Clauses sociales dans les marchés publics, stages pour jeunes des quartiers prioritaires. "
        "Soutien à l'économie sociale et solidaire"
    ),
    "attractivite": prop(
        "Filières d'avenir : cybersécurité, IA souveraine et sobre (RAGaRennes), mobilités durables, "
        "éco-construction, spatial, agroalimentaire durable. "
        "Pôle d'excellence industrielle de la Janais (53 ha, mobilité durable et construction bas carbone). "
        "Candidature de Rennes comme capitale verte européenne. "
        "Quartier de la création (industries créatives et culturelles). "
        "Éco-conditionnalité des aides publiques aux entreprises"
    ),
    "equipements-culturels": prop(
        "Rénovation du Triangle (Cité de la Danse) et du Musée des beaux-arts (site Quai Zola). "
        "Nouvelles bibliothèques de quartier à Maurepas (Gros-Chêne) et Beauregard. "
        "Ouverture du Musik Hall au Parc des Expositions : salle de 9 000 places. "
        "Transformation de l'ancienne prison Jacques Cartier en tiers-lieu créatif. "
        "Centre d'arts à hauteur d'enfants (0-10 ans). "
        "Fabrique sonore et numérique pour podcasts et mini-documentaires citoyens"
    ),
    "evenements-creation": prop(
        "Soutien aux scènes ouvertes hors les murs et plateaux de spectacle dans les parcs. "
        "États généraux métropolitains de la culture. "
        "Plateforme pour les pratiques artistiques dans les locaux temporairement inoccupés. "
        "Lieu dédié aux cultures de Bretagne, en lien avec le patrimoine immatériel. "
        "Biennale d'art urbain (street-art), biennale d'art au Couvent des Jacobins. "
        "Nouveau festival d'été pour et par les jeunes Métropolitains. "
        "Rennes comme ville amie du street-art"
    ),
    "equipements-sportifs": prop(
        "Équipement couvert de glisse urbaine dans l'ancienne piscine de Villejean, nouvelle salle au Haut-Sancé. "
        "Rénovation des piscines Saint-Georges et Bréquigny (isolation thermique). "
        "2 gymnases rénovés par an, 2 terrains synthétiques de football par an. "
        "Rénovation : halle des Gayeulles, dojo régional Bréquigny, skate-park Fresnais, "
        "gymnases Blosne et Albert-de-Mun, stade commandant Bougouin. "
        "Augmentation de la jauge du Roazhon Park en lien avec le Stade Rennais FC"
    ),
    "sport-pour-tous": prop(
        "Parcours sport-santé dans la ville utilisant le mobilier urbain, installations plein air « à hauteur d'enfants ». "
        "Sport sur ordonnance, soutien à la Maison Sport-Santé. "
        "Soutien à la pratique sportive des femmes et des filles (critères de mixité, plages horaires réservées). "
        "Tarif étudiant dans les piscines. "
        "Éducateurs sportifs dans les EHPAD. "
        "100% des enfants sachant nager et faire du vélo en fin de primaire"
    ),
    "amenagement-urbain": prop(
        "Aménagement des quais de Vilaine (scène flottante, expos, concerts). "
        "Métamorphose de la place de la République et rue du Pré Botté. "
        "Réaménagement de la dalle du Colombier avec végétation, détente et pôle culturel (ex-cinéma). "
        "Transformation de la dalle du Gros-Chêne en mail végétalisé avec commerces. "
        "Transformation du Palais du commerce, Palais Saint-Melaine, chapelle Saint-Yves, Hôtel-Dieu. "
        "Opérations Bois Perrin (380 logements), Haut-Sancé (500 logements), secteur Technicentre"
    ),
    "accessibilite": prop(
        "Rennes 100% accessible : zéro lieu inaccessible, tous les bâtiments, transports et équipements publics. "
        "Nouvelles places de stationnement PMR dans chaque quartier. "
        "Sensibilisation aux handicaps invisibles, neuro-inclusivité des événements et bâtiments. "
        "Accueil renforcé des enfants à besoins particuliers en centres de loisirs. "
        "Aires de jeux inclusives et pictothèques. "
        "Bourses pour matériel adapté, ateliers de réparation"
    ),
    "quartiers-prioritaires": prop(
        "700 M€ investis dans la rénovation urbaine des quartiers. "
        "Gros-Chêne : 540 logements, mail végétalisé, tiers-lieu citoyen, bibliothèque. "
        "Villejean-Kennedy : 600 logements rénovés, centre de santé, pôle petite enfance, école Trégain. "
        "Gayeulles, Cleunay, Bellangerais : nouveaux logements et espaces publics. "
        "Blosne-Est : place Jean Normand, crèche, commerces. "
        "Bréquigny et Italie : lancement des études et opérations de rénovation"
    ),
    "aide-sociale": prop(
        "« Restaurants séniors » : restauration municipale bio et locale pour les personnes à domicile. "
        "Guichet unique jeunes et bouclier anti-exclusion 16-25 ans (logement, mutuelle, transports, alimentation). "
        "Lieu de répit avec douches, bagagerie et laverie pour les personnes sans-abri. "
        "Hébergement des familles exilées (950 personnes mises à l'abri, soutien Maison des Migrations). "
        "Plan parents solo : garde d'enfant, soutien scolaire, loisirs, vacances, droit au répit. "
        "Expérimentation Territoire zéro chômeur de longue durée"
    ),
    "egalite-discriminations": prop(
        "Lieu métropolitain de ressources et d'accueil pour les victimes de discriminations, avec bus de l'égalité. "
        "Renforcement des formations laïcité pour les agents et acteurs associatifs. "
        "Gratuité des protections menstruelles dans tous les lieux publics, scolaires et sportifs. "
        "Plan de lutte contre les discriminations et observatoire local. "
        "Soutien aux programmes de mentorat et d'accès à la fonction publique pour les jeunes des quartiers. "
        "Expérimentation de médiateurs linguistiques et interprétariat interculturel"
    ),
    "pouvoir-achat": prop(
        "Renforcement des gratuités et tarifs solidaires, développement de la carte Sortir ! "
        "Territoire zéro non-recours : simplification des démarches, Points d'Accès au Droit dans les quartiers. "
        "Fournitures scolaires gratuites. "
        "Raccordement de 16 000 logements au chauffage urbain pour réduire les factures. "
        "Taux de taxe foncière inchangé depuis 15 ans"
    ),
}

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["id"] in ENRICHISSEMENTS:
                st["propositions"]["appere"] = ENRICHISSEMENTS[st["id"]]
                updated += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Count total
    total = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            if st["propositions"].get("appere") is not None:
                total += 1

    print(f"Propositions enrichies : {updated}")
    print(f"Total propositions Appéré : {total}/44 sous-thèmes")

if __name__ == "__main__":
    main()
