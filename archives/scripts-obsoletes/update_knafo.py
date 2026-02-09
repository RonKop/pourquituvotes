#!/usr/bin/env python3
"""
Intégration du programme complet de Sarah Knafo (133 pages) dans app.js
Remplace les entrées knafo partielles par les mesures extraites du PDF.
"""

import re
import os

APPJS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "js", "app.js")
SOURCE = "Programme officiel 2026"
SOURCE_URL = "https://unevilleheureuse.fr/"

def to_js(text):
    """Convertit les caractères accentués en escapes JS unicode."""
    result = []
    for ch in text:
        cp = ord(ch)
        if cp > 127:
            result.append('\\u{:04X}'.format(cp))
        else:
            result.append(ch)
    return ''.join(result)

# Mesures extraites du programme complet (133 pages)
MESURES = {
    # === LOGEMENT ===
    "logement-public": (
        "Moratoire sur la construction de logements sociaux (273 M\\u20AC/an d\\u2019\\u00E9conomies). "
        "Vente de 4 000 logements sociaux par an aux occupants avec exon\\u00E9ration de frais de notaire. "
        "Grand plan d\\u2019accession \\u00E0 la propri\\u00E9t\\u00E9 pour les classes moyennes"
    ),
    "encadrement-loyers": (
        "Suppression de l\\u2019encadrement des loyers pour remettre 50 000 logements sur le march\\u00E9 locatif "
        "et mettre fin aux effets n\\u00E9fastes (Airbnb, logements vacants, contentieux)"
    ),
    "parc-social": (
        "Attribution des logements sociaux via une appli transparente (crit\\u00E8res publics, points, file d\\u2019attente en temps r\\u00E9el). "
        "Favoriser la rotation (majoration loyer si revenus \\u00E9lev\\u00E9s). "
        "Expulsion syst\\u00E9matique des fauteurs de troubles du parc social. "
        "Villa des talents : r\\u00E9sidence \\u00E9tudiante d\\u2019excellence financ\\u00E9e par les grandes \\u00E9coles"
    ),

    # === ÉCOLOGIE POPULAIRE & POUVOIR D'ACHAT ===
    "alimentation": (
        "100% de produits issus de l\\u2019agriculture fran\\u00E7aise dans les cantines scolaires "
        "(30 millions de repas/an, +7 M\\u20AC/an)"
    ),

    # === BOUCLIER SOCIAL & SOLIDARITÉ ===
    "sante": (
        "Doubler la contribution au d\\u00E9pistage des cancers (1 M\\u20AC/an). "
        "Financer la recherche m\\u00E9dicale via l\\u2019Institut Pasteur (5 M\\u20AC/an). "
        "R\\u00E9nover les EHPAD municipaux (12 M\\u20AC sur le mandat). "
        "1\\u00E8re heure de stationnement gratuite pour les infirmi\\u00E8res lib\\u00E9rales"
    ),

    # === ÉDUCATION & JEUNESSE ===
    "creches-petite-enfance": (
        "Cr\\u00E9ation imm\\u00E9diate de 7 000 places en cr\\u00E8che : priorit\\u00E9 logement social aux pros petite enfance, "
        "salaire +10%, gestion centralis\\u00E9e des absences, appli transparente d\\u2019attribution sans passe-droit, "
        "achat de 1 000 places en cr\\u00E8ches priv\\u00E9es de qualit\\u00E9"
    ),
    "ecole-publique": (
        "Fin de la guerre contre l\\u2019\\u00E9cole priv\\u00E9e : \\u00E9quit\\u00E9 public/priv\\u00E9 pour l\\u2019acc\\u00E8s aux gymnases et piscines. "
        "Autoriser les implantations de nouvelles antennes d\\u2019\\u00E9coles priv\\u00E9es de qualit\\u00E9. "
        "Bras de fer avec le rectorat contre les crit\\u00E8res id\\u00E9ologiques d\\u2019Affelnet"
    ),
    "cantine-fournitures": (
        "100% de produits issus de l\\u2019agriculture fran\\u00E7aise dans les cantines scolaires "
        "(30 millions de repas/an, +7 M\\u20AC/an)"
    ),
    "periscolaire": (
        "V\\u00E9rifications strictes (casier, Fijais) pour tous les intervenants p\\u00E9riscolaires. "
        "Fin du recours aux associations : ATSEM en heures suppl\\u00E9mentaires. "
        "Appel aux parents et grands-parents b\\u00E9n\\u00E9voles r\\u00E9mun\\u00E9r\\u00E9s \\u00E0 la vacation"
    ),

    # === TRANSPORTS & MOBILITÉ ===
    "navettes-fluviales": (
        "D\\u00E9veloppement de la livraison de marchandises par voie fluviale "
        "(appel \\u00E0 manifestation d\\u2019int\\u00E9r\\u00EAt pour navettes fluviales, dernier km en v\\u00E9lo ou camion)"
    ),
    "velo": (
        "Nouveau contrat V\\u00E9lib int\\u00E9grant la publicit\\u00E9 (\\u00E9conomie de 22 M\\u20AC/an, clause de reprise du personnel). "
        "Piste cyclable bidirectionnelle maintenue sur la rue de Rivoli"
    ),
    "pietons-circulation": (
        "R\\u00E9ouverture des voies sur berge + promenade pi\\u00E9tonne et cycliste au-dessus (60 M\\u20AC, r\\u00E9f\\u00E9rendum). "
        "R\\u00E9am\\u00E9nagement de Rivoli (voie auto + piste cyclable + trottoir \\u00E9largi, 6 M\\u20AC). "
        "Feux tricolores pilot\\u00E9s par IA (-11% temps de trajet). "
        "Tarif unique stationnement 3\\u20AC/h, 1\\u00E8re heure gratuite, gratuit 12h-14h. "
        "15 000 places de stationnement cr\\u00E9\\u00E9es. "
        "Places disponibles en temps r\\u00E9el via IA"
    ),

    # === ESPACES PUBLICS & ENVIRONNEMENT ===
    "arbres-vegetation": (
        "Sublimer les parcs et jardins : remettre l\\u2019art du jardinage au c\\u0153ur des missions des agents. "
        "Ouvrir tous les squares aux chiens tenus en laisse (sauf aires de jeux enfants)"
    ),
    "peripherique": (
        "Relever la vitesse \\u00E0 80 km/h sur le p\\u00E9riph\\u00E9rique "
        "(infrastructure con\\u00E7ue pour 90 km/h, la limitation \\u00E0 50 km/h n\\u2019a r\\u00E9duit ni pollution ni bruit)"
    ),
    "proprete": (
        "Privatisation totale du ramassage des ordures m\\u00E9nag\\u00E8res (mod\\u00E8le Chirac 1983, -27% co\\u00FBt, 67,5 M\\u20AC/an d\\u2019\\u00E9conomie). "
        "Privatisation du nettoyage de la voirie (-25%, 16 M\\u20AC/an). "
        "Plan anti-rats : glace carbonique, pi\\u00E9geage intelligent, bacs \\u00E0 couvercle verrouill\\u00E9, "
        "QR codes sur poubelles pour signalement en temps r\\u00E9el"
    ),

    # === SÉCURITÉ & TRANQUILLITÉ ===
    "police-municipale": (
        "8 000 policiers municipaux arm\\u00E9s (contre 3 000 actuellement, +277 M\\u20AC/an). "
        "Brigade mont\\u00E9e \\u00E0 cheval (40 chevaux, 60 cavaliers). Brigade canine (30 chiens). "
        "IA vid\\u00E9osurveillance pour d\\u00E9tection automatique des agressions. "
        "Interpellations syst\\u00E9matiques. Reconqu\\u00EAte des zones de non-droit "
        "(Chapelle, Stalingrad, Goutte d\\u2019Or, Champ de Mars). "
        "500 policiers municipaux sur le r\\u00E9seau de transport"
    ),
    "eclairage-securite": (
        "R\\u00E9verb\\u00E8res intelligents anti-agression pilot\\u00E9s par IA "
        "(capteurs, lumi\\u00E8re intense en cas d\\u2019agression, alerte patrouille automatique, 8 000/an, 20 M\\u20AC/an). "
        "\\u00C9clairage LED toute la nuit. Vitrines commerciales \\u00E9clair\\u00E9es la nuit autoris\\u00E9es"
    ),

    # === DÉMOCRATIE & VIE DE QUARTIER ===
    "budget-participatif": (
        "Au moins 2 r\\u00E9f\\u00E9rendums locaux par an. R\\u00E9f\\u00E9rendum obligatoire pour tout projet > 10 M\\u20AC. "
        "Consultation locale + simulation sur maquette num\\u00E9rique (jumeau num\\u00E9rique de Paris) avant tout projet. "
        "Bilan trimestriel public de l\\u2019avancement"
    ),
    "vie-associative": (
        "R\\u00E9duction de 100 M\\u20AC/an des subventions aux associations politis\\u00E9es "
        "ou ne relevant pas de l\\u2019int\\u00E9r\\u00EAt municipal. Transparence totale sur les subventions"
    ),

    # === CULTURE & SPORT ===
    "musees-culture": (
        "Restauration du mobilier urbain historique (bancs Davioud, r\\u00E9verb\\u00E8res, grilles fonte, kiosques : 32,5 M\\u20AC/an). "
        "Plan de protection du patrimoine religieux (300 M\\u20AC sur le mandat). "
        "Abroger le PLUb, urbanisme au service du beau. "
        "S\\u00E9curiser les abords du Louvre. Terrasses chauff\\u00E9es autoris\\u00E9es. "
        "F\\u00EAte de la musique r\\u00E9serv\\u00E9e aux instruments et chanteurs"
    ),
    "sport": (
        "\\u00C9quipements sportifs ouverts de 7h \\u00E0 23h, ouverture dominicale g\\u00E9n\\u00E9ralis\\u00E9e. "
        "Partenariats entreprises pour cr\\u00E9neaux sous-utilis\\u00E9s. "
        "Terrains de sport sous le m\\u00E9tro a\\u00E9rien (padel, basket, foot). "
        "Vente du Parc des Princes au PSG (r\\u00E9f\\u00E9rendum)"
    ),

    # === GRAND PARIS & MÉTROPOLE ===
    "tarification-solidarite": (
        "Plan d\\u2019\\u00E9conomies de 10 milliards d\\u2019euros sur 10 ans. "
        "Division par 2 de la taxe fonci\\u00E8re (de 20,5% \\u00E0 10%, \\u00E9conomie de 950 M\\u20AC/an pour les Parisiens). "
        "Division par 2 de la taxe ordures m\\u00E9nag\\u00E8res et taxe de balayage (337 M\\u20AC/an). "
        "Baisse de 10% des frais de notaire. "
        "Remboursement du trop-per\\u00E7u de taxe fonci\\u00E8re (250 M\\u20AC). "
        "R\\u00E9duction des effectifs municipaux de 55 000 \\u00E0 28 000 en 10 ans. "
        "Division de la dette par 2 (de 10 Md\\u20AC \\u00E0 5 Md\\u20AC)"
    ),
}


def main():
    with open(APPJS, "r", encoding="utf-8") as f:
        content = f.read()

    # Trouver les bornes de la section Paris
    paris_start = content.find('"paris-2026": {')
    paris_end = content.find('"lyon-2026": {')
    if paris_start == -1 or paris_end == -1:
        print("ERREUR: section Paris non trouvée")
        return

    paris_section = content[paris_start:paris_end]
    new_section = paris_section

    # Construire le format JS pour source
    src = to_js(SOURCE)
    src_url = SOURCE_URL

    count_updated = 0
    count_new = 0

    for st_id, texte in MESURES.items():
        # Chercher le sous-thème dans la section Paris
        # Pattern: id: "st_id", suivi de propositions contenant knafo:
        pattern = f'id: "{st_id}"'
        pos = new_section.find(pattern)
        if pos == -1:
            print(f"  ATTENTION: sous-thème '{st_id}' non trouvé dans Paris")
            continue

        # Trouver knafo: dans ce sous-thème (chercher dans les ~2000 chars suivants)
        search_area = new_section[pos:pos+3000]

        # Chercher knafo: null ou knafo: { texte: "..." ... }
        knafo_null = search_area.find('knafo: null')
        knafo_obj_match = re.search(r'knafo: \{ texte: ".*?"(?:, source: ".*?"(?:, sourceUrl: ".*?")?)? \}', search_area)

        new_value = f'knafo: {{ texte: "{texte}", source: "{src}", sourceUrl: "{src_url}" }}'

        if knafo_null != -1 and knafo_null < 2000:
            # Remplacer knafo: null
            abs_pos = pos + knafo_null
            old = 'knafo: null'
            new_section = new_section[:abs_pos] + new_value + new_section[abs_pos + len(old):]
            count_new += 1
            print(f"  + {st_id}: ajouté (était null)")
        elif knafo_obj_match and knafo_obj_match.start() < 2000:
            # Remplacer knafo: { texte: "...", ... }
            abs_pos = pos + knafo_obj_match.start()
            old = knafo_obj_match.group(0)
            new_section = new_section[:abs_pos] + new_value + new_section[abs_pos + len(old):]
            count_updated += 1
            print(f"  ~ {st_id}: mis à jour")
        else:
            print(f"  ? {st_id}: knafo non trouvé dans le sous-thème")

    # Mettre à jour programmeComplet et programmePdfPath pour Knafo
    old_knafo_decl = new_section
    # Chercher la déclaration du candidat knafo
    knafo_cand = re.search(
        r'(\{ id: "knafo".*?programmeComplet: )false(.*?programmePdfPath: )null',
        new_section, re.DOTALL
    )
    if knafo_cand:
        new_section = (
            new_section[:knafo_cand.start(1)] +
            knafo_cand.group(1) + 'true' +
            knafo_cand.group(2) + '"Programme-Sarah-Knafo-Paris-2026.pdf"' +
            new_section[knafo_cand.end():]
        )
        print(f"\n  ✓ programmeComplet: true")
        print(f"  ✓ programmePdfPath: Programme-Sarah-Knafo-Paris-2026.pdf")

    # Reconstruire le fichier
    new_content = content[:paris_start] + new_section + content[paris_end:]

    with open(APPJS, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"\n=== Résultat ===")
    print(f"  {count_new} nouvelles entrées ajoutées")
    print(f"  {count_updated} entrées existantes mises à jour")
    print(f"  Total: {count_new + count_updated} modifications")


if __name__ == "__main__":
    main()
