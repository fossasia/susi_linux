import os
import pocketsphinx


class SphinxRecognizer(object):
    def __init__(self, threshold, sample_rate=16000):
        self.lang = "en-us"
        self.sample_rate = sample_rate
        self.threshold = threshold
        dict_name = "cmudict-en-us.dict"
        self.decoder = pocketsphinx.Decoder(self.create_config(dict_name))

    def create_config(self, dict_name):
        pocketsphinx_dir = os.path.dirname(pocketsphinx.__file__)
        model_dir = os.path.join(pocketsphinx_dir, "model")
        config = pocketsphinx.Decoder.default_config()
        config.set_string('-hmm', os.path.join(model_dir, 'en-us'))
        config.set_string('-keyphrase', 'susi')
        config.set_string('-dict', os.path.join(model_dir, dict_name))
        config.set_float('-kws_threshold', self.threshold)
        config.set_string('-logfn', '/dev/null')
        config.set_string('-verbose', 'true')
        # TODO: Optimize use of following parameters
        # config.set_float('-samprate', self.sample_rate)
        # config.set_int('-nfft', 2048)
        return config

    def start(self):
        self.decoder.start_utt()

    def stop(self):
        self.decoder.end_utt()

    def transcribe(self, byte_data):
        self.decoder.start_utt()
        self.decoder.process_raw(byte_data, False, False)
        self.decoder.end_utt()
        return self.decoder.hyp()

    def is_recognized(self, byte_data):
        hyp = self.transcribe(byte_data)
        return hyp
