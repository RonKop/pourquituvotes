#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extraction des propositions pour Ajaccio 2026 - Presse locale
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELECTIONS_DIR = os.path.join(BASE_DIR, "data", "elections")

propositions = {
    "sbraggia": {
        "urbanisme/amenagement-urbain": {
            "texte": "Créer deux nouveaux éco-quartiers à Finosello et Miséricorde avec équipements modernes et respect de l'environnement.",
            "source": "Presse locale (France 3 Corse)",
            "sourceUrl": "https://france3-regions.franceinfo.fr/corse/corse-du-sud/ajaccio/je-vais-defendre-un-bilan-dont-je-suis-tres-fier-stephane-sbraggia-se-lance-dans-la-campagne-des-municipales-a-ajaccio-3279686.html"
        },
        "urbanisme/accessibilite": {
            "texte": "Rénover le quartier de la citadelle et créer des équipements publics incluant un centre sportif et une médiathèque à Miséricorde.",
            "source": "Presse locale (Corse Net Infos)",
            "sourceUrl": "https://www.corsenetinfos.corsica/Municipales-Stephane-Sbraggia-fier-du-travail-accompli-trace-sa-vision-de-l-Ajaccio-de-demain_a88927.html"
        },
        "education/ecoles-renovation": {
            "texte": "Créer un nouveau groupe scolaire à Mezzavia dans une zone en mutation près d'un collège.",
            "source": "Presse locale (Corse Net Infos)",
            "sourceUrl": "https://www.corsenetinfos.corsica/Municipales-Stephane-Sbraggia-fier-du-travail-accompli-trace-sa-vision-de-l-Ajaccio-de-demain_a88927.html"
        },
        "environnement/espaces-verts": {
            "texte": "Créer un parc du patrimoine à Milelli, un quartier manquant d'espaces verts et d'équipements.",
            "source": "Presse locale (Corse Net Infos)",
            "sourceUrl": "https://www.corsenetinfos.corsica/Municipales-Stephane-Sbraggia-fier-du-travail-accompli-trace-sa-vision-de-l-Ajaccio-de-demain_a88927.html"
        },
        "environnement/renovation-energetique": {
            "texte": "Poursuivre la transition énergétique et la rénovation des anciens logements dans le cadre du projet Ajaccio 2030.",
            "source": "Presse locale (France 3 Corse)",
            "sourceUrl": "https://france3-regions.franceinfo.fr/corse/corse-du-sud/ajaccio/je-vais-defendre-un-bilan-dont-je-suis-tres-fier-stephane-sbraggia-se-lance-dans-la-campagne-des-municipales-a-ajaccio-3279686.html"
        },
        "transports/transports-en-commun": {
            "texte": "Améliorer la mobilité urbaine dans le cadre du développement durable du projet Ajaccio 2030.",
            "source": "Presse locale (France 3 Corse)",
            "sourceUrl": "https://france3-regions.franceinfo.fr/corse/corse-du-sud/ajaccio/je-vais-defendre-un-bilan-dont-je-suis-tres-fier-stephane-sbraggia-se-lance-dans-la-campagne-des-municipales-a-ajaccio-3279686.html"
        }
    },
    "filoni": {
        "securite/police-municipale": {
            "texte": "Doubler l'effectif de la police municipale pour apporter 'calme et sécurité' aux quartiers d'Ajaccio.",
            "source": "Presse locale (France 3 Corse)",
            "sourceUrl": "https://france3-regions.franceinfo.fr/corse/corse-du-sud/ajaccio/municipales-a-ajaccio-il-faut-etre-au-chevet-des-ajacciens-selon-francois-filoni-candidat-rassemblement-national-3296106.html"
        },
        "transports/stationnement": {
            "texte": "Construire trois parkings gratuits en centre-ville et éliminer les parcmètres pour arrêter 'l'extorsion' des Ajacciens.",
            "source": "Presse locale (France 3 Corse)",
            "sourceUrl": "https://france3-regions.franceinfo.fr/corse/corse-du-sud/ajaccio/municipales-2026-francois-filoni-officialise-sa-candidature-aux-elections-municipales-2223659.html"
        },
        "securite/videoprotection": {
            "texte": "Installer des systèmes de vidéosurveillance renforcés dans les zones sombres pour lutter contre le trafic de drogue.",
            "source": "Presse locale (Corse Net Infos)",
            "sourceUrl": "https://www.corsenetinfos.corsica/Municipales-Pour-Francois-Filoni-RN--Ajaccio-doit-redevenir-une-ville-propre-et-securisee_a88906.html"
        },
        "transports/transports-en-commun": {
            "texte": "Restaurer les droits des conducteurs de bus et améliorer les routes de transport public.",
            "source": "Presse locale (Corse Net Infos)",
            "sourceUrl": "https://www.corsenetinfos.corsica/Municipales-Pour-Francois-Filoni-RN--Ajaccio-doit-redevenir-une-ville-propre-et-securisee_a88906.html"
        },
        "urbanisme/amenagement-urbain": {
            "texte": "Restaurer le rond-point sur le boulevard périphérique et créer des routes de contournement vers Vazzio et Croix d'Alexandre.",
            "source": "Presse locale (Corse Net Infos)",
            "sourceUrl": "https://www.corsenetinfos.corsica/Municipales-Pour-Francois-Filoni-RN--Ajaccio-doit-redevenir-une-ville-propre-et-securisee_a88906.html"
        },
        "environnement/proprete-dechets": {
            "texte": "Faire d'Ajaccio 'une ville propre et sécurisée' en augmentant les moyens de nettoyage urbain.",
            "source": "Presse locale (Corse Net Infos)",
            "sourceUrl": "https://www.corsenetinfos.corsica/Municipales-Pour-Francois-Filoni-RN--Ajaccio-doit-redevenir-une-ville-propre-et-securisee_a88906.html"
        }
    },
    "zagnoli": {
        "education/petite-enfance": {
            "texte": "Réduire les inégalités chez les enfants par le développement d'équipements de garde d'enfants et la généralisation de petits-déjeuners gratuits à l'école.",
            "source": "Presse locale (France Bleu Corse)",
            "sourceUrl": "https://www.francebleu.fr/corse/municipales-a-ajaccio-pascal-zagnoli-benjamin-des-candidats-et-visage-d-un-nationalisme-de-terrain-3752917"
        },
        "education/cantines-fournitures": {
            "texte": "Généraliser les petits-déjeuners gratuits à l'école pour tous les élèves.",
            "source": "Presse locale (France Bleu Corse)",
            "sourceUrl": "https://www.francebleu.fr/corse/municipales-a-ajaccio-pascal-zagnoli-benjamin-des-candidats-et-visage-d-un-nationalisme-de-terrain-3752917"
        },
        "education/periscolaire-loisirs": {
            "texte": "Mettre en place une garde périscolaire gratuite pour les familles les plus précaires.",
            "source": "Presse locale (France Bleu Corse)",
            "sourceUrl": "https://www.francebleu.fr/corse/municipales-a-ajaccio-pascal-zagnoli-benjamin-des-candidats-et-visage-d-un-nationalisme-de-terrain-3752917"
        },
        "education/jeunesse": {
            "texte": "Créer un conseil municipal des jeunes pour impliquer la jeunesse dans les décisions municipales.",
            "source": "Presse locale (France Bleu Corse)",
            "sourceUrl": "https://www.francebleu.fr/corse/municipales-a-ajaccio-pascal-zagnoli-benjamin-des-candidats-et-visage-d-un-nationalisme-de-terrain-3752917"
        },
        "transports/transports-en-commun": {
            "texte": "Repenser les transports avec gestion intelligente du trafic, renforcer l'offre de transports publics et créer des pôles d'échanges aux entrées de ville.",
            "source": "Presse locale (Corsica Infurmazione)",
            "sourceUrl": "https://www.corsicainfurmazione.org/2024035/municipales-2026-repenser-les-transports-pour-simplifier-la-vie-des-ajacciens/2026/"
        },
        "economie/commerce-local": {
            "texte": "Revitaliser le commerce de centre-ville et réguler les locations Airbnb pour protéger le parc de logements.",
            "source": "Presse locale (Corsica Infurmazione)",
            "sourceUrl": "https://www.corsicainfurmazione.org/2023708/municipales-a-ajaccio-stintu-aiaccinu-entre-en-campagne-avec-une-liste-independante-et-un-projet-de-rupture-pour-la-ville/2026/"
        },
        "solidarite/aide-sociale": {
            "texte": "Installer des équipements d'hygiène dans l'espace public et renforcer le soutien logistique aux associations.",
            "source": "Presse locale (Corsica Infurmazione)",
            "sourceUrl": "https://www.corsicainfurmazione.org/2024047/municipale-daiacciu-la-ville-du-lien-et-de-la-justice-sociale/2026/"
        }
    },
    "carrolaggi": {
        "urbanisme/amenagement-urbain": {
            "texte": "Interdire les résidences secondaires dans les nouveaux projets à Miséricorde et à la Citadelle pour préserver le logement pour les résidents.",
            "source": "Presse locale (Corsica Infurmazione)",
            "sourceUrl": "https://www.corsicainfurmazione.org/2023571/aiacciu-a-la-croisee-des-chemins-lheure-du-choix-democratique/2026/"
        },
        "logement/acces-logement": {
            "texte": "Garantir le logement pour les résidents et éviter la privatisation de la citadelle.",
            "source": "Presse locale (Corsica Infurmazione)",
            "sourceUrl": "https://www.corsicainfurmazione.org/2023571/aiacciu-a-la-croisee-des-chemins-lheure-du-choix-democratique/2026/"
        },
        "securite/police-municipale": {
            "texte": "Créer une station de police municipale à Les Cannes pour renforcer la sécurité de ce quartier.",
            "source": "Presse locale (Corsica Infurmazione)",
            "sourceUrl": "https://www.corsicainfurmazione.org/2023571/aiacciu-a-la-croisee-des-chemins-lheure-du-choix-democratique/2026/"
        },
        "urbanisme/amenagement-urbain": {
            "texte": "Démanteler le téléphérique décrit comme un 'gouffre financier' et un projet coûteux et inutile.",
            "source": "Presse locale (Corsica Infurmazione)",
            "sourceUrl": "https://www.corsicainfurmazione.org/2023571/aiacciu-a-la-croisee-des-chemins-lheure-du-choix-democratique/2026/"
        },
        "solidarite/egalite-discriminations": {
            "texte": "Combattre les dérives mafieuses et établir une gouvernance éthique contre la corruption.",
            "source": "Presse locale (Corsica Infurmazione)",
            "sourceUrl": "https://www.corsicainfurmazione.org/2023571/aiacciu-a-la-croisee-des-chemins-lheure-du-choix-democratique/2026/"
        }
    },
    "cesari": {
        "logement/logement-social": {
            "texte": "Développer les logements sociaux et intermédiaires pour résoudre la crise du logement à Ajaccio.",
            "source": "Presse locale (France 3 Corse)",
            "sourceUrl": "https://france3-regions.franceinfo.fr/corse/corse-du-sud/ajaccio/municipales-a-ajaccio-charlotte-cesari-designee-tete-de-liste-pour-une-union-de-la-gauche-3283721.html"
        },
        "logement/acces-logement": {
            "texte": "Mettre le logement au cœur des décisions municipales pour améliorer l'accès pour tous les Ajacciens.",
            "source": "Presse locale (France 3 Corse)",
            "sourceUrl": "https://france3-regions.franceinfo.fr/corse/corse-du-sud/ajaccio/municipales-a-ajaccio-charlotte-cesari-designee-tete-de-liste-pour-une-union-de-la-gauche-3283721.html"
        },
        "culture/equipements-culturels": {
            "texte": "Développer des centres culturels dans les différents quartiers pour favoriser l'accès à la culture.",
            "source": "Presse locale (Alta Frequenza)",
            "sourceUrl": "https://www.alta-frequenza.corsica/actu/charlotte_cesari_candidate_pour_les_forces_de_gauche_a_ajaccio_entend_changer_de_modele_et_de_gouvernance_127229"
        },
        "environnement/espaces-verts": {
            "texte": "Créer des 'jardins du savoir' pour préserver le patrimoine local et l'identité d'Ajaccio.",
            "source": "Presse locale (Alta Frequenza)",
            "sourceUrl": "https://www.alta-frequenza.corsica/actu/charlotte_cesari_candidate_pour_les_forces_de_gauche_a_ajaccio_entend_changer_de_modele_et_de_gouvernance_127229"
        },
        "democratie/services-publics": {
            "texte": "Réintégrer la question sociale au cœur du conseil municipal avec un programme co-construit avec les Ajacciens.",
            "source": "Presse locale (France 3 Corse)",
            "sourceUrl": "https://france3-regions.franceinfo.fr/corse/corse-du-sud/ajaccio/ce-qui-nous-rassemble-est-plus-fort-que-ce-qui-nous-separe-cinq-partis-de-gauche-s-unissent-pour-les-municipales-2026-a-ajaccio-3191880.html"
        },
        "environnement/climat-adaptation": {
            "texte": "Promouvoir la transition écologique et le développement durable du territoire.",
            "source": "Presse locale (France Bleu Corse)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-2026-la-gauche-ajaccienne-reunie-sur-le-social-et-l-ecologie-6251935"
        }
    },
    "foata": {
        "solidarite/pouvoir-achat": {
            "texte": "Présenter une liste sans étiquette pour défendre les intérêts des Ajacciens.",
            "source": "Presse locale (France 3 Corse)",
            "sourceUrl": "https://france3-regions.franceinfo.fr/corse/corse-du-sud/ajaccio/quels-sont-les-candidats-declares-aux-elections-municipales-a-ajaccio-3288885.html"
        }
    }
}

def write_propositions(candidat_id, props):
    """Écrit les propositions pour un candidat"""
    filename = os.path.join(BASE_DIR, "scripts", f"tmp_{candidat_id}_props.json")
    output = {"propositions": props}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Écrit: {filename}")

if __name__ == "__main__":
    for candidat_id, props in propositions.items():
        write_propositions(candidat_id, props)
    print("\nPropositions écrites. Exécuter:")
    for candidat_id in propositions.keys():
        print(f'  python scripts/inserer_propositions.py --ville ajaccio --candidat {candidat_id} --file scripts/tmp_{candidat_id}_props.json')
