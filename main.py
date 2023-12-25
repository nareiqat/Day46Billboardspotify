from bs4 import BeautifulSoup
import datetime
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

# date = input("Which year do you want to go to? YYYY-MM-DD")
# year, month, day = map(int, date.split('-'))
# date1 = datetime.date(year, month, day)
date1 = "2007-06-16"

api_key = os.getenv("SECRET_KEY")
client_id = os.getenv("CLIENT_ID")

print(f"client id: {client_id}")
print(f"Secret Key: {api_key}")

URL = f"https://www.billboard.com/charts/hot-100/{date1}"

response = requests.get(URL)

page_html = response.text

soup = BeautifulSoup(page_html,"html.parser")

name_of_movies = soup.select(".o-chart-results-list__item .a-font-primary-bold-s")

song_names = [movies.getText().replace("\n", "").replace("\t", "") for movies in name_of_movies]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=api_key,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

list_uris = []
for song_name in song_names:
    # Perform a search for the song
    results = sp.search(q=song_name, type='track', limit=1)
    print(results)

    # # Check if there are any results
    try:
        track_uri = results['tracks']['items'][0]['uri']
        list_uris.append(track_uri)
    except IndexError:
        print(f"{song_name} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user_id, "My Favorite Songs", public=True, description="The list of my favorite "
                                                                                            "songs")
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=list_uris)


