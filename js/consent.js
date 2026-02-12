/* ============================================================
   #POURQUITUVOTES — Cookie Consent CMP
   CNIL-compliant + Google Consent Mode V2
   ============================================================ */
(function() {
  "use strict";

  var COOKIE_NAME = "pqv_consent";
  var COOKIE_DAYS = 180; // 6 mois

  // === Cookie helpers ===
  function getCookie(name) {
    var match = document.cookie.match(new RegExp("(^|;\\s*)" + name + "=([^;]+)"));
    return match ? decodeURIComponent(match[2]) : null;
  }

  function setCookie(name, value, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 86400000);
    document.cookie = name + "=" + encodeURIComponent(value) +
      ";expires=" + d.toUTCString() +
      ";path=/;SameSite=Lax;Secure";
  }

  function getConsent() {
    var raw = getCookie(COOKIE_NAME);
    if (!raw) return null;
    try { return JSON.parse(raw); } catch(e) { return null; }
  }

  // === Consent Mode V2 ===
  function updateGtagConsent(prefs) {
    if (typeof gtag === "function") {
      gtag("consent", "update", {
        "analytics_storage": prefs.analytics ? "granted" : "denied",
        "ad_storage": prefs.marketing ? "granted" : "denied",
        "ad_user_data": prefs.marketing ? "granted" : "denied",
        "ad_personalization": prefs.marketing ? "granted" : "denied",
        "personalization_storage": prefs.functional ? "granted" : "denied"
      });
    }
  }

  function pushDataLayer(prefs) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      "event": "consent_update",
      "consent_analytics": prefs.analytics ? "granted" : "denied",
      "consent_marketing": prefs.marketing ? "granted" : "denied",
      "consent_functional": prefs.functional ? "granted" : "denied"
    });
  }

  function saveConsent(prefs) {
    setCookie(COOKIE_NAME, JSON.stringify(prefs), COOKIE_DAYS);
    updateGtagConsent(prefs);
    pushDataLayer(prefs);
  }

  // === UI Elements ===
  var bannerOverlayEl = null;
  var overlayEl = null;

  function createBanner() {
    var wrapper = document.createElement("div");
    wrapper.className = "consent-banner-overlay";
    wrapper.setAttribute("role", "dialog");
    wrapper.setAttribute("aria-label", "Gestion des cookies");
    wrapper.innerHTML =
      '<div class="consent-banner">' +
        '<div class="consent-banner__icon" aria-hidden="true">\uD83D\uDD12</div>' +
        '<div class="consent-banner__title">Respect de votre vie priv\u00e9e</div>' +
        '<div class="consent-banner__desc">Nous utilisons des cookies pour mesurer l\u2019audience du site et am\u00e9liorer votre exp\u00e9rience. Aucune donn\u00e9e personnelle n\u2019est vendue. <a href="/confidentialite.html">En savoir plus</a></div>' +
        '<div class="consent-banner__actions">' +
          '<button type="button" class="consent-btn consent-btn--refuse" data-consent="refuse">Tout refuser</button>' +
          '<button type="button" class="consent-btn consent-btn--customize" data-consent="customize">Personnaliser</button>' +
          '<button type="button" class="consent-btn consent-btn--accept" data-consent="accept">Tout accepter</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(wrapper);
    bannerOverlayEl = wrapper;

    // Event listeners
    wrapper.querySelector('[data-consent="refuse"]').addEventListener("click", refuseAll);
    wrapper.querySelector('[data-consent="customize"]').addEventListener("click", function() {
      hideBanner();
      showModal();
    });
    wrapper.querySelector('[data-consent="accept"]').addEventListener("click", acceptAll);
  }

  function createModal() {
    var div = document.createElement("div");
    div.className = "consent-overlay";
    div.setAttribute("role", "dialog");
    div.setAttribute("aria-label", "Param\u00e8tres des cookies");
    div.innerHTML =
      '<div class="consent-modal">' +
        '<div class="consent-modal__header">' +
          '<h2 class="consent-modal__title">\uD83D\uDD27 Gestion des cookies</h2>' +
          '<button type="button" class="consent-modal__close" aria-label="Fermer">&times;</button>' +
        '</div>' +
        '<p class="consent-modal__desc">Choisissez les cookies que vous acceptez. Les cookies essentiels sont n\u00e9cessaires au fonctionnement du site et ne peuvent pas \u00eatre d\u00e9sactiv\u00e9s. <a href="/confidentialite.html">Politique de confidentialit\u00e9</a></p>' +

        // Essentiels (toujours actifs)
        '<div class="consent-category">' +
          '<div class="consent-category__header">' +
            '<div><span class="consent-category__name">Cookies essentiels</span><span class="consent-category__badge">Toujours actifs</span></div>' +
            '<label class="consent-toggle"><input type="checkbox" checked disabled><span class="consent-toggle__track"></span></label>' +
          '</div>' +
          '<p class="consent-category__desc">N\u00e9cessaires au fonctionnement du site (sauvegarde de vos pr\u00e9f\u00e9rences de consentement). Aucune donn\u00e9e personnelle n\u2019est collect\u00e9e.</p>' +
        '</div>' +

        // Analytiques
        '<div class="consent-category">' +
          '<div class="consent-category__header">' +
            '<span class="consent-category__name">Cookies analytiques</span>' +
            '<label class="consent-toggle"><input type="checkbox" id="consent-analytics"><span class="consent-toggle__track"></span></label>' +
          '</div>' +
          '<p class="consent-category__desc">Permettent de mesurer l\u2019audience du site de mani\u00e8re anonyme (Google Analytics). Nous aident \u00e0 comprendre quelles villes et fonctionnalit\u00e9s int\u00e9ressent le plus les visiteurs.</p>' +
        '</div>' +

        // Marketing
        '<div class="consent-category">' +
          '<div class="consent-category__header">' +
            '<span class="consent-category__name">Cookies marketing</span>' +
            '<label class="consent-toggle"><input type="checkbox" id="consent-marketing"><span class="consent-toggle__track"></span></label>' +
          '</div>' +
          '<p class="consent-category__desc">Utilis\u00e9s pour les fonctionnalit\u00e9s de partage social et le suivi des campagnes. Actuellement, aucun cookie marketing n\u2019est d\u00e9pos\u00e9 sur ce site.</p>' +
        '</div>' +

        // Actions
        '<div class="consent-modal__actions">' +
          '<button type="button" class="consent-btn consent-btn--refuse" data-modal="refuse">Tout refuser</button>' +
          '<button type="button" class="consent-btn consent-btn--save" data-modal="save">Enregistrer</button>' +
          '<button type="button" class="consent-btn consent-btn--accept" data-modal="accept">Tout accepter</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(div);
    overlayEl = div;

    // Event listeners
    div.querySelector(".consent-modal__close").addEventListener("click", hideModal);
    div.querySelector('[data-modal="refuse"]').addEventListener("click", refuseAll);
    div.querySelector('[data-modal="save"]').addEventListener("click", saveCustom);
    div.querySelector('[data-modal="accept"]').addEventListener("click", acceptAll);

    // Close on overlay click
    div.addEventListener("click", function(e) {
      if (e.target === div) hideModal();
    });

    // Close on Escape
    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape" && overlayEl && overlayEl.classList.contains("consent-overlay--visible")) {
        hideModal();
      }
    });
  }

  // === Show / Hide ===
  function showBanner() {
    if (!bannerOverlayEl) createBanner();
    void bannerOverlayEl.offsetHeight;
    bannerOverlayEl.classList.add("consent-banner-overlay--visible");
    document.body.style.overflow = "hidden";
  }

  function hideBanner() {
    if (bannerOverlayEl) {
      bannerOverlayEl.classList.remove("consent-banner-overlay--visible");
    }
    document.body.style.overflow = "";
  }

  function showModal() {
    if (!overlayEl) createModal();

    // Load current prefs into checkboxes
    var prefs = getConsent() || { analytics: false, marketing: false, functional: true };
    document.getElementById("consent-analytics").checked = prefs.analytics;
    document.getElementById("consent-marketing").checked = prefs.marketing;

    overlayEl.classList.add("consent-overlay--visible");
    document.body.style.overflow = "hidden";
  }

  function hideModal() {
    if (overlayEl) {
      overlayEl.classList.remove("consent-overlay--visible");
    }
    document.body.style.overflow = "";
  }

  // === Actions ===
  function acceptAll() {
    saveConsent({ analytics: true, marketing: true, functional: true });
    hideBanner();
    hideModal();
  }

  function refuseAll() {
    saveConsent({ analytics: false, marketing: false, functional: true });
    hideBanner();
    hideModal();
  }

  function saveCustom() {
    var prefs = {
      analytics: document.getElementById("consent-analytics").checked,
      marketing: document.getElementById("consent-marketing").checked,
      functional: true
    };
    saveConsent(prefs);
    hideBanner();
    hideModal();
  }

  // === Global function for footer link ===
  window.showConsentModal = function() {
    showModal();
  };

  // === Init ===
  function init() {
    var existing = getConsent();
    if (!existing) {
      setTimeout(showBanner, 800);
    }

    // Bind footer links
    var links = document.querySelectorAll(".js-open-consent");
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener("click", function(e) {
        e.preventDefault();
        showModal();
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
