# Spotify Replay

Spotify Replay is a Python-based application that interacts with the Spotify API and JSON files to provide insights into your listening history on Spotify over the past year.

![Desktop - 15](https://github.com/MohammaddSameer/SpotifyReplay/assets/138824243/461ce666-7506-44ad-a547-3b29dc2f2e66)

![SpotifyReplayGraph](https://github.com/MohammaddSameer/SpotifyReplay/assets/138824243/5d4617df-c535-4d91-87ff-76a6a42d1ae3)



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
python3 SpotifyReplay.py    
```

# Constraints

* Not enough space to display very long song names
* Graphs are displayed on text based version of program

# Planned Features

* Add button that let's user change color scheme of program

* Implement graphs of song and artist data 




