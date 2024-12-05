import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

REQ_PATH = "request_D.txt"
RES_PATH = "response_D.txt"


def read_request():
    """Reads the request from the file."""
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
    """Writes the response to the file."""
    try:
        with open(RES_PATH, "w") as file:
            file.write(response)
    except Exception as e:
        print(f"Error writing response: {e}")


def create_playlist(sp, user_id, playlist_name):
    """Creates a new playlist and writes the playlist ID to the response file."""
    try:
        playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
        write_response(f"Playlist created successfully: {playlist['id']}")
    except Exception as e:
        write_response(f"Error: {e}")


def main():
    """Main function to handle requests."""
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-private playlist-modify-public"
    ))
    user_id = sp.current_user()["id"]

    while True:
        # Read request
        request = read_request()
        if request:
            if len(request) == 1:
                playlist_name = request[0].strip()
                create_playlist(sp, user_id, playlist_name)
            else:
                write_response(
                    "Invalid request format. Expected one line for the playlist name.")
        else:
            # Indicate the microservice is running
            write_response("Microservice D is running.")
        time.sleep(3)


if __name__ == "__main__":
    main()
