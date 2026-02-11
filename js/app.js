(function () {
  "use strict";


  // === Chargement des données (JSON externe) ===
  var VILLES = [];
  var ELECTIONS = {};
  var ELECTIONS_CACHE = {};
  var DATA_BASE_URL = '/data/';
  var DATA_VERSION = '2026021002';

  function chargerVilles() {
    var prefetch = window.__prefetch && window.__prefetch.villes;
    var promise = prefetch || fetch(DATA_BASE_URL + 'villes.json?v=' + DATA_VERSION)
      .then(function(r) {
        if (!r.ok) throw new Error('Erreur chargement villes: ' + r.status);
        return r.json();
      });
    return promise.then(function(data) { VILLES = data; return data; });
  }

  function chargerDonneesElection(id) {
    if (ELECTIONS_CACHE[id]) return Promise.resolve(ELECTIONS_CACHE[id]);
    var prefetch = window.__prefetch && window.__prefetch.election;
    if (prefetch) {
      window.__prefetch.election = null; // Utiliser une seule fois
      return prefetch.then(function(data) {
        if (data) { ELECTIONS_CACHE[id] = data; ELECTIONS[id] = data; }
        return data || fetch(DATA_BASE_URL + 'elections/' + id + '.json?v=' + DATA_VERSION)
          .then(function(r) { if (!r.ok) throw new Error('Erreur chargement election: ' + r.status); return r.json(); })
          .then(function(d) { ELECTIONS_CACHE[id] = d; ELECTIONS[id] = d; return d; });
      });
    }
    return fetch(DATA_BASE_URL + 'elections/' + id + '.json?v=' + DATA_VERSION)
      .then(function(r) {
        if (!r.ok) throw new Error('Erreur chargement election: ' + r.status);
        return r.json();
      })
      .then(function(data) {
        ELECTIONS_CACHE[id] = data;
        ELECTIONS[id] = data;
        return data;
      });
  }

  function afficherChargement(visible) {
    var overlay = document.getElementById('loader-overlay');
    if (overlay) overlay.hidden = !visible;
  }

  // === Éléments DOM ===
  var villeSearchInput = document.getElementById("ville-search");
  var villeSuggestionsContainer = document.getElementById("ville-suggestions");
  var rechercheInput = document.getElementById("recherche-input");
  var electionInfo = document.getElementById("election-info");
  var electionTitre = document.getElementById("election-titre");
  var electionStats = document.getElementById("election-stats");
  var statistiquesSection = document.getElementById("statistiques");
  var repartitionSection = document.getElementById("repartition");
  var repartitionContenu = document.getElementById("repartition-contenu");
  var filtresContainer = document.getElementById("filtres-categories");
  var comparaisonContainer = document.getElementById("comparaison");
  var etatVide = document.getElementById("etat-vide");
  var countdownElement = document.getElementById("topbar-countdown");
  var countdownJours = document.getElementById("countdown-jours");
  var countdownHeures = document.getElementById("countdown-heures");
  var countdownMinutes = document.getElementById("countdown-minutes");
  var countdownSecondes = document.getElementById("countdown-secondes");
  var repartitionToggleContainer = document.getElementById("repartition-toggle");
  var radarChartComparerGlobal = null;
  var btnPartager = document.getElementById("btn-partager");
  var partageReseaux = document.getElementById("partage-reseaux");
  var selectionCandidatsSection = document.getElementById("selection-candidats");
  var candidatsCheckboxesContainer = document.getElementById("candidats-checkboxes");
  var btnTop = document.getElementById("btn-top");
  var progressPills = document.getElementById("progress-pills");
  var progressPillsList = document.getElementById("progress-pills-list");
  var progressPillsCounter = document.getElementById("progress-pills-counter");
  var themeToggle = document.getElementById("dp-theme-toggle");
  var fontSelect = null; // Moved to design panel
  var alertesSection = document.getElementById("alertes-section");
  var aucunCandidatSection = document.getElementById("aucun-candidat");
  var filAriane = document.getElementById("fil-ariane");
  var alerteEmailInput = document.getElementById("alerte-email");
  var btnAlerte = document.getElementById("btn-alerte");
  var alerteMessage = document.getElementById("alerte-message");

  // === Hero dynamique ===
  var heroSection = document.getElementById("hero");
  var heroBadgeVille = document.getElementById("hero-badge-ville");
  var heroStats = document.getElementById("hero-stats");
  var heroStatCandidats = document.getElementById("hero-stat-candidats");
  var heroStatThemes = document.getElementById("hero-stat-themes");
  var heroStatProps = document.getElementById("hero-stat-props");
  // heroStatJours, heroChampCandidat, heroChampRecherche — supprimés du HTML (Phase 5)

  // === Ordre consensuel des catégories ===
  var ORDRE_CATEGORIES = [
    "education",        // Éducation & Jeunesse
    "environnement",    // Environnement & Transition écologique
    "transports",       // Transports & Mobilité
    "sante",            // Santé & Accès aux soins
    "logement",         // Logement
    "economie",         // Économie & Emploi
    "solidarite",       // Solidarité & Égalité
    "urbanisme",        // Urbanisme & Cadre de vie
    "culture",          // Culture & Patrimoine
    "sport",            // Sport & Loisirs
    "democratie",       // Démocratie & Vie citoyenne
    "securite"          // Sécurité & Prévention
  ];

  // === État ===
  var donneesElection = null;
  var categorieActive = "toutes";
  var rechercheTexte = "";
  var countdownInterval = null;
  var suggestionActive = -1;
  var villeSelectionnee = null;
  var candidatsSelectionnes = [];
  var chartsInstances = {};

  // === Recherche de ville ===
  function rechercherVilles(terme) {
    if (!terme || terme.length < 1) {
      return VILLES;
    }

    var termeMin = terme.toLowerCase().trim();
    return VILLES.filter(function (ville) {
      var nomMatch = ville.nom.toLowerCase().indexOf(termeMin) !== -1;
      var codeMatch = ville.codePostal.indexOf(termeMin) !== -1;
      return nomMatch || codeMatch;
    });
  }

  function surligner(texte, terme) {
    if (!terme) return texte;
    var regex = new RegExp("(" + termeRegexSafe(terme) + ")", "gi");
    return texte.replace(regex, '<span class="ville-suggestion__highlight">$1</span>');
  }

  function afficherSuggestions(villes, terme) {
    villeSuggestionsContainer.innerHTML = "";
    suggestionActive = -1;

    if (villes.length === 0) {
      var empty = document.createElement("div");
      empty.className = "ville-suggestions-empty";
      empty.textContent = "Aucune ville trouvée";
      villeSuggestionsContainer.appendChild(empty);
      villeSuggestionsContainer.hidden = false;
      return;
    }

    villes.forEach(function (ville, index) {
      var div = document.createElement("div");
      div.className = "ville-suggestion";
      div.dataset.index = index;
      div.dataset.electionId = ville.elections[0];

      var nomHTML = surligner(echapper(ville.nom), terme);
      var codeHTML = surligner(echapper(ville.codePostal), terme);

      div.innerHTML =
        '<span class="ville-suggestion__nom">' + nomHTML + '</span>' +
        '<span class="ville-suggestion__code">' + codeHTML + '</span>';

      div.addEventListener("click", function () {
        selectionnerVille(ville);
      });

      villeSuggestionsContainer.appendChild(div);
    });

    villeSuggestionsContainer.hidden = false;
  }

  function masquerSuggestions() {
    villeSuggestionsContainer.hidden = true;
    suggestionActive = -1;
  }

  function selectionnerVille(ville) {
    villeSelectionnee = ville;
    villeSearchInput.value = ville.nom + " (" + ville.codePostal + ")";
    masquerSuggestions();
    chargerElection(ville.elections[0]);
  }

  function naviguerSuggestions(direction) {
    var suggestions = villeSuggestionsContainer.querySelectorAll(".ville-suggestion");
    if (suggestions.length === 0) return;

    if (suggestionActive !== -1) {
      suggestions[suggestionActive].classList.remove("ville-suggestion--active");
    }

    suggestionActive += direction;

    if (suggestionActive < 0) {
      suggestionActive = suggestions.length - 1;
    } else if (suggestionActive >= suggestions.length) {
      suggestionActive = 0;
    }

    suggestions[suggestionActive].classList.add("ville-suggestion--active");
    suggestions[suggestionActive].scrollIntoView({ block: "nearest" });
  }

  function validerSuggestion() {
    if (suggestionActive === -1) return;
    var suggestions = villeSuggestionsContainer.querySelectorAll(".ville-suggestion");
    if (suggestions[suggestionActive]) {
      var electionId = suggestions[suggestionActive].dataset.electionId;
      var ville = VILLES.find(function (v) { return v.elections[0] === electionId; });
      if (ville) {
        selectionnerVille(ville);
      }
    }
  }

  // === Recherche de candidat ===
  var candidatSearchInput = document.getElementById("candidat-search");
  var candidatSuggestionsContainer = document.getElementById("candidat-suggestions");
  var suggestionCandidatActive = -1;

  function rechercherCandidats(terme) {
    if (!terme || terme.length < 2) return [];
    var termeMin = terme.toLowerCase().trim();
    var resultats = [];
    VILLES.forEach(function (ville) {
      var electionId = ville.elections[0];
      var candidats = ville.candidats || [];
      candidats.forEach(function (candidat) {
        if (candidat.nom.toLowerCase().indexOf(termeMin) !== -1) {
          resultats.push({
            candidatId: candidat.id,
            candidatNom: candidat.nom,
            liste: candidat.liste,
            villeId: ville.id,
            villeNom: ville.nom,
            electionId: electionId
          });
        }
      });
    });
    return resultats;
  }

  function afficherSuggestionsCandidats(resultats, terme) {
    candidatSuggestionsContainer.innerHTML = "";
    suggestionCandidatActive = -1;

    if (resultats.length === 0) {
      var empty = document.createElement("div");
      empty.className = "ville-suggestions-empty";
      empty.textContent = "Aucun candidat trouv\u00e9";
      candidatSuggestionsContainer.appendChild(empty);
      candidatSuggestionsContainer.hidden = false;
      return;
    }

    resultats.forEach(function (r, index) {
      var div = document.createElement("div");
      div.className = "candidat-suggestion";
      div.dataset.index = index;

      var nomHTML = surligner(echapper(r.candidatNom), terme);

      div.innerHTML =
        '<span class="candidat-suggestion__nom">' + nomHTML + '</span>' +
        '<span class="candidat-suggestion__ville">\u2014 ' + echapper(r.villeNom) + '</span>' +
        '<span class="candidat-suggestion__liste">(' + echapper(r.liste) + ')</span>';

      div.addEventListener("click", function () {
        selectionnerCandidatRecherche(r);
      });

      candidatSuggestionsContainer.appendChild(div);
    });

    candidatSuggestionsContainer.hidden = false;
  }

  function selectionnerCandidatRecherche(resultat) {
    // Sélectionner la ville correspondante
    var ville = VILLES.find(function (v) { return v.id === resultat.villeId; });
    if (!ville) return;

    candidatSearchInput.value = resultat.candidatNom;
    candidatSuggestionsContainer.hidden = true;
    suggestionCandidatActive = -1;

    villeSelectionnee = ville;
    villeSearchInput.value = ville.nom + " (" + ville.codePostal + ")";

    // Pré-sélectionner le candidat AVANT le chargement async
    candidatsSelectionnes = [resultat.candidatId];

    // Charger l'élection (async) — afficherElection sera appelé dans chargerElection
    chargerElection(resultat.electionId);
  }

  function masquerSuggestionsCandidats() {
    candidatSuggestionsContainer.hidden = true;
    suggestionCandidatActive = -1;
  }

  function naviguerSuggestionsCandidats(direction) {
    var suggestions = candidatSuggestionsContainer.querySelectorAll(".candidat-suggestion");
    if (suggestions.length === 0) return;

    if (suggestionCandidatActive !== -1) {
      suggestions[suggestionCandidatActive].classList.remove("candidat-suggestion--active");
    }

    suggestionCandidatActive += direction;

    if (suggestionCandidatActive < 0) {
      suggestionCandidatActive = suggestions.length - 1;
    } else if (suggestionCandidatActive >= suggestions.length) {
      suggestionCandidatActive = 0;
    }

    suggestions[suggestionCandidatActive].classList.add("candidat-suggestion--active");
    suggestions[suggestionCandidatActive].scrollIntoView({ block: "nearest" });
  }

  // === Compte à rebours ===
  function demarrerCountdown(dateVote) {
    if (countdownInterval) {
      clearInterval(countdownInterval);
    }

    var dateVoteParsed = new Date(dateVote);

    function mettreAJourCountdown() {
      var maintenant = new Date().getTime();
      var tempsRestant = dateVoteParsed.getTime() - maintenant;

      if (tempsRestant < 0) {
        countdownElement.hidden = true;
        var mobileTopbarElapsed = document.getElementById("countdown-topbar-mobile");
        if (mobileTopbarElapsed) mobileTopbarElapsed.hidden = true;
        if (countdownInterval) clearInterval(countdownInterval);
        return;
      }

      var jours = Math.floor(tempsRestant / (1000 * 60 * 60 * 24));
      var heures = Math.floor((tempsRestant % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((tempsRestant % (1000 * 60 * 60)) / (1000 * 60));
      var secondes = Math.floor((tempsRestant % (1000 * 60)) / 1000);

      countdownJours.textContent = jours;
      countdownHeures.textContent = heures;
      countdownMinutes.textContent = minutes;
      countdownSecondes.textContent = secondes;

      // hero-stat-jours supprimé du HTML (Phase 5)

      countdownElement.hidden = false;

      // Sync mobile topbar countdown
      var mobileTopbar = document.getElementById("countdown-topbar-mobile");
      var mobileTimer = document.getElementById("countdown-mobile-timer");
      if (mobileTimer) {
        mobileTimer.textContent = jours + "j " + heures + "h " + minutes + "min " + secondes + "s";
      }
      if (mobileTopbar) {
        mobileTopbar.hidden = false;
      }
    }

    mettreAJourCountdown();
    countdownInterval = setInterval(mettreAJourCountdown, 1000);
  }

  function arreterCountdown() {
    if (countdownInterval) {
      clearInterval(countdownInterval);
      countdownInterval = null;
    }
    countdownElement.hidden = true;
    var mobileTopbar = document.getElementById("countdown-topbar-mobile");
    if (mobileTopbar) mobileTopbar.hidden = true;
  }

  // === Chargement d'une élection ===
  function chargerElection(fichier) {
    afficherChargement(true);
    chargerDonneesElection(fichier).then(function(data) {
      donneesElection = data;
      if (!donneesElection) {
        afficherChargement(false);
        return;
      }

      // Trier les catégories selon l'ordre consensuel
      donneesElection.categories.sort(function(a, b) {
        var idxA = ORDRE_CATEGORIES.indexOf(a.id);
        var idxB = ORDRE_CATEGORIES.indexOf(b.id);
        if (idxA === -1) idxA = 999;
        if (idxB === -1) idxB = 999;
        return idxA - idxB;
      });

      rechercheInput.disabled = false;
      rechercheInput.value = "";
      rechercheTexte = "";
      categorieActive = "toutes";
      treemapModeDuel = false;
      treemapCandidatPrincipal = null;
      treemapCandidatAdversaire = null;

      if (donneesElection.dateVote) {
        demarrerCountdown(donneesElection.dateVote);
      } else {
        arreterCountdown();
      }

      mettreAJourMetadonnees();
      mettreAJourFilAriane(donneesElection.ville);
      afficherElection();
      afficherChargement(false);

      // Scroll vers la catégorie si un hash est présent dans l'URL (ex: #securite)
      var hashCat = window.location.hash ? window.location.hash.substring(1) : "";
      if (hashCat) {
        setTimeout(function() { scrollVersCategorie(hashCat); }, 300);
      }
    }).catch(function(err) {
      console.error('Erreur chargement:', err);
      afficherChargement(false);
    });
  }

  // === Helper pour compter les propositions ===
  function compterPropositionsCategorie(categorie) {
    // Ancien format : propositions directes
    if (categorie.propositions) {
      return categorie.propositions.length;
    }
    // Nouveau format : sous-thèmes
    if (categorie.sousThemes) {
      var total = 0;
      categorie.sousThemes.forEach(function(st) {
        Object.keys(st.propositions).forEach(function(candidatId) {
          if (st.propositions[candidatId] && st.propositions[candidatId].texte) {
            total++;
          }
        });
      });
      return total;
    }
    return 0;
  }

  function compterPropositionsCandidat(categorie, candidatId) {
    // Ancien format : propositions directes
    if (categorie.propositions) {
      return categorie.propositions.filter(function (p) {
        return p.candidatId === candidatId;
      }).length;
    }
    // Nouveau format : sous-thèmes
    if (categorie.sousThemes) {
      var count = 0;
      categorie.sousThemes.forEach(function(st) {
        if (st.propositions[candidatId] && st.propositions[candidatId].texte) {
          count++;
        }
      });
      return count;
    }
    return 0;
  }

  function calculerCouverture(categorie, candidatId) {
    if (!categorie.sousThemes || categorie.sousThemes.length === 0) {
      return { couverts: 0, total: 0, pct: 0 };
    }
    var total = categorie.sousThemes.length;
    var couverts = 0;
    categorie.sousThemes.forEach(function(st) {
      if (st.propositions[candidatId] && st.propositions[candidatId].texte) {
        couverts++;
      }
    });
    return { couverts: couverts, total: total, pct: Math.round(couverts / total * 100) };
  }

  // === Métadonnées dynamiques (SEO) ===
  function mettreAJourMetadonnees() {
    if (!donneesElection) return;

    var ville = donneesElection.ville;
    var annee = donneesElection.annee;
    var nbCandidats = donneesElection.candidats.length;
    var nbPropositions = 0;
    donneesElection.categories.forEach(function (cat) {
      nbPropositions += compterPropositionsCategorie(cat);
    });

    // Titre de la page
    var titre = ville + " " + annee + " — Pour qui tu votes";
    document.title = titre;

    // Description
    var description = "Comparez les programmes de " + nbCandidats + " candidats aux élections municipales de " + ville + " " + annee + ". " + nbPropositions + " propositions détaillées et sourcées.";

    // URL canonique
    var urlBase = window.location.origin + window.location.pathname;
    var urlCanonique = urlBase + "?ville=" + (villeSelectionnee ? villeSelectionnee.id : ville.toLowerCase().replace(/\s+/g, '-'));

    // Mettre à jour les balises meta
    mettreAJourMeta("description", description);
    mettreAJourMeta("og:title", titre);
    mettreAJourMeta("og:description", description);
    mettreAJourMeta("og:url", urlCanonique);
    mettreAJourMeta("twitter:title", titre);
    mettreAJourMeta("twitter:description", description);

    // Mettre à jour le canonical
    var linkCanonical = document.querySelector('link[rel="canonical"]');
    if (linkCanonical) {
      linkCanonical.href = urlCanonique;
    }

    // Meta last-modified (fraîcheur SEO)
    if (villeSelectionnee && villeSelectionnee.derniereMaj) {
      var metaLastMod = document.querySelector('meta[name="last-modified"]');
      if (!metaLastMod) {
        metaLastMod = document.createElement("meta");
        metaLastMod.name = "last-modified";
        document.head.appendChild(metaLastMod);
      }
      metaLastMod.content = villeSelectionnee.derniereMaj;
    }

    // Mettre à jour les données structurées
    mettreAJourDonneesStructurees(ville, annee, nbCandidats, nbPropositions);
  }

  function mettreAJourMeta(propriete, contenu) {
    var selector = propriete.indexOf(':') > -1
      ? 'meta[property="' + propriete + '"]'
      : 'meta[name="' + propriete + '"]';

    var meta = document.querySelector(selector);
    if (meta) {
      meta.content = contenu;
    }
  }

  function mettreAJourDonneesStructurees(ville, annee, nbCandidats, nbPropositions) {
    var scriptExistant = document.querySelector('script[type="application/ld+json"]');
    if (!scriptExistant) return;

    // Générer les fiches Person pour chaque candidat
    var candidatsPersons = [];
    if (donneesElection && donneesElection.candidats) {
      donneesElection.candidats.forEach(function (candidat) {
        var person = {
          "@type": "Person",
          "name": candidat.nom
        };
        if (candidat.liste) {
          person.affiliation = {
            "@type": "Organization",
            "name": candidat.liste
          };
        }
        candidatsPersons.push(person);
      });
    }

    // Liste des noms pour og:description
    var nomsCandidats = donneesElection.candidats.map(function (c) { return c.nom; }).join(", ");
    var descriptionDetaillee = "Comparez les programmes de " + nbCandidats + " candidats aux \u00e9lections municipales de " + ville + " " + annee + " : " + nomsCandidats + ". " + nbPropositions + " propositions d\u00e9taill\u00e9es et sourc\u00e9es.";
    mettreAJourMeta("og:description", descriptionDetaillee);

    var donnees = {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "Pour qui tu votes \u2014 " + ville + " " + annee,
      "description": "Comparaison des programmes de " + nbCandidats + " candidats aux \u00e9lections municipales de " + ville + " " + annee,
      "url": window.location.href,
      "applicationCategory": "GovernmentApplication",
      "operatingSystem": "Any",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "EUR"
      },
      "creator": {
        "@type": "Organization",
        "name": "Pour qui tu votes"
      },
      "inLanguage": "fr-FR",
      "audience": {
        "@type": "Audience",
        "audienceType": "Citizens, Voters"
      },
      "about": {
        "@type": "Event",
        "name": "\u00c9lections municipales " + ville + " " + annee,
        "location": {
          "@type": "Place",
          "name": ville,
          "address": {
            "@type": "PostalAddress",
            "addressLocality": ville,
            "addressCountry": "FR"
          }
        },
        "performer": candidatsPersons
      }
    };

    scriptExistant.textContent = JSON.stringify(donnees, null, 2);

    // Générer le FAQPage Schema.org
    genererSchemaFAQ();
  }

  function mettreAJourFilAriane(ville) {
    if (!filAriane) return;
    if (!ville) {
      filAriane.hidden = true;
      return;
    }
    var villeId = villeSelectionnee ? villeSelectionnee.id : ville.toLowerCase().replace(/\s+/g, '-');
    var urlVille = '/municipales/2026/?ville=' + villeId;

    filAriane.innerHTML = '<ol class="fil-ariane__liste" itemscope itemtype="https://schema.org/BreadcrumbList">' +
      '<li class="fil-ariane__item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">' +
        '<a href="/" itemprop="item"><i class="ph ph-house" aria-hidden="true"></i> <span itemprop="name">Accueil</span></a>' +
        '<meta itemprop="position" content="1">' +
      '</li>' +
      '<li class="fil-ariane__item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">' +
        '<a href="/municipales/2026/" itemprop="item"><span itemprop="name">Municipales 2026</span></a>' +
        '<meta itemprop="position" content="2">' +
      '</li>' +
      '<li class="fil-ariane__item fil-ariane__item--actif" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">' +
        '<a href="' + urlVille + '" itemprop="item"><span itemprop="name">' + echapper(ville) + '</span></a>' +
        '<meta itemprop="position" content="3">' +
      '</li>' +
    '</ol>';
    filAriane.hidden = false;
  }

  // === Hero dynamique ===
  function mettreAJourHeroStats() {
    if (!donneesElection || !heroStats) return;
    var nbCandidats = donneesElection.candidats.length;
    var nbThemes = donneesElection.categories.length;
    var totalProps = 0;
    donneesElection.categories.forEach(function(cat) {
      totalProps += compterPropositionsCategorie(cat);
    });
    if (heroStatCandidats) heroStatCandidats.textContent = nbCandidats;
    if (heroStatThemes) heroStatThemes.textContent = nbThemes;
    if (heroStatProps) heroStatProps.textContent = totalProps;
    heroStats.hidden = false;

    // Sous-titre statique, ne pas écraser
  }

  function mettreAJourHeroEtat(ville) {
    if (!heroSection) return;
    var quizCta = document.getElementById("hero-quiz-cta");
    if (ville) {
      heroSection.classList.add("hero--ville");
      if (heroBadgeVille) {
        heroBadgeVille.textContent = ville;
        heroBadgeVille.hidden = false;
      }
      // heroChampCandidat/Recherche supprimés (Phase 5 — search-float unifié)
      mettreAJourHeroStats();
      // Quiz CTA : afficher et mettre à jour les liens
      if (quizCta && villeSelectionnee) {
        var villeId = villeSelectionnee.id;
        var expressLink = document.getElementById("hero-quiz-express");
        var expertLink = document.getElementById("hero-quiz-expert");
        if (expressLink) expressLink.href = "simulateur.html?ville=" + encodeURIComponent(villeId);
        if (expertLink) expertLink.href = "simulateur.html?ville=" + encodeURIComponent(villeId) + "&mode=expert";
        quizCta.hidden = false;
      }
    } else {
      heroSection.classList.remove("hero--ville");
      if (heroBadgeVille) heroBadgeVille.hidden = true;
      if (heroStats) heroStats.hidden = true;
      if (quizCta) quizCta.hidden = true;
      // heroChampCandidat/Recherche supprimés (Phase 5 — search-float unifié)
    }
  }

  function genererSchemaFAQ() {
    if (!donneesElection || !donneesElection.candidats || donneesElection.candidats.length === 0) return;

    // Supprimer l'ancien FAQ schema s'il existe
    var ancien = document.getElementById("schema-faq");
    if (ancien) ancien.remove();

    var faqEntries = [];

    donneesElection.candidats.forEach(function (candidat) {
      // Collecter les propositions par catégorie pour ce candidat
      donneesElection.categories.forEach(function (cat) {
        if (!cat.sousThemes) return;
        var textes = [];
        cat.sousThemes.forEach(function (st) {
          var prop = st.propositions[candidat.id];
          if (prop && prop.texte) {
            textes.push(prop.texte);
          }
        });
        if (textes.length === 0) return;

        faqEntries.push({
          "@type": "Question",
          "name": "Que propose " + candidat.nom + " sur le thème « " + cat.nom + " » à " + donneesElection.ville + " ?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": textes.join(" | ")
          }
        });
      });
    });

    if (faqEntries.length === 0) return;

    var faqSchema = {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": faqEntries
    };

    var script = document.createElement("script");
    script.type = "application/ld+json";
    script.id = "schema-faq";
    script.textContent = JSON.stringify(faqSchema);
    document.head.appendChild(script);
  }

  // === Filtres candidats inline ===
  var filtresListe = document.getElementById("filtres-candidats-liste");
  var filtreBtnTous = document.getElementById("filtre-btn-tous");
  var filtreBtnAucun = document.getElementById("filtre-btn-aucun");
  var filtresInitialise = false;

  function afficherSelectionCandidats(candidats) {
    if (!filtresListe) return;
    filtresListe.innerHTML = "";

    if (candidatsSelectionnes.length === 0) {
      candidatsSelectionnes = candidats.map(function (c) { return c.id; });
    }

    candidats.forEach(function (candidat, idx) {
      var estActif = candidatsSelectionnes.indexOf(candidat.id) !== -1;
      var couleur = getCouleurParti(candidat, idx);

      var chip = document.createElement("span");
      chip.className = "filtres-candidats__chip" + (estActif ? " filtres-candidats__chip--active" : "");
      chip.style.setProperty("--chip-couleur", couleur);
      if (estActif) {
        var r = parseInt(couleur.slice(1, 3), 16) || 44;
        var g = parseInt(couleur.slice(3, 5), 16) || 62;
        var b = parseInt(couleur.slice(5, 7), 16) || 107;
        chip.style.setProperty("--chip-bg", "rgba(" + r + "," + g + "," + b + ",0.08)");
      }
      chip.dataset.candidatId = candidat.id;

      var cb = document.createElement("span");
      cb.className = "filtres-candidats__chip-cb";
      cb.textContent = "\u2713";

      chip.appendChild(cb);
      chip.appendChild(document.createTextNode(echapper(candidat.nom)));

      chip.addEventListener("click", function () {
        toggleCandidatSelection(candidat.id);
      });

      filtresListe.appendChild(chip);
    });

    selectionCandidatsSection.hidden = false;

    // Init boutons Tous / Aucun (une seule fois)
    if (!filtresInitialise) {
      filtreBtnTous.addEventListener("click", function () {
        candidatsSelectionnes = donneesElection.candidats.map(function (c) { return c.id; });
        var cands = donneesElection.candidats.slice().sort(function (a, b) { return a.nom.localeCompare(b.nom, "fr"); });
        afficherSelectionCandidats(cands);
        afficherRepartition(cands);
        afficherGrille(cands);
        genererStatistiques(cands);
        mettreAJourURL();
      });
      filtreBtnAucun.addEventListener("click", function () {
        if (donneesElection.candidats.length > 0) {
          candidatsSelectionnes = [donneesElection.candidats[0].id];
          var cands = donneesElection.candidats.slice().sort(function (a, b) { return a.nom.localeCompare(b.nom, "fr"); });
          afficherSelectionCandidats(cands);
          afficherRepartition(cands);
          afficherGrille(cands);
          genererStatistiques(cands);
          mettreAJourURL();
          afficherToast("Au moins un candidat doit rester s\u00E9lectionn\u00E9");
        }
      });
      filtresInitialise = true;
    }

    // === Bottom sheet mobile ===
    mettreAJourMobileFiltre(candidats);
  }

  var mobileFilterBtn = document.getElementById("mobile-filtre-btn");
  var mobileFilterOverlay = document.getElementById("mobile-filtre-overlay");
  var mobileFilterSheet = document.getElementById("mobile-filtre-sheet");
  var mobileFilterListe = document.getElementById("mobile-filtre-liste");
  var mobileFilterBadge = document.getElementById("mobile-filtre-badge");
  var mobileFilterAppliquer = document.getElementById("mobile-filtre-appliquer");
  var mobileFilterClose = document.getElementById("mobile-filtre-close");
  var mobileSelectionsTemp = [];

  function mettreAJourMobileFiltre(candidats) {
    if (!mobileFilterBtn || !donneesElection) return;
    mobileFilterBtn.hidden = false;
    mobileFilterBadge.textContent = candidatsSelectionnes.length;
  }

  function ouvrirMobileFiltre() {
    if (!mobileFilterListe || !donneesElection) return;
    mobileFilterListe.innerHTML = "";
    mobileSelectionsTemp = candidatsSelectionnes.slice();

    var candidats = donneesElection.candidats.slice().sort(function(a, b) {
      return a.nom.localeCompare(b.nom, "fr");
    });

    candidats.forEach(function(candidat, idx) {
      var couleur = getCouleurParti(candidat, idx);
      var estActif = mobileSelectionsTemp.indexOf(candidat.id) !== -1;

      var r = parseInt(couleur.slice(1, 3), 16) || 44;
      var g = parseInt(couleur.slice(3, 5), 16) || 62;
      var b = parseInt(couleur.slice(5, 7), 16) || 107;

      var item = document.createElement("div");
      item.className = "mobile-filtre-item" + (estActif ? " mobile-filtre-item--active" : "");
      item.style.setProperty("--item-couleur", couleur);
      item.style.setProperty("--item-bg", "rgba(" + r + "," + g + "," + b + ",0.08)");
      item.dataset.candidatId = candidat.id;

      var cb = document.createElement("div");
      cb.className = "mobile-filtre-item__cb";
      cb.textContent = "\u2713";

      var infos = document.createElement("div");
      infos.innerHTML = '<div class="mobile-filtre-item__nom">' + echapper(candidat.nom) + '</div>' +
        '<div class="mobile-filtre-item__parti">' + echapper(candidat.liste) + '</div>';

      item.appendChild(cb);
      item.appendChild(infos);

      item.addEventListener("click", function() {
        var pos = mobileSelectionsTemp.indexOf(candidat.id);
        if (pos === -1) {
          mobileSelectionsTemp.push(candidat.id);
          item.classList.add("mobile-filtre-item--active");
        } else {
          if (mobileSelectionsTemp.length > 1) {
            mobileSelectionsTemp.splice(pos, 1);
            item.classList.remove("mobile-filtre-item--active");
          }
        }
      });

      mobileFilterListe.appendChild(item);
    });

    mobileFilterOverlay.hidden = false;
    mobileFilterSheet.hidden = false;
  }

  function fermerMobileFiltre() {
    mobileFilterOverlay.hidden = true;
    mobileFilterSheet.hidden = true;
  }

  function appliquerMobileFiltre() {
    candidatsSelectionnes = mobileSelectionsTemp.slice();
    var cands = donneesElection.candidats.slice().sort(function(a, b) {
      return a.nom.localeCompare(b.nom, "fr");
    });
    afficherSelectionCandidats(cands);
    afficherRepartition(cands);
    afficherGrille(cands);
    genererStatistiques(cands);
    mettreAJourURL();
    fermerMobileFiltre();
  }

  if (mobileFilterBtn) {
    mobileFilterBtn.addEventListener("click", ouvrirMobileFiltre);
  }
  if (mobileFilterOverlay) {
    mobileFilterOverlay.addEventListener("click", fermerMobileFiltre);
  }
  if (mobileFilterClose) {
    mobileFilterClose.addEventListener("click", fermerMobileFiltre);
  }
  if (mobileFilterAppliquer) {
    mobileFilterAppliquer.addEventListener("click", appliquerMobileFiltre);
  }

  function toggleCandidatSelection(candidatId) {
    var index = candidatsSelectionnes.indexOf(candidatId);

    if (index === -1) {
      candidatsSelectionnes.push(candidatId);
    } else {
      // Empêcher de tout désélectionner
      if (candidatsSelectionnes.length > 1) {
        candidatsSelectionnes.splice(index, 1);
      } else {
        afficherToast("Au moins un candidat doit être sélectionné");
        return;
      }
    }

    var candidats = donneesElection.candidats.slice().sort(function (a, b) {
      return a.nom.localeCompare(b.nom, "fr");
    });

    afficherSelectionCandidats(candidats);
    afficherRepartition(candidats);
    afficherGrille(candidats);
    genererStatistiques(candidats);
    afficherTreemap();
    mettreAJourURL();
  }

  function getCandidatsActifs() {
    if (!donneesElection) return [];
    return donneesElection.candidats.filter(function (c) {
      return candidatsSelectionnes.indexOf(c.id) !== -1;
    }).sort(function (a, b) {
      return a.nom.localeCompare(b.nom, "fr");
    });
  }

  // === Partage et permaliens ===
  function mettreAJourURL() {
    if (!donneesElection || !villeSelectionnee) return;

    var params = new URLSearchParams();
    params.set("ville", villeSelectionnee.id);

    if (categorieActive && categorieActive !== "toutes") {
      params.set("theme", categorieActive);
    }

    if (candidatsSelectionnes.length < donneesElection.candidats.length) {
      params.set("candidats", candidatsSelectionnes.join(","));
    }

    var newUrl = window.location.pathname + "?" + params.toString();
    window.history.replaceState({}, "", newUrl);
  }

  function genererURLAvecUTM(medium) {
    mettreAJourURL();
    var baseUrl = window.location.origin + window.location.pathname + window.location.search;

    var params = new URLSearchParams(window.location.search);
    params.set("utm_source", "partage");
    params.set("utm_medium", medium);
    params.set("utm_campaign", "pourquituvotes");

    return window.location.origin + window.location.pathname + "?" + params.toString();
  }

  function obtenirTextePartage() {
    if (!donneesElection) return "";

    var candidatsNoms = getCandidatsActifs().map(function(c) { return c.nom; }).join(", ");
    var texte = "Comparez les programmes de " + candidatsNoms +
                " pour " + donneesElection.ville + " " + donneesElection.annee;

    return texte;
  }

  function chargerDepuisURL() {
    var params = new URLSearchParams(window.location.search);
    var villeId = params.get("ville");

    if (villeId) {
      var ville = VILLES.find(function (v) { return v.id === villeId; });
      if (ville) {
        var candidatsParam = params.get("candidats");
        if (candidatsParam) {
          candidatsSelectionnes = candidatsParam.split(",");
        }

        villeSearchInput.value = ville.nom + " (" + ville.codePostal + ")";
        selectionnerVille(ville);

        var categorieParam = params.get("theme") || params.get("categorie");
        if (categorieParam) {
          var aliasCategories = {
            "amenagement": "urbanisme",
            "ecologie-pouvoir-achat": "environnement",
            "bouclier-social": "solidarite",
            "education-jeunesse": "education",
            "culture-sport": "culture",
            "egalite-droits": "solidarite",
            "grand-paris": "economie",
            "evenementiel": "sport",
            "services-familles": "democratie",
            "services-publics": "democratie",
            "tourisme-loisirs": "economie",
            "egalite": "solidarite",
            "ecologie": "environnement",
            "transport": "transports",
            "emploi": "economie"
          };
          categorieActive = aliasCategories[categorieParam] || categorieParam;
        }
      }
    }
  }

  function copierLien() {
    mettreAJourURL();
    var url = genererURLAvecUTM("copie_directe");

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(function () {
        afficherToast("\u2713 Lien copi\u00e9 ! Partagez-le avec vos proches");
        if (btnPartager) btnPartager.innerHTML = '<i class="ph ph-check"></i>';
        setTimeout(function() {
          if (btnPartager) btnPartager.innerHTML = '<i class="ph ph-link"></i>';
        }, 1500);
      }).catch(function () {
        afficherToast("Erreur lors de la copie du lien");
      });
    } else {
      var textarea = document.createElement("textarea");
      textarea.value = url;
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand("copy");
        afficherToast("\u2713 Lien copi\u00e9 !");
        if (btnPartager) btnPartager.innerHTML = '<i class="ph ph-check"></i>';
        setTimeout(function() {
          if (btnPartager) btnPartager.innerHTML = '<i class="ph ph-link"></i>';
        }, 1500);
      } catch (err) {
        afficherToast("Impossible de copier le lien");
      }
      document.body.removeChild(textarea);
    }
  }

  function partagerSurReseau(reseau) {
    var url = genererURLAvecUTM(reseau);
    var texte = obtenirTextePartage();
    var urlPartage = "";

    switch(reseau) {
      case "facebook":
        urlPartage = "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(url);
        break;
      case "twitter":
        urlPartage = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(texte) + "&url=" + encodeURIComponent(url);
        break;
      case "linkedin":
        urlPartage = "https://www.linkedin.com/sharing/share-offsite/?url=" + encodeURIComponent(url);
        break;
      case "whatsapp":
        urlPartage = "https://wa.me/?text=" + encodeURIComponent(texte + " " + url);
        break;
      case "email":
        urlPartage = "mailto:?subject=" + encodeURIComponent(texte) + "&body=" + encodeURIComponent(texte + "\n\n" + url);
        break;
    }

    if (urlPartage) {
      window.open(urlPartage, "_blank", "width=600,height=400");
      afficherToast("✓ Fenêtre de partage ouverte");
    }
  }

  function afficherToast(message) {
    var toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(function () {
      toast.style.animation = "slideInUp 0.3s ease-out reverse";
      setTimeout(function () {
        document.body.removeChild(toast);
      }, 300);
    }, 3000);
  }

  // === Progress Pills Navigation ===
  function genererSommaire() {
    if (!donneesElection || !progressPills || !progressPillsList) {
      if (progressPills) progressPills.hidden = true;
      return;
    }

    progressPillsList.innerHTML = "";
    var totalCats = donneesElection.categories.length;

    donneesElection.categories.forEach(function (cat) {
      var icone = getIconeCategorie(cat.id);

      var pill = document.createElement("div");
      pill.className = "progress-pill";
      pill.dataset.categorie = cat.id;

      var tooltip = document.createElement("span");
      tooltip.className = "progress-pill__tooltip";
      var nomCourt = cat.nom.split(" & ")[0].split(" et ")[0];
      tooltip.textContent = nomCourt;
      pill.appendChild(tooltip);

      pill.addEventListener("click", function () {
        var el = comparaisonContainer.querySelector("[data-categorie-id='" + cat.id + "']");
        if (el) {
          if (!el.classList.contains("categorie--ouverte")) {
            el.classList.add("categorie--ouverte");
          }
          el.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });

      progressPillsList.appendChild(pill);
    });

    if (progressPillsCounter) {
      progressPillsCounter.textContent = "0/" + totalCats;
    }

    progressPills.hidden = false;
    progressPills.classList.add("progress-pills--hidden");
    initPillsScrollSpy();
  }

  var pillsScrollSpyInit = false;
  function initPillsScrollSpy() {
    if (pillsScrollSpyInit) return;
    pillsScrollSpyInit = true;

    window.addEventListener("scroll", function () {
      if (progressPills.hidden) return;

      // Visibility: show only when category sections are in view
      var premiereCat = comparaisonContainer.querySelector("[data-categorie-id]");
      var derniereCat = comparaisonContainer.querySelector("[data-categorie-id]:last-of-type");
      if (!premiereCat) { progressPills.classList.add("progress-pills--hidden"); return; }
      var topRect = premiereCat.getBoundingClientRect();
      var bottomRect = derniereCat ? derniereCat.getBoundingClientRect() : topRect;
      var dansSection = topRect.top < window.innerHeight && bottomRect.bottom > 0;
      progressPills.classList.toggle("progress-pills--hidden", !dansSection);

      // Find visible section
      var sections = comparaisonContainer.querySelectorAll("[data-categorie-id]");
      if (sections.length === 0) return;

      var activeIdx = -1;
      var viewMid = window.innerHeight * 0.35;
      for (var i = 0; i < sections.length; i++) {
        var rect = sections[i].getBoundingClientRect();
        if (rect.top <= viewMid) {
          activeIdx = i;
        }
      }

      // Update pills
      var pills = progressPillsList.querySelectorAll(".progress-pill");
      pills.forEach(function (pill, idx) {
        pill.classList.remove("progress-pill--active", "progress-pill--past");
        if (idx === activeIdx) {
          pill.classList.add("progress-pill--active");
        } else if (idx < activeIdx) {
          pill.classList.add("progress-pill--past");
        }
      });

      // Update counter
      if (progressPillsCounter) {
        var current = activeIdx >= 0 ? activeIdx + 1 : 0;
        progressPillsCounter.textContent = current + "/" + sections.length;
      }
    }, { passive: true });
  }

  function mettreAJourSommaireActif() {
    // Compatibility stub — scroll spy handles active state
  }

  // === Bouton retour en haut ===
  function gererScrollTop() {
    if (window.pageYOffset > 300) {
      btnTop.hidden = false;
    } else {
      btnTop.hidden = true;
    }
  }

  function scrollVersHaut() {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }

  // === Mode sombre ===
  function chargerTheme() {
    var theme = localStorage.getItem("theme") || "light";
    appliquerTheme(theme);
  }

  function appliquerTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);

    // Régénérer les statistiques si elles existent
    if (donneesElection && !statistiquesSection.hidden) {
      var candidats = donneesElection.candidats.slice().sort(function (a, b) {
        return a.nom.localeCompare(b.nom, "fr");
      });
      genererStatistiques(candidats);
    }
  }

  function togglerTheme() {
    var themeActuel = document.documentElement.getAttribute("data-theme") || "light";
    var nouveauTheme = themeActuel === "light" ? "dark" : "light";
    appliquerTheme(nouveauTheme);
  }

  // === Alertes programmes ===
  function afficherAlertes() {
    if (!donneesElection) {
      alertesSection.hidden = true;
      return;
    }

    var total = donneesElection.candidats.length;
    var complets = donneesElection.candidats.filter(function(c) { return c.programmeComplet; }).length;
    var programmesIncomplets = complets < total;

    alertesSection.hidden = !programmesIncomplets;

    var titreCount = document.getElementById("alertes-titre-count");
    if (titreCount) {
      var ville = donneesElection.ville || "";
      var annee = donneesElection.annee || "";
      titreCount.textContent = "Municipales " + ville + " " + annee + " : " + complets + " programme" + (complets > 1 ? "s" : "") + " officiel" + (complets > 1 ? "s" : "") + " publi\u00E9" + (complets > 1 ? "s" : "") + " sur " + total;
    }
  }

  function validerEmail(email) {
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  }

  function afficherMessageAlerte(message, type) {
    alerteMessage.textContent = message;
    alerteMessage.className = "alerte-message alerte-message--" + type;
    alerteMessage.hidden = false;

    setTimeout(function() {
      alerteMessage.hidden = true;
    }, 5000);
  }

  function inscrireAlerte() {
    var email = alerteEmailInput.value.trim();

    if (!email) {
      afficherMessageAlerte("Veuillez entrer une adresse email.", "error");
      return;
    }

    if (!validerEmail(email)) {
      afficherMessageAlerte("Veuillez entrer une adresse email valide.", "error");
      return;
    }

    if (!villeSelectionnee) {
      afficherMessageAlerte("Veuillez d'abord sélectionner une ville.", "error");
      return;
    }

    // Récupérer les alertes existantes
    var alertes = JSON.parse(localStorage.getItem("alertes-programmes") || "{}");

    // Créer la clé pour cette ville
    var villeId = villeSelectionnee.id;
    if (!alertes[villeId]) {
      alertes[villeId] = [];
    }

    // Vérifier si l'email est déjà inscrit pour cette ville
    if (alertes[villeId].indexOf(email) !== -1) {
      afficherMessageAlerte("Vous êtes déjà inscrit aux alertes pour " + villeSelectionnee.nom + ".", "error");
      return;
    }

    // Ajouter l'email
    alertes[villeId].push(email);
    localStorage.setItem("alertes-programmes", JSON.stringify(alertes));

    afficherMessageAlerte("✓ Inscription confirmée ! Vous serez notifié par email.", "success");
    alerteEmailInput.value = "";
  }

  // === Affichage complet ===
  // === Dates clés ===
  var DATES_CLES = [
    { date: new Date("2026-02-06"), label: "Date limite d\u2019inscription sur les listes \u00e9lectorales" },
    { date: new Date("2026-02-26"), label: "Date limite de d\u00e9p\u00f4t des candidatures (1er tour)" },
    { date: new Date("2026-03-02"), label: "Ouverture de la campagne \u00e9lectorale officielle" },
    { date: new Date("2026-03-14"), label: "Fin de la campagne \u00e9lectorale (1er tour)" },
    { date: new Date("2026-03-15"), label: "Premier tour des \u00e9lections municipales" },
    { date: new Date("2026-03-17"), label: "Date limite de d\u00e9p\u00f4t des candidatures (2nd tour)" },
    { date: new Date("2026-03-22"), label: "Second tour des \u00e9lections municipales" }
  ];

  function afficherProchaineDateCle() {
    var existant = document.getElementById("prochaine-date-cle");
    if (existant) existant.remove();

    var maintenant = new Date();
    var prochaine = null;
    for (var i = 0; i < DATES_CLES.length; i++) {
      if (DATES_CLES[i].date >= maintenant) {
        prochaine = DATES_CLES[i];
        break;
      }
    }
    if (!prochaine) return;

    var options = { day: "numeric", month: "long" };
    var dateFormatee = prochaine.date.toLocaleDateString("fr-FR", options);

    var div = document.createElement("p");
    div.id = "prochaine-date-cle";
    div.className = "prochaine-date-cle";
    div.innerHTML = "\uD83D\uDCC5 <strong>" + dateFormatee + "</strong> \u2014 " + prochaine.label;
    electionStats.parentNode.insertBefore(div, electionStats.nextSibling);
  }

  function afficherElection() {
    if (!donneesElection) return;

    var candidats = donneesElection.candidats.slice().sort(function (a, b) {
      return a.nom.localeCompare(b.nom, "fr");
    });

    var totalPropositions = 0;
    donneesElection.categories.forEach(function (cat) {
      totalPropositions += compterPropositionsCategorie(cat);
    });

    electionTitre.textContent =
      donneesElection.type + " \u2014 " + donneesElection.ville + " " + donneesElection.annee;
    electionInfo.hidden = false;

    // Afficher la toolbar partage
    var toolbar = document.getElementById("toolbar");
    if (toolbar) toolbar.hidden = false;

    // Mettre à jour hero dynamique
    mettreAJourHeroEtat(donneesElection.ville);

    // Afficher la prochaine date clé
    afficherProchaineDateCle();

    // Cas : aucun candidat déclaré
    if (candidats.length === 0) {
      electionStats.textContent = "Aucun candidat d\u00e9clar\u00e9 pour le moment";
      aucunCandidatSection.hidden = false;
      selectionCandidatsSection.hidden = true;
      alertesSection.hidden = true;
      repartitionSection.hidden = true;
      statistiquesSection.hidden = true;
      var treemapSec = document.getElementById("treemap-section");
      if (treemapSec) treemapSec.hidden = true;
      filtresContainer.hidden = true;
      comparaisonContainer.hidden = true;
      etatVide.hidden = true;
      if (mobileFilterBtn) mobileFilterBtn.hidden = true;
      return;
    }

    aucunCandidatSection.hidden = true;
    electionStats.textContent =
      candidats.length + " candidats \u00B7 " +
      donneesElection.categories.length + " cat\u00E9gories \u00B7 " +
      totalPropositions + " propositions";

    afficherSelectionCandidats(candidats);
    genererStatistiques(candidats);
    afficherTreemap();
    afficherAlertes();
    afficherRepartition(candidats);
    afficherFiltres();
    afficherGrille(candidats);
    genererSommaire();

    etatVide.hidden = true;
    comparaisonContainer.hidden = false;
  }

  // === Statistiques visuelles ===
  function genererStatistiques(tousLesCandidats) {
    if (!donneesElection) return;

    // Masquer le radar s'il y a moins de 10 propositions au total
    var totalPropsRadar = 0;
    donneesElection.categories.forEach(function(cat) {
      totalPropsRadar += compterPropositionsCategorie(cat);
    });
    if (totalPropsRadar < 10) {
      statistiquesSection.hidden = true;
      return;
    }

    var candidats = getCandidatsActifs();

    // Détruire les anciens graphiques
    // if (chartsInstances.total) {
    //   chartsInstances.total.destroy();
    // }
    if (chartsInstances.radar) {
      chartsInstances.radar.destroy();
    }

    // Compter les propositions par candidat
    var data = [];
    var labels = [];
    var couleurs = [
      "rgba(52, 152, 219, 0.8)",
      "rgba(46, 204, 113, 0.8)",
      "rgba(155, 89, 182, 0.8)",
      "rgba(241, 196, 15, 0.8)",
      "rgba(231, 76, 60, 0.8)",
      "rgba(26, 188, 156, 0.8)",
      "rgba(230, 126, 34, 0.8)",
      "rgba(41, 128, 185, 0.8)",
      "rgba(39, 174, 96, 0.8)",
      "rgba(142, 68, 173, 0.8)",
      "rgba(243, 156, 18, 0.8)",
      "rgba(192, 57, 43, 0.8)",
      "rgba(22, 160, 133, 0.8)",
      "rgba(211, 84, 0, 0.8)"
    ];

    candidats.forEach(function (candidat) {
      var count = 0;
      donneesElection.categories.forEach(function (cat) {
        count += compterPropositionsCandidat(cat, candidat.id);
      });
      labels.push(candidat.nom);
      data.push(count);
    });

    // Obtenir la couleur de texte selon le thème
    var theme = document.documentElement.getAttribute("data-theme") || "light";
    var couleurTexte = theme === "dark" ? "#e8edf5" : "#1a1a2e";
    var couleurGrille = theme === "dark" ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)";

    // Graphique en barres désactivé (gardé uniquement le radar)
    // var ctx = document.getElementById("chart-total");
    // if (ctx) {
    //   chartsInstances.total = new Chart(ctx, {
    //     type: "bar",
    //     data: {
    //       labels: labels,
    //       datasets: [{
    //         label: "Nombre de propositions",
    //         data: data,
    //         backgroundColor: couleurs.slice(0, candidats.length),
    //         borderColor: couleurs.slice(0, candidats.length).map(function(c) {
    //           return c.replace("0.8", "1");
    //         }),
    //         borderWidth: 1
    //       }]
    //     },
    //     options: {
    //       responsive: true,
    //       maintainAspectRatio: true,
    //       plugins: {
    //         legend: {
    //           display: false
    //         },
    //         tooltip: {
    //           backgroundColor: theme === "dark" ? "#252538" : "#ffffff",
    //           titleColor: couleurTexte,
    //           bodyColor: couleurTexte,
    //           borderColor: couleurGrille,
    //           borderWidth: 1
    //         }
    //       },
    //       scales: {
    //         y: {
    //           beginAtZero: true,
    //           ticks: {
    //             color: couleurTexte,
    //             stepSize: 1
    //           },
    //           grid: {
    //             color: couleurGrille
    //           }
    //         },
    //         x: {
    //           ticks: {
    //             color: couleurTexte
    //           },
    //           grid: {
    //             color: couleurGrille
    //           }
    //         }
    //       }
    //     }
    //   });
    // }

    // === Radar chart — Radar de Puissance (Volume Brut) ===
    var radarComparer = document.getElementById("radar-vue-comparer");
    var radarCandidatsSelectionnes = [];

    if (donneesElection && radarComparer) {
      var categories = donneesElection.categories;
      var categoriesLabels = categories.map(function(cat) { return cat.nom; });
      var couleurGrilleRadar = theme === "dark" ? "rgba(255,255,255,0.1)" : "#e5e5e5";
      var couleurTexteRadar = theme === "dark" ? "#ccc" : "#555";
      var couleurMoyenne = theme === "dark" ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.05)";
      var couleurMoyenneBord = theme === "dark" ? "rgba(255,255,255,0.15)" : "rgba(0,0,0,0.1)";

      function hexToRgba(hex, alpha) {
        if (!hex || hex.charAt(0) !== "#") return "rgba(128,128,128," + alpha + ")";
        var r = parseInt(hex.slice(1, 3), 16);
        var g = parseInt(hex.slice(3, 5), 16);
        var b = parseInt(hex.slice(5, 7), 16);
        return "rgba(" + r + "," + g + "," + b + "," + alpha + ")";
      }

      // Données brutes directes (nombre de propositions par catégorie)
      function getDataCandidat(candidat) {
        return categories.map(function(cat) {
          return compterPropositionsCandidat(cat, candidat.id);
        });
      }

      // Moyenne brute par catégorie (tous candidats)
      var moyenneParCategorie = categories.map(function(cat) {
        var total = 0;
        candidats.forEach(function(c) { total += compterPropositionsCandidat(cat, c.id); });
        return candidats.length > 0 ? Math.round(total / candidats.length * 10) / 10 : 0;
      });

      var LABELS_COURTS = {
        "S\u00E9curit\u00E9 & Pr\u00E9vention": "S\u00E9curit\u00E9",
        "Transports & Mobilit\u00E9": "Transports",
        "Logement": "Logement",
        "\u00C9ducation & Jeunesse": "\u00C9ducation",
        "Environnement & Transition \u00E9cologique": "Environnement",
        "Sant\u00E9 & Acc\u00E8s aux soins": "Sant\u00E9",
        "D\u00E9mocratie & Vie citoyenne": "D\u00E9mocratie",
        "\u00C9conomie & Emploi": "\u00C9conomie",
        "Culture & Patrimoine": "Culture",
        "Sport & Loisirs": "Sport",
        "Urbanisme & Cadre de vie": "Urbanisme",
        "Solidarit\u00E9 & \u00C9galit\u00E9": "Solidarit\u00E9"
      };
      var labelsRadar = categories.map(function(cat) { return LABELS_COURTS[cat.nom] || cat.nom; });

      // Options radar — données brutes, suggestedMax 10, grille circulaire
      function getRadarOptions() {
        return {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: theme === "dark" ? "#252538" : "#fff",
              titleColor: couleurTexteRadar,
              bodyColor: couleurTexteRadar,
              borderColor: couleurGrilleRadar,
              borderWidth: 1,
              filter: function(item) { return item.dataset.label !== "Moyenne"; },
              callbacks: {
                label: function(ctx) {
                  var candidatNom = ctx.dataset.label || "";
                  var themeNom = ctx.chart.data.labels[ctx.dataIndex] || "";
                  var nb = ctx.parsed.r;
                  return candidatNom + " \u2014 " + nb + " proposition" + (nb > 1 ? "s" : "") + " en " + themeNom;
                }
              }
            }
          },
          scales: {
            r: {
              min: 0,
              suggestedMax: 10,
              ticks: {
                color: couleurTexteRadar,
                backdropColor: "transparent",
                stepSize: 2,
                callback: function(v) { return v === 0 ? "" : v; }
              },
              grid: { color: couleurGrilleRadar, circular: true },
              angleLines: { color: couleurGrilleRadar },
              pointLabels: { color: couleurTexteRadar, padding: 15, font: { family: "'DM Sans', sans-serif", size: 11, weight: 600 } }
            }
          }
        };
      }

      // Dataset de la moyenne (zone grise de repère)
      function getMoyenneDataset(moyData) {
        return {
          label: "Moyenne",
          data: moyData,
          backgroundColor: couleurMoyenne,
          borderColor: couleurMoyenneBord,
          borderWidth: 1,
          borderDash: [4, 4],
          pointRadius: 0,
          pointHoverRadius: 0,
          fill: true,
          order: 100 // derrière tout
        };
      }

      // --- Vue 2 : radar combiné avec checkboxes ---
      function rendreVueComparer() {
        var selDiv = document.getElementById("radar-selection-candidats");
        selDiv.innerHTML = "";
        radarCandidatsSelectionnes = [];

        var header = document.createElement("div");
        header.className = "filtres-candidats__header";
        header.innerHTML = '<span class="filtres-candidats__titre">Candidats \u00e0 comparer</span>';
        selDiv.appendChild(header);

        var liste = document.createElement("div");
        liste.className = "filtres-candidats__liste";

        candidats.forEach(function(candidat, idx) {
          var couleur = getCouleurParti(candidat, idx);
          var estPreselectionne = (idx < 2);

          var chip = document.createElement("span");
          chip.className = "filtres-candidats__chip" + (estPreselectionne ? " filtres-candidats__chip--active" : "");
          chip.style.setProperty("--chip-couleur", couleur);
          if (estPreselectionne) {
            var r = parseInt(couleur.slice(1, 3), 16) || 44;
            var g = parseInt(couleur.slice(3, 5), 16) || 62;
            var b = parseInt(couleur.slice(5, 7), 16) || 107;
            chip.style.setProperty("--chip-bg", "rgba(" + r + "," + g + "," + b + ",0.08)");
          }
          chip.dataset.candidatId = candidat.id;

          var cb = document.createElement("span");
          cb.className = "filtres-candidats__chip-cb";
          cb.textContent = "\u2713";

          chip.appendChild(cb);
          chip.appendChild(document.createTextNode(echapper(candidat.nom)));

          // Ajouter l'initiale du parti
          var initSpan = document.createElement("span");
          initSpan.className = "filtres-candidats__chip-parti";
          initSpan.textContent = getInitialeParti(candidat);
          initSpan.style.color = couleur;
          chip.appendChild(initSpan);

          chip.addEventListener("click", function() {
            var id = candidat.id;
            var pos = radarCandidatsSelectionnes.indexOf(id);
            if (pos >= 0) {
              radarCandidatsSelectionnes.splice(pos, 1);
              chip.classList.remove("filtres-candidats__chip--active");
              chip.style.removeProperty("--chip-bg");
            } else {
              radarCandidatsSelectionnes.push(id);
              chip.classList.add("filtres-candidats__chip--active");
              var r2 = parseInt(couleur.slice(1, 3), 16) || 44;
              var g2 = parseInt(couleur.slice(3, 5), 16) || 62;
              var b2 = parseInt(couleur.slice(5, 7), 16) || 107;
              chip.style.setProperty("--chip-bg", "rgba(" + r2 + "," + g2 + "," + b2 + ",0.08)");
            }
            mettreAJourRadarComparer();
          });

          liste.appendChild(chip);
          if (estPreselectionne) {
            radarCandidatsSelectionnes.push(candidat.id);
          }
        });

        selDiv.appendChild(liste);

        // Bouton "Aucun" en bas du panel
        var btnAucun = document.createElement("button");
        btnAucun.className = "filtres-candidats__btn filtres-candidats__btn--danger filtres-candidats__btn--bottom";
        btnAucun.innerHTML = "\u2717 Tout d\u00e9cocher";
        selDiv.appendChild(btnAucun);

        btnAucun.addEventListener("click", function() {
          if (candidats.length > 0) {
            radarCandidatsSelectionnes = [candidats[0].id];
            liste.querySelectorAll(".filtres-candidats__chip").forEach(function(chip, idx) {
              if (idx === 0) {
                chip.classList.add("filtres-candidats__chip--active");
                var couleur = getCouleurParti(candidats[0], 0);
                var r = parseInt(couleur.slice(1, 3), 16) || 44;
                var g = parseInt(couleur.slice(3, 5), 16) || 62;
                var b = parseInt(couleur.slice(5, 7), 16) || 107;
                chip.style.setProperty("--chip-bg", "rgba(" + r + "," + g + "," + b + ",0.08)");
              } else {
                chip.classList.remove("filtres-candidats__chip--active");
                chip.style.removeProperty("--chip-bg");
              }
            });
            mettreAJourRadarComparer();
          }
        });

        var canvasComparer = document.getElementById("chart-radar-comparer");
        if (radarChartComparerGlobal) { radarChartComparerGlobal.destroy(); }

        radarChartComparerGlobal = new Chart(canvasComparer, {
          type: "radar",
          data: { labels: labelsRadar, datasets: [getMoyenneDataset(moyenneParCategorie)] },
          options: getRadarOptions()
        });

        if (radarCandidatsSelectionnes.length > 0) {
          mettreAJourRadarComparer();
        }
      }

      function mettreAJourRadarComparer() {
        if (!radarChartComparerGlobal) return;
        var datasets = [getMoyenneDataset(moyenneParCategorie)];
        radarCandidatsSelectionnes.forEach(function(id) {
          var candidat = null;
          var idx = 0;
          for (var i = 0; i < candidats.length; i++) {
            if (candidats[i].id === id) { candidat = candidats[i]; idx = i; break; }
          }
          if (!candidat) return;
          var couleur = getCouleurParti(candidat, idx);
          datasets.push({
            label: candidat.nom,
            data: getDataCandidat(candidat),
            backgroundColor: hexToRgba(couleur, 0.15),
            borderColor: couleur,
            borderWidth: 2.5,
            pointBackgroundColor: couleur,
            pointBorderColor: "#fff",
            pointRadius: 4,
            pointHoverRadius: 6
          });
        });
        radarChartComparerGlobal.data.datasets = datasets;
        radarChartComparerGlobal.update();
      }

      radarComparer.hidden = false;
      rendreVueComparer();
    }

    // Afficher l'encart méthodologique sous le radar
    var methodoDiv = document.getElementById("radar-methodologie");
    if (methodoDiv && donneesElection) {
      var tousCandidats = donneesElection.candidats;
      var complets = tousCandidats.filter(function(c) { return c.programmeComplet; });
      var partiels = tousCandidats.filter(function(c) { return !c.programmeComplet; });

      var html = '<strong><i class="ph ph-scales"></i> \u00C9quit\u00E9 de comparaison :</strong> ';
      if (complets.length > 0 && partiels.length > 0) {
        html += 'Tous les candidats n\u2019ont pas encore publi\u00E9 leur programme officiel. ';
        html += 'Un radar plus petit ne signifie pas forc\u00E9ment moins d\u2019ambition, mais parfois simplement moins de propositions rendues publiques \u00E0 ce jour.';
        html += '<div class="methodo-legend">';
        complets.forEach(function(c) {
          html += '<span class="methodo-item"><strong class="methodo-item__nom">' + c.nom + '</strong><span class="methodo-item__statut methodo-item__statut--complet">programme officiel <i class="ph ph-check-circle"></i></span></span>';
        });
        partiels.forEach(function(c) {
          html += '<span class="methodo-item"><strong class="methodo-item__nom">' + c.nom + '</strong><span class="methodo-item__statut methodo-item__statut--partiel">programme \u00E0 venir <i class="ph ph-clock"></i></span></span>';
        });
        html += '</div>';
      } else if (complets.length === tousCandidats.length) {
        html += 'Tous les candidats affich\u00E9s ont publi\u00E9 un programme officiel. Les donn\u00E9es sont exhaustives.';
      } else {
        html += 'Aucun candidat n\u2019a encore publi\u00E9 de programme officiel. Les donn\u00E9es sont bas\u00E9es sur des sources publiques - programme \u00E0 venir.';
      }

      methodoDiv.innerHTML = html;
    }

    // Afficher la section
    statistiquesSection.hidden = false;
  }

  // === Treemap — ADN Politique ===
  var LABELS_TREEMAP = {
    "securite": "S\u00e9curit\u00e9",
    "transports": "Transports",
    "logement": "Logement",
    "education": "\u00c9ducation",
    "environnement": "Environnement",
    "sante": "Sant\u00e9",
    "democratie": "D\u00e9mocratie",
    "economie": "\u00c9conomie",
    "culture": "Culture",
    "sport": "Sport",
    "urbanisme": "Urbanisme",
    "solidarite": "Solidarit\u00e9"
  };

  var ICONES_PHOSPHOR_CATEGORIES = {
    "securite": "shield-check",
    "transports": "bus",
    "logement": "house-line",
    "education": "graduation-cap",
    "environnement": "leaf",
    "sante": "heart-half",
    "democratie": "megaphone",
    "economie": "storefront",
    "culture": "mask-happy",
    "sport": "soccer-ball",
    "urbanisme": "buildings",
    "solidarite": "handshake"
  };
  function getIconePhosphorCategorie(id) {
    return ICONES_PHOSPHOR_CATEGORIES[id] || "clipboard-text";
  }

  var treemapModeDuel = false;
  var treemapCandidatPrincipal = null;
  var treemapCandidatAdversaire = null;

  function afficherTreemap() {
    var treemapSection = document.getElementById("treemap-section");
    var treemapGrille = document.getElementById("treemap-grille");
    var treemapChips = document.getElementById("treemap-chips");
    var btnComparer = document.getElementById("treemap-btn-comparer");
    if (!treemapSection || !treemapGrille) return;

    var candidatsActifs = getCandidatsActifs();

    if (candidatsActifs.length === 0) {
      treemapSection.hidden = true;
      return;
    }

    // Sélectionner le principal s'il n'est pas encore choisi ou invalide
    if (!treemapCandidatPrincipal || !candidatsActifs.some(function(c) { return c.id === treemapCandidatPrincipal; })) {
      treemapCandidatPrincipal = candidatsActifs[0].id;
    }

    // Vérifier l'adversaire en mode duel
    if (treemapModeDuel && treemapCandidatAdversaire) {
      if (!candidatsActifs.some(function(c) { return c.id === treemapCandidatAdversaire; }) || treemapCandidatAdversaire === treemapCandidatPrincipal) {
        treemapCandidatAdversaire = null;
      }
    }

    // Chips candidats
    treemapChips.innerHTML = "";
    candidatsActifs.forEach(function(candidat, idx) {
      var couleur = getCouleurParti(candidat, idx);
      var chip = document.createElement("button");
      chip.className = "treemap__chip" + (candidat.id === treemapCandidatPrincipal ? " treemap__chip--active" : "");
      chip.style.setProperty("--chip-couleur", couleur);
      if (candidat.id === treemapCandidatPrincipal) {
        var r = parseInt(couleur.slice(1, 3), 16) || 44;
        var g = parseInt(couleur.slice(3, 5), 16) || 62;
        var b = parseInt(couleur.slice(5, 7), 16) || 107;
        chip.style.setProperty("--chip-bg", "rgba(" + r + "," + g + "," + b + ",0.08)");
      }
      chip.innerHTML =
        '<span class="treemap__chip-pastille" style="background:' + couleur + '"></span>' +
        echapper(candidat.nom);
      chip.addEventListener("click", function() {
        treemapCandidatPrincipal = candidat.id;
        if (treemapCandidatAdversaire === candidat.id) treemapCandidatAdversaire = null;
        rendreTreemap();
      });
      treemapChips.appendChild(chip);
    });

    // Bouton comparer
    if (btnComparer) {
      btnComparer.textContent = treemapModeDuel ? "Fermer" : "Comparer l'ADN";
      btnComparer.className = "treemap__btn-comparer" + (treemapModeDuel ? " treemap__btn-comparer--active" : "");
      btnComparer.onclick = function() {
        treemapModeDuel = !treemapModeDuel;
        if (!treemapModeDuel) treemapCandidatAdversaire = null;
        rendreTreemap();
      };
      // Masquer le bouton si un seul candidat actif
      btnComparer.hidden = (candidatsActifs.length < 2);
    }

    rendreTreemap();
    treemapSection.hidden = false;
  }

  function rendreTreemap() {
    var treemapGrille = document.getElementById("treemap-grille");
    var treemapChips = document.getElementById("treemap-chips");
    var btnComparer = document.getElementById("treemap-btn-comparer");
    if (!treemapGrille) return;

    var candidatsActifs = getCandidatsActifs();
    treemapGrille.innerHTML = "";

    // MAJ chips (état actif)
    if (treemapChips) {
      var chips = treemapChips.querySelectorAll(".treemap__chip");
      chips.forEach(function(chip, idx) {
        var candidat = candidatsActifs[idx];
        if (!candidat) return;
        var couleur = getCouleurParti(candidat, idx);
        if (candidat.id === treemapCandidatPrincipal) {
          chip.classList.add("treemap__chip--active");
          var r = parseInt(couleur.slice(1, 3), 16) || 44;
          var g = parseInt(couleur.slice(3, 5), 16) || 62;
          var b = parseInt(couleur.slice(5, 7), 16) || 107;
          chip.style.setProperty("--chip-bg", "rgba(" + r + "," + g + "," + b + ",0.08)");
        } else {
          chip.classList.remove("treemap__chip--active");
          chip.style.removeProperty("--chip-bg");
        }
      });
    }

    // MAJ bouton comparer
    if (btnComparer) {
      btnComparer.textContent = treemapModeDuel ? "Fermer" : "Comparer l'ADN";
      btnComparer.className = "treemap__btn-comparer" + (treemapModeDuel ? " treemap__btn-comparer--active" : "");
    }

    if (treemapModeDuel) {
      treemapGrille.className = "treemap__grille treemap__grille--duel";

      // Slot 1 : principal
      var principal = candidatsActifs.filter(function(c) { return c.id === treemapCandidatPrincipal; })[0];
      if (principal) {
        var idxP = candidatsActifs.indexOf(principal);
        treemapGrille.appendChild(creerTreemapCarte(principal, idxP));
      }

      // Slot 2 : adversaire ou placeholder
      if (treemapCandidatAdversaire) {
        var adversaire = candidatsActifs.filter(function(c) { return c.id === treemapCandidatAdversaire; })[0];
        if (adversaire) {
          var idxA = candidatsActifs.indexOf(adversaire);
          treemapGrille.appendChild(creerTreemapCarte(adversaire, idxA));
        }
      } else {
        treemapGrille.appendChild(creerTreemapPlaceholder(candidatsActifs));
      }
    } else {
      treemapGrille.className = "treemap__grille treemap__grille--solo";

      // Mode solo : 1 seul treemap
      var candidat = candidatsActifs.filter(function(c) { return c.id === treemapCandidatPrincipal; })[0];
      if (candidat) {
        var idxC = candidatsActifs.indexOf(candidat);
        treemapGrille.appendChild(creerTreemapCarte(candidat, idxC));
      }
    }
  }

  function creerTreemapPlaceholder(candidatsActifs) {
    var carte = document.createElement("div");
    carte.className = "treemap-carte treemap-carte--placeholder";

    var label = document.createElement("span");
    label.className = "treemap-placeholder__label";
    label.textContent = "Choisissez un adversaire";
    carte.appendChild(label);

    var select = document.createElement("select");
    select.className = "treemap-placeholder__select";

    var optDefault = document.createElement("option");
    optDefault.value = "";
    optDefault.textContent = "— S\u00e9lectionner —";
    select.appendChild(optDefault);

    candidatsActifs.forEach(function(c) {
      if (c.id === treemapCandidatPrincipal) return;
      var opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.nom;
      select.appendChild(opt);
    });

    select.addEventListener("change", function() {
      if (select.value) {
        treemapCandidatAdversaire = select.value;
        rendreTreemap();
      }
    });

    carte.appendChild(select);
    return carte;
  }

  function creerTreemapCarte(candidat, idx) {
    var couleur = getCouleurParti(candidat, idx);
    var carte = document.createElement("div");
    carte.className = "treemap-carte";

    // Header
    var header = document.createElement("div");
    header.className = "treemap-carte__header";

    var distribution = calculerDistribution(candidat.id);

    header.innerHTML =
      '<span class="treemap-carte__pastille" style="background:' + couleur + '"></span>' +
      '<div><div class="treemap-carte__nom">' + echapper(candidat.nom) + '</div>' +
      '<div class="treemap-carte__parti">' + echapper(candidat.liste || "") + '</div></div>' +
      '<span class="treemap-carte__total">' + distribution.total + ' prop.</span>';
    carte.appendChild(header);

    // Container bento treemap
    var container = document.createElement("div");
    container.className = "treemap-container";

    // Trier par count décroissant, filtrer les vides
    var cats = distribution.categories
      .filter(function(c) { return c.count > 0; })
      .sort(function(a, b) { return b.count - a.count; });

    // Limiter à 5 blocs visibles (1 principal + 4 secondaires), regrouper le reste dans "Autres"
    var blocsVisibles = cats.slice(0, 5);
    var reste = cats.slice(5);
    var autresCount = 0;
    var autresPercent = 0;
    reste.forEach(function(c) { autresCount += c.count; autresPercent += c.percent; });

    blocsVisibles.forEach(function(cat, i) {
      var block = document.createElement("div");
      var isMain = (i === 0);
      var isSmall = (i >= 3);
      block.className = "treemap-block" + (isMain ? " treemap-block--main" : "") + (isSmall ? " treemap-block--small" : "");

      // Nuances du parti : opacité décroissante
      var opacity = 1 - (i * 0.15);
      block.style.backgroundColor = hexToRgbaTreemap(couleur, Math.max(opacity, 0.4));

      var labelCourt = LABELS_TREEMAP[cat.id] || cat.nom;
      block.title = labelCourt + " \u2014 " + cat.count + " (" + Math.round(cat.percent) + "%)";
      block.innerHTML =
        '<span class="treemap-block__icone"><i class="ph ph-' + getIconePhosphorCategorie(cat.id) + '"></i></span>' +
        '<span class="treemap-block__label">' + echapper(labelCourt) + '</span>' +
        '<span class="treemap-block__value">' + cat.count + '</span>' +
        '<span class="treemap-block__percent">' + Math.round(cat.percent) + '%</span>';

      block.addEventListener("click", function() {
        scrollVersCategorie(cat.id);
      });

      container.appendChild(block);
    });

    // Bloc "Autres" si nécessaire
    if (autresCount > 0) {
      var autresBlock = document.createElement("div");
      autresBlock.className = "treemap-block treemap-block--small";
      autresBlock.style.backgroundColor = hexToRgbaTreemap(couleur, 0.25);
      autresBlock.title = "Autres \u2014 " + autresCount + " (" + Math.round(autresPercent) + "%)";
      autresBlock.innerHTML =
        '<span class="treemap-block__icone"><i class="ph ph-dots-three"></i></span>' +
        '<span class="treemap-block__label">Autres</span>' +
        '<span class="treemap-block__value">' + autresCount + '</span>' +
        '<span class="treemap-block__percent">' + Math.round(autresPercent) + '%</span>';
      container.appendChild(autresBlock);
    }

    carte.appendChild(container);
    return carte;
  }

  function hexToRgbaTreemap(hex, alpha) {
    if (!hex || hex.charAt(0) !== "#") return "rgba(128,128,128," + alpha + ")";
    var r = parseInt(hex.slice(1, 3), 16);
    var g = parseInt(hex.slice(3, 5), 16);
    var b = parseInt(hex.slice(5, 7), 16);
    return "rgba(" + r + "," + g + "," + b + "," + alpha + ")";
  }

  function calculerDistribution(candidatId) {
    var total = 0;
    var cats = donneesElection.categories.map(function(cat) {
      var count = compterPropositionsCandidat(cat, candidatId);
      total += count;
      return { id: cat.id, nom: cat.nom, count: count, percent: 0 };
    });
    cats.forEach(function(c) {
      c.percent = total > 0 ? (c.count / total) * 100 : 0;
    });
    return { total: total, categories: cats };
  }

  function scrollVersCategorie(categorieId) {
    var el = document.querySelector("[data-categorie-id='" + categorieId + "']");
    if (el) {
      // Ouvrir l'accordéon si fermé
      if (!el.classList.contains("categorie--ouverte")) {
        el.classList.add("categorie--ouverte");
      }
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      el.classList.add("categorie--highlight");
      setTimeout(function() { el.classList.remove("categorie--highlight"); }, 2000);
    }
  }

  // === Répartition thématique ===
  var repartitionModeActuel = "barres";

  function afficherRepartition(tousLesCandidats) {
    repartitionContenu.innerHTML = "";

    var candidats = getCandidatsActifs();

    // Préparer les données communes
    var donnees = preparerDonneesRepartition(candidats);

    // Toggle de modes (dans le conteneur header externe)
    repartitionToggleContainer.innerHTML =
      '<button class="repartition-toggle__btn' + (repartitionModeActuel === "barres" ? ' repartition-toggle__btn--active' : '') + '" data-rmode="barres">Barres group\u00E9es</button>' +
      '<button class="repartition-toggle__btn' + (repartitionModeActuel === "heatmap" ? ' repartition-toggle__btn--active' : '') + '" data-rmode="heatmap">Heatmap</button>' +
      '<button class="repartition-toggle__btn' + (repartitionModeActuel === "cartes" ? ' repartition-toggle__btn--active' : '') + '" data-rmode="cartes">Cartes individuelles</button>';

    repartitionToggleContainer.onclick = function (e) {
      var btn = e.target.closest("[data-rmode]");
      if (!btn) return;
      repartitionModeActuel = btn.dataset.rmode;
      afficherRepartition(tousLesCandidats);
    };

    // Conteneur du rendu
    var rendu = document.createElement("div");
    rendu.className = "repartition-rendu";

    if (repartitionModeActuel === "barres") {
      rendreBarresGroupees(rendu, donnees, candidats);
    } else if (repartitionModeActuel === "heatmap") {
      rendreHeatmap(rendu, donnees, candidats);
    } else {
      rendreCartesIndividuelles(rendu, donnees, candidats);
    }

    repartitionContenu.appendChild(rendu);

    // Notes (équité, écart volume) en dessous du graphique
    var avertissement = genererAvertissementVolume(candidats, donnees);
    if (avertissement) {
      repartitionContenu.appendChild(avertissement);
    }
    // Répartition masquée : barres intégrées dans les en-têtes de catégories
    repartitionSection.hidden = true;
  }

  function preparerDonneesRepartition(candidats) {
    var categories = [];
    donneesElection.categories.forEach(function (cat) {
      var parCandidat = {};
      var maxNb = 0;
      candidats.forEach(function (c) {
        var nb = compterPropositionsCandidat(cat, c.id);
        parCandidat[c.id] = nb;
        if (nb > maxNb) maxNb = nb;
      });
      categories.push({ id: cat.id, nom: cat.nom, parCandidat: parCandidat, maxNb: maxNb });
    });

    // Totaux par candidat
    var totaux = {};
    candidats.forEach(function (c) {
      var total = 0;
      categories.forEach(function (cat) { total += cat.parCandidat[c.id]; });
      totaux[c.id] = total;
    });

    // Max global
    var maxGlobal = 0;
    categories.forEach(function (cat) {
      candidats.forEach(function (c) {
        if (cat.parCandidat[c.id] > maxGlobal) maxGlobal = cat.parCandidat[c.id];
      });
    });

    return { categories: categories, totaux: totaux, maxGlobal: maxGlobal };
  }

  var COULEURS_REP = [
    "#8B5CF6", "#2563EB", "#16A34A", "#EAB308", "#DC2626",
    "#0891B2", "#EA580C", "#4F46E5", "#059669", "#C026D3",
    "#D97706", "#E11D48", "#0D9488", "#BE123C"
  ];

  // Couleurs officielles des partis politiques fran\u00E7ais
  var COULEURS_PARTIS = {
    "lfi": "#A855F7", "la france insoumise": "#A855F7", "fi\u00E8re et populaire": "#A855F7", "front populaire": "#A855F7",
    "pcf": "#FF2D9A", "communiste": "#FF2D9A",
    "ps": "#FF2D9A", "parti socialiste": "#FF2D9A", "gauche unie": "#FF2D9A", "printemps marseillais": "#FF2D9A", "union de la gauche": "#FF2D9A",
    "eelv": "#22C55E", "\u00E9cologistes": "#22C55E", "respire": "#22C55E", "pour vivre": "#22C55E",
    "modem": "#FFBF00", "centriste": "#FFBF00",
    "renaissance": "#FFBF00", "ensemble": "#FFBF00",
    "horizons": "#FFBF00",
    "lr": "#2D6EFF", "les r\u00E9publicains": "#2D6EFF", "union citoyenne de la droite": "#2D6EFF",
    "rn": "#1447E6", "rassemblement national": "#1447E6",
    "reconqu\u00EAte": "#FF6B00", "reconquete": "#FF6B00",
    "lo": "#A855F7", "lutte ouvri\u00E8re": "#A855F7", "anticapitaliste": "#A855F7",
    "udr": "#2D6EFF", "ciotti": "#2D6EFF",
    "dvd": "#14B8A6", "divers droite": "#14B8A6",
    "dvg": "#FF2D9A", "divers gauche": "#FF2D9A",
    "se": "#14B8A6", "sans \u00E9tiquette": "#14B8A6"
  };

  var INITIALES_PARTIS = {
    "lfi": "LFI", "la france insoumise": "LFI", "fi\u00E8re et populaire": "LFI", "front populaire": "LFI",
    "pcf": "UG", "communiste": "UG",
    "ps": "UG", "parti socialiste": "UG", "gauche unie": "UG", "printemps marseillais": "UG", "union de la gauche": "UG",
    "eelv": "ECO", "\u00E9cologistes": "ECO", "respire": "ECO", "pour vivre": "ECO",
    "modem": "REN", "centriste": "REN",
    "renaissance": "REN", "ensemble": "REN",
    "horizons": "REN",
    "lr": "LR", "les r\u00E9publicains": "LR", "union citoyenne de la droite": "LR",
    "rn": "RN", "rassemblement national": "RN",
    "reconqu\u00EAte": "REC", "reconquete": "REC",
    "lo": "LFI", "lutte ouvri\u00E8re": "LFI", "anticapitaliste": "LFI",
    "udr": "LR", "ciotti": "LR",
    "dvd": "DIV", "divers droite": "DIV",
    "dvg": "UG", "divers gauche": "UG",
    "se": "DIV", "sans \u00E9tiquette": "DIV"
  };

  function getInitialeParti(candidat) {
    var liste = (candidat.liste || "").toLowerCase();
    var keys = Object.keys(INITIALES_PARTIS);
    for (var i = 0; i < keys.length; i++) {
      if (liste.indexOf(keys[i]) !== -1) {
        return INITIALES_PARTIS[keys[i]];
      }
    }
    return "DIV";
  }

  function getCouleurParti(candidat, indexFallback) {
    var liste = (candidat.liste || "").toLowerCase();
    var keys = Object.keys(COULEURS_PARTIS);
    for (var i = 0; i < keys.length; i++) {
      if (liste.indexOf(keys[i]) !== -1) {
        return COULEURS_PARTIS[keys[i]];
      }
    }
    return COULEURS_REP[indexFallback % COULEURS_REP.length];
  }

  // --- Mode A : Tableau matriciel ---
  function rendreTableauMatriciel(container, donnees, candidats) {
    var table = document.createElement("table");
    table.className = "rep-tableau";

    // En-tête
    var thead = '<thead><tr><th class="rep-tableau__cat">Cat\u00E9gorie</th>';
    candidats.forEach(function (c) {
      thead += '<th class="rep-tableau__cand">' + echapper(c.nom) + '<div class="rep-tableau__total">' + donnees.totaux[c.id] + ' prop.</div></th>';
    });
    thead += '</tr></thead>';

    // Corps
    var tbody = '<tbody>';
    donnees.categories.forEach(function (cat) {
      var hasData = false;
      candidats.forEach(function (c) { if (cat.parCandidat[c.id] > 0) hasData = true; });

      tbody += '<tr class="' + (hasData ? '' : 'rep-tableau__row--vide') + '">';
      tbody += '<td class="rep-tableau__cat-cell"><span class="rep-tableau__icone">' + getIconeCategorie(cat.id) + '</span>' + echapper(cat.nom) + '</td>';

      candidats.forEach(function (c, idx) {
        var nb = cat.parCandidat[c.id];
        var pct = donnees.maxGlobal > 0 ? Math.round((nb / donnees.maxGlobal) * 100) : 0;
        var couleur = COULEURS_REP[idx % COULEURS_REP.length];
        tbody += '<td class="rep-tableau__cell">' +
          '<div class="rep-tableau__bar-wrap">' +
            '<div class="rep-tableau__bar" style="width:' + pct + '%;background:' + couleur + '"></div>' +
          '</div>' +
          '<span class="rep-tableau__val">' + nb + '</span>' +
        '</td>';
      });

      tbody += '</tr>';
    });
    tbody += '</tbody>';

    table.innerHTML = thead + tbody;
    container.appendChild(table);
  }

  // --- Mode B : Barres groupées (Flat Minimal Pills) ---
  function rendreBarresGroupees(container, donnees, candidats) {
    // Légende avec couleurs des partis
    var legende = document.createElement("div");
    legende.className = "rep-barres__legende";
    candidats.forEach(function (c, idx) {
      var couleur = getCouleurParti(c, idx);
      legende.innerHTML += '<span class="rep-barres__legende-item"><span class="rep-barres__legende-color" style="background:' + couleur + '"></span>' + echapper(c.nom) + ' <span class="rep-barres__legende-parti">(' + echapper(c.liste) + ')</span></span>';
    });
    container.appendChild(legende);

    donnees.categories.forEach(function (cat) {
      var hasData = false;
      // Calculer le max PAR THÈME (pas global) pour des barres proportionnelles au thème
      var maxTheme = 0;
      candidats.forEach(function (c) {
        var nb = cat.parCandidat[c.id];
        if (nb > 0) hasData = true;
        if (nb > maxTheme) maxTheme = nb;
      });

      var groupe = document.createElement("div");
      groupe.className = "rep-barres__groupe" + (hasData ? '' : ' rep-barres__groupe--vide');

      var labelHTML = '<div class="rep-barres__label"><span class="rep-barres__icone">' + getIconeCategorie(cat.id) + '</span>' + echapper(cat.nom) + '</div>';
      var barresHTML = '<div class="rep-barres__conteneur">';

      candidats.forEach(function (c, idx) {
        var nb = cat.parCandidat[c.id];
        var pct = maxTheme > 0 ? Math.round((nb / maxTheme) * 100) : 0;
        var couleur = getCouleurParti(c, idx);
        var initiale = getInitialeParti(c);
        if (nb > 0) {
          barresHTML += '<div class="rep-barres__ligne">' +
            '<span class="rep-barres__nom" style="color:' + couleur + '">' + echapper(c.nom) + '</span>' +
            '<div class="rep-barres__bar-track">' +
              '<div class="rep-barres__fill" style="width:' + pct + '%;background:' + couleur + '" title="' + echapper(c.nom) + ' : ' + nb + '"><span class="rep-barres__initiale">' + initiale + '</span></div>' +
            '</div>' +
            '<span class="rep-barres__nb">' + nb + '</span>' +
          '</div>';
        } else {
          barresHTML += '<div class="rep-barres__ligne rep-barres__ligne--vide">' +
            '<span class="rep-barres__nom" style="color:' + couleur + ';opacity:0.5">' + echapper(c.nom) + '</span>' +
            '<div class="rep-barres__bar-track">' +
              '<div class="rep-barres__fill rep-barres__fill--vide" style="width:100%" title="' + echapper(c.nom) + ' : aucune proposition">\u2014</div>' +
            '</div>' +
            '<span class="rep-barres__nb rep-barres__nb--vide">0</span>' +
          '</div>';
        }
      });

      barresHTML += '</div>';
      groupe.innerHTML = labelHTML + barresHTML;
      container.appendChild(groupe);
    });
  }

  // --- Mode C : Heatmap ---
  function rendreHeatmap(container, donnees, candidats) {
    var table = document.createElement("table");
    table.className = "rep-heatmap";

    // En-tête
    var thead = '<thead><tr><th class="rep-heatmap__cat">Cat\u00E9gorie</th>';
    candidats.forEach(function (c) {
      thead += '<th class="rep-heatmap__cand">' + echapper(c.nom) + '</th>';
    });
    thead += '<th class="rep-heatmap__cand">Total</th></tr></thead>';

    // Corps
    var tbody = '<tbody>';
    donnees.categories.forEach(function (cat) {
      tbody += '<tr>';
      tbody += '<td class="rep-heatmap__cat-cell"><span class="rep-heatmap__icone">' + getIconeCategorie(cat.id) + '</span>' + echapper(cat.nom) + '</td>';

      var totalCat = 0;
      candidats.forEach(function (c) {
        var nb = cat.parCandidat[c.id];
        totalCat += nb;
        var intensite = donnees.maxGlobal > 0 ? nb / donnees.maxGlobal : 0;
        var bg = intensite > 0 ? 'rgba(52, 152, 219, ' + (0.1 + intensite * 0.7) + ')' : 'transparent';
        var textColor = intensite > 0.5 ? '#fff' : 'var(--couleur-texte)';
        var fontWeight = nb > 0 ? '600' : '400';
        tbody += '<td class="rep-heatmap__cell" style="background:' + bg + ';color:' + textColor + ';font-weight:' + fontWeight + '">' + (nb > 0 ? nb : '\u2014') + '</td>';
      });

      // Total ligne
      var intensiteTot = donnees.maxGlobal > 0 ? (totalCat / (donnees.maxGlobal * candidats.length)) * 2 : 0;
      if (intensiteTot > 1) intensiteTot = 1;
      var bgTot = intensiteTot > 0 ? 'rgba(46, 204, 113, ' + (0.1 + intensiteTot * 0.6) + ')' : 'transparent';
      tbody += '<td class="rep-heatmap__cell rep-heatmap__cell--total" style="background:' + bgTot + '">' + totalCat + '</td>';
      tbody += '</tr>';
    });

    // Ligne total en bas
    tbody += '<tr class="rep-heatmap__row--total"><td class="rep-heatmap__cat-cell"><strong>Total</strong></td>';
    candidats.forEach(function (c) {
      tbody += '<td class="rep-heatmap__cell rep-heatmap__cell--total"><strong>' + donnees.totaux[c.id] + '</strong></td>';
    });
    var grandTotal = 0;
    candidats.forEach(function (c) { grandTotal += donnees.totaux[c.id]; });
    tbody += '<td class="rep-heatmap__cell rep-heatmap__cell--total"><strong>' + grandTotal + '</strong></td>';
    tbody += '</tr></tbody>';

    table.innerHTML = thead + tbody;
    container.appendChild(table);
  }

  // --- Mode D : Cartes individuelles (ancien mode) ---
  function rendreCartesIndividuelles(container, donnees, candidats) {
    var grille = document.createElement("div");
    grille.className = "repartition-cartes-grille";

    candidats.forEach(function (candidat) {
      var totalCandidat = donnees.totaux[candidat.id];

      var bloc = document.createElement("div");
      bloc.className = "repartition-candidat";

      var noteHTML = '';
      if (candidat.programmeComplet) {
        noteHTML = '<div class="repartition-note repartition-note--complet">Programme complet analys\u00E9</div>';
      } else {
        noteHTML = '<div class="repartition-note">Propositions extraites de sources publiques (site de campagne, tracts, presse, interviews)</div>';
      }

      var headerHTML =
        '<div class="repartition-candidat__header">' +
          '<div class="repartition-candidat__nom">' + echapper(candidat.nom) + '</div>' +
          '<div class="repartition-candidat__total">' + totalCandidat + ' proposition' + (totalCandidat > 1 ? 's' : '') + ' au total</div>' +
          noteHTML +
        '</div>';

      var barresHTML = '<div class="repartition-candidat__barres">';
      donnees.categories.forEach(function (cat) {
        var nb = cat.parCandidat[candidat.id];
        var pct = totalCandidat > 0 ? Math.round((nb / totalCandidat) * 100) : 0;
        barresHTML +=
          '<div class="repartition-barre">' +
            '<span class="repartition-barre__label" title="' + echapper(cat.nom) + '">' + echapper(cat.nom) + '</span>' +
            '<div class="repartition-barre__track">' +
              '<div class="repartition-barre__fill" style="width:' + pct + '%"></div>' +
            '</div>' +
            '<span class="repartition-barre__valeur">' + pct + '% (' + nb + ')</span>' +
          '</div>';
      });
      barresHTML += '</div>';

      bloc.innerHTML = headerHTML + barresHTML;
      grille.appendChild(bloc);
    });

    container.appendChild(grille);
  }

  function genererAvertissementVolume(candidats, donnees) {
    if (candidats.length < 2) return null;

    var complets = [];
    var partiels = [];
    candidats.forEach(function (c) {
      if (c.programmeComplet) {
        complets.push(c);
      } else {
        partiels.push(c);
      }
    });

    // Calculer l'écart de volume
    var volumes = candidats.map(function (c) { return donnees.totaux[c.id]; });
    var maxVol = Math.max.apply(null, volumes);
    var minVol = Math.min.apply(null, volumes);

    var div = document.createElement("div");
    div.className = "repartition-avertissement";

    var html = '';

    // Avertissement si mix complets/partiels
    if (complets.length > 0 && partiels.length > 0) {
      html += '<div class="repartition-avertissement__bloc repartition-avertissement__bloc--equite">';
      html += '<strong><i class="ph ph-scales"></i> \u00C9quit\u00E9 de comparaison</strong>';
      html += '<p>Tous les candidats n\u2019ont pas encore publi\u00E9 leur programme officiel. ';
      html += 'Un nombre inf\u00E9rieur de propositions ne refl\u00E8te pas n\u00E9cessairement un projet moins ambitieux.</p>';
      html += '<div class="repartition-avertissement__liste">';
      complets.forEach(function (c) {
        html += '<span class="repartition-avertissement__tag repartition-avertissement__tag--complet"><strong class="repartition-avertissement__nom">' + echapper(c.nom) + '</strong><span class="repartition-avertissement__statut repartition-avertissement__statut--complet">' + donnees.totaux[c.id] + ' propositions, programme officiel <i class="ph ph-check-circle"></i></span></span>';
      });
      partiels.forEach(function (c) {
        html += '<span class="repartition-avertissement__tag repartition-avertissement__tag--partiel"><strong class="repartition-avertissement__nom">' + echapper(c.nom) + '</strong><span class="repartition-avertissement__statut repartition-avertissement__statut--partiel">' + donnees.totaux[c.id] + ' propositions, programme \u00E0 venir <i class="ph ph-clock"></i></span></span>';
      });
      html += '</div>';
      html += '</div>';
    }

    // Date de disponibilité des programmes
    html += '<div class="repartition-avertissement__bloc repartition-avertissement__bloc--date">';
    html += '<strong><i class="ph ph-calendar-dots"></i> Calendrier</strong>';
    html += '<p>Date limite de d\u00E9p\u00F4t des candidatures : <strong>26 f\u00E9vrier 2026</strong>. ';
    html += 'Les programmes complets sont g\u00E9n\u00E9ralement publi\u00E9s entre fin f\u00E9vrier et d\u00E9but mars. ';
    html += 'Cette page est mise \u00E0 jour au fur et \u00E0 mesure des publications.</p>';
    html += '</div>';

    div.innerHTML = html;
    return div;
  }

  // === Filtres catégories ===
  function afficherFiltres() {
    filtresContainer.innerHTML = "";
    filtresContainer.appendChild(creerBoutonFiltre("Toutes", "toutes"));
    donneesElection.categories.forEach(function (cat) {
      filtresContainer.appendChild(creerBoutonFiltre(cat.nom, cat.id));
    });
    // Filtres masqués (supprimés de l'UI)
    filtresContainer.hidden = true;
  }

  function creerBoutonFiltre(label, valeur) {
    var btn = document.createElement("button");
    btn.className = "filtre-btn" + (valeur === categorieActive ? " filtre-btn--active" : "");
    btn.textContent = label;
    btn.dataset.categorie = valeur;
    btn.addEventListener("click", function () {
      categorieActive = valeur;
      var candidats = donneesElection.candidats.slice().sort(function (a, b) {
        return a.nom.localeCompare(b.nom, "fr");
      });
      filtresContainer.querySelectorAll(".filtre-btn").forEach(function (b) {
        b.classList.toggle("filtre-btn--active", b.dataset.categorie === valeur);
      });
      afficherGrille(candidats);
      mettreAJourURL();
    });
    return btn;
  }

  // === Colonnes masquées dans le tableau ===
  var tableauColonnesMasquees = {};

  function getAbrevNom(nom) {
    var parts = nom.split(" ");
    if (parts.length < 2) return nom;
    var initiales = "";
    for (var i = 0; i < parts.length - 1; i++) {
      initiales += parts[i].charAt(0).toUpperCase() + ".";
    }
    return initiales + " " + parts[parts.length - 1];
  }

  function recalculerGrilleTableau(tableau, candidats) {
    var cols = "160px";
    candidats.forEach(function(c) {
      cols += tableauColonnesMasquees[c.id] ? " 45px" : " 1fr";
    });
    tableau.style.gridTemplateColumns = cols;

    var entete = tableau.querySelector(".tableau-matriciel__entete");
    if (entete) entete.style.gridTemplateColumns = cols;

    tableau.querySelectorAll(".tableau-matriciel__ligne").forEach(function(ligne) {
      ligne.style.gridTemplateColumns = cols;
    });
  }

  function mettreAJourCompteurTableau() {
    var compteurEl = document.getElementById("tableau-compteur");
    if (!compteurEl || !donneesElection) return;
    var actifs = getCandidatsActifs();
    var nbMasques = 0;
    actifs.forEach(function(c) { if (tableauColonnesMasquees[c.id]) nbMasques++; });
    var nbVisibles = actifs.length - nbMasques;
    compteurEl.querySelector(".tableau-compteur__texte").textContent =
      nbVisibles + " candidat" + (nbVisibles > 1 ? "s" : "") + " affich\u00E9" + (nbVisibles > 1 ? "s" : "") + " sur " + actifs.length;
    var btnAll = compteurEl.querySelector(".tableau-compteur__btn-tous");
    btnAll.hidden = nbMasques === 0;
  }

  function afficherTousTableau() {
    tableauColonnesMasquees = {};
    var candidats = getCandidatsActifs();
    comparaisonContainer.querySelectorAll(".tableau-matriciel").forEach(function(tableau) {
      recalculerGrilleTableau(tableau, candidats);
      tableau.querySelectorAll("[data-col-candidat]").forEach(function(cell) {
        cell.classList.remove("tableau-col--collapsed");
      });
      tableau.querySelectorAll(".tableau-col-toggle").forEach(function(btn) {
        btn.textContent = "\u2212";
        btn.title = "Masquer";
      });
    });
    mettreAJourCompteurTableau();
  }

  // === Grille de comparaison ===
  function afficherGrille(tousLesCandidats) {
    // Réinitialiser les colonnes masquées
    tableauColonnesMasquees = {};

    // Conserver le H2 SEO et la section filtres, supprimer le reste
    var titreH2 = document.getElementById("comparaison-titre");
    var filtresSec = selectionCandidatsSection;
    // Détacher les éléments à conserver AVANT de vider le container
    if (titreH2 && titreH2.parentNode) titreH2.parentNode.removeChild(titreH2);
    if (filtresSec && filtresSec.parentNode) filtresSec.parentNode.removeChild(filtresSec);
    // Vider le reste
    while (comparaisonContainer.firstChild) {
      comparaisonContainer.removeChild(comparaisonContainer.firstChild);
    }
    if (titreH2) {
      var villeNom = donneesElection ? donneesElection.ville : "";
      titreH2.textContent = "Propositions des candidats \u00E0 " + villeNom + " par th\u00E8me";
      comparaisonContainer.appendChild(titreH2);
    }

    // Guide de lecture (affiché une seule fois, masquable)
    var guideDejaVu = localStorage.getItem("guide-lecture-vu");
    if (!guideDejaVu) {
      var guide = document.createElement("div");
      guide.className = "guide-lecture";
      guide.innerHTML = '<div class="guide-lecture__contenu">' +
        '<span class="guide-lecture__icone"><i class="ph ph-book-open-text"></i></span>' +
        '<div class="guide-lecture__texte">' +
        '<div class="guide-lecture__titre-bloc">Comment lire cette section ?</div>' +
        '<p>Chaque th\u00E8me regroupe les propositions de tous les candidats c\u00F4te \u00E0 c\u00F4te. ' +
        'Utilisez les <b>points de navigation</b> sur la droite (sur grand \u00E9cran) pour naviguer directement vers un th\u00E8me. ' +
        'Les cases grises indiquent qu\u2019un candidat ne s\u2019est pas encore prononc\u00E9 sur le sujet.</p>' +
        '</div>' +
        '<button class="guide-lecture__fermer" title="Fermer">\u00D7</button>' +
        '</div>';
      guide.querySelector(".guide-lecture__fermer").addEventListener("click", function () {
        guide.remove();
        localStorage.setItem("guide-lecture-vu", "1");
      });
      comparaisonContainer.appendChild(guide);
    }

    var candidats = getCandidatsActifs();
    var nbTotal = donneesElection ? donneesElection.candidats.length : candidats.length;

    // Pré-replier les colonnes des candidats avec 0 propositions
    candidats.forEach(function (c) {
      var total = 0;
      donneesElection.categories.forEach(function (cat) {
        if (cat.sousThemes) {
          cat.sousThemes.forEach(function (st) {
            if (st.propositions[c.id] && st.propositions[c.id].texte) total++;
          });
        }
      });
      if (total === 0) {
        tableauColonnesMasquees[c.id] = true;
      }
    });

    // Déplacer les filtres candidats ici (desktop), juste sous le titre
    if (filtresSec) {
      filtresSec.style.order = "";
      comparaisonContainer.appendChild(filtresSec);
    }

    // Compteur candidats affichés (tableau desktop +/-)
    var compteur = document.createElement("div");
    compteur.className = "tableau-compteur";
    compteur.id = "tableau-compteur";
    compteur.innerHTML = '<span class="tableau-compteur__texte">' + candidats.length + ' candidat' + (candidats.length > 1 ? 's' : '') + ' affich\u00E9' + (candidats.length > 1 ? 's' : '') + ' sur ' + candidats.length + '</span>' +
      '<button class="tableau-compteur__btn-tous" hidden onclick="">Afficher tous</button>';
    comparaisonContainer.appendChild(compteur);

    compteur.querySelector(".tableau-compteur__btn-tous").addEventListener("click", afficherTousTableau);

    var categoriesFiltrees = donneesElection.categories.filter(function (cat) {
      return categorieActive === "toutes" || cat.id === categorieActive;
    });

    // Trier : catégories avec propositions des candidats actifs en premier
    categoriesFiltrees.sort(function(a, b) {
      var nbA = 0, nbB = 0;
      if (a.sousThemes) {
        a.sousThemes.forEach(function(st) {
          candidats.forEach(function(c) { if (st.propositions[c.id]) nbA++; });
        });
      }
      if (b.sousThemes) {
        b.sousThemes.forEach(function(st) {
          candidats.forEach(function(c) { if (st.propositions[c.id]) nbB++; });
        });
      }
      // Celles avec propositions d'abord, puis conserver l'ordre consensuel
      if (nbA > 0 && nbB === 0) return -1;
      if (nbA === 0 && nbB > 0) return 1;
      return 0;
    });

    categoriesFiltrees.forEach(function (categorie, index) {
      var section;
      var estPremiere = index === 0;
      // Détecter le format : sous-thèmes ou propositions plates
      if (categorie.sousThemes) {
        section = creerSectionAvecSousThemes(categorie, candidats, estPremiere);
      } else {
        section = creerSectionCategorie(categorie, candidats, estPremiere);
      }
      if (section) {
        comparaisonContainer.appendChild(section);
      }
    });

    if (comparaisonContainer.children.length === 0 && rechercheTexte) {
      var msg = document.createElement("p");
      msg.className = "etat-vide";
      msg.textContent = "Aucune proposition ne correspond \u00E0 \u00AB " + rechercheTexte + " \u00BB.";
      comparaisonContainer.appendChild(msg);
    }

    mettreAJourCompteurTableau();
  }

  // Nouvelle fonction pour les catégories avec sous-thèmes (format matriciel)
  function creerSectionAvecSousThemes(categorie, candidats, estPremiere) {
    // Compter le nombre total de propositions
    var totalPropositions = 0;
    categorie.sousThemes.forEach(function(st) {
      candidats.forEach(function(cand) {
        if (st.propositions[cand.id]) {
          totalPropositions++;
        }
      });
    });

    var div = document.createElement("div");
    div.className = "categorie categorie--matricielle" + (estPremiere ? " categorie--ouverte" : "");
    div.dataset.categorieId = categorie.id;

    var header = document.createElement("div");
    header.className = "categorie__header";
    header.style.position = "relative";

    // Titre + count
    var titreDiv = document.createElement("div");
    titreDiv.innerHTML =
      '<span class="categorie__nom">' +
        '<span class="categorie__icone">' + getIconeCategorie(categorie.id) + '</span>' +
        echapper(categorie.nom) +
      '</span>';
    header.appendChild(titreDiv);

    // Mini-barres de répartition par candidat
    var maxThemeBar = 0;
    candidats.forEach(function(c) {
      var nb = compterPropositionsCandidat(categorie, c.id);
      if (nb > maxThemeBar) maxThemeBar = nb;
    });
    var barsContainer = document.createElement("div");
    barsContainer.className = "categorie__header-bars";
    candidats.forEach(function(c, idx) {
      var nb = compterPropositionsCandidat(categorie, c.id);
      var pct = maxThemeBar > 0 ? Math.round(nb / maxThemeBar * 100) : 0;
      var couleur = getCouleurParti(c, idx);
      var line = document.createElement("div");
      line.className = "categorie__header-bar-line";
      var nameSpan = document.createElement("span");
      nameSpan.className = "categorie__header-bar-name";
      nameSpan.style.color = couleur;
      var parties = c.nom.split(" ");
      var nomCourt = parties.length > 1
        ? parties.slice(0, -1).join(" ") + " " + parties[parties.length - 1].charAt(0) + "."
        : c.nom;
      nameSpan.textContent = nomCourt;
      var track = document.createElement("div");
      track.className = "categorie__header-bar-track";
      var fill = document.createElement("div");
      fill.className = "categorie__header-bar-fill";
      fill.style.width = pct + "%";
      fill.style.background = couleur;
      track.appendChild(fill);
      var nbSpan = document.createElement("span");
      nbSpan.className = "categorie__header-bar-nb";
      nbSpan.textContent = nb;
      line.appendChild(nameSpan);
      line.appendChild(track);
      line.appendChild(nbSpan);
      barsContainer.appendChild(line);
    });
    header.appendChild(barsContainer);

    // Toggle ▼
    var toggleSpan = document.createElement("span");
    toggleSpan.className = "categorie__toggle";
    toggleSpan.textContent = "\u25BC";
    header.appendChild(toggleSpan);

    header.addEventListener("click", function () {
      div.classList.toggle("categorie--ouverte");
    });

    div.appendChild(header);

    var contenu = document.createElement("div");
    contenu.className = "categorie__contenu";

    // Créer le tableau matriciel
    var tableau = document.createElement("div");
    tableau.className = "tableau-matriciel tableau-matriciel--mobile-accordion";
    tableau.style.setProperty("--nb-candidats", candidats.length);

    // En-tête avec les noms des candidats
    var entete = document.createElement("div");
    entete.className = "tableau-matriciel__entete";

    var celleSousTheme = document.createElement("div");
    celleSousTheme.className = "tableau-matriciel__cell tableau-matriciel__cell--header";
    celleSousTheme.textContent = "Sous-thème";
    entete.appendChild(celleSousTheme);

    candidats.forEach(function(candidat, idx) {
      var celleCand = document.createElement("div");
      celleCand.className = "tableau-matriciel__cell tableau-matriciel__cell--candidat";
      celleCand.setAttribute("data-col-candidat", candidat.id);
      var couleurParti = getCouleurParti(candidat, idx);
      celleCand.style.borderTop = "3px solid " + couleurParti;

      var estMasque = !!tableauColonnesMasquees[candidat.id];

      var toggleBtn = document.createElement("button");
      toggleBtn.className = "tableau-col-toggle";
      toggleBtn.style.borderColor = couleurParti;
      toggleBtn.textContent = estMasque ? "+" : "\u2212";
      toggleBtn.title = estMasque ? "Afficher " + candidat.nom : "Masquer " + candidat.nom;
      (function(cId, cNom, cCouleur, btn, cell, tbl) {
        btn.addEventListener("click", function(e) {
          e.stopPropagation();
          tableauColonnesMasquees[cId] = !tableauColonnesMasquees[cId];
          var isMasque = tableauColonnesMasquees[cId];
          btn.textContent = isMasque ? "+" : "\u2212";
          btn.title = isMasque ? "Afficher " + cNom : "Masquer " + cNom;

          // MAJ toutes les cellules de ce candidat dans ce tableau
          tbl.querySelectorAll('[data-col-candidat="' + cId + '"]').forEach(function(c) {
            c.classList.toggle("tableau-col--collapsed", isMasque);
          });

          // MAJ grille dans tous les tableaux
          comparaisonContainer.querySelectorAll(".tableau-matriciel").forEach(function(t) {
            recalculerGrilleTableau(t, candidats);
            t.querySelectorAll('[data-col-candidat="' + cId + '"]').forEach(function(c) {
              c.classList.toggle("tableau-col--collapsed", isMasque);
            });
            var togBtn = t.querySelector('.tableau-col-toggle[data-toggle-id="' + cId + '"]');
            if (togBtn) {
              togBtn.textContent = isMasque ? "+" : "\u2212";
              togBtn.title = isMasque ? "Afficher " + cNom : "Masquer " + cNom;
            }
          });

          mettreAJourCompteurTableau();
        });
      })(candidat.id, candidat.nom, couleurParti, toggleBtn, celleCand, tableau);
      toggleBtn.setAttribute("data-toggle-id", candidat.id);

      var badgeHTML = '';
      if (candidat.programmeComplet) {
        badgeHTML = '<span class="badge badge--complet mini">Officiel</span>';
      } else {
        badgeHTML = '<span class="badge badge--partiel mini">\u00C0 venir</span>';
      }

      var couv = calculerCouverture(categorie, candidat.id);
      var couvertureHTML = '<div class="couverture-bar">' +
        '<div class="couverture-bar__label">' + couv.couverts + '/' + couv.total + ' thèmes abordés</div>' +
        '<div class="couverture-bar__track">' +
          '<div class="couverture-bar__fill" style="width:' + couv.pct + '%;background:' + couleurParti + '"></div>' +
        '</div>' +
        '</div>';

      var fullContent = document.createElement("span");
      fullContent.className = "tableau-col__content-full";
      fullContent.innerHTML = '<strong>' + echapper(candidat.nom) + '</strong><span class="candidat-parti-label">' + echapper(candidat.liste) + '</span> ' + badgeHTML + couvertureHTML;

      var verticalName = document.createElement("span");
      verticalName.className = "tableau-col__nom-vertical";
      verticalName.textContent = getAbrevNom(candidat.nom);

      celleCand.appendChild(fullContent);
      celleCand.appendChild(verticalName);
      celleCand.appendChild(toggleBtn);

      if (estMasque) {
        celleCand.classList.add("tableau-col--collapsed");
      }

      entete.appendChild(celleCand);
    });
    tableau.appendChild(entete);

    // Lignes pour chaque sous-thème
    categorie.sousThemes.forEach(function(sousTheme) {
      var ligne = document.createElement("div");
      ligne.className = "tableau-matriciel__ligne";

      // Colonne du sous-thème
      var celleST = document.createElement("div");
      celleST.className = "tableau-matriciel__cell tableau-matriciel__cell--sous-theme";
      celleST.innerHTML = '<strong>' + echapper(sousTheme.nom) + '</strong>';
      ligne.appendChild(celleST);

      // Gestion de l'accordéon mobile sur le sous-thème
      celleST.addEventListener("click", function() {
        if (tableau.classList.contains("tableau-matriciel--mobile-accordion")) {
          ligne.classList.toggle("tableau-matriciel__ligne--collapsed");
        }
      });

      // Colonnes pour chaque candidat
      candidats.forEach(function(candidat, idxC) {
        var couleurCand = getCouleurParti(candidat, idxC);
        var celleProps = document.createElement("div");
        celleProps.className = "tableau-matriciel__cell tableau-matriciel__cell--proposition";
        celleProps.dataset.candidatId = candidat.id;
        celleProps.dataset.candidatNom = candidat.nom;
        celleProps.setAttribute("data-col-candidat", candidat.id);
        celleProps.style.setProperty("--couleur-candidat", couleurCand);
        if (tableauColonnesMasquees[candidat.id]) {
          celleProps.classList.add("tableau-col--collapsed");
        }

        var prop = sousTheme.propositions[candidat.id];

        if (prop && prop.texte) {
          var texteDiv = document.createElement("div");
          texteDiv.className = "proposition__texte";
          texteDiv.textContent = prop.texte;

          var sourceDiv = document.createElement("div");
          sourceDiv.className = "proposition__source";
          sourceDiv.innerHTML = '<a href="' + echapper(prop.sourceUrl || '#') + '" target="_blank" rel="noopener">' +
            echapper(prop.source) + '</a>';

          var voirPlusBtn = document.createElement("button");
          voirPlusBtn.className = "voir-plus-btn";
          voirPlusBtn.textContent = "Voir plus";
          voirPlusBtn.hidden = true;

          voirPlusBtn.addEventListener("click", function(e) {
            e.stopPropagation();
            if (texteDiv.classList.contains("proposition__texte--expanded")) {
              texteDiv.classList.remove("proposition__texte--expanded");
              voirPlusBtn.textContent = "Voir plus";
            } else {
              texteDiv.classList.add("proposition__texte--expanded");
              voirPlusBtn.textContent = "Voir moins";
            }
          });

          celleProps.appendChild(texteDiv);
          celleProps.appendChild(voirPlusBtn);
          celleProps.appendChild(sourceDiv);
          celleProps.classList.add('tableau-matriciel__cell--remplie');

          // Show "voir plus" only if text is actually truncated
          (function(td, btn) {
            requestAnimationFrame(function() {
              if (td.scrollHeight > td.clientHeight + 2) {
                btn.hidden = false;
              }
            });
          })(texteDiv, voirPlusBtn);
        } else {
          celleProps.innerHTML = '<div class="proposition__absence"><span class="absence__icon"></span><span class="absence__label">Non renseign\u00E9</span></div>';
          celleProps.classList.add('tableau-matriciel__cell--vide');
        }

        ligne.appendChild(celleProps);
      });

      tableau.appendChild(ligne);
    });

    // Initialiser toutes les lignes comme repliées par défaut (mode accordéon)
    var lignesMobile = tableau.querySelectorAll(".tableau-matriciel__ligne");
    lignesMobile.forEach(function(ligne, idx) {
      if (idx > 0) {
        ligne.classList.add("tableau-matriciel__ligne--collapsed");
      }
    });

    // Vue 2 : ajouter les barres horizontales au-dessus du tableau
    if (vuePageActuelle === "vue2") {
      var barresDiv = document.createElement("div");
      barresDiv.className = "categorie__barres-integrees";
      var maxTheme = 0;
      candidats.forEach(function(c) {
        var nb = compterPropositionsCandidat(categorie, c.id);
        if (nb > maxTheme) maxTheme = nb;
      });
      var barresHTML = '<div class="rep-barres__conteneur">';
      candidats.forEach(function(c, idx) {
        var nb = compterPropositionsCandidat(categorie, c.id);
        var pct = maxTheme > 0 ? Math.round(nb / maxTheme * 100) : 0;
        var couleur = getCouleurParti(c, idx);
        var initiale = getInitialeParti(c);
        if (nb > 0) {
          barresHTML += '<div class="rep-barres__ligne">' +
            '<span class="rep-barres__nom" style="color:' + couleur + '">' + echapper(c.nom) + '</span>' +
            '<div class="rep-barres__bar-track">' +
              '<div class="rep-barres__fill" style="width:' + pct + '%;background:' + couleur + '" title="' + echapper(c.nom) + ' : ' + nb + '"><span class="rep-barres__initiale">' + initiale + '</span></div>' +
            '</div>' +
            '<span class="rep-barres__nb">' + nb + '</span>' +
          '</div>';
        } else {
          barresHTML += '<div class="rep-barres__ligne rep-barres__ligne--vide">' +
            '<span class="rep-barres__nom" style="color:' + couleur + ';opacity:0.5">' + echapper(c.nom) + '</span>' +
            '<div class="rep-barres__bar-track">' +
              '<div class="rep-barres__fill rep-barres__fill--vide" style="width:100%" title="' + echapper(c.nom) + ' : aucune proposition">\u2014</div>' +
            '</div>' +
            '<span class="rep-barres__nb rep-barres__nb--vide">0</span>' +
          '</div>';
        }
      });
      barresHTML += '</div>';
      barresDiv.innerHTML = barresHTML;
      contenu.appendChild(barresDiv);
    }

    contenu.appendChild(tableau);
    div.appendChild(contenu);

    return div;
  }

  function creerSectionCategorie(categorie, candidats, estPremiere) {
    var propositionsFiltrees = categorie.propositions;
    if (rechercheTexte) {
      var termeMin = rechercheTexte.toLowerCase();
      propositionsFiltrees = propositionsFiltrees.filter(function (p) {
        return p.texte.toLowerCase().indexOf(termeMin) !== -1;
      });
      if (propositionsFiltrees.length === 0) return null;
    }

    var div = document.createElement("div");
    div.className = "categorie" + (estPremiere ? " categorie--ouverte" : "");

    var header = document.createElement("div");
    header.className = "categorie__header";
    header.innerHTML =
      '<div>' +
        '<span class="categorie__nom">' +
          '<span class="categorie__icone">' + getIconeCategorie(categorie.id) + '</span>' +
          echapper(categorie.nom) +
        '</span> ' +
        '<span class="categorie__count">' + propositionsFiltrees.length + ' proposition' +
        (propositionsFiltrees.length > 1 ? 's' : '') + '</span>' +
      '</div>' +
      '<span class="categorie__toggle">\u25BC</span>';

    header.addEventListener("click", function () {
      div.classList.toggle("categorie--ouverte");
    });
    div.appendChild(header);

    var contenu = document.createElement("div");
    contenu.className = "categorie__contenu";

    var grille = document.createElement("div");
    grille.className = "grille-candidats";
    grille.style.setProperty("--nb-candidats", candidats.length);

    candidats.forEach(function (candidat) {
      var colonne = document.createElement("div");
      colonne.className = "colonne-candidat";

      var headerCand = document.createElement("div");
      headerCand.className = "candidat-header";

      var badgeHTML = '';
      if (candidat.programmeComplet) {
        badgeHTML = '<span class="badge badge--complet">Programme officiel</span>';
      } else {
        badgeHTML = '<span class="badge badge--partiel">Sources publiques</span>';
      }

      var actionsHTML = '';
      if (candidat.programmeComplet && candidat.programmePdfPath) {
        actionsHTML = '<div class="candidat-header__actions">' +
          '<a href="' + echapper(candidat.programmePdfPath) + '" target="_blank" class="btn-pdf">👁️ Voir</a>' +
          '<a href="' + echapper(candidat.programmePdfPath) + '" download class="btn-pdf btn-pdf--download">⬇️ T\u00E9l\u00E9charger</a>' +
        '</div>';
      } else if (candidat.programmeComplet && candidat.programmeUrl && candidat.programmeUrl !== '#') {
        actionsHTML = '<div class="candidat-header__actions">' +
          '<a href="' + echapper(candidat.programmeUrl) + '" target="_blank" class="btn-pdf">🌐 Voir le programme</a>' +
        '</div>';
      }

      headerCand.innerHTML =
        '<div class="candidat-header__nom">' + echapper(candidat.nom) + '</div>' +
        '<div class="candidat-header__liste" style="color:' + getCouleurParti(candidat, 0) + '">' + echapper(candidat.liste) + '</div>' +
        '<div class="candidat-header__badges">' + badgeHTML + '</div>' +
        actionsHTML;
      colonne.appendChild(headerCand);

      var propsCand = propositionsFiltrees.filter(function (p) {
        return p.candidatId === candidat.id;
      });

      if (propsCand.length === 0) {
        var absenceDiv = document.createElement("div");
        absenceDiv.className = "proposition proposition--absence";
        absenceDiv.innerHTML =
          '<p class="proposition__texte">Aucune proposition identifi\u00E9e sur ce sujet</p>';
        colonne.appendChild(absenceDiv);
      } else {
        propsCand.forEach(function (prop) {
          var propDiv = document.createElement("div");
          propDiv.className = "proposition";

          var texteAffiche = echapper(prop.texte);
          if (rechercheTexte) {
            texteAffiche = surlignerPropositions(texteAffiche, rechercheTexte);
          }

          propDiv.innerHTML =
            '<p class="proposition__texte">' + texteAffiche + '</p>' +
            '<p class="proposition__source">' + echapper(prop.source) +
            (prop.sourceUrl && prop.sourceUrl !== "#"
              ? ' &mdash; <a href="' + echapper(prop.sourceUrl) + '" target="_blank" rel="noopener">Voir le document</a>'
              : '') +
            '</p>';
          colonne.appendChild(propDiv);
        });
      }

      grille.appendChild(colonne);
    });

    contenu.appendChild(grille);
    div.appendChild(contenu);
    return div;
  }

  // === Utilitaires ===
  function echapper(str) {
    var el = document.createElement("div");
    el.appendChild(document.createTextNode(str));
    return el.innerHTML;
  }

  var PICTO_STYLES = {
    standard: {
      "transports": "\uD83D\uDE87", "environnement": "\uD83C\uDF31", "education": "\uD83C\uDF93",
      "securite": "\uD83D\uDEE1\uFE0F", "economie": "\uD83D\uDCBC", "logement": "\uD83C\uDFE0",
      "sante": "\u2695\uFE0F", "culture": "\uD83C\uDFAD", "sport": "\u26BD",
      "urbanisme": "\uD83C\uDFD7\uFE0F", "democratie": "\uD83D\uDDF3\uFE0F", "solidarite": "\uD83E\uDD1D",
      fallback: "\uD83D\uDCCB"
    },
    moderne: {
      "transports": "\uD83D\uDE8C", "environnement": "\uD83C\uDF0D", "education": "\uD83D\uDCDA",
      "securite": "\uD83D\uDD12", "economie": "\uD83D\uDCB0", "logement": "\uD83C\uDFD8\uFE0F",
      "sante": "\uD83C\uDFE5", "culture": "\uD83C\uDFA8", "sport": "\uD83C\uDFC3",
      "urbanisme": "\uD83C\uDF06", "democratie": "\uD83C\uDFDB\uFE0F", "solidarite": "\u2764\uFE0F",
      fallback: "\uD83D\uDCC4"
    },
    sobre: {
      "transports": "\uD83D\uDE8A", "environnement": "\u267B\uFE0F", "education": "\uD83D\uDCD6",
      "securite": "\uD83D\uDD10", "economie": "\uD83D\uDCCA", "logement": "\uD83D\uDD11",
      "sante": "\uD83D\uDC8A", "culture": "\uD83C\uDFB5", "sport": "\uD83C\uDFC5",
      "urbanisme": "\uD83D\uDCD0", "democratie": "\u2696\uFE0F", "solidarite": "\uD83E\uDD32",
      fallback: "\u2022"
    },
    nature: {
      "transports": "\uD83D\uDEB2", "environnement": "\uD83C\uDF33", "education": "\u270F\uFE0F",
      "securite": "\uD83D\uDD25", "economie": "\uD83C\uDFE6", "logement": "\uD83D\uDECF\uFE0F",
      "sante": "\uD83C\uDF3F", "culture": "\uD83D\uDCF7", "sport": "\uD83C\uDFAF",
      "urbanisme": "\uD83C\uDFD9\uFE0F", "democratie": "\uD83D\uDCDC", "solidarite": "\uD83D\uDC9D",
      fallback: "\uD83C\uDF3E"
    },
    "fa-solid": {
      "transports": '<i class="fa-solid fa-train-subway"></i>', "environnement": '<i class="fa-solid fa-leaf"></i>',
      "education": '<i class="fa-solid fa-graduation-cap"></i>', "securite": '<i class="fa-solid fa-shield-halved"></i>',
      "economie": '<i class="fa-solid fa-briefcase"></i>', "logement": '<i class="fa-solid fa-house"></i>',
      "sante": '<i class="fa-solid fa-heart-pulse"></i>', "culture": '<i class="fa-solid fa-masks-theater"></i>',
      "sport": '<i class="fa-solid fa-futbol"></i>', "urbanisme": '<i class="fa-solid fa-city"></i>',
      "democratie": '<i class="fa-solid fa-landmark"></i>', "solidarite": '<i class="fa-solid fa-handshake"></i>',
      fallback: '<i class="fa-solid fa-list"></i>'
    },
    bootstrap: {
      "transports": '<i class="bi bi-bus-front"></i>', "environnement": '<i class="bi bi-tree"></i>',
      "education": '<i class="bi bi-mortarboard"></i>', "securite": '<i class="bi bi-shield-check"></i>',
      "economie": '<i class="bi bi-briefcase"></i>', "logement": '<i class="bi bi-house"></i>',
      "sante": '<i class="bi bi-heart-pulse"></i>', "culture": '<i class="bi bi-palette"></i>',
      "sport": '<i class="bi bi-trophy"></i>', "urbanisme": '<i class="bi bi-buildings"></i>',
      "democratie": '<i class="bi bi-bank"></i>', "solidarite": '<i class="bi bi-people"></i>',
      fallback: '<i class="bi bi-list"></i>'
    },
    material: {
      "transports": '<span class="material-symbols-outlined">directions_bus</span>',
      "environnement": '<span class="material-symbols-outlined">eco</span>',
      "education": '<span class="material-symbols-outlined">school</span>',
      "securite": '<span class="material-symbols-outlined">shield</span>',
      "economie": '<span class="material-symbols-outlined">work</span>',
      "logement": '<span class="material-symbols-outlined">home</span>',
      "sante": '<span class="material-symbols-outlined">health_and_safety</span>',
      "culture": '<span class="material-symbols-outlined">palette</span>',
      "sport": '<span class="material-symbols-outlined">sports_soccer</span>',
      "urbanisme": '<span class="material-symbols-outlined">apartment</span>',
      "democratie": '<span class="material-symbols-outlined">account_balance</span>',
      "solidarite": '<span class="material-symbols-outlined">handshake</span>',
      fallback: '<span class="material-symbols-outlined">list</span>'
    },
    phosphor: {
      "transports": '<i class="ph ph-bus"></i>', "environnement": '<i class="ph ph-leaf"></i>',
      "education": '<i class="ph ph-graduation-cap"></i>', "securite": '<i class="ph ph-shield-check"></i>',
      "economie": '<i class="ph ph-briefcase"></i>', "logement": '<i class="ph ph-house"></i>',
      "sante": '<i class="ph ph-heartbeat"></i>', "culture": '<i class="ph ph-palette"></i>',
      "sport": '<i class="ph ph-soccer-ball"></i>', "urbanisme": '<i class="ph ph-buildings"></i>',
      "democratie": '<i class="ph ph-bank"></i>', "solidarite": '<i class="ph ph-handshake"></i>',
      fallback: '<i class="ph ph-list"></i>'
    },
    "phosphor-fill": {
      "transports": '<i class="ph-fill ph-bus"></i>', "environnement": '<i class="ph-fill ph-leaf"></i>',
      "education": '<i class="ph-fill ph-graduation-cap"></i>', "securite": '<i class="ph-fill ph-shield-check"></i>',
      "economie": '<i class="ph-fill ph-briefcase"></i>', "logement": '<i class="ph-fill ph-house"></i>',
      "sante": '<i class="ph-fill ph-heartbeat"></i>', "culture": '<i class="ph-fill ph-palette"></i>',
      "sport": '<i class="ph-fill ph-soccer-ball"></i>', "urbanisme": '<i class="ph-fill ph-buildings"></i>',
      "democratie": '<i class="ph-fill ph-bank"></i>', "solidarite": '<i class="ph-fill ph-handshake"></i>',
      fallback: '<i class="ph-fill ph-list"></i>'
    },
    "phosphor-duotone": {
      "transports": '<i class="ph-duotone ph-bus"></i>', "environnement": '<i class="ph-duotone ph-leaf"></i>',
      "education": '<i class="ph-duotone ph-graduation-cap"></i>', "securite": '<i class="ph-duotone ph-shield-check"></i>',
      "economie": '<i class="ph-duotone ph-briefcase"></i>', "logement": '<i class="ph-duotone ph-house"></i>',
      "sante": '<i class="ph-duotone ph-heartbeat"></i>', "culture": '<i class="ph-duotone ph-palette"></i>',
      "sport": '<i class="ph-duotone ph-soccer-ball"></i>', "urbanisme": '<i class="ph-duotone ph-buildings"></i>',
      "democratie": '<i class="ph-duotone ph-bank"></i>', "solidarite": '<i class="ph-duotone ph-handshake"></i>',
      fallback: '<i class="ph-duotone ph-list"></i>'
    },
    tabler: {
      "transports": '<i class="ti ti-bus"></i>', "environnement": '<i class="ti ti-leaf"></i>',
      "education": '<i class="ti ti-school"></i>', "securite": '<i class="ti ti-shield-check"></i>',
      "economie": '<i class="ti ti-briefcase"></i>', "logement": '<i class="ti ti-home-2"></i>',
      "sante": '<i class="ti ti-heartbeat"></i>', "culture": '<i class="ti ti-palette"></i>',
      "sport": '<i class="ti ti-ball-football"></i>', "urbanisme": '<i class="ti ti-building"></i>',
      "democratie": '<i class="ti ti-building-bank"></i>', "solidarite": '<i class="ti ti-heart-handshake"></i>',
      fallback: '<i class="ti ti-list"></i>'
    },
    aucun: {
      "transports": "", "environnement": "", "education": "",
      "securite": "", "economie": "", "logement": "",
      "sante": "", "culture": "", "sport": "",
      "urbanisme": "", "democratie": "", "solidarite": "",
      fallback: ""
    }
  };
  var pictoStyleActuel = "phosphor";

  // --- Chargement CDN à la demande ---
  var ICON_CDNS = {
    "fa-solid": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
    "bootstrap": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
    "material": "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined",
    "phosphor": "https://cdn.jsdelivr.net/npm/@phosphor-icons/web/src/regular/style.css",
    "phosphor-fill": "https://cdn.jsdelivr.net/npm/@phosphor-icons/web/src/fill/style.css",
    "phosphor-duotone": "https://cdn.jsdelivr.net/npm/@phosphor-icons/web/src/duotone/style.css",
    "tabler": "https://cdn.jsdelivr.net/npm/@tabler/icons-webfont/dist/tabler-icons.min.css"
  };
  var cdnsCharges = {};

  function chargerIconCDN(styleId, callback) {
    var url = ICON_CDNS[styleId];
    if (!url || cdnsCharges[styleId]) {
      if (callback) callback();
      return;
    }
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = url;
    link.crossOrigin = "anonymous";
    link.onload = function() {
      cdnsCharges[styleId] = true;
      if (callback) callback();
    };
    link.onerror = function() {
      if (callback) callback();
    };
    document.head.appendChild(link);
  }

  function getIconeCategorie(categorieId) {
    var style = PICTO_STYLES[pictoStyleActuel] || PICTO_STYLES.standard;
    return style[categorieId] !== undefined ? style[categorieId] : style.fallback;
  }

  function surlignerPropositions(texte, terme) {
    if (!terme) return texte;
    var regex = new RegExp("(" + termeRegexSafe(terme) + ")", "gi");
    return texte.replace(regex, "<mark>$1</mark>");
  }

  function termeRegexSafe(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  // Badge ville : plus de clic (texte normal dans le H1)

  // === Événements ===
  villeSearchInput.addEventListener("input", function () {
    var terme = villeSearchInput.value.trim();
    if (terme.length === 0) {
      masquerSuggestions();
      villeSelectionnee = null;
      donneesElection = null;
      electionInfo.hidden = true;
      var toolbarEl = document.getElementById("toolbar");
      if (toolbarEl) toolbarEl.hidden = true;
      repartitionSection.hidden = true;
      filtresContainer.hidden = true;
      comparaisonContainer.hidden = true;
      aucunCandidatSection.hidden = true;
      selectionCandidatsSection.hidden = true;
      alertesSection.hidden = true;
      statistiquesSection.hidden = true;
      etatVide.hidden = false;
      rechercheInput.disabled = true;
      if (mobileFilterBtn) mobileFilterBtn.hidden = true;
      rechercheInput.value = "";
      arreterCountdown();
      mettreAJourHeroEtat(null);
      mettreAJourFilAriane(null);
      return;
    }

    var villesTrouvees = rechercherVilles(terme);
    afficherSuggestions(villesTrouvees, terme);

    // Aussi chercher des candidats et les afficher en dessous des villes
    if (terme.length >= 2) {
      var candidatsTrouves = rechercherCandidats(terme);
      if (candidatsTrouves.length > 0) {
        candidatsTrouves.slice(0, 5).forEach(function(r) {
          var div = document.createElement("div");
          div.className = "ville-suggestion ville-suggestion--candidat";
          div.innerHTML =
            '<span class="ville-suggestion__nom"><i class="ph ph-user"></i> ' + surligner(echapper(r.candidatNom), terme) + '</span>' +
            '<span class="ville-suggestion__code">' + echapper(r.villeNom) + ' \u2014 ' + echapper(r.liste) + '</span>';
          div.addEventListener("click", function() {
            selectionnerCandidatRecherche(r);
          });
          villeSuggestionsContainer.appendChild(div);
        });
        villeSuggestionsContainer.hidden = false;
      }
    }
  });

  villeSearchInput.addEventListener("keydown", function (e) {
    if (villeSuggestionsContainer.hidden) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      naviguerSuggestions(1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      naviguerSuggestions(-1);
    } else if (e.key === "Enter") {
      e.preventDefault();
      validerSuggestion();
    } else if (e.key === "Escape") {
      masquerSuggestions();
    }
  });

  villeSearchInput.addEventListener("focus", function () {
    var terme = villeSearchInput.value.trim();
    if (terme.length > 0 && !villeSelectionnee) {
      var villesTrouvees = rechercherVilles(terme);
      afficherSuggestions(villesTrouvees, terme);
    }
  });

  // === Événements recherche candidat ===
  candidatSearchInput.addEventListener("input", function () {
    var terme = candidatSearchInput.value.trim();
    if (terme.length < 2) {
      masquerSuggestionsCandidats();
      return;
    }
    var resultats = rechercherCandidats(terme);
    afficherSuggestionsCandidats(resultats, terme);
  });

  candidatSearchInput.addEventListener("keydown", function (e) {
    if (candidatSuggestionsContainer.hidden) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      naviguerSuggestionsCandidats(1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      naviguerSuggestionsCandidats(-1);
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (suggestionCandidatActive !== -1) {
        var suggestions = candidatSuggestionsContainer.querySelectorAll(".candidat-suggestion");
        if (suggestions[suggestionCandidatActive]) {
          suggestions[suggestionCandidatActive].click();
        }
      }
    } else if (e.key === "Escape") {
      masquerSuggestionsCandidats();
    }
  });

  document.addEventListener("click", function (e) {
    if (!villeSearchInput.contains(e.target) && !villeSuggestionsContainer.contains(e.target)) {
      masquerSuggestions();
    }
    if (!candidatSearchInput.contains(e.target) && !candidatSuggestionsContainer.contains(e.target)) {
      masquerSuggestionsCandidats();
    }
  });

  var rechercheTimeout = null;
  rechercheInput.addEventListener("input", function () {
    clearTimeout(rechercheTimeout);
    rechercheTimeout = setTimeout(function () {
      rechercheTexte = rechercheInput.value.trim();
      if (donneesElection) {
        var candidats = donneesElection.candidats.slice().sort(function (a, b) {
          return a.nom.localeCompare(b.nom, "fr");
        });
        afficherGrille(candidats);
      }
    }, 250);
  });

  // === Bouton Rechercher (search-float) ===
  var searchFloatBtn = document.getElementById("search-float-btn");
  if (searchFloatBtn) {
    searchFloatBtn.addEventListener("click", function() {
      var terme = villeSearchInput.value.trim();
      if (!terme) return;
      // Sélectionner la première suggestion visible
      var premiereSuggestion = villeSuggestionsContainer.querySelector(".ville-suggestion");
      if (premiereSuggestion) {
        premiereSuggestion.click();
      } else {
        // Tenter une recherche directe
        var villesTrouvees = rechercherVilles(terme);
        if (villesTrouvees.length > 0) {
          selectionnerVille(villesTrouvees[0]);
        } else {
          var candidatsTrouves = rechercherCandidats(terme);
          if (candidatsTrouves.length > 0) {
            selectionnerCandidatRecherche(candidatsTrouves[0]);
          }
        }
      }
    });
  }

  // === Événements partage ===
  btnPartager.addEventListener("click", function(e) {
    e.stopPropagation();
    copierLien();
  });

  // Gestionnaires pour les boutons de réseaux sociaux (toolbar)
  document.addEventListener("click", function(e) {
    if (e.target.closest(".btn-reseau--facebook")) {
      partagerSurReseau("facebook");
    } else if (e.target.closest(".btn-reseau--twitter")) {
      partagerSurReseau("twitter");
    } else if (e.target.closest(".btn-reseau--linkedin")) {
      partagerSurReseau("linkedin");
    } else if (e.target.closest(".btn-reseau--whatsapp")) {
      partagerSurReseau("whatsapp");
    } else if (e.target.closest(".btn-reseau--email")) {
      partagerSurReseau("email");
    }
  });

  // === Événements scroll et navigation ===
  window.addEventListener("scroll", gererScrollTop);

  btnTop.addEventListener("click", scrollVersHaut);

  // Progress dots visibility is handled by scroll spy in genererSommaire()


  // Palette de couleurs pour barres groupées
  var PALETTES = {
    officielle: {
      "lfi": "#BB1840", "la france insoumise": "#BB1840", "fi\u00E8re et populaire": "#BB1840", "front populaire": "#BB1840",
      "pcf": "#FF0000", "communiste": "#FF0000",
      "ps": "#E63946", "parti socialiste": "#E63946", "gauche unie": "#E63946", "printemps marseillais": "#E63946",
      "eelv": "#00A86B", "\u00E9cologistes": "#00A86B", "respire": "#00A86B", "pour vivre": "#00A86B",
      "modem": "#FF9500", "centriste": "#FF9500",
      "renaissance": "#FFCC00", "ensemble": "#FFCC00",
      "horizons": "#0082C4",
      "lr": "#0066CC", "les r\u00E9publicains": "#0066CC",
      "rn": "#0D1B4C", "rassemblement national": "#0D1B4C",
      "reconqu\u00EAte": "#1A1A1A", "reconquete": "#1A1A1A"
    },
    flat: {
      "ps": "#6366F1", "parti socialiste": "#6366F1", "gauche unie": "#6366F1", "printemps marseillais": "#6366F1",
      "renaissance": "#8B5CF6", "ensemble": "#8B5CF6",
      "lr": "#EC4899", "les r\u00E9publicains": "#EC4899",
      "reconqu\u00EAte": "#F59E0B", "reconquete": "#F59E0B",
      "lfi": "#10B981", "la france insoumise": "#10B981", "fi\u00E8re et populaire": "#10B981", "front populaire": "#10B981",
      "rn": "#64748B", "rassemblement national": "#64748B",
      "eelv": "#22D3EE", "\u00E9cologistes": "#22D3EE", "respire": "#22D3EE", "pour vivre": "#22D3EE",
      "pcf": "#F43F5E", "communiste": "#F43F5E",
      "modem": "#A78BFA", "centriste": "#A78BFA",
      "horizons": "#38BDF8"
    },
    moderne: {
      "ps": "#E63946", "parti socialiste": "#E63946", "gauche unie": "#E63946", "printemps marseillais": "#E63946",
      "renaissance": "#F59E0B", "ensemble": "#F59E0B",
      "lr": "#3B82F6", "les r\u00E9publicains": "#3B82F6",
      "reconqu\u00EAte": "#1A1A1A", "reconquete": "#1A1A1A",
      "lfi": "#C94277", "la france insoumise": "#C94277", "fi\u00E8re et populaire": "#C94277", "front populaire": "#C94277",
      "rn": "#64748B", "rassemblement national": "#64748B",
      "eelv": "#059669", "\u00E9cologistes": "#059669", "respire": "#059669", "pour vivre": "#059669",
      "pcf": "#DC2626", "communiste": "#DC2626",
      "modem": "#FB923C", "centriste": "#FB923C",
      "horizons": "#0284C7"
    }
  };

  var paletteActuelle = "officielle";
  var dpPaletteBarres = document.getElementById("dp-palette-barres");
  if (dpPaletteBarres) {
    dpPaletteBarres.addEventListener("change", function() {
      paletteActuelle = dpPaletteBarres.value;
      localStorage.setItem("dp-palette-barres", paletteActuelle);
      // Mettre à jour COULEURS_PARTIS
      var p = PALETTES[paletteActuelle] || PALETTES.officielle;
      var keys = Object.keys(p);
      for (var i = 0; i < keys.length; i++) {
        COULEURS_PARTIS[keys[i]] = p[keys[i]];
      }
      // Réafficher les barres et stats si visibles
      if (typeof afficherRepartition === "function" && !document.getElementById("repartition").hidden) {
        afficherRepartition();
      }
      if (typeof afficherStatistiques === "function" && !document.getElementById("statistiques").hidden) {
        afficherStatistiques();
      }
    });
    var storedPalette = localStorage.getItem("dp-palette-barres");
    if (storedPalette) {
      dpPaletteBarres.value = storedPalette;
      paletteActuelle = storedPalette;
      var p = PALETTES[paletteActuelle] || PALETTES.officielle;
      var keys = Object.keys(p);
      for (var i = 0; i < keys.length; i++) {
        COULEURS_PARTIS[keys[i]] = p[keys[i]];
      }
    }
  }

  // === Style pictos ===
  var dpPictoStyle = document.getElementById("dp-picto-style");

  function rafraichirPictos() {
    if (donneesElection) {
      var cands = donneesElection.candidats.slice().sort(function(a, b) { return a.nom.localeCompare(b.nom, "fr"); });
      genererSommaire();
      afficherGrille(cands);
      afficherRepartition(cands);
      genererStatistiques(cands);
    }
  }

  if (dpPictoStyle) {
    var storedPicto = localStorage.getItem("dp-picto-style");
    if (storedPicto) {
      dpPictoStyle.value = storedPicto;
      pictoStyleActuel = storedPicto;
      if (ICON_CDNS[storedPicto]) chargerIconCDN(storedPicto, null);
    }
    dpPictoStyle.addEventListener("change", function() {
      pictoStyleActuel = dpPictoStyle.value;
      localStorage.setItem("dp-picto-style", pictoStyleActuel);
      if (ICON_CDNS[pictoStyleActuel]) {
        chargerIconCDN(pictoStyleActuel, rafraichirPictos);
      } else {
        rafraichirPictos();
      }
    });
  }

  // === Toggle Vue de page (Vue 1 / Vue 2) ===
  var dpVuePage = document.getElementById("dp-vue-page");
  var vuePageActuelle = localStorage.getItem("dp-vue-page") || "vue1";

  function appliquerVuePage(vue) {
    vuePageActuelle = vue;
    document.body.setAttribute("data-vue", vue);
    localStorage.setItem("dp-vue-page", vue);
    dpVuePage.value = vue;

    if (vue === "vue2") {
      // Vue 2 : masquer répartition et filtres, réordonner sections
      repartitionSection.hidden = true;
      filtresContainer.hidden = true;
    }
    // Re-render si élection active
    if (donneesElection) {
      var cands = donneesElection.candidats.slice().sort(function (a, b) { return a.nom.localeCompare(b.nom, "fr"); });
      if (vue === "vue1") {
        repartitionSection.hidden = true;
      }
      afficherGrille(cands);
      genererStatistiques(cands);
    }
  }

  if (dpVuePage) {
    dpVuePage.value = vuePageActuelle;
    dpVuePage.addEventListener("change", function () {
      appliquerVuePage(dpVuePage.value);
    });
  }
  document.body.setAttribute("data-vue", vuePageActuelle);

  // Gestion des alertes
  btnAlerte.addEventListener("click", inscrireAlerte);
  alerteEmailInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      inscrireAlerte();
    }
  });

  // === Gestion des modales ===
  function ouvrirModal(modalId) {
    var modal = document.getElementById("modal-" + modalId);
    if (modal) {
      modal.hidden = false;
      document.body.style.overflow = "hidden"; // Bloquer le scroll
    }
  }

  function fermerModal(modal) {
    modal.hidden = true;
    document.body.style.overflow = ""; // Restaurer le scroll
  }

  // Événements pour ouvrir les modales
  document.addEventListener("click", function(e) {
    var lienModal = e.target.closest("[data-modal]");
    if (lienModal) {
      e.preventDefault();
      var modalId = lienModal.getAttribute("data-modal");
      ouvrirModal(modalId);
    }
  });

  // Événements pour fermer les modales
  document.addEventListener("click", function(e) {
    // Fermer via le bouton X
    if (e.target.classList.contains("modal__fermer")) {
      var modal = e.target.closest(".modal");
      if (modal) fermerModal(modal);
    }

    // Fermer via l'overlay
    if (e.target.classList.contains("modal__overlay")) {
      var modal = e.target.closest(".modal");
      if (modal) fermerModal(modal);
    }
  });

  // Fermer avec Échap
  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape") {
      var modalOuverte = document.querySelector(".modal:not([hidden])");
      if (modalOuverte) {
        fermerModal(modalOuverte);
      }
    }
  });

  // === Gestion du formulaire de signalement ===
  var formSignalement = document.getElementById("form-signalement");
  if (formSignalement) {
    formSignalement.addEventListener("submit", function(e) {
      e.preventDefault();

      // Récupérer les valeurs du formulaire
      var ville = document.getElementById("signalement-ville").value;
      var candidat = document.getElementById("signalement-candidat").value;
      var categorie = document.getElementById("signalement-categorie").value;
      var erreur = document.getElementById("signalement-erreur").value;
      var source = document.getElementById("signalement-source").value;
      var email = document.getElementById("signalement-email").value;

      // Construire le corps de l'email
      var sujet = "Signalement d'erreur - " + ville + " - " + candidat;
      var corps = "SIGNALEMENT D'ERREUR\n\n";
      corps += "Ville : " + ville + "\n";
      corps += "Candidat : " + candidat + "\n";
      if (categorie) {
        corps += "Catégorie : " + categorie + "\n";
      }
      corps += "\nDescription de l'erreur :\n" + erreur + "\n";
      if (source) {
        corps += "\nSource correcte : " + source + "\n";
      }
      if (email) {
        corps += "\nEmail de contact : " + email + "\n";
      }

      // Créer le lien mailto
      var mailtoLink = "mailto:erreurs@pourquituvotes.fr" +
        "?subject=" + encodeURIComponent(sujet) +
        "&body=" + encodeURIComponent(corps);

      // Ouvrir le client email
      window.location.href = mailtoLink;

      // Réinitialiser le formulaire
      formSignalement.reset();

      // Fermer la modale après un court délai
      setTimeout(function() {
        var modal = document.getElementById("modal-signaler");
        if (modal) fermerModal(modal);
      }, 500);
    });
  }

  // === Burger menu mobile (full-screen overlay) ===
  (function() {
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
      var diff = new Date("2026-03-15T08:00:00").getTime() - Date.now();
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
      a.addEventListener("click", function() {
        closeMenu();
      });
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
          var results = rechercherVilles(val).slice(0, 8);
          if (results.length === 0) {
            suggestionsEl.innerHTML = "";
            suggestionsEl.hidden = true;
            return;
          }
          suggestionsEl.innerHTML = results.map(function(v) {
            return '<div class="mobile-menu-suggestion-item" data-id="' + v.id + '">' +
              '<i class="ph ph-map-pin"></i>' +
              '<span>' + echapper(v.nom) + '</span>' +
              '<span class="mobile-menu-suggestion-cp">' + v.codePostal + '</span>' +
              '</div>';
          }).join("");
          suggestionsEl.hidden = false;

          suggestionsEl.querySelectorAll(".mobile-menu-suggestion-item").forEach(function(item) {
            item.addEventListener("click", function() {
              var ville = VILLES.find(function(v) { return v.id === item.dataset.id; });
              if (ville) {
                closeMenu();
                selectionnerVille(ville);
              }
            });
          });
        }, 200);
      });
    }
  })();

  // === Initialisation ===
  // Charger le thème sauvegardé
  chargerTheme();

  // Initialiser l'état du bouton scroll
  gererScrollTop();

  // Charger les données puis initialiser depuis l'URL
  afficherChargement(true);
  chargerVilles().then(function() {
    afficherChargement(false);
    chargerDepuisURL();
  }).catch(function(err) {
    console.error('Erreur chargement villes:', err);
    afficherChargement(false);
  });
})();
