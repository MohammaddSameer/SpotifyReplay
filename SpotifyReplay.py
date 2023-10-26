#!/usr/bin/env python3


from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, filedialog
import json
from collections import defaultdict
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
from dotenv import load_dotenv


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

load_dotenv()
client_id_key = os.getenv("client_id_key")
secret_key = os.getenv("client_secret_key")




scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= client_id_key, client_secret= secret_key,
                                                redirect_uri="http://8080/callback", scope=scope))



user = sp.current_user()
display_name = user["display_name"]
print(f"Logged in as {display_name}")

access_token = sp.auth_manager.get_cached_token()['access_token']






def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select Spotify listening history JSON files",
        filetypes=[("JSON files", "*.json")]
    )
    return file_paths



def load_data():
    global songs
    file_paths = select_files()

    songs = {}
    for file_path in file_paths:
        with open(file_path, encoding='utf-8') as f:
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




def load_data_default(file_path):
    songs = {}
    for file_path in file_paths:
        with open(file_path, encoding='utf-8') as f:
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
    top_songs_text = ""
    for i, ((artist, track), data) in enumerate(sorted_songs[:num_songs]):
        play_count = data['play_count']
        top_songs_text += f"{i+1}. {artist} \"{track}\" ({play_count} plays)\n"

    return top_songs_text







def top_songs_by_duration(songs, num_songs):
    sorted_songs = sorted(songs.items(), key=lambda x: x[1]['duration'], reverse=True)
    top_songs_text = ""
    for i, ((artist, track), song_data) in enumerate(sorted_songs[:num_songs]):
        duration = song_data['duration']
        formatted_duration = format_duration(duration)
        top_songs_text += (f"{i+1}. {artist} \"{track}\" ({formatted_duration})\n")

    return top_songs_text






def top_artists_by_duration(songs, num_artists):
    artist_durations = defaultdict(float)

    # Calculate total listening duration for each artist
    for (artist, _), song_data in songs.items():
        artist_durations[artist] += song_data['duration']

    # Sort artists by total listening duration
    sorted_artists = sorted(artist_durations.items(), key=lambda x: x[1], reverse=True)
    top_artist_text = ""

    # Display the top artists
    for i, (artist, duration) in enumerate(sorted_artists[:num_artists]):
        formatted_duration = format_duration(duration)
        top_artist_text += (f"{i+1}. {artist} ({formatted_duration})\n")
    return top_artist_text





def top_artists_by_play_count(songs, num_artists):
    artist_play_counts = defaultdict(int)

    # Count the number of times each artist appears in the listening history
    for (artist, _), song_data in songs.items():
        artist_play_counts[artist] += song_data['play_count']

    # Sort artists by play count
    sorted_artists = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)
    top_artist_text = ""

    # Display the top artists
    for i, (artist, play_count) in enumerate(sorted_artists[:num_artists]):
        top_artist_text += (f"{i+1}. {artist} ({play_count} plays)\n")
    return top_artist_text


   



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



def search_for_song(songs, query):
    matching_songs = filter(lambda x: query.lower() in x[0][1].lower(), songs.items())
    sorted_songs = sorted(matching_songs, key=lambda x: x[1]['play_count'], reverse=True)
    
    if not sorted_songs:
        return(f"No song found matching '{query}'")
    

    search_results = ''

    for i, ((artist, track), song_data) in enumerate(sorted_songs):
        play_count = song_data['play_count']
        search_results += (f"{i+1}. {artist} \"{track}\" ({play_count} plays)\n")

    return search_results

    # while True:
    #     song_num = input("Enter the number of the song you want to view, or 'q' to quit: ")
    #     if song_num == 'q':
    #         break
    #     try:
    #         song_num = int(song_num)
    #         if song_num < 1 or song_num > len(sorted_songs):
    #             raise ValueError
    #     except ValueError:
    #         print("Invalid input, please enter a valid song number or 'q' to quit.")
    #         continue

    #     (artist_name, song_name), song_data = sorted_songs[song_num - 1]
    #     play_count = song_data['play_count']
    #     print(f"Song: \"{song_name}\" by {artist_name}")
    #     print(f"Play Count: {play_count} plays")
    #     break



    

def search_for_artist(songs, query):
    matching_songs = filter(lambda x: query.lower() in x[0][0].lower(), songs.items())
    artist_play_counts = defaultdict(int)
    for (artist, track), data in matching_songs:
        artist_play_counts[artist] += data['play_count']
    sorted_artists = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)
    if not sorted_artists:
        return(f"No artist found matching '{query}'")
    
    artists_results = ''
    for i, (artist, play_count) in enumerate(sorted_artists):
        artists_results += (f"{i+1}. {artist} ({play_count} plays)\n")
    return artists_results

    # while True:
    #     artist_num = input("Enter the number of the artist you want to view, or 'q' to quit: ")
    #     if artist_num == 'q':
    #         break
    #     try:
    #         artist_num = int(artist_num)
    #         if artist_num < 1 or artist_num > len(sorted_artists):
    #             raise ValueError
    #     except ValueError:
    #         print("Invalid input, please enter a valid artist number or 'q' to quit.")
    #         continue

    #     artist_name, _ = sorted_artists[artist_num - 1]

    #     matching_songs = filter(lambda x: x[0][0] == artist_name, songs.items())
    #     sorted_songs = sorted(matching_songs, key=lambda x: x[1]['play_count'], reverse=True)
    #     for i, ((_, track), data) in enumerate(sorted_songs):
    #         play_count = data['play_count']
    #         print(f"{i+1}. \"{track}\" ({play_count} plays)")
    #     break







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





def make_label_top_songs_play_count():

    top_songs_text = top_songs_by_play_count(songs, 10)


    label = Canvas(window, bg="#6C02BB", width=1500, height=1000, borderwidth=0, highlightthickness=0)
    label.place(x=370, y=150)


    y = 20  # Initial y-coordinate
    line_spacing = 75 # Adjust this value to control vertical spacing

    for line in top_songs_text.split('\n'):
        label.create_text(10, y, anchor="w", text=line, fill="#F4FE46", font=("CircularStd-Medium", 20), justify="left")
        y += line_spacing





def make_label_top_songs_time_played():

    top_songs_text = top_songs_by_duration(songs, 10)

    label = Canvas(window, bg="#6C02BB", width=1500, height=1000, borderwidth=0, highlightthickness=0)
    label.place(x=370, y=150)

    y = 20  # Initial y-coordinate
    line_spacing = 75 # Adjust this value to control vertical spacing

    for line in top_songs_text.split('\n'):
        label.create_text(10, y, anchor="w", text=line, fill="#F4FE46", font=("CircularStd-Medium", 20), justify="left")
        y += line_spacing



def make_label_top_artists_play_count():

    top_artists_text = top_artists_by_play_count(songs, 10)

    # global label
    label = Canvas(window, bg="#6C02BB", width=1500, height=1000, borderwidth=0, highlightthickness=0)
    label.place(x=370, y=150)

    y = 20  # Initial y-coordinate
    line_spacing = 75 # Adjust this value to control vertical spacing

    for line in top_artists_text.split('\n'):
        label.create_text(10, y, anchor="w", text=line, fill="#F4FE46", font=("CircularStd-Medium", 35), justify="left")
        y += line_spacing



def make_label_top_artists_time_played():

    top_artists_text = top_artists_by_duration(songs, 10)

    # global label
    label = Canvas(window, bg="#6C02BB", width=1500, height=1000, borderwidth=0, highlightthickness=0)
    label.place(x=370, y=150)

    y = 20  # Initial y-coordinate
    line_spacing = 75 # Adjust this value to control vertical spacing

    for line in top_artists_text.split('\n'):
        label.create_text(10, y, anchor="w", text=line, fill="#F4FE46", font=("CircularStd-Medium", 35), justify="left")
        y += line_spacing

    


def make_label_search_song():

    def on_enter_pressed(event):
        query = entry_1.get()
        entry_1.delete(0, 'end')
        search_results = search_for_song(songs, query)

        label = Canvas(window, bg="#6C02BB", width=1500, height=1000, borderwidth=0, highlightthickness=0)
        label.place(x=370, y=300)

        y = 20  # Initial y-coordinate
        line_spacing = 75 # Adjust this value to control vertical spacing

        for line in search_results.split('\n'):
            label.create_text(10, y, anchor="w", text=line, fill="#F4FE46", font=("CircularStd-Medium", 20), justify="left")
            y += line_spacing


    label = Canvas(window, bg="#6C02BB", width=1500, height=1000, borderwidth=0, highlightthickness=0)
    label.place(x=370, y=150)
    label.create_text(10.0, 40.0, anchor="w", text="Enter a Song Name:  ", fill="#F4FE46", font=("CircularStd-Medium", 45))

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(1159.5,511.5,image=entry_image_1)
    entry_1 = Entry(bd=0, bg="#7F05D9", fg="#F9F9F9",highlightthickness=0, font=("CircularStd-Medium", 35))
    entry_1.place(x=950.0, y=150.0, width=419.0, height=81.0)

    entry_1.bind('<Return>', on_enter_pressed)




def make_label_search_artist():

    def on_enter_pressed(event):
        query = entry_1.get()
        entry_1.delete(0, 'end')
        search_results = search_for_artist(songs, query)

        label = Canvas(window, bg="#6C02BB", width=1500, height=1000, borderwidth=0, highlightthickness=0)
        label.place(x=370, y=300)

        y = 20  # Initial y-coordinate
        line_spacing = 75 # Adjust this value to control vertical spacing

        for line in search_results.split('\n'):
            label.create_text(10, y, anchor="w", text=line, fill="#F4FE46", font=("CircularStd-Medium", 20), justify="left")
            y += line_spacing



    label = Canvas(window, bg="#6C02BB", width=1500, height=1000, borderwidth=0, highlightthickness=0)
    label.place(x=370, y=150)
    label.create_text(10.0, 40.0, anchor="w", text="Enter an Artist Name:  ", fill="#F4FE46", font=("CircularStd-Medium", 45))

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(1159.5,511.5,image=entry_image_1)
    entry_1 = Entry(bd=0, bg="#7F05D9", fg="#F9F9F9",highlightthickness=0, font=("CircularStd-Medium", 35))
    entry_1.place(x=980.0, y=150.0, width=419.0, height=81.0)

    entry_1.bind('<Return>', on_enter_pressed)






file_paths = ["StreamingHistory0.json", "StreamingHistory1.json", "StreamingHistory2.json"]

songs = load_data_default(file_paths)



window = Tk()

window.geometry("1440x1024")
window.configure(bg = "#6C02BB")


canvas = Canvas(window,bg = "#6C02BB", height = 1024, width = 1440, bd = 0,highlightthickness = 0, relief = "ridge")

canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0, 0.0, 362.0, 1024.0, fill="#7E04D8",outline="")



button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=make_label_search_song, relief="flat")
button_1.place(x=26.0, y=756.0, width=309.0, height=92.0)


button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=make_label_search_artist, relief="flat")
button_2.place(x=26.0, y=614.0, width=309.0, height=92.0)


button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=button_image_3, borderwidth=0, highlightthickness=0, command= make_label_top_artists_play_count,relief="flat")
button_3.place(x=26.0, y=330.0, width=309.0, height=92.0)


button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=button_image_4, borderwidth=0, highlightthickness=0, command= make_label_top_songs_time_played, relief="flat")
button_4.place(x=26.0, y=188.0, width=309.0, height=92.0)


button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(image=button_image_5, borderwidth=0, highlightthickness=0, command= make_label_top_songs_play_count, relief="flat")
button_5.place(x=26.0, y=46.0, width=309.0,height=92.0)


button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(image=button_image_6, borderwidth=0, highlightthickness=0, command=make_label_top_artists_time_played,relief="flat")
button_6.place(x=26.0, y=472.0, width=309.0, height=92.0)



button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
button_8 = Button(image=button_image_8,borderwidth=0, highlightthickness=0, command= load_data, relief="flat")
button_8.place(x=252.0, y=866.0, width=77.0, height=77.0)


canvas.create_text(1030.0, 37.0, anchor="nw", text="Spotify Replay", fill="#F9F9F9",font=("CircularStd-Medium", 40))


window.resizable(True, True)
window.mainloop()
