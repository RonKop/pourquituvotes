(function () {
  "use strict";


  // === Chargement des données (JSON externe) ===
  var VILLES = [];
  var ELECTIONS = {};
  var ELECTIONS_CACHE = {};
  var DATA_BASE_URL = '/data/';
  var DATA_VERSION = '2026021001';

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
  var radarVueActuelle = "individuelle";
  var radarToggleInitialise = false;
  var radarChartComparerGlobal = null;
  var btnPartager = document.getElementById("btn-partager");
  var partageReseaux = document.getElementById("partage-reseaux");
  var selectionCandidatsSection = document.getElementById("selection-candidats");
  var candidatsCheckboxesContainer = document.getElementById("candidats-checkboxes");
  var btnTop = document.getElementById("btn-top");
  var sommaire = document.getElementById("sommaire");
  var sommaireNav = document.getElementById("sommaire-nav");
  var sommaireToggle = document.getElementById("sommaire-toggle");
  var themeToggle = document.getElementById("dp-theme-toggle");
  var fontSelect = null; // Moved to design panel
  var alertesSection = document.getElementById("alertes-section");
  var aucunCandidatSection = document.getElementById("aucun-candidat");
  var alerteEmailInput = document.getElementById("alerte-email");
  var btnAlerte = document.getElementById("btn-alerte");
  var alerteMessage = document.getElementById("alerte-message");

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

      countdownElement.hidden = false;
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

      if (donneesElection.dateVote) {
        demarrerCountdown(donneesElection.dateVote);
      } else {
        arreterCountdown();
      }

      mettreAJourMetadonnees();
      afficherElection();
      afficherChargement(false);
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

  function partagerComparaison() {
    // Toggle l'affichage des boutons réseaux sociaux
    partageReseaux.hidden = !partageReseaux.hidden;

    if (!partageReseaux.hidden) {
      btnPartager.textContent = "✕ Fermer";
    } else {
      btnPartager.textContent = "🔗 Copier le lien";
    }
  }

  function copierLien() {
    mettreAJourURL();
    var url = genererURLAvecUTM("copie_directe");

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(function () {
        afficherToast("✓ Lien copié ! Partagez-le avec vos proches");
        setTimeout(function() {
          partageReseaux.hidden = true;
          btnPartager.textContent = "🔗 Copier le lien";
        }, 1500);
      }).catch(function () {
        afficherToast("Erreur lors de la copie du lien");
      });
    } else {
      // Fallback
      var textarea = document.createElement("textarea");
      textarea.value = url;
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand("copy");
        afficherToast("✓ Lien copié !");
        setTimeout(function() {
          partageReseaux.hidden = true;
          btnPartager.textContent = "🔗 Copier le lien";
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

  // === Sommaire et navigation ===
  function genererSommaire() {
    if (!donneesElection) {
      sommaire.hidden = true;
      return;
    }

    sommaireNav.innerHTML = "";

    // Ajouter "Toutes les catégories"
    var itemToutes = creerItemSommaire("toutes", getIconeCategorie("_toutes"), "Toutes les cat\u00E9gories", null);
    sommaireNav.appendChild(itemToutes);

    // Ajouter chaque catégorie
    donneesElection.categories.forEach(function (cat) {
      var icone = getIconeCategorie(cat.id);
      var count = compterPropositionsCategorie(cat);
      var item = creerItemSommaire(cat.id, icone, cat.nom, count);
      sommaireNav.appendChild(item);
    });

    sommaire.hidden = false;
    mettreAJourSommaireActif();
  }

  function creerItemSommaire(categorieId, icone, nom, count) {
    var item = document.createElement("div");
    item.className = "sommaire__item";
    item.dataset.categorie = categorieId;

    var iconeSpan = document.createElement("span");
    iconeSpan.className = "sommaire__item-icone";
    iconeSpan.innerHTML = icone;

    var texteSpan = document.createElement("span");
    texteSpan.className = "sommaire__item-texte";
    texteSpan.textContent = nom;

    item.appendChild(iconeSpan);
    item.appendChild(texteSpan);

    if (count !== null) {
      var countSpan = document.createElement("span");
      countSpan.className = "sommaire__item-count";
      countSpan.textContent = count;
      item.appendChild(countSpan);
    }

    item.addEventListener("click", function () {
      categorieActive = categorieId;
      var candidats = donneesElection.candidats.slice().sort(function (a, b) {
        return a.nom.localeCompare(b.nom, "fr");
      });

      filtresContainer.querySelectorAll(".filtre-btn").forEach(function (btn) {
        btn.classList.toggle("filtre-btn--active", btn.dataset.categorie === categorieId);
      });

      afficherGrille(candidats);
      mettreAJourSommaireActif();
      mettreAJourURL();

      // Scroll vers la première catégorie affichée
      var premiereCategorie = comparaisonContainer.querySelector(".categorie");
      if (premiereCategorie) {
        premiereCategorie.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });

    return item;
  }

  function mettreAJourSommaireActif() {
    sommaireNav.querySelectorAll(".sommaire__item").forEach(function (item) {
      var estActif = item.dataset.categorie === categorieActive;
      item.classList.toggle("sommaire__item--actif", estActif);
    });
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
    afficherAlertes();
    afficherRepartition(candidats);
    afficherFiltres();
    afficherGrille(candidats);

    etatVide.hidden = true;
    comparaisonContainer.hidden = false;
  }

  // === Statistiques visuelles ===
  function genererStatistiques(tousLesCandidats) {
    if (!donneesElection) return;

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

    // === Radar chart — système à deux vues ===
    var radarGrille = document.getElementById("radar-vue-individuelle");
    var radarComparer = document.getElementById("radar-vue-comparer");
    var radarVueBtns = document.querySelectorAll(".radar-vue-btn");
    var radarChartsIndividuels = [];
    var radarCandidatsSelectionnes = [];

    if (donneesElection && radarGrille) {
      var categories = donneesElection.categories;
      var categoriesLabels = categories.map(function(cat) { return cat.nom; });
      var couleurGrilleRadar = theme === "dark" ? "rgba(255,255,255,0.1)" : "#e5e5e5";
      var couleurTexteRadar = theme === "dark" ? "#ccc" : "#555";

      function hexToRgba(hex, alpha) {
        if (!hex || hex.charAt(0) !== "#") return "rgba(128,128,128," + alpha + ")";
        var r = parseInt(hex.slice(1, 3), 16);
        var g = parseInt(hex.slice(3, 5), 16);
        var b = parseInt(hex.slice(5, 7), 16);
        return "rgba(" + r + "," + g + "," + b + "," + alpha + ")";
      }

      function getDataCandidat(candidat) {
        var counts = categories.map(function(cat) { return compterPropositionsCandidat(cat, candidat.id); });
        var total = counts.reduce(function(s, v) { return s + v; }, 0);
        return counts.map(function(v) { return total > 0 ? Math.round(v / total * 100) : 0; });
      }

      function getRadarOptions(showLegend) {
        return {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: { display: !!showLegend, position: "bottom", labels: { color: couleurTexteRadar, font: { family: "'DM Sans', sans-serif", size: 11 }, padding: 12 } },
            tooltip: {
              backgroundColor: theme === "dark" ? "#252538" : "#fff",
              titleColor: couleurTexteRadar,
              bodyColor: couleurTexteRadar,
              borderColor: couleurGrilleRadar,
              borderWidth: 1,
              callbacks: { label: function(ctx) { return (ctx.dataset.label || "") + ": " + ctx.parsed.r + "%"; } }
            }
          },
          scales: {
            r: {
              min: 0,
              ticks: { color: couleurTexteRadar, backdropColor: "transparent", stepSize: 10, callback: function(v) { return v + "%"; } },
              grid: { color: couleurGrilleRadar },
              pointLabels: { color: couleurTexteRadar, font: { family: "'DM Sans', sans-serif", size: 11, weight: 600 } }
            }
          }
        };
      }

      // --- Top 6 catégories (pour radars individuels, plus lisible) ---
      var totalParCategorie = categories.map(function(cat) {
        var total = 0;
        candidats.forEach(function(c) { total += compterPropositionsCandidat(cat, c.id); });
        return { nom: cat.nom, idx: categories.indexOf(cat), total: total };
      });
      totalParCategorie.sort(function(a, b) { return b.total - a.total; });
      var top6 = totalParCategorie.slice(0, 6);
      var top6Indices = top6.map(function(t) { return t.idx; });
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
      var top6Labels = top6.map(function(t) { return LABELS_COURTS[t.nom] || t.nom; });

      function getDataCandidatTop6(candidat) {
        var allData = getDataCandidat(candidat);
        return top6Indices.map(function(i) { return allData[i]; });
      }

      function getRadarOptionsIndiv() {
        var opts = getRadarOptions(false);
        opts.scales.r.pointLabels.font.size = 11;
        return opts;
      }

      // --- Vue 1 : grille individuelle ---
      function rendreVueIndividuelle() {
        radarGrille.innerHTML = "";
        radarChartsIndividuels.forEach(function(c) { c.destroy(); });
        radarChartsIndividuels = [];

        var candidatsActifs = getCandidatsActifs();

        candidatsActifs.forEach(function(candidat, idx) {
          var idxGlobal = candidats.indexOf(candidat);
          var couleur = getCouleurParti(candidat, idxGlobal >= 0 ? idxGlobal : idx);
          var carte = document.createElement("div");
          carte.className = "radar-carte";
          carte.dataset.candidatId = candidat.id;

          var headerDiv = document.createElement("div");
          headerDiv.className = "radar-carte__header";
          headerDiv.innerHTML =
            '<span class="radar-carte__pastille" style="background:' + couleur + '"></span>' +
            '<div class="radar-carte__infos">' +
              '<span class="radar-carte__nom">' + echapper(candidat.nom) + '</span>' +
              '<span class="radar-carte__parti">' + echapper(candidat.liste) + '</span>' +
            '</div>';

          var btnMasquer = document.createElement("button");
          btnMasquer.className = "radar-carte__masquer";
          btnMasquer.textContent = "\u00D7";
          btnMasquer.title = "Masquer " + candidat.nom;
          btnMasquer.addEventListener("click", function(e) {
            e.stopPropagation();
            toggleCandidatSelection(candidat.id);
          });
          headerDiv.appendChild(btnMasquer);

          var canvas = document.createElement("canvas");
          carte.appendChild(headerDiv);
          carte.appendChild(canvas);
          radarGrille.appendChild(carte);

          var chart = new Chart(canvas, {
            type: "radar",
            data: {
              labels: top6Labels,
              datasets: [{
                label: candidat.nom,
                data: getDataCandidatTop6(candidat),
                backgroundColor: hexToRgba(couleur, 0.25),
                borderColor: couleur,
                borderWidth: 2,
                pointBackgroundColor: couleur,
                pointBorderColor: "#fff",
                pointRadius: 3
              }]
            },
            options: getRadarOptionsIndiv()
          });
          radarChartsIndividuels.push(chart);
        });
      }

      // --- Vue 2 : radar combiné avec checkboxes ---
      function rendreVueComparer() {
        var selDiv = document.getElementById("radar-selection-candidats");
        selDiv.innerHTML = "";
        radarCandidatsSelectionnes = [];

        candidats.forEach(function(candidat, idx) {
          var couleur = getCouleurParti(candidat, idx);
          var item = document.createElement("label");
          item.className = "radar-comparer__candidat";

          var cb = document.createElement("input");
          cb.type = "checkbox";
          cb.className = "radar-comparer__checkbox";
          cb.value = candidat.id;
          cb.style.accentColor = couleur;

          var pastille = document.createElement("span");
          pastille.className = "radar-comparer__pastille";
          pastille.style.background = couleur;

          var infos = document.createElement("span");
          infos.className = "radar-comparer__infos";
          infos.innerHTML = '<span class="radar-comparer__nom">' + echapper(candidat.nom) + '</span>' +
            '<span class="radar-comparer__parti">' + echapper(candidat.liste) + '</span>';

          item.appendChild(cb);
          item.appendChild(pastille);
          item.appendChild(infos);

          cb.addEventListener("change", function() {
            var id = candidat.id;
            if (cb.checked) {
              radarCandidatsSelectionnes.push(id);
              item.classList.add("radar-comparer__candidat--active");
            } else {
              var pos = radarCandidatsSelectionnes.indexOf(id);
              if (pos >= 0) radarCandidatsSelectionnes.splice(pos, 1);
              item.classList.remove("radar-comparer__candidat--active");
            }
            mettreAJourRadarComparer();
          });
          selDiv.appendChild(item);
        });

        var canvasComparer = document.getElementById("chart-radar-comparer");
        if (radarChartComparerGlobal) { radarChartComparerGlobal.destroy(); }

        radarChartComparerGlobal = new Chart(canvasComparer, {
          type: "radar",
          data: { labels: categoriesLabels, datasets: [] },
          options: getRadarOptions(true)
        });
      }

      function mettreAJourRadarComparer() {
        if (!radarChartComparerGlobal) return;
        var datasets = [];
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
            borderWidth: 2,
            pointBackgroundColor: couleur,
            pointBorderColor: "#fff",
            pointRadius: 3
          });
        });
        radarChartComparerGlobal.data.datasets = datasets;
        radarChartComparerGlobal.update();
      }

      // Toggle entre vues — une seule visible à la fois
      if (!radarToggleInitialise) {
        radarVueBtns.forEach(function(btn) {
          btn.addEventListener("click", function() {
            var vue = btn.dataset.radarVue;
            if (vue === radarVueActuelle) return;
            radarVueActuelle = vue;
            document.querySelectorAll(".radar-vue-btn").forEach(function(b) { b.classList.remove("radar-vue-btn--active"); });
            btn.classList.add("radar-vue-btn--active");
            var rg = document.getElementById("radar-vue-individuelle");
            var rc = document.getElementById("radar-vue-comparer");
            if (vue === "individuelle") {
              rg.hidden = false;
              rc.hidden = true;
            } else {
              rg.hidden = true;
              rc.hidden = false;
              if (radarChartComparerGlobal) {
                setTimeout(function() { radarChartComparerGlobal.resize(); }, 50);
              }
            }
          });
        });
        radarToggleInitialise = true;
      }

      // Synchroniser l'état visible avec radarVueActuelle
      if (radarVueActuelle === "individuelle") {
        radarGrille.hidden = false;
        radarComparer.hidden = true;
      } else {
        radarGrille.hidden = true;
        radarComparer.hidden = false;
      }
      radarVueBtns.forEach(function(b) {
        b.classList.toggle("radar-vue-btn--active", b.dataset.radarVue === radarVueActuelle);
      });

      // Rendre les deux vues
      rendreVueIndividuelle();
      rendreVueComparer();
    }

    // Afficher l'encart méthodologique sous le radar
    var methodoDiv = document.getElementById("radar-methodologie");
    if (methodoDiv && donneesElection) {
      var tousCandidats = donneesElection.candidats;
      var complets = tousCandidats.filter(function(c) { return c.programmeComplet; });
      var partiels = tousCandidats.filter(function(c) { return !c.programmeComplet; });

      var html = '<strong>\u26A0\uFE0F \u00C9quit\u00E9 de comparaison :</strong> ';
      if (complets.length > 0 && partiels.length > 0) {
        html += 'Tous les candidats n\u2019ont pas encore publi\u00E9 leur programme officiel. ';
        html += 'Un radar plus petit ne signifie pas forc\u00E9ment moins d\u2019ambition, mais parfois simplement moins de propositions rendues publiques \u00E0 ce jour.';
        html += '<div class="methodo-legend">';
        complets.forEach(function(c) {
          html += '<span class="methodo-item">\u2705 <strong>' + c.nom + '</strong> \u2014 programme officiel</span>';
        });
        partiels.forEach(function(c) {
          html += '<span class="methodo-item">\uD83D\uDCCB <strong>' + c.nom + '</strong> \u2014 sources publiques - programme \u00E0 venir</span>';
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
    if (vuePageActuelle !== "vue2") {
      repartitionSection.hidden = false;
    }
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
    "lfi": "#BB1840", "la france insoumise": "#BB1840", "fi\u00E8re et populaire": "#BB1840", "front populaire": "#BB1840",
    "pcf": "#FF0000", "communiste": "#FF0000",
    "ps": "#E63946", "parti socialiste": "#E63946", "gauche unie": "#E63946", "printemps marseillais": "#E63946",
    "eelv": "#00A86B", "\u00E9cologistes": "#00A86B", "respire": "#00A86B", "pour vivre": "#00A86B",
    "modem": "#FF9500", "centriste": "#FF9500",
    "renaissance": "#FFCC00", "ensemble": "#FFCC00",
    "horizons": "#0082C4",
    "lr": "#0066CC", "les r\u00E9publicains": "#0066CC", "union citoyenne de la droite": "#0066CC",
    "rn": "#0D1B4C", "rassemblement national": "#0D1B4C",
    "reconqu\u00EAte": "#1A1A1A", "reconquete": "#1A1A1A",
    "lo": "#B91C1C", "lutte ouvri\u00E8re": "#B91C1C", "anticapitaliste": "#B91C1C",
    "udr": "#003399", "ciotti": "#003399",
    "dvd": "#4488CC", "divers droite": "#4488CC",
    "dvg": "#FFB0B0", "divers gauche": "#FFB0B0",
    "se": "#6C757D", "sans \u00E9tiquette": "#6C757D"
  };

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
        if (nb > 0) {
          barresHTML += '<div class="rep-barres__ligne">' +
            '<span class="rep-barres__nom" style="color:' + couleur + '">' + echapper(c.nom) + '</span>' +
            '<div class="rep-barres__bar-track">' +
              '<div class="rep-barres__fill" style="width:' + pct + '%;background:' + couleur + '" title="' + echapper(c.nom) + ' : ' + nb + '"></div>' +
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
      html += '<strong>\u26A0\uFE0F \u00C9quit\u00E9 de comparaison</strong>';
      html += '<p>Tous les candidats n\u2019ont pas encore publi\u00E9 leur programme officiel. ';
      html += 'Un nombre inf\u00E9rieur de propositions ne refl\u00E8te pas n\u00E9cessairement un projet moins ambitieux.</p>';
      html += '<div class="repartition-avertissement__liste">';
      complets.forEach(function (c) {
        html += '<span class="repartition-avertissement__tag repartition-avertissement__tag--complet">\u2705 ' + echapper(c.nom) + ' \u2014 ' + donnees.totaux[c.id] + ' propositions (programme officiel)</span>';
      });
      partiels.forEach(function (c) {
        html += '<span class="repartition-avertissement__tag repartition-avertissement__tag--partiel">\uD83D\uDCCB ' + echapper(c.nom) + ' \u2014 ' + donnees.totaux[c.id] + ' propositions (sources publiques - programme \u00E0 venir)</span>';
      });
      html += '</div>';
      html += '</div>';
    }

    // Date de disponibilité des programmes
    html += '<div class="repartition-avertissement__bloc repartition-avertissement__bloc--date">';
    html += '<strong>\uD83D\uDCC5 Calendrier</strong>';
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
    if (vuePageActuelle !== "vue2") {
      filtresContainer.hidden = false;
    }
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

    var candidats = getCandidatsActifs();
    var nbTotal = donneesElection ? donneesElection.candidats.length : candidats.length;

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

    var header = document.createElement("div");
    header.className = "categorie__header";
    header.style.position = "relative";
    header.innerHTML =
      '<div>' +
        '<span class="categorie__nom">' +
          '<span class="categorie__icone">' + getIconeCategorie(categorie.id) + '</span>' +
          echapper(categorie.nom) +
        '</span> ' +
        '<span class="categorie__count">' + totalPropositions + ' proposition' +
        (totalPropositions > 1 ? 's' : '') + ' \u2022 ' + categorie.sousThemes.length + ' sous-th\u00E8mes</span>' +
      '</div>' +
      '<span class="categorie__toggle">\u25BC</span>';

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

      var fullContent = document.createElement("span");
      fullContent.className = "tableau-col__content-full";
      fullContent.innerHTML = '<strong>' + echapper(candidat.nom) + '</strong><span class="candidat-parti-label">' + echapper(candidat.liste) + '</span> ' + badgeHTML;

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
        if (nb > 0) {
          barresHTML += '<div class="rep-barres__ligne">' +
            '<span class="rep-barres__nom" style="color:' + couleur + '">' + echapper(c.nom) + '</span>' +
            '<div class="rep-barres__bar-track">' +
              '<div class="rep-barres__fill" style="width:' + pct + '%;background:' + couleur + '" title="' + echapper(c.nom) + ' : ' + nb + '"></div>' +
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

  // === Événements ===
  villeSearchInput.addEventListener("input", function () {
    var terme = villeSearchInput.value.trim();
    if (terme.length === 0) {
      masquerSuggestions();
      villeSelectionnee = null;
      donneesElection = null;
      electionInfo.hidden = true;
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
      return;
    }

    var villesTrouvees = rechercherVilles(terme);
    afficherSuggestions(villesTrouvees, terme);
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

  // === Événements partage ===
  btnPartager.addEventListener("click", function(e) {
    e.stopPropagation();
    partagerComparaison();
  });

  // Copier le lien au double-clic sur le bouton principal
  btnPartager.addEventListener("dblclick", function(e) {
    e.stopPropagation();
    copierLien();
  });

  // Gestionnaires pour les boutons de réseaux sociaux
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
    } else if (!e.target.closest(".partage-container")) {
      // Fermer les boutons si on clique ailleurs
      if (!partageReseaux.hidden) {
        partageReseaux.hidden = true;
        btnPartager.textContent = "🔗 Copier le lien";
      }
    }
  });

  // === Événements scroll et navigation ===
  window.addEventListener("scroll", gererScrollTop);

  btnTop.addEventListener("click", scrollVersHaut);

  sommaireToggle.addEventListener("click", function () {
    sommaire.classList.toggle("sommaire--masque");
  });

  // === Panneau de contrôles Design ===
  var designPanel = document.getElementById("design-panel");
  var designPanelToggle = document.getElementById("design-panel-toggle");
  var heroEl = document.getElementById("hero");
  var HERO_STYLES = ["ruban", "confettis", "mesh", "topo"];

  // Toggle panneau
  designPanelToggle.addEventListener("click", function() {
    designPanel.classList.toggle("design-panel--collapsed");
  });

  // Police titres
  var dpFontTitres = document.getElementById("dp-font-titres");
  var dpFontTexte = document.getElementById("dp-font-texte");
  function appliquerPolices() {
    document.documentElement.style.setProperty("--police-titres", dpFontTitres.value);
    document.documentElement.style.setProperty("--police-texte", dpFontTexte.value);
    localStorage.setItem("dp-font-titres", dpFontTitres.value);
    localStorage.setItem("dp-font-texte", dpFontTexte.value);
  }
  var storedFontTitres = localStorage.getItem("dp-font-titres");
  var storedFontTexte = localStorage.getItem("dp-font-texte");
  if (storedFontTitres) { dpFontTitres.value = storedFontTitres; }
  if (storedFontTexte) { dpFontTexte.value = storedFontTexte; }
  appliquerPolices();
  dpFontTitres.addEventListener("change", appliquerPolices);
  dpFontTexte.addEventListener("change", appliquerPolices);

  // Couleurs
  var dpCouleurAccent = document.getElementById("dp-couleur-accent");
  var dpCouleurAccentLight = document.getElementById("dp-couleur-accent-light");
  function appliquerCouleurs() {
    document.documentElement.style.setProperty("--couleur-accent", dpCouleurAccent.value);
    document.documentElement.style.setProperty("--couleur-accent-light", dpCouleurAccentLight.value);
    localStorage.setItem("dp-couleur-accent", dpCouleurAccent.value);
    localStorage.setItem("dp-couleur-accent-light", dpCouleurAccentLight.value);
  }
  var storedAccent = localStorage.getItem("dp-couleur-accent");
  var storedAccentLight = localStorage.getItem("dp-couleur-accent-light");
  if (storedAccent) { dpCouleurAccent.value = storedAccent; }
  if (storedAccentLight) { dpCouleurAccentLight.value = storedAccentLight; }
  appliquerCouleurs();
  dpCouleurAccent.addEventListener("input", appliquerCouleurs);
  dpCouleurAccentLight.addEventListener("input", appliquerCouleurs);

  // Mode clair / sombre
  var dpThemeSwitch = document.getElementById("dp-theme-toggle");
  function syncThemeSwitch() {
    var isDark = document.documentElement.getAttribute("data-theme") === "dark";
    dpThemeSwitch.setAttribute("data-active", isDark ? "true" : "false");
  }
  syncThemeSwitch();
  dpThemeSwitch.addEventListener("click", function() {
    togglerTheme();
    syncThemeSwitch();
  });

  // Style hero
  var dpHeroStyle = document.getElementById("dp-hero-style");
  function appliquerHeroStyle(style) {
    HERO_STYLES.forEach(function(s) { heroEl.classList.remove("hero--" + s); });
    if (style) heroEl.classList.add("hero--" + style);
  }
  var heroStocke = localStorage.getItem("hero-pqtv");
  if (heroStocke) {
    appliquerHeroStyle(heroStocke);
    dpHeroStyle.value = heroStocke;
  }
  dpHeroStyle.addEventListener("change", function() {
    var style = dpHeroStyle.value;
    appliquerHeroStyle(style);
    localStorage.setItem("hero-pqtv", style);
  });

  // Liseré
  var dpLisereStyle = document.getElementById("dp-lisere-style");
  var dpLisereEpaisseur = document.getElementById("dp-lisere-epaisseur");
  var dpLisereEpaisseurVal = document.getElementById("dp-lisere-epaisseur-val");
  function appliquerLisere() {
    var lisere = dpLisereStyle.value;
    var epaisseur = dpLisereEpaisseur.value + "px";
    dpLisereEpaisseurVal.textContent = epaisseur;
    if (lisere) {
      document.body.setAttribute("data-lisere", lisere);
    } else {
      document.body.removeAttribute("data-lisere");
    }
    document.documentElement.style.setProperty("--lisere-epaisseur", epaisseur);
    localStorage.setItem("dp-lisere-style", lisere);
    localStorage.setItem("dp-lisere-epaisseur", dpLisereEpaisseur.value);
  }
  var storedLisere = localStorage.getItem("dp-lisere-style");
  var storedLisereEp = localStorage.getItem("dp-lisere-epaisseur");
  if (storedLisere) { dpLisereStyle.value = storedLisere; }
  if (storedLisereEp) { dpLisereEpaisseur.value = storedLisereEp; }
  appliquerLisere();
  dpLisereStyle.addEventListener("change", appliquerLisere);
  dpLisereEpaisseur.addEventListener("input", appliquerLisere);

  // Densité
  var densityBtns = document.querySelectorAll(".design-panel__density-btn");
  function appliquerDensite(density) {
    densityBtns.forEach(function(b) {
      b.classList.toggle("design-panel__density-btn--active", b.dataset.density === density);
    });
    if (density && density !== "normal") {
      document.body.setAttribute("data-density", density);
    } else {
      document.body.removeAttribute("data-density");
    }
    localStorage.setItem("dp-density", density);
  }
  var storedDensity = localStorage.getItem("dp-density");
  if (storedDensity) { appliquerDensite(storedDensity); }
  densityBtns.forEach(function(btn) {
    btn.addEventListener("click", function() {
      appliquerDensite(btn.dataset.density);
    });
  });

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
        repartitionSection.hidden = false;
        filtresContainer.hidden = false;
        afficherRepartition(cands);
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

  // Masquer le bouton d'inscription si la date limite est dépassée
  var heroCta = document.getElementById("hero-cta-inscription");
  if (heroCta) {
    var dateLimiteInscription = new Date("2026-02-06T23:59:59");
    if (new Date() > dateLimiteInscription) {
      heroCta.hidden = true;
    }
  }

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

  // === Burger menu mobile ===
  (function() {
    var btn = document.getElementById("burger-btn");
    var menu = document.getElementById("mobile-menu");
    if (!btn || !menu) return;
    btn.addEventListener("click", function() {
      var expanded = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", !expanded);
      menu.hidden = expanded;
    });
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
