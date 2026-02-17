#!/usr/bin/env python3
"""Met à jour suivi_candidats.csv avec les emails et Twitter trouvés par les agents."""
import csv
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'suivi_candidats.csv')

# Données trouvées par les 4 agents de recherche
# Format: (candidat_partiel, ville_partielle, email, type_email, twitter, source)
UPDATES = [
    # === AGENT IDF ===
    # Emails
    ("Senant", "Antony", "secretariat_elus@ville-antony.fr", "mairie", "@jysenant", "recherche web"),
    ("Precetti", "Antony", "perrine.precetti@ville-antony.fr", "institutionnel", None, "recherche web"),
    ("Aeschlimann", "Asnières", "info@mairieasnieres.fr", "mairie", "@maeschlimann", "recherche web"),
    ("Lagarde", "Drancy", "jean-christophe.lagarde@assemblee-nationale.fr", "institutionnel", "@jclagarde", "recherche web"),
    ("Bouyssou", "Ivry", "courrier@ivry94.fr", "mairie", "@pbouyssouivry", "recherche web"),
    ("Jeanne", "Champigny", "monsieur-le-maire@mairie-champigny94.fr", "mairie", "@LaurentJeanne94", "recherche web"),
    ("Fromantin", "Neuilly", "mr.lemaire@ville-neuillysurseine.fr", "mairie", "@JCFromantin", "recherche web"),
    ("Indjian", "Rueil", "patrick.indjian@mairie-rueilmalmaison.fr", "mairie", None, "recherche web"),
    ("Hanotin", "Saint-Denis", "mairie.saint.denis@ville-saint-denis.fr", "mairie", "@MathieuHanotin", "recherche web"),
    ("Bernalicis", "Villeneuve", "ugo.bernalicis@assemblee-nationale.fr", "institutionnel", "@Ugobernalicis", "recherche web"),
    ("Arthaud", "Pantin", "contact@lutte-ouvriere.org", "parti", "@n_arthaud", "recherche web"),
    ("Baguet", "Boulogne", "SCC@mairie-boulogne-billancourt.fr", "mairie", None, "recherche web"),
    # Twitter only IDF
    ("Mothron", "Argenteuil", None, None, "@GMothron", "recherche web"),
    ("Doucet", "Argenteuil", None, None, "@pdoucet", "recherche web"),
    ("Debeaud", "Argenteuil", None, None, "@FranckDebeaud", "recherche web"),
    ("Bougeard", "Argenteuil", None, None, "@nicolasbougeard", "recherche web"),
    ("Franclet", "Aubervilliers", None, None, "@francletkarine", "recherche web"),
    ("Lescaut", "Aubervilliers", None, None, "@GuillaumLescaut", "recherche web"),
    ("Karroumi", "Aubervilliers", None, None, "@KarroumiSo", "recherche web"),
    ("Djebbari", "Aubervilliers", None, None, "@NabilaDjebbari", "recherche web"),
    ("Daguet", "Aubervilliers", None, None, "@Anthony_Daguet", "recherche web"),
    ("Beschizza", "Aulnay", None, None, "@brunobeschizza", "recherche web"),
    ("Jerphanion", "Boulogne", None, None, "@2jerph", "recherche web"),
    ("Jeandon", "Cergy", None, None, "@Jp_Jeandon", "recherche web"),
    ("Léger", "Champigny", None, None, "@LEGERJulien94", "recherche web"),
    ("Muzeau", "Clichy", None, None, "@RMuzeau", "recherche web"),
    ("Chaimovitch", "Colombes", None, None, "@pchaimovitch", "recherche web"),
    ("Kossowski", "Courbevoie", None, None, "@jakossowski", "recherche web"),
    ("Taquillain", "Courbevoie", None, None, "@ATaquillain", "recherche web"),
    ("Pottier-Dumas", "Levallois", None, None, "@AgnesPottierD", "recherche web"),
    ("Messatfa", "Levallois", None, None, "@LiesMessatfa", "recherche web"),
    ("Bessac", "Montreuil", None, None, "@PatriceBessac", "recherche web"),
    ("Shahryari", "Montreuil", None, None, "@SaynaShahr", "recherche web"),
    ("Matouk", "Nanterre", None, None, "@helene_matouk", "recherche web"),
    ("Marsigny", "Noisy", None, None, "@B_Marsigny", "recherche web"),
    ("Monot", "Pantin", None, None, "@mat_monot", "recherche web"),
    ("Bardoux", "Pantin", None, None, "@BardouxThomas", "recherche web"),
    ("Carvalhinho", "Pantin", None, None, "@GeoffreyCarva", "recherche web"),
    ("Bagayoko", "Saint-Denis", None, None, "@BallyBagayoko", "recherche web"),
    ("Mazières", "Versailles", None, None, "@FdeMazieres", "recherche web"),
    ("La Faire", "Versailles", None, None, "@odelafr", "recherche web"),
    ("Clément", "Versailles", None, None, "@ClmentSabine", "recherche web"),
    ("Garzon", "Villejuif", None, None, "@PierreGarzon", "recherche web"),
    ("Caudron", "Villeneuve", None, None, "@CaudronGerard", "recherche web"),
    ("Burette", "Villeneuve", None, None, "@victorburette", "recherche web"),

    # === AGENT NORD/OUEST ===
    # Emails
    ("Jenlis", "Amiens", "nouslesamienois@hubertdejenlis.fr", "campagne", "@HubertdeJenlis", "recherche web"),
    ("Vergriete", "Dunkerque", "dunkenmouv@gmail.com", "campagne", "@P_Vergriete", "recherche web"),
    ("Guiraud", "Roubaix", "david@guiraud2026.fr", "campagne", "@GuiraudInd", "recherche web"),
    ("Becue", "Tourcoing", "dbecue@ville-tourcoing.fr", "institutionnel", "@DorianeBecue", "recherche web"),
    ("Assih", "Quimper", "isabelle.assih@quimper.bzh", "institutionnel", "@AssihIsabelle", "recherche web"),
    ("Menguy", "Quimper", "guillaume.menguy@quimper.bzh", "institutionnel", "@MenguyFr", "recherche web"),
    ("Lucas", "Saint-Nazaire", "sn26@mailo.com", "campagne", None, "recherche web"),
    ("Karamanli", "Le Mans", "contact@mariettakaramanli.fr", "campagne", "@MKaramanli72", "recherche web"),
    # Twitter only Nord/Ouest
    ("Fauvet", "Amiens", None, None, "@fredfauvet", "recherche web"),
    ("Caron", "Amiens", None, None, "@AurelienCARON", "recherche web"),
    ("Mercuzot", "Amiens", None, None, "@benoitmercuzot", "recherche web"),
    ("Toumi", "Amiens", None, None, "@DamienToumi", "recherche web"),
    ("Olivier", "Amiens", None, None, "@Samy_Olivier", "recherche web"),
    ("Dècle", "Amiens", None, None, "@PaulEricDecle", "recherche web"),
    ("Bouchart", "Calais", None, None, "@NatachaBouchart", "recherche web"),
    ("Fleurian", "Calais", None, None, "@MarcDeFleurian", "recherche web"),
    ("Garcin", "Roubaix", None, None, "@AlexandreGarcin", "recherche web"),
    ("Chalah", "Roubaix", None, None, "@MehdiChalah", "recherche web"),
    ("Sayah", "Roubaix", None, None, "@celinesayah_", "recherche web"),
    ("Vuylsteker", "Tourcoing", None, None, "@katyvuylsteker", "recherche web"),
    ("Verbrugghe", "Tourcoing", None, None, "@BVerbrugghe", "recherche web"),
    ("Cuillandre", "Brest", None, None, "@FCuillandre", "recherche web"),
    ("Loher", "Lorient", None, None, "@FabriceLoher", "recherche web"),
    ("Hénaff", "Quimper", None, None, "@Christel_Henaff", "recherche web"),
    ("Falorni", "La Rochelle", None, None, "@olivierfalorni", "recherche web"),
    ("Le Foll", "Le Mans", None, None, "@SLeFoll", "recherche web"),
    ("Sasso", "Le Mans", None, None, "@olsasso", "recherche web"),
    ("Béchu", "Angers", None, None, "@ChristopheBechu", "recherche web"),
    ("Laveau", "Angers", None, None, "@RomainLaveau", "recherche web"),
    ("Saeidi", "Angers", None, None, "@arashsaeidi", "recherche web"),
    ("Denis", "Tours", None, None, "@EmmanuelDenis37", "recherche web"),
    ("Alfandari", "Tours", None, None, "@Henri_Alfandari", "recherche web"),
    ("Bouchet", "Tours", None, None, "@ch_bouchet", "recherche web"),
    ("Nikolic", "Tours", None, None, "@Al_Nikolic", "recherche web"),
    ("Quinton", "Tours", None, None, "@MarieQuinton8", "recherche web"),
    ("Baloge", "Niort", None, None, "@JeromeBaloge", "recherche web"),
    ("Moncond", "Poitiers", None, None, "@L_Moncondhuy", "recherche web"),
    ("Blanchard", "Poitiers", None, None, "@FraBlanchard", "recherche web"),

    # === AGENT EST/CENTRE ===
    # Emails
    ("Frigout", "Reims", "contact@frigout2026.fr", "campagne", "@asfrigout", "recherche web"),
    ("Mertz", "Metz", "bertrandmertz2026@gmail.com", "campagne", None, "recherche web"),
    ("Haberstrau", "Dijon", "contact@dijonchangedere.fr", "campagne", None, "recherche web"),
    ("Minard", "Dijon", "municipales_lfi_dijon@protonmail.com", "campagne", None, "recherche web"),
    ("Koenders", "Dijon", "nathalie.koenders@cotedor.fr", "institutionnel", "@nkoenders", "recherche web"),
    ("Lacresse", "Nancy", "emmanuel.lacresse@assemblee-nationale.fr", "institutionnel", "@E_LACRESSE", "recherche web"),
    ("Klein", "Nancy", "maire@nancy.fr", "institutionnel", "@mathieuklein", "recherche web"),
    ("Mendes", "Metz", "ludovic.mendes@assemblee-nationale.fr", "institutionnel", "@LudovicMDS", "recherche web"),
    ("Delabrousse", "Besançon", "eric.delabrousse@univ-fcomte.fr", "universitaire", None, "recherche web"),
    ("Mayer-Rossignol", "Rouen", "cabinetdumaire@rouen.fr", "institutionnel", "@NicolasMayerNMR", "recherche web"),
    ("Aristide", "Caen", "aristide.olivier@normandie.fr", "institutionnel", "@AristideOlivier", "recherche web"),
    ("Orphelin", "Caen", "rudy.lorphelin@normandie.fr", "institutionnel", "@rudylorphelin", "recherche web"),
    ("Galut", "Bourges", "yann.galut@ville-bourges.fr", "institutionnel", "@yanngalut", "recherche web"),
    ("Mercier", "Bourges", "philippe-mercier@altajuris.com", "professionnel", None, "recherche web"),
    # Twitter only Est/Centre
    ("Straumann", "Colmar", None, None, "@ericstraumann", "recherche web"),
    ("Hémedinger", "Colmar", None, None, "@YvesHemedinger", "recherche web"),
    ("Aubert", "Colmar", None, None, "@Nath_Aubert65", "recherche web"),
    ("Lutz", "Mulhouse", None, None, "@michelelutzh", "recherche web"),
    ("Million", "Mulhouse", None, None, "@million_lara", "recherche web"),
    ("Minery", "Mulhouse", None, None, "@loic_minery", "recherche web"),
    ("Ritz", "Mulhouse", None, None, "@christelleritz", "recherche web"),
    ("Taffarelli", "Mulhouse", None, None, "@manutaffarelli", "recherche web"),
    ("Sornin", "Mulhouse", None, None, "@cecilesornin", "recherche web"),
    ("Hénart", "Nancy", None, None, "@LaurentHenart", "recherche web"),
    ("Roques", "Metz", None, None, "@JereRoques", "recherche web"),
    ("Leduc", "Metz", None, None, "@CharlotteLeducV", "recherche web"),
    ("Robinet", "Reims", None, None, "@ArnaudRobinet", "recherche web"),
    ("Mura", "Reims", None, None, "@sebastienmura", "recherche web"),
    ("Lang", "Reims", None, None, "@stephanelang51", "recherche web"),
    ("Beury", "Troyes", None, None, "@L_Beury", "recherche web"),
    ("Fraincart", "Troyes", None, None, "@FraincartSarah", "recherche web"),
    ("Bichot", "Dijon", None, None, "@emmanuelbichot", "recherche web"),
    ("Coudert", "Dijon", None, None, "@thierrycoudert", "recherche web"),
    ("Iannuzzi", "Bourges", None, None, "@ugo_flcn", "recherche web"),
    ("Grouard", "Orléans", None, None, "@SergeGrouard", "recherche web"),
    ("Grand", "Orléans", None, None, "@jphgrand", "recherche web"),
    ("Pelé", "Orléans", None, None, "@ValentinPeleFI", "recherche web"),
    ("Janvier", "Orléans", None, None, "@CarolineJanvier", "recherche web"),
    ("Caron", "Rouen", None, None, "@Marine_Caron76", "recherche web"),
    ("Da Silva", "Rouen", None, None, "@Maxime_DaSilva_", "recherche web"),
    ("Houdan", "Rouen", None, None, "@gregoirehoudan", "recherche web"),
    ("Chevalier", "Caen", None, None, "@TChevalier_", "recherche web"),

    # === AGENT SUD/OUTREMER ===
    # Emails
    ("Péna", "Aix", "marc.pena@assemblee-nationale.fr", "institutionnel", "@MarcPena_", "recherche web"),
    ("Armand", "Annecy", "antoine.armand@assemblee-nationale.fr", "institutionnel", "@antoine_armand", "recherche web"),
    ("Carignon", "Grenoble", "alain.carignon@grenoble.fr", "institutionnel", "@CarignonAlain", "recherche web"),
    ("Cinieri", "Saint-Étienne", "depute@dinocinieri.fr", "institutionnel", "@DinoCinieri", "recherche web"),
    ("Valentine Mercier", "Saint-Étienne", "mercier2026@etik.com", "campagne", None, "recherche web"),
    ("Delafosse", "Montpellier", "contact@michaeldelafosse.fr", "campagne", "@MDelafosse", "recherche web"),
    ("Jamet", "Montpellier", "france.jamet@europarl.europa.eu", "institutionnel", "@FranceJamet", "recherche web"),
    ("Roumegas", "Montpellier", "jean-louis.roumegas@assemblee-nationale.fr", "institutionnel", "@jlroumegas", "recherche web"),
    ("Oziol", "Montpellier", "nathalie.oziol@assemblee-nationale.fr", "institutionnel", "@NathalieOziol", "recherche web"),
    ("Ménard", "Béziers", "com@ville-beziers.fr", "mairie", "@RobertMenardFR", "recherche web"),
    # Twitter only Sud/Outremer
    ("Rigault", "Avignon", None, None, "@as_rigaultrn", "recherche web"),
    ("Lisnard", "Cannes", None, None, "@davidlisnard", "recherche web"),
    ("Bonnemain", "Fréjus", None, None, "@ebonnemain2020", "recherche web"),
    ("Rachline", "Fréjus", None, None, "@david_rachline", "recherche web"),
    ("Mansour", "La Seyne", None, None, "@Mansourcheikh83", "recherche web"),
    ("Roit", "Annecy", None, None, "@Gui_RoitLeveque", "recherche web"),
    ("Bernard", "Chambéry", None, None, "@B_Bernard73", "recherche web"),
    ("Patey", "Chambéry", None, None, "@VincentPatey", "recherche web"),
    ("Gerbi", "Grenoble", None, None, "@gerbiherve", "recherche web"),
    ("Le Jaouen", "Saint-Étienne", None, None, "@EricLeJaouen", "recherche web"),
    ("Christophle", "Valence", None, None, "@paulchristophle", "recherche web"),
    ("Aliot", "Perpignan", None, None, "@louis_aliot", "recherche web"),
    ("Ripoull", "Perpignan", None, None, "@clotilderipoull", "recherche web"),
    ("Bayrou", "Pau", None, None, "@bayrou", "recherche web"),
    ("Miguel", "Limoges", None, None, "@MiguelThierry2", "recherche web"),
    ("Léonie", "Limoges", None, None, "@vincentleonie", "recherche web"),
]


def normalize(s):
    """Normalise pour comparaison insensible aux accents/casse."""
    import unicodedata
    s = s.lower().strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s


def match_candidate(row_candidat, row_ville, search_name, search_ville):
    """Vérifie si une ligne CSV correspond à un candidat recherché."""
    norm_candidat = normalize(row_candidat)
    norm_ville = normalize(row_ville)
    norm_search = normalize(search_name)
    norm_search_ville = normalize(search_ville)

    # Le nom de recherche doit apparaître dans le nom du candidat
    if norm_search not in norm_candidat:
        return False

    # La ville de recherche doit apparaître dans la ville CSV
    if norm_search_ville not in norm_ville:
        return False

    return True


def main():
    # Lire le CSV
    rows = []
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    updates_count = 0
    emails_added = 0
    twitter_added = 0
    not_found = []

    for search_name, search_ville, email, type_email, twitter, source in UPDATES:
        found = False
        for row in rows:
            if match_candidate(row['candidat'], row['ville'], search_name, search_ville):
                found = True
                updated = False

                # Ajouter email si pas déjà présent et qu'on en a un
                if email and not row.get('email'):
                    row['email'] = email
                    row['type_email'] = type_email or ''
                    row['source_contact'] = source
                    row['statut_contact'] = 'EMAIL OK'
                    emails_added += 1
                    updated = True

                # Ajouter twitter si pas déjà présent et qu'on en a un
                if twitter and not row.get('twitter'):
                    row['twitter'] = twitter
                    if not updated:
                        row['source_contact'] = source
                    # Si on a un twitter mais pas d'email, marquer TWITTER OK
                    if not row.get('email') and not email:
                        row['statut_contact'] = 'TWITTER OK'
                    elif row.get('email') or email:
                        row['statut_contact'] = 'EMAIL OK'
                    twitter_added += 1
                    updated = True

                if updated:
                    updates_count += 1
                break

        if not found:
            not_found.append(f"{search_name} ({search_ville})")

    # Écrire le CSV mis à jour
    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

    # Stats
    total = len(rows)
    with_email = sum(1 for r in rows if r.get('email'))
    with_twitter = sum(1 for r in rows if r.get('twitter'))
    with_contact = sum(1 for r in rows if r.get('email') or r.get('twitter'))

    print(f"\n=== MISE À JOUR TERMINÉE ===")
    print(f"Lignes mises à jour : {updates_count}")
    print(f"Emails ajoutés : {emails_added}")
    print(f"Twitter ajoutés : {twitter_added}")
    print(f"\n=== STATS GLOBALES ===")
    print(f"Total candidats : {total}")
    print(f"Avec email : {with_email} ({with_email*100//total}%)")
    print(f"Avec Twitter : {with_twitter} ({with_twitter*100//total}%)")
    print(f"Avec au moins un contact : {with_contact} ({with_contact*100//total}%)")
    print(f"Sans aucun contact : {total - with_contact} ({(total-with_contact)*100//total}%)")

    if not_found:
        print(f"\n=== NON TROUVÉS ({len(not_found)}) ===")
        for name in not_found:
            print(f"  - {name}")


if __name__ == '__main__':
    main()
