from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from db.models import Song, Base
from tinytag import TinyTag
import os
import sqlalchemy as sa

DATABASE_URL = 'sqlite:///library.db'

class Library:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)

        self.initialized = False

    def is_initialized(self):
        return self.initialized

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

        self.initialized = True

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
        results = session.scalars(sa.select(Song).order_by(Song.track)).all()
        result_dicts = [{column.name: getattr(row, column.name) for column in Song.__table__.columns} for row in results]
        return result_dicts

    def get_songs_grouped_by_artist(self):
        session = Session(bind=self.engine)
        artist_groups = session.query(Song.albumartist).order_by(Song.albumartist).distinct().all()
        result_dicts = []
        for artist in artist_groups:
            songs = session.query(Song).filter(Song.albumartist == artist[0]).order_by(Song.album, Song.track).all()
            song_dicts = [{column.name: getattr(song, column.name) for column in Song.__table__.columns} for song in songs]
            result_dicts.append({artist[0]: song_dicts})
            
        #result_dicts = [{column.name: getattr(row, column.name) for column in Song.__table__.columns} for row in results]
        return result_dicts

    def get_database_size(self):
        session = Session(bind=self.engine)
        count = session.query(Song).count()
        session.close()
        return count
    
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
    