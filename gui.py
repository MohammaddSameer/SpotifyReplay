#!/usr/bin/env python3

import json
import tkinter as tk
from collections import defaultdict
import spotipy
from spotipy.oauth2 import SpotifyOAuth

root = tk.Tk()

root.geometry("1000x720")
root.title("Spotify Replay")

label = tk.Label(root, text = "Spotify Replay", font = ('Spotify Circular', 30))
label.pack()


root.mainloop()