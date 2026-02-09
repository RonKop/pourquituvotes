#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G\u00e9n\u00e8re et ins\u00e8re Montpellier dans app.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generateur_commun import insert_city

print("=== MONTPELLIER ===")
insert_city(
    ville_id="montpellier",
    ville_nom="Montpellier",
    ville_cp="34000",
    candidats=[
        {"id": "delafosse", "nom": "Micha\u00ebl Delafosse", "liste": "PS (maire sortant)", "programmeUrl": "https://www.michaeldelafosse.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "altrad", "nom": "Mohed Altrad", "liste": "Divers droite", "programmeUrl": "https://altrad2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "jamet", "nom": "France Jamet", "liste": "RN-UDR", "programmeUrl": "https://francejamet.com/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "oziol", "nom": "Nathalie Oziol", "liste": "L'union de la gauche de rupture (LFI)", "programmeUrl": "https://www.nathalieoziol.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "roumegas", "nom": "Jean-Louis Roumegas", "liste": "Le Printemps montpelli\u00e9rain (EELV)", "programmeUrl": "https://printemps-montpellierain.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "perrein", "nom": "Isabelle Perrein", "liste": "Aimer Montpellier (LR-UDI-MoDem)", "programmeUrl": "https://www.isabelleperrein2026.fr/", "programmeComplet": False, "programmePdfPath": None},
        {"id": "gaillard", "nom": "R\u00e9mi Gaillard", "liste": "Sans \u00e9tiquette", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "tsagalos", "nom": "Thierry Tsagalos", "liste": "Ex-RN (sans investiture)", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
        {"id": "muller", "nom": "Max Muller", "liste": "R\u00e9volution permanente", "programmeUrl": "#", "programmeComplet": False, "programmePdfPath": None},
    ],
    props={
        # --- Delafosse (PS, maire sortant) ---
        ("securite", "police-municipale", "delafosse"): (
            "Recruter 100 agents de s\u00e9curit\u00e9 suppl\u00e9mentaires sous responsabilit\u00e9 municipale et m\u00e9tropolitaine, budget de 4 millions d'euros par an",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/montpelliermunicipales-2026-candidat-a-sa-reelection-le-socialiste-michael-delafosse-veut-poursuivre-sa-politique-securitaire"
        ),
        ("securite", "videoprotection", "delafosse"): (
            "Doubler le r\u00e9seau de cam\u00e9ras de vid\u00e9oprotection, de 500 \u00e0 1 000 cam\u00e9ras, budget de 3 millions d'euros sur le mandat",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/montpelliermunicipales-2026-candidat-a-sa-reelection-le-socialiste-michael-delafosse-veut-poursuivre-sa-politique-securitaire"
        ),
        ("securite", "prevention-mediation", "delafosse"): (
            "Passer de 12 \u00e0 30 m\u00e9diateurs de quartier pour la r\u00e9solution des conflits de voisinage",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/montpelliermunicipales-2026-candidat-a-sa-reelection-le-socialiste-michael-delafosse-veut-poursuivre-sa-politique-securitaire"
        ),
        ("transports", "transports-en-commun", "delafosse"): (
            "Maintenir la gratuit\u00e9 totale des transports en commun et faire sortir le tramway hors de la M\u00e9tropole d'ici la fin du mandat",
            "France 3 Occitanie, 2026",
            "https://france3-regions.franceinfo.fr/occitanie/herault/montpellier/tant-que-je-serai-maire-la-gratuite-des-transports-sera-defendue-ce-qu-il-faut-retenir-de-l-interview-de-michael-delafosse-candidat-a-sa-reelection-a-la-mairie-de-montpellier-3284739.html"
        ),
        ("sante", "centres-sante", "delafosse"): (
            "Installer une antenne du CHU dans le quartier de la Mosson et cr\u00e9er des centres de sant\u00e9 avec m\u00e9decins salari\u00e9s dans les quartiers prioritaires",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/occitanie/herault-34/montpellier/municipales-2026-a-montpellier-michael-delafosse-promet-des-mesures-pour-le-pouvoir-d-achat-et-les-seniors-4159680"
        ),
        ("sante", "prevention-sante", "delafosse"): (
            "D\u00e9velopper une strat\u00e9gie d'aller-vers pour lutter contre le non-recours aux soins, notamment en sant\u00e9 mentale",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/occitanie/herault-34/montpellier/municipales-2026-a-montpellier-michael-delafosse-promet-des-mesures-pour-le-pouvoir-d-achat-et-les-seniors-4159680"
        ),
        ("sante", "seniors", "delafosse"): (
            "Cr\u00e9er 400 \u00e0 500 places dans quatre r\u00e9sidences sociales seniors municipales et installer 1 000 bancs suppl\u00e9mentaires dans l'espace public",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/occitanie/herault-34/montpellier/municipales-2026-a-montpellier-michael-delafosse-promet-des-mesures-pour-le-pouvoir-d-achat-et-les-seniors-4159680"
        ),
        ("solidarite", "pouvoir-achat", "delafosse"): (
            "Cr\u00e9er un Office municipal du pouvoir d'achat fonctionnant comme centrale de n\u00e9gociation pour des achats group\u00e9s",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/gratuite-sante-solidarite-pour-la-bataille-des-urnes-michael-delafosse-ajuste-son-bouclier-social"
        ),
        ("culture", "equipements-culturels", "delafosse"): (
            "Rendre gratuit l'acc\u00e8s aux 15 m\u00e9diath\u00e8ques de Montpellier et de la M\u00e9tropole",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/occitanie/herault-34/montpellier/municipales-2026-a-montpellier-michael-delafosse-promet-des-mesures-pour-le-pouvoir-d-achat-et-les-seniors-4159680"
        ),
        ("urbanisme", "quartiers-prioritaires", "delafosse"): (
            "R\u00e9nover les quartiers Mosson et Montasinos, restructurer les espaces publics et installer 50 concierges dans le parc social",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/gratuite-sante-solidarite-pour-la-bataille-des-urnes-michael-delafosse-ajuste-son-bouclier-social"
        ),
        ("solidarite", "aide-sociale", "delafosse"): (
            "Maintenir la tarification sociale pour l'eau, les mus\u00e9es, piscines et cantines, et exclure les produits issus du Mercosur des cantines scolaires",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/gratuite-sante-solidarite-pour-la-bataille-des-urnes-michael-delafosse-ajuste-son-bouclier-social"
        ),
        # --- Altrad (Divers droite) ---
        ("securite", "police-municipale", "altrad"): (
            "Doubler les effectifs de la police municipale",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-premieres-propositions-du-candidat-mohed-altrad/"
        ),
        ("securite", "prevention-mediation", "altrad"): (
            "Instaurer un couvre-feu pour les mineurs de moins de 16 ans non accompagn\u00e9s \u00e0 partir de 22h",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-cette-ville-a-besoin-qu-on-la-releve-mohed-altrad-retente-sa-chance-a-montpellier-1699900"
        ),
        ("transports", "transports-en-commun", "altrad"): (
            "Maintenir la gratuit\u00e9 totale des transports en commun pour tous les r\u00e9sidents",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-premieres-propositions-du-candidat-mohed-altrad/"
        ),
        ("transports", "pietons-circulation", "altrad"): (
            "Mettre en place un plan anti-bouchons complet pour r\u00e9viser le plan de circulation",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-premieres-propositions-du-candidat-mohed-altrad/"
        ),
        ("logement", "logement-social", "altrad"): (
            "Doubler le parc de logements sociaux et permettre aux locataires en HLM depuis 15 ans d'acc\u00e9der \u00e0 la propri\u00e9t\u00e9",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-premieres-propositions-du-candidat-mohed-altrad/"
        ),
        ("education", "cantines-fournitures", "altrad"): (
            "Rendre gratuite la cantine scolaire pour tous les enfants de Montpellier sans conditions de ressources",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-premieres-propositions-du-candidat-mohed-altrad/"
        ),
        ("environnement", "proprete-dechets", "altrad"): (
            "Abandonner le projet de chaudi\u00e8re CSR et cr\u00e9er une brigade municipale de propret\u00e9 et de v\u00e9g\u00e9talisation",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-premieres-propositions-du-candidat-mohed-altrad/"
        ),
        ("economie", "emploi-insertion", "altrad"): (
            "Cr\u00e9er 30 000 emplois et 10 000 contrats d'apprentissage en 5 ans pour l'objectif z\u00e9ro ch\u00f4meur",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-premieres-propositions-du-candidat-mohed-altrad/"
        ),
        ("democratie", "transparence", "altrad"): (
            "Reverser int\u00e9gralement les indemnit\u00e9s de maire aux associations locales et z\u00e9ro hausse d'imp\u00f4ts locaux",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-cette-ville-a-besoin-qu-on-la-releve-mohed-altrad-retente-sa-chance-a-montpellier-1699900"
        ),
        ("democratie", "services-publics", "altrad"): (
            "Cr\u00e9er des centres de services municipaux dans chaque quartier",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-cette-ville-a-besoin-qu-on-la-releve-mohed-altrad-retente-sa-chance-a-montpellier-1699900"
        ),
        # --- Jamet (RN-UDR) ---
        ("securite", "police-municipale", "jamet"): (
            "Doubler les effectifs de la police municipale",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-l-eurodeputee-rn-france-jamet-annonce-sa-candidature-a-montpellier-3891487"
        ),
        ("securite", "videoprotection", "jamet"): (
            "Doubler le nombre de cam\u00e9ras de vid\u00e9oprotection dans la ville",
            "France 3 Occitanie, 2026",
            "https://france3-regions.franceinfo.fr/occitanie/herault/montpellier/montpellier-est-une-capitale-dechue-sclerosee-et-fermee-france-jamet-se-declare-candidate-aux-elections-municipales-pour-le-rn-et-l-udr-3283358.html"
        ),
        ("transports", "pietons-circulation", "jamet"): (
            "R\u00e9ouvrir le tunnel de la Com\u00e9die \u00e0 la circulation automobile et r\u00e9tablir l'intermodalit\u00e9 en centre-ville",
            "France 3 Occitanie, 2026",
            "https://france3-regions.franceinfo.fr/occitanie/herault/montpellier/montpellier-est-une-capitale-dechue-sclerosee-et-fermee-france-jamet-se-declare-candidate-aux-elections-municipales-pour-le-rn-et-l-udr-3283358.html"
        ),
        ("transports", "tarifs-gratuite", "jamet"): (
            "Maintenir la gratuit\u00e9 des transports en commun, mesure propos\u00e9e d\u00e8s 2014",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/emissions/l-info-d-ici-ici-herault/municipales-2026-montpellier-la-securite-theme-prioritaire-de-campagne-y-compris-a-gauche-8772577"
        ),
        ("environnement", "proprete-dechets", "jamet"): (
            "Faire de la salubrit\u00e9 et du ramassage des ordures une priorit\u00e9 municipale",
            "France 3 Occitanie, 2026",
            "https://france3-regions.franceinfo.fr/occitanie/herault/montpellier/montpellier-est-une-capitale-dechue-sclerosee-et-fermee-france-jamet-se-declare-candidate-aux-elections-municipales-pour-le-rn-et-l-udr-3283358.html"
        ),
        # --- Oziol (LFI) ---
        ("logement", "logements-vacants", "oziol"): (
            "Cr\u00e9er un guichet municipal du droit au logement pour recenser les 12 000 \u00e0 18 000 logements vacants et les mobiliser",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-sept-premieres-mesures-de-la-liste-de-linsoumise-nathalie-oziol/"
        ),
        ("logement", "encadrement-loyers", "oziol"): (
            "Mettre en place l'encadrement des loyers \u00e0 Montpellier",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-sept-premieres-mesures-de-la-liste-de-linsoumise-nathalie-oziol/"
        ),
        ("environnement", "alimentation-durable", "oziol"): (
            "Cr\u00e9er une fonci\u00e8re agricole municipale pour acqu\u00e9rir des terres et favoriser l'installation de nouveaux agriculteurs",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-sept-premieres-mesures-de-la-liste-de-linsoumise-nathalie-oziol/"
        ),
        ("environnement", "climat-adaptation", "oziol"): (
            "S'opposer aux m\u00e9gaprojets \u00e9cocides : Contournement Ouest de Montpellier, LIEN, et stopper le b\u00e9tonnage",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-montpellier-la-deputee-lfi-nathalie-oziol-menera-une-liste-d-union-de-la-gauche-de-rupture-7171992"
        ),
        ("education", "cantines-fournitures", "oziol"): (
            "Cr\u00e9er un restaurant municipal bio \u00e0 prix r\u00e9duit et ouvrir les cantines scolaires en dehors du temps scolaire",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-sept-premieres-mesures-de-la-liste-de-linsoumise-nathalie-oziol/"
        ),
        ("culture", "equipements-culturels", "oziol"): (
            "Transformer le MOCO en espace d\u00e9di\u00e9 aux cultures populaires et renforcer les Maisons pour tous comme lieux de vie culturelle",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-sept-premieres-mesures-de-la-liste-de-linsoumise-nathalie-oziol/"
        ),
        ("democratie", "budget-participatif", "oziol"): (
            "Instituer un r\u00e9f\u00e9rendum d'initiative citoyenne municipal et un r\u00e9f\u00e9rendum r\u00e9vocatoire",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-sept-premieres-mesures-de-la-liste-de-linsoumise-nathalie-oziol/"
        ),
        ("urbanisme", "accessibilite", "oziol"): (
            "Mettre en conformit\u00e9 tous les locaux municipaux et former les agents aux accueils accessibles (loi du 11 f\u00e9vrier 2005)",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-les-sept-premieres-mesures-de-la-liste-de-linsoumise-nathalie-oziol/"
        ),
        ("environnement", "proprete-dechets", "oziol"): (
            "Organiser une grande consultation publique sur la gestion des d\u00e9chets \u00e0 Montpellier",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/infos/politique/municipales-2026-a-montpellier-la-deputee-lfi-nathalie-oziol-menera-une-liste-d-union-de-la-gauche-de-rupture-7171992"
        ),
        # --- Roumegas (EELV) ---
        ("urbanisme", "amenagement-urbain", "roumegas"): (
            "Z\u00e9ro artificialisation nette : arr\u00eat des extensions urbaines sur les espaces naturels et agricoles",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-le-printemps-montpellierain-devoile-son-pacte-de-rupture-et-ses-12-mesures-phares"
        ),
        ("transports", "pietons-circulation", "roumegas"): (
            "R\u00e9ouvrir l'avenue Albert-Dubout et mettre en place des circulations en p\u00e9tales sur les quatre boulevards",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-le-printemps-montpellierain-devoile-son-pacte-de-rupture-et-ses-12-mesures-phares"
        ),
        ("transports", "velo-mobilites-douces", "roumegas"): (
            "Cr\u00e9er un sch\u00e9ma cyclable coh\u00e9rent avec un r\u00e9seau continu privil\u00e9giant la s\u00e9curit\u00e9",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-le-printemps-montpellierain-devoile-son-pacte-de-rupture-et-ses-12-mesures-phares"
        ),
        ("democratie", "budget-participatif", "roumegas"): (
            "\u00c9lire sept parlements de quartier dot\u00e9s d'un pouvoir d\u00e9cisionnel et instaurer un r\u00e9f\u00e9rendum d'initiative citoyenne municipal",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-le-printemps-montpellierain-devoile-son-pacte-de-rupture-et-ses-12-mesures-phares"
        ),
        ("solidarite", "pouvoir-achat", "roumegas"): (
            "Cr\u00e9er une dizaine d'\u00e9piceries municipales \u00e0 prix co\u00fbtant dans tous les quartiers",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-le-printemps-montpellierain-devoile-son-pacte-de-rupture-et-ses-12-mesures-phares"
        ),
        ("sante", "centres-sante", "roumegas"): (
            "D\u00e9ployer des maisons de sant\u00e9 dans les quartiers confront\u00e9s \u00e0 des d\u00e9serts m\u00e9dicaux",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-le-printemps-montpellierain-devoile-son-pacte-de-rupture-et-ses-12-mesures-phares"
        ),
        ("securite", "police-municipale", "roumegas"): (
            "Cr\u00e9er une police municipale de proximit\u00e9 avec des bureaux locaux et recruter 100 agents suppl\u00e9mentaires",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-le-printemps-montpellierain-devoile-son-pacte-de-rupture-et-ses-12-mesures-phares"
        ),
        ("education", "cantines-fournitures", "roumegas"): (
            "Rendre gratuites les cantines scolaires et l'accueil p\u00e9riscolaire de 7h \u00e0 19h",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-le-printemps-montpellierain-devoile-son-pacte-de-rupture-et-ses-12-mesures-phares"
        ),
        ("sante", "prevention-sante", "roumegas"): (
            "Mettre en place une ordonnance verte : paniers alimentaires bio pour les femmes enceintes issus de l'agriculture locale",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-le-printemps-montpellierain-devoile-son-pacte-de-rupture-et-ses-12-mesures-phares"
        ),
        ("education", "jeunesse", "roumegas"): (
            "Cr\u00e9er des centres de loisirs pour adolescents et un parcours citoyen incluant le financement gratuit du BAFA",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/ne-pas-investir-pour-les-jeunes-cest-creer-les-conditions-de-la-delinquance-le-printemps-montpellierain-devoile-son-pacte-pour-la-jeunesse"
        ),
        ("logement", "acces-logement", "roumegas"): (
            "Permettre \u00e0 4 000 locataires du parc social d'acc\u00e9der \u00e0 la propri\u00e9t\u00e9 sur un mandat",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-le-printemps-montpellierain-devoile-son-pacte-de-rupture-et-ses-12-mesures-phares"
        ),
        # --- Perrein (LR-UDI-MoDem) ---
        ("securite", "police-municipale", "perrein"): (
            "Doubler les effectifs de la police municipale et r\u00e9tablir une pr\u00e9sence polici\u00e8re nocturne (absente entre 4h30 et 8h)",
            "isabelleperrein2026.fr, 2026",
            "https://www.isabelleperrein2026.fr/notre-projet"
        ),
        ("securite", "videoprotection", "perrein"): (
            "Renforcer le Centre de Supervision Urbain avec plus d'\u00e9crans et de cam\u00e9ras fonctionnelles",
            "isabelleperrein2026.fr, 2026",
            "https://www.isabelleperrein2026.fr/notre-projet"
        ),
        ("transports", "pietons-circulation", "perrein"): (
            "R\u00e9viser la Zone \u00e0 Faibles \u00c9missions jug\u00e9e dogmatique et rendre la ville accessible \u00e0 tous",
            "isabelleperrein2026.fr, 2026",
            "https://www.isabelleperrein2026.fr/notre-projet"
        ),
        ("environnement", "proprete-dechets", "perrein"): (
            "Rendre Montpellier autonome en traitement des d\u00e9chets et adapter les horaires de nettoyage \u00e0 chaque quartier",
            "isabelleperrein2026.fr, 2026",
            "https://www.isabelleperrein2026.fr/notre-projet"
        ),
        ("economie", "emploi-insertion", "perrein"): (
            "R\u00e9duire le ch\u00f4mage (19%, double du taux d\u00e9partemental) en facilitant l'accueil de PME en croissance",
            "isabelleperrein2026.fr, 2026",
            "https://www.isabelleperrein2026.fr/notre-projet"
        ),
        ("education", "petite-enfance", "perrein"): (
            "Cr\u00e9er 500 places de cr\u00e8ches suppl\u00e9mentaires",
            "isabelleperrein2026.fr, 2026",
            "https://www.isabelleperrein2026.fr/notre-projet"
        ),
        ("education", "ecoles-renovation", "perrein"): (
            "R\u00e9nover les \u00e9coles : am\u00e9liorer la climatisation, les \u00e9quipements sportifs et les biblioth\u00e8ques",
            "isabelleperrein2026.fr, 2026",
            "https://www.isabelleperrein2026.fr/notre-projet"
        ),
        ("democratie", "transparence", "perrein"): (
            "R\u00e9duire les imp\u00f4ts locaux de 15% en ciblant la TEOM, auditer les finances et publier toutes les d\u00e9penses en ligne",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/municipales-2026-a-montpellier-isabelle-perrein-defend-une-baisse-des-impots-fondee-sur-la-rigueur-budgetaire"
        ),
        ("urbanisme", "amenagement-urbain", "perrein"): (
            "Recr\u00e9er des quartiers verdoyants, am\u00e9liorer les trottoirs et augmenter les zones d'ombre et de v\u00e9g\u00e9tation",
            "isabelleperrein2026.fr, 2026",
            "https://www.isabelleperrein2026.fr/notre-projet"
        ),
        ("education", "jeunesse", "perrein"): (
            "Cr\u00e9er un passeport jeunesse 16-25 ans combinant sport et accompagnement vers l'emploi",
            "France Bleu H\u00e9rault, 2026",
            "https://www.francebleu.fr/emissions/l-invite-d-ici-matin-ici-herault/municipales-2026-la-candidate-isabelle-perrein-devoile-son-programme-pour-montpellier-6013218"
        ),
        # --- Gaillard (Sans etiquette) ---
        ("environnement", "espaces-verts", "gaillard"): (
            "Transformer le Verdanson en parc inondable v\u00e9g\u00e9talis\u00e9 servant d'\u00eelot de fra\u00eecheur en centre-ville",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-musee-a-ciel-ouvert-et-parc-inondable-remi-gaillard-veut-transformer-le-verdanson/"
        ),
        ("environnement", "climat-adaptation", "gaillard"): (
            "Am\u00e9nager le Verdanson en sections inondables avec v\u00e9g\u00e9tation pour am\u00e9liorer le drainage lors des \u00e9pisodes c\u00e9venols",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-musee-a-ciel-ouvert-et-parc-inondable-remi-gaillard-veut-transformer-le-verdanson/"
        ),
        ("culture", "evenements-creation", "gaillard"): (
            "Cr\u00e9er un mus\u00e9e de street-art \u00e0 ciel ouvert le long du Verdanson avec promenade haute et ombrag\u00e9e",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-musee-a-ciel-ouvert-et-parc-inondable-remi-gaillard-veut-transformer-le-verdanson/"
        ),
        ("democratie", "transparence", "gaillard"): (
            "Campagne \u00e0 budget z\u00e9ro financ\u00e9e sans argent public, transparence totale comme base du projet politique",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/montpellier-nappartient-pas-au-parti-socialiste-lhumoriste-remi-gaillard-candidat-a-la-mairie"
        ),
        # --- Tsagalos (Ex-RN) ---
        ("securite", "police-municipale", "tsagalos"): (
            "Tripler les effectifs de la police municipale de 192 \u00e0 650 agents",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-je-suis-candidat-aux-municipales-thierry-tsagalos/"
        ),
        ("transports", "tarifs-gratuite", "tsagalos"): (
            "Mettre fin \u00e0 la gratuit\u00e9 totale des transports, remplac\u00e9e par un mod\u00e8le plus \u00e9quitable et soutenable",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-je-suis-candidat-aux-municipales-thierry-tsagalos/"
        ),
        ("transports", "pietons-circulation", "tsagalos"): (
            "R\u00e9ouvrir le tunnel de la Com\u00e9die, r\u00e9tablir l'acc\u00e8s bidirectionnel au parking Gambetta et r\u00e9ouvrir l'avenue Albert-Dubout",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-je-suis-candidat-aux-municipales-thierry-tsagalos/"
        ),
        ("transports", "velo-mobilites-douces", "tsagalos"): (
            "Cr\u00e9er une piste cyclable d\u00e9di\u00e9e sur l'esplanade Charles-de-Gaulle pour une cohabitation s\u00e9curis\u00e9e",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-je-suis-candidat-aux-municipales-thierry-tsagalos/"
        ),
        ("environnement", "proprete-dechets", "tsagalos"): (
            "Construire une nouvelle usine de traitement des d\u00e9chets \u00e0 bilan carbone neutre, ouverte \u00e0 l'actionnariat des habitants",
            "InfocOccitanie, 2026",
            "https://infoccitanie.fr/montpellier-je-suis-candidat-aux-municipales-thierry-tsagalos/"
        ),
        # --- Muller (Revolution permanente) ---
        ("securite", "police-municipale", "muller"): (
            "D\u00e9sarmer la police municipale, dissoudre la BAC, la police des transports et la brigade du logement",
            "R\u00e9volution permanente, 2026",
            "https://www.revolutionpermanente.fr/Avec-Max-Muller-Revolution-Permanente-se-presente-pour-la-premiere-fois-aux-municipales-a"
        ),
        ("logement", "logements-vacants", "muller"): (
            "R\u00e9quisitionner les 13 160 logements vides pour loger les sans-abri, victimes de violences et \u00e9tudiants",
            "R\u00e9volution permanente, 2026",
            "https://www.revolutionpermanente.fr/Avec-Max-Muller-Revolution-Permanente-se-presente-pour-la-premiere-fois-aux-municipales-a"
        ),
        ("logement", "logement-social", "muller"): (
            "Lancer un plan de construction de logements sociaux \u00e9cologiques et r\u00e9nover massivement les r\u00e9sidences universitaires",
            "R\u00e9volution permanente, 2026",
            "https://www.revolutionpermanente.fr/Avec-Max-Muller-Revolution-Permanente-se-presente-pour-la-premiere-fois-aux-municipales-a"
        ),
        ("education", "petite-enfance", "muller"): (
            "Cr\u00e9er des cr\u00e8ches, laveries et cantines populaires pour r\u00e9duire le travail domestique",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/max-muller-candidat-a-montpellier-nous-voulons-porter-la-voix-des-travailleurs-de-la-jeunesse-et-des-quartiers-populaires"
        ),
        ("economie", "emploi-insertion", "muller"): (
            "Titulariser tous les travailleurs municipaux, indexer les salaires sur l'inflation, embaucher ATSEM et AESH",
            "R\u00e9volution permanente, 2026",
            "https://www.revolutionpermanente.fr/Avec-Max-Muller-Revolution-Permanente-se-presente-pour-la-premiere-fois-aux-municipales-a"
        ),
        ("sante", "centres-sante", "muller"): (
            "Plan d'investissement en sant\u00e9 avec recrutement massif de personnel, financ\u00e9 par la taxation des grandes fortunes",
            "R\u00e9volution permanente, 2026",
            "https://www.revolutionpermanente.fr/Avec-Max-Muller-Revolution-Permanente-se-presente-pour-la-premiere-fois-aux-municipales-a"
        ),
        ("democratie", "transparence", "muller"): (
            "\u00c9lus pay\u00e9s au salaire m\u00e9dian avec possibilit\u00e9 de r\u00e9vocation, assembl\u00e9e unique \u00e9lue \u00e0 partir de 16 ans",
            "R\u00e9volution permanente, 2026",
            "https://www.revolutionpermanente.fr/Avec-Max-Muller-Revolution-Permanente-se-presente-pour-la-premiere-fois-aux-municipales-a"
        ),
        ("solidarite", "egalite-discriminations", "muller"): (
            "Supprimer la charte municipale de la\u00efcit\u00e9, autoriser la nourriture halal dans les programmes jeunesse",
            "H\u00e9rault Tribune, 2026",
            "https://echo-des-tribunes.com/herault-tribune/articles/max-muller-candidat-a-montpellier-nous-voulons-porter-la-voix-des-travailleurs-de-la-jeunesse-et-des-quartiers-populaires"
        ),
    }
)
