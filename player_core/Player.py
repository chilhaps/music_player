from pydub import AudioSegment
import simpleaudio as sa, soundfile as sf

class Player():
    def __init__(self, music_queue):
        self.music_queue = music_queue
        self.elapsed = 0
        self.playback_start = 0
        self.playback_history = []
        self.play_obj = None
        self.is_playing = False
        
    def set_music_queue(self, music_queue):
        self.music_queue = music_queue

    def get_music_queue_length(self):
        return len(self.music_queue)

    def play(self):
        if len(self.music_queue) == 0:
            self.is_playing = False
            return
        
        current_song = self.music_queue.pop(0)
        # audio_stream = AudioSegment.from_file(current_song.get_file_path())
        audio_data, sample_rate = sf.read(current_song.get_file_path(), dtype='float32')
        audio_sample_width = 4
        audio_channels = audio_data.shape[1] if len(audio_data.shape) > 1 else 1

        print('Sample Rate: {}, Sample Width: {}, Channels: {}'.format(sample_rate, audio_sample_width, audio_channels))

        print("Now Playing:", current_song.get_title())
        self.is_playing = True

        wave_obj = sa.WaveObject(
            audio_data = audio_data,
            num_channels = audio_channels,
            bytes_per_sample = audio_sample_width,
            sample_rate = sample_rate
        )

        self.play_obj = wave_obj.play()

    def get_play_obj(self):
        return self.play_obj

    def stop(self):
        self.playback_history = []
        self.music_queue = []
        self.elapsed = 0
        self.is_playing = False
        if self.play_obj is not None:
            self.play_obj.stop()

    def get_is_playing(self):
        return self.is_playing
