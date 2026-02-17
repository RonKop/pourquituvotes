#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intègre les propositions d'Isabelle Perrein (Montpellier) extraites du
programme PDF officiel (18 pages) + sources presse complémentaires.

v2 — basé sur le PDF complet (source primaire), remplace la v1 basée
     uniquement sur le site web et la presse.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "elections", "montpellier-2026.json")

SRC = "Programme Isabelle Perrein, Aimer Montpellier, 2026"
PDF = "https://cdn.prod.website-files.com/67ce914d990e9dc66d63cf0b/695e994f8f76e4d91dea4053_Programme_isabelle%20Perrein.pdf"

def p(texte, source=SRC, url=PDF):
    return {"texte": texte, "source": source, "sourceUrl": url}

# ═══════════════════════════════════════════════════════════════════
#  TOUTES les propositions mappées par sous-thème (PDF pp. 1-18)
# ═══════════════════════════════════════════════════════════════════
PROPS = {
    # ── SÉCURITÉ ──────────────────────────────────────────────────
    "police-municipale": p(
        "Doubler les effectifs de la police municipale (1 pour 1 000 habitants), "
        "installer des postes de police de proximité dans chaque quartier avec des équipes dédiées, "
        "ouvrir un poste central jour et nuit, renforcer le Groupe de Soutien Opérationnel (GSO), "
        "créer une unité spécialisée anti-harcèlement, lancer les cadets de la police municipale "
        "et mettre fin à la souffrance au travail des agents"
    ),
    "videoprotection": p(
        "Mettre en œuvre un véritable Centre de Supervision Urbain (CSU) 7j/7 24h/24 "
        "avec des professionnels formés, déployer des caméras intelligentes 360° "
        "avec lecture automatique des plaques, renouveler les véhicules et l'unité cynophile, "
        "et installer des bornes d'appel d'urgence dans les bâtiments publics, commerces, "
        "zones à forte affluence, devant les écoles et les lieux de culte"
    ),
    "prevention-mediation": p(
        "Appliquer la tolérance zéro : exclusion des logements sociaux pour les fauteurs de troubles, "
        "couvre-feu pour les mineurs en zones sensibles, suppression des aides municipales "
        "pour les récidivistes, constitution systématique de la ville en partie civile "
        "contre les trafiquants et auteurs de violences graves, "
        "et contrôles renforcés des épiceries de nuit avec respect strict de la loi"
    ),
    "violences-femmes": p(
        "Créer des places d'hébergement sécurisé pour les femmes victimes de violences et leurs enfants, "
        "mettre en place l'éloignement de l'agresseur avec hébergement dédié et suivi psychologique, "
        "renforcer l'éclairage et la vidéoprotection ciblée, éduquer au respect et au consentement "
        "dans 100 % des écoles, former tous les élus et agents municipaux, "
        "créer un référent municipal dédié et soutenir financièrement les associations d'aide aux victimes"
    ),

    # ── TRANSPORTS ────────────────────────────────────────────────
    "transports-en-commun": p(
        "Mettre en place des minibus au départ des arrêts de tramway desservant tous les quartiers, "
        "rétablir le cadencement et l'amplitude horaire antérieurs des transports en commun "
        "et créer une brigade métropolitaine des transports pour la sécurité"
    ),
    "velo-mobilites-douces": p(
        "Sécuriser les segments cyclables les plus dangereux (baromètre des villes cyclables), "
        "améliorer le balisage au sol, retirer la signalétique autorisant le sens interdit "
        "et le passage au feu rouge, et supprimer les pistes cyclables sur les trottoirs "
        "pour un partage de l'espace sécurisé entre piétons et cyclistes"
    ),
    "pietons-circulation": p(
        "Créer un anneau de circulation urbain pour désengorger Montpellier, "
        "revenir sur le plan de circulation du maire sortant, suspendre la Zone à Faible Émission (ZFE), "
        "assurer la continuité des cheminements piétons, sécuriser les passages piétons, "
        "ajouter des bancs et des ombrages, mettre en place des navettes gratuites en centre-ville "
        "pour les seniors et PMR, et approuver le Contournement Ouest de Montpellier (COM)"
    ),
    "stationnement": p(
        "Restaurer les capacités de stationnement, rétablir les places de livraison, "
        "créer des parkings silos pour limiter l'étalement urbain "
        "et offrir un stationnement gratuit pour les professionnels de santé"
    ),
    "tarifs-gratuite": p(
        "Mettre fin à la gratuité des transports pour tous et la remplacer par une gratuité intelligente : "
        "gratuit pour les jeunes et les retraités, tarif solidaire pour les actifs"
    ),

    # ── LOGEMENT ──────────────────────────────────────────────────
    "logement-social": p(
        "Réhabiliter les logements sociaux avec gardiennage, bonne isolation thermique "
        "et panneaux photovoltaïques pour plus de pouvoir d'achat et de sécurité"
    ),
    "acces-logement": p(
        "Viser 50 % de propriétaires à Montpellier grâce à la densification intelligente, "
        "des prix abordables, la location-accession et le logement coopératif"
    ),

    # ── ÉDUCATION ─────────────────────────────────────────────────
    "petite-enfance": p(
        "Créer 500 places de crèches supplémentaires et veiller au bon équipement "
        "des crèches en termes d'accessibilité"
    ),
    "ecoles-renovation": p(
        "Rénover les établissements scolaires (climatisation, auvents contre la pluie), "
        "transformer chaque école en centre éducatif complet avec orthophonistes, "
        "psychomotriciens, infirmières et psychologues au cœur de l'école, "
        "et développer des ateliers d'arts, de sport et de citoyenneté"
    ),
    "periscolaire-loisirs": p(
        "Proposer des activités éducatives de quartier dans tous les lieux publics "
        "et pendant les vacances scolaires (piscines, gymnases, maisons pour tous) "
        "en partenariat avec les clubs sportifs, opéras, conservatoires et musées"
    ),
    "jeunesse": p(
        "Créer un passeport permis sport et emploi pour les jeunes de 16 à 25 ans, "
        "installer une Maison des Stagiaires pour la rencontre entreprises-jeunes "
        "et lancer une plateforme numérique innovante pour découvrir les métiers et formations locales"
    ),

    # ── ENVIRONNEMENT ─────────────────────────────────────────────
    "espaces-verts": p(
        "Créer des quartiers havres de paix verdoyants avec potagers urbains, zones de lecture, "
        "espaces sportifs, parcs à chiens et jardins sensoriels, "
        "rénover le Peyrou et classer le Parc Montcalm pour que la population se l'approprie"
    ),
    "proprete-dechets": p(
        "Revoir la fréquence de nettoyage selon la vie réelle des quartiers, "
        "installer des colonnes de tri modernes et verbaliser les incivilités, "
        "développer le tri à la source pour recycler 80 % des déchets, lancer le compostage massif, "
        "remplacer le projet de four à CSR par un incinérateur écologique mieux positionné "
        "et mettre en place un système de nettoiement aux eaux grises"
    ),
    "renovation-energetique": p(
        "Implanter des data centers de proximité pour alimenter un réseau de chaleur urbain "
        "(réduction de 25 % de la facture de chauffage, financé par le secteur privé), "
        "installer des compteurs individuels d'eau dans les logements collectifs "
        "et équiper les logements sociaux de panneaux photovoltaïques"
    ),
    "alimentation-durable": p(
        "Créer des épiceries solidaires locales avec des producteurs locaux "
        "pour offrir des produits de qualité à prix solidaires"
    ),

    # ── SANTÉ ─────────────────────────────────────────────────────
    "centres-sante": p(
        "Implanter des maisons de santé pluridisciplinaires, "
        "limiter le temps d'attente aux urgences, "
        "ouvrir la circulation sur les voies de bus aux soignants et assistants de vie à domicile, "
        "et offrir un forfait gratuité de 2h par jour sur les parkings des hôpitaux pour les familles"
    ),
    "prevention-sante": p(
        "Mettre en place un référent rappelant les droits des enfants malades, "
        "diffuser les documents MDPH/CAF/CPAM dans tous les lieux publics, "
        "lutter contre le renoncement aux soins "
        "et publier une page dédiée à la santé et la prévention dans chaque bulletin municipal"
    ),
    "seniors": p(
        "Créer une réserve de seniors actifs pour le lien intergénérationnel dans les maisons pour tous, "
        "installer un conseil consultatif des seniors pour élaborer et financer des projets, "
        "développer l'accompagnement renforcé à domicile "
        "et sensibiliser les syndics pour l'installation d'ascenseurs et de monte-charges"
    ),

    # ── DÉMOCRATIE ────────────────────────────────────────────────
    "budget-participatif": p(
        "Créer une plateforme locale de financement participatif connectée aux acteurs économiques "
        "du territoire pour soutenir directement les projets des habitants"
    ),
    "transparence": p(
        "Lancer un audit global des finances de la ville et de la métropole dès le début du mandat, "
        "mettre en ligne tous les postes de dépenses municipales "
        "et garantir une attribution transparente des subventions"
    ),
    "vie-associative": p(
        "Créer une maison des associations dans chaque quartier avec un bureau pour chacune "
        "et une salle partagée, regrouper les associations humanitaires pour plus d'efficacité "
        "et renforcer l'accompagnement dans les démarches de subventions"
    ),
    "services-publics": p(
        "Recruter les adjoints selon leurs compétences, assurer le maillage des médiathèques, "
        "créer un guichet unique pour orienter vers les associations et services publics, "
        "mettre en place une ligne téléphonique dédiée au handicap avec formation spécifique des agents "
        "et nommer un référent handicap au sein du personnel municipal"
    ),

    # ── ÉCONOMIE ──────────────────────────────────────────────────
    "commerce-local": p(
        "Dynamiser les 6 800 commerces montpelliérains par la sécurité, la propreté "
        "et l'accessibilité, rétablir les places de livraison, restaurer l'accès automobile "
        "au centre-ville, et animer les marchés, halles et places emblématiques"
    ),
    "emploi-insertion": p(
        "Créer des emplois locaux en dotant l'agence de développement économique d'une feuille de route claire, "
        "développer des formations en lien avec les besoins des entreprises locales via France Travail, "
        "créer un fonds d'investissement public/privé pour les entreprises qui embauchent localement "
        "et installer une Maison des Stagiaires"
    ),
    "attractivite": p(
        "Développer les filières d'excellence (santé, IA, agroalimentaire, cinéma, aéronautique), "
        "attirer des ETI, PME et PMI, mettre en place un PLUI économique "
        "pour préserver les zones d'activités et empêcher leur mutation en zones d'habitation"
    ),

    # ── CULTURE ───────────────────────────────────────────────────
    "equipements-culturels": p(
        "Installer des kiosques animés dans tous les quartiers pour une culture de proximité, "
        "créer un HandiPass (billet gratuit pour l'accompagnant d'une personne handicapée), "
        "lancer l'Appli Ville de Montpellier avec toute l'offre culturelle, "
        "amener la culture à l'école et dans les rues, "
        "et se réapproprier les équipements culturels (centre d'art contemporain, médiathèques, musées, théâtres)"
    ),
    "evenements-creation": p(
        "Promouvoir les talents montpelliérains via un comité artistique indépendant, "
        "relancer le Festival Méditerranéen du cinéma, soutenir les festivals en danger "
        "(Festival du Blues, Palmarosa), organiser chaque année un grand concert de l'été, "
        "développer des festivals OFF et attirer des artistes de renommée nationale et internationale"
    ),

    # ── SPORT ─────────────────────────────────────────────────────
    "equipements-sportifs": p(
        "Créer une Cité du Sport où se rencontrent clubs et écoles de sport, "
        "accompagner les projets des clubs professionnels au cas par cas "
        "et construire une grande enceinte sportive partagée multifonctionnelle"
    ),
    "sport-pour-tous": p(
        "Garantir l'accès au sport dès l'école avec pratique régulière et accès aux équipements, "
        "créer des City Parcs pour les jeunes, les PMR et les aînés avec parcours de santé, "
        "et détecter les talents sportifs dès l'école en partenariat avec les clubs"
    ),

    # ── URBANISME ─────────────────────────────────────────────────
    "amenagement-urbain": p(
        "Reconstruire la ville sur elle-même : densification intelligente avec îlots de fraîcheur, "
        "rénover plutôt que raser, élaborer un schéma directeur clair "
        "(accessibilité, écologie, équilibre habitat-économie), "
        "réserver des locaux pour crèches, épiceries solidaires et maisons de santé, "
        "et mettre à disposition des artistes les bas d'immeubles vacants"
    ),
    "accessibilite": p(
        "Appliquer le principe d'accessibilité universelle : rénover les trottoirs pour les PMR, "
        "rendre les transports en commun pleinement accessibles, "
        "créer une maison du handicap partagée avec la maison des aînés, "
        "doter les salles de sport et musées d'équipements adaptés, "
        "indiquer les itinéraires et toilettes accessibles via l'application Ville de Montpellier "
        "et organiser un mois dédié au handicap avec sensibilisation et partage"
    ),
    "quartiers-prioritaires": p(
        "Faire de chaque quartier un cœur battant : places animées, fontaines, jeux pour enfants, "
        "espaces de coworking extérieur, marchés de producteurs, "
        "et réserver des locaux pour crèches, épiceries solidaires et maisons de santé"
    ),

    # ── SOLIDARITÉ ────────────────────────────────────────────────
    "aide-sociale": p(
        "Recentrer les CCAS sur l'essentiel avec une analyse approfondie des besoins sociaux, "
        "garantir la domiciliation des personnes sans abri avec accompagnement vers l'autonomie, "
        "mettre en place un fichier actualisé des bénéficiaires pour une aide ciblée et pérenne"
    ),
    "egalite-discriminations": p(
        "Favoriser l'autonomie et l'inclusion des personnes handicapées : "
        "logement dédié (maisons Simon de Cyrène), HandiPass sport et culture, "
        "zones PMR pour tous les événements, sites internet accessibles aux malvoyants, "
        "référent handicap dans la mairie et la métropole, "
        "et conditionnement des subventions sportives à la désignation d'un référent violences"
    ),
    "pouvoir-achat": p(
        "Réduire la TEOM de 15 % en la remplaçant par une taxe incitative liée au tri, "
        "créer des épiceries solidaires avec producteurs locaux, "
        "installer des compteurs individuels d'eau dans les logements collectifs, "
        "et produire un chauffage urbain via data centers pour réduire la facture de 25 %"
    ),
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    added = 0

    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            sid = st["id"]
            if sid in PROPS:
                old = st["propositions"].get("perrein")
                st["propositions"]["perrein"] = PROPS[sid]
                if old is None:
                    added += 1
                    print(f"  + {sid}: AJOUTÉ")
                else:
                    updated += 1
                    print(f"  ~ {sid}: MIS À JOUR")

    # Mettre à jour le candidat
    for c in data["candidats"]:
        if c["id"] == "perrein":
            c["programmeComplet"] = True
            c["programmeUrl"] = "https://www.isabelleperrein2026.fr/notre-projet"
            c["programmePdfPath"] = "programme_perrein_montpellier.pdf"
            c["siteCampagne"] = "https://www.isabelleperrein2026.fr/"
            print(f"\n  programmeComplet -> true")
            print(f"  programmePdfPath -> data/programmes/programme_perrein_montpellier.pdf")
            break

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n  Résultat: {updated} mis à jour, {added} ajoutés")
    print(f"  Total sous-thèmes Perrein: {updated + added}")


if __name__ == "__main__":
    main()
