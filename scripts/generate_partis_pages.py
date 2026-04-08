#!/usr/bin/env python3
"""
Génère les pages dédiées /partis/{id}/index.html pour chaque parti.
Usage: python scripts/generate_partis_pages.py
"""
import json
import os
import sys
from html import escape

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_VERSION = "2026040804"
BASE_URL = "https://pourquituvotes.fr"

AXES_LABELS = {
    "economie": ("Économie", "1 = Interventionnisme · 10 = Libéralisme"),
    "social": ("Social", "1 = Conservateur · 10 = Progressiste"),
    "immigration": ("Immigration", "1 = Ouverture · 10 = Restriction"),
    "europe": ("Europe", "1 = Souverainisme · 10 = Fédéralisme"),
    "ecologie": ("Écologie", "1 = Productivisme · 10 = Écologie radicale"),
    "securite": ("Sécurité", "1 = Prévention · 10 = Répression"),
}

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def esc(s):
    return escape(str(s)) if s else ""

def generate_page(parti):
    pid = parti["id"]
    nom = parti["nom"]
    sigle = parti["sigle"]
    couleur = parti["couleur"]
    leader = parti.get("leader", "")
    fondation = parti.get("fondation", "")
    positionnement = parti.get("positionnement", "")
    histoire = parti.get("histoire", "")
    site = parti.get("site", "")
    figures = parti.get("figuresCles", [])
    programme = parti.get("programmeNational", [])
    ideologie = parti.get("ideologie", [])
    positions = parti.get("positions", {})
    resultats = parti.get("resultats", {})
    nuances = parti.get("nuancesAssociees", [])

    url = f"{BASE_URL}/partis/{pid}/"
    title = f"{nom} ({sigle}) — Programme et positions | #POURQUITUVOTES"
    description = f"Fiche complète du {nom} : leader, programme national, positionnement politique, résultats électoraux et histoire. Projet citoyen indépendant."

    # Positions HTML
    positions_html = ""
    for key, (label, legend) in AXES_LABELS.items():
        pos = positions.get(key, {})
        score = pos.get("score", 5)
        resume = esc(pos.get("resume", ""))
        pct = score * 10
        positions_html += f"""
      <div class="partip__pos-row">
        <div class="partip__pos-header">
          <span class="partip__pos-label">{label}</span>
          <span class="partip__pos-score">{score}/10</span>
        </div>
        <div class="partip__pos-track"><div class="partip__pos-fill pos-bar--{key}" style="width:{pct}%"></div></div>
        <p class="partip__pos-resume">{resume}</p>
        <p class="partip__pos-legend">{legend}</p>
      </div>"""

    # Programme HTML
    programme_html = ""
    for point in programme:
        programme_html += f"        <li>{esc(point)}</li>\n"

    # Figures HTML
    figures_html = ", ".join(esc(f) for f in figures) if figures else "—"

    # Ideologie tags
    tags_html = "".join(f'<span class="partip__tag">{esc(t)}</span>' for t in ideologie)

    # Résultats HTML
    res_html = ""
    if resultats.get("presidentielle2022"):
        r = resultats["presidentielle2022"]
        cand = r.get("candidat", "")
        t1 = r.get("tour1", 0)
        t2 = r.get("tour2")
        res_html += f'<div class="partip__res-item"><strong>Présidentielle 2022</strong> : {esc(cand)} — {t1}% au 1er tour'
        if t2:
            res_html += f", {t2}% au 2nd tour"
        res_html += "</div>\n"
    if resultats.get("legislatives2024"):
        r = resultats["legislatives2024"]
        res_html += f'<div class="partip__res-item"><strong>Législatives 2024</strong> : {r.get("sieges", "?")} sièges</div>\n'
    if resultats.get("europeennes2024"):
        r = resultats["europeennes2024"]
        res_html += f'<div class="partip__res-item"><strong>Européennes 2024</strong> : {r.get("pourcentage", "?")}%'
        if r.get("sieges"):
            res_html += f" ({r['sieges']} sièges)"
        res_html += "</div>\n"

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, interactive-widget=resizes-content">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{url}">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="#POURQUITUVOTES">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="fr_FR">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "{nom}",
    "alternateName": "{sigle}",
    "url": "{esc(site)}",
    "description": "{esc(description)}"
  }}
  </script>

  <script>
  window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
  gtag('consent','default',{{'ad_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','analytics_storage':'denied','functionality_storage':'granted','personalization_storage':'denied','security_storage':'granted','wait_for_update':500}});
  (function(){{var m=document.cookie.match(/pqv_consent=([^;]+)/);if(m){{try{{var p=JSON.parse(decodeURIComponent(m[1]));gtag('consent','update',{{'analytics_storage':p.analytics?'granted':'denied','ad_storage':p.marketing?'granted':'denied','ad_user_data':p.marketing?'granted':'denied','ad_personalization':p.marketing?'granted':'denied','personalization_storage':p.functional?'granted':'denied'}});}}catch(e){{}}}}}})()</script>
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-T4CCTF6V');</script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web/src/regular/style.css" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="/css/style.css?v={DATA_VERSION}">
  <link rel="stylesheet" href="/css/partis.css?v={DATA_VERSION}">
  <link rel="stylesheet" href="/css/consent.css">
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-T4CCTF6V" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <a href="#main-content" class="skip-link">Aller au contenu principal</a>

  <header class="site-header" id="site-header">
    <div class="site-header__inner">
      <a href="/" class="header-brand"><span class="brand-blanc">#POURQUITU</span><span class="brand-rouge">VOTES?</span></a>
      <nav class="header-nav">
        <ul class="header-nav__links">
          <li><a href="/municipales/2026/">Comparateur</a></li>
          <li><a href="/municipales-2026/resultats/">R&eacute;sultats</a></li>
          <li><a href="/methodologie">M&eacute;thodologie</a></li>
          <li><a href="/faq">FAQ</a></li>
          <li><a href="/partis/">Partis</a></li>
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
    <nav class="mobile-menu-overlay__nav">
      <ul>
        <li><a href="/municipales/2026/"><i class="ph ph-scales"></i> Comparateur</a></li>
        <li><a href="/municipales-2026/resultats/"><i class="ph ph-chart-bar"></i> R&eacute;sultats</a></li>
        <li><a href="/methodologie"><i class="ph ph-book-open"></i> M&eacute;thodologie</a></li>
        <li><a href="/faq"><i class="ph ph-question"></i> FAQ</a></li>
        <li><a href="/partis/"><i class="ph ph-flag"></i> Partis</a></li>
        <li><a href="/a-propos"><i class="ph ph-info"></i> &Agrave; propos</a></li>
      </ul>
    </nav>
  </div>

  <main id="main-content">
    <section class="partis-hero" style="--parti-accent:{couleur}">
      <div class="partis-hero__inner">
        <nav class="fil-ariane fil-ariane--hero" aria-label="Fil d'Ariane">
          <ol class="fil-ariane__liste" itemscope itemtype="https://schema.org/BreadcrumbList">
            <li class="fil-ariane__item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
              <a href="/" itemprop="item"><i class="ph ph-house"></i><span itemprop="name">Accueil</span></a><meta itemprop="position" content="1">
            </li>
            <li class="fil-ariane__item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
              <a href="/partis/" itemprop="item"><span itemprop="name">Partis politiques</span></a><meta itemprop="position" content="2">
            </li>
            <li class="fil-ariane__item fil-ariane__item--actif" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
              <a href="{url}" itemprop="item"><span itemprop="name">{esc(nom)}</span></a><meta itemprop="position" content="3">
            </li>
          </ol>
        </nav>

        <div class="partip__hero-header">
          <div class="partip__sigle-big" style="background:{couleur}">{esc(sigle)}</div>
          <div>
            <h1 class="partip__title">{esc(nom)}</h1>
            <p class="partip__subtitle"><i class="ph ph-user"></i> {esc(leader)} &middot; {esc(positionnement)} &middot; Fond&eacute; en {esc(fondation)}</p>
          </div>
        </div>
        <div class="partip__tags">{tags_html}</div>
      </div>
    </section>

    <div class="partip__content">
      <div class="partip__grid">

        <div class="partip__main">
          <section class="partip__section">
            <h2><i class="ph ph-target" aria-hidden="true"></i> Positionnement sur 6 axes</h2>
            <div class="partip__positions">{positions_html}
            </div>
          </section>

          <section class="partip__section">
            <h2><i class="ph ph-list-checks" aria-hidden="true"></i> Programme national — Points cl&eacute;s</h2>
            <ol class="partip__programme">
{programme_html}            </ol>
          </section>

          <section class="partip__section">
            <h2><i class="ph ph-clock-counter-clockwise" aria-hidden="true"></i> Histoire</h2>
            <div class="partip__histoire">{esc(histoire)}</div>
          </section>
        </div>

        <aside class="partip__sidebar">
          <div class="partip__sidebar-card">
            <h3>R&eacute;sultats &eacute;lectoraux</h3>
            {res_html}
          </div>

          <div class="partip__sidebar-card">
            <h3>Figures cl&eacute;s</h3>
            <p>{figures_html}</p>
          </div>

          {"<div class='partip__sidebar-card'><h3>Site officiel</h3><p><a href='" + esc(site) + "' target='_blank' rel='noopener'>" + esc(site) + " <i class='ph ph-arrow-square-out'></i></a></p></div>" if site else ""}

          <div class="partip__sidebar-card">
            <h3>Voir aussi</h3>
            <p><a href="/partis/">← Tous les partis</a></p>
            <p><a href="/municipales/2026/">Comparateur municipales</a></p>
          </div>
        </aside>

      </div>
    </div>
  </main>

  <footer class="footer" role="contentinfo">
    <div class="footer__inner">
      <div class="footer__grid">
        <div class="footer__brand">
          <a href="/" class="footer__logo" aria-label="Accueil"><span class="logo__hash">#</span><span class="logo__pourquitu">POURQUITU</span><span class="logo__votes">VOTES</span><span class="logo__question">?</span></a>
          <p class="footer__tagline">Comparez les programmes des candidats. Projet citoyen, ind&eacute;pendant et non-partisan.</p>
        </div>
        <div class="footer__col">
          <h3 class="footer__col-title">Municipales 2026</h3>
          <ul class="footer__list">
            <li><a href="/municipales-2026/paris/">Paris</a></li>
            <li><a href="/municipales-2026/lyon/">Lyon</a></li>
            <li><a href="/municipales-2026/marseille/">Marseille</a></li>
            <li><a href="/municipales/2026/" class="footer__link--all">Toutes les villes</a></li>
          </ul>
        </div>
        <div class="footer__col">
          <h3 class="footer__col-title">Enjeux &amp; &Eacute;lections</h3>
          <ul class="footer__list">
            <li><a href="/municipales-2026/resultats/">R&eacute;sultats des municipales</a></li>
            <li><a href="/partis/">Partis politiques</a></li>
            <li><a href="/presidentielle/2027/">Pr&eacute;sidentielle 2027</a></li>
          </ul>
        </div>
        <div class="footer__col">
          <h3 class="footer__col-title">Le projet</h3>
          <ul class="footer__list">
            <li><a href="/a-propos">&Agrave; propos</a></li>
            <li><a href="/methodologie">M&eacute;thodologie</a></li>
            <li><a href="/faq">FAQ</a></li>
            <li><a href="mailto:contact@pourquituvotes.fr">Contact</a></li>
          </ul>
        </div>
      </div>
      <div class="footer__bottom">
        <p>&copy; 2026 #POURQUITUVOTES &mdash; Projet citoyen ind&eacute;pendant</p>
        <div class="footer__legal">
          <a href="/mentions-legales">Mentions l&eacute;gales</a>
          <a href="/confidentialite">Confidentialit&eacute;</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    var b=document.getElementById("burger-btn"),m=document.getElementById("mobile-menu"),c=document.getElementById("mobile-menu-close");
    if(b&&m){{b.addEventListener("click",function(){{m.hidden=false;document.body.style.overflow="hidden"}});if(c)c.addEventListener("click",function(){{m.hidden=true;document.body.style.overflow=""}})}}
  </script>
  <script defer src="/js/consent.min.js"></script>
  <script defer src="/js/burger-search.js?v={DATA_VERSION}"></script>
  <script defer src="/js/contribuer.js"></script>
</body>
</html>"""


def main():
    data = load_json(os.path.join(ROOT, "data", "partis.json"))
    partis_list = data["partis"]

    for parti in partis_list:
        pid = parti["id"]
        out_dir = os.path.join(ROOT, "partis", pid)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        html = generate_page(parti)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  OK /partis/{pid}/index.html")

    print(f"\n{len(partis_list)} pages générées.")


if __name__ == "__main__":
    main()
