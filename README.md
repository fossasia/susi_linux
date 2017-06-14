# Susi Hardware

[![Join the chat at https://gitter.im/fossasia/susi_hardware](https://badges.gitter.im/fossasia/susi_hardware.svg)](https://gitter.im/fossasia/susi_hardware?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Hardware for SUSI AI

This project aims at creating an implementation of Susi, capable to run on Hardware Devices in a headless mode.
It will enable you to bring Susi AI intelligence to all devices you may think like a Speaker, Car etc.

**Current Status**
- Voice Detection working with Google Speech API.
- Voice Output working with Festival TTS.
- Susi AI response working through Susi AI API Python Wrapper(https://github.com/fossasia/susi_api_wrapper)

**Roadmap**
- Enable "Susi" Hotword Detection
- Offline Voice Detection (if possible with satisfactory results)
- Provision of more services for online Voice Detection and make it a user choice.
- Add more/better voice/tts engines to give more realistic feel to Susi Voice.
- Add hardware specific options like Susi Wake Button.


## Setting up Susi Hardware

Setting up Susi Hardware is pretty easy.

### Minimal Requirements
* A hardware device capable to run Linux.
* A Linux Based Distribution.
* Any Microphone/Speaker for Input/Output

### Setting Up (Ubuntu/ Debian)
* Install Python Version: 3.5+
    * ```sudo apt install python3```
    * ```sudo apt install python3-pip```

* Install flite
    * ```sudo apt install flite```

* Setup PyAudio
    * Install PortAudio ```sudo apt-get install portaudio19-dev```
    * Install PyAudio ```sudo pip3 install pyaudio```
 

### Setting Up (Language: en/us) (Arch Linux)

* Install Python Version: 3.5+ 
    * ```sudo pacman -Sy python```
    * ```sudo pacman -Sy python-pip```

* Install Flite TTS
    * sudo pacman -Sy flite

* Setup PyAudio 
    * Install PyAudio ```sudo pip3 install pyaudio```

### Raspberry Pi setup

- Distribution: Raspbian Jesse Lite

* Install required tools
    -    ```sudo apt install git swig portaudio19-dev pulseaudio libpulse-dev unzip```
* Download zip packages for Pocketsphinx
    -    ``` wget https://pypi.python.org/packages/0f/db/d830b477f97fdce5bf575dbf8abc090208e0b3e5956b533adb0f56c8f973/pocketsphinx-0.1.3.zip ```
* unzip Package
    - ```unzip pocketsphinx-0.1.3.zip```
* Install package
    - ``` cd pocketsphinx-0.1.3/ ```
    - ``` sudo python3 setup.py install ```

**Note**: If you get an error, reading a line in README.rst, just comment that line.

* Check if your devices show up:
    - For Recording Devices: ```arecord -l```
    - For Playback Devices: ```aplay -l```

## Running Susi
* Go to app directory
* Run ```./install.sh```
* After installation of dependencies, run ```python3 main.py```
* Say "Susi" to trigger speech recognition. You will see "Hotowrd Detected" on your console as an indicative message for detection. 
* Once detection triggers, ask Susi any question by speech.
* Susi will reply back with its answer using Flite TTS.