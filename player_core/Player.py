import threading, queue, soundfile as sf, sounddevice as sd

PREVIOUS_VS_RESTART_THRESHOLD = 0.03

class Command():
    def __init__(self, ID_str = None, func = None):
        self.ID_str = ID_str
        self.func = func

    def get_ID(self):
        return self.ID_str
    
    def get_func(self):
        return self.func

class Player():
    def __init__(self, music_queue):
        # Initialize playback variables
        self.music_queue = music_queue
        self.current_song = None
        self.current_frame = 0
        self.current_song_length = 0
        self.playback_history = []

        # Initialize event and queue objects
        self.stop_playback_event = threading.Event()
        self.command_queue = queue.Queue()

        # Initialize command and command map objects
        self.play_command = Command()
        self.pause_command = Command()
        self.stop_command = Command()
        self.skip_command = Command()
        self.prev_command = Command()
        self.command_map = {}
        
        def play_action():
            # Called when PLAY command is detected
            if not self.music_queue:
                print("Music queue is empty.")
                return
            
            if self.stop_playback_event.is_set():
                self.stop_playback_event.clear()

            self.current_song = self.music_queue.pop(0)
            audio_data, sample_rate = sf.read(self.current_song.get_file_path(), dtype='float32')
            self.current_song_length = len(audio_data)
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
                    
                    if user_command == self.play_command.get_ID():
                        sd.sleep(100)
                    elif user_command in self.command_map:
                        self.command_map[user_command]()

        def pause_action():
            # Called when PAUSE command is detected
            self.stop_playback_event.set()
            self.music_queue.insert(0, self.current_song)
            self.current_song = None

        def stop_action():
            # Called when STOP command is detected
            self.stop_playback_event.set()
            self.music_queue = []
            self.current_song = None
            self.current_frame = 0
            self.playback_history = []

        def skip_action():
            # Called when SKIP command is detected
            self.stop_playback_event.set()
            self.playback_history.append(self.current_song)
            self.current_song = None
            self.current_frame = 0
            self.command_queue.put(self.play_command.get_ID())

        def prev_action():
            playback_progress = self.current_frame / self.current_song_length
            print('Playback progress: {}'.format(playback_progress))
            
            if len(self.playback_history) == 0 or playback_progress > PREVIOUS_VS_RESTART_THRESHOLD:
                print('Restarting current song.')
                self.stop_playback_event.set()
                self.music_queue.insert(0, self.current_song)
                self.current_song = None
                self.current_frame = 0
                self.command_queue.put(self.play_command.get_ID())
            else:
                print('Playing previous song.')
                self.stop_playback_event.set()
                self.music_queue.insert(0, self.playback_history.pop())
                self.current_song = None
                self.current_frame = 0
                self.command_queue.put(self.play_command.get_ID())


        def handle_commands():
            # Define commands
            self.play_command = Command('PLAY', play_action)
            self.pause_command = Command('PAUSE', pause_action)
            self.stop_command = Command('STOP', stop_action)
            self.skip_command = Command('SKIP', skip_action)
            self.prev_command = Command('PREV', prev_action)

            # Map command IDs to action functions
            self.command_map = {
                self.play_command.get_ID(): self.play_command.get_func(),
                self.pause_command.get_ID(): self.pause_command.get_func(),
                self.stop_command.get_ID(): self.stop_command.get_func(),
                self.skip_command.get_ID():self.skip_command.get_func(),
                self.prev_command.get_ID():self.prev_command.get_func()
            }

            # Handle queued commands
            while True:
                if not self.command_queue.empty():
                    user_command = self.command_queue.get()
                    print(f"Received command: {user_command}")
                else:
                    user_command = None

                if user_command in self.command_map:
                    self.command_map[user_command]()
                elif user_command:
                    print('Invalid command: {}'.format(user_command))
                else:
                    pass

        # Start command handler thread
        self.handler_thread = threading.Thread(target=handle_commands)
        self.handler_thread.daemon = True
        self.handler_thread.start()

    # Define methods to push each command ID to queue
    def play(self):
        self.command_queue.put(self.play_command.get_ID())

    def stop(self):
        self.command_queue.put(self.stop_command.get_ID())

    def pause(self):
        self.command_queue.put(self.pause_command.get_ID())

    def skip(self):
        self.command_queue.put(self.skip_command.get_ID())

    def previous(self):
        self.command_queue.put(self.prev_command.get_ID())
    
    # Getters
    def get_current_song(self):
        return self.current_song
