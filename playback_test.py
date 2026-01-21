from player_core.Library import Library
from player_core.Player import Player
import time
import os

if __name__ == "__main__":
    test_library_path = r'{}'.format(input('Enter path to music library: ').strip())
    test_library_path = os.path.abspath(test_library_path)

    test_library = Library()
    test_library.initialize_library(test_library_path)
    test_queue = test_library.get_all_songs()
    print('Total songs in library: {}'.format(len(test_queue)))

    player = Player(test_queue)
    player.play()
    #print('Now Playing: {} by {}'.format(player.get_current_song().get_title(), player.get_current_song().get_artist()))
    time.sleep(20)
    player.stop()
    print('Test complete.')
