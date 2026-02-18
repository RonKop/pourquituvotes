#!/usr/bin/env python3
"""
Intégration du programme complet de Rachida Dati (Paris)
Source : PDF 32 pages "Mon projet pour changer Paris en mieux"
URL : https://rachidadati2026.com/dossiers_de_presse/dossier-de-presse-programme-rachida-dati/
"""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DATA_FILE = r"C:\Users\KOPELMANRon\Downloads\FR comp mun\data\elections\paris-2026.json"
SOURCE = "Programme officiel 2026 (PDF 32 pages)"
SOURCE_URL = "https://rachidadati2026.com/dossiers_de_presse/dossier-de-presse-programme-rachida-dati/"

PROPOSITIONS = {
    "securite": {
        "police-municipale": "5 000 agents de police municipale armés, formés et connectés, déployés jour et nuit dans tous les quartiers. Élargissement des compétences : contrôle d'identité, accès aux fichiers nationaux, traitement de la petite délinquance. Convention avec Île-de-France Mobilités pour intervention dans les transports en commun.",
        "videoprotection": "Doublement du réseau de vidéoprotection à 8 000 caméras, reliées à un Centre de Supervision Urbain unique avec antenne dans chaque arrondissement. Vidéoprotection prioritaire aux abords des écoles, collèges, terrains de sport et piscines. Bouclier de Sécurité : aide au financement de vidéoprotection et alarmes pour commerces et cabinets médicaux.",
        "prevention-mediation": "Sécurisation des immeubles sociaux (équipes de sécurité chez les bailleurs, caméras dans les parties communes). Brigades de Sécurité dans les Collèges composées de médiateurs et éducateurs contre le harcèlement et les rixes. Sécurisation des passages urbains (tunnels, ponts, portes de Paris). Lutte contre le trafic et la consommation de crack : centres de soins hors zones denses, transformation des CAARUD/CSAPA en pôles de soins intégrés.",
        "violences-femmes": "Dispositif de sécurisation du bois de Vincennes et du bois de Boulogne : deux antennes de police municipale dédiées avec brigades équestres, caméras et éclairage intelligent. Plan de sécurisation du Champ de Mars : clôture du site, fermeture nocturne, antenne dédiée contre le commerce illégal, les vols à la tire et les agressions."
    },
    "transports": {
        "transports-en-commun": "Schéma de circulation global à l'échelle de Paris intégrant les enjeux métropolitains. Rétablissement des 70 km/h sur le périphérique après pose d'enrobés phoniques. Investissement pour la mise en accessibilité du métro (Ligne 6 en priorité). Parkings relais gardés aux portes de Paris, connectés aux métros et bus, avec tarif unique abordable.",
        "velo-mobilites-douces": "Préservation et renforcement des pistes cyclables sur les axes sous-dotés (axe nord-sud), parcours longs et sécurisés. Vélib entièrement régional en partenariat avec la Région, en site propre. Essor des véhicules électriques : aides à l'achat, places réservées, plan de bornes de recharge dans chaque quartier (couverture intégrale d'ici fin de mandat).",
        "pietons-circulation": "Grandes traversées urbaines réservées aux piétons : rénovation et élargissement des trottoirs. Quais bas de Seine réservés aux piétons (grand parc urbain patrimonial). Rue de Rivoli rééquilibrée : trottoirs élargis, piste cyclable bidirectionnelle sécurisée, voie bus et voie de desserte locale. Fin du provisoire : séquençage annuel des projets structurants.",
        "stationnement": "Nouveau tarif résident unique pour stationner dans tout Paris (pas uniquement son quartier). Gratuité du stationnement pour les deux-roues motorisés sur emplacements réservés. Places réservées pour véhicules électriques. Stationnement gratuit pour les professionnels de santé intervenant à domicile.",
        "tarifs-gratuite": "Fin de la ZTL Paris-Centre. Tarif unique abordable pour les parkings relais aux portes de Paris. Tarif résident abordable pour que les familles puissent circuler et se garer sans coût confiscatoire."
    },
    "logement": {
        "logement-social": "Priorisation des travailleurs essentiels (soignants, police, éducateurs) et familles pour le logement social. Contrôle strict de l'occupation : vérification régulière des ressources et de la composition du foyer, mobilité vers logements adaptés et accession sociale à la propriété. Tolérance zéro pour les fauteurs de trouble : expulsion du parc social. Gel de la production de nouveaux logements sociaux via préemption, redéploiement de 100 M\u20ac/an vers la réhabilitation du parc existant.",
        "logements-vacants": "Transformation de bureaux vides en logements. Remise sur le marché du patrimoine non-stratégique de la Ville pour projets privés abordables. Encadrement d'Airbnb : blocage des transformations en locations professionnelles à l'année, accompagnement juridique des copropriétaires souhaitant interdire la location courte durée.",
        "encadrement-loyers": "Assouplissement de l'encadrement des loyers pour les logements revenant sur le marché après vacance. Assouplissement des plafonds pour les logements sortant des étiquettes F et G après rénovation énergétique (gain de 2 échelons). Stabilité de la taxe foncière comme signal aux bailleurs et investisseurs.",
        "acces-logement": "Prêt à taux zéro de 10 000 à 50 000\u20ac pour les familles déménageant pour accueillir un nouvel enfant. Production accrue de logements intermédiaires pour jeunes actifs via modification du PLU. Suppression des pastillages qui menacent les logements privés de transformation imposée en logements sociaux. Révision du PLU pour desserrer les contraintes quartier par quartier."
    },
    "education": {
        "petite-enfance": "100 % des places en crèche pourvues : personnels des crèches prioritaires pour le logement social. Horaires d'accueil élargis (tôt le matin, tard le soir) dans les crèches et écoles pour les parents en horaires décalés et les 31 % de familles monoparentales parisiennes.",
        "ecoles-renovation": "Grand plan de rénovation et d'équipement des écoles (budget passé de 152 à 77 M\u20ac sous la majorité sortante). Révision du forfait communal pour les écoles maternelles privées sous contrat, revalorisation pour les élémentaires. 100 % des élèves avec accès à l'éducation artistique et culturelle (socle commun EAC).",
        "cantines-fournitures": "Alimentation saine et équilibrée dès l'école : programmes d'éducation nutritionnelle et repas équilibrés en circuits-courts saisonniers dans les cantines.",
        "periscolaire-loisirs": "Semaine de 4 jours (lundi-mardi-jeudi-vendredi, 8h30-16h30). Mercredi sanctuarisé pour temps périscolaire de qualité avec animateurs mieux diplômés et contrôlés. Études dirigées après l'école pour les élèves en difficulté (mesure de justice sociale).",
        "jeunesse": "Nouveaux points 'Quartier Jeunes' pour les 16-30 ans : accompagnement en santé mentale, accès aux droits et insertion. Foncier libéré (écoles, collèges fermés) transformé en lieux dédiés à la jeunesse. Résidences d'artistes dans les écoles, conventions avec universités pour cursus d'excellence (IA, deeptech, quantique)."
    },
    "environnement": {
        "espaces-verts": "Préservation des 200 000 arbres de Paris et 300 000 arbres des Bois (aucun abattage sauf état phytosanitaire). 500 nouvelles bandes végétalisées. Débitumisation et retour des grilles Davioud pour préserver les racines. Végétalisation grimpante, désartificialisation des cours d'écoles et cœurs d'îlot.",
        "proprete-dechets": "Réorganisation de la direction de la propreté avec autorité aux maires d'arrondissement. Privatisation de la collecte des déchets ménagers pour un service uniforme. Brigades de la propreté : équipes d'intervention d'urgence plusieurs fois par jour. Tolérance zéro : verbalisation renforcée contre dépôts sauvages et tags. Grand plan de lutte contre les 6 millions de rats (glace carbonique, pièges écologiques connectés).",
        "climat-adaptation": "Débitumisation pour créer des îlots de fraîcheur (objectif -3°C dans les rues l'été). Paris 'ville éponge' : diagnostic par quartier, pavés enherbés, revêtements infiltrants. Plan 'Urgence Fours Urbains' : rafraîchissement des 100 sites les plus chauds, doublement des bâtiments raccordés au réseau Fraîcheur de Paris. Interdiction des projets créant des îlots de chaleur. Brumisateurs dans les parcs, 2 miroirs d'eau sur les quais de Seine.",
        "renovation-energetique": "Chantier du siècle : 54 % des logements parisiens sont des passoires thermiques (E, F, G). Interlocuteur unique pour les copropriétés, renforcement de l'Agence Parisienne du Climat. 10 000 rénovations de logements sociaux/an. 25 % des résidences raccordées aux réseaux de chaleur/fraîcheur d'ici 2032. 30 % de toitures solaires lors des grosses rénovations. Modernisation de l'éclairage public intelligent. Doublement de la couverture en panneaux solaires (164 000 m\u00b2).",
        "alimentation-durable": "Alimentation saine et équilibrée dès l'école via programmes d'éducation et repas en circuits-courts saisonniers. Contrôle trimestriel des bâtiments publics contre les nuisibles (rats, moustiques)."
    },
    "sante": {
        "centres-sante": "Plan de désengorgement des urgences et lutte contre les déserts médicaux sur certaines spécialités. Aide à l'installation de maisons de santé et centres de soins non programmés. 'Bus des Femmes' parisiens dédiés à la prévention et aux soins primaires (contraception, dépistage IST, frottis, mammographies) dans les quartiers les plus difficiles d'accès.",
        "prevention-sante": "Campagnes de dépistage pour maladies chroniques (respiratoires, cardiovasculaires, cancers, santé mentale). Contrôle trimestriel des bâtiments publics contre les nuisibles. Lutte contre les pollutions sonores et lumineuses : objectif de réduction de moitié des nuisances sonores d'ici 2032. Droit au sommeil garanti : médiateurs de quartier, terrasses soumises à permis à points.",
        "seniors": "Système de veille solidaire (agents publics, gardiens, commerçants, voisins) pour accompagner les personnes isolées. Soins à domicile facilités : stationnement gratuit pour les professionnels de santé intervenant à domicile. Aménagements adaptés aux personnes âgées dans l'espace public (assises, îlots de fraîcheur, prévention des chutes près des EHPAD)."
    },
    "democratie": {
        "budget-participatif": "Renforcement du pouvoir budgétaire des mairies d'arrondissement (3 % actuellement) pour davantage d'investissements localisés. Autorité fonctionnelle et hiérarchique des maires d'arrondissement sur les services déconcentrés : compétences en urbanisme, logements sociaux, voirie, propreté avec dotations appropriées.",
        "transparence": "Création d'une Direction permanente de l'évaluation et de la performance pour auditer chaque euro dépensé. Contrôle systématique des subventions et programmes non obligatoires. Maîtrise du train de vie de la mairie : contrôle strict des notes de frais et déplacements des élus. Commission indépendante de contrôle des subventions associatives.",
        "vie-associative": "Réorientation des subventions vers les associations agissant pour les Parisiens, fin de l'opacité. Mise à disposition d'espaces de réunion et moyens logistiques, plateforme de réservation de locaux dans les bâtiments publics. Rétablissement de la neutralité politique des subventions : fin des subventions militantes et de la préférence pour les arrondissements acquis à l'exécutif.",
        "services-publics": "Choc de gestion : réduction des dépenses de fonctionnement de 3 %/an (~275-300 M\u20ac). Application des 35h réellement travaillées (contre 32h actuelles). Règle d'or RH : effectifs alignés sur la courbe démographique (1 agent/39 habitants vs 1/107 à Londres). Non-remplacement partiel des départs en retraite. Prime au mérite renforcée pour les agents les plus engagés."
    },
    "economie": {
        "commerce-local": "Guichet unique pour implantations commerciales, artisanales et industrielles. Principe 'dites-le-nous une fois' : un seul dossier partagé entre services. Délais garantis de 3 semaines (silence vaut acceptation). Exonération de CFE pour les locaux vacants depuis plus de 2 ans. Marchés éphémères de quartier. Collecte mutualisée pour commerces. Étude d'impact sur le commerce pour chaque projet d'aménagement.",
        "emploi-insertion": "'Small Parisian Business Act' : faciliter l'accès des TPE-PME aux marchés publics via allotissement et procédures simplifiées. Pôles parisiens du numérique et de l'IA (entreprises, écoles, universités). Cours d'Adultes de Paris centrés sur compétences commerciales (langues, accueil, numérique, gestion). 1 % du budget d'investissement aux 'preuves de concept' pour entrepreneurs.",
        "attractivite": "Points de détaxe immédiate dans les quartiers touristiques (seuil abaissé de 100\u20ac à 50\u20ac). Signalétique multilingue renforcée (en lien avec la RATP). Labels 'Fabriqué à Paris' et 'Paris Business' pour dynamiser tourisme et commerce. Fonds Parisien pour l'Innovation pour faire de Paris un leader de la Smart City."
    },
    "culture": {
        "equipements-culturels": "Bibliothèques et médiathèques ouvertes systématiquement le dimanche avec horaires élargis. 2 000 places supplémentaires dans les conservatoires d'ici 2027 (priorité : 15e, 16e, 18e, 19e, 20e). Conservatoire 'hors les murs' : cours hebdomadaires dans les écoles des quartiers prioritaires. Espace culturel immersif au musée Carnavalet. 'Villa Médicis' du design sur l'ex-Mairie du 1er. Nocturnes hebdomadaires dans les grands musées municipaux.",
        "evenements-creation": "Nuit blanche des enfants (5-12 ans, 2 fois/an, 18h-minuit). Grand orchestre parisien des collèges des 17 arrondissements (3 concerts/an à la Philharmonie et Opéra Bastille). Festival populaire des arts vivants avec remise de prix. 20 toits-terrasses transformés en lieux de diffusion culturelle estivale gratuite. Œuvres d'art contemporain tournantes dans chaque square. Programmation culturelle dédiée aux Parisiens des outre-mer au Cent-Quatre."
    },
    "sport": {
        "equipements-sportifs": "Audit d'infrastructure et plan de modernisation des équipements sportifs. Rénovation prioritaire des piscines municipales vétustes. Négociation vente du Parc des Princes au PSG en contrepartie d'un village sportif et culturel ouvert aux associations et Parisiens. Plus de créneaux sur des plages horaires élargies. Fin des réquisitions intempestives des gymnases.",
        "sport-pour-tous": "Sport accessible à tous sans exception : créneaux réservés au sport adapté et sport-santé. Développement du sport féminin à Paris."
    },
    "urbanisme": {
        "amenagement-urbain": "Charte 'Paris du Beau' pour espaces publics et opérations d'aménagement. Réhabilitation du mobilier haussmannien (fontaines Wallace, colonnes Morris). Commission du Mobilier Urbain réactivée (pas réunie depuis 2011). Transformation des quais de Seine en grand parc urbain patrimonial (bancs Davioud, matériaux nobles). Végétalisation de la place de la République avec retour des fontaines aux dauphins. Concours architectural pour les portes de Paris. Retrait des palissades sous 7 jours. Plan d'urgence pour le patrimoine (églises, lieux cultuels).",
        "accessibilite": "Mise en accessibilité du métro pour les personnes handicapées (Ligne 6 en priorité). Espaces accessibles aux chiens dans les parcs (caniparcs avec double porte, enherbés). Opérations d'aménagement adaptées aux personnes âgées et PMR (assises, prévention des chutes). Amende de non-ramassage des déjections canines relevée de 135\u20ac à 300\u20ac.",
        "quartiers-prioritaires": "Obligations renforcées de végétalisation et d'adaptation climatique des QPV surminéralisés. Contrôle accru des nuisances automobiles : revêtements phoniques, radars 'méduses' contre le bruit. Limitation des nuisances liées aux travaux : interdiction soirs et week-ends (hors urgences), charte des chantiers à faible nuisance."
    },
    "solidarite": {
        "aide-sociale": "Maisons de la parentalité : extension des PMI au-delà de 6 ans pour accompagner les parents (conseils, aide recherche de professionnels). Animateurs formés à la mission AESH pour les enfants handicapés. Guichet unique MDPH effectif. Chèque vétérinaire pour les plus démunis via les Maisons des Solidarités.",
        "egalite-discriminations": "'Bus des Femmes' pour la prévention et les soins primaires dans les quartiers difficiles d'accès. Encadrement des terrasses et droit au sommeil garanti pour lutter contre les nuisances. Programmation culturelle valorisant les Parisiens des outre-mer.",
        "pouvoir-achat": "Pas de nouveaux impôts, stabilité de la taxe foncière. Prêt à taux zéro pour déménagement familial (10 000 à 50 000\u20ac). Fin des préemptions (250 M\u20ac/an économisés). Réduction progressive des dépenses de fonctionnement de 3 %/an. Colombariums pour urnes funéraires d'animaux, crémation à prix coûtant."
    }
}

def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Update candidate metadata
    for c in data['candidats']:
        if c['id'] == 'dati':
            c['programmeComplet'] = True
            c['programmeUrl'] = SOURCE_URL
            c['programmePdfPath'] = "dati-paris-programme.pdf"
            c['liste'] = "LR - UDI"
            print(f"Updated candidate: {c['nom']}")
            break

    # Insert/update proposals
    updated = 0
    new = 0
    errors = 0

    for cat in data['categories']:
        cat_id = cat['id']
        if cat_id not in PROPOSITIONS:
            continue
        for st in cat['sousThemes']:
            st_id = st['id']
            if st_id not in PROPOSITIONS.get(cat_id, {}):
                continue

            texte = PROPOSITIONS[cat_id][st_id]
            prop = {
                "texte": texte,
                "source": SOURCE,
                "sourceUrl": SOURCE_URL
            }

            if 'propositions' not in st:
                st['propositions'] = {}

            if 'dati' in st['propositions'] and st['propositions']['dati'] is not None:
                updated += 1
            else:
                new += 1

            st['propositions']['dati'] = prop

    # Clean up any remaining None values
    for cat in data['categories']:
        for st in cat['sousThemes']:
            props = st.get('propositions', {})
            if 'dati' in props and props['dati'] is None:
                del props['dati']
                print(f"  Cleaned None: {cat['id']}/{st['id']}")

    # Save
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nResults: Updated={updated}, New={new}, Errors={errors}")
    total = updated + new
    print(f"Total sub-themes covered: {total}")

if __name__ == '__main__':
    main()
