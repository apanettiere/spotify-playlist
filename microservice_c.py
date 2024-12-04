import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

REQ_PATH = "request_C.txt"
RES_PATH = "response_C.txt"


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


def show_top_songs(sp, artist_name):
    try:
        # Search for the artist
        results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
        artist_id = results['artists']['items'][0]['id']

        # Get the artist's top tracks
        top_tracks = sp.artist_top_tracks(artist_id)['tracks']
        songs = "\n".join(
            [f"{track['name']} - {track['id']}" for track in top_tracks[:10]])
        write_response(songs)
    except Exception as e:
        write_response(f"Error: {e}")


def add_top_song_to_playlist(sp, track_id, playlist_id):
    try:
        sp.playlist_add_items(playlist_id, [track_id])
        write_response("Song added successfully")
    except Exception as e:
        write_response(f"Error: {e}")


def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-private playlist-read-private"
    ))

    while True:
        request = read_request()
        if request:
            if len(request) == 1:
                artist_name = request[0].strip()
                show_top_songs(sp, artist_name)
            elif len(request) == 2:
                track_id, playlist_id = request[0].strip(), request[1].strip()
                add_top_song_to_playlist(sp, track_id, playlist_id)
        time.sleep(3)


if __name__ == "__main__":
    main()
