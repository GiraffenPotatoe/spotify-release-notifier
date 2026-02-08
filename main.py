
import requests
import json
import os
from datetime import datetime

PING_ROLE_ID = "14677256571768054581467725657176805458"


DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# 🔧 HIER DEINE ARTISTS (Spotify Artist IDs)
ARTISTS = {
    "5APQG46BzoVM8gm7mBRRo7": "Duplexcopy",
    "3Bu2yHzFWRIrtyAy8RnVRK": "CryXal",
    
}

STATE_FILE = "posted.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def get_latest_release(artist_id):
    url = f"https://open.spotify.com/artist/{artist_id}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if r.status_code != 200:
        return None

    text = r.text
    marker = '"latestRelease":'
    if marker not in text:
        return None

    snippet = text.split(marker, 1)[1][:1000]

    try:
        data = json.loads("{" + snippet.split("}", 1)[0] + "}")
        return data
    except:
        return None


def post_discord(artist, release):
    message = {
        "content": (
    f"<@&{1467725657176805458}> 🚨 **NEUER SPOTIFY RELEASE** 🚨\n\n"
    f"🎵 **{artist} – {release.get('name','Neuer Track')}**\n"
    f"▶ {release.get('shareUrl','https://open.spotify.com')}"
)

    }
    requests.post(DISCORD_WEBHOOK_URL, json=message)


def main():
    state = load_state()

    for artist_id, artist_name in ARTISTS.items():
        release = get_latest_release(artist_id)
        if not release:
            continue

        release_id = release.get("uri")
        if not release_id:
            continue

        if state.get(artist_id) == release_id:
            continue  # schon gepostet

        post_discord(artist_name, release)
        state[artist_id] = release_id

    save_state(state)


if __name__ == "__main__":
    main()

requests.post(
    DISCORD_WEBHOOK_URL,
    json={"content": f"<@&{PING_ROLE_ID}> 🔔 **PING-ROLLEN-TEST**"}
)

