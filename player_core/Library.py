from .Song import Song
from tinytag import TinyTag
import sqlite3, os

LIBRARY_DATA_FILENAME = "library_data.db"
SONGS_TABLE_CREATION_QUERY = '''
                                CREATE TABLE IF NOT EXISTS songs (
                                    id INTEGER PRIMARY KEY NOT NULL,
                                    title TEXT,
                                    artist TEXT,
                                    album TEXT,
                                    duration REAL,
                                    file_path TEXT NOT NULL UNIQUE
                                );
                            '''

class Library:
    def __init__(self):
        if not os.path.exists(os.path.join(os.getcwd(), 'db')):
            os.mkdir('db')
            
        self.library_data_path = os.path.join(os.getcwd(), 'db', LIBRARY_DATA_FILENAME)
        self.conn = sqlite3.connect(self.library_data_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute(SONGS_TABLE_CREATION_QUERY)

    def initialize_library(self, library_path=None):
        if not library_path:
            print("No library path provided.")
            return

        file_paths = []

        try:
            for dirpath, _dirnames, filenames in os.walk(library_path, topdown=False):
                file_paths.extend([os.path.join(dirpath, filename) for filename in filenames])
        except Exception as e:
            print(f"Error scanning directory: {e}")

        for file_path in file_paths:
            if not file_path.lower().endswith(TinyTag.SUPPORTED_FILE_EXTENSIONS):
                continue

            try:
                self.add_song(file_path)
            except Exception as e:
                print(f"Error adding song {file_path}: {e}")

    def add_song(self, song_path):
        tag: TinyTag = TinyTag.get(song_path)

        song_obj = Song(tag.title, tag.artist, tag.album, tag.duration, song_path)

        self.cursor.execute("INSERT INTO songs (title, artist, album, duration, file_path) VALUES (?, ?, ?, ?, ?)",
                            (song_obj.get_title(), song_obj.get_artist(), song_obj.get_album(), song_obj.get_duration(), song_obj.get_file_path()))
        self.conn.commit()

    def get_all_songs(self):
        songs = []
        self.cursor.execute("SELECT * FROM songs")
        for i in self.cursor.fetchall():
            song_obj = Song(i[1], i[2], i[3], i[4], i[5])
            songs.append(song_obj)
        return songs
