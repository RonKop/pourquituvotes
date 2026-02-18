#!/usr/bin/env python3
"""
Intégration du programme complet de Thierry Mariani (Paris) - PDF 24 pages
Source : https://irp.cdn-website.com/f6a2da30/files/uploaded/programme+complet-e894cac7.pdf
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "elections")
JSON_PATH = os.path.join(DATA_DIR, "paris-2026.json")

CANDIDAT_ID = "mariani"
SOURCE = "Programme officiel 2026 (PDF)"
SOURCE_URL = "https://www.mariani-2026.fr/Le-programme"

# Metadata updates
METADATA = {
    "programmeComplet": True,
    "programmeUrl": "https://www.mariani-2026.fr/Le-programme",
    "programmePdfPath": "mariani-paris-programme.pdf",
    "liste": "RN - UDR",
    "soutiens": "Marine Le Pen, Jordan Bardella, Marion Mar\u00e9chal, \u00c9ric Ciotti"
}

# Propositions mapped to sub-themes (category_id -> sub_theme_id -> texte)
PROPOSITIONS = {
    "securite": {
        "police-municipale": (
            "Police municipale arm\u00e9e de 8 350 agents (ratio de 4 pour 1 000 habitants, mod\u00e8le New York). "
            "15 000 cam\u00e9ras de vid\u00e9oprotection (144 cam/km\u00b2, moyenne europ\u00e9enne). "
            "Patrouilles 24h/24 dans les zones sensibles. "
            "Renforcement des pr\u00e9rogatives avec recours encadr\u00e9 aux drones et IA. "
            "D\u00e9l\u00e9gation de pouvoirs de s\u00e9curit\u00e9 aux mairies d'arrondissement (\u00ab police d'arrondissement \u00bb). "
            "Renforcement de l'\u00e9clairage public LED apr\u00e8s audit complet du territoire. "
            "Mobilier urbain anti-vandalisme et rev\u00eatements anti-tag"
        ),
        "videoprotection": (
            "Tripler le parc pour atteindre 15 000 cam\u00e9ras (144 cam/km\u00b2). "
            "Vid\u00e9oprotection dans le logement social (sur vote des locataires). "
            "Cam\u00e9ras mobiles d\u00e9ployables rapidement pour cibler les zones de deal. "
            "Dispositif \u00ab Voisins vigilants \u00bb sur tout Paris. "
            "Boutons d'alerte pour cr\u00e8ches, \u00e9coles et commer\u00e7ants. "
            "Vid\u00e9oprotection pour s\u00e9curiser abords des \u00e9coles, jardins et parcs"
        ),
        "prevention-mediation": (
            "7 brigades sp\u00e9cialis\u00e9es : anti-squat (intervention sous 48h), transports, anti-campements, "
            "anti-drogue, circulation, brigade d'action rapide (BAR) et police d'arrondissement. "
            "Zones de S\u00e9curit\u00e9 Prioritaires (ZSP) avec antennes de police et permanences mobiles. "
            "Tol\u00e9rance z\u00e9ro face au trafic de drogue et aux points de deals. "
            "Supprimer les salles de shoot et ouvrir un centre de soin unique. "
            "Principe \u00ab casseur-payeur \u00bb. Suppression des allocations municipales pour familles d'un membre condamn\u00e9"
        ),
        "violences-femmes": (
            "R\u00e9sidences s\u00e9curis\u00e9es pour victimes de violences conjugales (au moins une par arrondissement) "
            "avec aide juridique municipale. "
            "Patrouilles renforc\u00e9es dans les transports contre les violences sexuelles et le harc\u00e8lement. "
            "Pr\u00e9sence de nuit de la police municipale \u00e0 proximit\u00e9 des rues festives. "
            "Pr\u00e9sence permanente dans les bois de Boulogne et Vincennes"
        )
    },
    "transports": {
        "transports-en-commun": (
            "Ouverture des lignes de m\u00e9tro automatiques la nuit, les vendredis et samedis soir. "
            "D\u00e9velopper les navettes de proximit\u00e9 inter-arrondissements. "
            "Audit des d\u00e9penses et retard du Grand Paris Express et rationalisation des travaux"
        ),
        "velo-mobilites-douces": (
            "Moratoire et audit des nouvelles pistes cyclables afin de les s\u00e9curiser "
            "ou de revoir la r\u00e9partition de l'espace (comme rue de Rivoli)"
        ),
        "pietons-circulation": (
            "Faire strictement respecter le code de la route. "
            "R\u00e9viser le plan de circulation pour prot\u00e9ger pi\u00e9tons, cyclistes et automobilistes. "
            "Supprimer la Zone \u00e0 Trafic Limit\u00e9 dans le centre de Paris. "
            "Revenir \u00e0 90 km/h sur le p\u00e9riph\u00e9rique. Retour des 50 km/h sur les grands axes. "
            "Policiers municipaux pour fluidifier la circulation aux axes cl\u00e9s"
        ),
        "stationnement": (
            "Refuser les tarifs discriminatoires, supprimer le zonage pour les Parisiens. "
            "R\u00e9duire le Forfait Post-Stationnement. "
            "20 000 nouvelles places de stationnement sur le mandat. "
            "Gratuit\u00e9 du stationnement dans les parcs. "
            "R\u00e9tablir la gratuit\u00e9 pour les 2 roues motoris\u00e9s (retour ante-2022). "
            "Stationnement temporaire gratuit"
        ),
        "tarifs-gratuite": (
            "Gratuit\u00e9 du stationnement dans les parcs pour les familles. "
            "Gratuit\u00e9 pour les 2 roues motoris\u00e9s. "
            "Rendre les transports en commun accessibles aux chiens avec r\u00e9glementation simplifi\u00e9e"
        )
    },
    "logement": {
        "logement-social": (
            "Priorit\u00e9 nationale dans l'acc\u00e8s au logement social. "
            "R\u00e9tablir l'ordre dans les HLM : convention locataire permettant l'expulsion des d\u00e9linquants et trafiquants. "
            "Plan d'acc\u00e8s social \u00e0 la propri\u00e9t\u00e9 : 40 000 familles propri\u00e9taires de leur logement social d'ici fin du mandat. "
            "Fusionner Paris Habitat, RIVP et \u00c9logie-Siemp. "
            "Moratoire sur le sur-logement social. "
            "S\u00e9curiser les r\u00e9sidences avec la police municipale"
        ),
        "logements-vacants": (
            "Programme \u00ab Bureaux \u2192 Logements \u00bb : convertir 500 000 m\u00b2 sur 6 ans (environ 6 000 logements). "
            "Limiter Airbnb \u00e0 60 nuits/an (contre 90), taxe de s\u00e9jour \u00e0 15 % (contre 5 %). "
            "Incitation au d\u00e9m\u00e9nagement appropri\u00e9 pour favoriser la mobilit\u00e9 r\u00e9sidentielle"
        ),
        "encadrement-loyers": (
            "Supprimer l'encadrement des loyers \u00e0 terme, en l'assouplissant sur 4 ann\u00e9es pour prot\u00e9ger les locataires. "
            "R\u00e9viser le PLUb pour lib\u00e9rer la construction. "
            "Autoriser des immeubles de 8 \u00e0 10 \u00e9tages (contre 6) dans des zones d\u00e9finies le long des axes de transport"
        ),
        "acces-logement": (
            "Pr\u00eat \u00e0 taux z\u00e9ro via fonds de garantie municipal de 50 000 \u20ac pour primo-acc\u00e9dants (objectif : 500 m\u00e9nages/an). "
            "Programme de cohabitation interg\u00e9n\u00e9rationnelle \u00e9tudiants-seniors (formules \u00ab Loyer \u00bb et \u00ab Solidarit\u00e9 \u00bb). "
            "Guichet unique pour toutes les autorisations d'urbanisme. "
            "Simplification : d\u00e9lai max 6 mois pour permis de construire, d\u00e9mat\u00e9rialisation int\u00e9grale"
        )
    },
    "education": {
        "petite-enfance": (
            "Grand plan de protection de la petite enfance : contr\u00f4le des ant\u00e9c\u00e9dents obligatoire (casier + FIJAIS), "
            "interdiction d'exercer pour coupables d'agression sexuelle, cellules psychologiques. "
            "\u00ab Plan cr\u00e8che \u00bb : priorit\u00e9 nationale, cr\u00e8ches de nuit, encourager cr\u00e8ches priv\u00e9es/entreprises, "
            "horaires \u00e9tendus jusqu'\u00e0 19h30/20h. "
            "Gratuit\u00e9 de la cr\u00e8che \u00e0 partir du 3e enfant. "
            "Allocation de 300 \u20ac/mois quand pas de place en cr\u00e8che. "
            "Interdiction des \u00e9crans dans les cr\u00e8ches municipales"
        ),
        "ecoles-renovation": (
            "Tenue uniforme dans les \u00e9coles parisiennes. Semaine de 4 jours en primaire. Soutenir l'\u00e9cole libre. "
            "R\u00e9novation des \u00e9coles : isolation thermique, v\u00e9g\u00e9talisation des cours, accessibilit\u00e9 PMR, climatisation. "
            "100 centres de soutien scolaire gratuits avec 800 tuteurs (groupes de 8 \u00e9l\u00e8ves max). "
            "Parcours \u00ab Jeune Parisien \u00bb pour CM1-CM2 (5 sorties patrimoine : Notre-Dame, Panth\u00e9on, Arc de Triomphe...). "
            "Maintien des d\u00e9charges de direction"
        ),
        "cantines-fournitures": (
            "Simplifier la grille du prix des cantines scolaires, maximum 3 \u20ac par repas. "
            "Privil\u00e9gier les circuits courts pour les cantines. "
            "Service minimum d'accueil pour les cantines en cas de gr\u00e8ve"
        ),
        "periscolaire-loisirs": (
            "Contr\u00f4le des ant\u00e9c\u00e9dents obligatoire pour tous les candidats \u00e0 l'animation p\u00e9riscolaire "
            "(casier judiciaire + FIJAIS). "
            "P\u00e9riscolaire de qualit\u00e9 avec syst\u00e8me d'alerte rapide. "
            "Plan de pr\u00e9vention g\u00e9n\u00e9ralis\u00e9e contre la drogue dans les \u00e9coles-coll\u00e8ges. "
            "Respect strict de la la\u00efcit\u00e9 dans les cours EILE/ELCO. "
            "Service minimum d'accueil pour cr\u00e8ches et \u00e9coles en cas de gr\u00e8ve"
        ),
        "jeunesse": (
            "Parcours civique municipal pour les 16-25 ans : 200 heures de missions d'int\u00e9r\u00eat g\u00e9n\u00e9ral sur 6 mois "
            "(aide aux personnes \u00e2g\u00e9es, entretien espaces publics, soutien scolaire), r\u00e9mun\u00e9r\u00e9es au SMIC horaire. "
            "Plan d'apprentissage \u00ab savoir-nager \u00bb pour tous les \u00e9l\u00e8ves du cycle 3"
        )
    },
    "environnement": {
        "espaces-verts": (
            "Plan de v\u00e9g\u00e9talisation prioritaire : 50 000 arbres suppl\u00e9mentaires sur six ans. "
            "V\u00e9g\u00e9talisation de toutes les cours d'\u00e9cole (d\u00e9simperme\u0301abilisation des sols). "
            "Renforcer l'am\u00e9nagement de la Petite Ceinture (ouest : 16e, 17e, 18e ; sud : 12e, 13e, 14e, 15e). "
            "D\u00e9velopper les espaces canins dans les parcs et plan bien-\u00eatre animal"
        ),
        "proprete-dechets": (
            "Propret\u00e9 24h/24 par red\u00e9ploiement des effectifs sur le terrain. "
            "Externalisation totale de la collecte des d\u00e9chets. "
            "Autonomie des arrondissements pour choisir leurs prestataires. "
            "Grand plan de d\u00e9ratisation. \u00c9quipes anti-tag (amende port\u00e9e \u00e0 3 750 \u20ac). "
            "Modernisation du mat\u00e9riel. Fin du d\u00e9tournement de la TEOM (60 M\u20ac/an d\u00e9tourn\u00e9s). "
            "Tol\u00e9rance z\u00e9ro : verbalisation syst\u00e9matique, effacement des tags sous 24h"
        ),
        "renovation-energetique": (
            "R\u00e9novation du parc social et priv\u00e9 pour lutter contre les passoires \u00e9nerg\u00e9tiques "
            "avec aides cibl\u00e9es et exon\u00e9rations fiscales. "
            "Isolation thermique acc\u00e9l\u00e9r\u00e9e de tous les \u00e9tablissements scolaires. "
            "Climatisation des \u00e9tablissements scolaires et lieux accueillant du public"
        )
    },
    "sante": {
        "centres-sante": (
            "Soutenir toutes les initiatives et recrutements pour assurer une m\u00e9decine scolaire de qualit\u00e9. "
            "Supprimer les salles de shoot et ouvrir un centre de soin unique pour traiter la toxicomanie"
        ),
        "prevention-sante": (
            "Plan de lutte contre la consommation de stup\u00e9fiants et accompagnement vers la r\u00e9insertion sociale. "
            "Pr\u00e9vention scolaire obligatoire sur les dangers des stup\u00e9fiants. "
            "Plan de pr\u00e9vention des maladies mentales dans les \u00e9coles et coll\u00e8ges"
        ),
        "seniors": (
            "Programme de cohabitation interg\u00e9n\u00e9rationnelle pour lutter contre la solitude et la vuln\u00e9rabilit\u00e9 "
            "des seniors : logement partag\u00e9 avec des \u00e9tudiants (formules \u00ab Loyer \u00bb et \u00ab Solidarit\u00e9 \u00bb), "
            "cadre juridique et m\u00e9diation assur\u00e9s par la mairie"
        )
    },
    "democratie": {
        "budget-participatif": (
            "R\u00e9f\u00e9rendum d'Initiative Populaire d\u00e8s que 5 % du corps \u00e9lectoral le demande. "
            "\u00c9lire tous les conseils de quartiers tous les 3 ans et les consulter syst\u00e9matiquement "
            "d\u00e8s qu'un projet municipal les concerne. Renforcer leurs moyens d'actions. "
            "Votation citoyenne dont le r\u00e9sultat sera respect\u00e9 et appliqu\u00e9"
        ),
        "transparence": (
            "Audit complet et ind\u00e9pendant des d\u00e9penses et comptes de la Ville. "
            "Plan massif d'\u00e9conomie et de d\u00e9sendettement d\u00e8s la 1re ann\u00e9e. "
            "Encadrer les frais de r\u00e9ception pour \u00e9viter les abus. "
            "Conseil de Surveillance Budg\u00e9taire Ind\u00e9pendant avec rapport semestriel public. "
            "Lutter contre la bureaucratie et les privil\u00e8ges des \u00e9lus. "
            "Contr\u00f4le de gestion confi\u00e9 \u00e0 une association de d\u00e9fense des contribuables"
        ),
        "services-publics": (
            "Red\u00e9ployer les effectifs municipaux sur le terrain. "
            "Gestion assainie des services publics avec objectifs d'efficacit\u00e9. "
            "R\u00e9former la gestion des ressources humaines. "
            "Chaque arrondissement pourra choisir ses prestataires de services (propret\u00e9, entretien)"
        )
    },
    "economie": {
        "commerce-local": (
            "Fonds d'aide \u00e0 l'installation de 50 M\u20ac sur 5 ans pour reprises de commerces vacants. "
            "Fonds de soutien aux jeunes entrepreneurs (<35 ans) avec garantie municipale de 50 %. "
            "Taxe dissuasive de 30 % sur locaux commerciaux vacants >2 ans. "
            "Programme \u00ab 1 000 commerces \u00bb et 15 nouveaux march\u00e9s de plein vent. "
            "Transfert des comp\u00e9tences d'autorisations d'ouverture aux mairies d'arrondissement. "
            "Incubateur municipal"
        ),
        "emploi-insertion": (
            "Parcours civique municipal pour les 16-25 ans : 200 heures de missions d'int\u00e9r\u00eat g\u00e9n\u00e9ral "
            "r\u00e9mun\u00e9r\u00e9es au SMIC horaire. "
            "Cr\u00e9ation de zones franches pour revitaliser les quartiers en crise"
        ),
        "attractivite": (
            "Soutenir le \u00ab Made in France \u00bb et les initiatives \u00ab Faites en France \u00bb. "
            "Le Parc des Princes appartient aux Parisiens : cesser de brader les biens publics. "
            "Moratoire sur les grands travaux non-essentiels. "
            "Aucune hausse d'imp\u00f4ts sur les m\u00e9nages, travailleurs et entreprises"
        )
    },
    "culture": {
        "equipements-culturels": (
            "Pr\u00e9server l'h\u00e9ritage culturel parisien : recentrer le budget culture sur le patrimoine "
            "et le mobilier historique. "
            "Parcours obligatoire \u00ab Jeune Parisien \u00bb dans les hauts lieux du patrimoine "
            "(Notre-Dame, Panth\u00e9on, Arc de Triomphe, Invalides, Sainte-Chapelle, Op\u00e9ra Garnier...)"
        )
    },
    "sport": {
        "equipements-sportifs": (
            "Cr\u00e9er trois nouvelles piscines municipales et r\u00e9nover les existantes. "
            "Plan d'apprentissage \u00ab savoir-nager \u00bb pour tous les \u00e9l\u00e8ves du cycle 3"
        )
    },
    "urbanisme": {
        "amenagement-urbain": (
            "Moratoire et r\u00e9vision des projets Tour Eiffel-Trocad\u00e9ro, Champs de Mars-\u00c9cole Militaire "
            "et Place de la Concorde, r\u00e9f\u00e9rendum en 2026. "
            "Soutenir la couverture partielle du p\u00e9riph\u00e9rique. "
            "Garantir la pr\u00e9servation des quartiers pavillonnaires historiques. "
            "Nouveau cr\u00e9matorium sous d\u00e9l\u00e9gation de service public"
        ),
        "accessibilite": (
            "Mise aux normes d'accessibilit\u00e9 PMR compl\u00e8te de tous les \u00e9tablissements scolaires. "
            "Climatisation des \u00e9tablissements scolaires et lieux accueillant du public"
        ),
        "quartiers-prioritaires": (
            "D\u00e9velopper les Zones de S\u00e9curit\u00e9 Prioritaires (ZSP) avec antennes de police municipale "
            "et permanences mobiles dans les quartiers prioritaires. "
            "Cr\u00e9ation de zones franches pour revitaliser les quartiers les plus abandonn\u00e9s"
        )
    },
    "solidarite": {
        "aide-sociale": (
            "Fermer les structures municipales d'accueil pour migrants et rendre les locaux aux Parisiens. "
            "Supprimer les subventions aux associations immigrationnistes. "
            "Cellule de veille campements op\u00e9rationnelle 24h/24. "
            "Allocation de 300 \u20ac/mois pour les familles sans place en cr\u00e8che. "
            "Gratuit\u00e9 de la cr\u00e8che \u00e0 partir du 3e enfant"
        ),
        "pouvoir-achat": (
            "R\u00e9duire la taxe fonci\u00e8re : 310 M\u20ac rendus aux foyers parisiens par an "
            "(205 \u20ac pour un studio, 574 \u20ac pour 70 m\u00b2, 820 \u20ac pour un 4 pi\u00e8ces). "
            "Aucune hausse d'imp\u00f4ts. Gel des taxes (stationnement r\u00e9sidentiel, droits de terrasse, TEOM). "
            "Engager le remboursement acc\u00e9l\u00e9r\u00e9 de la dette parisienne"
        )
    }
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update candidate metadata
    for candidat in data["candidats"]:
        if candidat["id"] == CANDIDAT_ID:
            for key, value in METADATA.items():
                candidat[key] = value
            print(f"Metadata updated: programmeComplet={candidat['programmeComplet']}, liste={candidat['liste']}")
            break
    else:
        print(f"ERROR: Candidat {CANDIDAT_ID} not found!")
        return

    # Insert/update proposals
    count_updated = 0
    count_new = 0
    count_errors = 0

    for cat in data["categories"]:
        cat_id = cat["id"]
        if cat_id not in PROPOSITIONS:
            continue
        for st in cat["sousThemes"]:
            st_id = st["id"]
            if st_id not in PROPOSITIONS[cat_id]:
                continue
            texte = PROPOSITIONS[cat_id][st_id]
            existing = st["propositions"].get(CANDIDAT_ID)
            if existing is not None and existing is not None:
                count_updated += 1
                action = "UPDATED"
            else:
                count_new += 1
                action = "NEW"
            st["propositions"][CANDIDAT_ID] = {
                "texte": texte,
                "source": SOURCE,
                "sourceUrl": SOURCE_URL
            }
            print(f"  [{action}] {cat_id}/{st_id}")

    # Verify all proposed sub-themes were found
    for cat_id, subs in PROPOSITIONS.items():
        for st_id in subs:
            found = False
            for cat in data["categories"]:
                if cat["id"] == cat_id:
                    for st in cat["sousThemes"]:
                        if st["id"] == st_id:
                            found = True
                            break
            if not found:
                print(f"  ERROR: Sub-theme {cat_id}/{st_id} not found in JSON!")
                count_errors += 1

    # Write back
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Updated: {count_updated}, New: {count_new}, Errors: {count_errors}")
    total = count_updated + count_new
    print(f"Total sub-themes with Mariani proposals: {total}")


if __name__ == "__main__":
    main()
