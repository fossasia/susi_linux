import susi_python as susi
import subprocess
import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()


def speak(text):
    filename = '.response'
    file=open(filename,'w')
    file.write(text)
    file.close()
    # Call festival tts to reply the response by Susi
    subprocess.call('festival --tts '+filename, shell=True)


def askSusi(input_query):
    print(input_query)
    # get reply by Susi
    reply = susi.ask(input_query)
    print('Susi:' + reply)
    # Call festival tts to reply the response by Susi
    speak(reply)


try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
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
