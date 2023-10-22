import json
import pandas as pd
import plotly.express as px

with open('saved_tracks_with_features_2023-10-17.json', 'r') as infile:
    dr_s_tracks = json.load(infile)

df_1 = pd.json_normalize(dr_s_tracks)
df_1['year_added'] = pd.to_datetime(df_1['added_at']).dt.year
df_1 = df_1[["name", "artist", "year_added", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature", "uri", "added_at"]]


with open('williams_saved_tracks_with_features.json', 'r') as infile:
    saved_tracks_with_features = json.load(infile)

df_2 = pd.json_normalize(saved_tracks_with_features)
df_2['year_added'] = pd.to_datetime(df_2['added_at']).dt.year
df_2 = df_2[["name", "artist", "year_added", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature", "uri", "added_at"]]

df_1['source'] = 'dr_s'
df_2['source'] = 'william'

df = pd.concat([df_1, df_2])

color_map = {'dr_s': 'green', 'william': 'red'}
fig = px.scatter(df, x="danceability", y="energy", color="source", color_discrete_map=color_map, hover_data=['name', 'artist', 'valence'])

fig.update_layout(title='Comparision of Danceability and Energy between William and Me')
fig.write_html('images/plots/comparisons_between_william_and_me.html')
fig.show()

# calculate the Jaccard similarity coefficient between the two sets of points
set_1 = set(df_1[['danceability', 'energy']].itertuples(index=False, name=None))
set_2 = set(df_2[['danceability', 'energy']].itertuples(index=False, name=None))
jaccard_similarity = len(set_1.intersection(set_2)) / len(set_1.union(set_2))
print(f"Jaccard similarity coefficient: {jaccard_similarity:.2f}")
