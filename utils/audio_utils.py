import wave
import pyaudio


class AudioFile(object):
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        while len(data) > 0:
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)
        self.wf.rewind()

    def close(self):
        """ Graceful shutdown """
        self.stream.close()
        self.p.terminate()


# bell sound after hotword detected
detection_bell = AudioFile("extras/detection-bell.wav")
