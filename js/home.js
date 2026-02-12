(function () {
  "use strict";

  // === Data (chargé depuis JSON) ===
  var VILLES = [];
  var DATA_BASE_URL = '/data/';
  var DATA_VERSION = '2026021002';

  var DATE_SCRUTIN = new Date("2026-03-15T08:00:00");

  // SVG drapeau fran\u00e7ais (compatible tous OS)
  var FLAG_FR_SVG = '<svg width="28" height="20" viewBox="0 0 3 2" style="border-radius:3px;vertical-align:middle" aria-label="Drapeau fran\u00e7ais"><rect width="1" height="2" fill="#002395"/><rect x="1" width="1" height="2" fill="#fff"/><rect x="2" width="1" height="2" fill="#ED2939"/></svg>';

  // Tendances : totaux France enti\u00e8re (toutes villes confondues)
  var TENDANCES_FRANCE = [
    { icon: "ph-house", nom: "Logement", slug: "logement", count: 142 },
    { icon: "ph-shield-check", nom: "S\u00e9curit\u00e9", slug: "securite", count: 118 },
    { icon: "ph-bus", nom: "Transports", slug: "transports", count: 105 },
    { icon: "ph-leaf", nom: "Environnement", slug: "environnement", count: 98 },
    { icon: "ph-graduation-cap", nom: "\u00c9ducation", slug: "education", count: 87 },
    { icon: "ph-briefcase", nom: "\u00c9conomie", slug: "economie", count: 76 }
  ];

  // === Utility ===
  function esc(str) {
    var div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // === Countdown (m\u00eame format que index.html) ===
  function updateCountdown() {
    var now = new Date();
    var diff = DATE_SCRUTIN.getTime() - now.getTime();

    var joursEl = document.getElementById("countdown-jours");
    var heuresEl = document.getElementById("countdown-heures");
    var minutesEl = document.getElementById("countdown-minutes");
    var secondesEl = document.getElementById("countdown-secondes");
    var timelineJours = document.getElementById("timeline-jours");

    if (diff <= 0) {
      if (joursEl) joursEl.textContent = "0";
      if (heuresEl) heuresEl.textContent = "0";
      if (minutesEl) minutesEl.textContent = "0";
      if (secondesEl) secondesEl.textContent = "0";
      if (timelineJours) timelineJours.textContent = "J-0";
      return;
    }

    var jours = Math.floor(diff / 86400000);
    var heures = Math.floor((diff % 86400000) / 3600000);
    var minutes = Math.floor((diff % 3600000) / 60000);
    var secondes = Math.floor((diff % 60000) / 1000);

    if (joursEl) joursEl.textContent = jours;
    if (heuresEl) heuresEl.textContent = heures;
    if (minutesEl) minutesEl.textContent = minutes;
    if (secondesEl) secondesEl.textContent = secondes;
    if (timelineJours) timelineJours.textContent = "J-" + jours;
  }

  // === Timeline Stats ===
  function updateTimelineStats() {
    var totalCandidats = 0;
    var totalComplets = 0;
    var totalPropositions = 0;

    VILLES.forEach(function (v) {
      var s = v.stats || {};
      totalCandidats += s.candidats || 0;
      totalComplets += s.complets || 0;
      totalPropositions += s.propositions || 0;
    });

    var pct = totalCandidats > 0 ? Math.round((totalComplets / totalCandidats) * 100) : 0;
    var fill = document.getElementById("timeline-progress-fill");
    var text = document.getElementById("timeline-progress-text");
    var propEl = document.getElementById("timeline-propositions");

    if (fill) fill.style.width = pct + "%";
    if (text) text.textContent = pct + "%";
    if (propEl) propEl.textContent = totalPropositions;

    var progressBar = document.querySelector(".timeline__progress");
    if (progressBar) {
      progressBar.setAttribute("aria-valuenow", pct);
    }
  }

  // === Elections Grid ===
  function renderElections() {
    var grid = document.getElementById("elections-grid");
    if (!grid) return;

    var featured = VILLES.slice().sort(function (a, b) {
      return (b.stats ? b.stats.propositions : 0) - (a.stats ? a.stats.propositions : 0);
    });

    var cards = [];

    // Card 1: Paris (featured)
    var paris = VILLES.find(function (v) { return v.id === "paris"; });
    if (paris) {
      cards.push(createFeaturedCard(paris));
    }

    // Card 2: Best non-Paris
    var second = featured.find(function (v) { return v.id !== "paris" && (v.stats ? v.stats.propositions : 0) > 20; });
    if (second) {
      cards.push(createFeaturedCard(second));
    }

    // Card 3: Presidentielle (coming)
    cards.push(createComingCard(FLAG_FR_SVG, "PR\u00c9SIDENTIELLE 2027", "France 2027"));

    grid.innerHTML = cards.join("");
  }

  function createFeaturedCard(ville) {
    var s = ville.stats || {};
    return '<a href="/municipales/2026/?ville=' + ville.id + '" class="election-card election-card--featured">' +
      '<span class="election-card__badge election-card__badge--available"><i class="ph ph-check-circle" aria-hidden="true"></i> Disponible</span>' +
      '<div class="election-card__icon"><i class="ph ph-bank" aria-hidden="true"></i></div>' +
      '<div class="election-card__type">MUNICIPALES 2026</div>' +
      '<div class="election-card__name">' + esc(ville.nom) + '</div>' +
      '<div class="election-card__stats">' +
      '<span class="election-card__stat"><i class="ph ph-users" aria-hidden="true"></i> ' + (s.candidats || 0) + ' candidats</span>' +
      '<span class="election-card__stat"><i class="ph ph-file-text" aria-hidden="true"></i> ' + (s.propositions || 0) + ' propositions</span>' +
      '<span class="election-card__stat"><i class="ph ph-squares-four" aria-hidden="true"></i> ' + (s.themes || 0) + ' th\u00e8mes</span>' +
      '</div>' +
      '<span class="election-card__cta">Comparer les programmes <i class="ph ph-arrow-right" aria-hidden="true"></i></span>' +
      '</a>';
  }

  function createComingCard(icon, type, name) {
    return '<a href="presidentielle/2027/" class="home-alertes">' +
      '<div class="home-alertes__icon">' + icon + '</div>' +
      '<div class="home-alertes__texte">' +
        '<strong>' + esc(type) + '</strong>' +
        '<p>Parce que les enjeux nationaux se pr\u00e9parent aujourd\u2019hui, nous commen\u00e7ons d\u00e9j\u00e0 \u00e0 scanner les premi\u00e8res d\u00e9clarations pour la Pr\u00e9sidentielle 2027. Retrouvez prochainement le comparateur int\u00e9gral pour d\u00e9crypter l\u2019avenir de la France.</p>' +
      '</div>' +
      '<span class="home-alertes__btn">En savoir plus <i class="ph ph-arrow-right" aria-hidden="true"></i></span>' +
      '</a>';
  }

  // === Tendances (totaux France) ===
  function renderTendances() {
    var grid = document.getElementById("tendances-grid");
    var selectContainer = document.getElementById("tendances-ville");
    if (!grid) return;

    // Masquer le s\u00e9lecteur de ville (on affiche la France enti\u00e8re)
    if (selectContainer && selectContainer.parentNode) {
      selectContainer.parentNode.style.display = "none";
    }

    grid.innerHTML = TENDANCES_FRANCE.map(function (t, idx) {
      var cls = (idx === 0 || idx === TENDANCES_FRANCE.length - 1) ? " tendance-card--wide" : "";
      return '<a href="/municipales/2026/?categorie=' + t.slug + '" class="tendance-card' + cls + '">' +
        '<i class="ph ' + t.icon + ' tendance-card__icon" aria-hidden="true"></i>' +
        '<div class="tendance-card__name">' + esc(t.nom) + '</div>' +
        '<div class="tendance-card__count">' + t.count + ' propositions</div>' +
        '<span class="tendance-card__arrow">Voir <i class="ph ph-arrow-right" aria-hidden="true"></i></span>' +
        '</a>';
    }).join("");
  }

  // === Search Autocomplete ===
  function initSearch() {
    var input = document.getElementById("search-input");
    var btn = document.getElementById("search-btn");
    var dropdown = document.getElementById("suggestions-dropdown");
    if (!input || !dropdown) return;

    var debounceTimer = null;
    var activeIndex = -1;

    function search(terme) {
      if (!terme || terme.length < 2) {
        dropdown.hidden = true;
        dropdown.innerHTML = "";
        return;
      }

      var termeMin = terme.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      var results = VILLES.filter(function (v) {
        var nomNorm = v.nom.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        return nomNorm.indexOf(termeMin) !== -1 || v.codePostal.indexOf(termeMin) !== -1;
      }).slice(0, 8);

      if (results.length === 0) {
        dropdown.hidden = true;
        dropdown.innerHTML = "";
        return;
      }

      dropdown.innerHTML = results.map(function (v, idx) {
        return '<div class="hero__suggestion-item" role="option" data-ville="' + v.id + '" data-index="' + idx + '">' +
          '<i class="ph ph-map-pin" aria-hidden="true"></i>' +
          '<span>' + esc(v.nom) + '</span>' +
          '<span class="hero__suggestion-cp">' + v.codePostal + '</span>' +
          '<span class="hero__suggestion-stats">' + (v.stats ? v.stats.candidats : 0) + ' candidats</span>' +
          '</div>';
      }).join("");

      dropdown.hidden = false;
      activeIndex = -1;

      dropdown.querySelectorAll(".hero__suggestion-item").forEach(function (item) {
        item.addEventListener("click", function () {
          navigateTo(item.dataset.ville);
        });
      });
    }

    function navigateTo(villeId) {
      window.location.href = "/municipales/2026/?ville=" + villeId;
    }

    function highlightItem(idx) {
      var items = dropdown.querySelectorAll(".hero__suggestion-item");
      items.forEach(function (it) { it.classList.remove("hero__suggestion-item--active"); });
      if (idx >= 0 && idx < items.length) {
        items[idx].classList.add("hero__suggestion-item--active");
        items[idx].scrollIntoView({ block: "nearest" });
      }
    }

    input.addEventListener("input", function () {
      clearTimeout(debounceTimer);
      var val = input.value.trim();
      debounceTimer = setTimeout(function () {
        search(val);
      }, 300);
    });

    input.addEventListener("keydown", function (e) {
      var items = dropdown.querySelectorAll(".hero__suggestion-item");
      if (e.key === "ArrowDown") {
        e.preventDefault();
        activeIndex = Math.min(activeIndex + 1, items.length - 1);
        highlightItem(activeIndex);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        activeIndex = Math.max(activeIndex - 1, 0);
        highlightItem(activeIndex);
      } else if (e.key === "Enter") {
        e.preventDefault();
        if (activeIndex >= 0 && items[activeIndex]) {
          navigateTo(items[activeIndex].dataset.ville);
        } else if (items.length > 0) {
          navigateTo(items[0].dataset.ville);
        }
      } else if (e.key === "Escape") {
        dropdown.hidden = true;
        activeIndex = -1;
      }
    });

    if (btn) {
      btn.addEventListener("click", function () {
        var items = dropdown.querySelectorAll(".hero__suggestion-item");
        if (activeIndex >= 0 && items[activeIndex]) {
          navigateTo(items[activeIndex].dataset.ville);
        } else if (items.length > 0) {
          navigateTo(items[0].dataset.ville);
        } else {
          search(input.value.trim());
          setTimeout(function () {
            var newItems = dropdown.querySelectorAll(".hero__suggestion-item");
            if (newItems.length > 0) {
              navigateTo(newItems[0].dataset.ville);
            }
          }, 350);
        }
      });
    }

    document.addEventListener("click", function (e) {
      if (!e.target.closest(".hero__search")) {
        dropdown.hidden = true;
        activeIndex = -1;
      }
    });
  }

  // === Burger Menu (full-screen overlay) ===
  function initBurger() {
    var btn = document.getElementById("burger-btn");
    var overlay = document.getElementById("mobile-menu");
    var closeBtn = document.getElementById("mobile-menu-close");
    var searchInput = document.getElementById("mobile-menu-search");
    var suggestionsEl = document.getElementById("mobile-menu-suggestions");
    if (!btn || !overlay) return;

    var debounceTimer = null;

    function openMenu() {
      overlay.hidden = false;
      document.body.style.overflow = "hidden";
      btn.setAttribute("aria-expanded", "true");
      // Update countdown in footer
      var diff = DATE_SCRUTIN.getTime() - Date.now();
      var jours = Math.max(0, Math.floor(diff / 86400000));
      var joursEl = document.getElementById("mobile-menu-jours");
      if (joursEl) joursEl.textContent = jours;
    }

    function closeMenu() {
      overlay.hidden = true;
      document.body.style.overflow = "";
      btn.setAttribute("aria-expanded", "false");
      if (searchInput) searchInput.value = "";
      if (suggestionsEl) { suggestionsEl.innerHTML = ""; suggestionsEl.hidden = true; }
    }

    btn.addEventListener("click", openMenu);
    if (closeBtn) closeBtn.addEventListener("click", closeMenu);

    // Close on nav link click
    overlay.querySelectorAll(".mobile-menu-overlay__nav a").forEach(function(a) {
      a.addEventListener("click", closeMenu);
    });

    // Close on Escape
    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape" && !overlay.hidden) closeMenu();
    });

    // Search in overlay
    if (searchInput && suggestionsEl) {
      searchInput.addEventListener("input", function() {
        clearTimeout(debounceTimer);
        var val = searchInput.value.trim();
        debounceTimer = setTimeout(function() {
          if (!val || val.length < 2) {
            suggestionsEl.innerHTML = "";
            suggestionsEl.hidden = true;
            return;
          }
          var termeMin = val.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
          var results = VILLES.filter(function(v) {
            var nomNorm = v.nom.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            return nomNorm.indexOf(termeMin) !== -1 || v.codePostal.indexOf(termeMin) !== -1;
          }).slice(0, 8);

          if (results.length === 0) {
            suggestionsEl.innerHTML = "";
            suggestionsEl.hidden = true;
            return;
          }
          suggestionsEl.innerHTML = results.map(function(v) {
            return '<div class="mobile-menu-suggestion-item" data-ville="' + v.id + '">' +
              '<i class="ph ph-map-pin"></i>' +
              '<span>' + esc(v.nom) + '</span>' +
              '<span class="mobile-menu-suggestion-cp">' + v.codePostal + '</span>' +
              '</div>';
          }).join("");
          suggestionsEl.hidden = false;

          suggestionsEl.querySelectorAll(".mobile-menu-suggestion-item").forEach(function(item) {
            item.addEventListener("click", function() {
              window.location.href = "/municipales/2026/?ville=" + item.dataset.ville;
            });
          });
        }, 200);
      });
    }
  }

  // === Apercu Radar Chart ===
  function drawApercuRadar() {
    var canvas = document.getElementById("apercu-radar");
    if (!canvas || !canvas.getContext) return;

    var dpr = window.devicePixelRatio || 1;
    var w = 320;
    var h = 260;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";

    var ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);

    var cx = w / 2;
    var cy = h / 2 + 5;
    var radius = 95;
    var labels = ["\u00c9ducation", "Environnement", "Transports", "Logement", "\u00c9conomie", "S\u00e9curit\u00e9"];
    var n = labels.length;

    // Candidat A (blue)
    var data1 = [0.7, 0.85, 0.6, 0.9, 0.5, 0.65];
    // Candidat B (yellow)
    var data2 = [0.5, 0.4, 0.75, 0.55, 0.8, 0.9];

    function angleFor(i) {
      return (Math.PI * 2 * i) / n - Math.PI / 2;
    }

    function pointAt(i, val) {
      var a = angleFor(i);
      return { x: cx + Math.cos(a) * radius * val, y: cy + Math.sin(a) * radius * val };
    }

    // Grid circles
    ctx.strokeStyle = "#e2e8f0";
    ctx.lineWidth = 0.7;
    [0.25, 0.5, 0.75, 1.0].forEach(function (s) {
      ctx.beginPath();
      for (var i = 0; i <= n; i++) {
        var p = pointAt(i % n, s);
        if (i === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      }
      ctx.closePath();
      ctx.stroke();
    });

    // Axes
    ctx.strokeStyle = "#cbd5e1";
    ctx.lineWidth = 0.5;
    for (var i = 0; i < n; i++) {
      var p = pointAt(i, 1);
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(p.x, p.y);
      ctx.stroke();
    }

    // Labels
    ctx.fillStyle = "#64748b";
    ctx.font = "500 10px 'DM Sans', sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    for (var i = 0; i < n; i++) {
      var p = pointAt(i, 1.18);
      ctx.fillText(labels[i], p.x, p.y);
    }

    // Draw dataset
    function drawDataset(data, color, alpha) {
      ctx.beginPath();
      for (var i = 0; i <= n; i++) {
        var p = pointAt(i % n, data[i % n]);
        if (i === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      }
      ctx.closePath();
      ctx.fillStyle = color.replace("1)", alpha + ")");
      ctx.fill();
      ctx.strokeStyle = color.replace(", 1)", ", 0.9)");
      ctx.lineWidth = 2;
      ctx.stroke();

      // Points
      for (var i = 0; i < n; i++) {
        var p = pointAt(i, data[i]);
        ctx.beginPath();
        ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = color.replace(", 1)", ", 1)");
        ctx.fill();
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }
    }

    drawDataset(data1, "rgba(59, 130, 246, 1)", 0.15);
    drawDataset(data2, "rgba(245, 158, 11, 1)", 0.12);
  }

  // === Mobile Search Overlay (home only) ===
  function initMobileSearchOverlay() {
    var heroInput = document.getElementById("search-input");
    var overlay = document.getElementById("mobile-search-overlay");
    var backBtn = document.getElementById("mobile-search-back");
    var overlayInput = document.getElementById("mobile-search-input");
    var resultsEl = document.getElementById("mobile-search-results");
    if (!heroInput || !overlay || !overlayInput || !resultsEl) return;

    var debounceTimer = null;

    function openOverlay() {
      if (window.innerWidth > 768) return;
      heroInput.blur();
      overlay.hidden = false;
      document.body.style.overflow = "hidden";
      overlayInput.value = heroInput.value;
      setTimeout(function() { overlayInput.focus(); }, 150);
    }

    function closeOverlay() {
      overlay.hidden = true;
      document.body.style.overflow = "";
      overlayInput.value = "";
      resultsEl.innerHTML = "";
      overlayOpen = false;
    }

    function doSearch(val) {
      if (!val || val.length < 2) {
        resultsEl.innerHTML = "";
        return;
      }
      var termeMin = val.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      var results = VILLES.filter(function(v) {
        var nomNorm = v.nom.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        return nomNorm.indexOf(termeMin) !== -1 || v.codePostal.indexOf(termeMin) !== -1;
      }).slice(0, 15);

      if (results.length === 0) {
        resultsEl.innerHTML = '<div style="padding:20px;text-align:center;color:#64748b">Aucune ville trouv\u00e9e</div>';
        return;
      }

      resultsEl.innerHTML = results.map(function(v) {
        var s = v.stats || {};
        return '<div class="mobile-search-result-item" data-ville="' + v.id + '">' +
          '<i class="ph ph-map-pin"></i>' +
          '<span>' + esc(v.nom) + '</span>' +
          '<span class="mobile-search-result-stats">' + (s.candidats || 0) + ' candidats</span>' +
          '<span class="mobile-search-result-cp">' + v.codePostal + '</span>' +
          '</div>';
      }).join("");

      resultsEl.querySelectorAll(".mobile-search-result-item").forEach(function(item) {
        item.addEventListener("click", function() {
          window.location.href = "/municipales/2026/?ville=" + item.dataset.ville;
        });
      });
    }

    var overlayOpen = false;
    function safeOpenOverlay() {
      if (overlayOpen) return;
      overlayOpen = true;
      openOverlay();
    }
    heroInput.addEventListener("focus", safeOpenOverlay);
    heroInput.addEventListener("click", safeOpenOverlay);

    if (backBtn) backBtn.addEventListener("click", closeOverlay);

    overlayInput.addEventListener("input", function() {
      clearTimeout(debounceTimer);
      var val = overlayInput.value.trim();
      debounceTimer = setTimeout(function() { doSearch(val); }, 200);
    });
  }

  // === Init ===
  function initHome() {
    updateCountdown();
    setInterval(updateCountdown, 1000);
    updateTimelineStats();
    renderElections();
    renderTendances();
    drawApercuRadar();
    initSearch();
    initMobileSearchOverlay();
    initBurger();
  }

  function init() {
    fetch(DATA_BASE_URL + 'villes.json?v=' + DATA_VERSION)
      .then(function(r) { return r.json(); })
      .then(function(data) {
        VILLES = data;
        initHome();
      })
      .catch(function(err) {
        console.error('Erreur chargement villes:', err);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
