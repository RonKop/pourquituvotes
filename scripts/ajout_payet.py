"""Ajout de nouvelles propositions Giovanni Payet (Saint-Denis Réunion) - mail du 9 mars 2026."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/elections/saint-denis-reunion-2026.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

SRC = "Campagne Giovanni Payet 2026"
URL = "https://lavoixcitoyenne.re/"

# Mapping: catégorie → sous-thème → nouvelles mesures à AJOUTER
ajouts = {
    "transports": {
        "transports-en-commun": [
            "Mettre en place le suivi en temps réel des bus en station et sur téléphone portable.",
            "Créer « La Voix des Voyageurs » : comité d'usagers des lignes de bus pour améliorer le service.",
        ],
    },
    "education": {
        "periscolaire-loisirs": [
            "Renforcer les activités périscolaires avec « L'école des nouveaux liens ».",
            "Baisser de 20 % les tarifs du périscolaire.",
            "« La kour lé rouver » : ouvrir les cours d'écoles les week-ends et pendant les vacances pour les activités socio-culturelles et associatives.",
            "Mettre en place la formation continue de l'équipe éducative.",
        ],
        "petite-enfance": [
            "Expérimenter puis déployer les couches lavables dans les crèches municipales pour protéger la santé des enfants et réduire les déchets.",
        ],
        "ecoles-renovation": [
            "Plan de réduction du bruit dans les réfectoires scolaires pour faire de la pause déjeuner un moment de plaisir.",
        ],
    },
    "urbanisme": {
        "amenagement-urbain": [
            "Quartiers-jardins : plan de végétalisation et de désimperméabilisation des quartiers.",
            "« Ateliers du renouveau » : reconquête de 12 lieux en 12 mois par les habitants, associations et élus.",
            "Rénovation et modernisation du mobilier urbain pour s'adapter au changement climatique et au vieillissement de la population.",
        ],
    },
    "environnement": {
        "espaces-verts": [
            "Plan de lutte contre l'errance animale.",
        ],
        "climat-adaptation": [
            "Achat responsable : atteindre 30 % d'achats durables et responsables dans la commande publique d'ici la fin du mandat.",
        ],
        "proprete-dechets": [
            "Expérimenter la tarification incitative pour encourager la réduction globale des volumes de déchets.",
        ],
        "renovation-energetique": [
            "Réaliser un Schéma directeur des énergies pour économiser et produire de l'énergie, notamment photovoltaïque.",
            "Couvrir le marché des Camélias et le marché du Chaudron avec des ombrières solaires pour produire de l'énergie.",
        ],
    },
    "economie": {
        "attractivite": [
            "« La table des 150 » : création d'un réseau de 150 acteurs de la restauration de Saint-Denis engagés dans une alimentation locale et de qualité.",
            "Expérimenter le plafonnement des baux commerciaux.",
        ],
    },
    "logement": {
        "logement-social": [
            "Charte d'engagements réciproques entre les bailleurs sociaux, la commune et l'intercommunalité pour apporter une réponse rapide et concrète aux difficultés des locataires.",
        ],
    },
    "solidarite": {
        "aide-sociale": [
            "« Anpartaz » : application pour le recensement, la récolte et la transformation des surplus de fruits chez les habitants (mangues, letchis, etc.).",
        ],
    },
}

added = 0
for cat in data["categories"]:
    cat_id = cat["id"]
    if cat_id not in ajouts:
        continue
    for st in cat["sousThemes"]:
        st_id = st["id"]
        if st_id not in ajouts[cat_id]:
            continue
        nouvelles = ajouts[cat_id][st_id]
        current = st["propositions"].get("payet")
        if current is None:
            # Créer l'entrée
            st["propositions"]["payet"] = {
                "mesures": nouvelles,
                "source": SRC,
                "sourceUrl": URL,
            }
        else:
            # Ajouter aux mesures existantes
            if isinstance(current, dict) and "mesures" in current:
                current["mesures"].extend(nouvelles)
            else:
                st["propositions"]["payet"] = {
                    "mesures": nouvelles,
                    "source": SRC,
                    "sourceUrl": URL,
                }
        added += len(nouvelles)
        print(f"  {cat_id}/{st_id}: +{len(nouvelles)} mesures")

print(f"\nTotal: {added} mesures ajoutées")

# Compter le total Payet
total = sum(
    len(st.get("propositions", {}).get("payet", {}).get("mesures", []))
    for cat in data["categories"]
    for st in cat["sousThemes"]
    if st.get("propositions", {}).get("payet") and isinstance(st["propositions"]["payet"], dict)
)
print(f"Total Payet après ajout: {total} mesures")

with open('data/elections/saint-denis-reunion-2026.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("saint-denis-reunion-2026.json mis à jour OK")
