(function () {
  "use strict";

  var DATA_VERSION = "2026021002";
  var DATA_BASE_URL = "/data/";

  // === Utilitaires (copiés de app.js) ===
  function echapper(str) {
    var el = document.createElement("div");
    el.appendChild(document.createTextNode(str));
    return el.innerHTML;
  }

  var COULEURS_REP = [
    "#8B5CF6", "#2563EB", "#16A34A", "#EAB308", "#DC2626",
    "#0891B2", "#EA580C", "#4F46E5", "#059669", "#C026D3",
    "#D97706", "#E11D48", "#0D9488", "#BE123C"
  ];

  var COULEURS_PARTIS = {
    "lfi": "#A855F7", "la france insoumise": "#A855F7", "fière et populaire": "#A855F7", "front populaire": "#A855F7",
    "pcf": "#FF2D9A", "communiste": "#FF2D9A",
    "ps": "#FF2D9A", "parti socialiste": "#FF2D9A", "gauche unie": "#FF2D9A", "printemps marseillais": "#FF2D9A", "union de la gauche": "#FF2D9A",
    "eelv": "#22C55E", "écologistes": "#22C55E", "respire": "#22C55E", "pour vivre": "#22C55E",
    "modem": "#FFBF00", "centriste": "#FFBF00",
    "renaissance": "#FFBF00", "ensemble": "#FFBF00",
    "horizons": "#FFBF00",
    "lr": "#2D6EFF", "les républicains": "#2D6EFF", "union citoyenne de la droite": "#2D6EFF",
    "rn": "#1447E6", "rassemblement national": "#1447E6",
    "reconquête": "#FF6B00", "reconquete": "#FF6B00",
    "lo": "#A855F7", "lutte ouvrière": "#A855F7", "anticapitaliste": "#A855F7",
    "udr": "#2D6EFF", "ciotti": "#2D6EFF",
    "dvd": "#14B8A6", "divers droite": "#14B8A6",
    "dvg": "#FF2D9A", "divers gauche": "#FF2D9A",
    "se": "#14B8A6", "sans étiquette": "#14B8A6"
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

  var ORDRE_CATEGORIES = [
    "education", "environnement", "transports", "sante", "logement",
    "economie", "solidarite", "urbanisme", "culture", "sport",
    "democratie", "securite"
  ];

  var PICTOS = {
    "transports": '<i class="ph ph-bus"></i>', "environnement": '<i class="ph ph-tree"></i>', "education": '<i class="ph ph-graduation-cap"></i>',
    "securite": '<i class="ph ph-shield-check"></i>', "economie": '<i class="ph ph-briefcase"></i>', "logement": '<i class="ph ph-house"></i>',
    "sante": '<i class="ph ph-first-aid"></i>', "culture": '<i class="ph ph-mask-happy"></i>', "sport": '<i class="ph ph-soccer-ball"></i>',
    "urbanisme": '<i class="ph ph-buildings"></i>', "democratie": '<i class="ph ph-check-square"></i>', "solidarite": '<i class="ph ph-handshake"></i>'
  };

  // === État ===
  var etat = {
    phase: "selection",
    ville: null,
    villeId: null,
    donneesElection: null,
    mode: null,
    questions: [],      // questions classiques (oui/non)
    duels: [],          // questions duel (Expert, thèmes prioritaires)
    reponses: {},       // sousThemeId → -1|0|1
    reponsesDuels: {},  // sousThemeId → candidatId choisi
    questionCourante: 0,
    priorites: [],
    resultats: null
  };

  var villesData = [];

  // === Chargement données ===
  function chargerVilles() {
    var prefetch = window.__prefetch && window.__prefetch.villes;
    var promise = prefetch || fetch(DATA_BASE_URL + "villes.json?v=" + DATA_VERSION)
      .then(function (r) { return r.json(); });
    return promise.then(function (data) {
      villesData = data;
      return data;
    });
  }

  function chargerDonneesElection(id) {
    var prefetch = window.__prefetch && window.__prefetch.election;
    if (prefetch) {
      window.__prefetch.election = null;
      return prefetch.then(function (data) {
        if (data) return data;
        return fetch(DATA_BASE_URL + "elections/" + id + ".json?v=" + DATA_VERSION)
          .then(function (r) { return r.json(); });
      });
    }
    return fetch(DATA_BASE_URL + "elections/" + id + ".json?v=" + DATA_VERSION)
      .then(function (r) {
        if (!r.ok) throw new Error("Erreur chargement election: " + r.status);
        return r.json();
      });
  }

  // === Helper: trouver un sous-thème dans les données ===
  function trouverSousTheme(sousThemeId) {
    var categories = etat.donneesElection.categories;
    for (var c = 0; c < categories.length; c++) {
      for (var s = 0; s < categories[c].sousThemes.length; s++) {
        if (categories[c].sousThemes[s].id === sousThemeId) {
          return { categorie: categories[c], sousTheme: categories[c].sousThemes[s] };
        }
      }
    }
    return null;
  }

  // === Helper: trouver l'auteur d'une proposition dans une question ===
  // Compare le texte affiché dans la question au texte de chaque candidat
  function trouverAuteurQuestion(question) {
    var found = trouverSousTheme(question.sousThemeId);
    if (!found) return null;
    var candidats = etat.donneesElection.candidats;
    for (var i = 0; i < candidats.length; i++) {
      var prop = found.sousTheme.propositions[candidats[i].id];
      if (prop && prop.texte && prop.texte === question.texte) {
        return { candidat: candidats[i], proposition: prop };
      }
    }
    // Fallback : premier candidat avec une proposition
    for (var j = 0; j < candidats.length; j++) {
      var p = found.sousTheme.propositions[candidats[j].id];
      if (p && p.texte) {
        return { candidat: candidats[j], proposition: p };
      }
    }
    return null;
  }

  // === Génération de questions ===
  function calculerClivance(sousTheme, candidats) {
    var total = candidats.length;
    if (total === 0) return 0;
    var nbAvec = 0;
    for (var i = 0; i < candidats.length; i++) {
      if (sousTheme.propositions[candidats[i].id] != null) {
        nbAvec++;
      }
    }
    if (nbAvec === 0) return 0;
    var nbSans = total - nbAvec;
    return 1 - Math.abs(nbAvec - nbSans) / total;
  }

  function trouverTexteQuestion(sousTheme, candidats) {
    var options = [];
    // Collecter tous les candidats ayant une proposition
    for (var i = 0; i < candidats.length; i++) {
      var prop = sousTheme.propositions[candidats[i].id];
      if (prop && prop.texte) {
        options.push({ texte: prop.texte, candidatId: candidats[i].id });
      }
    }
    if (options.length === 0) return null;
    // Rotation aléatoire : tirer un candidat au hasard pour l'équité
    var choix = options[Math.floor(Math.random() * options.length)];
    return choix.texte;
  }

  // Trouver 2 propositions clivantes pour un duel
  function trouverDuel(sousTheme, candidats) {
    var props = [];
    for (var i = 0; i < candidats.length; i++) {
      var prop = sousTheme.propositions[candidats[i].id];
      if (prop && prop.texte) {
        props.push({
          candidatId: candidats[i].id,
          candidatNom: candidats[i].nom,
          candidatListe: candidats[i].liste,
          candidatIndex: i,
          texte: prop.texte,
          source: prop.source,
          sourceUrl: prop.sourceUrl
        });
      }
    }
    if (props.length < 2) return null;
    // Trier par longueur de texte pour varier (plus long = plus détaillé)
    props.sort(function (a, b) { return b.texte.length - a.texte.length; });
    // Prendre les 2 plus différents (premier et dernier)
    return { a: props[0], b: props[props.length - 1] };
  }

  function genererQuestions(donneesElection, mode) {
    var candidats = donneesElection.candidats;
    var categories = donneesElection.categories;
    var tous = [];

    // Calculer la clivance de chaque sous-thème
    for (var c = 0; c < categories.length; c++) {
      var cat = categories[c];
      for (var s = 0; s < cat.sousThemes.length; s++) {
        var st = cat.sousThemes[s];
        var cliv = calculerClivance(st, candidats);
        if (cliv === 0) continue;
        var texte = trouverTexteQuestion(st, candidats);
        if (!texte) continue;
        tous.push({
          categorieId: cat.id,
          categorieNom: cat.nom,
          sousThemeId: st.id,
          sousThemeNom: st.nom,
          texte: texte,
          clivance: cliv,
          type: "classique" // sera changé en "duel" pour les priorités Expert
        });
      }
    }

    // Trier par clivance décroissante
    tous.sort(function (a, b) { return b.clivance - a.clivance; });

    if (mode === "express") {
      return tous.slice(0, Math.min(10, tous.length));
    }

    // Mode expert : 2 par catégorie + 1 bonus
    var parCategorie = {};
    for (var i = 0; i < tous.length; i++) {
      var q = tous[i];
      if (!parCategorie[q.categorieId]) {
        parCategorie[q.categorieId] = [];
      }
      parCategorie[q.categorieId].push(q);
    }

    var selection = [];
    var utilises = {};
    for (var k = 0; k < ORDRE_CATEGORIES.length; k++) {
      var catId = ORDRE_CATEGORIES[k];
      var qCat = parCategorie[catId] || [];
      for (var j = 0; j < Math.min(2, qCat.length); j++) {
        selection.push(qCat[j]);
        utilises[qCat[j].sousThemeId] = true;
      }
    }

    for (var m = 0; m < tous.length && selection.length < 25; m++) {
      if (!utilises[tous[m].sousThemeId]) {
        selection.push(tous[m]);
        utilises[tous[m].sousThemeId] = true;
      }
    }

    return selection;
  }

  // Convertir des questions classiques en duels pour les thèmes prioritaires
  function genererDuels(questions, priorites, donneesElection) {
    var candidats = donneesElection.candidats;
    var duels = [];
    var questionsClassiques = [];

    for (var i = 0; i < questions.length; i++) {
      var q = questions[i];
      if (priorites.indexOf(q.categorieId) !== -1) {
        // Essayer de créer un duel
        var found = trouverSousTheme(q.sousThemeId);
        if (found) {
          var duel = trouverDuel(found.sousTheme, candidats);
          if (duel) {
            duels.push({
              categorieId: q.categorieId,
              categorieNom: q.categorieNom,
              sousThemeId: q.sousThemeId,
              sousThemeNom: q.sousThemeNom,
              type: "duel",
              duel: duel
            });
            continue;
          }
        }
      }
      questionsClassiques.push(q);
    }

    return { classiques: questionsClassiques, duels: duels };
  }

  // === Scoring ===
  function calculerResultats(questions, reponses, duels, reponsesDuels, donneesElection, priorites) {
    var candidats = donneesElection.candidats;
    var categories = donneesElection.categories;

    // Pré-calculer les catégories couvertes par chaque candidat
    var categoriesCouvertes = {};
    for (var ci = 0; ci < candidats.length; ci++) {
      var cId = candidats[ci].id;
      categoriesCouvertes[cId] = {};
      for (var cc = 0; cc < categories.length; cc++) {
        var cat = categories[cc];
        for (var ss = 0; ss < cat.sousThemes.length; ss++) {
          if (cat.sousThemes[ss].propositions[cId] != null) {
            categoriesCouvertes[cId][cat.id] = true;
            break;
          }
        }
      }
    }

    // Calculer le score de chaque candidat
    var classement = [];
    for (var i = 0; i < candidats.length; i++) {
      var candidat = candidats[i];
      var score = 0;
      var maxPossible = 0;

      // Score des questions classiques
      for (var q = 0; q < questions.length; q++) {
        var question = questions[q];
        var reponse = reponses[question.sousThemeId];
        if (reponse == null) reponse = 0;
        if (reponse === 0) continue;
        if (!categoriesCouvertes[candidat.id][question.categorieId]) continue;

        var aProposition = false;
        for (var kk = 0; kk < categories.length; kk++) {
          if (categories[kk].id === question.categorieId) {
            for (var ll = 0; ll < categories[kk].sousThemes.length; ll++) {
              if (categories[kk].sousThemes[ll].id === question.sousThemeId) {
                aProposition = categories[kk].sousThemes[ll].propositions[candidat.id] != null;
                break;
              }
            }
            break;
          }
        }

        var poids = 1;
        if (etat.mode === "expert" && priorites.indexOf(question.categorieId) !== -1) {
          poids = 2;
        }

        if ((reponse === 1 && aProposition) || (reponse === -1 && !aProposition)) {
          score += poids;
        }
        maxPossible += poids;
      }

      // Score des duels
      for (var d = 0; d < duels.length; d++) {
        var duel = duels[d];
        var choix = reponsesDuels[duel.sousThemeId];
        if (!choix) continue;
        if (!categoriesCouvertes[candidat.id][duel.categorieId]) continue;

        var poidsDuel = 4; // duels = poids x4 (thèmes prioritaires, confrontation directe)
        if (choix === candidat.id) {
          score += poidsDuel;
        }
        maxPossible += poidsDuel;
      }

      var pourcentage = maxPossible > 0 ? Math.round((score / maxPossible) * 100) : 0;

      // Indice de fiabilité : combien de questions le candidat a couvertes
      var totalQuestions = questions.length + duels.length;
      var questionsRepondues = 0;
      for (var qf = 0; qf < questions.length; qf++) {
        if (categoriesCouvertes[candidat.id][questions[qf].categorieId]) {
          questionsRepondues++;
        }
      }
      for (var df = 0; df < duels.length; df++) {
        if (categoriesCouvertes[candidat.id][duels[df].categorieId]) {
          questionsRepondues++;
        }
      }
      var fiabilite = totalQuestions > 0 ? Math.round((questionsRepondues / totalQuestions) * 100) : 0;

      classement.push({
        candidat: candidat,
        index: i,
        score: score,
        maxPossible: maxPossible,
        pourcentage: pourcentage,
        fiabilite: fiabilite,
        couleur: getCouleurParti(candidat, i)
      });
    }

    classement.sort(function (a, b) { return b.pourcentage - a.pourcentage; });

    return { classement: classement };
  }

  // === Rendu UI ===
  function afficherPhase(phase) {
    etat.phase = phase;
    var sections = ["sim-selection", "sim-mode", "sim-questions", "sim-priorites", "sim-resultats"];
    for (var i = 0; i < sections.length; i++) {
      var el = document.getElementById(sections[i]);
      if (el) el.hidden = true;
    }
    var target = document.getElementById("sim-" + phase);
    if (target) target.hidden = false;

    // Stepper : visible seulement pendant les questions
    var stepper = document.getElementById("sim-stepper");
    if (stepper) {
      stepper.hidden = (phase !== "questions");
    }

    // Hero search : visible en sélection et mode, caché pendant les questions/résultats
    var heroSearch = document.getElementById("sim-hero-search");
    if (heroSearch) {
      heroSearch.hidden = (phase === "questions" || phase === "priorites" || phase === "resultats");
    }

    if (phase === "resultats" && etat.donneesElection) {
      document.title = "R\u00e9sultats \u2014 Simulateur " + etat.donneesElection.ville + " 2026 : Quel candidat vous correspond ? | #POURQUITUVOTES";
    } else if (etat.donneesElection) {
      document.title = "Simulateur " + etat.donneesElection.ville + " 2026 : Quel candidat vous correspond ? | #POURQUITUVOTES";
    }

    window.scrollTo(0, 0);
  }

  // === SEO dynamique ===
  function mettreAJourSEO(ville, nbCandidats) {
    // Title
    document.title = "Simulateur " + ville + " 2026 : Quel candidat vous correspond ? | #POURQUITUVOTES";
    // Meta description
    var metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute("content",
        "Faites le test pour les \u00e9lections municipales de " + ville +
        ". Comparez les propositions des " + nbCandidats +
        " candidats sur vos th\u00e8mes prioritaires. 100% anonyme et gratuit.");
    }
    // OG
    var ogTitle = document.querySelector('meta[property="og:title"]');
    if (ogTitle) ogTitle.setAttribute("content", "Simulateur de convictions \u2014 " + ville + " 2026 | #POURQUITUVOTES");
    var ogDesc = document.querySelector('meta[property="og:description"]');
    if (ogDesc) ogDesc.setAttribute("content", "Quel candidat vous correspond \u00e0 " + ville + " ? Faites le quiz en 5 min.");
    // Twitter
    var twTitle = document.querySelector('meta[name="twitter:title"]');
    if (twTitle) twTitle.setAttribute("content", "Simulateur de convictions \u2014 " + ville + " 2026 | #POURQUITUVOTES");
    var twDesc = document.querySelector('meta[name="twitter:description"]');
    if (twDesc) twDesc.setAttribute("content", "Quel candidat vous correspond \u00e0 " + ville + " ? Faites le quiz en 5 min.");
  }

  // === Hero dynamique ===
  function mettreAJourHero(ville) {
    var titleEl = document.getElementById("sim-hero-title");
    var subtitleEl = document.getElementById("sim-hero-subtitle");

    if (titleEl) {
      titleEl.textContent = "Simulateur de convictions\u00a0: pour qui voter \u00e0 " + ville + "\u00a0?";
    }
    if (subtitleEl) {
      subtitleEl.textContent = "D\u00e9couvrez quel candidat aux municipales de " + ville +
        " correspond le mieux \u00e0 vos valeurs en r\u00e9pondant \u00e0 10 questions cl\u00e9s.";
    }
  }

  // === Stepper ===
  function creerStepper(total) {
    var container = document.getElementById("sim-stepper-inner");
    if (!container) return;
    container.innerHTML = "";
    for (var i = 0; i < total; i++) {
      if (i > 0) {
        var line = document.createElement("div");
        line.className = "sim-stepper__line";
        line.id = "sim-stepper-line-" + i;
        container.appendChild(line);
      }
      var step = document.createElement("div");
      step.className = "sim-stepper__step";
      step.id = "sim-stepper-step-" + i;
      step.textContent = (i + 1);
      container.appendChild(step);
    }
  }

  function mettreAJourStepper(idx) {
    var allQuestions = etat.questions.concat(etat.duels);
    var total = allQuestions.length;
    for (var i = 0; i < total; i++) {
      var step = document.getElementById("sim-stepper-step-" + i);
      var line = document.getElementById("sim-stepper-line-" + i);
      if (!step) continue;
      step.className = "sim-stepper__step";
      if (i < idx) {
        step.classList.add("sim-stepper__step--done");
        step.innerHTML = '<i class="ph ph-check"></i>';
      } else if (i === idx) {
        step.classList.add("sim-stepper__step--active");
        step.textContent = (i + 1);
      } else {
        step.textContent = (i + 1);
      }
      if (line) {
        line.className = "sim-stepper__line" + (i <= idx ? " sim-stepper__line--done" : "");
      }
    }
  }

  // Helper: texte avec accordéon si > 200 caractères
  function rendreTexteAccordeon(texte, id) {
    var texteEchappe = echapper(texte);
    if (texte.length <= 200) {
      return '<span class="sim-texte-complet">' + texteEchappe + '</span>';
    }
    var court = echapper(texte.substring(0, 197)) + "...";
    return '<span class="sim-texte-court" id="' + id + '-court">' + court +
      ' <button class="sim-lire-suite" data-target="' + id + '">Lire la suite</button></span>' +
      '<span class="sim-texte-complet" id="' + id + '-complet" hidden>' + texteEchappe +
      ' <button class="sim-lire-suite" data-target="' + id + '" data-action="replier">Replier</button></span>';
  }

  // Délégation globale pour les boutons "Lire la suite / Replier"
  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".sim-lire-suite");
    if (!btn) return;
    var targetId = btn.getAttribute("data-target");
    var court = document.getElementById(targetId + "-court");
    var complet = document.getElementById(targetId + "-complet");
    if (court && complet) {
      var showing = !complet.hidden;
      court.hidden = !showing;
      complet.hidden = showing;
    }
  });

  // --- Sélection ville ---
  function initSelection() {
    var input = document.getElementById("sim-ville-search");
    var suggestionsEl = document.getElementById("sim-ville-suggestions");
    if (!input || !suggestionsEl) return;

    input.addEventListener("input", function () {
      var val = input.value.trim().toLowerCase();
      suggestionsEl.innerHTML = "";
      if (val.length < 1) {
        suggestionsEl.hidden = true;
        return;
      }

      var resultats = [];
      for (var i = 0; i < villesData.length; i++) {
        var v = villesData[i];
        if (v.nom.toLowerCase().indexOf(val) !== -1) {
          resultats.push(v);
        }
      }

      if (resultats.length === 0) {
        suggestionsEl.hidden = true;
        return;
      }

      for (var j = 0; j < Math.min(resultats.length, 8); j++) {
        var v2 = resultats[j];
        var div = document.createElement("div");
        div.className = "sim-selection__suggestion";
        var nbCandidats = v2.stats ? v2.stats.candidats : (v2.candidats ? v2.candidats.length : 0);
        div.innerHTML = '<span class="sim-selection__suggestion-ville">' + echapper(v2.nom) + '</span>' +
          '<span class="sim-selection__suggestion-count">' + nbCandidats + ' candidats</span>';
        div.setAttribute("data-id", v2.id);
        div.addEventListener("click", (function (ville) {
          return function () { selectionnerVille(ville); };
        })(v2));
        suggestionsEl.appendChild(div);
      }
      suggestionsEl.hidden = false;
    });

    document.addEventListener("click", function (e) {
      if (!input.contains(e.target) && !suggestionsEl.contains(e.target)) {
        suggestionsEl.hidden = true;
      }
    });
  }

  function selectionnerVille(ville) {
    etat.ville = ville.nom;
    etat.villeId = ville.id;
    document.getElementById("sim-ville-search").value = ville.nom;
    document.getElementById("sim-ville-suggestions").hidden = true;

    var fichier = (ville.elections && ville.elections[0]) || (ville.id + "-2026");
    chargerDonneesElection(fichier).then(function (data) {
      etat.donneesElection = data;

      data.categories.sort(function (a, b) {
        var idxA = ORDRE_CATEGORIES.indexOf(a.id);
        var idxB = ORDRE_CATEGORIES.indexOf(b.id);
        if (idxA === -1) idxA = 999;
        if (idxB === -1) idxB = 999;
        return idxA - idxB;
      });

      // Mettre à jour le hero et le SEO
      var nbCandidats = data.candidats ? data.candidats.length : 0;
      mettreAJourHero(data.ville);
      mettreAJourSEO(data.ville, nbCandidats);

      if (!data.candidats || data.candidats.length === 0) {
        var container = document.getElementById("sim-mode");
        container.innerHTML = '<div class="sim-empty">' +
          '<div class="sim-empty__icon"><i class="ph ph-calendar-blank" style="font-size:2.5rem"></i></div>' +
          '<p class="sim-empty__text">Aucun candidat officiel pour ' + echapper(data.ville) + ' pour le moment.</p>' +
          '<p>Les candidats seront affich\u00e9s d\u00e8s leur d\u00e9claration officielle.</p>' +
          '<button class="sim-mode__back" onclick="window.simRetourSelection()"><i class="ph ph-arrow-left"></i> Choisir une autre ville</button>' +
          '</div>';
        afficherPhase("mode");
        return;
      }

      // Garde : un seul candidat
      if (data.candidats.length === 1) {
        var container2 = document.getElementById("sim-mode");
        container2.innerHTML = '<div class="sim-empty">' +
          '<div class="sim-empty__icon">\ud83e\udd37</div>' +
          '<p class="sim-empty__text">Un seul candidat est list\u00e9 pour ' + echapper(data.ville) + '.</p>' +
          '<p>Le simulateur n\u2019est pas n\u00e9cessaire avec un seul candidat. ' +
          '<a href="/municipales/2026/?ville=' + encodeURIComponent(etat.villeId) + '">Consultez directement son programme</a>.</p>' +
          '<button class="sim-mode__back" onclick="window.simRetourSelection()"><i class="ph ph-arrow-left"></i> Choisir une autre ville</button>' +
          '</div>';
        afficherPhase("mode");
        return;
      }

      rendreChoixMode();
      afficherPhase("mode");

      var url = new URL(window.location);
      url.searchParams.set("ville", ville.id);
      window.history.replaceState({}, "", url);
    }).catch(function (err) {
      console.error("Erreur chargement:", err);
    });
  }

  // --- Choix du mode ---
  function rendreChoixMode() {
    var ville = echapper(etat.donneesElection.ville);
    var nbCandidats = etat.donneesElection.candidats.length;
    var container = document.getElementById("sim-mode");
    container.innerHTML =
      '<h2 class="sim-mode__title">Choisissez votre mode</h2>' +
      '<p class="sim-mode__ville">' + ville + ' \u2014 ' + nbCandidats + ' candidats</p>' +
      '<div class="sim-mode__grid">' +
        '<div class="sim-mode__card sim-mode__card--express" id="sim-btn-express">' +
          '<span class="sim-mode__card-icon"><i class="ph ph-lightning"></i></span>' +
          '<div class="sim-mode__card-title">Test Express</div>' +
          '<div class="sim-mode__card-desc">10 questions sur les sujets les plus clivants</div>' +
          '<span class="sim-mode__card-badge">~ 2 min</span>' +
        '</div>' +
        '<div class="sim-mode__card sim-mode__card--expert" id="sim-btn-expert">' +
          '<span class="sim-mode__card-icon"><i class="ph ph-chart-bar"></i></span>' +
          '<div class="sim-mode__card-title">Analyse Compl\u00e8te</div>' +
          '<div class="sim-mode__card-desc">25 questions + duels de propositions sur vos priorit\u00e9s</div>' +
          '<span class="sim-mode__card-badge">~ 5 min</span>' +
        '</div>' +
      '</div>' +
      '<button class="sim-mode__back" id="sim-mode-back"><i class="ph ph-arrow-left"></i> Changer de ville</button>';

    document.getElementById("sim-btn-express").addEventListener("click", function () {
      lancerQuiz("express");
    });
    document.getElementById("sim-btn-expert").addEventListener("click", function () {
      lancerQuiz("expert");
    });
    document.getElementById("sim-mode-back").addEventListener("click", function () {
      afficherPhase("selection");
    });
  }

  window.simRetourSelection = function () {
    var titleEl = document.getElementById("sim-hero-title");
    var subtitleEl = document.getElementById("sim-hero-subtitle");
    if (titleEl) titleEl.textContent = "Simulateur de convictions\u00a0: pour qui voter\u00a0?";
    if (subtitleEl) subtitleEl.textContent = "Comparez vos id\u00e9es aux programmes r\u00e9els des candidats en moins de 5 minutes.";
    document.title = "Simulateur de convictions \u2014 Municipales 2026 | #POURQUITUVOTES";
    afficherPhase("selection");
  };

  // --- Quiz ---
  function lancerQuiz(mode) {
    etat.mode = mode;
    etat.questions = genererQuestions(etat.donneesElection, mode);
    etat.duels = [];
    etat.reponses = {};
    etat.reponsesDuels = {};
    etat.questionCourante = 0;
    etat.priorites = [];

    if (etat.questions.length === 0) {
      var container = document.getElementById("sim-questions");
      container.innerHTML = '<div class="sim-empty">' +
        '<div class="sim-empty__icon"><i class="ph ph-chat-dots" style="font-size:2.5rem"></i></div>' +
        '<p class="sim-empty__text">Pas assez de propositions pour g\u00e9n\u00e9rer un quiz.</p>' +
        '<button class="sim-mode__back" onclick="window.simRetourSelection()"><i class="ph ph-arrow-left"></i> Retour</button>' +
        '</div>';
      afficherPhase("questions");
      return;
    }

    // Créer le stepper
    creerStepper(etat.questions.length);

    rendreQuestion(0);
    afficherPhase("questions");

    // Analytics
    if (window.PQTV_Analytics) {
      PQTV_Analytics.trackQuizStart(etat.donneesElection.ville, mode);
    }
  }

  function rendreQuestion(idx) {
    var container = document.getElementById("sim-questions");
    var allQuestions = etat.questions.concat(etat.duels);
    var total = allQuestions.length;
    var q = allQuestions[idx];
    var pct = Math.round((idx / total) * 100);
    var picto = PICTOS[q.categorieId] || "\ud83d\udccb";

    // Mettre à jour le stepper
    mettreAJourStepper(idx);

    var html = '<div class="sim-progress"><div class="sim-progress__bar" style="width:' + pct + '%"></div></div>' +
      '<div class="sim-progress__text">Question ' + (idx + 1) + ' / ' + total + '</div>';

    if (q.type === "duel") {
      // Duel de propositions
      html += '<div class="sim-question">' +
        '<span class="sim-question__badge">' + picto + ' ' + echapper(q.categorieNom) + ' \u2014 Duel</span>' +
        '<p class="sim-question__hint">Sur le th\u00e8me <strong>' + echapper(q.sousThemeNom) + '</strong>, quelle approche pr\u00e9f\u00e9rez-vous ?</p>' +
        '<div class="sim-duel">' +
          '<div class="sim-duel__card" data-candidat="' + q.duel.a.candidatId + '" id="sim-duel-a">' +
            '<div class="sim-duel__label">Proposition A</div>' +
            '<div class="sim-duel__texte">\u00ab ' + rendreTexteAccordeon(q.duel.a.texte, "duel-a-" + idx) + ' \u00bb</div>' +
          '</div>' +
          '<div class="sim-duel__vs">VS</div>' +
          '<div class="sim-duel__card" data-candidat="' + q.duel.b.candidatId + '" id="sim-duel-b">' +
            '<div class="sim-duel__label">Proposition B</div>' +
            '<div class="sim-duel__texte">\u00ab ' + rendreTexteAccordeon(q.duel.b.texte, "duel-b-" + idx) + ' \u00bb</div>' +
          '</div>' +
        '</div>' +
        '<div class="sim-question__nav">';
    } else {
      // Question classique
      html += '<div class="sim-question">' +
        '<span class="sim-question__badge">' + picto + ' ' + echapper(q.categorieNom) + '</span>' +
        '<div class="sim-question__texte">\u00ab ' + rendreTexteAccordeon(q.texte, "q-" + idx) + ' \u00bb</div>' +
        '<p class="sim-question__hint">Cette mesure figure dans au moins un programme. \u00cates-vous pour ou contre ?</p>' +
        '<div class="sim-question__actions">' +
          '<button class="sim-question__btn sim-question__btn--accord" data-valeur="1"><i class="ph ph-thumbs-up"></i> D\'accord</button>' +
          '<button class="sim-question__btn sim-question__btn--neutre" data-valeur="0"><i class="ph ph-minus"></i> Neutre</button>' +
          '<button class="sim-question__btn sim-question__btn--contre" data-valeur="-1"><i class="ph ph-thumbs-down"></i> Pas d\'accord</button>' +
        '</div>' +
        '<div class="sim-question__nav">';
    }

    if (idx > 0) {
      html += '<button class="sim-question__nav-btn" id="sim-precedent"><i class="ph ph-arrow-left"></i> Pr\u00e9c\u00e9dente</button>';
    }

    if (etat.mode === "expert" && idx >= 11) {
      html += '<button class="sim-question__nav-btn sim-question__nav-btn--escape" id="sim-escape">' +
        '<i class="ph ph-flag-checkered"></i> Voir mes r\u00e9sultats partiels</button>';
    }

    html += '</div></div>';
    container.innerHTML = html;

    // Listeners
    if (q.type === "duel") {
      var cards = container.querySelectorAll(".sim-duel__card");
      for (var ci = 0; ci < cards.length; ci++) {
        cards[ci].addEventListener("click", function () {
          var candidatId = this.getAttribute("data-candidat");
          repondreDuel(candidatId);
        });
      }
    } else {
      var btns = container.querySelectorAll(".sim-question__btn");
      for (var i = 0; i < btns.length; i++) {
        btns[i].addEventListener("click", function () {
          repondre(parseInt(this.getAttribute("data-valeur")));
        });
      }
    }

    var btnPrec = document.getElementById("sim-precedent");
    if (btnPrec) {
      btnPrec.addEventListener("click", function () {
        etat.questionCourante--;
        rendreQuestion(etat.questionCourante);
      });
    }

    var btnEscape = document.getElementById("sim-escape");
    if (btnEscape) {
      btnEscape.addEventListener("click", function () {
        terminerQuiz();
      });
    }
  }

  function repondre(valeur) {
    var allQuestions = etat.questions.concat(etat.duels);
    var q = allQuestions[etat.questionCourante];
    etat.reponses[q.sousThemeId] = valeur;
    avancerQuestion();
  }

  function repondreDuel(candidatId) {
    var allQuestions = etat.questions.concat(etat.duels);
    var q = allQuestions[etat.questionCourante];
    etat.reponsesDuels[q.sousThemeId] = candidatId;
    avancerQuestion();
  }

  function avancerQuestion() {
    etat.questionCourante++;
    var allQuestions = etat.questions.concat(etat.duels);

    if (etat.questionCourante >= allQuestions.length) {
      if (etat.mode === "expert" && etat.duels.length === 0 && etat.priorites.length === 0) {
        // Pas encore passé par les priorités
        rendrePriorites();
        afficherPhase("priorites");
      } else {
        terminerQuiz();
      }
    } else {
      rendreQuestion(etat.questionCourante);
    }
  }

  // --- Pondération (Expert) ---
  function rendrePriorites() {
    var container = document.getElementById("sim-priorites");
    etat.priorites = [];

    var html = '<h2 class="sim-priorites__title">Quelles sont vos priorit\u00e9s ?</h2>' +
      '<p class="sim-priorites__subtitle">S\u00e9lectionnez 3 th\u00e8mes qui comptent le plus pour vous. Vous d\u00e9partagerez les candidats sur ces sujets via des duels de propositions.</p>' +
      '<p class="sim-priorites__counter"><strong id="sim-prio-count">0</strong> / 3 s\u00e9lectionn\u00e9s</p>' +
      '<div class="sim-priorites__grid">';

    for (var i = 0; i < ORDRE_CATEGORIES.length; i++) {
      var catId = ORDRE_CATEGORIES[i];
      var picto = PICTOS[catId] || "\ud83d\udccb";
      var catNom = catId.charAt(0).toUpperCase() + catId.slice(1);
      for (var c = 0; c < etat.donneesElection.categories.length; c++) {
        if (etat.donneesElection.categories[c].id === catId) {
          catNom = etat.donneesElection.categories[c].nom;
          break;
        }
      }
      var nomCourt = catNom.split(" & ")[0].split(" et ")[0];

      html += '<div class="sim-priorites__item" data-cat="' + catId + '">' +
        '<span class="sim-priorites__item-icon">' + picto + '</span>' +
        '<span class="sim-priorites__item-name">' + echapper(nomCourt) + '</span>' +
        '</div>';
    }

    html += '</div>' +
      '<button class="sim-priorites__btn" id="sim-prio-valider" disabled>Passer aux duels</button>' +
      '<button class="sim-mode__back" id="sim-prio-skip" style="display:block;margin:0.5rem auto 0"><i class="ph ph-arrow-right"></i> Passer sans duels (pond\u00e9ration simple)</button>';

    container.innerHTML = html;

    var items = container.querySelectorAll(".sim-priorites__item");
    for (var j = 0; j < items.length; j++) {
      items[j].addEventListener("click", function () {
        var catId2 = this.getAttribute("data-cat");
        var idx = etat.priorites.indexOf(catId2);
        if (idx !== -1) {
          etat.priorites.splice(idx, 1);
          this.classList.remove("sim-priorites__item--selected");
        } else if (etat.priorites.length < 3) {
          etat.priorites.push(catId2);
          this.classList.add("sim-priorites__item--selected");
        }
        document.getElementById("sim-prio-count").textContent = etat.priorites.length;
        document.getElementById("sim-prio-valider").disabled = etat.priorites.length !== 3;
      });
    }

    document.getElementById("sim-prio-valider").addEventListener("click", function () {
      lancerDuels();
    });

    document.getElementById("sim-prio-skip").addEventListener("click", function () {
      etat.priorites = [];
      etat.duels = [];
      terminerQuiz();
    });
  }

  function lancerDuels() {
    var resultat = genererDuels(etat.questions, etat.priorites, etat.donneesElection);
    etat.questions = resultat.classiques;
    etat.duels = resultat.duels;

    if (etat.duels.length === 0) {
      terminerQuiz();
      return;
    }

    // Recréer le stepper avec le total combiné (classiques + duels)
    creerStepper(etat.questions.length + etat.duels.length);

    // Reprendre à la première question duel (après les classiques)
    etat.questionCourante = etat.questions.length;
    rendreQuestion(etat.questionCourante);
    afficherPhase("questions");
  }

  // --- Résultats ---
  function terminerQuiz() {
    etat.resultats = calculerResultats(
      etat.questions, etat.reponses, etat.duels, etat.reponsesDuels,
      etat.donneesElection, etat.priorites
    );
    rendreResultats();
    afficherPhase("resultats");

    // Analytics
    if (window.PQTV_Analytics && etat.resultats.classement.length > 0) {
      var top = etat.resultats.classement[0];
      PQTV_Analytics.trackQuizResult(
        etat.donneesElection.ville, etat.mode,
        top.candidat.nom, top.pourcentage,
        etat.resultats.classement,
        Object.keys(etat.reponses).length
      );
    }
  }

  function rendreResultats() {
    var container = document.getElementById("sim-resultats");
    var res = etat.resultats;
    var classement = res.classement;

    var html = '<h2 class="sim-resultats__title">Vos r\u00e9sultats</h2>' +
      '<p class="sim-resultats__subtitle">' + echapper(etat.donneesElection.ville) + ' \u2014 Mode ' +
      (etat.mode === "express" ? "Express" : "Expert") + '</p>';

    // Podium — noms cliquables + indice de fiabilité
    html += '<div class="sim-podium">';
    for (var i = 0; i < classement.length; i++) {
      var c = classement[i];
      var rang = i + 1;
      var lienComparateur = '/municipales/2026/?ville=' + encodeURIComponent(etat.villeId) +
        '&candidats=' + encodeURIComponent(c.candidat.id);

      // Badge fiabilité si < 50%
      var badgeFiabilite = '';
      if (c.fiabilite < 50) {
        badgeFiabilite = '<span class="sim-podium__fiabilite sim-podium__fiabilite--low" title="Ce candidat n\u2019a r\u00e9pondu qu\u2019\u00e0 ' + c.fiabilite + '% des th\u00e8mes du quiz"><i class="ph ph-warning"></i> Donn\u00e9es partielles (' + c.fiabilite + '%)</span>';
      } else {
        badgeFiabilite = '<span class="sim-podium__fiabilite" title="Ce candidat couvre ' + c.fiabilite + '% des th\u00e8mes du quiz"><i class="ph ph-check-circle" style="color:#10b981"></i> ' + c.fiabilite + '% couvert</span>';
      }

      html += '<div class="sim-podium__item sim-podium__item--' + rang + '" style="--couleur-candidat:' + c.couleur + '">' +
        '<span class="sim-podium__rank">#' + rang + '</span>' +
        '<div class="sim-podium__info">' +
          '<a class="sim-podium__nom" href="' + lienComparateur + '">' + echapper(c.candidat.nom) + '</a>' +
          '<div class="sim-podium__liste">' + echapper(c.candidat.liste || "") + '</div>' +
          badgeFiabilite +
        '</div>' +
        '<div class="sim-podium__bar-wrap"><div class="sim-podium__bar" style="width:' + c.pourcentage + '%"></div></div>' +
        '<span class="sim-podium__pct">' + c.pourcentage + '%</span>' +
      '</div>';
    }
    html += '</div>';

    // === RÉCAPITULATIF DÉTAILLÉ : "Détail de vos affinités" ===
    html += rendreRecapitulatif();

    // Partage social
    var textePartage = genererTextePartage();
    html += '<div class="sim-share">' +
      '<h3 class="sim-share__title">Partagez vos r\u00e9sultats</h3>' +
      '<div class="sim-share__text">' + echapper(textePartage) + '</div>' +
      '<div class="sim-share__buttons">' +
        '<button class="sim-share__btn sim-share__btn--twitter" id="sim-share-twitter"><i class="ph ph-x-logo"></i> Twitter</button>' +
        '<button class="sim-share__btn sim-share__btn--facebook" id="sim-share-facebook"><i class="ph ph-facebook-logo"></i> Facebook</button>' +
        '<button class="sim-share__btn sim-share__btn--whatsapp" id="sim-share-whatsapp"><i class="ph ph-whatsapp-logo"></i> WhatsApp</button>' +
        '<button class="sim-share__btn sim-share__btn--copy" id="sim-share-copy"><i class="ph ph-link"></i> Copier le lien</button>' +
      '</div>' +
    '</div>';

    // CTA
    html += '<div class="sim-cta">' +
      '<a class="sim-cta__btn sim-cta__btn--primary" href="/municipales/2026/?ville=' +
        encodeURIComponent(etat.villeId) + '&candidats=' + encodeURIComponent(classement.slice(0, 3).map(function(cc) { return cc.candidat.id; }).join(",")) + '">' +
        '<i class="ph ph-chart-bar"></i> Comparer mon top 3</a>' +
      '<button class="sim-cta__btn sim-cta__btn--secondary" id="sim-refaire"><i class="ph ph-arrow-counter-clockwise"></i> Refaire le quiz</button>' +
    '</div>';

    container.innerHTML = html;

    document.getElementById("sim-share-twitter").addEventListener("click", function () {
      partagerTwitter(textePartage);
    });
    document.getElementById("sim-share-facebook").addEventListener("click", function () {
      partagerFacebook();
    });
    document.getElementById("sim-share-whatsapp").addEventListener("click", function () {
      partagerWhatsApp(textePartage);
    });
    document.getElementById("sim-share-copy").addEventListener("click", function () {
      copierLien(this);
    });
    document.getElementById("sim-refaire").addEventListener("click", function () {
      rendreChoixMode();
      afficherPhase("mode");
    });
  }

  // --- Récapitulatif détaillé ---
  function rendreRecapitulatif() {
    var html = '<div class="sim-recap">' +
      '<h3 class="sim-recap__title"><i class="ph ph-list-checks"></i> D\u00e9tail de vos affinit\u00e9s</h3>' +
      '<p class="sim-recap__subtitle">Cat\u00e9gorie, proposition int\u00e9grale, votre r\u00e9ponse, et le candidat r\u00e9v\u00e9l\u00e9.</p>';

    // Questions classiques
    for (var i = 0; i < etat.questions.length; i++) {
      var q = etat.questions[i];
      var reponse = etat.reponses[q.sousThemeId];
      var picto = PICTOS[q.categorieId] || "\ud83d\udccb";
      var auteur = trouverAuteurQuestion(q);

      var badgeClass, badgeText;
      if (reponse === 1) {
        badgeClass = "sim-recap__badge--accord";
        badgeText = "D'accord";
      } else if (reponse === -1) {
        badgeClass = "sim-recap__badge--contre";
        badgeText = "Pas d'accord";
      } else {
        badgeClass = "sim-recap__badge--neutre";
        badgeText = "Neutre";
      }

      html += '<div class="sim-recap__item">' +
        '<div class="sim-recap__item-header">' +
          '<span class="sim-recap__cat">' + picto + ' ' + echapper(q.categorieNom) + '</span>' +
          '<span class="sim-recap__badge ' + badgeClass + '">' + badgeText + '</span>' +
        '</div>' +
        '<div class="sim-recap__proposition">\u00ab ' + rendreTexteAccordeon(q.texte, "recap-q-" + i) + ' \u00bb</div>';

      if (auteur) {
        var couleur = getCouleurParti(auteur.candidat, 0);
        var lienSource = '/municipales/2026/index.html?ville=' + encodeURIComponent(etat.villeId) +
          '&candidats=' + encodeURIComponent(auteur.candidat.id) + '#' + q.categorieId;
        html += '<div class="sim-recap__auteur">' +
          '<span class="sim-recap__auteur-dot" style="background:' + couleur + '"></span> ' +
          '<strong>' + echapper(auteur.candidat.nom) + '</strong>' +
          ' <span class="sim-recap__auteur-liste">(' + echapper(auteur.candidat.liste || "") + ')</span>' +
          ' <a class="sim-recap__source" href="' + lienSource + '">V\u00e9rifier la source <i class="ph ph-arrow-right"></i></a>' +
        '</div>';
      }

      // Lien vers le comparateur pour ce thème
      html += '<a class="sim-recap__verify" href="/municipales/2026/index.html?ville=' +
        encodeURIComponent(etat.villeId) + '#' + q.categorieId + '">Voir toutes les propositions sur ce th\u00e8me <i class="ph ph-arrow-right"></i></a>';

      html += '</div>';
    }

    // Duels
    for (var d = 0; d < etat.duels.length; d++) {
      var duel = etat.duels[d];
      var choix = etat.reponsesDuels[duel.sousThemeId];
      var pictoD = PICTOS[duel.categorieId] || "\ud83d\udccb";

      html += '<div class="sim-recap__item sim-recap__item--duel">' +
        '<div class="sim-recap__item-header">' +
          '<span class="sim-recap__cat">' + pictoD + ' ' + echapper(duel.categorieNom) + ' \u2014 Duel</span>' +
          '<span class="sim-recap__badge sim-recap__badge--duel"><i class="ph ph-sword"></i> Duel</span>' +
        '</div>' +
        '<div class="sim-recap__duel-pair">';

      // Proposition A
      var isChosenA = (choix === duel.duel.a.candidatId);
      var candidatA = null;
      for (var ca = 0; ca < etat.donneesElection.candidats.length; ca++) {
        if (etat.donneesElection.candidats[ca].id === duel.duel.a.candidatId) {
          candidatA = etat.donneesElection.candidats[ca];
          break;
        }
      }
      var couleurA = candidatA ? getCouleurParti(candidatA, 0) : "#94a3b8";

      var lienSourceA = '/municipales/2026/index.html?ville=' + encodeURIComponent(etat.villeId) +
        '&candidats=' + encodeURIComponent(duel.duel.a.candidatId) + '#' + duel.categorieId;
      html += '<div class="sim-recap__duel-card' + (isChosenA ? ' sim-recap__duel-card--chosen' : ' sim-recap__duel-card--rejected') + '">' +
        '<div class="sim-recap__duel-status">' + (isChosenA ? '<i class="ph ph-check-circle" style="color:#10b981"></i> Votre choix' : '<i class="ph ph-x-circle" style="color:#ef4444"></i> Rejet\u00e9') + '</div>' +
        '<div class="sim-recap__proposition">\u00ab ' + rendreTexteAccordeon(duel.duel.a.texte, "recap-da-" + d) + ' \u00bb</div>' +
        '<div class="sim-recap__auteur">' +
          '<span class="sim-recap__auteur-dot" style="background:' + couleurA + '"></span> ' +
          '<strong>' + echapper(duel.duel.a.candidatNom) + '</strong> ' +
          '<span class="sim-recap__auteur-liste">(' + echapper(duel.duel.a.candidatListe || "") + ')</span>' +
          ' <a class="sim-recap__source" href="' + lienSourceA + '">V\u00e9rifier <i class="ph ph-arrow-right"></i></a>' +
        '</div></div>';

      // Proposition B
      var isChosenB = (choix === duel.duel.b.candidatId);
      var candidatB = null;
      for (var cb = 0; cb < etat.donneesElection.candidats.length; cb++) {
        if (etat.donneesElection.candidats[cb].id === duel.duel.b.candidatId) {
          candidatB = etat.donneesElection.candidats[cb];
          break;
        }
      }
      var couleurB = candidatB ? getCouleurParti(candidatB, 0) : "#94a3b8";

      var lienSourceB = '/municipales/2026/index.html?ville=' + encodeURIComponent(etat.villeId) +
        '&candidats=' + encodeURIComponent(duel.duel.b.candidatId) + '#' + duel.categorieId;
      html += '<div class="sim-recap__duel-card' + (isChosenB ? ' sim-recap__duel-card--chosen' : ' sim-recap__duel-card--rejected') + '">' +
        '<div class="sim-recap__duel-status">' + (isChosenB ? '<i class="ph ph-check-circle" style="color:#10b981"></i> Votre choix' : '<i class="ph ph-x-circle" style="color:#ef4444"></i> Rejet\u00e9') + '</div>' +
        '<div class="sim-recap__proposition">\u00ab ' + rendreTexteAccordeon(duel.duel.b.texte, "recap-db-" + d) + ' \u00bb</div>' +
        '<div class="sim-recap__auteur">' +
          '<span class="sim-recap__auteur-dot" style="background:' + couleurB + '"></span> ' +
          '<strong>' + echapper(duel.duel.b.candidatNom) + '</strong> ' +
          '<span class="sim-recap__auteur-liste">(' + echapper(duel.duel.b.candidatListe || "") + ')</span>' +
          ' <a class="sim-recap__source" href="' + lienSourceB + '">V\u00e9rifier <i class="ph ph-arrow-right"></i></a>' +
        '</div></div>';

      html += '</div>' +
        '<a class="sim-recap__verify" href="/municipales/2026/index.html?ville=' +
          encodeURIComponent(etat.villeId) + '#' + duel.categorieId + '">Voir toutes les propositions <i class="ph ph-arrow-right"></i></a>' +
        '</div>';
    }

    html += '</div>';
    return html;
  }

  // (Radar supprimé — les résultats affichent directement le récapitulatif détaillé)

  // --- Partage social ---
  function genererTextePartage() {
    if (!etat.resultats || !etat.resultats.classement.length) return "";
    var top = etat.resultats.classement[0];
    return "Je matche \u00e0 " + top.pourcentage + "% avec " + top.candidat.nom +
      " sur #POURQUITUVOTES. Et vous ?";
  }

  function getShareUrl() {
    return "https://pourquituvotes.fr/municipales/2026/simulateur.html?ville=" + encodeURIComponent(etat.villeId);
  }

  function partagerTwitter(texte) {
    var url = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(texte) +
      "&url=" + encodeURIComponent(getShareUrl());
    window.open(url, "_blank", "noopener,noreferrer");
  }

  function partagerFacebook() {
    var url = "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(getShareUrl());
    window.open(url, "_blank", "noopener,noreferrer");
  }

  function partagerWhatsApp(texte) {
    var url = "https://wa.me/?text=" + encodeURIComponent(texte + " " + getShareUrl());
    window.open(url, "_blank", "noopener,noreferrer");
  }

  function copierLien(btn) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(getShareUrl()).then(function () {
        var oldHtml = btn.innerHTML;
        btn.innerHTML = '<i class="ph ph-check"></i> Copi\u00e9 !';
        setTimeout(function () { btn.innerHTML = oldHtml; }, 2000);
      });
    }
  }

  // --- Open Graph dynamique ---
  function mettreAJourOG() {
    if (!etat.resultats || !etat.resultats.classement.length) return;
    var top = etat.resultats.classement[0];
    var ogTitle = document.querySelector('meta[property="og:title"]');
    var ogDesc = document.querySelector('meta[property="og:description"]');
    if (ogTitle) ogTitle.setAttribute("content", "Je matche \u00e0 " + top.pourcentage + "% avec " + top.candidat.nom + " | #POURQUITUVOTES");
    if (ogDesc) ogDesc.setAttribute("content", "D\u00e9couvrez quel candidat correspond \u00e0 vos convictions pour les municipales 2026 \u00e0 " + etat.donneesElection.ville);
  }

  // === Initialisation ===
  function init() {
    chargerVilles().then(function () {
      initSelection();
      afficherPhase("selection");

      var params = new URLSearchParams(window.location.search);
      var villeParam = params.get("ville");
      var modeParam = params.get("mode");

      if (villeParam) {
        for (var i = 0; i < villesData.length; i++) {
          if (villesData[i].id === villeParam) {
            selectionnerVille(villesData[i]);
            if (modeParam === "express" || modeParam === "expert") {
              var checkReady = setInterval(function () {
                if (etat.donneesElection) {
                  clearInterval(checkReady);
                  lancerQuiz(modeParam);
                }
              }, 100);
            }
            break;
          }
        }
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
