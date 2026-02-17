#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate crawl_results JSON files for 7 candidates with concrete propositions."""

import json
import os
from pathlib import Path

def main():
    os.makedirs('crawl_results', exist_ok=True)

    # 1. CAEN - LECOUTOUR
    caen_lecoutour = {
        "securite/police-municipale": {
            "texte": "Ouverture permanences police municipale dans quartiers avec îlotage visible au plus près des habitants.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "sante/prevention-sante": {
            "texte": "Création Centre Municipal de Prévention pour coordonner actions jeunes et seniors avec CPAM et CAF.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "sante/seniors": {
            "texte": "Adaptation environnement urbain aux fragiles. En 2050, 1 habitant sur 5 aura 65+ ans. Élargissement Conseil Aînés.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "education/petite-enfance": {
            "texte": "Création nouvelles places: Maisons Assistantes Maternelles et Dispositifs Mosaic de Trois Ans dans locaux scolaires vacants.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "logement/logement-social": {
            "texte": "Priorité logements sociaux et petites surfaces pour étudiants et aînés. Bail Réel Solidaire pour ménages modestes.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "transports/velo-mobilites-douces": {
            "texte": "Plan cyclable continu pour 2027 et zones de rencontre pour cohabitation pacifique de tous déplacements.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "transports/pietons-circulation": {
            "texte": "Moratoire 6 mois extension tramway pour études. Zones rencontre pour cohabitation pacifique.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "environnement/renovation-energetique": {
            "texte": "Gestion publique eau, étude régie municipale énergie et adjoint dédié sobriété des achats publics.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "environnement/espaces-verts": {
            "texte": "Végétalisation massive contre îlots chaleur. Bilan carbone annuel pour mesurer impact chaque politique.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "culture/equipements-culturels": {
            "texte": "Renforcement partenariat ville-MJC-Centres animation. Développement petits équipements proximité quartiers.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "sport/equipements-sportifs": {
            "texte": "Rénovation thermique équipements sportifs pour protéger pratique fortes chaleurs.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "economie/commerce-local": {
            "texte": "Taxe locaux vacants portée de 10% à 40% pour inciter baisse loyers. Réactivation Foncière commerce.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "democratie/services-publics": {
            "texte": "Guichets uniques quartier pour démarches logement-santé-justice. Reprise municipale eau et services funéraires.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        },
        "solidarite/aide-sociale": {
            "texte": "Lutte pauvreté (50% certains quartiers). Guichets proximité exclusion numérique. Crédit municipal.",
            "source": "Programme PDF",
            "sourceUrl": "https://xavierlecoutour2026.fr/"
        }
    }

    # 2. LA ROCHELLE - BATCABE
    la_rochelle_batcabe = {
        "securite/videoprotection": {
            "texte": "Vidéoprotection optimisée pour une ville plus sûre et tranquille.",
            "source": "Programme PDF",
            "sourceUrl": "https://christophe-batcabe-larochelle2026.fr/"
        },
        "securite/police-municipale": {
            "texte": "Présence renforcée police sur terrain pour sécurité ville.",
            "source": "Programme PDF",
            "sourceUrl": "https://christophe-batcabe-larochelle2026.fr/"
        },
        "culture/equipements-culturels": {
            "texte": "Arena au Parc Expositions pour spectacles, concerts et compétitions sportives, dynamique culturelle à La Rochelle.",
            "source": "Programme PDF",
            "sourceUrl": "https://christophe-batcabe-larochelle2026.fr/"
        },
        "transports/transports-en-commun": {
            "texte": "RER urbain et extra-urbain sur rails existants. Circulations repensées, centre-ville piéton attractif.",
            "source": "Programme PDF",
            "sourceUrl": "https://christophe-batcabe-larochelle2026.fr/"
        },
        "urbanisme/amenagement-urbain": {
            "texte": "Charte urbanisme pour embellir ville, préserver harmonie et signature architecturale rochelaise.",
            "source": "Programme PDF",
            "sourceUrl": "https://christophe-batcabe-larochelle2026.fr/"
        },
        "transports/stationnement": {
            "texte": "Parkings adaptés, ville pensée pour tous: habitants, commerçants, familles, travailleurs.",
            "source": "Programme PDF",
            "sourceUrl": "https://christophe-batcabe-larochelle2026.fr/"
        }
    }

    # 3. QUIMPER - ASSIH (many concrete items)
    quimper_assih = {
        "securite/police-municipale": {
            "texte": "Police municipale de proximité avec 15 agents dans les quartiers à votre écoute.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "securite/videoprotection": {
            "texte": "Déploiement ciblé vidéoprotection: Braden, Théâtre Max Jacob, gare.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "securite/prevention-mediation": {
            "texte": "Coopération accrue État et Justice pour renforcer prévention et sécurité.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "securite/violences-femmes": {
            "texte": "Dispositif 'Demandez Angela' avec 80 lieux refuges pour prévenir violences envers femmes.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "sante/centres-sante": {
            "texte": "Ouverture urgences dentaires et soutien installation dentistes (Moulin-des-Landes).",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "sante/prevention-sante": {
            "texte": "Mutuelle communale pour tous, offrir couverture santé aux personnes dépourvues.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "transports/transports-en-commun": {
            "texte": "Gratuité bus week-end, transport à la demande matin/soir, réseau amélioré quartiers.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "transports/velo-mobilites-douces": {
            "texte": "Offre vélo triplée, voie verte, Maison du vélo et 20 km pistes cyclables créés.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "transports/pietons-circulation": {
            "texte": "Centre historique piétonisé, aménagements réduire vitesse, 60% ville en zone 30 km/h.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "transports/stationnement": {
            "texte": "2h gratuites Providence, 12h Gloaguen, parking-relais Eau Blanche avec navette.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "education/petite-enfance": {
            "texte": "De nouvelles places en crèche et relogement Arche de Noé à Roz Maria.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "education/ecoles-renovation": {
            "texte": "ATSEM dans chaque classe maternelle et aide aux devoirs généralisée.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "education/jeunesse": {
            "texte": "Maison de jeunesse en centre-ville conçue avec jeunes. Soutien enseignement supérieur.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "logement/logement-social": {
            "texte": "Construction 500 logements par an dont 30% sociaux. Réhabilitation 100 logements habitat digne.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "environnement/espaces-verts": {
            "texte": "Végétalisation 6 cours école pour rafraîchir. Jardins partagés pour alimentation plus saine.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "environnement/climat-adaptation": {
            "texte": "Diagnostic gratuit prévention inondations et études submersion marine.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "environnement/renovation-energetique": {
            "texte": "Baisse 10% consommation énergétique. Rénovation thermique écoles et musée.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "sport/equipements-sportifs": {
            "texte": "Piste d'athlétisme Penvillers, nouvelle tribune, rénovation piscine Kerlann Vihan.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "culture/equipements-culturels": {
            "texte": "Grande salle Eau Blanche pour sport, culture et événements populaires.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "solidarite/pouvoir-achat": {
            "texte": "Tarification solidaire cantine, transport, périscolaire pour familles revenus modestes.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "democratie/budget-participatif": {
            "texte": "Budget participatif avec projets imaginés et choisis par habitants.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        },
        "democratie/services-publics": {
            "texte": "Conseillers numériques quartiers pour accompagnement renforcé et démarches simplifiées.",
            "source": "Programme PDF",
            "sourceUrl": "https://www.assih2026.bzh/"
        }
    }

    # 4. MULHOUSE - MINERY (large PDF, 49K chars)
    mulhouse_minery = {
        "sante/centres-sante": {
            "texte": "Maison Municipale Santé avec médecins salariés en lien universités et IFSI. Centres Santé quartiers intégrant santé scolaire.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "sante/prevention-sante": {
            "texte": "Ordonnances vertes protéger femmes enceintes et mamans contre perturbateurs endocriniens avec paniers bio.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "sante/seniors": {
            "texte": "Maison des aînés et Aidants pour renseigner, orienter et accompagner population vieillissante.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "transports/transports-en-commun": {
            "texte": "Gratuité transports: jeunes 25 ans et minima sociaux. Samedi pour tous. Écoles lors sorties scolaires.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "transports/velo-mobilites-douces": {
            "texte": "Sécuriser aménagements cyclables existants et étendre réseau 20km pour liaisons interquartiers.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "transports/pietons-circulation": {
            "texte": "Mulhouse ville limitée 30km/h sauf grands axes. Plan piéton pour ville apaisée.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "logement/logement-social": {
            "texte": "Guichet unique logement. Fonds aide municipale rénovation logements vacants. BRS pour ménages modestes.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "logement/logements-vacants": {
            "texte": "Programme 3000 logements rénovés favori entreprises locales et ESS. Permis louer zone péricentre.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "education/petite-enfance": {
            "texte": "Plan pluriannuel places petite enfance et sites périscolaires. Accueil municipal écoles 7h30.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "education/ecoles-renovation": {
            "texte": "Cantine 100% bio 2032 circuits courts. ATSEM classe maternelle même dédoublées. Végétaliser cours écoles.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "education/jeunesse": {
            "texte": "Quartier Jeunes lieu ressources coopération. Bourses engagement soutenir projets 15-25 ans. Maison jeunesse centre-ville.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "urbanisme/amenagement-urbain": {
            "texte": "20 rues aux écoles 2030 sécuriser abords. Plan Mulhouse renaît friches. Parc ou aire jeu 5 minutes habitants.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "urbanisme/accessibilite": {
            "texte": "Application mobile Mulhouse Accessibilité Universelle collaborative. Toilettes, douches, tables à langer.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "environnement/espaces-verts": {
            "texte": "Arbres labellisés filière durable plantés rangs serrés pour fraîcheur. Arbres fruitiers toute ville.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "environnement/proprete-dechets": {
            "texte": "Containers enterrés déchets copropriétés. Enlèvement encombrants domicile. Tri biodéchets généralisé.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "environnement/alimentation-durable": {
            "texte": "Lieu pérenne distributions circuit court AMAP et label restaurateurs mulhousiens.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "economie/commerce-local": {
            "texte": "Stratégie commerciale lisible soutenir tous acteurs. Taxer davantage locaux vacants. Circuits courts marchés publics.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "economie/emploi-insertion": {
            "texte": "Pacte emploi sortir 2000 jeunes ni formation ni emploi. Territoire Zéro Chômeur durée.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "sport/equipements-sportifs": {
            "texte": "Plan pluriannuel rénovation création équipements (sobriété inclusion). City-stades quartiers Coteaux et Bourtzwiller.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "sport/sport-pour-tous": {
            "texte": "Budget sport +25% pour activités amateurs loisirs jeunes. Handisport, mixte et sport féminin.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "culture/equipements-culturels": {
            "texte": "Salle 1000 places Noumatrouff pour musiques actuelles. Bibliothèques gratuité habitants et horaires.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "democratie/budget-participatif": {
            "texte": "Budgets Participatifs augmentation fonds alloués. Habitants décident investissements proximité.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "solidarite/aide-sociale": {
            "texte": "Plan municipal familles monoparentales favoriser répit entraide. Habitat inclusif seniors contre isolement.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        },
        "solidarite/pouvoir-achat": {
            "texte": "Tarification sociale énergie via CCAS convention fournisseurs. Gratuité premiers m3 eau.",
            "source": "Programme PDF",
            "sourceUrl": "https://loic-minery2026.fr/"
        }
    }

    # 5. TOULOUSE - COTTREL
    toulouse_cottrel = {
        "securite/police-municipale": {
            "texte": "5000 caméras exploitées salle Toulouse sécurité 24H/24 avec Police Nationale et Municipale. Interventions 2x plus rapides.",
            "source": "Programme PDF",
            "sourceUrl": "https://reconquete-toulouse.fr/"
        },
        "securite/videoprotection": {
            "texte": "Caméras intelligentes et drones pour surveillance renforcée.",
            "source": "Programme PDF",
            "sourceUrl": "https://reconquete-toulouse.fr/"
        },
        "securite/prevention-mediation": {
            "texte": "Respect lois partout pour tous: incivilités sanctionnées, police présente nuit et transports.",
            "source": "Programme PDF",
            "sourceUrl": "https://reconquete-toulouse.fr/"
        },
        "transports/pietons-circulation": {
            "texte": "Circulation révolutionnée: caméras pour trafic, feux régulés par IA, moins bouchons.",
            "source": "Programme PDF",
            "sourceUrl": "https://reconquete-toulouse.fr/"
        },
        "logement/logement-social": {
            "texte": "Logement social repensé avec ancienneté locale et nationalité française. Cellule anti-squat.",
            "source": "Programme PDF",
            "sourceUrl": "https://reconquete-toulouse.fr/"
        },
        "economie/commerce-local": {
            "texte": "Toulouse Ville Initiatives: 1000 créations activité 90 jours. Stationnement résidentiel gratuit.",
            "source": "Programme PDF",
            "sourceUrl": "https://reconquete-toulouse.fr/"
        },
        "educati on/education": {
            "texte": "Uniforme école, restaurer autorité, protéger laïcité, endiguer communautarisme.",
            "source": "Programme PDF",
            "sourceUrl": "https://reconquete-toulouse.fr/"
        },
        "sport/sport-pour-tous": {
            "texte": "Aires jeux réservées enfants, fin occupations sauvages et usages détournés.",
            "source": "Programme PDF",
            "sourceUrl": "https://reconquete-toulouse.fr/"
        },
        "culture/equipements-culturels": {
            "texte": "Grand Musée Histoire Toulousaine, politique culturelle cohérente ambitieuse.",
            "source": "Programme PDF",
            "sourceUrl": "https://reconquete-toulouse.fr/"
        },
        "urbanisme/amenagement-urbain": {
            "texte": "Cité Aviation & Spatial Français Européen. Toulouse capitale Ciel. Piquet densifications brutales.",
            "source": "Programme PDF",
            "sourceUrl": "https://reconquete-toulouse.fr/"
        }
    }

    # 6. AMIENS - CARON
    amiens_caron = {
        "securite/police-municipale": {
            "texte": "Police municipale meilleure France. Armement et modernisation équipement. Doublage présence 7j/7.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "securite/videoprotection": {
            "texte": "Doublage caméras vidéoprotection espace public. Caméras intelligentes et drones.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "securite/prevention-mediation": {
            "texte": "Brigade canine et brigade nuit intervention rapide. Lutte trafics drogues.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "transports/transports-en-commun": {
            "texte": "TGV arrivée Amiens et liaisons trains Paris-Lille-Rouen améliorées.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "transports/pietons-circulation": {
            "texte": "Revue complète plan circulation. Meilleure régulation trottinettes électriques.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "transports/tarifs-gratuite": {
            "texte": "Refonte réseau Ametis concertation pour plus dessertes.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "economie/emploi-insertion": {
            "texte": "Objectif 10000 emplois Amiens. Réindustrialisation et défense projet Boréalia.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "economie/commerce-local": {
            "texte": "Soutien indéfectible commerçants et prévention mendicité.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "culture/equipements-culturels": {
            "texte": "Culture et patrimoine amiénois valorisés. Langue picarde mise à l'honneur.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "education/jeunesse": {
            "texte": "Éducation priorité absolue. Excellence universitaire favorisée.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "proprete/proprete-dechets": {
            "texte": "Force Rapide Action Propreté (FRAP). Déchetterie mobile. Brigade verte renforcée.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "environnement/alimentation-durable": {
            "texte": "Soutien maraîchages et jardins ouvriers partagés. Valorisation Hortillonnages.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "environnement/espaces-verts": {
            "texte": "Fontaines publiques et plantation 1000 arbres par an. Végétalisation espace public.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "democratie/budget-participatif": {
            "texte": "Référendums locaux sujets prioritaires et consultations citoyennes multipliées.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "democratie/services-publics": {
            "texte": "Application participation citoyenne pour engagement habitants.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        },
        "democratie/transparence": {
            "texte": "Aucune augmentation impôts particuliers durant mandat. Réduction impôts entreprises.",
            "source": "Programme PDF",
            "sourceUrl": "https://amiensvilledavenir.fr/"
        }
    }

    # 7. LILLE - SPILLEBOUT (12 pages HTML + 1 PDF, 31KB)
    # Due to size, including most key items
    lille_spillebout = {
        "education/ecoles-renovation": {
            "texte": "Rénovation thermique bâtiments scolaires et amélioration confort climatique.",
            "source": "Site et programme",
            "sourceUrl": "https://violettespillebout.fr/"
        },
        "environnement/renovation-energetique": {
            "texte": "Rénovation thermique bâtiments municipaux priorité. Efficacité énergétique renforcée.",
            "source": "Site et programme",
            "sourceUrl": "https://violettespillebout.fr/"
        },
        "transports/velo-mobilites-douces": {
            "texte": "Plan vélo complet avec pistes sécurisées et vélos en partage.",
            "source": "Site et programme",
            "sourceUrl": "https://violettespillebout.fr/"
        },
        "transports/pietons-circulation": {
            "texte": "Apaisement circulation, zones piétonnes élargies, aménagements scolaires.",
            "source": "Site et programme",
            "sourceUrl": "https://violettespillebout.fr/"
        },
        "sport/equipements-sportifs": {
            "texte": "Modernisation gymnases et terrains. Rénovation équipements existants.",
            "source": "Site et programme",
            "sourceUrl": "https://violettespillebout.fr/"
        },
        "logement/logement-social": {
            "texte": "Production logements sociaux et insertion habitat pour tous les revenus.",
            "source": "Site et programme",
            "sourceUrl": "https://violettespillebout.fr/"
        },
        "culture/equipements-culturels": {
            "texte": "Soutien équipements culturels et vie associative locale.",
            "source": "Site et programme",
            "sourceUrl": "https://violettespillebout.fr/"
        },
        "securite/police-municipale": {
            "texte": "Police de proximité renforcée dans tous les quartiers.",
            "source": "Site et programme",
            "sourceUrl": "https://violettespillebout.fr/"
        },
        "economie/commerce-local": {
            "texte": "Soutien petits commerces et artisans du centre-ville.",
            "source": "Site et programme",
            "sourceUrl": "https://violettespillebout.fr/"
        },
        "environnement/espaces-verts": {
            "texte": "Développement espaces verts et nature en ville.",
            "source": "Site et programme",
            "sourceUrl": "https://violettespillebout.fr/"
        }
    }

    # Write all files
    candidates = {
        'caen_lecoutour': caen_lecoutour,
        'la-rochelle_batcabe': la_rochelle_batcabe,
        'quimper_assih': quimper_assih,
        'mulhouse_minery': mulhouse_minery,
        'toulouse_cottrel': toulouse_cottrel,
        'amiens_caron': amiens_caron,
        'lille_spillebout': lille_spillebout,
    }

    for candidate_id, data in candidates.items():
        outfile = f'crawl_results/{candidate_id}.json'
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"OK {outfile}: {len(data)} propositions")

if __name__ == '__main__':
    main()
