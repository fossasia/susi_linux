"""
This module defines all the hotword detection engines present in the app.
Presently, it support
* PocketSphinx KeyPhrase Search for Hotword Detection
* Snowboy Hotword Detection

While Snowboy gives marginally better results, if it is unavailable on your device,
you may use PocketSphinx
"""
SNOWBOY_AVAILABLE = False
POCKETSPHINX_AVAILABLE = False
try:
    from snowboy.snowboydetect import SnowboyDetect
    SNOWBOY_AVAILABLE = True
except ImportError:
    pass

try:
    from .sphinx_detector import PocketSphinxDetector
    POCKETSPHINX_AVAILABLE = True
except ImportError:
    pass

if SNOWBOY_AVAILABLE is True:
    print("Snowboy successfully imported.")
else:
    print("Snowboy not currently installed. You may use PocketSphinx instead or you need to install it from https://github.com/Kitt-AI/snowboy.")

if POCKETSPHINX_AVAILABLE is True:
    print("PocketSphinx successfully imported.")
else:
    print("PocketSphinx is not currently installed. You may use Snowboy instead.")

if SNOWBOY_AVAILABLE is True and POCKETSPHINX_AVAILABLE is True:
    print("Both Snowboy and PocketSphinx successfully imported. We will recommend using Snowboy.")
