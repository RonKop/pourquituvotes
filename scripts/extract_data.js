#!/usr/bin/env node
/**
 * extract_data.js — Extraction des données de app.js vers des fichiers JSON
 *
 * Lit app.js, extrait VILLES et ELECTIONS, les écrit en fichiers JSON séparés.
 * Validation intégrée : compare les données re-lues avec les originales.
 *
 * Usage : node scripts/extract_data.js
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const APP_JS = path.join(ROOT, 'js', 'app.js');
const DATA_DIR = path.join(ROOT, 'data');
const ELECTIONS_DIR = path.join(DATA_DIR, 'elections');

// Ensure directories exist
if (!fs.existsSync(ELECTIONS_DIR)) {
  fs.mkdirSync(ELECTIONS_DIR, { recursive: true });
}

console.log('=== Extraction des données app.js → JSON ===\n');

// 1. Read app.js
const content = fs.readFileSync(APP_JS, 'utf-8');

// 2. Extract VILLES array (lines 5 to the closing ];)
const villesStartMatch = content.match(/^\s*var VILLES\s*=\s*\[/m);
if (!villesStartMatch) {
  console.error('ERREUR: var VILLES introuvable dans app.js');
  process.exit(1);
}

const villesStart = villesStartMatch.index;

// Find the ELECTIONS declaration to know where VILLES ends
const electionsStartMatch = content.match(/^\s*var ELECTIONS\s*=\s*\{/m);
if (!electionsStartMatch) {
  console.error('ERREUR: var ELECTIONS introuvable dans app.js');
  process.exit(1);
}

const electionsVarStart = electionsStartMatch.index;

// Extract the VILLES source (from "var VILLES = [" to the "];" before ELECTIONS)
const villesSource = content.substring(villesStart, electionsVarStart).trim();
// Remove trailing semicolons / whitespace
const villesSourceClean = villesSource.replace(/;\s*$/, '');

// 3. Extract ELECTIONS object
// Find the end of ELECTIONS by tracking braces
let braceDepth = 0;
let electionsEnd = -1;
const electionsObjStart = content.indexOf('{', electionsVarStart);

for (let i = electionsObjStart; i < content.length; i++) {
  const ch = content[i];
  if (ch === '{') braceDepth++;
  else if (ch === '}') {
    braceDepth--;
    if (braceDepth === 0) {
      electionsEnd = i + 1;
      break;
    }
  }
}

if (electionsEnd === -1) {
  console.error('ERREUR: fin de ELECTIONS introuvable');
  process.exit(1);
}

const electionsSource = 'var ELECTIONS = ' + content.substring(electionsObjStart, electionsEnd) + ';';

console.log(`VILLES: lignes ${villesStart}..${electionsVarStart} (${(electionsVarStart - villesStart)} chars)`);
console.log(`ELECTIONS: lignes ${electionsVarStart}..${electionsEnd} (${(electionsEnd - electionsVarStart)} chars)`);

// 4. Evaluate both in a sandbox
const sandbox = {};
vm.createContext(sandbox);

try {
  vm.runInContext(villesSourceClean + ';', sandbox);
} catch (e) {
  console.error('ERREUR évaluation VILLES:', e.message);
  process.exit(1);
}

try {
  vm.runInContext(electionsSource, sandbox);
} catch (e) {
  console.error('ERREUR évaluation ELECTIONS:', e.message);
  process.exit(1);
}

const VILLES = sandbox.VILLES;
const ELECTIONS = sandbox.ELECTIONS;

console.log(`\n${VILLES.length} villes extraites`);
console.log(`${Object.keys(ELECTIONS).length} élections extraites\n`);

// 5. Compute departement from codePostal
function getDepartement(cp) {
  if (!cp) return '';
  // Corse
  if (cp.startsWith('20')) {
    const num = parseInt(cp.substring(0, 5));
    if (num >= 20000 && num <= 20190) return '2A';
    return '2B';
  }
  // DOM-TOM (97x, 98x)
  if (cp.startsWith('97') || cp.startsWith('98')) {
    return cp.substring(0, 3);
  }
  return cp.substring(0, 2);
}

// 6. Compute stats per ville and build villes.json
const villesJson = VILLES.map(function (v) {
  const electionId = v.elections[0];
  const election = ELECTIONS[electionId];

  let stats = { candidats: 0, propositions: 0, themes: 0, complets: 0 };
  let candidatsLeger = [];

  if (election) {
    stats.candidats = election.candidats.length;
    stats.themes = election.categories.length;
    stats.complets = election.candidats.filter(c => c.programmeComplet).length;

    // Count propositions
    let totalProps = 0;
    election.categories.forEach(function (cat) {
      if (cat.sousThemes) {
        cat.sousThemes.forEach(function (st) {
          Object.keys(st.propositions).forEach(function (cid) {
            if (st.propositions[cid] && st.propositions[cid].texte) {
              totalProps++;
            }
          });
        });
      }
    });
    stats.propositions = totalProps;

    // Build light candidats list
    candidatsLeger = election.candidats.map(function (c) {
      return { id: c.id, nom: c.nom, liste: c.liste };
    });
  }

  return {
    id: v.id,
    nom: v.nom,
    codePostal: v.codePostal,
    departement: getDepartement(v.codePostal),
    elections: v.elections,
    stats: stats,
    candidats: candidatsLeger
  };
});

// 7. Write villes.json
const villesJsonPath = path.join(DATA_DIR, 'villes.json');
fs.writeFileSync(villesJsonPath, JSON.stringify(villesJson, null, 2), 'utf-8');
console.log(`villes.json écrit (${villesJson.length} villes, ${(fs.statSync(villesJsonPath).size / 1024).toFixed(1)} KB)`);

// 8. Write each election JSON
let totalElections = 0;
Object.keys(ELECTIONS).forEach(function (electionId) {
  const election = ELECTIONS[electionId];
  const jsonPath = path.join(ELECTIONS_DIR, electionId + '.json');
  fs.writeFileSync(jsonPath, JSON.stringify(election, null, 2), 'utf-8');
  const size = (fs.statSync(jsonPath).size / 1024).toFixed(1);
  console.log(`  ${electionId}.json (${size} KB, ${election.candidats.length} candidats)`);
  totalElections++;
});

console.log(`\n${totalElections} fichiers élection écrits`);

// 9. Validation — re-read and deep compare
console.log('\n=== Validation ===\n');
let errors = 0;

// Validate villes.json
const rereadVilles = JSON.parse(fs.readFileSync(villesJsonPath, 'utf-8'));
if (rereadVilles.length !== villesJson.length) {
  console.error(`ERREUR: villes.json: ${rereadVilles.length} vs ${villesJson.length} villes`);
  errors++;
} else {
  console.log(`villes.json: OK (${rereadVilles.length} villes)`);
}

// Validate each election
Object.keys(ELECTIONS).forEach(function (electionId) {
  const jsonPath = path.join(ELECTIONS_DIR, electionId + '.json');
  const reread = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
  const original = ELECTIONS[electionId];

  // Deep compare via JSON.stringify
  const origStr = JSON.stringify(original);
  const rereadStr = JSON.stringify(reread);

  if (origStr !== rereadStr) {
    console.error(`ERREUR: ${electionId}.json ne correspond pas à l'original !`);
    // Find first difference
    for (let i = 0; i < Math.max(origStr.length, rereadStr.length); i++) {
      if (origStr[i] !== rereadStr[i]) {
        console.error(`  Diff à position ${i}: orig="${origStr.substring(i, i + 50)}" vs reread="${rereadStr.substring(i, i + 50)}"`);
        break;
      }
    }
    errors++;
  } else {
    console.log(`  ${electionId}.json: OK`);
  }
});

if (errors > 0) {
  console.error(`\n${errors} ERREUR(S) de validation !`);
  process.exit(1);
} else {
  console.log('\nValidation complète : TOUT EST OK');
}

// 10. Print summary
console.log('\n=== Résumé ===');
console.log(`Fichiers créés :`);
console.log(`  data/villes.json (${(fs.statSync(villesJsonPath).size / 1024).toFixed(1)} KB)`);
let totalSize = fs.statSync(villesJsonPath).size;
Object.keys(ELECTIONS).forEach(function (electionId) {
  const jsonPath = path.join(ELECTIONS_DIR, electionId + '.json');
  totalSize += fs.statSync(jsonPath).size;
});
console.log(`  data/elections/*.json (${totalElections} fichiers)`);
console.log(`  Total: ${(totalSize / 1024).toFixed(1)} KB`);
console.log(`\nDonnées dans app.js: ${((electionsEnd - villesStart) / 1024).toFixed(1)} KB → à supprimer`);
console.log(`Code UI restant: ~${((content.length - (electionsEnd - villesStart)) / 1024).toFixed(1)} KB`);
