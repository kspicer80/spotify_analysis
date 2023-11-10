import json
import spotify_secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
from datetime import datetime
from icecream import ic

os.environ['SPOTIPY_CLIENT_ID'] = spotify_secrets.SPOTIPY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = spotify_secrets.SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = spotify_secrets.SPOTIPY_REDIRECT_URI

scope = "user-library-read user-top-read"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
print(sp.me())

results = []
offset = 0
limit = 50
while True:
    tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)
    results += tracks['items']
    offset += len(tracks['items'])
    if len(tracks['items']) == 0:
        break

today = datetime.today().strftime('%Y-%m-%d')
with open(f'main_data_files/saved_tracks.json', 'w') as outfile:
    json.dump(results, outfile)

print(f"Saved {len(results)} tracks to saved_tracks.json")