#!/usr/bin/env python3
"""
Genere les images Open Graph (1200x630) pour pourquituvotes.fr
- 1 image par ville avec radar chart 12 axes (vraies donnees)
- 1 image par candidat avec couverture thematique
- 3 images generiques (home, comparateur, presidentielle)
Format: JPG qualite 90 dans img/og/
Polices: Montserrat (titres) + DM Sans (corps)
Cache: hash MD5, regenere uniquement si donnees modifiees
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os
import json
import hashlib

# === Configuration ===
W, H = 1200, 630
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")
OUT_DIR = os.path.join(ROOT_DIR, "img", "og")
DATA_DIR = os.path.join(ROOT_DIR, "data")
FONTS_DIR = os.path.join(ROOT_DIR, "fonts")
HASH_FILE = os.path.join(OUT_DIR, ".hashes.json")

# === Couleurs du site (identiques a style.css) ===
BLEU_DRAPEAU = "#002395"
ROUGE_DRAPEAU = "#ED2939"
FOND_TEXTE = "#1a1a2e"
ACCENT = "#2c3e6b"
ACCENT_LIGHT = "#4a5f94"
BLANC = "#FFFFFF"
GRIS_FOND = "#f0f2f5"
GRIS_BORDURE = "#d0d5dd"
SUCCESS = "#10b981"
WARNING = "#f59e0b"

# 12 labels courts avec accents
LABELS_COURTS = {
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
    "solidarite": "Solidarit\u00e9",
}

# Ordre des 12 categories (schema JSON)
CATEGORIES_ORDRE_SCHEMA = [
    "securite", "transports", "logement", "education",
    "environnement", "sante", "democratie", "economie",
    "culture", "sport", "urbanisme", "solidarite",
]

# Ordre consensuel (identique a ORDRE_CATEGORIES dans app.js ligne 103)
# Le site trie les categories dans cet ordre AVANT de rendre le radar
ORDRE_CATEGORIES = [
    "education", "environnement", "transports", "sante",
    "logement", "economie", "solidarite", "urbanisme",
    "culture", "sport", "democratie", "securite",
]

# Couleurs par parti (identique a COULEURS_PARTIS dans app.js)
COULEURS_PARTIS = {
    "lfi": "#A855F7", "la france insoumise": "#A855F7", "fiere et populaire": "#A855F7", "front populaire": "#A855F7",
    "pcf": "#FF2D9A", "communiste": "#FF2D9A",
    "ps": "#FF2D9A", "parti socialiste": "#FF2D9A", "gauche unie": "#FF2D9A", "printemps marseillais": "#FF2D9A", "union de la gauche": "#FF2D9A",
    "eelv": "#22C55E", "ecologistes": "#22C55E", "respire": "#22C55E", "pour vivre": "#22C55E",
    "modem": "#FFBF00", "centriste": "#FFBF00",
    "renaissance": "#FFBF00", "ensemble": "#FFBF00",
    "horizons": "#FFBF00",
    "lr": "#2D6EFF", "les republicains": "#2D6EFF", "union citoyenne de la droite": "#2D6EFF",
    "rn": "#1447E6", "rassemblement national": "#1447E6",
    "reconquete": "#FF6B00",
    "lo": "#A855F7", "lutte ouvriere": "#A855F7", "anticapitaliste": "#A855F7",
    "udr": "#2D6EFF", "ciotti": "#2D6EFF",
    "dvd": "#14B8A6", "divers droite": "#14B8A6",
    "dvg": "#FF2D9A", "divers gauche": "#FF2D9A",
    "se": "#14B8A6", "sans etiquette": "#14B8A6",
}
COULEUR_DEFAUT = "#2c3e6b"  # accent color

def get_candidate_color(liste_ou_parti):
    """Retourne la couleur du parti d'un candidat a partir de sa liste"""
    if not liste_ou_parti:
        return COULEUR_DEFAUT
    import unicodedata
    s = liste_ou_parti.lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    for key, color in COULEURS_PARTIS.items():
        if key in s:
            return color
    return COULEUR_DEFAUT


# === Polices ===
def get_font(name, size):
    paths = {
        "montserrat-black-italic": os.path.join(FONTS_DIR, "Montserrat-BlackItalic.ttf"),
        "montserrat-black": os.path.join(FONTS_DIR, "Montserrat-Black.ttf"),
        "montserrat-bold": os.path.join(FONTS_DIR, "Montserrat-Bold.ttf"),
        "montserrat-extrabold": os.path.join(FONTS_DIR, "Montserrat-ExtraBold.ttf"),
        "montserrat-semibold": os.path.join(FONTS_DIR, "Montserrat-SemiBold.ttf"),
        "montserrat": os.path.join(FONTS_DIR, "Montserrat-Regular.ttf"),
        "dm-sans-bold": os.path.join(FONTS_DIR, "DMSans-Bold.ttf"),
        "dm-sans-medium": os.path.join(FONTS_DIR, "DMSans-Medium.ttf"),
        "dm-sans": os.path.join(FONTS_DIR, "DMSans-Regular.ttf"),
    }
    path = paths.get(name)
    if path and os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.truetype(os.path.join(FONTS_DIR, "Montserrat-Bold.ttf"), size)


# === Dessin ===
def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def draw_fond_blanc(img):
    """Fond blanc comme le site, avec lisere tricolore en haut"""
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, H], fill=BLANC)
    # Lisere tricolore en haut (comme .hero border-top)
    tiers = W // 3
    draw.rectangle([0, 0, tiers, 4], fill=BLEU_DRAPEAU)
    draw.rectangle([tiers, 0, 2 * tiers, 4], fill=BLANC)
    draw.rectangle([2 * tiers, 0, W, 4], fill=ROUGE_DRAPEAU)


def draw_brand(draw, x=60, y=20, size=22, on_dark=False):
    """#POURQUITUVOTES? avec couleurs du site — Montserrat Black Italic (900)
    Site CSS: font-weight:900; font-style:italic; text-transform:uppercase
    <span class="brand-blanc">#POURQUITU</span><span class="brand-rouge">VOTES?</span>
    Sur fond blanc: #POURQUITU en noir (FOND_TEXTE), VOTES? en rouge
    Sur fond sombre: #POURQUITU en blanc, VOTES? en rouge
    """
    f = get_font("montserrat-black-italic", size)
    color_main = BLANC if on_dark else FOND_TEXTE
    parts = [("#POURQUITU", color_main), ("VOTES?", ROUGE_DRAPEAU)]
    cx = x
    for text, color in parts:
        draw.text((cx, y), text, fill=color, font=f)
        bbox = f.getbbox(text)
        cx += bbox[2] - bbox[0]


def draw_radar_chart(img, cx, cy, radius, n_axes, values, color_hex, alpha_pct=15):
    """Radar chart fidele au Chart.js du site.
    Dessine en supersampling 3x puis reduit pour antialiasing lisse.
    Lignes droites entre les points (comme Chart.js), pas de courbes.
    """
    SS = 3  # facteur de supersampling
    iw, ih = img.size

    # --- Grille (identique au site : 4 cercles a 25/50/75/100%) ---
    grid_layer = Image.new("RGBA", (iw, ih), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid_layer, "RGBA")
    grid_color = (229, 229, 229, 255)
    axis_color = (229, 229, 229, 140)
    for scale in [0.25, 0.50, 0.75, 1.0]:
        r = int(radius * scale)
        gdraw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=grid_color, width=1)
    for i in range(n_axes):
        a = (2 * math.pi * i / n_axes) - math.pi / 2
        ex = cx + math.cos(a) * radius
        ey = cy + math.sin(a) * radius
        gdraw.line([(cx, cy), (ex, ey)], fill=axis_color, width=1)
    img.alpha_composite(grid_layer)

    # --- Donnees (supersampling 3x pour lignes lisses) ---
    sw, sh = iw * SS, ih * SS
    ss_layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(ss_layer, "RGBA")

    scx, scy, sr = cx * SS, cy * SS, radius * SS
    pts = []
    for i, val in enumerate(values):
        a = (2 * math.pi * i / n_axes) - math.pi / 2
        v = max(0.0, min(1.0, val))  # 0% = centre, pas de minimum force
        pts.append((scx + math.cos(a) * sr * v, scy + math.sin(a) * sr * v))

    rv, gv, bv = hex_to_rgb(color_hex)
    fill_alpha = int(255 * alpha_pct / 100)

    # Fill (polygon = lignes droites)
    sdraw.polygon(pts, fill=(rv, gv, bv, fill_alpha))

    # Bordure : segments droits individuels (comme Chart.js, pas de joint="curve")
    border_w = round(2.5 * SS)  # 2.5px comme Chart.js borderWidth
    for i in range(len(pts)):
        p1 = pts[i]
        p2 = pts[(i + 1) % len(pts)]
        sdraw.line([p1, p2], fill=(rv, gv, bv, 220), width=border_w)

    # Points (radius 4px + bordure blanche 1px, comme Chart.js)
    point_r = 4 * SS
    border_r = point_r + 1 * SS  # 1px bordure blanche (Chart.js pointBorderWidth=1)
    for p in pts:
        sdraw.ellipse([p[0] - border_r, p[1] - border_r,
                       p[0] + border_r, p[1] + border_r],
                      fill=(255, 255, 255, 255))
        sdraw.ellipse([p[0] - point_r, p[1] - point_r,
                       p[0] + point_r, p[1] + point_r],
                      fill=(rv, gv, bv, 255))

    # Reduire avec LANCZOS pour antialiasing
    ss_layer = ss_layer.resize((iw, ih), Image.LANCZOS)
    img.alpha_composite(ss_layer)


def draw_radar_labels_12(draw, cx, cy, radius, labels, font_obj, on_dark=False):
    """Labels 12 axes autour du radar — DM Sans 600 comme le site.
    Positionnement intelligent pour eviter les collisions."""
    n = len(labels)
    label_color = (255, 255, 255, 204) if on_dark else (102, 102, 102, 255)
    padding = 22
    for i, lbl in enumerate(labels):
        a = (2 * math.pi * i / n) - math.pi / 2
        lx = cx + math.cos(a) * (radius + padding)
        ly = cy + math.sin(a) * (radius + padding)
        bbox = font_obj.getbbox(lbl)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Ancrage intelligent selon la position angulaire
        cos_a = math.cos(a)
        sin_a = math.sin(a)
        if abs(cos_a) < 0.15:  # haut/bas → centrer horizontalement
            tx = lx - tw / 2
        elif cos_a > 0:  # droite → aligner a gauche
            tx = lx
        else:  # gauche → aligner a droite
            tx = lx - tw
        if abs(sin_a) < 0.15:  # gauche/droite → centrer verticalement
            ty = ly - th / 2
        elif sin_a > 0:  # bas → en dessous
            ty = ly
        else:  # haut → au dessus
            ty = ly - th

        draw.text((tx, ty), lbl, fill=label_color, font=font_obj)


def draw_bottom_banner(draw, left_text="pourquituvotes.fr", right_text=""):
    """Bandeau bleu en bas (couleur drapeau)"""
    draw.rectangle([0, H - 44, W, H], fill=BLEU_DRAPEAU)
    draw.text((50, H - 34), left_text, fill=BLANC, font=get_font("montserrat-bold", 18))
    if right_text:
        f = get_font("dm-sans-medium", 15)
        bbox = f.getbbox(right_text)
        draw.text((W - (bbox[2] - bbox[0]) - 50, H - 33), right_text,
                  fill=(255, 255, 255, 200), font=f)


def draw_badge(draw, x, y, text, bg_color=SUCCESS, text_color=BLANC):
    f = get_font("montserrat-bold", 13)
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([x, y, x + tw + 20, y + 26], radius=13, fill=bg_color)
    draw.text((x + 10, y + 5), text, fill=text_color, font=f)
    return tw + 20


def draw_lisere_rouge(draw, x, y, w=80):
    """Petit trait rouge separateur (accent du site)"""
    draw.rounded_rectangle([x, y, x + w, y + 3], radius=1, fill=ROUGE_DRAPEAU)


# === Calcul densite thematique ===
def _sort_categories(election_data):
    """Trie les categories selon ORDRE_CATEGORIES (identique au sort() de app.js ligne 410).
    Retourne les categories triees (ne modifie pas l'original)."""
    cats = list(election_data.get("categories", []))
    def sort_key(cat):
        try:
            return ORDRE_CATEGORIES.index(cat["id"])
        except ValueError:
            return 999
    cats.sort(key=sort_key)
    return cats


def compute_city_radar_12(election_data):
    """Densité par catégorie pour une ville (moyenne de couverture).
    Ordre : ORDRE_CATEGORIES (comme le site)."""
    candidats = election_data.get("candidats", [])
    categories = _sort_categories(election_data)
    values = []
    for cat in categories:
        total, filled = 0, 0
        for st in cat.get("sousThemes", []):
            props = st.get("propositions", {})
            for cand in candidats:
                total += 1
                p = props.get(cand["id"])
                if p and isinstance(p, dict) and p.get("texte"):
                    filled += 1
        values.append(filled / total if total > 0 else 0)
    return values


def compute_candidate_radar_12(election_data, candidat_id):
    """Couverture par catégorie pour un candidat.
    Identique a calculerCouverture() du site :
      pct = Math.round(couverts / total * 100) → puis /100 pour ratio 0-1
    Ordre : ORDRE_CATEGORIES (comme le site)."""
    categories = _sort_categories(election_data)
    values = []
    for cat in categories:
        total = len(cat.get("sousThemes", []))
        if total == 0:
            values.append(0)
            continue
        filled = 0
        for st in cat.get("sousThemes", []):
            p = st.get("propositions", {}).get(candidat_id)
            if p and isinstance(p, dict) and p.get("texte"):
                filled += 1
        # Math.round() JS = round() Python, puis /100 pour ratio 0-1
        values.append(round(filled / total * 100) / 100)
    return values


def get_categories_labels(election_data):
    """Retourne les labels des categories dans ORDRE_CATEGORIES (comme le site)."""
    categories = _sort_categories(election_data)
    return [LABELS_COURTS.get(cat["id"], cat.get("nom", cat["id"]))
            for cat in categories]


# === Caching ===
def load_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return {}


def save_hashes(hashes):
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=2)


def file_hash(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def needs_regen(key, source_hash, hashes):
    if not os.path.exists(os.path.join(OUT_DIR, key)):
        return True
    return hashes.get(key) != source_hash


# === Calcul stats fiables depuis election_data ===
def compute_real_stats(election_data):
    """Calcule les stats directement depuis les donnees election (source de verite).
    Ne JAMAIS se fier a villes.json qui peut etre desynchronise."""
    candidats = election_data.get("candidats", [])
    categories = election_data.get("categories", [])
    n_cand = len(candidats)
    n_complets = sum(1 for c in candidats if c.get("programmeComplet"))
    n_props = 0
    n_themes = 0
    for cat in categories:
        cat_has_prop = False
        for st in cat.get("sousThemes", []):
            for cand in candidats:
                p = st.get("propositions", {}).get(cand["id"])
                if p and isinstance(p, dict) and p.get("texte"):
                    n_props += 1
                    cat_has_prop = True
        if cat_has_prop:
            n_themes += 1
    return {"candidats": n_cand, "propositions": n_props, "themes": n_themes, "complets": n_complets}


# === Generateurs d'images ===

def compute_thematiques_treemap(election_data):
    """Calcule le nombre de propositions par thematique (categorie).
    Retourne une liste triee par nb_propositions decroissant."""
    candidats = election_data.get("candidats", [])
    categories = _sort_categories(election_data)
    result = []
    for cat in categories:
        count = 0
        for st in cat.get("sousThemes", []):
            for cand in candidats:
                p = st.get("propositions", {}).get(cand["id"])
                if p and isinstance(p, dict) and p.get("texte"):
                    count += 1
        result.append({"id": cat["id"], "nom": LABELS_COURTS.get(cat["id"], cat["id"]),
                        "count": count})
    result.sort(key=lambda x: -x["count"])
    return result


# Couleurs des thematiques pour le treemap — palette flashy/vive (inspiree parti)
COULEURS_THEMATIQUES = {
    "education": "#FFBF00",       # jaune vif (Renaissance/MoDem)
    "environnement": "#22C55E",   # vert vif (EELV)
    "transports": "#2D6EFF",      # bleu franc (LR)
    "sante": "#ED2939",           # rouge drapeau
    "logement": "#A855F7",        # violet vif (LFI)
    "economie": "#FF6B00",        # orange vif (Reconquete)
    "solidarite": "#FF2D9A",      # rose vif (PS/PCF)
    "urbanisme": "#14B8A6",       # teal vif
    "culture": "#E040FB",         # magenta vif
    "sport": "#00E5FF",           # cyan electrique
    "democratie": "#00E676",      # vert emeraude vif
    "securite": "#536DFE",        # indigo vif
}

# Phosphor icon codepoints
PHOSPHOR_ICONS = {
    "transports": 0xe106,     # bus
    "environnement": 0xe2da,  # leaf
    "education": 0xe62c,      # graduation-cap
    "securite": 0xe40c,       # shield-check
    "economie": 0xe0ee,       # briefcase
    "logement": 0xe2c2,       # house
    "sante": 0xe2ac,          # heartbeat
    "culture": 0xe6c8,        # palette
    "sport": 0xe716,          # soccer-ball
    "urbanisme": 0xe102,      # buildings
    "democratie": 0xe0b4,     # bank
    "solidarite": 0xe582,     # handshake
}


def generate_city_image(ville_id, ville_nom, election_data, stats):
    """Treemap thematique : fond bleu, colonne gauche infos, colonne droite treemap"""
    img = Image.new("RGBA", (W, H))
    pad = 45

    # === FOND : degrade bleu 135deg ===
    draw_gradient_rect(img, 0, 0, W, H,
                       hex_to_rgb("#002395"), hex_to_rgb("#001a6e"))

    # === Calque semi-transparent ===
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay, "RGBA")

    # Badge "Municipales 2026" en haut a droite
    badge_text = "Municipales 2026"
    f_badge = get_font("dm-sans-medium", 14)
    bb = f_badge.getbbox(badge_text)
    bw = bb[2] - bb[0]
    bx = W - pad - bw - 40
    odraw.rounded_rectangle([bx, pad - 12, bx + bw + 40, pad + 22],
                            radius=25, fill=(255, 255, 255, 38))

    # Stats cards (colonne, gauche)
    n_cand = stats["candidats"]
    n_props = stats["propositions"]
    n_themes = stats["themes"]
    card_data = [
        (str(n_cand), "candidats"),
        (str(n_props), "propositions"),
        (str(n_themes), "th\u00e9matiques"),
    ]
    city_col_w = 320
    card_x = pad
    card_y_start = 180  # sera ajuste apres le nom de ville
    card_w = city_col_w - 10
    card_h = 52
    card_gap = 12

    for i, (val, label) in enumerate(card_data):
        cy = card_y_start + i * (card_h + card_gap)
        odraw.rounded_rectangle([card_x, cy, card_x + card_w, cy + card_h],
                                radius=12, fill=(255, 255, 255, 26))

    # Composer les overlays
    img = Image.alpha_composite(img, overlay)

    # === Texte opaque ===
    draw = ImageDraw.Draw(img, "RGBA")

    # Header : Logo + Badge
    draw_brand(draw, x=pad, y=pad - 8, size=22, on_dark=True)
    draw.text((bx + 20, pad - 4), badge_text, fill=BLANC, font=f_badge)

    # Nom de la ville (colonne gauche)
    main_y = pad + 50
    city_text = ville_nom.upper()
    f_city = get_font("montserrat-black", 72)
    bbox_city = f_city.getbbox(city_text)
    city_w = bbox_city[2] - bbox_city[0]
    if city_w > city_col_w:
        f_city = get_font("montserrat-black", 56)
        bbox_city = f_city.getbbox(city_text)
        city_w = bbox_city[2] - bbox_city[0]
    if city_w > city_col_w:
        f_city = get_font("montserrat-black", 42)
    draw.text((pad, main_y), city_text, fill=BLANC, font=f_city)

    # Stats dans les cards
    f_card_val = get_font("montserrat-extrabold", 32)
    f_card_lbl = get_font("dm-sans", 13)
    for i, (val, label) in enumerate(card_data):
        cy = card_y_start + i * (card_h + card_gap)
        # Valeur a gauche
        draw.text((card_x + 20, cy + 8), val, fill=BLANC, font=f_card_val)
        # Label a droite de la valeur
        bb_v = f_card_val.getbbox(val)
        vw = bb_v[2] - bb_v[0]
        draw.text((card_x + 20 + vw + 15, cy + 17), label,
                  fill=(255, 255, 255, 204), font=f_card_lbl)

    # === COLONNE DROITE : Treemap ===
    treemap_x = pad + city_col_w + 40
    treemap_y = pad + 140  # bien plus bas
    treemap_w = W - treemap_x - pad
    treemap_h_label = 25

    # Titre "Thematiques les plus debattues"
    f_treemap_title = get_font("dm-sans", 13)
    draw.text((treemap_x, treemap_y - 5),
              "TH\u00c9MATIQUES LES PLUS D\u00c9BATTUES",
              fill=(255, 255, 255, 178), font=f_treemap_title)

    treemap_top = treemap_y + treemap_h_label + 5
    treemap_h = H - treemap_top - pad - 15  # espace footer reduit
    gap = 4

    # Calculer les thematiques triees
    themes = compute_thematiques_treemap(election_data)
    # Garder seulement les themes avec propositions
    themes = [t for t in themes if t["count"] > 0]

    # Cas special : aucune proposition — afficher message "a venir"
    if not themes:
        f_avenir = get_font("dm-sans-bold", 22)
        f_sub = get_font("dm-sans", 14)
        msg1 = "Propositions \u00e0 venir"
        msg2 = "Les programmes seront ajout\u00e9s d\u00e8s publication"
        bb1 = f_avenir.getbbox(msg1)
        bb2 = f_sub.getbbox(msg2)
        cx_msg = treemap_x + treemap_w // 2
        cy_msg = treemap_top + treemap_h // 2
        # Fond semi-transparent
        cdraw_avenir = ImageDraw.Draw(Image.new("RGBA", (W, H), (0, 0, 0, 0)), "RGBA")
        avenir_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ad = ImageDraw.Draw(avenir_layer, "RGBA")
        box_w, box_h = max(bb1[2] - bb1[0], bb2[2] - bb2[0]) + 60, 90
        ad.rounded_rectangle([cx_msg - box_w // 2, cy_msg - box_h // 2,
                               cx_msg + box_w // 2, cy_msg + box_h // 2],
                              radius=16, fill=(255, 255, 255, 25))
        img = Image.alpha_composite(img, avenir_layer)
        draw = ImageDraw.Draw(img, "RGBA")
        w1 = bb1[2] - bb1[0]
        w2 = bb2[2] - bb2[0]
        draw.text((cx_msg - w1 // 2, cy_msg - 30), msg1, fill=BLANC, font=f_avenir)
        draw.text((cx_msg - w2 // 2, cy_msg + 5), msg2, fill=(255, 255, 255, 153), font=f_sub)
        # Footer
        footer_y = H - pad + 5
        draw.text((pad, footer_y), "pourquituvotes.fr",
                  fill=(255, 255, 255, 178), font=get_font("dm-sans-medium", 14))
        date_text = "15 mars 2026 \u00b7 Jour de vote"
        f_date = get_font("dm-sans-medium", 14)
        bb_d = f_date.getbbox(date_text)
        draw.text((W - pad - (bb_d[2] - bb_d[0]), footer_y), date_text,
                  fill=(255, 255, 255, 178), font=f_date)
        img.convert("RGB").save(os.path.join(OUT_DIR, "%s.jpg" % ville_id), "JPEG", quality=90)
        return

    # Assigner tailles : XL (top 1), L (top 2-3), M (top 4-6), S (reste)
    n_themes_shown = min(len(themes), 12)
    sizes = []
    for i in range(n_themes_shown):
        if i == 0:
            sizes.append("XL")
        elif i <= 2:
            sizes.append("L")
        elif i <= 5:
            sizes.append("M")
        else:
            sizes.append("S")

    # Pour les villes avec peu de themes, reduire la grille
    if n_themes_shown <= 3:
        cols = 3
    else:
        cols = 6
    col_w = (treemap_w - gap * (cols - 1)) / cols

    # Build cell positions
    cells = []
    for i in range(n_themes_shown):
        cells.append({
            "theme": themes[i],
            "size": sizes[i],
            "color": COULEURS_THEMATIQUES.get(themes[i]["id"], "#6366F1"),
            "icon": PHOSPHOR_ICONS.get(themes[i]["id"], 0xe2da),
        })

    # Position cells using a grid occupancy tracker
    if cols == 3:
        SIZE_SPANS = {"XL": (2, 2), "L": (1, 1), "M": (1, 1), "S": (1, 1)}
    else:
        SIZE_SPANS = {"XL": (3, 2), "L": (2, 1), "M": (1, 1), "S": (1, 1)}

    # Phase 1: dry-run placement to find actual rows needed
    dry_grid = [[False] * cols for _ in range(12)]

    def _find_slot(grid_ref, span_c, span_r):
        for r in range(len(grid_ref)):
            for c in range(cols - span_c + 1):
                if all(not grid_ref[r + dr][c + dc]
                       for dr in range(span_r) for dc in range(span_c)
                       if r + dr < len(grid_ref)):
                    return (r, c)
        return None

    def _mark_slot(grid_ref, r, c, span_c, span_r):
        for dr in range(span_r):
            for dc in range(span_c):
                if r + dr < len(grid_ref):
                    grid_ref[r + dr][c + dc] = True

    max_row_used = 0
    cell_positions = []
    for cell in cells:
        span_c, span_r = SIZE_SPANS[cell["size"]]
        slot = _find_slot(dry_grid, span_c, span_r)
        if not slot:
            cell_positions.append(None)
            continue
        r, c = slot
        _mark_slot(dry_grid, r, c, span_c, span_r)
        cell_positions.append((r, c, span_c, span_r))
        max_row_used = max(max_row_used, r + span_r - 1)

    # Recalculate row height with actual rows needed
    n_rows = max_row_used + 1
    row_h_unit = (treemap_h - gap * (n_rows - 1)) / n_rows

    phosphor_font_cache = {}

    def get_phosphor(size):
        if size not in phosphor_font_cache:
            path = os.path.join(FONTS_DIR, "Phosphor.ttf")
            if os.path.exists(path):
                phosphor_font_cache[size] = ImageFont.truetype(path, size)
            else:
                phosphor_font_cache[size] = get_font("dm-sans-bold", size)
        return phosphor_font_cache[size]

    cell_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(cell_overlay, "RGBA")

    for i, cell in enumerate(cells):
        pos = cell_positions[i]
        if not pos:
            continue
        r, c, span_c, span_r = pos

        # Cell rectangle
        cx = treemap_x + c * (col_w + gap)
        cy = treemap_top + r * (row_h_unit + gap)
        cw = span_c * col_w + (span_c - 1) * gap
        ch = span_r * row_h_unit + (span_r - 1) * gap

        # Cell background (couleur pleine, opaque)
        rv, gv, bv = hex_to_rgb(cell["color"])
        cdraw.rounded_rectangle([cx, cy, cx + cw, cy + ch],
                                radius=8, fill=(rv, gv, bv, 240))

        # Icon + text sizing based on cell size
        if cell["size"] == "XL":
            icon_sz, name_sz, count_sz = 36, 14, 28
        elif cell["size"] == "L":
            icon_sz, name_sz, count_sz = 26, 11, 20
        elif cell["size"] == "M":
            icon_sz, name_sz, count_sz = 22, 10, 16
        else:
            icon_sz, name_sz, count_sz = 18, 9, 13

        # Draw icon
        f_icon = get_phosphor(icon_sz)
        icon_char = chr(cell["icon"])
        ib = f_icon.getbbox(icon_char)
        iw = ib[2] - ib[0]

        # Center all content vertically
        f_name = get_font("dm-sans-bold", name_sz)
        f_count = get_font("montserrat-extrabold", count_sz)
        name_text = cell["theme"]["nom"]
        count_text = str(cell["theme"]["count"])

        nb = f_name.getbbox(name_text)
        cb = f_count.getbbox(count_text)
        total_h = icon_sz + 4 + (nb[3] - nb[1]) + 2 + (cb[3] - cb[1])
        start_y = cy + (ch - total_h) / 2

        # Icon centered
        cdraw.text((cx + (cw - iw) / 2, start_y),
                   icon_char, fill=(255, 255, 255, 230), font=f_icon)

        # Name centered
        nw = nb[2] - nb[0]
        if nw > cw - 6:
            # Truncate
            while nw > cw - 10 and len(name_text) > 3:
                name_text = name_text[:-1]
                nb = f_name.getbbox(name_text + "..")
                nw = nb[2] - nb[0]
            name_text += ".."
            nw = f_name.getbbox(name_text)[2] - f_name.getbbox(name_text)[0]
        cdraw.text((cx + (cw - nw) / 2, start_y + icon_sz + 4),
                   name_text, fill=(255, 255, 255, 230), font=f_name)

        # Count centered
        cntw = cb[2] - cb[0]
        cdraw.text((cx + (cw - cntw) / 2, start_y + icon_sz + 4 + (nb[3] - nb[1]) + 2),
                   count_text, fill=(255, 255, 255, 255), font=f_count)

    img = Image.alpha_composite(img, cell_overlay)

    # === FOOTER ===
    draw = ImageDraw.Draw(img, "RGBA")
    footer_y = H - pad + 5
    draw.text((pad, footer_y), "pourquituvotes.fr",
              fill=(255, 255, 255, 178), font=get_font("dm-sans-medium", 14))
    mention = "Donn\u00e9es issues des programmes officiels des candidats"
    f_mention = get_font("dm-sans", 11)
    bb_m = f_mention.getbbox(mention)
    draw.text((W - pad - (bb_m[2] - bb_m[0]), footer_y + 2), mention,
              fill=(255, 255, 255, 120), font=f_mention)

    img.convert("RGB").save(os.path.join(OUT_DIR, "%s.jpg" % ville_id), "JPEG", quality=90)


def draw_gradient_rect(img, x0, y0, x1, y1, color_top, color_bottom):
    """Degrade vertical (ou 135deg approxime) entre deux couleurs RGB."""
    draw = ImageDraw.Draw(img, "RGBA")
    h = y1 - y0
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * t)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * t)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * t)
        draw.line([(x0, y0 + y), (x1, y0 + y)], fill=(r, g, b, 255))


def generate_candidate_image(ville_id, ville_nom, candidat, election_data):
    """Option A : Split gauche (bleu degrade) / droite (gris clair + radar)"""
    img = Image.new("RGBA", (W, H))
    half = W // 2  # 600px

    # === COLONNE GAUCHE : fond bleu degrade ===
    draw_gradient_rect(img, 0, 0, half, H,
                       hex_to_rgb("#002395"), hex_to_rgb("#001a6e"))
    draw = ImageDraw.Draw(img, "RGBA")

    pad = 40  # padding interieur gauche

    # Logo en haut (plus grand)
    draw_brand(draw, x=pad, y=28, size=26, on_dark=True)

    # Calculer stats avant de dessiner (pour connaitre la hauteur totale)
    n_props = 0
    n_themes = 0
    for cat in election_data.get("categories", []):
        cat_has = False
        for st in cat.get("sousThemes", []):
            p = st.get("propositions", {}).get(candidat["id"])
            if p and isinstance(p, dict) and p.get("texte"):
                n_props += 1
                cat_has = True
        if cat_has:
            n_themes += 1

    cand_color = get_candidate_color(candidat.get("liste", ""))
    cr, cg, cb = hex_to_rgb(cand_color)

    # Preparer le nom (mesurer pour savoir s'il faut reduire)
    name_text = candidat["nom"].upper()
    f_name = get_font("montserrat-extrabold", 36)
    bbox_name = f_name.getbbox(name_text)
    name_w = bbox_name[2] - bbox_name[0]
    name_h = bbox_name[3] - bbox_name[1]
    multiline_name = False
    if name_w > half - 2 * pad:
        f_name = get_font("montserrat-extrabold", 28)
        bbox_name = f_name.getbbox(name_text)
        name_w = bbox_name[2] - bbox_name[0]
        name_h = bbox_name[3] - bbox_name[1]
    if name_w > half - 2 * pad:
        multiline_name = True
        f_name = get_font("montserrat-extrabold", 30)

    # Hauteur totale du bloc candidat : nom + ville + parti + stats
    # nom ~45, gap 16, ville ~20, gap 8, parti ~18, gap 30, stats(val+lbl) ~58
    bloc_h = (45 if not multiline_name else 83) + 16 + 20 + 8 + 18 + 30 + 58
    # Centrer verticalement entre logo (y=70) et footer (y=H-45)
    zone_top = 70
    zone_bottom = H - 45
    bloc_y = zone_top + (zone_bottom - zone_top - bloc_h) // 2

    # === Dessiner le bloc candidat centre ===

    # Nom du candidat
    name_y = bloc_y
    if multiline_name:
        parts = name_text.split(" ", 1)
        draw.text((pad, name_y), parts[0], fill=BLANC, font=f_name)
        if len(parts) > 1:
            draw.text((pad, name_y + 38), parts[1], fill=BLANC, font=f_name)
        name_bottom = name_y + 76
    else:
        draw.text((pad, name_y), name_text, fill=BLANC, font=f_name)
        name_bottom = name_y + 45

    # Ville (plus grand)
    ville_y = name_bottom + 16
    draw.text((pad, ville_y), ville_nom,
              fill=(255, 255, 255, 204), font=get_font("dm-sans-medium", 20))

    # Parti politique avec ligne couleur (alignee au centre du texte)
    parti_y = ville_y + 28
    liste = candidat.get("liste", "")
    if len(liste) > 40:
        liste = liste[:37] + "..."
    f_parti = get_font("dm-sans", 14)
    bb_parti = f_parti.getbbox(liste)
    text_h = bb_parti[3] - bb_parti[1]
    chip_cy = parti_y + text_h // 2  # centre vertical du texte
    draw.rounded_rectangle([pad, chip_cy - 2, pad + 30, chip_cy + 2],
                           radius=2, fill=(cr, cg, cb, 255))
    draw.text((pad + 42, parti_y), liste,
              fill=(255, 255, 255, 178), font=f_parti)

    # Stats
    stats_y = parti_y + 40
    f_stat_val = get_font("montserrat-extrabold", 32)
    f_stat_lbl = get_font("dm-sans", 11)
    draw.text((pad, stats_y), str(n_props), fill=BLANC, font=f_stat_val)
    draw.text((pad, stats_y + 42), "PROPOSITIONS",
              fill=(255, 255, 255, 178), font=f_stat_lbl)
    sx2 = pad + 160
    draw.text((sx2, stats_y), str(n_themes), fill=BLANC, font=f_stat_val)
    draw.text((sx2, stats_y + 42), "TH\u00c9MATIQUES",
              fill=(255, 255, 255, 178), font=f_stat_lbl)

    # Footer en bas
    draw.text((pad, H - 35), "pourquituvotes.fr \u00b7 Municipales 2026",
              fill=(255, 255, 255, 153), font=get_font("dm-sans", 12))
    mention_c = "Donn\u00e9es issues des programmes officiels des candidats"
    f_mc = get_font("dm-sans", 10)
    bb_mc = f_mc.getbbox(mention_c)
    draw.text((pad, H - 20), mention_c,
              fill=(255, 255, 255, 100), font=f_mc)

    # === COLONNE DROITE : fond gris clair + radar ===
    draw.rectangle([half, 0, W, H], fill=hex_to_rgb("#f8fafc"))

    # Radar centre dans la colonne droite (~90% de l'espace)
    radar_cx = half + (W - half) // 2  # centre horizontal = 900
    radar_cy = H // 2                   # centre vertical = 315
    radar_r = int(min(W - half, H) * 0.35)  # ~210px

    radar_values = compute_candidate_radar_12(election_data, candidat["id"])
    n_cats = len(radar_values)
    draw_radar_chart(img, radar_cx, radar_cy, radar_r, n_cats, radar_values,
                     cand_color, alpha_pct=15)
    draw = ImageDraw.Draw(img, "RGBA")
    labels = get_categories_labels(election_data)
    draw_radar_labels_12(draw, radar_cx, radar_cy, radar_r, labels,
                         get_font("dm-sans-bold", 11))

    filename = "%s-%s.jpg" % (ville_id, candidat["id"])
    img.convert("RGB").save(os.path.join(OUT_DIR, filename), "JPEG", quality=90)


def generate_home_image(total_villes, total_candidats, total_propositions):
    img = Image.new("RGBA", (W, H))
    draw_fond_blanc(img)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_brand(draw, x=50, y=18, size=24)

    draw.text((50, 75), "Comparez les programmes", fill=FOND_TEXTE,
              font=get_font("montserrat-extrabold", 48))
    draw.text((50, 135), "des candidats aux municipales", fill=FOND_TEXTE,
              font=get_font("montserrat-bold", 38))
    draw.text((50, 195), "Projet citoyen, independant et non-partisan",
              fill=hex_to_rgb(ACCENT_LIGHT), font=get_font("dm-sans-medium", 20))
    draw_lisere_rouge(draw, 50, 235)

    f_val = get_font("montserrat-bold", 42)
    f_lbl = get_font("dm-sans", 16)
    sx = 50
    for val, label in [(str(total_villes), "villes"),
                       (str(total_candidats), "candidats"),
                       (str(total_propositions), "propositions")]:
        draw.text((sx, 260), val, fill=FOND_TEXTE, font=f_val)
        bbox = f_val.getbbox(val)
        draw.text((sx, 310), label, fill=hex_to_rgb(ACCENT_LIGHT), font=f_lbl)
        sx += bbox[2] - bbox[0] + 60

    # Radar decoratif 12 axes (2 datasets superposes comme la page d'accueil)
    rcx, rcy, rr = 930, 310, 180
    draw_radar_chart(img, rcx, rcy, rr, 12, [0.7, 0.85, 0.6, 0.9, 0.5, 0.65, 0.4, 0.75, 0.55, 0.8, 0.45, 0.7], ACCENT, alpha_pct=15)
    draw_radar_chart(img, rcx, rcy, rr, 12, [0.5, 0.4, 0.75, 0.55, 0.8, 0.9, 0.6, 0.3, 0.7, 0.5, 0.65, 0.45], ROUGE_DRAPEAU, alpha_pct=10)
    draw = ImageDraw.Draw(img, "RGBA")
    labels = [LABELS_COURTS.get(c, c) for c in ORDRE_CATEGORIES]
    draw_radar_labels_12(draw, rcx, rcy, rr, labels, get_font("dm-sans-bold", 9))

    draw_bottom_banner(draw, "pourquituvotes.fr", "15 mars 2026 - Jour de vote")

    img.convert("RGB").save(os.path.join(OUT_DIR, "home.jpg"), "JPEG", quality=90)


def generate_comparateur_image():
    img = Image.new("RGBA", (W, H))
    draw_fond_blanc(img)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_brand(draw, x=50, y=18, size=24)

    draw.text((50, 75), "Comparateur de programmes", fill=FOND_TEXTE,
              font=get_font("montserrat-extrabold", 44))
    draw.text((50, 132), "Municipales 2026", fill=FOND_TEXTE,
              font=get_font("montserrat-bold", 36))
    draw.text((50, 190), "Analysez les propositions candidat par candidat",
              fill=hex_to_rgb(ACCENT_LIGHT), font=get_font("dm-sans-medium", 20))
    draw_lisere_rouge(draw, 50, 230)

    # Mini tableau stylise (couleurs du site)
    tx, ty, cw, rh = 50, 260, 165, 38
    headers = ["Theme", "Candidat A", "Candidat B", "Candidat C"]
    rows = ["Securite", "Transports", "Logement", "Ecologie"]
    f_h = get_font("dm-sans-bold", 13)
    f_r = get_font("dm-sans", 12)
    for i, h in enumerate(headers):
        x = tx + i * (cw + 6)
        draw.rounded_rectangle([x, ty, x + cw, ty + rh], radius=4, fill=hex_to_rgb(GRIS_FOND))
        draw.text((x + 10, ty + 10), h, fill=FOND_TEXTE, font=f_h)
    colors_bar = [ACCENT, SUCCESS, WARNING]
    bases = [0.8, 0.6, 0.7]
    for ri, rl in enumerate(rows):
        ry = ty + (ri + 1) * (rh + 4)
        draw.rounded_rectangle([tx, ry, tx + cw, ry + rh], radius=4, fill=(245, 247, 250, 255))
        draw.text((tx + 10, ry + 10), rl, fill=hex_to_rgb(ACCENT_LIGHT), font=f_r)
        for ci in range(3):
            cx = tx + (ci + 1) * (cw + 6)
            draw.rounded_rectangle([cx, ry, cx + cw, ry + rh], radius=4, fill=(250, 251, 253, 255))
            val = min(1.0, bases[ci] + ri * 0.06 * (1 if ci % 2 == 0 else -1))
            bw = int((cw - 14) * val)
            r, g, b = hex_to_rgb(colors_bar[ci])
            if bw > 5:
                draw.rounded_rectangle([cx + 7, ry + 10, cx + 7 + bw, ry + rh - 10],
                                       radius=3, fill=(r, g, b, 180))

    # Radar decoratif (petit, sans labels)
    rcx, rcy, rr = 1000, 160, 70
    draw_radar_chart(img, rcx, rcy, rr, 12, [0.8, 0.6, 0.9, 0.5, 0.7, 0.85, 0.4, 0.75, 0.6, 0.8, 0.5, 0.7], ACCENT, alpha_pct=15)
    draw = ImageDraw.Draw(img, "RGBA")

    draw_bottom_banner(draw, "pourquituvotes.fr", "Comparez. Decidez. Votez.")

    img.convert("RGB").save(os.path.join(OUT_DIR, "comparateur.jpg"), "JPEG", quality=90)


def generate_presidentielle_image():
    img = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(img, "RGBA")
    # Fond sombre special pour la presidentielle
    draw.rectangle([0, 0, W, H], fill=hex_to_rgb(FOND_TEXTE))
    # Lisere tricolore
    tiers = W // 3
    draw.rectangle([0, 0, tiers, 4], fill=BLEU_DRAPEAU)
    draw.rectangle([tiers, 0, 2 * tiers, 4], fill=BLANC)
    draw.rectangle([2 * tiers, 0, W, 4], fill=ROUGE_DRAPEAU)

    draw_brand(draw, x=50, y=18, size=24, on_dark=True)

    # Bandes drapeau en fond
    draw.rectangle([0, 0, 10, H], fill=hex_to_rgb(BLEU_DRAPEAU) + (30,))
    draw.rectangle([W - 10, 0, W, H], fill=hex_to_rgb(ROUGE_DRAPEAU) + (30,))

    # Drapeau stylise
    fx, fy, fw, fh = 740, 140, 340, 230
    draw.rectangle([fx, fy, fx + fw // 3, fy + fh], fill=hex_to_rgb(BLEU_DRAPEAU) + (100,))
    draw.rectangle([fx + fw // 3, fy, fx + 2 * fw // 3, fy + fh], fill=(255, 255, 255, 80))
    draw.rectangle([fx + 2 * fw // 3, fy, fx + fw, fy + fh], fill=hex_to_rgb(ROUGE_DRAPEAU) + (100,))
    draw.rounded_rectangle([fx - 2, fy - 2, fx + fw + 2, fy + fh + 2],
                           radius=8, outline=(255, 255, 255, 40), width=2)

    draw.text((50, 120), "Presidentielle", fill=BLANC, font=get_font("montserrat-extrabold", 52))
    draw.text((50, 185), "2027", fill=BLANC, font=get_font("montserrat-extrabold", 68))
    draw.text((50, 280), "Le comparateur des programmes",
              fill=(255, 255, 255, 200), font=get_font("dm-sans-medium", 22))
    draw.text((50, 315), "pour l'election presidentielle",
              fill=(255, 255, 255, 200), font=get_font("dm-sans-medium", 22))
    draw_badge(draw, 50, 370, "BIENTOT DISPONIBLE", bg_color=WARNING, text_color=FOND_TEXTE)

    draw_bottom_banner(draw, "pourquituvotes.fr", "Printemps 2027")

    img.convert("RGB").save(os.path.join(OUT_DIR, "presidentielle-2027.jpg"), "JPEG", quality=90)


def _draw_duel_radar_hd(img, cx, cy, radius, n_axes, values1, color1_hex, values2, color2_hex):
    """Radar duel HD : grille + 2 datasets, tout en supersampling 4x.
    Identique au Chart.js du site : circular grid, borderWidth 2.5, pointRadius 4,
    fill alpha 15%, grille #e5e5e5, axes #e5e5e5."""
    SS = 4  # supersampling 4x pour lignes parfaitement lisses
    iw, ih = img.size
    sw, sh = iw * SS, ih * SS
    layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")

    scx, scy, sr = cx * SS, cy * SS, radius * SS

    # Couleurs grille (identiques au site light mode)
    grid_col = (229, 229, 229, 255)   # #e5e5e5
    axis_col = (229, 229, 229, 180)   # #e5e5e5 un peu transparent

    # --- Grille : 4 cercles concentriques (circular: true comme Chart.js) ---
    for scale in [0.25, 0.50, 0.75, 1.0]:
        r = int(sr * scale)
        w = round(1.2 * SS) if scale == 1.0 else round(0.8 * SS)
        d.ellipse([scx - r, scy - r, scx + r, scy + r], outline=grid_col, width=w)

    # --- Axes (lignes du centre vers chaque sommet) ---
    for i in range(n_axes):
        a = (2 * math.pi * i / n_axes) - math.pi / 2
        ex = scx + math.cos(a) * sr
        ey = scy + math.sin(a) * sr
        d.line([(scx, scy), (ex, ey)], fill=axis_col, width=round(0.8 * SS))

    # --- Helper dataset ---
    def draw_dataset(values, color_hex):
        rv, gv, bv = hex_to_rgb(color_hex)
        pts = []
        for i, val in enumerate(values):
            a = (2 * math.pi * i / n_axes) - math.pi / 2
            v = max(0.0, min(1.0, val))
            pts.append((scx + math.cos(a) * sr * v, scy + math.sin(a) * sr * v))

        # Fill (alpha 15% = 38/255, comme hexToRgba(color, 0.15) du site)
        d.polygon(pts, fill=(rv, gv, bv, 38))

        # Bordure 2.5px (comme borderWidth: 2.5 du site)
        bw = round(2.5 * SS)
        for i in range(len(pts)):
            p1 = pts[i]
            p2 = pts[(i + 1) % len(pts)]
            d.line([p1, p2], fill=(rv, gv, bv, 220), width=bw)

        # Points : bordure blanche 1px + point couleur 4px (comme le site)
        pt_r = 4 * SS
        bd_r = pt_r + 1 * SS
        for p in pts:
            d.ellipse([p[0] - bd_r, p[1] - bd_r, p[0] + bd_r, p[1] + bd_r],
                      fill=(255, 255, 255, 255))
            d.ellipse([p[0] - pt_r, p[1] - pt_r, p[0] + pt_r, p[1] + pt_r],
                      fill=(rv, gv, bv, 255))

    # Dataset 1 dessous, dataset 2 dessus
    draw_dataset(values1, color1_hex)
    draw_dataset(values2, color2_hex)

    # Reduire avec LANCZOS pour antialiasing
    layer = layer.resize((iw, ih), Image.LANCZOS)
    img.alpha_composite(layer)


def generate_duel_image(ville_id, ville_nom, cand1, cand2, election_data):
    """Image OG duel : fond blanc, deux candidats face a face, radar HD identique au site,
    badge VS, footer. Couleurs fixes #00b2a9 vs #ff7a00. Tout en supersampling 4x."""
    SS = 4  # supersampling global pour eliminer toute pixelisation
    sw, sh = W * SS, H * SS
    img = Image.new("RGBA", (sw, sh))
    draw = ImageDraw.Draw(img, "RGBA")
    pad = 45 * SS

    # === FOND BLANC avec lisere tricolore ===
    draw.rectangle([0, 0, sw, sh], fill=(255, 255, 255, 255))
    tiers = sw // 3
    bh = 4 * SS
    draw.rectangle([0, 0, tiers, bh], fill=hex_to_rgb(BLEU_DRAPEAU))
    draw.rectangle([tiers, 0, 2 * tiers, bh], fill=(255, 255, 255, 255))
    draw.rectangle([2 * tiers, 0, sw, bh], fill=hex_to_rgb(ROUGE_DRAPEAU))

    # === HEADER ===
    # Brand
    f_brand = get_font("montserrat-black-italic", 22 * SS)
    bx = pad
    for text, color in [("#POURQUITU", hex_to_rgb(FOND_TEXTE)), ("VOTES?", hex_to_rgb(ROUGE_DRAPEAU))]:
        draw.text((bx, 18 * SS), text, fill=color, font=f_brand)
        bb = f_brand.getbbox(text)
        bx += bb[2] - bb[0]

    # Badges
    f_badge = get_font("dm-sans-medium", 13 * SS)
    f_badge_ville = get_font("montserrat-bold", 14 * SS)

    badge_mun = "Municipales 2026"
    bb_mun = f_badge.getbbox(badge_mun)
    bw_mun = bb_mun[2] - bb_mun[0]
    badge_ville = ville_nom.upper()
    bb_ville = f_badge_ville.getbbox(badge_ville)
    bw_ville = bb_ville[2] - bb_ville[0]

    bx_mun = sw - pad - bw_mun - 30 * SS
    draw.rounded_rectangle([bx_mun, 12 * SS, bx_mun + bw_mun + 30 * SS, 40 * SS],
                           radius=14 * SS, fill=hex_to_rgb(GRIS_FOND))
    draw.text((bx_mun + 15 * SS, 17 * SS), badge_mun, fill=hex_to_rgb(ACCENT), font=f_badge)

    bx_ville = bx_mun - bw_ville - 46 * SS
    draw.rounded_rectangle([bx_ville, 12 * SS, bx_ville + bw_ville + 30 * SS, 40 * SS],
                           radius=14 * SS, fill=hex_to_rgb(ACCENT))
    draw.text((bx_ville + 15 * SS, 17 * SS), badge_ville, fill=(255, 255, 255, 255), font=f_badge_ville)

    # Separateur
    draw.line([(pad, 52 * SS), (sw - pad, 52 * SS)], fill=hex_to_rgb(GRIS_BORDURE), width=SS)

    # === COULEURS FIXES DUEL ===
    color1 = "#00b2a9"
    color2 = "#ff7a00"
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)

    # === RADAR CHART HD (centre) — dessine sur le canvas SS ===
    radar_cx = sw // 2
    radar_cy = 310 * SS
    radar_r = 190 * SS

    radar_values1 = compute_candidate_radar_12(election_data, cand1["id"])
    radar_values2 = compute_candidate_radar_12(election_data, cand2["id"])
    n_cats = len(radar_values1)

    # Grille
    grid_col = (229, 229, 229, 255)
    axis_col = (229, 229, 229, 180)
    for scale in [0.25, 0.50, 0.75, 1.0]:
        r = int(radar_r * scale)
        w = round(1.2 * SS) if scale == 1.0 else round(0.8 * SS)
        draw.ellipse([radar_cx - r, radar_cy - r, radar_cx + r, radar_cy + r],
                     outline=grid_col, width=w)
    for i in range(n_cats):
        a = (2 * math.pi * i / n_cats) - math.pi / 2
        ex = radar_cx + math.cos(a) * radar_r
        ey = radar_cy + math.sin(a) * radar_r
        draw.line([(radar_cx, radar_cy), (ex, ey)], fill=axis_col, width=round(0.8 * SS))

    # Datasets — sur calque transparent pour alpha blending correct (0.15 comme le site)
    def draw_dataset_layer(values, color_hex):
        """Dessine un dataset radar sur un calque transparent separe,
        puis le composite sur img. Alpha fill = 0.15 (identique a hexToRgba(c, 0.15) du site)."""
        layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer, "RGBA")
        rv, gv, bv = hex_to_rgb(color_hex)
        pts = []
        for i, val in enumerate(values):
            a = (2 * math.pi * i / n_cats) - math.pi / 2
            v = max(0.0, min(1.0, val))
            pts.append((radar_cx + math.cos(a) * radar_r * v,
                        radar_cy + math.sin(a) * radar_r * v))
        # Fill alpha 0.15 = 38/255 (comme le site)
        ld.polygon(pts, fill=(rv, gv, bv, 38))
        # Bordure 2.5px
        bw = round(2.5 * SS)
        for i in range(len(pts)):
            ld.line([pts[i], pts[(i + 1) % len(pts)]],
                    fill=(rv, gv, bv, 220), width=bw)
        # Points : bordure blanche + point couleur
        pt_r = 4 * SS
        bd_r = pt_r + 1 * SS
        for p in pts:
            ld.ellipse([p[0] - bd_r, p[1] - bd_r, p[0] + bd_r, p[1] + bd_r],
                       fill=(255, 255, 255, 255))
            ld.ellipse([p[0] - pt_r, p[1] - pt_r, p[0] + pt_r, p[1] + pt_r],
                       fill=(rv, gv, bv, 255))
        return layer

    layer1 = draw_dataset_layer(radar_values1, color1)
    layer2 = draw_dataset_layer(radar_values2, color2)
    img = Image.alpha_composite(img, layer1)
    img = Image.alpha_composite(img, layer2)
    draw = ImageDraw.Draw(img, "RGBA")

    # Labels radar (DM Sans Bold 11px, #555)
    f_label = get_font("dm-sans-bold", 11 * SS)
    label_color = (85, 85, 85, 255)
    labels = get_categories_labels(election_data)
    label_padding = 22 * SS
    for i, lbl in enumerate(labels):
        a = (2 * math.pi * i / n_cats) - math.pi / 2
        lx = radar_cx + math.cos(a) * (radar_r + label_padding)
        ly = radar_cy + math.sin(a) * (radar_r + label_padding)
        bb = f_label.getbbox(lbl)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        cos_a, sin_a = math.cos(a), math.sin(a)
        if abs(cos_a) < 0.15:
            tx = lx - tw / 2
        elif cos_a > 0:
            tx = lx
        else:
            tx = lx - tw
        if abs(sin_a) < 0.15:
            ty = ly - th / 2
        elif sin_a > 0:
            ty = ly
        else:
            ty = ly - th
        draw.text((tx, ty), lbl, fill=label_color, font=f_label)

    # === CANDIDATS ===
    col_w = 230 * SS
    cand_y = 260 * SS
    text_dark = hex_to_rgb(FOND_TEXTE)
    text_sec = (85, 85, 85, 255)

    f_name = get_font("montserrat-extrabold", 22 * SS)
    f_parti = get_font("dm-sans", 13 * SS)
    f_leg = get_font("dm-sans-bold", 10 * SS)

    # --- Helper : dessiner un candidat ---
    def draw_candidat(cand, bar_x, align_right, color_rgb):
        rv, gv, bv = color_rgb
        # Barre verticale
        if align_right:
            bx0, bx1 = bar_x, bar_x + 4 * SS
        else:
            bx0, bx1 = bar_x, bar_x + 4 * SS
        draw.rounded_rectangle([bx0, cand_y, bx1, cand_y + 80 * SS],
                               radius=2 * SS, fill=(rv, gv, bv, 255))

        # Nom (split prenom/nom)
        name = cand["nom"].upper()
        parts = name.rsplit(" ", 1)
        if len(parts) == 2 and len(parts[0]) > 12:
            parts = name.split(" ", 1)
        for pi, part in enumerate(parts):
            bb = f_name.getbbox(part)
            pw = bb[2] - bb[0]
            if align_right:
                draw.text((bar_x - 14 * SS - pw, cand_y + pi * 28 * SS),
                          part, fill=text_dark, font=f_name)
            else:
                draw.text((bar_x + 18 * SS, cand_y + pi * 28 * SS),
                          part, fill=text_dark, font=f_name)

        # Parti (non tronque, multi-ligne si necessaire)
        liste = cand.get("liste", "")
        parti_y = cand_y + len(parts) * 28 * SS + 6 * SS
        max_w = col_w - 20 * SS
        # Couper en lignes si trop large
        parti_lines = []
        bb_full = f_parti.getbbox(liste)
        if (bb_full[2] - bb_full[0]) <= max_w:
            parti_lines = [liste]
        else:
            words = liste.split()
            current = ""
            for w in words:
                test = (current + " " + w).strip()
                bb_t = f_parti.getbbox(test)
                if (bb_t[2] - bb_t[0]) > max_w and current:
                    parti_lines.append(current)
                    current = w
                else:
                    current = test
            if current:
                parti_lines.append(current)

        for li, line in enumerate(parti_lines):
            bb_l = f_parti.getbbox(line)
            lw = bb_l[2] - bb_l[0]
            ly = parti_y + li * 18 * SS
            if align_right:
                draw.text((bar_x - 14 * SS - lw, ly), line,
                          fill=text_sec, font=f_parti)
            else:
                draw.text((bar_x + 18 * SS, ly), line,
                          fill=text_sec, font=f_parti)

        # Pastille legende
        leg_y = parti_y + len(parti_lines) * 18 * SS + 12 * SS
        leg_text = "Couverture"
        bb_lg = f_leg.getbbox(leg_text)
        lgw = bb_lg[2] - bb_lg[0]
        dot_r = 5 * SS
        if align_right:
            dx = bar_x - 14 * SS - lgw - 4 * SS - dot_r * 2
            draw.ellipse([dx, leg_y, dx + dot_r * 2, leg_y + dot_r * 2],
                         fill=(rv, gv, bv, 255))
            draw.text((dx + dot_r * 2 + 4 * SS, leg_y - 1 * SS), leg_text,
                      fill=(160, 160, 160, 255), font=f_leg)
        else:
            dx = bar_x + 18 * SS
            draw.ellipse([dx, leg_y, dx + dot_r * 2, leg_y + dot_r * 2],
                         fill=(rv, gv, bv, 255))
            draw.text((dx + dot_r * 2 + 4 * SS, leg_y - 1 * SS), leg_text,
                      fill=(160, 160, 160, 255), font=f_leg)

    # Candidat 1 (gauche, aligne a droite)
    bar_x1 = pad + col_w - 4 * SS
    draw_candidat(cand1, bar_x1, align_right=True, color_rgb=(r1, g1, b1))

    # Candidat 2 (droite, aligne a gauche)
    bar_x2 = sw - pad - col_w
    draw_candidat(cand2, bar_x2, align_right=False, color_rgb=(r2, g2, b2))

    # === BADGE VS ===
    vs_r = 24 * SS
    # Ombre
    draw.ellipse([radar_cx - vs_r - 8, radar_cy - vs_r - 8,
                  radar_cx + vs_r + 8, radar_cy + vs_r + 8],
                 fill=(0, 0, 0, 25))
    # Cercle blanc
    draw.ellipse([radar_cx - vs_r, radar_cy - vs_r,
                  radar_cx + vs_r, radar_cy + vs_r],
                 fill=(255, 255, 255, 255))
    # Bordure grise
    draw.ellipse([radar_cx - vs_r, radar_cy - vs_r,
                  radar_cx + vs_r, radar_cy + vs_r],
                 outline=(208, 213, 221, 180), width=round(1.2 * SS))
    f_vs = get_font("montserrat-black", 17 * SS)
    bb_vs = f_vs.getbbox("VS")
    vs_tw = bb_vs[2] - bb_vs[0]
    vs_th = bb_vs[3] - bb_vs[1]
    draw.text((radar_cx - vs_tw // 2, radar_cy - vs_th // 2 - 2 * SS), "VS",
              fill=text_dark, font=f_vs)

    # === FOOTER ===
    footer_y = (H - 38) * SS
    draw.text((pad, footer_y), "pourquituvotes.fr",
              fill=hex_to_rgb(ACCENT), font=get_font("dm-sans-medium", 13 * SS))

    mention = "Donn\u00e9es issues des programmes officiels des candidats"
    f_mention = get_font("dm-sans", 11 * SS)
    bb_m = f_mention.getbbox(mention)
    mw = bb_m[2] - bb_m[0]
    draw.text((sw - pad - mw, footer_y + 1 * SS), mention,
              fill=(160, 160, 160, 255), font=f_mention)

    # === Downscale LANCZOS ===
    img = img.resize((W, H), Image.LANCZOS)

    filename = "duel-%s-%s-vs-%s.jpg" % (ville_id, cand1["id"], cand2["id"])
    img.convert("RGB").save(os.path.join(OUT_DIR, filename), "JPEG", quality=90)
    return filename


# === Main ===
def main():
    import sys
    os.makedirs(OUT_DIR, exist_ok=True)

    # Mode test : python generer_og_images.py --test paris
    test_mode = "--test" in sys.argv
    test_ville = sys.argv[sys.argv.index("--test") + 1] if test_mode and len(sys.argv) > sys.argv.index("--test") + 1 else "paris"

    # Mode duel : python generer_og_images.py --duel paris bournazel chikirou
    duel_mode = "--duel" in sys.argv
    if duel_mode:
        di = sys.argv.index("--duel")
        duel_ville = sys.argv[di + 1] if len(sys.argv) > di + 1 else "paris"
        duel_c1 = sys.argv[di + 2] if len(sys.argv) > di + 2 else ""
        duel_c2 = sys.argv[di + 3] if len(sys.argv) > di + 3 else ""

        elections_dir = os.path.join(DATA_DIR, "elections")
        villes_path_d = os.path.join(DATA_DIR, "villes.json")
        with open(villes_path_d, "r", encoding="utf-8") as f:
            villes_d = json.load(f)
        ville_obj = next((v for v in villes_d if v["id"] == duel_ville), None)
        if not ville_obj:
            print("Ville '%s' non trouvee" % duel_ville)
            return
        el_path = os.path.join(elections_dir, "%s.json" % ville_obj["elections"][0])
        with open(el_path, "r", encoding="utf-8") as f:
            el_data = json.load(f)
        c1 = next((c for c in el_data["candidats"] if c["id"] == duel_c1), None)
        c2 = next((c for c in el_data["candidats"] if c["id"] == duel_c2), None)
        if not c1 or not c2:
            ids = [c["id"] for c in el_data["candidats"]]
            print("Candidat(s) non trouve(s). Disponibles: %s" % ", ".join(ids))
            return
        fname = generate_duel_image(duel_ville, ville_obj["nom"], c1, c2, el_data)
        print("[+] %s" % fname)
        print("Dossier: %s" % os.path.abspath(OUT_DIR))
        return

    hashes = load_hashes()
    new_hashes = dict(hashes)  # preserve existing
    generated, skipped = 0, 0

    villes_path = os.path.join(DATA_DIR, "villes.json")
    with open(villes_path, "r", encoding="utf-8") as f:
        villes = json.load(f)
    villes_hash = file_hash(villes_path)

    total_candidats = sum(v.get("stats", {}).get("candidats", 0) for v in villes)
    total_propositions = sum(v.get("stats", {}).get("propositions", 0) for v in villes)

    if not test_mode:
        # 1. Images generiques
        print("=== Images generiques ===")
        generics = [
            ("home.jpg", generate_home_image, (len(villes), total_candidats, total_propositions)),
            ("comparateur.jpg", generate_comparateur_image, ()),
            ("presidentielle-2027.jpg", generate_presidentielle_image, ()),
        ]
        for name, func, args in generics:
            if needs_regen(name, villes_hash, hashes):
                func(*args)
                new_hashes[name] = villes_hash
                generated += 1
                print("  [+] %s" % name)
            else:
                skipped += 1

    # 2. Images par ville + par candidat
    elections_dir = os.path.join(DATA_DIR, "elections")
    villes_to_process = villes
    if test_mode:
        villes_to_process = [v for v in villes if v["id"] == test_ville]
        print("=== Mode test : %s ===" % test_ville)

    for ville in villes_to_process:
        ville_id = ville["id"]
        ville_nom = ville["nom"]
        election_files = ville.get("elections", [])
        if not election_files:
            continue

        election_path = os.path.join(elections_dir, "%s.json" % election_files[0])
        if not os.path.exists(election_path):
            continue

        with open(election_path, "r", encoding="utf-8") as f:
            election_data = json.load(f)

        # Stats calculees depuis les donnees reelles (pas villes.json)
        stats = compute_real_stats(election_data)
        el_hash = file_hash(election_path)

        # Image ville
        city_key = "%s.jpg" % ville_id
        if test_mode or needs_regen(city_key, el_hash, hashes):
            generate_city_image(ville_id, ville_nom, election_data, stats)
            new_hashes[city_key] = el_hash
            generated += 1
            print("  [+] %s" % city_key)
        else:
            skipped += 1

        # Images candidats
        for candidat in election_data.get("candidats", []):
            cand_key = "%s-%s.jpg" % (ville_id, candidat["id"])
            if test_mode or needs_regen(cand_key, el_hash, hashes):
                generate_candidate_image(ville_id, ville_nom, candidat, election_data)
                new_hashes[cand_key] = el_hash
                generated += 1
                print("  [+] %s" % cand_key)
            else:
                skipped += 1

        # Images duels (uniquement candidats avec programmeComplet)
        complets = [c for c in election_data.get("candidats", []) if c.get("programmeComplet")]
        if len(complets) >= 2:
            from itertools import combinations
            for c1, c2 in combinations(complets, 2):
                duel_key = "duel-%s-%s-vs-%s.jpg" % (ville_id, c1["id"], c2["id"])
                if test_mode or needs_regen(duel_key, el_hash, hashes):
                    generate_duel_image(ville_id, ville_nom, c1, c2, election_data)
                    new_hashes[duel_key] = el_hash
                    generated += 1
                    print("  [+] %s" % duel_key)
                else:
                    skipped += 1

    save_hashes(new_hashes)
    print("\n=== Termine ===")
    print("%d images generees, %d inchangees" % (generated, skipped))
    print("Dossier: %s" % os.path.abspath(OUT_DIR))


if __name__ == "__main__":
    main()
