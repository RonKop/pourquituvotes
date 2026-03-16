(function () {
  "use strict";

  var DATA_BASE_URL = '/data/';
  var DATA_VERSION = '2026031601';

  function esc(str) {
    var el = document.createElement('span');
    el.textContent = str || '';
    return el.innerHTML;
  }

  function formatNumber(n) {
    return n ? n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '\u00A0') : '0';
  }

  function init() {
    // Charger villes.json
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
        document.getElementById('national-villes').textContent = villesAvecResultats.length;
        var avgPart = villesAvecResultats.length > 0 ? (totalParticipation / villesAvecResultats.length).toFixed(1) + '%' : '—';
        document.getElementById('national-participation').textContent = avgPart;
        document.getElementById('national-sous-titre').textContent =
          villesAvecResultats.length + ' villes sur ' + villes.length + ' — 15 et 22 mars 2026';

        if (villesAvecResultats.length === 0) {
          document.getElementById('national-villes-table').innerHTML =
            '<p style="text-align:center;color:var(--couleur-texte-secondaire);padding:2rem">Les résultats seront publiés le soir du scrutin.</p>';
          return;
        }

        // Trier par population / nom
        villesAvecResultats.sort(function (a, b) {
          return (a.nom || '').localeCompare(b.nom || '', 'fr');
        });

        // Tableau
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
        document.getElementById('national-sous-titre').textContent = 'Erreur de chargement';
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
