import json
import os
import secrets
from datetime import datetime
import spotipy
import spotipy.util as util
from icecream import ic
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

os.environ['SPOTIPY_CLIENT_ID'] = secrets.SPOTIPY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = secrets.SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = secrets.SPOTIPY_REDIRECT_URI

scope = "playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

playlist_id = '2aTnVVKW6RzSBCAOXnSGSP'
results = []
offset = 0
limit = 100
while True:
    tracks = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
    results += tracks['items']
    offset += len(tracks['items'])
    if len(tracks['items']) == 0:
        break

today = datetime.today().strftime('%Y-%m-%d')
with open(f'playlist_tracks_for_william_{today}.json', 'w') as outfile:
    json.dump(results, outfile)

ic(f"Saved {len(results)} tracks to playlist_tracks_{playlist_id}_{today}.json")