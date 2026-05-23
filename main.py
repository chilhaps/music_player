from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import DirectoryTree, Log
from db.Library import Library
from player_core.Player import Player
import time
import os

LIBRARY_PATH = os.path.abspath(r'{}'.format(input('Enter path to music library: ').strip()))

class DirectoryTreeApp(App):
    def __init__(self):
        super().__init__()
        self.library = Library()

        if Library.get_database_size(self.library) == 0:
            self.library.initialize_songs_table(LIBRARY_PATH)

    def compose(self) -> ComposeResult:
        yield HorizontalGroup(DirectoryTree(LIBRARY_PATH), Log())

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        selected_file = f'{event.path}'
        log = self.query_one(Log) 
        log.write_line(f'Selected file: {selected_file}')

        if selected_file.lower().endswith(('.mp3', '.flac', '.ogg', '.wav', '.aac', '.m4a')):
            q = self.library.get_song_by_path(selected_file)
            player = Player(q)
            player.play()
            while not player.get_current_song():
                time.sleep(0.1)  # Wait for the player to initialize the current song
            log = self.query_one(Log) 
            log.write_line(f'Playing: {player.get_current_song()["title"]} by {player.get_current_song()["artist"]}')
        else:
            log = self.query_one(Log) 
            log.write_line('Selected file is not a supported audio format.')

if __name__ == "__main__":
    app = DirectoryTreeApp()
    app.run()
