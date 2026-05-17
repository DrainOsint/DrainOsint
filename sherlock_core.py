"""
Drain OSINT Bot - Modulo ricerca username
By Drain | @fattissimo

Controlla username su piattaforme internazionali pubbliche.
Rimossi tutti i siti russi e siti di nicchia irrilevanti.
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Timeout per ogni richiesta HTTP
TIMEOUT = 10

# Lista piattaforme: { "Nome Sito": "https://esempio.com/{}" }
# {} viene sostituito con l'username cercato
SITI = {
    # Social principali
    "Instagram":        "https://www.instagram.com/{}/",
    "TikTok":           "https://www.tiktok.com/@{}",
    "Twitter / X":      "https://twitter.com/{}",
    "Facebook":         "https://www.facebook.com/{}",
    "Snapchat":         "https://www.snapchat.com/add/{}",
    "Pinterest":        "https://www.pinterest.com/{}/",
    "Tumblr":           "https://{}.tumblr.com/",
    "Reddit":           "https://www.reddit.com/user/{}",
    "LinkedIn":         "https://www.linkedin.com/in/{}/",
    # Video & Streaming
    "YouTube":          "https://www.youtube.com/@{}",
    "Twitch":           "https://www.twitch.tv/{}",
    "Vimeo":            "https://vimeo.com/{}",
    "Dailymotion":      "https://www.dailymotion.com/{}",
    "Trovo":            "https://trovo.live/s/{}",
    # Musica
    "SoundCloud":       "https://soundcloud.com/{}",
    "Spotify":          "https://open.spotify.com/user/{}",
    "Bandcamp":         "https://{}.bandcamp.com/",
    "Last.fm":          "https://www.last.fm/user/{}",
    "Mixcloud":         "https://www.mixcloud.com/{}/",
    # Dev & Tech
    "GitHub":           "https://github.com/{}",
    "GitLab":           "https://gitlab.com/{}",
    "Bitbucket":        "https://bitbucket.org/{}",
    "HackerNews":       "https://news.ycombinator.com/user?id={}",
    "Stack Overflow":   "https://stackoverflow.com/users/{}",
    "Replit":           "https://replit.com/@{}",
    "Codepen":          "https://codepen.io/{}",
    "Dev.to":           "https://dev.to/{}",
    "npm":              "https://www.npmjs.com/~{}",
    "PyPI":             "https://pypi.org/user/{}/",
    "Docker Hub":       "https://hub.docker.com/u/{}",
    # Gaming
    "Steam":            "https://steamcommunity.com/id/{}",
    "Xbox":             "https://xboxgamertag.com/search/{}",
    "PSN":              "https://psnprofiles.com/{}",
    "Minecraft":        "https://namemc.com/profile/{}",
    "Chess.com":        "https://www.chess.com/member/{}",
    "Lichess":          "https://lichess.org/@/{}",
    "Roblox":           "https://www.roblox.com/user.aspx?username={}",
    "Kongregate":       "https://www.kongregate.com/accounts/{}",
    # Design & Arte
    "Behance":          "https://www.behance.net/{}",
    "Dribbble":         "https://dribbble.com/{}",
    "DeviantArt":       "https://www.deviantart.com/{}",
    "ArtStation":       "https://www.artstation.com/{}",
    "Flickr":           "https://www.flickr.com/people/{}",
    "500px":            "https://500px.com/p/{}",
    "Unsplash":         "https://unsplash.com/@{}",
    # Scrittura & Blog
    "Medium":           "https://medium.com/@{}",
    "Substack":         "https://{}.substack.com/",
    "WordPress":        "https://{}.wordpress.com/",
    "Wattpad":          "https://www.wattpad.com/user/{}",
    # Crypto & Finance
    "Keybase":          "https://keybase.io/{}",
    "Patreon":          "https://www.patreon.com/{}",
    "Ko-fi":            "https://ko-fi.com/{}",
    "Buy Me a Coffee":  "https://www.buymeacoffee.com/{}",
    "OpenCollective":   "https://opencollective.com/{}",
    # Forum & Community
    "Disqus":           "https://disqus.com/by/{}/",
    "ProductHunt":      "https://www.producthunt.com/@{}",
    "Quora":            "https://www.quora.com/profile/{}",
    "Goodreads":        "https://www.goodreads.com/{}",
    "Letterboxd":       "https://letterboxd.com/{}",
    "Trakt":            "https://trakt.tv/users/{}",
    # Altro
    "Telegram":         "https://t.me/{}",
    "Linktree":         "https://linktr.ee/{}",
    "About.me":         "https://about.me/{}",
    "Gravatar":         "https://gravatar.com/{}",
    "Fiverr":           "https://www.fiverr.com/{}",
    "Freelancer":       "https://www.freelancer.com/u/{}",
    "Hackerearth":      "https://www.hackerearth.com/@{}",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def _controlla(sito: str, url_template: str, username: str):
    """Controlla se l'username esiste su un singolo sito."""
    url = url_template.format(username)
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        if r.status_code == 200:
            return ("trovato", sito, url)
        return ("non_trovato", sito, url)
    except Exception:
        return ("errore", sito, url)

def cerca_username(username: str):
    """
    Cerca l'username su tutte le piattaforme in parallelo.
    Restituisce (trovati, contatore_errori).
    trovati = lista di tuple (sito, url)
    """
    trovati = []
    errori = 0

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(_controlla, sito, url, username): sito
            for sito, url in SITI.items()
        }
        for future in as_completed(futures):
            risultato = future.result()
            if risultato[0] == "trovato":
                trovati.append((risultato[1], risultato[2]))
            elif risultato[0] == "errore":
                errori += 1

    # Ordina alfabeticamente per nome sito
    trovati.sort(key=lambda x: x[0].lower())
    return trovati, errori
