(function () {
  "use strict";

  // === Configuration ===
  var DATA_BASE_URL = '/data/';
  var DATA_VERSION = '2026031501';
  var BASE_URL = 'https://pourquituvotes.fr';

  // Couleurs par nuance politique
  var NUANCE_COLORS = {
    'LUG': '#e11d48',   // Gauche unie
    'LFI': '#cc2443',   // France Insoumise
    'LEXG': '#b91c1c',  // Extrême gauche
    'LUD': '#1d4ed8',   // Droite unie
    'LUC': '#f59e0b',   // Centre
    'LUXD': '#1e3a5f',  // Extrême droite unie
    'LEXD': '#374151',  // Extrême droite
    'LRN': '#1e3a5f',   // RN
    'LDVG': '#f43f5e',  // Divers gauche
    'LDVD': '#3b82f6',  // Divers droite
    'LDVC': '#eab308',  // Divers centre
    'LECO': '#22c55e',  // Écologistes
    'LDIV': '#6b7280',  // Divers
  };

  var DEFAULT_COLOR = '#94a3b8';

  // === Utilitaires ===
  function esc(str) {
    var el = document.createElement('span');
    el.textContent = str || '';
    return el.innerHTML;
  }

  function formatNumber(n) {
    return n ? n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '\u00A0') : '0';
  }

  function getVilleIdFromUrl() {
    // URL: /municipales-2026/{ville}/resultats/
    var parts = window.location.pathname.split('/').filter(Boolean);
    var idx = parts.indexOf('municipales-2026');
    if (idx !== -1 && parts[idx + 1]) {
      return parts[idx + 1];
    }
    // Fallback: query param
    var params = new URLSearchParams(window.location.search);
    return params.get('ville') || null;
  }

  function getCandidatColor(candidat) {
    if (!candidat) return DEFAULT_COLOR;
    var nuance = candidat.nuanceOfficielle || '';
    return NUANCE_COLORS[nuance] || DEFAULT_COLOR;
  }

  // === Chargement données ===
  function chargerDonnees(villeId) {
    return fetch(DATA_BASE_URL + 'elections/' + villeId + '-2026.json?v=' + DATA_VERSION)
      .then(function (r) {
        if (!r.ok) throw new Error('Erreur chargement: ' + r.status);
        return r.json();
      });
  }

  // === Rendu ===
  var currentTour = 1;
  var electionData = null;
  var candidatsMap = {};

  function buildCandidatsMap(candidats) {
    var map = {};
    for (var i = 0; i < candidats.length; i++) {
      map[candidats[i].id] = candidats[i];
    }
    return map;
  }

  function renderHero(tourData, ville, status) {
    var titre = document.getElementById('resultats-titre');
    var sousTitre = document.getElementById('resultats-sous-titre');
    var statusBadge = document.getElementById('resultats-status-badge');

    var hasT2 = electionData && electionData.resultats && electionData.resultats.tour2;
    var tourLabel = hasT2 ? (currentTour === 1 ? '1er tour' : '2nd tour') : '';
    titre.textContent = 'Résultats municipales 2026 — ' + ville;
    var dateStr = new Date(tourData.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
    sousTitre.textContent = tourLabel ? (tourLabel + ' — ' + dateStr) : dateStr;

    var badgeClass = status === 'definitif' ? 'badge--definitif' : 'badge--provisoire';
    var badgeLabel = status === 'definitif' ? 'Résultats définitifs' : 'Résultats provisoires';
    statusBadge.innerHTML = '<span class="badge ' + badgeClass + '">' + esc(badgeLabel) + '</span>';

    // Stats
    document.getElementById('stat-participation').textContent = tourData.tauxParticipation + '%';
    document.getElementById('stat-inscrits').textContent = formatNumber(tourData.inscrits);
    document.getElementById('stat-exprimes').textContent = formatNumber(tourData.exprimes);

    // Breadcrumb
    var villeId = getVilleIdFromUrl();
    var bcVille = document.getElementById('breadcrumb-ville');
    var bcVilleNom = document.getElementById('breadcrumb-ville-nom');
    if (bcVille) bcVille.href = '/municipales-2026/' + villeId + '/';
    if (bcVilleNom) bcVilleNom.textContent = ville;

    var bcCurrent = document.getElementById('breadcrumb-current');
    if (bcCurrent) bcCurrent.href = '/municipales-2026/' + villeId + '/resultats/';
  }

  function renderTableau(tourData, villeId) {
    var container = document.getElementById('resultats-table');
    var html = '';

    var candidats = tourData.candidats || [];
    // Déjà triés par voix décroissant normalement
    candidats.sort(function (a, b) { return b.voix - a.voix; });

    var maxVoix = candidats.length > 0 ? candidats[0].voix : 1;

    for (var i = 0; i < candidats.length; i++) {
      var rc = candidats[i];
      var cand = candidatsMap[rc.id] || {};
      var color = getCandidatColor(cand);
      var isElu = rc.elu;
      var pct = rc.pourcentage;
      var barWidth = Math.max(2, (rc.voix / maxVoix) * 100);

      var badges = '';
      if (isElu) {
        badges += ' <span class="badge badge--elu"><i class="ph ph-check-circle"></i> Élu(e)</span>';
      } else if (rc.qualifieT2 && currentTour === 1) {
        badges += ' <span class="badge badge--qualifie"><i class="ph ph-arrow-right"></i> Qualifié(e) T2</span>';
      } else if (currentTour === 1 && !rc.qualifieT2) {
        badges += ' <span class="badge badge--elimine">Éliminé(e)</span>';
      }

      var rowClass = 'resultats-table__row' + (isElu ? ' resultats-table__row--elu' : '');
      var candLink = '/municipales-2026/' + esc(villeId) + '/candidats/' + esc(rc.id) + '/';

      html += '<div class="' + rowClass + '" role="row">';
      html += '  <div class="resultats-table__rang" role="cell">' + (i + 1) + '</div>';
      html += '  <div class="resultats-table__info" role="cell">';
      html += '    <div class="resultats-table__nom"><a href="' + candLink + '">' + esc(cand.nom || rc.id) + '</a>' + badges + '</div>';
      html += '    <div class="resultats-table__liste">' + esc(cand.liste || '') + '</div>';
      html += '    <div class="resultats-table__bar-wrap"><div class="resultats-table__bar-bg"><div class="resultats-table__bar" style="background:' + color + ';width:0%" data-width="' + barWidth + '%"></div></div></div>';
      html += '  </div>';
      html += '  <div class="resultats-table__scores" role="cell">';
      html += '    <div class="resultats-table__pct">' + pct.toFixed(2) + '%</div>';
      html += '    <div class="resultats-table__voix">' + formatNumber(rc.voix) + ' voix</div>';
      html += '  </div>';
      html += '</div>';
    }

    container.innerHTML = html;

    // Animer les barres après rendu
    requestAnimationFrame(function () {
      var bars = container.querySelectorAll('.resultats-table__bar');
      for (var j = 0; j < bars.length; j++) {
        bars[j].style.width = bars[j].getAttribute('data-width');
      }
    });
  }

  function renderFusions(tourData) {
    var fusionsSection = document.getElementById('resultats-fusions');
    var content = document.getElementById('resultats-fusions-content');

    var fusions = tourData.fusionsListes || [];
    if (fusions.length === 0) {
      fusionsSection.hidden = true;
      return;
    }

    fusionsSection.hidden = false;
    var html = '';
    for (var i = 0; i < fusions.length; i++) {
      var f = fusions[i];
      var principal = candidatsMap[f.listePrincipale] || {};
      var fusionnees = (f.listesFusionnees || []).map(function (id) {
        return (candidatsMap[id] || {}).nom || id;
      });
      html += '<div class="resultats-fusion">';
      html += '  <i class="ph ph-git-merge resultats-fusion__icon"></i>';
      html += '  <div class="resultats-fusion__text"><strong>' + esc(f.nomFusion || 'Fusion') + '</strong> — ' + esc(principal.nom || f.listePrincipale) + ' + ' + fusionnees.map(esc).join(', ') + '</div>';
      html += '</div>';
    }
    content.innerHTML = html;
  }

  function renderParticipation(tourData) {
    var ctx = document.getElementById('participation-chart');
    if (!ctx) return;

    var votants = tourData.votants - tourData.blancs - tourData.nuls;
    var data = {
      labels: ['Votes exprimés', 'Blancs', 'Nuls', 'Abstentions'],
      datasets: [{
        data: [tourData.exprimes, tourData.blancs, tourData.nuls, tourData.abstentions],
        backgroundColor: ['#002395', '#94a3b8', '#cbd5e1', '#e2e8f0'],
        borderWidth: 2,
        borderColor: '#fff',
      }]
    };

    // Détruire le chart existant s'il y en a un
    if (window._participationChart) {
      window._participationChart.destroy();
    }

    window._participationChart = new Chart(ctx, {
      type: 'doughnut',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: true,
        cutout: '55%',
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function (context) {
                var label = context.label || '';
                var value = context.raw || 0;
                var pct = ((value / tourData.inscrits) * 100).toFixed(1);
                return label + ' : ' + formatNumber(value) + ' (' + pct + '%)';
              }
            }
          }
        }
      }
    });

    // Détails texte
    var details = document.getElementById('participation-details');
    var items = [
      { color: '#002395', label: 'Votes exprimés', value: tourData.exprimes },
      { color: '#94a3b8', label: 'Blancs', value: tourData.blancs },
      { color: '#cbd5e1', label: 'Nuls', value: tourData.nuls },
      { color: '#e2e8f0', label: 'Abstentions', value: tourData.abstentions },
    ];
    var detailsHtml = '';
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      var pct = ((it.value / tourData.inscrits) * 100).toFixed(1);
      detailsHtml += '<div class="resultats-participation__detail">';
      detailsHtml += '  <span class="resultats-participation__dot" style="background:' + it.color + '"></span>';
      detailsHtml += '  <span class="resultats-participation__detail-label">' + esc(it.label) + '</span>';
      detailsHtml += '  <span class="resultats-participation__detail-value">' + formatNumber(it.value) + ' (' + pct + '%)</span>';
      detailsHtml += '</div>';
    }
    details.innerHTML = detailsHtml;
  }

  function renderTour(tourNum) {
    currentTour = tourNum;
    var resultats = electionData.resultats || {};
    var tourKey = 'tour' + tourNum;
    var tourData = resultats[tourKey];

    if (!tourData) {
      document.getElementById('resultats-table').innerHTML = '<p class="resultats-table__loading">Pas de résultats disponibles pour ce tour.</p>';
      return;
    }

    var ville = electionData.ville;
    var villeId = getVilleIdFromUrl();

    renderHero(tourData, ville, resultats.status);
    renderTableau(tourData, villeId);
    renderFusions(tourData);
    renderParticipation(tourData);

    // Titre de section
    var sectionTitre = document.getElementById('resultats-section-titre');
    sectionTitre.textContent = 'Classement des candidats — ' + (tourNum === 1 ? '1er tour' : '2nd tour');

    // CTA
    var ctaComparer = document.getElementById('resultats-cta-comparer');
    var ctaVille = document.getElementById('resultats-cta-ville');
    if (ctaComparer) ctaComparer.href = '/municipales-2026/' + villeId + '/';
    if (ctaVille) ctaVille.textContent = ville;

    // Onglets actif
    var btns = document.querySelectorAll('.resultats-onglets__btn');
    for (var i = 0; i < btns.length; i++) {
      var t = parseInt(btns[i].getAttribute('data-tour'));
      if (t === tourNum) {
        btns[i].classList.add('resultats-onglets__btn--actif');
      } else {
        btns[i].classList.remove('resultats-onglets__btn--actif');
      }
    }

    // Analytics
    if (window.PQTV_Analytics && window.PQTV_Analytics.trackEvent) {
      window.PQTV_Analytics.trackEvent('results_viewed', { ville: villeId, tour: tourNum });
    }
  }

  function setupOnglets() {
    var btns = document.querySelectorAll('.resultats-onglets__btn');
    for (var i = 0; i < btns.length; i++) {
      btns[i].addEventListener('click', function () {
        var tour = parseInt(this.getAttribute('data-tour'));
        renderTour(tour);
      });
    }
  }

  function setupShare() {
    var shareBtn = document.getElementById('resultats-cta-share');
    if (!shareBtn) return;

    if (navigator.share) {
      shareBtn.hidden = false;
      shareBtn.addEventListener('click', function (e) {
        e.preventDefault();
        var ville = electionData ? electionData.ville : 'Ville';
        navigator.share({
          title: 'Résultats municipales 2026 — ' + ville,
          text: 'Découvrez les résultats des municipales 2026 à ' + ville + ' sur #POURQUITUVOTES',
          url: window.location.href,
        }).catch(function () { /* user cancelled */ });
      });
    }
  }

  // === Init ===
  function init() {
    var villeId = getVilleIdFromUrl();
    if (!villeId) {
      document.getElementById('resultats-titre').textContent = 'Ville non trouvée';
      return;
    }

    chargerDonnees(villeId).then(function (data) {
      electionData = data;
      candidatsMap = buildCandidatsMap(data.candidats || []);

      var resultats = data.resultats;
      if (!resultats || (!resultats.tour1 && !resultats.tour2)) {
        document.getElementById('resultats-titre').textContent = 'Résultats non encore disponibles';
        document.getElementById('resultats-sous-titre').textContent = data.ville || villeId;
        document.getElementById('resultats-table').innerHTML = '<p class="resultats-table__loading">Les résultats seront publiés le soir du scrutin.</p>';
        return;
      }

      // Afficher onglets si T2 disponible
      if (resultats.tour2) {
        document.getElementById('resultats-onglets').hidden = false;
      }

      setupOnglets();
      setupShare();

      // Afficher le tour le plus récent par défaut
      var defaultTour = resultats.tour2 ? 2 : 1;
      renderTour(defaultTour);

    }).catch(function (err) {
      console.error('Erreur chargement résultats:', err);
      document.getElementById('resultats-titre').textContent = 'Erreur de chargement';
      document.getElementById('resultats-table').innerHTML = '<p class="resultats-table__loading">Impossible de charger les résultats. Réessayez plus tard.</p>';
    });
  }

  // Lancer à DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
