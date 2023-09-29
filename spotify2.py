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
import tkinter as tk
from tkinter import messagebox, ttk
from functools import partial


scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="df93e00dbc434caab50d3e05cc59386d", client_secret="10237c2063664b94949b7a22c550c3f6",
                                                redirect_uri="http://8080/callback", scope=scope))



user = sp.current_user()
display_name = user["display_name"]
print(f"Logged in as {display_name}")

access_token = sp.auth_manager.get_cached_token()['access_token']


class MusicPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.geometry("800x600")
        

        # Create menu bar
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        # Create file menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open")

        # Create song list
        self.songs = []
        self.song_listbox = tk.Listbox(self.master, width=50, height=20)
        self.song_listbox.pack(pady=20)

        # Create buttons
        top_songs_button = tk.Button(self.master, text="Top Songs by Play Count", command=lambda: self.top_songs_by_play_count(self.songs))
        top_songs_button.pack(side=tk.LEFT, padx=20)

        top_songs_duration_button = tk.Button(self.master, text="Top Songs by Duration", command=self.top_songs_by_duration)
        top_songs_duration_button.pack(side=tk.LEFT, padx=20)

        search_song_button = tk.Button(self.master, text="Search for Song", command=self.search_for_song)
        search_song_button.pack(side=tk.LEFT, padx=20)

        search_artist_button = tk.Button(self.master, text="Search for Artist", command=self.search_for_artist)
        search_artist_button.pack(side=tk.LEFT, padx=20)

    def load_data(self, file_paths):
        songs = {}
        for file_path in file_paths:
            with open(file_path) as f:
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

    def format_duration(self, duration):
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        if hours == 0:
            return f"{minutes} minute{'s' if minutes > 1 else ''}"
        elif minutes == 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours > 1 else ''} and {minutes} minute{'s' if minutes > 1 else ''}"

    def top_songs_by_play_count(self, songs):
        num_songs = int(input("Enter the number of songs to show: "))
        sorted_songs = sorted(songs.items(), key=lambda x: x[1]['play_count'], reverse=True)
        for i, ((artist, track), data) in enumerate(sorted_songs[:num_songs]):
            play_count = data['play_count']
            print(f"{i+1}. {artist} \"{track}\" ({play_count} plays)")
        print()

    def top_songs_by_duration(self, songs, num_songs):
        sorted_songs = sorted(songs.items(), key=lambda x: x[1]['duration'], reverse=True)
        for i, ((artist, track), song_data) in enumerate(sorted_songs[:num_songs]):
            duration = song_data['duration']
            formatted_duration = format_duration(duration)
            play_count = song_data['play_count']
            print(f"{i+1}. {artist} \"{track}\" ({formatted_duration})")
        print()

    def search_for_song(self, songs, query):
        matching_songs = filter(lambda x: query.lower() in x[0][1].lower(), songs.items())
        sorted_songs = sorted(matching_songs, key=lambda x: x[1]['play_count'], reverse=True)
        if not sorted_songs:
            print(f"No song found matching '{query}'")
            return

        for i, ((artist, track), song_data) in enumerate(sorted_songs):
            play_count = song_data['play_count']
            print(f"{i+1}. {artist} \"{track}\" ({play_count} plays)")

    def search_for_artist(self, songs, query):
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

root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
