import json
import os
import secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

os.environ['SPOTIPY_CLIENT_ID'] = secrets.SPOTIPY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = secrets.SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = secrets.SPOTIPY_REDIRECT_URI

# Rest of the script goes here
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

scope = "user-library-read user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
print(sp.me())

with open('saved_tracks_test_2023-10-17.json', 'r') as infile:
    saved_tracks = json.load(infile)

tracks_with_features = []
batch_size = 50
for i in range(0, len(saved_tracks), batch_size):
    batch = saved_tracks[i:i+batch_size]
    track_uris = [item["track"]["uri"] for item in batch]
    track_infos = sp.tracks(track_uris)["tracks"]
    audio_features = sp.audio_features(track_uris)
    for j in range(len(batch)):
        track = batch[j]["track"]
        track_uri = track["uri"]
        track_info = track_infos[j]
        audio_feature = audio_features[j]
        track_with_features = {
            "name": track_info["name"],
            "artist": track_info["artists"][0]["name"],
            "album": track_info["album"]["name"],
            "uri": track_uri,
            "added_at": batch[j]["added_at"],
            "danceability": audio_feature["danceability"],
            "energy": audio_feature["energy"],
            "key": audio_feature["key"],
            "loudness": audio_feature["loudness"],
            "mode": audio_feature["mode"],
            "speechiness": audio_feature["speechiness"],
            "acousticness": audio_feature["acousticness"],
            "instrumentalness": audio_feature["instrumentalness"],
            "liveness": audio_feature["liveness"],
            "valence": audio_feature["valence"],
            "tempo": audio_feature["tempo"],
            "duration_ms": audio_feature["duration_ms"],
            "time_signature": audio_feature["time_signature"]
        }
        tracks_with_features.append(track_with_features)

with open(f'saved_tracks_with_features_{today}.json', 'w') as outfile:
    json.dump(tracks_with_features, outfile, indent=4)

print(f"Saved {len(tracks_with_features)} tracks with features to saved_tracks_with_features_{today}.json")