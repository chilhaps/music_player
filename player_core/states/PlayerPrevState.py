from player_core.states.PlayerStateBase import PlayerStateBase

class PlayerPrevState(PlayerStateBase):
    def __init__(self, _ctx):
        super().__init__(_ctx, "PREV")

    def execute(self):
        playback_progress = self._ctx.current_frame / self._ctx.current_song_length
        print('Playback progress: {}'.format(playback_progress))
        
        if len(self._ctx.playback_history) == 0 or playback_progress > self._ctx.PREVIOUS_VS_RESTART_THRESHOLD:
            print('Restarting current song.')
            self._ctx.stop_playback_event.set()
            self._ctx.music_queue.insert(0, self._ctx.current_song)
            self._ctx.current_song = None
            self._ctx.current_frame = 0
            self._ctx.play()
        else:
            print('Playing previous song.')
            self._ctx.stop_playback_event.set()
            self._ctx.music_queue.insert(0, self._ctx.playback_history.pop())
            self._ctx.current_song = None
            self._ctx.current_frame = 0
            self._ctx.play()