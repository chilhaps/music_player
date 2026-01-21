import threading, queue, soundfile as sf, sounddevice as sd

current_frame = 0

class Player():
    def __init__(self, music_queue):
        self.music_queue = music_queue
        self.current_song = None
        self.playback_history = []
        self.stop_event = threading.Event()
        self.command_queue = queue.Queue()

        def playback(q, stop_event):
            while not stop_event.is_set():
                user_command = q.get(block=True, timeout=0.1)

                if user_command == 'PLAY':
                    if len(self.music_queue) == 0:
                        return
                    
                    self.current_song = self.music_queue.pop(0)

                    audio_data, sample_rate = sf.read(self.current_song.get_file_path(), dtype='float32')
                    audio_sample_width = 4
                    audio_channels = audio_data.shape[1]

                    print('Sample Rate: {}, Sample Width: {}, Channels: {}'.format(sample_rate, audio_sample_width, audio_channels))

                    data, fs = audio_data, sample_rate

                    def callback(outdata, frames, time, status):
                        global current_frame
                        if status:
                            print(status)
                        chunksize = min(len(data) - current_frame, frames)
                        outdata[:chunksize] = data[current_frame:current_frame + chunksize]
                        if chunksize < frames:
                            outdata[chunksize:] = 0
                            raise sd.CallbackStop()
                        current_frame += chunksize

                    stream = sd.OutputStream(
                        samplerate=fs, device=sd.default.device, channels=data.shape[1],
                        callback=callback, finished_callback=self.stop_event.set)
                    with stream:
                        print('Playback progress: {}'.format(current_frame))
                elif user_command == 'STOP':
                    self.stop_event.set()

        self.playback_thread = threading.Thread(target=playback, args=(self.command_queue, self.stop_event))
        # self.playback_thread.daemon = True
        self.playback_thread.start()

    def play(self):
        self.command_queue.put('PLAY')

    def stop(self):
        self.command_queue.put('STOP')
    
    def get_current_song(self):
        return self.current_song
