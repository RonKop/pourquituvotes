"""
Mapping des propositions de Dino Cinieri - Saint-Étienne 2026
Extrait du programme de 28 pages.
"""

CINIERI_MEASURES = {
    # === SECURITE ===
    "police-municipale": [
        "Création d'une brigade canine d'intervention (BCI) au sein de la police municipale pour faciliter le dialogue et la prévention",
        "Redéploiement de policiers municipaux à pied, à moto et en vélo dans les quartiers pour une présence plus visible et plus efficace",
        "Renforcement des patrouilles de nuit des policiers municipaux pour sécuriser les rues 24h/24",
        "Coopération renforcée entre la police municipale et la police nationale : échanges d'informations hebdomadaires, opérations conjointes",
        "Fermeture des épiceries de nuit à 22h00 avec contrôles fréquents",
        "Dotation de boutons d'alerte chez les commerçants pour sécuriser les commerces",
    ],
    "videoprotection": [
        "Extension du réseau de caméras de vidéoprotection dernière génération, connectées au Centre de supervision urbain",
        "Expérimentation de la surveillance de l'espace public par drones pour lutter contre les rodéos et la circulation inappropriée des vélos et trottinettes",
        "Déployer la vidéoverbalisation contre les dépôts sauvages afin d'identifier et sanctionner les contrevenants",
    ],
    "prevention-mediation": [
        "Plus de moyens à la prévention de la délinquance via le CLSPD et durcissement des arrêtés anti-mendicité et de lutte contre la consommation d'alcool sur la voie publique",
        "Systématisation du rappel à la loi pour les mineurs délinquants, en présence des parents, de la justice et de la police, à l'Hôtel de Ville",
        "Tolérance zéro contre les incivilités et amélioration de l'efficacité des Travaux d'Intérêts Généraux sur le principe « celui qui casse, paie »",
        "Expérimentation d'un couvre-feu pour les mineurs de moins de 16 ans en accord avec les services de l'État",
    ],
    "violences-femmes": [
        "Lutter contre le harcèlement de rue par la formation des policiers municipaux, la verbalisation systématique, des opérations ciblées et des outils d'alerte d'urgence",
        "Déployer un dispositif de protection et d'accompagnement des victimes de violences faites aux femmes et liées au genre, en lien avec les acteurs sanitaires, sociaux, judiciaires et associatifs",
    ],

    # === TRANSPORTS ===
    "transports-en-commun": [
        "Sécurisation des transports en commun et mise en place de boutons d'alerte en station et sur l'application STAS",
        "Réduire le prix de l'abonnement annuel tout public aux transports en commun pour défendre le pouvoir d'achat",
        "Augmenter les fréquences des transports en commun, tôt le matin et en soirée, en lien avec la Métropole et la STAS (CHU, TER, TGV)",
        "Renforcer l'offre de mobilité nocturne en créant un Noctambus+ avec des fréquences doublées",
        "Soutenir le projet de RER stéphanois (Service express régional métropolitain) pour des trains plus fréquents",
        "Renforcer le service Handi'STAS pour améliorer la mobilité des personnes en situation de handicap",
    ],
    "velo-mobilites-douces": [
        "Développer les mobilités douces en sécurisant les itinéraires cyclables existants et en créant des stationnements vélos sûrs près des commerces et pôles de transport",
    ],
    "pietons-circulation": [
        "Étendre les dispositifs d'apaisement de la circulation dans les quartiers résidentiels, en concertation avec les habitants",
        "Créer une Ligne verte stéphanoise, cheminement piéton continu reliant les grandes places jusqu'au stade Geoffroy-Guichard, favorisant la flânerie et les commerces",
    ],
    "stationnement": [
        "Construire un parking en ouvrage place Carnot en délégation de service public",
        "Faciliter le stationnement en créant de nouvelles places de parking et en baissant les tarifs pour maintenir l'accessibilité du centre-ville",
        "Créer des places de stationnement supplémentaires à chaque opportunité, notamment lors des démolitions d'immeubles",
        "Créer davantage de places de stationnement adaptées aux personnes handicapées et renforcer les sanctions pour garantir un accès effectif",
    ],

    # === LOGEMENT ===
    "logement-social": [
        "Garantir la dignité des locataires dans le parc social et privé en luttant contre l'insalubrité, les logements indignes et les dysfonctionnements répétés",
        "Renforcer la lutte contre l'habitat insalubre en mobilisant tous les outils juridiques et opérationnels",
        "Mener une politique du logement équilibrée, favorisant la mixité sociale et générationnelle",
    ],
    "acces-logement": [
        "Développer un nouveau quartier sur le site de la Charité avec un projet architectural exigeant, des logements de qualité et un nouvel espace public",
        "Accompagner la construction et la rénovation de logements adaptés au vieillissement pour favoriser le maintien à domicile",
    ],

    # === EDUCATION ===
    "petite-enfance": [
        "Augmenter les capacités d'accueil en petite enfance en ouvrant de nouvelles places en crèche, en soutenant les initiatives associatives et privées, et en renforçant les relais petite enfance",
        "Développer l'accueil en crèche des enfants en situation de handicap par l'adaptation des structures et la formation des personnels",
    ],
    "ecoles-renovation": [
        "Lancer dès le lendemain de l'élection un état des lieux de toutes les écoles pour intervenir immédiatement partout où la situation l'exige",
        "Planifier les rénovations, extensions et réparations des écoles avec les directeurs et les parents d'élèves",
        "Rendre toutes les écoles réellement inclusives et faciliter l'accès aux sorties scolaires pour les enfants en situation de handicap",
        "Favoriser les classes à petit effectif et lutter contre les fermetures d'écoles et de classes",
        "Recruter, former et valoriser les ATSEM pour améliorer l'accueil et le bien-être des écoliers",
    ],
    "cantines-fournitures": [
        "Atteindre 80 % de produits locaux dans la restauration scolaire, garantir l'accès à la cantine pour tous y compris en cas d'impayé, et associer les parents à l'amélioration du service",
        "Rendre gratuits les transports scolaires et l'accès aux équipements municipaux pour tous les élèves, maintien du budget fournitures scolaires",
    ],
    "periscolaire-loisirs": [
        "Repenser le périscolaire et le temps méridien pour mieux répondre aux besoins des enfants et aux attentes des familles",
        "Renforcer les centres sociaux et les accueils de loisirs pour un périscolaire plus efficace et mieux adapté",
        "Signer une charte de partenariat avec les centres sociaux et les accueils de loisirs pour reconnaître leur rôle et formaliser les engagements avec la Ville",
    ],
    "jeunesse": [
        "Associer le Conseil municipal des enfants et le Conseil consultatif de la jeunesse aux grands projets municipaux",
        "Faire de Saint-Étienne une ville-laboratoire pour les étudiants en les associant concrètement aux projets municipaux",
        "Mettre en place des actions de prévention contre l'addiction aux écrans et le harcèlement scolaire dès l'école primaire",
        "Lancer un programme dédié aux adolescents en situation de handicap pour favoriser autonomie, inclusion sociale et épanouissement",
        "Plan éducation à l'image et aux réseaux sociaux pour apprendre à comprendre, produire et analyser les images, sensibiliser aux médias et aux fake news",
        "Faciliter la mobilité internationale des jeunes Stéphanois grâce à une plateforme recensant les opportunités d'études, de stages et d'échanges",
    ],

    # === ENVIRONNEMENT ===
    "espaces-verts": [
        "Lancer le plan « Moins de bitume, plus de nature » : désimperméabilisation d'environ 15 hectares d'ici 2033 et plantation de 15 000 végétaux, en priorité autour des écoles et places",
        "Soutenir et développer les jardins partagés et familiaux en améliorant leur accessibilité et leur sécurité",
        "Faire des parcs et jardins de véritables poumons verts et créer de nouveaux espaces végétalisés lors des opérations de renouvellement urbain",
        "Renforcer le fleurissement et la qualité paysagère de la ville",
        "Embellir rues et places par la végétalisation, les fleurs, les décors et les éclairages",
    ],
    "proprete-dechets": [
        "Réorganiser la propreté municipale pour garantir des passages réguliers dans tous les quartiers, avec priorité au centre-ville et zones commerçantes",
        "Créer une brigade verte chargée de faire respecter l'hygiène publique, verbaliser les incivilités et mener des actions de médiation",
        "Lancer le service « Propreté 48h maximum » pour signaler un problème et garantir une intervention sous 48h",
        "Renforcer fortement les équipes anti-tags pour une intervention rapide et systématique",
        "Mettre en place un service gratuit d'enlèvement des encombrants sur rendez-vous, avec des sanctions contre les dépôts sauvages",
        "Rendre les sanctions réellement dissuasives en augmentant les amendes et en durcissant les peines en cas de récidive",
        "Organiser chaque trimestre un grand nettoyage de quartier sur 48h avec renfort des équipes et mise à disposition de bennes",
        "Sensibiliser dès le plus jeune âge au respect de l'espace public par des actions pédagogiques dans les écoles",
    ],
    "climat-adaptation": [
        "Renforcer la place de l'eau en ville par des aménagements apportant fraîcheur et confort face au changement climatique",
        "Installer des fontaines à eau sur les places et lieux de vie pour améliorer le confort lors des fortes chaleurs",
        "Faire de la protection et de la gestion de l'eau une priorité pour lutter contre les îlots de chaleur et préserver les milieux naturels",
        "Contribuer à une baisse d'environ 30 % des émissions de gaz à effet de serre sur la mandature, avec Saint-Étienne Métropole",
        "Soumettre les grands projets municipaux à une évaluation d'impact sur le climat, la santé, le cadre de vie et l'environnement",
    ],
    "renovation-energetique": [
        "Accélérer le plan façades pour valoriser l'architecture et encourager la rénovation du bâti existant",
    ],
    "alimentation-durable": [
        "Transformer les friches urbaines en opportunités écologiques en développant l'agriculture urbaine, les circuits courts et l'éducation environnementale",
    ],

    # === SANTE ===
    "centres-sante": [
        "Déployer un médicobus de télémédecine accessible aux personnes en situation de handicap pour garantir l'accès aux soins dans tous les quartiers",
        "Créer un « Pack Médecins Saint-Étienne » pour attirer médecins généralistes et spécialistes : locaux, accompagnement logement, garde d'enfants et emploi du conjoint",
        "Favoriser l'offre de stages, de formations complémentaires et d'internat afin d'attirer des étudiants en médecine et permettre leur installation",
        "Soutenir et faciliter les maisons de santé privées pour renforcer l'offre de soins de proximité",
    ],
    "prevention-sante": [
        "Lancer un Plan Bien-être et Cancer pour mieux prévenir, soigner, accompagner les malades et renforcer la santé mentale",
        "Instaurer chaque année une grande cause municipale de santé (2026 : l'endométriose)",
        "Soutenir le futur pôle municipal de santé mentale pour informer, prévenir, orienter et lutter contre la stigmatisation",
        "Faire de Saint-Étienne une ville de référence en sport-santé en développant le sport sur ordonnance et des programmes pour les personnes en rémission",
    ],
    "seniors": [
        "Créer le Pass Loisirs Seniors+, associant une offre de loisirs renforcée et un crédit annuel de 15 € dans les commerces stéphanois",
        "Réaliser un état des lieux complet des résidences municipales seniors et engager les travaux nécessaires",
        "Développer la médiation animale auprès des personnes malades, âgées ou fragilisées dans les établissements de santé",
        "Développer par le design des quartiers adaptés au bien vieillir, en soutenant les projets intergénérationnels et le lien social",
        "Favoriser les liens intergénérationnels en développant les échanges entre étudiants et seniors",
        "Soutenir le futur projet de Maison d'accompagnement pour la fin de vie",
    ],

    # === DEMOCRATIE ===
    "budget-participatif": [
        "Rouvrir les conseils de quartier, réunis 4 fois par an, comme véritables espaces d'échange et de propositions ouverts à tous",
        "Associer les citoyens, les associations et les acteurs locaux au suivi et à l'évaluation de la transition écologique",
    ],
    "transparence": [
        "Lancer un audit général des finances de la Ville pour connaître précisément la santé financière de la collectivité",
        "Mettre en place une véritable démarche qualité avec évaluations, contrôles et audits réguliers pour garantir la bonne utilisation de l'argent public",
        "Mettre en place un tableau de bord public du développement durable avec des indicateurs simples, quartier par quartier",
        "Protéger le pouvoir d'achat des Stéphanois par une fiscalité maîtrisée, sans hausse des impôts locaux",
        "Rendre l'information publique accessible et compréhensible à tous en mettant en place des retranscriptions en FALC (Facile à Lire et à Comprendre)",
        "Généraliser la concertation pour les projets d'aménagement urbain en associant habitants, usagers et acteurs locaux en amont",
    ],
    "vie-associative": [
        "Former et accompagner les bénévoles mobilisés lors des événements municipaux (accueil, sécurité, secourisme)",
        "Mettre en place une politique de reconnaissance des bénévoles avec des cérémonies et trophées réguliers",
        "Soutenir les associations en valorisant dans l'attribution des subventions les projets qui renforcent la vie des quartiers et le lien social",
        "Adopter une charte municipale encadrant l'attribution des subventions pour assurer le respect des principes républicains et de la laïcité",
    ],
    "services-publics": [
        "Instaurer un dialogue permanent entre les élus et les habitants, avec des permanences mensuelles dans chaque quartier",
        "Rationaliser et renforcer les conseils consultatifs thématiques en clarifiant leur rôle et en leur donnant de véritables moyens d'action",
        "Lancer le programme « Saint-Étienne IA publique » pour moderniser les services municipaux, simplifier les démarches et accélérer les traitements",
        "Garantir une gestion rigoureuse des finances municipales en maîtrisant les dépenses de fonctionnement sans dégrader la qualité du service public",
        "Déployer un outil numérique de géolocalisation des lieux et équipements accessibles pour faciliter les déplacements",
    ],

    # === ECONOMIE ===
    "commerce-local": [
        "Encadrer les nouvelles ouvertures de commerces par une autorisation préalable pour préserver la diversité commerciale et lutter contre la monoactivité",
        "Redonner vie aux arcades de l'Hôtel de Ville en proposant des cellules commerciales gratuites pour tester des concepts",
        "Créer des « cœurs de quartiers » combinant aménagements de qualité, diversité commerciale et animations régulières",
        "Lancer le pack « J'ouvre ma boutique à Saint-Étienne » avec accompagnement complet, interlocuteur unique et délais garantis sous 30 jours",
        "Déployer la plateforme « Acheter Sainté » pour permettre aux commerçants de vendre en ligne (marketplace, click & collect, livraison)",
        "Embellir les vitrines et lutter contre la vacance commerciale par l'application stricte du règlement des enseignes",
        "Renforcer la foncière commerciale pour reprendre la main sur les rez-de-chaussée et diversifier l'offre de proximité",
        "Protéger et accompagner les commerçants pendant toute la durée des travaux du tramway (Plan Marshall centre-ville)",
    ],
    "emploi-insertion": [
        "Lancer le plan « Parcours PME Stéphanois » pour retenir les diplômés via une plateforme unique de stages, d'alternance et d'emplois dans les PME",
        "Développer des formations en adéquation avec les besoins réels des entreprises locales, notamment dans les métiers en tension",
        "Soutenir les associations d'insertion par l'emploi pour favoriser un retour à l'activité et à la dignité",
        "Intégrer systématiquement des clauses sociales dans les marchés publics pour favoriser l'insertion professionnelle",
        "Créer le « Pack Talents Sainté » pour attirer et accueillir les jeunes actifs avec guichet unique, conciergerie d'installation et parcours d'intégration",
        "Mettre en place des dispositifs de parrainage entre cadres d'entreprises locales et étudiants pour faciliter l'orientation professionnelle",
    ],
    "attractivite": [
        "Faire de Saint-Étienne une véritable ville touristique avec une stratégie claire et un Office de tourisme ouvert toute l'année",
        "Densifier et diversifier l'offre hôtelière et de restauration pour accompagner le tourisme événementiel",
        "Faciliter la découverte de Saint-Étienne par des parcours piétonniers lisibles et une signalétique touristique par pictogrammes",
        "Faire de Saint-Étienne une destination week-end grâce à des offres combinées et un tourisme autour de l'identité stéphanoise et footballistique",
        "Soutenir le développement de l'aéroport de Saint-Étienne Loire en renforçant les liaisons et diversifiant ses activités",
        "Chaque euro investi par la Ville devra soutenir l'économie locale : commande publique et investissement municipal comme leviers du développement",
        "Créer une instance permanente de dialogue économique réunissant des chefs d'entreprise de tous les secteurs",
        "Déployer une offre d'immobilier d'entreprise diversifiée et compétitive, en particulier en centre-ville",
        "Rééquilibrer l'activité économique entre Châteaucreux, le Technopôle et le centre-ville",
        "Soutenir les filières d'excellence pour renforcer leur visibilité et compétitivité à l'échelle nationale et internationale",
        "Développer de nouvelles pépinières d'entreprises et renforcer les structures existantes pour accompagner la création d'entreprises",
        "Soutenir le développement de l'économie sociale et solidaire",
        "Créer un club des ambassadeurs économiques de Saint-Étienne pour promouvoir les atouts de la ville",
        "Faire de Saint-Étienne la capitale française de l'industrie du futur en fédérant entreprises, start-up, écoles et chercheurs",
        "Renforcer la participation de Saint-Étienne aux programmes nationaux et européens d'innovation",
        "Structurer une filière locale du numérique et de l'IA, créatrice d'emplois, en s'appuyant sur le design et l'innovation industrielle",
        "Déployer une stratégie de marketing territorial à l'international pour valoriser l'image et les savoir-faire de Saint-Étienne",
        "Renforcer et dynamiser les partenariats internationaux dans les domaines culturel, économique, éducatif et institutionnel",
        "Mobiliser les financements internationaux, notamment européens, pour soutenir les projets locaux",
    ],

    # === CULTURE ===
    "equipements-culturels": [
        "Redonner à la Cité du design sa vocation de développement économique en faisant du design un levier d'innovation et de création d'emplois",
        "Remettre le design au cœur de l'action municipale comme outil de transformation urbaine adapté aux usages réels des Stéphanois",
        "Créer un véritable quartier de créateurs en centre-ville rassemblant galeries, boutiques, ateliers et initiatives culturelles",
        "Créer un parcours « Saint-Étienne, ville de design » au départ de la Cité pour renforcer l'attractivité touristique",
        "Développer une véritable éducation culturelle dès le plus jeune âge en facilitant l'accès à la lecture, à l'écriture et aux lieux culturels",
        "Faire du Puits Couriot un site phare de l'animation stéphanoise grâce à une programmation culturelle et événementielle régulière",
        "Prise en charge intégrale des transports scolaires vers les lieux culturels et sportifs (bibliothèques, stades, piscines)",
        "Lancer le programme « Les voix de Saint-Étienne » pour collecter et valoriser les récits de vie des quartiers",
    ],
    "evenements-creation": [
        "Faire de la Sainte-Barbe la grande fête populaire de toute la ville, célébrée dans tous les quartiers",
        "Renforcer les fêtes de fin d'année avec un marché de Noël renforcé et des animations locales dans les quartiers",
        "Garantir des animations culturelles et festives régulières dans tous les quartiers",
        "Renforcer la Fête du Livre par davantage d'animations, de spectacles vivants et de rendez-vous musicaux",
        "Densifier la programmation estivale en plein air avec des animations musicales et artistiques",
        "Redonner vie au kiosque de la place Jean-Jaurès avec des animations culturelles et musicales",
        "Soutenir la création artistique et les artistes par une politique culturelle équitable et ouverte, en renforçant le tissu associatif",
        "Décentraliser la culture dans tous les quartiers en soutenant la création artistique dans l'espace public",
        "Favoriser le mécénat et le financement participatif pour soutenir les événements culturels",
        "Organiser chaque trimestre des « puces design & vintage » en centre-ville",
        "Animer le centre-ville tous les week-ends en mobilisant les associations avec les commerçants",
        "Diversifier les spectacles lumineux lors des événements municipaux (drones, mises en lumière) pour réduire les nuisances sonores et respecter le bien-être animal",
    ],

    # === SPORT ===
    "equipements-sportifs": [
        "Lancer le plan « Sainté sait nager » : 3 piscines ouvertes toute l'année, 2 en période estivale, renforcement des maîtres-nageurs, modernisation énergétique et étude d'un bassin nordique",
        "Créer un grand espace dédié au roller et aux sports de glisse urbaine en réinventant la patinoire sur le modèle de La Main Jaune",
        "Adapter l'espace public au sport urbain en développant des équipements favorisant les pratiques libres et accessibles à tous",
        "Valoriser les atouts naturels et urbains du territoire (sports nautiques à Saint-Victor-sur-Loire, sports de nature à Rochetaillée, sports urbains en centre-ville)",
    ],
    "sport-pour-tous": [
        "Accompagner le développement des clubs sportifs et valoriser toutes les disciplines sportives",
        "Organiser une grande Nuit du Sport pour mettre à l'honneur les champions stéphanois de l'année",
        "Replacer l'ASSE au cœur de la ville par un partenariat Ville-club : programme « ASSE Cœur de Ville », Ligne verte supporter, partenariat socio-éducatif",
        "Accueillir de grandes compétitions sportives populaires comme le Tour de France",
        "Organiser un grand événement sportif estival proposant des initiations aux différentes disciplines sportives",
        "Développer et accompagner la pratique autonome du sport, notamment la course à pied, avec des parcours de running traversant la ville",
        "Renforcer l'offre de l'École municipale des sports pour permettre au plus grand nombre de pratiquer une activité sportive",
        "Organiser les États généraux du sport pour associer clubs, pratiquants et bénévoles à une stratégie sportive partagée",
        "Mettre en œuvre un plan handisport et sport adapté pour lever les freins à la pratique pour les personnes en situation de handicap",
    ],

    # === URBANISME ===
    "amenagement-urbain": [
        "Embellir les grandes places du centre-ville et proposer des aménagements adaptés à leurs usages",
        "Déployer un plan lumière pour valoriser les sites emblématiques, renforcer le sentiment de sécurité et l'attractivité nocturne",
        "Relocaliser emplois et services en centre-ville en transformant les locaux vacants",
        "À chaque démolition d'immeubles, étudier systématiquement la création de parcs urbains ou de parkings",
        "Déployer des toilettes publiques propres, accessibles et régulièrement entretenues sur l'ensemble de la ville",
        "Déployer une démarche de design appliqué aux commerces et aux rues, en lien avec la Cité du design",
        "Lancer des concours de design participatif associant enfants, jeunes et seniors pour imaginer aires de jeux, mobilier urbain et espaces publics",
        "Engager une double transition écologique et numérique en utilisant le numérique pour mieux piloter l'énergie, l'eau et les déchets",
    ],
    "accessibilite": [
        "Faire de l'inclusion des personnes en situation de handicap un principe transversal de toutes les politiques municipales",
        "Créer une délégation municipale dédiée et sanctuarisée au handicap",
        "Mettre en place un groupe de travail permanent sur le handicap associant personnes concernées, associations et services municipaux",
        "Rendre pleinement accessible l'espace public par un programme ambitieux sur les trottoirs, transports, équipements et bâtiments municipaux",
        "Installer davantage de bancs et de toilettes propres et accessibles dans l'espace public pour une ville confortable à tous les âges",
    ],
    "quartiers-prioritaires": [
        "Lancer le réseau « Vivre Ensemble à Saint-Étienne » pour favoriser le dialogue citoyen et interreligieux et renforcer la cohésion sociale",
    ],

    # === SOLIDARITE ===
    "aide-sociale": [
        "Soutenir le tissu associatif solidaire qui agit au quotidien auprès des publics fragiles",
        "Renforcer le rôle du CCAS pour garantir un accompagnement social réactif, humain et accessible aux Stéphanois les plus vulnérables",
        "Réaffirmer l'engagement en faveur de la protection animale en transférant à la SPA la propriété du site qu'elle occupe",
        "Créer un budget municipal consacré au bien-être animal pour soutenir des actions concrètes de protection et de sensibilisation",
        "Financer la stérilisation et l'identification des chats errants en partenariat avec les associations et vétérinaires",
    ],
    "egalite-discriminations": [
        "Instaurer une cérémonie d'accueil des nouveaux citoyens français",
        "Renforcer la formation des agents municipaux et des associations pour garantir la transmission des valeurs républicaines et de la laïcité",
        "Travailler sur l'inclusion culturelle afin que chaque enfant ait accès à la culture quel que soit son milieu et son quartier",
        "Sensibiliser les habitants aux usages et enjeux de l'IA afin de favoriser une appropriation éclairée et éthique",
    ],
    "pouvoir-achat": [
        "Désendetter la ville pour préserver la capacité d'investissement",
        "Mobiliser les financements de l'État et des partenaires publics pour éviter toute hausse des impôts locaux",
    ],
}


# Comptage total
total = sum(len(v) for v in CINIERI_MEASURES.values())
print(f"Nombre total de mesures extraites : {total}")
print(f"Nombre de sous-thèmes utilisés : {len(CINIERI_MEASURES)}")
print()
for category, measures in CINIERI_MEASURES.items():
    print(f"  {category}: {len(measures)} mesures")
