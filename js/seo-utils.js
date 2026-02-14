/**
 * seo-utils.js — Shared SEO utility functions for pourquituvotes.fr
 * Loaded across multiple pages to manage meta tags, canonical URLs,
 * Open Graph / Twitter Cards, and JSON-LD breadcrumbs.
 */

function updateMeta(key, content) {
  var el = document.querySelector('meta[name="' + key + '"]') ||
           document.querySelector('meta[property="' + key + '"]');
  if (el) {
    el.content = content;
  } else {
    el = document.createElement('meta');
    el.setAttribute(key.indexOf('og:') === 0 ? 'property' : 'name', key);
    el.content = content;
    document.head.appendChild(el);
  }
}

function setCanonical(url) {
  var el = document.querySelector('link[rel="canonical"]');
  if (el) {
    el.href = url;
  } else {
    el = document.createElement('link');
    el.rel = 'canonical';
    el.href = url;
    document.head.appendChild(el);
  }
}

function injectJsonLdBreadcrumb(items) {
  // items = [{name, url}, ...] — last item has no url (current page)
  var list = items.map(function(item, i) {
    var entry = {"@type": "ListItem", "position": i + 1, "name": item.name};
    if (item.url) entry.item = item.url;
    return entry;
  });
  var script = document.createElement('script');
  script.type = 'application/ld+json';
  script.textContent = JSON.stringify({
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": list
  });
  document.head.appendChild(script);
}

function updateOpenGraph(title, description, url) {
  updateMeta('og:title', title);
  updateMeta('og:description', description);
  updateMeta('og:url', url);
  updateMeta('og:type', 'website');
  updateMeta('twitter:title', title);
  updateMeta('twitter:description', description);
}

function updateOgImage(villeId, candidatId) {
  var base = 'https://pourquituvotes.fr/img/og/';
  var filename;
  if (candidatId) {
    filename = villeId + '-' + candidatId + '.jpg';
  } else if (villeId) {
    filename = villeId + '.jpg';
  } else {
    filename = 'comparateur.jpg';
  }
  var url = base + filename;
  updateMeta('og:image', url);
  updateMeta('og:image:width', '1200');
  updateMeta('og:image:height', '630');
  updateMeta('twitter:image', url);
}
