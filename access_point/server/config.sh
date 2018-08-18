#! /bin/bash

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

STT="$1"
TTS="$2"
HOTWORD="$3"
WAKE="$4"

cd $DIR_PATH/../../
sudo python3 config_generator.py $STT $TTS $HOTWORD $WAKE

sudo systemctl daemon-reload
sudo systemctl disable ss-python-flask.service
sudo systemctl enable ss-susi-linux.service
sudo systemctl enable ss-factory-daemon.service

sleep 5
cd $DIR_PATH/../
sudo ./rwap.sh
