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
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.font_manager import FontProperties



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

    while True:
        song_num = input("Enter the number of the song you want to view, or 'q' to quit: ")
        if song_num == 'q':
            break
        try:
            song_num = int(song_num)
            if song_num < 1 or song_num > len(sorted_songs):
                raise ValueError
        except ValueError:
            print("Invalid input, please enter a valid song number or 'q' to quit.")
            continue

        (artist_name, song_name), song_data = sorted_songs[song_num - 1]
        play_count = song_data['play_count']
        print(f"Song: \"{song_name}\" by {artist_name}")
        print(f"Play Count: {play_count} plays")
        break




def top_artists_by_duration(songs, num_artists):
    artist_durations = defaultdict(float)

    # Calculate total listening duration for each artist
    for (artist, _), song_data in songs.items():
        artist_durations[artist] += song_data['duration']

    # Sort artists by total listening duration
    sorted_artists = sorted(artist_durations.items(), key=lambda x: x[1], reverse=True)

    # Display the top artists
    for i, (artist, duration) in enumerate(sorted_artists[:num_artists]):
        formatted_duration = format_duration(duration)
        print(f"{i+1}. {artist} ({formatted_duration})")





def top_artists_by_play_count(songs, num_artists):
    artist_play_counts = defaultdict(int)

    # Count the number of times each artist appears in the listening history
    for (artist, _), song_data in songs.items():
        artist_play_counts[artist] += song_data['play_count']

    # Sort artists by play count
    sorted_artists = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)

    # Display the top artists
    for i, (artist, play_count) in enumerate(sorted_artists[:num_artists]):
        print(f"{i+1}. {artist} ({play_count} plays)")






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





def get_top_songs_by_duration(songs, num_songs):
    sorted_songs = sorted(songs.items(), key=lambda x: x[1]['duration'], reverse=True)
    return sorted_songs[:num_songs]


def get_top_artists_by_duration(songs, num_artists):
    # Create a dictionary to store the total listening duration for each artist
    artist_durations = {}

    # Iterate through the songs and accumulate the duration for each artist
    for (artist, _), song_data in songs.items():
        if artist not in artist_durations:
            artist_durations[artist] = 0
        artist_durations[artist] += song_data['duration']

    # Sort the artists by their total listening duration in descending order
    sorted_artists = sorted(artist_durations.items(), key=lambda x: x[1], reverse=True)

    # Return the top N artists by duration
    return sorted_artists[:num_artists]





def get_cover_art_url(track_name, artist_name):
    # Use the Spotify API to search for the track and retrieve its cover art URL
    results = sp.search(q=f"track:{track_name} artist:{artist_name}", type="track", limit=1)
    if results['tracks']['items']:
        return results['tracks']['items'][0]['album']['images'][0]['url']
    return None


def get_artist_profile_picture(artist_name):
    # Use the Spotify API to search for the artist and retrieve their profile picture URL
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
    if results['artists']['items']:
        return results['artists']['items'][0]['images'][0]['url']
    return None




def create_bar_chart(top_songs):
    song_names = []
    song_durations_hours = []
    cover_images = []

    for ((artist, track), song_data) in top_songs:
        cover_url = get_cover_art_url(track, artist)
        if cover_url:
            song_names.append(f"{artist} - {track}")
            duration_hours = song_data['duration'] / 3600  # Convert duration to hours
            song_durations_hours.append(duration_hours)
            cover_images.append(Image.open(BytesIO(requests.get(cover_url).content)))

    num_songs = len(cover_images)
    img_width = max(0.01, 0.5 / num_songs)  # Calculate the image width based on the number of songs

    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#6C02BC')
    ax.set_facecolor('#6C02BC')


    # Set the font color to white
    ax.xaxis.label.set_color('#F4FE46')
    ax.yaxis.label.set_color('#F4FE46')
    ax.title.set_color('#F4FE46')
    ax.tick_params(axis='x', colors='#F4FE46')
    ax.tick_params(axis='y', colors='#F4FE46')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Specify the path to your Spotify font file (.otf)
    spotify_font_path = '.\CircularStd-Black.otf'

    # Create a FontProperties object with the Spotify font
    spotify_font = FontProperties(fname=spotify_font_path)


    ax.barh(range(len(cover_images)), song_durations_hours, color='#1DB954')
    ax.set_yticks(range(len(cover_images)))
    ax.set_yticklabels(song_names,fontproperties=spotify_font, fontsize = 10)
    ax.set_xlabel('Total Listening Time (hours)', fontproperties=spotify_font, fontsize = 30)
    ax.set_title('Top Songs by Total Listening Time', fontproperties=spotify_font, fontsize = 30)
    ax.invert_yaxis()  # Invert y-axis to display the top song at the top

    for i, (img, duration) in enumerate(zip(cover_images, song_durations_hours)):

        # Calculate the x-position to align the image at the end of the bar
        x_position = duration - (img_width * 35)

        # Create an OffsetImage and AnnotationBbox to display the image at the end of the bar
        img_offset = OffsetImage(img, zoom=img_width, alpha = 1)
        img_ab = AnnotationBbox(img_offset, (x_position, i), frameon=False)
        ax.add_artist(img_ab)

    plt.tight_layout()

    plt.show()



def create_artist_bar_chart(top_artists):
    artist_names = []
    artist_durations_hours = []
    artist_images = []

    for (artist, duration) in top_artists:
        artist_names.append(artist)
        duration_hours = duration / 3600  # Convert duration to hours
        artist_durations_hours.append(duration_hours)
        artist_profile_url = get_artist_profile_picture(artist)
        if artist_profile_url:
            artist_images.append(Image.open(BytesIO(requests.get(artist_profile_url).content)))

    num_artists = len(artist_images)
    img_width = max(0.01, 0.5 / num_artists)  # Calculate the image width based on the number of artists

    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Set the font color to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Specify the path to your Spotify font file (.otf)
    spotify_font_path = '.\CircularStd-Black.otf'

    # Create a FontProperties object with the Spotify font
    spotify_font = FontProperties(fname=spotify_font_path)

    ax.barh(range(len(artist_images)), artist_durations_hours, color='#1DB954')
    ax.set_yticks(range(len(artist_images)))
    ax.set_yticklabels(artist_names, fontproperties=spotify_font, fontsize=10)
    ax.set_xlabel('Total Listening Time (hours)', fontproperties=spotify_font, fontsize=30)
    ax.set_title('Top Artists by Total Listening Time', fontproperties=spotify_font, fontsize=30)
    ax.invert_yaxis()  # Invert y-axis to display the top artist at the top

    for i, (img, duration) in enumerate(zip(artist_images, artist_durations_hours)):
        # Calculate the x-position to align the image at the end of the bar
        x_position = duration + (img_width * 35)

        # Create an OffsetImage and AnnotationBbox to display the image at the end of the bar
        img_offset = OffsetImage(img, zoom=img_width, alpha=1)
        img_ab = AnnotationBbox(img_offset, (x_position, i), frameon=False)
        ax.add_artist(img_ab)

    plt.tight_layout()
    plt.show()






def main():
    file_paths = ["StreamingHistory0.json", "StreamingHistory1.json", "StreamingHistory2.json", "StreamingHistoryUpdated.json"]
    #file_paths = ["StreamingHistoryMain0.json", "StreamingHistoryMain1.json"]
    #file_paths = ["StreamingHistory0V2.json", "StreamingHistory1V2.json"]
    #file_paths = ["StreamingHistory0A.json", "StreamingHistory1A.json", "StreamingHistory2A.json"]
    #file_paths = ["StreamingHistory0Z.json", "StreamingHistory1Z.json", "StreamingHistory2Z.json"]
    #file_paths = ["StreamingHistory0D.json", "StreamingHistory1D.json", "StreamingHistory2D.json", "StreamingHistory3D.json", "StreamingHistory4D.json", "StreamingHistory5D.json"]

    image_path = ''

    songs = load_data(file_paths)

    

    while True:
        print("**********************************")
        print("Choose an option:")
        print("1. Show top songs by play count")
        print("2. Show top songs by duration")
        print("3. Show top arists by play count")
        print("4. Show top artists by duration")
        print("5. Display graph of top songs by duration")
        print("6. Display graph of top artists by duration")
        print("7. Search for a song")
        print("8. Search for an artist")
        print("9. Quit")
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
            num_artists = int(input("Enter the number of artists to show: "))
            top_artists_by_play_count(songs, num_artists)
        elif choice == "4":
            num_artists = int(input("Enter the number of artists to show: "))
            top_artists_by_duration(songs, num_artists)
            print(image_path)
        elif choice == "5":
            num_songs = int(input("Enter the number of songs to show: "))
            top_songs = get_top_songs_by_duration(songs, num_songs)
            create_bar_chart(top_songs)
        elif choice == "6":
            num_songs = int(input("Enter the number of songs to show: "))
            top_artists = get_top_artists_by_duration(songs, num_songs)
            create_artist_bar_chart(top_artists)
        elif choice == "7":
            query = input("Enter a search query: ")
            search_for_song(songs, query)
        elif choice == "8":
            query = input("Enter a search query: ")
            image_path = search_for_artist(songs, query)
        elif choice == "9":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
