(function () {
  "use strict";

  var DATA_VERSION = "2026021302";
  var DATA_BASE_URL = "/data/";

  var ORDRE_CATEGORIES = [
    "securite", "transports", "logement", "education", "environnement",
    "sante", "democratie", "economie", "culture", "sport", "urbanisme", "solidarite"
  ];

  var COULEURS_CATEGORIES = {
    "securite": "#3B82F6",
    "transports": "#8B5CF6",
    "logement": "#F59E0B",
    "education": "#10B981",
    "environnement": "#22C55E",
    "sante": "#EF4444",
    "democratie": "#6366F1",
    "economie": "#F97316",
    "culture": "#EC4899",
    "sport": "#14B8A6",
    "urbanisme": "#64748B",
    "solidarite": "#E11D48"
  };

  var COULEURS_PARTIS = {
    "PS": "#E4003C", "Socialiste": "#E4003C", "Gauche unie": "#E4003C",
    "LR": "#0066CC", "R\u00e9publicains": "#0066CC", "Droite": "#0066CC",
    "LFI": "#CC2443", "Insoumis": "#CC2443",
    "RN": "#0D378A", "Rassemblement National": "#0D378A",
    "EELV": "#00A86B", "\u00c9cologistes": "#00A86B",
    "Renaissance": "#7D5BA6", "LREM": "#7D5BA6", "Horizons": "#7D5BA6",
    "PCF": "#DD0000", "Communiste": "#DD0000",
    "NPA": "#B71C1C", "Lutte Ouvri\u00e8re": "#C62828",
    "Reconqu\u00eate": "#1A1A1A",
    "Modem": "#FF9900"
  };

  var ICONES_CATEGORIES = {
    "securite": "ph-shield-check",
    "transports": "ph-bus",
    "logement": "ph-house",
    "education": "ph-graduation-cap",
    "environnement": "ph-leaf",
    "sante": "ph-heartbeat",
    "democratie": "ph-bank",
    "economie": "ph-briefcase",
    "culture": "ph-palette",
    "sport": "ph-soccer-ball",
    "urbanisme": "ph-buildings",
    "solidarite": "ph-handshake"
  };

  var COULEURS_DEFAUT = [
    "#3B82F6", "#EF4444", "#10B981", "#F59E0B", "#8B5CF6",
    "#EC4899", "#14B8A6", "#F97316", "#6366F1", "#64748B"
  ];

  function getCouleurParti(candidat, idx) {
    var liste = candidat.liste || "";
    for (var key in COULEURS_PARTIS) {
      if (liste.indexOf(key) !== -1) return COULEURS_PARTIS[key];
    }
    return COULEURS_DEFAUT[idx % COULEURS_DEFAUT.length];
  }

  function echapper(str) {
    var div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // === Chargement donn\u00e9es ===
  function chargerVilles() {
    return fetch(DATA_BASE_URL + "villes.json?v=" + DATA_VERSION).then(function (r) { return r.json(); });
  }

  function chargerElection(fichier) {
    return fetch(DATA_BASE_URL + "elections/" + fichier + ".json?v=" + DATA_VERSION).then(function (r) {
      if (!r.ok) throw new Error("Erreur " + r.status);
      return r.json();
    });
  }

  // === Rendu ===
  function afficherCandidat(villes, election, candidatId) {
    var candidatIdx = -1;
    var candidat = null;
    election.candidats.forEach(function (c, i) {
      if (c.id === candidatId) { candidat = c; candidatIdx = i; }
    });

    if (!candidat) {
      document.getElementById("candidat-main").innerHTML =
        '<div style="text-align:center;padding:4rem 2rem"><h2>Candidat introuvable</h2><p><a href="/municipales/2026/?ville=' +
        echapper(election.ville.toLowerCase().replace(/\s+/g, "-")) + '">Retour au comparateur</a></p></div>';
      return;
    }

    var couleur = getCouleurParti(candidat, candidatIdx);
    var ville = election.ville;
    var villeSlug = "";
    villes.forEach(function (v) {
      if (v.nom === ville) villeSlug = v.id;
    });

    // Comptage propositions
    var totalProps = 0;
    var propsByCat = {};
    ORDRE_CATEGORIES.forEach(function (catId) { propsByCat[catId] = 0; });

    election.categories.forEach(function (cat) {
      cat.sousThemes.forEach(function (st) {
        var prop = st.propositions[candidatId];
        if (prop && prop.texte) {
          totalProps++;
          if (!propsByCat[cat.id]) propsByCat[cat.id] = 0;
          propsByCat[cat.id]++;
        }
      });
    });

    var nbCategories = 0;
    for (var k in propsByCat) { if (propsByCat[k] > 0) nbCategories++; }

    // Meta & SEO
    var seoTitle = candidat.nom + " \u2014 Programme " + ville + " 2026 | #POURQUITUVOTES";
    var seoDesc = "D\u00e9couvrez les " + totalProps + " propositions de " + candidat.nom + " (" + candidat.liste + ") pour les municipales " + ville + " 2026.";
    var seoUrl = "https://pourquituvotes.fr/municipales-2026/" + villeSlug + "/candidats/" + candidatId;
    document.title = seoTitle;
    var metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) metaDesc.setAttribute("content", seoDesc);
    if (typeof setCanonical === "function") setCanonical(seoUrl);
    if (typeof updateOpenGraph === "function") updateOpenGraph(seoTitle, seoDesc, seoUrl);
    if (typeof injectJsonLdBreadcrumb === "function") {
      injectJsonLdBreadcrumb([
        { name: "Accueil", url: "https://pourquituvotes.fr/" },
        { name: "Municipales 2026", url: "https://pourquituvotes.fr/municipales/2026/" },
        { name: ville, url: "https://pourquituvotes.fr/municipales-2026/" + villeSlug },
        { name: candidat.nom }
      ]);
    }

    // Initiales
    var parts = candidat.nom.split(" ");
    var initiales = parts.length >= 2 ? parts[0][0] + parts[parts.length - 1][0] : parts[0].substring(0, 2);

    // Hero
    var heroHTML =
      '<nav class="fil-ariane fil-ariane--hero" aria-label="Fil d\'Ariane">' +
        '<ol class="fil-ariane__liste" itemscope itemtype="https://schema.org/BreadcrumbList">' +
          '<li class="fil-ariane__item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem"><a href="/" itemprop="item"><i class="ph ph-house" aria-hidden="true"></i> <span itemprop="name">Accueil</span></a><meta itemprop="position" content="1"></li>' +
          '<li class="fil-ariane__item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem"><a href="/municipales/2026/?ville=' + echapper(villeSlug) + '" itemprop="item"><span itemprop="name">' + echapper(ville) + '</span></a><meta itemprop="position" content="2"></li>' +
          '<li class="fil-ariane__item fil-ariane__item--actif" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem"><a href="/municipales/2026/candidat.html?ville=' + echapper(villeSlug) + '&candidat=' + echapper(candidat.id) + '" itemprop="item"><span itemprop="name">' + echapper(candidat.nom) + '</span></a><meta itemprop="position" content="3"></li>' +
        '</ol>' +
      '</nav>' +
      '<div class="candidat-hero__card">' +
        '<div class="candidat-hero__avatar" style="background:' + couleur + '">' + echapper(initiales.toUpperCase()) + '</div>' +
        '<div class="candidat-hero__info">' +
          '<h1 class="candidat-hero__nom">' + echapper(candidat.nom) + '</h1>' +
          '<div class="candidat-hero__liste">' + echapper(candidat.liste) + ' &mdash; ' + echapper(ville) + '</div>' +
          '<div class="candidat-hero__tags">' +
            (candidat.programmeComplet
              ? '<span class="candidat-hero__tag candidat-hero__tag--complet"><i class="ph ph-check-circle"></i> Programme complet</span>'
              : '<span class="candidat-hero__tag candidat-hero__tag--partiel"><i class="ph ph-clock"></i> Programme \u00e0 venir</span>') +
          '</div>' +
        '</div>' +
      '</div>';
    document.getElementById("candidat-hero-content").innerHTML = heroHTML;

    // Stats
    document.getElementById("candidat-stats-content").innerHTML =
      '<div class="candidat-stats__item"><span class="candidat-stats__value">' + totalProps + '</span> propositions</div>' +
      '<div class="candidat-stats__item"><span class="candidat-stats__value">' + nbCategories + '</span> th\u00e8mes couverts</div>' +
      '<div class="candidat-stats__item"><span class="candidat-stats__value">' + election.candidats.length + '</span> candidats en lice</div>';

    // Liens
    var linksHTML = '';
    if (candidat.programmePdfPath) {
      linksHTML += '<a href="' + echapper(candidat.programmePdfPath) + '" target="_blank" rel="noopener" class="candidat-links__btn candidat-links__btn--primary"><i class="ph ph-file-pdf"></i> Programme (PDF)</a>';
    }
    if (candidat.programmeUrl && candidat.programmeUrl !== "#") {
      linksHTML += '<a href="' + echapper(candidat.programmeUrl) + '" target="_blank" rel="noopener" class="candidat-links__btn candidat-links__btn--' + (candidat.programmePdfPath ? 'secondary' : 'primary') + '"><i class="ph ph-globe"></i> Site de campagne</a>';
    }
    linksHTML += '<a href="/municipales/2026/?ville=' + echapper(villeSlug) + '&candidats=' + echapper(candidatId) + '" class="candidat-links__btn candidat-links__btn--secondary"><i class="ph ph-chart-bar"></i> Voir dans le comparateur</a>';
    document.getElementById("candidat-links").innerHTML = linksHTML;

    // Radar
    if (totalProps >= 5) {
      document.getElementById("candidat-radar-section").hidden = false;
      dessinerRadar(election, candidat, candidatIdx, propsByCat);
    }

    // Propositions par cat\u00e9gorie
    var catsHTML = '';
    var catsSorted = election.categories.slice().sort(function (a, b) {
      var idxA = ORDRE_CATEGORIES.indexOf(a.id); if (idxA === -1) idxA = 999;
      var idxB = ORDRE_CATEGORIES.indexOf(b.id); if (idxB === -1) idxB = 999;
      return idxA - idxB;
    });

    catsSorted.forEach(function (cat) {
      var props = [];
      cat.sousThemes.forEach(function (st) {
        var p = st.propositions[candidatId];
        if (p && p.texte) {
          props.push({ theme: st.nom, texte: p.texte, source: p.source, sourceUrl: p.sourceUrl });
        }
      });
      if (props.length === 0) return;

      var catColor = COULEURS_CATEGORIES[cat.id] || "#64748b";

      catsHTML += '<div class="candidat-cat candidat-cat--open" data-cat="' + cat.id + '">' +
        '<div class="candidat-cat__header">' +
          '<div class="candidat-cat__icon" style="background:' + catColor + '20;color:' + catColor + '"><i class="ph ' + (ICONES_CATEGORIES[cat.id] || 'ph-folder') + '"></i></div>' +
          '<span class="candidat-cat__nom">' + echapper(cat.nom) + '</span>' +
          '<span class="candidat-cat__count">' + props.length + '</span>' +
          '<i class="ph ph-caret-down candidat-cat__chevron"></i>' +
        '</div>' +
        '<div class="candidat-cat__body">';

      props.forEach(function (p) {
        catsHTML += '<div class="candidat-prop" style="--cat-color:' + catColor + '">' +
          '<div class="candidat-prop__theme">' + echapper(p.theme) + '</div>' +
          '<div class="candidat-prop__texte">' + echapper(p.texte) + '</div>';
        if (p.source) {
          catsHTML += '<div class="candidat-prop__source">Source : ';
          if (p.sourceUrl && p.sourceUrl !== "#") {
            catsHTML += '<a href="' + echapper(p.sourceUrl) + '" target="_blank" rel="noopener">' + echapper(p.source) + '</a>';
          } else {
            catsHTML += echapper(p.source);
          }
          catsHTML += '</div>';
        }
        catsHTML += '</div>';
      });

      catsHTML += '</div></div>';
    });

    document.getElementById("candidat-propositions").innerHTML = catsHTML;

    // Toggle cat\u00e9gories
    document.querySelectorAll(".candidat-cat__header").forEach(function (header) {
      header.addEventListener("click", function () {
        header.parentElement.classList.toggle("candidat-cat--open");
      });
    });

    // CTA
    document.getElementById("candidat-cta-link").href = "/municipales/2026/?ville=" + encodeURIComponent(villeSlug);
    document.getElementById("candidat-cta-link").innerHTML = '<i class="ph ph-arrow-left"></i> Comparer tous les candidats \u00e0 ' + echapper(ville);
  }

  // === Radar individuel ===
  function dessinerRadar(election, candidat, candidatIdx, propsByCat) {
    var canvas = document.getElementById("candidat-radar-canvas");
    if (!canvas || !canvas.getContext) return;

    var dpr = window.devicePixelRatio || 1;
    var w = 350, h = 350;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";

    var ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);

    var cx = w / 2, cy = h / 2;
    var maxR = 130;

    // Cat\u00e9gories avec propositions
    var cats = [];
    var catsSorted = election.categories.slice().sort(function (a, b) {
      var idxA = ORDRE_CATEGORIES.indexOf(a.id); if (idxA === -1) idxA = 999;
      var idxB = ORDRE_CATEGORIES.indexOf(b.id); if (idxB === -1) idxB = 999;
      return idxA - idxB;
    });
    catsSorted.forEach(function (cat) {
      var total = cat.sousThemes.length;
      var count = propsByCat[cat.id] || 0;
      cats.push({ nom: cat.nom, id: cat.id, val: total > 0 ? count / total : 0 });
    });

    var n = cats.length;
    if (n < 3) return;

    function angleFor(i) { return (Math.PI * 2 * i) / n - Math.PI / 2; }
    function pointAt(i, val) {
      var a = angleFor(i);
      return { x: cx + Math.cos(a) * maxR * val, y: cy + Math.sin(a) * maxR * val };
    }

    // Grille circulaire
    ctx.strokeStyle = "#e2e8f0";
    ctx.lineWidth = 0.7;
    [0.25, 0.5, 0.75, 1.0].forEach(function (s) {
      ctx.beginPath();
      ctx.arc(cx, cy, maxR * s, 0, Math.PI * 2);
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
    ctx.fillStyle = "#475569";
    ctx.font = "500 10px 'DM Sans', sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    for (var i = 0; i < n; i++) {
      var p = pointAt(i, 1.18);
      // Raccourcir les noms longs
      var label = cats[i].nom;
      if (label.length > 14) label = label.substring(0, 12) + "\u2026";
      ctx.fillText(label, p.x, p.y);
    }

    // Dataset
    var couleur = getCouleurParti(candidat, candidatIdx);
    ctx.beginPath();
    for (var i = 0; i <= n; i++) {
      var p = pointAt(i % n, cats[i % n].val);
      if (i === 0) ctx.moveTo(p.x, p.y);
      else ctx.lineTo(p.x, p.y);
    }
    ctx.closePath();
    ctx.fillStyle = couleur + "30";
    ctx.fill();
    ctx.strokeStyle = couleur;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Points
    for (var i = 0; i < n; i++) {
      var p = pointAt(i, cats[i].val);
      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
      ctx.fillStyle = couleur;
      ctx.fill();
      ctx.strokeStyle = "#fff";
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }

  // === Init ===
  function init() {
    var params = new URLSearchParams(window.location.search);
    var villeParam = params.get("ville");
    var candidatParam = params.get("candidat");

    if (!villeParam || !candidatParam) {
      var pathMatch = window.location.pathname.match(/\/municipales-2026\/([^\/]+)\/candidats\/([^\/]+)/);
      if (pathMatch) {
        villeParam = decodeURIComponent(pathMatch[1]);
        candidatParam = decodeURIComponent(pathMatch[2]);
      }
    }

    if (!villeParam || !candidatParam) {
      document.getElementById("candidat-main").innerHTML =
        '<div style="text-align:center;padding:4rem 2rem"><h2>Param\u00e8tres manquants</h2><p><a href="/municipales/2026/">Retour au comparateur</a></p></div>';
      return;
    }

    Promise.all([chargerVilles(), chargerElection(villeParam + "-2026")])
      .then(function (results) {
        var villes = results[0];
        var election = results[1];
        afficherCandidat(villes, election, candidatParam);
      })
      .catch(function (err) {
        console.error("Erreur:", err);
        document.getElementById("candidat-main").innerHTML =
          '<div style="text-align:center;padding:4rem 2rem"><h2>Erreur de chargement</h2><p>Ville ou candidat introuvable.</p><p><a href="/municipales/2026/">Retour au comparateur</a></p></div>';
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
