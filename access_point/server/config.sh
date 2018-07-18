#! /bin/bash

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

STT="$1"
TTS="$2"
HOTWORD="$3"
WAKE="$4"

cd $DIR_PATH/../../
sudo python3 config_generator.py $STT $TTS $HOTWORD $WAKE
