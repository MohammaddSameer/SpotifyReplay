#!/usr/bin/env python3


# TO DO
# Add a menu
# Sort songs by most time played (dynamic time ex. 75 mins prints as 1h 15 mins)
# Most played artists
# Search for a song
# Search for an artist
# make functions to open file
# Make a bar graph showing an artist and their time played each month for a year

import json
from collections import defaultdict
import datetime
from collections import defaultdict
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import os




scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="df93e00dbc434caab50d3e05cc59386d", client_secret="10237c2063664b94949b7a22c550c3f6",
                                                redirect_uri="http://8080/callback", scope=scope))



user = sp.current_user()
display_name = user["display_name"]
print(f"Logged in as {display_name}")

access_token = sp.auth_manager.get_cached_token()['access_token']







def load_data(file_paths):
    songs = {}
    for file_path in file_paths:
        with open(file_path, encoding= 'utf-8') as f:
            data = json.load(f)

        for song in data:
            artist = song['artistName']
            track = song['trackName']
            duration = song['msPlayed'] / 1000  # Convert ms to seconds
            key = (artist, track)
            if key not in songs:
                songs[key] = {'play_count': 1, 'duration': duration}
            else:
                songs[key]['play_count'] += 1
                songs[key]['duration'] += duration

    return songs





def format_duration(duration):
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    if hours == 0:
        return f"{minutes} minute{'s' if minutes > 1 else ''}"
    elif minutes == 0:
        return f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        return f"{hours} hour{'s' if hours > 1 else ''} and {minutes} minute{'s' if minutes > 1 else ''}"







def top_songs_by_play_count(songs, num_songs):
    sorted_songs = sorted(songs.items(), key=lambda x: x[1]['play_count'], reverse=True)
    for i, ((artist, track), data) in enumerate(sorted_songs[:num_songs]):
        play_count = data['play_count']
        print(f"{i+1}. {artist} \"{track}\" ({play_count} plays)")
    print()




def top_songs_by_duration(songs, num_songs):
    sorted_songs = sorted(songs.items(), key=lambda x: x[1]['duration'], reverse=True)
    for i, ((artist, track), song_data) in enumerate(sorted_songs[:num_songs]):
        duration = song_data['duration']
        formatted_duration = format_duration(duration)
        play_count = song_data['play_count']
        print(f"{i+1}. {artist} \"{track}\" ({formatted_duration})")
    print()



def search_for_song(songs, query):
    matching_songs = filter(lambda x: query.lower() in x[0][1].lower(), songs.items())
    sorted_songs = sorted(matching_songs, key=lambda x: x[1]['play_count'], reverse=True)
    if not sorted_songs:
        print(f"No song found matching '{query}'")
        return

    for i, ((artist, track), song_data) in enumerate(sorted_songs):
        play_count = song_data['play_count']
        print(f"{i+1}. {artist} \"{track}\" ({play_count} plays)")






def search_for_artist(songs, query):
    matching_songs = filter(lambda x: query.lower() in x[0][0].lower(), songs.items())
    artist_play_counts = defaultdict(int)
    for (artist, track), data in matching_songs:
        artist_play_counts[artist] += data['play_count']
    sorted_artists = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)
    if not sorted_artists:
        print(f"No artist found matching '{query}'")
        return

    for i, (artist, play_count) in enumerate(sorted_artists):
        print(f"{i+1}. {artist}")

    while True:
        artist_num = input("Enter the number of the artist you want to view, or 'q' to quit: ")
        if artist_num == 'q':
            break
        try:
            artist_num = int(artist_num)
            if artist_num < 1 or artist_num > len(sorted_artists):
                raise ValueError
        except ValueError:
            print("Invalid input, please enter a valid artist number or 'q' to quit.")
            continue

        artist_name, _ = sorted_artists[artist_num - 1]

        matching_songs = filter(lambda x: x[0][0] == artist_name, songs.items())
        sorted_songs = sorted(matching_songs, key=lambda x: x[1]['play_count'], reverse=True)
        for i, ((_, track), data) in enumerate(sorted_songs):
            play_count = data['play_count']
            print(f"{i+1}. \"{track}\" ({play_count} plays)")
        break


    # Spotify Web API search endpoint to search for artists
    search_endpoint = 'https://api.spotify.com/v1/search'



    # Build the URL to search for artists
    params = {'q': artist_name, 'type': 'artist', 'limit': 1}
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.get(search_endpoint, params=params, headers=headers)
    if response.status_code != 200:
        print('Error searching for artist:', response.text)
        exit()

    # Retrieve the artist ID from the search results
    search_results = response.json()
    artist_id = search_results['artists']['items'][0]['id']


        # Spotify Web API endpoint to retrieve artist data
    artist_endpoint = 'https://api.spotify.com/v1/artists/'


    # Build the URL to retrieve artist data, including the profile picture URL
    artist_url = artist_endpoint + artist_id
    params = {'include_groups': 'album,single', 'market': 'US'}
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }
    response = requests.get(artist_url, params=params, headers=headers)
    if response.status_code != 200:
        print('Error retrieving artist data:', response.text)
        exit()
    artist_data = response.json()
    profile_picture_url = artist_data['images'][0]['url']

    # Retrieve the profile picture from the URL
    response = requests.get(profile_picture_url)
    if response.status_code != 200:
        print('Error retrieving profile picture:', response.text)
        exit()


    # Save the image to a file
    with open(f'{artist_name}_picture.png', 'wb') as f:
        f.write(response.content)





    print()
    return os.path.join(os.getcwd(), f'{artist_name}_picture.png')





def main():
    #file_paths = ["StreamingHistory0.json", "StreamingHistory1.json", "StreamingHistory2.json"]
    file_paths = ["StreamingHistoryMain0.json", "StreamingHistoryMain1.json"]
    #file_paths = ["StreamingHistory0V2.json", "StreamingHistory1V2.json"]
    #file_paths = ["StreamingHistory0S.json", "StreamingHistory1S.json", "StreamingHistory2S.json"]
    #file_paths = ["StreamingHistory0Z.json", "StreamingHistory1Z.json", "StreamingHistory2Z.json"]
    #file_paths = ["StreamingHistory0D.json", "StreamingHistory1D.json", "StreamingHistory2D.json", "StreamingHistory3D.json", "StreamingHistory4D.json", "StreamingHistory5D.json"]

    image_path = ''

    songs = load_data(file_paths)

    

    while True:
        print("**********************************")
        print("Choose an option:")
        print("1. Show top songs by play count")
        print("2. Show top songs by duration")
        print("3. Search for a song")
        print("4. Search for an artist")
        print("5. Quit")
        print("**********************************")


        choice = input("Enter your choice: ")
        if os.path.exists(image_path):
            os.remove(image_path)

        if choice == "1":
            num_songs = int(input("Enter the number of songs to show: "))
            top_songs_by_play_count(songs, num_songs)
        elif choice == "2":
            num_songs = int(input("Enter the number of songs to show: "))
            top_songs_by_duration(songs, num_songs)
        elif choice == "3":
            query = input("Enter a search query: ")
            search_for_song(songs, query)
        elif choice == "4":
            query = input("Enter a search query: ")
            image_path = search_for_artist(songs, query)
            print(image_path)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
