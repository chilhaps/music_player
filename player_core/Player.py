from player_core.states import PlayerPlayState, PlayerPauseState, PlayerStopState, PlayerSkipState, PlayerPrevState
import threading, queue, soundfile as sf, sounddevice as sd

PREVIOUS_VS_RESTART_THRESHOLD = 0.03
MAX_TRIES = 3

class Player():
    def __init__(self, music_queue=None):
        # Initialize playback variables
        self.music_queue = music_queue
        self.current_song = None
        self.current_frame = 0
        self.current_song_length = 0
        self.playback_history = []
        self.error_count = 0

        # Initialize event and queue objects
        self.stop_playback_event = threading.Event()
        self.state_queue = queue.Queue()

        self.play_state = PlayerPlayState(self)
        self.pause_state = PlayerPauseState(self)
        self.stop_state = PlayerStopState(self)
        self.skip_state = PlayerSkipState(self)
        self.prev_state = PlayerPrevState(self)

        self.current_state = None
        
        def play_action():
            # Called when PLAY command is detected
            if not self.music_queue:
                print("Music queue is empty.")
                return
            
            if self.stop_playback_event.is_set():
                self.stop_playback_event.clear()

            try:
                self.current_song = self.music_queue.pop(0)

                if not self.current_song:
                    print("Music queue is empty.")
                    return
                
                audio_data, sample_rate = sf.read(self.current_song['file_path'], dtype='float32')
                self.current_song_length = len(audio_data)
                data, fs = audio_data, sample_rate
            except Exception as e:
                print('Playback initialization error: {}'.format(e))
                return

            def callback(outdata, frames, time, status):
                if status:
                    print(status)
                chunksize = min(len(data) - self.current_frame, frames)
                outdata[:chunksize] = data[self.current_frame:self.current_frame + chunksize]
                if chunksize < frames:
                    outdata[chunksize:] = 0
                    self.skip()
                    raise sd.CallbackStop()
                self.current_frame += chunksize

            try:
                stream = sd.OutputStream(
                    samplerate=fs, device=sd.default.device, channels=data.shape[1],
                    callback=callback, finished_callback=self.stop_playback_event.set)
                with stream:
                    while not self.stop_playback_event.is_set():
                        if not self.state_queue.empty():
                            self.current_state = self.state_queue.get()
                            print(f"Received state: {self.current_state.get_ID()}")
                        else:
                            self.current_state = None
                            continue
                        
                        if self.error_count != 0: self.error_count = 0

                        try:
                            if self.current_state is not None and self.current_state.get_ID() != "PLAY":
                                self.current_state.execute()
                        except Exception as e:
                            print(f"Error executing state {self.current_state.get_ID()}: {e}")
            except Exception as e:
                print('Playback error: {}'.format(e))

                if self.error_count < MAX_TRIES:
                    print('Attempting to reinitialize playback...')
                    self.error_count += 1
                    self.command_queue.put(self.play_command.get_ID())
                    self.stop_playback_event.set()
                    self.music_queue.insert(0, self.current_song)
                    self.current_song = None
                    self.play()
                else:
                    print('Max attampts reached, stopping playback...')
                    self.stop()

                return

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
            self.play()

        def prev_action():
            playback_progress = self.current_frame / self.current_song_length
            print('Playback progress: {}'.format(playback_progress))
            
            if len(self.playback_history) == 0 or playback_progress > PREVIOUS_VS_RESTART_THRESHOLD:
                print('Restarting current song.')
                self.stop_playback_event.set()
                self.music_queue.insert(0, self.current_song)
                self.current_song = None
                self.current_frame = 0
                self.play()
            else:
                print('Playing previous song.')
                self.stop_playback_event.set()
                self.music_queue.insert(0, self.playback_history.pop())
                self.current_song = None
                self.current_frame = 0
                self.play()


        def handle_queued_states():
            # Handle queued states
            while True:
                if not self.state_queue.empty():
                    self.current_state = self.state_queue.get()
                    print(f"Received state: {self.current_state.get_ID()}")
                else:
                    self.current_state = None
                    continue

                try:
                    self.current_state.execute()
                except Exception as e:
                    print(f"Error executing state {self.current_state.get_ID()}: {e}")

        # Start state handler thread
        self.handler_thread = threading.Thread(target=handle_queued_states)
        self.handler_thread.daemon = True
        self.handler_thread.start()

    # Define methods to push each state to queue
    def play(self):
        self.state_queue.put(self.play_state)

    def stop(self):
        self.state_queue.put(self.stop_state)

    def pause(self):
        self.state_queue.put(self.pause_state)

    def skip(self):
        self.state_queue.put(self.skip_state)

    def previous(self):
        self.state_queue.put(self.prev_state)

    def enqueue_songs(songs):
        for song in songs:
            self.music_queue.append(song)
    
    def get_current_song(self):
        return self.current_song
