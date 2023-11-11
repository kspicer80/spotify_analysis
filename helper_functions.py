import json
import spotify_secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os

os.environ['SPOTIPY_CLIENT_ID'] = spotify_secrets.SPOTIPY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = spotify_secrets.SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = spotify_secrets.SPOTIPY_REDIRECT_URI

scope = "user-library-read user-top-read"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def get_all_my_saved_tracks() -> None:
    results = []
    offset = 0
    limit = 50
    while True:
        tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)
        results += tracks['items']
        offset += len(tracks['items'])
        if len(tracks['items']) == 0:
            break

    with open(f'main_data_files/saved_tracks.json', 'w') as outfile:
        json.dump(results, outfile)

    print(f"Saved {len(results)} tracks to saved_tracks.json")

def update_database_of_songs_with_features() -> None:
    # Load existing .json file with all saved tracks
    with open('main_data_files/saved_tracks.json', 'r') as infile:
        saved_tracks = json.load(infile)

    # Load the existing .json file into a dictionary
    with open('main_data_files/saved_tracks_with_features.json', 'r') as infile:
        tracks_with_features = json.load(infile)

    tracks_with_features_dict = {track['uri']: track for track in tracks_with_features}

    new_tracks_count = 0  # initialize the counter

    batch_size = 50
    for i in range(0, len(saved_tracks), batch_size):
        batch = saved_tracks[i:i+batch_size]
        track_uris = [item["track"]["uri"] for item in batch]
        track_infos = sp.tracks(track_uris)["tracks"]
        audio_features = sp.audio_features(track_uris)
        for j in range(len(batch)):
            track = batch[j]["track"]
            track_uri = track["uri"]
            # If the song already exists in the dictionary, skip it
            if track_uri in tracks_with_features_dict:
                continue
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
            tracks_with_features_dict[track_uri] = track_with_features
            new_tracks_count += 1  # increment the counter

    # Write the dictionary back to the .json file
    with open('main_data_files/saved_tracks_with_features.json', 'w') as outfile:
        json.dump(list(tracks_with_features_dict.values()), outfile, indent=4)

    print(f"Updated saved_tracks_with_features.json with {new_tracks_count} new tracks")