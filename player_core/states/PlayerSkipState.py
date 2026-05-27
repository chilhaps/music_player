from player_core.states.PlayerStateBase import PlayerStateBase
import queue

class PlayerSkipState(PlayerStateBase):
    def __init__(self, _ctx):
        super().__init__(_ctx, "SKIP")

    def execute(self):
        self._ctx["stop_playback_event"].set()
        self._ctx["playback_history"].append(self._ctx["current_song"])
        self._ctx["current_song"] = None
        self._ctx["current_frame"] = 0
        self._ctx["state_queue"].put(self.play_state)
