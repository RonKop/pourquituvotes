#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// Simple keyword-to-subtheme mapping
const keywordMap = {
  'police': 'securite/police-municipale',
  'gendarme': 'securite/police-municipale',
  'vidéo': 'securite/videoprotection',
  'surveillance': 'securite/videoprotection',
  'prévention': 'securite/prevention-mediation',
  'médiation': 'securite/prevention-mediation',
  'violences': 'securite/violences-femmes',
  'transport': 'transports/transports-en-commun',
  'bus': 'transports/transports-en-commun',
  'tramway': 'transports/transports-en-commun',
  'métro': 'transports/transports-en-commun',
  'vélo': 'transports/velo-mobilites-douces',
  'mobilité': 'transports/velo-mobilites-douces',
  'piéton': 'transports/pietons-circulation',
  'circulation': 'transports/pietons-circulation',
  'stationnement': 'transports/stationnement',
  'parking': 'transports/stationnement',
  'tarif': 'transports/tarifs-gratuite',
  'gratuit': 'transports/tarifs-gratuite',
  'logement': 'logement/logement-social',
  'loyer': 'logement/encadrement-loyers',
  'vacant': 'logement/logements-vacants',
  'école': 'education/ecoles-renovation',
  'crèche': 'education/petite-enfance',
  'cantine': 'education/cantines-fournitures',
  'périscolaire': 'education/periscolaire-loisirs',
  'loisir': 'education/periscolaire-loisirs',
  'jeunesse': 'education/jeunesse',
  'enfant': 'education/jeunesse',
  'espace vert': 'environnement/espaces-verts',
  'parc': 'environnement/espaces-verts',
  'jardin': 'environnement/espaces-verts',
  'arbre': 'environnement/espaces-verts',
  'propreté': 'environnement/proprete-dechets',
  'déchet': 'environnement/proprete-dechets',
  'climat': 'environnement/climat-adaptation',
  'rénovation': 'environnement/renovation-energetique',
  'énergie': 'environnement/renovation-energetique',
  'alimentation': 'environnement/alimentation-durable',
  'hôpital': 'sante/centres-sante',
  'médecin': 'sante/centres-sante',
  'santé': 'sante/centres-sante',
  'senior': 'sante/seniors',
  'retraité': 'sante/seniors',
  'budget participatif': 'democratie/budget-participatif',
  'citoyen': 'democratie/transparence',
  'transparence': 'democratie/transparence',
  'association': 'democratie/vie-associative',
  'services publics': 'democratie/services-publics',
  'commerce': 'economie/commerce-local',
  'emploi': 'economie/emploi-insertion',
  'travail': 'economie/emploi-insertion',
  'insertion': 'economie/emploi-insertion',
  'attractivité': 'economie/attractivite',
  'culture': 'culture/equipements-culturels',
  'musée': 'culture/equipements-culturels',
  'théâtre': 'culture/equipements-culturels',
  'bibliothèque': 'culture/equipements-culturels',
  'événement': 'culture/evenements-creation',
  'festival': 'culture/evenements-creation',
  'création': 'culture/evenements-creation',
  'sport': 'sport/equipements-sportifs',
  'gymnase': 'sport/equipements-sportifs',
  'stade': 'sport/equipements-sportifs',
  'piscine': 'sport/equipements-sportifs',
  'aménagement': 'urbanisme/amenagement-urbain',
  'urbanisme': 'urbanisme/amenagement-urbain',
  'quartier': 'urbanisme/quartiers-prioritaires',
  'rue': 'urbanisme/amenagement-urbain',
  'accessibilité': 'urbanisme/accessibilite',
  'aide': 'solidarite/aide-sociale',
  'égalité': 'solidarite/egalite-discriminations',
  'discrimination': 'solidarite/egalite-discriminations',
  'pouvoir d\'achat': 'solidarite/pouvoir-achat',
};

function getSubtheme(text) {
  const lower = text.toLowerCase();
  let best = null;
  let bestScore = 0;

  for (const [keyword, subtheme] of Object.entries(keywordMap)) {
    if (lower.includes(keyword)) {
      const score = keyword.length; // Longer matches win
      if (score > bestScore) {
        best = subtheme;
        bestScore = score;
      }
    }
  }
  return best;
}

function isConcrete(text) {
  if (!text || text.length < 20 || text.length > 400) return false;
  const hasNumber = /\d+/.test(text);
  const hasAction = /créer|construire|rénover|augmenter|développer|renforcer|installer|améliorer|transformer|ouvrir|éliminer|réduire|mettre/.test(text.toLowerCase());
  return hasNumber || hasAction;
}

function extract(cachePath) {
  const props = {};
  const data = JSON.parse(fs.readFileSync(cachePath, 'utf-8'));

  const allText = [];
  if (data.pages && Array.isArray(data.pages)) {
    data.pages.forEach(p => {
      if (p.text) allText.push(p.text);
    });
  }

  const combined = allText.join('\n\n');
  const lines = combined.split('\n').map(l => l.trim()).filter(l => l);

  let count = 0;
  for (const line of lines) {
    if (count >= 25) break;
    if (!isConcrete(line)) continue;

    const subtheme = getSubtheme(line);
    if (!subtheme || props[subtheme]) continue;

    props[subtheme] = {
      texte: line.substring(0, 200),
      source: 'Site officiel ' + (data.nom || ''),
      sourceUrl: data.url || ''
    };
    count++;
  }

  return props;
}

// Process all candidates
const base = 'C:\\\\Users\\\\KOPELMANRon\\\\Downloads\\\\FR comp mun\\\\scripts';
const candidates = [
  ['vitry-sur-seine', 'afflatet'],
  ['lille', 'spillebout'],
  ['toulouse', 'meilhac'],
  ['grenoble', 'belaid'],
  ['antibes', 'ducatel']
];

const resultDir = path.join(base, 'crawl_results');
if (!fs.existsSync(resultDir)) fs.mkdirSync(resultDir, { recursive: true });

console.log('='.repeat(80));
console.log('Extraction');
console.log('='.repeat(80));

let total = 0;
for (const [ville, candidat] of candidates) {
  try {
    const cachePath = path.join(base, 'crawl_cache', ville + '_' + candidat + '.json');
    const resultPath = path.join(resultDir, ville + '_' + candidat + '.json');

    const props = extract(cachePath);
    total += Object.keys(props).length;

    fs.writeFileSync(resultPath, JSON.stringify(props, null, 2), 'utf-8');
    console.log(`✓ ${ville}/${candidat}: ${Object.keys(props).length} propositions`);
  } catch (e) {
    console.log(`✗ ${ville}/${candidat}: ${e.message}`);
    const resultPath = path.join(resultDir, ville + '_' + candidat + '.json');
    fs.writeFileSync(resultPath, JSON.stringify({}, null, 2), 'utf-8');
  }
}

console.log('='.repeat(80));
console.log(`Total: ${total} propositions`);
