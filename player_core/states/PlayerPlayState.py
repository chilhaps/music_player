from player_core.states.PlayerStateBase import PlayerStateBase

class PlayerPlayState(PlayerStateBase):
    def __init__(self, _ctx):
        super().__init__(_ctx, "PLAY")

    def execute(self):
        if not self._ctx.music_queue:
            print("Music queue is empty.")
            return
        
        if self._ctx.stop_playback_event.is_set():
            self._ctx.stop_playback_event.clear()

        try:
            self.current_song = self._ctx.music_queue.pop(0)

            if not self._ctx.current_song:
                print("Music queue is empty.")
                return
            
            data, fs = sf.read(self._ctx.current_song['file_path'], dtype='float32')
            self._ctx.current_song_length = len(data)
        except Exception as e:
            print('Playback initialization error: {}'.format(e))
            return

        def callback(outdata, frames, time, status):
            if status:
                print(status)
            chunksize = min(len(data) - self._ctx.current_frame, frames)
            outdata[:chunksize] = data[self._ctx.current_frame:self._ctx.current_frame + chunksize]
            if chunksize < frames:
                outdata[chunksize:] = 0
                self.skip()
                raise sd.CallbackStop()
            self._ctx.current_frame += chunksize

        try:
            stream = sd.OutputStream(
                samplerate=fs, device=sd.default.device, channels=data.shape[1],
                callback=callback, finished_callback=self._ctx.stop_playback_event.set)
            with stream:
                while not self._ctx.stop_playback_event.is_set():
                    if not self._ctx.command_queue.empty():
                        user_command = self._ctx.command_queue.get()
                        print(f"Received command: {user_command.get_ID()}")
                    else:
                        user_command = None
                    
                    if self._ctx.error_count != 0: self._ctx.error_count = 0

                    try:
                        if user_command.get_ID() != "PLAY":
                            user_command.execute()
                    except Exception as e:
                        print(f"Error executing command {user_command.get_ID()}: {e}")
        except Exception as e:
            print('Playback error: {}'.format(e))

            if self._ctx.error_count < MAX_TRIES:
                print('Attempting to reinitialize playback...')
                self._ctx.error_count += 1
                self._ctx.command_queue.put(self._ctx.play_command.get_ID())
                self._ctx.stop_playback_event.set()
                self._ctx.music_queue.insert(0, self._ctx.current_song)
                self._ctx.current_song = None
                self._ctx.play()
            else:
                print('Max attampts reached, stopping playback...')
                self._ctx.stop()

            return
            