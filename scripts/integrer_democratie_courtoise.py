#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intègre le programme complet de Démocratie Courtoise (Le Chesnay-Rocquencourt)
dans le fichier JSON existant.

Sources :
- https://democratiecourtoise.org/programme/
- https://democratiecourtoise.org/2025/12/17/programme-democratie-1/
- https://democratiecourtoise.org/2025/12/21/programme-democratie-2/
- https://democratiecourtoise.org/2026/01/02/programme-culture/
- https://democratiecourtoise.org/2026/01/18/programme-sante/
- https://democratiecourtoise.org/2026/01/25/programme-solidarite/
- https://democratiecourtoise.org/2026/02/01/programme-economie/
- https://democratiecourtoise.org/2026/02/08/programme-environnement/
- https://democratiecourtoise.org/2026/02/15/programme-urbanisme-voirie/
"""
import json
import os
import re
from datetime import datetime

# Chemins
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
ELECTIONS_DIR = os.path.join(DATA_DIR, "elections")
VILLES_JSON = os.path.join(DATA_DIR, "villes.json")
APP_JS_PATH = os.path.join(ROOT_DIR, "js", "app.js")
HOME_JS_PATH = os.path.join(ROOT_DIR, "js", "home.js")
COMPARATEUR_HTML = os.path.join(ROOT_DIR, "municipales", "2026", "index.html")

ELECTION_FILE = os.path.join(ELECTIONS_DIR, "chesnay-rocquencourt-2026.json")
CANDIDAT_ID = "democratie-courtoise"

# =============================================================================
# Propositions mappées aux sous-thèmes
# Clé = (categorie_id, sous_theme_id)
# Valeur = {"texte": ..., "source": ..., "sourceUrl": ...}
# =============================================================================

SRC_PROGRAMME = "Programme officiel 2026"
URL_PROGRAMME = "https://democratiecourtoise.org/programme/"
URL_DEMOCRATIE_1 = "https://democratiecourtoise.org/2025/12/17/programme-democratie-1/"
URL_DEMOCRATIE_2 = "https://democratiecourtoise.org/2025/12/21/programme-democratie-2/"
URL_CULTURE = "https://democratiecourtoise.org/2026/01/02/programme-culture/"
URL_SANTE = "https://democratiecourtoise.org/2026/01/18/programme-sante/"
URL_SOLIDARITE = "https://democratiecourtoise.org/2026/01/25/programme-solidarite/"
URL_ECONOMIE = "https://democratiecourtoise.org/2026/02/01/programme-economie/"
URL_ENVIRONNEMENT = "https://democratiecourtoise.org/2026/02/08/programme-environnement/"
URL_URBANISME = "https://democratiecourtoise.org/2026/02/15/programme-urbanisme-voirie/"

PROPOSITIONS = {
    # ===== SÉCURITÉ =====
    # (pas de proposition spécifique sécurité)

    # ===== TRANSPORTS =====
    ("transports", "transports-en-commun"): {
        "texte": "Revoir les parcours de bus (ex. quartier Saint-Antoine) pour améliorer la sécurité et réduire les nuisances sonores. Engager une discussion avec Versailles Grand Parc sur l'électrification des bus. Mettre en place une navette interne à la ville desservant commerces et équipements publics.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_URBANISME
    },
    ("transports", "velo-mobilites-douces"): {
        "texte": "Développer un réseau cyclable sûr, continu et connecté aux communes voisines. Installer des stationnements vélos aux abords des commerces. Rejoindre le Réseau Vélo et Marche pour bénéficier d'expertise sur les mobilités actives. Recréer un pédibus pour les trajets scolaires avec la collaboration des parents.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_URBANISME
    },
    ("transports", "pietons-circulation"): {
        "texte": "Déclarer la commune « Ville 30 » avec limitation à 30 km/h. Surélever les carrefours et passages piétons pour la sécurité, notamment des personnes âgées et PMR. Tester une journée piétonne un jour par mois pour certaines rues commerçantes. Mettre en place des politiques régulières d'information et de verbalisation priorisant les usagers vulnérables.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_URBANISME
    },
    ("transports", "stationnement"): {
        "texte": "Transformer 20 places existantes en stationnement « 15 minutes » pour achats de courte durée. Organiser la gratuité ou un tarif réduit des parkings souterrains les jours de marché.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_ECONOMIE
    },

    # ===== LOGEMENT =====
    ("logement", "acces-logement"): {
        "texte": "Mettre en lien les jeunes en recherche d'emploi ou étudiants avec les personnes âgées ayant des chambres à louer. Lancer une consultation pour l'avenir de la résidence « Les Chênes Verts ». Développer des espaces communs de buanderie, laverie, outils, autopartage et vélo.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SOLIDARITE
    },

    # ===== ÉDUCATION =====
    ("education", "petite-enfance"): {
        "texte": "Soutenir la création d'une Maison d'Assistantes Maternelles (MAM) et d'une crèche parentale. Créer un service de Protection Maternelle et Infantile (PMI) dans la commune. Engager une aide à la parentalité avec un lieu d'accueil enfant-parent. Rejoindre un réseau de micro-crèches fondées sur le lien intergénérationnel.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SOLIDARITE
    },
    ("education", "ecoles-renovation"): {
        "texte": "Généraliser la désimperméabilisation des cours d'école. Installer potagers, poulaillers et composts dans les écoles. Privilégier la rénovation, l'isolation et la mise aux normes des bâtiments existants plutôt que la démolition.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_URBANISME
    },
    ("education", "cantines-fournitures"): {
        "texte": "Proposer des repas réalisés dans une cuisine centrale communale, respectant le goût, l'équilibre alimentaire, la proximité et le bio (50 %). Passer progressivement à l'option végétarienne quotidienne. Proposer un pain fait par un artisan de la ville. Inviter les habitants à déjeuner avec les enfants à l'école.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SANTE
    },
    ("education", "periscolaire-loisirs"): {
        "texte": "Rendre les terrains de sport accessibles les week-ends et soirées avec un planning visible. Élargir les horaires des aires d'activités et les rendre accessibles à tous.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SOLIDARITE
    },
    ("education", "jeunesse"): {
        "texte": "Créer un Conseil Municipal des Jeunes pour les 15-18 ans avec reconnaissance d'un pouvoir d'initiative. Inclure les jeunes dans la définition des projets de vie collective au-delà des obligations réglementaires.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_DEMOCRATIE_2
    },

    # ===== ENVIRONNEMENT =====
    ("environnement", "espaces-verts"): {
        "texte": "Créer un Atlas de la Biodiversité Communale avec inventaire et plan d'actions de préservation. Valoriser l'Arboretum de Chèvreloup par un partenariat renforcé et plusieurs événements annuels. Végétaliser les espaces devant la mairie en retirant 50 % de la dalle minérale. Réserver minimum 10 % de chaque jardin comme espace refuge pour la faune. Créer un poste d'élu dédié à la biodiversité et au patrimoine naturel.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_ENVIRONNEMENT
    },
    ("environnement", "proprete-dechets"): {
        "texte": "Créer une charte zéro déchet pour les événements municipaux. Intégrer une bricothèque aux bibliothèques existantes. Réserver un emplacement au marché pour les associations de réparation. Favoriser les contenants réutilisables chez les commerçants événementiels. Utiliser des produits ménagers naturels pour les activités municipales.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_ENVIRONNEMENT
    },
    ("environnement", "climat-adaptation"): {
        "texte": "Proposer la création d'une maison de la nature et de la biodiversité yvelinoise. Généraliser les plantations de vivaces et le paillage des massifs pour limiter la consommation d'eau. Appliquer les lois d'extinction nocturne de l'éclairage et tester l'extinction de minuit à 6h sur des rues volontaires. Étudier les réseaux de capteurs à distance pour l'irrigation et l'éclairage public. Introduire des espèces indigènes pour la résilience.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_ENVIRONNEMENT
    },
    ("environnement", "renovation-energetique"): {
        "texte": "Privilégier la rénovation, l'isolation et la mise aux normes des bâtiments existants plutôt que la démolition. Accompagner les habitants par des conseils techniques et des mécanismes financiers pour la rénovation de leur logement. Détailler dans le PLU des critères d'action couvrant la consommation d'eau et la perméabilité des sols.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_URBANISME
    },
    ("environnement", "alimentation-durable"): {
        "texte": "Mettre en valeur les Projets Alimentaires Territoriaux (PAT). Organiser des visites de fermes et coopératives locales pour enfants, agents et habitants. Encourager l'installation d'une AMAP. Réserver un espace au marché pour les producteurs bio et locaux de la Plaine de Versailles. Proposer une aide pour cultiver des plantes sur balcons, terrasses ou potagers communs. Planter des arbres fruitiers et haies nourricières dans les espaces verts.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SANTE
    },

    # ===== SANTÉ =====
    ("sante", "centres-sante"): {
        "texte": "Rechercher un boulanger pour les quartiers Aubert et Rocquencourt. Garantir et améliorer le maintien du stationnement gratuit des professions médicales. Améliorer la prise en charge partielle de la mutuelle, sous conditions de ressources.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SOLIDARITE
    },
    ("sante", "prevention-sante"): {
        "texte": "Organiser un forum annuel réunissant alimentation, sport et prévention. Créer des ateliers de cuisine simple, anti-gaspi et lactofermentation. Former les agents municipaux sur l'alimentation et ses bienfaits. Communiquer sur les recettes de restauration scolaire et la nutrition infantile. Inscrire la commune dans le réseau des Villes Ambassadrices du Don d'Organes.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SANTE
    },
    ("sante", "seniors"): {
        "texte": "Lancer une coopération avec les habitants pour contacter les personnes âgées isolées. Favoriser les échanges et rencontres entre maisons de seniors, écoles et commerces. Favoriser le déplacement et les promenades en triporteur pour les plus âgés. Renforcer le lien intergénérationnel grâce aux activités manuelles.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SOLIDARITE
    },

    # ===== DÉMOCRATIE =====
    ("democratie", "budget-participatif"): {
        "texte": "Créer un Conseil du Budget Participatif constitué de 14 conseillers des Conseils de Quartier. Confier au CBP 10 % du budget d'investissement annuel de la ville. Organiser un référendum local pour tout projet communal supérieur à 5 millions d'euros. Utiliser la consultation d'initiative citoyenne sur les grandes décisions structurantes.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_DEMOCRATIE_1
    },
    ("democratie", "transparence"): {
        "texte": "Créer un Open Data local avec ouverture des données budgétaires, de consommation énergétique et des marchés publics. Créer un observatoire de l'éthique et de la transparence avec droit de questionnement au Conseil Municipal. Publier annuellement les indemnités perçues par les élus, y compris les frais de mandat. Limiter le maire à un seul mandat et interdire le cumul avec d'autres élections.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_DEMOCRATIE_1
    },
    ("democratie", "vie-associative"): {
        "texte": "Créer des Conseils de Quartier de 20 personnes en parité, avec habitants tirés au sort, membres d'associations et agents. Organiser 8 réunions par an avec commissions thématiques (commerce, voirie, mobilité, espaces verts, propreté, communication, convivialité). Former aux méthodes d'animation et de distribution de la parole tous les agents, élus et associations.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_DEMOCRATIE_2
    },
    ("democratie", "services-publics"): {
        "texte": "Mettre en place une plateforme participative en ligne avec boîtes à idées numériques, votes et consultations en ligne. Postuler au label Villes Internet. Améliorer le site internet de la bibliothèque avec meilleur accès au catalogue et à la réservation en ligne. Soutenir les associations facilitant l'accès au numérique.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_DEMOCRATIE_2
    },

    # ===== ÉCONOMIE =====
    ("economie", "commerce-local"): {
        "texte": "Dynamiser le centre-ville avec une zone piétonne ombragée et un marché de qualité. Créer une carte « Achetez chesnaycourtois » pour les commerces de bouche. Soutenir la création de commerces dans les quartiers avec des périodes d'essai. Lancer des marchés de Noël et une Fête du Printemps dans différents quartiers. Proposer des chèques d'achat aux habitants défavorisés chez les commerçants partenaires.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_ECONOMIE
    },
    ("economie", "emploi-insertion"): {
        "texte": "Faciliter la création de tiers-lieux par quartier pour pépinières d'entreprises, espaces de coworking ou de recherche d'emploi. Soutenir les initiatives locales depuis la Pépinière de Versailles Grand Parc. Accompagner les associations d'aide aux demandeurs d'emploi et aux entreprises. Reconsidérer les ouvertures dominicales de Parly 2 pour protéger le repos des salariés.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_ECONOMIE
    },
    ("economie", "attractivite"): {
        "texte": "Créer un espace « Ambiance Plage » avec jeux en bois et assises pour la convivialité. Installer plus de bancs en ville pour la convivialité et le repos entre les trajets. Augmenter le nombre de fontaines d'eau (au moins 2 par quartier) et de toilettes publiques.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SOLIDARITE
    },

    # ===== CULTURE =====
    ("culture", "equipements-culturels"): {
        "texte": "Créer un kiosque extérieur pour des représentations musicales, théâtrales et philosophiques. Utiliser et mettre en valeur le théâtre André Malraux pour des représentations et répétitions. Créer une ressourcerie culturelle et événementielle. Installer un piano dans les espaces culturels et municipaux. Utiliser la buvette de la Bibliothèque Victor Hugo pour cafés philo, dédicaces et joutes d'éloquence.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_CULTURE
    },
    ("culture", "evenements-creation"): {
        "texte": "Proposer un festival thématique choisi par les habitants durant une fête de l'été. Favoriser des brocantes ou Gratiferia (fête du gratuit) sur les sujets culturels. Multiplier les jeux extérieurs gratuits : boîtes à livres, boîtes à jeux, damiers d'échiquier dessinés au sol. Proposer des tarifs solidaires selon un quotient familial pour l'accès aux théâtres et au sport. Créer un concours annuel de photo et de peinture sur la biodiversité.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_CULTURE
    },

    # ===== SPORT =====
    ("sport", "equipements-sportifs"): {
        "texte": "Installer des agrès et appareils de fitness en extérieur dans les parcs (Aubert, Mairie, etc.). Créer un parcours en forêt avec l'ONF. Lancer une consultation sur les usages de la piscine. Favoriser les sports combinables (ex. terrains de padel dans le skate park).",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SANTE
    },
    ("sport", "sport-pour-tous"): {
        "texte": "Rendre les terrains de sport accessibles les week-ends et soirées avec un planning visible en ligne. Optimiser l'occupation des salles de sport avec priorité aux habitants de la commune. Faciliter une bourse au matériel sportif avec prêt via un Système d'Échange Local.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SANTE
    },

    # ===== URBANISME =====
    ("urbanisme", "amenagement-urbain"): {
        "texte": "Mettre en place un processus participatif pour la révision du PLU au-delà des obligations réglementaires. Promouvoir un urbanisme dialogué permettant les échanges entre promoteurs, élus, habitants et associations. Détailler dans le PLU des critères sur la plantation et l'abattage d'arbres, la consommation d'eau et la perméabilité des sols. Définir l'avenir des sites automobiles actuels (stations-service, concessions).",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_URBANISME
    },
    ("urbanisme", "accessibilite"): {
        "texte": "Rendre les trottoirs et bus accessibles aux piétons et aux personnes à mobilité réduite. Fleurir les trottoirs en lien avec le voisinage tout en garantissant les déplacements des poussettes et PMR. Rénover les voiries pour les voitures et les bus.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SOLIDARITE
    },

    # ===== SOLIDARITÉ =====
    ("solidarite", "aide-sociale"): {
        "texte": "Utiliser la Villa de Chèvreloup comme foyer d'accueil solidaire. Consulter les habitants pour la création d'un foyer d'urgence. Soutenir les associations de maraude solidaire. Développer les « voisins solidaires » en lien avec les forces de l'ordre. Soutenir l'entraide de récoltes de fruits et légumes entre voisins.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SOLIDARITE
    },
    ("solidarite", "egalite-discriminations"): {
        "texte": "Développer le lien avec le Groupe d'Entraide Mutuel et l'Institut Médico-Éducatif. Soutenir les assistantes sociales dans le lancement de leurs projets. Former les professionnelles de la petite enfance pour des évolutions de carrière. Accorder aux groupes minoritaires du conseil municipal l'accès aux espaces d'événements et salles de réunion.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_SOLIDARITE
    },
    ("solidarite", "pouvoir-achat"): {
        "texte": "Proposer des chèques d'achat aux habitants défavorisés chez les commerçants partenaires avec une charte de qualité. Soutenir le commerce local via la promotion et les commandes publiques. Utiliser des emballages et couverts durables pour réduire les coûts et les déchets. Organiser plusieurs pique-niques multicolores annuels partagés.",
        "source": SRC_PROGRAMME,
        "sourceUrl": URL_ECONOMIE
    },
}


def main():
    # 1. Charger le fichier JSON existant
    print(f"Chargement de {ELECTION_FILE}...")
    with open(ELECTION_FILE, "r", encoding="utf-8") as f:
        election = json.load(f)

    # 2. Mettre à jour programmeComplet pour le candidat
    # Comptage : nous avons 32 sous-thèmes avec des propositions -> programmeComplet = true
    nb_propositions = len(PROPOSITIONS)
    print(f"Nombre de propositions à intégrer : {nb_propositions}")

    for candidat in election["candidats"]:
        if candidat["id"] == CANDIDAT_ID:
            candidat["programmeComplet"] = nb_propositions >= 15
            print(f"  programmeComplet = {candidat['programmeComplet']} ({nb_propositions} propositions)")
            break

    # 3. Mettre à jour les propositions dans chaque sous-thème
    updated = 0
    for cat in election["categories"]:
        for st in cat["sousThemes"]:
            key = (cat["id"], st["id"])
            if key in PROPOSITIONS:
                st["propositions"][CANDIDAT_ID] = PROPOSITIONS[key]
                updated += 1

    print(f"  {updated} sous-thèmes mis à jour")

    # 4. Écrire le fichier JSON
    with open(ELECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(election, f, ensure_ascii=False, indent=2)
    print(f"  Fichier {os.path.basename(ELECTION_FILE)} écrit")

    # 5. Mettre à jour villes.json (stats)
    if os.path.exists(VILLES_JSON):
        with open(VILLES_JSON, "r", encoding="utf-8") as f:
            villes = json.load(f)

        # Recalculer les stats
        total_props = 0
        complets = 0
        for cat in election["categories"]:
            for st in cat.get("sousThemes", []):
                for cid, prop in st.get("propositions", {}).items():
                    if prop and prop.get("texte"):
                        total_props += 1
        for c in election["candidats"]:
            if c.get("programmeComplet"):
                complets += 1

        stats = {
            "candidats": len(election["candidats"]),
            "propositions": total_props,
            "themes": len(election["categories"]),
            "complets": complets
        }

        today = datetime.now().strftime("%Y-%m-%d")
        for v in villes:
            if v["id"] == "chesnay-rocquencourt":
                v["stats"] = stats
                v["derniereMaj"] = today
                print(f"  villes.json mis à jour (stats: {stats}, derniereMaj: {today})")
                break

        with open(VILLES_JSON, "w", encoding="utf-8") as f:
            json.dump(villes, f, ensure_ascii=False, indent=2)

    # 6. Incrémenter DATA_VERSION pour le cache busting
    now = datetime.now()
    new_version = now.strftime("%Y%m%d") + "01"

    for js_path in [APP_JS_PATH, HOME_JS_PATH]:
        if not os.path.exists(js_path):
            continue
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.search(r"var DATA_VERSION\s*=\s*'(\d+)'", content)
        if m:
            old_version = m.group(1)
            if old_version[:8] == new_version[:8]:
                counter = int(old_version[8:]) + 1
                new_version = old_version[:8] + f"{counter:02d}"
            content = content[:m.start()] + f"var DATA_VERSION = '{new_version}'" + content[m.end():]
            with open(js_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  DATA_VERSION -> {new_version} dans {os.path.basename(js_path)}")

    for html_path in [COMPARATEUR_HTML]:
        if not os.path.exists(html_path):
            continue
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        html_updated = re.sub(r"\?v=\d+", f"?v={new_version}", html)
        if html_updated != html:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_updated)
            print(f"  ?v={new_version} dans {os.path.basename(html_path)}")

    # 7. Résumé final
    print(f"\n=== Résumé ===")
    print(f"Candidat : Démocratie Courtoise ({CANDIDAT_ID})")
    print(f"Propositions intégrées : {nb_propositions} sous-thèmes")
    print(f"programmeComplet : {nb_propositions >= 15}")

    # Lister les sous-thèmes sans proposition
    sans_prop = []
    for cat in election["categories"]:
        for st in cat["sousThemes"]:
            prop = st["propositions"].get(CANDIDAT_ID)
            if prop is None:
                sans_prop.append(f"  {cat['nom']} > {st['nom']}")
    if sans_prop:
        print(f"\nSous-thèmes sans proposition ({len(sans_prop)}) :")
        for s in sans_prop:
            print(s)
    else:
        print("\nTous les sous-thèmes ont une proposition !")


if __name__ == "__main__":
    main()
