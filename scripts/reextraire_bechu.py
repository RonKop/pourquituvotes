#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction des propositions de Christophe Béchu (Angers, municipales 2026).
Sources :
  - Site angersbechu.fr (programme officiel)
  - my-angers.info (Angers Info, 13/02/2026)
  - Angers Villactu (articles programme)
  - angersloiremetropole.fr (plan vélo)
"""
import io, json, os, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JSON_PATH = os.path.join(ROOT_DIR, "data", "elections", "angers-2026.json")
SOURCE = "Programme officiel 2026 — Christophe Béchu"
SOURCE_URL = "https://www.angersbechu.fr/programme/"
CANDIDAT_ID = "bechu"

MESURES = {
    # ── SÉCURITÉ ──
    "police-municipale": [
        "Augmentation des effectifs de police municipale de 75 à 100 agents.",
        "Déploiement de l'armement létal d'abord pour les équipes de nuit, puis pour l'ensemble des 75 policiers municipaux.",
    ],
    "videoprotection": [
        "Déploiement de 150 caméras supplémentaires pour porter le réseau à 450 caméras de vidéoprotection.",
        "Amélioration de la résolution des caméras pour une meilleure précision de zoom.",
    ],
    "prevention-mediation": [
        "Adoption d'un plan spécifique contre les incivilités et le bruit.",
        "Renforcement de la présence humaine dans l'espace public pour assurer la tranquillité du quotidien.",
    ],
    # ── TRANSPORTS ──
    "transports-en-commun": [
        "Acquisition de rames supplémentaires pour mettre en place des trams rallongés aux heures de pointe.",
        "Gratuité des transports en commun pour les sorties scolaires.",
    ],
    "velo-mobilites-douces": [
        "Ouverture d'une maison du vélo et des mobilités près de la gare.",
        "Atteindre 160 km de voies cyclables sécurisées (réseau Irigovélo) d'ici 2030.",
        "Doublement du budget plan vélo à 7 millions d'euros par an.",
    ],
    "tarifs-gratuite": [
        "Mise en place de la gratuité des transports en commun.",
    ],
    # ── LOGEMENT ──
    "logement-social": [
        "Création d'une bourse d'échanges de logements dans le parc social, validée par les bailleurs et la collectivité.",
    ],
    "acces-logement": [
        "Mise en place d'une assurance communale habitation à tarifs négociés pour couvrir les 2-3 % de ménages non assurés.",
    ],
    # ── ÉDUCATION ──
    "petite-enfance": [
        "Faire de l'enfance et la jeunesse la grande cause du mandat : petite enfance, soutien à la parentalité, réussite éducative.",
        "Organisation d'Assises de la Parentalité et de la Famille dès le début du mandat.",
    ],
    "ecoles-renovation": [
        "Améliorer les conditions d'apprentissage des enfants en veillant à la qualité des écoles.",
        "Renforcer l'offre périscolaire et l'égalité des chances pour les jeunes Angevins.",
        "Végétalisation de toutes les cours d'école d'ici fin 2027.",
    ],
    "cantines-fournitures": [
        "Poursuivre la montée en gamme de la restauration scolaire Papillote & Compagnie (42 % de bio atteint, objectif supérieur).",
    ],
    "periscolaire-loisirs": [
        "Maintenir la gratuité des activités périscolaires.",
    ],
    "jeunesse": [
        "Faire de l'enfance et l'adolescence la grande cause du mandat avec la lutte contre la surexposition aux écrans.",
        "Offrir un abonnement à un magazine de lecture pour les élèves de CE1 et CE2.",
        "Déployer un dispositif de terrain pour les jeunes souffrant de difficultés psychologiques.",
        "Créer un médicampus pour lutter contre les fausses informations en santé.",
    ],
    # ── ENVIRONNEMENT ──
    "espaces-verts": [
        "Lancer un plan parc annuel : revégétalisation des parcs de Villechien, du Haras et de Bellefontaine.",
        "Végétalisation de la rue Saint-Aubin dès le début du mandat.",
        "Création de 68 hectares de nature en ville depuis 2014, poursuite de l'effort.",
    ],
    "proprete-dechets": [
        "Installation de filets collecteurs de déchets dans la Maine.",
    ],
    "climat-adaptation": [
        "Organisation des Assises de la transition écologique avec élus, associations, ADEME, scientifiques et citoyens.",
        "Plan d'adaptation climatique visant une métropole zéro carbone.",
    ],
    "renovation-energetique": [
        "Poursuite de l'isolation des bâtiments municipaux et scolaires.",
    ],
    # ── SANTÉ ──
    "centres-sante": [
        "Rejet de la mutuelle communale classique ; mise en place d'une assurance habitation communale négociée comme alternative sociale.",
    ],
    "prevention-sante": [
        "Augmentation du plafond de ressources du CCAS de 10 % pour élargir le nombre de bénéficiaires.",
    ],
    "seniors": [
        "Accompagnement des personnes âgées au quotidien : diversification des solutions de logement et lutte contre l'isolement.",
        "Augmentation du budget CCAS de 1,6 million d'euros pour le soutien aux seniors.",
        "Présentation d'un rapport CCAS tous les deux mois au conseil municipal.",
    ],
    # ── DÉMOCRATIE ──
    "transparence": [
        "198 propositions réalisables sur 6 ans et finançables sans aucune augmentation des impôts.",
        "Programme décliné quartier par quartier avec 10 documents spécifiques et 50 propositions géolocalisées.",
    ],
    "vie-associative": [
        "Mise à disposition de véhicules adaptés pour les personnes en situation de handicap via les associations.",
    ],
    "services-publics": [
        "Relogement de la maison de quartier centre-ville place Saint-Éloi dans un espace unifié avec 150 m² supplémentaires.",
    ],
    # ── ÉCONOMIE ──
    "commerce-local": [
        "Confier la compétence commerce à l'agence Aldev pour professionnaliser la redynamisation.",
        "Démarcher les enseignes nationales manquantes pour les inciter à s'implanter à Angers.",
        "Création d'une foncière commerciale pour racheter les locaux vacants en centre-ville.",
        "Mise en place d'équipes de gestion de centre-ville (centre-ville managers).",
    ],
    "emploi-insertion": [
        "Accompagnement de l'implantation de halles alimentaires sur le site Cœur de Maine.",
    ],
    "attractivite": [
        "Inscrire l'IceParc dans la dynamique des Jeux des Alpes 2030 : Angers ville hôte d'entraînement des équipes nationales.",
    ],
    # ── CULTURE ──
    "equipements-culturels": [
        "Création d'un film office (bureau des tournages) pour le cinéma à Angers.",
        "Mise en place d'une artothèque citoyenne permettant d'emprunter des œuvres d'artistes locaux, installée au Lac de Maine.",
        "Rénovation de la médiathèque Toussaint avec intégration au jardin des beaux-arts transformé en jardin de sculptures.",
        "Transformation de l'hôtel de la Godeline en salle de bal et de danse.",
    ],
    # ── SPORT ──
    "equipements-sportifs": [
        "Réaménagement de la halle Jean-Bouin pour accompagner le basket de haut niveau à Angers.",
        "Création d'une piste de BMX sur un site alternatif après la non-reconstruction du vélodrome.",
    ],
    "sport-pour-tous": [
        "Organiser des états généraux du football pour soutenir les clubs et reconnaître leur rôle éducatif et d'enracinement urbain.",
    ],
    # ── URBANISME ──
    "amenagement-urbain": [
        "Végétalisation de la rue Saint-Aubin pour améliorer l'expérience piétonne en centre-ville.",
    ],
    "quartiers-prioritaires": [
        "Opérations de renouvellement urbain prioritaires sur les quartiers Monplaisir et Belle-Beille.",
        "Programme décliné en 10 documents spécifiques par quartier avec des propositions géolocalisées.",
    ],
    # ── SOLIDARITÉ ──
    "aide-sociale": [
        "Augmentation du plafond de ressources du CCAS de 10 % pour élargir l'accès aux aides sociales.",
        "Approche solidaire « accueillir, aider, agir, accompagner » tout en évitant l'assistanat.",
    ],
    "pouvoir-achat": [
        "Aucune augmentation des impôts locaux sur l'ensemble du mandat.",
    ],
}


def main():
    print("=" * 60)
    print(f"  RÉ-EXTRACTION {CANDIDAT_ID.upper()} (Angers)")
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
