import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=os.getenv("SPOTIPY_SCOPE", "playlist-read-private")
))

def read_request():
    try:
        with open("request.txt", "r") as file:
            playlist_id = file.read().strip()
            return playlist_id
    except FileNotFoundError:
        return None

def write_response(duplicates):
    with open("response.txt", "w") as file:
        if duplicates:
            for song in duplicates:
                file.write(f"{song}\n")
        else:
            file.write("No duplicates found.\n")

def check_duplicates(playlist_id):
    tracks = {}
    duplicates = []

    try:
        results = sp.playlist_items(playlist_id)
        for item in results['items']:
            track = item['track']
            track_name = track['name']
            track_artist = track['artists'][0]['name']
            song_key = f"{track_name} - {track_artist}"

            if song_key in tracks:
                duplicates.append(song_key)
            else:
                tracks[song_key] = 1

        return duplicates
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    print("Microservice is running...")
    while True:
        playlist_id = read_request()
        if playlist_id:
            print("Processing request...")
            duplicates = check_duplicates(playlist_id)
            write_response(duplicates)
            print("Response written to 'response.txt'.")
            open("request.txt", "w").close()
        time.sleep(5)
