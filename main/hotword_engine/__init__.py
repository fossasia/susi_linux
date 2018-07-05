"""
This module defines all the hotword detection engines present in the app.
Presently, it support
* PocketSphinx KeyPhrase Search for Hotword Detection
* Snowboy Hotword Detection

While Snowboy gives marginally better results, if it is unavailable on your device,
you may use PocketSphinx
"""

def import_hotword():
    try:
        from snowboy_detector import SnowboyDetector

    except ImportError:
           print('Snowboy Detector is not present.')
           print('Use Pocket Sphinx Detector instead.')

    try: 
        from sphinx_detector import PocketSphinxDetector

    except ImportError:
       print('PocketSphinx is not properly installed.')
       print('We recommend using Snowboy')
   
  
  
import_hotword()
