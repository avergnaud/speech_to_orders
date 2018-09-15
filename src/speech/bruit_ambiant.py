import pyaudio
import speech.constantes
import math
import audioop


def audio_int(num_samples=50):
    """ Gets average speech intensity of your mic sound. You can use it to get
        average intensities while you're talking and/or silent. The average
        is the avg of the 20% largest intensities recorded.
    """

    print("Getting intensity values from mic.")
    p = pyaudio.PyAudio()

    stream = p.open(format=speech.constantes.FORMAT,
                    channels=speech.constantes.CHANNELS,
                    rate=speech.constantes.RATE,
                    input=True,
                    frames_per_buffer=speech.constantes.CHUNK)

    values = [math.sqrt(abs(audioop.avg(stream.read(speech.constantes.CHUNK), 4)))
              for x in range(num_samples)]
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print(" Finished ")
    print(" Average speech intensity is ", r)
    stream.close()
    p.terminate()
    # 2400 c'est pas mal au micro
    return r