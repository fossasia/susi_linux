import os

from pocketsphinx import Decoder


class SphinxRecognizer(object):
    def __init__(self, threshold, sample_rate=16000):
        self.lang = "en-us"
        self.sample_rate = sample_rate
        self.threshold = threshold
        dict_name = "cmudict-en-us.dict"
        self.decoder = Decoder(self.create_config(dict_name))

    def create_config(self, dict_name):
        modeldir = "/usr/lib/python3.6/site-packages/pocketsphinx/model"
        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(modeldir, 'en-us'))
        config.set_string('-keyphrase', 'susi')
        config.set_string('-dict', os.path.join(modeldir, dict_name))
        config.set_float('-kws_threshold',self.threshold)
        config.set_string('-logfn', '/dev/null')
        # TODO: Optimize use of following parameters
        #config.set_float('-samprate', self.sample_rate)
        #config.set_int('-nfft', 2048)
        return config

    def start(self):
        self.decoder.start_utt()

    def stop(selfs):
        selfs.decoder.end_utt()

    def transcribe(self, byte_data):
        self.decoder.start_utt()
        self.decoder.process_raw(byte_data, False, False)
        self.decoder.end_utt()
        return self.decoder.hyp()

    def is_recognized(self, byte_data):
        hyp = self.transcribe(byte_data)
        return hyp
