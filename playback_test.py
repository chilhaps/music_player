from player_core.Library import Library
from player_core.Player import Player
import time
import os

if __name__ == "__main__":
    test_library_path = r'{}'.format(input('Enter path to music library: ').strip())
    test_library_path = os.path.abspath(test_library_path)

    test_library = Library()
    test_library.clear_database()
    test_library.initialize_database(test_library_path)
    test_queue = test_library.get_all_songs()
    print('Total songs in library: {}'.format(len(test_queue)))

    player = Player(test_queue)
    player.play()

    while True:
        if player.get_current_song():
            break

    current_track = player.get_current_song()

    print('''Current track info:
          Album: {}
          Album Artist: {}
          Artist: {}
          Disc Number: {}
          Title: {}
          Track Number: {}
          Duration: {}
          File path: {}
          '''.format(
              current_track.get_album(),
              current_track.get_albumartist(),
              current_track.get_artist(),
              current_track.get_disc(),
              current_track.get_title(),
              current_track.get_track(),
              current_track.get_duration(),
              current_track.get_file_path()
          ))
    
    time.sleep(20)

    print('Test complete.')
