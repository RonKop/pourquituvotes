(function () {
  "use strict";

  var DATA_BASE_URL = '/data/';
  var DATA_VERSION = '2026031601';
  var communesIndex = null;
  var searchDebounce = null;

  function esc(str) {
    var el = document.createElement('span');
    el.textContent = str || '';
    return el.innerHTML;
  }

  function formatNumber(n) {
    return n ? n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '\u00A0') : '0';
  }

  // === Départements ===
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

  // === Recherche communes ===
  function loadCommunesIndex(callback) {
    if (communesIndex) { callback(); return; }
    fetch(DATA_BASE_URL + 'index-communes.json?v=' + DATA_VERSION)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        communesIndex = data;
        callback();
      })
      .catch(function () {
        document.getElementById('national-search-results').innerHTML =
          '<p style="padding:1rem;color:var(--couleur-texte-secondaire)">Erreur de chargement.</p>';
        document.getElementById('national-search-results').hidden = false;
      });
  }

  function normalize(str) {
    return (str || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  }

  function searchCommunes(query) {
    var results = document.getElementById('national-search-results');
    if (!query || query.length < 2) {
      results.hidden = true;
      return;
    }

    loadCommunesIndex(function () {
      var q = normalize(query);
      var matches = [];

      for (var i = 0; i < communesIndex.length && matches.length < 20; i++) {
        var c = communesIndex[i];
        if (normalize(c.n).indexOf(q) === 0 || c.d === query) {
          matches.push(c);
        }
      }

      // Recherche plus large si pas assez de résultats
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
          if (c.w) {
            html += esc(c.w) + ' — ' + c.wp + '% · ';
          }
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

    input.addEventListener('focus', function () {
      // Pré-charger l'index dès le focus
      loadCommunesIndex(function () {});
    });

    input.addEventListener('input', function () {
      clearTimeout(searchDebounce);
      var val = input.value.trim();
      searchDebounce = setTimeout(function () {
        searchCommunes(val);
      }, 200);
    });

    // Fermer les résultats quand on clique ailleurs
    document.addEventListener('click', function (e) {
      var results = document.getElementById('national-search-results');
      var searchBox = document.querySelector('.resultats-search');
      if (searchBox && !searchBox.contains(e.target)) {
        results.hidden = true;
      }
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
      html += '<a href="#dept-' + esc(code) + '" class="resultats-dept-grid__item" data-dept="' + esc(code) + '">';
      html += '<span class="resultats-dept-grid__code">' + esc(code) + '</span>';
      html += '<span class="resultats-dept-grid__nom">' + esc(DEPTS[code]) + '</span>';
      html += '</a>';
    });

    grid.innerHTML = html;

    // Click → charger les communes du département
    grid.addEventListener('click', function (e) {
      var item = e.target.closest('[data-dept]');
      if (!item) return;
      e.preventDefault();
      var dept = item.getAttribute('data-dept');
      showDeptCommunes(dept);
    });
  }

  function showDeptCommunes(dept) {
    loadCommunesIndex(function () {
      var matches = [];
      for (var i = 0; i < communesIndex.length; i++) {
        if (communesIndex[i].d === dept) {
          matches.push(communesIndex[i]);
        }
      }
      matches.sort(function (a, b) { return b.p - a.p; });

      var section = document.getElementById('national-villes-section');
      var table = document.getElementById('national-villes-table');
      section.querySelector('.resultats-section__titre').textContent =
        DEPTS[dept] + ' (' + dept + ') — ' + matches.length + ' communes';

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

      table.innerHTML = html;
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  // === Init ===
  function init() {
    initSearch();
    renderDeptGrid();

    // Charger les grandes villes
    fetch(DATA_BASE_URL + 'villes.json?v=' + DATA_VERSION)
      .then(function (r) { return r.json(); })
      .then(function (villes) {
        var villesAvecResultats = [];
        var totalParticipation = 0;

        villes.forEach(function (v) {
          var res = v.resultats;
          if (res && res.tour1) {
            villesAvecResultats.push(v);
            totalParticipation += res.tauxParticipationT2 || res.tauxParticipationT1 || 0;
          }
        });

        // Hero stats
        document.getElementById('national-villes').textContent = '34 801';
        var avgPart = villesAvecResultats.length > 0 ? (totalParticipation / villesAvecResultats.length).toFixed(1) + '%' : '—';
        document.getElementById('national-participation').textContent = avgPart;
        document.getElementById('national-sous-titre').textContent =
          '34 801 communes — 15 et 22 mars 2026';

        // Trier par nom
        villesAvecResultats.sort(function (a, b) {
          return (a.nom || '').localeCompare(b.nom || '', 'fr');
        });

        // Tableau grandes villes
        var html = '';
        villesAvecResultats.forEach(function (v) {
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
      })
      .catch(function (err) {
        console.error('Erreur chargement résultats nationaux:', err);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
