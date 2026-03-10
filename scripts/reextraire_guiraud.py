#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ré-extraction propre du programme Guiraud (Roubaix) — 400 propositions
V2 : Extrait les bullets (●, ■, ○) ET les titres de propositions (paragraphes courts
suivis de texte explicatif long).
"""

import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TEXT_FILE = os.path.join(ROOT_DIR, "data", "programmes", "guiraud_roubaix_full_text.txt")
ELECTION_FILE = os.path.join(ROOT_DIR, "data", "elections", "roubaix-2026.json")

SOURCE = "Programme « 400 propositions — Roubaix 2040 » (Guiraud)"
SOURCE_URL = "https://www.fierderoubaix.fr/"

# Section title patterns -> sous-thème mapping with keywords
SECTIONS = [
    ("\uFFFDPauvreté", {
        "aide-sociale": ["CCAS", "aide", "secours", "non-recours", "sans-abri", "accompagnement", "épicerie", "alimentaire", "droits", "dignité", "étranger", "urgence", "prévention", "parentalité"],
        "pouvoir-achat": ["eau", "tarification", "facture", "budget", "pouvoir d'achat", "m³"],
        "services-publics": ["mairie de quartier", "guichet", "service public", "écrivain public", "proximité", "permanence"],
    }),
    ("誽Logement", {
        "logement-social": ["logement social", "HLM", "bailleur", "répartition", "métropol", "priorité municipale", "adjoint"],
        "logements-vacants": ["vacant", "insalubre", "indigne", "remettre en usage", "mission logement", "chantier d'insertion"],
        "encadrement-loyers": ["loyer", "encadrement", "charte"],
        "acces-logement": ["accession", "coopératif", "foncière", "bail réel", "expulsion", "PMR", "mobilité réduite", "mutualiser", "accessible"],
    }),
    ("載[^A-Za-z]*Social\\s*:?\\s*Familles,?\\s*enfance", {
        "petite-enfance": ["enfant", "crèche", "parentalité", "aire de jeux", "famille monoparentale", "tarif", "petite enfance", "accueil"],
        "seniors": ["aîné", "senior", "EHPAD", "aidant", "grand-âge", "intergénérationnel", "taxi solidaire"],
    }),
    ("虢Culture", {
        "equipements-culturels": ["pratique artistique", "conservatoire", "médiateur", "lecture", "bibliothèque", "médiathèque", "théâtre", "arts visuels", "tarification", "équipement", "école", "accessible"],
        "evenements-creation": ["festival", "artiste", "scène", "concert", "musiques", "Colloque", "tremplin", "POP-UP", "URBX", "création", "résidence"],
    }),
    ("겹Patrimoine", {
        "patrimoine-roubaisien": None,
    }),
    ("곬Commerce et entrepreneuriat", {
        "commerce-local": None,
    }),
    ("艌Coopération internationale", {
        "attractivite": None,
    }),
    ("긆Education et écoles", {
        "ecoles-renovation": ["école", "oasis", "classe", "enseignement", "REP", "transplantée", "transition écologique", "crèche", "violence éducative", "défendre"],
        "cantines-fournitures": ["cantine", "restauration", "repas"],
        "periscolaire-loisirs": ["périscolaire", "médiathèque", "devoir", "bibliothèque", "vacances", "horaires"],
        "jeunesse": ["cérémonie", "thème éducatif", "conseil parental", "natation"],
    }),
    ("袭Sport populaire", {
        "equipements-sportifs": ["parc des sports", "rénovation", "stade", "équipement", "office municipal", "contrat", "scolaire", "piscine", "gymnase", "city-stade"],
        "sport-pour-tous": ["pass sport", "olympiade", "urban trail", "gratuit", "populaire", "féminin", "parcours", "sport-études", "performance", "rayonner", "licence", "handisport", "découvrir"],
    }),
    ("ꏏ\\s*Formation,?\\s*emploi et insertion", {
        "emploi-insertion": None,
    }),
    ("課Urbanisme et cadre de vie", {
        "amenagement-urbain": ["agenda", "qualité urbaine", "centre-ville", "avenue des nations", "place", "publicité", "désaffecté", "convivialité", "piétonniser", "commerce de proximité", "valorisation"],
        "quartiers-prioritaires": ["ANRU", "Alma", "Épeule", "Pile", "Trois-Ponts", "Cul-de-Four", "rattrapage", "quartier marginalisé"],
    }),
    ("苩Nature", {
        "espaces-verts": ["parc", "jardin", "arbre", "forêt", "canopée", "vert", "nature", "biodiversité", "canal", "trame verte", "végétal", "habitant", "ponton", "boisement", "friche", "potager", "verger", "rucher", "plantation"],
        "climat-adaptation": ["climat", "canicule", "adaptation", "urgence climatique", "îlot de chaleur", "miroir d'eau", "fraîcheur", "récupérateur", "eau de pluie", "plan canicule", "animal", "nuisible", "stérilisation", "bien-être animal"],
    }),
    ("랖Mobilités", {
        "transports-en-commun": ["transport", "bus", "tram", "ilévia", "réseau", "cadencement", "gare"],
        "velo-mobilites-douces": ["vélo", "cyclable", "cycliste", "plan vélo", "bourses solidaires vélo", "système vélo", "trottinette"],
        "pietons-circulation": ["piéton", "piétonniser", "rue", "marcher", "zone 30", "trottoir", "scolaire apaisée", "code local", "voirie", "éclairage"],
        "stationnement": ["stationnement", "parking", "SUV", "garer"],
        "tarifs-gratuite": ["gratuit", "tarif", "pass mobilité", "coût", "1 €"],
    }),
    ("\uE0B6Energie", {
        "renovation-energetique": None,
    }),
    ("놉Propreté et circularités", {
        "proprete-dechets": None,
    }),
    ("츇Santé", {
        "centres-sante": ["médecin", "centre de santé", "pharmacie", "hôpital", "IFSI", "complémentaire", "réseau de centres"],
        "prevention-sante": ["prévention", "diabète", "sport-santé", "mental", "addiction", "protoxyde", "sortie d'hôpital"],
    }),
    ("莇Alimentation", {
        "alimentation-durable": None,
    }),
    ("뇃Participation et démocratie", {
        "budget-participatif": ["budget participatif", "assemblée citoyenne", "votation", "Porto Alegre", "2 %", "pouvoir citoyen", "budget d'investissement"],
        "transparence": ["éthique", "anticorruption", "transparence", "interpellation", "éducation populaire", "syndicale", "charte", "référent", "corrup", "déontologue", "rendez-vous citoyen", "former les citoyen", "rapport", "indicateur"],
        "services-publics": ["mairie de quartier", "guichet", "permanence", "gouvernance", "adjoint", "équipement public", "services publics", "fonction publique", "agent", "numérique"],
    }),
    ("괖\\s*Vie associative", {
        "vie-associative": None,
    }),
    ("B\\.\\s*Vivre ensemble", {
        "vie-associative": None,  # laïcité, lieux de culte, dialogue
    }),
    ("뮆Tranquillité publique", {
        "police-municipale": ["police", "brigade", "armement", "sécurité", "protection des habitants", "présence humaine"],
        "videoprotection": ["vidéo", "caméra", "surveillance", "piège", "Barbieux"],
        "prevention-mediation": ["médiat", "prévention", "délinquance", "tranquillité", "narcotrafic", "rodéo", "trafic", "centres sociaux", "comités citoyens", "jeune", "souffrance", "sortie"],
    }),
    ("붼Inclusion,?\\s*lutte contre les\\s+discriminations", {
        "egalite-discriminations": ["racis", "discriminat", "mémoire coloniale", "LGBTIphob", "observatoire", "antiracis", "livret", "charte", "formation"],
        "violences-femmes": ["femme", "féminisme", "sexis", "sexuel", "genre", "harcèlement", "protection des victimes", "nuit", "ville la nuit"],
        "accessibilite": ["accessibilité", "handicap", "PMR", "design universel"],
    }),
    ("궦Fonction publique municipale", {
        "services-publics": None,
    }),
    ("굇Finances", {
        "transparence": None,
    }),
    ("녔Infrastructures numériques", {
        "services-publics": None,
    }),
]


def get_body_text(full_text):
    """Extrait le texte du body (pages 30+)."""
    pages = full_text.split("=== PAGE ")
    body = ""
    for p in pages:
        if not p.strip():
            continue
        try:
            pnum = int(p.split("===")[0].strip())
        except (ValueError, IndexError):
            continue
        if pnum >= 30:
            content = p.split("===", 1)[-1] if "===" in p else p
            content = re.sub(r"^\s*\d{1,3}\s*\n", "", content.lstrip())
            body += f"\n<<PAGE_{pnum}>>\n" + content
    return body


def extract_bullet(raw_text):
    """Nettoie un bullet brut en mesure propre (max 300 chars)."""
    clean = raw_text.strip()
    clean = re.sub(r"\s*\n\s*", " ", clean)
    clean = re.sub(r"\s+", " ", clean)
    sentences = clean.split(". ")
    result = []
    char_count = 0
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        result.append(s)
        char_count += len(s)
        if char_count > 250:
            break
    if result:
        text_final = ". ".join(result)
        if not text_final.endswith(".") and not text_final.endswith("!") and not text_final.endswith(")"):
            text_final += "."
        if len(text_final) >= 20:
            return text_final
    return None


def extract_bullets(text):
    """Extrait les mesures à puces (●, ○, ■) d'un bloc de texte."""
    measures = []
    for marker in ["●", "○", "■"]:
        parts = re.split(r"\n\s*" + re.escape(marker) + r"\s*", text)
        for i, part in enumerate(parts):
            if i == 0:
                continue
            m = extract_bullet(part)
            if m and m not in measures:
                measures.append(m)
    return measures


def extract_titled_proposals(text):
    """Extrait les propositions formatées comme 'titre + paragraphe explicatif'.

    Dans le PDF Guiraud, les titres et le corps sont en texte continu SANS lignes
    vides. On joint tout le texte et on scanne pour trouver les frontières
    titre/corps en détectant les transitions.

    Pattern : ". Titre de la proposition Body text qui commence par..."
    On détecte le titre quand : après un point/fin de phrase, un texte de 25-200
    chars commence par un verbe d'action ou article, suivi d'un body starter.
    """
    measures = []

    # Joindre le texte en supprimant les marqueurs de page et numéros
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            lines.append("")  # garder les sauts de ligne
            continue
        if stripped.startswith("<<PAGE_"):
            continue
        if re.match(r"^\d{1,3}$", stripped):
            continue
        # Ignorer caractères unicode décoratifs seuls
        if len(stripped) <= 3 and not any(c.isalpha() for c in stripped):
            continue
        lines.append(stripped)

    joined = " ".join(lines)
    # Normaliser les espaces
    joined = re.sub(r"\s+", " ", joined).strip()

    # Verbes d'action qui débutent un titre de proposition
    action_verbs = (
        "Créer|Lancer|Faire|Garantir|Renforcer|Développer|"
        "Mettre|Instaurer|Nommer|Réformer|Inscrire|Organiser|"
        "Partager|Former|Associer|Ouvrir|Relancer|Relier|"
        "Anticiper|Construire|Soutenir|Favoriser|Proposer|"
        "Déployer|Obtenir|Défendre|Mutualiser|Adopter|"
        "Étendre|Rendre|Aller|Redonner|Sanctuariser|"
        "Améliorer|Valoriser|Libérer|Investir|Lutter|"
        "Reprendre|Installer|Mobiliser|Réparer|Diagnostiquer|"
        "Accompagner|Transformer|Revitaliser|Refonder|Affirmer|"
        "Moderniser|Structurer|Stimuler|Augmenter|Démocratiser|"
        "Cartographier|Expérimenter|Piétonniser|Sécuriser|"
        "Assurer|Interdire|Réinstaurer|Protéger|Réduire|"
        "Introduire|Réviser|Poursuivre|Préserver|Consolider|"
        "Bâtir|Impliquer|Déclarer|Engager|Préparer|"
        "Accélérer|Intégrer|Encadrer|Supprimer|"
        "Adapter|Renégocier|Promouvoir|Encourager|"
        "Doter|Généraliser|Amplifier|Revaloriser|"
        "Réaliser|Restaurer|Reprendre|Négocier|"
        "Planifier|Inscrire|Étendre|Relancer|"
        "Un |Une |Des |Le |La |Les |L'|D'|Vers |Chaque "
    )

    # Body starters : mots communs au début du texte explicatif
    body_starters_str = (
        "À [A-ZÉÈÊÀÂÔÙÇ]|Nous |La Ville |La ville |"
        "Dans |Pour |Cela |Cette |En |Face |Notre |"
        "Son |Dès |Trop |Chaque |Roubaix |Ceux |"
        "Il |Ce |Or |Aujourd'|Afin |Car |Alors |"
        "C'est |Plus |Moins |Tant |Avec |Sans |"
        "De nombreux |Depuis |Trop de |L'objectif|"
        "Les [0-9]|Les [a-zéèêà]|Les [A-ZÉÈÊÀÂ]|"
        "Des [a-zéèêà]|Des [A-ZÉÈÊÀÂ]|"
        "Un [a-zéèêà]|Une [a-zéèêà]|"
        "Toute |Tout |Le [a-zéèêà]|La [a-zéèêà]|"
        "La présence|Le réchauffement|"
        "Chaque Roubaisien|La Ville déploiera|"
        "La mobilité|La lutte|Nous voulons|Nous mettrons|"
        "Nous créerons|Nous renforcerons|Nous engagerons|"
        "Nous réaliserons|Nous lancerons|Nous soutiendrons|"
        "Nous favoriserons|Nous défendrons|Nous réviserons|"
        "Nous développerons|Nous déploierons|Nous adapterons|"
        "Nous élargirons|Nous intégrerons|Nous proposerons|"
        "La prolifération|L'accès|"
        "Ce schéma|Ce site|Ce plan|Cette action|"
        "Chaque rendez-vous|Chaque maire"
    )

    # Regex : chercher un titre (verbe d'action + 20-180 chars) suivi d'un body starter
    # Le titre commence après un ". " ou au début du texte, ou après "! " ou ") "
    title_re = re.compile(
        r'(?:^|(?<=\. )|(?<=! )|(?<= \) ))'
        r'((?:' + action_verbs + r')[^.!]{15,180}?)'
        r' (?=' + body_starters_str + r')',
    )

    for match in title_re.finditer(joined):
        title = match.group(1).strip()
        # Nettoyage
        if title.isupper():
            continue
        if len(title) < 25 or len(title) > 200:
            continue
        if not title.endswith(".") and not title.endswith("!"):
            title += "."
        if title not in measures:
            measures.append(title)

    return measures


def split_body_into_sections(body):
    """Découpe le body text en sections selon les titres connus."""
    section_positions = []

    for title_re, sous_themes_map in SECTIONS:
        pattern = re.compile(title_re, re.IGNORECASE)
        matches = list(pattern.finditer(body))
        if matches:
            pos = matches[0].start()
            section_positions.append((pos, title_re, sous_themes_map))

    section_positions.sort(key=lambda x: x[0])

    sections = []
    for i, (pos, title_re, stm) in enumerate(section_positions):
        if i + 1 < len(section_positions):
            end_pos = section_positions[i + 1][0]
        else:
            end_pos = len(body)
        text = body[pos:end_pos]
        sections.append((title_re, stm, text))

    return sections


def map_measures_to_sous_themes(measures, sous_themes_map):
    """Mappe les mesures aux sous-thèmes par mots-clés."""
    result = {}
    st_ids = list(sous_themes_map.keys())

    if len(st_ids) == 1 or all(v is None for v in sous_themes_map.values()):
        for st_id in st_ids:
            result[st_id] = measures
        return result

    for st_id in st_ids:
        result[st_id] = []

    for m in measures:
        lower = m.lower()
        best_st = None
        best_score = 0

        for st_id, keywords in sous_themes_map.items():
            if keywords is None:
                continue
            score = 0
            for kw in keywords:
                if kw.lower() in lower:
                    score += 1
                    # Bonus pour keywords longs (plus spécifiques)
                    if len(kw) > 12:
                        score += 1
            if score > best_score:
                best_score = score
                best_st = st_id

        if best_st:
            result[best_st].append(m)
        else:
            # Fallback: premier sous-thème
            result[st_ids[0]].append(m)

    return result


def main():
    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        full_text = f.read()

    with open(ELECTION_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 60)
    print("  RÉ-EXTRACTION GUIRAUD V2 (Roubaix)")
    print("=" * 60)
    print()

    # 1. Extraire le body text
    body = get_body_text(full_text)
    print(f"  Body text: {len(body)} chars (pages 30+)")

    # 2. Découper en sections
    sections = split_body_into_sections(body)
    print(f"  {len(sections)} sections trouvées")
    print()

    # 3. Extraire les mesures de chaque section (bullets + titres)
    all_mesures = {}
    total = 0

    for title_re, sous_themes_map, section_text in sections:
        # Extraire les bullets
        bullet_measures = extract_bullets(section_text)

        # Extraire les titres de propositions
        title_measures = extract_titled_proposals(section_text)

        # Combiner : bullets d'abord, puis titres non-dupliqués
        measures = list(bullet_measures)
        bullet_starts = set(m[:40].lower() for m in measures)
        for tm in title_measures:
            if tm[:40].lower() not in bullet_starts:
                measures.append(tm)

        total += len(measures)

        # Mapper aux sous-thèmes
        mapped = map_measures_to_sous_themes(measures, sous_themes_map)

        section_name = title_re[:45].replace("\\s*", " ").replace(":?", "").replace(",?", "")
        b_count = len(bullet_measures)
        t_count = len(measures) - b_count
        print(f"  {section_name}: {len(measures)} mesures ({b_count} bullets + {t_count} titres)")

        for st_id, st_measures in mapped.items():
            if st_measures:
                all_mesures.setdefault(st_id, []).extend(st_measures)
                print(f"    -> {st_id}: {len(st_measures)}")

    print()
    print(f"  TOTAL: {total} mesures extraites")
    print()

    # 4. Mettre à jour le JSON
    print("  Mise à jour JSON:")
    updated = 0
    for cat in data["categories"]:
        for st in cat["sousThemes"]:
            st_id = st["id"]
            prop = st["propositions"].get("guiraud")
            if not prop:
                # Si on a de nouvelles mesures pour un sous-thème non couvert
                if st_id in all_mesures and all_mesures[st_id]:
                    st["propositions"]["guiraud"] = {
                        "mesures": all_mesures[st_id],
                        "source": SOURCE,
                        "sourceUrl": SOURCE_URL,
                    }
                    updated += 1
                    print(f"    {st_id}: NOUVEAU -> {len(all_mesures[st_id])}")
                continue

            old_count = len(prop.get("mesures", []))
            new_measures = all_mesures.get(st_id, [])

            if new_measures:
                # V2 est plus précis — toujours remplacer
                prop["mesures"] = new_measures
                prop["source"] = SOURCE
                prop["sourceUrl"] = SOURCE_URL
                updated += 1
                if old_count != len(new_measures):
                    print(f"    {st_id}: {old_count} -> {len(new_measures)}")
                else:
                    print(f"    {st_id}: {len(new_measures)} (inchangé)")

    # Sauvegarder
    if total >= 100:
        with open(ELECTION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n  {updated} sous-thèmes mis à jour")
        print(f"  Fichier: {ELECTION_FILE}")
    else:
        print(f"\n  Seulement {total} mesures — seuil non atteint, JSON non modifié")

    return 0


if __name__ == "__main__":
    sys.exit(main())
