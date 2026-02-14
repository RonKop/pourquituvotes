(function () {
  "use strict";

  var DATA_BASE_URL = "/data/";
  var DATA_VERSION = "2026021302";

  var CATEGORIE_META = {
    "securite": { icon: "ph-shield-check" },
    "transports": { icon: "ph-bus" },
    "environnement": { icon: "ph-leaf" },
    "education": { icon: "ph-graduation-cap" },
    "democratie": { icon: "ph-bank" },
    "logement": { icon: "ph-house" },
    "economie": { icon: "ph-briefcase" },
    "sante": { icon: "ph-heartbeat" },
    "solidarite": { icon: "ph-handshake" },
    "urbanisme": { icon: "ph-buildings" },
    "culture": { icon: "ph-palette" },
    "sport": { icon: "ph-soccer-ball" }
  };

  function esc(str) {
    var div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  function getThemeSlug() {
    var match = window.location.pathname.match(/\/enjeux-2026\/([a-z-]+)/);
    if (match) return match[1];
    var params = new URLSearchParams(window.location.search);
    return params.get("theme");
  }

  function updateSEO(data) {
    var title = data.nom + " \u2014 Enjeux Municipales 2026 | #POURQUITUVOTES";
    var description = data.stats.totalPropositions + " propositions sur " +
      data.nom.toLowerCase() + " dans " + data.stats.villesAvecPropositions +
      " villes. Comparez les programmes des candidats aux municipales 2026.";
    var url = "https://pourquituvotes.fr/enjeux-2026/" + data.id;

    document.title = title;
    updateMeta("description", description);
    setCanonical(url);
    updateOpenGraph(title, description, url);
    injectJsonLdBreadcrumb([
      { name: "Accueil", url: "https://pourquituvotes.fr/" },
      { name: "Enjeux 2026", url: "https://pourquituvotes.fr/enjeux-2026" },
      { name: data.nom }
    ]);
  }

  function renderHero(data) {
    var meta = CATEGORIE_META[data.id] || { icon: "ph-tag" };

    // Breadcrumb
    var breadcrumbTheme = document.getElementById("breadcrumb-theme");
    if (breadcrumbTheme) {
      var bcName = breadcrumbTheme.querySelector("[itemprop='name']");
      if (bcName) bcName.textContent = data.nom;
      else breadcrumbTheme.textContent = data.nom;
    }

    // Hero content
    var heroContent = document.getElementById("theme-hero-content");
    if (heroContent) {
      heroContent.innerHTML =
        '<div class="theme-hero__icon"><i class="ph ' + meta.icon + '" aria-hidden="true"></i></div>' +
        '<h1 class="theme-hero__title">' + esc(data.nom) + '</h1>' +
        '<div class="theme-hero__stats">' +
          '<span class="theme-hero__stat"><i class="ph ph-file-text" aria-hidden="true"></i> ' +
            data.stats.totalPropositions + ' propositions</span>' +
          '<span class="theme-hero__stat"><i class="ph ph-map-pin" aria-hidden="true"></i> ' +
            data.stats.villesAvecPropositions + ' villes</span>' +
          '<span class="theme-hero__stat"><i class="ph ph-users" aria-hidden="true"></i> ' +
            data.stats.candidatsAvecPropositions + ' candidats</span>' +
        '</div>';
    }
  }

  function renderVilles(data) {
    var container = document.getElementById("theme-villes-list");
    if (!container || !data.villes) return;

    if (data.villes.length === 0) {
      container.innerHTML = '<p style="color:#64748b">Aucune ville n\'a de propositions sur ce th\u00e8me.</p>';
      return;
    }

    var html = data.villes.map(function (v) {
      var candidatsText = v.candidats.map(function (c) { return c.nom; }).slice(0, 3).join(", ");
      if (v.candidats.length > 3) candidatsText += " +" + (v.candidats.length - 3);

      return '<a href="/municipales/2026/?ville=' + v.id + '" class="theme-ville-card">' +
        '<div class="theme-ville-card__info">' +
          '<span class="theme-ville-card__nom">' + esc(v.nom) + '</span>' +
          '<span class="theme-ville-card__count">' + v.nbPropositions + ' propositions</span>' +
          '<span class="theme-ville-card__candidats">' + esc(candidatsText) + '</span>' +
        '</div>' +
        '<i class="ph ph-arrow-right theme-ville-card__arrow" aria-hidden="true"></i>' +
        '</a>';
    }).join("");

    container.innerHTML = html;
  }

  function renderPropositions(data) {
    var container = document.getElementById("theme-props-list");
    if (!container || !data.propositions_marquantes) return;

    if (data.propositions_marquantes.length === 0) {
      document.getElementById("theme-props").hidden = true;
      return;
    }

    var html = data.propositions_marquantes.map(function (p) {
      return '<div class="theme-prop-card">' +
        '<div class="theme-prop-card__header">' +
          '<a href="/municipales/2026/candidat.html?ville=' + p.villeId + '&candidat=' + p.candidatId + '" class="theme-prop-card__candidat" style="color:#3B82F6;text-decoration:none">' + esc(p.candidat) + '</a>' +
          '<span class="theme-prop-card__ville">' + esc(p.ville) + '</span>' +
          '<span class="theme-prop-card__tag">' + esc(p.sousThemeNom) + '</span>' +
        '</div>' +
        '<div class="theme-prop-card__texte">' + esc(p.texte) + '</div>' +
        (p.source ? '<div class="theme-prop-card__source">Source : ' + esc(p.source) + '</div>' : '') +
        '</div>';
    }).join("");

    container.innerHTML = html;
  }

  function init() {
    var slug = getThemeSlug();
    if (!slug) {
      document.getElementById("theme-hero-content").innerHTML =
        '<p style="text-align:center">Th\u00e8me non sp\u00e9cifi\u00e9. <a href="/enjeux-2026" style="color:#fff;text-decoration:underline">Voir tous les enjeux</a></p>';
      return;
    }

    fetch(DATA_BASE_URL + "themes/" + slug + ".json?v=" + DATA_VERSION)
      .then(function (r) {
        if (!r.ok) throw new Error("Th\u00e8me introuvable");
        return r.json();
      })
      .then(function (data) {
        updateSEO(data);
        renderHero(data);
        renderVilles(data);
        renderPropositions(data);
      })
      .catch(function (err) {
        console.error("Erreur:", err);
        document.getElementById("theme-hero-content").innerHTML =
          '<p style="text-align:center">Th\u00e8me introuvable. <a href="/enjeux-2026" style="color:#fff;text-decoration:underline">Voir tous les enjeux</a></p>';
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
