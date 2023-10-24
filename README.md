# Spotify Replay

Spotify Replay is a Python-based application that interacts with the Spotify API and JSON files to provide insights into your listening history on Spotify over the past year.

![SpotifyReplayScreenShot](https://github.com/MohammaddSameer/SpotifyReplay/assets/138824243/80743071-ef3b-4ba0-9368-613c6a0a1c18)

# Getting Started

## Requirements

* Spotify JSON files

* Python 3

* Spotify Developer Account

* spotipy, requests, Pillow, matplotlib, python-dotenv libraries

## Installation

1. **Download Spotify JSON files from your Spotify account:**

![SpotifyReplay_Account](https://github.com/MohammaddSameer/SpotifyReplay/assets/138824243/51559c47-c09d-49ca-941b-75ce94dd6e8f)

![SpotifyReplay_PrivacySettings](https://github.com/MohammaddSameer/SpotifyReplay/assets/138824243/fb6eab5a-e2ac-4fd3-a3ae-20174e07169c)

![SpotifyReplay_DowloadJsonFiles](https://github.com/MohammaddSameer/SpotifyReplay/assets/138824243/ab2d8d40-0842-4aa3-9532-382025f35503)


>May take up to 5 days to recieve JSON files in your email. Program uses JSON files in SpotifyReplay repo as default

2. **Clone Repository**
```bash
git clone https://github.com/MohammaddSameer/SpotifyReplay.git
```



3. **Get API keys**
* [See Guide](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)

* Put in .env file like so:
```bash
client_id_key = <insert client id here>
client_secret_key = <insert client secret here>
```

4. **Install Libraries** 
```bash
pip install -r requirements.txt     
```

## Usage

```bash
python SpotifyReplay.py    
```

# Constraints

* Not enough space to display very long song names
* Graphs are displayed on text based version of program

# Planned Features

* Add button that let's user change color scheme of program

* Implement graphs of song and artist data 




