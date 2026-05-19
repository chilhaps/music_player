from db.Library import Library
from player_core.Player import Player
import time
import os

if __name__ == "__main__":
    test_library_path = r'{}'.format(input('Enter path to music library: ').strip())
    test_library_path = os.path.abspath(test_library_path)

    test_library = Library()

    if Library.get_database_size(test_library) == 0:
        print("Initializing songs table...")
        test_library.initialize_songs_table(test_library_path)

    test_queue = test_library.get_songs_grouped_by_artist()
    
    for artist in test_queue:
        print(list(artist.items())[0][1])

    Player = Player(list(test_queue[0].items())[0][1])
    Player.play()
    time.sleep(100)
    Player.stop()

    print('Test complete.')
