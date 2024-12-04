import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

REQ_PATH = "request_D.txt"
RES_PATH = "response_D.txt"


def read_request():
    try:
        with open(REQ_PATH, "r") as file:
            lines = file.readlines()
        # Clear the request file after reading
        with open(REQ_PATH, "w") as file:
            file.write("")
        return lines
    except FileNotFoundError:
        return None


def write_response(response):
    try:
        with open(RES_PATH, "w") as file:
            file.write(response)
    except Exception as e:
        print(f"Error writing response: {e}")


def create_playlist(sp, user_id, playlist_name):
    try:
        playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
        write_response(f"Playlist created successfully: {playlist['id']}")
    except Exception as e:
        write_response(f"Error: {e}")


def add_first_song(sp, playlist_id, song_name):
    try:
        # Search for the song
        results = sp.search(q=song_name, type='track', limit=1)
        track_id = results['tracks']['items'][0]['id']
        sp.playlist_add_items(playlist_id, [track_id])
        write_response(f"Song '{song_name}' added successfully")
    except Exception as e:
        write_response(f"Error: {e}")


def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-private playlist-modify-public"
    ))
    user_id = sp.current_user()["id"]

    while True:
        request = read_request()
        if request:
            if len(request) == 1:
                playlist_name = request[0].strip()
                create_playlist(sp, user_id, playlist_name)
            elif len(request) == 2:
                playlist_id, song_name = request[0].strip(), request[1].strip()
                add_first_song(sp, playlist_id, song_name)
        time.sleep(3)


if __name__ == "__main__":
    main()
