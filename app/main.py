import susi_python as susi
import speech.TTS as TTS
import speech_recognition as sr

from speech.SphinxRecognizer import SphinxRecognizer
import pyaudio

r = sr.Recognizer()
r.dynamic_energy_threshold = False
r.energy_threshold = 1000

# TODO: Set parameters from environment variable.
# Currently, please set the variables for microphone initialization below manually.
# Refer following link for more information about parameters
# https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst#microphonedevice_index--none-sample_rate--16000-chunk_size--1024

#m = sr.Microphone(device_index=2, sample_rate=48000, chunk_size=2048)
m = sr.Microphone()


def speak(text):
    # Switch tts service here
    TTS.speak_flite_tts(text)
    # TTS.speak_watson_tts(text)


def askSusi(input_query):
    print(input_query)
    # get reply by Susi
    reply = susi.ask(input_query)

    if 'answer' in reply.keys():
        print('Susi:' + reply['answer'])
        # Call festival tts to reply the response by Susi
        speak(reply['answer'])
    else:
        speak("I don't have an answer to this")


def start_speech_recognition():
    try:
        # print("A moment of silence, please...")
        # with m as source:
        #     r.adjust_for_ambient_noise(source)

        print("Say something!")
        print("Energy Threshold " + str(r.energy_threshold))
        with m as source:
            audio = r.listen(source, phrase_time_limit=5)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            # query susi for the question
            askSusi(format(value))

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

    except KeyboardInterrupt:
        pass


p = pyaudio.PyAudio()

stream = None


def open_stream():
    global stream
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=30480)
    stream.start_stream()


def close_stream():
    global stream
    stream.stop_stream()
    stream.close()


open_stream()

# TODO: Decide threshold by a training based system.
# adjust threshold manually for now.
sphinxRecognizer = SphinxRecognizer(threshold=1e-23)

while True:
    buffer = stream.read(30480, exception_on_overflow=False)
    if buffer:
        if sphinxRecognizer.is_recognized(buffer):
            print("hotword detected")
            close_stream()
            start_speech_recognition()
            open_stream()
    else:
        break
