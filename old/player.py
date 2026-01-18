from pydub import AudioSegment
from Library import Library
from Queue import Queue
import simpleaudio as sa, time, reader

prev_control = ','
skip_control = '.'
stop_control = '/'
pause_control = ' '
new_album_detected = False
new_album_uid = 0

def play_queue(music_queue, lib, play_index = 0, playback_start = 0):
    user_lib = lib
    print(user_lib.get_lib())

    if play_index < 0:
        play_index = 0

    if play_index > music_queue.get_length() - 1:
        return

    while play_index < music_queue.get_length() - 1:
        current_item = music_queue.get_item_by_index(play_index)

        if not current_item.get_is_playable():
            play_index += 1
            continue

        print("Now Playing:", current_item.get_name()) 

        audio = AudioSegment.from_file(current_item.get_path(), current_item.get_format())
        song_length = len(audio) / 1000
        start = time.time()
        offset = playback_start / 1000
        audio = audio[playback_start:]
        playback_start = 0

        play_obj = sa.play_buffer(
            audio.raw_data,
            num_channels = audio.channels,
            bytes_per_sample = audio.sample_width,
            sample_rate = audio.frame_rate
        )

        while True:
            if play_obj.is_playing():
                elapsed = time.time() - start + offset

            '''
            if ord(c) == ord(skip_control):
                playback_start = 0
                play_obj.stop()
                play_index += 1
                break
            elif ord(c) == ord(stop_control):
                playback_start = 0
                play_obj.stop()
                return
            elif ord(c) == ord(prev_control):
                playback_start = 0
                play_obj.stop()
                play_index -= 1
                break
            elif ord(c) == ord(pause_control):
                if playback_start == 0:
                    print('Pausing playback...')
                    #print(elapsed)
                    playback_start = elapsed * 1000
                    #print(playback_start)
                    play_obj.stop()
                else:
                    print('Resuming playback...')
                    break
            '''

            new_album_uid = reader.listen_non_blocking()

            if new_album_uid != 0 and user_lib.check_for(new_album_uid):
                print('New album detected...')
                new_album_detected = True
                break
            
            if elapsed > song_length:
                playback_start = 0
                play_index += 1
                break
            
        play_obj.stop()
        break

    if new_album_detected:
        music_dir = user_lib.search(new_album_uid)
        current_queue = Queue()
        current_queue.populate(music_dir)
        play_queue(current_queue, user_lib)
