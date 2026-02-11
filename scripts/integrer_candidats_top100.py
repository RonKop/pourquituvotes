#!/usr/bin/env python3
"""
Intègre les candidats des nouvelles villes top 100 dans les fichiers JSON d'élection.
Met aussi à jour villes.json avec les stats et la liste des candidats.
"""
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VILLES_JSON = os.path.join(BASE_DIR, "data", "villes.json")
ELECTIONS_DIR = os.path.join(BASE_DIR, "data", "elections")


def kebab(s):
    """Convertit un nom en ID kebab-case."""
    s = s.lower().strip()
    # Remplacer les caractères accentués
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'î': 'i', 'ï': 'i',
        'ô': 'o', 'ö': 'o',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n',
        "'": "-", "'": "-", " ": "-",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    # Garder seulement lettres, chiffres et tirets
    s = re.sub(r'[^a-z0-9-]', '', s)
    # Réduire les tirets multiples
    s = re.sub(r'-+', '-', s).strip('-')
    return s


def ajouter_candidats(ville_id, candidats_data):
    """
    Ajoute les candidats dans le fichier JSON d'élection de la ville.
    candidats_data = [
        {"nom": "...", "liste": "...", "programmeUrl": "...", "programmeComplet": False},
        ...
    ]
    """
    election_file = os.path.join(ELECTIONS_DIR, f"{ville_id}-2026.json")
    if not os.path.exists(election_file):
        print(f"  ERREUR: {election_file} n'existe pas")
        return 0

    with open(election_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Si des candidats existent déjà, on ne fait rien
    if data.get("candidats") and len(data["candidats"]) > 0:
        print(f"  SKIP {ville_id}: {len(data['candidats'])} candidats déjà présents")
        return len(data["candidats"])

    candidats = []
    for c in candidats_data:
        cid = kebab(c["nom"].split(" ")[-1])  # Nom de famille en kebab
        # Vérifier unicité
        existing_ids = [x["id"] for x in candidats]
        if cid in existing_ids:
            # Ajouter le prénom
            cid = kebab(c["nom"])
        candidats.append({
            "id": cid,
            "nom": c["nom"],
            "liste": c.get("liste", ""),
            "programmeUrl": c.get("programmeUrl", "#"),
            "programmeComplet": c.get("programmeComplet", False),
            "programmePdfPath": None
        })

    data["candidats"] = candidats

    # Ajouter les propositions vides pour chaque candidat dans chaque sous-thème
    for cat in data.get("categories", []):
        for st in cat.get("sousThemes", []):
            props = st.get("propositions", {})
            for c in candidats:
                if c["id"] not in props:
                    props[c["id"]] = None
            st["propositions"] = props

    with open(election_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  + {ville_id}: {len(candidats)} candidats ajoutés")
    return len(candidats)


def mettre_a_jour_villes_json():
    """Met à jour les stats dans villes.json à partir des fichiers d'élection."""
    with open(VILLES_JSON, "r", encoding="utf-8") as f:
        villes = json.load(f)

    for v in villes:
        election_id = v.get("elections", [f"{v['id']}-2026"])[0] if v.get("elections") else f"{v['id']}-2026"
        election_file = os.path.join(ELECTIONS_DIR, f"{election_id}.json")
        if not os.path.exists(election_file):
            continue

        with open(election_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        nb_candidats = len(data.get("candidats", []))
        nb_props = 0
        nb_complets = 0
        for c in data.get("candidats", []):
            if c.get("programmeComplet"):
                nb_complets += 1
            for cat in data.get("categories", []):
                for st in cat.get("sousThemes", []):
                    prop = st.get("propositions", {}).get(c["id"])
                    if prop and isinstance(prop, dict) and prop.get("texte"):
                        nb_props += 1

        v["stats"] = {
            "candidats": nb_candidats,
            "propositions": nb_props,
            "themes": len(data.get("categories", [])),
            "complets": nb_complets
        }
        v["candidats"] = [
            {"id": c["id"], "nom": c["nom"], "liste": c.get("liste", "")}
            for c in data.get("candidats", [])
        ]

    with open(VILLES_JSON, "w", encoding="utf-8") as f:
        json.dump(villes, f, ensure_ascii=False, indent=2)

    print(f"\nvilles.json mis à jour ({len(villes)} villes)")


# ============================
# DONNÉES DES CANDIDATS
# ============================

CANDIDATS = {
    # --- Ouest + Centre (agent terminé) ---
    "le-mans": [
        {"nom": "Stéphane Le Foll", "liste": "PS (Parti Socialiste)"},
        {"nom": "Marietta Karamanli", "liste": "Union de la gauche écologique et citoyenne (EELV/PCF)"},
        {"nom": "Olivier Sasso", "liste": "LR (Les Républicains)"},
        {"nom": "Victoria de Vigneral", "liste": "RN (Rassemblement National)"},
        {"nom": "Benjamin Sainty", "liste": "Révolution Permanente"},
        {"nom": "Pascale Fontenel-Personne", "liste": "Renaissance (Ensemble)"},
    ],
    "la-rochelle": [
        {"nom": "Thibaut Guiraud", "liste": "Générations La Rochelle (centre-gauche)"},
        {"nom": "Maryline Simoné", "liste": "Union de la gauche (PS/EELV/PCF)"},
        {"nom": "Olivier Falorni", "liste": "PRG / Place Publique / La Convention"},
        {"nom": "Nino Salaün", "liste": "LFI (La France Insoumise)"},
        {"nom": "Christophe Batcabé", "liste": "Sans étiquette / centre-droit", "programmeUrl": "https://christophe-batcabe-larochelle2026.fr/"},
        {"nom": "Jaouad El Marbouh", "liste": "Sans étiquette, Ensemble pour La Rochelle"},
        {"nom": "Séverine Werbrouck", "liste": "RN (Rassemblement National)"},
        {"nom": "Antoine Colin", "liste": "Lutte Ouvrière"},
    ],
    "poitiers": [
        {"nom": "Léonore Moncond'huy", "liste": "EELV (Écologistes)"},
        {"nom": "Anthony Brottier", "liste": "Sans étiquette, Notre priorité c'est vous"},
        {"nom": "François Blanchard", "liste": "PS (Parti Socialiste)"},
        {"nom": "Abdelmajid Amzil", "liste": "Sans étiquette, J'aime Poitiers"},
        {"nom": "Bertrand Geay", "liste": "LFI (La France Insoumise)"},
        {"nom": "Ludovic Gaillard", "liste": "Lutte Ouvrière"},
        {"nom": "Lucile Parnaudeau", "liste": "MoDem / centre-droit"},
        {"nom": "Marie-Dolores Prost", "liste": "Divers droite"},
        {"nom": "Charles Rangheard", "liste": "RN (Rassemblement National)"},
    ],
    "niort": [
        {"nom": "Jérôme Baloge", "liste": "Parti Radical / Ensemble, Niort tous ensemble"},
        {"nom": "Sébastien Mathieu", "liste": "Union de la gauche (LFI/PCF/PS/EELV)"},
        {"nom": "Céline Bonnet-Derisbourg", "liste": "RN (Rassemblement National)"},
    ],
    "cherbourg-en-cotentin": [
        {"nom": "Benoît Arrivé", "liste": "PS (Parti Socialiste)"},
        {"nom": "Camille Margueritte", "liste": "Nouveau Centre / droite et centre"},
        {"nom": "Jean-Marie Lejeune", "liste": "Sans étiquette"},
        {"nom": "Quentin Briegel", "liste": "LFI, Cherbourg Populaire !"},
    ],
    "lorient": [
        {"nom": "Fabrice Loher", "liste": "Divers droite / Horizons, Nous Lorientais", "programmeUrl": "https://www.nous-lorientais.bzh/"},
        {"nom": "Damien Girard", "liste": "EELV, Lorient en commun", "programmeUrl": "https://lorientencommun.fr/"},
        {"nom": "Gaëlle Le Stradic", "liste": "PS (Parti Socialiste)"},
        {"nom": "Vincent Le Tertre", "liste": "LFI (La France Insoumise)"},
        {"nom": "Théo Thomas", "liste": "RN (Rassemblement National)"},
    ],
    "quimper": [
        {"nom": "Isabelle Assih", "liste": "Divers gauche / PS, Quimper Ensemble", "programmeUrl": "https://www.assih2026.bzh/"},
        {"nom": "Guillaume Menguy", "liste": "Droite et centre"},
        {"nom": "Chrystel Hénaff", "liste": "RN (Rassemblement National)"},
        {"nom": "Marie Lauwers", "liste": "LFI / NPA / Gauche bretonne"},
    ],
    "saint-nazaire": [
        {"nom": "David Samzun", "liste": "Divers gauche (sortant)"},
        {"nom": "Violaine Lucas", "liste": "Union de la gauche et de l'écologie (EELV/LFI/PCF)", "programmeUrl": "https://sn26.fr/"},
        {"nom": "Denis Chéreau", "liste": "Horizons / Union droite et centre (LR/Renaissance/MoDem)"},
        {"nom": "Julio Pichon", "liste": "RN, Renouvelle-toi Saint-Nazaire !"},
    ],
    "troyes": [
        {"nom": "François Baroin", "liste": "LR (Les Républicains)"},
        {"nom": "Loëtitia Beury", "liste": "Sans étiquette, Il est temps", "programmeUrl": "https://municipalestroyes.fr/"},
        {"nom": "Sarah Fraincart", "liste": "LFI (La France Insoumise)"},
        {"nom": "Pierre Brochet", "liste": "RN (Rassemblement National)"},
        {"nom": "Pierre Philippe", "liste": "Sans étiquette"},
    ],
    "bourges": [
        {"nom": "Yann Galut", "liste": "Divers gauche (PS/PCF/EELV)"},
        {"nom": "Philippe Mercier", "liste": "Union de la droite et du centre (LR/Renaissance/Horizons)"},
        {"nom": "Marion Recher", "liste": "LFI (La France Insoumise)"},
        {"nom": "Ugo Iannuzzi", "liste": "RN (Rassemblement National)"},
    ],

    # --- Sud (resultats_Sud.txt) ---
    "nimes": [
        {"nom": "Franck Proust", "liste": "LR-Horizons-UDI-Parti radical"},
        {"nom": "Julien Sanchez", "liste": "RN (Rassemblement National)"},
        {"nom": "Julien Plantier", "liste": "Nîmes Avenir + Renaissance"},
        {"nom": "Vincent Bouget", "liste": "Union de la gauche (hors LFI), Nîmes en Commun"},
        {"nom": "Pascal Dupretz", "liste": "LFI (La France Insoumise)"},
        {"nom": "Jean-Marc Philibert", "liste": "Liste citoyenne VIVONS Nîmes"},
    ],
    "avignon": [
        {"nom": "David Fournier", "liste": "PS (Parti Socialiste)"},
        {"nom": "Anne-Sophie Rigault", "liste": "RN (Rassemblement National)"},
        {"nom": "Mathilde Louvain", "liste": "LFI (La France Insoumise)"},
        {"nom": "Olivier Galzi", "liste": "Sans étiquette (droite), Galzi pour Avignon 2026"},
        {"nom": "Stéphan Fiori", "liste": "Divers droite, Entreprendre pour Avignon"},
        {"nom": "François Jacob", "liste": "Sans étiquette"},
    ],
    "beziers": [
        {"nom": "Robert Ménard", "liste": "Divers droite, soutien LR"},
        {"nom": "Julien Gabarron", "liste": "RN (Rassemblement National)"},
        {"nom": "Thierry Antoine", "liste": "Union de la gauche, Printemps de Béziers"},
        {"nom": "David Ocard", "liste": "LFI, Béziers Unie et Populaire"},
        {"nom": "Thierry Mathieu", "liste": "Sans étiquette, Rassembler Béziers"},
    ],
    "pau": [
        {"nom": "François Bayrou", "liste": "MoDem"},
        {"nom": "Jérôme Marbot", "liste": "Union de la gauche et écologistes (PS/EELV/PCF)"},
        {"nom": "Jean-François Blanco", "liste": "LFI / Écologiste, Pau Insoumise écologique et citoyenne"},
        {"nom": "Margaux Taillefer", "liste": "RN (Rassemblement National)"},
        {"nom": "Philippe Arraou", "liste": "Liste citoyenne, Arraou avec vous"},
        {"nom": "Pascal Boniface", "liste": "Liste citoyenne"},
        {"nom": "Cyrille Marconi", "liste": "Lutte Ouvrière"},
        {"nom": "Reynald Cronier", "liste": "Debout La France"},
    ],
    "montauban": [
        {"nom": "Thierry Deville", "liste": "LR (Les Républicains)"},
        {"nom": "Arnaud Hilion", "liste": "PS-EELV, Vivre Montauban"},
        {"nom": "Didier Lallemand", "liste": "UDR-RN"},
        {"nom": "Samir Chikhi", "liste": "LFI-PCF-NPA-Génération.s"},
        {"nom": "Jean-Lou Lévi", "liste": "Sans étiquette, centre-droit"},
        {"nom": "Jean-Philippe Labarre", "liste": "Sans étiquette, Nouveau Montauban"},
        {"nom": "Richard Blanco", "liste": "Lutte Ouvrière"},
    ],
    "cannes": [
        {"nom": "David Lisnard", "liste": "LR / Nouvelle Énergie pour la France"},
        {"nom": "Lucas Mussio", "liste": "RN (Rassemblement National)"},
        {"nom": "Michel Hugues", "liste": "Union de la gauche (PS-PC-Écologistes), Cannes à vous"},
    ],
    "antibes": [
        {"nom": "Jean Léonetti", "liste": "LR (Les Républicains)"},
        {"nom": "Hugo Muriel", "liste": "RN (Rassemblement National)"},
        {"nom": "Michèle Muratore", "liste": "PS-PCF-Place publique"},
        {"nom": "Adrien Nouet", "liste": "LFI-Écologistes"},
        {"nom": "Éric Ducatel", "liste": "Sans étiquette", "programmeUrl": "https://ericducatel.wordpress.com/elections-municipales-2026-a-antibes-juan-les-pins/"},
    ],
    "frejus": [
        {"nom": "David Rachline", "liste": "Sans étiquette (ex-RN)"},
        {"nom": "Emmanuel Bonnemain", "liste": "Centre-droit, Notre parti c'est Fréjus", "programmeUrl": "https://www.notreparticestfrejus.fr/"},
        {"nom": "Martial Cerrutti", "liste": "LR, Soyons fiers de Fréjus"},
        {"nom": "Paula Fassi", "liste": "Liste citoyenne, Fréjus notre territoire durablement"},
        {"nom": "Julien Poussin", "liste": "Opposition de gauche"},
        {"nom": "Christine Romano", "liste": "Union de la gauche (PCF-PS-LFI-EELV), Fréjus Riposte"},
    ],
    "la-seyne-sur-mer": [
        {"nom": "Joseph Minniti", "liste": "LR (Les Républicains)", "programmeUrl": "https://josephminniti2026.fr/"},
        {"nom": "Cheikh Mansour", "liste": "Horizons", "programmeUrl": "https://cheikhmansourmunicipales2026.fr/"},
        {"nom": "Jean-Pierre Colin", "liste": "Centre, Un cap pour la Seyne"},
        {"nom": "Stéphane Sacco", "liste": "Gauche (GRS-PCF-APRÈS), Uni.e.s à gauche pour La Seyne"},
        {"nom": "Olivier Andrau", "liste": "PS, La Seyne Ville des Possibles"},
    ],
    "ajaccio": [
        {"nom": "Stéphane Sbraggia", "liste": "Divers droite, Forza Aiacciu"},
        {"nom": "François Filoni", "liste": "RN-UDR-Mossa Palatina, Gagner pour Ajaccio"},
        {"nom": "Pascal Zagnoli", "liste": "PNC (Partitu di a Nazione Corsa), Stintu Aiaccinu"},
        {"nom": "Jean-Paul Carrolaggi", "liste": "Nationaliste, Aiacciu Vivu"},
        {"nom": "Charlotte Cesari", "liste": "Union de la gauche (PS-PCF)"},
        {"nom": "Philippe de la Foata", "liste": "Sans étiquette"},
    ],

    # --- IDF-Nord (resultats_IDF-Nord.txt) ---
    "argenteuil": [
        {"nom": "Georges Mothron", "liste": "LR (Les Républicains)"},
        {"nom": "Yassin Zeghli", "liste": "LFI (La France Insoumise)"},
        {"nom": "Nicolas Bougeard", "liste": "PS-EELV-Radicaux"},
        {"nom": "Philippe Doucet", "liste": "DVG / Indépendant, Argenteuil Debout"},
        {"nom": "Franck Debeaud", "liste": "PCD, Ensemble rassemblés pour Argenteuil"},
    ],
    "saint-denis": [
        {"nom": "Mathieu Hanotin", "liste": "PS-Écologistes-Parti animaliste-Génération.s-GRS-Place publique"},
        {"nom": "Bally Bagayoko", "liste": "LFI-PCF, Seine-Saint-Denis au cœur"},
        {"nom": "Quentin Gutierrez", "liste": "Horizons / Droite-Centre unis"},
        {"nom": "Elsa Marcel", "liste": "Révolution Permanente"},
    ],
    "montreuil": [
        {"nom": "Patrice Bessac", "liste": "PCF-Écologistes-PS-Génération.s-L'Après-NPA"},
        {"nom": "Sayna Shahryari", "liste": "LFI (La France Insoumise)"},
    ],
    "aubervilliers": [
        {"nom": "Karine Franclet", "liste": "UDI"},
        {"nom": "Sofienne Karroumi", "liste": "DVG, Union de la gauche (PS/Place publique/Génération.s)"},
        {"nom": "Guillaume Lescaut", "liste": "LFI (La France Insoumise)", "programmeUrl": "https://www.guillaumelescaut2026.fr/"},
        {"nom": "Anthony Daguet", "liste": "PCF"},
        {"nom": "Nabila Djebbari", "liste": "DVG"},
        {"nom": "Marc Guerrien", "liste": "DVG"},
        {"nom": "Jean-Louis Lavazec", "liste": "Lutte Ouvrière"},
    ],
    "aulnay-sous-bois": [
        {"nom": "Bruno Beschizza", "liste": "LR, Vivre Aulnay / Protéger Aulnay notre fierté", "programmeUrl": "https://brunobeschizza.fr/"},
        {"nom": "Elena Malandra", "liste": "LFI-PCF, La force de changer à Aulnay-sous-Bois"},
        {"nom": "Oussouf Siby", "liste": "PS-EELV"},
        {"nom": "Cheickh Nguette", "liste": "Démocratie Représentative, Aulnay Humaniste"},
    ],
    "drancy": [
        {"nom": "Jean-Christophe Lagarde", "liste": "UDI"},
        {"nom": "Hamid Chabani", "liste": "DVG / Divers"},
        {"nom": "Gokhan Unver", "liste": "LFI (La France Insoumise)"},
        {"nom": "Hacene Chibane", "liste": "Les Écologistes (EELV)"},
    ],
    "le-blanc-mesnil": [
        {"nom": "Jean-Philippe Ranquet", "liste": "LR (Les Républicains)"},
    ],
    "pantin": [
        {"nom": "Bertrand Kern", "liste": "PS dissident, Pantin au cœur"},
        {"nom": "Mathieu Monot", "liste": "PS officiel, Osez Pantin"},
        {"nom": "Thomas Bardoux", "liste": "LFI, Faire mieux pour Pantin"},
        {"nom": "Geoffrey Carvalhinho", "liste": "LR, Pantin en confiance"},
        {"nom": "Nathalie Arthaud", "liste": "Lutte Ouvrière"},
    ],
    "noisy-le-grand": [
        {"nom": "Brigitte Marsigny", "liste": "LR, Noisy Avenir"},
    ],
    "cergy": [
        {"nom": "Jean-Paul Jeandon", "liste": "DVG (PS/PCF/EELV/Génération.s)"},
        {"nom": "Daisy Yaich", "liste": "LFI (La France Insoumise)"},
        {"nom": "Armand Payet", "liste": "Horizons-LR, droite-centre unie"},
    ],

    # --- IDF-Ouest (resultats_IDF-Ouest.txt) ---
    "boulogne-billancourt": [
        {"nom": "Pierre-Christophe Baguet", "liste": "LR-UDI-MoDem-Renaissance-Horizons"},
        {"nom": "Antoine de Jerphanion", "liste": "Divers droite"},
        {"nom": "Pauline Rapilly-Ferniot", "liste": "Union de la gauche (Écologistes/PCF/LFI)"},
    ],
    "nanterre": [
        {"nom": "Raphaël Adam", "liste": "DVG (PCF/Écologistes/Génération.s), Choisir Nanterre"},
        {"nom": "Nicolas Huyghe", "liste": "LFI (La France Insoumise)"},
        {"nom": "Hélène Matouk", "liste": "LR (Les Républicains)"},
        {"nom": "Samia Kasmi", "liste": "Génération Écologie (dissidente)"},
    ],
    "asnieres-sur-seine": [
        {"nom": "Manuel Aeschlimann", "liste": "LR, 100% Asnières"},
        {"nom": "Clément Mathieu Dautelle", "liste": "Divers, Citoyens d'Asnières"},
        {"nom": "Romain Jehanin", "liste": "Divers, Changeons notre ville !"},
        {"nom": "Dimitri Delpech", "liste": "PS (Parti Socialiste)"},
    ],
    "colombes": [
        {"nom": "Patrick Chaimovitch", "liste": "Les Écologistes (EELV)"},
        {"nom": "Nicole Chassaniol", "liste": "LR (Les Républicains)"},
        {"nom": "Valentin Narbonnais", "liste": "DVG (PS/Génération Écologie/Place Publique/PRG), Colombes en mieux"},
        {"nom": "Joakim Giacomoni", "liste": "LR"},
    ],
    "rueil-malmaison": [
        {"nom": "Pierre Cazeneuve", "liste": "Renaissance"},
        {"nom": "Patrick Indjian", "liste": "Union citoyenne écologiste et solidaire (PS/EELV/PCF)", "programmeUrl": "https://www.patrickindjianrueil2026.fr/"},
    ],
    "courbevoie": [
        {"nom": "Jacques Kossowski", "liste": "LR (Les Républicains)"},
        {"nom": "Aurélie Taquillain", "liste": "Divers centre"},
        {"nom": "Cyprien Ronze-Spilliaert", "liste": "Gauche (Place Publique)"},
    ],
    "levallois-perret": [
        {"nom": "Agnès Pottier-Dumas", "liste": "LR (Les Républicains)"},
        {"nom": "Liès Messatfa", "liste": "Renaissance, Levallois d'Avenir"},
        {"nom": "Baptiste Nouguier", "liste": "DVG, Levallois en commun (PS/Écologistes/Place Publique/PCF)"},
    ],
    "issy-les-moulineaux": [
        {"nom": "André Santini", "liste": "UDI"},
        {"nom": "Mathieu Morel", "liste": "Les Écologistes, Issy écolo et social", "programmeUrl": "https://issyecoloetsocial.fr/"},
        {"nom": "Gaël Lago", "liste": "LFI (La France Insoumise)"},
    ],
    "neuilly-sur-seine": [
        {"nom": "Jean-Christophe Fromantin", "liste": "Divers droite", "programmeUrl": "https://www.fromantin2026.fr/"},
    ],
    "clichy": [
        {"nom": "Rémi Muzeau", "liste": "LR / DVD, Avec Rémi Muzeau Clichy", "programmeUrl": "http://clichynaturellement.com/"},
    ],
    "antony": [
        {"nom": "Jean-Yves Senant", "liste": "LR, Antony pour Tous", "programmeUrl": "https://antonypourtous2026.fr/"},
        {"nom": "David Mauger", "liste": "Gauche-écologistes, Antony Terre Citoyenne"},
        {"nom": "Perrine Precetti", "liste": "Divers droite (dissidente), Antony à venir", "programmeUrl": "https://www.antonyavenir.fr"},
    ],

    # --- IDF-Sud (resultats_IDF-Sud.txt) ---
    "vitry-sur-seine": [
        {"nom": "Pierre Bell-Lloch", "liste": "PCF", "programmeUrl": "https://pbl2026.fr/"},
        {"nom": "Hocine Tmimi", "liste": "LFI, Vitry Unie et Populaire", "programmeUrl": "https://vitry2026.fr/"},
        {"nom": "Alain Afflatet", "liste": "DVD (droite et centre unis), Vitry À Venir", "programmeUrl": "https://vitryavenir.fr/"},
    ],
    "creteil": [
        {"nom": "Laurent Cathala", "liste": "PS-PCF, Bien ensemble"},
        {"nom": "Mehmet Ceylan", "liste": "UDI (investi par LR)"},
        {"nom": "Sylvain Thézard", "liste": "DVD (droite dissident, ex-LR)"},
        {"nom": "Thierry Hebbrecht", "liste": "Sans étiquette (ex-LR)"},
    ],
    "champigny-sur-marne": [
        {"nom": "Laurent Jeanne", "liste": "DVD (union droite-centre)"},
        {"nom": "Julien Léger", "liste": "PCF, union de la gauche (PS/Place Publique/Génération.s/PRG)"},
    ],
    "saint-maur-des-fosses": [
        {"nom": "Pierre-Michel Delecroix", "liste": "LR (Les Républicains)"},
        {"nom": "Vincent Giacobbi", "liste": "Horizons"},
        {"nom": "Matthieu Fernandez", "liste": "Renaissance"},
    ],
    "ivry-sur-seine": [
        {"nom": "Philippe Bouyssou", "liste": "PCF"},
    ],
    "villejuif": [
        {"nom": "Pierre Garzon", "liste": "PCF-PS-Écologistes-Génération.s, Ensemble pour Villejuif"},
        {"nom": "Franck Conquet", "liste": "DVD"},
        {"nom": "Christel Esclangon", "liste": "Sans étiquette, Notre parti c'est Villejuif", "programmeUrl": "https://notrepartivillejuif.fr/"},
    ],
    "evry-courcouronnes": [
        {"nom": "Stéphane Beaudet", "liste": "Sans étiquette (ex-LR), #ONESTENSEMBLE"},
        {"nom": "Farida Amrani", "liste": "LFI (La France Insoumise)", "programmeUrl": "https://faridaamrani2026.fr/"},
        {"nom": "Julien Monier", "liste": "Les Écologistes, Agissons Citoyens", "programmeUrl": "https://julienmonier2026.fr/"},
    ],
    "versailles": [
        {"nom": "François de Mazières", "liste": "DVD / LR", "programmeUrl": "https://demazieres2026.fr/site/"},
        {"nom": "Olivier de La Faire", "liste": "UDR / soutenu par le RN, Union des droites pour Versailles"},
        {"nom": "Sabine Clément", "liste": "Reconquête, À la Reconquête de Versailles"},
        {"nom": "Carole Filleur", "liste": "Sans étiquette, Ensemble Vivons Versailles 2026"},
        {"nom": "Geoffrey Landrain", "liste": "DVG"},
    ],

    # --- Nord-Est (resultats_Nord-Est.txt) ---
    "tourcoing": [
        {"nom": "Doriane Becue", "liste": "Horizons (majorité présidentielle)"},
        {"nom": "Katy Vuylsteker", "liste": "Les Écologistes-PS-PCF"},
        {"nom": "Franck Talpaert", "liste": "Citoyen-ne-s pour Tourcoing (sans étiquette)"},
        {"nom": "Émilie Croes", "liste": "LFI (La France Insoumise)"},
        {"nom": "Bastien Verbrugghe", "liste": "RN (Rassemblement National)"},
    ],
    "roubaix": [
        {"nom": "Alexandre Garcin", "liste": "Divers droite (majorité sortante)"},
        {"nom": "David Guiraud", "liste": "LFI (La France Insoumise)"},
        {"nom": "Mehdi Chalah", "liste": "PS, Le Printemps Roubaisien", "programmeUrl": "https://www.printempsroubaisien2026.fr/"},
        {"nom": "Karim Amrouni", "liste": "Les Écologistes-PCF-PRG-Place publique"},
        {"nom": "Céline Sayah", "liste": "RN-Debout la France"},
        {"nom": "Françoise Delbarre", "liste": "Lutte Ouvrière"},
    ],
    "dunkerque": [
        {"nom": "Patrice Vergriete", "liste": "Divers gauche (soutenu par PS/PCF/LR)", "programmeUrl": "https://www.patricevergriete.dk/"},
        {"nom": "Damien Lacroix", "liste": "LFI, Dunkerque populaire"},
        {"nom": "Adrien Navé", "liste": "RN (Rassemblement National)"},
        {"nom": "Nicolas Fournier", "liste": "Les Écologistes / liste citoyenne, Dunkerque citoyenne"},
    ],
    "villeneuve-d-ascq": [
        {"nom": "Gérard Caudron", "liste": "Divers gauche (Rassemblement Citoyen/Génération.s/MRC)"},
        {"nom": "Ugo Bernalicis", "liste": "LFI (La France Insoumise)"},
        {"nom": "Victor Burette", "liste": "PS, Vivre Villeneuve d'Ascq"},
        {"nom": "Pauline Ségard", "liste": "Les Écologistes, Printemps villeneuvois"},
        {"nom": "Sylvain Estager", "liste": "Divers gauche, Ensemble pour Villeneuve d'Ascq"},
    ],
    "calais": [
        {"nom": "Natacha Bouchart", "liste": "Divers droite"},
        {"nom": "Marc de Fleurian", "liste": "RN (Rassemblement National)"},
        {"nom": "Jean-Philippe Lannoy", "liste": "LFI-EELV, À gauche toute !"},
        {"nom": "Marion Lavigne", "liste": "PCF-PS-Génération.s, Agissons pour Calais"},
        {"nom": "Lucille Nicolas", "liste": "Lutte Ouvrière"},
        {"nom": "Guy Delplanque", "liste": "Sans étiquette"},
        {"nom": "Romain Debaisieux", "liste": "Sans étiquette"},
    ],
    "besancon": [
        {"nom": "Anne Vignot", "liste": "Les Écologistes-PCF-Génération.s"},
        {"nom": "Ludovic Fagaut", "liste": "LR-MoDem, Ensemble Besançon avance"},
        {"nom": "Éric Delabrousse", "liste": "Horizons-Renaissance-Parti radical"},
        {"nom": "Séverine Véziès", "liste": "LFI (La France Insoumise)"},
        {"nom": "Jacques Ricciardetti", "liste": "RN-UDR-DLF-Identité Libertés"},
    ],
    "colmar": [
        {"nom": "Éric Straumann", "liste": "LR (Les Républicains)"},
        {"nom": "Nathalie Aubert", "liste": "RN (Rassemblement National)"},
        {"nom": "Christophe Roussel", "liste": "PS (Parti Socialiste)"},
        {"nom": "Cécile Ney", "liste": "Les Écologistes, Colmar Citoyenne Verte et Solidaire"},
        {"nom": "Frédéric Hilbert", "liste": "Les Écologistes-Place publique"},
        {"nom": "Bruno Deltour", "liste": "Sans étiquette (liste citoyenne)"},
        {"nom": "Yves Hémedinger", "liste": "Sans étiquette / ex-LR, Fiers d'être colmariens", "programmeUrl": "https://yhcolmar2026.fr/"},
    ],
    "valence": [
        {"nom": "Nicolas Daragon", "liste": "LR (Les Républicains)"},
        {"nom": "Paul Christophle", "liste": "PS-PCF-Les Écologistes, L'Appel pour Valence 2026"},
        {"nom": "Jules Boyadjian", "liste": "Divers gauche, Réunir Valence", "programmeUrl": "https://reunirvalence.fr/"},
        {"nom": "Stéphane Magnin", "liste": "LFI, Gauche Écologiste et Populaire"},
        {"nom": "Philippe Dos Reis", "liste": "RN (Rassemblement National)"},
        {"nom": "Adèle Kopff", "liste": "Lutte Ouvrière"},
    ],
    "chambery": [
        {"nom": "Thierry Repentin", "liste": "DVG-PS-PCF-Les Écologistes, Chambéry avance"},
        {"nom": "Vincent Patey", "liste": "Divers droite, Le Pacte", "programmeUrl": "https://chambery2026.fr/"},
        {"nom": "Brice Bernard", "liste": "RN, Rassemblement pour Chambéry", "programmeUrl": "https://brice-bernard.fr/"},
        {"nom": "Christian Saint-André", "liste": "Renaissance"},
        {"nom": "Christelle Favetta-Sieyès", "liste": "UDI dissidente, Chambéry pour de vrai"},
        {"nom": "Gaël Desreumaux", "liste": "Sans étiquette, Avenir Populaire"},
        {"nom": "Marie Ducruet", "liste": "Lutte Ouvrière"},
    ],
    "annecy": [
        {"nom": "Antoine Armand", "liste": "Renaissance-Horizons-MoDem-LR-UDI, Les Acteurs d'Annecy", "programmeUrl": "https://acteursannecy.fr/"},
        {"nom": "Alexandre Mulatier-Gachet", "liste": "Union de la gauche (Écologistes/PS/Place publique/PCF), Vivre Annecy 2026"},
        {"nom": "Jean-Luc Rigaut", "liste": "Divers droite, Pour Annecy 2026"},
        {"nom": "Guillaume Roit-Levêque", "liste": "RN, Retrouvons Annecy", "programmeUrl": "https://retrouvons-annecy.fr/"},
        {"nom": "Vincent Drême", "liste": "LFI, L'avenir en commune"},
        {"nom": "Daniel-Salem Chiad", "liste": "Sans étiquette, Vivre tous ensemble à Annecy"},
    ],

    # --- Rhône-Outre-Mer (resultats_Rhone-OM.txt) ---
    "villeurbanne": [
        {"nom": "Cédric Van Styvendael", "liste": "PS (soutenu par Écologistes/PCF/Place publique)"},
        {"nom": "Jean-Paul Bret", "liste": "Divers gauche (ex-maire, liste autonome)"},
        {"nom": "Mathieu Garabédian", "liste": "LFI (La France Insoumise)"},
        {"nom": "Sophie Cruz", "liste": "Droite et centre (union LR-centre)"},
        {"nom": "Marc Fraysse", "liste": "Sans étiquette (ex-LR)"},
        {"nom": "Gérald Canon", "liste": "RN (Rassemblement National)"},
        {"nom": "Nadia Bouhami", "liste": "Lutte Ouvrière"},
    ],
    "venissieux": [
        {"nom": "Michèle Picard", "liste": "PCF"},
        {"nom": "Idir Boumertit", "liste": "LFI (La France Insoumise)"},
        {"nom": "Pascal Dureau", "liste": "Divers droite-centre, Vénissieux Plurielle"},
        {"nom": "Quentin Taieb", "liste": "RN / UDR, Retrouver Vénissieux"},
        {"nom": "Barbara Petit", "liste": "Lutte Ouvrière"},
        {"nom": "Farid Omeir", "liste": "UDMF (Union des démocrates musulmans français)"},
    ],
    "merignac": [
        {"nom": "Thierry Trijoulet", "liste": "PS (Parti Socialiste)"},
        {"nom": "Thierry Millet", "liste": "Droite et centre (union droite-centre-macronistes)"},
    ],
    "pessac": [
        {"nom": "Franck Raynal", "liste": "Divers droite / Horizons"},
        {"nom": "Sébastien Saint-Pasteur", "liste": "PS (soutenu par PC/Écologistes/Place publique)"},
        {"nom": "Laure Curvale", "liste": "EELV (soutenue par LFI/PC/Génération.s)"},
        {"nom": "Bérangère Couillard", "liste": "Divers centre (ex-Renaissance, liste citoyenne)"},
        {"nom": "Philippe Jaouen", "liste": "LFI (La France Insoumise)"},
        {"nom": "Isabelle Ufferte", "liste": "NPA (Nouveau Parti Anticapitaliste)"},
        {"nom": "David Rybak", "liste": "Sans étiquette (liste citoyenne)"},
    ],
    "saint-denis-reunion": [
        {"nom": "Éricka Bareigts", "liste": "PS (Parti Socialiste)"},
        {"nom": "René-Paul Victoria", "liste": "LR (Les Républicains)"},
        {"nom": "Jean-Max Nativel", "liste": "RN (Rassemblement National)"},
        {"nom": "Gaëlle Lebon", "liste": "Rassemblement Réunion (ex-RN/Reconquête)"},
        {"nom": "Giovanni Payet", "liste": "Divers, collectif La Voix Citoyenne"},
        {"nom": "Farid Mangrolia", "liste": "Divers centre, Tous Dionysiens"},
        {"nom": "Ludovic Sautron", "liste": "Écologiste / divers gauche"},
    ],
    "saint-paul-reunion": [
        {"nom": "Emmanuel Séraphin", "liste": "PLR / Union des Forces Progressistes (PS/Écologistes/LFI)"},
        {"nom": "Jean-Yves Morel", "liste": "RN (Rassemblement National)"},
        {"nom": "Jean-Jacques Charolais", "liste": "Divers"},
        {"nom": "Alix Jean Méra", "liste": "Debout la France"},
        {"nom": "Hassam Moussa", "liste": "Force Citoyenne"},
    ],
    "saint-pierre-reunion": [
        {"nom": "David Lorion", "liste": "Divers droite / sans étiquette"},
        {"nom": "Émeline K/Bidi", "liste": "Divers gauche (soutenue par LFI/NFP)"},
        {"nom": "Ruth Dijoux", "liste": "Ekilibre, L'Union des Saint-Pierrois (PS/Écologistes)"},
        {"nom": "Virginie Gobalou", "liste": "Convictions Réunion"},
        {"nom": "Bernard Von-Pine", "liste": "Divers"},
        {"nom": "Richard Riani", "liste": "Divers / liste citoyenne"},
    ],
    "le-tampon": [
        {"nom": "Patrice Thien-Ah-Koon", "liste": "Divers droite (accord RN)"},
        {"nom": "Alexis Chaussalet", "liste": "LFI, union de la gauche"},
        {"nom": "Nathalie Bassire", "liste": "Divers droite, L'Alliance des Tamponnais"},
    ],
    "fort-de-france": [
        {"nom": "Didier Laguerre", "liste": "PPM (Parti Progressiste Martiniquais)"},
        {"nom": "Francis Carole", "liste": "Divers gauche, Démaré Fodwans"},
        {"nom": "Steeve Moreau", "liste": "PLP (Pour Le Peuple)"},
        {"nom": "Nathalie Jos", "liste": "PIA (Péyi A)"},
        {"nom": "Marie-Laurence Delor", "liste": "Divers"},
    ],
    "cayenne": [
        {"nom": "Marie-Laure Phinera-Horth", "liste": "NFG (Nouvelle Force de Guyane)"},
        {"nom": "Sandra Trochimara", "liste": "Divers (maire sortante)"},
        {"nom": "Olivier Taoumi", "liste": "La Guyane à droite"},
        {"nom": "Bernadette Duclona Constant", "liste": "Nous Guyane"},
    ],
}


if __name__ == "__main__":
    print("=== Intégration des candidats top 100 ===\n")
    total = 0
    for ville_id, candidats in CANDIDATS.items():
        nb = ajouter_candidats(ville_id, candidats)
        total += nb

    print(f"\n--- {total} candidats intégrés ---")

    print("\n=== Mise à jour villes.json ===")
    mettre_a_jour_villes_json()
