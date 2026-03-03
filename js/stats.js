(function () {
  "use strict";

  var DATA = null;

  // === Animated counter ===
  function animateCounter(el, target, duration) {
    var start = 0;
    var startTime = null;
    function step(ts) {
      if (!startTime) startTime = ts;
      var progress = Math.min((ts - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
      el.textContent = Math.round(start + (target - start) * eased).toLocaleString("fr-FR");
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  // === Render hero counters ===
  function renderCounters(national) {
    animateCounter(document.getElementById("counter-villes"), national.total_villes, 1200);
    animateCounter(document.getElementById("counter-candidats"), national.total_candidats, 1400);
    animateCounter(document.getElementById("counter-mesures"), national.total_mesures, 1600);
  }

  // === Render theme bars ===
  function renderThemeBars(themes) {
    var container = document.getElementById("bars-themes");
    if (!container || !themes.length) return;

    var maxVal = themes[0].total_mesures;
    var html = "";
    for (var i = 0; i < themes.length; i++) {
      var t = themes[i];
      var pct = Math.round((t.total_mesures / maxVal) * 100);
      html +=
        '<div class="stats-bar">' +
          '<span class="stats-bar__label">' + t.nom + '</span>' +
          '<div class="stats-bar__track">' +
            '<div class="stats-bar__fill" style="width:' + pct + '%"></div>' +
          '</div>' +
          '<span class="stats-bar__count">' + t.total_mesures.toLocaleString("fr-FR") + '</span>' +
        '</div>';
    }
    container.innerHTML = html;
  }

  // === Render top 10 table ===
  function renderTop10(top10) {
    var tbody = document.getElementById("tbody-top10");
    if (!tbody) return;

    var html = "";
    for (var i = 0; i < top10.length; i++) {
      var c = top10[i];
      var rankClass = i < 3 ? "stats-table__rank stats-table__rank--top3" : "stats-table__rank";
      var slug = c.ville_id.replace("-2026", "");
      html +=
        '<tr>' +
          '<td class="' + rankClass + '">' + (i + 1) + '</td>' +
          '<td><a href="/municipales-2026/' + slug + '/candidats/' + c.id + '/" style="color:inherit;text-decoration:none;font-weight:600">' + c.nom + '</a></td>' +
          '<td>' + c.ville + '</td>' +
          '<td class="stats-table__value">' + c.total_mesures + '</td>' +
          '<td class="stats-table__value">' + c.pct_mesures_chiffrees + '%</td>' +
        '</tr>';
    }
    tbody.innerHTML = html;
  }

  // === Chart.js: themes donut ===
  function renderThemeChart(themes) {
    var ctx = document.getElementById("chart-themes");
    if (!ctx || typeof Chart === "undefined") return;

    var colors = [
      "#002395", "#ED2939", "#4a5f94", "#10b981", "#f59e0b",
      "#6366f1", "#ec4899", "#14b8a6", "#f97316", "#8b5cf6",
      "#06b6d4", "#84cc16"
    ];

    new Chart(ctx.getContext("2d"), {
      type: "doughnut",
      data: {
        labels: themes.map(function (t) { return t.nom; }),
        datasets: [{
          data: themes.map(function (t) { return t.total_mesures; }),
          backgroundColor: colors.slice(0, themes.length),
          borderWidth: 2,
          borderColor: "#fff"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              font: { family: "'DM Sans', sans-serif", size: 11 },
              padding: 12,
              usePointStyle: true,
              pointStyleWidth: 10
            }
          },
          tooltip: {
            callbacks: {
              label: function (item) {
                var total = item.dataset.data.reduce(function (a, b) { return a + b; }, 0);
                var pct = Math.round(item.raw / total * 100);
                return item.label + " : " + item.raw + " (" + pct + "%)";
              }
            }
          }
        }
      }
    });
  }

  // === Chart.js: precision bar chart ===
  function renderPrecisionChart(top10) {
    var ctx = document.getElementById("chart-precision");
    if (!ctx || typeof Chart === "undefined") return;

    // Show pct chiffré for top 10
    var labels = top10.map(function (c) {
      var parts = c.nom.split(" ");
      return parts[parts.length - 1]; // nom de famille
    });

    new Chart(ctx.getContext("2d"), {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "% mesures chiffr\u00e9es",
          data: top10.map(function (c) { return c.pct_mesures_chiffrees; }),
          backgroundColor: "rgba(0, 35, 149, 0.75)",
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        indexAxis: "y",
        scales: {
          x: {
            beginAtZero: true,
            max: 100,
            ticks: {
              callback: function (v) { return v + "%"; },
              font: { family: "'DM Sans', sans-serif" }
            },
            grid: { color: "rgba(0,0,0,0.05)" }
          },
          y: {
            ticks: { font: { family: "'DM Sans', sans-serif", weight: "600" } },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function (item) { return item.raw + "% de mesures chiffr\u00e9es"; }
            }
          }
        }
      }
    });
  }

  // === Ville explorer ===
  function setupVilleExplorer(villes) {
    var select = document.getElementById("ville-select");
    if (!select) return;

    // Trier les villes par nom
    var sorted = villes.slice().sort(function (a, b) {
      return a.nom.localeCompare(b.nom, "fr");
    });

    for (var i = 0; i < sorted.length; i++) {
      var v = sorted[i];
      if (v.total_mesures === 0) continue;
      var opt = document.createElement("option");
      opt.value = v.id;
      opt.textContent = v.nom + " (" + v.total_mesures + " mesures)";
      select.appendChild(opt);
    }

    select.addEventListener("change", function () {
      var villeId = this.value;
      if (!villeId) {
        document.getElementById("ville-detail").hidden = true;
        return;
      }
      renderVilleDetail(villeId, villes);
    });
  }

  function renderVilleDetail(villeId, villes) {
    var ville = null;
    for (var i = 0; i < villes.length; i++) {
      if (villes[i].id === villeId) { ville = villes[i]; break; }
    }
    if (!ville) return;

    var detail = document.getElementById("ville-detail");
    detail.hidden = false;

    document.getElementById("ville-detail-nom").textContent = ville.nom;
    document.getElementById("ville-detail-total").textContent =
      ville.total_mesures + " mesures \u2014 " + ville.nb_candidats + " candidats";

    var slug = villeId.replace("-2026", "");
    var link = document.getElementById("ville-detail-link");
    link.href = "/municipales-2026/" + slug + "/";

    // Tableau candidats de la ville
    var candidats = ville.candidats.slice().sort(function (a, b) {
      return b.metriques.total_mesures - a.metriques.total_mesures;
    });

    var tbody = document.getElementById("ville-tbody");
    var html = "";
    for (var i = 0; i < candidats.length; i++) {
      var c = candidats[i];
      var m = c.metriques;
      if (m.total_mesures === 0) continue;
      var couv = m.couverture_sous_themes + "/" + m.couverture_sous_themes_max;
      html +=
        '<tr>' +
          '<td style="font-weight:600">' + c.nom + '</td>' +
          '<td>' + (c.liste || "").substring(0, 35) + '</td>' +
          '<td class="stats-table__value">' + m.total_mesures + '</td>' +
          '<td class="stats-table__value">' + couv + '</td>' +
          '<td class="stats-table__value">' + m.pct_mesures_chiffrees + '%</td>' +
        '</tr>';
    }
    tbody.innerHTML = html;
  }

  // === Init ===
  function init() {
    fetch("/data/metriques.json")
      .then(function (r) {
        if (!r.ok) throw new Error("Erreur chargement metriques: " + r.status);
        return r.json();
      })
      .then(function (data) {
        DATA = data;
        renderCounters(data.national);
        renderThemeBars(data.national.themes_ranking);
        renderTop10(data.national.top10_candidats);
        renderThemeChart(data.national.themes_ranking);
        renderPrecisionChart(data.national.top10_candidats);
        setupVilleExplorer(data.villes);
      })
      .catch(function (err) {
        console.error("Stats: erreur chargement données", err);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
