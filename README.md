# Susi Hardware

[![Join the chat at https://gitter.im/fossasia/susi_hardware](https://badges.gitter.im/fossasia/susi_hardware.svg)](https://gitter.im/fossasia/susi_hardware?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Hardware for SUSI AI

This project aims at creating an implementation of Susi, capable to run on Hardware Devices in a headless mode.
It will enable you to bring Susi AI intelligence to all devices you may think like a Speaker, Car etc.

**Current Status**
- Voice Detection working with Google Speech API/ IBM Watson Speech to Text API.
- Voice Output working with Google TTS/ IBM Watson TTS/ Flite TTS.
- Susi AI response working through Susi AI API Python Wrapper(https://github.com/fossasia/susi_api_wrapper)
- Hotword Detection works for hotword 'Susi'
- Susi Webchat connect mode works to connect Susi Hardware client to Webchat Client (in alpha stages)

**Roadmap**
- Offline Voice Detection (if possible with satisfactory results)
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

* Install Required Tools
    * ```sudo apt install git swig3.0 portaudio19-dev pulseaudio libpulse-dev unzip sox libatlas-dev libatlas-base-dev libsox-fmt-all```

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

- Distribution: Raspbian Jessie

* Install required tools
    -    ```sudo apt install git swig3.0 portaudio19-dev pulseaudio libpulse-dev unzip sox libatlas-dev libatlas-base-dev libsox-fmt-all```

* Check if your speaker and microphone devices show up:
    - For Recording Devices (Microphone) : ```arecord -l```
    - For Playback Devices (Speaker) : ```aplay -l```

## Running Susi
* Run ```./install.sh```
* After installation of dependencies, generate a config file by running ```python3 config_generator.py```
* After the creation of config.json file, run SUSI by ```python3 main.py```
* Say "Susi" to trigger speech recognition. You will see "Hotword Detected" on your console as an indicative message for detection.
* Once detection triggers, ask Susi any question by speech.
* Susi will reply back with its answer.
