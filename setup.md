# Setting up Susi Hardware

## Minimal Requirements
* A hardware device capable to run Linux.
* A Linux Based Distribution.
* Microphone/Speaker for Input/Output 

## Setting Up (Ubuntu/ Debian)
To be added shortly.

## Setting Up (Language: en/us) (Arch Linux)

* Python Version: 3.5+

* Install Festival TTS and voices
    * Install Festival ```sudo pacman -S festival```
    * Install English Voices ```sudo pacman -S festival-english```
    * Install English US voices ```sudo pacman -S festival-us```
    
* If you are using Sound Server like ALSA/PulseAudio (quite probable), configure festival to use Sound Server
    * Edit your ~/.festivalrc and add these lines at the end
        ```
        (Parameter.set 'Audio_Required_Format 'aiff)
        (Parameter.set 'Audio_Method 'Audio_Command)
        (Parameter.set 'Audio_Command "paplay $FILE --client-name=Festival --stream-name=Speech")
        ```

* Set US English Female Voice for Output. Edit your ~/.festivalrc and add these lines at the end
    ```
    (set! voice_default voice_cmu_us_cg)
    ```

* Setup PyAudio 
    * Install PyAudio ```sudo pip3 install pyaudio```
    
## Running Susi
* Go to src directory
* Run ./install.sh
* After installtion of dependencies, run app.py
