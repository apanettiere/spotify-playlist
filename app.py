import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=os.getenv("SPOTIPY_SCOPE")
))

user_id = sp.current_user()["id"]  # Get the user's Spotify ID

# User Story 1: Add a Song to a Playlist
def add_song_to_playlist():
    try:
        playlist_id = input("Enter your playlist ID: ")
        song_name = input("Enter the song name: ")

        # Search for the song
        results = sp.search(q=song_name, type='track', limit=1)
        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['id']
            sp.playlist_add_items(playlist_id, [track_id])
            print(f"'{song_name}' has been added to the playlist.")
        else:
            print("Song not found. Please try again.")
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# User Story 2: View All Songs in a Playlist
def view_songs_in_playlist():
    try:
        playlist_id = input("Enter your playlist ID: ")
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']

        if tracks:
            print("\nSongs in Playlist:")
            for idx, item in enumerate(tracks):
                track = item['track']
                print(f"{idx + 1}: {track['name']} by {track['artists'][0]['name']}")
        else:
            print("No songs found in the playlist.")
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# User Story 3: Delete a Song from a Playlist
def delete_song_from_playlist():
    try:
        playlist_id = input("Enter your playlist ID: ")
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']

        if tracks:
            print("\nSongs in Playlist:")
            for idx, item in enumerate(tracks):
                track = item['track']
                print(f"{idx + 1}: {track['name']} by {track['artists'][0]['name']}")

            # Select song to delete
            try:
                song_number = int(input("Enter the number of the song to delete: ")) - 1
                if 0 <= song_number < len(tracks):
                    track_id = tracks[song_number]['track']['id']
                    sp.playlist_remove_all_occurrences_of_items(playlist_id, [track_id])
                    print("Song deleted successfully.")
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("No songs found in the playlist.")
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main Menu
def main():
    while True:
        print("\nSpotify Playlist Manager")
        print("1. Add a Song to Playlist")
        print("2. View Songs in Playlist")
        print("3. Delete a Song from Playlist")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            add_song_to_playlist()
        elif choice == "2":
            view_songs_in_playlist()
        elif choice == "3":
            delete_song_from_playlist()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
