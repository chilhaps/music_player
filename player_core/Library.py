from .Song import Song
import json, os

LIBRARY_DATA_FILENAME = "library_data.json"

class Library:
    def __init__(self):
        self.songs = []

        if os.path.exists(os.path.join(os.getcwd(), LIBRARY_DATA_FILENAME)):
            self.load_library()

    def load_library(self):
        try:
            with open(os.path.join(os.getcwd(), LIBRARY_DATA_FILENAME), 'r') as f:
                data = json.load(f)
                for song_data in data:
                    song = Song(
                        title=song_data['title'],
                        artist=song_data['artist'],
                        album=song_data['album'],
                        duration=song_data['duration'],
                        file_path=song_data['file_path']
                    )
                    self.songs.append(song)
        except FileNotFoundError:
            self.songs = []
    
    def save_library(self):
        data = []
        for song in self.songs:
            song_data = {
                'title': song.get_title(),
                'artist': song.get_artist(),
                'album': song.get_album(),
                'duration': song.get_duration(),
                'file_path': song.get_file_path()
            }
            data.append(song_data)
        
        with open(os.path.join(os.getcwd(), LIBRARY_DATA_FILENAME), 'w') as f:
            json.dump(data, f, indent=4)

    def add_song(self, song):
        self.songs.append(song)

    def get_songs(self):
        return self.songs
