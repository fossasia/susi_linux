import susi_python as susi
import subprocess
import speech_recognition as sr

from pocketsphinx.pocketsphinx import *
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


modeldir = "/usr/share/pocketsphinx/model"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us'))
config.set_string('-dict', os.path.join(modeldir, 'en-us/cmudict-en-us.dict'))
config.set_string('-keyphrase', 'susi')
# adjust threshold according to your device. Implementation to be optimized later.
config.set_float('-kws_threshold', 1e-20)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

# Process audio chunk by chunk. On keyword detected perform action and restart search
decoder = Decoder(config)
decoder.start_utt()

while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
    else:
        break
    if decoder.hyp() is not None:
        # uncomment following line if you wish to see more debug info
        # print([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
        print("Hotword Detected")
        decoder.end_utt()
        start_speech_recognition()
        decoder.start_utt()
    else:
        pass
