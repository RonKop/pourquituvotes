#!/usr/bin/env python3
"""
Genere un planning de publication reseaux sociaux (Twitter/X + LinkedIn).
3 posts/jour sur 4 semaines avant les elections (17 fev - 15 mars 2026).

Usage: python scripts/generer_planning_social.py
"""

import json
import csv
import os
from datetime import datetime, timedelta

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
VILLES_JSON = os.path.join(ROOT, "data", "villes.json")
SCHEMA_JSON = os.path.join(ROOT, "data", "schema", "schema_elections.json")
ELECTIONS_DIR = os.path.join(ROOT, "data", "elections")
OUTPUT = os.path.join(ROOT, "data", "planning_social.csv")

BASE_URL = "https://pourquituvotes.fr"

POPULATIONS = {
    "paris": 2_145_906, "marseille": 873_076, "lyon": 522_969,
    "toulouse": 504_078, "nice": 342_669, "nantes": 320_732,
    "montpellier": 295_542, "strasbourg": 290_576, "bordeaux": 260_958,
    "lille": 236_234, "rennes": 222_485, "reims": 182_460,
    "toulon": 176_198, "saint-etienne": 174_082, "le-havre": 169_733,
    "dijon": 159_346, "grenoble": 158_198, "angers": 155_850,
    "villeurbanne": 154_781, "nimes": 148_561, "le-mans": 148_340,
    "clermont": 147_865, "aix-en-provence": 147_477, "brest": 142_722,
    "tours": 136_463, "amiens": 136_105, "annecy": 133_926,
    "limoges": 130_592, "perpignan": 121_875,
    "boulogne-billancourt": 121_334, "metz": 120_205,
    "besancon": 119_199, "orleans": 116_685, "rouen": 114_007,
    "argenteuil": 113_816, "saint-denis": 113_131, "montreuil": 111_260,
    "mulhouse": 108_038, "caen": 106_260, "nancy": 104_885,
    "roubaix": 99_301, "tourcoing": 98_656, "nanterre": 96_689,
    "vitry-sur-seine": 94_649, "creteil": 93_057, "avignon": 92_130,
    "poitiers": 90_032, "aubervilliers": 89_079,
    "asnieres-sur-seine": 87_764, "aulnay-sous-bois": 86_752,
    "dunkerque": 86_279, "versailles": 85_272, "colombes": 85_199,
    "beziers": 79_563, "la-rochelle": 79_119,
    "champigny-sur-marne": 77_890, "pau": 77_215, "cannes": 74_285,
    "merignac": 74_348, "antibes": 73_438, "ajaccio": 73_822,
    "saint-nazaire": 73_546, "calais": 72_929, "drancy": 72_498,
    "colmar": 70_284, "issy-les-moulineaux": 69_023,
    "evry-courcouronnes": 69_134, "noisy-le-grand": 68_238,
    "venissieux": 67_479, "cergy": 67_311, "bourges": 66_328,
    "levallois-perret": 66_082, "pessac": 66_027,
    "valence": 65_313, "cayenne": 64_709, "quimper": 63_929,
    "antony": 63_541, "montauban": 62_860, "troyes": 62_612,
    "chambery": 60_590, "niort": 60_775,
    "neuilly-sur-seine": 60_454, "fort-de-france": 75_714,
    "pantin": 58_924, "lorient": 57_408, "frejus": 55_735,
    "rueil-malmaison": 80_622, "courbevoie": 81_905,
    "le-chesnay-rocquencourt": 29_290, "puteaux": 45_448,
    "volvic": 4_625, "saint-paul-la-reunion": 105_240,
    "le-tampon-la-reunion": 81_614, "saint-denis-la-reunion": 154_766,
    "saint-pierre-la-reunion": 84_234,
}

DUELS = [
    ("paris", "Gregoire", "gregoire", "Dati", "dati", "Le duel au sommet pour la capitale"),
    ("paris", "Gregoire", "gregoire", "Knafo", "knafo", "Deux visions opposees pour Paris"),
    ("paris", "Chikirou", "chikirou", "Knafo", "knafo", "Gauche vs droite a Paris"),
    ("paris", "Bournazel", "bournazel", "Chikirou", "chikirou", "Centre vs gauche a Paris"),
    ("paris", "Gregoire", "gregoire", "Bournazel", "bournazel", "Qui pour succeder a Hidalgo ?"),
    ("paris", "Gregoire", "gregoire", "Chikirou", "chikirou", "Le duel a gauche a Paris"),
    ("paris", "Bournazel", "bournazel", "Knafo", "knafo", "Centre-droit vs droite a Paris"),
    ("paris", "Chikirou", "chikirou", "Bournazel", "bournazel", "Deux profils pour Paris"),
    ("strasbourg", "Barseghian", "barseghian", "Trautmann", "trautmann", "Le match de Strasbourg"),
    ("toulouse", "Moudenc", "moudenc", "Piquemal", "piquemal", "Le duel de Toulouse"),
    ("nice", "Estrosi", "estrosi", "Ciotti", "ciotti", "La droite face a face a Nice"),
    ("grenoble", "Carignon", "carignon", "Gentil", "gentil", "Le duel de Grenoble"),
    ("angers", "Bechu", "bechu", "Laveau", "laveau", "Le match d'Angers"),
    ("annecy", "Armand", "armand", "Roit-Leveque", "roit-leveque", "Le duel d'Annecy"),
    ("le-havre", "Philippe", "philippe", "Lecoq", "lecoq", "Le duel du Havre"),
    ("le-havre", "Philippe", "philippe", "Zarifian", "zarifian", "Le Havre : Philippe vs Zarifian"),
    ("le-havre", "Lecoq", "lecoq", "Zarifian", "zarifian", "Le Havre : gauche vs gauche"),
]

THEMES = [
    ("securite", "Securite"),
    ("transports", "Transports"),
    ("logement", "Logement"),
    ("education", "Education"),
    ("environnement", "Environnement"),
    ("sante", "Sante"),
    ("democratie", "Democratie"),
    ("economie", "Economie"),
    ("culture", "Culture"),
    ("sport", "Sport"),
    ("urbanisme", "Urbanisme"),
    ("solidarite", "Solidarite"),
]


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_pop(vid):
    return POPULATIONS.get(vid, 0)


def get_candidats_vedettes(villes):
    """Retourne les candidats les plus interessants (programme complet ou maire sortant)."""
    vedettes = []
    for v in villes:
        el_file = os.path.join(ELECTIONS_DIR, f"{v['id']}-2026.json")
        if not os.path.exists(el_file):
            continue
        el = load_json(el_file)
        for c in el.get("candidats", []):
            score = get_pop(v["id"])
            if c.get("programmeComplet"):
                score += 500_000
            nb = len([p for st in c.get("propositions", {}).values() for p in (st if isinstance(st, list) else [])])
            if nb > 10:
                score += 200_000
            vedettes.append({
                "ville_id": v["id"],
                "ville_nom": v["nom"],
                "candidat_id": c["id"],
                "candidat_nom": c["nom"],
                "liste": c.get("liste", ""),
                "complet": c.get("programmeComplet", False),
                "score": score,
            })
    vedettes.sort(key=lambda x: -x["score"])
    return vedettes


def main():
    villes = load_json(VILLES_JSON)
    villes.sort(key=lambda v: -get_pop(v["id"]))

    start = datetime(2026, 2, 17)  # Mardi
    election = datetime(2026, 3, 15)  # Dimanche

    posts = []

    def add(date, heure, phase, type_post, tw, li, url, img):
        posts.append({
            "date": date.strftime("%Y-%m-%d"),
            "jour": ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"][date.weekday()],
            "heure": heure,
            "phase": phase,
            "type": type_post,
            "texte_twitter": tw,
            "texte_linkedin": li,
            "url": url,
            "image_og": img,
        })

    # ======================================================
    # Preparer les contenus
    # ======================================================

    # File de villes (triees par population)
    ville_queue = list(villes)
    ville_idx = 0

    # File de duels
    duel_idx = 0

    # File de themes
    theme_idx = 0

    # File de candidats vedettes
    vedettes = get_candidats_vedettes(villes)
    vedette_idx = 0

    # ======================================================
    # PHASE 1 : LANCEMENT (17-21 fev) - 3 posts/jour = 15
    # Matin: ville top / Midi: duel ou thematique / Soir: ville
    # ======================================================

    d = start
    phase1_end = start + timedelta(days=5)

    while d < phase1_end:
        # MATIN : ville ou general
        if ville_idx == 0:
            # Jour 1 matin : post general
            add(d, "09:00", "1-Lancement", "general",
                "Municipales 2026 : comparez les programmes de 548 candidats dans 103 villes.\n\nNeutre. Factuel. Open source.\n\n#Municipales2026 #PourQuiTuVotes",
                "Les municipales 2026 approchent. J'ai cree un outil citoyen pour comparer les programmes de 548 candidats dans 103 villes francaises.\n\nNeutre, factuel, sans publicite.\n\nDecouvrez les propositions de vos candidats :",
                BASE_URL + "/",
                "home.jpg")
        elif ville_idx < len(ville_queue):
            v = ville_queue[ville_idx]
            n = v["stats"]["candidats"]
            hashtag = v["nom"].replace(" ", "").replace("-", "").replace("'", "")
            add(d, "09:00", "1-Lancement", "ville",
                f"Municipales 2026 a {v['nom']} : {n} candidats.\n\nComparez les programmes theme par theme.\n\n#{hashtag}2026 #Municipales2026",
                f"{v['nom']} : {n} candidats aux municipales 2026.\n\nComparez les {v['stats']['propositions']} propositions sur {v['stats']['themes']} thematiques.\n\nOutil citoyen gratuit :",
                f"{BASE_URL}/municipales-2026/{v['id']}/",
                f"{v['id']}.jpg")
        ville_idx += 1

        # MIDI : duel
        if duel_idx < len(DUELS):
            duel = DUELS[duel_idx]
            ville_id, nom_a, id_a, nom_b, id_b, accroche = duel
            vnom = next((v["nom"] for v in villes if v["id"] == ville_id), ville_id)
            add(d, "12:30", "1-Lancement", "duel",
                f"{nom_a} vs {nom_b} a {vnom}.\n\n{accroche}. Comparez leurs propositions.\n\n#{vnom.replace(' ', '').replace('-', '')}2026 #Municipales2026",
                f"Le duel {nom_a} vs {nom_b} a {vnom}.\n\n{accroche}.\nComparez leurs propositions theme par theme :",
                f"{BASE_URL}/municipales-2026/{ville_id}/?candidats={id_a},{id_b}",
                f"duel-{ville_id}-{id_a}-vs-{id_b}.jpg")
            duel_idx += 1

        # SOIR : ville suivante
        if ville_idx < len(ville_queue):
            v = ville_queue[ville_idx]
            n = v["stats"]["candidats"]
            hashtag = v["nom"].replace(" ", "").replace("-", "").replace("'", "")
            add(d, "18:00", "1-Lancement", "ville",
                f"Municipales 2026 a {v['nom']} : {n} candidats.\n\nQui propose quoi ? Comparez les programmes.\n\n#{hashtag}2026 #Municipales2026",
                f"{v['nom']} aux municipales 2026 : {n} candidats.\n\nComparez les programmes :",
                f"{BASE_URL}/municipales-2026/{v['id']}/",
                f"{v['id']}.jpg")
            ville_idx += 1

        d += timedelta(days=1)

    # ======================================================
    # PHASE 2 : MONTEE EN PUISSANCE (24 fev - 7 mars) - 3/jour = 36
    # Matin: ville / Midi: candidat vedette / Soir: duel ou thematique
    # ======================================================

    phase2_start = start + timedelta(days=7)  # Lundi 24 fev
    phase2_end = datetime(2026, 3, 8)
    d = phase2_start

    while d < phase2_end:
        # MATIN : ville
        if ville_idx < len(ville_queue):
            v = ville_queue[ville_idx]
            n = v["stats"]["candidats"]
            hashtag = v["nom"].replace(" ", "").replace("-", "").replace("'", "")
            add(d, "09:00", "2-Montee", "ville",
                f"Municipales 2026 a {v['nom']} : {n} candidats.\n\nComparez les programmes.\n\n#{hashtag}2026 #Municipales2026",
                f"{v['nom']} : {n} candidats aux municipales 2026.\n\nComparez les propositions :",
                f"{BASE_URL}/municipales-2026/{v['id']}/",
                f"{v['id']}.jpg")
            ville_idx += 1

        # MIDI : candidat vedette
        if vedette_idx < len(vedettes):
            cv = vedettes[vedette_idx]
            vedette_idx += 1
            badge = "Programme complet" if cv["complet"] else "Propositions"
            add(d, "12:30", "2-Montee", "candidat",
                f"{cv['candidat_nom']} - Municipales 2026 {cv['ville_nom']}\n\n{badge}. Decouvrez ses propositions.\n\n#{cv['ville_nom'].replace(' ', '').replace('-', '')}2026",
                f"{cv['candidat_nom']} aux municipales 2026 a {cv['ville_nom']}.\n\n{badge}. Consultez ses propositions et comparez :",
                f"{BASE_URL}/municipales-2026/{cv['ville_id']}/candidats/{cv['candidat_id']}/",
                f"{cv['ville_id']}-{cv['candidat_id']}.jpg")

        # SOIR : duel (jours pairs) ou thematique (jours impairs)
        day_num = (d - phase2_start).days
        if day_num % 2 == 0 and duel_idx < len(DUELS):
            duel = DUELS[duel_idx]
            ville_id, nom_a, id_a, nom_b, id_b, accroche = duel
            vnom = next((v["nom"] for v in villes if v["id"] == ville_id), ville_id)
            add(d, "18:00", "2-Montee", "duel",
                f"{nom_a} vs {nom_b} a {vnom}.\n\n{accroche}.\n\n#{vnom.replace(' ', '').replace('-', '')}2026 #Municipales2026",
                f"Le duel {nom_a} vs {nom_b} a {vnom}.\n\n{accroche}.\nComparez :",
                f"{BASE_URL}/municipales-2026/{ville_id}/?candidats={id_a},{id_b}",
                f"duel-{ville_id}-{id_a}-vs-{id_b}.jpg")
            duel_idx += 1
        elif theme_idx < len(THEMES):
            tid, tnom = THEMES[theme_idx]
            theme_idx += 1
            add(d, "18:00", "2-Montee", "thematique",
                f"{tnom} : que proposent les candidats aux municipales 2026 ?\n\nComparez dans 103 villes.\n\n#Municipales2026 #{tnom}",
                f"Enjeu municipales 2026 : {tnom}\n\nComparez les propositions des candidats sur ce theme cle :",
                f"{BASE_URL}/enjeux-2026/{tid}/",
                "comparateur.jpg")

        d += timedelta(days=1)

    # ======================================================
    # PHASE 3 : ACCELERATION (8-14 mars) - 3/jour = 21
    # Matin: candidat / Midi: candidat / Soir: ville ou rappel
    # ======================================================

    phase3_start = datetime(2026, 3, 8)
    d = phase3_start

    while d < election:
        jours_restants = (election - d).days

        # MATIN : candidat vedette
        if vedette_idx < len(vedettes):
            cv = vedettes[vedette_idx]
            vedette_idx += 1
            badge = "Programme complet" if cv["complet"] else "Propositions"
            add(d, "09:00", "3-Acceleration", "candidat",
                f"{cv['candidat_nom']} - Municipales 2026 {cv['ville_nom']}\n\n{badge}.\n\n#{cv['ville_nom'].replace(' ', '').replace('-', '')}2026 #Municipales2026",
                f"{cv['candidat_nom']} a {cv['ville_nom']}.\n\n{badge}. Comparez :",
                f"{BASE_URL}/municipales-2026/{cv['ville_id']}/candidats/{cv['candidat_id']}/",
                f"{cv['ville_id']}-{cv['candidat_id']}.jpg")

        # MIDI : candidat vedette
        if vedette_idx < len(vedettes):
            cv = vedettes[vedette_idx]
            vedette_idx += 1
            badge = "Programme complet" if cv["complet"] else "Propositions"
            add(d, "12:30", "3-Acceleration", "candidat",
                f"{cv['candidat_nom']} - {cv['ville_nom']} 2026\n\n{badge}.\n\n#{cv['ville_nom'].replace(' ', '').replace('-', '')}2026",
                f"{cv['candidat_nom']} aux municipales 2026 a {cv['ville_nom']}.\n\n{badge}. Decouvrez :",
                f"{BASE_URL}/municipales-2026/{cv['ville_id']}/candidats/{cv['candidat_id']}/",
                f"{cv['ville_id']}-{cv['candidat_id']}.jpg")

        # SOIR : rappel ville ou compte a rebours
        if jours_restants <= 3:
            # Compte a rebours
            top_v = ville_queue[jours_restants % len(ville_queue)]
            add(d, "18:00", "3-Acceleration", "rappel",
                f"J-{jours_restants} avant le 1er tour !\n\nVous n'avez pas encore compare les candidats a {top_v['nom']} ?\n\n#{top_v['nom'].replace(' ', '').replace('-', '')}2026 #Municipales2026",
                f"Les municipales 2026 approchent !\n\nComparez les programmes des candidats a {top_v['nom']} avant de voter.\n\nOutil citoyen gratuit :",
                f"{BASE_URL}/municipales-2026/{top_v['id']}/",
                f"{top_v['id']}.jpg")
        elif ville_idx < len(ville_queue):
            v = ville_queue[ville_idx]
            n = v["stats"]["candidats"]
            hashtag = v["nom"].replace(" ", "").replace("-", "").replace("'", "")
            add(d, "18:00", "3-Acceleration", "ville",
                f"Municipales 2026 a {v['nom']} : {n} candidats.\n\nDerniere ligne droite ! Comparez.\n\n#{hashtag}2026 #Municipales2026",
                f"Derniere ligne droite a {v['nom']} : {n} candidats aux municipales 2026.\n\nComparez avant de voter :",
                f"{BASE_URL}/municipales-2026/{v['id']}/",
                f"{v['id']}.jpg")
            ville_idx += 1

        d += timedelta(days=1)

    # Post jour J
    add(election, "08:00", "3-Acceleration", "jour-J",
        "C'est le jour du vote !\n\nMunicipales 2026 : comparez une derniere fois les programmes avant d'aller voter.\n\n548 candidats. 103 villes. Votre choix.\n\n#Municipales2026 #PourQuiTuVotes",
        "C'est le jour du vote ! Municipales 2026.\n\nComparez les programmes une derniere fois avant d'aller aux urnes.\n\n548 candidats, 103 villes, 12 thematiques.\n\nOutil citoyen gratuit :",
        BASE_URL + "/",
        "home.jpg")

    # ======================================================
    # ECRITURE CSV
    # ======================================================

    fieldnames = [
        "date", "jour", "heure", "phase", "type",
        "texte_twitter", "texte_linkedin", "url", "image_og"
    ]

    with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(posts)

    # Stats
    print("=" * 60)
    print("PLANNING RESEAUX SOCIAUX")
    print("=" * 60)
    print(f"Total posts : {len(posts)}")
    print(f"Periode : {posts[0]['date']} -> {posts[-1]['date']}")
    print(f"Villes couvertes : {ville_idx}")
    print(f"Candidats couverts : {vedette_idx}")
    print(f"Duels couverts : {duel_idx}")
    print(f"Themes couverts : {theme_idx}")
    print()

    phases = {}
    types = {}
    for p in posts:
        phases[p["phase"]] = phases.get(p["phase"], 0) + 1
        types[p["type"]] = types.get(p["type"], 0) + 1

    print("Par phase :")
    for phase, count in sorted(phases.items()):
        print(f"  {phase} : {count} posts")

    print("\nPar type :")
    for t, count in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t} : {count} posts")

    print(f"\nFichier : {OUTPUT}")
    print("-> Importable dans Google Sheets (separateur point-virgule)")


if __name__ == "__main__":
    main()
