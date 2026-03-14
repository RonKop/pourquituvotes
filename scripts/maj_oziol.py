#!/usr/bin/env python3
"""
Mise à jour du programme de Nathalie Oziol dans montpellier-2026.json.
~550 mesures brutes → ~180 mesures mappées sur les 44 sous-thèmes standard.
"""

import json
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "data", "elections", "montpellier-2026.json")

SOURCE = "Programme officiel 2026 — Nathalie Oziol"
SOURCE_URL = "https://oziol2026.fr/le-programme/"

# ── Mapping des ~550 mesures vers les 44 sous-thèmes ──
# Mesures combinées et condensées pour garder les plus concrètes et distinctives.

MAPPING = {
    # ═══════════════════════════════════════════
    # 1. SÉCURITÉ
    # ═══════════════════════════════════════════
    "police-municipale": [
        "Police municipale de proximité : patrouilles à pied dans les quartiers, fin de la vidéoverbalisation et des armes létales.",
        "Remunicipaliser la sécurité et supprimer les crédits du GSRI au profit de conciergeries de quartier.",
        "Médiateurs formés et éducateurs de rue dans chaque quartier sensible.",
        "Récépissé de contrôle d'identité pour lutter contre les contrôles au faciès.",
        "Sécurité routière ambitieuse et CISPD métropolitain.",
    ],
    "videoprotection": [
        "Moratoire sur la vidéosurveillance : audit indépendant de l'efficacité du parc existant.",
        "Création d'un comité d'éthique citoyen pour encadrer tout dispositif de surveillance.",
    ],
    "prevention-mediation": [
        "Médiation sociale et présence humaine renforcée dans les quartiers, y compris soirs et week-ends.",
        "Médiateurs scolaires et de rue pour la prévention de la délinquance.",
        "Accueil digne des victimes en commissariat et aide municipale au dépôt de plainte.",
    ],
    "violences-femmes": [
        "Maison des femmes : centre féministe avec guichet unique pour les victimes de violences.",
        "Numéro municipal d'urgence et permanence juridique gratuite pour les victimes.",
        "Hébergement d'urgence dédié aux victimes de violences conjugales et familiales.",
        "La ville se constitue partie civile aux côtés des victimes de violences sexistes.",
        "Marches exploratoires genrées pour sécuriser l'espace public.",
    ],

    # ═══════════════════════════════════════════
    # 2. TRANSPORTS
    # ═══════════════════════════════════════════
    "transports-en-commun": [
        "Renforcer massivement les transports en commun : tram toutes les 10 min (5 min en pointe), service étendu jusqu'à 2h du matin.",
        "Navettes vers les quartiers mal desservis et coordination métro/régionale.",
        "Gare routière digne et pôles de mobilité intermodaux.",
        "Moratoire sur les projets autoroutiers (COM) et opposition aux mégaprojets écocides.",
        "Convention citoyenne sur la ZFE.",
    ],
    "velo-mobilites-douces": [
        "Vélo pilier du transport : moderniser Vélomagg', développer le VAE et les vélostations sécurisées.",
        "Pistes cyclables séparées, continues et sécurisées sur l'ensemble de la ville.",
        "Massifier l'autopartage électrique dans tous les quartiers.",
    ],
    "pietons-circulation": [
        "Accessibilité universelle du réseau de transport pour les PMR.",
        "Sécurité routière ambitieuse : zones apaisées, aménagements piétons prioritaires.",
    ],
    "stationnement": [
        "Parkings gratuits autour des campus universitaires.",
    ],
    "tarifs-gratuite": [
        "Progresser vers la gratuité universelle des transports en commun.",
        "Gratuité immédiate des transports pour les faibles revenus et les jeunes.",
        "Réexaminer la couverture transport vers les campus.",
    ],

    # ═══════════════════════════════════════════
    # 3. LOGEMENT
    # ═══════════════════════════════════════════
    "logement-social": [
        "Construire 30 000 logements pendant le mandat avec 30 % de logements sociaux imposés dans tous les projets.",
        "Système transparent et public d'attribution des logements sociaux, avec relogement garanti dans le même quartier.",
        "Mettre aux normes d'accessibilité l'ensemble du parc social.",
        "Soutenir le Bail Réel Solidaire et les formes alternatives d'habitat (coopératif, partagé).",
        "Privilégier les conventions CROUS et investir dans la construction de logements étudiants.",
    ],
    "logements-vacants": [
        "Réquisitionner les logements vacants de longue durée.",
        "Taxer les logements vacants et plafonner les locations touristiques.",
        "Inventorier les friches urbaines et lancer un plan de revalorisation.",
    ],
    "encadrement-loyers": [
        "Créer un système municipal de garantie locative pour sécuriser l'accès au logement.",
    ],
    "acces-logement": [
        "Guichet unique municipal du droit au logement.",
        "Soutenir les locataires face aux marchands de sommeil et renforcer les contrôles contre l'habitat indigne.",
        "Doubler la capacité d'hébergement d'urgence et créer des espaces refuges pour victimes de violences.",
        "Créer des douches municipales gratuites et des centres d'accueil de jour.",
        "Plan massif de rénovation thermique et écologique des logements.",
    ],

    # ═══════════════════════════════════════════
    # 4. ÉDUCATION
    # ═══════════════════════════════════════════
    "petite-enfance": [
        "Service public local de la petite enfance : 100 % des parents avec une place en crèche.",
        "Accueil inclusif des enfants en situation de handicap dès la petite enfance.",
        "Atteindre 1 ATSEM par classe de maternelle.",
        "Unités d'enseignement maternelle autisme.",
    ],
    "ecoles-renovation": [
        "Rénover les écoles dégradées, notamment dans les quartiers populaires.",
        "Défendre un maximum de 24 élèves par classe.",
        "Sectorisation contre la ségrégation scolaire et observatoire municipal de la mixité scolaire.",
        "Recruter des professeurs d'EPS, musique et arts plastiques.",
        "École dehors dans chaque école et classe verte pour tous.",
    ],
    "cantines-fournitures": [
        "Gratuité des repas scolaires (seuil immédiat pour familles sous le seuil de pauvreté) et petits-déjeuners à l'école.",
        "Fournitures scolaires gratuites pour tous les élèves.",
        "100 % bio, local et de saison dans les cantines avec option végétarienne quotidienne, 2 jours végétariens et 1 jour vegan.",
        "Potagers scolaires bio et composteurs dans les écoles.",
    ],
    "periscolaire-loisirs": [
        "Semaine sans écran annuelle dans les écoles.",
        "Soutien scolaire gratuit dans les quartiers populaires.",
        "Sécuriser le financement de l'éducation populaire.",
    ],
    "jeunesse": [
        "Déployer des cantines sociales jeunesse à tarification progressive.",
        "Services municipaux de santé jeunesse gratuits et pôle municipal de santé mentale (gratuit, anonyme).",
        "Protections périodiques lavables gratuites pour les jeunes.",
        "Gratuité d'inscription en médiathèque et accès gratuit/tarif réduit aux lieux culturels pour les jeunes.",
        "Renforcer les conseils de jeunesse avec budgets dédiés et droit d'interpellation.",
        "Soutenir les maisons de la jeunesse et de la culture.",
    ],

    # ═══════════════════════════════════════════
    # 5. ENVIRONNEMENT
    # ═══════════════════════════════════════════
    "espaces-verts": [
        "Repenser parcs et jardins avec accent sur les arbres, créer des îlots de fraîcheur et jeux d'eau.",
        "Jardins partagés dans tous les quartiers, végétalisation prioritaire des quartiers populaires.",
        "Développer des corridors verts et bleus, éco-pâturage et fauche tardive pour la biodiversité.",
        "Végétaliser la Place de l'Europe et reconnecter les habitants au Verdanson.",
        "Rendre le lac des Garrigues baignable et étudier la baignade dans le Lez.",
        "Protéger les terres naturelles et agricoles de l'urbanisation.",
    ],
    "proprete-dechets": [
        "Convention citoyenne des déchets et programme d'éducation populaire sur la stratégie déchets.",
        "Ressourceries de quartier, soutien au vrac et à la consigne.",
        "Composteurs dans les écoles et les quartiers.",
    ],
    "climat-adaptation": [
        "Diagnostic de chaleur urbaine et plan canicule renforcé.",
        "Plan de désimperméabilisation des sols.",
        "Réduire la pollution lumineuse.",
        "Sécurité de l'eau : infrastructures de captage et réutilisation des eaux de pluie (bassins Rhône-Lez).",
    ],
    "renovation-energetique": [
        "Créer un opérateur public « Énergie de Montpellier » 100 % renouvelable avec tarification solidaire.",
        "Guichet public local de l'énergie et plan énergétique pour les bâtiments publics.",
        "Investir massivement dans le solaire et les réseaux de chaleur.",
        "Supprimer le chauffage au fioul dans tous les bâtiments publics.",
        "Combattre les passoires thermiques dans les quartiers populaires.",
    ],
    "alimentation-durable": [
        "Restaurant populaire municipal bio à prix bas avec produits locaux.",
        "Ceinture agricole autour de Montpellier : société foncière agricole publique, faciliter l'installation de nouveaux agriculteurs.",
        "Structurer la chaîne alimentaire locale : outils municipaux de transformation, soutien aux AMAP, marchés paysans et épiceries coopératives.",
        "Conseil alimentaire local et fermes pédagogiques.",
        "Réduction de 50 % de la consommation de produits animaux d'ici 2032.",
    ],

    # ═══════════════════════════════════════════
    # 6. SANTÉ
    # ═══════════════════════════════════════════
    "centres-sante": [
        "Centres de santé municipaux avec médecins salariés, sans dépassement d'honoraires.",
        "Soutenir les centres de santé communautaires.",
        "Centres vétérinaires publics pour les animaux domestiques.",
    ],
    "prevention-sante": [
        "Politique municipale de santé mentale et lutte contre la psychophobie.",
        "Équipes mobiles, maraudes et réinsertion par le logement pour les plus précaires.",
        "Salle de consommation à moindre risque.",
        "Planning familial renforcé, prévention IST/VIH et santé sexuelle et reproductive.",
        "Soutenir les associations de distribution alimentaire étudiante.",
    ],
    "seniors": [
        "CCAS pilier du service public du grand âge : maintien à domicile massif via le service autonomie.",
        "Soutenir et accompagner les aidants, refuser la marchandisation du grand âge.",
        "Habitat adapté intergénérationnel et clubs seniors pour rompre l'isolement social.",
        "Accès aux droits sans exclusion numérique.",
    ],

    # ═══════════════════════════════════════════
    # 7. DÉMOCRATIE
    # ═══════════════════════════════════════════
    "budget-participatif": [
        "Conseils citoyens de quartier décisionnaires par tirage au sort avec budgets dédiés.",
        "Conventions citoyennes par tirage au sort sur les grands sujets (déchets, ZFE, urbanisme).",
        "RIC municipal déclenché par 5 % des signatures des électeurs.",
    ],
    "transparence": [
        "Charte d'engagement des élus et plafonnement de l'indemnité du maire à 3 fois le salaire le plus bas.",
        "Droit de révocation des élus (10 % des signatures), droit de pétition (5 % déclenchent défense au conseil).",
        "Tableaux de bord publics des attributions et transparence des dépenses médias.",
        "Commission d'enquête municipale avec de vrais moyens.",
    ],
    "vie-associative": [
        "Fin de l'usage de la charte de la laïcité comme outil d'exclusion des associations.",
        "Égalité d'accès aux salles municipales et logiciel unique de réservation.",
        "Conventions pluriannuelles transparentes pour les associations.",
    ],
    "services-publics": [
        "Retour en régie publique de l'eau, l'énergie, les déchets et les transports.",
        "Services publics de proximité dans les quartiers : maisons de santé, équipements ouverts soirs et week-ends.",
        "Vote des 16+ et des résidents étrangers aux élections municipales.",
        "Campagne d'inscription sur les listes électorales.",
        "Assemblée citoyenne pour préparer la 6e République.",
    ],

    # ═══════════════════════════════════════════
    # 8. ÉCONOMIE
    # ═══════════════════════════════════════════
    "commerce-local": [
        "Bloquer l'extension de la grande distribution et renforcer la taxation des grandes surfaces.",
        "Droit de préemption sur le foncier commercial pour maintenir les commerces de proximité.",
        "Soutenir les épiceries solidaires et coopératives dans les quartiers populaires.",
    ],
    "emploi-insertion": [
        "Plan « 10 000 emplois non-délocalisables » et hôtels productifs municipaux.",
        "Commande publique avec critères sociaux et écologiques, soutien à l'ESS et aux SCOP.",
        "Plan de titularisation des agents municipaux et suppression du temps partiel subi.",
        "Pôles emploi de proximité et insertion professionnelle des femmes dans les quartiers populaires.",
        "Permanence municipale du droit du travail et locaux d'accueil pour livreurs indépendants.",
    ],
    "attractivite": [
        "Créer une Agence Métropolitaine d'Urbanisme.",
        "Mettre fin aux projets de « folies montpelliéraines » et aux mégaprojets coûteux.",
    ],

    # ═══════════════════════════════════════════
    # 9. CULTURE
    # ═══════════════════════════════════════════
    "equipements-culturels": [
        "Renforcer les Maisons Pour Tous et les médiathèques de proximité (gratuité, horaires étendus).",
        "Repenser le MOCO comme lieu d'arts populaires accessible à tous.",
        "Locaux municipaux vacants mis à disposition des artistes et collectifs émergents.",
        "1 % artistique dans toute construction publique.",
    ],
    "evenements-creation": [
        "Accès à l'enseignement artistique avec tarification sociale et culture dès la petite enfance.",
        "Soutien aux artistes et équipes locales émergentes, limiter l'IA pour préserver l'emploi artistique.",
        "Bifurcation écologique de la culture et agenda culturel interactif montpelliérain.",
        "Journée/festival annuel des langues et cultures.",
    ],

    # ═══════════════════════════════════════════
    # 10. SPORT
    # ═══════════════════════════════════════════
    "equipements-sportifs": [
        "Rénover les équipements sportifs de proximité et créer une salle de sport municipale publique.",
        "Ouvrir les équipements sportifs scolaires aux associations le soir et le week-end.",
        "Refuser la privatisation et le naming commercial des équipements sportifs.",
        "Gratuité des piscines municipales l'été.",
    ],
    "sport-pour-tous": [
        "Démocratiser la natation : apprentissage gratuit pour tous les enfants.",
        "Sport féminin, mixte et inclusif : garantir l'accès à la pratique via les équipements scolaires.",
        "Handisport et sport adapté dans tous les quartiers.",
    ],

    # ═══════════════════════════════════════════
    # 11. URBANISME
    # ═══════════════════════════════════════════
    "amenagement-urbain": [
        "S'opposer au COM et aux mégaprojets écocides, organiser des ateliers de quartier sur l'urbanisme.",
        "Mettre fin au mobilier urbain anti-SDF et installer du mobilier convivial (fontaines à eau, bancs).",
        "Créer des douches publiques et des fontaines à eau accessibles.",
    ],
    "accessibilite": [
        "Plan pluriannuel accessibilité : zéro lieu public inaccessible d'ici la fin du mandat.",
        "Diagnostic d'accessibilité PMR dans tout l'espace public et outil de signalement citoyen des zones non accessibles.",
        "Former tous les agents municipaux à l'accueil du handicap.",
        "Écoles inclusives avec matériel adapté et enseignement en LSF.",
        "Mobilité accessible : réseau de transport 100 % PMR.",
    ],
    "quartiers-prioritaires": [
        "Programme ANRU Saint-Martin co-construit avec les habitants, projet Paillade sud participatif.",
        "Zéro logement indigne dans les QPV : rénovation massive et combat des marchands de sommeil.",
        "Renforcer la fréquence bus/tram dans les quartiers populaires.",
        "Accès gratuit ou subventionné aux équipements culturels et sportifs dans les QPV.",
        "Végétalisation prioritaire des quartiers populaires : jardins partagés, lutte contre les nuisibles.",
    ],

    # ═══════════════════════════════════════════
    # 12. SOLIDARITÉ
    # ═══════════════════════════════════════════
    "aide-sociale": [
        "Employeur public féministe : revaloriser les catégories B et C, congé menstruel.",
        "Protection des étrangers précaires et accueil digne des mineurs non accompagnés.",
        "Cours de FLE dans les maisons municipales et dispositifs d'intégration des Gens du voyage.",
        "Délégation municipale dédiée au bien-être animal : centres vétérinaires publics, stérilisation chats errants, espaces refuges faune sauvage.",
    ],
    "egalite-discriminations": [
        "Observatoire municipal des discriminations avec CV anonymes et testing.",
        "Formation obligatoire de tout le personnel municipal contre les discriminations, le sexisme et les LGBTIphobies.",
        "Référent discrimination dans chaque service municipal.",
        "Mettre fin à l'instrumentalisation de la laïcité, la ville se constitue partie civile avec les victimes de racisme.",
        "Espaces d'accueil pour les victimes LGBTI et soutien aux Marches des Fiertés.",
        "Parité dans les noms de rues et commémoration des victimes de l'esclavage.",
    ],
    "pouvoir-achat": [
        "Tarification solidaire de l'énergie et de l'eau via les opérateurs publics municipaux.",
        "Gratuité des transports, cantines, fournitures scolaires et protections périodiques pour les plus modestes.",
        "Épiceries solidaires et restaurant populaire municipal à prix bas.",
    ],
}

# ── Relations internationales → democratie/transparence (closest fit)
# "Suspendre jumelage Tiberias, charte municipale relations internationales,
#  bureau permanent solidarité internationale" → ajouté à transparence
MAPPING["transparence"].append(
    "Charte municipale des relations internationales et bureau permanent de solidarité internationale."
)


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update candidate programmeUrl
    for cand in data["candidats"]:
        if cand["id"] == "oziol":
            cand["programmeUrl"] = "https://oziol2026.fr/"
            cand["programmeComplet"] = True
            break

    # Build proposition object
    def make_prop(mesures):
        return {
            "source": SOURCE,
            "sourceUrl": SOURCE_URL,
            "mesures": mesures,
        }

    # Update propositions
    total = 0
    stats = {}

    for cat in data["categories"]:
        cat_count = 0
        for st in cat["sousThemes"]:
            if st["id"] in MAPPING:
                mesures = MAPPING[st["id"]]
                st["propositions"]["oziol"] = make_prop(mesures)
                cat_count += len(mesures)
            # If not in mapping, leave existing value (null or previous)
        stats[cat["id"]] = cat_count
        total += cat_count

    # Write back
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Print stats
    print(f"\n{'='*50}")
    print(f"Programme Nathalie Oziol — Mise à jour terminée")
    print(f"{'='*50}\n")

    for cat in data["categories"]:
        cat_id = cat["id"]
        count = stats[cat_id]
        print(f"  {cat['nom']:40s} {count:3d} mesures")

    print(f"\n  {'TOTAL':40s} {total:3d} mesures")
    print(f"\n  Sous-thèmes couverts : {sum(1 for v in MAPPING.values() if v)}/44")
    print(f"  Fichier mis à jour : {JSON_PATH}")


if __name__ == "__main__":
    main()
