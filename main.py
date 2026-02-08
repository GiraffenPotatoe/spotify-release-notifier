import os
import requests
import time

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

ARTISTS = [
    "SPOTIFY_ARTIST_ID_1",
    "SPOTIFY_ARTIST_ID_2"
]

def get_token():
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    )
    return r.json()["access_token"]

def check_releases():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    for artist in ARTISTS:
        url = f"https://api.spotify.com/v1/artists/{artist}/albums?include_groups=single,album&limit=1"
        r = requests.get(url, headers=headers).json()

        if r.get("items"):
            release = r["items"][0]
            message = {
                "content": f"@Releases 🚨 **NEUER SPOTIFY RELEASE** 🚨\n\n🎵 **{release['name']}**\n▶ {release['external_urls']['spotify']}"
            }
            requests.post(DISCORD_WEBHOOK_URL, json=message)

check_releases()
