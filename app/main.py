import susi_python as susi
import speech.TTS as TTS
import speech_recognition as sr
import queue as queue

from threading import Thread
import asyncio
import websockets

from speech.SphinxRecognizer import SphinxRecognizer
import pyaudio

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 1000

# Make a queue for Storing queries by user
queries_queue = queue.Queue()

# TODO: Set parameters from environment variable.
# Currently, please set the variables for microphone initialization below manually.
# Refer following link for more information about parameters
# https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst#microphonedevice_index--none-sample_rate--16000-chunk_size--1024

# microphone = sr.Microphone(device_index=2, sample_rate=48000, chunk_size=2048)
microphone = sr.Microphone()


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
        print("Energy Threshold " + str(recognizer.energy_threshold))
        with microphone as source:
            audio = recognizer.listen(source, phrase_time_limit=5)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = recognizer.recognize_google(audio)
            queries_queue.put(value)
            # query susi for the question
            askSusi(value)

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

async def consumer(message):
    print(message)


async def consumer_handler(websocket):
    while True:
        message = await websocket.recv()
        await consumer(message)


async def producer():
    return queries_queue.get()


async def producer_handler(websocket):
    while True:
        message = await producer()
        await websocket.send(message)

async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(consumer_handler(websocket))
    producer_task = asyncio.ensure_future(producer_handler(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()


def start_server_thread(handler, loop):
    start_server = websockets.serve(handler, '127.0.0.1', 5678)
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


# TODO: Decide threshold by a training based system.
# adjust threshold manually for now.
sphinxRecognizer = SphinxRecognizer(threshold=1e-23)

loop = asyncio.get_event_loop()
thread = Thread(target=start_server_thread, args=(handler, loop,))
thread.start()

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

thread.join()
