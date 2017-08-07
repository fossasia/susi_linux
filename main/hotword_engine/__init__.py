"""
This module defines all the hotword detection engines present in the app.
Presently, it support
* PocketSphinx KeyPhrase Search for Hotword Detection
* Snowboy Hotword Detection

While Snowboy gives marginally better results, if it is unavailable on your device,
you may use PocketSphinx
"""
from .snowboy_detector import SnowboyDetector
from .sphinx_detector import PocketSphinxDetector
