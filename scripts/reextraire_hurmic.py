#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ré-extraction des mesures de Pierre Hurmic (Bordeaux 2026)
Sources : pierrehurmic2026.fr — pages programme thématiques + quartiers
"""
import io, json, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "bordeaux-2026.json")
SOURCE = "Programme officiel 2026 — Pierre Hurmic"
SOURCE_URL = "https://pierrehurmic2026.fr/notre-programme/"
CANDIDAT_ID = "hurmic"

MESURES = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Augmenter de 50 % les effectifs de policiers municipaux et d'agents de surveillance.",
        "Créer 3 nouvelles brigades de police municipale territorialisées.",
        "Développer les patrouilles à pied et à vélo dans tous les quartiers.",
        "Renforcer la brigade anti-incivilités (propreté, tags, dépôts sauvages).",
        "Élargir le champ de la charte éthique de la police municipale.",
    ],
    "videoprotection": [
        "Doubler le nombre de caméras de vidéoprotection dans la ville.",
    ],
    "prevention-mediation": [
        "Renforcer la médiation sociale dans tous les quartiers, y compris en zones nocturnes.",
        "Déployer des « Promeneurs du Net » sur les réseaux sociaux pour la prévention jeunesse.",
        "Mettre en place un plan municipal de prévention des comportements à risque chez les jeunes.",
        "Créer un « Forum tranquillité » dans chaque quartier de vie.",
        "Adopter une charte de la vie nocturne responsable avec patrouilles de médiation.",
    ],
    "violences-femmes": [
        "Renforcer le dispositif « Demandez Angela » dans les établissements de nuit.",
        "Organiser un mois de sensibilisation annuel contre le harcèlement de rue.",
        "Installer des points de sensibilisation dans les zones passantes.",
    ],

    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Augmenter les fréquences du tramway et des lignes de bus.",
        "Mettre en œuvre le RER métropolitain avec la Métropole.",
        "Déployer 5 lignes de bus express d'ici 2030.",
        "Lancer la navette fluviale BATO entre Queyries et Quinconces.",
    ],
    "velo-mobilites-douces": [
        "Doubler le rythme des aménagements cyclables pour achever le réseau express vélo d'ici 2030.",
        "Créer des parkings vélos sécurisés dans tous les quartiers.",
        "Déployer des « vélo-taxis » comme solution de mobilité douce.",
        "Aménager un grand tour piéton et vélo autour du lac.",
    ],
    "pietons-circulation": [
        "Sécuriser les itinéraires piétons végétalisés dans tous les quartiers.",
        "Aménager les abords des écoles et des structures seniors pour la sécurité piétonne.",
        "Transformer les grands boulevards en « rues du XXIe siècle » apaisées et végétalisées.",
        "Moderniser la gestion du trafic urbain pour fluidifier la circulation.",
        "Créer une passerelle piétons-vélos dédiée reliant les deux rives de la Garonne.",
    ],
    "stationnement": [
        "Expérimenter de nouveaux lieux de stationnement en centre-ville.",
        "Multiplier les parkings moto/scooter et les stations d'autopartage.",
    ],
    "tarifs-gratuite": [
        "Étendre la tarification solidaire aux transports, stationnement, piscines et services publics.",
        "Étudier la gratuité des transports en commun pour les enfants de moins de 10 ans.",
    ],

    # ── LOGEMENT ──
    "logement-social": [
        "Amplifier la production de logements sociaux pour atteindre 25 % réglementaires.",
        "Créer 3 000 logements sociaux pour jeunes et étudiants d'ici 2030.",
        "Développer des logements sociaux mixtes jeunes-seniors intergénérationnels.",
    ],
    "logements-vacants": [
        "Lancer le programme « Territoire Zéro Logement Passoire » contre la vacance et l'insalubrité.",
    ],
    "encadrement-loyers": [
        "Poursuivre l'encadrement des loyers et renforcer les contrôles Airbnb.",
        "Expérimenter l'encadrement des loyers commerciaux.",
    ],
    "acces-logement": [
        "Développer l'accession sociale à la propriété pour les classes moyennes.",
        "Proposer des solutions de logements solidaires (colocations seniors, habitat participatif, viager solidaire).",
        "Construire 2 500 logements abordables dans le nouveau quartier bas carbone de la Jallère.",
    ],

    # ── ÉDUCATION ──
    "petite-enfance": [
        "Créer plus de 200 nouvelles places en crèches sur le mandat.",
        "Ouvrir 2 maisons d'assistantes maternelles municipales.",
        "Expérimenter des crèches en plein air.",
        "Viser 100 % de bio dans les crèches municipales.",
    ],
    "ecoles-renovation": [
        "Poursuivre la rénovation massive des écoles bordelaises.",
        "Améliorer le rafraîchissement estival et le confort hivernal des établissements scolaires avec ombrières.",
        "Soutenir « l'école dehors » avec des espaces adaptés et des cours buissonnières.",
        "Ouvrir les cours d'écoles en squares accessibles les week-ends et vacances.",
    ],
    "cantines-fournitures": [
        "Construire une cuisine centrale municipale en « fait maison ».",
        "Viser 100 % de bio et local dans les cantines scolaires.",
        "Instaurer la gratuité progressive des fournitures scolaires.",
    ],
    "periscolaire-loisirs": [
        "Développer l'offre d'accueil périscolaire dans tous les quartiers.",
        "Créer les « Drôles de Samedis » : activités parents-enfants pour les 0-6 ans.",
        "Proposer des accueils ados encadrés en soirée.",
        "Lancer le programme « Vacances solidaires » pour permettre à tous les enfants de partir.",
    ],
    "jeunesse": [
        "Lancer l'application « Mes Premières Fois » pour guider les jeunes vers l'autonomie.",
        "Mener des campagnes de sensibilisation à la désinformation et aux bonnes pratiques numériques.",
        "Mettre en place le programme « Enfants-Ados-Parents & Écrans ».",
        "Créer un programme d'opportunités internationales pour les 18-25 ans.",
    ],

    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Créer 7 nouveaux parcs dans les quartiers déficitaires en espaces verts.",
        "Réaménager 6 grandes places arborées pour lutter contre les îlots de chaleur.",
        "Créer des îlots de fraîcheur à moins de 5 minutes à pied de chaque habitant.",
        "Installer des trames ombragées et végétalisées (rues voilées l'été, fontaines).",
        "Développer « Petits pas dans la ville » : espaces ludiques pour enfants dans les parcs.",
    ],
    "proprete-dechets": [
        "Renforcer les équipes de propreté le week-end dans les quartiers animés.",
        "Doubler la brigade anti-incivilités dédiée à la propreté et aux tags.",
        "Proposer des déchetteries mobiles de quartier.",
        "Étendre le dispositif « Ici Toilettes » en partenariat avec les commerces.",
    ],
    "climat-adaptation": [
        "Renforcer le plan canicule avec des lieux publics climatisés gratuits.",
        "Rafraîchir les écoles et crèches via la rénovation thermique et des ombrières.",
        "Gérer l'eau via une régie publique et cesser d'utiliser l'eau potable pour l'arrosage des espaces publics.",
        "Reconnaître des droits juridiques à la Garonne.",
    ],
    "renovation-energetique": [
        "Atteindre 100 % d'autonomie énergétique pour les bâtiments publics.",
        "Finaliser le passage à 100 % LED de l'éclairage public.",
        "Solariser une quarantaine de sites publics.",
        "Diminuer de 40 % les consommations énergétiques du patrimoine public d'ici 2030.",
    ],
    "alimentation-durable": [
        "Rénover le Marché des Capucins en gestion municipale directe.",
        "Valoriser le MIN comme distributeur de produits locaux et de circuits courts.",
        "Accompagner l'installation d'activités nourricières en territoire girondin.",
    ],

    # ── SANTÉ ──
    "centres-sante": [
        "Ouvrir des centres de santé municipaux dans les quartiers déficitaires en médecins.",
        "Créer un centre municipal de santé aux Aubiers opérationnel dès 2027.",
    ],
    "prevention-sante": [
        "Mener des campagnes de prévention des addictions.",
        "Ouvrir des lieux de soins pour usagers de drogues.",
        "Former aux premiers secours en santé mentale.",
        "Créer une équipe mobile spécialisée dans le refus scolaire anxieux.",
        "Développer une offre spécifique en santé mentale pour les jeunes.",
    ],
    "seniors": [
        "Organiser des rencontres entre seniors pour lutter contre l'isolement.",
        "Déployer des services civiques de quartier pour accompagner les personnes âgées.",
        "Faciliter l'accès au sport pour les seniors et développer le sport sur ordonnance.",
        "Créer le label « Établissements Seniors Inclusifs ».",
        "Adapter l'habitat des personnes âgées (colocations seniors, habitat participatif, viager solidaire).",
        "Développer la médiation animale en établissements pour personnes âgées.",
    ],

    # ── DÉMOCRATIE ──
    "budget-participatif": [
        "Réinventer le budget participatif avec de nouvelles modalités.",
        "Organiser des votes par quartier de vie sur les projets locaux.",
    ],
    "transparence": [
        "Rendre les pétitions citoyennes recevables dès 2 000 signatures.",
        "Utiliser des outils numériques souverains et éthiques (IA, respect de la vie privée).",
        "Simplifier les démarches administratives municipales.",
    ],
    "vie-associative": [
        "Financer les associations sur plusieurs années de manière sécurisée.",
        "Valoriser le bénévolat et garantir l'indépendance associative.",
        "Offrir des bonus financiers aux associations inclusives.",
        "Renforcer l'« Atelier des initiatives » pour accompagner les projets citoyens.",
    ],
    "services-publics": [
        "Créer 30 quartiers de vie pour rapprocher les services municipaux des habitants.",
    ],

    # ── ÉCONOMIE ──
    "commerce-local": [
        "Déployer l'Office du Commerce en partenariat avec la CCI.",
        "Mettre en œuvre un plan de sauvegarde des commerces de quartier.",
        "Valoriser le commerce indépendant engagé et l'artisanat local.",
        "Pérenniser « Bordeaux se met au verre » pour réduire les déchets commerciaux.",
    ],
    "emploi-insertion": [
        "Prolonger l'expérience « Territoire zéro chômeur de longue durée » au Grand Parc.",
        "Faciliter l'accès aux marchés publics pour les petites entreprises locales.",
        "Organiser une conférence sociale territoriale avec les acteurs économiques.",
        "Conditionner les aides publiques à des critères environnementaux et sociaux.",
    ],
    "attractivite": [
        "Accompagner la création d'un pôle numérique souverain à Bordeaux.",
        "Doubler la capacité d'acquisition de locaux économiques par la foncière publique.",
        "Créer des centres de logistique urbaine pour des livraisons décarbonées.",
        "Accueillir 10 000 entrepreneurs à Bordeaux d'ici 2032.",
        "Mobiliser les entreprises autour d'un dividende territorial.",
    ],

    # ── CULTURE ──
    "equipements-culturels": [
        "Garantir la liberté de création et d'expression artistique.",
        "Ouvrir la Bourse du travail aux pratiques artistiques amateurs.",
        "Renforcer l'accessibilité des pratiques artistiques amateurs dans tous les quartiers.",
        "Associer les habitants à la programmation des établissements culturels municipaux.",
        "Protéger et adapter le patrimoine bordelais aux enjeux contemporains.",
    ],
    "evenements-creation": [
        "Instaurer « 100 % Éducation artistique et culturelle » pour tous les élèves bordelais.",
        "Intensifier les actions culturelles hors les murs dans chaque quartier.",
        "Soutenir les artistes locaux et développer des ateliers d'artistes.",
        "Reconnaître le « droit à la fête » avec une charte vie nocturne responsable.",
    ],

    # ── SPORT ──
    "equipements-sportifs": [
        "Rénover les équipements sportifs existants et les adapter au parasport.",
        "Créer des parcours de running sécurisés.",
        "Moderniser le site sportif Charles-Martin à Bacalan.",
        "Rénover le complexe sportif Stéhélin (stade athlétisme, gymnase).",
    ],
    "sport-pour-tous": [
        "Développer des écoles multisports pour les enfants.",
        "Soutenir la pratique féminine avec un accès égal aux équipements sportifs.",
        "Développer le sport sur ordonnance.",
        "Soutenir les clubs et sportifs de haut niveau, avec priorité au sport féminin.",
    ],

    # ── URBANISME ──
    "amenagement-urbain": [
        "Créer 30 quartiers de vie pour plus de proximité et de convivialité.",
        "Lancer le grand projet urbain autour du lac avec le quartier bas carbone de la Jallère.",
        "Transformer la zone commerciale du Lac.",
        "Apaiser et végétaliser les allées de Tourny.",
        "Réaménager les quais de Garonne (cyclabilité, îlots fraîcheur).",
        "Végétaliser et réorganiser la place Victoire.",
    ],
    "accessibilite": [
        "Rendre 100 % des équipements publics accessibles aux personnes en situation de handicap.",
        "Sécuriser et adapter les trajets piétons pour les personnes à mobilité réduite.",
        "Systématiser l'intégration du genre et du handicap dans la construction d'équipements.",
    ],
    "quartiers-prioritaires": [
        "Ouvrir un centre de santé municipal, un centre d'animation et une crèche aux Aubiers.",
        "Lancer un plan propreté coordonné Ville-Métropole-Bailleurs dans les quartiers prioritaires.",
        "Réhabiliter le centre social et d'animation l'Escargot au Grand Parc.",
        "Rénover le centre commercial Europe au Grand Parc.",
    ],

    # ── SOLIDARITÉ ──
    "aide-sociale": [
        "Plan d'action avec l'État : zéro enfant sans abri à Bordeaux.",
        "Ouvrir des hébergements d'urgence et des accueils de jour.",
        "Développer l'habitat léger avec accompagnement social.",
        "Créer une cantine solidaire municipale.",
        "Renforcer la solidarité alimentaire (épiceries sociales et solidaires).",
    ],
    "egalite-discriminations": [
        "Intégrer l'égalité femmes-hommes dans toutes les politiques municipales.",
        "Former les agents municipaux au sexisme ordinaire et aux inégalités filles-garçons.",
        "Amplifier le « Mois des fiertés » à Bordeaux.",
        "Concevoir des campagnes municipales contre le racisme et l'antisémitisme.",
        "Soutenir les associations d'accompagnement des migrants.",
        "Coconstruire un plan d'action sur la mémoire de l'esclavage et de la colonisation.",
    ],
    "pouvoir-achat": [
        "Étendre la tarification solidaire au stationnement, piscines, concessions funéraires et services publics.",
        "Proposer des commandes groupées à tarifs avantageux pour les Bordelais.",
        "Soutenir les associations offrant des soins vétérinaires gratuits.",
    ],
}


def main():
    print("=" * 60)
    print(f"  RÉ-EXTRACTION {CANDIDAT_ID.upper()} (Bordeaux)")
    print("=" * 60)
    total = sum(len(v) for v in MESURES.values())
    print(f"\n  {total} mesures dans {len(MESURES)} sous-thèmes")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id in MESURES and len(MESURES[st_id]) > 0:
                prop = st["propositions"].get(CANDIDAT_ID)
                if prop is None:
                    prop = {}
                    st["propositions"][CANDIDAT_ID] = prop
                old_count = len(prop.get("mesures", []))
                new_mesures = MESURES[st_id]
                if len(new_mesures) >= old_count:
                    prop["mesures"] = new_mesures
                    prop["source"] = SOURCE
                    prop["sourceUrl"] = SOURCE_URL
                    updated += 1
                    if old_count != len(new_mesures):
                        print(f"    {st_id}: {old_count} -> {len(new_mesures)}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n    {updated} sous-thèmes mis à jour")
    print("=" * 60)


if __name__ == "__main__":
    main()
