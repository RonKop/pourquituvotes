/* ============================================================
   #POURQUITUVOTES — Recherche burger menu (partagé)
   Script autonome pour les pages sans recherche propre.
   Ne s'initialise QUE si #mobile-menu-search existe.
   ============================================================ */
(function () {
  "use strict";

  var DATA_BASE_URL = "/data/";
  var DATA_VERSION = "2026021401";
  var VILLES = null;

  var searchInput = document.getElementById("mobile-menu-search");
  var suggestionsEl = document.getElementById("mobile-menu-suggestions");
  if (!searchInput || !suggestionsEl) return;

  var debounceTimer = null;

  function esc(str) {
    var d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  function chargerVilles() {
    if (VILLES) return Promise.resolve(VILLES);
    return fetch(DATA_BASE_URL + "villes.json?v=" + DATA_VERSION)
      .then(function (r) { return r.json(); })
      .then(function (data) { VILLES = data; return data; });
  }

  function rechercherVilles(terme) {
    if (!terme || terme.length < 1 || !VILLES) return [];
    var t = terme.toLowerCase().trim();
    return VILLES.filter(function (v) {
      return v.nom.toLowerCase().indexOf(t) !== -1 ||
             v.codePostal.indexOf(t) !== -1;
    });
  }

  function rechercherCandidats(terme) {
    if (!terme || terme.length < 2 || !VILLES) return [];
    var t = terme.toLowerCase().trim();
    var res = [];
    VILLES.forEach(function (v) {
      (v.candidats || []).forEach(function (c) {
        if (c.nom.toLowerCase().indexOf(t) !== -1) {
          res.push({
            candidatId: c.id,
            candidatNom: c.nom,
            villeId: v.id,
            villeNom: v.nom
          });
        }
      });
    });
    return res;
  }

  function afficher(val) {
    var villes = rechercherVilles(val).slice(0, 8);
    var candidats = rechercherCandidats(val).slice(0, 5);

    if (villes.length === 0 && candidats.length === 0) {
      suggestionsEl.innerHTML = "";
      suggestionsEl.hidden = true;
      return;
    }

    var html = villes.map(function (v) {
      return '<a class="mobile-menu-suggestion-item" href="/municipales/2026/?ville=' + encodeURIComponent(v.id) + '">' +
        '<i class="ph ph-map-pin"></i>' +
        '<span>' + esc(v.nom) + '</span>' +
        '<span class="mobile-menu-suggestion-cp">' + v.codePostal + '</span>' +
        '</a>';
    }).join("");

    if (candidats.length > 0) {
      if (villes.length > 0) {
        html += '<div style="padding:6px 16px;font-size:0.72rem;font-weight:700;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.05em;border-top:1px solid rgba(255,255,255,0.1)">Candidats</div>';
      }
      candidats.forEach(function (r) {
        html += '<a class="mobile-menu-suggestion-item" href="/municipales/2026/candidat.html?ville=' + encodeURIComponent(r.villeId) + '&candidat=' + encodeURIComponent(r.candidatId) + '">' +
          '<i class="ph ph-user"></i>' +
          '<span>' + esc(r.candidatNom) + '</span>' +
          '<span class="mobile-menu-suggestion-cp">' + esc(r.villeNom) + '</span>' +
          '</a>';
      });
    }

    suggestionsEl.innerHTML = html;
    suggestionsEl.hidden = false;
  }

  searchInput.addEventListener("input", function () {
    clearTimeout(debounceTimer);
    var val = searchInput.value.trim();
    debounceTimer = setTimeout(function () {
      if (!val || val.length < 2) {
        suggestionsEl.innerHTML = "";
        suggestionsEl.hidden = true;
        return;
      }
      chargerVilles().then(function () { afficher(val); });
    }, 200);
  });

  searchInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      var firstLink = suggestionsEl.querySelector("a.mobile-menu-suggestion-item");
      if (firstLink) {
        firstLink.click();
      } else {
        var val = searchInput.value.trim();
        if (val.length >= 2) {
          chargerVilles().then(function () {
            afficher(val);
            if (suggestionsEl.hidden && window.PQTV_Analytics && PQTV_Analytics.renderNoResult) {
              PQTV_Analytics.renderNoResult(suggestionsEl, val);
              suggestionsEl.hidden = false;
            }
          });
        }
      }
    }
  });
})();
