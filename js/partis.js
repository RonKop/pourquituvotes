(function() {
  "use strict";

  var DATA_VERSION = "2026040804";
  var partis = [];
  var radarChart = null;

  var AXES = [
    { key: "economie",    label: "Économie",    icon: "ph-chart-line-up" },
    { key: "social",      label: "Social",      icon: "ph-users" },
    { key: "immigration", label: "Immigration", icon: "ph-airplane-tilt" },
    { key: "europe",      label: "Europe",      icon: "ph-globe" },
    { key: "ecologie",    label: "Écologie",    icon: "ph-leaf" },
    { key: "securite",    label: "Sécurité",    icon: "ph-shield-check" }
  ];

  var FILTER_RANGES = {
    "tous":            function() { return true; },
    "extreme-gauche":  function(p) { return p.spectrePosition < 10; },
    "gauche":          function(p) { return p.spectrePosition >= 10 && p.spectrePosition < 40; },
    "centre":          function(p) { return p.spectrePosition >= 40 && p.spectrePosition <= 60; },
    "droite":          function(p) { return p.spectrePosition > 60 && p.spectrePosition <= 75; },
    "extreme-droite":  function(p) { return p.spectrePosition > 75; }
  };

  // ---- Load data ----
  fetch("/data/partis.json?v=" + DATA_VERSION)
    .then(function(r) { return r.json(); })
    .then(function(data) {
      partis = data.partis;
      init();
    })
    .catch(function(err) {
      console.error("Erreur chargement partis.json:", err);
    });

  function init() {
    renderSpectre();
    renderCards(partis);
    setupFilters();
    populateSelectors();
    setupComparateur();
  }

  // ============================================================
  // SPECTRE POLITIQUE
  // ============================================================
  function renderSpectre() {
    var track = document.querySelector(".partis-spectre__track");
    if (!track) return;
    track.innerHTML = "";

    // Sort by spectrePosition to stagger overlapping dots vertically
    var sorted = partis.slice().sort(function(a, b) { return a.spectrePosition - b.spectrePosition; });

    sorted.forEach(function(p) {
      var dot = document.createElement("div");
      dot.className = "partis-spectre__dot";
      dot.style.left = p.spectrePosition + "%";
      dot.style.backgroundColor = p.couleur;
      dot.setAttribute("tabindex", "0");
      dot.setAttribute("role", "button");
      dot.setAttribute("aria-label", p.sigle + " — " + p.nom + " (" + p.positionnement + ")");
      dot.textContent = p.sigle;

      var tooltip = document.createElement("span");
      tooltip.className = "partis-spectre__tooltip";
      tooltip.textContent = p.nom;
      dot.appendChild(tooltip);

      dot.addEventListener("click", function() {
        scrollToCard(p.id);
      });
      dot.addEventListener("keydown", function(e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          scrollToCard(p.id);
        }
      });

      track.appendChild(dot);
    });
  }

  function scrollToCard(id) {
    var card = document.querySelector('[data-parti="' + id + '"]');
    if (card) {
      card.scrollIntoView({ behavior: "smooth", block: "center" });
      // Briefly highlight
      card.style.boxShadow = "0 0 0 3px #002395";
      setTimeout(function() { card.style.boxShadow = ""; }, 1500);
    }
  }

  // ============================================================
  // CARDS
  // ============================================================
  function renderCards(filtered) {
    var grid = document.getElementById("partis-grid");
    if (!grid) return;
    grid.innerHTML = "";

    if (filtered.length === 0) {
      grid.innerHTML = '<p style="text-align:center;color:#64748b;padding:2rem;grid-column:1/-1;">Aucun parti dans cette catégorie.</p>';
      return;
    }

    filtered.forEach(function(p) {
      var card = document.createElement("article");
      card.className = "parti-card";
      card.setAttribute("data-parti", p.id);
      card.style.setProperty("--parti-couleur", p.couleur);
      card.setAttribute("tabindex", "0");
      card.setAttribute("role", "link");
      card.setAttribute("aria-label", p.nom + " — voir la fiche complète");
      card.style.cursor = "pointer";

      var html = "";

      // Header
      html += '<div class="parti-card__header">';
      html += '<div class="parti-card__sigle">' + esc(p.sigle) + '</div>';
      html += '<div class="parti-card__info">';
      html += '<h3 class="parti-card__nom"><a href="/partis/' + esc(p.id) + '/">' + esc(p.nom) + '</a></h3>';
      html += '<p class="parti-card__leader"><i class="ph ph-user" aria-hidden="true"></i> ' + esc(p.leader) + '</p>';
      html += '</div></div>';

      // Position bars
      html += '<div class="parti-card__positions">';
      AXES.forEach(function(ax) {
        var score = p.positions[ax.key] ? p.positions[ax.key].score : 0;
        var pct = score * 10;
        html += '<div class="parti-card__pos-row">';
        html += '<span class="parti-card__pos-label">' + esc(ax.label) + '</span>';
        html += '<div class="parti-card__pos-track"><div class="parti-card__pos-fill pos-bar--' + ax.key + '" style="width:' + pct + '%"></div></div>';
        html += '<span class="parti-card__pos-val">' + score + '</span>';
        html += '</div>';
      });
      html += '</div>';

      // Tags
      html += '<div class="parti-card__tags">';
      html += '<span class="parti-card__tag">' + esc(p.positionnement) + '</span>';
      if (p.ideologie) {
        p.ideologie.slice(0, 3).forEach(function(t) {
          html += '<span class="parti-card__tag">' + esc(t) + '</span>';
        });
      }
      html += '</div>';

      // Results summary
      html += '<div class="parti-card__resultats">';
      if (p.resultats) {
        if (p.resultats.presidentielle2022 && p.resultats.presidentielle2022.tour1) {
          html += '<span class="parti-card__resultat">Prés. 2022 : <strong>' + formatPct(p.resultats.presidentielle2022.tour1) + '</strong></span>';
        }
        if (p.resultats.europeennes2024 && p.resultats.europeennes2024.pourcentage) {
          html += '<span class="parti-card__resultat">Europ. 2024 : <strong>' + formatPct(p.resultats.europeennes2024.pourcentage) + '</strong></span>';
        }
        if (p.resultats.legislatives2024 && p.resultats.legislatives2024.sieges) {
          html += '<span class="parti-card__resultat">Légis. 2024 : <strong>' + p.resultats.legislatives2024.sieges + ' sièges</strong></span>';
        }
      }
      html += '</div>';

      card.innerHTML = html;

      // Click to navigate to party page
      card.addEventListener("click", function(e) {
        if (e.target.closest("a")) return;
        window.location.href = "/partis/" + p.id + "/";
      });
      card.addEventListener("keydown", function(e) {
        if (e.key === "Enter" || e.key === " ") {
          if (e.target.closest("a")) return;
          e.preventDefault();
          window.location.href = "/partis/" + p.id + "/";
        }
      });

      grid.appendChild(card);
    });
  }


  // ============================================================
  // FILTERS
  // ============================================================
  function setupFilters() {
    var btns = document.querySelectorAll(".partis-filters__btn");
    btns.forEach(function(btn) {
      btn.addEventListener("click", function() {
        btns.forEach(function(b) {
          b.classList.remove("partis-filters__btn--active");
          b.setAttribute("aria-pressed", "false");
        });
        btn.classList.add("partis-filters__btn--active");
        btn.setAttribute("aria-pressed", "true");

        var filter = btn.getAttribute("data-filter");
        var fn = FILTER_RANGES[filter] || FILTER_RANGES["tous"];
        var filtered = partis.filter(fn);
        renderCards(filtered);
      });
    });
  }

  // ============================================================
  // COMPARATEUR
  // ============================================================
  function populateSelectors() {
    var sel1 = document.getElementById("comp-parti1");
    var sel2 = document.getElementById("comp-parti2");
    if (!sel1 || !sel2) return;

    var sorted = partis.slice().sort(function(a, b) {
      return a.nom.localeCompare(b.nom);
    });

    sorted.forEach(function(p) {
      var opt1 = document.createElement("option");
      opt1.value = p.id;
      opt1.textContent = p.sigle + " — " + p.nom;
      sel1.appendChild(opt1);

      var opt2 = opt1.cloneNode(true);
      sel2.appendChild(opt2);
    });
  }

  function setupComparateur() {
    var btn = document.getElementById("comp-btn");
    if (!btn) return;

    btn.addEventListener("click", function() {
      var id1 = document.getElementById("comp-parti1").value;
      var id2 = document.getElementById("comp-parti2").value;

      if (!id1 || !id2) {
        alert("Veuillez sélectionner deux partis.");
        return;
      }
      if (id1 === id2) {
        alert("Veuillez sélectionner deux partis différents.");
        return;
      }

      var p1 = partis.find(function(p) { return p.id === id1; });
      var p2 = partis.find(function(p) { return p.id === id2; });
      if (!p1 || !p2) return;

      renderRadar(p1, p2);
      renderCompTable(p1, p2);

      var results = document.getElementById("comp-results");
      if (results) {
        results.hidden = false;
        results.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  }

  function renderRadar(p1, p2) {
    var canvas = document.getElementById("comp-radar");
    if (!canvas) return;

    var labels = AXES.map(function(a) { return a.label; });
    var data1 = AXES.map(function(a) { return p1.positions[a.key] ? p1.positions[a.key].score : 0; });
    var data2 = AXES.map(function(a) { return p2.positions[a.key] ? p2.positions[a.key].score : 0; });

    if (radarChart) {
      radarChart.destroy();
    }

    var c1 = p1.couleur;
    var c2 = p2.couleur;

    radarChart = new Chart(canvas, {
      type: "radar",
      data: {
        labels: labels,
        datasets: [
          {
            label: p1.sigle,
            data: data1,
            backgroundColor: hexToRgba(c1, 0.18),
            borderColor: c1,
            borderWidth: 2.5,
            pointBackgroundColor: c1,
            pointBorderColor: "#fff",
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7
          },
          {
            label: p2.sigle,
            data: data2,
            backgroundColor: hexToRgba(c2, 0.18),
            borderColor: c2,
            borderWidth: 2.5,
            pointBackgroundColor: c2,
            pointBorderColor: "#fff",
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          r: {
            min: 0,
            max: 10,
            ticks: {
              stepSize: 2,
              font: { size: 11, family: "'DM Sans', sans-serif" },
              backdropColor: "transparent"
            },
            grid: {
              color: "rgba(0,0,0,0.08)"
            },
            angleLines: {
              color: "rgba(0,0,0,0.08)"
            },
            pointLabels: {
              font: { size: 13, weight: "600", family: "'Montserrat', sans-serif" },
              color: getComputedStyle(document.documentElement).getPropertyValue("--couleur-texte").trim() || "#1e293b"
            }
          }
        },
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              font: { size: 13, weight: "600", family: "'Montserrat', sans-serif" },
              usePointStyle: true,
              pointStyle: "circle",
              padding: 20
            }
          },
          tooltip: {
            callbacks: {
              label: function(ctx) {
                return ctx.dataset.label + " : " + ctx.raw + "/10";
              }
            }
          }
        }
      }
    });
  }

  function renderCompTable(p1, p2) {
    var output = document.getElementById("comp-output");
    if (!output) return;

    var html = "";

    // Header row
    html += '<div class="partis-comp__row partis-comp__row-header" role="row">';
    html += '<span>Axe</span>';
    html += '<span style="text-align:center">' + esc(p1.sigle) + '</span>';
    html += '<span style="text-align:center">' + esc(p2.sigle) + '</span>';
    html += '</div>';

    AXES.forEach(function(ax) {
      var pos1 = p1.positions[ax.key] || { score: 0, resume: "" };
      var pos2 = p2.positions[ax.key] || { score: 0, resume: "" };

      html += '<div class="partis-comp__row" role="row">';

      // Axis info
      html += '<div>';
      html += '<div class="partis-comp__axis-label"><i class="ph ' + ax.icon + '" aria-hidden="true"></i> ' + esc(ax.label) + '</div>';
      html += '</div>';

      // Party 1
      html += '<div class="partis-comp__cell">';
      html += '<span class="partis-comp__score" style="background:' + p1.couleur + '">' + pos1.score + '</span>';
      html += '<span class="partis-comp__cell-label">' + esc(p1.sigle) + '</span>';
      html += '</div>';

      // Party 2
      html += '<div class="partis-comp__cell">';
      html += '<span class="partis-comp__score" style="background:' + p2.couleur + '">' + pos2.score + '</span>';
      html += '<span class="partis-comp__cell-label">' + esc(p2.sigle) + '</span>';
      html += '</div>';

      html += '</div>';

      // Description row
      html += '<div class="partis-comp__row" role="row" style="border:none;background:transparent;padding:0 1.25rem 0.6rem;margin-bottom:0.4rem;">';
      html += '<div style="grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:1rem;">';
      html += '<p style="font-size:0.8rem;line-height:1.5;color:var(--couleur-texte-secondaire,#64748b);margin:0;"><strong style="color:' + p1.couleur + '">' + esc(p1.sigle) + '</strong> : ' + esc(pos1.resume) + '</p>';
      html += '<p style="font-size:0.8rem;line-height:1.5;color:var(--couleur-texte-secondaire,#64748b);margin:0;"><strong style="color:' + p2.couleur + '">' + esc(p2.sigle) + '</strong> : ' + esc(pos2.resume) + '</p>';
      html += '</div></div>';
    });

    output.innerHTML = html;
  }

  // ============================================================
  // HELPERS
  // ============================================================
  function esc(s) {
    if (!s) return "";
    var d = document.createElement("div");
    d.appendChild(document.createTextNode(s));
    return d.innerHTML;
  }

  function formatPct(n) {
    if (n == null) return "—";
    return n.toFixed(1).replace(".", ",") + " %";
  }

  function hexToRgba(hex, alpha) {
    hex = hex.replace("#", "");
    if (hex.length === 3) {
      hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    }
    var r = parseInt(hex.substring(0, 2), 16);
    var g = parseInt(hex.substring(2, 4), 16);
    var b = parseInt(hex.substring(4, 6), 16);
    return "rgba(" + r + "," + g + "," + b + "," + alpha + ")";
  }

})();
