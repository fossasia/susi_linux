#! /bin/bash

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

cp $DIR_PATH/Systemd/ss-update-daemon.service /lib/systemd/system/ss-update-daemon.service
cp $DIR_PATH/Systemd/ss-susi-server.service /lib/systemd/system/ss-susi-server.service
cp $DIR_PATH/Systemd/ss-python-flask.service /lib/systemd/system/ss-python-flask.service
cp $DIR_PATH/Systemd/ss-susi-linux.service /lib/systemd/system/ss-susi-linux.service
cp $DIR_PATH/Systemd/ss-startup-audio.service /lib/systemd/system/ss-startup-audio.service

sudo systemctl daemon-reload
sudo systemctl enable ss-update-daemon.service
sudo systemctl enable ss-susi-server.service
sudo systemctl enable ss-python-flask.service
