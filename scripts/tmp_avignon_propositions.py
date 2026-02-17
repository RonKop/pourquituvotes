#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extraction des propositions pour Avignon 2026 - Presse locale
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELECTIONS_DIR = os.path.join(BASE_DIR, "data", "elections")

propositions = {
    "galzi": {
        "securite/police-municipale": {
            "texte": "Recruter 60 agents de police supplémentaires pour renforcer la présence policière dans la ville.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-securite-proprete-circulation-coeur-projet-olivier-galzi-359720/"
        },
        "securite/videoprotection": {
            "texte": "Installer 100 caméras supplémentaires dotées d'intelligence artificielle dans les rues d'Avignon.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-securite-proprete-circulation-coeur-projet-olivier-galzi-359720/"
        },
        "securite/prevention-mediation": {
            "texte": "Déployer une application mobile liée à un bouton de sécurité permettant d'alerter les forces de l'ordre en cas de danger.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-securite-proprete-circulation-coeur-projet-olivier-galzi-359720/"
        },
        "democratie/services-publics": {
            "texte": "Demander l'autorisation au préfet de fermer administrativement les lieux générant un trouble à l'ordre public.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-securite-proprete-circulation-coeur-projet-olivier-galzi-359720/"
        },
        "environnement/proprete-dechets": {
            "texte": "Créer un 'monsieur ou madame propreté' pour avoir un interlocuteur unique et être plus réactif.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-securite-proprete-circulation-coeur-projet-olivier-galzi-359720/"
        },
        "environnement/proprete-dechets": {
            "texte": "Renforcer la lutte contre les dépôts sauvages avec déploiement de caméras nomades.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-securite-proprete-circulation-coeur-projet-olivier-galzi-359720/"
        },
        "transports/pietons-circulation": {
            "texte": "Revoir le plan faubourgs en concertation avec les habitants pour améliorer la circulation.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-securite-proprete-circulation-coeur-projet-olivier-galzi-359720/"
        },
        "transports/transports-en-commun": {
            "texte": "Sortir la gare routière du centre-ville pour désengorger le trafic routier.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-securite-proprete-circulation-coeur-projet-olivier-galzi-359720/"
        },
        "urbanisme/amenagement-urbain": {
            "texte": "Reprendre le tracé initial de la liaison Est-Ouest (LEO) et mettre la pression pour obtenir les financements nécessaires.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-securite-proprete-circulation-coeur-projet-olivier-galzi-359720/"
        }
    },
    "rigault": {
        "transports/pietons-circulation": {
            "texte": "Supprimer tous les sens uniques en une semaine et éliminer le plan faubourgs en trois mois, avant le festival.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://fr.headtopics.com/news/municipales-2026-a-avignon-stop-a-l-autophobie-le-plan-79217119"
        },
        "transports/velo-mobilites-douces": {
            "texte": "Réinstaller les journées vélo annuels d'Avignon pour promouvoir la mobilité douce.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/emissions/l-info-d-ici-ici-vaucluse/municipales-2026-a-avignon-quelles-sont-les-propositions-des-candidats-sur-la-circulation-9474169"
        },
        "transports/velo-mobilites-douces": {
            "texte": "Désigner un responsable transport comme point de contact privilégié pour étudier les remarques des usagers et associations.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/emissions/l-info-d-ici-ici-vaucluse/municipales-2026-a-avignon-quelles-sont-les-propositions-des-candidats-sur-la-circulation-9474169"
        },
        "transports/pietons-circulation": {
            "texte": "Implémenter un système à sens unique autour des remparts en sens inverse des aiguilles d'une montre avec onde verte, coût 150 000 euros.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://fr.headtopics.com/news/municipales-2026-a-avignon-stop-a-l-autophobie-le-plan-79217119"
        },
        "securite/police-municipale": {
            "texte": "Doubler l'effectif de la police municipale avec présence 24/24 heures.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/emissions/l-info-d-ici-ici-vaucluse/municipales-2026-a-avignon-la-securite-n-est-pas-une-mesure-de-droite-9639434"
        },
        "securite/videoprotection": {
            "texte": "Redéployer la vidéosurveillance pour améliorer la sécurité urbaine.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/emissions/l-info-d-ici-ici-vaucluse/municipales-2026-a-avignon-la-securite-n-est-pas-une-mesure-de-droite-9639434"
        },
        "education/ecoles-renovation": {
            "texte": "Revenir à une semaine scolaire de quatre jours et demi contre les rythmes actuels.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/provence-alpes-cote-d-azur/vaucluse-84/avignon/elections-municipales-a-avignon-la-semaine-de-quatre-jours-et-demi-dans-les-ecoles-divise-les-candidats-4664953"
        }
    },
    "fournier": {
        "transports/transports-en-commun": {
            "texte": "Créer des parcs de stationnement relais gratuits et surveillés pour favoriser l'utilisation des transports en commun.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-david-fournier-choisi-par-les-militants-socialistes-pour-etre-le-candidat-du-parti-a-avignon/"
        },
        "transports/transports-en-commun": {
            "texte": "Développer les transports publics pour réduire la congestion routière.",
            "source": "Presse locale (Echo du Mardi)",
            "sourceUrl": "https://www.echodumardi.com/actualite/david-fournier-il-faut-liberer-le-potentiel-davignon/"
        },
        "securite/police-municipale": {
            "texte": "Augmenter les ressources pour le nettoyage urbain et la propreté des rues.",
            "source": "Presse locale (Echo du Mardi)",
            "sourceUrl": "https://www.echodumardi.com/actualite/david-fournier-il-faut-liberer-le-potentiel-davignon/"
        },
        "education/cantines-fournitures": {
            "texte": "Poursuivre la politique d'accès gratuit aux repas scolaires pour les familles les plus modestes.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-david-fournier-choisi-par-les-militants-socialistes-pour-etre-le-candidat-du-parti-a-avignon/"
        },
        "education/jeunesse": {
            "texte": "Priorité à la jeunesse, au logement social et à la sécurité dans le programme municipal.",
            "source": "Presse locale (Echo du Mardi)",
            "sourceUrl": "https://www.echodumardi.com/actualite/david-fournier-il-faut-liberer-le-potentiel-davignon/"
        },
        "urbanisme/amenament-urbain": {
            "texte": "Créer une liaison entre l'A7 et l'A9 au sud d'Orange pour améliorer la rocade routière.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/emissions/l-invite-d-ici-vaucluse/nous-travaillons-pour-rassembler-la-gauche-a-avignon-assure-david-fournier-candidat-socialiste-aux-municipales-5914157"
        }
    },
    "louvain": {
        "education/ecoles-renovation": {
            "texte": "Mettre en place un plan pluriannuel de rénovation des écoles d'Avignon comme investissement dans l'égalité et l'avenir.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-avignon-mathilde-louvain-devoile-programme-rupture-lfi-357552/"
        },
        "logement/logement-social": {
            "texte": "Créer des brigades contre les logements insalubres pour contrôler les locations saisonnières et encadrer les loyers.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/la-france-insoumise-devoile-son-programme-sur-la-securite-a-avignon-7928102"
        },
        "logement/encadrement-loyers": {
            "texte": "Mettre en place un plafonnement des loyers pour lutter contre la spéculation immobilière.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/la-france-insoumise-devoile-son-programme-sur-la-securite-a-avignon-7928102"
        },
        "securite/prevention-mediation": {
            "texte": "Développer une approche globale de la sécurité appelée 'tranquillité publique' plutôt que sécurité autoritaire.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/la-france-insoumise-devoile-son-programme-sur-la-securite-a-avignon-7928102"
        },
        "solidarite/egalite-discriminations": {
            "texte": "Créer un observatoire municipal contre les discriminations (antisémitisme, racisme, islamophobie, LGBTphobie) et le sexisme.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.lejournaltoulousain.fr/provence-alpes-cote-dazur/vaucluse/municipales-2026-avignon-mathilde-louvain-devoile-programme-rupture-lfi-357552/"
        },
        "democratie/transparence": {
            "texte": "Instaurer une démocratie locale basée sur la participation des citoyens et leur contrôle des élus.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/infos/politique/la-france-insoumise-lance-sa-campagne-a-avignon-et-devoile-ses-premieres-mesures-7533861"
        }
    },
    "fiori": {
        "securite/police-municipale": {
            "texte": "Mettre en place une police municipale actionnée 24/7 avec création d'une brigade canine avec 6 chiens et 6 conducteurs jour et nuit.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/emissions/l-info-d-ici-ici-vaucluse/municipales-2026-a-avignon-l-entrepreneur-stephan-fiori-presente-ses-52-colistiers-issus-de-la-societe-civile-8577396"
        },
        "sante/centres-sante": {
            "texte": "Créer une 'police municipale santé' pour assurer la sécurité de l'hôpital, des établissements privés qui le demandent et des pharmacies.",
            "source": "Presse locale (France Bleu Vaucluse)",
            "sourceUrl": "https://www.francebleu.fr/emissions/l-info-d-ici-ici-vaucluse/municipales-2026-a-avignon-l-entrepreneur-stephan-fiori-presente-ses-52-colistiers-issus-de-la-societe-civile-8577396"
        },
        "transports/pietons-circulation": {
            "texte": "Restaurer les axes principaux en circulation bidirectionnelle, sauf là où les travaux l'empêchent.",
            "source": "Presse locale (Infoavignon)",
            "sourceUrl": "https://www.infoavignon.com/le-programme-de-stephan-fiori-serieux-mais-paradoxal/"
        },
        "urbanisme/amenagement-urbain": {
            "texte": "Étudier la faisabilité d'enfouir le périphérique d'Avignon sur environ 2,5 kilomètres.",
            "source": "Presse locale (Infoavignon)",
            "sourceUrl": "https://www.infoavignon.com/les-ambitions-urbaines-de-stephan-fiori-sont-elles-realistes/"
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
        print(f'  python scripts/inserer_propositions.py --ville avignon --candidat {candidat_id} --file scripts/tmp_{candidat_id}_props.json')
