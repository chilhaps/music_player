from pydub import AudioSegment
import time, simpleaudio as sa

class Player():
    def __init__(self, music_queue):
        self.music_queue = music_queue

        if self.music_queue:
            self.current_song = self.music_queue.pop(0)
            self.audio_stream = AudioSegment.from_file(self.current_song.get_file_path())
        else:
            self.current_song = None
            self.audio_stream = None

        self.play_index = 0
        self.playback_start = 0
        self.playback_history = []
        self.play_obj = None
        self.is_paused = False
        
    def set_music_queue(self, music_queue):
        self.music_queue = music_queue

    def get_music_queue_length(self):
        return len(self.music_queue)

    def play(self):
        if not self.current_song:
            return

        print("Now Playing:", self.current_song.get_title())

        audio = self.audio_stream[self.playback_start:]
