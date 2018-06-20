#! /bin/bash
STT="$1"
TTS="$2"
HOTWORD="$3"
WAKE="$4"
AUTH="$5"
EMAIL="$6"
PASS="$7"

cd /home/pi/SUSI.AI/susi_linux
sudo python3 config_generator.py $STT $TTS $HOTWORD $WAKE $AUTH $EMAIL $PASS
