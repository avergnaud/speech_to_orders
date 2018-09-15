import speech.bruit_ambiant
import speech.file_util
import speech.google_util
import speech.constantes
import pyaudio
import os
import audioop
import math
from collections import deque
import orders.order_util


THRESHOLD = int(speech.bruit_ambiant.audio_int()) + speech.constantes.SEUIL_INTENSITE_THRESHOLD  # 2500 The threshold intensity that defines silence
                  # and noise signal (an int. lower than THRESHOLD is silence).


def listen_for_speech(num_phrases=-1):
    """
    Listens to Microphone, extracts phrases from it and sends it to
    Google's TTS service and returns response. a "phrase" is sound
    surrounded by silence (according to threshold). num_phrases controls
    how many phrases to process before finishing the listening process
    (-1 for infinite).
    """

    # Open stream
    p = pyaudio.PyAudio()

    stream = p.open(format=speech.constantes.FORMAT,
                    channels=speech.constantes.CHANNELS,
                    rate=speech.constantes.RATE,
                    input=True,
                    frames_per_buffer=speech.constantes.CHUNK)

    print("* Listening mic. ")
    audio2send = []
    cur_data = ''  # current chunk  of speech data
    rel = speech.constantes.RATE / speech.constantes.CHUNK
    max_len_silence = int(speech.constantes.SILENCE_LIMIT * rel)
    slid_win = deque(maxlen=max_len_silence)
    #Prepend speech from PREV_AUDIO seconds before noise was detected
    max_len_prev = int(speech.constantes.PREV_AUDIO * rel)
    prev_audio = deque(maxlen=max_len_prev)
    started = False
    n = num_phrases
    response = []

    while (num_phrases == -1 or n > 0):
        cur_data = stream.read(speech.constantes.CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        #print slid_win[-1]
        la_somme = sum([x > THRESHOLD for x in slid_win])
        if(la_somme > speech.constantes.NB_FRAMES_SUPERIEUR):
            #print('la_somme ' + str(la_somme))
            if(not started):
                print("Starting record of phrase")
                started = True
            audio2send.append(cur_data)
        elif (started is True):
            print("Finished")
            # The limit was reached, finish capture and deliver.
            filename = speech.file_util.save_speech(list(prev_audio) + audio2send, p)
            # Send file to Google and get response
            r = speech.google_util.stt_google_wav(filename)
            if num_phrases == -1:
                print("Response", r)
                order_json_payload = orders.order_util.translate_to_order(r)
                order_response = orders.order_util.post_order(order_json_payload)
                print(order_response)
            else:
                response.append(r)
            # Remove temp file. Comment line to review.
            os.remove(filename)
            # Reset all
            started = False
            max_len_silence = int(speech.constantes.SILENCE_LIMIT * rel)
            slid_win = deque(maxlen=max_len_silence)
            max_len_prev = int(0.5 * rel)
            prev_audio = deque(maxlen=max_len_prev)
            audio2send = []
            n -= 1
            print("Listening ...")
        else:
            prev_audio.append(cur_data)

    print("* Done recording")
    stream.close()
    p.terminate()

    return response


if __name__ == '__main__' :
    listen_for_speech()  # listen to mic.

