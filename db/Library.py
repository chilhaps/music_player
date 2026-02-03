from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from db.models import Song, Base
from tinytag import TinyTag
import os

DATABASE_URL = 'sqlite:///library.db'

class Library:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)

    def initialize_songs_table(self, library_path=None):
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

        new_song = Song(album=tag.album,
                        albumartist=tag.albumartist,
                        artist=tag.artist,
                        disc=tag.disc,
                        title=tag.title,
                        track=tag.track,
                        duration=tag.duration,
                        file_path=song_path)
        
        session = Session(bind=self.engine)
        session.add(new_song)
        session.commit()
        session.close()

    def get_all_songs(self):
        session = Session(bind=self.engine)
        results = session.query(Song).all()
        result_dicts = [{column.name: getattr(row, column.name) for column in Song.__table__.columns} for row in results]
        return result_dicts
    
    '''
    def clear_database(self):
        self.cursor.execute(CLEAR_SONGS_TABLE_QUERY)
        self.conn.commit()

    def get_remaining_songs_from_album(self, album_name='', starting_track_number=0):
        songs = []
        self.cursor.execute(SELECT_REMAINING_TRACKS_IN_ALBUM_QUERY.format(album_name, starting_track_number))
        for i in self.cursor.fetchall():
            song_obj = Song(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            songs.append(song_obj)
        return songs
    '''
    