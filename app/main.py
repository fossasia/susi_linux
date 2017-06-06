import susi_python as susi
import subprocess
import speech_recognition as sr

from speech.SphinxRecognizer import SphinxRecognizer
import pyaudio


r = sr.Recognizer()
m = sr.Microphone()

def speak(text):
    filename = '.response'
    file = open(filename, 'w')
    file.write(text)
    file.close()
    # Call festival tts to reply the response by Susi
    subprocess.call('festival --tts ' + filename, shell=True)


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
        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)

        print("Say something!")
        with m as source:
            audio = r.listen(source)
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
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=20480)
stream.start_stream()

sphinxRecognizer = SphinxRecognizer(threshold=1e-20)

while True:
    buffer = stream.read(20480, exception_on_overflow=False)
    if buffer:
        if sphinxRecognizer.is_recognized(buffer):
            start_speech_recognition()
    else:
        break
