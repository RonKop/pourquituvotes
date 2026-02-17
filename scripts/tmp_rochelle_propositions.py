#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extraction des propositions pour La Rochelle 2026 - Presse locale
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELECTIONS_DIR = os.path.join(BASE_DIR, "data", "elections")

# Propositions par candidat (clés: categorie/sous-theme)
propositions = {
    "guiraud": {
        "urbanisme/amenagement-urbain": {
            "texte": "Créer un pack d'aménagements, d'équipements et de services commun à tous les quartiers avec city stades, barbecues et toilettes publiques.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://inf-info.fr/municipales-2026-a-la-rochelle-une-impression-de-premier-meeting-maire-depuis-7-mois-thibaut-guiraud-se-lance-dans-la-campagne/"
        },
        "environnement/climat-adaptation": {
            "texte": "Poursuivre le projet La Rochelle Territoire Zéro Carbone en superposant toutes les questions de santé.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://inf-info.fr/municipales-2026-a-la-rochelle-une-impression-de-premier-meeting-maire-depuis-7-mois-thibaut-guiraud-se-lance-dans-la-campagne/"
        },
        "securite/police-municipale": {
            "texte": "Augmenter la sécurité par l'éducation, la prévention et la répression. Recruter des policiers municipaux supplémentaires.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://inf-info.fr/municipales-2026-a-la-rochelle-une-impression-de-premier-meeting-maire-depuis-7-mois-thibaut-guiraud-se-lance-dans-la-campagne/"
        },
        "urbanisme/accessibilite": {
            "texte": "Généraliser l'accès à des terrains multisports et des aires de jeux pour enfants dans tous les quartiers.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://france3-regions.franceinfo.fr/nouvelle-aquitaine/charente-maritime/la-rochelle/municipales-le-maire-de-la-rochelle-thibaut-guiraud-est-candidat-a-sa-propre-succession-3280451.html"
        }
    },
    "simone": {
        "logement/logement-social": {
            "texte": "Augmenter le logement social et mieux encadrer les meublés de tourisme pour résoudre la crise du logement avec 12 000 demandes en attente.",
            "source": "Presse locale (France Bleu La Rochelle)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/elections-municipales-2026-un-ticket-simone-soubeste-pour-incarner-l-union-de-la-gauche-a-la-rochelle-1853779"
        },
        "democratie/budget-participatif": {
            "texte": "Mettre en place un référendum d'initiatives locales pour renforcer la démocratie locale.",
            "source": "Presse locale (France Bleu La Rochelle)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/elections-municipales-2026-un-ticket-simone-soubeste-pour-incarner-l-union-de-la-gauche-a-la-rochelle-1853779"
        },
        "sante/centres-sante": {
            "texte": "Créer un pôle dédié à la parentalité pour soutenir les familles monoparentales dans une 'ville de solidarité'.",
            "source": "Presse locale (France Bleu La Rochelle)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/elections-municipales-2026-un-ticket-simone-soubeste-pour-incarner-l-union-de-la-gauche-a-la-rochelle-1853779"
        },
        "culture/equipements-culturels": {
            "texte": "Établir un pass culture rochelais pour les jeunes de moins de 26 ans pour favoriser l'accès à la culture.",
            "source": "Presse locale (France Bleu La Rochelle)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/elections-municipales-2026-un-ticket-simone-soubeste-pour-incarner-l-union-de-la-gauche-a-la-rochelle-1853779"
        },
        "democratie/services-publics": {
            "texte": "Rénover les centres sociaux et renforcer les services publics de proximité.",
            "source": "Presse locale (France Bleu La Rochelle)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/elections-municipales-2026-un-ticket-simone-soubeste-pour-incarner-l-union-de-la-gauche-a-la-rochelle-1853779"
        }
    },
    "falorni": {
        "sante/centres-sante": {
            "texte": "Créer un centre de santé pour les quartiers ouest de la ville pour faciliter l'accès aux soins.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://inf-info.fr/municipales-2026-a-la-rochelle-hopital-de-la-rochelle-securite-logement-olivier-falorni-devoile-les-grandes-lignes-de-son-projet/"
        },
        "sante/prevention-sante": {
            "texte": "Moderniser l'hôpital de La Rochelle avec lancement du projet dans les 2 ans suivant l'élection et pose de la première pierre.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://inf-info.fr/municipales-2026-a-la-rochelle-hopital-de-la-rochelle-securite-logement-olivier-falorni-devoile-les-grandes-lignes-de-son-projet/"
        },
        "securite/police-municipale": {
            "texte": "Augmenter les effectifs de la police municipale de 20% pour plus de sécurité.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://inf-info.fr/municipales-2026-a-la-rochelle-hopital-de-la-rochelle-securite-logement-olivier-falorni-devoile-les-grandes-lignes-de-son-projet/"
        },
        "securite/videoprotection": {
            "texte": "Doubler les systèmes de vidéosurveillance pour améliorer la sécurité en ville.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://inf-info.fr/municipales-2026-a-la-rochelle-hopital-de-la-rochelle-securite-logement-olivier-falorni-devoile-les-grandes-lignes-de-son-projet/"
        },
        "logement/logement-social": {
            "texte": "Développer un parc de logements abordables avec un encadrement des loyers sur le modèle du Pays Basque.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://inf-info.fr/municipales-2026-a-la-rochelle-hopital-de-la-rochelle-securite-logement-olivier-falorni-devoile-les-grandes-lignes-de-son-projet/"
        },
        "logement/logements-vacants": {
            "texte": "Créer un bonus de conversion pour encourager les propriétaires de locations touristiques à convertir en baux annuels.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://inf-info.fr/municipales-2026-a-la-rochelle-hopital-de-la-rochelle-securite-logement-olivier-falorni-devoile-les-grandes-lignes-de-son-projet/"
        }
    },
    "salaun": {
        "democratie/budget-participatif": {
            "texte": "Mettre en place un référendum d'initiatives locales obligatoire si 10% des habitants participent.",
            "source": "Presse locale (France Bleu La Rochelle)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-2026-la-france-insoumise-investit-mathilde-louvain-pour-remporter-avignon-8544729"
        },
        "democratie/services-publics": {
            "texte": "Mettre en place un budget participatif municipal pour augmenter le pouvoir décisionnel des Rochelais.",
            "source": "Presse locale (LFI La Rochelle)",
            "sourceUrl": "https://louvain2026.fr/"
        },
        "transports/transports-en-commun": {
            "texte": "Instaurer la gratuité des transports publics pour faciliter la mobilité des habitants.",
            "source": "Presse locale (LFI La Rochelle)",
            "sourceUrl": "https://louvain2026.fr/"
        },
        "education/cantines-fournitures": {
            "texte": "Rendre la cantine scolaire gratuite et biologique pour tous les enfants.",
            "source": "Presse locale (LFI La Rochelle)",
            "sourceUrl": "https://louvain2026.fr/"
        },
        "environnement/climat-adaptation": {
            "texte": "Renforcer les politiques écologiques pour une transition durable.",
            "source": "Presse locale (LFI La Rochelle)",
            "sourceUrl": "https://louvain2026.fr/"
        }
    },
    "marbouh": {
        "solidarite/pouvoir-achat": {
            "texte": "Défendre le pouvoir d'achat des Rochelais face aux difficultés économiques avec une liste citoyenne 'Ensemble pour La Rochelle'.",
            "source": "Presse locale (France Bleu La Rochelle)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/municipales-2026-qui-sont-les-candidats-declares-a-la-rochelle-8235732"
        }
    },
    "werbrouck": {
        "urbanisme/amenagement-urbain": {
            "texte": "Dénonce l'abandon scandaleux du pont de Tasdon et demande une comparaison entre rénovation et reconstruction avec décision immédiate.",
            "source": "Presse locale (INF la Rochelle)",
            "sourceUrl": "https://inf-info.fr/municipales-a-la-rochelle-ce-que-pensent-les-candidats-sur-lavenir-du-pont-de-tasdon/"
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
        print(f'  python scripts/inserer_propositions.py --ville la-rochelle --candidat {candidat_id} --file scripts/tmp_{candidat_id}_props.json')
