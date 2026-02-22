#!/usr/bin/env python3
"""
Publie les posts du planning social sur Twitter/X.

Modes :
  --test         Publie UN seul tweet de test (sans toucher au planning)
  --now          Publie tous les posts dont la date/heure est passee
  --schedule     Tourne en continu et publie aux horaires prevus
  --dry-run      Affiche ce qui serait publie sans rien poster

Usage:
  python scripts/publier_twitter.py --test
  python scripts/publier_twitter.py --now
  python scripts/publier_twitter.py --schedule
  python scripts/publier_twitter.py --now --dry-run
"""

import csv
import json
import os
import sys
import time
import argparse
from datetime import datetime

# --- Config Twitter (env vars prioritaires, fallback local) ---
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY", "BU7TToCuKQXP8YPA2ENtLacFc")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET", "YCH17d7VDo3MHFHq93IVSRyixTocKmpL2gq76dSkwTSTeEOoI3")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "2023515636408651776-akAiop7FnUyuOpuXe51YjSWFaSIooS")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET", "uV7yIh9rKXr5qKghftuSuryLNYLwThKtpp6lU3RTvkIt9")

# --- Handles Twitter des candidats ---
HANDLES = {
    "gregoire": "@egregoire", "dati": "@datirachida", "chikirou": "@chikirouparis",
    "bournazel": "@pybournazel", "knafo": "@knafo_sarah", "mariani": "@ThierryMARIANI",
    "delogu": "@sebastiendelogu", "payan": "@BenoitPayan", "vassal": "@MartineVassal",
    "allisio": "@franckallisio", "davoux": "@erwandavoux",
    "doucet": "@Gregorydoucet", "aulas": "@JM_Aulas",
    "moudenc": "@jlmoudenc", "piquemal": "@FraPiquemal",
    "estrosi": "@cestrosi", "ciotti": "@eciotti",
    "barseghian": "@JeanneBarsegh", "trautmann": "@CatTrautmann",
    "hurmic": "@PierreHurmic",
    "rolland": "@Johanna_Rolland", "chombart": "@Foulques44",
    "oziol": "@NathalieOziol",
    "philippe": "@EPhilippe_LH",
    "carignon": "@CarignonAlain",
    "bechu": "@ChristopheBechu",
    "frigout": "@asfrigout",
}

# --- Chemins ---
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CSV_PATH = os.path.join(ROOT, "data", "planning_social.csv")
LOG_PATH = os.path.join(ROOT, "data", "twitter_published.json")
IMG_DIR = os.path.join(ROOT, "img", "og")


def get_client():
    """Cree le client Twitter API v2 avec tweepy."""
    import tweepy
    client = tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_SECRET,
    )
    return client


def get_api_v1():
    """Cree l'API v1.1 pour l'upload d'images."""
    import tweepy
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    return tweepy.API(auth)


def load_published():
    """Charge le log des posts deja publies."""
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_published(published):
    """Sauvegarde le log des posts publies."""
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(published, f, indent=2, ensure_ascii=False)


def load_planning():
    """Lit le CSV du planning."""
    posts = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            posts.append(row)
    return posts


def find_image(image_og):
    """Cherche l'image OG correspondante."""
    if not image_og:
        return None
    # Chercher dans img/og/
    path = os.path.join(IMG_DIR, image_og)
    if os.path.exists(path):
        return path
    # Chercher dans img/
    path2 = os.path.join(ROOT, "img", image_og)
    if os.path.exists(path2):
        return path2
    return None


def post_key(row):
    """Cle unique pour un post (date + heure)."""
    return f"{row['date']}_{row.get('heure', '09:00')}"


def extract_ville_from_url(url):
    """Extrait le slug de ville depuis l'URL."""
    if "/municipales-2026/" in url:
        parts = url.split("/municipales-2026/")[1].split("/")
        ville = parts[0].split("?")[0]
        if ville:
            return ville
    return None


def get_ville_candidat_ids(ville_slug):
    """Charge les IDs de tous les candidats d'une ville depuis le JSON."""
    json_path = os.path.join(ROOT, "data", "elections", f"{ville_slug}-2026.json")
    if not os.path.exists(json_path):
        return []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [c["id"] for c in data.get("candidats", [])]


def extract_candidat_ids(row):
    """Extrait les IDs candidats depuis l'URL du post."""
    url = row.get("url", "")
    post_type = row.get("type", "")
    ids = []
    # URL candidat : /municipales-2026/ville/candidats/id/
    if "/candidats/" in url:
        parts = url.rstrip("/").split("/")
        idx = parts.index("candidats")
        if idx + 1 < len(parts):
            ids.append(parts[idx + 1])
    # URL duel : ?candidats=a,b
    elif "candidats=" in url:
        param = url.split("candidats=")[1].split("&")[0].split("#")[0]
        ids.extend(param.split(","))
    # Post ville : tagger tous les candidats de la ville
    elif post_type == "ville":
        ville_slug = extract_ville_from_url(url)
        if ville_slug:
            ids = get_ville_candidat_ids(ville_slug)
    return ids


def inject_handles(text, row):
    """Ajoute les @handles des candidats mentionnes dans le tweet."""
    candidat_ids = extract_candidat_ids(row)
    handles = [HANDLES[cid] for cid in candidat_ids if cid in HANDLES]
    if not handles:
        return text
    handles_str = " ".join(handles)
    # Inserer les handles apres la premiere ligne
    lines = text.split("\n")
    if len(lines) >= 2:
        lines.insert(1, handles_str)
    else:
        lines.append(handles_str)
    return "\n".join(lines)


def publish_tweet(client, api_v1, text, image_path=None, dry_run=False):
    """Publie un tweet, avec image optionnelle."""
    # Tronquer a 280 caracteres
    if len(text) > 280:
        text = text[:277] + "..."

    if dry_run:
        print(f"  [DRY-RUN] Tweet ({len(text)} car.) :")
        print(f"  {text[:100]}...")
        if image_path:
            print(f"  Image : {image_path}")
        return True, "dry-run"

    try:
        media_id = None
        if image_path:
            media = api_v1.media_upload(image_path)
            media_id = media.media_id
            print(f"  Image uploadee : {os.path.basename(image_path)}")

        if media_id:
            response = client.create_tweet(text=text, media_ids=[media_id])
        else:
            response = client.create_tweet(text=text)

        tweet_id = response.data["id"]
        print(f"  Publie ! Tweet ID : {tweet_id}")
        return True, tweet_id

    except Exception as e:
        print(f"  ERREUR : {e}")
        return False, str(e)


def cmd_test(args):
    """Publie un tweet de test."""
    client = get_client()
    api_v1 = get_api_v1()

    text = "Test automatique depuis pourquituvotes.fr\n\nMunicipales 2026 : comparez les programmes.\n\n#Municipales2026 #PourQuiTuVotes"

    print("Publication tweet de test...")
    success, result = publish_tweet(client, api_v1, text, dry_run=args.dry_run)
    if success:
        print("OK !")
    else:
        print(f"Echec : {result}")


def cmd_now(args):
    """Publie tous les posts dont la date/heure est passee."""
    client = get_client()
    api_v1 = get_api_v1()
    posts = load_planning()
    published = load_published()
    now = datetime.now()

    print(f"Date/heure actuelle : {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"Posts dans le planning : {len(posts)}")
    print(f"Deja publies : {len(published)}")
    print()

    to_publish = []
    for row in posts:
        key = post_key(row)
        if key in published:
            continue
        try:
            post_dt = datetime.strptime(f"{row['date']} {row.get('heure', '09:00')}", "%Y-%m-%d %H:%M")
        except ValueError:
            continue
        if args.today:
            # Mode --today : publier tout ce qui est prevu aujourd'hui
            if row["date"] == now.strftime("%Y-%m-%d"):
                to_publish.append(row)
        elif post_dt <= now:
            to_publish.append(row)

    if not to_publish:
        print("Rien a publier pour l'instant.")
        return

    print(f"{len(to_publish)} post(s) a publier :\n")

    for i, row in enumerate(to_publish):
        key = post_key(row)
        text = row.get("texte_twitter", "").strip()
        url = row.get("url", "").strip()
        image_og = row.get("image_og", "").strip()

        # Injecter les @handles des candidats
        text = inject_handles(text, row)

        # Ajouter l'URL au tweet
        if url:
            text_with_url = f"{text}\n\n{url}"
        else:
            text_with_url = text

        image_path = find_image(image_og)

        print(f"[{i+1}/{len(to_publish)}] {row['date']} {row.get('heure', '')} - {row.get('type', '')}")

        success, result = publish_tweet(client, api_v1, text_with_url, image_path, dry_run=args.dry_run)

        if success and not args.dry_run:
            published[key] = {
                "tweet_id": result,
                "published_at": datetime.now().isoformat(),
                "type": row.get("type", ""),
                "date_planned": row["date"],
            }
            save_published(published)

        # Pause entre tweets pour eviter le rate limit
        if i < len(to_publish) - 1 and not args.dry_run:
            print("  Pause 30s...")
            time.sleep(30)

    print(f"\nTermine. {len(to_publish)} post(s) traites.")


def cmd_schedule(args):
    """Tourne en continu et publie aux horaires prevus."""
    print("Mode schedule : verification toutes les 5 minutes")
    print("Ctrl+C pour arreter\n")

    while True:
        posts = load_planning()
        published = load_published()
        now = datetime.now()

        for row in posts:
            key = post_key(row)
            if key in published:
                continue
            try:
                post_dt = datetime.strptime(f"{row['date']} {row.get('heure', '09:00')}", "%Y-%m-%d %H:%M")
            except ValueError:
                continue

            # Publier si l'heure est passee (avec 2 min de tolerance)
            diff = (now - post_dt).total_seconds()
            if 0 <= diff <= 600:  # dans les 10 dernieres minutes
                client = get_client()
                api_v1 = get_api_v1()

                text = row.get("texte_twitter", "").strip()
                url = row.get("url", "").strip()
                image_og = row.get("image_og", "").strip()

                text = inject_handles(text, row)

                if url:
                    text = f"{text}\n\n{url}"

                image_path = find_image(image_og)

                print(f"[{now.strftime('%H:%M')}] Publication : {row['date']} {row.get('heure', '')} - {row.get('type', '')}")
                success, result = publish_tweet(client, api_v1, text, image_path, dry_run=args.dry_run)

                if success and not args.dry_run:
                    published[key] = {
                        "tweet_id": result,
                        "published_at": now.isoformat(),
                        "type": row.get("type", ""),
                        "date_planned": row["date"],
                    }
                    save_published(published)

        # Attendre 5 minutes
        time.sleep(300)


def main():
    parser = argparse.ArgumentParser(description="Publier sur Twitter/X")
    parser.add_argument("--test", action="store_true", help="Publie un tweet de test")
    parser.add_argument("--now", action="store_true", help="Publie tous les posts en retard")
    parser.add_argument("--schedule", action="store_true", help="Mode continu")
    parser.add_argument("--today", action="store_true", help="Publie tous les posts du jour")
    parser.add_argument("--dry-run", action="store_true", help="Simule sans publier")

    args = parser.parse_args()

    if not any([args.test, args.now, args.schedule]):
        parser.print_help()
        return

    if args.test:
        cmd_test(args)
    elif args.now:
        cmd_now(args)
    elif args.schedule:
        cmd_schedule(args)


if __name__ == "__main__":
    main()
