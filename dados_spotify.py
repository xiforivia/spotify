import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="7469b025690441a6900dbdf0fd955211",
                                                           client_secret="94d9a566dcb1458babdfc4992902db7c"))

headers = {
    'Authorization': 'Bearer {token}'.format(token='BQDaNe7mUS1ejXNVtlq1vgliz6Nhjgeoyo3AJsMkWdd3qFjYGtJJ9BMztFvaR8AfFbaxiTmLEvgVxBES_Bt9PAMUhzsAeMvQrRI0lKtDSFXgwVOoGcHt_KXsUQNuAqvaZ5jMeqCZmQZPHSmsZQ0-VmTMKEpVZ3k-B6qbQz-jGZC2CbjF4_zqAiZMjasPkBTMVzI')
}

import requests
# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
track_id = '7ouMYWpwJ422jRcDASZB7P'

# actual GET request with proper header
r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

artist_name = []
track_name = []
track_id = []
track_number = []

lista_response = []
dct_response = {}

results = sp.playlist_tracks(playlist_id='37i9dQZEVXbMDoHDwVN2tF')

for i, item in enumerate(results['items']):
    track = item['track']
    artist_name.append(track['artists'][0]['name'])
    track_name.append(track['name'])
    track_id.append(track['id'])
    r = requests.get(BASE_URL + 'audio-features/' + track['id'], headers=headers)
    lista = r.json()
    dct_response.update({track['artists'][0]['name']+"+"+track['name']: lista})


df = pd.DataFrame(dct_response).T.reset_index()
df[['artista', 'musica']] = df['index'].str.split('+', expand=True)
df = df.drop("index", axis='columns')

df = df[['artista', 'musica', 'danceability', 'energy', 'key', 'loudness', 'mode',
       'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url',
       'duration_ms', 'time_signature']]

df = df.drop(["type", "uri", "track_href", "analysis_url", "time_signature", "id", "mode"], axis='columns')

df = df.rename(columns={
       'artista': 'artista',
       'musica': 'musica',
       'danceability': 'dancabilidade',
       'energy': 'energia', 
       'key':'chave',
       'loudness': 'volume',
       'speechiness': 'presenca_palavras',
       'acousticness': 'acustica', 
       'instrumentalness': 'instrumentalidade',
       'liveness' :'ao_vivo',
       'valence': 'positividade',
       'tempo': 'tempo',
       'duration_ms': 'duracao_ms'
})

df.to_excel(r'{}\base_musical.xlsx'.format(os.getcwd()), )


