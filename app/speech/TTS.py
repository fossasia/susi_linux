import subprocess


def speak_flite_tts(text):
    filename = '.response'
    file = open(filename, 'w')
    file.write(text)
    file.close()
    # Call flite tts to reply the response by Susi
    subprocess.call('flite -voice file://cmu_us_slt.flitevox -f ' + filename, shell=True)