(function () {
  "use strict";

  var EMAIL = "contact@pourquituvotes.fr";
  var villes = null;
  var villeChoisie = null;

  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
  function norm(s) { return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }

  // === Charger villes.json (une seule fois, au besoin) ===
  function loadVilles() {
    if (villes) return Promise.resolve(villes);
    return fetch("/data/villes.json?v=" + Date.now())
      .then(function (r) { return r.json(); })
      .then(function (d) { villes = d; return d; });
  }

  // === Templates ===
  var STEP_CHOIX =
    '<h2><i class="ph ph-hand-heart"></i> Comment souhaitez-vous contribuer\u00a0?</h2>' +
    '<div class="contribuer-choix">' +
      '<button type="button" class="contribuer-choix__card" data-type="erreur">' +
        '<i class="ph ph-warning-circle"></i>' +
        '<strong>Signaler une erreur</strong>' +
        '<span>Texte incorrect, source manquante, proposition mal class\u00e9e\u2026</span>' +
      '</button>' +
      '<button type="button" class="contribuer-choix__card" data-type="autre">' +
        '<i class="ph ph-chat-dots"></i>' +
        '<strong>Autre contribution</strong>' +
        '<span>Suggestion, partenariat, question, am\u00e9lioration\u2026</span>' +
      '</button>' +
    '</div>';

  var STEP_ERREUR =
    '<h2><i class="ph ph-warning-circle"></i> Signaler une erreur</h2>' +
    '<form id="contribuer-form">' +
      '<div class="contribuer-form__group contribuer-form__ac">' +
        '<label for="c-ville">Ville concern\u00e9e *</label>' +
        '<input type="text" id="c-ville" placeholder="Tapez pour rechercher\u2026" autocomplete="off" required>' +
        '<div class="contribuer-ac__list" id="c-ville-list" hidden></div>' +
      '</div>' +
      '<div class="contribuer-form__group contribuer-form__ac">' +
        '<label for="c-candidat">Candidat concern\u00e9</label>' +
        '<input type="text" id="c-candidat" placeholder="S\u00e9lectionnez d\u2019abord une ville" autocomplete="off" disabled>' +
        '<div class="contribuer-ac__list" id="c-candidat-list" hidden></div>' +
      '</div>' +
      '<div class="contribuer-form__group">' +
        '<label for="c-desc">Description de l\u2019erreur *</label>' +
        '<textarea id="c-desc" rows="4" placeholder="D\u00e9crivez ce qui est incorrect\u2026" required></textarea>' +
      '</div>' +
      '<div class="contribuer-form__group">' +
        '<label for="c-source">Source correcte (optionnel)</label>' +
        '<input type="url" id="c-source" placeholder="https://\u2026">' +
      '</div>' +
      '<div class="contribuer-form__group">' +
        '<label for="c-email">Votre email *</label>' +
        '<input type="email" id="c-email" placeholder="pour vous recontacter" required>' +
      '</div>' +
      '<div class="contribuer-form__actions">' +
        '<button type="button" class="contribuer-btn--back"><i class="ph ph-arrow-left"></i> Retour</button>' +
        '<button type="submit" class="contribuer-btn--send"><i class="ph ph-paper-plane-tilt"></i> Envoyer</button>' +
      '</div>' +
    '</form>';

  var STEP_AUTRE =
    '<h2><i class="ph ph-chat-dots"></i> Votre message</h2>' +
    '<form id="contribuer-form">' +
      '<div class="contribuer-form__group">' +
        '<label for="c-sujet">Sujet</label>' +
        '<select id="c-sujet">' +
          '<option value="Suggestion">Suggestion d\u2019am\u00e9lioration</option>' +
          '<option value="Question">Question sur le site</option>' +
          '<option value="Partenariat">Proposition de partenariat</option>' +
          '<option value="Autre">Autre</option>' +
        '</select>' +
      '</div>' +
      '<div class="contribuer-form__group">' +
        '<label for="c-msg">Votre message *</label>' +
        '<textarea id="c-msg" rows="5" placeholder="D\u00e9crivez votre id\u00e9e ou posez votre question\u2026" required></textarea>' +
      '</div>' +
      '<div class="contribuer-form__group">' +
        '<label for="c-email2">Votre email *</label>' +
        '<input type="email" id="c-email2" placeholder="pour vous recontacter" required>' +
      '</div>' +
      '<div class="contribuer-form__actions">' +
        '<button type="button" class="contribuer-btn--back"><i class="ph ph-arrow-left"></i> Retour</button>' +
        '<button type="submit" class="contribuer-btn--send"><i class="ph ph-paper-plane-tilt"></i> Envoyer</button>' +
      '</div>' +
    '</form>';

  // === Injection modale ===
  var shell =
    '<div id="modal-contribuer" class="modal" hidden>' +
      '<div class="modal__overlay"></div>' +
      '<div class="modal__contenu">' +
        '<button class="modal__fermer" aria-label="Fermer">&times;</button>' +
        '<div id="contribuer-body"></div>' +
      '</div>' +
    '</div>';

  var tmp = document.createElement("div");
  tmp.innerHTML = shell;
  document.body.appendChild(tmp.firstChild);

  var modal = document.getElementById("modal-contribuer");
  var bodyEl = document.getElementById("contribuer-body");

  function showStep(html) {
    bodyEl.innerHTML = html;
    villeChoisie = null;
  }

  function ouvrir(e) {
    e.preventDefault();
    showStep(STEP_CHOIX);
    modal.hidden = false;
    document.body.style.overflow = "hidden";
  }

  function fermer() {
    modal.hidden = true;
    document.body.style.overflow = "";
  }

  function buildMailto(subject, bodyText) {
    return "mailto:" + EMAIL +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(bodyText);
  }

  // === Autocomplétion ===
  function initAutocomplete() {
    var villeInput = document.getElementById("c-ville");
    var villeList = document.getElementById("c-ville-list");
    var candidatInput = document.getElementById("c-candidat");
    var candidatList = document.getElementById("c-candidat-list");
    if (!villeInput) return;

    var debounce = null;

    villeInput.addEventListener("input", function () {
      clearTimeout(debounce);
      var val = villeInput.value.trim();
      debounce = setTimeout(function () {
        if (!val || val.length < 2 || !villes) { villeList.hidden = true; return; }
        var t = norm(val);
        var results = villes.filter(function (v) {
          return norm(v.nom).indexOf(t) !== -1 || v.codePostal.indexOf(t) !== -1;
        }).slice(0, 8);
        if (results.length === 0) { villeList.hidden = true; return; }
        villeList.innerHTML = results.map(function (v) {
          return '<div class="contribuer-ac__item" data-id="' + v.id + '">' +
            '<span>' + esc(v.nom) + '</span><span class="contribuer-ac__cp">' + v.codePostal + '</span></div>';
        }).join("");
        villeList.hidden = false;
      }, 150);
    });

    villeList.addEventListener("click", function (e) {
      var item = e.target.closest(".contribuer-ac__item");
      if (!item) return;
      var v = villes.find(function (x) { return x.id === item.dataset.id; });
      if (!v) return;
      villeChoisie = v;
      villeInput.value = v.nom;
      villeList.hidden = true;
      // Activer candidat
      candidatInput.disabled = false;
      candidatInput.placeholder = "Tapez pour rechercher\u2026";
      candidatInput.value = "";
      candidatInput.focus();
    });

    if (candidatInput) {
      candidatInput.addEventListener("input", function () {
        clearTimeout(debounce);
        var val = candidatInput.value.trim();
        debounce = setTimeout(function () {
          if (!villeChoisie || !villeChoisie.candidats) { candidatList.hidden = true; return; }
          var cands = villeChoisie.candidats;
          if (val.length >= 1) {
            var t = norm(val);
            cands = cands.filter(function (c) { return norm(c.nom).indexOf(t) !== -1; });
          }
          cands = cands.slice(0, 10);
          if (cands.length === 0) { candidatList.hidden = true; return; }
          candidatList.innerHTML = cands.map(function (c) {
            return '<div class="contribuer-ac__item" data-id="' + c.id + '">' +
              '<span>' + esc(c.nom) + '</span></div>';
          }).join("");
          candidatList.hidden = false;
        }, 100);
      });

      candidatInput.addEventListener("focus", function () {
        if (villeChoisie && villeChoisie.candidats && !candidatInput.value) {
          candidatInput.dispatchEvent(new Event("input"));
        }
      });

      candidatList.addEventListener("click", function (e) {
        var item = e.target.closest(".contribuer-ac__item");
        if (!item) return;
        var c = villeChoisie.candidats.find(function (x) { return x.id === item.dataset.id; });
        if (c) candidatInput.value = c.nom;
        candidatList.hidden = true;
      });
    }

    // Fermer les listes au clic en dehors
    document.addEventListener("click", function (e) {
      if (!e.target.closest("#c-ville") && !e.target.closest("#c-ville-list")) villeList.hidden = true;
      if (candidatList && !e.target.closest("#c-candidat") && !e.target.closest("#c-candidat-list")) candidatList.hidden = true;
    });
  }

  // === Events ===
  document.addEventListener("click", function (e) {
    if (e.target.closest(".js-open-contribuer")) { ouvrir(e); return; }

    if (!e.target.closest("#modal-contribuer")) return;
    if (e.target.classList.contains("modal__overlay") || e.target.classList.contains("modal__fermer")) { fermer(); return; }

    var card = e.target.closest(".contribuer-choix__card");
    if (card) {
      if (card.dataset.type === "erreur") {
        loadVilles().then(function () {
          showStep(STEP_ERREUR);
          initAutocomplete();
        });
      } else {
        showStep(STEP_AUTRE);
      }
      return;
    }

    if (e.target.closest(".contribuer-btn--back")) { showStep(STEP_CHOIX); return; }
  });

  // Submit
  document.addEventListener("submit", function (e) {
    if (e.target.id !== "contribuer-form") return;
    e.preventDefault();

    var ville = document.getElementById("c-ville");
    var candidat = document.getElementById("c-candidat");
    var desc = document.getElementById("c-desc");
    var source = document.getElementById("c-source");
    var emailField = document.getElementById("c-email") || document.getElementById("c-email2");
    var sujet = document.getElementById("c-sujet");
    var msg = document.getElementById("c-msg");

    var subject, text;
    var userEmail = emailField ? emailField.value.trim() : "";

    if (ville) {
      subject = "Signalement \u2014 " + (ville.value || "");
      text = "Ville : " + (ville.value || "") + "\n";
      if (candidat && candidat.value) text += "Candidat : " + candidat.value + "\n";
      text += "\nDescription :\n" + (desc ? desc.value : "") + "\n";
      if (source && source.value) text += "\nSource correcte : " + source.value + "\n";
    } else {
      subject = sujet ? sujet.value : "Contact";
      text = msg ? msg.value : "";
    }

    if (userEmail) text += "\n\nEmail de contact : " + userEmail;
    text += "\n\n---\nEnvoy\u00e9 depuis " + location.href;

    window.location.href = buildMailto(subject, text);
    setTimeout(fermer, 300);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modal.hidden) fermer();
  });
})();
