# Susi Linux

[![Build Status](https://travis-ci.org/fossasia/susi_hardware.svg?branch=master)](https://travis-ci.org/fossasia/susi_hardware) 
[![Join the chat at https://gitter.im/fossasia/susi_hardware](https://badges.gitter.im/fossasia/susi_hardware.svg)](https://gitter.im/fossasia/susi_hardware?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

SUSI AI on Linux

This project aims at creating an implementation of Susi, capable to run on Linux Devices in a headless mode.
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


## Setting up Susi on Linux

Setting up Susi on Linux is pretty easy.

### Minimal Requirements
* A hardware device capable to run Linux. It included development boards like Raspberry Pi 
and other generic machines.
* A Debian based Linux Distribution. Tested on
    - Raspbian on Raspberry Pi 3
    - Ubuntu 64bit on x64 architecture
* A microphone for input. If you are using a development board like Raspberry Pi which does not have microphone
inbuilt, you can use a USB Microphone.
* A Speaker for Output. On development boards like Raspberry Pi, you can use a portable speaker that connects through
3.5mm audio jack.

### Installation on Raspberry Pi

For installation on Raspberry Pi, read [Raspberry Pi setup guide.](docs/raspberry-pi_install.md)

### Installing on Ubuntu and other Debian based distributions

For installation on Ubuntu and other Debian based distributions, read [Ubuntu Setup Guide](docs/ubuntu_install.md)