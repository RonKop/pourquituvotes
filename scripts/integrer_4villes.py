#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intègre les propositions trouvées pour 4 villes :
Tourcoing, Cannes, Fort-de-France, Aulnay-sous-Bois
"""

import json
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections"


def load_json(filename):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, filename):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {filepath}")


def set_proposition(data, sous_theme_id, candidat_id, proposition):
    """Set a proposition for a candidat in a sous-theme."""
    for cat in data['categories']:
        for st in cat['sousThemes']:
            if st['id'] == sous_theme_id:
                st['propositions'][candidat_id] = proposition
                return True
    print(f"WARNING: sous-theme '{sous_theme_id}' not found!")
    return False


def prop(texte, source, url):
    """Helper to create a proposition dict."""
    return {"texte": texte, "source": source, "sourceUrl": url}


# ============================================================
# 1. TOURCOING
# ============================================================
def integrer_tourcoing():
    data = load_json("tourcoing-2026.json")
    count = {"becue": 0, "vuylsteker": 0, "talpaert": 0, "croes": 0, "verbrugghe": 0}

    # --- BECUE (maire sortante, Horizons) ---
    src_becue = "Presse locale"
    url_wiki = "https://fr.wikipedia.org/wiki/%C3%89lections_municipales_de_2026_%C3%A0_Tourcoing"
    url_tourcoing = "https://www.tourcoing.fr/Vivre-a-Tourcoing/Securite-prevention/Pour-plus-de-securite-a-Tourcoing"
    url_anru = "https://www.lillemetropole.fr/renouvellement-urbain-la-bourgogne-tourcoing"
    url_mediacites = "https://www.mediacites.fr/breve/lille/2026/02/13/municipales-a-tourcoing-le-parti-de-doriane-becue-et-gerald-darmanin-sanctionne-au-pire-moment/"

    set_proposition(data, "police-municipale", "becue",
        prop("Renforcement du service Tranquillité résidentielle et des effectifs de police municipale, en complément de la police nationale", "Site ville de Tourcoing", url_tourcoing))
    count["becue"] += 1

    set_proposition(data, "videoprotection", "becue",
        prop("Extension du réseau de vidéoprotection au-delà des 166 caméras déjà en service sur la commune", "Site ville de Tourcoing", url_tourcoing))
    count["becue"] += 1

    set_proposition(data, "prevention-mediation", "becue",
        prop("Maintien et développement du dispositif d'aide aux victimes et de médiation de quartier", "Site ville de Tourcoing", url_tourcoing))
    count["becue"] += 1

    set_proposition(data, "logement-social", "becue",
        prop("Rénovation urbaine du quartier de la Bourgogne (81 M EUR ANRU) : diversification de l'offre de logements pour renforcer la mixité sociale", src_becue, url_anru))
    count["becue"] += 1

    set_proposition(data, "ecoles-renovation", "becue",
        prop("Poursuite du plan pluriannuel de rénovation des écoles et amélioration de la restauration scolaire", src_becue, url_mediacites))
    count["becue"] += 1

    set_proposition(data, "quartiers-prioritaires", "becue",
        prop("Transformation en profondeur du quartier de la Bourgogne : désenclavement, création d'espaces publics de qualité, sécurisation et développement économique", src_becue, url_anru))
    count["becue"] += 1

    set_proposition(data, "amenagement-urbain", "becue",
        prop("Projet ANRU Bourgogne : urbanisme à taille humaine, ouverture du quartier sur la ville, réaménagement des espaces publics", src_becue, url_anru))
    count["becue"] += 1

    set_proposition(data, "espaces-verts", "becue",
        prop("Création de jardins partagés et développement d'espaces verts dans le cadre de la rénovation du quartier de la Bourgogne", src_becue, url_anru))
    count["becue"] += 1

    set_proposition(data, "commerce-local", "becue",
        prop("Construction d'un nouvel équipement commercial et de services dans le quartier de la Bourgogne", src_becue, url_anru))
    count["becue"] += 1

    # --- VUYLSTEKER (Écologistes-PS-PCF) ---
    url_tvd = "https://tourcoingvertdemain.fr/"
    url_mediacites2 = "https://www.mediacites.fr/municipales-2026/lille/2025/06/26/municipales-2026-a-tourcoing-lunion-de-la-gauche-avance-mais-coince-encore-sur-le-leadership/"

    set_proposition(data, "espaces-verts", "vuylsteker",
        prop("Planter massivement des arbres, inviter la nature en ville et multiplier les espaces de repos et de fraîcheur", "Site de campagne", url_tvd))
    count["vuylsteker"] += 1

    set_proposition(data, "velo-mobilites-douces", "vuylsteker",
        prop("Rendre l'espace public respirable et apaisé pour les piétons et cyclistes, permettre aux enfants de marcher et jouer en sécurité", "Site de campagne", url_tvd))
    count["vuylsteker"] += 1

    set_proposition(data, "tarifs-gratuite", "vuylsteker",
        prop("Rendre les transports en commun gratuits avant la fin du mandat, tout en améliorant et sécurisant le réseau", "Site de campagne", url_tvd))
    count["vuylsteker"] += 1

    set_proposition(data, "climat-adaptation", "vuylsteker",
        prop("Répondre en urgence aux enjeux écologiques : végétalisation, désimperméabilisation des sols, lutte contre les îlots de chaleur", "Site de campagne", url_tvd))
    count["vuylsteker"] += 1

    set_proposition(data, "budget-participatif", "vuylsteker",
        prop("Mettre en place une démocratie locale renforcée pour répondre aux urgences démocratiques et sociales du prochain mandat", "Site de campagne", url_tvd))
    count["vuylsteker"] += 1

    # --- CROES (LFI) ---
    url_croes = "https://www.croes2026.com/"
    url_lfi = "https://programme.lafranceinsoumise.fr/municipales-2026/"

    set_proposition(data, "tarifs-gratuite", "croes",
        prop("Gratuité des transports en commun pour les habitants de Tourcoing, dans le cadre d'un programme de rupture sociale et écologique", "Site de campagne", url_croes))
    count["croes"] += 1

    set_proposition(data, "cantines-fournitures", "croes",
        prop("Cantines 100 % bio et locales avec tarification sociale, fournitures scolaires gratuites pour toutes les familles", "Programme LFI municipales", url_lfi))
    count["croes"] += 1

    set_proposition(data, "budget-participatif", "croes",
        prop("Mise en place d'un budget participatif ambitieux pour permettre aux habitants de décider directement des investissements de leur quartier", "Programme LFI municipales", url_lfi))
    count["croes"] += 1

    set_proposition(data, "renovation-energetique", "croes",
        prop("Plan massif de rénovation énergétique des bâtiments publics et accompagnement des copropriétés en précarité énergétique", "Programme LFI municipales", url_lfi))
    count["croes"] += 1

    # --- VERBRUGGHE (RN) ---
    url_rn = "https://rassemblementnational.fr/communiques/municipales-2026-le-rn-lance-une-charte-de-soutien"

    set_proposition(data, "police-municipale", "verbrugghe",
        prop("Renforcement des effectifs et des moyens de la police municipale pour assurer la sécurité au quotidien", "Charte RN municipales", url_rn))
    count["verbrugghe"] += 1

    set_proposition(data, "cantines-fournitures", "verbrugghe",
        prop("Promotion du localisme dans les cantines scolaires : approvisionnement en circuits courts et produits du terroir", "Charte RN municipales", url_rn))
    count["verbrugghe"] += 1

    set_proposition(data, "commerce-local", "verbrugghe",
        prop("Soutien aux commerces de proximité et aux artisans locaux, lutte contre la désertification commerciale", "Charte RN municipales", url_rn))
    count["verbrugghe"] += 1

    set_proposition(data, "transparence", "verbrugghe",
        prop("Gestion financière prudente, lutte contre le gaspillage d'argent public et transparence des dépenses municipales", "Charte RN municipales", url_rn))
    count["verbrugghe"] += 1

    save_json(data, "tourcoing-2026.json")
    return count


# ============================================================
# 2. CANNES
# ============================================================
def integrer_cannes():
    data = load_json("cannes-2026.json")
    count = {"lisnard": 0, "mussio": 0, "hugues": 0}

    # --- LISNARD (LR, maire sortant) ---
    url_f3 = "https://france3-regions.franceinfo.fr/provence-alpes-cote-d-azur/alpes-maritimes/cannes/campus-du-spatial-3000-nouveaux-logements-voie-rapide-vegetalisee-les-premieres-annonces-du-candidat-david-lisnard-pour-cannes-3295233.html"
    url_fb = "https://www.francebleu.fr/emissions/l-invite-d-ici-matin/municipales-a-cannes-david-lisnard-devoile-un-projet-ambitieux-tout-en-reduisant-la-depense-8620274"
    url_camp = "https://lisnard2026.fr/"
    url_rcf = "https://www.rcf.fr/articles/actualite/cannes-david-lisnard-annonce-sa-candidature-aux-elections-municipales"

    set_proposition(data, "police-municipale", "lisnard",
        prop("Maintien d'une police municipale armée avec un ratio parmi les plus élevés de France (1 policier pour 400 habitants), plus de 155 opérations anti-drogue par an en coordination avec la police nationale", "France Bleu Azur", url_fb))
    count["lisnard"] += 1

    set_proposition(data, "videoprotection", "lisnard",
        prop("Extension du réseau de vidéoprotection (déjà plus de 800 caméras, 1 pour 72 habitants) et déploiement d'une IA d'analyse d'images pour les réquisitions judiciaires", "Presse locale", "https://www.petitesaffiches.fr/politique,104/securite-la-ville-de-cannes,39526.html?lang=fr"))
    count["lisnard"] += 1

    set_proposition(data, "acces-logement", "lisnard",
        prop("Construction de 3 000 nouveaux logements, notamment dans le secteur de la Roubine, avec développement de logements diffus en centre-ville et programme de 300 logements dans le quartier République", "France 3 PACA", url_f3))
    count["lisnard"] += 1

    set_proposition(data, "amenagement-urbain", "lisnard",
        prop("Grand projet de végétalisation de la voie rapide qui recouvre la voie ferrée : la rendre plus belle, plus esthétique et végétalisée", "France 3 PACA", url_f3))
    count["lisnard"] += 1

    set_proposition(data, "espaces-verts", "lisnard",
        prop("Plantation massive d'arbres et végétalisation de la ville, poursuite de la lutte contre les inondations", "France Bleu Azur", url_fb))
    count["lisnard"] += 1

    set_proposition(data, "attractivite", "lisnard",
        prop("Création d'un campus du spatial en partenariat avec Thales Alenia Space et développement de filières IA et quantique, objectif 6 000 étudiants en 5 ans avec le campus Vatel", "France 3 PACA", url_f3))
    count["lisnard"] += 1

    set_proposition(data, "jeunesse", "lisnard",
        prop("Faire de Cannes une ville étudiante : construction du campus Vatel (hôtellerie), objectif de passer de 3 000 à 6 000 étudiants sur la commune", "RCF Nice", url_rcf))
    count["lisnard"] += 1

    set_proposition(data, "transparence", "lisnard",
        prop("Poursuite de l'orthodoxie financière : baisse de la dette de 81,7 M EUR depuis 2014, diminution du taux de la taxe foncière de 3,6 % en 2025, 56 M EUR d'économies réalisées", "France Bleu Azur", url_fb))
    count["lisnard"] += 1

    set_proposition(data, "evenements-creation", "lisnard",
        prop("Stratégie événementielle pour dynamiser la hors-saison : festivals, congrès internationaux et événements culturels et sportifs toute l'année", "France Bleu Azur", url_fb))
    count["lisnard"] += 1

    set_proposition(data, "quartiers-prioritaires", "lisnard",
        prop("Rénovation du quartier populaire de République : 300 logements neufs, amélioration des équipements publics et requalification urbaine", "Presse locale", "https://www.unenouvelleenergie.fr/le-quartier-populaire-de-republique-avance-avec-david-lisnard/"))
    count["lisnard"] += 1

    # Update programmeUrl
    for c in data['candidats']:
        if c['id'] == 'lisnard':
            c['programmeUrl'] = url_camp

    # --- MUSSIO (RN) ---
    url_mussio_sec = "https://cannes-actus.com/politique/municipales-2026-a-cannes-il-faut-une-tolerance-zero-face-a-linsecurite-et-au-narcotrafic-les-propositions-fortes-du-candidat-rn-lucas-mussio/"
    url_mussio_np = "https://nicepresse.com/a-cannes-le-candidat-rn-qui-part-a-lassaut-de-la-citadelle-lisnard-pointe-une-delinquance-en-hausse-et-une-police-municipale-a-reorganiser/"
    url_mussio_camp = "https://www.lucasmussio2026.fr/"

    set_proposition(data, "police-municipale", "mussio",
        prop("Réorganisation de la police municipale, création d'une brigade anti-stupéfiants municipale et d'une brigade maritime pour sécuriser les zones côtières et les îles de Lérins", "Cannes Actus", url_mussio_sec))
    count["mussio"] += 1

    set_proposition(data, "prevention-mediation", "mussio",
        prop("Tolérance zéro face à l'insécurité et au narcotrafic : stratégie de pression quotidienne sur le terrain contre les trafiquants, engagement de la responsabilité parentale pour les mineurs délinquants", "Cannes Actus", url_mussio_sec))
    count["mussio"] += 1

    set_proposition(data, "proprete-dechets", "mussio",
        prop("Améliorer le quotidien des habitants en rendant la ville plus propre et mieux entretenue, avec une attention particulière à chaque quartier", "Nice Presse", url_mussio_np))
    count["mussio"] += 1

    set_proposition(data, "commerce-local", "mussio",
        prop("Soutien renforcé aux commerçants et artisans locaux, présence quotidienne sur le terrain pour accompagner les commerces de proximité", "Site de campagne", url_mussio_camp))
    count["mussio"] += 1

    # Update programmeUrl
    for c in data['candidats']:
        if c['id'] == 'mussio':
            c['programmeUrl'] = url_mussio_camp

    # --- HUGUES (Union de la gauche) ---
    url_hugues_log = "https://cannes-actus.com/politique/municipales-2026-cannes-jeunes-travailleurs-ne-peuvent-plus-se-loger-gauche-fait-de-la-crise-du-logement-sa-priorite/"
    url_hugues_alt = "https://cannes-actus.com/politique/municipales-2026-cannes-gauche-locale-sunit-et-devoile-sa-tete-de-liste-pour-proposer-une-alternative-nette-et-coherente/"

    set_proposition(data, "logement-social", "hugues",
        prop("Faire du logement accessible une urgence sociale : lutte contre les logements vides et les meublés touristiques (80 % de l'offre immobilière), construction de logements pour les jeunes et les travailleurs", "Cannes Actus", url_hugues_log))
    count["hugues"] += 1

    set_proposition(data, "renovation-energetique", "hugues",
        prop("Investissements massifs dans la rénovation thermique des copropriétés dégradées et promotion de la mobilité durable", "Cannes Actus", url_hugues_log))
    count["hugues"] += 1

    set_proposition(data, "budget-participatif", "hugues",
        prop("Mise en place de budgets participatifs, renforcement de la transparence municipale et des conseils de quartier pour une démocratie locale vivante", "Cannes Actus", url_hugues_alt))
    count["hugues"] += 1

    set_proposition(data, "services-publics", "hugues",
        prop("Renforcement des services publics de proximité dans tous les quartiers, avec une attention particulière aux populations fragiles", "Cannes Actus", url_hugues_alt))
    count["hugues"] += 1

    set_proposition(data, "police-municipale", "hugues",
        prop("Sécurité de proximité recentrée sur la police nationale, avec des effectifs adaptés aux besoins réels des quartiers", "Cannes Actus", url_hugues_alt))
    count["hugues"] += 1

    save_json(data, "cannes-2026.json")
    return count


# ============================================================
# 3. FORT-DE-FRANCE
# ============================================================
def integrer_fort_de_france():
    data = load_json("fort-de-france-2026.json")
    count = {"laguerre": 0, "carole": 0, "moreau": 0, "jos": 0, "delor": 0}

    # --- LAGUERRE (PPM, maire sortant) ---
    url_lag_camp = "https://didierlaguerre2026.com/"
    url_rci = "https://rci.fm/deuxiles/node/5340554"
    url_rci_plan = "https://rci.fm/node/5111702"
    url_bondamanjak = "https://www.bondamanjak.com/le-projet-majeur-qui-permettra-a-didier-laguerre-de-gagner-les-elections-municipales-a-fort-de-france-en-mars-2026/"
    url_anru = "https://www.anru.fr/actualites/fort-de-france-une-ambitieuse-transformation-urbaine-avec-lanru"
    url_fondas = "https://fondaskreyol.org/article/didier-laguerre-ppm-lance-sa-campagne-electorale"

    set_proposition(data, "acces-logement", "laguerre",
        prop("Construction de 3 résidences étudiantes supplémentaires et réhabilitation de bâtiments vacants (ancienne Sécurité sociale, siège Crédit Mutuel) en logements", "RCI", url_rci_plan))
    count["laguerre"] += 1

    set_proposition(data, "stationnement", "laguerre",
        prop("Rénovation et construction de 3 parkings en centre-ville pour répondre à la demande de stationnement et redynamiser le commerce", "RCI", url_rci))
    count["laguerre"] += 1

    set_proposition(data, "velo-mobilites-douces", "laguerre",
        prop("Création d'une coulée verte et développement de pistes cyclables pour encourager les alternatives à la voiture", "RCI", url_rci_plan))
    count["laguerre"] += 1

    set_proposition(data, "espaces-verts", "laguerre",
        prop("Aménagement de davantage d'espaces verts en ville et création d'un corridor végétal traversant le centre-ville", "RCI", url_rci_plan))
    count["laguerre"] += 1

    set_proposition(data, "commerce-local", "laguerre",
        prop("Plan de revitalisation du centre-ville : développement de l'économie commerciale, incitation à l'investissement privé en centre de Fort-de-France", "RCI", url_rci))
    count["laguerre"] += 1

    set_proposition(data, "logements-vacants", "laguerre",
        prop("Réhabilitation de l'habitat dégradé et remise sur le marché des logements vacants du centre-ville dans le cadre du Plan Action Coeur de Ville", "RCI", url_rci_plan))
    count["laguerre"] += 1

    set_proposition(data, "amenagement-urbain", "laguerre",
        prop("Rendre Fort-de-France plus accessible à pied, requalifier les espaces publics et le patrimoine privé du centre-ville", "Bondamanjak", url_bondamanjak))
    count["laguerre"] += 1

    set_proposition(data, "attractivite", "laguerre",
        prop("Organiser de grands événements culturels et sportifs pour attirer trois publics cibles : seniors actifs, étudiants et jeunes actifs", "Fondas Kréyol", url_fondas))
    count["laguerre"] += 1

    set_proposition(data, "jeunesse", "laguerre",
        prop("Maintien et développement du Conseil municipal des jeunes (52 jeunes de 10 à 14 ans), soutien aux initiatives citoyennes des jeunes Foyalais", "Fondas Kréyol", url_fondas))
    count["laguerre"] += 1

    set_proposition(data, "quartiers-prioritaires", "laguerre",
        prop("Transformation urbaine ambitieuse avec l'ANRU dans les quartiers prioritaires : rénovation de l'habitat, désenclavement, amélioration des services publics", "ANRU", url_anru))
    count["laguerre"] += 1

    set_proposition(data, "transparence", "laguerre",
        prop("Poursuite du redressement des finances municipales avec un excédent budgétaire annoncé de 4,8 millions d'euros", "Fondas Kréyol", url_fondas))
    count["laguerre"] += 1

    # Update programmeUrl
    for c in data['candidats']:
        if c['id'] == 'laguerre':
            c['programmeUrl'] = url_lag_camp

    # --- CAROLE (Divers gauche, Démaré Fodwans) ---
    url_carole_1ere = "https://la1ere.franceinfo.fr/martinique/video-municipales-2026-francis-carole-est-a-nouveau-candidat-a-fort-de-france-1664769.html"
    url_carole_rci = "https://rci.fm/martinique/infos/Politique/Municipales-2026-Francis-Carole-et-Beatrice-Bellay-sallient-pour-ravir-la-mairie-de"
    url_carole_bonda = "https://www.bondamanjak.com/municipales-2026-bellay-carole-la-nouvelle-donne-pour-fort-de-france/"

    set_proposition(data, "attractivite", "carole",
        prop("Faire de Fort-de-France un phare dans la Caraïbe, un moteur d'innovation et un creuset d'audace, en rupture avec 67 ans de gestion PPM", "France Info Martinique", url_carole_1ere))
    count["carole"] += 1

    set_proposition(data, "transparence", "carole",
        prop("Redonner un nouveau souffle à la ville avec une municipalité qui ose, entreprend et construit, en rompant avec la résignation", "Bondamanjak", url_carole_bonda))
    count["carole"] += 1

    set_proposition(data, "services-publics", "carole",
        prop("Revitaliser les services publics municipaux et repositionner Fort-de-France au sein de la communauté d'agglomération du centre de la Martinique", "RCI", url_carole_rci))
    count["carole"] += 1

    # --- MOREAU (PLP) ---
    url_moreau_1ere = "https://la1ere.franceinfo.fr/martinique/video-municipales-2026-steeve-moreau-et-rodrigue-petitot-font-alliance-a-fort-de-france-1652834.html"
    url_moreau_rci = "https://rci.fm/martinique/infos/Politique/Elections-municipales-2026-Rodrigue-Petitot-presente-la-candidature-de-Steeve"

    set_proposition(data, "proprete-dechets", "moreau",
        prop("Nettoyage et entretien renforcé du centre-ville et des quartiers populaires, jugés délaissés et sales par le candidat", "France Info Martinique", url_moreau_1ere))
    count["moreau"] += 1

    set_proposition(data, "quartiers-prioritaires", "moreau",
        prop("Priorité aux quartiers populaires délaissés : présence de terrain, écoute des habitants, transformation de la colère en projet politique concret", "RCI", url_moreau_rci))
    count["moreau"] += 1

    set_proposition(data, "jeunesse", "moreau",
        prop("Mobilisation des jeunes électeurs et des quartiers populaires, faire du peuple le véritable contrôleur de l'action municipale", "RCI", url_moreau_rci))
    count["moreau"] += 1

    set_proposition(data, "pouvoir-achat", "moreau",
        prop("Lutte contre la vie chère en Martinique : le PLP est né du mouvement RPPRAC contre la hausse des prix, et porte cette revendication à l'échelle municipale", "France Info Martinique", url_moreau_1ere))
    count["moreau"] += 1

    # --- JOS (PIA / Péyi A) ---
    url_jos_1ere = "https://la1ere.franceinfo.fr/martinique/municipales-2026-week-end-d-annonces-de-candidatures-a-sainte-marie-riviere-pilote-fort-de-france-gros-morne-robert-ou-encore-a-schoelcher-1662551.html"
    url_jos_rci = "https://rci.fm/martinique/infos/Politique/Elections-le-bus-des-municipales-fait-un-arret-Fort-de-France"

    set_proposition(data, "pouvoir-achat", "jos",
        prop("Création d'une centrale d'achat solidaire pour casser la dynamique de la vie chère, dispositif éprouvé pour réduire les prix", "France Info Martinique", url_jos_1ere))
    count["jos"] += 1

    set_proposition(data, "acces-logement", "jos",
        prop("Programme immobilier solidaire « Ma ville, mon toit, mon patrimoine » avec des décotes de 40 000 à 60 000 euros pour les primo-accédants", "France Info Martinique", url_jos_1ere))
    count["jos"] += 1

    set_proposition(data, "police-municipale", "jos",
        prop("Renforcement de la sécurité de la ville avec une police municipale mieux dotée et une présence accrue dans les quartiers", "RCI", url_jos_rci))
    count["jos"] += 1

    set_proposition(data, "commerce-local", "jos",
        prop("Revitalisation du centre-ville de Fort-de-France par le soutien au commerce de proximité et l'attractivité économique", "France Info Martinique", url_jos_1ere))
    count["jos"] += 1

    # --- DELOR (Divers) ---
    url_delor = "https://rci.fm/deuxiles/node/5476282"
    # Very little specific programme info found for Delor
    set_proposition(data, "transparence", "delor",
        prop("Rompre avec le statu quo et défendre de nouvelles idées pour la gestion de Fort-de-France, avec une approche philosophique et citoyenne", "RCI", url_delor))
    count["delor"] += 1

    save_json(data, "fort-de-france-2026.json")
    return count


# ============================================================
# 4. AULNAY-SOUS-BOIS
# ============================================================
def integrer_aulnay():
    data = load_json("aulnay-sous-bois-2026.json")
    count = {"beschizza": 0, "malandra": 0, "siby": 0, "nguette": 0}

    # --- BESCHIZZA (LR, maire sortant) ---
    url_beschizza = "https://brunobeschizza.fr/"
    url_aulnaylibre_eco = "https://www.aulnaylibre.com/2025/01/le-maire-d-aulnay-sous-bois-bruno-beschizza-presente-sa-feuille-de-route-pour-2026-aux-acteurs-economiques.html"
    url_aulnaylibre_bilan = "https://www.aulnaylibre.com/2025/08/2014-2026-un-bilan-une-vision-pour-aulnay-sous-bois-avec-le-maire-bruno-beschizza.html"
    url_aulnaylibre_lance = "https://www.aulnaylibre.com/2025/12/elections-municipales-de-2026-a-aulnay-sous-bois-l-impressionnant-lancement-de-campagne-du-maire-bruno-beschizza.html"
    url_aulnaylibre_aultech = "https://www.aulnaylibre.com/2025/12/inauguration-de-aultech-nouveau-campus-du-numerique-et-de-l-intelligence-artificielle-a-aulnay-sous-bois.html"
    url_video = "https://www.aulnay-sous-bois.fr/ma-ville/securite-et-prevention/videoprotection/"
    url_police = "https://www.aulnay-sous-bois.fr/ma-ville/securite-et-prevention/services-dordre-public-durgence-2/securite-pieton/police-municipale/"
    url_garcelon = "https://www.aulnay-sous-bois.fr/grands-projets/projets-ecologiques-et-durables/laiterie-garcelon/"
    url_sport = "https://www.aulnay-sous-bois.fr/actualites/la-ville-soutient-les-pratiques-culturelles-et-sportives-au-sein-des-colleges-2026-2027/"

    set_proposition(data, "police-municipale", "beschizza",
        prop("Renforcement des effectifs de la police municipale, mieux armés et mieux équipés, avec des outils juridiques élargis pour accomplir leurs missions", "Site de campagne", url_beschizza))
    count["beschizza"] += 1

    set_proposition(data, "videoprotection", "beschizza",
        prop("Réseau de 530 caméras de vidéoprotection avec un centre de supervision urbain (CSU) fonctionnant 24h/24, 7j/7 avec 24 opérateurs", "Site ville", url_video))
    count["beschizza"] += 1

    set_proposition(data, "transports-en-commun", "beschizza",
        prop("Arrivée de la gare du métro ligne 16 (Grand Paris Express) à Aulnay-sous-Bois, désenclavement du territoire et connexion directe aux pôles d'emploi", "Aulnaylibre", url_aulnaylibre_eco))
    count["beschizza"] += 1

    set_proposition(data, "emploi-insertion", "beschizza",
        prop("Inauguration du campus numérique Aultech (IA et numérique) en partenariat avec Apple, Microsoft, Simplon et IBM, pour former les jeunes aux métiers d'avenir", "Aulnaylibre", url_aulnaylibre_aultech))
    count["beschizza"] += 1

    set_proposition(data, "amenagement-urbain", "beschizza",
        prop("Réaménagement du boulevard de Strasbourg, renaturation du canal de l'Ourcq, rénovation de la halle du marché du Vieux-Pays", "Aulnaylibre", url_aulnaylibre_eco))
    count["beschizza"] += 1

    set_proposition(data, "ecoles-renovation", "beschizza",
        prop("Toutes les écoles de la ville bénéficieront de travaux de rénovation dans le cadre d'un plan d'investissement pluriannuel", "Aulnaylibre", url_aulnaylibre_bilan))
    count["beschizza"] += 1

    set_proposition(data, "espaces-verts", "beschizza",
        prop("Plan ambitieux de création d'espaces verts supplémentaires, renaturation du canal de l'Ourcq et réhabilitation patrimoniale de la Laiterie Garcelon (2,5 M EUR)", "Site ville", url_garcelon))
    count["beschizza"] += 1

    set_proposition(data, "equipements-culturels", "beschizza",
        prop("Réhabilitation de la Laiterie Garcelon en équipement culturel et patrimonial, préservant le dernier témoignage du passé agricole du sud de la commune", "Site ville", url_garcelon))
    count["beschizza"] += 1

    set_proposition(data, "sport-pour-tous", "beschizza",
        prop("Soutien aux pratiques sportives et culturelles dans les collèges, avec un programme sportif renforcé (15 heures minimum de sport par semaine au collège Parc)", "Site ville", url_sport))
    count["beschizza"] += 1

    set_proposition(data, "commerce-local", "beschizza",
        prop("Organisation de festivités tout au long de l'année et soutien à l'installation de commerces de proximité dans tous les quartiers", "Aulnaylibre", url_aulnaylibre_lance))
    count["beschizza"] += 1

    set_proposition(data, "attractivite", "beschizza",
        prop("Réindustrialisation de l'ancien site PSA avec implantation de nouvelles entreprises, data center, centre de maintenance des métros 16 et 17, et puits géothermique", "Aulnaylibre", url_aulnaylibre_eco))
    count["beschizza"] += 1

    # Update programmeUrl
    for c in data['candidats']:
        if c['id'] == 'beschizza':
            c['programmeUrl'] = url_beschizza

    # --- MALANDRA (LFI-PCF) ---
    url_malandra_aulnaylibre = "https://www.aulnaylibre.com/2025/11/elections-municipales-de-2026-a-aulnay-sous-bois-elena-malandra-annonce-sa-candidature-pour-lfi.html"
    url_malandra_monaulnay = "https://monaulnay.com/2026/01/inauguration-du-local-de-campagne-de-la-liste-la-force-de-changer-a-aulnay-sous-bois.html"
    url_lfi = "https://programme.lafranceinsoumise.fr/municipales-2026/"

    set_proposition(data, "aide-sociale", "malandra",
        prop("Faire de la solidarité une réalité concrète et du droit à vivre mieux une revendication légitime pour tous les Aulnaysiens", "Aulnaylibre", url_malandra_aulnaylibre))
    count["malandra"] += 1

    set_proposition(data, "budget-participatif", "malandra",
        prop("Mise en place de budgets participatifs pour que les habitants décident directement de l'utilisation d'une part du budget municipal", "Programme LFI municipales", url_lfi))
    count["malandra"] += 1

    set_proposition(data, "cantines-fournitures", "malandra",
        prop("Cantines scolaires 100 % bio et locales avec tarification sociale, fournitures scolaires gratuites", "Programme LFI municipales", url_lfi))
    count["malandra"] += 1

    set_proposition(data, "renovation-energetique", "malandra",
        prop("Plan de rénovation énergétique des bâtiments publics et accompagnement des copropriétés en précarité énergétique", "Programme LFI municipales", url_lfi))
    count["malandra"] += 1

    # --- SIBY (PS-EELV, Aulnay Rassemblée) ---
    url_siby_monaulnay = "https://monaulnay.com/2025/08/elections-municipales-pour-oussouf-siby-rien-ne-se-fera-seul.html"
    url_siby_camp = "https://aulnayrassemblee2026.fr/candidat-equipe/"
    url_siby_tract = "https://monaulnay.com/2026/01/oussouf-siby-dans-un-tract-sadresse-aux-aulnaysiens.html"
    url_siby_educ = "https://monaulnay.com/2026/02/enfance-jeunesse-et-education-un-tract-de-la-liste-aulnay-rassemblee.html"

    set_proposition(data, "services-publics", "siby",
        prop("Remettre le service public au coeur des politiques municipales, garantir la proximité et l'écoute des habitants dans chaque quartier", "MonAulnay", url_siby_monaulnay))
    count["siby"] += 1

    set_proposition(data, "transparence", "siby",
        prop("Agir avec intégrité, responsabilité et transparence dans la gestion des finances et des projets municipaux", "MonAulnay", url_siby_monaulnay))
    count["siby"] += 1

    set_proposition(data, "egalite-discriminations", "siby",
        prop("Construire une ville plus solidaire, plus juste et plus durable, fondée sur les valeurs de solidarité, justice et égalité", "MonAulnay", url_siby_monaulnay))
    count["siby"] += 1

    set_proposition(data, "jeunesse", "siby",
        prop("Programme dédié à l'enfance, la jeunesse et l'éducation : renforcement de l'accueil périscolaire et des activités pour les jeunes Aulnaysiens", "MonAulnay", url_siby_educ))
    count["siby"] += 1

    set_proposition(data, "vie-associative", "siby",
        prop("Défense et soutien renforcé aux associations locales et aux agents municipaux, piliers du lien social à Aulnay", "MonAulnay", url_siby_tract))
    count["siby"] += 1

    # Update programmeUrl
    for c in data['candidats']:
        if c['id'] == 'siby':
            c['programmeUrl'] = url_siby_camp

    # --- NGUETTE (Démocratie Représentative, Aulnay Humaniste) ---
    url_nguette = "https://www.aulnaylibre.com/2025/11/elections-municipales-de-2026-a-aulnay-sous-bois-candidature-de-cheick-nguette-pour-la-democratie-representative.html"
    url_nguette2 = "https://aulnaycap.com/2025/09/28/video-cheickh-nguette-officialise-sa-candidature-aux-municipales-2026-a-aulnay-sous-bois/"

    set_proposition(data, "egalite-discriminations", "nguette",
        prop("Aulnay humaniste, ensemble pour la dignité : défense de la dignité de chaque habitant et lutte contre les discriminations", "Aulnaylibre", url_nguette))
    count["nguette"] += 1

    set_proposition(data, "transparence", "nguette",
        prop("Promouvoir la démocratie représentative avec des élus au service des citoyens, plus de transparence et de participation", "AulnayCap", url_nguette2))
    count["nguette"] += 1

    save_json(data, "aulnay-sous-bois-2026.json")
    return count


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Intégration des propositions - 4 villes")
    print("=" * 60)

    print("\n--- TOURCOING ---")
    count_tourcoing = integrer_tourcoing()
    for k, v in count_tourcoing.items():
        print(f"  {k}: {v} propositions")

    print("\n--- CANNES ---")
    count_cannes = integrer_cannes()
    for k, v in count_cannes.items():
        print(f"  {k}: {v} propositions")

    print("\n--- FORT-DE-FRANCE ---")
    count_fdf = integrer_fort_de_france()
    for k, v in count_fdf.items():
        print(f"  {k}: {v} propositions")

    print("\n--- AULNAY-SOUS-BOIS ---")
    count_aulnay = integrer_aulnay()
    for k, v in count_aulnay.items():
        print(f"  {k}: {v} propositions")

    total = sum(sum(c.values()) for c in [count_tourcoing, count_cannes, count_fdf, count_aulnay])
    print(f"\nTOTAL: {total} propositions intégrées")
    print("\nprogrammeComplet reste false pour tous (aucun programme structuré complet trouvé)")
