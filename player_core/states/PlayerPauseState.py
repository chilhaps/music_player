from player_core.states.PlayerStateBase import PlayerStateBase

class PlayerPauseState(PlayerStateBase):
    def __init__(self, _ctx):
        super().__init__(_ctx, "PAUSE")

    def execute(self):
        self._ctx.stop_playback_event.set()
        self._ctx.music_queue.insert(0, self._ctx.current_song)
        self._ctx.current_song = None