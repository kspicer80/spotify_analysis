import json
import spotify_secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
from helper_functions import get_all_my_saved_tracks, update_database_of_songs_with_features

get_all_my_saved_tracks()
update_database_of_songs_with_features()

print("Main Script Complete!")