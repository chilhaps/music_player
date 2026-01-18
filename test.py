from player_core.Song import Song
from player_core.Library import Library
from player_core.Player import Player
from tinytag import TinyTag
import os

if __name__ == "__main__":
    test_filepath = r'{}'.format(input('Enter path to audio file: ').strip())
    test_filepath = os.path.abspath(test_filepath)

    tag: TinyTag = TinyTag.get(test_filepath)

    test_song = Song(tag.title, tag.artist, tag.album, tag.duration, test_filepath)
    test_library = Library()
    test_library.add_song(test_song)

    print('Attempting to play {} by {}'.format(test_song.get_title(), test_song.get_artist()))

    player = Player(test_library.get_songs())

    player.play()
    
    print('Test complete.')
