# imports
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv
import os

import time

# Declaring Constants

REQ_PATH = "request.txt"
RES_PATH = "response.txt"

# Declare global variables


def loadEnvironment():
    load_dotenv()
    # get info from .env
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    scope = os.getenv("SPOTIPY_SCOPE")
    return SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

def getRequest():
    try:
        with open(REQ_PATH, "r") as file:
            # Read the first line as playlist ID and the second line as delete choice
            playlistId = file.readline().strip()  # Read and strip the playlist ID
            deleteChoice = file.readline().strip().lower()  # Read and strip the delete choice

            file.close()

            file = open(REQ_PATH, "w")
            file.write("")

            if playlistId == "" :
                return None
            
            # Ensure the delete choice is either 'yes' or 'no'
            if deleteChoice not in ['y', 'n']:
                print("Error: Invalid delete choice in request.txt. Please use 'yes' or 'no'.")
                return None
            
            # Return both playlist ID and delete choice as a tuple
            return playlistId, deleteChoice
    except FileNotFoundError:
        print(f"Error: The file '{REQ_PATH}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def outputResponse(output):
    try:
        with open(RES_PATH, "w") as file:
            file.write(output)  # Remove any extra whitespace or newlines
            return True
    except FileNotFoundError:
        print(f"Error: The file '{RES_PATH}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# This will find duplicates in the playlist, and return the list of them.
def findDuplicates(sp, playlistId):
    try:
        # Fetch playlist tracks
        tracks = []
        results = sp.playlist_items(playlistId)
        while results:
            tracks.extend(results['items'])
            results = sp.next(results) if results['next'] else None

        # Extract track IDs and names
        trackData = [
            {"id": track['track']['id'], "name": track['track']['name']}
            for track in tracks if track['track']
        ]

        # Detect duplicates
        seen = {}
        duplicates = []
        for track in trackData:
            trackId = track['id']
            if trackId in seen:
                if trackId not in [dup['id'] for dup in duplicates]:
                    duplicates.append({"id": trackId, "name": track["name"]})
            else:
                seen[trackId] = track

        return duplicates
    except Exception as e:
        print(f"An error occurred while finding duplicates: {e}")
        return None

def removeDuplicates(sp, playlistId, duplicates):
    try:
        # Remove all instances of duplicates
        for duplicate in duplicates:
            duplicateId = duplicate['id']
            print(f"Removing all instances of {duplicate['name']} (ID: {duplicateId})")
            
            # Fetch all tracks to remove
            tracks = sp.playlist_items(playlistId)['items']
            toRemove = [
                {"uri": f"spotify:track:{track['track']['id']}", "positions": [i]}
                for i, track in enumerate(tracks) if track['track']['id'] == duplicateId
            ]
            
            # Remove all instances
            if toRemove:
                sp.playlist_remove_specific_occurrences_of_items(playlistId, toRemove)

            # Add back one instance
            print(f"Adding back one instance of {duplicate['name']} (ID: {duplicateId})")
            sp.playlist_add_items(playlistId, [f"spotify:track:{duplicateId}"])

        print("All duplicates processed successfully!")
    except Exception as e:
        print(f"An error occurred while removing and re-adding duplicates: {e}")


if __name__ == "__main__":
    # Load environment
    sp_oauth = loadEnvironment()
    sp = spotipy.Spotify(auth_manager=sp_oauth)


    while True :
    # Get request
        request = getRequest()
        
        # Find duplicates
        if request:
            playlistId, deleteChoice = request
            duplicates = findDuplicates(sp, playlistId)
            if duplicates:
                
                if (deleteChoice == "y"):
                    print(f"Found {len(duplicates)} duplicate track(s). Removing and re-adding...")
                    removeDuplicates(sp, playlistId, duplicates)
                    outputResponse("None")
                else:
                    print("No duplicates were deleted.")
                    outputResponse("\n".join(str(item) for item in duplicates))
            else:
                # nothing to report
                print("No duplicate tracks found.")
                outputResponse("None")
        # Wait 3 seconds to check again
        time.sleep(3)
