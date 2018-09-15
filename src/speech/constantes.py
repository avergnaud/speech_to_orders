import pyaudio

FORMAT = pyaudio.paInt16

CHANNELS = 1

RATE = 16000

CHUNK = int(RATE / 10)

SILENCE_LIMIT = 3  # Silence limit in seconds. The max ammount of seconds where
                   # only silence is recorded. When this time passes the
                   # recording finishes and the file is delivered.

PREV_AUDIO = 1  # Previous speech (in seconds) to prepend. When noise
                  # is detected, how much of previously recorded speech is
                  # prepended. This helps to prevent chopping the beggining
                  # of the phrase.

SEUIL_INTENSITE_THRESHOLD = 150

NB_FRAMES_SUPERIEUR = 3