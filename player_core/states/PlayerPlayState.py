from player_core.states.PlayerStateBase import PlayerStateBase
import soundfile as sf, sounddevice as sd

class PlayerPlayState(PlayerStateBase):
    def __init__(self, _ctx):
        super().__init__(_ctx, "PLAY")

    def execute(self):
        if len(self._ctx["music_queue"]) == 0:
            print("Music queue is empty.")
            return
        
        if self._ctx["stop_playback_event"].is_set():
            self._ctx["stop_playback_event"].clear()

        try:
            self._ctx["current_song"] = self._ctx["music_queue"].pop(0)
            
            data, fs = sf.read(self._ctx["current_song"]['file_path'], dtype='float32')
            self._ctx["current_song_length"] = len(data)
        except Exception as e:
            print('Playback initialization error: {}'.format(e))
            return

        def callback(outdata, frames, time, status):
            if status:
                print(status)
            chunksize = min(len(data) - self._ctx["current_frame"], frames)
            outdata[:chunksize] = data[self._ctx["current_frame"]:self._ctx["current_frame"] + chunksize]
            if chunksize < frames:
                outdata[chunksize:] = 0
                self.skip()
                raise sd.CallbackStop()
            self._ctx["current_frame"] += chunksize

        try:
            stream = sd.OutputStream(
                samplerate=fs, device=sd.default.device, channels=data.shape[1],
                callback=callback, finished_callback=self._ctx["stop_playback_event"].set)
            with stream:
                while not self._ctx["stop_playback_event"].is_set():
                    if not self._ctx["state_queue"].empty():
                        new_state = self._ctx["state_queue"].get()
                        if new_state.get_ID() != "PLAY":
                            self._ctx["state_queue"].put(new_state)
                            break
        except Exception as e:
            print('Playback error: {}'.format(e))
            return
            