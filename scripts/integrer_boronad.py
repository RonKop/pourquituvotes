"""
Intégration du programme de Julie Boronad (Aix en commun / LFI) — 165 mesures
Source : https://www.aixencommun.fr/programme/
"""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FICHIER = r"C:\Users\KOPELMANRon\projets perso\FR comp mun\data\elections\aix-en-provence-2026.json"

SOURCE = "Programme officiel 2026 — Aix en commun"
SOURCE_URL = "https://www.aixencommun.fr/programme/"

# Mapping: sous-theme -> liste de mesures
PROPOSITIONS = {
    "police-municipale": [
        "Implanter une police municipale de proximité dans tous les quartiers, avec des référents identifiés pour renforcer les missions de proximité (lutte contre les incivilités, médiation de voisinage, accompagnement des personnes fragiles)."
    ],
    "videoprotection": [
        "Encadrer strictement la vidéosurveillance avec un moratoire sur toute nouvelle installation, retrait des dispositifs d'intelligence artificielle et évaluation par un comité citoyen indépendant."
    ],
    "prevention-mediation": [
        "Renforcer massivement les effectifs de médiateurs sur les enjeux clés (logement social, jeunesse, santé, addictions, relation police-population) et déployer dans chaque quartier une politique de prévention coordonnée avec associations, collectifs et police municipale.",
        "Mettre en place une réponse sanitaire et humaine aux situations de détresse psychique : former la police municipale à la désescalade de conflits, renforcer les équipes d'intervention pluridisciplinaires associant professionnels de santé et travailleurs sociaux.",
        "Créer un lieu d'accueil des personnes en situation d'addiction pour réduire les risques et apaiser l'espace public, en lien avec les associations spécialisées.",
        "Renforcer la prévention face aux usages de drogues et aux réseaux : formations régulières dans les collèges et lycées pour sensibiliser aux risques, aider les parents à repérer les signes de fragilité.",
        "Instaurer les arrêts à la demande pour les bus de nuit afin que personne ne marche seul trop longtemps dans des zones isolées.",
        "Améliorer et adapter l'éclairage public : ni trop sombre pour la sûreté, ni trop polluant (détecteurs de présence, panneaux solaires)."
    ],
    "violences-femmes": [
        "Créer une maison des femmes accueillant des actions de prévention, de santé et d'orientation, en lien avec le Planning familial.",
        "Soutenir la création d'un centre féministe au sein de la Maison des femmes, mis à disposition des associations et collectifs.",
        "Protéger et accompagner les victimes de VSS : renforcer leur accueil, développer l'hébergement d'urgence, prioriser leur accès au logement social, créer un guichet unique au sein de l'Observatoire des discriminations.",
        "Sensibiliser aux violences sexistes par des campagnes de sensibilisation et d'éducation populaire."
    ],
    "transports-en-commun": [
        "Adapter les transports au rythme de vie des Aixois en élargissant les horaires et renforçant les fréquences (notamment les week-ends), prioriser les quartiers sous-desservis et rétablir un véritable service de nuit.",
        "Développer le réseau en s'appuyant sur les Conseils de quartier pour mieux relier les quartiers entre eux.",
        "Garantir l'accessibilité universelle des transports publics par un programme accéléré de mise aux normes PMR et de sécurisation des arrêts de bus. Renforcer fortement le transport à la demande.",
        "Lancer le projet du Tram-Train pour desservir les zones résidentielles au nord, désengorger la RN 296 et la D9, et desservir la Pioline, Plan d'Aillane, les Milles, la Duranne et la gare TGV.",
        "Travailler à la mise en place d'une véritable liaison RER entre Aix et Marseille.",
        "Créer de véritables plateformes multimodales dans les grands points de connexion (parkings-relais, aires de covoiturage, gare routière, gares SNCF)."
    ],
    "velo-mobilites-douces": [
        "Faire du vélo un mode de déplacement sûr et pratique grâce à un réseau cyclable continu et séparé. Déploiement massif de stationnements vélo sécurisés (abris, box) et développement de vélo-écoles.",
        "Expérimenter et évaluer un nouveau système de locations de vélos en libre-service."
    ],
    "pietons-circulation": [
        "Redonner la priorité aux piétons et personnes à mobilité réduite en créant de grandes liaisons piétonnes continues entre quartiers, écoles, services publics et pôles d'échange, avec des trottoirs larges, accessibles et dégagés.",
        "Sécuriser et apaiser les abords des écoles avec davantage de « Rues aux écoles » : piétonniser et végétaliser progressivement, fermer la circulation aux heures d'entrée et de sortie."
    ],
    "tarifs-gratuite": [
        "Étendre la gratuité des transports aux jeunes de moins de 26 ans et s'engager dans la voie d'une gratuité totale."
    ],
    "logement-social": [
        "Construire 450 logements par an dont 40% très sociaux pour atteindre l'objectif légal de 25%.",
        "Mettre fin au clientélisme et aux discriminations dans l'attribution des logements sociaux : règles débattues et votées en conseil municipal, formation des commissions d'attribution.",
        "Création d'un organisme foncier solidaire pour développer le bail réel solidaire (BRS) afin de diminuer le coût du logement."
    ],
    "logements-vacants": [
        "Diminuer la vacance en utilisant tous les outils disponibles : taxe sur les logements vacants, bail à réhabilitation sociale, bail emphytéotique, et remettre en location des logements vacants du centre-ville.",
        "Acquérir à l'amiable (ou exproprier) des bâtiments insalubres du centre-ville pour en faire des lieux de vie (logements sociaux, services publics, commerces).",
        "Demander la réquisition des bâtiments vacants pour en faire des logements d'urgence ou d'hébergement temporaire."
    ],
    "encadrement-loyers": [
        "Mettre en place l'encadrement des loyers, en limitant les prix à la location sur la base d'un loyer de référence juste défini par quartier, taille et type de location.",
        "Encadrer les locations touristiques : plafonnement à 90 jours pour les résidences principales, contrôles réguliers des annonces frauduleuses.",
        "Relever les taxes sur les résidences secondaires.",
        "Étendre le permis de louer bien au-delà de la résidence des Facultés sur tous les lieux d'habitat indigne et insalubre. Exécution d'office des travaux si le propriétaire est défaillant."
    ],
    "acces-logement": [
        "Utiliser pleinement le droit de préemption de la ville et l'étendre au-delà du centre-ville.",
        "Définir et négocier une « charte promoteur » indiquant le prix de vente moyen et maximum, imposant des normes écologiques et donnant priorité d'acquisition aux demandeurs de la commune.",
        "Aider à la gestion locative et à la garantie de loyer par des mesures d'accompagnement.",
        "Créer une brigade municipale du logement composée d'équipes de terrain pour défendre les locataires, anticiper les situations de logement indigne, prévenir les expulsions et contrôler le permis de louer.",
        "Créer un Office municipal du logement étudiant pour construire des résidences dont la gestion sera confiée au CROUS ou à des bailleurs sociaux.",
        "Développer le parc CROUS par une recherche de foncier et une priorité donnée sur les opérateurs privés."
    ],
    "petite-enfance": [
        "Préparer le retour en régie publique des crèches municipales pour mettre fin à la recherche de rentabilité des acteurs privés.",
        "Garantir à toutes les familles un accès effectif et abordable à un mode de garde, en priorité dans les quartiers populaires. Développer les crèches municipales, soutenir les crèches associatives, mettre en place une aide municipale réduisant le reste à charge.",
        "Développer des centres de parentalité dans les centres sociaux."
    ],
    "ecoles-renovation": [
        "Relancer un plan de rénovation axé sur l'ombre et la fraîcheur : végétaliser et désimperméabiliser systématiquement les cours d'écoles pour lutter contre les îlots de chaleur.",
        "Sécuriser les abords des écoles avec davantage de Rues aux écoles : piétonniser, végétaliser, fermer la circulation aux heures d'entrée et de sortie.",
        "Affirmer la priorité donnée à l'école publique avec des subventions au privé limitées au minimum légal."
    ],
    "cantines-fournitures": [
        "Rendre la cantine 100% bio et progressivement gratuite.",
        "Sécuriser les approvisionnements en développant les partenariats avec les producteurs locaux.",
        "Développer les petits déjeuners gratuits pour qu'aucun enfant ne commence la journée le ventre vide.",
        "Exclure les additifs chimiques problématiques des marchés publics liés à l'alimentation."
    ],
    "periscolaire-loisirs": [
        "Organiser le temps périscolaire avec un accueil jusqu'à 18h30, assurer un accompagnement scolaire de qualité en élargissant les études dirigées et le soutien scolaire à toutes les écoles publiques.",
        "Redonner aux centres sociaux un rôle central dans l'éducation et la vie des quartiers.",
        "Reconnaître pleinement le rôle des ATSEM et affecter 100% de leurs missions sur le temps scolaire.",
        "Suivre et évaluer l'encadrement des enfants par un registre public et transparent des effectifs (ATSEM, AESH, agents d'animation) présenté à chaque conseil d'école."
    ],
    "jeunesse": [
        "Créer une plateforme municipale pour les stages et lutter contre les stages non-rémunérés.",
        "Accompagner à la rédaction de CV et à l'orientation, y compris des jeunes en recherche d'emploi, en lien avec la Mission locale.",
        "Créer de nouvelles MJC (Maisons des Jeunes et de la Culture), les soutenir financièrement et les inclure dans la politique culturelle.",
        "Inscrire les propositions du Conseil de la Vie Étudiante à l'ordre du jour du conseil municipal.",
        "Organiser des campagnes d'inscription sur les listes électorales en partenariat avec l'Université et le CROUS.",
        "Lutter contre la précarité menstruelle en développant les distributeurs et la mise à disposition de protections réutilisables.",
        "Développer les épiceries solidaires, notamment sur chaque campus, en s'appuyant sur les associations.",
        "Ouvrir l'accès à la mutuelle municipale aux étudiants et jeunes.",
        "Faire de la santé mentale des jeunes une priorité : création d'un CMP Jeunes et de lieux d'écoute gratuits sans rendez-vous.",
        "Développer une politique de prévention et de réduction des risques : faciliter l'accès aux moyens de contraception et aux dépistages."
    ],
    "espaces-verts": [
        "Déployer une stratégie ambitieuse de végétalisation et de ventilation naturelle : diagnostics par quartiers, objectifs chiffrés (arbres plantés, surfaces végétalisées), création de micro-forêts urbaines.",
        "Lancer un plan d'ombrage dans les rues trop étroites : installer des voiles, pergolas végétalisées ou structures d'ombre coconstruites avec les habitants, en priorité autour des écoles et quartiers denses."
    ],
    "proprete-dechets": [
        "Améliorer la propreté et l'attractivité des marchés et des rues commerçantes."
    ],
    "climat-adaptation": [
        "Créer une délégation à la planification écologique qui coordonnera les services municipaux, évaluera les politiques publiques et garantira la transparence et le contrôle citoyen.",
        "Construire un diagnostic partagé des urgences locales (chaleur, feux de forêt, inondations) en s'appuyant sur les Conseils de quartier et les associations.",
        "Protéger les plus vulnérables en adoptant un plan Canicule renforcé : multiplier les lieux d'accueil frais, y compris par réquisition si nécessaire.",
        "Lutter contre l'artificialisation des sols et l'étalement urbain en privilégiant la densification de l'habitat existant.",
        "Protéger les habitants face aux pollutions en créant un observatoire Santé-Environnement.",
        "Lutter contre les risques de feux de forêt en créant un service municipal de débroussaillement et un plan pluriannuel de gestion des Points d'Eau Incendie.",
        "Créer un réseau municipal d'entraide formant massivement les habitants aux premiers secours pour assister les personnes fragiles et relayer les alertes."
    ],
    "renovation-energetique": [
        "Accélérer la réhabilitation thermique des logements sociaux et bâtiments publics. Créer une coopérative municipale d'éco-rénovation avec accès facilité aux matériaux écologiques et formation des professionnels.",
        "Favoriser l'implantation de panneaux solaires en toiture sur les bâtiments publics et dans les nouveaux projets immobiliers."
    ],
    "alimentation-durable": [
        "Soutenir des expérimentations de Sécurité Sociale de l'Alimentation (SSA) : faciliter l'accès aux financements, mettre des locaux à disposition, appuyer les caisses solidaires.",
        "Rendre l'alimentation locale plus accessible dans les quartiers en renforçant les circuits courts. Soutenir la création de coopératives d'achats. Favoriser l'implantation de jardins partagés.",
        "Protéger et développer une agriculture durable en sanctuarisant les terres agricoles et en favorisant l'installation de nouveaux exploitants.",
        "Développer les solutions de captage des eaux individuelles et collectives."
    ],
    "centres-sante": [
        "Défendre l'hôpital public : exiger l'arrêt des fermetures de services et la réouverture des lits supprimés. Réserver les investissements municipaux aux établissements publics.",
        "Créer des centres de santé municipaux pluridisciplinaires en ciblant les quartiers populaires, avec si nécessaire l'embauche directe de médecins salariés.",
        "Créer une mutuelle municipale fondée sur une prise en charge éthique, sans dépassements d'honoraires ni conditions restrictives."
    ],
    "prevention-sante": [
        "Faire de la santé mentale une priorité de santé publique municipale : plan municipal de prévention et d'accueil des personnes en souffrance psychique, soutien renforcé aux Centres Médico-Psychologiques.",
        "Instaurer la gratuité des premiers m3 d'eau indispensables à la vie, avec une tarification progressive et différenciée selon les usages."
    ],
    "seniors": [
        "Favoriser le maintien à domicile en lien avec les acteurs de santé et les associations d'aidants. La Brigade du logement assurant un rôle d'alerte et de prévention.",
        "Augmenter l'offre publique en créant de nouvelles résidences publiques type EHPAD ou associatives sans but lucratif pour personnes âgées.",
        "Aider au développement du logement intergénérationnel avec une plateforme de mise en relation et un accompagnement."
    ],
    "budget-participatif": [
        "Faire des Conseils de quartier des acteurs de la vie locale en les dotant de budgets participatifs (fonctionnement et investissement), avec engagement d'inscrire leurs projets à l'ordre du jour du conseil municipal.",
        "Démocratiser l'élaboration du budget avec l'organisation d'un débat d'orientation public et participatif au sein des Conseils de quartier.",
        "Instaurer le Référendum d'Initiative Citoyenne : un RIC peut être déclenché par 10% des électeurs ; si la participation dépasse 50%, le résultat est appliqué."
    ],
    "transparence": [
        "Mettre en place une communication transparente et garantir l'accès aux documents municipaux. L'application « Aix ma ville » centralisera services, démarches et participation citoyenne.",
        "Instaurer le droit de pétition : si elle réunit au moins 5% des habitants de plus de 16 ans, elle est défendue en conseil municipal.",
        "Soutenir la participation des mineurs dès 16 ans et des résidents étrangers aux instances locales et au droit de pétition.",
        "Mener des campagnes d'inscription sur les listes électorales et mettre fin aux radiations abusives.",
        "Garantir la transparence de l'action municipale : rendre publiques toutes les études commandées par la mairie, appliquer les avis de la CADA.",
        "Encadrer l'action des élus par une charte pour le respect des engagements pris.",
        "Mettre en place une politique d'Open Data pour garantir l'accès aux données publiques.",
        "Prévenir les conflits d'intérêts : publier les rendez-vous des élus avec les représentants d'intérêts privés, refuser tout cadeau, obligation de retrait des débats ou votes concernés.",
        "Imposer la sobriété dans l'utilisation de l'argent public : encadrer les frais de réception, publier l'intégralité des frais de représentation des élus.",
        "Garantir une attribution juste et transparente des ressources publiques (logements sociaux, places en crèches, marchés publics) grâce à la présence d'habitants dans les conseils d'administration."
    ],
    "vie-associative": [
        "Donner de la stabilité aux associations par des conventions et subventions pluriannuelles.",
        "Empêcher le clientélisme dans l'attribution des subventions par un cahier des charges clair : utilité sociale, égalité femmes-hommes, conditions de travail dignes.",
        "Garantir un accès équitable aux ressources municipales : plateforme publique des lieux municipaux disponibles, prêt gratuit des équipements aux associations et collectifs.",
        "Recréer une maison des associations, cogérée avec la municipalité.",
        "Mettre en place des partenariats avec les associations pour l'élaboration des politiques locales."
    ],
    "services-publics": [
        "Œuvrer pour le retour de compétences à la ville, avec en premier lieu la compétence voirie.",
        "Garantir le choix entre démarche physique et dématérialisation.",
        "Assurer un rôle d'accompagnement numérique avec des services dédiés dans les mairies annexes et centres sociaux.",
        "Garantir la stabilité de l'emploi public en lançant un plan de titularisation des emplois permanents, en priorité les personnels de catégorie C.",
        "Développer le plan pluriannuel de formation des personnels municipaux.",
        "Redonner à la ville une ingénierie publique forte en reconstituant des filières municipales (bâtiment, voirie, énergie, espaces verts) pour réduire la dépendance aux cabinets extérieurs.",
        "Faire de la commande publique un levier de la bifurcation écologique en renforçant les clauses environnementales dans tous les marchés municipaux."
    ],
    "commerce-local": [
        "Protéger les commerces de proximité en renforçant le droit de préemption sur les commerces et l'artisanat. Acquérir des murs, rénover des locaux et les relouer à des loyers abordables dans les quartiers sous-dotés. Soutenir les commerces coopératifs.",
        "Protéger et développer les marchés comme piliers du lien social et de l'économie locale, prioriser la présence des producteurs locaux.",
        "Protéger les espaces agricoles par une sanctuarisation dans le PLUI.",
        "Soutenir les agriculteurs locaux par la commande publique et favoriser l'installation de nouveaux exploitants avec un guichet municipal d'accompagnement."
    ],
    "emploi-insertion": [
        "Utiliser la commande publique comme levier avec des clauses sociales et environnementales dans les marchés publics (SCOP, associations locales, circuits courts).",
        "Réserver du foncier pour des projets coopératifs (habitat participatif, commerces coopératifs).",
        "Aider à la structuration de filières locales (alimentation, ressourceries, recycleries, coopératives culturelles).",
        "Former les agents municipaux aux achats responsables."
    ],
    "equipements-culturels": [
        "Rééquilibrer l'accès à la culture sur le territoire : créer de nouveaux lieux culturels en réhabilitant des locaux vacants ou en préemptant des commerces, en priorité dans les quartiers dépourvus.",
        "Faire des lieux culturels de véritables espaces de vie de quartier : élargir les horaires des bibliothèques, accueillir débats, rencontres et fêtes.",
        "Rebâtir un Muséum d'Histoire Naturelle afin de faire profiter de ses collections.",
        "Mettre fin au manque d'espaces pour la création artistique : créer un réseau de lieux de répétition, de stockage et d'exposition.",
        "Aider les petits lieux de musiques actuelles : soutien pour les licences de spectacles, information sur les aides à l'emploi artistique."
    ],
    "evenements-creation": [
        "Faire de l'accès à la culture un droit effectif : renforcer la tarification sociale, proposer des places à très bas coût et des gratuités ciblées.",
        "Rompre avec la hiérarchie entre cultures « élitistes » et populaires : ouvrir les lieux culturels aux créations urbaines (hip-hop, rap, stand-up) et soutenir les espaces inclusifs.",
        "Garantir la liberté de création et de programmation : repenser l'attribution des subventions via un cahier des charges coconstruit avec lieux, associations, artistes et publics.",
        "Appliquer le 1% artistique pour consacrer 1% du budget à la commande d'œuvres d'art dans les bâtiments et espaces publics.",
        "Créer un PASS culture local en partenariat avec les salles de spectacles et lieux de création."
    ],
    "equipements-sportifs": [
        "Renforcer l'accessibilité aux équipements sportifs : améliorer leur desserte par les transports en commun, étendre les plages horaires, renforcer la tarification sociale, accueillir les personnes en situation de handicap."
    ],
    "amenagement-urbain": [
        "Lancer une conférence permanente sur un nouveau projet de ville réunissant habitants, associations, CIQ, architectes et urbanistes, et créer une Maison des projets.",
        "Travailler à la requalification des quartiers pour densifier l'habitat existant et développer des centralités de quartier vers la ville quart d'heure."
    ],
    "accessibilite": [
        "Faire d'Aix une ville 100% accessible aux PMR et UFR : plan massif d'accessibilité universelle couvrant l'espace public, transports, bâtiments et événements municipaux.",
        "Déployer des campagnes de sensibilisation relatives à l'usage abusif des places de stationnement réservées."
    ],
    "aide-sociale": [
        "Créer des places de logement d'urgence pour les sans-abris et personnes en situation de grande précarité, avec ou sans papiers.",
        "Mise en place d'une carte municipale pour les familles monoparentales ouvrant des droits prioritaires et tarifs réduits (crèches, cantines, périscolaire, logement social, transports, culture, sport).",
        "Garantir un véritable droit au répit parental : solutions de relais, accès prioritaire à l'aide aux devoirs, périscolaire jusqu'à 18h30, gratuité lors des événements municipaux, séjours de répit.",
        "Créer un guide municipal de la monoparentalité disponible sur l'application et en version papier.",
        "Protéger les plus vulnérables : places d'hébergement pour les personnes LGBTQIA+ en rupture familiale."
    ],
    "egalite-discriminations": [
        "Créer un Observatoire municipal des discriminations avec lieu d'accueil, permanence juridique gratuite et numéro vert pour le signalement et l'accompagnement des victimes.",
        "Créer un accueil mobile pour accueillir et accompagner les victimes de discriminations.",
        "Faire de la lutte contre les discriminations une politique municipale transversale. Se constituer partie civile aux côtés de toute victime. Former tous les personnels avec un référent dans chaque service.",
        "Soutenir les associations de traduction, d'interprétariat et d'apprentissage du français.",
        "Reconnaître et transmettre l'histoire des luttes féministes, antiracistes et LGBTQIA+ dans l'espace public. Soutenir un fonds d'archives dédié.",
        "Reconnaître et transmettre l'histoire des migrations à Aix-en-Provence en créant un musée dédié.",
        "Réduire les inégalités femmes-hommes dans les politiques municipales : évaluer l'impact des choix budgétaires et orienter les financements vers la réduction des inégalités.",
        "Garantir l'égalité professionnelle dans les services municipaux : parité dans les postes de direction, congé menstruel, conditionner les subventions au respect de l'égalité femmes-hommes.",
        "Garantir l'égalité d'accès au logement : anonymisation partielle des dossiers, grille publique d'évaluation, traçabilité des décisions.",
        "Combattre l'anti-tsiganisme : aires d'accueil dignes, accès aux services essentiels, fin des expulsions sans solution de relogement.",
        "Soutenir la création d'un centre antiraciste dans le cadre de l'Observatoire des discriminations.",
        "Déployer des campagnes municipales de sensibilisation contre les LGBTIphobies dans l'espace public et les transports.",
        "Garantir l'accès aux droits des personnes trans et intersexes : permanence juridique pour les changements d'état civil, respect du prénom d'usage dans les services municipaux.",
        "Soutenir les associations de terrain par des subventions stables, mise à disposition de locaux, et coordination régulière avec écoles, IME et familles pour le handicap.",
        "Exiger de l'État plus d'AESH pour garantir à chaque enfant en situation de handicap un accompagnement personnalisé. La ville pourra compléter les contrats pour le temps méridien.",
        "Garantir la laïcité et lutter contre son instrumentalisation : accès équitable aux salles municipales, liberté d'association, neutralité des services publics.",
        "Aider la communauté musulmane à créer un lieu de culte unique et adapté en mettant à disposition un terrain via bail emphytéotique.",
        "Prévenir et lutter contre les violences faites aux enfants : protocole municipal de prévention et signalement, campagnes de sensibilisation sur les violences éducatives, sexuelles, le harcèlement scolaire et le cyberharcèlement."
    ],
    "pouvoir-achat": [
        "Introduire des clauses dans les marchés publics pour exclure les entreprises impliquées dans une violation du droit international, en particulier du droit humanitaire.",
        "Réexaminer la politique des jumelages pour s'assurer que les villes partenaires respectent le droit international et les droits humains.",
        "Étendre la gratuité des transports pour les moins de 26 ans avec prise en charge des abonnements par la ville pour les boursiers et jeunes travailleurs."
    ],
}

# Charger le JSON
with open(FICHIER, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Compter les mesures
total_mesures = sum(len(m) for m in PROPOSITIONS.values())
print(f"Total mesures à intégrer : {total_mesures}")
print(f"Sous-thèmes couverts : {len(PROPOSITIONS)}")

# Vérifier que tous les sous-thèmes existent
sous_themes_existants = set()
for cat in data["categories"]:
    for st in cat["sousThemes"]:
        sous_themes_existants.add(st["id"])

for st_id in PROPOSITIONS:
    if st_id not in sous_themes_existants:
        print(f"ERREUR: sous-thème '{st_id}' n'existe pas dans le JSON!")
        sys.exit(1)

# Injecter les propositions
candidat_id = "boronad"
nb_injectees = 0

for cat in data["categories"]:
    for st in cat["sousThemes"]:
        st_id = st["id"]
        if st_id in PROPOSITIONS:
            st["propositions"][candidat_id] = {
                "source": SOURCE,
                "sourceUrl": SOURCE_URL,
                "mesures": PROPOSITIONS[st_id]
            }
            nb_injectees += len(PROPOSITIONS[st_id])
            print(f"  {st_id}: {len(PROPOSITIONS[st_id])} mesures")
        # else: laisser null ou existant tel quel

# Mettre programmeComplet à true
for c in data["candidats"]:
    if c["id"] == candidat_id:
        c["programmeComplet"] = True
        print(f"\nprogrammeComplet: true pour {c['nom']}")
        break

# Écrire le fichier
with open(FICHIER, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal mesures injectées : {nb_injectees}")
print(f"Fichier mis à jour : {FICHIER}")
