#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intègre les propositions de David Guiraud (Roubaix, LFI) extraites du
programme PDF officiel « Roubaix 2040 — Nos 400 propositions » (266 pages).

Source primaire : PDF téléchargé depuis guiraud2026.fr/programme
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "roubaix-2026.json")

SRC = "Programme David Guiraud, Fiers de Roubaix, 2026"
PDF = "https://guiraud2026.fr/wp-content/uploads/2026/02/Roubaix-2040-Nos-400-propositions.pdf"

def p(texte):
    return {"texte": texte, "source": SRC, "sourceUrl": PDF}


PROPS = {
    # ── SÉCURITÉ ──────────────────────────────────────────────────
    "police-municipale": p(
        "Créer une police municipale de proximité avec brigades à pied et à vélo, "
        "clarifier strictement les rôles entre police nationale et municipale, "
        "défendre le maintien des effectifs de police nationale, "
        "sécuriser les abords des écoles et lieux d'étude, "
        "et installer des permanences de police municipale dans chaque mairie de quartier"
    ),
    "videoprotection": p(
        "Déployer la vidéoprotection de manière ciblée sur les points sensibles "
        "(parc de Barbieux, dépôts sauvages) en complément de la présence humaine"
    ),
    "prevention-mediation": p(
        "Créer des comités citoyens de la tranquillité publique dans chaque quartier, "
        "installer des cellules de médiation avec médiateurs ancrés dans chaque mairie de quartier, "
        "lancer un plan « Aucun jeune laissé de côté » (équipe éducative mobile, repérage précoce, "
        "justice restaurative, numéro d'alerte local, soutien aux familles), "
        "renforcer les Centres Sociaux avec psychologues et éducateurs spécialisés, "
        "mettre fin aux rodéos urbains (médiation + réorientation vers sports non polluants) "
        "et prévenir les trafics (information en collèges/lycées, formations parents, parcours de sortie)"
    ),
    "violences-femmes": p(
        "Renforcer la Maison des Femmes et coordonner la lutte contre les violences, "
        "créer un réseau de correspondants municipaux égalité dans chaque service, "
        "installer un Conseil local des femmes, sécuriser l'espace public (marches exploratoires, "
        "éclairage renforcé, label « Lieu Sûr », dispositif « demandez ANGELA »), "
        "expérimenter le congé menstruel pour les agentes et créer un espace de répit "
        "pour les femmes cheffes de famille"
    ),

    # ── TRANSPORTS ────────────────────────────────────────────────
    "transports-en-commun": p(
        "Réduire le coût des transports : gratuité pour les moins de 25 ans, les chômeurs "
        "et les ménages à faibles revenus, avancer vers la gratuité totale, "
        "rénover et renforcer les fréquences du réseau Ilévia, "
        "et créer un Pass Mobilité Solidaire à 1 €/mois pour les bénéficiaires de minima sociaux"
    ),
    "velo-mobilites-douces": p(
        "Lancer un grand plan vélo pour l'autonomie des jeunes, "
        "distribuer des bourses solidaires de vélos reconditionnés, "
        "créer un réseau cyclable sécurisé et rapide avec véloroutes continues, "
        "développer des stationnements sécurisés et des ateliers de réparation, "
        "et fonder un comité vélo citoyen"
    ),
    "pietons-circulation": p(
        "Piétonniser la Grand-Place, la Grand-Rue et la place de la Liberté, "
        "sécuriser l'avenue des Nations Unies avec mail piéton et zone 30, "
        "instaurer un code local de la rue (priorité piétons/PMR/cyclistes), "
        "créer des rues scolaires apaisées et redonner vie à la gare de Roubaix "
        "avec un tiers-lieu des mobilités"
    ),
    "stationnement": p(
        "Réduire le stationnement de surface en centre-ville au profit des piétons, "
        "et garantir un accès effectif au stationnement pour les personnes handicapées "
        "avec carte mobilité inclusion attachée à la personne"
    ),
    "tarifs-gratuite": p(
        "Instaurer la gratuité des transports pour les moins de 25 ans, les chômeurs "
        "et les ménages à faibles revenus, créer un Pass Mobilité Solidaire à 1 €/mois "
        "et avancer vers la gratuité totale des transports en commun"
    ),

    # ── LOGEMENT ──────────────────────────────────────────────────
    "logement-social": p(
        "Faire du logement une priorité municipale avec un adjoint dédié, "
        "exiger une répartition juste du logement social à l'échelle de la MEL, "
        "imposer des conventions d'objectifs contraignantes aux bailleurs, "
        "installer une cellule mobile de proximité dans les quartiers "
        "et créer une cellule municipale de prévention des expulsions"
    ),
    "logements-vacants": p(
        "Remettre en usage les logements vacants via une Mission Logement en transition, "
        "mobiliser des chantiers d'insertion avec des jeunes, "
        "renforcer massivement la lutte contre l'habitat indigne (permis de louer, agents municipaux, "
        "sanctions contre marchands de sommeil) "
        "et créer une Maison de l'Habitat et du Développement Durable (guichet unique, architectes-conseil)"
    ),
    "encadrement-loyers": p(
        "Demander officiellement à l'État et à la MEL l'extension de l'encadrement des loyers "
        "à Roubaix et adopter une charte du logement et de la ville durable "
        "refusant la densification excessive"
    ),
    "acces-logement": p(
        "Développer l'accession populaire et coopérative au logement : "
        "foncière solidaire à l'échelle MEL, bail réel solidaire, "
        "habitat coopératif et participatif, "
        "créer un établissement municipal de prêt d'outillage pour la rénovation "
        "et garantir une offre de logements accessibles PMR dans chaque construction et réhabilitation"
    ),

    # ── ÉDUCATION ─────────────────────────────────────────────────
    "petite-enfance": p(
        "Garantir une place d'accueil pour chaque enfant dès la petite enfance "
        "avec des modes d'accueil diversifiés, créer des espaces d'accompagnement à la parentalité "
        "dans chaque mairie de quartier (co-animés avec PMI et Éducation nationale), "
        "installer des aires de jeux inclusives et intergénérationnelles, "
        "renforcer les tarifs solidaires pour familles monoparentales et bas revenus, "
        "créer un plan municipal dédié aux mères isolées "
        "et former les personnels de crèche à la prévention des violences éducatives"
    ),
    "ecoles-renovation": p(
        "Transformer les cours d'école en Cours Oasis (débitumisation, sols perméables, "
        "plantations massives, coins calmes, potagers co-construits avec élèves et parents), "
        "rénover thermiquement toutes les écoles, créer 5 écoles pilotes « à énergie positive », "
        "défendre chaque école publique et chaque classe contre les fermetures, "
        "augmenter les crédits pédagogiques en REP+, mutualiser les fonctions administratives "
        "en pôles scolaires et exiger le remplacement immédiat des enseignants absents"
    ),
    "cantines-fournitures": p(
        "Instaurer la gratuité de la cantine scolaire pour les familles dans le besoin, "
        "augmenter la part bio et locale dans la restauration collective, "
        "étudier la reprise en régie de la cantine municipale "
        "et faire de l'école un lieu d'éducation alimentaire avec potagers biologiques"
    ),
    "periscolaire-loisirs": p(
        "Créer une Grande Maison des Devoirs avec antennes-bulles dans chaque quartier, "
        "étendre les horaires de la médiathèque le soir et le week-end, "
        "lancer un Plan Natation pour garantir l'apprentissage à tous les enfants, "
        "renforcer les tarifs solidaires pour centres de loisirs et piscines, "
        "proposer des classes transplantées (mer, montagne, échanges internationaux) "
        "et organiser un grand thème éducatif annuel partagé avec écoles et associations"
    ),
    "jeunesse": p(
        "Développer le service civique comme tremplin, ouvrir les grandes écoles aux lycéens "
        "(Cordées de la réussite, tutorat, accompagnement financier), "
        "démocratiser l'accès à Erasmus Pro (accompagnement lycées professionnels et CFA), "
        "organiser une cérémonie annuelle des diplômés roubaisiens, "
        "créer un Pass Jeune Engagement Culture (tarif symbolique cinémas/spectacles) "
        "et ouvrir la mairie aux jeunes (stages, apprentissage, découverte des métiers municipaux)"
    ),

    # ── ENVIRONNEMENT ─────────────────────────────────────────────
    "espaces-verts": p(
        "Lancer un Plan Canopée : rues vertes avec plantations massives, "
        "15 forêts de poche et micro-boisements d'ici fin de mandat, "
        "vergers communaux à récolte libre, forêt comestible au Cul-de-Four, "
        "protéger le parc de Barbieux (brigade de tranquillité, rénovation statuaire, kiosque en bois), "
        "créer un plan de trame verte urbaine, valoriser le canal de Roubaix (ponton pédagogique), "
        "renforcer l'archipel des parcs et jardins partagés (un jardin à 300 m max), "
        "créer des réserves écologiques urbaines sur les friches, "
        "impliquer les habitants (« Samedis des espaces verts », charte de l'arbre, rucher-école), "
        "interdire les animaux sauvages dans les cirques "
        "et déclarer toute coupe d'arbre soumise à déclaration préalable"
    ),
    "proprete-dechets": p(
        "Reprendre en main la propreté par une régie municipale renforcée (internalisation progressive), "
        "viser le label « Ville propre » et « Zéro déchet d'ici 2030 », "
        "lutter fermement contre les dépôts sauvages (amendes multipliées, vidéoprotection), "
        "créer un Chèque Réparation vélo et électroménager (30-50 €), "
        "installer des toilettes publiques dignes en centre-ville et parc Barbieux, "
        "réorganiser la collecte (conteneurs enterrés, sacs renforcés, camion plateau commerçants), "
        "créer une équipe « Urgence propreté » 13h-19h, "
        "lancer un bilan-diagnostic participatif par quartier avec ambassadeurs de la propreté, "
        "viser zéro plastique et -75 % gaspillage en restauration collective (frigos solidaires), "
        "et développer la filière locale de réemploi des matériaux BTP"
    ),
    "climat-adaptation": p(
        "Déclarer l'état d'urgence climatique à Roubaix, "
        "renforcer le plan canicule (lieux frais accessibles, suivi personnes isolées), "
        "installer des miroirs d'eau et îlots de fraîcheur dans chaque quartier, "
        "déployer des récupérateurs d'eau de pluie pour les usages municipaux "
        "et interdire les barbecues sauvages en créant des zones dédiées sécurisées"
    ),
    "renovation-energetique": p(
        "Rénover thermiquement toutes les écoles, installer des ombrières solaires "
        "sur parkings et bâtiments publics avec autoconsommation partagée, "
        "créer un service municipal de l'énergie (équipes mobiles, diagnostics, petits travaux, écogestes), "
        "viser « zéro logement passoire ou bouilloire » (cartographie, chantiers d'insertion, tiers-financement MEL), "
        "lancer un plan roubaisien des énergies renouvelables (coopératives, régie ou SPL, tarif social), "
        "étendre le réseau de chaleur urbain et étudier la géothermie, "
        "réaliser un diagnostic énergétique complet de tous les bâtiments municipaux dès la première année "
        "et imposer l'extinction nocturne des bâtiments municipaux et publicités"
    ),
    "alimentation-durable": p(
        "Créer une filière alimentaire municipale locale (production fruits/légumes, "
        "vergers communaux, légumerie municipale), expérimenter une sécurité sociale "
        "de l'alimentation (~100 €/mois de crédit alimentaire), "
        "viser le « zéro gaspillage » et « zéro plastique » en restauration collective, "
        "planter des arbres fruitiers en ville à récolte libre "
        "et accompagner vers le « zéro phyto »"
    ),

    # ── SANTÉ ─────────────────────────────────────────────────────
    "centres-sante": p(
        "Garantir un médecin traitant pour chaque Roubaisien (aides installation, locaux à loyers modérés, "
        "classes pré-PASS dans les lycées), créer un réseau de centres de santé municipaux ou coopératifs "
        "(professionnels salariés, tiers payant intégral, offre pluridisciplinaire), "
        "installer un Conseil des pharmacies en lien avec la CPTS, "
        "renforcer le lien hôpital-CCAS-aides à domicile pour les sorties d'hôpital "
        "et accompagner le transfert de l'IFSI dans des conditions exemplaires"
    ),
    "prevention-sante": p(
        "Faire de la prévention une priorité municipale : refonte du Contrat Local de Santé, "
        "dépistages mobiles et stands santé sur les marchés et dans les écoles, "
        "créer un Pass Sport Santé (prescription d'activité physique par les médecins, activités gratuites), "
        "développer des espaces d'écoute en santé mentale (soutien hôpital Lucien Bonnafé, CLSM renforcé), "
        "lancer un plan global de lutte contre les addictions (protoxyde d'azote, tabac, alcool), "
        "instaurer un parcours Sport Santé dès la maternelle avec sensibilisation à l'hygiène "
        "et accompagner l'accès à la complémentaire santé solidaire avec la CPAM"
    ),
    "seniors": p(
        "Refuser la privatisation des EHPAD publics et contrôler les établissements, "
        "développer le co-logement solidaire seniors-étudiants, "
        "renforcer la Maison des Aidants (accueil, orientation, temps de répit), "
        "relancer le service de taxi solidaire pour soins et démarches "
        "et créer un réseau de voisins bienveillants contre l'isolement"
    ),

    # ── DÉMOCRATIE ────────────────────────────────────────────────
    "budget-participatif": p(
        "Réformer les budgets participatifs sur le modèle de Porto Alegre : "
        "2 % du budget d'investissement citoyen (~900 000 €/an), "
        "créer une Grande Assemblée Citoyenne de 60 membres tirés au sort (dès 16 ans, moyens propres), "
        "instaurer un droit d'interpellation citoyenne (pétition 2 % = inscription à l'ordre du jour), "
        "organiser des votations citoyennes orientantes sur les projets ANRU, "
        "nommer un adjoint dédié à la démocratie et à la vie associative, "
        "mettre en place des permanences hebdomadaires des maires de quartier, "
        "partager la gouvernance des équipements publics (comités d'usagers), "
        "former les citoyens de demain (ateliers citoyenneté dès le primaire, CME et CCJ élargis) "
        "et associer les organisations syndicales à la vie communale"
    ),
    "transparence": p(
        "Adopter une charte éthique anticorruption avec référent alerte indépendant "
        "et référent déontologue au règlement municipal, "
        "publier un budget annuel transparent des financements et projets obtenus, "
        "généraliser les achats publics sociaux et écologiquement responsables (SPASER, "
        "indicateurs empreinte carbone et biodiversité) "
        "et garantir la souveraineté numérique municipale (logiciels libres, hébergement maîtrisé)"
    ),
    "vie-associative": p(
        "Garantir transparence et équité dans le soutien aux associations "
        "(critères objectifs co-construits, vote en Conseil municipal, plancher de subvention à 500 €), "
        "simplifier les démarches (grande simplification administrative), "
        "sécuriser les pôles associatifs durables (FAL, MDA, OMS, pôles de quartier autonomes), "
        "créer une cellule d'appui pour subventions nationales et européennes, "
        "généraliser les conventions pluriannuelles, "
        "relancer les « Prodiges de la République » (30 lauréats/an, transport gratuit un an, subvention 500 €), "
        "relier vie étudiante et vie de quartier (forum annuel, partenariats enseignement supérieur) "
        "et protéger la liberté associative face au Contrat d'Engagement Républicain"
    ),
    "services-publics": p(
        "Ouvrir 5 mairies de quartier (guichet complet, accompagnement administratif, relais France Services), "
        "réinternaliser les services publics (propreté, entretien, restauration, petits travaux), "
        "garantir des réponses rapides aux habitants avec délais ciblés, "
        "développer une application municipale unique RBX (démarches, démocratie, signalements, alertes), "
        "lutter contre la fracture numérique (formations gratuites, fibre, lieux de travail partagés), "
        "stabiliser l'organisation municipale et restaurer le dialogue social (calendrier partage, "
        "règles RH équitables, lutte contre la souffrance au travail), "
        "lancer un grand plan de formation et d'accès aux concours pour tous les agents "
        "et protéger les données municipales (cybersécurité renforcée)"
    ),

    # ── ÉCONOMIE ──────────────────────────────────────────────────
    "commerce-local": p(
        "Relancer le Crédit municipal de Roubaix (microcrédits, prêt sur gage modernisé, "
        "épargne solidaire, éducation financière), créer un guichet « Entreprendre à Roubaix » "
        "avec espaces d'innovation de proximité, revitaliser les marchés (dialogue social, sécurisation, "
        "grand marché hebdomadaire), animer les rues commerçantes (équipes municipales dédiées, "
        "reprise de pas-de-porte, rénovation façades, médiateurs de terrain), "
        "soutenir la filière textile et mode (ESMOD, ESAAT, Blanchemaille, Tissel, Mode in Roubaix), "
        "créer une foncière commerciale solidaire avec boutiques à l'essai, "
        "organiser 3-4 grands temps forts populaires par an "
        "et lutter contre l'expansion des grandes surfaces à la MEL"
    ),
    "emploi-insertion": p(
        "Remobiliser la Mission locale avec plans quinquennaux d'insertion "
        "et plateforme locale de l'insertion, organiser un Grand Forum annuel de l'Emploi, "
        "généraliser les clauses sociales d'insertion dans la commande publique "
        "(chargé de mission « Marchés & Insertion »), "
        "créer des parcours d'autonomie économique pour 100 femmes/an "
        "(formations du soir, garde après 18h, École de la Seconde Chance), "
        "cartographier les besoins en main-d'œuvre quartier par quartier, "
        "soutenir les Territoires zéro chômeur et l'ESS, "
        "ouvrir des garages solidaires coopératifs "
        "et développer une politique municipale du réemploi solidaire (site dédié à l'Alma, "
        "marchés du réemploi itinérants, puces populaires)"
    ),
    "attractivite": p(
        "Faire de Roubaix un carrefour stratégique Nord/Europe avec diplomatie économique, "
        "moderniser les jumelages (échanges scolaires, formations croisées, projets environnementaux), "
        "créer un réseau Roubaix à l'international (appui aux diasporas, chargé de mission dédié), "
        "créer une Halle de la Méditerranée et des produits du monde à l'Épeule, "
        "développer l'économie transfrontalière avec l'Eurométropole (partenariats, formations binationales), "
        "proposer une Zone Franche Urbaine 2.0 (économie circulaire, numérique inclusif, artisanat local), "
        "lancer le label FAIR(E) ROUBAIX (économie solidaire internationale), "
        "organiser un Festival « 70 Nations » avec trois temps forts annuels, "
        "créer un lieu de recueillement des solidarités internationales (pavoisement drapeaux des 70 nationalités, "
        "espace de paix et de fraternité entre les peuples) "
        "et développer l'apprentissage pratique des langues dès la maternelle (dispositif EMILE)"
    ),

    # ── CULTURE ───────────────────────────────────────────────────
    "equipements-culturels": p(
        "Rendre la pratique artistique accessible (Conservatoire, École de danse, associations, "
        "tarification sociale dans tous les équipements, médiateur culturel territorial mobile), "
        "ouvrir les grands équipements aux quartiers (Condition Publique, Colisée, La Piscine), "
        "moderniser le théâtre Pierre-de-Roubaix et remettre en état le théâtre Pierre-Richard, "
        "renforcer la médiathèque avec horaires étendus, soutenir les librairies indépendantes, "
        "lancer un Salon BD et un prix littéraire scolaire, "
        "mettre à disposition des lieux vacants aux artistes, créer une artothèque locale "
        "et un fonds municipal d'acquisition (10 000 €), "
        "et installer un Centre régional des Mémoires urbaines et des Luttes populaires à l'Alma"
    ),
    "evenements-creation": p(
        "Créer le Festival URBX vitrine des artistes roubaisiens (tremplins, masterclasses), "
        "lancer POP-UP RBX (scènes ouvertes mensuelles dans les quartiers), "
        "le label « Cultures de Roubaix » (bourses, mentorat, réseaux d'appui), "
        "un festival annuel de théâtre populaire et de rue, "
        "un Grand festival des musiques des origines (maghreb, Afrique, Portugal, Italie, Flandre), "
        "un festival de cinéma populaire en plein air dans les quartiers, "
        "un budget participatif culturel, "
        "une exposition annuelle « Nos habitants ont du talent », "
        "le Colloque des Anciens (transmission mémoire, patois, visites locales) "
        "et valoriser le patrimoine roubaisien (Secteur Patrimonial Remarquable, "
        "plan d'investissement patrimoine en danger, éco-musée de l'Habitat ouvrier à l'Épeule)"
    ),

    # ── SPORT ─────────────────────────────────────────────────────
    "equipements-sportifs": p(
        "Rendre le Parc des Sports aux Roubaisiens (révision cahier des charges, poumon vert arboré), "
        "lancer un plan pluriannuel de rénovation (Nabuchodonosor, Brossolette, "
        "reprise des équipements de proximité), étudier la rénovation du stade populaire, "
        "créer un centre de référence sport de haut niveau (santé-sport, récupération, showroom), "
        "refonder l'Office municipal des sports (guichet unique, transparence des aides) "
        "et ouvrir les équipements scolaires aux clubs sportifs (coordonnateur logistique municipal)"
    ),
    "sport-pour-tous": p(
        "Rendre le sport populaire accessible à tous avec un Pass Sport Populaire municipal, "
        "ouvrir les équipements soir et week-end, proposer des olympiades populaires, "
        "offrir des activités gratuites dans l'espace public chaque semaine (circuits forme en accès libre), "
        "lancer le programme « Sport avec elles » dans les quartiers populaires "
        "(créneaux sécurisés, tournois, self-défense, agentes relais), "
        "créer un urban trail roubaisien accessible à tous, "
        "mettre en place des parcours sportifs pour les jeunes (découvrir plusieurs sports, vacances sportives), "
        "des parcours sport-études adaptés aux talents, "
        "une école municipale de football populaire "
        "et des contrats de développement avec priorité aux petits clubs formateurs"
    ),

    # ── URBANISME ─────────────────────────────────────────────────
    "amenagement-urbain": p(
        "Élaborer un Agenda Roubaix Avenir 2040 coproduit avec les habitants, "
        "piétonniser le centre-ville (Grand-Place, Grand-Rue, continuité gare-Eurotéléport-Lannoy), "
        "transformer l'Eurotéléport, requalifier les bâtiments vacants (Banque de France, Devianne, Midas), "
        "appliquer le principe « une friche = un projet » avec Régie locale des lieux vacants, "
        "valoriser le réseau des places roubaisiennes (espaces verts, assises, éclairage adapté), "
        "libérer l'espace public de la publicité (interdiction pubs nocives près des écoles, "
        "suppression écrans énergivores), créer un élu dédié « Roubaix La Nuit », "
        "engager le Secteur Patrimonial Remarquable et lancer un plan d'investissement "
        "pour le patrimoine en danger (église Notre-Dame, couvent des Clarisses, maison ossature métallique)"
    ),
    "accessibilite": p(
        "Lancer un plan pluriannuel d'accessibilité chiffré et priorisé, "
        "appliquer le design universel dans l'urbanisme et les services publics, "
        "rendre les écoles réellement inclusives (cellule municipale handicap-éducation), "
        "créer une bourse solidaire du matériel médical, "
        "développer le handisport et les clubs inclusifs, "
        "et faire de la mairie un employeur exemplaire en matière de handicap"
    ),
    "quartiers-prioritaires": p(
        "Refonder les projets ANRU Alma et Épeule avec ateliers populaires d'urbanisme, "
        "réviser les projets du Pile et Trois-Ponts, "
        "lancer un plan de rattrapage Cul-de-Four, Oran-Cartigny et Sartel-Carihem "
        "(forêt urbaine, ferme urbaine) et revaloriser la rue Jules-Guesde"
    ),

    # ── SOLIDARITÉ ────────────────────────────────────────────────
    "aide-sociale": p(
        "Revaloriser les aides du CCAS (300-500 €/famille/an), "
        "lutter contre le non-recours aux droits (guichet social de proximité dans chaque mairie de quartier, "
        "5 référents de parcours social, équipe spécialisée, renforcement écrivains publics), "
        "créer des permanences sociales de proximité avec assistants sociaux, "
        "renforcer l'accueil de jour et l'hébergement d'urgence (douches, repas, équipes mobiles « aller-vers »), "
        "créer un Pôle municipal Droits et Dignité des Personnes Étrangères "
        "(juriste en droit des étrangers, accompagnement multilingue) "
        "et déployer un réseau de voisins bienveillants pour lutter contre l'isolement"
    ),
    "egalite-discriminations": p(
        "Faire de Roubaix une ville résolument antiraciste : Observatoire indépendant des discriminations "
        "(co-géré avec associations et chercheurs, budget participatif, testing), "
        "livret municipal de lutte contre le racisme, "
        "soutenir les associations contre les LGBTIphobies (points d'écoute, mise à l'abri), "
        "former tous les agents municipaux à l'accueil inclusif et sans discrimination, "
        "soutenir les Marches des Fiertés (appui logistique, actions éducatives), "
        "valoriser la mémoire coloniale et l'histoire des immigrations (projets éducatifs et culturels), "
        "promouvoir la laïcité (sensibilisation agents, référents laïcité), "
        "schéma directeur des lieux de culte 2.0 avec concertation "
        "et relancer le dialogue interconvictionnel et interreligieux"
    ),
    "pouvoir-achat": p(
        "Instaurer une tarification sociale et progressive de l'eau "
        "(gratuité des premiers m³ vitaux), renforcer les tarifs solidaires familles, "
        "négocier des plans d'apurement EDF/Engie avec accompagnement personnalisé, "
        "créer un Chèque Réparation vélo et électroménager (30-50 €) "
        "et relancer le Crédit municipal (prêts à taux réduit, épargne solidaire)"
    ),
}

# === SOUS-THÈMES SPÉCIFIQUES ROUBAIX ===
# Propositions du PDF qui ne rentrent pas dans les 44 sous-thèmes standard
SOUS_THEMES_SPECIFIQUES = {
    "culture": {
        "patrimoine-roubaisien": {
            "nom": "Patrimoine roubaisien",
            "proposition": p(
                "Faire du patrimoine roubaisien un patrimoine vivant porté par ses habitants : "
                "habitants-ambassadeurs du patrimoine (transmission orale, récits de quartier, mémoire populaire), "
                "lieux emblématiques réinvestis en espaces culturels co-conçus, "
                "partenariats structurants (Métropole Label.le, Société d'émulation, Non-Lieu). "
                "Redynamiser le label Ville d'Art et d'Histoire : livrets pédagogiques, "
                "classe patrimoine en école volontaire, circuits avec panneaux explicatifs, "
                "partenariats universitaires, valorisation du matrimoine (statues féminines au parc de Barbieux). "
                "Stop aux démolitions spéculatives : opposition à toute démolition de valeur architecturale, "
                "renforcement des protections, fouilles d'archéologie préventive. "
                "Plan d'investissement pluriannuel chiffré : hôtel Dupire-Rozan (diagnostic), "
                "église Notre-Dame 4 M€ (2 M€ clos/couvert + 2 M€ désordres), "
                "couvent des Clarisses ~10 M€, maison ossature métallique 1,45 M€ (rachat + façade + intérieur), "
                "église Saint-François (appui au diocèse), le Moulin, couvent de la Visitation, hôtel Saint-Benoît. "
                "Appui au projet de maison mémorielle sur la Shoah (42 bd d'Armentières, Lili Leignel). "
                "Poursuivre la convention Fondation du patrimoine (aides aux particuliers, défiscalisation, mécénat). "
                "Stimuler la création d'une Fondation de défense du patrimoine roubaisien "
                "avec label Petit Patrimoine Populaire Roubaisien (PPPR). "
                "Requalification des façades via la Maison de l'Habitat (conseils architecturaux, accompagnement financier)"
            ),
        },
    },
    "democratie": {
        "fonction-publique-municipale": {
            "nom": "Fonction publique municipale",
            "proposition": p(
                "Faire du maire un véritable maire-employeur, garant de conditions de travail dignes. "
                "Stabiliser l'organisation municipale : fin aux réorganisations permanentes, "
                "chaîne de décision lisible, priorités politiques partagées avec l'administration. "
                "Ancrer la municipalité dans tous les quartiers avec une présence renforcée sur le terrain. "
                "Remettre à plat le régime indemnitaire pour garantir cohérence et équité, "
                "lutter contre la précarité et prioriser les bas salaires. "
                "Créer un lieu d'écoute indépendant et sécurisé : procédures claires de signalement "
                "du harcèlement moral et sexuel, discriminations et violences au travail, "
                "protection des agents, délais de traitement garantis. "
                "Agir contre les temps partiels subis (majoritairement imposés aux femmes). "
                "Repenser le parcours professionnel : entretiens d'évaluation transformés en outils de valorisation, "
                "mentorat, passerelles de carrière, reconnaissance des compétences. "
                "Ouvrir la mairie à la jeunesse : stages, apprentissage, tutorat, "
                "découverte des métiers municipaux sur base du volontariat. "
                "Relancer un Forum des métiers municipaux ouvert aux habitants "
                "pour rendre visibles les agents et leur savoir-faire"
            ),
        },
    },
    "economie": {
        "finances-ingenierie": {
            "nom": "Finances & Ingénierie de projets",
            "proposition": p(
                "Créer un Bureau municipal de la conception et du financement des projets "
                "(veille, montage et suivi des financements État, Europe, Région, Département, agences). "
                "Stratégie « zéro euro laissé sur la table » : audit des subventions perdues ou non sollicitées, "
                "référent financement dans chaque direction municipale. "
                "Constituer des projets « prêts à subventionner » avec coûts, calendriers et impacts pré-établis "
                "pour répondre sans délai aux appels à projets. "
                "Former les cadres et chefs de projet à l'ingénierie financière, "
                "base de données partagée des appels à projets et échéances. "
                "Créer un Conseil économique et social roubaisien pour relancer l'activité locale"
            ),
        },
    },
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Liste des candidats pour créer les entrées null
    candidat_ids = [c["id"] for c in data["candidats"]]

    updated = 0
    added = 0

    # 1. Mettre à jour les sous-thèmes standard
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            sid = st["id"]
            if sid in PROPS:
                old = st["propositions"].get("guiraud")
                st["propositions"]["guiraud"] = PROPS[sid]
                if old is None:
                    added += 1
                    print(f"  + {sid}: AJOUTÉ")
                else:
                    updated += 1
                    print(f"  ~ {sid}: MIS À JOUR")

    # 2. Ajouter les sous-thèmes spécifiques Roubaix
    specifiques_added = 0
    for cat in data["categories"]:
        cat_id = cat["id"]
        if cat_id in SOUS_THEMES_SPECIFIQUES:
            for st_id, st_info in SOUS_THEMES_SPECIFIQUES[cat_id].items():
                # Vérifier si le sous-thème existe déjà
                existe = any(st["id"] == st_id for st in cat["sousThemes"])
                if not existe:
                    # Créer le sous-thème avec propositions null pour tous les candidats
                    props = {cid: None for cid in candidat_ids}
                    props["guiraud"] = st_info["proposition"]
                    nouveau_st = {
                        "id": st_id,
                        "nom": st_info["nom"],
                        "propositions": props,
                    }
                    cat["sousThemes"].append(nouveau_st)
                    specifiques_added += 1
                    print(f"  ++ {st_id}: SOUS-THÈME SPÉCIFIQUE CRÉÉ (dans {cat_id})")
                else:
                    # Mettre à jour la proposition
                    for st in cat["sousThemes"]:
                        if st["id"] == st_id:
                            st["propositions"]["guiraud"] = st_info["proposition"]
                            updated += 1
                            print(f"  ~ {st_id}: MIS À JOUR (spécifique)")
                            break

    # 3. Mettre à jour le candidat
    for c in data["candidats"]:
        if c["id"] == "guiraud":
            c["programmeComplet"] = True
            c["programmeUrl"] = "https://guiraud2026.fr/programme"
            c["programmePdfPath"] = "Roubaix-2040-Nos-400-propositions.pdf"
            c["siteCampagne"] = "https://guiraud2026.fr/"
            print(f"\n  programmeComplet -> true")
            print(f"  programmeUrl -> https://guiraud2026.fr/programme")
            break

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    total = updated + added + specifiques_added
    print(f"\n  Résultat: {updated} mis à jour, {added} ajoutés, {specifiques_added} spécifiques créés")
    print(f"  Total sous-thèmes Guiraud: {total}")


if __name__ == "__main__":
    main()
