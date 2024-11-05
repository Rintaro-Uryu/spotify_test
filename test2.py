import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

client_id = '43ea166d32604a26b7ca3afba4572393'
client_secret = '55855b99cf584feca3cf709db376bae2'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

name = 'sakanaction'
result = spotify.search(q='artist:' + name, type='artist')
name = result['artists']['items'][0]['name']
genres = result['artists']['items'][0]['genres']
print('name : {} - genres : {}'.format(name, genres))

"""
result = spotify.artist_related_artists('0hCWVMGGQnRVfDgmhwLIxq')
for artist in result['artists']:
    artist_name = artist['name']
    popularity = artist['popularity']
    genres = artist['genres']
    info = 'アーティスト名： {0} - 人気: {1} ジャンル: {2}'.format(artist_name, popularity, genres)
    print(info)
"""