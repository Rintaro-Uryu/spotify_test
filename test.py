import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import requests
from requests.exceptions import HTTPError
import pandas as pd

client_id = '43ea166d32604a26b7ca3afba4572393'
client_secret = '55855b99cf584feca3cf709db376bae2'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_url = 'https://open.spotify.com/playlist/6KfKvkN7YEUFTwJHkczxdb?si=5d285aa4dade4002'
playlist_id = playlist_url.split('/')[-1].split('?')[0]  

results = sp.playlist(playlist_id)

tracks = []
artists = []
ids = []

for item in results['tracks']['items']:
    track = item['track']
    tracks.append(track['name'])
    ids.append(track['id'])
    artists.append(', '.join([artist['name'] for artist in track['artists']]))

id_2000s = pd.DataFrame({
    'Track': tracks,
    'Artist': artists,
    'ID': ids
})
id_2000s
# 空のリストを作成
track_list = []

# プレイリストにある100曲分のデータを取得
for i in range(100):
    while True:
        try:
            track_id = id_2000s['ID'][i]
            track = sp.audio_features(track_id)
            break
        except spotipy.SpotifyException as err:
            if err.http_status == 429:
                retry_after = int(err.headers.get('Retry-After', 1))
                time.sleep(retry_after)
    track_list.append(track)

df_2000s = pd.concat([pd.DataFrame(t) for t in track_list], ignore_index=True)

df_2000s['artist_names'] = id_2000s['Artist']
df_2000s['track_name'] = id_2000s['Track']

df_2000s['duration_secs'] = df_2000s['duration_ms'] // 1000

df_2000s = df_2000s.drop(['type'], axis=1)
df_2000s = df_2000s.drop(['uri'], axis=1)
df_2000s = df_2000s.drop(['track_href'], axis=1)
df_2000s = df_2000s.drop(['analysis_url'], axis=1)
df_2000s = df_2000s.drop(['time_signature'], axis=1)
df_2000s = df_2000s.drop(['id'], axis=1)
df_2000s = df_2000s.drop(['duration_ms'], axis=1)

df_2000s = df_2000s[['artist_names', 'track_name', 'danceability', 'energy','key', 'loudness', 'mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_secs']]
df_2000s.to_csv('data.csv')