(function () {
  "use strict";

  var DATA_BASE_URL = '/data/';
  var DATA_VERSION = '2026031601';
  var communesIndex = null;
  var statsData = null;
  var villesData = null;
  var searchDebounce = null;
  var currentSort = 'alpha';
  var currentNuance = '';

  function esc(str) {
    var el = document.createElement('span');
    el.textContent = str || '';
    return el.innerHTML;
  }

  function formatNumber(n) {
    return n ? n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '\u00A0') : '0';
  }

  // Couleurs par famille politique
  var NUANCE_COLORS = {
    'LUG': '#e11d48', 'LDVG': '#f43f5e', 'LFI': '#cc2443', 'LEXG': '#b91c1c', 'LECO': '#22c55e',
    'LUD': '#1d4ed8', 'LDVD': '#3b82f6', 'LUC': '#f59e0b', 'LDVC': '#eab308',
    'LUXD': '#1e3a5f', 'LEXD': '#374151', 'LRN': '#1e3a5f',
    'LDIV': '#6b7280', 'LREG': '#8b5cf6',
  };
  var NUANCE_LABELS = {
    'LUG': 'Union de la gauche', 'LDVG': 'Divers gauche', 'LFI': 'France Insoumise', 'LEXG': 'Extrême gauche', 'LECO': 'Écologistes',
    'LUD': 'Union de la droite', 'LDVD': 'Divers droite', 'LUC': 'Union au centre', 'LDVC': 'Divers centre',
    'LUXD': 'Union extrême droite', 'LEXD': 'Extrême droite', 'LRN': 'Rassemblement National',
    'LDIV': 'Divers', 'LREG': 'Régionalistes',
  };

  var DEPTS = {
    "01":"Ain","02":"Aisne","03":"Allier","04":"Alpes-de-Haute-Provence","05":"Hautes-Alpes",
    "06":"Alpes-Maritimes","07":"Ardèche","08":"Ardennes","09":"Ariège","10":"Aube",
    "11":"Aude","12":"Aveyron","13":"Bouches-du-Rhône","14":"Calvados","15":"Cantal",
    "16":"Charente","17":"Charente-Maritime","18":"Cher","19":"Corrèze","21":"Côte-d'Or",
    "22":"Côtes-d'Armor","23":"Creuse","24":"Dordogne","25":"Doubs","26":"Drôme",
    "27":"Eure","28":"Eure-et-Loir","29":"Finistère","2A":"Corse-du-Sud","2B":"Haute-Corse",
    "30":"Gard","31":"Haute-Garonne","32":"Gers","33":"Gironde","34":"Hérault",
    "35":"Ille-et-Vilaine","36":"Indre","37":"Indre-et-Loire","38":"Isère","39":"Jura",
    "40":"Landes","41":"Loir-et-Cher","42":"Loire","43":"Haute-Loire","44":"Loire-Atlantique",
    "45":"Loiret","46":"Lot","47":"Lot-et-Garonne","48":"Lozère","49":"Maine-et-Loire",
    "50":"Manche","51":"Marne","52":"Haute-Marne","53":"Mayenne","54":"Meurthe-et-Moselle",
    "55":"Meuse","56":"Morbihan","57":"Moselle","58":"Nièvre","59":"Nord",
    "60":"Oise","61":"Orne","62":"Pas-de-Calais","63":"Puy-de-Dôme","64":"Pyrénées-Atlantiques",
    "65":"Hautes-Pyrénées","66":"Pyrénées-Orientales","67":"Bas-Rhin","68":"Haut-Rhin","69":"Rhône",
    "70":"Haute-Saône","71":"Saône-et-Loire","72":"Sarthe","73":"Savoie","74":"Haute-Savoie",
    "75":"Paris","76":"Seine-Maritime","77":"Seine-et-Marne","78":"Yvelines","79":"Deux-Sèvres",
    "80":"Somme","81":"Tarn","82":"Tarn-et-Garonne","83":"Var","84":"Vaucluse",
    "85":"Vendée","86":"Vienne","87":"Haute-Vienne","88":"Vosges","89":"Yonne",
    "90":"Territoire de Belfort","91":"Essonne","92":"Hauts-de-Seine","93":"Seine-Saint-Denis",
    "94":"Val-de-Marne","95":"Val-d'Oise",
    "971":"Guadeloupe","972":"Martinique","973":"Guyane","974":"La Réunion","976":"Mayotte"
  };

  // === Chargement données ===
  function loadCommunesIndex(callback) {
    if (communesIndex) { callback(communesIndex); return; }
    fetch(DATA_BASE_URL + 'index-communes.json?v=' + DATA_VERSION)
      .then(function (r) { return r.json(); })
      .then(function (data) { communesIndex = data; callback(data); })
      .catch(function () {});
  }

  // === Hero stats ===
  function renderHeroStats() {
    if (!statsData) return;
    document.getElementById('national-villes').textContent = formatNumber(statsData.total_communes);
    document.getElementById('national-participation').textContent = statsData.participationMoyenne + '%';
    document.getElementById('national-sous-titre').textContent =
      formatNumber(statsData.total_communes) + ' communes — 1er tour — 15 mars 2026';

    var highEl = document.getElementById('national-highest-part');
    var lowEl = document.getElementById('national-lowest-part');
    if (highEl && statsData.highest_participation) {
      highEl.innerHTML = '<a href="/municipales-2026/' + esc(statsData.highest_participation.slug) + '/resultats/" style="color:#fff;text-decoration:underline">' + statsData.highest_participation.taux + '%</a>';
      highEl.nextElementSibling.innerHTML = esc(statsData.highest_participation.commune) + ' (' + esc(statsData.highest_participation.dept) + ')';
    }
    if (lowEl && statsData.lowest_participation) {
      lowEl.innerHTML = '<a href="/municipales-2026/' + esc(statsData.lowest_participation.slug) + '/resultats/" style="color:#fff;text-decoration:underline">' + statsData.lowest_participation.taux + '%</a>';
      lowEl.nextElementSibling.innerHTML = esc(statsData.lowest_participation.commune) + ' (' + esc(statsData.lowest_participation.dept) + ')';
    }
  }

  // === Faits marquants ===
  function renderHighlights() {
    if (!statsData) return;
    var section = document.getElementById('national-highlights-section');
    var container = document.getElementById('national-highlights');
    section.hidden = false;

    var ps = statsData.plus_serre || {};
    var highlights = [
      {
        icon: '🗳️', title: 'Inscrits',
        value: formatNumber(statsData.total_inscrits),
        detail: formatNumber(statsData.total_votants) + ' votants'
      },
      {
        icon: '📊', title: 'Participation moyenne',
        value: statsData.participationMoyenne + '%',
        detail: 'Sur ' + formatNumber(statsData.total_communes) + ' communes'
      },
      {
        icon: '🏆', title: 'Résultat le plus serré',
        value: '<a href="/municipales-2026/' + esc(ps.slug || '') + '/resultats/">' + esc(ps.commune || '—') + '</a>',
        detail: esc(ps.c1 || '') + ' (' + (ps.p1 || 0) + '%) vs ' + esc(ps.c2 || '') + ' (' + (ps.p2 || 0) + '%) — ' + (ps.ecart || 0) + ' pts d\'écart'
      },
    ];

    // Top nuances
    var nuances = statsData.nuances_gagnantes || {};
    var sortedNuances = Object.keys(nuances).filter(function(k) { return NUANCE_LABELS[k]; }).sort(function (a, b) { return nuances[b] - nuances[a]; });
    if (sortedNuances.length > 0) {
      var topN = sortedNuances[0];
      highlights.push({
        icon: '🏛️', title: 'Nuance en tête (nbre de villes)',
        value: NUANCE_LABELS[topN] || topN,
        detail: nuances[topN] + ' communes gagnées'
      });
    }

    var html = '';
    highlights.forEach(function (h) {
      html += '<div class="resultats-highlight">';
      html += '<div class="resultats-highlight__icon">' + h.icon + '</div>';
      html += '<div class="resultats-highlight__title">' + h.title + '</div>';
      html += '<div class="resultats-highlight__value">' + h.value + '</div>';
      html += '<div class="resultats-highlight__detail">' + h.detail + '</div>';
      html += '</div>';
    });
    container.innerHTML = html;
  }

  // === Barre nuances ===
  function renderNuancesBar() {
    if (!statsData) return;
    var section = document.getElementById('national-nuances-section');
    var bar = document.getElementById('national-nuances-bar');
    var legend = document.getElementById('national-nuances-legend');
    section.hidden = false;

    var nuances = statsData.nuances_gagnantes || {};
    var total = 0;
    var sorted = Object.keys(nuances).filter(function(k) { return NUANCE_LABELS[k]; }).sort(function (a, b) { return nuances[b] - nuances[a]; });
    sorted.forEach(function (k) { total += nuances[k]; });

    if (total === 0) { section.hidden = true; return; }

    var barHtml = '';
    var legendHtml = '';
    sorted.forEach(function (nuance) {
      var count = nuances[nuance];
      var pct = (count / total * 100).toFixed(1);
      var color = NUANCE_COLORS[nuance] || '#6b7280';
      var label = NUANCE_LABELS[nuance] || nuance;
      barHtml += '<div class="resultats-nuances-bar__segment" style="width:' + pct + '%;background:' + color + '" title="' + esc(label) + ' : ' + count + ' communes (' + pct + '%)"></div>';
      legendHtml += '<span class="resultats-nuances-legend__item" data-nuance="' + esc(nuance) + '">';
      legendHtml += '<span class="resultats-nuances-legend__dot" style="background:' + color + '"></span>';
      legendHtml += esc(label) + ' <span class="resultats-nuances-legend__count">' + count + '</span>';
      legendHtml += '</span>';
    });

    bar.innerHTML = barHtml;
    legend.innerHTML = legendHtml;

    // Populate filter select
    var filterSelect = document.getElementById('national-filter-nuance');
    if (filterSelect) {
      sorted.forEach(function (nuance) {
        var opt = document.createElement('option');
        opt.value = nuance;
        opt.textContent = (NUANCE_LABELS[nuance] || nuance) + ' (' + nuances[nuance] + ')';
        filterSelect.appendChild(opt);
      });
    }
  }

  // === Grandes villes (avec tri/filtre) ===
  function renderVillesTable() {
    if (!villesData) return;

    var filtered = villesData.filter(function (v) {
      if (!v.resultats || !v.resultats.tour1) return false;
      if (currentNuance) {
        // Filtrer par nuance du gagnant — on a besoin de l'index communes
        // Pour les grandes villes, on matche par ID dans l'index
        if (communesIndex) {
          for (var i = 0; i < communesIndex.length; i++) {
            if (communesIndex[i].s === v.id) {
              // Pas de champ nuance dans l'index des communes pour les grandes villes
              // On skip le filtre nuance pour les grandes villes
              break;
            }
          }
        }
        return true; // Garder toutes les grandes villes quand filtre nuance
      }
      return true;
    });

    // Tri
    filtered.sort(function (a, b) {
      var resA = a.resultats || {};
      var resB = b.resultats || {};
      switch (currentSort) {
        case 'part-desc':
          return (resB.tauxParticipationT1 || 0) - (resA.tauxParticipationT1 || 0);
        case 'part-asc':
          return (resA.tauxParticipationT1 || 0) - (resB.tauxParticipationT1 || 0);
        case 'pop-desc':
          return ((b.stats || {}).candidats || 0) - ((a.stats || {}).candidats || 0);
        default:
          return (a.nom || '').localeCompare(b.nom || '', 'fr');
      }
    });

    var html = '';
    filtered.forEach(function (v) {
      var res = v.resultats;
      var taux = res.tauxParticipationT2 || res.tauxParticipationT1 || 0;
      var eluNom = res.eluMaire ? res.eluMaire.nom : '—';
      var hasT2 = res.tour2;
      var tourLabel = hasT2 ? 'T1+T2' : 'T1';
      var statusBadge = res.status === 'definitif'
        ? '<span class="badge badge--definitif">Définitif</span>'
        : '<span class="badge badge--provisoire">Provisoire</span>';

      html += '<a href="/municipales-2026/' + esc(v.id) + '/resultats/" class="resultats-table__row" style="text-decoration:none">';
      html += '  <div class="resultats-table__rang" style="font-size:0.8rem">' + esc(tourLabel) + '</div>';
      html += '  <div class="resultats-table__info">';
      html += '    <div class="resultats-table__nom">' + esc(v.nom) + ' ' + statusBadge + '</div>';
      html += '    <div class="resultats-table__liste">' + (eluNom !== '—' ? 'Élu(e) : ' + esc(eluNom) : 'En attente du second tour') + '</div>';
      html += '  </div>';
      html += '  <div class="resultats-table__scores">';
      html += '    <div class="resultats-table__pct">' + taux + '%</div>';
      html += '    <div class="resultats-table__voix">participation</div>';
      html += '  </div>';
      html += '</a>';
    });

    document.getElementById('national-villes-table').innerHTML = html;
  }

  // === Recherche ===
  function normalize(str) {
    return (str || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  }

  function searchCommunes(query) {
    var results = document.getElementById('national-search-results');
    if (!query || query.length < 2) { results.hidden = true; return; }

    loadCommunesIndex(function () {
      var q = normalize(query);
      var matches = [];

      for (var i = 0; i < communesIndex.length && matches.length < 20; i++) {
        var c = communesIndex[i];
        if (normalize(c.n).indexOf(q) === 0 || c.d === query) {
          matches.push(c);
        }
      }
      if (matches.length < 5) {
        for (var j = 0; j < communesIndex.length && matches.length < 20; j++) {
          var c2 = communesIndex[j];
          if (normalize(c2.n).indexOf(q) !== -1 && matches.indexOf(c2) === -1) {
            matches.push(c2);
          }
        }
      }

      if (matches.length === 0) {
        results.innerHTML = '<p style="padding:1rem;color:var(--couleur-texte-secondaire)">Aucune commune trouvée pour "' + esc(query) + '"</p>';
      } else {
        var html = '';
        matches.forEach(function (c) {
          html += '<a href="/municipales-2026/' + esc(c.s) + '/resultats/" class="resultats-search__item">';
          html += '<div class="resultats-search__item-nom">' + esc(c.n) + ' <span class="resultats-search__item-dept">(' + esc(c.d) + ')</span></div>';
          html += '<div class="resultats-search__item-detail">';
          if (c.w) html += esc(c.w) + ' — ' + c.wp + '% · ';
          html += 'Participation ' + c.t + '%';
          html += '</div>';
          html += '</a>';
        });
        results.innerHTML = html;
      }
      results.hidden = false;
    });
  }

  function initSearch() {
    var input = document.getElementById('national-search');
    if (!input) return;
    input.addEventListener('focus', function () { loadCommunesIndex(function () {}); });
    input.addEventListener('input', function () {
      clearTimeout(searchDebounce);
      var val = input.value.trim();
      searchDebounce = setTimeout(function () { searchCommunes(val); }, 200);
    });
    document.addEventListener('click', function (e) {
      var results = document.getElementById('national-search-results');
      var box = document.querySelector('.resultats-search');
      if (box && !box.contains(e.target)) results.hidden = true;
    });
  }

  // === Grille départements ===
  function renderDeptGrid() {
    var grid = document.getElementById('national-dept-grid');
    if (!grid) return;
    var html = '';
    var keys = Object.keys(DEPTS).sort(function (a, b) {
      return a.localeCompare(b, 'fr', { numeric: true });
    });
    keys.forEach(function (code) {
      var partTxt = '';
      if (statsData && statsData.participation_par_dept && statsData.participation_par_dept[code]) {
        partTxt = ' · ' + statsData.participation_par_dept[code] + '%';
      }
      html += '<a href="#dept-' + esc(code) + '" class="resultats-dept-grid__item" data-dept="' + esc(code) + '">';
      html += '<span class="resultats-dept-grid__code">' + esc(code) + '</span>';
      html += '<span class="resultats-dept-grid__nom">' + esc(DEPTS[code]) + partTxt + '</span>';
      html += '</a>';
    });
    grid.innerHTML = html;
    grid.addEventListener('click', function (e) {
      var item = e.target.closest('[data-dept]');
      if (!item) return;
      e.preventDefault();
      showDeptCommunes(item.getAttribute('data-dept'));
    });
  }

  function showDeptCommunes(dept) {
    loadCommunesIndex(function () {
      var matches = [];
      for (var i = 0; i < communesIndex.length; i++) {
        if (communesIndex[i].d === dept) matches.push(communesIndex[i]);
      }
      matches.sort(function (a, b) { return b.p - a.p; });

      var section = document.getElementById('national-villes-section');
      section.querySelector('.resultats-section__titre').textContent =
        (DEPTS[dept] || dept) + ' (' + dept + ') — ' + matches.length + ' communes';

      var html = '';
      matches.forEach(function (c) {
        html += '<a href="/municipales-2026/' + esc(c.s) + '/resultats/" class="resultats-table__row" style="text-decoration:none">';
        html += '  <div class="resultats-table__rang" style="font-size:0.75rem">' + formatNumber(c.p) + '</div>';
        html += '  <div class="resultats-table__info">';
        html += '    <div class="resultats-table__nom">' + esc(c.n) + '</div>';
        html += '    <div class="resultats-table__liste">' + (c.w ? 'En tête : ' + esc(c.w) : '') + '</div>';
        html += '  </div>';
        html += '  <div class="resultats-table__scores">';
        html += '    <div class="resultats-table__pct">' + c.t + '%</div>';
        html += '    <div class="resultats-table__voix">participation</div>';
        html += '  </div>';
        html += '</a>';
      });

      document.getElementById('national-villes-table').innerHTML = html;
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  // === Init ===
  function init() {
    initSearch();

    // Charger stats agrégées
    fetch(DATA_BASE_URL + 'stats-resultats-t1.json?v=' + DATA_VERSION)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        statsData = data;
        renderHeroStats();
        renderHighlights();
        renderNuancesBar();
        renderDeptGrid();
      })
      .catch(function () { renderDeptGrid(); });

    // Charger grandes villes
    fetch(DATA_BASE_URL + 'villes.json?v=' + DATA_VERSION)
      .then(function (r) { return r.json(); })
      .then(function (villes) {
        villesData = villes;
        renderVillesTable();
      })
      .catch(function (err) { console.error(err); });

    // Événements tri/filtre
    var sortSelect = document.getElementById('national-sort');
    var nuanceSelect = document.getElementById('national-filter-nuance');
    if (sortSelect) {
      sortSelect.addEventListener('change', function () {
        currentSort = this.value;
        renderVillesTable();
      });
    }
    if (nuanceSelect) {
      nuanceSelect.addEventListener('change', function () {
        currentNuance = this.value;
        renderVillesTable();
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
