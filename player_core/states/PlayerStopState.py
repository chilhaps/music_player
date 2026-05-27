from player_core.states.PlayerStateBase import PlayerStateBase

class PlayerStopState(PlayerStateBase):
    def __init__(self, _ctx):
        super().__init__(_ctx, "STOP")

    def execute(self):
        self._ctx["stop_playback_event"].set()
        self._ctx["music_queue"] = []
        self._ctx["current_song"] = None
        self._ctx["current_frame"] = 0
        self._ctx["playback_history"] = []
