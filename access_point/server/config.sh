#! /bin/bash
STT="$1"
TTS="$2"
HOTWORD="$3"
WAKE="$4"

cd $HOME/SUSI.AI/susi_linux
sudo python3 config_generator.py $STT $TTS $HOTWORD $WAKE
