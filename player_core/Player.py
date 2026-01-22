import threading, queue, soundfile as sf, sounddevice as sd

class Player():
    def __init__(self, music_queue):
        self.music_queue = music_queue
        self.current_song = None
        self.current_frame = 0
        self.playback_history = []
        self.stop_playback_event = threading.Event()
        self.command_queue = queue.Queue()

        def stop_action():
            self.stop_playback_event.set()
            self.music_queue = []
            self.current_song = None
            self.current_frame = 0
            self.playback_history = []

        def pause_action():
            self.stop_playback_event.set()
            self.music_queue.insert(0, self.current_song)
            self.current_song = None
        
        def play_action():
            if not self.music_queue:
                print("Music queue is empty.")
                return
            
            if self.stop_playback_event.is_set():
                self.stop_playback_event.clear()

            self.current_song = self.music_queue.pop(0)
            audio_data, sample_rate = sf.read(self.current_song.get_file_path(), dtype='float32')
            data, fs = audio_data, sample_rate

            def callback(outdata, frames, time, status):
                if status:
                    print(status)
                chunksize = min(len(data) - self.current_frame, frames)
                outdata[:chunksize] = data[self.current_frame:self.current_frame + chunksize]
                if chunksize < frames:
                    outdata[chunksize:] = 0
                    raise sd.CallbackStop()
                self.current_frame += chunksize

            stream = sd.OutputStream(
                samplerate=fs, device=sd.default.device, channels=data.shape[1],
                callback=callback, finished_callback=self.stop_playback_event.set)
            with stream:
                while not self.stop_playback_event.is_set():
                    if not self.command_queue.empty():
                        user_command = self.command_queue.get()
                        print(f"Received command: {user_command}")
                    else:
                        user_command = None
                    
                    if user_command == 'PLAY':
                        sd.sleep(100)
                    elif user_command == 'STOP':
                        stop_action()
                    elif user_command == 'PAUSE':
                        pause_action()

        def playback():
            while True:
                if not self.command_queue.empty():
                    user_command = self.command_queue.get()
                    print(f"Received command: {user_command}")
                else:
                    user_command = None

                if user_command == 'PLAY':
                    play_action()
                elif user_command == 'STOP':
                    stop_action()
                elif user_command == 'PAUSE':
                    pause_action()

        self.playback_thread = threading.Thread(target=playback)
        self.playback_thread.daemon = True
        self.playback_thread.start()

    def play(self):
        self.command_queue.put('PLAY')

    def stop(self):
        self.command_queue.put('STOP')

    def pause(self):
        self.command_queue.put('PAUSE')
    
    def get_current_song(self):
        return self.current_song
