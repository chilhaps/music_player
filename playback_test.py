from db.Library import Library
from player_core.Player import Player
import time
import os

if __name__ == "__main__":
    test_library_path = r'{}'.format(input('Enter path to music library: ').strip())
    test_library_path = os.path.abspath(test_library_path)

    test_library = Library()
    test_library.initialize_songs_table(test_library_path)
    test_queue = test_library.get_all_songs()
    print('Total songs in library: {}'.format(len(test_queue)))

    queue_length = 0
    for song in test_queue:
        queue_length += float(song['duration'])

    player = Player(test_queue)
    player.play()

    while True:
        if player.get_current_song():
            break

    current_track = player.get_current_song()

    print('Now playing "{}" from "{}" by {}'.format(current_track['title'], current_track['album'], current_track['albumartist']))
    
    time.sleep(queue_length)

    print('Test complete.')
