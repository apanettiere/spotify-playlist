import os
import time
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

# Load environment variables
load_dotenv()

# Spotify API setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public playlist-modify-private user-library-read"
))

user_id = sp.current_user()["id"]  # Get the user's Spotify ID

# File paths for communication with microservices
REQ_A_PATH = "request.txt"
RES_A_PATH = "response.txt"
REQ_B_PATH = "request_B.txt"
RES_B_PATH = "response_B.txt"
REQ_C_PATH = "request_C.txt"
RES_C_PATH = "response_C.txt"
REQ_D_PATH = "request_D.txt"
RES_D_PATH = "response_D.txt"


def write_request(file_path, data):
    """Writes a request to the specified file."""
    try:
        with open(file_path, "w") as file:
            file.write(data)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")


def read_response(file_path):
    """Reads a response from the specified file."""
    try:
        with open(file_path, "r") as file:
            response = file.read().strip()
        # Clear the response file after reading
        with open(file_path, "w") as file:
            file.write("")
        return response
    except Exception as e:
        print(f"Error reading from {file_path}: {e}")
        return None


# User Story 1: Add a Song to a Playlist
def add_song_to_playlist():
    try:
        playlist_id = input("Enter your playlist ID: ").strip()
        song_name = input("Enter the song name: ").strip()

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
        playlist_id = input("Enter your playlist ID: ").strip()
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']

        if tracks:
            print("\nSongs in Playlist:")
            for idx, item in enumerate(tracks):
                track = item['track']
                print(f"{idx + 1}: {track['name']
                                    } by {track['artists'][0]['name']}")
        else:
            print("No songs found in the playlist.")
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# User Story 3: Delete a Song from a Playlist
def delete_song_from_playlist():
    try:
        playlist_id = input("Enter your playlist ID: ").strip()
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']

        if tracks:
            print("\nSongs in Playlist:")
            for idx, item in enumerate(tracks, start=1):
                track = item['track']
                print(f"{idx}: {track['name']} by {
                      track['artists'][0]['name']}")

            # Select song to delete
            try:
                song_number = int(
                    input("Enter the number of the song to delete: ").strip())
                if 1 <= song_number <= len(tracks):
                    track_to_delete = tracks[song_number - 1]
                    track_id = track_to_delete['track']['id']

                    # Remove the selected track
                    sp.playlist_remove_all_occurrences_of_items(
                        playlist_id, [track_id])
                    print(
                        f"Song '{track_to_delete['track']['name']}' deleted successfully.")
                else:
                    print("Invalid selection. Please choose a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("No songs found in the playlist.")
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Microservice A: Check for Duplicates


def check_duplicates():
    """Checks for duplicates in a playlist using Microservice A."""
    playlist_id = input("Enter your playlist ID: ").strip()
    delete_choice = input("Delete duplicates? (y/n): ").strip().lower()

    if delete_choice not in ['y', 'n']:
        print("Invalid choice. Please enter 'y' or 'n'.")
        return

    write_request(REQ_A_PATH, f"{playlist_id}\n{delete_choice}")
    print("Waiting for response from Microservice A...")
    time.sleep(5)  # Wait for Microservice A to process

    response = read_response(RES_A_PATH)
    if response:
        if response.lower() == "none":
            print("No duplicates found.")
        else:
            print("Duplicates found:")
            print(response)
    else:
        print("No response from Microservice A.")


# Microservice B: Shuffle Playlist
def shuffle_playlist():
    """Shuffles a playlist using Microservice B."""
    playlist_id = input("Enter your playlist ID: ").strip()
    write_request(REQ_B_PATH, playlist_id)
    print("Waiting for response from Microservice B...")
    time.sleep(5)  # Wait for Microservice B to process

    response = read_response(RES_B_PATH)
    if response:
        print(response)
    else:
        print("No response from Microservice B.")


# Microservice C: Show Top Songs for an Artist
def show_top_songs():
    """Shows top songs for an artist using Microservice C."""
    artist_name = input("Enter the artist's name: ").strip()
    write_request(REQ_C_PATH, artist_name)
    print("Waiting for response from Microservice C...")
    time.sleep(5)  # Wait for Microservice C to process

    response = read_response(RES_C_PATH)
    if response:
        print("Top Songs:")
        print(response)
    else:
        print("No response from Microservice C.")

# Microservice D: Create a New Playlist


def create_playlist():
    """Creates a new playlist using Microservice D."""
    playlist_name = input("Enter a name for your new playlist: ").strip()
    write_request(REQ_D_PATH, playlist_name)
    print("Waiting for response from Microservice D...")
    time.sleep(5)  # Wait for Microservice D to process

    response = read_response(RES_D_PATH)
    if response:
        print(response)
    else:
        print("No response from Microservice D.")

# Main Menu


def menu():
    """Displays the main menu."""
    print("\nSpotify Playlist Manager")
    print("1. Add a Song to Playlist (User Story 1)")
    print("2. View Songs in Playlist (User Story 2)")
    print("3. Delete a Song from Playlist (User Story 3)")
    print("4. Check for Duplicates in Playlist (Microservice A)")
    print("5. Shuffle Playlist (Microservice B)")
    print("6. Show Top Songs for an Artist (Microservice C)")
    print("7. Create a New Playlist (Microservice D)")
    print("8. Exit")

# Adjusted Main Program


def main():
    """Main program loop."""
    while True:
        menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            add_song_to_playlist()
        elif choice == "2":
            view_songs_in_playlist()
        elif choice == "3":
            delete_song_from_playlist()
        elif choice == "4":
            check_duplicates()
        elif choice == "5":
            shuffle_playlist()
        elif choice == "6":
            show_top_songs()
        elif choice == "7":
            create_playlist()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
