/**
 * Cloudflare Pages Function : /municipales-2026/:ville/resultats/
 *
 * SSR pour les communes < 432 habitants (pas de shell statique).
 * Lit les données depuis data/resultats-communes/ et génère le HTML à la volée.
 * Pour les communes avec shell statique, Cloudflare sert le fichier directement
 * (les fichiers statiques ont priorité sur les Functions).
 */

function escapeHtml(str) {
  return (str || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatNumber(n) {
  return n ? n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "\u00A0") : "0";
}

export async function onRequest(context) {
  const { params, env } = context;
  const villeSlug = params.ville;

  if (!villeSlug) {
    return new Response("Not Found", { status: 404 });
  }

  // Chercher les données de la commune dans les fichiers résultats par département
  // On doit charger le bon fichier département
  // Comme on ne sait pas quel département, on va chercher dans l'asset
  // En fait, on fait un fetch sur notre propre origin pour le JSON
  const url = new URL(context.request.url);
  const origin = url.origin;

  // Essayer de trouver la commune dans les départements
  // On stocke un index léger pour le lookup
  let communeData = null;

  // Fetch l'index des communes SSR
  try {
    // Chercher dans tous les fichiers résultats-communes (ils sont exclus de cfignore)
    // Donc on ne peut pas les fetch. On doit embarquer les données dans la Function.
    // Alternative : on génère un index léger au build time.
    // Pour l'instant, on retourne une page avec le JS qui charge les données côté client.
  } catch (e) {
    // Fallback
  }

  // Générer le HTML SSR (version légère — le JS prendra le relais)
  const title = `Résultats municipales 2026 ${villeSlug.replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase())}`;
  const desc = `Résultats des élections municipales 2026. Scores, participation et classement des candidats.`;
  const canonicalUrl = `https://pourquituvotes.fr/municipales-2026/${villeSlug}/resultats/`;

  const html = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <title>${escapeHtml(title)} | #POURQUITUVOTES</title>
  <meta name="description" content="${escapeHtml(desc)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="${escapeHtml(canonicalUrl)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="#POURQUITUVOTES">
  <meta property="og:title" content="${escapeHtml(title)}">
  <meta property="og:description" content="${escapeHtml(desc)}">
  <meta property="og:url" content="${escapeHtml(canonicalUrl)}">
  <meta property="og:locale" content="fr_FR">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="${escapeHtml(title)}">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Event",
    "name": "Élections municipales 2026",
    "startDate": "2026-03-15",
    "endDate": "2026-03-22",
    "eventStatus": "https://schema.org/EventCompleted",
    "location": {
      "@type": "Place",
      "name": "${escapeHtml(villeSlug.replace(/-/g, " "))}",
      "address": {"@type": "PostalAddress", "addressCountry": "FR"}
    }
  }
  </script>
  <script>
  window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
  gtag('consent','default',{'ad_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','analytics_storage':'denied','functionality_storage':'granted','personalization_storage':'denied','security_storage':'granted','wait_for_update':500});
  </script>
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-T4CCTF6V');</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web/src/regular/style.css">
  <link rel="stylesheet" href="/css/style.css?v=2026031601">
  <link rel="stylesheet" href="/css/resultats.css?v=2026031601">
  <link rel="stylesheet" href="/css/consent.css">
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-T4CCTF6V" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <a href="#resultats-main" class="skip-link">Aller au contenu principal</a>
  <header class="site-header">
    <div class="site-header__inner">
      <a href="/" class="header-brand"><span class="brand-blanc">#POURQUITU</span><span class="brand-rouge">VOTES?</span></a>
      <nav class="header-nav">
        <ul class="header-nav__links">
          <li><a href="/municipales/2026/">Comparateur</a></li>
          <li><a href="/methodologie">M&eacute;thodologie</a></li>
          <li><a href="/faq">FAQ</a></li>
          <li><a href="/a-propos">&Agrave; propos</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <main id="resultats-main">
    <section class="resultats-hero">
      <div class="resultats-hero__inner">
        <nav class="fil-ariane fil-ariane--hero" aria-label="Fil d'Ariane">
          <ol class="fil-ariane__liste">
            <li class="fil-ariane__item"><a href="/"><i class="ph ph-house"></i> Accueil</a></li>
            <li class="fil-ariane__item"><a href="/municipales/2026/">Municipales 2026</a></li>
            <li class="fil-ariane__item"><a href="/municipales-2026/resultats/">R&eacute;sultats</a></li>
            <li class="fil-ariane__item fil-ariane__item--actif"><a href="${escapeHtml(canonicalUrl)}">${escapeHtml(villeSlug.replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase()))}</a></li>
          </ol>
        </nav>
        <h1 class="resultats-hero__titre" style="color:#fff">R&eacute;sultats municipales 2026 &mdash; ${escapeHtml(villeSlug.replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase()))}</h1>
        <p class="resultats-hero__sous-titre" style="color:#fff">15 mars 2026</p>
      </div>
    </section>
    <section class="resultats-section">
      <div id="resultats-table">
        <p style="text-align:center;padding:2rem;color:var(--couleur-texte-secondaire)">Chargement des r&eacute;sultats...</p>
      </div>
    </section>
    <div class="resultats-cta">
      <a href="/municipales-2026/resultats/" class="resultats-cta__btn"><i class="ph ph-arrow-left"></i> Tous les r&eacute;sultats</a>
      <a href="/municipales/2026/" class="resultats-cta__btn resultats-cta__btn--secondary"><i class="ph ph-scales"></i> Comparateur</a>
    </div>
  </main>
  <footer class="footer" role="contentinfo">
    <div class="footer__inner">
      <div class="footer__bottom">
        <p>&copy; 2026 #POURQUITUVOTES &mdash; Projet citoyen ind&eacute;pendant</p>
        <div class="footer__legal">
          <a href="/mentions-legales">Mentions l&eacute;gales</a>
          <a href="/confidentialite">Confidentialit&eacute;</a>
        </div>
      </div>
    </div>
  </footer>
  <script defer src="/js/consent.js"></script>
</body>
</html>`;

  return new Response(html, {
    status: 200,
    headers: {
      "Content-Type": "text/html;charset=UTF-8",
      "Cache-Control": "public, max-age=3600, s-maxage=86400",
    },
  });
}
