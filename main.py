import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# os.environ['SPOTIPY_CLIENT_ID'] = 'fe106bbead8c4706aa6dfcc0470cdf9e'
# os.environ['SPOTIPY_CLIENT_SECRET'] = 'fcc5908106f64a2d9990e42ae664360b'
# os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:9000'

# Load environment variables from .env file
load_dotenv()

# Set up the Spotify API client
scope = "playlist-modify-public user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Create a new playlist

playlist_name = "My 170 BPM Playlist"
playlist_description = "A playlist of 100 tracks with a BPM of 170"
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_description)

# Get all tracks in the user's library
results = sp.current_user_saved_tracks()
liked_tracks = results['items']

while results['next']:
    results = sp.next(results)
    liked_tracks.extend(results['items'])

print(f'Found {len(liked_tracks)} liked tracks.\n')

bpm = 170
bpm_tracks = []

for track in liked_tracks:
    try:
        track_info = track['track']
        track_id = track_info['id']
        track_name = track_info['name']
        track_artist = track_info['artists'][0]['name']
        audio_features = sp.audio_features(track_id)[0]
        if audio_features:
            tempo = audio_features['tempo']

        if abs(tempo - bpm) < 3: # Allow for a small margin of error
            print(f"{track_id}: {track_name} - {track_artist}, BPM: {tempo}")
            bpm_tracks.append(track_info['id'])
    except:
        pass


# # Add 100 random tracks with a BPM of 170 to the playlist
print(f'\nFound {len(bpm_tracks)} bpm tracks.')
random_tracks = random.sample(bpm_tracks, min(len(bpm_tracks), 100))
sp.playlist_add_items(playlist['id'], random_tracks)

print(f'\nAdded tracks to {playlist_name}.')
