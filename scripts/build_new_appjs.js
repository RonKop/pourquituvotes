#!/usr/bin/env node
/**
 * build_new_appjs.js — Reconstruit app.js sans les données inline
 *
 * Remplace les données embarquées par des fonctions fetch async.
 * Garde tout le code UI intact.
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const APP_JS = path.join(ROOT, 'js', 'app.js');

const content = fs.readFileSync(APP_JS, 'utf-8');
const lines = content.split('\n');

// Find line indices (0-based)
// Data starts at line 4 (index 3): "// === Données embarquées..."
// Data ends after line 26515 (index 26514): "  };"
// Line 26516 (index 26515) is blank
// Line 26517 (index 26516) is blank
// UI starts at line 26518 (index 26517): "// === Éléments DOM ==="

// The IIFE opening is lines 1-3 (indices 0-2)
const iifeOpening = lines.slice(0, 3).join('\n');

// UI code is from line 26518 (index 26517) to end
const uiCode = lines.slice(26517).join('\n');

// New data loading code
const dataLoading = `
  // === Chargement des données (JSON externe) ===
  var VILLES = [];
  var ELECTIONS = {};
  var ELECTIONS_CACHE = {};
  var DATA_BASE_URL = 'data/';
  var DATA_VERSION = '2026020901';

  function chargerVilles() {
    return fetch(DATA_BASE_URL + 'villes.json?v=' + DATA_VERSION)
      .then(function(r) {
        if (!r.ok) throw new Error('Erreur chargement villes: ' + r.status);
        return r.json();
      })
      .then(function(data) { VILLES = data; return data; });
  }

  function chargerDonneesElection(id) {
    if (ELECTIONS_CACHE[id]) return Promise.resolve(ELECTIONS_CACHE[id]);
    return fetch(DATA_BASE_URL + 'elections/' + id + '.json?v=' + DATA_VERSION)
      .then(function(r) {
        if (!r.ok) throw new Error('Erreur chargement election: ' + r.status);
        return r.json();
      })
      .then(function(data) {
        ELECTIONS_CACHE[id] = data;
        ELECTIONS[id] = data;
        return data;
      });
  }

  function afficherChargement(visible) {
    var overlay = document.getElementById('loader-overlay');
    if (overlay) overlay.hidden = !visible;
  }
`;

// Construct new file
const newContent = iifeOpening + '\n' + dataLoading + '\n' + uiCode;

fs.writeFileSync(APP_JS, newContent, 'utf-8');

const newSize = (Buffer.byteLength(newContent, 'utf-8') / 1024).toFixed(1);
const newLines = newContent.split('\n').length;
console.log(`app.js reconstruit: ${newLines} lignes, ${newSize} KB`);
console.log('Données inline supprimées, fetch async ajouté');
