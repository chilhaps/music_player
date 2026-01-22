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

    print('Now Playing: {} by {}'.format(player.get_current_song().get_title(), player.get_current_song().get_artist()))
    
    time.sleep(5)
    player.pause()
    time.sleep(5)
    player.play()
    time.sleep(5)
    player.previous()
    time.sleep(5)
    player.skip()
    time.sleep(5)
    player.previous()
    time.sleep(10)
    player.previous()
    time.sleep(5)
    player.stop()
    time.sleep(5)
    player.play()
    time.sleep(5)

    print('Test complete.')
