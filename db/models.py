from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    album = Column(String(100), nullable=False)
    albumartist = Column(String(100), nullable=False)
    artist = Column(String(100), nullable=False)
    disc = Column(Integer)
    title = Column(String(100), nullable=False)
    track = Column(Integer)
    duration = Column(String(100))
    file_path = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        print('"{}" from the album {}, by {}')
