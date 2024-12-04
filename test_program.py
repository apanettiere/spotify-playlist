import time

def write_request(playlist_id):
    with open("request.txt", "w") as file:
        file.write(playlist_id)

def read_response():
    try:
        with open("response.txt", "r") as file:
            duplicates = file.readlines()
            if duplicates:
                print("Duplicate songs found:")
                for song in duplicates:
                    print(song.strip())
            else:
                print("No duplicates found.")
    except FileNotFoundError:
        print("Response file not found. Please run the microservice.")

if __name__ == "__main__":
    playlist_id = input("Enter your Spotify playlist ID: ")
    write_request(playlist_id)
    print("Request written to 'request.txt'. Waiting for response...")
    time.sleep(10)
    read_response()
