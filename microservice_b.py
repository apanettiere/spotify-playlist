import os
import random
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

REQ_PATH = "request_B.txt"
RES_PATH = "response_B.txt"


def read_request():
    try:
        with open(REQ_PATH, "r") as file:
            playlist_id = file.read().strip()
        # Clear the request file after reading
        with open(REQ_PATH, "w") as file:
            file.write("")
        return playlist_id
    except FileNotFoundError:
        return None


def write_response(response):
    try:
        with open(RES_PATH, "w") as file:
            file.write(response)
    except Exception as e:
        print(f"Error writing response: {e}")


def shuffle_playlist(sp, playlist_id):
    try:
        # Get playlist tracks
        results = sp.playlist_tracks(playlist_id)
        tracks = [item['track']['id'] for item in results['items']]

        # Shuffle the tracks
        random.shuffle(tracks)

        # Replace the playlist with the shuffled tracks
        sp.playlist_replace_items(playlist_id, tracks)
        write_response("Playlist shuffled successfully")
    except Exception as e:
        write_response(f"Error: {e}")


def main():
    # Spotify API setup
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-private playlist-modify-public"
    ))

    while True:
        playlist_id = read_request()
        if playlist_id:
            shuffle_playlist(sp, playlist_id)
        time.sleep(3)


if __name__ == "__main__":
    main()
