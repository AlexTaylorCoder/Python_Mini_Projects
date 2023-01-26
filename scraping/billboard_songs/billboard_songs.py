
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os 

dotenv.load_dotenv()

SPOTIFY_KEY = os.getenv("SPOTIFY_AUTH")
SPOTIFY_CLIENT = os.getenv("SPOTIFY_CLIENT")

SONG_ENDPOINT = "https://www.billboard.com/charts/hot-100/"

time_input = input("Enter a date in YYYY-MM-DD format: ")


response = requests.get(SONG_ENDPOINT+time_input)
data = response.text

soup = BeautifulSoup(data,"html.parser")

songs_names_h3 = soup.select(".o-chart-results-list__item h3.c-title")
songs_names = [song.getText().strip() for song in songs_names_h3]


with open("songs.txt","w") as f:
    for song in songs_names:
        f.write(song + "\n")



with open("songs.txt") as f:
    file = f.readlines()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT,
    client_secret=SPOTIFY_KEY, 
    redirect_uri="https://www.google.com/",
    show_dialog=True,
    cache_path="token.txt"))

user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id,name=f"{time_input} Billboard 100",collaborative=False,description=f"Compiled from {time_input} billboard top 100.",public=False)

loc = []
year = time_input.split('-')[0]
for s in songs_names:
    result = sp.search(q=f"track:{s} year:{year}",type="track",limit=1)["tracks"]["items"][0]["uri"]
    loc.append(result)

sp.playlist_add_items(playlist_id=playlist["id"], items=loc, position=None)
# playlist_change_details()