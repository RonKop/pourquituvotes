/**
 * #POURQUITUVOTES — Module Analytics GA4
 * Tracking centralisé via dataLayer (GTM-T4CCTF6V)
 * Nomenclature : snake_case uniquement
 * PII : email haché SHA-256, jamais en clair
 */
(function () {
  "use strict";

  window.dataLayer = window.dataLayer || [];

  // === Helper principal ===
  function sendAnalyticsEvent(eventName, params) {
    var payload = { event: eventName };
    if (params) {
      for (var key in params) {
        if (params.hasOwnProperty(key)) {
          payload[key] = params[key];
        }
      }
    }
    window.dataLayer.push(payload);
  }

  // === SHA-256 hash (Web Crypto API) ===
  function hashEmail(email) {
    if (!email || !window.crypto || !window.crypto.subtle) return Promise.resolve(null);
    var normalized = email.trim().toLowerCase();
    var encoder = new TextEncoder();
    var data = encoder.encode(normalized);
    return window.crypto.subtle.digest("SHA-256", data).then(function (buffer) {
      var bytes = new Uint8Array(buffer);
      var hex = "";
      for (var i = 0; i < bytes.length; i++) {
        hex += bytes[i].toString(16).padStart(2, "0");
      }
      return hex;
    });
  }

  // === Suivi du temps ===
  var pageLoadTime = Date.now();
  function getTimeOnPage() {
    return Math.round((Date.now() - pageLoadTime) / 1000);
  }

  // === Page view ===
  sendAnalyticsEvent("page_view_custom", {
    page_path: location.pathname + location.search,
    page_title: document.title,
    referrer: document.referrer || "(direct)"
  });

  // === Suivi scroll depth ===
  var scrollMilestones = [25, 50, 75, 100];
  var scrollMilestonesReached = {};
  window.addEventListener("scroll", function () {
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (docHeight <= 0) return;
    var pct = Math.round((window.scrollY / docHeight) * 100);
    for (var i = 0; i < scrollMilestones.length; i++) {
      var milestone = scrollMilestones[i];
      if (pct >= milestone && !scrollMilestonesReached[milestone]) {
        scrollMilestonesReached[milestone] = true;
        sendAnalyticsEvent("scroll_depth", {
          depth_percent: milestone,
          page_path: location.pathname,
          time_on_page: getTimeOnPage()
        });
      }
    }
  }, { passive: true });

  // === Tracking data-attributes ===
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-track-event]");
    if (!el) return;
    var params = {
      track_value: el.getAttribute("data-track-value") || "",
      track_type: el.getAttribute("data-track-type") || "",
      page_path: location.pathname
    };
    sendAnalyticsEvent(el.getAttribute("data-track-event"), params);
  });

  // === Tracking formulaire de signalement ===
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (form.id === "form-signalement") {
      var emailInput = form.querySelector("[name='email']");
      var villeInput = form.querySelector("[name='ville']");
      var catInput = form.querySelector("[name='categorie']");
      var emailVal = emailInput ? emailInput.value : "";
      var villeVal = villeInput ? villeInput.value : "";
      var catVal = catInput ? catInput.value : "";

      sendAnalyticsEvent("form_submit_report", {
        report_city: villeVal,
        report_category: catVal,
        time_on_page: getTimeOnPage()
      });

      if (emailVal) {
        hashEmail(emailVal).then(function (hashed) {
          if (hashed) {
            sendAnalyticsEvent("user_identified", {
              user_id_hashed: hashed,
              method: "report_form"
            });
          }
        });
      }
    }
  });

  // === Tracking newsletter/alerte ===
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (form.id === "form-alerte" || form.id === "form-newsletter") {
      var emailInput = form.querySelector("[type='email']");
      var emailVal = emailInput ? emailInput.value : "";

      sendAnalyticsEvent("lead_capture", {
        form_type: form.id === "form-alerte" ? "alert" : "newsletter",
        page_path: location.pathname,
        time_on_page: getTimeOnPage()
      });

      if (emailVal) {
        hashEmail(emailVal).then(function (hashed) {
          if (hashed) {
            sendAnalyticsEvent("user_identified", {
              user_id_hashed: hashed,
              method: form.id
            });
          }
        });
      }
    }
  });

  // === Tracking modales ===
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-modal]");
    if (!el) return;
    sendAnalyticsEvent("modal_open", {
      modal_name: el.getAttribute("data-modal"),
      page_path: location.pathname
    });
  });

  // === Tracking recherche ville ===
  var searchTimeout;
  document.addEventListener("input", function (e) {
    var el = e.target;
    if (el.id === "search-ville" || el.id === "sim-search" || el.classList.contains("search-float__input")) {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(function () {
        if (el.value.length >= 2) {
          sendAnalyticsEvent("search_city", {
            search_term: el.value,
            search_context: location.pathname.indexOf("simulateur") > -1 ? "simulator" : "comparator",
            page_path: location.pathname
          });
        }
      }, 1000);
    }
  });

  // === Tracking liens externes (sources programmes) ===
  document.addEventListener("click", function (e) {
    var link = e.target.closest("a[target='_blank']");
    if (!link) return;
    var href = link.href || "";
    if (href.indexOf("pourquituvotes.fr") > -1 || href.indexOf("localhost") > -1) return;

    var isPdf = href.indexOf(".pdf") > -1;
    var isSource = link.closest(".proposition-source") || link.classList.contains("btn-pdf") || link.getAttribute("data-source-url");

    sendAnalyticsEvent("outbound_click", {
      link_url: href,
      link_text: (link.textContent || "").trim().substring(0, 50),
      is_pdf: isPdf,
      is_source_verification: !!isSource,
      page_path: location.pathname
    });
  });

  // === Tracking partage social ===
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-track-event='social_share']");
    if (el) return; // Already handled by data-track-event
    var shareBtn = e.target.closest(".partage-btn, .sim-share__btn");
    if (!shareBtn) return;
    var platform = shareBtn.getAttribute("data-platform") ||
      (shareBtn.textContent.indexOf("Twitter") > -1 || shareBtn.textContent.indexOf("X") > -1 ? "twitter" :
       shareBtn.textContent.indexOf("Facebook") > -1 ? "facebook" :
       shareBtn.textContent.indexOf("WhatsApp") > -1 ? "whatsapp" :
       shareBtn.textContent.indexOf("Copier") > -1 ? "copy_link" : "unknown");
    sendAnalyticsEvent("social_share", {
      platform: platform,
      share_context: location.pathname.indexOf("simulateur") > -1 ? "simulator_result" : "comparator",
      page_path: location.pathname
    });
  });

  // === API publique pour app.js et simulateur.js ===
  window.PQTV_Analytics = {
    send: sendAnalyticsEvent,
    hashEmail: hashEmail,
    getTimeOnPage: getTimeOnPage,

    // Comparateur
    trackCitySelected: function (cityName, citySlug) {
      sendAnalyticsEvent("city_selected", {
        city_name: cityName,
        city_slug: citySlug,
        nb_candidates: 0, // set by caller
        page_path: location.pathname
      });
    },

    trackCandidateFilter: function (action, candidateName, totalSelected, totalAvailable) {
      sendAnalyticsEvent("candidate_filter", {
        filter_action: action, // "select", "deselect", "select_all", "deselect_all"
        candidate_name: candidateName || "",
        candidates_selected: totalSelected,
        candidates_available: totalAvailable,
        page_path: location.pathname
      });
    },

    trackCandidateFocusChange: function (selectedNames, selectionCount) {
      sendAnalyticsEvent("candidate_focus_change", {
        selected_candidates_names: selectedNames.join(", "),
        selection_count: selectionCount,
        page_path: location.pathname,
        time_on_page: getTimeOnPage()
      });
    },

    trackCategoryView: function (categoryId, categoryName) {
      sendAnalyticsEvent("category_view", {
        category_id: categoryId,
        category_name: categoryName,
        time_on_page: getTimeOnPage(),
        page_path: location.pathname
      });
    },

    trackSourceClick: function (candidateName, categoryId, sourceUrl) {
      sendAnalyticsEvent("source_verification", {
        candidate_name: candidateName,
        category_id: categoryId,
        source_url: sourceUrl,
        time_on_page: getTimeOnPage(),
        page_path: location.pathname
      });
    },

    trackViewModeChange: function (mode) {
      sendAnalyticsEvent("view_mode_change", {
        view_mode: mode, // "radar", "tableau", "fiches"
        page_path: location.pathname
      });
    },

    // Simulateur
    trackQuizStart: function (cityName, mode) {
      sendAnalyticsEvent("quiz_start", {
        city_name: cityName,
        quiz_mode: mode, // "express", "expert"
        page_path: location.pathname
      });
    },

    trackQuizStep: function (stepNumber, totalSteps, categoryId, answer, timeSpent) {
      sendAnalyticsEvent("quiz_step_complete", {
        step_number: stepNumber,
        total_steps: totalSteps,
        category_id: categoryId,
        answer_value: answer, // 1, 0, -1
        time_spent_seconds: timeSpent,
        page_path: location.pathname
      });
    },

    trackQuizStepChange: function (stepNumber, oldAnswer, newAnswer) {
      sendAnalyticsEvent("quiz_answer_changed", {
        step_number: stepNumber,
        old_answer: oldAnswer,
        new_answer: newAnswer,
        page_path: location.pathname
      });
    },

    trackQuizPriorities: function (priorities) {
      sendAnalyticsEvent("quiz_priorities_set", {
        priorities: priorities.join(","),
        page_path: location.pathname
      });
    },

    trackQuizResult: function (cityName, mode, topCandidate, topPct, podium, questionsAnswered) {
      sendAnalyticsEvent("quiz_result", {
        city_name: cityName,
        quiz_mode: mode,
        top_candidate: topCandidate,
        top_match_pct: topPct,
        podium_json: JSON.stringify(podium.slice(0, 3).map(function (c) {
          return { name: c.nom, pct: c.pourcentage };
        })),
        questions_answered: questionsAnswered,
        time_on_page: getTimeOnPage(),
        page_path: location.pathname
      });
    },

    trackQuizEarlyExit: function (stepNumber, totalSteps) {
      sendAnalyticsEvent("quiz_early_exit", {
        step_at_exit: stepNumber,
        total_steps: totalSteps,
        completion_pct: Math.round((stepNumber / totalSteps) * 100),
        time_on_page: getTimeOnPage(),
        page_path: location.pathname
      });
    },

    trackQuizShare: function (platform, topCandidate, topPct) {
      sendAnalyticsEvent("quiz_result_share", {
        platform: platform,
        top_candidate: topCandidate,
        top_match_pct: topPct,
        page_path: location.pathname
      });
    },

    // FAQ
    trackFaqOpen: function (questionId, questionText) {
      sendAnalyticsEvent("faq_question_open", {
        question_id: questionId,
        question_text: questionText.substring(0, 100),
        page_path: location.pathname
      });
    },

    // === Bloc "Ville non trouvée" avec formulaire de notification ===
    renderNoResult: function (container, searchTerm) {
      searchTerm = (searchTerm || "").trim();

      // 1. Tracking GA4
      sendAnalyticsEvent("search_no_result", {
        search_term: searchTerm,
        page_path: location.pathname
      });

      // 2. Construction DOM (textContent sur searchTerm → anti-XSS)
      var wrapper = document.createElement("div");
      wrapper.className = "search-no-result";

      // Header : icône + titre sur une ligne
      var header = document.createElement("div");
      header.className = "search-no-result__header";
      var iconI = document.createElement("i");
      iconI.className = "ph ph-map-pin-simple-area";
      header.appendChild(iconI);
      var title = document.createElement("span");
      title.textContent = "Cette ville n'est pas encore couverte";
      header.appendChild(title);

      // Description compacte
      var desc = document.createElement("p");
      desc.className = "search-no-result__desc";
      desc.appendChild(document.createTextNode("\u00catre pr\u00e9venu(e) quand "));
      var strong = document.createElement("strong");
      strong.textContent = searchTerm;
      desc.appendChild(strong);
      desc.appendChild(document.createTextNode(" sera disponible :"));

      // Formulaire inline
      var form = document.createElement("form");
      form.className = "search-no-result__form";

      var inputEmail = document.createElement("input");
      inputEmail.type = "email";
      inputEmail.className = "search-no-result__input";
      inputEmail.placeholder = "Votre email";
      inputEmail.required = true;

      var btn = document.createElement("button");
      btn.type = "submit";
      btn.className = "search-no-result__btn";
      var btnIcon = document.createElement("i");
      btnIcon.className = "ph ph-bell-ringing";
      btn.appendChild(btnIcon);
      btn.appendChild(document.createTextNode(" M'avertir"));

      form.appendChild(inputEmail);
      form.appendChild(btn);

      // Lien méthodologie
      var footer = document.createElement("div");
      footer.className = "search-no-result__footer";
      var link = document.createElement("a");
      link.href = "/methodologie.html";
      link.className = "search-no-result__link";
      var linkIcon = document.createElement("i");
      linkIcon.className = "ph ph-info";
      link.appendChild(linkIcon);
      link.appendChild(document.createTextNode(" Pourquoi pas toutes les villes ?"));
      footer.appendChild(link);

      wrapper.appendChild(header);
      wrapper.appendChild(desc);
      wrapper.appendChild(form);
      wrapper.appendChild(footer);

      container.innerHTML = "";
      container.appendChild(wrapper);
      container.hidden = false;

      // Empêcher la propagation des clics (évite fermeture dropdown)
      wrapper.addEventListener("mousedown", function (e) { e.stopPropagation(); });
      wrapper.addEventListener("click", function (e) { e.stopPropagation(); });

      // 3. Gestion soumission
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var email = inputEmail.value.trim();
        btn.disabled = true;
        btn.textContent = "";
        var checkIcon = document.createElement("i");
        checkIcon.className = "ph ph-check";
        btn.appendChild(checkIcon);
        btn.appendChild(document.createTextNode(" Merci !"));

        hashEmail(email).then(function (hash) {
          sendAnalyticsEvent("lead_notification_request", {
            requested_city: searchTerm,
            email_hash: hash,
            page_path: location.pathname
          });
        });
      });
    }
  };

})();
