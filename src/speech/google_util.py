import io
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def stt_google_wav(audio_fname):
    """ Sends speech file (audio_fname) to Google's text to speech
            service and returns service's response. We need a FLAC
            converter if speech is not FLAC (check FLAC_CONV). """
    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the speech into memory
    with io.open(audio_fname, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='fr-FR')

    # Detects speech in the speech file
    resp = client.recognize(config, audio)

    retour = ""
    for result in resp.results:
        retour += " " + result.alternatives[0].transcript

    return retour
