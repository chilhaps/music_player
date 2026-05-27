from player_core.states.PlayerPauseState import PlayerPauseState
from player_core.states.PlayerPlayState import PlayerPlayState
from player_core.states.PlayerStopState import PlayerStopState
from player_core.states.PlayerSkipState import PlayerSkipState
from player_core.states.PlayerPrevState import PlayerPrevState
import threading, queue

PREVIOUS_VS_RESTART_THRESHOLD = 0.03
MAX_TRIES = 3

class Player():
    def __init__(self, music_queue=[]):
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

        self.context = {
            "previous_vs_restart_threshold": PREVIOUS_VS_RESTART_THRESHOLD,
            "max_tries": MAX_TRIES,
            "music_queue": self.music_queue,
            "current_song": self.current_song,
            "current_frame": self.current_frame,
            "current_song_length": self.current_song_length,
            "playback_history": self.playback_history,
            "error_count": self.error_count,
            "stop_playback_event": self.stop_playback_event,
            "state_queue": self.state_queue
        }

        self.play_state = PlayerPlayState(self.context)
        self.pause_state = PlayerPauseState(self.context)
        self.stop_state = PlayerStopState(self.context)
        self.skip_state = PlayerSkipState(self.context)
        self.prev_state = PlayerPrevState(self.context)

        self.current_state = None

        def handle_queued_states():
            # Handle queued states
            while True:
                if not self.state_queue.empty():
                    self.current_state = self.state_queue.get()
                    print(f"Entering state: {self.current_state.get_ID()}")
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
        return self.context["current_song"]
