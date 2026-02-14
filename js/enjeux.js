(function () {
  "use strict";

  var DATA_BASE_URL = "/data/";
  var DATA_VERSION = "2026021302";

  var CATEGORIE_META = {
    "securite": { icon: "ph-shield-check", nom: "S\u00e9curit\u00e9 & Pr\u00e9vention" },
    "transports": { icon: "ph-bus", nom: "Transports & Mobilit\u00e9" },
    "environnement": { icon: "ph-leaf", nom: "Environnement & Transition \u00e9cologique" },
    "education": { icon: "ph-graduation-cap", nom: "\u00c9ducation & Jeunesse" },
    "democratie": { icon: "ph-bank", nom: "D\u00e9mocratie & Vie citoyenne" },
    "logement": { icon: "ph-house", nom: "Logement" },
    "economie": { icon: "ph-briefcase", nom: "\u00c9conomie & Emploi" },
    "sante": { icon: "ph-heartbeat", nom: "Sant\u00e9 & Acc\u00e8s aux soins" },
    "solidarite": { icon: "ph-handshake", nom: "Solidarit\u00e9 & \u00c9galit\u00e9" },
    "urbanisme": { icon: "ph-buildings", nom: "Urbanisme & Cadre de vie" },
    "culture": { icon: "ph-palette", nom: "Culture & Patrimoine" },
    "sport": { icon: "ph-soccer-ball", nom: "Sport & Loisirs" }
  };

  var CATEGORIE_ORDRE = [
    "securite", "transports", "logement", "education", "environnement",
    "sante", "democratie", "economie", "culture", "sport", "urbanisme", "solidarite"
  ];

  function esc(str) {
    var div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  function renderGrid(statsData) {
    var grid = document.getElementById("enjeux-grid");
    if (!grid) return;

    var catCounts = {};
    (statsData.categories || []).forEach(function (cat) {
      catCounts[cat.id] = cat.count;
    });

    var html = CATEGORIE_ORDRE.map(function (catId, idx) {
      var meta = CATEGORIE_META[catId] || { icon: "ph-tag", nom: catId };
      var count = catCounts[catId] || 0;
      var cls = (idx === 0 || idx === CATEGORIE_ORDRE.length - 1) ? " tendance-card--wide" : "";
      return '<a href="/thematique.html?theme=' + catId + '" class="tendance-card' + cls + '">' +
        '<i class="ph ' + meta.icon + ' tendance-card__icon" aria-hidden="true"></i>' +
        '<div class="tendance-card__name">' + esc(meta.nom) + '</div>' +
        '<div class="tendance-card__count">' + count + ' propositions</div>' +
        '<span class="tendance-card__arrow">Explorer <i class="ph ph-arrow-right" aria-hidden="true"></i></span>' +
        '</a>';
    }).join("");

    grid.innerHTML = html;
  }

  function init() {
    fetch(DATA_BASE_URL + "stats-global.json?v=" + DATA_VERSION)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        renderGrid(data);
      })
      .catch(function (err) {
        console.error("Erreur chargement stats:", err);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
