// _worker.js — Advanced Mode for Cloudflare Pages
// Routes /municipales-2026/:ville/resultats/ to dynamic generation
// All other requests pass through to static assets

const RESULTATS_PATTERN = /^\/municipales-2026\/([^\/]+)\/resultats\/?$/;

/**
 * Cloudflare Pages Function: /municipales-2026/:ville/resultats/
 *
 * Génère dynamiquement les pages de résultats pour les ~35 000 communes
 * au lieu de 32k fichiers HTML statiques (limite Cloudflare Pages = 20k).
 *
 * Données :
 *   - /data/index-communes.json → lookup commune par slug
 *   - /data/resultats-communes/resultats-{dept}-t1.json → résultats T1
 *   - /data/resultats-communes/resultats-{dept}-t2.json → résultats T2
 */

const DATA_VERSION = '2026040803';
const BASE_URL = 'https://pourquituvotes.fr';

const NUANCE_LABELS = {
  LUG: 'Union de la gauche', LFI: 'La France Insoumise', LEXG: 'Extrême gauche',
  LUD: 'Union de la droite', LUC: 'Union du centre', LUXD: 'Extrême droite unie',
  LEXD: 'Extrême droite', LRN: 'Rassemblement National',
  LDVG: 'Divers gauche', LDVD: 'Divers droite', LDVC: 'Divers centre',
  LECO: 'Écologistes', LDIV: 'Divers', LCOM: 'Parti communiste',
  LSOC: 'Parti socialiste', LLR: 'Les Républicains', LREM: 'Renaissance',
};

// Cache en mémoire (persiste entre les requêtes sur le même isolate)
let communesIndex = null;
let resultatsCache = {};

async function fetchJSON(origin, path) {
  const res = await fetch(origin + path);
  if (!res.ok) return null;
  return res.json();
}

async function getCommunesIndex(origin) {
  if (communesIndex) return communesIndex;
  const data = await fetchJSON(origin, `/data/index-communes.json?v=${DATA_VERSION}`);
  if (!data) return null;
  // Construire un map slug → commune
  const map = {};
  for (const c of data) {
    map[c.s] = c;
  }
  communesIndex = map;
  return map;
}

async function getResultats(origin, dept, tour) {
  const key = `${dept}-t${tour}`;
  if (resultatsCache[key]) return resultatsCache[key];
  const data = await fetchJSON(origin, `/data/resultats-communes/resultats-${dept}-t${tour}.json?v=${DATA_VERSION}`);
  if (!data) return null;
  // Construire un map slug → résultats
  const map = {};
  for (const c of data.communes || []) {
    map[c.slug] = c;
  }
  resultatsCache[key] = map;
  return map;
}

function esc(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function formatNumber(n) {
  if (!n && n !== 0) return '0';
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '\u00A0');
}

function buildSeoContent(commune, t1Data, t2Data) {
  const ville = esc(commune.n);
  let html = '';

  // T2 results
  if (t2Data && t2Data.resultats) {
    const r = t2Data.resultats;
    html += `<h2>Résultats des élections municipales 2026 à ${ville}</h2>\n`;
    html += `<p>Les résultats du second tour des élections municipales 2026 à ${ville} sont disponibles. Le taux de participation s'est établi à ${r.tauxParticipation}%.</p>\n`;
    html += `<h3>Classement des candidats aux municipales 2026 à ${ville}</h3>\n<ol>\n`;
    const sorted = [...(r.candidats || [])].sort((a, b) => b.pourcentage - a.pourcentage);
    for (const c of sorted) {
      const nuance = NUANCE_LABELS[c.nuance] || c.nuance || '';
      html += `<li>${esc(c.nom)}${nuance ? ` (${esc(nuance)})` : ''} — ${c.pourcentage}% (${formatNumber(c.voix)} voix)</li>\n`;
    }
    html += `</ol>\n`;
  }

  // T1 results
  if (t1Data && t1Data.resultats) {
    const r = t1Data.resultats;
    if (t2Data) {
      html += `<h3>Premier tour des municipales 2026 à ${ville}</h3>\n`;
      html += `<p>Au premier tour (${r.date || '15 mars 2026'}), le taux de participation était de ${r.tauxParticipation}%.</p>\n`;
    } else {
      html += `<h2>Résultats des municipales des municipales 2026 à ${ville}</h2>\n`;
      html += `<p>Le taux de participation au premier tour s'est établi à ${r.tauxParticipation}%.</p>\n`;
    }
    html += `<ol>\n`;
    const sorted = [...(r.candidats || [])].sort((a, b) => b.pourcentage - a.pourcentage);
    for (const c of sorted) {
      const qualif = c.qualifieT2 ? ' — qualifié(e) au second tour' : '';
      html += `<li>${esc(c.nom)} — ${c.pourcentage}% (${formatNumber(c.voix)} voix)${qualif}</li>\n`;
    }
    html += `</ol>\n`;
  }

  html += `<h3>Comparer les programmes</h3>\n`;
  html += `<p>Retrouvez l'analyse complète des programmes des candidats à ${ville} sur notre <a href="/municipales-2026/${esc(commune.s)}/">comparateur de programmes</a>.</p>\n`;

  return html;
}

function buildPage(commune, t1Data, t2Data) {
  const ville = esc(commune.n);
  const slug = esc(commune.s);
  const dept = esc(commune.d);
  const participation = commune.t || 0;
  const url = `${BASE_URL}/municipales-2026/${slug}/resultats/`;

  const hasT2 = !!(t2Data && t2Data.resultats);
  const tourLabel = hasT2 ? 'second' : '1er';
  const title = `Résultats du ${tourLabel} tour municipales 2026 ${ville}`;
  const description = `Résultats du ${tourLabel} tour des municipales 2026 à ${ville}. Participation : ${participation}%. Classement et scores de tous les candidats.`;

  const seoContent = buildSeoContent(commune, t1Data, t2Data);

  // Schema.org structured data
  const schemaJson = JSON.stringify({
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Event",
        "name": `Élections municipales 2026 — ${commune.n}`,
        "description": `Résultats des élections municipales 2026 à ${commune.n}, France.`,
        "startDate": "2026-03-15",
        "endDate": "2026-03-22",
        "eventStatus": "https://schema.org/EventCompleted",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {
          "@type": "Place",
          "name": commune.n,
          "address": { "@type": "PostalAddress", "addressLocality": commune.n, "addressCountry": "FR" }
        },
        "organizer": { "@type": "GovernmentOrganization", "name": "Ministère de l'Intérieur" }
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": `Qui a gagné les municipales 2026 à ${commune.n} ?`,
            "acceptedAnswer": {
              "@type": "Answer",
              "text": commune.w
                ? `${commune.w} a remporté les municipales 2026 à ${commune.n} avec ${commune.wp}% des voix.`
                : `Les résultats des municipales 2026 à ${commune.n} sont en cours de publication.`
            }
          },
          {
            "@type": "Question",
            "name": `Quel est le taux de participation aux municipales 2026 à ${commune.n} ?`,
            "acceptedAnswer": {
              "@type": "Answer",
              "text": `Le taux de participation au 1er tour des municipales 2026 à ${commune.n} est de ${participation}%.`
            }
          }
        ]
      }
    ]
  });

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, interactive-widget=resizes-content">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <title>${title}</title>
  <meta name="description" content="${esc(description)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="${url}">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="#POURQUITUVOTES">
  <meta property="og:title" content="${title}">
  <meta property="og:description" content="${esc(description)}">
  <meta property="og:url" content="${url}">
  <meta property="og:locale" content="fr_FR">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${title}">
  <meta name="twitter:description" content="${esc(description)}">

  <meta property="article:modified_time" content="2026-03-23T00:00:00+01:00">

  <!-- Structured Data -->
  <script type="application/ld+json">${schemaJson}</script>

  <script>
  window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
  gtag('consent','default',{'ad_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','analytics_storage':'denied','functionality_storage':'granted','personalization_storage':'denied','security_storage':'granted','wait_for_update':500});
  (function(){var m=document.cookie.match(/pqv_consent=([^;]+)/);if(m){try{var p=JSON.parse(decodeURIComponent(m[1]));gtag('consent','update',{'analytics_storage':p.analytics?'granted':'denied','ad_storage':p.marketing?'granted':'denied','ad_user_data':p.marketing?'granted':'denied','ad_personalization':p.marketing?'granted':'denied','personalization_storage':p.functional?'granted':'denied'});}catch(e){}}})();
  </script>
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-T4CCTF6V');</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web/src/regular/style.css">
  <link rel="stylesheet" href="/css/style.css?v=${DATA_VERSION}">
  <link rel="stylesheet" href="/css/resultats.css?v=${DATA_VERSION}">
  <link rel="stylesheet" href="/css/consent.css">
</head>
<body>
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-T4CCTF6V" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  <a href="#resultats-main" class="skip-link">Aller au contenu principal</a>

  <header class="site-header" id="site-header">
    <div class="site-header__inner">
      <a href="/" class="header-brand"><span class="brand-blanc">#POURQUITU</span><span class="brand-rouge">VOTES?</span></a>
      <nav class="header-nav">
        <ul class="header-nav__links">
          <li><a href="/municipales/2026/">Comparateur</a></li>
          <li><a href="/municipales-2026/resultats/">R&eacute;sultats</a></li>
          <li><a href="/methodologie">M&eacute;thodologie</a></li>
          <li><a href="/faq">FAQ</a></li>
          <li><a href="/a-propos">&Agrave; propos</a></li>
        </ul>
      </nav>
      <button class="header__burger" id="burger-btn" aria-label="Ouvrir le menu" aria-expanded="false">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="15" y2="6"/><line x1="3" y1="12" x2="12" y2="12"/><line x1="3" y1="18" x2="10" y2="18"/><circle cx="19" cy="16" r="3" stroke-width="1.8" fill="none"/><line x1="21.2" y1="18.2" x2="23" y2="20"/></svg>
      </button>
    </div>
  </header>

  <div class="mobile-menu-overlay" id="mobile-menu" hidden>
    <div class="mobile-menu-overlay__header">
      <a href="/" class="header-brand"><span class="brand-blanc">#POURQUITU</span><span class="brand-rouge">VOTES?</span></a>
      <button class="mobile-menu-overlay__close" id="mobile-menu-close" aria-label="Fermer"><i class="ph ph-x"></i></button>
    </div>
    <div class="mobile-menu-overlay__search">
      <div class="mobile-menu-search-box">
        <i class="ph ph-magnifying-glass"></i>
        <input type="text" id="mobile-menu-search" placeholder="Ville, candidat ou code postal..." autocomplete="off">
      </div>
      <div class="mobile-menu-suggestions" id="mobile-menu-suggestions" hidden></div>
    </div>
    <nav class="mobile-menu-overlay__nav">
      <ul>
        <li><a href="/municipales/2026/"><i class="ph ph-scales"></i> Comparateur</a></li>
        <li><a href="/municipales-2026/resultats/"><i class="ph ph-chart-bar"></i> R&eacute;sultats</a></li>
        <li><a href="/methodologie"><i class="ph ph-book-open"></i> M&eacute;thodologie</a></li>
        <li><a href="/faq"><i class="ph ph-question"></i> FAQ</a></li>
        <li><a href="/a-propos"><i class="ph ph-info"></i> &Agrave; propos</a></li>
      </ul>
    </nav>
  </div>

  <main id="resultats-main">
    <section class="resultats-hero" id="resultats-hero">
      <div class="resultats-hero__inner">
        <nav class="fil-ariane fil-ariane--hero" aria-label="Fil d'Ariane">
          <ol class="fil-ariane__liste" itemscope itemtype="https://schema.org/BreadcrumbList">
            <li class="fil-ariane__item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
              <a href="/" itemprop="item"><i class="ph ph-house"></i><span itemprop="name">Accueil</span></a>
              <meta itemprop="position" content="1">
            </li>
            <li class="fil-ariane__item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
              <a href="/municipales-2026/resultats/" itemprop="item"><span itemprop="name">Résultats</span></a>
              <meta itemprop="position" content="2">
            </li>
            <li class="fil-ariane__item fil-ariane__item--actif" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
              <a href="${url}" itemprop="item"><span itemprop="name">${ville}</span></a>
              <meta itemprop="position" content="3">
            </li>
          </ol>
        </nav>

        <div class="resultats-hero__status" id="resultats-status-badge"></div>
        <h1 class="resultats-hero__titre" id="resultats-titre">Chargement des r&eacute;sultats...</h1>
        <p class="resultats-hero__sous-titre" id="resultats-sous-titre"></p>

        <div class="resultats-hero__stats" id="resultats-hero-stats">
          <div class="resultats-hero__stat">
            <span class="resultats-hero__stat-valeur" id="stat-participation">—</span>
            <span class="resultats-hero__stat-label">Participation</span>
          </div>
          <div class="resultats-hero__stat">
            <span class="resultats-hero__stat-valeur" id="stat-inscrits">—</span>
            <span class="resultats-hero__stat-label">Inscrits</span>
          </div>
          <div class="resultats-hero__stat">
            <span class="resultats-hero__stat-valeur" id="stat-exprimes">—</span>
            <span class="resultats-hero__stat-label">Exprim&eacute;s</span>
          </div>
        </div>
      </div>
    </section>

    <div class="resultats-onglets" id="resultats-onglets" hidden>
      <button class="resultats-onglets__btn resultats-onglets__btn--actif" data-tour="1">Tour 1</button>
      <button class="resultats-onglets__btn" data-tour="2">Tour 2</button>
    </div>

    <section class="resultats-section" id="resultats-section">
      <h2 class="resultats-section__titre" id="resultats-section-titre">Classement des candidats</h2>
      <div class="resultats-table" id="resultats-table" role="table" aria-label="R&eacute;sultats par candidat">
        <p class="resultats-table__loading">Chargement...</p>
      </div>
    </section>

    <section class="resultats-fusions" id="resultats-fusions" hidden>
      <h2 class="resultats-fusions__titre">Fusions de listes au second tour</h2>
      <div id="resultats-fusions-content"></div>
    </section>

    <section class="resultats-participation" id="resultats-participation">
      <h2 class="resultats-participation__titre">Participation &eacute;lectorale</h2>
      <div class="resultats-participation__inner">
        <div class="resultats-participation__chart-wrap">
          <canvas id="participation-chart" width="300" height="300"></canvas>
        </div>
        <div class="resultats-participation__details" id="participation-details"></div>
      </div>
    </section>

    <div class="resultats-cta">
      <a href="/municipales-2026/${slug}/" id="resultats-cta-comparer" class="resultats-cta__btn">
        <i class="ph ph-scales"></i> Comparez les programmes &agrave; ${ville}
      </a>
      <a href="#" id="resultats-cta-share" class="resultats-cta__btn resultats-cta__btn--secondary" hidden>
        <i class="ph ph-share-network"></i> Partager les r&eacute;sultats
      </a>
    </div>
  </main>

  <section class="seo-content" aria-label="Résultats des élections municipales 2026 à ${ville}">
    ${seoContent}
  </section>

  <footer class="footer" role="contentinfo">
    <div class="footer__inner">
      <div class="footer__grid">
        <div class="footer__brand">
          <a href="/" class="footer__logo" aria-label="Accueil">
            <span class="logo__hash">#</span><span class="logo__pourquitu">POURQUITU</span><span class="logo__votes">VOTES</span><span class="logo__question">?</span>
          </a>
          <p class="footer__tagline">Comparez les programmes des candidats. Projet citoyen, ind&eacute;pendant et non-partisan.</p>
          <div class="footer__socials" aria-label="R&eacute;seaux sociaux">
            <a href="#" aria-label="X (Twitter)" class="footer__social"><i class="ph ph-x-logo" aria-hidden="true"></i></a>
            <a href="#" aria-label="Facebook" class="footer__social"><i class="ph ph-facebook-logo" aria-hidden="true"></i></a>
            <a href="#" aria-label="LinkedIn" class="footer__social"><i class="ph ph-linkedin-logo" aria-hidden="true"></i></a>
          </div>
        </div>
        <div class="footer__col">
          <h3 class="footer__col-title">Municipales 2026</h3>
          <ul class="footer__list">
            <li><a href="/municipales-2026/paris/">Paris</a></li>
            <li><a href="/municipales-2026/lyon/">Lyon</a></li>
            <li><a href="/municipales-2026/marseille/">Marseille</a></li>
            <li><a href="/municipales-2026/toulouse/">Toulouse</a></li>
            <li><a href="/municipales-2026/nice/">Nice</a></li>
            <li><a href="/municipales-2026/nantes/">Nantes</a></li>
            <li><a href="/municipales-2026/bordeaux/">Bordeaux</a></li>
            <li><a href="/municipales/2026/" class="footer__link--all">Toutes les villes <i class="ph ph-arrow-right" aria-hidden="true"></i></a></li>
          </ul>
        </div>
        <div class="footer__col">
          <h3 class="footer__col-title">Enjeux &amp; &Eacute;lections</h3>
          <ul class="footer__list">
            <li><a href="/municipales-2026/resultats/">Résultats des municipales</a></li>
            <li><a href="/enjeux-index.html">Enjeux 2026</a></li>
            <li><a href="/presidentielle/2027/">Pr&eacute;sidentielle 2027 <span class="footer__badge footer__badge--soon">bient&ocirc;t</span></a></li>
            <li><span class="footer__item-soon">L&eacute;gislatives 2027</span></li>
            <li><span class="footer__item-soon">R&eacute;gionales</span></li>
            <li><span class="footer__item-soon">Europ&eacute;ennes 2029</span></li>
          </ul>
        </div>
        <div class="footer__col">
          <h3 class="footer__col-title">Le projet</h3>
          <ul class="footer__list">
            <li><a href="/a-propos">&Agrave; propos</a></li>
            <li><a href="/methodologie">M&eacute;thodologie</a></li>
            <li><a href="/faq">FAQ</a></li>
            <li><a href="mailto:contact@pourquituvotes.fr">Contact</a></li>
            <li><a href="#" class="js-open-contribuer"><i class="ph ph-hand-heart" aria-hidden="true"></i> Contribuer</a></li>
          </ul>
        </div>
      </div>
      <div class="footer__bottom">
        <p>&copy; 2026 #POURQUITUVOTES &mdash; Projet citoyen ind&eacute;pendant</p>
        <div class="footer__legal">
          <a href="/mentions-legales">Mentions l&eacute;gales</a>
          <a href="/confidentialite">Confidentialit&eacute;</a>
          <a href="/confidentialite" class="js-open-consent">Gestion des cookies</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    var burgerBtn = document.getElementById("burger-btn");
    var mobileMenu = document.getElementById("mobile-menu");
    var menuClose = document.getElementById("mobile-menu-close");
    if (burgerBtn && mobileMenu) {
      burgerBtn.addEventListener("click", function() {
        mobileMenu.hidden = false;
        document.body.style.overflow = "hidden";
      });
      if (menuClose) menuClose.addEventListener("click", function() {
        mobileMenu.hidden = true;
        document.body.style.overflow = "";
      });
    }
  </script>
  <script defer src="/js/consent.min.js"></script>
  <script defer src="/js/seo-utils.js"></script>
  <script defer src="/js/burger-search.js?v=${DATA_VERSION}"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
  <script defer src="/js/resultats.js?v=${DATA_VERSION}"></script>
  <script defer src="/js/contribuer.js"></script>
</body>
</html>`;
}


export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const match = url.pathname.match(RESULTATS_PATTERN);

    if (!match) {
      return env.ASSETS.fetch(request);
    }

    if (!url.pathname.endsWith('/')) {
      return Response.redirect(url.origin + url.pathname + '/', 301);
    }

    const slug = decodeURIComponent(match[1]).toLowerCase();
    const origin = url.origin;

    const index = await getCommunesIndex(origin);
    if (!index || !index[slug]) {
      return env.ASSETS.fetch(request);
    }

    const commune = index[slug];
    const [t1Map, t2Map] = await Promise.all([
      getResultats(origin, commune.d, 1),
      getResultats(origin, commune.d, 2),
    ]);

    const html = buildPage(commune, t1Map ? t1Map[slug] : null, t2Map ? t2Map[slug] : null);

    return new Response(html, {
      status: 200,
      headers: {
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'public, max-age=3600, s-maxage=86400',
        'X-Robots-Tag': 'index, follow',
      },
    });
  },
};
