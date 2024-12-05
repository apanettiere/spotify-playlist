import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

REQ_PATH = "request_C.txt"
RES_PATH = "response_C.txt"


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


def show_top_songs(sp, artist_name):
    """Fetches and writes the top 10 songs for a given artist."""
    try:
        # Search for the artist
        results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
        if not results['artists']['items']:
            write_response(f"Artist '{artist_name}' not found.")
            return

        artist_id = results['artists']['items'][0]['id']

        # Get the artist's top tracks
        top_tracks = sp.artist_top_tracks(artist_id)['tracks']
        songs = "\n".join(
            [f"{track['name']} - {track['id']}" for track in top_tracks[:10]])
        write_response(songs)
    except Exception as e:
        write_response(f"Error: {e}")


def main():
    """Main function to handle requests."""
    # Initialize Spotify API client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-read-private"
    ))

    while True:
        # Read and process requests
        request = read_request()
        if request:
            if len(request) == 1:
                artist_name = request[0].strip()
                show_top_songs(sp, artist_name)
            else:
                write_response(
                    "Invalid request format. Expected one line for artist name.")
        else:
            # Provide success message when idle
            write_response("Microservice C is running successfully.")
        time.sleep(3)


if __name__ == "__main__":
    main()
